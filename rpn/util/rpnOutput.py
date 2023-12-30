#!/usr/bin/env python

#******************************************************************************
#
#  rpnOutput.py
#
#  rpnChilada output functions
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import math
import string
import sys
import textwrap

from mpmath import e, floor, frac, im, mp, mpf, mpmathify, nstr, phi, pi, re, sqrt

from rpn.math.rpnBase import convertFractionToBaseN, convertToBaseN
from rpn.time.rpnDateTime import RPNDateTime
from rpn.util.rpnGenerator import RPNGenerator
from rpn.units.rpnMeasurementClass import RPNMeasurement
from rpn.util.rpnPersistence import loadHelpData, loadUnitData
from rpn.math.rpnSpecialBase import convertToFibBase, convertToNonintegerBase, convertToSpecialBase, specialBaseFunctions
from rpn.units.rpnUnitTypes import basicUnitTypes
from rpn.util.rpnUtils import addAliases
from rpn.rpnVersion import COPYRIGHT_MESSAGE, PROGRAM_VERSION, PROGRAM_VERSION_STRING, \
                           RPN_PROGRAM_NAME, PROGRAM_DESCRIPTION
from rpn.time.rpnDateTime import formatDateTime

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  formatNumber
#
#  This takes a mpf value and turns it into a string.
#
#******************************************************************************

