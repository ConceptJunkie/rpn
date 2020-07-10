#!/usr/bin/env python

# //******************************************************************************
# //
# //  makeUnits
# //
# //  rpnChilada unit conversion data generator
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  *** NOTE:  Don't run this file directly.  Use ../makeUnits.py.
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import argparse
import bz2
import contextlib
import itertools
import os
import pickle
import sys
import textwrap
import time

from mpmath import almosteq, mp, fdiv, fmul, fneg

if not hasattr( time, 'time_ns' ):
    from rpn.rpnNanoseconds import time_ns
else:
    from time import time_ns


#  This has to go here so the mpf's in the import get created with 52 places of precision.
mp.dps = 52

from rpn.rpnConstantOperators import *
from rpn.rpnMeasurement import specialUnitConversionMatrix
from rpn.rpnUnits import *
from rpn.rpnUtils import getUserDataPath
from rpn.rpnUnitTypes import basicUnitTypes
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'makeUnits'
PROGRAM_DESCRIPTION = 'rpnChilada unit conversion data generator'

validationPrecision = 20


# //******************************************************************************
# //
# //  printParagraph
# //
# //******************************************************************************

def printParagraph( text, indent = 0 ):
    lines = textwrap.wrap( text, 80 - ( indent + 1 ) )

    for line in lines:
        print( ' ' * indent + line )


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

    for unit, unitInfo in unitOperators.items( ):
        unitTypeTable[ unitInfo.unitType ].append( unit )

    return unitTypeTable


# //******************************************************************************
# //
# //  makeAliases
# //
# //******************************************************************************

