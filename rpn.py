#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import math
import random
import sys
from mpmath import *


#//******************************************************************************
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = "rpn"
RPN_VERSION = "3.0.0"
PROGRAM_DESCRIPTION = 'RPN command-line calculator'
COPYRIGHT_MESSAGE = "copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 12

defaultNumerals = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

numerals = ""

phiBase = -1
fibBase = -2


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
        #print( remaining )
        place = int( floor( log( remaining, phi ) ) )
        #print( place )

        if start:
            output = '1'
            start = False
            originalPlace = place
        else:
            if place < -originalPlace:
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
#//******************************************************************************

def convertToFibBase( num ):
    return '***fib-base***'


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//******************************************************************************

def convertToBaseN( value, base, baseAsDigits, numerals ):
    """
    Converts any integer to a base 2-62 string.

    For example:
    >>> convertToBaseN( -13, 4 )
    '-31'
    >>> convertToBaseN( 91321, 2 )
    '10110010010111001'
    >>> convertToBaseN( 791321, 36 )
    'gyl5'
    """

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

def convertFractionToBaseN( value, base, precision, baseAsDigits ):
    """
    Convert any fraction to base/radix 2-36 and returns the resulting mantissa as a string.

    0 <= value < 1

    For example:
    >>> convertFractionToBaseN( 1 / 64, 16, 10, False )
    '04'
    >>> convertFractionToBaseN( 1 / 11, 2, 10, False )
    '0001011101'
    >>> convertFractionToBaseN( 1 / 13, 36, 12, False )
    '2rox8b2rox8b'
    >>> convertFractionToBaseN( 1 / 13, 50, 12, True )
    ''
    """

    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'Base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'Base must be from 2 to %d' % len( numerals ) )

    if value < 0 or value >= 1.0:
        raise ValueError( 'Value must be >= 0 and < 1.0' )

    result = ''

    while value > 0 and precision > 0:
        value = value * base
        digit = int( value )

        if baseAsDigits:
            if result != '':
                result += ' '

            result += str( digit % base )
        else:
            result += numerals[ digit % base ]

        value -= digit
        precision -= 1

    return result


#//******************************************************************************
#//
#//  convertToBase10
#//
#//******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpf( 0 )
    base = mpf( 1 )

    validNumerals = numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'Invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = mpf( 1 ) / inputRadix

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'Invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


#//******************************************************************************
#//
#//  getPi
#//
#//******************************************************************************

def getPi( valueList ):
    valueList.append( pi )


#//******************************************************************************
#//
#//  getE
#//
#//******************************************************************************

def getE( valueList ):
    valueList.append( e )


#//******************************************************************************
#//
#//  getPhi
#//
#//******************************************************************************

def getPhi( valueList ):
    valueList.append( phi )


#//******************************************************************************
#//
#//  getIToTheIPower
#//
#//******************************************************************************

def getIToTheIPower( valueList ):
    valueList.append( fexp( mpf( -0.5 ) * pi ) )


#//******************************************************************************
#//
#//  add
#//
#//******************************************************************************

