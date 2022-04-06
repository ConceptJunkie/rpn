#!/usr/bin/env python

#******************************************************************************
#
#  rpnMeasurementClass.py
#
#  rpnChilada measurement class
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import chop, extradps, fadd, fdiv, floor, fmod, fmul, frac, fsub, log10, \
                   mpf, mpmathify, power, root

from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnPersistence import loadUnitConversionMatrix, loadUnitData
from rpn.units.rpnUnitClasses import getUnitType, RPNUnits
from rpn.units.rpnUnitTypes import basicUnitTypes
from rpn.util.rpnUtils import getPowerSet

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  specialUnitConversionMatrix
#
#  This is for units that can't be converted with a simple multiplication
#  factor.
#
#  Plus, I'm not going to do the transitive thing here, so it's necessary
#  to explicitly state the conversions for all permutations.  That bugs me.
#
#  I would have included this table in makeUnits.py, but pickle doesn't
#  work on lambdas, which is, to me, very non-Pythonic.   I could also
#  save the expressions as strings and use eval, but that seems very
#  non-Pythonic, too.
#
#  ( first unit, second unit, conversion function )
#
#  For temperature conversions, see
#  https://en.wikipedia.org/wiki/Conversion_of_units_of_temperature.
#
#******************************************************************************

specialUnitConversionMatrix = {
    # pylint: disable=line-too-long
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


#******************************************************************************
#
#  class RPNMeasurement
#
#******************************************************************************

class RPNMeasurement( ):
    '''This class represents a measurement, which includes a numerical value
    and an RPNUnits instance.'''
    value = mpf( )
    units = RPNUnits( )

    def __init__( self, value, units = RPNUnits( ) ):
        if isinstance( value, ( str, int ) ):
            self.value = mpmathify( value )
            self.units = RPNUnits( units )
        elif isinstance( value, RPNMeasurement ):
            self.value = value.value
            self.units = RPNUnits( value.units )
        else:
            self.value = value
            self.units = RPNUnits( units )

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
    #    return 'RPNMeasurement(\'' + str( self.value ) + ' ' + \
    #           ( '{}' if self.units is None else '\'' + self.units.getUnitString( ) + '\'' )

    #def __str__( self ):
    #    return repr( self )

    def increment( self, unit, amount = 1 ):
        self.units[ unit ] += amount

    def decrement( self, unit, amount = 1 ):
        self.increment( unit, -amount )

    def add( self, other ):
        if isinstance( other, RPNMeasurement ):
            if self.units == other.units:
                return RPNMeasurement( fadd( self.value, other.value ), self.units )

            return RPNMeasurement( fadd( self.value, other.convertValue( self ) ), self.units )

        return RPNMeasurement( fadd( self.value, other ), self.units )

    def subtract( self, other ):
        if isinstance( other, RPNMeasurement ):
            if self.units == other.units:
                return RPNMeasurement( fsub( self.value, other.value ), self.units )

            return RPNMeasurement( fsub( self.value, other.convertValue( self ) ), self.units )

        return RPNMeasurement( fsub( self.value, other ), self.units )

    def multiply( self, other ):
        if isinstance( other, RPNMeasurement ):
            factor, newUnits = self.units.combineUnits( other.units )
            newUnits = RPNMeasurement( 1, newUnits ).simplifyUnits( ).units
            return RPNMeasurement( fmul( fmul( self.value, other.value ), factor ), newUnits ).normalizeUnits( )

        return RPNMeasurement( fmul( self.value, other ), self.units ).normalizeUnits( )

    def divide( self, other ):
        if isinstance( other, RPNMeasurement ):
            factor, newUnits = self.units.combineUnits( other.units.inverted( ) )
            newUnits = RPNMeasurement( 1, newUnits ).simplifyUnits( ).units

            return RPNMeasurement( fmul( fdiv( self.value, other.value ), factor ), newUnits ).normalizeUnits( )

        return RPNMeasurement( fdiv( self.value, other ), self.units ).normalizeUnits( )

    def getModulo( self, other ):
        if isinstance( other, RPNMeasurement ):
            measurement = RPNMeasurement( self ).convert( other.units )
            measurement.value = fmod( measurement.value, other.value )

            return measurement.normalizeUnits( )

        return RPNMeasurement( fmod( self.value, other ), self.units ).normalizeUnits( )

    def exponentiate( self, exponent ):
        if floor( exponent ) != exponent:
            raise ValueError( 'cannot raise a measurement to a non-integral power' )

        exponent = int( exponent )
        newValue = power( self.value, exponent )

        for unit in self.units:
            self.units[ unit ] *= exponent

        return RPNMeasurement( newValue, self.units )

    def getRoot( self, operand ):
        if floor( operand ) != operand:
            raise ValueError( 'cannot take a fractional root of a measurement' )

        newUnits = RPNUnits( self.units )

        for unit, exponent in newUnits.items( ):
            if fmod( exponent, operand ) != 0:
                if operand == 2:
                    name = 'square'
                elif operand == 3:
                    name = 'cube'
                else:
                    # getOrdinalName( operand )
                    name = str( int( operand ) ) + 'th'

                baseUnits = self.convertToPrimitiveUnits( )

                if baseUnits != self:
                    return baseUnits.getRoot( operand )

                raise ValueError( 'cannot take the ' + name + ' root of this measurement: ', self.units )

            newUnits[ unit ] /= operand

        value = root( self.value, operand )

        return RPNMeasurement( value, newUnits ).normalizeUnits( )

    def getInverted( self, invertValue=True ):
        units = self.units

        newUnits = RPNUnits( )

        for unit in units:
            newUnits[ unit ] = -units[ unit ]

        if invertValue:
            return RPNMeasurement( fdiv( 1, self.value ), newUnits )

        return RPNMeasurement( self.value, newUnits )

    def normalizeUnits( self ):
        units = self.units.normalizeUnits( )

        debugPrint( )
        debugPrint( 'normalize', units )

        if units == RPNUnits( ):
            return self.value

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

        for nUnit in numerator:
            for i in range( min( numerator[ nUnit ], 3 ) ):
                nElements.append( nUnit )

        dElements = [ ]

        for dUnit in denominator:
            for i in range( min( denominator[ dUnit ], 3 ) ):
                dElements.append( dUnit )

        debugPrint( 'nOriginalElements', nOriginalElements )
        debugPrint( 'nElements', nElements )

        debugPrint( 'dOriginalElements', dOriginalElements )
        debugPrint( 'dElements', dElements )

        matchFound = True   # technically not true yet, but it gets us into the loop

        conversionsNeeded = [ ]

        while matchFound:
            matchFound = False

            for nSubset in getPowerSet( nElements ):
                for dSubset in getPowerSet( dElements ):
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

                        for nUnit in nSubset:
                            baseUnit = g.basicUnitTypes[ getUnitType( nUnit ) ].baseUnit

                            if nUnit != baseUnit:
                                debugPrint( 'conversion added:', nUnit, baseUnit )
                                conversionsNeeded.append( ( nUnit, baseUnit ) )

                            newNSubset.append( baseUnit )

                        for dUnit in dSubset:
                            baseUnit = g.basicUnitTypes[ getUnitType( dUnit ) ].baseUnit

                            if dUnit != baseUnit:
                                debugPrint( 'conversion added:', dUnit, baseUnit )
                                conversionsNeeded.append( ( dUnit, baseUnit ) )

                            newDSubset.append( baseUnit )

                        # This maybe isn't quite what we want.
                        debugPrint( 'conversions added', '*'.join( sorted( newNSubset ) ),
                                    '*'.join( sorted( newDSubset ) ) )
                        conversionsNeeded.append( ( '*'.join( sorted( newNSubset ) ),
                                                    '*'.join( sorted( newDSubset ) ) ) )
                        matchFound = True

                        for nUnit in nSubset:
                            #print( 'nOriginalElements', nOriginalElements, 'n', nUnit )
                            nOriginalElements.remove( nUnit )
                            changed = True

                        for dUnit in dSubset:
                            #print( 'dOriginalElements', dOriginalElements, 'd', dUnit )
                            dOriginalElements.remove( dUnit )
                            changed = True

                        break

                if matchFound:
                    break

            if matchFound:
                break

        debugPrint( 'final nElements', nOriginalElements )
        debugPrint( 'final dElements', dOriginalElements )

        # convert the value based on all the conversions we queued up
        convertedValue = self.value

        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        for i in conversionsNeeded:
            if i in g.unitConversionMatrix:
                convertedValue = fmul( convertedValue, g.unitConversionMatrix[ i ] )
            else:
                convertedValue = fmul( convertedValue, RPNMeasurement( 1, i[ 0 ] ).convertValue( i[ 1 ] ) )

        # build up the resulting units
        units = RPNUnits( '*'.join( nOriginalElements ) )
        denominator = RPNUnits( '*'.join( dOriginalElements ) )

        for dUnit in denominator:
            units[ dUnit ] += denominator[ dUnit ] * -1

        debugPrint( 'normalizeUnits final units', units )
        debugPrint( )

        if units and units != RPNUnits( ):
            result = RPNMeasurement( convertedValue, units )

            if changed:
                return result.normalizeUnits( )

            return result

        return convertedValue

    def update( self, units ):
        for i in self.units:
            del self.units[ i ]

        if not isinstance( units, dict ):
            raise ValueError( 'dict expected' )

        self.units.update( units )

    def isCompatible( self, other ):
        if isinstance( other, str ):
            return self.isCompatible( RPNMeasurement( 1, other ) )

        if isinstance( other, RPNUnits ):
            return self.getUnitTypes( ) == other.getUnitTypes( )

        if isinstance( other, RPNMeasurement ):
            debugPrint( 'isCompatible -----------------------' )
            debugPrint( 'units: ', self.units, other.units )
            debugPrint( 'types: ', self.getUnitTypes( ), other.getUnitTypes( ) )
            debugPrint( 'dimensions: ', self.getDimensions( ), other.getDimensions( ) )
            debugPrint( )

            if self.getUnitTypes( ) == other.getUnitTypes( ):
                return True

            if self.getDimensions( ) == other.getDimensions( ):
                return True

            debugPrint( 'RPNMeasurement.isCompatible exiting with false...' )
            return False

        if isinstance( other, list ):
            result = True

            for item in other:
                result = self.isCompatible( item )

                if not result:
                    break

            return result

        raise ValueError( 'RPNMeasurement or dict expected' )

    def getUnitName( self ):
        return self.units.getUnitString( )

    def getPluralUnitName( self ):
        unitString = self.getUnitName( )

        if unitString in g.unitOperators:
            return g.unitOperators[ unitString ].plural

        return unitString

    def getUnitTypes( self ):
        types = RPNUnits( )

        for unit in self.units:
            if unit == '1':
                continue

            if unit not in g.unitOperators:
                raise ValueError( f'1 undefined unit type \'{ unit }\'' )

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

    def convertToPrimitiveUnits( self ):
        debugPrint( )
        debugPrint( 'convertToPrimitiveUnits:', self.value, self.units )

        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        value = self.value
        units = RPNUnits( )

        debugPrint( 'value', value )

        for unit in self.units:

            if self.units[ unit ] == 0:
                continue

            newUnits = g.basicUnitTypes[ getUnitType( unit ) ].primitiveUnit

            debugPrint( 'unit', unit, 'newUnits', newUnits )

            if unit != newUnits:
                debugPrint( 'unit vs newUnits:', unit, newUnits )

                if ( unit, newUnits ) in g.unitConversionMatrix:
                    value = fmul( value, power( mpf( g.unitConversionMatrix[ ( unit, newUnits ) ] ),
                                                self.units[ unit ] ) )
                elif ( unit, newUnits ) in specialUnitConversionMatrix:
                    value = power( specialUnitConversionMatrix[ ( unit, newUnits ) ]( value ), self.units[ unit ] )
                else:
                    if unit == '1' and newUnits == '_null_unit':
                        reduced = RPNMeasurement( value, units )
                        debugPrint( 'convertToPrimitiveUnits 2:', reduced.value, reduced.units )
                        return reduced

                    raise ValueError( 'cannot find a conversion for ' + unit + ' and ' + newUnits )

            newUnits = RPNUnits( newUnits )

            for newUnit in newUnits:
                newUnits[ newUnit ] *= self.units[ unit ]

            units.update( newUnits )

            debugPrint( 'value', value )

        baseUnits = RPNMeasurement( value, units )
        debugPrint( 'convertToPrimitiveUnits 3:', baseUnits.value, baseUnits.units )
        debugPrint( )
        return baseUnits

    def simplifyUnits( self ):
        '''
        This is a subset of convertToPrimitiveUnits' functionality.  It calls
        convertToPrimitiveUnits( ), but if the value changes (i.e., there's a conversion
        factor needed, then it will ignore the conversion.   The reason we are doing
        this is because we want joules/watt to convert to seconds, but we don't want
        miles/hour to convert to meters/second.
        '''
        originalValue = self.value

        # Try converting to base units, but only keep it if there's no conversion factor.
        baseUnits = self.convertToPrimitiveUnits( )

        if baseUnits.value == originalValue:
            result = baseUnits
        else:
            result = self

        # Let's see if we have a base unit type, and use it if we do, since that's a great
        # simplification.  This way you can multiply watts by seconds and get joules.  However,
        # again we don't want a conversion factor.  e.g., meters^3 should not be converted to liters.
        for _, unitTypeInfo in basicUnitTypes.items( ):
            if result.getUnitName( ) == unitTypeInfo.primitiveUnit:
                test = RPNMeasurement( result )

                if test.convert( unitTypeInfo.baseUnit ).value == result.value:
                    result = RPNMeasurement( originalValue, unitTypeInfo.baseUnit )

                break

        return result

    def convert( self, other ):
        if isinstance( other, RPNMeasurement ):
            return RPNMeasurement( self.convertValue( other ), other.units )

        if isinstance( other, ( RPNUnits, dict, str ) ):
            measurement = RPNMeasurement( 1, other )
            return RPNMeasurement( self.convertValue( measurement ), measurement.units )

        if isinstance( other, mpf ):
            measurement = RPNMeasurement( other, 'unity' )
            return RPNMeasurement( self.convertValue( measurement ), measurement.units )

        raise ValueError( 'convert doesn\'t know what to do with this argument' )

    def isLarger( self, other ):
        newValue = self.convertValue( other.units )
        return newValue > other.value

    def isNotLarger( self, other ):
        return not self.isLarger( other )

    def isSmaller( self, other ):
        newValue = self.convertValue( other.units )
        return newValue < other.value

    def isNotSmaller( self, other ):
        return not self.isSmaller( other )

    def isEqual( self, other ):
        newValue = self.convertValue( other.units )
        return newValue == other.value

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
            raise ValueError( 'convertValue must be called with an RPNUnits object, '
                              'an RPNMeasurement object, a string or a list of RPNMeasurement' )

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
                return self.convertValue( other[ 0 ] )
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

        # let's look for straightforward conversions
        units1 = self.units
        units2 = other.units

        unit1String = units1.getUnitString( )
        unit2String = units2.getUnitString( )

        if unit1String == unit2String:
            return value

        exponents = { }

        # look for a straight-up conversion
        if ( unit1String, unit2String ) in g.unitConversionMatrix:
            value = fmul( value, mpmathify( g.unitConversionMatrix[ ( unit1String, unit2String ) ] ) )
        elif ( unit1String, unit2String ) in specialUnitConversionMatrix:
            value = specialUnitConversionMatrix[ ( unit1String, unit2String ) ]( value )
        else:
            if other.doDimensionsCancel( ):
                other = other.convertToPrimitiveUnits( )
                units2 = other.units
                value = fdiv( value, other.value )

            # otherwise, we need to figure out how to do the conversion
            conversionValue = value

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

                if not foundConversion:
                    debugPrint( )
                    debugPrint( 'didn\'t find a conversion, try reducing' )
                    debugPrint( )
                    reduced = self.convertToPrimitiveUnits( )

                    debugPrint( 'reduced:', self.units, 'becomes', reduced.units )

                    reducedOther = other.convertToPrimitiveUnits( )

                    reduced.value = fdiv( reduced.value, reducedOther.value )

                    debugPrint( 'reduced other:', other.units, 'becomes', reducedOther.units )

                    # check to see if reducing did anything and bail if it didn't... bail out
                    if ( reduced.units == self.units ) and ( reducedOther.units == other.units ):
                        debugPrint( 'reducing didn\'t help' )
                        break

                    return reduced.convertValue( reducedOther )

            debugPrint( )

            value = conversionValue

            debugPrint( 'Iterating through conversions...' )

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
            conversion = g.unitConversionMatrix[ ( other[ i - 1 ].getUnitName( ), other[ i ].getUnitName( ) ) ]

            if conversion != floor( conversion ):
                nonIntegral = True

        if nonIntegral:
            source = self

            for count, measurement in enumerate( other ):
                with extradps( 2 ):
                    conversion = source.convertValue( measurement )

                    if count < len( other ) - 1:
                        result.append( RPNMeasurement( floor( conversion ), measurement.units ) )
                        source = RPNMeasurement( chop( frac( conversion ) ), measurement.units )
                    else:
                        result.append( RPNMeasurement( conversion, measurement.units ) )

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
            otherUnit = other.getUnitName( )

        # last chance check, some units are reciprocals of each other
        unit = self.getUnitName( )

        try:
            baseUnit1 = g.basicUnitTypes[ getUnitType( unit ) ].baseUnit
            baseUnit2 = g.basicUnitTypes[ getUnitType( otherUnit ) ].baseUnit
        except ValueError as e:
            inverted = self.getInverted( )

            if inverted.isCompatible( other ):
                return inverted.convert( other )
            else:
                raise ValueError( 'incompatible units cannot be converted: ' +
                                  self.getUnitName( ) + ' and ' + otherUnit ) from e

        if ( baseUnit1, baseUnit2 ) in specialUnitConversionMatrix:
            # debugPrint( '----->', self.getUnitName( ), baseUnit1, baseUnit2, otherUnit )
            result = RPNMeasurement( self )

            if unit != baseUnit1:
                result = self.convert( baseUnit1 )

            result = RPNMeasurement( specialUnitConversionMatrix[ ( baseUnit1, baseUnit2 ) ]( result.value ),
                                     baseUnit2 )

            if baseUnit2 != otherUnit:
                result = result.convert( otherUnit )

            return result

        raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitName( ) + ' and ' + otherUnit )
