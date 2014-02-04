#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeUnits
#//
#//  RPN command-line calculator unit conversion data generator
#//  copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import bz2
import contextlib
import os
import pickle
import string

from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_VERSION = '5.7.1'
PROGRAM_DESCRIPTION = 'RPN command-line calculator unit conversion data generator'
COPYRIGHT_MESSAGE = 'copyright (c) 2013, Rick Gutleber (rickg@his.com)'


#//******************************************************************************
#//
#//  unitTypes
#//
#//  unit type : conversion from the basic unit types (length, mass, time)
#//
#//******************************************************************************

unitTypes = {
    'acceleration'  : 'length/time^2',
    'area'          : 'length^2',
    'energy'        : 'mass*length^2/time^2',
    'force'         : 'mass*length/time',
    'length'        : 'length',
    'mass'          : 'mass',
    'power'         : 'mass*length^2/time',
    'pressure'      : 'mass/length*time^2',
    'time'          : 'time',
    'velocity'      : 'length/time',
    'volume'        : 'length^3',
}


#//******************************************************************************
#//
#//  class UnitInfo
#//
#//******************************************************************************

class UnitInfo( ):
    def __init__( self, unitType, representation, plural, abbrev, aliases ):
        self.unitType = unitType
        self.representation = representation
        self.plural = plural
        self.abbrev = abbrev
        self.aliases = aliases


#//******************************************************************************
#//
#//  unitOperators
#//
#//  unit name : unitType, representation, plural, abbrev, aliases
#//
#//******************************************************************************

