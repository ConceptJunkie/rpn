#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeUnits
#//
#//  RPN command-line calculator unit conversion data generator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
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
from rpnUnits import *
from rpnVersion import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_DESCRIPTION = 'RPN command-line calculator unit conversion data generator'


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

def expandMetricUnits( ):
    # expand metric measurements for all prefixes
    metricConversions = { }
    metricAliases = { }
    metricCompoundUnits = { }

    for metricUnit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], metricUnit[ 0 ] )
            newPlural = makeMetricUnit( prefix[ 0 ], metricUnit[ 1 ] )

            if newName not in unitOperators:
                # constuct unit operator info
                unitOperators[ newName ] = \
                    UnitInfo( unitOperators[ metricUnit[ 0 ] ].unitType, newName, newPlural,
                                             prefix[ 1 ] + metricUnit[ 2 ], [ ], [ 'SI' ] )

                newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
                unitConversionMatrix[ ( newName, metricUnit[ 0 ] ) ] = newConversion
                newConversion = fdiv( 1, newConversion )
                unitConversionMatrix[ ( metricUnit[ 0 ], newName ) ] = newConversion
            else:
                newConversion = power( 10, fneg( mpmathify( prefix[ 2 ] ) ) )

            # create area and volume operators for new length units
            if unitOperators[ metricUnit[ 0 ] ].unitType == 'length':
                # create new area operators
                newUnit = 'square_' + newName

                areaConversion = power( newConversion, 2 )
                oldUnit = 'square_' + metricUnit[ 0 ]

                if newUnit not in unitOperators:
                    newUnitInfo, newUnitAliases = makeAreaOperator( newName, newPlural )
                    metricAliases.update( newUnitAliases )

                    unitOperators[ newUnit ] = newUnitInfo

                    compoundUnit = newName + '^2'
                    metricCompoundUnits[ newUnit ] = compoundUnit

                    # add new conversions
                    metricConversions[ ( oldUnit, newUnit ) ] = areaConversion
                    metricConversions[ ( newUnit, oldUnit ) ] = fdiv( 1, areaConversion )

                # create new volume operators
                newUnit = 'cubic_' + newName

                volumeConversion = power( newConversion, 3 )
                oldUnit = 'cubic_' + metricUnit[ 0 ]

                if newUnit not in unitOperators:
                    newUnitInfo, newUnitAliases = makeVolumeOperator( newName, newPlural )
                    metricAliases.update( newUnitAliases )

                    unitOperators[ newUnit ] = newUnitInfo

                    compoundUnit = newName + '^3'
                    metricCompoundUnits[ newUnit ] = compoundUnit

                    # add new conversions
                    metricConversions[ ( oldUnit, newUnit ) ] = volumeConversion
                    metricConversions[ ( newUnit, oldUnit ) ] = fdiv( 1, volumeConversion )

    return metricConversions, metricAliases, metricCompoundUnits


#//******************************************************************************
#//
#//  expandDataUnits
#//
#//  Every data unit needs to be permuted for all positive SI power types and
#//  the binary power types.  We need to create conversions for each new type,
#//  as well as aliases.
#//
#//******************************************************************************

