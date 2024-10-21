#!/usr/bin/env python

#******************************************************************************
#
#  rpnList.py
#
#  rpnChilada list operators
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import collections
import itertools
import random
import types

from mpmath import arange, fadd, fdiv, fmod, fmul, fneg, fprod, fsub, fsum, inf, mpmathify, power, \
                   root, sqrt

from rpn.math.rpnMath import add, multiply, square, subtract, divide
from rpn.units.rpnMeasurementClass import RPNMeasurement
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnUtils import getPowerSet, listArgFunctionEvaluator, listAndOneArgFunctionEvaluator, \
                         listAndTwoArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, ComparableValidator, ComplexValidator, DefaultValidator, IntValidator, \
                             ListValidator


#******************************************************************************
#
#  getGCD
#
#******************************************************************************

def getGCD( n, k ):
    while k:
        n, k = k, fmod( n, k )

    return n


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getGCDOperator( n, k ):
    return getGCD( n, k )


#******************************************************************************
#
#  getGCDOfListOperator
#
#******************************************************************************

def getGCDOfList( args ):
    if isinstance( args, RPNGenerator ):
        args = list( args )

    if not isinstance( args, list ):
        args = [ args ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getGCDOfList( arg ) for arg in args ]

    result = set( )

    if len( args ) == 1:
        return args[ 0 ]

    for pair in itertools.combinations( args, 2 ):
        result.add( getGCD( *pair ) )

    if len( result ) == 1:
        return result.pop( )

    return getGCDOfList( list( result ) )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getGCDOfListOperator( n ):
    return getGCDOfList( n )


#******************************************************************************
#
#  alternateSigns
#
#******************************************************************************

def alternateSigns( n, startNegative = False ):
    negative = startNegative

    for i in n:
        yield fneg( i ) if negative else i
        negative = not negative


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def alternateSignsOperator( n ):
    return RPNGenerator( alternateSigns( n, False ) )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def alternateSigns2Operator( n ):
    return RPNGenerator( alternateSigns( n, True ) )


#******************************************************************************
#
#  getAlternatingSum
#
#******************************************************************************

def getAlternatingSum( args, startNegative = False ):
    result = 0

    negative = startNegative

    for i in args:
        if negative:
            result = fsub( result, i )
        else:
            result = fadd( result, i )

        negative = not negative

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getAlternatingSumOperator( n ):
    return getAlternatingSum( n, False )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getAlternatingSum2Operator( n ):
    return getAlternatingSum( n, True )


#******************************************************************************
#
#  appendLists
#
#******************************************************************************

def appendLists( arg1, arg2 ):
    result = list( arg1 )
    result.extend( list( arg2 ) )

    return result


@argValidator( [ ListValidator( ), ListValidator( ) ] )
def appendListsOperator( n, k ):
    return appendLists( n, k )


#******************************************************************************
#
#  compareListsOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def compareListsOperator( arg1, arg2 ):
    if len( arg1 ) != len( arg2 ):
        return 0

    for i, arg in enumerate( arg1 ):
        if arg != arg2[ i ]:
            return 0

    return 1


#******************************************************************************
#
#  countElementsOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def countElementsOperator( args ):
    if isinstance( args, list ):
        return len( args )

    if isinstance( args, RPNGenerator ) and args.getCount( ) > -1:
        return args.getCount( )

    # args might be a generator, so we need to iterate
    count = 0

    for _ in args:
        count += 1

    return count


#******************************************************************************
#
#  interleaveOperator
#
#  http://stackoverflow.com/questions/7946798/interleaving-two-lists-in-python
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def interleaveOperator( arg1, arg2 ):
    return [ val for pair in zip( arg1, arg2 ) for val in pair ]


#******************************************************************************
#
#  collateOperator
#
#******************************************************************************

def collate( argList ):
    if not isinstance( argList, list ):
        yield argList
        return

    listOfLists = [ ]
    length = 0

    for arg in argList:
        if isinstance( arg, list ):
            listOfLists.append( arg )
            length = max( len( arg ), length )
        else:
            listOfLists.append( [ arg ] )
            length = max( 1, length )

    for i in range( 0, length ):
        newSubList = [ ]

        for subList in argList:
            newSubList.append( subList[ i ] )

        yield newSubList


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def collateOperator( n ):
    return RPNGenerator( collate( n ) )


