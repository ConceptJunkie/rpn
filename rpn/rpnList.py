#!/usr/bin/env python

#******************************************************************************
#
#  rpnList.py
#
#  rpnChilada list operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import collections
import itertools
import random

from mpmath import arange, fadd, fdiv, fmod, fmul, fneg, fprod, fsub, fsum, inf, \
                   power, root, sqrt

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMath import add, multiply, square, subtract, divide
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnUtils import getPowerSet, listArgFunctionEvaluator, listAndOneArgFunctionEvaluator, \
                         listAndTwoArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, DefaultValidator, IntValidator, ListValidator, \
                             RealOrMeasurementOrDateTimeValidator


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
#  getGCDOfList
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getGCDOfList( args ):
    if isinstance( args, RPNGenerator ):
        args = list( args )
    if not isinstance( args, list ):
        args = [ args ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getGCDOfList( arg ) for arg in args ]
    else:
        result = set( )

        if len( args ) == 1:
            return args[ 0 ]

        for pair in itertools.combinations( args, 2 ):
            result.add( getGCD( *pair ) )

        if len( result ) == 1:
            return result.pop( )
        else:
            return getGCDOfList( list( result ) )


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
    return alternateSigns( n, False )

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def alternateSigns2Operator( n ):
    return alternateSigns( n, True )


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

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def appendLists( arg1, arg2 ):
    result = list( arg1 )
    result.extend( list( arg2 ) )

    return result

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def appendListsOperator( n, k ):
    return appendLists( n, k )


#******************************************************************************
#
#  compareLists
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def compareLists( arg1, arg2 ):
    if len( arg1 ) != len( arg2 ):
        return 0

    for i, arg in enumerate( arg1 ):
        if arg != arg2[ i ]:
            return 0

    return 1


#******************************************************************************
#
#  countElements
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def countElements( args ):
    if isinstance( args, list ):
        return len( args )
    elif isinstance( args, RPNGenerator ) and args.getCount( ) > -1:
        return args.getCount( )

    # args might be a generator, so we need to iterate
    count = 0

    for _ in args:
        count += 1

    return count


#******************************************************************************
#
#  interleave
#
#  http://stackoverflow.com/questions/7946798/interleaving-two-lists-in-python
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def interleave( arg1, arg2 ):
    return [ val for pair in zip( arg1, arg2 ) for val in pair ]


#******************************************************************************
#
#  collate
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def collate( argList ):
    if not isinstance( argList, list ):
        yield argList
        return

    listOfLists = [ ]
    length = 0

    for arg in argList:
        if isinstance( arg, list ):
            listOfLists.append( arg )

            if length < len( arg ):
                length = len( arg )
        else:
            listOfLists.append( [ arg ] )

            if length < 1:
                length = 1

    for i in range( 0, length ):
        newSubList = [ ]

        for subList in argList:
            newSubList.append( subList[ i ] )

        yield newSubList


#******************************************************************************
#
#  makeUnion
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def makeUnion( arg1, arg2 ):
    result = set( arg1 )
    return list( result.union( set( arg2 ) ) )


#******************************************************************************
#
#  makeIntersection
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def makeIntersection( arg1, arg2 ):
    result = set( arg1 )
    return list( result.intersection( set( arg2 ) ) )


#******************************************************************************
#
#  getDifference
#
#******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def getDifference( arg1, arg2 ):
    return list( set( arg2 ) - set( arg1 ) )


#******************************************************************************
#
#  getIndexOfMax
#
#******************************************************************************

#@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getIndexOfMax( args ):
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
#  getIndexOfMin
#
#******************************************************************************

#@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getIndexOfMin( args ):
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
#  getListElement
#
#******************************************************************************

@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getListElement( args, index ):
    if isinstance( index, ( list, RPNGenerator ) ):
        for i in index:
            return args[ int( i ) ]
    else:
        return args[ int( index ) ]


#******************************************************************************
#
#  getRandomElement
#
#******************************************************************************

@argValidator( [ ListValidator( ) ] )
def getRandomElement( arg ):
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
def enumerateList( args, k ):
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
def getSlice( args, start, end ):
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
def getSublist( args, start, count ):
    return RPNGenerator.createGenerator( getSublistGenerator, [ args, start, count ] )


