#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeUnits
#//
#//  RPN command-line calculator unit conversion data generator
#//  copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import bz2
import contextlib
import itertools
import os
import pickle
import string

from mpmath import *

from rpnDeclarations import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_DESCRIPTION = 'RPN command-line calculator unit conversion data generator'


#//******************************************************************************
#//
#//  basicUnitTypes
#//
#//  conversion from the basic unit types (length, mass, time, current, angle)
#//
#//******************************************************************************

basicUnitTypes = {
    'acceleration'              : [ 'length/time^2', 'meter/second^2' ],
    'angle'                     : [ 'angle', 'radian' ],
    'area'                      : [ 'length^2', 'meter^2' ],
    'capacitance'               : [ 'current^2*time^4/mass*length^2', 'farad' ],
    'charge'                    : [ 'current*time', 'coulomb' ],
    'constant'                  : [ 'constant', 'unity' ],
    'current'                   : [ 'current', 'ampere' ],
    'data_rate'                 : [ 'information_entropy/time', 'bit/second' ],
    'electrical_conductance'    : [ 'time*current^2/mass*length^2', 'mho' ],
    'electrical_resistance'     : [ 'mass*length^2/time*current^2', 'ohm' ],
    'electric_potential'        : [ 'mass*length^2/current*time^3', 'volt' ],
    'energy'                    : [ 'mass*length^2/time^2', 'joule' ],
    'force'                     : [ 'mass*length/time', 'newton' ],
    'illuminance'               : [ 'luminous_intensity*angle^2/length^2', 'lux' ],
    'inductance'                : [ 'electric_potential*time/current', 'henry' ],
    'information_entropy'       : [ 'information_entropy', 'bit' ],
    'length'                    : [ 'length', 'meter' ],
    'luminance'                 : [ 'luminous_intensity/length^2', 'candela/meter^2' ],
    'luminous_flux'             : [ 'luminous_intensity*angle^2', 'lumen' ],
    'luminous_intensity'        : [ 'luminous_intensity', 'candela' ],
    'magnetic_field_strength'   : [ 'charge/length', 'ampere/meter' ],
    'magnetic_flux'             : [ 'electric_potential*time', 'weber' ],
    'magnetic_flux_density'     : [ 'electric_potential*time/length^2', 'tesla' ],
    'mass'                      : [ 'mass', 'gram' ],
    'power'                     : [ 'mass*length^2/time^3', 'watt' ],
    'pressure'                  : [ 'mass/length*time^2', 'pascal' ],
    'radiation_absorbed_dose'   : [ 'energy/mass', 'gray' ],
    'radiation_equivalent_dose' : [ 'radiation_equivalent_dose', 'sievert' ],
    'radiation_exposure'        : [ 'radiation_exposure', 'coulomb/kilogram' ],
    'radioactivity'             : [ 'radioactivity', 'becquerel' ],
    'solid_angle'               : [ 'angle^2', 'steradian' ],
    'temperature'               : [ 'temperature', 'kelvin' ],
    'time'                      : [ 'time', 'second' ],
    'velocity'                  : [ 'length/time', 'meter/second' ],
    'volume'                    : [ 'length^3', 'meter^3' ],
}


#//******************************************************************************
#//
#//  unitOperators
#//
#//  unit name : unitType, representation, plural, abbrev, aliases, categories
#//
#//******************************************************************************

