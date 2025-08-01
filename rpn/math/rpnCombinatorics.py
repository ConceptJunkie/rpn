#!/usr/bin/env python

#******************************************************************************
#
#  rpnCombinatorics.py
#
#  rpnChilada combinatorics operators
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import arange, bell, bernfrac, bernoulli, binomial, e, fac, fadd, fdiv, \
                   floor, fmul, fprod, fsub, fsum, log10, mp, mpmathify, nint, nsum, pi, \
                   power, sqrt, stirling1, stirling2

from rpn.math.rpnNumberTheory import getNthLinearRecurrence
from rpn.math.rpnPolytope import getNthGeneralizedPolygonalNumber

from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnPersistence import cachedFunction
from rpn.util.rpnSettings import setAccuracy
from rpn.util.rpnUtils import listAndOneArgFunctionEvaluator, listArgFunctionEvaluator, \
                         oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, ComplexValidator, IntValidator, ListValidator

from flint import *


#******************************************************************************
#
#  getNthAperyNumberOperator
#
#******************************************************************************

@cachedFunction( 'apery' )
def getNthAperyNumber( n ):
    '''
    http://oeis.org/A005259

    a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
    '''
    setAccuracy( fmul( n, 1.6 ) )

    result = 0

    for k in arange( 0, n + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ),
                                     power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthAperyNumberOperator( n ):
    return getNthAperyNumber( n )


#******************************************************************************
#
#  getNthDelannoyNumberOperator
#
#******************************************************************************

@cachedFunction( 'delannoy' )
def getNthDelannoyNumber( n ):
    if n == 1:
        return 3

    setAccuracy( fmul( n, 0.8 ) )

    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthDelannoyNumberOperator( n ):
    return getNthDelannoyNumber( n )


#******************************************************************************
#
#  getNthSchroederNumberOperator
#
#******************************************************************************

