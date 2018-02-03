#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnList.py
# //
# //  RPN command-line calculator list operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools
import random

from mpmath import arange, fadd, fdiv, fmul, fneg, fprod, fsub, fsum, inf, \
                   power, root, sqrt

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMath import add, subtract, divide
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnNumberTheory import getGCDOfList
from rpn.rpnUtils import listAndOneArgFunctionEvaluator, listAndTwoArgFunctionEvaluator, \
                         listArgFunctionEvaluator


# //******************************************************************************
# //
# //  alternateSigns
# //
# //******************************************************************************

def alternateSigns( n, startNegative = False ):
    negative = startNegative

    for i in n:
        yield fneg( i ) if negative else i
        negative = not negative


# //******************************************************************************
# //
# //  getAlternatingSum
# //
# //******************************************************************************

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

def countElements( args ):
    if isinstance( args, list ):
        return len( args )
    elif isinstance( args, RPNGenerator ) and args.getCount( ) > -1:
        return args.getCount( )

    count = 0

    for i in args:
        count += 1

    return count


# //******************************************************************************
# //
# //  interleave
# //
# //  http://stackoverflow.com/questions/7946798/interleaving-two-lists-in-python
# //
# //******************************************************************************

def interleave( arg1, arg2 ):
    return [ val for pair in zip( arg1, arg2 ) for val in pair ]


# //******************************************************************************
# //
# //  collate
# //
# //******************************************************************************

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
# //  getDifference
# //
# //******************************************************************************

def getDifference( arg1, arg2 ):
    return list( set( arg2 ) - set( arg1 ) )


# //******************************************************************************
# //
# //  getIndexOfMax
# //
# //******************************************************************************

#@listArgFunctionEvaluator( )
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


# //******************************************************************************
# //
# //  getIndexOfMin
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getListElement
# //
# //******************************************************************************

def getListElement( args, index ):
    if isinstance( index, ( list, RPNGenerator ) ):
        for i in index:
            return args[ int( i ) ]
    else:
        return args[ int( index ) ]


# //******************************************************************************
# //
# //  enumerateListGenerator
# //
# //******************************************************************************

def enumerateListGenerator( args, k ):
    i = 0

    for arg in args:
        yield [ fadd( i, k ), arg ]
        i += 1

def enumerateList( args, k ):
    return RPNGenerator.createGenerator( enumerateListGenerator, [ args, k ] )


# //******************************************************************************
# //
# //  getSliceGenerator
# //
# //******************************************************************************

def getSliceGenerator( args, start, end ):
    if end == 0:
        for i in args[ int( start ) : ]:
            yield i
    else:
        for i in args[ int( start ) : int( end ) ]:
            yield i

@listAndTwoArgFunctionEvaluator( )
def getSlice( args, start, end ):
    return RPNGenerator.createGenerator( getSliceGenerator, [ args, start, end ] )


# //******************************************************************************
# //
# //  getSublistGenerator
# //
# //******************************************************************************

def getSublistGenerator( args, start, count ):
    for i in arange( start, fadd( start, count ) ):
        yield args[ int( i ) ]

@listAndTwoArgFunctionEvaluator( )
def getSublist( args, start, count ):
    return RPNGenerator.createGenerator( getSublistGenerator, [ args, start, count ] )


# //******************************************************************************
# //
# //  getLeft
# //
# //******************************************************************************

