#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPhysics.py
# //
# //  RPN command-line calculator physics operators
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import struct

from rpnConstants import getNewtonsConstant, getSpeedOfLight
from rpnGenerator import RPNGenerator
from rpnList import getProduct
from rpnMath import divide, exponentiate
from rpnMeasurement import RPNMeasurement, validateUnits
from rpnUtils import real_int

import rpnGlobals as g

from mpmath import fdiv, fsub, inf, power, sqrt


# //******************************************************************************
# //
# //  getSchwarzchildRadius
# //
# //******************************************************************************

def getSchwarzchildRadius( mass ):
    validateUnits( mass, 'mass' )

    return getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( exponentiate( getSpeedOfLight( ), 2 ) )


# //******************************************************************************
# //
# //  getTimeDilation
# //
# //******************************************************************************

def getTimeDilation( velocity ):
    validateUnits( velocity, 'velocity' )

    c_ratio = divide( velocity, getSpeedOfLight( ) ).value

    if c_ratio == 1:
        return inf

    return fdiv( 1, sqrt( fsub( 1, power( c_ratio, 2 ) ) ) )

