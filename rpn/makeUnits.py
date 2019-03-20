#!/usr/bin/env python

# //******************************************************************************
# //
# //  makeUnits
# //
# //  RPN command-line calculator unit conversion data generator
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

import bz2
import contextlib
import itertools
import os
import pickle

from mpmath import almosteq, mp, fdiv, fmul

#  This has to go here so the mpf's in the import get created with 50 places of precision.
mp.dps = 50

from rpn.rpnMeasurement import specialUnitConversionMatrix
from rpn.rpnUnits import *
from rpn.rpnUtils import getDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_DESCRIPTION = 'RPN command-line calculator unit conversion data generator'


# //******************************************************************************
# //
# //  makeMetricUnit
# //
# //******************************************************************************

def makeMetricUnit( prefix, unit ):
    # special case because the standard is inconsistent
    if ( unit == 'ohm' ) and ( prefix == 'giga' ):
        return 'gigaohm'   # not gigohm
    elif ( unit[ 0 ] == 'o' ) and ( prefix[ -1 ] in 'oa' ):
        return prefix[ : -1 ] + unit
    elif unit[ 0 ] == 'a' and ( ( prefix[ -1 ] == 'a' ) or ( prefix[ -3 : ] == 'cto' ) ):
        return prefix[ : -1 ] + unit
    else:
        return prefix + unit


# //******************************************************************************
# //
# //  makeUnitTypeTable
# //
# //  maps each unit type to a list of units with that type
# //
# //******************************************************************************

def makeUnitTypeTable( unitOperators ):
    unitTypeTable = { }

    for unitType in basicUnitTypes:
        unitTypeTable[ unitType ] = [ ]

    for unit in unitOperators:
        unitTypeTable[ unitOperators[ unit ].unitType ].append( unit )

    return unitTypeTable


# //******************************************************************************
# //
# //  makeAliases
# //
# //******************************************************************************

def makeAliases( ):
    newAliases = { }

    for metricUnit in metricUnits:
        for prefix in metricPrefixes:
            unit = makeMetricUnit( prefix[ 0 ], metricUnit )
            pluralUnit = makeMetricUnit( prefix[ 0 ], metricUnits[ metricUnit ][ 0 ] )

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit             # add plural alias

            for alternateUnit in metricUnits[ metricUnit ][ 2 ]:           # add alternate spelling alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

            for alternateUnit in metricUnits[ metricUnit ][ 3 ]:           # add alternate spelling plural alias
                newAliases[ makeMetricUnit( prefix[ 0 ], alternateUnit ) ] = unit

    for dataUnit in dataUnits:
        newAliases[ dataUnit[ 2 ] ] = dataUnit[ 0 ]

        for prefix in dataPrefixes:
            unit = prefix[ 0 ] + dataUnit[ 0 ]
            pluralUnit = prefix[ 0 ] + dataUnit[ 1 ]

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit                 # add plural alias

            newAliases[ prefix[ 1 ] + dataUnit[ 0 ] ] = unit    # add SI abbreviation alias
            newAliases[ prefix[ 1 ] + dataUnit[ 1 ] ] = unit    # add SI abbreviation alias
            newAliases[ prefix[ 1 ] + dataUnit[ 2 ] ] = unit    # add SI abbreviation alias

            for alternateUnit in dataUnit[ 3 ]:                 # add alternate spelling alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

            for alternateUnit in dataUnit[ 4 ]:                 # add alternate spelling plural alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

        for prefix in binaryPrefixes:
            unit = prefix[ 0 ] + dataUnit[ 0 ]
            pluralUnit = prefix[ 0 ] + dataUnit[ 1 ]

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit                 # add plural alias

            newAliases[ prefix[ 1 ] + dataUnit[ 0 ] ] = unit    # add SI abbreviation alias
            newAliases[ prefix[ 1 ] + dataUnit[ 1 ] ] = unit    # add SI abbreviation alias
            newAliases[ prefix[ 1 ] + dataUnit[ 2 ] ] = unit    # add SI abbreviation alias

            for alternateUnit in dataUnit[ 3 ]:                 # add alternate spelling alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

            for alternateUnit in dataUnit[ 4 ]:                 # add alternate spelling plural alias
                newAliases[ prefix[ 0 ] + alternateUnit ] = unit

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]

        if unitInfo.plural != unit:
            newAliases[ unitInfo.plural ] = unit

        for alias in unitInfo.aliases:
            newAliases[ alias ] = unit

        if unitInfo.abbrev != '':
            newAliases[ unitInfo.abbrev ] = unit

    for constant in constantOperators:
        constantInfo = constantOperators[ constant ]

        for alias in constantInfo.aliases:
            newAliases[ alias ] = constant

    return newAliases


