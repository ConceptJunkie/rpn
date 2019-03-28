#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnMeasurement.py
# //
# //  RPN command-line calculator, Measurements class and unit conversion
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections

from mpmath import chop, extradps, fadd, fdiv, floor, fmod, fmul, fprod, frac, \
                   fsub, log10, mpf, mpmathify, nstr, power, root

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnPersistence import loadUnitConversionMatrix
from rpn.rpnUnitClasses import getUnitDimensionList, \
                               getUnitDimensions, getUnitType, RPNUnits
from rpn.rpnUtils import debugPrint, flattenList, getPowerset, oneArgFunctionEvaluator

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  specialUnitConversionMatrix
# //
# //  This is for units that can't be converted with a simple multiplication
# //  factor.
# //
# //  Plus, I'm not going to do the transitive thing here, so it's necessary
# //  to explicitly state the conversions for all permutations.  That bugs me.
# //
# //  I would have included this table in makeUnits.py, but pickle doesn't
# //  work on lambdas, which is, to me, very non-Pythonic.   I could also
# //  save the expressions as strings and use eval, but that seems very
# //  non-Pythonic, too.
# //
# //  ( first unit, second unit, conversion function )
# //
# //  For temperature conversions, see
# //  https://en.wikipedia.org/wiki/Conversion_of_units_of_temperature.
# //
# //******************************************************************************

specialUnitConversionMatrix = {
    ( 'celsius', 'delisle' )                    : lambda c: fmul( fsub( 100, c ), fdiv( 3, 2 ) ),
    ( 'celsius', 'fahrenheit' )                 : lambda c: fadd( fmul( c, fdiv( 9, 5 ) ), 32 ),
    ( 'celsius', 'kelvin' )                     : lambda c: fadd( c, mpf( '273.15' ) ),
    ( 'celsius', 'rankine' )                    : lambda c: fmul( fadd( c, mpf( '273.15' ) ), fdiv( 9, 5 ) ),
    ( 'celsius', 'reaumur' )                    : lambda c: fmul( c, fdiv( 4, 5 ) ),
    ( 'celsius', 'romer' )                      : lambda c: fadd( fmul( c, fdiv( 21, 40 ) ), mpf( '7.5' ) ),

    ( 'delisle', 'celsius' )                    : lambda d: fsub( 100, fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle', 'degree_newton' )              : lambda d: fsub( 33, fmul( d, fdiv( 11, 50 ) ) ),
    ( 'delisle', 'fahrenheit' )                 : lambda d: fsub( 212, fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle', 'kelvin' )                     : lambda d: fsub( mpf( '373.15' ), fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle', 'rankine' )                    : lambda d: fsub( mpf( '671.67' ), fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle', 'reaumur' )                    : lambda d: fsub( 80, fmul( d, fdiv( 8, 15 ) ) ),
    ( 'delisle', 'romer' )                      : lambda d: fsub( 60, fmul( d, fdiv( 7, 20 ) ) ),

    ( 'degree_newton', 'delisle' )              : lambda n: fmul( fsub( 33, n ), fdiv( 50, 11 ) ),
    ( 'degree_newton', 'fahrenheit' )           : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), 32 ),
    ( 'degree_newton', 'kelvin' )               : lambda n: fadd( fmul( n, fdiv( 100, 33 ) ), mpf( '273.15' ) ),
    ( 'degree_newton', 'rankine' )              : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), mpf( '491.67' ) ),
    ( 'degree_newton', 'romer' )                : lambda n: fadd( fmul( n, fdiv( 35, 22 ) ), mpf( 7.5 ) ),

    ( 'fahrenheit', 'celsius' )                 : lambda f: fmul( fsub( f, 32 ), fdiv( 5, 9 ) ),
    ( 'fahrenheit', 'degree_newton' )           : lambda f: fmul( fsub( f, 32 ), fdiv( 11, 60 ) ),
    ( 'fahrenheit', 'delisle' )                 : lambda f: fmul( fsub( 212, f ), fdiv( 5, 6 ) ),
    ( 'fahrenheit', 'kelvin' )                  : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 5, 9 ) ), mpf( '273.15' ) ),
    ( 'fahrenheit', 'rankine' )                 : lambda f: fadd( f, mpf( '459.67' ) ),
    ( 'fahrenheit', 'reaumur' )                 : lambda f: fmul( fsub( f, 32 ), fdiv( 4, 9 ) ),
    ( 'fahrenheit', 'romer' )                   : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'kelvin', 'celsius' )                     : lambda k: fsub( k, mpf( '273.15' ) ),
    ( 'kelvin', 'degree_newton' )               : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 33, 100 ) ),
    ( 'kelvin', 'delisle' )                     : lambda k: fmul( fsub( mpf( '373.15' ), k ), fdiv( 3, 2 ) ),
    ( 'kelvin', 'fahrenheit' )                  : lambda k: fsub( fmul( k, fdiv( 9, 5 ) ), mpf( '459.67' ) ),
    ( 'kelvin', 'reaumur' )                     : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 4, 5 ) ),
    ( 'kelvin', 'romer' )                       : lambda k: fadd( fmul( fsub( k, mpf( '273.15' ) ), fdiv( 21, 40 ) ), mpf( 7.5 ) ),

    ( 'rankine', 'celsius' )                    : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 5, 9 ) ),
    ( 'rankine', 'degree_newton' )              : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 11, 60 ) ),
    ( 'rankine', 'delisle' )                    : lambda r: fmul( fsub( mpf( '671.67' ), r ), fdiv( 5, 6 ) ),
    ( 'rankine', 'fahrenheit' )                 : lambda r: fsub( r, mpf( '459.67' ) ),
    ( 'rankine', 'reaumur' )                    : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 4, 9 ) ),
    ( 'rankine', 'romer' )                      : lambda r: fadd( fmul( fsub( r, mpf( '491.67' ) ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'reaumur', 'delisle' )                    : lambda re: fmul( fsub( 80, re ), fdiv( 15, 8 ) ),
    ( 'reaumur', 'fahrenheit' )                 : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), 32 ),
    ( 'reaumur', 'kelvin' )                     : lambda re: fadd( fmul( re, fdiv( 5, 4 ) ), mpf( '273.15' ) ),
    ( 'reaumur', 'rankine' )                    : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), mpf( '491.67' ) ),
    ( 'reaumur', 'romer' )                      : lambda re: fadd( fmul( re, fdiv( 21, 32 ) ), mpf( 7.5 ) ),

    ( 'romer', 'celsius' )                      : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ),
    ( 'romer', 'degree_newton' )                : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 22, 35 ) ),
    ( 'romer', 'delisle' )                      : lambda ro: fmul( fsub( 60, ro ), fdiv( 20, 7 ) ),
    ( 'romer', 'fahrenheit' )                   : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), 32 ),
    ( 'romer', 'kelvin' )                       : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ), mpf( '273.15' ) ),
    ( 'romer', 'rankine' )                      : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), mpf( '491.67' ) ),
    ( 'romer', 'reaumur' )                      : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 32, 21 ) ),

    ( 'decibel-volt', 'volt' )                  : lambda dBV: power( 10, fdiv( dBV, 10 ) ),
    ( 'volt', 'decibel-volt' )                  : lambda V: fmul( log10( V ), 10 ),

    ( 'decibel-watt', 'watt' )                  : lambda dBW: power( 10, fdiv( dBW, 10 ) ),
    ( 'watt', 'decibel-watt' )                  : lambda W: fmul( log10( W ), 10 ),

    ( 'decibel-milliwatt', 'watt' )             : lambda dBm: power( 10, fdiv( fsub( dBm, 30 ), 10 ) ),
    ( 'watt', 'decibel-milliwatt' )             : lambda W: fmul( log10( fmul( W, 1000 ) ), 10 ),

    ( 'second', 'hertz' )                       : lambda second: fdiv( 1, second ),

    ( 'hertz', 'second' )                       : lambda hertz: fdiv( 1, hertz ),

    ( 'ohm', 'siemens' )                        : lambda ohm: fdiv( 1, ohm ),

    ( 'siemens', 'ohm' )                        : lambda siemens: fdiv( 1, siemens ),
}


