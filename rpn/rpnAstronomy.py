#!/usr/bin/env python

#******************************************************************************
#
#  rpnAstronomy.py
#
#  rpnChilada astronomical operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import ephem

from dateutil import tz

from mpmath import acos, fadd, fdiv, fmul, fsub, mpmathify, pi, power, sqrt
from skyfield import almanac

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnLocation import getLocation, getTimeZone
from rpn.rpnMatchUnitTypes import matchUnitTypes
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnMath import subtract
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         loadAstronomyData
from rpn.rpnValidator import argValidator, DateTimeValidator, IntValidator, YearValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  class RPNAstronomicalObject
#
#******************************************************************************

class RPNAstronomicalObject( ):
    '''This class is for identifying astronomical objects.'''
    def __init__( self, object ):
        self.object = object

    def getDistanceFromEarth( self, date=None ):
        if date:
            self.object.compute( date.to( 'utc' ).format( ) )

        return RPNMeasurement( fmul( self.object.earth_distance, ephem.meters_per_au ), 'meters' )

    def getAngularSize( self, location=None, date=None ):
        if location and date:
            if isinstance( location, str ):
                location = getLocation( location )

            location.observer.date = date.to( 'utc' ).format( )
            self.object.compute( location.observer )

        # I have no idea why size seems to return the value in arcseconds... that
        # goes against the pyephem documentation that it always uses radians for angles.
        return RPNMeasurement( mpmathify( fdiv( fmul( fdiv( self.object.size, 3600 ), pi ), 180 ) ), 'radian' )

    def getAngularSeparation( self, other, location, date ):
        if isinstance( location, str ):
            location = getLocation( location )

        location.observer.date = date.to( 'utc' ).format( )

        self.object.compute( location.observer )
        other.object.compute( location.observer )

        return RPNMeasurement( mpmathify( ephem.separation( ( self.object.az, self.object.alt ),
                                                            ( other.object.az, other.object.alt ) ) ), 'radian' )

    def getAzimuthAndAltitude( self, location=None, date=None ):
        if location and date:
            if isinstance( location, str ):
                location = getLocation( location )

            location.observer.date = date.to( 'utc' ).format( )
            self.object.compute( location.observer )

        return RPNMeasurement( mpmathify( self.object.az ), 'radians' ), \
               RPNMeasurement( mpmathify( self.object.alt ), 'radians' )

    def getAstronomicalEvent( self, location, date, func, horizon=None, useCenter=False, matchUSNO=False ):
        if isinstance( location, str ):
            location = getLocation( location )

        if horizon is None:
            horizon = float( location.observer.horizon )

        if matchUSNO:
            location.pressure = 0
            horizon -= 34 / 60        # 34 arcminutes

        oldHorizon = location.observer.horizon

        location.observer.date = date.to( 'utc' ).format( )
        location.observer.horizon = str( horizon )

        #print( 'date', date )
        #print( 'utc date', location.observer.date )

        if useCenter:
            result = RPNDateTime.convertFromEphemDate( func( location.observer, self.object, use_center=useCenter ) ).getLocalTime( )
        else:
            result = RPNDateTime.convertFromEphemDate( func( location.observer, self.object ) ).getLocalTime( )

        location.observer.horizon = oldHorizon

        return result

    def getNextRising( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.next_rising, horizon, useCenter, matchUSNO )

    def getNextSetting( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.next_setting, horizon, useCenter, matchUSNO )

    def getNextTransit( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.next_transit, horizon, useCenter, matchUSNO )

    def getNextAntitransit( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.next_antitransit, horizon, useCenter, matchUSNO )

    def getPreviousRising( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.previous_rising, horizon, useCenter, matchUSNO )

    def getPreviousSetting( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.previous_setting, horizon, useCenter, matchUSNO )

    def getPreviousTransit( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.previous_transit, horizon, useCenter, matchUSNO )

    def getPreviousAntitransit( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        return self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                          ephem.Observer.previous_antitransit, horizon, useCenter, matchUSNO )

    def getTransitTime( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        result1 = self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                             ephem.Observer.next_rising, horizon, useCenter, matchUSNO )
        result2 = self.getAstronomicalEvent( arguments[ 'location' ], result1,
                                             ephem.Observer.next_setting, horizon, useCenter, matchUSNO )

        return subtract( result2, result1 )

    def getAntitransitTime( self, arg1, arg2, horizon=None, useCenter=False, matchUSNO=False ):
        validUnitTypes = [ [ 'location', 'datetime' ] ]
        arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

        if not arguments:
            raise ValueError( 'unexpected arguments' )

        result1 = self.getAstronomicalEvent( arguments[ 'location' ], arguments[ 'datetime' ],
                                             ephem.Observer.next_setting, horizon, useCenter, matchUSNO )
        result2 = self.getAstronomicalEvent( arguments[ 'location' ], result1,
                                             ephem.Observer.next_rising, horizon, useCenter, matchUSNO )

        return subtract( result2, result1 )