def formatNumber( number, outputRadix, leadingZero, integerGrouping, integerDelimiter, decimalDelimiter ):
    negative = number < 0

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
    elif outputRadix < 0:   # these mean special bases, not negative numbers
        strInteger = convertToSpecialBase( floor( number ), specialBaseFunctions[ outputRadix ] )
        strMantissa = ''
    elif ( outputRadix != 10 ) or ( g.numerals != g.defaultNumerals ):
        strInteger = str( convertToBaseN( floor( number ), outputRadix, False, g.numerals ) )
        strMantissa = str( convertFractionToBaseN( frac( number ), outputRadix,
                                                   int( mp.dps / math.log10( outputRadix ) ), False ) )
        if strMantissa == '[]':
            strMantissa = ''
    else:
        strNumber = nstr( number, n=g.outputAccuracy, min_fixed=-g.maximumFixed - 1 )

        if '.' in strNumber:
            decimal = strNumber.find( '.' )
        else:
            decimal = len( strNumber )

        strInteger = strNumber[ 1 if negative else 0 : decimal ]

        strMantissa = strNumber[ decimal + 1 : ]

        if strMantissa == '0':
            strMantissa = ''
        elif ( strMantissa != '' ) and ( g.outputAccuracy == -1 ):
            strMantissa = strMantissa.rstrip( '0' )

    if integerGrouping > 0:
        if strInteger[ 0 ] == '-':
            strInteger = strInteger[ 1 : ]

        firstDelimiter = len( strInteger ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += strInteger[ : firstDelimiter ]

        for i in range( firstDelimiter, len( strInteger ), integerGrouping ):
            if integerResult != '':
                integerResult += integerDelimiter

            integerResult += strInteger[ i : i + integerGrouping ]
    else:
        integerResult = strInteger

    if g.decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( strMantissa ), g.decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += decimalDelimiter

            mantissaResult += strMantissa[ i : i + g.decimalGrouping ]
    else:
        mantissaResult = strMantissa

    result = integerResult

    if mantissaResult != '':
        result += '.' + mantissaResult

    return result, negative


#******************************************************************************
#
#  formatOutput
#
#  This takes a string representation of the result and formats it according
#  to a whole bunch of options.
#
#******************************************************************************

def formatOutput( output ):
    # filter out text strings
    for c in output:
        if c in '+-.':
            continue

        # anything with embedded whitespace is a string
        if c in string.whitespace or c in string.punctuation:
            return output

    # output settings, which may be overridden by temp settings
    outputRadix = g.outputRadix
    integerGrouping = g.integerGrouping
    leadingZero = g.leadingZero
    integerDelimiter = g.integerDelimiter

    # override settings with temporary settings if needed
    if g.tempCommaMode:
        integerGrouping = 3     # override whatever was set on the command-line
        leadingZero = False     # this one, too
        integerDelimiter = ','

    if g.tempHexMode:
        integerGrouping = 4
        leadingZero = True
        outputRadix = 16

    if g.tempLeadingZeroMode:
        leadingZero = True

    if g.tempOctalMode:
        integerGrouping = 3
        leadingZero = True
        outputRadix = 8

    mpOutput = mpmathify( output )

    imaginary = im( mpOutput )
    real = re( mpOutput )

    result, negative = formatNumber( real, outputRadix, leadingZero, integerGrouping,
                                     integerDelimiter, g.decimalDelimiter )

    if negative:
        result = '-' + result

    if imaginary != 0:
        strImaginary, negativeImaginary = \
            formatNumber( imaginary, outputRadix, leadingZero, integerGrouping, integerDelimiter, g.decimalDelimiter )
        result = '( ' + result + ( ' - ' if negativeImaginary else ' + ' ) + strImaginary + 'j )'

    return result


#******************************************************************************
#
#  formatListOutput
#
#******************************************************************************

def formatListOutput( result, level=0, indent=0, file=sys.stdout ):
    '''
    This function formats a list for output, taking into account the list
    format level, as specified by the -s option.
    '''
    indentString = ' ' * indent

    first = True

    if level < g.listFormatLevel:
        useIndent = True
        print( indentString + '[', end='', file=file )
        levelIndent = ' ' * ( level + 1 ) * 4
    else:
        useIndent = False
        print( indentString + '[ ', end='', file=file )

    #print( 'result type', type( result ) )

    for item in result:
        newString = ''

        if isinstance( item, ( list, RPNGenerator ) ):
            if first:
                first = False

                if useIndent:
                    print( file=file )
                    print( indentString + levelIndent, end='', file=file )
            else:
                if useIndent:
                    print( ',', file=file )
                    print( indentString + levelIndent, end='', file=file )
                else:
                    print( ', ', end='', file=file )

            formatListOutput( item, level + 1, file=file )
            continue

        if isinstance( item, str ):
            newString = item
        elif isinstance( item, RPNDateTime ):
            newString = formatDateTime( item )
        elif isinstance( item, RPNMeasurement ):
            newString = formatOutput( nstr( item.value, min_fixed=-g.maximumFixed - 1 ) )
            newString += ' ' + formatUnits( item )
        else:
            newString = formatOutput( str( item ) )

        if first:
            first = False
        else:
            print( ', ', end='', file=file )

        if useIndent:
            print( file=file )
            print( indentString + levelIndent + newString, end='', flush=True, file=file )
        else:
            print( newString, end='', flush=True, file=file )

    if useIndent:
        print( file=file )
        print( ' ' * level * 4 + ']', end='', file=file )
    else:
        print( ' ]', end='', file=file )

    if level == 0:
        print( file=file )


#******************************************************************************
#
#  formatUnits
#
#  For outputting an RPNMeasurement object, this method formats the units part
#  of the object, and returns the formatted string.
#
#******************************************************************************

def formatUnits( measurement ):
    value = measurement.value

    unitName = measurement.getUnitName( )

    if unitName is not None:
        unitString = ''

        if mpf( -1.0 ) < value > mpf( 1.0 ) or value == 0:
            tempString = measurement.getPluralUnitName( )
        else:
            tempString = unitName

        tempString = tempString.replace( '_null_unit*', '' )
        tempString = tempString.replace( '*_null_unit', '' )

        tempString = tempString.replace( '_null_unit/', '1/' )
        tempString = tempString.replace( '/_null_unit', '' )

        for c in tempString:
            if c == '_':
                unitString += ' '
            else:
                unitString += c

        return unitString

    unitString = ''

    units = measurement.units

    # now that we've expanded the compound units, let's format...
    for unit in units:
        if unit == '_null_unit':
            continue

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
            if unit == '_null_unit':
                continue

            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits != '':
                    negativeUnits += ' '

                negativeUnits += unit
                negativeUnits += '^' + str( int( exponent ) )
    else:
        for unit in units:
            if unit == '_null_unit':
                continue

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

    # filter out the underscores
    for c in unitString + negativeUnits:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#******************************************************************************
#
#  printParagraph
#
#******************************************************************************

def printParagraph( text, indent = 0 ):
    lines = textwrap.wrap( text, g.lineLength - ( indent + 1 ) )

    for line in lines:
        print( ' ' * indent + line )


#******************************************************************************
#
#  printOperatorHelp
#
#******************************************************************************

def printOperatorHelp( term, operatorInfo, operatorHelp, regularOperator = True):
    if regularOperator:
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

    aliasList = [ key for key, value in g.aliases.items( ) if term == value ]

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

    if regularOperator:
        if len( operatorHelp ) > 3:
            if operatorHelp[ 3 ] == '' or operatorHelp[ 3 ] == '\n':
                print( 'No examples are available.' )
            else:
                print( term + ' examples:' )
                print( operatorHelp[ 3 ] )
        else:
            print( 'No examples are available.' )

    if len( operatorHelp ) > 4 and len( operatorHelp[ 4 ] ) > 0:
        print( 'see also:  ', end='' )

        bFirst = True

        for name in sorted( operatorHelp[ 4 ] ):
            if bFirst:
                bFirst = False
            else:
                print( ', ', end='' )

            print( name, end='' )

        print( )


#******************************************************************************
#
#  printCategoryHelp
#
#******************************************************************************

def printCategoryHelp( category, operators, listOperators, modifiers, operatorHelp ):
    if category in basicUnitTypes:
        units = [ ]

        for unit, unitInfo in g.unitOperators.items( ):
            if unitInfo.unitType == category:
                units.append( unit )

        printParagraph( 'The ' + category + ' category includes the following units:' )
        print( )

        printParagraph( ', '.join( sorted( units ) ), indent=4 )
        return

    printParagraph( 'The ' + category + ' category includes the following operators (with aliases in parentheses):' )
    print( )

    operatorList = [ key for key in operators if operatorHelp[ key ][ 0 ] == category ]
    operatorList.extend( [ key for key in listOperators if operatorHelp[ key ][ 0 ] == category ] )
    operatorList.extend( [ key for key in modifiers if operatorHelp[ key ][ 0 ] == category ] )

    addAliases( operatorList, g.aliases )

    for operator in sorted( operatorList ):
        print( operator )


#******************************************************************************
#
#  printHelp
#
#******************************************************************************

def printHelp( terms = None, interactive = False ):
    from rpn.rpnOperators import constants, listOperators, modifiers, operators

    if terms is None:
        terms = [ ]

    loadHelpData( )
    loadUnitData( )

    if g.helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    unitType = False

    if len( terms ) > 0:
        term = terms[ 0 ]
    else:
        term = ''

    if len( terms ) > 1 and terms[ 0 ] == 'unit_type':
        term = terms[ 1 ]
        unitType = True

    if term == '':
        if interactive:
            printInteractiveHelp( )
        else:
            printGeneralHelp( )
        return

    # first check if the term is an alias and translate
    if term in g.aliases:
        term = g.aliases[ term ]

    # then look for exact matches in all the lists of terms for which we have help support
    if term in operators and not unitType:
        printOperatorHelp( term, operators[ term ], g.OPERATOR_HELP[ term ] )
    elif term in g.unitOperators:
        printOperatorHelp( term, g.unitOperators[ term ], g.OPERATOR_HELP[ term ], regularOperator = False )
    elif term in g.constantOperators:
        printOperatorHelp( term, g.constantOperators[ term ], g.OPERATOR_HELP[ term ], regularOperator = False )
    elif term in constants:
        printOperatorHelp( term, constants[ term ], g.OPERATOR_HELP[ term ] )
    elif term in listOperators:
        printOperatorHelp( term, listOperators[ term ], g.OPERATOR_HELP[ term ] )
    elif term in modifiers:
        printOperatorHelp( term, modifiers[ term ], g.OPERATOR_HELP[ term ] )
    elif term in g.HELP_TOPICS:
        print( g.HELP_TOPICS[ term ] )
    elif term in g.operatorCategories:
        printCategoryHelp( term, operators, listOperators, modifiers, g.OPERATOR_HELP )
    elif term == 'unit_types':
        printParagraph( ', '.join( sorted( [ key for key in g.unitTypeDict.keys( ) if key != '_null_type' ] ) ),
                        indent=4 )
    elif term in g.unitTypeDict:
        unitList = sorted( g.unitTypeDict[ term ] )
        addAliases( unitList, g.aliases )
        for unit in unitList:
            printParagraph( unit, indent=4 )
    else:
        # if no exact matches for any topic, let's look for partial matches
        if 'unit_types'.startswith( term ):
            print( 'Interpreting topic as \'unit_types\'.' )
            printParagraph( ', '.join( sorted( g.unitTypeDict.keys( ) ) ), indent=4 )
            return

        helpTerm = next( ( i for i in g.unitTypeDict if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( )
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            printParagraph( ', '.join( sorted( g.unitTypeDict[ helpTerm ] ) ), indent=4 )
            return

        helpTerm = next( ( i for i in operators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, operators[ helpTerm ], g.OPERATOR_HELP[ helpTerm ] )
            return

        helpTerm = next( ( i for i in constants if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, constants[ helpTerm ], g.OPERATOR_HELP[ helpTerm ] )
            return

        helpTerm = next( ( i for i in listOperators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, listOperators[ helpTerm ], g.OPERATOR_HELP[ helpTerm ] )
            return

        helpTerm = next( ( i for i in modifiers if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpTerm, modifiers[ helpTerm ], g.OPERATOR_HELP[ helpTerm ] )
            return

        helpTerm = next( ( i for i in g.HELP_TOPICS if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            print( g.HELP_TOPICS[ helpTerm ] )
            return

        helpTerm = next( ( i for i in g.operatorCategories if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printCategoryHelp( helpTerm, operators, listOperators, modifiers, g.OPERATOR_HELP )
        else:
            print( 'Help topic not found.' )


#******************************************************************************
#
#  printGeneralHelp
#
#******************************************************************************

def printGeneralHelp( ):
    print( RPN_PROGRAM_NAME + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
        'For help on a specific topic, use \'rpn help\' and add a help topic, '
        'operator category or a specific operator name.' )

    printHelpTopics( )


#******************************************************************************
#
#  printInteractiveHelp
#
#******************************************************************************

def printInteractiveHelp( ):
    loadHelpData( )

    printParagraph(
        'For help on a specific topic, use the topic operator with a general topic, '
        'operator category or a specific operator name.' )

    printHelpTopics( )


#******************************************************************************
#
#  printHelpTopics
#
#******************************************************************************

def printHelpTopics( ):
    print( )
    print( 'The following is a list of general topics:' )
    print( )

    helpTopics = list( g.HELP_TOPICS.keys( ) )
    helpTopics.append( 'unit_types' )

    printParagraph( ', '.join( sorted( helpTopics ) ), indent=4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    operatorCategories = set( g.operatorCategories )

    unitTypes = dict( basicUnitTypes )

    for i in unitTypes:
        if i in operatorCategories:
            operatorCategories.remove( i )

    printParagraph( ', '.join( sorted( operatorCategories ) ), indent=4 )

    print( )
    print( 'The following is a list of unit categories\n(use \'rpn help unit_type name\' for more info):' )
    print( )

    del unitTypes[ '_null_type' ]

    printParagraph( ', '.join( sorted( unitTypes ) ), indent=4 )


#******************************************************************************
#
#  printHelpModeHelp
#
#******************************************************************************

def printHelpModeHelp( ):
    printParagraph( 'rpn help mode - \'topics\' for a list of topics, \'exit\' to return to rpn' )


#******************************************************************************
#
#  printTitleScreen
#
#******************************************************************************

def printTitleScreen( programName, programDescription, showHelp=True ):
    print( programName + PROGRAM_VERSION_STRING + ' - ' + programDescription )
    print( COPYRIGHT_MESSAGE )

    if showHelp:
        print( )
        print( 'Type "help" for more information, and "exit" to exit.' )
