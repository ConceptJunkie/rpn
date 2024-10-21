#!/usr/bin/env python

#******************************************************************************
#
#  rpnLexicographic.py
#
#  rpnChilada lexicography operators
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import itertools
import random
import string
import types

from mpmath import arange, fabs, fadd, ceil, floor, fmod, fmul, fneg, fprod, fsub, fsum, log10, \
                   mp, mpf, mpmathify, nint, power

from rpn.math.rpnBase import convertToBaseN, getBaseKDigits
from rpn.math.rpnFactor import getFactors
from rpn.math.rpnMath import isDivisible, getPowMod
from rpn.math.rpnPrimeUtils import isPrime

from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnPersistence import cachedFunction
from rpn.util.rpnSettings import setAccuracy
from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, getMPFIntegerAsString, \
                         listArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, IntValidator, ListValidator, RealValidator


#******************************************************************************
#
#  splitNumberByDigits
#
#  This splits the number into 2 numbers by splitting off half the digits
#  for the first and the rest of the digits for the second.  If there is an
#  odd number of digits then the extra digit goes to the second number.
#
#******************************************************************************

def splitNumberByDigits( n ):
    n = getMPFIntegerAsString( n )

    split = len( n ) // 2

    return mpmathify( n[ : split ] ), mpmathify( n[ split : ] )


#******************************************************************************
#
#  getDigitList
#
#******************************************************************************

def getDigitList( n, dropZeroes=False ):
    result = [ ]

    for c in getMPFIntegerAsString( n ):
        if dropZeroes and c == '0':
            continue

        result.append( int( c ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getDigitsOperator( n ):
    return getDigitList( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getNonzeroDigitsOperator( n ):
    return getDigitList( n, dropZeroes=True )


#******************************************************************************
#
#  getDecimalDigitListOperator
#
#******************************************************************************

def getDecimalDigitList( n, k ):
    result = [ ]

    setAccuracy( k )

    digits = floor( log10( n ) )

    if digits < 0:
        for _ in arange( fsub( fabs( digits ), 1 ) ):
            result.append( 0 )

        k = fsub( k, fsub( fabs( digits ), 1 ) )

    value = fmul( n, power( 10, fsub( k, fadd( digits, 1 ) ) ) )

    for c in getMPFIntegerAsString( floor( value ) ):
        result.append( int( c ) )

    return result


@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( ), IntValidator( 1 ) ] )
def getDecimalDigitsOperator( n, k ):
    return getDecimalDigitList( n, k )


#******************************************************************************
#
#  getRightDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 1 ) ] )
def getRightDigitsOperator( n, k ):
    return fmod( n, pow( 10, k ) )


#******************************************************************************
#
#  getLeftDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 1 ) ] )
def getLeftDigitsOperator( n, k ):
    return combineDigits( getDigitList( n )[ : int( k ) ] )


#******************************************************************************
#
#  isBaseKPandigitalOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 2 ) ] )
def isBaseKPandigitalOperator( n, base ):
    digits = convertToBaseN( n, base, outputBaseDigits=True )

    for i in arange( min( int( base ), len( digits ) ) ):
        try:
            digits.index( i )
        except ValueError:
            return 0

    return 1


#******************************************************************************
#
#  sumDigitsOperator
#
#******************************************************************************

def sumDigits( n ):
    result = 0

    for c in getMPFIntegerAsString( n ):
        result = fadd( result, int( c ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def sumDigitsOperator( n ):
    return sumDigits( n )


#******************************************************************************
#
#  multiplyDigitListOperator
#
#******************************************************************************

def multiplyDigitList( n, exponent = 1, dropZeroes = False ):
    if exponent < 1:
        raise ValueError( 'multiplyDigitList( ) expects a positive integer for \'exponent\'' )

    if exponent == 1:
        return fprod( getDigitList( n, dropZeroes ) )

    return fprod( [ power( i, exponent ) for i in getDigitList( n, dropZeroes ) ] )


def multiplyDigits( n ):
    return multiplyDigitList( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def multiplyDigitsOperator( n ):
    return multiplyDigitList( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 0 ) ] )
def multiplyDigitPowersOperator( n, k ):
    return multiplyDigitList( n, k )


def multiplyNonzeroDigits( n ):
    return multiplyDigitList( n, dropZeroes = True )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def multiplyNonzeroDigitsOperator( n ):
    return multiplyDigitList( n, dropZeroes = True )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 0 ) ] )
