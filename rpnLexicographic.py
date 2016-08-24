#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnLexicographic.py
# //
# //  RPN command-line calculator lexicographic functions
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools
import string

from mpmath import arange, fadd, fdiv, floor, fmod, fmul, fprod, fsub, fsum, \
                   log10, mpmathify, nint, power

from rpnGenerator import RPNGenerator
from rpnUtils import real, real_int, getMPFIntegerAsString


# //******************************************************************************
# //
# //  splitNumberByDigits
# //
# //  This splits the number into 2 numbers by splitting off half the digits
# //  for the first and the rest of the digits for the second.  If there is an
# //  odd number of digits then the extra digit goes to the second number.
# //
# //******************************************************************************

def splitNumberByDigits( n ):
    str = getMPFIntegerAsString( n )

    split = len( str ) // 2

    return mpmathify( str[ : split ] ), mpmathify( str[ split : ] )


# //******************************************************************************
# //
# //  getDigits
# //
# //******************************************************************************

def getDigits( n, dropZeroes = False ):
    str = getMPFIntegerAsString( n )

    result = [ ]

    for c in str:
        if dropZeroes and c == '0':
            continue

        result.append( int( c ) )

    return result


# //******************************************************************************
# //
# //  sumDigits
# //
# //******************************************************************************

def sumDigits( n ):
    return fsum( getDigits( n ) )


# //******************************************************************************
# //
# //  multiplyDigits
# //
# //******************************************************************************

def multiplyDigits( n, exponent = 1, dropZeroes = False ):
    if exponent < 1:
        raise ValueError( 'multiplyDigits( ) expects a positive integer for \'exponent\'' )
    elif exponent == 1:
        return fprod( getDigits( n, dropZeroes ) )
    else:
        return fprod( [ power( i, exponent ) for i in getDigits( n, dropZeroes ) ] )


# //******************************************************************************
# //
# //  appendDigits
# //
# //******************************************************************************

def appendDigits( n, digits, digitCount ):
    if real( n ) < 0:
        return nint( fsub( fmul( floor( n ), power( 10, digitCount ) ), digits ) )
    else:
        return nint( fadd( fmul( floor( n ), power( 10, digitCount ) ), digits ) )


# //******************************************************************************
# //
# //  addDigits
# //
# //******************************************************************************

def addDigits( n, k ):
    if real( k ) < 0:
        raise ValueError( "'add_digits' requires a non-negative integer for the second argument" )

    digits = int( k )

    if digits == 0:
        digitCount = 1
    else:
        digitCount = int( fadd( floor( log10( k ) ), 1 ) )

    return appendDigits( n, digits, digitCount )


# //******************************************************************************
# //
# //  combineDigits
# //
# //******************************************************************************

def combineDigits( n ):
    result = 0

    listResult = False

    for i in n:
        if isinstance( i, ( list, RPNGenerator ) ) and result == 0:
            listResult = True
            result = [ combineDigits( i ) ]
        elif listResult:
            result.append( combineDigits( i ) )
        else:
            result = addDigits( result, real_int( i ) )

    return result


# //******************************************************************************
# //
# //  duplicateDigits
# //
# //******************************************************************************

def duplicateDigits( n, k ):
    if real( k ) < 0:
        raise ValueError( "'dup_digits' requires a non-negative integer for the second argument" )

    return appendDigits( real( n ), fmod( n, power( 10, nint( floor( k ) ) ) ), k )


# //******************************************************************************
# //
# //  reverseDigits
# //
# //******************************************************************************

def reverseDigits( n ):
    return mpmathify( getMPFIntegerAsString( n )[ : : -1 ] )


# //******************************************************************************
# //
# //  isPalindrome
# //
# //******************************************************************************

