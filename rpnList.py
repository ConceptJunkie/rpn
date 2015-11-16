#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnList.py
# //
# //  RPN command-line calculator list operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools
import random

from mpmath import *

from rpnMeasurement import RPNMeasurement
from rpnNumberTheory import getGCD


# //******************************************************************************
# //
# //  class RPNGenerator
# //
# //******************************************************************************

class RPNGenerator( ):
    def __init__( self, generator = None, count = -1 ):
        self.generator = generator
        self.count = count

    def getGenerator( self ):
        return self.generator

    def getCount( self ):
        return self.count

    def __iter__( self ):
        return self.getGenerator( )

    def __getitem__( self, index ):
        return next( itertools.islice( self.generator, index, index + 1 ) )

    @staticmethod
    def create( value ):
        if isinstance( value, RPNGenerator ):
            return value
        else:
            if isinstance( value, list ):
                count = len( value )
            else:
                count = 1

            return RPNGenerator( itemGenerator( value ), count )

    @staticmethod
    def createRange( start, end, step = 1 ):
        try:
            result = RPNGenerator( rangeGenerator( start, end, step ),
                                   ceil( fdiv( fadd( fsub( end, start ), 1 ), step ) ) )
        except TypeError:
            result = RPNGenerator( rangeGenerator( start, end, step ) )

        return result

    @staticmethod
    def createGeometric( value, step, count ):
        return RPNGenerator( geometricRangeGenerator( value, step, count ), count )

    @staticmethod
    def createExponential( value, step, count ):
        return RPNGenerator( exponentialRangeGenerator( value, step, count ), count )

    @staticmethod
    def createChained( generator, func ):
        return RPNGenerator( chainedGenerator( generator, func ) )


# //******************************************************************************
# //
# //  itemGenerator
# //
# //  A generator for a single item or list, used in list operators
# //
# //******************************************************************************

def itemGenerator( value ):
    if isinstance( value, list ):
        for item in value:
            yield item
    else:
        for item in [ value ]:
            yield item


# //******************************************************************************
# //
# //  rangeGenerator
# //
# //******************************************************************************

def rangeGenerator( start, end, step ):
    if start > end and step > 0:
        step = -step

    current = start

    if ( step > 0 ):
        while ( current <= end ):
            yield current
            current = fadd( current, step )
    else:
        while ( current >= end ):
            yield current
            current = fadd( current, step )


# //******************************************************************************
# //
# //  geometricRangeGenerator
# //
# //******************************************************************************

def geometricRangeGenerator( value, step, count ):
    current = value

    for i in arange( 0, count ):
        yield current
        current = fmul( current, step )


# //******************************************************************************
# //
# //  exponentialRangeGenerator
# //
# //******************************************************************************

def exponentialRangeGenerator( value, step, count ):
    current = value

    for i in arange( 0, count ):
        yield current
        current = power( current, step )


# //******************************************************************************
# //
# //  chainedGenerator
# //
# //******************************************************************************

def chainedGenerator( generator, func ):
    for i in generator:
        yield( func( i ) )


# //******************************************************************************
# //
# //  alternateSigns
# //
# //******************************************************************************

def alternateSigns( n, startNegative = False ):
    negative = startNegative

    for i in n.getGenerator( ):
        yield fneg( i ) if negative else i
        negative = not negative


# //******************************************************************************
# //
# //  getAlternatingSum
# //
# //******************************************************************************

def getAlternatingSum( arg, startNegative = False ):
    result = 0

    negative = startNegative

    for i in arg.getGenerator( ):
        if negative:
            result = fsub( result, i )
        else:
            result = fadd( result, i )

        negative = not negative

    return result


# //******************************************************************************
# //
# //  appendLists
# //
# //******************************************************************************

def appendLists( arg1, arg2 ):
    result = list( arg1 )
    result.extend( list( arg2 ) )

    return result


# //******************************************************************************
# //
# //  countElements
# //
# //******************************************************************************

def countElements( arg ):
    if arg.getCount( ) > -1:
        return arg.getCount( )

    count = 0

    for i in arg.getGenerator( ):
        count += 1

    return count


# //******************************************************************************
# //
# //  interleave
# //
# //******************************************************************************

def interleave( arg1, arg2 ):
    result = list( )

    combined = list( zip( arg1, arg2  ) )
    combined = [ item for sublist in combined for item in sublist ]

    for i in combined:
        result.append( i )
    else:
        for i in arg1:
            result.append( i )
            result.append( arg2 )

    return result


# //******************************************************************************
# //
# //  makeUnion
# //
# //******************************************************************************

