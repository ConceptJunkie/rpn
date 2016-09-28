#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import difflib
import inspect
import itertools
import struct

from enum import Enum
from random import randrange

from mpmath import acosh, acot, acoth, acsc, acsch, agm, altzeta, arg, asec, \
                   asech, asin, asinh, atan, atanh, barnesg, beta, conj, cosh, \
                   cos, coth, csc, csch, fac2, fadd, fmod, harmonic, hyperfac, \
                   lambertw, li, limit, ln, loggamma, nprod, nsum, polyexp, \
                   polylog, plot, psi, rand, sec, sech, sin, sinh, superfac, \
                   tan, tanh, unitroots, zeta

from rpnAliases import dumpAliases

from rpnAstronomy import *
from rpnCalendar import *
from rpnChemistry import *
from rpnCombinatorics import *
from rpnComputer import *
from rpnConstants import *
from rpnConstantUtils import *
from rpnDateTime import *
from rpnDice import *
from rpnDeclarations import *
from rpnFactor import *
from rpnGeometry import *
from rpnInput import *
from rpnLexicographic import *
from rpnList import *
from rpnLocation import *
from rpnMath import *
from rpnMeasurement import *
from rpnModifiers import *
from rpnName import *
from rpnNumberTheory import *
from rpnPersistence import *
from rpnPhysics import *
from rpnPolynomials import *
from rpnPolytope import *
from rpnPrimeUtils import *
from rpnSettings import *
from rpnUtils import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNOperator
# //
# //******************************************************************************

class RPNOperator( object ):
    measurementsAllowed = True
    measurementsNotAllowed = False

    Default = 0                 # any argument is valid
    Real = 1
    NonnegativeReal = 2         # real >= 0
    Integer = 3
    NonnegativeInteger = 5      # integer >= 0
    PositiveInteger = 4         # integer >= 1
    String = 6
    DateTime = 7
    Location = 8                # location object (operators will automatically convert a string)
    Boolean = 9                 # 0 or 1
    Measurement = 10
    AstronomicalObject = 11
    List = 12                   # the argument must be a list
    Generator = 13              # Generator needs to be a separate type now, but eventually it should be equivalent to List
    Function = 14

    """This class represents all the data needed to define an operator."""
    def __init__( self, function, argCount, argTypes = None, allowMeasurements = measurementsNotAllowed ):
        self.function = function
        self.argCount = argCount

        if argTypes is None:
            self.argTypes = list( )
        else:
            self.argTypes = argTypes

        self.allowMeasurements = allowMeasurements

    @staticmethod
    def validateArgType( self, term, arg, argType ):
        if isinstance( arg, ( list, RPNGenerator ) ) and argType not in ( RPNOperator.List, RPNOperator.Generator ):
            return True

        if argType == RPNOperator.Default:
            pass
        elif argType == RPNOperator.Real and im( arg ):
            raise ValueError( '\'' + term + '\':  real argument expected' )
        elif argType == RPNOperator.NonnegativeReal and ( im( arg ) or arg < 0 ):
            raise ValueError( '\'' + term + '\':  non-negative real argument expected' )
        elif argType == RPNOperator.Integer and arg != floor( arg ):
            raise ValueError( '\'' + term + '\':  integer argument expected' )
        elif argType == RPNOperator.NonnegativeInteger and arg != floor( arg ) or arg < 0:
            raise ValueError( '\'' + term + '\':  non-negative integer argument expected' )
        elif argType == RPNOperator.PositiveInteger and arg != floor( arg ) or arg < 1:
            raise ValueError( '\'' + term + '\':  positive integer argument expected' )
        elif argType == RPNOperator.String and not isinstance( arg, str ):
            raise ValueError( '\'' + term + '\':  string argument expected' )
        elif argType == RPNOperator.DateTime and not isinstance( arg, RPNDateTime ):
            raise ValueError( '\'' + term + '\':  date-time argument expected' )
        elif argType == RPNOperator.Location and not isinstance( arg, ( RPNLocation, str ) ):
            raise ValueError( '\'' + term + '\':  location argument expected' )
        elif argType == RPNOperator.Boolean and arg != 0 and arg != 1:
            raise ValueError( '\'' + term + '\':  boolean argument expected (0 or 1)' )
        elif argType == RPNOperator.Measurement and not isinstance( arg, RPNMeasurement ):
            raise ValueError( '\'' + term + '\':  measurement argument expected' )
        elif argType == RPNOperator.AstronomicalObject:
            pass
        elif argType == RPNOperator.List and not isinstance( arg, ( list, RPNGenerator ) ):
            raise ValueError( '\'' + term + '\':  list argument expected' )
        elif argType == RPNOperator.Generator and not isinstance( arg, RPNGenerator ):
            raise ValueError( '\'' + term + '\':  generator argument expected' )
        elif argType == RPNOperator.Function and not isinstance( arg, RPNFunction ):
            raise ValueError( '\'' + term + '\':  function argument expected' )

    def evaluate( self, term, index, currentValueList ):
        # handle a regular operator
        argsNeeded = self.argCount

        # first we validate, and make sure the operator has enough arguments
        if len( currentValueList ) < argsNeeded:
            abortArgsNeeded( term, index, argsNeeded )
            return False

        if argsNeeded == 0:
            result = self.function( )
        else:
            argList = list( )

            if g.operatorList:
                g.operatorsInList += 1

            # build argument list
            for i in range( 0, argsNeeded ):
                if g.operatorList:
                    arg = currentValueList[ g.lastOperand - i ]

                    if argsNeeded > g.operandsToRemove:
                        g.operandsToRemove = argsNeeded
                else:
                    arg = checkForVariable( currentValueList.pop( ) )

                    if term != 'set' and isinstance( arg, RPNVariable ):
                        arg = arg.getValue( )

                argList.append( arg if isinstance( arg, ( list, RPNGenerator ) ) else [ arg ] )

            # argument validation
            #for i, arg in enumerate( argList ):
            #    self.validateArgType( term, arg, self.argTypes[ i ] )

            #print( 'argList', *reversed( argList ) )
            #print( 'self.function', self.function )

            result = callers[ argsNeeded ]( self.function, *argList )
            #result = list( map( self.function, *reversed( argList ) ) )

        # process results
        newResult = list( )

        if isinstance( result, RPNGenerator ):
            newResult.append( result )
        else:
            if not isinstance( result, list ):
                result = [ result ]

            for item in result:
                if isinstance( item, RPNMeasurement ) and item.getUnits( ) == { }:
                    newResult.append( item.value )
                else:
                    newResult.append( item )

        if len( newResult ) == 1:
            newResult = newResult[ 0 ]

        if term not in sideEffectOperators:
            currentValueList.append( newResult )

        return True


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are operators that take no arguments.
# //
# //******************************************************************************

