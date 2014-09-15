#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnUtils
#//
#//  RPN command-line calculator utility functions
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import arrow
import builtins
import bz2
import contextlib
import math
import os
import pickle
import string
import textwrap

from mpmath import *

from rpnDeclarations import *
from rpnVersion import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  loadUnitConversionMatrix
#//
#//******************************************************************************

def loadUnitConversionMatrix( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitConversionMatrix = pickle.load( pickleFile )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit conversion matrix data.  Unit conversion will be unavailable.' )


#//******************************************************************************
#//
#//  removeUnderscores
#//
#//******************************************************************************

def removeUnderscores( source ):
    result = ''

    for c in source:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#//******************************************************************************
#//
#//  debugPrint
#//
#//******************************************************************************

def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


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

            #print( 'parseUnitString result:', result )
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

        return Measurement( fdiv( 1, value ), newUnits )


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
                    newUnit1String = g.compoundUnits[ unit1String ]
                else:
                    newUnit1String = unit1String

                if unit2String in g.compoundUnits:
                    newUnit2String = g.compoundUnits[ unit2String ]
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
                        return reduced.convertValue( other )

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
#//  downloadOEISSequence
#//
#//******************************************************************************

def downloadOEISSequence( id ):
    keywords = downloadOEISText( id, 'K' ).split( ',' )

    if 'nonn' in keywords:
        result = downloadOEISText( id, 'S' )
        result += downloadOEISText( id, 'T' )
        result += downloadOEISText( id, 'U' )
    else:
        result = downloadOEISText( id, 'V' )
        result += downloadOEISText( id, 'W' )
        result += downloadOEISText( id, 'X' )

    if 'cons' in keywords:
        offset = int( downloadOEISText( id, 'O' ).split( ',' )[ 0 ] )
        result = ''.join( result.split( ',' ) )
        return mpmathify( result[ : offset ] + '.' + result[ offset : ] )
    else:
        return [ int( i ) for i in result.split( ',' ) ]


#//******************************************************************************
#//
#//  downloadOEISText
#//
#//******************************************************************************

def downloadOEISText( id, char, addCR=False ):
    import urllib.request
    import re as regex

    data = urllib.request.urlopen( 'http://oeis.org/search?q=id%3AA{:06}'.format( id ) + '&fmt=text' ).read( )

    pattern = regex.compile( b'%' + bytes( char, 'ascii' ) + b' A[0-9][0-9][0-9][0-9][0-9][0-9] (.*?)\n', regex.DOTALL )

    lines = pattern.findall( data )

    result = ''

    for line in lines:
        if result != '' and addCR:
            result += '\n'

        result += line.decode( 'ascii' )

    return result


#//******************************************************************************
#//
#//  convertToBase10
#//
#//******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = g.numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  Parse out a time value or a numerical expression and attempt to set the
#//  precision to an appropriate value based on the expression.
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
    innerChars = term[ 1 : -1 ]

    if '/' in innerChars:
        term = term.replace( '/', '-' )
        innerChars = term[ 1 : -1 ]

    if ( '-' in innerChars ) or ( ':' in innerChars ):
        try:
            datetime = arrow.get( term )
        except:
            raise ValueError( 'error parsing datetime' )

        return datetime

    if term == '0':
        return mpmathify( 0 )

    # ignore commas
    term = ''.join( [ i for i in term if i not in ',' ] )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return mpmathify( term )

        decimal = term.find( '.' )
    else:
        decimal = len( term )

    negative = term[ 0 ] == '-'

    if negative:
        start = 1
    else:
        if term[ 0 ] == '+':
            start = 1
        else:
            start = 0

    integer = term[ start : decimal ]
    mantissa = term[ decimal + 1 : ]

    # check for hex, then binary, then octal, otherwise a plain old decimal integer
    if not ignoreSpecial and mantissa == '':
        if integer[ 0 ] == '0':
            if len( integer ) == 1:
                return mpmathify( 0 )

            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        if integer[ 0 ] == '1' and integer[ -1 ] in 'bB':
            # set the precision big enough to handle this value
            newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            integer = integer[ : -1 ]
            return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


#//******************************************************************************
#//
#//  roundMantissa
#//
#//******************************************************************************

def roundMantissa( mantissa, accuracy ):
    if len( mantissa ) <= accuracy:
        return mantissa

    lastDigit = int( mantissa[ accuracy - 1 ] )
    extraDigit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extraDigit >= 5:
        result += str( lastDigit + 1 )
    else:
        result += str( lastDigit )

    return result


#//******************************************************************************
#//
#//  convertToBaseN
#//
#//******************************************************************************

def convertToBaseN( value, base, baseAsDigits, numerals ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( numerals ) )

    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( ( -1 ) * value, base, baseAsDigits, numerals )

    if base == 10:
        return str( value )

    result = ''
    leftDigits = value

    while leftDigits > 0:
        if baseAsDigits:
            if result != '':
                result = ' ' + result

            result = str( int( leftDigits ) % base ) + result
        else:
            result = numerals[ int( leftDigits ) % base ] + result

        leftDigits = floor( fdiv( leftDigits, base ) )

    return result


#//******************************************************************************
#//
#//  convertToPhiBase
#//
#//******************************************************************************

def convertToPhiBase( num ):
    epsilon = power( 10, -( mp.dps - 3 ) )

    output = ''
    integer = ''

    start = True
    previousPlace = 0
    remaining = num

    originalPlace = 0

    while remaining > epsilon:
        place = int( floor( log( remaining, phi ) ) )

        if start:
            output = '1'
            start = False
            originalPlace = place
        else:
            if place < -( originalPlace + 1 ):
                break

            for i in range( previousPlace, place + 1, -1 ):
                output += '0'

                if ( i == 1 ):
                    integer = output
                    output = ''

            output += '1'

            if place == 0:
                integer = output
                output = ''

        previousPlace = place
        remaining -= power( phi, place )

    if integer == '':
        return output, ''
    else:
        return integer, output


#//******************************************************************************
#//
#//  convertToFibBase
#//
#//  Returns a string with Fibonacci encoding for n (n >= 1).
#//
#//  adapted from https://en.wikipedia.org/wiki/Fibonacci_coding
#//
#//******************************************************************************

def convertToFibBase( value ):
    result = ''

    n = value

    if n >= 1:
        a = 1
        b = 1

        c = fadd( a, b )    # next Fibonacci number
        fibs = [ b ]        # list of Fibonacci numbers, starting with F(2), each <= n

        while n >= c:
            fibs.append( c )  # add next Fibonacci number to end of list
            a = b
            b = c
            c = fadd( a, b )

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + '1'
            else:
                result = result + '0'

    return result


#//******************************************************************************
#//
#//  convertFractionToBaseN
#//
#//******************************************************************************

def convertFractionToBaseN( value, base, precision, baseAsDigits, accuracy ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( g.numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( g.numerals ) )

    if value < 0 or value >= 1.0:
        raise ValueError( 'value (%s) must be >= 0 and < 1.0' % value )

    if base == 10:
        return str( value )

    result = ''

    while value > 0 and precision > 0:
        value = value * base
        digit = int( value )

        if len( result ) == accuracy:
            value -= digit
            newDigit = int( value ) % base

            if newDigit >= base // 2:
                digit += 1

        if baseAsDigits:
            if result != '':
                result += ' '

            result += str( digit % base )
        else:
            result += g.numerals[ digit % base ]

        if len( result ) == accuracy:
            break

        value -= digit
        precision -= 1

    return result


#//******************************************************************************
#//
#//  formatOutput
#//
#//  This takes a string representation of the result and formats it according
#//  to a whole bunch of options.
#//
#//******************************************************************************

def formatOutput( output, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                  decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    # filter out text strings
    for c in output:
        if c in '+-.':
            continue

        if c in string.whitespace or c in string.punctuation:
            return output

    exponentIndex = output.find( 'e' )

    if exponentIndex > 0:
        exponent = int( output[ exponentIndex + 1 : ] )
        output = output[ : exponentIndex ]
    else:
        exponent = 0

    imaginary = im( mpmathify( output ) )

    if imaginary != 0:
        if imaginary < 0:
            imaginary = fabs( imaginary )
            negativeImaginary = True
        else:
            negativeImaginary = False

        imaginaryValue = formatOutput( nstr( imaginary, mp.dps ), radix, numerals, integerGrouping,
                                       integerDelimiter, leadingZero, decimalGrouping, decimalDelimiter,
                                       baseAsDigits, outputAccuracy )

        strOutput = str( re( mpmathify( output ) ) )
    else:
        imaginaryValue = ''
        strOutput = nstr( output, outputAccuracy  )[ 1 : -1 ]
        #strOutput = str( output )

    #print( strOutput )

    if '.' in strOutput:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    integer = strOutput[ 1 if negative else 0 : decimal ]
    integerLength = len( integer )

    mantissa = strOutput[ decimal + 1 : ]

    if mantissa == '0':
        mantissa = ''
    elif mantissa != '' and outputAccuracy == -1:
        mantissa = mantissa.rstrip( '0' )

    #print( 'integer: ', integer )
    #print( 'mantissa: ', mantissa )
    #print( 'exponent: ', exponent )
    #
    #if exponent > 0:
    #    if exponent > len( mantissa ):
    #        integer += mantissa + '0' * ( exponent - len( mantissa ) )
    #        mantissa = ''
    #    else:
    #        integer += mantissa[ : exponent ]
    #        mantissa = mantissa[ exponent + 1 : ]
    #elif exponent < 0:
    #    exponent = -exponent
    #
    #    if exponent > len( integer ):
    #        mantissa = '0' * ( exponent - len( integer ) ) + integer + mantissa
    #        integer = '0'
    #    else:
    #        mantissa = integer[ exponent : ]
    #        integer = integer[ : exponent - 1 ]

    if radix == phiBase:
        integer, mantissa = convertToPhiBase( mpmathify( output ) )
    elif radix == fibBase:
        integer = convertToFibBase( floor( mpmathify( output ) ) )
    elif radix != 10 or numerals != defaultNumerals:
        integer = str( convertToBaseN( mpmathify( integer ), radix, baseAsDigits, numerals ) )

        if mantissa:
            mantissa = str( convertFractionToBaseN( mpmathify( '0.' + mantissa ), radix,
                            int( ( mp.dps - integerLength ) / math.log10( radix ) ),
                            baseAsDigits, outputAccuracy ) )
    else:
        if outputAccuracy == 0:
            mantissa = ''
        elif outputAccuracy > 0:
            mantissa = roundMantissa( mantissa, outputAccuracy )
            mantissa = mantissa.rstrip( '0' )

    if integerGrouping > 0:
        firstDelimiter = len( integer ) % integerGrouping

        if leadingZero and firstDelimiter > 0:
            integerResult = '0' * ( integerGrouping - firstDelimiter )
        else:
            integerResult = ''

        integerResult += integer[ : firstDelimiter ]

        for i in range( firstDelimiter, len( integer ), integerGrouping ):
            if integerResult != '':
                integerResult += integerDelimiter

            integerResult += integer[ i : i + integerGrouping ]

    else:
        integerResult = integer

    if decimalGrouping > 0:
        mantissaResult = ''

        for i in range( 0, len( mantissa ), decimalGrouping ):
            if mantissaResult != '':
                mantissaResult += decimalDelimiter

            mantissaResult += mantissa[ i : i + decimalGrouping ]
    else:
        mantissaResult = mantissa

    if negative:
        result = '-'
    else:
        result = ''

    result += integerResult

    if mantissaResult != '':
        result += '.' + mantissaResult

    if imaginaryValue != '':
        result = '( ' + result + ( ' - ' if negativeImaginary else ' + ' ) + imaginaryValue + 'j )'

    if exponent != 0:
        result += 'e' + str( exponent )

    return result


#//******************************************************************************
#//
#//  formatListOutput
#//
#//******************************************************************************

def formatListOutput( result, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                      decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    resultString = '[ '

    for item in result:
        if resultString != '[ ':
            resultString += ', '

        if isinstance( item, list ):
            resultString += formatListOutput( item, radix, numerals, integerGrouping, integerDelimiter,
                                              leadingZero, decimalGrouping, decimalDelimiter, baseAsDigits,
                                              outputAccuracy )
        else:
            if isinstance( item, arrow.Arrow ):
                resultString += formatDateTime( item )
            else:
                itemString = str( item )

                resultString += formatOutput( itemString, radix, numerals, integerGrouping, integerDelimiter,
                                              leadingZero, decimalGrouping, decimalDelimiter, baseAsDigits,
                                              outputAccuracy )

            if isinstance( item, Measurement ):
                resultString += ' ' + formatUnits( item )

    resultString += ' ]'

    return resultString


#//******************************************************************************
#//
#//  formatUnits
#//
#//******************************************************************************

def formatUnits( measurement ):
    value = mpf( measurement )

    if measurement.getUnitName( ) is not None:
        unitString = ''

        if value < mpf( -1.0 ) or value > mpf( 1.0 ):
            tempString = measurement.getPluralUnitName( )
        else:
            tempString = measurement.getUnitName( )

        for c in tempString:
            if c == '_':
                unitString += ' '
            else:
                unitString += c

        return unitString

    unitString = ''

    # first, we simplify the units
    units = measurement.getUnits( ).simplify( )

    # now that we've expanded the compound units, let's format...
    for unit in units:
        exponent = units[ unit ]

        if exponent > 0:
            if unitString != '':
                unitString += ' '

            if value == 1:
                unitString += unit
            else:
                unitString += g.unitOperators[ unit ].plural

            if exponent > 1:
                unitString += '^' + str( int( exponent ) )

    negativeUnits = ''

    if unitString == '':
        for unit in units:
            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits != '':
                    negativeUnits += ' '

                negativeUnits += unit
                negativeUnits += '^' + str( int( exponent ) )
    else:
        for unit in units:
            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits == '':
                    negativeUnits = ' per '
                else:
                    negativeUnits += ' '

                negativeUnits += unit

                if exponent > 1:
                    negativeUnits += '^' + str( int( exponent ) )
                elif exponent < -1:
                    negativeUnits += '^' + str( int( -exponent ) )

    result = ''

    for c in unitString + negativeUnits:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#//******************************************************************************
#//
#//  formatDateTime
#//
#//******************************************************************************

def formatDateTime( datetime ):
    return datetime.format( 'YYYY-MM-DD HH:mm:ss' )


#//******************************************************************************
#//
#//  printParagraph
#//
#//******************************************************************************

def printParagraph( text, lineLength=80, indent=0 ):
    lines = textwrap.wrap( text, lineLength - 1 )

    for line in lines:
        print( ' ' * indent + line )


#//******************************************************************************
#//
#//  printOperatorHelp
#//
#//******************************************************************************

def printOperatorHelp( helpArgs, term, operatorInfo, operatorHelp, operatorAliases, lineLength ):
    if operatorInfo.argCount == 1:
        print( 'n ', end='' )
    elif operatorInfo.argCount == 2:
        print( 'n k ', end='' )
    elif operatorInfo.argCount == 3:
        print( 'a b c ', end='' )
    elif operatorInfo.argCount == 4:
        print( 'a b c d ', end='' )
    elif operatorInfo.argCount == 5:
        print( 'a b c d e ', end='' )

    aliasList = [ key for key in operatorAliases if term == operatorAliases[ key ] ]

    print( term + ' - ' + operatorHelp[ 1 ] )

    print( )

    if len( aliasList ) > 1:
        printParagraph( 'aliases:  ' + ', '.join( aliasList ), lineLength )
    elif len( aliasList ) == 1:
        printParagraph( 'alias:  ' + aliasList[ 0 ], lineLength )

    print( 'category: ' + operatorHelp[ 0 ] )

    if operatorHelp[ 2 ] == '\n':
        print( )
        print( 'No further help is available.' )
    else:
        print( operatorHelp[ 2 ] )

    if len( helpArgs ) > 1 and helpArgs[ 1 ] in ( 'ex', 'example' ):
        print( )

        if operatorHelp[ 3 ] == '\n':
            print( 'No examples are available.' )
        else:
            print( term + ' examples:' )
            print( operatorHelp[ 3 ] )


#//******************************************************************************
#//
#//  addAliases
#//
#//******************************************************************************

def addAliases( operatorList, operatorAliases ):
    for index, operator in enumerate( operatorList ):
        aliasList = [ key for key in operatorAliases if operator == operatorAliases[ key ] ]

        if len( aliasList ) > 0:
            operatorList[ index ] += ' (' + ', '.join( aliasList ) + ')'


#//******************************************************************************
#//
#//  printCategoryHelp
#//
#//******************************************************************************

def printCategoryHelp( category, operators, listOperators, modifiers, operatorAliases, operatorHelp, lineLength ):
    printParagraph( 'The ' + category + ' category includes the following operators (with aliases in parentheses):', lineLength )
    print( )

    operatorList = [ key for key in operators if operatorHelp[ key ][ 0 ] == category ]
    operatorList.extend( [ key for key in listOperators if operatorHelp[ key ][ 0 ] == category ] )
    operatorList.extend( [ key for key in modifiers if operatorHelp[ key ][ 0 ] == category ] )

    addAliases( operatorList, operatorAliases )

    for operator in sorted( operatorList ):
        print( operator )


#//******************************************************************************
#//
#//  printHelp
#//
#//******************************************************************************

def printHelp( programName, programDescription, operators, listOperators, modifiers, operatorAliases,
               dataPath, helpArgs, lineLength ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            helpVersion = pickle.load( pickleFile )
            basicCategories = pickle.load( pickleFile )
            operatorHelp = pickle.load( pickleFile )

        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'unit_help.pckl.bz2', 'rb' ) ) as pickleFile:
            unitTypeDict = pickle.load( pickleFile )

    except FileNotFoundError:
        print( 'rpn:  Unable to load help file.  Help will be unavailable.' )
        return

    if helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    operatorCategories = set( operatorHelp[ key ][ 0 ] for key in operatorHelp )

    if len( helpArgs ) == 0:
        printGeneralHelp( programName, programDescription, basicCategories, operatorCategories, lineLength )
        return

    term = helpArgs[ 0 ]

    # first check if the term is an alias and translate
    if term in operatorAliases:
        term = operatorAliases[ term ]

    # then look for exact matches in all the lists of terms for which we have help support
    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ], operatorHelp[ term ], operatorAliases, lineLength )
    elif term in listOperators:
        printOperatorHelp( helpArgs, term, listOperators[ term ], operatorHelp[ term ], operatorAliases, lineLength )
    elif term in modifiers:
        printOperatorHelp( helpArgs, term, modifiers[ term ], operatorHelp[ term ], operatorAliases, lineLength )
    elif term in basicCategories:
        print( basicCategories[ term ] )
    elif term in operatorCategories:
        printCategoryHelp( term, operators, listOperators, modifiers, operatorAliases, operatorHelp, lineLength )
    elif term == 'unit_types':
        printParagraph( ', '.join( sorted( unitTypeDict.keys( ) ) ), lineLength - 5, 4 )
    elif term in unitTypeDict:
        printParagraph( ', '.join( sorted( unitTypeDict[ term ] ) ), lineLength - 5, 4 )
    else:
        # if no exact matches for any topic, let's look for partial matches
        if 'unit_types'.startswith( term ):
            print( 'Interpreting topic as \'unit_types\'.' )
            printParagraph( ', '.join( sorted( unitTypeDict.keys( ) ) ), lineLength - 5, 4 )
            return

        helpTerm = next( ( i for i in unitTypeDict if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( )
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            printParagraph( ', '.join( sorted( unitTypeDict[ helpTerm ] ) ), lineLength - 5, 4 )
            return

        helpTerm = next( ( i for i in operators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpArgs, helpTerm, operators[ helpTerm ], operatorHelp[ helpTerm ], operatorAliases, lineLength )
            return

        helpTerm = next( ( i for i in listOperators if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpArgs, helpTerm, listOperators[ helpTerm ], operatorHelp[ helpTerm ], operatorAliases, lineLength )
            return

        helpTerm = next( ( i for i in modifiers if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printOperatorHelp( helpArgs, helpTerm, modifiers[ helpTerm ], operatorHelp[ helpTerm ], operatorAliases, lineLength )
            return

        helpTerm = next( ( i for i in basicCategories if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            print( basicCategories[ helpTerm ] )
            return

        helpTerm = next( ( i for i in operatorCategories if i != term and i.startswith( term ) ), '' )

        if helpTerm != '':
            print( 'Interpreting topic as \'' + helpTerm + '\'.' )
            print( )
            printCategoryHelp( helpTerm, operators, listOperators, modifiers, operatorAliases, operatorHelp, lineLength )
        else:
            print( "Help topic not found." )


#//******************************************************************************
#//
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( programName, programDescription, basicCategories, operatorCategories, lineLength ):
    print( programName + ' ' + PROGRAM_VERSION + ' - ' + programDescription )
    print( COPYRIGHT_MESSAGE )
    print( )

    printParagraph(
'''For help on a specific topic, add a help topic, operator category or a specific operator name.  Adding
'example', or 'ex' after an operator name will result in examples of use being printed as well.''', lineLength )

    print( )
    print( 'The following is a list of general topics:' )
    print( )

    helpCategories = list( basicCategories.keys( ) )
    helpCategories.append( 'unit_types' )

    printParagraph( ', '.join( sorted( helpCategories ) ), lineLength - 5, 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( operatorCategories ) ), lineLength - 5, 4 )


#//******************************************************************************
#//
#//  printTitleScreen
#//
#//******************************************************************************

def printTitleScreen( programName, programDescription ):
    print( programName, PROGRAM_VERSION, '-', programDescription )
    print( COPYRIGHT_MESSAGE )
    print( )
    print( 'For more information use, \'' + programName + ' help\'.' )


#//******************************************************************************
#//
#//  validateOptions
#//
#//******************************************************************************

def validateOptions( args ):
    if args.hex:
        if args.output_radix != 10 and args.output_radix != 16:
            return False, '-r and -x can\'t be used together'

        if args.octal:
            return False, '-x and -o can\'t be used together'

    if args.octal:
        if args.output_radix != 10 and args.output_radix != 8:
            return False, '-r and -o can\'t be used together'

    if args.output_radix_numerals > 0:
        if args.hex:
            return False, '-R and -x can\'t be used together'

        if args.octal:
            return False, '-R and -o can\'t be used together'

        if args.output_radix != 10:
            return False, '-R and -r can\'t be used together'

        if args.output_radix_numerals < 2:
            return False, 'output radix must be greater than 1'

    if args.comma and args.integer_grouping > 0 :
        return False, 'rpn:  -c can\'t be used with -i'

    if args.output_radix_numerals > 0 and \
       ( args.comma or args.decimal_grouping > 0 or args.integer_grouping > 0 ):
        return False, '-c, -d and -i can\'t be used with -R'

    return True, ''


#//******************************************************************************
#//
#//  validateArguments
#//
#//******************************************************************************

def validateArguments( terms ):
    bracketCount = 0

    for term in terms:
        if term == '[':
            bracketCount += 1
        elif term == ']':
            bracketCount -= 1

    if bracketCount:
        print( 'rpn:  mismatched brackets (count: {})'.format( bracketCount ) )
        return False

    return True


#//******************************************************************************
#//
#//  evaluateOneListFunction
#//
#//******************************************************************************

def evaluateOneListFunction( func, args ):
    if isinstance( args, list ):
        for arg in args:
            if isinstance( arg, list ) and isinstance( arg[ 0 ], list ):
                return [ evaluateOneListFunction( func, arg ) for arg in args ]

        return func( args )
    else:
        return func( [ args ] )


#//******************************************************************************
#//
#//  evaluateOneArgFunction
#//
#//******************************************************************************

def evaluateOneArgFunction( func, args ):
    if isinstance( args, list ):
        return [ evaluateOneArgFunction( func, i ) for i in args ]
    else:
        return func( args )


#//******************************************************************************
#//
#//  evaluateTwoArgFunction
#//
#//******************************************************************************

def evaluateTwoArgFunction( func, arg1, arg2 ):
    #print( 'arg1: ' + str( arg1 ) )
    #print( 'arg2: ' + str( arg2 ) )

    len1 = len( arg1 )
    len2 = len( arg2 )

    list1 = len1 > 1
    list2 = len2 > 1

    #print( list1 )
    #print( list2 )

    if list1:
        if list2:
            return [ func( arg2[ index ], arg1[ index ] ) for index in range( 0, min( len1, len2 ) ) ]
        else:
            return [ func( arg2[ 0 ], i ) for i in arg1 ]

    else:
        if list2:
            return [ func( j, arg1[ 0 ] ) for j in arg2 ]
        else:
            return [ func( arg2[ 0 ], arg1[ 0 ] ) ]


#//******************************************************************************
#//
#//  callers
#//
#//******************************************************************************

callers = [
    lambda func, args: [ func( ) ],
    evaluateOneArgFunction,
    evaluateTwoArgFunction,
    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for c in arg1 for b in arg2 for a in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for d in arg1 for c in arg2 for b in arg3 for a in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for e in arg1 for d in arg2 for c in arg3 for b in arg4 for a in arg5 ],
]


#//******************************************************************************
#//
#//  convertUnits
#//
#//******************************************************************************

def convertUnits( unit1, unit2 ):
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


