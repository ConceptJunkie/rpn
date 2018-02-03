#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnInput.py
# //
# //  RPN command-line calculator input functions
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import arrow
import math

from mpmath import fdiv, fneg, mp, mpf, mpmathify

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnSettings import setAccuracy
from rpn.rpnUtils import oneArgFunctionEvaluator

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  convertToBase10
# //
# //******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = g.numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


# //******************************************************************************
# //
# //  parseInputValue
# //
# //  Parse out a time value or a numerical expression and attempt to set the
# //  precision to an appropriate value based on the expression.
# //
# //******************************************************************************

def parseInputValue( term, inputRadix = 10 ):
    if isinstance( term, mpf ):
        return term

    if not g.interactive:
        if term[ 0 ] == '$' and term[ 1 : ] in g.userVariables:
            term = g.userVariables[ term[ 1 : ] ]
            return term

        if term[ 0 ] == '@' and term[ 1 : ] in g.userFunctions:
            term = g.userFunctions[ term[ 1 : ] ]
            return term

    innerChars = term[ 1 : -1 ]

    # this helps us parse dates
    if '/' in innerChars:
        term = term.replace( '/', '-' )
        innerChars = term[ 1 : -1 ]

    # 'e' implies scientific notation, which isn't a date regardless
    if ( 'e' not in innerChars ):
        # 'd' means a dice expression, '[' means a build_number expression, so don't treat it as a date
        if ( ( '-' in innerChars ) or ( ':' in innerChars ) ) and ( 'd' not in term ) and ( '[' not in term ):
            # try:
                datetime = arrow.get( term )
                datetime = RPNDateTime( datetime.year, datetime.month, datetime.day,
                                        datetime.hour, datetime.minute, datetime.second,
                                        datetime.microsecond )
            # except:
            #     raise ValueError( 'error parsing datetime' )

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

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

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

                if mp.dps < newPrecision:
                    setAccuracy( newPrecision )

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    setAccuracy( newPrecision )

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        if integer[ 0 ] == '1' and integer[ -1 ] in 'bB':
            # set the precision big enough to handle this value
            newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

            integer = integer[ : -1 ]
            return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


# //******************************************************************************
# //
# //  readListFromFile
# //
# //******************************************************************************

def readListFromFileGenerator( filename ):
    result = [ ]

    with open( filename ) as file:
        for i in file:
            if i == '\n':
                continue
            else:
                try:
                    yield parseInputValue( i )
                except:
                    pass

@oneArgFunctionEvaluator( )
def readListFromFile( filename ):
    return RPNGenerator( readListFromFileGenerator( filename ) )

