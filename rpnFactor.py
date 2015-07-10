#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnFactor.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
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

from rpnDeclarations import *

from rpnUtils import setAccuracy
from rpnPrimes import primes
from rpnUtils import getExpandedFactorList

import rpnGlobals as g

from pyecm import factors


# //******************************************************************************
# //
# //  loadFactorCache
# //
# //******************************************************************************

def loadFactorCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'rb' ) ) as pickleFile:
            factorCache = pickle.load( pickleFile )
    except FileNotFoundError:
        factorCache = { }

    return factorCache


# //******************************************************************************
# //
# //  saveFactorCache
# //
# //******************************************************************************

def saveFactorCache( factorCache ):
    with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( factorCache, pickleFile )


# //******************************************************************************
# //
# //  getSmallFactors
# //
# //  This function factors out all small primes (i.e., the primes in the prime
# //  table in rpnPrimes.py).
# //
# //  The return values are the remaining value, and the factors already divided
# //  out.  The factors is a list of two-tuples, consisting of each prime factor
# //  and its exponent.
# //
# //******************************************************************************

def getSmallFactors( candidate, verbose = False ):
    remaining = candidate
    smallFactors = [ ]

    for prime in primes:
        exponent = 0
        modulus = remaining % prime

        if modulus == 0:
            while modulus == 0:
                exponent += 1
                remaining //= prime
                modulus = remaining % prime

            smallFactors.append( ( prime, exponent ) )

            if verbose:
                print( prime, 'is a prime factor of', candidate, ', exponent:', exponent )

    if verbose and remaining == candidate:
        print( 'getSmallFactors:  no small factors found!' )

    return remaining, smallFactors


# //******************************************************************************
# //
# //  doMillerTest
# //
# //  n is odd, > 1, and does not divide b, 0 < b < R0.
# //  if 1 is returned, then *Nptr passes Miller's test for base b.
# //  if 0 is returned, then *Nptr is composite.
# //
# //******************************************************************************

def doMillerTest( n, b ):
    i = 0
    j = 0

    D = n - 1
    A = D // 2

    while A % 2 == 0:
        i += 1
        A //= 2

    C = pow( b, A, n )

    if C == 1:
        return 1

    while True:
        if C == D:
            return 1

        j += 1

        if i < j:
            return 0

        C = ( C * C ) % n
        A *= 2


# //******************************************************************************
# //
# //  doQPrimeTest
# //
# //  n > 1 and not equal to PRIME[0],...,PRIME[4].
# //  if 1 is returned, then *Nptr passes Miller's test for bases PRIME[0],
# //  ...,PRIME[16] and is likely to be prime.
# //  if 0 is returned, then *Nptr is composite.
# //
# //******************************************************************************

def doQPrimeTest( n, verbose = False ):
    for i in range( 0, 17 ):
        if doMillerTest( n, primes[ i ] ) == 0:
            if verbose:
                print( 'Miller\'s Test finished:', n, 'is composite' )

            return 0

    if verbose:
        print( n, 'passed Miller\'s Test' )

    return 1


# //******************************************************************************
# //
# //  isPerfectPower
# //
# //  Here N > 1.
# //  Returns X if N = X^k, for some X, k > 1,  0 otherwise.
# //  See E. Bach and J. Sorenson, "Sieve algorithms for perfect power testing"
# //  Algorithmica 9 (1993) 313-328.
# //
# //******************************************************************************

def isPerfectPower( n, verbose = False ):
    if verbose:
        print( 'isPerfectPower...' )

    t = int.bit_length( n ) - 1

    i = 0

    while primes[ i ] <= t:
        X = n // primes[ i ]
        Y = x ** primes[ i ]

        if Y == N:
            if verbose:
                print( 'Yup!' )

            return X
        else:
            i += 1

    if verbose:
        print( 'Nope!' )

    return 0


# //******************************************************************************
# //
# //  getPollard
# //
# //  Pollard's p-1 method of factoring *Nptr.
# //
# //******************************************************************************

def getPollard( n, verbose = False ):
    b = 1
    PP = 1
    T = 2

    while b <= 2:
        b += 1

        if verbose:
            print( 'b =', b )

        i = 2

        while i <= 10000:
            if verbose and ( i % 100 ) == 0:
                print( 'i =', i )

            T = pow( T, i, n )

            TT = T - PP
            P = fractions.gcd( n, TT )

            if ( P != 1 ) and ( P < n ):
                if verbose:
                    print( P, 'is a proper factor of', n )

                return P

            if P == n:
                b += 1

                if verbose:
                    print( 'GCD = n; b increased to', b )

                T = b
                continue

            i += 1

    if verbose:
        print( 'no factors returned' )

    return 0


# //******************************************************************************
# //
# //  getBrentPollard
# //
# //  https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/
# //
# //******************************************************************************

