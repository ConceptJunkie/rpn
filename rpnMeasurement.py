#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnMeasurement.py
# //
# //  RPN command-line calculator, Measurements class and unit conversion
# //  copyright (c) 2017, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import chop, extradps, fadd, fdiv, floor, fmul, frac, fsub, mpf, \
                   mpmathify, nstr, power

from rpnGenerator import RPNGenerator
from rpnPersistence import loadUnitData, loadUnitConversionMatrix
from rpnUnitClasses import RPNUnits
from rpnUtils import debugPrint, oneArgFunctionEvaluator

import rpnGlobals as g


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
# //******************************************************************************

specialUnitConversionMatrix = {
    ( 'celsius', 'delisle' )                    : lambda c: fmul( fsub( 100, c ), fdiv( 3, 2 ) ),
    ( 'celsius', 'degrees_newton' )             : lambda c: fmul( c, fdiv( 33, 100 ) ),
    ( 'celsius', 'fahrenheit' )                 : lambda c: fadd( fmul( c, fdiv( 9, 5 ) ), 32 ),
    ( 'celsius', 'kelvin' )                     : lambda c: fadd( c, mpf( '273.15' ) ),
    ( 'celsius', 'rankine' )                    : lambda c: fmul( fadd( c, mpf( '273.15' ) ), fdiv( 9, 5 ) ),
    ( 'celsius', 'reaumur' )                    : lambda c: fmul( c, fdiv( 4, 5 ) ),
    ( 'celsius', 'romer' )                      : lambda c: fadd( fmul( c, fdiv( 21, 40 ) ), mpf( '7.5' ) ),

    ( 'delisle', 'celsius' )                    : lambda d: fsub( 100, fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle', 'degrees_newton' )             : lambda d: fsub( 33, fmul( d, fdiv( 11, 50 ) ) ),
    ( 'delisle', 'fahrenheit' )                 : lambda d: fsub( 212, fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle', 'kelvin' )                     : lambda d: fsub( mpf( '373.15' ), fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle', 'rankine' )                    : lambda d: fsub( mpf( '671.67' ), fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle', 'reaumur' )                    : lambda d: fsub( 80, fmul( d, fdiv( 8, 15 ) ) ),
    ( 'delisle', 'romer' )                      : lambda d: fsub( 60, fmul( d, fdiv( 7, 20 ) ) ),

    ( 'degrees_newton', 'celsius' )             : lambda n: fmul( n, fdiv( 100, 33 ) ),
    ( 'degrees_newton', 'delisle' )             : lambda n: fmul( fsub( 33, n ), fdiv( 50, 11 ) ),
    ( 'degrees_newton', 'fahrenheit' )          : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), 32 ),
    ( 'degrees_newton', 'kelvin' )              : lambda n: fadd( fmul( n, fdiv( 100, 33 ) ), mpf( '273.15' ) ),
    ( 'degrees_newton', 'rankine' )             : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), mpf( '491.67' ) ),
    ( 'degrees_newton', 'reaumur' )             : lambda n: fmul( n, fdiv( 80, 33 ) ),
    ( 'degrees_newton', 'romer' )               : lambda n: fadd( fmul( n, fdiv( 35, 22 ) ), mpf( 7.5 ) ),

    ( 'fahrenheit', 'celsius' )                 : lambda f: fmul( fsub( f, 32 ), fdiv( 5, 9 ) ),
    ( 'fahrenheit', 'degrees_newton' )          : lambda f: fmul( fsub( f, 32 ), fdiv( 11, 60 ) ),
    ( 'fahrenheit', 'delisle' )                 : lambda f: fmul( fsub( 212, f ), fdiv( 5, 6 ) ),
    ( 'fahrenheit', 'kelvin' )                  : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 5, 9 ) ), mpf( '273.15' ) ),
    ( 'fahrenheit', 'rankine' )                 : lambda f: fadd( f, mpf( '459.67' ) ),
    ( 'fahrenheit', 'reaumur' )                 : lambda f: fmul( fsub( f, 32 ), fdiv( 4, 9 ) ),
    ( 'fahrenheit', 'romer' )                   : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'kelvin', 'celsius' )                     : lambda k: fsub( k, mpf( '273.15' ) ),
    ( 'kelvin', 'degrees_newton' )              : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 33, 100 ) ),
    ( 'kelvin', 'delisle' )                     : lambda k: fmul( fsub( mpf( '373.15' ), k ), fdiv( 3, 2 ) ),
    ( 'kelvin', 'fahrenheit' )                  : lambda k: fsub( fmul( k, fdiv( 9, 5 ) ), mpf( '459.67' ) ),
    ( 'kelvin', 'rankine' )                     : lambda k: fmul( k, fdiv( 9, 5 ) ),
    ( 'kelvin', 'reaumur' )                     : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 4, 5 ) ),
    ( 'kelvin', 'romer' )                       : lambda k: fadd( fmul( fsub( k, mpf( '273.15' ) ), fdiv( 21, 40 ) ), mpf( 7.5 ) ),

    ( 'rankine', 'celsius' )                    : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 5, 9 ) ),
    ( 'rankine', 'degrees_newton' )             : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 11, 60 ) ),
    ( 'rankine', 'delisle' )                    : lambda r: fmul( fsub( mpf( '671.67' ), r ), fdiv( 5, 6 ) ),
    ( 'rankine', 'fahrenheit' )                 : lambda r: fsub( r, mpf( '459.67' ) ),
    ( 'rankine', 'kelvin' )                     : lambda r: fmul( r, fdiv( 5, 9 ) ),
    ( 'rankine', 'reaumur' )                    : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 4, 9 ) ),
    ( 'rankine', 'romer' )                      : lambda r: fadd( fmul( fsub( r, mpf( '491.67' ) ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'reaumur', 'celsius' )                    : lambda re: fmul( re, fdiv( 5, 4 ) ),
    ( 'reaumur', 'degrees_newton' )             : lambda re: fmul( re, fdiv( 33, 80 ) ),
    ( 'reaumur', 'delisle' )                    : lambda re: fmul( fsub( 80, re ), fdiv( 15, 8 ) ),
    ( 'reaumur', 'fahrenheit' )                 : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), 32 ),
    ( 'reaumur', 'kelvin' )                     : lambda re: fadd( fmul( re, fdiv( 5, 4 ) ), mpf( '273.15' ) ),
    ( 'reaumur', 'rankine' )                    : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), mpf( '491.67' ) ),
    ( 'reaumur', 'romer' )                      : lambda re: fadd( fmul( re, fdiv( 21, 32 ) ), mpf( 7.5 ) ),

    ( 'romer', 'celsius' )                      : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ),
    ( 'romer', 'degrees_newton' )               : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 22, 35 ) ),
    ( 'romer', 'delisle' )                      : lambda ro: fmul( fsub( 60, ro ), fdiv( 20, 7 ) ),
    ( 'romer', 'fahrenheit' )                   : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), 32 ),
    ( 'romer', 'kelvin' )                       : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ), mpf( '273.15' ) ),
    ( 'romer', 'rankine' )                      : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), mpf( '491.67' ) ),
    ( 'romer', 'reaumur' )                      : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 32, 21 ) ),

    ( 'dBm', 'watt' )                           : lambda dBm: power( 10, fdiv( fsub( dBm, 30 ), 10 ) ),
    ( 'watt', 'dBm' )                           : lambda W: fmul( log10( fmul( W, 1000 ) ), 10 ),
}


