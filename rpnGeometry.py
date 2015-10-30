#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnGeometry.py
# //
# //  RPN command-line calculator geometric operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import *

from rpnMeasurement import RPNMeasurement
from rpnUnitClasses import *
from rpnUtils import real


# //******************************************************************************
# //
# //  getRegularPolygonArea
# //
# //  based on having sides of unit length
# //
# //  http://www.mathopenref.com/polygonregulararea.html
# //
# //******************************************************************************

def getRegularPolygonArea( n ):
    if real( n ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) )


# //******************************************************************************
# //
# //  getNSphereRadius
# //
# //  k needs to be an RPNMeasurement so getNSphereRadius can tell if it's an
# //  area or a volume and use the correct formula.
# //
# //******************************************************************************

def getNSphereRadius( n, k ):
    if real( n ) < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, RPNMeasurement ):
        return RPNMeasurement( k, 'inch' )

    measurementType = k.getBasicTypes( )

    if measurementType == { 'length' : 1 }:
        return k
    elif measurementType == { 'length' : 2 }:
        return fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                           fmul( n, power( pi, fdiv( n, 2 ) ) ) ),
                     root( k, fsub( n, 1 ) ) )
    elif measurementType == { 'length' : 3 }:
        return root( fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                                 power( pi, fdiv( n, 2 ) ) ), k ), 3 )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' +
                          measurementType )


# //******************************************************************************
# //
# //  getNSphereSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
# //
# //  n dimensions, k measurement
# //
# //  If k is a length, then it is taken to be the radius.  If it is a volume
# //  then it is taken to be the volume.  If it is an area, then it is returned
# //  unchanged.  Other measurement types cause an exception.
# //
# //******************************************************************************

def getNSphereSurfaceArea( n, k ):
    if not isinstance( k, RPNMeasurement ):
        return getNSphereSurfaceArea( n, RPNMeasurement( real( k ), 'inch' ) )

    if real( n ) < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    measurementType = k.getBasicTypes( )

    if measurementType == { 'length' : 1 }:
        newUnits = Units( k.units )

        for unit in newUnits:
            newUnits[ unit ] *= 2

        return RPNMeasurement( fmul( fdiv( fmul( n, power( pi, fdiv( n, 2 ) ) ),
                                     gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, fsub( n, 1 ) ) ),
                            newUnits )
    elif measurementType == { 'length' : 2 }:
        return k
    elif measurementType == { 'length' : 3 }:
        raise ValueError( 'convertion volume to area is not implemented yet' )
        return 3    # TODO: formula for converting volume to surface area
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )


# //******************************************************************************
# //
# //  getNSphereVolume
# //
# //  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
# //
# //  n dimensions, k measurement
# //
# //  If k is a length, then it is taken to be the radius.  If it is an area
# //  then it is taken to be the surface area.  If it is a volume, then it is
# //  returned unchanged.  Other measurement types cause an exception.
# //
# //******************************************************************************

def getNSphereVolume( n, k ):
    if real( n ) < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, RPNMeasurement ):
        return getNSphereVolume( n, RPNMeasurement( real( k ), 'inch' ) )

    measurementType = k.getBasicTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( power( pi, fdiv( n, 2 ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, n ) )
    elif measurementType == { 'length' : 2 }:
        raise ValueError( 'convertion area to volume is not implemented yet' )
        return 2   # TODO: formula for converting surface area to volume
    elif measurementType == { 'length' : 3 }:
        return k
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )


# //******************************************************************************
# //
# //  getTriangleArea
# //
# //******************************************************************************

def getTriangleArea( a, b, c ):
    s = fdiv( fsum( [ a, b, c ] ), 2 )   # semi-perimeter
    return sqrt( fprod( [ s, fsub( s, a ), fsub( s, b ), fsub( s, c ) ] ) )


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

def getTorusVolume( R, s ):
    return fprod( [ 2, power( pi, 2 ), real( R ), pow( real( s ), 2 ) ] )


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

def getTorusSurfaceArea( R, s ):
    return fprod( [ 4, power( pi, 2 ), real( R ), real( s ) ] )


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

def getConeVolume( r, h ):
    return fprod( [ pi, power( real( r ), 2 ), fdiv( real( h ), 3 ) ] )


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

def getConeSurfaceArea( r, h ):
    return fprod( [ pi, real( r ), fadd( r, hypot( r, real( h ) ) ) ] )


# //******************************************************************************
# //
# //  getTetrahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Tetrahedron
# //
# //******************************************************************************

def getTetrahedronSurfaceArea( n ):
    return fmul( sqrt( 3 ), power( real( n ), 2 ) )


# //******************************************************************************
# //
# //  getTetrahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Tetrahedron
# //
# //******************************************************************************

def getTetrahedronVolume( n ):
    return fdiv( power( real( n ), 3 ), fmul( 6, sqrt( 2 ) ) )


# //******************************************************************************
# //
# //  getOctahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Octahedron
# //
# //******************************************************************************

def getOctahedronSurfaceArea( n ):
    return fprod( [ 2, sqrt( 3 ), power( real( n ), 2 ) ] )


# //******************************************************************************
# //
# //  getOctahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Octahedron
# //
# //******************************************************************************

def getOctahedronVolume( n ):
    return fdiv( fmul( [ sqrt( 2 ), power( real( n ), 3 ) ] ), 3 )


# //******************************************************************************
# //
# //  getDodecahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Dodecahedron
# //
# //******************************************************************************

def getDodecahedronSurfaceArea( n ):
    return fmul( 3, sqrt( fadd( 25, fprod( [ 10, sqrt( 5 ), power( real( a ), 2 ) ] ) ) ) )


# //******************************************************************************
# //
# //  getDodecahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Dodecahedron
# //
# //******************************************************************************

def getDodecahedronVolume( n ):
    return fdiv( fmul( fadd( 15, fmul( 7, sqrt( 5 ) ) ), power( a, 3 ) ), 4 )


# //******************************************************************************
# //
# //  getIcosahedronSurfaceArea
# //
# //  https://en.wikipedia.org/wiki/Icosahedron
# //
# //******************************************************************************

def getIcosahedronSurfaceArea( n ):
    return fprod( [ 5, sqrt( 3 ), power( a, 2 ) ] )


# //******************************************************************************
# //
# //  getIcosahedronVolume
# //
# //  https://en.wikipedia.org/wiki/Icosahedron
# //
# //******************************************************************************

def getIcosahedronVolume( n ):
    return fprod( [ fdiv( 5, 12 ), fadd( 3, sqrt( 5 ) ), power( a, 3 ) ] )


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

def getAntiprismSurfaceArea( n, k ):
    return fprod( [ fdiv( n, 2 ), fadd( cot( fdiv( pi, n ) ), sqrt( 3 ) ), power( k, 2 ) ] )


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

def getAntiprismVolume( n, k ):
    return fprod( [ fdiv( fprod( [ n, sqrt( fsub( fmul( 4, cos( cos( fdiv( pi, fmul( n, 2 ) ) ) ) ), 1 ) ),
                                   sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ) ] ),
                          fmul( 12, sin( sin( fdiv( pi, n ) ) ) ) ),
                    sin( fdiv( fmul( 3, pi ), fmul( 2, n ) ) ),
                    power( k, 3 ) ] )


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
    return fadd( fprod( [ fdiv( n, 2 ), power( k, 2 ), cot( fdiv( pi, n ) ) ] ), fprod( [ n, k, h, ] ) )


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
    return fprod( [ fdiv( n, 4 ), h, power( k, 2 ), cot( fdiv( pi, n ) ) ] )

