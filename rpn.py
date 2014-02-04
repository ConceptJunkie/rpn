#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator
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
import datetime
import itertools
import math
import os
import pickle
import pyprimes
import random
import string
import sys
import textwrap
import time

from fractions import Fraction
from functools import reduce
from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpn'
RPN_VERSION = '5.2.3'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'
COPYRIGHT_MESSAGE = 'copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)'

defaultPrecision = 20
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

unitStack = [ ]


#//******************************************************************************
#//
#//  UnitOfMeasurement
#//
#//******************************************************************************

class UnitOfMeasurement( dict ):
    def __init__( self, value={ } ):
        if isinstance( value, str ):
            self.increment( value )
        elif isinstance( value, ( list, tuple ) ):
            for unit in value:
                self.increment( unit )
        else:
            raise ValueError( 'UnitOfMeasurement requires a string or a list' )

    def increment( self, value, amount=1 ):
        if value not in self:
            self[ value ] = amount
        else:
            self[ value ] += amount

    def decrement( self, value, amount=1 ):
        if value not in self:
            self[ value ] = -amount
        else:
            self[ value ] -= amount

    def isCompatible( self, other ):
        if isinstance( other, ( str, list, tuple ) ):
            return isCompatible( self, UnitOfMeasurement( other ) )
        else:
            return self.getType( ) == other.getType( )

    def getType( self ):
        unitTypes = { }

        for unit in self:
            if unit not in unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = unitOperators[ unit ]

            if unitType not in unitTypes:
                unitTypes[ unitType ] = self[ unit ]
            else:
                unitTypes[ unitType ] += self[ unit ]

        return unitTypes

    def getConversion( self, other ):
        if self.isCompatible( other ):
            unit1 = [ k for k, v in self.items( ) ][ 0 ]
            unit2 = [ k for k, v in other.items( ) ][ 0 ]
            return mpmathify( unitConversionMatrix[ ( unit1, unit2 ) ] )
        else:
            raise ValueError( 'incompatible types cannot be converted' )
            return 0


#//******************************************************************************
#//
#//  class Polynomial
#//
#//  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
#//
#//******************************************************************************

class Polynomial( object ):
    def __init__( self, *args ):
        """
        Create a polynomial in one of three ways:

        p = Polynomial( poly )              # copy constructor
        p = Polynomial( [ 1, 2, 3 ... ] )   # from sequence
        p = Polynomial( 1, 2, 3 ... )       # from scalars
        """
        super( Polynomial, self ).__init__( )

        if len( args ) == 1:
            val = args[ 0 ]

            if isinstance( val, Polynomial ):                # copy constructor
                self.coeffs = val.coeffs[ : ]
            elif isinstance( val, collections.Iterable ):    # from sequence
                self.coeffs = list( val )
            else:                                            # from single scalar
                self.coeffs = [ val + 0 ]
        else:                                                # multiple scalars
            self.coeffs = [ i + 0 for i in args ]
        self.trim( )

    def __add__( self, val ):
        "Return self+val"
        if isinstance( val, Polynomial ):                    # add Polynomial
            res = [ a + b for a, b in itertools.zip_longest( self.coeffs, val.coeffs, fillvalue=0 ) ]
        else:                                                # add scalar
            if self.coeffs:
                res = self.coeffs[ : ]
                res[ 0 ] += val
            else:
                res = val

        return self.__class__( res )

    def __call__( self, val ):
        "Evaluate at X==val"
        res = 0
        pwr = 1

        for co in self.coeffs:
            res += co * pwr
            pwr *= val

        return res

    def __eq__( self, val ):
        "Test self==val"
        if isinstance( val, Polynomial ):
            return self.coeffs == val.coeffs
        else:
            return len( self.coeffs ) == 1 and self.coeffs[ 0 ] == val

    def __mul__( self, val ):
        "Return self*val"
        if isinstance( val, Polynomial ):
            _s = self.coeffs
            _v = val.coeffs
            res = [ 0 ] * ( len( _s ) + len( _v ) - 1 )

            for selfpow, selfco in enumerate( _s ):
                for valpow,valco in enumerate( _v ):
                    res[ selfpow + valpow ] += selfco * valco
        else:
            res = [ co * val for co in self.coeffs ]
        return self.__class__( res )

    def __neg__( self ):
        "Return -self"
        return self.__class__( [ -co for co in self.coeffs ] )

    def __pow__( self, y, z = None ):
        raise NotImplemented( )

    def _radd__( self, val ):
        "Return val+self"
        return self + val

    def __repr__( self ):
        return "{0}({1})".format( self.__class__.__name__, self.coeffs )

    def __rmul__( self, val ):
        "Return val*self"
        return self * val

    def __rsub__( self, val ):
        "Return val-self"
        return -self + val

    def __str__( self ):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = [ ]

        for po, co in enumerate( self.coeffs ):
            if co:
                if po == 0:
                    po = ''
                elif po == 1:
                    po = 'X'
                else:
                    po = 'X^' + str( po )

                res.append( str( co ) + po )

        if res:
            res.reverse( )
            return ' + '.join( res )
        else:
            return "0"

    def __sub__( self, val ):
        "Return self-val"
        return self.__add__( -val )

    def trim( self ):
        "Remove trailing 0-coefficients"
        _co = self.coeffs

        if _co:
            offs = len( _co ) - 1

            if _co[ offs ] == 0:
                offs -= 1

                while offs >= 0 and _co[ offs ] == 0:
                    offs -= 1

                del _co[ offs + 1 : ]

    def getCoefficients( self ):
        return self.coeffs


#//******************************************************************************
#//
#//  downloadOEISSequence
#//
#//******************************************************************************

def downloadOEISSequence( id ):
    keywords = downloadOEISText( id, 'K' ).split( ',' )

    if 'nonn' in keywords:
        result = downloadOEISText( id, 'S' )
        result += downloadOEISText( id, 'T' )
        result += downloadOEISText( id, 'U' )
    else:
        result = downloadOEISText( id, 'V' )
        result += downloadOEISText( id, 'W' )
        result += downloadOEISText( id, 'X' )

    if 'cons' in keywords:
        offset = int( downloadOEISText( id, 'O' ).split( ',' )[ 0 ] )
        result = ''.join( result.split( ',' ) )
        return mpmathify( result[ : offset ] + '.' + result[ offset : ] )
    else:
        return [ int( i ) for i in result.split( ',' ) ]


#//******************************************************************************
#//
#//  downloadOEISText
#//
#//******************************************************************************

def downloadOEISText( id, char, addCR=False ):
    import urllib.request
    import re as regex

    data = urllib.request.urlopen( 'http://oeis.org/search?q=id%3AA{:06}'.format( id ) + '&fmt=text' ).read( )

    pattern = regex.compile( b'%' + bytes( char, 'ascii' ) + b' A[0-9][0-9][0-9][0-9][0-9][0-9] (.*?)\n', regex.DOTALL )

    lines = pattern.findall( data )

    result = ''

    for line in lines:
        if result != '' and addCR:
            result += '\n'

        result += line.decode( 'ascii' )

    return result


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
    return loadTable( 'double_balanced_primes', { 1 : getNthDoubleBalancedPrime( 1 ) } )

def loadTripleBalancedPrimes( ):
    return loadTable( 'triple_balanced_primes', { 1 : getNthTripleBalancedPrime( 1 ) } )

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
    end = makeTable( start, end, step, getNthBalancedPrime, 'balanced' )
    saveBalancedPrimes( balancedPrimes )
    return end

def makeDoubleBalancedPrimes( start, end, step ):
    global doubleBalancedPrimes
    end = makeTable( start, end, step, getNthDoubleBalancedPrime, 'double_balanced' )
    saveDoubleBalancedPrimes( doubleBalancedPrimes )
    return end

def makeTripleBalancedPrimes( start, end, step ):
    global tripleBalancedPrimes
    end = makeTable( start, end, step, getNthTripleBalancedPrime, 'triple_balanced' )
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
    getNthTripletPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTripletPrime, 'triplet' )
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
    getNthQuintupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuintupletPrime, 'quint' )
    saveQuintupletPrimes( quintPrimes )
    return end

def makeSextupletPrimes( start, end, step ):
    global sextPrimes
    getNthSextupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthSextupletPrime, 'sext' )
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
#//  getNextPrime
#//
#//******************************************************************************

def getNextPrime( p, f, func = getNextPrimeCandidate ):
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
        p, f = getNextPrime( p, f )
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
        p, f = getNextPrime( p, f )

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
#//  getNthAperyNumber
#//
#//  http://oeis.org/A005259
#//
#//  a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
#//
#//******************************************************************************

def getNthAperyNumber( n ):
    result = 0

    for k in arange( 0, n + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ), power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


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

    if n == 1:
        return 3

    if n >= 100:
        if cousinPrimes == { }:
            cousinPrimes = loadCousinPrimes( )

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
#//  getNthSexyQuadrupletList
#//
#//******************************************************************************

def getNthSexyQuadrupletList( arg ):
    p = getNthSexyQuadrupletPrime( arg )
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

        currentIndex = max( key for key in tripletPrimes if key <= n )
        p = tripletPrimes[ currentIndex ]

        if isPrime( p + 2 ):
            middle = 2
        else:
            middle = 4

    else:
        currentIndex = 3
        p = 11
        middle = 2

    f = p % 10

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
            if isPrime( p + 2 ) or isPrime( p + 4 ):
                currentIndex += 1

    if updateDicts:
        tripletPrimes[ int( arg ) ] = p

    return p


#//******************************************************************************
#//
#//  getNthTripletPrimeList
#//
#//******************************************************************************

def getNthTripletPrimeList( arg ):
    p = getNthTripletPrime( arg )
    f = p % 10

    return [ p, getNextPrime( p, f )[ 0 ], fadd( p, 6 ) ]


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

    if n == 1:
        return 5
    elif n == 2:
        return 7

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
    p = getNthQuintupletPrime( arg )

    f = p % 10

    if f == 1:
        return [ p, fadd( p, 2 ), fadd( p, 6 ), fadd( p, 8 ), fadd( p, 12 ) ]
    elif f == 7:
        return [ p, fadd( p, 4 ), fadd( p, 6 ), fadd( p, 10 ), fadd( p, 12 ) ]
    else:
        # not the right exception type
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

    if n == 1:
        return 7

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

    return p


#//******************************************************************************
#//
#//  getNthSextupletPrimeList
#//
#//******************************************************************************

def getNthSextupletPrimeList( arg ):
    p = getNthSextpletPrime( arg )
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
            raise ValueError( 'ContinuedFraction requires a number or a list' )

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
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


#//******************************************************************************
#//
#//  getDivisorCount
#//
#//******************************************************************************

def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in factor( n ) ] )


#//******************************************************************************
#//
#//  getDivisors
#//
#//******************************************************************************

def getDivisors( n ):
    result = getExpandedFactorList( factor( n ) )

    result = [ list( i ) for i in itertools.chain.from_iterable( itertools.combinations( result, r ) for r in range( 0, len( result ) + 1 ) ) ]

    from operator import mul
    result = set( [ reduce( mul, i, 1 ) for i in result[ 1 : ] ] )
    result.add( 1 )

    result = sorted( list( result ) )

    return result


#//******************************************************************************
#//
#//  factor
#//
#//  This is not my code, and I need to find the source so I can attribute it.
#//
#//******************************************************************************