# //******************************************************************************
# //
# //  getSimpleUnitType
# //
# //******************************************************************************

def getSimpleUnitType( unit ):
    if unit in g.operatorAliases:
        unit = g.operatorAliases[ unit ]

    if unit in g.unitOperators:
        return g.unitOperators[ unit ].representation
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


# //******************************************************************************
# //
# //  invertUnits
# //
# //  invert the units and take the reciprocal of the value to create an
# //  equivalent measurement
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def invertUnits( measurement ):
    if not isinstance( measurement, RPNMeasurement ):
        raise ValueError( 'cannot invert non-measurements' )

    return RPNMeasurement( fdiv( 1, measurement.getValue( ) ), measurement.invert( ).getUnits( ) )


# //******************************************************************************
# //
# //  class RPNMeasurement
# //
# //******************************************************************************

class RPNMeasurement( object ):
    '''This class represents a measurement, which includes a numerical value
    and an RPNUnits instance.'''
    value = mpf( )
    units = RPNUnits( )
    unitName = None
    pluralUnitName = None

    def __init__( self, value, units = RPNUnits( ), unitName = None, pluralUnitName = None ):
        if isinstance( value, str ):
            self.value = mpmathify( value )
            self.units = RPNUnits( units )
        elif isinstance( value, RPNMeasurement ):
            self.value = value.getValue( )
            self.units = RPNUnits( value.getUnits( ) )
        else:
            self.value = value
            self.units = RPNUnits( units )

        self.unitName = unitName
        self.pluralUnitName = pluralUnitName

    def __eq__( self, other ):
        if isinstance( other, RPNMeasurement ):
            result = mpf.__eq__( self.value, other.value )
        else:
            result = mpf.__eq__( self.value, other )

        if not result:
            return result

        if isinstance( other, RPNMeasurement ):
            result = ( self.units == other.units )

        return result

    def __ne__( self, other ):
        return not self.__eq__( other )

    def __lt__( self, other ):
        return self.isSmaller( other )

    def __gt__( self, other ):
        return self.isLarger( other )

    def __ge__( self, other ):
        return not self.isSmaller( other )

    def __le__( self, other ):
        return not self.isLarger( other )

    #def __repr__( self ):
    #    return 'RPNMeasurement(\'' + str( mpf( self ) ) + '\',' + \
    #           ( '{}' if self.units is None else '\'' + self.units.getUnitString( ) + '\'' ) + \
    #           '\'' + self.unitName + '\',\'' + self.pluralUnitName + '\')'

    #def __str__( self ):
    #    return repr( self )

    def increment( self, unit, amount = 1 ):
        self.unitName = None
        self.pluralUnitName = None
        self.units[ unit ] += amount

    def decrement( self, unit, amount = 1 ):
        increment( self, unit, -amount )

    def add( self, other ):
        if isinstance( other, RPNMeasurement ):
            if self.getUnits( ) == other.getUnits( ):
                return RPNMeasurement( fadd( self.value, other.value ), self.getUnits( ),
                                       self.getUnitName( ), self.getPluralUnitName( ) )
            else:
                newOther = other.convertValue( self )

                return RPNMeasurement( fadd( self.value, newOther ), self.getUnits( ),
                                       self.getUnitName( ), self.getPluralUnitName( ) )
        else:
            return RPNMeasurement( fadd( self.value, other ), self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

    def subtract( self, other ):
        if isinstance( other, RPNMeasurement ):
            if self.getUnits( ) == other.getUnits( ):
                return RPNMeasurement( fsub( self.value, other.value ), self.getUnits( ),
                                       self.getUnitName( ), self.getPluralUnitName( ) )
            else:
                newOther = other.convertValue( self )
                return RPNMeasurement( fsub( self.value, newOther ), self.getUnits( ),
                                       self.getUnitName( ), self.getPluralUnitName( ) )

        else:
            return RPNMeasurement( fsub( self.value, other ), self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

    def multiply( self, other ):
        if isinstance( other, RPNMeasurement ):
            newValue = fmul( self.value, other.value )

            factor, newUnits = self.getUnits( ).combineUnits( other.getUnits( ) )

            self = RPNMeasurement( fmul( newValue, factor ), newUnits )
        else:
            newValue = fmul( self.value, other )

            self = RPNMeasurement( newValue, self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

        return self.normalizeUnits( )

    def divide( self, other ):
        if isinstance( other, RPNMeasurement ):
            newValue = fdiv( self.value, other.value )

            factor, newUnits = self.getUnits( ).combineUnits( other.getUnits( ).inverted( ) )

            self = RPNMeasurement( fmul( newValue, factor ), newUnits )
        else:
            newValue = fdiv( self.value, other )

            self = RPNMeasurement( newValue, self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

        return self.normalizeUnits( )

    def getModulo( self, other ):
        if isinstance( other, RPNMeasurement ):
            measurement = RPNMeasurement( self )

            measurement = measurement.convert( other.getUnits( ) )
            measurement.setValue( fmod( measurement.getValue( ), other.getValue( ) ) )

            self = RPNMeasurement( measurement )
        else:
            self.setValue( fmod( self.getValue( ), other ) )

        return self.normalizeUnits( )

    def exponentiate( self, exponent ):
        if ( floor( exponent ) != exponent ):
            raise ValueError( 'cannot raise a measurement to a non-integral power' )

        exponent = int( exponent )

        newValue = power( self.value, exponent )

        for unit in self.units:
            self.units[ unit ] *= exponent

        self = RPNMeasurement( newValue, self.units )

        return self

    def getRoot( self, operand ):
        if ( floor( operand ) != operand ):
            raise ValueError( 'cannot take a fractional root of a measurement' )

        newUnits = RPNUnits( self.getUnits( ) )

        for unit, exponent in newUnits.items( ):
            if fmod( exponent, operand ) != 0:
                if operand == 2:
                    name = 'square'
                elif operand == 3:
                    name = 'cube'
                else:
                    name = getOrdinalName( operand )

                baseUnits = self.convertToBaseUnits( )

                if ( baseUnits != self ):
                    return baseUnits.getRoot( operand )
                else:
                    raise ValueError( 'cannot take the ' + name + ' root of this measurement: ', self.getUnits( ) )

            newUnits[ unit ] /= operand

        value = root( self.getValue( ), operand )

        return RPNMeasurement( value, newUnits ).normalizeUnits( )

    def invert( self ):
        units = self.getUnits( )

        newUnits = RPNUnits( )

        for unit in units:
            newUnits[ unit ] = -units[ unit ]

        return RPNMeasurement( self.value, newUnits )

    def normalizeUnits( self ):
        units = self.getUnits( ).normalizeUnits( )
        debugPrint( )
        debugPrint( 'normalize', units )

        # look for units that cancel between the numerator and denominator
        numerator, denominator = units.splitUnits( )

        # if we don't have a numerator or denominator, we're done
        if not numerator or not denominator:
            return RPNMeasurement( self.value, units )

        if not g.basicUnitTypes:
            loadUnitData( )

        debugPrint( 'numerator', numerator )
        debugPrint( 'denominator', denominator )

        nOriginalElements = sorted( list( numerator.elements( ) ) )
        dOriginalElements = sorted( list( denominator.elements( ) ) )

        changed = False

        nElements = [ ]

        for n in numerator:
            for i in range( min( numerator[ n ], 3 ) ):
                nElements.append( n )

        dElements = [ ]

        for d in denominator:
            for i in range( min( denominator[ d ], 3 ) ):
                dElements.append( d )

        debugPrint( 'nOriginalElements', nOriginalElements )
        debugPrint( 'nElements', nElements )

        debugPrint( 'dOriginalElements', dOriginalElements )
        debugPrint( 'dElements', dElements )

        matchFound = True   # technically not true yet, but it gets us into the loop

        conversionsNeeded = [ ]

        while matchFound:
            matchFound = False

            for nSubset in getPowerset( nElements ):
                for dSubset in getPowerset( dElements ):
                    #debugPrint( '))) nSubset', list( nSubset ) )
                    #debugPrint( '))) dSubset', list( dSubset ) )

                    nSubsetUnit = RPNUnits( '*'.join( sorted( list( nSubset ) ) ) )
                    dSubsetUnit = RPNUnits( '*'.join( sorted( list( dSubset ) ) ) )

                    #debugPrint( '1 nSubset', dSubsetUnit )
                    #debugPrint( '2 dSubset', dSubsetUnit )

                    if nSubsetUnit.getDimensions( ) == dSubsetUnit.getDimensions( ):
                        debugPrint( 'dimensions matched', dSubsetUnit.getDimensions( ) )
                        newNSubset = [ ]
                        newDSubset = [ ]

                        for n in nSubset:
                            baseUnit = g.basicUnitTypes[ getUnitType( n ) ].baseUnit

                            if n != baseUnit:
                                debugPrint( 'conversion added:', n, baseUnit )
                                conversionsNeeded.append( ( n, baseUnit ) )

                            newNSubset.append( baseUnit )

                        for d in dSubset:
                            baseUnit = g.basicUnitTypes[ getUnitType( d ) ].baseUnit

                            if d != baseUnit:
                                debugPrint( 'conversion added:', d, baseUnit )
                                conversionsNeeded.append( ( d, baseUnit ) )

                            newDSubset.append( baseUnit )

                        # TODO:  This maybe isn't quite what we want.
                        debugPrint( 'conversions added', '*'.join( sorted( newNSubset ) ),
                                                         '*'.join( sorted( newDSubset ) ) )
                        conversionsNeeded.append( ( '*'.join( sorted( newNSubset ) ),
                                                    '*'.join( sorted( newDSubset ) ) ) )
                        matchFound = True

                        for n in nSubset:
                            #print( 'nOriginalElements', nOriginalElements, 'n', n )
                            nOriginalElements.remove( n )
                            changed = True

                        for d in dSubset:
                            #print( 'dOriginalElements', dOriginalElements, 'd', d )
                            dOriginalElements.remove( d )
                            changed = True

                        break

                if matchFound:
                    break

            if matchFound:
                break

        debugPrint( 'final nElements', nOriginalElements )
        debugPrint( 'final dElements', dOriginalElements )

        # convert the value based on all the conversions we queued up
        convertedValue = self.getValue( )

        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        for i in conversionsNeeded:
            convertedValue = fmul( convertedValue, g.unitConversionMatrix[ i ] )

        # build up the resulting units
        units = RPNUnits( '*'.join( nOriginalElements ) )
        denominator = RPNUnits( '*'.join( dOriginalElements ) )

        for d in denominator:
            units[ d ] = denominator[ d ] * -1

        debugPrint( 'normalizeUnits final units', units )
        debugPrint( )

        if units:
            result = RPNMeasurement( convertedValue, units )

            if changed:
                return result.normalizeUnits( )
            else:
                return result
        else:
            return convertedValue

    def update( self, units ):
        for i in self.units:
            del self.units[ i ]

        if not isinstance( units, dict ):
            raise ValueError( 'dict expected' )

        self.unitName = None
        self.pluralUnitName = None

        self.units.update( units )

    def isCompatible( self, other ):
        if isinstance( other, str ):
            return self.isCompatible( RPNMeasurement( 1, other ) )
        if isinstance( other, RPNUnits ):
            return self.getUnitTypes( ) == other.getUnitTypes( )
        elif isinstance( other, RPNMeasurement ):
            debugPrint( 'isCompatible -----------------------' )
            debugPrint( 'units: ', self.units, other.units )
            debugPrint( 'types: ', self.getUnitTypes( ), other.getUnitTypes( ) )
            debugPrint( 'dimensions: ', self.getDimensions( ), other.getDimensions( ) )
            debugPrint( )

            if self.getUnitTypes( ) == other.getUnitTypes( ):
                return True
            elif self.getDimensions( ) == other.getDimensions( ):
                return True
            else:
                debugPrint( 'RPNMeasurement.isCompatible exiting with false...' )
                return False
        elif isinstance( other, list ):
            result = True

            for item in other:
                result = self.isCompatible( item )

                if not result:
                    break

            return result
        else:
            raise ValueError( 'RPNMeasurement or dict expected' )

    def getValue( self ):
        return self.value

    def setValue( self, value ):
        self.value = value

    def getUnits( self ):
        return self.units

    def setUnits( self, units ):
        self.units = RPNUnits( units )

    def getUnitString( self ):
        return self.units.getUnitString( )

    def getUnitName( self ):
        if self.unitName:
            return self.unitName

        unitString = self.getUnitString( )

        if unitString in g.unitOperators:
            return g.unitOperators[ unitString ].representation
        else:
            return unitString

    def getPluralUnitName( self ):
        if self.pluralUnitName:
            return self.pluralUnitName

        unitString = self.getUnitString( )

        if unitString in g.unitOperators:
            return g.unitOperators[ unitString ].plural
        else:
            return unitString

    def getUnitTypes( self ):
        types = RPNUnits( )

        for unit in self.units:
            if unit == '1':
                continue

            if unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            if unitType in types:
                types[ unitType ] += self.units[ unit ]
            elif self.units[ unit ] != 0:
                types[ unitType ] = self.units[ unit ]

        return types

    def getDimensions( self ):
        return self.units.getDimensions( )

    def doDimensionsCancel( self ):
        return self.units.doDimensionsCancel( )

    def convertToBaseUnits( self ):
        debugPrint( 'convertToBaseUnits:', self.getValue( ), self.getUnits( ) )

        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        value = self.value
        units = RPNUnits( )

        debugPrint( 'value', value )

        for unit in self.units:
            newUnits = g.basicUnitTypes[ getUnitType( unit ) ].primitiveUnit

            debugPrint( 'unit', unit, 'newUnits', newUnits )

            if unit != newUnits:
                if ( unit, newUnits ) in g.unitConversionMatrix:
                    value = fmul( value, power( mpf( g.unitConversionMatrix[ ( unit, newUnits ) ] ), self.units[ unit ] ) )
                elif ( unit, newUnits ) in specialUnitConversionMatrix:
                    value = power( specialUnitConversionMatrix[ ( unit, newUnits ) ]( value ), self.units[ unit ] )
                else:
                    if unit == '1' and newUnits == '_null_unit':
                        reduced = RPNMeasurement( value, units )
                        debugPrint( 'convertToBaseUnits 2:', reduced.getValue( ), reduced.getUnits( ) )
                        return reduced
                    else:
                        raise ValueError( 'cannot find conversion for ' + unit + ' and ' + newUnits )

            newUnits = RPNUnits( newUnits )

            for newUnit in newUnits:
                newUnits[ newUnit ] *= self.units[ unit ]

            units.update( newUnits )

            debugPrint( 'value', value )

        baseUnits = RPNMeasurement( value, units )
        debugPrint( 'convertToBaseUnits 3:', baseUnits.getValue( ), baseUnits.getUnits( ) )
        return baseUnits

    def convert( self, other ):
        if isinstance( other, RPNMeasurement ):
            return RPNMeasurement( self.convertValue( other ), other.getUnits( ) )
        elif isinstance( other, ( RPNUnits, dict, str ) ):
            measurement = RPNMeasurement( 1, other )
            return RPNMeasurement( self.convertValue( measurement ), measurement.getUnits( ) )
        elif isinstance( other, mpf ):
            measurement = RPNMeasurement( other, 'unity' )
            return RPNMeasurement( self.convertValue( measurement ), measurement.getUnits( ) )
        else:
            raise ValueError( 'convert doesn\'t know what to do with this argument' )

    def isLarger( self, other ):
        newValue = self.convertValue( other.getUnits( ) )
        return ( newValue > other.getValue( ) )

    def isNotLarger( self, other ):
        return not self.isLarger( other )

    def isSmaller( self, other ):
        newValue = self.convertValue( other.getUnits( ) )
        return ( newValue < other.getValue( ) )

    def isNotSmaller( self, other ):
        return not self.isSmaller( other )

    def isEqual( self, other ):
        newValue = self.convertValue( other.getUnits( ) )
        return ( newValue == other.getValue( ) )

    def isNotEqual( self, other ):
        return not self.isEqual( other )

    def isOfUnitType( self, unitType ):
        if self.isCompatible( RPNUnits( g.basicUnitTypes[ unitType ].baseUnit ) ):
            return True

        return self.getDimensions( ) == g.basicUnitTypes[ unitType ].dimensions

    def validateUnits( self, unitType ):
        if not self.isOfUnitType( unitType ):
            raise ValueError( unitType + ' unit expected' )

    def convertValue( self, other ):
        if not isinstance( other, ( RPNUnits, RPNMeasurement, str, list ) ):
            raise ValueError( 'convertValue must be called with an RPNUnits object, an RPNMeasurement object, a string or a list of RPNMeasurement' )

        if isinstance( other, ( str, RPNUnits ) ):
            other = RPNMeasurement( 1, other )

        if not self.isCompatible( other ):
            # We can try to convert incompatible units.
            return self.convertIncompatibleUnit( other )

        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        # handle list conversions like [ year, day, minute, hour ]
        if isinstance( other, list ):
            # a list of length one is treated the same as a single measurement
            if len( other ) == 1:
                return convertValue( other[ 0 ] )
            else:
                listToConvert = [ ]

                for i in other:
                    if isinstance( i, str ):
                        listToConvert.append( RPNMeasurement( 1, i ) )
                    elif isinstance( i, RPNMeasurement ):
                        listToConvert.append( i )
                    else:
                        raise ValueError( 'we\'ve got something else' )

                return self.convertUnitList( listToConvert )

        conversions = [ ]

        value = self.value    # This is what we'll return down below

        # TODO:  Should we just convert to base units regardless?  It would be safer...
        if other.doDimensionsCancel( ):
            other = other.convertToBaseUnits( )
            value = fdiv( value, other.value )

        # let's look for straightforward conversions
        units1 = self.getUnits( )
        units2 = other.getUnits( )

        unit1String = units1.getUnitString( )
        unit2String = units2.getUnitString( )

        debugPrint( 'unit1String: ', unit1String )
        debugPrint( 'unit2String: ', unit2String )

        if unit1String == unit2String:
            return value

        exponents = { }

        # look for a straight-up conversion
        if ( unit1String, unit2String ) in g.unitConversionMatrix:
            value = fmul( value, mpmathify( g.unitConversionMatrix[ ( unit1String, unit2String ) ] ) )
        elif ( unit1String, unit2String ) in specialUnitConversionMatrix:
            value = specialUnitConversionMatrix[ ( unit1String, unit2String ) ]( value )
        else:
            # otherwise, we need to figure out how to do the conversion
            conversionValue = mpmathify( 1 )

            # if that isn't found, then we need to do the hard work and break the units down
            newUnits1 = RPNUnits( units1 )
            newUnits2 = RPNUnits( units2 )

            debugPrint( 'newUnits1:', newUnits1 )
            debugPrint( 'newUnits2:', newUnits2 )

            debugPrint( )
            debugPrint( 'iterating through units to match for conversion:' )

            for unit1 in newUnits1:
                foundConversion = False

                for unit2 in newUnits2:
                    debugPrint( 'units 1:', unit1, newUnits1[ unit1 ], getUnitType( unit1 ) )
                    debugPrint( 'units 2:', unit2, newUnits2[ unit2 ], getUnitType( unit2 ) )

                    if getUnitType( unit1 ) == getUnitType( unit2 ):
                        debugPrint( 'found a conversion:', unit1, unit2 )
                        conversions.append( ( unit1, unit2 ) )
                        exponents[ ( unit1, unit2 ) ] = units1[ unit1 ]
                        foundConversion = True
                        break

                skip = False

                if not foundConversion:
                    debugPrint( )
                    debugPrint( 'didn\'t find a conversion, try reducing' )
                    debugPrint( )
                    reduced = self.convertToBaseUnits( )

                    debugPrint( 'reduced:', self.units, 'becomes', reduced.units )

                    reducedOther = other.convertToBaseUnits( )

                    reduced.setValue( fdiv( reduced.getValue( ), reducedOther.getValue( ) ) )

                    debugPrint( 'reduced other:', other.units, 'becomes', reducedOther.units )

                    # check to see if reducing did anything and bail if it didn't... bail out
                    if ( reduced.units == self.units ) and ( reducedOther.units == other.units ):
                        debugPrint( 'reducing didn\'t help' )
                        break

                    return reduced.convertValue( reducedOther )

            debugPrint( )

            value = conversionValue

            # If we can't convert, then let's twiddle the units around and see if we can get it another way.
            if not foundConversion:
                debugPrint( 'attempting to twiddle the units' )
                success, returnValue = self.twiddleUnits( units1, True, units2, False )

                if success:
                    return returnValue

                success, returnValue = self.twiddleUnits( units1, False, units2, True )

                if success:
                    return returnValue

                success, returnValue = self.twiddleUnits( units1, True, units2, True )

                if success:
                    return returnValue
                else:
                    raise ValueError( 'unable to convert ' + units1.getUnitString( ) + ' to ' + units2.getUnitString( ) )

            debugPrint( 'Iterating through conversions...' )

            value = self.getValue( )

            for conversion in conversions:
                if conversion[ 0 ] == conversion[ 1 ]:
                    continue  # no conversion needed

                debugPrint( '----> conversion', conversion )

                conversionIndex = tuple( conversion )

                if conversionIndex in g.unitConversionMatrix:
                    debugPrint( 'unit conversion:', g.unitConversionMatrix[ tuple( conversion ) ] )
                    debugPrint( 'exponents', exponents )

                    conversionValue = mpmathify( g.unitConversionMatrix[ conversionIndex ] )
                    conversionValue = power( conversionValue, exponents[ conversionIndex ] )
                    debugPrint( 'conversion: ', conversion, conversionValue )

                    debugPrint( 'value before', value )
                    value = fmul( value, conversionValue )
                    debugPrint( 'value after', value )
                else:
                    # we're ignoring the exponents, but this works for dBm<->milliwatt, etc.
                    baseUnit = g.basicUnitTypes[ getUnitType( conversion[ 0 ] ) ].baseUnit

                    conversion1 = ( conversion[ 0 ], baseUnit )
                    conversion2 = ( baseUnit, conversion[ 1 ] )

                    debugPrint( 'conversion1', conversion1 )
                    debugPrint( 'conversion2', conversion2 )

                    debugPrint( 'value0', value )

                    if conversion1 in g.unitConversionMatrix:
                        debugPrint( 'standard conversion 1' )
                        value = fmul( value, mpmathify( g.unitConversionMatrix[ conversion1 ] ) )
                    else:
                        debugPrint( 'special conversion 1' )
                        value = specialUnitConversionMatrix[ conversion1 ]( value )

                    debugPrint( 'value1', value )

                    if conversion2 in g.unitConversionMatrix:
                        debugPrint( 'standard conversion 2' )
                        value = fmul( value, mpmathify( g.unitConversionMatrix[ conversion2 ] ) )
                    else:
                        debugPrint( 'special conversion 2' )
                        value = specialUnitConversionMatrix[ conversion2 ]( value )

                    debugPrint( 'value2', value )

        debugPrint( 'convertValue final', value )
        return value

    def convertUnitList( self, other ):
        if not isinstance( other, list ):
            raise ValueError( 'convertUnitList expects a list argument' )

        result = [ ]

        nonIntegral = False

        for i in range( 1, len( other ) ):
            conversion = g.unitConversionMatrix[ ( other[ i - 1 ].getUnitString( ),
                                                   other[ i ].getUnitString( ) ) ]

            if conversion != floor( conversion ):
                nonIntegral = True

        if nonIntegral:
            source = self

            for count, measurement in enumerate( other ):
                with extradps( 2 ):
                    conversion = source.convertValue( measurement )

                    if count < len( other ) - 1:
                        result.append( RPNMeasurement( floor( conversion ), measurement.getUnits( ) ) )
                        source = RPNMeasurement( chop( frac( conversion ) ), measurement.getUnits( ) )
                    else:
                        result.append( RPNMeasurement( conversion, measurement.getUnits( ) ) )

            return result
        else:
            source = self.convert( other[ -2 ] )

            with extradps( 2 ):
                result.append( source.getModulo( other[ -2 ] ).convert( other[ -1 ] ) )

            source = source.subtract( result[ -1 ] )

            for i in range( len( other ) - 2, 0, -1 ):
                source = source.convert( other[ i - 1 ] )

                with extradps( 2 ):
                    result.append( source.getModulo( other[ i - 1 ] ).convert( other[ i ] ) )

                source = source.subtract( result[ -1 ] )

            result.append( source )

            return result[ : : -1 ]

    def convertIncompatibleUnit( self, other ):
        if isinstance( other, list ):
            otherUnit = '[ ' + ', '.join( [ unit.getUnitString( ) for unit in other ] ) + ' ]'
        else:
            otherUnit = other.getUnitString( )

        # last chance check, some units are reciprocals of each other
        unit = self.getUnitString( )

        try:
            baseUnit1 = g.basicUnitTypes[ getUnitType( unit ) ].baseUnit
            baseUnit2 = g.basicUnitTypes[ getUnitType( otherUnit ) ].baseUnit
        except:
            raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) + ' and ' + otherUnit )

        if ( baseUnit1, baseUnit2 ) in specialUnitConversionMatrix:
            debugPrint( '----------------------------->', self.getUnitString( ), baseUnit1, baseUnit2, otherUnit )
            result = RPNMeasurement( self )

            if ( unit != baseUnit1 ):
                result = self.convert( baseUnit1 )

            result = RPNMeasurement( specialUnitConversionMatrix[ ( baseUnit1, baseUnit2 ) ]( result.getValue( ) ), baseUnit2 )

            if ( baseUnit2 != otherUnit ):
                result = result.convert( otherUnit )

            return result

        raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) + ' and ' + otherUnit )

    def twiddleUnits( self, units1, twiddle1, units2, twiddle2 ):
        numeratorFound = False
        denominatorFound = False

        twiddleUnits1 = RPNUnits( units1 )
        twiddleUnits2 = RPNUnits( units2 )

        debugPrint( '0 twiddleUnits1', twiddleUnits1 )
        debugPrint( '0 twiddleUnits2', twiddleUnits2 )

        if twiddle1:
            for unit in twiddleUnits1:
                if twiddleUnits1[ unit ] > 0:
                    numeratorFound = True
                    continue

                if twiddleUnits1[ unit ] < 0:
                    denominatorFound = True
                    exponent = twiddleUnits1[ unit ] * -1

                    if unit in twiddleUnits2:
                        twiddleUnits2[ unit ] += exponent
                    else:
                        twiddleUnits2[ unit ] = exponent

                    twiddleUnits1[ unit ] = 0

            twiddleUnits1 = RPNUnits( twiddleUnits1 ).normalizeUnits( )
            twiddleUnits2 = RPNUnits( twiddleUnits2 ).normalizeUnits( )

            debugPrint( '1 twiddleUnits1', twiddleUnits1 )
            debugPrint( '1 twiddleUnits2', twiddleUnits2 )

        if twiddle2:
            for unit in twiddleUnits2:
                if twiddleUnits2[ unit ] > 0:
                    numeratorFound = True
                    continue

                if twiddleUnits2[ unit ] < 0:
                    denominatorFound = True

                    if unit in twiddleUnits1:
                        twiddleUnits1[ unit ] += twiddleUnits2[ unit ] * -1
                    else:
                        twiddleUnits1[ unit ] = twiddleUnits2[ unit ] * -1

                    twiddleUnits2[ unit ] = 0

            twiddleUnits1 = RPNUnits( twiddleUnits1 ).normalizeUnits( )
            twiddleUnits2 = RPNUnits( twiddleUnits2 ).normalizeUnits( )

            debugPrint( '2 twiddleUnits1', twiddleUnits1 )
            debugPrint( '2 twiddleUnits2', twiddleUnits2 )

        if denominatorFound and numeratorFound:
            try:
                value = RPNMeasurement( self.getValue( ), twiddleUnits1 ). convertValue( twiddleUnits2 )
                return True, RPNMeasurement( value, units2 )
            except:
                return False, None
                pass

        return False, None


