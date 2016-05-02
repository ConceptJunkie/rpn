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
from rpnMeasurement import checkUnits, getWhichUnitType, RPNMeasurement, validateUnits
from rpnUtils import real_int

import rpnGlobals as g

from mpmath import fdiv, fmul, fsub, inf, pi, power, sqrt


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
# //  getOrbitalMass
# //
# //******************************************************************************

def getOrbitalMass( measurement1, measurement2 ):
    """
    To solve for the planetary mass for an object in a circular orbit, we need
    Newton's gravitational constant and two of the following three items:

    G = Newton's gravitational constant

    T = orbital period
    v = orbital velocity
    r = orbit radius (the distance from the center of mass)

    ---- mass in terms of period and velocity
    m =

    ---- mass in terms of period and radius
    m = 4*pi^2*r3/G*T^2

    ---- mass in terms of velocity and radius
    m = v^2*r/G
    """
    unitTypes = [ 'time', 'length', 'velocity' ]

    unitType1 = getWhichUnitType( measurement1, unitTypes )

    if not unitType1:
        raise ValueError( '\'orbital_period\' expects arguments for two of the following: ', ', '.join( unitTypes ) )

    unitTypes.remove( unitType1 )

    unitType2 = getWhichUnitType( measurement2, unitTypes )

    if not unitType2:
        raise ValueError( '\'orbital_period\' expects the second argument to be one of the following: ', ', '.join( unitTypes ) )

    if unitType1 == 'time':
        period = measurement1

        if unitType2 == 'length':
            bRadius = True
            radius = measurement2
        else:
            bRadius = False
            velocity = measurement2
    elif unitType2 == 'time':
        mass = measurement2

        if unitType1 == 'length':
            bRadius = True
            radius = measurement1
        else:
            bRadius = False
            velocity = measurement1
    else:
        if unitType1 == 'length':
            radius, velocity = measurement1, measurement2
        else:
            radius, velocity = measurement2, measurement1

        return divide( getProduct( [ velocity, velocity, radius ] ), getNewtonsConstant( ) )

    if bRadius:
        return divide( getProduct( [ 4, pi, pi, radius, radius, radius ] ),
                       getProduct( [ getNewtonsConstant( ), period, period ] ) )
    else:
        return RPNMeasurement( 1, [ 'kilogram' ] )  # velocity and period


# //******************************************************************************
# //
# //  getOrbitalPeriod
# //
# //******************************************************************************

def getOrbitalPeriod( measurement1, measurement2 ):
    """
    To solve the period of a circular orbit, we need Newton's gravitational
    constant and two of the following three items:

    G = Newton's gravitational constant

    m = planetary mass (i.e., mass of the thing being orbited)
    r = orbit radius (the distance from the center of mass)
    v = orbital velocity

    ---- period in terms of radius and mass
    T = 2*pi*sqrt( r^3/G*m )

    ---- period in terms of radius and velocity
    T = 2*pi*r/v

    ---- period in terms of mass and velocity
    T =
    """
    unitTypes = [ 'mass', 'length', 'velocity' ]

    unitType1 = getWhichUnitType( measurement1, unitTypes )

    if not unitType1:
        raise ValueError( '\'orbital_period\' expects arguments for two of the following: ', ', '.join( unitTypes ) )

    unitTypes.remove( unitType1 )

    unitType2 = getWhichUnitType( measurement2, unitTypes )

    if not unitType2:
        raise ValueError( '\'orbital_period\' expects the second argument to be one of the following: ', ', '.join( unitTypes ) )

    if unitType1 == 'mass':
        mass = measurement1

        if unitType2 == 'length':
            bRadius = True
            radius = measurement2
        else:
            bRadius = False
            velocity = measurement2
    elif unitType2 == 'mass':
        mass = measurement2

        if unitType1 == 'length':
            bRadius = True
            radius = measurement1
        else:
            bRadius = False
            velocity = measurement1
    else:
        if unitType1 == 'length':
            radius, velocity = measurement1, measurement2
        else:
            radius, velocity = measurement2, measurement1

        return divide( getProduct( [ 2, pi, radius ] ), velocity )

    if bRadius:
        term = divide( exponentiate( radius, 3 ), multiply( getNewtonsConstant( ), mass ) )
        return getProduct( [ 2, pi, getRoot( term, 2 ) ] )
    else:
        return RPNMeasurement( 1, [ 'second ' ] )  # velocity and mass


