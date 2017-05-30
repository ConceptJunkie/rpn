#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnAstronomy.py
# //
# //  RPN command-line calculator astronomical operators
# //  copyright (c) 2017, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import ephem

from mpmath import fdiv, fmul, mpmathify, pi
from pytz import timezone

from rpnDateTime import RPNDateTime
from rpnLocation import getLocation, RPNLocation, getTimeZone
from rpnMeasurement import RPNMeasurement
from rpnMath import subtract
from rpnUtils import oneArgFunctionEvaluator


# //******************************************************************************
# //
# //  getVernalEquinox
# //
# //  http://rhodesmill.org/pyephem/quick.html
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getVernalEquinox( n ):
    '''Returns the date of the next vernal equinox after n.'''
    result = RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getSummerSolstice
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getSummerSolstice( n ):
    '''Returns the date of the next summer solstice after n.'''
    result = RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getAutumnalEquinox( n ):
    '''Returns the date of the next autumnal equinox after n.'''
    result = RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) + '-07-01' ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getWinterSolstice( n ):
    '''Returns the date of the next winter solstice after n.'''
    result = RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) + '-07-01' ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getEphemTime
# //
# //******************************************************************************

def getEphemTime( n, func ):
    '''Returns a pyephem date-time value from an RPNDateTime value.'''
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'expected a date-time argument' )

    result = RPNDateTime.convertFromEphemDate( func( n.format( ) ) )
    return result.getLocalTime( )

@oneArgFunctionEvaluator( )
def getNextFirstQuarterMoon( n ):
    return getEphemTime( n, ephem.next_first_quarter_moon )

@oneArgFunctionEvaluator( )
def getNextFullMoon( n ):
    return getEphemTime( n, ephem.next_full_moon )

@oneArgFunctionEvaluator( )
def getNextLastQuarterMoon( n ):
    return getEphemTime( n, ephem.next_last_quarter_moon )

@oneArgFunctionEvaluator( )
def getNextNewMoon( n ):
    return getEphemTime( n, ephem.next_new_moon )

@oneArgFunctionEvaluator( )
def getPreviousFirstQuarterMoon( n ):
    return getEphemTime( n, ephem.previous_first_quarter_moon )

@oneArgFunctionEvaluator( )
def getPreviousFullMoon( n ):
    return getEphemTime( n, ephem.previous_full_moon )

@oneArgFunctionEvaluator( )
def getPreviousLastQuarterMoon( n ):
    return getEphemTime( n, ephem.previous_last_quarter_moon )

@oneArgFunctionEvaluator( )
def getPreviousNewMoon( n ):
    return getEphemTime( n, ephem.previous_new_moon )


# //******************************************************************************
# //
# //  getMoonPhase
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getMoonPhase( n ):
    '''Returns the current moon phase as a percentage, starting from the new moon.'''
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'moon_phase\' expects a date-time argument' )

    datetime = n.format( )

    previous = RPNDateTime.convertFromEphemDate( ephem.previous_new_moon( datetime ) )
    next = RPNDateTime.convertFromEphemDate( ephem.next_new_moon( datetime ) )

    cycle = next - previous
    current = n - previous

    return current.total_seconds( ) / cycle.total_seconds( )


# //******************************************************************************
# //
# //  getSkyLocation
# //
# //******************************************************************************

def getSkyLocation( n, k ):
    '''Returns the location of an astronomical object in the sky in terms of right ascension and declination.'''
    if not isinstance( n, ephem.Body ) or not isinstance( k, RPNDateTime ):
        raise ValueError( '\'sky_location\' expects an astronomical object and a date-time' )

    n.compute( k.to( 'utc' ).format( ) )

    return [ fdiv( fmul( mpmathify( n.ra ), 180 ), pi ), fdiv( fmul( mpmathify( n.dec ), 180 ), pi ) ]


# //******************************************************************************
# //
# //  getNextRising
# //
# //******************************************************************************

