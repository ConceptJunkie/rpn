#!/usr/bin/env python

#******************************************************************************
#
#  rpnMeasurement.py
#
#  rpnChilada measurement operators and unit conversion
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import fdiv, fmul, nstr, mpmathify

from rpn.rpnDebug import debugPrint
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnUnitClasses import RPNUnits
from rpn.rpnUtils import oneArgFunctionEvaluator
from rpn.rpnValidator import argValidator, MeasurementValidator, MultiplicativeValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  convertUnits
#
#******************************************************************************

def convertUnits( unit1, unit2 ):
    if isinstance( unit1, RPNGenerator ):
        unit1 = list( unit1 )

        if len( unit1 ) == 1:
            unit1 = unit1[ 0 ]

    if isinstance( unit2, RPNGenerator ):
        unit2 = list( unit2 )

        if len( unit2 ) == 1:
            unit2 = unit2[ 0 ]

    if isinstance( unit1, list ):
        result = [ ]

        for unit in unit1:
            result.append( convertUnits( unit, unit2 ) )

        return result

    if not isinstance( unit1, RPNMeasurement ):
        raise ValueError( 'cannot convert non-measurements' )

    if isinstance( unit2, list ):
        return unit1.convertValue( unit2 )

    if isinstance( unit2, ( str, RPNUnits ) ):
        measurement = RPNMeasurement( 1, unit2 )
        return RPNMeasurement( unit1.convertValue( measurement ), unit2 )

    if not isinstance( unit2, ( list, str, RPNUnits, RPNMeasurement ) ):
        raise ValueError( 'cannot convert non-measurements' )

    debugPrint( 'convertUnits' )
    debugPrint( 'unit1:', unit1.getUnitTypes( ) )
    debugPrint( 'unit2:', unit2.getUnitTypes( ) )

    newValue = unit1.convertValue( unit2 )

    debugPrint( '*** value:', newValue )

    return RPNMeasurement( newValue, unit2.units )


#@twoArgFunctionEvaluator( )  # This breaks the multiple unit conversion!
@argValidator( [ MeasurementValidator( ), MeasurementValidator( ) ] )
def convertUnitsOperator( unit1, unit2 ):
    return convertUnits( unit1, unit2 )


#******************************************************************************
#
#  convertToDMSOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def convertToDMSOperator( n ):
    return convertUnits( n, [ 'degree', 'arcminute', 'arcsecond' ] )


#******************************************************************************
#
#  estimateOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def estimateOperator( measurement ):
    if not isinstance( measurement, RPNMeasurement ):
        raise TypeError( 'incompatible type for estimating' )

    unitType = None

    dimensions = measurement.getDimensions( )

    for key, basicUnitType in g.basicUnitTypes.items( ):
        if dimensions == basicUnitType.dimensions:
            unitType = key
            break

    if unitType is None:
        return 'No estimates are available for this unit type'

    unitTypeInfo = g.basicUnitTypes[ unitType ]

    unit = RPNMeasurement( 1, unitTypeInfo.baseUnit )
    value = RPNMeasurement( measurement.convertValue( unit ), unit.units ).value

    if not unitTypeInfo.estimateTable:
        return 'No estimates are available for this unit type (' + unitType + ').'

    matchingKeys = [ key for key in unitTypeInfo.estimateTable if key <= value ]

    if matchingKeys:
        estimateKey = max( matchingKeys )

        multiple = fdiv( value, estimateKey )

        return 'approximately ' + nstr( multiple, 3 ) + ' times ' + \
               unitTypeInfo.estimateTable[ estimateKey ]
    else:
        estimateKey = min( key for key in unitTypeInfo.estimateTable )

        multiple = fdiv( estimateKey, value )

        return 'approximately ' + nstr( multiple, 3 ) + ' times smaller than ' + \
               unitTypeInfo.estimateTable[ estimateKey ]


#******************************************************************************
#
#  applyNumberValueToUnit
#
#  We have to treat constant units differently because they can become plain
#  numbers.
#
#******************************************************************************

def applyNumberValueToUnit( number, term, constant ):
    if isinstance( term, RPNUnits ):
        value = RPNMeasurement( number, term )
        value = value.normalizeUnits( )

        if value.units == RPNUnits( '_null_unit' ):
            value = mpmathify( 1 )
    elif constant:
        if g.constantOperators[ term ].unit:
            value = RPNMeasurement( fmul( number, mpmathify( g.constantOperators[ term ].value ) ),
                                    g.constantOperators[ term ].unit )
        else:
            value = fmul( number, g.constantOperators[ term ].value )
    else:
        if g.unitOperators[ term ].unitType == 'constant':
            value = RPNMeasurement( number, term ).convertValue( RPNMeasurement( 1, { 'unity' : 1 } ) )
        else:
            value = RPNMeasurement( number, term )

    return value


#******************************************************************************
#
#  getDimensions
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getDimensionsOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.getDimensions( )
    else:
        return n


#******************************************************************************
#
#  convertToBaseUnitsOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def convertToBaseUnitsOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.convertToPrimitiveUnits( )
    else:
        return n


#******************************************************************************
#
#  convertToPrimitiveUnitsOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def convertToPrimitiveUnitsOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.convertToPrimitiveUnits( )
    else:
        return n


#******************************************************************************
#
#  invertUnitsOperator
#
#  invert the units and take the reciprocal of the value to create an
#  equivalent measurement
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MeasurementValidator( ) ] )
def invertUnitsOperator( measurement ):
    if not isinstance( measurement, RPNMeasurement ):
        raise ValueError( 'cannot invert non-measurements' )

    return measurement.getInverted( )
