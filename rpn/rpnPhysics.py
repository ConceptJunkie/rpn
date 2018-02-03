#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPhysics.py
# //
# //  RPN command-line calculator physics operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import struct

from rpn.rpnConstantUtils import getNewtonsConstant, getSpeedOfLight
from rpn.rpnGeometry import getNSphereRadius
from rpn.rpnList import getProduct
from rpn.rpnMath import divide, getPower, getRoot, multiply
from rpn.rpnMeasurement import checkUnits, getWhichUnitType, matchUnitTypes, \
                               RPNMeasurement, validateUnits
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, real_int

import rpn.rpnGlobals as g

from mpmath import fdiv, fmul, fsub, inf, pi, power, sqrt


# //******************************************************************************
# //
# //  calculateSchwarzchildRadius
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateSchwarzchildRadius( mass ):
    validateUnits( mass, 'mass' )

    radius = getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( getPower( getSpeedOfLight( ), 2 ) )
    return radius.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateTimeDilation
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
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

@twoArgFunctionEvaluator( )
def calculateOrbitalMass( measurement1, measurement2 ):
    '''
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
    '''
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

@twoArgFunctionEvaluator( )
def calculateOrbitalPeriod( measurement1, measurement2 ):
    '''
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
    '''
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

@twoArgFunctionEvaluator( )
def calculateOrbitalRadius( measurement1, measurement2 ):
    '''
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
    '''
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

@twoArgFunctionEvaluator( )
def calculateOrbitalVelocity( measurement1, measurement2 ):
    '''
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
    '''
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
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateDistance( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'length', 'time' ],
        [ 'velocity', 'time' ],
        [ 'acceleration', 'time' ],
        [ 'jerk', 'time' ],
        [ 'jounce', 'time' ]
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'distance\' requires specific measurement types (see help)' )

    time = arguments[ 'time' ]

    if 'length' in arguments:
        distance = arguments[ 'length' ]
    elif 'acceleration' in arguments:
        # acceleration and time
        distance = getProduct( [ fdiv( 1, 2 ), arguments[ 'acceleration' ], time, time ] )
    elif 'jerk' in arguments:
        # jerk and time
        distance = calculateDistance( getProduct( [ fdiv( 1, 2 ), arguments[ 'jerk' ], time ] ), time )
    elif 'jounce' in arguments:
        # jounce and time
        distance = calculateDistance( getProduct( [ fdiv( 1, 2 ), arguments[ 'jounce' ], time ] ), time )
    else:
        # velocity and time
        distance = multiply( arguments[ 'velocity' ], time )

    return distance.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateVelocity
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateVelocity( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'length', 'time' ],
        [ 'acceleration', 'length' ],
        [ 'jerk', 'length' ],
        [ 'jounce', 'length' ],
        [ 'velocity', 'time' ],
        [ 'velocity', 'length' ],
        [ 'acceleration', 'time' ],
        [ 'jerk', 'time' ],
        [ 'jounce', 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if 'velocity' in arguments:
        velocity = arguments[ 'velocity' ]
    elif 'length' in arguments:
        if 'time' in arguments:
            velocity = divide( arguments[ 'length' ], arguments[ 'time' ] )
        elif 'acceleration' in arguments:
            acceleration = arguments[ 'acceleration' ]
            time = getRoot( multiply( divide( arguments[ 'length' ], acceleration ), 2 ), 2 )
            velocity = multiply( acceleration, time )
        elif 'jerk' in arguments:
            jerk = arguments[ 'jerk' ]
            time = getRoot( multiply( divide( arguments[ 'length' ], jerk ), 6 ), 3 )
            velocity = getProduct( [ jerk, time, time, fdiv( 1, 2 ) ] )
        elif 'jounce' in arguments:
            jounce = arguments[ 'jounce' ]
            time = getRoot( multiply( divide( arguments[ 'length' ], jounce ), 24 ), 4 )
            velocity = getProduct( [ jounce, time, time, time, fdiv( 1, 6 ) ] )
    elif 'acceleration' in arguments:
        velocity = divide( multiply( arguments[ 'acceleration' ], arguments[ 'time' ] ), 2 )
    elif 'jerk' in arguments:
        velocity = divide( multiply( arguments[ 'jerk' ], getPower( arguments[ 'time' ], 2 ) ), 4 )
    elif 'jounce' in arguments:
        velocity = divide( multiply( arguments[ 'jounce' ], getPower( arguments[ 'time' ], 3 ) ), 8 )

    return velocity.convert( 'meter/second' )


# //******************************************************************************
# //
# //  calculateAcceleration
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateAcceleration( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'velocity', 'length' ],
        [ 'velocity', 'time' ],
        [ 'distance', 'time' ],
        [ 'acceleration', 'time' ],
        [ 'acceleration', 'length' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if 'acceleration' in arguments:
        acceleration = arguments[ 'acceleration' ]
    else:
        acceleration = RPNMeasurement( '1.0', 'meter/second^2' )

    return acceleration.convert( 'meter/second^2' )


# //******************************************************************************
# //
# //  calculateKineticEnergy
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateKineticEnergy( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'velocity', 'mass' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'kinetic_energy\' requires velocity and mass measurements' )

    mass = arguments[ 'mass' ]
    velocity = arguments[ 'velocity' ]
    energy = getProduct( [ fdiv( 1, 2 ), mass, velocity, velocity ] )
    return energy.convert( 'joule' )


# //******************************************************************************
# //
# //  calculateHorizonDistance
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateHorizonDistance( altitude, radius ):
    validateUnits( altitude, 'length' )
    validateUnits( radius, 'length' )

    distance = getRoot( getProduct( [ 2, radius, altitude ] ), 2 )
    return distance.convert( 'meter' )


# //******************************************************************************
# //
# //  calculateEnergyEquivalence
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateEnergyEquivalence( mass ):
    validateUnits( mass, 'mass' )

    energy = getProduct( [ mass, getSpeedOfLight( ), getSpeedOfLight( ) ] )
    return energy.convert( 'joule' )


# //******************************************************************************
# //
# //  calculateMassEquivalence
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateMassEquivalence( energy ):
    validateUnits( energy, 'energy' )

    mass = divide( energy, multiply( getSpeedOfLight( ), getSpeedOfLight( ) ) )
    return mass.convert( 'kilogram' )


# //******************************************************************************
# //
# //  calculateSurfaceGravity
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateSurfaceGravity( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'mass', 'density' ],
        [ 'mass', 'length' ],
        [ 'mass', 'volume' ],
        [ 'density', 'length' ],
        [ 'density', 'volume' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'surface_gravity\' requires length and mass measurements' )

    if 'mass' in arguments:
        mass = arguments[ 'mass' ]

        if 'length' in arguments:
            length = arguments[ 'length' ]
        elif 'density' in arguments:
            volume = divide( mass, arguments[ 'density' ] )
            length = getNSphereRadius( volume, 3 )
        else:
            length = getNSphereRadius( arguments[ 'volume' ], 3 )
    elif 'volume' in arguments:
        # density, volume
        volume = arguments[ 'volume' ]
        mass = multiply( arguments[ 'density' ], volume )
        length = getNSphereRadius( volume, 3 )
    else:
        # density, length
        length = arguments[ 'length' ]
        volume = getPower( length, 3 )
        mass = multiply( arguments[ 'density' ], volume )

    gravity = multiply( divide( mass, getPower( length, 2 ) ), getNewtonsConstant( ) )
    return gravity.convert( 'meters/seconds^2' )