def makeAliases( ):
    newAliases = { }

    for metricUnit in metricUnits:
        unitInfo = unitOperators[ metricUnit ]

        for prefix in metricPrefixes:
            unit = makeMetricUnit( prefix[ 0 ], metricUnit )
            pluralUnit = makeMetricUnit( prefix[ 0 ], unitInfo.plural )

            for alias in unitInfo.aliases:
                newAliases[ makeMetricUnit( prefix[ 0 ], alias ) ] = unit

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit             # add plural alias

    for integralMetricUnit in integralMetricUnits:
        unitInfo = unitOperators[ integralMetricUnit ]

        for prefix in metricPrefixes:
            if prefix[ 2 ] < 3:    # skip deca- and hecto- as well
                continue

            unit = makeMetricUnit( prefix[ 0 ], integralMetricUnit )
            pluralUnit = makeMetricUnit( prefix[ 0 ], unitInfo.plural )

            for alias in unitInfo.aliases:
                newAliases[ makeMetricUnit( prefix[ 0 ], alias ) ] = unit

            if pluralUnit != unit:
                newAliases[ pluralUnit ] = unit             # add plural alias

    for dataUnit in dataUnits:
        unitInfo = unitOperators[ dataUnit ]

        for prefix in dataPrefixes:
            newUnit = prefix[ 0 ] + dataUnit
            newPlural = prefix[ 0 ] + unitInfo.plural

            if newPlural != newUnit:
                newAliases[ newPlural ] = newUnit           # add plural alias

            for alias in unitInfo.aliases:
                newAliases[ prefix[ 0 ] + alias ] = newUnit

            if unitInfo.abbrev:
                newAliases[ prefix[ 1 ] + unitInfo.abbrev ] = newUnit

        for prefix in binaryPrefixes:
            newUnit = prefix[ 0 ] + dataUnit
            newPlural = prefix[ 0 ] + unitInfo.plural

            if newPlural != newUnit:
                newAliases[ newPlural ] = newUnit           # add plural alias

            for alias in unitInfo.aliases:
                newAliases[ prefix[ 0 ] + alias ] = newUnit

            if unitInfo.abbrev:
                newAliases[ prefix[ 1 ] + unitInfo.abbrev ] = newUnit

    for unit, unitInfo in unitOperators.items( ):
        if unitInfo.plural != unit and unitInfo.plural != '':
            newAliases[ unitInfo.plural ] = unit

        for alias in unitInfo.aliases:
            newAliases[ alias ] = unit

        if unitInfo.abbrev != '':
            newAliases[ unitInfo.abbrev ] = unit

    for constant, constantInfo in constantOperators.items( ):
        for alias in constantInfo.aliases:
            newAliases[ alias ] = constant

    for compoundTimeUnit in compoundTimeUnits:
        unitInfo = unitOperators[ compoundTimeUnit ]

        for timeUnit, abbrev in timeUnits.items( ):
            for metricPrefix in metricPrefixes:
                compoundUnit = metricPrefix[ 0 ] + compoundTimeUnit + '*' + timeUnit
                newAbbrev = metricPrefix[ 1 ] + unitInfo.abbrev + abbrev

                newAliases[ newAbbrev ] = compoundUnit

    # add area aliases
    for unit, unitInfo in unitOperators.items( ):
        if unitInfo.unitType == 'length':
            for prefix in [ 'sq', 'square', 'sq_', 'square_' ]:
                newAliases[ prefix + unit ] = unit + '^2'

                if unitInfo.plural != unit:
                    newAliases[ prefix + unitInfo.plural ] = unit + '^2'

                if unitInfo.abbrev:
                    newAliases[ prefix + unitInfo.abbrev ] = unit + '^2'

                for alias in unitInfo.aliases:
                    newAliases[ prefix + alias ] = unit + '^2'

            for prefix in [ 'cu', 'cubic', 'cu_', 'cubic_' ]:
                newAliases[ prefix + unit ] = unit + '^3'

                if unitInfo.plural != unit:
                    newAliases[ prefix + unitInfo.plural ] = unit + '^3'

                if unitInfo.abbrev:
                    newAliases[ prefix + unitInfo.abbrev ] = unit + '^3'

                for alias in unitInfo.aliases:
                    newAliases[ prefix + alias ] = unit + '^3'

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
        unitInfo = unitOperators[ metricUnit ]

        for prefix in metricPrefixes:
            if metricUnit not in unitOperators:
                continue

            newName = makeMetricUnit( prefix[ 0 ], metricUnit )
            newPlural = makeMetricUnit( prefix[ 0 ], unitInfo.plural )

            # construct unit operator info
            helpText = '\n\'Using the standard SI prefixes, ' + newName + '\' is the equivalent\nof ' + \
                       '{:,}'.format( 10 ** prefix[ 2 ] ) + ' times the value of \'' + metricUnit + \
                       '\'.\n\nPlease see the help entry for \'' + metricUnit + '\' for more information.'

            if unitInfo.abbrev:
                newAbbrev = prefix[ 1 ] + unitInfo.abbrev
            else:
                newAbbrev = ''

            unitOperators[ newName ] = \
                    RPNUnitInfo( unitInfo.unitType, newPlural, newAbbrev, [ ],
                                 unitInfo.categories, helpText, True )

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            metricConversions[ ( newName, metricUnit ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            metricConversions[ ( metricUnit, newName ) ] = newConversion

    for integralMetricUnit in integralMetricUnits:
        unitInfo = unitOperators[ integralMetricUnit ]

        for prefix in metricPrefixes:
            if prefix[ 2 ] < 3:      # we don't want deca- or hecto- here either.
                continue

            newName = makeMetricUnit( prefix[ 0 ], integralMetricUnit )
            newPlural = makeMetricUnit( prefix[ 0 ], unitInfo.plural )

            if unitInfo.abbrev:
                newAbbrev = prefix[ 1 ] + unitInfo.abbrev
            else:
                newAbbrev = ''

            # construct unit operator info
            helpText = '\n\'Using the standard SI prefixes, ' + newName + '\' is the equivalent\nof ' + \
                       '{:,}'.format( 10 ** prefix[ 2 ] ) + ' times the value of \'' + integralMetricUnit + \
                       '\'.\n\nPlease see the help entry for \'' + integralMetricUnit + '\' for more information.'

            unitOperators[ newName ] = \
                    RPNUnitInfo( unitInfo.unitType, newPlural, newAbbrev, [ ],
                                 unitInfo.categories, helpText, True )

            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            metricConversions[ ( newName, integralMetricUnit ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            metricConversions[ ( integralMetricUnit, newName ) ] = newConversion

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
        unitInfo = unitOperators[ dataUnit ]

        for prefix in dataPrefixes:
            newName = prefix[ 0 ] + dataUnit

            # constuct unit operator info
            helpText = '\n\'Using the standard SI prefixes, ' + newName + '\' is the equivalent\nof ' + \
                       '{:,}'.format( 10 ** prefix[ 2 ] ) + ' times the value of \'' + dataUnit + \
                       '\'.\n\nPlease see the help entry for \'' + dataUnit + '\' for more information.'

            if unitInfo.abbrev:
                newAbbrev = prefix[ 0 ] + unitInfo.abbrev
            else:
                newAbbrev = ''

            unitOperators[ newName ] = \
                RPNUnitInfo( unitInfo.unitType, prefix[ 0 ] + unitInfo.plural,
                             newAbbrev, [ ], unitInfo.categories, helpText, True )

            # create new conversions
            newConversion = power( 10, mpmathify( prefix[ 2 ] ) )
            newConversions[ ( newName, dataUnit ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            newConversions[ ( dataUnit, newName ) ] = newConversion

        for prefix in binaryPrefixes:
            newName = prefix[ 0 ] + dataUnit

            # constuct unit operator info
            helpText = '\n\'Using the binary data size prefixes, ' + newName + '\' is the equivalent\nof 2^' + \
                       str( prefix[ 2 ] ) + ' times the value of \'' + dataUnit + \
                       '\'.\n\nPlease see the help entry for \'' + dataUnit + '\' for more information.'

            if unitInfo.abbrev:
                newAbbrev = prefix[ 0 ] + unitInfo.abbrev
            else:
                newAbbrev = ''

            unitOperators[ newName ] = \
                RPNUnitInfo( unitInfo.unitType, prefix[ 0 ] + unitInfo.plural,
                             newAbbrev, [ ], unitInfo.categories, helpText, True )

            # create new conversions
            newConversion = power( 2, mpmathify( prefix[ 2 ] ) )
            newConversions[ ( newName, dataUnit ) ] = newConversion
            newConversion = fdiv( 1, newConversion )
            newConversions[ ( dataUnit, newName ) ] = newConversion

    return newConversions


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
# //  Let's make sure all the conversions exist.
# //
# //  For the case of transitive conversions involving units that use the
# //  special unit conversion matrix, we'll need to do checks, to see if we
# //  can convert to the base unit type on the way from converting from unit1
# //  to unit2.
# //
# //******************************************************************************

def testAllCombinations( unitTypeTable, unitConversionMatrix ):
    for unitType, unitList in unitTypeTable.items( ):
        for unit1, unit2 in itertools.combinations( unitList, 2 ):
            if ( unit1, unit2 ) not in unitConversionMatrix and \
               ( unit1, unit2 ) not in specialUnitConversionMatrix:
                baseUnit1 = basicUnitTypes[ unitOperators[ unit1 ].unitType ].baseUnit
                baseUnit2 = basicUnitTypes[ unitOperators[ unit2 ].unitType ].baseUnit

                if ( unit1, baseUnit1 ) not in unitConversionMatrix and \
                   ( unit1, baseUnit1 ) not in specialUnitConversionMatrix and \
                   ( baseUnit1, unit2 ) not in unitConversionMatrix and \
                   ( baseUnit1, unit2 ) not in specialUnitConversionMatrix:
                    print( 'conversion not found for', unit1, 'and', unit2 )


# //******************************************************************************
# //
# //  testAllConversions
# //
# //  Let's prove the conversions are consistent.
# //
# //******************************************************************************

def testAllConversions( unitTypeTable, unitConversionMatrix ):
    print( 'Testing all conversions for consistency...' )
    print( )

    validated = 0

    for unitType, unitList in unitTypeTable.items( ):
        for unit1, unit2, unit3 in itertools.permutations( unitList, 3 ):
            try:
                factor1 = unitConversionMatrix[ unit1, unit2 ]
                factor2 = unitConversionMatrix[ unit2, unit3 ]
                factor3 = unitConversionMatrix[ unit1, unit3 ]
            except:
                continue

            epsilon = power( 10, fneg( validationPrecision ) )

            if not almosteq( fmul( factor1, factor2 ), factor3, rel_eps=epsilon ):
                print( 'conversion inconsistency found for ' + unit1 + ', ' + unit2 + ', and', unit3, file=sys.stderr )
                print( unit1 + ' --> ' + unit2, factor1, file=sys.stderr )
                print( unit2 + ' --> ' + unit3, factor2, file=sys.stderr )
                print( unit3 + ' --> ' + unit1, factor3, file=sys.stderr )
                print( )

            validated += 1

            if validated % 1000 == 0:
                print( '\r' + '{:,} conversion permutations validated...'.format( validated ), end='' )

    print( '\r' + '{:,} conversion permutations were validated to {:,} digits precision.'. \
                                                                        format( validated, validationPrecision ) )
    print( 'No consistency problems detected.' )


# //******************************************************************************
# //
# //  initializeConversionMatrix
# //
# //******************************************************************************

def initializeConversionMatrix( unitConversionMatrix, validateConversions ):
    # reverse each conversion
    print( 'Reversing each conversion...' )

    newConversions = { }

    for ops, factor in unitConversionMatrix.items( ):
        conversion = fdiv( 1, factor )
        newConversions[ ( ops[ 1 ], ops[ 0 ] ) ] = conversion

    unitConversionMatrix.update( newConversions )

    print( 'Expanding metric units against the list of SI prefixes...' )

    metricConversions, metricAliases = expandMetricUnits( )

    unitConversionMatrix.update( metricConversions )
    newAliases = metricAliases

    print( 'Expanding data units against the list of SI and binary prefixes...' )
    unitConversionMatrix.update( expandDataUnits( ) )

    # add new operators for compound time units
    print( 'Expanding compound time units...' )

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

            print( '\r' + '{:,}'.format( len( unitConversionMatrix ) ), end='' )

    print( '\r' + '{:,} conversions'.format( len( unitConversionMatrix ) ) )

    # make some more aliases
    print( '        ' )
    print( 'Making some more aliases...' )

    newAliases.update( makeAliases( ) )

    print( 'Stringifying conversion matrix values...' )
    for ops, factor in unitConversionMatrix.items( ):
        unitConversionMatrix[ ( ops[ 0 ], ops[ 1 ] ) ] = str( factor )

    print( 'Saving everything...' )

    # save the list of unit operator names and aliases
    fileName = getUserDataPath( ) + os.sep + 'unit_names.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( list( unitOperators.keys( ) ), pickleFile )
        pickle.dump( list( constantOperators.keys( ) ), pickleFile )
        pickle.dump( newAliases, pickleFile )

    # save the actual unit data
    fileName = getUserDataPath( ) + os.sep + 'units.pckl.bz2'

    testAllCombinations( unitTypeTable, unitConversionMatrix )

    if validateConversions:
        testAllConversions( unitTypeTable, unitConversionMatrix )

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicUnitTypes, pickleFile )
        pickle.dump( unitOperators, pickleFile )
        pickle.dump( constantOperators, pickleFile )

    fileName = getUserDataPath( ) + os.sep + 'unit_conversions.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( unitConversionMatrix, pickleFile )

    unitTypeDict = { }

    for unitType in basicUnitTypes.keys( ):
        unitTypeDict[ unitType ] = list( )

    for unit, unitInfo in unitOperators.items( ):
        unitTypeDict[ unitInfo.unitType ].append( unit )

    fileName = getUserDataPath( ) + os.sep + 'unit_help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( unitTypeDict, pickleFile )

    print( )
    print( '{:,} unit operators'.format( len( unitOperators ) ) )
    print( '{:,} unit conversions'.format( len( unitConversionMatrix ) ) )
    print( '{:,} aliases'.format( len( newAliases ) ) )

    missingHelp = [ ]

    for unit, unitInfo in unitOperators.items( ):
        found = False

        for i in unitInfo.helpText:
            if i.isalnum( ):
                found = True
                break

        if not found:
            missingHelp.append( unit )

    if missingHelp:
        print( )
        print( 'The following {} units do not have help text:'.format( len( missingHelp ) ) )
        print( )
        printParagraph( ', '.join( sorted( missingHelp ) ) )

    missingHelp = [ ]

    for constant, constantInfo in constantOperators.items( ):
        found = False

        for i in constantInfo.helpText:
            if i.isalnum( ):
                found = True
                break

        if not found:
            missingHelp.append( constant )

    if missingHelp:
        print( )
        print( 'The following {} constants do not have help text:'.format( len( missingHelp ) ) )
        print( )
        printParagraph( ', '.join( sorted( missingHelp ) ) )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    print( PROGRAM_NAME + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    parser = argparse.ArgumentParser( prog = PROGRAM_NAME, description = PROGRAM_NAME + ' - ' +
                                      PROGRAM_DESCRIPTION + COPYRIGHT_MESSAGE,
                                      add_help = False,
                                      formatter_class = argparse.RawTextHelpFormatter,
                                      prefix_chars = '-' )

    parser.add_argument( '-v', '--validate_conversions', action = 'store_true' )

    args = parser.parse_args( sys.argv[ 1 : ] )

    validateConversions = args.validate_conversions

    startTime = time_ns( )

    initializeConversionMatrix( unitConversionMatrix, validateConversions )

    print( )
    print( 'Unit data completed.  Time elapsed:  {:.3f} seconds'.format( ( time_ns( ) - startTime ) / 1000000000 ) )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