def factor( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factor( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def getPotentialPrimes( ):
            basePrimes = ( 2, 3, 5 )

            for basePrime in basePrimes:
                yield basePrime

            basePrimes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            primeGroup = 0

            while True:
                for basePrime in basePrimes:
                    yield primeGroup + basePrime

                primeGroup += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in getPotentialPrimes( ):
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
    result = ''

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

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + '1'
            else:
                result = result + '0'

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
    leftDigits = value

    while leftDigits > 0:
        if baseAsDigits:
            if result != '':
                result = ' ' + result

            result = str( int( leftDigits ) % base ) + result
        else:
            result = numerals[ int( leftDigits ) % base ] + result

        leftDigits = floor( fdiv( leftDigits, base ) )

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
#//  getBitCount
#//
#//******************************************************************************

def getBitCount( n ):
    result = 0

    value = int( n )

    while ( value ):
        value &= value - 1
        result += 1

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
#//  getNthJacobsthalNumber
#//
#//  From: http://oeis.org/A001045
#//
#//  a(n) = ceiling(2^(n+1)/3)-ceiling(2^n/3)
#//
#//******************************************************************************

def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthPellNumber
#//
#//  From:  http://oeis.org/A000129
#//
#//  a(n) = round((1+sqrt(2))^n)
#//
#//******************************************************************************

def getNthPellNumber( n ):
    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthBaseKRepunit
#//
#//******************************************************************************

def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( k ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


#//******************************************************************************
#//
#//  getPrimePi
#//
#//******************************************************************************

def getPrimePi( n ):
    result = primepi2( n )

    return [ mpf( result.a ), mpf( result.b ) ]


#//******************************************************************************
#//
#//  getNthTribonacci
#//
#//******************************************************************************

def getNthTribonacci( n ):
    roots = polyroots( [ 1, -1, -1, -1  ] )
    roots2 = polyroots( [ 44, 0, -2, -1 ] )

    result = 0

    for i in range( 0, 3 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthTetranacci
#//
#//  http://mathworld.wolfram.com/TetranacciNumber.html
#//
#//******************************************************************************

def getNthTetranacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1 ] )
    roots2 = polyroots( [ 563, 0, -20, -5, -1 ] )

    result = 0

    for i in range( 0, 4 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthPentanacci
#//
#//******************************************************************************

def getNthPentanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 5 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 8, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHexanacci
#//
#//******************************************************************************

def getNthHexanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 6 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 10, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHeptanacci
#//
#//******************************************************************************

def getNthHeptanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 7 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 3, 12, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


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
#//  getNthPolygonalNumber
#//
#//******************************************************************************

def getNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coeff = fdiv( fsub( k, 2 ), 2 )
    return polyval( [ coeff, fneg( fsub( coeff, 1 ) ), 0 ], n )


#//******************************************************************************
#//
#//  getRegularPolygonArea
#//
#//  based on having sides of unit length
#//
#//  http://www.mathopenref.com/polygonregulararea.html
#//
#//******************************************************************************

def getRegularPolygonArea( n ):
    if n < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) )


#//******************************************************************************
#//
#//  getHypersphereSurfaceArea
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, radius k
#//
#//******************************************************************************

def getHypersphereSurfaceArea( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    return fmul( fdiv( fmul( n, power( pi, fdiv( n, 2 ) ) ),
                       gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, fsub( n, 1 ) ) )


#//******************************************************************************
#//
#//  getHypersphereVolume
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, radius k
#//
#//******************************************************************************

def getHypersphereVolume( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    return fmul( fdiv( power( pi, fdiv( n, 2 ) ),
                       gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, n ) )


#//******************************************************************************
#//
#//  getTriangleArea
#//
#//  https://en.wikipedia.org/wiki/Equilateral_triangle#Area
#//
#//******************************************************************************

def getTriangleArea( a, b, c ):
    return fdiv( fsum( [ power( a, 2 ), power( b, 2 ), power( c, 2 ) ] ), fmul( 4, sqrt( 3 ) ) )


#//******************************************************************************
#//
#//  findNthPolygonalNumber
#//
#//  http://www.wolframalpha.com/input/?i=solve+%28+%28+k+%2F+2+%29+-+1+%29+x^2+-+%28+%28+k+%2F+2+%29+-+2+%29+x+%2B+0+%3D+n+for+x
#//
#//******************************************************************************

def findNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( fsum( [ sqrt( fsum( [ power( k, 2 ), fprod( [ 8, k, n ] ),
                                       fneg( fmul( 8, k ) ), fneg( fmul( 16, n ) ), 16 ] ) ),
                         k, -4 ] ), fmul( 2, fsub( k, 2 ) ) )


#//******************************************************************************
#//
#//  getCenteredPolygonalNumber
#//
#//******************************************************************************

def getCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coefficient = fdiv( k, 2 )
    return polyval( [ coefficient, fneg( coefficient ), 1 ], n )


#//******************************************************************************
#//
#//  findCenteredPolygonalNumber
#//
#//  wolframalpha.com solved this for me.
#//
#//******************************************************************************

def findCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    s = fdiv( k, 2 )

    return fdiv( fadd( sqrt( s ), sqrt( fsum( [ fmul( 4, n ), s, -4 ] ) ) ), fmul( 2, sqrt( s ) ) )


#//******************************************************************************
#//
#//  getNthHexagonalSquareNumber
#//
#//  http://oeis.org/A046177
#//
#//  a(n) = floor(1/32*(tan(3*pi/8))^(8*n-4))
#//
#//******************************************************************************

#//******************************************************************************
#//
#//  getNthHexagonalPentagonalNumber
#//
#//  http://oeis.org/A046178
#//
#//  a(n) = ceiling(1/12*(sqrt(3)-1)*(2+sqrt(3))^(4n-2)).
#//
#//******************************************************************************

#//******************************************************************************
#//
#//  getNthHeptagonalTriangularNumber
#//
#//  http://oeis.org/A046194
#//
#//  a(n) = 1/80*((3-sqrt(5)*(-1)^n)*(2+sqrt(5))^(4n-2)+
#//               (3+sqrt(5)*(-1)^n)*(2-sqrt(5))^(4n-2)-14)
#//
#//  LinearRecurrence[ { 1, 103682, -103682, -1, 1 },
#//                    { 1, 55, 121771, 5720653, 12625478965 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalTriangularNumber( n ):
    #return floor( fdiv( fsum( [ fmul( fmul( fsub( 3, sqrt( 5 ) ), power( -1, n ) ) ),
    #                                power( fadd( 2, sqrt( 5 ) ), fsub( fmul( 4, n ), 2 ) ) ),
    #                            fmul( fmul( fadd( 3, sqrt( 5 ) ), power( -1, n ) ) ),
    #                                  power( fsub( 2, sqrt( 5 ) ), fsub( fmul( 4, n ), 2 ) ) ),
    #                            14 ] ),
    #                    80 ) )

    return getNthLinearRecurrence( [ 1, -1, -103682, 103682, 1 ],
                                   [ 1, 55, 121771, 5720653, 12625478965 ], n )


#//******************************************************************************
#//
#//  getNthHeptagonalSquareNumber
#//
#//  http://oeis.org/A046195
#//
#//  LinearRecurrence[ { 1 , 0, 1442, -1442, 0, -1, 1 },
#//                    { 1, 6, 49, 961, 8214, 70225, 1385329 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalSquareNumber( n ):
    index = getNthLinearRecurrence( [ 1, -1, 0, -1442, 1442, 0, 1 ],
                                    [ 1, 6, 49, 961, 8214, 70225, 1385329 ], n )

    return getNthPolygonalNumber( index, 7 )


#//******************************************************************************
#//
#//  getNthHeptagonalPentagonalNumber
#//
#//  http://oeis.org/A048900
#//
#//  a(n) = floor(1/240*((2+sqrt(15))^2*(4+sqrt(15))^(4n-3)))
#//
#//******************************************************************************

def getNthHeptagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( power( fadd( 2, sqrt( 15 ) ), 2 ),
                              power( fadd( 4, sqrt( 15 ) ), fsub( fmul( 4, n ), 3 ) ) ), 240 ) )


#//******************************************************************************
#//
#//  getNthHeptagonalHexagonalNumber
#//
#//  http://oeis.org/A048903
#//
#//  a(n) = floor(1/80*(sqrt(5)-1)*(2+sqrt(5))^(8n-5))
#//
#//******************************************************************************

def getNthHeptagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( sqrt( 5 ), 1 ),
                              power( fadd( 2, sqrt( 5 ) ), fsub( fmul( 8, n ), 5 ) ) ), 80 ) )


#//******************************************************************************
#//
#//  getNthOctagonalTriangularNumber
#//
#//  From http://oeis.org/A046183
#//
#//  a(n) = floor(1/96*(7-2*sqrt(6)*(-1)^n)*(sqrt(3)+sqrt(2))^(4n-2))
#//
#//  LinearRecurrence[{1, 9602, -9602, -1, 1}, {1, 21, 11781, 203841, 113123361}, 13]
#//
#//******************************************************************************

