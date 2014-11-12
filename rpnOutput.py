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

        imaginaryValue = formatOutput( nstr( imaginary, mp.dps ) )

        strOutput = str( re( mpmathify( output ) ) )
    else:
        imaginaryValue = ''
        strOutput = nstr( output, g.accuracy  )[ 1 : -1 ]

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
    elif ( mantissa != '' ) and ( g.accuracy == -1 ):
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

    if g.outputRadix == g.phiBase:
        integer, mantissa = convertToPhiBase( mpmathify( output ) )
    elif g.outputRadix == g.fibBase:
        integer = convertToFibBase( floor( mpmathify( output ) ) )
    elif ( g.outputRadix != 10 ) or ( g.numerals != g.defaultNumerals ):
        integer = str( convertToBaseN( mpmathify( integer ), g.outputRadix, g.outputBaseDigits, g.numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpmathify( '0.' + mantissa ), g.outputRadix,
                            int( ( mp.dps - integerLength ) / math.log10( g.outputRadix ) ),
                            g.outputBaseDigits ) )
    else:
        if g.accuracy == 0:
            mantissa = ''
        elif g.accuracy > 0:
            mantissa = roundMantissa( mantissa, g.accuracy )
            mantissa = mantissa.rstrip( '0' )

    if g.comma and g.integerGrouping > 0:
        firstDelimiter = len( integer ) % g.integerGrouping

        if g.leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( g.integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += integer[ : firstDelimiter ]

        for i in range( firstDelimiter, len( integer ), g.integerGrouping ):
            if integerResult != '':
                integerResult += g.integerDelimiter

            integerResult += integer[ i : i + g.integerGrouping ]

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
                itemString = str( mpf( item ) )

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

def printOperatorHelp( helpArgs, term, operatorInfo, operatorHelp ):
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

def printHelp( programName, programDescription, operators, listOperators, modifiers, helpArgs ):
    loadHelpData( )

    if g.helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    operatorCategories = set( g.operatorHelp[ key ][ 0 ] for key in g.operatorHelp )

    if len( helpArgs ) == 0:
        printGeneralHelp( programName, programDescription, g.basicCategories, operatorCategories )
        return

    term = helpArgs[ 0 ]

    # first check if the term is an alias and translate
    if term in g.operatorAliases:
        term = g.operatorAliases[ term ]

    # then look for exact matches in all the lists of terms for which we have help support
    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ], g.operatorHelp[ term ] )
    elif term in listOperators:
        printOperatorHelp( helpArgs, term, listOperators[ term ], operatorHelp[ term ] )
    elif term in modifiers:
        printOperatorHelp( helpArgs, term, modifiers[ term ], operatorHelp[ term ] )
    elif term in g.basicCategories:
        print( g.basicCategories[ term ] )
    elif term in operatorCategories:
        printCategoryHelp( term, operators, listOperators, modifiers, g.operatorAliases, g.operatorHelp )
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
            printOperatorHelp( helpArgs, helpTerm, operators[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in listOperators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpArgs, helpTerm, listOperators[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in modifiers if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpArgs, helpTerm, modifiers[ helpTerm ], g.operatorHelp[ helpTerm ] )
            return

        helpTerm = next( ( i for i in g.basicCategories if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            print( basicCategories[ helpTerm ] )
            return

        helpTerm = next( ( i for i in operatorCategories if i != term and i.startswith( term ) ), '' )

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

def printGeneralHelp( programName, programDescription, basicCategories, operatorCategories ):
    print( programName + ' ' + PROGRAM_VERSION + ' - ' + programDescription )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
'''For help on a specific topic, add a help topic, operator category or a specific operator name.''' )

    print( )
    print( 'The following is a list of general topics:' )
    print( )

    helpCategories = list( basicCategories.keys( ) )
    helpCategories.append( 'unit_types' )

    printParagraph( ', '.join( sorted( helpCategories ) ), 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( operatorCategories ) ), 4 )


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