@cachedFunction( 'schroeder' )
def getNthSchroederNumber( n ):
    if n == 1:
        return 1

    n = fsub( n, 1 )

    result = 0

    setAccuracy( fmul( n, 0.8 ) )

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fdiv( fprod( [ power( 2, k ), binomial( n, k ),
                                              binomial( n, fsub( k, 1 ) ) ] ), n ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthSchroederNumberOperator( n ):
    return getNthSchroederNumber( n )


#******************************************************************************
#
#  getNthMotzkinNumberOperator
#
#******************************************************************************

@cachedFunction( 'motzkin' )
def getNthMotzkinNumber( n ):
    '''
    http://oeis.org/A001006

    a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
    '''
    setAccuracy( n )

    result = 0

    for j in arange( 0, floor( fdiv( n, 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                        binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthMotzkinNumberOperator( n ):
    return getNthMotzkinNumber( n )


#******************************************************************************
#
#  getNthSchroederHipparchusNumberOperator
#
#******************************************************************************

@cachedFunction( 'schroeder_hipparchus' )
def getNthSchroederHipparchusNumber( n ):
    '''
    https://en.wikipedia.org/wiki/Schr%C3%B6der%E2%80%93Hipparchus_number
    https://oeis.org/A001003
    '''
    if n == 0:
        return 1

    setAccuracy( fmul( n, 0.8 ) )

    result = 0

    for i in arange( n ):
        result = fadd( result, fmul( getNarayanaNumber( n, fadd( i, 1 ) ), power( 2, i ) ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthSchroederHipparchusNumberOperator( n ):
    return getNthSchroederHipparchusNumber( n )


#******************************************************************************
#
#  getNthPellNumberOperator
#
#******************************************************************************

def getNthPellNumber( n ):
    '''
    From:  http://oeis.org/A000129:
    a( n ) = round( ( 1 + sqrt( 2 ) ) ^ n )
    '''
    setAccuracy( fmul( n, 0.4 ) )

    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], fsub( n, 1 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthPellNumberOperator( n ):
    return getNthPellNumber( n )


#******************************************************************************
#
#  getPermutations
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getPermutationsOperator( n, r ):
    if r > n:
        raise ValueError( f'number of elements { r } cannot exceed the size of the set { r }' )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


#******************************************************************************
#
#  getCombinations
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getCombinationsOperator( n, r ):
    if r > n:
        raise ValueError( f'number of elements { r } cannot exceed the size of the set { n }' )

    return fdiv( fac( n ), fmul( fac( fsub( n, r ) ), fac( r ) ) )


#******************************************************************************
#
#  getArrangements
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getArrangementsOperator( n ):
    return floor( fmul( fac( n ), e ) )


#******************************************************************************
#
#  getNthSylvesterNumberOperator
#
#******************************************************************************

def getNthSylvesterNumber( n ):
    if n == 1:
        return 2

    if n == 2:
        return 3

    sylvesters = [ 2, 3 ]

    for _ in arange( 2, n ):
        sylvesters.append( fprod( sylvesters ) + 1 )

    return sylvesters[ -1 ]


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getNthSylvesterNumberOperator( n ):
    return getNthSylvesterNumber( n )


#******************************************************************************
#
#  createDeBruijnSequence
#
#******************************************************************************

def createDeBruijnSequence( n, k ):
    wordSize = int( k )
    symbolCount = int( n )

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


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def getDeBruijnSequenceOperator( n, k ):
    return RPNGenerator( createDeBruijnSequence( n, k ) )


#******************************************************************************
#
#  getCompositions
#
#******************************************************************************

def getCompositionsGenerator( n, k ):
    value = int( n )
    count = int( k )

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
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getCompositionsOperator( n, k ):
    return RPNGenerator( getCompositionsGenerator( n, k ) )


#******************************************************************************
#
#  oldGetPartitionNumber2
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def oldGetPartitionNumber2( n ):
    if n in ( 0, 1 ):
        return 1

    total = 0
    sign = 1
    i = 1

    k = getNthGeneralizedPolygonalNumber( i, 5 )

    while n - k >= 0:
        total += sign * oldGetPartitionNumber2( fsub( n, k ) )

        i += 1

        if i % 2:
            sign *= -1

        k = getNthGeneralizedPolygonalNumber( i, 5 )

    return total


#public static long partition(long k, long n){
#    long sum = 0;
#    if(k > n) return 0;
#    if(k == n) return 1;
#    sum += partition(k+1, n) + partition(k, n-k);
#    return sum;
#}

def partitionsWithLimit( n, k=None ):
    """Generate all partitions of integer n (>= 0) using integers no
    greater than k (default, None, allows the partition to contain n).

    Each partition is represented as a multiset, i.e. a dictionary
    mapping an integer to the number of copies of that integer in
    the partition.  For example, the partitions of 4 are {4: 1},
    {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, and {1: 4} corresponding to
    [4], [1, 3], [2, 2], [1, 1, 2] and [1, 1, 1, 1], respectively.
    In general, sum(k * v for k, v in a_partition.iteritems()) == n, and
    len(a_partition) is never larger than about sqrt(2*n).

    Note that the _same_ dictionary object is returned each time.
    This is for speed:  generating each partition goes quickly,
    taking constant time independent of n. If you want to build a list
    of returned values then use .copy() to get copies of the returned
    values:

    >>> p_all = []
    >>> for p in partitions(6, 2):
    ...         p_all.append(p.copy())
    ...
    >>> print p_all
    [{2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]

    Reference
    ---------
    Modified from Tim Peter's posting to accomodate a k value:
    http://code.activestate.com/recipes/218332/
    """
    n = int( n )

    if n < 0 or k < 0:
        raise ValueError( '\'partition_limit\' requires a positive count and a positive limit' )

    if n == 0:
        yield [ ]
        return

    if k is None or k > n:
        k = n

    k = int( k )

    quotient, remainder = divmod( n, k )
    itemCounts = { k : quotient }
    keys = [ k ]

    if remainder:
        itemCounts[ remainder ] = 1
        keys.append( remainder )

    result = [ ]

    for key, value in itemCounts.items( ):
        result.extend( [ key ] * value )

    yield result

    while keys != [ 1 ]:
        # Reuse any 1's.
        if keys[ -1 ] == 1:
            del keys[ -1 ]
            reuse = itemCounts.pop( 1 )
        else:
            reuse = 0

        # Let i be the smallest key larger than 1.  Reuse one
        # instance of i.
        i = keys[ -1 ]
        newcount = itemCounts[ i ] = itemCounts[ i ] - 1
        reuse += i

        if newcount == 0:
            del keys[ -1 ], itemCounts[ i ]

        # Break the remainder into pieces of size i - 1.
        i -= 1
        quotient, remainder = divmod( reuse, i )
        itemCounts[ i ] = quotient
        keys.append( i )

        if remainder:
            itemCounts[ remainder ] = 1
            keys.append( remainder )

        result = [ ]

        for key, value in itemCounts.items( ):
            result.extend( [ key ] * value )

        yield result


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def getPartitionsWithLimitOperator( n, k ):
    k = min( k, n )

    return RPNGenerator( partitionsWithLimit( n, k ) )


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

    if n in ( 0, 1 ):
        return 1

    sign = 1
    i = 1
    k = 1

    estimate = log10( fdiv( power( e, fmul( pi, sqrt( fdiv( fmul( 2, n ), 3 ) ) ) ),
                            fprod( [ 4, n, sqrt( 3 ) ] ) ) )
    setAccuracy( estimate + 5 )

    partitionList = [ ]

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

def getPartitionNumber( n ):
    '''
    Fredrick Johannson's version of the partition number, which is infinitely
    better than anything I could come up with. It uses the FLINT library to
    calculate the partition number for any integer n, and since it's not
    recursive, I'm not bothering to cache it anymore.
    '''
    debugPrint( 'partition', int( n ) )

    if n in ( 0, 1 ):
        return 1

    total = mpmathify( int ( fmpz( int ( n ) ).partitions_p( ) ) )

    return total



@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getPartitionNumberOperator( n ):
    return getPartitionNumber( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
@cachedFunction( 'old_partition' )
def oldGetPartitionNumber( n ):
    if n < 2:
        return 1

    result = mpmathify( 0 )

    for k in arange( 1, n + 1 ):
        #n1 = n - k * ( 3 * k - 1 ) / 2
        sub1 = fsub( n, fdiv( fmul( k, fsub( fmul( 3, k ), 1 ) ), 2 ) )
        #n2 = n - k * ( 3 * k + 1 ) / 2
        sub2 = fsub( n, fdiv( fmul( k, fadd( fmul( 3, k ), 1 ) ), 2 ) )

        result = fadd( result, fmul( power( -1, fadd( k, 1 ) ),
                                     fadd( getPartitionNumber( sub1 ), getPartitionNumber( sub2 ) ) ) )

        if sub1 <= 0:
            break

    #old = NOT_QUITE_AS_OLDgetPartitionNumber( n )
    #
    #if ( old != result ):
    #    raise ValueError( "It's broke." )

    return result


#******************************************************************************
#
#  createIntegerPartitions
#
#  https://code.activestate.com/recipes/218332-generator-for-integer-partitions/
#
#  http://jeromekelleher.net/generating-integer-partitions.html provides a
#  similar version of this algorithm.
#
#******************************************************************************

def createIntegerPartitions( n ):
    """Generate partitions of n as ordered lists in ascending
    lexicographical order.

    This highly efficient routine is based on the delightful
    work of Kelleher and O'Sullivan.

    Examples
    ========

    >>> for i in aP(6): i
    ...
    [1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 2]
    [1, 1, 1, 3]
    [1, 1, 2, 2]
    [1, 1, 4]
    [1, 2, 3]
    [1, 5]
    [2, 2, 2]
    [2, 4]
    [3, 3]
    [6]

    >>> for i in aP(0): i
    ...
    []

    References
    ==========

    .. [1] Generating Integer Partitions, [online],
        Available: http://jeromekelleher.net/generating-integer-partitions.html
    .. [2] Jerome Kelleher and Barry O'Sullivan, "Generating All
        Partitions: A Comparison Of Two Encodings", [online],
        Available: http://arxiv.org/pdf/0909.2331v2.pdf

    """
    # The list `a`'s leading elements contain the partition in which
    # y is the biggest element and x is either the same as y or the
    # 2nd largest element; v and w are adjacent element indices
    # to which x and y are being assigned, respectively.
    a = [ 1 ] * n
    y = -1
    v = n

    while v > 0:
        v -= 1
        x = a[ v ] + 1

        while y >= 2 * x:
            a[ v ] = x
            y -= x
            v += 1

        w = v + 1

        while x <= y:
            a[ v ] = x
            a[ w ] = y
            yield a[ : w + 1 ]
            x += 1
            y -= 1

        a[ v ] = x + y
        y = a[ v ] - 1
        yield a[ : w ]


#******************************************************************************
#
#  getIntegerPartitions
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getIntegerPartitionsOperator( n ):
    return RPNGenerator( createIntegerPartitions( int( n ) ) )


#******************************************************************************
#
#  getNthMultifactorial
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getNthMultifactorialOperator( n, k ):
    return fprod( arange( n, 0, -( k ) ) )


#******************************************************************************
#
#  getMultinomialOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getMultinomialOperator( n ):
    numerator = fac( fsum( n ) )

    denominator = 1

    for arg in n:
        denominator = fmul( denominator, fac( arg ) )

    return fdiv( numerator, denominator )


#******************************************************************************
#
#  getLahNumberOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getLahNumberOperator( n, k ):
    return fmul( power( -1, n ), fdiv( fmul( binomial( n, k ),
                                             fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ) )


#******************************************************************************
#
#  getNarayanaNumber
#
#******************************************************************************

def getNarayanaNumber( n, k ):
    return fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getNarayanaNumberOperator( n, k ):
    return getNarayanaNumber( n, k )


#******************************************************************************
#
#  getNthCatalanNumber
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthCatalanNumberOperator( n ):
    return fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) )


#******************************************************************************
#
#  getNthMenageNumberOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthMenageNumber( n ):
    '''https://oeis.org/A000179'''
    if n == 1:
        return -1

    if n == 2:
        return 0

    if n in [ 0, 3 ]:
        return 1

    return nsum( lambda k: fdiv( fprod( [ power( -1, k ), fmul( 2, n ), binomial( fsub( fmul( 2, n ), k ), k ),
                                          fac( fsub( n, k ) ) ] ), fsub( fmul( 2, n ), k ) ), [ 0, n ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthMenageNumberOperator( n ):
    return getNthMenageNumber( n )


#******************************************************************************
#
#  getNthBellPolynomialOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), ComplexValidator( ) ] )
def getNthBellPolynomialOperator( n, k ):
    return bell( n, k )


#******************************************************************************
#
#  getBinomialOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), ComplexValidator( ) ] )
def getBinomialOperator( n, k ):
    return binomial( n, k )


#******************************************************************************
#
#  getNthBellNumberOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthBellNumberOperator( n ):
    return bell( n )


#******************************************************************************
#
#  getNthBernoulliNumberOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthBernoulliNumberOperator( n ):
    return bernoulli( n )


#******************************************************************************
#
#  getNthBernoulliFractionOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthBernoulliFractionOperator( n ):
    return list( bernfrac( n ) )


#******************************************************************************
#
#  getNthBernoulliNumeratorOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthBernoulliNumeratorOperator( n ):
    return bernfrac( n )[ 0 ]


#******************************************************************************
#
#  getNthBernoulliDenominatorOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthBernoulliDenominatorOperator( n ):
    return bernfrac( n )[ 1 ]


#******************************************************************************
#
#  countFrobeniusOperator
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ) ] )
def countFrobeniusOperator( denominations, target ):
    '''
    https://math.stackexchange.com/questions/176363/keep-getting-generating- \
    function-wrong-making-change-for-a-dollar/176397#176397

    Here's another way from Sloane that doesn't require so much memory:

    a(n) = (1/n)*Sum_{k=1..n} A008472(k)*a(n-k).
    '''
    target = int( target )
    data = [ 0 ] * ( target + 1 )
    data[ 0 ] = 1

    for k in denominations:
        k = int( k )

        for i in range( 0, target - k + 1 ):
            data[ i + k ] += data[ i ]

    return data[ target ]


#******************************************************************************
#
#  getStirling1NumberOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getStirling1NumberOperator( n, k ):
    return stirling1( n, k )


#******************************************************************************
#
#  getStirling2NumberOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getStirling2NumberOperator( n, k ):
    return stirling2( n, k )


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
#    #thatbb will still be a valid partition
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