def add( valueList ):
    value = valueList.pop( )
    valueList.append( fadd( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  sum
#//
#//******************************************************************************

def sum( valueList ):
    result = valueList.pop( )

    while valueList:
        result = fadd( result, valueList.pop( ) )

    valueList.append( result )


#//******************************************************************************
#//
#//  getMean
#//
#//******************************************************************************

def getMean( valueList ):
    count = 1
    result = valueList.pop( )

    while valueList:
        result = fadd( result, valueList.pop( ) )
        count += 1

    valueList.append( result / count )


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
#//  multiply
#//
#//******************************************************************************

def multiply( valueList ):
    value = valueList.pop( )
    valueList.append( fmul( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  multiplyAll
#//
#//******************************************************************************

def multiplyAll( valueList ):
    result = valueList.pop( )

    while valueList:
        value = valueList.pop( )
        result *= value

    valueList.append( result )


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
#//  getHypotenuse
#//
#//******************************************************************************

def getHypotenuse( valueList ):
    value = valueList.pop( )
    valueList.append( hypot( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  getAbsoluteValue
#//
#//******************************************************************************

def getAbsoluteValue( valueList ):
    valueList.append( fabs( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getNegative
#//
#//******************************************************************************

def getNegative( valueList ):
    valueList.append( fneg( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getRandom
#//
#//******************************************************************************

def getRandom( valueList ):
    valueList.append( rand( ) )


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
        result = power( power, operand )

    valueList.append( result )


#//******************************************************************************
#//
#//  tetrate2
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
#//  getSquare
#//
#//******************************************************************************

def getSquare( valueList ):
    value = valueList.pop( )
    valueList.append( power( value, 2 ) )


#//******************************************************************************
#//
#//  getCube
#//
#//******************************************************************************

def getCube( valueList ):
    value = valueList.pop( )
    valueList.append( power( value, 3 ) )


#//******************************************************************************
#//
#//  getSquareRoot
#//
#//******************************************************************************

def getSquareRoot( valueList ):
    valueList.append( sqrt( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getCubeRoot
#//
#//******************************************************************************

def getCubeRoot( valueList ):
    valueList.append( cbrt( valueList.pop( ) ) )


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
#//  getFactorial
#//
#//******************************************************************************

def getFactorial( valueList ):
    valueList.append( fac( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getSuperfactorial
#//
#//******************************************************************************

def getSuperfactorial( valueList ):
    valueList.append( superfac( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getHyperfactorial
#//
#//******************************************************************************

def getHyperfactorial( valueList ):
    valueList.append( hyperfac( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getHarmonic
#//
#//******************************************************************************

def getHarmonic( valueList ):
    valueList.append( harmonic( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getLog
#//
#//******************************************************************************

def getLog( valueList ):
    valueList.append( ln( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getLog10
#//
#//******************************************************************************

def getLog10( valueList ):
    valueList.append( log10( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getGamma
#//
#//******************************************************************************

def getGamma( valueList ):
    valueList.append( gamma( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getLGamma
#//
#//******************************************************************************

def getLGamma( valueList ):
    valueList.append( loggamma( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getExp
#//
#//******************************************************************************

def getExp( valueList ):
    valueList.append( exp( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getExp10
#//
#//******************************************************************************

def getExp10( valueList ):
    valueList.append( power( 10, valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getExpPhi
#//
#//******************************************************************************

def getExpPhi( valueList ):
    valueList.append( power( phi, valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getSine
#//
#//******************************************************************************

def getSine( valueList ):
    valueList.append( sin( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getArcsine
#//
#//******************************************************************************

def getArcsine( valueList ):
    valueList.append( asin( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getCosine
#//
#//******************************************************************************

def getCosine( valueList ):
    valueList.append( cos( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getArccosine
#//
#//******************************************************************************

def getArccosine( valueList ):
    valueList.append( acos( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getTangent
#//
#//******************************************************************************

def getTangent( valueList ):
    valueList.append( tan( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getArctangent
#//
#//******************************************************************************

def getArctangent( valueList ):
    valueList.append( atan( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  convertRadiansToDegrees
#//
#//******************************************************************************

def convertRadiansToDegrees( valueList ):
    valueList.append( degrees( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  convertDegreesToRadians
#//
#//******************************************************************************

def convertDegreesToRadians( valueList ):
    valueList.append( radians( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getNthFibonacci
#//
#//******************************************************************************

def getNthFibonacci( valueList ):
    n = valueList.append( fib( valueList.pop( ) ) )


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
    valueList.append( ( ( 3 * n * n ) - n ) / 2 )


#//******************************************************************************
#//
#//  getAntiPentagonalNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiPentagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( fdiv( fadd( power( ( fadd( fmul( 24 , n ), 1 ) ), 0.5 ), 1 ), 6 ) )


#//******************************************************************************
#//
#//  getNthHexagonalNumber
#//
#//******************************************************************************

def getNthHexagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( ( 2 * n * n ) - n )


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

# p=(1/6)*(n^3+3*n^2+2*n)

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
#//  getFloor
#//
#//******************************************************************************

def getFloor( valueList ):
    valueList.append( floor( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getCeiling
#//
#//******************************************************************************

def getCeiling( valueList ):
    valueList.append( ceil( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  expressions
#//
#//  Function names and number of args needed
#//
#//******************************************************************************

expressions = {
    '!'        : [ getFactorial, 1 ],
    '%'        : [ getModulo, 2 ],
    '*'        : [ multiply, 2 ],
    '**'       : [ exponentiate, 2 ],
    '***'      : [ tetrate, 2 ],
    '+'        : [ add, 2 ],
    '-'        : [ subtract, 2 ],
    '/'        : [ divide, 2 ],
    '//'       : [ antiexponentiate, 2 ],
    'abs'      : [ getAbsoluteValue, 1 ],
    'acos'     : [ getArccosine, 1 ],
    'antihex'  : [ getAntiHexagonalNumber, 1 ],
    'antipent' : [ getAntiPentagonalNumber, 1 ],
    'antitri'  : [ getAntiTriangularNumber, 1 ],
    'asin'     : [ getArcsine, 1 ],
    'atan'     : [ getArctangent, 1 ],
    'cbrt'     : [ getCubeRoot, 1 ],
    'ceil'     : [ getCeiling, 1 ],
    'cos'      : [ getCosine, 1 ],
    'cosine'   : [ getCosine, 1 ],
    'cube'     : [ getCube, 1 ],
    'deg'      : [ convertRadiansToDegrees, 1 ],
    'degrees'  : [ convertRadiansToDegrees, 1 ],
    'e'        : [ getE, 0 ],
    'exp'      : [ getExp, 1 ],
    'exp10'    : [ getExp10, 1 ],
    'expphi'   : [ getExpPhi, 1 ],
    'fac'      : [ getFactorial, 1 ],
    'fib'      : [ getNthFibonacci, 1 ],
    'floor'    : [ getFloor, 1 ],
    'gamma'    : [ getGamma, 1 ],
    'harm'     : [ getHarmonic, 1 ],
    'harmonic' : [ getHarmonic, 1 ],
    'hex'      : [ getNthHexagonalNumber, 1 ],
    'hyperfac' : [ getHyperfactorial, 1 ],
    'hypot'    : [ getHypotenuse, 2 ],
    'itoi'     : [ getIToTheIPower, 0 ],
    'lgamma'   : [ getLGamma, 1 ],
    'log'      : [ getLog, 1 ],
    'log10'    : [ getLog10, 1 ],
    'logxy'    : [ getLogXY, 2 ],
    'mean'     : [ getMean, 2 ],      # this one eats the whole stack
    'mod'      : [ getModulo, 2 ],
    'modulo'   : [ getModulo, 2 ],
    'mult'     : [ multiplyAll, 2 ],  # this one eats the whole stack
    'neg'      : [ getNegative, 1 ],
    'pent'     : [ getNthPentagonalNumber, 1 ],
    'phi'      : [ getPhi, 0 ],
    'pi'       : [ getPi, 0 ],
    'rad'      : [ convertDegreesToRadians, 1 ],
    'radians'  : [ convertDegreesToRadians, 1 ],
    'rand'     : [ getRandom, 0 ],
    'random'   : [ getRandom, 0 ],
    'sin'      : [ getSine, 1 ],
    'sine'     : [ getSine, 1 ],
    'sqr'      : [ getSquare, 1 ],
    'sqrt'     : [ getSquareRoot, 1 ],
    'sqtri'    : [ getNthSquareTriangularNumber, 1 ],
    'sum'      : [ sum, 2 ],          # this one eats the whole stack
    'superfac' : [ getSuperfactorial, 1 ],
    'tan'      : [ getTangent, 1 ],
    'tangent'  : [ getTangent, 1 ],
    'tet'      : [ getNthTetrahedralNumber, 1 ],
    'tetra'    : [ getNthTetrahedralNumber, 1 ],
    'tri'      : [ getNthTriangularNumber, 1 ],
    '^'        : [ exponentiate, 2 ],
#    'antitet'  : [ getAntiTetrahedralNumber, 1 ],
#    'isprime'  : [ isPrime, 1 ],
#    'powmod'   : [ getPowMod, 3 ],
}


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  parse out regular decimal, hexadecimal, octal or binary input values,
#//  integers only
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
    if term == '0':
        return mpf( 0 )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if '.' in term:
        if inputRadix == 10:
            return mpf( term )

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

    # check for hex, then binary, then octal
    if not ignoreSpecial and mantissa == '':
        if integer[ 0 ] == '0':
            if integer[ 1 ] in 'Xx':
                return mpf( int( integer, 16 ) )
            elif integer[ -1 ] in 'bB':
                integer = integer[ : -1 ]
                return mpf( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpf( int( integer, 8 ) )
        elif inputRadix == 10:
            result = mpf( integer )
            return mpf( -result if negative else result )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )

    return mpf( -result if negative else result )


#//******************************************************************************
#//
#//  formatOutput
#//
#//******************************************************************************

def formatOutput( output, radix, numerals, comma, decimalGrouping, baseAsDigits ):
    strOutput = str( output )

    if '.' in strOutput:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    strResult = '';

    integer = strOutput[ 1 if negative else 0 : decimal ]

    integerLength = len( integer )

    mantissa = strOutput[ decimal + 1 : ]

    if mantissa != '' and mantissa.find( 'e' ) == -1:
        mantissa = mantissa.rstrip( '0' )

    if radix == phiBase:
        integer, mantissa = convertToPhiBase( mpf( output ) )
    elif radix != 10 or numerals != defaultNumerals:
        integer = str( convertToBaseN( mpf( integer ), radix, baseAsDigits, numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpf( '.' + mantissa ), radix,
                            int( ( mp.dps - integerLength ) / math.log10( radix ) ),
                            baseAsDigits ) )

    if comma:
        firstComma = len( integer ) % 3
        integerResult = integer[ : firstComma ]

        for i in range( firstComma, len( integer ), 3 ):
            if integerResult != '':
                integerResult += ','

            integerResult += integer[ i : i + 3 ]
    else:
        integerResult = integer

    if decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( mantissa ), decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += ' '

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

    return result


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global numerals

    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + RPN_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE,
                                      epilog=
'''
Arguments are interpreted as Reverse Polish Notation.

Supported unary operators:
    !, fac
    %, mod, modulo
    abs
    cbrt (cube root)
    ceil
    cube
    deg, degrees (radians to degrees),
    exp
    exp10
    expphi
    floor
    gamma
    hypot
    hyperfac
    lgamma
    log
    log10
    neg
    rad, radians (degrees to radians),
    rand
    sqr
    sqrt
    superfac

Supported unary trigonometric operators:
    sin, sine
    cos, cosine
    tan, tangent
    asin
    acos
    atan

Supported integer sequence unary operators
    fib (nth Fibonacci number)*

    tri (nth triangular number)
    antitri (which triangular number is this)

    pent (nth pentagonal number)
    antipent (which pentagonal number is this)

    hex (nth hexagonal number)
    antihex (which hexagonal number is this)

    sqtri (nth square triangular number)*

    tet, tetra (nth tetrahedronal number)

    * requires sufficient precision for accuracy (see Notes)

Supported binary operators:
    +, -, *, /, ** (power), ^ (power), *** (tetration), // (root), logxy

Supported multi operators (operate on all preceding operands):
    sum, mult, mean

Supported constants:
    e, pi, phi (the Golden Ratio), itoi (i^i)

For integers, rpn understands hexidecimal input of the form '0x....'.
Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B' is
interpreted as binary.  These rules hold regardless of what is specified by -b.

A leading '\\' forces the term to be a number rather than an operator (for use
with higher bases with -b).

Note:  rpn now supports converting fractional results to different bases, but
       input in binary, octal or hex is still restricted to integers.  Use -b
       for inputting fractional values in other bases.

Note:  When converting fractional output to other bases, rpn adjusts the
       precision to the approximate equivalent (that gives a correct answer) for
       the new base since the precision is applicable to base 10.

Note:  tetration forces the second argument to an integer.

Note:  To compute the nth Fibonacci number accurately, rpn sets the precision to
       a level sufficient to guarantee a correct answer.

''',
                                      formatter_class=RawTextHelpFormatter )

    parser.add_argument( 'terms', nargs='+', metavar='term' )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=10,
                         help="specify the radix for input (default: 10)" )
    parser.add_argument( '-c', '--comma', action='store_true',
                         help="add commas to result, e.g., 1,234,567.0" )
    parser.add_argument( '-d', '--decimal_grouping', type=int, action='store', default=0,
                         help="number decimal places separated into groups (default: 0)" )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals,
                         help="characters set to use as numerals for output" )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision,
                         help="precision, i.e., number of significant digits to use" )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=10,
                         help="output in a different base (2 to 62, or phi)" )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0,
                         help="each digit is a space-delimited base-10 number" )
    parser.add_argument( '-x', '--hex', action='store_true', help="equivalent to '-r 16'" )

    if len( sys.argv ) == 1:
        parser.print_help( )
        return

    args = parser.parse_args( )
    mp.dps = args.precision

    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        outputRadix = int( args.output_radix )

    numerals = args.numerals

    if args.hex:
        if outputRadix != 10:
            print( "rpn:  -r and -x can't be used together" )
            return

        outputRadix = 16

    if args.input_radix == 'phi':
        intputRadix = phiBase
    elif args.output_radix == 'fib':
        inputRadix = fibBase
    else:
        inputRadix = int( args.input_radix )

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

    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( "rpn:  output radix greater than 1" )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and ( outputRadix < 2 or outputRadix > 62 ) ):
            print( "rpn:  output radix must be from 2 to 62" )
            return

    if baseAsDigits and ( args.comma or args.decimal_grouping > 0 ):
        print( "rpn:  -c and -d can't be used with -R" )
        return

    index = 1                 # only used for error messages
    valueList = list( )

    # start parsing terms and populating the evaluation stack
    for term in args.terms:
        argType = expressions

        if term in expressions:
            argsNeeded = expressions[ term ][ 1 ]

            if len( valueList ) < argsNeeded:
                print( "rpn: error in arg " + format( index ) + ": operator " + term + " requires " +
                       format( argsNeeded ) + " argument", end='' )

                if argsNeeded > 1:
                    print( "s" )
                else:
                    print( "" )
                break

            try:
                expressions[ term ][ 0 ]( valueList )   # evaluate the expression
            except KeyboardInterrupt as error:
                print( "rpn:  keyboard interrupt" )
                break
            except OverflowError as error:
                print( "rpn:  error in arg " + format( index ) + " ('" + term + "'): {0}".format( error ) )
                break
            except Overflow as error:
                print( "rpn:  decimal overflow error" )
                break
        else:
            try:
                valueList.append( parseInputValue( term, inputRadix ) )
            except Exception as error:
                print( "rpn: error in arg " + format( index ) + ": {0}".format( error ) )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1:
            print( "rpn: unexpected end of input" )
        else:
            result = nstr( valueList.pop( ), mp.dps )
            print( formatOutput( result, outputRadix, numerals, args.comma, args.decimal_grouping, baseAsDigits ) )



#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