#******************************************************************************
#
#  makeUnionOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def makeUnionOperator( arg1, arg2 ):
    result = set( arg1 )
    return list( result.union( set( arg2 ) ) )


#******************************************************************************
#
#  makeIntersectionOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def makeIntersectionOperator( arg1, arg2 ):
    result = set( arg1 )
    return list( result.intersection( set( arg2 ) ) )


#******************************************************************************
#
#  getDifferenceOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def getDifferenceOperator( arg1, arg2 ):
    return list( set( arg2 ) - set( arg1 ) )


#******************************************************************************
#
#  getIndexOfMaxOperator
#
#******************************************************************************

#@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getIndexOfMaxOperator( args ):
    maximum = -inf
    result = -1
    index = 0

    for i in args:
        if i > maximum:
            maximum = i
            result = index

        index += 1

    return result


#******************************************************************************
#
#  getIndexOfMinOperator
#
#******************************************************************************

#@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getIndexOfMinOperator( args ):
    minimum = inf
    result = -1
    index = 0

    for i in args:
        if i < minimum:
            minimum = i
            result = index

        index += 1

    return result


#******************************************************************************
#
#  getListElementOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getListElementOperator( args, index ):
    if isinstance( index, ( list, RPNGenerator ) ):
        result = [ ]

        for i in index:
            result.append( args[ int( i ) ] )

        return result

    return args[ int( index ) ]


#******************************************************************************
#
#  getRandomElementOperator
#
#******************************************************************************

@argValidator( [ ListValidator( ) ] )
def getRandomElementOperator( arg ):
    return random.choice( arg )


#******************************************************************************
#
#  enumerateListGenerator
#
#******************************************************************************

def enumerateListGenerator( args, k ):
    i = 0

    for arg in args:
        yield [ fadd( i, k ), arg ]
        i += 1


@argValidator( [ ListValidator( ), IntValidator( ) ] )
def enumerateListOperator( args, k ):
    return RPNGenerator.createGenerator( enumerateListGenerator, [ args, k ] )


#******************************************************************************
#
#  getSliceGenerator
#
#******************************************************************************

def getSliceGenerator( args, start, end ):
    if end == 0:
        for i in args[ int( start ) : ]:
            yield i
    else:
        for i in args[ int( start ) : int( end ) ]:
            yield i


@listAndTwoArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ), IntValidator( ) ] )
def getSliceOperator( args, start, end ):
    return RPNGenerator.createGenerator( getSliceGenerator, [ args, start, end ] )


#******************************************************************************
#
#  getSublistGenerator
#
#******************************************************************************

def getSublistGenerator( args, start, count ):
    for i in arange( start, fadd( start, count ) ):
        yield args[ int( i ) ]


@listAndTwoArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ), IntValidator( ) ] )
def getSublistOperator( args, start, count ):
    return RPNGenerator.createGenerator( getSublistGenerator, [ args, start, count ] )


