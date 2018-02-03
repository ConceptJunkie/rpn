#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnAstronomy.py
# //
# //  RPN command-line calculator astronomical operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import ephem

from mpmath import acos, fabs, fadd, fdiv, fmul, fsub, mpmathify, pi, power, sqrt
from pytz import timezone

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnLocation import getLocation, RPNLocation, getTimeZone
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnMath import subtract
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator


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


# //*****************************************************************************
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

def getSkyLocation( body, location, date ):
    '''Returns the location of an astronomical object in the sky in terms of azimuth and altitude.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )

    body.compute( location.observer )

    return [ RPNMeasurement( fdiv( fmul( mpmathify( body.az ), 180 ), pi ), 'degree' ),
             RPNMeasurement( fdiv( fmul( mpmathify( body.alt ), 180 ), pi ), 'degree' ) ]


# //******************************************************************************
# //
# //  getAngularSize
# //
# //******************************************************************************

def getAngularSize( body, location, date ):
    '''Returns the angular size of an astronomical object in radians.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )

    body.compute( location.observer )

    # I have no idea why size seems to return the value in arcseconds... that
    # goes against the pyephem documentation that it always uses radians for angles.
    return RPNMeasurement( fdiv( fmul( fdiv( body.size, 3600 ), pi ), 180 ), 'radian' )


# //******************************************************************************
# //
# //  getAngularSeparation
# //
# //******************************************************************************

def getAngularSeparation( body1, body2, location, date ):
    '''Returns the angular size of an astronomical object in radians.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body1, ephem.Body ) or not isinstance( body2, ephem.Body ) and \
       not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected two astronomical objects, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )

    body1.compute( location.observer )
    body2.compute( location.observer )

    separation = float( ephem.separation( ( body1.az, body1.alt ), ( body2.az, body2.alt ) ) )

    return RPNMeasurement( separation, 'radian' )


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

@twoArgFunctionEvaluator( )
def getNextSunrise( n, k ):
    return getNextRising( ephem.Sun( ), n, k )

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def getNextSunset( n, k ):
    return getNextSetting( ephem.Sun( ), n, k )

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def getSolarNoon( n, k ):
    return getNextTransit( ephem.Sun( ), n, k )

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def getNextSunAntitransit( n, k ):
    return getNextAntitransit( ephem.Sun( ), n, k )

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def getNextCivilDawn( n, k ):
    return getNextDawn( n, k, -6 )

@twoArgFunctionEvaluator( )
def getNextNauticalDawn( n, k ):
    return getNextDawn( n, k, -12 )

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def getNextCivilDusk( n, k ):
    return getNextDusk( n, k, -6 )

@twoArgFunctionEvaluator( )
def getNextNauticalDusk( n, k ):
    return getNextDusk( n, k, -12 )

@twoArgFunctionEvaluator( )
def getNextAstronomicalDusk( n, k ):
    return getNextDusk( n, k, -18 )


# //******************************************************************************
# //
# //  getDistanceFromEarth
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getDistanceFromEarth( n, k ):
    if not isinstance( n, ephem.Body ) or not isinstance( k, RPNDateTime ):
        raise ValueError( '\'sky_location\' expects an astronomical object and a date-time' )

    n.compute( k.to( 'utc' ).format( ) )

    return RPNMeasurement( n.earth_distance * ephem.meters_per_au, 'meters' )


# //******************************************************************************
# //
# //  getCircleIntersectionTerm
# //
# //  http://mathworld.wolfram.com/Circle-CircleIntersection.html
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getEclipseTotality
# //
# //******************************************************************************

def getEclipseTotality( body1, body2, location, date ):
    '''Returns the angular size of an astronomical object in radians.'''
    if isinstance( location, str ):
        location = getLocation( location )

    if not isinstance( body1, ephem.Body ) or not isinstance( body2, ephem.Body ) and \
       not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected two astronomical objects, a location and a date-time' )

    location.observer.date = date.to( 'utc' ).format( )

    body1.compute( location.observer )
    body2.compute( location.observer )

    separation = mpmathify( ephem.separation( ( body1.az, body1.alt ), ( body2.az, body2.alt ) ) )

    radius1 = fdiv( fdiv( fmul( fdiv( body1.size, 3600 ), pi ), 180 ), 2 )
    radius2 = fdiv( fdiv( fmul( fdiv( body2.size, 3600 ), pi ), 180 ), 2 )

    if separation > fadd( radius1, radius2 ):
        return 0

    distance1 = body1.earth_distance
    distance2 = body2.earth_distance

    area1 = fmul( pi, power( radius1, 2 ) )
    area2 = fmul( pi, power( radius2, 2 ) )

    area_of_intersection = fadd( getCircleIntersectionTerm( radius1, radius2, separation ),
                                 getCircleIntersectionTerm( radius2, radius1, separation ) )

    if distance1 > distance2:
        result = fdiv( area_of_intersection, area1 )
    else:
        result = fdiv( area_of_intersection, area2 )

    if result > 1:
        return 1
    else:
        return result

