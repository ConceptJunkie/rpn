#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import argparse
import bz2
import collections
import contextlib
import datetime
import pickle
import itertools
import math
import os
import random
import string
import struct
import sys
import textwrap
import time

from fractions import Fraction
from functools import reduce
from mpmath import *

from rpnDeclarations import *
from rpnPrimeUtils import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


#//******************************************************************************
#//
#//  getUnitType
#//
#//******************************************************************************

def getUnitType( unit ):
    if unit in unitOperators:
        return unitOperators[ unit ].unitType
    else:
        return unit


#//******************************************************************************
#//
#//  getSimpleUnitType
#//
#//******************************************************************************

def getSimpleUnitType( unit ):
    if unit in unitOperators:
        return unitOperators[ unit ].representation
    else:
        return unit


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
    global unitConversionMatrix

    if unitConversionMatrix is None:
        loadUnitConversionMatrix( )

    #print( 'combine units1:', units1 )
    #print( 'combine units2:', units2 )
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
                    factor = fdiv( factor, pow( mpmathify( unitConversionMatrix[ ( unit1, unit2 ) ] ), units2[ unit2 ] ) )
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
            if unit not in unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            if unitType in types:
                types[ unitType ] += self.units[ unit ]
            else:
                types[ unitType ] = self[ unit ]

        #print( 'types:', types )
        return types


    def simplify( self ):
        #print( 'simplify in:', self )

        result = Units( )

        for unit in self:
            simpleUnits = Units( unitOperators[ unit ].representation )
            #print( 'simple units:', simpleUnits )

            exponent = self.get( unit )

            if exponent != 1:   # handle exponent
                for unit2 in simpleUnits:
                    simpleUnits[ unit2 ] *= exponent

            result.increment( simpleUnits )

        #print( 'simplify out:', result )
        return result


    def getBasicTypes( self ):
        result = Units( )

        for unitType in self:
            basicUnits = Units( basicUnitTypes[ unitType ][ 0 ] )

            exponent = self[ unitType ]

            if exponent != 1:   # handle exponent
                for unitType2 in basicUnits:
                    basicUnits[ unitType2 ] *= exponent

            result = combineUnits( result, basicUnits )[ 1 ]

        #print( 'basic in:', unitTypes )
        #print( 'basic out:', result )
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
                    resultString += '^' + str( exponent )

        denominator = ''

        for unit in sorted( self ):
            exponent = self.get( unit )

            if exponent < 0:
                if denominator != '':
                    denominator += '*'

                denominator += unit

                if exponent < -1:
                    denominator += '^' + str( -exponent )

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
                    raise ValueError( 'wasn\'t expecting another \'*\'', start )

                operands = unit.split( '^' )

                if len( operands ) > 2:
                    raise ValueError( 'wasn\'t expecting another exponent' )
                else:
                    if len( operands ) == 2:
                        exponent = int( operands[ 1 ] )
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
                return add( self, newOther )
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
                return subtract( self, newOther )
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

        return self.normalizeUnits( )


    def divide( self, other ):
        newValue = fdiv( self, other )

        if isinstance( other, Measurement ):
            factor, newUnits = combineUnits( self.getUnits( ).simplify( ),
                                             other.getUnits( ).invert( ).simplify( ) )

            self = Measurement( fmul( newValue, factor ), newUnits )
        else:
            self = Measurement( newValue, self.getUnits( ),
                                self.getUnitName( ), self.getPluralUnitName( ) )

        return self.normalizeUnits( )


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


    def normalizeUnits( self ):
        value = mpf( self )
        units = self.getUnits( )

        newUnits = { }

        for unit in units:
            if units[ unit ] != 0:
                newUnits[ unit ] = units[ unit ]

        negative = True

        for unit in newUnits:
            if newUnits[ unit ] > 0:
                negative = False
                break

        if negative:
            return Measurement( value, newUnits ).invert( )
        else:
            return Measurement( value, newUnits, self.getUnitName( ), self.getPluralUnitName( ) )


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
                result = result and self.isCompatible( item )

            return result
        elif isinstance( other, Measurement ):
            #print( 'types: ', self.getTypes( ), other.getTypes( ) )
            #print( 'simple types: ', self.getSimpleTypes( ), other.getSimpleTypes( ) )
            #print( 'basic types: ', self.getBasicTypes( ), other.getBasicTypes( ) )

            if self.getTypes( ) == other.getTypes( ):
                return True
            elif self.getSimpleTypes( ) == other.getSimpleTypes( ):
                return True
            elif self.getBasicTypes( ) == other.getBasicTypes( ):
                return True
            else:
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
            if unit not in unitOperators:
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
        global unitConversionMatrix

        if unitConversionMatrix is None:
            loadUnitConversionMatrix( )

        reduced = Measurement( mpf( self ), Units( ) )

        for unit in self.units:
            if unit not in unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            unitType = getUnitType( unit )

            newUnit = basicUnitTypes[ unitType ][ 1 ]

            if unit != newUnit:
                value = power( mpf( unitConversionMatrix[ ( unit, newUnit ) ] ), self.units[ unit ] )
            else:
                value = '1.0'

            reduced = reduced.multiply( Measurement( value, Units( newUnit ) ) )

        return reduced


    def convertValue( self, other ):
        global unitConversionMatrix

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

            global operatorAliases

            if unit1String in operatorAliases:
                unit1String = operatorAliases[ unit1String ]

            if unit2String in operatorAliases:
                unit2String = operatorAliases[ unit2String ]

            #print( 'unit1String: ', unit1String )
            #print( 'unit2String: ', unit2String )

            exponents = [ ]

            if unitConversionMatrix is None:
                loadUnitConversionMatrix( )

            # look for a straight-up conversion
            if ( unit1String, unit2String ) in unitConversionMatrix:
                value = fmul( mpf( self ), mpmathify( unitConversionMatrix[ ( unit1String, unit2String ) ] ) )
            elif ( unit1String, unit2String ) in specialUnitConversionMatrix:
                value = specialUnitConversionMatrix[ ( unit1String, unit2String ) ]( mpf( self ) )
            else:
                conversionValue = mpmathify( 1 )

                if unit1String in compoundUnits:
                    newUnit1String = compoundUnits[ unit1String ]
                else:
                    newUnit1String = unit1String

                if unit2String in compoundUnits:
                    newUnit2String = compoundUnits[ unit2String ]
                else:
                    newUnit2String = unit2String

                #print( 'newUnit1String: ', newUnit1String )
                #print( 'newUnit2String: ', newUnit2String )

                # if that isn't found, then we need to do the hard work and break the units down
                for unit1 in units1:
                    for unit2 in units2:
                        #print( '1 and 2:', unit1, unit2 )
                        if getUnitType( unit1 ) == getUnitType( unit2 ):
                            conversions.append( [ unit1, unit2 ] )
                            exponents.append( units1[ unit1 ] )
                            break

                value = conversionValue
                index = 0

                for conversion in conversions:
                    #print( 'conversion: ', conversion, '^', exponents[ index ] )
                    if conversion[ 0 ] == conversion[ 1 ]:
                        continue  # no conversion needed

                    conversionValue = mpmathify( unitConversionMatrix[ ( conversion[ 0 ], conversion[ 1 ] ) ] )
                    conversionValue = power( conversionValue, exponents[ index ] )
                    #print( 'conversion: ', conversion, conversionValue )

                    index += 1

                    value = fmul( value, conversionValue )

                value = fmul( mpf( self ), value )

            return value
        else:
            raise ValueError( 'incompatible units cannot be converted: ' + self.getUnitString( ) + \
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
#//  add
#//
#//  We used to be able to call fadd directly, but now we want to be able to add
#//  units.  Adding units includes an implicit conversion if the units are not
#//  the same.
#//
#//******************************************************************************

def add( n, k ):
    if isinstance( n, Measurement ):
        return n.add( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).add( k )
    else:
        return fadd( n, k )


#//******************************************************************************
#//
#//  subtract
#//
#//  We used to be able to call fsub directly, but now we want to be able to
#//  subtract units and do the appropriate conversions.
#//
#//******************************************************************************

def subtract( n, k ):
    if isinstance( n, Measurement ):
        return n.subtract( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).subtract( k )
    else:
        return fsub( n, k )


#//******************************************************************************
#//
#//  divide
#//
#//  We used to be able to call fdiv directly, but now we want to also divide
#//  the units.  Doing so lets us do all kinds of great stuff because now we
#//  can support compound units without having to explicitly declare them in
#//  makeUnits.py.
#//
#//******************************************************************************

def divide( n, k ):
    if isinstance( n, Measurement ):
        return n.divide( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).divide( k )
    else:
        return fdiv( n, k )


#//******************************************************************************
#//
#//  multiply
#//
#//  We used to be able to call fmul directly, but now we want to also multiply
#//  the units.  This allows compound units and the conversion routines try to
#//  be smart enough to deal with this.  There are scenarios in which it doesn't
#//  work, like converting parsec*barn to cubic_inch.  However, that can be done
#//  by converting parsec to inche and barn to square_inch separately and
#//  multiplying the result.
#//
#//******************************************************************************

def multiply( n, k ):
    if isinstance( n, Measurement ):
        return n.multiply( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).multiply( k )
    else:
        return fmul( n, k )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( n, k ):
    if isinstance( n, Measurement ):
        return n.exponentiate( k )
    elif isinstance( k, Measurement ):
        raise ValueError( 'a measurement cannot be exponentiated' )
    else:
        return power( n, k )


#//******************************************************************************
#//
#//  sum
#//
#//******************************************************************************

def sum( n ):
    hasUnits = False

    for item in n:
        if isinstance( item, Measurement ):
            hasUnits = True
            break

    if hasUnits:
        result = None

        for item in n:
            if result is None:
                result = item
            else:
                result = result.add( item )

        return result
    else:
        return fsum( n )


#//******************************************************************************
#//
#//  takeReciprocal
#//
#//  We used to be able to call fdiv directly, but now we want to handle
#//  Measurements
#//
#//******************************************************************************

def takeReciprocal( n ):
    if isinstance( n, Measurement ):
        return n.invert( )
    else:
        return fdiv( 1, n )


#//******************************************************************************
#//
#//  getNthAlternatingFactorial
#//
#//******************************************************************************

def getNthAlternatingFactorial( n ):
    result = 0

    negative = False

    for i in arange( n, 0, -1 ):
        if negative:
            result = fadd( result, fneg( fac( i ) ) )
            negative = False
        else:
            result = fadd( result, fac( i ) )
            negative = True

    return result


#//******************************************************************************
#//
#//  getNthPascalLine
#//
#//******************************************************************************

def getNthPascalLine( n ):
    result = [ ]

    for i in arange( 0, n ):
        result.append( binomial( n - 1, i ) )

    return result


#//******************************************************************************
#//
#//  getNthAperyNumber
#//
#//  http://oeis.org/A005259
#//
#//  a(n) = sum(k=0..n, C(n,k)^2 * C(n+k,k)^2 )
#//
#//******************************************************************************

def getNthAperyNumber( n ):
    result = 0

    for k in arange( 0, n + 1 ):
        result = fadd( result, fmul( power( binomial( n, k ), 2 ), power( binomial( fadd( n, k ), k ), 2 ) ) )

    return result


#//******************************************************************************
#//
#//  ContinuedFraction
#//
#//  A continued fraction, represented as a list of integer terms.
#//
#//  adapted from ActiveState Python, recipe 578647
#//
#//******************************************************************************

class ContinuedFraction( list ):
    def __init__( self, value, maxterms=15, cutoff=1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            self.extend( value )
        else:
            raise ValueError( 'ContinuedFraction requires a number or a list' )

    def getFraction( self, terms=None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


#//******************************************************************************
#//
#//  getDivisorCount
#//
#//******************************************************************************

def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in factor( n ) ] )


#//******************************************************************************
#//
#//  getDivisors
#//
#//******************************************************************************

def getDivisors( n ):
    result = getExpandedFactorList( factor( n ) )

    result = [ list( i ) for i in itertools.chain.from_iterable( itertools.combinations( result, r ) for r in range( 0, len( result ) + 1 ) ) ]

    from operator import mul
    result = set( [ reduce( mul, i, 1 ) for i in result[ 1 : ] ] )
    result.add( 1 )

    result = sorted( list( result ) )

    return result


#//******************************************************************************
#//
#//  factor
#//
#//  This is not my code, and I need to find the source so I can attribute it.
#//
#//******************************************************************************

def factor( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factor( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def getPotentialPrimes( ):
            basePrimes = ( 2, 3, 5 )

            for basePrime in basePrimes:
                yield basePrime

            basePrimes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            primeGroup = 0

            while True:
                for basePrime in basePrimes:
                    yield primeGroup + basePrime

                primeGroup += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in getPotentialPrimes( ):
            if divisor > sqrtn:
                break

            power = 0

            while ( fmod( n, divisor ) ) == 0:
                n = floor( fdiv( n, divisor ) )
                power += 1

            if power > 0:
                factors.append( ( divisor, power ) )
                sqrtn = sqrt( n )

        if n > 1:
             factors.append( ( int( n ), 1 ) )

        return factors


#//******************************************************************************
#//
#//  getExpandedFactorList
#//
#//******************************************************************************

def getExpandedFactorList( factors ):
    factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return reduce( lambda x, y: x + y, factors, [ ] )


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
#//  convertFractionToBaseN
#//
#//******************************************************************************

def convertFractionToBaseN( value, base, precision, baseAsDigits, accuracy ):
    if baseAsDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( numerals ) )

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
            result += numerals[ digit % base ]

        if len( result ) == accuracy:
            break

        value -= digit
        precision -= 1

    return result


#//******************************************************************************
#//
#//  convertToBase10
#//
#//******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = numerals[ : inputRadix ]

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
#//  getInvertedBits
#//
#//******************************************************************************

def getInvertedBits( n ):
    global bitwiseGroupSize

    value = floor( n )
    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining = value

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        result = fadd( fmul( fsum( [ placeValue, fneg( fmod( remaining, placeValue ) ), -1 ] ), multiplier ), result )
        remaining = floor( fdiv( remaining, placeValue ) )
        multiplier = fmul( multiplier, placeValue )

    return result


#//******************************************************************************
#//
#//  performBitwiseOperation
#//
#//  The operations are performed on groups of bits as specified by the variable
#//  bitwiseGroupSize.  Although doing it this way isn't really necessary, it
#//  does mean that under normal circumstances the regular Python bit operators
#//  can be used.
#//
#//******************************************************************************

def performBitwiseOperation( i, j, operation ):
    global bitwiseGroupSize

    value1 = floor( i )
    value2 = floor( j )

    # determine how many groups of bits we will be looking at
    groupings = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )
    groupings2 = int( fadd( floor( fdiv( ( log( value1, 2 ) ), bitwiseGroupSize ) ), 1 ) )

    if groupings2 > groupings:
        groupings = groupings2

    placeValue = mpmathify( 1 << bitwiseGroupSize )
    multiplier = mpmathify( 1 )
    remaining1 = value1
    remaining2 = value2

    result = mpmathify( 0 )

    for i in range( 0, groupings ):
        mod1 = fmod( remaining1, placeValue )
        mod2 = fmod( remaining2, placeValue )

        result = fadd( fmul( operation( int( mod1 ), int( mod2 ) ), multiplier ), result )

        remaining1 = floor( fdiv( remaining1, placeValue ) )
        remaining2 = floor( fdiv( remaining2, placeValue ) )

        multiplier = fmul( multiplier, placeValue )

    return result


#//******************************************************************************
#//
#//  performTrigOperation
#//
#//******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, Measurement ):
        value = mpf( i.convertValue( Measurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )


#//******************************************************************************
#//
#//  getBitCount
#//
#//******************************************************************************

def getBitCount( n ):
    result = 0

    value = int( n )

    while ( value ):
        value &= value - 1
        result += 1

    return result


#//******************************************************************************
#//
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  getNthLucasNumber
#//
#//******************************************************************************

def getNthLucasNumber( n ):
    if n == 1:
        return 1
    else:
        return floor( fadd( power( phi, n ), 0.5 ) )


#//******************************************************************************
#//
#//  getNthJacobsthalNumber
#//
#//  From: http://oeis.org/A001045
#//
#//  a(n) = ceiling(2^(n+1)/3)-ceiling(2^n/3)
#//
#//******************************************************************************

def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthPellNumber
#//
#//  From:  http://oeis.org/A000129
#//
#//  a(n) = round((1+sqrt(2))^n)
#//
#//******************************************************************************

def getNthPellNumber( n ):
    return getNthLinearRecurrence( [ 1, 2 ], [ 0, 1 ], n )


#//******************************************************************************
#//
#//  getNthBaseKRepunit
#//
#//******************************************************************************

def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( k ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


#//******************************************************************************
#//
#//  getPrimePi
#//
#//******************************************************************************

def getPrimePi( n ):
    result = primepi2( n )

    return [ mpf( result.a ), mpf( result.b ) ]


#//******************************************************************************
#//
#//  getNthTribonacci
#//
#//******************************************************************************

def getNthTribonacci( n ):
    roots = polyroots( [ 1, -1, -1, -1  ] )
    roots2 = polyroots( [ 44, 0, -2, -1 ] )

    result = 0

    for i in range( 0, 3 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthTetranacci
#//
#//  http://mathworld.wolfram.com/TetranacciNumber.html
#//
#//******************************************************************************

def getNthTetranacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1 ] )
    roots2 = polyroots( [ 563, 0, -20, -5, -1 ] )

    result = 0

    for i in range( 0, 4 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthPentanacci
#//
#//******************************************************************************

def getNthPentanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 5 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 8, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHexanacci
#//
#//******************************************************************************

def getNthHexanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 6 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 10, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthHeptanacci
#//
#//******************************************************************************

def getNthHeptanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 7 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 3, 12, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


#//******************************************************************************
#//
#//  getNthSylvester
#//
#//******************************************************************************

def getNthSylvester( n ):
    if n == 1:
        return 2
    elif n == 2:
        return 3
    else:
        list = [ 2, 3 ]

        for i in arange( 2, n ):
            list.append( fprod( list ) + 1 )

    return list[ -1 ]


#//******************************************************************************
#//
#//  getNthPolygonalNumber
#//
#//******************************************************************************

def getNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coeff = fdiv( fsub( k, 2 ), 2 )
    return polyval( [ coeff, fneg( fsub( coeff, 1 ) ), 0 ], n )


#//******************************************************************************
#//
#//  getRegularPolygonArea
#//
#//  based on having sides of unit length
#//
#//  http://www.mathopenref.com/polygonregulararea.html
#//
#//******************************************************************************

def getRegularPolygonArea( n ):
    if n < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) )


#//******************************************************************************
#//
#//  getNSphereRadius
#//
#//  k needs to be a Measurement so getNSphereRadius can tell if it's an area
#//  or a volume and use the correct formula.
#//
#//******************************************************************************

def getNSphereRadius( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return Measurement( k, 'length' )  # default is 'length' anyway

    print( type( k.getBasicTypes( ).getUnitString( ) ) )

    measurementType = k.getBasicTypes( ).getUnitString( )

    if measurementType == 'length':
        return 1
    elif measurementType == 'area':
        return fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                           fmul( n, power( pi, fdiv( n, 2 ) ) ) ),
                     root( k, fsub( n, 1 ) ) )
    elif measurementType == 'volume':
        return root( fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                                 power( pi, fdiv( n, 2 ) ) ), k ), 3 )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' + measurementType )


