#!/usr/bin/env python

#******************************************************************************
#
#  rpnLexicographic.py
#
#  rpnChilada lexicography operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import itertools
import string

from mpmath import arange, fadd, ceil, floor, fmod, fmul, fneg, fprod, fsub, \
                   fsum, log10, mpf, mpmathify, nint, power

import gmpy2

from rpn.rpnBase import convertToBaseN
from rpn.rpnFactor import getFactors
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMath import isDivisible
from rpn.rpnNumberTheory import getPowMod
from rpn.rpnPersistence import cachedFunction
from rpn.rpnPrimeUtils import isPrime
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, validateRealInt, \
                         getMPFIntegerAsString


#******************************************************************************
#
#  splitNumberByDigits
#
#  This splits the number into 2 numbers by splitting off half the digits
#  for the first and the rest of the digits for the second.  If there is an
#  odd number of digits then the extra digit goes to the second number.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def splitNumberByDigits( n ):
    n = getMPFIntegerAsString( n )

    split = len( n ) // 2

    return mpmathify( n[ : split ] ), mpmathify( n[ split : ] )


#******************************************************************************
#
#  getDigitList
#
#******************************************************************************

def getDigitList( n, dropZeroes = False ):
    result = [ ]

    for c in getMPFIntegerAsString( n ):
        if dropZeroes and c == '0':
            continue

        result.append( int( c ) )

    return result


@oneArgFunctionEvaluator( )
def getDigits( n ):
    return getDigitList( n )

@oneArgFunctionEvaluator( )
def getNonzeroDigits( n ):
    return getDigitList( n, dropZeroes = True )


#******************************************************************************
#
#  getRightDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getRightDigits( n, k ):
    return fmod( n, pow( 10, k ) )


#******************************************************************************
#
#  getLeftDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getLeftDigits( n, k ):
    return combineDigits( getDigitList( n )[ : int( k ) ] )


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
                digits.append( ord( i ) - orda )
            else:
                digits.append( ord( i ) - ordA )
    else:
        digits = convertToBaseN( n, base, outputBaseDigits=True )

    result = [ ]

    for digit in digits:
        if dropZeroes and digit == 0:
            continue

        result.append( digit )

    return result


@twoArgFunctionEvaluator( )
def getBaseKDigits( n, k ):
    return getBaseKDigitList( n, k )

@twoArgFunctionEvaluator( )
def getNonzeroBaseKDigits( n, k ):
    return getBaseKDigitList( n, k, dropZeroes = True )


#******************************************************************************
#
#  isBaseKPandigital
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isBaseKPandigital( n, base ):
    digits = convertToBaseN( n, base, outputBaseDigits=True )

    for i in arange( min( int( base ), len( digits ) ) ):
        try:
            digits.index( i )
        except:
            return 0

    return 1


#******************************************************************************
#
#  sumDigits
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def sumDigits( n ):
    result = 0

    for c in getMPFIntegerAsString( n ):
        result = fadd( result, int( c ) )

    return result


#******************************************************************************
#
#  multiplyDigitList
#
#******************************************************************************

def multiplyDigitList( n, exponent = 1, dropZeroes = False ):
    if exponent < 1:
        raise ValueError( 'multiplyDigitList( ) expects a positive integer for \'exponent\'' )

    if exponent == 1:
        return fprod( getDigitList( n, dropZeroes ) )

    return fprod( [ power( i, exponent ) for i in getDigitList( n, dropZeroes ) ] )

@oneArgFunctionEvaluator( )
def multiplyDigits( n ):
    return multiplyDigitList( n )

@twoArgFunctionEvaluator( )
def multiplyDigitPowers( n, k ):
    return multiplyDigitList( n, k )

@oneArgFunctionEvaluator( )
def multiplyNonzeroDigits( n ):
    return multiplyDigitList( n, dropZeroes = True )

@twoArgFunctionEvaluator( )
def multiplyNonzeroDigitPowers( n, k ):
    return multiplyDigitList( n, k, dropZeroes = True )


#******************************************************************************
#
#  appendDigits
#
#******************************************************************************

def appendDigits( n, digits, digitCount ):
    if validateRealInt( n ) < 0:
        return nint( fsub( fmul( floor( n ), power( 10, digitCount ) ), digits ) )
    else:
        return nint( fadd( fmul( floor( n ), power( 10, digitCount ) ), digits ) )


