#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUnitClasses.py
# //
# //  RPN command-line calculator, unit class declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools

from mpmath import fdiv, mpmathify

from rpn.rpnPersistence import loadUnitConversionMatrix, loadUnitData
from rpn.rpnUtils import debugPrint

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getUnitDimensions
# //
# //******************************************************************************

def getUnitDimensions( unit ):
    if unit in g.basicUnitTypes:
        return unit

    return RPNUnits( g.basicUnitTypes[ g.unitOperators[ unit ].unitType ].dimensions )


# //******************************************************************************
# //
# //  getUnitDimensionList
# //
# //******************************************************************************

def getUnitDimensionList( unit ):
    if unit in g.basicUnitTypes:
        return [ unit ]

    dimensions = getUnitDimensions( unit )

    numerator = [ ]
    denominator = [ ]

    for dimension in dimensions:
        if dimensions[ dimension ] > 0:
            for i in range( dimensions[ dimension ] ):
                numerator.append( dimension )
        else:
            for i in range( dimensions[ dimension ] * -1 ):
                denominator.append( dimension )

    return numerator, denominator


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
        if unit == '1':
            return '_null_type'
        else:
            raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


# //******************************************************************************
# //
# //  class RPNUnitTypeInfo
# //
# //******************************************************************************

class RPNUnitTypeInfo( object ):
    '''This class defines the information needed to define a measurement unit type.'''
    def __init__( self, dimensions, baseUnit, primitiveUnit, estimateTable ):
        self.dimensions = RPNUnits( dimensions )
        self.baseUnitType = RPNUnits( baseUnit )
        self.baseUnit = baseUnit
        self.primitiveUnit = primitiveUnit
        self.estimateTable = estimateTable


# //******************************************************************************
# //
# //  class RPNConstantInfo
# //
# //******************************************************************************

class RPNConstantInfo( object ):
    '''This class defines the information needed to define a constant.'''
    def __init__( self, value, unit, aliases, multipliable, description = '', helpText = '' ):
        self.value = value
        self.unit = unit
        self.aliases = aliases
        self.multipliable = multipliable
        self.description = description
        self.helpText = helpText


# //******************************************************************************
# //
# //  class RPNUnitInfo
# //
# //******************************************************************************

class RPNUnitInfo( object ):
    '''This class defines the information needed to define a unit of measurement.'''
    def __init__( self, unitType, representation, plural, abbrev, aliases, categories,
                  helpText = '', autoGenerated = False ):
        self.unitType = unitType
        self.representation = representation
        self.plural = plural
        self.abbrev = abbrev
        self.aliases = aliases
        self.categories = categories
        self.helpText = helpText
        self.autoGenerated = autoGenerated


# //******************************************************************************
# //
# //  class RPNUnits
# //
# //******************************************************************************

