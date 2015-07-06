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

from mpmath import *

from rpnDeclarations import *
from rpnMeasurement import *


# //******************************************************************************
# //
# //  alternateSigns
# //
# //******************************************************************************

def alternateSigns( n ):
    for i in range( 1, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


# //******************************************************************************
# //
# //  alternateSigns2
# //
# //******************************************************************************

def alternateSigns2( n ):
    for i in range( 0, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


# //******************************************************************************
# //
# //  appendLists
# //
# //******************************************************************************

def appendLists( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = [ ]

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    return result


# //******************************************************************************
# //
# //  expandRange
# //
# //******************************************************************************

def expandRange( start, end ):
    if start > end:
        step = -1
    else:
        step = 1

    result = list( )

    for i in arange( start, end + step, step ):
        result.append( i )

    return result


# //******************************************************************************
# //
# //  expandSteppedRange
# //
# //******************************************************************************

def expandSteppedRange( start, end, step ):
    result = list( )

    for i in arange( start, end + 1, step ):
        result.append( i )

    return result


# //******************************************************************************
# //
# //  expandGeometricRange
# //
# //******************************************************************************

def expandGeometricRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = fmul( value, step )

    return result


# //******************************************************************************
# //
# //  expandExponentialRange
# //
# //******************************************************************************

def expandExponentialRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = power( value, step )

    return result


# //******************************************************************************
# //
# //  interleave
# //
# //******************************************************************************

def interleave( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            combined = list( zip( arg1, arg2  ) )
            combined = [ item for sublist in combined for item in sublist ]

            for i in combined:
                result.append( i )
        else:
            for i in arg1:
                result.append( i )
                result.append( arg2 )
    else:
        if list2:
            for i in arg2:
                result.append( arg1 )
                result.append( i )
        else:
            result.append( arg1 )
            result.append( arg2 )

    return result


# //******************************************************************************
# //
# //  makeUnion
# //
# //******************************************************************************

def makeUnion( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    return result


# //******************************************************************************
# //
# //  makeIntersection
# //
# //******************************************************************************

def makeIntersection( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            for i in arg1:
                if i in arg2:
                    result.append( i )
        else:
            if arg2 in arg1:
                result.append( arg2 )
    else:
        if list2:
            if arg1 in arg2:
                result.append( arg1 )
        else:
            if arg1 == arg2:
                result.append( arg1 )

    return result


# //******************************************************************************
# //
# //  getIndexOfMax
# //
# //******************************************************************************

def getIndexOfMax( arg ):
    if isinstance( arg[ 0 ], list ):
        return [ getIndexOfMax( item ) for item in arg ]

    maximum = -inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] > maximum:
            maximum = arg[ i ]
            index = i

    return index


# //******************************************************************************
# //
# //  getIndexOfMin
# //
# //******************************************************************************

def getIndexOfMin( arg ):
    if isinstance( arg[ 0 ], list ):
        return [ getIndexOfMin( item ) for item in arg ]

    minimum = inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] < minimum:
            minimum = arg[ i ]
            index = i

    return index


# //******************************************************************************
# //
# //  getListElement
# //
# //******************************************************************************

def getListElement( arg, index ):
    if isinstance( arg, list ):
        return arg[ int( index ) ]
    else:
        return arg
        # TODO: throw exception if index > 0


# //******************************************************************************
# //
# //  getSlice
# //
# //******************************************************************************

def getSlice( arg, start, end ):
    if isinstance( arg, list ):
        slist = isinstance( start, list )
        elist = isinstance( end, list )

        if slist:
            if elist:
                return [ getSlice( arg, i, j ) for i in start for j in end ]
            else:
                return [ getSlice( arg, i, end ) for i in start ]
        else:
            if elist:
                return [ getSlice( arg, start, i ) for i in end ]
            else:
                return arg[ int( start ) : int( end ) ]
    else:
        return arg
        # TODO: raise an exception for slicing a non-list


# //******************************************************************************
# //
# //  getSublist
# //
# //******************************************************************************

def getSublist( arg, start, count ):
    if isinstance( arg, list ):
        slist = isinstance( start, list )
        clist = isinstance( count, list )

        if slist:
            if clist:
                return [ getSublist( arg, i, j ) for i in start for j in count ]
            else:
                return [ getSublist( arg, i, count ) for i in start ]
        else:
            if clist:
                return [ getSublist( arg, start, i ) for i in count ]
            else:
                return arg[ int( start ) : int( start + count ) ]
    else:
        return arg
        # TODO: raise an exception for sublisting a non-list


# //******************************************************************************
# //
# //  getLeft
# //
# //******************************************************************************

def getLeft( arg, count ):
    if isinstance( arg, list ):
        if isinstance( count, list ):
            return [ getLeft( arg, i ) for i in count ]
        else:
            return arg[ : int( count ) ]
    else:
        return arg
        # TODO: raise an exception for slicing a non-list


# //******************************************************************************
# //
# //  getRight
# //
# //******************************************************************************

def getRight( arg, count ):
    if isinstance( arg, list ):
        if isinstance( count, list ):
            return [ getRight( arg, i ) for i in count ]
        else:
            return arg[ len( arg ) - int( count ) : ]
    else:
        return arg
        # TODO: raise an exception for slicing a non-list


# //******************************************************************************
# //
# //  countElements
# //
# //******************************************************************************

def countElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( countElements( args[ i ] ) )

        return result
    else:
        return len( args )


# //******************************************************************************
# //
# //  getListDiffs
# //
# //******************************************************************************

def getListDiffs( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListDiffs( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fsub( args[ i + 1 ], args[ i ] ) )

    return result


# //******************************************************************************
# //
# //  getListDiffsFromFirst
# //
# //******************************************************************************

def getListDiffsFromFirst( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListDiffsFromFirst( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fsub( args[ i + 1 ], args[ 0 ] ) )

    return result


# //******************************************************************************
# //
# //  getListRatios
# //
# //******************************************************************************

def getListRatios( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListRatios( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fdiv( args[ i + 1 ], args[ i ] ) )

    return result


# //******************************************************************************
# //
# //  getReverse
# //
# //******************************************************************************

def getReverse( args ):
    return [ arg for arg in reversed( args ) ]


# //******************************************************************************
# //
# //  getUniqueElements
# //
# //******************************************************************************

def getUniqueElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( getUniqueElements( args[ i ] ) )

    else:
        seen = set( )

        for i in range( 0, len( args ) ):
            seen.add( args[ i ] )

        result = [ ]

        for i in seen:
            result.append( i )

    return result


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
            result.append( sorted( args[ i ], reverse=True ) )

        return result
    else:
        return sorted( args, reverse=True )


# //******************************************************************************
# //
# //  calculatePowerTower
# //
# //******************************************************************************

def calculatePowerTower( args ):
    if isinstance( args[ 0 ], list ):
        return [ calculatePowerTower( arg ) for arg in args ]

    result = args[ -1 ]

    for i in args[ -1 : : -1 ]:
        result = power( i, result )

    return result


# //******************************************************************************
# //
# //  calculatePowerTower2
# //
# //******************************************************************************

def calculatePowerTower2( args ):
    if isinstance( args[ 0 ], list ):
        return [ calculatePowerTower2( arg ) for arg in args ]

    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


# //******************************************************************************
# //
# //  getAlternatingSum
# //
# //******************************************************************************

def getAlternatingSum( args ):
    if isinstance( args[ 0 ], list ):
        return [ getAlternatingSum( arg ) for arg in args ]

    for i in range( 1, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


# //******************************************************************************
# //
# //  getAlternatingSum2
# //
# //******************************************************************************

def getAlternatingSum2( args ):
    if isinstance( args[ 0 ], list ):
        return [ getAlternatingSum2( arg ) for arg in args ]

    for i in range( 0, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


# //******************************************************************************
# //
# //  getSum
# //
# //******************************************************************************

def getSum( n ):
    hasUnits = False

    for item in n:
        if isinstance( item, Measurement ):
            hasUnits = True
            break

    if hasUnits:
        result = None

        for item in n:
            if isinstance( item, list ):
                return [ getSum( arg ) for arg in item ]

            if result is None:
                result = item
            else:
                result = result.add( item )

        return result
    else:
        if len( n ) == 0:
            return 0

        if isinstance( n[ 0 ], list ):
            return [ getSum( item ) for item in n ]
        else:
            return fsum( n )


# //******************************************************************************
# //
# //  getProduct
# //
# //******************************************************************************

def getProduct( n ):
    hasUnits = False

    for item in n:
        if isinstance( item, Measurement ):
            hasUnits = True
            break

    if hasUnits:
        result = None

        for item in n:
            if isinstance( item, list ):
                return [ getProduct( arg ) for arg in item ]

            if result is None:
                result = item
            else:
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
# //  unlist
# //
# //******************************************************************************

def unlist( arg ):
    if isinstance( arg, list ):
        for i in arg:
            result.append( i )
    else:
        result.append( i )


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
# //  calculateMean
# //
# //******************************************************************************

def calculateMean( args ):
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
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getMax( arg ) for arg in args ]
        else:
            return max( args )
    else:
        return args


# //******************************************************************************
# //
# //  getMin
# //
# //******************************************************************************

def getMin( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getMin( arg ) for arg in args ]
        else:
            return max( args )
    else:
        return args



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


