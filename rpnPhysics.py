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
from rpnMath import divide, exponentiate, getRoot, multiply
from rpnMeasurement import RPNMeasurement, validateUnits
from rpnUtils import real_int

import rpnGlobals as g

from mpmath import fdiv, fsub, inf, pi, power, sqrt


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


# //******************************************************************************
# //
# //  getEscapeVelocity
# //
# //******************************************************************************

def getEscapeVelocity( mass, radius ):
    validateUnits( mass, 'mass' )
    validateUnits( radius, 'length' )

    return getRoot( getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( radius ), 2 )


# //******************************************************************************
# //
# //  getOrbitalVelocity
# //
# //******************************************************************************

def getOrbitalVelocity( mass, radius ):
    validateUnits( mass, 'mass' )
    validateUnits( radius, 'length' )

    return getRoot( getProduct( [ getNewtonsConstant( ), mass ] ).divide( radius ), 2 )


# //******************************************************************************
# //
# //  getOrbitalPeriod
# //
# //******************************************************************************

def getOrbitalPeriod( mass, radius ):
    validateUnits( mass, 'mass' )
    validateUnits( radius, 'length' )

    return divide( getProduct( [ 2, pi, radius ] ), getOrbitalVelocity( mass, radius ) )

