

# //******************************************************************************
# //
# //  rpnOutput.py
# //
# //  RPN command-line calculator output functions
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

import arrow

if six.PY3:
    import builtins

import bz2
import contextlib
import math
import os
import pickle
import string
import textwrap

from mpmath import *

from rpnDate import RPNDateTime
from rpnDeclarations import PROGRAM_NAME, PROGRAM_DESCRIPTION
from rpnMeasurement import *
from rpnNumberTheory import getNthLucasNumber
from rpnPolytope import getNthPolygonalNumber
from rpnPrimeUtils import getNthPrimorial

import rpnGlobals as g


# //******************************************************************************
# //
# //  debugPrint
# //
# //******************************************************************************

def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


# //******************************************************************************
# //
# //  formatNumber
# //
# //  This takes a mpf value and turns it into a string.
# //
# //******************************************************************************

specialBaseFunctions = {
    g.facBase         : fac,
    g.doublefacBase   : fac2,
    g.squareBase      : lambda n: power( n, 2 ),
    g.lucasBase       : getNthLucasNumber,
    g.triangularBase  : lambda n: getNthPolygonalNumber( n, 3 ),
    g.primorialBase   : lambda n: getNthPrimorial( n - 1 ),
}

def formatNumber( number, outputRadix, leadingZero, integerGrouping,  ):
    negative = ( number < 0 )

    if outputRadix == g.fibBase:
        strInteger = convertToFibBase( floor( number ) )
        strMantissa = ''
    elif outputRadix == g.phiBase:
        strInteger, strMantissa = convertToNonintegerBase( number, phi )
    elif outputRadix == g.eBase:
        strInteger, strMantissa = convertToNonintegerBase( number, e )
    elif outputRadix == g.piBase:
        strInteger, strMantissa = convertToNonintegerBase( number, pi )
    elif outputRadix == g.sqrt2Base:
        strInteger, strMantissa = convertToNonintegerBase( number, sqrt( 2 ) )
    elif outputRadix < 0:
        strInteger = convertToSpecialBase( floor( number ), specialBaseFunctions[ outputRadix ] )
        strMantissa = ''
    elif ( outputRadix != 10 ) or ( g.numerals != g.defaultNumerals ):
        strInteger = str( convertToBaseN( floor( number ), outputRadix, g.outputBaseDigits, g.numerals ) )
        strMantissa = str( convertFractionToBaseN( frac( number ), outputRadix,
                                                   int( mp.dps / math.log10( outputRadix ) ),
                                                   g.outputBaseDigits ) )
    else:
        strNumber = nstr( number, n = g.outputAccuracy )

        if '.' in strNumber:
            decimal = strNumber.find( '.' )
        else:
            decimal = len( strNumber )

        strInteger = strNumber[ 1 if negative else 0 : decimal ]
        integerLength = len( strNumber )

        strMantissa = strNumber[ decimal + 1 : ]

        if strMantissa == '0':
            strMantissa = ''
        elif ( strMantissa != '' ) and ( g.outputAccuracy == -1 ):
            strMantissa = strMantissa.rstrip( '0' )

    if integerGrouping > 0:
        firstDelimiter = len( strInteger ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += strInteger[ : firstDelimiter ]

        for i in range( firstDelimiter, len( strInteger ), integerGrouping ):
            if integerResult != '':
                integerResult += g.integerDelimiter

            integerResult += strInteger[ i : i + integerGrouping ]

    else:
        integerResult = strInteger

    if g.decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( strMantissa ), g.decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += g.decimalDelimiter

            mantissaResult += strMantissa[ i : i + g.decimalGrouping ]
    else:
        mantissaResult = strMantissa

    result = integerResult

    if mantissaResult != '':
        result += '.' + mantissaResult

    return result, negative


# //******************************************************************************
# //
# //  formatOutput
# //
# //  This takes a string representation of the result and formats it according
# //  to a whole bunch of options.
# //
# //******************************************************************************

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

    # output settings, which may be overrided by temp settings
    outputRadix = g.outputRadix
    bitwiseGroupSize = g.bitwiseGroupSize
    integerGrouping = g.integerGrouping
    leadingZero = g.leadingZero

    if g.tempHexMode:
        bitwiseGroupSize = 16
        integerGrouping = 4
        leadingZero = True
        outputRadix = 16

    if g.tempLeadingZeroMode:
        leadingZero = True

    if g.tempOctalMode:
        bitwiseGroupSize = 9
        integerGrouping = 3
        leadingZero = True
        outputRadix = 8

    mpOutput = mpmathify( output )

    imaginary = im( mpOutput )
    real = re( mpOutput )

    result, negative = formatNumber( real, outputRadix, leadingZero, integerGrouping )

    if negative:
        result = '-' + result

    if imaginary != 0:
        strImaginary, negativeImaginary = formatNumber( imaginary, outputRadix, leadingZero )
        result = '( ' + result + ( ' - ' if negativeImaginary else ' + ' ) + strImaginary + 'j )'

    return result


# //******************************************************************************
# //
# //  formatListOutput
# //
# //******************************************************************************

def formatListOutput( result, level = 0 ):
    resultString = '[ '

    for item in result:
        if level < g.listFormatLevel:
            resultString += '\n' + ' ' * level * 4
        else:
            if resultString != '[ ':
                resultString += ', '

        if isinstance( item, list ):
            resultString += formatListOutput( item, level + 1 )
        else:
            if isinstance( item, RPNDateTime ):
                resultString += formatDateTime( item )
            elif isinstance( item, Measurement ):
                itemString = nstr( item.getValue( ) )

                resultString += formatOutput( itemString )

                resultString += ' ' + formatUnits( item )
            else:
                itemString = str( item )

                resultString += formatOutput( itemString )

        if level < g.listFormatLevel:
            resultString += ','

    if level < g.listFormatLevel:
        resultString += '\n]'
    else:
        resultString += ' ]'

    return resultString


# //******************************************************************************
# //
# //  formatUnits
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  formatDateTime
# //
# //******************************************************************************

def formatDateTime( datetime ):
    if not isinstance( datetime, RPNDateTime ):
        raise ValueError( 'expected RPNDateTime' )

    if datetime.getDateOnly( ):
        return datetime.format( 'YYYY-MM-DD' )
    else:
        return datetime.format( 'YYYY-MM-DD HH:mm:ss' )


# //******************************************************************************
# //
# //  printParagraph
# //
# //******************************************************************************

def printParagraph( text, indent = 0 ):
    lines = textwrap.wrap( text, g.lineLength - ( indent + 1 ) )

    for line in lines:
        print( ' ' * indent + line )


# //******************************************************************************
# //
# //  printOperatorHelp
# //
# //******************************************************************************

def printOperatorHelp( term, operatorInfo, operatorHelp ):
    if operatorInfo.argCount == 1:
        print( 'n ', end = '' )
    elif operatorInfo.argCount == 2:
        print( 'n k ', end = '' )
    elif operatorInfo.argCount == 3:
        print( 'a b c ', end = '' )
    elif operatorInfo.argCount == 4:
        print( 'a b c d ', end = '' )
    elif operatorInfo.argCount == 5:
        print( 'a b c d e ', end = '' )

    aliasList = [ key for key in g.operatorAliases if term == g.operatorAliases[ key ] ]

    print( term + ' - ' + operatorHelp[ 1 ] )

    print( )

    if len( aliasList ) > 1:
        printParagraph( 'aliases:  ' + ', '.join( aliasList ) )
    elif len( aliasList ) == 1:
        printParagraph( 'alias:  ' + aliasList[ 0 ] )

    print( 'category: ' + operatorHelp[ 0 ] )

    if operatorHelp[ 2 ] == '' or operatorHelp[ 2 ] == '\n':
        print( )
        print( 'No further help is available.' )
        print( )
    else:
        print( operatorHelp[ 2 ] )

    if len( operatorHelp ) > 3:
        if operatorHelp[ 3 ] == '' or operatorHelp[ 3 ] == '\n':
            print( 'No examples are available.' )
        else:
            print( term + ' examples:' )
            print( operatorHelp[ 3 ] )
    else:
        print( 'No examples are available.' )


# //******************************************************************************
# //
# //  printCategoryHelp
# //
# //******************************************************************************

def printCategoryHelp( category, operators, listOperators, modifiers, operatorHelp ):
    printParagraph( 'The ' + category + ' category includes the following operators (with aliases in parentheses):' )
    print( )

    operatorList = [ key for key in operators if operatorHelp[ key ][ 0 ] == category ]
    operatorList.extend( [ key for key in listOperators if operatorHelp[ key ][ 0 ] == category ] )
    operatorList.extend( [ key for key in modifiers if operatorHelp[ key ][ 0 ] == category ] )

    addAliases( operatorList, g.operatorAliases )

    for operator in sorted( operatorList ):
        print( operator )


# //******************************************************************************
# //
# //  printHelp
# //
# //******************************************************************************

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
        printOperatorHelp( term, listOperators[ term ], g.operatorHelp[ term ] )
    elif term in modifiers:
        printOperatorHelp( term, modifiers[ term ], g.operatorHelp[ term ] )
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


# //******************************************************************************
# //
# //  printGeneralHelp
# //
# //******************************************************************************

def printGeneralHelp( ):
    print( PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
'''For help on a specific topic, use 'rpn help' and add a help topic, operator category or a specific operator name.''' )

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


# //******************************************************************************
# //
# //  printInteractiveHelp
# //
# //******************************************************************************

def printInteractiveHelp( ):
    loadHelpData( )

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


# //******************************************************************************
# //
# //  printHelpModeHelp
# //
# //******************************************************************************

def printHelpModeHelp( ):
    printParagraph( 'rpn help mode - \'topics\' for a list of topics, \'exit\' to return to rpn' )


# //******************************************************************************
# //
# //  printTitleScreen
# //
# //******************************************************************************

def printTitleScreen( programName, programDescription ):
    print( programName, PROGRAM_VERSION, '-', programDescription )
    print( COPYRIGHT_MESSAGE )
    print( )
    print( 'Type "help" for more information, and "exit" to exit.' )