#******************************************************************************
#
#  getLeftOperator
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getLeftOperator( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( args[ : int( i ) ] )
    else:
        result.append( args[ : int( count ) ] )

    if len( result ) == 1:
        return result[ 0 ]

    return result


#******************************************************************************
#
#  getRightOperator
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getRightOperator( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( args[ int( fneg( i ) ) : ] )
    else:
        result.append( args[ int( fneg( count ) ) : ] )

    if len( result ) == 1:
        return result[ 0 ]

    return result


#******************************************************************************
#
#  getListDiffsOperator
#
#******************************************************************************

def getListDiffs( args ):
    old = None

    for i in args:
        if old is not None:
            yield subtract( i, old )

        old = i


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListDiffsOperator( n ):
    return RPNGenerator( getListDiffs( n ) )


#******************************************************************************
#
#  getCumulativeListDiffsOperator
#
#******************************************************************************

def getCumulativeListDiffs( args ):
    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield subtract( i, first )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListDiffsOperator( n ):
    return RPNGenerator( getCumulativeListDiffs( n ) )


#******************************************************************************
#
#  getCumulativeListProductsOperator
#
#******************************************************************************

def getCumulativeListProducts( args ):
    total = 1

    for i in args:
        total = multiply( total, i )
        yield total


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListProductsOperator( n ):
    return RPNGenerator( getCumulativeListProducts( n ) )


#******************************************************************************
#
#  getCumulativeListMeansOperator
#
#******************************************************************************

def getCumulativeListMeans( args ):
    mean = None

    for index, i in enumerate( args ):
        if mean is None:
            mean = i
        else:
            mean = fdiv( fadd( fmul( mean, index ), i ), fadd( index, 1 ) )

        yield mean


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListMeansOperator( n ):
    return RPNGenerator( getCumulativeListMeans( n ) )


#******************************************************************************
#
#  getCumulativeListSumsOperator
#
#******************************************************************************

def getCumulativeListSums( args ):
    total = 0

    for i in args:
        total = add( total, i )
        yield total


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListSumsOperator( n ):
    return RPNGenerator( getCumulativeListSums( n ) )


#******************************************************************************
#
#  getListRatiosOperator
#
#******************************************************************************

def getListRatios( args ):
    old = None

    for i in args:
        if old is not None:
            yield divide( i, old )

        old = i


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListRatiosOperator( n ):
    return RPNGenerator( getListRatios( n ) )


#******************************************************************************
#
#  getCumulativeListRatiosOperator
#
#******************************************************************************

def getCumulativeListRatios( args ):
    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield divide( i, first )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListRatiosOperator( n ):
    return RPNGenerator( getCumulativeListRatios( n ) )


#******************************************************************************
#
#  getReverseOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getReverseOperator( args ):
    # These list comprehensions _are_ needed.
    # pylint: disable=unnecessary-comprehension
    return [ i for i in reversed( [ j for j in args ] ) ]


#******************************************************************************
#
#  shuffleListOperator
#
#******************************************************************************

def shuffleList( args ):
    if isinstance( args, RPNGenerator ):
        return shuffleList( list( args ) )

    if not isinstance( args, list ):
        return args

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        result = [ ]

        for arg in args:
            result.append( shuffleList( arg ) )

        return result

    result = args[ : ]
    random.shuffle( result )
    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def shuffleListOperator( n ):
    return shuffleList( n )


#******************************************************************************
#
#  getUniqueElementsOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getUniqueElementsOperator( args ):
    return list( set( args ) )


#******************************************************************************
#
#  sortAscendingOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def sortAscendingOperator( args ):
    result = [ ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        for arg in args:
            result.append( sorted( arg ) )

        return result

    return sorted( args )


#******************************************************************************
#
#  sortDescendingOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def sortDescendingOperator( args ):
    result = [ ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        for arg in args:
            result.append( sorted( arg, reverse = True ) )

        return result

    return sorted( args, reverse = True )


#******************************************************************************
#
#  calculatePowerTowerOperator
#
#******************************************************************************

def calculatePowerTower( args ):
    if isinstance( args, RPNGenerator ):
        return calculatePowerTower( list( args ) )

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ calculatePowerTower( arg ) for arg in args ]

    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculatePowerTowerOperator( n ):
    return calculatePowerTower( n )


#******************************************************************************
#
#  calculatePowerTowerRightOperator
#
#******************************************************************************

def calculatePowerTowerRight( args ):
    if isinstance( args, RPNGenerator ):
        return calculatePowerTowerRight( list( args ) )

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ calculatePowerTowerRight( arg ) for arg in args ]

    result = args[ -1 ]

    for i in args[ -2 : : -1 ]:
        result = power( i, result )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculatePowerTowerRightOperator( n ):
    return calculatePowerTowerRight( n )


#******************************************************************************
#
#  getSumOperator
#
#******************************************************************************

def getSum( n ):
    if isinstance( n, RPNGenerator ):
        return getSum( list( n ) )

    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ getSum( arg ) for arg in n ]

    result = None

    try:
        result = fsum( n )
    except TypeError:
        result = n[ 0 ]

        for i in n[ 1 : ]:
            result = add( result, i )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getSumOperator( n ):
    return getSum( n )


#******************************************************************************
#
#  getProductOperator
#
#******************************************************************************

def getProduct( n ):
    if isinstance( n, RPNGenerator ):
        return getProduct( list( n ) )

    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ getProduct( arg ) for arg in n ]

    if not n:
        return 0

    if len( n ) == 1:
        return n[ 0 ]

    hasUnits = False

    for item in n:
        if isinstance( item, RPNMeasurement ):
            hasUnits = True
            break

    if hasUnits:
        result = RPNMeasurement( 1 )

        for item in n:
            if isinstance( item, list ):
                return [ getProduct( arg ) for arg in item ]

            result = multiply( result, item )

        return result

    if not n:
        return 0

    if isinstance( n[ 0 ], list ):
        return [ getProduct( item ) for item in n ]

    return fprod( n )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getProductOperator( n ):
    return getProduct( n )


