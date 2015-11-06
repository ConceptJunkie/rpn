#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUtils.py
# //
# //  RPN command-line calculator lexicographic functions
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import string

from mpmath import *

import rpnGlobals as g

from rpnUtils import real, real_int


# //******************************************************************************
# //
# //  getDigits
# //
# //******************************************************************************

def getDigits( n ):
    str = nstr( nint( n ), int( floor( log10( n ) + 2 ) ) )

    result = [ ]

    for c in str[ : -2 ]:
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
    if isinstance( n, list ):
        if isinstance( n[ 0 ], list ):
            return [ combineDigits( i ) for i in n ]
        else:
            result = 0

            for i in n:
                if im( i ) != 0:
                    raise ValueError( "'combine_digits' requires a list of real values" )
                elif i < 0:
                    raise ValueError( "'combine_digits' requires a list of non-negative integers" )
                else:
                    result = addDigits( result, i )

            return result
    else:
        return n


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
    str = nstr( nint( n ), int( floor( log10( n ) + 2 ) ) )
    return mpmathify( str[ -3 : : -1 ] )


# //******************************************************************************
# //
# //  isPalindrome
# //
# //******************************************************************************

def isPalindrome( n ):
    str = nstr( nint( n ), int( floor( log10( n ) + 2 ) ) )[ 0: -2 ]

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
    str = nstr( nint( n ), int( floor( log10( n ) + 2 ) ) )[ 0: -2 ]

    for c in string.digits:
        if not c in str:
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

