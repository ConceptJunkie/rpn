#!/usr/bin/env python

#******************************************************************************
#
#  rpnFactor.py
#
#  rpnChilada factoring utilities
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import collections
import os
import subprocess

from mpmath import fadd, fdiv, floor, fmod, fneg, fprod, log10, mpmathify

from rpn.math.factorise import factorise
from rpn.math.rpnPrimeUtils import isPrime
from rpn.math.rpnPrimes import primes

from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnPersistence import loadFactorCache
from rpn.util.rpnSettings import setAccuracy
from rpn.util.rpnUtils import oneArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, IntValidator

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  getFactors
#
#******************************************************************************

def getFactors( target ):
    if target < -1:
        result = [ -1 ]
        result.extend( getFactors( fneg( target ) ) )
        return result

    if target == -1:
        return [ -1 ]

    if target == 0:
        return [ 0 ]

    if target == 1:
        return [ 1 ]

    n = int( floor( target ) )

    setAccuracy( floor( fadd( log10( n ), 2 ) ) )

    if g.factorCache is None:
        loadFactorCache( )

    if not g.ignoreCache:
        if n in g.factorCache:
            if g.verbose and n != 1:
                print( 'cache hit:', n )
                print( )

            debugPrint( '\nfactor cache', n, g.factorCache[ n ] )

            return g.factorCache[ n ]

    try:
        result = factorByTrialDivision( n )   # throws if n is too big

        if n > g.minValueToCache and n not in g.factorCache:
            g.factorCache[ n ] = result

        return result
    except ValueError:
        pass

    if g.useYAFU and n > g.minValueForYAFU:
        result = runYAFU( n )
    else:
        result = factorise( int( n ) )

    if n > g.minValueToCache:
        if g.ignoreCache or ( not g.ignoreCache and n not in g.factorCache ):
            debugPrint( '\ncaching factors of ', n, result )
            g.factorCache[ n ] = result

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getFactorsOperator( n ):
    return getFactors( n )


#******************************************************************************
#
#  getFactorList
#
#******************************************************************************

def getFactorList( n ):
    return list( collections.Counter( getFactors( n ) ).items( ) )


#******************************************************************************
#
#  factorByTrialDivision
#
#  This is sufficiently fast for small numbers... at least for now.
#
#******************************************************************************

def factorByTrialDivision( n ):
    if n > g.maxToFactorByTrialDivision:
        raise ValueError( 'value', n, 'is too big to factor by trial division' )

    result = [ ]

    for i in primes:
        while n > 1 and fmod( n, i ) == 0:
            n = fdiv( n, i )
            result.append( i )

        if isPrime( n ):
            break

    if n > 1:
        result.append( int( n ) )

    return result


#******************************************************************************
#
#  runYAFU
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def runYAFU( n ):
    fullOut = subprocess.run( [ g.userConfiguration[ 'yafu_path' ] + os.sep +
                                g.userConfiguration[ 'yafu_binary' ], '-R', '-xover', '120' ],
                              input='factor(' + str( int( n ) ) + ')\n', encoding='ascii', stdout=subprocess.PIPE,
                              cwd=g.userConfiguration[ 'yafu_path' ], check=True ).stdout

    debugPrint( 'yafu output: ', fullOut )

    out = fullOut[ fullOut.find( '***factors found***' ) : ]

    if len( out ) < 2:
        if log10( n ) > 40:
            raise ValueError( 'yafu seems to have crashed trying to factor ' + str( int( n ) ) +
                              '.\n\nyafu output follows:\n' + fullOut )

        debugPrint( 'yafu seems to have crashed, switching to built-in factoring code' )
        return factorise( int( n ) )

    result = [ ]

    while True:
        prime = ''

        out = out[ out.find( 'P' ) : ]

        if len( out ) < 2:
            break

        out = out[ out.find( '=' ) : ]

        index = 2

        while out[ index ] >= '0' and out[ index ] <= '9':
            prime += out[ index ]
            index += 1

        result.append( mpmathify( prime ) )

    if not result:
        raise ValueError( 'yafu seems to have failed.' )

    answer = fprod( result )

    if answer != n:
        debugPrint( '\nyafu has failed, result:', result )

        for i in result:
            n = fdiv( n, i )

        result.extend( runYAFU( n ) )

    return sorted( result )