#//******************************************************************************
#//
#//  getNSphereSurfaceArea
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is a volume
#//  then it is taken to be the volume.  If it is an area, then it is returned
#//  unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereSurfaceArea( n, k ):
    if not isinstance( k, Measurement ):
        return getNSphereSurfaceArea( n, Measurement( k, 'length' ) )

    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( fmul( n, power( pi, fdiv( n, 2 ) ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, fsub( n, 1 ) ) )
    elif measurementType == { 'length' : 2 }:
        return k
    elif measurementType == { 'length' : 3 }:
        return 3
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )


#//******************************************************************************
#//
#//  getNSphereVolume
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is an area
#//  then it is taken to be the surface area.  If it is a volume, then it is
#//  returned unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereVolume( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return getNSphereVolume( n, Measurement( k, 'length' ) )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( power( pi, fdiv( n, 2 ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, n ) )
    elif measurementType == { 'length' : 2 }:
        return 2   # formula for converting surface area to volume
    elif measurementType == { 'length' : 3 }:
        return k
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )


#//******************************************************************************
#//
#//  getTriangleArea
#//
#//  https://en.wikipedia.org/wiki/Equilateral_triangle#Area
#//
#//******************************************************************************

def getTriangleArea( a, b, c ):
    return fdiv( fsum( [ power( a, 2 ), power( b, 2 ), power( c, 2 ) ] ), fmul( 4, sqrt( 3 ) ) )


#//******************************************************************************
#//
#//  findNthPolygonalNumber
#//
#//  http://www.wolframalpha.com/input/?i=solve+%28+%28+k+%2F+2+%29+-+1+%29+x^2+-+%28+%28+k+%2F+2+%29+-+2+%29+x+%2B+0+%3D+n+for+x
#//
#//******************************************************************************

def findNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( fsum( [ sqrt( fsum( [ power( k, 2 ), fprod( [ 8, k, n ] ),
                                       fneg( fmul( 8, k ) ), fneg( fmul( 16, n ) ), 16 ] ) ),
                         k, -4 ] ), fmul( 2, fsub( k, 2 ) ) )


#//******************************************************************************
#//
#//  getCenteredPolygonalNumber
#//
#//******************************************************************************

def getCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coefficient = fdiv( k, 2 )
    return polyval( [ coefficient, fneg( coefficient ), 1 ], n )


#//******************************************************************************
#//
#//  findCenteredPolygonalNumber
#//
#//  wolframalpha.com solved this for me.
#//
#//******************************************************************************

def findCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    s = fdiv( k, 2 )

    return fdiv( fadd( sqrt( s ), sqrt( fsum( [ fmul( 4, n ), s, -4 ] ) ) ), fmul( 2, sqrt( s ) ) )


#//******************************************************************************
#//
#//  getNthHexagonalSquareNumber
#//
#//  http://oeis.org/A046177
#//
#//  a(n) = floor(1/32*(tan(3*pi/8))^(8*n-4))
#//
#//******************************************************************************

#//******************************************************************************
#//
#//  getNthHexagonalPentagonalNumber
#//
#//  http://oeis.org/A046178
#//
#//  a(n) = ceiling(1/12*(sqrt(3)-1)*(2+sqrt(3))^(4n-2)).
#//
#//******************************************************************************

def getNthHexagonalPentagonalNumber( n ):
    return ceil( fdiv( fmul( fsub( sqrt( 3 ), 1 ),
                             power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                       12 ) )


#//******************************************************************************
#//
#//  getNthHeptagonalTriangularNumber
#//
#//  http://oeis.org/A046194
#//
#//  a(n) = 1/80*((3-sqrt(5)*(-1)^n)*(2+sqrt(5))^(4n-2)+
#//               (3+sqrt(5)*(-1)^n)*(2-sqrt(5))^(4n-2)-14)
#//
#//  LinearRecurrence[ { 1, 103682, -103682, -1, 1 },
#//                    { 1, 55, 121771, 5720653, 12625478965 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -1, -103682, 103682, 1 ],
                                   [ 1, 55, 121771, 5720653, 12625478965 ], n )


#//******************************************************************************
#//
#//  getNthHeptagonalSquareNumber
#//
#//  http://oeis.org/A046195
#//
#//  LinearRecurrence[ { 1 , 0, 1442, -1442, 0, -1, 1 },
#//                    { 1, 6, 49, 961, 8214, 70225, 1385329 }, n ]
#//
#//******************************************************************************

def getNthHeptagonalSquareNumber( n ):
    index = getNthLinearRecurrence( [ 1, -1, 0, -1442, 1442, 0, 1 ],
                                    [ 1, 6, 49, 961, 8214, 70225, 1385329 ], n )

    return getNthPolygonalNumber( index, 7 )


#//******************************************************************************
#//
#//  getNthHeptagonalPentagonalNumber
#//
#//  http://oeis.org/A048900
#//
#//  a(n) = floor(1/240*((2+sqrt(15))^2*(4+sqrt(15))^(4n-3)))
#//
#//******************************************************************************

def getNthHeptagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( power( fadd( 2, sqrt( 15 ) ), 2 ),
                              power( fadd( 4, sqrt( 15 ) ), fsub( fmul( 4, n ), 3 ) ) ), 240 ) )


#//******************************************************************************
#//
#//  getNthHeptagonalHexagonalNumber
#//
#//  http://oeis.org/A048903
#//
#//  a(n) = floor(1/80*(sqrt(5)-1)*(2+sqrt(5))^(8n-5))
#//
#//******************************************************************************

def getNthHeptagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( sqrt( 5 ), 1 ),
                              power( fadd( 2, sqrt( 5 ) ), fsub( fmul( 8, n ), 5 ) ) ), 80 ) )


#//******************************************************************************
#//
#//  getNthOctagonalTriangularNumber
#//
#//  From http://oeis.org/A046183
#//
#//  a(n) = floor(1/96*(7-2*sqrt(6)*(-1)^n)*(sqrt(3)+sqrt(2))^(4n-2))
#//
#//  LinearRecurrence[{1, 9602, -9602, -1, 1}, {1, 21, 11781, 203841, 113123361}, 13]
#//
#//******************************************************************************