#******************************************************************************
#
#  getStandardDeviationOperator
#
#******************************************************************************

def getStandardDeviation( args ):
    if isinstance( args, RPNGenerator ):
        return getStandardDeviation( list( args ) )

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getStandardDeviation( arg ) for arg in args ]

    if len( args ) < 2:
        return 0

    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fdiv( fsum( dev ), fsub( len( dev ), 1 ) ) )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getStandardDeviationOperator( n ):
    return getStandardDeviation( n )


#******************************************************************************
#
#  reduceListOperator
#
#  This function reduces out the greatest common denominator from a list of
#  values.
#
#******************************************************************************

def reduceList( args ):
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ reduceList( arg ) for arg in args ]

    gcd = getGCDOfList( args )

    result = [ ]

    for i in args:
        result.append( fdiv( i, gcd ) )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def reduceListOperator( n ):
    return reduceList( n )


#******************************************************************************
#
#  calculateGeometricMeanOperator
#
#******************************************************************************

def calculateGeometricMean( args ):
    if not isinstance( args, types.GeneratorType ):
        if isinstance( args[ 0 ], ( list, types.GeneratorType ) ):
            return [ calculateGeometricMean( arg ) for arg in args ]

    result = mpmathify( 1 )
    count = 0

    for arg in args:
        print( 'arg', arg, type( arg ) )
        
        result = fmul( result, arg )
        count += 1

    return root( result, count )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateGeometricMeanOperator( n ):
    return calculateGeometricMean( n )


#******************************************************************************
#
#  calculateHarmonicMeanOperator
#
#******************************************************************************

def calculateHarmonicMean( args ):
    if isinstance( args, RPNGenerator ):
        return calculateHarmonicMean( list( args ) )

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateHarmonicMean( list( arg ) ) for arg in args ]

        result = 0

        for arg in args:
            result = fadd( result, fdiv( 1, arg ) )

        return fdiv( len( args ), result )

    return args


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateHarmonicMeanOperator( n ):
    return calculateHarmonicMean( n )


#******************************************************************************
#
#  calculateAntiharmonicMeanOperator
#
# https://en.wikipedia.org/wiki/Contraharmonic_mean
#
#******************************************************************************

def calculateAntiharmonicMean( args ):
    if isinstance( args, RPNGenerator ):
        return calculateAntiharmonicMean( list( args ) )

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateAntiharmonicMean( list( arg ) ) for arg in args ]

        return fdiv( fsum( args, squared=True ), fsum( args ) )

    return args


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateAntiharmonicMeanOperator( n ):
    return calculateAntiharmonicMean( n )


#******************************************************************************
#
#  calculateArithmeticMeanOperator
#
#******************************************************************************

def calculateArithmeticMean( args ):
    if isinstance( args, RPNGenerator ):
        total = 0
        count = 0

        for i in args:
            total += i
            count += 1

        return fdiv( total, count )

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateArithmeticMean( list( arg ) ) for arg in args ]

        if isinstance( args[ 0 ], RPNMeasurement ):
            # TODO: handle measurements
            raise ValueError( '\'mean\' doesn\'t support measurements (yet)' )

        return fdiv( fsum( args ), len( args ) )

    return args


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateArithmeticMeanOperator( n ):
    return calculateArithmeticMean( n )


#******************************************************************************
#
#  calculateRootMeanSquareOperator
#
#******************************************************************************

