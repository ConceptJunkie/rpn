#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnAstronomy.py
# //
# //  RPN command-line calculator astronomical operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from dateutil import tz
import ephem

from mpmath import *

from rpnDateTime import RPNDateTime
from rpnDeclarations import *
from rpnLocation import RPNLocation
from rpnMeasurement import RPNMeasurement

import rpnGlobals as g


# //******************************************************************************
# //
# //  getVernalEquinox
# //
# //  http://rhodesmill.org/pyephem/quick.html
# //
# //******************************************************************************

def getVernalEquinox( n ):
    result = RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getSummerSolstice
# //
# //******************************************************************************

def getSummerSolstice( n ):
    result = RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getAutumnalEquinox( n ):
    result = RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) + '-07-01' ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getWinterSolstice( n ):
    result = RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) + '-07-01' ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getEphemTime
# //
# //******************************************************************************

def getEphemTime( n, func ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'expected a date-time argument' )

    result = RPNDateTime.convertFromEphemDate( func( n.format( ) ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getMoonPhase
# //
# //******************************************************************************

def getMoonPhase( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'moon_phase\' expects a date-time argument' )

    datetime = n.to( 'utc' ).format( )

    previous = RPNDateTime.convertFromEphemDate( ephem.previous_new_moon( datetime ) ).getLocalTime( )
    next = RPNDateTime.convertFromEphemDate( ephem.next_new_moon( datetime ) ).getLocalTime( )

    cycle = next - previous
    current = n - previous

    return current / cycle


# //******************************************************************************
# //
# //  getSkyLocation
# //
# //******************************************************************************

def getSkyLocation( n, k ):
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
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_rising( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextSetting
# //
# //******************************************************************************

def getNextSetting( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_setting( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextTransit
# //
# //******************************************************************************

def getNextTransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_transit( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextAntitransit
# //
# //******************************************************************************

def getNextAntitransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.next_antitransit( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousRising
# //
# //******************************************************************************

def getPreviousRising( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_rising( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousSetting
# //
# //******************************************************************************

def getPreviousSetting( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_setting( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousTransit
# //
# //******************************************************************************

def getPreviousTransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_transit( body ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getPreviousAntitransit
# //
# //******************************************************************************

def getPreviousAntitransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or \
       not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = '0'

    result = RPNDateTime.convertFromEphemDate( location.observer.previous_antitransit( body ) ).getLocalTime( )

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
    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected locaton and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.convertFromEphemDate(
                location.observer.next_rising( ephem.Sun( ), use_center=True ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


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
    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected locaton and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.to( 'utc' ).format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.convertFromEphemDate(
                location.observer.next_setting( ephem.Sun( ), use_center=True ) ).getLocalTime( )

    location.observer.horizon = old_horizon

    return result


