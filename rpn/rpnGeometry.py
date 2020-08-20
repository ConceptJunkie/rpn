#!/usr/bin/env python

#******************************************************************************
#
#  rpnGeometry.py
#
#  rpnChilada geometry operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
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
from rpn.rpnValidator import argValidator, DefaultValidator, IntValidator, LengthValidator, RealValidator, \
                             RealOrMeasurementValidator



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
    if not isinstance( k, RPNMeasurement ):
        return getRegularPolygonArea( n, RPNMeasurement( k, 'meter' ) )

    dimensions = k.getDimensions( )

    if dimensions != { 'length' : 1 }:
        raise ValueError( '\'polygon_area\' argument 2 must be a length' )

    return multiply( fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) ), getPower( k, 2 ) ).convert( 'meter^2' )

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), RealOrMeasurementValidator( 0 ) ] )
def getRegularPolygonAreaOperator( n, k ):
    return getRegularPolygonArea( n, k )


#******************************************************************************
#
#  getKSphereRadius
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
    elif dimensions == { 'length' : int( k - 1 ) }:
        area = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k - 1 ) } ] ) )

        result = root( fdiv( fmul( area, gamma( fdiv( k, 2 ) ) ),
                             fmul( 2, power( pi, fdiv( k, 2 ) ) ) ), fsub( k, 1 ) )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )
    elif dimensions == { 'length' : int( k ) }:
        volume = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k ) } ] ) )

        result = root( fmul( fdiv( gamma( fadd( fdiv( k, 2 ), 1 ) ),
                                   power( pi, fdiv( k, 2 ) ) ),
                             volume ), k )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' +
                          str( dimensions ) )

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereRadiusOperator( n, k ):
    return getKSphereRadius( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ) ] )
def getSphereRadius( n ):
    return getKSphereRadius( n, 3 )


#******************************************************************************
#
#  getKSphereSurfaceArea
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
    elif dimensions == { 'length' : int( k - 1 ) }:
        return n
    elif dimensions == { 'length' : int( k ) }:
        radius = getKSphereRadius( n, k )
        return getKSphereSurfaceArea( radius, k )
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereSurfaceAreaOperator( n, k ):
    return getKSphereSurfaceArea( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ) ] )
def getSphereArea( n ):
    return getKSphereSurfaceArea( n, 3 )


#******************************************************************************
#
#  getKSphereVolume
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
    elif dimensions == { 'length' : int( k - 1 ) }:
        radius = getKSphereRadius( n, k )
        return getKSphereVolume( radius, k )
    elif dimensions == { 'length' : int( k ) }:
        return n
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ), IntValidator( 3 ) ] )
def getKSphereVolumeOperator( n, k ):
    return getKSphereVolume( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( 0 ) ] )
def getSphereVolume( n ):
    return getKSphereVolume( n, 3 )


#******************************************************************************
#
#  getTriangleArea
#
#******************************************************************************

@argValidator( [ LengthValidator( ), LengthValidator( ), LengthValidator( ) ] )
def getTriangleArea( a, b, c ):
    if not isinstance( a, RPNMeasurement ):
        return getTriangleArea( RPNMeasurement( a, 'meter' ), b, c )

    if a.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 1 must be a length' )

    if not isinstance( b, RPNMeasurement ):
        return getTriangleArea( a, RPNMeasurement( b, 'meter' ), c )

    if b.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 2 must be a length' )

    if not isinstance( c, RPNMeasurement ):
        return getTriangleArea( a, b, RPNMeasurement( c, 'meter' ) )

    if b.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 3 must be a length' )

    if add( a, b ).isNotLarger( c ) or add( b, c ).isNotLarger( a ) or add( a, c ).isNotLarger( b ):
        raise ValueError( 'invalid triangle, the sum of any two sides must be longer than the third side' )

    s = divide( getSum( [ a, b, c ] ), 2 )   # semi-perimeter
    return getRoot( getProduct( [ s, subtract( s, a ), subtract( s, b ), subtract( s, c ) ] ), 2 )