#******************************************************************************
#
#  getLeft
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getLeft( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( args[ : int( i ) ] )
    else:
        result.append( args[ : int( count ) ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


#******************************************************************************
#
#  getRight
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( ) ] )
def getRight( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( args[ int( fneg( i ) ) : ] )
    else:
        result.append( args[ int( fneg( count ) ) : ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


#******************************************************************************
#
#  getListDiffs
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListDiffs( args ):
    old = None

    for i in args:
        if old is not None:
            yield subtract( i, old )

        old = i


#******************************************************************************
#
#  getCumulativeListDiffs
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListDiffs( args ):
    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield subtract( i, first )


#******************************************************************************
#
#  getCumulativeListProducts
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListProducts( args ):
    sum = 1

    for i in args:
        sum = multiply( sum, i )
        yield sum


#******************************************************************************
#
#  getCumulativeListSums
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListSums( args ):
    sum = 0

    for i in args:
        sum = add( sum, i )
        yield sum


#******************************************************************************
#
#  getListRatios
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListRatios( args ):
    old = None

    for i in args:
        if old is not None:
            yield divide( i, old )

        old = i


#******************************************************************************
#
#  getCumulativeListRatios
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeListRatios( args ):
    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield divide( i, first )


#******************************************************************************
#
#  getReverse
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getReverse( args ):
    # These list comprehensions _are_ needed.
    # pylint: disable=unnecessary-comprehension
    return [ i for i in reversed( [ j for j in args ] ) ]


#******************************************************************************
#
#  shuffleList
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def shuffleList( args ):
    if isinstance( args, RPNGenerator ):
        return shuffleList( list( args ) )
    elif not isinstance( args, list ):
        return args
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        result = [ ]

        for arg in args:
            result.append( shuffleList( arg ) )

        return result
    else:
        result = args[ : ]
        random.shuffle( result )
        return result


#******************************************************************************
#
#  getUniqueElements
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getUniqueElements( args ):
    return list( set( args ) )


#******************************************************************************
#
#  sortAscending
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def sortAscending( args ):
    result = [ ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        for arg in args:
            result.append( sorted( arg ) )

        return result
    else:
        return sorted( args )


#******************************************************************************
#
#  sortDescending
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def sortDescending( args ):
    result = [ ]

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        for arg in args:
            result.append( sorted( arg, reverse = True ) )

        return result
    else:
        return sorted( args, reverse = True )


#******************************************************************************
#
#  calculatePowerTowerOperator
#
#******************************************************************************

def calculatePowerTower( args ):
    if isinstance( args, RPNGenerator ):
        return calculatePowerTower( list( args ) )
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ calculatePowerTower( arg ) for arg in args ]

    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculatePowerTowerOperator( args ):
    return calculatePowerTower( args )


#******************************************************************************
#
#  calculatePowerTower2Operator
#
#******************************************************************************

def calculatePowerTower2( args ):
    if isinstance( args, RPNGenerator ):
        return calculatePowerTower2( list( args ) )
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ calculatePowerTower2( arg ) for arg in args ]

    result = args[ -1 ]

    for i in args[ -2 : : -1 ]:
        result = power( i, result )

    return result

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculatePowerTower2Operator( args ):
    return calculatePowerTower2( args )


#******************************************************************************
#
#  getSum
#
#******************************************************************************

def getSum( n ):
    if isinstance( n, RPNGenerator ):
        return getSum( list( n ) )
    elif isinstance( n[ 0 ], ( list, RPNGenerator ) ):
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
    elif isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ getProduct( arg ) for arg in n ]

    if not n:
        return 0
    elif len( n ) == 1:
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
    else:
        if not n:
            return 0

        if isinstance( n[ 0 ], list ):
            return [ getProduct( item ) for item in n ]
        else:
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
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getStandardDeviation( arg ) for arg in args ]

    if len( args ) < 2:
        return 0

    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fdiv( fsum( dev ), fsub( len( dev ), 1 ) ) )

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getStandardDeviationOperator( args ):
    return getStandardDeviation( args )

#******************************************************************************
#
#  reduceList
#
#  This function reduces out the greatest common denominator from a list of
#  values.
#
#******************************************************************************