def getBrentPollard( n ):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    y = random.randint( 1, n - 1 )
    c = random.randint( 1, n - 1 )
    m = random.randint( 1, n - 1 )
    g, r, q = 1, 1, 1

    while g == 1:
        x = y
        for i in range( r ):
            y = ( pow( y, 2, n ) + c ) % n

        k = 0

        while k < r and g == 1:
            ys = y
            for i in range( min( m, r - k ) ):
                y = ( pow( y, 2, n ) + c ) % n
                q = q * abs( x- y ) % n
            g = fractions.gcd( q, n )
            k += m
        r *= 2
    if g == n:
        while True:
            ys = ( pow( ys, 2, n ) + c ) % n
            g = fractions.gcd( abs( x - ys ), n )
            if g > 1:
                break

    return g


# //******************************************************************************
# //
# //  getLargeFactors
# //
# //  n > 1 is not divisible by the primes in rpnPrimes.py.
# //
# //  Since we've already checked against all the primes in the primes table,
# //  if n is smaller than the largest prime squared, we already know it's prime.
# //
# //******************************************************************************

def getLargeFactors( n, verbose = False ):
    if verbose:
        print( 'getLargeFactors', n )

    cutoff = primes[ -1 ] * primes[ -1 ]

    if ( n < cutoff ) or doQPrimeTest( n ):
        return n

    f = 1
    X = n

    while f:
        Y = getBrentPollard( X )

        if Y == 0:
            Y = isPerfectPower( X, verbose )

        if Y == 0:
            Y = MPQS1( X )

        if Y == 0:
            print( 'Switching to ECF:', ECMAX, 'elliptic curves' )
            Y = EFACTOR( X, 1279, 1 )

        if Y == 0:
            print( 'Switching to Pollard p-1' )
            Y = getPollard( X, verbose )

        if Y == 0:
            raise ValueError( 'getLargeFactors: no factor found' )

        X //= Y

        if X > Y:
            X = Y

        if X < cutoff:
            return X

        if doQPrimeTest( X, verbose ):
            f = 0

    return X


# //******************************************************************************
# //
# //  getPrimeFactors
# //
# //  A quasi-prime (q-prime) factor of *Nptr is > 1,000,000,
# //  is not divisible by PRIMES[0],...,PRIMES[167], passes Millers' test
# //  for bases PRIMES[0],...,PRIMES[10] and is hence likely to be prime.
# //
# //  PRIME_FACTORS returns the number of q-prime factors of n, stores
# //  them in the global array Q_PRIME[].
# //
# //  Any prime factors < 1000 of n and corresponding exponents are printed and
# //  placed in the arrays Q[ ] and K[ ], while any prime factors > 1000 and all
# //  q-prime factors and corresponding exponents of n are printed and placed in
# //  the arrays Q_[ ] and K_[ ].
# //
# //  Return values:
# //    smallFactors, largeFactors, qPrimes
# //
# //******************************************************************************

def getPrimeFactors( n, verbose = False ):
    cutoff = primes[ -1 ] * primes[ -1 ]

    smallFactors = [ ]
    largeFactors = [ ]
    qPrimes = [ ]

    if verbose:
        print( "Factoring", n, '...' )

    remaining, smallFactors = getSmallFactors( n, verbose )

    if remaining > 1 and not g.factorCache is None:
        if remaining in g.factorCache:
            if verbose:
                print( 'cache hit:', remaining )
            largeFactors.extend( g.factorCache[ remaining ] )
            remaining = 1

    while remaining > 1:
        exponent = 0
        P = getLargeFactors( remaining, verbose )

        while True:
            Z = remaining % P

            if Z != 0:
                break

            exponent += 1
            remaining //= P

        if verbose:
            if P < cutoff:
                print( P, 'is a prime factor of', n )

        if  fabs( P ) > fabs( cutoff ):
            if verbose:
                print( P, 'is a q-prime factor of', n )

            qPrimes.append( ( P, 1 ) )

        largeFactors.append( ( P, exponent ) )

        if verbose:
            print( ' exponent:', exponent )
            print( '--' )

    if verbose:
        print( 'factorization into primes and q-primes completed for', n )

    return smallFactors, largeFactors, qPrimes


# //******************************************************************************
# //
# //  doSelfridgeTest
# //
# //  Selfridges's test for primality - see "Prime Numbers and Computer
# //  Methods for Factorization" by H. Riesel, Theorem 4.4, p.106.
# //  n > 1 is a q-prime.
# //
# //  The prime and q-prime factors of n - 1 are first found. If no q-prime
# //  factor is present and 1 is returned, then n is prime.  However if at
# //  least one q-prime factor is present and 1 is returned, then n retains its
# //  q-prime status.  If 0 is returned, then n is either composite or likely
# //  to be composite.
# //
# //******************************************************************************