def getLeft( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( [ j for j in args ][ : int( i ) ] )
    else:
        result.append( [ j for j in args ][ : int( count ) ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


# //******************************************************************************
# //
# //  getRight
# //
# //******************************************************************************

def getRight( args, count ):
    result = [ ]

    if isinstance( count, list ):
        for i in count:
            result.append( [ j for j in args ][ int( fneg( i ) ) : ] )
    else:
        result.append( [ j for j in args ][ int( fneg( count ) ) : ] )

    if len( result ) == 1:
        return result[ 0 ]
    else:
        return result


# //******************************************************************************
# //
# //  getListDiffs
# //
# //******************************************************************************

def getListDiffs( args ):
    old = None

    for i in args:
        if old is not None:
            yield( subtract( i, old ) )

        old = i


# //******************************************************************************
# //
# //  getCumulativeListDiffs
# //
# //******************************************************************************

def getCumulativeListDiffs( args ):
    result = [ ]

    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield subtract( i, first )


# //******************************************************************************
# //
# //  getListRatios
# //
# //******************************************************************************

def getListRatios( args ):
    old = None

    for i in args:
        if old is not None:
            yield( divide( i, old ) )

        old = i


# //******************************************************************************
# //
# //  getCumulativeListRatios
# //
# //******************************************************************************

def getCumulativeListRatios( args ):
    result = [ ]

    first = None

    for i in args:
        if first is None:
            first = i
        else:
            yield divide( i, first )


# //******************************************************************************
# //
# //  getReverse
# //
# //******************************************************************************

def getReverse( args ):
    return [ i for i in reversed( [ j for j in args ] ) ]


# //******************************************************************************
# //
# //  shuffleList
# //
# //******************************************************************************

def shuffleList( args ):
    if isinstance( args, RPNGenerator ):
        return shuffleList( list( args ) )
    elif not isinstance( args, list ):
        return args
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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
    if isinstance( args, RPNGenerator ):
        return calculatePowerTower( list( args ) )
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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
    if isinstance( args, RPNGenerator ):
        return calculatePowerTower2( list( args ) )
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
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
    if isinstance( n, RPNGenerator ):
        return getSum( list( n ) )
    elif isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ getSum( arg ) for arg in n ]

    result = None

    for i in n:
        if result is None:
            result = i
        else:
            result = add( result, i )

    return result


# //******************************************************************************
# //
# //  getProduct
# //
# //******************************************************************************

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
        result = RPNMeasurement( 1, { } )

        for item in n:
            if isinstance( item, list ):
                return [ getProduct( arg ) for arg in item ]

            result = result.multiply( item )

        return result
    else:
        if not n:
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
    if isinstance( args, RPNGenerator ):
        return getStandardDeviation( list( args ) )
    elif isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getStandardDeviation( arg ) for arg in args ]

    if len( args ) < 2:
        return 0

    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fdiv( fsum( dev ), fsub( len( dev ), 1 ) ) )


# //******************************************************************************
# //
# //  reduceList
# //
# //  This function reduces out the greatest common denominator from a list of
# //  values.
# //
# //******************************************************************************

def reduceList( args ):
    if isinstance( args, RPNGenerator ):
        return reduceList( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ reduceList( arg ) for arg in args ]
        else:
            gcd = getGCDOfList( args )

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
    if isinstance( args, RPNGenerator ):
        return calculateGeometricMean( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateGeometricMean( list( arg ) ) for arg in args ]
        else:
            return root( fprod( args ), len( args ) )
    else:
        return args


# //******************************************************************************
# //
# //  calculateHarmonicMean
# //
# //******************************************************************************

def calculateHarmonicMean( args ):
    if isinstance( args, RPNGenerator ):
        return calculateHarmonicMean( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ calculateHarmonicMean( list( arg ) ) for arg in args ]
        else:
            sum = 0

            for arg in args:
                sum = fadd( sum, fdiv( 1, arg ) )

            return fdiv( len( args ), sum )
    else:
        return args


# //******************************************************************************
# //
# //  calculateArithmeticMean
# //
# //******************************************************************************

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
            pass # TODO: handle measurements
        else:
            return fdiv( fsum( args ), len( args ) )
    else:
        return args


# //******************************************************************************
# //
# //  getZeroes
# //
# //******************************************************************************

def getZeroes( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e == 0 ]
    else:
        return [ 0 ] if args == 0 else [ ]


# //******************************************************************************
# //
# //  getNonzeroes
# //
# //******************************************************************************

def getNonzeroes( args ):
    if isinstance( args, ( RPNGenerator, list ) ):
        return [ index for index, e in enumerate( args ) if e != 0 ]
    else:
        return [ 0 ] if args == 0 else [ ]


# //******************************************************************************
# //
# //  groupElements
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getOccurrences
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getOccurrenceRatios
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getCumulativeOccurrenceRatios
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  flatten
# //
# //******************************************************************************