#******************************************************************************
#
#  getTorusSurfaceArea
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#  major = major radius
#  minor = minor radius
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getTorusSurfaceArea( major, minor ):
    if not isinstance( major, RPNMeasurement ):
        return getTorusSurfaceArea( RPNMeasurement( major, 'meter' ),
                                    minor )

    if major.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_area\' argument 1 must be a length' )

    if not isinstance( minor, RPNMeasurement ):
        return getTorusSurfaceArea( major, RPNMeasurement( minor, 'meter' ) )

    if minor.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_area\' argument 2 must be a length' )

    return getProduct( [ 4, power( pi, 2 ), major, minor ] )


#******************************************************************************
#
#  getTorusVolume
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#  major = major radius
#  minor = minor radius
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getTorusVolume( major, minor ):
    if not isinstance( major, RPNMeasurement ):
        return getTorusVolume( RPNMeasurement( major, 'meter' ), minor )

    if major.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_volume\' argument 1 must be a length' )

    if not isinstance( minor, RPNMeasurement ):
        return getTorusVolume( major, RPNMeasurement( minor, 'meter' ) )

    if minor.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_volume\' argument 2 must be a length' )

    return getProduct( [ 2, power( pi, 2 ), major, getPower( minor, 2 ) ] )


#******************************************************************************
#
#  getConeSurfaceArea
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getConeSurfaceArea( radius, height ):
    if not isinstance( radius, RPNMeasurement ):
        return getConeSurfaceArea( RPNMeasurement( radius, 'meter' ), height )

    if radius.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_area\' argument 1 must be a length' )

    if not isinstance( height, RPNMeasurement ):
        return getConeSurfaceArea( radius, RPNMeasurement( height, 'meter' ) )

    if height.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_area\' argument 2 must be a length' )

    hypotenuse = getRoot( add( getPower( radius, 2 ), getPower( height, 2 ) ), 2 )

    return getProduct( [ pi, radius, add( radius, hypotenuse ) ] )


#******************************************************************************
#
#  getConeVolume
#
#  http://preccalc.sourceforge.net/geometry.shtml
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ), LengthValidator( ) ] )
def getConeVolume( radius, height ):
    if not isinstance( radius, RPNMeasurement ):
        return getConeVolume( RPNMeasurement( radius, 'meter' ), height )

    if not isinstance( height, RPNMeasurement ):
        return getConeVolume( radius, RPNMeasurement( height, 'meter' ) )

    return getProduct( [ pi, getPower( radius, 2 ), divide( height, 3 ) ] )


#******************************************************************************
#
#  getTetrahedronSurfaceArea
#
#  https://en.wikipedia.org/wiki/Tetrahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getTetrahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getTetrahedronSurfaceArea( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'tetrahedron_area\' argument must be a length' )

    return multiply( sqrt( 3 ), getPower( n, 2 ) )


#******************************************************************************
#
#  getTetrahedronVolume
#
#  https://en.wikipedia.org/wiki/Tetrahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getTetrahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getTetrahedronVolume( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'tetrahedron_volume\' argument must be a length' )

    return divide( getPower( n, 3 ), fmul( 6, sqrt( 2 ) ) )


#******************************************************************************
#
#  getOctahedronSurfaceArea
#
#  https://en.wikipedia.org/wiki/Octahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getOctahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getOctahedronSurfaceArea( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'octahedron_area\' argument must be a length' )

    return getProduct( [ 2, sqrt( 3 ), getPower( n, 2 ) ] )


#******************************************************************************
#
#  getOctahedronVolume
#
#  https://en.wikipedia.org/wiki/Octahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getOctahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getOctahedronVolume( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'octahedron_volume\' argument must be a length' )

    return divide( multiply( sqrt( 2 ), getPower( n, 3 ) ), 3 )