def makeUnion( arg1, arg2 ):
    result = set( arg1 )
    return list( result.union( set( arg2 ) ) )


# //******************************************************************************
# //
# //  makeIntersection
# //
# //******************************************************************************

def makeIntersection( arg1, arg2 ):
    result = set( arg1 )
    return list( result.intersection( set( arg2 ) ) )


# //******************************************************************************
# //
# //  getIndexOfMax
# //
# //******************************************************************************

def getIndexOfMax( arg ):
    maximum = -inf
    result = -1

    for index, i in enumerate( arg ):
        if i > maximum:
            maximum = i
            result = index

    return result


# //******************************************************************************
# //
# //  getIndexOfMin
# //
# //******************************************************************************

def getIndexOfMin( arg ):
    minimum = inf
    result = -1

    for index, i in enumerate( arg ):
        if i < minimum:
            minimum = i
            result = index

    return result


# //******************************************************************************
# //
# //  getListElement
# //
# //******************************************************************************

def getListElement( arg, index ):
    return arg[ int( index[ 0 ] ) ]


# //******************************************************************************
# //
# //  getSlice
# //
# //******************************************************************************

def getSlice( arg, start_, end_ ):
    start = int( start_[ 0 ] )
    end = int( end_[ 0 ] )

    result = [ arg[ start ] ]

    for i in range( end - start - 1 ):
        result.append( next( arg.getGenerator( ) ) )

    return result


# //******************************************************************************
# //
# //  getSublist
# //
# //******************************************************************************

def getSublist( arg, start, count ):
    result = [ ]

    fullList = [ item for item in arg.getGenerator( ) ]

    for i in start.getGenerator( ):
        for j in count.getGenerator( ):
            result.append( fullList[ int( i ) : int( j ) ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


# //******************************************************************************
# //
# //  getLeft
# //
# //******************************************************************************

def getLeft( arg, count ):
    result = [ ]

    for i in count.getGenerator( ):
        result.append( [ j for j in arg.getGenerator( ) ][ : int( i ) ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


# //******************************************************************************
# //
# //  getRight
# //
# //******************************************************************************

def getRight( arg, count ):
    result = [ ]

    for i in count.getGenerator( ):
        result.append( [ j for j in arg.getGenerator( ) ][ int( fneg( i ) ) : ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


# //******************************************************************************
# //
# //  getListDiffs
# //
# //******************************************************************************

def getListDiffs( arg ):
    old = None

    for i in arg.getGenerator( ):
        if old is not None:
            yield( fsub( i, old ) )

        old = i


# //******************************************************************************
# //
# //  getCumulativeListDiffs
# //
# //******************************************************************************

def getCumulativeListDiffs( arg ):
    result = [ ]

    first = None

    for i in arg.getGenerator( ):
        if first is None:
            first = i
        else:
            yield fsub( i, first )


# //******************************************************************************
# //
# //  getListRatios
# //
# //******************************************************************************

def getListRatios( args ):
    old = None

    for i in arg.getGenerator( ):
        if old is not None:
            yield( fdiv( i, old ) )

        old = i


# //******************************************************************************
# //
# //  getCumulativeListRatios
# //
# //******************************************************************************

def getCumulativeListRatios( arg ):
    result = [ ]

    first = None

    for i in arg.getGenerator( ):
        if first is None:
            first = i
        else:
            yield fdiv( i, first )


# //******************************************************************************
# //
# //  getReverse
# //
# //******************************************************************************

def getReverse( args ):
    return [ i for i in reversed( [ j for j in args.getGenerator( ) ] ) ]


# //******************************************************************************
# //
# //  shuffleList
# //
# //******************************************************************************

def shuffleList( args ):
    if not isinstance( args, list ):
        return args

    if isinstance( args[ 0 ], list ):
        result = [ ]

        for i in range( 0, len( args ) ):
            result.append( shuffleList( args[ i ] ) )

        return result
    else:
        result = args[ : ]
        random.shuffle( result )
        return result


# //******************************************************************************
# //
# //  getUniqueElements
# //
# //******************************************************************************

def getUniqueElements( args ):
    return list( set( args ) )


# //******************************************************************************
# //
# //  sortAscending
# //
# //******************************************************************************

def sortAscending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ] ) )

        return result
    else:
        return sorted( args )


# //******************************************************************************
# //
# //  sortDescending
# //
# //******************************************************************************

def sortDescending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ], reverse = True ) )

        return result
    else:
        return sorted( args, reverse = True )


# //******************************************************************************
# //
# //  calculatePowerTower
# //
# //******************************************************************************

