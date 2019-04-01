#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPrimeUtils.py
# //
# //  RPN command-line calculator prime number utilies
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import contextlib
import gmpy2
import os
import pickle
import sys

from bisect import bisect_left
from mpmath import arange, fadd, fmod, fmul, fsub, mp
from pathlib import Path

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnPrimes import primes
from rpn.rpnPersistence import cachedFunction, openPrimeCache
from rpn.rpnUtils import debugPrint, getDataPath, oneArgFunctionEvaluator, \
                         twoArgFunctionEvaluator, real_int

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  isPrimeNumber
# //
# //******************************************************************************

def isPrimeNumber( n ):
    if g.zhangConjecturesAllowed and n < 1543267864443420616877677640751301:
        return isPrimeMillerRabin( int( n ) )
    elif n < 3317044064679887385961981:
        return isPrimeMillerRabin( int( n ) )
    else:
        debugPrint( 'primality testing of ' + str( int( n ) ) )
        return 1 if gmpy2.is_bpsw_prp( int( n ) ) else 0

@oneArgFunctionEvaluator( )
def isComposite( n ):
    return 0 if n == 1 or isPrimeNumber( n ) else 1

@oneArgFunctionEvaluator( )
def isPrime( n ):
    return 1 if isPrimeNumber( n ) else 0


# //******************************************************************************
# //
# //  isPrimeNumberSimple
# //
# //  Use this for numbers smaller than 10,000,000,000.
# //
# //******************************************************************************

def isPrimeNumberSimple( n ):
    # if prime is already in the list, just pick it
    if n <= max( primes ):
        i = bisect_left( primes, n )
        return i != len( primes ) and primes[ i ] == n

    # Divide by each known prime
    limit = int( n ** .5 )

    for p in primes:
        if p > limit:
            return True

        if n % p == 0:
            return False

    return True


# //******************************************************************************
# //
# //  getNextPrimeCandidate
# //
# //  p is the next prime candidate.  Starting with ( p - 10 ) mod 30, we only
# //  need to check 8 values out of the next 30, which eliminates all multiples
# //  of 2, 3 and 5, and saves us a lot of unnecessary checking.
# //
# //  We only need to check for a prime if ( p - 10 ) mod 30 is 1, 3, 7, 9, 13, 19,
# //  21 or 27.
# //
# //******************************************************************************

# can this work?
#
# rpn 10 4 primorial 9 - range x [ 2 3 5 7 ] is_div sum unfilter

# simpler version:   rpn 3 x [ 2 3 ] + eval


def getNextPrimeCandidate( p ):
    f = ( p - 10 ) % 30

    if f == 1:
        p += 2
    elif f == 3:
        p += 4
    elif f == 7:
        p += 2
    elif f == 9:
        p += 4
    elif f == 13:
        p += 6
    elif f == 19:
        p += 2
    elif f == 21:
        p += 6
    else:  # f == 27
        p += 4

    return p


# //******************************************************************************
# //
# //  getNextPrimeCandidateForAny
# //
# //  p is the next prime candidate.  Starting with ( p - 10 ) mod 210, we only
# //  need to check 43 values out of the next 210, which eliminates all multiples
# //  of 2, 3, 5, and 7 and saves us a lot of unnecessary checking.
# //
# //  We only need to check for a prime if ( p - 10 ) mod 210 is one of the
# //  following:
# //
# //  1, 3, 7, 9, 13, 19, 21, 27, 31, 33, 37, 43, 49, 51, 57, 61, 63, 69, 73,
# //  79, 87, 91, 93, 97, 99, 103, 111, 117, 121, 127, 129, 133, 139, 141, 147,
# //  153, 157, 159, 163, 169, 171, 177, 181, 183, 187, 189, 199, 201
# //
# //  rpn 10 219 range lambda x 7 is_div unfilter lambda x 5 is_div unfilter lambda x 3 is_div unfilter lambda x 2 is_div unfilter 10 -
# //
# //******************************************************************************