def calculateRootMeanSquare( args ):
    if isinstance( args, RPNGenerator ):
        total = 0
        count = 0

        for i in args:
            total += power( i, 2 )
            count += 1

        return square( fdiv( total, count ) )

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateRootMeanSquare( list( arg ) ) for arg in args ]

        if isinstance( args[ 0 ], RPNMeasurement ):
            raise ValueError( '\'root_mean_square\' doesn\'t support measurements' )

        return sqrt( fdiv( fsum( args, squared=True ), len( args ) ) )

    return args


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateRootMeanSquareOperator( n ):
    return calculateRootMeanSquare( n )


#******************************************************************************
#
#  getZeroesOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getZeroesOperator( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e == 0 ]

    return [ 0 ] if args == 0 else [ ]


#******************************************************************************
#
#  getNonzeroesOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNonzeroesOperator( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e != 0 ]

    return [ 0 ] if args == 0 else [ ]


#******************************************************************************
#
#  groupElementsOperator
#
#******************************************************************************

def groupElements( args, count ):
    if isinstance( count, list ):
        return [ groupElements( args, i ) for i in count ]

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ groupElements( args, count ) for arg in args ]

        result = [ ]

        n = int( count )

        for i in range( 0, len( args ), n ):
            result.append( args[ i : i + n ] )

        return result

    return [ args ]


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def groupElementsOperator( args, count ):
    return groupElements( args, count )


#******************************************************************************
#
#  getOccurrencesOperator
#
#******************************************************************************

def getOccurrences( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getOccurrences( arg ) for arg in args ]

        counter = collections.Counter( )

        for i in args:
            counter[ i ] += 1

        result = [ ]

        for i in counter:
            result.append( [ i, counter[ i ] ] )

        return sorted( result )

    return [ [ args, 1 ] ]


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOccurrencesOperator( n ):
    return getOccurrences( n )


#******************************************************************************
#
#  getOccurrenceRatiosOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOccurrenceRatiosOperator( args ):
    if isinstance( args, list ):
        count = len( args )

        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getOccurrences( arg ) for arg in args ]

        counter = collections.Counter( )

        for i in args:
            counter[ i ] += 1

        result = [ ]

        for i in counter:
            result.append( [ i, counter[ i ] / count ] )

        return sorted( result )

    return [ [ args, 1 ] ]


#******************************************************************************
#
#  getCumulativeOccurrenceRatiosOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeOccurrenceRatiosOperator( args ):
    if isinstance( args, list ):
        count = len( args )

        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getOccurrences( arg ) for arg in args ]

        counter = collections.Counter( )

        for i in args:
            counter[ i ] += 1

        result = [ ]

        runningTotal = 0
        for i in counter:
            runningTotal += counter[ i ]
            result.append( [ i, runningTotal / count ] )

        return sorted( result )

    return [ [ args, 1 ] ]


#******************************************************************************
#
#  flattenOperator
#
#******************************************************************************

def flatten( value ):
    if isinstance( value, ( list, RPNGenerator ) ):
        result = [ ]

        for item in value:
            result.extend( flatten( item ) )

        return result

    return [ value ]


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def flattenOperator( value ):
    return flatten( value )


#******************************************************************************
#
#  getAndAllOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getAndAllOperator( value ):
    for i in value:
        if not i:
            return 0

    return 1


#******************************************************************************
#
#  getNandAllOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNandAllOperator( value ):
    for i in value:
        if i:
            return 0

    return 1


#******************************************************************************
#
#  getOrAllOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOrAllOperator( value ):
    for i in value:
        if i:
            return 1

    return 0


#******************************************************************************
#
#  getNorAllOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNorAllOperator( value ):
    for i in value:
        if not i:
            return 1

    return 0


#******************************************************************************
#
#  permuteListsOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def permuteListsOperator( lists ):
    for i in lists:
        if not isinstance( i, ( list, RPNGenerator ) ):
            raise ValueError( '\'permute_lists\' expects a list of lists' )

    #for i in RPNGenerator.createProduct( lists ):
    #    yield i

    for item in itertools.product( *lists ):
        yield [ i for i in item ]

#******************************************************************************
#
#  getListCombinationsOperator
#
#******************************************************************************