unitOperators = {
    # acceleration

    'meter/second^2' :
        UnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', 'm/s', [ ] ),

    'standard_gravity' :
        UnitInfo( 'acceleration', 'standard_gravity', 'standard_gravities', 'G', [ ] ),

    # area

    'acre' :
        UnitInfo( 'area', 'acre', 'acres', 'ac', [ ] ),

    'are' :
        UnitInfo( 'area', 'are', 'ares', 'a', [ ] ),

    'barn' :
        UnitInfo( 'area', 'barn', 'barns', '', [ ] ),

    'shed' :
        UnitInfo( 'area', 'shed', 'sheds', '', [ ] ),

    'square_meter' :
        UnitInfo( 'area', 'meter^2', 'square_meters', 'm^2', [ 'meter^2', 'meters^2' ] ),

    'square_yard' :
        UnitInfo( 'area', 'yard^2', 'square_yards', 'sqyd', [ 'sqyd', 'yd^2', 'yard^2', 'yards^2' ] ),

    # energy

    'BTU' :
        UnitInfo( 'energy', 'BTU', 'BTUs', 'BTU', [ 'btu' ] ),

    'calorie' :
        UnitInfo( 'energy', 'calorie', 'calories', 'cal', [ ] ),

    'electron-volt' :
        UnitInfo( 'energy', 'electron-volt', 'electron-volts', 'eV', [ ] ),

    'erg' :
        UnitInfo( 'energy', 'erg', 'ergs', '', [ ] ),

    'horsepower-second' :
        UnitInfo( 'energy', 'horsepower*second', 'horsepower-seconds', 'hps', [ ] ),

    'joule' :
        UnitInfo( 'energy', 'joule', 'joules', 'J', [ ] ),

    'kilogram*meter^2/second^2' :
        UnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', 'kg*m^2/s^2', [ ] ),

    'ton_of_TNT' :
        UnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT', [ ] ),

    'watt-second' :
        UnitInfo( 'energy', 'watt*second', 'watt-seconds', 'Ws', [ ] ),

    # length

    'angstrom' :
        UnitInfo( 'length', 'angstrom', 'angstroms', 'A', [ ] ),

    'astronomical_unit' :
        UnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au', [ ] ),

    'chain' :
        UnitInfo( 'length', 'chain', 'chains', '', [ ] ),

    'foot' :
        UnitInfo( 'length', 'foot', 'feet', 'ft', [ ] ),

    'furlong' :
        UnitInfo( 'length', 'furlong', 'furlongs', '', [ ] ),

    'inch' :
        UnitInfo( 'length', 'inch', 'inches', 'in', [ ] ),

    'league' :
        UnitInfo( 'length', 'league', 'leagues', '', [ ] ),

    'meter' :
        UnitInfo( 'length', 'meter', 'meters', 'm', [ ] ),

    'micron' :
        UnitInfo( 'length', 'micron', 'microns', '', [ ] ),

    'mile' :
        UnitInfo( 'length', 'mile', 'miles', 'mi', [ ] ),

    'nautical_mile' :
        UnitInfo( 'length', 'nautical_mile', 'nautical_miles', '', [ ] ),

    'rod' :
        UnitInfo( 'length', 'rod', 'rods', '', [ ] ),

    'speed_of_light-second' :
        UnitInfo( 'length', 'speed_of_light*second', 'light-seconds', '', [ ] ),

    'yard' :
        UnitInfo( 'length', 'yard', 'yards', 'yd', [ '' ] ),

    # mass

    'carat' :
        UnitInfo( 'mass', 'carat', 'carats', 'kt', [ ] ),

    'grain' :
        UnitInfo( 'mass', 'grain', 'grains', 'gr', [ ] ),

    'gram' :
        UnitInfo( 'mass', 'gram', 'grams', 'g', [ ] ),

    'mass' :
        UnitInfo( 'mass', 'mass', 'mass', '', [ ] ),

    'ounce' :
        UnitInfo( 'mass', 'ounce', 'ounces', 'oz', [ ] ),

    'pennyweight' :
        UnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt', [ ] ),

    'pound' :
        UnitInfo( 'mass', 'pound', 'pounds', 'lb', [ ] ),

    'stone' :
        UnitInfo( 'mass', 'stone', 'stone', '', [ ] ),

    'ton' :
        UnitInfo( 'mass', 'ton', 'tons', '', [ ] ),

    'tonne' :
        UnitInfo( 'mass', 'tonne', 'tonnes', '', [ ] ),

    'troy_ounce' :
        UnitInfo( 'mass', 'troy_ounce', 'troy_ounces', '', [ ] ),

    'troy_pound' :
        UnitInfo( 'mass', 'troy_pound', 'troy_pounds', '', [ ] ),

    # power

    'horsepower' :
        UnitInfo( 'power', 'horsepower', 'horsepower', 'hp', [ ] ),

    'joule/second' :
        UnitInfo( 'power', 'joule/second', 'joules/second', 'J/s', [ ] ),

    'watt' :
        UnitInfo( 'power', 'watt', 'watts', 'W', [ ] ),

    # pressure

    'atmosphere' :
        UnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm', [ ] ),

    'bar' :
        UnitInfo( 'pressure', 'bar', 'bar', '', [ ] ),

    'mmHg' :
        UnitInfo( 'pressure', 'mmHg', 'mmHg', '', [ ] ),

    'pascal' :
        UnitInfo( 'pressure', 'pascal', 'pascal', 'Pa', [ ] ),

    'psi' :
        UnitInfo( 'pressure', 'psi', 'pounds/inch^2', 'psi', [ 'lb/in^2' ] ),

    'torr' :
        UnitInfo( 'pressure', 'torr', 'torr', '', [ ] ),

    # time

    'day' :
        UnitInfo( 'time', 'day', 'days', '', [ ] ),

    'fortnight' :
        UnitInfo( 'time', 'fortnight', 'fortnights', '', [ ] ),

    'hour' :
        UnitInfo( 'time', 'hour', 'hours', 'hr', [ ] ),

    'minute' :
        UnitInfo( 'time', 'minute', 'minutes', '', [ ] ),   # 'min' is already an operator

    'second' :
        UnitInfo( 'time', 'second', 'seconds', '', [ ] ),   # 'sec' is already an operator

    'week' :
        UnitInfo( 'time', 'week', 'weeks', 'wk', [ ] ),

    # velocity

    'meter/second' :
        UnitInfo( 'velocity', 'meter/second', 'meters per second', 'c', [ 'light' ] ),

    'speed_of_light' :
        UnitInfo( 'velocity', 'speed_of_light', 'x_speed_of_light', 'c', [ 'light' ] ),

    # volume

    'cubic_foot' :
        UnitInfo( 'volume', 'foot^3', 'cubic_feet', 'cuft', [ 'ft^3', 'foot^3', 'feet^3' ] ),

    'cubic_meter' :
        UnitInfo( 'volume', 'meter^3', 'cubic_meters', 'm^3', [ 'meter^3', 'meters^3' ] ),

    'cup' :
        UnitInfo( 'volume', 'cup', 'cups', '', [ ] ),

    'dram' :
        UnitInfo( 'volume', 'dram', 'dram', '', [ ] ),

    'fifth' :
        UnitInfo( 'volume', 'fifth', 'fifths', '', [ ] ),

    'firkin' :
        UnitInfo( 'volume', 'firkin', 'firkins', '', [ ] ),

    'fluid_ounce' :
        UnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', 'floz', [ ] ),

    'gallon' :
        UnitInfo( 'volume', 'gallon', 'gallons', 'gal', [ ] ),

    'gill' :
        UnitInfo( 'volume', 'gill', 'gills', '', [ ] ),

    'liter' :
        UnitInfo( 'volume', 'liter', 'liters', 'l', [ ] ),

    'pinch' :
        UnitInfo( 'volume', 'pinch', 'pinches', '', [ ] ),

    'pint' :
        UnitInfo( 'volume', 'pint', 'pints', 'pt', [ ] ),

    'quart' :
        UnitInfo( 'volume', 'quart', 'quarts', 'qt', [ ] ),

    'tablespoon' :
        UnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp', [ ] ),

    'teaspoon' :
        UnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp', [ ] ),
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
    ( 'meter',          'meters',           'm',    [ 'metre' ],    [ 'metres' ] ),
    ( 'second',         'seconds',          's',    [ ],            [ ] ),
    ( 'liter',          'liters',           'l',    [ 'litre' ],    [ 'litres' ] ),
    ( 'gram',           'grams',            'g',    [ 'gramme' ],   [ 'grammes' ] ),
    ( 'are',            'ares',             'a',    [ ], [ ] ),
    ( 'joule',          'joules',           'J',    [ ], [ ] ),
    ( 'electron-volt',  'electron-volts',   'eV',   [ ], [ ] ),
    ( 'watt',           'watts',            'W',    [ ], [ ] ),
    ( 'calorie',        'calories',         'cal',  [ ], [ ] ),
    ( 'ton_of_TNT',     'tons_of_TNT',      'tTNT', [ ], [ ] ),
    ( 'watt-second',    'watt-seconds',     'Ws',   [ ], [ ] ),
    ( 'pascal'      ,   'pascal',           'Pa',   [ ], [ ] ),
]