def getNextPrimeCandidateForAny( p ):
    f = ( p - 10 ) % 210

    moduloTable = {
        0 : 1,
        1 : 2, 2 : 1,
        3 : 4, 4 : 3, 5 : 2, 6 : 1,
        7 : 2, 8 : 1,
        9 : 4, 10 : 3, 11 : 2, 12 : 1,
        13 : 6, 14 : 5, 15 : 4, 16 : 3, 17 : 2, 18 : 1,
        19 : 2, 20 : 1,
        21 : 6, 22 : 5, 23 : 4, 24 : 3, 25 : 2, 26 : 1,
        27 : 4, 28 : 3, 29 : 2, 30 : 1,
        31 : 2, 32 : 1,
        33 : 4, 34 : 3, 35 : 2, 36 : 1,
        37 : 6, 38 : 5, 39 : 4, 40 : 3, 41 : 2, 42 : 1,
        43 : 6, 44 : 5, 45 : 4, 46 : 3, 47 : 2, 48 : 1,
        49 : 2, 50 : 1,
        51 : 6, 52 : 5, 53 : 4, 54 : 3, 55 : 2, 56 : 1,
        57 : 4, 58 : 3, 59 : 2, 60 : 1,
        61 : 2, 62 : 1,
        63 : 6, 64 : 5, 65 : 4, 66 : 3, 67 : 2, 68 : 1,
        69 : 4, 70 : 3, 71 : 2, 72 : 1,
        73 : 6, 74 : 5, 75 : 4, 76 : 3, 77 : 2, 78 : 1,
        79 : 8, 80 : 7, 81 : 6, 82 : 5, 83 : 4, 84 : 3, 85 : 2, 86 : 1,
        87 : 4, 88 : 3, 89 : 2, 90 : 1,
        91 : 2, 92 : 1,
        93 : 4, 94 : 3, 95 : 2, 96 : 1,
        97 : 2, 98 : 1,
        99 : 4, 100 : 3, 101 : 2, 102 : 1,
        103 : 8, 104 : 7, 105 : 6, 106 : 5, 107 : 4, 108 : 3, 109 : 2, 110 : 1,
        111 : 6, 112 : 5, 113 : 4, 114 : 3, 115 : 2, 116 : 1,
        117 : 4, 118 : 3, 119 : 2, 120 : 1,
        121 : 6, 122 : 5, 123 : 4, 124 : 3, 125 : 2, 126 : 1,
        127 : 2, 128 : 1,
        129 : 4, 130 : 3, 131 : 2, 132 : 1,
        133 : 6, 134 : 5, 135 : 4, 136 : 3, 137 : 2, 138 : 1,
        139 : 2, 140 : 1,
        141 : 6, 142 : 5, 143 : 4, 144 : 3, 145 : 2, 146 : 1,
        147 : 6, 148 : 5, 149 : 4, 150 : 3, 151 : 2, 152 : 1,
        153 : 4, 154 : 3, 155 : 2, 156 : 1,
        157 : 2, 158 : 1,
        159 : 4, 160 : 3, 161 : 2, 162 : 1,
        163 : 6, 164 : 5, 165 : 4, 166 : 3, 167 : 2, 168 : 1,
        169 : 2, 170 : 1,
        171 : 6, 172 : 5, 173 : 4, 174 : 3, 175 : 2, 176 : 1,
        177 : 4, 178 : 3, 179 : 2, 180 : 1,
        181 : 2, 182 : 1,
        183 : 4, 184 : 3, 185 : 2, 186 : 1,
        187 : 2, 188 : 1,
        189 : 10, 190 : 9, 191 : 8, 192 : 7, 193 : 6, 194 : 5, 195 : 4, 196 : 3, 197 : 2, 198 : 1,
        199 : 2, 200 : 1,
        201 : 10, 202 : 9, 203 : 8, 204 : 7, 205 : 6, 206 : 5, 207 : 4, 208 : 3, 209 : 2
    }

    return p + moduloTable[ f ]


# //******************************************************************************
# //
# //  getPreviousPrimeCandidateForAny
# //
# //******************************************************************************

