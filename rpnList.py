#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnList.py
# //
# //  RPN command-line calculator list operators
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools
import random

from mpmath import arange, fadd, fdiv, fneg, fprod, fsub, fsum, inf, power, \
                   root, sqrt

from rpnGenerator import RPNGenerator
from rpnMath import add, subtract, divide
from rpnMeasurement import RPNMeasurement
from rpnNumberTheory import getGCD


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
        return argList

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
# //  getIndexOfMax
# //
# //******************************************************************************

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
            yield args[ int( i ) ]
    else:
        yield args[ int( index ) ]


# //******************************************************************************
# //
# //  enumerateList
# //
# //******************************************************************************

def enumerateList( args, k ):
    i = 0

    for arg in args:
        yield [ fadd( i, k ), arg ]
        i += 1


# //******************************************************************************
# //
# //  getSlice
# //
# //******************************************************************************

def getSlice( args, start, end ):
    for i in range( int( start ), int( end + 1 ) ):
        yield args[ i ]


# //******************************************************************************
# //
# //  getSublist
# //
# //******************************************************************************

def getSublist( args, start, count ):
    for i in arange( start, fadd( count, 1 ) ):
        yield args[ int( i ) ]


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
    if isinstance( args, RPNGenerator ):
        return reduceList( list( args ) )
    elif isinstance( args, list ):
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
# //  getOccurrenceRatios
# //
# //******************************************************************************

def getOccurrenceRatios( args ):
    if isinstance( args, list ):
        count = len( args )

        if isinstance( args[ 0 ], list ):
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

        if isinstance( args[ 0 ], list ):
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
# //  forEach
# //
# //******************************************************************************

def forEach( list, func ):
    for i in list:
        yield func( *i )

