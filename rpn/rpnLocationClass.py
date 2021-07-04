#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocationClass.py
#
#  rpnChilada location class declaration
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import ephem

from mpmath import fdiv, fmul, mpmathify, pi
from skyfield.api import Topos


#******************************************************************************
#
#  class RPNLocation
#
#  The observer class measures lat/long in radians, but no one else does,
#  so the methods assume degrees.
#
#******************************************************************************

class RPNLocation( ):
    '''This class represents a location on the surface of the Earth.'''
    observer = None
    name = None
    
    def __init__( self, *_, **kwargs ):
        self.name = kwargs.get( 'name', None )
        observer = kwargs.get( 'observer', None )
        lat = kwargs.get( 'lat', None )
        long = kwargs.get( 'long', None )

        if observer:
            self.observer = observer
        else:
            self.observer = ephem.Observer( )

        if lat:
            self.setLat( lat )

        if long:
            self.setLong( long )

    def setObserver( self, observer ):
        self.name = ''
        self.observer.lat = observer.lat
        self.observer.long = observer.long
        self.observer.epoch = observer.epoch
        self.observer.date = observer.date
        self.observer.elevation = observer.elevation
        self.observer.temp = observer.temp
        self.observer.pressure = observer.pressure

    def getName( self ):
        return self.name

    # latitude in degrees
    def getLat( self ):
        return fdiv( fmul( mpmathify( float( self.observer.lat ) ), 180 ), pi )

    # longitude in degrees
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

    def setName( self, value ):
        self.name = value

    # set latitude in degrees
    def setLat( self, value ):
        self.observer.lat = fmul( fdiv( value, 180 ), pi )

    # set longitude in degrees
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

    def getTopos( self ):
        return Topos( latitude_degrees=float( self.getLat( ) ),
                      longitude_degrees=float( self.getLong( ) ),
                      elevation_m=self.getElevation( ) )