# //******************************************************************************
# //
# //  combineUnits
# //
# //  Combine units2 into units1
# //
# //******************************************************************************

def combineUnits( units1, units2 ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    newUnits = RPNUnits( units1 )

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


# //******************************************************************************
# //
# //  getUnitType
# //
# //******************************************************************************

def getUnitType( unit ):
    if unit in g.basicUnitTypes:
        return unit

    if unit in g.operatorAliases:
        unit = g.operatorAliases[ unit ]

    if unit in g.unitOperators:
        return g.unitOperators[ unit ].unitType
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


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
        if not g.unitOperators:
            loadUnitData( )

        #print( '__init__', value, units, unitName, pluralUnitName )

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
        return not __eq__( self, other )

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

            factor, newUnits = combineUnits( self.getUnits( ), other.getUnits( ) )

            self = RPNMeasurement( fmul( newValue, factor ), newUnits )
        else:
            newValue = fmul( self.value, other )

            self = RPNMeasurement( newValue, self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

        return self.normalizeUnits( )

    def divide( self, other ):
        if isinstance( other, RPNMeasurement ):
            newValue = fdiv( self.value, other.value )

            factor, newUnits = combineUnits( self.getUnits( ), other.getUnits( ).inverted( ) )

            self = RPNMeasurement( fmul( newValue, factor ), newUnits )
        else:
            newValue = fdiv( self.value, other )

            self = RPNMeasurement( newValue, self.getUnits( ),
                                   self.getUnitName( ), self.getPluralUnitName( ) )

        return self.normalizeUnits( )

    def exponentiate( self, exponent ):
        if ( floor( exponent ) != exponent ):
            raise ValueError( 'cannot raise a measurement to a non-integral power' )

        newValue = power( self.value, exponent )

        for unit in self.units:
            self.units[ unit ] *= exponent

        self = RPNMeasurement( newValue, self.units )

        return self

    def invert( self ):
        units = self.getUnits( )

        newUnits = RPNUnits( )

        for unit in units:
            newUnits[ unit ] = -units[ unit ]

        return RPNMeasurement( self.value, newUnits )

    def normalizeUnits( self ):
        units = self.getUnits( )

        newUnits = RPNUnits( )

        for unit in units:
            if units[ unit ] != 0 and unit != '_null_unit':
                newUnits[ unit ] = units[ unit ]

        return RPNMeasurement( self.value, newUnits, self.getUnitName( ), self.getPluralUnitName( ) )

    def update( self, units ):
        for i in self.units:
            del self.units[ i ]

        if not isinstance( units, dict ):
            raise ValueError( 'dict expected' )

        self.unitName = None
        self.pluralUnitName = None

        self.units.update( units )

    def isCompatible( self, other ):
        if isinstance( other, RPNUnits ):
            return self.getUnitTypes( ) == other.getUnitTypes( )
        elif isinstance( other, dict ):
            return self.getUnitTypes( ) == other
        elif isinstance( other, list ):
            result = True

            for item in other:
                result = self.isCompatible( item )

                if not result:
                    break

            return result
        elif isinstance( other, RPNMeasurement ):
            debugPrint( 'units: ', self.units, other.units )
            debugPrint( 'types: ', self.getUnitTypes( ), other.getUnitTypes( ) )
            debugPrint( 'dimensions: ', self.getDimensions( ), other.getDimensions( ) )

            if self.getUnitTypes( ) == other.getUnitTypes( ):
                return True
            elif self.getDimensions( ) == other.getDimensions( ):
                return True
            else:
                debugPrint( 'RPNMeasurement.isCompatible exiting with false...' )
                return False
        else:
            raise ValueError( 'RPNMeasurement or dict expected' )

    def isEquivalent( self, other ):
        if isinstance( other, list ):
            result = True

            for item in other:
                result = self.isEquivalent( item )

                if not result:
                    break

            return result
        elif isinstance( other, RPNMeasurement ):
            return self.getUnits( ) == other.getUnits( )
        else:
            raise ValueError( 'RPNMeasurement or dict expected' )

    def getValue( self ):
        return self.value

    def getUnits( self ):
        return self.units

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

    def getReduced( self ):
        debugPrint( 'getReduced 1:', self, [ ( i, self.units[ i ] ) for i in self.units ] )
        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        value = self.value
        units = RPNUnits( )

        debugPrint( 'value', value )

        for unit in self.units:
            newUnit = g.basicUnitTypes[ getUnitType( unit ) ].baseUnit
            debugPrint( 'unit', unit, 'newUnit', newUnit )

            if unit != newUnit:
                value = fmul( value, power( mpf( g.unitConversionMatrix[ ( unit, newUnit ) ] ), self.units[ unit ] ) )

            units.update( RPNUnits( g.unitOperators[ newUnit ].representation + "^" + str( self.units[ unit ] ) ) )
            debugPrint( 'value', value )

        reduced = RPNMeasurement( value, units )
        debugPrint( 'getReduced 2:', reduced )
        return reduced

    def convert( self, other ):
        if isinstance( other, RPNMeasurement ):
            return RPNMeasurement( self.convertValue( other ), other.getUnits( ) )
        elif isinstance( other, ( RPNUnits, dict, str ) ):
            measurement = RPNMeasurement( 1, other )
            return RPNMeasurement( self.convertValue( measurement ), measurement.getUnits( ) )
        else:
            raise ValueError( 'convert doesn\'t know what to do with this argument' )

    def isLarger( self, other ):
        newValue = self.convert( other )
        return ( newValue.getValue( ) > other.getValue( ) )

    def isNotLarger( self, other ):
        return not self.isLarger( other )

    def isSmaller( self, other ):
        newValue = self.convert( other )
        return ( newValue.getValue( ) < other.getValue( ) )

    def isNotSmaller( self, other ):
        return not self.isSmaller( other )

    def isEqual( self, other ):
        newValue = self.convert( other )
        #print( newValue.getValue( ), other.getValue( ) )
        return ( newValue.getValue( ) == other.getValue( ) )

    def isNotEqual( self, other ):
        return not self.isEqual( other )

    def convertValue( self, other, tryReverse=True ):
        if self.isEquivalent( other ):
            return self.getValue( )

        if self.isCompatible( other ):
            conversions = [ ]

            if isinstance( other, list ):
                result = [ ]
                source = self

                for count, measurement in enumerate( other ):
                    with extradps( 1 ):
                        conversion = source.convertValue( measurement )

                    if count < len( other ) - 1:
                        result.append( RPNMeasurement( floor( conversion ), measurement.getUnits( ) ) )
                        source = RPNMeasurement( chop( frac( conversion ) ), measurement.getUnits( ) )
                    else:
                        result.append( RPNMeasurement( conversion, measurement.getUnits( ) ) )

                return result

            units1 = self.getUnits( )
            units2 = other.getUnits( )

            unit1String = units1.getUnitString( )
            unit2String = units2.getUnitString( )

            debugPrint( 'unit1String: ', unit1String )
            debugPrint( 'unit2String: ', unit2String )

            if unit1String == unit2String:
                return fmul( self.getValue( ), other.getValue( ) )

            if unit1String in g.operatorAliases:
                unit1String = g.operatorAliases[ unit1String ]

            if unit2String in g.operatorAliases:
                unit2String = g.operatorAliases[ unit2String ]

            exponents = { }

            if not g.unitConversionMatrix:
                loadUnitConversionMatrix( )

            # look for a straight-up conversion
            unit1NoStar = unit1String.replace( '*', '-' )
            unit2NoStar = unit2String.replace( '*', '-' )

            debugPrint( 'unit1NoStar: ', unit1NoStar )
            debugPrint( 'unit2NoStar: ', unit2NoStar )

            if ( unit1NoStar, unit2NoStar ) in g.unitConversionMatrix:
                value = fmul( self.value, mpmathify( g.unitConversionMatrix[ ( unit1NoStar, unit2NoStar ) ] ) )
            elif ( unit1NoStar, unit2NoStar ) in specialUnitConversionMatrix:
                value = specialUnitConversionMatrix[ ( unit1NoStar, unit2NoStar ) ]( self.value )
            else:
                # otherwise, we need to figure out how to do the conversion
                conversionValue = mpmathify( 1 )

                # if that isn't found, then we need to do the hard work and break the units down
                newUnits1 = RPNUnits( )

                for unit in units1:
                    newUnits1.update( RPNUnits( g.unitOperators[ unit ].representation + "^" +
                                                str( units1[ unit ] ) ) )

                newUnits2 = RPNUnits( )

                for unit in units2:
                    newUnits2.update( RPNUnits( g.unitOperators[ unit ].representation + "^" +
                                                str( units2[ unit ] ) ) )

                debugPrint( 'units1:', units1 )
                debugPrint( 'units2:', units2 )
                debugPrint( 'newUnits1:', newUnits1 )
                debugPrint( 'newUnits2:', newUnits2 )

                debugPrint( )
                debugPrint( 'iterating through units:' )

                for unit1 in newUnits1:
                    foundConversion = False

                    for unit2 in newUnits2:
                        debugPrint( 'units 1:', unit1, newUnits1[ unit1 ], getUnitType( unit1 ) )
                        debugPrint( 'units 2:', unit2, newUnits2[ unit2 ], getUnitType( unit2 ) )

                        if getUnitType( unit1 ) == getUnitType( unit2 ):
                            conversions.append( [ unit1, unit2 ] )
                            exponents[ ( unit1, unit2 ) ] = units1[ unit1 ]
                            foundConversion = True
                            break

                    if not foundConversion:
                        debugPrint( 'didn\'t find a conversion, try reducing' )
                        reduced = self.getReduced( )

                        debugPrint( 'reduced:', self.units, 'becomes', reduced.units )

                        reducedOther = other.getReduced( )

                        debugPrint( 'reduced other:', other.units, 'becomes', reducedOther.units )

                        # check to see if reducing did anything and bail if it didn't... bail out
                        if ( reduced.units == self.units ) and ( reducedOther.units == other.units ):
                            break

                        reduced = reduced.convertValue( reducedOther )
                        return RPNMeasurement( fdiv( reduced, reducedOther.value ), reducedOther.getUnits( ) ).getValue( )

                debugPrint( )

                value = conversionValue

                if not foundConversion:
                    # This is a cheat.  The conversion logic has flaws, but if it's possible to do the
                    # conversion in the opposite direction, then we can do that and return the reciprocal.
                    # This allows more conversions without fixing the underlying problems, which will
                    # require some redesign.
                    if tryReverse:
                        return fdiv( 1, other.convertValue( self, False ) )
                    else:
                        raise ValueError( 'unable to convert ' + self.getUnitString( ) +
                                          ' to ' + other.getUnitString( ) )

                for conversion in conversions:
                    if conversion[ 0 ] == conversion[ 1 ]:
                        continue  # no conversion needed

                    debugPrint( 'unit conversion:', g.unitConversionMatrix[ tuple( conversion ) ] )
                    debugPrint( 'exponents', exponents )

                    conversionValue = mpmathify( g.unitConversionMatrix[ tuple( conversion ) ] )
                    conversionValue = power( conversionValue, exponents[ tuple( conversion ) ] )
                    debugPrint( 'conversion: ', conversion, conversionValue )

                    value = fmul( value, conversionValue )

                value = fmul( self.value, value )

            return value
        else:
            if isinstance( other, list ):
                otherUnit = '[ ' + ', '.join( [ unit.getUnitString( ) for unit in other ] ) + ' ]'
            else:
                otherUnit = other.getUnitString( )

            raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) +
                              ' and ' + otherUnit )


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
    elif isinstance( unit2, str ):
        measurement = RPNMeasurement( 1, { unit2 : 1 } )
        return RPNMeasurement( unit1.convertValue( measurement ), unit2 )
    elif not isinstance( unit2, RPNMeasurement ):
        raise ValueError( 'cannot convert non-measurements' )
    else:
        debugPrint( 'convertUnits' )
        debugPrint( 'unit1:', unit1.getUnitTypes( ) )
        debugPrint( 'unit2:', unit2.getUnitTypes( ) )

        return RPNMeasurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                               unit2.getUnitName( ), unit2.getPluralUnitName( ) )