#******************************************************************************
#
#  getSeasonOperator
#
#  0 = spring, 1 = summer, 2 = mn, 3 = winter
#
#******************************************************************************

def getSeason( n, season ):
    '''Returns the date of the season for year n.'''
    loadAstronomyData( )

    if isinstance( n, RPNDateTime ):
        n = n.year

    if not g.astroDataAvailable:
        raise ValueError( 'Astronomy functions are unavailable.' )

    times, _ = almanac.find_discrete( g.timescale.utc( n, 1, 1 ),
                                      g.timescale.utc( n, 12, 31 ), almanac.seasons( g.ephemeris ) )
    result = RPNDateTime.parseDateTime( times[ season ].utc_datetime( ) )
    return result.getLocalTime( )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0, 3 ) ] )
def getSeasonOperator( n, season ):
    getSeason( n, season )


#******************************************************************************
#
#  getVernalEquinox
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( 0 ) ] )
def getVernalEquinoxOperator( n ):
    '''Returns the date of the vernal equinox for year n.'''
    return getSeason( n, 0 )


#******************************************************************************
#
#  getSummerSolstice
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( 0 ) ] )
def getSummerSolsticeOperator( n ):
    '''Returns the date of the summer solstice for year n.'''
    return getSeason( n, 1 )


#******************************************************************************
#
#  getAutumnalEquinox
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( 0 ) ] )
def getAutumnalEquinoxOperator( n ):
    '''Returns the date of the autumnal equinox for year n.'''
    return getSeason( n, 2 )


#******************************************************************************
#
#  getWinterSolstice
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( 0 ) ] )
def getWinterSolsticeOperator( n ):
    '''Returns the date of the winter solstice for year n.'''
    return getSeason( n, 3 )


#******************************************************************************
#
#  getEphemTime
#
#******************************************************************************

