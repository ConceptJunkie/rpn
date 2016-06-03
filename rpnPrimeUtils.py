#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPrimeUtils.py
# //
# //  RPN command-line calculator prime number utilies
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import contextlib
import os
import pickle
import pyprimes
import sys

from mpmath import arange, fadd, fmul

import rpnGlobals as g

from rpnUtils import real_int


# //******************************************************************************
# //
# //  globals
# //
# //******************************************************************************

updateDicts = False

balancedPrimes = { }
cousinPrimes = { }
doubleBalancedPrimes = { }
hugePrimes = { }
isolatedPrimes = { }
largePrimes = { }
quadPrimes = { }
quintPrimes = { }
sextPrimes = { }
sexyPrimes = { }
sexyQuadruplets = { }
sexyTriplets = { }
smallPrimes = { }
sophiePrimes = { }
superPrimes = { }
tripleBalancedPrimes = { }
tripletPrimes = { }
twinPrimes = { }


# //******************************************************************************
# //
# //  loadTable
# //
# //******************************************************************************

def loadTable( dataPath, fileName, default ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'rb' ) ) as pickleFile:
            primes = pickle.load( pickleFile )
    except FileNotFoundError:
        primes = default

    return primes


def loadBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'balanced_primes', { 2 : 5 } )


def loadCousinPrimes( dataPath ):
    return loadTable( dataPath, 'cousin_primes', { 2 : 7 } )


def loadDoubleBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'double_balanced_primes', { 1 : getNthDoubleBalancedPrime( 1 ) } )


def loadHugePrimes( dataPath ):
    return loadTable( dataPath, 'huge_primes', { 1000000000: 22801763489 } )


def loadIsolatedPrimes( dataPath ):
    return loadTable( dataPath, 'isolated_primes', { 2 : 23 } )


def loadLargePrimes( dataPath ):
    return loadTable( dataPath, 'large_primes', { 1000000 : 15485863 } )


def loadQuadrupletPrimes( dataPath ):
    return loadTable( dataPath, 'quad_primes', { 2 : 11 } )


def loadQuintupletPrimes( dataPath ):
    return loadTable( dataPath, 'quint_primes', { 3 : 11 } )


def loadSextupletPrimes( dataPath ):
    return loadTable( dataPath, 'sext_primes', { 1 : 7 } )


def loadSexyPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_primes', { 2 : 7 } )


def loadSexyQuadrupletPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_quadruplets', { 2 : 11 } )


def loadSexyTripletPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_triplets', { 2 : 7 } )


def loadSmallPrimes( dataPath ):
    return loadTable( dataPath, 'small_primes', { 4 : 7 } )


def loadSophiePrimes( dataPath ):
    return loadTable( dataPath, 'sophie_primes', { 4 : 11 } )


def loadTripleBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'triple_balanced_primes', { 1 : getNthTripleBalancedPrime( 1 ) } )


def loadTripletPrimes( dataPath ):
    return loadTable( dataPath, 'triplet_primes', { 2 : 7 } )


def loadTwinPrimes( dataPath ):
    return loadTable( dataPath, 'twin_primes', { 3 : 11 } )


# //******************************************************************************
# //
# //  isPrime
# //
# //******************************************************************************

def isPrime( arg ):
    return pyprimes.isprime( int( arg ) )


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

# rpn 10 219 range x 7 is_div unfilter x 5 is_div unfilter x 3 is_div unfilter x 2 is_div unfilter
#
# [ 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
# 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149,
# 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 209, 211 ]


