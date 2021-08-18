#!/usr/bin/env python

#******************************************************************************
#
#  rpnGeometry.py
#
#  rpnChilada geometry operators
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import cos, cot, fadd, fdiv, fmul, fprod, fsub, gamma, power, pi, \
                   root, sin, sqrt, tan

from rpn.rpnList import getProduct, getSum
from rpn.rpnMath import add, divide, getPower, getRoot, multiply, subtract
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, IntValidator, LengthValidator, MeasurementValidator


#******************************************************************************
#
#  getRegularPolygonArea
#
#  based on having sides of edge length k
#
#  http://www.mathopenref.com/polygonregulararea.html
#
#******************************************************************************

def getRegularPolygonArea( n, k ):
    return multiply( fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) ), getPower( k, 2 ) ).convert( 'meter^2' )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), LengthValidator( ) ] )
def getRegularPolygonAreaOperator( n, k ):
    return getRegularPolygonArea( n, k )


#******************************************************************************
#
#  getKSphereRadiusOperator
#
#  n - measurement
#  k - dimension
#
#  n needs to be an RPNMeasurement so getKSphereRadius can tell if it's an
#  area or a volume and use the correct formula.
#
#******************************************************************************

def getKSphereRadius( n, k ):
    if k < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( n, RPNMeasurement ):
        return RPNMeasurement( n, 'meter' )

    dimensions = n.getDimensions( )

    if dimensions == { 'length' : 1 }:
        return n

    if dimensions == { 'length' : int( k - 1 ) }:
        area = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k - 1 ) } ] ) )

        result = root( fdiv( fmul( area, gamma( fdiv( k, 2 ) ) ),
                             fmul( 2, power( pi, fdiv( k, 2 ) ) ) ), fsub( k, 1 ) )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )

    if dimensions == { 'length' : int( k ) }:
        volume = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k ) } ] ) )

        result = root( fmul( fdiv( gamma( fadd( fdiv( k, 2 ), 1 ) ),
                                   power( pi, fdiv( k, 2 ) ) ),
                             volume ), k )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )

    raise ValueError( 'incompatible measurement type for computing the radius: ' + str( dimensions ) )


@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereRadiusOperator( n, k ):
    return getKSphereRadius( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ) ] )
def getSphereRadiusOperator( n ):
    return getKSphereRadius( n, 3 )


#******************************************************************************
#
#  getKSphereSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#
#  n - measurement
#  k - dimension
#
#  If n is a length, then it is taken to be the radius.  If it is a volume
#  then it is taken to be the volume.  If it is an area, then it is returned
#  unchanged.  Other measurement types cause an exception.
#
#******************************************************************************

def getKSphereSurfaceArea( n, k ):
    if not isinstance( n, RPNMeasurement ):
        return getKSphereSurfaceArea( n, RPNMeasurement( n, 'meter' ) )

    dimensions = n.getDimensions( )

    if dimensions == { 'length' : 1 }:
        m = n.convertValue( RPNMeasurement( 1, [ { 'meter' : 1 } ] ) )

        result = fmul( fdiv( fmul( power( pi, fdiv( k, 2 ) ), 2 ), gamma( fdiv( k, 2 ) ) ), power( m, fsub( k, 1 ) ) )

        return RPNMeasurement( result, [ { 'meter' : int( k - 1 ) } ] )

    if dimensions == { 'length' : int( k - 1 ) }:
        return n

    if dimensions == { 'length' : int( k ) }:
        radius = getKSphereRadius( n, k )
        return getKSphereSurfaceArea( radius, k )

    raise ValueError( 'incompatible measurement type for computing the surface area' )


@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereSurfaceAreaOperator( n, k ):
    return getKSphereSurfaceArea( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ) ] )
def getSphereAreaOperator( n ):
    return getKSphereSurfaceArea( n, 3 )


#******************************************************************************
#
#  getKSphereVolumeOperator
#
#  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#
#  n - measurement
#  k - dimension
#
#  If n is a length, then it is taken to be the radius.  If it is an area
#  then it is taken to be the surface area.  If it is a volume, then it is
#  returned unchanged.  Other measurement types cause an exception.
#
#******************************************************************************

def getKSphereVolume( n, k ):
    if not isinstance( n, RPNMeasurement ):
        return getKSphereVolume( RPNMeasurement( n, 'meter' ), k )

    dimensions = n.getDimensions( )
    m = n.value

    if dimensions == { 'length' : 1 }:
        m = n.convertValue( RPNMeasurement( 1, [ { 'meter' : 1 } ] ) )

        result = fmul( fdiv( power( pi, fdiv( k, 2 ) ), gamma( fadd( fdiv( k, 2 ), 1 ) ) ), power( m, k ) )

        return RPNMeasurement( result, [ { 'meter' : k } ] )

    if dimensions == { 'length' : int( k - 1 ) }:
        radius = getKSphereRadius( n, k )
        return getKSphereVolume( radius, k )

    if dimensions == { 'length' : int( k ) }:
        return n

    raise ValueError( 'incompatible measurement type for computing the volume' )


@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereVolumeOperator( n, k ):
    return getKSphereVolume( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( 0 ) ] )
def getSphereVolumeOperator( n ):
    return getKSphereVolume( n, 3 )


#******************************************************************************
#
#  getTriangleAreaOperator
#
#******************************************************************************

@argValidator( [ LengthValidator( ), LengthValidator( ), LengthValidator( ) ] )
def getTriangleAreaOperator( a, b, c ):
    s = divide( getSum( [ a, b, c ] ), 2 )   # semi-perimeter
    return getRoot( getProduct( [ s, subtract( s, a ), subtract( s, b ), subtract( s, c ) ] ), 2 )


