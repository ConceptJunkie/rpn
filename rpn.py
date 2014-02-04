#!/usr/bin/env python

import argparse
import bz2
import contextlib
import itertools
import math
import os
import pickle
import pyprimes
import random
import sys
import time
import types

from fractions import Fraction
from functools import reduce
from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = "rpn"
RPN_VERSION = "4.9.0"
PROGRAM_DESCRIPTION = 'RPN command-line calculator'
COPYRIGHT_MESSAGE = "copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 12
defaultAccuracy = 10
defaultCFTerms = 10
defaultBitwiseGroupSize = 16
defaultInputRadix = 10
defaultOutputRadix = 10
defaultDecimalGrouping = 5
defaultIntegerGrouping = 3

defaultNumerals = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

numerals = ""

phiBase = -1
fibBase = -2

inputRadix = 10

updateDicts = False


#//******************************************************************************
#//
#//  loadTable
#//
#//******************************************************************************

def loadTable( fileName, default ):
    global dataPath

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'rb' ) ) as pickleFile:
            primes = pickle.load( pickleFile )
    except FileNotFoundError as error:
        primes = default

    return primes


def loadSmallPrimes( ):
    return loadTable( 'small_primes', { 4 : 7 } )

def loadLargePrimes( ):
    return loadTable( 'large_primes', { 1000000 : 15485863 } )

def loadTwinPrimes( ):
    return loadTable( 'twin_primes', { 3 : 11 } )

def loadBalancedPrimes( ):
    return loadTable( 'balanced_primes', { 2 : 53 } )

def loadSophiePrimes( ):
    return loadTable( 'sophie_primes', { 4 : 11 } )

def loadCousinPrimes( ):
    return loadTable( 'cousin_primes', { 2 : 7 } )

def loadSexyPrimes( ):
    return loadTable( 'sexy_primes', { 2 : 7 } )

def loadSexyTriplets( ):
    return loadTable( 'sexy_triplets', { 2 : 17 } )

def loadSexyQuadruplets( ):
    return loadTable( 'sexy_quadruplets', { 2 : 11 } )

def loadTripletPrimes( ):
    return loadTable( 'triplet_primes', { 2 : 7 } )

def loadQuadrupletPrimes( ):
    return loadTable( 'quad_primes', { 2 : 11 } )


#//******************************************************************************
#//
#//  saveTable
#//
#//******************************************************************************

def saveTable( fileName, var ):
    global dataPath

    with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( var, pickleFile )

def saveSmallPrimes( smallPrimes ):
    saveTable( 'small_primes', smallPrimes )

def saveLargePrimes( largePrimes ):
    saveTable( 'large_primes', largePrimes )

def saveTwinPrimes( twinPrimes ):
    saveTable( 'twin_primes', twinPrimes )

def saveBalancedPrimes( balancedPrimes ):
    saveTable( 'balanced_primes', balancedPrimes )

def saveSophiePrimes( sophiePrimes ):
    saveTable( 'sophie_primes', sophiePrimes )

def saveCousinPrimes( cousinPrimes ):
    saveTable( 'cousin_primes', cousinPrimes )

def saveSexyPrimes( sexyPrimes ):
    saveTable( 'sexy_primes', sexyPrimes )

def saveSexyTriplets( sexyTriplets ):
    saveTable( 'sexy_triplets', sexyTriplets )

def saveSexyQuadruplets( sexyQuadruplets ):
    saveTable( 'sexy_quadruplets', sexyQuadruplets )

def saveTripletPrimes( tripletPrimes ):
    saveTable( 'triplet_primes', tripletPrimes )

def saveQuadrupletPrimes( quadPrimes ):
    saveTable( 'quad_primes', quadPrimes )


#//******************************************************************************
#//
#//  makeTable
#//
#//******************************************************************************

def makeTable( start, end, step, func, name ):
    global updateDicts

    updateDicts = True

    try:
        for i in range( int( start ), int( end ) + 1, int( step ) ):
            p = func( i )

            if isinstance( p, list ):
                p = p[ 0 ]

            print( name + ':  {:,} : {:,}'.format( i, p ) )
            sys.stdout.flush( )
    except KeyboardInterrupt as error:
        pass

    return end

def makeSmallPrimes( start, end, step ):
    global smallPrimes
    getNthPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthPrime, 'small' )
    saveSmallPrimes( smallPrimes )
    return end

def makeLargePrimes( start, end, step ):
    global largePrimes
    getNthPrime( 1000000 )  # force the cache to load
    end = makeTable( start, end, step, getNthPrime, 'prime' )
    saveLargePrimes( largePrimes )
    return end

def makeSuperPrimes( start, end ):
    global smallPrimes
    global largePrimes
    global updateDicts

    getNthPrime( 100 )      # force small primes cache to load
    getNthPrime( 1000000 )  # force large primes cache to load

    try:
        for i in range( int( start ), int( end ) + 1, 1 ):
            updateDicts = False
            nth = getNthPrime( i )

            updateDicts = True
            p = getNthPrime( nth )

            print( 'super:  {:,} : {:,} : {:,}'.format( i, nth, p ) )
            sys.stdout.flush( )
    except KeyboardInterrupt as error:
        pass

    saveSmallPrimes( smallPrimes )
    saveLargePrimes( largePrimes )

    return end

def makeTwinPrimes( start, end, step ):
    global twinPrimes
    getNthTwinPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTwinPrimes, 'twin' )
    saveTwinPrimes( twinPrimes )
    return end

def makeBalancedPrimes( start, end, step ):
    global balancedPrimes
    getNthBalancedPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthBalancedPrimes, 'balanced' )
    saveBalancedPrimes( balancedPrimes )
    return end

def makeSophiePrimes( start, end, step ):
    global sophiePrimes
    getNthSophiePrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSophiePrime, 'sophie' )
    saveSophiePrimes( sophiePrimes )
    return end

def makeCousinPrimes( start, end, step ):
    global cousinPrimes
    getNthCousinPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthCousinPrimes, 'cousin' )
    saveCousinPrimes( cousinPrimes )
    return end

def makeSexyPrimes( start, end, step ):
    global sexyPrimes
    getNthSexyPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyPrimes, 'sexy' )
    saveSexyPrimes( sexyPrimes )
    return end

def makeSexyTriplets( start, end, step ):
    global sexyTriplets
    getNthSexyTriplets( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyTriplet, 'sexytrip' )
    saveSexyTriplets( sexyTriplets )
    return end

def makeSexyQuadruplets( start, end, step ):
    global sexyQUadruplets
    getNthSexyQuadruplets( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyQuadruplets, 'sexyquad' )
    saveSexyPrimes( sexyQuadruplets )
    return end

def makeTripletPrimes( start, end, step ):
    global tripletPrimes
    getNthTripletPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTripletPrimes, 'triplet' )
    saveTripletPrimes( tripletPrimes )
    return end

def makeQuadrupletPrimes( start, end, step ):
    global quadPrimes
    getNthQuadrupletPrimes( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuadrupletPrimes, 'quad' )
    saveQuadrupletPrimes( quadPrimes )
    return end


#//******************************************************************************
#//
#//  dumpTable
#//
#//******************************************************************************

def dumpTable( loadFunc, name ):
    var = loadFunc( )

    for i in sorted( [ key for key in var ] ):
        print( name + ':  ' + str( i ) + ' : ' + str( var[ i ] ) )

    return max( [ key for key in var ] )

def dumpSmallPrimes( ):
    return dumpTable( loadSmallPrimes, 'small' )

def dumpLargePrimes( ):
    return dumpTable( loadLargePrimes, 'prime' )

def dumpTwinPrimes( ):
    return dumpTable( loadTwinPrimes, 'twin' )

def dumpBalancedPrimes( ):
    return dumpTable( loadBalancedPrimes, 'balanced' )

def dumpSophiePrimes( ):
    return dumpTable( loadSophiePrimes, 'sophie' )

def dumpCousinPrimes( ):
    return dumpTable( loadCousinPrimes, 'cousin' )

def dumpSexyPrimes( ):
    return dumpTable( loadSexyPrimes, 'sexy' )

def dumpSexyTriplets( ):
    return dumpTable( loadSexyTriplets, 'sexytrip' )

def dumpSexyQuadruplets( ):
    return dumpTable( loadSexyQuadruplets, 'sexyquad' )

def dumpTripletPrimes( ):
    return dumpTable( loadTripletPrimes, 'triplet' )

def dumpQuadrupletPrimes( ):
    return dumpTable( loadQuadrupletPrimes, 'quad' )


#//******************************************************************************
#//
#//  isPrime
#//
#//******************************************************************************

def isPrime( arg ):
    return pyprimes.isprime( int( arg ) )


#//******************************************************************************
#//
#//  findPrime
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
#//  getNthPrime
#//
#//******************************************************************************

def getNthPrime( arg ):
    global smallPrimes
    global largePrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 2

    if n == 2:
        return 3

    if n == 3:
        return 5

    if n >= 1000000:
        if largePrimes == { }:
            largePrimes = loadLargePrimes( )

        maxIndex = max( key for key in largePrimes )

        if n > maxIndex:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

        currentIndex = max( key for key in largePrimes if key <= n )
        p = largePrimes[ currentIndex ]

        #print( 'starting: ' + str( currentIndex ) )
    elif n >= 100:
        if smallPrimes == { }:
            smallPrimes = loadSmallPrimes( )

        currentIndex = max( key for key in smallPrimes if key <= n )
        p = smallPrimes[ currentIndex ]

        #print( 'looking for nth: ' + str( n ) + ' - starting: ' + str( currentIndex ) + ', p: ' + str( p ) )
    else:
        currentIndex = 4
        p = 7

    f = p % 10

    while n > currentIndex:
        p, f = getNextPrimeCandidate( p, f )

        if isPrime( p ):
            currentIndex += 1

    if updateDicts:
        if n >= 1000000:
            largePrimes[ n ] = p
        else:
            smallPrimes[ n ] = p

    #print( 'finished: ' + str( n ) + ', ' + str( p ) )
    return p


#//******************************************************************************
#//
#//  findPrimeIndex
#//
#//******************************************************************************