# //******************************************************************************
# //
# //  convertToDMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToDMS( n ):
    return convertUnits( n, [ RPNMeasurement( 1, { 'degree' : 1 } ),
                              RPNMeasurement( 1, { 'arcminute' : 1 } ),
                              RPNMeasurement( 1, { 'arcsecond' : 1 } ) ] )


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
# //  We have to treat constant units differently because they become plain
# //  numbers.
# //
# //******************************************************************************

def applyNumberValueToUnit( number, term ):
    if isinstance( term, RPNUnits ):
        value = RPNMeasurement( number, term )
    elif g.unitOperators[ term ].unitType == 'constant':
        value = RPNMeasurement( number, term ).convertValue( RPNMeasurement( 1, { 'unity' : 1 } ) )
    else:
        value = RPNMeasurement( number, term, g.unitOperators[ term ].representation,
                                g.unitOperators[ term ].plural )

    return value


# //******************************************************************************
# //
# //  checkUnits
# //
# //******************************************************************************

def checkUnits( measurement, unitType ):
    if measurement.isCompatible( RPNUnits( g.basicUnitTypes[ unitType ].baseUnit ) ):
        return True

    return measurement.isCompatible( RPNUnits( g.basicUnitTypes[ unitType ].dimensions ) )


# //******************************************************************************
# //
# //  validateUnits
# //
# //******************************************************************************

def validateUnits( measurement, unitType ):
    if not checkUnits( measurement, unitType ):
        raise ValueError( unitType + ' unit expected' )


# //******************************************************************************
# //
# //  getWhichUnitType
# //
# //******************************************************************************

def getWhichUnitType( measurement, unitTypes ):
    for unitType in unitTypes:
        if checkUnits( measurement, unitType ):
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
                break

            unitTypes.remove( unitType )
        else:
            return result

    #print( 'first loop completed' )
    return None