# //******************************************************************************
# //
# //  getNextPrimeCandidate
# //
# //******************************************************************************

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
# //  We only need to check for a prime if ( p - 10 ) mod 210 is 1, 3, 7, 9, 13, 19,
# //  21, 27 31, 33, 37, 43, 49, 51, 57, 61, 63, 69, 73, 79, 87, 91, 93, 97, 99,
# //  103, 117, 121, 127, 129, 139, 141, 147, 153, 157, 163, 169, 171, 181, 183,
# //  187, 189, or 201.
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
        103 : 14, 104 : 13, 105 : 12, 106 : 11, 107 : 10, 108 : 9, 109 : 8, 110 : 7, 111 : 6, 112 : 5, 113 : 4, 114 : 3, 115 : 2, 116 : 1,
        117 : 4, 118 : 3, 119 : 2, 120 : 1,
        121 : 6, 122 : 5, 123 : 4, 124 : 3, 125 : 2, 126 : 1,
        127 : 2, 128 : 1,
        129 : 10, 130 : 9, 131 : 8, 132 : 7, 133 : 6, 134 : 5, 135 : 4, 136 : 3, 137 : 2, 138 : 1,
        139 : 2, 140 : 1,
        141 : 6, 142 : 5, 143 : 4, 144 : 3, 145 : 2, 146 : 1,
        147 : 6, 148 : 5, 149 : 4, 150 : 3, 151 : 2, 152 : 1,
        153 : 4, 154 : 3, 155 : 2, 156 : 1,
        157 : 6, 158 : 5, 159 : 4, 160 : 3, 161 : 2, 162 : 1,
        163 : 6, 164 : 5, 165 : 4, 166 : 3, 167 : 2, 168 : 1,
        169 : 2, 170 : 1,
        171 : 10, 172 : 9, 173 : 8, 174 : 7, 175 : 6, 176 : 5, 177 : 4, 178 : 3, 179 : 2, 180 : 1,
        181 : 2, 182 : 1,
        183 : 4, 184 : 3, 185 : 2, 186 : 1,
        187 : 2, 188 : 1,
        189 : 12, 190 : 11, 191 : 10, 192 : 9, 193 : 8, 194 : 7, 195 : 6, 196 : 5, 197 : 4, 198 : 3, 199 : 2, 200 : 1,
        201 : 10, 202 : 9, 203 : 8, 204 : 7, 205 : 6, 206 : 5, 207 : 4, 208 : 3, 209 : 2
    }

    return p + moduloTable[ f ]


# //******************************************************************************
# //
# //  getNextPrime
# //
# //******************************************************************************

def getNextPrime( p, func = getNextPrimeCandidate ):
    p = func( p )

    while not isPrime( p ):
        p = func( p )

    return p


# //******************************************************************************
# //
# //  getNthPrime
# //
# //******************************************************************************

def getNthPrime( arg ):
    global smallPrimes
    global largePrimes
    global hugePrimes
    global updateDicts

    n = int( arg )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 3
    elif n == 3:
        return 5
    elif n >= 1000000000:
        if hugePrimes == { }:
            hugePrimes = loadHugePrimes( g.dataPath )

        maxIndex = max( key for key in hugePrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in hugePrimes if key <= n )
        p = hugePrimes[ currentIndex ]
    elif n >= 1000000:
        if largePrimes == { }:
            largePrimes = loadLargePrimes( g.dataPath )

        currentIndex = max( key for key in largePrimes if key <= n )
        p = largePrimes[ currentIndex ]
    elif n >= 100:
        if smallPrimes == { }:
            smallPrimes = loadSmallPrimes( g.dataPath )

        currentIndex = max( key for key in smallPrimes if key <= n )
        p = smallPrimes[ currentIndex ]
    else:
        currentIndex = 4
        p = 7

    while n > currentIndex:
        p = getNextPrime( p )
        currentIndex += 1

    if updateDicts:
        if n >= 1000000:
            largePrimes[ n ] = p
        else:
            smallPrimes[ n ] = p

    return p


# //******************************************************************************
# //
# //  findPrime
# //
# //******************************************************************************

