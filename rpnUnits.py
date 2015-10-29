#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUnits.py
# //
# //  RPN command-line calculator unit conversion declarations
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import *

from rpnEstimates import *
from rpnUnitClasses import *


# //******************************************************************************
# //
# //  basicUnitTypes
# //
# //  There are 'primitive' unit types and 'compound' unit types.
# //  The compound unit types can always be broken down in terms of the
# //  primitive unit types.  The 'primitive' unit types cannot be expressed
# //  in terms of other primitive unit types.
# //
# //  The primitive unit types include:
# //
# //  length, mass, time, charge, temperature, angle, electric_potential
# //  information_entropy, luminous_intensity
# //
# //  simpleUnitType:  conversion from the primitive unit types
# //
# //  compoundUnitType:  a list of conversions from other unit types where
# //     the conversion does not consist solely of primitive unit types
# //
# //  baseUnit:  The standard or customary unit of measurement for this unit
# //     type
# //
# //  estimateTable : The table of estimates, expressed in terms of the base
# //     unit, used for the 'estimate' operator.
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  Notes:
# //
# //  I chose not to incorporate mass-energy equivalence here.  I don't think it
# //  helps.  I just created the 'gram-equivalent' unit instead.  I have some
# //  ideas about how to better implement the fact that a number of energy
# //  units are really mass units in disguise.
# //
# //  Constant is not a 'real' unit type, but it is useful for it to act like
# //  one because it makes for useful operators, e.g. "20 M" for "20,000,000'.
# //
# //  dimension
# //  baseUnitType
# //  primitiveUnit
# //  estimateTable
# //
# //******************************************************************************

basicUnitTypes = {
    'acceleration' : UnitTypeInfo(
        'length/time^2',
        'meter/second^2',
        'meter/second^2',
        accelerationTable
    ),

    'amount_of_substance' : UnitTypeInfo(
        'amount_of_substance',
        'mole',
        'mole',
        amountOfSubstanceTable
    ),

    'angle' : UnitTypeInfo(
        'angle',
        'radian',
        'radian',
        angleTable
    ),

    'area' : UnitTypeInfo(
        'length^2',
        'square_meter',
        'square_meter',
        areaTable,
    ),

    'capacitance' : UnitTypeInfo(
        'charge/electric_potential',
        'farad',
        'coulomb/volt',
        capacitanceTable,
    ),

    'charge' : UnitTypeInfo(
        'charge',
        'coulomb',
        'coulomb',
        chargeTable,
    ),

    'constant' : UnitTypeInfo(
        'constant',
        'unity',
        'unity',
        constantTable,
    ),

    'current' : UnitTypeInfo(
        'charge/time',
        'ampere',
        'coulomb/second',
        currentTable,
    ),

    'data_rate' : UnitTypeInfo(
        'information_entropy/time',
        'bit/second',
        'bit/second',
        dataRateTable,
    ),

    'density' : UnitTypeInfo(
        'mass/length^3',
        'kilogram/liter',
        'kilogram/liter',
        densityTable,
    ),

    'dynamic_viscosity' : UnitTypeInfo(
        'mass/length*time',     # force*time/length^2
        'pascal*second',
        'kilogram/meter*second',
        dynamicViscosityTable,
    ),

    'electrical_conductance' : UnitTypeInfo(
        '1/electrical_resistance',
        'siemens',
        '1/ohm',
        electricalConductanceTable,
    ),

    'electrical_resistance' : UnitTypeInfo(
        'electrical_resistance',
        'ohm',
        'ohm',
        electricalResistanceTable,
    ),

    'electric_potential' : UnitTypeInfo(
        'electric_potential',
        'volt',
        'volt',
        electricPotentialTable,
    ),

    'energy' : UnitTypeInfo(
        'mass*length^2/time^2',
        'joule',
        'kilogram*meter^2/second^2',  # , 'volt*coulomb' ]
        energyTable,
    ),

    'force' : UnitTypeInfo(
        'mass*length/time^2',
        'newton',
        'kilogram*meter/second^2',
        forceTable,
    ),

    'frequency' : UnitTypeInfo(
        '1/time',
        'hertz',
        'hertz',
        frequencyTable,
    ),

    'illuminance' : UnitTypeInfo(
        'luminous_intensity*angle^2/length^2',
        'lux',
        'candela*steradian/meter^2',
        illuminanceTable,
    ),

    'inductance' : UnitTypeInfo(
        'electric_potential/charge',
        'henry',
        'volt/coulomb',
        inductanceTable,
    ),

    'information_entropy' : UnitTypeInfo(
        'information_entropy',
        'bit',
        'bit',
        informationEntropyTable,
    ),

    'length' : UnitTypeInfo(
        'length',
        'meter',
        'meter',
        lengthTable,
    ),

    'luminance' : UnitTypeInfo(
        'luminous_intensity/length^2',
        'candela/meter^2',
        'candela/meter^2',
        luminanceTable,
    ),

    'luminous_flux' : UnitTypeInfo(
        'luminous_intensity*angle^2',
        'lumen',
        'candela*steradian',
        luminousFluxTable,
    ),

    'luminous_intensity' : UnitTypeInfo(
        'luminous_intensity',
        'candela',
        'candela',
        luminousIntensityTable,
    ),

    'magnetic_field_strength' : UnitTypeInfo(
        'charge/length',
        'ampere/meter',
        'ampere/meter',
        magneticFieldStrengthTable,
    ),

    'magnetic_flux' : UnitTypeInfo(
        'electric_potential*time',
        'weber',
        'volt*second',
        magneticFluxTable,
    ),

    'magnetic_flux_density' : UnitTypeInfo(
        'electric_potential*time/length^2',
        'tesla',
        'volt*second/meter^2',
        magneticFluxDensityTable,
    ),

    'mass' : UnitTypeInfo(
        'mass',
        'kilogram',
        'kilogram',
        massTable,
    ),

    'power' : UnitTypeInfo(
        'electric_potential*charge/time',
        'watt',
        'volt*coulomb/second',
        powerTable,
    ),

    'pressure' : UnitTypeInfo(
        'mass/length*time^2',
        'pascal',
        'kilogram/meter*second^2',
        pressureTable,
    ),

    'radiation_dose' : UnitTypeInfo(
        'electric_potential*charge/mass',
        'sievert',
        'volt*coulomb/kilogram',
        radiationDoseTable,
    ),

    'radiation_exposure' : UnitTypeInfo(
        'charge/mass',
        'coulomb/kilogram',
        'coulomb/kilogram',
        radiationExposureTable,
    ),

    'solid_angle' : UnitTypeInfo(
        'angle^2',
        'steradian',
        'steradian',
        solidAngleTable,
    ),

    'temperature' : UnitTypeInfo(
        'temperature',
        'kelvin',
        'kelvin',
        temperatureTable,
    ),

    'time' : UnitTypeInfo(
        'time',
        'second',
        'second',
        timeTable,
    ),

    'velocity' : UnitTypeInfo(
        'length/time',
        'meter/second',
        'meter/second',
        velocityTable,
    ),

    'volume' : UnitTypeInfo(
        'length^3',
        'liter',
        'liter',
        volumeTable,
    ),
}


# //******************************************************************************
# //
# //  unitOperators
# //
# //  unit name : unitType, representation, plural, abbrev, aliases, categories
# //
# //******************************************************************************

