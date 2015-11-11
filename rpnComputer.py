#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnComputer.py
# //
# //  RPN command-line calculator computing operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import struct

from mpmath import *

from rpnMeasurement import RPNMeasurement
from rpnUtils import real_int

import rpnGlobals as g


# //******************************************************************************
# //
# //  getInvertedBits
# //
# //******************************************************************************

def getInvertedBits( n ):
    value = real_int( n )

    # determine how many groups of bits we will be looking at
    if value == 0:
        groupings = 1
    else:
        groupings = int( fadd( floor( fdiv( ( log( value, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << g.bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = value

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        result = fadd( fmul( fsum( [ placeValue,
                                     fneg( fmod( remaining, placeValue ) ), -1 ] ),
                             multiplier ), result )
        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    return result


# //******************************************************************************
# //
# //  convertToSignedInt
# //
# //  two's compliment logic is in effect here
# //
# //******************************************************************************

def convertToSignedInt( n, k ):
    value = fadd( real_int( n ), ( power( 2, fsub( real_int( k ), 1 ) ) ) )
    value = fmod( value, power( 2, k ) )
    value = fsub( value, ( power( 2, fsub( k, 1 ) ) ) )

    return value


# //******************************************************************************
# //
# //  performBitwiseOperation
# //
# //  The operations are performed on groups of bits as specified by the variable
# //  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
# //  does mean that under normal circumstances the regular Python bit operators
# //  can be used.
# //
# //******************************************************************************

def performBitwiseOperation( i, j, operation ):
    value1 = real_int( i )
    value2 = real_int( j )

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

    for i in range( 0, groupings ):
        mod1 = fmod( remaining1, placeValue )
        mod2 = fmod( remaining2, placeValue )

        result = fadd( fmul( operation( int( mod1 ), int( mod2 ) ), multiplier ), result )

        remaining1 = floor( fdiv( remaining1, placeValue ) )
        remaining2 = floor( fdiv( remaining2, placeValue ) )

        multiplier = fmul( multiplier, placeValue )

    return result


# //******************************************************************************
# //
# //  getBitCount
# //
# //******************************************************************************

def getBitCount( n ):
    result = 0

    if isinstance( n, RPNMeasurement ):
        value = real_int( n.getValue( ) )
    else:
        value = real_int( n )

    while ( value ):
        value &= value - 1
        result += 1

    return result


# //******************************************************************************
# //
# //  unpackInteger
# //
# //******************************************************************************

def unpackInteger( n, fields ):
    if isinstance( n, list ):
        return [ unpackInteger( i, fields ) for i in n ]

    if not isinstance( fields, list ):
        return unpackInteger( n, [ fields ] )

    value = real_int( n )
    result = [ ]

    for field in reversed( fields ):
        size = int( field )
        result.insert( 0, value & ( 2 ** size - 1 ) )
        value >>= size

    return result


# //******************************************************************************
# //
# //  packInteger
# //
# //******************************************************************************

def packInteger( values, fields ):
    if not isinstance( values, list ):
        return unpackInteger( [ values ], fields )

    if not isinstance( fields, list ):
        return unpackInteger( values, [ fields ] )

    if isinstance( values[ 0 ], list ):
        return [ unpackInteger( value, fields ) for value in values ]

    result = 0

    count = min( len( values ), len( fields ) )

    size = 0

    for i in range( count, 0, -1 ):
        result = fadd( result, fmul( values[ i - 1 ], power( 2, size ) ) )
        size += fields[ i - 1 ]

    return result


# //******************************************************************************
# //
# //  interpretAsFloat
# //
# //******************************************************************************

def interpretAsFloat( n ):
    if ( real_int( n ) < 0 ) or ( n >= 2 ** 32 - 1 ):
        raise ValueError( 'value out of range for a 32-bit float' )

    intValue = struct.pack( 'I', int( n ) )
    return mpf( struct.unpack( 'f', intValue )[ 0 ] )


# //******************************************************************************
# //
# //  interpretAsDouble
# //
# //******************************************************************************

def interpretAsDouble( n ):
    if ( real_int( n ) < 0 ) or ( n >= 2 ** 64 - 1 ):
        raise ValueError( 'value out of range for a 64-bit float' )

    intValue = struct.pack( 'Q', int( n ) )
    return mpf( struct.unpack( 'd', intValue )[ 0 ] )

