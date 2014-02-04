#!/usr/bin/env python

import argparse
from argparse import RawTextHelpFormatter
import math
import sys
from decimal import *


#//**********************************************************************
#//
#//  constants
#//
#//**********************************************************************

RPN_VERSION = "2.4.0"
COPYRIGHT_MESSAGE = "copyright 2013 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 12


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//  http://code.activestate.com/recipes/65212/
#//
#//******************************************************************************

def convertToBaseN( num, base, numerals="0123456789abcdefghijklmnopqrstuvwxyz" ):
    """
    Convert any int to base/radix 2-36 string. Special numerals can be used
    to convert to any base or radix you need. This function is essentially
    an inverse int(s, base).

    For example:
    >>> baseN(-13, 4)
    '-31'
    >>> baseN(91321, 2)
    '10110010010111001'
    >>> baseN(791321, 36)
    'gyl5'
    >>> baseN(91321, 2, 'ab')
    'babbaabaababbbaab'
    """
    if num == 0:
        return "0"

    if num < 0:
        return '-' + convertToBaseN( ( -1 ) * num, base, numerals )

    if not ( 2 <= base <= len( numerals ) ):
        raise ValueError( 'Base must be between 2-%d' % len( numerals ) )

    left_digits = num // base

    if left_digits == 0:
        return numerals[ int( num ) % base ]
    else:
        return convertToBaseN( left_digits, base, numerals ) + numerals[ int( num ) % base  ]


#//**********************************************************************
#//
#//  decimal_log
#//
#//  http://www.programmish.com/?p=25
#//
#//**********************************************************************

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


#//**********************************************************************
#//
#//  getPI
#//
#//**********************************************************************

def getPI( valueList ):
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


#//**********************************************************************
#//
#//  getE
#//
#//**********************************************************************

def getE( valueList ):
    valueList.append( Decimal( 1 ) )
    takeExp( valueList )


#//**********************************************************************
#//
#//  add
#//
#//**********************************************************************

def add( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) + value )


#//**********************************************************************
#//
#//  subtract
#//
#//**********************************************************************

def subtract( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) - value )


#//**********************************************************************
#//
#//  multiply
#//
#//**********************************************************************

def multiply( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) * value )


#//**********************************************************************
#//
#//  divide
#//
#//**********************************************************************

def divide( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) / value )


#//**********************************************************************
#//
#//  exponentiate
#//
#//**********************************************************************

def exponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( Decimal( valueList.pop( ) ** value ) )


#//**********************************************************************
#//
#//  antiexponentiate
#//
#//**********************************************************************

def antiexponentiate( valueList ):
    value = valueList.pop( )
    valueList.append( valueList.pop( ) ** ( Decimal( 1 ) / value ) )


#//**********************************************************************
#//
#//  takeLogXY
#//
#//**********************************************************************

def takeLogXY( valueList ):
    value = valueList.pop( )
    valueList.append( decimal_log( valueList.pop( ), value ) )


#//**********************************************************************
#//
#//  takeFactorial
#//
#//**********************************************************************

def takeFactorial( valueList ):
    valueList.append( math.factorial( valueList.pop( ) ) )


#//**********************************************************************
#//
#//  takeLog
#//
#//**********************************************************************

def takeLog( valueList ):
    getE( valueList )
    value = valueList.pop( )
    valueList.append( decimal_log( valueList.pop( ), value ) )


#//**********************************************************************
#//
#//  takeLog10
#//
#//**********************************************************************

def takeLog10( valueList ):
    valueList.append( decimal_log( valueList.pop( ) ) )


#//**********************************************************************
#//
#//  takeExp
#//
#//**********************************************************************

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


#//**********************************************************************
#//
#//  takeExp10
#//
#//**********************************************************************

def takeExp10( valueList ):
    valueList.append( Decimal( 10 ) ** valueList.pop( ) )


#//**********************************************************************
#//
#//  expressions
#//
#//  Function names and number of args needed
#//
#//**********************************************************************

expressions = {
    'pi' : [ getPI, 0 ],
    'e'  : [ getE, 0 ],
    '+'  : [ add, 2 ],
    '-'  : [ subtract, 2 ],
    '*'  : [ multiply, 2 ],
    '/'  : [ divide, 2 ],
    '**' : [ exponentiate, 2 ],
    '//' : [ antiexponentiate, 2 ],
    'logxy' : [ takeLogXY, 2 ],
    '!'     : [ takeFactorial, 1 ],
    'log'   : [ takeLog, 1 ],
    'log10' : [ takeLog10, 1 ],
    'exp'   : [ takeExp, 1 ],
    'exp10' : [ takeExp10, 1 ],
}

#//**********************************************************************
#//
#//  main
#//
#//**********************************************************************

def main( ):
    parser = argparse.ArgumentParser( prog='rpn', description='rpn - ' + RPN_VERSION +
                                      ' - ' + COPYRIGHT_MESSAGE,
                                       epilog="Arguments are interpreted as Reverse Polish Notation.\n\n" +
                                       "Supported binary operators: +, -, *, /, ** (power), // (root), logxy\n" +
                                       "Supported unary operators: !, log, log10, exp, exp10\n\n" +
                                       "Note:  Unary operators are also postfix.\n\n" +
                                       "Note:  rpn supports arbitrary precision using Decimal( ), however the following operators\n" +
                                       "       do not always provide arbitrary precision: **, //, exp, exp10." +
                                       "Note:  rpn understands hexidecimal input of the form '0x....'",
                                       formatter_class=RawTextHelpFormatter )

    parser.add_argument( 'terms', nargs='+', metavar='term' )
    parser.add_argument( '-x', '--hex', action='store_true', help="equivalent to '-r 16'" )
    parser.add_argument( '-r', '--output_radix', type=int, action='store', default=10, help="output in a different base (drops fractional part of the result)" )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision, help="precision, i.e., number of significant digits to use" )
    parser.add_argument( '-c', '--comma', action='store_true', help="add commas to result, e.g., 1,234,567.0 (cannot be used with -r or -x)" )

    if len( sys.argv ) == 1:
        parser.print_help( )
        return

    args = parser.parse_args( )
    getcontext( ).prec = args.precision

    if args.hex:
        outputRadix = 16
    else:
        outputRadix = args.output_radix

    if outputRadix < 2 or outputRadix > 36:
        print( "rpn only supports output radix between 2 and 36" )
        return

    if outputRadix != 10 and args.comma:
        print( "-c cannot currently be used with -r or -x" )
        return

    index = 1                 # only used for error messages
    valueList = list( )

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
                expressions[ term ][ 0 ]( valueList )
            except OverflowError:
                print( "rpn: error in arg " + format( index ) + " ('" + term + "'): overflow error" )
                break
        else:
            try:
                value = Decimal( int( term, 0 ) )

                valueList.append( value )
            except:
                print( "rpn: error parsing arg " + format( index ) + " ('" + term + "')" )
                break

        index = index + 1
    else:
        if len( valueList ) > 1:
            print( "rpn: unexpected end of input" )
        else:
            if ( args.comma ):
                formatString = '{:<' + str( args.precision ) + ',}'
                if outputRadix == 10:
                    print( formatString.format( valueList.pop( ) ).strip( ) )
                else:
                    print( formatString.format( convertToBaseN( valueList.pop( ), outputRadix ) ).strip( ) )
            else:
                if outputRadix == 10:
                    print( valueList.pop( ) )
                else:
                    print( convertToBaseN( valueList.pop( ), outputRadix ) )



#//**********************************************************************
#//
#//  __main__
#//
#//**********************************************************************

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
#