#******************************************************************************
#
#  getDodecahedronSurfaceArea
#
#  https://en.wikipedia.org/wiki/Dodecahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getDodecahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getDodecahedronSurfaceArea( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'dodecahedron_area\' argument must be a length' )

    area = getProduct( [ 3, getRoot( add( 25, fmul( 10, sqrt( 5 ) ) ), 2 ), getPower( n, 2 ) ] )
    return area.convert( 'meter^2' )


#******************************************************************************
#
#  getDodecahedronVolume
#
#  https://en.wikipedia.org/wiki/Dodecahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getDodecahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getDodecahedronVolume( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'dodecahedron_volume\' argument must be a length' )

    return divide( multiply( fadd( 15, fmul( 7, sqrt( 5 ) ) ), getPower( n, 3 ) ), 4 ).convert( 'meter^3' )


#******************************************************************************
#
#  getIcosahedronSurfaceArea
#
#  https://en.wikipedia.org/wiki/Icosahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getIcosahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getIcosahedronSurfaceArea( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'icosahedron_area\' argument must be a length' )

    return getProduct( [ 5, sqrt( 3 ), getPower( n, 2 ) ] ).convert( 'meter^2' )


#******************************************************************************
#
#  getIcosahedronVolume
#
#  https://en.wikipedia.org/wiki/Icosahedron
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LengthValidator( ) ] )
def getIcosahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getIcosahedronVolume( RPNMeasurement( n, 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'icosahedron_volume\' argument must be a length' )

    return getProduct( [ fdiv( 5, 12 ), fadd( 3, sqrt( 5 ) ), getPower( n, 3 ) ] ).convert( 'meter^3' )


#******************************************************************************
#
#  getAntiprismSurfaceArea
#
#  https://en.wikipedia.org/wiki/Antiprism
#
#  n = sides
#  k = edge length
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), LengthValidator( ) ] )
def getAntiprismSurfaceArea( n, k ):
    if not isinstance( k, RPNMeasurement ):
        return getAntiprismSurfaceArea( n, RPNMeasurement( k, 'meter' ) )

    result = getProduct( [ fdiv( n, 2 ), fadd( cot( fdiv( pi, n ) ), sqrt( 3 ) ), getPower( k, 2 ) ] )
    return result.convert( 'meter^2' )


#******************************************************************************
#
#  getAntiprismVolume
#
#  http://www.fxsolver.com/browse/formulas/Antiprism+uniform+%28Volume%29
#
#  n = sides
#  k = edge length
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 3 ), LengthValidator( ) ] )
def getAntiprismVolume( n, k ):
    if not isinstance( k, RPNMeasurement ):
        return getAntiprismVolume( n, RPNMeasurement( k, 'meter' ) )

    if k.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'antiprism_volume\' argument 2 must be a length' )

    result = getProduct( [ fdiv( fprod( [ n, sqrt( fsub( fmul( 4, cos( cos( fdiv( pi, fmul( n, 2 ) ) ) ) ), 1 ) ),
                                          sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ) ] ),
                                 fmul( 12, sin( sin( fdiv( pi, n ) ) ) ) ),
                           sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ),
                           getPower( k, 3 ) ] )

    return result.convert( 'meter^3' )


#******************************************************************************
#
#  getPrismSurfaceArea
#
#  https://en.wikipedia.org/wiki/Prism
#
#  n = sides
#  k = edge length
#  h = height
#
#******************************************************************************

@argValidator( [ IntValidator( 3 ), LengthValidator( ), LengthValidator( ) ] )
def getPrismSurfaceArea( n, k, h ):
    result = add( getProduct( [ fdiv( n, 2 ), getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ),
                  getProduct( [ n, k, h ] ) )
    return result.convert( 'meter^2' )


#******************************************************************************
#
#  getPrismVolume
#
#  https://en.wikipedia.org/wiki/Prism
#
#  n = sides
#  k = edge length
#  h = height
#
#******************************************************************************

@argValidator( [ IntValidator( 3 ), LengthValidator( ), LengthValidator( ) ] )
def getPrismVolume( n, k, h ):
    return getProduct( [ fdiv( n, 4 ), h, getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ).convert( 'meter^3' )