def reduceList( args ):
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ reduceList( arg ) for arg in args ]
    else:
        gcd = getGCDOfList( args )

        result = [ ]

        for i in args:
            result.append( fdiv( i, gcd ) )

        return result

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def reduceListOperator( args ):
    return reduceList( args )


#******************************************************************************
#
#  calculateGeometricMean
#
#******************************************************************************

def calculateGeometricMean( args ):
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ calculateGeometricMean( list( arg ) ) for arg in args ]
    else:
        return root( fprod( args ), len( args ) )

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateGeometricMeanOperator( args ):
    return calculateGeometricMean( args )


#******************************************************************************
#
#  calculateHarmonicMean
#
#******************************************************************************

def calculateHarmonicMean( args ):
    if isinstance( args, RPNGenerator ):
        return calculateHarmonicMean( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateHarmonicMean( list( arg ) ) for arg in args ]
        else:
            result = 0

            for arg in args:
                result = fadd( result, fdiv( 1, arg ) )

            return fdiv( len( args ), result )
    else:
        return args

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateHarmonicMeanOperator( args ):
    return calculateHarmonicMean( args )


#******************************************************************************
#
#  calculateAntiharmonicMean
#
# https://en.wikipedia.org/wiki/Contraharmonic_mean
#
#******************************************************************************

def calculateAntiharmonicMean( args ):
    if isinstance( args, RPNGenerator ):
        return calculateAntiharmonicMean( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateAntiharmonicMean( list( arg ) ) for arg in args ]
        else:
            return fdiv( fsum( args, squared=True ), fsum( args ) )
    else:
        return args

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateAntiharmonicMeanOperator( args ):
    return calculateAntiharmonicMean( args )


#******************************************************************************
#
#  calculateArithmeticMean
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
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateArithmeticMean( list( arg ) ) for arg in args ]
        elif isinstance( args[ 0 ], RPNMeasurement ):
            # TODO: handle measurements
            raise ValueError( '\'mean\' doesn\'t support measurements' )
        else:
            return fdiv( fsum( args ), len( args ) )
    else:
        return args

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateArithmeticMeanOperator( args ):
    return calculateArithmeticMean( args )


#******************************************************************************
#
#  calculateRootMeanSquare
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
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateRootMeanSquare( list( arg ) ) for arg in args ]
        elif isinstance( args[ 0 ], RPNMeasurement ):
            # TODO: handle measurements
            raise ValueError( '\'root_mean_square\' doesn\'t support measurements' )
        else:
            return sqrt( fdiv( fsum( args, squared=True ), len( args ) ) )
    else:
        return args

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def calculateRootMeanSquareOperator( args ):
    return calculateRootMeanSquare( args )


#******************************************************************************
#
#  getZeroes
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getZeroes( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e == 0 ]
    else:
        return [ 0 ] if args == 0 else [ ]


#******************************************************************************
#
#  getNonzeroes
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNonzeroes( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e != 0 ]
    else:
        return [ 0 ] if args == 0 else [ ]


#******************************************************************************
#
#  groupElements
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def groupElements( args, count ):
    if isinstance( count, list ):
        return [ groupElements( args, i ) for i in count ]
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ groupElements( args, count ) for arg in args ]
        else:
            result = [ ]

            n = int( count )

            for i in range( 0, len( args ), n ):
                result.append( args[ i : i + n ] )

            return result
    else:
        return [ args ]


#******************************************************************************
#
#  getOccurrences
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOccurrences( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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


#******************************************************************************
#
#  getOccurrenceRatios
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOccurrenceRatios( args ):
    if isinstance( args, list ):
        count = len( args )

        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getOccurrences( arg ) for arg in args ]
        else:
            counter = collections.Counter( )

            for i in args:
                counter[ i ] += 1

            result = [ ]

            for i in counter:
                result.append( [ i, counter[ i ] / count ] )

            return sorted( result )

    else:
        return [ [ args, 1 ] ]