#//******************************************************************************
#//
#//  timeUnits
#//
#//******************************************************************************

timeUnits = [
    ( 'minute',     'minutes',      'm',        '60' ),
    ( 'hour',       'hour',         'h',        '3600' ),
    ( 'day',        'day',          'd',        '86400' ),
    ( 'year',       'year',         'y',        '31557600' ),   # 365.25 days
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
    ( 'micro',      'mc',     '-6' ),
    ( 'nano',       'n',      '-9' ),
    ( 'pico',       'p',      '-12' ),
    ( 'femto',      'f',      '-15' ),
    ( 'atto',       'a',      '-18' ),
    ( 'zepto',      'z',      '-21' ),
    ( 'yocto',      'y',      '-24' ),
]


#//******************************************************************************
#//
#//  metricPrefixes
#//
#//  ( first unit, second unit, conversion factor )
#//
#//******************************************************************************

unitConversionMatrix = {
    ( 'acre',                  'square_yard' )                     : '4840',
    ( 'are',                   'square_meter' )                    : '100',
    ( 'astronomical_unit',     'meter' )                           : '149597870700',
    ( 'atmosphere',            'pascal' )                          : '101325',
    ( 'bar',                   'pascal' )                          : '100000',
    ( 'BTU',                   'joule' )                           : '1054.5',
    ( 'calorie',               'joule' )                           : '4.184',
    ( 'carat',                 'grain' )                           : '3.1666666666666666666666',
    ( 'chain',                 'yard' )                            : '22',
    ( 'cubic_meter',           'liter' )                           : '1000',
    ( 'cup',                   'dram' )                            : '64',
    ( 'cup',                   'fluid_ounce' )                     : '8',
    ( 'cup',                   'gill' )                            : '2',
    ( 'day',                   'hour' )                            : '24',
    ( 'firkin',                'gallon' )                          : '9',
    ( 'fluid_ounce',           'tablespoon' )                      : '2',
    ( 'foot',                  'inch' )                            : '12',
    ( 'fortnight',             'day' )                             : '14',
    ( 'furlong',               'yard' )                            : '220',
    ( 'gallon',                'fifth' )                           : '5',
    ( 'gallon',                'quart' )                           : '4',
    ( 'horsepower',            'watt' )                            : '745.69987158227022',
    ( 'horsepower-second',     'joule' )                           : '745.69987158227022',
    ( 'hour',                  'minute' )                          : '60',
    ( 'inch',                  'meter' )                           : '0.0254',
    ( 'joule',                 'electron-volt' )                   : '6.24150974e18',
    ( 'joule',                 'erg' )                             : '10000000',
    ( 'joule',                 'kilogram*meter^2/second^2' )       : '1',
    ( 'joule/second',          'watt' )                            : '1',
    ( 'league',                'mile' )                            : '3',
    ( 'speed_of_light-second', 'meter' )                           : '299792458',
    ( 'meter',                 'angstrom' )                        : '10000000000',
    ( 'meter',                 'micron' )                          : '1000000',
    ( 'mile',                  'foot' )                            : '5280',
    ( 'minute',                'second' )                          : '60',
    ( 'mmHg',                  'pascal' )                          : '133.3224',        # approx.
    ( 'nautical_mile',         'meter' )                           : '1852',
    ( 'ounce',                 'gram' )                            : '28.349523125',
    ( 'pound',                 'grain' )                           : '7000',
    ( 'pound',                 'ounce' )                           : '16',
    ( 'psi',                   'pascal' )                          : '6894.757',        # approx.
    ( 'quart',                 'cup' )                             : '4',
    ( 'quart',                 'liter' )                           : '0.946352946',
    ( 'quart',                 'pint' )                            : '2',
    ( 'rod',                   'foot' )                            : '16.5',
    ( 'speed_of_light',        'meter/second' )                    : '299792458',
    ( 'square_meter',          'barn' )                            : '1.0e28',
    ( 'square_meter',          'shed' )                            : '1.0e52',
    ( 'standard_gravity',      'meter/second^2' )                  : '9.806650',
    ( 'stone',                 'pound' )                           : '14',
    ( 'tablespoon',            'teaspoon' )                        : '3',
    ( 'teaspoon',              'pinch' )                           : '8',
    ( 'ton',                   'pound' )                           : '2000',
    ( 'tonne',                 'gram' )                            : '1000000',
    ( 'ton_of_TNT',            'joule' )                           : '4184000000',
    ( 'torr',                  'mmHg' )                            : '1',
    ( 'troy_ounce',            'gram' )                            : '31.1034768',
    ( 'troy_pound',            'pound' )                           : '12',
    ( 'watt-second',           'joule' )                           : '1',
    ( 'week',                  'day' )                             : '7',
    ( 'yard',                  'foot' )                            : '3',
}


