#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpndata
#//
#//  Data maintenance utility for rpn
#//  copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import argparse
import bz2
import collections
import contextlib
import itertools
import math
import os
import pickle
import pyprimes
import random
import re as regex
import sys
import time
import types
import urllib.request

from fractions import Fraction
from functools import reduce
from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpndata'
RPN_VERSION = '0.0.0'
PROGRAM_DESCRIPTION = 'Data maintenance utility for rpn'
COPYRIGHT_MESSAGE = 'copyright (c) 2013, Rick Gutleber (rickg@his.com)'

defaultPrecision = 12
defaultAccuracy = 10
defaultCFTerms = 10
defaultBitwiseGroupSize = 16
defaultInputRadix = 10
defaultOutputRadix = 10
defaultDecimalGrouping = 5
defaultIntegerGrouping = 3

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

numerals = ''

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

def loadIsolatedPrimes( ):
    return loadTable( 'isolated_primes', { 2 : 23 } )

def loadTwinPrimes( ):
    return loadTable( 'twin_primes', { 3 : 11 } )

def loadBalancedPrimes( ):
    return loadTable( 'balanced_primes', { 2 : 5 } )

def loadDoubleBalancedPrimes( ):
    return loadTable( 'double_balanced_primes', { 1 : getNthDoubleBalancedPrimes( 1 ) } )

def loadTripleBalancedPrimes( ):
    return loadTable( 'triple_balanced_primes', { 1 : getNthTripleBalancedPrimes( 1 ) } )

def loadSophiePrimes( ):
    return loadTable( 'sophie_primes', { 4 : 11 } )

def loadCousinPrimes( ):
    return loadTable( 'cousin_primes', { 2 : 7 } )

def loadSexyPrimes( ):
    return loadTable( 'sexy_primes', { 2 : 7 } )

def loadSexyTripletPrimes( ):
    return loadTable( 'sexy_triplets', { 2 : 7 } )

def loadSexyQuadrupletPrimes( ):
    return loadTable( 'sexy_quadruplets', { 2 : 11 } )

def loadTripletPrimes( ):
    return loadTable( 'triplet_primes', { 2 : 7 } )

def loadQuadrupletPrimes( ):
    return loadTable( 'quad_primes', { 2 : 11 } )

def loadQuintupletPrimes( ):
    return loadTable( 'quint_primes', { 3 : 11 } )

def loadSextupletPrimes( ):
    return loadTable( 'sext_primes', { 1 : 7 } )


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

def saveIsolatedPrimes( isolatedPrimes ):
    saveTable( 'isolated_primes', isolatedPrimes )

def saveTwinPrimes( twinPrimes ):
    saveTable( 'twin_primes', twinPrimes )

def saveBalancedPrimes( balancedPrimes ):
    saveTable( 'balanced_primes', balancedPrimes )

def saveDoubleBalancedPrimes( doubleBalancedPrimes ):
    saveTable( 'double_balanced_primes', doubleBalancedPrimes )

def saveTripleBalancedPrimes( tripleBalancedPrimes ):
    saveTable( 'triple_balanced_primes', tripleBalancedPrimes )

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

def saveQuintupletPrimes( quintPrimes ):
    saveTable( 'quint_primes', quintPrimes )

def saveSextupletPrimes( sextPrimes ):
    saveTable( 'sext_primes', sextPrimes )


#//******************************************************************************
#//
#//  importTable
#//
#//******************************************************************************

def importTable( fileName, loadTableFunc, saveTableFunc  ):
    print( fileName )
    var = loadTableFunc( )

    with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
        imported = pickle.load( pickleFile )

    var.update( imported )

    saveTableFunc( var )

    return len( var )

def importSmallPrimes( fileName ):
    return importTable( fileName, loadSmallPrimes, saveSmallPrimes )

def importLargePrimes( fileName ):
    return importTable( fileName, loadLargePrimes, saveLargePrimes )

def importIsolatedPrimes( fileName ):
    return importTable( fileName, loadIsolatedPrimes, saveIsolatedPrimes )

def importTwinPrimes( fileName ):
    return importTable( fileName, loadTwinPrimes, saveTwinPrimes )

def importBalancedPrimes( fileName ):
    return importTable( fileName, loadBalancedPrimes, saveBalancedPrimes )

def importDoubleBalancedPrimes( fileName ):
    return importTable( fileName, loadDoubleBalancedPrimes, saveDoubleBalancedPrimes )

def importTripleBalancedPrimes( fileName ):
    return importTable( fileName, loadTripleBalancedPrimes, saveTripleBalancedPrimes )

def importSophiePrimes( fileName ):
    return importTable( fileName, loadSophiePrimes, saveSophiePrimes )

def importCousinPrimes( fileName ):
    return importTable( fileName, loadCousinPrimes, saveCousinPrimes )

def importSexyPrimes( fileName ):
    return importTable( fileName, loadSexyPrimes, saveSexyPrimes )

def importSexyTriplets( fileName ):
    return importTable( fileName, loadSexyTripletPrimes, saveSexyTriplets )

def importSexyQuadruplets( fileName ):
    return importTable( fileName, loadSexyQuadrupletPrimes, saveSexyQuadruplets )

def importTripletPrimes( fileName ):
    return importTable( fileName, loadTripletPrimes, saveTripletPrimes )

def importQuadrupletPrimes( fileName ):
    return importTable( fileName, loadQuadrupletPrimes, saveQuadrupletPrimes )

def importQuintupletPrimes( fileName ):
    return importTable( fileName, loadQuintupletPrimes, saveQuintupletPrimes )

def importSextupletPrimes( fileName ):
    return importTable( fileName, loadSextupletPrimes, saveSextupletPrimes )


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

def makeIsolatedPrimes( start, end, step ):
    global isolatedPrimes
    getNthIsolatedPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthIsolatedPrime, 'isolated' )
    saveIsolatedPrimes( isolatedPrimes )
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
    getNthTwinPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTwinPrime, 'twin' )
    saveTwinPrimes( twinPrimes )
    return end

def makeBalancedPrimes( start, end, step ):
    global balancedPrimes
    getNthBalancedPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthBalancedPrimes, 'balanced' )
    saveBalancedPrimes( balancedPrimes )
    return end

def makeDoubleBalancedPrimes( start, end, step ):
    global doubleBalancedPrimes
    end = makeTable( start, end, step, getNthDoubleBalancedPrimes, 'double_balanced' )
    saveDoubleBalancedPrimes( doubleBalancedPrimes )
    return end

def makeTripleBalancedPrimes( start, end, step ):
    global tripleBalancedPrimes
    end = makeTable( start, end, step, getNthTripleBalancedPrimes, 'triple_balanced' )
    saveTripleBalancedPrimes( tripleBalancedPrimes )
    return end

def makeSophiePrimes( start, end, step ):
    global sophiePrimes
    getNthSophiePrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSophiePrime, 'sophie' )
    saveSophiePrimes( sophiePrimes )
    return end

def makeCousinPrimes( start, end, step ):
    global cousinPrimes
    getNthCousinPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthCousinPrime, 'cousin' )
    saveCousinPrimes( cousinPrimes )
    return end

def makeSexyPrimes( start, end, step ):
    global sexyPrimes
    getNthSexyPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyPrime, 'sexy' )
    saveSexyPrimes( sexyPrimes )
    return end

def makeSexyTriplets( start, end, step ):
    global sexyTriplets
    getNthSexyTriplet( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyTriplet, 'sexytrip' )
    saveSexyTriplets( sexyTriplets )
    return end

def makeSexyQuadruplets( start, end, step ):
    global sexyQUadruplets
    getNthSexyQuadruplet( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyQuadruplet, 'sexyquad' )
    saveSexyQuadruplets( sexyQuadruplets )
    return end

def makeTripletPrimes( start, end, step ):
    global tripletPrimes
    getNthTripletPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTripletPrimes, 'triplet' )
    saveTripletPrimes( tripletPrimes )
    return end

def makeQuadrupletPrimes( start, end, step ):
    global quadPrimes
    getNthQuadrupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuadrupletPrime, 'quad' )
    saveQuadrupletPrimes( quadPrimes )
    return end

def makeQuintupletPrimes( start, end, step ):
    global quintPrimes
    getNthQuintupletPrimes( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuintupletPrimes, 'quint' )
    saveQuintupletPrimes( quintPrimes )
    return end

def makeSextupletPrimes( start, end, step ):
    global sextPrimes
    getNthSextupletPrimes( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthSextupletPrimes, 'sext' )
    saveSextupletPrimes( sextPrimes )
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