def isPalindrome( n ):
    str = getMPFIntegerAsString( n )

    length = len( str )

    for i in range( 0, length // 2 ):
        if str[ i ] != str[ -( i + 1 ) ]:
            return 0

    return 1


# //******************************************************************************
# //
# //  isPandigital
# //
# //******************************************************************************

def isPandigital( n ):
    str = getMPFIntegerAsString( n )

    for c in string.digits:
        if c not in str:
            return 0

    return 1


# //******************************************************************************
# //
# //  getNthReversalAddition
# //
# //  https://en.wikipedia.org/wiki/Lychrel_number
# //
# //******************************************************************************

def getNthReversalAddition( n, k ):
    next = int( real_int( n ) )
    yield next

    previous = next

    for i in arange( k ):
        if isPalindrome( next ):
            break

        next = fadd( reverseDigits( next ), next )
        yield next


# //******************************************************************************
# //
# //  findPalindrome
# //
# //  https://en.wikipedia.org/wiki/Lychrel_number
# //
# //******************************************************************************

def findPalindrome( n, k ):
    next = int( real_int( n ) )

    for i in range( int( real_int( k ) ) + 1 ):
        if isPalindrome( next ):
            return [ i, next ]
        else:
            next = reverseDigits( next ) + next

    return [ k, 0 ]


# //******************************************************************************
# //
# //  isNarcissistic
# //
# //******************************************************************************

def isNarcissistic( n ):
    digits = getDigits( real_int( n ) )

    count = len( digits )

    sum = 0

    for d in digits:
        sum = fadd( sum, power( d, count ) )

    return 1 if sum == n else 0


# //******************************************************************************
# //
# //  isKaprekar
# //
# //******************************************************************************

def isKaprekar( n ):
    if n == 1:
        return 1
    elif n < 9:
        return 0

    a, b = splitNumberByDigits( power( n, 2 ) )

    return 1 if ( fadd( a, b ) == n ) else 0


# //******************************************************************************
# //
# //  convertStringsToNumbers
# //
# //******************************************************************************

def convertStringsToNumbers( values ):
    for i in values:
        yield( mpmathify( i ) )


# //******************************************************************************
# //
# //  buildNumbers
# //
# //******************************************************************************

def buildNumbers( expression ):
    digitLists = parseNumbersExpression( expression )

    if ( len( digitLists ) == 1 ):
        return RPNGenerator.createGenerator( convertStringsToNumbers, digitLists )
    else:
        return RPNGenerator.createStringProduct( digitLists )


# //******************************************************************************
# //
# //  buildLimitedDigitNumbers
# //
# //  TODO:  This should be creating a generator!
# //
# //******************************************************************************

def buildLimitedDigitNumbers( digits, minLength, maxLength ):
    result = [ ]

    if minLength < 1:
        raise ValueError( 'minimum length must be greater than 0' )

    if  maxLength < minLength:
        raise ValueError( 'maximum length must be greater than or equal to minimum length' )

    for i in range( minLength, maxLength + 1 ):
        for item in itertools.product( digits, repeat=i ):
            number = ''

            for digit in item:
                number += digit

            result.append( number )

    return result


# //******************************************************************************
# //
# //  parseNumbersExpression
# //
# //  D[D]...
# //
# //  One or more digit expressions where each digit expression can be:
# //      - A single digit, "0" through "9"
# //      - "d" - digit (equivalent to "[0-9]"
# //      - "[I[I]...]" - any of the individual digit expressions
# //      - "[I[I]...:m]" - permutations of any digits I, m digits long
# //      - "[I[I]...:n:m]" - permutations of any digits I, from a minimum of n,
# //                          up to a maximum of m digits long
# //
# //  A digit expression (I) can be a single digit or a range.  A single digit is
# //  anything from "0" through "9".  A digit range looks like: "a-b" where a
# //  is a digit that is smaller than b.
# //
# //******************************************************************************

def parseNumbersExpression( arg ):
    if not isinstance( arg, str ):
        arg = str( real_int( arg ) )

    result = [ ]

    digitRange = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]

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

    for ch in arg:
        #print( 'state', state, 'ch', ch, 'result', result, 'currentGroup', currentGroup )
        if state == defaultState:
            if ch == 'd':
                result.append( digitRange )
            elif ch == '[':
                state = digitState
                currentGroup = set( )
            elif '0' <= ch <= '9':
                result.append( [ ch ] )
            else:
                raise ValueError( 'unexpected character \'{}\''.format( ch ) )
        elif state == startDigitState:
            if '0' <= ch <= '9':
                currentGroup.add( ch )
                state = digitState
                lastDigit = ch
            elif ch == ']':
                result.append( sorted( list( currentGroup ) ) )
                state = defaultState
            else:
                raise ValueError( 'unexpected character \'{}\''.format( ch ) )
        elif state == digitState:
            if '0' <= ch <= '9':
                currentGroup.add( ch )
                lastDigit = ch
            elif ch == '-':
                state = startRangeState
            elif ch == ':':
                state = numberLengthRange1
            elif ch == ']':
                result.append( sorted( list( currentGroup ) ) )
                state = defaultState
        elif state == startRangeState:
            if '0' <= ch <= '9':
                if ch <= lastDigit:
                    raise ValueError( 'invalid digit range' )
                else:
                    for i in range( int( lastDigit ), int( ch ) + 1 ):
                        currentGroup.add( str( i ) )

                state = digitState
        elif state == numberLengthRange1:
            if '0' <= ch <= '9':
                lengthRangeHigh += ch
            elif ch == ':':
                lengthRangeLow = lengthRangeHigh
                lengthRangeHigh = ''
                state = numberLengthRange2
            elif ch == ']':
                result.append( buildLimitedDigitNumbers( sorted( list( currentGroup ) ),
                                                         int( lengthRangeHigh ), int( lengthRangeHigh ) ) )
                lengthRangeLow = ''
                lengthRangeHigh = ''
                state = defaultState
            else:
                raise ValueError( 'unexpected character \'{}\''.format( ch ) )
        elif state == numberLengthRange2:
            if '0' <= ch <= '9':
                lengthRangeHigh += ch
            elif ch == ']':
                result.append( buildLimitedDigitNumbers( sorted( list( currentGroup ) ),
                                                         int( lengthRangeLow ), int( lengthRangeHigh ) ) )
                lengthRangeLow = ''
                lengthRangeHigh = ''
                state = defaultState
            else:
                raise ValueError( 'unexpected character \'{}\''.format( ch ) )

    return result


