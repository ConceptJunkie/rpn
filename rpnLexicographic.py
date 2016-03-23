#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnLexicographic.py
# //
# //  RPN command-line calculator lexicographic functions
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import string

from mpmath import fadd, fdiv, floor, fmod, fmul, fprod, fsub, fsum, log10, \
                   mpmathify, nint, power

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

def getDigits( n ):
    str = getMPFIntegerAsString( n )

    result = [ ]

    for c in str:
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

def multiplyDigits( n ):
    return fprod( getDigits( n ) )


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

    for i in n:
        result = addDigits( result, real_int( i ) )

    return result


# //******************************************************************************
# //
# //  duplicateDigits
# //
# //******************************************************************************

def duplicateDigits( n, k ):
    if real( k ) < 0:
        raise ValueError( "'add_digits' requires a non-negative integer for the second argument" )

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

    for i in range( int( real_int( k ) ) ):
        if isPalindrome( next ):
            break

        next = reverseDigits( next ) + next

    return next


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
# //  buildNumbers
# //
# //******************************************************************************

def buildNumbers( expression ):
    digitLists = parseNumbersExpression( expression )

    return RPNGenerator.createProduct( digitLists )


# //******************************************************************************
# //
# //  parseNumbersExpression
# //
# //******************************************************************************

def parseNumbersExpression( expression ):
    return [ [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ],
             [ '2', '3', '4', '5', '9' ],
             [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ] ]

