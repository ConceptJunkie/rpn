#!/usr/bin/env python

#******************************************************************************
#
#  rpnLocationLookup.py
#
#  rpnChilada location look-up functionality
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import bz2
import contextlib
import os
import pickle

import pendulum
import timezonefinder

from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim

from rpn.util.rpnKeyboard import DelayedKeyboardInterrupt

from rpn.rpnVersion import RPN_PROGRAM_NAME

import rpn.util.rpnGlobals as g

from rpn.util.rpnUtils import getUserDataPath


#******************************************************************************
#
#  loadLocationCache
#
#******************************************************************************

def loadLocationCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep +
                                              'locations.pckl.bz2', 'rb' ) ) as pickleFile:
            locationCache = pickle.load( pickleFile )
    except FileNotFoundError:
        locationCache = { }

    return locationCache


#******************************************************************************
#
#  saveLocationCache
#
#******************************************************************************

def saveLocationCache( locationCache ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep +
                                              'locations.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( locationCache, pickleFile )


#******************************************************************************
#
#  lookUpLocation
#
#******************************************************************************

def lookUpLocation( name ):
    if g.locationCache is None:
        g.locationCache = loadLocationCache( )

    if name in g.locationCache:
        locationInfo = g.locationCache[ name ]
        return locationInfo[ 1 ], locationInfo[ 2 ]

    geolocator = Nominatim( user_agent=RPN_PROGRAM_NAME )

    location = None

    for attempts in range( 3 ):
        try:
            location = geolocator.geocode( name )
            break
        except GeocoderUnavailable as e:
            if attempts == 2:
                raise ValueError( 'location lookup connection failure, check network connectivity' ) from e

    if location is None:
        raise ValueError( 'location lookup failed, try a different search term' )

    return location.latitude, location.longitude


#******************************************************************************
#
#  lookUpTimeZone
#
#******************************************************************************

def lookUpTimeZone( lat, long ):
    if g.timeZoneFinder is None:
        g.timeZoneFinder = timezonefinder.TimezoneFinder( )

    tzName = g.timeZoneFinder.timezone_at( lat=lat, lng=long )
    return pendulum.timezone( tzName )