def multiplyNonzeroDigitPowersOperator( n, k ):
    return multiplyDigitList( n, k, dropZeroes = True )


#******************************************************************************
#
#  appendDigits
#
#******************************************************************************

def appendDigits( n, digits, digitCount ):
    if ( n ) < 0:
        return nint( fsub( fmul( floor( n ), power( 10, digitCount ) ), digits ) )

    return nint( fadd( fmul( floor( n ), power( 10, digitCount ) ), digits ) )


#******************************************************************************
#
#  addDigitsOperator
#
#******************************************************************************

def addDigits( n, k ):
    digits = int( k )

    if digits == 0:
        digitCount = 1
    else:
        digitCount = int( fadd( floor( log10( k ) ), 1 ) )

    return appendDigits( n, digits, digitCount )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 0 ) ] )
def addDigitsOperator( n, k ):
    return addDigits( n, k )


#******************************************************************************
#
#  combineDigits
#
#******************************************************************************

def combineDigits( n ):
    result = 0

    listResult = False

    for i in n:
        if isinstance( i, ( list, types.GeneratorType, RPNGenerator ) ) and result == 0:
            listResult = True
            result = combineDigits( i )
        elif listResult:
            if not isinstance( result, list ):
                result = [ result ]

            result.append( combineDigits( i ) )
        else:
            result = addDigits( result, i )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def combineDigitsOperator( n ):
    return combineDigits( n )


#******************************************************************************
#
#  replaceDigitsOperator
#
#******************************************************************************

@argValidator( [ IntValidator( ), IntValidator( 0 ), IntValidator( 0 ) ] )
def replaceDigitsOperator( n, source, replace ):
    n = getMPFIntegerAsString( n )

    if source < 0:
        raise ValueError( 'source value must be a positive integer' )

    if replace < 0:
        raise ValueError( 'replace value must be a positive integer' )

    return mpmathify( n.replace( str( int( source ) ), str( int( replace ) ) ) )


#******************************************************************************
#
#  duplicateDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 0 ) ] )
def duplicateDigitsOperator( n, k ):
    return appendDigits( n, fmod( n, power( 10, nint( floor( k ) ) ) ), k )


#******************************************************************************
#
#  duplicateNumberOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 0 ) ] )
def duplicateNumberOperator( n, k ):
    if k == 0:
        return 0

    return mpmathify( getMPFIntegerAsString( n ) * int( k ) )


#******************************************************************************
#
#  reverseDigitsOperator
#
#******************************************************************************