#******************************************************************************
#
#  addDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def addDigits( n, k ):
    if validateRealInt( k ) < 0:
        raise ValueError( "'add_digits' requires a non-negative integer for the second argument" )

    digits = int( k )

    if digits == 0:
        digitCount = 1
    else:
        digitCount = int( fadd( floor( log10( k ) ), 1 ) )

    return appendDigits( n, digits, digitCount )


#******************************************************************************
#
#  combineDigits
#
#******************************************************************************

def combineDigits( n ):
    if isinstance( n, RPNGenerator ):
        return combineDigits( list( n ) )

    result = 0

    listResult = False

    for i in n:
        if isinstance( i, ( list, RPNGenerator ) ) and result == 0:
            listResult = True
            result = [ combineDigits( i ) ]
        elif listResult:
            if not isinstance( result, list ):
                result = [ result ]

            result.append( combineDigits( i ) )
        else:
            result = addDigits( result, validateRealInt( i ) )

    return result


#******************************************************************************
#
#  replaceDigits
#
#******************************************************************************

def replaceDigits( n, source, replace ):
    n = getMPFIntegerAsString( validateRealInt( n ) )

    if  validateRealInt( source ) < 0:
        raise ValueError( 'source value must be a positive integer' )

    if validateRealInt( replace ) < 0:
        raise ValueError( 'replace value must be a positive integer' )

    return mpmathify( n.replace( str( int ( source ) ), str( int( replace ) ) ) )


#******************************************************************************
#
#  duplicateDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def duplicateDigits( n, k ):
    if validateRealInt( k ) < 0:
        raise ValueError( "'duplicate_digits' requires a non-negative integer for the second argument" )

    return appendDigits( validateRealInt( n ), fmod( n, power( 10, nint( floor( k ) ) ) ), k )


#******************************************************************************
#
#  duplicateNumber
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def duplicateNumber( n, k ):
    if validateRealInt( k ) == 0:
        return 0

    if k < 0:
        raise ValueError( "'duplicate_number' requires a non-negative integer for the second argument" )

    return mpmathify( getMPFIntegerAsString( n ) * int( k ) )


#******************************************************************************
#
#  reverseDigits
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def reverseDigits( n ):
    return mpmathify( getMPFIntegerAsString( n )[ : : -1 ] )