# //******************************************************************************
# //
# //  expandMetricUnits
# //
# //  Every metric unit needs to be permuted for all SI power types.  We need to
# //  create conversions for each new type, as well as aliases.
# //
# //******************************************************************************

def expandMetricUnits( ):
    # expand metric measurements for all prefixes
    metricConversions = { }
    metricAliases = { }

    for metricUnit in metricUnits:
        for prefix in metricPrefixes:
            newName = makeMetricUnit( prefix[ 0 ], metricUnit )
            newPlural = makeMetricUnit( prefix[ 0 ], metricUnits[ metricUnit][ 0 ] )

            if newName not in unitOperators:
                # constuct unit operator info
                if metricUnits[ metricUnit ][ 1 ]:
                    unitOperators[ newName ] = \
                        RPNUnitInfo( unitOperators[ metricUnit ].unitType, newName, newPlural,
                                     prefix[ 1 ] + metricUnits[ metricUnit ][ 1 ], [ ], [ 'SI' ], True )
                else:
                    unitOperators[ newName ] = \
                        RPNUnitInfo( unitOperators[ metricUnit ].unitType, newName, newPlural,
                                     '', [ ], [ 'SI' ], True )


                newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
                unitConversionMatrix[ ( newName, metricUnit ) ] = newConversion
                newConversion = fdiv( 1, newConversion )
                unitConversionMatrix[ ( metricUnit, newName ) ] = newConversion
            else:
                newConversion = power( 10, fneg( mpmathify( prefix[ 2 ] ) ) )

            # create area and volume operators for new length units
            if unitOperators[ metricUnit ].unitType == 'length':
                # create new area operators
                newUnit = newName + '^2'

                areaConversion = power( newConversion, 2 )
                oldUnit = metricUnit + '^2'

                if newUnit not in unitOperators:
                    newUnitInfo, newUnitAliases = makeAreaOperator( newName, newPlural )
                    metricAliases.update( newUnitAliases )

                    unitOperators[ newUnit ] = newUnitInfo

                    # add new conversions
                    metricConversions[ ( oldUnit, newUnit ) ] = areaConversion
                    metricConversions[ ( newUnit, oldUnit ) ] = fdiv( 1, areaConversion )

                # create new volume operators
                newUnit = newName + '^3'

                volumeConversion = power( newConversion, 3 )
                oldUnit = metricUnit + '^3'

                if newUnit not in unitOperators:
                    newUnitInfo, newUnitAliases = makeVolumeOperator( newName, newPlural )
                    metricAliases.update( newUnitAliases )

                    unitOperators[ newUnit ] = newUnitInfo

                    # add new conversions
                    metricConversions[ ( oldUnit, newUnit ) ] = volumeConversion
                    metricConversions[ ( newUnit, oldUnit ) ] = fdiv( 1, volumeConversion )

    return metricConversions, metricAliases


# //******************************************************************************
# //
# //  expandDataUnits
# //
# //  Every data unit needs to be permuted for all positive SI power types and
# //  the binary power types.  We need to create conversions for each new type,
# //  as well as aliases.
# //
# //******************************************************************************