def getListCombinationsGenerator( n, k ):
    for i in itertools.combinations( n, int( k ) ):
        yield list( i )


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListCombinationsOperator( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    for i in RPNGenerator( getListCombinationsGenerator( n, k ) ):
        yield i


#******************************************************************************
#
#  getListCombinationsWithRepeatsOperator
#
#******************************************************************************

def getListCombinationsWithRepeatsGenerator( n, k ):
    for i in itertools.combinations_with_replacement( n, int( k ) ):
        yield list( i )


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListCombinationsWithRepeatsOperator( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    for i in RPNGenerator( getListCombinationsWithRepeatsGenerator( n, k ) ):
        yield i


#******************************************************************************
#
#  getListPermutationsOperator
#
#******************************************************************************

def getListPermutationsGenerator( n, k ):
    for i in itertools.permutations( n, int( k ) ):
        yield list( i )


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListPermutationsOperator( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'permute_list\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    for i in RPNGenerator( getListPermutationsGenerator( n, k ) ):
        yield i


#******************************************************************************
#
#  getListPermutationsWithRepeatsOperator
#
#******************************************************************************

def getListPermutationsWithRepeatsGenerator( n, k ):
    for i in itertools.product( n, repeat=int( k ) ):
        yield list( i )


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListPermutationsWithRepeatsOperator( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_permutations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    for i in RPNGenerator( getListPermutationsWithRepeatsGenerator( n, k ) ):
        yield i


#******************************************************************************
#
#  equalsOneOfOperator
#
#******************************************************************************

@argValidator( [ ComplexValidator( ), ListValidator( ) ] )
def equalsOneOfOperator( value, targetList ):
    for i in targetList:
        if value == i:
            return 1

    return 0


#******************************************************************************
#
#  getListPowerSetOperator
#
#******************************************************************************

def getListPowerSet( n ):
    for i in getPowerSet( n ):
        if len( i ) > 0:
            yield list( i )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListPowerSetOperator( n ):
    for i in RPNGenerator( getListPowerSet( n ) ):
        yield i


#******************************************************************************

#  findInListOperator
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), DefaultValidator( ) ] )
def findInListOperator( target, k ):
    try:
        result = target.index( k )
    except ValueError:
        return -1

    return result


#******************************************************************************
#
#  isPalindromeListOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def isPalindromeListOperator( n ):
    length = len( n )

    for i in range( 0, length // 2 ):
        if n[ i ] != n[ -( i + 1 ) ]:
            return 0

    return 1


#******************************************************************************
#
#  filterOnFlagsGenerator
#
#******************************************************************************

def filterOnFlagsGenerator( n, k ):
    for nItem, kItem in zip( n, k ):
        if kItem:
            yield nItem


@argValidator( [ ListValidator( ), ListValidator( ) ] )
def filterOnFlagsOperator( n, k ):
    return RPNGenerator.createGenerator( filterOnFlagsGenerator, [ n, k ] )


#******************************************************************************
#
#  filterMaxGenerator
#
#******************************************************************************

def filterMaxGenerator( n, k ):
    for item in n:
        if item <= k:
            yield item


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), ComparableValidator( ) ] )
def filterMaxOperator( n, k ):
    return RPNGenerator.createGenerator( filterMaxGenerator, [ n, k ] )


#******************************************************************************
#
#  filterMinGenerator
#
#******************************************************************************

def filterMinGenerator( n, k ):
    for item in n:
        if item >= k:
            yield item


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), ComparableValidator( ) ] )
def filterMinOperator( n, k ):
    return RPNGenerator.createGenerator( filterMinGenerator, [ n, k ] )


#******************************************************************************
#
#  doesListRepeatOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def doesListRepeatOperator( n ):
    n = list( n )
    length = len( n )

    if length == 0:
        return 0

    for i in range( 1, ( length // 2 ) + 1 ):
        substring = n[ 0 : i ]

        start = i
        end = start + i

        foundRepeats = True

        while end <= length:
            if n[ start : end ] != substring:
                foundRepeats = False
                break

            start += i
            end += i

        if not foundRepeats:
            continue

        # Check the remainder, if there is one.
        if ( start < length ) and \
           ( n[ end - i : length ] != substring[ : length - ( end - i ) ] ):
            foundRepeats = False

        if foundRepeats:
            return i

    return 0
