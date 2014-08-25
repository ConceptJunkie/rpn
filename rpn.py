#!/usr/bin/env python

# Things that don't work, but should:
#
#   This requires implicit conversion between unit types
#   rpn -D 16800 mA hours * 5 volts * joule convert
#

#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import arrow
import argparse
import calendar
import datetime
import struct
import sys
import time

from functools import reduce
from mpmath import *
from random import randrange

from rpnDeclarations import *
from rpnPrimeUtils import *
from rpnUtils import *
from rpnVersion import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


#//******************************************************************************
#//
#//  add
#//
#//  We used to be able to call fadd directly, but now we want to be able to add
#//  units.  Adding units includes an implicit conversion if the units are not
#//  the same.
#//
#//******************************************************************************

def add( n, k ):
    if isinstance( n, arrow.Arrow ) and isinstance( k, Measurement ):
        return addTimes( n, k )
    elif isinstance( n, Measurement ) and isinstance( k, arrow.Arrow ):
        return addTimes( k, n )
    elif isinstance( n, Measurement ):
        return n.add( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).add( k )
    else:
        return fadd( n, k )


#//******************************************************************************
#//
#//  incrementMonths
#//
#//******************************************************************************

def incrementMonths( n, months ):
    newDay = n.day
    newMonth = n.month + int( months )
    newYear = n.year

    if newMonth < 1 or newMonth > 12:
        newYear += ( newMonth - 1 ) // 12
        newMonth = ( ( newMonth - 1 ) % 12 ) + 1

    maxDay = calendar.monthrange( newYear, newMonth )[ 1 ]

    if newDay > maxDay:
        newDay = maxDay

    return arrow.Arrow( newYear, newMonth, newDay, n.hour, n.minute, n.second )


#//******************************************************************************
#//
#//  addTimes
#//
#//  arrow + measurement
#//
#//******************************************************************************

def addTimes( n, k ):
    if 'years' in g.unitOperators[ k.getUnitString( ) ].categories:
        years = convertUnits( k, 'year' ).getValue( )
        return n.replace( year=n.year + years )
    elif 'months' in g.unitOperators[ k.getUnitString( ) ].categories:
        months = convertUnits( k, 'month' ).getValue( )
        result = incrementMonths( n, months )
        return result
    else:
        delta = datetime.timedelta

        days = int( floor( convertUnits( k, 'day' ).getValue( ) ) )
        seconds = int( fmod( floor( convertUnits( k, 'second' ).getValue( ) ), 86400 ) )
        microseconds = int( fmod( floor( convertUnits( k, 'microsecond' ).getValue( ) ), 1000000 ) )

        return n + datetime.timedelta( days=days, seconds=seconds, microseconds=microseconds )


#//******************************************************************************
#//
#//  subtractTimes
#//
#//  arrow - measurement
#//
#//******************************************************************************

def subtractTimes( n, k ):
    kneg = Measurement( fneg( k.getValue( ) ), k.getUnits( ) )
    return addTimes( n, kneg )


#//******************************************************************************
#//
#//  subtract
#//
#//  We used to be able to call fsub directly, but now we want to be able to
#//  subtract units and do the appropriate conversions.
#//
#//******************************************************************************

def subtract( n, k ):
    if isinstance( n, arrow.Arrow ):
        if isinstance( k, Measurement ):
            return subtractTimes( n, k )
        elif isinstance( k, arrow.Arrow ):
            if n > k:
                delta = n - k
                factor = 1
            else:
                delta = k - n
                factor = -1

            if delta.days != 0:
                result = Measurement( delta.days * factor, 'day' )
                result = result.add( Measurement( delta.seconds * factor, 'second' ) )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            elif delta.seconds != 0:
                result = Measurement( delta.seconds * factor, 'second' )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            else:
                result = Measurement( delta.microseconds * factor, 'microsecond' )

            return result
        else:
            raise ValueError( 'cannot subtract incompatible types' )
    elif isinstance( n, Measurement ):
        if isinstance( k, arrow.Arrow ):
            return subtractTimes( k, n )
        elif isinstance( k, Measurement ):
            return Measurement( n ).subtract( k )
        else:
            return n.subtract( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).subtract( k )
    else:
        return fsub( n, k )


#//******************************************************************************
#//
#//  getNegative
#//
#//******************************************************************************

def getNegative( n ):
    if isinstance( n, Measurement ):
        return Measurement( fneg( n.getValue( ) ), n.getUnits( ) )
    else:
        return fneg( n )


#//******************************************************************************
#//
#//  divide
#//
#//  We used to be able to call fdiv directly, but now we want to also divide
#//  the units.  Doing so lets us do all kinds of great stuff because now we
#//  can support compound units without having to explicitly declare them in
#//  makeUnits.py.
#//
#//******************************************************************************

def divide( n, k ):
    if isinstance( n, Measurement ):
        return n.divide( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).divide( k )
    else:
        return fdiv( n, k )


#//******************************************************************************
#//
#//  multiply
#//
#//  We used to be able to call fmul directly, but now we want to also multiply
#//  the units.  This allows compound units and the conversion routines try to
#//  be smart enough to deal with this.  There are scenarios in which it doesn't
#//  work, like converting parsec*barn to cubic_inch.  However, that can be done
#//  by converting parsec to inches and barn to square_inch separately and
#//  multiplying the result.
#//
#//******************************************************************************

def multiply( n, k ):
    if isinstance( n, Measurement ):
        return n.multiply( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).multiply( k )
    else:
        return fmul( n, k )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( n, k ):
    if isinstance( n, Measurement ):
        return n.exponentiate( k )
    elif isinstance( k, Measurement ):
        raise ValueError( 'a measurement cannot be exponentiated (yet)' )
    else:
        return power( n, k )


#//******************************************************************************
#//
#//  sum
#//
#//******************************************************************************

def sum( n ):
    hasUnits = False

    for item in n:
        if isinstance( item, Measurement ):
            hasUnits = True
            break

    if hasUnits:
        result = None

        for item in n:
            if result is None:
                result = item
            else:
                result = result.add( item )

        return result
    else:
        return fsum( n )


#//******************************************************************************
#//
#//  takeReciprocal
#//
#//  We used to be able to call fdiv directly, but now we want to handle
#//  Measurements.
#//
#//******************************************************************************

def takeReciprocal( n ):
    if isinstance( n, Measurement ):
        return n.invert( )
    else:
        return fdiv( 1, n )


#//******************************************************************************
#//
#//  getNthAlternatingFactorial
#//
#//******************************************************************************

def getNthAlternatingFactorial( n ):
    result = 0

    negative = False

    for i in arange( n, 0, -1 ):
        if negative:
            result = fadd( result, fneg( fac( i ) ) )
            negative = False
        else:
            result = fadd( result, fac( i ) )
            negative = True

    return result


#//******************************************************************************
#//
#//  getNthPascalLine
#//
#//******************************************************************************

def getNthPascalLine( n ):
    result = [ ]

    for i in arange( 0, n ):
        result.append( binomial( n - 1, i ) )

    return result


#//******************************************************************************
#//
#//  getNthAperyNumber
#//
#//  http://oeis.org/A005259
#//
#//  a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
#//
#//******************************************************************************

def getNthAperyNumber( n ):
    result = 0

    for k in arange( 0, n + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ), power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


#//******************************************************************************
#//
#//  getDivisorCount
#//
#//******************************************************************************

def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in factor( n ) ] )


#//******************************************************************************
#//
#//  getDivisors
#//
#//******************************************************************************

def getDivisors( n ):
    result = getExpandedFactorList( factor( n ) )

    result = [ list( i ) for i in itertools.chain.from_iterable( itertools.combinations( result, r ) for r in range( 0, len( result ) + 1 ) ) ]

    from operator import mul
    result = set( [ reduce( mul, i, 1 ) for i in result[ 1 : ] ] )
    result.add( 1 )

    result = sorted( list( result ) )

    return result


#//******************************************************************************
#//
#//  factor
#//
#//  This is not my code, and I need to find the source so I can attribute it.
#//  I think I got it from stackoverflow.com.
#//
#//******************************************************************************

def factor( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factor( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def getPotentialPrimes( ):
            basePrimes = ( 2, 3, 5 )

            for basePrime in basePrimes:
                yield basePrime

            basePrimes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            primeGroup = 0

            while True:
                for basePrime in basePrimes:
                    yield primeGroup + basePrime

                primeGroup += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in getPotentialPrimes( ):
            if divisor > sqrtn:
                break

            power = 0

            while ( fmod( n, divisor ) ) == 0:
                n = floor( fdiv( n, divisor ) )
                power += 1

            if power > 0:
                factors.append( ( divisor, power ) )
                sqrtn = sqrt( n )

        if n > 1:
            factors.append( ( int( n ), 1 ) )

        return factors


#//******************************************************************************
#//
#//  getExpandedFactorList
#//
#//******************************************************************************

def getExpandedFactorList( factors ):
    factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return reduce( lambda x, y: x + y, factors, [ ] )


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
#//  performTrigOperation
#//
#//******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, Measurement ):
        value = mpf( i.convertValue( Measurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )


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
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  getNthLucasNumber
#//
#//******************************************************************************

def getNthLucasNumber( n ):
    if n == 1:
        return 1
    else:
        return floor( fadd( power( phi, n ), 0.5 ) )


#//******************************************************************************
#//
#//  getNthJacobsthalNumber
#//
#//  From: http://oeis.org/A001045
#//
#//  a( n ) = ceiling( 2 ^ ( n + 1 ) / 3 ) - ceiling( 2 ^ n / 3 )
#//
#//******************************************************************************

def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthPellNumber
#//
#//  From:  http://oeis.org/A000129
#//
#//  a( n ) = round( ( 1 + sqrt( 2 ) ) ^ n )
#//
#//******************************************************************************

def getNthPellNumber( n ):
    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthBaseKRepunit
#//
#//******************************************************************************

def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( k ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


#//******************************************************************************
#//
#//  getPrimePi
#//
#//******************************************************************************

def getPrimePi( n ):
    result = primepi2( n )

    return [ mpf( result.a ), mpf( result.b ) ]


#//******************************************************************************
#//
#//  getNthTribonacci
#//
#//******************************************************************************

def getNthTribonacci( n ):
    roots = polyroots( [ 1, -1, -1, -1  ] )
    roots2 = polyroots( [ 44, 0, -2, -1 ] )

    result = 0

    for i in range( 0, 3 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthTetranacci
#//
#//  http://mathworld.wolfram.com/TetranacciNumber.html
#//
#//******************************************************************************

def getNthTetranacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1 ] )
    roots2 = polyroots( [ 563, 0, -20, -5, -1 ] )

    result = 0

    for i in range( 0, 4 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthPentanacci
#//
#//******************************************************************************

def getNthPentanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 5 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 8, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHexanacci
#//
#//******************************************************************************

def getNthHexanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 6 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 10, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHeptanacci
#//
#//******************************************************************************

def getNthHeptanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 7 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 3, 12, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthSylvester
#//
#//******************************************************************************

def getNthSylvester( n ):
    if n == 1:
        return 2
    elif n == 2:
        return 3
    else:
        list = [ 2, 3 ]

        for i in arange( 2, n ):
            list.append( fprod( list ) + 1 )

    return list[ -1 ]


#//******************************************************************************
#//
#//  getNthPolygonalNumber
#//
#//******************************************************************************

def getNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coeff = fdiv( fsub( k, 2 ), 2 )
    return polyval( [ coeff, fneg( fsub( coeff, 1 ) ), 0 ], n )


#//******************************************************************************
#//
#//  getRegularPolygonArea
#//
#//  based on having sides of unit length
#//
#//  http://www.mathopenref.com/polygonregulararea.html
#//
#//******************************************************************************

def getRegularPolygonArea( n ):
    if n < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) )


#//******************************************************************************
#//
#//  getNSphereRadius
#//
#//  k needs to be a Measurement so getNSphereRadius can tell if it's an area
#//  or a volume and use the correct formula.
#//
#//******************************************************************************

def getNSphereRadius( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return Measurement( k, 'length' )

    print( type( k.getBasicTypes( ).getUnitString( ) ) )

    measurementType = k.getBasicTypes( ).getUnitString( )

    if measurementType == 'length':
        return 1
    elif measurementType == 'area':
        return fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                           fmul( n, power( pi, fdiv( n, 2 ) ) ) ),
                     root( k, fsub( n, 1 ) ) )
    elif measurementType == 'volume':
        return root( fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                                 power( pi, fdiv( n, 2 ) ) ), k ), 3 )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' + measurementType )


