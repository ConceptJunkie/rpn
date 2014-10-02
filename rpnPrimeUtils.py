#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnPrimeUtils.py
#//
#//  RPN command-line calculator prime number utilies
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import bz2
import contextlib
import os
import pickle
import pyprimes
import sys

import rpnGlobals as g

from mpmath import *


#//******************************************************************************
#//
#//  globals
#//
#//******************************************************************************

updateDicts = False

balancedPrimes = { }
cousinPrimes = { }
doubleBalancedPrimes = { }
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


#//******************************************************************************
#//
#//  loadTable
#//
#//******************************************************************************

def loadTable( dataPath, fileName, default ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'rb' ) ) as pickleFile:
            primes = pickle.load( pickleFile )
    except FileNotFoundError:
        primes = default

    return primes


def loadSmallPrimes( dataPath ):
    return loadTable( dataPath, 'small_primes', { 4 : 7 } )


def loadLargePrimes( dataPath ):
    return loadTable( dataPath, 'large_primes', { 1000000 : 15485863 } )


def loadIsolatedPrimes( dataPath ):
    return loadTable( dataPath, 'isolated_primes', { 2 : 23 } )


def loadTwinPrimes( dataPath ):
    return loadTable( dataPath, 'twin_primes', { 3 : 11 } )


def loadBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'balanced_primes', { 2 : 5 } )


def loadDoubleBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'double_balanced_primes', { 1 : getNthDoubleBalancedPrime( 1 ) } )


def loadTripleBalancedPrimes( dataPath ):
    return loadTable( dataPath, 'triple_balanced_primes', { 1 : getNthTripleBalancedPrime( 1 ) } )


def loadSophiePrimes( dataPath ):
    return loadTable( dataPath, 'sophie_primes', { 4 : 11 } )


def loadCousinPrimes( dataPath ):
    return loadTable( dataPath, 'cousin_primes', { 2 : 7 } )


def loadSexyPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_primes', { 2 : 7 } )


def loadSexyTripletPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_triplets', { 2 : 7 } )


def loadSexyQuadrupletPrimes( dataPath ):
    return loadTable( dataPath, 'sexy_quadruplets', { 2 : 11 } )


def loadTripletPrimes( dataPath ):
    return loadTable( dataPath, 'triplet_primes', { 2 : 7 } )


def loadQuadrupletPrimes( dataPath ):
    return loadTable( dataPath, 'quad_primes', { 2 : 11 } )


def loadQuintupletPrimes( dataPath ):
    return loadTable( dataPath, 'quint_primes', { 3 : 11 } )


def loadSextupletPrimes( dataPath ):
    return loadTable( dataPath, 'sext_primes', { 1 : 7 } )


#//******************************************************************************
#//
#//  isPrime
#//
#//******************************************************************************

def isPrime( arg ):
    return pyprimes.isprime( int( arg ) )


#//******************************************************************************
#//
#//  getNextPrimeCandidate
#//
#//******************************************************************************

def getNextPrimeCandidate( p, f ):
    if f == 1:
        p += 2
        f = 3
    elif f == 3:
        p += 4
        f = 7
    elif f == 7:
        p += 2
        f = 9
    else:
        p += 2
        f = 1

    return p, f


#//******************************************************************************
#//
#//  getNextPrime
#//
#//******************************************************************************

def getNextPrime( p, f, func=getNextPrimeCandidate ):
    p, f = getNextPrimeCandidate( p, f )

    while not isPrime( p ):
        p, f = func( p, f )

    return p, f


#//******************************************************************************
#//
#//  getNthPrime
#//
#//******************************************************************************

def getNthPrime( arg ):
    global smallPrimes
    global largePrimes
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
    elif n >= 1000000:
        if largePrimes == { }:
            largePrimes = loadLargePrimes( g.dataPath )

        maxIndex = max( key for key in largePrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                              format( n, maxIndex ) )

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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f )
        currentIndex += 1

    if updateDicts:
        if n >= 1000000:
            largePrimes[ n ] = p
        else:
            smallPrimes[ n ] = p

    return p


#//******************************************************************************
#//
#//  findPrime
#//
#//******************************************************************************

def findPrime( arg ):
    global smallPrimes
    global largePrimes

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
    else:
        if largePrimes == { }:
            largePrimes = loadLargePrimes( g.dataPath )

        currentIndex = max( key for key in largePrimes if largePrimes[ key ] <= target )
        p = largePrimes[ currentIndex ]

    f = p % 10

    while True:
        p, f = getNextPrime( p, f )
        currentIndex += 1

        if p >= target:
            return currentIndex, p


#//******************************************************************************
#//
#//  findQuadrupletPrimes
#//
#//******************************************************************************

def findQuadrupletPrimes( arg ):
    global quadPrimes

    n = int( arg )

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


#//******************************************************************************
#//
#//  getNthQuadrupletPrime
#//
#//******************************************************************************

def getNthQuadrupletPrime( arg ):
    global quadPrimes
    global updateDicts

    n = int( arg )

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