def getNextRising( body, location, date ):
    '''Returns the next rising time for an astronomical object.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_rising( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getNextSunrise( n, k ):
    return getNextRising( ephem.Sun( ), n, k )

def getNextMoonRise( n, k ):
    return getNextRising( ephem.Moon( ), n, k )


# //******************************************************************************
# //
# //  getNextSetting
# //
# //******************************************************************************

def getNextSetting( body, location, date ):
    '''Returns the next setting time for an astronomical object.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_setting( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getNextSunset( n, k ):
    return getNextSetting( ephem.Sun( ), n, k )

def getNextMoonSet( n, k ):
    return getNextSetting( ephem.Moon( ), n, k )


# //******************************************************************************
# //
# //  getNextTransit
# //
# //******************************************************************************

def getNextTransit( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_transit( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getSolarNoon( n, k ):
    return getNextTransit( ephem.Sun( ), n, k )

def getNextMoonTransit( n, k ):
    return getNextTransit( ephem.Moon( ), n, k )


# //******************************************************************************
# //
# //  getNextAntitransit
# //
# //******************************************************************************

def getNextAntitransit( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_antitransit( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getNextSunAntitransit( n, k ):
    return getNextAntitransit( ephem.Sun( ), n, k )

def getNextMoonAntitransit( n, k ):
    return getNextAntitransit( ephem.Moon( ), n, k )


# //******************************************************************************
# //
# //  getTransitTime
# //
# //******************************************************************************

def getTransitTime( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    ephemRising = location.observer.next_rising( body )
    rising = RPNDateTime.convertFromEphemDate( ephemRising ).getLocalTime( )
    setting = RPNDateTime.convertFromEphemDate( location.observer.next_setting( body, start=ephemRising ) ).getLocalTime( )

    return subtract( setting, rising )

def getDayTime( n, k ):
    return getTransitTime( ephem.Sun( ), n, k )


# //******************************************************************************
# //
# //  getAntitransitTime
# //
# //******************************************************************************

def getAntitransitTime( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    ephemSetting = location.observer.next_setting( body )
    setting = RPNDateTime.convertFromEphemDate( ephemSetting ).getLocalTime( )
    rising = RPNDateTime.convertFromEphemDate( location.observer.next_rising( body, start=ephemSetting ) ).getLocalTime( )

    return subtract( rising, setting )

def getNightTime( n, k ):
    return getAntitransitTime( ephem.Sun( ), n, k )


# //******************************************************************************
# //
# //  getPreviousRising
# //
# //******************************************************************************

def getPreviousRising( body, location, date ):
    '''Returns the previous rising time for an astronomical object.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_rising( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousSetting
# //
# //******************************************************************************

def getPreviousSetting( body, location, date ):
    '''Returns the previous setting time for an astronomical object.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_setting( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousTransit
# //
# //******************************************************************************

def getPreviousTransit( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_transit( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousAntitransit
# //
# //******************************************************************************

def getPreviousAntitransit( body, location, date ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_antitransit( body ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextDawn
# //
# //  -6 is "civil" twilight
# //  -12 is nautical twilight
# //  -18 is astronomical twilight
# //
# //******************************************************************************

def getNextDawn( location, date, horizon = -6 ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected location and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.convertFromEphemDate(
                location.observer.next_rising( ephem.Sun( ), use_center=True ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getNextNauticalDawn( n, k ):
    return getNextDawn( n, k, -12 )

def getNextAstronomicalDawn( n, k ):
    return getNextDawn( n, k, -18 )


# //******************************************************************************
# //
# //  getNextDusk
# //
# //  -6 is "civil" twilight
# //  -12 is nautical twilight
# //  -18 is astronomical twilight
# //
# //******************************************************************************

def getNextDusk( location, date, horizon = -6 ):
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected location and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.convertFromEphemDate(
                location.observer.next_setting( ephem.Sun( ), use_center=True ) )
    result = result.getLocalTime( timezone( getTimeZone( location ) ) )

    location.observer.horizon = old_horizon

    return result

def getNextNauticalDusk( n, k ):
    return getNextDusk( n, k, -12 )

def getNextAstronomicalDusk( n, k ):
    return getNextDusk( n, k, -18 )


# //******************************************************************************
# //
# //  getDistanceFromEarth
# //
# //******************************************************************************

def getDistanceFromEarth( n, k ):
    if not isinstance( n, ephem.Body ) or not isinstance( k, RPNDateTime ):
        raise ValueError( '\'sky_location\' expects an astronomical object and a date-time' )

    n.compute( k.to( 'utc' ).format( ) )

    return RPNMeasurement( n.earth_distance * ephem.meters_per_au, 'meters' )