def expandDataUnits( ):
    # expand data measurements for all prefixes
    newConversions = { }

    for dataUnit in dataUnits:
        for prefix in dataPrefixes:
            newName = prefix[ 0 ] + dataUnit[ 0 ]
            newPlural = prefix[ 0 ] + dataUnit[ 1 ]

            # constuct unit operator info
            unitOperators[ newName ] = \
                RPNUnitInfo( unitOperators[ dataUnit[ 0 ] ].unitType, newName, newPlural,
                             prefix[ 1 ] + dataUnit[ 2 ], [ ],
                             unitOperators[ dataUnit[ 0 ] ].categories, True )

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
                RPNUnitInfo( unitOperators[ dataUnit[ 0 ] ].unitType, newName, newPlural,
                             prefix[ 1 ] + dataUnit[ 2 ], [ ],
                             unitOperators[ dataUnit[ 0 ] ].categories, True )

            # create new conversions
            newConversion = power( 2, mpmathify( prefix[ 2 ] ) )
            newConversions[ ( newName, dataUnit[ 0 ] ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            newConversions[ ( dataUnit[ 0 ], newName ) ] = newConversion

    return newConversions


# //******************************************************************************
# //
# //  makeAreaOperator
# //
# //******************************************************************************

def makeAreaOperator( unit, unitPlural ):
    unitInfo = unitOperators[ unit ]

    newAliases = { }

    newUnit = unit + '^2'

    if unitInfo.abbrev == '':
        abbrev = 'sq' + unit
    else:
        abbrev = 'sq' + unitInfo.abbrev
        newAliases[ 'sq' + unitInfo.abbrev ] = newUnit
        newAliases[ 'sq_' + unitInfo.abbrev ] = newUnit
        newAliases[ 'square_' + unitInfo.abbrev ] = newUnit

    newAliases[ 'square_' + unit ] = newUnit
    newAliases[ 'square_' + unitInfo.plural ] = newUnit
    newAliases[ 'sq_' + unit ] = newUnit
    newAliases[ 'sq_' + unitInfo.plural ] = newUnit
    newAliases[ 'sq' + unit ] = newUnit
    newAliases[ 'sq' + unitInfo.plural ] = newUnit

    newUnitInfo = RPNUnitInfo( 'area', newUnit, newUnit, abbrev, [ ],
                               unitInfo.categories, True )

    return newUnitInfo, newAliases


# //******************************************************************************
# //
# //  makeVolumeOperator
# //
# //******************************************************************************

def makeVolumeOperator( unit, unitPlural ):
    unitInfo = unitOperators[ unit ]

    newAliases = { }

    newUnit = unit + '^3'

    if unitInfo.abbrev == '':
        abbrev = 'cu' + unit
    else:
        abbrev = 'cu' + unitInfo.abbrev
        newAliases[ 'cu' + unitInfo.abbrev ] = newUnit
        newAliases[ 'cu_' + unitInfo.abbrev ] = newUnit
        newAliases[ 'cubic_' + unitInfo.abbrev ] = newUnit

    newAliases[ 'cubic_' + unit ] = newUnit
    newAliases[ 'cubic_' + unitInfo.plural ] = newUnit
    newAliases[ 'cu_' + unit ] = newUnit
    newAliases[ 'cu_' + unitInfo.plural ] = newUnit
    newAliases[ 'cu' + unit ] = newUnit
    newAliases[ 'cu' + unitInfo.plural ] = newUnit

    newUnitInfo = RPNUnitInfo( 'volume', newUnit, newUnit, abbrev, [ ],
                               unitInfo.categories, True )

    return newUnitInfo, newAliases


# //******************************************************************************
# //
# //  createAreaAndVolumeOperators
# //
# //******************************************************************************

def createAreaAndVolumeOperators( unitOperators ):
    newOperators = { }
    newAliases = { }

    for unit in unitOperators:
        unitInfo = unitOperators[ unit ]

        if unitInfo.representation != unit:
            newAliases[ unitInfo.representation ] = unit

        if unitInfo.unitType == 'length':
            newUnit = unit + '^2'

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = \
                    makeAreaOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnit = unit + '^2'
                newAliases[ compoundUnit ] = newUnit

            newUnit = unit + '^3'

            if newUnit not in unitOperators:
                newUnitInfo, newUnitAliases = \
                    makeVolumeOperator( unit, unitOperators[ unit ].plural )

                newAliases.update( newUnitAliases )
                newOperators[ newUnit ] = newUnitInfo

                compoundUnit = unit + '^3'
                newAliases[ compoundUnit ] = newUnit

    return newOperators, newAliases


# //******************************************************************************
# //
# //  expandCompoundTimeUnits
# //
# //******************************************************************************

def expandCompoundTimeUnits( unitConversionMatrix, unitOperators, newAliases ):
    newUnitOperators = { }

    # We need to store the new ones in a different dictionary because we can't
    # modified unitOperators while iterating through it.  This is only guaranteed
    # a single unit compounded with seconds, but that's all I'm interested in.
    for unit in unitOperators:
        unitRoot = ''

        if unit[ -7 : ] == '*second' and not any( ( c in [ '*^/' ] ) for c in unit ):
            unitRoot = unit[ : -7 ]

        if unit[ : 7 ] == 'second*' and not any( ( c in [ '*^/' ] ) for c in unit ):
            unitRoot = unit[ 7 : ]

        if '/' in unitRoot:
            continue

        if unitRoot:
            newRoots = [ unitRoot ]

            if unitRoot in metricUnits:
                for prefix in metricPrefixes:
                    newRoots.append( prefix[ 0 ] + unitRoot )

            for newRoot in newRoots:
                if newRoot not in unitOperators:
                    continue

                unitInfo = unitOperators[ newRoot ]
                rootUnitInfo = unitOperators[ newRoot ]

                for timeUnit in timeUnits:
                    newUnit = newRoot + '*' + timeUnit[ 0 ]

                    # make a bunch of obvious aliases
                    newAliases[ newRoot + '-' + timeUnit[ 0 ] ] = newUnit
                    newPlural = newRoot + '-' + timeUnit[ 1 ]
                    newAliases[ newPlural ] = newUnit
                    newAliases[ newRoot + '-' + timeUnit[ 1 ] ] = newUnit

                    # We assume the abbrev ends with an s for second
                    if unitInfo.abbrev != '':
                        newAbbrev = unitInfo.abbrev + timeUnit[ 2 ]
                        newAliases[ newAbbrev ] = newUnit

                    for alias in rootUnitInfo.aliases:
                        newAliases[ alias + '*' + timeUnit[ 0 ] ] = newUnit
                        newAliases[ alias + '-' + timeUnit[ 0 ] ] = newUnit

                        if timeUnit[ 0 ] != timeUnit[ 1 ]:
                            newAliases[ alias + '*' + timeUnit[ 1 ] ] = newUnit
                            newAliases[ alias + '-' + timeUnit[ 1 ] ] = newUnit

                    newUnitOperators[ newUnit ] = \
                        RPNUnitInfo( unitInfo.unitType, newRoot + '*' + timeUnit[ 0 ], newPlural,
                                     '', [ ], unitInfo.categories, True )

                    conversion = mpmathify( timeUnit[ 3 ] )
                    unitConversionMatrix[ ( newUnit, unit ) ] = conversion
                    unitConversionMatrix[ ( unit, newUnit ) ] = fdiv( 1, conversion )

    unitOperators.update( newUnitOperators )


# //******************************************************************************
# //
# //  extrapolateTransitiveConversions
# //
# //******************************************************************************

def extrapolateTransitiveConversions( op1, op2, unitTypeTable, unitType, unitConversionMatrix ):
    newConversions = { }

    for op3 in unitTypeTable[ unitType ]:
        # we can ignore duplicate operators
        if op3 in [ op1, op2 ]:
            continue

        conversion = unitConversionMatrix[ ( op1, op2 ) ]

        if ( op1, op3 ) not in unitConversionMatrix and \
           ( op2, op3 ) in unitConversionMatrix:
            # print( 'transitive: ', ( op2, op3 ),
            #        unitConversionMatrix[ ( op2, op3 ) ] )
            newConversion = fmul( conversion, unitConversionMatrix[ ( op2, op3 ) ] )
            # print( ( op1, op3 ), newConversion )
            newConversions[ ( op1, op3 ) ] = newConversion
            # print( ( op3, op1 ), fdiv( 1, newConversion ) )
            newConversions[ ( op3, op1 ) ] = fdiv( 1, newConversion )
        elif ( op2, op3 ) not in unitConversionMatrix and \
             ( op1, op3 ) in unitConversionMatrix:
            # print( 'transitive: ', ( op1, op3 ),
            #        unitConversionMatrix[ ( op1, op3 ) ] )
            newConversion = fdiv( unitConversionMatrix[ ( op1, op3 ) ], conversion )
            # print( ( op2, op3 ), newConversion )
            newConversions[ ( op2, op3 ) ] = newConversion
            # print( ( op3, op2 ), fdiv( 1, newConversion ) )
            newConversions[ ( op3, op2 ) ] = fdiv( 1, newConversion )

    return newConversions


# //******************************************************************************
# //
# //  testAllCombinations
# //
# //  Let's make sure all the conversions exist (except for transitive conversions
# //  involving units that use the special unit conversion matrix.
# //
# //  This means this test will print out some errors regardless.
# //
# //******************************************************************************

def testAllCombinations( unitTypeTable, unitConversionMatrix ):
    for unitType in unitTypeTable:
        print( unitType, '*************************************************' )

        for unit1, unit2 in itertools.combinations( unitTypeTable[ unitType ], 2 ):
            if ( unit1, unit2 ) not in unitConversionMatrix and \
               ( unit1, unit2 ) not in specialUnitConversionMatrix:
                print( 'conversion not found for', unit1, 'and', unit2 )


# //******************************************************************************
# //
# //  testAllConversions
# //
# //  Let's prove the conversions are consistent.
# //
# //******************************************************************************

def testAllConversions( unitTypeTable, unitConversionMatrix ):
    for unitType in unitTypeTable:
        for unit1, unit2, unit3 in itertools.permutations( unitTypeTable[ unitType ], 3 ):
            try:
                factor1 = unitConversionMatrix[ unit1, unit2 ]
                factor2 = unitConversionMatrix[ unit2, unit3 ]
                factor3 = unitConversionMatrix[ unit1, unit3 ]
            except:
                continue

            if not almosteq( fmul( factor1, factor2 ), factor3, rel_eps=1.0e-10 ):
                print( 'conversion inconsistency found for ' + unit1 + ', ' + unit2 + ', and', unit3 )
                print( factor1, factor2, factor3 )
                print( fmul( factor1, factor2 ), factor3 )
                print( )


# //******************************************************************************
# //
# //  initializeConversionMatrix
# //
# //******************************************************************************

def initializeConversionMatrix( unitConversionMatrix ):
    # reverse each conversion
    print( 'Reversing each conversion...' )

    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        conversion = fdiv( 1, unitConversionMatrix[ ( op1, op2 ) ] )
        newConversions[ ( op2, op1 ) ] = conversion

    unitConversionMatrix.update( newConversions )

    # create area and volume units from all of the length units
    print( 'Creating area and volume units for all length units...' )

    newOperators, newAliases = createAreaAndVolumeOperators( unitOperators )

    unitOperators.update( newOperators )

    # add new conversions for the new area and volume units
    print( 'Adding new conversions for the new area and volume units...' )

    newConversions = { }

    for op1, op2 in unitConversionMatrix:
        if unitOperators[ op1 ].unitType == 'length':
            conversion = unitConversionMatrix[ ( op1, op2 ) ]
            newConversions[ ( op1 + '^2', op2 + '^2' ) ] = power( conversion, 2 )
            newConversions[ ( op1 + '^3', op2 + '^3' ) ] = power( conversion, 3 )

    unitConversionMatrix.update( newConversions )

    print( 'Expanding metric units against the list of SI prefixes...' )

    metricConversions, metricAliases = expandMetricUnits( )

    unitConversionMatrix.update( metricConversions )
    newAliases.update( metricAliases )

    print( 'Expanding data units against the list of SI and binary prefixes...' )
    unitConversionMatrix.update( expandDataUnits( ) )

    # add new operators for compound time units
    print( 'Expanding compound time units...' )

    expandCompoundTimeUnits( unitConversionMatrix, unitOperators, newAliases )

    # extrapolate transitive conversions
    print( )
    print( 'Extrapolating transitive conversions for', len( unitOperators ), 'units...' )

    unitTypeTable = makeUnitTypeTable( unitOperators )

    for unitType in sorted( basicUnitTypes ):
        if unitType != '_null_type':
            print( '\r     ', unitType, '({} units)'.format( len( unitTypeTable[ unitType ] ) ) )

        while True:
            newConversions = { }

            for op1, op2 in itertools.combinations( unitTypeTable[ unitType ], 2 ):
                if ( op1, op2 ) in unitConversionMatrix:
                    # print( )
                    # print( ( op1, op2 ), ': ', unitConversionMatrix[ ( op1, op2 ) ] )
                    newConversions.update( \
                        extrapolateTransitiveConversions( op1, op2, unitTypeTable, unitType, \
                                                          unitConversionMatrix ) )

            if not newConversions:
                break

            unitConversionMatrix.update( newConversions )

            print( '\r' + str( len( unitConversionMatrix ) ), end='' )

    print( '\r' + str( len( unitConversionMatrix ) ) + ' conversions' )

    # make some more aliases
    print( '        ' )
    print( 'Making some more aliases...' )

    newAliases.update( makeAliases( ) )

    print( 'Stringifying conversion matrix values...' )
    for op1, op2 in unitConversionMatrix:
        unitConversionMatrix[ ( op1, op2 ) ] = str( unitConversionMatrix[ ( op1, op2 ) ] )

    print( 'Saving everything...' )

    # save the list of unit operator names and aliases
    fileName = getDataPath( ) + os.sep + 'unit_names.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( list( unitOperators.keys( ) ), pickleFile )
        pickle.dump( list( constantOperators.keys( ) ), pickleFile )
        pickle.dump( newAliases, pickleFile )

    # save the actual unit data
    fileName = getDataPath( ) + os.sep + 'units.pckl.bz2'

    #testAllCombinations( unitTypeTable, unitConversionMatrix )
    #testAllConversions( unitTypeTable, unitConversionMatrix )

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicUnitTypes, pickleFile )
        pickle.dump( unitOperators, pickleFile )
        pickle.dump( constantOperators, pickleFile )

    fileName = getDataPath( ) + os.sep + 'unit_conversions.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( unitConversionMatrix, pickleFile )

    unitTypeDict = { }

    for unitType in basicUnitTypes.keys( ):
        unitTypeDict[ unitType ] = list( )

    for unit in unitOperators:
        unitTypeDict[ unitOperators[ unit ].unitType ].append( unit )

    fileName = getDataPath( ) + os.sep + 'unit_help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( unitTypeDict, pickleFile )

    print( )
    print( '{:,} unit operators'.format( len( unitOperators ) ) )
    print( '{:,} unit conversions'.format( len( unitConversionMatrix ) ) )
    print( '{:,} aliases'.format( len( newAliases ) ) )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    print( PROGRAM_NAME + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    initializeConversionMatrix( unitConversionMatrix )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

