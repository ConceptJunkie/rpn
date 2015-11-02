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

from mpmath import *

from rpnConstantUtils import *


# //******************************************************************************
# //
# //  class OperatorInfo
# //
# //******************************************************************************

class OperatorInfo( ):
    def __init__( self, function, argCount = 0 ):
        self.function = function
        self.argCount = argCount


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are operators that take no arguments.
# //
# //******************************************************************************

constants = {
    # constant
    'aa_battery'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '15400' ), [ { 'joule' : 1 } ] ), 0 ),
    'apery_constant'                : OperatorInfo( apery, 0 ),
    'catalan_constant'              : OperatorInfo( catalan, 0 ),
    'champernowne_constant'         : OperatorInfo( getChampernowneConstant, 0 ),
    'copeland_erdos_constant'       : OperatorInfo( getCopelandErdosConstant, 0 ),
    'default'                       : OperatorInfo( lambda: mpmathify( '-1' ), 0 ),
    'e'                             : OperatorInfo( e, 0 ),
    'eddington_number'              : OperatorInfo( lambda: fmul( 136, power( 2, 256 ) ), 0 ),
    'euler_mascheroni_constant'     : OperatorInfo( euler, 0 ),
    'false'                         : OperatorInfo( lambda: mpmathify( '0' ), 0 ),
    'gallon_of_ethanol'             : OperatorInfo( lambda: RPNMeasurement( mpmathify( '8.4e7' ), [ { 'joule' : 1 } ] ), 0 ),
    'gallon_of_gasoline'            : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.2e8' ), [ { 'joule' : 1 } ] ), 0 ),
    'glaisher_constant'             : OperatorInfo( glaisher, 0 ),
    'infinity'                      : OperatorInfo( lambda: inf, 0 ),
    'itoi'                          : OperatorInfo( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'khinchin_constant'             : OperatorInfo( khinchin, 0 ),
    'merten_constant'               : OperatorInfo( mertens, 0 ),
    'mills_constant'                : OperatorInfo( getMillsConstant, 0 ),
    'negative_infinity'             : OperatorInfo( lambda: -inf, 0 ),
    'omega_constant'                : OperatorInfo( lambda: lambertw( 1 ), 0 ),
    'phi'                           : OperatorInfo( phi, 0 ),
    'pi'                            : OperatorInfo( pi, 0 ),
    'plastic_constant'              : OperatorInfo( getPlasticConstant, 0 ),
    'prevost_constant'              : OperatorInfo( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ), 0 ),
    'robbins_constant'              : OperatorInfo( getRobbinsConstant, 0 ),
    'sidereal_month'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '27.321661' ), [ { 'day' : 1 } ] ), 0 ),
    'sidereal_year'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '365.256360417' ), [ { 'day' : 1 } ] ), 0 ),
    'silver_ratio'                  : OperatorInfo( lambda: fadd( 1, sqrt( 2 ) ), 0 ),
    'tropical_year'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '365.24219' ), [ { 'day' : 1 } ] ), 0 ),
    'true'                          : OperatorInfo( lambda: mpmathify( 1 ), 0 ),
