#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnMeasurement.py
#//
#//  RPN command-line calculator, Measurements class and unit conversion
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import collections
import itertools

from mpmath import *

from fractions import Fraction

from rpnUtils import *
from rpnOperators import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  getSimpleUnitType
#//
#//******************************************************************************

def getSimpleUnitType( unit ):
    if unit in g.operatorAliases:
        unit = g.operatorAliases[ unit ]

    if unit in g.unitOperators:
        return g.unitOperators[ unit ].representation
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


#//******************************************************************************
#//
#//  combineUnits
#//
#//  Combine units2 into units1
#//
#//******************************************************************************

def combineUnits( units1, units2 ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    newUnits = Units( )
    newUnits.update( units1 )

    factor = mpmathify( 1 )

    for unit2 in units2:
        if unit2 in newUnits:
            newUnits[ unit2 ] += units2[ unit2 ]
        else:
            for unit1 in units1:
                if unit1 == unit2:
                    newUnits[ unit2 ] += units2[ unit2 ]
                    break
                elif getUnitType( unit1 ) == getUnitType( unit2 ):
                    factor = fdiv( factor, pow( mpmathify( g.unitConversionMatrix[ ( unit1, unit2 ) ] ), units2[ unit2 ] ) )
                    newUnits[ unit1 ] += units2[ unit2 ]
                    break
            else:
                newUnits[ unit2 ] = units2[ unit2 ]

    return factor, newUnits


#//******************************************************************************
#//
#//  class Measurement
#//
#//******************************************************************************

class Measurement( mpf ):
    #@property
    #def units( self ):
    #    return self.units
    #
    #@units.setter
    #def units( self, value ):
    #    self.units.clear( )
    #    self.units.update( value )

    def __new__( cls, value, units=None, unitName=None, pluralUnitName=None ):
        if isinstance( value, list ):
            raise ValueError( 'cannot use a list for the value of a measurement' )

        return mpf.__new__( cls, value )


    def __init__( self, value, units=None, unitName=None, pluralUnitName=None ):
        mpf.__init__( value )
        self.units = Units( units )
        self.unitName = unitName
        self.pluralUnitName = pluralUnitName


    def __eq__( self, other ):
        result = mpf.__eq__( other )

        if isinstance( other, Measurement ):
            result &= ( self.units == other.units )

        return result


    def __ne__( self, other ):
        return not __eq__( self, other )


    def __str__( self ):
        return 'Measurement(' + str( mpf( self ) ) + ', { ' + \
               ', '.join( [ '(\'' + name + '\', ' + str( self.units[ name ] ) + ')' for name in self.units ] ) + ' })'


    def increment( self, value, amount=1 ):
        self.unitName = None
        self.pluralUnitName = None
        self.units[ value ] += amount


    def decrement( self, value, amount=1 ):
        self.unitName = None
        self.pluralUnitName = None
        self.units[ value ] = -amount


    def add( self, other ):
        if isinstance( other, Measurement ):
            if self.getUnits( ) == other.getUnits( ):
                return Measurement( fadd( self, other ), self.getUnits( ),
                                    self.getUnitName( ), self.getPluralUnitName( ) )
            else:
                newOther = other.convertValue( self )
                return Measurement( fadd( self, newOther ), self.getUnits( ),
                                    self.getUnitName( ), self.getPluralUnitName( ) )
        else:
            return Measurement( fadd( self, other ), self.getUnits( ),
                                self.getUnitName( ), self.getPluralUnitName( ) )


    def subtract( self, other ):
        if isinstance( other, Measurement ):
            if self.getUnits( ) == other.getUnits( ):
                return Measurement( fsub( self, other ), self.getUnits( ),
                                    self.getUnitName( ), self.getPluralUnitName( ) )
            else:
                newOther = other.convertValue( self )
                return Measurement( fsub( self, newOther ), self.getUnits( ),
                                    self.getUnitName( ), self.getPluralUnitName( ) )

        else:
            return Measurement( fsub( self, other ), self.getUnits( ),
                                self.getUnitName( ), self.getPluralUnitName( ) )


    def multiply( self, other ):
        newValue = fmul( self, other )

        if isinstance( other, Measurement ):
            factor, newUnits = combineUnits( self.getUnits( ).simplify( ), other.getUnits( ).simplify( ) )

            self = Measurement( fmul( newValue, factor ), newUnits )
        else:
            self = Measurement( newValue, self.getUnits( ),
                                self.getUnitName( ), self.getPluralUnitName( ) )

        return self.dezeroUnits( )


    def divide( self, other ):
        newValue = fdiv( self, other )

        if isinstance( other, Measurement ):
            factor, newUnits = combineUnits( self.getUnits( ).simplify( ),
                                             other.getUnits( ).invert( ).simplify( ) )

            self = Measurement( fmul( newValue, factor ), newUnits )
        else:
            self = Measurement( newValue, self.getUnits( ),
                                self.getUnitName( ), self.getPluralUnitName( ) )

        return self.dezeroUnits( )


    def exponentiate( self, exponent ):
        if ( floor( exponent ) != exponent ):
            raise ValueError( 'cannot raise a measurement to a non-integral power' )

        newValue = power( self, exponent )

        for unit in self.units:
            self.units[ unit ] *= exponent

        self = Measurement( newValue, self.units )

        return self


    def invert( self ):
        value = mpf( self )
        units = self.getUnits( )

        newUnits = Units( )

        for unit in units:
            newUnits[ unit ] = -units[ unit ]

        return Measurement( value, newUnits )


    def dezeroUnits( self ):
        value = mpf( self )
        units = self.getUnits( )

        newUnits = Units( )

        for unit in units:
            if units[ unit ] != 0:
                newUnits[ unit ] = units[ unit ]

        return Measurement( value, newUnits, self.getUnitName( ), self.getPluralUnitName( ) )


    def update( self, units ):
        for i in self.units:
            del self.units[ i ]

        if not isinstance( units, dict ):
            raise ValueError( 'dict expected' )

        self.unitName = None
        self.pluralUnitName = None

        self.units.update( units )


    def isCompatible( self, other ):
        if isinstance( other, dict ):
            return self.getUnitTypes( ) == other
        elif isinstance( other, list ):
            result = True

            for item in other:
                result = self.isCompatible( item )

                if not result:
                    break

            return result
        elif isinstance( other, Measurement ):
            debugPrint( 'units: ', self.units, other.units )
            debugPrint( 'types: ', self.getUnitTypes( ), other.getUnitTypes( ) )
            debugPrint( 'simple types: ', self.getSimpleTypes( ), other.getSimpleTypes( ) )
            debugPrint( 'basic types: ', self.getBasicTypes( ), other.getBasicTypes( ) )
            debugPrint( 'primitive types: ', self.getPrimitiveTypes( ), other.getPrimitiveTypes( ) )

            if self.getUnitTypes( ) == other.getUnitTypes( ):
                return True
            elif self.getSimpleTypes( ) == other.getSimpleTypes( ):
                return True
            elif self.getBasicTypes( ) == other.getBasicTypes( ):
                return True
            else:
                debugPrint( 'Measurement.isCompatible exiting with false...' )
                return False
        else:
            raise ValueError( 'Measurement or dict expected' )


    def isEquivalent( self, other ):
        if isinstance( other, list ):
            result = True

            for item in other:
                result = self.isEquivalent( item )

                if not result:
                    break

            return result
        elif isinstance( other, Measurement ):
            if self.units == other.units:
                return True
            else:
                return self.getSimpleTypes( ) == other.getSimpleTypes( )
        else:
            raise ValueError( 'Measurement or dict expected' )


    def getValue( self ):
        return mpf( self )


    def getUnits( self ):
        return self.units


    def getUnitString( self ):
        return self.units.getUnitString( )


    def getUnitName( self ):
        return self.unitName


    def getPluralUnitName( self ):
        return self.pluralUnitName


    def getUnitTypes( self ):
        types = Units( )

        for unit in self.units:
            if unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            if unitType in types:
                types[ unitType ] += self.units[ unit ]
            elif self.units[ unit ] != 0:
                types[ unitType ] = self.units[ unit ]

        return types


    def getSimpleTypes( self ):
        return self.units.simplify( )


    def getBasicTypes( self ):
        return self.getUnitTypes( ).getBasicTypes( )


    def getPrimitiveTypes( self ):
        return self.getUnitTypes( ).getPrimitiveTypes( )


    def getReduced( self ):
        debugPrint( 'getReduced 1:', self, [ ( i, self.units[ i ] ) for i in self.units ] )
        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        value = mpf( self )
        units = Units( )

        for unit in self.units:
            newUnit = g.basicUnitTypes[ getUnitType( unit ) ].baseUnit
            debugPrint( 'newUnit', newUnit )

            if unit != newUnit:
                value = fmul( value, power( mpf( g.unitConversionMatrix[ ( unit, newUnit ) ] ), self.units[ unit ] ) )

            units.update( Units( g.unitOperators[ newUnit ].representation + "^" + str( self.units[ unit ] ) ) )

        reduced = Measurement( value, units )
        debugPrint( 'getReduced 2:', reduced )
        return reduced


    def convertValue( self, other ):
        if self.isEquivalent( other ):
            return mpf( 1.0 )

        if self.isCompatible( other ):
            conversions = [ ]

            if isinstance( other, list ):
                result = [ ]
                source = self

                for count, measurement in enumerate( other ):
                    conversion = source.convertValue( measurement )

                    if count < len( other ) - 1:
                        newValue = floor( mpf( conversion ) )
                    else:
                        newValue = mpf( conversion )

                    result.append( Measurement( newValue, measurement.getUnits( ) ) )

                    source = Measurement( fsub( mpf( conversion ), newValue ), measurement.getUnits( ) )

                return result

            units1 = self.getUnits( )
            units2 = other.getUnits( )

            unit1String = units1.getUnitString( )
            unit2String = units2.getUnitString( )

            if unit1String == unit2String:
                return fmul( mpf( self ), mpf( other ) )

            if unit1String in g.operatorAliases:
                unit1String = g.operatorAliases[ unit1String ]

            if unit2String in g.operatorAliases:
                unit2String = g.operatorAliases[ unit2String ]

            debugPrint( 'unit1String: ', unit1String )
            debugPrint( 'unit2String: ', unit2String )

            exponents = { }

            if not g.unitConversionMatrix:
                loadUnitConversionMatrix( )

            # look for a straight-up conversion
            if ( unit1String, unit2String ) in g.unitConversionMatrix:
                value = fmul( mpf( self ), mpmathify( g.unitConversionMatrix[ ( unit1String, unit2String ) ] ) )
            elif ( unit1String, unit2String ) in specialUnitConversionMatrix:
                value = specialUnitConversionMatrix[ ( unit1String, unit2String ) ]( mpf( self ) )
            else:
                # otherwise, we need to figure out how to do the conversion
                conversionValue = mpmathify( 1 )

                # if that isn't found, then we need to do the hard work and break the units down
                newUnits1 = Units( )

                for unit in units1:
                    newUnits1.update( Units( g.unitOperators[ unit ].representation + "^" + str( units1[ unit ] ) ) )

                newUnits2 = Units( )

                for unit in units2:
                    newUnits2.update( Units( g.unitOperators[ unit ].representation + "^" + str( units2[ unit ] ) ) )

                debugPrint( 'newUnits1:', newUnits1 )
                debugPrint( 'newUnits2:', newUnits2 )

                for unit1 in newUnits1:
                    foundConversion = False

                    for unit2 in newUnits2:
                        debugPrint( '1 and 2:', unit1, units1[ unit1 ], getUnitType( unit1 ),
                                    unit2, units2[ unit2 ], getUnitType( unit2 ) )

                        if getUnitType( unit1 ) == getUnitType( unit2 ):
                            conversions.append( [ unit1, unit2 ] )
                            exponents[ ( unit1, unit2 ) ] = units1[ unit1 ]
                            foundConversion = True
                            break

                    if not foundConversion:
                        debugPrint( 'didn\'t find a conversion, try reducing' )
                        reduced = self.getReduced( )

                        debugPrint( 'reduced:', self.units, reduced.units )

                        reducedOther = other.getReduced( )

                        if ( reduced.units == self.units ) and ( reducedOther.units == other.units ):
                            raise ValueError( 'unable to convert ' + self.getUnitString( ) +
                                              ' to ' + other.getUnitString( ) )

                        reduced = reduced.convertValue( reducedOther )
                        return reduced

                value = conversionValue

                for conversion in conversions:
                    if conversion[ 0 ] == conversion[ 1 ]:
                        continue  # no conversion needed

                    conversionValue = mpmathify( g.unitConversionMatrix[ tuple( conversion ) ] )
                    conversionValue = power( conversionValue, exponents[ tuple( conversion ) ] )
                    debugPrint( 'conversion: ', conversion, conversionValue )

                    value = fmul( value, conversionValue )

                value = fmul( mpf( self ), value )

            return value
        else:
            if isinstance( other, list ):
                otherUnit = '[ ' + ', '.join( [ unit.getUnitString( ) for unit in other ] ) + ' ]'
            else:
                otherUnit = other.getUnitString( )

            raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) +
                              ' and ' + otherUnit )


