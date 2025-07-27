#!/usr/bin/env python

#******************************************************************************
#
#  rpnInput.py
#
#  rpnChilada input functions
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import math
import os

import pendulum

from mpmath import fdiv, fneg, mp, mpc, mpf, mpmathify

from rpn.time.rpnDateTime import RPNDateTime
from rpn.time.rpnDateTimeClass import getLocalTimeZone
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnSettings import setAccuracy
from rpn.util.rpnUtils import oneArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, StringValidator

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  convertToBase10
#
#******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = g.numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( f'invalid numeral \'{ integer[ i ] } \' for base { inputRadix }' )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i, numeral in enumerate( mantissa ):
        digit = validNumerals.find( numeral )

        if digit == -1:
            raise ValueError( f'invalid numeral \'{ mantissa[ i ] }\' for base { inputRadix }' )

        result += digit * base
        base /= inputRadix

    return result


#******************************************************************************
#
#  parseInputValue
#
#  Parse out a datetime value or a numerical expression and attempt to set
#  the precision to an appropriate value based on the expression.
#
#******************************************************************************

def parseInputValue( term, inputRadix = 10 ):
    if isinstance( term, mpf ):
        return term

    possibleDate = False

    hasDigit = False
    hasDatePunct = False
    illegalDateChars = False

    # one 'T' is allowed in a date, but no other letters
    for c in term:
        if c.isdigit( ):
            hasDigit = True
            break

    for c in term[ 1 : ]:
        if c in ' -/:':
            hasDatePunct = True
            break

    for c in term:
        if c in '[]':
            illegalDateChars = True
            break

    if hasDigit and hasDatePunct and not illegalDateChars:
        possibleDate = True

    if not g.interactive:
        if term[ 0 ] == '$' and term[ 1 : ] in g.userVariables:
            term = parseInputValue( g.userVariables[ term[ 1 : ] ] )
            return term

        if term[ 0 ] == '@' and term[ 1 : ] in g.userFunctions:
            term = g.userFunctions[ term[ 1 : ] ]
            return term

        if term[ 0 ] == "'":
            return term[ 1 : ]

    innerChars = term[ 1 : -1 ]

    # this helps us parse dates
    if '/' in innerChars and possibleDate:
        term = term.replace( '/', '-' )
        innerChars = term[ 1 : -1 ]

    # Try to parse a date
    if possibleDate:
        tryAgain = False
        datetime = None

        try:
            # Try to parse a default date-time
            datetime = pendulum.parse( term )

            # convert pendulum to RPNDateTime with the parsed timezone
            datetime = RPNDateTime( datetime.year, datetime.month, datetime.day,
                                    datetime.hour, datetime.minute, datetime.second,
                                    datetime.microsecond )
            tryAgain = False
            return datetime
        except pendulum.parsing.exceptions.ParserError:
            tryAgain = True

        dtFormats = [
            'MMM D YYYY HH:mm:ss ZZ',
            'MMM D YYYY HH:mm:ss ZZ',
            'MMM D, YYYY HH:mm:ss ZZ',
            'MMM DD YYYY HH:mm:ss ZZ',
            'MMM DD, YYYY HH:mm:ss ZZ',
            'MMMM D YYYY HH:mm:ss ZZ',
            'MMMM D, YYYY HH:mm:ss ZZ',
            'MMMM DD YYYY HH:mm:ss ZZ',
            'MMMM DD, YYYY HH:mm:ss ZZ',
            'YYYY-MM-DD HH:mm:ss ZZ'
        ]

        for dtFormat in dtFormats:
            try:
                datetime = pendulum.from_format( term, dtFormat )
                datetime = RPNDateTime( datetime.year, datetime.month, datetime.day,
                                        datetime.hour, datetime.minute, datetime.second,
                                        datetime.microsecond, tz=datetime.tzinfo )
                break
            except ValueError:
                continue

        # If that fails, try to parse without a timezone, and use the local timezone
        dtFormats = [
            'MMM D YYYY HH:mm:ss',
            'MMM D YYYY',
            'MMM D, YYYY HH:mm:ss',
            'MMM D, YYYY',
            'MMM DD YYYY HH:mm:ss',
            'MMM DD YYYY',
            'MMM DD, YYYY HH:mm:ss',
            'MMM DD, YYYY',
            'MMMM D YYYY HH:mm:ss',
            'MMMM D YYYY',
            'MMMM D, YYYY HH:mm:ss',
            'MMMM D, YYYY',
            'MMMM DD YYYY HH:mm:ss',
            'MMMM DD YYYY',
            'MMMM DD, YYYY HH:mm:ss',
            'MMMM DD, YYYY',
            'YYYY-MM-DD HH:mm:ss',
            'YYYY-MM-DD',
            'MM-DD-YYYY'
        ]

        for dtFormat in dtFormats:
            try:
                datetime = pendulum.from_format( term, dtFormat )
                datetime = RPNDateTime( datetime.year, datetime.month, datetime.day,
                                        datetime.hour, datetime.minute, datetime.second,
                                        datetime.microsecond, tz=getLocalTimeZone( ) )
                break
            except ValueError:
                continue

        # if we get a datetime, then let's use it, otherwise keep trying
        if datetime:
            return datetime

    if term == '0':
        return mpmathify( 0 )

    # ignore commas
    term = ''.join( [ i for i in term if i not in ',' ] )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if inputRadix == 10:
        imaginary = term[ -1 ] in ( 'i', 'j' )
    else:
        imaginary = False

    if imaginary:
        term = term[ : -1 ]

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            setAccuracy( newPrecision )

            if imaginary:
                return mpc( imag = term )

            return mpmathify( term )

        decimal = term.find( '.' )
    else:
        decimal = len( term )

    negative = term[ 0 ] == '-'

    if negative:
        start = 1
    else:
        if term[ 0 ] == '+':
            start = 1
        else:
            start = 0

    integer = term[ start : decimal ]
    mantissa = term[ decimal + 1 : ]

    # check for hex, then binary, then octal, otherwise a plain old decimal integer
    if not ignoreSpecial and mantissa == '':
        if integer[ 0 ] == '0':
            if len( integer ) == 1:
                return mpmathify( 0 )

            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                setAccuracy( newPrecision )

                return mpmathify( int( integer[ 2 : ], 16 ) )

            if integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                setAccuracy( newPrecision )

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )

            integer = integer[ 1 : ]

            return mpmathify( int( integer, 8 ) )
        if integer[ 0 ] == '1' and integer[ -1 ] in 'bB':
            # set the precision big enough to handle this value
            newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

            setAccuracy( newPrecision )

            integer = integer[ : -1 ]
            return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )

        if inputRadix == 10:
            newPrecision = len( integer ) + 1

            setAccuracy( newPrecision )

            result = fneg( integer ) if negative else mpmathify( integer )

            if imaginary:
                return mpc( real = '0.0', imag = result )

            return result

    # finally, we have a non-radix 10 number with a mantissa to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    result = fneg( result ) if negative else mpmathify( result )

    if imaginary:
        return mpc( real = '0.0', imag = result )

    return result


#******************************************************************************
#
#  readListFromFile
#
#******************************************************************************

def readListFromFileGenerator( filename ):
    filename = g.cwd + os.sep + filename

    with open( filename, encoding='ascii' ) as file:
        for i in file:
            if i == '\n':
                continue

            i = i[ : -1 ]    # trim off the newline

            yield parseInputValue( i )


@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def readListFromFileOperator( filename ):
    return RPNGenerator( readListFromFileGenerator( filename ) )


#******************************************************************************
#
#  readNUmberFromFile
#
#******************************************************************************

def readNumberFromFileGenerator( filename ):
    filename = g.cwd + os.sep + filename

    string = ''

    with open( filename, encoding='ascii' ) as file:
        for i in file:
            for c in i:
                if '0' <= c <= '9':
                    string += c

    setAccuracy( len( string ) + 1 )

    return mpmathify( string )


@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def readNumberFromFileOperator( filename ):
    return readNumberFromFileGenerator( filename )