def reverseDigits( n ):
    return mpmathify( getMPFIntegerAsString( n )[ : : -1 ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def reverseDigitsOperator( n ):
    return reverseDigits( n )


#******************************************************************************
#
#  isPalindromeOperator
#
#******************************************************************************

def isPalindrome( n ):
    result = getMPFIntegerAsString( n )

    length = len( result )

    for i in range( 0, length // 2 ):
        if result[ i ] != result[ -( i + 1 ) ]:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPalindromeOperator( n ):
    return isPalindrome( n )


#******************************************************************************
#
#  isPandigitalOperator
#
#******************************************************************************

def isPandigital( n ):
    n = getMPFIntegerAsString( n )

    length = len( n )

    if length < 10:
        return 0

    digitsToCheck = string.digits

    for c in digitsToCheck:
        if c not in n:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPandigitalOperator( n ):
    return isPandigital( n )


#******************************************************************************
#
#  containsDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def containsDigitsOperator( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in k:
        if c not in n:
            return 0

    return 1


#******************************************************************************
#
#  containsAnyDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def containsAnyDigitsOperator( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in k:
        if c in n:
            return 1

    return 0


#******************************************************************************
#
#  containsOnlyDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def containsOnlyDigitsOperator( n, k ):
    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in getMPFIntegerAsString( n ):
        if c not in k:
            return 0

    return 1


#******************************************************************************
#
#  countDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def countDigitsOperator( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        #k = set( [ char for char in getMPFIntegerAsString( k ) ] )
        k = set( getMPFIntegerAsString( k ) )
        #print( k )

    result = 0

    for c in k:
        result += n.count( c )

    return result


#******************************************************************************
#
#  getDigitCountOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getDigitCountOperator( n ):
    if n == 0:
        return 1

    return floor( fadd( log10( fabs( n ) ), 1 ) )


#******************************************************************************
#
#  countDifferentDigitsOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def countDifferentDigitsOperator( n ):
    return len( list( set( getMPFIntegerAsString( n ) ) ) )


#******************************************************************************
#
#  getNthReversalAdditionOperator
#
#  https://en.wikipedia.org/wiki/Lychrel_number
#
#******************************************************************************

def getNthReversalAdditionGenerator( n, k ):
    nextOne = int( n  )
    yield nextOne

    for _ in arange( k ):
        nextOne = fadd( reverseDigits( nextOne ), nextOne )

        yield nextOne

        if isPalindrome( nextOne ):
            break


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def getNthReversalAdditionOperator( n, k ):
    return RPNGenerator( getNthReversalAdditionGenerator( n, k ) )


#******************************************************************************
#
#  findPalindromeOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def findPalindromeOperator( n, k ):
    nextOne = int( n )

    for i in range( int( k ) + 1 ):
        nextOne = reverseDigits( nextOne ) + nextOne

        if isPalindrome( nextOne ):
            return [ i + 1, nextOne ]

    return [ k, 0 ]


#******************************************************************************
#
#  isNarcissisticOperator
#
#******************************************************************************

def isNarcissistic( n ):
    digits = getDigitList( n )
    count = len( digits )

    total = 0

    for digit in digits:
        total = fadd( total, power( digit, count ) )

        if total > n:
            return 0

    return 1 if total == n else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isNarcissisticOperator( n ):
    return isNarcissistic( n )


#******************************************************************************
#
#  isPerfectDigitalInvariantOperator
#
#******************************************************************************

def isPerfectDigitalInvariant( n ):
    digits = getDigitList( n )

    exponent = 1

    oldTotal = 0

    while True:
        total = 0

        for digit in digits:
            total = fadd( total, power( digit, exponent ) )

            if total > n:
                return 0

            if total == n:
                return 1

        if total == oldTotal:
            return 0

        oldTotal = total

        exponent += 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPerfectDigitalInvariantOperator( n ):
    return isPerfectDigitalInvariant( n )


#******************************************************************************
#
#  isBaseKNarcissisticOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def isBaseKNarcissisticOperator( n, k ):
    digits = getBaseKDigits( n, k )

    count = len( digits )

    total = 0

    for digit in digits:
        total = fadd( total, power( digit, count ) )

        if total > n:
            return 0

    return 1 if total == n else 0


#******************************************************************************
#
#  isGeneralizedDudeneyNumberOperator
#
#******************************************************************************

@cachedFunction( 'generalized_dudeney' )
def isGeneralizedDudeneyNumber( base, exponent ):
    '''http://www.jakob.at/steffen/dudeney.html'''
    precision = fadd( fmul( base, exponent ), 2 )
    mp.dps = max( precision, mp.dps )

    n = power( base, exponent )
    return 1 if sumDigits( n ) == base else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def isGeneralizedDudeneyNumberOperator( base, exponent ):
    return isGeneralizedDudeneyNumber( base, exponent )


#******************************************************************************
#
#  isPerfectDigitToDigitInvariantOperator
#
#******************************************************************************

def isPerfectDigitToDigitInvariant( n, k ):
    '''https://en.wikipedia.org/wiki/Perfect_digit-to-digit_invariant'''
    digits = getBaseKDigits( n, k )

    total = 0

    for digit in digits:
        digit = int( digit )

        if digit != 0:
            total = fadd( total, power( digit, digit ) )

        if total > n:
            return 0

    return 1 if total == n else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def isPerfectDigitToDigitInvariantOperator( n, k ):
    return isPerfectDigitToDigitInvariant( n, k )


#******************************************************************************
#
#  isSumProductNumberOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def isSumProductNumberOperator( n, k ):
    '''https://en.wikipedia.org/wiki/Sum-product_number'''
    digits = getBaseKDigits( n, k )
    total = fmul( fsum( digits ), fprod( digits ) )
    return 1 if total == n else 0


#******************************************************************************
#
#  isHarshadNumberOperator
#
#******************************************************************************

def isHarshadNumber( n, k ):
    '''https://en.wikipedia.org/wiki/Harshad_number'''
    digits = getBaseKDigits( n, k )
    return 1 if isDivisible( n, fsum( digits ) ) else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def isHarshadNumberOperator( n, k ):
    return isHarshadNumber( n, k )


#******************************************************************************
#
#  isKaprekarNumberOperator
#
#******************************************************************************

def isKaprekarNumber( n ):
    if n == 1:
        return 1

    if n < 9:
        return 0

    a, b = splitNumberByDigits( power( n, 2 ) )

    return 1 if ( fadd( a, b ) == n ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isKaprekarNumberOperator( n ):
    return isKaprekarNumber( n )


#******************************************************************************
#
#  convertStringsToNumbers
#
#******************************************************************************

def convertStringsToNumbers( values ):
    for i in values:
        yield mpmathify( i )


#******************************************************************************
#
#  buildNumbersOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def buildNumbersOperator( expression ):
    digitLists = parseNumbersExpression( expression )

    if len( digitLists ) == 1:
        return RPNGenerator.createGenerator( convertStringsToNumbers, digitLists )

    return RPNGenerator.createStringProduct( digitLists )


#******************************************************************************
#
#  buildLimitedDigitNumbers
#
#******************************************************************************

def buildLimitedDigitNumbers( digits, minLength, maxLength ):
    if minLength < 1:
        raise ValueError( 'minimum length must be greater than 0' )

    if maxLength < minLength:
        raise ValueError( 'maximum length must be greater than or equal to minimum length' )

    for i in range( minLength, maxLength + 1 ):
        for item in itertools.product( digits, repeat=i ):
            number = ''.join( item )

            yield number


#******************************************************************************
#
#  parseNumbersExpression
#
#  D[D]...
#
#  One or more digit expressions where each digit expression can be:
#      - A single digit, "0" through "9"
#      - "d" - digit (equivalent to "[0-9]"
#      - "[I[I]...]" - any of the individual digit expressions
#      - "[I[I]...:m]" - permutations of any digits I, m digits long
#      - "[I[I]...:n:m]" - permutations of any digits I, from a minimum of n,
#                          up to a maximum of m digits long
#      - "s" - the designation for a "step digit", which can be one greater
#              or one less than the previous digit.  For the purposes of step,
#              0 succeeds 9 and precedes 1.
#
#  A digit expression (I) can be a single digit or a range.  A single digit is
#  anything from "0" through "9".  A digit range looks like: "a-b" where a
#  is a digit that is smaller than b.
#
#******************************************************************************

def parseNumbersExpression( arg ):
    if not isinstance( arg, str ):
        arg = str( arg )

    result = [ ]

    digitRange = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
    oddRange = [ '1', '3', '5', '7', '9' ]
    evenRange = [ '0', '2', '4', '6', '8' ]

    defaultState = 0
    startDigitState = 1
    digitState = 2
    startRangeState = 3
    numberLengthRange1 = 4
    numberLengthRange2 = 5

    state = defaultState

    currentGroup = set( )

    lengthRangeLow = ''
    lengthRangeHigh = ''
    lastDigit = ''

    for char in arg:
        #print( 'state', state, 'ch', ch, 'result', result, 'currentGroup', currentGroup )
        if state == defaultState:
            if char == 'd':
                result.append( digitRange )
            elif char == 'e':
                result.append( evenRange )
            elif char == 'o':
                result.append( oddRange )
            elif char == '[':
                state = digitState
                currentGroup = set( )
            elif '0' <= char <= '9':
                result.append( [ char ] )
            else:
                raise ValueError( f'unexpected character \'{ char }\'' )
        elif state == startDigitState:
            if '0' <= char <= '9':
                currentGroup.add( char )
                state = digitState
                lastDigit = char
            elif char == ']':
                result.append( sorted( list( currentGroup ) ) )
                state = defaultState
            else:
                raise ValueError( f'unexpected character \'{ char }\'' )
        elif state == digitState:
            if '0' <= char <= '9':
                currentGroup.add( char )
                lastDigit = char
            elif char == 'd':
                for digit in digitRange:
                    currentGroup.add( digit )

                lastDigit = ' '
            elif char == 'e':
                for digit in evenRange:
                    currentGroup.add( digit )

                lastDigit = ' '
            elif char == 'o':
                for digit in oddRange:
                    currentGroup.add( digit )

                lastDigit = ' '
            elif char == '-':
                state = startRangeState
            elif char == ':':
                state = numberLengthRange1
            elif char == ']':
                result.append( sorted( list( currentGroup ) ) )
                state = defaultState
        elif state == startRangeState:
            if lastDigit == ' ':
                raise ValueError( 'invalid digit range' )

            if '0' <= char <= '9':
                if char <= lastDigit:
                    raise ValueError( 'invalid digit range' )

                for i in range( int( lastDigit ), int( char ) + 1 ):
                    currentGroup.add( str( i ) )

                state = digitState
        elif state == numberLengthRange1:
            if '0' <= char <= '9':
                lengthRangeHigh += char
            elif char == ':':
                lengthRangeLow = lengthRangeHigh
                lengthRangeHigh = ''
                state = numberLengthRange2
            elif char == ']':
                result.append( buildLimitedDigitNumbers( sorted( list( currentGroup ) ),
                                                         int( lengthRangeHigh ), int( lengthRangeHigh ) ) )
                lengthRangeLow = ''
                lengthRangeHigh = ''
                state = defaultState
            else:
                raise ValueError( f'unexpected character \'{ char }\'' )
        elif state == numberLengthRange2:
            if '0' <= char <= '9':
                lengthRangeHigh += char
            elif char == ']':
                result.append( buildLimitedDigitNumbers( sorted( list( currentGroup ) ),
                                                         int( lengthRangeLow ), int( lengthRangeHigh ) ) )
                lengthRangeLow = ''
                lengthRangeHigh = ''
                state = defaultState
            else:
                raise ValueError( f'unexpected character \'{ char }\'' )

    return result


#******************************************************************************
#
#  hasUniqueDigitsOperator
#
#******************************************************************************

def hasUniqueDigits( n ):
    digits = getDigitList( n )

    existing = set( )

    for digit in digits:
        if digit in existing:
            return 0

        existing.add( digit )

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def hasUniqueDigitsOperator( n ):
    return hasUniqueDigits( n )


#******************************************************************************
#
#  hasDigits
#
#******************************************************************************

#@twoArgFunctionEvaluator( )
#def hasDigits( value, digits ):
#    pass


#******************************************************************************
#
#  isKMorphicOperator
#
#******************************************************************************

def isKMorphic( n, k ):
    '''
    Returns true if n to the k power ends with n.

    This code won't work correctly for integral powers of 10, but they can
    never be morphic anyway, except for 1, which I handle specially.
    '''
    if n == 1:
        return 1

    modulo = power( 10, ceil( log10( n ) ) )
    powmod = getPowMod( n, k, modulo )

    return 1 if ( n == powmod ) else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def isKMorphicOperator( n, k ):
    return isKMorphic( n, k )


def isAutomorphic( n ):
    return isKMorphic( n, 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isAutomorphicOperator( n ):
    return isKMorphic( n, 2 )


def isTrimorphic( n ):
    return isKMorphic( n, 3 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isTrimorphicOperator( n ):
    return isKMorphic( n, 3 )


#******************************************************************************
#
#  getLeftTruncationsOperator
#
#******************************************************************************

def getLeftTruncationsGenerator( n ):
    n = getMPFIntegerAsString( n )

    for i, _ in enumerate( n ):
        yield mpmathify( n[ i : ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getLeftTruncationsOperator( n ):
    return RPNGenerator.createGenerator( getLeftTruncationsGenerator, n )


#******************************************************************************
#
#  getRightTruncationsOperator
#
#******************************************************************************

def getRightTruncationsGenerator( n ):
    result = getMPFIntegerAsString( n )

    for i in range( len( result ), 0, -1 ):
        yield mpmathify( result[ 0 : i ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getRightTruncationsOperator( n ):
    return RPNGenerator.createGenerator( getRightTruncationsGenerator, n )


#******************************************************************************
#
#  getMultiplicativePersistence
#
#******************************************************************************

def getMultiplicativePersistence( n, exponent = 1, dropZeroes = False, persistence = 0 ):
    if exponent == 1 and n < 10:
        return persistence

    if n <= 1:
        return persistence

    return getMultiplicativePersistence( multiplyDigitList( n, exponent, dropZeroes ),
                                         exponent, dropZeroes, persistence + 1 )


def getPersistence( n ):
    return getMultiplicativePersistence( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getPersistenceOperator( n ):
    return getMultiplicativePersistence( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def getKPersistenceOperator( n, k ):
    return getMultiplicativePersistence( n, k )


def getErdosPersistence( n ):
    return getMultiplicativePersistence( n, 1, True )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getErdosPersistenceOperator( n ):
    return getMultiplicativePersistence( n, 1, True )


#******************************************************************************
#
#  showMultiplicativePersistence
#
#******************************************************************************

def showMultiplicativePersistenceGenerator( n, exponent = 1, dropZeroes = False ):
    yield n

    if exponent == 1:
        while n >= 10:
            n = multiplyDigitList( n, exponent, dropZeroes )
            yield n
    else:
        while n > 1:
            n = multiplyDigitList( n, exponent, dropZeroes )
            yield n


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def showPersistenceOperator( n ):
    return RPNGenerator.createGenerator( showMultiplicativePersistenceGenerator, [ n ] )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def showKPersistenceOperator( n, k ):
    return RPNGenerator.createGenerator( showMultiplicativePersistenceGenerator, [ n, k ] )


#******************************************************************************
#
#  showErdosPersistenceGenerator
#
#******************************************************************************

def showErdosPersistenceGenerator( n ):
    yield n

    while n >= 10:
        n = multiplyDigitList( n, 1, True )
        yield n


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def showErdosPersistenceOperator( n ):
    return RPNGenerator.createGenerator( showErdosPersistenceGenerator, [ n ] )


#******************************************************************************
#
#  permuteDigitsOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def permuteDigitsOperator( n ):
    return RPNGenerator.createPermutations( getMPFIntegerAsString( n ) )


#******************************************************************************
#
#  changeDigitsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def changeDigitsOperator( n, k ):
    numbers = '0123456789'
    digits = getMPFIntegerAsString( n )
    digit_count = len( digits )

    if k > digit_count:
        raise ValueError( 'change_digits cannot change more digits than exist' )

    indices_to_change = [ ]

    for _ in arange( k ):
        done = False

        while not done:
            index = random.randrange( digit_count )

            if index not in indices_to_change:
                indices_to_change.append( index )
                done = True

    for index in indices_to_change:
        digit_to_change = digits[ index ]

        done = False

        while not done:
            new_digit = numbers[ random.randrange( 10 ) ]

            if new_digit != digit_to_change:
                done = True

        digits = digits[ : index ] + new_digit + digits[ index + 1 : ]

    return mpmathify( digits )


#******************************************************************************
#
#  isIncreasingOperator
#
#******************************************************************************

def isIncreasing( n ):
    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if n[ i ] < n[ i - 1 ]:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isIncreasingOperator( n ):
    return isIncreasing( n )


#******************************************************************************
#
#  isDecreasingOperator
#
#******************************************************************************

def isDecreasing( n ):
    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if n[ i ] > n[ i - 1 ]:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isDecreasingOperator( n ):
    return isDecreasing( n )


#******************************************************************************
#
#  isBouncyOperator
#
#******************************************************************************

def isBouncy( n ):
    if isIncreasing( n ) == 0 and isDecreasing( n ) == 0:
        return 1

    return 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isBouncyOperator( n ):
    return isBouncy( n )


#******************************************************************************
#
#  rotateDigitsLeftOperator
#
#******************************************************************************

def rotateDigitsLeft( n, k ):
    if k < 0:
        return rotateDigitsRight( n, fneg( k ) )

    n = getMPFIntegerAsString( n )

    if k > len( n ):
        fmod( k, len( n ) )

    rotate = int( k )

    n = n[ rotate : ] + n[ : rotate ]
    return mpmathify( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( ) ] )
def rotateDigitsLeftOperator( n, k ):
    return rotateDigitsLeft( n, k )


#******************************************************************************
#
#  rotateDigitsRightOperator
#
#******************************************************************************

def rotateDigitsRight( n, k ):
    if k < 0:
        return rotateDigitsLeft( n, fneg( k ) )

    n = getMPFIntegerAsString( n )

    if k > len( n ):
        fmod( k, len( n ) )

    rotate = int( k )

    n = n[ -rotate : ] + n[ : -rotate ]
    return mpmathify( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( ) ] )
def rotateDigitsRightOperator( n, k ):
    return rotateDigitsRight( n, k )


#******************************************************************************
#
#  getCyclicPermutations
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getCyclicPermutationsOperator( n ):
    result = [ n ]

    n = getMPFIntegerAsString( n )

    for _ in range( len( n ) - 1 ):
        n = n[ 1 : ] + n[ : 1 ]
        result.append( mpmathify( n ) )

    return result


#******************************************************************************
#
#  isDigitalPermutationOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def isDigitalPermutationOperator( n, k ):
    str1 = getMPFIntegerAsString( n )
    str2 = getMPFIntegerAsString( k )

    if len( str1 ) != len( str2 ):
        return 0

    if sorted( str1 ) != sorted( str2 ):
        return 0

    return 1


#******************************************************************************
#
#  getSquareDigitChainOperator
#
#******************************************************************************

def generateSquareDigitChainGenerator( n ):
    n = int( n )

    chain = [ ]

    if n == 0:
        yield 0
        return

    if n == 1:
        yield 1
        return

    done = False

    while not done:
        digits = getDigitList( n )

        n = 0

        for i in digits:
            n = fadd( n, pow( i, 2 ) )

        if n in chain:
            done = True
        else:
            chain.append( n )

            yield n


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def generateSquareDigitChainOperator( n ):
    return RPNGenerator.createGenerator( generateSquareDigitChainGenerator, [ n ] )


#******************************************************************************
#
#  isStepNumberOperator
#
#******************************************************************************

def isStepNumber( n ):
    if n < 10:
        return 0

    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if abs( int( n[ i ] ) - int( n[ i - 1 ] ) ) != 1:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isStepNumberOperator( n ):
    return isStepNumber( n )


#******************************************************************************
#
#  buildNextStepNumbers
#
#  This method expects a list of digits.
#
#******************************************************************************

def buildNextStepNumbers( n ):
    result = [ ]

    if n[ -1 ] == 0:
        result.append( n + [ 1 ] )
    elif n[ -1 ] == 9:
        result.append( n + [ 8 ] )
    else:
        result.append( n + [ n[ -1 ] - 1 ] )
        result.append( n + [ n[ -1 ] + 1 ] )

    return result


#******************************************************************************
#
#  buildStepNumbersOperator
#
#******************************************************************************

def buildStepNumbersGenerator( maxLength ):
    if maxLength < 2:
        raise ValueError( '\'build_step_numbers\' requires an argument of 2 or greater' )

    stepNumbers = [ ]

    for i in range( 1, 10 ):
        stepNumbers.extend( buildNextStepNumbers( [ i ] ) )

    for i in stepNumbers:
        yield combineDigits( i )

    for i in range( 0, int( maxLength ) - 2 ):
        newStepNumbers = [ ]

        for j in stepNumbers:
            newStepNumbers.extend( buildNextStepNumbers( j ) )

        stepNumbers = newStepNumbers

        for j in stepNumbers:
            yield combineDigits( j )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def buildStepNumbersOperator( n ):
    return RPNGenerator.createGenerator( buildStepNumbersGenerator, [ n ] )


#******************************************************************************
#
#  isSmithNumberOperator
#
#******************************************************************************

@cachedFunction( 'smith' )
def isSmithNumber( n ):
    if isPrime( n ) or n < 2:
        return 0

    sum1 = sumDigits( n )
    sum2 = fsum( [ sumDigits( i ) for i in getFactors( n ) ] )

    return 1 if sum1 == sum2 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isSmithNumberOperator( n ):
    isSmithNumber( n )


#******************************************************************************
#
#  isBaseKSmithNumberOperator
#
#******************************************************************************

@cachedFunction( 'base_k_smith' )
def isBaseKSmithNumber( n, k ):
    if k > 4 and n == 4:
        return 1

    if k > 4 and n < k:
        return 0

    if isPrime( n ) or n < 2:
        return 0

    sum1 = fsum( getBaseKDigits( n, k ) )
    sum2 = fsum( [ fsum( getBaseKDigits( i, k ) ) for i in getFactors( n ) ] )

    return 1 if sum1 == sum2 else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def isBaseKSmithNumberOperator( n, k ):
    return isBaseKSmithNumber( n, k )


#******************************************************************************
#
#  isOrderKSmithNumberOperator
#
#******************************************************************************

@cachedFunction( 'order_k_smith' )
def isOrderKSmithNumber( n, k ):
    if isPrime( n ) or n < 2:
        return 0

    digitList1 = getDigitList( n, dropZeroes=True )
    digitList2 = [ item for sublist in [ getDigitList( m, dropZeroes=True ) for m in getFactors( n ) ]
                   for item in sublist ]

    if sorted( digitList1 ) == sorted( digitList2 ):
        return 0

    sum1 = fsum( [ power( i, k ) for i in getDigitList( n ) ] )
    sum2 = fsum( [ power( j, k ) for j in [ item for sublist in
                                            [ getDigitList( m ) for m in getFactors( n ) ] for item in sublist ] ] )

    return 1 if sum1 == sum2 else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def isOrderKSmithNumberOperator( n, k ):
    isOrderKSmithNumber( n, k )


#  Look and Say from:
#  https://www.rosettacode.org/wiki/Look-and-say_sequence#Python

#>>> from itertools import groupby
#>>> def lookandsay(number):
#    return ''.join( str(len(list(g))) + k
#                for k,g in groupby(number) )
#
#>>> numberstring='1'
#>>> for i in range(10):
#    print numberstring
#    numberstring = lookandsay(numberstring)
#
