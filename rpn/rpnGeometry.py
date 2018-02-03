#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnGeometry.py
# //
# //  RPN command-line calculator geometric operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import cos, cot, fadd, fdiv, fmul, fprod, fsub, fsum, gamma, hypot, \
                   power, pi, root, sin, sqrt, tan

from rpn.rpnList import getProduct, getSum
from rpn.rpnMath import add, divide, getPower, getRoot, multiply, subtract
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         real, real_int


# //******************************************************************************
# //
# //  getRegularPolygonArea
# //
# //  based on having sides of edge length k
# //
# //  http://www.mathopenref.com/polygonregulararea.html
# //
# //******************************************************************************

def getRegularPolygonArea( n, k ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    if not isinstance( k, RPNMeasurement ):
        return getRegularPolygonArea( n, RPNMeasurement( real( k ), 'meter' ) )

    dimensions = k.getDimensions( )

    if dimensions != { 'length' : 1 }:
        raise ValueError( '\'polygon_area\' argument 2 must be a length' )

    return multiply( fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) ), getPower( k, 2 ) ).convert( 'meter^2' )

@twoArgFunctionEvaluator( )
def getRegularPolygonAreaOperator( n, k ):
    return getRegularPolygonArea( n, k )


# //******************************************************************************
# //
# //  getNSphereRadius
# //
# //  n - measurement
# //  k - dimension
# //
# //  n needs to be an RPNMeasurement so getNSphereRadius can tell if it's an
# //  area or a volume and use the correct formula.
# //
# //******************************************************************************

def getNSphereRadius( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( n, RPNMeasurement ):
        return RPNMeasurement( n, 'meter' )

    dimensions = n.getDimensions( )

    if dimensions == { 'length' : 1 }:
        return n
    elif dimensions == { 'length' : int( k - 1 ) }:
        m2 = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k - 1 ) } ] ) )

        result = root( fdiv( fmul( m2, gamma( fdiv( k, 2 ) ) ),
                             fmul( 2, power( pi, fdiv( k, 2 ) ) ) ), fsub( k, 1 ) )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )
    elif dimensions == { 'length' : int( k ) }:
        m3 = n.convertValue( RPNMeasurement( 1, [ { 'meter' : int( k ) } ] ) )

        result = root( fmul( fdiv( gamma( fadd( fdiv( k, 2 ), 1 ) ),
                                   power( pi, fdiv( k, 2 ) ) ),
                             m3 ), k )

        return RPNMeasurement( result, [ { 'meter' : 1 } ] )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' +
                          str( dimensions ) )

@twoArgFunctionEvaluator( )
def getNSphereRadiusOperator( n, k ):
    return getNSphereRadius( n, k )

@oneArgFunctionEvaluator( )
def getSphereRadius( n ):
    return getNSphereRadius( n, 3 )


# //******************************************************************************
# //
# //  getNSphereSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
# //
# //  n - measurement
# //  k - dimension
# //
# //  If n is a length, then it is taken to be the radius.  If it is a volume
# //  then it is taken to be the volume.  If it is an area, then it is returned
# //  unchanged.  Other measurement types cause an exception.
# //
# //******************************************************************************

def getNSphereSurfaceArea( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( n, RPNMeasurement ):
        return getNSphereSurfaceArea( n, RPNMeasurement( real( n ), 'meter' ) )

    dimensions = n.getDimensions( )

    if dimensions == { 'length' : 1 }:
        m = n.convertValue( RPNMeasurement( 1, [ { 'meter' : 1 } ] ) )

        result = fmul( fdiv( fmul( power( pi, fdiv( k, 2 ) ), 2 ),
                             gamma( fdiv( k, 2 ) ) ),
                       power( m, fsub( k, 1 ) ) )

        return RPNMeasurement( result, [ { 'meter' : int( k - 1 ) } ] )
    elif dimensions == { 'length' : int( k - 1 ) }:
        return n
    elif dimensions == { 'length' : int( k ) }:
        radius = getNSphereRadius( n, k )
        return getNSphereSurfaceArea( radius, k )
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )

