#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnMeasurement.py
#//
#//  RPN command-line calculator, Measurements class
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

import rpnGlobals as g


#//******************************************************************************
#//
#//  getUnitType
#//
#//******************************************************************************

def getUnitType( unit ):
    if unit in g.basicUnitTypes:
        return unit

    if unit in operatorAliases:
        unit = operatorAliases[ unit ]

    if unit in g.unitOperators:
        return g.unitOperators[ unit ].unitType
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


#//******************************************************************************
#//
#//  getSimpleUnitType
#//
#//******************************************************************************

def getSimpleUnitType( unit ):
    if unit in g.unitOperators:
        return g.unitOperators[ unit ].representation
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


#//******************************************************************************
#//
#//  getUnitList
#//
#//******************************************************************************

def getUnitList( units ):
    unitList = [ ]

    for unit in units:
        for i in range( units[ unit ] ):
            unitList.append( unit )

    return unitList


#//******************************************************************************
#//
#//  combineUnits
#//
#//  Combine units2 into units1
#//
#//******************************************************************************

def combineUnits( units1, units2 ):
    if g.unitConversionMatrix is None:
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
#//  class Units
#//
#//******************************************************************************

class Units( dict ):
    def __init__( self, *arg, **kw ):
        if ( len( arg ) == 1 ):
            if isinstance( arg[ 0 ], str ):
                self.update( self.parseUnitString( arg[ 0 ] ) )
            elif isinstance( arg[ 0 ], ( list, tuple ) ):
                for item in arg[ 0 ]:
                    self.increment( item )
        else:
            super( Units, self ).__init__( *arg, **kw )


    def increment( self, value, amount=1 ):
        if isinstance( value, Units ):
            for unit in value:
                self.increment( unit, value[ unit ] * amount )
        else:
            if value not in self:
                self[ value ] = amount
            else:
                self[ value ] = self[ value ] + amount

        return self


    def decrement( self, value, amount=1 ):
        if isinstance( value, Units ):
            for unit in value:
                self.decrement( unit, value[ unit ] * amount )
        else:
            if value not in self:
                self[ value ] = -amount
            else:
                self[ value ] = self[ value ] - amount

        return self


    def invert( self ):
        print( '!' )
        for unit in self:
            self[ unit ] = -( self[ unit ] )

        return self


    def getUnitTypes( self ):
        types = { }

        for unit in self:
            if unit not in g.basicUnitTypes and unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            if unitType in types:
                types[ unitType ] += self.units[ unit ]
            else:
                types[ unitType ] = self[ unit ]

        return types


    def simplify( self ):
        result = Units( )

        for unit in self:
            simpleUnits = Units( g.unitOperators[ unit ].representation )

            exponent = self.get( unit )

            if exponent != 1:   # handle exponent
                for unit2 in simpleUnits:
                    simpleUnits[ unit2 ] *= exponent

            result.increment( simpleUnits )

        return result


    def getBasicTypes( self ):
        result = Units( )

        for unitType in self.getUnitTypes( ):
            basicUnits = Units( g.basicUnitTypes[ unitType ].simpleTypes[ 0 ] )

            exponent = self[ unitType ]

            if exponent != 1:   # handle exponent
                for unitType2 in basicUnits:
                    basicUnits[ unitType2 ] *= exponent

            result = combineUnits( result, basicUnits )[ 1 ]

        return result


    def getUnitString( self ):
        resultString = ''

        for unit in sorted( self ):
            exponent = self.get( unit )

            if exponent > 0:
                if resultString != '':
                    resultString += '*'

                resultString += unit

                if exponent > 1:
                    resultString += '^' + str( int( exponent ) )

        denominator = ''

        for unit in sorted( self ):
            exponent = self.get( unit )

            if exponent < 0:
                if denominator != '':
                    denominator += '*'

                denominator += unit

                if exponent < -1:
                    denominator += '^' + str( int( -exponent ) )

        if denominator != '':
            resultString += '/' + denominator

        return resultString


    def parseUnitString( self, expression ):
        pieces = expression.split( '/' )

        if len( pieces ) > 2:
            raise ValueError( 'only one \'/\' is permitted' )
        elif len( pieces ) == 2:
            result = self.parseUnitString( pieces[ 0 ] )
            result.decrement( self.parseUnitString( pieces[ 1 ] ) )

            return result
        else:
            result = Units( )

            units = expression.split( '*' )

            for unit in units:
                if unit == '':
                    raise ValueError( 'wasn\'t expecting another \'*\'' )

                operands = unit.split( '^' )

                if len( operands ) > 2:
                    raise ValueError( 'wasn\'t expecting another exponent (parsing expression: \'' + expression + '\')' )
                else:
                    if len( operands ) == 2:
                        exponent = int( float( operands[ 1 ] ) )   # find out why this is needed 'rpn foot 4 power square_inch sqr convert'
                    else:
                        exponent = 1

                    if operands[ 0 ] in result:
                        result[ operands[ 0 ] ] += exponent
                    else:
                        result[ operands[ 0 ] ] = exponent

            return result