# //******************************************************************************
# //
# //  convertUnits
# //
# //******************************************************************************

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
    elif isinstance( unit2, ( str, RPNUnits ) ):
        measurement = RPNMeasurement( 1, unit2 )
        return RPNMeasurement( unit1.convertValue( measurement ), unit2 )
    elif not isinstance( unit2, ( list, str, RPNUnits, RPNMeasurement ) ):
        raise ValueError( 'cannot convert non-measurements' )
    else:
        debugPrint( 'convertUnits' )
        debugPrint( 'unit1:', unit1.getUnitTypes( ) )
        debugPrint( 'unit2:', unit2.getUnitTypes( ) )
        debugPrint( 'value:', unit1.convertValue( unit2 ) )

        return RPNMeasurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                               unit2.getUnitName( ), unit2.getPluralUnitName( ) )


# //******************************************************************************
# //
# //  convertToDMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToDMS( n ):
    return convertUnits( n, [ 'degree', 'arcminute', 'arcsecond' ] )


# //******************************************************************************
# //
# //  estimate
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def estimate( measurement ):
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
    value = RPNMeasurement( measurement.convertValue( unit ), unit.getUnits( ) ).getValue( )

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


# //******************************************************************************
# //
# //  applyNumberValueToUnit
# //
# //  We have to treat constant units differently because they can become plain
# //  numbers.
# //
# //******************************************************************************

