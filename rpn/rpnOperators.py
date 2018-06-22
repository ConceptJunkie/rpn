#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
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
from mpmath import cplot, fadd, fmod, limit, nint, nprod, nsum, plot, splot
from random import randrange

from rpn.rpnAliases import dumpAliases

from rpn.rpnAstronomy import *
from rpn.rpnCalendar import *
from rpn.rpnChemistry import *
from rpn.rpnCombinatorics import *
from rpn.rpnComputer import *
from rpn.rpnConstants import *
from rpn.rpnConstantUtils import *
from rpn.rpnDateTime import *
from rpn.rpnDice import *
from rpn.rpnDeclarations import *
from rpn.rpnFactor import *
from rpn.rpnGeometry import *
from rpn.rpnInput import *
from rpn.rpnLexicographic import *
from rpn.rpnList import *
from rpn.rpnLocation import *
from rpn.rpnMath import *
from rpn.rpnMeasurement import *
from rpn.rpnModifiers import *
from rpn.rpnName import *
from rpn.rpnNumberTheory import *
from rpn.rpnPersistence import *
from rpn.rpnPhysics import *
from rpn.rpnPolynomials import *
from rpn.rpnPolytope import *
from rpn.rpnPrimeUtils import *
from rpn.rpnSettings import *
from rpn.rpnSpecial import *
from rpn.rpnUtils import *

import rpn.rpnGlobals as g


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
    PositiveInteger = 4         # integer >= 1
    NonnegativeInteger = 5      # integer >= 0
    PrimeInteger = 6,
    String = 7
    DateTime = 8
    Location = 9                # location object (operators will automatically convert a string)
    Boolean = 10                # 0 or 1
    Measurement = 11
    AstronomicalObject = 12
    List = 13                   # the argument must be a list
    Generator = 14              # Generator needs to be a separate type now, but eventually it should be equivalent to List
    Function = 15

    '''This class represents all the data needed to define an operator.'''
    def __init__( self, function, argCount, argTypes = None, allowMeasurements = measurementsNotAllowed ):
        self.function = function
        self.argCount = argCount

        if argTypes is None:
            self.argTypes = list( )
        else:
            self.argTypes = argTypes

        self.allowMeasurements = allowMeasurements

    # This method isn't used yet, but I hope to start using it soon.
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
                    # we need to tee a generator so it can run more than once
                    if isinstance( currentValueList[ g.lastOperand - 1 ], RPNGenerator ):
                        arg = currentValueList[ g.lastOperand - i ].clone( )
                    else:
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

            result = callers[ argsNeeded ]( self.function, *reversed( argList ) )
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

    def generateCalls( self, args ):
        pass


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are always operators that take no arguments.
# //
# //  Please note that the last two RPNOperator arguments must go on a new line
# //  because the 'lambda' functionality parses the lambdas in RPNOperator objects
# //  to build Python code out of them.
# //
# //******************************************************************************