def dumpIsolatedPrimes( ):
    return dumpTable( loadIsolatedPrimes, 'isolated' )

def dumpTwinPrimes( ):
    return dumpTable( loadTwinPrimes, 'twin' )

def dumpBalancedPrimes( ):
    return dumpTable( loadBalancedPrimes, 'balanced' )

def dumpDoubleBalancedPrimes( ):
    return dumpTable( loadDoubleBalancedPrimes, 'double_balanced' )

def dumpTripleBalancedPrimes( ):
    return dumpTable( loadTripleBalancedPrimes, 'triple_balanced' )

def dumpSophiePrimes( ):
    return dumpTable( loadSophiePrimes, 'sophie' )

def dumpCousinPrimes( ):
    return dumpTable( loadCousinPrimes, 'cousin' )

def dumpSexyPrimes( ):
    return dumpTable( loadSexyPrimes, 'sexy' )

def dumpSexyTriplets( ):
    return dumpTable( loadSexyTripletPrimes, 'sexytrip' )

def dumpSexyQuadruplets( ):
    return dumpTable( loadSexyQuadrupletPrimes, 'sexyquad' )

def dumpTripletPrimes( ):
    return dumpTable( loadTripletPrimes, 'triplet' )

def dumpQuadrupletPrimes( ):
    return dumpTable( loadQuadrupletPrimes, 'quad' )

def dumpQuintupletPrimes( ):
    return dumpTable( loadQuintupletPrimes, 'quint' )

def dumpSextupletPrimes( ):
    return dumpTable( loadQSextupletPrimes, 'sext' )


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
#//  findNextPrime
#//
#//******************************************************************************

def findNextPrime( p, f, func = getNextPrimeCandidate ):
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

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

        currentIndex = max( key for key in largePrimes if key <= n )
        p = largePrimes[ currentIndex ]
    elif n >= 100:
        if smallPrimes == { }:
            smallPrimes = loadSmallPrimes( )

        currentIndex = max( key for key in smallPrimes if key <= n )
        p = smallPrimes[ currentIndex ]
    else:
        currentIndex = 4
        p = 7

    f = p % 10

    while n > currentIndex:
        p, f = findNextPrime( p, f )
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
    oldPrime = p

    while True:
        p, f = findNextPrime( p, f )
        currentIndex += 1

        if p > target:
            return currentIndex, p


#//******************************************************************************
#//
#//  findQuadrupletPrimes
#//
#//******************************************************************************

def findQuadrupletPrimes( arg ):
    global quadPrimes

    target = int( arg )

    if quadPrimes == { }:
        quadPrimes = loadQuadrupletPrimes( )

    currentIndex = max( key for key in quadPrimes if quadPrimes[ key ] <= target )
    p = quadPrimes[ currentIndex ]

    while True:
        p += 30

        if isPrime( p ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ):
            currentIndex += 1

            if p > target:
                return currentIndex, [ p, p + 2, p + 6, p + 8 ]


#//******************************************************************************
#//
#//  getNthIsolatedPrime
#//
#//******************************************************************************

def getNthIsolatedPrime( arg ):
    global isolatedPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 2

    if n == 2:
        return 23

    if n >= 100:
        if isolatedPrimes == { }:
            isolatedPrimes = loadIsolatedPrimes( )

        currentIndex = max( key for key in isolatedPrimes if key <= n )
        p = isolatedPrimes[ currentIndex ]
    else:
        currentIndex = 2
        p = 23

    f = p % 10

    while n > currentIndex:
        p, f = findNextPrime( p, f )

        if not isPrime( p - 2 ) and not isPrime( p + 2 ):
            currentIndex += 1

    if updateDicts:
        isolatedPrimes[ n ] = p

    return p


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
#//  getNthAlternatingFactorial
#//
#//******************************************************************************

def getNthAlternatingFactorial( n ):
    result = 0

    negative = False

    for i in arange( n, 0, -1 ):
        if negative:
            result = fadd( result, fneg( fac( i ) ) )
            negative = False
        else:
            result = fadd( result, fac( i ) )
            negative = True

    return result


#//******************************************************************************
#//
#//  getNthPascalLine
#//
#//******************************************************************************

def getNthPascalLine( n ):
    result = [ ]

    for i in arange( 0, n ):
        result.append( binomial( n - 1, i ) )

    return result


#//******************************************************************************
#//
#//  getNthTwinPrime
#//
#//******************************************************************************

def getNthTwinPrime( arg ):
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

        maxIndex = max( key for key in twinPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

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
#//  returns the first of a set of 3 balanced primes
#//
#//******************************************************************************

def getNthBalancedPrimes( arg ):
    global balancedPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 3
    elif n == 2:
        return 5

    if n >= 100:
        if balancedPrimes == { }:
            balancedPrimes = loadBalancedPrimes( )

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
        p, f = findNextPrime( p, f )

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
#//  getNthDoubleBalancedPrimes
#//
#//******************************************************************************

def getNthDoubleBalancedPrimes( arg ):
    global doubleBalancedPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 18713

    if doubleBalancedPrimes == { }:
        doubleBalancedPrimes = loadDoubleBalancedPrimes( )

    maxIndex = max( key for key in doubleBalancedPrimes )

    if n > maxIndex and not updateDicts:
        sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                format( n, maxIndex ) )

    currentIndex = max( key for key in doubleBalancedPrimes if key <= n )
    primes = [ ]

    for p in doubleBalancedPrimes[ currentIndex ]:
        primes.append( p )

    p = primes[ -1 ]
    f = p % 10

    while n > currentIndex:
        p, f = findNextPrime( p, f )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 3 ] - primes[ 2 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 4 ] - primes[ 3 ] ) ):
            currentIndex += 1

    if updateDicts:
        doubleBalancedPrimes[ n ] = [ ]

        for p in primes:
            doubleBalancedPrimes[ n ].append( p )

    return primes


#//******************************************************************************
#//
#//  getNthTripleBalancedPrimes
#//
#//******************************************************************************