def findPrime( arg ):
    global smallPrimes
    global largePrimes
    global hugePrimes

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
    elif target < 15485863:     # 1,000,000th prime
        if smallPrimes == { }:
            smallPrimes = loadSmallPrimes( g.dataPath )

        currentIndex = max( key for key in smallPrimes if smallPrimes[ key ] <= target )
        p = smallPrimes[ currentIndex ]
    elif target < 22801763489:  # 1,000,000,000th prime
        if largePrimes == { }:
            largePrimes = loadLargePrimes( g.dataPath )

        currentIndex = max( key for key in largePrimes if largePrimes[ key ] <= target )
        p = largePrimes[ currentIndex ]
    else:
        if hugePrimes == { }:
            hugePrimes = loadHugePrimes( g.dataPath )

        currentIndex = max( key for key in hugePrimes if hugePrimes[ key ] <= target )
        p = hugePrimes[ currentIndex ]

    while True:
        p = getNextPrime( p )
        currentIndex += 1

        if p >= target:
            return currentIndex, p


# //******************************************************************************
# //
# //  findQuadrupletPrimes
# //
# //******************************************************************************

def findQuadrupletPrimes( arg ):
    global quadPrimes

    n = int( real_int( arg ) )

    if n < 5:
        return 1, [ 5, 7, 11, 13 ]
    elif n < 11:
        return 2, [ 11, 13, 17, 19 ]

    if quadPrimes == { }:
        quadPrimes = loadQuadrupletPrimes( g.dataPath )

    currentIndex = max( key for key in quadPrimes if quadPrimes[ key ] <= n )
    p = quadPrimes[ currentIndex ]

    while True:
        p += 30

        if isPrime( p ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ):
            currentIndex += 1

            if p > n:
                return currentIndex, [ p, p + 2, p + 6, p + 8 ]


# //******************************************************************************
# //
# //  getNthQuadrupletPrime
# //
# //******************************************************************************

def getNthQuadrupletPrime( arg ):
    global quadPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 11

    if n >= 10:
        if quadPrimes == { }:
            quadPrimes = loadQuadrupletPrimes( g.dataPath )

        maxIndex = max( key for key in quadPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace = max( key for key in quadPrimes if key <= n )
        p = quadPrimes[ startingPlace ]
    else:
        startingPlace = 2
        p = 11

    # after 5, the first of a prime quadruplet must be a number of the form 30n + 11
    while n > startingPlace:
        p += 30

        if isPrime( p ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ):
            n -= 1

    if updateDicts:
        quadPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthIsolatedPrime
# //
# //******************************************************************************

def getNthIsolatedPrime( arg ):
    global isolatedPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 23
    elif n >= 1000:
        if isolatedPrimes == { }:
            isolatedPrimes = loadIsolatedPrimes( g.dataPath )

        currentIndex = max( key for key in isolatedPrimes if key <= n )
        p = isolatedPrimes[ currentIndex ]
    else:
        currentIndex = 2
        p = 23

    while n > currentIndex:
        p = getNextPrime( p )

        if not isPrime( p - 2 ) and not isPrime( p + 2 ):
            currentIndex += 1

    if updateDicts:
        isolatedPrimes[ n ] = p

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

def getNthTwinPrime( arg ):
    global twinPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif n == 2:
        return 5
    elif n == 3:
        return 11

    if n >= 100:
        if twinPrimes == { }:
            twinPrimes = loadTwinPrimes( g.dataPath )

        maxIndex = max( key for key in twinPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in twinPrimes if key <= n )
        p = twinPrimes[ currentIndex ]
    else:
        currentIndex = 3
        p = 11

    while n > currentIndex:
        p = getNextPrime( p, getNextTwinPrimeCandidate )

        if isPrime( p + 2 ):
            currentIndex += 1

    if updateDicts:
        twinPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthTwinPrimeList
# //
# //******************************************************************************

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

def getNthBalancedPrime( arg ):
    global balancedPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif n == 2:
        return 5
    elif n >= 100:
        if balancedPrimes == { }:
            balancedPrimes = loadBalancedPrimes( g.dataPath )

        maxIndex = max( key for key in balancedPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in balancedPrimes if key < n )
        p = balancedPrimes[ currentIndex ]
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

    if updateDicts:
        balancedPrimes[ int( arg ) ] = secondPrevPrime

    return secondPrevPrime


# //******************************************************************************
# //
# //  getNthBalancedPrimeList
# //
# //******************************************************************************

def getNthBalancedPrimeList( arg ):
    p = getNthBalancedPrime( arg )
    q = getNextPrime( p )
    r = getNextPrime( q )

    return [ p, q, r ]


# //******************************************************************************
# //
# //  getNthDoubleBalancedPrime
# //
# //******************************************************************************

def getNthDoubleBalancedPrime( arg, first = False ):
    global doubleBalancedPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 18713

    if doubleBalancedPrimes == { }:
        doubleBalancedPrimes = loadDoubleBalancedPrimes( g.dataPath )

    maxIndex = max( key for key in doubleBalancedPrimes )

    if n > maxIndex and not updateDicts:
        sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                          format( n, maxIndex ) )

    currentIndex = max( key for key in doubleBalancedPrimes if key <= n )
    primes = [ ]

    p = doubleBalancedPrimes[ currentIndex ]

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

    if updateDicts:
        doubleBalancedPrimes[ n ] = result

    return result