def getNthOctagonalTriangularNumber( n ):
    sign = power( -1, n )

    return floor( fdiv( fmul( fsub( 7, fprod( [ 2, sqrt( 6 ), sign ] ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                        96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalSquareNumber
#//
#//  From http://oeis.org/A036428:
#//
#//  a(n) = 1/12 * ((2 + sqrt(3)) ^ (4n-2) + (2 - sqrt(3)) ^ (4n-2) - 2).
#//  a(n) = floor (1/12 * (2 + sqrt(3)) ^ (4n-2)).
#//
#//******************************************************************************

def getNthOctagonalSquareNumber( n ):
    return floor( fdiv( power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ), 12 ) )


#//******************************************************************************
#//
#//  getNthOctagonalPentagonalNumber
#//
#//  http://oeis.org/A046189
#//
#//  a(n) = floor(1/96*(11-6*sqrt(2)*(-1)^n)*(1+sqrt(2))^(8*n-6))
#//
#//******************************************************************************

def getNthOctagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( fsub( 11, fprod( [ 6, sqrt( 2 ), power( -1, n ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 8, n ), 6 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHexagonalNumber
#//
#//  http://oeis.org/A046192
#//
#//  a(n) = floor(1/96*(3*sqrt(3)-sqrt(2))*(sqrt(3)+sqrt(2))^(8n-5))
#//
#//******************************************************************************

def getNthOctagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( fmul( 3, sqrt( 3 ) ), sqrt( 2 ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 8, n ), 5 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHeptagonalNumber
#//
#//  http://oeis.org/A048906
#//
#//  a(n) = floor(1/480*(17+2*sqrt(30))*(sqrt(5)+sqrt(6))^(8n-6))
#//
#//******************************************************************************

def getNthOctagonalHeptagonalNumber( n ):
    return floor( fdiv( fmul( fadd( 17, fmul( sqrt( 30 ), 2 ) ),
                              power( fadd( sqrt( 5 ), sqrt( 6 ) ), fsub( fmul( 8, n ), 6 ) ) ), 480 ) )


#//******************************************************************************
#//
#//  getNthNonagonalTriangularNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = ( 5/14 ) +
#//           ( 9/28 ) * { [ 8 - 3 * sqrt(7) ] ^ n + [ 8 + 3 * sqrt( 7 ) ] ^ n } +
#//           ( 3/28 ) * sqrt(7) * { [ 8 + 3 * sqrt(7) ] ^ n - [ 8 - 3 * sqrt(7) ] ^ n }
#//
#//******************************************************************************

def getNthNonagonalTriangularNumber( n ):
    a = fmul( 3, sqrt( 7 ) )
    b = fadd( 8, a )
    c = fsub( 8, a )

    return fsum( [ fdiv( 5, 14 ),
                   fmul( fdiv( 9, 28 ), fadd( power( b, n ), power( c, n ) ) ),
                   fprod( [ fdiv( 3, 28 ),
                            sqrt( 7 ),
                            fsub( power( b, n ), power( c, n ) ) ] ) ] )


#//******************************************************************************
#//
#//  getNthNonagonalSquareNumber
#//
#//  From http://oeis.org/A048911:
#//
#//  Indices of square numbers which are also 9-gonal.
#//
#//  Let p = 8 * sqrt( 7 ) + 9 * sqrt( 14 ) - 7 * sqrt( 2 ) - 28 and
#//      q = 7 * sqrt( 2 ) + 9 * sqrt( 14 ) - 8 * sqrt( 7 ) - 28.
#//
#//  Then a( n ) = 1 / 112 *
#//                 ( ( p + q * (-1) ^ n ) * ( 2 * sqrt( 2 ) + sqrt( 7 ) ) ^ n -
#//                  ( p - q * (-1) ^ n ) * ( 2 * sqrt( 2 ) - sqrt( 7 ) ) ^ ( n - 1 ) )
#//
#//******************************************************************************

def getNthNonagonalSquareNumber( n ):
    p = fsum( [ fmul( 8, sqrt( 7 ) ), fmul( 9, sqrt( 14 ) ), fmul( -7, sqrt( 2 ) ), -28 ] )
    q = fsum( [ fmul( 7, sqrt( 2 ) ), fmul( 9, sqrt( 14 ) ), fmul( -8, sqrt( 7 ) ), -28 ] )
    sign = power( -1, n )

    index = fdiv( fsub( fmul( fadd( p, fmul( q, sign ) ),
                                    power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), n ) ),
                              fmul( fsub( p, fmul( q, sign ) ),
                                    power( fsub( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), fsub( n, 1 ) ) ) ), 112 )

    return power( round( index ), 2 )


#//******************************************************************************
#//
#//  getNthNonagonalPentagonalNumber
#//
#//  http://oeis.org/A048915
#//
#//  a(n) = floor(1/336*(25+4*sqrt(21))*(5-sqrt(21)*(-1)^n)*(2*sqrt(7)+3*sqrt(3))^(4n-4)).
#//
#//  LinearRecurrence[{1, 146361602, -146361602, -1, 1}, {1, 651, 180868051, 95317119801, 26472137730696901}, 9]
#//
#//******************************************************************************

def getNthNonagonalPentagonalNumber( n ):
    sqrt21 = sqrt( 21 )
    sign = power( -1, n )

    return floor( fdiv( fprod( [ fadd( 25, fmul( 4, sqrt21 ) ),
                                 fsub( 5, fmul( sqrt21, sign ) ),
                                 power( fadd( fmul( 2, sqrt( 7 ) ), fmul( 3, sqrt( 3 ) ) ),
                                        fsub( fmul( 4, n ), 4 ) ) ] ),
                        336 ) )


#//******************************************************************************
#//
#//  getNthNonagonalHexagonalNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = floor( 9/112 * ( 8 - 3 * sqrt( 7 ) * (-1) ^ n ) *
#//                          ( 8 + 3 * sqrt( 7 ) ) ^ ( 4 * n - 4 ) )
#//
#//******************************************************************************

def getNthNonagonalHexagonalNumber( n ):
    #a = fmul( 3, sqrt( 7 ) )
    #b = fadd( 8, a )
    #c = fsub( 8, a )

    #sign = 1 #power( -1, n )
    #exponent = fsub( fmul( 4, n ), 4 )

    #print( str( fmul( c, sign ) ) + '  ' + str( power( b, exponent ) ) )

    #return floor( fprod( [ fdiv( 9, 112 ), fmul( c, sign ), power( b, exponent ) ] ) )

    return getNthLinearRecurrence( [ 1, -1, -4162056194, 4162056194, 1 ],
                                   [ 1, 325, 5330229625, 1353857339341, 22184715227362706161 ], n )


#//******************************************************************************
#//
#//  getNthNonagonalHeptagonalNumber
#//
#//  From http://oeis.org/A048921
#//
#//  a(n) = floor(1/560*(39+4*sqrt(35))*(6+sqrt(35))^(4*n-3)).
#//
#//  LinearRecurrence[{20163, -20163, 1}, {1, 26884, 542041975}, 9]; (* Ant King, Dec 31 2011 *)
#//
#//******************************************************************************

def getNthNonagonalHeptagonalNumber( n ):
    sqrt35 = sqrt( 35 )

    return floor( fdiv( fmul( fadd( 39, fmul( 4, sqrt35 ) ),
                        power( fadd( 6, sqrt35 ), fsub( fmul( 4, n ), 3 ) ) ),
                        560 ) )


#//******************************************************************************
#//
#//  getNthNonagonalOctagonalNumber
#//
#//  From http://oeis.org/A048924:
#//
#//  a(n) = floor(1/672*(11*sqrt(7)-9*sqrt(6))*(sqrt(6)+sqrt(7))^(8n-5)).
#//
#//  LinearRecurrence[{454275, -454275, 1}, {1, 631125, 286703855361}, 30] (* Vincenzo Librandi, Dec 24 2011 *)
#//
#//******************************************************************************

def getNthNonagonalOctagonalNumber( n ):
    sqrt6 = sqrt( 6 )
    sqrt7 = sqrt( 7 )

    return floor( fdiv( fmul( fsub( fmul( 11, sqrt7 ), fmul( 9, sqrt6 ) ),
                              power( fadd( sqrt6, sqrt7 ), fsub( fmul( 8, n ), 5 ) ) ),
                        672 ) )

# Dec-tri
# http://oeis.org/A133216
# a(n) = floor ( 1/64 * (9 + 4*sqrt(2)*(-1)^n) * (1+sqrt(2))^(4*n-6) )

# Dec-square
# http://oeis.org/A133142
#  a(n)=(1/8)+(7/16)*[721-228*sqrt(10)]^n-(1/8)*[721-228*sqrt(10)]^n*sqrt(10)+(1/8)*[721+228 *sqrt(10)]^n*sqrt(10)+(7/16)*[721+228*sqrt(10)]^n

# Dec-pent
# http://oeis.org/A202563
# a(n) = floor(25/192*(sqrt(3)+sqrt(2))^(8*n-6))

# Dec-hex
# http://oeis.org/A203134
# a(n) = floor(1/64 *(5*sqrt(2)-1)*(sqrt(2)+1)^(8*n-5)).

# Dec-hept
# http://oeis.org/A203408
# a(n) = floor(1/320*(11-2*sqrt(10)*(-1)^n)*(1+sqrt(10))* (3+sqrt(10))^(4*n-3)).

# Dec-oct
# http://oeis.org/A203624
# a(n) = floor(1/192*(13+4*sqrt(3))*(2+sqrt(3))^(8*n-6)).

# Dec-non
# http://oeis.org/A203627
# a(n) = floor(1/448*(15+2*sqrt(14))*(2*sqrt(2)+sqrt(7))^(8*n-6)).

#//******************************************************************************
#//
#//  findTetrahedralNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def findTetrahedralNumber( n ):
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
#//  getNthPolygonalPyramidalNumber
#//
#//******************************************************************************

def getNthPolygonalPyramidalNumber( n, k ):
    return fprod( [ n, fadd( n, 1 ),
                    fsub( fmul( fsub( k, 2 ), n ), fsub( k, 5 ) ),
                    fdiv( 1, 6 ) ] )


#// A002415         4-dimensional pyramidal numbers: n^2*(n^2-1)/12.
#//                                                  n^4 - n^2 / 12
#//
#// A005585         5-dimensional pyramidal numbers: n(n+1)(n+2)(n+3)(2n+3)/5!.
#//
#// A001608         Perrin sequence (or Ondrej Such sequence): a(n) = a(n-2) + a(n-3).
#//                 LinearRecurrence[{0, 1, 1}, {3, 0, 2}, n]
#//
#// A001845         Centered octahedral numbers (crystal ball sequence for cubic lattice).
#//                 LinearRecurrence[{4, -6, 4, -1}, {1, 7, 25, 63}, 40]
#//
#// A046090         Consider all Pythagorean triples (X,X+1,Z) ordered by increasing Z; sequence gives X+1 values.
#//                 a(n+1)=round((1+(7+5*sqrt(2))*(3+2*sqrt(2))^n)/2);
#//                 LinearRecurrence[{7, -7, 1}, {1, 4, 21}, 25]
#//
#// A050534         Tritriangular numbers: a(n)=binomial(binomial(n,2),2) = n(n + 1)(n - 1)(n - 2)/8.
#//
#// A002817         Doubly triangular numbers: n*(n+1)*(n^2+n+2)/8.
#//                 a(n) = 3*binomial(n+2, 4)+binomial(n+1, 2).
#//
#// A007588         Stella octangula numbers: n*(2*n^2 - 1).
#//
#// A005803         Second-order Eulerian numbers: 2^n - 2*n.
#//
#// A060888         n^6-n^5+n^4-n^3+n^2-n+1.      -- general form of this
#//
#// A048736         Dana Scott's sequence: a(n) = (a(n-2) + a(n-1) * a(n-3)) / a(n-4), a(0) = a(1) = a(2) = a(3) = 1.
#//
#// A022095         Fibonacci sequence beginning 1 5.
#//                 a(n) = ((2*sqrt(5)-1)*(((1+sqrt(5))/2)^(n+1)) + (2*sqrt(5)+1)*(((1-sqrt(5))/2)^(n+1)))/(sqrt(5)).
#//
#// A005894         Centered tetrahedral numbers.
#//                 a(n)=(2*n+1)*(n^2+n+3)/3
#//
#// A015447         Generalized Fibonacci numbers: a(n) = a(n-1) + 11*a(n-2).
#//                 a(n)={[ (1+3*sqrt(5))/2 ]^(n+1) - [ (1-3*sqrt(5))/2 ]^(n+1)}/3*sqrt(5).
#//                 LinearRecurrence[{1, 11}, {1, 1}, 30]
#//                 CoefficientList[Series[ 1/(1-x-11 x^2), {x, 0, 50}], x]
#//
#// A046176         Indices of square numbers which are also hexagonal.
#//
#// A056105         First spoke of a hexagonal spiral.
#//
#// A006522         4-dimensional analogue of centered polygonal numbers. Also number of regions created by sides and diagonals of n-gon in general position.
#//                 a(n)=binomial(n, 4)+ binomial(n-1, 2)
#//
#// A022086         Fibonacci sequence beginning 0 3.
#//                 a(n) = round( (6phi-3)/5 phi^n ) (works for n>2)
#//
#// A069778         q-factorial numbers 3!_q.
#//
#// A005021         Random walks (binomial transform of A006054).
#//
#// A074584         Esanacci ("6-anacci") numbers.
#//                 LinearRecurrence[{1, 1, 1, 1, 1, 1}, {6, 1, 3, 7, 15, 31}, 50]
#//
#// A195142         Concentric 10-gonal numbers.
#//
#// A000453         Stirling numbers of the second kind, S(n,4).
#//
#// A005915         Hexagonal prism numbers: (n + 1)*(3*n^2 + 3*n + 1).
#//
#// A015442         Generalized Fibonacci numbers: a(n) = a(n-1) + 7 a(n-2), a(0)=0, a(1)=1.
#//                 a(n) = ( ((1+sqrt(29))/2)^(n+1) - ((1-sqrt(29))/2)^(n+1) )/sqrt(29)
#//
#// A002418         4-dimensional figurate numbers: (5*n-1)*binomial(n+2,3)/4.
#//
#// A005165         Alternating factorials: n! - (n-1)! + (n-2)! - ... 1!.
#//
#// A006007         4-dimensional analogue of centered polygonal numbers: a(n) = n(n+1)*(n^2+n+4)/12.
#//
#// A104621         Heptanacci-Lucas numbers.
#//


#//******************************************************************************
#//
#//  getNthStellaOctangulaNumber
#//
#//  Stel(n) = Oct(n) + 8 Tet(n-1)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthStellaOctangulaNumber( n ):
    return polyval( [ 4, 0, -2 ], n )


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
#//  (1/(d-1)!) PI k=0 to n-1 (n+k)
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
#//  getNthDelannoyNumber
#//
#//******************************************************************************

def getNthDelannoyNumber( n ):
    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


#//******************************************************************************
#//
#//  getNthSchroederNumber
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getNthMotzkinNumber
#//
#//  http://oeis.org/A001006
#//
#//  a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
#//
#//******************************************************************************

def getNthMotzkinNumber( n ):
    result = 0

    for j in arange( 0, floor( fdiv( n, 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                      binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


#//******************************************************************************
#//
#//  getNthPadovanNumber
#//
#//  Padovan sequence: a(n) = a(n-2) + a(n-3) with a(0)=1, a(1)=a(2)=0.
#//
#//  http://oeis.org/A000931
#//
#//  a(n) = (r^n)/(2r+3) + (s^n)/(2s+3) + (t^n)/(2t+3) where r, s, t are the
#//  three roots of x^3-x-1
#//
#//  http://www.wolframalpha.com/input/?i=solve+x^3-x-1
#//
#//  Unfortunately, the roots are scary-complicated, but it's a non-iterative
#//  formula, so I'll use it.
#//
#//  Wikipedia leaves off the first 4 terms, but Sloane's includes them.
#//  Wikipedia cites Ian Stewart and Mathworld, and I'll use their definition.
#//
#//******************************************************************************

def getNthPadovanNumber( arg ):
    result = 0

    n = fadd( arg, 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    e = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, e ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, e ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, e ) ) )

    return round( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                              fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                              fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )

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
    if not isinstance( i, list ):
        i = [ i ]

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
#//  This is a list operator so if the integer argument (base) is also a list,
#//  we need to handle that explicitly here.
#//
#//******************************************************************************

def interpretAsBase( args, base ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ interpretAsBase( i, base ) for i in args ]
        else:
            args.reverse( )
    else:
        args = [ args ]

    if isinstance( base, list ):
        return [ interpretAsBase( args, i ) for i in base ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


#//******************************************************************************
#//
#//  unpackInteger
#//
#//******************************************************************************

def unpackInteger( n, fields ):
    if isinstance( n, list ):
        return [ unpackInteger( i, fields ) for i in n ]

    if not isinstance( fields, list ):
        return unpackInteger( n, [ fields ] )

    value = int( n )
    result = [ ]

    for i in reversed( fields ):
        size = int( i )
        result.insert( 0, value & ( 2 ** size - 1 ) )
        value >>= size

    return result


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
            raise ValueError( 'invalid equation, no variable coefficients' )
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
    sqrtN = sqrt( n )

    return 1 if sqrtN == floor( sqrtN ) else 0


#//******************************************************************************
#//
#//  addPolynomials
#//
#//******************************************************************************

def addPolynomials( a, b ):
    result = Polynomial( a )
    result += Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  multiplyPolynomials
#//
#//******************************************************************************

def multiplyPolynomials( a, b ):
    result = Polynomial( a )
    result *= Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  evaluatePolynomial
#//
#//******************************************************************************

def evaluatePolynomial( a, b ):
    if not isinstance( a, list ):
        a = [ a ]

    return polyval( a, b )


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
#//  evaluateOneListFunction
#//
#//******************************************************************************

def evaluateOneListFunction( func, args ):
    if isinstance( args, list ):
        for arg in args:
            if isinstance( arg, list ):
                return [ evaluateOneListFunction( func, arg ) for arg in args ]

        return func( args )
    else:
        return func( [ args ] )


#//******************************************************************************
#//
#//  getAlternatingSum
#//
#//******************************************************************************

def getAlternatingSum( args ):
    for i in range( 1, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getAlternatingSum2
#//
#//******************************************************************************

def getAlternatingSum2( args ):
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
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getGCD[ arg ] for arg in args ]
        else:
            result = max( args )

            for pair in itertools.permutations( args, 2 ):
                gcd = getGCDForTwo( *pair )

                if gcd < result:
                    result = gcd

                return result
    else:
        return args


#//******************************************************************************
#//
#//  multiplyListOfPolynomials
#//
#//******************************************************************************

def multiplyListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    for i in range( 1, len( args ) ):
        if isinstance( args[ i ], list ) and isinstance( args[ i ][ 0 ], list ):
            pass  # dunno what to do here
        else:
            result *= Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  addListOfPolynomials
#//
#//******************************************************************************

def addListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    for i in range( 1, len( args ) ):
        result += Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  getGreedyEgyptianFraction
#//
#//******************************************************************************

def getGreedyEgyptianFraction( n, d ):
    if n > d:
        raise ValueError( "'egypt' requires the numerator to be smaller than the denominator" )

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
#//  dumpOperators
#//
#//******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )

    print( 'special operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    return [ int( i ) for i in RPN_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  convertToSignedInt
#//
#//  two's compliment logic is effect here
#//
#//******************************************************************************

def convertToSignedInt( n, k ):
    value = fadd( n, ( power( 2, fsub( k, 1 ) ) ) )
    value = fmod( value, power( 2, k ) )
    value = fsub( value, ( power( 2, fsub( k, 1 ) ) ) )

    return value


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
    global unitConversionMatrix

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) + len( modifiers ) ) )
    print( '{:10,} unit conversions'.format( len( unitConversionMatrix ) ) )
    print( )

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
#//  incrementNestedListLevel
#//
#//  Unlike all other operators, '[' and ']' change global state.
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
#//  appendLists
#//
#//******************************************************************************

def appendLists( valueList ):
    arg2 = valueList.pop( )
    arg1 = valueList.pop( )

    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = [ ]

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    valueList.append( result )


#//******************************************************************************
#//
#//  alternateSigns
#//
#//******************************************************************************

def alternateSigns( n ):
    for i in range( 1, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  alternateSigns2
#//
#//******************************************************************************

def alternateSigns2( n ):
    for i in range( 0, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  expandRange
#//
#//******************************************************************************

def expandRange( start, end ):
    if start > end:
        step = -1
    else:
        step = 1

    result = list( )

    for i in arange( start, end + step, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandSteppedRange
#//
#//******************************************************************************

def expandSteppedRange( start, end, step ):
    result = list( )

    for i in arange( start, end + 1, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandGeometricRange
#//
#//******************************************************************************

def expandGeometricRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = fmul( value, step )

    return result


#//******************************************************************************
#//
#//  interleave
#//
#//******************************************************************************

def interleave( arg1, arg2 ):
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

    return result


#//******************************************************************************
#//
#//  makeUnion
#//
#//******************************************************************************

def makeUnion( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    return result


#//******************************************************************************
#//
#//  makeIntersection
#//
#//******************************************************************************

def makeIntersection( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            for i in arg1:
                if i in arg2:
                    result.append( i )
        else:
            if arg2 in arg1:
                result.append( arg2 )
    else:
        if list2:
            if arg1 in arg2:
                result.append( arg1 )
        else:
            if arg1 == arg2:
                result.append( arg1 )

    return result


#//******************************************************************************
#//
#//  getIndexOfMax
#//
#//******************************************************************************

def getIndexOfMax( arg ):
    maximum = -inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] > maximum:
            maximum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  getIndexOfMin
#//
#//******************************************************************************

def getIndexOfMin( arg ):
    minimum = inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] < minimum:
            minimum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  unlist
#//
#//******************************************************************************

def unlist( valueList ):
    arg = valueList.pop( )

    if isinstance( arg, list ):
        for i in arg:
            valueList.append( i )
    else:
        valueList.append( arg )


#//******************************************************************************
#//
#//  flatten
#//
#//  http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
#//
#//******************************************************************************

def _flatten( L, containers=( list, tuple ) ):
    i = 0

    while i < len( L ):
        while isinstance( L[ i ], containers ):
            if not L[ i ]:
                L.pop( i )
                i -= 1
                break
            else:
                L[ i : i + 1 ] = ( L[ i ] )
        i += 1
    return L


def flatten( valueList ):
    valueList.append( _flatten( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getListElement
#//
#//******************************************************************************

def getListElement( arg, index ):
    if isinstance( arg, list ):
        return arg[ int( index ) ]
    else:
        return arg
        # TODO: throw exception if index > 0


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
#//  getNthLinearRecurrence
#//
#//  nth element of Fibonacci sequence = rpn [ 1 1 ] 1 n
#//  nth element of Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n
#//
#//******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    if not isinstance( recurrence, list ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, list ):
        seeds = [ seeds ]

    if len( seeds ) == 0:
        raise ValueError( 'internal error:  for operator \'linearrecur\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getNthLinearRecurrence( recurrence[ : i ], seeds, i ) )

    if isinstance( n, list ):
        return [ getNthLinearRecurrence( recurrence, seeds, i ) for i in n ]

    if n < len( seeds ):
        return seeds[ int( n ) - 1 ]
    else:
        if len( recurrence ) == 0:
            raise ValueError( 'internal error:  for operator \'linearrecur\', recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in arange( len( seeds ), n ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

            result.append( newValue )
            del result[ 0 ]

        return result[ -1 ]


#//******************************************************************************
#//
#//  countElements
#//
#//******************************************************************************

def countElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( countElements( args[ i ] ) )

        return result
    else:
        return len( args )


#//******************************************************************************
#//
#//  getListDiffs
#//
#//******************************************************************************

def getListDiffs( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListDiffs( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fsub( args[ i + 1 ], args[ i ] ) )

    return result


#//******************************************************************************
#//
#//  getUniqueElements
#//
#//******************************************************************************

def getUniqueElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( getUniqueElements( args[ i ] ) )

    else:
        seen = set( )

        for i in range( 0, len( args ) ):
            seen.add( args[ i ] )

        result = [ ]

        for i in seen:
            result.append( i )

    return result


#//******************************************************************************
#//
#//  sortAscending
#//
#//******************************************************************************

def sortAscending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ] ) )

        return result
    else:
        return sorted( args )


#//******************************************************************************
#//
#//  sortDescending
#//
#//******************************************************************************

def sortDescending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ], reverse=True ) )

        return result
    else:
        return sorted( args, reverse=True )


#//******************************************************************************
#//
#//  getStandardDeviation
#//
#//******************************************************************************

def getStandardDeviation( args ):
    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fsum( dev ) / len( dev ) )


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
#//  evaluateOneArgFunction
#//
#//******************************************************************************

def evaluateOneArgFunction( func, args ):
    if isinstance( args, list ):
        return [ evaluateOneArgFunction( func, i ) for i in args ]
    else:
        return func( args )


#//******************************************************************************
#//
#//  evaluateTwoArgFunction
#//
#//******************************************************************************

def evaluateTwoArgFunction( func, arg1, arg2 ):
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


callers = [
    lambda func, args: [ func( ) ],
    evaluateOneArgFunction,
    evaluateTwoArgFunction,
    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for c in arg1 for b in arg2 for a in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for d in arg1 for c in arg2 for b in arg3 for a in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for e in arg1 for d in arg2 for c in arg3 for b in arg4 for a in arg5 ],
]


#//******************************************************************************
#//
#//  convertUnits
#//
#//******************************************************************************

def convertUnits( valueList ):
    global unitStack
    global unitConversionMatrix

    unit2 = unitStack.pop( )
    unit1 = unitStack.pop( )

    conversion = unit1.getConversion( unit2 )

    # this way you can do a conversion without specifying an amount... it will default to 1
    if len( valueList ) == 0:
        valueList.append( mpmathify( 1 ) )

        return evaluateOneArgFunction( lambda i: fmul( i, conversion ), valueList.pop( ) )
    else:
        raise ValueError( 'no conversion is defined between \'{}\' and \'{}\''.format( unit1, unit2 ) )


#//******************************************************************************
#//
#//  operatorAliases
#//
#//******************************************************************************

operatorAliases = {
    '!!'          : 'doublefac',
    '!'           : 'factorial',
    '%'           : 'modulo',
    '*'           : 'multiply',
    '**'          : 'power',
    '***'         : 'tetrate',
    '+'           : 'add',
    '-'           : 'subtract',
    '/'           : 'divide',
    '//'          : 'root',
    '1/x'         : 'reciprocal',
    'au'          : 'astronomical_unit',
    'average'     : 'mean',
    'avg'         : 'mean',
    'bal'         : 'balanced',
    'bal?'        : 'balanced?',
    'bal_'        : 'balanced_',
    'bits'        : 'countbits',
    'cbrt'        : 'root3',
    'ccube'       : 'centeredcube',
    'cdec'        : 'cdecagonal',
    'cdec?'       : 'cdecagonal?',
    'ceil'        : 'ceiling',
    'champ'       : 'champernowne',
    'chept'       : 'cheptagonal',
    'chept?'      : 'cheptagonal?',
    'chex'        : 'chexagonal',
    'chex?'       : 'chexagonal?',
    'cnon'        : 'cnonagonal',
    'cnon?'       : 'cnonagonal?',
    'coct'        : 'coctagonal',
    'coct?'       : 'coctagonal?',
    'cousin'      : 'cousinprime',
    'cousin?'     : 'cousinprime?',
    'cousin_'     : 'cousinprime_',
    'cpent'       : 'cpentagonal',
    'cpent?'      : 'cpentagonal?',
    'cpoly'       : 'cpolygonal',
    'cpoly?'      : 'cpolygonal?',
    'ctri'        : 'ctriangular',
    'ctri?'       : 'ctriangular?',
    'cuberoot'    : 'root3',
    'dec'         : 'decagonal',
    'dec?'        : 'decagonal?',
    'deg'         : 'degrees',
    'divcount'    : 'countdiv',
    'fac'         : 'factorial',
    'fac2'        : 'doublefac',
    'feet'        : 'foot',
    'fib'         : 'fibonacci',
    'floz'        : 'fluid_ounce',
    'frac'        : 'fraction',
    'harm'        : 'harmonic',
    'hept'        : 'heptagonal',
    'hept?'       : 'heptagonal?',
    'hex'         : 'hexagonal',
    'hex?'        : 'hexagonal?',
    'hyper4'      : 'tetrate',
    'int'         : 'integer',
    'inv'         : 'reciprocal',
    'isdiv'       : 'isdivisible',
    'issqr'       : 'issquare',
    'lb'          : 'pound',
    'left'        : 'shiftleft',
    'linear'      : 'linearrecur',
    'litre'       : 'liter',
    'log'         : 'ln',
    'metre'       : 'meter',
    'mi'          : 'mile',
    'mod'         : 'modulo',
    'mult'        : 'multiply',
    'neg'         : 'negative',
    'non'         : 'nonagonal',
    'non?'        : 'nonagonal?',
    'nonasq'      : 'nonasquare',
    'nonzeroes'   : 'nonzero',
    'oct'         : 'octagonal',
    'oct?'        : 'octagonal?',
    'oz'          : 'ounce',
    'p!'          : 'primorial',
    'pent'        : 'pentagonal',
    'pent?'       : 'pentagonal?',
    'poly'        : 'polygonal',
    'poly?'       : 'polygonal?',
    'prod'        : 'product',
    'pyr'         : 'pyramid',
    'quad'        : 'quadprime',
    'quad?'       : 'quadprime?',
    'quad_'       : 'quadprime_',
    'quint'       : 'quintprime',
    'quint?'      : 'quintprime?',
    'quint_'      : 'quintprime_',
    'rad'         : 'radians',
    'rand'        : 'random',
    'right'       : 'shiftright',
    'safe'        : 'safeprime',
    'safe?'       : 'safeprime?',
    'sext'        : 'sextprime',
    'sext?'       : 'sextprime?',
    'sext_'       : 'sextprime_',
    'sexy'        : 'sexyprime',
    'sexy3'       : 'sexytriplet',
    'sexy3?'      : 'sexytriplet?',
    'sexy3_'      : 'sexytriplet_',
    'sexy4'       : 'sexyquad',
    'sexy4?'      : 'sexyquad?',
    'sexy4_'      : 'sexyquad_',
    'sexy?'       : 'sexyprime?',
    'sexy_'       : 'sexyprime',
    'sophie'      : 'sophieprime',
    'sophie?'     : 'sophieprime?',
    'sqr'         : 'square',
    'sqrt'        : 'root2',
    'syl'         : 'sylvester',
    'tri'         : 'triangular',
    'tri?'        : 'triangular?',
    'triarea'     : 'trianglearea',
    'triplet'     : 'tripletprime',
    'triplet?'    : 'tripletprime?',
    'triplet_'    : 'tripletprime_',
    'twin'        : 'twinprime',
    'twin?'       : 'twinprime?',
    'twin_'       : 'twinprime_',
    'uint'        : 'uinteger',
    'zeroes'      : 'zero',
    '^'           : 'power',
    '~'           : 'not',
}


#//******************************************************************************
#//
#//  modifiers are operators that directly modify the argument stack instead of
#//  just returning a value.
#//
#//  '[' and ']' are special arguments that change global state in order to
#//  create list operands.
#//
#//******************************************************************************

modifiers = {
    'dup'       : [ duplicateTerm, 2,
'modifiers', 'duplicates a argument n k times',
'''
''',
'''
''' ],
    'flatten'   : [ flatten, 1,
'listOperators', 'flattens a nested lists in list n to a single level',
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


#//******************************************************************************
#//
#//  listOperators are operators that handle whether or not an argument is a
#//  list themselves (because they require a list argument).  Unlike regular
#//  operators, we don't want listOperators permutated over each list element,
#//  and if we do for auxillary arguments, these operator handlers will do that
#//  themselves.
#//
#//******************************************************************************

listOperators = {
    'append'        : [ appendLists, 2,
'listOperators', 'appends the second list on to the first list',
'''
''',
'''
''' ],
    'altsign'       : [ alternateSigns, 1,
'listOperators', 'alternates signs in the list by making every even element negative',
'''
''',
'''
''' ],
    'altsign2'      : [ alternateSigns2, 1,
'listOperators', 'alternates signs in the list by making every odd element negative',
'''
''',
'''
''' ],
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
    'base'      : [ interpretAsBase, 2,
'number_theory', 'interpret list elements as base k digits',
'''
''',
'''
''' ],
    'cf'        : [ convertFromContinuedFraction, 1,
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''' ],
    'count'     : [ countElements, 1,
'listOperators', 'counts the elements of list n',
'''
''',
'''
''' ],
    'convert'     : [ convertUnits, 0,
'conversion', 'perform unit conversion',
'''
This is a special operator that doesn't require an operand.  If there is no
numerical value, then rpn will assume a value of 1.
''',
'''
''' ],
    'diffs'      : [ getListDiffs, 1,
'listOperators', 'returns a list with the differences between successive elements of list n',
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
    'interleave'    : [ interleave, 2,
'listOperators', 'interleaves lists n and k into a single list',
'''
''',
'''
''' ],
    'intersection'  : [ makeIntersection, 2,
'listOperators', 'returns the intersection of two lists',
'''
''',
'''
''' ],
    'linearrecur'   : [ getNthLinearRecurrence, 3,
'arithmetic', 'calculates the nth value of a linear recurrence specified by a list of seeds and of factors'
'''
''',
'''
''' ],
    'max'       : [ max, 1,
'arithmetic', 'returns the largest value in list n',
'''
''',
'''
''' ],
    'maxindex'  : [ getIndexOfMax, 1,
'arithmetic', 'returns the index of largest value in list n',
'''
''',
'''
''' ],
    'mean'      : [ lambda n: fdiv( fsum( n ), len( n ) ), 1,
'arithmetic', 'calculates the mean of values in list n',
'''
''',
'''
''' ],
    'min'       : [ min, 1,
'arithmetic', 'returns the smallest value in list n',
'''
''',
'''
''' ],
    'minindex'  : [ getIndexOfMin, 1,
'arithmetic', 'returns the index of smallest value in list n',
'''
''',
'''
''' ],
    'nonzero'   : [ lambda n: [ index for index, e in enumerate( n ) if e != 0 ], 1,
'listOperators', 'returns the indices of elements of list n that are not zero',
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
    'polyval'   : [ evaluatePolynomial, 2,
'algebra', 'interpret the list as a polynomial and evaluate it for value k',
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
    'repunit'   : [ getNthBaseKRepunit, 2,
'algebra', 'returns the nth repunit in base k',
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
    'sort'      : [ sortAscending, 1,
'listOperators', 'sort the elements of list n numerically in ascending order',
'''
The 'sort' operator gets applied recursively, so all sublists will be sorted as
well.  I might have to reconsider that.
''',
'''
c:\>rpn [ rand rand rand ] sort
[ 0.782934612763, 0.956555810967, 0.97728726503 ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] sort
[ [ 10 ], [ 9 ], [ 8 ], [ 5, 6, 7 ], [ 4 ], [ 3 ], [ 1, 2 ], [ 0 ], [ -1 ] ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] flatten sort
[ -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'sortdesc'  : [ sortDescending, 1,
'listOperators', 'sorts the elements of list n numerically in descending order',
'''
The 'sortdesc' operator works exactly like the sort operator, sorting the list
(and all sublists), except in descending order.
''',
'''
c:\>rpn 1 70 6 range2 sortdesc
[ 67, 61, 55, 49, 43, 37, 31, 25, 19, 13, 7, 1 ]

c:\>rpn 1 20 range countdiv sortdesc
[ 6, 6, 6, 5, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1 ]
''' ],
    'stddev'    : [ getStandardDeviation, 1,
'arithmetic', 'calculates the standard deviation of values in list n',
'''
''',
'''
c:\>rpn 1 50 range countdiv stddev
2.14485430741
''' ],
    'sum'       : [ fsum, 1,
'arithmetic', 'calculates the sum of values in list n',
'''
''',
'''
''' ],
    'tounixtime'  : [ lambda i: datetime.datetime( *i ).timestamp( ), 1,
'conversion', 'converts from date-time list to Unix time (seconds since epoch)'
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
    'union'         : [ makeUnion, 2,
'listOperators', 'returns the union of two lists',
'''
''',
'''
''' ],
    'unique'    : [ getUniqueElements, 1,
'listOperators', 'replaces list n with a list of its unique elements',
'''
''',
'''
''' ],
    'unpack'      : [ unpackInteger, 2,
'number_theory', 'unpack an integer value into bit fields',
'''
''',
'''
''' ],
    'zero'    : [ lambda n: [ index for index, e in enumerate( n ) if e == 0 ], 1,
'listOperators', 'returns a list of the indices of elements in list n that are zero',
'''
''',
'''
''' ],
}


#//******************************************************************************
#//
#//  operators
#//
#//  Regular operators expect zero or more single values and if those arguments
#//  are lists, rpn will iterate calls to the operator handler for each element
#//  in the list.   Multiple lists for arguments are not permutated.  Instead,
#//  the operator handler is called for each element in the first list, along
#//  with the nth element of each other argument that is also a list.
#//
#//******************************************************************************

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
    'and'           : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x & y ), 2,
'logical', 'calculates the bitwise \'and\' of n and k',
'''
''',
'''
''' ],
    'apery'         : [ apery, 0,
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
''' ],
    'aperynum'      : [ getNthAperyNumber, 1,
'comnbinatorics', 'calculates the nth Apery number',
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
    'balanced'      : [ getNthBalancedPrime, 1,
'prime_numbers', 'calculate the first of the nth set of balanced primes',
'''
''',
'''
''' ],
    'balanced_'     : [ getNthBalancedPrimeList, 1,
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
    'catalan'       : [ lambda n: fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) ), 1,
'combinatorics', 'calculates nth Catalan number',
'''
''',
'''
''' ],
    'carol'         : [ lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1,
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
    'centeredcube'  : [ getNthCenteredCubeNumber, 1,
'polyhedral_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' ],
    'cdecagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 10 ), 1,
'polygonal_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''' ],
    'cdecagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 10 ), 1,
'polygonal_numbers', 'finds the index of the centered decagonal number of value n',
'''
'cdecagonal?' solves for the index of the equation used by 'cdecagonal' to
get the index i of the ith centered decagonal number that corresponds to the
value n.

If n is not a centered decagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'ceiling'       : [ ceil, 1,
'arithmetic', 'returns the next highest integer for n',
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
    'cheptagonal'   : [ lambda n: getCenteredPolygonalNumber( n, 7 ), 1,
'polygonal_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''' ],
    'cheptagonal?'  : [ lambda n: findCenteredPolygonalNumber( n, 7 ), 1,
'polygonal_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'cheptagonal?' solves for the index of the equation used by 'cheptagonal' to
get the index i of the ith centered heptagonal number that corresponds to the
value n.

If n is not a centered heptagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'chexagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 6 ), 1,
'polygonal_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''' ],
    'chexagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 6 ), 1,
'polygonal_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'chexagonal?' solves for the index of the equation used by 'chexagonal' to
get the index i of the ith centered hexagonal number that corresponds to the
value n.

If n is not a centered hexagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cnonagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 9 ), 1,
'polygonal_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''' ],
    'cnonagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 9 ), 1,
'polygonal_numbers', 'finds the index of the centered nonagonal number of value n',
'''
'cnonagonal?' solves for the index of the equation used by 'cnonagonal' to
get the index i of the ith centered nonagonal number that corresponds to the
value n.

If n is not a centered nonagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'coctagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 8 ), 1,
'polygonal_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''' ],
    'coctagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 8 ), 1,
'polygonal_numbers', 'finds the index of the centered octgonal number of value n',
'''
'coctagonal?' solves for the index of the equation used by 'coctagonal' to
get the index i of the ith centered octagonal number that corresponds to the
value n.

If n is not a centered octagonal number, the result will not be a whole
number.
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
    'countbits'     : [ getBitCount, 1,
'logical', 'returns the number of set bits in the value of n',
'''
''',
'''
''' ],
    'countdiv'      : [ getDivisorCount, 1,
'number_theory', 'returns a count of the divisors of n',
'''
The divcount operator factors the argument and then calculates number of divisors
from the list of prime factors.  'divisors count' calculates the same result, but
the 'divisors' operator can generate prohibitively large lists for numbers with a
lot of factors.
''',
'''
c:\>rpn 98280 divcount
128

c:\>rpn 1 20 range divcount
[ 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6 ]
''' ],
    'cousinprime'   : [ getNthCousinPrime, 1,
'prime_numbers', 'returns the nth cousin prime',
'''
''',
'''
''' ],
    'cpentagonal'   : [ lambda n: getCenteredPolygonalNumber( n, 5 ), 1,
'polygonal_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''' ],
    'cpentagonal?'  : [ lambda n: findCenteredPolygonalNumber( n, 5 ), 1,
'polygonal_numbers', 'finds the index of the centered pentagonal number of value n',
'''
'cpentagonal?' solves for the index of the equation used by 'cpentagonal' to
get the index i of the ith centered pentagonal number that corresponds to the
value n.

If n is not a centered pentagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cpolygonal'    : [ lambda n, k: getCenteredPolygonalNumber( n, k ), 2,
'polygonal_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''' ],
    'cpolygonal?'   : [ lambda n, k: findCenteredPolygonalNumber( n, k ), 2,
'polygonal_numbers', 'finds the index of the centered polygonal number of value n',
'''
'cpolygonal?' solves for the index of the equation used by 'cpolygonal' to
get the index i of the ith centered k-sided polygonal number that corresponds
to the value n.

If n is not a centered k-sided polygonal number, the result will not be a whole
number.
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
    'csquare'       : [ lambda n: getCenteredPolygonalNumber( n, 4 ), 1,
'polygonal_numbers', 'calculates the nth centered square number',
'''
''',
'''
''' ],
    'csquare?'       : [ lambda n: findCenteredPolygonalNumber( n, 4 ), 1,
'polygonal_numbers', 'finds the index of the centered square number of value n',
'''
'csquare?' solves for the index of the equation used by 'csquare' to get the
index i of the ith centered square number that corresponds to the value n.

If n is not a centered square number, the result will not be a whole number.
''',
'''
''' ],
    'ctriangular'   : [ lambda n: getCenteredPolygonalNumber( n, 3 ), 1,
'polygonal_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''' ],
    'ctriangular?'   : [ lambda n: findCenteredPolygonalNumber( n, 3 ), 1,
'polygonal_numbers', 'finds the index of the centered triangular number of value n',
'''
'ctriangular?' solves for the index of the equation used by 'ctriangular' to
get the index i of the ith centered triangular number that corresponds to the
value n.

If n is not a centered triangular number, the result will not be a whole
number.
''',
'''
''' ],
    'cube'          : [ lambda n: power( n, 3 ), 1,
'powers_and_roots', 'calculates the cube of n',
'''
'cube' simply returns the value of n to the third power.
''',
'''
''' ],
    'decagonal'     : [ lambda n: getNthPolygonalNumber( n, 10 ), 1,
'polygonal_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''' ],
    'decagonal?'    : [ lambda n: findNthPolygonalNumber( n, 10 ), 1,
'polygonal_numbers', 'finds the index of the decagonal number of value n',
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
'combinatorics', 'calculates the nth Delannoy number',
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
    'divisors'      : [ getDivisors, 1,
'number_theory', 'returns a list of divisors of n',
'''
''',
'''
''' ],
    'dodecahedral'  : [ lambda n : polyval( [ 9/2, -9/2, 1, 0 ], n ), 1,
'polyhedral_numbers', 'returns the nth dodecahedral number',
'''
''',
'''
''' ],
    'doublebal'     : [ getNthDoubleBalancedPrime, 1,
'prime_numbers', 'returns the nth set of double balanced primes',
'''
''',
'''
''' ],
    'doublebal_'    : [ getNthDoubleBalancedPrimeList, 1,
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
    'element'       : [ getListElement, 2,
'listOperators', 'return a single element from a list',
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
    'exp10'         : [ lambda n: power( 10, n ), 1,
'powers_and_roots', 'calculates nth power of 10',
'''
''',
'''
''' ],
    'expphi'        : [ lambda n: power( phi, n ), 1,
'powers_and_roots', 'calculates the nth power of phi',
'''
expphi simply takes phi (the Golden Ratio) to the power of the argument n.

It was originally added to make testing the base phi output easier.
''',
'''
c:\>rpn 2 expphi
2.61803398875

c:\>rpn 3 expphi 2 expphi -
1.61803398875
''' ],
    'factor'        : [ lambda i: getExpandedFactorList( factor( i ) ), 1,
'number_theory', 'calculates the prime factorization of n',
'''
''',
'''
''' ],
    'factorial'     : [ fac, 1,
'number_theory', 'calculates the prime factorization of n',
'''
'factorial' calculates the product of all whole numbers from 1 to n.
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
    'fraction'      : [ interpretAsFraction, 2,
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''' ],
    'fromunixtime'  : [ lambda n: [ time.localtime( n ).tm_year, time.localtime( n ).tm_mon,
                                    time.localtime( n ).tm_mday, time.localtime( n ).tm_hour,
                                    time.localtime( n ).tm_min, time.localtime( n ).tm_sec ], 1,
'conversion', 'converts Unix time (seconds since epoch) to a date-time format'
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
    'georange'      : [ expandGeometricRange, 3,
'listOperators', 'generates a list of geometric progression of numbers',
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
    'heptagonal'    : [ lambda n: getNthPolygonalNumber( n, 7 ), 1,
'polygonal_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''' ],
    'heptagonal?'   : [ lambda n: findNthPolygonalNumber( n, 7 ), 1,
'polygonal_numbers', 'finds the index of the heptagonal number of value n',
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
    'heptsquare'    : [ getNthHeptagonalSquareNumber, 1,
'polygonal_numbers', 'calculates the nth heptagonal square number',
'''
''',
'''
''' ],
    'hepttri'       : [ getNthHeptagonalTriangularNumber, 1,
'polygonal_numbers', 'calculates the nth heptagonal triangular number',
'''
''',
'''
''' ],
    'hexagonal'     : [ lambda n: getNthPolygonalNumber( n, 6 ), 1,
'polygonal_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''' ],
    'hexagonal?'    : [ lambda n: findNthPolygonalNumber( n, 6 ), 1,
'polygonal_numbers', 'finds the index of the hexagonal number of value n',
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
    'icosahedral'   : [ lambda n: polyval( [ 5/2, -5/2, 1, 0 ], n ), 1,
'polyhedral_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''' ],
    'integer'       : [ convertToSignedInt, 2,
'conversion', 'convert the value to an signed ik-bit nteger',
'''
''',
'''
''' ],
    'isdivisible'   : [ lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2,
'arithmetic', 'is n divisible by k?',
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
'arithmetic', 'is n a perfect square?',
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
    'jacobsthal'      : [ getNthJacobsthalNumber, 1,
'number_theory', 'returns nth number of the Jacobsthal sequence',
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
'logarithms', '',
'''
''',
'''
''' ],
    'kynea'         : [ lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1,
'number_theory', 'gets the nth Kynea number',
'''
''',
'''
''' ],
    'leyland'       : [ lambda x, y : fadd( power( x, y ), power( y, x ) ), 2,
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
    'log2'          : [ lambda n: log( n, 2 ), 1,
'logarithms', 'calculates the base-2 logarithm of n',
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
    'makecf'        : [ lambda n, k: ContinuedFraction( n, maxterms=k, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2,
'number_theory', 'calculates k terms of the continued fraction representation of n',
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
'combinatorics', 'calculates the nth Motzkin number',
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
    'nonagonal'     : [ lambda n: getNthPolygonalNumber( n, 9 ), 1,
'polygonal_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''' ],
    'nonagonal?'    : [ lambda n: findNthPolygonalNumber( n, 9 ), 1,
'polygonal_numbers', 'finds the index of the nonagonal number of value n',
'''
''',
'''
''' ],
    'nonahept'      : [ getNthNonagonalHeptagonalNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and heptagonal.
''',
'''
''' ],
    'nonahex'       : [ getNthNonagonalHexagonalNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and hexagonal.
''',
'''
''' ],
    'nonaoct'       : [ getNthNonagonalOctagonalNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and octagonal.
''',
'''
''' ],
    'nonapent'      : [ getNthNonagonalPentagonalNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and pentgonal.
''',
'''
''' ],
    'nonasquare'    : [ getNthNonagonalSquareNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal square number',
'''
'nonasquare' calculates the nth number that is both nonagonal and square.
''',
'''
''' ],
    'nonatri'       : [ getNthNonagonalTriangularNumber, 1,
'polygonal_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonatri' calculates the nth number that is both nonagonal and triangular.
''',
'''
''' ],
    'not'           : [ getInvertedBits, 1,
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
    'nspherearea'   : [ getHypersphereSurfaceArea, 2,
'trigonometry', 'calculate the surface area of a k-sphere of radius n',
'''
''',
'''
''' ],
    'nspherevolume' : [ getHypersphereVolume, 2,
'trigonometry', 'calculate the volume of a k-sphere of radius n',
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
    'octagonal'     : [ lambda n: getNthPolygonalNumber( n, 8 ), 1,
'polygonal_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''' ],
    'octagonal?'    : [ lambda n: findNthPolygonalNumber( n, 8 ), 1,
'polygonal_numbers', 'finds the index of the octagonal number of value n',
'''
''',
'''
''' ],
    'octahedral'    : [ lambda n: polyval( [ 2/3, 0, 1/3, 0 ], n ), 1,
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
    'octsquare'     : [ getNthOctagonalSquareNumber, 1,
'polygonal_numbers', 'calculates the nth octagonal square number',
'''
''',
'''
''' ],
    'octtri'       : [ getNthOctagonalTriangularNumber, 1,
'polygonal_numbers', 'calculates the nth octagonal triangular number',
'''
''',
'''
''' ],
    'oeis'          : [ lambda n: downloadOEISSequence( int( n ) ), 1,
'special', 'downloads the OEIS integer series n',
'''
''',
'''
''' ],
    'oeiscomment'   : [ lambda n: downloadOEISText( int( n ), 'C', True ), 1,
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisex'        : [ lambda n: downloadOEISText( int( n ), 'E', True ), 1,
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisname'      : [ lambda n: downloadOEISText( int( n ), 'N', True ), 1,
'special', 'downloads the name of the OEIS integer series n',
'''
''',
'''
''' ],
    'omega'         : [ lambda: lambertw( 1 ), 0,
'constants', 'return the Omega constant',
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
    'padovan'       : [ getNthPadovanNumber, 1,
'number_theory', 'calculates the the nth Padovan number',
'''
''',
'''
''' ],
    'parity'        : [ lambda n : getBitCount( n ) & 1, 1,
'logical', 'returns the bit parity of n (0 == even, 1 == odd)',
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
    'pell'          : [ getNthPellNumber, 1,
'combinatorics', 'calculates the nth Pell number',
'''
''',
'''
''' ],
    'pentagonal'    : [ lambda n: getNthPolygonalNumber( n, 5 ), 1,
'polygonal_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''' ],
    'pentagonal?'   : [ lambda n: findNthPolygonalNumber( n, 5 ), 1,
'polygonal_numbers', 'finds the index of the pentagonal number of value n',
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
    'polyarea'   : [ getRegularPolygonArea, 1,
'trigonometry', 'calculates the area of an regular n-sided polygon with sides of unit length',
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
    'polygonal'     : [ getNthPolygonalNumber, 2,
'number_theory', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' ],
    'polygonal?'     : [ findNthPolygonalNumber, 2,
'number_theory', 'finds the index of the polygonal number with k sides of value n',
'''
''',
'''
''' ],
    'polylog'       : [ polylog, 2,
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
    'primepi'       : [ getPrimePi, 1,
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''
''',
'''
''' ],
    'primes'        : [ getPrimes, 2,
'prime_numbers', 'generates a range of primes from index n to index k',
'''
This function is identical to 'n k range prime', but is much more efficient
given the way calculating prime numbers is currently done.
''',
'''
''' ],
    'prime?'        : [ lambda n: findPrime( n )[ 1 ], 1,
'prime_numbers', 'find the index of the closest prime at n or above',
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
    'pyramid'       : [ lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1,
'polyhedral_numbers', 'calculates the nth square pyramidal number',
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
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quadprime_'    : [ getNthQuadrupletPrimeList, 1,
'prime_numbers', 'returns the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quintprime'    : [ getNthQuintupletPrime, 1,
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'quintprime_'   : [ getNthQuintupletPrimeList, 1,
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
    'range'         : [ expandRange, 2,
'listOperators', 'generates a list of successive integers from n to k',
'''
''',
'''
''' ],
    'range2'        : [ expandSteppedRange, 3,
'listOperators', 'generates a list of arithmetic progression of numbers',
'''
''',
'''
''' ],
    'reciprocal'    : [ lambda n : fdiv( 1, n ), 1,
'arithmetic', 'returns the reciprocal of n',
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
This operator is the equivalent of 'n 2 root'.
''',
'''
''' ],
    'root3'         : [ cbrt, 1,
'powers_and_roots', 'calculates the cube root of n',
'''
This operator is the equivalent of 'n 3 root'.
''',
'''
''' ],
    'round'         : [ lambda n: floor( fadd( n, 0.5 ) ), 1,
'arithmetic', 'rounds n to the nearest integer',
'''
''',
'''
''' ],
    'safeprime'     : [ lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1,
'prime_numbers', 'returns the nth safe prime',
'''
''',
'''
''' ],
    'schroeder'     : [ getNthSchroederNumber, 1,
'combinatorics', 'calculates the nth Schroeder number',
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
    'sextprime'     : [ getNthSextupletPrime, 1,
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sextprime_'    : [ getNthSextupletPrimeList, 1,
'prime_numbers', 'returns the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sexyprime'     : [ getNthSexyPrime, 1,
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexyprime_'    : [ getNthSexyPrimeList, 1,
'prime_numbers', 'returns the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexytriplet'   : [ getNthSexyTriplet, 1,
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexytriplet_'  : [ getNthSexyTripletList, 1,
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexyquad'     : [ getNthSexyQuadruplet, 1,
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'sexyquad_'     : [ getNthSexyQuadrupletList, 1,
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
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
    'shiftleft'     : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2,
'logical', 'performs a bitwise left shift of value n by k bits',
'''
''',
'''
''' ],
    'shiftright'    : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2,
'logical', 'performs a bitwise right shift of value n by k bits',
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
    'squaretri'     : [ getNthSquareTriangularNumber, 1,
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
    'sylvester'     : [ getNthSylvester, 1,
'combinatorics', 'calculates the nth Sylvester number',
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
    'tetrate'       : [ tetrate, 2,
'powers_and_roots', 'tetrates n by k',
'''
''',
'''
''' ],
    'tetrahedral'   : [ lambda n: polyval( [ 1/6, 1/2, 1/3, 0 ], n ), 1,
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
    'trianglearea'  : [ getTriangleArea, 3,
'trigonometry', 'calculates the area of a triangle with sides of length a, b, and c'
'''
''',
'''
''' ],
    'triangular'    : [ lambda n : getNthPolygonalNumber( n, 3 ), 1,
'polygonal_numbers', 'calcuates the nth triangular number',
'''
''',
'''
''' ],
    'triangular?'   : [ lambda n : findNthPolygonalNumber( n, 3 ), 1,
'polygonal_numbers', 'finds the index of the triangular number of value n',
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
    'triplebal'     : [ getNthTripleBalancedPrime, 1,
'prime_numbers', 'returns the first of the nth set of triple balanced primes',
'''
''',
'''
''' ],
    'triplebal_'    : [ getNthTripleBalancedPrimeList, 1,
'prime_numbers', 'returns the nth set of triple balanced primes',
'''
''',
'''
''' ],
    'tripletprime'  : [ getNthTripletPrime, 1,
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
''',
'''
''' ],
    'tripletprime'  : [ getNthTripletPrimeList, 1,
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
'prime_numbers', 'returns the first of the nth set of twin primes',
'''
''',
'''
''' ],
    'twinprime_'    : [ getNthTwinPrimeList, 1,
'prime_numbers', 'returns the nth set of twin primes',
'''
''',
'''
''' ],
    'uinteger'      : [ lambda n, k: int( fmod( n, power( 2, k ) ) ), 2,
'conversion', 'convert the value to an unsigned k-bit integer',
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
    'fromunixtime'  : [ lambda n: [ time.localtime( n ).tm_year, time.localtime( n ).tm_mon,
                                    time.localtime( n ).tm_mday, time.localtime( n ).tm_hour,
                                    time.localtime( n ).tm_min, time.localtime( n ).tm_sec ], 1,
'conversion', 'converts Unix time (seconds since epoch) to a date-time format'
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
    '_dumpops'      : [ dumpOperators, 0,
'internal', 'lists all rpn operators',
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
    '_dumpops'      : [ dumpOperators, 0,
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

    # ignore commas
    term = ''.join( [ i for i in term if i not in ',' ] )

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

    lastDigit = int( mantissa[ accuracy - 1 ] )
    extraDigit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extraDigit >= 5:
        result += str( lastDigit + 1 )
    else:
        result += str( lastDigit )

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
    # filter out text strings
    for c in output:
        if c in '+-.':
            continue

        if c in string.whitespace or c in string.punctuation:
            return output

    # filter out scientific notation, rpn doesn't grok that yet
    if ( output.find( 'e+' ) != -1 ) or ( output.find( 'e-' ) != -1 ):
        return output

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
        #strOutput = nstr( output, outputAccuracy  )[ 1 : -2 ]     # nstr seems to add quotes
        strOutput = str( output )

    if '.' in strOutput:
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
#//  printParagraph
#//
#//******************************************************************************

def printParagraph( text, length = 79, indent = 0 ):
    lines = textwrap.wrap( text, length )

    for line in lines:
        print( ' ' * indent + line )


#//******************************************************************************
#//
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( basicCategories, operatorCategories ):
    print( )
    print( PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )
    printParagraph(
'''For help on a specific topic, add a help topic, operator category or a specific operator name.  Adding
'example', or 'ex' after an operator name will result in examples of using being printed as well.''' )
    print( )
    print( 'The following is a list of general topics:' )
    print( )

    printParagraph( ', '.join( sorted( basicCategories ) ), 75, 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( operatorCategories ) ), 75, 4 )


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
        print( 'alias:  ' + aliasList[ 0 ] )

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
            operatorList[ index ] += ' (' + ', '.join( aliasList ) + ')'


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
command-line options:

    -a [n], --output_accuracy [n]
        maximum number of decimal places to display, irrespective of internal
        precision (default: ''' + str( defaultAccuracy ) + ')' + '''

    -b n : --input_radix n
        specify the radix for input (default: ''' + str( defaultInputRadix ) + ')' + '''

    -c, --comma -
        add commas to result, e.g., 1,234,567.0

    -d [n], --decimal_grouping [n] -
        display decimal places separated into groups (default: ''' + str( defaultDecimalGrouping ) + ')' + '''

    -h, --help -
        displays basic help information

    -i [n], --integer_grouping [n]
        display integer separated into groups (default: ''' + str( defaultIntegerGrouping ) + ')' + '''

    -n str, --numerals str
        characters set to use as numerals for output

    -o, --octal
        octal mode: equivalent to \'-r8 -w9 -i3 -z\'

    -p n, --precision n
        precision, i.e., number of significant digits to use

    -r n, --output_radix n
        output in a different base (2 to 62, or phi)

    -R n, --output_radix_numerals n
        output each digit is a space-delimited base-10 number

    -t, --time
        display calculation time

    -u, --find_poly
        find a polynomial such that P(x) ~= 0 of degree <= N (default: 1000)

    -w [n], --bitwise_group_size [n]
        bitwise operations group values by this size (default: ''' + str( defaultBitwiseGroupSize ) + ')' + '''

    -x, --hex
        hex mode: equivalent to '-r16 -w16 -i4 -z'

    -y, --identify
        identify the result (may repeat input)

    -z, --leading_zero
        add leading zeros if needed with -i

    -!, --print_options
        print values for all options
''',
'arguments' :
'''
Arguments:

    As its name implies, rpn uses Reverse Polish Notation, otherwise referred
    to as postfix notation.  The operand(s) come first and then the operator.
    This notation works without the need for parentheses.  rpn supports
    brackets for creating lists of operands, but this serves a different
    purpose and is described later.

    Some simple examples:

    2 + 2:
        rpn 2 2 +

    3 sqrt(2) / 4:
        rpn 3 2 sqrt * 4 /

    Lists are specified using the bracket operators.
    Most operators can take lists as operands, which results in the operation
    being performed on each item in the list.  If the operator takes two
    operands, then either operand can be a list.  If one operand is a list
    and the other is a single value, then each value in the list will have
    the single operand applied to it with the operator, and the result will
    be displayed as a list.

    It is possible in certain cases to nest lists.  rpn tries to figure out
    a logical way (and unequivocal) to apply the operators to the operands.

    *** Special note:  I have not exhaustively tested every possible
    scenario with lists, but in general, if it makes sense, rpn will work
    correctly.

    For example:

    c:\>rpn [ 2 3 4 5 6 ] 10 +
    [ 12, 13, 14, 15, 16, 17 ]

    c:\>rpn 7 [ 1 2 3 4 5 6 7 ] *
    [ 7, 14, 21, 28, 35, 42, 49 ]

    If both operands are lists, then each element from the first list is
    applied to the corresponding element in the second list.  If one list
    is shorter than the other, then only that many elements will have the
    operator applied and the resulting list will only be as long as the
    shorter list.

    For example:

    rpn [ 1 2 3 4 5 6 7 ] [ 1 2 3 4 5 6 7 ] **
    [ 1, 4, 27, 256, 3125, 46656, 823543 ]

    rpn [ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *
    [ 30, 40, 90, 160 ]

    Some operators take lists as operands 'natively'.  This means the
    operator requires a list, because the operation does not make sense for
    a single value.  For example, 'mean' averages the values of a list.  If
    the required list argument is a single value, rpn will promote it to a
    list.

    For example:

    c:\>rpn [ 1 2 3 ] [ 4 5 6 ] polyval
    [ 27, 38, 51 ]
''',
'input' :
'''
    For integers, rpn understands hexidecimal input of the form '0x....'.
    Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B'
    is interpreted as binary.  Decimal points are not allowed for binary,
    octal or hexadecimal modes, but fractional numbers in another base can be
    input using -b.

    A leading '\\' forces the term to be a number rather than an operator (for
    use with higher bases with -b).
''',
'output' :
'''
    [ description of output formats supported by rpn ]
''',
'conversion' :
'''
    [ describe unit conversions in rpn ]
''',
'about' :
PROGRAM_NAME + ' ' + RPN_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE +
'''

rpn is a command-line Reverse-Polish Notation calculator that was first written in C in 1988.
It was rewritten in Python 3 in 2012 and now uses the mpmath library.
''',
'bugs' :
'''
    rpn doesn't describe the correct argument in error messages if an option
    flag is used.

    -u doesn't work with complex numbers
''',
'license' :
'''
rpn is licensed under the GPL, version 3.0 and is ''' + '\n' + COPYRIGHT_MESSAGE + '''

    [ fill in extra boilerplate as needed ]
''',
'examples' :
'''
Here are some examples of using rpn:

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

    c:\>rpn -p20 [ 1 2 30 dup ] cf
    1.41421356237309504880

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        rpn 1 50 range fib isprime nonzero 1 + fib

    Which of the first thousand pentagonal numbers are also triangular:
        c:\>rpn 1000 pent tri?
        1731.26218055

        c:\>rpn 1 1000 range pent 1 1732 range tri intersection

Please note that several of the following commands are broken up into multiple
lines for readability, but all of them are single commands to rpn.

In some commands, the precision is explicitly set such to limit the output to
what is accurately calculated.   If no precision options are used then the
calculation will be correct regardless of precision.

Calculation (or approximation) of various mathematical constants:

    Polya Random Walk Constant
        = rpn -p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 /
                    gamma 7 24 / gamma 11 24 / gamma ] prod 1/x * -

    Schwartzchild Constant (Conic Constant)
        = rpn -p20 2 0 30 range ** 0 30 range ! / sum
        = rpn e 2 **

    Somos\' Quadratic Recurrence Constant
        = rpn -p20 1 100 range 0.5 0.5 100 georange ** prod

    Prevost Constant
        = rpn -p20 1 100 range fib 1/x sum

    Euler's number = rpn -p20 0 100 range fac 1/x sum
                   = rpn e

    Gelfond Constant
        = rpn -p20 pi 0 100 range power 0 100 range ! / sum
        = rpn e pi power

    Bloch-Landau Constant
        = rpn -p20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /

    Hausdorff Dimension
        = rpn -p20 2 0 100 range 2 * 1 + power 0 100 range 2 * 1 + *
            1/x sum 3 0 100 range 2 * 1 + power 0 100 range 2 * 1 +
            * 1/x sum /
        = rpn 3 log 2 log /

    Machin-Gregory Series
        = rpn -p20 1 1000 2 range2 2 1 1000 2 range2 power * 1/x altsum
        = rpn 1 2 / atan

    Beta(3)
        = rpn -p17 1 1000000 2 range2 3 power 1/x altsum
        = rpn pi 3 power 32 /

    Cahen's constant
        = rpn -p20 1 20 range sylvester 1 - 1/x altsum

    Lemniscate Constant
        = rpn 4 2 pi / sqrt * 0.25 ! sqr *

    sqrt( e )
        = rpn -p20 2 0 20 range power [ 0 20 range ] ! * 1/x sum
        = rpn -p20 0 20 range 2 * !! 1/x sum
        = rpn -p20 e sqrt

    1/e
        = rpn -p20 0 25 range fac 1/x altsum
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
        = rpn -a6 1 1 100000 primes 3 * 2 - 1 100000 primes 3 power / - prod
        = rpn -a7 6 pi sqr / 1 2
                1 100000 primes 1 100000 primes 1 + * 1/x * - prod *

    Ramanujan-Forsythe Constant
        = rpn 0 100000 range 2 * 3 - fac2 0 100000 range 2 * fac2 / sqr sum

    Apery's Constant
        = rpn -p20 1 5000 range 3 power 1/x sum
        = rpn -p20 3 zeta
        = rpn -p20 apery

    Omega Constant
        = rpn -p20 [ e 1/x 100 dup ] tower
        = rpn -p20 omega

    Liouville Number
        = rpn -p120 10 1 10 range ! power 1/x surpnm

    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                0 100000 range 3 * 2 + sqr 1/x sum -
                1 100000 range 3 * 1 + sqr 1/x sum + *

    Hafner-Sarnak-McCurley Constant (2)
        = rpn -a7 1 1 100000 primes sqr 1/x - prod
        = rpn 2 zeta 1/x

    Infinite Tetration of i
        = rpn -p20 [ 1 i 1000 dup ] tower
''',
'notes' :
'''
When converting fractional output to other bases, rpn adjusts the precision
to the approximate equivalent for the new base since the precision is
applicable to base 10.

Tetration (hyperexponentiation) forces the second argument to an integer.

To compute the nth Fibonacci number accurately, rpn sets the precision to
a level sufficient to guarantee a correct answer.

Bitwise operators force all arguments to integers by truncation if necessary.
'''
}

    operatorCategories = set( operators[ key ][ 2 ] for key in operators )
    operatorCategories.update( set( listOperators[ key ][ 2 ] for key in listOperators ) )
    operatorCategories.update( set( modifiers[ key ][ 2 ] for key in modifiers ) )

    if len( helpArgs ) == 0:
        printGeneralHelp( basicCategories, operatorCategories )
        return

    term = helpArgs[ 0 ]

    if term in operatorAliases:
        term = operatorAliases[ term ]

    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ] )

    if term in listOperators:
        printOperatorHelp( helpArgs, term, listOperators[ term ] )

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
        operatorList.extend( [ key for key in listOperators if listOperators[ key ][ 2 ] == term ] )
        operatorList.extend( [ key for key in modifiers if modifiers[ key ][ 2 ] == term ] )

        addAliases( operatorList )

        printParagraph( ', '.join( sorted( operatorList ) ), 75, 4 )


#//******************************************************************************
#//
#//  validateOptions
#//
#//******************************************************************************

def validateOptions( args ):
    if args.hex:
        if args.output_radix != 10 and args.output_radix != 16:
            return False, '-r and -x can\'t be used together'

        if args.octal:
            return False, '-x and -o can\'t be used together'

    if args.octal:
        if args.output_radix != 10 and args.output_radix != 8:
            return False, '-r and -o can\'t be used together'

    if args.output_radix_numerals > 0:
        if args.hex:
            return False, '-R and -x can\'t be used together'

        if args.octal:
            return False, '-R and -o can\'t be used together'

        if args.output_radix != 10:
            return False, '-R and -r can\'t be used together'

        if args.output_radix_numerals < 2:
            return False, 'output radix must be greater than 1'

    if args.comma and args.integer_grouping > 0 :
        return False, 'rpn:  -c can\'t be used with -i'

    if args.output_radix_numerals > 0 and \
       ( args.comma or args.decimal_grouping > 0 or args.integer_grouping > 0 ):
        return False, '-c, -d and -i can\'t be used with -R'

    return True, ''


#//******************************************************************************
#//
#//  validateArguments
#//
#//******************************************************************************

def validateArguments( terms ):
    bracketCount = 0

    for term in terms:
        if term == '[':
            bracketCount += 1
        elif term == ']':
            bracketCount -= 1

    if bracketCount:
        print( 'rpn:  mismatched brackets (count: {})'.format( bracketCount ) )
        return False

    return True


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
    global unitOperators
    global unitTypes
    global unitConversionMatrix

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
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=-1,
                         const=defaultAccuracy )
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
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store',
                         default=defaultBitwiseGroupSize )
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

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
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

    # handle -n
    numerals = args.numerals

    # handle -b
    inputRadix = int( args.input_radix )

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return

    # handle -x
    if args.hex:
        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        bitwiseGroupSize = 9

    # handle -R
    if args.output_radix_numerals > 0:
        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( 'rpn:  output radix must be from 2 to 62, or phi' )
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

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            unitTypes = pickle.load( pickleFile )
            unitOperators = pickle.load( pickleFile )
            unitConversionMatrix = pickle.load( pickleFile )
            operatorAliases.update( pickle.load( pickleFile ) )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit conversion matrix data.  Unit conversion will be unavailable.' )

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
        elif term in unitOperators:
            unitStack.append( UnitOfMeasurement( term ) )
        elif term in operators:
            argsNeeded = operators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    result = callers[ 0 ]( operators[ term ][ 0 ], None )
                else:
                    argList = list( )

                    for i in range( 0, argsNeeded ):
                        arg = currentValueList.pop( )
                        argList.append( arg if isinstance( arg, list ) else [ arg ] )

                    result = callers[ argsNeeded ]( operators[ term ][ 0 ], *argList )

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            #except ValueError as error:
            #    print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
            #except TypeError as error:
            #    print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
        elif term in listOperators:
            argsNeeded = listOperators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term + ' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    currentValueList.append( listOperators[ term ][ 0 ]( currentValueList ) )
                elif argsNeeded == 1:
                    currentValueList.append( evaluateOneListFunction( listOperators[ term ][ 0 ], currentValueList.pop( ) ) )
                else:
                    listArgs = [ ]

                    for i in range( 0, argsNeeded ):
                        listArgs.insert( 0, currentValueList.pop( ) )

                    currentValueList.append( listOperators[ term ][ 0 ]( *listArgs ) )
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
        if len( valueList ) > 1 or len( valueList ) == 0:
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

                    # I don't know if this would ever be useful to try.
                    #if formula is None:
                    #    base.extend( [ 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' ] )
                    #    formula = identify( result, base )
                    #
                    # Nor this.
                    #if formula is None:
                    #    base.extend( [ 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' ] )
                    #    formula = identify( result, base )

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

