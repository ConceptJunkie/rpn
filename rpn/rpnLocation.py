#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocation.py
#
#  rpnChilada location operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import bz2
import datetime
import contextlib
import os
import pickle

import ephem
import pytz

from geopy.distance import geodesic
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from mpmath import fadd, fdiv, fmul, mpmathify, pi
from timezonefinder import TimezoneFinder

from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnLocationClass import RPNLocation
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnOutput import convertToBaseN
from rpn.rpnUtils import getUserDataPath, oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, DefaultValidator, LocationValidator, RealValidator, StringValidator
from rpn.rpnVersion import RPN_PROGRAM_NAME

import rpn.rpnGlobals as g


#******************************************************************************
#
#  makeLocationOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( 0, 90 ), RealValidator( -180, 180 ) ] )
def makeLocationOperator( n, k ):
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
@argValidator( [ StringValidator( ) ] )
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
        except GeocoderUnavailable:
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
#  getLocationInfoOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ LocationValidator( ) ] )
def getLocationInfoOperator( location ):
    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    return [ fdiv( fmul( mpmathify( location.observer.lat ), 180 ), pi ),
             fdiv( fmul( mpmathify( location.observer.long ), 180 ), pi ) ]


#******************************************************************************
#
#  getTimeZoneOperator
#
#******************************************************************************

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


@oneArgFunctionEvaluator( )
@argValidator( [ LocationValidator( ) ] )
def getTimeZoneOperator( location ):
    return getTimeZone( location )


#******************************************************************************
#
#  getTimeZoneOffsetOperator
#
#******************************************************************************

def getTimeZoneOffset( location ):
    timezoneName = getTimeZone( location )
    # compute the timezone's offset
    today = datetime.datetime.now( )
    tz_target = pytz.timezone( timezoneName )

    if tz_target:
        today_target = tz_target.localize( today )
        today_utc = pytz.utc.localize( today )
        return ( today_utc - today_target ).total_seconds( ) / 60

    return 0


@oneArgFunctionEvaluator( )
@argValidator( [ LocationValidator( ) ] )
def getTimeZoneOffsetOperator( location ):
    return getTimeZoneOffset( location )


#******************************************************************************
#
#  getGeographicDistanceOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ LocationValidator( ), LocationValidator( ) ] )
def getGeographicDistanceOperator( location1, location2 ):
    if isinstance( location1, str ):
        location1 = getLocation( location1 )

    if isinstance( location2, str ):
        location2 = getLocation( location2 )

    if not isinstance( location1, RPNLocation ) or not isinstance( location2, RPNLocation ):
        raise ValueError( 'two location arguments expected' )

    distance = geodesic( ( location1.getLat( ), location1.getLong( ) ),
                         ( location2.getLat( ), location2.getLong( ) ) ).miles

    return RPNMeasurement( distance, [ { 'miles' : 1 } ] )


#******************************************************************************
#
#  convertLatLongToNACOperator
#
#  https://en.wikipedia.org/wiki/Natural_Area_Code
#
#******************************************************************************

@argValidator( [ DefaultValidator( ) ] )
def convertLatLongToNACOperator( n ):
    if isinstance( n[ 0 ], str ):
        n = getLocation( n[ 0 ] )
        lat = n.getLat( )
        long = n.getLong( )
    elif isinstance( n, list ) and len( n ) == 2:
        lat = n[ 0 ]
        long = n[ 1 ]
    elif isinstance( n[ 0 ], RPNLocation ):
        lat = n[ 0 ].getLat( )
        long = n[ 0 ].getLong( )
    else:
        raise ValueError( 'location or lat-long (in a list) expected' )

    numerals = '0123456789BCDFGHJKLMNPQRSTVWXZ'

    if lat > 90.0 or lat < -90.0:
        raise ValueError( '\'natural_area_code\' requires a latitude parameter of -90 to 90' )

    if long > 180.0 or long < -180.0:
        raise ValueError( '\'natural_area_code\' requires a longitutde parameter of -180 to 180' )

    lat = fdiv( fadd( lat, 90 ), 180 ) * 729000000
    long = fdiv( fadd( long, 180 ), 360 ) * 729000000   # 30 ** 6

    return convertToBaseN( long, 30, False, numerals ) + ' ' + convertToBaseN( lat, 30, False, numerals )