def findPrimeIndex( arg ):
    global smallPrimes
    global largePrimes

    target = int( arg )

    if target < 2:
        return 1
    elif target == 3:
        return 2
    elif target < 5:
        return 3
    elif target < 541:          # 100th prime
        currentIndex = 4
        p = 7
    elif target < 15485863:     # 1,000,000th prime
        if smallPrimes == { }:
            smallPrimes = loadSmallPrimes( )

        currentIndex = max( key for key in smallPrimes if smallPrimes[ key ] <= target )
        p = smallPrimes[ currentIndex ]
    else:
        if largePrimes == { }:
            largePrimes = loadLargePrimes( )

        currentIndex = max( key for key in largePrimes if largePrimes[ key ] <= target )
        p = largePrimes[ currentIndex ]

    f = p % 10

    while True:
        p, f = getNextPrimeCandidate( p, f )

        if isPrime( p ):
            if p > target:
                return currentIndex
            else:
                currentIndex += 1


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
#//  getNthTwinPrimes
#//
#//******************************************************************************

def getNthTwinPrimes( arg ):
    global twinPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 3
    elif n == 2:
        return 5
    elif n == 3:
        return 11

    if n >= 100:
        if twinPrimes == { }:
            twinPrimes = loadTwinPrimes( )

        startingPlace = max( key for key in twinPrimes if key <= n )
        p = twinPrimes[ startingPlace ]
    else:
        startingPlace = 3
        p = 11

    f = p % 10

    while n > startingPlace:
        if f == 1:
            p += 6
            f = 7
        elif f == 7:
            p += 2
            f = 9
        else:
            p += 2
            f = 1

        if isPrime( p ) and isPrime( p + 2 ):
            n -= 1

    if updateDicts:
        twinPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthBalancedPrimes
#//
#//******************************************************************************

def getNthBalancedPrimes( arg ):
    global balancedPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return [ 3, 5, 7 ]

    if n >= 100:
        if balancedPrimes == { }:
            balancedPrimes = loadBalancedPrimes( )

        startingPlace = max( key for key in balancedPrimes if key < n )
        p = balancedPrimes[ startingPlace ]
    else:
        startingPlace = 2
        p = 53

    prevPrime = secondPrevPrime = p

    f = p % 10

    while n > startingPlace:
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

        if isPrime( p ):
            if ( prevPrime - secondPrevPrime ) == ( p - prevPrime ):
                n -= 1

            if n > startingPlace:
                secondPrevPrime = prevPrime
                prevPrime = p

    if updateDicts:
        balancedPrimes[ int( arg ) ] = prevPrime

    return [ secondPrevPrime, prevPrime, p  ]


#//******************************************************************************
#//
#//  getNthSophiePrime
#//
#//******************************************************************************

def getNthSophiePrime( arg ):
    global sophiePrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 2
    elif n == 2:
        return 3
    elif n == 3:
        return 5

    if n >= 100:
        if sophiePrimes == { }:
            sophiePrimes = loadSophiePrimes( )

        startingPlace = max( key for key in sophiePrimes if key <= n )
        p = sophiePrimes[ startingPlace ]
    else:
        startingPlace = 4
        p = 11

    f = p % 10

    while n > startingPlace:
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

        if isPrime( p ) and isPrime( 2 * p + 1 ):
            n -= 1

    if updateDicts:
        sophiePrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthCousinPrimes
#//
#//******************************************************************************

def getNthCousinPrimes( arg ):
    global cousinPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 3

    if n >= 100:
        if cousinPrimes == { }:
            cousinPrimes = loadCousinPrimes( )

        startingPlace = max( key for key in cousinPrimes if key <= n )
        p = cousinPrimes[ startingPlace ]
    else:
        startingPlace = 2
        p = 7

    f = p % 10

    while n > startingPlace:
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

        if isPrime( p ) and isPrime( p + 4 ):
            n -= 1

    if updateDicts:
        cousinPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthSexyPrimes
#//
#//******************************************************************************

def getNthSexyPrimes( arg ):
    global sexyPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 5

    if n >= 100:
        if sexyPrimes == { }:
            sexyPrimes = loadSexyPrimes( )

        startingPlace = max( key for key in sexyPrimes if key <= n )
        p = sexyPrimes[ startingPlace ]
    else:
        startingPlace = 2
        p = 7

    f = p % 10

    while n > startingPlace:
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
            n -= 1

    if updateDicts:
        sexyPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthSexyTriplets
#//
#//******************************************************************************