def getNthOctagonalTriangularNumber( n ):
    sign = power( -1, n )

    return floor( fdiv( fmul( fsub( 7, fprod( [ 2, sqrt( 6 ), sign ] ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                        96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalSquareNumber
#//
#//  From http://oeis.org/A036428:
#//
#//  a(n) = 1/12 * ((2 + sqrt(3)) ^ (4n-2) + (2 - sqrt(3)) ^ (4n-2) - 2).
#//  a(n) = floor (1/12 * (2 + sqrt(3)) ^ (4n-2)).
#//
#//******************************************************************************

def getNthOctagonalSquareNumber( n ):
    return floor( fdiv( power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ), 12 ) )


#//******************************************************************************
#//
#//  getNthOctagonalPentagonalNumber
#//
#//  http://oeis.org/A046189
#//
#//  a(n) = floor(1/96*(11-6*sqrt(2)*(-1)^n)*(1+sqrt(2))^(8*n-6))
#//
#//******************************************************************************

def getNthOctagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( fsub( 11, fprod( [ 6, sqrt( 2 ), power( -1, n ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 8, n ), 6 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHexagonalNumber
#//
#//  http://oeis.org/A046192
#//
#//  a(n) = floor(1/96*(3*sqrt(3)-sqrt(2))*(sqrt(3)+sqrt(2))^(8n-5))
#//
#//******************************************************************************

def getNthOctagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( fmul( 3, sqrt( 3 ) ), sqrt( 2 ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 8, n ), 5 ) ) ), 96 ) )


#//******************************************************************************
#//
#//  getNthOctagonalHeptagonalNumber
#//
#//  http://oeis.org/A048906
#//
#//  a(n) = floor(1/480*(17+2*sqrt(30))*(sqrt(5)+sqrt(6))^(8n-6))
#//
#//******************************************************************************

def getNthOctagonalHeptagonalNumber( n ):
    return floor( fdiv( fmul( fadd( 17, fmul( sqrt( 30 ), 2 ) ),
                              power( fadd( sqrt( 5 ), sqrt( 6 ) ), fsub( fmul( 8, n ), 6 ) ) ), 480 ) )


#//******************************************************************************
#//
#//  getNthNonagonalTriangularNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = ( 5/14 ) +
#//           ( 9/28 ) * { [ 8 - 3 * sqrt(7) ] ^ n + [ 8 + 3 * sqrt( 7 ) ] ^ n } +
#//           ( 3/28 ) * sqrt(7) * { [ 8 + 3 * sqrt(7) ] ^ n - [ 8 - 3 * sqrt(7) ] ^ n }
#//
#//******************************************************************************

def getNthNonagonalTriangularNumber( n ):
    a = fmul( 3, sqrt( 7 ) )
    b = fadd( 8, a )
    c = fsub( 8, a )

    return fsum( [ fdiv( 5, 14 ),
                   fmul( fdiv( 9, 28 ), fadd( power( b, n ), power( c, n ) ) ),
                   fprod( [ fdiv( 3, 28 ),
                            sqrt( 7 ),
                            fsub( power( b, n ), power( c, n ) ) ] ) ] )


#//******************************************************************************
#//
#//  getNthNonagonalSquareNumber
#//
#//  From http://oeis.org/A048911:
#//
#//  Indices of square numbers which are also 9-gonal.
#//
#//  Let p = 8 * sqrt( 7 ) + 9 * sqrt( 14 ) - 7 * sqrt( 2 ) - 28 and
#//      q = 7 * sqrt( 2 ) + 9 * sqrt( 14 ) - 8 * sqrt( 7 ) - 28.
#//
#//  Then a( n ) = 1 / 112 *
#//                 ( ( p + q * (-1) ^ n ) * ( 2 * sqrt( 2 ) + sqrt( 7 ) ) ^ n -
#//                  ( p - q * (-1) ^ n ) * ( 2 * sqrt( 2 ) - sqrt( 7 ) ) ^ ( n - 1 ) )
#//
#//******************************************************************************

def getNthNonagonalSquareNumber( n ):
    p = fsum( [ fmul( 8, sqrt( 7 ) ), fmul( 9, sqrt( 14 ) ), fmul( -7, sqrt( 2 ) ), -28 ] )
    q = fsum( [ fmul( 7, sqrt( 2 ) ), fmul( 9, sqrt( 14 ) ), fmul( -8, sqrt( 7 ) ), -28 ] )
    sign = power( -1, n )

    index = fdiv( fsub( fmul( fadd( p, fmul( q, sign ) ),
                                    power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), n ) ),
                              fmul( fsub( p, fmul( q, sign ) ),
                                    power( fsub( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), fsub( n, 1 ) ) ) ), 112 )

    return power( round( index ), 2 )


#//******************************************************************************
#//
#//  getNthNonagonalPentagonalNumber
#//
#//  http://oeis.org/A048915
#//
#//  a(n) = floor(1/336*(25+4*sqrt(21))*(5-sqrt(21)*(-1)^n)*(2*sqrt(7)+3*sqrt(3))^(4n-4)).
#//
#//  LinearRecurrence[{1, 146361602, -146361602, -1, 1}, {1, 651, 180868051, 95317119801, 26472137730696901}, 9]
#//
#//******************************************************************************

def getNthNonagonalPentagonalNumber( n ):
    sqrt21 = sqrt( 21 )
    sign = power( -1, n )

    return floor( fdiv( fprod( [ fadd( 25, fmul( 4, sqrt21 ) ),
                                 fsub( 5, fmul( sqrt21, sign ) ),
                                 power( fadd( fmul( 2, sqrt( 7 ) ), fmul( 3, sqrt( 3 ) ) ),
                                        fsub( fmul( 4, n ), 4 ) ) ] ),
                        336 ) )


#//******************************************************************************
#//
#//  getNthNonagonalHexagonalNumber
#//
#//  From http://oeis.org/A048907:
#//
#//  a( n ) = floor( 9/112 * ( 8 - 3 * sqrt( 7 ) * (-1) ^ n ) *
#//                          ( 8 + 3 * sqrt( 7 ) ) ^ ( 4 * n - 4 ) )
#//
#//******************************************************************************

def getNthNonagonalHexagonalNumber( n ):
    #a = fmul( 3, sqrt( 7 ) )
    #b = fadd( 8, a )
    #c = fsub( 8, a )

    #sign = 1 #power( -1, n )
    #exponent = fsub( fmul( 4, n ), 4 )

    #print( str( fmul( c, sign ) ) + '  ' + str( power( b, exponent ) ) )

    #return floor( fprod( [ fdiv( 9, 112 ), fmul( c, sign ), power( b, exponent ) ] ) )

    return getNthLinearRecurrence( [ 1, -1, -4162056194, 4162056194, 1 ],
                                   [ 1, 325, 5330229625, 1353857339341, 22184715227362706161 ], n )


#//******************************************************************************
#//
#//  getNthNonagonalHeptagonalNumber
#//
#//  From http://oeis.org/A048921
#//
#//  a(n) = floor(1/560*(39+4*sqrt(35))*(6+sqrt(35))^(4*n-3)).
#//
#//  LinearRecurrence[{20163, -20163, 1}, {1, 26884, 542041975}, 9]; (* Ant King, Dec 31 2011 *)
#//
#//******************************************************************************

def getNthNonagonalHeptagonalNumber( n ):
    sqrt35 = sqrt( 35 )

    return floor( fdiv( fmul( fadd( 39, fmul( 4, sqrt35 ) ),
                        power( fadd( 6, sqrt35 ), fsub( fmul( 4, n ), 3 ) ) ),
                        560 ) )


#//******************************************************************************
#//
#//  getNthNonagonalOctagonalNumber
#//
#//  From http://oeis.org/A048924:
#//
#//  a(n) = floor(1/672*(11*sqrt(7)-9*sqrt(6))*(sqrt(6)+sqrt(7))^(8n-5)).
#//
#//  LinearRecurrence[{454275, -454275, 1}, {1, 631125, 286703855361}, 30] (* Vincenzo Librandi, Dec 24 2011 *)
#//
#//******************************************************************************

def getNthNonagonalOctagonalNumber( n ):
    sqrt6 = sqrt( 6 )
    sqrt7 = sqrt( 7 )

    return floor( fdiv( fmul( fsub( fmul( 11, sqrt7 ), fmul( 9, sqrt6 ) ),
                              power( fadd( sqrt6, sqrt7 ), fsub( fmul( 8, n ), 5 ) ) ),
                        672 ) )

# Dec-tri
# http://oeis.org/A133216
# a(n) = floor ( 1/64 * (9 + 4*sqrt(2)*(-1)^n) * (1+sqrt(2))^(4*n-6) )

# Dec-square
# http://oeis.org/A133142
#  a(n)=(1/8)+(7/16)*[721-228*sqrt(10)]^n-(1/8)*[721-228*sqrt(10)]^n*sqrt(10)+(1/8)*[721+228 *sqrt(10)]^n*sqrt(10)+(7/16)*[721+228*sqrt(10)]^n

# Dec-pent
# http://oeis.org/A202563
# a(n) = floor(25/192*(sqrt(3)+sqrt(2))^(8*n-6))

# Dec-hex
# http://oeis.org/A203134
# a(n) = floor(1/64 *(5*sqrt(2)-1)*(sqrt(2)+1)^(8*n-5)).

# Dec-hept
# http://oeis.org/A203408
# a(n) = floor(1/320*(11-2*sqrt(10)*(-1)^n)*(1+sqrt(10))* (3+sqrt(10))^(4*n-3)).

# Dec-oct
# http://oeis.org/A203624
# a(n) = floor(1/192*(13+4*sqrt(3))*(2+sqrt(3))^(8*n-6)).

# Dec-non
# http://oeis.org/A203627
# a(n) = floor(1/448*(15+2*sqrt(14))*(2*sqrt(2)+sqrt(7))^(8*n-6)).

#//******************************************************************************
#//
#//  findTetrahedralNumber
#//
#//  Thanks for wolframalpha.com for solving the reverse of the above formula.
#//
#//******************************************************************************

def findTetrahedralNumber( n ):
    sqrt3 = sqrt( 3 )
    curt3 = cbrt( 3 )

    # TODO:  finish me
    return 0

# http://www.wolframalpha.com/input/?i=solve+p%3D%281%2F6%29*%28n^3%2B3*n^2%2B2*n%29+for+n


#//******************************************************************************
#//
#//  getNthTruncatedTetrahedralNumber
#//
#//  Take the (3n-2)th terahedral number and chop off the (n-1)th tetrahedral
#//  number from each corner.
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedTetrahedralNumber( n ):
    return fmul( fdiv( n, 6 ), fsum( [ fprod( [ 23, n, n ] ), fmul( -27, n ), 10 ] ) )


#//******************************************************************************
#//
#//  getNthSquareTriangularNumber
#//
#//******************************************************************************

def getNthSquareTriangularNumber( n ):
    neededPrecision = int( n * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        mp.dps = neededPrecision

    sqrt2 = sqrt( 2 )

    return ceil( power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                    power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                              fmul( 4, sqrt2 ) ), 2 ) )


#//******************************************************************************
#//
#//  getNthPolygonalPyramidalNumber
#//
#//******************************************************************************

def getNthPolygonalPyramidalNumber( n, k ):
    return fprod( [ n, fadd( n, 1 ),
                    fsub( fmul( fsub( k, 2 ), n ), fsub( k, 5 ) ),
                    fdiv( 1, 6 ) ] )


#// A002415         4-dimensional pyramidal numbers: n^2*(n^2-1)/12.
#//                                                  n^4 - n^2 / 12
#//
#// A005585         5-dimensional pyramidal numbers: n(n+1)(n+2)(n+3)(2n+3)/5!.
#//
#// A001608         Perrin sequence (or Ondrej Such sequence): a(n) = a(n-2) + a(n-3).
#//                 LinearRecurrence[{0, 1, 1}, {3, 0, 2}, n]
#//
#// A001845         Centered octahedral numbers (crystal ball sequence for cubic lattice).
#//                 LinearRecurrence[{4, -6, 4, -1}, {1, 7, 25, 63}, 40]
#//
#// A046090         Consider all Pythagorean triples (X,X+1,Z) ordered by increasing Z; sequence gives X+1 values.
#//                 a(n+1)=round((1+(7+5*sqrt(2))*(3+2*sqrt(2))^n)/2);
#//                 LinearRecurrence[{7, -7, 1}, {1, 4, 21}, 25]
#//
#// A050534         Tritriangular numbers: a(n)=binomial(binomial(n,2),2) = n(n + 1)(n - 1)(n - 2)/8.
#//
#// A002817         Doubly triangular numbers: n*(n+1)*(n^2+n+2)/8.
#//                 a(n) = 3*binomial(n+2, 4)+binomial(n+1, 2).
#//
#// A007588         Stella octangula numbers: n*(2*n^2 - 1).
#//
#// A005803         Second-order Eulerian numbers: 2^n - 2*n.
#//
#// A060888         n^6-n^5+n^4-n^3+n^2-n+1.      -- general form of this
#//
#// A048736         Dana Scott's sequence: a(n) = (a(n-2) + a(n-1) * a(n-3)) / a(n-4), a(0) = a(1) = a(2) = a(3) = 1.
#//
#// A022095         Fibonacci sequence beginning 1 5.
#//                 a(n) = ((2*sqrt(5)-1)*(((1+sqrt(5))/2)^(n+1)) + (2*sqrt(5)+1)*(((1-sqrt(5))/2)^(n+1)))/(sqrt(5)).
#//
#// A005894         Centered tetrahedral numbers.
#//                 a(n)=(2*n+1)*(n^2+n+3)/3
#//
#// A015447         Generalized Fibonacci numbers: a(n) = a(n-1) + 11*a(n-2).
#//                 a(n)={[ (1+3*sqrt(5))/2 ]^(n+1) - [ (1-3*sqrt(5))/2 ]^(n+1)}/3*sqrt(5).
#//                 LinearRecurrence[{1, 11}, {1, 1}, 30]
#//                 CoefficientList[Series[ 1/(1-x-11 x^2), {x, 0, 50}], x]
#//
#// A046176         Indices of square numbers which are also hexagonal.
#//
#// A056105         First spoke of a hexagonal spiral.
#//
#// A006522         4-dimensional analogue of centered polygonal numbers. Also number of regions created by sides and diagonals of n-gon in general position.
#//                 a(n)=binomial(n, 4)+ binomial(n-1, 2)
#//
#// A022086         Fibonacci sequence beginning 0 3.
#//                 a(n) = round( (6phi-3)/5 phi^n ) (works for n>2)
#//
#// A069778         q-factorial numbers 3!_q.
#//
#// A005021         Random walks (binomial transform of A006054).
#//
#// A074584         Esanacci ("6-anacci") numbers.
#//                 LinearRecurrence[{1, 1, 1, 1, 1, 1}, {6, 1, 3, 7, 15, 31}, 50]
#//
#// A195142         Concentric 10-gonal numbers.
#//
#// A000453         Stirling numbers of the second kind, S(n,4).
#//
#// A005915         Hexagonal prism numbers: (n + 1)*(3*n^2 + 3*n + 1).
#//
#// A015442         Generalized Fibonacci numbers: a(n) = a(n-1) + 7 a(n-2), a(0)=0, a(1)=1.
#//                 a(n) = ( ((1+sqrt(29))/2)^(n+1) - ((1-sqrt(29))/2)^(n+1) )/sqrt(29)
#//
#// A002418         4-dimensional figurate numbers: (5*n-1)*binomial(n+2,3)/4.
#//
#// A005165         Alternating factorials: n! - (n-1)! + (n-2)! - ... 1!.
#//
#// A006007         4-dimensional analogue of centered polygonal numbers: a(n) = n(n+1)*(n^2+n+4)/12.
#//
#// A104621         Heptanacci-Lucas numbers.
#//


#//******************************************************************************
#//
#//  getNthStellaOctangulaNumber
#//
#//  Stel(n) = Oct(n) + 8 Tet(n-1)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthStellaOctangulaNumber( n ):
    return polyval( [ 4, 0, -2 ], n )


#//******************************************************************************
#//
#//  getNthCenteredCube
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthCenteredCubeNumber( n ):
    return fadd( power( n, 3 ), power( fsub( n, 1 ), 3 ) )


#//******************************************************************************
#//
#//  getNthTruncatedOctahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  16n^3 - 33n^2 + 24n - 6
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthTruncatedOctahedralNumber( n ):
    return polyval( [ 16, -33, 24, 6 ], n )


#//******************************************************************************
#//
#//  getNthRhombicDodecahedralNumber
#//
#//  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
#//  number from each of the six vertices.
#//
#//  Rho(n) = CCub(n) + 6 Pyr(n-1)
#//
#//  4n^3 + 6n^2 + 4n + 1
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthRhombicDodecahedralNumber( n ):
    return polyval( [ 4, 6, 4, 1 ], n )


#//******************************************************************************
#//
#//  getNthPentatopeNumber
#//
#//  1/24n ( n + 1 )( n + 2 )( n + 3 )
#//
#//  1/24 n^4 + 1/4 n^3 + 11/24 n^2 + 1/4 n
#//
#//  1/24 ( n^4 + 6 n^3 + 11 n^2 + 6n )
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPentatopeNumber( n ):
    return fdiv( polyval( [ 1, 6, 11, 6, 0 ], n ), 24 )


#//******************************************************************************
#//
#//  getNthPolytopeNumber
#//
#//  d = dimension
#//
#//  (1/(d-1)!) PI k=0 to n-1 (n+k)
#//
#//  from Conway and Guy's "The Book of Numbers"
#//
#//******************************************************************************

def getNthPolytopeNumber( n, d ):
    result = n
    m = n + 1

    for i in arange( 1, d - 1 ):
        result = fmul( result, m )
        m += 1

    return fdiv( result, fac( d - 1 ) )


#//******************************************************************************
#//
#//  getNthDelannoyNumber
#//
#//******************************************************************************

def getNthDelannoyNumber( n ):
    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fmul( binomial( n, k ), binomial( fadd( n, k ), k ) ) )

    return result


#//******************************************************************************
#//
#//  getNthSchroederNumber
#//
#//******************************************************************************