#******************************************************************************
#
#  isPalindrome
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isPalindrome( n ):
    result = getMPFIntegerAsString( n )

    length = len( result )

    for i in range( 0, length // 2 ):
        if result[ i ] != result[ -( i + 1 ) ]:
            return 0

    return 1


#******************************************************************************
#
#  isPandigital
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isPandigital( n ):
    n = getMPFIntegerAsString( n )

    length = len( n )

    if length < 10:
        digitsToCheck = string.digits[ 1 : length + 1 ]
    else:
        digitsToCheck = string.digits

    for c in digitsToCheck:
        if c not in n:
            return 0

    return 1


#******************************************************************************
#
#  containsDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def containsDigits( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in k:
        if c not in n:
            return 0

    return 1


#******************************************************************************
#
#  containsAnyDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def containsAnyDigits( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in k:
        if c in n:
            return 1

    return 0


#******************************************************************************
#
#  containsOnlyDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def containsOnlyDigits( n, k ):
    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    for c in getMPFIntegerAsString( n ):
        if c not in k:
            return 0

    return 1


#******************************************************************************
#
#  countDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def countDigits( n, k ):
    n = getMPFIntegerAsString( n )

    if isinstance( k, ( mpf, int, float ) ):
        k = getMPFIntegerAsString( k )

    result = 0

    for c in k:
        result += n.count( c )

    return result


#******************************************************************************
#
#  getDigitCount
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getDigitCount( n ):
    return len( getMPFIntegerAsString( n ) )


#******************************************************************************
#
#  countDifferentDigits
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def countDifferentDigits( n ):
    return len( list( set( getMPFIntegerAsString( n ) ) ) )


#******************************************************************************
#
#  getNthReversalAdditionGenerator
#
#  https://en.wikipedia.org/wiki/Lychrel_number
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getNthReversalAdditionGenerator( n, k ):
    next = int( validateRealInt( n ) )
    yield next

    for _ in arange( k ):
        next = fadd( reverseDigits( next ), next )

        yield next

        if isPalindrome( next ):
            break

def getNthReversalAddition( n, k ):
    return RPNGenerator( getNthReversalAdditionGenerator( n, k ) )


#******************************************************************************
#
#  findPalindrome
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def findPalindrome( n, k ):
    next = int( validateRealInt( n ) )

    for i in range( int( validateRealInt( k ) ) + 1 ):
        next = reverseDigits( next ) + next

        if isPalindrome( next ):
            return [ i + 1, next ]

    return [ k, 0 ]


#******************************************************************************
#
#  isNarcissistic
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isNarcissistic( n ):
    digits = getDigitList( validateRealInt( n ) )

    count = len( digits )

    sum = 0

    for digit in digits:
        sum = fadd( sum, power( digit, count ) )

        if sum > n:
            return 0

    return 1 if sum == n else 0


#******************************************************************************
#
#  isPerfectDigitalInvariant
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isPerfectDigitalInvariant( n ):
    digits = getDigitList( validateRealInt( n ) )

    exponent = 1

    oldsum = 0

    while True:
        sum = 0

        for digit in digits:
            sum = fadd( sum, power( digit, exponent ) )

            if sum > n:
                return 0
            elif sum == n:
                return 1

        if sum == oldsum:
            return 0

        oldsum = sum

        exponent += 1


#******************************************************************************
#
#  isBaseKNarcissistic
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isBaseKNarcissistic( n, k ):
    digits = getBaseKDigits( validateRealInt( n ), k )

    count = len( digits )

    sum = 0

    for digit in digits:
        sum = fadd( sum, power( digit, count ) )

        if sum > n:
            return 0

    return 1 if sum == n else 0


#******************************************************************************
#
#  isGeneralizedDudeneyNumber
#
#  http://www.jakob.at/steffen/dudeney.html
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isGeneralizedDudeneyNumber( base, exponent ):
    n = power( validateRealInt( base ), validateRealInt( exponent ) )
    return 1 if sumDigits( n ) == base else 0


#******************************************************************************
#
#  isPerfectDigitToDigitInvariant
#
#  https://en.wikipedia.org/wiki/Perfect_digit-to-digit_invariant
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isPerfectDigitToDigitInvariant( n, k ):
    digits = getBaseKDigits( validateRealInt( n ), k )

    sum = 0

    for digit in digits:
        digit = int( digit )

        if digit != 0:
            sum = fadd( sum, power( digit, digit ) )

        if sum > n:
            return 0

    return 1 if sum == n else 0


#******************************************************************************
#
#  isSumProductNumber
#
#  https://en.wikipedia.org/wiki/Sum-product_number
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isSumProductNumber( n, k ):
    digits = getBaseKDigits( validateRealInt( n ), k )
    sum = fmul( fsum( digits ), fprod( digits ) )
    return 1 if sum == n else 0


#******************************************************************************
#
#  isHarshadNumber
#
#  https://en.wikipedia.org/wiki/Harshad_number
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isHarshadNumber( n, k ):
    digits = getBaseKDigits( validateRealInt( n ), k )
    return 1 if isDivisible( n, fsum( digits ) ) else 0


#******************************************************************************
#
#  isKaprekarNumber
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isKaprekarNumber( n ):
    if n == 1:
        return 1
    elif n < 9:
        return 0

    a, b = splitNumberByDigits( power( n, 2 ) )

    return 1 if ( fadd( a, b ) == n ) else 0


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
#  buildNumbers
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def buildNumbers( expression ):
    digitLists = parseNumbersExpression( expression )

    if len( digitLists ) == 1:
        return RPNGenerator.createGenerator( convertStringsToNumbers, digitLists )
    else:
        return RPNGenerator.createStringProduct( digitLists )


#******************************************************************************
#
#  buildLimitedDigitNumbers
#
#******************************************************************************

def buildLimitedDigitNumbers( digits, minLength, maxLength ):
    if minLength < 1:
        raise ValueError( 'minimum length must be greater than 0' )

    if  maxLength < minLength:
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
#
#  A digit expression (I) can be a single digit or a range.  A single digit is
#  anything from "0" through "9".  A digit range looks like: "a-b" where a
#  is a digit that is smaller than b.
#
#******************************************************************************

def parseNumbersExpression( arg ):
    if not isinstance( arg, str ):
        arg = str( validateRealInt( arg ) )

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
                raise ValueError( 'unexpected character \'{}\''.format( char ) )
        elif state == startDigitState:
            if '0' <= char <= '9':
                currentGroup.add( char )
                state = digitState
                lastDigit = char
            elif char == ']':
                result.append( sorted( list( currentGroup ) ) )
                state = defaultState
            else:
                raise ValueError( 'unexpected character \'{}\''.format( char ) )
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
                raise ValueError( 'unexpected character \'{}\''.format( char ) )
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
                raise ValueError( 'unexpected character \'{}\''.format( char ) )

    return result


#******************************************************************************
#
#  hasUniqueDigits
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def hasUniqueDigits( n ):
    digits = getDigitList( validateRealInt( n ) )

    existing = set( )

    for digit in digits:
        if digit in existing:
            return 0
        else:
            existing.add( digit )

    return 1


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
#  isKMorphic
#
#  This code won't work correctly for integral powers of 10, but they can
#  never be morphic anyway, except for 1, which I handle specially.
#
#******************************************************************************

def isKMorphic( n, k ):
    '''
    Returns true if n to the k power ends with n.
    '''
    if n == 1:
        return 1

    modulo = power( 10, ceil( log10( n ) ) )
    powmod = getPowMod( n, validateRealInt( k ), modulo )

    return 1 if ( n == powmod ) else 0

@twoArgFunctionEvaluator( )
def isKMorphicOperator( n, k ):
    return isKMorphic( n, k )

@oneArgFunctionEvaluator( )
def isAutomorphic( n ):
    return isKMorphic( n, 2 )

@oneArgFunctionEvaluator( )
def isTrimorphic( n ):
    return isKMorphic( n, 3 )


#******************************************************************************
#
#  getLeftTruncations
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLeftTruncations( n ):
    if n < 0:
        raise ValueError( '\'get_left_truncations\' requires a positive argument' )

    n = getMPFIntegerAsString( n )

    for i, _ in enumerate( n ):
        yield mpmathify( n[ i : ] )

@oneArgFunctionEvaluator( )
def getLeftTruncationsGenerator( n ):
    return RPNGenerator.createGenerator( getLeftTruncations, n )


#******************************************************************************
#
#  getRightTruncations
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getRightTruncations( n ):
    if n < 0:
        raise ValueError( '\'get_right_truncations\' requires a positive argument' )

    result = getMPFIntegerAsString( n )

    for i in range( len( result ), 0, -1 ):
        yield mpmathify( result[ 0 : i ] )

@oneArgFunctionEvaluator( )
def getRightTruncationsGenerator( n ):
    return RPNGenerator.createGenerator( getRightTruncations, n )


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
    else:
        return getMultiplicativePersistence( multiplyDigitList( n, exponent, dropZeroes ),
                                             exponent, dropZeroes, persistence + 1 )

@oneArgFunctionEvaluator( )
def getPersistence( n ):
    return getMultiplicativePersistence( n )

@twoArgFunctionEvaluator( )
def getKPersistence( n, k ):
    return getMultiplicativePersistence( n, k )

@oneArgFunctionEvaluator( )
def getErdosPersistence( n ):
    return getMultiplicativePersistence( n, 1, True )



#******************************************************************************
#
#  showMultiplicativePersistence
#
#******************************************************************************

def showMultiplicativePersistence( n, exponent = 1, dropZeroes = False ):
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
def showPersistence( n ):
    return RPNGenerator.createGenerator( showMultiplicativePersistence, [ n ] )

@twoArgFunctionEvaluator( )
def showKPersistence( n, k ):
    return RPNGenerator.createGenerator( showMultiplicativePersistence, [ n, k ] )


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
def showErdosPersistence( n ):
    return RPNGenerator.createGenerator( showErdosPersistenceGenerator, [ n ] )

@oneArgFunctionEvaluator( )
def permuteDigits( n ):
    return RPNGenerator.createPermutations( getMPFIntegerAsString( n ) )


#******************************************************************************
#
#  isIncreasing
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isIncreasing( n ):
    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if n[ i ] < n[ i - 1 ]:
            return 0

    return 1


#******************************************************************************
#
#  isDecreasing
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isDecreasing( n ):
    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if n[ i ] > n[ i - 1 ]:
            return 0

    return 1


#******************************************************************************
#
#  isBouncy
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isBouncy( n ):
    if isIncreasing( n ) == 0 and isDecreasing( n ) == 0:
        return 1
    else:
        return 0


#******************************************************************************
#
#  rotateDigitsLeft
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def rotateDigitsLeft( n, k ):
    if k < 0:
        return rotateDigitsRight( n, fneg( k ) )

    n = getMPFIntegerAsString( n )

    if k > len( n ):
        raise ValueError( 'cannot rotate more digits than the number has' )

    rotate = int( k )

    n = n[ rotate : ] + n[ : rotate ]
    return mpmathify( n )


#******************************************************************************
#
#  rotateDigitsRight
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def rotateDigitsRight( n, k ):
    if k < 0:
        return rotateDigitsLeft( n, fneg( k ) )

    n = getMPFIntegerAsString( n )

    if k > len( n ):
        raise ValueError( 'cannot rotate more digits than the number has' )

    rotate = int( k )

    n = n[ -rotate : ] + n[ : -rotate ]
    return mpmathify( n )


#******************************************************************************
#
#  getCyclicPermutations
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getCyclicPermutations( n ):
    result = [ n ]

    n = getMPFIntegerAsString( n )

    for _ in range( len( n ) - 1 ):
        n = n[ 1 : ] + n[ : 1 ]
        result.append( mpmathify( n ) )

    return result


#******************************************************************************
#
#  isDigitalPermutation
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def isDigitalPermutation( n, k ):
    str1 = getMPFIntegerAsString( n )
    str2 = getMPFIntegerAsString( k )

    if len( str1 ) != len( str2 ):
        return 0

    if sorted( str1 ) != sorted( str2 ):
        return 0

    return 1


#******************************************************************************
#
#  getSquareDigitChainGenerator
#
#******************************************************************************

def generateSquareDigitChainGenerator( n ):
    n = validateRealInt( floor( n ) )

    if n == 0:
        yield 0
        return

    if n == 1:
        yield 1
        return

    if n == 89:
        yield 89
        return

    done = False

    while not done:
        digits = getDigits( n )

        n = 0

        for i in digits:
            n = fadd( n, pow( i, 2 ) )

        yield n

        if n in ( 1, 89 ):
            done = True

@oneArgFunctionEvaluator( )
def generateSquareDigitChain( n ):
    return RPNGenerator.createGenerator( generateSquareDigitChainGenerator, [ n ] )


#******************************************************************************
#
#  isStepNumber
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def isStepNumber( n ):
    if n < 10:
        return 0

    n = getMPFIntegerAsString( n )

    for i in range( 1, len( n ) ):
        if abs( int( n[ i ] ) - int( n[ i - 1 ] ) ) != 1:
            return 0

    return 1


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
#  buildStepNumbers
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
def buildStepNumbers( n ):
    return RPNGenerator.createGenerator( buildStepNumbersGenerator, [ n ] )


#******************************************************************************
#
#  isSmithNumber
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'smith' )
def isSmithNumber( n ):
    if isPrime( validateRealInt( n ) ) or n < 2:
        return 0

    sum1 = sumDigits( n )
    sum2 = fsum( [ sumDigits( i ) for i in getFactors( n ) ] )

    return 1 if sum1 == sum2 else 0


