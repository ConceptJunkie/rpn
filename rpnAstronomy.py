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

import bz2
import contextlib
import ephem
import os
import pickle

from mpmath import *

from ephem import cities
from rpnDeclarations import *
from rpnUtils import DelayedKeyboardInterrupt

import rpnGlobals as g


# //******************************************************************************
# //
# //  getVernalEquinox
# //
# //  http://rhodesmill.org/pyephem/quick.html
# //
# //******************************************************************************

def getVernalEquinox( n ):
    return RPNDateTime.parseDateTime( ephem.next_equinox( str( n ) ) )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getAutumnalEquinox( n ):
    return RPNDateTime.parseDateTime( ephem.next_equinox( str( n ) + '-07-01' ) )


# //******************************************************************************
# //
# //  getSummerSolstice
# //
# //******************************************************************************

def getSummerSolstice( n ):
    return RPNDateTime.parseDateTime( ephem.next_solstice( str( n ) ) )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getWinterSolstice( n ):
    return RPNDateTime.parseDateTime( ephem.next_solstice( str( n ) + '-07-01' ) )


# //******************************************************************************
# //
# //  getEphemTime
# //
# //******************************************************************************

def getEphemTime( n, func ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'expected a date-time argument' )

    return RPNDateTime.parseDateTime( ephem.localtime( func( n.format( ) ) ) )


# //******************************************************************************
# //
# //  getMoonPhase
# //
# //******************************************************************************

def getMoonPhase( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'moon_phase\' expects a date-time argument' )

    previous = RPNDateTime.parseDateTime( ephem.localtime( ephem.previous_new_moon( n.format( ) ) ) )
    next = RPNDateTime.parseDateTime( ephem.localtime( ephem.next_new_moon( n.format( ) ) ) )

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

    n.compute( k.format( ) )

    return [ fdiv( fmul( mpmathify( n.ra ), 180 ), pi ), fdiv( fmul( mpmathify( n.dec ), 180 ), pi ) ]


# //******************************************************************************
# //
# //  getNextRising
# //
# //******************************************************************************

def getNextRising( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    #old_horizon = location.observer.horizon

    location.observer.date = date.format( )
    #location.observer.horizon = '-0.34'     # per U.S. Naval Astronomical Almanac

    result = RPNDateTime.parseDateTime( ephem.localtime( location.observer.next_rising( body ) ) )

    #location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextSetting
# //
# //******************************************************************************

def getNextSetting( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    #old_horizon = location.observer.horizon

    location.observer.date = date.format( )
    #location.observer.horizon = '-0.34'     # per U.S. Naval Astronomical Almanac

    result = RPNDateTime.parseDateTime( ephem.localtime( location.observer.next_setting( body ) ) )

    #location.observer.horizon = old_horizon

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

    #old_horizon = location.observer.horizon

    location.observer.date = date.format( )
    #location.observer.horizon = '-0.34'     # per U.S. Naval Astronomical Almanac

    result = RPNDateTime.parseDateTime( ephem.localtime( location.observer.next_transit( body ) ) )

    #location.observer.horizon = old_horizon

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

    location.observer.date = date.format( )
    location.observer.horizon = '-0.34'     # per U.S. Naval Astronomical Almanac

    result = RPNDateTime.parseDateTime( ephem.localtime( location.observer.next_antitransit( body ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextDawn
# //
# //******************************************************************************

def getNextDawn( location, date, horizon = -6 ):
    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected locaton and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.parseDateTime(
                ephem.localtime( location.observer.next_rising( ephem.Sun( ) ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  getNextDusk
# //
# //******************************************************************************

def getNextDusk( location, date, horizon = -6 ):
    if not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected locaton and date-time arguments' )

    old_horizon = location.observer.horizon

    location.observer.date = date.format( )
    location.observer.horizon = str( horizon )

    result = RPNDateTime.parseDateTime(
                ephem.localtime( location.observer.next_setting( ephem.Sun( ) ) ) )

    location.observer.horizon = old_horizon

    return result


# //******************************************************************************
# //
# //  loadLocationCache
# //
# //******************************************************************************

def loadLocationCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'locations.pckl.bz2', 'rb' ) ) as pickleFile:
            locationCache = pickle.load( pickleFile )
    except FileNotFoundError:
        locationCache = { }

    return locationCache


# //******************************************************************************
# //
# //  saveLocationCache
# //
# //******************************************************************************

def saveLocationCache( locationCache ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'locations.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( locationCache, pickleFile )


# //******************************************************************************
# //
# //  getLocation
# //
# //******************************************************************************

def getLocation( name ):
    if not isinstance( name, str ):
        raise ValueError( '\'location\' expects a string argument' )

    if g.locationCache == None:
        g.locationCache = loadLocationCache( )

    #if name in g.locationCache:
    #    print( 'looked up', g.locationCache[ name ].name )
    #    print( 'lat/long', fdiv( fmul( mpmathify( g.locationCache[ name ].observer.lat ), 180 ), pi ),
    #         fdiv( fmul( mpmathify( g.locationCache[ name ].observer.long ), 180 ), pi ) )
    #    return g.locationCache[ name ]

    try:
        observer = cities.lookup( name )
    except ValueError:
        raise ValueError( 'location cannot be found, please try different terms' )

    g.locationCache[ name ] = RPNLocation( name, observer )
    saveLocationCache( g.locationCache )

    #print( 'lat/long', fdiv( fmul( mpmathify( g.locationCache[ name ].observer.lat ), 180 ), pi ),
    #    fdiv( fmul( mpmathify( g.locationCache[ name ].observer.long ), 180 ), pi ) )

    return g.locationCache[ name ]


# //******************************************************************************
# //
# //  getLocationInfo
# //
# //******************************************************************************

def getLocationInfo( location ):
    if isinstance( location, str ):
        location = getLocation( location )
    elif not isinstance( location. RPNLocation ):
        raise ValueError( 'location name or location object expected' )

    return [ fdiv( fmul( mpmathify( location.observer.lat ), 180 ), pi ),
             fdiv( fmul( mpmathify( location.observer.long ), 180 ), pi ) ]

