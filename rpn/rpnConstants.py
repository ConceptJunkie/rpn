#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnConstants.py
# //
# //  RPN command-line calculator constants
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import apery, bell, bernoulli, catalan, e, euler, exp, glaisher, \
                   inf, khinchin, lambertw, mertens, phi, pi

from rpn.rpnConstantUtils import getBoltzmannsConstant, getChampernowneConstant, \
        getCopelandErdosConstant, getElectricConstant, getElectronCharge, \
        getFineStructureConstant, getMaxDouble, getMaxFloat, getMillsConstant, \
        getMinDouble, getMinFloat, getNewtonsConstant, getPlanckCharge, \
        getPlanckConstant, getPlanckLength, getPlanckMass, getPlanckTemperature, \
        getPlanckTime, getPlasticConstant,  getReducedPlanckConstant, \
        getRobbinsConstant, getSpeedOfLight

#from rpn.rpnDeclarations import RPNOperator
from rpn.rpnMath import getPower, getRoot


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are operators that take no arguments.
# //
# //******************************************************************************
#
#constants = {
#    'default'                       : RPNOperator( lambda: -1, 0 ),
#    'false'                         : RPNOperator( lambda: 0, 0 ),
#    'true'                          : RPNOperator( lambda: 1, 0 ),
#
#    # day of week constants
#    'monday'                        : RPNOperator( lambda: 1, 0 ),
#    'tuesday'                       : RPNOperator( lambda: 2, 0 ),
#    'wednesday'                     : RPNOperator( lambda: 3, 0 ),
#    'thursday'                      : RPNOperator( lambda: 4, 0 ),
#    'friday'                        : RPNOperator( lambda: 5, 0 ),
#    'saturday'                      : RPNOperator( lambda: 6, 0 ),
#    'sunday'                        : RPNOperator( lambda: 7, 0 ),
#
#    # month constants
#    'january'                       : RPNOperator( lambda: 1, 0 ),
#    'february'                      : RPNOperator( lambda: 2, 0 ),
#    'march'                         : RPNOperator( lambda: 3, 0 ),
#    'april'                         : RPNOperator( lambda: 4, 0 ),
#    'may'                           : RPNOperator( lambda: 5, 0 ),
#    'june'                          : RPNOperator( lambda: 6, 0 ),
#    'july'                          : RPNOperator( lambda: 7, 0 ),
#    'august'                        : RPNOperator( lambda: 8, 0 ),
#    'september'                     : RPNOperator( lambda: 9, 0 ),
#    'october'                       : RPNOperator( lambda: 10, 0 ),
#    'november'                      : RPNOperator( lambda: 11, 0 ),
#    'december'                      : RPNOperator( lambda: 12, 0 ),
#
#    # mathematical constants
#    'apery_constant'                : RPNOperator( apery, 0 ),
#    'catalan_constant'              : RPNOperator( catalan, 0 ),
#    'champernowne_constant'         : RPNOperator( getChampernowneConstant, 0 ),
#    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant, 0 ),
#    'e'                             : RPNOperator( e, 0 ),
#    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ), 0 ),
#    'euler_mascheroni_constant'     : RPNOperator( euler, 0 ),
#    'glaisher_constant'             : RPNOperator( glaisher, 0 ),
#    'infinity'                      : RPNOperator( lambda: inf, 0 ),
#    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ), 0 ),
#    'khinchin_constant'             : RPNOperator( khinchin, 0 ),
#    'merten_constant'               : RPNOperator( mertens, 0 ),
#    'mills_constant'                : RPNOperator( getMillsConstant, 0 ),
#    'negative_infinity'             : RPNOperator( lambda: -inf, 0 ),
#    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ), 0 ),
#    'phi'                           : RPNOperator( phi, 0 ),
#    'pi'                            : RPNOperator( pi, 0 ),
#    'plastic_constant'              : RPNOperator( getPlasticConstant, 0 ),
#    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ), 0 ),
#    'robbins_constant'              : RPNOperator( getRobbinsConstant, 0 ),
#    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ), 0 ),
#
#    # physical quantities
#    'aa_battery'                    : RPNOperator( lambda: RPNMeasurement( '15400', 'joule' ), 0 ),
#    'gallon_of_ethanol'             : RPNOperator( lambda: RPNMeasurement( '8.4e7', 'joule' ), 0 ),
#    'gallon_of_gasoline'            : RPNOperator( lambda: RPNMeasurement( '1.2e8', 'joule' ), 0 ),
#    'density_of_water'              : RPNOperator( lambda: RPNMeasurement( '1000', 'kilogram/meter^3' ), 0 ),
#    'density_of_hg'                 : RPNOperator( lambda: RPNMeasurement( '13534', 'kilogram/meter^3' ), 0 ),
#
#    # physical constants
#    'avogadro_number'               : RPNOperator( lambda: '6.022140857e23', 0 ),
#    'bohr_radius'                   : RPNOperator( lambda: RPNMeasurement( '5.2917721e-11', [ { 'meter' : 1 } ] ), 0 ),
#    'boltzmann_constant'            : RPNOperator( getBoltzmannsConstant, 0 ),
#    'coulomb_constant'              : RPNOperator( lambda: RPNMeasurement( '8.987551787e9', 'joule*meter/coulomb^2' ), 0 ),
#    'electric_constant'             : RPNOperator( getElectricConstant, 0 ),
#    'electron_charge'               : RPNOperator( getElectronCharge, 0 ),
#    'faraday_constant'              : RPNOperator( lambda: RPNMeasurement( '96485.33289', 'coulomb/mole' ), 0 ),
#    'fine_structure_constant'       : RPNOperator( getFineStructureConstant, 0 ),
#    'magnetic_constant'             : RPNOperator( lambda: RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), 'newton/ampere^2' ), 0 ),
#    'newton_constant'               : RPNOperator( getNewtonsConstant, 0 ),
#    'radiation_constant'            : RPNOperator( lambda: RPNMeasurement( '7.5657e-16', 'kilogram/second^2*meter*kelvin^4' ), 0 ),
#    'rydberg_constant'              : RPNOperator( lambda: RPNMeasurement( '10973731.568508', 'meter^-1' ), 0 ),
#    'speed_of_light'                : RPNOperator( getSpeedOfLight, 0 ),
#    'stefan_boltzmann_constant'     : RPNOperator( lambda: RPNMeasurement( '5.670367e-8', 'watt/meter^2*kelvin^4' ), 0 ),
#    'vacuum_impedance'              : RPNOperator( lambda: RPNMeasurement( '376.730313461', 'ohm' ), 0 ),
#    'von_klitzing_constant'         : RPNOperator( lambda: RPNMeasurement( '25812.8074555', 'ohm' ), 0 ),
#
#    # programming integer constants
#    'max_char'                      : RPNOperator( lambda: ( 1 << 7 ) - 1, 0 ),
#    'max_double'                    : RPNOperator( getMaxDouble, 0 ),
#    'max_float'                     : RPNOperator( getMaxFloat, 0 ),
#    'max_long'                      : RPNOperator( lambda: ( 1 << 31 ) - 1, 0 ),
#    'max_longlong'                  : RPNOperator( lambda: ( 1 << 63 ) - 1, 0 ),
#    'max_quadlong'                  : RPNOperator( lambda: ( 1 << 127 ) - 1, 0 ),
#    'max_short'                     : RPNOperator( lambda: ( 1 << 15 ) - 1, 0 ),
#    'max_uchar'                     : RPNOperator( lambda: ( 1 << 8 ) - 1, 0 ),
#    'max_ulong'                     : RPNOperator( lambda: ( 1 << 32 ) - 1, 0 ),
#    'max_ulonglong'                 : RPNOperator( lambda: ( 1 << 64 ) - 1, 0 ),
#    'max_uquadlong'                 : RPNOperator( lambda: ( 1 << 128 ) - 1, 0 ),
#    'max_ushort'                    : RPNOperator( lambda: ( 1 << 16 ) - 1, 0 ),
#    'min_char'                      : RPNOperator( lambda: -( 1 << 7 ), 0 ),
#    'min_double'                    : RPNOperator( getMinDouble, 0 ),
#    'min_float'                     : RPNOperator( getMinFloat, 0 ),
#    'min_long'                      : RPNOperator( lambda: -( 1 << 31 ), 0 ),
#    'min_longlong'                  : RPNOperator( lambda: -( 1 << 63 ), 0 ),
#    'min_quadlong'                  : RPNOperator( lambda: -( 1 << 127 ), 0 ),
#    'min_short'                     : RPNOperator( lambda: -( 1 << 15 ), 0 ),
#    'min_uchar'                     : RPNOperator( lambda: 0, 0 ),
#    'min_ulong'                     : RPNOperator( lambda: 0, 0 ),
#    'min_ulonglong'                 : RPNOperator( lambda: 0, 0 ),
#    'min_uquadlong'                 : RPNOperator( lambda: 0, 0 ),
#    'min_ushort'                    : RPNOperator( lambda: 0, 0 ),
#
#    # Planck constants
#    'planck_constant'               : RPNOperator( getPlanckConstant, 0 ),
#    'reduced_planck_constant'       : RPNOperator( getReducedPlanckConstant, 0 ),
#
#    'planck_length'                 : RPNOperator( getPlanckLength, 0 ),
#    'planck_mass'                   : RPNOperator( getPlanckMass, 0 ),
#    'planck_time'                   : RPNOperator( getPlanckTime, 0 ),
#    'planck_charge'                 : RPNOperator( getPlanckCharge, 0 ),
#    'planck_temperature'            : RPNOperator( getPlanckTemperature, 0 ),
#
#    'planck_angular_frequency'      : RPNOperator( lambda: RPNMeasurement( '1.85487e43', 'second^-1' ), 0 ),
#    'planck_area'                   : RPNOperator( lambda: RPNMeasurement( '2.61219618e-70', 'meter^2' ), 0 ),
#    'planck_current'                : RPNOperator( lambda: RPNMeasurement( '3.4789e25', 'ampere' ), 0 ),
#    'planck_density'                : RPNOperator( lambda: RPNMeasurement( '5.15518197484e+96', 'kilogram/meter^3' ), 0 ),
#    'planck_energy'                 : RPNOperator( lambda: RPNMeasurement( '1.220910e28', 'electron-volt' ), 0 ),
#    'planck_energy_density'         : RPNOperator( lambda: RPNMeasurement( '4.63298e113', 'joule/meter^3' ), 0 ),
#    'planck_force'                  : RPNOperator( lambda: RPNMeasurement( '1.2102947186e44', 'newton' ), 0 ),
#    'planck_impedance'              : RPNOperator( lambda: RPNMeasurement( '29.9792458', 'ohm' ), 0 ),
#    'planck_intensity'              : RPNOperator( lambda: RPNMeasurement( '1.38893e122', 'watt/meter^2' ), 0 ),
#    'planck_momentum'               : RPNOperator( lambda: RPNMeasurement( '6.52485', 'kilogram*meter/second' ), 0 ),
#    'planck_power'                  : RPNOperator( lambda: RPNMeasurement( '3.62831e52', 'watt' ), 0 ),
#    'planck_pressure'               : RPNOperator( lambda: RPNMeasurement( '4.63309e113', 'pascal' ), 0 ),
#    'planck_voltage'                : RPNOperator( lambda: RPNMeasurement( '1.04295e27', 'volt' ), 0 ),
#    'planck_volume'                 : RPNOperator( lambda: RPNMeasurement( '4.22190722e-105', 'meter^3' ), 0 ),
#
#    # subatomic particle constants
#    'alpha_particle_mass'           : RPNOperator( lambda: RPNMeasurement( '6.644657230e-27', 'kilogram' ), 0 ),
#    'deuteron_mass'                 : RPNOperator( lambda: RPNMeasurement( '3.343583719e-27', 'kilogram' ), 0 ),
#    'electron_mass'                 : RPNOperator( lambda: RPNMeasurement( '9.10938356e-31', 'kilogram' ), 0 ),
#    'helion_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.006412700e-27', 'kilogram' ), 0 ),
#    'muon_mass'                     : RPNOperator( lambda: RPNMeasurement( '1.883531594e-28', 'kilogram' ), 0 ),
#    'neutron_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.674927471e-27', 'kilogram' ), 0 ),
#    'proton_mass'                   : RPNOperator( lambda: RPNMeasurement( '1.672621898e-27', 'kilogram' ), 0 ),
#    'tau_mass'                      : RPNOperator( lambda: RPNMeasurement( '3.16747e-27', 'kilogram' ), 0 ),
#    'triton_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.007356665e-27', 'kilogram' ), 0 ),
#
#    # heavenly body constants
#    # sun_day
#    'solar_luminosity'              : RPNOperator( lambda: RPNMeasurement( '3.826e26', 'watt' ), 0 ),
#    'solar_mass'                    : RPNOperator( lambda: RPNMeasurement( '1.988500e30', 'kilogram' ), 0 ),
#    'solar_radius'                  : RPNOperator( lambda: RPNMeasurement( '6.9599e8', 'meter' ), 0 ),
#    'solar_volume'                  : RPNOperator( lambda: RPNMeasurement( '1.412e27', 'meter^3' ), 0 ),
#
#    'mercury_mass'                  : RPNOperator( lambda: RPNMeasurement( '3.301e26', 'kilogram' ), 0 ),
#    # equitorial radius
#    'mercury_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4397e6', 'meter' ), 0 ),
#    # sidereal orbit period
#    'mercury_revolution'            : RPNOperator( lambda: RPNMeasurement( '87.969', 'day' ), 0 ),
#    'mercury_volume'                : RPNOperator( lambda: RPNMeasurement( '6.083e19', 'meter^3' ), 0 ),
#
#    'venus_mass'                    : RPNOperator( lambda: RPNMeasurement( '4.8689952e24', 'kilogram' ), 0 ),
#    'venus_radius'                  : RPNOperator( lambda: RPNMeasurement( '6.0518e6', 'meter' ), 0 ),
#    'venus_revolution'              : RPNOperator( lambda: RPNMeasurement( '224.701', 'day' ), 0 ),
#    'venus_volume'                  : RPNOperator( lambda: RPNMeasurement( '9.2843e20', 'meter^3' ), 0 ),
#
#    'earth_gravity'                 : RPNOperator( lambda: RPNMeasurement( '9.806650', 'meter/second^2' ), 0 ),
#    'earth_mass'                    : RPNOperator( lambda: RPNMeasurement( '5.9742e24', 'kilogram' ), 0 ),
#    'earth_radius'                  : RPNOperator( lambda: RPNMeasurement( '6378136', 'meter' ), 0 ),
#    'earth_volume'                  : RPNOperator( lambda: RPNMeasurement( '1.08321e21', 'meter^3' ), 0 ),
#    'sidereal_year'                 : RPNOperator( lambda: RPNMeasurement( '365.256360417', 'day' ), 0 ),
#    'tropical_year'                 : RPNOperator( lambda: RPNMeasurement( '365.24219', 'day' ), 0 ),
#
#    'moon_gravity'                  : RPNOperator( lambda: RPNMeasurement( '1.62', 'meter/second^2' ), 0 ),
#    'moon_mass'                     : RPNOperator( lambda: RPNMeasurement( '7.342e22', 'kilogram' ), 0 ),
#    'moon_radius'                   : RPNOperator( lambda: RPNMeasurement( '1.7381e6', 'meter' ), 0 ),
#    'moon_revolution'               : RPNOperator( lambda: RPNMeasurement( '27.3217', 'day' ), 0 ),
#    'moon_volume'                   : RPNOperator( lambda: RPNMeasurement( '2.1958e19', 'meter^3' ), 0 ),
#
#    'mars_mass'                     : RPNOperator( lambda: RPNMeasurement( '6.4191269e23', 'kilogram' ), 0 ),
#    'mars_radius'                   : RPNOperator( lambda: RPNMeasurement( '3.3962e6', 'meter' ), 0 ),
#    'mars_revolution'               : RPNOperator( lambda: RPNMeasurement( '686.980', 'day' ), 0 ),
#    'mars_volume'                   : RPNOperator( lambda: RPNMeasurement( '1.6318e20', 'meter^3' ), 0 ),
#
#    'jupiter_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.8983e27', 'kilogram' ), 0 ),
#    'jupiter_radius'                : RPNOperator( lambda: RPNMeasurement( '7.1492e7', 'meter' ), 0 ),
#    'jupiter_revolution'            : RPNOperator( lambda: RPNMeasurement( '11.862', 'year' ), 0 ),
#    'jupiter_volume'                : RPNOperator( lambda: RPNMeasurement( '1.43128e24', 'meter^3' ), 0 ),
#
#    'saturn_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.6836e26', 'kilogram' ), 0 ),
#    'saturn_radius'                 : RPNOperator( lambda: RPNMeasurement( '6.0268e7', 'meter' ), 0 ),
#    'saturn_revolution'             : RPNOperator( lambda: RPNMeasurement( '29.457', 'year' ), 0 ),
#    'saturn_volume'                 : RPNOperator( lambda: RPNMeasurement( '8.2713e23', 'meter^3' ), 0 ),
#
#    'uranus_mass'                   : RPNOperator( lambda: RPNMeasurement( '8.6816e25', 'kilogram' ), 0 ),
#    'uranus_radius'                 : RPNOperator( lambda: RPNMeasurement( '2.5559e7', 'meter' ), 0 ),
#    'uranus_revolution'             : RPNOperator( lambda: RPNMeasurement( '84.011', 'year' ), 0 ),
#    'uranus_volume'                 : RPNOperator( lambda: RPNMeasurement( '6.833e22', 'meter^3' ), 0 ),
#
#    'neptune_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.0242e26', 'kilogram' ), 0 ),
#    'neptune_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4764e7', 'meter' ), 0 ),
#    'neptune_revolution'            : RPNOperator( lambda: RPNMeasurement( '164.79', 'year' ), 0 ),
#    'neptune_volume'                : RPNOperator( lambda: RPNMeasurement( '6.254e22', 'meter^3' ), 0 ),
#
#    'pluto_mass'                    : RPNOperator( lambda: RPNMeasurement( '1.0303e22', 'kilogram' ), 0 ),
#    'pluto_radius'                  : RPNOperator( lambda: RPNMeasurement( '1.185e6', 'meter' ), 0 ),
#    'pluto_revolution'              : RPNOperator( lambda: RPNMeasurement( '247.94', 'year' ), 0 ),
#    'pluto_volume'                  : RPNOperator( lambda: RPNMeasurement( '6.97e18', 'meter^3' ), 0 ),
#
#    # Astronomical object operators
#
#    #    # Planetary moon operators
#    #    'phobos'                        : RPNOperator( ephem.Phobos, 0 ),
#    #    'deimos'                        : RPNOperator( ephem.Deimos, 0 ),
#    #    'io'                            : RPNOperator( ephem.Io, 0 ),
#    #    'europa'                        : RPNOperator( ephem.Europa, 0 ),
#    #    'ganymede'                      : RPNOperator( ephem.Ganymede, 0 ),
#    #    'callisto'                      : RPNOperator( ephem.Callisto, 0 ),
#    #    'mimas'                         : RPNOperator( ephem.Mimas, 0 ),
#    #    'enceladus'                     : RPNOperator( ephem.Enceladus, 0 ),
#    #    'tethys'                        : RPNOperator( ephem.Tethys, 0 ),
#    #    'dione'                         : RPNOperator( ephem.Dione, 0 ),
#    #    'rhea'                          : RPNOperator( ephem.Rhea, 0 ),
#    #    'titan'                         : RPNOperator( ephem.Titan, 0 ),
#    #    'hyperion'                      : RPNOperator( ephem.Hyperion, 0 ),
#    #    'iapetus'                       : RPNOperator( ephem.Iapetus, 0 ),
#    #    'ariel'                         : RPNOperator( ephem.Ariel, 0 ),
#    #    'umbriel'                       : RPNOperator( ephem.Umbriel, 0 ),
#    #    'titania'                       : RPNOperator( ephem.Titania, 0 ),
#    #    'oberon'                        : RPNOperator( ephem.Oberon, 0 ),
#    #    'miranda'                       : RPNOperator( ephem.Miranda, 0 ),
#}
#
#  Earth's approximate water volume (the total water supply of the world) is
#  1,338,000,000 km3 (321,000,000 mi3).[2]

