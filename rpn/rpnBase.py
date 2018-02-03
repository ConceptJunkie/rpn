#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnBase.py
# //
# //  RPN command-line calculator base conversion functions
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import chop, fac, fac2, fadd, fdiv, floor, fmod, fmul, fneg, fsub, \
                   log, mp, mpmathify, nint, power

from rpn.rpnNumberTheory import getNthLucasNumber
from rpn.rpnPolytope import getNthPolygonalNumber
from rpn.rpnPrimeUtils import getNthPrimorial

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  specialBaseFunctons
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


# //******************************************************************************
# //
# //  convertToBaseN
# //
# //******************************************************************************

def convertToBaseN( value, base, outputBaseDigits=False, numerals=g.defaultNumerals ):
    '''
    This handles any integer base as long as there is a big-enough list of
    numerals to use.  In practice this ends up being 0-9, a-z, and A-Z, which
    allows us to support up to base 62.
    '''
    if outputBaseDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to {0}'.format( len( numerals ) ) )

    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( fneg( value ), base, outputBaseDigits, numerals )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    leftDigits = mpmathify( value )

    while leftDigits > 0:
        modulo = fmod( leftDigits, base )

        if outputBaseDigits:
            result.insert( 0, int( modulo ) )
        else:
            result = numerals[ int( modulo ) ] + result

        leftDigits = floor( fdiv( leftDigits, base ) )

    return result


# //******************************************************************************
# //
# //  convertFractionToBaseN
# //
# //******************************************************************************

def convertFractionToBaseN( value, base, precision, outputBaseDigits ):
    if outputBaseDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( g.numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( g.numerals ) )

    if 0 > value >= 1.0:
        raise ValueError( 'value (%s) must be >= 0 and < 1.0' % value )

    if base == 10:
        return str( value )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    while value > 0 and precision > 0:
        value = fmul( value, base )

        digit = int( value )

        if len( result ) == g.outputAccuracy:
            if digit >= base // 2:
                digit += 1

            break

        if outputBaseDigits:
            result.append( digit )
        else:
            result += g.numerals[ digit ]

        value = fsub( value, digit )
        precision -= 1

    return result


# //******************************************************************************
# //
# //  convertToSpecialBase
# //
# //******************************************************************************

def convertToSpecialBase( value, baseFunction, outputBaseDigits = False, numerals = g.defaultNumerals ):
    '''
    This version supports arbitrary non-constant bases.  The place value is
    determined by the function passed in.  The function takes a single argument
    which represents the place, and it returns the value that that place
    represents.   As an example for base 10, the function would return 10^n for
    argument n.
    '''
    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( fneg( value ), base, outputBaseDigits, numerals )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    positionValues = [ ]

    position = 1
    positionValue = baseFunction( position )

    while positionValue <= value:
        positionValues.append( positionValue )

        position += 1
        positionValue = baseFunction( position )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    remaining = value

    while positionValues:
        base = positionValues.pop( )

        digit = floor( fdiv( remaining, base ) )

        if outputBaseDigits:
            result.append( digit )
        else:
            result += numerals[ int( digit ) ]

        remaining = fsub( remaining, fmul( digit, base ) )

    return result


# //******************************************************************************
# //
# //  convertToIterativeBase
# //
# //******************************************************************************

def convertToIterativeBase( value, baseFunction, outputBaseDigits, numerals ):
    return 'fred'


# //******************************************************************************
# //
# //  convertToNonintegerBase
# //
# //******************************************************************************

def convertToNonintegerBase( num, base ):
    epsilon = power( 10, -( mp.dps - 3 ) )
    minPlace = -( floor( mp.dps / log( base ) ) )

    output = ''
    integer = ''

    remaining = num

    # find starting place
    place = int( floor( log( remaining, base ) ) )

    while remaining > epsilon:
        if place < minPlace:
            break

        if place == -1:
            integer = output
            output = ''

        placeValue = power( base, place )

        value = fdiv( remaining, placeValue )

        value = fmul( value, power( 10, mp.dps - 3 ) )
        value = nint( value )
        value = fdiv( value, power( 10, mp.dps - 3 ) )

        value = floor( value )
        remaining = chop( fsub( remaining, fmul( placeValue, value ) ) )

        output += str( value )[ : -2 ]

        place -= 1

    if place >= 0:
        integer = output + '0' * ( place + 1 )
        output = ''

    if integer == '':
        return output, ''
    else:
        return integer, output


# //******************************************************************************
# //
# //  convertToPhiBase
# //
# //******************************************************************************

def convertToPhiBase( num ):
    epsilon = power( 10, -( mp.dps - 3 ) )

    output = ''
    integer = ''

    start = True
    previousPlace = 0
    remaining = num

    originalPlace = 0

    while remaining > epsilon:
        place = int( floor( log( remaining, phi ) ) )

        if start:
            output = '1'
            start = False
            originalPlace = place
        else:
            if place < -( originalPlace + 1 ):
                break

            for i in range( previousPlace, place + 1, -1 ):
                output += '0'

                if ( i == 1 ):
                    integer = output
                    output = ''

            output += '1'

            if place == 0:
                integer = output
                output = ''

        previousPlace = place
        remaining -= power( phi, place )

    if integer == '':
        return output, ''
    else:
        return integer, output


# //******************************************************************************
# //
# //  convertToFibBase
# //
# //******************************************************************************

def convertToFibBase( value ):
    '''
    Returns a string with Fibonacci encoding for n (n >= 1).

    adapted from https://en.wikipedia.org/wiki/Fibonacci_coding
    '''

    result = ''

    n = value

    if n >= 1:
        a = 1
        b = 1

        c = fadd( a, b )    # next Fibonacci number
        fibs = [ b ]        # list of Fibonacci numbers, starting with F(2), each <= n

        while n >= c:
            fibs.append( c )  # add next Fibonacci number to end of list
            a = b
            b = c
            c = fadd( a, b )

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + '1'
            else:
                result = result + '0'

    return result

