#!/usr/bin/env python

#//******************************************************************************
#//
#//  getInvertedBits
#//
#//******************************************************************************

def getInvertedBits( n ):
    value = floor( n )
    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << g.bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = value

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        result = fadd( fmul( fsum( [ placeValue, fneg( fmod( remaining, placeValue ) ), -1 ] ), multiplier ), result )
        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    return result


#//******************************************************************************
#//
#//  convertToSignedInt
#//
#//  two's compliment logic is in effect here
#//
#//******************************************************************************

def convertToSignedInt( n, k ):
    value = fadd( n, ( power( 2, fsub( k, 1 ) ) ) )
    value = fmod( value, power( 2, k ) )
    value = fsub( value, ( power( 2, fsub( k, 1 ) ) ) )

    return value


#//******************************************************************************
#//
#//  performBitwiseOperation
#//
#//  The operations are performed on groups of bits as specified by the variable
#//  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
#//  does mean that under normal circumstances the regular Python bit operators
#//  can be used.
#//
#//******************************************************************************

def performBitwiseOperation( i, j, operation ):
    value1 = floor( i )
    value2 = floor( j )

    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value1, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )
    groupings2 = int( fadd( floor( fdiv( ( log( value1, 2 ) ), g.bitwiseGroupSize ) ), 1 ) )

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


#//******************************************************************************
#//
#//  getBitCount
#//
#//******************************************************************************

def getBitCount( n ):
    result = 0

    if isinstance( n, Measurement ):
        value = n.getValue( )
    else:
        value = int( n )

    while ( value ):
        value &= value - 1
        result += 1

    return result


#//******************************************************************************
#//
#//  unpackInteger
#//
#//******************************************************************************

def unpackInteger( n, fields ):
    if isinstance( n, list ):
        return [ unpackInteger( i, fields ) for i in n ]

    if not isinstance( fields, list ):
        return unpackInteger( n, [ fields ] )

    value = int( n )
    result = [ ]

    for i in reversed( fields ):
        size = int( i )
        result.insert( 0, value & ( 2 ** size - 1 ) )
        value >>= size

    return result


