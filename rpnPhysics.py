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
from rpnMath import divide, getPower, getRoot, multiply, performTrigOperation
from rpnMeasurement import checkUnits, getWhichUnitType, matchUnitTypes, \
                           RPNMeasurement, validateUnits
from rpnUtils import real_int

import rpnGlobals as g

from mpmath import fdiv, fmul, fsub, inf, pi, power, sin, sqrt


# //******************************************************************************
# //
# //  calculateSchwarzchildRadius
# //
# //******************************************************************************

def calculateSchwarzchildRadius( mass ):
    validateUnits( mass, 'mass' )

    radius = getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( getPower( getSpeedOfLight( ), 2 ) )
    return radius.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateTimeDilation
# //
# //******************************************************************************

def calculateTimeDilation( velocity ):
    validateUnits( velocity, 'velocity' )

    c_ratio = divide( velocity, getSpeedOfLight( ) ).value

    if c_ratio == 1:
        return inf

    return fdiv( 1, sqrt( fsub( 1, power( c_ratio, 2 ) ) ) )


# //******************************************************************************
# //
# //  calculateEscapeVelocity
# //
# //******************************************************************************

def calculateEscapeVelocity( mass, radius ):
    validateUnits( mass, 'mass' )
    validateUnits( radius, 'length' )

    velocity = getRoot( getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( radius ), 2 )
    return velocity.convert( 'meter/second' )


# //******************************************************************************
# //
# //  calculateOrbitalMass
# //
# //******************************************************************************