#//******************************************************************************
#//
#//  getNSphereSurfaceArea
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is a volume
#//  then it is taken to be the volume.  If it is an area, then it is returned
#//  unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereSurfaceArea( n, k ):
    if not isinstance( k, Measurement ):
        return getNSphereSurfaceArea( n, Measurement( k, 'length' ) )

    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( fmul( n, power( pi, fdiv( n, 2 ) ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, fsub( n, 1 ) ) )
    elif measurementType == { 'length' : 2 }:
        return k
    elif measurementType == { 'length' : 3 }:
        return 3
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )


#//******************************************************************************
#//
#//  getNSphereVolume
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is an area
#//  then it is taken to be the surface area.  If it is a volume, then it is
#//  returned unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereVolume( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return getNSphereVolume( n, Measurement( k, 'length' ) )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( power( pi, fdiv( n, 2 ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, n ) )
    elif measurementType == { 'length' : 2 }:
        return 2   # formula for converting surface area to volume
    elif measurementType == { 'length' : 3 }:
        return k
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )


#//******************************************************************************
#//
#//  getTriangleArea
#//
#//  https://en.wikipedia.org/wiki/Equilateral_triangle#Area
#//
#//******************************************************************************

def getTriangleArea( a, b, c ):
    return fdiv( fsum( [ power( a, 2 ), power( b, 2 ), power( c, 2 ) ] ), fmul( 4, sqrt( 3 ) ) )


#//******************************************************************************
#//
#//  findNthPolygonalNumber
#//
#//  http://www.wolframalpha.com/input/?i=solve+%28+%28+k+%2F+2+%29+-+1+%29+x^2+-+%28+%28+k+%2F+2+%29+-+2+%29+x+%2B+0+%3D+n+for+x
#//
#//******************************************************************************

def findNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( fsum( [ sqrt( fsum( [ power( k, 2 ), fprod( [ 8, k, n ] ),
                                       fneg( fmul( 8, k ) ), fneg( fmul( 16, n ) ), 16 ] ) ),
                         k, -4 ] ), fmul( 2, fsub( k, 2 ) ) )


#//******************************************************************************
#//
#//  getCenteredPolygonalNumber
#//
#//******************************************************************************

def getCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coefficient = fdiv( k, 2 )
    return polyval( [ coefficient, fneg( coefficient ), 1 ], n )


#//******************************************************************************
#//
#//  findCenteredPolygonalNumber
#//
#//  wolframalpha.com solved this for me.
#//
#//******************************************************************************

def findCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    s = fdiv( k, 2 )

    return fdiv( fadd( sqrt( s ), sqrt( fsum( [ fmul( 4, n ), s, -4 ] ) ) ), fmul( 2, sqrt( s ) ) )


#//******************************************************************************
#//
#//  getNthHexagonalSquareNumber
#//
#//  http://oeis.org/A046177
#//
#//  a( n ) = floor( 1 / 32 * ( tan( 3 * pi / 8 ) ) ^ ( 8 * n - 4 ) )
#//
#//******************************************************************************

#//******************************************************************************
#//
#//  getNthHexagonalPentagonalNumber
#//
#//  http://oeis.org/A046178
#//
#//  a( n ) = ceiling( 1 / 12 * ( sqrt( 3 ) - 1 ) * ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) )
#//
#//******************************************************************************

def getNthHexagonalPentagonalNumber( n ):
    return ceil( fdiv( fmul( fsub( sqrt( 3 ), 1 ),
                             power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                       12 ) )


#//******************************************************************************
#//
#//  getNthHeptagonalTriangularNumber
#//
#//  http://oeis.org/A046194
#//
#//  a(n) = 1 / 80 * ( ( 3 - sqrt( 5 ) * ( -1 ) ^ n ) * ( 2 + sqrt( 5 ) ) ^ ( 4n - 2 ) +
#//                    ( 3 + sqrt( 5 ) * ( -1 ) ^ n ) * ( 2 - sqrt( 5 ) ) ^ ( 4n - 2 ) - 14 )
#//
#//  LinearRecurrence[ { 1, 103682, -103682, -1, 1 },
#//                    { 1, 55, 121771, 5720653, 12625478965 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -1, -103682, 103682, 1 ],
                                   [ 1, 55, 121771, 5720653, 12625478965 ], n )


#//******************************************************************************
#//
#//  getNthHeptagonalSquareNumber
#//
#//  http://oeis.org/A046195
#//
#//  LinearRecurrence[ { 1 , 0, 1442, -1442, 0, -1, 1 },
#//                    { 1, 6, 49, 961, 8214, 70225, 1385329 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalSquareNumber( n ):
    index = getNthLinearRecurrence( [ 1, -1, 0, -1442, 1442, 0, 1 ],
                                    [ 1, 6, 49, 961, 8214, 70225, 1385329 ], n )

    return getNthPolygonalNumber( index, 7 )


#//******************************************************************************
#//
#//  getNthHeptagonalPentagonalNumber
#//
#//  http://oeis.org/A048900
#//
#//  a(n) = floor( 1 / 240 * ( ( 2 + sqrt( 15 ) ) ^ 2 * ( 4 + sqrt( 15 ) ) ^ ( 4n - 3 ) ) )
#//
#//******************************************************************************

def getNthHeptagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( power( fadd( 2, sqrt( 15 ) ), 2 ),
                              power( fadd( 4, sqrt( 15 ) ), fsub( fmul( 4, n ), 3 ) ) ), 240 ) )


#//******************************************************************************
#//
#//  getNthHeptagonalHexagonalNumber
#//
#//  http://oeis.org/A048903
#//
#//  a(n) = floor( 1 / 80 * ( sqrt( 5 ) - 1 ) * ( 2 + sqrt( 5 ) ) ^ ( 8n - 5 ) )
#//
#//******************************************************************************

def getNthHeptagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( sqrt( 5 ), 1 ),
                              power( fadd( 2, sqrt( 5 ) ), fsub( fmul( 8, n ), 5 ) ) ), 80 ) )


#//******************************************************************************
#//
#//  getNthOctagonalTriangularNumber
#//
#//  From http://oeis.org/A046183
#//
#//  a(n) = floor( 1 / 96 * ( 7 - 2 * sqrt( 6 ) * ( -1 ) ^ n ) * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 4n - 2 ) )
#//
#//  LinearRecurrence[{1, 9602, -9602, -1, 1}, {1, 21, 11781, 203841, 113123361}, 13]
#//
#//******************************************************************************

