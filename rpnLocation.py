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

import ephem

from mpmath import *

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

    def setLat( self, value ):
        self.observer.lat = fmul( fdiv( value, 180 ), pi )

    def setLong( self, value ):
        self.observer.long = fmul( fdiv( value, 180 ), pi )