@twoArgFunctionEvaluator( )
def getNSphereSurfaceAreaOperator( n, k ):
    return getNSphereSurfaceArea( n, k )

@oneArgFunctionEvaluator( )
def getSphereArea( n ):
    return getNSphereSurfaceArea( n, 3 )


# //******************************************************************************
# //
# //  getNSphereVolume
# //
# //  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
# //
# //  n - measurement
# //  k - dimension
# //
# //  If n is a length, then it is taken to be the radius.  If it is an area
# //  then it is taken to be the surface area.  If it is a volume, then it is
# //  returned unchanged.  Other measurement types cause an exception.
# //
# //******************************************************************************

def getNSphereVolume( n, k ):
    if real_int( k ) < 1:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( n, RPNMeasurement ):
        return getNSphereVolume( RPNMeasurement( real( n ), 'meter' ), k )

    dimensions = n.getDimensions( )
    m = n.getValue( )

    if dimensions == { 'length' : 1 }:
        m = n.convertValue( RPNMeasurement( 1, [ { 'meter' : 1 } ] ) )

        result = fmul( fdiv( power( pi, fdiv( k, 2 ) ),
                             gamma( fadd( fdiv( k, 2 ), 1 ) ) ), power( m, k ) )

        return RPNMeasurement( result, [ { 'meter' : k } ] )
    elif dimensions == { 'length' : int( k - 1 ) }:
        radius = getNSphereRadius( n, k )
        return getNSphereVolume( radius, k )
    elif dimensions == { 'length' : int( k ) }:
        return n
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )

@twoArgFunctionEvaluator( )
def getNSphereVolumeOperator( n, k ):
    return getNSphereVolume( n, k )

@oneArgFunctionEvaluator( )
def getSphereVolume( n ):
    return getNSphereVolume( n, 3 )


# //******************************************************************************
# //
# //  getTriangleArea
# //
# //******************************************************************************

def getTriangleArea( a, b, c ):
    if not isinstance( a, RPNMeasurement ):
        return getTriangleArea( RPNMeasurement( real( a ), 'meter' ), b, c )

    if a.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 1 must be a length' )

    if not isinstance( b, RPNMeasurement ):
        return getTriangleArea( a, RPNMeasurement( real( b ), 'meter' ), c )

    if b.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 2 must be a length' )

    if not isinstance( c, RPNMeasurement ):
        return getTriangleArea( a, b, RPNMeasurement( real( c ), 'meter' ) )

    if b.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'triangle_area\' argument 3 must be a length' )

    if add( a, b ).isNotLarger( c ) or add( b, c ).isNotLarger( a ) or add( a, c ).isNotLarger( b ):
        raise ValueError( 'invalid triangle, the sum of any two sides must be longer than the third side' )

    s = divide( getSum( [ a, b, c ] ), 2 )   # semi-perimeter
    return getRoot( getProduct( [ s, subtract( s, a ), subtract( s, b ), subtract( s, c ) ] ), 2 )


# //******************************************************************************
# //
# //  getTorusSurfaceArea
# //
# //  http://preccalc.sourceforge.net/geometry.shtml
# //
# //  R = major radius
# //  s = minor radius
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getTorusSurfaceArea( R, s ):
    if not isinstance( R, RPNMeasurement ):
        return getTorusSurfaceArea( RPNMeasurement( real( R ), 'meter' ), s )

    if R.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_area\' argument 1 must be a length' )

    if not isinstance( s, RPNMeasurement ):
        return getTorusSurfaceArea( R, RPNMeasurement( real( s ), 'meter' ) )

    if s.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_area\' argument 2 must be a length' )

    return getProduct( [ 4, power( pi, 2 ), R, s ] )