def getNthOctagonalTriangularNumber( n ):
    sign = power( -1, n )

    return floor( fdiv( fmul( fsub( 7, fprod( [ 2, sqrt( 6 ), sign ] ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                        96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalSquareNumber
#//
#//  From http://oeis.org/A036428:
#//
#//  a(n) = 1 / 12 * ( ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) + ( 2 - sqrt( 3 ) ) ^ ( 4n -2 ) - 2 )
#//  a(n) = floor ( 1 / 12 * ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) )
#//
#//******************************************************************************

def getNthOctagonalSquareNumber( n ):
    return floor( fdiv( power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ), 12 ) )


#//******************************************************************************
#//
#//  getNthOctagonalPentagonalNumber
#//
#//  http://oeis.org/A046189
#//
#//  a(n) = floor( 1 / 96 * ( 11 - 6 * sqrt( 2 ) *( -1 ) ^ n ) * ( 1 + sqrt( 2 ) ) ^ ( 8 * n - 6 ) )
#//
#//******************************************************************************

def getNthOctagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( fsub( 11, fprod( [ 6, sqrt( 2 ), power( -1, n ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 8, n ), 6 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHexagonalNumber
#//
#//  http://oeis.org/A046192
#//
#//  a(n) = floor( 1 / 96 * ( 3 * sqrt( 3 ) - sqrt( 2 ) ) * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 8n - 5 ) )
#//
#//******************************************************************************

def getNthOctagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( fmul( 3, sqrt( 3 ) ), sqrt( 2 ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 8, n ), 5 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHeptagonalNumber
#//
#//  http://oeis.org/A048906
#//
#//  a(n) = floor( 1 / 480 * ( 17 + 2 * sqrt( 3 0 ) ) * ( sqrt( 5 ) + sqrt( 6 ) ) ^ ( 8n - 6 ) )
#//
#//******************************************************************************

def getNthOctagonalHeptagonalNumber( n ):
    return floor( fdiv( fmul( fadd( 17, fmul( sqrt( 30 ), 2 ) ),
                              power( fadd( sqrt( 5 ), sqrt( 6 ) ), fsub( fmul( 8, n ), 6 ) ) ), 480 ) )


#//******************************************************************************
#//
#//  getNthNonagonalTriangularNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = ( 5 / 14 ) +
#//           ( 9 / 28 ) * { [ 8 - 3 * sqrt( 7 ) ] ^ n + [ 8 + 3 * sqrt( 7 ) ] ^ n } +
#//           ( 3 / 28 ) * sqrt( 7 ) * { [ 8 + 3 * sqrt( 7 ) ] ^ n - [ 8 - 3 * sqrt( 7 ) ] ^ n }
#//
#//******************************************************************************

def getNthNonagonalTriangularNumber( n ):
    a = fmul( 3, sqrt( 7 ) )
    b = fadd( 8, a )
    c = fsub( 8, a )

    return fsum( [ fdiv( 5, 14 ),
                   fmul( fdiv( 9, 28 ), fadd( power( b, n ), power( c, n ) ) ),
                   fprod( [ fdiv( 3, 28 ),
                            sqrt( 7 ),
                            fsub( power( b, n ), power( c, n ) ) ] ) ] )


#//******************************************************************************
#//
#//  getNthNonagonalSquareNumber
#//
#//  From http://oeis.org/A048911:
#//
#//  Indices of square numbers which are also 9-gonal.
#//
#//  Let p = 8 * sqrt( 7 ) + 9 * sqrt( 14 ) - 7 * sqrt( 2 ) - 28 and
#//      q = 7 * sqrt( 2 ) + 9 * sqrt( 14 ) - 8 * sqrt( 7 ) - 28.
#//
#//  Then a( n ) = 1 / 112 *
#//                 ( ( p + q * (-1) ^ n ) * ( 2 * sqrt( 2 ) + sqrt( 7 ) ) ^ n -
#//                  ( p - q * (-1) ^ n ) * ( 2 * sqrt( 2 ) - sqrt( 7 ) ) ^ ( n - 1 ) )
#//
#//******************************************************************************

def getNthNonagonalSquareNumber( n ):
    p = fsum( [ fmul( 8, sqrt( 7 ) ), fmul( 9, sqrt( 14 ) ), fmul( -7, sqrt( 2 ) ), -28 ] )
    q = fsum( [ fmul( 7, sqrt( 2 ) ), fmul( 9, sqrt( 14 ) ), fmul( -8, sqrt( 7 ) ), -28 ] )
    sign = power( -1, n )

    index = fdiv( fsub( fmul( fadd( p, fmul( q, sign ) ),
                              power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), n ) ),
                        fmul( fsub( p, fmul( q, sign ) ),
                              power( fsub( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), fsub( n, 1 ) ) ) ), 112 )

    return power( round( index ), 2 )


#//******************************************************************************
#//
#//  getNthNonagonalPentagonalNumber
#//
#//  http://oeis.org/A048915
#//
#//  a(n) = floor(1/336*(25+4*sqrt(21))*(5-sqrt(21)*(-1)^n)*(2*sqrt(7)+3*sqrt(3))^(4n-4)).
#//
#//  LinearRecurrence[{1, 146361602, -146361602, -1, 1}, {1, 651, 180868051, 95317119801, 26472137730696901}, 9]
#//
#//******************************************************************************

def getNthNonagonalPentagonalNumber( n ):
    sqrt21 = sqrt( 21 )
    sign = power( -1, n )

    return floor( fdiv( fprod( [ fadd( 25, fmul( 4, sqrt21 ) ),
                                 fsub( 5, fmul( sqrt21, sign ) ),
                                 power( fadd( fmul( 2, sqrt( 7 ) ), fmul( 3, sqrt( 3 ) ) ),
                                        fsub( fmul( 4, n ), 4 ) ) ] ),
                        336 ) )


#//******************************************************************************
#//
#//  getNthNonagonalHexagonalNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = floor( 9 / 112 * ( 8 - 3 * sqrt( 7 ) * (-1) ^ n ) *
#//                            ( 8 + 3 * sqrt( 7 ) ) ^ ( 4 * n - 4 ) )
#//
#//******************************************************************************

def getNthNonagonalHexagonalNumber( n ):
    #a = fmul( 3, sqrt( 7 ) )
    #b = fadd( 8, a )
    #c = fsub( 8, a )

    #sign = 1 #power( -1, n )
    #exponent = fsub( fmul( 4, n ), 4 )

    #print( str( fmul( c, sign ) ) + '  ' + str( power( b, exponent ) ) )

    #return floor( fprod( [ fdiv( 9, 112 ), fmul( c, sign ), power( b, exponent ) ] ) )

    return getNthLinearRecurrence( [ 1, -1, -4162056194, 4162056194, 1 ],
                                   [ 1, 325, 5330229625, 1353857339341, 22184715227362706161 ], n )


#//******************************************************************************
#//
#//  getNthNonagonalHeptagonalNumber
#//
#//  From http://oeis.org/A048921
#//
#//  a(n) = floor(1/560*(39+4*sqrt(35))*(6+sqrt(35))^(4*n-3)).
#//
#//  LinearRecurrence[{20163, -20163, 1}, {1, 26884, 542041975}, 9]; (* Ant King, Dec 31 2011 *)
#//
#//******************************************************************************

def getNthNonagonalHeptagonalNumber( n ):
    sqrt35 = sqrt( 35 )

    return floor( fdiv( fmul( fadd( 39, fmul( 4, sqrt35 ) ),
                        power( fadd( 6, sqrt35 ), fsub( fmul( 4, n ), 3 ) ) ),
                        560 ) )


#//******************************************************************************
#//
#//  getNthNonagonalOctagonalNumber
#//
#//  From http://oeis.org/A048924:
#//
#//  a(n) = floor(1/672*(11*sqrt(7)-9*sqrt(6))*(sqrt(6)+sqrt(7))^(8n-5)).
#//
#//  LinearRecurrence[{454275, -454275, 1}, {1, 631125, 286703855361}, 30] (* Vincenzo Librandi, Dec 24 2011 *)
#//
#//******************************************************************************

def getNthNonagonalOctagonalNumber( n ):
    sqrt6 = sqrt( 6 )
    sqrt7 = sqrt( 7 )

    return floor( fdiv( fmul( fsub( fmul( 11, sqrt7 ), fmul( 9, sqrt6 ) ),
                              power( fadd( sqrt6, sqrt7 ), fsub( fmul( 8, n ), 5 ) ) ),
                        672 ) )

# Dec-tri
# http://oeis.org/A133216
# a(n) = floor ( 1/64 * (9 + 4*sqrt(2)*(-1)^n) * (1+sqrt(2))^(4*n-6) )

# Dec-square
# http://oeis.org/A133142
#  a(n)=(1/8)+(7/16)*[721-228*sqrt(10)]^n-(1/8)*[721-228*sqrt(10)]^n*sqrt(10)+(1/8)*[721+228 *sqrt(10)]^n*sqrt(10)+(7/16)*[721+228*sqrt(10)]^n

# Dec-pent
# http://oeis.org/A202563
# a(n) = floor(25/192*(sqrt(3)+sqrt(2))^(8*n-6))

# Dec-hex
# http://oeis.org/A203134
# a(n) = floor(1/64 *(5*sqrt(2)-1)*(sqrt(2)+1)^(8*n-5)).

# Dec-hept
# http://oeis.org/A203408
# a(n) = floor(1/320*(11-2*sqrt(10)*(-1)^n)*(1+sqrt(10))* (3+sqrt(10))^(4*n-3)).

# Dec-oct
# http://oeis.org/A203624
# a(n) = floor(1/192*(13+4*sqrt(3))*(2+sqrt(3))^(8*n-6)).

# Dec-non
# http://oeis.org/A203627
# a(n) = floor(1/448*(15+2*sqrt(14))*(2*sqrt(2)+sqrt(7))^(8*n-6)).


#//******************************************************************************
#//
#//  findTetrahedralNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def findTetrahedralNumber( n ):
    #sqrt3 = sqrt( 3 )
    #curt3 = cbrt( 3 )

    # TODO:  finish me
    return 0

# http://www.wolframalpha.com/input/?i=solve+p%3D%281%2F6%29*%28n^3%2B3*n^2%2B2*n%29+for+n


#//******************************************************************************
#//
#//  getNthTruncatedTetrahedralNumber
#//
#//  Take the (3n-2)th terahedral number and chop off the (n-1)th tetrahedral
#//  number from each corner.
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedTetrahedralNumber( n ):
    return fmul( fdiv( n, 6 ), fsum( [ fprod( [ 23, n, n ] ), fmul( -27, n ), 10 ] ) )


#//******************************************************************************
#//
#//  getNthSquareTriangularNumber
#//
#//******************************************************************************

def getNthSquareTriangularNumber( n ):
    neededPrecision = int( n * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        mp.dps = neededPrecision

    sqrt2 = sqrt( 2 )

    return ceil( power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                    power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                              fmul( 4, sqrt2 ) ), 2 ) )


#//******************************************************************************
#//
#//  getNthPolygonalPyramidalNumber
#//
#//******************************************************************************

def getNthPolygonalPyramidalNumber( n, k ):
    return fprod( [ n, fadd( n, 1 ),
                    fsub( fmul( fsub( k, 2 ), n ), fsub( k, 5 ) ),
                    fdiv( 1, 6 ) ] )


#// A002415         4-dimensional pyramidal numbers: n^2*(n^2-1)/12.
#//                                                  n^4 - n^2 / 12
#//
#// A005585         5-dimensional pyramidal numbers: n(n+1)(n+2)(n+3)(2n+3)/5!.
#//
#// A001608         Perrin sequence (or Ondrej Such sequence): a(n) = a(n-2) + a(n-3).
#//                 LinearRecurrence[{0, 1, 1}, {3, 0, 2}, n]
#//
#// A001845         Centered octahedral numbers (crystal ball sequence for cubic lattice).
#//                 LinearRecurrence[{4, -6, 4, -1}, {1, 7, 25, 63}, 40]
#//
#// A046090         Consider all Pythagorean triples (X,X+1,Z) ordered by increasing Z; sequence gives X+1 values.
#//                 a(n+1)=round((1+(7+5*sqrt(2))*(3+2*sqrt(2))^n)/2);
#//                 LinearRecurrence[{7, -7, 1}, {1, 4, 21}, 25]
#//
#// A050534         Tritriangular numbers: a(n)=binomial(binomial(n,2),2) = n(n + 1)(n - 1)(n - 2)/8.
#//
#// A002817         Doubly triangular numbers: n*(n+1)*(n^2+n+2)/8.
#//                 a(n) = 3*binomial(n+2, 4)+binomial(n+1, 2).
#//
#// A007588         Stella octangula numbers: n*(2*n^2 - 1).
#//
#// A005803         Second-order Eulerian numbers: 2^n - 2*n.
#//
#// A060888         n^6-n^5+n^4-n^3+n^2-n+1.      -- general form of this
#//
#// A048736         Dana Scott's sequence: a(n) = (a(n-2) + a(n-1) * a(n-3)) / a(n-4), a(0) = a(1) = a(2) = a(3) = 1.
#//
#// A022095         Fibonacci sequence beginning 1 5.
#//                 a(n) = ((2*sqrt(5)-1)*(((1+sqrt(5))/2)^(n+1)) + (2*sqrt(5)+1)*(((1-sqrt(5))/2)^(n+1)))/(sqrt(5)).
#//
#// A005894         Centered tetrahedral numbers.
#//                 a(n)=(2*n+1)*(n^2+n+3)/3
#//
#// A015447         Generalized Fibonacci numbers: a(n) = a(n-1) + 11*a(n-2).
#//                 a(n)={[ (1+3*sqrt(5))/2 ]^(n+1) - [ (1-3*sqrt(5))/2 ]^(n+1)}/3*sqrt(5).
#//                 LinearRecurrence[{1, 11}, {1, 1}, 30]
#//                 CoefficientList[Series[ 1/(1-x-11 x^2), {x, 0, 50}], x]
#//
#// A046176         Indices of square numbers which are also hexagonal.
#//
#// A056105         First spoke of a hexagonal spiral.
#//
#// A006522         4-dimensional analogue of centered polygonal numbers. Also number of regions created by sides and diagonals of n-gon in general position.
#//                 a(n)=binomial(n, 4)+ binomial(n-1, 2)
#//
#// A022086         Fibonacci sequence beginning 0 3.
#//                 a(n) = round( (6phi-3)/5 phi^n ) (works for n>2)
#//
#// A069778         q-factorial numbers 3!_q.
#//
#// A005021         Random walks (binomial transform of A006054).
#//
#// A074584         Esanacci ("6-anacci") numbers.
#//                 LinearRecurrence[{1, 1, 1, 1, 1, 1}, {6, 1, 3, 7, 15, 31}, 50]
#//
#// A195142         Concentric 10-gonal numbers.
#//
#// A000453         Stirling numbers of the second kind, S(n,4).
#//
#// A005915         Hexagonal prism numbers: (n + 1)*(3*n^2 + 3*n + 1).
#//
#// A015442         Generalized Fibonacci numbers: a(n) = a(n-1) + 7 a(n-2), a(0)=0, a(1)=1.
#//                 a(n) = ( ((1+sqrt(29))/2)^(n+1) - ((1-sqrt(29))/2)^(n+1) )/sqrt(29)
#//
#// A002418         4-dimensional figurate numbers: (5*n-1)*binomial(n+2,3)/4.
#//
#// A005165         Alternating factorials: n! - (n-1)! + (n-2)! - ... 1!.
#//
#// A006007         4-dimensional analogue of centered polygonal numbers: a(n) = n(n+1)*(n^2+n+4)/12.
#//
#// A104621         Heptanacci-Lucas numbers.
#//


#//******************************************************************************
#//
#//  getNthStellaOctangulaNumber
#//
#//  Stel(n) = Oct(n) + 8 Tet(n-1)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthStellaOctangulaNumber( n ):
    return polyval( [ 4, 0, -2 ], n )


#//******************************************************************************
#//
#//  getNthCenteredCube
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthCenteredCubeNumber( n ):
    return fadd( power( n, 3 ), power( fsub( n, 1 ), 3 ) )


#//******************************************************************************
#//
#//  getNthTruncatedOctahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  16n^3 - 33n^2 + 24n - 6
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedOctahedralNumber( n ):
    return polyval( [ 16, -33, 24, 6 ], n )


#//******************************************************************************
#//
#//  getNthRhombicDodecahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  Rho(n) = CCub(n) + 6 Pyr(n-1)
#//
#//  4n^3 + 6n^2 + 4n + 1
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthRhombicDodecahedralNumber( n ):
    return polyval( [ 4, 6, 4, 1 ], n )


#//******************************************************************************
#//
#//  getNthPentatopeNumber
#//
#//  1/24n ( n + 1 )( n + 2 )( n + 3 )
#//
#//  1/24 n^4 + 1/4 n^3 + 11/24 n^2 + 1/4 n
#//
#//  1/24 ( n^4 + 6 n^3 + 11 n^2 + 6n )
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPentatopeNumber( n ):
    return fdiv( polyval( [ 1, 6, 11, 6, 0 ], n ), 24 )


#//******************************************************************************
#//
#//  getNthPolytopeNumber
#//
#//  d = dimension
#//
#//  (1/(d-1)!) PI k=0 to n-1 (n+k)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPolytopeNumber( n, d ):
    result = n
    m = n + 1

    for i in arange( 1, d - 1 ):
        result = fmul( result, m )
        m += 1

    return fdiv( result, fac( d - 1 ) )


#//******************************************************************************
#//
#//  getNthDelannoyNumber
#//
#//******************************************************************************

def getNthDelannoyNumber( n ):
    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


#//******************************************************************************
#//
#//  getNthSchroederNumber
#//
#//******************************************************************************

def getNthSchroederNumber( n ):
    if n == 1:
        return 1

    # TODO: raise exception for n < 0 !

    n = fsub( n, 1 )

    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fdiv( fprod( [ power( 2, k ), binomial( n, k ),
                                              binomial( n, fsub( k, 1 ) ) ] ), n ) )

    return result


#//******************************************************************************
#//
#//  getNthMotzkinNumber
#//
#//  http://oeis.org/A001006
#//
#//  a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
#//
#//******************************************************************************

def getNthMotzkinNumber( n ):
    result = 0

    for j in arange( 0, floor( fdiv( n, 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                      binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


#//******************************************************************************
#//
#//  getNthPadovanNumber
#//
#//  Padovan sequence: a(n) = a(n-2) + a(n-3) with a(0)=1, a(1)=a(2)=0.
#//
#//  http://oeis.org/A000931
#//
#//  a(n) = (r^n)/(2r+3) + (s^n)/(2s+3) + (t^n)/(2t+3) where r, s, t are the
#//  three roots of x^3-x-1
#//
#//  http://www.wolframalpha.com/input/?i=solve+x^3-x-1
#//
#//  Unfortunately, the roots are scary-complicated, but it's a non-iterative
#//  formula, so I'll use it.
#//
#//  Wikipedia leaves off the first 4 terms, but Sloane's includes them.
#//  Wikipedia cites Ian Stewart and Mathworld, and I'll use their definition.
#//
#//******************************************************************************

def getNthPadovanNumber( arg ):
    n = fadd( arg, 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    e = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, e ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, e ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, e ) ) )

    return round( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                              fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                              fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )


#//******************************************************************************
#//
#//  getPrimorial
#//
#//******************************************************************************

def getPrimorial( n ):
    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result


#//******************************************************************************
#//
#//  getPermutations
#//
#//******************************************************************************

def getPermutations( n, r ):
    if ( r > n ):
        raise ValueError( 'number of elements (%d) cannot exceed the size of the set (%d)' % ( r, n ) )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


#//******************************************************************************
#//
#//  convertFromContinuedFraction
#//
#//******************************************************************************

def convertFromContinuedFraction( i ):
    if not isinstance( i, list ):
        i = [ i ]

    fraction = ContinuedFraction( i ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


#//******************************************************************************
#//
#//  interpretAsFraction
#//
#//******************************************************************************

def interpretAsFraction( i, j ):
    fraction = ContinuedFraction( i, maxterms=j ).getFraction( )
    return [ fraction.numerator, fraction.denominator ]


#//******************************************************************************
#//
#//  interpretAsBase
#//
#//  This is a list operator so if the integer argument (base) is also a list,
#//  we need to handle that explicitly here.
#//
#//******************************************************************************

def interpretAsBase( args, base ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ interpretAsBase( i, base ) for i in args ]
        else:
            args.reverse( )
    else:
        args = [ args ]

    if isinstance( base, list ):
        return [ interpretAsBase( args, i ) for i in base ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


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


#//******************************************************************************
#//
#//  getPlasticConstant
#//
#//******************************************************************************

def getPlasticConstant( ):
    term = fmul( 12, sqrt( 69 ) )
    return fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 )


#//******************************************************************************
#//
#//  solveQuadraticPolynomial
#//
#//******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    if a == 0:
        if b == 0:
            raise ValueError( 'invalid equation, no variable coefficients' )
        else:
            # linear equation, one root
            return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


#//******************************************************************************
#//
#//  solveCubicPolynomial
#//
#//  Adapted from http://www.1728.org/cubic2.htm
#//
#//******************************************************************************

def solveCubicPolynomial( a, b, c, d ):
    if a == 0:
        return solveQuadraticPolynomial( b, c, d )

    f = fdiv( fsub( fdiv( fmul( 3, c ), a ), fdiv( power( b, 2 ), power( a, 2 ) ) ), 3 )

    g = fdiv( fadd( fsub( fdiv( fmul( 2, power( b, 3 ) ), power( a, 3 ) ),
                          fdiv( fprod( [ 9, b, c ] ), power( a, 2 ) ) ),
                    fdiv( fmul( 27, d ), a ) ), 27 )
    h = fadd( fdiv( power( g, 2 ), 4 ), fdiv( power( f, 3 ), 27 ) )

    # all three roots are the same
    if h == 0:
        x1 = fneg( root( fdiv( d, a ), 3 ) )
        x2 = x1
        x3 = x2
    # two imaginary and one real root
    elif h > 0:
        r = fadd( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if r < 0:
            s = fneg( root( fneg( r ), 3 ) )
        else:
            s = root( r, 3 )

        t = fsub( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if t < 0:
            u = fneg( root( fneg( t ), 3 ) )
        else:
            u = root( t, 3 )

        x1 = fsub( fadd( s, u ), fdiv( b, fmul( 3, a ) ) )

        real = fsub( fdiv( fneg( fadd( s, u ) ), 2 ), fdiv( b, fmul( 3, a ) ) )
        imaginary = fdiv( fmul( fsub( s, u ), sqrt( 3 ) ), 2 )

        x2 = mpc( real, imaginary )
        x3 = mpc( real, fneg( imaginary ) )
    # all real roots
    else:
        j = sqrt( fsub( fdiv( power( g, 2 ), 4 ), h ) )
        k = acos( fneg( fdiv( g, fmul( 2, j ) ) ) )

        if j < 0:
            l = fneg( root( fneg( j ), 3 ) )
        else:
            l = root( j, 3 )

        m = cos( fdiv( k, 3 ) )
        n = fmul( sqrt( 3 ), sin( fdiv( k, 3 ) ) )
        p = fneg( fdiv( b, fmul( 3, a ) ) )

        x1 = fsub( fmul( fmul( 2, l ), cos( fdiv( k, 3 ) ) ), fdiv( b, fmul( 3, a ) ) )
        x2 = fadd( fmul( fneg( l ), fadd( m, n ) ), p )
        x3 = fadd( fmul( fneg( l ), fsub( m, n ) ), p )

    return [ chop( x1 ), chop( x2 ), chop( x3 ) ]


#//******************************************************************************
#//
#//  solveQuarticPolynomial
#//
#//  Adapted from http://www.1728.org/quartic2.htm
#//
#//******************************************************************************

def solveQuarticPolynomial( _a, _b, _c, _d, _e ):
    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )

    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    elif _b == 0 and _c == 0 and _d == 0:
        e = fdiv( _e, _a )

        f = root( _a, 4 )

        x1 = fdiv( root( fneg( e ), 4 ), f )
        x2 = fdiv( fneg( root( fneg( e ), 4 ) ), f )
        x3 = fdiv( mpc( 0, root( fneg( e ), 4 ) ), f )
        x4 = fdiv( mpc( 0, fneg( root( fneg( e ), 4 ) ) ), f )

        return [ x1, x2, x3, x4 ]

    # otherwise we have a regular quartic to solve
    a = 1
    b = fdiv( _b, _a )
    c = fdiv( _c, _a )
    d = fdiv( _d, _a )
    e = fdiv( _e, _a )

    # we turn the equation into a cubic that we can solve
    f = fsub( c, fdiv( fmul( 3, power( b, 2 ) ), 8 ) )
    g = fsum( [ d, fdiv( power( b, 3 ), 8 ), fneg( fdiv( fmul( b, c ), 2 ) ) ] )
    h = fsum( [ e, fneg( fdiv( fmul( 3, power( b, 4 ) ), 256 ) ),
                fmul( power( b, 2 ), fdiv( c, 16 ) ), fneg( fdiv( fmul( b, d ), 4 ) ) ] )

    y1, y2, y3 = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                       fneg( fdiv( power( g, 2 ), 64 ) ) )

    # pick two non-zero roots, if there are two imaginary roots, use them
    if im( y1 ) != 0:
        root1 = y1

        if y2 == 0 or im( y2 ) == 0:
            root2 = y3
        else:
            root2 = y2
    elif y1 == 0:
        root1 = y2
        root2 = y3
    elif y2 == 0:
        root1 = y1
        root2 = y3
    else:
        root1 = y2
        root2 = y3

    # more variables...
    p = sqrt( root1 )
    q = sqrt( root2 )
    r = fdiv( fneg( g ), fprod( [ 8, p, q ] ) )
    s = fneg( fdiv( b, 4 ) )

    # put together the 4 roots
    x1 = fsum( [ p, q, r, s ] )
    x2 = fsum( [ p, fneg( q ), fneg( r ), s ] )
    x3 = fsum( [ fneg( p ), q, fneg( r ), s ] )
    x4 = fsum( [ fneg( p ), fneg( q ), r, s ] )

    return [ chop( x1 ), chop( x2 ), chop( x3 ), chop( x4 ) ]


#//******************************************************************************
#//
#//  getChampernowne
#//
#//******************************************************************************

def getChampernowne( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += convertToBaseN( count, g.inputRadix, False, defaultNumerals )
        count += 1

    return convertToBase10( '0', result, g.inputRadix )


#//******************************************************************************
#//
#//  getCopelandErdos
#//
#//******************************************************************************

def getCopelandErdos( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += str( getNthPrime( count ) )
        count += 1

    return convertToBase10( '0', result, 10 )


#//******************************************************************************
#//
#//  makeImaginary
#//
#//******************************************************************************

def makeImaginary( n ):
    return mpc( real='0.0', imag=n )


#//******************************************************************************
#//
#//  isSquare
#//
#//******************************************************************************

def isSquare( n ):
    sqrtN = sqrt( n )

    return 1 if sqrtN == floor( sqrtN ) else 0


#//******************************************************************************
#//
#//  addPolynomials
#//
#//******************************************************************************

def addPolynomials( a, b ):
    result = Polynomial( a )
    result += Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  multiplyPolynomials
#//
#//******************************************************************************

def multiplyPolynomials( a, b ):
    result = Polynomial( a )
    result *= Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  evaluatePolynomial
#//
#//******************************************************************************

def evaluatePolynomial( a, b ):
    if not isinstance( a, list ):
        a = [ a ]

    return polyval( a, b )


#//******************************************************************************
#//
#//  solvePolynomial
#//
#//******************************************************************************

def solvePolynomial( args ):
    if len( args ) < 2:
        raise ValueError( "'solve' requires at least an order-1 polynomial (i.e., 2 terms)" )

    return polyroots( args )


#//******************************************************************************
#//
#//  calculatePowerTower
#//
#//******************************************************************************

def calculatePowerTower( args ):
    result = args[ -1 ]

    for i in args[ -1 : : -1 ]:
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  calculatePowerTower2
#//
#//******************************************************************************

def calculatePowerTower2( args ):
    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  getAlternatingSum
#//
#//******************************************************************************

def getAlternatingSum( args ):
    for i in range( 1, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getAlternatingSum2
#//
#//******************************************************************************

def getAlternatingSum2( args ):
    for i in range( 0, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getGCDForTwo
#//
#//******************************************************************************

def getGCDForTwo( a, b ):
    a, b = fabs( a ), fabs( b )

    while a:
        b, a = a, fmod( b, a )

    return b


#//******************************************************************************
#//
#//  getGCD
#//
#//******************************************************************************

def getGCD( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getGCD[ arg ] for arg in args ]
        else:
            result = max( args )

            for pair in itertools.permutations( args, 2 ):
                gcd = getGCDForTwo( *pair )

                if gcd < result:
                    result = gcd

                return result
    else:
        return args


#//******************************************************************************
#//
#//  multiplyListOfPolynomials
#//
#//******************************************************************************

def multiplyListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    for i in range( 1, len( args ) ):
        if isinstance( args[ i ], list ) and isinstance( args[ i ][ 0 ], list ):
            pass  # dunno what to do here
        else:
            result *= Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  addListOfPolynomials
#//
#//******************************************************************************

def addListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    #print( 'addListOfPolynomials' )
    #print( args[ 0 ] )
    #print( result.getCoefficients( ) )

    for i in range( 1, len( args ) ):
        result += Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  getGreedyEgyptianFraction
#//
#//******************************************************************************

def getGreedyEgyptianFraction( n, d ):
    if n > d:
        raise ValueError( "'egypt' requires the numerator to be smaller than the denominator" )

    # Create a list to store the Egyptian fraction representation.
    result = [ ]

    rational = Fraction( int( n ), int( d ) )

    # Now, iteratively subtract out the largest unit fraction that may be
    # subtracted out until we arrive at a unit fraction.
    while True:
        # If the rational number has numerator 1, we're done.
        if rational.numerator == 1:
            result.append( rational )
            return result

        # Otherwise, find the largest unit fraction less than the current rational number.
        # This is given by the ceiling of the denominator divided by the numerator.
        unitFraction = Fraction( 1, rational.denominator // rational.numerator + 1 )

        result.append( unitFraction )

        # Subtract out this unit fraction.
        rational = rational - unitFraction

    return result


#//******************************************************************************
#//
#//  getNow
#//
#//******************************************************************************

def getNow( ):
    return arrow.now( )


#//******************************************************************************
#//
#//  getToday
#//
#//******************************************************************************

def getToday( ):
    now = datetime.datetime.now( )
    return arrow.Arrow( now.year, now.month, now.day )


#//******************************************************************************
#//
#//  convertToUnixTime
#//
#//******************************************************************************

def convertToUnixTime( args ):
    argList = args

    if len( argList ) == 1:
        argList.append( 1 )

    if len( argList ) == 2:
        argList.append( 1 )

    if len( argList ) == 3:
        argList.append( 0 )

    if len( argList ) == 4:
        argList.append( 0 )

    if len( argList ) == 5:
        argList.append( 0 )

    try:
        result = calendar.timegm( args[ 0 : 6 ] )
    except OverflowError as error:
        print( 'rpn:  out of range error for \'tounixtime\'' )
        return 0

    return result


#//******************************************************************************
#//
#//  convertFromUnixTime
#//
#//******************************************************************************

def convertFromUnixTime( n ):
    try:
        unixtime = time.gmtime( n )
    except OverflowError as error:
        print( 'rpn:  out of range error for \'fromunixtime\'' )
        return 0

    return [ unixtime.tm_year, unixtime.tm_mon, unixtime.tm_mday,
             unixtime.tm_hour, unixtime.tm_min, unixtime.tm_sec ]


#//******************************************************************************
#//
#//  dumpOperators
#//
#//******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )

    print( 'special operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  dumpAliases
#//
#//******************************************************************************

def dumpAliases( ):
    for alias in sorted( [ key for key in operatorAliases ] ):
        print( alias, operatorAliases[ alias ] )

    return len( operatorAliases )


#//******************************************************************************
#//
#//  printStats
#//
#//******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:13,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


#//******************************************************************************
#//
#//  dumpStats
#//
#//******************************************************************************

def dumpStats( ):
    if g.unitConversionMatrix is None:
        loadUnitConversionMatrix( )

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) + len( modifiers ) ) )
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( g.dataPath ), 'small primes' )
    printStats( loadLargePrimes( g.dataPath ), 'large primes' )
    printStats( loadIsolatedPrimes( g.dataPath ), 'isolated primes' )
    printStats( loadTwinPrimes( g.dataPath ), 'twin primes' )
    printStats( loadBalancedPrimes( g.dataPath ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( g.dataPath ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( g.dataPath ), 'triple balanced primes' )
    printStats( loadSophiePrimes( g.dataPath ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( g.dataPath ), 'cousin primes' )
    printStats( loadSexyPrimes( g.dataPath ), 'sexy primes' )
    printStats( loadTripletPrimes( g.dataPath ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( g.dataPath ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( g.dataPath ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( g.dataPath ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( g.dataPath ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( g.dataPath ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  incrementNestedListLevel
#//
#//  Unlike all other operators, '[' and ']' change global state.
#//
#//******************************************************************************

def incrementNestedListLevel( valueList ):
    g.nestedListLevel += 1

    valueList.append( list( ) )


#//******************************************************************************
#//
#//  decrementNestedListLevel
#//
#//******************************************************************************

def decrementNestedListLevel( valueList ):
    g.nestedListLevel -= 1

    if g.nestedListLevel < 0:
        raise ValueError( "negative list level (too many ']'s)" )


#//******************************************************************************
#//
#//  duplicateTerm
#//
#//******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, int( count ) ):
        if isinstance( value, list ):
            for i in value:
                valueList.append( i )
        else:
            valueList.append( value )


#//******************************************************************************
#//
#//  getPrevious
#//
#//******************************************************************************

def getPrevious( valueList ):
    valueList.append( valueList[ -1 ] )


#//******************************************************************************
#//
#//  duplicateTerm
#//
#//******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, int( count ) ):
        if isinstance( value, list ):
            for i in value:
                valueList.append( i )
        else:
            valueList.append( value )


#//******************************************************************************
#//
#//  appendLists
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  loadResult
#//
#//******************************************************************************

def loadResult( valueList ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'result.pckl.bz2', 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError:
        result = mapmathify( 0 )

    return result


#//******************************************************************************
#//
#//  saveResult
#//
#//******************************************************************************

def saveResult( result ):
    with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'result.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( result, pickleFile )


#//******************************************************************************
#//
#//  alternateSigns
#//
#//******************************************************************************

def alternateSigns( n ):
    for i in range( 1, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  alternateSigns2
#//
#//******************************************************************************

def alternateSigns2( n ):
    for i in range( 0, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  expandRange
#//
#//******************************************************************************

def expandRange( start, end ):
    if start > end:
        step = -1
    else:
        step = 1

    result = list( )

    for i in arange( start, end + step, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandSteppedRange
#//
#//******************************************************************************

def expandSteppedRange( start, end, step ):
    result = list( )

    for i in arange( start, end + 1, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandGeometricRange
#//
#//******************************************************************************

def expandGeometricRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = fmul( value, step )

    return result


#//******************************************************************************
#//
#//  expandExponentialRange
#//
#//******************************************************************************

def expandExponentialRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = power( value, step )

    return result


#//******************************************************************************
#//
#//  interleave
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  makeUnion
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  makeIntersection
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getIndexOfMax
#//
#//******************************************************************************

def getIndexOfMax( arg ):
    maximum = -inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] > maximum:
            maximum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  getIndexOfMin
#//
#//******************************************************************************

def getIndexOfMin( arg ):
    minimum = inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] < minimum:
            minimum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  unlist
#//
#//******************************************************************************

def unlist( valueList ):
    arg = valueList.pop( )

    if isinstance( arg, list ):
        for i in arg:
            valueList.append( i )
    else:
        valueList.append( arg )


#//******************************************************************************
#//
#//  flatten
#//
#//  http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
#//
#//******************************************************************************

def _flatten( L, containers=( list, tuple ) ):
    i = 0

    while i < len( L ):
        while isinstance( L[ i ], containers ):
            if not L[ i ]:
                L.pop( i )
                i -= 1
                break
            else:
                L[ i : i + 1 ] = ( L[ i ] )
        i += 1
    return L


def flatten( valueList ):
    valueList.append( _flatten( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getListElement
#//
#//******************************************************************************

def getListElement( arg, index ):
    if isinstance( arg, list ):
        return arg[ int( index ) ]
    else:
        return arg
        # TODO: throw exception if index > 0


#//******************************************************************************
#//
#//  getPrimes
#//
#//******************************************************************************

def getPrimes( value, count ):
    result = list( )

    for i in getNthPrimeRange( value, count ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  getNthLinearRecurrence
#//
#//  nth element of Fibonacci sequence = rpn [ 1 1 ] 1 n
#//  nth element of Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n
#//
#//******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    if not isinstance( recurrence, list ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, list ):
        seeds = [ seeds ]

    if len( seeds ) == 0:
        raise ValueError( 'internal error:  for operator \'linearrecur\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getNthLinearRecurrence( recurrence[ : i ], seeds, i ) )

    if isinstance( n, list ):
        return [ getNthLinearRecurrence( recurrence, seeds, i ) for i in n ]

    if n < len( seeds ):
        return seeds[ int( n ) - 1 ]
    else:
        if len( recurrence ) == 0:
            raise ValueError( 'internal error:  for operator \'linearrecur\', recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in arange( len( seeds ), n ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

            result.append( newValue )
            del result[ 0 ]

        return result[ -1 ]


#//******************************************************************************
#//
#//  countElements
#//
#//******************************************************************************

def countElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( countElements( args[ i ] ) )

        return result
    else:
        return len( args )


#//******************************************************************************
#//
#//  getListDiffs
#//
#//******************************************************************************

def getListDiffs( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListDiffs( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fsub( args[ i + 1 ], args[ i ] ) )

    return result


#//******************************************************************************
#//
#//  getUniqueElements
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  sortAscending
#//
#//******************************************************************************

def sortAscending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ] ) )

        return result
    else:
        return sorted( args )


#//******************************************************************************
#//
#//  sortDescending
#//
#//******************************************************************************

def sortDescending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ], reverse=True ) )

        return result
    else:
        return sorted( args, reverse=True )


#//******************************************************************************
#//
#//  getStandardDeviation
#//
#//******************************************************************************

def getStandardDeviation( args ):
    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fsum( dev ) / len( dev ) )


#//******************************************************************************
#//
#//  getCurrentArgList
#//
#//******************************************************************************

def getCurrentArgList( valueList ):
    argList = valueList

    for i in range( 0, g.nestedListLevel ):
        argList = argList[ -1 ]

    return argList


#//******************************************************************************
#//
#//  estimate
#//
#//******************************************************************************

def estimate( measurement ):
    if isinstance( measurement, Measurement ):
        unitType = getUnitType( measurement.getUnitName( ) )
        unitTypeOutput = removeUnderscores( unitType )

        unitTypeInfo = g.basicUnitTypes[ unitType ]

        unit = Measurement( 1, { unitTypeInfo.baseUnit : 1 } )
        value = mpf( Measurement( measurement.convertValue( unit ), unit.getUnits( ) ) )

        if len( unitTypeInfo.estimateTable ) == 0:
            return 'No estimates are available for this unit type (' + unitTypeOutput + ').'

        matchingKeys = [ key for key in unitTypeInfo.estimateTable if key <= mpf( value ) ]

        if len( matchingKeys ) == 0:
            estimateKey = min( key for key in unitTypeInfo.estimateTable )

            multiple = fdiv( estimateKey, value )

            return 'approximately ' + nstr( multiple, 3 ) + ' times smaller than ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
        else:
            estimateKey = max( matchingKeys )

            multiple = fdiv( value, estimateKey )

            return 'approximately ' + nstr( multiple, 3 ) + ' times ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
    elif isinstance( measurement, arrow.Arrow ):
        return measurement.humanize( )
    else:
        raise TypeError( 'incompatible type for estimating' )


#//******************************************************************************
#//
#//  convertToDMS
#//
#//******************************************************************************

def convertToDMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'degree' : 1 } ), Measurement( 1, { 'arcminute' : 1 } ),
                              Measurement( 1, { 'arcsecond' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToHMS
#//
#//******************************************************************************

def convertToHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToDHMS
#//
#//******************************************************************************

def convertToDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'day' : 1 } ), Measurement( 1, { 'hour' : 1 } ),
                              Measurement( 1, { 'minute' : 1 } ), Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToYDHMS
#//
#//******************************************************************************

def convertToYDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'year' : 1 } ), Measurement( 1, { 'day' : 1 } ),
                              Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertUnits
#//
#//******************************************************************************

def convertUnits( unit1, unit2 ):
    if not isinstance( unit1, Measurement ):
        raise ValueError( 'cannot convert non-measurements' )

    if isinstance( unit2, list ):
        return unit1.convertValue( unit2 )
    elif isinstance( unit2, str ):
        measurement = Measurement( 1, { unit2 : 1 } )

        return Measurement( unit1.convertValue( measurement ), unit2 )
    else:
        debugPrint( 'convertUnits' )
        debugPrint( 'unit1:', unit1.getTypes( ) )
        debugPrint( 'unit2:', unit2.getTypes( ) )

        return Measurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                            unit2.getUnitName( ), unit2.getPluralUnitName( ) )


#//******************************************************************************
#//
#//  makeTime
#//
#//******************************************************************************

def makeTime( n ):
    if len( n ) == 1:
        n.append( 1 )

    if len( n ) == 2:
        n.append( 1 )
    elif len( n ) > 7:
        n = n[ : 7 ]

    return arrow.get( *n )


#//******************************************************************************
#//
#//  getWeekDay
#//
#//******************************************************************************

def getWeekday( n ):
    return [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ][ n.weekday( ) ]


#//******************************************************************************
#//
#//  modifiers are operators that directly modify the argument stack instead of
#//  just returning a value.
#//
#//  '[' and ']' are special arguments that change global state in order to
#//  create list operands.
#//
#//******************************************************************************

modifiers = {
    'dup'           : OperatorInfo( duplicateTerm, 2, [ Measurement ] ),
    'flatten'       : OperatorInfo( flatten, 1, [ ] ),
    'previous'      : OperatorInfo( getPrevious, 1, [ ] ),
    'unlist'        : OperatorInfo( unlist, 1, [ ] ),
    '['             : OperatorInfo( incrementNestedListLevel, 0, [ ] ),
    ']'             : OperatorInfo( decrementNestedListLevel, 0, [ ] ),
}


#//******************************************************************************
#//
#//  listOperators are operators that handle whether or not an argument is a
#//  list themselves (because they require a list argument).  Unlike regular
#//  operators, we don't want listOperators permutated over each list element,
#//  and if we do for auxillary arguments, these operator handlers will do that
#//  themselves.
#//
#//******************************************************************************

listOperators = {
    'append'        : OperatorInfo( appendLists, 2, [ ] ),
    'altsign'       : OperatorInfo( alternateSigns, 1, [ ] ),
    'altsign2'      : OperatorInfo( alternateSigns2, 1, [ ] ),
    'altsum'        : OperatorInfo( getAlternatingSum, 1, [ ] ),
    'altsum2'       : OperatorInfo( getAlternatingSum2, 1, [ ] ),
    'base'          : OperatorInfo( interpretAsBase, 2, [ ] ),
    'cf'            : OperatorInfo( convertFromContinuedFraction, 1, [ ] ),
    'convert'       : OperatorInfo( convertUnits, 2, [ ] ),
    'count'         : OperatorInfo( countElements, 1, [ ] ),
    'diffs'         : OperatorInfo( getListDiffs, 1, [ ] ),
    'gcd'           : OperatorInfo( getGCD, 1, [ ] ),
    'interleave'    : OperatorInfo( interleave, 2, [ ] ),
    'intersection'  : OperatorInfo( makeIntersection, 2, [ ] ),
    'linearrecur'   : OperatorInfo( getNthLinearRecurrence, 3, [ ] ),
    'maketime'      : OperatorInfo( makeTime, 1, [ Measurement ] ),
    'max'           : OperatorInfo( max, 1, [ ] ),
    'maxindex'      : OperatorInfo( getIndexOfMax, 1, [ ] ),
    'mean'          : OperatorInfo( lambda n: fdiv( fsum( n ), len( n ) ), 1, [ ] ),
    'min'           : OperatorInfo( min, 1, [ ] ),
    'minindex'      : OperatorInfo( getIndexOfMin, 1, [ ] ),
    'nonzero'       : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e != 0 ], 1, [ ] ),
    'polyadd'       : OperatorInfo( addPolynomials, 2, [ ] ),
    'polymul'       : OperatorInfo( multiplyPolynomials, 2, [ ] ),
    'polyprod'      : OperatorInfo( multiplyListOfPolynomials, 1, [ ] ),
    'polysum'       : OperatorInfo( addListOfPolynomials, 1, [ ] ),
    'polyval'       : OperatorInfo( evaluatePolynomial, 2, [ ] ),
    'product'       : OperatorInfo( fprod, 1, [ ] ),
    'result'        : OperatorInfo( loadResult, 0, [ ] ),
    'solve'         : OperatorInfo( solvePolynomial, 1, [ ] ),
    'sort'          : OperatorInfo( sortAscending, 1, [ ] ),
    'sortdesc'      : OperatorInfo( sortDescending, 1, [ ] ),
    'stddev'        : OperatorInfo( getStandardDeviation, 1, [ ] ),
    'sum'           : OperatorInfo( sum, 1, [ ] ),
    'tounixtime'    : OperatorInfo( convertToUnixTime, 1, [ ] ),
    'tower'         : OperatorInfo( calculatePowerTower, 1, [ ] ),
    'tower2'        : OperatorInfo( calculatePowerTower2, 1, [ ] ),
    'union'         : OperatorInfo( makeUnion, 2, [ ] ),
    'unique'        : OperatorInfo( getUniqueElements, 1, [ ] ),
    'unpack'        : OperatorInfo( unpackInteger, 2, [ ] ),
    'zero'          : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e == 0 ], 1, [ ] ),
}


#//******************************************************************************
#//
#//  operators
#//
#//  Regular operators expect zero or more single values and if those arguments
#//  are lists, rpn will iterate calls to the operator handler for each element
#//  in the list.   Multiple lists for arguments are not permutated.  Instead,
#//  the operator handler is called for each element in the first list, along
#//  with the nth element of each other argument that is also a list.
#//
#//******************************************************************************

operators = {
    'abs'           : OperatorInfo( fabs, 1, [ Measurement ] ),
    'acos'          : OperatorInfo( lambda n: performTrigOperation( n, acos ), 1, [ ] ),
    'acosh'         : OperatorInfo( lambda n: performTrigOperation( n, acosh ), 1, [ ] ),
    'acot'          : OperatorInfo( lambda n: performTrigOperation( n, acot ), 1, [ ] ),
    'acoth'         : OperatorInfo( lambda n: performTrigOperation( n, acoth ), 1, [ ] ),
    'acsc'          : OperatorInfo( lambda n: performTrigOperation( n, acsc ), 1, [ ] ),
    'acsch'         : OperatorInfo( lambda n: performTrigOperation( n, acsch ), 1, [ ] ),
    'add'           : OperatorInfo( add, 2, [ Measurement, arrow.Arrow ] ),
    'altfac'        : OperatorInfo( getNthAlternatingFactorial, 1, [ ] ),
    'and'           : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x & y ), 2, [ ] ),
    'apery'         : OperatorInfo( apery, 0, [ ] ),
    'aperynum'      : OperatorInfo( getNthAperyNumber, 1, [ ] ),
    'asec'          : OperatorInfo( lambda n: performTrigOperation( n, asec ), 1, [ ] ),
    'asech'         : OperatorInfo( lambda n: performTrigOperation( n, asech ), 1, [ ] ),
    'asin'          : OperatorInfo( lambda n: performTrigOperation( n, asin ), 1, [ ] ),
    'asinh'         : OperatorInfo( lambda n: performTrigOperation( n, asinh ), 1, [ ] ),
    'atan'          : OperatorInfo( lambda n: performTrigOperation( n, atan ), 1, [ ] ),
    'atanh'         : OperatorInfo( lambda n: performTrigOperation( n, atanh ), 1, [ ] ),
    'avogadro'      : OperatorInfo( lambda: mpf( '6.02214179e23' ), 0, [ ] ),
    'balanced'      : OperatorInfo( getNthBalancedPrime, 1, [ ] ),
    'balanced_'     : OperatorInfo( getNthBalancedPrimeList, 1, [ ] ),
    'bell'          : OperatorInfo( bell, 1, [ ] ),
    'bellpoly'      : OperatorInfo( bell, 2, [ ] ),
    'bernoulli'     : OperatorInfo( bernoulli, 1, [ ] ),
    'binomial'      : OperatorInfo( binomial, 2, [ ] ),
    'carol'         : OperatorInfo( lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1, [ ] ),
    'catalan'       : OperatorInfo( lambda n: fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) ), 1, [ ] ),
    'catalans'      : OperatorInfo( catalan, 0, [ ] ),
    'cdecagonal'    : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 10 ), 1, [ ] ),
    'cdecagonal?'   : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 10 ), 1, [ ] ),
    'ceiling'       : OperatorInfo( ceil, 1, [ Measurement ] ),
    'centeredcube'  : OperatorInfo( getNthCenteredCubeNumber, 1, [ ] ),
    'champernowne'  : OperatorInfo( getChampernowne, 0, [ ] ),
    'char'          : OperatorInfo( lambda n: convertToSignedInt( n , 8 ), 1, [ ] ),
    'cheptagonal'   : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 7 ), 1, [ ] ),
    'cheptagonal?'  : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 7 ), 1, [ ] ),
    'chexagonal'    : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 6 ), 1, [ ] ),
    'cnonagonal'    : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 9 ), 1, [ ] ),
    'cnonagonal?'   : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 9 ), 1, [ ] ),
    'coctagonal'    : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 8 ), 1, [ ] ),
    'coctagonal?'   : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 8 ), 1, [ ] ),
    'copeland'      : OperatorInfo( getCopelandErdos, 0, [ ] ),
    'cos'           : OperatorInfo( lambda n: performTrigOperation( n, cos ), 1, [ ] ),
    'cosh'          : OperatorInfo( lambda n: performTrigOperation( n, cosh ), 1, [ ] ),
    'cot'           : OperatorInfo( lambda n: performTrigOperation( n, cot ), 1, [ ] ),
    'coth'          : OperatorInfo( lambda n: performTrigOperation( n, coth ), 1, [ ] ),
    'countbits'     : OperatorInfo( getBitCount, 1, [ ] ),
    'countdiv'      : OperatorInfo( getDivisorCount, 1, [ ] ),
    'cousinprime'   : OperatorInfo( getNthCousinPrime, 1, [ ] ),
    'cpentagonal'   : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 5 ), 1, [ ] ),
    'cpentagonal?'  : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 5 ), 1, [ ] ),
    'cpolygonal'    : OperatorInfo( lambda n, k: getCenteredPolygonalNumber( n, k ), 2, [ ] ),
    'cpolygonal?'   : OperatorInfo( lambda n, k: findCenteredPolygonalNumber( n, k ), 2, [ ] ),
    'csc'           : OperatorInfo( lambda n: performTrigOperation( n, csc ), 1, [ ] ),
    'csch'          : OperatorInfo( lambda n: performTrigOperation( n, csch ), 1, [ ] ),
    'csquare'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 4 ), 1, [ ] ),
    'csquare?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 4 ), 1, [ ] ),
    'ctriangular'   : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 3 ), 1, [ ] ),
    'ctriangular?'  : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 3 ), 1, [ ] ),
    'cube'          : OperatorInfo( lambda n: exponentiate( n, 3 ), 1, [ Measurement ] ),
    'decagonal'     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 10 ), 1, [ ] ),
    'decagonal?'    : OperatorInfo( lambda n: findNthPolygonalNumber( n, 10 ), 1, [ ] ),
    'delannoy'      : OperatorInfo( getNthDelannoyNumber, 1, [ ] ),
    'divide'        : OperatorInfo( divide, 2, [ Measurement ] ),
    'divisors'      : OperatorInfo( getDivisors, 1, [ ] ),
    'dhms'          : OperatorInfo( convertToDHMS, 1, [ Measurement ] ),
    'dms'           : OperatorInfo( convertToDMS, 1, [ Measurement ] ),
    'dodecahedral'  : OperatorInfo( lambda n : polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], n ), 1, [ ] ),
    'double'        : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( n ) ) ) ), 1, [ ] ),
    'doublebal'     : OperatorInfo( getNthDoubleBalancedPrime, 1, [ ] ),
    'doublebal_'    : OperatorInfo( getNthDoubleBalancedPrimeList, 1, [ ] ),
    'doublefac'     : OperatorInfo( fac2, 1, [ ] ),
    'e'             : OperatorInfo( e, 0, [ ] ),
    'egypt'         : OperatorInfo( getGreedyEgyptianFraction, 2, [ ] ),
    'element'       : OperatorInfo( getListElement, 2, [ ] ),
    'estimate'      : OperatorInfo( estimate, 1, [ ] ),
    'euler'         : OperatorInfo( euler, 0, [ ] ),
    'exp'           : OperatorInfo( exp, 1, [ ] ),
    'exp10'         : OperatorInfo( lambda n: power( 10, n ), 1, [ ] ),
    'expphi'        : OperatorInfo( lambda n: power( phi, n ), 1, [ ] ),
    'exprange'      : OperatorInfo( expandExponentialRange, 3, [ ] ),
    'factor'        : OperatorInfo( lambda i: getExpandedFactorList( factor( i ) ), 1, [ ] ),
    'factorial'     : OperatorInfo( fac, 1, [ ] ),
    'fibonacci'     : OperatorInfo( fib, 1, [ ] ),
    'float'         : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( n ) ) ) ), 1, [ ] ),
    'floor'         : OperatorInfo( floor, 1, [ Measurement ] ),
    'fraction'      : OperatorInfo( interpretAsFraction, 2, [ ] ),
    'fromunixtime'  : OperatorInfo( convertFromUnixTime, 1, [ ] ),
    'gamma'         : OperatorInfo( gamma, 1, [ ] ),
    'georange'      : OperatorInfo( expandGeometricRange, 3, [ ] ),
    'glaisher'      : OperatorInfo( glaisher, 0, [ ] ),
    'harmonic'      : OperatorInfo( harmonic, 1, [ ] ),
    'heptagonal'    : OperatorInfo( lambda n: getNthPolygonalNumber( n, 7 ), 1, [ ] ),
    'heptagonal?'   : OperatorInfo( lambda n: findNthPolygonalNumber( n, 7 ), 1, [ ] ),
    'heptanacci'    : OperatorInfo( getNthHeptanacci, 1, [ ] ),
    'hepthex'       : OperatorInfo( getNthHeptagonalHexagonalNumber, 1, [ ] ),
    'heptpent'      : OperatorInfo( getNthHeptagonalPentagonalNumber, 1, [ ] ),
    'heptsquare'    : OperatorInfo( getNthHeptagonalSquareNumber, 1, [ ] ),
    'hepttri'       : OperatorInfo( getNthHeptagonalTriangularNumber, 1, [ ] ),
    'hexagonal'     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 6 ), 1, [ ] ),
    'hexagonal?'    : OperatorInfo( lambda n: findNthPolygonalNumber( n, 6 ), 1, [ ] ),
    'hexanacci'     : OperatorInfo( getNthHexanacci, 1, [ ] ),
    'hexpent'       : OperatorInfo( getNthHexagonalPentagonalNumber, 1, [ ] ),
    'hms'           : OperatorInfo( convertToHMS, 1, [ Measurement ] ),
    'hyper4_2'      : OperatorInfo( tetrateLarge, 2, [ ] ),
    'hyperfac'      : OperatorInfo( hyperfac, 1, [ ] ),
    'hypot'         : OperatorInfo( hypot, 2, [ ] ),
    'i'             : OperatorInfo( makeImaginary, 1, [ ] ),
    'icosahedral'   : OperatorInfo( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], n ), 1, [ ] ),
    'integer'       : OperatorInfo( convertToSignedInt, 2, [ ] ),
    'isdivisible'   : OperatorInfo( lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2, [ ] ),
    'isolated'      : OperatorInfo( getNthIsolatedPrime, 1, [ ] ),
    'isprime'       : OperatorInfo( lambda n: 1 if isPrime( n ) else 0, 1, [ ] ),
    'issquare'      : OperatorInfo( isSquare, 1, [ ] ),
    'itoi'          : OperatorInfo( lambda: exp( fmul( -0.5, pi ) ), 0, [ ] ),
    'jacobsthal'    : OperatorInfo( getNthJacobsthalNumber, 1, [ ] ),
    'khinchin'      : OperatorInfo( khinchin, 0, [ ] ),
    'kynea'         : OperatorInfo( lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1, [ ] ),
    'lah'           : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2, [ ] ),
    'lambertw'      : OperatorInfo( lambertw, 1, [ ] ),
    'leyland'       : OperatorInfo( lambda x, y : fadd( power( x, y ), power( y, x ) ), 2, [ ] ),
    'lgamma'        : OperatorInfo( loggamma, 1, [ ] ),
    'li'            : OperatorInfo( li, 1, [ ] ),
    'ln'            : OperatorInfo( ln, 1, [ ] ),
    'log10'         : OperatorInfo( log10, 1, [ ] ),
    'log2'          : OperatorInfo( lambda n: log( n, 2 ), 1, [ ] ),
    'logxy'         : OperatorInfo( log, 2, [ ] ),
    'long'          : OperatorInfo( lambda n: convertToSignedInt( n , 32 ), 1, [ ] ),
    'longlong'      : OperatorInfo( lambda n: convertToSignedInt( n , 64 ), 1, [ ] ),
    'lucas'         : OperatorInfo( getNthLucasNumber, 1, [ ] ),
    'makecf'        : OperatorInfo( lambda n, k: ContinuedFraction( n, maxterms=k, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2, [ ] ),
    'maxchar'       : OperatorInfo( lambda: ( 1 << 7 ) - 1, 0, [ ] ),
    'maxlong'       : OperatorInfo( lambda: ( 1 << 31 ) - 1, 0, [ ] ),
    'maxlonglong'   : OperatorInfo( lambda: ( 1 << 63 ) - 1, 0, [ ] ),
    'maxquadlong'   : OperatorInfo( lambda: ( 1 << 127 ) - 1, 0, [ ] ),
    'maxshort'      : OperatorInfo( lambda: ( 1 << 15 ) - 1, 0, [ ] ),
    'maxuchar'      : OperatorInfo( lambda: ( 1 << 8 ) - 1, 0, [ ] ),
    'maxulong'      : OperatorInfo( lambda: ( 1 << 32 ) - 1, 0, [ ] ),
    'maxulonglong'  : OperatorInfo( lambda: ( 1 << 64 ) - 1, 0, [ ] ),
    'maxuquadlong'  : OperatorInfo( lambda: ( 1 << 128 ) - 1, 0, [ ] ),
    'maxushort'     : OperatorInfo( lambda: ( 1 << 16 ) - 1, 0, [ ] ),
    'mertens'       : OperatorInfo( mertens, 0, [ ] ),
    'minchar'       : OperatorInfo( lambda: -( 1 << 7 ), 0, [ ] ),
    'minlong'       : OperatorInfo( lambda: -( 1 << 31 ), 0, [ ] ),
    'minlonglong'   : OperatorInfo( lambda: -( 1 << 63 ), 0, [ ] ),
    'minquadlong'   : OperatorInfo( lambda: -( 1 << 127 ), 0, [ ] ),
    'minshort'      : OperatorInfo( lambda: -( 1 << 15 ), 0, [ ] ),
    'minuchar'      : OperatorInfo( lambda: 0, 0, [ ] ),
    'minulong'      : OperatorInfo( lambda: 0, 0, [ ] ),
    'minulonglong'  : OperatorInfo( lambda: 0, 0, [ ] ),
    'minuquadlong'  : OperatorInfo( lambda: 0, 0, [ ] ),
    'minushort'     : OperatorInfo( lambda: 0, 0, [ ] ),
    'modulo'        : OperatorInfo( fmod, 2, [ ] ),
    'motzkin'       : OperatorInfo( getNthMotzkinNumber, 1, [ ] ),
    'multiply'      : OperatorInfo( multiply, 2, [ Measurement ] ),
    'narayana'      : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2, [ ] ),
    'negative'      : OperatorInfo( getNegative, 1, [ Measurement ] ),
    'nonagonal'     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 9 ), 1, [ ] ),
    'nonagonal?'    : OperatorInfo( lambda n: findNthPolygonalNumber( n, 9 ), 1, [ ] ),
    'nonahept'      : OperatorInfo( getNthNonagonalHeptagonalNumber, 1, [ ] ),
    'nonahex'       : OperatorInfo( getNthNonagonalHexagonalNumber, 1, [ ] ),
    'nonaoct'       : OperatorInfo( getNthNonagonalOctagonalNumber, 1, [ ] ),
    'nonapent'      : OperatorInfo( getNthNonagonalPentagonalNumber, 1, [ ] ),
    'nonasquare'    : OperatorInfo( getNthNonagonalSquareNumber, 1, [ ] ),
    'nonatri'       : OperatorInfo( getNthNonagonalTriangularNumber, 1, [ ] ),
    'not'           : OperatorInfo( getInvertedBits, 1, [ ] ),
    'now'           : OperatorInfo( getNow, 0, [ ] ),
    'nspherearea'   : OperatorInfo( getNSphereSurfaceArea, 2, [ Measurement ] ),
    'nsphereradius' : OperatorInfo( getNSphereRadius, 2, [ Measurement ] ),
    'nspherevolume' : OperatorInfo( getNSphereVolume, 2, [ Measurement ] ),
    'nthprime?'     : OperatorInfo( lambda i: findPrime( i )[ 0 ], 1, [ ] ),
    'nthquad?'      : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 0 ], 1, [ ] ),
    'octagonal'     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 8 ), 1, [ ] ),
    'octagonal?'    : OperatorInfo( lambda n: findNthPolygonalNumber( n, 8 ), 1, [ ] ),
    'octahedral'    : OperatorInfo( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], n ), 1, [ ] ),
    'octhept'       : OperatorInfo( getNthOctagonalHeptagonalNumber, 1, [ ] ),
    'octhex'        : OperatorInfo( getNthOctagonalHexagonalNumber, 1, [ ] ),
    'octpent'       : OperatorInfo( getNthOctagonalPentagonalNumber, 1, [ ] ),
    'octsquare'     : OperatorInfo( getNthOctagonalSquareNumber, 1, [ ] ),
    'octtri'        : OperatorInfo( getNthOctagonalTriangularNumber, 1, [ ] ),
    'oeis'          : OperatorInfo( lambda n: downloadOEISSequence( int( n ) ), 1, [ ] ),
    'oeiscomment'   : OperatorInfo( lambda n: downloadOEISText( int( n ), 'C', True ), 1, [ ] ),
    'oeisex'        : OperatorInfo( lambda n: downloadOEISText( int( n ), 'E', True ), 1, [ ] ),
    'oeisname'      : OperatorInfo( lambda n: downloadOEISText( int( n ), 'N', True ), 1, [ ] ),
    'omega'         : OperatorInfo( lambda: lambertw( 1 ), 0, [ ] ),
    'or'            : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2, [ ] ),
    'padovan'       : OperatorInfo( getNthPadovanNumber, 1, [ ] ),
    'parity'        : OperatorInfo( lambda n : getBitCount( n ) & 1, 1, [ ] ),
    'pascal'        : OperatorInfo( getNthPascalLine, 1, [ ] ),
    'pell'          : OperatorInfo( getNthPellNumber, 1, [ ] ),
    'pentagonal'    : OperatorInfo( lambda n: getNthPolygonalNumber( n, 5 ), 1, [ ] ),
    'pentagonal?'   : OperatorInfo( lambda n: findNthPolygonalNumber( n, 5 ), 1, [ ] ),
    'pentanacci'    : OperatorInfo( getNthPentanacci, 1, [ ] ),
    'pentatope'     : OperatorInfo( getNthPentatopeNumber, 1, [ ] ),
    'perm'          : OperatorInfo( getPermutations, 2, [ ] ),
    'phi'           : OperatorInfo( phi, 0, [ ] ),
    'pi'            : OperatorInfo( pi, 0, [ ] ),
    'plastic'       : OperatorInfo( getPlasticConstant, 0, [ ] ),
    'polyarea'      : OperatorInfo( getRegularPolygonArea, 1, [ Measurement ] ),
    'polygamma'     : OperatorInfo( psi, 2, [ ] ),
    'polygonal'     : OperatorInfo( getNthPolygonalNumber, 2, [ ] ),
    'polygonal?'    : OperatorInfo( findNthPolygonalNumber, 2, [ ] ),
    'polylog'       : OperatorInfo( polylog, 2, [ ] ),
    'polyprime'     : OperatorInfo( getNthPolyPrime, 2, [ ] ),
    'polytope'      : OperatorInfo( getNthPolytopeNumber, 2, [ ] ),
    'power'         : OperatorInfo( exponentiate, 2, [ Measurement ] ),
    'prime'         : OperatorInfo( getNthPrime, 1, [ ] ),
    'prime?'        : OperatorInfo( lambda n: findPrime( n )[ 1 ], 1, [ ] ),
    'primepi'       : OperatorInfo( getPrimePi, 1, [ ] ),
    'primes'        : OperatorInfo( getPrimes, 2, [ ] ),
    'primorial'     : OperatorInfo( getPrimorial, 1, [ ] ),
    'pyramid'       : OperatorInfo( lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1, [ ] ),
    'quadprime'     : OperatorInfo( getNthQuadrupletPrime, 1, [ ] ),
    'quadprime?'    : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 1 ], 1, [ ] ),
    'quadprime_'    : OperatorInfo( getNthQuadrupletPrimeList, 1, [ ] ),
    'quintprime'    : OperatorInfo( getNthQuintupletPrime, 1, [ ] ),
    'quintprime_'   : OperatorInfo( getNthQuintupletPrimeList, 1, [ ] ),
    'randint'       : OperatorInfo( randrange, 1, [ ] ),
    'random'        : OperatorInfo( rand, 0, [ ] ),
    'range'         : OperatorInfo( expandRange, 2, [ ] ),
    'range2'        : OperatorInfo( expandSteppedRange, 3, [ ] ),
    'reciprocal'    : OperatorInfo( takeReciprocal, 1, [ ] ),
    'repunit'       : OperatorInfo( getNthBaseKRepunit, 2, [ ] ),
    'rhombdodec'    : OperatorInfo( getNthRhombicDodecahedralNumber, 1, [ ] ),
    'riesel'        : OperatorInfo( lambda n: fsub( fmul( n, power( 2, n ) ), 1 ), 1, [ ] ),
    'root'          : OperatorInfo( root, 2, [ Measurement ] ),
    'root2'         : OperatorInfo( sqrt, 1, [ Measurement ] ),
    'root3'         : OperatorInfo( cbrt, 1, [ Measurement ] ),
    'round'         : OperatorInfo( lambda n: floor( fadd( n, 0.5 ) ), 1, [ Measurement ] ),
    'safeprime'     : OperatorInfo( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1, [ ] ),
    'schroeder'     : OperatorInfo( getNthSchroederNumber, 1, [ ] ),
    'sec'           : OperatorInfo( lambda n: performTrigOperation( n, sec ), 1, [ ] ),
    'sech'          : OperatorInfo( lambda n: performTrigOperation( n, sech ), 1, [ ] ),
    'sextprime'     : OperatorInfo( getNthSextupletPrime, 1, [ ] ),
    'sextprime_'    : OperatorInfo( getNthSextupletPrimeList, 1, [ ] ),
    'sexyprime'     : OperatorInfo( getNthSexyPrime, 1, [ ] ),
    'sexyprime_'    : OperatorInfo( getNthSexyPrimeList, 1, [ ] ),
    'sexyquad'      : OperatorInfo( getNthSexyQuadruplet, 1, [ ] ),
    'sexyquad_'     : OperatorInfo( getNthSexyQuadrupletList, 1, [ ] ),
    'sexytriplet'   : OperatorInfo( getNthSexyTriplet, 1, [ ] ),
    'sexytriplet_'  : OperatorInfo( getNthSexyTripletList, 1, [ ] ),
    'shiftleft'     : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2, [ ] ),
    'shiftright'    : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2, [ ] ),
    'short'         : OperatorInfo( lambda n: convertToSignedInt( n , 16 ), 1, [ ] ),
    'sin'           : OperatorInfo( lambda n: performTrigOperation( n, sin ), 1, [ ] ),
    'sinh'          : OperatorInfo( lambda n: performTrigOperation( n, sinh ), 1, [ ] ),
    'solve2'        : OperatorInfo( solveQuadraticPolynomial, 3, [ ] ),
    'solve3'        : OperatorInfo( solveCubicPolynomial, 4, [ ] ),
    'solve4'        : OperatorInfo( solveQuarticPolynomial, 5, [ ] ),
    'sophieprime'   : OperatorInfo( getNthSophiePrime, 1, [ ] ),
    'spherearea'    : OperatorInfo( lambda n: getNSphereSurfaceArea( 3, n ), 1, [ Measurement ] ),
    'sphereradius'  : OperatorInfo( lambda n: getNSphereRadius( 3, n ), 1, [ Measurement ] ),
    'spherevolume'  : OperatorInfo( lambda n: getNSphereVolume( 3, n ), 1, [ Measurement ] ),
    'square'        : OperatorInfo( lambda i: exponentiate( i, 2 ), 1, [ Measurement ] ),
    'squaretri'     : OperatorInfo( getNthSquareTriangularNumber, 1, [ ] ),
    'steloct'       : OperatorInfo( getNthStellaOctangulaNumber, 1, [ ] ),
    'subfac'        : OperatorInfo( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1, [ ] ),
    'subtract'      : OperatorInfo( subtract, 2, [ Measurement, arrow.Arrow ] ),
    'superfac'      : OperatorInfo( superfac, 1, [ ] ),
    'superprime'    : OperatorInfo( getNthSuperPrime, 1, [ ] ),
    'sylvester'     : OperatorInfo( getNthSylvester, 1, [ ] ),
    'tan'           : OperatorInfo( lambda n: performTrigOperation( n, tan ), 1, [ ] ),
    'tanh'          : OperatorInfo( lambda n: performTrigOperation( n, tanh ), 1, [ ] ),
    'tetrahedral'   : OperatorInfo( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ), 1, [ ] ),
    'tetranacci'    : OperatorInfo( getNthTetranacci, 1, [ ] ),
    'tetrate'       : OperatorInfo( tetrate, 2, [ ] ),
    'thabit'        : OperatorInfo( lambda n : fsub( fmul( 3, power( 2, n ) ), 1 ), 1, [ ] ),
    'today'         : OperatorInfo( getToday, 0, [ ] ),
    'trianglearea'  : OperatorInfo( getTriangleArea, 3, [ Measurement ] ),
    'triangular'    : OperatorInfo( lambda n : getNthPolygonalNumber( n, 3 ), 1, [ ] ),
    'triangular?'   : OperatorInfo( lambda n : findNthPolygonalNumber( n, 3 ), 1, [ ] ),
    'tribonacci'    : OperatorInfo( getNthTribonacci, 1, [ ] ),
    'triplebal'     : OperatorInfo( getNthTripleBalancedPrime, 1, [ ] ),
    'triplebal_'    : OperatorInfo( getNthTripleBalancedPrimeList, 1, [ ] ),
    'tripletprime'  : OperatorInfo( getNthTripletPrime, 1, [ ] ),
    'tripletprime'  : OperatorInfo( getNthTripletPrimeList, 1, [ ] ),
    'truncoct'      : OperatorInfo( getNthTruncatedOctahedralNumber, 1, [ ] ),
    'trunctet'      : OperatorInfo( getNthTruncatedTetrahedralNumber, 1, [ ] ),
    'twinprime'     : OperatorInfo( getNthTwinPrime, 1, [ ] ),
    'twinprime_'    : OperatorInfo( getNthTwinPrimeList, 1, [ ] ),
    'uchar'         : OperatorInfo( lambda n: int( fmod( n, power( 2, 8 ) ) ), 1, [ ] ),
    'uinteger'      : OperatorInfo( lambda n, k: int( fmod( n, power( 2, k ) ) ), 2, [ ] ),
    'ulong'         : OperatorInfo( lambda n: int( fmod( n, power( 2, 32 ) ) ), 1, [ ] ),
    'ulonglong'     : OperatorInfo( lambda n: int( fmod( n, power( 2, 64 ) ) ), 1, [ ] ),
    'unitroots'     : OperatorInfo( lambda i: unitroots( int( i ) ), 1, [ ] ),
    'ushort'        : OperatorInfo( lambda n: int( fmod( n, power( 2, 16 ) ) ), 1, [ ] ),
    'weekday'       : OperatorInfo( getWeekday, 1, [ arrow.Arrow ] ),
    'xor'           : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2, [ ] ),
    'ydhms'         : OperatorInfo( convertToYDHMS, 1, [ Measurement ] ),
    'zeta'          : OperatorInfo( zeta, 1, [ ] ),
    '_dumpalias'    : OperatorInfo( dumpAliases, 0, [ ] ),
    '_dumpops'      : OperatorInfo( dumpOperators, 0, [ ] ),
    '_stats'        : OperatorInfo( dumpStats, 0, [ ] ),
    '~'             : OperatorInfo( getInvertedBits, 1, [ ] ),