def doSelfridgeTest( candidate, verbose = False ):
    n_minus_1 = candidate - 1

    if verbose:
        print( 'Selfridge\'s exponent test in progress for', candidate )

    smallFactors, largeFactors, qPrimes = getPrimeFactors( n_minus_1, verbose )

    factors = [ ]
    factors.extend( smallFactors )
    factors.extend( largeFactors )

    for i in range( 0, len( factors ) ):
        for x in range( 2, 65536 ):
            modulus = pow( x, n_minus_1, candidate )

            if modulus != 1:
                if verbose:
                    print( 'Selfridge\'s test is finished:', candidate,
                           'is not a pseudo-prime to base', x, 'and is hence composite' )
                return False

            dividend = n_minus_1 // factors[ i ][ 0 ]
            T = pow( x, dividend, candidate )

            if T != 1:
                break

        if x == 65536:
            if verbose:
                print( 'Selfridge\'s test is finished:', candidate,
                       'is likely to be composite' )

            return False

    if verbose:
        if len( qPrimes ) == 0:
            print( 'Selfridge\'s test is finished:', candidate, 'is prime.' )
        else:
            print( 'Selfridge\'s test is finished:', candidate, 'is still q-prime.' )

    return True


# //******************************************************************************
# //
# //  factor
# //
# //  A factorization of *Nptr into prime and q-prime factors is first obtained.
# //
# //  Selfridge's primality test is then applied to any q-prime factors; the test
# //  is applied repeatedly until either a q-prime is found to be composite or
# //  likely to be composite (in which case the initial factorization is doubtful
# //  and an extra base should be used in Miller's test) or we run out of q-primes,
# //  in which case every q-prime factor of *Nptr is certified as prime.
# //
# //  Returns a list of tuples where each tuple is a prime factor and an exponent.
# //
# //
# //******************************************************************************

def factor( n ):
    verbose = g.verbose

    if n < -1:
        return [ ( -1, 1 ) ] + factor( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]

    target = int( n )

    dps = ceil( log( n ) )

    if dps > mp.dps:
        setAccuracy( dps )

    if target > g.minValueToCache:
        if g.factorCache is None:
            g.factorCache = loadFactorCache( )

            #for i in g.factorCache:
            #    print( i, g.factorCache[ i ] )

        if target in g.factorCache:
            if verbose:
                print( 'cache hit:', target )

            return g.factorCache[ target ]

    smallFactors, largeFactors, qPrimes = getPrimeFactors( int( n ), verbose )
    u = 0

    if len( qPrimes ) == 0:
        if verbose:
            print( 'NO Q-PRIMES:' )
            print( )
            print( n, 'has the following factorization:' )

            for i in smallFactors:
                print( 'prime factor:', i[ 0 ], 'exponent:', i[ 1 ] )

            for i in largeFactors:
                print( 'prime factor:', i[ 0 ], 'exponent:', i[ 1 ] )
    else:
        if verbose:
            print( 'testing q-primes for primality' )
            print( '--' )

        i = 0

        for qPrime in qPrimes:
            t = doSelfridgeTest( qPrime[ 0 ], verbose )

            if not t:
                print( 'do FACTOR() again with an extra base' )
                return 0

        if verbose:
            print( 'all q-primes are primes:', n, 'has the following factorization:' )
            print( )

            for i in smallFactors:
                print( 'prime factor:', i[ 0 ], 'exponent:', i[ 1 ] )

            for i in largeFactors:
                print( 'prime factor:', i[ 0 ], 'exponent:', i[ 1 ] )

    result = [ ]

    result.extend( smallFactors )
    result.extend( largeFactors )

    if not g.factorCache is None:
        product = int( fprod( [ power( i[ 0 ], i[ 1 ] ) for i in largeFactors ] ) )

        save = False

        if product not in g.factorCache:
            g.factorCache[ product ] = largeFactors
            save = True

        if n > g.minValueToCache and n not in g.factorCache:
            g.factorCache[ n ] = result
            save = True

        if save:
            saveFactorCache( g.factorCache )

    return result


# //******************************************************************************
# //
# //  getECMFactors
# //
# //  Returns a sorted list of factors
# //
# //******************************************************************************

def getECMFactors( n ):
    verbose = g.verbose
    randomSigma = True
    asymptoticSpeed = 10
    processingPower = 1.0

    result = [ ]

    if n < -1:
        return [ -1 ] + factor( fneg( n ) )
    elif n == -1:
        return [ -1 ]
    elif n == 0:
        return [ 0 ]
    elif n == 1:
        return [ 1 ]

    if verbose:
        print( 'factoring', n, '(', int( log10( n ) ), ')' )

    if g.factorCache is None:
        g.factorCache = loadFactorCache( )

        #for i in g.factorCache:
        #    print( i, g.factorCache[ i ] )

    if n in g.factorCache:
        if verbose:
            print( 'cache hit', n )
            print( )

        return getExpandedFactorList( g.factorCache[ n ] )

    for factor in factors( n, verbose, randomSigma, asymptoticSpeed, processingPower ):
        result.append( factor )

    largeFactors = list( collections.Counter( [ int( i ) for i in result if i > 65535 ] ).items( ) )
    product = int( fprod( [ power( i[ 0 ], i[ 1 ] ) for i in largeFactors ] ) )

    save = False

    if product not in g.factorCache:
        g.factorCache[ product ] = largeFactors
        save = True

    if n > g.minValueToCache and n not in g.factorCache:
        allFactors = list( collections.Counter( [ int( i ) for i in result ] ).items( ) )
        g.factorCache[ n ] = allFactors
        save = True

    if save:
        saveFactorCache( g.factorCache )

    if verbose:
        print( )

    return sorted( result )