# //******************************************************************************
# //
# //  getNthDoubleBalancedPrimeList
# //
# //******************************************************************************

def getNthDoubleBalancedPrimeList( arg ):
    p = getNthDoubleBalancedPrime( arg, first = True )
    result = [ p ]

    for i in range( 0, 4 ):
        p = getNextPrime( p )
        result.append( p )

    return result


# //******************************************************************************
# //
# //  getNthTripleBalancedPrime
# //
# //******************************************************************************

def getNthTripleBalancedPrime( arg, first = False ):
    global tripleBalancedPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 683747

    if tripleBalancedPrimes == { }:
        tripleBalancedPrimes = loadTripleBalancedPrimes( g.dataPath )

    maxIndex = max( key for key in tripleBalancedPrimes )

    if n > maxIndex and not updateDicts:
        sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                          format( n, maxIndex ) )

    currentIndex = max( key for key in tripleBalancedPrimes if key <= n )

    p = tripleBalancedPrimes[ currentIndex ]

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

    if updateDicts:
        tripleBalancedPrimes[ n ] = result

    return result


# //******************************************************************************
# //
# //  getNthTripleBalancedPrimeList
# //
# //******************************************************************************

def getNthTripleBalancedPrimeList( arg ):
    p = getNthTripleBalancedPrime( arg, first = True )
    result = [ p ]

    for i in range( 0, 6 ):
        p = getNextPrime( p )
        result.append( p )

    return result


# //******************************************************************************
# //
# //  getNthSophiePrime
# //
# //******************************************************************************

def getNthSophiePrime( arg ):
    global sophiePrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 2
    elif n == 2:
        return 3
    elif n == 3:
        return 5

    if n >= 100:
        if sophiePrimes == { }:
            sophiePrimes = loadSophiePrimes( g.dataPath )

        maxIndex = max( key for key in sophiePrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in sophiePrimes if key <= n )
        p = sophiePrimes[ currentIndex ]
    else:
        currentIndex = 4
        p = 11

    while n > currentIndex:
        p = getNextPrime( p )

        if isPrime( 2 * p + 1 ):
            currentIndex += 1

    if updateDicts:
        sophiePrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthCousinPrime
# //
# //  http://oeis.org/A023200
# //
# //  Validate: rpn 1 52 range cousin 23200 oeis  -
# //
# //******************************************************************************

def getNthCousinPrime( arg ):
    global cousinPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 3
    elif n >= 100:
        if cousinPrimes == { }:
            cousinPrimes = loadCousinPrimes( g.dataPath )

        maxIndex = max( key for key in cousinPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in cousinPrimes if key <= n )
        p = cousinPrimes[ currentIndex ]
    else:
        currentIndex = 2
        p = 7

    while n > currentIndex:
        p = getNextPrime( p )

        if isPrime( p + 4 ):
            currentIndex += 1

    if updateDicts:
        cousinPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthCousinPrimeList
# //
# //******************************************************************************

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

