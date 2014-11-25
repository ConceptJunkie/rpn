#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnOutput.py
#//
#//  RPN command-line calculator output functions
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import arrow
import builtins
import bz2
import contextlib
import math
import os
import pickle
import string
import textwrap

from mpmath import *

from rpnDeclarations import PROGRAM_NAME, PROGRAM_DESCRIPTION
from rpnMeasurement import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  debugPrint
#//
#//******************************************************************************

def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


#//******************************************************************************
#//
#//  roundMantissa
#//
#//******************************************************************************

def roundMantissa( mantissa, accuracy ):
    if len( mantissa ) <= accuracy:
        return mantissa

    lastDigit = int( mantissa[ accuracy - 1 ] )
    extraDigit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extraDigit >= 5:
        result += str( lastDigit + 1 )
    else:
        result += str( lastDigit )

    return result


#//******************************************************************************
#//
#//  formatOutput
#//
#//  This takes a string representation of the result and formats it according
#//  to a whole bunch of options.
#//
#//******************************************************************************

def formatOutput( output ):
    # filter out text strings
    for c in output:
        if c in '+-.':
            continue

        if c in string.whitespace or c in string.punctuation:
            return output

    # override settings with temporary settings if needed
    if g.tempCommaMode:
        comma = True
    else:
        comma = g.comma

    if g.tempFindPolyMode:
        pass

    if g.tempHexMode:
        bitwiseGroupSize = 16
        integerGrouping = 4
        leadingZero = True
        outputRadix = 16
    else:
        bitwiseGroupSize = g.bitwiseGroupSize
        integerGrouping = g.integerGrouping
        leadingZero = g.leadingZero
        outputRadix = g.outputRadix

    if g.tempIdentifyMode:
        pass

    if g.tempLeadingZeroMode:
        leadingZero = True
    else:
        leadingZero = g.leadingZero

    if g.tempOctalMode:
        bitwiseGroupSize = 9
        integerGrouping = 3
        leadingZero = True
        outputRadix = 8
    else:
        bitwiseGroupSize = g.bitwiseGroupSize
        integerGrouping = g.integerGrouping
        leadingZero = g.leadingZero
        outputRadix = g.outputRadix

    if g.tempTimeMode:
        pass

    exponentIndex = output.find( 'e' )

    if exponentIndex > 0:
        exponent = int( output[ exponentIndex + 1 : ] )
        output = output[ : exponentIndex ]
    else:
        exponent = 0

    imaginary = im( mpmathify( output ) )

    if imaginary != 0:
        if imaginary < 0:
            imaginary = fabs( imaginary )
            negativeImaginary = True
        else:
            negativeImaginary = False

        imaginaryValue = formatOutput( nstr( imaginary ) )

        strOutput = nstr( re( mpmathify( output ) ) )
    else:
        imaginaryValue = ''
        strOutput = nstr( output, g.outputAccuracy )[ 1 : -1 ]

    if '.' in strOutput:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    integer = strOutput[ 1 if negative else 0 : decimal ]
    integerLength = len( integer )

    mantissa = strOutput[ decimal + 1 : ]

    if mantissa == '0':
        mantissa = ''
    elif ( mantissa != '' ) and ( g.outputAccuracy == -1 ):
        mantissa = mantissa.rstrip( '0' )

    #print( 'integer: ', integer )
    #print( 'mantissa: ', mantissa )
    #print( 'exponent: ', exponent )
    #
    #if exponent > 0:
    #    if exponent > len( mantissa ):
    #        integer += mantissa + '0' * ( exponent - len( mantissa ) )
    #        mantissa = ''
    #    else:
    #        integer += mantissa[ : exponent ]
    #        mantissa = mantissa[ exponent + 1 : ]
    #elif exponent < 0:
    #    exponent = -exponent
    #
    #    if exponent > len( integer ):
    #        mantissa = '0' * ( exponent - len( integer ) ) + integer + mantissa
    #        integer = '0'
    #    else:
    #        mantissa = integer[ exponent : ]
    #        integer = integer[ : exponent - 1 ]

    if outputRadix == g.phiBase:
        integer, mantissa = convertToPhiBase( mpmathify( output ) )
    elif outputRadix == g.fibBase:
        integer = convertToFibBase( floor( mpmathify( output ) ) )
    elif ( outputRadix != 10 ) or ( g.numerals != g.defaultNumerals ):
        integer = str( convertToBaseN( mpmathify( integer ), outputRadix, g.outputBaseDigits, g.numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpmathify( '0.' + mantissa ), outputRadix,
                            int( ( mp.dps - integerLength ) / math.log10( outputRadix ) ),
                            g.outputBaseDigits ) )
    else:
        if g.outputAccuracy <= 0:
            mantissa = ''
        else:
            mantissa = roundMantissa( mantissa, g.outputAccuracy )
            mantissa = mantissa.rstrip( '0' )

    if comma and integerGrouping > 0:
        firstDelimiter = len( integer ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += integer[ : firstDelimiter ]

        for i in range( firstDelimiter, len( integer ), integerGrouping ):
            if integerResult != '':
                integerResult += g.integerDelimiter

            integerResult += integer[ i : i + integerGrouping ]

    else:
        integerResult = integer

    if g.decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( mantissa ), g.decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += g.decimalDelimiter

            mantissaResult += mantissa[ i : i + g.decimalGrouping ]
    else:
        mantissaResult = mantissa

    if negative:
        result = '-'
    else:
        result = ''

    result += integerResult

    if mantissaResult != '':
        result += '.' + mantissaResult

    if imaginaryValue != '':
        result = '( ' + result + ( ' - ' if negativeImaginary else ' + ' ) + imaginaryValue + 'j )'

    if exponent != 0:
        result += 'e' + str( exponent )

    return result


#//******************************************************************************
#//
#//  formatListOutput
#//
#//******************************************************************************

def formatListOutput( result ):
    resultString = '[ '

    for item in result:
        if resultString != '[ ':
            resultString += ', '

        if isinstance( item, list ):
            resultString += formatListOutput( item )
        else:
            if isinstance( item, arrow.Arrow ):
                resultString += formatDateTime( item )
            elif isinstance( item, Measurement ):
                itemString = nstr( item.getValue( ) )

                resultString += formatOutput( itemString )

                resultString += ' ' + formatUnits( item )
            else:
                itemString = str( item )

                resultString += formatOutput( itemString )

    resultString += ' ]'

    return resultString


#//******************************************************************************
#//
#//  formatUnits
#//
#//******************************************************************************

def formatUnits( measurement ):
    value = mpf( measurement )

    if measurement.getUnitName( ) is not None:
        unitString = ''

        if value < mpf( -1.0 ) or value > mpf( 1.0 ):
            tempString = measurement.getPluralUnitName( )
        else:
            tempString = measurement.getUnitName( )

        for c in tempString:
            if c == '_':
                unitString += ' '
            else:
                unitString += c

        return unitString

    unitString = ''

    # first, we simplify the units
    units = measurement.getUnits( ).simplify( )

    # now that we've expanded the compound units, let's format...
    for unit in units:
        exponent = units[ unit ]

        if exponent > 0:
            if unitString != '':
                unitString += ' '

            if value == 1:
                unitString += unit
            else:
                unitString += g.unitOperators[ unit ].plural

            if exponent > 1:
                unitString += '^' + str( int( exponent ) )

    negativeUnits = ''

    if unitString == '':
        for unit in units:
            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits != '':
                    negativeUnits += ' '

                negativeUnits += unit
                negativeUnits += '^' + str( int( exponent ) )
    else:
        for unit in units:
            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits == '':
                    negativeUnits = ' per '
                else:
                    negativeUnits += ' '

                negativeUnits += unit

                if exponent > 1:
                    negativeUnits += '^' + str( int( exponent ) )
                elif exponent < -1:
                    negativeUnits += '^' + str( int( -exponent ) )

    result = ''

    for c in unitString + negativeUnits:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#//******************************************************************************
#//
#//  formatDateTime
#//
#//******************************************************************************

def formatDateTime( datetime ):
    return datetime.format( 'YYYY-MM-DD HH:mm:ss' )


#//******************************************************************************
#//
#//  printParagraph
#//
#//******************************************************************************

def printParagraph( text, indent=0 ):
    lines = textwrap.wrap( text, g.lineLength - ( indent + 1 ) )

    for line in lines:
        print( ' ' * indent + line )


#//******************************************************************************
#//
#//  printOperatorHelp
#//
#//******************************************************************************

def printOperatorHelp( term, operatorInfo, operatorHelp ):
    if operatorInfo.argCount == 1:
        print( 'n ', end='' )
    elif operatorInfo.argCount == 2:
        print( 'n k ', end='' )
    elif operatorInfo.argCount == 3:
        print( 'a b c ', end='' )
    elif operatorInfo.argCount == 4:
        print( 'a b c d ', end='' )
    elif operatorInfo.argCount == 5:
        print( 'a b c d e ', end='' )

    aliasList = [ key for key in g.operatorAliases if term == g.operatorAliases[ key ] ]

    print( term + ' - ' + operatorHelp[ 1 ] )

    print( )

    if len( aliasList ) > 1:
        printParagraph( 'aliases:  ' + ', '.join( aliasList ) )
    elif len( aliasList ) == 1:
        printParagraph( 'alias:  ' + aliasList[ 0 ] )

    print( 'category: ' + operatorHelp[ 0 ] )

    if operatorHelp[ 2 ] == '\n':
        print( )
        print( 'No further help is available.' )
    else:
        print( operatorHelp[ 2 ] )

    print( )

    if operatorHelp[ 3 ] == '\n':
        print( 'No examples are available.' )
    else:
        print( term + ' examples:' )
        print( operatorHelp[ 3 ] )


#//******************************************************************************
#//
#//  printCategoryHelp
#//
#//******************************************************************************

def printCategoryHelp( category, operators, listOperators, modifiers, operatorHelp ):
    printParagraph( 'The ' + category + ' category includes the following operators (with aliases in parentheses):' )
    print( )

    operatorList = [ key for key in operators if operatorHelp[ key ][ 0 ] == category ]
    operatorList.extend( [ key for key in listOperators if operatorHelp[ key ][ 0 ] == category ] )
    operatorList.extend( [ key for key in modifiers if operatorHelp[ key ][ 0 ] == category ] )

    addAliases( operatorList, g.operatorAliases )

    for operator in sorted( operatorList ):
        print( operator )


#//******************************************************************************
#//
#//  printHelp
#//
#//******************************************************************************

def printHelp( operators, listOperators, modifiers, term, interactive = False ):
    loadHelpData( )

    if g.helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    if term == '':
        if interactive:
            printInteractiveHelp( )
        else:
            printGeneralHelp( )
        return

    # first check if the term is an alias and translate
    if term in g.operatorAliases:
        term = g.operatorAliases[ term ]

    # then look for exact matches in all the lists of terms for which we have help support
    if term in operators:
        printOperatorHelp( term, operators[ term ], g.operatorHelp[ term ] )
    elif term in listOperators:
        printOperatorHelp( term, listOperators[ term ], operatorHelp[ term ] )
    elif term in modifiers:
        printOperatorHelp( term, modifiers[ term ], operatorHelp[ term ] )
    elif term in g.helpTopics:
        print( g.helpTopics[ term ] )
    elif term in g.operatorCategories:
        printCategoryHelp( term, operators, listOperators, modifiers, g.operatorHelp )
    elif term == 'unit_types':
        printParagraph( ', '.join( sorted( g.unitTypeDict.keys( ) ) ), 4 )
    elif term in g.unitTypeDict:
        unitList = sorted( g.unitTypeDict[ term ] )
        addAliases( unitList, g.operatorAliases )
        for unit in unitList:
            printParagraph( unit, 4 )
    else:
        # if no exact matches for any topic, let's look for partial matches
        if 'unit_types'.startswith( term ):
            print( 'Interpreting topic as \'unit_types\'.' )
            printParagraph( ', '.join( sorted( g.unitTypeDict.keys( ) ) ), 4 )
            return

        helpTerm = next( ( i for i in g.unitTypeDict if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( )
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            printParagraph( ', '.join( sorted( g.unitTypeDict[ helpTerm ] ) ), 4 )
            return

        helpTerm = next( ( i for i in operators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, operators[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in listOperators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, listOperators[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in modifiers if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, modifiers[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in g.helpTopics if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            print( g.helpTopics[ helpTerm ] )
            return

        helpTerm = next( ( i for i in g.operatorCategories if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printCategoryHelp( helpTerm, operators, listOperators, modifiers, g.operatorHelp )
        else:
            print( "Help topic not found." )


#//******************************************************************************
#//
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( ):
    print( PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
'''For help on a specific topic, add a help topic, operator category or a specific operator name.''' )

    print( )
    print( 'The following is a list of general topics:' )
    print( )

    helpTopics = list( g.helpTopics.keys( ) )
    helpTopics.append( 'unit_types' )

    printParagraph( ', '.join( sorted( helpTopics ) ), 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( g.operatorCategories ) ), 4 )


#//******************************************************************************
#//
#//  printInteractiveHelp
#//
#//******************************************************************************

def printInteractiveHelp( ):
    print( PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
'''For help on a specific topic, use the topic operator with a general topic, operator category or a specific operator name.''' )

    print( )
    print( 'The following is a list of general topics:' )
    print( )

    helpTopics = list( g.helpTopics.keys( ) )
    helpTopics.append( 'unit_types' )

    printParagraph( ', '.join( sorted( helpTopics ) ), 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( g.operatorCategories ) ), 4 )


#//******************************************************************************
#//
#//  printTitleScreen
#//
#//******************************************************************************

def printTitleScreen( programName, programDescription ):
    print( programName, PROGRAM_VERSION, '-', programDescription )
    print( COPYRIGHT_MESSAGE )
    print( )
    print( 'Type "help" for more information, and "exit" to exit.' )