#    'density_of_hg'        13595.1 g/L (or kg/m3 ) :  Conventional density of mercury.
#    'density_of_water'

    # constant - physical constants
    'avogadro_number'               : OperatorInfo( lambda: mpmathify( '6.022140857e23' ), 0 ),
    'bohr_radius'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.2917721e-11' ), [ { 'meter' : 1 } ] ), 0 ),
    'boltzmann_constant'            : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.3806488e-23' ), [ { 'joule' : 1 }, { 'kelvin' : -1 } ] ), 0 ),
    'electric_constant'             : OperatorInfo( lambda: RPNMeasurement( mpmathify( '8.854187817e-12' ), [ { 'farad' : 1 }, { 'meter' : -1 } ] ), 0 ),
    'electron_charge'               : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.602176565e-19' ), [ { 'coulomb' : 1 } ] ), 0 ),
    'electron_mass'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '9.10938291e-28' ), [ { 'gram' : 1 } ] ), 0 ),
    'faraday_constant'              : OperatorInfo( lambda: RPNMeasurement( mpmathify( '96485.33289' ), [ { 'coulomb' : 1 }, { 'mole' : -1 } ] ), 0 ),
    'fine_structure_constant'       : OperatorInfo( lambda: mpmathify( '7.2973525664e-3' ), 0 ),
    'magnetic_constant'             : OperatorInfo( lambda: RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), [ { 'newton' : 1 }, { 'ampere' : -2 } ] ), 0 ),
    'newton_constant'               : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6.67408e-11' ), [ { 'meter' : 3 }, { 'kilogram' : -1 }, { 'second' : -2 } ] ), 0 ),
    'radiation_constant'            : OperatorInfo( lambda: RPNMeasurement( mpmathify( '7.5657e-16' ), [ { 'joule' : 1 }, { 'meter' : -3 }, { 'kelvin' : -4 } ] ), 0 ),
    'rydberg_constant'              : OperatorInfo( lambda: RPNMeasurement( mpmathify( '10973731.568508' ), { 'meter' : -1 } ), 0 ),
    'speed_of_light'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '299792458' ), [ { 'meter' : 1 }, { 'second' : -1 } ] ), 0 ),
    'stefan_boltzmann_constant'     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.670367e-8' ), [ { 'watt' : 1 }, { 'meter' : -2 }, { 'kelvin' : -4 } ] ), 0 ),
    'von_klitzing_constant'         : OperatorInfo( lambda: RPNMeasurement( mpmathify( '25812.807' ), [ { 'ohm' : 1 } ] ), 0 ),

    # constant - programming integer constants
    'max_char'                      : OperatorInfo( lambda: mpmathify( ( 1 << 7 ) - 1 ), 0 ),
    'max_double'                    : OperatorInfo( getMaxDouble, 0 ),
    'max_float'                     : OperatorInfo( getMaxFloat, 0 ),
    'max_long'                      : OperatorInfo( lambda: mpmathify( ( 1 << 31 ) - 1 ), 0 ),
    'max_longlong'                  : OperatorInfo( lambda: mpmathify( ( 1 << 63 ) - 1 ), 0 ),
    'max_quadlong'                  : OperatorInfo( lambda: mpmathify( ( 1 << 127 ) - 1 ), 0 ),
    'max_short'                     : OperatorInfo( lambda: mpmathify( ( 1 << 15 ) - 1 ), 0 ),
    'max_uchar'                     : OperatorInfo( lambda: mpmathify( ( 1 << 8 ) - 1 ), 0 ),
    'max_ulong'                     : OperatorInfo( lambda: mpmathify( ( 1 << 32 ) - 1 ), 0 ),
    'max_ulonglong'                 : OperatorInfo( lambda: mpmathify( ( 1 << 64 ) - 1 ), 0 ),
    'max_uquadlong'                 : OperatorInfo( lambda: mpmathify( ( 1 << 128 ) - 1 ), 0 ),
    'max_ushort'                    : OperatorInfo( lambda: mpmathify( ( 1 << 16 ) - 1 ), 0 ),
    'min_char'                      : OperatorInfo( lambda: mpmathify( -( 1 << 7 ) ), 0 ),
    'min_double'                    : OperatorInfo( getMinDouble, 0 ),
    'min_float'                     : OperatorInfo( getMinFloat, 0 ),
    'min_long'                      : OperatorInfo( lambda: mpmathify( -( 1 << 31 ) ), 0 ),
    'min_longlong'                  : OperatorInfo( lambda: mpmathify( -( 1 << 63 ) ), 0 ),
    'min_quadlong'                  : OperatorInfo( lambda: mpmathify( -( 1 << 127 ) ), 0 ),
    'min_short'                     : OperatorInfo( lambda: mpmathify( -( 1 << 15 ) ), 0 ),
    'min_uchar'                     : OperatorInfo( lambda: mpmathify( 0 ), 0 ),
    'min_ulong'                     : OperatorInfo( lambda: mpmathify( 0 ), 0 ),
    'min_ulonglong'                 : OperatorInfo( lambda: mpmathify( 0 ), 0 ),
    'min_uquadlong'                 : OperatorInfo( lambda: mpmathify( 0 ), 0 ),
    'min_ushort'                    : OperatorInfo( lambda: mpmathify( 0 ), 0 ),

    # constant - Planck constants
    'planck_angular_frequency'      : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.8548743' ), [ { 'second' : -1 } ] ), 0 ),
    'planck_area'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '2.61219618e-70' ), [ { 'square_meter' : 1 } ] ), 0 ),
    'planck_charge'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.875545956e-18' ), [ { 'coulomb' : 1 } ] ), 0 ),
    'planck_constant'               : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6.626070040e-34' ), [ { 'joule' : 1 }, { 'second' : 1 } ] ), 0 ),
    'planck_current'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.4789e25' ), [ { 'ampere' : 1 } ] ), 0 ),
    'planck_density'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.15518197484e+96' ), [ { 'kilogram' : 1 }, { 'meter' : -3 } ] ), 0 ),
    'planck_energy'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.220910e28' ), [ { 'electron-volt' : 1 } ] ), 0 ),
    'planck_energy_density'         : OperatorInfo( lambda: RPNMeasurement( mpmathify( '4.63298e113' ), [ { 'joule' : 1 }, { 'meter' : -3 } ] ), 0 ),
    'planck_force'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.2102947186e44' ), [ { 'newton' : 1 } ] ), 0 ),
    'planck_impedance'              : OperatorInfo( lambda: RPNMeasurement( mpmathify( '29.9792458' ), [ { 'ohm' : 1 } ] ), 0 ),
    'planck_intensity'              : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.38893e122' ), [ { 'watt' : 1 }, { 'meter' : -2 } ] ), 0 ),
    'planck_length'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.616229e-35' ), [ { 'meter' : 1 } ] ), 0 ),
    'planck_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '2.176470e-8' ), [ { 'kilogram' : 1 } ] ), 0 ),
    'planck_momentum'               : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6524.85' ), [ { 'gram' : 1 }, { 'meter' : 1 }, { 'second': -1 } ] ), 0 ),
    'planck_power'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.62831e52' ), [ { 'watt' : 1 } ] ), 0 ),
    'planck_pressure'               : OperatorInfo( lambda: RPNMeasurement( mpmathify( '4.63309e113' ), [ { 'pascal' : 1 } ] ), 0 ),
    'planck_temperature'            : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.416808e32' ), [ { 'kelvin' : 1 } ] ), 0 ),
    'planck_time'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.39116e-44' ), [ { 'second' : 1 } ] ), 0 ),
    'planck_voltage'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.04295e27' ), [ { 'volt' : 1 } ] ), 0 ),
    'planck_volume'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '4.22190722e-105' ), [ { 'cubic_meter' : 1 } ] ), 0 ),
    'reduced_planck_constant'       : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.054571800e-34' ), [ { 'joule' : 1 }, { 'second' : 1 } ] ), 0 ),

    # constant - subatomic particle constants
    'alpha_particle_mass'           : OperatorInfo( lambda: RPNMeasurement( mpmathify( '4.001506179125' ), [ { 'dalton' : 1 } ] ), 0 ),
    'deuteron_mass'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '2.013553212712' ), [ { 'dalton' : 1 } ] ), 0 ),
    'helion_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.0149322468' ), [ { 'dalton' : 1 } ] ), 0 ),
    'muon_mass'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '0.1134289267' ), [ { 'dalton' : 1 } ] ), 0 ),
    'neutron_mass'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.00866491600' ), [ { 'dalton' : 1 } ] ), 0 ),
    'proton_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.6726218e-27' ), [ { 'kilogram' : 1 } ] ), 0 ),
    'tau_mass'                      : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.90749' ), [ { 'dalton' : 1 } ] ), 0 ),
    'triton_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.0155007134' ), [ { 'dalton' : 1 } ] ), 0 ),

    # constant - heavenly body constants
    # sun_day
    'solar_luminosity'              : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.826e26' ), [ { 'watt' : 1 } ] ), 0 ),
    'solar_mass'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.988500e30' ), [ { 'kilogram' : 1 } ] ), 0 ),
    'solar_radius'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6.9599e8' ), [ { 'meter' : 1 } ] ), 0 ),
    'solar_volume'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.412e27' ), [ { 'meter' : 3 } ] ), 0 ),

    'mercury_day'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '58.785' ), [ { 'day' : 1 } ] ), 0 ),
    'mercury_mass'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '3.301e26' ), [ { 'kilogram' : 1 } ] ), 0 ),
    'mercury_radius'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '2.4397e6' ), [ { 'meter' : 1 } ] ), 0 ),
    'mercury_year'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '87.969' ), [ { 'day' : 1 } ] ), 0 ),

    'venus_day'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '243.01' ), [ { 'day' : 1 } ] ), 0 ),
    'venus_mass'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '4.8689952e27' ), [ { 'gram' : 1 } ] ), 0 ),
    # venus_radius
    'venus_year'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '0.61519726' ), [ { 'year' : 1 } ] ), 0 ),

    'earth_gravity'                 : OperatorInfo( lambda: RPNMeasurement( mpmathify( '9.806650' ), [ { 'meter' : 1 }, { 'second' : -2 } ] ), 0 ),
    'earth_mass'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.9742e27' ), [ { 'gram' : 1 } ] ), 0 ),
    'earth_radius'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6378136' ), [ { 'meter' : 1 } ] ), 0 ),

    #'moon_day'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1490' ),  'minute' )
    'moon_gravity'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.62' ), [ { 'meter' : 1 }, { 'second' : -2 } ] ), 0 ),
    # moon_mass
    # moon_radius
    # moon_orbit

    'mars_day'                      : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.02595675' ), [ { 'day' : 1 } ] ), 0 ),
    'mars_mass'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6.4191269e26' ), [ { 'gram' : 1 } ] ), 0 ),
    # mars_radius
    'mars_year'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.8808476' ), [ { 'year' : 1 } ] ), 0 ),

    'jupiter_day'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '9.92496' ), [ { 'hour' : 1 } ] ), 0 ),
    'jupiter_mass'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.8992e30' ), [ { 'gram' : 1 } ] ), 0 ),
    'jupiter_radius'                : OperatorInfo( lambda: RPNMeasurement( mpmathify( '7.1492e7' ), [ { 'meter' : 1 } ] ), 0 ),
    'jupiter_year'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '11.862615' ), [ { 'year' : 1 } ] ), 0 ),

    'saturn_day'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '0.4375' ), [ { 'day' : 1 } ] ), 0 ),
    'saturn_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '5.6865580e29' ), [ { 'gram' : 1 } ] ), 0 ),
    # saturn_radius
    'saturn_year'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '29.447498' ), [ { 'year' : 1 } ] ), 0 ),

    'uranus_day'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '0.65' ), [ { 'day' : 1 } ] ), 0 ),
    'uranus_mass'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '8.6848960e28' ), [ { 'gram' : 1 } ] ), 0 ),
    # uranus_radius
    'uranus_year'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '84.016846' ), [ { 'year' : 1 } ] ), 0 ),

    'neptune_day'                   : OperatorInfo( lambda: RPNMeasurement( mpmathify( '0.768' ), [ { 'day' : 1 } ] ), 0 ),
    'neptune_mass'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.0247e29' ), [ { 'gram' : 1 } ] ), 0 ),
    # neptune_radius
    'neptune_year'                  : OperatorInfo( lambda: RPNMeasurement( mpmathify( '164.79132' ), [ { 'year' : 1 } ] ), 0 ),

    'pluto_day'                     : OperatorInfo( lambda: RPNMeasurement( mpmathify( '6.3867' ), [ { 'day' : 1 } ] ), 0 ),
    'pluto_mass'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '1.4734074e25' ), [ { 'gram' : 1 } ] ), 0 ),
    # pluto_radius
    'pluto_year'                    : OperatorInfo( lambda: RPNMeasurement( mpmathify( '247.92065' ), [ { 'year' : 1 } ] ), 0 ),

    # constant - day of week operators
    'monday'                        : OperatorInfo( lambda: mpmathify( 1 ), 0 ),
    'tuesday'                       : OperatorInfo( lambda: mpmathify( 2 ), 0 ),
    'wednesday'                     : OperatorInfo( lambda: mpmathify( 3 ), 0 ),
    'thursday'                      : OperatorInfo( lambda: mpmathify( 4 ), 0 ),
    'friday'                        : OperatorInfo( lambda: mpmathify( 5 ), 0 ),
    'saturday'                      : OperatorInfo( lambda: mpmathify( 6 ), 0 ),
    'sunday'                        : OperatorInfo( lambda: mpmathify( 7 ), 0 ),

    # constant - month operators
    'january'                       : OperatorInfo( lambda: mpmathify( 1 ), 0 ),
    'february'                      : OperatorInfo( lambda: mpmathify( 2 ), 0 ),
    'march'                         : OperatorInfo( lambda: mpmathify( 3 ), 0 ),
    'april'                         : OperatorInfo( lambda: mpmathify( 4 ), 0 ),
    'may'                           : OperatorInfo( lambda: mpmathify( 5 ), 0 ),
    'june'                          : OperatorInfo( lambda: mpmathify( 6 ), 0 ),
    'july'                          : OperatorInfo( lambda: mpmathify( 7 ), 0 ),
    'august'                        : OperatorInfo( lambda: mpmathify( 8 ), 0 ),
    'september'                     : OperatorInfo( lambda: mpmathify( 9 ), 0 ),
    'october'                       : OperatorInfo( lambda: mpmathify( 10 ), 0 ),
    'november'                      : OperatorInfo( lambda: mpmathify( 11 ), 0 ),
    'december'                      : OperatorInfo( lambda: mpmathify( 12 ), 0 ),

    # Astronomical object operators

