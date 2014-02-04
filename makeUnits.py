#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator
#//  copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import argparse
import contextlib
import bz2
import pickle
import os

from mpmath import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_VERSION = '5.4.2'
PROGRAM_DESCRIPTION = 'RPN command-line calculator unit conversion data generator'
COPYRIGHT_MESSAGE = 'copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)'


#//******************************************************************************
#//
#//  measurement units
#//
#//******************************************************************************

unitTypes = [
    'length',
    'mass',
    'time',
]

unitOperators = {
    'acre'              : [ { 'length' : 2 }, 'acres', [ ] ],
    'are'               : [ { 'length' : 2 }, 'ares', [ ] ],
    'area'              : [ { 'length' : 2 }, 'area', [ ] ],
    'barn'              : [ { 'length' : 2 }, 'barns', [ ] ],
    'shed'              : [ { 'length' : 2 }, 'sheds', [ ] ],
    'square_meter'      : [ { 'length' : 2 }, 'square meters', [ 'sqm', 'm^2', 'meter^2', 'meters^2' ] ],
    'square_yard'       : [ { 'length' : 2 }, 'square yards', [ 'sqyd', 'yd^2', 'yard^2', 'yards^2' ] ],

    'angstrom'          : [ { 'length' : 1 }, 'angstroms', [ ] ],
    'astronomical_unit' : [ { 'length' : 1 }, 'astronomical units', [ 'au' ] ],
    'chain'             : [ { 'length' : 1 }, 'chain', [ ] ],
    'foot'              : [ { 'length' : 1 }, 'feet', [ 'ft' ] ],
    'furlong'           : [ { 'length' : 1 }, 'furlongs', [ ] ],
    'inch'              : [ { 'length' : 1 }, 'inches', [ ] ],
    'league'            : [ { 'length' : 1 }, 'leagues', [ ] ],
    'length'            : [ { 'length' : 1 }, 'length', [ ] ],
    'light_day'         : [ { 'length' : 1 }, 'light days', [ ] ],
    'light_hour'        : [ { 'length' : 1 }, 'light hours', [ ] ],
    'light_minute'      : [ { 'length' : 1 }, 'light minutes', [ ] ],
    'light_second'      : [ { 'length' : 1 }, 'light seconds', [ ] ],
    'light_year'        : [ { 'length' : 1 }, 'light years', [ ] ],
    'meter'             : [ { 'length' : 1 }, 'meters', [ 'm' ] ],
    'micron'            : [ { 'length' : 1 }, 'microns', [ ] ],
    'mile'              : [ { 'length' : 1 }, 'miles', [ 'mi' ] ],
    'nautical_mile'     : [ { 'length' : 1 }, 'nautical miles', [ ] ],
    'rod'               : [ { 'length' : 1 }, 'rods', [ ] ],
    'yard'              : [ { 'length' : 1 }, 'yards', [ 'yd' ] ],

    'grain'             : [ { 'mass' : 1 },   'grains', [ ] ],
    'gram'              : [ { 'mass' : 1 },   'grams', [ 'g' ] ],
    'mass'              : [ { 'mass' : 1 },   'mass', [ ] ],
    'ounce'             : [ { 'mass' : 1 },   'ounces', [ 'oz' ] ],
    'pennyweight'       : [ { 'mass' : 1 },   'pennyweights', [ ] ],
    'pound'             : [ { 'mass' : 1 },   'pounds', [ 'lb' ] ],
    'stone'             : [ { 'mass' : 1 },   'stone', [ ] ],
    'ton'               : [ { 'mass' : 1 },   'ton', [ ] ],
    'tonne'             : [ { 'mass' : 1 },   'tonnes', [ ] ],
    'troy_ounce'        : [ { 'mass' : 1 },   'troy ounces', [ ] ],
    'troy_pound'        : [ { 'mass' : 1 },   'troy pounds', [ ] ],

    'day'               : [ { 'time' : 1 },   'days', [ ] ],
    'fortnight'         : [ { 'time' : 1 },   'fortnights', [ ] ],
    'hour'              : [ { 'time' : 1 },   'hours', [ 'hr' ] ],
    'minute'            : [ { 'time' : 1 },   'minutes', [ ] ],   # 'min' is already an operator
    'second'            : [ { 'time' : 1 },   'seconds', [ ] ],   # 'sec' is already an operator
    'time'              : [ { 'time' : 1 },   'time', [ ] ],
    'week'              : [ { 'time' : 1 },   'weeks', [ 'wk' ] ],

    'cubic_foot'        : [ { 'length' : 3 }, 'cubic feet', [ 'cuft', 'ft^3', 'foot^3', 'feet^3' ] ],
    'cubic_meter'       : [ { 'length' : 3 }, 'cubic meters', [ 'cum', 'm^3', 'meter^3', 'meters^3' ] ],
    'cup'               : [ { 'length' : 3 }, 'cups', [ ] ],
    'fifth'             : [ { 'length' : 3 }, 'fifths', [ ] ],
    'firkin'            : [ { 'length' : 3 }, 'firkins', [ ] ],
    'fluid_ounce'       : [ { 'length' : 3 }, 'fluid ounces', [ 'floz' ] ],
    'gallon'            : [ { 'length' : 3 }, 'gallons', [ 'gal' ] ],
    'gill'              : [ { 'length' : 3 }, 'gills', [ ] ],
    'liter'             : [ { 'length' : 3 }, 'liters', [ 'l' ] ],
    'pinch'             : [ { 'length' : 3 }, 'pinches', [ ] ],
    'pint'              : [ { 'length' : 3 }, 'pints', [ 'pt' ] ],
    'quart'             : [ { 'length' : 3 }, 'quarts', [ 'qt' ] ],
    'tablespoon'        : [ { 'length' : 3 }, 'tablespoons', [ 'tsp' ] ],
    'teaspoon'          : [ { 'length' : 3 }, 'teaspoons', [ 'tbsp' ] ],
    'volume'            : [ { 'length' : 3 }, 'volume', [ ] ],
}


