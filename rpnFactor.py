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

from mpmath import ceil, fabs, fdiv, floor, fmod, fneg, fprod, log, log10, mp, power

import rpnGlobals as g

from rpnPersistence import loadFactorCache
from rpnPrimes import primes
from rpnPrimeUtils import isPrime
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
# //  getFactors
# //
# //******************************************************************************

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

    if n in g.factorCache:
        if g.verbose and n != 1:
            print( 'cache hit:', n )
            print( )

        return g.factorCache[ n ]

    try:
        result = factorByTrialDivision( n )   # throws if n is too big

        if n > g.minValueToCache and n not in g.factorCache:
            g.factorCache[ n ] = result

        return result

    except ValueError as error:
        pass

    verbose = g.verbose

    if verbose:
        print( '\nfactoring', n, '(', int( floor( log10( n ) ) ), ' digits)...' )

    from factorise import factorise
    result = factorise( int( n ) )

    if n > g.minValueToCache and n not in g.factorCache:
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
    if n > 10000000000:   # 100,000^2
        raise ValueError( 'value', n, 'is too big to factor by trial division' )

    result = [ ]

    for i in primes:
        while n > 1 and fmod( n, i ) == 0:
            n = fdiv( n, i )
            result.append( i )

        if isPrime( n ):
            break

    if n > 1:
        result.append( n )

    return result