#//******************************************************************************
#//
#//  convertUnits
#//
#//******************************************************************************

def convertUnits( unit1, unit2 ):
    if isinstance( unit1, list ):
        result = [ ]

        for unit in unit1:
            result.append( convertUnits( unit, unit2 ) )

        return result

    if not isinstance( unit1, Measurement ):
        raise ValueError( 'cannot convert non-measurements' )


    if isinstance( unit2, list ):
        return unit1.convertValue( unit2 )
    elif isinstance( unit2, str ):
        measurement = Measurement( 1, { unit2 : 1 } )

        return Measurement( unit1.convertValue( measurement ), unit2 )
    elif not isinstance( unit2, Measurement ):
        raise ValueError( 'cannot convert non-measurements' )
    else:
        debugPrint( 'convertUnits' )
        debugPrint( 'unit1:', unit1.getUnitTypes( ) )
        debugPrint( 'unit2:', unit2.getUnitTypes( ) )

        return Measurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                            unit2.getUnitName( ), unit2.getPluralUnitName( ) )


#//******************************************************************************
#//
#//  convertToDMS
#//
#//******************************************************************************

def convertToDMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'degree' : 1 } ), Measurement( 1, { 'arcminute' : 1 } ),
                              Measurement( 1, { 'arcsecond' : 1 } ) ] )