def calculatePowerTower( args ):
    if isinstance( args[ 0 ], list ):
        return [ calculatePowerTower( arg ) for arg in args ]

    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


# //******************************************************************************
# //
# //  calculatePowerTower2
# //
# //******************************************************************************

def calculatePowerTower2( args ):
    if isinstance( args[ 0 ], list ):
        return [ calculatePowerTower2( arg ) for arg in args ]

    result = args[ -1 ]

    for i in args[ -2 : : -1 ]:
        result = power( i, result )

    return result


# //******************************************************************************
# //
# //  getSum
# //
# //******************************************************************************

def getSum( n ):
    result = 0

    for i in n.getGenerator( ):
        result = fadd( result, i )

    return result


# //******************************************************************************
# //
# //  getProduct
# //
# //******************************************************************************

def getProduct( n ):
    if len( n ) == 0:
        return 0
    elif len( n ) == 1:
        return n[ 0 ]

    hasUnits = False

    for item in n:
        if isinstance( item, RPNMeasurement ):
            hasUnits = True
            break

    if hasUnits:
        result = RPNMeasurement( 1, { } )

        for item in n:
            if isinstance( item, list ):
                return [ getProduct( arg ) for arg in item ]

            result = result.multiply( item )

        return result
    else:
        if len( n ) == 0:
            return 0

        if isinstance( n[ 0 ], list ):
            return [ getProduct( item ) for item in n ]
        else:
            return fprod( n )


# //******************************************************************************
# //
# //  getStandardDeviation
# //
# //******************************************************************************

def getStandardDeviation( args ):
    if isinstance( args[ 0 ], list ):
        return [ getStandardDeviation( arg ) for arg in args ]

    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fsum( dev ) / len( dev ) )


# //******************************************************************************
# //
# //  reduceList
# //
# //  This function reduces out the greatest common denominator from a list of
# //  values.
# //
# //******************************************************************************

def reduceList( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ reduceList( arg ) for arg in args ]
        else:
            gcd = getGCD( args )

            result = [ ]

            for i in args:
                result.append( fdiv( i, gcd ) )

            return result
    else:
        return args


# //******************************************************************************
# //
# //  calculateGeometricMean
# //
# //******************************************************************************

def calculateGeometricMean( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ calculateGeometricMean( arg ) for arg in args ]
        else:
            return root( fprod( args ), len( args ) )
    else:
        return args


# //******************************************************************************
# //
# //  calculateArithmeticMean
# //
# //******************************************************************************

def calculateArithmeticMean( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ calculateMean( arg ) for arg in args ]
        else:
            return fdiv( fsum( args ), len( args ) )
    else:
        return args


# //******************************************************************************
# //
# //  getMax
# //
# //******************************************************************************

def getMax( args ):
    return max( list( args ) )


# //******************************************************************************
# //
# //  getMin
# //
# //******************************************************************************

def getMin( args ):
    return min( list( args ) )

# //******************************************************************************
# //
# //  getZeroes
# //
# //******************************************************************************

def getZeroes( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getZeroes( arg ) for arg in args ]
        else:
            return [ index for index, e in enumerate( args ) if e == 0 ]
    else:
        return args


# //******************************************************************************
# //
# //  getNonzeroes
# //
# //******************************************************************************

def getNonzeroes( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getNonzeroes( arg ) for arg in args ]
        else:
            return [ index for index, e in enumerate( args ) if e != 0 ]
    else:
        return args


# //******************************************************************************
# //
# //  groupElements
# //
# //******************************************************************************

def groupElements( args, count ):
    if isinstance( count, list ):
        return [ groupElements( args, i ) for i in count ]

    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ groupElements( args, count ) for arg in args ]
        else:
            result = [ ]

            n = int( count )

            for i in range( 0, len( args ), n ):
                result.append( args[ i : i + n ] )

            return result
    else:
        return [ args ]


# //******************************************************************************
# //
# //  getOccurrences
# //
# //******************************************************************************

def getOccurrences( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getOccurrences( arg ) for arg in args ]
        else:
            counter = collections.Counter( )

            for i in args:
                counter[ i ] += 1

            result = [ ]

            for i in counter:
                result.append( [ i, counter[ i ] ] )

            return sorted( result )

    else:
        return [ [ args, 1 ] ]


# //******************************************************************************
# //
# //  flatten
# //
# //******************************************************************************

def flatten( value ):
    result = [ ]

    if isinstance( value, list ):
        for item in value:
            result.extend( flatten( item ) )
    elif isinstance( value, RPNGenerator ):
        for item in value.getGenerator( ):
            result.extend( flatten( item ) )
    else:
        result.append( value )

    return result