def getNthSchroederNumber( n ):
    if n == 1:
        return 1

    # TODO: raise exception for n < 0 !

    n = fsub( n, 1 )

    result = 0

    for k in arange( 0, fadd( n, 1 ) ):
        result = fadd( result, fdiv( fprod( [ power( 2, k ), binomial( n, k ),
                                              binomial( n, fsub( k, 1 ) ) ] ), n ) )

    return result


#//******************************************************************************
#//
#//  getNthMotzkinNumber
#//
#//  http://oeis.org/A001006
#//
#//  a(n) = sum((-1)^j*binomial(n+1, j)*binomial(2n-3j, n), j=0..floor(n/3))/(n+1)
#//
#//******************************************************************************

def getNthMotzkinNumber( n ):
    result = 0

    for j in arange( 0, floor( fdiv( n, 3 ) ) + 1 ):
        result = fadd( result, fprod( [ power( -1, j ), binomial( fadd( n, 1 ), j ),
                                      binomial( fsub( fmul( 2, n ), fmul( 3, j ) ), n ) ] ) )

    return fdiv( result, fadd( n, 1 ) )


#//******************************************************************************
#//
#//  getNthPadovanNumber
#//
#//  Padovan sequence: a(n) = a(n-2) + a(n-3) with a(0)=1, a(1)=a(2)=0.
#//
#//  http://oeis.org/A000931
#//
#//  a(n) = (r^n)/(2r+3) + (s^n)/(2s+3) + (t^n)/(2t+3) where r, s, t are the
#//  three roots of x^3-x-1
#//
#//  http://www.wolframalpha.com/input/?i=solve+x^3-x-1
#//
#//  Unfortunately, the roots are scary-complicated, but it's a non-iterative
#//  formula, so I'll use it.
#//
#//  Wikipedia leaves off the first 4 terms, but Sloane's includes them.
#//  Wikipedia cites Ian Stewart and Mathworld, and I'll use their definition.
#//
#//******************************************************************************

def getNthPadovanNumber( arg ):
    result = 0

    n = fadd( arg, 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    e = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, e ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, e ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, e ) ) )

    return round( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                              fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                              fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )

#//******************************************************************************
#//
#//  getPrimorial
#//
#//******************************************************************************

def getPrimorial( n ):
    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result


#//******************************************************************************
#//
#//  getPermutations
#//
#//******************************************************************************

def getPermutations( n, r ):
    if ( r > n ):
        raise ValueError( 'number of elements (%d) cannot exceed the size of the set (%d)' % ( r, n ) )

    return fdiv( fac( n ), fac( fsub( n, r ) ) )


#//******************************************************************************
#//
#//  convertFromContinuedFraction
#//
#//******************************************************************************

