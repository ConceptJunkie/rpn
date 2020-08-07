#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocation.py
#
#  rpnChilada location class declarations
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import bz2
import contextlib
import os
import pickle

import ephem

from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from mpmath import fadd, fdiv, fmul, mpmathify, pi
from timezonefinder import TimezoneFinder

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnOutput import convertToBaseN
from rpn.rpnUtils import getUserDataPath, oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnVersion import RPN_PROGRAM_NAME

import rpn.rpnGlobals as g


#******************************************************************************
#
#  class RPNLocation
#
#  The observer class measures lat/long in radians, but no one else does,
#  so the methods assume degrees.
#
#******************************************************************************

class RPNLocation( ):
    observer = None
    name = None

    '''This class represents a location on the surface of the Earth.'''
    def __init__( self, *args, **kwargs ):
        name = kwargs.get( 'name', None )
        observer = kwargs.get( 'observer', None )
        lat = kwargs.get( 'lat', None )
        long = kwargs.get( 'long', None )

        if observer:
            self.observer = observer
        else:
            self.observer = ephem.Observer( )

        if lat:
            self.setLat( lat )

        if long:
            self.setLong( long )

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


#******************************************************************************
#
#  makeLocation
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def makeLocation( n, k ):
    return RPNLocation( lat=float( n ), long=float( k ) )


#******************************************************************************
#
#  loadLocationCache
#
#******************************************************************************

def loadLocationCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep +
                                              'locations.pckl.bz2', 'rb' ) ) as pickleFile:
            locationCache = pickle.load( pickleFile )
    except FileNotFoundError:
        locationCache = { }

    return locationCache


#******************************************************************************
#
#  saveLocationCache
#
#******************************************************************************

def saveLocationCache( locationCache ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep +
                                              'locations.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( locationCache, pickleFile )


#******************************************************************************
#
#  getLocation
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLocation( name ):
    if not isinstance( name, str ):
        raise ValueError( '\'location\' expects a string argument' )

    if g.locationCache is None:
        g.locationCache = loadLocationCache( )

    if name in g.locationCache:
        locationInfo = g.locationCache[ name ]

        observer = ephem.Observer( )
        result = RPNLocation( name=name, observer=observer )

        result.setLat( locationInfo[ 1 ] )
        result.setLong( locationInfo[ 2 ] )

        # print( 'looked up', result.name )
        # print( 'lat/long', result.getLat( ), result.getLong( ) )
        return result

    geolocator = Nominatim( user_agent=RPN_PROGRAM_NAME )

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
    result = RPNLocation( name=name, observer=observer )

    result.setLat( location.latitude )
    result.setLong( location.longitude )

    g.locationCache[ name ] = [ name, result.getLat( ), result.getLong( ) ]
    saveLocationCache( g.locationCache )

    return result


#******************************************************************************
#
#  getLocationInfo
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLocationInfo( location ):
    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    return [ fdiv( fmul( mpmathify( location.observer.lat ), 180 ), pi ),
             fdiv( fmul( mpmathify( location.observer.long ), 180 ), pi ) ]


#******************************************************************************
#
#  getTimeZone
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getTimeZone( location ):
    tzFinder = TimezoneFinder( )

    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    timezoneName = tzFinder.timezone_at( lat = location.getLat( ), lng = location.getLong( ) )

    if timezoneName is None:
        timezoneName = tzFinder.closest_timezone_at( lat = location.getLat( ),
                                                     lng = location.getLong( ) )

    return timezoneName


#******************************************************************************
#
#  getGeographicDistance
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getGeographicDistance( location1, location2 ):
    from rpn.rpnMeasurement import RPNMeasurement

    if isinstance( location1, str ):
        location1 = getLocation( location1 )

    if isinstance( location2, str ):
        location2 = getLocation( location2 )

    print( 'location1', location1 )
    print( 'location2', location2 )
    print( 'location1.observer', location1.observer )
    print( 'location2.observer', location2.observer )

    if not isinstance( location1, RPNLocation ) or not isinstance( location2, RPNLocation ):
        raise ValueError( 'two location arguments expected' )

    distance = vincenty( ( location1.getLat( ), location1.getLong( ) ),
                         ( location2.getLat( ), location2.getLong( ) ) ).miles

    return RPNMeasurement( distance, [ { 'miles' : 1 } ] )


#******************************************************************************
#
#  convertLatLongToNAC
#
#  https://en.wikipedia.org/wiki/Natural_Area_Code
#
#******************************************************************************

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

