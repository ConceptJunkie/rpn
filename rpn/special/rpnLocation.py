#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocation.py
#
#  rpnChilada location operators
#  copyright (c) 2024, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import ephem
import pendulum

from geopy.distance import geodesic

from mpmath import fdiv, fmul, mpmathify, pi

from rpn.special.rpnLocationClass import RPNLocation

from rpn.time.rpnDateTimeClass import RPNDateTime

from rpn.units.rpnMeasurementClass import RPNMeasurement
from rpn.special.rpnLocationLookup import lookUpLocation

from rpn.special.rpnLocationLookup import lookUpTimeZone
from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, LocationValidator, LocationOrDateTimeValidator, RealValidator, \
                             StringValidator

import rpn.util.rpnGlobals as g


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
#  getLocation
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def getLocation( name ):
    if not isinstance( name, str ):
        raise ValueError( '\'location\' expects a string argument' )

    latitude, longitude = lookUpLocation(name)

    observer = ephem.Observer( )
    result = RPNLocation( name=name, observer=observer )

    result.setLat( latitude )
    result.setLong( longitude )

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
        return value.getTZ( ).name
    elif isinstance( value, pendulum.Timezone ):
        return value.name
    elif isinstance( value, str ):
        value = getLocation( value )
    elif not isinstance( value, RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    return lookUpTimeZone( value.getLat( ), value.getLong( ) ).name


def getTimeZone( value ):
    if isinstance( value, RPNDateTime ):
        return value.tz
    elif isinstance( value, pendulum.Timezone ):
        return value
    elif isinstance( value, RPNLocation ):
        return lookUpTimeZone( value.getLat( ), value.getLong( ) )

    try:
        tz = pendulum.timezone( value )
    except pendulum.tz.exceptions.InvalidTimezone:
        tz = lookUpTimeZone( *lookUpLocation( value ) )

    return tz

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
    tz = getTimeZone( value )

    return RPNMeasurement( pendulum.from_timestamp(0, tz).offset, 'seconds' )


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