def convertFromContinuedFraction( i ):
    if not isinstance( i, list ):
        i = [ i ]

    fraction = ContinuedFraction( i ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


#//******************************************************************************
#//
#//  interpretAsFraction
#//
#//******************************************************************************

def interpretAsFraction( i, j ):
    fraction = ContinuedFraction( i, maxterms=j ).getFraction( )
    return [ fraction.numerator, fraction.denominator ]


#//******************************************************************************
#//
#//  interpretAsBase
#//
#//  This is a list operator so if the integer argument (base) is also a list,
#//  we need to handle that explicitly here.
#//
#//******************************************************************************

def interpretAsBase( args, base ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ interpretAsBase( i, base ) for i in args ]
        else:
            args.reverse( )
    else:
        args = [ args ]

    if isinstance( base, list ):
        return [ interpretAsBase( args, i ) for i in base ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


#//******************************************************************************
#//
#//  unpackInteger
#//
#//******************************************************************************

def unpackInteger( n, fields ):
    if isinstance( n, list ):
        return [ unpackInteger( i, fields ) for i in n ]

    if not isinstance( fields, list ):
        return unpackInteger( n, [ fields ] )

    value = int( n )
    result = [ ]

    for i in reversed( fields ):
        size = int( i )
        result.insert( 0, value & ( 2 ** size - 1 ) )
        value >>= size

    return result


#//******************************************************************************
#//
#//  getPlasticConstant
#//
#//******************************************************************************

def getPlasticConstant( ):
    term = fmul( 12, sqrt( 69 ) )
    return fdiv( fadd( cbrt( fadd( 108, term ) ), cbrt( fsub( 108, term ) ) ), 6 )


#//******************************************************************************
#//
#//  solveQuadraticPolynomial
#//
#//******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    if a == 0:
        if b == 0:
            raise ValueError( 'invalid equation, no variable coefficients' )
        else:
            # linear equation, one root
            return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


#//******************************************************************************
#//
#//  solveCubicPolynomial
#//
#//  Adapted from http://www.1728.org/cubic2.htm
#//
#//******************************************************************************

def solveCubicPolynomial( a, b, c, d ):
    if a == 0:
        return solveQuadraticPolynomial( b, c, d )

    f = fdiv( fsub( fdiv( fmul( 3, c ), a ), fdiv( power( b, 2 ), power( a, 2 ) ) ), 3 )

    g = fdiv( fadd( fsub( fdiv( fmul( 2, power( b, 3 ) ), power( a, 3 ) ),
                          fdiv( fprod( [ 9, b, c ] ), power( a, 2 ) ) ),
                    fdiv( fmul( 27, d ), a ) ), 27 )
    h = fadd( fdiv( power( g, 2 ), 4 ), fdiv( power( f, 3 ), 27 ) )

    # all three roots are the same
    if h == 0:
        x1 = fneg( root( fdiv( d, a ), 3 ) )
        x2 = x1
        x3 = x2
    # two imaginary and one real root
    elif h > 0:
        r = fadd( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if r < 0:
            s = fneg( root( fneg( r ), 3 ) )
        else:
            s = root( r, 3 )

        t = fsub( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if t < 0:
            u = fneg( root( fneg( t ), 3 ) )
        else:
            u = root( t, 3 )

        x1 = fsub( fadd( s, u ), fdiv( b, fmul( 3, a ) ) )

        real = fsub( fdiv( fneg( fadd( s, u ) ), 2 ), fdiv( b, fmul( 3, a ) ) )
        imaginary = fdiv( fmul( fsub( s, u ), sqrt( 3 ) ), 2 )

        x2 = mpc( real, imaginary )
        x3 = mpc( real, fneg( imaginary ) )
    # all real roots
    else:
        j = sqrt( fsub( fdiv( power( g, 2 ), 4 ), h ) )
        k = acos( fneg( fdiv( g, fmul( 2, j ) ) ) )

        if j < 0:
            l = fneg( root( fneg( j ), 3 ) )
        else:
            l = root( j, 3 )

        m = cos( fdiv( k, 3 ) )
        n = fmul( sqrt( 3 ), sin( fdiv( k, 3 ) ) )
        p = fneg( fdiv( b, fmul( 3, a ) ) )

        x1 = fsub( fmul( fmul( 2, l ), cos( fdiv( k, 3 ) ) ), fdiv( b, fmul( 3, a ) ) )
        x2 = fadd( fmul( fneg( l ), fadd( m, n ) ), p )
        x3 = fadd( fmul( fneg( l ), fsub( m, n ) ), p )

    return [ chop( x1 ), chop( x2 ), chop( x3 ) ]


#//******************************************************************************
#//
#//  solveQuarticPolynomial
#//
#//  Adapted from http://www.1728.org/quartic2.htm
#//
#//******************************************************************************

def solveQuarticPolynomial( _a, _b, _c, _d, _e ):
    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )

    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    elif _b == 0 and _c == 0 and _d == 0:
        e = fdiv( _e, _a )

        f = root( _a, 4 )

        x1 = fdiv( root( fneg( e ), 4 ), f )
        x2 = fdiv( fneg( root( fneg( e ), 4 ) ), f )
        x3 = fdiv( mpc( 0, root( fneg( e ), 4 ) ), f )
        x4 = fdiv( mpc( 0, fneg( root( fneg( e ), 4 ) ) ), f )

        return [ x1, x2, x3, x4 ]

    # otherwise we have a regular quartic to solve
    a = 1
    b = fdiv( _b, _a )
    c = fdiv( _c, _a )
    d = fdiv( _d, _a )
    e = fdiv( _e, _a )

    # we turn the equation into a cubic that we can solve
    f = fsub( c, fdiv( fmul( 3, power( b, 2 ) ), 8 ) )
    g = fsum( [ d, fdiv( power( b, 3 ), 8 ), fneg( fdiv( fmul( b, c ), 2 ) ) ] )
    h = fsum( [ e, fneg( fdiv( fmul( 3, power( b, 4 ) ), 256 ) ),
                fmul( power( b, 2 ), fdiv( c, 16 ) ), fneg( fdiv( fmul( b, d ), 4 ) ) ] )

    y1, y2, y3 = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                       fneg( fdiv( power( g, 2 ), 64 ) ) )

    # pick two non-zero roots, if there are two imaginary roots, use them
    if im( y1 ) != 0:
        root1 = y1

        if y2 == 0 or im( y2 ) == 0:
            root2 = y3
        else:
            root2 = y2
    elif y1 == 0:
        root1 = y2
        root2 = y3
    elif y2 == 0:
        root1 = y1
        root2 = y3
    else:
        root1 = y2
        root2 = y3

    # more variables...
    p = sqrt( root1 )
    q = sqrt( root2 )
    r = fdiv( fneg( g ), fprod( [ 8, p, q ] ) )
    s = fneg( fdiv( b, 4 ) )

    # put together the 4 roots
    x1 = fsum( [ p, q, r, s ] )
    x2 = fsum( [ p, fneg( q ), fneg( r ), s ] )
    x3 = fsum( [ fneg( p ), q, fneg( r ), s ] )
    x4 = fsum( [ fneg( p ), fneg( q ), r, s ] )

    return [ chop( x1 ), chop( x2 ), chop( x3 ), chop( x4 ) ]


#//******************************************************************************
#//
#//  getChampernowne
#//
#//******************************************************************************

def getChampernowne( ):
    global inputRadix

    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += convertToBaseN( count, inputRadix, False, defaultNumerals )
        count += 1

    return convertToBase10( '0', result, inputRadix )


#//******************************************************************************
#//
#//  getCopelandErdos
#//
#//******************************************************************************

def getCopelandErdos( ):
    result = ''

    count = 1

    while len( result ) < mp.dps:
        result += str( getNthPrime( count ) )
        count += 1

    return convertToBase10( '0', result, 10 )


#//******************************************************************************
#//
#//  makeImaginary
#//
#//******************************************************************************

def makeImaginary( n ):
    return mpc( real='0.0', imag=n )


#//******************************************************************************
#//
#//  isSquare
#//
#//******************************************************************************

def isSquare( n ):
    sqrtN = sqrt( n )

    return 1 if sqrtN == floor( sqrtN ) else 0


#//******************************************************************************
#//
#//  addPolynomials
#//
#//******************************************************************************

def addPolynomials( a, b ):
    result = Polynomial( a )
    result += Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  multiplyPolynomials
#//
#//******************************************************************************

def multiplyPolynomials( a, b ):
    result = Polynomial( a )
    result *= Polynomial( b )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  evaluatePolynomial
#//
#//******************************************************************************

def evaluatePolynomial( a, b ):
    if not isinstance( a, list ):
        a = [ a ]

    return polyval( a, b )


#//******************************************************************************
#//
#//  solvePolynomial
#//
#//******************************************************************************

def solvePolynomial( args ):
    if len( args ) < 2:
        raise ValueError( "'solve' requires at least an order-1 polynomial (i.e., 2 terms)" )

    return polyroots( args )


#//******************************************************************************
#//
#//  calculatePowerTower
#//
#//******************************************************************************

def calculatePowerTower( args ):
    result = args[ -1 ]

    for i in args[ -1 : : -1 ]:
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  calculatePowerTower2
#//
#//******************************************************************************

def calculatePowerTower2( args ):
    result = args[ 0 ]

    for i in args[ 1 : ]:
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  evaluateOneListFunction
#//
#//******************************************************************************

def evaluateOneListFunction( func, args ):
    if isinstance( args, list ):
        for arg in args:
            if isinstance( arg, list ):
                return [ evaluateOneListFunction( func, arg ) for arg in args ]

        return func( args )
    else:
        return func( [ args ] )


#//******************************************************************************
#//
#//  getAlternatingSum
#//
#//******************************************************************************

def getAlternatingSum( args ):
    for i in range( 1, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getAlternatingSum2
#//
#//******************************************************************************

def getAlternatingSum2( args ):
    for i in range( 0, len( args ), 2 ):
        args[ i ] = fneg( args[ i ] )

    return fsum( args )


#//******************************************************************************
#//
#//  getGCDForTwo
#//
#//******************************************************************************

def getGCDForTwo( a, b ):
    a, b = fabs( a ), fabs( b )

    while a:
        b, a = a, fmod( b, a )

    return b


#//******************************************************************************
#//
#//  getGCD
#//
#//******************************************************************************

def getGCD( args ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getGCD[ arg ] for arg in args ]
        else:
            result = max( args )

            for pair in itertools.permutations( args, 2 ):
                gcd = getGCDForTwo( *pair )

                if gcd < result:
                    result = gcd

                return result
    else:
        return args


#//******************************************************************************
#//
#//  multiplyListOfPolynomials
#//
#//******************************************************************************

def multiplyListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    for i in range( 1, len( args ) ):
        if isinstance( args[ i ], list ) and isinstance( args[ i ][ 0 ], list ):
            pass  # dunno what to do here
        else:
            result *= Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  addListOfPolynomials
#//
#//******************************************************************************

def addListOfPolynomials( args ):
    result = Polynomial( args[ 0 ] )

    for i in range( 1, len( args ) ):
        result += Polynomial( args[ i ] )

    return result.getCoefficients( )


#//******************************************************************************
#//
#//  getGreedyEgyptianFraction
#//
#//******************************************************************************

def getGreedyEgyptianFraction( n, d ):
    if n > d:
        raise ValueError( "'egypt' requires the numerator to be smaller than the denominator" )

    # Create a list to store the Egyptian fraction representation.
    result = [ ]

    rational = Fraction( int( n ), int( d ) )

    # Now, iteratively subtract out the largest unit fraction that may be
    # subtracted out until we arrive at a unit fraction.
    while True:
        # If the rational number has numerator 1, we're done.
        if rational.numerator == 1:
            result.append( rational )
            return result

        # Otherwise, find the largest unit fraction less than the current rational number.
        # This is given by the ceiling of the denominator divided by the numerator.
        unitFraction = Fraction( 1, rational.denominator // rational.numerator + 1 )

        result.append( unitFraction )

        # Subtract out this unit fraction.
        rational = rational - unitFraction

    return result


#//******************************************************************************
#//
#//  dumpOperators
#//
#//******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )

    print( 'special operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ][ 1 ] ) )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  dumpAliases
#//
#//******************************************************************************

def dumpAliases( ):
    for alias in sorted( [ key for key in operatorAliases ] ):
        print( alias, operatorAliases[ alias ] )

    return len( operatorAliases )


#//******************************************************************************
#//
#//  convertToSignedInt
#//
#//  two's compliment logic is in effect here
#//
#//******************************************************************************

def convertToSignedInt( n, k ):
    value = fadd( n, ( power( 2, fsub( k, 1 ) ) ) )
    value = fmod( value, power( 2, k ) )
    value = fsub( value, ( power( 2, fsub( k, 1 ) ) ) )

    return value


#//******************************************************************************
#//
#//  printStats
#//
#//******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:13,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


#//******************************************************************************
#//
#//  dumpStats
#//
#//******************************************************************************

def dumpStats( ):
    global unitConversionMatrix

    if unitConversionMatrix is None:
        loadUnitConversionMatrix( )

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) + len( modifiers ) ) )
    print( '{:10,} unit conversions'.format( len( unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( dataPath ), 'small primes' )
    printStats( loadLargePrimes( dataPath ), 'large primes' )
    printStats( loadIsolatedPrimes( dataPath ), 'isolated primes' )
    printStats( loadTwinPrimes( dataPath ), 'twin primes' )
    printStats( loadBalancedPrimes( dataPath ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( dataPath ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( dataPath ), 'triple balanced primes' )
    printStats( loadSophiePrimes( dataPath ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( dataPath ), 'cousin primes' )
    printStats( loadSexyPrimes( dataPath ), 'sexy primes' )
    printStats( loadTripletPrimes( dataPath ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( dataPath ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( dataPath ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( dataPath ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( dataPath ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( dataPath ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  incrementNestedListLevel
#//
#//  Unlike all other operators, '[' and ']' change global state.
#//
#//******************************************************************************

def incrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel += 1

    valueList.append( list( ) )


#//******************************************************************************
#//
#//  decrementNestedListLevel
#//
#//******************************************************************************

def decrementNestedListLevel( valueList ):
    global nestedListLevel
    nestedListLevel -= 1

    if nestedListLevel < 0:
        raise ValueError( "negative list level (too many ']'s)" )


#//******************************************************************************
#//
#//  duplicateTerm
#//
#//******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, int( count ) ):
        if isinstance( value, list ):
            for i in value:
                valueList.append( i )
        else:
            valueList.append( value )


#//******************************************************************************
#//
#//  appendLists
#//
#//******************************************************************************

def appendLists( valueList ):
    arg2 = valueList.pop( )
    arg1 = valueList.pop( )

    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = [ ]

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    valueList.append( result )


#//******************************************************************************
#//
#//  loadResult
#//
#//******************************************************************************

def loadResult( valueList ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'result.pckl.bz2', 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError as error:
        result = mapmathify( 0 )

    return result


#//******************************************************************************
#//
#//  saveResult
#//
#//******************************************************************************

def saveResult( result ):
    with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'result.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( result, pickleFile )


#//******************************************************************************
#//
#//  alternateSigns
#//
#//******************************************************************************

def alternateSigns( n ):
    for i in range( 1, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  alternateSigns2
#//
#//******************************************************************************

def alternateSigns2( n ):
    for i in range( 0, len( n ), 2 ):
        n[ i ] = -n[ i ]

    return n


#//******************************************************************************
#//
#//  expandRange
#//
#//******************************************************************************

def expandRange( start, end ):
    if start > end:
        step = -1
    else:
        step = 1

    result = list( )

    for i in arange( start, end + step, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandSteppedRange
#//
#//******************************************************************************

def expandSteppedRange( start, end, step ):
    result = list( )

    for i in arange( start, end + 1, step ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  expandGeometricRange
#//
#//******************************************************************************

def expandGeometricRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = fmul( value, step )

    return result


#//******************************************************************************
#//
#//  expandExponentialRange
#//
#//******************************************************************************

def expandExponentialRange( value, step, count ):
    result = list( )

    for i in arange( 0, count ):
        result.append( value )
        value = power( value, step )

    return result


#//******************************************************************************
#//
#//  interleave
#//
#//******************************************************************************

def interleave( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            combined = list( zip( arg1, arg2  ) )
            combined = [ item for sublist in combined for item in sublist ]

            for i in combined:
                result.append( i )
        else:
            for i in arg1:
                result.append( i )
                result.append( arg2 )
    else:
        if list2:
            for i in arg2:
                result.append( arg1 )
                result.append( i )
        else:
            result.append( arg1 )
            result.append( arg2 )

    return result


#//******************************************************************************
#//
#//  makeUnion
#//
#//******************************************************************************

def makeUnion( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        result.extend( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )
    else:
        result.append( arg1 )

        if list2:
            result.extend( arg2 )
        else:
            result.append( arg2 )

    return result


#//******************************************************************************
#//
#//  makeIntersection
#//
#//******************************************************************************

def makeIntersection( arg1, arg2 ):
    list1 = isinstance( arg1, list )
    list2 = isinstance( arg2, list )

    result = list( )

    if list1:
        if list2:
            for i in arg1:
                if i in arg2:
                    result.append( i )
        else:
            if arg2 in arg1:
                result.append( arg2 )
    else:
        if list2:
            if arg1 in arg2:
                result.append( arg1 )
        else:
            if arg1 == arg2:
                result.append( arg1 )

    return result


#//******************************************************************************
#//
#//  getIndexOfMax
#//
#//******************************************************************************

def getIndexOfMax( arg ):
    maximum = -inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] > maximum:
            maximum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  getIndexOfMin
#//
#//******************************************************************************

def getIndexOfMin( arg ):
    minimum = inf
    index = -1

    for i in range( 0, len( arg ) ):
        if arg[ i ] < minimum:
            minimum = arg[ i ]
            index = i

    return index


#//******************************************************************************
#//
#//  unlist
#//
#//******************************************************************************

def unlist( valueList ):
    arg = valueList.pop( )

    if isinstance( arg, list ):
        for i in arg:
            valueList.append( i )
    else:
        valueList.append( arg )


#//******************************************************************************
#//
#//  flatten
#//
#//  http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
#//
#//******************************************************************************

def _flatten( L, containers=( list, tuple ) ):
    i = 0

    while i < len( L ):
        while isinstance( L[ i ], containers ):
            if not L[ i ]:
                L.pop( i )
                i -= 1
                break
            else:
                L[ i : i + 1 ] = ( L[ i ] )
        i += 1
    return L


def flatten( valueList ):
    valueList.append( _flatten( valueList.pop( ) ) )


#//******************************************************************************
#//
#//  getListElement
#//
#//******************************************************************************

def getListElement( arg, index ):
    if isinstance( arg, list ):
        return arg[ int( index ) ]
    else:
        return arg
        # TODO: throw exception if index > 0


#//******************************************************************************
#//
#//  getPrimes
#//
#//******************************************************************************

def getPrimes( value, count ):
    result = list( )

    for i in getNthPrimeRange( value, count ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  getNthLinearRecurrence
#//
#//  nth element of Fibonacci sequence = rpn [ 1 1 ] 1 n
#//  nth element of Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n
#//
#//******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    if not isinstance( recurrence, list ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, list ):
        seeds = [ seeds ]

    if len( seeds ) == 0:
        raise ValueError( 'internal error:  for operator \'linearrecur\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getNthLinearRecurrence( recurrence[ : i ], seeds, i ) )

    if isinstance( n, list ):
        return [ getNthLinearRecurrence( recurrence, seeds, i ) for i in n ]

    if n < len( seeds ):
        return seeds[ int( n ) - 1 ]
    else:
        if len( recurrence ) == 0:
            raise ValueError( 'internal error:  for operator \'linearrecur\', recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in arange( len( seeds ), n ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

            result.append( newValue )
            del result[ 0 ]

        return result[ -1 ]


#//******************************************************************************
#//
#//  countElements
#//
#//******************************************************************************

def countElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( countElements( args[ i ] ) )

        return result
    else:
        return len( args )


#//******************************************************************************
#//
#//  getListDiffs
#//
#//******************************************************************************

def getListDiffs( args ):
    result = [ ]

    for i in range( 0, len( args ) ):
        if isinstance( args[ i ], list ):
            result.append( getListDiffs( args[ i ] ) )
        else:
            if i < len( args ) - 1:
                result.append( fsub( args[ i + 1 ], args[ i ] ) )

    return result


#//******************************************************************************
#//
#//  getUniqueElements
#//
#//******************************************************************************

def getUniqueElements( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( getUniqueElements( args[ i ] ) )

    else:
        seen = set( )

        for i in range( 0, len( args ) ):
            seen.add( args[ i ] )

        result = [ ]

        for i in seen:
            result.append( i )

    return result


#//******************************************************************************
#//
#//  sortAscending
#//
#//******************************************************************************

def sortAscending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ] ) )

        return result
    else:
        return sorted( args )


#//******************************************************************************
#//
#//  sortDescending
#//
#//******************************************************************************

def sortDescending( args ):
    result = [ ]

    if isinstance( args[ 0 ], list ):
        for i in range( 0, len( args ) ):
            result.append( sorted( args[ i ], reverse=True ) )

        return result
    else:
        return sorted( args, reverse=True )


#//******************************************************************************
#//
#//  getStandardDeviation
#//
#//******************************************************************************

def getStandardDeviation( args ):
    mean = fsum( args ) / len( args )

    dev = [ power( fsub( i, mean ), 2 ) for i in args ]
    return sqrt( fsum( dev ) / len( dev ) )


#//******************************************************************************
#//
#//  getCurrentArgList
#//
#//******************************************************************************

def getCurrentArgList( valueList ):
    global nestedListLevel

    argList = valueList

    for i in range( 0, nestedListLevel ):
        argList = argList[ -1 ]

    return argList


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
#//  estimate
#//
#//******************************************************************************

def estimate( measurement ):
    if isinstance( measurement, Measurement ):
        unitType = getUnitType( measurement.getUnitName( ) )

        if unitType == 'mass':
            return estimateMass( measurement )
        elif unitType == 'length':
            return estimateLength( measurement )
        elif unitType == 'volume':
            return estimateVolume( measurement )

    return 0


#//******************************************************************************
#//
#//  estimateMass
#//
#//******************************************************************************

def estimateMass( mass ):
    oneGram = Measurement( 1, { 'gram' : 1 } )
    massInGrams = mpf( Measurement( mass.convertValue( oneGram ), oneGram.getUnits( ) ) )

    massKey = max( key for key in massTable if key <= massInGrams )
    multiple = fdiv( massInGrams, massKey )

    return 'Approximately ' + nstr( multiple, 3 ) + ' times the mass of ' + massTable[ massKey ]


#//******************************************************************************
#//
#//  estimateLength
#//
#//******************************************************************************

def estimateLength( length ):
    oneMeter = Measurement( 1, { 'meter' : 1 } )
    lengthInMeters = mpf( Measurement( length.convertValue( oneMeter ), oneMeter.getUnits( ) ) )

    lengthKey = max( key for key in lengthTable if mpf( key ) < lengthInMeters )
    multiple = fdiv( lengthInMeters, mpf( lengthKey ) )

    return 'Approximately ' + nstr( multiple, 3 ) + ' times the length of ' + lengthTable[ lengthKey ]


#//******************************************************************************
#//
#//  estimateVolume
#//
#//******************************************************************************

def estimateVolume( volume ):
    oneLiter = Measurement( 1, { 'liter' : 1 } )
    volumeInLiters = mpf( Measurement( volume.convertValue( oneLiter ), oneLiter.getUnits( ) ) )

    volumeKey = max( key for key in volumeTable if mpf( key ) < volumeInLiters )
    multiple = fdiv( volumeInLiters, mpf( volumeKey ) )

    return 'Approximately ' + nstr( multiple, 3 ) + ' times the volume of ' + volumeTable[ volumeKey ]


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
#//  convertToHMS
#//
#//******************************************************************************

def convertToHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToDHMS
#//
#//******************************************************************************

def convertToDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'day' : 1 } ), Measurement( 1, { 'hour' : 1 } ),
                              Measurement( 1, { 'minute' : 1 } ), Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToYDHMS
#//
#//******************************************************************************

def convertToYDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'year' : 1 } ), Measurement( 1, { 'day' : 1 } ),
                              Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertUnits
#//
#//******************************************************************************

def convertUnits( unit1, unit2 ):
    #print( )
    #print( 'unit1:', unit1.getTypes( ) )
    #print( 'unit2:', unit2.getTypes( ) )

    if isinstance( unit1, Measurement ):
        unit1 = unit1.getReduced( )
    else:
        raise ValueError( 'cannot convert non-measurements' )

    if isinstance( unit2, list ):
        return unit1.convertValue( unit2 )
    else:
        return Measurement( unit1.convertValue( unit2 ), unit2.getUnits( ),
                            unit2.getUnitName( ), unit2.getPluralUnitName( ) )


#//******************************************************************************
#//
#//  operatorAliases
#//
#//******************************************************************************

operatorAliases = {
    '!!'          : 'doublefac',
    '!'           : 'factorial',
    '%'           : 'modulo',
    '*'           : 'multiply',
    '**'          : 'power',
    '***'         : 'tetrate',
    '+'           : 'add',
    '-'           : 'subtract',
    '/'           : 'divide',
    '//'          : 'root',
    '1/x'         : 'reciprocal',
    'average'     : 'mean',
    'avg'         : 'mean',
    'bal'         : 'balanced',
    'bal?'        : 'balanced?',
    'bal_'        : 'balanced_',
    'bits'        : 'countbits',
    'cbrt'        : 'root3',
    'cc'          : 'cubic_centimeter',
    'ccube'       : 'centeredcube',
    'cdec'        : 'cdecagonal',
    'cdec?'       : 'cdecagonal?',
    'ceil'        : 'ceiling',
    'champ'       : 'champernowne',
    'chept'       : 'cheptagonal',
    'chept?'      : 'cheptagonal?',
    'chex'        : 'chexagonal',
    'chex?'       : 'chexagonal?',
    'cnon'        : 'cnonagonal',
    'cnon?'       : 'cnonagonal?',
    'coct'        : 'coctagonal',
    'coct?'       : 'coctagonal?',
    'cousin'      : 'cousinprime',
    'cousin?'     : 'cousinprime?',
    'cousin_'     : 'cousinprime_',
    'cpent'       : 'cpentagonal',
    'cpent?'      : 'cpentagonal?',
    'cpoly'       : 'cpolygonal',
    'cpoly?'      : 'cpolygonal?',
    'ctri'        : 'ctriangular',
    'ctri?'       : 'ctriangular?',
    'cuberoot'    : 'root3',
    'cube_root'   : 'root3',
    'dec'         : 'decagonal',
    'dec?'        : 'decagonal?',
    'divcount'    : 'countdiv',
    'fac'         : 'factorial',
    'fac2'        : 'doublefac',
    'fermi'       : 'femtometer',
    'fib'         : 'fibonacci',
    'frac'        : 'fraction',
    'gemmho'      : 'micromho',
    'geomrange'   : 'georange',
    'gigohm'      : 'gigaohm',
    'harm'        : 'harmonic',
    'hept'        : 'heptagonal',
    'hept?'       : 'heptagonal?',
    'hex'         : 'hexagonal',
    'hex?'        : 'hexagonal?',
    'hyper4'      : 'tetrate',
    'int'         : 'long',
    'int16'       : 'short',
    'int32'       : 'long',
    'int64'       : 'longlong',
    'int8'        : 'char',
    'inv'         : 'reciprocal',
    'isdiv'       : 'isdivisible',
    'issqr'       : 'issquare',
    'left'        : 'shiftleft',
    'linear'      : 'linearrecur',
    'log'         : 'ln',
    'maxint'      : 'maxlong',
    'maxint128'   : 'maxquadlong',
    'maxint16'    : 'maxshort',
    'maxint32'    : 'maxlong',
    'maxint64'    : 'maxlonglong',
    'maxint8'     : 'maxchar',
    'maxuint'     : 'maxulong',
    'maxuint128'  : 'maxuquadlong',
    'maxuint16'   : 'maxushort',
    'maxuint32'   : 'maxulong',
    'maxuint64'   : 'maxulonglong',
    'maxuint8'    : 'maxuchar',
    'mcg'         : 'microgram',
    'megaohm'     : 'megohm',
    'megalerg'    : 'megaerg',
    'minint'      : 'minlong',
    'minint128'   : 'minquadlong',
    'minint16'    : 'minshort',
    'minint32'    : 'minlong',
    'minint64'    : 'minlonglong',
    'minint8'     : 'minchar',
    'minuint'     : 'minulong',
    'minuint128'  : 'minuquadlong',
    'minuint16'   : 'minushort',
    'minuint32'   : 'minulong',
    'minuint64'   : 'minulonglong',
    'minuint8'    : 'minuchar',
    'mod'         : 'modulo',
    'mult'        : 'multiply',
    'neg'         : 'negative',
    'non'         : 'nonagonal',
    'non?'        : 'nonagonal?',
    'nonasq'      : 'nonasquare',
    'nonzeroes'   : 'nonzero',
    'oct'         : 'octagonal',
    'oct?'        : 'octagonal?',
    'p!'          : 'primorial',
    'pent'        : 'pentagonal',
    'pent?'       : 'pentagonal?',
    'poly'        : 'polygonal',
    'poly?'       : 'polygonal?',
    'prod'        : 'product',
    'pyr'         : 'pyramid',
    'quad'        : 'quadprime',
    'quad?'       : 'quadprime?',
    'quad_'       : 'quadprime_',
    'quint'       : 'quintprime',
    'quint?'      : 'quintprime?',
    'quint_'      : 'quintprime_',
    'rand'        : 'random',
    'right'       : 'shiftright',
    'safe'        : 'safeprime',
    'safe?'       : 'safeprime?',
    'sext'        : 'sextprime',
    'sext?'       : 'sextprime?',
    'sext_'       : 'sextprime_',
    'sexy'        : 'sexyprime',
    'sexy3'       : 'sexytriplet',
    'sexy3?'      : 'sexytriplet?',
    'sexy3_'      : 'sexytriplet_',
    'sexy4'       : 'sexyquad',
    'sexy4?'      : 'sexyquad?',
    'sexy4_'      : 'sexyquad_',
    'sexy?'       : 'sexyprime?',
    'sexy_'       : 'sexyprime',
    'sigma'       : 'microsecond',
    'sigmas'      : 'microsecond',
    'sophie'      : 'sophieprime',
    'sophie?'     : 'sophieprime?',
    'sqr'         : 'square',
    'sqrt'        : 'root2',
    'squareroot'  : 'root2',
    'square_root' : 'root2',
    'syl'         : 'sylvester',
    'tri'         : 'triangular',
    'tri?'        : 'triangular?',
    'triarea'     : 'trianglearea',
    'triplet'     : 'tripletprime',
    'triplet?'    : 'tripletprime?',
    'triplet_'    : 'tripletprime_',
    'twin'        : 'twinprime',
    'twin?'       : 'twinprime?',
    'twin_'       : 'twinprime_',
    'uint'        : 'ulong',
    'uint16'      : 'ushort',
    'uint32'      : 'ulong',
    'uint64'      : 'ulonglong',
    'uint8'       : 'uchar',
    'unsigned'    : 'uinteger',
    'woodall'     : 'riesel',
    'zeroes'      : 'zero',
    '^'           : 'power',
    '~'           : 'not',
}


#//******************************************************************************
#//
#//  modifiers are operators that directly modify the argument stack instead of
#//  just returning a value.
#//
#//  '[' and ']' are special arguments that change global state in order to
#//  create list operands.
#//
#//******************************************************************************

modifiers = {
    'dup'       : [ duplicateTerm, 2 ],
    'flatten'   : [ flatten, 1 ],
    'unlist'    : [ unlist, 1 ],
    '['         : [ incrementNestedListLevel, 0 ],
    ']'         : [ decrementNestedListLevel, 0 ],
}


#//******************************************************************************
#//
#//  listOperators are operators that handle whether or not an argument is a
#//  list themselves (because they require a list argument).  Unlike regular
#//  operators, we don't want listOperators permutated over each list element,
#//  and if we do for auxillary arguments, these operator handlers will do that
#//  themselves.
#//
#//******************************************************************************

listOperators = {
    'append'        : [ appendLists, 2 ],
    'altsign'       : [ alternateSigns, 1 ],
    'altsign2'      : [ alternateSigns2, 1 ],
    'altsum'        : [ getAlternatingSum, 1 ],
    'altsum2'       : [ getAlternatingSum2, 1 ],
    'base'          : [ interpretAsBase, 2 ],
    'cf'            : [ convertFromContinuedFraction, 1 ],
    'convert'       : [ convertUnits, 2 ],
    'count'         : [ countElements, 1 ],
    'diffs'         : [ getListDiffs, 1 ],
    'gcd'           : [ getGCD, 1 ],
    'interleave'    : [ interleave, 2 ],
    'intersection'  : [ makeIntersection, 2 ],
    'linearrecur'   : [ getNthLinearRecurrence, 3 ],
    'max'           : [ max, 1 ],
    'maxindex'      : [ getIndexOfMax, 1 ],
    'mean'          : [ lambda n: fdiv( fsum( n ), len( n ) ), 1 ],
    'min'           : [ min, 1 ],
    'minindex'      : [ getIndexOfMin, 1 ],
    'nonzero'       : [ lambda n: [ index for index, e in enumerate( n ) if e != 0 ], 1 ],
    'polyadd'       : [ addPolynomials, 2 ],
    'polymul'       : [ multiplyPolynomials, 2 ],
    'polyprod'      : [ multiplyListOfPolynomials, 1 ],
    'polysum'       : [ addListOfPolynomials, 1 ],
    'polyval'       : [ evaluatePolynomial, 2 ],
    'product'       : [ fprod, 1 ],
    'result'        : [ loadResult, 0 ],
    'solve'         : [ solvePolynomial, 1 ],
    'sort'          : [ sortAscending, 1 ],
    'sortdesc'      : [ sortDescending, 1 ],
    'stddev'        : [ getStandardDeviation, 1 ],
    'sum'           : [ sum, 1 ],
    'tounixtime'    : [ lambda i: datetime.datetime( *i ).timestamp( ), 1 ],
    'tower'         : [ calculatePowerTower, 1 ],
    'tower2'        : [ calculatePowerTower2, 1 ],
    'union'         : [ makeUnion, 2 ],
    'unique'        : [ getUniqueElements, 1 ],
    'unpack'        : [ unpackInteger, 2 ],
    'zero'          : [ lambda n: [ index for index, e in enumerate( n ) if e == 0 ], 1 ],
}


#//******************************************************************************
#//
#//  operators
#//
#//  Regular operators expect zero or more single values and if those arguments
#//  are lists, rpn will iterate calls to the operator handler for each element
#//  in the list.   Multiple lists for arguments are not permutated.  Instead,
#//  the operator handler is called for each element in the first list, along
#//  with the nth element of each other argument that is also a list.
#//
#//******************************************************************************

operators = {
    'abs'           : [ fabs, 1 ],
    'acos'          : [ lambda n: performTrigOperation( n, acos ), 1 ],
    'acosh'         : [ lambda n: performTrigOperation( n, acosh ), 1 ],
    'acot'          : [ lambda n: performTrigOperation( n, acot ), 1 ],
    'acoth'         : [ lambda n: performTrigOperation( n, acoth ), 1 ],
    'acsc'          : [ lambda n: performTrigOperation( n, acsc ), 1 ],
    'acsch'         : [ lambda n: performTrigOperation( n, acsch ), 1 ],
    'add'           : [ add, 2 ],
    'altfac'        : [ getNthAlternatingFactorial, 1 ],
    'and'           : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x & y ), 2 ],
    'apery'         : [ apery, 0 ],
    'aperynum'      : [ getNthAperyNumber, 1 ],
    'asec'          : [ lambda n: performTrigOperation( n, asec ), 1 ],
    'asech'         : [ lambda n: performTrigOperation( n, asech ), 1 ],
    'asin'          : [ lambda n: performTrigOperation( n, asin ), 1 ],
    'asinh'         : [ lambda n: performTrigOperation( n, asinh ), 1 ],
    'atan'          : [ lambda n: performTrigOperation( n, atan ), 1 ],
    'atanh'         : [ lambda n: performTrigOperation( n, atanh ), 1 ],
    'balanced'      : [ getNthBalancedPrime, 1 ],
    'balanced_'     : [ getNthBalancedPrimeList, 1 ],
    'bell'          : [ bell, 1 ],
    'bellpoly'      : [ bell, 2 ],
    'bernoulli'     : [ bernoulli, 1 ],
    'binomial'      : [ binomial, 2 ],
    'carol'         : [ lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1 ],
    'catalan'       : [ lambda n: fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) ), 1 ],
    'catalans'      : [ catalan, 0 ],
    'cdecagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 10 ), 1 ],
    'cdecagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 10 ), 1 ],
    'ceiling'       : [ ceil, 1 ],
    'centeredcube'  : [ getNthCenteredCubeNumber, 1 ],
    'champernowne'  : [ getChampernowne, 0 ],
    'char'          : [ lambda n: convertToSignedInt( n , 8 ), 1 ],
    'cheptagonal'   : [ lambda n: getCenteredPolygonalNumber( n, 7 ), 1 ],
    'cheptagonal?'  : [ lambda n: findCenteredPolygonalNumber( n, 7 ), 1 ],
    'chexagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 6 ), 1 ],
    'cnonagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 9 ), 1 ],
    'cnonagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 9 ), 1 ],
    'coctagonal'    : [ lambda n: getCenteredPolygonalNumber( n, 8 ), 1 ],
    'coctagonal?'   : [ lambda n: findCenteredPolygonalNumber( n, 8 ), 1 ],
    'copeland'      : [ getCopelandErdos, 0 ],
    'cos'           : [ lambda n: performTrigOperation( n, cos ), 1 ],
    'cosh'          : [ lambda n: performTrigOperation( n, cosh ), 1 ],
    'cot'           : [ lambda n: performTrigOperation( n, cot ), 1 ],
    'coth'          : [ lambda n: performTrigOperation( n, coth ), 1 ],
    'countbits'     : [ getBitCount, 1 ],
    'countdiv'      : [ getDivisorCount, 1 ],
    'cousinprime'   : [ getNthCousinPrime, 1 ],
    'cpentagonal'   : [ lambda n: getCenteredPolygonalNumber( n, 5 ), 1 ],
    'cpentagonal?'  : [ lambda n: findCenteredPolygonalNumber( n, 5 ), 1 ],
    'cpolygonal'    : [ lambda n, k: getCenteredPolygonalNumber( n, k ), 2 ],
    'cpolygonal?'   : [ lambda n, k: findCenteredPolygonalNumber( n, k ), 2 ],
    'csc'           : [ lambda n: performTrigOperation( n, csc ), 1 ],
    'csch'          : [ lambda n: performTrigOperation( n, csch ), 1 ],
    'csquare'       : [ lambda n: getCenteredPolygonalNumber( n, 4 ), 1 ],
    'csquare?'      : [ lambda n: findCenteredPolygonalNumber( n, 4 ), 1 ],
    'ctriangular'   : [ lambda n: getCenteredPolygonalNumber( n, 3 ), 1 ],
    'ctriangular?'  : [ lambda n: findCenteredPolygonalNumber( n, 3 ), 1 ],
    'cube'          : [ lambda n: exponentiate( n, 3 ), 1 ],
    'decagonal'     : [ lambda n: getNthPolygonalNumber( n, 10 ), 1 ],
    'decagonal?'    : [ lambda n: findNthPolygonalNumber( n, 10 ), 1 ],
    'delannoy'      : [ getNthDelannoyNumber, 1 ],
    'divide'        : [ divide, 2 ],
    'divisors'      : [ getDivisors, 1 ],
    'dhms'          : [ convertToDHMS, 1 ],
    'dms'           : [ convertToDMS, 1 ],
    'dodecahedral'  : [ lambda n : polyval( [ 9/2, -9/2, 1, 0 ], n ), 1 ],
    'double'        : [ lambda n : sum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( n ) ) ) ), 1 ],
    'doublebal'     : [ getNthDoubleBalancedPrime, 1 ],
    'doublebal_'    : [ getNthDoubleBalancedPrimeList, 1 ],
    'doublefac'     : [ fac2, 1 ],
    'e'             : [ e, 0 ],
    'egypt'         : [ getGreedyEgyptianFraction, 2 ],
    'element'       : [ getListElement, 2 ],
    'estimate'      : [ estimate, 1 ],
    'euler'         : [ euler, 0 ],
    'exp'           : [ exp, 1 ],
    'exp10'         : [ lambda n: power( 10, n ), 1 ],
    'expphi'        : [ lambda n: power( phi, n ), 1 ],
    'exprange'      : [ expandExponentialRange, 3 ],
    'factor'        : [ lambda i: getExpandedFactorList( factor( i ) ), 1 ],
    'factorial'     : [ fac, 1 ],
    'fibonacci'     : [ fib, 1 ],
    'float'         : [ lambda n : sum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( n ) ) ) ), 1 ],
    'floor'         : [ floor, 1 ],
    'fraction'      : [ interpretAsFraction, 2 ],
    'fromunixtime'  : [ lambda n: [ time.localtime( n ).tm_year, time.localtime( n ).tm_mon,
                                    time.localtime( n ).tm_mday, time.localtime( n ).tm_hour,
                                    time.localtime( n ).tm_min, time.localtime( n ).tm_sec ], 1 ],
    'gamma'         : [ gamma, 1 ],
    'georange'      : [ expandGeometricRange, 3 ],
    'glaisher'      : [ glaisher, 0 ],
    'harmonic'      : [ harmonic, 1 ],
    'heptagonal'    : [ lambda n: getNthPolygonalNumber( n, 7 ), 1 ],
    'heptagonal?'   : [ lambda n: findNthPolygonalNumber( n, 7 ), 1 ],
    'heptanacci'    : [ getNthHeptanacci, 1 ],
    'hepthex'       : [ getNthHeptagonalHexagonalNumber, 1 ],
    'heptpent'      : [ getNthHeptagonalPentagonalNumber, 1 ],
    'heptsquare'    : [ getNthHeptagonalSquareNumber, 1 ],
    'hepttri'       : [ getNthHeptagonalTriangularNumber, 1 ],
    'hexagonal'     : [ lambda n: getNthPolygonalNumber( n, 6 ), 1 ],
    'hexagonal?'    : [ lambda n: findNthPolygonalNumber( n, 6 ), 1 ],
    'hexanacci'     : [ getNthHexanacci, 1 ],
    'hexpent'       : [ getNthHexagonalPentagonalNumber, 1 ],
    'hms'           : [ convertToHMS, 1 ],
    'hyper4_2'      : [ tetrateLarge, 2 ],
    'hyperfac'      : [ hyperfac, 1 ],
    'hypot'         : [ hypot, 2 ],
    'i'             : [ makeImaginary, 1 ],
    'icosahedral'   : [ lambda n: polyval( [ 5/2, -5/2, 1, 0 ], n ), 1 ],
    'integer'       : [ convertToSignedInt, 2 ],
    'isdivisible'   : [ lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2 ],
    'isolated'      : [ getNthIsolatedPrime, 1 ],
    'isprime'       : [ lambda n: 1 if isPrime( n ) else 0, 1 ],
    'issquare'      : [ isSquare, 1 ],
    'itoi'          : [ lambda: exp( fmul( -0.5, pi ) ), 0 ],
    'jacobsthal'    : [ getNthJacobsthalNumber, 1 ],
    'khinchin'      : [ khinchin, 0 ],
    'kynea'         : [ lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1 ],
    'lah'           : [ lambda n, k: fdiv( fmul( binomial( n, k ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2 ],
    'lambertw'      : [ lambertw, 1 ],
    'leyland'       : [ lambda x, y : fadd( power( x, y ), power( y, x ) ), 2 ],
    'lgamma'        : [ loggamma, 1 ],
    'li'            : [ li, 1 ],
    'ln'            : [ ln, 1 ],
    'log10'         : [ log10, 1 ],
    'log2'          : [ lambda n: log( n, 2 ), 1 ],
    'logxy'         : [ log, 2 ],
    'long'          : [ lambda n: convertToSignedInt( n , 32 ), 1 ],
    'longlong'      : [ lambda n: convertToSignedInt( n , 64 ), 1 ],
    'lucas'         : [ getNthLucasNumber, 1 ],
    'makecf'        : [ lambda n, k: ContinuedFraction( n, maxterms=k, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2 ],
    'maxchar'       : [ lambda: ( 1 << 7 ) - 1, 0 ],
    'maxlong'       : [ lambda: ( 1 << 31 ) - 1, 0 ],
    'maxlonglong'   : [ lambda: ( 1 << 63 ) - 1, 0 ],
    'maxquadlong'   : [ lambda: ( 1 << 127 ) - 1, 0 ],
    'maxshort'      : [ lambda: ( 1 << 15 ) - 1, 0 ],
    'maxuchar'      : [ lambda: ( 1 << 8 ) - 1, 0 ],
    'maxulong'      : [ lambda: ( 1 << 32 ) - 1, 0 ],
    'maxulonglong'  : [ lambda: ( 1 << 64 ) - 1, 0 ],
    'maxuquadlong'  : [ lambda: ( 1 << 128 ) - 1, 0 ],
    'maxushort'     : [ lambda: ( 1 << 16 ) - 1, 0 ],
    'mertens'       : [ mertens, 0 ],
    'minchar'       : [ lambda: -( 1 << 7 ), 0 ],
    'minlong'       : [ lambda: -( 1 << 31 ), 0 ],
    'minlonglong'   : [ lambda: -( 1 << 63 ), 0 ],
    'minquadlong'   : [ lambda: -( 1 << 127 ), 0 ],
    'minshort'      : [ lambda: -( 1 << 15 ), 0 ],
    'minuchar'      : [ lambda: 0, 0 ],
    'minulong'      : [ lambda: 0, 0 ],
    'minulonglong'  : [ lambda: 0, 0 ],
    'minuquadlong'  : [ lambda: 0, 0 ],
    'minushort'     : [ lambda: 0, 0 ],
    'modulo'        : [ fmod, 2 ],
    'motzkin'       : [ getNthMotzkinNumber, 1 ],
    'multiply'      : [ multiply, 2 ],
    'narayana'      : [ lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2 ],
    'negative'      : [ fneg, 1 ],
    'nonagonal'     : [ lambda n: getNthPolygonalNumber( n, 9 ), 1 ],
    'nonagonal?'    : [ lambda n: findNthPolygonalNumber( n, 9 ), 1 ],
    'nonahept'      : [ getNthNonagonalHeptagonalNumber, 1 ],
    'nonahex'       : [ getNthNonagonalHexagonalNumber, 1 ],
    'nonaoct'       : [ getNthNonagonalOctagonalNumber, 1 ],
    'nonapent'      : [ getNthNonagonalPentagonalNumber, 1 ],
    'nonasquare'    : [ getNthNonagonalSquareNumber, 1 ],
    'nonatri'       : [ getNthNonagonalTriangularNumber, 1 ],
    'not'           : [ getInvertedBits, 1 ],
    'nspherearea'   : [ getNSphereSurfaceArea, 2 ],
    'nsphereradius' : [ getNSphereRadius, 2 ],
    'nspherevolume' : [ getNSphereVolume, 2 ],
    'nthprime?'     : [ lambda i: findPrime( i )[ 0 ], 1 ],
    'nthquad?'      : [ lambda i: findQuadrupletPrimes( i )[ 0 ], 1 ],
    'octagonal'     : [ lambda n: getNthPolygonalNumber( n, 8 ), 1 ],
    'octagonal?'    : [ lambda n: findNthPolygonalNumber( n, 8 ), 1 ],
    'octahedral'    : [ lambda n: polyval( [ 2/3, 0, 1/3, 0 ], n ), 1 ],
    'octhept'       : [ getNthOctagonalHeptagonalNumber, 1 ],
    'octhex'        : [ getNthOctagonalHexagonalNumber, 1 ],
    'octpent'       : [ getNthOctagonalPentagonalNumber, 1 ],
    'octsquare'     : [ getNthOctagonalSquareNumber, 1 ],
    'octtri'        : [ getNthOctagonalTriangularNumber, 1 ],
    'oeis'          : [ lambda n: downloadOEISSequence( int( n ) ), 1 ],
    'oeiscomment'   : [ lambda n: downloadOEISText( int( n ), 'C', True ), 1 ],
    'oeisex'        : [ lambda n: downloadOEISText( int( n ), 'E', True ), 1 ],
    'oeisname'      : [ lambda n: downloadOEISText( int( n ), 'N', True ), 1 ],
    'omega'         : [ lambda: lambertw( 1 ), 0 ],
    'or'            : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2 ],
    'padovan'       : [ getNthPadovanNumber, 1 ],
    'parity'        : [ lambda n : getBitCount( n ) & 1, 1 ],
    'pascal'        : [ getNthPascalLine, 1 ],
    'pell'          : [ getNthPellNumber, 1 ],
    'pentagonal'    : [ lambda n: getNthPolygonalNumber( n, 5 ), 1 ],
    'pentagonal?'   : [ lambda n: findNthPolygonalNumber( n, 5 ), 1 ],
    'pentanacci'    : [ getNthPentanacci, 1 ],
    'pentatope'     : [ getNthPentatopeNumber, 1 ],
    'perm'          : [ getPermutations, 2 ],
    'phi'           : [ phi, 0 ],
    'pi'            : [ pi, 0 ],
    'plastic'       : [ getPlasticConstant, 0 ],
    'polyarea'      : [ getRegularPolygonArea, 1 ],
    'polygamma'     : [ psi, 2 ],
    'polygonal'     : [ getNthPolygonalNumber, 2 ],
    'polygonal?'    : [ findNthPolygonalNumber, 2 ],
    'polylog'       : [ polylog, 2 ],
    'polyprime'     : [ getNthPolyPrime, 2 ],
    'polytope'      : [ getNthPolytopeNumber, 2 ],
    'power'         : [ exponentiate, 2 ],
    'prime'         : [ getNthPrime, 1 ],
    'prime?'        : [ lambda n: findPrime( n )[ 1 ], 1 ],
    'primepi'       : [ getPrimePi, 1 ],
    'primes'        : [ getPrimes, 2 ],
    'primorial'     : [ getPrimorial, 1 ],
    'pyramid'       : [ lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1 ],
    'quadprime'     : [ getNthQuadrupletPrime, 1 ],
    'quadprime?'    : [ lambda i: findQuadrupletPrimes( i )[ 1 ], 1 ],
    'quadprime_'    : [ getNthQuadrupletPrimeList, 1 ],
    'quintprime'    : [ getNthQuintupletPrime, 1 ],
    'quintprime_'   : [ getNthQuintupletPrimeList, 1 ],
    'random'        : [ rand, 0 ],
    'range'         : [ expandRange, 2 ],
    'range2'        : [ expandSteppedRange, 3 ],
    'reciprocal'    : [ takeReciprocal, 1 ],
    'repunit'       : [ getNthBaseKRepunit, 2 ],
    'rhombdodec'    : [ getNthRhombicDodecahedralNumber, 1 ],
    'riesel'        : [ lambda n: fsub( fmul( n, power( 2, n ) ), 1 ), 1 ],
    'root'          : [ root, 2 ],
    'root2'         : [ sqrt, 1 ],
    'root3'         : [ cbrt, 1 ],
    'round'         : [ lambda n: floor( fadd( n, 0.5 ) ), 1 ],
    'safeprime'     : [ lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1 ],
    'schroeder'     : [ getNthSchroederNumber, 1 ],
    'score'         : [ lambda: mpf( '20' ), 0 ],
    'sec'           : [ lambda n: performTrigOperation( n, sec ), 1 ],
    'sech'          : [ lambda n: performTrigOperation( n, sech ), 1 ],
    'sextprime'     : [ getNthSextupletPrime, 1 ],
    'sextprime_'    : [ getNthSextupletPrimeList, 1 ],
    'sexyprime'     : [ getNthSexyPrime, 1 ],
    'sexyprime_'    : [ getNthSexyPrimeList, 1 ],
    'sexyquad'      : [ getNthSexyQuadruplet, 1 ],
    'sexyquad_'     : [ getNthSexyQuadrupletList, 1 ],
    'sexytriplet'   : [ getNthSexyTriplet, 1 ],
    'sexytriplet_'  : [ getNthSexyTripletList, 1 ],
    'shiftleft'     : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2 ],
    'shiftright'    : [ lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2 ],
    'short'         : [ lambda n: convertToSignedInt( n , 16 ), 1 ],
    'sin'           : [ lambda n: performTrigOperation( n, sin ), 1 ],
    'sinh'          : [ lambda n: performTrigOperation( n, sinh ), 1 ],
    'solve2'        : [ solveQuadraticPolynomial, 3 ],
    'solve3'        : [ solveCubicPolynomial, 4 ],
    'solve4'        : [ solveQuarticPolynomial, 5 ],
    'sophieprime'   : [ getNthSophiePrime, 1 ],
    'spherearea'    : [ lambda n: getNSphereSurfaceArea( 3, n ), 1 ],
    'sphereradius'  : [ lambda n: getNSphereRadius( 3, n ), 1 ],
    'spherevolume'  : [ lambda n: getNSphereVolume( 3, n ), 1 ],
    'square'        : [ lambda i: exponentiate( i, 2 ), 1 ],
    'squaretri'     : [ getNthSquareTriangularNumber, 1 ],
    'steloct'       : [ getNthStellaOctangulaNumber, 1 ],
    'subfac'        : [ lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1 ],
    'subtract'      : [ subtract, 2 ],
    'superfac'      : [ superfac, 1 ],
    'superprime'    : [ getNthSuperPrime, 1 ],
    'sylvester'     : [ getNthSylvester, 1 ],
    'tan'           : [ lambda n: performTrigOperation( n, tan ), 1 ],
    'tanh'          : [ lambda n: performTrigOperation( n, tanh ), 1 ],
    'tetrahedral'   : [ lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ), 1 ],
    'tetranacci'    : [ getNthTetranacci, 1 ],
    'tetrate'       : [ tetrate, 2 ],
    'thabit'        : [ lambda n : fsub( fmul( 3, power( 2, n ) ), 1 ), 1 ],
    'trianglearea'  : [ getTriangleArea, 3 ],
    'triangular'    : [ lambda n : getNthPolygonalNumber( n, 3 ), 1 ],
    'triangular?'   : [ lambda n : findNthPolygonalNumber( n, 3 ), 1 ],
    'tribonacci'    : [ getNthTribonacci, 1 ],
    'triplebal'     : [ getNthTripleBalancedPrime, 1 ],
    'triplebal_'    : [ getNthTripleBalancedPrimeList, 1 ],
    'tripletprime'  : [ getNthTripletPrime, 1 ],
    'tripletprime'  : [ getNthTripletPrimeList, 1 ],
    'truncoct'      : [ getNthTruncatedOctahedralNumber, 1 ],
    'trunctet'      : [ getNthTruncatedTetrahedralNumber, 1 ],
    'twinprime'     : [ getNthTwinPrime, 1 ],
    'twinprime_'    : [ getNthTwinPrimeList, 1 ],
    'uchar'         : [ lambda n: int( fmod( n, power( 2, 8 ) ) ), 1 ],
    'uinteger'      : [ lambda n, k: int( fmod( n, power( 2, k ) ) ), 2 ],
    'ulong'         : [ lambda n: int( fmod( n, power( 2, 32 ) ) ), 1 ],
    'ulonglong'     : [ lambda n: int( fmod( n, power( 2, 64 ) ) ), 1 ],
    'unitroots'     : [ lambda i: unitroots( int( i ) ), 1 ],
    'ushort'        : [ lambda n: int( fmod( n, power( 2, 16 ) ) ), 1 ],
    'xor'           : [ lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2 ],
    'ydhms'         : [ convertToYDHMS, 1 ],
    'zeta'          : [ zeta, 1 ],
    '_dumpalias'    : [ dumpAliases, 0 ],
    '_dumpops'      : [ dumpOperators, 0 ],
    '_stats'        : [ dumpStats, 0 ],
    '~'             : [ getInvertedBits, 1 ],
#   'antitet'       : [ findTetrahedralNumber, 1 ],
#   'bernfrac'      : [ bernfrac, 1 ],
#   'powmod'        : [ getPowMod, 3 ],
}


#//******************************************************************************
#//
#//  parseInputValue
#//
#//  Parse out a numerical expression and attempt to set the precision to an
#//  appropriate value based on the expression.
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
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

    strResult = '';

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
    resultString = ''

    for item in result:
        if resultString == '':
            resultString = '[ '
        else:
            resultString += ', '

        if isinstance( item, list ):
            resultString += formatListOutput( item, radix, numerals, integerGrouping, integerDelimiter,
                                              leadingZero, decimalGrouping, decimalDelimiter, baseAsDigits,
                                              outputAccuracy )
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

        if value < mpf( -1.0 ) or value >mpf( 1.0 ):
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

        #print( unit, exponent )

        if exponent > 0:
            if unitString != '':
                unitString += ' '

            if value == 1:
                unitString += unit
            else:
                unitString += unitOperators[ unit ].plural

            if exponent > 1:
                unitString += '^' + str( exponent )

    negativeUnits = ''

    if unitString == '':
        for unit in units:
            exponent = units[ unit ]

            if exponent < 0:
                if negativeUnits != '':
                    negativeUnits += ' '

                negativeUnits += unit
                negativeUnits += '^' + str( exponent )
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
                    negativeUnits += '^' + str( exponent )
                elif exponent < -1:
                    negativeUnits += '^' + str( -exponent )

    result = ''

    for c in unitString + negativeUnits:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#//******************************************************************************
#//
#//  printParagraph
#//
#//******************************************************************************

def printParagraph( text, length = 79, indent = 0 ):
    lines = textwrap.wrap( text, length )

    for line in lines:
        print( ' ' * indent + line )


#//******************************************************************************
#//
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( basicCategories, operatorCategories ):
    print( PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )
    printParagraph(
'''For help on a specific topic, add a help topic, operator category or a specific operator name.  Adding
'example', or 'ex' after an operator name will result in examples of use being printed as well.''' )
    print( )
    print( 'The following is a list of general topics:' )
    print( )

    printParagraph( ', '.join( sorted( basicCategories ) ), 75, 4 )

    print( )
    print( 'The following is a list of operator categories:' )
    print( )

    printParagraph( ', '.join( sorted( operatorCategories ) ), 75, 4 )


#//******************************************************************************
#//
#//  printTitleScreen
#//
#//******************************************************************************

def printTitleScreen( ):
    print( PROGRAM_NAME, PROGRAM_VERSION, '-', PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )
    print( 'For more information use, \'rpn help\'.' )


#//******************************************************************************
#//
#//  printOperatorHelp
#//
#//******************************************************************************

def printOperatorHelp( helpArgs, term, operatorInfo, operatorHelp ):
    if operatorInfo[ 1 ] == 1:
        print( 'n ', end='' )
    elif operatorInfo[ 1 ] == 2:
        print( 'n k ', end='' )
    elif operatorInfo[ 1 ] == 3:
        print( 'a b c ', end='' )
    elif operatorInfo[ 1 ] == 4:
        print( 'a b c d ', end='' )
    elif operatorInfo[ 1 ] == 5:
        print( 'a b c d e ', end='' )

    aliasList = [ key for key in operatorAliases if term == operatorAliases[ key ] ]

    print( term + ' - ' + operatorHelp[ 1 ] )

    print( )

    if len( aliasList ) > 1:
        print( 'aliases:  ' + ', '.join( aliasList ) )
    elif len( aliasList ) == 1:
        print( 'alias:  ' + aliasList[ 0 ] )

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

def addAliases( operatorList ):
    for index, operator in enumerate( operatorList ):
        aliasList = [ key for key in operatorAliases if operator == operatorAliases[ key ] ]

        if len( aliasList ) > 0:
            operatorList[ index ] += ' (' + ', '.join( aliasList ) + ')'


#//******************************************************************************
#//
#//  printHelp
#//
#//******************************************************************************

def printHelp( helpArgs ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            helpVersion = pickle.load( pickleFile )
            basicCategories = pickle.load( pickleFile )
            operatorHelp = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to help file.  Help will be unavailable.' )
        return

    if helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    operatorCategories = set( operatorHelp[ key ][ 0 ] for key in operatorHelp )

    if len( helpArgs ) == 0:
        printGeneralHelp( basicCategories, operatorCategories )
        return

    term = helpArgs[ 0 ]

    if term in operatorAliases:
        term = operatorAliases[ term ]

    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ], operatorHelp[ term ] )

    if term in listOperators:
        printOperatorHelp( helpArgs, term, listOperators[ term ], operatorHelp[ term ] )

    if term in modifiers:
        printOperatorHelp( helpArgs, term, modifiers[ term ], operatorHelp[ term ] )

    if term in basicCategories:
        print( basicCategories[ term ] )

    if term in operatorCategories:
        print( )
        print( 'The ' + term + ' category includes the following operators (with aliases in' )
        print( 'parentheses):' )
        print( )

        operatorList = [ key for key in operators if operatorHelp[ key ][ 0 ] == term ]
        operatorList.extend( [ key for key in listOperators if operatorHelp[ key ][ 0 ] == term ] )
        operatorList.extend( [ key for key in modifiers if operatorHelp[ key ][ 0 ] == term ] )

        addAliases( operatorList )

        printParagraph( ', '.join( sorted( operatorList ) ), 75, 4 )


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
#//  loadUnitConversionMatrix
#//
#//******************************************************************************

def loadUnitConversionMatrix( ):
    global unitConversionMatrix

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) as pickleFile:
            unitConversionMatrix = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit conversion matrix data.  Unit conversion will be unavailable.' )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global addToListArgument
    global bitwiseGroupSize
    global dataPath
    global inputRadix
    global nestedListLevel
    global numerals
    global updateDicts

    global unitOperators
    global basicUnitTypes
    global unitConversionMatrix
    global specialUnitConversionMatrix
    global compoundUnits

    global massTable
    global lengthTable
    global volumeTable

    global balancedPrimes
    global cousinPrimes
    global doubleBalancedPrimes
    global isolatedPrimes
    global largePrimes
    global quadPrimes
    global quintPrimes
    global sextPrimes
    global sexyPrimes
    global sexyQuadruplets
    global sexyTriplets
    global smallPrimes
    global sophiePrimes
    global superPrimes
    global tripleBalancedPrimes
    global tripletPrimes
    global twinPrimes

    # initialize globals
    nestedListLevel = 0

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )

    help = False
    helpArgs = [ ]

    for i in range( 0, len( sys.argv ) ):
        if sys.argv[ i ] == 'help':
            help = True
        else:
            if help:
                helpArgs.append( sys.argv[ i ] )

    if help:
        printHelp( helpArgs )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=defaultAccuracy, # -1
                         const=defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--identify', action='store_true' )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0 )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-u', '--find_poly', nargs='?', type=int, action='store', default=0, const=1000 )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store',
                         default=defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    if len( sys.argv ) == 1:
        printTitleScreen( )
        return

    args = parser.parse_args( )

    if args.help or args.other_help:
        printHelp( [ ] )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

    mp.dps = args.precision

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -n
    numerals = args.numerals

    # handle -b
    inputRadix = int( args.input_radix )

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return

    # handle -x
    if args.hex:
        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        bitwiseGroupSize = 9

    # handle -R
    if args.output_radix_numerals > 0:
        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( 'rpn:  output radix must be from 2 to 62, or phi' )
            return

    # handle -y and -u:  mpmath wants precision of at least 53 for these functions
    if args.identify or args.find_poly > 0:
        if mp.dps < 53:
            mp.dps = 53

    index = 1                 # only used for error messages
    valueList = list( )

    if args.print_options:
        print( '--output_accuracy:  %d' % args.output_accuracy )
        print( '--input_radix:  %d'% inputRadix )
        print( '--comma:  ' + ( 'true' if args.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % args.decimal_grouping )
        print( '--integer_grouping:  %d' % integerGrouping )
        print( '--numerals:  ' + args.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % args.output_radix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--time:  ' + ( 'true' if args.time else 'false' ) )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

    if len( args.terms ) == 0:
        print( 'rpn:  no terms found' )
        return

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            unitsVersion = pickle.load( pickleFile )
            basicUnitTypes = pickle.load( pickleFile )
            unitOperators = pickle.load( pickleFile )
            operatorAliases.update( pickle.load( pickleFile ) )
            compoundUnits = pickle.load( pickleFile )
            massTable = pickle.load( pickleFile )
            lengthTable = pickle.load( pickleFile )
            volumeTable = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.' )

    if unitsVersion != PROGRAM_VERSION:
        print( 'rpn  units data file version mismatch' )

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        if term in operatorAliases:
            term = operatorAliases[ term ]

        currentValueList = getCurrentArgList( valueList )

        if term in modifiers:
            try:
                modifiers[ term ][ 0 ]( currentValueList )
            except IndexError as error:
                print( 'rpn:  index error for operator at arg ' + format( index ) +
                       '.  Are your arguments in the right order?' )
                break
        elif term in unitOperators:
            if len( currentValueList ) == 0 or isinstance( currentValueList[ -1 ], Measurement ):
                if unitOperators[ term ].unitType == 'constant':
                    value = mpf( Measurement( 1, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                else:
                    value = Measurement( 1, term, unitOperators[ term ].representation, unitOperators[ term ].plural )

                currentValueList.append( value )
            elif isinstance( currentValueList[ -1 ], list ):
                argList = currentValueList.pop( )

                for listItem in argList:
                    if unitOperators[ term ].unitType == 'constant':
                        value = mpf( Measurement( listItem, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                    else:
                        value = Measurement( listItem, term, unitOperators[ term ].representation, unitOperators[ term ].plural )

                    currentValueList.append( value )
            else:
                if unitOperators[ term ].unitType == 'constant':
                    value = mpf( Measurement( currentValueList.pop( ), term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
                else:
                    value = Measurement( currentValueList.pop( ), term, unitOperators[ term ].representation, unitOperators[ term ].plural )

                currentValueList.append( value )
        elif term in operators:
            argsNeeded = operators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    result = callers[ 0 ]( operators[ term ][ 0 ], None )
                else:
                    argList = list( )

                    for i in range( 0, argsNeeded ):
                        arg = currentValueList.pop( )
                        argList.append( arg if isinstance( arg, list ) else [ arg ] )

                    result = callers[ argsNeeded ]( operators[ term ][ 0 ], *argList )

                if len( result ) == 1:
                    result = result[ 0 ]

                currentValueList.append( result )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
        elif term in listOperators:
            argsNeeded = listOperators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator ' + term + ' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    currentValueList.append( listOperators[ term ][ 0 ]( currentValueList ) )
                elif argsNeeded == 1:
                    currentValueList.append( evaluateOneListFunction( listOperators[ term ][ 0 ], currentValueList.pop( ) ) )
                else:
                    listArgs = [ ]

                    for i in range( 0, argsNeeded ):
                        listArgs.insert( 0, currentValueList.pop( ) )

                    currentValueList.append( listOperators[ term ][ 0 ]( *listArgs ) )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except IndexError as error:
                print( 'rpn:  index error for operator at arg ' + format( index ) +
                       '.  Are your arguments in the right order?' )
                break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
        else:
            try:
                currentValueList.append( parseInputValue( term, inputRadix ) )
            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                currentValueList.append( term )
                print( 'rpn:  error in arg ' + format( index ) +
                       ':  unrecognized argument: \'%s\'' % sys.argv[ index ] )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if len( valueList ) > 1 or len( valueList ) == 0:
            print( 'rpn:  unexpected end of input' )
        else:
            mp.pretty = True
            result = valueList.pop( )

            if args.comma:
                integerGrouping = 3     # override whatever was set on the command-line
                leadingZero = False     # this one, too
                integerDelimiter = ','
            else:
                integerDelimiter = ' '

            if isinstance( result, list ):
                print( formatListOutput( result, outputRadix, numerals, integerGrouping, integerDelimiter,
                                         leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                         args.output_accuracy ) )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                outputString = formatOutput( resultString, outputRadix, numerals, integerGrouping,
                                             integerDelimiter, leadingZero, args.decimal_grouping,
                                             ' ', baseAsDigits, args.output_accuracy )

                # handle the units if we are display a measurement
                if isinstance( result, Measurement ):
                    outputString += ' ' + formatUnits( result )

                print( outputString )

                # handle --identify
                if args.identify:
                    formula = identify( result )

                    if formula is None:
                        base = [ 'pi', 'e' ]
                        formula = identify( result, base )

                    # I don't know if this would ever be useful to try.
                    #if formula is None:
                    #    base.extend( [ 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' ] )
                    #    formula = identify( result, base )
                    #
                    # Nor this.
                    #if formula is None:
                    #    base.extend( [ 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' ] )
                    #    formula = identify( result, base )

                    if formula is None:
                        print( '    = [formula cannot be found]' )
                    else:
                        print( '    = ' + formula )

                # handle --find_poly
                if args.find_poly > 0:
                    poly = str( findpoly( result, args.find_poly ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000, tol=1e-10 ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )

            saveResult( result )

        if args.time:
            print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    # print( parseUnitString( 'meter' ) )
    # print( parseUnitString( 'meter^2' ) )
    # print( parseUnitString( 'meter/second' ) )
    # print( parseUnitString( 'meter*second' ) )
    # print( parseUnitString( 'meter*meter' ) )
    # print( parseUnitString( 'meter/meter' ) )
    # print( parseUnitString( 'meter^2*fred/second^3' ) )

    main( )