#//******************************************************************************
#//
#//  estimate
#//
#//******************************************************************************

def estimate( measurement ):
    if isinstance( measurement, Measurement ):
        unitType = None

        for basicUnitType in g.basicUnitTypes:
            if measurement.isCompatible( Measurement( 1, g.basicUnitTypes[ basicUnitType ].baseUnit ) ):
                unitType = basicUnitType
                break

        if unitType is None:
            return 'No estimates are available for this unit type'

        unitTypeInfo = g.basicUnitTypes[ unitType ]

        unit = Measurement( 1, unitTypeInfo.baseUnit )
        value = mpf( Measurement( measurement.convertValue( unit ), unit.getUnits( ) ) )

        if len( unitTypeInfo.estimateTable ) == 0:
            return 'No estimates are available for this unit type (' + unitTypeOutput + ').'

        matchingKeys = [ key for key in unitTypeInfo.estimateTable if key <= mpf( value ) ]

        if len( matchingKeys ) == 0:
            estimateKey = min( key for key in unitTypeInfo.estimateTable )

            multiple = fdiv( estimateKey, value )

            return 'approximately ' + nstr( multiple, 3 ) + ' times smaller than ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
        else:
            estimateKey = max( matchingKeys )

            multiple = fdiv( value, estimateKey )

            return 'approximately ' + nstr( multiple, 3 ) + ' times ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
    elif isinstance( measurement, arrow.Arrow ):
        return measurement.humanize( )
    else:
        raise TypeError( 'incompatible type for estimating' )