constants = {
    'default'                       : RPNOperator( lambda: -1, 0 ),
    'false'                         : RPNOperator( lambda: 0, 0 ),
    'true'                          : RPNOperator( lambda: 1, 0 ),

    # day of week constants
    'monday'                        : RPNOperator( lambda: 1, 0 ),
    'tuesday'                       : RPNOperator( lambda: 2, 0 ),
    'wednesday'                     : RPNOperator( lambda: 3, 0 ),
    'thursday'                      : RPNOperator( lambda: 4, 0 ),
    'friday'                        : RPNOperator( lambda: 5, 0 ),
    'saturday'                      : RPNOperator( lambda: 6, 0 ),
    'sunday'                        : RPNOperator( lambda: 7, 0 ),

    # month constants
    'january'                       : RPNOperator( lambda: 1, 0 ),
    'february'                      : RPNOperator( lambda: 2, 0 ),
    'march'                         : RPNOperator( lambda: 3, 0 ),
    'april'                         : RPNOperator( lambda: 4, 0 ),
    'may'                           : RPNOperator( lambda: 5, 0 ),
    'june'                          : RPNOperator( lambda: 6, 0 ),
    'july'                          : RPNOperator( lambda: 7, 0 ),
    'august'                        : RPNOperator( lambda: 8, 0 ),
    'september'                     : RPNOperator( lambda: 9, 0 ),
    'october'                       : RPNOperator( lambda: 10, 0 ),
    'november'                      : RPNOperator( lambda: 11, 0 ),
    'december'                      : RPNOperator( lambda: 12, 0 ),

    # mathematical constants
    'apery_constant'                : RPNOperator( apery, 0 ),
    'catalan_constant'              : RPNOperator( catalan, 0 ),
    'champernowne_constant'         : RPNOperator( getChampernowneConstant, 0 ),
    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant, 0 ),
    'e'                             : RPNOperator( e, 0 ),
    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ), 0 ),
    'euler_mascheroni_constant'     : RPNOperator( euler, 0 ),
    'glaisher_constant'             : RPNOperator( glaisher, 0 ),
    'infinity'                      : RPNOperator( lambda: inf, 0 ),
    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'khinchin_constant'             : RPNOperator( khinchin, 0 ),
    'merten_constant'               : RPNOperator( mertens, 0 ),
    'mills_constant'                : RPNOperator( getMillsConstant, 0 ),
    'negative_infinity'             : RPNOperator( lambda: -inf, 0 ),
    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ), 0 ),
    'phi'                           : RPNOperator( phi, 0 ),
    'pi'                            : RPNOperator( pi, 0 ),
    'plastic_constant'              : RPNOperator( getPlasticConstant, 0 ),
    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ), 0 ),
    'robbins_constant'              : RPNOperator( getRobbinsConstant, 0 ),
    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ), 0 ),

    # physical quantities
    'aa_battery'                    : RPNOperator( lambda: RPNMeasurement( '15400', 'joule' ), 0 ),
    'gallon_of_ethanol'             : RPNOperator( lambda: RPNMeasurement( '8.4e7', 'joule' ), 0 ),
    'gallon_of_gasoline'            : RPNOperator( lambda: RPNMeasurement( '1.2e8', 'joule' ), 0 ),
    'density_of_water'              : RPNOperator( lambda: RPNMeasurement( '1000', 'kilogram/meter^3' ), 0 ),
    'density_of_hg'                 : RPNOperator( lambda: RPNMeasurement( '13595.1', 'kilogram/meter^3' ), 0 ),
    'solar_constant'                : RPNOperator( lambda: RPNMeasurement( '1360.8', 'watt/meter^2' ), 0 ),  # average... it varies slightly

    # physical constants
    'avogadro_number'               : RPNOperator( lambda: '6.022140857e23', 0 ),
    'bohr_radius'                   : RPNOperator( lambda: RPNMeasurement( '5.2917721e-11', [ { 'meter' : 1 } ] ), 0 ),
    'boltzmann_constant'            : RPNOperator( getBoltzmannsConstant, 0 ),
    'coulomb_constant'              : RPNOperator( lambda: RPNMeasurement( '8.987551787e9', 'joule*meter/coulomb^2' ), 0 ),
    'electric_constant'             : RPNOperator( getElectricConstant, 0 ),
    'electron_charge'               : RPNOperator( getElectronCharge, 0 ),
    'faraday_constant'              : RPNOperator( lambda: RPNMeasurement( '96485.33289', 'coulomb/mole' ), 0 ),
    'fine_structure_constant'       : RPNOperator( getFineStructureConstant, 0 ),
    'magnetic_constant'             : RPNOperator( lambda: RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), 'joule/ampere^2*meter' ), 0 ),
    'newton_constant'               : RPNOperator( getNewtonsConstant, 0 ),
    'radiation_constant'            : RPNOperator( lambda: RPNMeasurement( '7.5657e-16', 'kilogram/second^2*meter*kelvin^4' ), 0 ),
    'rydberg_constant'              : RPNOperator( lambda: RPNMeasurement( '10973731.568508', 'meter^-1' ), 0 ),
    'speed_of_light'                : RPNOperator( getSpeedOfLight, 0 ),
    'stefan_boltzmann_constant'     : RPNOperator( lambda: RPNMeasurement( '5.670367e-8', 'watt/meter^2*kelvin^4' ), 0 ),
    'vacuum_impedance'              : RPNOperator( lambda: RPNMeasurement( '376.730313461', 'ohm' ), 0 ),
    'von_klitzing_constant'         : RPNOperator( lambda: RPNMeasurement( '25812.8074555', 'ohm' ), 0 ),

    # programming integer constants
    'max_char'                      : RPNOperator( lambda: ( 1 << 7 ) - 1, 0 ),
    'max_double'                    : RPNOperator( getMaxDouble, 0 ),
    'max_float'                     : RPNOperator( getMaxFloat, 0 ),
    'max_long'                      : RPNOperator( lambda: ( 1 << 31 ) - 1, 0 ),
    'max_longlong'                  : RPNOperator( lambda: ( 1 << 63 ) - 1, 0 ),
    'max_quadlong'                  : RPNOperator( lambda: ( 1 << 127 ) - 1, 0 ),
    'max_short'                     : RPNOperator( lambda: ( 1 << 15 ) - 1, 0 ),
    'max_uchar'                     : RPNOperator( lambda: ( 1 << 8 ) - 1, 0 ),
    'max_ulong'                     : RPNOperator( lambda: ( 1 << 32 ) - 1, 0 ),
    'max_ulonglong'                 : RPNOperator( lambda: ( 1 << 64 ) - 1, 0 ),
    'max_uquadlong'                 : RPNOperator( lambda: ( 1 << 128 ) - 1, 0 ),
    'max_ushort'                    : RPNOperator( lambda: ( 1 << 16 ) - 1, 0 ),
    'min_char'                      : RPNOperator( lambda: -( 1 << 7 ), 0 ),
    'min_double'                    : RPNOperator( getMinDouble, 0 ),
    'min_float'                     : RPNOperator( getMinFloat, 0 ),
    'min_long'                      : RPNOperator( lambda: -( 1 << 31 ), 0 ),
    'min_longlong'                  : RPNOperator( lambda: -( 1 << 63 ), 0 ),
    'min_quadlong'                  : RPNOperator( lambda: -( 1 << 127 ), 0 ),
    'min_short'                     : RPNOperator( lambda: -( 1 << 15 ), 0 ),
    'min_uchar'                     : RPNOperator( lambda: 0, 0 ),
    'min_ulong'                     : RPNOperator( lambda: 0, 0 ),
    'min_ulonglong'                 : RPNOperator( lambda: 0, 0 ),
    'min_uquadlong'                 : RPNOperator( lambda: 0, 0 ),
    'min_ushort'                    : RPNOperator( lambda: 0, 0 ),

    # Planck constants
    'planck_constant'               : RPNOperator( getPlanckConstant, 0 ),
    'reduced_planck_constant'       : RPNOperator( getReducedPlanckConstant, 0 ),

    'planck_length'                 : RPNOperator( getPlanckLength, 0 ),
    'planck_mass'                   : RPNOperator( getPlanckMass, 0 ),
    'planck_time'                   : RPNOperator( getPlanckTime, 0 ),
    'planck_charge'                 : RPNOperator( getPlanckCharge, 0 ),
    'planck_temperature'            : RPNOperator( getPlanckTemperature, 0 ),

    'planck_angular_frequency'      : RPNOperator( lambda: RPNMeasurement( '1.85487e43', 'second^-1' ), 0 ),
    'planck_area'                   : RPNOperator( lambda: RPNMeasurement( '2.61219618e-70', 'meter^2' ), 0 ),
    'planck_current'                : RPNOperator( lambda: RPNMeasurement( '3.4789e25', 'ampere' ), 0 ),
    'planck_density'                : RPNOperator( lambda: RPNMeasurement( '5.15518197484e+96', 'kilogram/meter^3' ), 0 ),
    'planck_energy'                 : RPNOperator( lambda: RPNMeasurement( '1.220910e28', 'electron-volt' ), 0 ),
    'planck_energy_density'         : RPNOperator( lambda: RPNMeasurement( '4.63298e113', 'joule/meter^3' ), 0 ),
    'planck_force'                  : RPNOperator( lambda: RPNMeasurement( '1.2102947186e44', 'joule/meter' ), 0 ),
    'planck_impedance'              : RPNOperator( lambda: RPNMeasurement( '29.9792458', 'ohm' ), 0 ),
    'planck_intensity'              : RPNOperator( lambda: RPNMeasurement( '1.38893e122', 'watt/meter^2' ), 0 ),
    'planck_momentum'               : RPNOperator( lambda: RPNMeasurement( '6.52485', 'kilogram*meter/second' ), 0 ),
    'planck_power'                  : RPNOperator( lambda: RPNMeasurement( '3.62831e52', 'watt' ), 0 ),
    'planck_pressure'               : RPNOperator( lambda: RPNMeasurement( '4.63309e113', 'pascal' ), 0 ),
    'planck_voltage'                : RPNOperator( lambda: RPNMeasurement( '1.04295e27', 'volt' ), 0 ),
    'planck_volume'                 : RPNOperator( lambda: RPNMeasurement( '4.22190722e-105', 'meter^3' ), 0 ),

    # https://en.wikipedia.org/wiki/Natural_units
    # Stoney Units
    # Hartee Atomic Units
    # QCD Units
    # Natural Units

    # subatomic particle constants
    'alpha_particle_mass'           : RPNOperator( lambda: RPNMeasurement( '6.644657230e-27', 'kilogram' ), 0 ),
    'deuteron_mass'                 : RPNOperator( lambda: RPNMeasurement( '3.343583719e-27', 'kilogram' ), 0 ),
    'electron_mass'                 : RPNOperator( lambda: RPNMeasurement( '9.10938356e-31', 'kilogram' ), 0 ),
    'helion_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.006412700e-27', 'kilogram' ), 0 ),
    'muon_mass'                     : RPNOperator( lambda: RPNMeasurement( '1.883531594e-28', 'kilogram' ), 0 ),
    'neutron_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.674927471e-27', 'kilogram' ), 0 ),
    'proton_mass'                   : RPNOperator( lambda: RPNMeasurement( '1.672621898e-27', 'kilogram' ), 0 ),
    'tau_mass'                      : RPNOperator( lambda: RPNMeasurement( '3.16747e-27', 'kilogram' ), 0 ),
    'triton_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.007356665e-27', 'kilogram' ), 0 ),

    # heavenly body constants
    # sun_day
    'sun_luminosity'                : RPNOperator( lambda: RPNMeasurement( '3.826e26', 'watt' ), 0 ),
    'sun_mass'                      : RPNOperator( lambda: RPNMeasurement( '1.988500e30', 'kilogram' ), 0 ),
    'sun_radius'                    : RPNOperator( lambda: RPNMeasurement( '6.9599e8', 'meter' ), 0 ),
    'sun_volume'                    : RPNOperator( lambda: RPNMeasurement( '1.412e27', 'meter^3' ), 0 ),

    'mercury_mass'                  : RPNOperator( lambda: RPNMeasurement( '3.301e26', 'kilogram' ), 0 ),
    # equitorial radius
    'mercury_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4397e6', 'meter' ), 0 ),
    # sidereal orbit period
    'mercury_revolution'            : RPNOperator( lambda: RPNMeasurement( '87.969', 'day' ), 0 ),
    'mercury_volume'                : RPNOperator( lambda: RPNMeasurement( '6.083e19', 'meter^3' ), 0 ),

    'venus_mass'                    : RPNOperator( lambda: RPNMeasurement( '4.8689952e24', 'kilogram' ), 0 ),
    'venus_radius'                  : RPNOperator( lambda: RPNMeasurement( '6.0518e6', 'meter' ), 0 ),
    'venus_revolution'              : RPNOperator( lambda: RPNMeasurement( '224.701', 'day' ), 0 ),
    'venus_volume'                  : RPNOperator( lambda: RPNMeasurement( '9.2843e20', 'meter^3' ), 0 ),

    'earth_density'                 : RPNOperator( lambda: RPNMeasurement( '5.514', 'gram/centimeter^3' ), 0 ),  # https://en.wikipedia.org/wiki/Earth#Composition_and_structure
    'earth_gravity'                 : RPNOperator( lambda: RPNMeasurement( '9.806650', 'meter/second^2' ), 0 ),
    'earth_mass'                    : RPNOperator( lambda: RPNMeasurement( '5.9640955e24', 'kilogram' ), 0 ),   # based on earth_radius and earth_gravity
    'earth_radius'                  : RPNOperator( lambda: RPNMeasurement( '6371000.8', 'meter' ), 0 ),         # https://en.wikipedia.org/wiki/Earth_radius#Global_average_radii - volumetric radius
    'earth_volume'                  : RPNOperator( lambda: RPNMeasurement( '1.083207324897e21', 'meter^3' ), 0 ),  # based on earth_radius
    'sidereal_year'                 : RPNOperator( lambda: RPNMeasurement( '365.256360417', 'day' ), 0 ),
    'tropical_year'                 : RPNOperator( lambda: RPNMeasurement( '365.24219', 'day' ), 0 ),

    'moon_gravity'                  : RPNOperator( lambda: RPNMeasurement( '1.62', 'meter/second^2' ), 0 ),
    'moon_mass'                     : RPNOperator( lambda: RPNMeasurement( '7.342e22', 'kilogram' ), 0 ),
    'moon_radius'                   : RPNOperator( lambda: RPNMeasurement( '1.7381e6', 'meter' ), 0 ),
    'moon_revolution'               : RPNOperator( lambda: RPNMeasurement( '27.3217', 'day' ), 0 ),
    'moon_volume'                   : RPNOperator( lambda: RPNMeasurement( '2.1958e19', 'meter^3' ), 0 ),

    'mars_mass'                     : RPNOperator( lambda: RPNMeasurement( '6.4191269e23', 'kilogram' ), 0 ),
    'mars_radius'                   : RPNOperator( lambda: RPNMeasurement( '3.3962e6', 'meter' ), 0 ),
    'mars_revolution'               : RPNOperator( lambda: RPNMeasurement( '686.980', 'day' ), 0 ),
    'mars_volume'                   : RPNOperator( lambda: RPNMeasurement( '1.6318e20', 'meter^3' ), 0 ),

    'jupiter_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.8983e27', 'kilogram' ), 0 ),
    'jupiter_radius'                : RPNOperator( lambda: RPNMeasurement( '7.1492e7', 'meter' ), 0 ),
    'jupiter_revolution'            : RPNOperator( lambda: RPNMeasurement( '11.862', 'year' ), 0 ),
    'jupiter_volume'                : RPNOperator( lambda: RPNMeasurement( '1.43128e24', 'meter^3' ), 0 ),

    'saturn_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.6836e26', 'kilogram' ), 0 ),
    'saturn_radius'                 : RPNOperator( lambda: RPNMeasurement( '6.0268e7', 'meter' ), 0 ),
    'saturn_revolution'             : RPNOperator( lambda: RPNMeasurement( '29.457', 'year' ), 0 ),
    'saturn_volume'                 : RPNOperator( lambda: RPNMeasurement( '8.2713e23', 'meter^3' ), 0 ),

    'uranus_mass'                   : RPNOperator( lambda: RPNMeasurement( '8.6816e25', 'kilogram' ), 0 ),
    'uranus_radius'                 : RPNOperator( lambda: RPNMeasurement( '2.5559e7', 'meter' ), 0 ),
    'uranus_revolution'             : RPNOperator( lambda: RPNMeasurement( '84.011', 'year' ), 0 ),
    'uranus_volume'                 : RPNOperator( lambda: RPNMeasurement( '6.833e22', 'meter^3' ), 0 ),

    'neptune_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.0242e26', 'kilogram' ), 0 ),
    'neptune_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4764e7', 'meter' ), 0 ),
    'neptune_revolution'            : RPNOperator( lambda: RPNMeasurement( '164.79', 'year' ), 0 ),
    'neptune_volume'                : RPNOperator( lambda: RPNMeasurement( '6.254e22', 'meter^3' ), 0 ),

    'pluto_mass'                    : RPNOperator( lambda: RPNMeasurement( '1.0303e22', 'kilogram' ), 0 ),
    'pluto_radius'                  : RPNOperator( lambda: RPNMeasurement( '1.185e6', 'meter' ), 0 ),
    'pluto_revolution'              : RPNOperator( lambda: RPNMeasurement( '247.94', 'year' ), 0 ),
    'pluto_volume'                  : RPNOperator( lambda: RPNMeasurement( '6.97e18', 'meter^3' ), 0 ),

    # Astronomical object operators

    #    # Planetary moon operators
    #    'phobos'                        : RPNOperator( ephem.Phobos, 0 ),
    #    'deimos'                        : RPNOperator( ephem.Deimos, 0 ),
    #    'io'                            : RPNOperator( ephem.Io, 0 ),
    #    'europa'                        : RPNOperator( ephem.Europa, 0 ),
    #    'ganymede'                      : RPNOperator( ephem.Ganymede, 0 ),
    #    'callisto'                      : RPNOperator( ephem.Callisto, 0 ),
    #    'mimas'                         : RPNOperator( ephem.Mimas, 0 ),
    #    'enceladus'                     : RPNOperator( ephem.Enceladus, 0 ),
    #    'tethys'                        : RPNOperator( ephem.Tethys, 0 ),
    #    'dione'                         : RPNOperator( ephem.Dione, 0 ),
    #    'rhea'                          : RPNOperator( ephem.Rhea, 0 ),
    #    'titan'                         : RPNOperator( ephem.Titan, 0 ),
    #    'hyperion'                      : RPNOperator( ephem.Hyperion, 0 ),
    #    'iapetus'                       : RPNOperator( ephem.Iapetus, 0 ),
    #    'ariel'                         : RPNOperator( ephem.Ariel, 0 ),
    #    'umbriel'                       : RPNOperator( ephem.Umbriel, 0 ),
    #    'titania'                       : RPNOperator( ephem.Titania, 0 ),
    #    'oberon'                        : RPNOperator( ephem.Oberon, 0 ),
    #    'miranda'                       : RPNOperator( ephem.Miranda, 0 ),
}

#  Earth's approximate water volume (the total water supply of the world) is
#  1,338,000,000 km3 (321,000,000 mi3).[2]


# //******************************************************************************
# //
# //  class RPNFunction
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  RPNFunction object.  However, it can't know how many of them it
# //  actually needs until it's time to evaluate the function, so we need to
# //  save all the terms we have so far, since we can't know until later how
# //  many of them we will need.
# //
# //  Once we are able to parse out how many arguments belong to the function
# //  declaration, then we can determine what arguments are left over to be used
# //  with the function operation.   All function operations take at least one
# //  argument before the function declaration.
# //
# //******************************************************************************

