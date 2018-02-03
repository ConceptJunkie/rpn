#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnCombinatorics.py
# //
# //  RPN command-line calculator combinatorics operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools

from mpmath import arange, bell, bernoulli, binomial, e, fac, fadd, fdiv, floor, \
                   fmul, fprod, fsub, fsum, log10, mp, mpmathify, nint, nsum, pi, \
                   power, fprod, sqrt

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnNumberTheory import getNthLinearRecurrence, getLinearRecurrence
from rpn.rpnPersistence import cachedFunction
from rpn.rpnPolytope import getNthGeneralizedPolygonalNumber
from rpn.rpnUtils import debugPrint, oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         real, real_int


# //******************************************************************************
# //
# //  getNthAperyNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthAperyNumber( n ):
    '''
    http://oeis.org/A005259

    a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
    '''
    result = 0

    for k in arange( 0, real( n ) + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ),
                                     power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


# //******************************************************************************
# //
# //  getNthDelannoyNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDelannoyNumber( n ):
    result = 0

    for k in arange( 0, fadd( real( n ), 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


# //******************************************************************************
# //
# //  getNthSchroederNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSchroederNumber( n ):
    if real( n ) == 1:
        return 1

    if n < 0:
        raise ValueError( '\'nth_schroeder\' expects a non-negative argument' )

    n = fsub( n, 1 )

    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fdiv( fprod( [ power( 2, k ), binomial( n, k ),
                                              binomial( n, fsub( k, 1 ) ) ] ), n ) )

    return result


# //******************************************************************************
# //
# //  getNthMotzkinNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthMotzkinNumber( n ):
    '''
    http://oeis.org/A001006

    a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
    '''

    precision = int( fdiv( n, 1 ) )

    if ( mp.dps < precision ):
        mp.dps = precision

    result = 0

    for j in arange( 0, floor( fdiv( real( n ), 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                      binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


# //******************************************************************************
# //
# //  getNthPellNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPellNumber( n ):
    '''
    From:  http://oeis.org/A000129

    a( n ) = round( ( 1 + sqrt( 2 ) ) ^ n )
    '''
    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], n )


# //******************************************************************************
# //
# //  getPermutations
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getPermutations( n, r ):
    if ( real( r ) > real( n ) ):
        raise ValueError( 'number of elements {0} cannot exceed the size of the set {1}'.format( r, n ) )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


# //******************************************************************************
# //
# //  getCombinations
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getCombinations( n, r ):
    if ( real( r ) > real( n ) ):
        raise ValueError( 'number of elements {0} cannot exceed the size of the set {1}'.format( r, n ) )

    return fdiv( fac( n ), fmul( fac( fsub( n, r ) ), fac( r ) ) )


# //******************************************************************************
# //
# //  getArrangements
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getArrangements( n ):
    return floor( fmul( fac( n ), e ) )


# //******************************************************************************
# //
# //  getNthSylvester
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSylvester( n ):
    if real( n ) == 1:
        return 2
    elif n == 2:
        return 3
    else:
        list = [ 2, 3 ]

        for i in arange( 2, n ):
            list.append( fprod( list ) + 1 )

    return list[ -1 ]


# //******************************************************************************
# //
# //  createDeBruijnSequence
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def createDeBruijnSequence( n, k ):
    wordSize = real_int( k )
    symbolCount = real_int( n )

    v = [ 0 for _ in range( wordSize ) ]
    l = 1

    while True:
        if wordSize % l == 0:
            for i in range( 0, l ):
                yield v[ i ]

        for i in range( l, wordSize ):
            v[ i ] = v[ i - l ]

        l = wordSize

        while l > 0 and v[ l - 1 ] >= symbolCount - 1:
            l -= 1

        if l == 0:
            break

        v[ l - 1 ] += 1

def getDeBruijnSequence( n, k ):
    return RPNGenerator( createDeBruijnSequence( n, k ) )


# //******************************************************************************
# //
# //  getCompositions
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getCompositionsGenerator( n, k ):
    value = int( real_int( n ) )
    count = int( real_int( k ) )

    if count < 1:
        raise ValueError( "'compositions' expects a size argument greater than 0'" )

    if count == 1:
        yield [ value ]
    else:
        #result = [ ]

        for i in range( 1, int( ( value - count ) + 2 ) ):
            #result.extend( [ [ nint( i ) ] + comp for comp in getCompositions( n - i, count - 1 ) ] )
            for comp in getCompositionsGenerator( n - i, count - 1 ):
                yield [ nint( i ) ] + comp

@twoArgFunctionEvaluator( )
def getCompositions( n, k ):
    return RPNGenerator( getCompositionsGenerator( n, k ) )


# //******************************************************************************
# //
# //  OLDgetPartitionNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def OLDgetPartitionNumber( n ):
    if real_int( n ) < 0:
        raise ValueError( 'non-negative argument expected' )
    elif n in ( 0, 1 ):
        return 1

    total = 0
    sign = 1
    i = 1

    k = getNthGeneralizedPolygonalNumber( i, 5 )

    while n - k >= 0:
        total += sign * getPartitionNumber( fsub( n, k ) )

        i += 1

        if i % 2:
            sign *= -1

        k = getNthGeneralizedPolygonalNumber( i, 5 )

    return total


@oneArgFunctionEvaluator( )
@cachedFunction( 'partition' )
def getPartitionNumber( n ):
    '''
    This version is, um, less recursive than the original, which I've kept.
    The strategy is to create a list of the smaller partition numbers we need
    to calculate and then start calling them recursively, starting with the
    smallest.  This will minimize the number of recursions necessary, and in
    combination with caching values, will calculate practically any integer
    partition without the risk of a stack overflow.

    I can't help but think this is still grossly inefficient compared to what's
    possible.  It seems that using this algorithm, calculating any integer
    partition ends up necessitating calculating the integer partitions of
    every integer smaller than the original argument.
    '''
    debugPrint( 'partition', int( n ) )
    if real_int( n ) < 0:
        raise ValueError( 'non-negative argument expected' )
    elif n in ( 0, 1 ):
        return 1

    sign = 1
    i = 1
    k = 1

    estimate = log10( fdiv( power( e, fmul( pi, sqrt( fdiv( fmul( 2, n ), 3 ) ) ) ),
                            fprod( [ 4, n, sqrt( 3 ) ] ) ) )
    if mp.dps < estimate + 5:
        mp.dps = estimate + 5

    partitionList = [ ]
    signList = [ ]

    while n - k >= 0:
        partitionList.append( ( fsub( n, k ), sign ) )
        i += 1

        if i % 2:
            sign *= -1

        k = getNthGeneralizedPolygonalNumber( i, 5 )

    partitionList = partitionList[ : : -1 ]

    total = 0

    for partition, sign in partitionList:
        total = fadd( total, fmul( sign, getPartitionNumber( partition ) ) )

    return total


@oneArgFunctionEvaluator( )
@cachedFunction( 'new_partition' )
def NEWgetPartitionNumber( n ):
    if n < 0:
        return 0

    if n < 2:
        return 1

    result = mpmathify( 0 )

    for k in arange( 1, n + 1 ):
        #n1 = n - k * ( 3 * k - 1 ) / 2
        n1 = fsub( n, fdiv( fmul( k, fsub( fmul( 3, k ), 1 ) ), 2 ) )
        #n2 = n - k * ( 3 * k + 1 ) / 2
        n2 = fsub( n, fdiv( fmul( k, fadd( fmul( 3, k ), 1 ) ), 2 ) )

        result = fadd( result, fmul( power( -1, fadd( k, 1 ) ), fadd( getPartitionNumber( n1 ), getPartitionNumber( n2 ) ) ) )

        if n1 <= 0:
            break

    #old = NOT_QUITE_AS_OLDgetPartitionNumber( n )
    #
    #if ( old != result ):
    #    raise ValueError( "It's broke." )

    return result


# //******************************************************************************
# //
# //  getNthMultifactorial
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthMultifactorial( n, k ):
    return fprod( arange( real_int( n ), 0, -( real_int( k ) ) ) )


# //******************************************************************************
# //
# //  getMultinomial
# //
# //******************************************************************************

def getMultinomial( args ):
    numerator = fac( fsum( args ) )

    denominator = 1

    for arg in args:
        denominator = fmul( denominator, fac( arg ) )

    return fdiv( numerator, denominator )


# //******************************************************************************
# //
# //  getLahNumber
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getLahNumber( n, k ):
    return fmul( power( -1, n ), fdiv( fmul( binomial( real( n ), real( k ) ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ) )


# //******************************************************************************
# //
# //  getNarayanaNumber
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNarayanaNumber( n, k ):
    return fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n )


# //******************************************************************************
# //
# //  getNthCatalanNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCatalanNumber( n ):
    return fdiv( binomial( fmul( 2, real( n ) ), n ), fadd( n, 1 ) )


# //******************************************************************************
# //
# //  getNthSchroederHipparchusNumber
# //
# //  https://en.wikipedia.org/wiki/Schr%C3%B6der%E2%80%93Hipparchus_number
# //  https://oeis.org/A001003
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSchroederHipparchusNumber( n ):
    if n == 0:
        return 1

    result = 0

    for i in arange( n ):
        result = fadd( result, fmul( getNarayanaNumber( n, fadd( i, 1 ) ), power( 2, i ) ) )

    return result


# //******************************************************************************
# //
# //  getNthMenageNumber
# //
# //  https://oeis.org/A000179
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthMenageNumber( n ):
    if n < 0:
        raise ValueError( '\'menage\' requires a non-negative argument' )
    elif n in [ 1, 2 ]:
        return 0
    elif n in [ 0, 3 ]:
        return 1
    else:
        return nsum( lambda k: fdiv( fprod( [ power( -1, k ), fmul( 2, n ), binomial( fsub( fmul( 2, n ), k ), k ),
                                            fac( fsub( n, k ) ) ] ), fsub( fmul( 2, n ), k ) ), [ 0, n ] )

@twoArgFunctionEvaluator( )
def getBellPolynomial( n, k ):
    return bell( n, k )

@twoArgFunctionEvaluator( )
def getBinomial( n, k ):
    return binomial( n, k )

@oneArgFunctionEvaluator( )
def getNthBell( n ):
    return bell( n )

@oneArgFunctionEvaluator( )
def getNthBernoulli( n ):
    return bernoulli( n )


# //******************************************************************************
# //
# //  getDenominationCombinations
# //
# //  https://math.stackexchange.com/questions/176363/keep-getting-generating-function-wrong-making-change-for-a-dollar/176397#176397
# //
# //  Here's another way from Sloane that doesn't require so much memory:
# //
# //  a(n) = (1/n)*Sum_{k=1..n} A008472(k)*a(n-k).
# //
# //******************************************************************************

def getDenominationCombinations( denominations, target ):
    target = int( target )
    data = [ 0 ] * ( target + 1 )
    data[ 0 ] = 1

    for k in denominations:
        k = int( k )

        for i in range( 0, target - k + 1 ):
            data[ i + k ] += data[ i ]

    return data[ target ]


#  http://crowsandcats.blogspot.com/2013/04/approximate-restricted-integer.html

#Recursive restricted block partition. Each call reduces the sum, n,
# and m, the number of parts.
#def blockpart(n, m, k):
#
#    #Is the number of parts only 1?
#    if(m == 1):
#        #Trivial: to partition n into one part, we need to be able to use  n
#        if(n < k):
#            return 1
#        else:
#            return 0
#    #what is the highest possible sum we may have
#    #that will still be a valid partition
#    smax = m * (k - 1)
#    #This is the lowest term we can add to the partition (subtract from sum)
#    start = n - k + 1
#
#    #If the lowest is too high, then we aren't able to get a valid partition
#    if( start > smax):
#        return 0
#
#    paths = 0
#
#    #add up all possible other partitions after subtracting choices
#    #to place in the current part (m)
#    for i in range(max(0,start), 1 + min(smax, n)):
#        paths += blockpart(i, m - 1, k)
#
#    return paths


