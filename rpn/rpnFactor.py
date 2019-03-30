#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnFactor.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import collections
import contextlib
import fractions
import os
import pickle
import random

from mpmath import ceil, fabs, fdiv, floor, fmod, fneg, fprod, log, log10, mp, \
                   mpmathify, power

from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnPersistence import loadFactorCache
from rpn.rpnPrimes import primes
from rpn.rpnPrimeUtils import isPrimeNumber
from rpn.rpnSettings import setAccuracy
from rpn.rpnUtils import debugPrint, getExpandedFactorList, oneArgFunctionEvaluator, \
                         real, real_int

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getFactors
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getFactors( target ):
    if target < -1:
        result = [ -1 ]
        result.extend( getFactors( fneg( target ) ) )
        return result
    elif target == -1:
        return [ -1 ]
    elif target == 0:
        return [ 0 ]
    elif target == 1:
        return [ 1 ]

    n = int( floor( target ) )

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

    except ValueError as error:
        pass

    if g.useYAFU and n > g.minValueForYAFU:
        result = runYAFU( n )
    else:
        from rpn.factorise import factorise
        result = factorise( int( n ) )

    if n > g.minValueToCache:
        if g.ignoreCache or ( not g.ignoreCache and n not in g.factorCache ):
            debugPrint( '\ncaching factors of ', n, result )
            g.factorCache[ n ] = result

    return result


# //******************************************************************************
# //
# //  getFactorList
# //
# //******************************************************************************

def getFactorList( n ):
    return list( collections.Counter( getFactors( n ) ).items( ) )


# //******************************************************************************
# //
# //  factorByTrialDivision
# //
# //  This is sufficiently fast for small numbers... at least for now.
# //
# //******************************************************************************

def factorByTrialDivision( n ):
    if n > g.maxToFactorByTrialDivision:
        raise ValueError( 'value', n, 'is too big to factor by trial division' )

    result = [ ]

    for i in primes:
        while n > 1 and fmod( n, i ) == 0:
            n = fdiv( n, i )
            result.append( i )

        if isPrimeNumber( n ):
            break

    if n > 1:
        result.append( int( n ) )

    return result


# //******************************************************************************
# //
# //  runYAFU
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def runYAFU( n ):
    import subprocess

    full_out = subprocess.run( [ g.userConfiguration[ 'yafu_path' ] + os.sep +
                                 g.userConfiguration[ 'yafu_binary' ], str( int( n ) ), '-xover', '120' ],
                             stdout=subprocess.PIPE, cwd=g.userConfiguration[ 'yafu_path' ] ).stdout.decode( 'ascii' )

    #print( 'out', full_out )

    out = full_out[ full_out.find( '***factors found***' ) : ]

    if len( out ) < 2:
        if log10( n ) > 40:
            raise ValueError( 'yafu seems to have crashed trying to factor ' + str( int( n ) ) +
                              '.\n\nyafu output follows:\n' + full_out )
        else:
            debugPrint( 'yafu seems to have crashed, switching to built-in factoring code' )
            from rpn.factorise import factorise
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
        debugPrint( '\nyafu has barfed' )
        for i in result:
            n = fdiv( n, i )

        result.extend( runYAFU( n ) )

    return sorted( result )