def getNthSexyPrime( arg ):
    global sexyPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n >= 100:
        if sexyPrimes == { }:
            sexyPrimes = loadSexyPrimes( g.dataPath )

        maxIndex = max( key for key in sexyPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace = max( key for key in sexyPrimes if key <= n )
        p = sexyPrimes[ startingPlace ]
    else:
        startingPlace = 2
        p = 7

    while n > startingPlace:
        p = getNextPrime( p, getNextSexyPrimeCandidate )

        if isPrime( p + 6 ):
            n -= 1

    if updateDicts:
        sexyPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthSexyPrimeList
# //
# //******************************************************************************

def getNthSexyPrimeList( arg ):
    p = getNthSexyPrime( arg )
    return [ p, fadd( p, 6 ) ]


# //******************************************************************************
# //
# //  getNthSexyTriplet
# //
# //******************************************************************************

def getNthSexyTriplet( arg ):
    global sexyTriplets
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 7
    elif n >= 100:
        if sexyTriplets == { }:
            sexyTriplets = loadSexyTripletPrimes( g.dataPath )

        maxIndex = max( key for key in sexyTriplets )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace = max( key for key in sexyTriplets if key <= n )
        p = sexyTriplets[ startingPlace ]
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

        if isPrime( p ) and isPrime( p + 6 ) and isPrime( p + 12 ):
            n -= 1

    if updateDicts:
        sexyTriplets[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthSexyTripletList
# //
# //******************************************************************************

def getNthSexyTripletList( arg ):
    p = getNthSexyTriplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ) ]


# //******************************************************************************
# //
# //  getNthSexyQuadruplet
# //
# //******************************************************************************

def getNthSexyQuadruplet( arg ):
    global sexyQuadruplets
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n < 100:
        startingPlace = 2
        p = 11
    elif n >= 100:
        if sexyQuadruplets == { }:
            sexyQuadruplets = loadSexyQuadrupletPrimes( g.dataPath )

            maxIndex = max( key for key in sexyQuadruplets )

            if n > maxIndex and not updateDicts:
                sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                  format( n, maxIndex ) )

        startingPlace = max( key for key in sexyQuadruplets if key <= n )
        p = sexyQuadruplets[ startingPlace ]

    ten = True

    while n > startingPlace:
        if ten:
            p += 10
            ten = False
        else:
            p += 20
            ten = True

        if isPrime( p ) and isPrime( p + 6 ) and isPrime( p + 12 ) and isPrime( p + 18 ):
            n -= 1

    if updateDicts:
        sexyQuadruplets[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthSexyQuadrupletList
# //
# //******************************************************************************

def getNthSexyQuadrupletList( arg ):
    p = getNthSexyQuadruplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ), fadd( p, 18 ) ]


# //******************************************************************************
# //
# //  getNthTripletPrimeList
# //
# //******************************************************************************

def getNthTripletPrimeList( arg ):
    global tripletPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return [ 5, 7, 11 ]
    elif n == 2:
        return [ 7, 11, 13 ]

    if n >= 100:
        if tripletPrimes == { }:
            tripletPrimes = loadTripletPrimes( g.dataPath )

        maxIndex = max( key for key in tripletPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in tripletPrimes if key <= n )
        p = tripletPrimes[ currentIndex ]
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

        if isPrime( p ) and isPrime( p + 6 ):
            if isPrime( p + 2 ):
                pPlus2 = True
                currentIndex += 1
            elif isPrime( p + 4 ):
                pPlus2 = False
                currentIndex += 1

    if updateDicts:
        tripletPrimes[ int( arg ) ] = p

    return [ p, p + 2 if pPlus2 else p + 4, p + 6 ]


# //******************************************************************************
# //
# //  getNthTripletPrime
# //
# //******************************************************************************

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

def getNthQuadrupletPrimeList( arg ):
    p = getNthQuadrupletPrime( arg )
    return [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ) ]


# //******************************************************************************
# //
# //  getNthQuintupletPrime
# //
# //******************************************************************************