def getNthTripleBalancedPrimes( arg ):
    global tripleBalancedPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 683747

    if tripleBalancedPrimes == { }:
        tripleBalancedPrimes = loadTripleBalancedPrimes( )

    maxIndex = max( key for key in tripleBalancedPrimes )

    if n > maxIndex and not updateDicts:
        sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                format( n, maxIndex ) )

    currentIndex = max( key for key in tripleBalancedPrimes if key <= n )

    p = tripleBalancedPrimes[ currentIndex ]
    f = p % 10

    primes = [ p ]

    for i in range( 0, 6 ):
        p, f = findNextPrime( p, f )
        primes.append( p )

    while n > currentIndex:
        p, f = findNextPrime( p, f )

        primes.append( p )
        del primes[ 0 ]

        if ( ( primes[ 3 ] - primes[ 2 ] ) == ( primes[ 4 ] - primes[ 3 ] ) and
             ( primes[ 2 ] - primes[ 1 ] ) == ( primes[ 5 ] - primes[ 4 ] ) and
             ( primes[ 1 ] - primes[ 0 ] ) == ( primes[ 6 ] - primes[ 5 ] ) ):
            currentIndex += 1

    if updateDicts:
        tripleBalancedPrimes[ n ] = p

    return primes


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

        maxIndex = max( key for key in sophiePrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

        startingPlace = max( key for key in sophiePrimes if key <= n )
        p = sophiePrimes[ startingPlace ]
    else:
        startingPlace = 4
        p = 11

    f = p % 10

    while n > startingPlace:
        p, f = getNextPrimeCandidate( p, f )

        if isPrime( p ) and isPrime( 2 * p + 1 ):
            n -= 1

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

    if n == 1:
        return 3

    if n >= 100:
        if cousinPrimes == { }:
            cousinPrimes = loadCousinPrimes( )

        maxIndex = max( key for key in cousinPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

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
#//  getNthSexyPrime
#//
#//******************************************************************************

def getNthSexyPrime( arg ):
    global sexyPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return 5

    if n >= 100:
        if sexyPrimes == { }:
            sexyPrimes = loadSexyPrimes( )

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
#//  getNthSexyTriplet
#//
#//******************************************************************************

def getNthSexyTriplet( arg ):
    global sexyTriplets
    global updateDicts

    n = int( arg )

    if n == 1:
        return 5
    elif n == 2:
        return 7

    if n >= 100:
        if sexyTriplets == { }:
            sexyTriplets = loadSexyTripletPrimes( )

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
#//  getNthSexyQuadruplet
#//
#//******************************************************************************

def getNthSexyQuadruplet( arg ):
    global sexyQuadruplets
    global updateDicts

    n = int( arg )

    if n == 1:
        return 5

    if sexyQuadruplets == { }:
        sexyQuadruplets = loadSexyQuadrupletPrimes( )

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

        maxIndex = max( key for key in tripletPrimes )

        if n > maxIndex and not updateDicts:
            sys.stderr.write( '{:,} is above the max cached index of {:,}.  This could take some time...\n'.
                                    format( n, maxIndex ) )

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
#//  getNthQuadrupletPrime
#//
#//******************************************************************************

def getNthQuadrupletPrime( arg ):
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


def getNextQuintupletPrimeCandidate( p, f ):
    if f == 1:
        p += 6
        f = 7
    else:
        p += 4
        f = 1


#//******************************************************************************
#//
#//  getNthQuintupletPrimes
#//
#//******************************************************************************

def getNthQuintupletPrimes( arg ):
    global quintPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return [ 5, 7, 11, 13, 17 ]
    elif n == 2:
        return [ 7, 11, 13, 17, 19 ]

    if n >= 10:
        if quintPrimes == { }:
            quintPrimes = loadQuintupletPrimes( )

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
        p, f = findNextPrime( p, f, getNextQuintupletPrimeCandidate )

        if ( ( f == 1 ) and isPrime( p + 2 ) and isPrime( p + 6 ) and isPrime( p + 8 ) and isPrime( p + 12 ) ) or \
           ( ( f == 7 ) and isPrime( p + 4 ) and isPrime( p + 6 ) and isPrime( p + 10 ) and isPrime( p + 12 ) ):
            currentIndex += 1

    if updateDicts:
        quintPrimes[ int( arg ) ] = p

    f = p % 10

    if f == 1:
        return [ p, p + 2, p + 6, p + 8, p + 12 ]
    elif f == 7:
        return [ p, p + 4, p + 6, p + 10, p + 12 ]
    else:
        # not the right exception type
        raise ValueError( 'internal error:  getNthQuintupletPrimes is broken' )


#//******************************************************************************
#//
#//  getNthSextupletPrimes
#//
#//******************************************************************************

def getNthSextupletPrimes( arg ):
    global sextPrimes
    global updateDicts

    n = int( arg )

    if n == 1:
        return [ 7, 11, 13, 17, 19, 23 ]

    if n >= 10:
        if sextPrimes == { }:
            sextPrimes = loadSextupletPrimes( )

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

    return [ p, p + 4, p + 6, p + 10, p + 12, p + 16 ]


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
#//  printStats
#//
#//******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:13,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


#//******************************************************************************
#//
#//  dumpStats
#//
#//******************************************************************************

def dumpStats( ):
    print( '{:10,} operators\n'.format( len( modifiers ) + len( list_operators ) +
                                        len( list_operators_2 ) + len( operators ) ) )

    printStats( loadSmallPrimes( ), 'small primes' )
    printStats( loadLargePrimes( ), 'large primes' )
    printStats( loadIsolatedPrimes( ), 'isolated primes' )
    printStats( loadTwinPrimes( ), 'twin primes' )
    printStats( loadBalancedPrimes( ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( ), 'triple balanced primes' )
    printStats( loadSophiePrimes( ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( ), 'cousin primes' )
    printStats( loadSexyPrimes( ), 'sexy primes' )
    printStats( loadTripletPrimes( ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in RPN_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  twoArgCaller
#//
#//******************************************************************************

def twoArgCaller( func, args ):
    arg1 = args[ 0 ]
    arg2 = args[ 1 ]

    #print( 'arg1: ' + str( arg1 ) )
    #print( 'arg2: ' + str( arg2 ) )

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

callers = [
    lambda func, args: [ func( ) ],
    lambda func, args: [ func( i ) for i in args[ 0 ] ],
    twoArgCaller,
    lambda func, args: [ func( k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] ],
    lambda func, args: [ func( l, k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] for l in args[ 3 ] ],
    lambda func, args: [ func( m, l, k, j, i ) for i in args[ 0 ] for j in args[ 1 ] for k in args[ 2 ] for l in args[ 3 ] for m in args[ 4 ] ],
]


operatorAliases = {
    '!!'        : 'doublefac',
    '!'         : 'factorial',
    '%'         : 'modulo',
    '*'         : 'multiply',
    '**'        : 'power',
    '***'       : 'tetrate',
    '+'         : 'add',
    '-'         : 'subtract',
    '/'         : 'divide',
    '//'        : 'root',
    '1/x'       : 'reciprocal',
    'average'   : 'mean',
    'avg'       : 'mean',
    'bal'       : 'balanced',
    'cbrt'      : 'root3',
    'ceil'      : 'ceiling',
    'cousin'    : 'cousinprime',
    'cuberoot'  : 'root3',
    'deg'       : 'degrees',
    'fac'       : 'factorial',
    'fac2'      : 'doublefac',
    'fib'       : 'fibonacci',
    'harm'      : 'harmonic',
    'hyper4'    : 'tetrate',
    'inv'       : 'reciprocal',
    'isdiv'     : 'isdivisible',
    'issqr'     : 'issquare',
    'log'       : 'ln',
    'mod'       : 'modulo',
    'mult'      : 'multiply',
    'neg'       : 'negative',
    'nonzeroes' : 'nonzero',
    'prod'      : 'product',
    'pyr'       : 'pyramid',
    'quad'      : 'quadprime',
    'quad?'     : 'quadprime?',
    'quint'     : 'quintprime',
    'quint'     : 'quintprime',
    'quint?'    : 'quintprime?',
    'rad'       : 'radians',
    'rand'      : 'random',
    'safe'      : 'safeprime',
    'sext'      : 'sextprime',
    'sext?'     : 'sextprime?',
    'sexy'      : 'sexyprime',
    'sexy3'     : 'sexytriplet',
    'sexy4'     : 'sexyquad',
    'sophie'    : 'sophieprime',
    'sqr'       : 'square',
    'sqrt'      : 'root2',
    'triplet'   : 'tripletprime',
    'twin'      : 'twinprime',
    'zeroes'    : 'zero',
    '^'         : 'power',
}


modifiers = {
    'dup'       : [ duplicateTerm, 2,
'modifiers', 'duplicates a argument n k times',
'''
''',
'''
''' ],
    'element': [ getListElement, 2,
'modifiers', 'return a single element from a list',
'''
''',
'''
''' ],
    'georange'  : [ expandGeometricRange, 3,
'modifiers', 'generates a list of geometric progression of numbers',
'''
''',
'''
''' ],
    'interleave': [ interleave, 2,
'modifiers', 'interleaves lists n and k into a single list',
'''
''',
'''
''' ],
    'intersection': [ makeIntersection, 2,
'modifiers', 'returns the intersection of two lists',
'''
''',
'''
''' ],
    'primes'     : [ getPrimes, 2,
'modifiers', 'generates a range of primes from index n to index k',
'''
''',
'''
''' ],
    'range'     : [ expandRange, 2,
'modifiers', 'generates a list of successive integers from n to k',
'''
''',
'''
''' ],
    'range2'    : [ expandSteppedRange, 3,
'modifiers', 'generates a list of arithmetic progression of numbers',
'''
''',
'''
''' ],
    'union': [ makeUnion, 2,
'modifiers', 'returns the union of two lists',
'''
''',
'''
''' ],
    'unlist'    : [ unlist, 1,
'modifiers', 'expands list n to individual arguments',
'''
''',
'''
''' ],
    '['         : [ incrementNestedListLevel, 0,
'modifiers', 'begins a list',
'''
''',
'''
''' ],
    ']'         : [ decrementNestedListLevel, 0,
'modifiers', 'ends a list',
'''
''',
'''
''' ],
}


list_operators = {
    'altsum'    : [ getAlternatingSum, 1,
'arithmetic', 'calculates the alternating sum of list n (addition first)',
'''
''',
'''
''' ],
    'altsum2'   : [ getAlternatingSum2, 1,
'arithmetic', 'calaculates the alternating sum of list n (subtraction first)',
'''
''',
'''
''' ],
    'cf2'       : [ convertFromContinuedFraction, 1,
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''' ],
    'count'     : [ countElements, 1,
'special', 'counts the elements of list n',
'''
''',
'''
''' ],
    'flatten'   : [ flatten, 1,
'special', 'flattens a nested lists in list n to a single level',
'''
''',
'''
''' ],
    'gcd'       : [ getGCD, 1,
'arithmetic', 'calculates the greatest common denominator of elements in list n',
'''
''',
'''
''' ],
    'mean'      : [ lambda i: fdiv( fsum( i ), len( i ) ), 1,
'arithmetic', 'calculates the mean of values in list n',
'''
''',
'''
''' ],
    'nonzero'   : [ lambda i: [ index for index, e in enumerate( i ) if e != 0 ], 1,
'special', 'returns the indices of elements of list n that are not zero',
'''
''',
'''
''' ],
    'polyprod'  : [ multiplyListOfPolynomials, 1,
'algebra', 'interprets elements of list n as polynomials and calculates their product',
'''
''',
'''
''' ],
    'polysum'   : [ addListOfPolynomials, 1,
'algebra', 'interprets elements of list n as polynomials and calculates their sum',
'''
''',
'''
''' ],
    'product'   : [ fprod, 1,
'arithmetic', 'calculates the product of values in list n',
'''
''',
'''
''' ],
    'solve'     : [ solvePolynomial, 1,
'algebra', 'interprets list n as a polynomial and solves for its roots',
'''
''',
'''
''' ],
    'sort'      : [ sort, 1,
'special', 'sort the elements of list n numerically in ascending order',
'''
''',
'''
''' ],
    'sortdesc'      : [ sortDescending, 1,
'special', 'sorts the elements of list n numerically in descending order',
'''
''',
'''
''' ],
    'sum'       : [ fsum, 1,
'arithmetic', 'calculates the sum of values in list n',
'''
''',
'''
''' ],
    'tower'     : [ calculatePowerTower, 1,
'powers_and_roots', 'calculates list n as a power tower',
'''
''',
'''
''' ],
    'tower2'    : [ calculatePowerTower2, 1,
'powers_and_roots', 'calculates list n as a right-associative power tower',
'''
''',
'''
''' ],
    'unique'    : [ getUniqueElements, 1,
'special', 'replaces list n with a list of its unique elements',
'''
''',
'''
''' ],
    'zero'    : [ lambda i: [ index for index, e in enumerate( i ) if e == 0 ], 1,
'special', 'returns a list of the indices of elements in list n that are zero',
'''
''',
'''
''' ],
}

list_operators_2 = {
    'base'      : [ interpretAsBase, 2,
'number_theory', 'interpret list elements as base k digits',
'''
''',
'''
''' ],
    'polyadd'   : [ addPolynomials, 2,
'algebra', 'interpret two lists as polynomials and add them',
'''
''',
'''
''' ],
    'polymul'   : [ multiplyPolynomials, 2,
'algebra', 'interpret two lists as polynomials and multiply them',
'''
''',
'''
''' ],
    'polyval'   : [ polyval, 2,
'algebra', 'interpret the list as a polynomial and evaluate it for value k',
'''
''',
'''
''' ],
}

operators = {
    'abs'           : [ fabs, 1,
'arithmetic', 'calculates the absolute value of n',
'''
''',
'''
''' ],
    'acos'          : [ acos, 1,
'trigonometry', 'calculates the arccosine of n',
'''
''',
'''
''' ],
    'acosh'         : [ acosh, 1,
'trigonometry', 'calculates the hyperbolic arccosine of n',
'''
''',
'''
''' ],
    'acot'          : [ acot, 1,
'trigonometry', 'calcuates the arccotangent of n',
'''
''',
'''
''' ],
    'acoth'         : [ acoth, 1,
'trigonometry', 'calculates the hyperbolic arccotangent of n',
'''
''',
'''
''' ],
    'acsc'          : [ acsc, 1,
'trigonometry', 'calculates the arccosecant of n',
'''
''',
'''
''' ],
    'acsch'         : [ acsch, 1,
'trigonometry', 'calculates the hyperbolic arccosecant of n',
'''
''',
'''
''' ],
    'add'           : [ fadd, 2,
'arithmetic', 'adds n to k',
'''
This operator adds two terms together.
''',
'''
c:\>rpn 2 2 add
4

c:\>rpn [ 1 2 3 4 5 6 ] 5 add
[ 6, 7, 8, 9, 10, 11 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 10 10 10 ] add
[ 11, 12, 13, 14, 15, 16 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 ] add
[ 11, 12, 13 ]''' ],
    'altfac'        : [ getNthAlternatingFactorial, 1,
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''' ],
    'and'           : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x & y ), 2,
'logical', 'calculates the bitwise \'and\' of n and k',
'''
''',
'''
''' ],
    'apery'         : [ apery, 0,
'constants', 'returns Apery\'s constant',
'''
''',
'''
''' ],
    'asec'          : [ asec, 1,
'trigonometry', 'calculates the arcsecant of n',
'''
''',
'''
''' ],
    'asech'         : [ asech, 1,
'trigonometry', 'calculates the hyperbolic arcsecant of n',
'''
''',
'''
''' ],
    'asin'          : [ asin, 1,
'trigonometry', 'calculates the arcsine of n',
'''
''',
'''
''' ],
    'asinh'         : [ asinh, 1,
'trigonometry', 'calculates the hyperbolic arcsine of n',
'''
''',
'''
''' ],
    'atan'          : [ atan, 1,
'trigonometry', 'calculates the arctangent of n',
'''
''',
'''
''' ],
    'atanh'         : [ atanh, 1,
'trigonometry', 'calculates the hyperbolic arctangent of n',
'''
''',
'''
''' ],
    'balanced'      : [ getNthBalancedPrimes, 1,
'prime_numbers', 'calculate the nth set of balanced primes',
'''
''',
'''
''' ],
    'bell'          : [ bell, 1,
'combinatorics', 'calculate the nth Bell number',
'''
''',
'''
''' ],
    'bellpoly'      : [ bell, 2,
'algebra', 'evaluates the nth Bell polynomial with k',
'''
''',
'''
''' ],
    'bernoulli'     : [ bernoulli, 1,
'combinatorics', 'calculate the nth Bernoulli number',
'''
''',
'''
''' ],
    'binomial'      : [ binomial, 2,
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
''',
'''
''' ],
    'catalan'       : [ lambda i: fdiv( binomial( fmul( 2, i ), i ), fadd( i, 1 ) ), 1,
'combinatorics', 'calculates nth Catalan number',
'''
''',
'''
''' ],
    'carol'      : [ lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1,
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''' ],
    'catalans'      : [ catalan, 0,
'constants', 'returns Catalan\'s constant',
'''
''',
'''
''' ],
    'ccube'         : [ getNthCenteredCubeNumber, 1,
'polyhedral_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' ],
    'ceiling'       : [ ceil, 1,
'arithmetic', 'returns the next highest integer for n',
'''
''',
'''
''' ],
    'cf'            : [ lambda i, j: ContinuedFraction( i, maxterms=j, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2,
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''' ],
    'champ'         : [ getChampernowne, 0,
'constants', 'returns the Champernowne constant',
'''
''',
'''
''' ],
    'champernowne'  : [ getChampernowne, 0,
'constants', 'returns the Champernowne constant',
'''
''',
'''
''' ],
    'copeland'      : [ getCopelandErdos, 0,
'constants', 'returns the Copeland Erdos constant',
'''
''',
'''
''' ],
    'cos'           : [ cos, 1,
'trigonometry', 'calculates the cosine of n',
'''
''',
'''
''' ],
    'cosh'          : [ cosh, 1,
'trigonometry', 'calculates the hyperbolic cosine of n',
'''
''',
'''
''' ],
    'cot'           : [ cot, 1,
'trigonometry', 'calculates the cotangent of n',
'''
''',
'''
''' ],
    'coth'          : [ coth, 1,
'trigonometry', 'calculates the hyperbolic cotangent of n',
'''
''',
'''
''' ],
    'cousinprime'   : [ getNthCousinPrime, 1,
'prime_numbers', 'returns the nth cousin prime',
'''
''',
'''
''' ],
    'csc'           : [ csc, 1,
'trigonometry', 'calculates the cosecant of n',
'''
''',
'''
''' ],
    'csch'          : [ csch, 1,
'trigonometry', 'calculates hyperbolic cosecant of n',
'''
''',
'''
''' ],
    'cube'          : [ lambda i: power( i, 3 ), 1,
'powers_and_roots', 'calculates the cube of n',
'''
''',
'''
''' ],
    'dec'           : [ lambda i: polyval( [ 4, -3, 0 ],  i ), 1,
'polygonal_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''' ],
    'degrees'       : [ radians, 1,
'trigonometry', 'interprets n as degrees and converts to radians',
'''
''',
'''
''' ],
    'delannoy'      : [ getNthDelannoyNumber, 1,
'[TBD]', 'calculates the nth Delannoy number',
'''
''',
'''
''' ],
    'divide'        : [ fdiv, 2,
'arithmetic', 'divides n by k',
'''
''',
'''
''' ],
    'doublebal'     : [ getNthDoubleBalancedPrimes, 1,
'prime_numbers', 'returns the nth set of double balanced primes',
'''
''',
'''
''' ],
    'doublefac'     : [ fac2, 1,
'number_theory', 'calculates the double factorial of n',
'''
''',
'''
''' ],
    'e'             : [ e, 0,
'constants', 'returns e (Euler\'s number)',
'''
''',
'''
''' ],
    'egypt'         : [ getGreedyEgyptianFraction, 2,
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' ],
    'euler'         : [ euler, 0,
'constants', 'returns the Euler-Mascheroni constant',
'''
''',
'''
''' ],
    'exp'           : [ exp, 1,
'powers_and_roots', 'calculates the nth power of e',
'''
''',
'''
''' ],
    'exp10'         : [ lambda i: power( 10, i ), 1,
'powers_and_roots', 'calculates nth power of 10',
'''
''',
'''
''' ],
    'expphi'        : [ phi, 1,
'powers_and_roots', 'calculates the nth power of phi',
'''
''',
'''
''' ],
    'factor'        : [ lambda i: getExpandedFactorList( factorize( i ) ), 1,
'number_theory', 'calculates the prime factorization of n',
'''
''',
'''
''' ],
    'fibonacci'     : [ fib, 1,
'number_theory', 'calculates the nth Fibonacci number',
'''
''',
'''
''' ],
    'floor'         : [ floor, 1,
'arithmetic', 'calculates the next lowest integer for n',
'''
''',
'''
''' ],
    'frac'          : [ interpretAsFraction, 2,
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''' ],
    'fraction'      : [ interpretAsFraction, 2,
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''' ],
    'gamma'         : [ gamma, 1,
'number_theory', 'calculates the gamma function for n',
'''
''',
'''
''' ],
    'glaisher'      : [ glaisher, 0,
'constants', 'returns Glaisher\'s constant',
'''
''',
'''
''' ],
    'harmonic'      : [ harmonic, 1,
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
''',
'''
''' ],
    'hept'          : [ getNthHeptagonalNumber, 1,
'polygonal_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''' ],
    'heptanacci'    : [ getNthHeptanacci, 1,
'polygonal_numbers', 'calculates the nth Heptanacci number',
'''
''',
'''
''' ],
    'hepthex'       : [ getNthHeptagonalHexagonalNumber, 1,
'polygonal_numbers', 'calculates the nth heptagonal hexagonal number',
'''
''',
'''
''' ],
    'heptpent'      : [ getNthHeptagonalPentagonalNumber, 1,
'polygonal_numbers', 'calculates the nth heptagonal pentagonal number',
'''
''',
'''
''' ],
    'hex'           : [ lambda i: fsub( fprod( 2, i, i ), i ), 1,
'polygonal_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''' ],
    'hex?'          : [ findHexagonalNumber, 1,
'number_theory', 'finds index of the closest hexagonal number over n',
'''
''',
'''
''' ],
    'hexanacci'     : [ getNthHexanacci, 1,
'number_theory', 'calculates the nth Hexanacci number',
'''
''',
'''
''' ],
    'hyper4_2'      : [ tetrateLarge, 2,
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''' ],
    'hyperfac'      : [ hyperfac, 1,
'number_theory', 'calculates the hyperfactorial of n',
'''
''',
'''
''' ],
    'hypot'         : [ hypot, 2,
'trigonometry', 'calculates the hypotenuse of n and k',
'''
''',
'''
''' ],
    'i'             : [ makeImaginary, 1,
'complex_math', 'multiplies n by i',
'''
''',
'''
''' ],
    'isdivisible'   : [ lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2,
'arithmetic', 'is divisible by n?',
'''
''',
'''
''' ],
    'isolated'      : [ getNthIsolatedPrime, 1,
'prime_numbers', 'returns the nth isolated prime',
'''
''',
'''
''' ],
    'isprime'       : [ lambda i: 1 if isPrime( i ) else 0, 1,
'number_theory', 'is prime?',
'''
''',
'''
''' ],
    'issquare'      : [ isSquare, 1,
'arithmetic', 'is perfect square?',
'''
''',
'''
''' ],
    'itoi'          : [ lambda: exp( fmul( -0.5, pi ) ), 0,
'constants', 'returns i to the i power',
'''
''',
'''
''' ],
    'khinchin'      : [ khinchin, 0,
'constants', 'returns Khinchin\'s constant',
'''
''',
'''
''' ],
    'lah'           : [ lambda n, k: fdiv( fmul( binomial( n, k ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2,
'combinatorics', '',
'''
''',
'''
''' ],
    'lambertw'      : [ lambertw, 1,
'[TBD]', '',
'''
''',
'''
''' ],
    'kynea'      : [ lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1,
'number_theory', 'gets the nth Kynea number',
'''
''',
'''
''' ],
    'leyland'      : [ lambda x, y : fadd( power( x, y ), power( y, x ) ), 2,
'number_theory', 'gets the Leyland number for n and k',
'''
''',
'''
''' ],
    'lgamma'        : [ loggamma, 1,
'number_theory', 'calculates the loggamma function for n',
'''
''',
'''
''' ],
    'li'            : [ li, 1,
'logarithms', 'calculates the logarithmic interval of n',
'''
''',
'''
''' ],
    'ln'            : [ ln, 1,
'logarithms', 'calculates the natural logarithm of n',
'''
''',
'''
''' ],
    'log10'         : [ log10, 1,
'logarithms', 'calculates the base-10 logarithm of n',
'''
''',
'''
''' ],
    'logxy'         : [ log, 2,
'logarithms', 'calculates the base-k logarithm of n',
'''
''',
'''
''' ],
    'lucas'         : [ getNthLucas, 1,
'number_theory', 'calculates the nth Lucas number',
'''
''',
'''
''' ],
    'mertens'       : [ mertens, 0,
'constants', 'returns Merten\'s constant',
'''
''',
'''
''' ],
    'modulo'        : [ fmod, 2,
'arithmetic', 'calculates n modulo k',
'''
''',
'''
''' ],
    'motzkin'       : [ getNthMotzkinNumber, 1,
'[TBD]', 'calculates the nth Motzkin number',
'''
''',
'''
''' ],
    'multiply'      : [ fmul, 2,
'arithmetic', 'multiplies n by k',
'''
''',
'''
''' ],
    'narayana'      : [ lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2,
'combinatorics', '',
'''
''',
'''
''' ],
    'negative'      : [ fneg, 1,
'arithmetic', 'calculates the negative of n',
'''
''',
'''
''' ],
    'non'           : [ lambda n: fdiv( polyval( [ 7, -5, 0 ], n ), 2 ), 1,
'polygonal_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''' ],
    'nthprime?'     : [ lambda i: findPrime( i )[ 0 ], 1,
'prime_numbers', 'finds the index of the closest prime over n',
'''
''',
'''
''' ],
    'nthquad?'      : [ lambda i: findQuadrupletPrimes( i )[ 0 ], 1,
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''
''',
'''
''' ],
    'oct'           : [ lambda n: polyval( [ 3, -2, 0 ], n ), 1,
'polygonal_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''' ],
    'octahedral'    : [ getNthOctahedralNumber, 1,
'polyhedral_numbers', 'calculates the nth octahedral number',
'''
''',
'''
''' ],
    'octhept'       : [ getNthOctagonalHeptagonalNumber, 1,
'polygonal_numbers', 'nth octagonal heptagonal number',
'''
''',
'''
''' ],
    'octhex'        : [ getNthOctagonalHexagonalNumber, 1,
'polygonal_numbers', 'calculates the nth octagonal hexagonal number',
'''
''',
'''
''' ],
    'octpent'       : [ getNthOctagonalPentagonalNumber, 1,
'polygonal_numbers', 'calculates the nth octagonal pentagonal number',
'''
''',
'''
''' ],
    'oeis'          : [ getOEISSequence, 1,
'special', 'downloads the OEIS integer series n',
'''
''',
'''
''' ],
    'omega'         : [ lambda: lambertw( 1 ), 0,
'constants', 'return the Omega constant (goobles)',
'''
''',
'''
''' ],
    'or'            : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2,
'logical', 'calculates the bitwise \'or\' of n and k',
'''
''',
'''
''' ],
    'padovan'  : [ getNthPadovanNumber, 1,
'number_theory', 'calculates their the nth Padovan number',
'''
''',
'''
''' ],
    'pascal'        : [ getNthPascalLine, 1,
'number_theory', 'calculates the nth line of Pascal\'s triangle',
'''
''',
'''
''' ],
    'pent'          : [ lambda i: fdiv( fsub( fprod( [ 3, i, i ] ), i ), 2 ), 1,
'polygonal_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''' ],
    'pent?'         : [ lambda i: fdiv( fadd( sqrt( fadd( fmul( 24 , i ), 1 ) ), 1 ), 6 ), 1,
'polygonal_numbers', 'finds the index of the closest pentagonal number over n',
'''
''',
'''
''' ],
    'pentanacci'    : [ getNthPentanacci, 1,
'number_theory', 'calculates the nth Pentanacci number',
'''
''',
'''
''' ],
    'pentatope'     : [ getNthPentatopeNumber, 1,
'polyhedral_numbers', 'calculates the nth pentatope number',
'''
''',
'''
''' ],
    'perm'          : [ getPermutations, 2,
'combinatorics', 'calculates the number of permutations of k out of n objects',
'''
''',
'''
''' ],
    'phi'           : [ phi, 0,
'constants', 'returns phi (the Golden Ratio)',
'''
''',
'''
''' ],
    'pi'            : [ pi, 0,
'constants', 'returns pi (Archimedes\' constant)',
'''
''',
'''
''' ],
    'plastic'       : [ getPlasticConstant, 0,
'constants', 'returns the Plastic constant',
'''
''',
'''
''' ],
    'polygamma'     : [ psi, 2,
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''' ],
    'polylog'            : [ polylog, 2,
'logarithms', 'calculates the polylogarithm of n, k',
'''
''',
'''
''' ],
    'polyprime'     : [ getNthPolyPrime, 2,
'prime_numbers', 'returns the nth prime, recursively k times',
'''
''',
'''
''' ],
    'polytope'      : [ getNthPolytopeNumber, 2,
'polyhedral_numbers', 'calculates nth polytope number of dimension k',
'''
''',
'''
''' ],
    'power'         : [ power, 2,
'powers_and_roots', 'calculates the kth power of n',
'''
''',
'''
''' ],
    'prime'         : [ getNthPrime, 1,
'prime_numbers', 'returns the nth prime',
'''
''',
'''
''' ],
    'primepi'       : [ primepi2, 1,
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''
''',
'''
''' ],
    'prime?'        : [ lambda i: findPrime( i )[ 1 ], 1,
'prime_numbers', 'find the index of the closest prime above n',
'''
''',
'''
''' ],
    'primorial'     : [ getPrimorial, 1,
'prime_numbers', 'calculates the nth primorial',
'''
''',
'''
''' ],
    'psi'           : [ psi, 2,
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''' ],
    'pyramid'       : [ getNthPyramidalNumber, 1,
'polyhedral_numbers', 'calculates the nth pyramidal number',
'''
''',
'''
''' ],
    'quadprime?'    : [ lambda i: findQuadrupletPrimes( i )[ 1 ], 1,
'prime_numbers', 'find the closest set of quadruplet primes above n',
'''
''',
'''
''' ],
    'quadprime'     : [ getNthQuadrupletPrime, 1,
'prime_numbers', 'returns the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quintprime'    : [ getNthQuintupletPrimes, 1,
'prime_numbers', 'returns the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'radians'       : [ degrees, 1,
'trigonometry', 'interprets n as radians and converts to degrees',
'''
''',
'''
''' ],
    'random'        : [ rand, 0,
'special', 'returns a random value from 0 to 1',
'''
''',
'''
''' ],
    'rhombdodec'    : [ getNthRhombicDodecahedralNumber, 1,
'polyhedral_numbers', 'calculates the nth rhombic dodecahedral number',
'''
''',
'''
''' ],
    'root'          : [ root, 2,
'powers_and_roots', 'calculates the kth root of n',
'''
''',
'''
''' ],
    'root2'         : [ sqrt, 1,
'powers_and_roots', 'calculates the square root of n',
'''
''',
'''
''' ],
    'root3'         : [ cbrt, 1,
'powers_and_roots', 'calculates the cube root of n',
'''
''',
'''
''' ],
    'round'         : [ lambda i: floor( fadd( i, 0.5 ) ), 1,
'arithmetic', 'rounds n to the nearest integer',
'''
''',
'''
''' ],
    'safeprime'   : [ lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1,
'prime_numbers', 'returns the nth safe prime',
'''
''',
'''
''' ],
    'schroeder'     : [ getNthSchroederNumber, 1,
'[TBD]', 'calculates the nth Schroeder number',
'''
''',
'''
''' ],
    'sec'           : [ sec, 1,
'trigonometry', 'calculates the secant of n',
'''
''',
'''
''' ],
    'sech'          : [ sech, 1,
'trigonometry', 'calculates the hyperbolic secant of n',
'''
''',
'''
''' ],
    'sextprime'     : [ getNthSextupletPrimes, 1,
'prime_numbers', 'returns the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sexyprime'     : [ getNthSexyPrime, 1,
'prime_numbers', 'returns the nth sexy prime',
'''
''',
'''
''' ],
    'sexytriplet'     : [ getNthSexyTriplet, 1,
'prime_numbers', 'returns first of the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexyquad'     : [ getNthSexyQuadruplet, 1,
'prime_numbers', 'returns first of the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'sin'           : [ sin, 1,
'trigonometry', 'calculates the sine of n',
'''
''',
'''
''' ],
    'sinh'          : [ sinh, 1,
'trigonometry', 'calculates the hyperbolic sine of n',
'''
''',
'''
''' ],
    'solve2'        : [ solveQuadraticPolynomial, 3,
'algebra', 'solves a quadratic equation',
'''
''',
'''
''' ],
    'solve3'        : [ solveCubicPolynomial, 4,
'algebra', 'solves a cubic equation',
'''
''',
'''
''' ],
    'solve4'        : [ solveQuarticPolynomial, 5,
'algebra', 'solves a quartic equation',
'''
''',
'''
''' ],
    'sophieprime'   : [ getNthSophiePrime, 1,
'prime_numbers', 'returns the nth Sophie Germain prime',
'''
''',
'''
''' ],
    'square'        : [ lambda i: power( i, 2 ), 1,
'powers_and_roots', 'calculates the square of n',
'''
''',
'''
''' ],
    'sqtri'         : [ getNthSquareTriangularNumber, 1,
'polygonal_numbers', 'calculates the nth square triangular number',
'''
''',
'''
''' ],
    'steloct'       : [ getNthStellaOctangulaNumber, 1,
'polyhedral_numbers', 'calculates the nth stella octangula number',
'''
''',
'''
''' ],
    'subfac'        : [ lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1,
'number_theory', 'calculates the subfactorial of n',
'''
''',
'''
''' ],
    'subtract'      : [ fsub, 2,
'arithmetic', 'subtracts k from n',
'''
''',
'''
''' ],
    'superfac'      : [ superfac, 1,
'number_theory', 'calculates the superfactorial of n',
'''
''',
'''
''' ],
    'superprime'    : [ getNthSuperPrime, 1,
'prime_numbers', 'returns the nth superprime (the nth primeth prime)',
'''
''',
'''
''' ],
    'syl'           : [ getNthSylvester, 1,
'[TBD]', 'calculates the nth Sylvester number',
'''
''',
'''
''' ],
    'sylvester'     : [ getNthSylvester, 1,
'[TBD]', 'calculates the nth Sylvester number',
'''
''',
'''
''' ],
    'tan'           : [ tan, 1,
'trigonometry', 'calculates the tangent of n',
'''
''',
'''
''' ],
    'tanh'          : [ tanh, 1,
'trigonometry', 'calculates the hyperbolic tangent of n',
'''
''',
'''
''' ],
    'tetrate'       : [ lambda i: fdiv( fsum( [ power( i, 3 ), fmul( 3, power( i, 2 ) ), fmul( 2, i ) ] ), 6 ), 1,
'polyhedral_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' ],
    'tetra'         : [ lambda i: fdiv( fsum( [ power( i, 3 ), fmul( 3, power( i, 2 ) ), fmul( 2, i ) ] ), 6 ), 1,
'polyhedral_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' ],
    'tetranacci'    : [ getNthTetranacci, 1,
'number_theory', 'calculates the nth Tetranacci number',
'''
''',
'''
''' ],
    'thabit'        : [ lambda n : fsub( fmul( 3, power( 2, n ) ), 1 ), 1,
'number_theory', 'gets the nth Thabit number',
'''
''',
'''
''' ],
    'tri'           : [ getNthTriangularNumber, 1,
'polygonal_numbers', 'calcuates the nth triangular number',
'''
''',
'''
''' ],
    'tri?'          : [ findTriangularNumber, 1,
'polygonal_numbers', 'finds nearest triangular number index for n',
'''
''',
'''
''' ],
    'tribonacci'    : [ getNthTribonacci, 1,
'number_theory', 'calculates the nth Tribonacci number',
'''
''',
'''
''' ],
    'triplebal'     : [ getNthTripleBalancedPrimes, 1,
'prime_numbers', 'returns the nth set of triple balanced primes',
'''
''',
'''
''' ],
    'tripletprime'  : [ getNthTripletPrimes, 1,
'prime_numbers', 'returns the nth set of triplet primes',
'''
''',
'''
''' ],
    'truncoct'      : [ getNthTruncatedOctahedralNumber, 1,
'polyhedral_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' ],
    'trunctet'      : [ getNthTruncatedTetrahedralNumber, 1,
'polyhedral_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' ],
    'twinprime'     : [ getNthTwinPrime, 1,
'prime_numbers', 'returns the nth twin prime',
'''
''',
'''
''' ],
    'unitroots'     : [ lambda i: unitroots( int( i ) ), 1,
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
''' ],
    'xor'           : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2,
'logical', 'calculates the bitwise \'xor\' of n and k',
'''
''',
'''
''' ],
    'zeta'          : [ zeta, 1,
'number_theory', 'calculates the zeta function for n',
'''
''',
'''
''' ],
    '_dumpbal'      : [ dumpBalancedPrimes, 0,
'internal', 'dumps the cached list of balanced primes',
'''
''',
'''
''' ],
    '_dumpcousin'   : [ dumpCousinPrimes, 0,
'internal', 'dumps the cached list of cousin primes',
'''
''',
'''
''' ],
    '_dumpdouble'   : [ dumpDoubleBalancedPrimes, 0,
'internal', 'dumps the cached list of double balanced primes',
'''
''',
'''
''' ],
    '_dumpiso'      : [ dumpIsolatedPrimes, 0,
'internal', 'dumps the cached list of isolated primes',
'''
''',
'''
''' ],
    '_dumpprimes'   : [ dumpLargePrimes, 0,
'internal', 'dumps the cached list of large primes',
'''
''',
'''
''' ],
    '_dumpquad'     : [ dumpQuadrupletPrimes, 0,
'internal', 'dumps the cached list of quadruplet primes',
'''
''',
'''
''' ],
    '_dumpquint'    : [ dumpQuintupletPrimes, 0,
'internal', 'dumps the cached list of quintuplet primes',
'''
''',
'''
''' ],
    '_dumpsext'     : [ dumpSextupletPrimes, 0,
'internal', 'dumps the cached list of sextuplet primes',
'''
''',
'''
''' ],
    '_dumpsexy'     : [ dumpSexyPrimes, 0,
'internal', 'dumps the cached list of sexy primes',
'''
''',
'''
''' ],
    '_dumpsmall'    : [ dumpSmallPrimes, 0,
'internal', 'dumps the cached list of small primes',
'''
''',
'''
''' ],
    '_dumpsophie'   : [ dumpSophiePrimes, 0,
'internal', 'dumps the cached list of Sophie Germain primes',
'''
''',
'''
''' ],
    '_dumptriple'   : [ dumpTripleBalancedPrimes, 0,
'internal', 'dumps the cached list of triple balanced primes',
'''
''',
'''
''' ],
    '_dumptriplet'  : [ dumpTripletPrimes, 0,
'internal', 'dumps the cached list of triplet primes',
'''
''',
'''
''' ],
    '_dumptwin'     : [ dumpTwinPrimes, 0,
'internal', 'dumps the cached list of twin primes',
'''
''',
'''
''' ],
    '_importbal'    : [ importBalancedPrimes, 1,
'internal', 'imports balanced primes from file n',
'''
''',
'''
''' ],
    '_importcousin' : [ importCousinPrimes, 1,
'internal', 'imports cousin primes from file n',
'''
''',
'''
''' ],
    '_importdouble' : [ importDoubleBalancedPrimes, 1,
'internal', 'imports double balanced primes from file n',
'''
''',
'''
''' ],
    '_importiso'    : [ importIsolatedPrimes, 1,
'internal', 'imports isolated primes from file n',
'''
''',
'''
''' ],
    '_importprimes' : [ importLargePrimes, 1,
'internal', 'imports large primes from file n',
'''
''',
'''
''' ],
    '_importquad'   : [ importQuadrupletPrimes, 1,
'internal', 'imports quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importquint'  : [ importQuintupletPrimes, 1,
'internal', 'imports quintuplet primes from file n',
'''
''',
'''
''' ],
    '_importsext'   : [ importSextupletPrimes, 1,
'internal', 'imports sextuplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy'   : [ importSexyPrimes, 1,
'internal', 'imports sexy primes from file n',
'''
''',
'''
''' ],
    '_importsexy3'  : [ importSexyTriplets, 1,
'internal', 'imports sexy triplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy4'  : [ importSexyQuadruplets, 1,
'internal', 'imports sexy quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importsmall'  : [ importSmallPrimes, 1,
'internal', 'imports small primes from file n',
'''
''',
'''
''' ],
    '_importsophie' : [ importSophiePrimes, 1,
'internal', 'imports Sophie Germain primes from file n',
'''
''',
'''
''' ],
    '_importtriple' : [ importTripleBalancedPrimes, 1,
'internal', 'imports triple balanced primes from file n',
'''
''',
'''
''' ],
    '_importtriplet': [ importTripletPrimes, 1,
'internal', 'imports triplet primes from file n',
'''
''',
'''
''' ],
    '_importtwin'   : [ importTwinPrimes, 1,
'internal', 'imports twin primes from file n',
'''
''',
'''
''' ],
    '_listops'      : [ listOperators, 0,
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_makebal'      : [ makeBalancedPrimes, 3,
'internal', 'calculates and caches balanced primes',
'''
''',
'''
''' ],
    '_makecousin'   : [ makeCousinPrimes, 3,
'internal', 'calculates and caches cousin primes',
'''
''',
'''
''' ],
    '_makedouble'   : [ makeDoubleBalancedPrimes, 3,
'internal', 'calculates and caches double balanced primes',
'''
''',
'''
''' ],
    '_makeiso'      : [ makeIsolatedPrimes, 3,
'internal', 'calculates and caches isolated primes',
'''
''',
'''
''' ],
    '_makeprimes'   : [ makeLargePrimes, 3,
'internal', 'calculates and caches large primes',
'''
''',
'''
''' ],
    '_makequad'     : [ makeQuadrupletPrimes, 3,
'internal', 'calculates and caches quaduplet primes',
'''
''',
'''
''' ],
    '_makequint'    : [ makeQuintupletPrimes, 3,
'internal', 'calculates and caches quintuplet primes',
'''
''',
'''
''' ],
    '_makesext'     : [ makeSextupletPrimes, 3,
'internal', 'calculates and caches sextuplet primes',
'''
''',
'''
''' ],
    '_makesexy'     : [ makeSexyPrimes, 3,
'internal', 'calculates and caches sexy primes',
'''
''',
'''
''' ],
    '_makesexy3'    : [ makeSexyTriplets, 3,
'internal', 'calculates and caches sexy triplet primes',
'''
''',
'''
''' ],
    '_makesexy4'    : [ makeSexyQuadruplets, 3,
'internal', 'calculates and caches sexy quadruplet primes',
'''
''',
'''
''' ],
    '_makesmall'    : [ makeSmallPrimes, 3,
'internal', 'calculates and caches small primes',
'''
''',
'''
''' ],
    '_makesophie'   : [ makeSophiePrimes, 3,
'internal', 'calculates and caches Sophie Germain primes',
'''
''',
'''
''' ],
    '_makesuper'    : [ makeSuperPrimes, 2,
'internal', 'calculates and caches super primes',
'''
''',
'''
''' ],
    '_maketriple'   : [ makeTripleBalancedPrimes, 3,
'internal', 'calculates and caches triple balanced primes',
'''
''',
'''
''' ],
    '_maketriplet'  : [ makeTripletPrimes, 3,
'internal', 'calculates and caches triplet primes',
'''
''',
'''
''' ],
    '_maketwin'     : [ makeTwinPrimes, 3,
'internal', 'calculates and caches twin primes',
'''
''',
'''
''' ],
    '_stats'        : [ dumpStats, 0,
'internal', 'dumps rpn statistics',
'''
''',
'''
''' ],
    '~'             : [ getInvertedBits, 1,
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
#   'antitet'       : [ findTetrahedralNumber, 1 ],
#   'bernfrac'      : [ bernfrac, 1 ],
#   'powmod'        : [ getPowMod, 3 ],
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

    # ignore a trailing comma, since it's easy to want to use those in lists
    if term[ -1 ] == ',':
        term = term[ : -1 ]

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

    #print( 'mantissa: %s' % mantissa )
    #print( 'output: %s' % output )

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
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( basicCategories, operatorCategories ):
    print(
'\n' + PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE +
'''

For help on a specific topic, add a help topic, operator category or a
specific operator name.  Adding 'example', or 'ex' after an operator name will
result in examples of using being printed as well.

The following is a list of general topics:

    ''' + ',\n    '.join( sorted( basicCategories ) ) + '''

The following is a list of operator categories:

    ''' + ',\n    '.join( sorted( operatorCategories ) ) )


#//******************************************************************************
#//
#//  printTitleScreen
#//
#//******************************************************************************

def printTitleScreen( ):
    print(
'\n' + PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE +
'''

For more information use, 'rpn help'.''' )


#//******************************************************************************
#//
#//  printOperatorHelp
#//
#//******************************************************************************

def printOperatorHelp( helpArgs, term, operatorInfo ):
    if operatorInfo[ 1 ] == 1:
        print( 'n ', end='' )
    elif operatorInfo[ 1 ] == 2:
        print( 'n k ', end='' )
    elif operatorInfo[ 1 ] == 3:
        print( 'a b c ', end='' )
    elif operatorInfo[ 1 ] == 4:
        print( 'a b c d ', end='' )
    elif operatorInfo[ 1 ] == 5:
        print( 'a b c d e ', end='' )

    aliasList = [ key for key in operatorAliases if term == operatorAliases[ key ] ]

    print( term + ' - ' + operatorInfo[ 3 ] )

    print( )

    if len( aliasList ) > 1:
        print( 'aliases:  ' + ', '.join( aliasList ) )
    elif len( aliasList ) == 1:
        print( 'alias:  ' + ', '.join( aliasList ) )

    print( 'category: ' + operatorInfo[ 2 ] )

    if operatorInfo[ 4 ] == '\n':
        print( )
        print( 'No further help is available.' )
    else:
        print( operatorInfo[ 4 ] )

    if len( helpArgs ) > 1 and helpArgs[ 1 ] in ( 'ex', 'example' ):
        print( )

        if operatorInfo[ 5 ] == '\n':
            print( 'No examples are available.' )
        else:
            print( term + ' examples:' )
            print( operatorInfo[ 5 ] )


#//******************************************************************************
#//
#//  addAliases
#//
#//******************************************************************************

def addAliases( operatorList ):
    for index, operator in enumerate( operatorList ):
        aliasList = [ key for key in operatorAliases if operator == operatorAliases[ key ] ]

        if len( aliasList ) > 0:
            operatorList[ index ] += ' ( ' + ', '.join( aliasList ) + ' )'


#//******************************************************************************
#//
#//  printHelp
#//
#//******************************************************************************

def printHelp( helpArgs ):
    basicCategories = {
'options' :
PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE + '\n\n' +
'''
    -h, --help -
        displays basic help information
''',
'arguments' :
'''
''',
'input' :
'''
''',
'output' :
'''
''',
'about' :
PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE +
'''
''',
'bugs' :
'''
''',
'license' :
'''
rpndata is licensed under the GPL, version 3.0 and is ''' + '\n' + COPYRIGHT_MESSAGE + '''

    [ fill in extra boilerplate as needed ]
''',
'examples' :
'''
''',
'notes' :
'''
'''
}

    operatorCategories = set( operators[ key ][ 2 ] for key in operators )
    operatorCategories.update( set( modifiers[ key ][ 2 ] for key in modifiers ) )
    operatorCategories.update( set( list_operators[ key ][ 2 ] for key in list_operators ) )
    operatorCategories.update( set( list_operators_2[ key ][ 2 ] for key in list_operators_2 ) )

    if len( helpArgs ) == 0:
        printGeneralHelp( basicCategories, operatorCategories )
        return

    term = helpArgs[ 0 ]

    if term in operatorAliases:
        term = operatorAliases[ term ]

    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ] )

    if term in list_operators:
        printOperatorHelp( helpArgs, term, list_operators[ term ] )

    if term in list_operators_2:
        printOperatorHelp( helpArgs, term, list_operators_2[ term ] )

    if term in modifiers:
        printOperatorHelp( helpArgs, term, modifiers[ term ] )

    if term in basicCategories:
        print( basicCategories[ term ] )

    if term in operatorCategories:
        print( )
        print( 'The ' + term + ' category includes the following operators (with aliases in' )
        print( 'parentheses):' )
        print( )

        operatorList = [ key for key in operators if operators[ key ][ 2 ] == term ]
        operatorList.extend( [ key for key in list_operators if list_operators[ key ][ 2 ] == term ] )
        operatorList.extend( [ key for key in list_operators_2 if list_operators_2[ key ][ 2 ] == term ] )
        operatorList.extend( [ key for key in modifiers if modifiers[ key ][ 2 ] == term ] )

        addAliases( operatorList )

        print( '    ' + ',\n    '.join( sorted( operatorList ) ) )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global addToListArgument
    global bitwiseGroupSize
    global dataPath
    global inputRadix
    global nestedListLevel
    global numerals
    global updateDicts

    global balancedPrimes
    global cousinPrimes
    global doubleBalancedPrimes
    global isolatedPrimes
    global largePrimes
    global quadPrimes
    global quintPrimes
    global sextPrimes
    global sexyPrimes
    global sexyQuadruplets
    global sexyTriplets
    global smallPrimes
    global sophiePrimes
    global superPrimes
    global tripleBalancedPrimes
    global tripletPrimes
    global twinPrimes

    # initialize globals
    nestedListLevel = 0

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

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )

    help = False
    helpArgs = [ ]

    for i in range( 0, len( sys.argv ) ):
        if sys.argv[ i ] == 'help':
            help = True
        else:
            if help:
                helpArgs.append( sys.argv[ i ] )

    if help:
        printHelp( helpArgs )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + RPN_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=-1, const=defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0 )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-u', '--find_poly', nargs='?', type=int, action='store', default=0, const=1000 )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store', default=defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-y', '--identify', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    if len( sys.argv ) == 1:
        printTitleScreen( )
        return

    args = parser.parse_args( )

    if args.help or args.other_help:
        printHelp( [ ] )
        return

    mp.dps = args.precision

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
        print( 'rpn:  no terms found' )
        return

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        if term in operatorAliases:
            term = operatorAliases[ term ]

        currentValueList = getCurrentArgList( valueList )

        if term in modifiers:
            try:
                modifiers[ term ][ 0 ]( currentValueList )
            except IndexError as error:
                print( 'rpn:  index error for operator at arg ' + format( index ) +
                       '.  Are your arguments in the right order?' )
                break
        elif term in operators:
            argsNeeded = operators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term + ' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )

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
                print( 'rpn:  keyboard interrupt' )
                break
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            #except TypeError as error:
            #    print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
        elif term in list_operators:
            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < 1:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term +
                       ' requires a list argument' )
                break

            try:
                arg = currentValueList.pop( )
                currentValueList.append( list_operators[ term ][ 0 ]( arg ) )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except IndexError as error:
                print( 'rpn:  index error for operator at arg ' + format( index ) +
                       '.  Are your arguments in the right order?' )
                break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
        elif term in list_operators_2:
            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < 2:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term +
                       ' requires two arguments' )
                break

            try:
                secondArg = currentValueList.pop( )
                listArg = currentValueList.pop( )

                if not isinstance( secondArg, list ):
                    secondArg = [ secondArg ]

                result = [ list_operators_2[ term ][ 0 ]( listArg, i ) for i in secondArg ]

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            #except TypeError as error:
            #    print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
        else:
            try:
                currentValueList.append( parseInputValue( term, inputRadix ) )
            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                currentValueList.append( term )
                print( 'rpn:  error in arg ' + format( index ) +
                       ':  unrecognized argument: \'%s\'' % sys.argv[ index ] )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1:
            print( 'rpn:  unexpected end of input' )
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
                        base.extend( [ 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' ] )
                        formula = identify( result, base )

                    if formula is None:
                        base.extend( [ 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' ] )
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
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000, tol=1e-10 ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )

        if args.time:
            print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

