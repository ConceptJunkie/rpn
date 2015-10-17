#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnLocation.py
# //
# //  RPN command-line calculator RPNLocationn class declaration
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import contextlib
import pickle
import ephem
import os

from mpmath import *

from rpnMeasurement import RPNMeasurement

import rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNLocation
# //
# //  This class represents a location on the surface of the Earth.
# //
# //  The observer class measures lat/long in radians, but no one else does,
# //  so the methods assume degrees.
# //
# //******************************************************************************

class RPNLocation( object ):
    def __init__( self, name, observer ):
        self.name = name
        self.observer = observer

    def getLat( self ):
        return fdiv( fmul( mpmathify( float( self.observer.lat ) ), 180 ), pi )

    def getLong( self ):
        return fdiv( fmul( mpmathify( float( self.observer.long ) ), 180 ), pi )

    def getDate( self ):
        return self.observer.date

    def getEpoch( self ):
        return self.observer.epoch

    def getElevation( self ):
        return self.observer.elevation

    def getTemp( self ):
        return self.observer.temp

    def getPressure( self ):
        return self.observer.pressure

    def setLat( self, value ):
        self.observer.lat = fmul( fdiv( value, 180 ), pi )

    def setLong( self, value ):
        self.observer.long = fmul( fdiv( value, 180 ), pi )

    def setDate( self, value ):
        self.observer.date = value

    def setEpoch( self, value ):
        self.observer.epoch = value

    def setElevation( self, value ):
        self.observer.elevation = value

    def setTemp( self, value ):
        self.observer.temp = value

    def setPressure( self, value ):
        self.observer.pressure = value


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
    from rpnUtils import DelayedKeyboardInterrupt

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

    if name in g.locationCache:
        locationInfo = g.locationCache[ name ]

        observer = ephem.Observer( )
        result = RPNLocation( name, observer )

        result.setLat( locationInfo[ 1 ] )
        result.setLong( locationInfo[ 2 ] )

        #print( 'looked up', result.name )
        #print( 'lat/long', result.getLat( ), result.getLong( ) )
        return result

    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim( )
        location = geolocator.geocode( name )

        if location is None:
            raise ValueError( 'location lookup failed, try a different search term' )

        observer = ephem.Observer( )
        result = RPNLocation( name, observer )

        result.setLat( location.latitude )
        result.setLong( location.longitude )
    except ValueError:
        raise ValueError( 'location lookup failed' )

    result = RPNLocation( name, observer )

    g.locationCache[ name ] = [ name, result.getLat( ), result.getLong( ) ]
    saveLocationCache( g.locationCache )

    return result


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


# //******************************************************************************
# //
# //  getDistance
# //
# //******************************************************************************

def getDistance( location1, location2 ):
    if not isinstance( location1, RPNLocation ) or not isinstance( location2, RPNLocation ):
        raise ValueError( 'expected an two locations as arguments' )

    from geopy.distance import vincenty

    distance = vincenty( ( location1.getLat( ), location1.getLong( ) ),
                         ( location2.getLat( ), location2.getLong( ) ) ).miles

    return RPNMeasurement( distance, [ { 'mile' : 1 } ] )
