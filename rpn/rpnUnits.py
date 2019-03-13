#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUnits.py
# //
# //  RPN command-line calculator unit conversion declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import fadd, fdiv, fmul, fprod, log, mpf, mpmathify, pi, power

from rpn.rpnConstantUtils import *
from rpn.rpnEstimates import *
from rpn.rpnUnitClasses import RPNConstantInfo, RPNUnitInfo, RPNUnitTypeInfo


# //******************************************************************************
# //
# //  basicUnitTypes
# //
# //  dimension:
# //      length, mass, time, charge, temperature, angle, electric_potential
# //      information_entropy, luminous_intensity
# //
# //  baseUnit:  The standard or customary unit of measurement for this unit
# //      type
# //
# //  estimateTable : The table of estimates, expressed in terms of the base
# //      unit, used for the 'estimate' operator.
# //
# //  Constant is not a 'real' unit type, but it is useful for it to act like
# //  one because it makes for useful operators, e.g. "20 M" for "20,000,000'.
# //
# //  https://en.wikipedia.org/wiki/SI_electromagnetism_units
# //
# //
# //******************************************************************************

basicUnitTypes = {
    '_null_type' : RPNUnitTypeInfo(
        'constant',
        'length^0',
        None
    ),

    'acceleration' : RPNUnitTypeInfo(
        'length/time^2',
        'meter/second^2',
        accelerationTable
    ),

    'amount_of_substance' : RPNUnitTypeInfo(
        'amount_of_substance',
        'mole',
        amountOfSubstanceTable
    ),

    'angle' : RPNUnitTypeInfo(
        'angle',
        'radian',
        angleTable
    ),

    'area' : RPNUnitTypeInfo(
        'length^2',
        'meter^2',
        areaTable,
    ),

    'capacitance' : RPNUnitTypeInfo(
        'current^2*time^4/mass*length^2',
        'farad',
        capacitanceTable,
    ),

    'charge' : RPNUnitTypeInfo(
        'current*time',
        'coulomb',
        chargeTable,
    ),

    'constant' : RPNUnitTypeInfo(
        'constant',
        'unity',
        constantTable,
    ),

    'current' : RPNUnitTypeInfo(
        'current',
        'ampere',
        currentTable,
    ),

    'data_rate' : RPNUnitTypeInfo(
        'mass*length^2/time^3*temperature',
        'bit/second',
        dataRateTable,
    ),

    'density' : RPNUnitTypeInfo(
        'mass/length^3',
        'kilogram/liter',
        densityTable,
    ),

    'dynamic_viscosity' : RPNUnitTypeInfo(
        'mass/length*time',
        'pascal*second',
        dynamicViscosityTable,
    ),

    'electrical_conductance' : RPNUnitTypeInfo(
        'current^2*time^3/length^2*mass',
        'siemens',
        electricalConductanceTable,
    ),

    'electrical_resistance' : RPNUnitTypeInfo(
        'length^2*mass/current^2*time^3',
        'ohm',
        electricalResistanceTable,
    ),

    'electric_potential' : RPNUnitTypeInfo(
        'mass*length^2/current*time^3',
        'volt',
        electricPotentialTable,
    ),

    'energy' : RPNUnitTypeInfo(
        'mass*length^2/time^2',
        'joule',
        energyTable,
    ),

    'force' : RPNUnitTypeInfo(
        'mass*length/time^2',
        'newton',
        forceTable,
    ),

    'frequency' : RPNUnitTypeInfo(
        '1/time',
        'hertz',
        frequencyTable,
    ),

    'illuminance' : RPNUnitTypeInfo(
        'luminous_intensity*angle^2/length^2',
        'lux',
        illuminanceTable,
    ),

    'inductance' : RPNUnitTypeInfo(
        'mass*length^2/time^2*current^2',
        'henry',
        inductanceTable,
    ),

    'information_entropy' : RPNUnitTypeInfo(
        'mass*length^2/time^2*temperature',
        'bit',
        informationEntropyTable,
    ),

    'jerk' : RPNUnitTypeInfo(
        'length/time^3',
        'meter/second^3',
        jerkTable
    ),

    'jounce' : RPNUnitTypeInfo(
        'length/time^4',
        'meter/second^4',
        jounceTable
    ),

    'length' : RPNUnitTypeInfo(
        'length',
        'meter',
        lengthTable,
    ),

    'luminance' : RPNUnitTypeInfo(
        'luminous_intensity/length^2',
        'candela/meter^2',
        luminanceTable,
    ),

    'luminous_flux' : RPNUnitTypeInfo(
        'luminous_intensity*angle^2',
        'lumen',
        luminousFluxTable,
    ),

    'luminous_intensity' : RPNUnitTypeInfo(
        'luminous_intensity',
        'candela',
        luminousIntensityTable,
    ),

    'magnetic_field_strength' : RPNUnitTypeInfo(
        'current/length',
        'ampere/meter',
        magneticFieldStrengthTable,
    ),

    'magnetic_flux' : RPNUnitTypeInfo(
        'mass*length^2/time^2*current',
        'weber',
        magneticFluxTable,
    ),

    'magnetic_flux_density' : RPNUnitTypeInfo(
        'mass/time^2*current',
        'tesla',
        magneticFluxDensityTable,
    ),

    'mass' : RPNUnitTypeInfo(
        'mass',
        'kilogram',
        massTable,
    ),

    'power' : RPNUnitTypeInfo(
        'mass*length^2/time^3',
        'watt',
        powerTable,
    ),

    'pressure' : RPNUnitTypeInfo(
        'mass/length*time^2',
        'pascal',
        pressureTable,
    ),

    'radiation_dose' : RPNUnitTypeInfo(
        'length^2/time^2',
        'sievert',
        radiationDoseTable,
    ),

    'radiation_exposure' : RPNUnitTypeInfo(
        'current*time/mass',
        'coulomb/kilogram',
        radiationExposureTable,
    ),

    'radiosity' : RPNUnitTypeInfo(
        'mass/time^3',
        'watt/meter^2',
        radiosityTable,
    ),

    'solid_angle' : RPNUnitTypeInfo(
        'angle^2',
        'steradian',
        solidAngleTable,
    ),

    'temperature' : RPNUnitTypeInfo(
        'temperature',
        'kelvin',
        temperatureTable,
    ),

    'time' : RPNUnitTypeInfo(
        'time',
        'second',
        timeTable,
    ),

    'velocity' : RPNUnitTypeInfo(
        'length/time',
        'meter/second',
        velocityTable,
    ),

    'volume' : RPNUnitTypeInfo(
        'length^3',
        'liter',
        volumeTable,
    ),
}


# //******************************************************************************
# //
# //  constantOperators
# //
# //  unit name : value, unit, aliases, multipliable, description
# //
# //  When unit types are multiplied in compound units, they need to be
# //  specified in alphabetical order in the name, but not the representations.
# //
# //******************************************************************************