constants = {
    'default'                       : RPNOperator( lambda: -1,
                                                   0, [ ] ),
    'false'                         : RPNOperator( lambda: 0,
                                                   0, [ ] ),
    'true'                          : RPNOperator( lambda: 1,
                                                   0, [ ] ),

    # day of week constants
    'monday'                        : RPNOperator( lambda: 1,
                                                   0, [ ] ),
    'tuesday'                       : RPNOperator( lambda: 2,
                                                   0, [ ] ),
    'wednesday'                     : RPNOperator( lambda: 3,
                                                   0, [ ] ),
    'thursday'                      : RPNOperator( lambda: 4,
                                                   0, [ ] ),
    'friday'                        : RPNOperator( lambda: 5,
                                                   0, [ ] ),
    'saturday'                      : RPNOperator( lambda: 6,
                                                   0, [ ] ),
    'sunday'                        : RPNOperator( lambda: 7,
                                                   0, [ ] ),

    # month constants
    'january'                       : RPNOperator( lambda: 1,
                                                   0, [ ] ),
    'february'                      : RPNOperator( lambda: 2,
                                                   0, [ ] ),
    'march'                         : RPNOperator( lambda: 3,
                                                   0, [ ] ),
    'april'                         : RPNOperator( lambda: 4,
                                                   0, [ ] ),
    'may'                           : RPNOperator( lambda: 5,
                                                   0, [ ] ),
    'june'                          : RPNOperator( lambda: 6,
                                                   0, [ ] ),
    'july'                          : RPNOperator( lambda: 7,
                                                   0, [ ] ),
    'august'                        : RPNOperator( lambda: 8,
                                                   0, [ ] ),
    'september'                     : RPNOperator( lambda: 9,
                                                   0, [ ] ),
    'october'                       : RPNOperator( lambda: 10,
                                                   0, [ ] ),
    'november'                      : RPNOperator( lambda: 11,
                                                   0, [ ] ),
    'december'                      : RPNOperator( lambda: 12,
                                                   0, [ ] ),

    # mathematical constants
    'apery_constant'                : RPNOperator( lambda: mpf( apery ),
                                                   0, [ ] ),
    'catalan_constant'              : RPNOperator( lambda: mpf( catalan ),
                                                   0, [ ] ),
    'champernowne_constant'         : RPNOperator( getChampernowneConstant,
                                                   0, [ ] ),
    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant,
                                                   0, [ ] ),
    'e'                             : RPNOperator( lambda: mpf( e ),
                                                   0, [ ] ),
    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ),
                                                   0, [ ] ),
    'euler_mascheroni_constant'     : RPNOperator( lambda: mpf( euler ),
                                                   0, [ ] ),
    'glaisher_constant'             : RPNOperator( lambda: mpf( glaisher ),
                                                   0, [ ] ),
    'infinity'                      : RPNOperator( lambda: inf,
                                                   0, [ ] ),
    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ),
                                                   0, [ ] ),
    'khinchin_constant'             : RPNOperator( lambda: mpf( khinchin ),
                                                   0, [ ] ),
    'merten_constant'               : RPNOperator( lambda: mpf( mertens ),
                                                   0, [ ] ),
    'mills_constant'                : RPNOperator( getMillsConstant,
                                                   0, [ ] ),
    'negative_infinity'             : RPNOperator( lambda: -inf,
                                                   0, [ ] ),
    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ),
                                                   0, [ ] ),
    'phi'                           : RPNOperator( lambda: mpf( phi ),
                                                   0, [ ] ),
    'pi'                            : RPNOperator( lambda: mpf( pi ),
                                                   0, [ ] ),
    'plastic_constant'              : RPNOperator( getPlasticConstant,
                                                   0, [ ] ),
    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ),
                                                   0, [ ] ),
    'robbins_constant'              : RPNOperator( getRobbinsConstant,
                                                   0, [ ] ),
    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ),
                                                   0, [ ] ),
    'thue_morse_constant'           : RPNOperator( getThueMorseConstant,
                                                   0, [ ] ),

    # physical quantities
    'aa_battery'                    : RPNOperator( lambda: RPNMeasurement( '15400', 'joule' ),
                                                   0, [ ] ),
    'gallon_of_ethanol'             : RPNOperator( lambda: RPNMeasurement( '8.4e7', 'joule' ),
                                                   0, [ ] ),
    'gallon_of_gasoline'            : RPNOperator( lambda: RPNMeasurement( '1.2e8', 'joule' ),
                                                   0, [ ] ),
    'density_of_water'              : RPNOperator( lambda: RPNMeasurement( '1000', 'kilogram/meter^3' ),
                                                   0, [ ] ),
    'density_of_hg'                 : RPNOperator( lambda: RPNMeasurement( '13534', 'kilogram/meter^3' ),
                                                   0, [ ] ),
    'solar_constant'                : RPNOperator( lambda: RPNMeasurement( '1360.8', 'watt/meter^2' ),
                                                   0, [ ] ),       # average... it varies slightly

    # physical constants
    'avogadro_number'               : RPNOperator( lambda: '6.022140857e23',
                                                   0, [ ] ),
    'bohr_radius'                   : RPNOperator( lambda: RPNMeasurement( '5.2917721e-11', [ { 'meter' : 1 } ] ),
                                                   0, [ ] ),
    'boltzmann_constant'            : RPNOperator( getBoltzmannsConstant,
                                                   0, [ ] ),
    'coulomb_constant'              : RPNOperator( lambda: RPNMeasurement( '8.987551787e9', 'joule*meter/coulomb^2' ),
                                                   0, [ ] ),
    'electric_constant'             : RPNOperator( getElectricConstant,
                                                   0, [ ] ),
    'electron_charge'               : RPNOperator( getElectronCharge,
                                                   0, [ ] ),
    'faraday_constant'              : RPNOperator( lambda: RPNMeasurement( '96485.33289', 'coulomb/mole' ),
                                                   0, [ ] ),
    'fine_structure_constant'       : RPNOperator( getFineStructureConstant,
                                                   0, [ ] ),
    'magnetic_constant'             : RPNOperator( lambda: RPNMeasurement( fprod( [ 4, pi, power( 10, -7 ) ] ), 'joule/ampere^2*meter' ),
                                                   0, [ ] ),
    'magnetic_flux_quantum'         : RPNOperator( lambda: RPNMeasurement( '2.067833831e-15', 'Weber' ),
                                                   0, [ ] ),
    'newton_constant'               : RPNOperator( getNewtonsConstant,
                                                   0, [ ] ),
    'nuclear_magneton'              : RPNOperator( lambda: RPNMeasurement( '5.050783699e-27', 'joule/tesla' ),
                                                   0, [ ] ),
    'radiation_constant'            : RPNOperator( lambda: RPNMeasurement( '7.5657e-16', 'kilogram/second^2*meter*kelvin^4' ),
                                                   0, [ ] ),
    'rydberg_constant'              : RPNOperator( lambda: RPNMeasurement( '10973731.568508', 'meter^-1' ),
                                                   0, [ ] ),
    'speed_of_light'                : RPNOperator( getSpeedOfLight,
                                                   0, [ ] ),
    'stefan_boltzmann_constant'     : RPNOperator( lambda: RPNMeasurement( '5.670367e-8', 'watt/meter^2*kelvin^4' ),
                                                   0, [ ] ),
    'vacuum_impedance'              : RPNOperator( lambda: RPNMeasurement( '376.730313461', 'ohm' ),
                                                   0, [ ] ),
    'von_klitzing_constant'         : RPNOperator( lambda: RPNMeasurement( '25812.8074555', 'ohm' ),
                                                   0, [ ] ),

    # programming integer constants
    'max_char'                      : RPNOperator( lambda: ( 1 << 7 ) - 1,
                                                   0, [ ] ),
    'max_double'                    : RPNOperator( getMaxDouble,
                                                   0, [ ] ),
    'max_float'                     : RPNOperator( getMaxFloat,
                                                   0, [ ] ),
    'max_long'                      : RPNOperator( lambda: ( 1 << 31 ) - 1,
                                                   0, [ ] ),
    'max_longlong'                  : RPNOperator( lambda: ( 1 << 63 ) - 1,
                                                   0, [ ] ),
    'max_quadlong'                  : RPNOperator( lambda: ( 1 << 127 ) - 1,
                                                   0, [ ] ),
    'max_short'                     : RPNOperator( lambda: ( 1 << 15 ) - 1,
                                                   0, [ ] ),
    'max_uchar'                     : RPNOperator( lambda: ( 1 << 8 ) - 1,
                                                   0, [ ] ),
    'max_ulong'                     : RPNOperator( lambda: ( 1 << 32 ) - 1,
                                                   0, [ ] ),
    'max_ulonglong'                 : RPNOperator( lambda: ( 1 << 64 ) - 1,
                                                   0, [ ] ),
    'max_uquadlong'                 : RPNOperator( lambda: ( 1 << 128 ) - 1,
                                                   0, [ ] ),
    'max_ushort'                    : RPNOperator( lambda: ( 1 << 16 ) - 1,
                                                   0, [ ] ),
    'min_char'                      : RPNOperator( lambda: -( 1 << 7 ),
                                                   0, [ ] ),
    'min_double'                    : RPNOperator( getMinDouble,
                                                   0, [ ] ),
    'min_float'                     : RPNOperator( getMinFloat,
                                                   0, [ ] ),
    'min_long'                      : RPNOperator( lambda: -( 1 << 31 ),
                                                   0, [ ] ),
    'min_longlong'                  : RPNOperator( lambda: -( 1 << 63 ),
                                                   0, [ ] ),
    'min_quadlong'                  : RPNOperator( lambda: -( 1 << 127 ),
                                                   0, [ ] ),
    'min_short'                     : RPNOperator( lambda: -( 1 << 15 ),
                                                   0, [ ] ),
    'min_uchar'                     : RPNOperator( lambda: 0,
                                                   0, [ ] ),
    'min_ulong'                     : RPNOperator( lambda: 0,
                                                   0, [ ] ),
    'min_ulonglong'                 : RPNOperator( lambda: 0,
                                                   0, [ ] ),
    'min_uquadlong'                 : RPNOperator( lambda: 0,
                                                   0, [ ] ),
    'min_ushort'                    : RPNOperator( lambda: 0,
                                                   0, [ ] ),

    # Planck constants
    'planck_constant'               : RPNOperator( getPlanckConstant,
                                                   0, [ ] ),
    'reduced_planck_constant'       : RPNOperator( getReducedPlanckConstant,
                                                   0, [ ] ),

    'planck_length'                 : RPNOperator( getPlanckLength,
                                                   0, [ ] ),
    'planck_mass'                   : RPNOperator( getPlanckMass,
                                                   0, [ ] ),
    'planck_time'                   : RPNOperator( getPlanckTime,
                                                   0, [ ] ),
    'planck_charge'                 : RPNOperator( getPlanckCharge,
                                                   0, [ ] ),
    'planck_temperature'            : RPNOperator( getPlanckTemperature,
                                                   0, [ ] ),

    'planck_angular_frequency'      : RPNOperator( lambda: RPNMeasurement( '1.85487e43', 'second^-1' ),
                                                   0, [ ] ),
    'planck_area'                   : RPNOperator( lambda: RPNMeasurement( '2.61219618e-70', 'meter^2' ),
                                                   0, [ ] ),
    'planck_current'                : RPNOperator( lambda: RPNMeasurement( '3.4789e25', 'ampere' ),
                                                   0, [ ] ),
    'planck_density'                : RPNOperator( lambda: RPNMeasurement( '5.15518197484e+96', 'kilogram/meter^3' ),
                                                   0, [ ] ),
    'planck_energy'                 : RPNOperator( lambda: RPNMeasurement( '1.220910e28', 'electron-volt' ),
                                                   0, [ ] ),
    'planck_energy_density'         : RPNOperator( lambda: RPNMeasurement( '4.63298e113', 'joule/meter^3' ),
                                                   0, [ ] ),
    'planck_force'                  : RPNOperator( lambda: RPNMeasurement( '1.2102947186e44', 'joule/meter' ),
                                                   0, [ ] ),
    'planck_impedance'              : RPNOperator( lambda: RPNMeasurement( '29.9792458', 'ohm' ),
                                                   0, [ ] ),
    'planck_intensity'              : RPNOperator( lambda: RPNMeasurement( '1.38893e122', 'watt/meter^2' ),
                                                   0, [ ] ),
    'planck_momentum'               : RPNOperator( lambda: RPNMeasurement( '6.52485', 'kilogram*meter/second' ),
                                                   0, [ ] ),
    'planck_power'                  : RPNOperator( lambda: RPNMeasurement( '3.62831e52', 'watt' ),
                                                   0, [ ] ),
    'planck_pressure'               : RPNOperator( lambda: RPNMeasurement( '4.63309e113', 'pascal' ),
                                                   0, [ ] ),
    'planck_voltage'                : RPNOperator( lambda: RPNMeasurement( '1.04295e27', 'volt' ),
                                                   0, [ ] ),
    'planck_volume'                 : RPNOperator( lambda: RPNMeasurement( '4.22190722e-105', 'meter^3' ),
                                                   0, [ ] ),

    # https://en.wikipedia.org/wiki/Natural_units
    # Stoney Units
    # Hartee Atomic Units
    # QCD Units
    # Natural Units

    # subatomic particle constants
    'alpha_particle_mass'           : RPNOperator( lambda: RPNMeasurement( '6.644657230e-27', 'kilogram' ),
                                                   0, [ ] ),
    'deuteron_mass'                 : RPNOperator( lambda: RPNMeasurement( '3.343583719e-27', 'kilogram' ),
                                                   0, [ ] ),
    'electron_mass'                 : RPNOperator( lambda: RPNMeasurement( '9.10938356e-31', 'kilogram' ),
                                                   0, [ ] ),
    'helion_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.006412700e-27', 'kilogram' ),
                                                   0, [ ] ),
    'muon_mass'                     : RPNOperator( lambda: RPNMeasurement( '1.883531594e-28', 'kilogram' ),
                                                   0, [ ] ),
    'neutron_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.674927471e-27', 'kilogram' ),
                                                   0, [ ] ),
    'proton_mass'                   : RPNOperator( lambda: RPNMeasurement( '1.672621898e-27', 'kilogram' ),
                                                   0, [ ] ),
    'tau_mass'                      : RPNOperator( lambda: RPNMeasurement( '3.16747e-27', 'kilogram' ),
                                                   0, [ ] ),
    'triton_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.007356665e-27', 'kilogram' ),
                                                   0, [ ] ),

    # heavenly body constants
    # sun_day
    'sun_luminosity'                : RPNOperator( lambda: RPNMeasurement( '3.826e26', 'watt' ),
                                                   0, [ ] ),
    'sun_mass'                      : RPNOperator( lambda: RPNMeasurement( '1.988500e30', 'kilogram' ),
                                                   0, [ ] ),
    'sun_radius'                    : RPNOperator( lambda: RPNMeasurement( '6.9599e8', 'meter' ),
                                                   0, [ ] ),
    'sun_volume'                    : RPNOperator( lambda: RPNMeasurement( '1.412e27', 'meter^3' ),
                                                   0, [ ] ),

    'mercury_mass'                  : RPNOperator( lambda: RPNMeasurement( '3.301e26', 'kilogram' ),
                                                   0, [ ] ),
    # equitorial radius
    'mercury_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4397e6', 'meter' ),
                                                   0, [ ] ),
    # sidereal orbit period
    'mercury_revolution'            : RPNOperator( lambda: RPNMeasurement( '87.969', 'day' ),
                                                   0, [ ] ),
    'mercury_volume'                : RPNOperator( lambda: RPNMeasurement( '6.083e19', 'meter^3' ),
                                                   0, [ ] ),

    'venus_mass'                    : RPNOperator( lambda: RPNMeasurement( '4.8689952e24', 'kilogram' ),
                                                   0, [ ] ),
    'venus_radius'                  : RPNOperator( lambda: RPNMeasurement( '6.0518e6', 'meter' ),
                                                   0, [ ] ),
    'venus_revolution'              : RPNOperator( lambda: RPNMeasurement( '224.701', 'day' ),
                                                   0, [ ] ),
    'venus_volume'                  : RPNOperator( lambda: RPNMeasurement( '9.2843e20', 'meter^3' ),
                                                   0, [ ] ),

    'earth_density'                 : RPNOperator( lambda: RPNMeasurement( '5.514', 'gram/centimeter^3' ),
                                                   0, [ ] ),        # https://en.wikipedia.org/wiki/Earth#Composition_and_structure
    'earth_gravity'                 : RPNOperator( lambda: RPNMeasurement( '9.806650', 'meter/second^2' ),
                                                   0, [ ] ),
    'earth_mass'                    : RPNOperator( lambda: RPNMeasurement( '5.9640955e24', 'kilogram' ),
                                                   0, [ ] ),        # based on earth_radius and earth_gravity
    'earth_radius'                  : RPNOperator( lambda: RPNMeasurement( '6371800', 'meter' ),
                                                   0, [ ] ),        # https://en.wikipedia.org/wiki/Earth_radius#Global_average_radii - volumetric radius
    'earth_volume'                  : RPNOperator( lambda: RPNMeasurement( '1.083207324897e21', 'meter^3' ),
                                                   0, [ ] ),        # based on earth_radius
    'sidereal_year'                 : RPNOperator( lambda: RPNMeasurement( '365.256360417', 'day' ),
                                                   0, [ ] ),
    'tropical_year'                 : RPNOperator( lambda: RPNMeasurement( '365.24219', 'day' ),
                                                   0, [ ] ),

    'moon_gravity'                  : RPNOperator( lambda: RPNMeasurement( '1.62', 'meter/second^2' ),
                                                   0, [ ] ),
    'moon_mass'                     : RPNOperator( lambda: RPNMeasurement( '7.342e22', 'kilogram' ),
                                                   0, [ ] ),
    'moon_radius'                   : RPNOperator( lambda: RPNMeasurement( '1.7381e6', 'meter' ),
                                                   0, [ ] ),
    'moon_revolution'               : RPNOperator( lambda: RPNMeasurement( '27.3217', 'day' ),
                                                   0, [ ] ),
    'moon_volume'                   : RPNOperator( lambda: RPNMeasurement( '2.1958e19', 'meter^3' ),
                                                   0, [ ] ),

    'mars_mass'                     : RPNOperator( lambda: RPNMeasurement( '6.4191269e23', 'kilogram' ),
                                                   0, [ ] ),
    'mars_radius'                   : RPNOperator( lambda: RPNMeasurement( '3.3962e6', 'meter' ),
                                                   0, [ ] ),
    'mars_revolution'               : RPNOperator( lambda: RPNMeasurement( '686.980', 'day' ),
                                                   0, [ ] ),
    'mars_volume'                   : RPNOperator( lambda: RPNMeasurement( '1.6318e20', 'meter^3' ),
                                                   0, [ ] ),

    'jupiter_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.8983e27', 'kilogram' ),
                                                   0, [ ] ),
    'jupiter_radius'                : RPNOperator( lambda: RPNMeasurement( '7.1492e7', 'meter' ),
                                                   0, [ ] ),
    'jupiter_revolution'            : RPNOperator( lambda: RPNMeasurement( '11.862', 'year' ),
                                                   0, [ ] ),
    'jupiter_volume'                : RPNOperator( lambda: RPNMeasurement( '1.43128e24', 'meter^3' ),
                                                   0, [ ] ),

    'saturn_mass'                   : RPNOperator( lambda: RPNMeasurement( '5.6836e26', 'kilogram' ),
                                                   0, [ ] ),
    'saturn_radius'                 : RPNOperator( lambda: RPNMeasurement( '6.0268e7', 'meter' ),
                                                   0, [ ] ),
    'saturn_revolution'             : RPNOperator( lambda: RPNMeasurement( '29.457', 'year' ),
                                                   0, [ ] ),
    'saturn_volume'                 : RPNOperator( lambda: RPNMeasurement( '8.2713e23', 'meter^3' ),
                                                   0, [ ] ),

    'uranus_mass'                   : RPNOperator( lambda: RPNMeasurement( '8.6816e25', 'kilogram' ),
                                                   0, [ ] ),
    'uranus_radius'                 : RPNOperator( lambda: RPNMeasurement( '2.5559e7', 'meter' ),
                                                   0, [ ] ),
    'uranus_revolution'             : RPNOperator( lambda: RPNMeasurement( '84.011', 'year' ),
                                                   0, [ ] ),
    'uranus_volume'                 : RPNOperator( lambda: RPNMeasurement( '6.833e22', 'meter^3' ),
                                                   0, [ ] ),

    'neptune_mass'                  : RPNOperator( lambda: RPNMeasurement( '1.0242e26', 'kilogram' ),
                                                   0, [ ] ),
    'neptune_radius'                : RPNOperator( lambda: RPNMeasurement( '2.4764e7', 'meter' ),
                                                   0, [ ] ),
    'neptune_revolution'            : RPNOperator( lambda: RPNMeasurement( '164.79', 'year' ),
                                                   0, [ ] ),
    'neptune_volume'                : RPNOperator( lambda: RPNMeasurement( '6.254e22', 'meter^3' ),
                                                   0, [ ] ),

    'pluto_mass'                    : RPNOperator( lambda: RPNMeasurement( '1.0303e22', 'kilogram' ),
                                                   0, [ ] ),
    'pluto_radius'                  : RPNOperator( lambda: RPNMeasurement( '1.185e6', 'meter' ),
                                                   0, [ ] ),
    'pluto_revolution'              : RPNOperator( lambda: RPNMeasurement( '247.94', 'year' ),
                                                   0, [ ] ),
    'pluto_volume'                  : RPNOperator( lambda: RPNMeasurement( '6.97e18', 'meter^3' ),
                                                   0, [ ] ),

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
    '''This class represents a user-defined function in rpn.'''
    def __init__( self, valueList = None, startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        elif valueList:
            self.valueList.append( valueList )
        else:
            self.valueList = None

        self.startingIndex = startingIndex
        self.code = ''
        self.code_locals = { }
        self.compiled = None
        self.function = None
        self.argCount = 0

    def add( self, arg ):
        self.valueList.append( arg )

    def evaluate( self, x = 0, y = 0, z = 0 ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        if self.argCount == 0:
            return self.function( )
        elif self.argCount == 1:
            return self.function( x )
        elif self.argCount == 2:
            return self.function( x, y )
        elif self.argCount == 3:
            return self.function( x, y, z )

    def setCode( self, code ):
        if code.find( 'rpnInternalFunction( ):' ) != -1:
            self.argCount = 0
        elif code.find( 'rpnInternalFunction( x ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( z ):' ) != -1:
            self.argCount = 1
        elif code.find( 'rpnInternalFunction( x, y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( x, z ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y, z ):' ) != -1:
            self.argCount = 2
        else:
            self.argCount = 3

        self.code = code
        self.compile( )

    def getCode( self ):
        if not self.code:
            self.buildCode( )
            self.compile( )

        return self.code

    def getFunction( self ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        return self.function

    def buildCode( self ):
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

        emptyFunction = True

        args = [ ]
        listArgs = [ ]
        listDepth = 0

        debugPrint( 'terms', valueList )

        while valueList:
            term = valueList.pop( 0 )
            debugPrint( 'term:', term, 'args:', args )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            if term in ( 'x', 'y', 'z' ) and not valueList:
                self.code += term
                emptyFunction = False
            elif term in constants:
                function = constants[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( constants[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) - 1 ] + ' )'

                function += '( )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term == '[':
                listArgs.append( [ ] )
                listDepth += 1
            elif term == ']':
                arg = '[ '

                for listArg in listArgs[ listDepth - 1 ]:
                    if arg != '[ ':
                        arg += ', '

                    arg += listArg

                arg += ' ]'

                args.append( arg )

                del listArgs[ listDepth - 1 ]

                listDepth -= 1
            #elif term in specialFormatOperators:
            elif term in operators:
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

                if listDepth > 0:
                    if len( listArgs[ listDepth - 1 ] ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for i in range( 0, operands ):
                        argList.insert( 0, listArgs[ listDepth - 1 ].pop( ) )
                else:
                    if len( args ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for i in range( 0, operands ):
                        argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term in listOperators:
                function = listOperators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( listOperators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = listOperators[ term ].argCount

                if len( args ) < operands:
                    raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term[ 0 ] == '@' and term[ 1 : ] in g.userFunctions:
                function2 = g.userFunctions[ term[ 1 : ] ].getCode( )
                debugPrint( 'function:', function2 )

                function2 = function2.replace( 'def rpnInternalFunction(', '( lambda' )
                function2 = function2.replace( ' ): return', ':' )

                function2 += ' )( '

                first = True

                argList = [ ]

                operands = g.userFunctions[ term[ 1 : ] ].argCount

                if len( args ) < operands:
                    raise ValueError( '{0} expects {1} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function2 += ', '

                    function2 += arg

                function2 += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function2 )
                else:
                    args.append( function2 )

                if not valueList:
                    self.code += function2
                    emptyFunction = False
            elif term[ 0 ] == '$' and term[ 1 : ] in g.userVariables:
                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( g.userVariables[ term[ 1 : ] ] )
                else:
                    args.append( g.userVariables[ term[ 1 : ] ] )
            else:
                if term not in ( 'x', 'y', 'z' ):
                    term = str( parseInputValue( term, g.inputRadix ) )

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( term )
                else:
                    args.append( term )

        if emptyFunction:
            self.code += args[ 0 ]

        debugPrint( 'args:', args )
        debugPrint( 'valueList:', self.valueList[ self.startingIndex : ] )
        debugPrint( 'code:', self.code )

    def compile( self ):
        if not self.code:
            self.buildCode( )

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
# //  loadUserFunctionsFile
# //
# //******************************************************************************

def loadUserFunctionsFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserFunctionsFileName( ) )

    try:
        items = config.items( 'User Functions' )
    except:
        return

    for tuple in items:
        func = RPNFunction( )
        func.setCode( tuple[ 1 ] )
        g.userFunctions[ tuple[ 0 ] ] = func


# //******************************************************************************
# //
# //  saveUserFunctionsFile
# //
# //******************************************************************************

def saveUserFunctionsFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Functions' ] = { }

    for key in g.userFunctions.keys( ):
        config[ 'User Functions' ][ key ] = g.userFunctions[ key ].getCode( )

    import os.path

    if os.path.isfile( getUserFunctionsFileName( ) ):
        from shutil import copyfile
        copyfile( getUserFunctionsFileName( ), getUserFunctionsFileName( ) + '.backup' )

    with open( getUserFunctionsFileName( ), 'w' ) as userFunctionsFile:
        config.write( userFunctionsFile )


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
# //  evaluateRecurrence
# //
# //******************************************************************************

def evaluateRecurrence( start, count, func ):
    arg = start
    result = [ start ]

    for i in arange( count ):
        arg = func.evaluate( arg )
        result.append( arg )

    return result


# //******************************************************************************
# //
# //  repeatGenerator
# //
# //******************************************************************************

def repeatGenerator( n, func ):
    for i in arange( 0, n ):
        yield func.evaluate( )


# //******************************************************************************
# //
# //  repeatGenerator
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def repeat( n, func ):
    return RPNGenerator( repeatGenerator( n, func ) )


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

    for i in n:
        value = k.evaluate( i )

        if ( value != 0 ) != invert:
            yield i


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

    for index, item in enumerate( n ):
        value = k.evaluate( index )

        if ( value != 0 ) != invert:
            yield item


# //******************************************************************************
# //
# //  forEach
# //
# //******************************************************************************

def forEach( list, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each\' expects a function argument' )

    for i in list:
        yield func.evaluate( *i )


# //******************************************************************************
# //
# //  forEachList
# //
# //******************************************************************************

def forEachList( list, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each_list\' expects a function argument' )

    for i in list:
        yield func.evaluate( i )


# //******************************************************************************
# //
# //  breakOnCondition
# //
# //******************************************************************************

def breakOnCondition( n, k ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        raise ValueError( '\'break_on\' expects a function argument' )

    for i in n:
        value = k.evaluate( i )

        if value:
            return i


# //******************************************************************************
# //
# //  createRange
# //
# //  Used by 'lambda'.
# //
# //******************************************************************************

def createRange( start, end ):
    return arange( start, fadd( end, 1 ) )


# //******************************************************************************
# //
# //  createSizedRange
# //
# //  Used by 'lambda'.
# //
# //******************************************************************************

def createSizedRange( start, interval, size ):
    return arange( start, fadd( start, fmul( interval, size ) ), interval )


# //******************************************************************************
# //
# //  preprocessTerms
# //
# //******************************************************************************

def preprocessTerms( terms ):
    '''
    Given the initial list of arguments form the user, there are several
    things we want to do to the list before handing it off to the actual
    operator evaluator.  This logic used to be part of the evaluator, but
    that made the code a lot more complicated.  Hopefully, this will make
    the code simpler and easier to read.

    If this function returns an empty list, then rpn should abort.  This
    function should print out any error messages.
    '''
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

    if not g.interactive and term[ 1 : ] in g.userVariables:
        return g.userVariables[ term[ 1 : ] ]

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
        print( '   ' + i )

    print( )

    return len( operators ) + len( listOperators ) + len( modifiers )


# //******************************************************************************
# //
# //  dumpConstants
# //
# //******************************************************************************

def dumpConstants( ):
    for i in sorted( [ key for key in constants ] ):
        print( i )

    print( )

    return len( constants )


# //******************************************************************************
# //
# //  dumpUnits
# //
# //******************************************************************************

def dumpUnits( ):
    if not g.unitOperators:
        loadUnitData( )

    for i in sorted( [ key for key in g.unitOperators ] ):
        print( i )

    print( )

    return len( g.unitOperators )


# //******************************************************************************
# //
# //  callers
# //
# //******************************************************************************

callers = [
    lambda func, args: func( ),
    lambda func, arg: func( arg ),
    lambda func, arg1, arg2: func( arg1, arg2 ),

    # 3, 4, and 5 argument functions don't recurse with lists more than one level
    # I have some ideas about how to improve this.
    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for a in arg1 for b in arg2 for c in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for a in arg1 for b in arg2 for c in arg3 for d in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for a in arg1 for b in arg2 for c in arg3 for d in arg4 for e in arg5 ],
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

    printStats( 'small_primes', 'small primes' )
    printStats( 'large_primes', 'large primes' )
    printStats( 'huge_primes', 'huge primes' )
    printStats( 'isolated_primes', 'isolated primes' )
    printStats( 'twin_primes', 'twin primes' )
    printStats( 'balanced_primes', 'balanced primes' )
    printStats( 'double_balanced_primes', 'double balanced primes' )
    printStats( 'triple_balanced_primes', 'triple balanced primes' )
    printStats( 'sophie_primes', 'Sophie Germain primes' )
    printStats( 'cousin_primes', 'cousin primes' )
    printStats( 'sexy_primes', 'sexy primes' )
    printStats( 'triplet_primes', 'triplet primes' )
    printStats( 'sexy_triplets', 'sexy triplet primes' )
    printStats( 'quad_primes', 'quadruplet primes' )
    printStats( 'sexy_quadruplets', 'sexy quadruplet primes' )
    printStats( 'quint_primes', 'quintuplet primes' )
    printStats( 'sext_primes', 'sextuplet primes' )

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
    listDepth = 0

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
            # handle a plain old value (i.e., a number or list, not an operator)... or
            # a reference to a user-defined function
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

            # handle a user-defined function
            if isinstance( currentValueList[ -1 ], RPNFunction ):
                if currentValueList[ -1 ].argCount == 0:
                    if not operators[ 'eval0' ].evaluate( 'eval0', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 1:
                    if not operators[ 'eval' ].evaluate( 'eval', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 2:
                    if not operators[ 'eval2' ].evaluate( 'eval2', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 3:
                    if not operators[ 'eval3' ].evaluate( 'eval3', index, currentValueList ):
                        return False

                return True

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
# //  getUserVariable
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getUserVariable( key ):
    if key in g.userVariables:
        return g.userVariables[ key ]
    else:
        return ""


# //******************************************************************************
# //
# //  setUserVariable
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def setUserVariable( key, value ):
    g.userVariables[ key ] = value
    g.userVariablesAreDirty = True

    return value


# //******************************************************************************
# //
# //  getUserConfiguration
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getUserConfiguration( key ):
    if key in g.userConfiguration:
        return g.userConfiguration[ key ]
    else:
        return ""


# //******************************************************************************
# //
# //  setUserConfiguration
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def setUserConfiguration( key, value ):
    g.userConfiguration[ key ] = value
    g.userConfigurationIsDirty = True

    return value


# //******************************************************************************
# //
# //  deleteUserConfiguration
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def deleteUserConfiguration( key ):
    if key not in g.userConfiguration:
        raise ValueError( 'key \'' + key + '\' not found' )

    del g.userConfiguration[ key ]
    g.userConfigurationIsDirty = True

    return key


# //******************************************************************************
# //
# //  dumpUserConfiguration
# //
# //******************************************************************************

def dumpUserConfiguration( ):
    for i in g.userConfiguration:
        print( i + ':', '"' + g.userConfiguration[ i ] + '"' );

    print( )

    return len( g.userConfiguration )


# //******************************************************************************
# //
# //  createUserFunction
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def createUserFunction( key, func ):
    g.userFunctions[ key ] = func
    g.userFunctionsAreDirty = True

    return key


@oneArgFunctionEvaluator( )
def evaluateFunction0( func ):
    return func.evaluate( )

@twoArgFunctionEvaluator( )
def evaluateFunction( n, func ):
    return func.evaluate( n )

def evaluateFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )

@listAndOneArgFunctionEvaluator( )
def evaluateListFunction( n, func ):
    return func.evaluate( n )

def evaluateListFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateListFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )

@listAndOneArgFunctionEvaluator( )
def filterListOfLists( n, func ):
    return func.evaluate( n )

@twoArgFunctionEvaluator( )
def evaluateLimit( n, func ):
    return limit( lambda x: func.evaluate( x ), n )

@twoArgFunctionEvaluator( )
def evaluateReverseLimit( n, func ):
    return limit( lambda x: func.evaluate( x ), n, direction = -1 )

def evaluateProduct( start, end, func ):
    return nprod( lambda x: func.evaluate( x ), [ start, end ] )

def evaluateSum( start, end, func ):
    return nsum( lambda x: func.evaluate( x, func ), [ start, end ] )

def createExponentialRange( a, b, c ):
    return RPNGenerator.createExponential( a, b, c )

def createGeometricRange( a, b, c ):
    return RPNGenerator.createGeometric( a, b, c )

@twoArgFunctionEvaluator( )
def createRange( start, end ):
    return RPNGenerator.createRange( start, end )

def createIntervalRangeOperator( a, b, c ):
    return RPNGenerator.createRange( a, b, c )

def createSizedRangeOperator( a, b, c ):
    return RPNGenerator.createSizedRange( a, b, c )


# //******************************************************************************
# //
# //  specialFormatOperators
# //
# //******************************************************************************

specialFormatOperators = {
    'and'       : '( {0} and {1} )',
    'nand'      : '( not ( {0} and {1} ) )',
    'or'        : '( {0} or {1} )',
    'nor'       : '( not ( {0} or {1} ) )',
}


# //******************************************************************************
# //
# //  functionOperators
# //
# //  This is a list of operators that terminate the function creation state.
# //
# //******************************************************************************

functionOperators = [
    'break_on',
    'eval0',
    'eval',
    'eval2',
    'eval3',
    'eval_list',
    'eval_list2',
    'eval_list3',
    'filter',
    'filter_by_index',
    'for_each',
    'for_each_list',
    'function',
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plotc',
    'recurrence',
    'repeat',
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
    'duplicate_term'        : RPNOperator( duplicateTerm, 1 ),

    'duplicate_operator'    : RPNOperator( duplicateOperation, 1 ),

    'previous'              : RPNOperator( getPrevious, 0 ),

    'unlist'                : RPNOperator( unlist, 0 ),

    'lambda'                : RPNOperator( createFunction, 0 ),

    'x'                     : RPNOperator( addX, 0 ),

    'y'                     : RPNOperator( addY, 0 ),

    'z'                     : RPNOperator( addZ, 0 ),

    '['                     : RPNOperator( incrementNestedListLevel, 0 ),

    ']'                     : RPNOperator( decrementNestedListLevel, 0 ),

    '('                     : RPNOperator( startOperatorList, 0 ),

    ')'                     : RPNOperator( endOperatorList, 0 ),
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

    'discriminant'          : RPNOperator( getPolynomialDiscriminant,
                                           1, [ RPNOperator.List ] ),

    'eval_polynomial'       : RPNOperator( evaluatePolynomial,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'multiply_polynomials'  : RPNOperator( multiplyPolynomials,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'polynomial_power'      : RPNOperator( exponentiatePolynomial,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'polynomial_product'    : RPNOperator( multiplyListOfPolynomials,
                                           1, [ RPNOperator.List ] ),

    'polynomial_sum'        : RPNOperator( sumListOfPolynomials,
                                           1, [ RPNOperator.List ] ),

    'solve'                 : RPNOperator( solvePolynomial,
                                           1, [ RPNOperator.List ] ),

    # arithmetic
    'equals_one_of'         : RPNOperator( equalsOneOf,
                                           2, [ RPNOperator.Default, RPNOperator.List ],
                                           RPNOperator.measurementsAllowed ),

    'gcd'                   : RPNOperator( getGCDOfList,
                                           1, [ RPNOperator.List ] ),

    'geometric_mean'        : RPNOperator( calculateGeometricMean,
                                           1, [ RPNOperator.List ] ),

    'harmonic_mean'         : RPNOperator( calculateHarmonicMean,
                                           1, [ RPNOperator.List ] ),

    'lcm'                   : RPNOperator( getLCMOfList,
                                           1, [ RPNOperator.List ] ),

    'max'                   : RPNOperator( getMaximum,
                                           1, [ RPNOperator.List ] ),

    'mean'                  : RPNOperator( calculateArithmeticMean,
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
    'denomination_combinations' : RPNOperator( getDenominationCombinations,
                                               2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

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
    'break_on'              : RPNOperator( breakOnCondition,
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'filter'                : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'filter_list'           : RPNOperator( lambda n, k: RPNGenerator( filterListOfLists( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'filter_by_index'       : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'for_each'              : RPNOperator( lambda n, k: RPNGenerator( forEach( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'for_each_list'         : RPNOperator( lambda n, k: RPNGenerator( forEachList( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'unfilter'              : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k, True ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    'unfilter_by_index'     : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k, True ) ),
                                           2, [ RPNOperator.List, RPNOperator.Function ] ),

    # lexicographic
    'combine_digits'        : RPNOperator( combineDigits,
                                           1, [ RPNOperator.Generator ] ),

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

    'collate'               : RPNOperator( lambda n: RPNGenerator( collate( n ) ),
                                           1, [ RPNOperator.List ] ),

    'compare_lists'         : RPNOperator( compareLists,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'count'                 : RPNOperator( countElements,
                                           1, [ RPNOperator.Generator ] ),

    'cumulative_diffs'      : RPNOperator( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'cumulative_ratios'     : RPNOperator( lambda n: RPNGenerator( getCumulativeListRatios( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'difference'            : RPNOperator( getDifference,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'diffs'                 : RPNOperator( lambda n: RPNGenerator( getListDiffs( n ) ),
                                           1, [ RPNOperator.Generator ] ),

    'element'               : RPNOperator( getListElement,
                                           2, [ RPNOperator.List, RPNOperator.NonnegativeInteger ] ),

    'enumerate'             : RPNOperator( lambda n, k: RPNGenerator( enumerateList( n, k ) ),
                                           2, [ RPNOperator.List, RPNOperator.Integer ] ),

    'find'                  : RPNOperator( findInList,
                                           2, [ RPNOperator.List, RPNOperator.Default ] ),

    'flatten'               : RPNOperator( flatten,
                                           1, [ RPNOperator.List ] ),

    'get_combinations'      : RPNOperator( getListCombinations,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'get_repeat_combinations'   : RPNOperator( getListCombinationsWithRepeats,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'get_permutations'      : RPNOperator( getListPermutations,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'get_repeat_permutations'   : RPNOperator( getListPermutationsWithRepeats,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'group_elements'        : RPNOperator( groupElements,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'interleave'            : RPNOperator( interleave,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'intersection'          : RPNOperator( makeIntersection,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'is_palindrome_list'    : RPNOperator( isPalindromeList,
                                           1, [ RPNOperator.List ] ),

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

    'powerset'              : RPNOperator( lambda n: RPNGenerator( getPowerset( n ) ),
                                           1, [ RPNOperator.List ] ),

    'random_element'        : RPNOperator( getRandomElement,
                                           1, [ RPNOperator.List ] ),

    'ratios'                : RPNOperator( lambda n: RPNGenerator( getListRatios( n ) ),
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
    'base'                  : RPNOperator( interpretAsBaseOperator,
                                           2, [ RPNOperator.List, RPNOperator.PositiveInteger ] ),

    'cf'                    : RPNOperator( convertFromContinuedFraction,
                                           1, [ RPNOperator.List ] ),

    'crt'                   : RPNOperator( calculateChineseRemainderTheorem,
                                           2, [ RPNOperator.List, RPNOperator.List ] ),

    'frobenius'             : RPNOperator( getFrobeniusNumber,
                                           1, [ RPNOperator.List ] ),

    'geometric_recurrence'  : RPNOperator( lambda a, b, c, d: RPNGenerator( getGeometricRecurrence( a, b, c, d ) ),
                                           4, [ RPNOperator.List, RPNOperator.List, RPNOperator.List,
                                                RPNOperator.PositiveInteger ] ),

    'is_friendly'           : RPNOperator( isFriendly,
                                           1, [ RPNOperator.List ] ),

    'linear_recurrence'     : RPNOperator( lambda a, b, c: RPNGenerator( getLinearRecurrence( a, b, c ) ),
                                           3, [ RPNOperator.List, RPNOperator.List,
                                                RPNOperator.PositiveInteger ] ),

    'linear_recurrence_with_modulo' : RPNOperator( lambda a, b, c, d: RPNGenerator( getLinearRecurrenceWithModulo( a, b, c, d ) ),
                                           4, [ RPNOperator.List, RPNOperator.List,
                                                RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    # powers_and_roots
    'power_tower'           : RPNOperator( calculatePowerTower,
                                           1, [ RPNOperator.List ] ),

    'power_tower2'          : RPNOperator( calculatePowerTower2,
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

    'decrement'                      : RPNOperator( decrement,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'divide'                         : RPNOperator( divide,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'floor'                          : RPNOperator( getFloor,
                                                    1, [ RPNOperator.Default ] ),

    'gcd2'                           : RPNOperator( getGCD,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'increment'                      : RPNOperator( increment,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'is_divisible'                   : RPNOperator( isDivisible,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_equal'                       : RPNOperator( isEqual,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'is_even'                        : RPNOperator( isEven,
                                                    1, [ RPNOperator.Real ] ),

    'is_greater'                     : RPNOperator( isGreater,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_integer'                     : RPNOperator( isInteger,
                                                    1, [ RPNOperator.Real ] ),

    'is_kth_power'                   : RPNOperator( isKthPower,
                                                    2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'is_less'                        : RPNOperator( isLess,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_equal'                   : RPNOperator( isNotEqual,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ],
                                                    RPNOperator.measurementsAllowed ),

    'is_not_greater'                 : RPNOperator( isNotGreater,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_less'                    : RPNOperator( isNotLess,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'is_not_zero'                    : RPNOperator( isNotZero,
                                                    1, [ RPNOperator.Default ] ),

    'is_odd'                         : RPNOperator( isOdd,
                                                    1, [ RPNOperator.Real ] ),

    'is_power_of_k'                  : RPNOperator( isPower,
                                                    2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'is_square'                      : RPNOperator( isSquare,
                                                    1, [ RPNOperator.Integer ] ),

    'is_zero'                        : RPNOperator( isZero,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'larger'                         : RPNOperator( getLarger,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'lcm2'                           : RPNOperator( getLCM,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'mantissa'                       : RPNOperator( getMantissa,
                                                    1, [ RPNOperator.Default ] ),

    'modulo'                         : RPNOperator( getModulo,
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

    'round_by_digits'                : RPNOperator( roundByDigits,
                                                    2, [ RPNOperator.Real, RPNOperator.Integer ],
                                                    RPNOperator.measurementsAllowed ),

    'round_by_value'                 : RPNOperator( roundByValue,
                                                    2, [ RPNOperator.Real, RPNOperator.NonnegativeReal ],
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
    'angular_separation'             : RPNOperator( getAngularSeparation,
                                                    4, [ RPNOperator.AstronomicalObject, RPNOperator.AstronomicalObject,
                                                         RPNOperator.Location, RPNOperator.DateTime ] ),

    'angular_size'                   : RPNOperator( getAngularSize,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'antitransit_time'               : RPNOperator( getAntitransitTime,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'astronomical_dawn'              : RPNOperator( getNextAstronomicalDawn,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'astronomical_dusk'              : RPNOperator( getNextAstronomicalDusk,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'autumnal_equinox'               : RPNOperator( getAutumnalEquinox,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'dawn'                           : RPNOperator( getNextCivilDawn,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'day_time'                       : RPNOperator( getDayTime,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'distance_from_earth'            : RPNOperator( getDistanceFromEarth,
                                                    2, [ RPNOperator.AstronomicalObject, RPNOperator.DateTime ] ),

    'dusk'                           : RPNOperator( getNextCivilDusk,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'eclipse_totality'               : RPNOperator( getEclipseTotality,
                                                    4, [ RPNOperator.AstronomicalObject, RPNOperator.AstronomicalObject,
                                                         RPNOperator.Location, RPNOperator.DateTime ] ),

    'moonrise'                       : RPNOperator( getNextMoonRise,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moonset'                        : RPNOperator( getNextMoonSet,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moon_antitransit'               : RPNOperator( getNextMoonAntitransit,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'moon_phase'                     : RPNOperator( getMoonPhase,
                                                    1, [ RPNOperator.DateTime ] ),

    'moon_transit'                   : RPNOperator( getNextMoonTransit,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'nautical_dawn'                  : RPNOperator( getNextNauticalDawn,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'nautical_dusk'                  : RPNOperator( getNextNauticalDusk,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'next_antitransit'               : RPNOperator( getNextAntitransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'next_first_quarter_moon'        : RPNOperator( getNextFirstQuarterMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'next_full_moon'                 : RPNOperator( getNextFullMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'next_last_quarter_moon'         : RPNOperator( getNextLastQuarterMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'next_new_moon'                  : RPNOperator( getNextNewMoon,
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

    'night_time'                     : RPNOperator( getNightTime,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'previous_antitransit'           : RPNOperator( getPreviousAntitransit,
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'previous_first_quarter_moon'    : RPNOperator( getPreviousFirstQuarterMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_full_moon'             : RPNOperator( getPreviousFullMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_last_quarter_moon'     : RPNOperator( getPreviousLastQuarterMoon,
                                                    1, [ RPNOperator.DateTime ] ),

    'previous_new_moon'              : RPNOperator( getPreviousNewMoon,
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
                                                    3, [ RPNOperator.AstronomicalObject, RPNOperator.Location,
                                                         RPNOperator.DateTime ] ),

    'solar_noon'                     : RPNOperator( getSolarNoon,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'summer_solstice'                : RPNOperator( getSummerSolstice,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sunrise'                        : RPNOperator( getNextSunrise,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'sunset'                         : RPNOperator( getNextSunset,
                                                    2, [ RPNOperator.Location, RPNOperator.DateTime ] ),

    'sun_antitransit'                : RPNOperator( getNextSunAntitransit,
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
    'bitwise_and'                    : RPNOperator( getBitwiseAnd,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'bitwise_nand'                   : RPNOperator( getBitwiseNand,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'bitwise_nor'                    : RPNOperator( getBitwiseNor,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'bitwise_not'                    : RPNOperator( getInvertedBits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'bitwise_or'                     : RPNOperator( getBitwiseOr,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'bitwise_xor'                    : RPNOperator( getBitwiseXor,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'count_bits'                     : RPNOperator( getBitCountOperator,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'parity'                         : RPNOperator( getParity,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'shift_left'                     : RPNOperator( shiftLeft,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'shift_right'                    : RPNOperator( shiftRight,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    # calendar
    'ascension'                      : RPNOperator( calculateAscensionThursday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'ash_wednesday'                  : RPNOperator( calculateAshWednesday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'calendar'                       : RPNOperator( generateMonthCalendar,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'christmas'                      : RPNOperator( getChristmasDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'columbus_day'                   : RPNOperator( calculateColumbusDay,
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

    'fathers_day'                    : RPNOperator( calculateFathersDay,
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

    'good_friday'                    : RPNOperator( calculateGoodFriday,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'independence_day'               : RPNOperator( getIndependenceDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'iso_date'                       : RPNOperator( getISODate,
                                                    1, [ RPNOperator.DateTime ] ),

    'labor_day'                      : RPNOperator( calculateLaborDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'martin_luther_king_day'         : RPNOperator( calculateMartinLutherKingDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'memorial_day'                   : RPNOperator( calculateMemorialDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'mothers_day'                    : RPNOperator( calculateMothersDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'new_years_day'                  : RPNOperator( getNewYearsDay,
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

    'veterans_day'                   : RPNOperator( getVeteransDay,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'weekday'                        : RPNOperator( getWeekday,
                                                    1, [ RPNOperator.DateTime ] ),

    'weekday_name'                   : RPNOperator( getWeekdayName,
                                                    1, [ RPNOperator.DateTime ] ),

    'year_calendar'                  : RPNOperator( generateYearCalendar,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # chemistry
    'atomic_number'                  : RPNOperator( getAtomicNumber,
                                                    1, [ RPNOperator.String ] ),

    'atomic_symbol'                  : RPNOperator( getAtomicSymbol,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'atomic_weight'                  : RPNOperator( getAtomicWeight,
                                                    1, [ RPNOperator.String ] ),

    'element_block'                  : RPNOperator( getElementBlock,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_boiling_point'          : RPNOperator( getElementBoilingPoint,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_density'                : RPNOperator( getElementDensity,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_description'            : RPNOperator( getElementDescription,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_group'                  : RPNOperator( getElementGroup,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_melting_point'          : RPNOperator( getElementMeltingPoint,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_name'                   : RPNOperator( getElementName,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_occurrence'             : RPNOperator( getElementOccurrence,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_period'                 : RPNOperator( getElementPeriod,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'element_state'                  : RPNOperator( getElementState,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'molar_mass'                     : RPNOperator( getMolarMass,
                                                    1, [ RPNOperator.String ] ),

    # combinatoric
    'arrangements'                   : RPNOperator( getArrangements,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'bell_polynomial'                : RPNOperator( getBellPolynomial,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'binomial'                       : RPNOperator( getBinomial,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'combinations'                   : RPNOperator( getCombinations,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'compositions'                   : RPNOperator( getCompositions,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'debruijn'                       : RPNOperator( getDeBruijnSequence,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'lah'                            : RPNOperator( getLahNumber,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'nth_menage'                     : RPNOperator( getNthMenageNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'multifactorial'                 : RPNOperator( getNthMultifactorial,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'narayana'                       : RPNOperator( getNarayanaNumber,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'nth_apery'                      : RPNOperator( getNthAperyNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_bell'                       : RPNOperator( getNthBell,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_bernoulli'                  : RPNOperator( getNthBernoulli,
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

    'nth_sylvester'                  : RPNOperator( getNthSylvesterNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'partitions'                     : RPNOperator( getPartitionNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'permutations'                   : RPNOperator( getPermutations,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    # complex
    'argument'                       : RPNOperator( getArgument,
                                                    1, [ RPNOperator.Default ] ),

    'conjugate'                      : RPNOperator( getConjugate,
                                                    1, [ RPNOperator.Default ] ),

    'i'                              : RPNOperator( getI,
                                                    1, [ RPNOperator.Real ] ),

    'imaginary'                      : RPNOperator( getImaginary,
                                                    1, [ RPNOperator.Default ] ),

    'real'                           : RPNOperator( getReal,
                                                    1, [ RPNOperator.Default ] ),

    # conversion
    'char'                           : RPNOperator( convertToChar,
                                                    1, [ RPNOperator.Integer ] ),

    'dhms'                           : RPNOperator( convertToDHMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'dms'                            : RPNOperator( convertToDMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'double'                         : RPNOperator( convertToDouble,
                                                    1, [ RPNOperator.Real ] ),

    'float'                          : RPNOperator( convertToFloat,
                                                    1, [ RPNOperator.Real ] ),

    'from_unix_time'                 : RPNOperator( convertFromUnixTime,
                                                    1, [ RPNOperator.Integer ] ),

    'hms'                            : RPNOperator( convertToHMS,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'integer'                        : RPNOperator( convertToSignedIntOperator,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'invert_units'                   : RPNOperator( invertUnits,
                                                    1, [ RPNOperator.Measurement ],
                                                    RPNOperator.measurementsAllowed ),

    'long'                           : RPNOperator( convertToLong,
                                                    1, [ RPNOperator.Integer ] ),

    'longlong'                       : RPNOperator( convertToLongLong,
                                                    1, [ RPNOperator.Integer ] ),

    # pack ???

    'short'                          : RPNOperator( convertToShort,
                                                    1, [ RPNOperator.Integer ] ),

    'to_unix_time'                   : RPNOperator( convertToUnixTime,
                                                    1, [ RPNOperator.DateTime ] ),

    'uchar'                          : RPNOperator( convertToUnsignedChar,
                                                    1, [ RPNOperator.Integer ] ),

    'uinteger'                       : RPNOperator( convertToUnsignedInt,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'ulong'                          : RPNOperator( convertToUnsignedLong,
                                                    1, [ RPNOperator.Integer ] ),

    'ulonglong'                      : RPNOperator( convertToUnsignedLongLong,
                                                    1, [ RPNOperator.Integer ] ),

    'undouble'                       : RPNOperator( interpretAsDouble,
                                                    1, [ RPNOperator.Integer ] ),

    'unfloat'                        : RPNOperator( interpretAsFloat,
                                                    1, [ RPNOperator.Integer ] ),

    # unpack ???

    'ushort'                         : RPNOperator( convertToUnsignedShort,
                                                    1, [ RPNOperator.Integer ] ),

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

    # figurate
    'centered_cube'                  : RPNOperator( getNthCenteredCubeNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_decagonal'             : RPNOperator( getNthCenteredDecagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_dodecahedral'          : RPNOperator( getNthCenteredDodecahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_heptagonal'            : RPNOperator( getNthCenteredHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_hexagonal'             : RPNOperator( getNthCenteredHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_icosahedral'           : RPNOperator( getNthCenteredIcosahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_nonagonal'             : RPNOperator( getNthCenteredNonagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_octagonal'             : RPNOperator( getNthCenteredOctagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_octahedral'            : RPNOperator( getNthCenteredOctahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_pentagonal'            : RPNOperator( getNthCenteredPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_polygonal'             : RPNOperator( getNthCenteredPolygonalNumberOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'centered_square'                : RPNOperator( getNthCenteredSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_tetrahedral'           : RPNOperator( getNthCenteredTetrahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'centered_triangular'            : RPNOperator( getNthCenteredTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'decagonal'                      : RPNOperator( getNthDecagonalNumber,
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

    'dodecahedral'                   : RPNOperator( getNthDodecahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'generalized_pentagonal'         : RPNOperator( getNthGeneralizedPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal'                     : RPNOperator( getNthHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_hexagonal'           : RPNOperator( getNthHeptagonalHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_pentagonal'          : RPNOperator( getNthHeptagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_square'              : RPNOperator( getNthHeptagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'heptagonal_triangular'          : RPNOperator( getNthHeptagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal'                      : RPNOperator( getNthHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal_pentagonal'           : RPNOperator( getNthHexagonalPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexagonal_square'               : RPNOperator( getNthHexagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'icosahedral'                    : RPNOperator( getNthIcosahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nonagonal'                      : RPNOperator( getNthNonagonalNumber,
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

    'nth_centered_decagonal'         : RPNOperator( findCenteredDecagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_heptagonal'        : RPNOperator( findCenteredHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_hexagonal'         : RPNOperator( findCenteredHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_nonagonal'         : RPNOperator( findCenteredNonagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_octagonal'         : RPNOperator( findCenteredOctagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_pentagonal'        : RPNOperator( findCenteredPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_polygonal'         : RPNOperator( findCenteredPolygonalNumberOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'nth_centered_square'            : RPNOperator( findCenteredSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_centered_triangular'        : RPNOperator( findCenteredTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_decagonal'                  : RPNOperator( findDecagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_heptagonal'                 : RPNOperator( findHeptagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_hexagonal'                  : RPNOperator( findHexagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_nonagonal'                  : RPNOperator( findNonagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_octagonal'                  : RPNOperator( findOctagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_pentagonal'                 : RPNOperator( findPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_polygonal'                  : RPNOperator( findPolygonalNumberOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'nth_square'                     : RPNOperator( findSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_triangular'                 : RPNOperator( findTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octagonal'                      : RPNOperator( getNthOctagonalNumber,
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

    'octahedral'                     : RPNOperator( getNthOctahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal'                     : RPNOperator( getNthPentagonalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal_square'              : RPNOperator( getNthPentagonalSquareNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentagonal_triangular'          : RPNOperator( getNthPentagonalTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentatope'                      : RPNOperator( getNthPentatopeNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polygonal'                      : RPNOperator( getNthPolygonalNumberOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'polytope'                       : RPNOperator( getNthPolytopeNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'pyramid'                        : RPNOperator( getNthPyramidalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'rhombic_dodecahedral'           : RPNOperator( getNthRhombicDodecahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'square_triangular'              : RPNOperator( getNthSquareTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'star'                           : RPNOperator( getNthStarNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'stella_octangula'               : RPNOperator( getNthStellaOctangulaNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'tetrahedral'                    : RPNOperator( getNthTetrahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'triangular'                     : RPNOperator( getNthTriangularNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'truncated_octahedral'           : RPNOperator( getNthTruncatedOctahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'truncated_tetrahedral'          : RPNOperator( getNthTruncatedTetrahedralNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    # function
    'eval0'                           : RPNOperator( evaluateFunction0,
                                                    1, [ RPNOperator.Function ] ),

    'eval'                           : RPNOperator( evaluateFunction,
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'eval2'                          : RPNOperator( evaluateFunction2,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'eval3'                          : RPNOperator( evaluateFunction3,
                                                    4, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Function ] ),

    'eval_list'                      : RPNOperator( evaluateListFunction,
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'eval_list2'                     : RPNOperator( evaluateListFunction2,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'eval_list3'                     : RPNOperator( evaluateListFunction3,
                                                    4, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Function ] ),

    'function'                       : RPNOperator( createUserFunction,
                                                    2, [ RPNOperator.String, RPNOperator.Function ] ),

    'limit'                          : RPNOperator( evaluateLimit,
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'limitn'                         : RPNOperator( evaluateReverseLimit,
                                                    2, [ RPNOperator.Default, RPNOperator.Function ] ),

    'nprod'                          : RPNOperator( evaluateProduct,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'nsum'                           : RPNOperator( evaluateSum,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'plot'                           : RPNOperator( plotFunction,
                                                    3, [ RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Function ] ),

    'plot2'                          : RPNOperator( plot2DFunction,
                                                    5, [ RPNOperator.Default, RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Function ] ),

    'plotc'                          : RPNOperator( plotComplexFunction,
                                                    5, [ RPNOperator.Default, RPNOperator.Default, RPNOperator.Default,
                                                         RPNOperator.Default, RPNOperator.Function ] ),

    'recurrence'                     : RPNOperator( evaluateRecurrence,
                                                    3, [ RPNOperator.Default, RPNOperator.PositiveInteger, RPNOperator.Function ] ),

    'repeat'                        : RPNOperator( repeat,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.Function ] ),

    # geography
    'distance'                       : RPNOperator( getDistance,
                                                    2, [ RPNOperator.Location, RPNOperator.Location ] ),

    'get_timezone'                   : RPNOperator( getTimeZone,
                                                    1, [ RPNOperator.Location ] ),

    'lat_long'                       : RPNOperator( lambda n, k: RPNLocation( n, k ),
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

    'hypotenuse'                     : RPNOperator( calculateHypotenuse,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'icosahedron_area'               : RPNOperator( getIcosahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'icosahedron_volume'             : RPNOperator( getIcosahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'n_sphere_area'                  : RPNOperator( getNSphereSurfaceAreaOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                         RPNOperator.measurementsAllowed ),

    'n_sphere_radius'                : RPNOperator( getNSphereRadiusOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                             RPNOperator.measurementsAllowed ),

    'n_sphere_volume'                : RPNOperator( getNSphereVolumeOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal ],
                                                         RPNOperator.measurementsAllowed ),

    'octahedron_area'                : RPNOperator( getOctahedronSurfaceArea,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'octahedron_volume'              : RPNOperator( getOctahedronVolume,
                                                    1, [ RPNOperator.NonnegativeReal ] ),

    'polygon_area'                   : RPNOperator( getRegularPolygonAreaOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.Measurement ] ),

    'prism_area'                     : RPNOperator( getPrismSurfaceArea,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal,
                                                         RPNOperator.NonnegativeReal ] ),

    'prism_volume'                   : RPNOperator( getPrismVolume,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.NonnegativeReal,
                                                         RPNOperator.NonnegativeReal ] ),

    'sphere_area'                    : RPNOperator( getSphereArea,
                                                    1, [ RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_radius'                  : RPNOperator( getSphereRadius,
                                                    1, [ RPNOperator.NonnegativeReal ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_volume'                  : RPNOperator( getSphereVolume,
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

    'build_step_numbers'             : RPNOperator( buildStepNumbers,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'count_different_digits'         : RPNOperator( countDifferentDigits,
                                                    1, [ RPNOperator.Integer ] ),

    'count_digits'                   : RPNOperator( countDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'cyclic_permutations'            : RPNOperator( getCyclicPermutations,
                                                    1, [ RPNOperator.Integer ] ),

    'digits'                         : RPNOperator( getDigitCount,
                                                    1, [ RPNOperator.Integer ] ),

    'duplicate_digits'               : RPNOperator( duplicateDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'duplicate_number'               : RPNOperator( duplicateNumber,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'erdos_persistence'              : RPNOperator( getErdosPersistence,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'find_palindrome'                : RPNOperator( findPalindrome,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'get_base_k_digits'              : RPNOperator( getBaseKDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'get_digits'                     : RPNOperator( getDigits,
                                                    1, [ RPNOperator.Integer ] ),

    'get_left_digits'                : RPNOperator( getLeftDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'get_left_truncations'           : RPNOperator( getLeftTruncationsGenerator,
                                                    1, [ RPNOperator.Integer ] ),

    'get_nonzero_base_k_digits'      : RPNOperator( getNonzeroBaseKDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'get_nonzero_digits'             : RPNOperator( getNonzeroDigits,
                                                    1, [ RPNOperator.Integer ] ),

    'get_right_digits'                : RPNOperator( getRightDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger ] ),

    'get_right_truncations'          : RPNOperator( getRightTruncationsGenerator,
                                                    1, [ RPNOperator.Integer ] ),

    'has_any_digits'                 : RPNOperator( containsAnyDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'has_digits'                     : RPNOperator( containsDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'has_only_digits'                : RPNOperator( containsOnlyDigits,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'is_automorphic'                 : RPNOperator( isAutomorphic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_base_k_pandigital'           : RPNOperator( isBaseKPandigital,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_base_k_smith_number'         : RPNOperator( isBaseKSmithNumber,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_bouncy'                      : RPNOperator( isBouncy,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_decreasing'                  : RPNOperator( isDecreasing,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_digital_permutation'         : RPNOperator( isDigitalPermutation,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_generalized_dudeney'         : RPNOperator( isGeneralizedDudeneyNumber,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_harshad'                     : RPNOperator( isHarshadNumber,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_increasing'                  : RPNOperator( isIncreasing,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_kaprekar'                    : RPNOperator( isKaprekar,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_k_morphic'                   : RPNOperator( isKMorphicOperator,
                                                    2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'is_k_narcissistic'              : RPNOperator( isBaseKNarcissistic,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_narcissistic'                : RPNOperator( isNarcissistic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_order_k_smith_number'        : RPNOperator( isOrderKSmithNumber,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_palindrome'                  : RPNOperator( isPalindrome,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_pandigital'                  : RPNOperator( isPandigital,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_pddi'                        : RPNOperator( isPerfectDigitToDigitInvariant,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_pdi'                         : RPNOperator( isPerfectDigitalInvariant,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_smith_number'                : RPNOperator( isSmithNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_step_number'                 : RPNOperator( isStepNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_sum_product'                 : RPNOperator( isSumProductNumber,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_trimorphic'                  : RPNOperator( isTrimorphic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'k_persistence'                  : RPNOperator( getKPersistence,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'multiply_digits'                : RPNOperator( multiplyDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'multiply_digit_powers'          : RPNOperator( multiplyDigitPowers,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'multiply_nonzero_digits'        : RPNOperator( multiplyNonzeroDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'multiply_nonzero_digit_powers'  : RPNOperator( multiplyNonzeroDigitPowers,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'permute_digits'                 : RPNOperator( permuteDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'persistence'                    : RPNOperator( getPersistence,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'replace_digits'                 : RPNOperator( replaceDigits,
                                                    3, [ RPNOperator.Integer, RPNOperator.NonnegativeInteger,
                                                         RPNOperator.NonnegativeInteger ] ),

    'reverse_digits'                 : RPNOperator( reverseDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'rotate_digits_left'             : RPNOperator( rotateDigitsLeft,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.Integer ] ),

    'rotate_digits_right'            : RPNOperator( rotateDigitsRight,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.Integer ] ),

    'show_erdos_persistence'         : RPNOperator( showErdosPersistence,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'show_k_persistence'             : RPNOperator( showKPersistence,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'show_persistence'               : RPNOperator( showPersistence,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'square_digit_chain'             : RPNOperator( generateSquareDigitChain,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'sum_digits'                     : RPNOperator( sumDigits,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    # list
    'exponential_range'              : RPNOperator( createExponentialRange,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.PositiveInteger ] ),

    'geometric_range'                : RPNOperator( createGeometricRange,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.PositiveInteger ] ),

    'interval_range'                 : RPNOperator( createIntervalRangeOperator,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.Real ] ),

    'range'                          : RPNOperator( createRange,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'sized_range'                    : RPNOperator( createSizedRangeOperator,
                                                    3, [ RPNOperator.Real, RPNOperator.Real,
                                                         RPNOperator.Real ] ),

    # logarithms
    'lambertw'                       : RPNOperator( getLambertW,
                                                    1, [ RPNOperator.Default ] ),

    'li'                             : RPNOperator( getLI,
                                                    1, [ RPNOperator.Default ] ),

    'log'                            : RPNOperator( getLog,
                                                    1, [ RPNOperator.Default ] ),

    'log10'                          : RPNOperator( getLog10,
                                                    1, [ RPNOperator.Default ] ),

    'log2'                           : RPNOperator( getLog2,
                                                    1, [ RPNOperator.Default ] ),

    'logxy'                          : RPNOperator( getLogXY,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'polyexp'                        : RPNOperator( getPolyexp,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'polylog'                        : RPNOperator( getPolylog,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    # logical
    'and'                            : RPNOperator( andOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'nand'                           : RPNOperator( nandOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'nor'                            : RPNOperator( norOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'not'                            : RPNOperator( notOperand,
                                                    1, [ RPNOperator.Integer ] ),

    'or'                             : RPNOperator( orOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'xnor'                           : RPNOperator( xnorOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'xor'                            : RPNOperator( xorOperands,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    # number_theory
    'abundance'                      : RPNOperator( getAbundance,
                                                    1, RPNOperator.PositiveInteger ),

    'abundance_ratio'                : RPNOperator( getAbundanceRatio,
                                                    1, RPNOperator.PositiveInteger ),

    'aliquot'                        : RPNOperator( getAliquotSequence,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'alternating_factorial'          : RPNOperator( getNthAlternatingFactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'barnesg'                        : RPNOperator( getBarnesG,
                                                    1, [ RPNOperator.Default ] ),

    'beta'                           : RPNOperator( getBeta,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'calkin_wilf'                    : RPNOperator( getNthCalkinWilf,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'collatz'                        : RPNOperator( getCollatzSequence,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'count_divisors'                 : RPNOperator( getDivisorCount,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'cyclotomic'                     : RPNOperator( getCyclotomic,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.Default ] ),

    'digamma'                        : RPNOperator( getDigamma,
                                                    1, [ RPNOperator.Default ] ),

    'digital_root'                   : RPNOperator( getDigitalRoot,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'divisors'                       : RPNOperator( getDivisors,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'double_factorial'               : RPNOperator( getNthDoubleFactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'egypt'                          : RPNOperator( getGreedyEgyptianFraction,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'eta'                            : RPNOperator( getAltZeta,
                                                    1, [ RPNOperator.Default ] ),

    'euler_brick'                    : RPNOperator( makeEulerBrick,
                                                    3, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger,
                                                    RPNOperator.PositiveInteger ] ),

    'euler_phi'                      : RPNOperator( getEulerPhi,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'factor'                         : RPNOperator( getFactors,
                                                    1, [ RPNOperator.Integer ] ),

    'factorial'                      : RPNOperator( getNthFactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'fibonacci'                      : RPNOperator( getNthFibonacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'fibonorial'                     : RPNOperator( getNthFibonorial,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'find_sum_of_cubes'              : RPNOperator( findNthSumOfCubes,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'find_sum_of_squares'            : RPNOperator( findNthSumOfSquares,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'fraction'                       : RPNOperator( interpretAsFraction,
                                                    2, [ RPNOperator.Integer, RPNOperator.Integer ] ),

    'gamma'                          : RPNOperator( getGamma,
                                                    1, [ RPNOperator.Default ] ),

    'generate_polydivisibles'        : RPNOperator( generatePolydivisibles,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'get_base_k_digits'              : RPNOperator( getBaseKDigits,
                                           2, [ RPNOperator.Integer, RPNOperator.PositiveInteger ] ),

    'harmonic'                       : RPNOperator( getHarmonic,
                                                    1, [ RPNOperator.Default ] ),

    'heptanacci'                     : RPNOperator( getNthHeptanacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hexanacci'                      : RPNOperator( getNthHexanacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'hurwitz_zeta'                   : RPNOperator( getHurwitzZeta,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'hyperfactorial'                 : RPNOperator( getNthHyperfactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_abundant'                    : RPNOperator( isAbundant,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_achilles'                    : RPNOperator( isAchillesNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_carmichael'                  : RPNOperator( isCarmichaelNumberOperator,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_composite'                   : RPNOperator( isComposite,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_deficient'                   : RPNOperator( isDeficient,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    # is_friendly

    'is_k_hyperperfect'              : RPNOperator( isKHyperperfect,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'is_k_semiprime'                 : RPNOperator( isKSemiPrimeOperator,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_k_sphenic'                   : RPNOperator( isKSphenicOperator,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'is_perfect'                     : RPNOperator( isPerfect,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_polydivisible'               : RPNOperator( isPolydivisible,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_powerful'                    : RPNOperator( isPowerful,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_prime'                       : RPNOperator( isPrime,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_pronic'                      : RPNOperator( isPronic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_rough'                       : RPNOperator( isRoughOperator,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PrimeInteger ] ),

    'is_ruth_aaron'                  : RPNOperator( isRuthAaronNumber,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_semiprime'                   : RPNOperator( isSemiPrime,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_smooth'                      : RPNOperator( isSmoothOperator,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PrimeInteger ] ),

    'is_sphenic'                     : RPNOperator( isSphenic,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_squarefree'                  : RPNOperator( isSquareFree,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'is_strong_pseudoprime'          : RPNOperator( isStrongPseudoprime,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.NonnegativeInteger ] ),

    'is_unusual'                     : RPNOperator( isUnusual,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'k_fibonacci'                    : RPNOperator( getNthKFibonacciNumber,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'leyland'                        : RPNOperator( getLeyland,
                                                    2, [ RPNOperator.Real, RPNOperator.Real ] ),

    'log_gamma'                      : RPNOperator( getLogGamma,
                                                    1, [ RPNOperator.Default ] ),

    'lucas'                          : RPNOperator( getNthLucasNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'make_cf'                        : RPNOperator( makeContinuedFraction,
                                                    2, [ RPNOperator.Real, RPNOperator.PositiveInteger ] ),

    'make_pyth_3'                    : RPNOperator( makePythagoreanTriple,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'make_pyth_4'                    : RPNOperator( makePythagoreanQuadruple,
                                                    2, [ RPNOperator.NonnegativeReal, RPNOperator.NonnegativeReal ] ),

    'merten'                         : RPNOperator( getNthMerten,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'mobius'                         : RPNOperator( getMobius,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_carol'                      : RPNOperator( getNthCarolNumber,
                                                    1, [ RPNOperator.Real ] ),

    'nth_jacobsthal'                 : RPNOperator( getNthJacobsthalNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_kynea'                      : RPNOperator( getNthKyneaNumber,
                                                    1, [ RPNOperator.Real ] ),

    'nth_leonardo'                   : RPNOperator( getNthLeonardoNumber,
                                                    1, [ RPNOperator.Real ] ),

    'nth_mersenne_exponent'          : RPNOperator( getNthMersenneExponent,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_mersenne_prime'             : RPNOperator( getNthMersennePrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_padovan'                    : RPNOperator( getNthPadovanNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_perfect_number'             : RPNOperator( getNthPerfectNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_stern'                      : RPNOperator( getNthStern,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_thue_morse'                 : RPNOperator( getNthThueMorse,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'octanacci'                      : RPNOperator( getNthOctanacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pascal_triangle'                : RPNOperator( getNthPascalLine,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'pentanacci'                     : RPNOperator( getNthPentanacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polygamma'                      : RPNOperator( getPolygamma,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.Default ] ),

    'radical'                        : RPNOperator( getRadical,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'repunit'                        : RPNOperator( getNthBaseKRepunit,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'reversal_addition'              : RPNOperator( getNthReversalAddition,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'riesel'                         : RPNOperator( getNthRieselNumber,
                                                    1, [ RPNOperator.Real ] ),

    'sigma'                          : RPNOperator( getSigmaOperator,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'sigma_k'                        : RPNOperator( getSigmaK,
                                                    2, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger ] ),

    'subfactorial'                   : RPNOperator( getNthSubfactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'sums_of_k_powers'               : RPNOperator( findSumsOfKPowers,
                                                    3, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'sums_of_k_nonzero_powers'       : RPNOperator( findSumsOfKNonzeroPowers,
                                                    3, [ RPNOperator.NonnegativeInteger, RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'superfactorial'                 : RPNOperator( getNthSuperfactorial,
                                                    1, [ RPNOperator.NonnegativeInteger ] ),

    'tetranacci'                     : RPNOperator( getNthTetranacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'thabit'                         : RPNOperator( getNthThabitNumber,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'tribonacci'                     : RPNOperator( getNthTribonacci,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'trigamma'                       : RPNOperator( getTrigamma,
                                                    1, [ RPNOperator.Default ] ),

    'unit_roots'                     : RPNOperator( getUnitRoots,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'zeta'                           : RPNOperator( getZeta,
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

    # powers_and_roots
    'agm'                            : RPNOperator( getAGM,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ] ),

    'cube'                           : RPNOperator( cube,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cube_root'                      : RPNOperator( getCubeRoot,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'exp'                            : RPNOperator( getExp,
                                                    1, [ RPNOperator.Default ] ),

    'exp10'                          : RPNOperator( getExp10,
                                                    1, [ RPNOperator.Default ] ),

    'expphi'                         : RPNOperator( getExpPhi,
                                                    1, [ RPNOperator.Default ] ),

    'hyper4_2'                       : RPNOperator( tetrateLarge,
                                                    2, [ RPNOperator.Default, RPNOperator.Real ] ),

    'power'                          : RPNOperator( getPower,
                                                    2, [ RPNOperator.Default, RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'powmod'                         : RPNOperator( getPowModOperator,
                                                    3, [ RPNOperator.Integer, RPNOperator.Integer,
                                                         RPNOperator.Integer ] ),

    'root'                           : RPNOperator( getRoot,
                                                    2, [ RPNOperator.Default, RPNOperator.Real ],
                                                    RPNOperator.measurementsAllowed ),

    'square'                         : RPNOperator( square,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'square_root'                    : RPNOperator( getSquareRoot,
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

    'next_prime'                     : RPNOperator( getNextPrimeOperator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'next_primes'                    : RPNOperator( getNextPrimesOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'next_quadruplet_prime'          : RPNOperator( getNextQuadrupletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'next_quintuplet_prime'          : RPNOperator( getNextQuintupletPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_prime'                      : RPNOperator( findPrimeOperator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_quadruplet_prime'           : RPNOperator( findQuadrupletPrimeOperator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'nth_quintuplet_prime'           : RPNOperator( findQuintupletPrimeOperator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'polyprime'                      : RPNOperator( getNthPolyPrime,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'previous_prime'                 : RPNOperator( getPreviousPrimeOperator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'previous_primes'                : RPNOperator( getPreviousPrimesOperator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'prime'                          : RPNOperator( getNthPrime,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'primes'                         : RPNOperator( getPrimesGenerator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'prime_pi'                       : RPNOperator( getPrimePi,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'prime_range'                    : RPNOperator( getPrimeRange,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

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

    'safe_prime'                     : RPNOperator( getSafePrime,
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

    'timer'                          : RPNOperator( setTimer,
                                                    1, [ RPNOperator.Boolean ] ),

    'timer_mode'                     : RPNOperator( setTimerMode,
                                                    0, [ ] ),

    # special
    'constant'                       : RPNOperator( createConstant,
                                                    2, [ RPNOperator.Default, RPNOperator.String ],
                                                    RPNOperator.measurementsAllowed ),

    'delete_config'                  : RPNOperator( deleteUserConfiguration,
                                                    1, [ RPNOperator.String ] ),

    'describe'                       : RPNOperator( describeInteger,
                                                    1, [ RPNOperator.Integer ] ),

    'dump_config'                    : RPNOperator( dumpUserConfiguration,
                                                    0, [ ] ),

    'enumerate_dice'                 : RPNOperator( enumerateDiceGenerator,
                                                    1, [ RPNOperator.String ] ),

    'enumerate_dice_'                : RPNOperator( enumerateMultipleDiceGenerator,
                                                    2, [ RPNOperator.String, RPNOperator.PositiveInteger ] ),

    'estimate'                       : RPNOperator( estimate,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'help'                           : RPNOperator( printHelpMessage,
                                                    0, [ ] ),

    'get_config'                     : RPNOperator( getUserConfiguration,
                                                    1, [ RPNOperator.String ] ),

    'get_variable'                   : RPNOperator( getUserVariable,
                                                    1, [ RPNOperator.String ] ),

    'if'                             : RPNOperator( lambda a, b, c: a if c else b,
                                                    3, [ RPNOperator.Default, RPNOperator.Default, RPNOperator.Integer ] ),

    'list_from_file'                 : RPNOperator( readListFromFile,
                                                    1, [ RPNOperator.String ] ),

    'name'                           : RPNOperator( getName,
                                                    1, [ RPNOperator.Integer ] ),

    'oeis'                           : RPNOperator( downloadOEISSequence,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_comment'                   : RPNOperator( downloadOEISComment,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_ex'                        : RPNOperator( downloadOEISExtra,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_name'                      : RPNOperator( downloadOEISName,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'oeis_offset'                    : RPNOperator( downloadOEISOffset,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'ordinal_name'                   : RPNOperator( getOrdinalName,
                                                    1, [ RPNOperator.Integer ] ),

    'result'                         : RPNOperator( loadResult,
                                                    0, [ ] ),

    'permute_dice'                   : RPNOperator( permuteDiceGenerator,
                                                    1, [ RPNOperator.String ] ),

    'random'                         : RPNOperator( getRandomNumber,
                                                    0, [ ] ),

    'random_'                        : RPNOperator( getMultipleRandomsGenerator,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'random_integer'                 : RPNOperator( getRandomInteger,
                                                    1, [ RPNOperator.PositiveInteger ] ),

    'random_integer_'                : RPNOperator( getRandomIntegersGenerator,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'roll_dice'                      : RPNOperator( rollDice,
                                                    1, [ RPNOperator.String ] ),

    'roll_simple_dice'               : RPNOperator( rollSimpleDice,
                                                    2, [ RPNOperator.PositiveInteger, RPNOperator.PositiveInteger ] ),

    'roll_dice_'                     : RPNOperator( rollMultipleDiceGenerator,
                                                    2, [ RPNOperator.String, RPNOperator.PositiveInteger ] ),

    'set_config'                     : RPNOperator( setUserConfiguration,
                                                    2, [ RPNOperator.String, RPNOperator.String ] ),

    'set_variable'                   : RPNOperator( setUserVariable,
                                                    2, [ RPNOperator.String, RPNOperator.String ] ),

    'topic'                          : RPNOperator( printHelpTopic,
                                                    1, [ RPNOperator.String ] ),

    'uuid'                           : RPNOperator( generateUUID,
                                                    0, [ ] ),

    'uuid_random'                    : RPNOperator( generateRandomUUID,
                                                    0, [ ] ),

    'value'                          : RPNOperator( getValue,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    # trigonometry
    'acos'                           : RPNOperator( get_acos,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acosh'                          : RPNOperator( get_acosh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acot'                           : RPNOperator( get_acot,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acoth'                          : RPNOperator( get_acoth,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acsc'                           : RPNOperator( get_acsc,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'acsch'                          : RPNOperator( get_acsch,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asec'                           : RPNOperator( get_asec,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asech'                          : RPNOperator( get_asech,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asin'                           : RPNOperator( get_asin,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'asinh'                          : RPNOperator( get_asinh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'atan'                           : RPNOperator( get_atan,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'atanh'                          : RPNOperator( get_atanh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cos'                            : RPNOperator( get_cos,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cosh'                           : RPNOperator( get_cosh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'cot'                            : RPNOperator( get_cot,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'coth'                           : RPNOperator( get_coth,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'csc'                            : RPNOperator( get_csc,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'csch'                           : RPNOperator( get_csch,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sec'                            : RPNOperator( get_sec,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sech'                           : RPNOperator( get_sech,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sin'                            : RPNOperator( get_sin,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'sinh'                           : RPNOperator( get_sinh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'tan'                            : RPNOperator( get_tan,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    'tanh'                           : RPNOperator( get_tanh,
                                                    1, [ RPNOperator.Default ],
                                                    RPNOperator.measurementsAllowed ),

    # internal
    '_dump_aliases'                  : RPNOperator( dumpAliases,
                                                    0, [ ] ),

    '_dump_constants'                : RPNOperator( dumpConstants,
                                                    0, [ ] ),

    '_dump_operators'                : RPNOperator( dumpOperators,
                                                    0, [ ] ),

    '_dump_units'                    : RPNOperator( dumpUnits,
                                                    0, [ ] ),

    '_stats'                         : RPNOperator( dumpStats,
                                                    0, [ ] ),

    #   'antitet'                       : RPNOperator( findTetrahedralNumber, 0 ),
    #   'bernfrac'                      : RPNOperator( bernfrac, 1 ),
}