#//******************************************************************************
#//
#//  getNthIsolatedPrime
#//
#//******************************************************************************

def getNthIsolatedPrime( arg ):
    global isolatedPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        if not isPrime( p - 2 ) and not isPrime( p + 2 ):
            currentIndex += 1

    if updateDicts:
        isolatedPrimes[ n ] = p

    return p


#//******************************************************************************
#//
#//  getNextTwinPrimeCandidate
#//
#//******************************************************************************

def getNextTwinPrimeCandidate( p, f ):
    if f == 1:
        p += 6
        f = 7
    elif f == 7:
        p += 2
        f = 9
    else:
        p += 2
        f = 1

    return p, f


#//******************************************************************************
#//
#//  getNthTwinPrime
#//
#//******************************************************************************

def getNthTwinPrime( arg ):
    global twinPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f, getNextTwinPrimeCandidate )

        if isPrime( p + 2 ):
            currentIndex += 1

    if updateDicts:
        twinPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthTwinPrimeList
#//
#//******************************************************************************

def getNthTwinPrimeList( arg ):
    p = getNthTwinPrime( arg )
    return [ p, fadd( p, 2 ) ]


#//******************************************************************************
#//
#//  getNthBalancedPrime
#//
#//  returns the first of a set of 3 balanced primes
#//
#//******************************************************************************

def getNthBalancedPrime( arg ):
    global balancedPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        if ( prevPrime - secondPrevPrime ) == ( p - prevPrime ):
            currentIndex += 1

        if n > currentIndex:
            secondPrevPrime = prevPrime
            prevPrime = p

    if updateDicts:
        balancedPrimes[ int( arg ) ] = secondPrevPrime

    return secondPrevPrime


#//******************************************************************************
#//
#//  getNthBalancedPrimeList
#//
#//******************************************************************************

def getNthBalancedPrimeList( arg ):
    p = getNthBalancedPrime( arg )
    f = p % 10

    q, f = getNextPrime( p, f )
    r, f = getNextPrime( q, f )

    return [ p, q, r ]


#//******************************************************************************
#//
#//  getNthDoubleBalancedPrime
#//
#//******************************************************************************

def getNthDoubleBalancedPrime( arg ):
    global doubleBalancedPrimes
    global updateDicts

    n = int( arg )

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
    f = p % 10

    primes = [ p ]

    for i in range( 0, 4 ):
        p, f = getNextPrime( p, f )
        primes.append( p )

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 3 ] - primes[ 2 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 4 ] - primes[ 3 ] ) ):
            currentIndex += 1

    if updateDicts:
        doubleBalancedPrimes[ n ] = p

    return p


#//******************************************************************************
#//
#//  getNthDoubleBalancedPrimeList
#//
#//******************************************************************************

def getNthDoubleBalancedPrimeList( arg ):
    p = getNthDoubleBalancedPrime( arg )
    result = [ p ]

    f = p % 10

    for i in range( 0, 4 ):
        p, f = getNextPrime( p, f )
        result.append( p )

    return result


#//******************************************************************************
#//
#//  getNthTripleBalancedPrime
#//
#//******************************************************************************

def getNthTripleBalancedPrime( arg ):
    global tripleBalancedPrimes
    global updateDicts

    n = int( arg )

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
    f = p % 10

    primes = [ p ]

    for i in range( 0, 6 ):
        p, f = getNextPrime( p, f )
        primes.append( p )

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 3 ] - primes[ 2 ] ) == ( primes[ 4 ] - primes[ 3 ] ) and
             ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 5 ] - primes[ 4 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 6 ] - primes[ 5 ] ) ):
            currentIndex += 1

    if updateDicts:
        tripleBalancedPrimes[ n ] = p

    return p


#//******************************************************************************
#//
#//  getNthTripleBalancedPrimeList
#//
#//******************************************************************************

def getNthTripleBalancedPrimeList( arg ):
    p = [ getNthTripleBalancedPrime( arg ) ]

    return p[ 0 ]

    #result = [ p ]
    #
    #f = p % 10
    #
    #for i in range( 0, 6 ):
    #   p, f = getNextPrime( p, f )
    #   result.append( p )
    #
    #return result


#//******************************************************************************
#//
#//  getNthSophiePrime
#//
#//******************************************************************************

def getNthSophiePrime( arg ):
    global sophiePrimes
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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        if isPrime( 2 * p + 1 ):
            currentIndex += 1

    if updateDicts:
        sophiePrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthCousinPrime
#//
#//******************************************************************************

def getNthCousinPrime( arg ):
    global cousinPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrime( p, f )

        if isPrime( p + 4 ):
            currentIndex += 1

    if updateDicts:
        cousinPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthCousinPrimeList
#//
#//******************************************************************************

def getNthCousinPrimeList( arg ):
    p = getNthCousinPrime( arg )
    return [ p, fadd( p, 4 ) ]


#//******************************************************************************
#//
#//  getNextSexyPrimeCandidate
#//
#//******************************************************************************

def getNextSexyPrimeCandidate( p, f ):
    if f == 1:
        p += 2
        f = 3
    elif f == 3:
        p += 4
        f = 7
    else:
        p += 4
        f = 1

    return p, f


