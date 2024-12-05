#!/usr/bin/env python

#******************************************************************************
#
#  rpnBase.py
#
#  rpnChilada base conversion functions
#  copyright (c) 2024, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import chop, fac, fac2, fadd, fdiv, floor, fmul, fsub, log, mp, nint, phi, power

from rpn.math.rpnNumberTheory import getNthLucasNumber
from rpn.math.rpnPolytope import getNthPolygonalNumber
from rpn.math.rpnPrimeUtils import getNthPrimorial

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  specialBaseFunctons
#
#******************************************************************************

specialBaseFunctions = {
    g.facBase         : fac,
    g.doublefacBase   : fac2,
    g.squareBase      : lambda n: power( n, 2 ),
    g.lucasBase       : getNthLucasNumber,
    g.triangularBase  : lambda n: getNthPolygonalNumber( n, 3 ),
    g.primorialBase   : lambda n: getNthPrimorial( n - 1 ),
}


#******************************************************************************
#
#  specialBaseNames
#
#******************************************************************************

specialBaseNames = {
    'phi'               : g.phiBase,
    'fib'               : g.fibBase,
    'fibonacci'         : g.fibBase,
    'fac'               : g.facBase,
    'factorial'         : g.facBase,
    '!'                 : g.facBase,
    'factorial2'        : g.doublefacBase,
    'double_factorial'  : g.doublefacBase,
    'fac2'              : g.doublefacBase,
    'double_fac'        : g.doublefacBase,
    '!!'                : g.doublefacBase,
    'square'            : g.squareBase,
    'sqr'               : g.squareBase,
    'lucas'             : g.lucasBase,
    'triangular'        : g.triangularBase,
    'tri'               : g.triangularBase,
    'primorial'         : g.primorialBase,
    'e'                 : g.eBase,
    'pi'                : g.piBase,
    'root2'             : g.sqrt2Base,
    'sqrt2'             : g.sqrt2Base,
}


#******************************************************************************
#
#  convertToSpecialBase
#
#******************************************************************************

def convertToSpecialBase( value, baseFunction, outputBaseDigits = False, numerals = g.defaultNumerals ):
    '''
    This version supports arbitrary non-constant bases.  The place value is
    determined by the function passed in.  The function takes a single argument
    which represents the place, and it returns the value that that place
    represents.  As an example for base 10, the function would return 10^n for
    argument n.
    '''
    if value == 0:
        return 0

    if value < 0:
        raise ValueError( 'Negative numbers are not supported.' )

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


#******************************************************************************
#
#  convertToIterativeBase
#
#******************************************************************************

#def convertToIterativeBase( value, baseFunction, outputBaseDigits, numerals ):
#    return 'fred'


#******************************************************************************
#
#  convertToNonintegerBase
#
#******************************************************************************

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

    return integer, output


#******************************************************************************
#
#  convertToPhiBase
#
#******************************************************************************

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

                if i == 1:
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

    return integer, output


#******************************************************************************
#
#  convertToFibBase
#
#******************************************************************************

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
