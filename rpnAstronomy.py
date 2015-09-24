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
    return RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) ) )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getAutumnalEquinox( n ):
    return RPNDateTime.convertFromEphemDate( ephem.next_equinox( str( n ) + '-07-01' ) )


# //******************************************************************************
# //
# //  getSummerSolstice
# //
# //******************************************************************************

def getSummerSolstice( n ):
    return RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) ) )


# //******************************************************************************
# //
# //  getAutumnalEquinox
# //
# //******************************************************************************

def getWinterSolstice( n ):
    return RPNDateTime.convertFromEphemDate( ephem.next_solstice( str( n ) + '-07-01' ) )


# //******************************************************************************
# //
# //  getNextFirstQuarterMoon
# //
# //******************************************************************************

def getNextFirstQuarterMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'next_first_quarter_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.next_first_quarter_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getNextFullMoon
# //
# //******************************************************************************

def getNextFullMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'next_full_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.next_full_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getNextLastQuarterMoon
# //
# //******************************************************************************

def getNextLastQuarterMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'next_last_quarter_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.next_last_quarter_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getNextNewMoon
# //
# //******************************************************************************

def getNextNewMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'next_new_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.next_new_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getPreviousFirstQuarterMoon
# //
# //******************************************************************************

def getPreviousFirstQuarterMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'previous_first_quarter_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.previous_first_quarter_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getPreviousFullMoon
# //
# //******************************************************************************

def getPreviousFullMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'previous_full_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.previous_full_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getPreviousLastQuarterMoon
# //
# //******************************************************************************

def getPreviousLastQuarterMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'previous_last_quarter_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.previous_last_quarter_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getPreviousNewMoon
# //
# //******************************************************************************

def getPreviousNewMoon( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'previous_new_moon\' expects a date-time argument' )

    return RPNDateTime.convertFromEphemDate( ephem.previous_new_moon( n.format( ) ) )


# //******************************************************************************
# //
# //  getMoonPhase
# //
# //******************************************************************************

def getMoonPhase( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( '\'moon_phase\' expects a date-time argument' )

    previous = RPNDateTime.convertFromEphemDate( ephem.previous_new_moon( n.format( ) ) )
    next = RPNDateTime.convertFromEphemDate( ephem.next_new_moon( n.format( ) ) )

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
        raise ValueError( '\'sky_location\' expects an astronomical object argument and a date-time argument' )

    n.compute( k.format( ) )
    return [ mpmathify( n.ra ), mpmathify( n.dec ) ]

