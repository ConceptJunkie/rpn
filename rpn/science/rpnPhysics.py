#!/usr/bin/env python

#******************************************************************************
#
#  rpnPhysics.py
#
#  rpnChilada physics operators
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import fdiv, fmul, fneg, fprod, fsub, fsum, inf, ln, mpmathify, pi, power, sqrt

from rpn.math.rpnGeometry import getKSphereRadius
from rpn.math.rpnMath import divide, getPower, getRoot, multiply

from rpn.special.rpnList import getProduct

from rpn.units.rpnConstantUtils import getConstant
from rpn.units.rpnMatchUnitTypes import matchUnitTypes
from rpn.units.rpnMeasurementClass import RPNMeasurement

from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, MeasurementValidator


#******************************************************************************
#
#  calculateBlackHoleMassOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleMass( measurement ):
    # pylint: disable=line-too-long
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_mass: invalid argument' )

    if 'mass' in arguments:
        return arguments[ 'mass' ].convert( 'kilogram' )

    if 'length' in arguments:
        radius = arguments[ 'length' ]

        return divide( getProduct( [ 2, getConstant( 'newton_constant' ) ] ),
                       getProduct( [ getPower( getConstant( 'speed_of_light' ), 2 ), radius ] ) ).convert( 'kilogram' )

    if 'acceleration' in arguments:
        gravity = arguments[ 'acceleration' ]

        return divide( getPower( getConstant( 'speed_of_light' ), 4 ),
                       getProduct( [ 4, getConstant( 'newton_constant' ),
                                     gravity ] ) ).convert( 'kilogram' )

    if 'area' in arguments:
        area = arguments[ 'area' ].convert( 'meters^2' )

        return getRoot( divide( getProduct( [ getPower( getConstant( 'speed_of_light' ),
                                                        4 ), area ] ),
                                getProduct( [ 16, pi, getPower( getConstant( 'newton_constant' ),
                        2 ) ] ) ), 2 ).convert( 'kilogram' )

    if 'temperature' in arguments:
        temperature = arguments[ 'temperature' ]

        return divide( getProduct( [ getConstant( 'reduced_planck_constant' ),
                       getPower( getConstant( 'speed_of_light' ), 3 ) ] ),
                       getProduct( [ temperature, 8, getConstant( 'boltzmann_constant' ), pi,
                       getConstant( 'newton_constant' ) ] ) ).convert( 'kilogram' )

    if 'power' in arguments:
        luminosity = arguments[ 'power' ]

        return getRoot( divide(
                        getProduct( [ getConstant( 'reduced_planck_constant' ),
                                      getPower( getConstant( 'speed_of_light' ), 6 ) ] ),
                        getProduct( [ luminosity.convert( 'kilogram*meter^2/second^3' ), 15360, pi,
                                      getPower( getConstant( 'newton_constant' ), 2 ) ] ) ),
                        2  ).convert( 'kilogram' )

    if 'tidal_force' in arguments:
        tidalForce = arguments[ 'tidal_force' ]

        return getRoot( divide( getPower( getConstant( 'speed_of_light' ), 6 ),
                                getProduct( [ 4, tidalForce,
                                     getPower( getConstant( 'newton_constant' ), 2 ) ] ) ),
                        2 ).convert( 'kilogram' )

    if 'time' in arguments:
        lifetime = arguments[ 'time' ]

        return getRoot( divide( getProduct( [ lifetime, mpmathify( '1.8083' ),
                                              getConstant( 'reduced_planck_constant' ),
                                              getPower( getConstant( 'speed_of_light' ), 4 ) ] ),
                                getProduct( [ 5120, pi,
                                              getPower( getConstant( 'newton_constant' ), 2 ) ] ) ),
                        3 ).convert( 'kilogram' )

    raise ValueError( 'invalid arguments to black hole operator' )


@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleMassOperator( n ):
    return calculateBlackHoleMass( n )


#******************************************************************************
#
#  calculateBlackHoleRadiusOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleRadiusOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_radius: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    radius = getProduct( [ 2, getConstant( 'newton_constant' ), mass ] ). \
             divide( getPower( getConstant( 'speed_of_light' ), 2 ) )
    return radius.convert( 'meter' )


#******************************************************************************
#
#  calculateBlackHoleSurfaceAreaOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleSurfaceAreaOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_surface_area: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    area = divide( getProduct( [ 16, pi,
                                 getPower( getConstant( 'newton_constant' ), 2 ), getPower( mass, 2 ) ] ),
                   getPower( getConstant( 'speed_of_light' ), 4 ) )
    return area.convert( 'meter^2' )


