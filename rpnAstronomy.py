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
    return n


# //******************************************************************************
# //
# //  getNextFullMoon
# //
# //******************************************************************************

def getNextFullMoon( n ):
    return n


# //******************************************************************************
# //
# //  getNextLastQuarterMoon
# //
# //******************************************************************************

def getNextLastQuarterMoon( n ):
    return n


# //******************************************************************************
# //
# //  getNextNewMoon
# //
# //******************************************************************************

def getNextNewMoon( n ):
    return n


# //******************************************************************************
# //
# //  getPreviousFirstQuarterMoon
# //
# //******************************************************************************

def getPreviousFirstQuarterMoon( n ):
    return n


# //******************************************************************************
# //
# //  getPreviousFullMoon
# //
# //******************************************************************************

def getPreviousFullMoon( n ):
    return n


# //******************************************************************************
# //
# //  getPreviousLastQuarterMoon
# //
# //******************************************************************************

def getPreviousLastQuarterMoon( n ):
    return n


# //******************************************************************************
# //
# //  getPreviousNewMoon
# //
# //******************************************************************************

def getPreviousNewMoon( n ):
    return n