#******************************************************************************
#
#  getTorusSurfaceAreaperator
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#  major = major radius
#  minor = minor radius
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getTorusSurfaceAreaOperator( major, minor ):
    return getProduct( [ 4, power( pi, 2 ), major, minor ] )


#******************************************************************************
#
#  getTorusVolumeOperator
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#  major = major radius
#  minor = minor radius
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getTorusVolumeOperator( major, minor ):
    return getProduct( [ 2, power( pi, 2 ), major, getPower( minor, 2 ) ] )


#******************************************************************************
#
#  getConeSurfaceAreaOperator
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getConeSurfaceAreaOperator( radius, height ):
    hypotenuse = getRoot( add( getPower( radius, 2 ), getPower( height, 2 ) ), 2 )
    return getProduct( [ pi, radius, add( radius, hypotenuse ) ] )


#******************************************************************************
#
#  getConeVolumeOperator
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getConeVolumeOperator( radius, height ):
    return getProduct( [ pi, getPower( radius, 2 ), divide( height, 3 ) ] )


#******************************************************************************
#
#  getTetrahedronSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Tetrahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getTetrahedronSurfaceAreaOperator( n ):
    return multiply( sqrt( 3 ), getPower( n, 2 ) )


#******************************************************************************
#
#  getTetrahedronVolumeOperator
#
#  https://en.wikipedia.org/wiki/Tetrahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getTetrahedronVolumeOperator( n ):
    return divide( getPower( n, 3 ), fmul( 6, sqrt( 2 ) ) )


#******************************************************************************
#
#  getOctahedronSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Octahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getOctahedronSurfaceAreaOperator( n ):
    return getProduct( [ 2, sqrt( 3 ), getPower( n, 2 ) ] )


#******************************************************************************
#
#  getOctahedronVolumeOperator
#
#  https://en.wikipedia.org/wiki/Octahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getOctahedronVolumeOperator( n ):
    return divide( multiply( sqrt( 2 ), getPower( n, 3 ) ), 3 )


#******************************************************************************
#
#  getDodecahedronSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Dodecahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getDodecahedronSurfaceAreaOperator( n ):
    area = getProduct( [ 3, getRoot( add( 25, fmul( 10, sqrt( 5 ) ) ), 2 ), getPower( n, 2 ) ] )
    return area.convert( 'meter^2' )


#******************************************************************************
#
#  getDodecahedronVolumeOperator
#
#  https://en.wikipedia.org/wiki/Dodecahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getDodecahedronVolumeOperator( n ):
    return divide( multiply( fadd( 15, fmul( 7, sqrt( 5 ) ) ), getPower( n, 3 ) ), 4 ).convert( 'meter^3' )


#******************************************************************************
#
#  getIcosahedronSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Icosahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getIcosahedronSurfaceAreaOperator( n ):
    return getProduct( [ 5, sqrt( 3 ), getPower( n, 2 ) ] ).convert( 'meter^2' )


#******************************************************************************
#
#  getIcosahedronVolumeOperator
#
#  https://en.wikipedia.org/wiki/Icosahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getIcosahedronVolumeOperator( n ):
    return getProduct( [ fdiv( 5, 12 ), fadd( 3, sqrt( 5 ) ), getPower( n, 3 ) ] ).convert( 'meter^3' )


#******************************************************************************
#
#  getAntiprismSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Antiprism
#
#  n = sides
#  k = edge length
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), LengthValidator( ) ] )
def getAntiprismSurfaceAreaOperator( n, k ):
    result = getProduct( [ fdiv( n, 2 ), fadd( cot( fdiv( pi, n ) ), sqrt( 3 ) ), getPower( k, 2 ) ] )
    return result.convert( 'meter^2' )


#******************************************************************************
#
#  getAntiprismVolumeOperator
#
#  http://www.fxsolver.com/browse/formulas/Antiprism+uniform+%28Volume%29
#
#  n = sides
#  k = edge length
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), LengthValidator( ) ] )
def getAntiprismVolumeOperator( n, k ):
    result = getProduct( [ fdiv( fprod( [ n, sqrt( fsub( fmul( 4, cos( cos( fdiv( pi, fmul( n, 2 ) ) ) ) ), 1 ) ),
                                          sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ) ] ),
                                 fmul( 12, sin( sin( fdiv( pi, n ) ) ) ) ),
                           sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ),
                           getPower( k, 3 ) ] )

    return result.convert( 'meter^3' )


#******************************************************************************
#
#  getPrismSurfaceAreaOperator
#
#  https://en.wikipedia.org/wiki/Prism
#
#  n = sides
#  k = edge length
#  h = height
#
#******************************************************************************

@argValidator( [ IntValidator( 3 ), LengthValidator( ), LengthValidator( ) ] )
def getPrismSurfaceAreaOperator( n, k, h ):
    result = add( getProduct( [ fdiv( n, 2 ), getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ),
                  getProduct( [ n, k, h ] ) )
    return result.convert( 'meter^2' )


#******************************************************************************
#
#  getPrismVolumeOperator
#
#  https://en.wikipedia.org/wiki/Prism
#
#  n = sides
#  k = edge length
#  h = height
#
#******************************************************************************

@argValidator( [ IntValidator( 3 ), LengthValidator( ), LengthValidator( ) ] )
def getPrismVolumeOperator( n, k, h ):
    return getProduct( [ fdiv( n, 4 ), h, getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ).convert( 'meter^3' )