def applyNumberValueToUnit( number, term, constant ):
    if isinstance( term, RPNUnits ):
        value = RPNMeasurement( number, term )
        value = value.normalizeUnits( )
    elif constant:
        if ( g.constantOperators[ term ].unit ):
            value = RPNMeasurement( fmul( number, mpmathify( g.constantOperators[ term ].value ) ),
                                    g.constantOperators[ term ].unit )
        else:
            value = fmul( number, g.constantOperators[ term ].value )
    else:
        if g.unitOperators[ term ].unitType == 'constant':
            value = RPNMeasurement( number, term ).convertValue( RPNMeasurement( 1, { 'unity' : 1 } ) )
        else:
            value = RPNMeasurement( number, term, g.unitOperators[ term ].representation,
                                    g.unitOperators[ term ].plural )

    return value


# //******************************************************************************
# //
# //  getWhichUnitType
# //
# //******************************************************************************

def getWhichUnitType( measurement, unitTypes ):
    for unitType in unitTypes:
        if measurement.isOfUnitType( unitType ):
            return unitType

    return None


# //******************************************************************************
# //
# //  matchUnitTypes
# //
# //******************************************************************************

def matchUnitTypes( args, validUnitTypes ):
    result = { }

    for unitTypeList in validUnitTypes:
        unitTypes = list( unitTypeList )

        #print( 'unitTypes', unitTypes )

        if len( args ) != len( unitTypes ):
            raise ValueError( 'argument count mismatch in matchUnitTypes( )' )

        for arg in args:
            unitType = getWhichUnitType( arg, unitTypes )
            #print( 'found unit type', unitType )

            if unitType:
                #print( 'setting unitType', unitType )
                result[ unitType ] = arg
            else:
                result = { }
                #print( 'breaking...' )
                #print( )
                break

            unitTypes.remove( unitType )
        else:
            return result

    #print( 'first loop completed' )
    return None


# //******************************************************************************
# //
# //  getDimensions
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getDimensions( n ):
    if isinstance( n, RPNMeasurement ):
        return n.getDimensions( )
    else:
        return n


# //******************************************************************************
# //
# //  convertToBaseUnits
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToBaseUnits( n ):
    if isinstance( n, RPNMeasurement ):
        return n.convertToBaseUnits( )
    else:
        return n