#******************************************************************************
#
#  isBaseKSmithNumber
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@cachedFunction( 'base_k_smith' )
def isBaseKSmithNumber( n, k ):
    if validateRealInt( k ) < 2:
        raise ValueError( "'is_base_k_smith_number' base argument must be 2 or greater" )

    if k > 4 and n == 4:
        return 1

    if k > 4 and n < k:
        return 0

    if isPrime( validateRealInt( n ) ) or n < 2:
        return 0

    sum1 = fsum( getBaseKDigits( n, k ) )
    sum2 = fsum( [ fsum( getBaseKDigits( i, k ) ) for i in getFactors( n ) ] )

    return 1 if sum1 == sum2 else 0


#******************************************************************************
#
#  isOrderKSmithNumber
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@cachedFunction( 'order_k_smith' )
def isOrderKSmithNumber( n, k ):
    if isPrime( validateRealInt( n ) ) or n < 2:
        return 0

    digitList1 = getNonzeroDigits( n )
    digitList2 = [ item for sublist in [ getNonzeroDigits( m ) for m in getFactors( n ) ] for item in sublist ]

    if sorted( digitList1 ) == sorted( digitList2 ):
        return 0

    sum1 = fsum( [ power( i, k ) for i in getDigits( n ) ] )
    sum2 = fsum( [ power( j, k ) for j in [ item for sublist in \
                        [ getDigits( m ) for m in getFactors( n ) ] for item in sublist ] ] )

    return 1 if sum1 == sum2 else 0


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