def getPreviousPrimeCandidateForAny( p ):
    f = ( p - 10 ) % 210

    moduloTable = {
        0 : 9, 1 : 10,
        2 : 1, 3 : 2,
        4 : 1, 5 : 2, 6 : 3, 7 : 4,
        8 : 1, 9 : 2,
        10 : 1, 11 : 2, 12 : 3, 13 : 4,
        14 : 1, 15 : 2, 16 : 3, 17 : 4, 18 : 5, 19 : 6,
        20 : 1, 21 : 2,
        22 : 1, 23 : 2, 24 : 3, 25 : 4, 26 : 5, 27 : 6,
        28 : 1, 29 : 2, 30 : 3, 31 : 4,
        32 : 1, 33 : 2,
        34 : 1, 35 : 2, 36 : 3, 37 : 4,
        38 : 1, 39 : 2, 40 : 3, 41 : 4, 42 : 5, 43 : 6,
        44 : 1, 45 : 2, 46 : 3, 47 : 4, 48 : 5, 49 : 6,
        50 : 1, 51 : 2,
        52 : 1, 53 : 2, 54 : 3, 55 : 4, 56 : 5, 57 : 6,
        58 : 1, 59 : 2, 60 : 3, 61 : 4,
        62 : 1, 63 : 2,
        64 : 1, 65 : 2, 66 : 3, 67 : 4, 68 : 5, 69 : 6,
        70 : 1, 71 : 2, 72 : 3, 73 : 4,
        74 : 1, 75 : 2, 76 : 3, 77 : 4, 78 : 5, 79 : 6,
        80 : 1, 81 : 2, 82 : 3, 83 : 4, 84 : 5, 85 : 6, 86 : 7, 87 : 8,
        88 : 1, 89 : 2, 90 : 3, 91 : 4,
        92 : 1, 93 : 2,
        94 : 1, 95 : 2, 96 : 3, 97 : 4,
        98 : 1, 99 : 2,
        100: 1, 101 : 2, 102 : 3, 103 : 4,
        104 : 1, 105 : 2, 106 : 3, 107 : 4, 108 : 5, 109 : 6, 110 : 7, 111 : 8,
        112 : 1, 113 : 2, 114 : 3, 115 : 4, 116 : 5, 117 : 6,
        118 : 1, 119 : 2, 120 : 3, 121 : 4,
        122 : 1, 123 : 2, 124 : 3, 125 : 4, 126 : 5, 127 : 6,
        128 : 1, 129 : 2,
        130 : 1, 131 : 2, 132 : 3, 133 : 4,
        134 : 1, 135 : 2, 136 : 3, 137 : 4, 138 : 5, 139 : 6,
        140 : 1, 141 : 2,
        142 : 1, 143 : 2, 144 : 3, 145 : 4, 146 : 5, 147 : 6,
        148 : 1, 149 : 2, 150 : 3, 151 : 4, 152 : 5, 153 : 6,
        154 : 1, 155 : 2, 156 : 3, 157 : 4,
        158 : 1, 159 : 2,
        160 : 1, 161 : 2, 162 : 3, 163 : 4,
        164 : 1, 165 : 2, 166 : 3, 167 : 4, 168 : 5, 169 : 6,
        170 : 1, 171 : 2,
        172 : 1, 173 : 2, 174 : 3, 175 : 4, 176 : 5, 177 : 6,
        178 : 1, 179 : 2, 180 : 3, 181 : 4,
        182 : 1, 183 : 2,
        184 : 1, 185 : 2, 186 : 3, 187 : 4,
        188 : 1, 189 : 2,
        190 : 1, 191 : 2, 192 : 3, 193 : 4, 194 : 5, 195 : 6, 196 : 7, 197 : 8, 198 : 9, 199 : 10,
        200 : 1, 201 : 2,
        202 : 1, 203 : 2, 204 : 3, 205 : 4, 206 : 5, 207 : 6, 208 : 7, 209 : 8,
    }

    return p - moduloTable[ f ]


# //******************************************************************************
# //
# //  getNextPrime
# //
# //******************************************************************************

def getNextPrime( p, func = getNextPrimeCandidateForAny ):
    if ( p < 2 ):
        return 2
    if ( p == 2 ):
        return 3
    elif ( p < 5 ):
        return 5
    elif ( p < 7 ):
        return 7

    p = func( p )

    debugPrint( 'testing', p )

    while not isPrimeNumber( p ):
        p = func( p )

    return p

@oneArgFunctionEvaluator( )
@cachedFunction( 'next_prime' )
def getNextPrimeOperator( n ):
    return getNextPrime( n, func=getNextPrimeCandidateForAny )


# //******************************************************************************
# //
# //  getPreviousPrime
# //
# //******************************************************************************

def getPreviousPrime( p, func = getPreviousPrimeCandidateForAny ):
    if p < 12:
        if p < 3:
            raise ValueError( 'There is no previous prime to 2.' )
        elif p == 3:
            return 2
        elif p <= 5:
            return 3
        elif p <= 7:
            return 5
        elif p <= 11:
            return 7

    p = func( p )

    while not isPrimeNumber( p ):
        p = func( p )

    return p

@oneArgFunctionEvaluator( )
@cachedFunction( 'previous_prime' )
def getPreviousPrimeOperator( n ):
    return getPreviousPrime( n, func=getPreviousPrimeCandidateForAny )


# //******************************************************************************
# //
# //  getNextPrimes
# //
# //******************************************************************************

def getNextPrimes( p, k, func = getNextPrimeCandidateForAny ):
    result = [ ]

    for i in arange( 0, k ):
        p = getNextPrime( p, func )
        result.append( p )

    return result

@twoArgFunctionEvaluator( )
def getNextPrimesOperator( n, k ):
    return getNextPrimes( n, k, func=getNextPrimeCandidateForAny )


# //******************************************************************************
# //
# //  getPreviousPrimes
# //
# //******************************************************************************

def getPreviousPrimes( p, k, func = getPreviousPrimeCandidateForAny ):
    if p < 1000000000 and getNthPrime( p ) < k:
        raiseError( 'There is no previous prime to 2.' )

    result = [ ]

    for i in arange( 0, k ):
        p = getPreviousPrime( p, func )
        result.append( p )

    return result

@twoArgFunctionEvaluator( )
def getPreviousPrimesOperator( n, k ):
    return getPreviousPrimes( n, k, func=getPreviousPrimeCandidateForAny )