def getNthQuintupletPrime( arg ):
    global quintPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 5
    elif n == 2:
        return 7

    if n >= 10:
        if quintPrimes == { }:
            quintPrimes = loadQuintupletPrimes( g.dataPath )

        maxIndex = max( key for key in quintPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        currentIndex = max( key for key in quintPrimes if key <= n )
        p = quintPrimes[ currentIndex ]
    else:
        currentIndex = 3
        p = 11

    # after 5, the first of a prime quintruplet must be a number of the form 30n + 11
    while n > currentIndex:
        p = getNextPrime( p, getNextQuintupletPrimeCandidate )

        f = ( p - 10 ) % 30

        if ( ( f == 1 ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ) and isPrime( p + 12 ) ) or \
           ( ( f == 7 ) and isPrime( p + 4 ) and isPrime( p + 6 ) and isPrime( p + 10 ) and isPrime( p + 12 ) ):
            currentIndex += 1

    if updateDicts:
        quintPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthQuintupletPrimeList
# //
# //******************************************************************************

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
    global quintPrimes

    n = int( real_int( arg ) )

    if n < 5:
        return 1, [ 5, 7, 11, 13, 17 ]
    elif n < 7:
        return 2, [ 7, 11, 13, 17, 19 ]

    if quintPrimes == { }:
        quintPrimes = loadQuintupletPrimes( g.dataPath )

    currentIndex = max( key for key in quintPrimes if quintPrimes[ key ] <= n )
    p = quintPrimes[ currentIndex ]

    while True:
        p += 30

        f = p % 10

        if ( ( f == 1 ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ) and isPrime( p + 12 ) ) or \
           ( ( f == 7 ) and isPrime( p + 4 ) and isPrime( p + 6 ) and isPrime( p + 10 ) and isPrime( p + 12 ) ):
            currentIndex += 1

            if p > n:
                if f == 1:
                    return currentIndex, [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ), fadd( p, 12 ) ]
                elif f == 7:
                    return currentIndex, [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ) ]


# //******************************************************************************
# //
# //  getNthSextupletPrime
# //
# //******************************************************************************

def getNthSextupletPrime( arg ):
    global sextPrimes
    global updateDicts

    n = int( real_int( arg ) )

    if n < 1:
        raise ValueError( 'index must be > 0' )
    elif n == 1:
        return 7
    elif n >= 10:
        if sextPrimes == { }:
            sextPrimes = loadSextupletPrimes( g.dataPath )

        maxIndex = max( key for key in sextPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

        startingPlace = max( key for key in sextPrimes if key <= n )
        p = sextPrimes[ startingPlace ]
    else:
        startingPlace = 1
        p = 7

    # all sets of prime sextuplets must start with 30x+7
    while n > startingPlace:
        p += 30

        if isPrime( p ) and isPrime( p + 4 ) and isPrime( p + 6 ) and \
           isPrime( p + 10 ) and isPrime( p + 12 ) + isPrime( 16 ):
            n -= 1

    if updateDicts:
        sextPrimes[ int( arg ) ] = p

    return p


# //******************************************************************************
# //
# //  getNthSextupletPrimeList
# //
# //******************************************************************************

def getNthSextupletPrimeList( arg ):
    p = getNthSextupletPrime( arg )
    return [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ), fadd( p, 16 ) ]


# //******************************************************************************
# //
# //  getNthPrimeRange
# //
# //******************************************************************************

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
        p = getNextPrimeCandidate( p )

        if isPrime( p ):
            result.append( p )
            found += 1

    return result


# //******************************************************************************
# //
# //  getNthSuperPrime
# //
# //******************************************************************************

def getNthSuperPrime( arg ):
    return getNthPrime( getNthPrime( arg ) )


# //******************************************************************************
# //
# //  getNthPolyPrime
# //
# //******************************************************************************

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
    result = list( )

    for i in getNthPrimeRange( value, count ):
        result.append( i )

    return result


# //******************************************************************************
# //
# //  getNthPrimorial
# //
# //******************************************************************************

def getNthPrimorial( n ):
    if real_int( n ) == 0:
        return 1

    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result

