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
import contextlib
import os
import pickle

import ephem

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from mpmath import fadd, fdiv, fmul, mpmathify, pi
from timezonefinder import TimezoneFinder

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnLocationClass import RPNLocation
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnOutput import convertToBaseN
from rpn.rpnUtils import getUserDataPath, oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, RealValidator, StringValidator, StringOrLocationValidator
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
@argValidator( [ StringValidator ] )
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
#  getLocationInfoOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ StringOrLocationValidator ] )
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
@argValidator( [ StringOrLocationValidator ] )
def getTimeZoneOperator( location ):
    return getTimeZone( location )


#******************************************************************************
#
#  getGeographicDistanceOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ StringOrLocationValidator, StringOrLocationValidator ] )
def getGeographicDistanceOperator( location1, location2 ):
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

@oneArgFunctionEvaluator( )
@argValidator( [ StringOrLocationValidator ] )
def convertLatLongToNACOperator( n ):
    if isinstance( n, str ):
        n = getLocation( n )
    elif isinstance( args, RPNLocation ):
        lat = n.getLat( )
        long = n.getLong( )

    numerals = '0123456789BCDFGHJKLMNPQRSTVWXZ'

    if lat > 90.0 or lat < -90.0:
        raise ValueError( '\'natural_area_code\' requires a latitude parameter of -90 to 90' )

    if long > 180.0 or long < -180.0:
        raise ValueError( '\'natural_area_code\' requires a longitutde parameter of -180 to 180' )

    lat = fdiv( fadd( lat, 90 ), 180 ) * 729000000
    long = fdiv( fadd( long, 180 ), 360 ) * 729000000   # 30 ** 6

    return convertToBaseN( long, 30, False, numerals ) + ' ' + convertToBaseN( lat, 30, False, numerals )

