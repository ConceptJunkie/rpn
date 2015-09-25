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

import ephem
from mpmath import *

from rpnDeclarations import *


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
    return [ mpmathify( n.ra ), mpmathify( n.dec ) ]


# //******************************************************************************
# //
# //  getNextRising
# //
# //******************************************************************************

def getNextRising( body, location, date, func ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    observer = ephem.Observer( )
    observer.lat = location.lat
    observer.long = location.long
    observer.date = date.format( )
    return RPNDateTime.convertFromEphemDate( observer.next_rising( body ) )


# //******************************************************************************
# //
# //  getNextSetting
# //
# //******************************************************************************

def getNextSetting( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    observer = ephem.Observer( )
    observer.lat = location.lat
    observer.date = date.format( )
    return RPNDateTime.convertFromEphemDate( observer.next_setting( body ) )


# //******************************************************************************
# //
# //  getNextTransit
# //
# //******************************************************************************

def getNextTransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    observer = ephem.Observer( )
    observer.lat = location.lat
    observer.date = date.format( )
    return RPNDateTime.convertFromEphemDate( observer.next_transit( body ) )


# //******************************************************************************
# //
# //  getNextAntitransit
# //
# //******************************************************************************

def getNextAntitransit( body, location, date ):
    if not isinstance( body, ephem.Body ) or not isinstance( location, RPNLocation ) or not isinstance( date, RPNDateTime ):
        raise ValueError( 'expected an astronomical object, a locaton and a date-time' )

    observer = ephem.Observer( )
    observer.lat = location.lat
    observer.date = date.format( )
    return RPNDateTime.convertFromEphemDate( observer.next_antitransit( body ) )