# //******************************************************************************
# //
# //  getTorusVolume
# //
# //  http://preccalc.sourceforge.net/geometry.shtml
# //
# //  R = major radius
# //  s = minor radius
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getTorusVolume( R, s ):
    if not isinstance( R, RPNMeasurement ):
        return getTorusVolume( RPNMeasurement( real( R ), 'meter' ), s )

    if R.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_volume\' argument 1 must be a length' )

    if not isinstance( s, RPNMeasurement ):
        return getTorusVolume( R, RPNMeasurement( real( s ), 'meter' ) )

    if s.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'torus_volume\' argument 2 must be a length' )

    return getProduct( [ 2, power( pi, 2 ), R, getPower( s, 2 ) ] )


# //******************************************************************************
# //
# //  getConeSurfaceArea
# //
# //  http://preccalc.sourceforge.net/geometry.shtml
# //
# //  r = radius
# //  h = height
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getConeSurfaceArea( r, h ):
    if not isinstance( r, RPNMeasurement ):
        return getConeSurfaceArea( RPNMeasurement( real( r ), 'meter' ), h )

    if r.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_area\' argument 1 must be a length' )

    if not isinstance( h, RPNMeasurement ):
        return getConeSurfaceArea( r, RPNMeasurement( real( h ), 'meter' ) )

    if h.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_area\' argument 2 must be a length' )

    hypotenuse = getRoot( add( getPower( r, 2 ), getPower( h, 2 ) ), 2 )

    return getProduct( [ pi, r, add( r, hypotenuse ) ] )


# //******************************************************************************
# //
# //  getConeVolume
# //
# //  http://preccalc.sourceforge.net/geometry.shtml
# //
# //  r = radius
# //  h = height
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getConeVolume( r, h ):
    if not isinstance( r, RPNMeasurement ):
        return getConeVolume( RPNMeasurement( real( r ), 'meter' ), h )

    if r.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_volume\' argument 1 must be a length' )

    if not isinstance( h, RPNMeasurement ):
        return getConeVolume( r, RPNMeasurement( real( h ), 'meter' ) )

    if h.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'cone_volume\' argument 2 must be a length' )

    return getProduct( [ pi, getPower( r, 2 ), divide( h, 3 ) ] )


# //******************************************************************************
# //
# //  getTetrahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Tetrahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getTetrahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getTetrahedronSurfaceArea( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'tetrahedron_area\' argument must be a length' )

    return multiply( sqrt( 3 ), getPower( n, 2 ) )


# //******************************************************************************
# //
# //  getTetrahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Tetrahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getTetrahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getTetrahedronVolume( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'tetrahedron_volume\' argument must be a length' )

    return divide( getPower( n, 3 ), fmul( 6, sqrt( 2 ) ) )


# //******************************************************************************
# //
# //  getOctahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Octahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getOctahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getOctahedronSurfaceArea( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'octahedron_area\' argument must be a length' )

    return getProduct( [ 2, sqrt( 3 ), getPower( n, 2 ) ] )


# //******************************************************************************
# //
# //  getOctahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Octahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getOctahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getOctahedronVolume( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'octahedron_volume\' argument must be a length' )

    return divide( multiply( sqrt( 2 ), getPower( n, 3 ) ), 3 )


# //******************************************************************************
# //
# //  getDodecahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Dodecahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getDodecahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getDodecahedronSurfaceArea( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'dodecahedron_area\' argument must be a length' )

    area = getProduct( [ 3, getRoot( add( 25, fmul( 10, sqrt( 5 ) ) ), 2 ), getPower( n, 2 ) ] )
    return area.convert( 'meter^2' )


# //******************************************************************************
# //
# //  getDodecahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Dodecahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getDodecahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getDodecahedronVolume( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'dodecahedron_volume\' argument must be a length' )

    return divide( multiply( fadd( 15, fmul( 7, sqrt( 5 ) ) ), getPower( n, 3 ) ), 4 ).convert( 'meter^3' )


# //******************************************************************************
# //
# //  getIcosahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Icosahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getIcosahedronSurfaceArea( n ):
    if not isinstance( n, RPNMeasurement ):
        return getIcosahedronSurfaceArea( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'icosahedron_area\' argument must be a length' )

    return getProduct( [ 5, sqrt( 3 ), getPower( n, 2 ) ] ).convert( 'meter^2' )