unitOperators = {
    # acceleration

    'galileo' :
        UnitInfo( 'acceleration', 'galileo', 'galileos', '', [ ], [ 'CGS' ] ),

    'meter/second^2' :
        UnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', 'm/s^2', [ ], [ 'SI' ] ),

    'standard_gravity' :
        UnitInfo( 'acceleration', 'standard_gravity', 'standard_gravities', 'G', [ ], [ 'natural' ] ),

    # angle

    'arcminute' :
        UnitInfo( 'angle', 'arcminute', 'arcminutes', 'arcmin', [ 'arcmins' ], [ 'mathematics' ] ),

    'arcsecond' :
        UnitInfo( 'angle', 'arcsecond', 'arcseconds', 'arcsec', [ 'arcsecs' ], [ 'mathematics' ] ),

    'degree' :
        UnitInfo( 'angle', 'degree', 'degrees', 'deg', [ ], [ 'mathematics' ] ),

    'grad' :
        UnitInfo( 'angle', 'grad', 'grads', '', [ 'gon', 'gons' ], [ 'mathematics' ] ),

    'octant' :
        UnitInfo( 'angle', 'octant', 'octants', '', [ ], [ 'mathematics' ] ),

    'quadrant' :
        UnitInfo( 'angle', 'quadrant', 'quadrants', '', [ ], [ 'mathematics' ] ),

    'quintant' :
        UnitInfo( 'angle', 'quintant', 'quintants', '', [ ], [ 'mathematics' ] ),

    'radian' :
        UnitInfo( 'angle', 'radian', 'radians', 'rad', [ ], [ 'mathematics', 'SI' ] ),

    'sextant' :
        UnitInfo( 'angle', 'sextant', 'sextants', '', [ 'flat', 'flats' ], [ 'mathematics' ] ),

    # area

    'acre' :
        UnitInfo( 'area', 'acre', 'acres', 'ac', [ ], [ 'imperial' ] ),

    'are' :
        UnitInfo( 'area', 'are', 'ares', 'a', [ ], [ 'SI' ] ),

    'barn' :
        UnitInfo( 'area', 'barn', 'barns', '', [ ], [ 'science' ] ),

    'bovate' :
        UnitInfo( 'area', 'bovate', 'bovates', '', [ ], [ 'imperial' ] ),

    'carucate' :
        UnitInfo( 'area', 'carucate', 'carucates', '', [ ], [ 'imperial' ] ),

    'homestead':
        UnitInfo( 'area', 'homestead', 'homesteads', '', [ ], [ 'US' ] ),

    'outhouse' :
        UnitInfo( 'area', 'outhouse', 'outhouse', '', [ ], [ 'science', 'humorous' ] ),

    'rood' :
        UnitInfo( 'area', 'rood', 'roods', '', [ 'farthingdale' ], [ 'imperial' ] ),

    'section':
        UnitInfo( 'area', 'section', 'sections', '', [ ], [ 'US' ] ),

    'shed' :
        UnitInfo( 'area', 'shed', 'sheds', '', [ ], [ 'science' ] ),

    'square_meter' :
        UnitInfo( 'area', 'meter^2', 'square_meters', 'm^2', [ 'meter^2', 'meters^2' ], [ 'SI' ] ),

    'square_yard' :
        UnitInfo( 'area', 'yard^2', 'square_yards', 'sqyd', [ 'sqyd', 'yd^2', 'yard^2', 'yards^2' ], [ 'imperial' ] ),

    'township':
        UnitInfo( 'area', 'township', 'townships', '', [ ], [ 'US' ] ),

    'virgate':
        UnitInfo( 'area', 'virgate', 'virgates', '', [ ], [ 'imperial' ] ),

    # capacitance

    'abfarad' :
        UnitInfo( 'capacitance', 'abfarad', 'abfarads', 'abF', [ ], [ 'CGS' ] ),

    'coulomb/volt' :
        UnitInfo( 'capacitance', 'coulomb/volt', 'coulombs/volt', 'C/V', [ 'coulomb/volts', 'coulombs/volts', 'C/volts', 'C/volt', 'coulomb/V', 'coulombs/V' ], [ 'SI' ] ),

    'farad' :
        UnitInfo( 'capacitance', 'farad', 'farads', 'F', [ ], [ 'SI' ] ),

    'jar' :
        UnitInfo( 'capacitance', 'jar', 'jars', '', [ ], [ 'obsolete' ] ),

    'statfarad' :
        UnitInfo( 'capacitance', 'statfarad', 'statfarads', 'statF', [ ], [ 'CGS' ] ),

    # charge

    'abcoulomb' :
        UnitInfo( 'charge', 'abcoulomb', 'abcoulombs', 'abC', [ ], [ 'CGS' ] ),

    'ampere-second' :
        UnitInfo( 'charge', 'ampere*second', 'ampere*second', 'A/s', [ 'ampere/sec', 'ampere/s', 'amp/sec', 'amp/s', 'amps/sec', 'amps/s' ], [ 'SI' ] ),

    'coulomb' :
        UnitInfo( 'charge', 'coulomb', 'coulombs', 'C', [ ], [ 'SI' ] ),

    'farad-volt' :
        UnitInfo( 'charge', 'farad*volt', 'farad-volts', 'F*V', [ 'F/volt', 'F/volts', 'farad/volts', 'farads/volts', 'farad/V', 'farads/V' ], [ 'SI' ] ),

    'franklin' :
        UnitInfo( 'charge', 'franklin', 'franklins', 'Fr', [ ], [ 'CGS' ] ),

    'electron_charge' :
        UnitInfo( 'charge', 'electron_charge', 'electron_charges', '', [ 'elementary_charge', 'proton_charge' ], [ 'natural' ] ),

    'faraday' :
        UnitInfo( 'charge', 'faraday', 'faradays', 'Fd', [ ], [ 'natural' ] ),   # electron_charge * Avogradro's number!

    'planck_charge' :
        UnitInfo( 'charge', 'planck_charge', 'planck_charges', '', [ ], [ 'natural' ] ),

    'statcoulomb' :
        UnitInfo( 'charge', 'statcoulomb', 'statcoulombs', 'statC', [ 'esu_charge' ], [ 'CGS' ] ),

    # constant - Constant is a special type that is immediately converted to a numerical value when used.
    #            It's not intended to be used as a unit, per se.  Also, these units are in order of their
    #            value instead of alphabetical order like all the others

    'unity' :
        UnitInfo( 'constant', 'unity', 'x unity', '', [ ], [ 'constant' ] ),

    'dozen' :
        UnitInfo( 'constant', 'dozen', 'dozen', '', [ ], [ 'constant' ] ),

    'score' :
        UnitInfo( 'constant', 'score', 'score', '', [ ], [ 'constant' ] ),

    'hundred' :
        UnitInfo( 'constant', 'hundred', 'hundred', '', [ ], [ 'constant' ] ),

    'thousand' :
        UnitInfo( 'constant', 'thousand', 'thousand', '', [ ], [ 'constant' ] ),

    'million' :
        UnitInfo( 'constant', 'million', 'million', '', [ ], [ 'constant' ] ),

    'billion' :
        UnitInfo( 'constant', 'billion', 'billion', '', [ ], [ 'constant' ] ),

    'trillion' :
        UnitInfo( 'constant', 'trillion', 'trillion', '', [ ], [ 'constant' ] ),

    'quadrillion' :
        UnitInfo( 'constant', 'quadrillion', 'quadrillion', '', [ ], [ 'constant' ] ),

    'quintillion' :
        UnitInfo( 'constant', 'quintillion', 'quintillion', '', [ ], [ 'constant' ] ),

    'sextillion' :
        UnitInfo( 'constant', 'sextillion', 'sextillion', '', [ ], [ 'constant' ] ),

    'septillion' :
        UnitInfo( 'constant', 'septillion', 'septillion', '', [ ], [ 'constant' ] ),

    'octillion' :
        UnitInfo( 'constant', 'octillion', 'octillion', '', [ ], [ 'constant' ] ),

    'nonillion' :
        UnitInfo( 'constant', 'nonillion', 'nonillion', '', [ ], [ 'constant' ] ),

    'decillion' :
        UnitInfo( 'constant', 'decillion', 'decillion', '', [ ], [ 'constant' ] ),

    'googol' :
        UnitInfo( 'constant', 'googol', 'googols', '', [ ], [ 'constant' ] ),

    'centillion' :
        UnitInfo( 'constant', 'centillion', 'centillion', '', [ ], [ 'constant' ] ),

    # current

    'abampere' :
        UnitInfo( 'current', 'abampere', 'abamperes', 'abA', [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ] ),

    'ampere' :
        UnitInfo( 'current', 'ampere', 'amperes', 'A', [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ] ),

    'coulomb/second' :
        UnitInfo( 'current', 'coulomb/second', 'coulombs/second', 'C/s', [ 'C/sec', 'coulomb/sec', 'coulombs/sec', 'coulomb/s', 'coulombs/s' ], [ 'SI' ] ),

    'statampere' :
        UnitInfo( 'current', 'statampere', 'statamperes', 'statA', [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ] ),

    # data_rate

    'bit/second' :
        UnitInfo( 'data_rate', 'bit/second', 'bits/second', 'b/s', [ 'bit/s', 'bits/s', 'bit/sec', 'bits/sec' ], [ 'computing' ] ),

    'byte/second' :
        UnitInfo( 'data_rate', 'byte/second', 'bytes/second', 'B/s', [ 'byte/s', 'bytes/s' 'byte/sec', 'bytes/sec' ], [ 'computing' ] ),

    # electric_potential

    'abvolt' :
        UnitInfo( 'electric_potential', 'abvolt', 'abvolts', 'abV', [ ], [ 'CGS' ] ),

    'coulomb/farad' :
        UnitInfo( 'electric_potential', 'coulomb/farad', 'coulombs/farad', 'C/F', [ 'coulomb/F', 'coulombs/F', 'C/farad', 'C/farads', 'coulombs/farads' ], [ 'SI' ] ),

    'volt' :
        UnitInfo( 'electric_potential', 'volt', 'volts', 'V', [ ], [ 'SI' ] ),

    'watt/ampere' :
        UnitInfo( 'electric_potential', 'watt/ampere', 'watts/ampere', 'W/A', [ 'watt/amp', 'watt/amps', 'watt/A', 'watts/amp', 'watts/amps', 'watts/A', 'W/amp', 'W/amps', 'W/ampere', 'W/amperes' ], [ 'SI' ] ),

    'statvolt' :
        UnitInfo( 'electric_potential', 'statvolt', 'statvolts', 'statV', [ 'esu_potential' ], [ 'CGS' ] ),

    # electrical_conductance

    'abmho' :
        UnitInfo( 'electrical_conductance', 'abmho', 'abmhos', '', [ ], [ 'CGS' ] ),

    'ampere/volt' :
        UnitInfo( 'electrical_conductance', 'ampere/volt', 'amperes/volt', 'A/V', [ 'amp/V', 'amps/V', 'ampere/V', 'amperes/V', 'A/volt', 'amp/volt', 'amps/volt', 'A/volts', 'amp/volts', 'amps/volts', 'amperes/volts', ], [ 'SI' ] ),

    'second^3-ampere^2/kilogram-meter^2':
        UnitInfo( 'electrical_conductance', 'kilogram*meter^2/second^3*ampere^2', 'kilogram*meter^2/second^3*ampere^2', 'kg*m^2/s^3*A^2', [ ], [ 'SI' ] ),

    'siemens' :
        UnitInfo( 'electrical_conductance', 'siemens', 'siemens', 'S', [ 'mho' ], [ 'SI' ] ),

    'statmho' :
        UnitInfo( 'electrical_conductance', 'statmho', 'statmhos', '', [ ], [ 'CGS' ] ),

    # electrical_resistance

    '1/siemens' :
        UnitInfo( 'electrical_resistance', '1/siemens', '1/siemens', '1/S', [ '1/mho' ], [ 'SI' ] ),

    'abohm' :
        UnitInfo( 'electrical_resistance', 'abohm', 'abohms', 'o', [ ], [ 'CGS' ] ),

    'german_mile' :
        UnitInfo( 'electrical_resistance', 'german_mile', 'german_mile', '', [ ], [ 'obsolete' ] ),

    'jacobi' :
        UnitInfo( 'electrical_resistance', 'jacobi', 'jacobis', '', [ ], [ 'obsolete' ] ),

    'joule-second/coulomb^2' :
        UnitInfo( 'electrical_resistance', 'joule*second/coulomb^2', 'joule*second/coulomb^2', 'J*s/C^2', [ ], [ 'SI' ] ),

    'joule/second-ampere^2' :
        UnitInfo( 'electrical_resistance', 'joule/second*ampere^2', 'joule/second*ampere^2', 'J/s*A^2', [ ], [ 'SI' ] ),

    'kilogram-meter^2/second^3-ampere^2' :
        UnitInfo( 'electrical_resistance', 'kilogram*meter^2/second^3*ampere^2', 'kilogram*meter^2/second^3*ampere^2', 'kg*m^2/s^3*A^2', [ ], [ 'SI' ] ),

    'matthiessen' :
        UnitInfo( 'electrical_resistance', 'matthiessen', 'matthiessens', '', [ ], [ 'obsolete' ] ),   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C

    'meter^2-kilogram/second-couloumb^2' :
        UnitInfo( 'electrical_resistance', 'meter^2*kilogram/second*couloumb^2', 'meter^2*kilogram/second*couloumb^2', 'm^2*kg/s*C^2', [ ], [ 'SI' ] ),

    'ohm' :
        UnitInfo( 'electrical_resistance', 'ohm', 'ohms', 'O', [ ], [ 'SI' ] ),

    'second/farad' :
        UnitInfo( 'electrical_resistance', 'second/farad', 'second/farad', 's/F', [ 's/farad', 's/farads', 'sec/farad', 'sec/farads', 'sec/F', 'second/F', 'seconds/F' ], [ 'SI' ] ),

    'statohm' :
        UnitInfo( 'electrical_resistance', 'statohm', 'statohms', 'statO', [ ], [ 'SI' ] ),

    'varley' :
        UnitInfo( 'electrical_resistance', 'varley', 'varleys', '', [ ], [ 'obsolete' ] ),  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C

    'von_klitzing_constant' :
        UnitInfo( 'electrical_resistance', 'von_klitzing_constant', 'x_von_klitzing_constant', '', [ 'von_klitzing' ], [ 'natural' ] ),

    'volt/ampere' :
        UnitInfo( 'electrical_resistance', 'volt/ampere', 'volts/ampere', 'V/A', [ 'volt/amp', 'volt/amps', 'volt/A', 'volts/amp', 'volts/amps', 'volts/A', 'V/amp', 'V/amps', 'V/ampere', 'V/amperes' ], [ 'SI' ] ),

    'watt/ampere^2' :
        UnitInfo( 'electrical_resistance', 'watt/ampere^2', 'watts/ampere^2', 'W/A^2', [ 'watt/amperes^2', 'watts/amperes^2', 'W/ampere^2', 'W/amperes^2' ], [ 'SI' ] ),

    # energy

    'aa_battery' :
        UnitInfo( 'energy', 'AA_battery', 'AA_batteries', '', [ 'aa-battery', 'aa-batteries', 'AA-battery', 'AA-batteries' ], [ 'informal' ] ),

    'btu' :
        UnitInfo( 'energy', 'BTU', 'BTUs', '', [ 'btu', 'btus' ], [ 'England', 'US' ] ),

    'calorie' :
        UnitInfo( 'energy', 'calorie', 'calories', 'cal', [ ], [ 'CGS' ] ),

    'electronvolt' :
        UnitInfo( 'energy', 'electronvolt', 'electronvolts', 'eV', [ 'electron-volt', 'electron-volts' ], [ 'science' ] ),

    'erg' :
        UnitInfo( 'energy', 'erg', 'ergs', '', [ ], [ 'CGS' ] ),

    'gallon_of_ethanol' :
        UnitInfo( 'energy', 'gallon_of_ethanol', 'gallons_of_ethanol', '', [ ], [ 'informal' ] ),

    'gallon_of_gasoline' :
        UnitInfo( 'energy', 'gallon_of_gasoline', 'gallons_of_gasoline', '', [ 'gallon_of_gas', 'gallons_of_gas' ], [ 'informal' ] ),

    'gram-equivalent' :
        UnitInfo( 'energy', 'gram-equivalent', 'grams-equivalent', 'gE', [ 'gram-energy', 'grams-energy', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ] ),

    'hartree' :
        UnitInfo( 'energy', 'hartree', 'hartrees', 'Ha', [ ], [ 'science' ] ),

    'horsepower-second' :
        UnitInfo( 'energy', 'horsepower*second', 'horsepower-seconds', 'hps', [ ], [ 'US' ] ),

    'joule' :
        UnitInfo( 'energy', 'joule', 'joules', 'J', [ ], [ 'SI' ] ),

    'kilogram-meter^2/second^2' :
        UnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', 'kg*m^2/s^2', [ ], [ 'SI' ] ),

    'newton-meter' :
        UnitInfo( 'energy', 'newton*meter', 'newton-meters', 'N*m', [ ], [ 'SI' ] ),

    'planck_energy' :
        UnitInfo( 'energy', 'planck_energy', 'planck_energy', 'EP', [ ], [ 'natural' ] ),

    'rydberg' :
        UnitInfo( 'energy', 'rydberg', 'rydbergs', 'Ry', [ ], [ 'science' ] ),

    'ton_of_TNT' :
        UnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT', [ ], [ 'informal' ] ),

    'watt-second' :
        UnitInfo( 'energy', 'watt*second', 'watt-seconds', 'Ws', [ ], [ 'SI' ] ),

    # force

    'dyne' :
        UnitInfo( 'force', 'dyne', 'dynes', 'dyn', [ ], [ 'CGS' ] ),

    'gram-force' :
        UnitInfo( 'force', 'gram-force', 'grams-force', 'g-m', [ ], [ 'CGS' ] ),

    'joule/meter' :
        UnitInfo( 'force', 'joule/meter', 'joule/meter', 'J/m', [ ], [ 'SI' ] ),

    'newton' :
        UnitInfo( 'force', 'newton', 'newtons', 'N', [ ], [ 'SI' ] ),

    'pond' :
        UnitInfo( 'force', 'pond', 'ponds', 'p', [ ], [ 'metric' ] ),

    'pound-foot/second^2' :
        UnitInfo( 'force', 'pound*foot/second^2', 'pound*foot/second^2', 'lb*ft/sec^2', [ ], [ 'FPS' ] ),

    'poundal' :
        UnitInfo( 'force', 'poundal', 'poundals', 'pdl', [ ], [ 'England' ] ),

    'sthene' :
        UnitInfo( 'force', 'sthene', 'sthenes', 'sn', [ 'funal' ], [ 'MTS' ] ),

    # illuminance

    'footcandle' :
        UnitInfo( 'illuminance', 'footcandle', 'footcandles', 'fc', [ ], [ 'FPS' ] ),

    'lux' :
        UnitInfo( 'illuminance', 'lux', 'lux', 'lx', [ ], [ 'SI' ] ),

    'lumen/meter^2' :
        UnitInfo( 'illuminance', 'lumen/meter^2', 'lumens/meter^2', 'lm/m^2', [ 'lm/square_meter', 'lumen/square_meter', 'lumens/square_meter', 'lumen/m^2', 'lumens/m^2' ], [ 'SI' ] ),

    'lumen/foot^2' :
        UnitInfo( 'illuminance', 'lumen/foot^2', 'lumens/foot^2', 'lm/ft^2', [ 'lm/square_foot', 'lumen/square_foot', 'lumens/square_foot', 'lumen/ft^2', 'lumens/ft^2' ], [ 'FPS' ] ),

    'nox' :
        UnitInfo( 'illuminance', 'nox', 'nox', 'nx', [ ], [ 'obsolete' ] ),

    'phot' :
        UnitInfo( 'illuminance', 'phot', 'phots', 'ph', [ ], [ 'CGS' ] ),

    # inductance

    'abhenry' :
        UnitInfo( 'inductance', 'abhenry', 'abhenries', 'abH', [ ], [ 'CGS' ] ),

    'henry' :
        UnitInfo( 'inductance', 'henry', 'henries', 'H', [ ], [ 'SI' ] ),

    'weber/ampere' :
        UnitInfo( 'inductance', 'weber/ampere', 'webers/ampere', 'Wb/A', [ 'Wb/ampere', 'Wb/ampere', 'weber/A', 'webers/A', 'Wb/amp', 'weber/amp', 'webers/amp' ], [ 'SI' ] ),

    'stathenry' :
        UnitInfo( 'inductance', 'stathenry', 'stathenries', 'statH', [ ], [ 'CGS' ] ),

    # information_entropy

    'ban' :
        UnitInfo( 'information_entropy', 'ban', 'bans', '', [ 'hartley', 'hartleys', 'dit', 'dits' ], [ 'IEC' ] ),

    'bit' :
        UnitInfo( 'information_entropy', 'bit', 'bits', 'b', [ 'shannon', 'shannons' ], [ 'computing' ] ),

    'byte' :
        UnitInfo( 'information_entropy', 'byte', 'bytes', 'B', [ 'octet', 'octets' ], [ 'computing' ] ),

    'clausius' :
        UnitInfo( 'information_entropy', 'clausius', 'clausius', '', [ ], [ 'CGS' ] ),

    'dword' :
        UnitInfo( 'information_entropy', 'dword', 'dwords', '', [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ] ),

    'joule/kelvin' :
        UnitInfo( 'information_entropy', 'joule/kelvin', 'joules/kelvin', 'J/K', [ 'joule/K', 'joules/K' ], [ 'SI' ] ),

    'nibble' :
        UnitInfo( 'information_entropy', 'nibble', 'nibbles', '', [ 'nybble', 'nybbles' ], [ 'computing' ] ),

    'nat' :
        UnitInfo( 'information_entropy', 'nat', 'nats', '', [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ] ),

    'nyp' :
        UnitInfo( 'information_entropy', 'nyp', 'nyps', '', [ ], [ 'computing' ] ),   # suggested by Donald Knuth

    'oword' :
        UnitInfo( 'information_entropy', 'oword', 'owords', '', [ 'octaword', 'octawords' ], [ 'computing' ] ),

    'qword' :
        UnitInfo( 'information_entropy', 'qword', 'qwords', '', [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ] ),

    'trit' :
        UnitInfo( 'information_entropy', 'trit', 'trits', '', [ ], [ 'computing' ] ),

    'tryte' :
        UnitInfo( 'information_entropy', 'tryte', 'trytes', '', [ ], [ 'computing' ] ),

    'word' :
        UnitInfo( 'information_entropy', 'word', 'words', '', [ 'short_integer', 'short_integers', 'wyde' ], [ 'computing' ] ),  # 'wyde' suggested by Knuth

    # length

    'aln' :
        UnitInfo( 'length', 'aln', 'aln', '', [ ], [ 'obsolete' ] ),

    'arpent' :
        UnitInfo( 'length', 'arpent', 'arpent', '', [ ], [ 'obsolete', 'France' ] ),

    'angstrom' :
        UnitInfo( 'length', 'angstrom', 'angstroms', 'A', [ ], [ 'science' ] ),

    'astronomical_unit' :
        UnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au', [ ], [ 'science' ] ),

    'barleycorn' :
        UnitInfo( 'length', 'barleycorn', 'barleycorns', '', [ ], [ 'imperial' ] ),

    'caliber' :
        UnitInfo( 'length', 'caliber', 'caliber', '', [ 'calibre' ], [ 'US' ] ),

    'chain' :
        UnitInfo( 'length', 'chain', 'chains', '', [ ], [ 'imperial' ] ),

    'cubit' :
        UnitInfo( 'length', 'cubit', 'cubits', '', [ ], [ 'imperial' ] ),

    'ell' :
        UnitInfo( 'length', 'ell', 'ell', '', [ ], [ 'imperial' ] ),

    'famn' :
        UnitInfo( 'length', 'famn', 'famn', '', [ ], [ 'obsolete' ] ),

    'farshimmelt_potrzebie' :
        UnitInfo( 'length', 'farshimmelt_potrzebie', 'farshimmelt potrzebies', 'fpz', [ 'far-potrzebie' ], [ 'Potrzebie', 'humorous' ] ),

    'fathom' :
        UnitInfo( 'length', 'fathom', 'fathom', 'fath', [ ], [ 'imperial' ] ),

    'finger' :
        UnitInfo( 'length', 'finger', 'finger', '', [ ], [ 'imperial' ] ),

    'fingerbreadth' :
        UnitInfo( 'length', 'fingerbreadth', 'fingerbreadths', '', [ 'fingersbreadth' ], [ 'obsolete' ] ),

    'foot' :
        UnitInfo( 'length', 'foot', 'feet', 'ft', [ ], [ 'traditional', 'FPS' ] ),

    'furlong' :
        UnitInfo( 'length', 'furlong', 'furlongs', '', [ ], [ 'imperial' ] ),

    'furshlugginer_potrzebie' :
        UnitInfo( 'length', 'furshlugginer_potrzebie', 'furshlugginer potrzebies', 'Fpz', [ 'Fur-potrzebie' ], [ 'Potrzebie', 'humorous' ] ),

    'greek_cubit' :
        UnitInfo( 'length', 'greek_cubit', 'greek_cubits', '', [ ], [ 'obsolete', 'Greece' ] ),

    'gutenberg' :
        UnitInfo( 'length', 'gutenberg', 'gutenbergs', '', [ ], [ 'typography' ] ),

    'hand' :
        UnitInfo( 'length', 'hand', 'hands', '', [ ], [ 'imperial' ] ),

    'handbreadth' :
        UnitInfo( 'length', 'handbreadth', 'handbreadths', '', [ 'handsbreadth' ], [ 'obsolete' ] ),

    'inch' :
        UnitInfo( 'length', 'inch', 'inches', 'in', [ ], [ 'imperial' ] ),

    'long_reed' :
        UnitInfo( 'length', 'long_reed', 'long_reeds', '', [ ], [ 'obsolete' ] ),

    'long_cubit' :
        UnitInfo( 'length', 'long_cubit', 'long_cubits', '', [ ], [ 'obsolete' ] ),

    'ken' :
        UnitInfo( 'length', 'ken', 'ken', '', [ ], [ 'obsolete' ] ),

    'kyu' :
        UnitInfo( 'length', 'kyu', 'kyus', '', [ 'Q' ], [ 'typography', 'computing' ] ),

    'league' :
        UnitInfo( 'length', 'league', 'leagues', '', [ ], [ 'imperial' ] ),

    'light-second' :
        UnitInfo( 'length', 'light*second', 'light-seconds', '', [ 'light-second' ], [ 'science' ] ),

    'light-year' :
        UnitInfo( 'length', 'light-year', 'light-years', 'ly', [ ], [ 'science' ] ),

    'link' :
        UnitInfo( 'length', 'link', 'link', '', [ ], [ 'informal' ] ),

    'marathon' :
        UnitInfo( 'length', 'marathon', 'marathons', '', [ ], [ 'informal' ] ),

    'meter' :
        UnitInfo( 'length', 'meter', 'meters', 'm', [ ], [ 'SI' ] ),

    'micron' :
        UnitInfo( 'length', 'micron', 'microns', '', [ ], [ 'science' ] ),

    'mil' :
        UnitInfo( 'length', 'mil', 'mils', '', [ 'thou' ], [ 'US' ] ),

    'mile' :
        UnitInfo( 'length', 'mile', 'miles', 'mi', [ ], [ 'imperial' ] ),

    'nail' :
        UnitInfo( 'length', 'nail', 'nail', '', [ ], [ 'imperial' ] ),

    'nautical_mile' :
        UnitInfo( 'length', 'nautical_mile', 'nautical_miles', '', [ ], [ 'nautical' ] ),

    'parsec' :
        UnitInfo( 'length', 'parsec', 'parsec', 'pc', [ ], [ 'science' ] ),

    'perch' :
        UnitInfo( 'length', 'perch', 'perches', '', [ 'pole', 'poles' ], [ 'imperial' ] ),

    'pica' :
        UnitInfo( 'length', 'pica', 'pica', '', [ 'cicero' ], [ 'typography' ] ),

    'planck_length' :
        UnitInfo( 'length', 'planck_length', 'planck_length', 'lP', [ ], [ 'science' ] ),

    'point' :
        UnitInfo( 'length', 'point', 'points', '', [ ], [ 'typography' ] ),

    'poppyseed' :
        UnitInfo( 'length', 'poppyseed', 'poppyseeds', '', [ ], [ 'imperial' ] ),

    'reed' :
        UnitInfo( 'length', 'reed', 'reeds', '', [ ], [ 'obsolete' ] ),

    'rod' :
        UnitInfo( 'length', 'rod', 'rods', 'rd', [ ], [ 'imperial' ] ),

    'rope' :
        UnitInfo( 'length', 'rope', 'ropes', '', [ ], [ 'obsolete' ] ),

    'potrzebie' :
        UnitInfo( 'length', 'potrzebie', 'potrzebies', 'pz', [ ], [ 'Potrzebie', 'humorous' ] ),

    'smoot' :
        UnitInfo( 'length', 'smoot', 'smoots', '', [ ], [ 'humorous' ] ),

    'span' :
        UnitInfo( 'length', 'span', 'spans', '', [ 'breadth' ], [ 'imperial' ] ),

    'twip' :
        UnitInfo( 'length', 'twip', 'twips', '', [ ], [ 'computing' ] ),

    'yard' :
        UnitInfo( 'length', 'yard', 'yards', 'yd', [ ], [ 'imperial' ] ),

    # luminance

    'apostilb' :
        UnitInfo( 'luminance', 'apostilb', 'apostilbs', 'asb', [ 'blondel' ], [ 'CGS' ] ),

    'bril' :
        UnitInfo( 'luminance', 'bril', 'brils', '', [ ], [ 'obsolete' ] ),

    'candela/meter^2' :
        UnitInfo( 'luminance', 'candela/meter^2', 'candelas/meter^2', 'cd/m^2', [ 'candela/m^2', 'candelas/m^2', 'candela/square_meter', 'candelas/square_meter', 'cd/square_meter' ], [ 'SI' ] ),

    'footlambert' :
        UnitInfo( 'luminance', 'footlambert', 'footlamberts', 'fL', [ 'foot-lambert' ], [ 'US', 'obsolete' ] ),

    'lambert' :
        UnitInfo( 'luminance', 'lambert', 'lamberts', 'L', [ ], [ 'CGS' ] ),

    'nit' :
        UnitInfo( 'luminance', 'nit', 'nits', 'nt', [ 'meterlambert', 'meter-lambert', 'meterlamberts', 'meter-lamberts' ], [ 'obsolete' ] ),

    'skot' :
        UnitInfo( 'luminance', 'skot', 'skots', '', [ ], [ 'obsolete' ] ),

    'stilb' :
        UnitInfo( 'luminance', 'stilb', 'stilbs', 'sb', [ ], [ 'CGS' ] ),

    # luminous_flux

    'lumen' :
        UnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm', [ ], [ 'SI' ] ),

    'candela-steradian' :
        UnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm', [ ], [ 'SI' ] ),

    # luminous_intensity

    'candela' :
        UnitInfo( 'luminous_intensity', 'candela', 'candelas', 'cd', [ ], [ 'SI' ] ),

    'hefnerkerze' :
        UnitInfo( 'luminous_intensity', 'hefnerkerze', 'hefnerkerze', 'HK', [ ], [ 'obsolete' ] ),

    # magnetic_field_strength

    'ampere/meter' :
        UnitInfo( 'magnetic_field_strength', 'ampere/meter', 'amperes/meter', 'A/m', [ 'amp/m', 'amps/m', 'ampere/m', 'amperes/m', 'A/meter', 'amp/meter', 'amps/meter', 'A/meters', 'amp/meters', 'amps/meters', 'ampere/meters', 'amperes/meters' ], [ 'SI' ] ),

    'oersted' :
        UnitInfo( 'magnetic_field_strength', 'oersted', 'oersted', 'Oe', [ ], [ 'CGS' ] ),

    # magnetic_flux

    'gauss*centimeter^2' :
        UnitInfo( 'magnetic_flux', 'gauss*centimeter^2', 'gauss*centimeter^2', 'gauss*cm^2', [ 'gauss*square_cm' ], [ 'CGS' ] ),

    'maxwell' :
        UnitInfo( 'magnetic_flux', 'maxwell', 'maxwells', 'Mx', [ 'line' ], [ 'CGS' ] ),

    'volt-second' :
        UnitInfo( 'magnetic_flux', 'volt*second', 'volts*seconds', 'V*s', [ ], [ 'SI' ] ),

    'unit_pole' :
        UnitInfo( 'magnetic_flux', 'unit_pole', 'unit_pole', '', [ ], [ 'CGS' ] ),

    'tesla*meter^2' :
        UnitInfo( 'magnetic_flux', 'tesla*meter^2', 'tesla*meter^2', 'T/m^2', [ 'tesla*square_meter', 'teslas*square_meter', 'T*square_meter', 'tesla*m^2', 'teslas*m^2', 'teslas*meter^2' ], [ 'SI' ] ),

    'weber' :
        UnitInfo( 'magnetic_flux', 'weber', 'webers', 'Wb', [ ], [ 'SI' ] ),

    # magnetic_flux_density

    'gauss' :
        UnitInfo( 'magnetic_flux_density', 'gauss', 'gauss', 'Gs', [ ], [ 'CGS' ] ),

    'kilogram/ampere-second^2' :
        UnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', 'kilogram/ampere*second^2', 'kg/A*s^2', [ ], [ 'SI' ] ),

    'maxwell/centimeter^2' :
        UnitInfo( 'magnetic_flux_density', 'maxwell/centimeter^2', 'maxwells/centimeter^2', 'Mx/cm^2', [ 'maxwell/cm^2', 'maxwells/cm^2', 'Mx/centimeter^2', 'Mx/square_centimeter', 'Mx/square_cm', 'maxwell/square_centimeter', 'maxwells/square_centimeter', 'maxwell/square_cm', 'maxwells/square_cm' ], [ 'CGS' ] ),

    'tesla' :
        UnitInfo( 'magnetic_flux_density', 'tesla', 'teslas', 'T', [ ], [ 'SI' ] ),

    'weber/meter^2' :
        UnitInfo( 'magnetic_flux_density', 'weber/meter^2', 'webers/meter^2', 'Wb/m^2', [ ], [ 'SI' ] ),

    # mass

    'blintz' :
        UnitInfo( 'mass', 'blintz', 'blintzes', 'b', [ ], [ 'Potrzebie', 'humorous' ] ),

    'carat' :
        UnitInfo( 'mass', 'carat', 'carats', 'kt', [ 'karat', 'karats' ], [ 'US' ] ),

    'dalton' :
        UnitInfo( 'mass', 'dalton', 'daltons', '', [ 'amu', 'atomic-mass-unit' ], [ 'science' ] ),

    'electron_rest_mass' :
        UnitInfo( 'mass', 'electron_rest_mass', 'x_electron_rest_mass', '', [ ], [ 'natural' ] ),

    'farshimmelt_blintz' :
        UnitInfo( 'mass', 'farshimmelt_blintz', 'farshimmelt_blintzes', 'fb', [ 'far-blintz' ], [ 'Potrzebie', 'humorous' ] ),

    'furshlugginer_blintz' :
        UnitInfo( 'mass', 'furshlugginer_blintz', 'furshlugginer_blintzes', 'Fb', [ 'Fur-blintz' ], [ 'Potrzebie', 'humorous' ] ),

    'grain' :
        UnitInfo( 'mass', 'grain', 'grains', 'gr', [ ], [ 'traditional' ] ),

    'gram' :
        UnitInfo( 'mass', 'gram', 'grams', 'g', [ 'gramme', 'grammes' ], [ 'SI' ] ),

    'kip' :
        UnitInfo( 'mass', 'kip', 'kips', '', [ 'kilopound', 'kilopounds' ], [ 'US' ] ),

    'ounce' :
        UnitInfo( 'mass', 'ounce', 'ounces', 'oz', [ ], [ 'traditional' ] ),

    'pennyweight' :
        UnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt', [ 'pwt' ], [ 'traditional', 'England' ] ),

    'planck_mass' :
        UnitInfo( 'mass', 'planck_mass', 'planck_masses', 'mP', [ ], [ 'natural' ] ),

    'pound' :
        UnitInfo( 'mass', 'pound', 'pounds', 'lb', [ ], [ 'US', 'traditional', 'FPS' ] ),

    'quintal' :
        UnitInfo( 'mass', 'quintal', 'quintals', 'q', [ ], [ ] ),

    'sheet' :
        UnitInfo( 'mass', 'sheet', 'sheets', '', [ ], [ ] ),

    'slug' :
        UnitInfo( 'mass', 'slug', 'slugs', '', [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ] ),

    'stone' :
        UnitInfo( 'mass', 'stone', 'stone', '', [ ], [ 'traditional', 'England' ] ),

    'stone_us' :
        UnitInfo( 'mass', 'stone_us', 'stones_us', '', [ 'us_stone', 'us_stones' ], [ 'US' ] ),

    'ton' :
        UnitInfo( 'mass', 'ton', 'tons', '', [ ], [ 'traditional', 'US' ] ),

    'tonne' :
        UnitInfo( 'mass', 'tonne', 'tonnes', '', [ ], [ 'MTS' ] ),

    'troy_ounce' :
        UnitInfo( 'mass', 'troy_ounce', 'troy_ounces', '', [ ], [ 'traditional' ] ),

    'troy_pound' :
        UnitInfo( 'mass', 'troy_pound', 'troy_pounds', '', [ ], [ 'traditional'  ] ),

    'wey' :
        UnitInfo( 'mass', 'wey', 'weys', '', [ ], [ 'obsolete', 'England' ] ),

    # power

    'dBm' :
        UnitInfo( 'power', 'dBm', 'dBm', 'dBm', [ 'dBmW', 'decibel-milliwatt' ], [ 'engineering' ] ),

    'erg/second' :
        UnitInfo( 'power', 'erg/second', 'ergs/second', 'erg/s', [ 'ergs/s' ], [ 'CGS' ] ),

    'horsepower' :
        UnitInfo( 'power', 'horsepower', 'horsepower', 'hp', [ ], [ 'US' ] ),

    'joule/second' :
        UnitInfo( 'power', 'joule/second', 'joules/second', 'J/s', [ 'joule/s', 'joules/s', 'J/sec', 'joule/sec', 'joules/sec', 'J/seconds', 'joule/seconds', 'joules/seconds' ], [ 'SI' ] ),

    'kilogram-meter^2/second^3' :
        UnitInfo( 'power', 'kilogram*meter^2/second^3', 'kilogram*meter^2/second^3', 'kg*m^2/s^3', [ ], [ 'SI' ] ),

    'newton-meter/second' :
        UnitInfo( 'power', 'newton*meter/second', 'newton*meter/second', 'N*m/s', [ ], [ 'SI' ] ),

    'pferdestarke' :
        UnitInfo( 'power', 'pferdestarke', 'pferdestarke', 'pf', [ ], [ 'obsolete', 'Germany' ] ),

    'poncelet' :
        UnitInfo( 'power', 'poncelet', 'poncelets', 'p', [ ], [ 'obsolete' ] ),

    'watt' :
        UnitInfo( 'power', 'watt', 'watts', 'W', [ ], [ 'SI' ] ),

    # pressure

    'atmosphere' :
        UnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm', [ ], [ 'natural' ] ),

    'bar' :
        UnitInfo( 'pressure', 'bar', 'bars', '', [ ], [ ] ),

    'barye' :
        UnitInfo( 'pressure', 'barye', 'baryes', '', [ ], [ 'CGS' ] ),

    'mmHg' :
        UnitInfo( 'pressure', 'mmHg', 'mmHg', '', [ ], [ 'metric' ] ),

    'newton/meter^2' :
        UnitInfo( 'pressure', 'newton/meter^2', 'newtons/meter^2', 'N/m^2', [ ], [ 'SI' ] ),

    'pascal' :
        UnitInfo( 'pressure', 'pascal', 'pascals', 'Pa', [ ], [ 'SI' ] ),

    'pieze' :
        UnitInfo( 'pressure', 'pieze', 'piezes', '', [ ], [ 'MTS' ] ),

    'psi' :
        UnitInfo( 'pressure', 'pound/inch^2', 'pounds/inch^2', 'psi', [ 'lb/in^2' ], [ 'FPS' ] ),

    'torr' :
        UnitInfo( 'pressure', 'torr', 'torr', '', [ ], [ ] ),

    # radioactivity

    'becquerel' :
        UnitInfo( 'radioactivity', 'becquerel', 'becquerels', 'Bq', [ ], [ 'SI' ] ),

    'curie' :
        UnitInfo( 'radioactivity', 'curie', 'curies', 'Ci', [ ], [ 'obsolete' ] ),

    'rutherford' :
        UnitInfo( 'radioactivity', 'rutherford', 'rutherfords', 'rd', [ ], [ 'obsolete' ] ),

    # radiation_absorbed_dose

    'gray' :
        UnitInfo( 'radiation_absorbed_dose', 'gray', 'grays', 'Gy', [ ], [ 'SI' ] ),

    'joule/kilogram' :
        UnitInfo( 'radiation_absorbed_dose', 'joule/kilogram', 'joules/kilogram', 'J/kg', [ 'joule/kg', 'joules/kg', 'J/kilogram', 'J/kilograms', 'joule/kilograms', 'joules/kilograms' ], [ 'SI' ] ),

    'rad' :
        UnitInfo( 'radiation_absorbed_dose', 'rad', 'rads', '', [ ], [ 'CGS' ] ),

    # radiation_equivalent_dose

    'banana_equivalent_dose' :
        UnitInfo( 'radiation_equivalent_dose', 'banana_equivalent_dose', 'banana_equivalent_doses', '', [ 'banana' ], [ 'natural' ] ),

    'rem' :
        UnitInfo( 'radiation_equivalent_dose', 'rem', 'rems', '', [ 'roentgen_equivalent_man' ], [ 'CGS' ] ),

    'sievert' :
        UnitInfo( 'radiation_equivalent_dose', 'sievert', 'sieverts', 'Sv', [ ], [ 'SI' ] ),

    # radiation_exposure

    'coulomb/kilogram' :
        UnitInfo( 'radiation_exposure', 'coulomb/kilogram', 'coulombs/kilogram', 'C/kg', [ ], [ 'SI' ] ),

    'roentgen' :
        UnitInfo( 'radiation_exposure', 'roentgen', 'roentgens', 'R', [ 'parker' ], [ 'NIST' ] ),

    # solid_angle
    'square_arcminute' :
        UnitInfo( 'solid_angle', 'arcminute^2', 'arcminutes^2', 'arcmin^2', [ 'square_arcminutes', 'sqarcmin', 'sqarcmins', 'arcmins^2' ], [ 'mathematics' ] ),

    'square_arcsecond' :
        UnitInfo( 'solid_angle', 'arcsecond^2', 'arcseconds^2', 'arcsec^2', [ 'square_arcseconds', 'sqarcsec', 'sqarcsecs', 'arcsecs^2' ], [ 'mathematics' ] ),

    'square_degree' :
        UnitInfo( 'solid_angle', 'degree^2', 'degrees^2', 'deg^2', [ 'square_degrees', 'sqdeg' ], [ 'mathematics' ] ),

    'square_octant' :
        UnitInfo( 'solid_angle', 'octant^2', 'octants^2', '', [ 'square_octants', 'sqoctant', 'sqoctants' ], [ 'mathematics' ] ),

    'square_quadrant' :
        UnitInfo( 'solid_angle', 'quadrant^2', 'quadrants^2', '', [ 'square_quadrants', 'sqquadrant', 'sqquadrants' ], [ 'mathematics' ] ),

    'square_quintant' :
        UnitInfo( 'solid_angle', 'quintant^2', 'quintants^2', '', [ 'square_quintants', 'sqquintant', 'sqquintants' ], [ 'mathematics' ] ),

    'square_sextant' :
        UnitInfo( 'solid_angle', 'sextant^2', 'sextants^2', '', [ 'square_sextants', 'sqsextant', 'sqsextants' ], [ 'mathematics' ] ),

    'square_grad' :
        UnitInfo( 'solid_angle', 'grad^2', 'grads^2', '', [ 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'grad^2', 'grads^2', 'gon^2', 'gons^2' ], [ 'mathematics' ] ),

    'steradian' :
        UnitInfo( 'solid_angle', 'steradian', 'steradians', '', [ 'square_radian', 'square_radians', 'radian^2', 'radians^2', 'rad^2' ], [ 'SI', 'mathematics' ] ),

    # temperature

    'celsius' :
        UnitInfo( 'temperature', 'celsius', 'degrees_celsius', '', [ 'centigrade', 'degC' ], [ 'SI' ] ),

    'degree_newton' :
        UnitInfo( 'temperature', 'degree_newton', 'degrees_newton', '', [ 'newton_degree', 'newton_degrees', 'degN' ], [ 'obsolete' ] ),

    'delisle' :
        UnitInfo( 'temperature', 'delisle', 'degrees_delisle', 'De', [ 'degDe' ], [ 'obsolete' ] ),

    'fahrenheit' :
        UnitInfo( 'temperature', 'fahrenheit', 'degrees_fahrenheit', '', [ 'fahr', 'degF' ], [ 'US', 'traditional' ] ),

    'kelvin' :
        UnitInfo( 'temperature', 'kelvin', 'degrees_kelvin', 'K', [ 'degK' ], [ 'SI' ] ),

    'rankine' :
        UnitInfo( 'temperature', 'rankine', 'degrees_rankine', 'R', [ 'degR' ], [ 'obsolete' ] ),

    'reaumur' :
        UnitInfo( 'temperature', 'reaumur', 'degrees_reaumur', 'Re', [ 'degRe' ], [ 'obsolete' ] ),

    'romer' :
        UnitInfo( 'temperature', 'romer', 'degrees_romer', 'Ro', [ 'defRo' ], [ 'obsolete' ] ),

    # time

    'century' :
        UnitInfo( 'time', 'century', 'centuries', '', [ ], [ 'traditional', 'US' ] ),

    'clarke' :
        UnitInfo( 'time', 'clarke', 'clarkes', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'cowznofski' :
        UnitInfo( 'time', 'cowznofski', 'cowznofskis', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'day' :
        UnitInfo( 'time', 'day', 'days', '', [ ], [ 'traditional', 'US' ] ),

    'decade' :
        UnitInfo( 'time', 'decade', 'decades', '', [ ], [ 'traditional' ] ),

    'fortnight' :
        UnitInfo( 'time', 'fortnight', 'fortnights', '', [ ], [ 'traditional' ] ),

    'gregorian_year' :
        UnitInfo( 'time', 'gregorian_year', 'gregorian_years', '', [ '' ], [ 'traditional' ] ),

    'hour' :
        UnitInfo( 'time', 'hour', 'hours', 'hr', [ ], [ 'traditional' ] ),

    'kovac' :
        UnitInfo( 'time', 'kovac', 'kovacs', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'jiffy' :
        UnitInfo( 'time', 'jiffy', 'jiffies', '', [ ], [ 'computing' ] ),

    'lunar_day' :
        UnitInfo( 'time', 'lunar_day', 'lunar_days', '', [ 'tidal_day', 'tidal_days' ], [ 'science' ] ),

    'martin' :
        UnitInfo( 'time', 'martin', 'martins', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'microcentury' :
        UnitInfo( 'time', 'microcentury', 'microcenturies', '', [ ], [ 'humorous', 'computing' ] ),

    'microfortnight' :
        UnitInfo( 'time', 'microfortnight', 'microfortnights', '', [ ], [ 'humorous', 'computing' ] ),

    'mingo' :
        UnitInfo( 'time', 'mingo', 'mingoes', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'minute' :
        UnitInfo( 'time', 'minute', 'minutes', '', [ ], [ 'traditional' ] ),  # 'min' is already an operator

    'nanocentury' :
        UnitInfo( 'time', 'nanocentury', 'nanocenturies', '', [ ], [ 'humorous', 'computing' ] ),

    'planck_time' :
        UnitInfo( 'time', 'planck_time', 'x planck_time', 'tP', [ ], [ 'science' ] ),

    'second' :
        UnitInfo( 'time', 'second', 'seconds', '', [ ], [ 'SI', 'traditional', 'FPS' ] ),   # 'sec' is already an operator

    'shake' :
        UnitInfo( 'time', 'shake', 'shakes', '', [ ], [ 'science' ] ),

    'siderial_day' :
        UnitInfo( 'time', 'siderial_day', 'siderial_days', '', [ ], [ 'science' ] ),

    'siderial_year' :
        UnitInfo( 'time', 'siderial_year', 'siderial_years', '', [ ], [ 'science' ] ),

    'svedberg' :
        UnitInfo( 'time', 'svedberg', 'svedbergs', '', [ ], [ ] ),

    'tropical_year' :
        UnitInfo( 'time', 'tropical_year', 'tropical_years', '', [ 'solar_year', 'solar_years' ], [ 'science' ] ),

    'week' :
        UnitInfo( 'time', 'week', 'weeks', 'wk', [ 'sennight' ], [ 'traditional', 'obsolete' ] ),

    'wolverton' :
        UnitInfo( 'time', 'wolverton', 'wolvertons', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'wood' :
        UnitInfo( 'time', 'wood', 'woods', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'year' :
        UnitInfo( 'time', 'year', 'years', '', [ 'julian_year', 'julian_years' ], [ 'traditional' ] ),

    # velocity

    'meter/second' :
        UnitInfo( 'velocity', 'meter/second', 'meters/second', 'm/s', [ ], [ 'SI' ] ),

    'knot' :
        UnitInfo( 'velocity', 'knot', 'knots', '', [ ], [ 'nautical' ] ),

    'light' :    # I shouldn't need a whole extra unit for what is really an alias, but this makes life easier
        UnitInfo( 'velocity', 'speed_of_light', 'x_speed_of_light', '', [ ], [ 'natural' ] ),

    'mach' :
        UnitInfo( 'velocity', 'mach', 'mach', '', [ ], [ 'US' ] ),

    # volume

    'acre-foot' :
        UnitInfo( 'volume', 'acre*foot', 'acre-feet', 'ac*ft', [ ], [ 'US', 'traditional' ] ),

    'balthazar' :
        UnitInfo( 'volume', 'balthazar', 'balthazars', '', [ ], [ 'wine' ] ),

    'bucket' :
        UnitInfo( 'volume', 'bucket', 'buckets', '', [ ], [ 'imperial' ] ),

    'bushel' :
        UnitInfo( 'volume', 'bushel', 'bushels', 'bu', [ ], [ 'imperial' ] ),

    'chopine' :
        UnitInfo( 'volume', 'chopine', 'chopines', '', [ ], [ 'wine' ] ),

    'clavelin' :
        UnitInfo( 'volume', 'clavelin', 'clavelins', '', [ ], [ 'wine' ] ),

    'cord' :
        UnitInfo( 'volume', 'cord', 'cords', '', [ ], [ 'traditional' ] ),

    'cubic_inch' :
        UnitInfo( 'volume', 'inch^3', 'cubic_inches', 'cuin', [ 'in^3', 'inch^3', 'inches^3' ], [ 'traditional' ] ),

    'cubic_foot' :
        UnitInfo( 'volume', 'foot^3', 'cubic_feet', 'cuft', [ 'ft^3', 'foot^3', 'feet^3' ], [ 'traditional', 'FPS' ] ),

    'cubic_meter' :
        UnitInfo( 'volume', 'meter^3', 'cubic_meters', 'm^3', [ 'meter^3', 'meters^3' ], [ 'SI' ] ),

    'coomb' :
        UnitInfo( 'volume', 'coomb', 'coombs', '', [ ], [ 'imperial' ] ),

    'cup' :
        UnitInfo( 'volume', 'cup', 'cups', '', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'dash' :
        UnitInfo( 'volume', 'dash', 'dashes', '', [ ], [ 'cooking' ] ),

    'demi' :
        UnitInfo( 'volume', 'demi', 'demis', '', [ ], [ 'wine' ] ),

    'dessertspoon' :
        UnitInfo( 'volume', 'dessertspoon', 'dessertspoons', '', [ ], [ 'traditional', 'cooking' ] ),

    'dram' :
        UnitInfo( 'volume', 'dram', 'drams', '', [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ] ),

    'dry_barrel' :
        UnitInfo( 'volume', 'dry_barrel', 'dry_barrels', '', [ ], [ 'imperial' ] ),

    'dry_hogshead' :
        UnitInfo( 'volume', 'dry_hogshead', 'dry_hogsheads', '', [ ], [ 'imperial' ] ),

    'dry_gallon' :
        UnitInfo( 'volume', 'dry_gallon', 'dry_gallons', '', [ ], [ 'traditional', 'US' ] ),

    'dry_pint' :
        UnitInfo( 'volume', 'dry_pint', 'dry_pints', '', [ ], [ 'traditional', 'US' ] ),

    'dry_quart' :
        UnitInfo( 'volume', 'dry_quart', 'dry_quarts', '', [ ], [ 'traditional', 'US' ] ),

    'dry_tun' :
        UnitInfo( 'volume', 'dry_tun', 'dry_tuns', '', [ ], [ 'imperial' ] ),

    'farshimmelt_ngogn' :
        UnitInfo( 'volume', 'farshimmelt_ngogn', 'farshimmelt_ngogns', 'fn', [ 'far-ngogn' ], [ 'Potrzebie', 'humorous' ] ),

    'fifth' :
        UnitInfo( 'volume', 'fifth', 'fifths', '', [ ], [ 'wine' ] ),

    'firkin' :
        UnitInfo( 'volume', 'firkin', 'firkins', '', [ ], [ 'imperial' ] ),

    'fluid_ounce' :
        UnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', '', [ 'floz' ], [ 'traditional' ] ),

    'furshlugginer_ngogn' :
        UnitInfo( 'volume', 'furshlugginer_ngogn', 'furshlugginer_ngogns', 'Fn', [ 'Fur-ngogn' ], [ 'Potrzebie', 'humorous' ] ),

    'gallon' :
        UnitInfo( 'volume', 'gallon', 'gallons', 'gal', [ ], [ 'imperial' ] ),

    'gill' :
        UnitInfo( 'volume', 'gill', 'gills', '', [ ], [ 'imperial' ] ),

    'goliath' :
        UnitInfo( 'volume', 'goliath', 'goliaths', '', [ 'primat' ], [ 'wine' ] ),

    'hogshead' :
        UnitInfo( 'volume', 'hogshead', 'hogsheads', '', [ ], [ 'traditional', 'wine' ] ),

    'imperial' :
        UnitInfo( 'volume', 'imperial', 'imperials', '', [ ], [ 'wine' ] ),

    'imperial_bushel' :
        UnitInfo( 'volume', 'imperial_bushel', 'imperial_bushels', '', [ ], [ 'imperial' ] ),

    'imperial_butt' :
        UnitInfo( 'volume', 'imperial_butt', 'imperial_butts', '', [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial' ] ),

    'imperial_cup' :
        UnitInfo( 'volume', 'imperial_cup', 'imperial_cups', '', [ ], [ 'imperial' ] ),

    'imperial_gallon' :
        UnitInfo( 'volume', 'imperial_gallon', 'imperial_gallons', '', [ ], [ 'imperial' ] ),

    'imperial_gill' :
        UnitInfo( 'volume', 'imperial_gill', 'imperial_gills', '', [ ], [ 'imperial' ] ),

    'imperial_hogshead' :
        UnitInfo( 'volume', 'imperial_hogshead', 'imperial_hogsheads', '', [ ], [ 'imperial' ] ),

    'imperial_peck' :
        UnitInfo( 'volume', 'imperial_peck', 'imperial_pecks', '', [ ], [ 'imperial' ] ),

    'imperial_pint' :
        UnitInfo( 'volume', 'imperial_pint', 'imperial_pints', '', [ ], [ 'imperial' ] ),

    'imperial_quart' :
        UnitInfo( 'volume', 'imperial_quart', 'imperial_quarts', '', [ ], [ 'imperial' ] ),

    'jack' :
        UnitInfo( 'volume', 'jack', 'jacks', '', [ 'jackpot' ], [ 'imperial' ] ),

    'jennie' :
        UnitInfo( 'volume', 'jennie', 'jennies', '', [ ], [ 'wine' ] ),

    'jeroboam' :
        UnitInfo( 'volume', 'jeroboam', 'jeroboams', '', [ 'double_magnum' ], [ 'wine' ] ),

    'jigger' :
        UnitInfo( 'volume', 'jigger', 'jiggers', '', [ ], [ 'imperial' ] ),

    'kenning' :
        UnitInfo( 'volume', 'kenning', 'kennings', '', [ ], [ 'imperial' ] ),

    'kilderkin' :
        UnitInfo( 'volume', 'kilderkin', 'kilderkins', '', [ ], [ 'imperial' ] ),

    'liter' :
        UnitInfo( 'volume', 'liter', 'liters', 'l', [ ], [ 'SI' ] ),

    'magnum' :
        UnitInfo( 'volume', 'magnum', 'magnums', '', [ ], [ 'wine' ] ),

    'marie_jeanne' :
        UnitInfo( 'volume', 'marie_jeanne', 'marie_jeannes', '', [ ], [ 'wine' ] ),

    'melchior' :
        UnitInfo( 'volume', 'melchior', 'melchiors', '', [ ], [ 'wine' ] ),

    'melchizedek' :
        UnitInfo( 'volume', 'melchizedek', 'melchizedeks', '', [ ], [ 'wine' ] ),

    'methuselah' :
        UnitInfo( 'volume', 'methuselah', 'methuselahs', '', [ ], [ 'wine' ] ),

    'minim':
        UnitInfo( 'volume', 'minim', 'minims', 'gtt', [ 'drop' ], [ 'traditional' ] ),

    'mordechai' :
        UnitInfo( 'volume', 'mordechai', 'mordechais', '', [ ], [ 'wine' ] ),

    'nebuchadnezzar' :
        UnitInfo( 'volume', 'nebuchadnezzar', 'nebuchadnezzars', '', [ ], [ 'wine' ] ),

    'ngogn' :
        UnitInfo( 'volume', 'ngogn', 'ngogns', 'n', [ ], [ 'Potrzebie', 'humorous' ] ),

    'oil_barrel' :
        UnitInfo( 'volume', 'oil_barrel', 'oil_barrels', 'bbl', [ ], [ 'US' ] ),

    'peck' :
        UnitInfo( 'volume', 'peck', 'pecks', 'pk', [ ], [ 'imperial' ] ),

    'piccolo' :
        UnitInfo( 'volume', 'piccolo', 'piccolos', '', [ ], [ 'wine' ] ),

    'pinch' :
        UnitInfo( 'volume', 'pinch', 'pinches', '', [ ], [ 'traditional', 'cooking' ] ),

    'pin' :
        UnitInfo( 'volume', 'pin', 'pins', '', [ ], [ 'imperial' ] ),

    'pint' :
        UnitInfo( 'volume', 'pint', 'pints', 'pt', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'pipe' :
        UnitInfo( 'volume', 'pipe', 'pipes', '', [ 'butt', 'butts' ], [ 'imperial' ] ),

    'pony' :
        UnitInfo( 'volume', 'pony', 'ponies', '', [ ], [ 'imperial' ] ),

    'pottle' :
        UnitInfo( 'volume', 'pottle', 'pottles', '', [ ], [ 'imperial' ] ),

    'puncheon' :
        UnitInfo( 'volume', 'puncheon', 'puncheons', '', [ 'tertian', 'tertians' ], [ 'wine' ] ),

    'quart' :
        UnitInfo( 'volume', 'quart', 'quart', '', [ ], [ 'US' ] ),

    'rehoboam' :
        UnitInfo( 'volume', 'rehoboam', 'rehoboams', '', [ ], [ 'wine' ] ),

    'rundlet' :
        UnitInfo( 'volume', 'rundlet', 'rundlets', '', [ ], [ 'imperial', 'wine' ] ),

    'salmanazar' :
        UnitInfo( 'volume', 'salmanazar', 'salmanazars', '', [ ], [ 'wine' ] ),

    'scruple' :
        UnitInfo( 'volume', 'scruple', 'scruples', '', [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ] ),

    'smidgen' :
        UnitInfo( 'volume', 'smidgen', 'smidgens', '', [ ], [ 'traditional', 'cooking' ] ),

    'solomon' :
        UnitInfo( 'volume', 'solomon', 'solomons', '', [ ], [ 'wine' ] ),

    'sovereign' :
        UnitInfo( 'volume', 'sovereign', 'sovereigns', '', [ ], [ 'wine' ] ),

    'standard' :
        UnitInfo( 'volume', 'standard', 'standards', '', [ ], [ 'wine' ] ),

    'stere' :
        UnitInfo( 'volume', 'stere', 'steres', 'st', [ ], [ 'metric', 'obsolete' ] ),  # ... but not SI

    'strike' :
        UnitInfo( 'volume', 'strike', 'strikes', '', [ ], [ 'imperial' ] ),

    'tablespoon' :
        UnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'teaspoon' :
        UnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'tenth' :
        UnitInfo( 'volume', 'tenth', 'tenths', '', [ ], [ 'wine' ] ),

    'tierce' :
        UnitInfo( 'volume', 'tierce', 'tierces', '', [ ], [ 'wine', 'imperial' ] ),

    'tun' :
        UnitInfo( 'volume', 'tun', 'tuns', '', [ ], [ 'imperial' ] ),

    'wine_barrel' :
        UnitInfo( 'volume', 'wine_barrel', 'wine_barrels', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_butt' :
        UnitInfo( 'volume', 'wine_butt', 'wine_butts', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_gallon' :
        UnitInfo( 'volume', 'wine_gallon', 'wine_gallons', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_hogshead' :
        UnitInfo( 'volume', 'wine_hogshead', 'wine_hogsheads', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_pipe' :
        UnitInfo( 'volume', 'wine_pipe', 'wine_pipes', '', [ 'wine_butt', 'wine_butts' ], [ 'imperial' ] ),

    'wine_tun' :
        UnitInfo( 'volume', 'wine_tun', 'wine_tuns', '', [ ], [ 'imperial', 'wine' ] ),
}


#//******************************************************************************
#//
#//  metricUnits
#//
#//  ... or any units that should get the SI prefixes
#//
#//  ( name, plural name, abbreviation, aliases, plural aliases )
#//
#//******************************************************************************

metricUnits = [
    ( 'ampere',             'amperes',          'A',    [ 'amp' ], [ 'amps' ] ),
    ( 'are',                'ares',             'a',    [ ], [ ] ),
    ( 'becquerel',          'becquerels',       'Bq',   [ ], [ ] ),
    ( 'blintz',             'blintzes',         'bl',   [ ], [ ] ),
    ( 'coulomb',            'coulombs',         'C',    [ ], [ ] ),
    ( 'calorie',            'calories',         'cal',  [ 'cal' ], [ 'cals' ] ),
    ( 'electronvolt',       'electronvolts',    'eV',   [ ], [ ] ),
    ( 'farad',              'farad',            'F',    [ ], [ ] ),
    ( 'gram-equivalent',    'grams-equivalent', 'gE',   [ 'gram-energy', 'gramme-energy' ], [ 'grams-energy', 'grammes-energy' ] ),
    ( 'gram',               'grams',            'g',    [ 'gramme' ], [ 'grammes' ] ),
    ( 'gram-force',         'grams-force',      'gf',   [ 'gramme-force' ], [ 'grammes-force' ] ),
    ( 'henry',              'henries',          'H',    [ ], [ ] ),
    ( 'joule',              'joules',           'J',    [ ], [ ] ),
    ( 'kelvin',             'kelvins',          'K',    [ ], [ ] ),
    ( 'liter',              'liters',           'l',    [ 'litre' ], [ 'litres' ] ),
    ( 'light-year',         'light-years',      'ly',   [ ], [ ] ),
    ( 'lux',                'lux',              'lx',   [ ], [ ] ),
    ( 'meter',              'meters',           'm',    [ 'metre' ], [ 'metres' ] ),
    ( 'newton',             'newtons',          'N',    [ ], [ ] ),
    ( 'ngogn',              'ngogns',           'n',    [ ], [ ] ),
    ( 'ohm',                'ohms',             'O',    [ ], [ ] ),
    ( 'parsec',             'parsecs',          'pc',   [ ], [ ] ),
    ( 'pascal',             'pascals',          'Pa',   [ ], [ ] ),
    ( 'pond',               'ponds',            'p',    [ ], [ ] ),
    ( 'potrzebie',          'potrzebies',       'pz',   [ ], [ ] ),
    ( 'rem',                'rems',             'rem',  [ ], [ ] ),
    ( 'second',             'seconds',          's',    [ ], [ ] ),
    ( 'siemens',            'siemens',          'S',    [ 'mho' ], [ 'mhos' ] ),
    ( 'sievert',            'sieverts',         'Sv',   [ ], [ ] ),
    ( 'stere',              'steres',           'st',   [ ], [ ] ),
    ( 'tesla',              'teslas',           'T',    [ ], [ ] ),
    ( 'ton_of_TNT',         'tons_of_TNT',      'tTNT', [ ], [ ] ),
    ( 'volt',               'volts',            'V',    [ ], [ ] ),
    ( 'watt',               'watts',            'W',    [ ], [ ] ),
    ( 'watt-second',        'watt-seconds',     'Ws',   [ ], [ ] ),
]


#//******************************************************************************
#//
#//  dataUnits
#//
#//  ... or any units that should get the SI prefixes (positive powers of 10)
#//  and the binary prefixes
#//
#//  ( name, plural name, abbreviation, aliases, plural aliases )
#//
#//******************************************************************************

dataUnits = [
    ( 'bit',            'bits',             'b',    [ ], [ ] ),
    ( 'bit/second',     'bits/second',      'bps',  [ ], [ ] ),
    ( 'byte',           'bytes',            'B',    [ ], [ ] ),
    ( 'byte/second',    'bytes/second',     'Bps',  [ ], [ ] ),
]


#//******************************************************************************
#//
#//  timeUnits
#//
#//******************************************************************************

timeUnits = [
    ( 'minute',     'minutes',      'm',        '60' ),
    ( 'hour',       'hours',        'h',        '3600' ),
    ( 'day',        'days',         'd',        '86400' ),
    ( 'year',       'years',        'y',        '31557600' ),   # Julian year == 365.25 days
]


#//******************************************************************************
#//
#//  metricPrefixes
#//
#//  ( name, abbreviation, power of 10 )
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  dataPrefixes
#//
#//  ( name, abbreviation, power of 10 )
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  binaryPrefixes
#//
#//  ( name, abbreviation, power of 2 )
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  conversion constants
#//
#//******************************************************************************

speedOfLight = '299792458'   # in m/s by definition


#//******************************************************************************
#//
#//  unitConversionMatrix
#//
#//  ( first unit, second unit, conversion factor )
#//
#//******************************************************************************

unitConversionMatrix = {
    ( 'aa_battery',            'joule' )                                : '15400',
    ( 'abampere',              'ampere' )                               : '10',
    ( 'abcoulomb',             'coulomb' )                              : '10',
    ( 'abfarad',               'farad' )                                : '1.0e9',
    ( 'abmho',                 'siemens' )                              : '1.0e9',
    ( 'acre',                  'square_yard' )                          : '4840',
    ( 'acre-foot',             'cubic_foot' )                           : '43560',
    ( 'aln',                   'inch' )                                 : '23.377077865',
    ( 'ampere',                'coulomb/second' )                       : '1',
    ( 'ampere',                'statampere' )                           : speedOfLight,
    ( 'arcminute',             'arcsecond' )                            : '60',
    ( 'are',                   'square_meter' )                         : '100',
    ( 'arpent',                'foot' )                                 : '192',
    ( 'astronomical_unit',     'meter' )                                : '149597870700',
    ( 'atmosphere',            'pascal' )                               : '101325',
    ( 'balthazar',             'liter' )                                : '12.0',
    ( 'ban',                   'nat' )                                  : str( log( 10 ) ),
    ( 'banana_equivalent_dose', 'sievert' )                             : '9.8e-8',
    ( 'bar',                   'pascal' )                               : '1.0e5',
    ( 'barleycorn',            'poppyseed' )                            : '4',
    ( 'becquerel',             'curie' )                                : '3.7e10',
    ( 'billion',               'unity' )                                : '1.0e9',
    ( 'bit',                   'nat' )                                  : str( log( 2 ) ),
    ( 'blintz',                'farshimmelt_blintz' )                   : '1.0e5',
    ( 'blintz',                'furshlugginer_blintz' )                 : '1.0e-6',
    ( 'blintz',                'gram' )                                 : '36.42538631',
    ( 'btu',                   'joule' )                                : '1054.5',
    ( 'bucket',                'gallon' )                               : '4',
    ( 'bushel',                'peck' )                                 : '4',
    ( 'byte',                  'bit' )                                  : '8',
    ( 'calorie',               'joule' )                                : '4.184',
    ( 'carat',                 'grain' )                                : str( fadd( 3, fdiv( 1, 6 ) ) ),
    ( 'carucate',              'acre' )                                 : '120',
    ( 'carucate',              'bovate' )                               : '8',
    ( 'centillion',            'unity' )                                : '1.0e303',
    ( 'century',               'microcentury' )                         : '1.0e6',
    ( 'century',               'nanocentury' )                          : '1.0e9',
    ( 'century',               'year' )                                 : '100',
    ( 'chain',                 'yard' )                                 : '22',
    ( 'chopine',               'liter' )                                : '0.25',
    ( 'clarke',                'day' )                                  : '1',
    ( 'clarke',                'wolverton' )                            : '1.0e6',
    ( 'clausius',              'joule/kelvin' )                         : '4186.8',
    ( 'clavelin',              'liter' )                                : '0.62',
    ( 'coomb',                 'strike' )                               : '2',
    ( 'cord',                  'cubic_foot' )                           : '128',
    ( 'coulomb',               'ampere-second' )                        : '1',
    ( 'coulomb',               'farad-volt' )                           : '1',
    ( 'coulomb/farad',         'volt' )                                 : '1',
    ( 'coulomb/kilogram',      'roentgen' )                             : '3876',
    ( 'coulomb/volt',          'farad' )                                : '1',
    ( 'cowznofski',            'mingo' )                                : '10',
    ( 'cubic_meter',           'liter' )                                : '1000',
    ( 'cubit',                 'inch' )                                 : '18',
    ( 'cup',                   'dram' )                                 : '64',
    ( 'cup',                   'fluid_ounce' )                          : '8',
    ( 'cup',                   'gill' )                                 : '2',
    ( 'day',                   'hour' )                                 : '24',
    ( 'decade',                'year' )                                 : '10',
    ( 'decillion',             'unity' )                                : '1.0e33',
    ( 'degree',                'arcminute' )                            : '60',
    ( 'demi',                  'liter' )                                : '0.375',
    ( 'dessertspoon',          'teaspoon' )                             : '2',
    ( 'dozen',                 'unity' )                                : '12',
    ( 'dram',                  'scruple' )                              : '3',
    ( 'dry_barrel',            'bushel' )                               : '4',
    ( 'dry_barrel',            'cubic_inch' )                           : '7056',
    ( 'dry_gallon',            'dry_quart' )                            : '4',
    ( 'dry_hogshead',          'dry_barrel' )                           : '2',
    ( 'dry_pint',              'cubic_inch' )                           : '33.6003125',
    ( 'dry_quart',             'dry_pint' )                             : '2',
    ( 'dry_tun',               'dry_hogshead' )                         : '4',
    ( 'dword',                 'bit' )                                  : '32',
    ( 'electron_charge',       'coulomb' )                              : '1.602176565e-19',
    ( 'electron_rest_mass',    'gram' )                                 : '9.10938291e-28',
    ( 'ell',                   'inch' )                                 : '45',
    ( 'famn',                  'aln' )                                  : '3',
    ( 'farad',                 'jar' )                                  : '9.0e8',
    ( 'farad',                 'statfarad' )                            : '898755178736.5',
    ( 'faraday',               'coulomb' )                              : '96485.3383',
    ( 'fathom',                'foot' )                                 : '6',
    ( 'finger',                'inch' )                                 : '4.5',
    ( 'fingerbreadth',         'inch' )                                 : '0.75',
    ( 'firkin',                'gallon' )                               : '9',
    ( 'firkin',                'pin' )                                  : '2',
    ( 'fluid_ounce',           'dram' )                                 : '8',
    ( 'fluid_ounce',           'tablespoon' )                           : '2',
    ( 'foot',                  'inch' )                                 : '12',
    ( 'footcandle',            'lumen/foot^2' )                         : '1',
    ( 'footcandle',            'lux' )                                  : '10.763910417',           # (m/ft)^2
    ( 'footlambert',           'candela/meter^2' )                      : '3.42625909963539052691', # 1/pi cd/ft^2
    ( 'fortnight',             'day' )                                  : '14',
    ( 'fortnight',             'microfortnight' )                       : '1.0e6',
    ( 'furlong',               'yard' )                                 : '220',
    ( 'gallon',                'fifth' )                                : '5',
    ( 'gallon',                'quart' )                                : '4',
    ( 'gallon_of_gasoline',    'gallon_of_ethanol' )                    : '1.425',  # approx.
    ( 'gallon_of_gasoline',    'joule' )                                : '1.2e8',  # approx. obviously
    ( 'gauss',                 'maxwell/centimeter^2' )                 : '1',
    ( 'goliath',               'liter' )                                : '27.0',
    ( 'googol',                'unity' )                                : '1.0e100',
    ( 'grad',                  'degree' )                               : '0.9',
    ( 'gram',                  'dalton' )                               : '1.66053e-27',
    ( 'gram',                  'planck_mass' )                          : '45940.892447777',
    ( 'gram-equivalent',       'joule' )                                : str( fdiv( power( mpf( speedOfLight ), 2 ), 1000 ) ),
    ( 'gray',                  'joule/kilogram' )                       : '1',
    ( 'gray',                  'rad' )                                  : '100',
    ( 'greek_cubit',           'inch' )                                 : '18.22',
    ( 'gregorian_year',        'day' )                                  : '365.2425',
    ( 'handbreadth',           'inch' )                                 : '3',
    ( 'hartree',               'rydberg' )                              : '2',
    ( 'hefnerkerze',           'candela' )                              : '0.920',  # approx.
    ( 'henry',                 'abhenry' )                              : '1.0e9',
    ( 'henry',                 'weber/ampere' )                         : '1',
    ( 'homestead',             'acre' )                                 : '160',
    ( 'horsepower',            'watt' )                                 : '745.69987158227022',
    ( 'horsepower-second',     'joule' )                                : '745.69987158227022',
    ( 'hour',                  'minute' )                               : '60',
    ( 'hundred',               'unity' )                                : '100',
    ( 'imperial_bushel',       'kenning' )                              : '2',
    ( 'imperial_butt',         'imperial_hogshead' )                    : '2',
    ( 'imperial_cup',          'imperial_gill' )                        : '2',
    ( 'imperial_gallon',       'pottle' )                               : '2',
    ( 'imperial_gill',         'jack' )                                 : '2',
    ( 'imperial_hogshead',     'coomb' )                                : '2',
    ( 'imperial_peck',         'imperial_quart' )                       : '2',
    ( 'imperial_pint',         'imperial_cup' )                         : '2',
    ( 'imperial_quart',        'imperial_pint' )                        : '2',
    ( 'inch',                  'barleycorn' )                           : '3',
    ( 'inch',                  'caliber' )                              : '100',
    ( 'inch',                  'gutenberg' )                            : '7200',
    ( 'inch',                  'meter' )                                : '0.0254',
    ( 'inch',                  'mil' )                                  : '1000',
    ( 'inch',                  'pica' )                                 : '6',
    ( 'inch',                  'point' )                                : '72',
    ( 'inch',                  'twip' )                                 : '1440',
    ( 'jack',                  'tablespoon' )                           : '5',
    ( 'jennie',                'liter' )                                : '0.5',
    ( 'jeroboam',              'liter' )                                : '3.0',  # some French regions use 4.5
    ( 'jigger',                'pony' )                                 : '2',
    ( 'joule',                 'electronvolt' )                         : '6.24150974e18',
    ( 'joule',                 'erg' )                                  : '1.0e7',
    ( 'joule',                 'kilogram-meter^2/second^2' )            : '1',
    ( 'joule/second',          'watt' )                                 : '1',
    ( 'ken',                   'inch' )                                 : '83.4',
    ( 'kenning',               'imperial_peck' )                        : '2',
    ( 'kilderkin',             'firkin' )                               : '2',
    ( 'kip',                   'pound' )                                : '1000',
    ( 'kovac',                 'wolverton' )                            : '10',
    ( 'lambert',               'candela/meter^2' )                      : str( fdiv( 10000, pi ) ),
    ( 'league',                'mile' )                                 : '3',
    ( 'light',                 'meter/second' )                         : speedOfLight,
    ( 'light-second',          'meter' )                                : speedOfLight,
    ( 'light-year',            'light-second' )                         : '31557600',
    ( 'link',                  'inch' )                                 : '7.92',
    ( 'liter',                 'ngogn' )                                : '86.2477899004',
    ( 'long_cubit',            'inch' )                                 : '21',
    ( 'long_reed',             'foot' )                                 : '10.5',
    ( 'lunar_day',             'minute' )                               : '1490',
    ( 'lux',                   'lumen/meter^2' )                        : '1',
    ( 'lux',                   'nox' )                                  : '1000',
    ( 'mach',                  'meter/second' )                         : '295.0464',
    ( 'magnum',                'liter' )                                : '1.5',
    ( 'marathon',              'yard' )                                 : '46145',
    ( 'marie_jeanne',          'liter' )                                : '2.25',
    ( 'martin',                'kovac' )                                : '100',
    ( 'maxwell',               'gauss*centimeter^2' )                   : '1',
    ( 'melchior',              'liter' )                                : '18.0',
    ( 'melchizedek',           'liter' )                                : '30.0',
    ( 'meter',                 'angstrom' )                             : '1.0e10',
    ( 'meter',                 'kyu' )                                  : '4000',
    ( 'meter',                 'micron' )                               : '1.0e6',
    ( 'meter/second',          'knot' )                                 : '1.943844492',
    ( 'methuselah',            'liter' )                                : '6.0',
    ( 'mile',                  'foot' )                                 : '5280',
    ( 'million',               'unity' )                                : '1.0e6',
    ( 'mingo',                 'clarke' )                               : '10',
    ( 'minute',                'second' )                               : '60',
    ( 'mmHg',                  'pascal' )                               : '133.3224',        # approx.
    ( 'mordechai',             'liter' )                                : '9.0',
    ( 'nail',                  'inch' )                                 : '2.25',
    ( 'nat',                   'joule/kelvin' )                         : '1.380650e-23',
    ( 'nautical_mile',         'meter' )                                : '1852',
    ( 'nebuchadnezzar',        'liter' )                                : '15.0',
    ( 'newton',                'dyne' )                                 : '1.0e5',
    ( 'newton',                'joule/meter' )                          : '1',
    ( 'newton',                'pond' )                                 : '101.97161298',
    ( 'newton',                'poundal' )                              : '7.233013851',
    ( 'newton/meter^2',        'pascal' )                               : '1',
    ( 'ngogn',                 'farshimmelt_ngogn' )                    : '1.0e5',
    ( 'ngogn',                 'furshlugginer_ngogn' )                  : '1.0e-6',
    ( 'nibble',                'bit' )                                  : '4',
    ( 'nit',                   'apostilb' )                             : str( pi ),
    ( 'nit',                   'candela/meter^2' )                      : '1',
    ( 'nit',                   'lambert' )                              : str( fdiv( pi, 10000 ) ),
    ( 'nonillion',             'unity' )                                : '1.0e30',
    ( 'nyp',                   'bit' )                                  : '2',
    ( 'octant',                'degree' )                               : '45',
    ( 'octillion',             'unity' )                                : '1.0e27',
    ( 'oersted',               'ampere/meter' )                         : '79.5774715',
    ( 'ohm',                   '1/siemens' )                            : '1',
    ( 'ohm',                   'abohm' )                                : '1e9',
    ( 'ohm',                   'german_mile' )                          : '57.44',
    ( 'ohm',                   'jacobi' )                               : '0.6367',
    ( 'ohm',                   'joule-second/coulomb^2' )               : '1',
    ( 'ohm',                   'joule/second-ampere^2' )                : '1',
    ( 'ohm',                   'kilogram-meter^2/second^3-ampere^2' )   : '1',
    ( 'ohm',                   'matthiessen' )                          : '13.59',
    ( 'ohm',                   'meter^2-kilogram/second-couloumb^2' )   : '1',
    ( 'ohm',                   'second/farad' )                         : '1',
    ( 'ohm',                   'varley' )                               : '25.61',
    ( 'ohm',                   'volt/ampere' )                          : '1',
    ( 'ohm',                   'watt/ampere^2' )                        : '1',
    ( 'oil_barrel',            'gallon' )                               : '42',
    ( 'ounce',                 'gram' )                                 : '28.349523125',
    ( 'oword',                 'bit' )                                  : '128',
    ( 'parsec',                'light-year' )                           : '3.261563776971',
    ( 'pascal',                'barye' )                                : '10',
    ( 'peck',                  'dry_gallon' )                           : '2',
    ( 'perch',                 'foot' )                                 : '16.5',
    ( 'pferdestarke',          'watt' )                                 : '735.49875',
    ( 'phot',                  'lux' )                                  : '10000',
    ( 'piccolo',               'liter' )                                : '0.1875',
    ( 'pieze',                 'pascal' )                               : '1000',
    ( 'planck_charge',         'coulomb' )                              : '1.875545956e-18',
    ( 'planck_energy',         'joule' )                                : '1.956e9',
    ( 'planck_length',         'meter' )                                : '1.616199e-35',
    ( 'planck_time',           'second' )                               : '5.39106e-44',
    ( 'poncelet',              'watt' )                                 : '980.665',
    ( 'pony',                  'dram' )                                 : '6',
    ( 'potrzebie',             'farshimmelt_potrzebie' )                : '1.0e5',
    ( 'potrzebie',             'furshlugginer_potrzebie' )              : '1.0e-6',
    ( 'potrzebie',             'meter' )                                : '0.002263348517438173216473',  # see Mad #33
    ( 'pottle',                'imperial_quart' )                       : '2',
    ( 'pound',                 'grain' )                                : '7000',
    ( 'pound',                 'ounce' )                                : '16',
    ( 'pound',                 'sheet' )                                : '700',
    ( 'psi',                   'pascal' )                               : '6894.757',        # approx.
    ( 'quadrant',              'degree' )                               : '90',
    ( 'quadrillion',           'unity' )                                : '1.0e15',
    ( 'quart',                 'cup' )                                  : '4',
    ( 'quart',                 'liter' )                                : '0.946352946',
    ( 'quart',                 'pint' )                                 : '2',
    ( 'quintant',              'degree' )                               : '72',
    ( 'quintillion',           'unity' )                                : '1.0e18',
    ( 'qword',                 'bit' )                                  : '64',
    ( 'radian',                'degree' )                               : str( fdiv( 180, pi ) ),
    ( 'reed',                  'foot' )                                 : '9',
    ( 'rehoboam',              'liter' )                                : '4.5',
    ( 'rod',                   'foot' )                                 : '16.5',
    ( 'rood',                  'square_yard' )                          : '1210',
    ( 'rope',                  'foot' )                                 : '20',
    ( 'rutherford',            'becquerel' )                            : '1.0e6',
    ( 'rydberg',               'joule' )                                : '2.179872e-18',
    ( 'salmanazar',            'liter' )                                : '9.0',
    ( 'score',                 'unity' )                                : '20',
    ( 'scruple',               'minim' )                                : '20',
    ( 'second',                'jiffy' )                                : '100',
    ( 'second',                'shake' )                                : '1.0e8',
    ( 'second',                'svedberg' )                             : '1.0e13',
    ( 'section',               'acre' )                                 : '640',
    ( 'septillion',            'unity' )                                : '1.0e24',
    ( 'sextant',               'degree' )                               : '60',
    ( 'sextillion',            'unity' )                                : '1.0e21',
    ( 'siderial_day',          'second' )                               : '86164.1',
    ( 'siderial_year',         'day' )                                  : '365.256363',
    ( 'siemens',               'ampere/volt' )                          : '1',
    ( 'siemens',               'kilogram-meter^2/second^3-ampere^2' )   : '1',
    ( 'sievert',               'rem' )                                  : '100',
    ( 'skot',                  'bril' )                                 : '1.0e4',
    ( 'skot',                  'lambert' )                              : '1.0e7',
    ( 'slug',                  'pound' )                                : '32.174048556',
    ( 'smoot',                 'inch' )                                 : '67',
    ( 'solomon',               'liter' )                                : '20.0',
    ( 'sovereign',             'liter' )                                : '25.0',
    ( 'span',                  'inch' )                                 : '9',
    ( 'square_arcminute',      'square_arcsecond' )                     : '3600',
    ( 'square_degree',         'square_arcminute' )                     : '3600',
    ( 'square_meter',          'barn' )                                 : '1.0e28',
    ( 'square_meter',          'outhouse' )                             : '1.0e34',
    ( 'square_meter',          'shed' )                                 : '1.0e52',
    ( 'square_octant',         'square_degree' )                        : '2025',
    ( 'square_quadrant',       'square_degree' )                        : '8100',
    ( 'square_sextant',        'square_degree' )                        : '3600',
    ( 'standard',              'liter' )                                : '0.75',
    ( 'standard_gravity',      'galileo' )                              : '980.6650',
    ( 'standard_gravity',      'meter/second^2' )                       : '9.80665',
    ( 'statcoulomb',           'coulomb' )                              : '3.335641e-10',  # 0.1A*m/c, approx.
    ( 'statcoulomb',           'franklin' )                             : '1',
    ( 'stathenry',             'henry' )                                : '898755178740',
    ( 'statmho',               'siemens' )                              : '8.99e11',
    ( 'statohm',               'ohm' )                                  : '898755178740',
    ( 'statvolt',              'volt' )                                 : str( fdiv( mpf( speedOfLight ), mpf( '1.0e6' ) ) ),
    ( 'steradian',             'square_degree' )                        : str( power( fdiv( pi, 180 ), 2 ) ),
    ( 'steradian',             'square_grad' )                          : str( power( fdiv( pi, 200 ), 2 ) ),
    ( 'sthene',                'newton' )                               : '1000',
    ( 'stilb',                 'candela/meter^2' )                      : '10000',
    ( 'stone',                 'pound' )                                : '14',
    ( 'stone_us',              'pound' )                                : '12.5',
    ( 'strike',                'imperial_bushel' )                      : '2',
    ( 'tablespoon',            'teaspoon' )                             : '3',
    ( 'teaspoon',              'dash' )                                 : '8',
    ( 'teaspoon',              'pinch' )                                : '16',
    ( 'teaspoon',              'smidgen' )                              : '32',
    ( 'tenth',                 'liter' )                                : '0.378',
    ( 'tesla',                 'gauss' )                                : '10000',
    ( 'tesla',                 'kilogram/ampere-second^2' )             : '1',
    ( 'tesla',                 'weber/meter^2' )                        : '1',
    ( 'thousand',              'unity' )                                : '100',
    ( 'ton',                   'pound' )                                : '2000',
    ( 'tonne',                 'gram' )                                 : '1.0e6',
    ( 'ton_of_TNT',            'joule' )                                : '4.184e9',
    ( 'torr',                  'mmHg' )                                 : '1',
    ( 'township',              'acre' )                                 : '23040',
    ( 'trillion',              'unity' )                                : '1.0e12',
    ( 'trit',                  'nat' )                                  : str( log( 3 ) ),
    ( 'tropical_year',         'day' )                                  : '365.24219',
    ( 'troy_ounce',            'gram' )                                 : '31.1034768',
    ( 'troy_pound',            'pound' )                                : '12',
    ( 'tryte',                 'trit' )                                 : '6',   # as defined by the Setun computer
    ( 'virgate',               'bovate' )                               : '30',
    ( 'volt',                  'abvolt' )                               : '1.0e8',
    ( 'von_klitzing_constant', 'ohm' )                                  : '25812.807557',
    ( 'watt',                  'erg/second' )                           : '1.0e7',
    ( 'watt',                  'kilogram-meter^2/second^3' )            : '1',
    ( 'watt',                  'newton-meter/second' )                  : '1',
    ( 'watt-second',           'joule' )                                : '1',
    ( 'weber',                 'maxwell' )                              : '1.0e8',
    ( 'weber',                 'tesla*meter^2' )                        : '1',
    ( 'weber',                 'unit_pole' )                            : '7957747.154594',
    ( 'weber',                 'volt-second' )                          : '1',
    ( 'week',                  'day' )                                  : '7',
    ( 'wey',                   'pound' )                                : '252',
    ( 'wine_barrel',           'wine_gallon' )                          : '31.5',
    ( 'wine_butt',             'wine_gallon' )                          : '126',
    ( 'wine_gallon',           'gallon' )                               : '1',
    ( 'wine_hogshead',         'gallon' )                               : '63',
    ( 'wine_tun',              'gallon' )                               : '252',
    ( 'wine_tun',              'puncheon' )                             : '3',
    ( 'wine_tun',              'rundlet' )                              : '14',
    ( 'wine_tun',              'tierce' )                               : '6',
    ( 'wine_tun',              'wine_pipe' )                            : '2',
    ( 'wood',                  'martin' )                               : '100',
    ( 'word',                  'bit' )                                  : '16',
    ( 'yard',                  'foot' )                                 : '3',
    ( 'year',                  'day' )                                  : '365.25',   # Julian year = 365 and 1/4 days
}


#//******************************************************************************
#//
#//  massTable
#//
#//  used in estimateMass( )
#//
#//  grams : description
#//
#//******************************************************************************

massTable = {
    mpf( '0.003' )      : 'an average ant',
    mpf( '7.0e4' )      : 'an average human',
    mpf( '5.5e6' )      : 'an average male African bush elephant',
    mpf( '4.39985e8' )  : 'the takeoff weight of a Boeing 747-8',
}


#//******************************************************************************
#//
#//  lengthTable
#//
#//  used in estimateLength( )
#//
#//  meters : description
#//
#//******************************************************************************

lengthTable = {
    '1' : 'a long thing'
}


#//******************************************************************************
#//
#//  volumeTable
#//
#//  used in estimateVolume( )
#//
#//  liters : description
#//
#//******************************************************************************

volumeTable = {
    '1' : 'a voluminous thing'
}


#//******************************************************************************
#//
#//  makeMetricUnit
#//
#//******************************************************************************

def makeMetricUnit( prefix, unit ):
    # special case because the standard is inconsistent
    if ( unit == 'ohm' ) and ( prefix == 'giga' ):
        return 'gigaohm'
    elif ( unit[ 0 ] == 'o' ) and ( prefix[ -1 ] in 'oa' ):
        return prefix[ : -1 ] + unit
    elif unit[ 0 ] == 'a' and ( ( prefix[ -1 ] == 'a' ) or ( prefix[ -3 : ] == 'cto' ) ):
        return prefix[ : -1 ] + unit
    else:
        return prefix + unit


#//******************************************************************************
#//
#//  makeUnitTypeTable
#//
#//  maps each unit type to a list of units with that type
#//
#//******************************************************************************

def makeUnitTypeTable( unitOperators ):
    unitTypeTable = { }

    for unitType in basicUnitTypes:
        unitTypeTable[ unitType ] = [ ]

    for unit in unitOperators:
        unitTypeTable[ unitOperators[ unit ].unitType ].append( unit )

    return unitTypeTable


#//******************************************************************************
#//
#//  makeAliases
#//
#//******************************************************************************

def makeAliases( ):
    newAliases = { }

    for metricUnit in metricUnits:
        newAliases[ metricUnit[ 2 ] ] = metricUnit[ 0 ]

        for prefix in metricPrefixes:
            unit = makeMetricUnit( prefix[ 0 ], metricUnit[ 0 ] )
            pluralUnit = makeMetricUnit( prefix[ 0 ], metricUnit[ 1 ] )

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit                  # add plural alias

            newAliases[ prefix[ 1 ] + metricUnit[ 2 ] ] = unit   # add SI abbreviation alias

            for alternateUnit in metricUnit[ 3 ]:                # add alternate spelling alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

            for alternateUnit in metricUnit[ 4 ]:                # add alternate spelling plural alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

    for dataUnit in dataUnits:
        newAliases[ dataUnit[ 2 ] ] = dataUnit[ 0 ]

        for prefix in dataPrefixes:
            unit = prefix[ 0 ] + dataUnit[ 0 ]
            pluralUnit = prefix[ 0 ] + dataUnit[ 1 ]

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit                # add plural alias

            newAliases[ prefix[ 1 ] + dataUnit[ 2 ] ] = unit   # add SI abbreviation alias

            for alternateUnit in dataUnit[ 3 ]:                # add alternate spelling alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

            for alternateUnit in dataUnit[ 4 ]:                # add alternate spelling plural alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

        for prefix in binaryPrefixes:
            unit = prefix[ 0 ] + dataUnit[ 0 ]
            pluralUnit = prefix[ 0 ] + dataUnit[ 1 ]

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit                # add plural alias

            newAliases[ prefix[ 1 ] + dataUnit[ 2 ] ] = unit   # add SI abbreviation alias

            for alternateUnit in dataUnit[ 3 ]:                # add alternate spelling alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

            for alternateUnit in dataUnit[ 4 ]:                # add alternate spelling plural alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]
        newAliases[ unitInfo.plural ] = unit

        for alias in unitInfo.aliases:
            newAliases[ alias ] = unit

        if unitInfo.abbrev != '':
            newAliases[ unitInfo.abbrev ] = unit

    #for i in newAliases:
    #    print( i, newAliases[ i ] )
    return newAliases


#//******************************************************************************
#//
#//  expandMetricUnits
#//
#//  Every metric unit needs to be permuted for all SI power types.  We need to
#//  create conversions for each new type, as well as aliases.
#//
#//******************************************************************************

def expandMetricUnits( newAliases ):
    # expand metric measurements for all prefixes
    newConversions = { }

    for metricUnit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], metricUnit[ 0 ] )
            newPlural = makeMetricUnit( prefix[ 0 ], metricUnit[ 1 ] )

            # constuct unit operator info
            unitOperators[ newName ] = \
                UnitInfo( unitOperators[ metricUnit[ 0 ] ].unitType, newName, newPlural,
                                         prefix[ 1 ] + metricUnit[ 2 ], [ ], [ 'SI' ] )

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, metricUnit[ 0 ] ) ] = str( newConversion )
            newConversion = fdiv( 1, newConversion )
            unitConversionMatrix[ ( metricUnit[ 0 ], newName ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == metricUnit[ 0 ] ) or ( op2 == metricUnit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == metricUnit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fdiv( oldConversion, newConversion ) )
                    elif op2 == metricUnit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fmul( oldConversion, newConversion ) )

            if unitOperators[ metricUnit[ 0 ] ].unitType == 'length':
                newUnitInfo, newUnitAliases = makeAreaOperator( newName, newPlural )

                newUnit = 'square_' + newName
                unitOperators[ newUnit ] = newUnitInfo
                newAliases.update( newUnitAliases )

                oldUnit = 'square_' + metricUnit[ 0 ]

                # add new conversions
                areaConversion = power( newConversion, 2 )

                newConversions[ ( oldUnit, newUnit ) ] = str( areaConversion )
                newConversions[ ( newUnit, oldUnit ) ] = str( fdiv( 1, areaConversion ) )

                for op1, op2 in unitConversionMatrix:
                    if ( op1 == oldUnit ) or ( op2 == oldUnit ):
                        oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                        if op1 == oldUnit and newUnit != op2:
                            newConversions[ ( newUnit, op2 ) ] = str( fdiv( oldConversion, areaConversion ) )
                        elif op2 == oldUnit and newUnit != op1:
                            newConversions[ ( op1, newUnit ) ] = str( fmul( oldConversion, areaConversion ) )

                newUnitInfo, newUnitAliases = makeVolumeOperator( newName, newPlural )

                newUnit = 'cubic_' + newName
                unitOperators[ newUnit ] = newUnitInfo
                newAliases.update( newUnitAliases )

                oldUnit = 'cubic_' + metricUnit[ 0 ]

                # add new conversions
                volumeConversion = power( newConversion, 3 )

                newConversions[ ( oldUnit, newUnit ) ] = str( volumeConversion )
                newConversions[ ( newUnit, oldUnit ) ] = str( fdiv( 1, volumeConversion ) )

                for op1, op2 in unitConversionMatrix:
                    if ( op1 == oldUnit ) or ( op2 == oldUnit ):
                        oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                        if op1 == oldUnit and newUnit != op2:
                            newConversions[ ( newUnit, op2 ) ] = str( fdiv( oldConversion, volumeConversion ) )
                            #print( newUnit, op2, volumeConversion )
                        elif op2 == oldUnit and newUnit!= op1:
                            newConversions[ ( op1, newUnit) ] = str( fmul( oldConversion, volumeConversion ) )
                            #print( op1, newUnit, volumeConversion )

    return newConversions


#//******************************************************************************
#//
#//  expandDataUnits
#//
#//  Every data unit needs to be permuted for all positive SI power types and
#//  the binary power types.  We need to create conversions for each new type,
#//  as well as aliases.
#//
#//******************************************************************************

def expandDataUnits( newAliases ):
    # expand data measurements for all prefixes
    newConversions = { }

    for dataUnit in dataUnits:
        for prefix in dataPrefixes:
            newName = prefix[ 0 ] + dataUnit[ 0 ]
            newPlural = prefix[ 0 ] + dataUnit[ 1 ]

            # constuct unit operator info
            unitOperators[ newName ] = \
                UnitInfo( unitOperators[ dataUnit[ 0 ] ].unitType, newName, newPlural, prefix[ 1 ] + dataUnit[ 2 ],
                                         [ ], unitOperators[ dataUnit[ 0 ] ].categories )

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, dataUnit[ 0 ] ) ] = str( newConversion )
            newConversion = fdiv( 1, newConversion )
            unitConversionMatrix[ ( dataUnit[ 0 ], newName ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == dataUnit[ 0 ] ) or ( op2 == dataUnit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == dataUnit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fdiv( oldConversion, newConversion ) )
                        #print( '(', newName, op2, ')', str( fdiv( oldConversion, newConversion ) ) )
                    elif op2 == dataUnit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fmul( oldConversion, newConversion ) )
                        #print( '(', op1, newName, ')', str( fmul( oldConversion, newConversion ) ) )

        for prefix in binaryPrefixes:
            newName = prefix[ 0 ] + dataUnit[ 0 ]
            newPlural = prefix[ 0 ] + dataUnit[ 1 ]

            # constuct unit operator info
            unitOperators[ newName ] = \
                UnitInfo( unitOperators[ dataUnit[ 0 ] ].unitType, newName, newPlural, prefix[ 1 ] + dataUnit[ 2 ],
                                         [ ], unitOperators[ dataUnit[ 0 ] ].categories )

            newConversion = power( 2, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, dataUnit[ 0 ] ) ] = str( newConversion )
            newConversion = fdiv( 1, newConversion )
            unitConversionMatrix[ ( dataUnit[ 0 ], newName ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == dataUnit[ 0 ] ) or ( op2 == dataUnit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == dataUnit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fdiv( oldConversion, newConversion ) )
                    elif op2 == dataUnit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fmul( oldConversion, newConversion ) )

    return newConversions


#//******************************************************************************
#//
#//  makeAreaOperator
#//
#//******************************************************************************

def makeAreaOperator( unit, unitPlural ):
    unitInfo = unitOperators[ unit ]

    newAliases = { }

    newUnit = 'square_' + unit

    if unitInfo.abbrev == '':
        abbrev = 'sq' + unit
    else:
        abbrev = 'sq' + unitInfo.abbrev
        newAliases[ 'sq' + unitInfo.abbrev ] = newUnit

    newUnitInfo = UnitInfo( 'area', unit + '^2', 'square_' + unitPlural, abbrev, [ ], unitInfo.categories )

    newAliases[ 'square_' + unitInfo.plural ] = newUnit
    newAliases[ 'square_' + unitInfo.abbrev ] = newUnit
    newAliases[ 'sq' + unitInfo.plural ] = newUnit
    newAliases[ unit +  '^2' ] = newUnit
    newAliases[ unitInfo.plural + '^2' ] = newUnit

    return newUnitInfo, newAliases


#//******************************************************************************
#//
#//  makeVolumeOperator
#//
#//******************************************************************************

def makeVolumeOperator( unit, unitPlural ):
    unitInfo = unitOperators[ unit ]

    newAliases = { }

    newUnit = 'cubic_' + unit

    if unitInfo.abbrev == '':
        abbrev = 'cu' + unit
    else:
        abbrev = 'cu' + unitInfo.abbrev
        newAliases[ 'cu' + unitInfo.abbrev ] = newUnit

    newUnitInfo = UnitInfo( 'volume', unit + '^3', 'cubic_' + unitPlural, abbrev, [ ], unitInfo.categories )

    newAliases[ 'cubic_' + unitInfo.plural ] = newUnit
    newAliases[ 'cubic_' + unitInfo.abbrev ] = newUnit
    newAliases[ 'cu' + unitInfo.plural ] = newUnit
    newAliases[ unit +  '^3' ] = newUnit
    newAliases[ unitInfo.plural + '^3' ] = newUnit

    return newUnitInfo, newAliases


#//******************************************************************************
#//
#//  initializeConversionMatrix
#//
#//******************************************************************************

def initializeConversionMatrix( unitConversionMatrix ):
    mp.dps = 50

    # reverse each conversion
    print( 'Reversing each conversion...' )

    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        conversion = fdiv( 1, mpmathify( unitConversionMatrix[ ( op1, op2 ) ] ) )
        newConversions[ ( op2, op1 ) ] = str( conversion )

    unitConversionMatrix.update( newConversions )

    # create map for compound units based on the conversion matrix
    print( 'Mapping compound units...' )

    compoundUnits = { }

    for unit1, unit2 in unitConversionMatrix:
        chars = set( '*/^' )

        if any( ( c in chars ) for c in unit2 ):
            compoundUnits[ unit1 ] = unit2
            #print( '    compound unit: ', unit1, '(', unit2, ')' )

    # create area and volume units from all of the length units
    #print( )
    print( 'Creating area and volume units for all length units...' )

    newOperators = { }
    newAliases = { }

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]

        if unitInfo.unitType == 'length':
            newUnit = 'square_' + unit

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = makeAreaOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnits[ unit + '*' + unit ] = newUnit

            newUnit = 'cubic_'+ unit

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = makeVolumeOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnits[ unit + '*' + unit + '*' + unit ] = newUnit

    unitOperators.update( newOperators )

    # add new conversions for the new area and volume units
    print( 'Adding new conversions for the new area and volume units...' )

    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if unitOperators[ op1 ].unitType == 'length':
            conversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )
            newConversions[ ( 'square_' + op1, 'square_' + op2 ) ] = str( power( conversion, 2 ) )
            newConversions[ ( 'cubic_' + op1, 'cubic_' + op2 ) ] = str( power( conversion, 3 ) )

    unitConversionMatrix.update( newConversions )

    # extrapolate transitive conversions
    print( )
    print( 'Extrapolating transitive conversions for', len( unitOperators ), 'units...' )

    unitTypeTable = makeUnitTypeTable( unitOperators )

    for unitType in sorted( basicUnitTypes ):
        print( '    ', unitType, '({} operators)'.format( len( unitTypeTable[ unitType ] ) ) )

        while True:
            newConversion = False

            for op1, op2 in itertools.combinations( unitTypeTable[ unitType ], 2 ):
                if ( op1, op2 ) in unitConversionMatrix:
                    #print( )
                    #print( ( op1, op2 ), ': ', unitConversionMatrix[ ( op1, op2 ) ] )

                    for op3 in unitTypeTable[ unitType ]:
                        # we can ignore duplicate operators
                        if ( op3 == op1 ) or ( op3 == op2 ):
                            continue

                        # we can shortcut if the types are not compatible
                        if unitOperators[ op3 ].unitType != unitOperators[ op1 ].unitType:
                            continue

                        conversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                        if ( op1, op3 ) not in unitConversionMatrix and ( op2, op3 ) in unitConversionMatrix:
                            #print( 'transitive: ', ( op2, op3 ), unitConversionMatrix[ ( op2, op3 ) ] )
                            newConversion = fmul( conversion, mpmathify( unitConversionMatrix[ ( op2, op3 ) ] ) )
                            #print( ( op1, op3 ), newConversion )
                            unitConversionMatrix[ ( op1, op3 ) ] = str( newConversion )
                            #print( ( op3, op1 ), fdiv( 1, newConversion ) )
                            unitConversionMatrix[ ( op3, op1 ) ] = str( fdiv( 1, newConversion ) )

                            newConversion = True
                        elif ( op2, op3 ) not in unitConversionMatrix and ( op1, op3 ) in unitConversionMatrix:
                            #print( 'transitive: ', ( op1, op3 ), unitConversionMatrix[ ( op1, op3 ) ] )
                            newConversion = fdiv( mpmathify( unitConversionMatrix[ ( op1, op3 ) ] ), conversion )
                            #print( ( op2, op3 ), newConversion )
                            unitConversionMatrix[ ( op2, op3 ) ] = str( newConversion )
                            #print( ( op3, op2 ), fdiv( 1, newConversion ) )
                            unitConversionMatrix[ ( op3, op2 ) ] = str( fdiv( 1, newConversion ) )

                            newConversion = True

                print( len( unitConversionMatrix ), end='\r' )

            if not newConversion:
                break

    # expand metric operators and add new conversions, aliases, etc.
    print( '           ' )
    print( 'Expanding metric units against the list of SI prefixes...' )

    newAliases = { }

    unitConversionMatrix.update( expandMetricUnits( newAliases ) )

    # the second pass allows the full permuation of conversions between base types of the same unit type
    # (e.g., it's necessary to get a conversion between 'megameter' and 'megapotrzebie' )
    print( 'Expanding metric units (second pass)...' )
    unitConversionMatrix.update( expandMetricUnits( newAliases ) )

    print( 'Expanding data units against the list of SI and binary prefixes...' )

    unitConversionMatrix.update( expandDataUnits( newAliases ) )

    print( 'Expanding data units (second pass)...' )
    unitConversionMatrix.update( expandDataUnits( newAliases ) )

    # add new operators for compound time units
    print( 'Expanding compound time units...' )

    newUnitOperators = { }

    for unit in unitOperators:
        if unit[ -7 : ] == '-second' and unit[ : 7 ] != 'square_' and unit[ : 6 ] != 'cubic_':
            unitRoot = unit[ : -7 ]
            unitInfo = unitOperators[ unit ]

            rootUnitInfo = unitOperators[ unitRoot ]

            for timeUnit in timeUnits:
                newUnit = unitRoot + '-' + timeUnit[ 0 ]
                newPlural = unitRoot + '-' + timeUnit[ 1 ]
                newAliases[ newPlural ] = newUnit
                newAliases[ unitRoot + '-' + timeUnit[ 1 ] ] = newUnit

                # We assume the abbrev ends with an s for second
                if unitInfo.abbrev != '':
                    newAbbrev = unitInfo.abbrev[ : -1 ] + timeUnit[ 2 ]
                    newAliases[ newAbbrev ] = newUnit

                for alias in rootUnitInfo.aliases:
                    newAliases[ alias + '*' + timeUnit[ 0 ] ] = newUnit
                    newAliases[ alias + '-' + timeUnit[ 0 ] ] = newUnit

                    if timeUnit[ 0 ] != timeUnit[ 1 ]:
                        newAliases[ alias + '*' + timeUnit[ 1 ] ] = newUnit
                        newAliases[ alias + '-' + timeUnit[ 1 ] ] = newUnit

                newUnitOperators[ newUnit ] = \
                    UnitInfo( unitInfo.unitType, unitRoot + '*' + timeUnit[ 0 ], newPlural, '', [ ], unitInfo.categories )

                conversion = mpmathify( timeUnit[ 3 ] )
                unitConversionMatrix[ ( newUnit, unit ) ] = str( conversion )
                unitConversionMatrix[ ( unit, newUnit ) ] = str( fdiv( 1, conversion ) )

    unitOperators.update( newUnitOperators )

    newUnitOperators = { }

    for unit in unitOperators:
        if unit[ -7 : ] == '/second' and unit[ : 7 ] != 'square_' and unit[ : 6 ] != 'cubic_':
            unitRoot = unit[ : -7 ]

            unitInfo = unitOperators[ unit ]
            rootUnitInfo = unitOperators[ unitRoot ]

            for timeUnit in timeUnits:
                newUnit = unitRoot + '/' + timeUnit[ 0 ]
                newPlural = unitRoot + '/' + timeUnit[ 1 ]
                newAliases[ newPlural ] = newUnit
                newAliases[ unitRoot + '/' + timeUnit[ 1 ] ] = newUnit

                # We assume the abbrev ends with an s for second
                if unitInfo.abbrev != '':
                    newAbbrev = unitInfo.abbrev[ : -1 ] + timeUnit[ 2 ]
                    newAliases[ newAbbrev ] = newUnit

                for alias in rootUnitInfo.aliases:
                    newAliases[ alias + '/' + timeUnit[ 0 ] ] = newUnit

                    if timeUnit[ 0 ] != timeUnit[ 1 ]:
                        newAliases[ alias + '/' + timeUnit[ 1 ] ] = newUnit

                newUnitOperators[ newUnit ] = \
                    UnitInfo( unitInfo.unitType, unitRoot + '*' + timeUnit[ 0 ], newPlural, '', [ ], unitInfo.categories )

                conversion = mpmathify( timeUnit[ 3 ] )
                unitConversionMatrix[ ( newUnit, unit ) ] = str( fdiv( 1, conversion ) )
                unitConversionMatrix[ ( unit, newUnit ) ] = str( conversion )

    unitOperators.update( newUnitOperators )

    # add new conversions for compound time units
    print( 'Adding new conversions for compound time units...' )

    newUnitConversions = { }

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]

        if unit[ -7 : ] == '-second':
            for timeUnit in timeUnits:
                newUnit = unit[ : -6 ] + timeUnit[ 0 ]

                factor = mpmathify( timeUnit[ 3 ] )

                for op1, op2 in unitConversionMatrix:
                    if op1 == unit:
                        oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )
                        newUnitConversions[ ( newUnit, op2 ) ] = str( fmul( oldConversion, factor ) )

                        if unitInfo.abbrev != '':
                            newAliases[ unitInfo.abbrev[ : -1 ] + timeUnit[ 2 ] ] = newUnit
                    elif op2 == unit:
                        oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )
                        newUnitConversions[ ( op1, newUnit ) ] = str( fdiv( oldConversion, factor ) )

                        if unitInfo.abbrev != '':
                            newAliases[ unitInfo.abbrev[ : -1 ] + timeUnit[ 2 ] ] = newUnit

    unitConversionMatrix.update( newUnitConversions )

    # make some more aliases
    print( 'Making some more aliases...' )

    newAliases.update( makeAliases( ) )

    #for op1, op2 in unitConversionMatrix:
    #    print( op1, op2, unitConversionMatrix[ ( op1, op2 ) ] )

    #print( )
    #print( )

    #for alias in newAliases:
    #    print( alias, newAliases[ alias ] )

    print( 'Saving everything...' )

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
    fileName = dataPath + os.sep + 'units.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicUnitTypes, pickleFile )
        pickle.dump( unitOperators, pickleFile )
        pickle.dump( newAliases, pickleFile )
        pickle.dump( compoundUnits, pickleFile )
        pickle.dump( massTable, pickleFile )
        pickle.dump( lengthTable, pickleFile )
        pickle.dump( volumeTable, pickleFile )

    fileName = dataPath + os.sep + 'unit_conversions.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( unitConversionMatrix, pickleFile )

    print( )
    print( '{:,} unit operators'.format( len( unitOperators ) ) )
    print( '{:,} unit conversions'.format( len( unitConversionMatrix ) ) )
    print( '{:,} aliases'.format( len( newAliases ) ) )
    print( '{:,} compound units'.format( len( compoundUnits ) ) )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    print( PROGRAM_NAME, PROGRAM_VERSION, '-', PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    initializeConversionMatrix( unitConversionMatrix )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

