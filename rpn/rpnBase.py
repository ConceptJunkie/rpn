#!/usr/bin/env python

#*******************************************************************************
#
#  rpnBase.py
#
#  rpnChilada base conversion functions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#*******************************************************************************

import gmpy2

from mpmath import fdiv, floor, fmod, fmul, fneg, fsub, mpmathify, power

from rpn.rpnUtils import twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, IntValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  convertToBaseN
#
#******************************************************************************

def convertToBaseN( value, base, outputBaseDigits=False, numerals=g.defaultNumerals ):
    '''
    This handles any integer base as long as there is a big-enough list of
    numerals to use.  In practice this ends up being 0-9, a-z, and A-Z, which
    allows us to support up to base 62.
    '''
    if outputBaseDigits:
        if base < 2:
            raise ValueError( 'base must be greater than 1' )

        if value < 0:
            raise ValueError( '\'get_base_k_digits\' does not support negative numbers.' )
    else:
        if not 2 <= base <= len( numerals ):
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


#******************************************************************************
#
#  convertFractionToBaseN
#
#******************************************************************************

def convertFractionToBaseN( value, base, precision, outputBaseDigits ):
    if outputBaseDigits:
        if base < 2:
            raise ValueError( 'base must be greater than 1' )
    else:
        if not 2 <= base <= len( g.numerals ):
            raise ValueError( 'base must be from 2 to %d' % len( g.numerals ) )

    if value < 0 or value >= 1.0:
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


#******************************************************************************
#
#  getBaseKDigitList
#
#  gmpy2's digits( ) function is way faster, but only works for bases 2 to
#  62.  I need to overhaul convertToBaseN( )... it's way too slow.
#
#******************************************************************************

def getBaseKDigitList( n, base, dropZeroes = False ):
    if 1 < base < 63:
        if n < 0:
            raise ValueError( '\'get_base_k_digits\' does not support negative numbers.' )

        asciiDigits = gmpy2.digits( int( n ), int( base ) )

        digits = [ ]

        ord0 = ord( '0' )
        orda = ord( 'a' )
        ordA = ord( 'A' )

        for i in asciiDigits:
            if '0' <= i <= '9':
                digits.append( ord( i ) - ord0 )
            elif 'a' <= i <= 'z':
                digits.append( ord( i ) - orda + 10 )
            else:
                digits.append( ord( i ) - ordA + 36 )
    else:
        digits = convertToBaseN( n, base, outputBaseDigits=True )

    result = [ ]

    for digit in digits:
        if dropZeroes and digit == 0:
            continue

        result.append( digit )

    return result


def getBaseKDigits( n, k ):
    return getBaseKDigitList( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 2 ) ] )
def getBaseKDigitsOperator( n, k ):
    return getBaseKDigitList( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 2 ) ] )
def getNonzeroBaseKDigitsOperator( n, k ):
    return getBaseKDigitList( n, k, dropZeroes = True )