# //******************************************************************************
# //
# //  getOrbitalRadius
# //
# //******************************************************************************

def getOrbitalRadius( measurement1, measurement2 ):
    """
    To solve the radius of a circular orbit, we need Newton's gravitational
    constant and two of the following three items:

    G = Newton's gravitational constant

    m = planetary mass (i.e., mass of the thing being orbited)
    T = orbital period
    v = orbital velocity

    ---- radius in terms of period and mass
    r = cbrt( T^2*G*m/4*pi^2 )

    ---- radius in terms of velocity and mass
    r = G*m/v^2

    ---- radius in terms of velocity and period
    r = v*T/2*pi
    """
    unitTypes = [ 'mass', 'time', 'velocity' ]

    unitType1 = getWhichUnitType( measurement1, unitTypes )

    if not unitType1:
        raise ValueError( '\'orbital_radius\' expects arguments for two of the following: ', ', '.join( unitTypes ) )

    unitTypes.remove( unitType1 )

    unitType2 = getWhichUnitType( measurement2, unitTypes )

    if not unitType2:
        raise ValueError( '\'orbital_radius\' expects the second argument to be one of the following: ', ', '.join( unitTypes ) )

    if unitType1 == 'mass':
        mass = measurement1

        if unitType2 == 'time':
            bPeriod = True
            period = measurement2
        else:
            bPeriod = False
            period = measurement2
    elif unitType2 == 'mass':
        mass = measurement2

        if unitType1 == 'time':
            bPeriod = True
            period = measurement1
        else:
            bPeriod = False
            velocity = measurement1
    else:
        if unitType1 == 'time':
            period, velocity = measurement1, measurement2
        else:
            period, velocity = measurement2, measurement1

        return divide( multiply( velocity, period ), fmul( 2, pi ) )

    if bPeriod:
        term = divide( getProduct( [ exponentiate( period, 2 ), getNewtonsConstant( ), mass ] ),
                       fmul( 4, power( pi, 2 ) ) )
        return getRoot( term, 3 )
    else:
        return divide( multiply( getNewtonsConstant( ), mass ), exponentiate( velocity, 2 ) )


# //******************************************************************************
# //
# //  getOrbitalVelocity
# //
# //******************************************************************************

def getOrbitalVelocity( measurement1, measurement2 ):
    """
    To solve the velocity of a circular orbit, we need Newton's gravitational
    constant and two of the following three items:

    G = Newton's gravitational constant

    m = planetary mass (i.e., mass of the thing being orbited)
    r = orbit radius (the distance from the center of mass)
    T = orbital period

    ---- velocity in terms of mass and radius
    v = sqrt( G*m/r )

    ---- velocity in terms of radius and period
    v = 2*pi*r/T

    ---- velocity in terms of mass and period
    v = ( 2*pi*cbrt( T^2*G*m/4*pi^2 ) ) / T
    """
    unitTypes = [ 'mass', 'length', 'time' ]

    unitType1 = getWhichUnitType( measurement1, unitTypes )

    if not unitType1:
        raise ValueError( '\'orbital_velocity\' expects arguments for two of the following: ', ', '.join( unitTypes ) )

    unitTypes.remove( unitType1 )

    unitType2 = getWhichUnitType( measurement2, unitTypes )

    if not unitType2:
        raise ValueError( '\'orbital_velocity\' expects the second argument to be one of the following: ', ', '.join( unitTypes ) )

    if unitType1 == 'mass':
        mass = measurement1

        if unitType2 == 'length':
            bRadius = True
            radius = measurement2
        else:
            bRadius = False
            period = measurement2
    elif unitType2 == 'mass':
        mass = measurement2

        if unitType1 == 'length':
            bRadius = True
            radius = measurement1
        else:
            bRadius = False
            period = measurement1
    else:
        if unitType1 == 'length':
            radius, period = measurement1, measurement2
        else:
            radius, period = measurement2, measurement1

        return divide( getProduct( [ 2, pi, radius ] ), period )

    if bRadius:
        return getRoot( divide( multiply( getNewtonsConstant( ), mass ), radius ), 2 )
    else:
        term = divide( getProduct( [ period, period, getNewtonsConstant( ), mass ] ),
                       getProduct( [ 4, pi, pi ] ) )

        return divide( getProduct( [ 2, pi, getRoot( term, 3 ) ] ), period )