unitOperators = {
    # acceleration

    'galileo' :
        UnitInfo( 'acceleration', 'galileo', 'galileos', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'meter/second^2' :
        UnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', 'm/s^2', [ ], [ 'SI' ],
                  '''
                  ''' ),


    # amount of substance

    'mole' :
        UnitInfo( 'amount_of_substance', 'mole', 'mole', 'mol', [ 'einstein' ], [ 'SI' ],
                  '''
                  ''' ),

    # angle

    'arcminute' :
        UnitInfo( 'angle', 'arcminute', 'arcminutes', 'arcmin', [ 'arcmins' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'arcsecond' :
        UnitInfo( 'angle', 'arcsecond', 'arcseconds', 'arcsec', [ 'arcsecs' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'centrad' :
        UnitInfo( 'angle', 'centrad', 'centrads', '', [ ], [ 'mathematics', 'science' ],
                  '''
                  ''' ),

    'degree' :
        UnitInfo( 'angle', 'degree', 'degrees', 'deg', [ ], [ 'mathematics' ],
                  '''
                  ''' ),

    'grad' :
        UnitInfo( 'angle', 'grad', 'grads', '', [ 'gon', 'gons' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'milliarcsecond' :
        UnitInfo( 'angle', 'milliarcsecond', 'milliarcseconds', 'mas', [ 'milliarcsecs' ], [ 'astronomy' ],
                  '''
                  ''' ),

    'octant' :
        UnitInfo( 'angle', 'octant', 'octants', '', [ ], [ 'mathematics' ],
                  '''
                  ''' ),

    'pointangle' :
        UnitInfo( 'angle', 'pointangle', 'pointangles', '', [ ], [ 'navigation' ],
                  '''
                  ''' ),

    'quadrant' :
        UnitInfo( 'angle', 'quadrant', 'quadrants', '', [ ], [ 'mathematics' ],
                  '''
                  ''' ),

    'quintant' :
        UnitInfo( 'angle', 'quintant', 'quintants', '', [ ], [ 'mathematics' ],
                  '''
                  ''' ),

    'radian' :
        UnitInfo( 'angle', 'radian', 'radians', 'rad', [ ], [ 'mathematics', 'SI' ],
                  '''
                  ''' ),

    'sextant' :
        UnitInfo( 'angle', 'sextant', 'sextants', '', [ 'flat', 'flats' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'streck' :
        UnitInfo( 'angle', 'streck', 'strecks', '', [ ], [ 'Sweden' ],
                  '''
                  ''' ),

    # area

    'acre' :
        UnitInfo( 'area', 'acre', 'acres', 'ac', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'are' :
        UnitInfo( 'area', 'are', 'ares', 'a', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'barn' :
        UnitInfo( 'area', 'barn', 'barns', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'bovate' :
        UnitInfo( 'area', 'bovate', 'bovates', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'carucate' :
        UnitInfo( 'area', 'carucate', 'carucates', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'homestead':
        UnitInfo( 'area', 'homestead', 'homesteads', '', [ ], [ 'US' ],
                  '''
                  ''' ),

    'imperial_square' :
        UnitInfo( 'area', 'imperial_sqaure', 'imperial_squares', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'morgen' :
        UnitInfo( 'area', 'morgen', 'morgens', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'nanoacre' :
        UnitInfo( 'area', 'nanoacre', 'nanoacres', 'nac', [ ], [ 'computing' ],
                  '''
                  ''' ),

    'outhouse' :
        UnitInfo( 'area', 'outhouse', 'outhouse', '', [ ], [ 'science', 'humorous' ],
                  '''
                  ''' ),

    'rood' :
        UnitInfo( 'area', 'rood', 'roods', '', [ 'farthingdale' ], [ 'imperial' ],
                  '''
                  ''' ),

    'section':
        UnitInfo( 'area', 'section', 'sections', '', [ ], [ 'US' ],
                  '''
                  ''' ),

    'shed' :
        UnitInfo( 'area', 'shed', 'sheds', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'square_foot' :
        UnitInfo( 'area', 'foot^2', 'square_feet', 'ft^2', [ 'feet^2', 'sqft', 'sq_ft', 'sq_foot', 'sq_feet', 'square_ft' ], [ 'imperial' ],
                  '''
                  ''' ),

    'square_meter' :
        UnitInfo( 'area', 'meter^2', 'square_meters', 'm^2', [ 'meters^2', 'sqm', 'sq_m', 'sq_meter', 'sq_meters', 'square_m' ], [ 'SI' ],
                  '''
                  ''' ),

    'square_yard' :
        UnitInfo( 'area', 'yard^2', 'square_yards', 'yd^2', [ 'yards^2', 'sqyd', 'sq_yd', 'sq_yard', 'sq_yards', 'square_yd' ], [ 'imperial' ],
                  '''
                  ''' ),

    'township':
        UnitInfo( 'area', 'township', 'townships', '', [ ], [ 'US' ],
                  '''
                  ''' ),

    'virgate':
        UnitInfo( 'area', 'virgate', 'virgates', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    # capacitance

    'abfarad' :
        UnitInfo( 'capacitance', 'abfarad', 'abfarads', 'abF', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'coulomb/volt' :
        UnitInfo( 'capacitance', 'coulomb/volt', 'coulombs/volt', 'C/V', [ 'coulomb/volts', 'coulombs/volts', 'C/volts', 'C/volt', 'coulomb/V', 'coulombs/V' ], [ 'SI' ],
                  '''
                  ''' ),

    'farad' :
        UnitInfo( 'capacitance', 'farad', 'farads', 'F', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'jar' :
        UnitInfo( 'capacitance', 'jar', 'jars', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'statfarad' :
        UnitInfo( 'capacitance', 'statfarad', 'statfarads', 'statF', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # charge

    'abcoulomb' :
        UnitInfo( 'charge', 'abcoulomb', 'abcoulombs', 'abC', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'ampere-second' :
        UnitInfo( 'charge', 'ampere*second', 'ampere-seconds', 'A/s', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'coulomb' :
        UnitInfo( 'charge', 'coulomb', 'coulombs', 'C', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'farad-volt' :
        UnitInfo( 'charge', 'farad*volt', 'farad-volts', 'F*V', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'franklin' :
        UnitInfo( 'charge', 'franklin', 'franklins', 'Fr', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'faraday' :
        UnitInfo( 'charge', 'faraday', 'faradays', 'Fd', [ ], [ 'natural' ],   # electron_charge * Avogradro's number!
                  '''
                  ''' ),

    'statcoulomb' :
        UnitInfo( 'charge', 'statcoulomb', 'statcoulombs', 'statC', [ 'esu_charge' ], [ 'CGS' ],
                  '''
                  ''' ),

    # constant - Constant is a special type that is immediately converted to a numerical value when used.
    #            It's not intended to be used as a unit, per se.  Also, these units are in order of their
    #            value instead of alphabetical order like all the others

    'decillionth' :
        UnitInfo( 'constant', 'decillionth', 'decillionths', '', [ ], [ 'constant' ],
                  '''One decillionth:  10e-33 or 1/1,000,000,000,000,000,000,000,000,000,000,000''' ),

    'nonillionth' :
        UnitInfo( 'constant', 'nonillionth', 'nonillionths', '', [ ], [ 'constant' ],
                  '''One nonillionth:  10e-30 or 1/1,000,000,000,000,000,000,000,000,000,000''' ),

    'octillionth' :
        UnitInfo( 'constant', 'octillionth', 'octillionths', '', [ ], [ 'constant' ],
                  '''One octillionth:  10e-27 or 1/1,000,000,000,000,000,000,000,000,000''' ),

    # 'y' can't be used here since it's an operator
    'septillionth' :
        UnitInfo( 'constant', 'septillionth', 'septillionths', '', [ 'yocto' ], [ 'constant' ],
                  '''One septillionth:  10e-24 or 1/1,000,000,000,000,000,000,000,000''' ),

    # 'z' can't be used here since it's an operator
    'sextillionth' :
        UnitInfo( 'constant', 'sextillionth', 'sextillionths', '', [ 'zepto' ], [ 'constant' ],
                  '''One sextillionth:  10e-21 or 1/1,000,000,000,000,000,000,000''' ),

    # 'a' can't be used here since it's used for 'are'
    'quintillionth' :
        UnitInfo( 'constant', 'quintillionth', 'quintillionths', '', [ 'atto' ], [ 'constant' ],
                  '''One quintillionth:  10e-18 or 1/1,000,000,000,000,000,000''' ),

    'quadrillionth' :
        UnitInfo( 'constant', 'quadrillionth', 'quadrillionths', 'f', [ 'femto' ], [ 'constant' ],
                  '''One quadrillionth:  10e-15 or 1/1,000,000,000,000,000''' ),

    'trillionth' :
        UnitInfo( 'constant', 'trillionth', 'trillionths', 'p', [ 'pico' ], [ 'constant' ],
                  '''One trillionth:  10e-12 or 1/1,000,000,000,000''' ),

    'billionth' :
        UnitInfo( 'constant', 'billionth', 'billionths', 'n', [ 'nano' ], [ 'constant' ],
                  '''One billionth:  10e-9 or 1/1,000,000,000''' ),

    'millionth' :
        UnitInfo( 'constant', 'millionth', 'millionths', 'u', [ 'micro' ], [ 'constant' ],
                  '''One millionth:  10e-6 or 1/1,000,000''' ),

    # 'm' can't be used here since it's used for 'meter'
    'thousandth' :
        UnitInfo( 'constant', 'thousandth', 'thousandths', '', [ 'milli' ], [ 'constant' ],
                  '''One thousandth:  10e-3 or 1/1,000''' ),

    'percent' :
        UnitInfo( 'constant', 'percent', 'percent', '%', [ 'hundredth', 'centi' ], [ 'constant' ],
                  '''One hundredth:  10e-2 or 1/100''' ),

    'tenth' :
        UnitInfo( 'constant', 'tenth', 'tenths', '', [ 'deci', 'tithe' ], [ 'constant' ],
                  '''One tenth:  10e-1 or 1/10''' ),

    'quarter' :
        UnitInfo( 'constant', 'quarter', 'quarters', '', [ 'fourth' ], [ 'constant' ],
                  '''One quarter:  1/4 or 0.25''' ),

    'third' :
        UnitInfo( 'constant', 'third', 'thirds', '', [ ], [ 'constant' ],
                  '''One third:  1/3 or 0.333333...''' ),

    'half' :
        UnitInfo( 'constant', 'half', 'halves', '', [ ], [ 'constant' ],
                  '''One half:  1/2 or 0.5''' ),

    'unity' :
        UnitInfo( 'constant', 'x unity', 'x unity', '', [ ], [ 'constant' ],
                  '''Unity, one, 1''' ),

    'ten' :
        UnitInfo( 'constant', 'ten', 'tens', '', [ 'deca', 'deka', 'dicker' ], [ 'constant' ],
                  '''Ten:  10e1, or 10''' ),

    'dozen' :
        UnitInfo( 'constant', 'dozen', 'dozen', '', [ ], [ 'constant' ],
                  '''A dozen is 12.''' ),

    'score' :
        UnitInfo( 'constant', 'score', 'score', '', [ ], [ 'constant' ],
                  '''A score is 20.''' ),

    'flock' :
        UnitInfo( 'constant', 'flock', 'flocks', '', [ ], [ 'constant' ],
                  '''A flock is an archaic name for 40.''' ),

    'shock' :
        UnitInfo( 'constant', 'shock', 'shocks', '', [ ], [ 'constant' ],
                  '''A shock is an archaic name for 60.''' ),

    'hundred' :
        UnitInfo( 'constant', 'hundred', 'hundred', '', [ 'hecto', 'toncount' ], [ 'constant' ],
                  '''One hundred:  10e2, or 100''' ),

    'long_hundred' :
        UnitInfo( 'constant', 'long_hundred', 'long_hundreds', '', [ ], [ 'constant' ],
                  '''\'long\' hundred is an archaic term for 120.''' ),

    'gross' :
        UnitInfo( 'constant', 'gross', 'gross', '', [ ], [ 'constant' ],
                  '''A gross is a dozen dozen, or 144''' ),

    'thousand' :
        UnitInfo( 'constant', 'thousand', 'thousand', 'k', [ 'kilo' ], [ 'constant' ],
                  '''One thousand:  10e3, or 1,000''' ),

    'great_gross' :
        UnitInfo( 'constant', 'great_gross', 'great_gross', '', [ ], [ 'constant' ],
                  '''A great gross is a dozen gross, or 1728.''' ),

    'million' :
        UnitInfo( 'constant', 'million', 'million', 'M', [ 'mega' ], [ 'constant' ],
                  '''One million:  10e6 or 1,000,000''' ),

    # 'G' can't be used here since it's used for 'standard gravity'
    'billion' :
        UnitInfo( 'constant', 'billion', 'billion', '', [ 'giga' ], [ 'constant' ],
                  '''One billion:  10e9 or 1,000,000,000''' ),

    # 'T' can't be used here since it's used for 'tesla'
    'trillion' :
        UnitInfo( 'constant', 'trillion', 'trillion', '', [ 'tera' ], [ 'constant' ],
                  '''One trillion:  10e12 or 1,000,000,000,000''' ),

    'quadrillion' :
        UnitInfo( 'constant', 'quadrillion', 'quadrillion', 'P', [ 'peta' ], [ 'constant' ],
                  '''One quadrillion:  10e15 or 1,000,000,000,000,000''' ),

    'quintillion' :
        UnitInfo( 'constant', 'quintillion', 'quintillion', 'E', [ 'exa' ], [ 'constant' ],
                  '''One quintillion:  10e18 or 1,000,000,000,000,000,000''' ),

    'sextillion' :
        UnitInfo( 'constant', 'sextillion', 'sextillion', 'Z', [ 'zetta' ], [ 'constant' ],
                  '''One sextillion:  10e21 or 1,000,000,000,000,000,000,000''' ),

    'septillion' :
        UnitInfo( 'constant', 'septillion', 'septillion', 'Y', [ 'yotta' ], [ 'constant' ],
                  '''One septillion:  10e24 or 1,000,000,000,000,000,000,000,000''' ),

    'octillion' :
        UnitInfo( 'constant', 'octillion', 'octillion', '', [ ], [ 'constant' ],
                  '''One octillion:  10e27 or 1,000,000,000,000,000,000,000,000,000''' ),

    'nonillion' :
        UnitInfo( 'constant', 'nonillion', 'nonillion', '', [ ], [ 'constant' ],
                  '''One nonillion:  10e30 or 1,000,000,000,000,000,000,000,000,000,000''' ),

    'decillion' :
        UnitInfo( 'constant', 'decillion', 'decillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e33 or 1,000,000,000,000,000,000,000,000,000,000,000''' ),

    'undecillion' :
        UnitInfo( 'constant', 'undecillion', 'undecillion', '', [ ], [ 'constant' ],
                  '''One undecillion:  10e36''' ),

    'duodecillion' :
        UnitInfo( 'constant', 'duodecillion', 'duodecillion', '', [ ], [ 'constant' ],
                  '''One duodecillion:  10e39''' ),

    'tredecillion' :
        UnitInfo( 'constant', 'tredecillion', 'tredecillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e42''' ),

    'quattuordecillion' :
        UnitInfo( 'constant', 'quattuordecillion', 'quattuordecillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e45''' ),

    'quindecillion' :
        UnitInfo( 'constant', 'quindecillion', 'quindecillion', '', [ 'quinquadecillion' ], [ 'constant' ],
                  '''One decillion:  10e48''' ),

    'sexdecillion' :
        UnitInfo( 'constant', 'sexdecillion', 'sexdecillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e51''' ),

    'septendecillion' :
        UnitInfo( 'constant', 'septemdecillion', 'septemdecillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e54''' ),

    'octodecillion' :
        UnitInfo( 'constant', 'octodecillion', 'octodecillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e57''' ),

    'novemdecillion' :
        UnitInfo( 'constant', 'novemdecillion', 'novemdecillion', '', [ 'novendecillion' ], [ 'constant' ],
                  '''One decillion:  10e60''' ),

    'vigintillion' :
        UnitInfo( 'constant', 'vigintillion', 'vigintillion', '', [ ], [ 'constant' ],
                  '''One decillion:  10e63''' ),

    'googol' :
        UnitInfo( 'constant', 'googol', 'googols', '', [ ], [ 'constant' ],
                  '''One googol:  10e100 or ten duotrigintillion, famously named in 1920 by 9-year-old Milton Sirotta''' ),

    'centillion' :
        UnitInfo( 'constant', 'centillion', 'centillion', '', [ ], [ 'constant' ],
                  '''One centillion:  10e303''' ),

    # current

    'abampere' :
        UnitInfo( 'current', 'abampere', 'abamperes', 'abA', [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ],
                  '''
                  ''' ),

    'ampere' :
        UnitInfo( 'current', 'ampere', 'amperes', 'A', [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ],
                  '''
                  ''' ),

    'coulomb/second' :
        UnitInfo( 'current', 'coulomb/second', 'coulombs/second', 'C/s', [ 'C/sec', 'coulomb/sec', 'coulombs/sec', 'coulomb/s', 'coulombs/s' ], [ 'SI' ],
                  '''
                  ''' ),

    'statampere' :
        UnitInfo( 'current', 'statampere', 'statamperes', 'statA', [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ],
                  '''
                  ''' ),

    # data_rate

    'bit/second' :
        UnitInfo( 'data_rate', 'bit/second', 'bits/second', 'b/s', [ 'bit/s', 'bits/s', 'bit/sec', 'bits/sec', 'b/sec', 'b/second' ], [ 'computing' ],
                  '''
                  ''' ),

    'byte/second' :
        UnitInfo( 'data_rate', 'byte/second', 'bytes/second', 'B/s', [ 'byte/s', 'bytes/s' 'byte/sec', 'bytes/sec', 'B/sec', 'B/second' ], [ 'computing' ],
                  '''
                  ''' ),

    # density

    'kilogram/liter' :
        UnitInfo( 'density', 'kilogram/liter', 'kilograms/liter', 'kg/l', [ '' ], [ 'SI' ],
                  '''
                  ''' ),

    'kilogram/meter^3' :
        UnitInfo( 'density', 'kilogram/meter^3', 'kilograms/meter^3', 'kg/m^3', [ '' ], [ 'SI' ],
                  '''
                  ''' ),

    'density_of_water' :
        UnitInfo( 'density', 'x density_of_water', 'x density_of_water', '', [ 'water' ], [ 'natural' ],
                  '''
                  ''' ),

    # dynamic_viscosity

#pound per foot hour                 lb/(ft*h)    1 lb/(ft*h)   = 4.133 789e-4 Pa*s
#pound per foot second               lb/(ft*s)    1 lb/(ft*s)   = 1.488164 Pa*s
#pound-force second per square foot  lbf*s/ft2    1 lbf*s/ft2   = 47.88026 Pa*s
#pound-force second per square inch  lbf*s/in2    1 lbf*s/in2   = 6,894.757 Pa*s

    'kilogram/meter-second' :
        UnitInfo( 'dynamic_viscosity', 'kilogram/meter*second', 'kilogram/meter*second', 'kg/m*s', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'newton-second/meter^2' :
        UnitInfo( 'dynamic_viscosity', 'newton*second/meter^2', 'newton*second/meter^2', 'N*s/m^2', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'pascal-second' :
        UnitInfo( 'dynamic_viscosity', 'pascal*second', 'pascal-seconds', 'Pa*s', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'poise' :
        UnitInfo( 'dynamic_viscosity', 'poise', 'poise', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # electric_potential

    'abvolt' :
        UnitInfo( 'electric_potential', 'abvolt', 'abvolts', 'abV', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'coulomb/farad' :
        UnitInfo( 'electric_potential', 'coulomb/farad', 'coulombs/farad', 'C/F', [ 'coulomb/F', 'coulombs/F', 'C/farad', 'C/farads', 'coulombs/farads' ], [ 'SI' ],
                  '''
                  ''' ),

    'volt' :
        UnitInfo( 'electric_potential', 'volt', 'volts', 'V', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'watt/ampere' :
        UnitInfo( 'electric_potential', 'watt/ampere', 'watts/ampere', 'W/A', [ 'watt/amp', 'watt/amps', 'watt/A', 'watts/amp', 'watts/amps', 'watts/A', 'W/amp', 'W/amps', 'W/ampere', 'W/amperes' ], [ 'SI' ],
                  '''
                  ''' ),

    'statvolt' :
        UnitInfo( 'electric_potential', 'statvolt', 'statvolts', 'statV', [ 'esu_potential' ], [ 'CGS' ],
                  '''
                  ''' ),

    # electrical_conductance

    'abmho' :
        UnitInfo( 'electrical_conductance', 'abmho', 'abmhos', '', [ 'absiemens' ], [ 'CGS' ],
                  '''
                  ''' ),

    'ampere/volt' :
        UnitInfo( 'electrical_conductance', 'ampere/volt', 'amperes/volt', 'A/V', [ 'amp/V', 'amps/V', 'ampere/V', 'amperes/V', 'A/volt', 'amp/volt', 'amps/volt', 'A/volts', 'amp/volts', 'amps/volts', 'amperes/volts', ], [ 'SI' ],
                  '''
                  ''' ),

    'conductance_quantum' :
        UnitInfo( 'electrical_conductance', 'conductance_quantum', 'conductance_quanta', 'G0', [ ], [ 'SI' ],
                  '''
                  The conductance quantum appears when measuring the conductance of a quantum point contact,
                  and, more generally, is a key component of Landauer formula which relates the electrical
                  conductance of a quantum conductor to its quantum properties. It is twice the reciprocal
                  of the von Klitzing constant (2/RK). (https://en.wikipedia.org/wiki/Conductance_quantum)
                  ''' ),

    'second^3-ampere^2/kilogram-meter^2':
        UnitInfo( 'electrical_conductance', 'second^3*ampere^2/kilogram*meter^2', 'second^3*ampere^2/kilogram*meter^2', 's^3*A^2/kg*m^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'siemens' :
        UnitInfo( 'electrical_conductance', 'siemens', 'siemens', 'S', [ 'mho', 'mhos' ], [ 'SI' ],
                  '''
                  ''' ),

    'statmho' :
        UnitInfo( 'electrical_conductance', 'statmho', 'statmhos', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'statsiemens' :
        UnitInfo( 'electrical_conductance', 'statsiemens', 'statsiemens', 'statS', [ '' ], [ 'SI' ],
                  '''
                  ''' ),

    # electrical_resistance

    '1/siemens' :
        UnitInfo( 'electrical_resistance', '1/siemens', '1/siemens', '1/S', [ '1/mho' ], [ 'SI' ],
                  '''
                  ''' ),

    'abohm' :
        UnitInfo( 'electrical_resistance', 'abohm', 'abohms', 'o', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'german_mile' :
        UnitInfo( 'electrical_resistance', 'german_mile', 'german_miles', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'impedance_of_free_space' :
        UnitInfo( 'electrical_resistance', 'impedance_of_free_space', 'x impedance_of_free_space', 'Z0', [ 'vacuum_impedence' ], [ 'natural' ],
                  '''
                  ''' ),

    'jacobi' :
        UnitInfo( 'electrical_resistance', 'jacobi', 'jacobis', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'joule-second/coulomb^2' :
        UnitInfo( 'electrical_resistance', 'joule*second/coulomb^2', 'joule*second/coulomb^2', 'J*s/C^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'joule/second-ampere^2' :
        UnitInfo( 'electrical_resistance', 'joule/second*ampere^2', 'joule/second*ampere^2', 'J/s*A^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'kilogram-meter^2/second^3-ampere^2' :
        UnitInfo( 'electrical_resistance', 'kilogram*meter^2/second^3*ampere^2', 'kilogram*meter^2/second^3*ampere^2', 'kg*m^2/s^3*A^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'matthiessen' :
        UnitInfo( 'electrical_resistance', 'matthiessen', 'matthiessens', '', [ ], [ 'obsolete' ],   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                  '''
                  ''' ),

    'kilogram-meter^2/second-coulomb^2' :
        UnitInfo( 'electrical_resistance', 'kilogram*meter^2/second*coulomb^2', 'kilogram*meter^2/second*coulomb^2', 'm^2*kg/s*C^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'ohm' :
        UnitInfo( 'electrical_resistance', 'ohm', 'ohms', 'O', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'second/farad' :
        UnitInfo( 'electrical_resistance', 'second/farad', 'second/farad', 's/F', [ 's/farad', 's/farads', 'sec/farad', 'sec/farads', 'sec/F', 'second/F', 'seconds/F' ], [ 'SI' ],
                  '''
                  ''' ),

    'statohm' :
        UnitInfo( 'electrical_resistance', 'statohm', 'statohms', 'statO', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'varley' :
        UnitInfo( 'electrical_resistance', 'varley', 'varleys', '', [ ], [ 'obsolete' ],  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                  '''
                  ''' ),

    'volt/ampere' :
        UnitInfo( 'electrical_resistance', 'volt/ampere', 'volts/ampere', 'V/A', [ 'volt/amp', 'volt/amps', 'volt/A', 'volts/amp', 'volts/amps', 'volts/A', 'V/amp', 'V/amps', 'V/ampere', 'V/amperes' ], [ 'SI' ],
                  '''
                  ''' ),

    'watt/ampere^2' :
        UnitInfo( 'electrical_resistance', 'watt/ampere^2', 'watts/ampere^2', 'W/A^2', [ 'watt/amperes^2', 'watts/amperes^2', 'W/ampere^2', 'W/amperes^2' ], [ 'SI' ],
                  '''
                  ''' ),

    # energy

    'ampere-second-volt' :
        UnitInfo( 'energy', 'ampere*second*volt', 'ampere*second*volt', 'AVs', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'btu' :
        UnitInfo( 'energy', 'BTU', 'BTUs', '', [ 'btu', 'btus' ], [ 'England', 'US' ],
                  '''
                  ''' ),

    'calorie' :
        UnitInfo( 'energy', 'calorie', 'calories', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'electron-volt' :
        UnitInfo( 'energy', 'electron-volt', 'electron-volts', 'eV', [ 'electronvolt', 'electronvolts' ], [ 'science' ],
                  '''
                  ''' ),

    'erg' :
        UnitInfo( 'energy', 'erg', 'ergs', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'gram-equivalent' :
        UnitInfo( 'energy', 'gram-equivalent', 'grams-equivalent', 'gE', [ 'gram-energy', 'grams-energy', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ],
                  '''
                  ''' ),

    'hartree' :
        UnitInfo( 'energy', 'hartree', 'hartrees', 'Eh', [ ], [ 'science' ],
                  '''
                  ''' ),

    'horsepower-second' :
        UnitInfo( 'energy', 'horsepower*second', 'horsepower-seconds', 'hps', [ ], [ 'US' ],
                  '''
                  ''' ),

    'joule' :
        UnitInfo( 'energy', 'joule', 'joules', 'J', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'kilogram-meter^2/second^2' :
        UnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', 'kg*m^2/s^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'newton-meter' :
        UnitInfo( 'energy', 'newton*meter', 'newton-meters', 'N*m', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'pascal-meter^3' :
        UnitInfo( 'energy', 'pascal*meter^3', 'pascal*meter^3', 'Pa*m^3', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'rydberg' :
        UnitInfo( 'energy', 'rydberg', 'rydbergs', 'Ry', [ ], [ 'science' ],
                  '''
                  ''' ),

    'ton_of_TNT' :
        UnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT', [ ], [ 'informal' ],
                  '''
                  ''' ),

    'volt-coulomb' :
        UnitInfo( 'energy', 'volt*coulomb', 'volt*coulomb', 'VC', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'watt-second' :
        UnitInfo( 'energy', 'watt*second', 'watt-seconds', 'Ws', [ ], [ 'SI' ],
                  '''
                  ''' ),

    # force

    'dyne' :
        UnitInfo( 'force', 'dyne', 'dynes', 'dyn', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'gram-force' :
        UnitInfo( 'force', 'gram-force', 'grams-force', 'g-m', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'joule/meter' :
        UnitInfo( 'force', 'joule/meter', 'joule/meter', 'J/m', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'kilogram-meter/second^2' :
        UnitInfo( 'energy', 'kilogram*meter/second^2', 'kilogram*meter/second^2', 'kg*m/s^2', [ ], [ 'SI' ],
                  '''
                  This is the definition of the SI derived unit Newton (N).
                  ''' ),

    'newton' :
        UnitInfo( 'force', 'newton', 'newtons', 'N', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'pond' :
        UnitInfo( 'force', 'pond', 'ponds', '', [ ], [ 'metric' ],
                  '''
                  ''' ),

    'pound-foot/second^2' :
        UnitInfo( 'force', 'pound*foot/second^2', 'pound*foot/second^2', 'lb*ft/sec^2', [ ], [ 'FPS' ],
                  '''
                  ''' ),

    'poundal' :
        UnitInfo( 'force', 'poundal', 'poundals', 'pdl', [ ], [ 'England' ],
                  '''
                  ''' ),

    'sthene' :
        UnitInfo( 'force', 'sthene', 'sthenes', 'sn', [ 'funal' ], [ 'MTS' ],
                  '''
                  ''' ),

    # frequency

    'hertz' :
        UnitInfo( 'frequency', 'hertz', 'hertz', 'Hz', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'every_minute' :
        UnitInfo( 'frequency', 'x every_minute', 'x every minute', '', [ ], [ ],
                  '''
                  ''' ),

    'hourly' :
        UnitInfo( 'frequency', 'x hourly', 'x hourly', '', [ ], [ ],
                  '''
                  ''' ),

    'daily' :
        UnitInfo( 'frequency', 'x daily', 'x daily', '', [ ], [ ],
                  '''
                  ''' ),

    'weekly' :
        UnitInfo( 'frequency', 'x weekly', 'x weekly', '', [ ], [ ],
                  '''
                  ''' ),

    'monthly' :
        UnitInfo( 'frequency', 'x monthly', 'x monthly', '', [ ], [ ],
                  '''
                  ''' ),

    'yearly' :
        UnitInfo( 'frequency', 'x yearly', 'x yearly', '', [ ], [ ],
                  '''
                  ''' ),

    'becquerel' :
        UnitInfo( 'frequency', 'becquerel', 'becquerels', 'Bq', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'curie' :
        UnitInfo( 'frequency', 'curie', 'curies', 'Ci', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'rutherford' :
        UnitInfo( 'frequency', 'rutherford', 'rutherfords', 'rd', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    # illuminance

    'footcandle' :
        UnitInfo( 'illuminance', 'footcandle', 'footcandles', 'fc', [ ], [ 'FPS' ],
                  '''
                  ''' ),

    'lux' :
        UnitInfo( 'illuminance', 'lux', 'lux', 'lx', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'lumen/meter^2' :
        UnitInfo( 'illuminance', 'lumen/meter^2', 'lumens/meter^2', 'lm/m^2', [ 'lm/square_meter', 'lumen/square_meter', 'lumens/square_meter', 'lumen/m^2', 'lumens/m^2' ], [ 'SI' ],
                  '''
                  ''' ),

    'lumen/foot^2' :
        UnitInfo( 'illuminance', 'lumen/foot^2', 'lumens/foot^2', 'lm/ft^2', [ 'lm/square_foot', 'lumen/square_foot', 'lumens/square_foot', 'lumen/ft^2', 'lumens/ft^2' ], [ 'FPS' ],
                  '''
                  ''' ),

    'nox' :
        UnitInfo( 'illuminance', 'nox', 'nox', 'nx', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'phot' :
        UnitInfo( 'illuminance', 'phot', 'phots', 'ph', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # inductance

    'abhenry' :
        UnitInfo( 'inductance', 'abhenry', 'abhenries', 'abH', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'henry' :
        UnitInfo( 'inductance', 'henry', 'henries', 'H', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'weber/ampere' :
        UnitInfo( 'inductance', 'weber/ampere', 'webers/ampere', 'Wb/A', [ 'Wb/ampere', 'Wb/ampere', 'weber/A', 'webers/A', 'Wb/amp', 'weber/amp', 'webers/amp' ], [ 'SI' ],
                  '''
                  ''' ),

    'stathenry' :
        UnitInfo( 'inductance', 'stathenry', 'stathenries', 'statH', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # information_entropy

    'ban' :
        UnitInfo( 'information_entropy', 'ban', 'bans', '', [ 'hartley', 'hartleys', 'dit', 'dits' ], [ 'IEC' ],
                  '''
                  ''' ),

    'bit' :
        UnitInfo( 'information_entropy', 'bit', 'bits', 'b', [ 'shannon', 'shannons' ], [ 'computing' ],
                  '''A 'binary digit', which can store two values.''' ),

    'byte' :
        UnitInfo( 'information_entropy', 'byte', 'bytes', 'B', [ 'octet', 'octets' ], [ 'computing' ],
                  '''The traditional unit of computer storage, whose value has varied over the years and on different platforms,'''
                  '''but is now commonly defined to be 8 bits in size.''' ),

    'btupf' :
        UnitInfo( 'information_entropy', 'btupf', 'btupf', '', [ ], [ 'England' ],
                  '''
                  ''' ),

    'clausius' :
        UnitInfo( 'information_entropy', 'clausius', 'clausius', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'dword' :
        UnitInfo( 'information_entropy', 'dword', 'dwords', '', [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ],
                  '''A 'double-word' consisting of 2 16-bits words, or 32 bits total.''' ),

    'joule/kelvin' :
        UnitInfo( 'information_entropy', 'joule/kelvin', 'joules/kelvin', 'J/K', [ 'joule/K', 'joules/K' ], [ 'SI' ],
                  '''
                  ''' ),

    'library_of_congress' :
        UnitInfo( 'information_entropy', 'library_of_congress', 'libraries_of_congress', 'LoC', [ 'congress', 'congresses', 'loc' ], [ 'computing' ],
                  '''An informal unit of information measurement based on the contents of the U.S. Library of Congress, estimated to be'''
                  '''the equivalent of 10 terabytes in size.''' ),

    'nibble' :
        UnitInfo( 'information_entropy', 'nibble', 'nibbles', '', [ 'nybble', 'nybbles' ], [ 'computing' ],
                  '''A nybble is a half-byte, or 4 bits.  A nybble can be represented by a single hexadecimal digit.''' ),

    'nat' :
        UnitInfo( 'information_entropy', 'nat', 'nats', '', [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ],
                  '''
                  ''' ),

    'nyp' :
        UnitInfo( 'information_entropy', 'nyp', 'nyps', '', [ ], [ 'computing' ],   # suggested by Donald Knuth
                  '''A nyp is a term suggested by Knuth to represent two bits.  It is not a commonly used term.''' ),

    'oword' :
        UnitInfo( 'information_entropy', 'oword', 'owords', '', [ 'octaword', 'octawords' ], [ 'computing' ],
                  '''An 'octo-word' consisting of 8 16-bit words or 128 bits total.''' ),

    'qword' :
        UnitInfo( 'information_entropy', 'qword', 'qwords', '', [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ],
                  '''A 'quad-word' consisting of 4 16-bit words, or 64 bits total.''' ),

    'trit' :
        UnitInfo( 'information_entropy', 'trit', 'trits', '', [ ], [ 'computing' ],
                  '''A trit is a 'ternary digit', by extension from the term 'bit' for 'binary digit'.  In 1958 the Setun '''
                  '''balanced ternary computer was developed at Moscow State University, which used trits and 6-trit trytes.''' ),

    'tryte' :
        UnitInfo( 'information_entropy', 'tryte', 'trytes', '', [ ], [ 'computing' ],
                  '''A tryte consists of 6 trits (i.e., 'ternary digits'), and is named by extension from the term 'byte'.  In 1958 the Setun '''
                  '''balanced ternary computer was developed at Moscow State University, which used trits and 6-trit trytes.''' ),

    'word' :
        UnitInfo( 'information_entropy', 'word', 'words', '', [ 'short_integer', 'short_integers', 'wyde' ], [ 'computing' ],
                  '''A word is traditionally two bytes, or 16 bits.  The term 'wyde' was suggested by Knuth.''' ),

    # length

    'aln' :
        UnitInfo( 'length', 'aln', 'alns', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'arpent' :
        UnitInfo( 'length', 'arpent', 'arpents', '', [ ], [ 'obsolete', 'France' ],
                  '''
                  ''' ),

    'angstrom' :
        UnitInfo( 'length', 'angstrom', 'angstroms', 'A', [ 'angstroem' ], [ 'science' ],
                  '''
                  ''' ),

    'astronomical_unit' :
        UnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au', [ ], [ 'science' ],
                  '''
                  ''' ),

    'barleycorn' :
        UnitInfo( 'length', 'barleycorn', 'barleycorns', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'bolt' :
        UnitInfo( 'length', 'bolt', 'bolts', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'caliber' :
        UnitInfo( 'length', 'caliber', 'caliber', '', [ 'calibre' ], [ 'US' ],
                  '''
                  ''' ),

    'chain' :
        UnitInfo( 'length', 'chain', 'chains', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'cubit' :
        UnitInfo( 'length', 'cubit', 'cubits', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'ell' :
        UnitInfo( 'length', 'ell', 'ells', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'famn' :
        UnitInfo( 'length', 'famn', 'famns', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'farshimmelt_potrzebie' :
        UnitInfo( 'length', 'farshimmelt_potrzebie', 'farshimmelt potrzebies', 'fpz', [ 'far-potrzebie' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'fathom' :
        UnitInfo( 'length', 'fathom', 'fathoms', 'fath', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'fermi' :
        UnitInfo( 'length', 'fermi', 'fermis', '', [ ], [ '' ],
                  '''
                  ''' ),

    'finger' :
        UnitInfo( 'length', 'finger', 'fingers', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'fingerbreadth' :
        UnitInfo( 'length', 'fingerbreadth', 'fingerbreadths', '', [ 'fingersbreadth' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'foot' :
        UnitInfo( 'length', 'foot', 'feet', 'ft', [ ], [ 'traditional', 'FPS' ],
                  '''
                  ''' ),

    'furlong' :
        UnitInfo( 'length', 'furlong', 'furlongs', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'furshlugginer_potrzebie' :
        UnitInfo( 'length', 'furshlugginer_potrzebie', 'furshlugginer potrzebies', 'Fpz', [ 'Fur-potrzebie' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'greek_cubit' :
        UnitInfo( 'length', 'greek_cubit', 'greek_cubits', '', [ ], [ 'obsolete', 'Greece' ],
                  '''
                  ''' ),

    'gutenberg' :
        UnitInfo( 'length', 'gutenberg', 'gutenbergs', '', [ ], [ 'typography' ],
                  '''
                  ''' ),

    'hand' :
        UnitInfo( 'length', 'hand', 'hands', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'handbreadth' :
        UnitInfo( 'length', 'handbreadth', 'handbreadths', '', [ 'handsbreadth' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'inch' :
        UnitInfo( 'length', 'inch', 'inches', 'in', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'ken' :
        UnitInfo( 'length', 'ken', 'kens', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'kyu' :
        UnitInfo( 'length', 'kyu', 'kyus', '', [ 'Q' ], [ 'typography', 'computing' ],
                  '''
                  ''' ),

    'league' :
        UnitInfo( 'length', 'league', 'leagues', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'light-second' :
        UnitInfo( 'length', 'light-second', 'light-seconds', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'light-year' :
        UnitInfo( 'length', 'light-year', 'light-years', 'ly', [ 'a1' ], [ 'science' ],
                  '''
                  ''' ),

    'link' :
        UnitInfo( 'length', 'link', 'links', '', [ ], [ 'informal' ],
                  '''
                  ''' ),

    'long_cubit' :
        UnitInfo( 'length', 'long_cubit', 'long_cubits', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'long_reed' :
        UnitInfo( 'length', 'long_reed', 'long_reeds', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'marathon' :
        UnitInfo( 'length', 'marathon', 'marathons', '', [ ], [ 'informal' ],
                  '''
                  ''' ),

    'meter' :
        UnitInfo( 'length', 'meter', 'meters', 'm', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'micron' :
        UnitInfo( 'length', 'micron', 'microns', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'mil' :
        UnitInfo( 'length', 'mil', 'mils', '', [ 'thou' ], [ 'US' ],
                  '''
                  ''' ),

    'mile' :
        UnitInfo( 'length', 'mile', 'miles', 'mi', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'nail' :
        UnitInfo( 'length', 'nail', 'nails', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'nautical_mile' :
        UnitInfo( 'length', 'nautical_mile', 'nautical_miles', '', [ ], [ 'nautical' ],
                  '''
                  ''' ),

    'parsec' :
        UnitInfo( 'length', 'parsec', 'parsecs', 'pc', [ ], [ 'science' ],
                  '''
                  ''' ),

    'perch' :
        UnitInfo( 'length', 'perch', 'perches', '', [ 'pole', 'poles' ], [ 'imperial' ],
                  '''
                  ''' ),

    'pica' :
        UnitInfo( 'length', 'pica', 'picas', '', [ 'cicero' ], [ 'typography' ],
                  '''
                  ''' ),

    'point' :
        UnitInfo( 'length', 'point', 'points', '', [ ], [ 'typography' ],
                  '''
                  ''' ),

    'poppyseed' :
        UnitInfo( 'length', 'poppyseed', 'poppyseeds', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'reed' :
        UnitInfo( 'length', 'reed', 'reeds', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'rod' :
        UnitInfo( 'length', 'rod', 'rods', 'rd', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'rope' :
        UnitInfo( 'length', 'rope', 'ropes', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'potrzebie' :
        UnitInfo( 'length', 'potrzebie', 'potrzebies', 'pz', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'siriometer' :
        UnitInfo( 'length', 'siriometer', 'siriometers', '', [ ], [ 'science' ],  # proposed in 1911 by Cark V. L. Charlier
                  '''
                  ''' ),

    'skein' :
        UnitInfo( 'length', 'skein', 'skeins', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'smoot' :
        UnitInfo( 'length', 'smoot', 'smoots', '', [ ], [ 'humorous' ],
                  '''
                  ''' ),

    'span' :
        UnitInfo( 'length', 'span', 'spans', '', [ 'breadth' ], [ 'imperial' ],
                  '''
                  ''' ),

    'twip' :
        UnitInfo( 'length', 'twip', 'twips', '', [ ], [ 'computing' ],
                  '''
                  ''' ),

    'yard' :
        UnitInfo( 'length', 'yard', 'yards', 'yd', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    # luminance

    'apostilb' :
        UnitInfo( 'luminance', 'apostilb', 'apostilbs', 'asb', [ 'blondel' ], [ 'CGS' ],
                  '''
                  ''' ),

    'bril' :
        UnitInfo( 'luminance', 'bril', 'brils', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'candela/meter^2' :
        UnitInfo( 'luminance', 'candela/meter^2', 'candelas/meter^2', 'cd/m^2', [ 'candela/m^2', 'candelas/m^2', 'candela/square_meter', 'candelas/square_meter', 'cd/square_meter' ], [ 'SI' ],
                  '''
                  ''' ),

    'footlambert' :
        UnitInfo( 'luminance', 'footlambert', 'footlamberts', 'fL', [ 'foot-lambert', 'foot-lamberts' ], [ 'US', 'obsolete' ],
                  '''
                  ''' ),

    'lambert' :
        UnitInfo( 'luminance', 'lambert', 'lamberts', 'L', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'nit' :
        UnitInfo( 'luminance', 'nit', 'nits', 'nt', [ 'meterlambert', 'meter-lambert', 'meterlamberts', 'meter-lamberts' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'skot' :
        UnitInfo( 'luminance', 'skot', 'skots', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'stilb' :
        UnitInfo( 'luminance', 'stilb', 'stilbs', 'sb', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # luminous_flux

    'lumen' :
        UnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'candela-steradian' :
        UnitInfo( 'luminous_flux', 'candela-steradian', 'candela-steradians', 'cd*sr', [ 'cd-sr' ], [ 'SI' ],
                  '''
                  ''' ),

    # luminous_intensity

    'candela' :
        UnitInfo( 'luminous_intensity', 'candela', 'candelas', 'cd', [ 'candle' ], [ 'SI' ],
                  '''
                  ''' ),

    'hefnerkerze' :
        UnitInfo( 'luminous_intensity', 'hefnerkerze', 'hefnerkerze', 'HK', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    # magnetic_field_strength

    'ampere/meter' :
        UnitInfo( 'magnetic_field_strength', 'ampere/meter', 'amperes/meter', 'A/m', [ 'amp/m', 'amps/m', 'ampere/m', 'amperes/m', 'A/meter', 'amp/meter', 'amps/meter', 'A/meters', 'amp/meters', 'amps/meters', 'ampere/meters', 'amperes/meters' ], [ 'SI' ],
                  '''
                  ''' ),

    'oersted' :
        UnitInfo( 'magnetic_field_strength', 'oersted', 'oersted', 'Oe', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    # magnetic_flux

    'gauss-centimeter^2' :
        UnitInfo( 'magnetic_flux', 'gauss*centimeter^2', 'gauss*centimeter^2', 'gauss*cm^2', [ 'gauss*square_cm' ], [ 'CGS' ],
                  '''
                  ''' ),

    'maxwell' :
        UnitInfo( 'magnetic_flux', 'maxwell', 'maxwells', 'Mx', [ 'line' ], [ 'CGS' ],
                  '''
                  ''' ),

    'volt-second' :
        UnitInfo( 'magnetic_flux', 'volt*second', 'volts*seconds', 'V*s', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'unit_pole' :
        UnitInfo( 'magnetic_flux', 'unit_pole', 'unit_poles', '', [ 'unitpole', 'unitpoles' ], [ 'CGS' ],
                  '''
                  ''' ),

    'tesla-meter^2' :
        UnitInfo( 'magnetic_flux', 'tesla*meter^2', 'tesla*meter^2', 'T/m^2', [ 'tesla*square_meter', 'teslas*square_meter', 'T*square_meter', 'tesla*m^2', 'teslas*m^2', 'teslas*meter^2' ], [ 'SI' ],
                  '''
                  ''' ),

    'weber' :
        UnitInfo( 'magnetic_flux', 'weber', 'webers', 'Wb', [ ], [ 'SI' ],
                  '''
                  ''' ),

    # magnetic_flux_density

    'gauss' :
        UnitInfo( 'magnetic_flux_density', 'gauss', 'gauss', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'kilogram/ampere-second^2' :
        UnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', 'kilogram/ampere*second^2', 'kg/A*s^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'maxwell/centimeter^2' :
        UnitInfo( 'magnetic_flux_density', 'maxwell/centimeter^2', 'maxwells/centimeter^2', 'Mx/cm^2', [ 'maxwell/cm^2', 'maxwells/cm^2', 'Mx/centimeter^2', 'Mx/square_centimeter', 'Mx/square_cm', 'maxwell/square_centimeter', 'maxwells/square_centimeter', 'maxwell/square_cm', 'maxwells/square_cm' ], [ 'CGS' ],
                  '''
                  ''' ),

    'tesla' :
        UnitInfo( 'magnetic_flux_density', 'tesla', 'teslas', 'T', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'volt-second/meter^2' :
        UnitInfo( 'magnetic_flux_density', 'volt*second/meter^2', 'volt*second/meter^2', '', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'weber/meter^2' :
        UnitInfo( 'magnetic_flux_density', 'weber/meter^2', 'webers/meter^2', 'Wb/m^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    # mass

    'blintz' :
        UnitInfo( 'mass', 'blintz', 'blintzes', 'b', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'carat' :
        UnitInfo( 'mass', 'carat', 'carats', 'kt', [ 'karat', 'karats' ], [ 'US' ],
                  '''
                  ''' ),

    'chandrasekhar_limit' :
        UnitInfo( 'mass', 'chandrasekhar_limit', 'x chandrasekhar_limit', '', [ 'chandrasekhar' ], [ 'science' ],
                  '''
                  ''' ),

    'dalton' :
        UnitInfo( 'mass', 'dalton', 'daltons', '', [ 'amu', 'atomic_mass_unit' ], [ 'science' ],
                  '''
                  ''' ),

    'doppelzentner' :
        UnitInfo( 'mass', 'doppelzentner', 'doppelzentners', '', [ ], [ 'Germany' ],
                  '''
                  ''' ),

    'farshimmelt_blintz' :
        UnitInfo( 'mass', 'farshimmelt_blintz', 'farshimmelt_blintzes', 'fb', [ 'far-blintz' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'furshlugginer_blintz' :
        UnitInfo( 'mass', 'furshlugginer_blintz', 'furshlugginer_blintzes', 'Fb', [ 'Fur-blintz' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'grain' :
        UnitInfo( 'mass', 'grain', 'grains', 'gr', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'gram' :
        UnitInfo( 'mass', 'gram', 'grams', 'g', [ 'gramme', 'grammes' ], [ 'SI' ],
                  '''
                  ''' ),

    'kip' :
        UnitInfo( 'mass', 'kip', 'kips', '', [ 'kilopound', 'kilopounds' ], [ 'US' ],
                  '''
                  ''' ),

    'ounce' :
        UnitInfo( 'mass', 'ounce', 'ounces', 'oz', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'pennyweight' :
        UnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt', [ 'pwt' ], [ 'traditional', 'England' ],
                  '''
                  ''' ),

    'pfund' :
        UnitInfo( 'mass', 'pfund', 'pfunds', '', [ ], [ 'Germany' ],
                  '''
                  ''' ),

    'pound' :
        UnitInfo( 'mass', 'pound', 'pounds', 'lb', [ ], [ 'US', 'traditional', 'FPS' ],
                  '''
                  ''' ),

    'quintal' :
        UnitInfo( 'mass', 'quintal', 'quintals', 'q', [ ], [ ],
                  '''
                  ''' ),

    'sheet' :
        UnitInfo( 'mass', 'sheet', 'sheets', '', [ ], [ ],
                  '''
                  ''' ),

    'slug' :
        UnitInfo( 'mass', 'slug', 'slugs', '', [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ],
                  '''
                  ''' ),

    'stone' :
        UnitInfo( 'mass', 'stone', 'stone', '', [ ], [ 'traditional', 'England' ],
                  '''
                  ''' ),

    'stone_us' :
        UnitInfo( 'mass', 'stone_us', 'stones_us', '', [ 'us_stone', 'us_stones' ], [ 'US' ],
                  '''
                  ''' ),

    'ton' :
        UnitInfo( 'mass', 'ton', 'tons', '', [ ], [ 'traditional', 'US' ],
                  '''
                  ''' ),

    'tonne' :
        UnitInfo( 'mass', 'tonne', 'tonnes', '', [ ], [ 'MTS' ],
                  '''
                  ''' ),

    'troy_ounce' :
        UnitInfo( 'mass', 'troy_ounce', 'troy_ounces', '', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'troy_pound' :
        UnitInfo( 'mass', 'troy_pound', 'troy_pounds', '', [ ], [ 'traditional'  ],
                  '''
                  ''' ),

    'wey' :
        UnitInfo( 'mass', 'wey', 'weys', '', [ ], [ 'obsolete', 'England' ],
                  '''
                  ''' ),

    'zentner' :
        UnitInfo( 'mass', 'zentner', 'zentners', '', [ ], [ 'Germany' ],
                  '''
                  ''' ),

    # power

    'dBm' :
        UnitInfo( 'power', 'dBm', 'dBm', 'dBm', [ 'dBmW', 'decibel-milliwatt' ], [ 'engineering' ],
                  '''
                  ''' ),

    'erg/second' :
        UnitInfo( 'power', 'erg/second', 'ergs/second', 'erg/s', [ 'ergs/s' ], [ 'CGS' ],
                  '''
                  ''' ),

    'horsepower' :
        UnitInfo( 'power', 'horsepower', 'horsepower', 'hp', [ ], [ 'US' ],
                  '''
                  ''' ),

    'joule/second' :
        UnitInfo( 'power', 'joule/second', 'joules/second', 'J/s', [ 'joule/s', 'joules/s', 'J/sec', 'joule/sec', 'joules/sec', 'J/seconds', 'joule/seconds', 'joules/seconds' ], [ 'SI' ],
                  '''
                  ''' ),

    'lusec' :
        UnitInfo( 'power', 'lusec', 'lusecs', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'kilogram-meter^2/second^3' :
        UnitInfo( 'power', 'kilogram*meter^2/second^3', 'kilogram*meter^2/second^3', 'kg*m^2/s^3', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'newton-meter/second' :
        UnitInfo( 'power', 'newton*meter/second', 'newton*meter/second', 'N*m/s', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'pferdestarke' :
        UnitInfo( 'power', 'pferdestarke', 'pferdestarke', '', [ ], [ 'obsolete', 'Germany' ],
                  '''
                  ''' ),

    'poncelet' :
        UnitInfo( 'power', 'poncelet', 'poncelets', '', [ ], [ 'obsolete' ],
                  '''
                  ''' ),

    'volt-ampere' :
        UnitInfo( 'power', 'volt*ampere', 'volt-amperes', 'VA', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'watt' :
        UnitInfo( 'power', 'watt', 'watts', 'W', [ ], [ 'SI' ],
                  '''
                  ''' ),

    # pressure

    'atmosphere' :
        UnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm', [ ], [ 'natural' ],
                  '''
                  ''' ),

    'bar' :
        UnitInfo( 'pressure', 'bar', 'bars', '', [ ], [ ],
                  '''
                  ''' ),

    'barye' :
        UnitInfo( 'pressure', 'barye', 'baryes', 'Ba', [ 'barad' ], [ 'CGS' ],
                  '''
                  ''' ),

    'mmHg' :
        UnitInfo( 'pressure', 'mmHg', 'mmHg', '', [ ], [ 'metric' ],
                  '''
                  ''' ),

    'kilogram/meter-second^2' :
        UnitInfo( 'pressure', 'kilogram/meter*second^2', 'kilogram/meter*second^2', 'kg/m*s^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'newton/meter^2' :
        UnitInfo( 'pressure', 'newton/meter^2', 'newtons/meter^2', 'N/m^2', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'pascal' :
        UnitInfo( 'pressure', 'pascal', 'pascals', 'Pa', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'pieze' :
        UnitInfo( 'pressure', 'pieze', 'piezes', '', [ ], [ 'MTS' ],
                  '''
                  ''' ),

    'psi' :
        UnitInfo( 'pressure', 'pound/inch^2', 'pounds/inch^2', 'psi', [ 'lb/in^2' ], [ 'FPS' ],
                  '''
                  ''' ),

    'torr' :
        UnitInfo( 'pressure', 'torr', 'torr', '', [ ], [ ],
                  '''
                  ''' ),

    # radiation_dose

    'banana_equivalent_dose' :
        UnitInfo( 'radiation_dose', 'banana_equivalent_dose', 'banana_equivalent_doses', '', [ 'banana' ], [ 'natural' ],
                  '''
                  ''' ),

    'gray' :
        UnitInfo( 'radiation_dose', 'gray', 'grays', 'Gy', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'joule/kilogram' :
        UnitInfo( 'radiation_dose', 'joule/kilogram', 'joules/kilogram', 'J/kg', [ 'joule/kg', 'joules/kg', 'J/kilogram', 'J/kilograms', 'joule/kilograms', 'joules/kilograms' ], [ 'SI' ],
                  '''
                  ''' ),

    'rad' :
        UnitInfo( 'radiation_dose', 'rad', 'rads', '', [ ], [ 'CGS' ],
                  '''
                  ''' ),

    'rem' :
        UnitInfo( 'radiation_dose', 'rem', 'rems', '', [ 'roentgen_equivalent_man' ], [ 'CGS' ],
                  '''
                  ''' ),

    'sievert' :
        UnitInfo( 'radiation_dose', 'sievert', 'sieverts', 'Sv', [ ], [ 'SI' ],
                  '''
                  ''' ),

    # radiation_exposure

    'coulomb/kilogram' :
        UnitInfo( 'radiation_exposure', 'coulomb/kilogram', 'coulombs/kilogram', 'C/kg', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'roentgen' :
        UnitInfo( 'radiation_exposure', 'roentgen', 'roentgens', 'R', [ 'parker' ], [ 'NIST' ],
                  '''
                  ''' ),

    # solid_angle

    'sphere' :
        UnitInfo( 'solid_angle', 'sphere', 'spheres', '', [ ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_arcminute' :
        UnitInfo( 'solid_angle', 'arcminute^2', 'arcminutes^2', 'arcmin^2', [ 'square_arcminutes', 'solid_arcminute', 'solid_arcminutes', 'sq_arcminute', 'sq_arcminutes', 'sqarcmin', 'sqarcmins', 'arcmins^2', 'spherical_minute', 'spherical_minutes' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_arcsecond' :
        UnitInfo( 'solid_angle', 'arcsecond^2', 'arcseconds^2', 'arcsec^2', [ 'square_arcseconds', 'solid_arcsecond', 'solid_arcseconds', 'sq_arcsecond', 'sq_arcseconds', 'sqarcsec', 'sqarcsecs', 'arcsecs^2', 'spherical_second', 'spherical_seconds' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_degree' :
        UnitInfo( 'solid_angle', 'degree^2', 'degrees^2', 'deg^2', [ 'square_degrees', 'sqdeg', 'solid_degree', 'solid_degrees', 'sq_degree', 'sq_degrees', 'sqdeg', 'sqdegs', 'spherical_degree', 'spherical_degrees' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_octant' :
        UnitInfo( 'solid_angle', 'octant^2', 'octants^2', '', [ 'square_octants', 'sqoctant', 'sqoctants', 'solid_octant', 'solid_octants', 'sq_octant', 'sq_octants', 'spherical_octant', 'spherical_octants' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_quadrant' :
        UnitInfo( 'solid_angle', 'quadrant^2', 'quadrants^2', '', [ 'square_quadrants', 'sqquadrant', 'sqquadrants', 'solid_quadrant', 'solid_quadrants', 'sq_quadrant', 'sq_quadrants', 'spherical_quadrant', 'spherical_quadrants' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_quintant' :
        UnitInfo( 'solid_angle', 'quintant^2', 'quintants^2', '', [ 'square_quintants', 'sqquintant', 'sqquintants', 'solid_quintant', 'solid_quintants', 'sq_quintant', 'sq_quintants', 'spherical_quintant', 'spherical_quintants' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_sextant' :
        UnitInfo( 'solid_angle', 'sextant^2', 'sextants^2', '', [ 'square_sextants', 'sqsextant', 'sqsextants', 'solid_sextant', 'solid_sextants', 'sq_sextant', 'sq_sextants', 'spherical_sextant', 'spherical_sextants' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'square_grad' :
        UnitInfo( 'solid_angle', 'grad^2', 'grads^2', '', [ 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'sq_gon', 'sq_gons','sqgon', 'sqgons', 'grad^2', 'grads^2', 'gon^2', 'gons^2', 'spherical_gon', 'spherical_gons', 'spherical_grad', 'spherical_grads' ], [ 'mathematics' ],
                  '''
                  ''' ),

    'steradian' :
        UnitInfo( 'solid_angle', 'steradian', 'steradians', 'sr', [ 'square_radian', 'square_radians', 'sq_radian', 'sq_radians', 'sq_rad', 'sqrad', 'radian^2', 'radians^2', 'rad^2', 'spherical_radian', 'spherical_radians' ], [ 'SI', 'mathematics' ],
                  '''
                  ''' ),

    # temperature

    'celsius' :
        UnitInfo( 'temperature', 'celsius', 'degrees_celsius', '', [ 'centigrade', 'degC', 'degreesC' ], [ 'SI' ],
                  '''
                  ''' ),

    'degree_newton' :
        UnitInfo( 'temperature', 'degree_newton', 'degrees_newton', '', [ 'newton_degree', 'newton_degrees', 'degN', 'degreesN' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'delisle' :
        UnitInfo( 'temperature', 'delisle', 'degrees_delisle', 'De', [ 'degD', 'degreesD' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'fahrenheit' :
        UnitInfo( 'temperature', 'fahrenheit', 'degrees_fahrenheit', '', [ 'fahr', 'degF', 'degreesF' ], [ 'US', 'traditional' ],
                  '''
                  ''' ),

    'kelvin' :
        UnitInfo( 'temperature', 'kelvin', 'degrees_kelvin', 'K', [ 'degK', 'degreesK' ], [ 'SI' ],
                  '''
                  ''' ),

    'rankine' :
        UnitInfo( 'temperature', 'rankine', 'degrees_rankine', 'R', [ 'degR', 'degreesR' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'reaumur' :
        UnitInfo( 'temperature', 'reaumur', 'degrees_reaumur', 'Re', [ 'degRe', 'degreesRe' ], [ 'obsolete' ],
                  '''
                  ''' ),

    'romer' :
        UnitInfo( 'temperature', 'romer', 'degrees_romer', 'Ro', [ 'degRo', 'degreesRo' ], [ 'obsolete' ],
                  '''
                  ''' ),

    # time

    'beat' :
        UnitInfo( 'time', 'beat', 'beat', '', [ ], [ ],
                  '''
                  ''' ),

    'blink' :
        UnitInfo( 'time', 'blink', 'blink', '', [ ], [ ],
                  '''
                  ''' ),

    'century' :
        UnitInfo( 'time', 'century', 'centuries', '', [ ], [ 'traditional', 'US', 'years' ],
                  '''
                  ''' ),

    'clarke' :
        UnitInfo( 'time', 'clarke', 'clarkes', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'cowznofski' :
        UnitInfo( 'time', 'cowznofski', 'cowznofskis', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'day' :
        UnitInfo( 'time', 'day', 'days', 'd', [ ], [ 'traditional', 'US' ],
                  '''
                  ''' ),

    'decade' :
        UnitInfo( 'time', 'decade', 'decades', '', [ ], [ 'traditional', 'years' ],
                  '''
                  ''' ),

    'fortnight' :
        UnitInfo( 'time', 'fortnight', 'fortnights', '', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'gregorian_year' :
        UnitInfo( 'time', 'gregorian_year', 'gregorian_years', '', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'hour' :
        UnitInfo( 'time', 'hour', 'hours', 'hr', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'kovac' :
        UnitInfo( 'time', 'kovac', 'kovacs', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'jiffy' :
        UnitInfo( 'time', 'jiffy', 'jiffies', '', [ ], [ 'computing' ],
                  '''
                  ''' ),

    'lustrum' :
        UnitInfo( 'time', 'lustrum', 'lustra', '', [ ], [ 'obsolete', 'years' ],
                  '''
                  ''' ),

    'martin' :
        UnitInfo( 'time', 'martin', 'martins', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'microcentury' :
        UnitInfo( 'time', 'microcentury', 'microcenturies', '', [ ], [ 'humorous', 'computing' ],
                  '''
                  ''' ),

    'microfortnight' :
        UnitInfo( 'time', 'microfortnight', 'microfortnights', '', [ ], [ 'humorous', 'computing' ],
                  '''
                  ''' ),

    'mingo' :
        UnitInfo( 'time', 'mingo', 'mingoes', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'minute' :
        UnitInfo( 'time', 'minute', 'minutes', '', [ ], [ 'traditional' ],  # 'min' is already an operator
                  '''
                  ''' ),

    'month' :
        UnitInfo( 'time', 'month', 'months', 'mo', [ ], [ 'traditional', 'months' ],
                  '''
                  ''' ),

    'nanocentury' :
        UnitInfo( 'time', 'nanocentury', 'nanocenturies', '', [ ], [ 'humorous', 'computing' ],
                  '''
                  ''' ),

    'second' :
        UnitInfo( 'time', 'second', 'seconds', '', [ ], [ 'SI', 'traditional', 'FPS' ],   # 'sec' is already an operator
                  '''
                  ''' ),

    'shake' :
        UnitInfo( 'time', 'shake', 'shakes', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_day' :
        UnitInfo( 'time', 'sidereal_day', 'sidereal_days', '', [ 'earth_day' ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_hour' :
        UnitInfo( 'time', 'sidereal_hour', 'sidereal_hours', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_minute' :
        UnitInfo( 'time', 'sidereal_minute', 'sidereal_minutes', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_month' :
        UnitInfo( 'time', 'sidereal_month', 'sidereal_months', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_second' :
        UnitInfo( 'time', 'sidereal_second', 'sidereal_seconds', '', [ ], [ 'science' ],
                  '''
                  ''' ),

    'sidereal_year' :
        UnitInfo( 'time', 'sidereal_year', 'sidereal_years', '', [ 'earth_year' ], [ 'science' ],
                  '''
                  ''' ),

    'svedberg' :
        UnitInfo( 'time', 'svedberg', 'svedbergs', '', [ ], [ ],
                  '''
                  ''' ),

    'tropical_year' :
        UnitInfo( 'time', 'tropical_year', 'tropical_years', '', [ 'solar_year', 'solar_years' ], [ 'science' ],
                  '''
                  ''' ),

    'week' :
        UnitInfo( 'time', 'week', 'weeks', 'wk', [ 'sennight' ], [ 'traditional', 'obsolete' ],
                  '''
                  ''' ),

    'wolverton' :
        UnitInfo( 'time', 'wolverton', 'wolvertons', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'wood' :
        UnitInfo( 'time', 'wood', 'woods', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'year' :
        UnitInfo( 'time', 'year', 'years', '', [ 'annum', 'julian_year', 'julian_years' ], [ 'traditional', 'years' ],
                  '''
                  ''' ),

    # velocity

    'kine' :
        UnitInfo( 'velocity', 'kine', 'kine', '', [ '' ], [ 'CGS' ],
                  '''
                  ''' ),

    'meter/second' :
        UnitInfo( 'velocity', 'meter/second', 'meters/second', 'm/s', [ 'mps' ], [ 'SI' ],
                  '''
                  ''' ),

    'knot' :
        UnitInfo( 'velocity', 'knot', 'knots', 'kt', [ ], [ 'nautical' ],
                  '''
                  ''' ),

    'light' :
        UnitInfo( 'velocity', 'light', 'x_light', '', [ 'light' ], [ 'natural' ],
                  '''
                  ''' ),

    'mach' :
        UnitInfo( 'velocity', 'mach', 'mach', '', [ ], [ 'US' ],
                  '''
                  ''' ),

    'mile/hour' :
        UnitInfo( 'velocity', 'mile/hour', 'miles/hour', 'mph', [ 'mi/hr' ], [ 'FPS', 'imperial' ],
                  '''
                  ''' ),

    'kilometer/hour' :
        UnitInfo( 'velocity', 'kilometer/hour', 'kilometers/hour', 'km/h', [ 'kph' ], [ 'FPS', 'imperial' ],
                  '''
                  ''' ),

    # volume

    'acre-foot' :
        UnitInfo( 'volume', 'acre*foot', 'acre-feet', 'ac*ft', [ ], [ 'FPS', 'imperial' ],
                  '''
                  ''' ),

    'balthazar' :
        UnitInfo( 'volume', 'balthazar', 'balthazars', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'bucket' :
        UnitInfo( 'volume', 'bucket', 'buckets', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'bushel' :
        UnitInfo( 'volume', 'bushel', 'bushels', 'bu', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'chopine' :
        UnitInfo( 'volume', 'chopine', 'chopines', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'clavelin' :
        UnitInfo( 'volume', 'clavelin', 'clavelins', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'cord' :
        UnitInfo( 'volume', 'cord', 'cords', '', [ ], [ 'traditional' ],
                  '''
                  ''' ),

    'cubic_inch' :
        UnitInfo( 'volume', 'inch^3', 'cubic_inches', 'in^3', [ 'inches^3', 'cuin', 'cu_in', 'cu_inch', 'cu_inches', 'cubic_in' ], [ 'traditional' ],
                  '''
                  ''' ),

    'cubic_foot' :
        UnitInfo( 'volume', 'foot^3', 'cubic_feet', 'ft^3', [ 'feet^3', 'cuft', 'cu_ft', 'cu_foot', 'cu_feet', 'cubic_ft' ], [ 'traditional', 'FPS' ],
                  '''
                  ''' ),

    'cubic_meter' :
        UnitInfo( 'volume', 'meter^3', 'cubic_meters', 'm^3', [ 'meters^3', 'cum', 'cu_m', 'cu_meter', 'cu_meters', 'cubic_m' ], [ 'SI' ],
                  '''
                  ''' ),

    'coomb' :
        UnitInfo( 'volume', 'coomb', 'coombs', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'cup' :
        UnitInfo( 'volume', 'cup', 'cups', '', [ ], [ 'traditional', 'cooking', 'US' ],
                  '''
                  ''' ),

    'dash' :
        UnitInfo( 'volume', 'dash', 'dashes', '', [ ], [ 'cooking' ],
                  '''
                  ''' ),

    'demi' :
        UnitInfo( 'volume', 'demi', 'demis', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'dessertspoon' :
        UnitInfo( 'volume', 'dessertspoon', 'dessertspoons', '', [ ], [ 'traditional', 'cooking' ],
                  '''
                  ''' ),

    'dram' :
        UnitInfo( 'volume', 'dram', 'drams', '', [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ],
                  '''
                  ''' ),

    'dry_barrel' :
        UnitInfo( 'volume', 'dry_barrel', 'dry_barrels', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'dry_hogshead' :
        UnitInfo( 'volume', 'dry_hogshead', 'dry_hogsheads', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'dry_gallon' :
        UnitInfo( 'volume', 'dry_gallon', 'dry_gallons', '', [ ], [ 'traditional', 'US' ],
                  '''
                  ''' ),

    'dry_pint' :
        UnitInfo( 'volume', 'dry_pint', 'dry_pints', '', [ ], [ 'traditional', 'US' ],
                  '''
                  ''' ),

    'dry_quart' :
        UnitInfo( 'volume', 'dry_quart', 'dry_quarts', '', [ ], [ 'traditional', 'US' ],
                  '''
                  ''' ),

    'dry_tun' :
        UnitInfo( 'volume', 'dry_tun', 'dry_tuns', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'farshimmelt_ngogn' :
        UnitInfo( 'volume', 'farshimmelt_ngogn', 'farshimmelt_ngogns', 'fn', [ 'far-ngogn' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'fifth' :
        UnitInfo( 'volume', 'fifth', 'fifths', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'firkin' :
        UnitInfo( 'volume', 'firkin', 'firkins', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'fluid_ounce' :
        UnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', '', [ 'floz' ], [ 'traditional' ],
                  '''
                  ''' ),

    'furshlugginer_ngogn' :
        UnitInfo( 'volume', 'furshlugginer_ngogn', 'furshlugginer_ngogns', 'Fn', [ 'Fur-ngogn' ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'gallon' :
        UnitInfo( 'volume', 'gallon', 'gallons', 'gal', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'gill' :
        UnitInfo( 'volume', 'gill', 'gills', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'goliath' :
        UnitInfo( 'volume', 'goliath', 'goliaths', '', [ 'primat' ], [ 'wine' ],
                  '''
                  ''' ),

    'hogshead' :
        UnitInfo( 'volume', 'hogshead', 'hogsheads', '', [ ], [ 'traditional', 'wine' ],
                  '''
                  ''' ),

    'imperial' :
        UnitInfo( 'volume', 'imperial', 'imperials', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'imperial_bushel' :
        UnitInfo( 'volume', 'imperial_bushel', 'imperial_bushels', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_butt' :
        UnitInfo( 'volume', 'imperial_butt', 'imperial_butts', '', [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_cup' :
        UnitInfo( 'volume', 'imperial_cup', 'imperial_cups', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_gallon' :
        UnitInfo( 'volume', 'imperial_gallon', 'imperial_gallons', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_gill' :
        UnitInfo( 'volume', 'imperial_gill', 'imperial_gills', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_hogshead' :
        UnitInfo( 'volume', 'imperial_hogshead', 'imperial_hogsheads', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_peck' :
        UnitInfo( 'volume', 'imperial_peck', 'imperial_pecks', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_pint' :
        UnitInfo( 'volume', 'imperial_pint', 'imperial_pints', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'imperial_quart' :
        UnitInfo( 'volume', 'imperial_quart', 'imperial_quarts', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'jack' :
        UnitInfo( 'volume', 'jack', 'jacks', '', [ 'jackpot' ], [ 'imperial' ],
                  '''
                  ''' ),

    'jennie' :
        UnitInfo( 'volume', 'jennie', 'jennies', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'jeroboam' :
        UnitInfo( 'volume', 'jeroboam', 'jeroboams', '', [ 'double_magnum' ], [ 'wine' ],
                  '''
                  ''' ),

    'jigger' :
        UnitInfo( 'volume', 'jigger', 'jiggers', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'kenning' :
        UnitInfo( 'volume', 'kenning', 'kennings', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'kilderkin' :
        UnitInfo( 'volume', 'kilderkin', 'kilderkins', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'liter' :
        UnitInfo( 'volume', 'liter', 'liters', 'l', [ ], [ 'SI' ],
                  '''
                  ''' ),

    'magnum' :
        UnitInfo( 'volume', 'magnum', 'magnums', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'marie_jeanne' :
        UnitInfo( 'volume', 'marie_jeanne', 'marie_jeannes', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'melchior' :
        UnitInfo( 'volume', 'melchior', 'melchiors', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'melchizedek' :
        UnitInfo( 'volume', 'melchizedek', 'melchizedeks', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'methuselah' :
        UnitInfo( 'volume', 'methuselah', 'methuselahs', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'minim':
        UnitInfo( 'volume', 'minim', 'minims', 'gtt', [ 'drop' ], [ 'traditional' ],
                  '''
                  ''' ),

    'mordechai' :
        UnitInfo( 'volume', 'mordechai', 'mordechais', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'nebuchadnezzar' :
        UnitInfo( 'volume', 'nebuchadnezzar', 'nebuchadnezzars', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'ngogn' :
        UnitInfo( 'volume', 'ngogn', 'ngogns', '', [ ], [ 'Potrzebie', 'humorous' ],
                  '''
                  ''' ),

    'oil_barrel' :
        UnitInfo( 'volume', 'oil_barrel', 'oil_barrels', 'bbl', [ ], [ 'US' ],
                  '''
                  ''' ),

    'peck' :
        UnitInfo( 'volume', 'peck', 'pecks', 'pk', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'piccolo' :
        UnitInfo( 'volume', 'piccolo', 'piccolos', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'pinch' :
        UnitInfo( 'volume', 'pinch', 'pinches', '', [ ], [ 'traditional', 'cooking' ],
                  '''
                  ''' ),

    'pin' :
        UnitInfo( 'volume', 'pin', 'pins', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'pint' :
        UnitInfo( 'volume', 'pint', 'pints', 'pt', [ ], [ 'traditional', 'cooking', 'US' ],
                  '''
                  ''' ),

    'pipe' :
        UnitInfo( 'volume', 'pipe', 'pipes', '', [ 'butt', 'butts' ], [ 'imperial' ],
                  '''
                  ''' ),

    'pony' :
        UnitInfo( 'volume', 'pony', 'ponies', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'pottle' :
        UnitInfo( 'volume', 'pottle', 'pottles', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'puncheon' :
        UnitInfo( 'volume', 'puncheon', 'puncheons', '', [ 'tertian', 'tertians' ], [ 'wine' ],
                  '''
                  ''' ),

    'quart' :
        UnitInfo( 'volume', 'quart', 'quarts', '', [ ], [ 'US' ],
                  '''
                  ''' ),

    'rehoboam' :
        UnitInfo( 'volume', 'rehoboam', 'rehoboams', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'rundlet' :
        UnitInfo( 'volume', 'rundlet', 'rundlets', '', [ ], [ 'imperial', 'wine' ],
                  '''
                  ''' ),

    'salmanazar' :
        UnitInfo( 'volume', 'salmanazar', 'salmanazars', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'scruple' :
        UnitInfo( 'volume', 'scruple', 'scruples', '', [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ],
                  '''
                  ''' ),

    'smidgen' :
        UnitInfo( 'volume', 'smidgen', 'smidgens', '', [ 'smidgeon', 'smidgeons' ], [ 'traditional', 'cooking' ],
                  '''
                  ''' ),

    'solomon' :
        UnitInfo( 'volume', 'solomon', 'solomons', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'sovereign' :
        UnitInfo( 'volume', 'sovereign', 'sovereigns', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'standard' :
        UnitInfo( 'volume', 'standard', 'standards', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'stere' :
        UnitInfo( 'volume', 'stere', 'steres', 'st', [ ], [ 'metric', 'obsolete' ],  # ... but not SI
                  '''
                  ''' ),

    'strike' :
        UnitInfo( 'volume', 'strike', 'strikes', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'tablespoon' :
        UnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp', [ ], [ 'traditional', 'cooking', 'US' ],
                  '''
                  ''' ),

    'teaspoon' :
        UnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp', [ ], [ 'traditional', 'cooking', 'US' ],
                  '''
                  ''' ),

    'tenth' :
        UnitInfo( 'volume', 'tenth', 'tenths', '', [ ], [ 'wine' ],
                  '''
                  ''' ),

    'tierce' :
        UnitInfo( 'volume', 'tierce', 'tierces', '', [ ], [ 'wine', 'imperial' ],
                  '''
                  ''' ),

    'tun' :
        UnitInfo( 'volume', 'tun', 'tuns', '', [ ], [ 'imperial' ],
                  '''
                  ''' ),

    'wine_barrel' :
        UnitInfo( 'volume', 'wine_barrel', 'wine_barrels', '', [ ], [ 'imperial', 'wine' ],
                  '''
                  ''' ),

    'wine_butt' :
        UnitInfo( 'volume', 'wine_butt', 'wine_butts', '', [ ], [ 'imperial', 'wine' ],
                  '''
                  ''' ),

    'wine_gallon' :
        UnitInfo( 'volume', 'wine_gallon', 'wine_gallons', '', [ ], [ 'imperial', 'wine' ],
                  '''
                  ''' ),

    'wine_hogshead' :
        UnitInfo( 'volume', 'wine_hogshead', 'wine_hogsheads', '', [ ], [ 'imperial', 'wine' ],
                  '''
                  ''' ),

    'wine_pipe' :
        UnitInfo( 'volume', 'wine_pipe', 'wine_pipes', '', [ 'wine_butt', 'wine_butts' ], [ 'imperial' ],
                  '''
                  ''' ),

    'wine_tun' :
        UnitInfo( 'volume', 'wine_tun', 'wine_tuns', '', [ ], [ 'imperial', 'wine' ],
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
    ( 'ampere-second',      'ampere-seconds',   'As',   [ 'amp-second' ], [ 'amp-seconds' ] ),
    ( 'are',                'ares',             'a',    [ ], [ ] ),
    ( 'bar',                'bars',             'bar',  [ ], [ ] ),
    ( 'barn',               'barns',            'bn',   [ ], [ ] ),     # 'bn' is not standard
    ( 'becquerel',          'becquerels',       'Bq',   [ ], [ ] ),
    ( 'blintz',             'blintzes',         'bl',   [ ], [ ] ),
    ( 'coulomb',            'coulombs',         'C',    [ ], [ ] ),
    ( 'calorie',            'calories',         'cal',  [ 'cal' ], [ 'cals' ] ),
    ( 'electron-volt',      'electron-volts',   'eV',   [ ], [ ] ),
    ( 'farad',              'farads',           'F',    [ ], [ ] ),
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
    ( 'mole',               'moles',            'mol',  [ ], [ ] ),
    ( 'newton',             'newtons',          'N',    [ ], [ ] ),
    ( 'ngogn',              'ngogns',           'ng',   [ ], [ ] ),
    ( 'ohm',                'ohms',             'O',    [ ], [ ] ),
    ( 'parsec',             'parsecs',          'pc',   [ ], [ ] ),
    ( 'pascal',             'pascals',          'Pa',   [ ], [ ] ),
    ( 'pascal-second',      'pascal-seconds',   'Pas',  [ ], [ ] ),
    ( 'pond',               'ponds',            'pond', [ ], [ ] ),     # 'p' is used for 'pico'
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
    ( 'acre',                       'nanoacre' )                            : mpmathify( '1.0e9' ),
    ( 'acre',                       'square_yard' )                         : mpmathify( '4840' ),
    ( 'acre-foot',                  'cubic_foot' )                          : mpmathify( '43560' ),
    ( 'aln',                        'inch' )                                : mpmathify( '23.377077865' ),
    ( 'ampere',                     'coulomb/second' )                      : mpmathify( '1' ),
    ( 'ampere',                     'statampere' )                          : mpmathify( '299792458' ),
    ( 'ampere-second-volt',         'joule' )                               : mpmathify( '1' ),
    ( 'arcminute',                  'arcsecond' )                           : mpmathify( '60' ),
    ( 'arcsecond',                  'milliarcsecond' )                      : mpmathify( '1000' ),
    ( 'are',                        'square_meter' )                        : mpmathify( '100' ),
    ( 'arpent',                     'foot' )                                : mpmathify( '192' ),
    ( 'astronomical_unit',          'meter' )                               : mpmathify( '149597870691' ),
    ( 'atmosphere',                 'pascal' )                              : mpmathify( '101325' ),
    ( 'balthazar',                  'liter' )                               : mpmathify( '12.0' ),
    ( 'ban',                        'nat' )                                 : log( 10 ),
    ( 'banana_equivalent_dose',     'sievert' )                             : mpmathify( '9.8e-8' ),
    ( 'bar',                        'pascal' )                              : mpmathify( '1.0e5' ),
    ( 'barleycorn',                 'poppyseed' )                           : mpmathify( '4' ),
    ( 'beat',                       'blink' )                               : mpmathify( '100' ),
    ( 'becquerel',                  'curie' )                               : mpmathify( '3.7e10' ),
    ( 'billion',                    'unity' )                               : mpmathify( '1.0e9' ),
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
    ( 'calorie',                    'joule' )                               : mpmathify( '4.184' ),
    ( 'carat',                      'grain' )                               : fadd( 3, fdiv( 1, 6 ) ),
    ( 'carucate',                   'acre' )                                : mpmathify( '120' ),
    ( 'carucate',                   'bovate' )                              : mpmathify( '8' ),
    ( 'centillion',                 'unity' )                               : mpmathify( '1.0e303' ),
    ( 'century',                    'microcentury' )                        : mpmathify( '1.0e6' ),
    ( 'century',                    'nanocentury' )                         : mpmathify( '1.0e9' ),
    ( 'century',                    'year' )                                : mpmathify( '100' ),
    ( 'chain',                      'yard' )                                : mpmathify( '22' ),
    ( 'chandrasekhar_limit',        'gram' )                                : mpmathify( '2.765e33' ),
    ( 'chopine',                    'liter' )                               : mpmathify( '0.25' ),
    ( 'clarke',                     'day' )                                 : mpmathify( '1' ),
    ( 'clarke',                     'wolverton' )                           : mpmathify( '1.0e6' ),
    ( 'clausius',                   'joule/kelvin' )                        : mpmathify( '4186.8' ),
    ( 'clavelin',                   'liter' )                               : mpmathify( '0.62' ),
    ( 'conductance_quantum',        'siemens' )                             : mpmathify( '7.7480917310e-5' ),
    ( 'coomb',                      'strike' )                              : mpmathify( '2' ),
    ( 'cord',                       'cubic_foot' )                          : mpmathify( '128' ),
    ( 'coulomb',                    'ampere-second' )                       : mpmathify( '1' ),
    ( 'coulomb',                    'farad-volt' )                          : mpmathify( '1' ),
    ( 'coulomb/farad',              'volt' )                                : mpmathify( '1' ),
    ( 'coulomb/kilogram',           'roentgen' )                            : mpmathify( '3876' ),
    ( 'coulomb/volt',               'farad' )                               : mpmathify( '1' ),
    ( 'cowznofski',                 'mingo' )                               : mpmathify( '10' ),
    ( 'cubic_meter',                'liter' )                               : mpmathify( '1000' ),
    ( 'cubit',                      'inch' )                                : mpmathify( '18' ),
    ( 'cup',                        'dram' )                                : mpmathify( '64' ),
    ( 'cup',                        'fluid_ounce' )                         : mpmathify( '8' ),
    ( 'cup',                        'gill' )                                : mpmathify( '2' ),
    ( 'daily',                      'monthly' )                             : mpmathify( '30' ),
    ( 'daily',                      'weekly' )                              : mpmathify( '7' ),
    ( 'daily',                      'yearly' )                              : mpmathify( '365.25' ),
    ( 'day',                        'beat' )                                : mpmathify( '1000' ),
    ( 'day',                        'hour' )                                : mpmathify( '24' ),
    ( 'decade',                     'year' )                                : mpmathify( '10' ),
    ( 'decillion',                  'unity' )                               : mpmathify( '1.0e33' ),
    ( 'degree',                     'arcminute' )                           : mpmathify( '60' ),
    ( 'degree',                     'streck' )                              : mpmathify( '17.5' ),
    ( 'demi',                       'liter' )                               : mpmathify( '0.375' ),
    ( 'density_of_water',           'kilogram/liter' )                      : mpmathify( '1.0' ),
    ( 'density_of_water',           'kilogram/meter^3' )                    : mpmathify( '1.0e3' ),
    ( 'dessertspoon',               'teaspoon' )                            : mpmathify( '2' ),
    ( 'doppelzentner',              'zentner' )                             : mpmathify( '2' ),
    ( 'dozen',                      'unity' )                               : mpmathify( '12' ),
    ( 'dram',                       'scruple' )                             : mpmathify( '3' ),
    ( 'dry_barrel',                 'bushel' )                              : mpmathify( '4' ),
    ( 'dry_barrel',                 'cubic_inch' )                          : mpmathify( '7056' ),
    ( 'dry_gallon',                 'dry_quart' )                           : mpmathify( '4' ),
    ( 'dry_hogshead',               'dry_barrel' )                          : mpmathify( '2' ),
    ( 'dry_pint',                   'cubic_inch' )                          : mpmathify( '33.6003125' ),
    ( 'dry_quart',                  'dry_pint' )                            : mpmathify( '2' ),
    ( 'dry_tun',                    'dry_hogshead' )                        : mpmathify( '4' ),
    ( 'duodecillion',               'unity' )                               : mpmathify( '1.0e39' ),
    ( 'dword',                      'bit' )                                 : mpmathify( '32' ),
    ( 'ell',                        'inch' )                                : mpmathify( '45' ),
    ( 'every_minute',               'hourly' )                              : mpmathify( '60' ),
    ( 'famn',                       'aln' )                                 : mpmathify( '3' ),
    ( 'farad',                      'jar' )                                 : mpmathify( '9.0e8' ),
    ( 'farad',                      'statfarad' )                           : mpmathify( '898755178736.5' ),
    ( 'faraday',                    'coulomb' )                             : mpmathify( '96485.3383' ),
    ( 'fathom',                     'foot' )                                : mpmathify( '6' ),
    ( 'finger',                     'inch' )                                : mpmathify( '4.5' ),
    ( 'fingerbreadth',              'inch' )                                : mpmathify( '0.75' ),
    ( 'firkin',                     'gallon' )                              : mpmathify( '9' ),
    ( 'firkin',                     'pin' )                                 : mpmathify( '2' ),
    ( 'flock',                      'unity' )                               : mpmathify( '40' ),
    ( 'fluid_ounce',                'dram' )                                : mpmathify( '8' ),
    ( 'fluid_ounce',                'tablespoon' )                          : mpmathify( '2' ),
    ( 'foot',                       'inch' )                                : mpmathify( '12' ),
    ( 'footcandle',                 'lumen/foot^2' )                        : mpmathify( '1' ),
    ( 'footcandle',                 'lux' )                                 : mpmathify( '10.763910417' ),            # (m/ft)^2
    ( 'footlambert',                'candela/meter^2' )                     : mpmathify( '3.42625909963539052691' ),  # 1/pi cd/ft^2
    ( 'fortnight',                  'day' )                                 : mpmathify( '14' ),
    ( 'fortnight',                  'microfortnight' )                      : mpmathify( '1.0e6' ),
    ( 'furlong',                    'yard' )                                : mpmathify( '220' ),
    ( 'galileo',                    'meter/second^2' )                      : mpmathify( '100' ),
    ( 'gallon',                     'fifth' )                               : mpmathify( '5' ),
    ( 'gallon',                     'quart' )                               : mpmathify( '4' ),
    ( 'gauss',                      'maxwell/centimeter^2' )                : mpmathify( '1' ),
    ( 'goliath',                    'liter' )                               : mpmathify( '27.0' ),
    ( 'googol',                     'unity' )                               : mpmathify( '1.0e100' ),
    ( 'grad',                       'degree' )                              : mpmathify( '0.9' ),
    ( 'gram',                       'dalton' )                              : mpmathify( '1.66053886e-24' ),
    ( 'gram-equivalent',            'joule' )                               : fdiv( power( mpf( '299792458' ), 2 ), 1000 ),
    ( 'gray',                       'joule/kilogram' )                      : mpmathify( '1' ),
    ( 'gray',                       'rad' )                                 : mpmathify( '100' ),
    ( 'great_gross',                'gross' )                               : mpmathify( '12' ),
    ( 'greek_cubit',                'inch' )                                : mpmathify( '18.22' ),
    ( 'gross',                      'unity' )                               : mpmathify( '144' ),
    ( 'handbreadth',                'inch' )                                : mpmathify( '3' ),
    ( 'hartree',                    'rydberg' )                             : mpmathify( '2' ),
    ( 'hefnerkerze',                'candela' )                             : mpmathify( '0.920' ),  # approx.
    ( 'henry',                      'abhenry' )                             : mpmathify( '1.0e9' ),
    ( 'henry',                      'weber/ampere' )                        : mpmathify( '1' ),
    ( 'hertz',                      'every_minute' )                        : mpmathify( '60' ),
    ( 'homestead',                  'acre' )                                : mpmathify( '160' ),
    ( 'horsepower',                 'watt' )                                : mpmathify( '745.69987158227022' ),
    ( 'horsepower-second',          'joule' )                               : mpmathify( '745.69987158227022' ),
    ( 'hour',                       'minute' )                              : mpmathify( '60' ),
    ( 'hourly',                     'daily' )                               : mpmathify( '24' ),
    ( 'hundred',                    'unity' )                               : mpmathify( '100' ),
    ( 'impedance_of_free_space',    'ohm' )                                 : fmul( pi, mpmathify( '119.9169832' ) ),
    ( 'imperial_bushel',            'kenning' )                             : mpmathify( '2' ),
    ( 'imperial_butt',              'imperial_hogshead' )                   : mpmathify( '2' ),
    ( 'imperial_cup',               'imperial_gill' )                       : mpmathify( '2' ),
    ( 'imperial_gallon',            'pottle' )                              : mpmathify( '2' ),
    ( 'imperial_gill',              'jack' )                                : mpmathify( '2' ),
    ( 'imperial_hogshead',          'coomb' )                               : mpmathify( '2' ),
    ( 'imperial_peck',              'imperial_quart' )                      : mpmathify( '2' ),
    ( 'imperial_pint',              'imperial_cup' )                        : mpmathify( '2' ),
    ( 'imperial_quart',             'imperial_pint' )                       : mpmathify( '2' ),
    ( 'imperial_square',            'square_foot' )                         : mpmathify( '100' ),
    ( 'inch',                       'barleycorn' )                          : mpmathify( '3' ),
    ( 'inch',                       'caliber' )                             : mpmathify( '100' ),
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
    ( 'joule',                      'electron-volt' )                       : mpmathify( '6.24150974e18' ),
    ( 'joule',                      'erg' )                                 : mpmathify( '1.0e7' ),
    ( 'joule',                      'kilogram-meter^2/second^2' )           : mpmathify( '1' ),
    ( 'joule/second',               'watt' )                                : mpmathify( '1' ),
    ( 'ken',                        'inch' )                                : mpmathify( '83.4' ),
    ( 'kenning',                    'imperial_peck' )                       : mpmathify( '2' ),
    ( 'kilderkin',                  'firkin' )                              : mpmathify( '2' ),
    ( 'kip',                        'pound' )                               : mpmathify( '1000' ),
    ( 'kovac',                      'wolverton' )                           : mpmathify( '10' ),
    ( 'lambert',                    'candela/meter^2' )                     : fdiv( 10000, pi ),
    ( 'league',                     'mile' )                                : mpmathify( '3' ),
    ( 'library_of_congress',        'byte' )                                : mpmathify( '1.0e13' ),
    ( 'light',                      'meter/second' )                        : mpmathify( '299792458' ),
    ( 'light-second',               'meter' )                               : mpmathify( '299792458' ),
    ( 'light-year',                 'light-second' )                        : mpmathify( '31557600' ),
    ( 'link',                       'inch' )                                : mpmathify( '7.92' ),
    ( 'liter',                      'ngogn' )                               : mpmathify( '86.2477899004' ),
    ( 'long_cubit',                 'inch' )                                : mpmathify( '21' ),
    ( 'long_hundred',               'unity' )                               : mpmathify( '120' ),
    ( 'long_reed',                  'foot' )                                : mpmathify( '10.5' ),
    ( 'lustrum',                    'year' )                                : mpmathify( '5' ),
    ( 'lux',                        'lumen/meter^2' )                       : mpmathify( '1' ),
    ( 'lux',                        'nox' )                                 : mpmathify( '1000' ),
    ( 'mach',                       'meter/second' )                        : mpmathify( '295.0464' ),
    ( 'magnum',                     'liter' )                               : mpmathify( '1.5' ),
    ( 'marathon',                   'yard' )                                : mpmathify( '46145' ),
    ( 'marie_jeanne',               'liter' )                               : mpmathify( '2.25' ),
    ( 'martin',                     'kovac' )                               : mpmathify( '100' ),
    ( 'maxwell',                    'gauss-centimeter^2' )                  : mpmathify( '1' ),
    ( 'melchior',                   'liter' )                               : mpmathify( '18.0' ),
    ( 'melchizedek',                'liter' )                               : mpmathify( '30.0' ),
    ( 'meter',                      'angstrom' )                            : mpmathify( '1.0e10' ),
    ( 'meter',                      'fermi' )                               : mpmathify( '1.0e15' ),
    ( 'meter',                      'kyu' )                                 : mpmathify( '4000' ),
    ( 'meter',                      'micron' )                              : mpmathify( '1.0e6' ),
    ( 'meter/second',               'kine' )                                : mpmathify( '100' ),
    ( 'meter/second',               'knot' )                                : mpmathify( '1.943844492' ),
    ( 'methuselah',                 'liter' )                               : mpmathify( '6.0' ),
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
    ( 'newton',                     'dyne' )                                : mpmathify( '1.0e5' ),
    ( 'newton',                     'joule/meter' )                         : mpmathify( '1' ),
    ( 'newton',                     'kilogram-meter/second^2' )             : mpmathify( '1' ),
    ( 'newton',                     'pond' )                                : mpmathify( '101.97161298' ),
    ( 'newton',                     'poundal' )                             : mpmathify( '7.233013851' ),
    ( 'newton-second/meter^2',      'pascal-second' )                       : mpmathify( '1' ),
    ( 'newton/meter^2',             'pascal' )                              : mpmathify( '1' ),
    ( 'ngogn',                      'farshimmelt_ngogn' )                   : mpmathify( '1.0e5' ),
    ( 'ngogn',                      'furshlugginer_ngogn' )                 : mpmathify( '1.0e-6' ),
    ( 'nibble',                     'bit' )                                 : mpmathify( '4' ),
    ( 'nit',                        'apostilb' )                            : pi,
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'nonillion',                  'unity' )                               : mpmathify( '1.0e30' ),
    ( 'novemdecillion',             'unity' )                               : mpmathify( '1.0e60' ),
    ( 'nyp',                        'bit' )                                 : mpmathify( '2' ),
    ( 'octant',                     'degree' )                              : mpmathify( '45' ),
    ( 'octillion',                  'unity' )                               : mpmathify( '1.0e27' ),
    ( 'octodecillion',              'unity' )                               : mpmathify( '1.0e57' ),
    ( 'oersted',                    'ampere/meter' )                        : mpmathify( '79.5774715' ),
    ( 'ohm',                        '1/siemens' )                           : mpmathify( '1' ),
    ( 'ohm',                        'abohm' )                               : mpmathify( '1e9' ),
    ( 'ohm',                        'german_mile' )                         : mpmathify( '57.44' ),
    ( 'ohm',                        'jacobi' )                              : mpmathify( '0.6367' ),
    ( 'ohm',                        'joule-second/coulomb^2' )              : mpmathify( '1' ),
    ( 'ohm',                        'joule/second-ampere^2' )               : mpmathify( '1' ),
    ( 'ohm',                        'kilogram-meter^2/second-coulomb^2' )   : mpmathify( '1' ),
    ( 'ohm',                        'kilogram-meter^2/second^3-ampere^2' )  : mpmathify( '1' ),
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
    ( 'pascal',                     'kilogram/meter-second^2' )             : mpmathify( '1' ),
    ( 'pascal-meter^3',             'joule' )                               : mpmathify( '1' ),
    ( 'pascal-second',              'kilogram/meter-second' )               : mpmathify( '1' ),
    ( 'pascal-second',              'poise' )                               : mpmathify( '10' ),
    ( 'peck',                       'dry_gallon' )                          : mpmathify( '2' ),
    ( 'perch',                      'foot' )                                : mpmathify( '16.5' ),
    ( 'pferdestarke',               'watt' )                                : mpmathify( '735.49875' ),
    ( 'pfund',                      'gram' )                                : mpmathify( '500' ),
    ( 'phot',                       'lux' )                                 : mpmathify( '10000' ),
    ( 'piccolo',                    'liter' )                               : mpmathify( '0.1875' ),
    ( 'pieze',                      'pascal' )                              : mpmathify( '1000' ),
    ( 'pointangle',                 'degree' )                              : fdiv( 360, 32 ),
    ( 'poncelet',                   'watt' )                                : mpmathify( '980.665' ),
    ( 'pony',                       'dram' )                                : mpmathify( '6' ),
    ( 'potrzebie',                  'farshimmelt_potrzebie' )               : mpmathify( '1.0e5' ),
    ( 'potrzebie',                  'furshlugginer_potrzebie' )             : mpmathify( '1.0e-6' ),
    ( 'potrzebie',                  'meter' )                               : mpmathify( '0.002263348517438173216473' ),  # see Mad #33
    ( 'pottle',                     'imperial_quart' )                      : mpmathify( '2' ),
    ( 'pound',                      'grain' )                               : mpmathify( '7000' ),
    ( 'pound',                      'ounce' )                               : mpmathify( '16' ),
    ( 'pound',                      'sheet' )                               : mpmathify( '700' ),
    ( 'psi',                        'pascal' )                              : mpmathify( '6894.757' ),        # approx.
    ( 'quadrant',                   'degree' )                              : mpmathify( '90' ),
    ( 'quadrillion',                'unity' )                               : mpmathify( '1.0e15' ),
    ( 'quart',                      'cup' )                                 : mpmathify( '4' ),
    ( 'quart',                      'liter' )                               : mpmathify( '0.946352946' ),
    ( 'quart',                      'pint' )                                : mpmathify( '2' ),
    ( 'quattuordecillion',          'unity' )                               : mpmathify( '1.0e45' ),
    ( 'quindecillion',              'unity' )                               : mpmathify( '1.0e48' ),
    ( 'quintant',                   'degree' )                              : mpmathify( '72' ),
    ( 'quintillion',                'unity' )                               : mpmathify( '1.0e18' ),
    ( 'qword',                      'bit' )                                 : mpmathify( '64' ),
    ( 'radian',                     'centrad' )                             : mpmathify( '100' ),
    ( 'radian',                     'degree' )                              : fdiv( 180, pi ),
    ( 'reed',                       'foot' )                                : mpmathify( '9' ),
    ( 'rehoboam',                   'liter' )                               : mpmathify( '4.5' ),
    ( 'rod',                        'foot' )                                : mpmathify( '16.5' ),
    ( 'rood',                       'square_yard' )                         : mpmathify( '1210' ),
    ( 'rope',                       'foot' )                                : mpmathify( '20' ),
    ( 'rutherford',                 'becquerel' )                           : mpmathify( '1.0e6' ),
    ( 'rydberg',                    'joule' )                               : mpmathify( '2.179872e-18' ),
    ( 'salmanazar',                 'liter' )                               : mpmathify( '9.0' ),
    ( 'score',                      'unity' )                               : mpmathify( '20' ),
    ( 'scruple',                    'minim' )                               : mpmathify( '20' ),
    ( 'second',                     'jiffy' )                               : mpmathify( '100' ),
    ( 'second',                     'shake' )                               : mpmathify( '1.0e8' ),
    ( 'second',                     'svedberg' )                            : mpmathify( '1.0e13' ),
    ( 'section',                    'acre' )                                : mpmathify( '640' ),
    ( 'septendecillion',            'unity' )                               : mpmathify( '1.0e54' ),
    ( 'septillion',                 'unity' )                               : mpmathify( '1.0e24' ),
    ( 'sexdecillion',               'unity' )                               : mpmathify( '1.0e51' ),
    ( 'sextant',                    'degree' )                              : mpmathify( '60' ),
    ( 'sextillion',                 'unity' )                               : mpmathify( '1.0e21' ),
    ( 'shock',                      'unity' )                               : mpmathify( '60' ),
    ( 'siemens',                    'ampere/volt' )                         : mpmathify( '1' ),
    ( 'siemens',                    'kilogram-meter^2/second^3-ampere^2' )  : mpmathify( '1' ),
    ( 'siemens',                    'statsiemens' )                         : mpmathify( '898755178736.5' ),
    ( 'sievert',                    'rem' )                                 : mpmathify( '100' ),
    ( 'siriometer',                 'astronomical_unit' )                   : mpmathify( '1.0e6' ),
    ( 'skein',                      'foot' )                                : mpmathify( '360' ),
    ( 'skot',                       'bril' )                                : mpmathify( '1.0e4' ),
    ( 'skot',                       'lambert' )                             : mpmathify( '1.0e7' ),
    ( 'slug',                       'pound' )                               : mpmathify( '32.174048556' ),
    ( 'smoot',                      'inch' )                                : mpmathify( '67' ),
    ( 'solomon',                    'liter' )                               : mpmathify( '20.0' ),
    ( 'sovereign',                  'liter' )                               : mpmathify( '25.0' ),
    ( 'span',                       'inch' )                                : mpmathify( '9' ),
    ( 'sphere',                     'steradian' )                           : fmul( 4, pi ),
    ( 'square_arcminute',           'square_arcsecond' )                    : mpmathify( '3600' ),
    ( 'square_degree',              'square_arcminute' )                    : mpmathify( '3600' ),
    ( 'square_meter',               'barn' )                                : mpmathify( '1.0e28' ),
    ( 'square_meter',               'outhouse' )                            : mpmathify( '1.0e34' ),
    ( 'square_meter',               'shed' )                                : mpmathify( '1.0e52' ),
    ( 'square_octant',              'square_degree' )                       : mpmathify( '2025' ),
    ( 'square_quadrant',            'square_degree' )                       : mpmathify( '8100' ),
    ( 'square_sextant',             'square_degree' )                       : mpmathify( '3600' ),
    ( 'square_yard',                'square_foot' )                         : mpmathify( '9' ),
    ( 'standard',                   'liter' )                               : mpmathify( '0.75' ),
    ( 'statcoulomb',                'coulomb' )                             : mpmathify( '3.335641e-10' ),  # 0.1A*m/c, approx.
    ( 'statcoulomb',                'franklin' )                            : mpmathify( '1' ),
    ( 'stathenry',                  'henry' )                               : mpmathify( '898755178740' ),
    ( 'statmho',                    'siemens' )                             : mpmathify( '8.99e11' ),
    ( 'statohm',                    'ohm' )                                 : mpmathify( '898755178740' ),
    ( 'statvolt',                   'volt' )                                : fdiv( mpf( '299792458' ), mpf( '1.0e6' ) ),
    ( 'steradian',                  'square_degree' )                       : power( fdiv( 180, pi ), 2 ),
    ( 'steradian',                  'square_grad' )                         : power( fdiv( 200, pi ), 2 ),
    ( 'sthene',                     'newton' )                              : mpmathify( '1000' ),
    ( 'stilb',                      'candela/meter^2' )                     : mpmathify( '10000' ),
    ( 'stone',                      'pound' )                               : mpmathify( '14' ),
    ( 'stone_us',                   'pound' )                               : mpmathify( '12.5' ),
    ( 'strike',                     'imperial_bushel' )                     : mpmathify( '2' ),
    ( 'tablespoon',                 'teaspoon' )                            : mpmathify( '3' ),
    ( 'teaspoon',                   'dash' )                                : mpmathify( '8' ),
    ( 'teaspoon',                   'pinch' )                               : mpmathify( '16' ),
    ( 'teaspoon',                   'smidgen' )                             : mpmathify( '32' ),
    ( 'ten',                        'unity' )                               : mpmathify( '10' ),
    ( 'tenth',                      'liter' )                               : mpmathify( '0.378' ),
    ( 'tesla',                      'gauss' )                               : mpmathify( '10000' ),
    ( 'tesla',                      'kilogram/ampere-second^2' )            : mpmathify( '1' ),
    ( 'tesla',                      'volt-second/meter^2' )                 : mpmathify( '1' ),
    ( 'tesla',                      'weber/meter^2' )                       : mpmathify( '1' ),
    ( 'thousand',                   'unity' )                               : mpmathify( '100' ),
    ( 'ton',                        'pound' )                               : mpmathify( '2000' ),
    ( 'tonne',                      'gram' )                                : mpmathify( '1.0e6' ),
    ( 'ton_of_TNT',                 'joule' )                               : mpmathify( '4.184e9' ),
    ( 'torr',                       'mmHg' )                                : mpmathify( '1' ),
    ( 'township',                   'acre' )                                : mpmathify( '23040' ),
    ( 'tredecillion',               'unity' )                               : mpmathify( '1.0e42' ),
    ( 'trillion',                   'unity' )                               : mpmathify( '1.0e12' ),
    ( 'trit',                       'nat' )                                 : log( 3 ),
    ( 'troy_ounce',                 'gram' )                                : mpmathify( '31.1034768' ),
    ( 'troy_pound',                 'pound' )                               : mpmathify( '12' ),
    ( 'tryte',                      'trit' )                                : mpmathify( '6' ),   # as defined by the Setun computer
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
    ( 'unity',                      'trillionth' )                          : mpmathify( '1.0e12' ),
    ( 'vigintillion',               'unity' )                               : mpmathify( '1.0e63' ),
    ( 'virgate',                    'bovate' )                              : mpmathify( '30' ),
    ( 'volt',                       'abvolt' )                              : mpmathify( '1.0e8' ),
    ( 'volt-ampere',                'watt' )                                : mpmathify( '1' ),
    ( 'volt-coulomb',               'joule' )                               : mpmathify( '1' ),
    ( 'watt',                       'erg/second' )                          : mpmathify( '1.0e7' ),
    ( 'watt',                       'kilogram-meter^2/second^3' )           : mpmathify( '1' ),
    ( 'watt',                       'lusec' )                               : mpmathify( '7500' ),
    ( 'watt',                       'newton-meter/second' )                 : mpmathify( '1' ),
    ( 'watt-second',                'joule' )                               : mpmathify( '1' ),
    ( 'weber',                      'maxwell' )                             : mpmathify( '1.0e8' ),
    ( 'weber',                      'tesla-meter^2' )                       : mpmathify( '1' ),
    ( 'weber',                      'unit_pole' )                           : mpmathify( '7957747.154594' ),
    ( 'weber',                      'volt-second' )                         : mpmathify( '1' ),
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
}

