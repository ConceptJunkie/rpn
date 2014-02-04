#!/usr/bin/env python

import argparse
import math
import os
import random
import sys
import types

from fractions import Fraction
from functools import reduce
from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = "rpn"
RPN_VERSION = "3.7.0"
PROGRAM_DESCRIPTION = 'RPN command-line calculator'
COPYRIGHT_MESSAGE = "copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 12
defaultAccuracy = 10
defaultCFTerms = 10
defaultBitwiseGroupSize = 16
defaultInputRadix = 10
defaultOutputRadix = 10
defaultDecimalGrouping = 5
defaultIntegerGrouping = 3

defaultNumerals = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

numerals = ""

phiBase = -1
fibBase = -2

numberArg = -1
listArg = -2

argumentPrefixLinux = '-'
argumentPrefixWindows = '/'


#//******************************************************************************
#//
#//  globals
#//
#//******************************************************************************

prefixListLinux = argumentPrefixLinux
prefixListWindows = argumentPrefixLinux + argumentPrefixWindows

nestedListLevel = 0


#//******************************************************************************
#//
#//  ContinuedFraction
#//
#//  A continued fraction, represented as a list of integer terms.
#//
#//  adapted from ActiveState Python, recipe 578647
#//
#//******************************************************************************

class ContinuedFraction( list ):
    def __init__( self, value, maxterms=15, cutoff=1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            self.extend( value )
        else:
            raise ValueError( "ContinuedFraction requires number or list" )

    def getFraction( self, terms=None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return "[%s]" % ", ".join( [ str( int( x ) ) for x in self ] )



#//******************************************************************************
#//
#//  factorize
#//
#//  This is not my code, and I need to find the source so I can attribute it.
#//
#//******************************************************************************

def factorize( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factorize( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def potential_primes( ):
            base_primes = ( 2, 3, 5 )

            for base_prime in base_primes:
                yield base_prime

            base_primes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            prime_group = 0

            while True:
                for base_prime in base_primes:
                    yield prime_group + base_prime

                prime_group += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in potential_primes( ):
            if divisor > sqrtn:
                break

            power = 0

            while ( fmod( n, divisor ) ) == 0:
                n = floor( fdiv( n, divisor ) )
                power += 1

            if power > 0:
                factors.append( ( divisor, power ) )
                sqrtn = sqrt( n )

        if n > 1:
             factors.append( ( int( n ), 1 ) )

        return factors


#//******************************************************************************
#//
#//  factorInteger
#//
#//******************************************************************************

def factorInteger( n ):
    def getStringFromFactorsWithExponents( factors ):
        def getStringFromFactor( factor ):
            if factor[ 1 ] == 1:
                return str( factor[ 0 ] )
            else:
                return "^".join( map( str, factor ) )

        return " * ".join( map( getStringFromFactor, factors ) )

    def getStringFromFactorsWithMultiplication( factors ):
        factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
        factors = reduce( lambda x, y: x + y, factors, [ ] )
        return " * ".join( map( str, factors ) )

    factors = factorize( n )

    exponents = getStringFromFactorsWithExponents( factors )
    multiplication = getStringFromFactorsWithMultiplication( factors )

    print( "    = " + getStringFromFactorsWithExponents( factors ) )

    if ( multiplication != exponents ):
        print( "    = " + getStringFromFactorsWithMultiplication( factors ) )

    print( )


#//******************************************************************************
#//
#//  convertToPhiBase
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  convertToFibBase
#//
#//  Returns a string with Fibonacci encoding for n (n >= 1).
#//
#//  adapted from https://en.wikipedia.org/wiki/Fibonacci_coding
#//
#//******************************************************************************

def convertToFibBase( value ):
    result = ""

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

        result = ""

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + "1"
            else:
                result = result + "0"

    return result


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//******************************************************************************

def convertToBaseN( value, base, baseAsDigits, numerals ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'Base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'Base must be from 2 to %d' % len( numerals ) )

    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( ( -1 ) * value, base, baseAsDigits, numerals )

    result = ''
    left_digits = value

    while left_digits > 0:
        if baseAsDigits:
            if result != '':
                result = ' ' + result

            result = str( int( left_digits ) % base ) + result
        else:
            result = numerals[ int( left_digits ) % base ] + result

        left_digits = floor( fdiv( left_digits, base ) )

    return result



#//******************************************************************************
#//
#//  convertFractionToBaseN
#//
#//******************************************************************************

def convertFractionToBaseN( value, base, precision, baseAsDigits, accuracy ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'Base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'Base must be from 2 to %d' % len( numerals ) )

    if value < 0 or value >= 1.0:
        raise ValueError( 'Value (%s) must be >= 0 and < 1.0' % value )

    result = ''

    while value > 0 and precision > 0:
        value = value * base
        digit = int( value )

        if len( result ) == accuracy:
            value -= digit
            newDigit = int( value ) % base

            if newDigit >= base // 2:
                digit += 1

        if baseAsDigits:
            if result != '':
                result += ' '

            result += str( digit % base )
        else:
            result += numerals[ digit % base ]

        if len( result ) == accuracy:
            break

        value -= digit
        precision -= 1

    return result


#//******************************************************************************
#//
#//  convertToBase10
#//
#//******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'Invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'Invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


#//******************************************************************************
#//
#//  getInvertedBits
#//
#//******************************************************************************

def getInvertedBits( valueList ):
    global bitwiseGroupSize

    value = floor( valueList.pop( ) )
    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = value

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        result = fadd( fmul( fsum( [ placeValue, fneg( fmod( remaining, placeValue ) ), -1 ] ), multiplier ), result )
        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    valueList.append( result )


#//******************************************************************************
#//
#//  performBitwiseOperation
#//
#//  The operations are performed on groups of bits as specified by the variable
#//  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
#//  does mean that under normal circumstances the regular Python bit operators
#//  can be used.
#//
#//******************************************************************************

def performBitwiseOperation( valueList, operation ):
    global bitwiseGroupSize

    value1 = floor( valueList.pop( ) )
    value2 = floor( valueList.pop( ) )

    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )
    groupings2 = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    if groupings2 > groupings:
        groupings = groupings2

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining1 = value1
    remaining2 = value2

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        mod1 = fmod( remaining1, placeValue )
        mod2 = fmod( remaining2, placeValue )

        result = fadd( fmul( operation( int( mod1 ), int( mod2 ) ), multiplier ), result )

        remaining1 = floor( fdiv( remaining1, placeValue ) )
        remaining2 = floor( fdiv( remaining2, placeValue ) )

        multiplier = fmul( multiplier, placeValue )

    valueList.append( result )


#//******************************************************************************
#//
#//  sum
#//
#//******************************************************************************

def sum( valueList ):
    args = valueList.pop( )

    if not isinstance( args, list ):
        args = [ args ]

    valueList.append( fsum( args ) )


#//******************************************************************************
#//
#//  getMean
#//
#//******************************************************************************

def getMean( valueList ):
    args = valueList.pop( )

    if not isinstance( args, list ):
        args = [ args ]

    valueList.append( fdiv( fsum( args ), len( args ) ) )


#//******************************************************************************
#//
#//  subtract
#//
#//******************************************************************************

def subtract( valueList ):
    value = valueList.pop( )
    valueList.append( fsub( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  multiplyAll
#//
#//******************************************************************************

def multiplyAll( valueList ):
    args = valueList.pop( )

    if not isinstance( args, list ):
        args = [ args ]

    valueList.append( fprod( args ) )


#//******************************************************************************
#//
#//  divide
#//
#//******************************************************************************

def divide( valueList ):
    value = valueList.pop( )
    valueList.append( fdiv( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  getModulo
#//
#//******************************************************************************

def getModulo( valueList ):
    value = valueList.pop( )
    valueList.append( fmod( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( power( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( valueList ):
    value = valueList.pop( )

    operand = valueList.pop( )
    result = operand

    for i in range( 1, int( value ) ):
        result = power( result, operand )

    valueList.append( result )


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( valueList ):
    value = valueList.pop( )

    operand = valueList.pop( )
    result = operand

    for i in range( 1, int( value ) ):
        result = power( operand, result )

    valueList.append( result )


#//******************************************************************************
#//
#//  antiexponentiate
#//
#//******************************************************************************

def antiexponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( root( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  getLogXY
#//
#//******************************************************************************

def getLogXY( valueList ):
    value = valueList.pop( )
    valueList.append( log( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  getNthLucas
#//
#//******************************************************************************

def getNthLucas( valueList ):
    value = valueList.pop

    if value == 1:
        valueList.append( 1 )
    else:
        valueList.append( round( power( phi, valueList.pop( ) ) ) )


#//******************************************************************************
#//
#//  getNthTriangularNumber
#//
#//******************************************************************************

def getNthTriangularNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv ( fmul( n, fadd( n, 1 ) ), 2 ) )


#//******************************************************************************
#//
#//  getAntiTriangularNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiTriangularNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fmul( 0.5, fsub( sqrt( fadd( fmul( 8, n ), 1 ) ), 1 ) ) )


#//******************************************************************************
#//
#//  getNthPentagonalNumber
#//
#//******************************************************************************

def getNthPentagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv( fsub( fprod( [ 3, n, n ] ), n ), 2 ) )


#//******************************************************************************
#//
#//  getAntiPentagonalNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiPentagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv( fadd( sqrt( fadd( fmul( 24 , n ), 1 ) ), 1 ), 6 ) )


#//******************************************************************************
#//
#//  getNthHexagonalNumber
#//
#//******************************************************************************

def getNthHexagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fsub( fprod( 2, n, n ), n ) )


#//******************************************************************************
#//
#//  getAntiHexagonalNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiHexagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv( fadd( sqrt( fadd( fmul( 8, n ), 1 ) ), 1 ), 4 ) )


#//******************************************************************************
#//
#//  getNthTetrahedralNumber
#//
#//******************************************************************************

def getNthTetrahedralNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv( fsum( [ power( n, 3 ), fmul( 3, power( n, 2 ) ), fmul( 2, n ) ] ), 6 ) )


#//******************************************************************************
#//
#//  getAntiTetrahedralNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiTetrahedralNumber( valueList ):
    n = valueList.pop( )

    sqrt3 = sqrt( 3 )
    curt3 = cbrt( 3 )

    # TODO:  finish me
    valueList.append( 0 )

# http://www.wolframalpha.com/input/?i=solve+p%3D%281%2F6%29*%28n^3%2B3*n^2%2B2*n%29+for+n


#//******************************************************************************
#//
#//  getNthSquareTriangularNumber
#//
#//******************************************************************************

def getNthSquareTriangularNumber( valueList ):
    n = valueList.pop( )

    neededPrecision = int( n * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        mp.dps = neededPrecision

    sqrt2 = sqrt( 2 )

    valueList.append( ceil( power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                               power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                                         fmul( 4, sqrt2 ) ), 2 ) ) )


#//******************************************************************************
#//
#//  getCombinations
#//
#//******************************************************************************

def getCombinations( valueList ):
    r = valueList.pop( )
    n = valueList.pop( )

    if ( r > n ):
        raise ValueError( 'Number of elements (%d) cannot exceed the size of the set (%d)' % ( r, n ) )

    valueList.append( fdiv( fac( n ), fmul( fac( r ), fac( fsub( n, r ) ) ) ) )


#//******************************************************************************
#//
#//  getPermutations
#//
#//******************************************************************************

def getPermutations( valueList ):
    r = valueList.pop( )
    n = valueList.pop( )

    if ( r > n ):
        raise ValueError( 'Number of elements (%d) cannot exceed the size of the set (%d)' % ( r, n ) )

    valueList.append( fdiv( fac( n ), fac( fsub( n, r ) ) ) )


#//******************************************************************************
#//
#//  interpretAsContinuedFraction
#//
#//******************************************************************************

def interpretAsContinuedFraction( valueList ):
    args = valueList.pop( )

    if not isinstance( args, list ):
        args = [ args ]

    fraction = ContinuedFraction( args ).getFraction( )

    valueList.append( fdiv( fraction.numerator, fraction.denominator ) )


#//******************************************************************************
#//
#//  interpretAsBase
#//
#//******************************************************************************

def interpretAsBase( valueList ):
    base = valueList.pop( )

    args = valueList.pop( )

    if isinstance( args, list ):
        args.reverse( )
    else:
        args = [ args ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    valueList.append( value )


#//******************************************************************************
#//
#//  duplicateTerm
#//
#//******************************************************************************

def duplicateTerm( valueList ):
    count = int( valueList.pop( ) )
    value = valueList.pop( )

    for i in range( 0, count ):
        if isinstance( value, list ):
            for i in value:
                valueList.append( i )
        else:
            valueList.append( value )


#//******************************************************************************
#//
#//  expandRange
#//
#//******************************************************************************

def expandRange( valueList ):
    end = int( valueList.pop( ) )
    start = int( valueList.pop( ) )

    if start > end:
        step = -1
    else:
        step = 1

    for i in range( start, end + step, step ):
        valueList.append( i )


#//******************************************************************************
#//
#//  expandSteppedRange
#//
#//******************************************************************************

def expandSteppedRange( valueList ):
    step = int( valueList.pop( ) )
    end = int( valueList.pop( ) )
    start = int( valueList.pop( ) )

    for i in range( start, end + 1, step ):
        valueList.append( i )


#//******************************************************************************
#//
#//  getPlasticConstant
#//
#//******************************************************************************

def getPlasticConstant( valueList ):
    term = fmul( 12, sqrt( 69 ) )
    valueList.append( fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 ) )


#//******************************************************************************
#//
#//  solveQuadraticPolynomial
#//
#//******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    if a == 0:
        if b == 0:
            raise ValueError( "Invalid equation, no variable coefficients" )
        else:
            # linear equation, one root
            return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


#//******************************************************************************
#//
#//  solveOrder2
#//
#//******************************************************************************

def solveOrder2( valueList ):
    c = valueList.pop( )
    b = valueList.pop( )
    a = valueList.pop( )

    valueList.append( solveQuadraticPolynomial( a, b, c ) )


#//******************************************************************************
#//
#//  solveCubicPolynomial
#//
#//  Adapted from http://www.1728.org/cubic2.htm
#//
#//******************************************************************************

def solveCubicPolynomial( a, b, c, d ):
    if a == 0:
        return solveQuadraticPolynomial( b, c, d )

    f = fdiv( fsub( fdiv( fmul( 3, c ), a ), fdiv( power( b, 2 ), power( a, 2 ) ) ), 3 )

    g = fdiv( fadd( fsub( fdiv( fmul( 2, power( b, 3 ) ), power( a, 3 ) ),
                          fdiv( fprod( [ 9, b, c ] ), power( a, 2 ) ) ),
                    fdiv( fmul( 27, d ), a ) ), 27 )
    h = fadd( fdiv( power( g, 2 ), 4 ), fdiv( power( f, 3 ), 27 ) )

    # all three roots are the same
    if h == 0:
        x1 = fneg( root( fdiv( d, a ), 3 ) )
        x2 = x1
        x3 = x2
    # two imaginary and one real root
    elif h > 0:
        r = fadd( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if r < 0:
            s = fneg( root( fneg( r ), 3 ) )
        else:
            s = root( r, 3 )

        t = fsub( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if t < 0:
            u = fneg( root( fneg( t ), 3 ) )
        else:
            u = root( t, 3 )

        x1 = fsub( fadd( s, u ), fdiv( b, fmul( 3, a ) ) )

        real = fsub( fdiv( fneg( fadd( s, u ) ), 2 ), fdiv( b, fmul( 3, a ) ) )
        imaginary = fdiv( fmul( fsub( s, u ), sqrt( 3 ) ), 2 )

        x2 = mpc( real, imaginary )
        x3 = mpc( real, fneg( imaginary ) )
    # all real roots
    else:
        j = sqrt( fsub( fdiv( power( g, 2 ), 4 ), h ) )
        k = acos( fneg( fdiv( g, fmul( 2, j ) ) ) )

        if j < 0:
            l = fneg( root( fneg( j ), 3 ) )
        else:
            l = root( j, 3 )

        m = cos( fdiv( k, 3 ) )
        n = fmul( sqrt( 3 ), sin( fdiv( k, 3 ) ) )
        p = fneg( fdiv( b, fmul( 3, a ) ) )

        x1 = fsub( fmul( fmul( 2, l ), cos( fdiv( k, 3 ) ) ), fdiv( b, fmul( 3, a ) ) )
        x2 = fadd( fmul( fneg( l ), fadd( m, n ) ), p )
        x3 = fadd( fmul( fneg( l ), fsub( m, n ) ), p )

    return [ chop( x1 ), chop( x2 ), chop( x3 ) ]


#//******************************************************************************
#//
#//  solveOrder3
#//
#//******************************************************************************

def solveOrder3( valueList ):
    d = valueList.pop( )
    c = valueList.pop( )
    b = valueList.pop( )
    a = valueList.pop( )

    valueList.append( solveCubicPolynomial( a, b, c, d ) )


#//******************************************************************************
#//
#//  solveQuarticPolynomial
#//
#//  Adapted from http://www.1728.org/quartic2.htm
#//
#//******************************************************************************

def solveQuarticPolynomial( _a, _b, _c, _d, _e ):
    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )
    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    elif _b == 0 and _c == 0 and _d == 0:
        e = fdiv( _e, _a )

        f = root( _a, 4 )

        x1 = fdiv( root( fneg( e ), 4 ), f )
        x2 = fdiv( fneg( root( fneg( e ), 4 ) ), f )
        x3 = fdiv( mpc( 0, root( fneg( e ), 4 ) ), f )
        x4 = fdiv( mpc( 0, fneg( root( fneg( e ), 4 ) ) ), f )

        return [ x1, x2, x3, x4 ]

    # otherwise we have a regular quartic to solve
    a = 1
    b = fdiv( _b, _a )
    c = fdiv( _c, _a )
    d = fdiv( _d, _a )
    e = fdiv( _e, _a )

    # we turn the equation into a cubic that we can solve
    f = fsub( c, fdiv( fmul( 3, power( b, 2 ) ), 8 ) )
    g = fsum( [ d, fdiv( power( b, 3 ), 8 ), fneg( fdiv( fmul( b, c ), 2 ) ) ] )
    h = fsum( [ e, fneg( fdiv( fmul( 3, power( b, 4 ) ), 256 ) ),
                fmul( power( b, 2 ), fdiv( c, 16 ) ), fneg( fdiv( fmul( b, d ), 4 ) ) ] )

    y1, y2, y3 = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                       fneg( fdiv( power( g, 2 ), 64 ) ) )

    # pick two non-zero roots, if there are two imaginary roots, use them
    if im( y1 ) != 0:
        root1 = y1

        if y2 == 0 or im( y2 ) == 0:
            root2 = y3
        else:
            root2 = y2
    elif y1 == 0:
        root1 = y2
        root2 = y3
    elif y2 == 0:
        root1 = y1
        root2 = y3
    else:
        root1 = y2
        root2 = y3

    # more variables...
    p = sqrt( root1 )
    q = sqrt( root2 )
    r = fdiv( fneg( g ), fprod( [ 8, p, q ] ) )
    s = fneg( fdiv( b, 4 ) )

    # put together the 4 roots
    x1 = fsum( [ p, q, r, s ] )
    x2 = fsum( [ p, fneg( q ), fneg( r ), s ] )
    x3 = fsum( [ fneg( p ), q, fneg( r ), s ] )
    x4 = fsum( [ fneg( p ), fneg( q ), r, s ] )

    return [ chop( x1 ), chop( x2 ), chop( x3 ), chop( x4 ) ]


#//******************************************************************************
#//
#//  solveOrder4
#//
#//******************************************************************************

def solveOrder4( valueList ):
    e = valueList.pop( )
    d = valueList.pop( )
    c = valueList.pop( )
    b = valueList.pop( )
    a = valueList.pop( )

    valueList.append( solveQuarticPolynomial( a, b, c, d, e ) )


#//******************************************************************************
#//
#//  solvePolynomial
#//
#//******************************************************************************

def solvePolynomial( valueList ):
    args = valueList.pop( )

    if isinstance( args, list ):
        args.reverse( )
    else:
        args = [ args ]

    if len( args ) < 2:
        raise ValueError( "solve requires at least an order-1 polynomial (i.e., 2 terms)" )

    valueList.append( polyroots( args ) )


#//******************************************************************************
#//
#//  incrementNestedListLevel
#//
#//******************************************************************************

def incrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel += 1

    valueList.append( list( ) )


#//******************************************************************************
#//
#//  decrementNestedListLevel
#//
#//******************************************************************************

def decrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel -= 1

    if nestedListLevel < 0:
        raise ValueError( "Negative list level (too many ']'s)" )


#//******************************************************************************
#//
#//  getCurrentArgList
#//
#//******************************************************************************

def getCurrentArgList( valueList ):
    global nestedListLevel

    argList = valueList

    for i in range( 0, nestedListLevel ):
        argList = argList[ -1 ]

    return argList


#//******************************************************************************
#//
#//  expressions
#//
#//  Function names and number of args needed.  One line/zero-or-one arg
#//  functions are implemented as lambdas.
#//
#//  If the number of arguments is -1, then a list argument is expected.
#//
#//******************************************************************************

expressions = {
    '!'         : [ lambda v: v.append( fac( v.pop( ) ) ), [ numberArg ] ],
    '%'         : [ getModulo, [ numberArg ] * 2 ],
    '*'         : [ lambda v: v.append( fmul( v.pop( ), v.pop( ) ) ), [ numberArg ] * 2 ],
    '**'        : [ exponentiate, [ numberArg ] * 2 ],
    '***'       : [ tetrate, [ numberArg ] * 2 ],
    '+'         : [ lambda v: v.append( fadd( v.pop( ), v.pop( ) ) ), [ numberArg ] * 2 ],
    '-'         : [ subtract, [ numberArg ] * 2 ],
    '/'         : [ divide, [ numberArg ] * 2 ],
    '1/x'       : [ lambda v: v.append( fdiv( 1, v.pop( ) ) ), [ numberArg ] ],
    'abs'       : [ lambda v: v.append( fabs( v.pop( ) ) ), [ numberArg ] ],
    'acos'      : [ lambda v: v.append( acos( v.pop( ) ) ), [ numberArg ] ],
    'acosh'     : [ lambda v: v.append( acosh( v.pop( ) ) ), [ numberArg ] ],
    'acosh'     : [ lambda v: v.append( acosh( v.pop( ) ) ), [ numberArg ] ],
    'acot'      : [ lambda v: v.append( acot( v.pop( ) ) ), [ numberArg ] ],
    'acoth'     : [ lambda v: v.append( acoth( v.pop( ) ) ), [ numberArg ] ],
    'acsc'      : [ lambda v: v.append( acsc( v.pop( ) ) ), [ numberArg ] ],
    'acsch'     : [ lambda v: v.append( acsch( v.pop( ) ) ), [ numberArg ] ],
    'and'       : [ lambda v: performBitwiseOperation( v, lambda x, y:  x & y ), [ numberArg ] * 2 ],
    'antihex'   : [ getAntiHexagonalNumber, [ numberArg ] ],
    'antipent'  : [ getAntiPentagonalNumber, [ numberArg ] ],
    'antitri'   : [ getAntiTriangularNumber, [ numberArg ] ],
    'apery'     : [ lambda v: v.append( apery ), [ ] ],
    'asec'      : [ lambda v: v.append( asec( v.pop( ) ) ), [ numberArg ] ],
    'asech'     : [ lambda v: v.append( asech( v.pop( ) ) ), [ numberArg ] ],
    'asin'      : [ lambda v: v.append( asin( v.pop( ) ) ), [ numberArg ] ],
    'asinh'     : [ lambda v: v.append( asinh( v.pop( ) ) ), [ numberArg ] ],
    'atan'      : [ lambda v: v.append( atan( v.pop( ) ) ), [ numberArg ] ],
    'atanh'     : [ lambda v: v.append( atanh( v.pop( ) ) ), [ numberArg ] ],
    'avg'       : [ getMean, [ listArg ] ],
    'base'      : [ interpretAsBase, [ listArg, numberArg ] ],
    'catalan'   : [ lambda v: v.append( catalan ), [ ] ],
    'cbrt'      : [ lambda v: v.append( cbrt( v.pop( ) ) ), [ numberArg ] ],
    'ceil'      : [ lambda v: v.append( ceil( v.pop( ) ) ), [ numberArg ] ],
    'cf'        : [ interpretAsContinuedFraction, [ listArg ] ],
    'cos'       : [ lambda v: v.append( cos( v.pop( ) ) ), [ numberArg ] ],
    'cosh'      : [ lambda v: v.append( cosh( v.pop( ) ) ), [ numberArg ] ],
    'cot'       : [ lambda v: v.append( cot( v.pop( ) ) ), [ numberArg ] ],
    'coth'      : [ lambda v: v.append( coth( v.pop( ) ) ), [ numberArg ] ],
    'csc'       : [ lambda v: v.append( csc( v.pop( ) ) ), [ numberArg ] ],
    'csch'      : [ lambda v: v.append( csch( v.pop( ) ) ), [ numberArg ] ],
    'cube'      : [ lambda v: v.append( power( v.pop( ), 3 ) ), [ numberArg ] ],
    'deg'       : [ lambda v: v.append( radians( v.pop( ) ) ), [ numberArg ] ],
    'degrees'   : [ lambda v: v.append( radians( v.pop( ) ) ), [ numberArg ] ],
    'dup'       : [ duplicateTerm, [ listArg, numberArg ] ],
    'e'         : [ lambda v: v.append( e ), [ ] ],
    'euler'     : [ lambda v: v.append( euler ), [ ] ],
    'exp'       : [ lambda v: v.append( exp( v.pop( ) ) ), [ numberArg ] ],
    'exp10'     : [ lambda v: v.append( power( 10, v.pop( ) ) ), [ numberArg ] ],
    'expphi'    : [ lambda v: v.append( power( phi, v.pop( ) ) ), [ numberArg ] ],
    'fac'       : [ lambda v: v.append( fac( v.pop( ) ) ), [ numberArg ] ],
    'fib'       : [ lambda v: v.append( fib( v.pop( ) ) ), [ numberArg ] ],
    'floor'     : [ lambda v: v.append( floor( v.pop( ) ) ), [ numberArg ] ],
    'gamma'     : [ lambda v: v.append( gamma( v.pop( ) ) ), [ numberArg ] ],
    'glaisher'  : [ lambda v: v.append( glaisher ), [ ] ],
    'harm'      : [ lambda v: v.append( harmonic( v.pop( ) ) ), [ numberArg ] ],
    'harmonic'  : [ lambda v: v.append( harmonic( v.pop( ) ) ), [ numberArg ] ],
    'hex'       : [ getNthHexagonalNumber, [ numberArg ] ],
    'hyper4_2'  : [ tetrateLarge, [ numberArg ] * 2 ],
    'hyperfac'  : [ lambda v: v.append( hyperfac( v.pop( ) ) ), [ numberArg ] ],
    'hypot'     : [ lambda v: v.append( hypot( v.pop( ), v.pop( ) ) ), [ numberArg ] * 2 ],
    'inv'       : [ lambda v: v.append( fdiv( 1, v.pop( ) ) ), [ numberArg ] ],
    'itoi'      : [ lambda v: v.append( exp( fmul( -0.5, pi ) ) ), [ ] ],
    'khinchin'  : [ lambda v: v.append( khinchin ), [ ] ],
    'lgamma'    : [ lambda v: v.append( loggamma( v.pop( ) ) ), [ numberArg ] ],
    'ln'        : [ lambda v: v.append( ln( v.pop( ) ) ), [ numberArg ] ],
    'log'       : [ lambda v: v.append( ln( v.pop( ) ) ), [ numberArg ] ],
    'log10'     : [ lambda v: v.append( log10( v.pop( ) ) ), [ numberArg ] ],
    'logxy'     : [ getLogXY, [ numberArg ] * 2 ],
    'luc'       : [ getNthLucas, [ numberArg ] ],
    'lucas'     : [ getNthLucas, [ numberArg ] ],
    'mean'      : [ getMean, [ listArg ] ],
    'mertens'   : [ lambda v: v.append( mertens ), [ ] ],
    'mod'       : [ getModulo, [ numberArg ] * 2 ],
    'modulo'    : [ getModulo, [ numberArg ] * 2 ],
    'mult'      : [ multiplyAll, [ listArg ] ],
    'nCr'       : [ getCombinations, [ numberArg ] * 2 ],
    'ncr'       : [ getCombinations, [ numberArg ] * 2 ],
    'neg'       : [ lambda v: v.append( fneg( v.pop( ) ) ), [ numberArg ] ],
    'npr'       : [ getPermutations, [ numberArg ] * 2 ],
    'nPr'       : [ getPermutations, [ numberArg ] * 2 ],
    'omega'     : [ lambda v: v.append( lambertw( 1 ) ), [ ] ],
    'or'        : [ lambda v: performBitwiseOperation( v, lambda x, y:  x | y ), [ numberArg ] * 2 ],
    'pent'      : [ getNthPentagonalNumber, [ numberArg ] ],
    'phi'       : [ lambda v: v.append( phi ), [ ] ],
    'pi'        : [ lambda v: v.append( pi ), [ ] ],
    'plastic'   : [ getPlasticConstant, [ ] ],
    'prod'      : [ multiplyAll, [ listArg ] ],
    'rad'       : [ lambda v: v.append( degrees( v.pop( ) ) ), [ numberArg ] ],
    'radians'   : [ lambda v: v.append( degrees( v.pop( ) ) ), [ numberArg ] ],
    'rand'      : [ lambda v: v.append( rand( ) ), [ ] ],
    'random'    : [ lambda v: v.append( rand( ) ), [ ] ],
    'range'     : [ expandRange, [ numberArg ] * 2 ],
    'range2'    : [ expandSteppedRange, [ numberArg ] * 3 ],
    'root'      : [ antiexponentiate, [ numberArg ] * 2 ],
    'root2'     : [ lambda v: v.append( sqrt( v.pop( ) ) ), [ numberArg ] ],
    'root3'     : [ lambda v: v.append( cbrt( v.pop( ) ) ), [ numberArg ] ],
    'round'     : [ lambda v: v.append( floor( fadd( v.pop( ), 0.5 ) ) ), [ numberArg ] ],
    'sec'       : [ lambda v: v.append( sec( v.pop( ) ) ), [ numberArg ] ],
    'sech'      : [ lambda v: v.append( sech( v.pop( ) ) ), [ numberArg ] ],
    'sin'       : [ lambda v: v.append( sin( v.pop( ) ) ), [ numberArg ] ],
    'sinh'      : [ lambda v: v.append( sinh( v.pop( ) ) ), [ numberArg ] ],
    'solve'     : [ solvePolynomial, [ listArg ] ],
    'solve2'    : [ solveOrder2, [ numberArg ] * 3 ],
    'solve3'    : [ solveOrder3, [ numberArg ] * 4 ],
    'solve4'    : [ solveOrder4, [ numberArg ] * 5 ],
    'sqr'       : [ lambda v: v.append( power( v.pop( ), 2 ) ), [ numberArg ] ],
    'sqrt'      : [ lambda v: v.append( sqrt( v.pop( ) ) ), [ numberArg ] ],
    'sqtri'     : [ getNthSquareTriangularNumber, [ numberArg ] ],
    'sum'       : [ sum, [ listArg ] ],
    'superfac'  : [ lambda v: v.append( superfac( v.pop( ) ) ), [ numberArg ] ],
    'tan'       : [ lambda v: v.append( tan( v.pop( ) ) ), [ numberArg ] ],
    'tanh'      : [ lambda v: v.append( tanh( v.pop( ) ) ), [ numberArg ] ],
    'tet'       : [ getNthTetrahedralNumber, [ numberArg ] ],
    'tetra'     : [ getNthTetrahedralNumber, [ numberArg ] ],
    'tri'       : [ getNthTriangularNumber, [ numberArg ] ],
    'twinprime' : [ lambda v: v.append( twinprime ), [ ] ],
    'xor'       : [ lambda v: performBitwiseOperation( v, lambda x, y:  x ^ y ), [ numberArg ] * 2 ],
    '['         : [ incrementNestedListLevel, [ ] ],
    ']'         : [ decrementNestedListLevel, [ ] ],
    '^'         : [ exponentiate, [ numberArg ] * 2 ],
    '~'         : [ getInvertedBits, [ numberArg ] ],
#    'antitet'  : [ getAntiTetrahedralNumber, [ numberArg ] ],
#    'isprime'  : [ isPrime, [ numberArg ] ],
#    'powmod'   : [ getPowMod, [ numberArg ] * 3 ],
}


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  Parse out a numerical expression and attempt to set the precision to an
#//  appropriate value based on the expression.
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
    if term == '0':
        return mpmathify( 0 )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

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
            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


#//******************************************************************************
#//
#//  roundMantissa
#//
#//******************************************************************************

def roundMantissa( mantissa, accuracy ):
    if len( mantissa ) <= accuracy:
        return mantissa

    last_digit = int( mantissa[ accuracy - 1 ] )
    extra_digit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extra_digit >= 5:
        result += str( last_digit + 1 )
    else:
        result += str( last_digit )

    return result


#//******************************************************************************
#//
#//  formatOutput
#//
#//  This takes a string representation of the result and formats it according
#//  to a whole bunch of options.
#//
#//******************************************************************************

def formatOutput( output, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                  decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    imaginary = im( mpmathify( output ) )

    if imaginary != 0:
        if imaginary < 0:
            imaginary = fabs( imaginary )
            negativeImaginary = True
        else:
            negativeImaginary = False

        imaginaryValue = formatOutput( nstr( imaginary, mp.dps ), radix, numerals, integerGrouping,
                                       integerDelimiter, leadingZero, decimalGrouping, decimalDelimiter,
                                       baseAsDigits, outputAccuracy )

        strOutput = str( re( mpmathify( output ) ) )
    else:
        imaginaryValue = ''
        strOutput = str( output )

    if '.' in strOutput and strOutput.find( 'e' ) == -1:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    strResult = '';

    integer = strOutput[ 1 if negative else 0 : decimal ]
    integerLength = len( integer )

    mantissa = strOutput[ decimal + 1 : ]

    if mantissa != '':
        if outputAccuracy == -1:
            mantissa = mantissa.rstrip( '0' )

    #print( "mantissa: %s" % mantissa )
    #print( "output: %s" % output )

    if radix == phiBase:
        integer, mantissa = convertToPhiBase( mpmathify( output ) )
    elif radix == fibBase:
        integer = convertToFibBase( floor( mpmathify( output ) ) )
    elif radix != 10 or numerals != defaultNumerals:
        integer = str( convertToBaseN( mpmathify( integer ), radix, baseAsDigits, numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpmathify( '0.' + mantissa ), radix,
                            int( ( mp.dps - integerLength ) / math.log10( radix ) ),
                            baseAsDigits, outputAccuracy ) )
    else:
        if outputAccuracy == 0:
            mantissa = ''
        elif outputAccuracy > 0:
            mantissa = roundMantissa( mantissa, outputAccuracy )

    if integerGrouping > 0:
        firstDelimiter = len( integer ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += integer[ : firstDelimiter ]

        for i in range( firstDelimiter, len( integer ), integerGrouping ):
            if integerResult != '':
                integerResult += integerDelimiter

            integerResult += integer[ i : i + integerGrouping ]

    else:
        integerResult = integer

    if decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( mantissa ), decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += decimalDelimiter

            mantissaResult += mantissa[ i : i + decimalGrouping ]
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

    return result


#//******************************************************************************
#//
#//  printMoreHelp
#//
#//******************************************************************************

def printMoreHelp( ):
    print(
'''
Arguments are interpreted as Reverse Polish Notation.

Supported unary operators (synonyms are separated by commas):
    !, fac; %, mod, modulo; 1/x, inv (take reciprocal); abs;
    cbrt, root3 (cube root); ceil; cube; exp; exp10; expphi; floor; gamma;
    hypot; hyperfac; lgamma; log, ln; log10; neg; rand; round; sqr;
    sqrt, root2; superfac

Supported unary trigonometric operators:
    deg, degrees (treat term as degrees (i.e., convert to radians), e.g.,
    "rpn 45 degrees tan"); rad, radians (treat term as radians (i.e., convert
    to degrees), e.g., "rpn pi radians")

    sin; asin; sinh; asinh; cos; acos; cosh; acosh; tan; atan; tanh; atanh;
    sec; asec; sech; asech; csc; acsc; csch; acsch; cot; acot; coth; acoth

Supported integer sequence unary operators:
    fib (nth Fibonacci number); luc (nth Lucas number);
    tri (nth triangular number); antitri (which triangular number is this);
    pent (nth pentagonal number); antipent (which pentagonal number is this);
    hex (nth hexagonal number); antihex (which hexagonal number is this);
    sqtri (nth square triangular number)*; tet, tetra (nth tetrahedral number)

    * requires sufficient precision for accuracy (see Notes)

Supported binary operators:
    +; -; *; /; **, ^ (power); *** (tetration); // (root); logxy;
    nCr, ncr (combinations); nRp, nrp (permutations), dup (duplicate previous
    term a number of times, useful with cf)

Supported multi operators (operate on all preceding operands):
    sum; mult; mean, cf (treat all preceding terms as part of a continued
    fraction, and evalutate), base (sort of the reverse of -R, with the
    base being the last argument)

Supported constants:
    e; pi; phi (the Golden Ratio); itoi (i^i); euler (Euler's constant);
    catalan (Catalan's constant); apery (Apery's constant); khinchin
    (Khinchin's constant); glaisher (Glaisher's constant); mertens (Merten's
    constant); twinprime (Twin prime constant), omega (Omega constant)

Supported bitwise operators:
    ~, not; and; or; xor

Polynomial solvers:
    solve2 (solve quadratic equation, 3 args)
    solve3 (solve cubic equation, 4 args)
    solve4 (solve quartic equation, 5 args)
    solve  (solve arbitrary polynomial, list of coefficients followed by
            the number of coefficients )

Input:
    For integers, rpn understands hexidecimal input of the form '0x....'.
    Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B'
    is interpreted as binary.  Decimal points are not allowed for binary,
    octal or hexadecimal modes, but fractional numbers in another base can be
    input using -b.

    A leading '\\' forces the term to be a number rather than an operator (for
    use with higher bases with -b).

Notes:
    When converting fractional output to other bases, rpn adjusts the precision
    to the approximate equivalent for the new base since the precision is
    applicable to base 10.

    Tetration (hyperexponentiation) forces the second argument to an integer.

    To compute the nth Fibonacci number accurately, rpn sets the precision to
    a level sufficient to guarantee a correct answer.

    Some of the trig functions return complex results as provided by mpmath,
    but rpn doesn't otherwise support complex numbers.

    Bitwise operators force all arguments to integers by truncation if
    necessary.
''' )


#//******************************************************************************
#//
#//  printEvenMoreHelp
#//
#//******************************************************************************

def printEvenMoreHelp( ):
    print(
'''
Examples of rpn usage follow.

Basic arithmetic operations:

    c:\>rpn 2 3 +
    5

    c:\>rpn 12 9 -
    3

    c:\>rpn 23 47 *
    1081

    c:\>rpn 10 7 /
    1.42857142857

Basic trigonometry usage:

    c:\>rpn 60 deg sin         # sine of 60 degrees
    0.866025403784

    c:\>rpn 45 deg tan         # tangent of 45 degrees
    1

    c:\>rpn 2 pi * rad         # 2 pi radians is how many degrees?
    360

    c:\>rpn 2 atan rad         # What angle (in degrees) has a slope of 2?
    63.4349488229

Convert an IP address to a 32-bit value and back:

    c:\>rpn 192 168 0 1 256 base -x
    c0a8 0001

    c:\>rpn 0xc0a80001 -R 256
    192 168 0 1

Construct the square root of two from a continued fraction:

    c:\>rpn 2 sqrt
    1.41421356237

    c:\>rpn 2 sqrt -e20 -p20
    1.4142135623730950488
        = [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ~= 22619537/15994428

    c:\>rpn 1 2 20 dup cf -p20
    1.41421356237

''' )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global numerals
    global bitwiseGroupSize
    global addToListArgument

    if os.name == 'nt':
        argumentPrefix = argumentPrefixWindows
        prefixList = prefixListWindows
    else:
        argumentPrefix = argumentPrefixLinux
        prefixList = prefixListLinux

    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + RPN_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars=prefixList )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=-1, const=defaultAccuracy,
                         help="maximum number of decimal places to display, irrespective\nof internal precision (default:  " +
                              str( defaultAccuracy ) + ")" )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix,
                         help="specify the radix for input (default:  " + str( defaultInputRadix ) + ")" )
    parser.add_argument( '-c', '--comma', action='store_true',
                         help="add commas to result, e.g., 1,234,567.0" )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping, help="display decimal places separated into groups (default: " +
                                                            str( defaultDecimalGrouping ) + ")" )
    parser.add_argument( '-e', '--continued_fraction', nargs='?', type=int, action='store', default=0,
                         const=defaultCFTerms, help="number of terms to represent as a continued fraction" )
    parser.add_argument( '-f', '--factor', action='store_true',
                         help="compute prime factors of result (truncated to an integer)" )
    parser.add_argument( '-hh', '--more_help', action='store_true',
                         help="display additional help information" )
    parser.add_argument( '-hhh', '--even_more_help', action='store_true',
                         help="display examples of various rpn functionality in use" )
    parser.add_argument( '-i', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping,
                         help="display integer separated into groups (default: " + str( defaultIntegerGrouping ) + ")" )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals,
                         help="characters set to use as numerals for output" )
    parser.add_argument( '-o', '--octal', action='store_true', help="octal mode: equivalent to '-r8 -w9 -i3 -z'" )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision,
                         help="precision, i.e., number of significant digits to use" )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix,
                         help="output in a different base (2 to 62, or phi)" )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0,
                         help="each digit is a space-delimited base-10 number" )
    parser.add_argument( '-u', '--find_poly', type=int, action='store', default=0,
                         help="find a polynomial such that P(x) ~= 0 of degree <= N" )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store', default=defaultBitwiseGroupSize,
                         help="bitwise operations group values by this size (default: " +
                              str( defaultBitwiseGroupSize ) + ")" )
    parser.add_argument( '-x', '--hex', action='store_true', help="hex mode: equivalent to '-r16 -w16 -i4 -z'" )
    parser.add_argument( '-y', '--identify', action='store_true', help="identify the result (may repeat input)" )
    parser.add_argument( '-z', '--leading_zero', action='store_true', help="add leading zeros if needed with -i" )
    parser.add_argument( '-?', '--print_options', action='store_true', help="print values for all options" )

    # OK, let's parse and validate the arguments
    if len( sys.argv ) == 1:
        parser.print_help( )
        return

    args = parser.parse_args( )
    mp.dps = args.precision

    if args.more_help:
        printMoreHelp( )
        return

    if args.even_more_help:
        printEvenMoreHelp( )
        return

    # these are either globals or can be modified by other options (like -x)
    bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -e - set precision equal to the number of continued fraction items to print for accuracy
    if mp.dps < args.continued_fraction:
        mp.dps = args.continued_fraction

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( "rpn:  can't interpret output radix '%s' as a number" % args.output_radix )
            return

    numerals = args.numerals

    # handle -x
    if args.hex:
        if outputRadix != 10 and outputRadix != 16:
            print( "rpn:  -r and -x can't be used together" )
            return

        if args.octal:
            print( "rpn:  -x and -o can't be used together" )
            return

        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        if outputRadix != 10 and outputRadix != 8:
            print( "rpn:  -r and -o can't be used together" )
            return

        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        bitwiseGroupSize = 9

    # handle -b
    inputRadix = int( args.input_radix )

    # handle -R
    if args.output_radix_numerals > 0:
        if args.hex:
            print( "rpn:  -R and -x can't be used together" )
            return

        if args.output_radix != 10:
            print( "rpn:  -R and -r can't be used together" )
            return

        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( "rpn:  output radix must be greater than 1" )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( "rpn:  output radix must be from 2 to 62, or phi" )
            return

    if args.comma and args.integer_grouping > 0 :
        print( "rpn:  -c can't be used with -i" )
        return

    if baseAsDigits and ( args.comma or args.decimal_grouping > 0 or args.integer_grouping > 0 ):
        print( "rpn:  -c, -d and -i can't be used with -R" )
        return

    # handle -y and -u:  mpmath wants precision of at least 53 for these functions
    if args.identify or args.find_poly > 0:
        if mp.dps < 53:
            mp.dps = 53

    index = 1                 # only used for error messages
    valueList = list( )

    if args.print_options:
        print( '--output_accuracy:  %d' % args.output_accuracy )
        print( '--input_radix:  %d'% inputRadix )
        print( '--comma:  ' + ( 'true' if args.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % args.decimal_grouping )
        print( '--continued_fraction:  %d' % args.continued_fraction )
        print( '--factor:  ' + ( 'true' if args.factor else 'false' ) )
        print( '--integer_grouping:  %d' % integerGrouping )
        print( '--numerals:  ' + args.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % args.output_radix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

    if len( args.terms ) == 0:
        print( "rpn:  no terms found" )
        return

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        currentValueList = getCurrentArgList( valueList )
        #print( "valueList: " + str( valueList ) )
        #print( "current: " + str( currentValueList ) )

        if term in expressions:
            argsListNeeded = expressions[ term ][ 1 ]
            parseError = False
            argsNeeded = len( argsListNeeded )
            currentValueList = getCurrentArgList( valueList )

            if len( currentValueList ) < argsNeeded:
                print( "rpn:  error in arg " + format( index ) + ":  operator " + term + " requires " +
                       format( argsNeeded ) + " argument", end='' )

                if argsNeeded > 1:
                    print( "s" )
                else:
                    print( "" )

                break   # breaks out of term in args.terms, setting parseError isn't needed

            for i in range( argsNeeded, 0, -1 ):
                argType = argsListNeeded[ -i ]
                arg = currentValueList[ -i ]

                isList = isinstance( arg, list )

                # a numerical argument is OK when a list is expected
                if argType == numberArg and isList:
                    print( "rpn:  operator '" + term + "' expects a numerical argument, not a list" )

                    parseError = True
                    break

            if parseError:
                break

            try:
                expressions[ term ][ 0 ]( currentValueList )   # evaluate the expression
            except KeyboardInterrupt as error:
                print( "rpn:  keyboard interrupt" )
                break
            except ValueError as error:
                print( "rpn:  error in arg " + format( index ) + ":  {0}".format( error ) )
                break
        else:
            try:
                currentValueList.append( parseInputValue( term, inputRadix ) )
            except ValueError as error:
                print( "rpn:  error in arg " + format( index ) + ":  {0}".format( error ) )
                break
            except TypeError as error:
                print( "rpn:  error in arg " + format( index ) + ":  unrecognized argument: '%s'" % sys.argv[ index ] )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1:
            print( "rpn:  unexpected end of input" )
        else:
            mp.pretty = True
            result = valueList.pop( )

            if args.comma:
                integerGrouping = 3     # overridde whatever was set on the command-line
                leadingZero = False     # this one, too
                integerDelimiter = ','
            else:
                integerDelimiter = ' '

            if isinstance( result, list ):
                resultString = ''

                for item in result:
                    if resultString == '':
                        resultString = '[ '
                    else:
                        resultString += ', '

                    itemString = nstr( item, mp.dps )

                    resultString += formatOutput( itemString, outputRadix, numerals, integerGrouping,
                                               integerDelimiter, leadingZero, args.decimal_grouping, ' ',
                                               baseAsDigits, args.output_accuracy )

                print( resultString + ' ]' )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                print( formatOutput( resultString, outputRadix, numerals, integerGrouping, integerDelimiter,
                                     leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                     args.output_accuracy ) )

                # handle --factor
                if args.factor:
                    try:
                        factorInteger( int( floor( result ) ) )
                    except KeyboardInterrupt as error:
                        print( 'rpn:  keyboard interrupt' )
                        return

                # handle --continued_fraction
                if args.continued_fraction:
                    try:
                        cf = ContinuedFraction( mpmathify( result ), maxterms=args.continued_fraction )
                    except KeyboardInterrupt as error:
                        print( 'rpn:  keyboard interrupt' )
                        return

                    # format the fraction output
                    fraction = str( cf.getFraction( ) )
                    solidus = fraction.find( '/' )

                    if solidus == -1:    # should never happen
                        numerator = fraction
                        denominator = ''
                    else:
                        numerator = fraction[ : solidus ]
                        denominator = fraction [ solidus + 1 : ]

                    numerator = formatOutput( numerator, outputRadix, numerals, integerGrouping, integerDelimiter,
                                              leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                              args.output_accuracy )

                    if denominator != '':
                        denominator = formatOutput( denominator, outputRadix, numerals, integerGrouping, integerDelimiter,
                                                    leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                                    args.output_accuracy )

                    print( '    = ' + str( cf ) )
                    print( '    ~= ' + numerator + ' / ' + denominator )

                # handle --identify
                if args.identify:
                    formula = identify( result )

                    if formula is None:
                        print( '    = [formula cannot be found]' )
                    else:
                        print( '    = ' + formula )

                # handle --find_poly
                if args.find_poly > 0:
                    poly = str( findpoly( result, args.find_poly ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

