#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import math
import sys
from decimal import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = "rpn"
RPN_VERSION = "2.12.1"
PROGRAM_DESCRIPTION = 'RPN command-line calculator'
COPYRIGHT_MESSAGE = "copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 12

degreesPerRadian = Decimal( 180 ) / Decimal( math.pi )

numerals = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//******************************************************************************

def convertToBaseN( num, base, baseAsDigits ):
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

    if num == 0:
        return 0

    if num < 0:
        return '-' + convertToBaseN( ( -1 ) * num, base, baseAsDigits )

    result = ''
    left_digits = num

    while left_digits > 0:
        if baseAsDigits:
            if result != '':
                result = ' ' + result

            result = str( int( left_digits ) % base ) + result
        else:
            result = numerals[ int( left_digits ) % base ] + result

        left_digits //= base

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
#//  decimal_log
#//
#//  http://www.programmish.com/?p=25
#//
#//******************************************************************************

def decimal_log( self, base = 10 ):
    cur_prec = getcontext( ).prec
    getcontext( ).prec += 2

    baseDec = Decimal( 10 )
    retValue = self

    if isinstance( base, Decimal ):
        baseDec = base
    elif isinstance( base, float ):
        baseDec = Decimal( "%f" % ( base ) )
    else:
        baseDec = Decimal( base )

    integer_part = Decimal( 0 )

    while retValue < 1:
        integer_part = integer_part - 1
        retValue = retValue * baseDec

    while retValue >= baseDec:
        integer_part = integer_part + 1
        retValue = retValue / baseDec

    retValue = retValue ** 10
    decimal_frac = Decimal( 0 )
    partial_part = Decimal( 1 )

    while cur_prec > 0:
        partial_part = partial_part / Decimal( 10 )
        digit = Decimal( 0 )

        while retValue >= baseDec:
            digit += 1
            retValue = retValue / baseDec

        decimal_frac = decimal_frac + digit * partial_part
        retValue = retValue ** 10
        cur_prec -= 1

    getcontext( ).prec -= 2

    return integer_part + decimal_frac


#//******************************************************************************
#//
#//  getPi
#//
#//******************************************************************************

def getPi( valueList ):
    """Compute Pi to the current precision.

    >>> print pi()
    3.141592653589793238462643383

    (from http://docs.python.org/lib/decimal-recipes.html)

    """

    getcontext( ).prec += 2   # extra digits for intermediate steps
    three = Decimal( 3 )      # substitute "three=3.0" for regular floats

    last_s, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24

    while s != last_s:
        last_s = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t

    getcontext( ).prec -= 2
    valueList.append( +s )              # unary plus applies the new precision


#//******************************************************************************
#//
#//  getE
#//
#//******************************************************************************

def getE( valueList ):
    valueList.append( Decimal( 1 ) )
    takeExp( valueList )


#//******************************************************************************
#//
#//  calculatePhi
#//
#//******************************************************************************

def calculatePhi( ):
    return ( Decimal( 1 ) + Decimal( 5 ) ** Decimal( 0.5 ) ) / Decimal( 2 )


#//******************************************************************************
#//
#//  getPhi
#//
#//******************************************************************************

def getPhi( valueList ):
    valueList.append( calculatePhi( ) )


#//******************************************************************************
#//
#//  add
#//
#//******************************************************************************

def add( valueList ):
    value = valueList.pop( )
    valueList.append( Decimal( valueList.pop( ) ) + value )


#//******************************************************************************
#//
#//  sum
#//
#//******************************************************************************

def sum( valueList ):
    result = valueList.pop( )

    while valueList:
        value = valueList.pop( )
        result += value

    valueList.append( result )


#//******************************************************************************
#//
#//  takeMean
#//
#//******************************************************************************

def takeMean( valueList ):
    count = 1
    result = valueList.pop( )

    while valueList:
        value = valueList.pop( )
        result += value
        count += 1

    valueList.append( result / count )


#//******************************************************************************
#//
#//  subtract
#//
#//******************************************************************************

def subtract( valueList ):
    value = valueList.pop( )
    valueList.append( Decimal( valueList.pop( ) ) - value )


#//******************************************************************************
#//
#//  multiply
#//
#//******************************************************************************

def multiply( valueList ):
    value = valueList.pop( )
    valueList.append( Decimal( valueList.pop( ) ) * value )


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
    valueList.append( Decimal( valueList.pop( ) ) / value )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) ** value )


#//******************************************************************************
#//
#//  tetrate
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
        result = operand ** result

    valueList.append( result )


#//******************************************************************************
#//
#//  takeSquare
#//
#//******************************************************************************