metricUnits = [
    ( 'meter',  'meters',  'm', [ 'metre' ], [ 'metres' ] ),
    ( 'second', 'seconds', 's', [ ], [ ] ),
    ( 'liter',  'liters',  'l', [ 'litre' ], [ 'litres' ] ),
    ( 'gram',   'grams',   'g', [ 'gramme' ], [ 'grammes' ] ),
    ( 'are',    'ares',    'a', [ ], [ ] ),
]


metricPrefixes = [
    ( 'yotta',  'Y',  '24' ),
    ( 'zetta',  'Z',  '21' ),
    ( 'exa',    'E',  '18' ),
    ( 'peta',   'P',  '15' ),
    ( 'tera',   'T',  '12' ),
    ( 'giga',   'G',  '9' ),
    ( 'mega',   'M',  '6' ),
    ( 'kilo',   'k',  '3' ),
    ( 'hecto',  'h',  '2' ),
    ( 'deca',   'da', '1' ),
    ( 'deci',   'd',  '-1' ),
    ( 'centi',  'c',  '-2' ),
    ( 'milli',  'm',  '-3' ),
    ( 'micro',  'mc', '-6' ),
    ( 'nano',   'n',  '-9' ),
    ( 'pico',   'p',  '-12' ),
    ( 'femto',  'f',  '-15' ),
    ( 'atto',   'a',  '-18' ),
    ( 'zepto',  'z',  '-21' ),
    ( 'yocto',  'y',  '-24' ),
]