#******************************************************************************
#
#  calculateBlackHoleSurfaceGravityOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleSurfaceGravityOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_surface_gravity: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    gravity = divide( getPower( getConstant( 'speed_of_light' ), 4 ),
                      getProduct( [ mass, 4, getConstant( 'newton_constant' ) ] ) )
    return gravity.convert( 'meter/second^2' )


#******************************************************************************
#
#  calculateBlackHoleEntropyOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleEntropyOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_entropy: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    entropy = divide( getProduct( [ getPower( mass, 2 ), 4, pi, getConstant( 'newton_constant' ) ] ),
                      getProduct( [ getConstant( 'reduced_planck_constant' ),
                                    getConstant( 'speed_of_light' ), ln( 10.0 ) ] ) )

    return getConstant( 'boltzmann_constant' ).multiply( entropy ).convert( 'bit' )


#******************************************************************************
#
#  calculateBlackHoleTemperatureOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleTemperatureOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_temperature: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    temperature = divide( getProduct( [ getConstant( 'reduced_planck_constant' ),
                                        getPower( getConstant( 'speed_of_light' ), 3 ) ] ),
                          getProduct( [ mass, 8, getConstant( 'boltzmann_constant' ), pi,
                                        getConstant( 'newton_constant' ) ] ) )

    return temperature.convert( 'kelvin' )


#******************************************************************************
#
#  calculateBlackHoleLuminosityOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleLuminosityOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_luminosity: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    luminosity = divide( getProduct( [ getConstant( 'reduced_planck_constant' ),
                                       getPower( getConstant( 'speed_of_light' ), 6 ) ] ),
                         getProduct( [ getPower( mass, 2 ), 15360, pi,
                                       getPower( getConstant( 'newton_constant' ), 2 ) ] ) )

    return luminosity.convert( 'watts' )


#******************************************************************************
#
#  calculateBlackHoleLifetimeOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleLifetimeOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_lifetime: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    lifetime = divide( getProduct( [ getPower( mass, 3 ), 5120, pi,
                                     getPower( getConstant( 'newton_constant' ), 2 ) ] ),
                       getProduct( [ mpmathify( '1.8083' ), getConstant( 'reduced_planck_constant' ),
                                     getPower( getConstant( 'speed_of_light' ), 4 ) ] ) )

    return lifetime.convert( 'seconds' )


#******************************************************************************
#
#  calculateSurfaceTidesOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateBlackHoleSurfaceTidesOperator( measurement ):
    validUnitTypes = [
        [ 'mass' ],
        [ 'length' ],
        [ 'acceleration' ],
        [ 'area' ],
        [ 'temperature' ],
        [ 'power' ],
        [ 'tidal_force' ],
        [ 'time' ],
    ]

    arguments = matchUnitTypes( [ measurement ], validUnitTypes )

    if not arguments:
        raise ValueError( 'black_hole_surface_tides: invalid argument' )

    mass = calculateBlackHoleMass( measurement )

    tidalForce = divide( getPower( getConstant( 'speed_of_light' ), 6 ),
                         getProduct( [ 4, getPower( getConstant( 'newton_constant' ), 2 ), getPower( mass, 2 ) ] ) )

    return tidalForce.convert( '1/second^2' )


#******************************************************************************
#
#  calculateTidalForceOperator
#
#  https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
#
#  Two arguments are the same unit type, so the order needs to be fixed.
#
#******************************************************************************

