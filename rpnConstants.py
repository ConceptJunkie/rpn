#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnConstants.py
# //
# //  RPN command-line calculator constants
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from functools import lru_cache

from mpmath import *

from rpnConstantUtils import *
from rpnDeclarations import *
from rpnMath import exponentiate, getRoot


# //******************************************************************************
# //
# //  getNewtonsConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getNewtonsConstant( ):
    return RPNMeasurement( '6.67408e-11', 'meter^3/kilogram*second^2' )


# //******************************************************************************
# //
# //  getSpeedOfLight
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getSpeedOfLight( ):
    return RPNMeasurement( '299792458', 'meter/second' )


# //******************************************************************************
# //
# //  getElectricConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getElectricConstant( ):
    return RPNMeasurement( '8.854187817e-12', 'farad/meter' )


# //******************************************************************************
# //
# //  getPlanckConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckConstant( ):
    return RPNMeasurement( '6.626070040e-34', 'kilogram*meter^2/second' )


# //******************************************************************************
# //
# //  getReducedPlanckConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getReducedPlanckConstant( ):
    return getPlanckConstant( ).divide( fmul( 2, pi ) )


# //******************************************************************************
# //
# //  getFineStructureConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getFineStructureConstant( ):
    return mpmathify( '7.2973525664e-3' )


# //******************************************************************************
# //
# //  getElectronCharge
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getElectronCharge( ):
    return RPNMeasurement( '1.602176565e-19', 'coulomb' )


# //******************************************************************************
# //
# //  getBoltzmannsConstant
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getBoltzmannsConstant( ):
    return RPNMeasurement( '1.38064852e-23', 'kilogram*meter^2/second^2*kelvin' )


# //******************************************************************************
# //
# //  getPlanckLength
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckLength( ):
    return getRoot( getReducedPlanckConstant( ).multiply( getNewtonsConstant( ) ).divide(
                exponentiate( getSpeedOfLight( ), 3 ) ), 2 )


# //******************************************************************************
# //
# //  getPlanckMass
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckMass( ):
    return getRoot( getReducedPlanckConstant( ).multiply( getSpeedOfLight( ) ).divide(
                getNewtonsConstant( ) ), 2 )


# //******************************************************************************
# //
# //  getPlanckTime
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckTime( ):
    return getRoot( getReducedPlanckConstant( ).multiply( getNewtonsConstant( ) ).divide(
                exponentiate( getSpeedOfLight( ), 5 ) ), 2 )


# //******************************************************************************
# //
# //  getPlanckCharge
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckCharge( ):
    return getElectronCharge( ).divide( getRoot( getFineStructureConstant( ), 2 ) )


# //******************************************************************************
# //
# //  getPlanckTemperature
# //
# //******************************************************************************

@lru_cache( maxsize=1 )
def getPlanckTemperature( ):
    return getRoot( getReducedPlanckConstant( ).multiply( exponentiate( getSpeedOfLight( ), 5 ) ).
        divide( getNewtonsConstant( ).multiply( exponentiate( getBoltzmannsConstant( ), 2 ) ) ), 2 )


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are operators that take no arguments.
# //
# //******************************************************************************