class RPNFunction( object ):
    """This class represents a user-defined function in rpn."""
    def __init__( self, valueList, startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        else:
            self.valueList.append( valueList )

        self.startingIndex = startingIndex
        self.code = ''
        self.code_locals = { }
        self.compiled = None
        self.function = None
        self.argCount = 0

    def add( self, arg ):
        self.valueList.append( arg )

    def evaluate( self, x, y = 0, z = 0 ):
        if not self.function:
            self.compile( )

        if self.argCount == 1:
            return self.function( x )
        elif self.argCount == 2:
            return self.function( x, y )
        elif self.argCount == 3:
            return self.function( x, y, z )

    def getFunction( self ):
        if not self.function:
            self.compile( )

        return self.function

    def compile( self ):
        valueList = [ ]

        xArg = False
        yArg = False
        zArg = False

        for index, item in enumerate( self.valueList ):
            if index < self.startingIndex:
                continue

            if item == 'x':
                xArg = True
            elif item == 'y':
                yArg = True
            elif item == 'z':
                zArg = True

            valueList.append( item )

        self.code = 'def rpnInternalFunction('

        first = True

        self.argCount = 0

        if xArg:
            self.code += ' x'
            first = False
            self.argCount += 1

        if yArg:
            if first:
                first = False
            else:
                self.code += ','

            self.code += ' y'
            self.argCount += 1

        if zArg:
            if not first:
                self.code += ','

            self.code += ' z'
            self.argCount += 1

        self.code += ' ): return '

        args = [ ]

        debugPrint( 'terms', valueList )

        while valueList:
            term = valueList.pop( 0 )
            debugPrint( 'term:', term, 'args:', args )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            if term in operators:
                function = operators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( operators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = operators[ term ].argCount

                if len( args ) < operands:
                    raise ValueError( '{1} expects {2} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                args.append( function )

                if not valueList:
                    self.code += function
            else:
                args.append( term )

        debugPrint( 'valueList:', self.valueList[ self.startingIndex : ] )
        debugPrint( 'code:', self.code )

        self.compiled = compile( self.code, '<string>', 'exec' )

        exec( self.compiled, globals( ), self.code_locals )
        self.function = self.code_locals[ 'rpnInternalFunction' ]


# //******************************************************************************
# //
# //  createFunction
# //
# //  This only gets called if we are not already creating a function.
# //
# //******************************************************************************

def createFunction( valueList ):
    g.creatingFunction = True
    valueList.append( RPNFunction( valueList, len( valueList ) ) )


# //******************************************************************************
# //
# //  addX
# //
# //******************************************************************************

def addX( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'x\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'x' )


# //******************************************************************************
# //
# //  addY
# //
# //******************************************************************************

def addY( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'y\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'y' )


# //******************************************************************************
# //
# //  addZ
# //
# //******************************************************************************

def addZ( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'z\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'z' )


# //******************************************************************************
# //
# //  plotFunction
# //
# //******************************************************************************

def plotFunction( start, end, func ):
    plot( lambda x: func.evaluate( x, func ), [ start, end ] )
    return 0


# //******************************************************************************
# //
# //  plot2DFunction
# //
# //******************************************************************************

def plot2DFunction( start1, end1, start2, end2, func ):
    splot( lambda x, y: func.evaluate( x, y ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


# //******************************************************************************
# //
# //  plotComplexFunction
# //
# //******************************************************************************

def plotComplexFunction( start1, end1, start2, end2, func ):
    cplot( lambda x: func.evaluate( x ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ],
           points = 10000 )
    return 0


# //******************************************************************************
# //
# //  filterList
# //
# //******************************************************************************

def filterList( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )
        else:
            raise ValueError( '\'filter\' expects a function argument' )

    result = [ ]

    if isinstance( n, RPNGenerator ):
        return RPNGenerator.createFilter( n.generator, k.getFunction( ) )

    for i in n:
        value = k.evaluate( i )

        if ( value != 0 ) != invert:
            result.append( i )

    return result


# //******************************************************************************
# //
# //  filterListByIndex
# //
# //******************************************************************************

def filterListByIndex( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter_by_index\' expects a function argument' )
        else:
            raise ValueError( '\'filter_by_index\' expects a function argument' )

    result = [ ]

    for index, item in enumerate( n ):
        value = k.evaluate( index )

        if ( value != 0 ) != invert:
            result.append( item )

    return result


# //******************************************************************************
# //
# //  preprocessTerms
# //
# //******************************************************************************

def preprocessTerms( terms ):
    """
    Given the initial list of arguments form the user, there are several
    things we want to do to the list before handing it off to the actual
    operator evaluator.  This logic used to be part of the evaluator, but
    that made the code a lot more complicated.  Hopefully, this will make
    the code simpler and easier to read.

    If this function returns an empty list, then rpn should abort.  This
    function should print out any error messages.
    """
    result = [ ]

    # do some basic validation of the arguments we were given...
    if not validateArguments( terms ):
        return result

    for term in terms:
        # translate the aliases into their real names
        if term in g.operatorAliases:
            result.append( g.operatorAliases[ term ] )
        # operators and unit operator names can be stuck right back in the list
        elif term in ( operators, g.unitOperatorNames ):
            result.append( term )
        # translate compound units in the equivalent operators
        elif ( '*' in term or '^' in term or '/' in term ) and \
            any( c in term for c in string.ascii_letters ):

            # handle a unit operator
            if not g.unitOperators:
                loadUnitData( )

            newTerms = unpackUnitExpression( term )

            for newTerm in newTerms:
                result.append( newTerm )
        else:
            result.append( term )

    return result


# //******************************************************************************
# //
# //  evaluateConstantOperator
# //
# //  We know there are no arguments.  Although none of the constants currently
# //  return a list, maybe one will in the future, so I'll handle list results.
# //
# //******************************************************************************

def evaluateConstantOperator( term, index, currentValueList ):
    # handle a constant operator
    operatorInfo = constants[ term ]
    result = callers[ 0 ]( operatorInfo.function, None )

    newResult = list( )

    if not isinstance( result, list ):
        result = [ result ]

    for item in result:
        if isinstance( item, RPNMeasurement ) and item.getUnits( ) == { }:
            newResult.append( item.getValue( ) )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    currentValueList.append( newResult )

    return True


# //******************************************************************************
# //
# //  checkForVariable
# //
# //******************************************************************************

def checkForVariable( term ):
    if not isinstance( term, str ):
        return term

    # first check for a variable name or history expression
    if not term or term[ 0 ] != '$':
        return term

    return RPNVariable( term[ 1 : ] )


# //******************************************************************************
# //
# //  handleOneArgListOperator
# //
# //  Each operator is going to have to be responsible for how it handles
# //  recursive lists.  In some cases, handling recursive lists makes sense.
# //
# //******************************************************************************

def handleOneArgListOperator( func, args, currentValueList ):
    recursive = False

    if isinstance( args, RPNGenerator ):
        args = list( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if not isinstance( args, list ):
        currentValueList.append( func( [ args ] ) )
    else:
        currentValueList.append( func( args ) )


# //******************************************************************************
# //
# //  handleOneArgGeneratorOperator
# //
# //******************************************************************************

def handleOneArgGeneratorOperator( func, args, currentValueList ):
    recursive = False

    if isinstance( args, list ):
        args = RPNGenerator.create( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if isinstance( args, RPNGenerator ):
        currentValueList.append( func( args ) )
    else:
        raise ValueError( 'then you shouldn\'t call handleOneArgGeneratorOperator, should you?' )


# //******************************************************************************
# //
# //  handleMultiArgListOperator
# //
# //  Each operator is going to have to be responsible for how it handles
# //  recursive lists.  In some cases, handling recursive lists makes sense.
# //
# //******************************************************************************

def handleMultiArgListOperator( func, argList, currentValueList ):
    newArgList = [ ]

    for arg in argList:
        if isinstance( arg, RPNGenerator ):
            newArgList.append( list( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


# //******************************************************************************
# //
# //  handleMultiArgGeneratorOperator
# //
# //******************************************************************************

def handleMultiArgGeneratorOperator( func, args, currentValueList ):
    newArgList = [ ]

    for arg in args:
        if isinstance( arg, list ):
            newArgList.append( RPNGenerator.create( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


# //******************************************************************************
# //
# //  evaluateListOperator
# //
# //******************************************************************************

def evaluateListOperator( term, index, currentValueList ):
    # handle a list operator
    operatorInfo = listOperators[ term ]
    argsNeeded = operatorInfo.argCount
    argTypes = operatorInfo.argTypes

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    # handle the call depending on the number of arguments needed
    if argsNeeded == 0:
        currentValueList.append( operatorInfo.function( currentValueList ) )
    elif argsNeeded == 1:
        args = currentValueList.pop( )

        if argTypes[ 0 ] == RPNOperator.Generator:
            handleOneArgGeneratorOperator( operatorInfo.function, args, currentValueList )
        else:
            handleOneArgListOperator( operatorInfo.function, args, currentValueList )
    else:
        argList = [ ]

        for i in range( 0, argsNeeded ):
            argList.insert( 0, currentValueList.pop( ) )

        if argTypes[ 0 ] == RPNOperator.Generator:
            handleMultiArgGeneratorOperator( operatorInfo.function, argList, currentValueList )
        else:
            handleMultiArgListOperator( operatorInfo.function, argList, currentValueList )

    return True


# //******************************************************************************
# //
# //  dumpOperators
# //
# //******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        # print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )
        print( '   ' + i )

    print( )
    print( 'constants:' )

    for i in sorted( [ key for key in constants ] ):
        print( '   ' + i )

    print( )
    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )
    print( 'modifer operators:' )

    for i in sorted( [ key for key in modifiers ] ):
        print( '   ' + i )

    print( )
    print( 'internal operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


# //******************************************************************************
# //
# //  evaluateOneArgFunction
# //
# //******************************************************************************

def evaluateOneArgFunction( func, args, level = 0 ):
    if isinstance( args, list ):
        result = [ evaluateOneArgFunction( func, i, level + 1 ) for i in args ]
    elif isinstance( args, RPNGenerator ):
        result = RPNGenerator.createChained( args.getGenerator( ), func )
    else:
        result = func( args )

    # if this is the 'echo' operator, just return the result
    if func.__name__ == 'addEchoArgument':
        return result

    # otherwise, check for arguments to be echoed, and echo them before the result
    if level == 0 and not g.operatorList and len( g.echoArguments ) > 0:
        returnValue = list( g.echoArguments )
        returnValue.append( result )
        g.echoArguments = [ ]
        return returnValue
    else:
        return result


# //******************************************************************************
# //
# //  evaluateTwoArgFunction
# //
# //  This seems somewhat non-pythonic...
# //
# //******************************************************************************

def evaluateTwoArgFunction( func, _arg1, _arg2, level = 0 ):
    if isinstance( _arg1, list ):
        len1 = len( _arg1 )

        if len1 == 1:
            arg1 = _arg1[ 0 ]
            list1 = False
        else:
            arg1 = _arg1
            list1 = True

        generator1 = False
    else:
        arg1 = _arg1
        list1 = False

    generator1 = isinstance( arg1, RPNGenerator )

    if isinstance( _arg2, list ):
        len2 = len( _arg2 )

        if len2 == 1:
            arg2 = _arg2[ 0 ]
            list2 = False
        else:
            arg2 = _arg2
            list2 = True

        generator2 = False
    else:
        arg2 = _arg2
        list2 = False

    generator2 = isinstance( arg2, RPNGenerator )

    if generator1:
        if generator2:
            iter1 = iter( arg1 )
            iter2 = iter( arg2 )

            result = [ ]

            while True:
                try:
                    i1 = iter1.__next__( )
                    i2 = iter2.__next__( )

                    result.append( func( i1, i2 ) )
                except:
                    break
        else:
            result = [ evaluateTwoArgFunction( func, i, arg2, level + 1 ) for i in arg1.getGenerator( ) ]
    elif generator2:
        result = [ evaluateTwoArgFunction( func, arg1, i, level + 1 ) for i in arg2.getGenerator( ) ]
    elif list1:
        if list2:
            result = [ evaluateTwoArgFunction( func, arg1[ index ], arg2[ index ], level + 1 ) for index in range( 0, min( len1, len2 ) ) ]
        else:
            result = [ evaluateTwoArgFunction( func, i, arg2, level + 1 ) for i in arg1 ]

    else:
        if list2:
            result = [ evaluateTwoArgFunction( func, arg1, j, level + 1 ) for j in arg2 ]
        else:
            result = func( arg2, arg1 )

    # check for arguments to be echoed, and echo them before the result
    if level == 0 and not g.operatorList and len( g.echoArguments ) > 0:
        returnValue = list( g.echoArguments )
        returnValue.append( result )
        g.echoArguments = [ ]
        return returnValue
    else:
        return result


# //******************************************************************************
# //
# //  caller
# //
# //******************************************************************************

def caller( func, args ):
    if not args:
        return func( )

    for arg in args:
        if isinstance( arg, list ):
            for i in arg:
                return [ map( func, *args ) ]


# //******************************************************************************
# //
# //  callers
# //
# //******************************************************************************

callers = [
    lambda func, args: [ func( ) ],
    evaluateOneArgFunction,
    evaluateTwoArgFunction,

    # 3, 4, and 5 argument functions don't recurse with lists more than one level
    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for c in arg1 for b in arg2 for a in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for d in arg1 for c in arg2 for b in arg3 for a in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for e in arg1 for d in arg2 for c in arg3 for b in arg4 for a in arg5 ],
]


# //******************************************************************************
# //
# //  dumpStats
# //
# //******************************************************************************

def dumpStats( ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) +
                                             len( modifiers ) ) )
    print( '{:10,} constants'.format( len( constants ) ) )
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( g.dataPath ), 'small primes' )
    printStats( loadLargePrimes( g.dataPath ), 'large primes' )
    printStats( loadHugePrimes( g.dataPath ), 'huge primes' )
    printStats( loadIsolatedPrimes( g.dataPath ), 'isolated primes' )
    printStats( loadTwinPrimes( g.dataPath ), 'twin primes' )
    printStats( loadBalancedPrimes( g.dataPath ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( g.dataPath ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( g.dataPath ), 'triple balanced primes' )
    printStats( loadSophiePrimes( g.dataPath ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( g.dataPath ), 'cousin primes' )
    printStats( loadSexyPrimes( g.dataPath ), 'sexy primes' )
    printStats( loadTripletPrimes( g.dataPath ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( g.dataPath ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( g.dataPath ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( g.dataPath ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( g.dataPath ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( g.dataPath ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


# //******************************************************************************
# //
# //  unpackUnitExpression
# //
# //******************************************************************************

def unpackUnitExpression( expression, addNullUnit = True ):
    pieces = expression.split( '/' )

    if len( pieces ) > 2:
        raise ValueError( 'only one \'/\' is permitted' )
    elif len( pieces ) == 2:
        result = unpackUnitExpression( pieces[ 0 ] )
        result.extend( unpackUnitExpression( pieces[ 1 ], False ) )
        result.append( 'divide' )

        return result
    else:
        result = [ ]

        units = expression.split( '*' )

        bFirst = True

        for unit in units:
            if unit == '':
                raise ValueError( 'wasn\'t expecting another \'*\' in \'' + expression + '\'' )

            operands = unit.split( '^' )

            plainUnit = operands[ 0 ]

            if plainUnit not in g.unitOperators and plainUnit in g.operatorAliases:
                plainUnit = g.operatorAliases[ plainUnit ]

            operandCount = len( operands )

            exponent = 1

            if operandCount > 1:
                for i in range( 1, operandCount ):
                    exponent *= int( floor( operands[ i ] ) )

            if exponent != 0:
                result.append( plainUnit )

                if exponent != 1:
                    result.append( str( exponent ) )
                    result.append( 'power' )

            if bFirst:
                bFirst = False
            else:
                result.append( 'multiply' )

        # kludge
        if len( result ) > 1 and addNullUnit:
            result.insert( 0, '_null_unit' )
            result.append( 'multiply' )

        return result


# //******************************************************************************
# //
# //  evaluateTerm
# //
# //  This looks worse than it is.  It just has to do slightly different things
# //  depending on what kind of term or operator is involved.  Plus, there's a
# //  lot of exception handling.
# //
# //  This function assumes operator alias replacements have already occurred.
# //
# //******************************************************************************

def evaluateTerm( term, index, currentValueList, lastArg = True ):
    isList = isinstance( term, list )
    isGenerator = isinstance( term, RPNGenerator )

    try:
        # handle a modifier operator
        if not isList and not isGenerator and term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )
        elif not isList and term in g.unitOperatorNames or \
             ( '*' in term or '^' in term or '/' in term ) and \
             any( c in term for c in string.ascii_letters ):

            # handle a unit operator
            if not g.unitOperators:
                loadUnitData( )

            if term not in g.unitOperatorNames:
                newTerms = unpackUnitExpression( term )

                if len( newTerms ) == 1 and newTerms[ 0 ] == term:
                    term = RPNUnits( term )
                else:
                    for newTerm in newTerms:
                        evaluateTerm( newTerm, index, currentValueList, lastArg )

                    return True

            # look for unit without a value (in which case we give it a value of 1)
            if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], RPNMeasurement ) or \
                isinstance( currentValueList[ -1 ], RPNDateTime ) or ( isinstance( currentValueList[ -1 ], list ) and
                                                                       isinstance( currentValueList[ -1 ][ 0 ], RPNMeasurement ) ):
                    currentValueList.append( applyNumberValueToUnit( 1, term ) )
            # if the unit comes after a generator, convert it to a list and apply the unit to each
            elif isinstance( currentValueList[ -1 ], RPNGenerator ):
                newArg = [ ]

                for value in list( currentValueList.pop( ) ):
                    newArg.append( applyNumberValueToUnit( value, term ) )

                currentValueList.append( newArg )
            # if the unit comes after a list, then apply it to every item in the list
            elif isinstance( currentValueList[ -1 ], list ):
                argList = currentValueList.pop( )

                newArg = [ ]

                for listItem in argList:
                    newArg.append( applyNumberValueToUnit( listItem, term ) )

                currentValueList.append( newArg )
            # and if it's a plain old number, then apply it to the unit
            elif isinstance( currentValueList[ -1 ], ( mpf, int ) ):
                currentValueList.append( applyNumberValueToUnit( currentValueList.pop( ), term ) )
            else:
                raise ValueError( 'unsupported type for a unit operator' )
        elif term in constants:
            if not g.unitOperators:
                loadUnitData( )

            if not evaluateConstantOperator( term, index, currentValueList ):
                return False
        elif term in operators:
            if g.duplicateOperations > 0:
                operatorInfo = operators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not operators[ term ].evaluate( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not operators[ term ].evaluate( term, index, currentValueList ):
                    return False
        elif term in listOperators:
            if g.duplicateOperations > 0:
                operatorInfo = operators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not evaluateListOperator( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not evaluateListOperator( term, index, currentValueList ):
                    return False
        else:
            # handle a plain old value (i.e., a number or list, not an operator)
            try:
                currentValueList.append( parseInputValue( term, g.inputRadix ) )

            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    return False

            except ( AttributeError, TypeError ):
                if not lastArg:
                    currentValueList.append( term )
                    return True

                # build keyword list if needed
                if len( g.keywords ) == 0:
                    g.keywords = list( operators.keys( ) )
                    g.keywords.extend( list( listOperators.keys( ) ) )
                    g.keywords.extend( constants )
                    g.keywords.extend( g.unitOperatorNames )
                    g.keywords.extend( g.operatorAliases )

                guess = difflib.get_close_matches( term, g.keywords, 1 )

                if ( len( guess ) == 1 ):
                    guess = guess[ 0 ]

                    if guess in g.operatorAliases:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  Did you mean \'{1}\', i.e., an alias for \'{2}\'?'.format( term, guess, g.operatorAliases[ guess ] ) )
                    else:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  Did you mean \'{1}\'?'.format( term, guess ) )
                else:
                    print( 'rpn:  Unrecognized operator \'{0}\'.'.format( term ) )

                return False

    except ( ValueError, AttributeError, TypeError ) as error:
        print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

        if g.debugMode:
            raise
        else:
            return False

    except ZeroDivisionError as error:
        print( 'rpn:  division by zero' )

        if g.debugMode:
            raise
        else:
            return False

    except IndexError as error:
        print( 'rpn:  index error for list operator at arg ' + format( index ) +
               '.  Are your arguments in the right order?' )

        if g.debugMode:
            raise
        else:
            return False

    return True


# //******************************************************************************
# //
# //  printHelpMessage
# //
# //******************************************************************************

def printHelpMessage( ):
    from rpnOutput import printHelp
    printHelp( operators, constants, listOperators, modifiers, '', True )
    return 0


# //******************************************************************************
# //
# //  printHelpTopic
# //
# //******************************************************************************

def printHelpTopic( n ):
    from rpnOutput import printHelp

    if isinstance( n, str ):
        printHelp( operators, listOperators, modifiers, n, True )
    elif isinstance( n, RPNMeasurement ):
        units = n.getUnits( )
        # help for units isn't implemented yet, but now it will work
        printHelp( operators, constants, listOperators, modifiers, list( units.keys( ) )[ 0 ], True )
    else:
        print( 'The \'topic\' operator requires a string argument.' )

    return 0


# //******************************************************************************
# //
# //  functionOperators
# //
# //  This is a list of operators that terminate the function creation state.
# //
# //******************************************************************************

functionOperators = [
    'eval',
    'eval2',
    'eval3',
    'filter',
    'filter_by_index',
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plotc',
    'unfilter',
    'unfilter_by_index',
]


# //******************************************************************************
# //
# //  sideEffectOperators
# //
# //  This is a list of operators that execute without modifying the result
# //  stack.
# //
# //******************************************************************************

sideEffectOperators = [
    'comma_mode',
    'hex_mode',
    'identify_mode',
    'leading_zero_mode',
    'octal_mode',
    'timer_mode',
]


# //******************************************************************************
# //
# //  Modifiers are operators that directly modify the argument stack or global
# //  state in addition to or instead of just returning a value.
# //
# //  Modifiers also don't adhere to the 'language' of rpn, which is strictly
# //  postfix and context-free.  Unlike other operators consume one or more
# //  values and return either a single list (possibly with sublists) or a single
# //  value.  Also by changing global state, they can modify what comes _after_
# //  them, which is not how the rpn language is defined.  However, this gives me
# //  the flexibility to do some useful things that I am not otherwise able to
# //  do.
# //
# //******************************************************************************

modifiers = {
    'dup_term'          : RPNOperator( duplicateTerm, 1 ),

    'dup_operator'      : RPNOperator( duplicateOperation, 1 ),

    'previous'          : RPNOperator( getPrevious, 0 ),

    'unlist'            : RPNOperator( unlist, 0 ),

    #'for_each'          : RPNOperator( forEach, 0 ),

    'lambda'            : RPNOperator( createFunction, 0 ),

    'x'                 : RPNOperator( addX, 0 ),

    'y'                 : RPNOperator( addY, 0 ),

    'z'                 : RPNOperator( addZ, 0 ),

    '['                 : RPNOperator( incrementNestedListLevel, 0 ),

    ']'                 : RPNOperator( decrementNestedListLevel, 0 ),

    '{'                 : RPNOperator( startOperatorList, 0 ),

    '}'                 : RPNOperator( endOperatorList, 0 ),
}


# //******************************************************************************
# //
# //  listOperators are operators that handle whether or not an argument is a
# //  list themselves (because they require a list argument).  Unlike regular
# //  operators, we don't want listOperators permutated over each list element,
# //  and if we do for auxillary arguments, these operator handlers will do that
# //  themselves.
# //
# //******************************************************************************

listOperators = {
    # algebra
    'add_polynomials'       : RPNOperator( addPolynomials,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'eval_polynomial'       : RPNOperator( evaluatePolynomial,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'multiply_polynomials'  : RPNOperator( multiplyPolynomials,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'polynomial_power'      : RPNOperator( exponentiatePolynomial,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'polynomial_product'    : RPNOperator( multiplyListOfPolynomials,
                                           1, [ RPNOperator.List ] ),

    'polynomial_sum'        : RPNOperator( addListOfPolynomials,
                                           1, [ RPNOperator.List ] ),

    'solve'                 : RPNOperator( solvePolynomial,
                                           1, [ RPNOperator.List ] ),

    # arithmetic
    'gcd'                   : RPNOperator( getGCD,
                                           1, [ RPNOperator.List ] ),

    'lcm'                   : RPNOperator( getLCM,
                                           1, [ RPNOperator.List ] ),

    'max'                   : RPNOperator( getMaximum,
                                           1, [ RPNOperator.List ] ),

    'mean'                  : RPNOperator( calculateArithmeticMean,
                                           1, [ RPNOperator.List ] ),

    'geometric_mean'        : RPNOperator( calculateGeometricMean,
                                           1, [ RPNOperator.List ] ),

    'min'                   : RPNOperator( getMinimum,
                                           1, [ RPNOperator.List ] ),

    'product'               : RPNOperator( getProduct,
                                           1, [ RPNOperator.List ] ),

    'stddev'                : RPNOperator( getStandardDeviation,
                                           1, [ RPNOperator.List ] ),

    'sum'                   : RPNOperator( getSum,
                                           1, [ RPNOperator.List ] ),

    # combinatoric
    'multinomial'           : RPNOperator( getMultinomial,
                                           1, [ RPNOperator.List ] ),

    # conversion
    'convert'               : RPNOperator( convertUnits,
                                           2, [ RPNOperator.List ] ),   # list arguments are special

    'latlong_to_nac'        : RPNOperator( convertLatLongToNAC,
                                           1, [ RPNOperator.List ] ),

    'unpack'                : RPNOperator( unpackInteger,
                                           2, [ RPNOperator.Integer, RPNOperator.List ] ),

    'pack'                  : RPNOperator( packInteger,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    # date_time
    'make_datetime'         : RPNOperator( makeDateTime,
                                           1, [ RPNOperator.List ] ),

    'make_iso_time'         : RPNOperator( makeISOTime,
                                           1, [ RPNOperator.List ] ),

    'make_julian_time'      : RPNOperator( makeJulianTime,
                                           1, [ RPNOperator.List ] ),

    # function
    'filter'                : RPNOperator( filterList,
                                           2, [ RPNOperator.Generator, RPNOperator.Function ] ),

    'filter_by_index'       : RPNOperator( filterListByIndex,
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'unfilter'              : RPNOperator( lambda n, k: filterList( n, k, True ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'unfilter_by_index'     : RPNOperator( lambda n, k: filterListByIndex( n, k, True ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    # list
    'alternate_signs'       : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, False ) ),
                                           1, [ RPNOperator.Generator ] ),

    'alternate_signs_2'     : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, True ) ),
                                           1, [ RPNOperator.Generator ] ),

    'alternating_sum'       : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                           1, [ RPNOperator.Generator ] ),

    'alternating_sum_2'     : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                           1, [ RPNOperator.Generator ] ),

    'and_all'               : RPNOperator( getAndAll,
                                           1, [ RPNOperator.List ] ),

    'append'                : RPNOperator( appendLists,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'collate'               : RPNOperator( collate,
                                           1, [ RPNOperator.List ] ),

    'count'                 : RPNOperator( countElements,
                                           1, [ RPNOperator.Generator ] ),

    'diffs'                 : RPNOperator( lambda n: RPNGenerator( getListDiffs( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'diffs2'                : RPNOperator( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'element'               : RPNOperator( lambda n, k: RPNGenerator( getListElement( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.NonnegativeInteger ] ),

    'enumerate'             : RPNOperator( lambda n, k: RPNGenerator( enumerateList( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Integer ] ),

    'flatten'               : RPNOperator( flatten,
                                           1, [ RPNOperator.List ] ),

    'group_elements'        : RPNOperator( groupElements,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'interleave'            : RPNOperator( interleave,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'intersection'          : RPNOperator( makeIntersection,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'left'                  : RPNOperator( getLeft,
                                           2, [ RPNOperator.List, RPNOperator.NonnegativeInteger ] ),

    'max_index'             : RPNOperator( getIndexOfMax,
                                           1, [ RPNOperator.List ] ),

    'min_index'             : RPNOperator( getIndexOfMin,
                                           1, [ RPNOperator.List ] ),

    'nand_all'              : RPNOperator( getNandAll,
                                           1, [ RPNOperator.List ] ),

    'nonzero'               : RPNOperator( getNonzeroes,
                                           1, [ RPNOperator.List ] ),

    'nor_all'               : RPNOperator( getNorAll,
                                           1, [ RPNOperator.List ] ),

    'occurrences'           : RPNOperator( getOccurrences,
                                           1, [ RPNOperator.List ] ),

    'occurrence_cumulative' : RPNOperator( getCumulativeOccurrenceRatios,
                                           1, [ RPNOperator.List ] ),

    'occurrence_ratios'     : RPNOperator( getOccurrenceRatios,
                                           1, [ RPNOperator.List ] ),

    'or_all'                : RPNOperator( getOrAll,
                                           1, [ RPNOperator.List ] ),

    'permute_lists'         : RPNOperator( permuteLists,
                                           1, [ RPNOperator.List ] ),

    'ratios'                : RPNOperator( lambda n: RPNGenerator( getListRatios( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'ratios2'               : RPNOperator( lambda n: RPNGenerator( getCumulativeListRatios( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'reduce'                : RPNOperator( reduceList,
                                           1, [ RPNOperator.List ] ),

    'reverse'               : RPNOperator( getReverse,
                                           1, [ RPNOperator.List ] ),

    'right'                 : RPNOperator( getRight,
                                           2, [ RPNOperator.List, RPNOperator.NonnegativeInteger ] ),

    'shuffle'               : RPNOperator( shuffleList,
                                           1, [ RPNOperator.List ] ),

    'slice'                 : RPNOperator( lambda a, b, c: RPNGenerator( getSlice( a, b, c ) ),
                                           3, [ RPNOperator.List, RPNOperator.Integer,
                                                RPNOperator.Integer ] ),

    'sort'                  : RPNOperator( sortAscending,
                                           1, [ RPNOperator.List ] ),

    'sort_descending'       : RPNOperator( sortDescending,
                                           1, [ RPNOperator.List ] ),

    'sublist'               : RPNOperator( lambda a, b, c: RPNGenerator( getSublist( a, b, c ) ),
                                           3, [ RPNOperator.List, RPNOperator.Integer,
                                                RPNOperator.Integer ] ),

    'union'                 : RPNOperator( makeUnion,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'unique'                : RPNOperator( getUniqueElements,
                                           1, [ RPNOperator.List ] ),

    'zero'                  : RPNOperator( getZeroes,
                                           1, [ RPNOperator.List ] ),

    # number_theory
    'base'                  : RPNOperator( interpretAsBase,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'cf'                    : RPNOperator( convertFromContinuedFraction,
                                           1, [ RPNOperator.List ] ),

    'crt'                   : RPNOperator( calculateChineseRemainderTheorem,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'frobenius'             : RPNOperator( getFrobeniusNumber,
                                           1, [ RPNOperator.List ] ),

    'is_friendly'           : RPNOperator( isFriendly,
                                           1, [ RPNOperator.List ] ),

    'linear_recurrence'     : RPNOperator( getNthLinearRecurrence,
                                           3, [ RPNOperator.List, RPNOperator.List,
                                                RPNOperator.PositiveInteger ] ),

    # lexicographic
    'combine_digits'        : RPNOperator( combineDigits,
                                           1, [ RPNOperator.Generator ] ),

    # powers_and_roots
    'tower'                 : RPNOperator( calculatePowerTower,
                                           1, [ RPNOperator.List ] ),

    'tower2'                : RPNOperator( calculatePowerTower2,
                                           1, [ RPNOperator.List ] ),

    # special
    'echo'                  : RPNOperator( addEchoArgument,
                                           1, [ RPNOperator.Default ] ),
}


# //******************************************************************************
# //
# //  operators
# //
# //  Regular operators expect zero or more single values and if those arguments
# //  are lists, rpn will iterate calls to the operator handler for each element
# //  in the list.   Multiple lists for arguments are not permutated.  Instead,
# //  the operator handler is called for each element in the first list, along
# //  with the nth element of each other argument that is also a list.
# //
# //  Note:  There is something about the way some of the mpmath functions are
# //  defined causes them not to work when used in a user-defined function.  So,
# //  they are all wrapped in a lambda.
# //
# //******************************************************************************

operators = {
    # algebra
    'find_polynomial'                : RPNOperator( findPolynomial,
                                                    2, [ RPNOperator.Default, RPNOperator.PositiveInteger ] ),

    'solve_cubic'                    : RPNOperator( solveCubicPolynomial,
                                                    4, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Default ] ),

    'solve_quadratic'                : RPNOperator( solveQuadraticPolynomial,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default ] ),

    'solve_quartic'                  : RPNOperator( solveQuarticPolynomial,
                                                    5, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default ] ),

    # arithmetic
    'abs'                            : RPNOperator( getAbsoluteValue,
                                                    1, [ RPNOperator.Default ] ),

    'add'                            : RPNOperator( add,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'ceiling'                        : RPNOperator( getCeiling,
                                                    1, [ RPNOperator.Default ] ),

    'decrement'                      : RPNOperator( lambda n: subtract( n, 1 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'divide'                         : RPNOperator( divide,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'floor'                          : RPNOperator( getFloor,
                                                    1, [ RPNOperator.Default ] ),

    'increment'                      : RPNOperator( lambda n: add( n, 1 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'is_divisible'                   : RPNOperator( isDivisible,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_equal'                       : RPNOperator( isEqual,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'is_even'                        : RPNOperator( lambda n: 1 if fmod( real( n ), 2 ) == 0 else 0,
                                                    1, [ RPNOperator.Real ] ),

    'is_greater'                     : RPNOperator( isGreater,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_less'                        : RPNOperator( isLess,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_equal'                   : RPNOperator( isNotEqual,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ],
                                                    RPNOperator.measurementsAllowed ),

    'is_not_greater'                 : RPNOperator( isNotGreater,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_less'                    : RPNOperator( isNotLess,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_zero'                    : RPNOperator( lambda n: 0 if n == 0 else 1,
                                                    1, [ RPNOperator.Default ] ),

    'is_odd'                         : RPNOperator( lambda n: 1 if fmod( real( n ), 2 ) == 1 else 0,
                                                    1, [ RPNOperator.Real ] ),

    'is_square'                      : RPNOperator( isSquare,
                                                    1, [ RPNOperator.Default ] ),

    'is_zero'                        : RPNOperator( lambda n: 1 if n == 0 else 0,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'larger'                         : RPNOperator( getLarger,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'modulo'                         : RPNOperator( lambda n, k: fmod( real( n ), real( k ) ),
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'multiply'                       : RPNOperator( multiply,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'nearest_int'                    : RPNOperator( getNearestInt,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'negative'                       : RPNOperator( getNegative,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'reciprocal'                     : RPNOperator( takeReciprocal,
                                                    1, [ RPNOperator.Default ] ),

    'round'                          : RPNOperator( roundOff,
                                                    1, [ RPNOperator.Real ],
                                                    RPNOperator.measurementsAllowed ),

    'round_by_value'                 : RPNOperator( roundByValue,
                                                    2, [ RPNOperator.Real, RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'round_by_digits'                : RPNOperator( roundByDigits,
                                                    2, [ RPNOperator.Real, RPNOperator.Integer ],
                                                    RPNOperator.measurementsAllowed ),

    'sign'                           : RPNOperator( getSign,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'smaller'                        : RPNOperator( getSmaller,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'subtract'                       : RPNOperator( subtract,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    # astronomy
    'antitransit_time'               : RPNOperator( getAntitransitTime,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'astronomical_dawn'              : RPNOperator( lambda n, k: getNextDawn( n, k, -18 ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'astronomical_dusk'              : RPNOperator( lambda n, k: getNextDawn( n, k, -18 ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'autumnal_equinox'               : RPNOperator( getAutumnalEquinox,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'dawn'                           : RPNOperator( getNextDawn,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'day_time'                       : RPNOperator( lambda n, k: getTransitTime( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'distance_from_earth'            : RPNOperator( getDistanceFromEarth,
                                                    2, [ RPNOperator.AstronomicalObject, RPNOperator.DateTime ] ),

    'dusk'                           : RPNOperator( getNextDusk,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moonrise'                       : RPNOperator( lambda n, k: getNextRising( ephem.Moon( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moonset'                        : RPNOperator( lambda n, k: getNextSetting( ephem.Moon( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moon_antitransit'               : RPNOperator( lambda n, k: getNextAntitransit( ephem.Moon( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moon_phase'                     : RPNOperator( getMoonPhase,
                                                    1, [ RPNOperator.DateTime ] ),

    'moon_transit'                   : RPNOperator( lambda n, k: getNextTransit( ephem.Moon( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'nautical_dawn'                  : RPNOperator( lambda n, k: getNextDawn( n, k, -12 ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'nautical_dusk'                  : RPNOperator( lambda n, k: getNextDawn( n, k, -12 ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'next_antitransit'               : RPNOperator( getNextAntitransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'next_first_quarter_moon'        : RPNOperator( lambda n: getEphemTime( n, ephem.next_first_quarter_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'next_full_moon'                 : RPNOperator( lambda n: getEphemTime( n, ephem.next_full_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'next_last_quarter_moon'         : RPNOperator( lambda n: getEphemTime( n, ephem.next_last_quarter_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'next_new_moon'                  : RPNOperator( lambda n: getEphemTime( n, ephem.next_new_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'next_rising'                    : RPNOperator( getNextRising,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'next_setting'                   : RPNOperator( getNextSetting,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'next_transit'                   : RPNOperator( getNextTransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'night_time'                     : RPNOperator( lambda n, k: getAntitransitTime( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'previous_antitransit'           : RPNOperator( getPreviousAntitransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'previous_first_quarter_moon'    : RPNOperator( lambda n: getEphemTime( n, ephem.previous_first_quarter_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_full_moon'             : RPNOperator( lambda n: getEphemTime( n, ephem.previous_full_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_last_quarter_moon'     : RPNOperator( lambda n: getEphemTime( n, ephem.previous_last_quarter_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_new_moon'              : RPNOperator( lambda n: getEphemTime( n, ephem.previous_new_moon ),
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_rising'                : RPNOperator( getPreviousRising,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'previous_setting'               : RPNOperator( getPreviousSetting,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'previous_transit'               : RPNOperator( getPreviousTransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'sky_location'                   : RPNOperator( getSkyLocation,
                                                    2, [ RPNOperator.AstronomicalObject, RPNOperator.DateTime ] ),

    'solar_noon'                     : RPNOperator( lambda n, k: getNextTransit( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'summer_solstice'                : RPNOperator( getSummerSolstice,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sunrise'                        : RPNOperator( lambda n, k: getNextRising( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'sunset'                         : RPNOperator( lambda n, k: getNextSetting( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'sun_antitransit'                : RPNOperator( lambda n, k: getNextAntitransit( ephem.Sun( ), n, k ),
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'transit_time'                   : RPNOperator( getTransitTime,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'vernal_equinox'                 : RPNOperator( getVernalEquinox,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'winter_solstice'                : RPNOperator( getWinterSolstice,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # astronomy - heavenly body operators
    'sun'                            : RPNOperator( ephem.Sun,
                                                    0, [ ] ),

    'mercury'                        : RPNOperator( ephem.Mercury,
                                                    0, [ ] ),

    'venus'                          : RPNOperator( ephem.Venus,
                                                    0, [ ] ),

    'moon'                           : RPNOperator( ephem.Moon,
                                                    0, [ ] ),

    'mars'                           : RPNOperator( ephem.Mars,
                                                    0, [ ] ),

    'jupiter'                        : RPNOperator( ephem.Jupiter,
                                                    0, [ ] ),

    'saturn'                         : RPNOperator( ephem.Saturn,
                                                    0, [ ] ),

    'uranus'                         : RPNOperator( ephem.Uranus,
                                                    0, [ ] ),

    'neptune'                        : RPNOperator( ephem.Neptune,
                                                    0, [ ] ),

    'pluto'                          : RPNOperator( ephem.Pluto,
                                                    0, [ ] ),


    # bitwise
    'and'                            : RPNOperator( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x & y ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'count_bits'                     : RPNOperator( getBitCount,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'nand'                           : RPNOperator( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x & y ) ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'nor'                            : RPNOperator( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x | y ) ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'not'                            : RPNOperator( getInvertedBits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'or'                             : RPNOperator( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x | y ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'parity'                         : RPNOperator( lambda n: getBitCount( n ) & 1,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'shift_left'                     : RPNOperator( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x << y ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'shift_right'                    : RPNOperator( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x >> y ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'xor'                            : RPNOperator( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x ^ y ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    # calendar
    'ascension'                      : RPNOperator( calculateAscensionThursday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'ash_wednesday'                  : RPNOperator( calculateAshWednesday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'christmas'                      : RPNOperator( getChristmasDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'calendar'                       : RPNOperator( generateMonthCalendar,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'dst_end'                        : RPNOperator( calculateDSTEnd,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'dst_start'                      : RPNOperator( calculateDSTStart,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'easter'                         : RPNOperator( calculateEaster,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'election_day'                   : RPNOperator( calculateElectionDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'epiphany'                       : RPNOperator( getEpiphanyDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'from_bahai'                     : RPNOperator( convertBahaiDate,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_hebrew'                    : RPNOperator( convertHebrewDate,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_indian_civil'              : RPNOperator( convertIndianCivilDate,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_islamic'                   : RPNOperator( convertIslamicDate,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_julian'                    : RPNOperator( convertJulianDate,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_mayan'                     : RPNOperator( convertMayanDate,
                                                    5, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.PositiveInteger ] ),

    'from_persian'                   : RPNOperator( convertPersianDate,
                                                    3, [ RPNOperator.Integer, RPNOperator.Integer,
                                                         RPNOperator.Integer ] ),

    'iso_date'                       : RPNOperator( getISODate,
                                                    1, [ RPNOperator.DateTime ] ),

    'labor_day'                      : RPNOperator( calculateLaborDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'memorial_day'                   : RPNOperator( calculateMemorialDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_weekday'                    : RPNOperator( calculateNthWeekdayOfMonth,
                                                    4, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                         RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'nth_weekday_of_year'            : RPNOperator( calculateNthWeekdayOfYear,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.Integer,
                                                         RPNOperator.PositiveInteger ] ),

    'pentecost'                      : RPNOperator( calculatePentecostSunday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'presidents_day'                 : RPNOperator( calculatePresidentsDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'thanksgiving'                   : RPNOperator( calculateThanksgiving,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'to_bahai'                       : RPNOperator( getBahaiCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_bahai_name'                  : RPNOperator( getBahaiCalendarDateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_hebrew'                      : RPNOperator( getHebrewCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_hebrew_name'                 : RPNOperator( getHebrewCalendarDateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_indian_civil'                : RPNOperator( getIndianCivilCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_indian_civil_name'           : RPNOperator( getIndianCivilCalendarDateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_islamic'                     : RPNOperator( getIslamicCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_islamic_name'                : RPNOperator( getIslamicCalendarDateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_iso'                         : RPNOperator( getISODate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_iso_name'                    : RPNOperator( getISODateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_julian'                      : RPNOperator( getJulianCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_julian_day'                  : RPNOperator( getJulianDay,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_lilian_day'                  : RPNOperator( getLilianDay,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_mayan'                       : RPNOperator( getMayanCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_ordinal_date'                : RPNOperator( getOrdinalDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_persian'                     : RPNOperator( getPersianCalendarDate,
                                                    1, [ RPNOperator.DateTime ] ),

    'to_persian_name'                : RPNOperator( getPersianCalendarDateName,
                                                    1, [ RPNOperator.DateTime ] ),

    'weekday'                        : RPNOperator( getWeekday,
                                                    1, [ RPNOperator.DateTime ] ),

    'year_calendar'                  : RPNOperator( generateYearCalendar,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # chemistry
    'atomic_number'                  : RPNOperator( getAtomicNumber,
                                                    1, [ RPNOperator.String ] ),

    'atomic_symbol'                  : RPNOperator( lambda n: getElementAttribute( n, 1 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'atomic_weight'                  : RPNOperator( getAtomicWeight,
                                                    1, [ RPNOperator.String ] ),

    'element_block'                  : RPNOperator( lambda n: getElementAttribute( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_boiling_point'          : RPNOperator( getElementBoilingPoint,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_density'                : RPNOperator( getElementDensity,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_description'            : RPNOperator( lambda n: getElementAttribute( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_group'                  : RPNOperator( lambda n: getElementAttribute( n, 2 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_melting_point'          : RPNOperator( getElementMeltingPoint,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_name'                   : RPNOperator( lambda n: getElementAttribute( n, 0 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_occurrence'             : RPNOperator( lambda n: getElementAttribute( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_period'                 : RPNOperator( lambda n: getElementAttribute( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_state'                  : RPNOperator( lambda n: getElementAttribute( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'molar_mass'                     : RPNOperator( lambda n: getMolarMass( RPNMolecule( n ) ),
                                                    1, [ RPNOperator.String ] ),

    # combinatoric
    'bell_polynomial'                : RPNOperator( lambda n, k: bell( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'binomial'                       : RPNOperator( binomial,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'compositions'                   : RPNOperator( getCompositions,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'debruijn'                       : RPNOperator( createDeBruijnSequence,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'lah'                            : RPNOperator( getLahNumber,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'multifactorial'                 : RPNOperator( getNthMultifactorial,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'narayana'                       : RPNOperator( getNarayanaNumber,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'nth_apery'                      : RPNOperator( getNthAperyNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_bell'                       : RPNOperator( lambda n: bell( n ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_bernoulli'                  : RPNOperator( bernoulli,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_catalan'                    : RPNOperator( getNthCatalanNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_delannoy'                   : RPNOperator( getNthDelannoyNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_motzkin'                    : RPNOperator( getNthMotzkinNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_pell'                       : RPNOperator( getNthPellNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_schroeder'                  : RPNOperator( getNthSchroederNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_schroeder_hipparchus'       : RPNOperator( getNthSchroederHipparchusNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_sylvester'                  : RPNOperator( getNthSylvester,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'partitions'                     : RPNOperator( getPartitionNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'permutations'                   : RPNOperator( getPermutations,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),


    # complex
    'argument'                       : RPNOperator( lambda n: arg( n ),
                                                    1, [ RPNOperator.Default ] ),

    'conjugate'                      : RPNOperator( lambda n: conj( n ),
                                                    1, [ RPNOperator.Default ] ),

    'i'                              : RPNOperator( lambda n: mpc( real = '0.0', imag = n ),
                                                    1, [ RPNOperator.Real ] ),

    'imaginary'                      : RPNOperator( lambda n: im( n ),
                                                    1, [ RPNOperator.Default ] ),

    'real'                           : RPNOperator( lambda n: re( n ),
                                                    1, [ RPNOperator.Default ] ),

    # conversion
    'char'                           : RPNOperator( lambda n: convertToSignedInt( n, 8 ),
                                                    1, [ RPNOperator.Integer ] ),

    'dhms'                           : RPNOperator( convertToDHMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'dms'                            : RPNOperator( convertToDMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'double'                         : RPNOperator( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( real( n ) ) ) ) ),
                                                    1, [ RPNOperator.Real ] ),

    'float'                          : RPNOperator( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( real( n ) ) ) ) ),
                                                    1, [ RPNOperator.Real ] ),

    'from_unix_time'                 : RPNOperator( convertFromUnixTime,
                                                    1, [ RPNOperator.Integer ] ),

    'long'                           : RPNOperator( lambda n: convertToSignedInt( n, 32 ),
                                                    1, [ RPNOperator.Integer ] ),

    'longlong'                       : RPNOperator( lambda n: convertToSignedInt( n, 64 ),
                                                    1, [ RPNOperator.Integer ] ),

    'hms'                            : RPNOperator( convertToHMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'integer'                        : RPNOperator( convertToSignedInt,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'invert_units'                   : RPNOperator( invertUnits,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'uchar'                          : RPNOperator( lambda n: fmod( real_int( n ), power( 2, 8 ) ),
                                                    1, [ RPNOperator.Integer ] ),

    'uinteger'                       : RPNOperator( lambda n, k: fmod( real_int( n ), power( 2, real( k ) ) ),
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'ulong'                          : RPNOperator( lambda n: fmod( real_int( n ), power( 2, 32 ) ),
                                                    1, [ RPNOperator.Integer ] ),

    'ulonglong'                      : RPNOperator( lambda n: fmod( real_int( n ), power( 2, 64 ) ),
                                                    1, [ RPNOperator.Integer ] ),

    'undouble'                       : RPNOperator( interpretAsDouble,
                                                    1, [ RPNOperator.Integer ] ),

    'unfloat'                        : RPNOperator( interpretAsFloat,
                                                    1, [ RPNOperator.Integer ] ),

    'ushort'                         : RPNOperator( lambda n: fmod( real_int( n ), power( 2, 16 ) ),
                                                    1, [ RPNOperator.Integer ] ),

    'short'                          : RPNOperator( lambda n: convertToSignedInt( n, 16 ),
                                                    1, [ RPNOperator.Integer ] ),

    'to_unix_time'                   : RPNOperator( convertToUnixTime,
                                                    1, [ RPNOperator.DateTime ] ),

    'ydhms'                          : RPNOperator( convertToYDHMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    # date_time
    'get_year'                       : RPNOperator( getYear,
                                                    1, [ RPNOperator.DateTime ] ),

    'get_month'                      : RPNOperator( getMonth,
                                                    1, [ RPNOperator.DateTime ] ),

    'get_day'                        : RPNOperator( getDay,
                                                    1, [ RPNOperator.DateTime ] ),

    'get_hour'                       : RPNOperator( getHour,
                                                    1, [ RPNOperator.DateTime ] ),

    'get_minute'                     : RPNOperator( getMinute,
                                                    1, [ RPNOperator.DateTime ] ),

    'get_second'                     : RPNOperator( getSecond,
                                                    1, [ RPNOperator.DateTime ] ),

    'iso_day'                        : RPNOperator( getISODay,
                                                    1, [ RPNOperator.DateTime ] ),

    'now'                            : RPNOperator( RPNDateTime.getNow,
                                                    0, [ ] ),

    'today'                          : RPNOperator( getToday,
                                                    0, [ ] ),

    'tomorrow'                       : RPNOperator( getTomorrow,
                                                    0, [ ] ),

    'yesterday'                      : RPNOperator( getYesterday,
                                                    0, [ ] ),

    # function
    'eval'                           : RPNOperator( lambda n, func: func.evaluate( n ),
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'eval2'                          : RPNOperator( lambda a, b, func: func.evaluate( a, b ),
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'eval3'                          : RPNOperator( lambda a, b, c, func: func.evaluate( a, b, c ),
                                                    4, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Function ] ),

    'limit'                          : RPNOperator( lambda n, func: limit( lambda x: func.evaluate( x ), n ),
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'limitn'                         : RPNOperator( lambda n, func: limit( lambda x: func.evaluate( x ), n, direction = -1 ),
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'negate'                         : RPNOperator( lambda n: 1 if n == 0 else 0,
                                                    1, [ RPNOperator.Boolean ] ),

    'nprod'                          : RPNOperator( lambda start, end, func: nprod( lambda x: func.evaluate( x ), [ start, end ] ),
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'nsum'                           : RPNOperator( lambda start, end, func: nsum( lambda x: func.evaluate( x, func ), [ start, end ] ),
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'plot'                           : RPNOperator( plotFunction,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'plot2'                          : RPNOperator( plot2DFunction,
                                                    5, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'plotc'                          : RPNOperator( plotComplexFunction,
                                                    5, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    # geography
    'distance'                       : RPNOperator( getDistance,
                                                    2, [ RPNOperator.Location, RPNOperator.Location ] ),

    'latlong'                        : RPNOperator( lambda n, k: RPNLocation( n, k ),
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'location'                       : RPNOperator( getLocation,
                                                    1, [ RPNOperator.String ] ),

    'location_info'                  : RPNOperator( getLocationInfo,
                                                    1, [ RPNOperator.String ] ),

    # geometry
    'antiprism_area'                 : RPNOperator( getAntiprismSurfaceArea,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ] ),

    'antiprism_volume'               : RPNOperator( getAntiprismVolume,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ] ),

    'cone_area'                      : RPNOperator( getConeSurfaceArea,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'cone_volume'                    : RPNOperator( getConeVolume,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'dodecahedron_area'              : RPNOperator( getDodecahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'dodecahedron_volume'            : RPNOperator( getDodecahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'icosahedron_area'               : RPNOperator( getIcosahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'icosahedron_volume'             : RPNOperator( getIcosahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'n_sphere_area'                  : RPNOperator( getNSphereSurfaceArea,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                         RPNOperator.measurementsAllowed ),

    'n_sphere_radius'                : RPNOperator( getNSphereRadius,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                             RPNOperator.measurementsAllowed ),

    'n_sphere_volume'                : RPNOperator( getNSphereVolume,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                         RPNOperator.measurementsAllowed ),

    'octahedron_area'                : RPNOperator( getOctahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'octahedron_volume'              : RPNOperator( getOctahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'polygon_area'                   : RPNOperator( getRegularPolygonArea,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.Measurement ] ),

    'prism_area'                     : RPNOperator( getPrismSurfaceArea,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal,
                                                         RPNOperator.NonnegativeReal ] ),

    'prism_volume'                   : RPNOperator( getPrismVolume,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal,
                                                         RPNOperator.NonnegativeReal ] ),

    'sphere_area'                    : RPNOperator( lambda n: getNSphereSurfaceArea( n, 3 ),
                                                    1, [ RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_radius'                  : RPNOperator( lambda n: getNSphereRadius( n, 3 ),
                                                    1, [ RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_volume'                  : RPNOperator( lambda n: getNSphereVolume( n, 3 ),
                                                    1, [ RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'tetrahedron_area'               : RPNOperator( getTetrahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'tetrahedron_volume'             : RPNOperator( getTetrahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'torus_area'                     : RPNOperator( getTorusSurfaceArea,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'torus_volume'                   : RPNOperator( getTorusVolume,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'triangle_area'                  : RPNOperator( getTriangleArea,
                                                    3, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal,
                                                         RPNOperator.NonnegativeReal ] ),

    # lexicographic
    'add_digits'                     : RPNOperator( addDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'build_numbers'                  : RPNOperator( buildNumbers,
                                                    1, [ RPNOperator.String ] ),

    'dup_digits'                     : RPNOperator( duplicateDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'find_palindrome'                : RPNOperator( findPalindrome,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'get_digits'                     : RPNOperator( getDigits,
                                                    1, [ RPNOperator.Integer ] ),

    'get_left_truncations'           : RPNOperator( lambda n: RPNGenerator.createGenerator( getLeftTruncations, n ),
                                                    1, [ RPNOperator.Integer ] ),

    'get_right_truncations'          : RPNOperator( lambda n: RPNGenerator.createGenerator( getRightTruncations, n ),
                                                    1, [ RPNOperator.Integer ] ),

    'is_automorphic'                 : RPNOperator( lambda n: isMorphic( n, 2 ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_kaprekar'                    : RPNOperator( isKaprekar,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_morphic'                     : RPNOperator( isMorphic,
                                                    2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'is_narcissistic'                : RPNOperator( isNarcissistic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_palindrome'                  : RPNOperator( isPalindrome,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_pandigital'                  : RPNOperator( isPandigital,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_trimorphic'                  : RPNOperator( lambda n: isMorphic( n, 3 ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'multiply_digits'                : RPNOperator( multiplyDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'permute_digits'                 : RPNOperator( lambda n: RPNGenerator.createPermutations( getMPFIntegerAsString( n ) ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'reverse_digits'                 : RPNOperator( reverseDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'sum_digits'                     : RPNOperator( sumDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    # list
    'exponential_range'              : RPNOperator( RPNGenerator.createExponential,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.PositiveInteger ] ),

    'geometric_range'                : RPNOperator( RPNGenerator.createGeometric,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.PositiveInteger ] ),

    'interval_range'                 : RPNOperator( RPNGenerator.createRange,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.Real ] ),

    'range'                          : RPNOperator( RPNGenerator.createRange,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'sized_range'                    : RPNOperator( RPNGenerator.createSizedRange,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.Real ] ),

    # logarithms
    'lambertw'                       : RPNOperator( lambda n: lambertw( n ),
                                                    1, [ RPNOperator.Default ] ),

    'li'                             : RPNOperator( lambda n: li( n ),
                                                    1, [ RPNOperator.Default ] ),

    'ln'                             : RPNOperator( lambda n: ln( n ),
                                                    1, [ RPNOperator.Default ] ),

    'log10'                          : RPNOperator( lambda n: log10( n ),
                                                    1, [ RPNOperator.Default ] ),

    'log2'                           : RPNOperator( lambda n: log( n, 2 ),
                                                    1, [ RPNOperator.Default ] ),

    'logxy'                          : RPNOperator( lambda n, k: log( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'polyexp'                        : RPNOperator( lambda n, k: polyexp( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'polylog'                        : RPNOperator( lambda n, k: polylog( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    # number_theory
    'abundance'                      : RPNOperator( lambda n: fdiv( getSigma( n ), n ),
                                                    1, RPNOperator.PositiveInteger ),

    'aliquot'                        : RPNOperator( lambda n, k: RPNGenerator.createGenerator( getAliquotSequence, [ n, k ] ),
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'alternating_factorial'          : RPNOperator( getNthAlternatingFactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'barnesg'                        : RPNOperator( lambda n: barnesg( n ),
                                                    1, [ RPNOperator.Default ] ),

    'beta'                           : RPNOperator( lambda n, k: beta( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'calkin_wilf'                    : RPNOperator( getNthCalkinWilf,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'count_divisors'                 : RPNOperator( getDivisorCount,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'digamma'                        : RPNOperator( lambda n: psi( 0, n ),
                                                    1, [ RPNOperator.Default ] ),

    'divisors'                       : RPNOperator( getDivisors,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'double_factorial'               : RPNOperator( lambda n: fac2( n ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'ecm'                            : RPNOperator( getECMFactorList,
                                                    1, [ RPNOperator.Integer ] ),

    'egypt'                          : RPNOperator( getGreedyEgyptianFraction,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'eta'                            : RPNOperator( lambda n: altzeta( n ),
                                                    1, [ RPNOperator.Default ] ),

    'euler_brick'                    : RPNOperator( makeEulerBrick,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                    RPNOperator.PositiveInteger ] ),

    'euler_phi'                      : RPNOperator( getEulerPhi,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'factor'                         : RPNOperator( getFactorList,
                                                    1, [ RPNOperator.Integer ] ),

    'factorial'                      : RPNOperator( lambda n: fac( n ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'fibonacci'                      : RPNOperator( getNthFibonacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'fibonorial'                     : RPNOperator( getNthFibonorial,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'generate_polydivisibles'        : RPNOperator( lambda n: RPNGenerator.createGenerator( generatePolydivisibles, n ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'erdos_persistence'              : RPNOperator( lambda n: getPersistence( n, 1, True ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'fraction'                       : RPNOperator( interpretAsFraction,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'gamma'                          : RPNOperator( lambda n: gamma( n ),
                                                    1, [ RPNOperator.Default ] ),

    'harmonic'                       : RPNOperator( lambda n: harmonic( n ),
                                                    1, [ RPNOperator.Default ] ),

    'heptanacci'                     : RPNOperator( lambda n: getNthKFibonacciNumber( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexanacci'                      : RPNOperator( lambda n: getNthKFibonacciNumber( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hyperfactorial'                 : RPNOperator( lambda n: hyperfac( n ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_abundant'                    : RPNOperator( isAbundant,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_achilles'                    : RPNOperator( isAchillesNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_deficient'                   : RPNOperator( isDeficient,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_k_hyperperfect'              : RPNOperator( isKHyperperfect,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'is_k_semiprime'                 : RPNOperator( isKSemiPrime,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_perfect'                     : RPNOperator( isPerfect,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_polydivisible'               : RPNOperator( isPolydivisible,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_powerful'                    : RPNOperator( isPowerful,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_prime'                       : RPNOperator( lambda n: 1 if isPrime( n ) else 0,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_pronic'                      : RPNOperator( isPronic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_rough'                       : RPNOperator( isRough,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_semiprime'                   : RPNOperator( lambda n: isKSemiPrime( n, 2 ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_smooth'                      : RPNOperator( isSmooth,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_sphenic'                     : RPNOperator( isSphenic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_squarefree'                  : RPNOperator( isSquareFree,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_unusual'                     : RPNOperator( isUnusual,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'k_fibonacci'                    : RPNOperator( getNthKFibonacciNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'leyland'                        : RPNOperator( lambda n, k: fadd( power( n, k ), power( k, n ) ),
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'log_gamma'                      : RPNOperator( lambda n: loggamma( n ),
                                                    1, [ RPNOperator.Default ] ),

    'lucas'                          : RPNOperator( getNthLucasNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'make_cf'                        : RPNOperator( lambda n, k: RPNContinuedFraction( real( n ), maxterms = real( k ), cutoff = power( 10, -( mp.dps - 2 ) ) ),
                                                    2, [ RPNOperator.Real, RPNOperator.PositiveInteger ] ),

    'make_pyth_3'                    : RPNOperator( makePythagoreanTriple,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'make_pyth_4'                    : RPNOperator( makePythagoreanQuadruple,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'merten'                         : RPNOperator( getNthMerten,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'mobius'                         : RPNOperator( getMobius,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_carol'                      : RPNOperator( lambda n: fsub( power( fsub( power( 2, real( n ) ), 1 ), 2 ), 2 ),
                                                    1, [ RPNOperator.Real ] ),

    'nth_jacobsthal'                 : RPNOperator( getNthJacobsthalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_kynea'                      : RPNOperator( lambda n: fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ),
                                                    1, [ RPNOperator.Real ] ),

    'nth_leonardo'                   : RPNOperator( lambda n: fsub( fmul( 2, fib( fadd( n, 1 ) ) ), 1 ),
                                                    1, [ RPNOperator.Real ] ),

    'nth_mersenne_prime'             : RPNOperator( getNthMersennePrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_padovan'                    : RPNOperator( getNthPadovanNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_stern'                      : RPNOperator( getNthStern,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'n_persistence'                  : RPNOperator( getPersistence,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'octanacci'                      : RPNOperator( lambda n: getNthKFibonacciNumber( n, 8 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pascal_triangle'                : RPNOperator( lambda n: RPNGenerator.createGenerator( getNthPascalLine, n ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentanacci'                     : RPNOperator( lambda n: getNthKFibonacciNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'persistence'                    : RPNOperator( getPersistence,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'polygamma'                      : RPNOperator( lambda n, k: psi( n, k ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.Default ] ),

    'repunit'                        : RPNOperator( getNthBaseKRepunit,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'reversal_addition'              : RPNOperator( lambda n, k: RPNGenerator( getNthReversalAddition( n, k ) ),
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'riesel'                         : RPNOperator( lambda n: fsub( fmul( real( n ), power( 2, n ) ), 1 ),
                                                    1, [ RPNOperator.Real ] ),

    'show_n_persistence'             : RPNOperator( lambda n, k: RPNGenerator.createGenerator( showPersistence, [ n, k ] ),
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'show_persistence'               : RPNOperator( lambda n: RPNGenerator.createGenerator( showPersistence, [ n ] ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'show_erdos_persistence'         : RPNOperator( lambda n: RPNGenerator.createGenerator( showErdosPersistence, [ n ] ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'sigma'                          : RPNOperator( getSigma,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'sigma_n'                        : RPNOperator( getSigmaN,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'subfactorial'                   : RPNOperator( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'superfactorial'                 : RPNOperator( lambda n: superfac( n ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'tetranacci'                     : RPNOperator( lambda n: getNthKFibonacciNumber( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'thabit'                         : RPNOperator( lambda n: fsub( fmul( 3, power( 2, n ) ), 1 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'tribonacci'                     : RPNOperator( lambda n: getNthKFibonacciNumber( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'trigamma'                       : RPNOperator( lambda n: psi( 1, n ),
                                                    1, [ RPNOperator.Default ] ),

    'unit_roots'                     : RPNOperator( lambda n: unitroots( real_int( n ) ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'zeta'                           : RPNOperator( lambda n: zeta( n ),
                                                    1, [ RPNOperator.Default ] ),

    'zeta_zero'                      : RPNOperator( getNthZetaZero,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # physics
    'acceleration'                   : RPNOperator( calculateAcceleration,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'energy_equivalence'             : RPNOperator( calculateEnergyEquivalence,
                                                    1, [ RPNOperator.Measurement ] ),

    'escape_velocity'                : RPNOperator( calculateEscapeVelocity,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'horizon_distance'               : RPNOperator( lambda n: calculateHorizonDistance( n, constants[ 'earth_radius' ].function( ) ),
                                                    1, [ RPNOperator.Measurement ] ),

    'kinetic_energy'                 : RPNOperator( calculateKineticEnergy,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'mass_equivalence'               : RPNOperator( calculateMassEquivalence,
                                                    1, [ RPNOperator.Measurement ] ),

    'orbital_mass'                   : RPNOperator( calculateOrbitalMass,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'orbital_period'                 : RPNOperator( calculateOrbitalPeriod,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'orbital_radius'                 : RPNOperator( calculateOrbitalRadius,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'orbital_velocity'               : RPNOperator( calculateOrbitalVelocity,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'schwarzchild_radius'            : RPNOperator( calculateSchwarzchildRadius,
                                                    1, [ RPNOperator.Measurement ] ),

    'surface_gravity'                : RPNOperator( calculateSurfaceGravity,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    'time_dilation'                  : RPNOperator( calculateTimeDilation,
                                                    1, [ RPNOperator.Measurement ] ),

    'velocity'                       : RPNOperator( calculateVelocity,
                                                    2, [ RPNOperator.Measurement, RPNOperator.Measurement ] ),

    # polygonal
    'centered_decagonal'             : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 10 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_heptagonal'            : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_hexagonal'             : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_nonagonal'             : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 9 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_octagonal'             : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 8 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_pentagonal'            : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_polygonal'             : RPNOperator( getCenteredPolygonalNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'centered_square'                : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_triangular'            : RPNOperator( lambda n: getCenteredPolygonalNumber( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal'                      : RPNOperator( lambda n: getNthPolygonalNumber( n, 10 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_centered_square'      : RPNOperator( getNthDecagonalCenteredSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_heptagonal'           : RPNOperator( getNthDecagonalHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_hexagonal'            : RPNOperator( getNthDecagonalHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_nonagonal'            : RPNOperator( getNthDecagonalNonagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_octagonal'            : RPNOperator( getNthDecagonalOctagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_pentagonal'           : RPNOperator( getNthDecagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal_triangular'           : RPNOperator( getNthDecagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'generalized_pentagonal'         : RPNOperator( lambda n: getNthGeneralizedPolygonalNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal'                     : RPNOperator( lambda n: getNthPolygonalNumber( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_hexagonal'           : RPNOperator( getNthHeptagonalHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_pentagonal'          : RPNOperator( getNthHeptagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_square'              : RPNOperator( getNthHeptagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_triangular'          : RPNOperator( getNthHeptagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal'                      : RPNOperator( lambda n: getNthPolygonalNumber( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal_pentagonal'           : RPNOperator( getNthHexagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal_square'               : RPNOperator( getNthHexagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal'                      : RPNOperator( lambda n: getNthPolygonalNumber( n, 9 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_heptagonal'           : RPNOperator( getNthNonagonalHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_hexagonal'            : RPNOperator( getNthNonagonalHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_octagonal'            : RPNOperator( getNthNonagonalOctagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_pentagonal'           : RPNOperator( getNthNonagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_square'               : RPNOperator( getNthNonagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal_triangular'           : RPNOperator( getNthNonagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_decagonal'         : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 10 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_heptagonal'        : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_hexagonal'         : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_nonagonal'         : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 9 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_octagonal'         : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 8 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_pentagonal'        : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_polygonal'         : RPNOperator( findCenteredPolygonalNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'nth_centered_square'            : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_triangular'        : RPNOperator( lambda n: findCenteredPolygonalNumber( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_decagonal'                  : RPNOperator( lambda n: findNthPolygonalNumber( n, 10 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_heptagonal'                 : RPNOperator( lambda n: findNthPolygonalNumber( n, 7 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_hexagonal'                  : RPNOperator( lambda n: findNthPolygonalNumber( n, 6 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_nonagonal'                  : RPNOperator( lambda n: findNthPolygonalNumber( n, 9 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_octagonal'                  : RPNOperator( lambda n: findNthPolygonalNumber( n, 8 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_pentagonal'                 : RPNOperator( lambda n: findNthPolygonalNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_polygonal'                  : RPNOperator( findNthPolygonalNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'nth_square'                     : RPNOperator( lambda n: findNthPolygonalNumber( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_triangular'                 : RPNOperator( lambda n: findNthPolygonalNumber( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal'                      : RPNOperator( lambda n: getNthPolygonalNumber( n, 8 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal_heptagonal'           : RPNOperator( getNthOctagonalHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal_hexagonal'            : RPNOperator( getNthOctagonalHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal_pentagonal'           : RPNOperator( getNthOctagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal_square'               : RPNOperator( getNthOctagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal_triangular'           : RPNOperator( getNthOctagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal'                     : RPNOperator( lambda n: getNthPolygonalNumber( n, 5 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal_square'              : RPNOperator( getNthPentagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal_triangular'          : RPNOperator( getNthPentagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polygonal'                      : RPNOperator( getNthPolygonalNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'square_triangular'              : RPNOperator( getNthSquareTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'star'                           : RPNOperator( getNthStarNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triangular'                     : RPNOperator( lambda n: getNthPolygonalNumber( n, 3 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # polyhedral
    'centered_cube'                  : RPNOperator( getNthCenteredCubeNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_dodecahedral'          : RPNOperator( getNthCenteredDodecahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_icosahedral'           : RPNOperator( getNthCenteredIcosahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_octahedral'            : RPNOperator( getNthCenteredOctahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_tetrahedral'           : RPNOperator( getNthCenteredTetrahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'dodecahedral'                   : RPNOperator( lambda n: polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], real( n ) ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'icosahedral'                    : RPNOperator( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], real( n ) ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octahedral'                     : RPNOperator( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], real( n ) ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentatope'                      : RPNOperator( getNthPentatopeNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polytope'                       : RPNOperator( getNthPolytopeNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'pyramid'                        : RPNOperator( lambda n: getNthPolygonalPyramidalNumber( n, 4 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'rhombdodec'                     : RPNOperator( getNthRhombicDodecahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'stella_octangula'               : RPNOperator( getNthStellaOctangulaNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'tetrahedral'                    : RPNOperator( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'truncated_octahedral'           : RPNOperator( getNthTruncatedOctahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'truncated_tetrahedral'          : RPNOperator( getNthTruncatedTetrahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # powers_and_roots
    'agm'                            : RPNOperator( lambda n, k: agm( n, k ),
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'cube'                           : RPNOperator( lambda n: getPower( n, 3 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cube_root'                      : RPNOperator( lambda n: getRoot( n, 3 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'exp'                            : RPNOperator( lambda n: exp( n ),
                                                    1, [ RPNOperator.Default ] ),

    'exp10'                          : RPNOperator( lambda n: power( 10, n ),
                                                    1, [ RPNOperator.Default ] ),

    'expphi'                         : RPNOperator( lambda n: power( phi, n ),
                                                    1, [ RPNOperator.Default ] ),

    'hyper4_2'                       : RPNOperator( tetrateLarge,
                                                    2, [ RPNOperator.Default, RPNOperator.Real ] ),

    'power'                          : RPNOperator( getPower,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'powmod'                         : RPNOperator( getPowMod,
                                                    3, [ RPNOperator.Integer, RPNOperator.Integer,
                                                         RPNOperator.Integer ] ),

    'root'                           : RPNOperator( getRoot,
                                                    2, [ RPNOperator.Default, RPNOperator.Real ],
                                                    RPNOperator.measurementsAllowed ),

    'square'                         : RPNOperator( lambda n: getPower( n, 2 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'square_root'                    : RPNOperator( lambda n: getRoot( n, 2 ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'tetrate'                        : RPNOperator( tetrate,
                                                    2, [ RPNOperator.Default, RPNOperator.Real ] ),

    # prime_number
    'balanced_prime'                 : RPNOperator( getNthBalancedPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'balanced_prime_'                : RPNOperator( getNthBalancedPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'cousin_prime'                   : RPNOperator( getNthCousinPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'cousin_prime_'                  : RPNOperator( getNthCousinPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'double_balanced'                : RPNOperator( getNthDoubleBalancedPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'double_balanced_'               : RPNOperator( getNthDoubleBalancedPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'isolated_prime'                 : RPNOperator( getNthIsolatedPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'next_prime'                     : RPNOperator( lambda n: getNextPrime( n, func=getNextPrimeCandidateForAny ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'next_primes'                    : RPNOperator( lambda n, k: getNextPrimes( n, k, func=getNextPrimeCandidateForAny ),
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'next_quadruplet_prime'          : RPNOperator( lambda n: findQuadrupletPrimes( n )[ 1 ],
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'next_quintuplet_prime'          : RPNOperator( lambda n: findQuintupletPrimes( n )[ 1 ],
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_prime'                      : RPNOperator( lambda n: findPrime( n )[ 0 ],
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_quadruplet_prime'           : RPNOperator( lambda n: findQuadrupletPrimes( n )[ 0 ],
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_quintuplet_prime'           : RPNOperator( lambda n: findQuintupletPrimes( n )[ 0 ],
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polyprime'                      : RPNOperator( getNthPolyPrime,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'prime'                          : RPNOperator( getNthPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'primes'                         : RPNOperator( getPrimes,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'prime_pi'                       : RPNOperator( getPrimePi,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'primorial'                      : RPNOperator( getNthPrimorial,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'quadruplet_prime'               : RPNOperator( getNthQuadrupletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'quadruplet_prime_'              : RPNOperator( getNthQuadrupletPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'quintuplet_prime'               : RPNOperator( getNthQuintupletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'quintuplet_prime_'              : RPNOperator( getNthQuintupletPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'safe_prime'                     : RPNOperator( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sextuplet_prime'                : RPNOperator( getNthSextupletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sextuplet_prime_'               : RPNOperator( getNthSextupletPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_prime'                     : RPNOperator( getNthSexyPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_prime_'                    : RPNOperator( getNthSexyPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_quadruplet'                : RPNOperator( getNthSexyQuadruplet,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_quadruplet_'               : RPNOperator( getNthSexyQuadrupletList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_triplet'                   : RPNOperator( getNthSexyTriplet,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sexy_triplet_'                  : RPNOperator( getNthSexyTripletList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sophie_prime'                   : RPNOperator( getNthSophiePrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'superprime'                     : RPNOperator( getNthSuperPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triplet_prime'                  : RPNOperator( getNthTripletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triplet_prime_'                 : RPNOperator( getNthTripletPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triple_balanced'                : RPNOperator( getNthTripleBalancedPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triple_balanced_'               : RPNOperator( getNthTripleBalancedPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'twin_prime'                     : RPNOperator( getNthTwinPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'twin_prime_'                    : RPNOperator( getNthTwinPrimeList,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # settings
    'accuracy'                       : RPNOperator( lambda n: setAccuracy( fadd( n, 2 ) ),
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'comma'                          : RPNOperator( setComma,
                                                    1, [ RPNOperator.Boolean ] ),

    'comma_mode'                     : RPNOperator( setCommaMode,
                                                    0, [ ] ),

    'decimal_grouping'               : RPNOperator( setDecimalGrouping,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hex_mode'                       : RPNOperator( setHexMode,
                                                    0, [ ] ),

    'identify'                       : RPNOperator( setIdentify,
                                                    1, [ RPNOperator.Boolean ] ),

    'identify_mode'                  : RPNOperator( setIdentifyMode,
                                                    0, [ ] ),

    'input_radix'                    : RPNOperator( setInputRadix,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'integer_grouping'               : RPNOperator( setIntegerGrouping,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'leading_zero'                   : RPNOperator( setLeadingZero,
                                                    1, [ RPNOperator.Boolean ] ),

    'leading_zero_mode'              : RPNOperator( setLeadingZeroMode,
                                                    0, [ ] ),

    'octal_mode'                     : RPNOperator( setOctalMode,
                                                    0, [ ] ),

    'output_radix'                   : RPNOperator( setOutputRadix,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'precision'                      : RPNOperator( setPrecision,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'random'                         : RPNOperator( rand,
                                                    0, [ ] ),

    'random_'                        : RPNOperator( lambda n: RPNGenerator.createGenerator( getMultipleRandoms, n ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'random_integer'                 : RPNOperator( randrange,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'random_integer_'                : RPNOperator( lambda n, k: RPNGenerator.createGenerator( getRandomIntegers, [ n, k ] ),
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'timer'                          : RPNOperator( setTimer,
                                                    1, [ RPNOperator.Boolean ] ),

    'timer_mode'                     : RPNOperator( setTimerMode,
                                                    0, [ ] ),

    # special
    'constant'                       : RPNOperator( createConstant,
                                                    2, [ RPNOperator.Default, RPNOperator.String ],
                                                    RPNOperator.measurementsAllowed ),

    'enumerate_dice'                 : RPNOperator( enumerateDice,
                                                    1, [ RPNOperator.String ] ),

    'enumerate_dice_'                : RPNOperator( enumerateMultipleDice,
                                                    2, [ RPNOperator.String, RPNOperator.PositiveInteger ] ),

    'estimate'                       : RPNOperator( estimate,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'help'                           : RPNOperator( printHelpMessage,
                                                    0, [ ] ),

    'name'                           : RPNOperator( getNumberName,
                                                    1, [ RPNOperator.Integer ] ),

    'oeis'                           : RPNOperator( lambda n: downloadOEISSequence( real_int( n ) ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_comment'                   : RPNOperator( lambda n: downloadOEISText( real_int( n ), 'C', True ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_ex'                        : RPNOperator( lambda n: downloadOEISText( real_int( n ), 'E', True ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_name'                      : RPNOperator( lambda n: downloadOEISText( real_int( n ), 'N', True ),
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'ordinal_name'                   : RPNOperator( getOrdinalName,
                                                    1, [ RPNOperator.Integer ] ),

    'result'                         : RPNOperator( loadResult,
                                                    0, [ ] ),

    'permute_dice'                   : RPNOperator( permuteDice,
                                                    1, [ RPNOperator.String ] ),

    'roll_dice'                      : RPNOperator( rollDice,
                                                    1, [ RPNOperator.String ] ),

    'roll_dice_'                     : RPNOperator( rollMultipleDice,
                                                    2, [ RPNOperator.String, RPNOperator.PositiveInteger ] ),

    'set'                            : RPNOperator( setVariable,
                                                    2, [ RPNOperator.Default, RPNOperator.String ] ),

    'topic'                          : RPNOperator( printHelpTopic,
                                                    1, [ RPNOperator.String ] ),

    'value'                          : RPNOperator( getValue,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    # trigonometry
    'acos'                           : RPNOperator( lambda n: performTrigOperation( n, acos ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acosh'                          : RPNOperator( lambda n: performTrigOperation( n, acosh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acot'                           : RPNOperator( lambda n: performTrigOperation( n, acot ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acoth'                          : RPNOperator( lambda n: performTrigOperation( n, acoth ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acsc'                           : RPNOperator( lambda n: performTrigOperation( n, acsc ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acsch'                          : RPNOperator( lambda n: performTrigOperation( n, acsch ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asec'                           : RPNOperator( lambda n: performTrigOperation( n, asec ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asech'                          : RPNOperator( lambda n: performTrigOperation( n, asech ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asin'                           : RPNOperator( lambda n: performTrigOperation( n, asin ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asinh'                          : RPNOperator( lambda n: performTrigOperation( n, asinh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'atan'                           : RPNOperator( lambda n: performTrigOperation( n, atan ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'atanh'                          : RPNOperator( lambda n: performTrigOperation( n, atanh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cos'                            : RPNOperator( lambda n: performTrigOperation( n, cos ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cosh'                           : RPNOperator( lambda n: performTrigOperation( n, cosh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cot'                            : RPNOperator( lambda n: performTrigOperation( n, cot ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'coth'                           : RPNOperator( lambda n: performTrigOperation( n, coth ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'csc'                            : RPNOperator( lambda n: performTrigOperation( n, csc ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'csch'                           : RPNOperator( lambda n: performTrigOperation( n, csch ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'hypotenuse'                     : RPNOperator( lambda n, k: hypot( n, k ),
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'sec'                            : RPNOperator( lambda n: performTrigOperation( n, sec ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sech'                           : RPNOperator( lambda n: performTrigOperation( n, sech ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sin'                            : RPNOperator( lambda n: performTrigOperation( n, sin ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sinh'                           : RPNOperator( lambda n: performTrigOperation( n, sinh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'tan'                            : RPNOperator( lambda n: performTrigOperation( n, tan ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'tanh'                           : RPNOperator( lambda n: performTrigOperation( n, tanh ),
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    # internal
    '_dump_aliases'                  : RPNOperator( dumpAliases,
                                                    0, [ ] ),

    '_dump_operators'                : RPNOperator( dumpOperators,
                                                    0, [ ] ),

    '_stats'                         : RPNOperator( dumpStats,
                                                    0, [ ] ),

    #   'antitet'                       : RPNOperator( findTetrahedralNumber, 0 ),
    #   'bernfrac'                      : RPNOperator( bernfrac, 1 ),
}