#//******************************************************************************
#//
#//  class Measurement
#//
#//******************************************************************************

class Measurement( mpf ):
    def __new__( cls, value, units=None, unitName=None, pluralUnitName=None ):
        if isinstance( value, list ):
            raise ValueError( 'cannot use a list for the value of a measurement' )

        return mpf.__new__( cls, value )


    def __init__( self, value, units=None, unitName=None, pluralUnitName=None ):
        mpf.__init__( value )

        self.units = Units( )

        if units is not None:
            if isinstance( units, str ):
                self.units = self.units.parseUnitString( units )
            elif isinstance( units, ( list, tuple ) ):
                for unit in units:
                    self.increment( unit )
            elif isinstance( units, dict ):
                self.update( units )
            else:
                raise ValueError( 'invalid units specifier' )

        self.unitName = unitName
        self.pluralUnitName = pluralUnitName


    def __eq__( self, other ):
        result = mpf.__eq__( other )

        if isinstance( other, Measurement ):
            result &= ( self.units == other.units )

        return result


    def __ne__( self, other ):
        return not __eq__( self, other )


    def increment( self, value, amount=1 ):
        self.unitName = None
        self.pluralUnitName = None

        if value not in self.units:
            self.units[ value ] = amount
        else:
            self.units[ value ] += amount


    def decrement( self, value, amount=1 ):
        self.unitName = None
        self.pluralUnitName = None

        if value not in self.units:
            self.units[ value ] = -amount
        else:
            self.units[ value ] -= amount


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

        newUnits = { }

        for unit in units:
            newUnits[ unit ] = -units[ unit ]

        return Measurement( value, newUnits )


    def dezeroUnits( self ):
        value = mpf( self )
        units = self.getUnits( )

        newUnits = { }

        for unit in units:
            if units[ unit ] != 0:
                newUnits[ unit ] = units[ unit ]

        return Measurement( value, newUnits, self.getUnitName( ), self.getPluralUnitName( ) )


    def normalizeUnits( self ):
        value = mpf( self )
        units = self.getUnits( )

        negative = True

        for unit in units:
            if units[ unit ] > 0:
                negative = False
                break

        if negative:
            return Measurement( value, units ).invert( )
        else:
            return Measurement( value, units, self.getUnitName( ), self.getPluralUnitName( ) )


    def update( self, units ):
        if not isinstance( units, dict ):
            raise ValueError( 'dict expected' )

        self.unitName = None
        self.pluralUnitName = None

        self.units.update( units )


    def isCompatible( self, other ):
        if isinstance( other, dict ):
            return self.getTypes( ) == other
        elif isinstance( other, list ):
            result = True

            for item in other:
                result = self.isCompatible( item )

                if not result:
                    break

            return result
        elif isinstance( other, Measurement ):
            debugPrint( 'types: ', self.getTypes( ), other.getTypes( ) )
            debugPrint( 'simple types: ', self.getSimpleTypes( ), other.getSimpleTypes( ) )
            debugPrint( 'basic types: ', self.getBasicTypes( ), other.getBasicTypes( ) )

            if self.getTypes( ) == other.getTypes( ):
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


    def getTypes( self ):
        types = Units( )

        for unit in self.units:
            #print( 'unit: ', unit )
            if unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            if unitType in types:
                types[ unitType ] += self.units[ unit ]
            else:
                types[ unitType ] = self.units[ unit ]

        #print( 'types:', types )
        return types


    def getSimpleTypes( self ):
        return self.units.simplify( )


    def getBasicTypes( self ):
        return self.getTypes( ).getBasicTypes( )


    def getReduced( self ):
        if g.unitConversionMatrix is None:
            loadUnitConversionMatrix( )

        reduced = Measurement( mpf( self ), Units( ) )

        for unit in self.units:
            if unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            newUnit = g.basicUnitTypes[ unitType ].baseUnit

            if unit != newUnit:
                value = power( mpf( g.unitConversionMatrix[ ( unit, newUnit ) ] ), self.units[ unit ] )
            else:
                value = '1.0'

            if self.units[ unit ] != 1:
                newUnit = newUnit + '^' + str( self.units[ unit ] )

            reduced = reduced.multiply( Measurement( value, Units( newUnit ) ) )

        return reduced


    def convertValue( self, other ):
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

            if unit1String in operatorAliases:
                unit1String = operatorAliases[ unit1String ]

            if unit2String in operatorAliases:
                unit2String = operatorAliases[ unit2String ]

            debugPrint( 'unit1String: ', unit1String )
            debugPrint( 'unit2String: ', unit2String )

            exponents = { }

            if g.unitConversionMatrix is None:
                loadUnitConversionMatrix( )

            # look for a straight-up conversion
            if ( unit1String, unit2String ) in g.unitConversionMatrix:
                value = fmul( mpf( self ), mpmathify( g.unitConversionMatrix[ ( unit1String, unit2String ) ] ) )
            elif ( unit1String, unit2String ) in specialUnitConversionMatrix:
                value = specialUnitConversionMatrix[ ( unit1String, unit2String ) ]( mpf( self ) )
            else:
                conversionValue = mpmathify( 1 )

                if unit1String in g.compoundUnits:
                    # we need support for multiple compoundUnitInfo records for each compound type
                    # and a way to select the right one to use
                    compoundInfo = g.compoundUnits[ unit2String ]
                    newUnit1String = compoundInfo.type
                    conversionValue = fmul( conversionValue, compoundInfo.conversion )
                else:
                    newUnit1String = unit1String

                if unit2String in g.compoundUnits:
                    compoundInfo = g.compoundUnits[ unit2String ]
                    newUnit2String = compoundInfo.type
                    conversionValue = fmul( conversionValue, compoundInfo.conversion )
                else:
                    newUnit2String = unit2String

                debugPrint( 'newUnit1String: ', newUnit1String )
                debugPrint( 'newUnit2String: ', newUnit2String )

                if newUnit1String == newUnit2String:
                    return conversionValue

                # if that isn't found, then we need to do the hard work and break the units down
                for unit1 in units1:
                    foundConversion = False

                    for unit2 in units2:
                        debugPrint( '1 and 2:', unit1, unit2, units1[ unit1 ], units2[ unit2 ] )

                        if getUnitType( unit1 ) == getUnitType( unit2 ):
                            conversions.append( [ unit1, unit2 ] )
                            exponents[ ( unit1, unit2 ) ] = units1[ unit1 ]
                            foundConversion = True
                            break

                    if not foundConversion:
                        reduced = self.getReduced( )
                        reduced = reduced.convertValue( other )
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
            raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) +
                              ' and ' + other.getUnitString( ) )


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
    else:
        debugPrint( 'convertUnits' )
        debugPrint( 'unit1:', unit1.getTypes( ) )
        debugPrint( 'unit2:', unit2.getTypes( ) )

        return Measurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                            unit2.getUnitName( ), unit2.getPluralUnitName( ) )


