#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnLocation.py
# //
# //  RPN command-line calculator RPNLocationn class declaration
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

if not six.PY3:
    FileNotFoundError = IOError

import bz2
import contextlib
import pickle
import ephem
import os

from mpmath import fadd, fdiv, fmul, mpmathify, pi

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnOutput import convertToBaseN
from rpn.rpnPhysics import calculateDistance
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNLocation
# //
# //  The observer class measures lat/long in radians, but no one else does,
# //  so the methods assume degrees.
# //
# //******************************************************************************

class RPNLocation( object ):
    '''This class represents a location on the surface of the Earth.'''
    def __init__( self, name, observer=ephem.Observer( ) ):
        self.name = name
        self.observer = observer

    def setObserver( self, observer ):
        self.observer.lat = observer.lat
        self.observer.long = observer.long
        self.observer.epoch = observer.epoch
        self.observer.date = observer.date
        self.observer.elevation = observer.elevation
        self.observer.temp = observer.temp
        self.observer.pressure = observer.pressure

    def getName( self ):
        return self.name

    def getLat( self ):
        return fdiv( fmul( mpmathify( float( self.observer.lat ) ), 180 ), pi )

    def getLong( self ):
        return fdiv( fmul( mpmathify( float( self.observer.long ) ), 180 ), pi )

    def getDate( self ):
        return self.observer.date

    def getEpoch( self ):
        return self.observer.epoch

    def getElevation( self ):
        return self.observer.elevation

    def getTemp( self ):
        return self.observer.temp

    def getPressure( self ):
        return self.observer.pressure

    def setName( self, value ):
        self.name = value

    def setLat( self, value ):
        self.observer.lat = fmul( fdiv( value, 180 ), pi )

    def setLong( self, value ):
        self.observer.long = fmul( fdiv( value, 180 ), pi )

    def setDate( self, value ):
        self.observer.date = value

    def setEpoch( self, value ):
        self.observer.epoch = value

    def setElevation( self, value ):
        self.observer.elevation = value

    def setTemp( self, value ):
        self.observer.temp = value

    def setPressure( self, value ):
        self.observer.pressure = value


# //******************************************************************************
# //
# //  loadLocationCache
# //
# //******************************************************************************

def loadLocationCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'locations.pckl.bz2', 'rb' ) ) as pickleFile:
            locationCache = pickle.load( pickleFile )
    except FileNotFoundError:
        locationCache = { }

    return locationCache


# //******************************************************************************
# //
# //  saveLocationCache
# //
# //******************************************************************************

def saveLocationCache( locationCache ):
    from rpn.rpnKeyboard import DelayedKeyboardInterrupt

    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'locations.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( locationCache, pickleFile )


# //******************************************************************************
# //
# //  getLocation
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLocation( name ):
    if not isinstance( name, str ):
        raise ValueError( '\'location\' expects a string argument' )

    if g.locationCache is None:
        g.locationCache = loadLocationCache( )

    if name in g.locationCache:
        locationInfo = g.locationCache[ name ]

        observer = ephem.Observer( )
        result = RPNLocation( name, observer )

        result.setLat( locationInfo[ 1 ] )
        result.setLong( locationInfo[ 2 ] )

        # print( 'looked up', result.name )
        # print( 'lat/long', result.getLat( ), result.getLong( ) )
        return result

    from geopy.geocoders import Nominatim
    geolocator = Nominatim( )

    for attempts in range( 3 ):
        try:
            location = geolocator.geocode( name )
            break
        except:
            if attempts == 2:
                raise ValueError( 'location lookup connection failure, check network connectivity' )

    if location is None:
        raise ValueError( 'location lookup failed, try a different search term' )

    observer = ephem.Observer( )
    result = RPNLocation( name, observer )

    result.setLat( location.latitude )
    result.setLong( location.longitude )

    result = RPNLocation( name, observer )

    g.locationCache[ name ] = [ name, result.getLat( ), result.getLong( ) ]
    saveLocationCache( g.locationCache )

    return result


# //******************************************************************************
# //
# //  getLocationInfo
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLocationInfo( location ):
    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    return [ fdiv( fmul( mpmathify( location.observer.lat ), 180 ), pi ),
             fdiv( fmul( mpmathify( location.observer.long ), 180 ), pi ) ]


# //******************************************************************************
# //
# //  getTimeZone
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getTimeZone( location ):
    from timezonefinder import TimezoneFinder

    tf = TimezoneFinder( )

    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    timezone_name = tf.timezone_at( lat = location.getLat( ), lng = location.getLong( ) )

    if timezone_name is None:
        timezone_name = tf.closest_timezone_at( lat = location.getLat( ),
                                                lng = location.getLong( ) )

    return timezone_name


# //******************************************************************************
# //
# //  getDistance
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getDistance( location1, location2 ):
    # if measurements were passed in, we want the physics version of 'distance'
    if isinstance( location1, RPNMeasurement ) or isinstance( location2, RPNMeasurement ):
        return calculateDistance( location1, location2 )

    if isinstance( location1, str ):
        location1 = getLocation( location1 )

    if isinstance( location2, str ):
        location2 = getLocation( location2 )

    if not isinstance( location1, RPNLocation ) or not isinstance( location2, RPNLocation ):
        return calculateDistance( location1, location2 )

    from geopy.distance import vincenty

    distance = vincenty( ( location1.getLat( ), location1.getLong( ) ),
                         ( location2.getLat( ), location2.getLong( ) ) ).miles

    return RPNMeasurement( distance, [ { 'mile' : 1 } ] )


# //******************************************************************************
# //
# //  convertLatLongToNAC
# //
# //  https://en.wikipedia.org/wiki/Natural_Area_Code
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertLatLongToNAC( args ):
    if isinstance( args, RPNGenerator ):
        return convertLatLongToNAC( list( args ) )
    elif not isinstance( args, list ):
        args = [ args, 0 ]
    elif args and isinstance( args[ 0 ], list ):
        return [ convertLatLongToNAC( i ) for i in args ]
    elif len( args ) == 1:
        args.append( 0 )

    numerals = '0123456789BCDFGHJKLMNPQRSTVWXZ'

    if args[ 0 ] > 90.0 or args[ 0 ] < -90.0:
        raise ValueError( '\'natural_area_code\' requires a latitude parameter of -90 to 90' )

    if args[ 1 ] > 180.0 or args[ 1 ] < -180.0:
        raise ValueError( '\'natural_area_code\' requires a longitutde parameter of -180 to 180' )

    lat = fdiv( fadd( args[ 0 ], 90 ), 180 ) * 729000000
    long = fdiv( fadd( args[ 1 ], 180 ), 360 ) * 729000000   # 30 ** 6

    return convertToBaseN( long, 30, False, numerals ) + ' ' + convertToBaseN( lat, 30, False, numerals )

