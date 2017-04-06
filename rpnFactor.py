#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnFactor.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
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

from mpmath import ceil, fabs, floor, fneg, fprod, log, log10, mp, power

import rpnGlobals as g

from rpnPersistence import loadFactorCache
from rpnPrimes import primes
from rpnSettings import setAccuracy
from rpnUtils import DelayedKeyboardInterrupt, getExpandedFactorList, \
                     getExpandedFactorListSympy, real, real_int


# //******************************************************************************
# //
# //  getFactorListSympy
# //
# //******************************************************************************

def getFactorListSympy( n ):
    # We shouldn't have to check for lists here, but something isn't right...
    if isinstance( n, list ):
        return [ getFactorListSympy( i ) for i in n ]

    from sympy.ntheory import factorint

    return getExpandedFactorListSympy( factorint( n ) )


# //******************************************************************************
# //
# //  getECMFactors
# //
# //******************************************************************************

def getECMFactors( target ):
    from pyecm import factors

    n = int( floor( target ) )

    verbose = g.verbose
    randomSigma = True
    asymptoticSpeed = 10
    processingPower = 1.0

    if n < -1:
        return [ -1 ] + getECMFactors( fneg( n ) )
    elif n == -1:
        return [ -1 ]
    elif n == 0:
        return [ 0 ]
    elif n == 1:
        return [ 1 ]

    if verbose:
        print( '\nfactoring', n, '(', int( floor( log10( n ) ) ), ' digits)...' )

    if g.factorCache is None:
        loadFactorCache( )

    if n in g.factorCache:
        if verbose and n != 1:
            print( 'cache hit:', n )
            print( )

        return g.factorCache[ n ]

    result = [ ]

    for factor in factors( n, verbose, randomSigma, asymptoticSpeed, processingPower ):
        result.append( factor )

    result = [ int( i ) for i in result ]

    largeFactors = list( collections.Counter( [ i for i in result if i > 65535 ] ).items( ) )
    product = int( fprod( [ power( i[ 0 ], i[ 1 ] ) for i in largeFactors ] ) )

    save = False

    if product not in g.factorCache:
        g.factorCache[ product ] = largeFactors
        save = True

    if n > g.minValueToCache and n not in g.factorCache:
        g.factorCache[ n ] = result

    if verbose:
        print( )

    return result


# //******************************************************************************
# //
# //  getSIQSFactors
# //
# //******************************************************************************

def getSIQSFactors( target ):
    if target < 1000000000000000000000:
        return getECMFactors( target )

    verbose = g.verbose

    n = int( floor( target ) )

    if verbose:
        print( '\nfactoring', n, '(', int( floor( log10( n ) ) ), ' digits)...' )

    if g.factorCache is None:
        loadFactorCache( )

    if n in g.factorCache:
        if verbose and n != 1:
            print( 'cache hit:', n )
            print( )

        return g.factorCache[ n ]

    from factorise import factorise
    result = factorise( int( n ) )

    if n > g.minValueToCache and n not in g.factorCache:
        g.factorCache[ n ] = result

    return result


# //******************************************************************************
# //
# //  getSIQSFactorList
# //
# //******************************************************************************

def getSIQSFactorList( n ):
    return list( collections.Counter( getSIQSFactors( n ) ).items( ) )