def flatten( value ):
    if isinstance( value, ( list, RPNGenerator ) ):
        result = [ ]

        for item in value:
            result.extend( flatten( item ) )

        return result
    else:
        return [ value ]


# //******************************************************************************
# //
# //  getAndAll
# //
# //******************************************************************************

def getAndAll( value ):
    for i in value:
        if not i:
            return 0

    return 1


# //******************************************************************************
# //
# //  getNandAll
# //
# //******************************************************************************

def getNandAll( value ):
    for i in value:
        if i:
            return 0

    return 1


# //******************************************************************************
# //
# //  getOrAll
# //
# //******************************************************************************

def getOrAll( value ):
    for i in value:
        if i:
            return 1

    return 0


# //******************************************************************************
# //
# //  getNorAll
# //
# //******************************************************************************

def getNorAll( value ):
    for i in value:
        if not i:
            return 1

    return 0


# //******************************************************************************
# //
# //  permuteLists
# //
# //******************************************************************************

def permuteLists( lists ):
    for i in lists:
        if not isinstance( i, ( list, RPNGenerator ) ):
            raise ValueError( '\'permute_lists\' expects a list of lists' )

    return RPNGenerator.createProduct( lists )


# //******************************************************************************
# //
# //  getListCombinationsGenerator
# //
# //******************************************************************************

def getListCombinationsGenerator( n, k ):
    for i in itertools.combinations( n, int( k ) ):
        yield list( i )


# //******************************************************************************
# //
# //  getListCombinations
# //
# //******************************************************************************

def getListCombinations( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListCombinationsGenerator( n, k ) )


# //******************************************************************************
# //
# //  getListCombinationsWithRepeatsGenerator
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def getListCombinationsWithRepeatsGenerator( n, k ):
    for i in itertools.combinations_with_replacement( n, int( k ) ):
        yield list( i )


# //******************************************************************************
# //
# //  getListCombinationsWithRepeats
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def getListCombinationsWithRepeats( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_combinations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListCombinationsWithRepeatsGenerator( n, k ) )


# //******************************************************************************
# //
# //  getListPermutationsGenerator
# //
# //******************************************************************************

def getListPermutationsGenerator( n, k ):
    for i in itertools.permutations( n, int( k ) ):
        yield list( i )


# //******************************************************************************
# //
# //  getListPermutations
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def getListPermutations( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'permute_list\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListPermutationsGenerator( n, k ) )


# //******************************************************************************
# //
# //  getListPermutationsWithRepeatsGenerator
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def getListPermutationsWithRepeatsGenerator( n, k ):
    for i in itertools.product( n, repeat=int( k ) ):
        yield list( i )


# //******************************************************************************
# //
# //  getListPermutationsWithRepeats
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def getListPermutationsWithRepeats( n, k ):
    if not isinstance( n, ( list, RPNGenerator ) ):
        raise ValueError( '\'get_repeat_permutations\' expects a list' )

    if len( n ) < k:
        raise ValueError( 'k must be greater than or equal to the length of list n' )

    return RPNGenerator( getListPermutationsWithRepeatsGenerator( n, k ) )


# //******************************************************************************
# //
# //  equalsOneOf
# //
# //******************************************************************************

# rpn 1 1000 primes lambda x 40 mod [ 7 19 23 ] equals_one_of x 1 - 2 / is_prime and filter

def equalsOneOf( value, targetList ):
    for i in targetList:
        if value == i:
            return 1

    return 0


# //******************************************************************************
# //
# //  getPowerset
# //
# //******************************************************************************

def getPowerset( n ):
    for i in itertools.chain.from_iterable( itertools.combinations( n, r ) for r in range( len( n ) + 1 ) ):
        if len( i ) > 0:
            yield list( i )


# //******************************************************************************
# //
# //  findInList
# //
# //******************************************************************************

@listAndOneArgFunctionEvaluator( )
def findInList( target, k ):
    try:
        result = k.index( target )
    except:
        return -1

    return result


# //******************************************************************************
# //
# //  isPalindromeList
# //
# //******************************************************************************

def isPalindromeList( n ):
    length = len( n )

    for i in range( 0, length // 2 ):
        if n[ i ] != n[ -( i + 1 ) ]:
            return 0

    return 1

