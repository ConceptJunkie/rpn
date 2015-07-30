#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnCombinatorics.py
# //
# //  RPN command-line calculator combinatorics operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools

from mpmath import *

from rpnNumberTheory import *


# //******************************************************************************
# //
# //  getNthAperyNumber
# //
# //  http://oeis.org/A005259
# //
# //  a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
# //
# //******************************************************************************

def getNthAperyNumber( n ):
    result = 0

    for k in arange( 0, n + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ),
                                     power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


# //******************************************************************************
# //
# //  getNthDelannoyNumber
# //
# //******************************************************************************

def getNthDelannoyNumber( n ):
    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


# //******************************************************************************
# //
# //  getNthSchroederNumber
# //
# //******************************************************************************

def getNthSchroederNumber( n ):
    if n == 1:
        return 1

    # TODO: raise exception for n < 0 !

    n = fsub( n, 1 )

    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fdiv( fprod( [ power( 2, k ), binomial( n, k ),
                                              binomial( n, fsub( k, 1 ) ) ] ), n ) )

    return result


# //******************************************************************************
# //
# //  getNthMotzkinNumber
# //
# //  http://oeis.org/A001006
# //
# //  a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
# //
# //******************************************************************************

def getNthMotzkinNumber( n ):
    result = 0

    for j in arange( 0, floor( fdiv( n, 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                      binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


# //******************************************************************************
# //
# //  getNthPellNumber
# //
# //  From:  http://oeis.org/A000129
# //
# //  a( n ) = round( ( 1 + sqrt( 2 ) ) ^ n )
# //
# //******************************************************************************

def getNthPellNumber( n ):
    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], n )


# //******************************************************************************
# //
# //  getPermutations
# //
# //******************************************************************************

def getPermutations( n, r ):
    if ( r > n ):
        raise ValueError( 'number of elements (%d) cannot exceed the size '
                          'of the set (%d)' % ( r, n ) )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


# //******************************************************************************
# //
# //  getNthSylvester
# //
# //******************************************************************************

def getNthSylvester( n ):
    if n == 1:
        return 2
    elif n == 2:
        return 3
    else:
        list = [ 2, 3 ]

        for i in arange( 2, n ):
            list.append( fprod( list ) + 1 )

    return list[ -1 ]


# //******************************************************************************
# //
# //  createDeBruijnSequence
# //
# //******************************************************************************

def createDeBruijnSequence( n, k ):
    wordSize = int( k )
    symbolCount = int( n )

    v = [ 0 for _ in range( wordSize ) ]
    l = 1
    result = [ ]

    while True:
        if wordSize % l == 0:
            result.extend( v[ 0 : l ] )

        for i in range( l, wordSize ):
            v[ i ] = v[ i - l ]

        l = wordSize

        while l > 0 and v[ l - 1 ] >= symbolCount - 1:
            l-=1

        if l == 0:
            break

        v[ l - 1 ] += 1

    return result


# //******************************************************************************
# //
# //  getCompositions
# //
# //******************************************************************************

def getCompositions( n, k ):
    value = int( floor( n ) )
    count = int( floor( k ) )

    if count < 1:
        raise ValueError( "'compositions' expects a size greater than 0'" )

    if count == 1:
        return [ [ floor( n ) ] ]
    else:
        result = [ ]

        for i in range( 1, int( ( n - count ) + 2 ) ):
            result.extend( [ [ nint( i ) ] + comp for comp in getCompositions( n - i, count - 1 ) ] )

        return result


# //******************************************************************************
# //
# //  getPartitionNumber
# //
# //******************************************************************************

def getPartitionNumber( n, k ):
    #if k < 1:
    #    raise ValueError

    #if n < 0:
    #    raise ValueError

    if k > n:
         return 0

    if k == n:
        return 1

    return getPartitionNumber( n, k + 1 ) + getPartitionNumber( n - k, k )


# //******************************************************************************
# //
# //  getNthMultifactorial
# //
# //******************************************************************************

def getNthMultifactorial( n, k ):
    return fprod( range( int( n ), 0, -( int( k ) ) ) )