# //******************************************************************************
# //
# //  hasUniqueDigits
# //
# //******************************************************************************

def hasUniqueDigits( n ):
    digits = getDigits( real_int( n ) )

    existing = set( )

    for digit in digits:
        if digit in existing:
            return 0
        else:
            existing.add( digit )

    return 1


# //******************************************************************************
# //
# //  hasDigits
# //
# //******************************************************************************

def hasDigits( value, digits ):
    pass


# //******************************************************************************
# //
# //  isMorphic
# //
# //******************************************************************************

def isMorphic( n, k ):
    '''
    Returns true if n to the k power ends with n.
    '''
    digits = getMPFIntegerAsString( real_int( n ) )
    sqr_digits = getMPFIntegerAsString( power( n, real_int( k ) ) )

    start = len( sqr_digits ) - len( digits )
    return 1 if ( sqr_digits[ start : ] == digits ) else 0


# //******************************************************************************
# //
# //  getLeftTruncations
# //
# //******************************************************************************

def getLeftTruncations( n ):
    if n < 0:
        raise ValueError( '\'get_left_truncations\' requires a positive argument' )

    str = getMPFIntegerAsString( n )

    for i, e in enumerate( str ):
        yield mpmathify( str[ i : ] )


# //******************************************************************************
# //
# //  getRightTruncations
# //
# //******************************************************************************

def getRightTruncations( n ):
    if n < 0:
        raise ValueError( '\'get_right_truncations\' requires a positive argument' )

    str = getMPFIntegerAsString( n )

    for i in range( len( str ), 0, -1 ):
        yield mpmathify( str[ 0 : i ] )


# //******************************************************************************
# //
# //  getPersistence
# //
# //******************************************************************************

def getPersistence( n, exponent = 1, dropZeroes = False, persistence = 0 ):
    if exponent == 1 and n < 10:
        return persistence

    if n <= 1:
        return persistence
    else:
        return getPersistence( multiplyDigits( n, exponent, dropZeroes ), exponent, dropZeroes, persistence + 1 )


# //******************************************************************************
# //
# //  showPersistence
# //
# //******************************************************************************

def showPersistence( n, exponent = 1, dropZeroes = False ):
    yield n

    if exponent == 1:
        while n >= 10:
            n = multiplyDigits( n, exponent, dropZeroes )
            yield n
    else:
        while n > 1:
            n = multiplyDigits( n, exponent, dropZeroes )
            yield n


# //******************************************************************************
# //
# //  showErdosPersistence
# //
# //******************************************************************************

def showErdosPersistence( n ):
    yield n

    while n >= 10:
        n = multiplyDigits( n, 1, True )
        yield n