@argValidator( [ MeasurementValidator( ), MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateTidalForceOperator( mass, distance, delta ):
    mass.validateUnits( 'mass' )
    distance.validateUnits( 'length' )
    delta.validateUnits( 'length' )

    tidalForce = divide( getProduct( [ 2, getConstant( 'newton_constant' ), mass, delta ] ),
                         getPower( distance, 3 ) )

    return tidalForce.convert( 'meter/second^2' )


#******************************************************************************
#
#  calculateTimeDilationOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateTimeDilationOperator( velocity ):
    velocity.validateUnits( 'velocity' )

    ratio = divide( velocity, getConstant( 'speed_of_light' ) )

    if ratio == 1:
        return inf

    return fdiv( 1, sqrt( fsub( 1, power( ratio, 2 ) ) ) )


#******************************************************************************
#
#  calculateEscapeVelocityOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateEscapeVelocityOperator( mass, radius ):
    mass.validateUnits( 'mass' )
    radius.validateUnits( 'length' )

    velocity = getRoot( getProduct( [ 2, getConstant( 'newton_constant' ), mass ] ).divide( radius ), 2 )
    return velocity.convert( 'meter/second' )


#******************************************************************************
#
#  calculateOrbitalMassOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateOrbitalMassOperator( measurement1, measurement2 ):
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
        mass = divide( getProduct( [ velocity, velocity, radius ] ), getConstant( 'newton_constant' ) )
        return mass.convert( 'kilogram' )

    if bRadius:
        # radius and period
        mass = divide( getProduct( [ 4, pi, pi, radius, radius, radius ] ),
                       getProduct( [ getConstant( 'newton_constant' ), period, period ] ) )
    else:
        # velocity and period
        mass = divide( getProduct( [ velocity, velocity, velocity, period ] ),
                       getProduct( [ 2, pi, getConstant( 'newton_constant' ) ] ) )

    return mass.convert( 'kilogram' )


#******************************************************************************
#
#  calculateOrbitalPeriodOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateOrbitalPeriodOperator( measurement1, measurement2 ):
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
        term = divide( getPower( radius, 3 ), multiply( getConstant( 'newton_constant' ), mass ) )
        period = getProduct( [ 2, pi, getRoot( term, 2 ) ] )
    else:
        # velocity and mass
        period = divide( getProduct( [ 2, pi, getConstant( 'newton_constant' ), mass ] ),
                         getPower( velocity, 3 ) )

    return period.convert( 'second' )


#******************************************************************************
#
#  calculateOrbitalRadiusOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateOrbitalRadiusOperator( measurement1, measurement2 ):
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
        term = divide( getProduct( [ getPower( period, 2 ), getConstant( 'newton_constant' ), mass ] ),
                       fmul( 4, power( pi, 2 ) ) )
        radius = getRoot( term, 3 )
    else:
        # velocity and mass
        radius = divide( multiply( getConstant( 'newton_constant' ), mass ), getPower( velocity, 2 ) )

    return radius.convert( 'meter' )


#******************************************************************************
#
#  calculateOrbitalVelocityOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateOrbitalVelocityOperator( measurement1, measurement2 ):
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
        velocity = getRoot( divide( multiply( getConstant( 'newton_constant' ), mass ), radius ), 2 )
    else:
        # mass and period
        term = divide( getProduct( [ period, period, getConstant( 'newton_constant' ), mass ] ),
                       getProduct( [ 4, pi, pi ] ) )

        velocity = divide( getProduct( [ 2, pi, getRoot( term, 3 ) ] ), period )

    return velocity.convert( 'meter/second' )


#******************************************************************************
#
#  calculateDistanceOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
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


@twoArgFunctionEvaluator( )
def calculateDistanceOperator( measurement1, measurement2 ):
    return calculateDistance( measurement1, measurement2 )


#******************************************************************************
#
#  calculateVelocityOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateVelocityOperator( measurement1, measurement2 ):
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


#******************************************************************************
#
#  calculateAccelerationOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateAccelerationOperator( measurement1, measurement2 ):
    validUnitTypes = [
        [ 'velocity', 'length' ],
        [ 'velocity', 'time' ],
        [ 'length', 'time' ],
        [ 'acceleration', 'time' ],
        [ 'acceleration', 'length' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if 'acceleration' in arguments:
        acceleration = arguments[ 'acceleration' ]
    elif 'velocity' in arguments:
        if 'length' in arguments:
            acceleration = divide( getPower( arguments[ 'velocity' ], 2 ), multiply( arguments[ 'length' ], 2 ) )
        else:
            acceleration = divide( arguments[ 'velocity' ], arguments[ 'time' ] )
    elif 'length' in arguments and 'time' in arguments:
        acceleration = multiply( 2, divide( arguments[ 'length' ], getPower( arguments[ 'time' ], 2 ) ) )

    return acceleration.convert( 'meter/second^2' )


#******************************************************************************
#
#  calculateKineticEnergyOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateKineticEnergyOperator( measurement1, measurement2 ):
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


#******************************************************************************
#
#  calculateHorizonDistanceOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateHorizonDistanceOperator( altitude, radius ):
    altitude.validateUnits( 'length' )
    radius.validateUnits( 'length' )

    distance = getRoot( getProduct( [ 2, radius, altitude ] ), 2 )
    return distance.convert( 'meter' )


#******************************************************************************
#
#  calculateEnergyEquivalenceOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateEnergyEquivalenceOperator( mass ):
    mass.validateUnits( 'mass' )

    energy = getProduct( [ mass, getConstant( 'speed_of_light' ), getConstant( 'speed_of_light' ) ] )
    return energy.convert( 'joule' )


#******************************************************************************
#
#  calculateMassEquivalenceOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def calculateMassEquivalenceOperator( energy ):
    energy.validateUnits( 'energy' )

    mass = divide( energy, multiply( getConstant( 'speed_of_light' ), getConstant( 'speed_of_light' ) ) )
    return mass.convert( 'kilogram' )


#******************************************************************************
#
#  calculateSurfaceGravityOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateSurfaceGravityOperator( measurement1, measurement2 ):
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
            length = getKSphereRadius( volume, 3 )
        else:
            length = getKSphereRadius( arguments[ 'volume' ], 3 )
    elif 'volume' in arguments:
        # density, volume
        volume = arguments[ 'volume' ]
        mass = multiply( arguments[ 'density' ], volume )
        length = getKSphereRadius( volume, 3 )
    else:
        # density, length
        length = arguments[ 'length' ]
        volume = getPower( length, 3 )
        mass = multiply( arguments[ 'density' ], volume )

    gravity = multiply( divide( mass, getPower( length, 2 ) ), getConstant( 'newton_constant' ) )
    return gravity.convert( 'meters/seconds^2' )


#******************************************************************************
#
#  calculateWindChillOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateWindChillOperator( measurement1, measurement2 ):
    '''
    https://www.ibiblio.org/units/dictW.html
    '''

    validUnitTypes = [
        [ 'velocity', 'temperature' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'wind_chill\' requires velocity and temperature measurements' )

    windSpeed = arguments[ 'velocity' ].convert( 'miles/hour' ).value
    temperature = arguments[ 'temperature' ].convert( 'degrees_F' ).value

    if windSpeed < 3:
        raise ValueError( '\'wind_chill\' is not defined for wind speeds less than 3 mph' )

    if temperature > 50:
        raise ValueError( '\'wind_chill\' is not defined for temperatures over 50 degrees fahrenheit' )

    result = fsum( [ 35.74, fmul( temperature, 0.6215 ), fneg( fmul( 35.75, power( windSpeed, 0.16 ) ) ),
                     fprod( [ 0.4275, temperature, power( windSpeed, 0.16 ) ] ) ] )

    # in case someone puts in a silly velocity
    if result < -459.67:
        result = -459.67

    return RPNMeasurement( result, 'degrees_F' ).convert( arguments[ 'temperature' ].units )


#******************************************************************************
#
#  calculateHeatIndexOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def calculateHeatIndexOperator( measurement1, measurement2 ):
    '''
    https://en.wikipedia.org/wiki/Heat_index#Formula
    '''
    # pylint: disable=invalid-name
    validUnitTypes = [
        [ 'temperature', 'constant' ],
    ]

    arguments = matchUnitTypes( [ measurement1, measurement2 ], validUnitTypes )

    if not arguments:
        raise ValueError( '\'heat_index\' requires a temperature measurement and the relative humidity in percent' )

    T = arguments[ 'temperature' ].convert( 'degrees_F' ).value
    R = arguments[ 'constant' ]

    if T < 80:
        raise ValueError( '\'heat_index\' is not defined for temperatures less than 80 degrees fahrenheit' )

    if R < 0.4 or R > 1.0:
        raise ValueError( '\'heat_index\' requires a relative humidity value ranging from 40% to 100%' )

    R = fmul( R, 100 )

    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783e-3
    c6 = -5.481717e-2
    c7 = 1.22874e-3
    c8 = 8.5282e-4
    c9 = -1.99e-6

    heatIndex = fsum( [ c1, fmul( c2, T ), fmul( c3, R ), fprod( [ c4, T, R ] ), fprod( [ c5, T, T ] ),
                        fprod( [ c6, R, R ] ), fprod( [ c7, T, T, R ] ), fprod( [ c8, T, R, R ] ),
                        fprod( [ c9, T, T, R, R ] ) ] )

    return RPNMeasurement( heatIndex, 'fahrenheit' ).convert( arguments[ 'temperature' ].units )
