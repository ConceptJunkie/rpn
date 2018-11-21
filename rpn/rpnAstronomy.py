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
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         loadAstronomyData, real_int

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getSeason
# //
# //  0 = spring, 1 = summer, 2 = autumn, 3 = winter
# //
# //******************************************************************************

def getSeason( n, season ):
    '''Returns the date of the season for year n.'''
    from skyfield import almanac
    loadAstronomyData( )

    t, y = almanac.find_discrete( g.timescale.utc( real_int( n ), 1, 1 ),
                                  g.timescale.utc( n, 12, 31 ), almanac.seasons( g.ephemeris ) )
    result = RPNDateTime.parseDateTime( t[ season ].utc_datetime( ) )
    return result.getLocalTime( )


# //******************************************************************************
# //
# //  getVernalEquinox
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getVernalEquinox( n ):
    '''Returns the date of the vernal equinox for year n.'''
    return getSeason( n, 0 )



# //*****************************************************************************
# //
# //  getSummerSolstice
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getSummerSolstice( n ):
    '''Returns the date of the summer solstice for year n.'''
    return getSeason( n, 1 )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getAutumnalEquinox( n ):
    '''Returns the date of the autumnal equinox for year n.'''
    return getSeason( n, 2 )


# //*****************************************************************************
# //
# //  getWinterSolstice
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getWinterSolstice( n ):
    '''Returns the date of the winter solstice for year n.'''
    return getSeason( n, 3 )


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