def calculateOrbitalMass( measurement1, measurement2 ):
    """
    To solve for the planetary mass for an object in a circular orbit, we need
    Newton's gravitational constant and two of the following three items:

    G = Newton's gravitational constant

    T = orbital period
    v = orbital velocity
    r = orbit radius (the distance from the center of mass)

    ---- mass in terms of period and velocity
    m = v^3*T/2*pi*G

    ---- mass in terms of period and radius
    m = 4*pi^2*r3/G*T^2

    ---- mass in terms of velocity and radius
    m = v^2*r/G
    """
    validUnitTypes = [
        [ 'time', 'length' ],
        [ 'velocity', 'length' ],
        [ 'time', 'velocity' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'orbital_mass\' requires specific measurement types (see help)' )

    if 'time' in arguments:
        period = arguments[ 'time' ]

        if 'length' in arguments:
            bRadius = True
            radius = arguments[ 'length' ]
        else:
            bRadius = False
            velocity = arguments[ 'velocity' ]
    else:
        # velocity and radius
        radius = arguments[ 'length' ]
        velocity = arguments[ 'velocity' ]
        mass = divide( getProduct( [ velocity, velocity, radius ] ), getNewtonsConstant( ) )
        return mass.convert( 'kilogram' )

    if bRadius:
        # radius and period
        mass = divide( getProduct( [ 4, pi, pi, radius, radius, radius ] ),
                       getProduct( [ getNewtonsConstant( ), period, period ] ) )
    else:
        # velocity and period
        mass = divide( getProduct( [ velocity, velocity, velocity, period ] ),
                       getProduct( [ 2, pi, getNewtonsConstant( ) ] ) )

    return mass.convert( 'kilogram' )


# //******************************************************************************
# //
# //  calculateOrbitalPeriod
# //
# //******************************************************************************

def calculateOrbitalPeriod( measurement1, measurement2 ):
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
    T = 2*pi*G*m/v^3
    """
    validUnitTypes = [
        [ 'mass', 'length' ],
        [ 'velocity', 'length' ],
        [ 'mass', 'velocity' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'orbital_period\' requires specific measurement types (see help)' )

    if 'mass' in arguments:
        mass = arguments[ 'mass' ]

        if 'length' in arguments:
            bRadius = True
            radius = arguments[ 'length' ]
        else:
            bRadius = False
            velocity = arguments[ 'velocity' ]
    else:
        # radius and velocity
        radius = arguments[ 'length' ]
        velocity = arguments[ 'velocity' ]
        period = divide( getProduct( [ 2, pi, radius ] ), velocity )
        return period.convert( 'second' )

    if bRadius:
        # radius and mass
        term = divide( getPower( radius, 3 ), multiply( getNewtonsConstant( ), mass ) )
        period = getProduct( [ 2, pi, getRoot( term, 2 ) ] )
    else:
        # velocity and mass
        period = divide( getProduct( [ 2, pi, getNewtonsConstant( ), mass ] ),
                         getPower( velocity, 3 ) )

    return period.convert( 'second' )


# //******************************************************************************
# //
# //  calculateOrbitalRadius
# //
# //******************************************************************************

def calculateOrbitalRadius( measurement1, measurement2 ):
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
    validUnitTypes = [
        [ 'mass', 'time' ],
        [ 'velocity', 'time' ],
        [ 'mass', 'velocity' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'orbital_radius\' requires specific measurement types (see help)' )

    if 'mass' in arguments:
        mass = arguments[ 'mass' ]

        if 'time' in arguments:
            bPeriod = True
            period = arguments[ 'time' ]
        else:
            bPeriod = False
            velocity = arguments[ 'velocity' ]
    else:
        # period and velocity
        period = arguments[ 'time' ]
        velocity = arguments[ 'velocity' ]
        radius = divide( multiply( velocity, period ), fmul( 2, pi ) )
        return radius.convert( 'meter' )

    if bPeriod:
        # period and mass
        term = divide( getProduct( [ getPower( period, 2 ), getNewtonsConstant( ), mass ] ),
                       fmul( 4, power( pi, 2 ) ) )
        radius = getRoot( term, 3 )
    else:
        # velocity and mass
        radius = divide( multiply( getNewtonsConstant( ), mass ), getPower( velocity, 2 ) )

    return radius.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateOrbitalVelocity
# //
# //******************************************************************************

def calculateOrbitalVelocity( measurement1, measurement2 ):
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
    validUnitTypes = [
        [ 'mass', 'time' ],
        [ 'length', 'time' ],
        [ 'mass', 'length' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'orbital_velocity\' requires specific measurement types (see help)' )

    if 'mass' in arguments:
        mass = arguments[ 'mass' ]

        if 'length' in arguments:
            bRadius = True
            radius = arguments[ 'length' ]
        else:
            bRadius = False
            period = arguments[ 'time' ]
    else:
        # radius and period
        radius = arguments[ 'length' ]
        period = arguments[ 'time' ]

        velocity = divide( getProduct( [ 2, pi, radius ] ), period )
        return velocity.convert( 'meter/second' )

    if bRadius:
        # mass and radius
        velocity = getRoot( divide( multiply( getNewtonsConstant( ), mass ), radius ), 2 )
    else:
        # mass and period
        term = divide( getProduct( [ period, period, getNewtonsConstant( ), mass ] ),
                       getProduct( [ 4, pi, pi ] ) )

        velocity = divide( getProduct( [ 2, pi, getRoot( term, 3 ) ] ), period )

    return velocity.convert( 'meter/second' )


# //******************************************************************************
# //
# //  calculateDistance
# //
# //  see https://en.wikipedia.org/wiki/Jounce
# //
# //******************************************************************************

def calculateDistance( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'time', 'velocity' ],
        [ 'acceleration', 'time' ],
        [ 'acceleration', 'velocity' ],
        [ 'jerk', 'acceleration' ],
        [ 'jerk', 'time' ],
        [ 'jerk', 'velocity' ],
        [ 'jounce', 'acceleration' ],
        [ 'jounce', 'time' ],
        [ 'jounce', 'velocity' ],
        [ 'jounce', 'jerk' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'distance\' requires specific measurement types (see help)' )

    types = sorted( [ key for key in arguments.keys( ) ] )

    if 'acceleration' in arguments:
        acceleration = arguments[ 'acceleration' ]

    if 'jerk' in arguments:
        jerk = arguments[ 'jerk' ]

    if 'jounce' in arguments:
        jounce = arguments[ 'jounce' ]

    if 'time' in arguments:
        time = arguments[ 'time' ]

    if 'velocity' in arguments:
        velocity = arguments[ 'velocity' ]

    if types == [ 'time', 'velocity' ]:
        distance = multiply( velocity, time )
    if types == [ 'acceleration', 'time' ]:
        distance = divide( multiply( acceleration, getPower( time, 2 ) ), 2 )
    if types == [ 'acceleration', 'velocity' ]:
        distance = divide( multiply( velocity, velocity ), multiply( acceleration, 2 ) )
    if types == [ 'jerk', 'acceleration' ]:
        time = divide( jerk, acceleration )
        distance = divide( multiply( jerk, getPower( time, 3 ) ), 6 )
    if types == [ 'jerk', 'time' ]:
        distance = divide( multiply( jerk, getPower( time, 3 ) ), 6 )
    if types == [ 'jerk', 'velocity' ]:
        distance = RPNMeasurement( '0.0', 'meter' )
    if types == [ 'jounce', 'acceleration' ]:
        distance = RPNMeasurement( '0.0', 'meter' )
    if types == [ 'jounce', 'time' ]:
        distance = divide( multiply( jounce, getPower( time, 4 ) ), 24 )
    if types == [ 'jounce', 'velocity' ]:
        distance = RPNMeasurement( '0.0', 'meter' )
    if types == [ 'jounce', 'jerk' ]:
        time = divide( jounce, jerk )
        distance = divide( multiply( jounce, getPower( time, 4 ) ), 24 )

    return distance.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateVelocity
# //
# //  see https://en.wikipedia.org/wiki/Jounce
# //
# //******************************************************************************

def calculateVelocity( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'length', 'time' ],
        [ 'acceleration', 'time' ],
        [ 'acceleration', 'length' ],
        [ 'jerk', 'time' ],
        [ 'jerk', 'length' ],
        [ 'jerk', 'acceleration' ],
        [ 'jounce', 'time' ],
        [ 'jounce', 'length' ],
        [ 'jounce', 'acceleration' ],
        [ 'jounce', 'jerk' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'velocity\' requires specific measurement types (see help)' )

    types = sorted( [ key for key in arguments.keys( ) ] )

    if 'acceleration' in arguments:
        acceleration = arguments[ 'acceleration' ]

    if 'jerk' in arguments:
        jerk = arguments[ 'jerk' ]

    if 'jounce' in arguments:
        jounce = arguments[ 'jounce' ]

    if 'length' in arguments:
        distance = arguments[ 'length' ]

    if 'time' in arguments:
        time = arguments[ 'time' ]

    if types == [ 'length', 'time' ]:
        velocity = divide( distance, time )
    elif types == [ 'acceleration', 'time' ]:
        velocity = multiply( acceleration, time )
    elif types == [ 'acceleration', 'length' ]:
        velocity = root( getProduct( [ 2, acceleration, distance ] ), 2 )
    elif types == [ 'jerk', 'time' ]:
        velocity = divide( multiply( jounce, getPower( time, 2 ) ), 2 )
    elif types == [ 'jerk', 'length' ]:
        velocity = RPNMeasurement( '0.0', 'meter/second' )
    elif types == [ 'jerk', 'accelerationn' ]:
        velocity = RPNMeasurement( '0.0', 'meter/second' )
    elif types == [ 'jounce', 'time' ]:
        velocity = divide( multiply( jounce, getPower( time, 3 ) ), 6 )
    elif types == [ 'jounce', 'length' ]:
        velocity = RPNMeasurement( '0.0', 'meter/second' )
    elif types == [ 'jounce', 'accelerationn' ]:
        velocity = RPNMeasurement( '0.0', 'meter/second' )
    elif types == [ 'jounce', 'jerk' ]:
        time = divide( jounce, jerk )
        velocity = divide( multiply( jounce, getPower( time, 3 ) ), 6 )

    return velocity.convert( 'meter/second' )


# //******************************************************************************
# //
# //  calculateAcceleration
# //
# //  see https://en.wikipedia.org/wiki/Jounce,
# //  http://hyperphysics.phy-astr.gsu.edu/hbase/avari.html
# //
# //******************************************************************************

def calculateAcceleration( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'length', 'velocity' ],
        [ 'time', 'velocity' ],
        [ 'jerk', 'length' ],
        [ 'jerk', 'time' ],
        [ 'jerk', 'velocity' ],
        [ 'jounce', 'length' ],
        [ 'jounce', 'time' ],
        [ 'jounce', 'velocity' ],
        [ 'jounce', 'jerk' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'acceleration\' requires specific measurement types (see help)' )

    types = sorted( [ key for key in arguments.keys( ) ] )

    if 'jerk' in arguments:
        jerk = arguments[ 'jerk' ]

    if 'jounce' in arguments:
        jounce = arguments[ 'jounce' ]

    if 'length' in arguments:
        distance = arguments[ 'length' ]

    if 'time' in arguments:
        time = arguments[ 'time' ]

    if 'velocity' in arguments:
        velocity = arguments[ 'velocity' ]

    if types == [ 'length', 'velocity' ]:
        acceleration = divide( multiply( velocity, velocity ), multply( distance, 2 ) )
    elif types == [ 'time', 'velocity' ]:
        acceleration = divide( velocity, time )
    elif types == [ 'jerk', 'length' ]:
        acceleration = RPNMeasurement( '0.0', 'meter/second^2' )
    elif types == [ 'jerk', 'time' ]:
        acceleration = multiply( jerk, time )
    elif types == [ 'jerk', 'velocity' ]:
        acceleration = RPNMeasurement( '0.0', 'meter/second^2' )
    elif types == [ 'jounce', 'length' ]:
        acceleration = RPNMeasurement( '0.0', 'meter/second^2' )
    elif types == [ 'jounce', 'time' ]:
        acceleration = calculateAcceleration( divide( multiply( jounce, time ), 2 ), time )
    elif types == [ 'jounce', 'velocity' ]:
        acceleration = RPNMeasurement( '0.0', 'meter/second^2' )
    elif types == [ 'jounce', 'jerk' ]:
        time = divide( jounce, jerk )
        acceleration = calculateAcceleration( divide( multiply( jounce, time ), 2 ), time )

    return acceleration.convert( 'meter/second^2' )


# //******************************************************************************
# //
# //  calculateKineticEnergy
# //
# //******************************************************************************

def calculateKineticEnergy( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'velocity', 'mass' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'kinetic_energy\' requires velocity and mass measurements' )

    mass = arguments[ 'mass' ]
    velocity = arguments[ 'velocity' ]

    energy = getProduct( [ 0.5, mass, velocity, velocity ] )
    return energy.convert( 'joule' )


# //******************************************************************************
# //
# //  calculateHorizonDistance
# //
# //******************************************************************************

def calculateHorizonDistance( altitude, radius ):
    validateUnits( altitude, 'length' )
    validateUnits( radius, 'length' )

    distance = getRoot( getProduct( [ 2, radius, altitude ] ), 2 )
    return distance.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateTrajectoryDistance
# //
# //  https://en.wikipedia.org/wiki/Trajectory_of_a_projectile
# //
# //******************************************************************************

def calculateTrajectoryDistance( velocity, angle ):
    validateUnits( velocity, 'velocity' )
    validateUnits( angle, 'angle' )

    sinValue = performTrigOperation( multiply( 2, angle ), sin )

    distance = divide( getProduct( [ velocity, velocity, sinValue ] ), RPNMeasurement( '9.806650', 'meter/second^2' ) )
    return distance.convert( 'meter' )