constantOperators = {
    # physical constants
    'avogadro_number' :
        RPNConstantInfo( '6.022140857e23', '', [ 'avogadro', 'avogadros_number' ], True,
                         'Avogadro\'s number, the number of atoms in a mole',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?na
''' ),

    'boltzmann_constant' :
        RPNConstantInfo( '1.38064852e-23', 'kilogram*meter^2/second^2*kelvin', [ 'boltzmann', 'boltzmanns_const', 'k_sub_b', 'k_b' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?e
''' ),

    'bohr_radius' :
        RPNConstantInfo( '5.2917721067e-11', 'meter', [ ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0
''' ),

    'coulomb_constant' :
        RPNConstantInfo( '8.9875517873681764e9', 'joule*meter/coulomb^2', [ ], True,
                         '',
                         '''
Ref:  https://en.wikipedia.org/wiki/Coulomb%27s_constant
''' ),

    'electric_constant' :
        RPNConstantInfo( '8.854187817e-12', 'ampere^2*second^4/kilogram*meter^3', [ 'e0', 'e_0', 'e_nought', 'e_sub_0', 'free_space_permittivity', 'vacuum_permittivity' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?ep0
''' ),

    'electric_constant_2' :
        RPNConstantInfo( '8.854187817e-12', 'coulomb^2/newton*meter^2', [ ], True,
                         'same as the electric_constant, but with different units',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?ep0
''' ),

#    return RPNMeasurement( '8.854187817e-12', 'farad/meter' )
#    return RPNMeasurement( '8.854187817e-12', 'coulomb/volt*meter' )

    'electron_charge' :
        RPNConstantInfo( '1.6021766208e-19', 'coulomb', [ 'elementary_charge' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?e
''' ),

    'faraday_constant' :
        RPNConstantInfo( '96485.33289', 'coulomb/mole', [ 'faradays_constant' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?f
''' ),

    'magnetic_constant' :
        RPNConstantInfo( fprod( [ 4, pi, 1.0e-7 ] ), 'newton/ampere^2', [ 'free_space_permeability', 'mu0', 'mu_0', 'mu_sub_0', 'mu_nought' ], True,
                         '',
                         '''
This constant is exact by definition.

Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?mu0
''' ),

    'magnetic_flux_quantum' :
        RPNConstantInfo( '2.067833831e-15', 'weber', [ 'magnetic_flux', 'magnetic_flux_quantum', 'magnetic_flux_quanta' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?flxquhs2e
''' ),

    'molar_gas_constant' :
        RPNConstantInfo( '8.3144598', 'joule/mole*kelvin', [ 'gas_constant', 'ideal_gas_constant', 'universal_gas_constant' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?r
''' ),

    'newton_constant' :
        RPNConstantInfo( '6.67408e-11', 'meter^3/kilogram*second^2', [ 'G', 'newtons_constant' ], True,
                         'Newton\'s constant of gravitation',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?bg
''' ),

    'nuclear_magneton' :
        RPNConstantInfo( '5.050783699e-27', 'joule/tesla', [ ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?mun

''' ),

    'planck_constant' :
        RPNConstantInfo( '6.626070040e-34', 'kilogram*meter^2/second', [ 'h', 'planck' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?h
''' ),

    'reduced_planck_constant' :
        RPNConstantInfo( fdiv( mpmathify( '6.626070040e-34' ), fmul( 2, pi ) ), 'kilogram*meter^2/second', [ 'h_bar', 'reduced_planck', 'dirac', 'dirac_constant' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?h
''' ),

    'rydberg_constant' :
        RPNConstantInfo( '10973731.568508', 'meter^-1', [ ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?ryd
''' ),

    'speed_of_light' :
        RPNConstantInfo( '299792458', 'meter/second', [ 'c', 'lightspeed', 'light_speed', 'planck_speed', 'planck_velocity' ], True,
                         'the speed of light in a vacuum',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?c
''' ),

    'stefan_boltzmann_constant' :
        RPNConstantInfo( '5.670367e-8', 'watt/meter^2*kelvin^4', [ 'sigma_sb', 'stefan_boltzmann' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?sigma
''' ),

    'vacuum_impedance' :
        RPNConstantInfo( '376.730313461', 'ohm', [ 'z_nought', 'z0','z_0', 'z_sub_0' ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?z0
''' ),

    'von_klitzing_constant' :
        RPNConstantInfo( '25812.8074555', 'ohm', [ ], True,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?rk
''' ),

    # physical quantities
    'aa_battery' :
        RPNConstantInfo( '15400', 'joule', [ ], True,
                         'Typical energy charge of a fully-charged alkaline AA battery',
                         '''
''' ),

    'gallon_of_ethanol' :
        RPNConstantInfo( '8.4e7', 'joule', [ ], True,
                         'Energy content of a U.S. gallon of ethanol',
                         '''
''' ),

    'gallon_of_gasoline' :
        RPNConstantInfo( '1.2e8', 'joule', [ ], True,
                         'Typical energy content of a U.S. gallon of gasoline',
                         '''
''' ),

    'density_of_water' :
        RPNConstantInfo( '997.0474', 'kilogram/meter^3', [ 'water' ], True,
                         'Density of pure water at 25 degress Celsius',
                         '''
''' ),

    'solar_constant' :
        RPNConstantInfo( '1360.8', 'watt/meter^2', [ ], True,
                         'Average maximum energy received from the Sun on the Earth\'s surface',
                         '''
This constant represents the average maximum amount of luminous energy the
Earth receives from the Sun.  The solar constant does vary slightly over
time due to fluctuations in solar energy output.
''' ),

    # subatomic particle constants
    'alpha_particle_mass' :
        RPNConstantInfo( '6.644657230e-27', 'kilogram', [ ], True,
                         'Alpha particle (helium nucleus) mass',
                         '''
The alpha particle is the equivalent of a helium nucleus, and consists of two
protons and two neutrons.
''' ),

    'deuteron_mass' :
        RPNConstantInfo( '3.343583719e-27', 'kilogram', [ ], True,
                         'Deuterium nucleus mass',
                         '''
''' ),

    'electron_mass' :
        RPNConstantInfo( '9.10938356e-31', 'kilogram', [ 'electron_rest_mass' ], True,
                         '',
                         '''
''' ),

    'helion_mass' :
        RPNConstantInfo( '5.006412700e-27', 'kilogram', [ ], True,
                         'Helium-3 nucleus mass',
                         '''
''' ),

    'muon_mass' :
        RPNConstantInfo( '1.883531594e-28', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'neutron_mass' :
        RPNConstantInfo( '1.674927471e-27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'proton_mass' :
        RPNConstantInfo( '1.672621898e-27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'tau_mass' :
        RPNConstantInfo( '3.16747e-27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'triton_mass' :
        RPNConstantInfo( '5.007356665e-27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    # heavenly body constants
    'sun_luminosity' :
        RPNConstantInfo( '3.826e26', 'watt', [ 'solar_luminosity' ], True,
                         '',
                         '''
''' ),

    'sun_mass' :
        RPNConstantInfo( '1.988500e30', 'kilogram', [ 'solar_mass' ], True,
                         '',
                         '''
Ref:  http://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
''' ),

    'sun_radius' :
        RPNConstantInfo( '6.9599e8', 'meter', [ 'solar_radius' ], True,
                         '',
                         '''
''' ),

    'sun_volume' :
        RPNConstantInfo( '1.412e27', 'meter^3', [ 'solar_volume' ], True,
                         '',
                         '''
''' ),


    'mercury_mass' :
        RPNConstantInfo( '3.301e26', 'kilogram', [ ], True,
                         'the mass of the planet Mercury',
                         '''
''' ),

    # equitorial radius
    'mercury_radius' :
        RPNConstantInfo( '2.4397e6', 'meter', [ ], True,
                         'the radius of the planet Mercury',
                         '''
''' ),

    # sidereal orbit period
    'mercury_revolution' :
        RPNConstantInfo( '87.969', 'day', [ 'mercury_year' ], True,
                         'the revolution time of the planet Mercury around the Sun',
                         '''
''' ),

    'mercury_volume' :
        RPNConstantInfo( '6.083e19', 'meter^3', [ ], True,
                         'the volume of the planet Mercury',
                         '''
''' ),

    'venus_mass' :
        RPNConstantInfo( '4.8689952e24', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'venus_radius' :
        RPNConstantInfo( '6.0518e6', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'venus_revolution' :
        RPNConstantInfo( '224.701', 'day', [ 'venus_year' ], True,
                         '',
                         '''
''' ),

    'venus_volume' :
        RPNConstantInfo( '9.2843e20', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'earth_density' :
        RPNConstantInfo( '5.514', 'gram/centimeter^3', [ ], True,   # https://en.wikipedia.org/wiki/Earth#Composition_and_structure
                         '',
                         '''
''' ),

    'earth_gravity' :
        RPNConstantInfo( '9.80665', 'meter/second^2',               # based on earth_radius
                         [ 'earth_gravities', 'gee', 'gees', 'standard_gravity', 'standard_gravities' ], True,
                         '',
                         '''
''' ),

    'earth_mass' :
        RPNConstantInfo( '5.9640955e24', 'kilogram', [ ], True,     # based on earth_radius and earth_gravity
                         '',
                         '''
''' ),

    'earth_radius' :
        RPNConstantInfo( '6371800', 'meter', [ ], True,             # https://en.wikipedia.org/wiki/Earth_radius#Global_average_radii - volumetric radius
                         '',
                         '''
''' ),

    'earth_volume' :
        RPNConstantInfo( '1.083207324897e21', 'meter^3', [ ], True, # based on earth_radius
                         '',
                         '''
''' ),

    'sidereal_year' :
        RPNConstantInfo( '365.256360417', 'day', [ ], True,
                         '',
                         '''
''' ),

    'tropical_year' :
        RPNConstantInfo( '365.24219', 'day', [ 'solar_year' ], True,
                         '',
                         '''
The definition used is the calculation of the mean tropical year on
1 January 2000.
''' ),

    'moon_gravity' :
        RPNConstantInfo( '1.62', 'meter/second^2',                  # based on moon_radius
                         [ 'moon_gravities', 'lunar_gravity', 'lunar_gravities' ], True,
                         '',
                         '''
''' ),

    'moon_mass' :
        RPNConstantInfo( '7.342e22', 'kilogram', [ 'lunar_mass' ], True,
                         '',
                         '''
''' ),


    'moon_radius' :
        RPNConstantInfo( '1.7381e6', 'meter', [ 'lunar_radius' ], True,
                         '',
                         '''
''' ),

    'moon_revolution' :
        RPNConstantInfo( '27.321662', 'day', [ 'sidereal_month', 'lunar_revolution' ], True,
                         '',
                         '''
''' ),

    'moon_volume' :
        RPNConstantInfo( '2.1958e19', 'meter^3', [ 'lunar_volume' ], True,
                         '',
                         '''
''' ),

    'mars_mass' :
        RPNConstantInfo( '6.4191269e23', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'mars_radius' :
        RPNConstantInfo( '3.3962e6', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'mars_revolution' :
        RPNConstantInfo( '686.980', 'day', [  'mars_year' ], True,
                         '',
                         '''
''' ),

    'mars_volume' :
        RPNConstantInfo( '1.6318e20', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_mass' :
        RPNConstantInfo( '1.8983e27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_radius' :
        RPNConstantInfo( '7.1492e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_revolution' :
        RPNConstantInfo( '11.862', 'year', [ 'jupiter_year' ], True,
                         '',
                         '''
''' ),

    'jupiter_volume' :
        RPNConstantInfo( '1.43128e24', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'saturn_mass' :
        RPNConstantInfo( '5.6836e26', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'saturn_radius' :
        RPNConstantInfo( '6.0268e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'saturn_revolution' :
        RPNConstantInfo( '29.457', 'year', [ 'saturn_year' ], True,
                         '',
                         '''
''' ),

    'saturn_volume' :
        RPNConstantInfo( '8.2713e23', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'uranus_mass' :
        RPNConstantInfo( '8.6816e25', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'uranus_radius' :
        RPNConstantInfo( '2.5559e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'uranus_revolution' :
        RPNConstantInfo( '84.011', 'year', [ 'uranus_year' ], True,
                         '',
                         '''
''' ),

    'uranus_volume' :
        RPNConstantInfo( '6.833e22', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'neptune_mass' :
        RPNConstantInfo( '1.0242e26', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'neptune_radius' :
        RPNConstantInfo( '2.4764e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'neptune_revolution' :
        RPNConstantInfo( '164.79', 'year', [ 'neptune_year' ], True,
                         '',
                         '''
''' ),

    'neptune_volume' :
        RPNConstantInfo( '6.254e22', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'pluto_mass' :
        RPNConstantInfo( '1.0303e22', 'kilogram', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_radius' :
        RPNConstantInfo( '1.185e6', 'meter', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_revolution' :
        RPNConstantInfo( '247.94', 'year', [ 'pluto_year' ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_volume' :
        RPNConstantInfo( '6.97e18', 'meter^3', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    # settings constants
    'default' :
        RPNConstantInfo( '-1', '', [ ], False,
                         '\'default\' simply evaluates to -1',
                         '''
used with settings operators

''' ),

    'false' :
        RPNConstantInfo( 0, '', [ ], False,
                         '\'false\' simply evaluates to 0',
                         '''
used with boolean settings operators

''' ),

    'true' :
        RPNConstantInfo( 1, '', [ ], False,
                         '\'true\' simply evaluates to 1',
                         '''
used with boolean settings operators

rpn (1)>5 12 **
244140625
rpn (2)>true comma
1
rpn (3)>5 12 **
244,140,625
''' ),

    # day of week constants
    'monday' :
        RPNConstantInfo( 1, '', [ 'mon' ], False,
                         '',
                         '''
This is defined for convenience for use with date operators.
''' ),

    'tuesday' :
        RPNConstantInfo( 2, '', [ 'tue', 'tues' ], False,
                         '',
                         '''
''' ),

    'wednesday' :
        RPNConstantInfo( 3, '', [ 'wed' ], False,
                         '',
                         '''
''' ),

    'thursday' :
        RPNConstantInfo( 4, '', [ 'thu', 'thur','thurs' ], False,
                         '',
                         '''
''' ),

    'friday' :
        RPNConstantInfo( 5, '', [ 'fri' ], False,
                         '',
                         '''
''' ),

    'saturday' :
        RPNConstantInfo( 6, '', [ 'sat' ], False,
                         '',
                         '''
''' ),

    'sunday' :
        RPNConstantInfo( 7, '', [ ], False,
                         '',
                         '''
''' ),

    # month constants
    'january' :
        RPNConstantInfo( 1, '', [ 'jan' ], False,
                         '',
                         '''
''' ),

    'february' :
        RPNConstantInfo( 2, '', [ 'feb' ],  False,
                         '',
                         '''
''' ),

    'march' :
        RPNConstantInfo( 3, '', [ 'mar' ], False,
                         '',
                         '''
''' ),

    'april' :
        RPNConstantInfo( 4, '', [ 'apr' ], False,
                         '',
                         '''
''' ),

    'may' :
        RPNConstantInfo( 5, '', [ ], False,
                         '',
                         '''
''' ),

    'june' :
        RPNConstantInfo( 6, '', [ 'jun' ], False,
                         '',
                         '''
''' ),

    'july' :
        RPNConstantInfo( 7, '', [ 'jul' ], False,
                         '',
                         '''
''' ),

    'august' :
        RPNConstantInfo( 8, '', [ 'aug' ], False,
                         '',
                         '''
''' ),

    'september' :
        RPNConstantInfo( 9, '', [ 'sep' ], False,
                         '',
                         '''
''' ),

    'october' :
        RPNConstantInfo( 10, '', [ 'oct' ], False,
                         '',
                         '''
''' ),

    'november' :
        RPNConstantInfo( 11, '', [ 'nov' ], False,
                         '',
                         '''
''' ),

    'december' :
        RPNConstantInfo( 12, '', [ 'dec' ], False,
                         '',
                         '''
''' ),

    # programming integer constants
    'max_char' :
        RPNConstantInfo( ( 1 << 7 ) - 1, '', [ 'maxchar', 'max_int8', 'maxint8' ], False,
                         'the maximum 8-bit signed integer',
                         '''
This is the largest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''' ),

    'max_double' :
        RPNConstantInfo( getMaxDouble( ), '', [ 'maxdouble' ], False,
                         'the largest value that can be represented by a 64-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'max_float' :
        RPNConstantInfo( getMaxFloat( ), '', [ 'maxfloat' ], False,
                         'the largest value that can be represented by a 32-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'max_long' :
        RPNConstantInfo( ( 1 << 31 ) - 1, '', [ 'max_int', 'maxint', 'max_int32', 'maxint32', 'maxlong' ], False,
                         'the maximum 32-bit signed integer',
                         '''
This is the largest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''' ),

    'max_longlong' :
        RPNConstantInfo( ( 1 << 63 ) - 1, '', [ 'max_int64', 'maxint64', 'maxlonglong' ], False,
                         'the maximum 64-bit signed integer',
                         '''
This is the largest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''' ),

    'max_quadlong' :
        RPNConstantInfo( ( 1 << 127 ) - 1, '', [ 'max_int128', 'maxint128', 'max_quad', 'maxquad', 'maxquadlong' ], False,
                         'the maximum 128-bit signed integer',
                         '''
This is the largest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''' ),

    'max_short' :
        RPNConstantInfo( ( 1 << 15 ) - 1, '', [ 'max_int16', 'maxint16', 'maxshort' ], False,
                         'the maximum 16-bit signed integer',
                         '''
This is the largest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''' ),

    'max_uchar' :
        RPNConstantInfo( ( 1 << 8 ) - 1, '', [ 'max_uint8', 'maxuint8', 'maxuchar' ], False,
                         'the maximum 8-bit unsigned integer',
                         '''
This is the largest number that can be represented by an 8-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ulong' :
        RPNConstantInfo( ( 1 << 32 ) - 1, '', [ 'max_uint32', 'maxuint32', 'max_uint', 'maxuint', 'maxulong' ], False,
                         'the maximum 32-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 32-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ulonglong' :
        RPNConstantInfo( ( 1 << 64 ) - 1, '', [ 'max_uint64', 'maxuint64', 'maxulonglong' ], False,
                         'the maximum 64-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 64-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_uquadlong' :
        RPNConstantInfo( ( 1 << 128 ) - 1, '', [ 'max_uint128', 'maxuint128', 'maxuquadlong' ], False,
                         'the maximum 128-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 128-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ushort' :
        RPNConstantInfo( ( 1 << 16 ) - 1, '', [ 'max_uint16', 'maxuint16', 'maxushort' ], False,
                         'the maximum 16-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 16-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_char' :
        RPNConstantInfo( -( 1 << 7 ), '', [ 'min_int8', 'minint8', 'minchar' ], False,
                         'the minimum 8-bit signed integer',
                         '''
This is the smallest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''' ),

    'min_double' :
        RPNConstantInfo( getMinDouble( ), '', [ 'mindouble' ], False,
                         'the smallest value that can be represented by a 64-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'min_float' :
        RPNConstantInfo( getMinFloat( ), '', [ 'minfloat' ], False,
                         'the smallest value that can be represented by a 32-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'min_long' :
        RPNConstantInfo( -( 1 << 31 ), '', [ 'min_int32', 'minint32', 'minlong' ], False,
                         'the minimum 32-bit signed integer',
                         '''
This is the smallest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''' ),

    'min_longlong' :
        RPNConstantInfo( -( 1 << 63 ), '', [ 'min_int64', 'minint64', 'minlonglong' ], False,
                         'the minimum 64-bit signed integer',
                         '''
This is the smallest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''' ),

    'min_quadlong' :
        RPNConstantInfo( -( 1 << 127 ), '', [ 'min_int128', 'minint128', 'min_quad', 'minquad', 'minquadlong' ], False,
                         'the minimum 128-bit signed integer',
                         '''
This is the smallest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''' ),

    'min_short' :
        RPNConstantInfo( -( 1 << 15 ), '', [ 'min_int16', 'minint16', 'minshort' ], False,
                         'the minimum 16-bit signed integer',
                         '''
This is the smallest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''' ),

    'min_uchar' :
        RPNConstantInfo( 0, '', [ 'min_uint8', 'minuint8', 'minuchar' ], False,
                         'the minimum 8-bit unsigned integer',
                         '''
This is the smallest number that can be represented by an 8-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ulong' :
        RPNConstantInfo( 0, '', [ 'min_uint32', 'minuint32', 'minulong' ], False,
                         'the minimum 32-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 32-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ulonglong' :
        RPNConstantInfo( 0, '', [ 'min_uint64', 'minuint64', 'minulonglong' ], False,
                         'the minimum 64-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 64-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_uquadlong' :
        RPNConstantInfo( 0, '', [ 'min_uint128', 'minuint128', 'min_quad', 'minquad', 'minquadlong' ], False,
                         'the minimum 128-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 128-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ushort' :
        RPNConstantInfo( 0, '', [ 'min_uint16', 'minuint16', 'minushort' ], False,
                         'the minimum 16-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 16-bit unsigned
integer assuming two's complement representation.
''' ),
}


# //******************************************************************************
# //
# //  unitOperators
# //
# //  unit name : unitType, representation, plural, abbrev,
# //              aliases, categories,
# //              description
# //
# //  When unit types are multiplied in compound units, they need to be
# //  specified in alphabetical order in the name, but not the representations.
# //
# //******************************************************************************

unitOperators = {
    # _null_type - used internally
    '_null_unit' :
        RPNUnitInfo( '_null_type', '', '', '',
                     [ ], [ ],
                     '''
''' ),

    # acceleration
    'galileo' :
        RPNUnitInfo( 'acceleration', 'galileo', 'galileos', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'leo' :
        RPNUnitInfo( 'acceleration', 'leo', 'leos', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'meter/second^2' :
        RPNUnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),


    # amount of substance
    'mole' :
        RPNUnitInfo( 'amount_of_substance', 'mole', 'mole', 'mol',
                     [ 'einstein', 'einsteins' ], [ 'SI' ],
                     '''
''' ),

    # angle
    'arcminute' :
        RPNUnitInfo( 'angle', 'arcminute', 'arcminutes', '',
                     [ 'arcmin', 'arcmins' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'arcsecond' :
        RPNUnitInfo( 'angle', 'arcsecond', 'arcseconds', '',
                     [ 'arcsec', 'arcsecs' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'centrad' :
        RPNUnitInfo( 'angle', 'centrad', 'centrads', '',
                     [ ], [ 'mathematics', 'science' ],
                     '''
''' ),

    'circle' :
        RPNUnitInfo( 'angle', 'circle', 'circles', '',
                     [ ], [ 'mathematics' ],
                     '''
The whole circle, all 360 degrees.
''' ),

    'degree' :
        RPNUnitInfo( 'angle', 'degree', 'degrees', 'deg',
                     [ ], [ 'astronomy', 'mathematics', 'traditional' ],
                     '''
The traditional degree, 1/360th of a circle.
''' ),

    'furman' :
        RPNUnitInfo( 'angle', 'furman', 'furmans', '',
                     [ ], [ 'non-standard' ],
                     '''
From https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement#Furman:

The Furman is a unit of angular measure equal to 1/65,536 of a circle, or just
under 20 arcseconds.  It is named for Alan T. Furman, the American
mathematician who adapted the CORDIC algorithm for 16-bit fixed-point
arithmetic sometime around 1980.
''' ),

    'grad' :
        RPNUnitInfo( 'angle', 'grad', 'grads', '',
                     [ 'gon', 'gons' ], [ 'mathematics' ],
                     '''
''' ),

    'octant' :
        RPNUnitInfo( 'angle', 'octant', 'octants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'pointangle' :
        RPNUnitInfo( 'angle', 'pointangle', 'pointangles', '',
                     [ ], [ 'navigation' ],
                     '''
''' ),

    'quadrant' :
        RPNUnitInfo( 'angle', 'quadrant', 'quadrants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'quintant' :
        RPNUnitInfo( 'angle', 'quintant', 'quintants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'radian' :
        RPNUnitInfo( 'angle', 'radian', 'radians', '',
                     [ ], [ 'mathematics', 'SI' ],
                     '''
''' ),

    'sextant' :
        RPNUnitInfo( 'angle', 'sextant', 'sextants', '',
                     [ 'flat', 'flats' ], [ 'mathematics' ],
                     '''
''' ),

    'streck' :
        RPNUnitInfo( 'angle', 'streck', 'strecks', '',
                     [ ], [ 'Sweden' ],
                     '''
''' ),

    # area
    'acre' :
        RPNUnitInfo( 'area', 'acre', 'acres', 'ac',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'are' :
        RPNUnitInfo( 'area', 'are', 'ares', 'a',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'barn' :
        RPNUnitInfo( 'area', 'barn', 'barns', '',
                     [ 'bethe', 'bethes', 'oppenheimer', 'oppenheimers' ], [ 'science' ],
                     '''
''' ),

    'bovate' :
        RPNUnitInfo( 'area', 'bovate', 'bovates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'carucate' :
        RPNUnitInfo( 'area', 'carucate', 'carucates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'foot^2' :
        RPNUnitInfo( 'area', 'foot^2', 'foot^2', '',
                     [ 'sqft', 'sq_ft', 'square_ft', 'square_foot', 'square_feet', 'sq_foot', 'sq_feet', 'sqfoot', 'sqfeet' ], [ 'imperial' ],
                     '''
''' ),

    'homestead' :
        RPNUnitInfo( 'area', 'homestead', 'homesteads', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'imperial_square' :
        RPNUnitInfo( 'area', 'imperial_sqaure', 'imperial_squares', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'meter^2' :
        RPNUnitInfo( 'area', 'meter^2', 'meter^2', '',
                     [ 'sqm', 'sq_m', 'square_m', 'square_meter', 'square_meters', 'sq_meter', 'sq_meters', 'sqmeter', 'sqmeters' ], [ 'SI' ],
                     '''
''' ),

    'morgen' :
        RPNUnitInfo( 'area', 'morgen', 'morgens', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'nanoacre' :
        RPNUnitInfo( 'area', 'nanoacre', 'nanoacres', 'nac',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'outhouse' :
        RPNUnitInfo( 'area', 'outhouse', 'outhouse', '',
                     [ ], [ 'science', 'humorous' ],
                     '''
''' ),

    'rood' :
        RPNUnitInfo( 'area', 'rood', 'roods', '',
                     [ 'farthingdale' ], [ 'imperial' ],
                     '''
''' ),

    'section' :
        RPNUnitInfo( 'area', 'section', 'sections', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'shed' :
        RPNUnitInfo( 'area', 'shed', 'sheds', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'township' :
        RPNUnitInfo( 'area', 'township', 'townships', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'virgate' :
        RPNUnitInfo( 'area', 'virgate', 'virgates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    # capacitance

    '1/hertz*ohm' :
        RPNUnitInfo( 'capacitance', '1/hertz*ohm', '1/hertz*ohm', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'abfarad' :
        RPNUnitInfo( 'capacitance', 'abfarad', 'abfarads', 'abF',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'ampere*second/volt' :
        RPNUnitInfo( 'capacitance', 'ampere*second/volt', 'ampere*second/volt', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'coulomb^2/joule' :
        RPNUnitInfo( 'capacitance', 'coulomb^2/joule', 'coulomb^2/joule', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'coulomb^2/meter*newton' :
        RPNUnitInfo( 'capacitance', 'coulomb^2/newton*meter', 'coulomb^2/newton*meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'coulomb/volt' :
        RPNUnitInfo( 'capacitance', 'coulomb/volt', 'coulombs/volt', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'farad' :
        RPNUnitInfo( 'capacitance', 'farad', 'farads', 'F',
                     [ ], [ 'SI' ],
                     '''
The SI unit for capacitance.
''' ),

    'jar' :
        RPNUnitInfo( 'capacitance', 'jar', 'jars', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'joule/volt^2' :
        RPNUnitInfo( 'capacitance', 'joule/volt^2', 'joule/volt^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'meter*newton/volt^2' :
        RPNUnitInfo( 'capacitance', 'newton*meter/volt^2', 'newton*meter/volt^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second/ohm' :
        RPNUnitInfo( 'capacitance', 'second/ohm', 'second/ohm', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'coulomb^2*second^2/kilogram*meter^2' :
        RPNUnitInfo( 'capacitance', 'second^2*coulomb^2/meter^2*kilogram', 'second^2*coulomb^2/meter^2*kilogram', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second^2/henry' :
        RPNUnitInfo( 'capacitance', 'second^2/henry', 'second^2/henry', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'ampere^2*second^4/kilogram*meter^2' :
        RPNUnitInfo( 'capacitance', 'second^4*ampere^2/meter^2*kilogram', 'second^4*ampere^2/meter^2*kilogram', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statfarad' :
        RPNUnitInfo( 'capacitance', 'statfarad', 'statfarads', 'statF',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'second*watt/volt^2' :
        RPNUnitInfo( 'capacitance', 'watt*second/volt^2', 'watt*second/volt^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # charge
    'abcoulomb' :
        RPNUnitInfo( 'charge', 'abcoulomb', 'abcoulombs', 'abC',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'ampere*second' :
        RPNUnitInfo( 'charge', 'ampere*second', 'ampere*seconds', 'As',
                     [ 'second*ampere', 'second*amperes' ], [ 'SI' ],
                     '''
''' ),

    'coulomb' :
        RPNUnitInfo( 'charge', 'coulomb', 'coulombs', 'C',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'farad*volt' :
        RPNUnitInfo( 'charge', 'farad*volt', 'farad*volts', 'FV',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'franklin' :
        RPNUnitInfo( 'charge', 'franklin', 'franklins', 'Fr',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'faraday' :
        RPNUnitInfo( 'charge', 'faraday', 'faradays', 'Fd',
                     [ ], [ 'natural' ],   # electron_charge * Avogradro's number!
                     '''
''' ),

    'joule/volt' :
        RPNUnitInfo( 'charge', 'joule/volt', 'joule/volt', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statcoulomb' :
        RPNUnitInfo( 'charge', 'statcoulomb', 'statcoulombs', 'statC',
                     [ 'esu_charge' ], [ 'CGS' ],
                     '''
''' ),

# constant - Constant is a special type that is immediately converted to a numerical value when used.
#            It's not intended to be used as a unit, per se.  Also, these units are in order of their
#            value instead of alphabetical order like all the others
    'decillionth' :
        RPNUnitInfo( 'constant', 'decillionth', 'decillionths', '',
                     [ ], [ 'constant' ],
                     '''
One decillionth:  10e-33 or 1/1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'nonillionth' :
        RPNUnitInfo( 'constant', 'nonillionth', 'nonillionths', '',
                     [ ], [ 'constant' ],
                     '''
One nonillionth:  10e-30 or 1/1,000,000,000,000,000,000,000,000,000,000
''' ),

    'octillionth' :
        RPNUnitInfo( 'constant', 'octillionth', 'octillionths', '',
                     [ ], [ 'constant' ],
                     '''
One octillionth:  10e-27 or 1/1,000,000,000,000,000,000,000,000,000
''' ),

    # 'y' can't be used here since it's an operator
    'septillionth' :
        RPNUnitInfo( 'constant', 'septillionth', 'septillionths', '',
                     [ 'yocto' ], [ 'constant' ],
                     '''
One septillionth:  10e-24 or 1/1,000,000,000,000,000,000,000,000
''' ),

    # 'z' can't be used here since it's an operator
    'sextillionth' :
        RPNUnitInfo( 'constant', 'sextillionth', 'sextillionths', '',
                     [ 'zepto' ], [ 'constant' ],
                     '''
One sextillionth:  10e-21 or 1/1,000,000,000,000,000,000,000
''' ),

    # 'a' can't be used here since it's used for 'are'
    'quintillionth' :
        RPNUnitInfo( 'constant', 'quintillionth', 'quintillionths', '',
                     [ 'atto' ], [ 'constant' ],
                     '''
One quintillionth:  10e-18 or 1/1,000,000,000,000,000,000
''' ),

    'quadrillionth' :
        RPNUnitInfo( 'constant', 'quadrillionth', 'quadrillionths', 'f',
                     [ 'femto' ], [ 'constant' ],
                     '''
One quadrillionth:  10e-15 or 1/1,000,000,000,000,000
''' ),

    'trillionth' :
        RPNUnitInfo( 'constant', 'trillionth', 'trillionths', 'p',
                     [ 'pico' ], [ 'constant' ],
                     '''
One trillionth:  10e-12 or 1/1,000,000,000,000
''' ),

    'billionth' :
        RPNUnitInfo( 'constant', 'billionth', 'billionths', 'n',
                     [ 'nano' ], [ 'constant' ],
                     '''
One billionth:  10e-9 or 1/1,000,000,000
''' ),

    'millionth' :
        RPNUnitInfo( 'constant', 'millionth', 'millionths', 'u',
                     [ 'micro' ], [ 'constant' ],
                     '''
One millionth:  10e-6 or 1/1,000,000
''' ),

    # 'm' can't be used here since it's used for 'meter'
    'thousandth' :
        RPNUnitInfo( 'constant', 'thousandth', 'thousandths', '',
                     [ 'milli' ], [ 'constant' ],
                     '''
One thousandth:  10e-3 or 1/1,000
''' ),

    'percent' :
        RPNUnitInfo( 'constant', 'percent', 'percent', '%',
                     [ 'hundredth', 'centi' ], [ 'constant' ],
                     '''
One hundredth:  10e-2 or 1/100
''' ),

    'tenth' :
        RPNUnitInfo( 'constant', 'tenth', 'tenths', '',
                     [ 'deci', 'tithe' ], [ 'constant' ],
                     '''
One tenth:  10e-1 or 1/10
''' ),

    'quarter' :
        RPNUnitInfo( 'constant', 'quarter', 'quarters', '',
                     [ 'fourth', 'fourths' ], [ 'constant' ],
                     '''
One quarter:  1/4 or 0.25
''' ),

    'third' :
        RPNUnitInfo( 'constant', 'third', 'thirds', '',
                     [ ], [ 'constant' ],
                     '''
One third:  1/3 or 0.333333...
''' ),

    'half' :
        RPNUnitInfo( 'constant', 'half', 'halves', '',
                     [ ], [ 'constant' ],
                     '''
One half:  1/2 or 0.5
''' ),

    'unity' :
        RPNUnitInfo( 'constant', 'x unity', 'x unity', '',
                     [ 'one', 'ones' ], [ 'constant' ],
                     '''
Unity, one, 1
''' ),

    'two' :
        RPNUnitInfo( 'constant', 'two', 'twos', '',
                     [ 'pair', 'pairs' ], [ 'constant' ],
                     '''
two, 2
''' ),

    'three' :
        RPNUnitInfo( 'constant', 'three', 'threes', '',
                     [ ], [ 'constant' ],
                     '''
three, 3
''' ),

    'four' :
        RPNUnitInfo( 'constant', 'four', 'fours', '',
                     [ ], [ 'constant' ],
                     '''
four, 4
''' ),

    'five' :
        RPNUnitInfo( 'constant', 'five', 'fives', '',
                     [ ], [ 'constant' ],
                     '''
five, 5
''' ),

    'six' :
        RPNUnitInfo( 'constant', 'six', 'sixes', '',
                     [ ], [ 'constant' ],
                     '''
six, 6
''' ),

    'seven' :
        RPNUnitInfo( 'constant', 'seven', 'sevens', '',
                     [ ], [ 'constant' ],
                     '''
seven, 7
''' ),

    'eight' :
        RPNUnitInfo( 'constant', 'eight', 'eights', '',
                     [ ], [ 'constant' ],
                     '''
eight, 8
''' ),

    'nine' :
        RPNUnitInfo( 'constant', 'nine', 'nines', '',
                     [ ], [ 'constant' ],
                     '''
nine, 9
''' ),

    'ten' :
        RPNUnitInfo( 'constant', 'ten', 'tens', '',
                     [ 'deca', 'deka', 'dicker', 'dickers' ], [ 'constant' ],
                     '''
Ten:  10e1, or 10
''' ),

    'eleven' :
        RPNUnitInfo( 'constant', 'eleven', 'elevens', '',
                     [ ], [ 'constant' ],
                     '''
eleven, 11
''' ),

    'dozen' :
        RPNUnitInfo( 'constant', 'dozen', 'dozen', '',
                     [ 'twelve', 'twelves' ], [ 'constant' ],
                     '''
A dozen is 12.
''' ),

    'bakers_dozen' :
        RPNUnitInfo( 'constant', 'bakers_dozen', 'bakers_dozens', '',
                     [ 'thirteen', 'thirteens' ], [ 'constant' ],
                     '''
A baker's dozen is 13.
''' ),

    'fourteen' :
        RPNUnitInfo( 'constant', 'fourteen', 'fourteens', '',
                     [ ], [ 'constant' ],
                     '''
fourteen, 14
''' ),

    'fifteen' :
        RPNUnitInfo( 'constant', 'fifteen', 'fifteens', '',
                     [ ], [ 'constant' ],
                     '''
fifteen, 15
''' ),

    'sixteen' :
        RPNUnitInfo( 'constant', 'sixteen', 'sixteens', '',
                     [ ], [ 'constant' ],
                     '''
sixteen, 16
''' ),

    'seventeen' :
        RPNUnitInfo( 'constant', 'seventeen', 'seventeens', '',
                     [ ], [ 'constant' ],
                     '''
seventeen, 17
''' ),

    'eighteen' :
        RPNUnitInfo( 'constant', 'eighteen', 'eighteens', '',
                     [ ], [ 'constant' ],
                     '''
eighteen, 18
''' ),

    'nineteen' :
        RPNUnitInfo( 'constant', 'nineteen', 'nineteens', '',
                     [ ], [ 'constant' ],
                     '''
nineteen, 19
''' ),

    'score' :
        RPNUnitInfo( 'constant', 'score', 'score', '',
                     [ 'twenty', 'twenties' ], [ 'constant' ],
                     '''
A score is 20.
''' ),

    'thirty' :
        RPNUnitInfo( 'constant', 'thirty', 'thirties', '',
                     [ ], [ 'constant' ],
                     '''
thirty, 30
''' ),

    'flock' :
        RPNUnitInfo( 'constant', 'flock', 'flocks', '',
                     [ 'forty', 'forties' ], [ 'constant', 'obsolete' ],
                     '''
A flock is an archaic name for 40.
''' ),

    'fifty' :
        RPNUnitInfo( 'constant', 'fifty', 'fifties', '',
                     [ ], [ 'constant' ],
                     '''
fifty, 50
''' ),

    'shock' :
        RPNUnitInfo( 'constant', 'shock', 'shocks', '',
                     [ 'shook', 'shooks', 'sixty', 'sixties' ], [ 'constant', 'obsolete' ],
                     '''
A shock is an archaic name for 60.
''' ),

    'seventy' :
        RPNUnitInfo( 'constant', 'seventy', 'seventies', '',
                     [ ], [ 'constant' ],
                     '''
seventy, 70
''' ),

    'eighty' :
        RPNUnitInfo( 'constant', 'eighty', 'eighties', '',
                     [ ], [ 'constant' ],
                     '''
eighty, 80
''' ),

    'ninety' :
        RPNUnitInfo( 'constant', 'ninety', 'nineties', '',
                     [ ], [ 'constant' ],
                     '''
ninety, 90
''' ),

    'hundred' :
        RPNUnitInfo( 'constant', 'hundred', 'hundred', '',
                     [ 'hecto', 'toncount', 'toncounts' ], [ 'constant' ],
                     '''
One hundred:  10e2, or 100
''' ),

    'long_hundred' :
        RPNUnitInfo( 'constant', 'long_hundred', 'long_hundreds', '',
                     [ ], [ 'constant', 'obsolete' ],
                     '''
\'long\' hundred is an archaic term for 120.
''' ),

    'gross' :
        RPNUnitInfo( 'constant', 'gross', 'gross', '',
                     [ ], [ 'constant' ],
                     '''
A gross is a dozen dozen, or 144.
''' ),

    'thousand' :
        RPNUnitInfo( 'constant', 'thousand', 'thousand', 'k',
                     [ 'kilo', 'chiliad' ], [ 'constant' ],
                     '''
One thousand:  10e3, or 1,000
''' ),

    'great_gross' :
        RPNUnitInfo( 'constant', 'great_gross', 'great_gross', '',
                     [ ], [ 'constant' ],
                     '''
A great gross is a dozen gross, or 1728.
''' ),

    'million' :
        RPNUnitInfo( 'constant', 'million', 'million', 'M',
                     [ 'mega' ], [ 'constant' ],
                     '''
One million:  10e6 or 1,000,000
''' ),

    # 'G' can't be used here since it's used for 'standard gravity'
    'billion' :
        RPNUnitInfo( 'constant', 'billion', 'billion', '',
                     [ 'giga', 'gigas', 'milliard', 'milliards' ], [ 'constant' ],
                     '''
One billion:  10e9 or 1,000,000,000
''' ),

    # 'T' can't be used here since it's used for 'tesla'
    'trillion' :
        RPNUnitInfo( 'constant', 'trillion', 'trillion', '',
                     [ 'tera' ], [ 'constant' ],
                     '''
One trillion:  10e12 or 1,000,000,000,000
''' ),

    # 'P' can't be used here since it's used for 'Phosphorus'
    'quadrillion' :
        RPNUnitInfo( 'constant', 'quadrillion', 'quadrillion', '',
                     [ 'peta', 'petas', 'billiard', 'billiards' ], [ 'constant' ],
                     '''
One quadrillion:  10e15 or 1,000,000,000,000,000
''' ),

    'quintillion' :
        RPNUnitInfo( 'constant', 'quintillion', 'quintillion', 'E',
                     [ 'exa' ], [ 'constant' ],
                     '''
One quintillion:  10e18 or 1,000,000,000,000,000,000
''' ),

    'sextillion' :
        RPNUnitInfo( 'constant', 'sextillion', 'sextillion', 'Z',
                     [ 'zetta', 'zettas', 'trilliard', 'trilliards' ], [ 'constant' ],
                     '''
One sextillion:  10e21 or 1,000,000,000,000,000,000,000
''' ),

    # 'Y' can't be used here since it's used for 'Yttrium'
    'septillion' :
        RPNUnitInfo( 'constant', 'septillion', 'septillion', '',
                     [ 'yotta' ], [ 'constant' ],
                     '''
One septillion:  10e24 or 1,000,000,000,000,000,000,000,000
''' ),

    'octillion' :
        RPNUnitInfo( 'constant', 'octillion', 'octillion', '',
                     [ ], [ 'constant' ],
                     '''
One octillion:  10e27 or 1,000,000,000,000,000,000,000,000,000
''' ),

    'nonillion' :
        RPNUnitInfo( 'constant', 'nonillion', 'nonillion', '',
                     [ ], [ 'constant' ],
                     '''
One nonillion:  10e30 or 1,000,000,000,000,000,000,000,000,000,000
''' ),

    'decillion' :
        RPNUnitInfo( 'constant', 'decillion', 'decillion', '',
                     [ ], [ 'constant' ],
                     '''
One decillion:  10e33 or 1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'undecillion' :
        RPNUnitInfo( 'constant', 'undecillion', 'undecillion', '',
                     [ ], [ 'constant' ],
                     '''
One undecillion:  10e36
''' ),

    'duodecillion' :
        RPNUnitInfo( 'constant', 'duodecillion', 'duodecillion', '',
                     [ ], [ 'constant' ],
                     '''
One duodecillion:  10e39
''' ),

    'tredecillion' :
        RPNUnitInfo( 'constant', 'tredecillion', 'tredecillion', '',
                     [ ], [ 'constant' ],
                     '''
One tredecillion:  10e42
''' ),

    'quattuordecillion' :
        RPNUnitInfo( 'constant', 'quattuordecillion', 'quattuordecillion', '',
                     [ ], [ 'constant' ],
                     '''
One quattuordecillion:  10e45
''' ),

    'quindecillion' :
        RPNUnitInfo( 'constant', 'quindecillion', 'quindecillion', '',
                     [ 'quinquadecillion' ], [ 'constant' ],
                     '''
One quindecillion:  10e48
''' ),

    'sexdecillion' :
        RPNUnitInfo( 'constant', 'sexdecillion', 'sexdecillion', '',
                     [ ], [ 'constant' ],
                     '''
One sexdecillion:  10e51
''' ),

    'septendecillion' :
        RPNUnitInfo( 'constant', 'septemdecillion', 'septemdecillion', '',
                     [ ], [ 'constant' ],
                     '''
One septendecillion:  10e54
''' ),

    'octodecillion' :
        RPNUnitInfo( 'constant', 'octodecillion', 'octodecillion', '',
                     [ ], [ 'constant' ],
                     '''
One octodecillion:  10e57
''' ),

    'novemdecillion' :
        RPNUnitInfo( 'constant', 'novemdecillion', 'novemdecillion', '',
                     [ 'novendecillion' ], [ 'constant' ],
                     '''
One novemdecillion:  10e60
''' ),

    'vigintillion' :
        RPNUnitInfo( 'constant', 'vigintillion', 'vigintillion', '',
                     [ ], [ 'constant' ],
                     '''
One vigintdecillion:  10e63
''' ),

    'googol' :
        RPNUnitInfo( 'constant', 'googol', 'googols', '',
                     [ ], [ 'constant' ],
                     '''
One googol:  10e100 or ten duotrigintillion, famously named in 1920 by
9-year-old Milton Sirotta.
''' ),

    'centillion' :
        RPNUnitInfo( 'constant', 'centillion', 'centillion', '',
                     [ ], [ 'constant' ],
                     '''
One centillion:  10e303
''' ),

    # current
    'abampere' :
        RPNUnitInfo( 'current', 'abampere', 'abamperes', 'abA',
                     [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ],
                     '''
''' ),

    'ampere' :
        RPNUnitInfo( 'current', 'ampere', 'amperes', 'A',
                     [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ],
                     '''
''' ),

    'coulomb/second' :
        RPNUnitInfo( 'current', 'coulomb/second', 'coulombs/second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statampere' :
        RPNUnitInfo( 'current', 'statampere', 'statamperes', 'statA',
                     [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ],
                     '''
''' ),

    'watt/volt' :
        RPNUnitInfo( 'current', 'watt/volt', 'watt/volt', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # data_rate
    'bit/second' :
        RPNUnitInfo( 'data_rate', 'bit/second', 'bits/second', 'bps',
                     [ 'bips' ], [ 'computing' ],
                     '''
''' ),

    'byte/second' :
        RPNUnitInfo( 'data_rate', 'byte/second', 'bytes/second', 'Bps',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc1' :
        RPNUnitInfo( 'data_rate', 'oc1', 'x_oc1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc3' :
        RPNUnitInfo( 'data_rate', 'oc3', 'x_oc3', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc12' :
        RPNUnitInfo( 'data_rate', 'oc12', 'x_oc12', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc24' :
        RPNUnitInfo( 'data_rate', 'oc24', 'x_oc24', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc48' :
        RPNUnitInfo( 'data_rate', 'oc48', 'x_oc24', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc192' :
        RPNUnitInfo( 'data_rate', 'oc192', 'x_oc192', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc768' :
        RPNUnitInfo( 'data_rate', 'oc768', 'x_oc768', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb1' :
        RPNUnitInfo( 'data_rate', 'usb1', 'x_usb1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb2' :
        RPNUnitInfo( 'data_rate', 'usb2', 'x_usb2', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.0' :
        RPNUnitInfo( 'data_rate', 'usb3.0', 'x_usb3.0', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.1' :
        RPNUnitInfo( 'data_rate', 'usb3.1', 'x_usb3.1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    # density
    'kilogram/liter' :
        RPNUnitInfo( 'density', 'kilogram/liter', 'kilograms/liter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram/meter^3' :
        RPNUnitInfo( 'density', 'kilogram/meter^3', 'kilograms/meter^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # dynamic_viscosity

    # pound per foot hour                 lb/(ft*h)    1 lb/(ft*h)   = 4.133 789e-4 Pa*s
    # pound per foot second               lb/(ft*s)    1 lb/(ft*s)   = 1.488164 Pa*s
    # pound-force second per square foot  lbf*s/ft2    1 lbf*s/ft2   = 47.88026 Pa*s
    # pound-force second per square inch  lbf*s/in2    1 lbf*s/in2   = 6,894.757 Pa*s

    'kilogram/meter*second' :
        RPNUnitInfo( 'dynamic_viscosity', 'kilogram/meter*second', 'kilogram/meter*second', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'newton*second/meter^2' :
        RPNUnitInfo( 'dynamic_viscosity', 'newton*second/meter^2', 'newton*second/meter^2', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'pascal*second' :
        RPNUnitInfo( 'dynamic_viscosity', 'pascal*second', 'pascal*seconds', 'Pas',
                     [ 'poiseuille', 'poiseuilles' ], [ 'SI' ],
                     '''
''' ),

    'poise' :
        RPNUnitInfo( 'dynamic_viscosity', 'poise', 'poise', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'reynolds' :
        RPNUnitInfo( 'dynamic_viscosity', 'reynolds', 'reynolds', '',
                     [ 'reyn', 'reyns' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_conductance
    'abmho' :
        RPNUnitInfo( 'electrical_conductance', 'abmho', 'abmhos', '',
                     [ 'absiemens' ], [ 'CGS' ],
                     '''
''' ),

    'ampere/volt' :
        RPNUnitInfo( 'electrical_conductance', 'ampere/volt', 'amperes/volt', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'conductance_quantum' :
        RPNUnitInfo( 'electrical_conductance', 'conductance_quantum', 'conductance_quanta', 'G0',
                     [ ], [ 'SI' ],
                     '''
The conductance quantum appears when measuring the conductance of a quantum
point contact, and, more generally, is a key component of Landauer formula
which relates the electrical conductance of a quantum conductor to its quantum
properties.  It is twice the reciprocal of the von Klitzing constant (2/RK).

https://en.wikipedia.org/wiki/Conductance_quantum
''' ),

    'ampere^2*second^3/kilogram*meter^2':
        RPNUnitInfo( 'electrical_conductance', 'ampere^2*second^3/kilogram*meter^2', 'ampere^2*second^3/kilogram*meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'coulomb^2*second/kilogram*meter^2' :
        RPNUnitInfo( 'electrical_conductance', 'coulomb^2*second/kilogram*meter^2', 'coulomb^2*second/kilogram*meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'siemens' :
        RPNUnitInfo( 'electrical_conductance', 'siemens', 'siemens', 'S',
                     [ 'mho', 'mhos' ], [ 'SI' ],
                     '''
''' ),

    'statmho' :
        RPNUnitInfo( 'electrical_conductance', 'statmho', 'statmhos', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'statsiemens' :
        RPNUnitInfo( 'electrical_conductance', 'statsiemens', 'statsiemens', 'statS',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # electric_potential
    'abvolt' :
        RPNUnitInfo( 'electric_potential', 'abvolt', 'abvolts', 'abV',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # ampere*ohm

    'coulomb/farad' :
        RPNUnitInfo( 'electric_potential', 'coulomb/farad', 'coulombs/farad', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # joule/coulomb
    # meter*newton/coulomb
    # kilogram*meter^2/ampere*second^3

    'volt' :
        RPNUnitInfo( 'electric_potential', 'volt', 'volts', 'V',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'watt/ampere' :
        RPNUnitInfo( 'electric_potential', 'watt/ampere', 'watts/ampere', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statvolt' :
        RPNUnitInfo( 'electric_potential', 'statvolt', 'statvolts', 'statV',
                     [ 'esu_potential' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_resistance
    '1/siemens' :
        RPNUnitInfo( 'electrical_resistance', '1/siemens', '1/siemens', '',
                     [ '1/mho' ], [ 'SI' ],
                     '''
''' ),

    'abohm' :
        RPNUnitInfo( 'electrical_resistance', 'abohm', 'abohms', 'o',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'german_mile' :
        RPNUnitInfo( 'electrical_resistance', 'german_mile', 'german_miles', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'jacobi' :
        RPNUnitInfo( 'electrical_resistance', 'jacobi', 'jacobis', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'joule*second/coulomb^2' :
        RPNUnitInfo( 'electrical_resistance', 'joule*second/coulomb^2', 'joule*second/coulomb^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'joule/ampere^2*second' :
        RPNUnitInfo( 'electrical_resistance', 'joule/ampere^2*second', 'joule/ampere^2*second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^3' :
        RPNUnitInfo( 'electrical_resistance', 'kilogram*meter^2/ampere^2*second^3', 'kilogram*meter^2/ampere^2*second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # kilogram*meter^2/coulomb^2*second

    'matthiessen' :
        RPNUnitInfo( 'electrical_resistance', 'matthiessen', 'matthiessens', '',
                     [ ], [ 'obsolete' ],   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),

    'ohm' :
        RPNUnitInfo( 'electrical_resistance', 'ohm', 'ohms', 'O',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second/farad' :
        RPNUnitInfo( 'electrical_resistance', 'second/farad', 'second/farad', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statohm' :
        RPNUnitInfo( 'electrical_resistance', 'statohm', 'statohms', 'statO',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'varley' :
        RPNUnitInfo( 'electrical_resistance', 'varley', 'varleys', '',
                     [ ], [ 'obsolete' ],  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),

    'volt/ampere' :
        RPNUnitInfo( 'electrical_resistance', 'volt/ampere', 'volts/ampere', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # volt^2/watt

    'watt/ampere^2' :
        RPNUnitInfo( 'electrical_resistance', 'watt/ampere^2', 'watts/ampere^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # energy
    'ampere*second*volt' :
        RPNUnitInfo( 'energy', 'ampere*second*volt', 'ampere*second*volt', 'AVs',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'btu' :
        RPNUnitInfo( 'energy', 'BTU', 'BTUs', '', [ 'btu', 'btus' ],
                     [ 'England', 'US' ],
                     '''
''' ),

    'calorie' :
        RPNUnitInfo( 'energy', 'calorie', 'calories', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'electron-volt' :
        RPNUnitInfo( 'energy', 'electron-volt', 'electron-volts', 'eV',
                     [ 'electronvolt', 'electronvolts' ], [ 'science' ],
                     '''
''' ),

    'erg' :
        RPNUnitInfo( 'energy', 'erg', 'ergs', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'foe' :
        RPNUnitInfo( 'energy', 'foe', 'foes', '',
                     [ 'bethe', 'bethes' ], [ 'astrophysics' ],
                     '''
A foe is a unit of energy equal to 10^44 joules or 10^51 ergs, used to measure
the large amount of energy released by a supernova.  The word is an acronym
derived from the phrase [ten to the power of] fifty-one ergs.  It was coined
by Gerald Brown of Stony Brook University in his work with Hans Bethe, because
"it came up often enough in our work".
''' ),

    'gram-equivalent' :
        RPNUnitInfo( 'energy', 'gram-equivalent', 'grams-equivalent', 'gE',
                     [ 'gram-energy', 'grams-energy', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ],
                     '''
''' ),

    'hartree' :
        RPNUnitInfo( 'energy', 'hartree', 'hartrees', 'Eh',
                     [ ], [ 'science' ],
                     '''
''' ),

    'horsepower*second' :
        RPNUnitInfo( 'energy', 'horsepower*second', 'horsepower*seconds', 'hps',
                     [ 'second*horsepower' ], [ 'US' ],
                     '''
''' ),

    'joule' :
        RPNUnitInfo( 'energy', 'joule', 'joules', 'J',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/second^2' :
        RPNUnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'meter*newton' :
        RPNUnitInfo( 'energy', 'meter*newton', 'meter*newtons', '',
                     [ 'newton*meter', 'newton*meters' ], [ 'SI' ],
                     '''
''' ),

    'meter^3*pascal' :
        RPNUnitInfo( 'energy', 'meter^3*pascal', 'meter^3*pascal', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pound_of_TNT' :
        RPNUnitInfo( 'energy', 'pound_of_TNT', 'pounds_of_TNT', 'pTNT',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'quad' :
        RPNUnitInfo( 'energy', 'quad', 'quads', '',
                     [ ], [ 'US' ],
                     '''
A quad is a unit of energy equal to 10^15 (a short-scale quadrillion) BTU, or
1.055e18 joules (1.055 exajoules or EJ) in SI units.  The unit is used by
the U.S. Department of Energy in discussing world and national energy budgets.
The global primary energy production in 2004 was 446 quad, equivalent to 471 EJ.

(https://en.wikipedia.org/wiki/Quad_%28unit%29)
''' ),

    'rydberg' :
        RPNUnitInfo( 'energy', 'rydberg', 'rydbergs', 'Ry',
                     [ ], [ 'science' ],
                     '''
''' ),

    'therm' :
        RPNUnitInfo( 'energy', 'therm', 'therms', '',
                     [ 'thm' ], [ 'England', 'US' ],
                     '''
The therm (symbol thm) is a non-SI unit of heat energy equal to 100,000
British thermal units (BTU).  It is approximately the energy equivalent of
burning 100 cubic feet (often referred to as 1 CCF) of natural gas.

(https://en.wikipedia.org/wiki/Therm)
''' ),

    'toe' :
        RPNUnitInfo( 'energy', 'toe', 'toes', '',
                     [ 'tonne_of_oil_equivalent', 'tonnes_of_oil_equivalent' ], [ 'international' ],
                     '''
"Toe" is a symbol for tonne of oil equivalent, a unit of energy used in the
international energy industry.  One toe represents the energy available from
burning approximately one tonne (metric ton) of crude oil; this is defined by
the International Energy Agency to be exactly 10^7 kilocalories, equivalent to
approximately 7.4 barrels of oil, 1270 cubic meters of natural gas, or 1.4
tonnes of coal. 1 toe is also equivalent to 41.868 gigajoules (GJ), 39.683
million Btu (MM Btu) or dekatherms, or 11.630 megawatt hours (MWh).

http://www.unc.edu/~rowlett/units/dictT.html
''' ),

    'ton_of_coal' :
        RPNUnitInfo( 'energy', 'ton_of_coal', 'tons_of_coal', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'ton_of_TNT' :
        RPNUnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'coulomb*volt' :
        RPNUnitInfo( 'energy', 'volt*coulomb', 'volt*coulomb', 'VC',
                     [ 'coulomb*volt', 'coulomb*volts' ], [ 'SI' ],
                     '''
''' ),

    'second*watt' :
        RPNUnitInfo( 'energy', 'watt*second', 'watt*seconds', 'Ws',
                     [ 'second*watt', 'second*watts' ], [ 'SI' ],
                     '''
''' ),

    # force
    'ampere*weber/meter' :
        RPNUnitInfo( 'force', 'ampere*weber/meter', 'ampere*weber/meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'dyne' :
        RPNUnitInfo( 'force', 'dyne', 'dynes', 'dyn',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'gram-force' :
        RPNUnitInfo( 'force', 'gram-force', 'grams-force', 'g-m',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'joule/meter' :
        RPNUnitInfo( 'force', 'joule/meter', 'joule/meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter/second^2' :
        RPNUnitInfo( 'force', 'kilogram*meter/second^2', 'kilogram*meter/second^2', '',
                     [ ], [ 'SI' ],
                     '''
This is the definition of the SI derived unit Newton (N).
''' ),

    'newton' :
        RPNUnitInfo( 'force', 'newton', 'newtons', 'N',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pond' :
        RPNUnitInfo( 'force', 'pond', 'ponds', '',
                     [ ], [ 'metric' ],
                     '''
''' ),

    'pound-force' :
        RPNUnitInfo( 'force', 'pound-force', 'pound-force', '',
                     [ ], [ 'FPS' ],
                     '''
''' ),

    'poundal' :
        RPNUnitInfo( 'force', 'poundal', 'poundals', 'pdl',
                     [ ], [ 'England' ],
                     '''
''' ),

    'sthene' :
        RPNUnitInfo( 'force', 'sthene', 'sthenes', 'sn',
                     [ 'funal' ], [ 'MTS' ],
                     '''
''' ),

    # frequency
    '1/second' :
        RPNUnitInfo( 'frequency', '1/second', '1/second', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'every_minute' :
        RPNUnitInfo( 'frequency', 'x_every_minute', 'x_every_minute', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'every_second' :
        RPNUnitInfo( 'frequency', 'x_every_second', 'x_every_second', '',
                     [ '' ], [ 'traditional' ],
                     '''
''' ),

    'hertz' :
        RPNUnitInfo( 'frequency', 'hertz', 'hertz', 'Hz',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'hourly' :
        RPNUnitInfo( 'frequency', 'x_hourly', 'x_hourly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'daily' :
        RPNUnitInfo( 'frequency', 'x_daily', 'x_daily', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'weekly' :
        RPNUnitInfo( 'frequency', 'x_weekly', 'x_weekly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'monthly' :
        RPNUnitInfo( 'frequency', 'x_monthly', 'x_monthly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'yearly' :
        RPNUnitInfo( 'frequency', 'x_yearly', 'x_yearly', '',
                     [ 'annually' ], [ 'traditional' ],
                     '''
''' ),

    'becquerel' :
        RPNUnitInfo( 'frequency', 'becquerel', 'becquerels', 'Bq',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'curie' :
        RPNUnitInfo( 'frequency', 'curie', 'curies', 'Ci',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'rutherford' :
        RPNUnitInfo( 'frequency', 'rutherford', 'rutherfords', 'rd',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    # illuminance
    'flame' :
        RPNUnitInfo( 'illuminance', 'flame', 'flame', '',
                     [ ], [ '' ],
                     '''
''' ),

    'footcandle' :
        RPNUnitInfo( 'illuminance', 'footcandle', 'footcandles', 'fc',
                     [ ], [ 'FPS' ],
                     '''
''' ),

    'lux' :
        RPNUnitInfo( 'illuminance', 'lux', 'lux', 'lx',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'lumen/meter^2' :
        RPNUnitInfo( 'illuminance', 'lumen/meter^2', 'lumens/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'lumen/foot^2' :
        RPNUnitInfo( 'illuminance', 'lumen/foot^2', 'lumens/foot^2', '',
                     [ ], [ 'FPS' ],
                     '''
''' ),

    'nox' :
        RPNUnitInfo( 'illuminance', 'nox', 'nox', 'nx',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'phot' :
        RPNUnitInfo( 'illuminance', 'phot', 'phots', 'ph',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # inductance
    'abhenry' :
        RPNUnitInfo( 'inductance', 'abhenry', 'abhenries', 'abH',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'henry' :
        RPNUnitInfo( 'inductance', 'henry', 'henries', 'H',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'joule/ampere^2' :
        RPNUnitInfo( 'inductance', 'joule/ampere^2', 'joule/ampere^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/coulomb^2' :
        RPNUnitInfo( 'inductance', 'kilogram*meter^2/coulomb^2', 'kilogram*meter^2/coulomb^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^2' :
        RPNUnitInfo( 'inductance', 'kilogram*meter^2/second^2*ampere^2', 'kilogram*meter^2/second^2*ampere^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'ohm*second' :
        RPNUnitInfo( 'inductance', 'ohm*second', 'ohm*second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'ohm/hertz' :
        RPNUnitInfo( 'inductance', 'ohm/hertz', 'ohm/hertz', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second^2/farad' :
        RPNUnitInfo( 'inductance', 'second^2/farad', 'second^2/farad', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'stathenry' :
        RPNUnitInfo( 'inductance', 'stathenry', 'stathenries', 'statH',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # meter^2*tesla/ampere
    # second*volt/ampere

    'weber/ampere' :
        RPNUnitInfo( 'inductance', 'weber/ampere', 'webers/ampere', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # information_entropy
    'ban' :
        RPNUnitInfo( 'information_entropy', 'ban', 'bans', '',
                     [ 'hartley', 'hartleys', 'dit', 'dits' ], [ 'IEC' ],
                     '''
''' ),

    'bit' :
        RPNUnitInfo( 'information_entropy', 'bit', 'bits', 'b',
                     [ 'shannon', 'shannons' ], [ 'computing' ],
                     '''
A 'binary digit', which can store two values.
''' ),

    'byte' :
        RPNUnitInfo( 'information_entropy', 'byte', 'bytes', 'B',
                     [ 'octet', 'octets' ], [ 'computing' ],
                     '''
The traditional unit of computer storage, whose value has varied over the years
and on different platforms, but is now commonly defined to be 8 bits in size.
''' ),

    'btupf' :
        RPNUnitInfo( 'information_entropy', 'btupf', 'btupf', '',
                     [ ], [ 'England' ],
                     '''
''' ),

    'clausius' :
        RPNUnitInfo( 'information_entropy', 'clausius', 'clausius', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'dword' :
        RPNUnitInfo( 'information_entropy', 'dword', 'dwords', '',
                     [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ],
                     '''
A 'double-word' consisting of 2 16-bits words, or 32 bits total.
''' ),

    'joule/kelvin' :
        RPNUnitInfo( 'information_entropy', 'joule/kelvin', 'joules/kelvin', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/kelvin*second^2' :
        RPNUnitInfo( 'information_entropy', 'kilogram*meter^2/kelvin*second^2', 'kilogram*meter^2/kelvin*second^2', '',
                     [ ], [ 'physics' ],
                     '''
This is the unit of the Boltzmann constant.
''' ),

    'library_of_congress' :
        RPNUnitInfo( 'information_entropy', 'library_of_congress', 'x_library_of_congress', 'LoC',
                     [ 'congress', 'congresses', 'loc' ], [ 'computing' ],
                     '''
An informal unit of information measurement based on the contents of the U.S.
Library of Congress, estimated to be the equivalent of 10 terabytes in size.
''' ),

    'nibble' :
        RPNUnitInfo( 'information_entropy', 'nibble', 'nibbles', '',
                     [ 'nybble', 'nybbles' ], [ 'computing' ],
                     '''
A nybble is a half-byte, or 4 bits.  A nybble can be represented by a single
hexadecimal digit.
''' ),

    'nat' :
        RPNUnitInfo( 'information_entropy', 'nat', 'nats', '',
                     [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ],
                     '''
''' ),

    'nyp' :
        RPNUnitInfo( 'information_entropy', 'nyp', 'nyps', '',
                     [ ], [ 'computing' ],   # suggested by Donald Knuth
                     '''
A nyp is a term suggested by Knuth to represent two bits.  It is not a
commonly used term.
''' ),

    'oword' :
        RPNUnitInfo( 'information_entropy', 'oword', 'owords', '',
                     [ 'octaword', 'octawords', 'octoword', 'octowords' ], [ 'computing' ],
                     '''
An 'octo-word' consisting of 8 16-bit words or 128 bits total.
''' ),

    'qword' :
        RPNUnitInfo( 'information_entropy', 'qword', 'qwords', '',
                     [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ],
                     '''
A 'quad-word' consisting of 4 16-bit words, or 64 bits total.
''' ),

    'trit' :
        RPNUnitInfo( 'information_entropy', 'trit', 'trits', '',
                     [ ], [ 'computing' ],
                     '''
A trit is a 'ternary digit', by extension from the term 'bit' for 'binary
digit'.  In 1958 the Setun balanced ternary computer was developed at Moscow
State University, which used trits and 6-trit trytes.
''' ),

    'tryte' :
        RPNUnitInfo( 'information_entropy', 'tryte', 'trytes', '',
                     [ ], [ 'computing' ],
                     '''
A tryte consists of 6 trits (i.e., 'ternary digits'), and is named by extension
from the term 'byte'.  In 1958 the Setun balanced ternary computer was
developed at Moscow State University, which used trits and 6-trit trytes.
''' ),

    'word' :
        RPNUnitInfo( 'information_entropy', 'word', 'words', '',
                     [ 'short_integer', 'short_integers', 'short_int', 'short_ints', 'wyde' ], [ 'computing' ],
                     '''
A word is traditionally two bytes, or 16 bits.  The term 'wyde' was suggested
by Knuth.
''' ),

    # jerk
    'meter/second^3' :
        RPNUnitInfo( 'jerk', 'meter/second^3', 'meter/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'stapp' :
        RPNUnitInfo( 'jerk', 'stapp', 'stapps', '',
                     [ ], [ 'SI' ],
                     '''
The stapp a unit used to express the effects of acceleration or deceleration on
the human body.  One stapp represents an acceleration of 1 g for a period of 1
second, or 9.80665 meters per second per second for 1 second.  The unit is
named for the U.S. Air Force physician John P. Stapp (1910-1999), a pioneer in
research on the human effects of acceleration during the 1940s and 1950s.

http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    # jounce
    'meter/second^4' :
        RPNUnitInfo( 'jounce', 'meter/second^4', 'meter/second^4', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # length
    'aln' :
        RPNUnitInfo( 'length', 'aln', 'alns', '',
                     [ 'alen', 'alens' ], [ 'obsolete' ],
                     '''
''' ),

    'angstrom' :
        RPNUnitInfo( 'length', 'angstrom', 'angstroms', 'A',
                     [ 'angstroem', 'angstroems' ], [ 'science' ],
                     '''
''' ),

    'arpent' :
        RPNUnitInfo( 'length', 'arpent', 'arpents', '',
                     [ ], [ 'obsolete', 'France' ],
                     '''
''' ),

    'arshin' :
        RPNUnitInfo( 'length', 'arshin', 'arshins', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'astronomical_unit' :
        RPNUnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au',
                     [ ], [ 'science' ],
                     '''
''' ),

    'barleycorn' :
        RPNUnitInfo( 'length', 'barleycorn', 'barleycorns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'bolt' :
        RPNUnitInfo( 'length', 'bolt', 'bolts', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'caliber' :
        RPNUnitInfo( 'length', 'caliber', 'caliber', '',
                     [ 'calibre' ], [ 'US' ],
                     '''
''' ),

    'chain' :
        RPNUnitInfo( 'length', 'chain', 'chains', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'cicero' :
        RPNUnitInfo( 'length', 'cicero', 'ciceros', '',
                     [ ], [ 'typography', 'obsolete' ],
                     '''
''' ),

    'cubit' :
        RPNUnitInfo( 'length', 'cubit', 'cubits', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'diuym' :
        RPNUnitInfo( 'length', 'diuym', 'diuyms', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ell' :
        RPNUnitInfo( 'length', 'ell', 'ells', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'famn' :
        RPNUnitInfo( 'length', 'famn', 'famns', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'farshimmelt_potrzebie' :
        RPNUnitInfo( 'length', 'farshimmelt_potrzebie', 'farshimmelt_potrzebies', 'fpz',
                     [ 'far-potrzebie', 'far-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fathom' :
        RPNUnitInfo( 'length', 'fathom', 'fathoms', 'fath',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'finger' :
        RPNUnitInfo( 'length', 'finger', 'fingers', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'fingerbreadth' :
        RPNUnitInfo( 'length', 'fingerbreadth', 'fingerbreadths', '',
                     [ 'fingersbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'foot' :
        RPNUnitInfo( 'length', 'foot', 'feet', 'ft',
                     [ ], [ 'traditional', 'FPS' ],
                     '''
''' ),

    'french' :
        RPNUnitInfo( 'length', 'french', 'French', '',
                     [ 'french_gauge', 'french_scale', 'charrier' ], [ 'France' ],
                     '''
The French scale or French gauge system is commonly used to measure the size of
a catheter.  It is most often abbreviated as Fr, but can often be seen
abbreviated as Fg, Ga, FR or F.  It may also be abbreviated as CH or Ch (for
Charriere, its inventor).

https://en.wikipedia.org/wiki/French_catheter_scale
''' ),

    'furlong' :
        RPNUnitInfo( 'length', 'furlong', 'furlongs', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'furshlugginer_potrzebie' :
        RPNUnitInfo( 'length', 'furshlugginer_potrzebie', 'furshlugginer_potrzebies', 'Fpz',
                     [ 'fur-potrzebie', 'fur-potrzebies', 'Fur-potrzebie', 'Fur-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fut' :
        RPNUnitInfo( 'length', 'fut', 'futs', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'greek_cubit' :
        RPNUnitInfo( 'length', 'greek_cubit', 'greek_cubits', '',
                     [ ], [ 'obsolete', 'Greece' ],
                     '''
''' ),

    'gutenberg' :
        RPNUnitInfo( 'length', 'gutenberg', 'gutenbergs', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'hand' :
        RPNUnitInfo( 'length', 'hand', 'hands', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'handbreadth' :
        RPNUnitInfo( 'length', 'handbreadth', 'handbreadths', '',
                     [ 'handsbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'hubble' :
        RPNUnitInfo( 'length', 'hubble', 'hubbles', '',
                     [ ], [ 'astronomy' ],
                     '''
''' ),

    'inch' :
        RPNUnitInfo( 'length', 'inch', 'inches', 'in',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'ken' :
        RPNUnitInfo( 'length', 'ken', 'kens', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'kosaya_sazhen' :
        RPNUnitInfo( 'length', 'kosaya_sazhen', 'kosaya_sazhens', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'kyu' :
        RPNUnitInfo( 'length', 'kyu', 'kyus', '',
                     [ 'Q' ], [ 'typography', 'computing' ],
                     '''
''' ),

    'league' :
        RPNUnitInfo( 'length', 'league', 'leagues', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'light-second' :
        RPNUnitInfo( 'length', 'light-second', 'light-seconds', '',
                      [ ], [ 'science' ],
                     '''
''' ),

    'light-year' :
        RPNUnitInfo( 'length', 'light-year', 'light-years', 'ly',
                     [ 'a1' ], [ 'science' ],
                     '''
''' ),

    'liniya' :
        RPNUnitInfo( 'length', 'liniya', 'liniya', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'link' :
        RPNUnitInfo( 'length', 'link', 'links', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'long_cubit' :
        RPNUnitInfo( 'length', 'long_cubit', 'long_cubits', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'long_reed' :
        RPNUnitInfo( 'length', 'long_reed', 'long_reeds', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'marathon' :
        RPNUnitInfo( 'length', 'marathon', 'marathons', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'mezhevaya_versta' :
        RPNUnitInfo( 'length', 'mezhevaya_versta', 'mezhevaya_verstas', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'meter' :
        RPNUnitInfo( 'length', 'meter', 'meters', 'm',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'metric_foot' :
        RPNUnitInfo( 'length', 'metric_foot', 'metric_feet', '',
                     [ ], [ 'UK', 'unofficial' ],
                     '''
''' ),

    'micron' :
        RPNUnitInfo( 'length', 'micron', 'microns', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'mil' :
        RPNUnitInfo( 'length', 'mil', 'mils', '',
                     [ 'thou' ], [ 'US' ],
                     '''
''' ),

    'mile' :
        RPNUnitInfo( 'length', 'mile', 'miles', 'mi',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'nail' :
        RPNUnitInfo( 'length', 'nail', 'nails', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'nautical_mile' :
        RPNUnitInfo( 'length', 'nautical_mile', 'nautical_miles', '',
                     [ ], [ 'nautical' ],
                     '''
''' ),

    'parsec' :
        RPNUnitInfo( 'length', 'parsec', 'parsecs', 'pc',
                     [ ], [ 'science' ],
                     '''
''' ),

    'perch' :
        RPNUnitInfo( 'length', 'perch', 'perches', '',
                     [ 'pole', 'poles' ], [ 'imperial' ],
                     '''
''' ),

    'pica' :
        RPNUnitInfo( 'length', 'pica', 'picas', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'point' :
        RPNUnitInfo( 'length', 'point', 'points', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'poppyseed' :
        RPNUnitInfo( 'length', 'poppyseed', 'poppyseeds', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'pyad' :
        RPNUnitInfo( 'length', 'pyad', 'pyads', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'rack_unit' :
        RPNUnitInfo( 'length', 'rack_unit', 'rack_units', '',
                     [ ], [ 'computers' ],
                     '''
A rack unit (abbreviated U or RU) is a unit of measure defined as 44.50
millimetres (1.752 in).  It is most frequently used as a measurement of the
overall height of 19-inch and 23-inch rack frames, as well as the height of
equipment that mounts in these frames, whereby the height of the frame or
equipment is expressed as multiples of rack units.

https://en.wikipedia.org/wiki/Rack_unit
''' ),

    'reed' :
        RPNUnitInfo( 'length', 'reed', 'reeds', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'rod' :
        RPNUnitInfo( 'length', 'rod', 'rods', 'rd',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'rope' :
        RPNUnitInfo( 'length', 'rope', 'ropes', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'potrzebie' :
        RPNUnitInfo( 'length', 'potrzebie', 'potrzebies', 'pz',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'sazhen' :
        RPNUnitInfo( 'length', 'sazhen', 'sazhens', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'siriometer' :
        RPNUnitInfo( 'length', 'siriometer', 'siriometers', '',
                     [ ], [ 'science' ],  # proposed in 1911 by Cark V. L. Charlier
                     '''
''' ),

    'skein' :
        RPNUnitInfo( 'length', 'skein', 'skeins', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'smoot' :
        RPNUnitInfo( 'length', 'smoot', 'smoots', '',
                     [ ], [ 'humorous' ],
                     '''
''' ),

    'span' :
        RPNUnitInfo( 'length', 'span', 'spans', '',
                     [ 'breadth' ], [ 'imperial' ],
                     '''
''' ),

    'stadium' :
        RPNUnitInfo( 'length', 'stadium', 'stadia', '',
                     [ ], [ 'Rome' ],
                     '''
''' ),

    'twip' :
        RPNUnitInfo( 'length', 'twip', 'twips', 'twp',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'vershok' :
        RPNUnitInfo( 'length', 'vershok', 'vershoks', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'versta' :
        RPNUnitInfo( 'length', 'versta', 'verstas', '',
                     [ 'verst', 'versts' ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'yard' :
        RPNUnitInfo( 'length', 'yard', 'yards', 'yd',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    # luminance
    'apostilb' :
        RPNUnitInfo( 'luminance', 'apostilb', 'apostilbs', 'asb',
                     [ 'blondel', 'blondels' ], [ 'CGS' ],
                     '''
''' ),

    'bril' :
        RPNUnitInfo( 'luminance', 'bril', 'brils', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'candela/meter^2' :
        RPNUnitInfo( 'luminance', 'candela/meter^2', 'candelas/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'footlambert' :
        RPNUnitInfo( 'luminance', 'footlambert', 'footlamberts', '',
                     [ 'foot*lambert', 'foot*lamberts', 'feet*lambert' ], [ 'US', 'obsolete' ],
                     '''
''' ),

    'lambert' :
        RPNUnitInfo( 'luminance', 'lambert', 'lamberts', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'nit' :
        RPNUnitInfo( 'luminance', 'nit', 'nits', 'nt',
                     [ 'meterlambert', 'meter*lambert', 'meterlamberts', 'meter*lamberts' ], [ 'obsolete' ],
                     '''
''' ),

    'skot' :
        RPNUnitInfo( 'luminance', 'skot', 'skots', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'stilb' :
        RPNUnitInfo( 'luminance', 'stilb', 'stilbs', 'sb',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # luminous_flux
    'lumen' :
        RPNUnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'candela*steradian' :
        RPNUnitInfo( 'luminous_flux', 'candela*steradian', 'candela*steradians', '',
                     [ 'cd*sr', 'steradian*candela', 'steradian*candelas' ], [ 'SI' ],
                     '''
''' ),

    # luminous_intensity
    'candela' :
        RPNUnitInfo( 'luminous_intensity', 'candela', 'candelas', 'cd',
                     [ 'candle', 'candles', 'bougie', 'bougies' ], [ 'SI' ],
                     '''
''' ),

    'hefnerkerze' :
        RPNUnitInfo( 'luminous_intensity', 'hefnerkerze', 'hefnerkerze', 'HK',
                     [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    # magnetic_field_strength
    'ampere/meter' :
        RPNUnitInfo( 'magnetic_field_strength', 'ampere/meter', 'amperes/meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'oersted' :
        RPNUnitInfo( 'magnetic_field_strength', 'oersted', 'oersted', 'Oe',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # magnetic_flux
    'centimeter^2*gauss' :
        RPNUnitInfo( 'magnetic_flux', 'centimeter^2*gauss', 'centimeter^2*gauss', '',
                     [ 'gauss*centimeter^2' ], [ 'CGS' ],
                     '''
''' ),

    # kilogram*meter^2/ampere*second^2
    # joule/ampere

    'maxwell' :
        RPNUnitInfo( 'magnetic_flux', 'maxwell', 'maxwells', 'Mx',
                     [ 'line', 'lines' ], [ 'CGS' ],
                     '''
''' ),

    'meter^2*tesla' :
        RPNUnitInfo( 'magnetic_flux', 'meter^2*tesla', 'meter^2*tesla', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'unit_pole' :
        RPNUnitInfo( 'magnetic_flux', 'unit_pole', 'unit_poles', '',
                     [ 'unitpole', 'unitpoles' ], [ 'CGS' ],
                     '''
''' ),

    'second*volt' :
        RPNUnitInfo( 'magnetic_flux', 'volt*second', 'volt*second', 'Vs',
                     [ 'second*volt', 'second*volts' ], [ 'SI' ],
                     '''
''' ),

    'weber' :
        RPNUnitInfo( 'magnetic_flux', 'weber', 'webers', 'Wb',
                     [ 'promaxwell', 'promaxwells' ], [ 'SI' ],
                     '''
''' ),

    # magnetic_flux_density
    'gauss' :
        RPNUnitInfo( 'magnetic_flux_density', 'gauss', 'gauss', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'ampere*henry/meter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'henry*ampere/meter^2', 'henry*ampere/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'joule/ampere*meter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'joule/ampere*meter^2', 'joule/ampere*meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram/ampere*second^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', 'kilogram/ampere*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram/coulomb*second' :
        RPNUnitInfo( 'magnetic_flux_density', 'kilogram/coulomb*second', 'kilogram/coulomb*second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'maxwell/centimeter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'maxwell/centimeter^2', 'maxwells/centimeter^2', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'newton/ampere*meter' :
        RPNUnitInfo( 'magnetic_flux_density', 'newton/ampere*meter', 'newton/ampere*meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'newton*second/coulomb*meter' :
        RPNUnitInfo( 'magnetic_flux_density', 'newton*second/coulomb*meter', 'newton*second/coulomb*meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second*volt/meter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'second*volt/meter^2', 'second*volt/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'tesla' :
        RPNUnitInfo( 'magnetic_flux_density', 'tesla', 'teslas', 'T',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'second*volt/meter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'volt*second/meter^2', 'volt*second/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),


    'weber/meter^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'weber/meter^2', 'webers/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # mass
    'berkovets' :
        RPNUnitInfo( 'mass', 'berkovets', 'berkovets', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'blintz' :
        RPNUnitInfo( 'mass', 'blintz', 'blintzes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'carat' :
        RPNUnitInfo( 'mass', 'carat', 'carats', 'ct',
                     [ 'karat', 'karats' ], [ 'US' ],
                     '''
''' ),

    'chandrasekhar_limit' :
        RPNUnitInfo( 'mass', 'chandrasekhar_limit', 'x chandrasekhar_limit', '',
                     [ 'chandrasekhar', 'chandrasekhars' ], [ 'science' ],
                     '''
''' ),

    'dalton' :
        RPNUnitInfo( 'mass', 'dalton', 'daltons', '',
                     [ 'amu', 'atomic_mass_unit' ], [ 'science' ],
                     '''
''' ),

    'dolya' :
        RPNUnitInfo( 'mass', 'dolya', 'dolyas', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'doppelzentner' :
        RPNUnitInfo( 'mass', 'doppelzentner', 'doppelzentners', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'farshimmelt_blintz' :
        RPNUnitInfo( 'mass', 'farshimmelt_blintz', 'farshimmelt_blintzes', 'fb',
                     [ 'far-blintz', 'far-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'funt' :
        RPNUnitInfo( 'mass', 'funt', 'funts', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'furshlugginer_blintz' :
        RPNUnitInfo( 'mass', 'furshlugginer_blintz', 'furshlugginer_blintzes', 'Fb',
                     [ 'fur-blintz', 'fur-blintzes', 'Fur-blintz', 'Fur-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'grain' :
        RPNUnitInfo( 'mass', 'grain', 'grains', 'gr',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'gram' :
        RPNUnitInfo( 'mass', 'gram', 'grams', 'g',
                     [ 'gramme', 'grammes' ], [ 'SI' ],
                     '''
''' ),

# hyl, metric_slug, technical_mass_unit, technische_masseseinheit, 9.80665 kg

    'joule*second^2/meter^2' :
        RPNUnitInfo( 'mass', 'joule*second^2/meter^2', 'joule*second^2/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
This conversion is required to do mass-energy equivalence calculations.
''' ),

    'kip' :
        RPNUnitInfo( 'mass', 'kip', 'kips', '',
                     [ 'kilopound', 'kilopounds' ], [ 'US' ],
                     '''
''' ),

    'lot' :
        RPNUnitInfo( 'mass', 'lot', 'lots', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ounce' :
        RPNUnitInfo( 'mass', 'ounce', 'ounces', 'oz',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'pennyweight' :
        RPNUnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt',
                     [ 'pwt' ], [ 'traditional', 'England' ],
                     '''
''' ),

    'pfund' :
        RPNUnitInfo( 'mass', 'pfund', 'pfunds', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'pood' :
        RPNUnitInfo( 'mass', 'pood', 'poods', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'pound' :
        RPNUnitInfo( 'mass', 'pound', 'pounds', 'lb',
                     [ ], [ 'US', 'traditional', 'FPS' ],
                     '''
''' ),

    'quintal' :
        RPNUnitInfo( 'mass', 'quintal', 'quintals', 'q',
                     [ 'cantar', 'cantars' ], [ ],
                     '''
''' ),

    'sheet' :
        RPNUnitInfo( 'mass', 'sheet', 'sheets', '',
                     [ ], [ ],
                     '''
''' ),

    'slinch' :
        RPNUnitInfo( 'mass', 'slinch', 'slinches', '',
                     [ 'mug', 'mugs', 'snail', 'snails' ], [ 'NASA' ],
                     '''
''' ),

    'slug' :
        RPNUnitInfo( 'mass', 'slug', 'slugs', '',
                     [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ],
                     '''
''' ),

    'stone' :
        RPNUnitInfo( 'mass', 'stone', 'stones', '',
                     [ ], [ 'traditional', 'England' ],
                     '''
''' ),

    'stone_us' :
        RPNUnitInfo( 'mass', 'stone_us', 'stones_us', '',
                     [ 'us_stone', 'us_stones' ], [ 'US' ],
                     '''
''' ),

    'ton' :
        RPNUnitInfo( 'mass', 'ton', 'tons', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'tonne' :
        RPNUnitInfo( 'mass', 'tonne', 'tonnes', '',
                     [ 'metric_ton', 'metric_tons' ], [ 'MTS' ],
                     '''
''' ),

    'troy_ounce' :
        RPNUnitInfo( 'mass', 'troy_ounce', 'troy_ounces', 'toz',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'troy_pound' :
        RPNUnitInfo( 'mass', 'troy_pound', 'troy_pounds', '',
                     [ ], [ 'traditional'  ],
                     '''
''' ),

    'wey' :
        RPNUnitInfo( 'mass', 'wey', 'weys', '',
                     [ ], [ 'obsolete', 'England' ],
                     '''
''' ),

    'zentner' :
        RPNUnitInfo( 'mass', 'zentner', 'zentners', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'zolotnik' :
        RPNUnitInfo( 'mass', 'zolotnik', 'zolotniks', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    # power
    'ampere*volt' :
        RPNUnitInfo( 'power', 'ampere*volt', 'ampere*volts', 'VA',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # ampere^2*ohm

    'dBm' :
        RPNUnitInfo( 'power', 'dBm', 'dBm', 'dBm',
                     [ 'dBmW', 'decibel-milliwatt' ], [ 'engineering' ],
                     '''
''' ),

    'erg/second' :
        RPNUnitInfo( 'power', 'erg/second', 'ergs/second', 'erg/s',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'horsepower' :
        RPNUnitInfo( 'power', 'horsepower', 'horsepower', 'hp',
                     [ ], [ 'US' ],
                     '''
''' ),

    'joule/second' :
        RPNUnitInfo( 'power', 'joule/second', 'joules/second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'lusec' :
        RPNUnitInfo( 'power', 'lusec', 'lusecs', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'kilogram*meter^2/second^3' :
        RPNUnitInfo( 'power', 'kilogram*meter^2/second^3', 'kilogram*meter^2/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'meter*newton/second' :
        RPNUnitInfo( 'power', 'meter*newton/second', 'meter*newton/second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pferdestarke' :
        RPNUnitInfo( 'power', 'pferdestarke', 'pferdestarke', 'PS',
                     [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    'poncelet' :
        RPNUnitInfo( 'power', 'poncelet', 'poncelets', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    # volt^2/ohm

    'watt' :
        RPNUnitInfo( 'power', 'watt', 'watts', 'W',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # pressure
    'atmosphere' :
        RPNUnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm',
                     [ ], [ 'natural' ],
                     '''
''' ),

    'bar' :
        RPNUnitInfo( 'pressure', 'bar', 'bars', '',
                     [ ], [ ],
                     '''
''' ),

    'barye' :
        RPNUnitInfo( 'pressure', 'barye', 'baryes', 'Ba',
                     [ 'barad', 'barads' ], [ 'CGS' ],
                     '''
''' ),

    'mmHg' :
        RPNUnitInfo( 'pressure', 'mmHg', 'mmHg', '',
                     [ ], [ 'metric' ],
                     '''
''' ),

    # joule/meter^3

    'kilogram/meter*second^2' :
        RPNUnitInfo( 'pressure', 'kilogram/meter*second^2', 'kilogram/meter*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'newton/meter^2' :
        RPNUnitInfo( 'pressure', 'newton/meter^2', 'newtons/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pascal' :
        RPNUnitInfo( 'pressure', 'pascal', 'pascals', 'Pa',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pieze' :
        RPNUnitInfo( 'pressure', 'pieze', 'piezes', '',
                     [ ], [ 'MTS' ],
                     '''
''' ),

    'psi' :
        RPNUnitInfo( 'pressure', 'pound/inch^2', 'pounds/inch^2', '',
                     [ ], [ 'FPS' ],
                     '''
''' ),

# technical_atmosphere (at) 98.0665 kPa

    'torr' :
        RPNUnitInfo( 'pressure', 'torr', 'torr', '',
                     [ ], [ ],
                     '''
''' ),

    # radiation_dose
    'banana_equivalent_dose' :
        RPNUnitInfo( 'radiation_dose', 'banana_equivalent_dose', 'banana_equivalent_doses', '',
                     [ 'banana', 'bananas' ], [ 'natural', 'informal' ],
                     '''
''' ),

    'gray' :
        RPNUnitInfo( 'radiation_dose', 'gray', 'grays', 'Gy',
                     [ ], [ 'SI' ],   # or should 'Gy' be giga-years?
                     '''
''' ),

    'joule/kilogram' :
        RPNUnitInfo( 'radiation_dose', 'joule/kilogram', 'joules/kilogram', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'rem' :
        RPNUnitInfo( 'radiation_dose', 'rem', 'rems', '',
                     [ 'roentgen_equivalent_man' ], [ 'CGS' ],
                     '''
''' ),

    'sievert' :
        RPNUnitInfo( 'radiation_dose', 'sievert', 'sieverts', 'Sv',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # radiation_exposure
    'coulomb/kilogram' :
        RPNUnitInfo( 'radiation_exposure', 'coulomb/kilogram', 'coulombs/kilogram', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'rad' :
        RPNUnitInfo( 'radiation_exposure', 'rad', 'rads', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'roentgen' :
        RPNUnitInfo( 'radiation_exposure', 'roentgen', 'roentgens', 'R',
                     [ 'parker', 'parkers', 'rep', 'reps' ], [ 'NIST' ],
                     '''
''' ),

    # radiosity
    'kilogram/second^3' :
        RPNUnitInfo( 'radiosity', 'kilogram/second^3', 'kilogram/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'watt/meter^2' :
        RPNUnitInfo( 'radiosity', 'watt/meter^2', 'watt/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # solid_angle
    'hemisphere' :
        RPNUnitInfo( 'solid_angle', 'hemisphere', 'hemisphere', '',
                     [ 'half_sphere', 'half_spheres', 'halfsphere', 'halfspheres' ], [ 'mathematics' ],
                     '''
''' ),

    'radian^2' :
        RPNUnitInfo( 'solid_angle', 'radian^2', 'radian^2', '',
                     [ ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    'sphere' :
        RPNUnitInfo( 'solid_angle', 'sphere', 'spheres', '',
                     [ 'spat', 'spats' ], [ 'mathematics' ],
                     '''
''' ),

    'square_arcminute' :
        RPNUnitInfo( 'solid_angle', 'arcminute^2', 'arcminutes^2', '',
                     [ 'square_arcminutes', 'solid_arcminute', 'solid_arcminutes', 'sq_arcminute', 'sq_arcminutes', 'sqarcmin', 'sqarcmins', 'arcmins^2', 'spherical_minute', 'spherical_minutes' ], [ 'mathematics' ],
                     '''
''' ),

    'square_arcsecond' :
        RPNUnitInfo( 'solid_angle', 'arcsecond^2', 'arcseconds^2', '',
                     [ 'square_arcseconds', 'solid_arcsecond', 'solid_arcseconds', 'sq_arcsecond', 'sq_arcseconds', 'sqarcsec', 'sqarcsecs', 'arcsecs^2', 'spherical_second', 'spherical_seconds' ], [ 'mathematics' ],
                     '''
''' ),

    'square_degree' :
        RPNUnitInfo( 'solid_angle', 'degree^2', 'degrees^2', '',
                     [ 'square_degrees', 'sqdeg', 'solid_degree', 'solid_degrees', 'sq_degree', 'sq_degrees', 'sqdeg', 'sqdegs', 'spherical_degree', 'spherical_degrees' ], [ 'mathematics' ],
                     '''
''' ),

    'square_octant' :
        RPNUnitInfo( 'solid_angle', 'octant^2', 'octants^2', '',
                     [ 'square_octants', 'sqoctant', 'sqoctants', 'solid_octant', 'solid_octants', 'sq_octant', 'sq_octants', 'spherical_octant', 'spherical_octants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_quadrant' :
        RPNUnitInfo( 'solid_angle', 'quadrant^2', 'quadrants^2', '',
                     [ 'square_quadrants', 'sqquadrant', 'sqquadrants', 'solid_quadrant', 'solid_quadrants', 'sq_quadrant', 'sq_quadrants', 'spherical_quadrant', 'spherical_quadrants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_quintant' :
        RPNUnitInfo( 'solid_angle', 'quintant^2', 'quintants^2', '',
                     [ 'square_quintants', 'sqquintant', 'sqquintants', 'solid_quintant', 'solid_quintants', 'sq_quintant', 'sq_quintants', 'spherical_quintant', 'spherical_quintants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_sextant' :
        RPNUnitInfo( 'solid_angle', 'sextant^2', 'sextants^2', '',
                     [ 'square_sextants', 'sqsextant', 'sqsextants', 'solid_sextant', 'solid_sextants', 'sq_sextant', 'sq_sextants', 'spherical_sextant', 'spherical_sextants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_grad' :
        RPNUnitInfo( 'solid_angle', 'grad^2', 'grads^2', '',
                     [ 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'sq_gon', 'sq_gons', 'sqgon', 'sqgons', 'grad^2', 'grads^2', 'gon^2', 'gons^2', 'spherical_gon', 'spherical_gons', 'spherical_grad', 'spherical_grads' ], [ 'mathematics' ],
                     '''
''' ),

    'steradian' :
        RPNUnitInfo( 'solid_angle', 'steradian', 'steradians', 'sr',
                     [ 'square_radian', 'square_radians', 'sq_radian', 'sq_radians', 'sq_rad', 'sqrad', 'spherical_radian', 'spherical_radians' ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    # temperature
    'celsius' :
        RPNUnitInfo( 'temperature', 'celsius', 'degrees_celsius', 'Cel',
                     [ 'centigrade', 'degC', 'degreeC', 'degreesC', 'degree_centigrade', 'degrees_centigrade' ], [ 'SI' ],
                     '''
''' ),

    'degree_newton' :
        RPNUnitInfo( 'temperature', 'degree_newton', 'degrees_newton', '',
                     [ 'degN', 'degreeN', 'degreesN' ], [ 'obsolete' ],
                     '''
''' ),

    'delisle' :
        RPNUnitInfo( 'temperature', 'delisle', 'degrees_delisle', 'De',
                     [ 'degD', 'degreeD', 'degreesD', 'degree_delisle' ], [ 'obsolete' ],
                     '''
''' ),

    'fahrenheit' :
        RPNUnitInfo( 'temperature', 'fahrenheit', 'degrees_fahrenheit', '',
                     [ 'fahr', 'degF', 'degreeF', 'degreesF', 'degree_fahrenheit' ], [ 'US', 'traditional' ],
                     '''
''' ),

    'kelvin' :
        RPNUnitInfo( 'temperature', 'kelvin', 'degrees_kelvin', 'K',
                     [ 'degK', 'degreeK', 'degreesK', 'degree_kelvin' ], [ 'SI' ],
                     '''
''' ),

    'rankine' :
        RPNUnitInfo( 'temperature', 'rankine', 'degrees_rankine', 'R',
                     [ 'degR', 'degreeR', 'degreesR', 'degree_rankine' ], [ 'obsolete' ],
                     '''
''' ),

    'reaumur' :
        RPNUnitInfo( 'temperature', 'reaumur', 'degrees_reaumur', 'Re',
                     [ 'degRe', 'degreeRe', 'degreesRe', 'degree_reaumur' ], [ 'obsolete' ],
                     '''
''' ),

    'romer' :
        RPNUnitInfo( 'temperature', 'romer', 'degrees_romer', 'Ro',
                     [ 'degRo', 'degreeRo', 'degreesRo', 'degree_romer' ], [ 'obsolete' ],
                     '''
''' ),

    # time
    'beat' :
        RPNUnitInfo( 'time', 'beat', 'beat', '',
                     [ ], [ ],
                     '''
''' ),

    'blink' :
        RPNUnitInfo( 'time', 'blink', 'blinks', '',
                     [ 'metric_second', 'metric_seconds' ], [ ],
                     '''
''' ),

    'century' :
        RPNUnitInfo( 'time', 'century', 'centuries', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'clarke' :
        RPNUnitInfo( 'time', 'clarke', 'clarkes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'cowznofski' :
        RPNUnitInfo( 'time', 'cowznofski', 'cowznofskis', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'day' :
        RPNUnitInfo( 'time', 'day', 'days', '', [ 'ephemeris_day' ],
                     [ 'traditional' ],
                     '''
''' ),

    'decade' :
        RPNUnitInfo( 'time', 'decade', 'decades', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'eon' :
        RPNUnitInfo( 'time', 'eon', 'eons', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'fortnight' :
        RPNUnitInfo( 'time', 'fortnight', 'fortnights', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'gregorian_year' :
        RPNUnitInfo( 'time', 'gregorian_year', 'gregorian_years', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'hour' :
        RPNUnitInfo( 'time', 'hour', 'hours', 'hr',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'kovac' :
        RPNUnitInfo( 'time', 'kovac', 'kovacs', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'jiffy' :
        RPNUnitInfo( 'time', 'jiffy', 'jiffies', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'lustrum' :
        RPNUnitInfo( 'time', 'lustrum', 'lustra', '',
                     [ ], [ 'obsolete', 'years' ],
                     '''
''' ),

    'martin' :
        RPNUnitInfo( 'time', 'martin', 'martins', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'microcentury' :
        RPNUnitInfo( 'time', 'microcentury', 'microcenturies', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'microfortnight' :
        RPNUnitInfo( 'time', 'microfortnight', 'microfortnights', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'mingo' :
        RPNUnitInfo( 'time', 'mingo', 'mingoes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'minute' :
        RPNUnitInfo( 'time', 'minute', 'minutes', '',
                     [ ], [ 'traditional' ],  # 'min' is already an operator
                     '''
''' ),

    'month' :
        RPNUnitInfo( 'time', 'month', 'months', 'mo',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'nanocentury' :
        RPNUnitInfo( 'time', 'nanocentury', 'nanocenturies', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'second' :
        RPNUnitInfo( 'time', 'second', 'seconds', 's',
                     [ ], [ 'SI', 'traditional', 'FPS' ],   # 'sec' is already an operator
                     '''
''' ),

    'shake' :
        RPNUnitInfo( 'time', 'shake', 'shakes', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_day' :
        RPNUnitInfo( 'time', 'sidereal_day', 'sidereal_days', '',
                     [ 'earth_day', 'earth_days' ], [ 'science' ],
                     '''
''' ),

    'sidereal_hour' :
        RPNUnitInfo( 'time', 'sidereal_hour', 'sidereal_hours', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_minute' :
        RPNUnitInfo( 'time', 'sidereal_minute', 'sidereal_minutes', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_second' :
        RPNUnitInfo( 'time', 'sidereal_second', 'sidereal_seconds', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'svedberg' :
        RPNUnitInfo( 'time', 'svedberg', 'svedbergs', '',
                     [ ], [ ],
                     '''
''' ),

    'tropical_month' :
        RPNUnitInfo( 'time', 'tropical_month', 'tropical_months', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'week' :
        RPNUnitInfo( 'time', 'week', 'weeks', 'wk', [ 'sennight' ],
                     [ 'traditional' ],
                     '''
''' ),

    'wolverton' :
        RPNUnitInfo( 'time', 'wolverton', 'wolvertons', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'wood' :
        RPNUnitInfo( 'time', 'wood', 'woods', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'year' :
        RPNUnitInfo( 'time', 'year', 'years', '',
                     [ 'annum', 'annums', 'julian_year', 'julian_years', 'twelvemonth', 'twelvemonths' ], [ 'traditional', 'years' ],
                     '''
''' ),

    # velocity
    'bubnoff_unit' :
        RPNUnitInfo( 'velocity', 'bubnoff_unit', 'bubnoff_units', '',
                     [ 'bubnoff', 'bubnoffs' ], [ 'science' ],
                     '''
The Bubnoff unit is employed in geology to measure rates of lowering of earth
surfaces due to erosion and is named after the Russian (German-Baltic)
geologist Serge von Bubnoff (1888-1957).  An erosion speed of 1 B also means
that 1 cubic meter of earth is being removed from an area of 1 square km in 1
year.

https://en.wikipedia.org/wiki/Bubnoff_unit
''' ),

    'kine' :
        RPNUnitInfo( 'velocity', 'kine', 'kine', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'meter/second' :
        RPNUnitInfo( 'velocity', 'meter/second', 'meters/second', 'mps',
                     [ 'benz' ], [ 'SI' ],
                     '''
''' ),

    'knot' :
        RPNUnitInfo( 'velocity', 'knot', 'knots', 'kt',
                     [ ], [ 'nautical' ],
                     '''
''' ),

    'mach' :
        RPNUnitInfo( 'velocity', 'mach', 'mach', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'mile/hour' :
        RPNUnitInfo( 'velocity', 'mile/hour', 'miles/hour', 'mph',
                     [ ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'kilometer/hour' :
        RPNUnitInfo( 'velocity', 'kilometer/hour', 'kilometers/hour', 'kph',
                     [ ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'speed_of_sound' :
        RPNUnitInfo( 'velocity', 'speed_of_sound', 'x speed_of_sound', '',
                     [ ], [ 'natural' ], '',
                     '''
''' ),

    # volume
    'acre*foot' :
        RPNUnitInfo( 'volume', 'acre*foot', 'acre*feet', '',
                     [ ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'balthazar' :
        RPNUnitInfo( 'volume', 'balthazar', 'balthazars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'beer_barrel' :
        RPNUnitInfo( 'volume', 'beer_barrel', 'beer_barrel', '',
                     [ ], [ 'US', 'beer' ],
                     '''
''' ),

    'beer_keg' :
        RPNUnitInfo( 'volume', 'beer_keg', 'beer_kegs', '',
                     [ ], [ 'US', 'beer' ],
                     '''
''' ),

    'bottle' :
        RPNUnitInfo( 'volume', 'bottle', 'bottles', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'bucket' :
        RPNUnitInfo( 'volume', 'bucket', 'buckets', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'bushel' :
        RPNUnitInfo( 'volume', 'bushel', 'bushels', 'bu',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'chopine' :
        RPNUnitInfo( 'volume', 'chopine', 'chopines', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'clavelin' :
        RPNUnitInfo( 'volume', 'clavelin', 'clavelins', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'coffeespoon' :
        RPNUnitInfo( 'volume', 'coffeespoon', 'coffeespoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'coomb' :
        RPNUnitInfo( 'volume', 'coomb', 'coombs', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'cord' :
        RPNUnitInfo( 'volume', 'cord', 'cords', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'foot^3' :
        RPNUnitInfo( 'volume', 'foot^3', 'foot^3', '',
                     [ 'cuft', 'cu_ft', 'cubic_ft', 'cubic_foot', 'cubic_feet', 'cu_foot', 'cu_feet', 'cufoot', 'cufeet'  ], [ 'traditional', 'FPS' ],
                     '''
''' ),

    'cup' :
        RPNUnitInfo( 'volume', 'cup', 'cups', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'dash' :
        RPNUnitInfo( 'volume', 'dash', 'dashes', '',
                    [ ], [ 'cooking' ],
                     '''
''' ),

    'demi' :
        RPNUnitInfo( 'volume', 'demi', 'demis', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'dessertspoon' :
        RPNUnitInfo( 'volume', 'dessertspoon', 'dessertspoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'dram' :
        RPNUnitInfo( 'volume', 'dram', 'drams', '',
                     [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ],
                     '''
''' ),

    'dry_barrel' :
        RPNUnitInfo( 'volume', 'dry_barrel', 'dry_barrels', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'dry_hogshead' :
        RPNUnitInfo( 'volume', 'dry_hogshead', 'dry_hogsheads', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'dry_gallon' :
        RPNUnitInfo( 'volume', 'dry_gallon', 'dry_gallons', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_pint' :
        RPNUnitInfo( 'volume', 'dry_pint', 'dry_pints', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_quart' :
        RPNUnitInfo( 'volume', 'dry_quart', 'dry_quarts', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_tun' :
        RPNUnitInfo( 'volume', 'dry_tun', 'dry_tuns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'farshimmelt_ngogn' :
        RPNUnitInfo( 'volume', 'farshimmelt_ngogn', 'farshimmelt_ngogns', 'fn',
                     [ 'far-ngogn', 'far-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fifth' :
        RPNUnitInfo( 'volume', 'fifth', 'fifths', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'firkin' :
        RPNUnitInfo( 'volume', 'firkin', 'firkins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'fluid_ounce' :
        RPNUnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', '',
                     [ 'floz' ], [ 'traditional' ],
                     '''
''' ),

    'furshlugginer_ngogn' :
        RPNUnitInfo( 'volume', 'furshlugginer_ngogn', 'furshlugginer_ngogns', 'Fn',
                     [ 'Fur-ngogn', 'Fur-ngogns', 'fur-ngogn', 'fur-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'gallon' :
        RPNUnitInfo( 'volume', 'gallon', 'gallons', 'gal',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'gill' :
        RPNUnitInfo( 'volume', 'gill', 'gills', '',
                     [ 'noggin', 'noggins', 'teacup', 'teacups' ], [ 'imperial' ],
                     '''
''' ),

    'goliath' :
        RPNUnitInfo( 'volume', 'goliath', 'goliaths', '',
                     [ 'primat' ], [ 'wine' ],
                     '''
''' ),

    'hogshead' :
        RPNUnitInfo( 'volume', 'hogshead', 'hogsheads', '',
                     [ ], [ 'traditional', 'wine' ],
                     '''
''' ),

    'hoppus_foot' :
        RPNUnitInfo( 'volume', 'hoppus_foot', 'hoppus_feet', '',
                     [ 'hoppus_cube', 'hoppus_cubes' ], [ 'England', 'obsolete' ],
                     '''
The hoppus cubic foot (or 'hoppus cube') was the standard volume measurement
used for timber in the British Empire and countries in the British sphere of
influence before the introduction of metric units.  It is still used in the
hardwood trade of some countries.  This volume measurement was developed to
estimate what volume of a round log would be usable timber after processing,
in effect attempting to 'square' the log and allow for waste.

The English surveyor Edward Hoppus introduced the eponymous unit in his 1736
manual of practical calculations.

Ref:  https://en.wikipedia.org/wiki/Hoppus
''' ),

    'hoppus_ton' :
        RPNUnitInfo( 'volume', 'hoppus_ton', 'hoppus_tons', '',
                     [ ], [ 'England', 'obsolete' ],
                     '''
The hoppus ton (HT) was also a traditionally used unit of volume in British
forestry. One hoppus ton is equal to 50 hoppus feet or 1.8027 cubic metres.
Some shipments of tropical hardwoods, especially shipments of teak from
Myanmar (Burma), are still stated in hoppus tons.

Ref:  https://en.wikipedia.org/wiki/Hoppus
''' ),

    'imperial_bushel' :
        RPNUnitInfo( 'volume', 'imperial_bushel', 'imperial_bushels', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_butt' :
        RPNUnitInfo( 'volume', 'imperial_butt', 'imperial_butts', '',
                     [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_cup' :
        RPNUnitInfo( 'volume', 'imperial_cup', 'imperial_cups', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gallon' :
        RPNUnitInfo( 'volume', 'imperial_gallon', 'imperial_gallons', '',
                     [ 'congius', 'congii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gill' :
        RPNUnitInfo( 'volume', 'imperial_gill', 'imperial_gills', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_hogshead' :
        RPNUnitInfo( 'volume', 'imperial_hogshead', 'imperial_hogsheads', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_peck' :
        RPNUnitInfo( 'volume', 'imperial_peck', 'imperial_pecks', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_pint' :
        RPNUnitInfo( 'volume', 'imperial_pint', 'imperial_pints', '',
                     [ 'octarius', 'octarii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_quart' :
        RPNUnitInfo( 'volume', 'imperial_quart', 'imperial_quarts', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'jack' :
        RPNUnitInfo( 'volume', 'jack', 'jacks', '',
                     [ 'jackpot', 'jackpots' ], [ 'imperial' ],
                     '''
''' ),

    'jennie' :
        RPNUnitInfo( 'volume', 'jennie', 'jennies', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'jeroboam' :
        RPNUnitInfo( 'volume', 'jeroboam', 'jeroboams', '',
                     [ 'double_magnum', 'double_magnums' ], [ 'wine' ],
                     '''
''' ),

    'jigger' :
        RPNUnitInfo( 'volume', 'jigger', 'jiggers', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'kenning' :
        RPNUnitInfo( 'volume', 'kenning', 'kennings', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'kilderkin' :
        RPNUnitInfo( 'volume', 'kilderkin', 'kilderkins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'liter' :
        RPNUnitInfo( 'volume', 'liter', 'liters', 'L',    # The U.S. standard is to use uppercase "L" because the lower case 'l' looks like a 1
                     [ ], [ 'SI' ],
                     '''
''' ),

    'magnum' :
        RPNUnitInfo( 'volume', 'magnum', 'magnums', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'marie_jeanne' :
        RPNUnitInfo( 'volume', 'marie_jeanne', 'marie_jeannes', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'melchior' :
        RPNUnitInfo( 'volume', 'melchior', 'melchiors', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'melchizedek' :
        RPNUnitInfo( 'volume', 'melchizedek', 'melchizedeks', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'meter^3' :
        RPNUnitInfo( 'volume', 'meter^3', 'meter^3', '',
                     [ 'cum', 'cu_m', 'cubic_m', 'cubic_meter', 'cubic_meters', 'cu_meter', 'cu_meters', 'cumeter', 'cumeters' ], [ 'SI' ],
                     '''
''' ),

    'methuselah' :
        RPNUnitInfo( 'volume', 'methuselah', 'methuselahs', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'minim' :
        RPNUnitInfo( 'volume', 'minim', 'minims', 'gtt',
                     [ 'drop' ], [ 'traditional' ],
                     '''
''' ),

    'mordechai' :
        RPNUnitInfo( 'volume', 'mordechai', 'mordechais', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'nebuchadnezzar' :
        RPNUnitInfo( 'volume', 'nebuchadnezzar', 'nebuchadnezzars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'ngogn' :
        RPNUnitInfo( 'volume', 'ngogn', 'ngogns', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'oil_barrel' :
        RPNUnitInfo( 'volume', 'oil_barrel', 'oil_barrels', 'bbl',
                     [ ], [ 'US' ],
                     '''
''' ),

    'peck' :
        RPNUnitInfo( 'volume', 'peck', 'pecks', 'pk',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'piccolo' :
        RPNUnitInfo( 'volume', 'piccolo', 'piccolos', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'pinch' :
        RPNUnitInfo( 'volume', 'pinch', 'pinches', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'pin' :
        RPNUnitInfo( 'volume', 'pin', 'pins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'pint' :
        RPNUnitInfo( 'volume', 'pint', 'pints', 'pt',
                     [ ], [ 'traditional', 'cooking', 'US' ],
                     '''
''' ),

    'pipe' :
        RPNUnitInfo( 'volume', 'pipe', 'pipes', '',
                     [ 'butt', 'butts' ], [ 'imperial' ],
                     '''
''' ),

    'pony' :
        RPNUnitInfo( 'volume', 'pony', 'ponies', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'portuguese_almude' :
        RPNUnitInfo( 'volume', 'portuguese_almude', 'portuguese_almudes', '',
                     [ ], [ 'Portugal' ],
                     '''
''' ),

    'pottle' :
        RPNUnitInfo( 'volume', 'pottle', 'pottles', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'puncheon' :
        RPNUnitInfo( 'volume', 'puncheon', 'puncheons', '',
                     [ 'tertian', 'tertians' ], [ 'wine' ],
                     '''
''' ),

    'quart' :
        RPNUnitInfo( 'volume', 'quart', 'quarts', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'rehoboam' :
        RPNUnitInfo( 'volume', 'rehoboam', 'rehoboams', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'rundlet' :
        RPNUnitInfo( 'volume', 'rundlet', 'rundlets', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'salmanazar' :
        RPNUnitInfo( 'volume', 'salmanazar', 'salmanazars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'saltspoon' :
        RPNUnitInfo( 'volume', 'saltspoon', 'saltspoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'scruple' :
        RPNUnitInfo( 'volume', 'scruple', 'scruples', '',
                     [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ],
                     '''
''' ),

    'smidgen' :
        RPNUnitInfo( 'volume', 'smidgen', 'smidgens', '',
                     [ 'smidgeon', 'smidgeons' ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'snit' :
        RPNUnitInfo( 'volume', 'snit', 'snits', '',
                     [ ], [ 'U.S.' ],
                     '''
http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'spanish_almude' :
        RPNUnitInfo( 'volume', 'spanish_almude', 'spanish_almudes', '',
                     [ ], [ 'Spain' ],
                     '''
''' ),

    'solomon' :
        RPNUnitInfo( 'volume', 'solomon', 'solomons', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'sovereign' :
        RPNUnitInfo( 'volume', 'sovereign', 'sovereigns', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'standard' :
        RPNUnitInfo( 'volume', 'standard', 'standards', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'stein' :
        RPNUnitInfo( 'volume', 'stein', 'steins', '',
                     [ ], [ 'Germany' ],
                     '''
A stein is a German beer mug.  Steins come in various sizes, but the most
common size seems to be 1/2 liter (1.057 U.S pint or 0.880 British Imperial
pint).

http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'stere' :
        RPNUnitInfo( 'volume', 'stere', 'steres', 'st',
                     [ ], [ 'metric', 'obsolete' ],  # ... but not SI
                     '''
''' ),

    'strike' :
        RPNUnitInfo( 'volume', 'strike', 'strikes', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'sydharb' :
        RPNUnitInfo( 'volume', 'sydharb', 'sydharbs', '',
                     [ ], [ 'informal' ],
                     '''
The approximate volume of the Syndey Harbor at high tide, considered to be
equal to 562,000 megaliters.
''' ),

    'tablespoon' :
        RPNUnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'teaspoon' :
        RPNUnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'tierce' :
        RPNUnitInfo( 'volume', 'tierce', 'tierces', '',
                     [ ], [ 'wine', 'imperial' ],
                     '''
''' ),

    'tun' :
        RPNUnitInfo( 'volume', 'tun', 'tuns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'wineglass' :
        RPNUnitInfo( 'volume', 'wineglass', 'wineglasses', '',
                     [ 'wine_glass', 'wine_glasses' ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_barrel' :
        RPNUnitInfo( 'volume', 'wine_barrel', 'wine_barrels', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_butt' :
        RPNUnitInfo( 'volume', 'wine_butt', 'wine_butts', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_gallon' :
        RPNUnitInfo( 'volume', 'wine_gallon', 'wine_gallons', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_hogshead' :
        RPNUnitInfo( 'volume', 'wine_hogshead', 'wine_hogsheads', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_pipe' :
        RPNUnitInfo( 'volume', 'wine_pipe', 'wine_pipes', '',
                     [ 'wine_butt', 'wine_butts' ], [ 'imperial' ],
                     '''
''' ),

    'wine_tun' :
        RPNUnitInfo( 'volume', 'wine_tun', 'wine_tuns', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),
}


# //******************************************************************************
# //
# //  metricUnits
# //
# //  ... or any units that should get the SI prefixes
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

metricUnits = [
    ( 'ampere',             'amperes',          'A',    [ 'amp' ], [ 'amps' ] ),
    ( 'ampere*second',      'ampere*seconds',   'As',   [ 'amp*second' ], [ 'amp*seconds' ] ),
    ( 'arcsecond',          'arcseconds',       'as',   [ ], [ ] ),
    ( 'are',                'ares',             'a',    [ ], [ ] ),
    ( 'bar',                'bars',             'bar',  [ ], [ ] ),
    ( 'barn',               'barns',            '',     [ ], [ ] ),
    ( 'becquerel',          'becquerels',       'Bq',   [ ], [ ] ),
    ( 'blintz',             'blintzes',         'bl',   [ ], [ ] ),
    ( 'calorie',            'calories',         'cal',  [ ], [ 'cals' ] ),
    ( 'coulomb',            'coulombs',         'C',    [ ], [ ] ),
    ( 'curie',              'cruies',           'Ci',   [ ], [ ] ),
    ( 'dyne',               'dynes',            '',     [ ], [ ] ),
    ( 'electron-volt',      'electron-volts',   'eV',   [ ], [ ] ),
    ( 'erg',                'ergs',             '',     [ ], [ ] ),
    ( 'farad',              'farads',           'F',    [ ], [ ] ),
    ( 'gauss',              'gauss',            '',     [ ], [ ] ),
    ( 'gram',               'grams',            'g',    [ 'gramme' ], [ 'grammes' ] ),
    ( 'gram-equivalent',    'grams-equivalent', 'gE',   [ 'gram-energy', 'gramme-energy' ], [ 'grams-energy', 'grammes-energy' ] ),
    ( 'gram-force',         'grams-force',      'gf',   [ 'gramme-force' ], [ 'grammes-force' ] ),
    ( 'gray',               'grays',            'Gy',   [ ], [ ] ),
    ( 'henry',              'henries',          'H',    [ ], [ ] ),
    ( 'hertz',              'hertz',            'Hz',   [ ], [ ] ),
    ( 'joule',              'joules',           'J',    [ ], [ ] ),
    ( 'kelvin',             'kelvins',          'K',    [ ], [ ] ),
    ( 'light-year',         'light-years',      'ly',   [ ], [ ] ),
    ( 'liter',              'liters',           'L',    [ 'litre' ], [ 'litres' ] ),
    ( 'lumen',              'lumens',           'lm ',  [ ], [ ] ),
    ( 'lux',                'lux',              'lx',   [ ], [ ] ),
    ( 'maxwell',            'maxwells',         'Mx',   [ ], [ ] ),
    ( 'meter',              'meters',           'm',    [ 'metre' ], [ 'metres' ] ),
    ( 'mole',               'moles',            'mol',  [ ], [ ] ),
    ( 'newton',             'newtons',          'N',    [ ], [ ] ),
    ( 'ngogn',              'ngogns',           'ng',   [ ], [ ] ),
    ( 'ohm',                'ohms',             'O',    [ ], [ ] ),
    ( 'parsec',             'parsecs',          'pc',   [ ], [ ] ),
    ( 'pascal',             'pascals',          'Pa',   [ ], [ ] ),
    ( 'pascal*second',      'pascal*seconds',   'Pas',  [ ], [ ] ),
    ( 'poise',              'poise',            '',     [ ], [ ] ),
    ( 'pond',               'ponds',            '',     [ ], [ ] ),
    ( 'potrzebie',          'potrzebies',       'pz',   [ ], [ ] ),
    ( 'rad',                'rads',             'rad',  [ ], [ ] ),
    ( 'radian',             'radians',          '',     [ ], [ ] ),
    ( 'rem',                'rems',             'rem',  [ ], [ ] ),
    ( 'second',             'seconds',          's',    [ ], [ ] ),
    ( 'siemens',            'siemens',          'S',    [ 'mho' ], [ 'mhos' ] ),
    ( 'sievert',            'sieverts',         'Sv',   [ ], [ ] ),
    ( 'steradian',          'steradians',       '',     [ ], [ ] ),
    ( 'stere',              'steres',           'st',   [ ], [ ] ),
    ( 'tesla',              'teslas',           'T',    [ ], [ ] ),
    ( 'ton',                'tons',             '',     [ ], [ ] ),
    ( 'tonne',              'tonnes',           '',     [ ], [ ] ),
    ( 'ton_of_TNT',         'tons_of_TNT',      'tTNT', [ ], [ ] ),
    ( 'volt',               'volts',            'V',    [ ], [ ] ),
    ( 'watt',               'watts',            'W',    [ ], [ ] ),
    ( 'second*watt',        'watt*seconds',     'Ws',   [ ], [ ] ),
    ( 'weber',              'webers',           'Wb',   [ ], [ ] ),
]


# //******************************************************************************
# //
# //  dataUnits
# //
# //  ... or any units that should get the SI prefixes (positive powers of 10)
# //  and the binary prefixes
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

dataUnits = [
    ( 'bit',            'bits',             'b',    [ ], [ ] ),
    ( 'bit/second',     'bits/second',      'bps',  [ ], [ ] ),
    ( 'byte',           'bytes',            'B',    [ ], [ ] ),
    ( 'byte/second',    'bytes/second',     'Bps',  [ ], [ ] ),
]


# //******************************************************************************
# //
# //  timeUnits
# //
# //******************************************************************************

timeUnits = [
    ( 'minute',     'minutes',      'm',        '60' ),
    ( 'hour',       'hours',        'h',        '3600' ),
    ( 'day',        'days',         'd',        '86400' ),
    ( 'year',       'years',        'y',        '31557600' ),   # Julian year == 365.25 days
]


# //******************************************************************************
# //
# //  metricPrefixes
# //
# //  ( name, abbreviation, power of 10 )
# //
# //******************************************************************************

metricPrefixes = [
    ( 'yotta',      'Y',      '24' ),
    ( 'zetta',      'Z',      '21' ),
    ( 'exa',        'E',      '18' ),
    ( 'peta',       'P',      '15' ),
    ( 'tera',       'T',      '12' ),
    ( 'giga',       'G',      '9' ),
    ( 'mega',       'M',      '6' ),
    ( 'kilo',       'k',      '3' ),
    ( 'hecto',      'h',      '2' ),
    ( 'deca',       'da',     '1' ),
    ( 'deci',       'd',      '-1' ),
    ( 'centi',      'c',      '-2' ),
    ( 'milli',      'm',      '-3' ),
    ( 'micro',      'u',      '-6' ),  # it's really a mu
    ( 'nano',       'n',      '-9' ),
    ( 'pico',       'p',      '-12' ),
    ( 'femto',      'f',      '-15' ),
    ( 'atto',       'a',      '-18' ),
    ( 'zepto',      'z',      '-21' ),
    ( 'yocto',      'y',      '-24' ),
]


# //******************************************************************************
# //
# //  dataPrefixes
# //
# //  ( name, abbreviation, power of 10 )
# //
# //******************************************************************************

dataPrefixes = [
    ( 'yotta',      'Y',      '24' ),
    ( 'zetta',      'Z',      '21' ),
    ( 'exa',        'E',      '18' ),
    ( 'peta',       'P',      '15' ),
    ( 'tera',       'T',      '12' ),
    ( 'giga',       'G',      '9' ),
    ( 'mega',       'M',      '6' ),
    ( 'kilo',       'k',      '3' ),
]


# //******************************************************************************
# //
# //  binaryPrefixes
# //
# //  ( name, abbreviation, power of 2 )
# //
# //******************************************************************************

binaryPrefixes = [
    ( 'yobi',       'Yi',     '80' ),
    ( 'zebi',       'Zi',     '70' ),
    ( 'exi',        'Ei',     '60' ),
    ( 'pebi',       'Pi',     '50' ),
    ( 'tebi',       'Ti',     '40' ),
    ( 'gibi',       'Gi',     '30' ),
    ( 'mebi',       'Mi',     '20' ),
    ( 'kibi',       'ki',     '10' ),
]


# //******************************************************************************
# //
# //  unitConversionMatrix
# //
# //  ( first unit, second unit, conversion factor )
# //
# //******************************************************************************

unitConversionMatrix = {
    ( 'abampere',                   'ampere' )                              : mpmathify( '10' ),
    ( 'abcoulomb',                  'coulomb' )                             : mpmathify( '10' ),
    ( 'abfarad',                    'farad' )                               : mpmathify( '1.0e9' ),
    ( 'abmho',                      'siemens' )                             : mpmathify( '1.0e9' ),
    ( 'acre',                       'foot^2' )                              : mpmathify( '43560' ),
    ( 'acre',                       'nanoacre' )                            : mpmathify( '1.0e9' ),
    ( 'acre*foot',                  'foot^3' )                              : mpmathify( '43560' ),
    ( 'aln',                        'inch' )                                : mpmathify( '23.377077865' ),
    ( 'ampere',                     'coulomb/second' )                      : mpmathify( '1' ),
    ( 'ampere',                     'statampere' )                          : mpmathify( '299792458' ),
    ( 'ampere',                     'watt/volt' )                           : mpmathify( '1' ),
    ( 'ampere*second*volt',         'joule' )                               : mpmathify( '1' ),
    ( 'ampere*volt',                'watt' )                                : mpmathify( '1' ),
    ( 'arcminute',                  'arcsecond' )                           : mpmathify( '60' ),
    ( 'are',                        'meter^2' )                             : mpmathify( '100' ),
    ( 'arpent',                     'foot' )                                : mpmathify( '192' ),
    ( 'arshin',                     'pyad' )                                : mpmathify( '4' ),
    ( 'astronomical_unit',          'meter' )                               : mpmathify( '149597870691' ),
    ( 'atmosphere',                 'pascal' )                              : mpmathify( '101325' ),
    ( 'bakers_dozen',               'unity' )                               : mpmathify( '13' ),
    ( 'balthazar',                  'liter' )                               : mpmathify( '12.0' ),
    ( 'ban',                        'nat' )                                 : log( 10 ),
    ( 'banana_equivalent_dose',     'sievert' )                             : mpmathify( '9.8e-8' ),
    ( 'bar',                        'pascal' )                              : mpmathify( '1.0e5' ),
    ( 'barleycorn',                 'poppyseed' )                           : mpmathify( '4' ),
    ( 'beat',                       'blink' )                               : mpmathify( '100' ),
    ( 'beer_barrel',                'beer_keg' )                            : mpmathify( '2' ),
    ( 'beer_barrel',                'gallon' )                              : mpmathify( '31' ),
    ( 'berkovets',                  'dolya' )                               : mpmathify( '3686400' ),
    ( 'billion',                    'unity' )                               : mpmathify( '1.0e9' ),
    ( 'bit',                        'kilogram*meter^2/kelvin*second^2' )    : fmul( mpmathify( '1.38064852e-23' ), log( 2 ) ),
    ( 'bit',                        'nat' )                                 : log( 2 ),
    ( 'blintz',                     'farshimmelt_blintz' )                  : mpmathify( '1.0e5' ),
    ( 'blintz',                     'furshlugginer_blintz' )                : mpmathify( '1.0e-6' ),
    ( 'blintz',                     'gram' )                                : mpmathify( '36.42538631' ),
    ( 'bolt',                       'foot' )                                : mpmathify( '120' ),
    ( 'btu',                        'joule' )                               : mpmathify( '1054.5' ),
    ( 'btupf',                      'joule/kelvin' )                        : mpmathify( '1899.100534716' ),
    ( 'bucket',                     'gallon' )                              : mpmathify( '4' ),
    ( 'bushel',                     'peck' )                                : mpmathify( '4' ),
    ( 'byte',                       'bit' )                                 : mpmathify( '8' ),
    ( 'byte/second',                'bit/second' )                          : mpmathify( '8' ),
    ( 'calorie',                    'joule' )                               : mpmathify( '4.184' ),
    ( 'carat',                      'grain' )                               : fadd( 3, fdiv( 1, 6 ) ),
    ( 'carucate',                   'acre' )                                : mpmathify( '120' ),
    ( 'carucate',                   'bovate' )                              : mpmathify( '8' ),
    ( 'celsius',                    'degree_newton' )                       : fdiv( 33, 100 ),
    ( 'celsius',                    'reaumur' )                             : fdiv( 4, 5 ),
    ( 'centillion',                 'unity' )                               : mpmathify( '1.0e303' ),
    ( 'century',                    'microcentury' )                        : mpmathify( '1.0e6' ),
    ( 'century',                    'nanocentury' )                         : mpmathify( '1.0e9' ),
    ( 'century',                    'year' )                                : mpmathify( '100' ),
    ( 'chain',                      'yard' )                                : mpmathify( '22' ),
    ( 'chandrasekhar_limit',        'gram' )                                : mpmathify( '2.765e33' ),
    ( 'chopine',                    'liter' )                               : mpmathify( '0.25' ),
    ( 'circle',                     'degree' )                              : mpmathify( '360' ),
    ( 'clarke',                     'day' )                                 : mpmathify( '1' ),
    ( 'clarke',                     'wolverton' )                           : mpmathify( '1.0e6' ),
    ( 'clausius',                   'joule/kelvin' )                        : mpmathify( '4186.8' ),
    ( 'clavelin',                   'liter' )                               : mpmathify( '0.62' ),
    ( 'conductance_quantum',        'siemens' )                             : mpmathify( '7.7480917310e-5' ),
    ( 'coomb',                      'strike' )                              : mpmathify( '2' ),
    ( 'cord',                       'foot^3' )                              : mpmathify( '128' ),
    ( 'coulomb',                    'ampere*second' )                       : mpmathify( '1' ),
    ( 'coulomb',                    'farad*volt' )                          : mpmathify( '1' ),
    ( 'coulomb',                    'joule/volt' )                          : mpmathify( '1' ),
    ( 'coulomb/farad',              'volt' )                                : mpmathify( '1' ),
    ( 'coulomb/kilogram',           'roentgen' )                            : mpmathify( '3876' ),
    ( 'coulomb/volt',               'farad' )                               : mpmathify( '1' ),
    ( 'cowznofski',                 'mingo' )                               : mpmathify( '10' ),
    ( 'cubit',                      'inch' )                                : mpmathify( '18' ),
    ( 'cup',                        'dram' )                                : mpmathify( '64' ),
    ( 'cup',                        'fluid_ounce' )                         : mpmathify( '8' ),
    ( 'cup',                        'gill' )                                : mpmathify( '2' ),
    ( 'cup',                        'wineglass' )                           : mpmathify( '4' ),
    ( 'curie',                      'becquerel' )                           : mpmathify( '3.7e10' ),
    ( 'daily',                      'monthly' )                             : mpmathify( '30' ),
    ( 'daily',                      'weekly' )                              : mpmathify( '7' ),
    ( 'daily',                      'yearly' )                              : mpmathify( '365.25' ),
    ( 'dalton',                     'gram' )                                : mpmathify( '1.660539040e-24' ),
    ( 'day',                        'beat' )                                : mpmathify( '1000' ),
    ( 'day',                        'hour' )                                : mpmathify( '24' ),
    ( 'decade',                     'year' )                                : mpmathify( '10' ),
    ( 'decillion',                  'unity' )                               : mpmathify( '1.0e33' ),
    ( 'degree',                     'arcminute' )                           : mpmathify( '60' ),
    ( 'degree',                     'furman' )                              : mpmathify( '65536' ),
    ( 'degree',                     'streck' )                              : mpmathify( '17.5' ),
    ( 'demi',                       'liter' )                               : mpmathify( '0.375' ),
    ( 'dessertspoon',               'teaspoon' )                            : mpmathify( '2' ),
    ( 'diuym',                      'inch' )                                : mpmathify( '1' ),
    ( 'diuym',                      'liniya' )                              : mpmathify( '10' ),
    ( 'doppelzentner',              'zentner' )                             : mpmathify( '2' ),
    ( 'dozen',                      'unity' )                               : mpmathify( '12' ),
    ( 'dram',                       'scruple' )                             : mpmathify( '3' ),
    ( 'dry_barrel',                 'bushel' )                              : mpmathify( '4' ),
    ( 'dry_barrel',                 'foot^2' )                              : fdiv( 49, 12 ),
    ( 'dry_gallon',                 'dry_quart' )                           : mpmathify( '4' ),
    ( 'dry_hogshead',               'dry_barrel' )                          : mpmathify( '2' ),
    ( 'dry_pint',                   'foot^3' )                              : mpmathify( '0.0194446252894' ),
    ( 'dry_quart',                  'dry_pint' )                            : mpmathify( '2' ),
    ( 'dry_tun',                    'dry_hogshead' )                        : mpmathify( '4' ),
    ( 'duodecillion',               'unity' )                               : mpmathify( '1.0e39' ),
    ( 'dword',                      'bit' )                                 : mpmathify( '32' ),
    ( 'eight',                      'unity' )                               : mpmathify( '8' ),
    ( 'eighteen',                   'unity' )                               : mpmathify( '18' ),
    ( 'eighty',                     'unity' )                               : mpmathify( '80' ),
    ( 'electron-volt',              'joule' )                               : mpmathify( '1.6021766208e-19' ),
    ( 'eleven',                     'unity' )                               : mpmathify( '11' ),
    ( 'ell',                        'inch' )                                : mpmathify( '45' ),
    ( 'eon',                        'year' )                                : mpmathify( '1e9' ),
    ( 'every_minute',               'hourly' )                              : mpmathify( '60' ),
    ( 'every_second',               '1/second' )                            : mpmathify( '1' ),
    ( 'every_second',               'every_minute' )                        : mpmathify( '60' ),
    ( 'famn',                       'aln' )                                 : mpmathify( '3' ),
    ( 'farad',                      '1/hertz*ohm' )                         : mpmathify( '1' ),
    ( 'farad',                      'ampere*second/volt' )                  : mpmathify( '1' ),
    ( 'farad',                      'ampere^2*second^4/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'farad',                      'coulomb^2*second^2/kilogram*meter^2' ) : mpmathify( '1' ),
    ( 'farad',                      'coulomb^2/joule' )                     : mpmathify( '1' ),
    ( 'farad',                      'coulomb^2/meter*newton' )              : mpmathify( '1' ),
    ( 'farad',                      'jar' )                                 : mpmathify( '9.0e8' ),
    ( 'farad',                      'joule/volt^2' )                        : mpmathify( '1' ),
    ( 'farad',                      'meter*newton/volt^2' )                 : mpmathify( '1' ),
    ( 'farad',                      'second*watt/volt^2' )                  : mpmathify( '1' ),
    ( 'farad',                      'second/ohm' )                          : mpmathify( '1' ),
    ( 'farad',                      'second^2/henry' )                      : mpmathify( '1' ),
    ( 'farad',                      'statfarad' )                           : mpmathify( '898755178736.5' ),
    ( 'faraday',                    'coulomb' )                             : mpmathify( '96485.3383' ),
    ( 'fathom',                     'foot' )                                : mpmathify( '6' ),
    ( 'fifteen',                    'unity' )                               : mpmathify( '15' ),
    ( 'fifty',                      'unity' )                               : mpmathify( '50' ),
    ( 'finger',                     'inch' )                                : mpmathify( '4.5' ),
    ( 'fingerbreadth',              'inch' )                                : mpmathify( '0.75' ),
    ( 'firkin',                     'gallon' )                              : mpmathify( '9' ),
    ( 'firkin',                     'pin' )                                 : mpmathify( '2' ),
    ( 'five',                       'unity' )                               : mpmathify( '5' ),
    ( 'flame',                      'lux' )                                 : mpmathify( '43.0556416668' ),
    ( 'flock',                      'unity' )                               : mpmathify( '40' ),
    ( 'fluid_ounce',                'dram' )                                : mpmathify( '8' ),
    ( 'fluid_ounce',                'tablespoon' )                          : mpmathify( '2' ),
    ( 'foe',                        'joule' )                               : mpmathify( '10e44' ),
    ( 'foot',                       'inch' )                                : mpmathify( '12' ),
    ( 'footcandle',                 'lumen/foot^2' )                        : mpmathify( '1' ),
    ( 'footcandle',                 'lux' )                                 : mpmathify( '10.763910417' ),            # (m/ft)^2
    ( 'footlambert',                'candela/meter^2' )                     : mpmathify( '3.42625909963539052691' ),  # 1/pi cd/ft^2
    ( 'fortnight',                  'day' )                                 : mpmathify( '14' ),
    ( 'fortnight',                  'microfortnight' )                      : mpmathify( '1.0e6' ),
    ( 'four',                       'unity' )                               : mpmathify( '4' ),
    ( 'fourteen',                   'unity' )                               : mpmathify( '14' ),
    ( 'funt',                       'dolya' )                               : mpmathify( '9216' ),
    ( 'furlong',                    'yard' )                                : mpmathify( '220' ),
    ( 'fut',                        'foot' )                                : mpmathify( '1' ),
    ( 'galileo',                    'meter/second^2' )                      : mpmathify( '0.01' ),
    ( 'gallon',                     'fifth' )                               : mpmathify( '5' ),
    ( 'gallon',                     'quart' )                               : mpmathify( '4' ),
    ( 'gauss',                      'maxwell/centimeter^2' )                : mpmathify( '1' ),
    ( 'goliath',                    'liter' )                               : mpmathify( '27.0' ),
    ( 'googol',                     'unity' )                               : mpmathify( '1.0e100' ),
    ( 'grad',                       'degree' )                              : mpmathify( '0.9' ),
    ( 'gram',                       'dolya' )                               : mpmathify( '22.50481249152' ),
    ( 'gram-equivalent',            'joule' )                               : fdiv( power( 299792458, 2 ), 1000 ),
    ( 'gram-force',                 'newton' )                              : mpmathify( '0.00980665' ),
    ( 'gray',                       'joule/kilogram' )                      : mpmathify( '1' ),
    ( 'gray',                       'rad' )                                 : mpmathify( '100' ),
    ( 'gray',                       'sievert' )                             : mpmathify( '1' ),
    ( 'great_gross',                'gross' )                               : mpmathify( '12' ),
    ( 'greek_cubit',                'inch' )                                : mpmathify( '18.22' ),
    ( 'gregorian_year',             'second' )                              : mpmathify( '31556952' ),
    ( 'gross',                      'unity' )                               : mpmathify( '144' ),
    ( 'hand',                       'inch' )                                : mpmathify( '4' ),
    ( 'handbreadth',                'inch' )                                : mpmathify( '3' ),
    ( 'hartree',                    'rydberg' )                             : mpmathify( '2' ),
    ( 'hefnerkerze',                'candela' )                             : mpmathify( '0.920' ),  # approx.
    ( 'henry',                      'abhenry' )                             : mpmathify( '1.0e9' ),
    ( 'henry',                      'joule/ampere^2' )                      : mpmathify( '1' ),
    ( 'henry',                      'kilogram*meter^2/ampere^2*second^2' )  : mpmathify( '1' ),
    ( 'henry',                      'kilogram*meter^2/coulomb^2' )          : mpmathify( '1' ),
    ( 'henry',                      'ohm*second' )                          : mpmathify( '1' ),
    ( 'henry',                      'ohm/hertz' )                           : mpmathify( '1' ),
    ( 'henry',                      'second^2/farad' )                      : mpmathify( '1' ),
    ( 'henry',                      'weber/ampere' )                        : mpmathify( '1' ),
    ( 'hertz',                      '1/second' )                            : mpmathify( '1' ),
    ( 'hertz',                      'becquerel' )                           : mpmathify( '1' ),
    ( 'hogshead',                   'liter' )                               : mpmathify( '238.481' ),
    ( 'homestead',                  'acre' )                                : mpmathify( '160' ),
    ( 'hoppus_ton',                 'hoppus_foot' )                         : mpmathify( '50' ),
    ( 'hoppus_ton',                 'meter^3' )                             : mpmathify( '1.8027' ),
    ( 'horsepower',                 'watt' )                                : mpmathify( '745.69987158227022' ),
    ( 'horsepower*second',          'joule' )                               : mpmathify( '745.69987158227022' ),
    ( 'hour',                       'minute' )                              : mpmathify( '60' ),
    ( 'hourly',                     'daily' )                               : mpmathify( '24' ),
    ( 'hubble',                     'light-year' )                          : mpmathify( '1.0e9' ),
    ( 'hundred',                    'unity' )                               : mpmathify( '100' ),
    ( 'imperial_bushel',            'kenning' )                             : mpmathify( '2' ),
    ( 'imperial_butt',              'imperial_hogshead' )                   : mpmathify( '2' ),
    ( 'imperial_cup',               'imperial_gill' )                       : mpmathify( '2' ),
    ( 'imperial_gallon',            'pottle' )                              : mpmathify( '2' ),
    ( 'imperial_gill',              'jack' )                                : mpmathify( '2' ),
    ( 'imperial_hogshead',          'coomb' )                               : mpmathify( '2' ),
    ( 'imperial_peck',              'imperial_quart' )                      : mpmathify( '2' ),
    ( 'imperial_pint',              'imperial_cup' )                        : mpmathify( '2' ),
    ( 'imperial_quart',             'imperial_pint' )                       : mpmathify( '2' ),
    ( 'imperial_square',            'foot^2' )                              : mpmathify( '100' ),
    ( 'inch',                       'barleycorn' )                          : mpmathify( '3' ),
    ( 'inch',                       'caliber' )                             : mpmathify( '100' ),
    ( 'inch',                       'cicero' )                              : fdiv( mpmathify( '50.8' ), 9 ),
    ( 'inch',                       'gutenberg' )                           : mpmathify( '7200' ),
    ( 'inch',                       'meter' )                               : mpmathify( '0.0254' ),
    ( 'inch',                       'mil' )                                 : mpmathify( '1000' ),
    ( 'inch',                       'pica' )                                : mpmathify( '6' ),
    ( 'inch',                       'point' )                               : mpmathify( '72' ),
    ( 'inch',                       'twip' )                                : mpmathify( '1440' ),
    ( 'jack',                       'tablespoon' )                          : mpmathify( '5' ),
    ( 'jennie',                     'liter' )                               : mpmathify( '0.5' ),
    ( 'jeroboam',                   'liter' )                               : mpmathify( '3.0' ),  # some French regions use 4.5
    ( 'jigger',                     'pony' )                                : mpmathify( '2' ),
    ( 'joule',                      'coulomb*volt' )                        : mpmathify( '1' ),
    ( 'joule',                      'erg' )                                 : mpmathify( '1.0e7' ),
    ( 'joule',                      'kilogram*meter^2/second^2' )           : mpmathify( '1' ),
    ( 'joule',                      'second*watt' )                         : mpmathify( '1' ),
    ( 'joule*second^2/meter^2',     'gram' )                                : mpmathify( '1000' ),
    ( 'joule/second',               'watt' )                                : mpmathify( '1' ),
    ( 'kelvin',                     'rankine' )                             : fdiv( 9, 5 ),
    ( 'ken',                        'inch' )                                : mpmathify( '83.4' ),
    ( 'kenning',                    'imperial_peck' )                       : mpmathify( '2' ),
    ( 'kilderkin',                  'firkin' )                              : mpmathify( '2' ),
    ( 'kilogram/meter^3',           'kilogram/liter' )                      : mpmathify( '1000' ),
    ( 'kip',                        'pound' )                               : mpmathify( '1000' ),
    ( 'kosaya_sazhen',              'meter' )                               : mpmathify( '2.48' ),
    ( 'kovac',                      'wolverton' )                           : mpmathify( '10' ),
    ( 'lambert',                    'candela/meter^2' )                     : fdiv( 10000, pi ),
    ( 'league',                     'mile' )                                : mpmathify( '3' ),
    ( 'leo',                        'meter/second^2' )                      : mpmathify( '10' ),
    ( 'library_of_congress',        'byte' )                                : mpmathify( '1.0e13' ),
    ( 'light-second',               'meter' )                               : mpmathify( '299792458' ),
    ( 'light-year',                 'light-second' )                        : mpmathify( '31557600' ),
    ( 'link',                       'inch' )                                : mpmathify( '7.92' ),
    ( 'liter',                      'ngogn' )                               : mpmathify( '86.2477899004' ),
    ( 'liter',                      'stein' )                               : mpmathify( '2' ),
    ( 'long_cubit',                 'inch' )                                : mpmathify( '21' ),
    ( 'long_hundred',               'unity' )                               : mpmathify( '120' ),
    ( 'long_reed',                  'foot' )                                : mpmathify( '10.5' ),
    ( 'lot',                        'dolya' )                               : mpmathify( '288' ),
    ( 'lumen',                      'candela*steradian' )                   : mpmathify( '1' ),
    ( 'lustrum',                    'year' )                                : mpmathify( '5' ),
    ( 'lux',                        'lumen/meter^2' )                       : mpmathify( '1' ),
    ( 'lux',                        'nox' )                                 : mpmathify( '1000' ),
    ( 'mach',                       'meter/second' )                        : mpmathify( '340.2868' ),
    ( 'magnum',                     'bottle' )                              : mpmathify( '2' ),
    ( 'magnum',                     'liter' )                               : mpmathify( '1.5' ),
    ( 'marathon',                   'yard' )                                : mpmathify( '46145' ),
    ( 'marie_jeanne',               'liter' )                               : mpmathify( '2.25' ),
    ( 'martin',                     'kovac' )                               : mpmathify( '100' ),
    ( 'maxwell',                    'centimeter^2*gauss' )                  : mpmathify( '1' ),
    ( 'melchior',                   'liter' )                               : mpmathify( '18.0' ),
    ( 'melchizedek',                'liter' )                               : mpmathify( '30.0' ),
    ( 'meter',                      'angstrom' )                            : mpmathify( '1.0e10' ),
    ( 'meter',                      'french' )                              : mpmathify( '3000' ),
    ( 'meter',                      'kyu' )                                 : mpmathify( '4000' ),
    ( 'meter',                      'micron' )                              : mpmathify( '1.0e6' ),
    ( 'meter*newton',               'joule' )                               : mpmathify( '1' ),
    ( 'meter/second',               'bubnoff_unit' )                        : mpmathify( '3.15576e13' ),
    ( 'meter/second',               'kine' )                                : mpmathify( '100' ),
    ( 'meter/second',               'knot' )                                : mpmathify( '1.943844492' ),
    ( 'meter^2',                    'barn' )                                : mpmathify( '1.0e28' ),
    ( 'meter^2',                    'foot^2' )                              : mpmathify( '10.7639104167' ),
    ( 'meter^2',                    'outhouse' )                            : mpmathify( '1.0e34' ),
    ( 'meter^2',                    'shed' )                                : mpmathify( '1.0e52' ),
    ( 'meter^3',                    'foot^3' )                              : mpmathify( '35.3146667215' ),
    ( 'meter^3',                    'liter' )                               : mpmathify( '1000' ),
    ( 'meter^3',                    'liter' )                               : mpmathify( '1000' ),
    ( 'meter^3*pascal',             'joule' )                               : mpmathify( '1' ),
    ( 'methuselah',                 'liter' )                               : mpmathify( '6.0' ),
    ( 'metric_foot',                'meter' )                               : mpmathify( '0.3' ),
    ( 'mezhevaya_versta',           'versta' )                              : mpmathify( '2' ),
    ( 'mile',                       'foot' )                                : mpmathify( '5280' ),
    ( 'mile/hour',                  'kilometer/hour' )                      : mpmathify( '1.609344' ),
    ( 'mile/hour',                  'meter/second' )                        : mpmathify( '0.44704' ),
    ( 'million',                    'unity' )                               : mpmathify( '1.0e6' ),
    ( 'mingo',                      'clarke' )                              : mpmathify( '10' ),
    ( 'minute',                     'second' )                              : mpmathify( '60' ),
    ( 'mmHg',                       'pascal' )                              : mpmathify( '133.3224' ),        # approx.
    ( 'month',                      'day' )                                 : mpmathify( '30' ),
    ( 'mordechai',                  'liter' )                               : mpmathify( '9.0' ),
    ( 'morgen',                     'are' )                                 : mpmathify( '85.6532' ),
    ( 'nail',                       'inch' )                                : mpmathify( '2.25' ),
    ( 'nat',                        'joule/kelvin' )                        : mpmathify( '1.380650e-23' ),
    ( 'nautical_mile',              'meter' )                               : mpmathify( '1852' ),
    ( 'nebuchadnezzar',             'liter' )                               : mpmathify( '15.0' ),
    ( 'newton',                     'ampere*weber/meter' )                  : mpmathify( '1' ),
    ( 'newton',                     'dyne' )                                : mpmathify( '1.0e5' ),
    ( 'newton',                     'joule/meter' )                         : mpmathify( '1' ),
    ( 'newton',                     'kilogram*meter/second^2' )             : mpmathify( '1' ),
    ( 'newton',                     'pond' )                                : mpmathify( '101.97161298' ),
    ( 'newton',                     'poundal' )                             : mpmathify( '7.233013851' ),
    ( 'newton*second/meter^2',      'pascal*second' )                       : mpmathify( '1' ),
    ( 'newton/meter^2',             'pascal' )                              : mpmathify( '1' ),
    ( 'ngogn',                      'farshimmelt_ngogn' )                   : mpmathify( '1.0e5' ),
    ( 'ngogn',                      'furshlugginer_ngogn' )                 : mpmathify( '1.0e-6' ),
    ( 'nibble',                     'bit' )                                 : mpmathify( '4' ),
    ( 'nine',                       'unity' )                               : mpmathify( '9' ),
    ( 'nineteen',                   'unity' )                               : mpmathify( '19' ),
    ( 'ninety',                     'unity' )                               : mpmathify( '90' ),
    ( 'nit',                        'apostilb' )                            : pi,
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'nonillion',                  'unity' )                               : mpmathify( '1.0e30' ),
    ( 'novemdecillion',             'unity' )                               : mpmathify( '1.0e60' ),
    ( 'nyp',                        'bit' )                                 : mpmathify( '2' ),
    ( 'oc1',                        'bit/second' )                          : mpmathify( '5.184e7' ),
    ( 'oc12',                       'oc1' )                                 : mpmathify( '12' ),
    ( 'oc192',                      'oc1' )                                 : mpmathify( '192' ),
    ( 'oc24',                       'oc1' )                                 : mpmathify( '24' ),
    ( 'oc3',                        'oc1' )                                 : mpmathify( '3' ),
    ( 'oc48',                       'oc1' )                                 : mpmathify( '48' ),
    ( 'oc768',                      'oc1' )                                 : mpmathify( '768' ),
    ( 'octant',                     'degree' )                              : mpmathify( '45' ),
    ( 'octillion',                  'unity' )                               : mpmathify( '1.0e27' ),
    ( 'octodecillion',              'unity' )                               : mpmathify( '1.0e57' ),
    ( 'oersted',                    'ampere/meter' )                        : mpmathify( '79.5774715' ),
    ( 'ohm',                        '1/siemens' )                           : mpmathify( '1' ),
    ( 'ohm',                        'abohm' )                               : mpmathify( '1e9' ),
    ( 'ohm',                        'german_mile' )                         : mpmathify( '57.44' ),
    ( 'ohm',                        'jacobi' )                              : mpmathify( '0.6367' ),
    ( 'ohm',                        'joule*second/coulomb^2' )              : mpmathify( '1' ),
    ( 'ohm',                        'joule/ampere^2*second' )               : mpmathify( '1' ),
    ( 'ohm',                        'kilogram*meter^2/ampere^2*second^3' )  : mpmathify( '1' ),
    ( 'ohm',                        'matthiessen' )                         : mpmathify( '13.59' ),
    ( 'ohm',                        'second/farad' )                        : mpmathify( '1' ),
    ( 'ohm',                        'varley' )                              : mpmathify( '25.61' ),
    ( 'ohm',                        'volt/ampere' )                         : mpmathify( '1' ),
    ( 'ohm',                        'watt/ampere^2' )                       : mpmathify( '1' ),
    ( 'oil_barrel',                 'gallon' )                              : mpmathify( '42' ),
    ( 'ounce',                      'gram' )                                : mpmathify( '28.349523125' ),
    ( 'oword',                      'bit' )                                 : mpmathify( '128' ),
    ( 'parsec',                     'light-year' )                          : mpmathify( '3.261563776971' ),
    ( 'pascal',                     'barye' )                               : mpmathify( '10' ),
    ( 'pascal',                     'kilogram/meter*second^2' )             : mpmathify( '1' ),
    ( 'pascal*second',              'kilogram/meter*second' )               : mpmathify( '1' ),
    ( 'pascal*second',              'poise' )                               : mpmathify( '10' ),
    ( 'peck',                       'dry_gallon' )                          : mpmathify( '2' ),
    ( 'pennyweight',                'gram' )                                : mpmathify( '1.55517384' ),
    ( 'perch',                      'foot' )                                : mpmathify( '16.5' ),
    ( 'pferdestarke',               'watt' )                                : mpmathify( '735.49875' ),
    ( 'pfund',                      'gram' )                                : mpmathify( '500' ),
    ( 'phot',                       'lux' )                                 : mpmathify( '10000' ),
    ( 'piccolo',                    'liter' )                               : mpmathify( '0.1875' ),
    ( 'pieze',                      'pascal' )                              : mpmathify( '1000' ),
    ( 'pointangle',                 'degree' )                              : fdiv( 360, 32 ),
    ( 'poncelet',                   'watt' )                                : mpmathify( '980.665' ),
    ( 'pony',                       'dram' )                                : mpmathify( '6' ),
    ( 'pood',                       'dolya' )                               : mpmathify( '368640' ),
    ( 'portuguese_almude',          'liter' )                               : mpmathify( '16.7' ),
    ( 'potrzebie',                  'farshimmelt_potrzebie' )               : mpmathify( '1.0e5' ),
    ( 'potrzebie',                  'furshlugginer_potrzebie' )             : mpmathify( '1.0e-6' ),
    ( 'potrzebie',                  'meter' )                               : mpmathify( '0.002263348517438173216473' ),  # see Mad #33
    ( 'pottle',                     'imperial_quart' )                      : mpmathify( '2' ),
    ( 'pound',                      'grain' )                               : mpmathify( '7000' ),
    ( 'pound',                      'ounce' )                               : mpmathify( '16' ),
    ( 'pound',                      'sheet' )                               : mpmathify( '700' ),
    ( 'pound-force',                'newton' )                              : mpmathify( '4.4482216152605' ),
    ( 'psi',                        'pascal' )                              : mpmathify( '6894.75728' ),      # approx.
    ( 'pyad',                       'inch' )                                : mpmathify( '7' ),
    ( 'pyad',                       'vershok' )                             : mpmathify( '4' ),
    ( 'quad',                       'btu' )                                 : mpmathify( '10e15' ),
    ( 'quadrant',                   'degree' )                              : mpmathify( '90' ),
    ( 'quadrillion',                'unity' )                               : mpmathify( '1.0e15' ),
    ( 'quart',                      'cup' )                                 : mpmathify( '4' ),
    ( 'quart',                      'liter' )                               : mpmathify( '0.946352946' ),
    ( 'quart',                      'pint' )                                : mpmathify( '2' ),
    ( 'quattuordecillion',          'unity' )                               : mpmathify( '1.0e45' ),
    ( 'quindecillion',              'unity' )                               : mpmathify( '1.0e48' ),
    ( 'quintal',                    'gram' )                                : mpmathify( '100000' ),
    ( 'quintant',                   'degree' )                              : mpmathify( '72' ),
    ( 'quintillion',                'unity' )                               : mpmathify( '1.0e18' ),
    ( 'qword',                      'bit' )                                 : mpmathify( '64' ),
    ( 'rack_unit',                  'meter' )                               : mpmathify( '0.0445' ),
    ( 'radian',                     'centrad' )                             : mpmathify( '100' ),
    ( 'radian',                     'degree' )                              : fdiv( 180, pi ),
    ( 'reaumur',                    'degree_newton' )                       : fdiv( 33, 80 ),
    ( 'reed',                       'foot' )                                : mpmathify( '9' ),
    ( 'rehoboam',                   'liter' )                               : mpmathify( '4.5' ),
    ( 'reynolds',                   'pascal*second' )                       : mpmathify( '6894.75729' ),
    ( 'rod',                        'foot' )                                : mpmathify( '16.5' ),
    ( 'roentgen',                   'rad' )                                 : mpmathify( '0.877' ),
    ( 'rood',                       'foot^2' )                              : mpmathify( '10890' ),
    ( 'rope',                       'foot' )                                : mpmathify( '20' ),
    ( 'rutherford',                 'becquerel' )                           : mpmathify( '1.0e6' ),
    ( 'rydberg',                    'joule' )                               : mpmathify( '2.17987232498e-18' ),
    ( 'salmanazar',                 'liter' )                               : mpmathify( '9.0' ),
    ( 'sazhen',                     'meter' )                               : mpmathify( '2.1336' ),
    ( 'score',                      'unity' )                               : mpmathify( '20' ),
    ( 'scruple',                    'minim' )                               : mpmathify( '20' ),
    ( 'second',                     'jiffy' )                               : mpmathify( '100' ),
    ( 'second',                     'shake' )                               : mpmathify( '1.0e8' ),
    ( 'second',                     'svedberg' )                            : mpmathify( '1.0e13' ),
    ( 'section',                    'acre' )                                : mpmathify( '640' ),
    ( 'septendecillion',            'unity' )                               : mpmathify( '1.0e54' ),
    ( 'septillion',                 'unity' )                               : mpmathify( '1.0e24' ),
    ( 'seven',                      'unity' )                               : mpmathify( '7' ),
    ( 'seventeen',                  'unity' )                               : mpmathify( '17' ),
    ( 'seventy',                    'unity' )                               : mpmathify( '70' ),
    ( 'sexdecillion',               'unity' )                               : mpmathify( '1.0e51' ),
    ( 'sextant',                    'degree' )                              : mpmathify( '60' ),
    ( 'sextillion',                 'unity' )                               : mpmathify( '1.0e21' ),
    ( 'shock',                      'unity' )                               : mpmathify( '60' ),
    ( 'sidereal_day',               'second' )                              : mpmathify( '86164.0905' ),   # https://en.wikipedia.org/wiki/Sidereal_time
    ( 'sidereal_day',               'sidereal_hour' )                       : mpmathify( '24' ),
    ( 'sidereal_hour',              'sidereal_minute' )                     : mpmathify( '60' ),
    ( 'sidereal_minute',            'sidereal_second' )                     : mpmathify( '60' ),
    ( 'siemens',                    'ampere/volt' )                         : mpmathify( '1' ),
    ( 'siemens',                    'ampere^2*second^3/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'siemens',                    'coulomb^2*second/kilogram*meter^2' )   : mpmathify( '1' ),
    ( 'siemens',                    'statsiemens' )                         : mpmathify( '898755178736.5' ),
    ( 'sievert',                    'rem' )                                 : mpmathify( '100' ),
    ( 'siriometer',                 'astronomical_unit' )                   : mpmathify( '1.0e6' ),
    ( 'six',                        'unity' )                               : mpmathify( '6' ),
    ( 'sixteen',                    'unity' )                               : mpmathify( '16' ),
    ( 'skein',                      'foot' )                                : mpmathify( '360' ),
    ( 'skot',                       'bril' )                                : mpmathify( '1.0e4' ),
    ( 'skot',                       'lambert' )                             : mpmathify( '1.0e7' ),
    ( 'slug',                       'pound' )                               : mpmathify( '32.174048556' ),
    ( 'slug',                       'slinch' )                              : mpmathify( '12' ),
    ( 'smoot',                      'inch' )                                : mpmathify( '67' ),
    ( 'snit',                       'jigger' )                              : mpmathify( '2' ),
    ( 'solomon',                    'liter' )                               : mpmathify( '20.0' ),
    ( 'sovereign',                  'liter' )                               : mpmathify( '25.0' ),
    ( 'span',                       'inch' )                                : mpmathify( '9' ),
    ( 'spanish_almude',             'liter' )                               : mpmathify( '4.625' ),
    ( 'speed_of_sound',             'meter/second' )                        : mpmathify( '343' ),
    ( 'sphere',                     'hemisphere' )                          : mpmathify( '2' ),
    ( 'sphere',                     'steradian' )                           : fmul( 4, pi ),
    ( 'square_arcminute',           'square_arcsecond' )                    : mpmathify( '3600' ),
    ( 'square_degree',              'square_arcminute' )                    : mpmathify( '3600' ),
    ( 'square_octant',              'square_degree' )                       : mpmathify( '2025' ),
    ( 'square_quadrant',            'square_degree' )                       : mpmathify( '8100' ),
    ( 'square_quintant',            'square_degree' )                       : mpmathify( '5184' ),
    ( 'square_sextant',             'square_degree' )                       : mpmathify( '3600' ),
    ( 'stadium',                    'foot' )                                : mpmathify( '606.95' ),
    ( 'standard',                   'liter' )                               : mpmathify( '0.75' ),
    ( 'stapp',                      'meter/second^3' )                      : mpmathify( '9.80665' ),
    ( 'statcoulomb',                'coulomb' )                             : mpmathify( '3.335641e-10' ),  # 0.1A*m/c, approx.
    ( 'statcoulomb',                'franklin' )                            : mpmathify( '1' ),
    ( 'stathenry',                  'henry' )                               : mpmathify( '898755178740' ),
    ( 'statmho',                    'siemens' )                             : mpmathify( '8.99e11' ),
    ( 'statohm',                    'ohm' )                                 : mpmathify( '898755178740' ),
    ( 'statvolt',                   'volt' )                                : fdiv( 299792458, 1000000 ),
    ( 'steradian',                  'radian^2' )                            : mpmathify( '1' ),
    ( 'steradian',                  'square_degree' )                       : power( fdiv( 180, pi ), 2 ),
    ( 'steradian',                  'square_grad' )                         : power( fdiv( 200, pi ), 2 ),
    ( 'stere',                      'liter' )                               : mpmathify( '1000' ),
    ( 'sthene',                     'newton' )                              : mpmathify( '1000' ),
    ( 'stilb',                      'candela/meter^2' )                     : mpmathify( '10000' ),
    ( 'stone',                      'pound' )                               : mpmathify( '14' ),
    ( 'stone_us',                   'pound' )                               : mpmathify( '12.5' ),
    ( 'strike',                     'imperial_bushel' )                     : mpmathify( '2' ),
    ( 'sydharb',                    'liter' )                               : mpmathify( '5.62e11' ),
    ( 'tablespoon',                 'teaspoon' )                            : mpmathify( '3' ),
    ( 'teaspoon',                   'coffeespoon' )                         : mpmathify( '2' ),
    ( 'teaspoon',                   'dash' )                                : mpmathify( '8' ),
    ( 'teaspoon',                   'pinch' )                               : mpmathify( '16' ),
    ( 'teaspoon',                   'saltspoon' )                           : mpmathify( '4' ),
    ( 'teaspoon',                   'smidgen' )                             : mpmathify( '32' ),
    ( 'ten',                        'unity' )                               : mpmathify( '10' ),
    ( 'tesla',                      'ampere*henry/meter^2' )                : mpmathify( '1' ),
    ( 'tesla',                      'gauss' )                               : mpmathify( '10000' ),
    ( 'tesla',                      'joule/ampere*meter^2' )                : mpmathify( '1' ),
    ( 'tesla',                      'kilogram/ampere*second^2' )            : mpmathify( '1' ),
    ( 'tesla',                      'kilogram/coulomb*second' )             : mpmathify( '1' ),
    ( 'tesla',                      'newton*second/coulomb*meter' )         : mpmathify( '1' ),
    ( 'tesla',                      'newton/ampere*meter' )                 : mpmathify( '1' ),
    ( 'tesla',                      'second*volt/meter^2' )                 : mpmathify( '1' ),
    ( 'tesla',                      'second*volt/meter^2' )                 : mpmathify( '1' ),
    ( 'tesla',                      'weber/meter^2' )                       : mpmathify( '1' ),
    ( 'therm',                      'btu' )                                 : mpmathify( '100000' ),
    ( 'thirty',                     'unity' )                               : mpmathify( '30' ),
    ( 'thousand',                   'unity' )                               : mpmathify( '1000' ),
    ( 'three',                      'unity' )                               : mpmathify( '3' ),
    ( 'toe',                        'calorie' )                             : mpmathify( '1.0e10' ),
    ( 'ton',                        'pound' )                               : mpmathify( '2000' ),
    ( 'ton_of_TNT',                 'joule' )                               : mpmathify( '4.184e9' ),
    ( 'ton_of_TNT',                 'pound_of_TNT' )                        : mpmathify( '2000' ),
    ( 'ton_of_coal',                'joule' )                               : mpmathify( '29.288e9' ),
    ( 'tonne',                      'gram' )                                : mpmathify( '1.0e6' ),
    ( 'torr',                       'mmHg' )                                : mpmathify( '1' ),
    ( 'township',                   'acre' )                                : mpmathify( '23040' ),
    ( 'tredecillion',               'unity' )                               : mpmathify( '1.0e42' ),
    ( 'trillion',                   'unity' )                               : mpmathify( '1.0e12' ),
    ( 'trit',                       'nat' )                                 : log( 3 ),
    ( 'tropical_month',             'day' )                                 : mpmathify( '27.321582' ),
    ( 'troy_ounce',                 'gram' )                                : mpmathify( '31.1034768' ),
    ( 'troy_pound',                 'pound' )                               : mpmathify( '12' ),
    ( 'tryte',                      'trit' )                                : mpmathify( '6' ),   # as defined by the Setun computer
    ( 'tun',                        'gallon' )                              : mpmathify( '252' ),
    ( 'tun',                        'pipe' )                                : mpmathify( '2' ),
    ( 'two',                        'unity' )                               : mpmathify( '2' ),
    ( 'undecillion',                'unity' )                               : mpmathify( '1.0e36' ),
    ( 'unity',                      'billionth' )                           : mpmathify( '1.0e9' ),
    ( 'unity',                      'decillionth' )                         : mpmathify( '1.0e33' ),
    ( 'unity',                      'half' )                                : mpmathify( '2' ),
    ( 'unity',                      'millionth' )                           : mpmathify( '1.0e6' ),
    ( 'unity',                      'nonillionth' )                         : mpmathify( '1.0e30' ),
    ( 'unity',                      'octillionth' )                         : mpmathify( '1.0e27' ),
    ( 'unity',                      'percent' )                             : mpmathify( '100' ),
    ( 'unity',                      'quadrillionth' )                       : mpmathify( '1.0e15' ),
    ( 'unity',                      'quarter' )                             : mpmathify( '4' ),
    ( 'unity',                      'quintillionth' )                       : mpmathify( '1.0e18' ),
    ( 'unity',                      'septillionth' )                        : mpmathify( '1.0e24' ),
    ( 'unity',                      'sextillionth' )                        : mpmathify( '1.0e21' ),
    ( 'unity',                      'tenth' )                               : mpmathify( '10' ),
    ( 'unity',                      'third' )                               : mpmathify( '3' ),
    ( 'unity',                      'thousandth' )                          : mpmathify( '1000' ),
    ( 'unity',                      'trillionth' )                          : mpmathify( '1.0e12' ),
    ( 'usb1',                       'bit/second' )                          : mpmathify( '1.2e7' ),
    ( 'usb2',                       'bit/second' )                          : mpmathify( '2.8e8' ),
    ( 'usb3.0',                     'bit/second' )                          : mpmathify( '5.0e9' ),
    ( 'usb3.1',                     'bit/second' )                          : mpmathify( '1.0e10' ),
    ( 'versta',                     'meter' )                               : mpmathify( '1066.8' ),
    ( 'vigintillion',               'unity' )                               : mpmathify( '1.0e63' ),
    ( 'virgate',                    'bovate' )                              : mpmathify( '30' ),
    ( 'volt',                       'abvolt' )                              : mpmathify( '1.0e8' ),
    ( 'volt',                       'watt/ampere' )                         : mpmathify( '1' ),
    ( 'watt',                       'erg/second' )                          : mpmathify( '1.0e7' ),
    ( 'watt',                       'kilogram*meter^2/second^3' )           : mpmathify( '1' ),
    ( 'watt',                       'lusec' )                               : mpmathify( '7500' ),
    ( 'watt',                       'meter*newton/second' )                 : mpmathify( '1' ),
    ( 'watt/meter^2',               'kilogram/second^3' )                   : mpmathify( '1' ),
    ( 'weber',                      'maxwell' )                             : mpmathify( '1.0e8' ),
    ( 'weber',                      'meter^2*tesla' )                       : mpmathify( '1' ),
    ( 'weber',                      'second*volt' )                         : mpmathify( '1' ),
    ( 'weber',                      'unit_pole' )                           : mpmathify( '7957747.154594' ),
    ( 'week',                       'day' )                                 : mpmathify( '7' ),
    ( 'wey',                        'pound' )                               : mpmathify( '252' ),
    ( 'wine_barrel',                'wine_gallon' )                         : mpmathify( '31.5' ),
    ( 'wine_butt',                  'wine_gallon' )                         : mpmathify( '126' ),
    ( 'wine_gallon',                'gallon' )                              : mpmathify( '1' ),
    ( 'wine_hogshead',              'gallon' )                              : mpmathify( '63' ),
    ( 'wine_tun',                   'gallon' )                              : mpmathify( '252' ),
    ( 'wine_tun',                   'puncheon' )                            : mpmathify( '3' ),
    ( 'wine_tun',                   'rundlet' )                             : mpmathify( '14' ),
    ( 'wine_tun',                   'tierce' )                              : mpmathify( '6' ),
    ( 'wine_tun',                   'wine_pipe' )                           : mpmathify( '2' ),
    ( 'wood',                       'martin' )                              : mpmathify( '100' ),
    ( 'word',                       'bit' )                                 : mpmathify( '16' ),
    ( 'yard',                       'foot' )                                : mpmathify( '3' ),
    ( 'year',                       'day' )                                 : mpmathify( '365.25' ),   # Julian year = 365 and 1/4 days
    ( 'zentner',                    'gram' )                                : mpmathify( '50000' ),
    ( 'zolotnik',                   'dolya' )                               : mpmathify( '96' ),
}