#******************************************************************************
#
#  getCumulativeOccurrenceRatios
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getCumulativeOccurrenceRatios( args ):
    if isinstance( args, list ):
        count = len( args )

        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getOccurrences( arg ) for arg in args ]
        else:
            counter = collections.Counter( )

            for i in args:
                counter[ i ] += 1

            result = [ ]

            runningTotal = 0
            for i in counter:
                runningTotal += counter[ i ]
                result.append( [ i, runningTotal / count ] )

            return sorted( result )

    else:
        return [ [ args, 1 ] ]


#******************************************************************************
#
#  flatten
#
#******************************************************************************

def flatten( value ):
    if isinstance( value, ( list, RPNGenerator ) ):
        result = [ ]

        for item in value:
            result.extend( flatten( item ) )

        return result
    else:
        return [ value ]


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def flattenOperator( value ):
    return flatten( value )


#******************************************************************************
#
#  getAndAll
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getAndAll( value ):
    for i in value:
        if not i:
            return 0

    return 1


#******************************************************************************
#
#  getNandAll
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNandAll( value ):
    for i in value:
        if i:
            return 0

    return 1


#******************************************************************************
#
#  getOrAll
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getOrAll( value ):
    for i in value:
        if i:
            return 1

    return 0


#******************************************************************************
#
#  getNorAll
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getNorAll( value ):
    for i in value:
        if not i:
            return 1

    return 0


#******************************************************************************
#
#  permuteLists
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def permuteLists( lists ):
    for i in lists:
        if not isinstance( i, ( list, RPNGenerator ) ):
            raise ValueError( '\'permute_lists\' expects a list of lists' )

    return RPNGenerator.createProduct( lists )


#******************************************************************************
#
#  getListCombinationsGenerator
#
#******************************************************************************

def getListCombinationsGenerator( n, k ):
    for i in itertools.combinations( n, int( k ) ):
        yield list( i )


#******************************************************************************
#
#  getListCombinations
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListCombinations( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListCombinationsGenerator( n, k ) )


#******************************************************************************
#
#  getListCombinationsWithRepeatsGenerator
#
#******************************************************************************

def getListCombinationsWithRepeatsGenerator( n, k ):
    for i in itertools.combinations_with_replacement( n, int( k ) ):
        yield list( i )

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListCombinationsWithRepeats( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListCombinationsWithRepeatsGenerator( n, k ) )


#******************************************************************************
#
#  getListPermutationsGenerator
#
#******************************************************************************

def getListPermutationsGenerator( n, k ):
    for i in itertools.permutations( n, int( k ) ):
        yield list( i )

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListPermutations( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'permute_list\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListPermutationsGenerator( n, k ) )


#******************************************************************************
#
#  getListPermutationsWithRepeatsGenerator
#
#******************************************************************************

def getListPermutationsWithRepeatsGenerator( n, k ):
    for i in itertools.product( n, repeat=int( k ) ):
        yield list( i )

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def getListPermutationsWithRepeats( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_permutations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListPermutationsWithRepeatsGenerator( n, k ) )


#******************************************************************************
#
#  equalsOneOf
#
#******************************************************************************

# rpn 1 1000 primes lambda x 40 mod [ 7 19 23 ] equals_one_of x 1 - 2 / is_prime and filter

def equalsOneOf( value, targetList ):
    for i in targetList:
        if value == i:
            return 1

    return 0


#******************************************************************************
#
#  getListPowerSet
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getListPowerSet( n ):
    for i in getPowerSet( n ):
        if len( i ) > 0:
            yield list( i )


#******************************************************************************
#
#  findInList
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), DefaultValidator( ) ] )
def findInList( target, k ):
    try:
        result = k.index( target )
    except AttributeError:
        return -1

    return result


#******************************************************************************
#
#  isPalindromeList
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def isPalindromeList( n ):
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

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def filterOnFlagsGenerator( n, k ):
    for nItem, kItem in zip( n, k ):
        if kItem:
            yield nItem

def filterOnFlags( n, k ):
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
@argValidator( [ ListValidator( ), RealOrMeasurementOrDateTimeValidator( ) ] )
def filterMax( n, k ):
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
@argValidator( [ ListValidator( ), RealOrMeasurementOrDateTimeValidator( ) ] )
def filterMin( n, k ):
    return RPNGenerator.createGenerator( filterMinGenerator, [ n, k ] )


#******************************************************************************
#
#  doesListRepeat
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def doesListRepeat( n ):
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