constants = {
    'default'                       : RPNOperatorInfo( lambda: -1, 0 ),
    'false'                         : RPNOperatorInfo( lambda: 0, 0 ),
    'true'                          : RPNOperatorInfo( lambda: 1, 0 ),

    # day of week constants
    'monday'                        : RPNOperatorInfo( lambda: 1, 0 ),
    'tuesday'                       : RPNOperatorInfo( lambda: 2, 0 ),
    'wednesday'                     : RPNOperatorInfo( lambda: 3, 0 ),
    'thursday'                      : RPNOperatorInfo( lambda: 4, 0 ),
    'friday'                        : RPNOperatorInfo( lambda: 5, 0 ),
    'saturday'                      : RPNOperatorInfo( lambda: 6, 0 ),
    'sunday'                        : RPNOperatorInfo( lambda: 7, 0 ),

    # month constants
    'january'                       : RPNOperatorInfo( lambda: 1, 0 ),
    'february'                      : RPNOperatorInfo( lambda: 2, 0 ),
    'march'                         : RPNOperatorInfo( lambda: 3, 0 ),
    'april'                         : RPNOperatorInfo( lambda: 4, 0 ),
    'may'                           : RPNOperatorInfo( lambda: 5, 0 ),
    'june'                          : RPNOperatorInfo( lambda: 6, 0 ),
    'july'                          : RPNOperatorInfo( lambda: 7, 0 ),
    'august'                        : RPNOperatorInfo( lambda: 8, 0 ),
    'september'                     : RPNOperatorInfo( lambda: 9, 0 ),
    'october'                       : RPNOperatorInfo( lambda: 10, 0 ),
    'november'                      : RPNOperatorInfo( lambda: 11, 0 ),
    'december'                      : RPNOperatorInfo( lambda: 12, 0 ),

    # mathematical constants
    'apery_constant'                : RPNOperatorInfo( apery, 0 ),
    'catalan_constant'              : RPNOperatorInfo( catalan, 0 ),
    'champernowne_constant'         : RPNOperatorInfo( getChampernowneConstant, 0 ),
    'copeland_erdos_constant'       : RPNOperatorInfo( getCopelandErdosConstant, 0 ),
    'e'                             : RPNOperatorInfo( e, 0 ),
    'eddington_number'              : RPNOperatorInfo( lambda: fmul( 136, power( 2, 256 ) ), 0 ),
    'euler_mascheroni_constant'     : RPNOperatorInfo( euler, 0 ),
    'glaisher_constant'             : RPNOperatorInfo( glaisher, 0 ),
    'infinity'                      : RPNOperatorInfo( lambda: inf, 0 ),
    'itoi'                          : RPNOperatorInfo( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'khinchin_constant'             : RPNOperatorInfo( khinchin, 0 ),
    'merten_constant'               : RPNOperatorInfo( mertens, 0 ),
    'mills_constant'                : RPNOperatorInfo( getMillsConstant, 0 ),
    'negative_infinity'             : RPNOperatorInfo( lambda: -inf, 0 ),
    'omega_constant'                : RPNOperatorInfo( lambda: lambertw( 1 ), 0 ),
    'phi'                           : RPNOperatorInfo( phi, 0 ),
    'pi'                            : RPNOperatorInfo( pi, 0 ),
    'plastic_constant'              : RPNOperatorInfo( getPlasticConstant, 0 ),
    'prevost_constant'              : RPNOperatorInfo( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ), 0 ),
    'robbins_constant'              : RPNOperatorInfo( getRobbinsConstant, 0 ),
    'silver_ratio'                  : RPNOperatorInfo( lambda: fadd( 1, sqrt( 2 ) ), 0 ),

    # physical quantities
    'aa_battery'                    : RPNOperatorInfo( lambda: RPNMeasurement( '15400', 'joule' ), 0 ),
    'gallon_of_ethanol'             : RPNOperatorInfo( lambda: RPNMeasurement( '8.4e7', 'joule' ), 0 ),
    'gallon_of_gasoline'            : RPNOperatorInfo( lambda: RPNMeasurement( '1.2e8', 'joule' ), 0 ),
    'density_of_water'              : RPNOperatorInfo( lambda: RPNMeasurement( '1000', 'kilogram/meter^3' ), 0 ),
    'density_of_hg'                 : RPNOperatorInfo( lambda: RPNMeasurement( '13595.1', 'kilogram/meter^3' ), 0 ),

    # constant - physical constants
    'avogadro_number'               : RPNOperatorInfo( lambda: '6.022140857e23', 0 ),
    'bohr_radius'                   : RPNOperatorInfo( lambda: RPNMeasurement( '5.2917721e-11', [ { 'meter' : 1 } ] ), 0 ),
    'boltzmann_constant'            : RPNOperatorInfo( getBoltzmannsConstant, 0 ),
    'coulomb_constant'              : RPNOperatorInfo( lambda: RPNMeasurement( '8.987551787e9', 'newton*meter^2/coulomb^2' ), 0 ),
    'electric_constant'             : RPNOperatorInfo( getElectricConstant, 0 ),
    'electron_charge'               : RPNOperatorInfo( getElectronCharge, 0 ),
    'faraday_constant'              : RPNOperatorInfo( lambda: RPNMeasurement( '96485.33289', 'coulomb/mole' ), 0 ),
    'fine_structure_constant'       : RPNOperatorInfo( getFineStructureConstant, 0 ),
    'magnetic_constant'             : RPNOperatorInfo( lambda: RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), 'newton/ampere^2' ), 0 ),
    'newton_constant'               : RPNOperatorInfo( getNewtonsConstant, 0 ),
    'radiation_constant'            : RPNOperatorInfo( lambda: RPNMeasurement( '7.5657e-16', 'kilogram/second^2*meter*kelvin^4' ), 0 ),
    'rydberg_constant'              : RPNOperatorInfo( lambda: RPNMeasurement( '10973731.568508', 'meter^-1' ), 0 ),
    'speed_of_light'                : RPNOperatorInfo( getSpeedOfLight, 0 ),
    'stefan_boltzmann_constant'     : RPNOperatorInfo( lambda: RPNMeasurement( '5.670367e-8', 'watt/meter^2*kelvin^4' ), 0 ),
    'vacuum_impedance'              : RPNOperatorInfo( lambda: RPNMeasurement( '376.730313461', 'ohm' ), 0 ),
    'von_klitzing_constant'         : RPNOperatorInfo( lambda: RPNMeasurement( '25812.8074555', 'ohm' ), 0 ),

    # constant - programming integer constants
    'max_char'                      : RPNOperatorInfo( lambda: ( 1 << 7 ) - 1, 0 ),
    'max_double'                    : RPNOperatorInfo( getMaxDouble, 0 ),
    'max_float'                     : RPNOperatorInfo( getMaxFloat, 0 ),
    'max_long'                      : RPNOperatorInfo( lambda: ( 1 << 31 ) - 1, 0 ),
    'max_longlong'                  : RPNOperatorInfo( lambda: ( 1 << 63 ) - 1, 0 ),
    'max_quadlong'                  : RPNOperatorInfo( lambda: ( 1 << 127 ) - 1, 0 ),
    'max_short'                     : RPNOperatorInfo( lambda: ( 1 << 15 ) - 1, 0 ),
    'max_uchar'                     : RPNOperatorInfo( lambda: ( 1 << 8 ) - 1, 0 ),
    'max_ulong'                     : RPNOperatorInfo( lambda: ( 1 << 32 ) - 1, 0 ),
    'max_ulonglong'                 : RPNOperatorInfo( lambda: ( 1 << 64 ) - 1, 0 ),
    'max_uquadlong'                 : RPNOperatorInfo( lambda: ( 1 << 128 ) - 1, 0 ),
    'max_ushort'                    : RPNOperatorInfo( lambda: ( 1 << 16 ) - 1, 0 ),
    'min_char'                      : RPNOperatorInfo( lambda: -( 1 << 7 ), 0 ),
    'min_double'                    : RPNOperatorInfo( getMinDouble, 0 ),
    'min_float'                     : RPNOperatorInfo( getMinFloat, 0 ),
    'min_long'                      : RPNOperatorInfo( lambda: -( 1 << 31 ), 0 ),
    'min_longlong'                  : RPNOperatorInfo( lambda: -( 1 << 63 ), 0 ),
    'min_quadlong'                  : RPNOperatorInfo( lambda: -( 1 << 127 ), 0 ),
    'min_short'                     : RPNOperatorInfo( lambda: -( 1 << 15 ), 0 ),
    'min_uchar'                     : RPNOperatorInfo( lambda: 0, 0 ),
    'min_ulong'                     : RPNOperatorInfo( lambda: 0, 0 ),
    'min_ulonglong'                 : RPNOperatorInfo( lambda: 0, 0 ),
    'min_uquadlong'                 : RPNOperatorInfo( lambda: 0, 0 ),
    'min_ushort'                    : RPNOperatorInfo( lambda: 0, 0 ),

    # constant - Planck constants
    'planck_constant'               : RPNOperatorInfo( getPlanckConstant, 0 ),
    'reduced_planck_constant'       : RPNOperatorInfo( getReducedPlanckConstant, 0 ),

    'planck_length'                 : RPNOperatorInfo( getPlanckLength, 0 ),
    'planck_mass'                   : RPNOperatorInfo( getPlanckMass, 0 ),
    'planck_time'                   : RPNOperatorInfo( getPlanckTime, 0 ),
    'planck_charge'                 : RPNOperatorInfo( getPlanckCharge, 0 ),
    'planck_temperature'            : RPNOperatorInfo( getPlanckTemperature, 0 ),

    'planck_angular_frequency'      : RPNOperatorInfo( lambda: RPNMeasurement( '1.85487e43', 'second^-1' ), 0 ),
    'planck_area'                   : RPNOperatorInfo( lambda: RPNMeasurement( '2.61219618e-70', 'meter^2' ), 0 ),
    'planck_current'                : RPNOperatorInfo( lambda: RPNMeasurement( '3.4789e25', 'ampere' ), 0 ),
    'planck_density'                : RPNOperatorInfo( lambda: RPNMeasurement( '5.15518197484e+96', 'kilogram/meter^3' ), 0 ),
    'planck_energy'                 : RPNOperatorInfo( lambda: RPNMeasurement( '1.220910e28', 'electron-volt' ), 0 ),
    'planck_energy_density'         : RPNOperatorInfo( lambda: RPNMeasurement( '4.63298e113', 'joule/meter^3' ), 0 ),
    'planck_force'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.2102947186e44', 'newton' ), 0 ),
    'planck_impedance'              : RPNOperatorInfo( lambda: RPNMeasurement( '29.9792458', 'ohm' ), 0 ),
    'planck_intensity'              : RPNOperatorInfo( lambda: RPNMeasurement( '1.38893e122', 'watt/meter^2' ), 0 ),
    'planck_momentum'               : RPNOperatorInfo( lambda: RPNMeasurement( '6.52485', 'kilogram*meter/second' ), 0 ),
    'planck_power'                  : RPNOperatorInfo( lambda: RPNMeasurement( '3.62831e52', 'watt' ), 0 ),
    'planck_pressure'               : RPNOperatorInfo( lambda: RPNMeasurement( '4.63309e113', 'pascal' ), 0 ),
    'planck_voltage'                : RPNOperatorInfo( lambda: RPNMeasurement( '1.04295e27', 'volt' ), 0 ),
    'planck_volume'                 : RPNOperatorInfo( lambda: RPNMeasurement( '4.22190722e-105', 'meter^3' ), 0 ),

    # constant - subatomic particle constants
    'alpha_particle_mass'           : RPNOperatorInfo( lambda: RPNMeasurement( '6.644657230e-27', 'kilogram' ), 0 ),
    'deuteron_mass'                 : RPNOperatorInfo( lambda: RPNMeasurement( '3.343583719e-27', 'kilogram' ), 0 ),
    'electron_mass'                 : RPNOperatorInfo( lambda: RPNMeasurement( '9.10938356e-31', 'kilogram' ), 0 ),
    'helion_mass'                   : RPNOperatorInfo( lambda: RPNMeasurement( '5.006412700e-27', 'kilogram' ), 0 ),
    'muon_mass'                     : RPNOperatorInfo( lambda: RPNMeasurement( '1.883531594e-28', 'kilogram' ), 0 ),
    'neutron_mass'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.674927471e-27', 'kilogram' ), 0 ),
    'proton_mass'                   : RPNOperatorInfo( lambda: RPNMeasurement( '1.672621898e-27', 'kilogram' ), 0 ),
    'tau_mass'                      : RPNOperatorInfo( lambda: RPNMeasurement( '3.16747e-27', 'kilogram' ), 0 ),
    'triton_mass'                   : RPNOperatorInfo( lambda: RPNMeasurement( '5.007356665e-27', 'kilogram' ), 0 ),

    # constant - heavenly body constants
    # sun_day
    'solar_luminosity'              : RPNOperatorInfo( lambda: RPNMeasurement( '3.826e26', 'watt' ), 0 ),
    'solar_mass'                    : RPNOperatorInfo( lambda: RPNMeasurement( '1.988500e30', 'kilogram' ), 0 ),
    'solar_radius'                  : RPNOperatorInfo( lambda: RPNMeasurement( '6.9599e8', 'meter' ), 0 ),
    'solar_volume'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.412e27', 'meter^3' ), 0 ),

    'mercury_mass'                  : RPNOperatorInfo( lambda: RPNMeasurement( '3.301e26', 'kilogram' ), 0 ),
    # equitorial radius
    'mercury_radius'                : RPNOperatorInfo( lambda: RPNMeasurement( '2.4397e6', 'meter' ), 0 ),
    # sidereal orbit period
    'mercury_revolution'            : RPNOperatorInfo( lambda: RPNMeasurement( '87.969', 'day' ), 0 ),
    'mercury_volume'                : RPNOperatorInfo( lambda: RPNMeasurement( '6.083e19', 'meter^3' ), 0 ),

    'venus_mass'                    : RPNOperatorInfo( lambda: RPNMeasurement( '4.8689952e24', 'kilogram' ), 0 ),
    'venus_radius'                  : RPNOperatorInfo( lambda: RPNMeasurement( '6.0518e6', 'meter' ), 0 ),
    'venus_revolution'              : RPNOperatorInfo( lambda: RPNMeasurement( '224.701', 'day' ), 0 ),
    'venus_volume'                  : RPNOperatorInfo( lambda: RPNMeasurement( '9.2843e20', 'meter^3' ), 0 ),

    'earth_gravity'                 : RPNOperatorInfo( lambda: RPNMeasurement( '9.806650', 'meter/second^2' ), 0 ),
    'earth_mass'                    : RPNOperatorInfo( lambda: RPNMeasurement( '5.9742e24', 'kilogram' ), 0 ),
    'earth_radius'                  : RPNOperatorInfo( lambda: RPNMeasurement( '6378136', 'meter' ), 0 ),
    'earth_volume'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.08321e21', 'meter^3' ), 0 ),
    'sidereal_year'                 : RPNOperatorInfo( lambda: RPNMeasurement( '365.256360417', 'day' ), 0 ),
    'tropical_year'                 : RPNOperatorInfo( lambda: RPNMeasurement( '365.24219', 'day' ), 0 ),

    'moon_gravity'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.62', 'meter/second^2' ), 0 ),
    'moon_mass'                     : RPNOperatorInfo( lambda: RPNMeasurement( '7.342e22', 'kilogram' ), 0 ),
    'moon_radius'                   : RPNOperatorInfo( lambda: RPNMeasurement( '1.7381e6', 'meter' ), 0 ),
    'moon_revolution'               : RPNOperatorInfo( lambda: RPNMeasurement( '27.3217', 'day' ), 0 ),
    'moon_volume'                   : RPNOperatorInfo( lambda: RPNMeasurement( '2.1958e19', 'meter^3' ), 0 ),

    'mars_mass'                     : RPNOperatorInfo( lambda: RPNMeasurement( '6.4191269e23', 'kilogram' ), 0 ),
    'mars_radius'                   : RPNOperatorInfo( lambda: RPNMeasurement( '3.3962e6', 'meter' ), 0 ),
    'mars_revolution'               : RPNOperatorInfo( lambda: RPNMeasurement( '686.980', 'day' ), 0 ),
    'mars_volume'                   : RPNOperatorInfo( lambda: RPNMeasurement( '1.6318e20', 'meter^3' ), 0 ),

    'jupiter_mass'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.8983e27', 'kilogram' ), 0 ),
    'jupiter_radius'                : RPNOperatorInfo( lambda: RPNMeasurement( '7.1492e7', 'meter' ), 0 ),
    'jupiter_revolution'            : RPNOperatorInfo( lambda: RPNMeasurement( '11.862', 'year' ), 0 ),
    'jupiter_volume'                : RPNOperatorInfo( lambda: RPNMeasurement( '1.43128e24', 'meter^3' ), 0 ),

    'saturn_mass'                   : RPNOperatorInfo( lambda: RPNMeasurement( '5.6836e26', 'kilogram' ), 0 ),
    'saturn_radius'                 : RPNOperatorInfo( lambda: RPNMeasurement( '6.0268e7', 'meter' ), 0 ),
    'saturn_revolution'             : RPNOperatorInfo( lambda: RPNMeasurement( '29.457', 'year' ), 0 ),
    'saturn_volume'                 : RPNOperatorInfo( lambda: RPNMeasurement( '8.2713e23', 'meter^3' ), 0 ),

    'uranus_mass'                   : RPNOperatorInfo( lambda: RPNMeasurement( '8.6816e25', 'kilogram' ), 0 ),
    'uranus_radius'                 : RPNOperatorInfo( lambda: RPNMeasurement( '2.5559e7', 'meter' ), 0 ),
    'uranus_revolution'             : RPNOperatorInfo( lambda: RPNMeasurement( '84.011', 'year' ), 0 ),
    'uranus_volume'                 : RPNOperatorInfo( lambda: RPNMeasurement( '6.833e22', 'meter^3' ), 0 ),

    'neptune_mass'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.0242e26', 'kilogram' ), 0 ),
    'neptune_radius'                : RPNOperatorInfo( lambda: RPNMeasurement( '2.4764e7', 'meter' ), 0 ),
    'neptune_revolution'            : RPNOperatorInfo( lambda: RPNMeasurement( '164.79', 'year' ), 0 ),
    'neptune_volume'                : RPNOperatorInfo( lambda: RPNMeasurement( '6.254e22', 'meter^3' ), 0 ),

    'pluto_mass'                    : RPNOperatorInfo( lambda: RPNMeasurement( '1.0303e22', 'kilogram' ), 0 ),
    'pluto_radius'                  : RPNOperatorInfo( lambda: RPNMeasurement( '1.185e6', 'meter' ), 0 ),
    'pluto_revolution'              : RPNOperatorInfo( lambda: RPNMeasurement( '247.94', 'year' ), 0 ),
    'pluto_volume'                  : RPNOperatorInfo( lambda: RPNMeasurement( '6.97e18', 'meter^3' ), 0 ),

    # Astronomical object operators

    #    # Planetary moon operators
    #    'phobos'                        : RPNOperatorInfo( ephem.Phobos, 0 ),
    #    'deimos'                        : RPNOperatorInfo( ephem.Deimos, 0 ),
    #    'io'                            : RPNOperatorInfo( ephem.Io, 0 ),
    #    'europa'                        : RPNOperatorInfo( ephem.Europa, 0 ),
    #    'ganymede'                      : RPNOperatorInfo( ephem.Ganymede, 0 ),
    #    'callisto'                      : RPNOperatorInfo( ephem.Callisto, 0 ),
    #    'mimas'                         : RPNOperatorInfo( ephem.Mimas, 0 ),
    #    'enceladus'                     : RPNOperatorInfo( ephem.Enceladus, 0 ),
    #    'tethys'                        : RPNOperatorInfo( ephem.Tethys, 0 ),
    #    'dione'                         : RPNOperatorInfo( ephem.Dione, 0 ),
    #    'rhea'                          : RPNOperatorInfo( ephem.Rhea, 0 ),
    #    'titan'                         : RPNOperatorInfo( ephem.Titan, 0 ),
    #    'hyperion'                      : RPNOperatorInfo( ephem.Hyperion, 0 ),
    #    'iapetus'                       : RPNOperatorInfo( ephem.Iapetus, 0 ),
    #    'ariel'                         : RPNOperatorInfo( ephem.Ariel, 0 ),
    #    'umbriel'                       : RPNOperatorInfo( ephem.Umbriel, 0 ),
    #    'titania'                       : RPNOperatorInfo( ephem.Titania, 0 ),
    #    'oberon'                        : RPNOperatorInfo( ephem.Oberon, 0 ),
    #    'miranda'                       : RPNOperatorInfo( ephem.Miranda, 0 ),
}

#  Earth's approximate water volume (the total water supply of the world) is
#  1,338,000,000 km3 (321,000,000 mi3).[2]