#    # Planetary moon operators
#    'phobos'                        : OperatorInfo( ephem.Phobos, 0 ),
#    'deimos'                        : OperatorInfo( ephem.Deimos, 0 ),
#    'io'                            : OperatorInfo( ephem.Io, 0 ),
#    'europa'                        : OperatorInfo( ephem.Europa, 0 ),
#    'ganymede'                      : OperatorInfo( ephem.Ganymede, 0 ),
#    'callisto'                      : OperatorInfo( ephem.Callisto, 0 ),
#    'mimas'                         : OperatorInfo( ephem.Mimas, 0 ),
#    'enceladus'                     : OperatorInfo( ephem.Enceladus, 0 ),
#    'tethys'                        : OperatorInfo( ephem.Tethys, 0 ),
#    'dione'                         : OperatorInfo( ephem.Dione, 0 ),
#    'rhea'                          : OperatorInfo( ephem.Rhea, 0 ),
#    'titan'                         : OperatorInfo( ephem.Titan, 0 ),
#    'hyperion'                      : OperatorInfo( ephem.Hyperion, 0 ),
#    'iapetus'                       : OperatorInfo( ephem.Iapetus, 0 ),
#    'ariel'                         : OperatorInfo( ephem.Ariel, 0 ),
#    'umbriel'                       : OperatorInfo( ephem.Umbriel, 0 ),
#    'titania'                       : OperatorInfo( ephem.Titania, 0 ),
#    'oberon'                        : OperatorInfo( ephem.Oberon, 0 ),
#    'miranda'                       : OperatorInfo( ephem.Miranda, 0 ),
}

#  Earth's approximate water volume (the total water supply of the world) is
#  1,338,000,000 km3 (321,000,000 mi3).[2]