def takeSquare( valueList ):
    value = valueList.pop( )
    valueList.append( value ** Decimal( 2.0 ) )


#//******************************************************************************
#//
#//  takeSquareRoot
#//
#//******************************************************************************

def takeSquareRoot( valueList ):
    value = valueList.pop( )
    valueList.append( value ** Decimal( 0.5 ) )


#//******************************************************************************
#//
#//  antiexponentiate
#//
#//******************************************************************************

def antiexponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) ** ( Decimal( 1 ) / value ) )


#//******************************************************************************
#//
#//  takeLogXY
#//
#//******************************************************************************

def takeLogXY( valueList ):
    value = valueList.pop( )
    valueList.append( decimal_log( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  takeFactorial
#//
#//******************************************************************************

def takeFactorial( valueList ):
    valueList.append( math.factorial( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeLog
#//
#//******************************************************************************

def takeLog( valueList ):
    getE( valueList )
    value = valueList.pop( )
    valueList.append( decimal_log( valueList.pop( ), value ) )


#//******************************************************************************
#//
#//  takeLog10
#//
#//******************************************************************************

def takeLog10( valueList ):
    valueList.append( decimal_log( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeGamma
#//
#//******************************************************************************

def takeGamma( valueList ):
    valueList.append( math.gamma( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeLGamma
#//
#//******************************************************************************

def takeLGamma( valueList ):
    valueList.append( math.lgamma( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeExp
#//
#//******************************************************************************

def takeExp( valueList ):
    """Return e raised to the power of x.  Result type matches input type.

    (from http://docs.python.org/lib/decimal-recipes.html)

    """

    getcontext( ).prec += 2

    i, last_s, s, fact, num = 0, 0, 1, 1, 1

    x = valueList.pop( )

    while s != last_s:
        last_s = s
        i += 1
        fact *= i
        num *= x
        s += num / fact

    getcontext( ).prec -= 2
    valueList.append( +s )        # unary plus applies the new precision


#//******************************************************************************
#//
#//  takeExp10
#//
#//******************************************************************************

def takeExp10( valueList ):
    valueList.append( Decimal( 10 ) ** Decimal( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeExpPhi
#//
#//******************************************************************************

def takeExpPhi( valueList ):
    valueList.append( calculatePhi( ) ** Decimal( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  Decimal trig functions
#//
#//  http://code.activestate.com/recipes/523018-sin-cos-tan-for-decimal/
#//
#//******************************************************************************

def gen_den( ):
    d = 1
    f = 1

    while ( 1 ):
        yield f
        d = d + 1
        f = f * d

    return


def gen_num( x ):
    n = x

    while ( True ):
        yield n
        n *= x

    return


def gen_sign( ):
    while ( True ):
        yield 1
        yield -1
        yield -1
        yield 1

    return


def sincos( x ):
    x = divmod( x, Decimal( 2.0 ) * Decimal( math.pi ) )[ 1 ]
    den = gen_den( )
    num = gen_num( x )
    sign = gen_sign( )

    s = 0
    c = 1
    i = 1

    done_s = False
    done_c = False

    while not done_s and not done_c:
        new_s = s + next( sign ) * next( num ) / next( den )
        new_c = c + next( sign ) * next( num ) / next( den )

        if ( new_c - c == 0 ):
            done_c = True

        if ( new_s - s == 0 ):
            done_s = True

        c = new_c
        s = new_s
        i = i + 2
    return ( s, c )


def dec_sin( x ):
    ( s, c ) = sincos( x )
    return s


def dec_cos( x ):
    ( s, c ) = sincos( x )
    return c


def dec_tan( x ):
    ( s, c ) = sincos( x )
    return s / c


#//******************************************************************************
#//
#//  takeSin
#//
#//******************************************************************************

def takeSin( valueList ):
    valueList.append( dec_sin( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeCos
#//
#//******************************************************************************

def takeCos( valueList ):
    valueList.append( dec_cos( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  takeTan
#//
#//******************************************************************************

def takeTan( valueList ):
    valueList.append( dec_tan( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  convertRadiansToDegrees
#//
#//******************************************************************************

def convertRadiansToDegrees( valueList ):
    valueList.append( valueList.pop( ) * degreesPerRadian )


#//******************************************************************************
#//
#//  convertDegreesToRadians
#//
#//******************************************************************************

def convertDegreesToRadians( valueList ):
    valueList.append( valueList.pop( ) / degreesPerRadian )


#//******************************************************************************
#//
#//  takePowMod
#//
#//******************************************************************************

def takePowMod( valueList ):
    modulo = valueList.pop( )
    exponent = valueList.pop( )
    base = valueList.pop( )

    valueList.append( pow( base, exponent, modulo ) )


#//******************************************************************************
#//
#//  getNthFibonacci
#//
#//******************************************************************************

def getNthFibonacci( valueList ):
    n = valueList.pop( )
    sqrt5 = Decimal( 5 ) ** Decimal( 0.5 )
    valueList.append( int( ( pow( 1 + sqrt5, n ) - pow( 1 - sqrt5, n ) ) / ( pow( 2, n ) * sqrt5 ) ) )


#//******************************************************************************
#//
#//  getNthTriangularNumber
#//
#//******************************************************************************

def getNthTriangularNumber( valueList ):
    n = valueList.pop( )
    valueList.append( ( n * ( n + 1 ) ) / 2 )


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
#//  getNthHexagonalNumber
#//
#//******************************************************************************

def getNthHexagonalNumber( valueList ):
    n = valueList.pop( )
    valueList.append( ( 2 * n * n ) - n )


#//******************************************************************************
#//
#//  getNthSquareTriangularNumber
#//
#//******************************************************************************

def getNthSquareTriangularNumber( valueList ):
    n = valueList.pop( )
    sqrt2 = Decimal( 2 ) ** Decimal( 0.5 )

    valueList.append( math.ceil( ( ( pow( 1 + sqrt2, 2 * n ) - pow( 1 - sqrt2, 2 * n ) ) / ( 4 * sqrt2 ) ) ** 2 ) )



#//******************************************************************************
#//
#//  removeExponent
#//
#//  from http://docs.python.org/2/library/decimal.html
#//
#//******************************************************************************

def removeExponent( d ):
    '''Remove exponent and trailing zeros.

    >>> remove_exponent(Decimal('5E+3'))
    Decimal('5000')

    '''
    return d.quantize( Decimal( 1 ) ) if d == d.to_integral( ) else d.normalize( )


#//******************************************************************************
#//
#//  expressions
#//
#//  Function names and number of args needed
#//
#//******************************************************************************

expressions = {
    'pi'     : [ getPi, 0 ],
    'e'      : [ getE, 0 ],
    'phi'    : [ getPhi, 0 ],
    '+'      : [ add, 2 ],
    '-'      : [ subtract, 2 ],
    '*'      : [ multiply, 2 ],
    '/'      : [ divide, 2 ],
    '**'     : [ exponentiate, 2 ],
    '***'    : [ tetrate, 2 ],
    '//'     : [ antiexponentiate, 2 ],
    'logxy'  : [ takeLogXY, 2 ],
    '!'      : [ takeFactorial, 1 ],
    'log'    : [ takeLog, 1 ],
    'log10'  : [ takeLog10, 1 ],
    'exp'    : [ takeExp, 1 ],
    'exp10'  : [ takeExp10, 1 ],
    'expphi' : [ takeExpPhi, 1 ],
    'sin'    : [ takeSin, 1 ],
    'cos'    : [ takeCos, 1 ],
    'tan'    : [ takeTan, 1 ],
    'gamma'  : [ takeGamma, 1 ],
    'lgamma' : [ takeLGamma, 1 ],
    'deg'    : [ convertRadiansToDegrees, 1 ],
    'rad'    : [ convertDegreesToRadians, 1 ],
    'sqr'    : [ takeSquare, 1 ],
    'sqrt'   : [ takeSquareRoot, 1 ],
    'powmod' : [ takePowMod, 3 ],
    'fib'    : [ getNthFibonacci, 1 ],
    'tri'    : [ getNthTriangularNumber, 1 ],
    'pent'   : [ getNthPentagonalNumber, 1 ],
    'hex'    : [ getNthHexagonalNumber, 1 ],
    'sqtri'  : [ getNthSquareTriangularNumber, 1 ],
    'sum'    : [ sum, 2 ],          # this one eats the whole stack
    'mult'   : [ multiplyAll, 2 ],  # this one eats the whole stack
    'mean'   : [ takeMean, 2 ]      # this one eats the whole stack
}


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  parse out regular decimal, hexadecimal, octal or binary input values,
#//  integers only
#//
#//******************************************************************************

def parseInputValue( term ):
    if term == '0':
        return Decimal( 0 )

    if '.' in term:
        return Decimal( term )

    # parse out the leading negative or positive sign
    if term[ 0 ] == '-':
        actual = term[ 1: ]
        negative = True
    elif term[ 0 ] == '+':
        actual = term[ 1: ]
        negative = False
    else:
        actual = term
        negative = False

    # check for hex, then binary, then octal
    if actual[ 0 ] == '0':
        if actual[ 1 ] in 'Xx':
            return Decimal( int( term, 16 ) )
        elif actual[ -1 ] in 'bB':
            actual = actual[ :-1 ]
            return Decimal( int( actual, 2 ) * ( -1 if negative else 1 ) )
        else:
            actual = actual[ 1: ]

            return Decimal( int( actual, 8 ) )

    # otherwise, assume base 10
    return Decimal( int( term, 0 ) )


#//******************************************************************************
#//
#//  formatOutput
#//
#//******************************************************************************

def formatOutput( output, radix, comma, decimalGrouping, baseAsDigits ):
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

    if radix != 10:
        integer = str( convertToBaseN( Decimal( integer ), radix, baseAsDigits ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( Decimal( '.' + mantissa ), radix,
                            int( ( getcontext( ).prec - integerLength ) / math.log10( radix ) ),
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
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + RPN_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE,
                                      epilog=
'''
Arguments are interpreted as Reverse Polish Notation.

Supported unary operators:
    !, cos, deg (radians to degrees), exp, exp10, expphi, gamma, lgamma, log,
    log10, rad (degrees to radians), sin, sqr, sqrt, tan

Supported integer sequence unary operators
    fib (nth Fibonacci number)*
    tri (nth triangular number)
    pent (nth pentagonal number)
    hex (nth hexagonal number)
    sqtri (nth square triangular number)*

    * requires sufficient precision for accuracy (see Notes)

Supported binary operators:
    +, -, *, /, ** (power), *** (tetration), // (root), logxy

Supported ternary operators:
    powmod ( x ^ y % z )

Supported multi operators (operate on all preceding operands):
    sum, mult, mean

Supported constants:
    e, pi, phi

rpn supports arbitrary precision using Decimal( ), however the following
operators do not always provide arbitrary precision:
    **, //, exp, exp10, gamma, lgamma

For integers, rpn understands hexidecimal input of the form '0x....'.
Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B' is
interpreted as binary.

Note:  rpn now supports converting fractional results to different bases, but
       input in binary, octal or hex is still restricted to integers

Note:  tetration forces the second argument to an integer.

Note:  To compute the nth Fibonacci number accurately, set the precision to
       about 12 more than the number of digits in the result.

       The sqtri operator needs a similar precision to get the correct answer.

       I'd like to add logic to do this automatically.

''',
                                      formatter_class=RawTextHelpFormatter )

    parser.add_argument( 'terms', nargs='+', metavar='term' )
    parser.add_argument( '-x', '--hex', action='store_true', help="equivalent to '-r 16'" )
    parser.add_argument( '-r', '--output_radix', type=int, action='store', default=10,
                         help="output in a different base (2 to 62)" )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0,
                         help="each digit is a space-delimited base-10 number" )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision,
                         help="precision, i.e., number of significant digits to use" )
    parser.add_argument( '-c', '--comma', action='store_true',
                         help="add commas to result, e.g., 1,234,567.0" )
    parser.add_argument( '-d', '--decimal_grouping', type=int, action='store', default=0,
                         help="number decimal places separated into groups (default: 0)" )

    if len( sys.argv ) == 1:
        parser.print_help( )
        return

    args = parser.parse_args( )
    getcontext( ).prec = args.precision

    if args.hex:
        outputRadix = 16
    else:
        outputRadix = args.output_radix

    if args.output_radix_numerals > 0:
        if args.output_radix != 10:
            print( "rpn:  -r and -R can't be used together" )
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
        if ( outputRadix < 2 or outputRadix > 62 ):
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
                valueList.append( parseInputValue( term ) )
            except Exception as error:
                print( "rpn: error in arg " + format( index ) + ": {0}".format( error ) )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1:
            print( "rpn: unexpected end of input" )
        else:
            result = removeExponent( Decimal( valueList.pop( ) ) )
            print( formatOutput( result, outputRadix, args.comma, args.decimal_grouping, baseAsDigits ) )



#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )


# http://www.programmish.com/?p=24
#
# def nth_root(num, n, digits):
#     getcontext().prec = digits
#     a = Decimal(num)
#     oneOverN = 1 / Decimal(n)
#     nMinusOne = Decimal(n) - 1
#     curVal = Decimal(num) / (Decimal(n) ** 2)
#     if curVal <= Decimal("1.0"):
#         curVal = Decimal("1.1")
#     lastVal = 0
#     while lastVal != curVal:
#         lastVal = curVal
#         curVal = oneOverN * ( (nMinusOne * curVal) + (a / (curVal ** nMinusOne)))
#     return curVal
#