#//******************************************************************************
#//
#//  makeMetricUnit
#//
#//******************************************************************************

def makeMetricUnit( prefix, unit ):
    if unit[ 0 ] == 'a' and ( ( prefix[ -1 ] in 'a' ) or ( prefix[ -3 : ] == 'cto' ) ):
        return prefix[ : -1 ] + unit
    else:
        return prefix + unit


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
            newAliases[ pluralUnit ] = unit                     # add plural alias

            newAliases[ prefix[ 1 ] + metricUnit[ 2 ] ] = unit   # add SI abbreviation alias

            for alternateUnit in metricUnit[ 3 ]:                # add alternate spelling alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

            for alternateUnit in metricUnit[ 4 ]:                # add alternate spelling plural alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]
        newAliases[ unitInfo.plural ] = unit

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

def expandMetricUnits( ):
    # expand metric measurements for all prefixes
    newConversions = { }

    for unit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], unit[ 0 ] )
            newPlural = makeMetricUnit( prefix[ 0 ], unit[ 1 ] )

            # constuct unit operator info
            unitOperators[ newName ] = \
                UnitInfo( unitOperators[ unit[ 0 ] ].unitType, newName, newPlural,
                                         prefix[ 1 ] + unit[ 2 ], [ ] )

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, unit[ 0 ] ) ] = str( newConversion )
            newConversion = fdiv( 1, newConversion )
            unitConversionMatrix[ ( unit[ 0 ], newName ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == unit[ 0 ] ) or ( op2 == unit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == unit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fdiv( oldConversion, newConversion ) )
                    elif op2 == unit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fmul( oldConversion, newConversion ) )

    return newConversions


#//******************************************************************************
#//
#//  initializeConversionMatrix
#//
#//******************************************************************************