def getEphemTime( n, func ):
    '''Returns a pyephem date-time value from an RPNDateTime value.'''
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'expected a date-time argument' )

    # We always convert to UTC when passing to any third-party library, and
    # convert the answer back to the previous timezone.
    tzinfo = n.tzinfo

    result = RPNDateTime.convertFromEphemDate( func( n.to( 'utc' ).format( ) ) )
    result.tzinfo = tz.UTC
    return result.getLocalTime( tzinfo )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getNextFirstQuarterMoonOperator( n ):
    return getEphemTime( n, ephem.next_first_quarter_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getNextFullMoonOperator( n ):
    return getEphemTime( n, ephem.next_full_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getNextLastQuarterMoonOperator( n ):
    return getEphemTime( n, ephem.next_last_quarter_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getNextNewMoonOperator( n ):
    return getEphemTime( n, ephem.next_new_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getPreviousFirstQuarterMoonOperator( n ):
    return getEphemTime( n, ephem.previous_first_quarter_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getPreviousFullMoonOperator( n ):
    return getEphemTime( n, ephem.previous_full_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getPreviousLastQuarterMoonOperator( n ):
    return getEphemTime( n, ephem.previous_last_quarter_moon )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getPreviousNewMoonOperator( n ):
    return getEphemTime( n, ephem.previous_new_moon )


#******************************************************************************
#
#  getMoonPhaseOperator
#
#******************************************************************************

def getMoonPhase( n ):
    '''Returns the current moon phase as a percentage, starting from the new moon.'''
    datetime = n.format( )

    previous = RPNDateTime.convertFromEphemDate( ephem.previous_new_moon( datetime ) )
    next = RPNDateTime.convertFromEphemDate( ephem.next_new_moon( datetime ) )

    cycle = next - previous
    current = n - previous

    return current.total_seconds( ) / cycle.total_seconds( )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getMoonPhaseOperator( n ):
    return getMoonPhase( n )


#******************************************************************************
#
#  getSkyLocation
#
#******************************************************************************

def getSkyLocationOperator( arg1, arg2, arg3 ):
    '''Returns the location of an astronomical object in the sky in terms of azimuth and altitude.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    azimuth, altitude = arguments[ 'body' ].getAzimuthAndAltitude( arguments[ 'location' ], arguments[ 'datetime' ] )

    return [ azimuth.convert( 'degree' ), altitude.convert( 'degree' ) ]


#******************************************************************************
#
#  getAngularSizeOperator
#
#******************************************************************************

def getAngularSizeOperator( arg1, arg2, arg3 ):
    '''Returns the angular size of an astronomical object in radians.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    return arguments[ 'body' ].getAngularSize( arguments[ 'location' ], arguments[ 'datetime' ] )


#******************************************************************************
#
#  getAngularSeparationOperator
#
#******************************************************************************

def getAngularSeparationOperator( body1, body2, arg3, arg4 ):
    '''Returns the angular separation of two astronomical objects in radians.'''
    validUnitTypes = [ [ 'location', 'datetime' ] ]
    arguments = matchUnitTypes( [ arg3, arg4 ], validUnitTypes )

    if not isinstance( body1, RPNAstronomicalObject ) or not isinstance( body2, RPNAstronomicalObject ) or \
       not arguments:
        raise ValueError( 'expected two astronomical objects, a location and a date-time' )

    return body1.getAngularSeparation( body2, arguments[ 'location' ], arguments[ 'datetime' ] )


#******************************************************************************
#
#  getNextRisingOperator
#
#******************************************************************************

def getNextRising( arg1, arg2, arg3 ):
    '''Returns the next rising time for an astronomical object.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getNextRising( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getNextSunriseOperator( n, k ):
    return getNextRising( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


@twoArgFunctionEvaluator( )
def getNextMoonRiseOperator( n, k ):
    return getNextRising( RPNAstronomicalObject( ephem.Moon( ) ), n, k )


def getNextRisingOperator( arg1, arg2, arg3 ):
    return getNextRising( arg1, arg2, arg3 )


#******************************************************************************
#
#  getNextSettingOperator
#
#******************************************************************************

def getNextSetting( arg1, arg2, arg3 ):
    '''Returns the next setting time for an astronomical object.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getNextSetting( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getNextSunsetOperator( n, k ):
    return getNextSetting( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


@twoArgFunctionEvaluator( )
def getNextMoonSetOperator( n, k ):
    return getNextSetting( RPNAstronomicalObject( ephem.Moon( ) ), n, k )


def getNextSettingOperator( arg1, arg2, arg3 ):
    return getNextSetting( arg1, arg2, arg3 )


#******************************************************************************
#
#  getNextTransitOperator
#
#******************************************************************************

def getNextTransit( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getNextTransit( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getSolarNoonOperator( n, k ):
    return getNextTransit( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


@twoArgFunctionEvaluator( )
def getNextMoonTransitOperator( n, k ):
    return getNextTransit( RPNAstronomicalObject( ephem.Moon( ) ), n, k )


def getNextTransitOperator( arg1, arg2, arg3 ):
    return getNextTransit( arg1, arg2, arg3 )


#******************************************************************************
#
#  getNextAntitransitOperator
#
#******************************************************************************

def getNextAntitransit( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getNextAntitransit( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getNextSunAntitransitOperator( n, k ):
    return getNextAntitransit( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


@twoArgFunctionEvaluator( )
def getNextMoonAntitransitOperator( n, k ):
    return getNextAntitransit( RPNAstronomicalObject( ephem.Moon( ) ), n, k )


def getNextAntitransitOperator( arg1, arg2, arg3 ):
    return getNextTransit( arg1, arg2, arg3 )


#******************************************************************************
#
#  getTransitTimeOperator
#
#******************************************************************************

def getTransitTime( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    return arguments[ 'body' ].getTransitTime( arguments[ 'location' ], arguments[ 'datetime' ] )


@twoArgFunctionEvaluator( )
def getDayTimeOperator( n, k ):
    return getTransitTime( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


def getTransitTimeOperator( arg1, arg2, arg3 ):
    return getTransitTime( arg1, arg2, arg3 )


#******************************************************************************
#
#  getAntitransitTimeOperator
#
#******************************************************************************

def getAntitransitTime( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    return arguments[ 'body' ].getAntitransitTime( arguments[ 'location' ], arguments[ 'datetime' ] )


@twoArgFunctionEvaluator( )
def getNightTimeOperator( n, k ):
    return getAntitransitTime( RPNAstronomicalObject( ephem.Sun( ) ), n, k )


def getAntitransitTimeOperator( arg1, arg2, arg3 ):
    return getAntitransitTime( arg1, arg2, arg3 )


#******************************************************************************
#
#  getPreviousRisingperator
#
#******************************************************************************

def getPreviousRising( arg1, arg2, arg3 ):
    '''Returns the previous rising time for an astronomical object.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getPreviousRising( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


def getPreviousRisingOperator( arg1, arg2, arg3 ):
    return getPreviousRising( arg1, arg2, arg3 )


#******************************************************************************
#
#  getPreviousSettingOperator
#
#******************************************************************************

def getPreviousSetting( arg1, arg2, arg3 ):
    '''Returns the previous setting time for an astronomical object.'''
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getPreviousSetting( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


def getPreviousSettingOperator( arg1, arg2, arg3 ):
    return getPreviousSetting( arg1, arg2, arg3 )


#******************************************************************************
#
#  getPreviousTransitOperator
#
#******************************************************************************

def getPreviousTransit( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getPreviousTransit( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


def getPreviousTransitOperator( arg1, arg2, arg3 ):
    return getPreviousTransit( arg1, arg2, arg3 )


#******************************************************************************
#
#  getPreviousAntitransitOperator
#
#******************************************************************************

def getPreviousAntitransit( arg1, arg2, arg3 ):
    validUnitTypes = [ [ 'location', 'datetime', 'body' ] ]
    arguments = matchUnitTypes( [ arg1, arg2, arg3 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = arguments[ 'body' ].getPreviousAntitransit( arguments[ 'location' ], arguments[ 'datetime' ] )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


def getPreviousAntitransitOperator( arg1, arg2, arg3 ):
    return getPreviousAntitransit( arg1, arg2, arg3 )


#******************************************************************************
#
#  getNextDawnOperator
#
#  -6 is "civil" twilight
#  -12 is nautical twilight
#  -18 is astronomical twilight
#
#******************************************************************************

def getNextDawn( arg1, arg2, horizon = -6 ):
    validUnitTypes = [ [ 'location', 'datetime' ] ]
    arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = RPNAstronomicalObject( ephem.Sun( ) ).getNextRising( arguments[ 'location' ],
                                                                  arguments[ 'datetime' ], horizon=horizon )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getNextCivilDawnOperator( n, k ):
    return getNextDawn( n, k, -6 )


@twoArgFunctionEvaluator( )
def getNextNauticalDawnOperator( n, k ):
    return getNextDawn( n, k, -12 )


@twoArgFunctionEvaluator( )
def getNextAstronomicalDawnOperator( n, k ):
    return getNextDawn( n, k, -18 )


#******************************************************************************
#
#  getNextDuskOperator
#
#  -6 is "civil" twilight
#  -12 is nautical twilight
#  -18 is astronomical twilight
#
#******************************************************************************

def getNextDusk( arg1, arg2, horizon = -6 ):
    validUnitTypes = [ [ 'location', 'datetime' ] ]
    arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    result = RPNAstronomicalObject( ephem.Sun( ) ).getNextSetting( arguments[ 'location' ],
                                                                   arguments[ 'datetime' ], horizon=horizon )
    return result.getLocalTime( tz.gettz( getTimeZone( arguments[ 'location' ] ) ) )


@twoArgFunctionEvaluator( )
def getNextCivilDuskOperator( n, k ):
    return getNextDusk( n, k, -6 )


@twoArgFunctionEvaluator( )
def getNextNauticalDuskOperator( n, k ):
    return getNextDusk( n, k, -12 )


@twoArgFunctionEvaluator( )
def getNextAstronomicalDuskOperator( n, k ):
    return getNextDusk( n, k, -18 )


#******************************************************************************
#
#  getDistanceFromEarthOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getDistanceFromEarthOperator( arg1, arg2 ):
    validUnitTypes = [ [ 'body', 'datetime' ] ]
    arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

    if not arguments:
        raise ValueError( 'unexpected arguments' )

    return RPNMeasurement( arguments[ 'body' ].getDistanceFromEarth( arguments[ 'datetime' ] ), 'meters' )


#******************************************************************************
#
#  getCircleIntersectionTerm
#
#  http://mathworld.wolfram.com/Circle-CircleIntersection.html
#
#******************************************************************************

def getCircleIntersectionTerm( radius1, radius2, separation ):
    distance = fdiv( fadd( fsub( power( separation, 2 ), power( radius1, 2 ) ),
                           power( radius2, 2 ) ),
                     fmul( 2, separation ) )

    #print( 'radius1', radius1 )
    #print( 'radius2', radius2 )
    #print( 'distance', distance )
    #print( 'radius1 - distance', fsub( radius1, distance ) )
    #print( 'radius1^2 - distance^2', fsub( power( radius1, 2 ), power( distance, 2 ) ) )
    #print( )

    if power( distance, 2 ) > power( radius1, 2 ):
        return fmul( power( radius1, 2 ), fdiv( pi, 2 ) )

    return fsub( fmul( power( radius1, 2 ), acos( fdiv( distance, radius1 ) ) ),
                 fmul( distance, sqrt( fsub( power( radius1, 2 ), power( distance, 2 ) ) ) ) )


#******************************************************************************
#
#  getEclipseTotality
#
#******************************************************************************

def getEclipseTotalityOperator( body1, body2, arg1, arg2 ):
    '''Returns the angular size of an astronomical object in radians.'''
    validUnitTypes = [ [ 'location', 'datetime' ] ]
    arguments = matchUnitTypes( [ arg1, arg2 ], validUnitTypes )

    if not isinstance( body1, RPNAstronomicalObject ) or not isinstance( body2, RPNAstronomicalObject ) or \
       not arguments:
        raise ValueError( 'expected two astronomical objects, a location and a date-time' )

    separation = body1.getAngularSeparation( body2, arguments[ 'location' ], arguments[ 'datetime' ] ).value

    radius1 = body1.getAngularSize( ).value
    radius2 = body2.getAngularSize( ).value

    if separation > fadd( radius1, radius2 ):
        return 0

    distance1 = body1.getDistanceFromEarth( arguments[ 'datetime' ] )
    distance2 = body2.getDistanceFromEarth( arguments[ 'datetime' ] )

    area1 = fmul( pi, power( radius1, 2 ) )
    area2 = fmul( pi, power( radius2, 2 ) )

    # pylint: disable=arguments-out-of-order
    areaOfIntersection = fadd( getCircleIntersectionTerm( radius1, radius2, separation ),
                               getCircleIntersectionTerm( radius2, radius1, separation ) )

    if distance1 > distance2:
        result = fdiv( areaOfIntersection, area1 )
    else:
        result = fdiv( areaOfIntersection, area2 )

    if result > 1:
        return 1
    else:
        return result

#function [Az El] = RaDec2AzEl(Ra,Dec,lat,lon,time)
#% Programed by Darin C. Koblick 01/23/2010
#%--------------------------------------------------------------------------
#% External Function Call Sequence:
#% [Az El] = RaDec2AzEl(0,0,0,-104,'1992/08/20 12:14:00')
#%
#% Worked Example: pg. 262 Vallado
#%[Az El] = RaDec2AzEl(294.9891115,-20.8235624,39.007,-104.883,'1994/05/14 13:11:20.59856')
#%[210.7514  23.9036] = RaDec2AzEl(294.9891115,-20.8235624,39.007,-104.883,'1994/05/14 13:11:20.59856')
#%
#% Worked Example: http://www.stargazing.net/kepler/altaz.html
#% [Az El] = RaDec2AzEl(344.95,42.71667,52.5,-1.91667,'1997/03/14 19:00:00')
#% [311.92258 22.40100] = RaDec2AzEl(344.95,42.71667,52.5,-1.91667,'1997/03/14 19:00:00')
#%
#% [Beta,el] = RaDec2AzEl(alpha_t,delta_t,phi,lamda,'yyyy/mm/dd hh:mm:ss')
#%
#% Function Description:
#%--------------------------------------------------------------------------
#% RaDec2AzEl will take the Right Ascension and Declination in the topocentric
#% reference frame, site latitude and longitude as well as a time in GMT
#% and output the Azimuth and Elevation in the local horizon
#% reference frame.
#%
#% Inputs:                                                       Format:
#%--------------------------------------------------------------------------
#% Topocentric Right Ascension (Degrees)                         [N x 1]
#% Topocentric Declination Angle (Degrees)                       [N x 1]
#% Lat (Site Latitude in degrees -90:90 -> S(-) N(+))            [N x 1]
#% Lon (Site Longitude in degrees -180:180 W(-) E(+))            [N x 1]
#% UTC (Coordinated Universal Time YYYY/MM/DD hh:mm:ss)          [N x 1]
#%
#% Outputs:                                                      Format:
#%--------------------------------------------------------------------------
#% Local Azimuth Angle   (degrees)                               [N x 1]
#% Local Elevation Angle (degrees)                               [N x 1]
#%
#%
#% External Source References:
#% Fundamentals of Astrodynamics and Applications
#% D. Vallado, Second Edition
#% Example 3-5. Finding Local Siderial Time (pg. 192)
#% Algorithm 28: AzElToRaDec (pg. 259)
#% -------------------------------------------------------------------------

#%Example 3-5
#[yyyy mm dd HH MM SS] = datevec(datenum(time,'yyyy/mm/dd HH:MM:SS'));
#JD = juliandate(yyyy,mm,dd,HH,MM,SS);
#T_UT1 = (JD-2451545)./36525;
#ThetaGMST = 67310.54841 + (876600*3600 + 8640184.812866).*T_UT1 ...
#+ .093104.*(T_UT1.^2) - (6.2*10^-6).*(T_UT1.^3);
#ThetaGMST = mod((mod(ThetaGMST,86400*(ThetaGMST./abs(ThetaGMST)))/240),360);
#ThetaLST = ThetaGMST + lon;

#%Equation 4-11 (Define Siderial Time LHA)
#LHA = mod(ThetaLST - Ra,360);

#%Equation 4-12 (Elevation Deg)
#El = asind(sind(lat).*sind(Dec)+cosd(lat).*cosd(Dec).*cosd(LHA));

#%Equation 4-13 / 4-14 (Adaptation) (Azimuth Deg)
#%Az = mod(atand(-(sind(LHA).*cosd(Dec)./(cosd(lat).*sind(Dec) - sind(lat).*cosd(Dec).*cosd(LHA)))),360);
#Az = mod(atan2(-sind(LHA).*cosd(Dec)./cosd(El),...
#    (sind(Dec)-sind(El).*sind(lat))./(cosd(El).*cosd(lat))).*(180/pi),360);


#function jd = juliandate(year, month, day, hour, min, sec)
#YearDur = 365.25;
#for i = length(month):-1:1
#    if (month(i)<=2)
#        year(i)=year(i)-1;
#        month(i)=month(i)+12;
#    end
#end
#A = floor(YearDur*(year+4716));
#B = floor(30.6001*(month+1));
#C = 2;
#D = floor(year/100);
#E = floor(floor(year/100)*.25);
#F = day-1524.5;
#G = (hour+(min/60)+sec/3600)/24;
#jd =A+B+C-D+E+F+G;
