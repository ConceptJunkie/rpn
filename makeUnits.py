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
#//  measurement units
#//
#//******************************************************************************

unitTypes = [
    'area',
    'length',
    'mass',
    'time',
    'volume',
]

unitOperators = {
    'are'               : 'area',
    'acre'              : 'area',
    'barn'              : 'area',
    'shed'              : 'area',
    'square_meter'      : 'area',
    'square_yard'       : 'area',

    'foot'              : 'length',
    'inch'              : 'length',
    'meter'             : 'length',
    'micron'            : 'length',
    'mile'              : 'length',
    'yard'              : 'length',
    'rod'               : 'length',
    'astronomical_unit' : 'length',
    'furlong'           : 'length',
    'chain'             : 'length',
    'league'            : 'length',
    'light_second'      : 'length',
    'light_minute'      : 'length',
    'light_hour'        : 'length',
    'light_day'         : 'length',
    'light_year'        : 'length',
    'nautical_mile'     : 'length',
    'angstrom'          : 'length',

    'grain'             : 'mass',
    'gram'              : 'mass',
    'ounce'             : 'mass',
    'pennyweight'       : 'mass',
    'pound'             : 'mass',
    'stone'             : 'mass',
    'ton'               : 'mass',
    'tonne'             : 'mass',
    'troy_ounce'        : 'mass',
    'troy_pound'        : 'mass',

    'day'               : 'time',
    'fortnight'         : 'time',
    'hour'              : 'time',
    'minute'            : 'time',
    'second'            : 'time',
    'week'              : 'time',

    'cubic_foot'        : 'volume',
    'cup'               : 'volume',
    'fifth'             : 'volume',
    'firkin'            : 'volume',
    'fluid_ounce'       : 'volume',
    'gallon'            : 'volume',
    'gill'              : 'volume',
    'liter'             : 'volume',
    'pinch'             : 'volume',
    'pint'              : 'volume',
    'quart'             : 'volume',
    'tablespoon'        : 'volume',
    'teaspoon'          : 'volume',
}


metricUnits = [
    ( 'meter',  'm', [ 'metre' ] ),
    ( 'second', 's', [ ] ),
    ( 'liter',  'l', [ 'litre' ] ),
    ( 'gram',   'g', [ 'gramme' ] ),
    ( 'are',    'a', [ ] ),
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
    ( 'cubic_foot',        'liter' )            : '28.316846592',
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
        newAliases[ metricUnit[ 1 ] ] = metricUnit[ 0 ]

        for prefix in metricPrefixes:
            unit = makeMetricUnit( prefix[ 0 ], metricUnit[ 0 ] )
            newAliases[ prefix[ 1 ] + metricUnit[ 1 ] ] = unit

            for alternateUnit in metricUnit[ 2 ]:
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

    #for i in newAliases:
    #    print( i, newAliases[ i ] )

    return newAliases


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

    for operator in unitOperators:
        if unitOperators[ operator ] == 'length':
            newOp = 'square_' + operator

            if newOp not in unitOperators:
                newOperators[ newOp ] = 'area'

            newOp = 'cubic_'+ operator

            if newOp not in unitOperators:
                newOperators[ newOp ] = 'volume'

    unitOperators.update( newOperators )

    # add new conversions for the new area and volume units
    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if unitOperators[ op1 ] == 'length':
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
                    for op3 in unitOperators:
                        if ( op3 == op1 ) or ( op3 == op2 ):
                            continue

                        if ( op1, op3 ) not in unitConversionMatrix and ( op2, op3 ) in unitConversionMatrix:
                            conversion = fmul( mpmathify( unitConversionMatrix[ ( op1, op2 ) ] ),
                                               mpmathify( unitConversionMatrix[ ( op2, op3 ) ] ) )
                            unitConversionMatrix[ ( op1, op3 ) ] = str( conversion )
                            unitConversionMatrix[ ( op3, op1 ) ] = str( fdiv( 1, conversion ) )

                            newConversion = True
                        elif ( op2, op3 ) not in unitConversionMatrix and ( op1, op3 ) in unitConversionMatrix:
                            conversion = fdiv( mpmathify( unitConversionMatrix[ ( op1, op2 ) ] ),
                                               mpmathify( unitConversionMatrix[ ( op1, op3 ) ] ) )
                            unitConversionMatrix[ ( op2, op3 ) ] = str( conversion )
                            unitConversionMatrix[ ( op3, op2 ) ] = str( fdiv( 1, conversion ) )

                            newConversion = True

        if not newConversion:
            break

    # expand metric measurements for all prefixes
    newConversions = { }

    for unit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], unit[ 0 ] )
            unitOperators[ newName ] = unitOperators[ unit[ 0 ] ]
            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            unitConversionMatrix[ ( newName, unit[ 0 ] ) ] = str( newConversion )

            for op1, op2 in unitConversionMatrix:
                if ( op1 == unit[ 0 ] ) or ( op2 == unit[ 0 ] ):
                    oldConversion = mpmathify( unitConversionMatrix[ ( op1, op2 ) ] )

                    if op1 == unit[ 0 ] and newName != op2:
                        newConversions[ ( newName, op2 ) ] = str( fmul( newConversion, oldConversion  ) )
                    elif op2 == unit[ 0 ] and newName != op1:
                        newConversions[ ( op1, newName ) ] = str( fdiv( oldConversion, newConversion  ) )

    unitConversionMatrix.update( newConversions )

    newAliases = makeAliases( )

    #for op1, op2 in unitConversionMatrix:
    #    print( op1, op2, unitConversionMatrix[ ( op1, op2 ) ] )

    print( '{:,} unit conversions'.format( len( unitConversionMatrix ) ) )

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )

    with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'units.pckl.bz2', 'wb' ) ) as pickleFile:
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
    initializeConversionMatrix( unitConversionMatrix )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