def initializeConversionMatrix( unitConversionMatrix ):
    mp.dps = 50

    # reverse each conversion
    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        conversion = fdiv( 1, mpmathify( unitConversionMatrix[ ( op1, op2 ) ] ) )
        newConversions[ ( op2, op1 ) ] = str( conversion )

    unitConversionMatrix.update( newConversions )

    # create map for compound units based on the conversion matrix
    compoundUnits = { }

    for unit1, unit2 in unitConversionMatrix:
        chars = set( '*/^' )

        if any( ( c in chars ) for c in unit2 ):
            compoundUnits[ unit1 ] = unit2

    # create area and volume units from all of the length units
    newOperators = { }
    newAliases = { }

    for operator in unitOperators:
        unitInfo = unitOperators[ operator ]

        if unitInfo.unitType == 'length':
            newOp = 'square_' + operator

            if newOp not in unitOperators:
                if unitInfo.abbrev == '':
                    abbrev = 'sq' + operator
                else:
                    abbrev = 'sq' + unitInfo.abbrev
                    newAliases[ 'sq' + unitInfo.abbrev ] = newOp

                newOperators[ newOp ] = \
                    UnitInfo( 'area', newOp, 'square_' + unitInfo.plural, abbrev, [ ] )

                newAliases[ 'square_' + unitInfo.plural ] = newOp
                newAliases[ 'sq' + unitInfo.plural ] = newOp
                newAliases[ operator +  '^2' ] = newOp
                newAliases[ unitInfo.plural + '^2' ] = newOp

            newOp = 'cubic_'+ operator

            if newOp not in unitOperators:
                if unitInfo.abbrev == '':
                    abbrev = 'cu' + operator
                else:
                    abbrev = 'cu' + unitInfo.abbrev
                    newAliases[ 'cu' + unitInfo.abbrev ] = newOp

                newOperators[ newOp ] = \
                    UnitInfo( 'volume', operator + '^3',
                              'cubic_' + unitInfo.plural, abbrev, [ ] )

                newAliases[ 'cubic_' + unitInfo.plural ] = newOp
                newAliases[ 'cu' + unitInfo.plural ] = newOp
                newAliases[ operator +  '^3' ] = newOp
                newAliases[ unitInfo.plural + '^3' ] = newOp

    unitOperators.update( newOperators )

    # add new conversions for the new area and volume units
    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if unitOperators[ op1 ].unitType == 'length':
            conversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )
            newConversions[ ( 'square_' + op1, 'square_' + op2 ) ] = str( power( conversion, 2 ) )
            newConversions[ ( 'cubic_' + op1, 'cubic_' + op2 ) ] = str( power( conversion, 3 ) )

    unitConversionMatrix.update( newConversions )

    # extrapolate transitive conversions
    while True:
        newConversion = False

        for op1 in unitOperators:
            for op2 in unitOperators:
                if ( op1, op2 ) in unitConversionMatrix:
                    #print( )
                    #print( ( op1, op2 ), ': ', unitConversionMatrix[ ( op1, op2 ) ] )

                    for op3 in unitOperators:
                        if ( op3 == op1 ) or ( op3 == op2 ):
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

        if not newConversion:
            break

    unitConversionMatrix.update( expandMetricUnits( ) )

    # add new operators for compound time units
    newUnitOperators = { }

    for unit in unitOperators:
        if unit[ -7 : ] == '-second' and unit[ : 7 ] != 'square_' and unit[ : 6 ] != 'cubic_':
            unitRoot = unit[ : -7 ]

            unitInfo = unitOperators[ unit ]

            for timeUnit in timeUnits:
                newUnit = unitRoot + '-' + timeUnit[ 0 ]
                newPlural = unitRoot + '-' + timeUnit[ 1 ]
                newAliases[ newPlural ] = newUnit
                newAliases[ unitRoot + '-' + timeUnit[ 1 ] ] = newUnit

                # We assume the abbrev ends with an s for second
                if unitInfo.abbrev != '':
                    newAbbrev = unitInfo.abbrev[ : -1 ] + timeUnit[ 2 ]
                    #print( newUnit, newAbbrev )
                    newAliases[ newAbbrev ] = newUnit

                for alias in unitInfo.aliases:
                    newAliases[ alias + '*' + timeUnit[ 1 ] ] = newUnit
                    newAliases[ alias + '-' + timeUnit[ 1 ] ] = newUnit

                newUnitOperators[ newUnit ] = \
                    UnitInfo( unitInfo.unitType, unitRoot + '*' + timeUnit[ 0 ],
                              newPlural, '', [ ] )

                conversion = mpmathify( timeUnit[ 3 ] )
                unitConversionMatrix[ ( newUnit, unit ) ] = str( conversion )
                unitConversionMatrix[ ( unit, newUnit ) ] = str( fdiv( 1, conversion ) )

    unitOperators.update( newUnitOperators )

    # add new conversions for compound time units
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
    newAliases.update( makeAliases( ) )

    #for op1, op2 in unitConversionMatrix:
    #    print( op1, op2, unitConversionMatrix[ ( op1, op2 ) ] )

    #print( )
    #print( )

    #for alias in newAliases:
    #    print( alias, newAliases[ alias ] )

    print( '{:,} unit conversions'.format( len( unitConversionMatrix ) ) )

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
    fileName = dataPath + os.sep + 'units.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( unitTypes, pickleFile )
        pickle.dump( unitOperators, pickleFile )
        pickle.dump( unitConversionMatrix, pickleFile )
        pickle.dump( newAliases, pickleFile )
        pickle.dump( compoundUnits, pickleFile )


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