def getNthSexyPrimes( arg ):
    global sexyTriplets
    global updateDicts

    n = int( arg )

    if n == 1:
        return 7

    if n >= 100:
        if sexyTriplets == { }:
            sexyTriplets = loadSexyTriplets( )

        startingPlace = max( key for key in sexyTriplets if key <= n )
        p = sexyTriplets[ startingPlace ]
    else:
        startingPlace = 1
        p = 7

    f = p % 10

    while n > startingPlace:
        if f == 1:
            p += 6
            f = 7
        else:
            p += 4
            f = 1

        if isPrime( p ) and isPrime( p + 6 ) and isPrime( p + 12 ) and not isPrime( p + 18 ):
            n -= 1

    if updateDicts:
        sexyTriplets[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthTripletPrimes
#//
#//******************************************************************************

def getNthTripletPrimes( arg ):
    global tripletPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return [ 5, 7, 11 ]
    elif n == 2:
        return [ 7, 11, 13 ]

    if n >= 100:
        if tripletPrimes == { }:
            tripletPrimes = loadTripletPrimes( )

        startingPlace = max( key for key in tripletPrimes if key <= n )
        p = tripletPrimes[ startingPlace ]

        if isPrime( p + 2 ):
            middle = 2
        else:
            middle = 4

    else:
        startingPlace = 3
        p = 11
        middle = 2

    f = p % 10

    while n > startingPlace:
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
                middle = 2
                n -= 1
            elif isPrime( p + 4 ):
                middle = 4
                n -= 1

    if updateDicts:
        tripletPrimes[ int( arg ) ] = p

    return [ p, p + middle, p + 6 ]


#//******************************************************************************
#//
#//  getNthQuadrupletPrimes
#//
#//******************************************************************************

def getNthQuadrupletPrimes( arg ):
    global quadPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 5
    elif n == 2:
        return 11

    if n >= 10:
        if quadPrimes == { }:
            quadPrimes = loadQuadrupletPrimes( )

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
#//  getNthPrimeRange
#//
#//******************************************************************************

def getNthPrimeRange( arg1, arg2 ):
    n = int( arg1 )
    count = int( arg2 )

    if count < 1:
        return [ ]

    if n == 1:
        if count == 1:
            return [ 2 ]
        elif count == 2:
            return[ 2, 3 ]
        else:
            result = [ 2, 3, 5 ]
            n = 3
            count -= 3
            p = 5
    elif n == 2:
        if count == 1:
            return [ 3 ]
        else:
            result = [ 3, 5 ]
            n = 3
            count -= 2
            p = 5
    else:
        p = getNthPrime( n )
        result = [ p ]

    f = p % 10

    found = 0

    while found < count:
        p, f = getNextPrimeCandidate( p, f )

        if isPrime( p ):
            result.append( p )
            found += 1

    return result


#//******************************************************************************
#//
#//  ContinuedFraction
#//
#//  A continued fraction, represented as a list of integer terms.
#//
#//  adapted from ActiveState Python, recipe 578647
#//
#//******************************************************************************

class ContinuedFraction( list ):
    def __init__( self, value, maxterms=15, cutoff=1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            self.extend( value )
        else:
            raise ValueError( "ContinuedFraction requires number or list" )

    def getFraction( self, terms=None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return "[%s]" % ", ".join( [ str( int( x ) ) for x in self ] )



#//******************************************************************************
#//
#//  factorize
#//
#//  This is not my code, and I need to find the source so I can attribute it.
#//
#//******************************************************************************

def factorize( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factorize( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def potential_primes( ):
            base_primes = ( 2, 3, 5 )

            for base_prime in base_primes:
                yield base_prime

            base_primes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            prime_group = 0

            while True:
                for base_prime in base_primes:
                    yield prime_group + base_prime

                prime_group += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in potential_primes( ):
            if divisor > sqrtn:
                break

            power = 0

            while ( fmod( n, divisor ) ) == 0:
                n = floor( fdiv( n, divisor ) )
                power += 1

            if power > 0:
                factors.append( ( divisor, power ) )
                sqrtn = sqrt( n )

        if n > 1:
             factors.append( ( int( n ), 1 ) )

        return factors


#//******************************************************************************
#//
#//  getExpandedFactorList
#//
#//******************************************************************************

def getExpandedFactorList( factors ):
    factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return reduce( lambda x, y: x + y, factors, [ ] )


#//******************************************************************************
#//
#//  convertToPhiBase
#//
#//******************************************************************************

def convertToPhiBase( num ):
    epsilon = power( 10, -( mp.dps - 3 ) )

    output = ''
    integer = ''

    start = True
    previousPlace = 0
    remaining = num

    originalPlace = 0

    while remaining > epsilon:
        place = int( floor( log( remaining, phi ) ) )

        if start:
            output = '1'
            start = False
            originalPlace = place
        else:
            if place < -( originalPlace + 1 ):
                break

            for i in range( previousPlace, place + 1, -1 ):
                output += '0'

                if ( i == 1 ):
                    integer = output
                    output = ''

            output += '1'

            if place == 0:
                integer = output
                output = ''

        previousPlace = place
        remaining -= power( phi, place )

    if integer == '':
        return output, ''
    else:
        return integer, output


#//******************************************************************************
#//
#//  convertToFibBase
#//
#//  Returns a string with Fibonacci encoding for n (n >= 1).
#//
#//  adapted from https://en.wikipedia.org/wiki/Fibonacci_coding
#//
#//******************************************************************************

def convertToFibBase( value ):
    result = ""

    n = value

    if n >= 1:
        a = 1
        b = 1

        c = fadd( a, b )    # next Fibonacci number
        fibs = [ b ]        # list of Fibonacci numbers, starting with F(2), each <= n

        while n >= c:
            fibs.append( c )  # add next Fibonacci number to end of list
            a = b
            b = c
            c = fadd( a, b )

        result = ""

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + "1"
            else:
                result = result + "0"

    return result


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//******************************************************************************

def convertToBaseN( value, base, baseAsDigits, numerals ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( numerals ) )

    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( ( -1 ) * value, base, baseAsDigits, numerals )

    if base == 10:
        return str( value )

    result = ''
    left_digits = value

    while left_digits > 0:
        if baseAsDigits:
            if result != '':
                result = ' ' + result

            result = str( int( left_digits ) % base ) + result
        else:
            result = numerals[ int( left_digits ) % base ] + result

        left_digits = floor( fdiv( left_digits, base ) )

    return result


#//******************************************************************************
#//
#//  convertFractionToBaseN
#//
#//******************************************************************************

def convertFractionToBaseN( value, base, precision, baseAsDigits, accuracy ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( numerals ) )

    if value < 0 or value >= 1.0:
        raise ValueError( 'value (%s) must be >= 0 and < 1.0' % value )

    if base == 10:
        return str( value )

    result = ''

    while value > 0 and precision > 0:
        value = value * base
        digit = int( value )

        if len( result ) == accuracy:
            value -= digit
            newDigit = int( value ) % base

            if newDigit >= base // 2:
                digit += 1

        if baseAsDigits:
            if result != '':
                result += ' '

            result += str( digit % base )
        else:
            result += numerals[ digit % base ]

        if len( result ) == accuracy:
            break

        value -= digit
        precision -= 1

    return result


#//******************************************************************************
#//
#//  convertToBase10
#//
#//******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


#//******************************************************************************
#//
#//  getInvertedBits
#//
#//******************************************************************************

def getInvertedBits( n ):
    global bitwiseGroupSize

    value = floor( n )
    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = value

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        result = fadd( fmul( fsum( [ placeValue, fneg( fmod( remaining, placeValue ) ), -1 ] ), multiplier ), result )
        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    return result


#//******************************************************************************
#//
#//  performBitwiseOperation
#//
#//  The operations are performed on groups of bits as specified by the variable
#//  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
#//  does mean that under normal circumstances the regular Python bit operators
#//  can be used.
#//
#//******************************************************************************

def performBitwiseOperation( i, j, operation ):
    global bitwiseGroupSize

    value1 = floor( i )
    value2 = floor( j )

    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )
    groupings2 = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    if groupings2 > groupings:
        groupings = groupings2

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining1 = value1
    remaining2 = value2

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        mod1 = fmod( remaining1, placeValue )
        mod2 = fmod( remaining2, placeValue )

        result = fadd( fmul( operation( int( mod1 ), int( mod2 ) ), multiplier ), result )

        remaining1 = floor( fdiv( remaining1, placeValue ) )
        remaining2 = floor( fdiv( remaining2, placeValue ) )

        multiplier = fmul( multiplier, placeValue )

    return result


#//******************************************************************************
#//
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  getNthLucas
#//
#//******************************************************************************

def getNthLucas( n ):
    if n == 1:
        return 1
    else:
        return floor( fadd( power( phi, n ), 0.5 ) )


#//******************************************************************************
#//
#//  getNthSylvester
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getNthTriangularNumber
#//
#//******************************************************************************

def getNthTriangularNumber( n ):
    return fdiv( fmul( n, fadd( n, 1 ) ), 2 )


#//******************************************************************************
#//
#//  getAntiTriangularNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiTriangularNumber( n ):
    return fmul( 0.5, fsub( sqrt( fadd( fmul( 8, n ), 1 ) ), 1 ) )


#//******************************************************************************
#//
#//  getAntiHexagonalNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiHexagonalNumber( n ):
    return fdiv( fadd( sqrt( fadd( fmul( 8, n ), 1 ) ), 1 ), 4 )


#//******************************************************************************
#//
#//  getNthTetrahedralNumber
#//
#//******************************************************************************

def getNthTetrahedralNumber( n ):
    return fdiv( fsum( [ power( n, 3 ), fmul( 3, power( n, 2 ) ), fmul( 2, n ) ] ), 6 )


#//******************************************************************************
#//
#//  getAntiTetrahedralNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def getAntiTetrahedralNumber( n ):
    sqrt3 = sqrt( 3 )
    curt3 = cbrt( 3 )

    # TODO:  finish me
    return 0

# http://www.wolframalpha.com/input/?i=solve+p%3D%281%2F6%29*%28n^3%2B3*n^2%2B2*n%29+for+n


#//******************************************************************************
#//
#//  getNthTruncatedTetrahedralNumber
#//
#//  Take the (3n-2)th terahedral number and chop off the (n-1)th tetrahedral
#//  number from each corner.
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedTetrahedralNumber( n ):
    return fmul( fdiv( n, 6 ), fsum( [ fprod( [ 23, n, n ] ), fmul( -27, n ), 10 ] ) )


#//******************************************************************************
#//
#//  getNthSquareTriangularNumber
#//
#//******************************************************************************

def getNthSquareTriangularNumber( n ):
    neededPrecision = int( n * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        mp.dps = neededPrecision

    sqrt2 = sqrt( 2 )

    return ceil( power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                    power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                              fmul( 4, sqrt2 ) ), 2 ) )


#//******************************************************************************
#//
#//  getNthPyramidalNumber
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPyramidalNumber( n ):
    return fprod( [ fdiv( n, 6 ), fadd( n, 1 ), fadd( fmul( 2, n ), 1 ) ] )


#//******************************************************************************
#//
#//  getNthOctahedralNumber
#//
#//  Oct( n ) = Pyr( n ) + Pyr( n - 1)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthOctahedralNumber( n ):
    return fmul( fdiv( n, 3 ), fadd( fprod( [ 2, n, n ] ), 1 ) )


#//******************************************************************************
#//
#//  getNthStellaOctangulaNumber
#//
#//  Stel( n ) = Oct( n ) + 8 Tet( n - 1 )
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthStellaOctangulaNumber( n ):
    return fmul( 2, fsub( fprod( [ 2, n, n ] ), 1 ) )


#//******************************************************************************
#//
#//  getNthCenteredCube
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthCenteredCubeNumber( n ):
    return fadd( power( n, 3 ), power( fsub( n, 1 ), 3 ) )


#//******************************************************************************
#//
#//  getNthTruncatedOctahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  16n^3 - 33n^2 + 24n - 6
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedOctahedralNumber( n ):
    return polyval( [ 16, -33, 24, 6 ], n )


#//******************************************************************************
#//
#//  getNthRhombicDodecahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  Rho(n) = CCub(n) + 6 Pyr(n-1)
#//
#//  4n^3 + 6n^2 + 4n + 1
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthRhombicDodecahedralNumber( n ):
    return polyval( [ 4, 6, 4, 1 ], n )


#//******************************************************************************
#//
#//  getNthPentatopeNumber
#//
#//  1/24n ( n + 1 )( n + 2 )( n + 3 )
#//
#//  1/24 n^4 + 1/4 n^3 + 11/24 n^2 + 1/4 n
#//
#//  1/24 ( n^4 + 6 n^3 + 11 n^2 + 6n )
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPentatopeNumber( n ):
    return fdiv( polyval( [ 1, 6, 11, 6, 0 ], n ), 24 )


#//******************************************************************************
#//
#//  getNthPolytopeNumber
#//
#//  d = dimension
#//
#//  ( 1 / ( d - 1 )! ) PI k=0 to n-1 ( n + k )
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPolytopeNumber( n, d ):
    result = n
    m = n + 1

    for i in arange( 1, d - 1 ):
        result = fmul( result, m )
        m += 1

    return fdiv( result, fac( d - 1 ) )


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


#//******************************************************************************
#//
#//  getPermutations
#//
#//******************************************************************************

def getPermutations( n, r ):
    if ( r > n ):
        raise ValueError( 'number of elements (%d) cannot exceed the size of the set (%d)' % ( r, n ) )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


#//******************************************************************************
#//
#//  convertFromContinuedFraction
#//
#//******************************************************************************

def convertFromContinuedFraction( i ):
    fraction = ContinuedFraction( i ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


#//******************************************************************************
#//
#//  interpretAsFraction
#//
#//******************************************************************************

def interpretAsFraction( i, j ):
    fraction = ContinuedFraction( i, maxterms=j ).getFraction( )
    return [ fraction.numerator, fraction.denominator ]


#//******************************************************************************
#//
#//  interpretAsBase
#//
#//******************************************************************************

def interpretAsBase( args, base ):
    args.reverse( )

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


#//******************************************************************************
#//
#//  getPlasticConstant
#//
#//******************************************************************************

def getPlasticConstant( ):
    term = fmul( 12, sqrt( 69 ) )
    return fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 )


#//******************************************************************************
#//
#//  solveQuadraticPolynomial
#//
#//******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    if a == 0:
        if b == 0:
            raise ValueError( "invalid equation, no variable coefficients" )
        else:
            # linear equation, one root
            return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


#//******************************************************************************
#//
#//  solveCubicPolynomial
#//
#//  Adapted from http://www.1728.org/cubic2.htm
#//
#//******************************************************************************

def solveCubicPolynomial( a, b, c, d ):
    if a == 0:
        return solveQuadraticPolynomial( b, c, d )

    f = fdiv( fsub( fdiv( fmul( 3, c ), a ), fdiv( power( b, 2 ), power( a, 2 ) ) ), 3 )

    g = fdiv( fadd( fsub( fdiv( fmul( 2, power( b, 3 ) ), power( a, 3 ) ),
                          fdiv( fprod( [ 9, b, c ] ), power( a, 2 ) ) ),
                    fdiv( fmul( 27, d ), a ) ), 27 )
    h = fadd( fdiv( power( g, 2 ), 4 ), fdiv( power( f, 3 ), 27 ) )

    # all three roots are the same
    if h == 0:
        x1 = fneg( root( fdiv( d, a ), 3 ) )
        x2 = x1
        x3 = x2
    # two imaginary and one real root
    elif h > 0:
        r = fadd( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if r < 0:
            s = fneg( root( fneg( r ), 3 ) )
        else:
            s = root( r, 3 )

        t = fsub( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if t < 0:
            u = fneg( root( fneg( t ), 3 ) )
        else:
            u = root( t, 3 )

        x1 = fsub( fadd( s, u ), fdiv( b, fmul( 3, a ) ) )

        real = fsub( fdiv( fneg( fadd( s, u ) ), 2 ), fdiv( b, fmul( 3, a ) ) )
        imaginary = fdiv( fmul( fsub( s, u ), sqrt( 3 ) ), 2 )

        x2 = mpc( real, imaginary )
        x3 = mpc( real, fneg( imaginary ) )
    # all real roots
    else:
        j = sqrt( fsub( fdiv( power( g, 2 ), 4 ), h ) )
        k = acos( fneg( fdiv( g, fmul( 2, j ) ) ) )

        if j < 0:
            l = fneg( root( fneg( j ), 3 ) )
        else:
            l = root( j, 3 )

        m = cos( fdiv( k, 3 ) )
        n = fmul( sqrt( 3 ), sin( fdiv( k, 3 ) ) )
        p = fneg( fdiv( b, fmul( 3, a ) ) )

        x1 = fsub( fmul( fmul( 2, l ), cos( fdiv( k, 3 ) ) ), fdiv( b, fmul( 3, a ) ) )
        x2 = fadd( fmul( fneg( l ), fadd( m, n ) ), p )
        x3 = fadd( fmul( fneg( l ), fsub( m, n ) ), p )

    return [ chop( x1 ), chop( x2 ), chop( x3 ) ]


#//******************************************************************************
#//
#//  solveQuarticPolynomial
#//
#//  Adapted from http://www.1728.org/quartic2.htm
#//
#//******************************************************************************

def solveQuarticPolynomial( _a, _b, _c, _d, _e ):
    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )
    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    elif _b == 0 and _c == 0 and _d == 0:
        e = fdiv( _e, _a )

        f = root( _a, 4 )

        x1 = fdiv( root( fneg( e ), 4 ), f )
        x2 = fdiv( fneg( root( fneg( e ), 4 ) ), f )
        x3 = fdiv( mpc( 0, root( fneg( e ), 4 ) ), f )
        x4 = fdiv( mpc( 0, fneg( root( fneg( e ), 4 ) ) ), f )

        return [ x1, x2, x3, x4 ]

    # otherwise we have a regular quartic to solve
    a = 1
    b = fdiv( _b, _a )
    c = fdiv( _c, _a )
    d = fdiv( _d, _a )
    e = fdiv( _e, _a )

    # we turn the equation into a cubic that we can solve
    f = fsub( c, fdiv( fmul( 3, power( b, 2 ) ), 8 ) )
    g = fsum( [ d, fdiv( power( b, 3 ), 8 ), fneg( fdiv( fmul( b, c ), 2 ) ) ] )
    h = fsum( [ e, fneg( fdiv( fmul( 3, power( b, 4 ) ), 256 ) ),
                fmul( power( b, 2 ), fdiv( c, 16 ) ), fneg( fdiv( fmul( b, d ), 4 ) ) ] )

    y1, y2, y3 = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                       fneg( fdiv( power( g, 2 ), 64 ) ) )

    # pick two non-zero roots, if there are two imaginary roots, use them
    if im( y1 ) != 0:
        root1 = y1

        if y2 == 0 or im( y2 ) == 0:
            root2 = y3
        else:
            root2 = y2
    elif y1 == 0:
        root1 = y2
        root2 = y3
    elif y2 == 0:
        root1 = y1
        root2 = y3
    else:
        root1 = y2
        root2 = y3

    # more variables...
    p = sqrt( root1 )
    q = sqrt( root2 )
    r = fdiv( fneg( g ), fprod( [ 8, p, q ] ) )
    s = fneg( fdiv( b, 4 ) )

    # put together the 4 roots
    x1 = fsum( [ p, q, r, s ] )
    x2 = fsum( [ p, fneg( q ), fneg( r ), s ] )
    x3 = fsum( [ fneg( p ), q, fneg( r ), s ] )
    x4 = fsum( [ fneg( p ), fneg( q ), r, s ] )

    return [ chop( x1 ), chop( x2 ), chop( x3 ), chop( x4 ) ]


#//******************************************************************************
#//
#//  getChampernowne
#//
#//******************************************************************************

def getChampernowne( ):
    global inputRadix

    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += convertToBaseN( count, inputRadix, False, defaultNumerals )
        count += 1

    return convertToBase10( '0', result, inputRadix )


#//******************************************************************************
#//
#//  getCopelandErdos
#//
#//******************************************************************************

def getCopelandErdos( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += str( getNthPrime( count ) )
        count += 1

    return convertToBase10( '0', result, 10 )


#//******************************************************************************
#//
#//  makeImaginary
#//
#//******************************************************************************

def makeImaginary( n ):
    return mpc( real='0.0', imag=n )


#//******************************************************************************
#//
#//  isSquare
#//
#//******************************************************************************

def isSquare( n ):
    sqrt_n = sqrt( n )

    return 1 if sqrt_n == floor( sqrt_n ) else 0


#//******************************************************************************
#//
#//  solvePolynomial
#//
#//******************************************************************************

def solvePolynomial( args ):
    if len( args ) < 2:
        raise ValueError( "'solve' requires at least an order-1 polynomial (i.e., 2 terms)" )

    return polyroots( args )


#//******************************************************************************
#//
#//  calculatePowerTower
#//
#//******************************************************************************

def calculatePowerTower( args ):
    result = args[ -1 ]

    for i in args[ -1 : : -1 ]:
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  calculatePowerTower2
#//
#//******************************************************************************

def calculatePowerTower2( args ):
    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  getAlternatingSum
#//
#//******************************************************************************

def getAlternatingSum( args ):
    result = args[ 0 ]

    for i in range( 1, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getAlternatingSum2
#//
#//******************************************************************************

def getAlternatingSum2( args ):
    result = args[ 0 ]

    for i in range( 0, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getGCDForTwo
#//
#//******************************************************************************

def getGCDForTwo( a, b ):
    a, b = fabs( a ), fabs( b )

    while a:
        b, a = a, fmod( b, a )

    return b


#//******************************************************************************
#//
#//  getGCD
#//
#//******************************************************************************

def getGCD( args ):
    result = max( args )

    for pair in itertools.permutations( args, 2 ):
        gcd = getGCDForTwo( *pair )

        if gcd < result:
            result = gcd

    return result


#//******************************************************************************
#//
#//  getGreedyEgyptianFraction
#//
#//******************************************************************************

def getGreedyEgyptianFraction( n, d ):
    if n > d:
        raise ValueError( "'solve' requires at least an order-1 polynomial (i.e., 2 terms)" )

    # Create a list to store the Egyptian fraction representation.
    result = [ ]

    rational = Fraction( int( n ), int( d ) )

    # Now, iteratively subtract out the largest unit fraction that may be
    # subtracted out until we arrive at a unit fraction.
    while True:
        # If the rational number has numerator 1, we're done.
        if rational.numerator == 1:
            result.append( rational )
            return result

        # Otherwise, find the largest unit fraction less than the current rational number.
        # This is given by the ceiling of the denominator divided by the numerator.
        unitFraction = Fraction( 1, rational.denominator // rational.numerator + 1 )

        result.append( unitFraction )

        # Subtract out this unit fraction.
        rational = rational - unitFraction

    return result


#//******************************************************************************
#//
#//  listOperators
#//
#//******************************************************************************

def listOperators( ):
    print( 'argument modifiers:' )

    for i in sorted( [ key for key in modifiers ] ):
        print( '   ' + i )

    print( )

    print( 'list operators:' )

    for i in sorted( [ key for key in list_operators ] ):
        print( '   ' + i )

    print( )

    print( 'list operators with 2 args:' )

    for i in sorted( [ key for key in list_operators_2 ] ):
        print( '   ' + i )

    print( )

    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    print( 'special operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    return [ int( i ) for i in RPN_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  dumpStats
#//
#//******************************************************************************

def dumpStats( ):
    print( '{:10,} operators\n'.format( len( modifiers ) + len( list_operators ) +
                                        len( list_operators_2 ) + len( operators ) ) )

    smallPrimes = loadSmallPrimes( )
    print( '{:10,} small primes,          max: {:,}'.format( len( smallPrimes ),
                                                         max( [ key for key in smallPrimes ] ) ) )

    largePrimes = loadLargePrimes( )
    print( '{:10,} large primes,          max: {:,}'.format( len( largePrimes ),
                                                         max( [ key for key in largePrimes ] ) ) )

    twinPrimes = loadTwinPrimes( )
    print( '{:10,} twin primes,           max: {:,}'.format( len( twinPrimes ),
                                                         max( [ key for key in twinPrimes ] ) ) )

    balancedPrimes = loadBalancedPrimes( )
    print( '{:10,} balanced primes        max: {:,}'.format( len( balancedPrimes ),
                                                         max( [ key for key in balancedPrimes ] ) ) )

    sophiePrimes = loadSophiePrimes( )
    print( '{:10,} Sophie Germain primes, max: {:,}'.format( len( sophiePrimes ),
                                                         max( [ key for key in sophiePrimes ] ) ) )

    cousinPrimes = loadCousinPrimes( )
    print( '{:10,} cousin primes,         max: {:,}'.format( len( cousinPrimes ),
                                                         max( [ key for key in cousinPrimes ] ) ) )

    sexyPrimes = loadSexyPrimes( )
    print( '{:10,} sexy primes,           max: {:,}'.format( len( sexyPrimes ),
                                                         max( [ key for key in sexyPrimes ] ) ) )

    tripletPrimes = loadTripletPrimes( )
    print( '{:10,} triplet primes,        max: {:,}'.format( len( tripletPrimes ),
                                                         max( [ key for key in tripletPrimes ] ) ) )

    quadPrimes = loadQuadrupletPrimes( )
    print( '{:10,} quadruplet primes,     max: {:,}\n'.format( len( quadPrimes ),
                                                           max( [ key for key in quadPrimes ] ) ) )

    return [ int( i ) for i in RPN_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  incrementNestedListLevel
#//
#//******************************************************************************

def incrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel += 1

    valueList.append( list( ) )


#//******************************************************************************
#//
#//  decrementNestedListLevel
#//
#//******************************************************************************

def decrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel -= 1

    if nestedListLevel < 0:
        raise ValueError( "negative list level (too many ']'s)" )


#//******************************************************************************
#//
#//  duplicateTerm
#//
#//******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, int( count ) ):
        if isinstance( value, list ):
            for i in value:
                valueList.append( i )
        else:
            valueList.append( value )


#//******************************************************************************
#//
#//  expandRange
#//
#//******************************************************************************

def expandRange( valueList ):
    end = valueList.pop( )
    start = valueList.pop( )

    if start > end:
        step = -1
    else:
        step = 1

    for i in arange( start, end + step, step ):
        valueList.append( i )


#//******************************************************************************
#//
#//  expandSteppedRange
#//
#//******************************************************************************

def expandSteppedRange( valueList ):
    step = valueList.pop( )
    end = valueList.pop( )
    start = valueList.pop( )

    for i in arange( start, end + 1, step ):
        valueList.append( i )


#//******************************************************************************
#//
#//  expandGeometricRange
#//
#//******************************************************************************

def expandGeometricRange( valueList ):
    count = int( valueList.pop( ) )
    step = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, count ):
        valueList.append( value )
        value = fmul( value, step )


#//******************************************************************************
#//
#//  interleave
#//
#//******************************************************************************

def interleave( valueList ):
    arg2 = valueList.pop( )
    arg1 = valueList.pop( )

    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            combined = list( zip( arg1, arg2  ) )
            combined = [ item for sublist in combined for item in sublist ]

            for i in combined:
                result.append( i )
        else:
            for i in arg1:
                result.append( i )
                result.append( arg2 )
    else:
        if list2:
            for i in arg2:
                result.append( arg1 )
                result.append( i )
        else:
            result.append( arg1 )
            result.append( arg2 )

    valueList.append( result )


#//******************************************************************************
#//
#//  getPrimes
#//
#//******************************************************************************

def getPrimes( valueList ):
    count = int( valueList.pop( ) )
    value = int( valueList.pop( ) )

    for i in getNthPrimeRange( value, count ):
        valueList.append( i )


#//******************************************************************************
#//
#//  countElements
#//
#//******************************************************************************

def countElements( valueList ):
    value = valueList.pop( )

    if isinstance( value, list ):
        return len( value )
    else:
        return 1


#//******************************************************************************
#//
#//  getCurrentArgList
#//
#//******************************************************************************

def getCurrentArgList( valueList ):
    global nestedListLevel

    argList = valueList

    for i in range( 0, nestedListLevel ):
        argList = argList[ -1 ]

    return argList


#//******************************************************************************
#//
#//  twoArgCaller
#//
#//******************************************************************************

def twoArgCaller( func, args ):
    arg1 = args[ 0 ]
    arg2 = args[ 1 ]

    #print( "arg1: " + str( arg1 ) )
    #print( "arg2: " + str( arg2 ) )

    list1 = len( arg1 ) > 1
    list2 = len( arg2 ) > 1

    #print( list1 )
    #print( list2 )

    if list1:
        if list2:
            return [ func( arg2[ index ], arg1[ index ] ) for index in range( 0, len( arg1 ) ) ]
        else:
            return [ func( arg2[ 0 ], i ) for i in arg1 ]

    else:
        if list2:
            return [ func( j, arg1[ 0 ] ) for j in arg2 ]
        else:
            return [ func( arg2[ 0 ], arg1[ 0 ] ) ]



#//******************************************************************************
#//
#//  operators
#//
#//******************************************************************************

modifiers = {
    'dup'       : duplicateTerm, #2 ],
    'range'     : expandRange, #2 ],
    'range2'    : expandSteppedRange, #3 ],
    'georange'  : expandGeometricRange, #3 ],
    'interleave': interleave, #2 ],
    'primes'    : getPrimes, #2 ]
    '['         : incrementNestedListLevel, #0 ],
    ']'         : decrementNestedListLevel, #0 ],
}


callers = [
    lambda func, args: [ func( ) ],
    lambda func, args: [ func( i ) for i in args[ 0 ] ],
    twoArgCaller,
    lambda func, args: [ func( k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] ],
    lambda func, args: [ func( l, k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] for l in args[ 3 ] ],
    lambda func, args: [ func( m, l, k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] for l in args[ 3 ] for m in args[ 4 ] ],
]


list_operators = {
    'altsum'    : getAlternatingSum,
    'altsum2'   : getAlternatingSum2,
    'average'   : lambda i: fdiv( fsum( i ), len( i ) ),
    'avg'       : lambda i: fdiv( fsum( i ), len( i ) ),
    'cf2'       : convertFromContinuedFraction,
    'gcd'       : getGCD,
    'mean'      : lambda i: fdiv( fsum( i ), len( i ) ),
    'nonzero'   : lambda i: [ index for index, e in enumerate( i ) if e != 0 ],
    'nonzeroes' : lambda i: [ index for index, e in enumerate( i ) if e != 0 ],
    'prod'      : fprod,
    'product'   : fprod,
    'solve'     : solvePolynomial,
    'sum'       : fsum,
    'tower'     : calculatePowerTower,
    'tower2'    : calculatePowerTower2,
    'zeroes'    : lambda i: [ index for index, e in enumerate( i ) if e == 0 ],
}

list_operators_2 = {
    'base'      : interpretAsBase,
    'polyval'   : polyval,
}

operators = {
    '!!'          : [ fac2, 1 ],
    '!'           : [ fac, 1 ],
    '%'           : [ fmod, 2 ],
    '*'           : [ fmul, 2 ],
    '**'          : [ power, 2 ],
    '***'         : [ tetrate, 2 ],
    '+'           : [ fadd, 2 ],
    '-'           : [ fsub, 2 ],
    '/'           : [ fdiv, 2 ],
    '//'          : [ root, 2 ],
    '1/x'         : [ lambda i: fdiv( 1, i ), 1 ],
    'abs'         : [ fabs, 1 ],
    'acos'        : [ acos, 1 ],
    'acosh'       : [ acosh, 1 ],
    'acosh'       : [ acosh, 1 ],
    'acot'        : [ acot, 1 ],
    'acoth'       : [ acoth, 1 ],
    'acsc'        : [ acsc, 1 ],
    'acsch'       : [ acsch, 1 ],
    'add'         : [ fadd, 2 ],
    'and'         : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x & y ), 2 ],
    'antihex'     : [ getAntiHexagonalNumber, 1 ],
    'antipent'    : [ lambda i: fdiv( fadd( sqrt( fadd( fmul( 24 , i ), 1 ) ), 1 ), 6 ), 1 ],
    'antitri'     : [ getAntiTriangularNumber, 1 ],
    'apery'       : [ apery, 0 ],
    'asec'        : [ asec, 1 ],
    'asech'       : [ asech, 1 ],
    'asin'        : [ asin, 1 ],
    'asinh'       : [ asinh, 1 ],
    'atan'        : [ atan, 1 ],
    'atanh'       : [ atanh, 1 ],
    'bal'         : [ getNthBalancedPrimes, 1 ],
    'balanced'    : [ getNthBalancedPrimes, 1 ],
    'bernoulli'   : [ bernoulli, 1 ],
    'binomial'    : [ binomial, 2 ],
    'catalan'     : [ catalan, 0 ],
    'cbrt'        : [ cbrt, 1 ],
    'ccube'       : [ getNthCenteredCubeNumber, 1 ],
    'ceil'        : [ ceil, 1 ],
    'cf'          : [ lambda i, j: ContinuedFraction( i, maxterms=j, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2 ],
    'champ'       : [ getChampernowne, 0 ],
    'copeland'    : [ getCopelandErdos, 0 ],
    'cos'         : [ cos, 1 ],
    'cosh'        : [ cosh, 1 ],
    'cot'         : [ cot, 1 ],
    'coth'        : [ coth, 1 ],
    'cousin'      : [ getNthCousinPrimes, 1 ],
    'cousinprime' : [ getNthCousinPrimes, 1 ],
    'csc'         : [ csc, 1 ],
    'csch'        : [ csch, 1 ],
    'cube'        : [ lambda i: power( i, 3 ), 1 ],
    'deg'         : [ radians, 1 ],
    'degrees'     : [ radians, 1 ],
    'e'           : [ e, 0 ],
    'egypt'       : [ getGreedyEgyptianFraction, 2 ],
    'euler'       : [ euler, 0 ],
    'exp'         : [ exp, 1 ],
    'exp10'       : [ lambda i: power( 10, i ), 1 ],
    'expphi'      : [ phi, 1 ],
    'fac'         : [ fac, 1 ],
    'fac2'        : [ fac2, 1 ],
    'factor'      : [ lambda i: getExpandedFactorList( factorize( i ) ), 1 ],
    'fib'         : [ fib, 1 ],
    'floor'       : [ floor, 1 ],
    'frac'        : [ interpretAsFraction, 2 ],
    'fraction'    : [ interpretAsFraction, 2 ],
    'gamma'       : [ gamma, 1 ],
    'glaisher'    : [ glaisher, 0 ],
    'harm'        : [ harmonic, 1 ],
    'harmonic'    : [ harmonic, 1 ],
    'hex'         : [ lambda i: fsub( fprod( 2, i, i ), i ), 1 ],
    'hyper4'      : [ tetrate, 2 ],
    'hyper4_2'    : [ tetrateLarge, 2 ],
    'hyperfac'    : [ hyperfac, 1 ],
    'hypot'       : [ hypot, 2 ],
    'i'           : [ makeImaginary, 1 ],
    'inv'         : [ lambda i: fdiv( 1, i ), 1 ],
    'isdiv'       : [ lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2 ],
    'isprime'     : [ lambda i: 1 if isPrime( i ) else 0, 1 ],
    'issqr'       : [ isSquare, 1 ],
    'issquare'    : [ isSquare, 1 ],
    'itoi'        : [ lambda: exp( fmul( -0.5, pi ) ), 0 ],
    'khinchin'    : [ khinchin, 0 ],
    'lambertw'    : [ lambertw, 1 ],
    'lgamma'      : [ loggamma, 1 ],
    'ln'          : [ ln, 1 ],
    'log'         : [ ln, 1 ],
    'log10'       : [ log10, 1 ],
    'logxy'       : [ log, 2 ],
    'luc'         : [ getNthLucas, 1 ],
    'lucas'       : [ getNthLucas, 1 ],
    'mertens'     : [ mertens, 0 ],
    'mod'         : [ fmod, 2 ],
    'modulo'      : [ fmod, 2 ],
    'mulitply'    : [ fmul, 2 ],
    'mult'        : [ fmul, 2 ],
    'neg'         : [ fneg, 1 ],
    'npr'         : [ getPermutations, 2 ],
    'nPr'         : [ getPermutations, 2 ],
    'oct'         : [ getNthOctahedralNumber, 1 ],
    'octahedral'  : [ getNthOctahedralNumber, 1 ],
    'omega'       : [ lambda: lambertw( 1 ), 0 ],
    'or'          : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2 ],
    'pent'        : [ lambda i: fdiv( fsub( fprod( [ 3, i, i ] ), i ), 2 ), 1 ],
    'pentatope'   : [ getNthPentatopeNumber, 1 ],
    'perm'        : [ getPermutations, 2 ],
    'phi'         : [ phi, 0 ],
    'pi'          : [ pi, 0 ],
    'plastic'     : [ getPlasticConstant, 0 ],
    'polygamma'   : [ psi, 2 ],
    'polyprime'   : [ getNthPolyPrime, 2 ],
    'polytope'    : [ getNthPolytopeNumber, 2 ],
    'power'       : [ power, 2 ],
    'primorial'   : [ getPrimorial, 1 ],
    'prime'       : [ getNthPrime, 1 ],
    'prime?'      : [ findPrimeIndex, 1 ],
    'primepi'     : [ primepi, 1 ],
    'psi'         : [ psi, 2 ],
    'pyr'         : [ getNthPyramidalNumber, 1 ],
    'pyramid'     : [ getNthPyramidalNumber, 1 ],
    'quad'        : [ getNthQuadrupletPrimes, 1 ],
    'quadprime'   : [ getNthQuadrupletPrimes, 1 ],
    'rad'         : [ degrees, 1 ],
    'radians'     : [ degrees, 1 ],
    'rand'        : [ rand, 0 ],
    'random'      : [ rand, 0 ],
    'rhombdodec'  : [ getNthRhombicDodecahedralNumber, 1 ],
    'root'        : [ root, 2 ],
    'root2'       : [ sqrt, 1 ],
    'root3'       : [ cbrt, 1 ],
    'round'       : [ lambda i: floor( fadd( i, 0.5 ) ), 1 ],
    'sec'         : [ sec, 1 ],
    'sech'        : [ sech, 1 ],
    'sexy'        : [ getNthSexyPrimes, 1 ],
    'sexyprime'   : [ getNthSexyPrimes, 1 ],
    'sin'         : [ sin, 1 ],
    'sinh'        : [ sinh, 1 ],
    'solve2'      : [ solveQuadraticPolynomial, 3 ],
    'solve3'      : [ solveCubicPolynomial, 4 ],
    'solve4'      : [ solveQuarticPolynomial, 5 ],
    'sophie'      : [ getNthSophiePrime, 1 ],
    'sqr'         : [ lambda i: power( i, 2 ), 1 ],
    'sqrt'        : [ sqrt, 1 ],
    'sqtri'       : [ getNthSquareTriangularNumber, 1 ],
    'steloct'     : [ getNthStellaOctangulaNumber, 1 ],
    'sub'         : [ fsub, 2 ],
    'subtract'    : [ fsub, 2 ],
    'superfac'    : [ superfac, 1 ],
    'superprime'  : [ getNthSuperPrime, 1 ],
    'syl'         : [ getNthSylvester, 1 ],
    'sylvester'   : [ getNthSylvester, 1 ],
    'tan'         : [ tan, 1 ],
    'tanh'        : [ tanh, 1 ],
    'tet'         : [ lambda i: fdiv( fsum( [ power( i, 3 ), fmul( 3, power( i, 2 ) ), fmul( 2, i ) ] ), 6 ), 1 ],
    'tetra'       : [ getNthTetrahedralNumber, 1 ],
    'tri'         : [ getNthTriangularNumber, 1 ],
    'triplet'     : [ getNthTripletPrimes, 1 ],
    'tripletprime': [ getNthTripletPrimes, 1 ],
    'truncoct'    : [ getNthTruncatedOctahedralNumber, 1 ],
    'trunctet'    : [ getNthTruncatedTetrahedralNumber, 1 ],
    'twin'        : [ getNthTwinPrimes, 1 ],
    'twinprime'   : [ getNthTwinPrimes, 1 ],
    'unitroots'   : [ lambda i: unitroots( int( i ) ), 1 ],
    'xor'         : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2 ],
    'zeta'        : [ zeta, 1 ],
    '^'           : [ power, 2 ],
    '_dumpbal'    : [ dumpBalancedPrimes, 0 ],
    '_dumpcousin' : [ dumpCousinPrimes, 0 ],
    '_dumpprimes' : [ dumpLargePrimes, 0 ],
    '_dumpquad'   : [ dumpQuadrupletPrimes, 0 ],
    '_dumpsexy'   : [ dumpSexyPrimes, 0 ],
    '_dumpsmall'  : [ dumpSmallPrimes, 0 ],
    '_dumpsophie' : [ dumpSophiePrimes, 0 ],
    '_dumptriplet': [ dumpTripletPrimes, 0 ],
    '_dumptwin'   : [ dumpTwinPrimes, 0 ],
    '_listops'    : [ listOperators, 0 ],
    '_makebal'    : [ makeBalancedPrimes, 3 ],
    '_makecousin' : [ makeCousinPrimes, 3 ],
    '_makeprimes' : [ makeLargePrimes, 3 ],
    '_makequad'   : [ makeQuadrupletPrimes, 3 ],
    '_makesexy'   : [ makeSexyPrimes, 3 ],
    '_makesmall'  : [ makeSmallPrimes, 3 ],
    '_makesophie' : [ makeSophiePrimes, 3 ],
    '_makesuper'  : [ makeSuperPrimes, 2 ],
    '_maketriplet': [ makeTripletPrimes, 3 ],
    '_maketwin'   : [ makeTwinPrimes, 3 ],
    '_stats'      : [ dumpStats, 0 ],
    '~'           : [ getInvertedBits, 1 ],
#   'antitet'     : [ getAntiTetrahedralNumber, 1 ],
#   'bernfrac'    : [ bernfrac, 1 ],
#   'powmod'      : [ getPowMod, 3 ],
#   'count'       : [ countElements, 1 ],
}


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  Parse out a numerical expression and attempt to set the precision to an
#//  appropriate value based on the expression.
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
    if term == '0':
        return mpmathify( 0 )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return mpmathify( term )

        decimal = term.find( '.' )
    else:
        decimal = len( term )

    negative = term[ 0 ] == '-'

    if negative:
        start = 1
    else:
        if term[ 0 ] == '+':
            start = 1
        else:
            start = 0

    integer = term[ start : decimal ]
    mantissa = term[ decimal + 1 : ]

    # check for hex, then binary, then octal, otherwise a plain old decimal integer
    if not ignoreSpecial and mantissa == '':
        if integer[ 0 ] == '0':
            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


#//******************************************************************************
#//
#//  roundMantissa
#//
#//******************************************************************************

def roundMantissa( mantissa, accuracy ):
    if len( mantissa ) <= accuracy:
        return mantissa

    last_digit = int( mantissa[ accuracy - 1 ] )
    extra_digit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extra_digit >= 5:
        result += str( last_digit + 1 )
    else:
        result += str( last_digit )

    return result


#//******************************************************************************
#//
#//  formatOutput
#//
#//  This takes a string representation of the result and formats it according
#//  to a whole bunch of options.
#//
#//******************************************************************************

def formatOutput( output, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                  decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    imaginary = im( mpmathify( output ) )

    if imaginary != 0:
        if imaginary < 0:
            imaginary = fabs( imaginary )
            negativeImaginary = True
        else:
            negativeImaginary = False

        imaginaryValue = formatOutput( nstr( imaginary, mp.dps ), radix, numerals, integerGrouping,
                                       integerDelimiter, leadingZero, decimalGrouping, decimalDelimiter,
                                       baseAsDigits, outputAccuracy )

        strOutput = str( re( mpmathify( output ) ) )
    else:
        imaginaryValue = ''
        strOutput = str( output )

    if '.' in strOutput and strOutput.find( 'e' ) == -1:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    strResult = '';

    integer = strOutput[ 1 if negative else 0 : decimal ]
    integerLength = len( integer )

    mantissa = strOutput[ decimal + 1 : ]

    if mantissa != '':
        if outputAccuracy == -1:
            mantissa = mantissa.rstrip( '0' )

    #print( "mantissa: %s" % mantissa )
    #print( "output: %s" % output )

    if radix == phiBase:
        integer, mantissa = convertToPhiBase( mpmathify( output ) )
    elif radix == fibBase:
        integer = convertToFibBase( floor( mpmathify( output ) ) )
    elif radix != 10 or numerals != defaultNumerals:
        integer = str( convertToBaseN( mpmathify( integer ), radix, baseAsDigits, numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpmathify( '0.' + mantissa ), radix,
                            int( ( mp.dps - integerLength ) / math.log10( radix ) ),
                            baseAsDigits, outputAccuracy ) )
    else:
        if outputAccuracy == 0:
            mantissa = ''
        elif outputAccuracy > 0:
            mantissa = roundMantissa( mantissa, outputAccuracy )

    if integerGrouping > 0:
        firstDelimiter = len( integer ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += integer[ : firstDelimiter ]

        for i in range( firstDelimiter, len( integer ), integerGrouping ):
            if integerResult != '':
                integerResult += integerDelimiter

            integerResult += integer[ i : i + integerGrouping ]

    else:
        integerResult = integer

    if decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( mantissa ), decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += decimalDelimiter

            mantissaResult += mantissa[ i : i + decimalGrouping ]
    else:
        mantissaResult = mantissa

    if negative:
        result = '-'
    else:
        result = ''

    result += integerResult

    if mantissaResult != '':
        result += '.' + mantissaResult

    if imaginaryValue != '':
        result = '( ' + result + ( ' - ' if negativeImaginary else ' + ' ) + imaginaryValue + 'j )'

    return result



#//******************************************************************************
#//
#//  formatListOutput
#//
#//******************************************************************************

def formatListOutput( result, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                      decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    resultString = ''

    for item in result:
        if resultString == '':
            resultString = '[ '
        else:
            resultString += ', '

        if isinstance( item, list ):
            resultString += formatListOutput( item, radix, numerals, integerGrouping, integerDelimiter,
                                              leadingZero, decimalGrouping, decimalDelimiter, baseAsDigits,
                                              outputAccuracy )
        else:
            itemString = nstr( item, mp.dps )

            resultString += formatOutput( itemString, radix, numerals, integerGrouping, integerDelimiter,
                                          leadingZero, decimalGrouping, decimalDelimiter, baseAsDigits,
                                          outputAccuracy )

    resultString += ' ]'

    return resultString


#//******************************************************************************
#//
#//  printMoreHelp
#//
#//******************************************************************************

def printMoreHelp( ):
    print(
'''
Arguments are interpreted as Reverse Polish Notation.

Supported unary operators (synonyms are separated by commas):
    !, fac; !!, fac2 (double factorial); %, mod, modulo; 1/x, inv (take
    reciprocal); abs; cbrt, root3 (cube root); ceil; cube; exp; exp10; expphi;
    fac2 (double factorial) floor; gamma; hypot; hyperfac; isdiv; isprime;
    lgamma; log, ln; log10; neg; rand; round; sqr; sqrt, root2; superfac

Supported unary trigonometric operators:
    deg, degrees (treat term as degrees (i.e., convert to radians), e.g.,
    "rpn 45 degrees tan"); rad, radians (treat term as radians (i.e., convert
    to degrees), e.g., "rpn pi radians")

    sin; asin; sinh; asinh; cos; acos; cosh; acosh; tan; atan; tanh; atanh;
    sec; asec; sech; asech; csc; acsc; csch; acsch; cot; acot; coth; acoth

Supported integer sequence unary operators:
    fib (nth Fibonacci number); luc, lucas (nth Lucas number); sylvester, syl
    (nth Sylvester number); tri (nth triangular number); antitri (which
    triangular number is this); pent (nth pentagonal number); antipent (which
    pentagonal number is this); hex (nth hexagonal number); antihex (which
    hexagonal number is this); sqtri (nth square triangular number)*; tet,
    tetra (nth tetrahedral number); prime (nth prime); twin (nth twin prime);
    bal, balanced (nth balanced prime); cousin (nth cousin prime); sexy
    (nth sexy prime); sophie (nth Sophie Germain prime); triplet (nth prime
    triplet); quad (nth prime quadruplet)

    * requires sufficient precision for accuracy (see Notes)

Supported binary operators:
    +, add; -, sub; *, mult; /, div; **, ^, power; ***, mod, modulo, %; hyper4
    (tetration); hyper4_2 (tetration, right-associative); //, root; logxy;
    binomial, nCr, ncr (binomial coefficient (combinations)); perm, nRp, nrp
    (permutations)

Supported list operators (requires a list as an operand):
    sum; prod; mean, avg, average; cf (treat as a continued fraction);
    base (sort of the reverse of -R, with the base being the last argument);
    solve (solve polynomial), altsum (sum terms, alternating add and subtract);
    altsum2 (sum terms, alternating subtract and add); tower (calculate power
    tower), tower2 (calculate left-associative power tower), nonzero, zero,
    index

Supported constants:
    e; pi; phi (the Golden Ratio); itoi (i^i); euler (Euler's constant);
    catalan (Catalan's constant); apery (Apery's constant); khinchin
    (Khinchin's constant); glaisher (Glaisher's constant); mertens (Merten's
    constant); twinprime (Twin prime constant), omega (Omega constant)

Supported bitwise operators:
    ~, not; and; or; xor

Polynomial solvers:
    solve2 (solve quadratic equation, 3 args)
    solve3 (solve cubic equation, 4 args)
    solve4 (solve quartic equation, 5 args)
    solve  (solve arbitrary polynomial, list of coefficients followed by
            the number of coefficients )

Argument modifiers:
    dup; range; range2; georange; interleave; primes; [; ]

Input:
    For integers, rpn understands hexidecimal input of the form '0x....'.
    Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B'
    is interpreted as binary.  Decimal points are not allowed for binary,
    octal or hexadecimal modes, but fractional numbers in another base can be
    input using -b.

    A leading '\\' forces the term to be a number rather than an operator (for
    use with higher bases with -b).

Notes:
    When converting fractional output to other bases, rpn adjusts the precision
    to the approximate equivalent for the new base since the precision is
    applicable to base 10.

    Tetration (hyperexponentiation) forces the second argument to an integer.

    To compute the nth Fibonacci number accurately, rpn sets the precision to
    a level sufficient to guarantee a correct answer.

    Some of the trig functions return complex results as provided by mpmath,
    but rpn doesn't otherwise support complex numbers.

    Bitwise operators force all arguments to integers by truncation if
    necessary.
''' )


#//******************************************************************************
#//
#//  printEvenMoreHelp
#//
#//******************************************************************************

def printEvenMoreHelp( ):
    print(
'''
Examples of rpn usage follow.

Basic arithmetic operations:

    c:\>rpn 2 3 +
    5

    c:\>rpn 12 9 -
    3

    c:\>rpn 23 47 *
    1081

    c:\>rpn 10 7 /
    1.42857142857

Basic trigonometry usage:

    c:\>rpn 60 deg sin         # sine of 60 degrees
    0.866025403784

    c:\>rpn 45 deg tan         # tangent of 45 degrees
    1

    c:\>rpn 2 pi * rad         # 2 pi radians is how many degrees?
    360

    c:\>rpn 2 atan rad         # What angle (in degrees) has a slope of 2?
    63.4349488229

Convert an IP address to a 32-bit value and back:

    c:\>rpn [ 192 168 0 1 ] 256 base -x
    c0a8 0001

    c:\>rpn 0xc0a80001 -R 256
    192 168 0 1

Construct the square root of two from a continued fraction:

    c:\>rpn -p20 2 sqrt
    1.41421356237309504880

    c:\>rpn -p20 2 sqrt 20 cf2
    [ 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ]

    c:\>rpn -p20 2 sqrt 20 frac
    [ 22619537, 15994428 ]

    c:\>rpn -p20 [ 1 2 30 ] dup cf
    1.41421356237309504880

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        rpn [ 1 50 range ] fib isprime nonzero 1 + fib

Calculate various constants:

    Polya Random Walk Constant
        = rpn -p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 /
                    gamma 7 24 / gamma 11 24 / gamma ] prod 1/x * -

    Schwartzchild Constant (Conic Constant)
        = rpn -p20 2 [ 0 30 range ] ** [ 0 30 range ] ! / sum
        = rpn -p20 e 2 **

    Somos\' Quadratic Recurrence Constant
        = rpn -p20 [ 1 100 range ] [ 0.5 0.5 100 georange ] ** prod

    Prevost Constant
        = rpn -p20 [ 1 100 range ] fib 1/x sum

    Euler's number = rpn -p20 [ 0 100 range ] fac 1/x sum
                   = rpn -p20 e

    Gelfond Constant
        = rpn -p20 pi [ 0 100 range ] power [ 0 100 range ] ! / sum
        = rpn -p20 e pi power

    Bloch-Landau Constant
        = rpn -p20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /

    Hausdorff Dimension
        = rpn -p20 2 [ 0 100 range ] 2 * 1 + power [ 0 100 range ] 2 * 1 + *
            1/x sum 3 [ 0 100 range ] 2 * 1 + power [ 0 100 range ] 2 * 1 +
            * 1/x sum /
        = rpn -p20 3 log 2 log /

    Machin-Gregory Series
        = rpn -p20 [ 1 1000 2 range2 ] 2 [ 1 1000 2 range2 ] power * 1/x altsum
        = rpn -p20 1 2 / atan

    Beta(3)
        = rpn -p17 [ 1 1000000 2 range2 ] 3 power 1/x altsum
        = rpn -p20 pi 3 power 32 /

    Cahen's constant
        = rpn -p20 [ 1 20 range ] sylvester 1 - 1/x altsum

    Lemniscate Constant
        = rpn -p20 4 2 pi / sqrt * 0.25 ! sqr *

    sqrt( e )
        = rpn -p20 2 [ 0 20 range ] power [ 0 20 range ] ! * 1/x sum
        = rpn -p20 [ 0 20 range ] 2 * !! 1/x sum
        = rpn -p20 e sqrt

    1/e
        = rpn -p20 [ 0 25 range ] fac 1/x altsum
        = rpn -p20 e 1/x

    Zeta( 6 )
        = rpn -p25 -a19 1 1 1000 primes -6 power - 1/x prod
        = rpn -p20 pi 6 power 945 /
        = rpn -p20 6 zeta

    Pythagoras' constant
        = rpn -p20 [ 1 2 25 dup ] cf
        = rpn -p20 2 sqrt

    Digamma
        = rpn -p25 -a20 1 1 1000 primes -6 power - 1/x prod
        = rpn -a5 [ 0 100000 range ] 1 + 1/x
                        [ 0 100000 range ] 1 4 / + 1/x - sum euler -

    Strongly Carefree Constant
        = rpn -a6 1 [ 1 100000 primes ] 3 * 2 -
                [ 1 100000 primes ] 3 power / - prod
        = rpn -a7 6 pi sqr / 1 2
                [ 1 100000 primes ] [ 1 100000 primes ] 1 + * 1/x * - prod *

    Ramanujan-Forsythe Constant
        = rpn [ 0 100000 range ] 2 * 3 - fac2
                [ 0 100000 range ] 2 * fac2 / sqr sum

    Apery's Constant
        = rpn -p20 [ 1 5000 range ] 3 power 1/x sum
        = rpn -p20  3 zeta
        = rpn -p20 apery

    Omega Constant
        = rpn -p20 [ e 1/x 100 dup ] tower
        = rpn -p20 omega

    Liouville Number
        = rpn -p120 10 [ 1 10 range ] ! power 1/x sum

    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                [ 0 100000 range ] 3 * 2 + sqr 1/x sum -
                [ 1 100000 range ] 3 * 1 + sqr 1/x sum + *

    Hafner-Sarnak-McCurley Constant (2)
        = rpn -a7 1 [ 1 100000 primes ] sqr 1/x - prod
        = rpn 2 zeta 1/x

    Infinite Tetration of i
        = rpn -p20 [ 1 i 1000 dup ] tower

''' )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global addToListArgument
    global balancedPrimes
    global bitwiseGroupSize
    global cousinPrimes
    global dataPath
    global inputRadix
    global largePrimes
    global nestedListLevel
    global numerals
    global quadPrimes
    global sexyPrimes
    global smallPrimes
    global sophiePrimes
    global superPrimes
    global tripletPrimes
    global twinPrimes
    global updateDicts

    # initialize globals
    nestedListLevel = 0

    balancedPrimes = { }
    cousinPrimes = { }
    smallPrimes = { }
    largePrimes = { }
    quadPrimes = { }
    sexyPrimes = { }
    sophiePrimes = { }
    superPrimes = { }
    tripletPrimes = { }
    twinPrimes = { }

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' )

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + RPN_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=-1, const=defaultAccuracy,
                         help="maximum number of decimal places to display, irrespective\nof internal precision (default:  " +
                              str( defaultAccuracy ) + ")" )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix,
                         help="specify the radix for input (default:  " + str( defaultInputRadix ) + ")" )
    parser.add_argument( '-c', '--comma', action='store_true',
                         help="add commas to result, e.g., 1,234,567.0" )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping, help="display decimal places separated into groups (default: " +
                                                            str( defaultDecimalGrouping ) + ")" )
    parser.add_argument( '-hh', '--more_help', action='store_true',
                         help="display additional help information" )
    parser.add_argument( '-hhh', '--even_more_help', action='store_true',
                         help="display examples of various rpn functionality in use" )
    parser.add_argument( '-i', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping,
                         help="display integer separated into groups (default: " + str( defaultIntegerGrouping ) + ")" )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals,
                         help="characters set to use as numerals for output" )
    parser.add_argument( '-o', '--octal', action='store_true', help="octal mode: equivalent to '-r8 -w9 -i3 -z'" )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision,
                         help="precision, i.e., number of significant digits to use" )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix,
                         help="output in a different base (2 to 62, or phi)" )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0,
                         help="each digit is a space-delimited base-10 number" )
    parser.add_argument( '-t', '--time', action='store_true', help="display calculation time" )
    parser.add_argument( '-u', '--find_poly', type=int, action='store', default=0,
                         help="find a polynomial such that P(x) ~= 0 of degree <= N" )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store', default=defaultBitwiseGroupSize,
                         help="bitwise operations group values by this size (default: " +
                              str( defaultBitwiseGroupSize ) + ")" )
    parser.add_argument( '-x', '--hex', action='store_true', help="hex mode: equivalent to '-r16 -w16 -i4 -z'" )
    parser.add_argument( '-y', '--identify', action='store_true', help="identify the result (may repeat input)" )
    parser.add_argument( '-z', '--leading_zero', action='store_true', help="add leading zeros if needed with -i" )
    parser.add_argument( '-?', '--print_options', action='store_true', help="print values for all options" )

    # OK, let's parse and validate the arguments
    if len( sys.argv ) == 1:
        parser.print_help( )
        return

    args = parser.parse_args( )
    mp.dps = args.precision

    if args.more_help:
        printMoreHelp( )
        return

    if args.even_more_help:
        printEvenMoreHelp( )
        return

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( "rpn:  can't interpret output radix '%s' as a number" % args.output_radix )
            return

    numerals = args.numerals

    # handle -x
    if args.hex:
        if outputRadix != 10 and outputRadix != 16:
            print( "rpn:  -r and -x can't be used together" )
            return

        if args.octal:
            print( "rpn:  -x and -o can't be used together" )
            return

        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        if outputRadix != 10 and outputRadix != 8:
            print( "rpn:  -r and -o can't be used together" )
            return

        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        bitwiseGroupSize = 9

    # handle -b
    inputRadix = int( args.input_radix )

    # handle -R
    if args.output_radix_numerals > 0:
        if args.hex:
            print( "rpn:  -R and -x can't be used together" )
            return

        if args.output_radix != 10:
            print( "rpn:  -R and -r can't be used together" )
            return

        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( "rpn:  output radix must be greater than 1" )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( "rpn:  output radix must be from 2 to 62, or phi" )
            return

    if args.comma and args.integer_grouping > 0 :
        print( "rpn:  -c can't be used with -i" )
        return

    if baseAsDigits and ( args.comma or args.decimal_grouping > 0 or args.integer_grouping > 0 ):
        print( "rpn:  -c, -d and -i can't be used with -R" )
        return

    # handle -y and -u:  mpmath wants precision of at least 53 for these functions
    if args.identify or args.find_poly > 0:
        if mp.dps < 53:
            mp.dps = 53

    index = 1                 # only used for error messages
    valueList = list( )

    if args.print_options:
        print( '--output_accuracy:  %d' % args.output_accuracy )
        print( '--input_radix:  %d'% inputRadix )
        print( '--comma:  ' + ( 'true' if args.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % args.decimal_grouping )
        print( '--integer_grouping:  %d' % integerGrouping )
        print( '--numerals:  ' + args.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % args.output_radix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--time:  ' + ( 'true' if args.time else 'false' ) )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

    if len( args.terms ) == 0:
        print( "rpn:  no terms found" )
        return

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        currentValueList = getCurrentArgList( valueList )

        if term in modifiers:
            try:
                modifiers[ term ]( currentValueList )
            except IndexError as error:
                print( "rpn:  index error for operator at arg " + format( index ) +
                       ".  Are your arguments in the right order?" )
                break
        elif term in operators:
            argsNeeded = operators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( "rpn:  error in arg " + format( index ) + ":  operator " + term + " requires " +
                       format( argsNeeded ) + " argument", end='' )

                if argsNeeded > 1:
                    print( "s" )
                else:
                    print( "" )

                break

            try:
                argList = list( )

                for i in range( 0, argsNeeded ):
                    arg = currentValueList.pop( )
                    argList.append( arg if isinstance( arg, list ) else [ arg ] )

                result = callers[ argsNeeded ]( operators[ term ][ 0 ], argList )

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )
            except KeyboardInterrupt as error:
                print( "rpn:  keyboard interrupt" )
                break
            except ValueError as error:
                print( "rpn:  error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
            except TypeError as error:
                print( "rpn:  type error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
        elif term in list_operators:
            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < 1:
                print( "rpn:  error in arg " + format( index ) + ":  operator " + term +
                       " requires a list argument" )
                break

            try:
                arg = currentValueList.pop( )
                currentValueList.append( list_operators[ term ]( arg ) )
            except KeyboardInterrupt as error:
                print( "rpn:  keyboard interrupt" )
                break
            except ValueError as error:
                print( "rpn:  error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
            except TypeError as error:
                print( "rpn:  type error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
            except IndexError as error:
                print( "rpn:  index error for operator at arg " + format( index ) +
                       ".  Are your arguments in the right order?" )
                break
        elif term in list_operators_2:
            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < 2:
                print( "rpn:  error in arg " + format( index ) + ":  operator " + term +
                       " requires two arguments" )
                break

            try:
                secondArg = currentValueList.pop( )
                listArg = currentValueList.pop( )

                if not isinstance( secondArg, list ):
                    secondArg = [ secondArg ]

                result = [ list_operators_2[ term ]( listArg, i ) for i in secondArg ]

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )
            except KeyboardInterrupt as error:
                print( "rpn:  keyboard interrupt" )
                break
            except ValueError as error:
                print( "rpn:  error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
            except TypeError as error:
                print( "rpn:  type error for operator at arg " + format( index ) + ":  {0}".format( error ) )
                break
        else:
            try:
                currentValueList.append( parseInputValue( term, inputRadix ) )
            except ValueError as error:
                print( "rpn:  error in arg " + format( index ) + ":  {0}".format( error ) )
                break
            except TypeError as error:
                print( "rpn:  error in arg " + format( index ) +
                       ":  unrecognized argument: '%s'" % sys.argv[ index ] )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1:
            print( "rpn:  unexpected end of input" )
        else:
            mp.pretty = True
            result = valueList.pop( )

            if args.comma:
                integerGrouping = 3     # override whatever was set on the command-line
                leadingZero = False     # this one, too
                integerDelimiter = ','
            else:
                integerDelimiter = ' '

            if isinstance( result, list ):
                print( formatListOutput( result, outputRadix, numerals, integerGrouping, integerDelimiter,
                                         leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                         args.output_accuracy ) )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                print( formatOutput( resultString, outputRadix, numerals, integerGrouping, integerDelimiter,
                                     leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                     args.output_accuracy ) )

                # handle --identify
                if args.identify:
                    formula = identify( result )

                    if formula is None:
                        base = [ 'pi', 'e' ]
                        formula = identify( result, base )

                    if formula is None:
                        base.append( 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' )
                        formula = identify( result, base )

                    if formula is None:
                        base.append( 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' )
                        formula = identify( result, base )

                    if formula is None:
                        print( '    = [formula cannot be found]' )
                    else:
                        print( '    = ' + formula )

                # handle --find_poly
                if args.find_poly > 0:
                    poly = str( findpoly( result, args.find_poly ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=10000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=100000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000, tol=1e-10 ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )

        if args.time:
            print( "\n%.3f seconds" % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