# //******************************************************************************
# //
# //  getIcosahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Icosahedron
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getIcosahedronVolume( n ):
    if not isinstance( n, RPNMeasurement ):
        return getIcosahedronVolume( RPNMeasurement( real( n ), 'meter' ) )

    if n.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'icosahedron_volume\' argument must be a length' )

    return getProduct( [ fdiv( 5, 12 ), fadd( 3, sqrt( 5 ) ), getPower( n, 3 ) ] ).convert( 'meter^3' )


# //******************************************************************************
# //
# //  getAntiprismSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Antiprism
# //
# //  n = sides
# //  k = edge length
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getAntiprismSurfaceArea( n, k ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the prism cannot be less than 3,' )

    if not isinstance( k, RPNMeasurement ):
        return getAntiprismSurfaceArea( n, RPNMeasurement( real( k ), 'meter' ) )

    if k.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'antiprism_area\' argument 2 must be a length' )

    result = getProduct( [ fdiv( n, 2 ), fadd( cot( fdiv( pi, n ) ), sqrt( 3 ) ), getPower( k, 2 ) ] )
    return result.convert( 'meter^2' )


# //******************************************************************************
# //
# //  getAntiprismVolume
# //
# //  http://www.fxsolver.com/browse/formulas/Antiprism+uniform+%28Volume%29
# //
# //  n = sides
# //  k = edge length
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getAntiprismVolume( n, k ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the prism cannot be less than 3,' )

    if not isinstance( k, RPNMeasurement ):
        return getAntiprismVolume( n, RPNMeasurement( real( k ), 'meter' ) )

    if k.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'antiprism_volume\' argument 2 must be a length' )

    result = getProduct( [ fdiv( fprod( [ n, sqrt( fsub( fmul( 4, cos( cos( fdiv( pi, fmul( n, 2 ) ) ) ) ), 1 ) ),
                                   sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ) ] ),
                           fmul( 12, sin( sin( fdiv( pi, n ) ) ) ) ),
                           sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ),
                           getPower( k, 3 ) ] )

    return result.convert( 'meter^3' )


# //******************************************************************************
# //
# //  getPrismSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Prism
# //
# //  n = sides
# //  k = edge length
# //  h = height
# //
# //******************************************************************************

def getPrismSurfaceArea( n, k, h ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the prism cannot be less than 3,' )

    if not isinstance( k, RPNMeasurement ):
        return getPrismSurfaceArea( n, RPNMeasurement( real( k ), 'meter' ), h )

    if not isinstance( h, RPNMeasurement ):
        return getPrismSurfaceArea( n, k, RPNMeasurement( real( h ), 'meter' ) )

    if k.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'prism_area\' argument 2 must be a length' )

    if h.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'prism_area\' argument 3 must be a length' )

    result = add( getProduct( [ fdiv( n, 2 ), getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ),
                  getProduct( [ n, k, h ] ) )
    return result.convert( 'meter^2' )


# //******************************************************************************
# //
# //  getPrismVolume
# //
# //  https://en.wikipedia.org/wiki/Prism
# //
# //  n = sides
# //  k = edge length
# //  h = height
# //
# //******************************************************************************

def getPrismVolume( n, k, h ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the prism cannot be less than 3,' )

    if not isinstance( k, RPNMeasurement ):
        return getPrismVolume( n, RPNMeasurement( real( k ), 'meter' ), h )

    if not isinstance( h, RPNMeasurement ):
        return getPrismVolume( n, k, RPNMeasurement( real( h ), 'meter' ) )

    if k.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'prism_volume\' argument 2 must be a length' )

    if h.getDimensions( ) != { 'length' : 1 }:
        raise ValueError( '\'prism_volume\' argument 3 must be a length' )

    return getProduct( [ fdiv( n, 4 ), h, getPower( k, 2 ), cot( fdiv( pi, n ) ) ] ).convert( 'meter^3' )