unitConversionMatrix = {
    ( 'acre',              'square_yard' )      : '4840',
    ( 'meter',             'angstrom' )         : '10000000000',
    ( 'are',               'square_meter' )     : '100',
    ( 'astronomical_unit', 'meter' )            : '149597870700',
    ( 'chain',             'yard' )             : '22',
    ( 'cup',               'fluid_ounce' )      : '8',
    ( 'cup',               'gill' )             : '2',
    ( 'day',               'hour' )             : '24',
    ( 'firkin',            'gallon' )           : '9',
    ( 'fluid_ounce',       'tablespoon' )       : '2',
    ( 'foot',              'inch' )             : '12',
    ( 'furlong',           'yard' )             : '220',
    ( 'gallon',            'fifth' )            : '5',
    ( 'gallon',            'quart' )            : '4',
    ( 'hour',              'minute' )           : '60',
    ( 'inch',              'meter' )            : '0.0254',
    ( 'league',            'mile' )             : '3',
    ( 'light_day',         'light_hour' )       : '24',
    ( 'light_hour',        'light_minute' )     : '60',
    ( 'light_minute',      'light_second' )     : '60',
    ( 'light_second',      'meter' )            : '299792458',
    ( 'light_year',        'light_day' )        : '365.25',
    ( 'cubic_meter',       'liter' )            : '1000',
    ( 'meter',             'micron' )           : '1000000',
    ( 'mile',              'foot' )             : '5280',
    ( 'minute',            'second' )           : '60',
    ( 'nautical_mile',     'meter' )            : '1852',
    ( 'ounce',             'gram' )             : '28.349523125',
    ( 'pound',             'grain' )            : '7000',
    ( 'pound',             'ounce' )            : '16',
    ( 'quart',             'cup' )              : '4',
    ( 'quart',             'liter' )            : '0.946352946',
    ( 'quart',             'pint' )             : '2',
    ( 'rod',               'foot' )             : '16.5',
    ( 'square_meter',      'barn' )             : '1.0e28',
    ( 'square_meter',      'shed' )             : '1.0e52',
    ( 'stone',             'pound' )            : '14',
    ( 'tablespoon',        'teaspoon' )         : '3',
    ( 'teaspoon',          'pinch' )            : '8',
    ( 'ton',               'pound' )            : '2000',
    ( 'tonne',             'gram' )             : '1000000',
    ( 'troy_ounce',        'gram' )             : '31.1034768',
    ( 'troy_pound',        'pound' )            : '12',
    ( 'yard',              'foot' )             : '3',
    ( 'fortnight',         'day' )              : '14',
    ( 'week',              'day' )              : '7',
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
        newAliases[ unitOperators[ unit ][ 1 ] ] = unit

        #print( unit )
        for abbrev in unitOperators[ unit ][ 2 ]:
            newAliases[ abbrev ] = unit

    #for i in newAliases:
    #    print( i, newAliases[ i ] )
    return newAliases


#//******************************************************************************
#//
#//  expandMetricUnits
#//
#//  Every metric unit needs to be permuted for all SI power types.  We need to
#//  create conversions for each new type, as well as aliases.
#..
#//******************************************************************************

def expandMetricUnits( ):
    # expand metric measurements for all prefixes
    newConversions = { }

    for unit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], unit[ 0 ] )
            newPlural = makeMetricUnit( prefix[ 0 ], unit[ 1 ] )

            # constuct unit operator info (3 parts: unit type, plural name and alias list)
            unitOperators[ newName ] = [ unitOperators[ unit[ 0 ] ][ 0 ], newPlural, [ prefix[ 1 ] + unit[ 2 ] ] ]

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, unit[ 0 ] ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == unit[ 0 ] ) or ( op2 == unit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == unit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fmul( newConversion, oldConversion  ) )
                    elif op2 == unit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fdiv( oldConversion, newConversion  ) )

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

    # create area and volume units from all of the length units
    newOperators = { }
    newAliases = { }

    for operator in unitOperators:
        unitInfo = unitOperators[ operator ]

        if unitInfo[ 0 ] == { 'length' : 1 }:
            newOp = 'square_' + operator

            if newOp not in unitOperators:
                abbrevs = [ ]

                for abbrev in unitInfo[ 2 ]:
                    abbrevs.append( 'sq' + abbrev )
                    abbrevs.append( abbrev + '^2' )

                newOperators[ newOp ] = [ { 'length' : 2 }, 'square_' + unitInfo[ 1 ], abbrevs ]

                newAliases[ 'square_' + unitInfo[ 1 ] ] = newOp
                newAliases[ operator +  '^2' ] = newOp
                newAliases[ unitInfo[ 1 ] + '^2' ] = newOp

            newOp = 'cubic_'+ operator

            if newOp not in unitOperators:
                newOperators[ newOp ] = [ { 'length' : 3 }, 'cubic_' + unitInfo[ 1 ], [ ] ]
                newAliases[ 'cubic_' + unitInfo[ 1 ] ] = newOp

                for abbrev in unitInfo[ 2 ]:
                    abbrevs.append( 'cu' + abbrev )
                    abbrevs.append( abbrev + '^3' )

                newAliases[ 'square_' + unitInfo[ 1 ] ] = newOp
                newAliases[ operator +  '^3' ] = newOp
                newAliases[ unitInfo[ 1 ] + '^3' ] = newOp

    unitOperators.update( newOperators )

    # add new conversions for the new area and volume units
    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if unitOperators[ op1 ][ 0 ] == { 'length' : 1 }:
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

                        #if newConversion:
                        #    break

        if not newConversion:
            break

    unitConversionMatrix.update( expandMetricUnits( ) )

    newAliases.update( makeAliases( ) )

    #for op1, op2 in unitConversionMatrix:
    #    print( op1, op2, unitConversionMatrix[ ( op1, op2 ) ] )

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


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    print( PROGRAM_NAME, PROGRAM_VERSION )
    print( PROGRAM_DESCRIPTION )
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