def expandDataUnits( ):
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

            # create new conversions
            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            newConversions[ ( newName, dataUnit[ 0 ] ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            newConversions[ ( dataUnit[ 0 ], newName ) ] = newConversion

        for prefix in binaryPrefixes:
            newName = prefix[ 0 ] + dataUnit[ 0 ]
            newPlural = prefix[ 0 ] + dataUnit[ 1 ]

            # constuct unit operator info
            unitOperators[ newName ] = \
                UnitInfo( unitOperators[ dataUnit[ 0 ] ].unitType, newName, newPlural, prefix[ 1 ] + dataUnit[ 2 ],
                                         [ ], unitOperators[ dataUnit[ 0 ] ].categories )

            # create new conversions
            newConversion = power( 2, mpmathify( prefix[ 2 ] ) )
            newConversions[ ( newName, dataUnit[ 0 ] ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            newConversions[ ( dataUnit[ 0 ], newName ) ] = newConversion

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
        conversion = fdiv( 1, unitConversionMatrix[ ( op1, op2 ) ] )
        newConversions[ ( op2, op1 ) ] = conversion

    unitConversionMatrix.update( newConversions )

    # create map for compound units based on the conversion matrix
    print( 'Mapping compound units...' )

    compoundUnits = { }

    for unit in unitOperators:
        chars = set( '*/^' )

        compoundUnit = unitOperators[ unit ].representation

        if any( ( c in chars ) for c in compoundUnit ):
            compoundUnits[ unit ] = compoundUnit
            #print( '    compound unit: ', unit1, '(', unit2, ')' )

    for unit1, unit2 in unitConversionMatrix:
        chars = set( '*/^' )

        if any( ( c in chars ) for c in unit2 ):
            compoundUnits[ unit1 ] = unit2
            #print( '    compound unit: ', unit1, '(', unit2, ')' )

    # create area and volume units from all of the length units
    print( 'Creating area and volume units for all length units...' )

    newOperators = { }
    newAliases = { }

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]

        if unitInfo.representation != unit:
            newAliases[ unitInfo.representation ] = unit

        if unitInfo.unitType == 'length':
            newUnit = 'square_' + unit

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = makeAreaOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnit = unit + '^2'
                compoundUnits[ newUnit ] = compoundUnit

                newAliases[ compoundUnit ] = newUnit

            newUnit = 'cubic_' + unit

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = makeVolumeOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnit = unit + '^3'
                compoundUnits[ newUnit ] = compoundUnit

                newAliases[ compoundUnit ] = newUnit

    unitOperators.update( newOperators )
    unitConversionMatrix.update( newConversions )

    # add new conversions for the new area and volume units
    print( 'Adding new conversions for the new area and volume units...' )

    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if op1 == 'light':            # special exception because it's called 'light-second',not 'speed_of_light-second'
            op1 = 'speed_of_light'

        if op2 == 'light':
            op2 = 'speed_of_light'

        if unitOperators[ op1 ].unitType == 'length':
            conversion = unitConversionMatrix[ ( op1, op2 ) ]
            newConversions[ ( 'square_' + op1, 'square_' + op2 ) ] = power( conversion, 2 )
            newConversions[ ( 'cubic_' + op1, 'cubic_' + op2 ) ] = power( conversion, 3 )

    unitConversionMatrix.update( newConversions )

    print( 'Expanding metric units against the list of SI prefixes...' )

    metricConversions, metricAliases, metricCompoundUnits = expandMetricUnits( )

    unitConversionMatrix.update( metricConversions )
    newAliases.update( metricAliases )
    compoundUnits.update( metricCompoundUnits )

    print( 'Expanding data units against the list of SI and binary prefixes...' )
    unitConversionMatrix.update( expandDataUnits( ) )

    # add new operators for compound time units
    print( 'Expanding compound time units...' )

    newUnitOperators = { }

    for unit in unitOperators:
        if unit[ -7 : ] == '-second' and unit[ : 7 ] != 'square_' and unit[ : 6 ] != 'cubic_' and \
           not any( ( c in [ '*^/' ] ) for c in unit ):
            unitRoot = unit[ : -7 ]
            unitInfo = unitOperators[ unit ]

            if unitRoot == 'light':           # special exception (see above)
                unitRoot = 'speed_of_light'

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
                unitConversionMatrix[ ( newUnit, unit ) ] = conversion
                unitConversionMatrix[ ( unit, newUnit ) ] = fdiv( 1, conversion )

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
                unitConversionMatrix[ ( newUnit, unit ) ] = fdiv( 1, conversion )
                unitConversionMatrix[ ( unit, newUnit ) ] = conversion

    unitOperators.update( newUnitOperators )

    # extrapolate transitive conversions
    print( )
    print( 'Extrapolating transitive conversions for', len( unitOperators ), 'units...' )

    unitTypeTable = makeUnitTypeTable( unitOperators )

    for unitType in sorted( basicUnitTypes ):
        print( '    ', unitType, '({} units)'.format( len( unitTypeTable[ unitType ] ) ) )

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

                        conversion = unitConversionMatrix[ ( op1, op2 ) ]

                        if ( op1, op3 ) not in unitConversionMatrix and ( op2, op3 ) in unitConversionMatrix:
                            #print( 'transitive: ', ( op2, op3 ), unitConversionMatrix[ ( op2, op3 ) ] )
                            newConversion = fmul( conversion, unitConversionMatrix[ ( op2, op3 ) ] )
                            #print( ( op1, op3 ), newConversion )
                            unitConversionMatrix[ ( op1, op3 ) ] = newConversion
                            #print( ( op3, op1 ), fdiv( 1, newConversion ) )
                            unitConversionMatrix[ ( op3, op1 ) ] = fdiv( 1, newConversion )

                            newConversion = True
                        elif ( op2, op3 ) not in unitConversionMatrix and ( op1, op3 ) in unitConversionMatrix:
                            #print( 'transitive: ', ( op1, op3 ), unitConversionMatrix[ ( op1, op3 ) ] )
                            newConversion = fdiv( unitConversionMatrix[ ( op1, op3 ) ], conversion )
                            #print( ( op2, op3 ), newConversion )
                            unitConversionMatrix[ ( op2, op3 ) ] = newConversion
                            #print( ( op3, op2 ), fdiv( 1, newConversion ) )
                            unitConversionMatrix[ ( op3, op2 ) ] = fdiv( 1, newConversion )

                            newConversion = True

                print( len( unitConversionMatrix ), end='\r' )

            if not newConversion:
                break

    # make some more aliases
    print( '        ' )
    print( 'Making some more aliases...' )

    newAliases.update( makeAliases( ) )

    print( 'Stringifying conversion matrix values...' )
    for op1, op2 in unitConversionMatrix:
        unitConversionMatrix[ ( op1, op2 ) ] = str( unitConversionMatrix[ ( op1, op2 ) ] )

    print( 'Saving everything...' )

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
    fileName = dataPath + os.sep + 'units.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicUnitTypes, pickleFile )
        pickle.dump( unitOperators, pickleFile )
        pickle.dump( newAliases, pickleFile )
        pickle.dump( compoundUnits, pickleFile )

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