#//******************************************************************************
#//
#//  getNthSexyPrime
#//
#//******************************************************************************

def getNthSexyPrime( arg ):
    global sexyPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    while n > startingPlace:
        p, f = getNextPrime( p, f, getNextSexyPrimeCandidate )

        if isPrime( p + 6 ):
            n -= 1

    if updateDicts:
        sexyPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthSexyPrimeList
#//
#//******************************************************************************

def getNthSexyPrimeList( arg ):
    p = getNthSexyPrime( arg )
    return [ p, fadd( p, 6 ) ]


#//******************************************************************************
#//
#//  getNthSexyTriplet
#//
#//******************************************************************************

def getNthSexyTriplet( arg ):
    global sexyTriplets
    global updateDicts

    n = int( arg )

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


#//******************************************************************************
#//
#//  getNthSexyTripletList
#//
#//******************************************************************************

def getNthSexyTripletList( arg ):
    p = getNthSexyTriplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ) ]


#//******************************************************************************
#//
#//  getNthSexyQuadruplet
#//
#//******************************************************************************

def getNthSexyQuadruplet( arg ):
    global sexyQuadruplets
    global updateDicts

    n = int( arg )

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


#//******************************************************************************
#//
#//  getNthSexyQuadrupletList
#//
#//******************************************************************************

def getNthSexyQuadrupletList( arg ):
    p = getNthSexyQuadruplet( arg )
    return [ p, fadd( p, 6 ), fadd( p, 12 ), fadd( p, 18 ) ]


#//******************************************************************************
#//
#//  getNthTripletPrime
#//
#//******************************************************************************

def getNthTripletPrime( arg ):
    global tripletPrimes
    global updateDicts

    n = int( arg )

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

    return [ p, p + 2 if pPlus2 else 4, p + 6 ]


#//******************************************************************************
#//
#//  getNthTripletPrimeList
#//
#//******************************************************************************

def getNthTripletPrimeList( arg ):
    p = int( getNthTripletPrime( arg )[ 0 ] )
    f = p % 10

    return [ p, getNextPrime( p, f )[ 0 ], fadd( p, 6 ) ]


#//******************************************************************************
#//
#//  getNextQuintupletPrimeCandidate
#//
#//******************************************************************************

def getNextQuintupletPrimeCandidate( p, f ):
    if f == 1:
        p += 6
        f = 7
    else:
        p += 4
        f = 1

    return p, f


#//******************************************************************************
#//
#//  getNthQuadrupletPrimeList
#//
#//******************************************************************************

def getNthQuadrupletPrimeList( arg ):
    p = getNthQuadrupletPrime( arg )
    return [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ) ]


#//******************************************************************************
#//
#//  getNthQuintupletPrime
#//
#//******************************************************************************

def getNthQuintupletPrime( arg ):
    global quintPrimes
    global updateDicts

    n = int( arg )

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

    f = p % 10

    # after 5, the first of a prime quintruplet must be a number of the form 30n + 11
    while n > currentIndex:
        p, f = getNextPrime( p, f, getNextQuintupletPrimeCandidate )

        if ( ( f == 1 ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ) and isPrime( p + 12 ) ) or \
           ( ( f == 7 ) and isPrime( p + 4 ) and isPrime( p + 6 ) and isPrime( p + 10 ) and isPrime( p + 12 ) ):
            currentIndex += 1

    if updateDicts:
        quintPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthQuintupletPrimeList
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getNthSextupletPrime
#//
#//******************************************************************************

def getNthSextupletPrime( arg ):
    global sextPrimes
    global updateDicts

    n = int( arg )

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


#//******************************************************************************
#//
#//  getNthSextupletPrimeList
#//
#//******************************************************************************

def getNthSextupletPrimeList( arg ):
    p = getNthSextupletPrime( arg )
    return [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ), fadd( p, 16 ) ]


#//******************************************************************************
#//
#//  getNthPrimeRange
#//
#//******************************************************************************

def getNthPrimeRange( arg1, arg2 ):
    n = int( arg1 )
    count = int( arg2 )

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

    f = p % 10

    found = 1

    while found < count:
        p, f = getNextPrimeCandidate( p, f )

        if isPrime( p ):
            result.append( p )
            found += 1

    return result


#//******************************************************************************
#//
#//  getNthSuperPrime
#//
#//******************************************************************************

def getNthSuperPrime( arg ):
    return getNthPrime( getNthPrime( arg ) )


#//******************************************************************************
#//
#//  getNthPolyPrime
#//
#//******************************************************************************

def getNthPolyPrime( n, poly ):
    result = getNthPrime( n )

    for i in arange( 1, poly ):
        result = getNthPrime( result )

    return result


#//******************************************************************************
#//
#//  getPrimes
#//
#//******************************************************************************

def getPrimes( value, count ):
    result = list( )

    for i in getNthPrimeRange( value, count ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  getPrimorial
#//
#//******************************************************************************

def getPrimorial( n ):
    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result


