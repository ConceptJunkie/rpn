#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocation.py
#
#  rpnChilada location operators
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
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

from dateutil import tz

from geopy.distance import geodesic
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from mpmath import fdiv, fmul, mpmathify, pi
from timezonefinder import TimezoneFinder

from rpn.rpnDateTimeClass import RPNDateTime
from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnLocationClass import RPNLocation
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnUtils import getUserDataPath, oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, LocationValidator, LocationOrDateTimeValidator, RealValidator, \
                             StringValidator
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

    location = None

    for attempts in range( 3 ):
        try:
            location = geolocator.geocode( name )
            break
        except GeocoderUnavailable as e:
            if attempts == 2:
                raise ValueError( 'location lookup connection failure, check network connectivity' ) from e

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

def getTimeZoneName( value ):
    if isinstance( value, RPNDateTime ):
        return value.tzname( )

    if isinstance( value, str ):
        value = getLocation( value )
    elif not isinstance( value, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    tzFinder = TimezoneFinder( )
    timezoneName = tzFinder.timezone_at( lat = value.getLat( ), lng = value.getLong( ) )

    if timezoneName is None:
        timezoneName = tzFinder.closest_timezone_at( lat = value.getLat( ),
                                                     lng = value.getLong( ) )

    return timezoneName


def getTimeZone( name ):
    return tz.gettz( getTimeZoneName( name ) )


@oneArgFunctionEvaluator( )
@argValidator( [ LocationOrDateTimeValidator( ) ] )
def getTimeZoneOperator( location ):
    return getTimeZoneName( location )


#******************************************************************************
#
#  getTimeZoneOffsetOperator
#
#******************************************************************************

def getTimeZoneOffset( value ):
    if isinstance( value, str ):
        try:
            timezone = pytz.timezone( value )
        except pytz.exceptions.UnknownTimeZoneError:
            timezone = pytz.timezone( getTimeZoneName( value ) )
    else:
        timezone = pytz.timezone( getTimeZoneName( value ) )

    # compute the timezone's offset
    now = datetime.datetime.now( )

    if timezone:
        now1 = timezone.localize( now )
        now2 = pytz.utc.localize( now )
        return RPNMeasurement( ( now2 - now1 ).total_seconds( ), 'seconds' )

    return RPNMeasurement( 0, 'seconds' )


@oneArgFunctionEvaluator( )
@argValidator( [ LocationOrDateTimeValidator( ) ] )
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