#   'antitet'       : OperatorInfo( findTetrahedralNumber, 1, [ ] ),
#   'bernfrac'      : OperatorInfo( bernfrac, 1, [ ] ),
#   'powmod'        : OperatorInfo( getPowMod, 3, [ ] ),
}


#//******************************************************************************
#//
#//  rpn
#//
#//******************************************************************************

def rpn( cmd_args ):
    # initialize globals
    g.debugMode = False

    if getattr( sys, 'frozen', False ):
        g.dataPath = os.path.dirname( sys.executable )
    else:
        g.dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + 'rpndata'

    help = False
    helpArgs = [ ]

    for i in range( 0, len( cmd_args ) ):
        if cmd_args[ i ] == 'help':
            help = True
        else:
            if help:
                helpArgs.append( cmd_args[ i ] )

    if help:
        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, listOperators, modifiers, operatorAliases, g.dataPath, helpArgs )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=defaultAccuracy,  # -1
                         const=defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping )
    parser.add_argument( '-D', '--DEBUG', action='store_true' )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--identify', action='store_true' )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0 )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-u', '--find_poly', nargs='?', type=int, action='store', default=0, const=1000 )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store',
                         default=defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    if len( cmd_args ) == 0:
        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )
        return

    args = parser.parse_args( cmd_args )

    if args.help or args.other_help:
        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, listOperators, modifiers,
                   operatorAliases, g.dataPath, [ ] )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

    mp.dps = args.precision

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    g.bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -D
    if args.DEBUG:
        g.debugMode = True

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -n
    g.numerals = args.numerals

    # handle -b
    g.inputRadix = int( args.input_radix )

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return

    # handle -x
    if args.hex:
        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        g.bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        g.bitwiseGroupSize = 9

    # handle -R
    if args.output_radix_numerals > 0:
        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( 'rpn:  output radix must be from 2 to 62, or phi' )
            return

    # handle -y and -u:  mpmath wants precision of at least 53 for these functions
    if args.identify or args.find_poly > 0:
        if mp.dps < 53:
            mp.dps = 53

    index = 1                 # only used for error messages
    valueList = list( )

    if args.print_options:
        print( '--output_accuracy:  %d' % args.output_accuracy )
        print( '--input_radix:  %d' % g.inputRadix )
        print( '--comma:  ' + ( 'true' if args.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % args.decimal_grouping )
        print( '--integer_grouping:  %d' % integerGrouping )
        print( '--numerals:  ' + args.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % args.output_radix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--time:  ' + ( 'true' if args.time else 'false' ) )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % g.bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

    if len( args.terms ) == 0:
        print( 'rpn:  no terms found' )
        return

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            unitsVersion = pickle.load( pickleFile )
            g.basicUnitTypes = pickle.load( pickleFile )
            g.unitOperators = pickle.load( pickleFile )
            operatorAliases.update( pickle.load( pickleFile ) )
            g.compoundUnits = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.' )

    if unitsVersion != PROGRAM_VERSION:
        print( 'rpn  units data file version mismatch' )

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        if term in operatorAliases:
            term = operatorAliases[ term ]

        currentValueList = getCurrentArgList( valueList )

        if term in modifiers:
            try:
                operatorInfo = modifiers[ term ]
                operatorInfo.function( currentValueList )
            except IndexError as error:
                print( 'rpn:  index error for operator at arg ' + format( index ) + ', \'' + term +
                       '.  Are your arguments in the right order?' )
                break

        elif term in g.unitOperators:
            if len( currentValueList ) == 0 or isinstance( currentValueList[ -1 ], Measurement ):
                if g.unitOperators[ term ].unitType == 'constant':
                    value = mpf( Measurement( 1, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                else:
                    value = Measurement( 1, term, g.unitOperators[ term ].representation, g.unitOperators[ term ].plural )

                currentValueList.append( value )
            elif isinstance( currentValueList[ -1 ], list ):
                argList = currentValueList.pop( )

                for listItem in argList:
                    if g.unitOperators[ term ].unitType == 'constant':
                        value = mpf( Measurement( listItem, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                    else:
                        value = Measurement( listItem, term, g.unitOperators[ term ].representation, g.unitOperators[ term ].plural )

                    currentValueList.append( value )
            elif isinstance( currentValueList[ -1 ], mpf ):
                if g.unitOperators[ term ].unitType == 'constant':
                    value = mpf( Measurement( currentValueList.pop( ), term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                else:
                    value = Measurement( currentValueList.pop( ), term, g.unitOperators[ term ].representation, g.unitOperators[ term ].plural )

                currentValueList.append( value )
            else:
                raise ValueError( 'unsupported type for a unit operator' )
        elif term in operators:
            operatorInfo = operators[ term ]

            argsNeeded = operatorInfo.argCount

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    result = callers[ 0 ]( operatorInfo.function, None )
                else:
                    argList = list( )

                    for i in range( 0, argsNeeded ):
                        arg = currentValueList.pop( )
                        argList.append( arg if isinstance( arg, list ) else [ arg ] )

                    result = callers[ argsNeeded ]( operatorInfo.function, *argList )

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )

            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )

                if g.debugMode:
                    raise
                else:
                    break

            except ValueError as error:
                print( 'rpn:  value error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    break

            except TypeError as error:
                print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    break

            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )

                if g.debugMode:
                    raise
                else:
                    break

        elif term in listOperators:
            operatorInfo = listOperators[ term ]
            argsNeeded = operatorInfo.argCount

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term + ' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    currentValueList.append( operatorInfo.function( currentValueList ) )
                elif argsNeeded == 1:
                    currentValueList.append( evaluateOneListFunction( operatorInfo.function, currentValueList.pop( ) ) )
                else:
                    listArgs = [ ]

                    for i in range( 0, argsNeeded ):
                        listArgs.insert( 0, currentValueList.pop( ) )

                    currentValueList.append( operatorInfo.function( *listArgs ) )

            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )

                if g.debugMode:
                    raise
                else:
                    break

            except ValueError as error:
                print( 'rpn:  value error for list operator at arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    break

            except TypeError as error:
                print( 'rpn:  type error for list operator at arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    break

            except IndexError as error:
                print( 'rpn:  index error for list operator at arg ' + format( index ) +
                       '.  Are your arguments in the right order?' )

                if g.debugMode:
                    raise
                else:
                    break

            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )

                if g.debugMode:
                    raise
                else:
                    break
        else:
            try:
                currentValueList.append( parseInputValue( term, g.inputRadix ) )

            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                     break

            except TypeError as error:
                currentValueList.append( term )

                try:
                    print( 'rpn:  error in arg ' + format( index ) + ':  unrecognized argument: \'' +
                           term + '\'' )
                except:
                    print( 'rpn:  error in arg ' + format( index ) + ':  non-ASCII characters' )

                if g.debugMode:
                    raise
                else:
                    break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1 or len( valueList ) == 0:
            print( 'rpn:  unexpected end of input' )
        else:
            mp.pretty = True
            result = valueList.pop( )

            if args.comma:
                integerGrouping = 3     # override whatever was set on the command-line
                leadingZero = False     # this one, too
                integerDelimiter = ','
            else:
                integerDelimiter = ' '

            if isinstance( result, list ):
                print( formatListOutput( result, outputRadix, g.numerals, integerGrouping, integerDelimiter,
                                         leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                         args.output_accuracy ) )
            else:
                if isinstance( result, arrow.Arrow ):
                    outputString = formatDateTime( result )
                else:
                    # output the answer with all the extras according to command-line arguments
                    resultString = nstr( result, mp.dps )

                    outputString = formatOutput( resultString, outputRadix, g.numerals, integerGrouping,
                                                 integerDelimiter, leadingZero, args.decimal_grouping,
                                                 ' ', baseAsDigits, args.output_accuracy )

                    # handle the units if we are displaying a measurement
                    if isinstance( result, Measurement ):
                        outputString += ' ' + formatUnits( result.normalizeUnits( ) )

                print( outputString )

                # handle --identify
                if args.identify:
                    formula = identify( result )

                    if formula is None:
                        base = [ 'pi', 'e' ]
                        formula = identify( result, base )

                    # I don't know if this would ever be useful to try.
                    #if formula is None:
                    #    base.extend( [ 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' ] )
                    #    formula = identify( result, base )
                    #
                    # Nor this.
                    #if formula is None:
                    #    base.extend( [ 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' ] )
                    #    formula = identify( result, base )

                    if formula is None:
                        print( '    = [formula cannot be found]' )
                    else:
                        print( '    = ' + formula )

                # handle --find_poly
                if args.find_poly > 0:
                    poly = str( findpoly( result, args.find_poly ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000, tol=1e-10 ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )

            saveResult( result )

        if args.time:
            print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    rpn( sys.argv[ 1 : ] )