# //******************************************************************************
# //
# //  getNthPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPrime( arg ):
    n = int( arg )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 3
    elif n == 3:
        return 5
    elif g.primeDataAvailable and n >= 1000000000:
        openPrimeCache( 'huge_primes' )

        maxIndex = g.cursors[ 'huge_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'huge_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    elif g.primeDataAvailable and n >= 1000000:
        openPrimeCache( 'large_primes' )

        currentIndex, p = g.cursors[ 'large_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'small_primes' )

        currentIndex, p = g.cursors[ 'small_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 4
        p = 7

    while n > currentIndex:
        p = getNextPrime( p )
        currentIndex += 1

    return p


# //******************************************************************************
# //
# //  findPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def findPrime( arg ):
    target = int( arg )

    if target < 3:
        return 1, 2
    elif target == 3:
        return 2, 3
    elif target <= 5:
        return 3, 5
    elif target <= 7:
        return 4, 7
    elif target < 541:          # 100th prime
        currentIndex = 4
        p = 7
    elif g.primeDataAvailable and target <= 15485863:     # 1,000,000th prime
        openPrimeCache( 'small_primes' )

        currentIndex, p = g.cursors[ 'small_primes' ].execute(
            '''SELECT id, max( value ) FROM cache WHERE value <= ?''', ( target, ) ).fetchone( )
    elif g.primeDataAvailable and target <= 22801763489:  # 1,000,000,000th prime
        openPrimeCache( 'large_primes' )

        currentIndex, p = g.cursors[ 'large_primes' ].execute(
            '''SELECT id, max( value ) FROM cache WHERE value <= ?''', ( target, ) ).fetchone( )
    elif g.primeDataAvailable:
        openPrimeCache( 'huge_primes' )

        currentIndex, p = g.cursors[ 'huge_primes' ].execute(
            '''SELECT id, max( value ) FROM cache WHERE value <= ?''', ( target, ) ).fetchone( )
    else:
        currentIndex = 4
        p = 7

    while True:
        old_p = p
        p = getNextPrime( p )
        currentIndex += 1

        if p > target:
            return currentIndex - 1, old_p

@oneArgFunctionEvaluator( )
def findPrimeOperator( n ):
    return findPrime( n )[ 0 ]


# //******************************************************************************
# //
# //  findQuadrupletPrimes
# //
# //******************************************************************************

def findQuadrupletPrimes( arg ):
    n = int( real_int( arg ) )

    if n < 5:
        return 1, [ 5, 7, 11, 13 ]
    elif n < 11:
        return 2, [ 11, 13, 17, 19 ]

    openPrimeCache( 'quad_primes' )

    currentIndex, p = g.cursors[ 'quad_primes' ].execute(
        '''SELECT id, max( value ) FROM cache WHERE value <= ?''', ( n, ) ).fetchone( )

    while True:
        p += 30

        if isPrimeNumber( p ) and isPrimeNumber( p + 2 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 8 ):
            currentIndex += 1

            if p > n:
                return currentIndex, [ p, p + 2, p + 6, p + 8 ]

@oneArgFunctionEvaluator( )
def findQuadrupletPrimeOperator( n ):
    return findQuadrupletPrimes( n )[ 0 ]

@oneArgFunctionEvaluator( )
def getNextQuadrupletPrime( n ):
    return findQuadrupletPrimes( n )[ 1 ]


# //******************************************************************************
# //
# //  getNthQuadrupletPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthQuadrupletPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 11

    if g.primeDataAvailable and n >= 10:
        openPrimeCache( 'quad_primes' )

        maxIndex = g.cursors[ 'quad_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace, p = g.cursors[ 'quad_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        startingPlace = 2
        p = 11

    # after 5, the first of a prime quadruplet must be a number of the form 30n + 11
    while n > startingPlace:
        p += 30

        if isPrimeNumber( p ) and isPrimeNumber( p + 2 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 8 ):
            n -= 1

    return p


# //******************************************************************************
# //
# //  getNthIsolatedPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthIsolatedPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 23
    elif n >= 1000:
        openPrimeCache( 'isolated_primes' )

        currentIndex, p = g.cursors[ 'isolated_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 2
        p = 23

    while n > currentIndex:
        p = getNextPrime( p )

        if not isPrimeNumber( p - 2 ) and not isPrimeNumber( p + 2 ):
            currentIndex += 1

    return p


# //******************************************************************************
# //
# //  getNextTwinPrimeCandidate
# //
# //  Looking at ( p - 10 ) mod 30, the only twin prime candidates are 1, 7,
# //  and 19.
# //
# //******************************************************************************

def getNextTwinPrimeCandidate( p ):
    f = ( p - 10 ) % 30

    if f == 1:
        p += 6
    elif f == 7:
        p += 12
    else:  # f == 19
        p += 12

    return p


# //******************************************************************************
# //
# //  getNthTwinPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTwinPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif n == 2:
        return 5
    elif n == 3:
        return 11

    if g.primeDataAvailable and n >= 100:
        openPrimeCache( 'twin_primes' )

        maxIndex = g.cursors[ 'twin_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'twin_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 3
        p = 11

    while n > currentIndex:
        p = getNextPrime( p, getNextTwinPrimeCandidate )

        if isPrimeNumber( p + 2 ):
            currentIndex += 1

    return p


# //******************************************************************************
# //
# //  getNthTwinPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTwinPrimeList( arg ):
    p = getNthTwinPrime( arg )
    return [ p, fadd( p, 2 ) ]


# //******************************************************************************
# //
# //  getNthBalancedPrime
# //
# //  returns the first of a set of 3 balanced primes
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthBalancedPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif n == 2:
        return 5
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'balanced_primes' )

        maxIndex = g.cursors[ 'balanced_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'balanced_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
        prevPrime = 0
        secondPrevPrime = 0
    else:
        currentIndex = 2
        p = 11
        prevPrime = 7
        secondPrevPrime = 5

    while n > currentIndex:
        p = getNextPrime( p )

        if ( prevPrime - secondPrevPrime ) == ( p - prevPrime ):
            currentIndex += 1

        if n > currentIndex:
            secondPrevPrime = prevPrime
            prevPrime = p

    return secondPrevPrime


# //******************************************************************************
# //
# //  getNthBalancedPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthBalancedPrimeList( arg ):
    p = getNthBalancedPrime( arg )
    q = getNextPrime( p )
    r = getNextPrime( q )

    return [ p, q, r ]


# //******************************************************************************
# //
# //  getNthDoubleBalancedPrimeElement
# //
# //******************************************************************************

def getNthDoubleBalancedPrimeElement( arg, first = False ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 18713

    primes = [ ]

    if g.primeDataAvailable:
        openPrimeCache( 'double_balanced_primes' )

        maxIndex = g.cursors[ 'double_balanced_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )
        currentIndex, p = g.cursors[ 'double_balanced_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        if n > 50:
            sys.stderr.write( 'The prime number cache data is not available.  This could take some time...\n' );

        # no cache... we'll do this the hard way
        currentIndex = 1
        p = 18713

    primes = [ p ]

    for i in range( 0, 4 ):
        p = getNextPrime( p )
        primes.append( p )

    while n > currentIndex:
        p = getNextPrime( p )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 3 ] - primes[ 2 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 4 ] - primes[ 3 ] ) ):
            currentIndex += 1

    result = primes[ 0 ] if first else primes[ 2 ]

    return result


# //******************************************************************************
# //
# //  getNthDoubleBalancedPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDoubleBalancedPrimeList( arg ):
    p = getNthDoubleBalancedPrimeElement( arg, first = True )
    result = [ p ]

    for i in range( 0, 4 ):
        p = getNextPrime( p )
        result.append( p )

    return result

@oneArgFunctionEvaluator( )
def getNthDoubleBalancedPrime( arg ):
    return getNthDoubleBalancedPrimeElement( arg )


# //******************************************************************************
# //
# //  getNthTripleBalancedPrimeElement
# //
# //******************************************************************************

def getNthTripleBalancedPrimeElement( arg, first = False ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 683747

    if g.primeDataAvailable:
        openPrimeCache( 'triple_balanced_primes' )

        maxIndex = g.cursors[ 'triple_balanced_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'triple_balanced_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        if n > 10:
            sys.stderr.write( 'The prime number cache data is not available.  This could take some time...\n' );

        # no cache... we'll do this the hard way
        currentIndex = 1
        p = 683747

    primes = [ p ]

    for i in range( 0, 6 ):
        p = getNextPrime( p )
        primes.append( p )

    while n > currentIndex:
        p = getNextPrime( p )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 3 ] - primes[ 2 ] ) == ( primes[ 4 ] - primes[ 3 ] ) and
             ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 5 ] - primes[ 4 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 6 ] - primes[ 5 ] ) ):
            currentIndex += 1

    result = primes[ 0 ] if first else primes[ 3 ]

    return result


# //******************************************************************************
# //
# //  getNthTripleBalancedPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTripleBalancedPrimeList( arg ):
    p = getNthTripleBalancedPrimeElement( arg, first = True )
    result = [ p ]

    for i in range( 0, 6 ):
        p = getNextPrime( p )
        result.append( p )

    return result


@oneArgFunctionEvaluator( )
def getNthTripleBalancedPrime( arg ):
    return getNthTripleBalancedPrimeElement( arg )


# //******************************************************************************
# //
# //  getNthSophiePrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSophiePrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 3
    elif n == 3:
        return 5

    if g.primeDataAvailable and n >= 100:
        openPrimeCache( 'sophie_primes' )

        maxIndex = g.cursors[ 'sophie_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'sophie_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 4
        p = 11

    while n > currentIndex:
        p = getNextPrime( p )

        if isPrimeNumber( 2 * p + 1 ):
            currentIndex += 1

    return p

@oneArgFunctionEvaluator( )
def getSafePrime( n ):
    return fadd( fmul( getNthSophiePrime( n ), 2 ), 1 )


# //******************************************************************************
# //
# //  getNthCousinPrime
# //
# //  http://oeis.org/A023200
# //
# //  Validate: rpn 1 52 range cousin 23200 oeis  -
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCousinPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'cousin_primes' )

        maxIndex = g.cursors[ 'cousin_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'cousin_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 2
        p = 7

    while n > currentIndex:
        p = getNextPrime( p )

        if isPrimeNumber( p + 4 ):
            currentIndex += 1

    return p


# //******************************************************************************
# //
# //  getNthCousinPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCousinPrimeList( arg ):
    p = getNthCousinPrime( arg )
    return [ p, fadd( p, 4 ) ]


# //******************************************************************************
# //
# //  getNextSexyPrimeCandidate
# //
# //  For a number ( p - 10 ) mod 30, the only sexy candidates are 1, 3, 7, 13,
# //  21 and 27.
# //
# //******************************************************************************

def getNextSexyPrimeCandidate( p ):
    f = ( p - 10 ) % 30

    if f == 1:
        p += 2
    elif f == 3:
        p += 4
    elif f == 7:
        p += 6
    elif f == 13:
        p += 8
    elif f == 21:
        p += 6
    else:   # f == 27
        p += 4

    return p


# //******************************************************************************
# //
# //  getNthSexyPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'sexy_primes' )

        maxIndex = g.cursors[ 'sexy_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace, p = g.cursors[ 'sexy_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        startingPlace = 2
        p = 7

    while n > startingPlace:
        p = getNextPrime( p, getNextSexyPrimeCandidate )

        if isPrimeNumber( p + 6 ):
            n -= 1

    return p


# //******************************************************************************
# //
# //  getNthSexyPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyPrimeList( arg ):
    p = getNthSexyPrime( arg )
    return [ p, fadd( p, 6 ) ]


# //******************************************************************************
# //
# //  getNthSexyTriplet
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyTriplet( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 7
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'sexy_triplets' )

        maxIndex = g.cursors[ 'sexy_triplets' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace, p = g.cursors[ 'sexy_triplets' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        startingPlace = 2
        p = 7

    f = p % 10

    while n > startingPlace:
        if f == 1:
            p += 6
            f = 7
        else:
            p += 4
            f = 1

        if isPrimeNumber( p ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 12 ):
            n -= 1

    return p


# //******************************************************************************
# //
# //  getNthSexyTripletList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyTripletList( arg ):
    p = getNthSexyTriplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ) ]


# //******************************************************************************
# //
# //  getNthSexyQuadruplet
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyQuadruplet( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n < 100:
        startingPlace = 2
        p = 11
    elif g.primeDataAvailable and n >= 100:
        openPrimeCache( 'sexy_quadruplets' )

        maxIndex = g.cursors[ 'sexy_quadruplets' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace, p = g.cursors[ 'sexy_quadruplets' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )

    ten = True

    while n > startingPlace:
        if ten:
            p += 10
            ten = False
        else:
            p += 20
            ten = True

        if isPrimeNumber( p ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 12 ) and isPrimeNumber( p + 18 ):
            n -= 1

    return p


# //******************************************************************************
# //
# //  getNthSexyQuadrupletList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSexyQuadrupletList( arg ):
    p = getNthSexyQuadruplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ), fadd( p, 18 ) ]


# //******************************************************************************
# //
# //  getNthTripletPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTripletPrimeList( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return [ 5, 7, 11 ]
    elif n == 2:
        return [ 7, 11, 13 ]

    if g.primeDataAvailable and n >= 100:
        openPrimeCache( 'triplet_primes' )

        maxIndex = g.cursors[ 'triplet_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'triplet_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 3
        p = 11

    f = p % 10

    pPlus2 = False

    while n > currentIndex:
        if f == 1:
            p += 2
            f = 3
        elif f == 3:
            p += 4
            f = 7
        else:
            p += 4
            f = 1

        if isPrimeNumber( p ) and isPrimeNumber( p + 6 ):
            if isPrimeNumber( p + 2 ):
                pPlus2 = True
                currentIndex += 1
            elif isPrimeNumber( p + 4 ):
                pPlus2 = False
                currentIndex += 1

    return [ p, p + 2 if pPlus2 else p + 4, p + 6 ]


# //******************************************************************************
# //
# //  getNthTripletPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTripletPrime( arg ):
    return getNthTripletPrimeList( arg )[ 0 ]


# //******************************************************************************
# //
# //  getNextQuintupletPrimeCandidate
# //
# //  For ( p - 10 ) mod 30, the only quintuplet prime candidates are:
# //  1, 7, 21, or 27
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNextQuintupletPrimeCandidate( p ):
    f = ( p - 10 ) % 30

    if f == 1:
        p += 6
    elif f == 7:
        p += 14
    elif f == 21:
        p += 6
    else:  # f == 27
        p += 4

    return p


# //******************************************************************************
# //
# //  getNthQuadrupletPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthQuadrupletPrimeList( arg ):
    p = getNthQuadrupletPrime( arg )
    return [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ) ]


# //******************************************************************************
# //
# //  getNthQuintupletPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthQuintupletPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 7

    if g.primeDataAvailable and n >= 10:
        openPrimeCache( 'quint_primes' )

        maxIndex = g.cursors[ 'quint_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex, p = g.cursors[ 'quint_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        currentIndex = 3
        p = 11

    # after 5, the first of a prime quintruplet must be a number of the form 30n + 11
    while n > currentIndex:
        p = getNextPrime( p, getNextQuintupletPrimeCandidate )

        f = ( p - 10 ) % 30

        if ( ( f == 1 ) and isPrimeNumber( p + 2 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 8 ) and isPrimeNumber( p + 12 ) ) or \
           ( ( f == 7 ) and isPrimeNumber( p + 4 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 10 ) and isPrimeNumber( p + 12 ) ):
            currentIndex += 1

    return p


# //******************************************************************************
# //
# //  getNthQuintupletPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthQuintupletPrimeList( arg ):
    if arg == 1:
        return [ 5, 7, 11, 13, 17 ]

    p = getNthQuintupletPrime( arg )

    f = p % 10

    if f == 1:
        return [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ), fadd( p, 12 ) ]
    elif f == 7:
        return [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ) ]
    else:
        raise ValueError( 'internal error:  getNthQuintupletPrimeList is broken' )


# //******************************************************************************
# //
# //  findQuintupletPrimes
# //
# //******************************************************************************

def findQuintupletPrimes( arg ):
    n = int( real_int( arg ) )

    if n < 5:
        return 1, [ 5, 7, 11, 13, 17 ]
    elif n < 7:
        return 2, [ 7, 11, 13, 17, 19 ]

    if g.primeDataAvailable:
        openPrimeCache( 'quint_primes' )

        currentIndex, p = g.cursors[ 'quint_primes' ].execute(
            '''SELECT id, max( value ) FROM cache WHERE value <= ?''', ( n, ) ).fetchone( )
    else:
        currentIndex = 3
        p = 11

    while True:
        p += 30

        f = p % 10

        if ( ( f == 1 ) and isPrimeNumber( p + 2 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 8 ) and isPrimeNumber( p + 12 ) ) or \
           ( ( f == 7 ) and isPrimeNumber( p + 4 ) and isPrimeNumber( p + 6 ) and isPrimeNumber( p + 10 ) and isPrimeNumber( p + 12 ) ):
            currentIndex += 1

            if p > n:
                if f == 1:
                    return currentIndex, [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ), fadd( p, 12 ) ]
                elif f == 7:
                    return currentIndex, [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ) ]

@oneArgFunctionEvaluator( )
def findQuintupletPrimeOperator( n ):
    return findQuintupletPrimes( n )[ 0 ]

@oneArgFunctionEvaluator( )
def getNextQuintupletPrime( n ):
    return findQuintupletPrimes( n )[ 1 ]



# //******************************************************************************
# //
# //  getNthSextupletPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSextupletPrime( arg ):
    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 7
    elif g.primeDataAvailable and n >= 10:
        openPrimeCache( 'sext_primes' )

        maxIndex = g.cursors[ 'sext_primes' ].execute(
            '''SELECT MAX( id ) FROM cache''' ).fetchone( )[ 0 ]

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace, p = g.cursors[ 'sext_primes' ].execute(
            '''SELECT MAX( id ), value FROM cache WHERE id <= ?''', ( int( n ), ) ).fetchone( )
    else:
        startingPlace = 1
        p = 7

    # all sets of prime sextuplets must start with 30x+7
    while n > startingPlace:
        p += 30

        if isPrimeNumber( p ) and isPrimeNumber( p + 4 ) and isPrimeNumber( p + 6 ) and \
           isPrimeNumber( p + 10 ) and isPrimeNumber( p + 12 ) + isPrimeNumber( p + 16 ):
            n -= 1

    return p


# //******************************************************************************
# //
# //  getNthSextupletPrimeList
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSextupletPrimeList( arg ):
    p = getNthSextupletPrime( arg )
    return [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ), fadd( p, 16 ) ]


# //******************************************************************************
# //
# //  getNthPrimeRange
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthPrimeRange( arg1, arg2 ):
    n = int( real_int( arg1 ) )
    count = int( real_int( arg2 ) )

    if count < 1:
        return [ ]

    # for primes below 7, we have to do it manually
    if n == 1:
        if count == 1:
            return [ 2 ]
        elif count == 2:
            return[ 2, 3 ]
        elif count == 3:
            return [ 2, 3, 5 ]
        else:
            result = [ 2, 3, 5, 7 ]
            count -= 3
            p = 7
    elif n == 2:
        if count == 1:
            return [ 3 ]
        elif count == 2:
            return [ 3, 5 ]
        else:
            result = [ 3, 5, 7 ]
            count -= 2
            p = 7
    elif n == 3:
        if count == 1:
            return [ 5 ]
        else:
            result = [ 5, 7 ]
            count -= 1
            p = 7
    else:
        p = getNthPrime( n )
        result = [ p ]

    found = 1

    while found < count:
        p = getNextPrimeCandidateForAny( p )

        if isPrimeNumber( p ):
            result.append( p )
            found += 1

    return result


# //******************************************************************************
# //
# //  getNthSuperPrime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSuperPrime( arg ):
    return getNthPrime( getNthPrime( arg ) )


# //******************************************************************************
# //
# //  getNthPolyPrime
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthPolyPrime( n, poly ):
    result = getNthPrime( n )

    for i in arange( 1, poly ):
        result = getNthPrime( result )

    return result


# //******************************************************************************
# //
# //  getPrimes
# //
# //******************************************************************************

def getPrimes( value, count ):
    for i in getNthPrimeRange( value, count ):
        yield i

@twoArgFunctionEvaluator( )
def getPrimesGenerator( n, k ):
    return RPNGenerator( getPrimes( n, k ) )


# //******************************************************************************
# //
# //  getPrimeRange
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getPrimeRange( start, end ):
    result = list( )

    for i in getNthPrimeRange( start, fadd( fsub( end, start ), 1 ) ):
        result.append( i )

    return result


# //******************************************************************************
# //
# //  getNthPrimorial
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPrimorial( n ):
    if real_int( n ) == 0:
        return 1

    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result


# //******************************************************************************
# //
# //  countCache
# //
# //******************************************************************************

def countCache( name ):
    openPrimeCache( name )
    return g.cursors[ name ].execute( '''SELECT count( id ) FROM cache''' ).fetchone( )[ 0 ]


# //******************************************************************************
# //
# //  getMaxPrime
# //
# //******************************************************************************

def getMaxPrime( name ):
    openPrimeCache( name )
    return g.cursors[ name ].execute( '''SELECT max( id ), value FROM cache''' ).fetchone( )


# //******************************************************************************
# //
# //  printStats
# //
# //******************************************************************************

def printStats( cacheName, name ):
    count = countCache( cacheName )
    key, value = getMaxPrime( cacheName )

    print( '{:10,} {:23} max: {:14,} ({:,})'.format( count, name, key, value ) )


# //******************************************************************************
# //
# //  miller_rabin_pass
# //
# //  https://gist.github.com/sharnett/5479106
# //
# //******************************************************************************

def miller_rabin_pass( a, s, d, n ):
    a_to_power = pow( a, d, n )

    if a_to_power == 1:
        return True

    for i in range( s - 1 ):
        if a_to_power == n - 1:
            return True

        a_to_power = ( a_to_power * a_to_power ) % n

    return a_to_power == n - 1


# //******************************************************************************
# //
# //  isPrimeMillerRabin
# //
# //  https://gist.github.com/sharnett/5479106
# //  http://mathworld.wolfram.com/StrongPseudoprime.html
# //
# //  http://pi-e.de/Miller-Rabin-Pseudoprimzahlen.htm - check this out!
# //
# //******************************************************************************

def isPrimeMillerRabin( n ):
    if n < 2:
        return False

    if n < 2047:
        testPrimes = [ 2 ]
    elif n < 1373653:
        testPrimes = [ 2, 3 ]
    elif n < 9080191:
        testPrimes = [ 31, 73 ]
    elif n < 4759123141:
        testPrimes = [ 2, 7, 61 ]
    elif n < 2152302898747:
        testPrimes = [ 2, 3, 5, 7, 11 ]
    elif n < 3474749660383:
        testPrimes = [ 2, 3, 5, 7, 11, 13 ]
    elif n < 341550071728321:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17 ]
    elif n < 18446744073709551616:
        testPrimes = [ 2, 325, 9375, 28178, 450775, 9780504, 1795265022 ]
    elif n < 318665857834031151167461:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37 ]
    elif n < 3317044064679887385961981:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41 ]
    elif n < 6003094289670105800312596501 and g.zhangConjecturesAllowed:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43 ]
    elif n < 59276361075595573263446330101 and g.zhangConjecturesAllowed:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 ]
    elif n < 564132928021909221014087501701 and g.zhangConjecturesAllowed:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59 ]
    elif n < 1543267864443420616877677640751301 and g.zhangConjecturesAllowed:
        testPrimes = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67 ]
    else:
        if g.zhangConjecturesAllowed:
            raise ValueError( str( n ) + ' is too large to use the deterministic Miller-Rabin test for 19 prime bases' )
        else:
            raise ValueError( str( n ) + ' is too large to use the deterministic Miller-Rabin test for 13 prime bases' )

    if n in testPrimes:
        return True

    d = n - 1
    s = 0

    while d % 2 == 0:
        d >>= 1
        s += 1

    for a in testPrimes:
        if not miller_rabin_pass( a, s, d, n ):
            return False

    return True


# //******************************************************************************
# //
# //  isStrongPseudoprime
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isStrongPseudoprime( n, k ):
    if n < k or fmod( n, 2 ) == 0 or isPrime( n ):
        return 0

    d = int( n - 1 )
    s = 0

    while d % 2 == 0:
        d >>= 1
        s += 1

    return 1 if miller_rabin_pass( int( k ), s, d, int( n ) ) else 0


# //******************************************************************************
# //
# //  checkForPrimeData
# //
# //******************************************************************************

def checkForPrimeData( ):
    primeFile = Path( getDataPath( ) + os.sep + 'large_primes.cache' )

    if primeFile.is_file( ):
        g.primeDataAvailable = True
    else:
        g.primeDataAvailable = False

