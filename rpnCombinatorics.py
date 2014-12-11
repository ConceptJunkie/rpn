#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnCombinatorics.py
# //
# //  RPN command-line calculator combinatorics operators
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

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


