#!/usr/bin/env python

#******************************************************************************
#
#  rpnComputer.py
#
#  rpnChilada computing operators
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import struct

from mpmath import fadd, fdiv, floor, fmod, fmul, fsub, fsum, log, mpf, mp, mpmathify, power

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnSettings import setAccuracy
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, IntValidator, ListValidator, RealValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  convertToSignedInt
#
#  two's compliment logic is in effect here
#
#******************************************************************************

def convertToSignedInt( n, k ):
    newPrecision = ( int( k ) * 3 / 10 ) + 3

    if mp.dps < newPrecision:
        setAccuracy( newPrecision )

    value = fadd( n, ( power( 2, fsub( k, 1 ) ) ) )
    value = fmod( value, power( 2, k ) )
    value = fsub( value, ( power( 2, fsub( k, 1 ) ) ) )

    return value


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 1 ) ] )
def convertToSignedIntOperator( n, k ):
    return convertToSignedInt( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToCharOperator( n ):
    return convertToSignedInt( n, 8 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToShortOperator( n ):
    return convertToSignedInt( n, 16 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToLongOperator( n ):
    return convertToSignedInt( n, 32 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToLongLongOperator( n ):
    return convertToSignedInt( n, 64 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToQuadLongOperator( n ):
    return convertToSignedInt( n, 128 )


#******************************************************************************
#
#  getInvertedBitsOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getInvertedBits( n ):
    # determine how many groups of bits we will be looking at
    if n == 0:
        groupings = 1
    else:
        groupings = int( fadd( floor( fdiv( ( log( n, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << g.bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = n

    result = mpmathify( 0 )

    for _ in range( 0, groupings ):
        # Let's let Python do the actual inverting
        group = fmod( ~int( fmod( remaining, placeValue ) ), placeValue )

        result += fmul( group, multiplier )

        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getInvertedBitsOperator( n ):
    return getInvertedBits( n )


#******************************************************************************
#
#  performBitwiseOperation
#
#  The operations are performed on groups of bits as specified by the variable
#  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
#  does mean that under normal circumstances the regular Python bit operators
#  can be used.
#
#******************************************************************************

def performBitwiseOperation( i, j, operation ):
    value1 = int( i )
    value2 = int( j )

    # determine how many groups of bits we will be looking at
    if value1 == 0:
        groupings = 1
    else:
        groupings = int( fadd( floor( fdiv( ( log( value1, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

    if value2 == 0:
        groupings2 = 1
    else:
        groupings2 = int( fadd( floor( fdiv( ( log( value2, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

    if groupings2 > groupings:
        groupings = groupings2

    placeValue = mpmathify( 1 << g.bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining1 = value1
    remaining2 = value2

    result = mpmathify( 0 )

    for _ in range( 0, groupings ):
        mod1 = fmod( remaining1, placeValue )
        mod2 = fmod( remaining2, placeValue )

        result = fadd( fmul( operation( int( mod1 ), int( mod2 ) ), multiplier ), result )

        remaining1 = floor( fdiv( remaining1, placeValue ) )
        remaining2 = floor( fdiv( remaining2, placeValue ) )

        multiplier = fmul( multiplier, placeValue )

    return result


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseAndOperator( n, k ):
    return performBitwiseOperation( n, k, lambda x, y: x & y )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseNandOperator( n, k ):
    return getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x & y ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseNorOperator( n, k ):
    return getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x | y ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseOrOperator( n, k ):
    return performBitwiseOperation( n, k, lambda x, y: x | y )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseXorOperator( n, k ):
    return performBitwiseOperation( n, k, lambda x, y: x ^ y )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getBitwiseXnorOperator( n, k ):
    return getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x ^ y ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def shiftLeftOperator( n, k ):
    return fmul( n, 1 << int( k ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def shiftRightOperator( n, k ):
    return floor( fdiv( n, 1 << int( k ) ) )


#******************************************************************************
#
#  getBitCount
#
#******************************************************************************

def getBitCount( n ):
    n = int( n )

    if n < 0:
        raise ValueError( '\'bit_count\' requires a positive integer value' )

    result = 0

    if isinstance( n, RPNMeasurement ):
        value = n.value
    else:
        value = n

    while value:
        result += fmod( value, 2 )
        value = floor( fdiv( value, 2 ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getBitCountOperator( n ):
    return getBitCount( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getParityOperator( n ):
    return fmod( getBitCount( n ), 2 )


#******************************************************************************
#
#  unpackInteger
#
#******************************************************************************

def unpackInteger( n, fields ):
    if isinstance( n, RPNGenerator ):
        return unpackInteger( list( n ), fields )

    if isinstance( n, list ):
        return [ unpackInteger( i, fields ) for i in n ]

    if isinstance( fields, RPNGenerator ):
        return unpackInteger( n, list( fields ) )

    if not isinstance( fields, list ):
        return unpackInteger( n, [ fields ] )

    value = int( n )
    result = [ ]

    for field in reversed( fields ):
        size = int( field )
        result.insert( 0, value & ( 2 ** size - 1 ) )
        value >>= size

    return result


#oneArgAndListFunctionEvaluator( )
@argValidator( [ IntValidator( ), ListValidator( ) ] )
def unpackIntegerOperator( n, fields ):
    return unpackInteger( n, fields )


#******************************************************************************
#
#  packInteger
#
#******************************************************************************

def packInteger( values, fields ):
    if isinstance( values, RPNGenerator ):
        return packInteger( list( values ), fields )

    if not isinstance( values, list ):
        return unpackInteger( [ values ], fields )

    if isinstance( fields, RPNGenerator ):
        return packInteger( values, list( fields ) )

    if not isinstance( fields, list ):
        return unpackInteger( values, [ fields ] )

    if isinstance( values[ 0 ], list ):
        return [ unpackInteger( value, fields ) for value in values ]

    result = 0

    count = min( len( values ), len( fields ) )

    size = 0

    for i in range( count, 0, -1 ):
        field = int( fields[ i - 1 ] )
        value = int( values[ i - 1 ] ) & ( 2 ** field - 1 )
        result = fadd( result, fmul( value, power( 2, size ) ) )
        size += field

    return result


@argValidator( [ ListValidator( ), ListValidator( ) ] )
def packIntegerOperator( values, fields ):
    return packInteger( values, fields )


#******************************************************************************
#
#  interpretAsFloat
#
#******************************************************************************

def interpretAsFloat( n ):
    intValue = struct.pack( 'I', int( n ) )
    return mpf( struct.unpack( 'f', intValue )[ 0 ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0, 2 ** 32 - 1 ) ] )
def interpretAsFloatOperator( n ):
    return interpretAsFloat( n )


#******************************************************************************
#
#  interpretAsDouble
#
#******************************************************************************

def interpretAsDouble( n ):
    setAccuracy( 25 )

    intValue = struct.pack( 'Q', int( n ) )
    return mpf( struct.unpack( 'd', intValue )[ 0 ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0, 2 ** 64 - 1 ) ] )
def interpretAsDoubleOperator( n ):
    return interpretAsDouble( n )


#******************************************************************************
#
#  conversion operators
#
#******************************************************************************


@oneArgFunctionEvaluator( )
@argValidator( [ RealValidator( ) ] )
def convertToDoubleOperator( n ):
    return fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( n ) ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ RealValidator( ) ] )
def convertToFloatOperator( n ):
    return fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( n ) ) ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( 1 ) ] )
def convertToUnsignedIntOperator( n, k ):
    return fmod( n, power( 2, k ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToUnsignedCharOperator( n ):
    return fmod( n, power( 2, 8 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToUnsignedShortOperator( n ):
    return fmod( n, power( 2, 16 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToUnsignedLongOperator( n ):
    return fmod( n, power( 2, 32 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToUnsignedLongLongOperator( n ):
    return fmod( n, power( 2, 64 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertToUnsignedQuadLongOperator( n ):
    return fmod( n, power( 2, 128 ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def andOperator( n, k ):
    return 1 if ( n != 0 and k != 0 ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def notOperator( n ):
    return 1 if n == 0 else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def nandOperator( n, k ):
    return 0 if ( n != 0 and k != 0 ) else 1


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def norOperator( n, k ):
    return 0 if ( n != 0 or k != 0 ) else 1


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def orOperator( n, k ):
    return 1 if ( n != 0 or k != 0 ) else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def xnorOperator( n, k ):
    return 1 if ( n != 0 ) == ( k != 0 ) else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def xorOperator( n, k ):
    return 1 if ( n != 0 ) != ( k != 0 ) else 0