class RPNUnits( collections.Counter ):
    '''This class represents a unit of measurement.'''
    def __init__( self, *arg, **kw ):
        if ( len( arg ) == 1 ):
            if isinstance( arg[ 0 ], str ):
                self.update( RPNUnits.parseUnitString( arg[ 0 ] ) )
            elif isinstance( arg[ 0 ], ( list, tuple ) ):
                for item in arg[ 0 ]:
                    self.update( item )  # for Counter, update( ) adds, not replaces
            elif isinstance( arg[ 0 ], ( RPNUnits, dict ) ):
                self.update( arg[ 0 ] )
            else:
                raise ValueError( 'invalid call to RPNUnits constructor' )
        else:
            super( RPNUnits, self ).__init__( *arg, **kw )

    def __eq__( self, other ):
        for i in self:
            if i in other:
                if self[ i ] != other[ i ]:
                    return False;
            else:
                return False;

        for i in other:
            if i in self:
                if other[ i ] != self[ i ]:
                    return False;
            else:
                return False;

        return True

    def invert( self ):
        '''Inverts the units by reversing the signs of their exponents.'''
        for unit in self:
            self[ unit ] = -( self[ unit ] )

        return self

    def inverted( self ):
        '''Returns a new RPNUnits object with the units inverted.'''
        result = RPNUnits( self )
        result.invert( )
        return result

    def combineUnits( self, units ):
        if not g.unitConversionMatrix:
            loadUnitConversionMatrix( )

        newUnits = RPNUnits( self )

        factor = mpmathify( 1 )

        for unit2 in units:
            if unit2 in newUnits:
                newUnits[ unit2 ] += units[ unit2 ]
            else:
                for unit1 in self:
                    if unit1 == unit2:
                        newUnits[ unit2 ] += units[ unit2 ]
                        break
                    elif getUnitType( unit1 ) == getUnitType( unit2 ):
                        factor = fdiv( factor, pow( mpmathify( g.unitConversionMatrix[ ( unit1, unit2 ) ] ), units[ unit2 ] ) )
                        newUnits[ unit1 ] += units[ unit2 ]
                        break
                else:
                    newUnits[ unit2 ] = units[ unit2 ]

        #print( 'newUnits', newUnits )
        return factor, newUnits

    def getUnitTypes( self ):
        types = RPNUnits( )

        for unit in self:
            if unit in g.basicUnitTypes:
                unitType = unit
            else:
                if unit not in g.unitOperators:
                    raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

                unitType = g.unitOperators[ unit ].unitType

            if unitType in types:
                types[ unitType ] += self[ unit ]
            else:
                types[ unitType ] = self[ unit ]

        return types

    def doDimensionsCancel( self ):
        totalDimensions = RPNUnits( )

        for unit in self:
            dimensions = getUnitDimensions( unit )

            for dimension in dimensions:
                if dimension in totalDimensions:
                    if ( ( dimensions[ dimension ] * self[ unit ] ) > 0 ) != ( totalDimensions[ dimension ] > 0 ):
                        return True

            totalDimensions.update( dimensions )

        return False

    def getDimensions( self ):
        result = RPNUnits( )

        for unit in self:
            if unit == '1':
                continue

            dimensions = getUnitDimensions( unit )

            exponent = self.get( unit )

            if exponent != 1:   # handle exponent
                for unit2 in dimensions:
                    dimensions[ unit2 ] *= exponent

            result.update( dimensions )

        # It's possible to end up with a dimension with exponent 0 due to something dividing out,
        # so we need to clean those out.
        old_result = dict( result )

        for unit in old_result:
            if result[ unit ] == 0:
                del result[ unit ]
            elif unit == '1':
                del result[ unit ]

        return result

    def getUnitString( self ):
        '''Returns a string with the algebraic representation of the units.'''
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

        if resultString == '':
            resultString = '1'

        if denominator != '':
            resultString += '/' + denominator

        return resultString

    @staticmethod
    def parseUnitString( expression ):
        '''Parses a string with the algebraic representation of the units and populates
        the RPNUnits object (self) with the parsed unit values.'''

        result = RPNUnits( )

        # no point in trying to parse an empty string
        if not expression:
            return result

        pieces = expression.split( '/' )

        if len( pieces ) > 2:
            raise ValueError( 'only one \'/\' is permitted' )
        elif len( pieces ) == 2:
            result = RPNUnits.parseUnitString( pieces[ 0 ] )
            result.subtract( RPNUnits.parseUnitString( pieces[ 1 ] ) )

            return result.normalizeUnits( )
        else:
            units = expression.split( '*' )

            for unit in units:
                if unit == '1':
                    continue

                if unit == '':
                    raise ValueError( 'wasn\'t expecting another \'*\' in \'' + expression + '\'' )

                operands = unit.split( '^' )

                plainUnit = operands[ 0 ]

                if plainUnit not in g.unitOperators and plainUnit in g.operatorAliases:
                    plainUnit = g.operatorAliases[ plainUnit ]

                operandCount = len( operands )

                exponent = 1

                if operandCount > 1:
                    for i in range( 1, operandCount ):
                        exponent *= int( operands[ i ] )

                result[ plainUnit ] += exponent

            return result.normalizeUnits( )

    def normalizeUnits( self, value = 0 ):
        newUnits = RPNUnits( )

        # strip out '_null_type' and units with and exponent of 0
        for unit in self:
            # mpf's keep slipping in here
            self[ unit ] = int( self[ unit ] )

            if self[ unit ] != 0 and unit != '_null_type':
                newUnits[ unit ] = self[ unit ]

        return newUnits

    def splitUnits( self ):
        numerator = RPNUnits( )
        denominator = RPNUnits( )

        for unit in self:
            if self[ unit ] > 0:
                numerator[ unit ] = self[ unit ]
            else:
                denominator[ unit ] = self[ unit ] * -1

        return numerator, denominator

