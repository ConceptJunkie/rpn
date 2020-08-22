#!/usr/bin/env python

#******************************************************************************
#
#  rpnOperator.py
#
#  rpnChilada operator class definitions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import random

from enum import Enum

from mpmath import exp, fadd, fmul, floor, im, nan, nstr

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnLocation import RPNLocation
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnSpecial import getRandomInteger, getRandomNumber
from rpn.rpnUtils import abortArgsNeeded
from rpn.rpnValidator import RPNValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  generateDefaultArgument
#
#******************************************************************************

def generateDefaultArgument( ):
    return 'argument'


#******************************************************************************
#
#  generateRealArgument
#
#  for real numbers we are treating the range as logarithms
#
#******************************************************************************

def generateRealArgument( range = None, allowNegative = True ):
    if range is None:
        range = [ 0, 10 ]

    factor = 1

    if allowNegative and getRandomInteger( 2 ) == 1:
        factor = -1

    return nstr( fmul( exp( fmul( getRandomNumber( ), random.uniform( *range ) ) ), factor ) )


#******************************************************************************
#
#  generateNonnegativeRealArgument
#
#******************************************************************************

def generateNonnegativeRealArgument( range ):
    return generateRealArgument( range, allowNegative=False )


def generateIntegerArgument( range = None, allowNegative=True ):
    if range is None:
        range = [ 0, 1_000_000_000 ]

    factor = 1

    if allowNegative and getRandomInteger( 2 ) == 1:
        factor = -1

    return str( fmul( fadd( getRandomInteger( range[ 1 ] ), range[ 0 ] ), factor ) )


def generatePositiveIntegerArgument( range=None ):
    if range is None:
        range = [ 1, 1_000_000_000 ]

    return generateIntegerArgument( range, allowNegative=False )


def generateNonnegativeIntegerArgument( range=None ):
    if range is None:
        range = [ 0, 1_000_000_000 ]

    return generateIntegerArgument( range, allowNegative=False )


def generatePrimeArgument( ):
    return 'argument'


def generateStringArgument( ):
    return 'argument'


def generateDateTimeArgument( ):
    return 'argument'


def generateLocationArgument( ):
    return 'argument'


def generateBooleanArgument( ):
    return 'argument'


def generateMeasurementArgument( ):
    return 'argument'


def generateAstronomicalObjectArgument( ):
    return 'argument'


def generateListArgument( ):
    return 'argument'


def generateGeneratorArgument( ):
    return 'argument'


def generateFunctionArgument( ):
    return 'argument'


#******************************************************************************
#
#  argumentGenerators dict
#
#******************************************************************************

argumentGenerators = {
    RPNValidator.Default             : generateDefaultArgument,
    RPNValidator.Real                : generateRealArgument,
    RPNValidator.NonnegativeReal     : generateNonnegativeRealArgument,
    RPNValidator.Integer             : generateIntegerArgument,
    RPNValidator.PositiveInteger     : generatePositiveIntegerArgument,
    RPNValidator.NonnegativeInteger  : generateNonnegativeIntegerArgument,
    RPNValidator.PrimeInteger        : generatePrimeArgument,
    RPNValidator.String              : generateStringArgument,
    RPNValidator.DateTime            : generateDateTimeArgument,
    RPNValidator.Location            : generateLocationArgument,
    RPNValidator.Boolean             : generateBooleanArgument,
    RPNValidator.Measurement         : generateMeasurementArgument,
    RPNValidator.AstronomicalObject  : generateAstronomicalObjectArgument,
    RPNValidator.List                : generateListArgument,
    RPNValidator.Generator           : generateGeneratorArgument,
    RPNValidator.Function            : generateFunctionArgument,
}


#******************************************************************************
#
#  class RPNVariable
#
#******************************************************************************

class RPNVariable( ):
    '''
    This class represents a variable in rpn, and it maintains a global
    dictionary of all variables keyed by name.
    '''
    def __init__( self, name ):
        self.name = name
        self.isHistory = not name[ 0 ].isalpha( )

        if name in g.variables:
            self.value = g.variables[ name ]
        else:
            self.value = nan

    def setValue( self, value ):
        if self.isHistory:
            raise ValueError( 'cannot set the value of a history expression' )

        self.value = value
        g.variables[ self.name ] = value

    def getValue( self ):
        if self.isHistory:
            prompt = int( self.name )

            if 0 < prompt < g.promptCount:
                self.value = g.results[ prompt ]
            else:
                raise ValueError( 'result index out of range' )

        return self.value


#******************************************************************************
#
#  class RPNOperator
#
#******************************************************************************

class RPNOperator( ):
    '''This class represents all the data needed to define an operator.'''
    def __init__( self, function, argCount ):
        self.function = function
        self.argCount = argCount

    def evaluate( self, term, index, currentValueList ):
        # handle a regular operator
        argsNeeded = self.argCount

        # first we validate, and make sure the operator has enough arguments
        if len( currentValueList ) < argsNeeded:
            abortArgsNeeded( term, index, argsNeeded )
            return False

        if argsNeeded == 0:
            result = self.function( )
        else:
            argList = list( )

            if g.operatorList:
                g.operatorsInList += 1

            # build argument list
            for i in range( 0, argsNeeded ):
                if g.operatorList:
                    # we need to tee a generator so it can run more than once
                    if isinstance( currentValueList[ g.lastOperand - 1 ], RPNGenerator ):
                        arg = currentValueList[ g.lastOperand - i ].clone( )
                    else:
                        arg = currentValueList[ g.lastOperand - i ]

                    if argsNeeded > g.operandsToRemove:
                        g.operandsToRemove = argsNeeded
                else:
                    arg = checkForVariable( currentValueList.pop( ) )

                    if term != 'set_variable' and isinstance( arg, RPNVariable ):
                        raise ValueError( 'set_variable called with a nonvariable argument' )
                        #arg = arg.getValue( )

                argList.append( arg if isinstance( arg, ( list, RPNGenerator ) ) else [ arg ] )

            # argument validation
            #self.validateArgTypes( term, *reverse( argList ), self.argTypes[ i ] )

            #print( 'argList', *reversed( argList ) )
            #print( 'self.function', self.function )

            result = callers[ argsNeeded ]( self.function, *reversed( argList ) )
            #result = list( map( self.function, *reversed( argList ) ) )

        # process results
        newResult = list( )

        if isinstance( result, RPNGenerator ):
            newResult.append( result )
        else:
            if not isinstance( result, list ):
                result = [ result ]

            for item in result:
                if isinstance( item, RPNMeasurement ) and item.units == { }:
                    newResult.append( item.value )
                else:
                    newResult.append( item )

        if len( newResult ) == 1:
            newResult = newResult[ 0 ]

        if term not in sideEffectOperators:
            currentValueList.append( newResult )

        return True

    def generateCall( self, operatorName ):
        args = [ ]

        print( operatorName )
        for i in range( self.argCount ):
            args.append( argumentGenerators[ self.argTypes[ i ] ]( ) )

        if args:
            print( args )
            return ' '.join( args ) + ' ' + operatorName
        else:
            return operatorName


#******************************************************************************
#
#  checkForVariable
#
#******************************************************************************

def checkForVariable( term ):
    if not isinstance( term, str ):
        return term

    # first check for a variable name or history expression
    if not term or term[ 0 ] != '$':
        return term

    if not g.interactive and term[ 1 : ] in g.userVariables:
        return g.userVariables[ term[ 1 : ] ]

    return RPNVariable( term[ 1 : ] )


#******************************************************************************
#
#  callers
#
#******************************************************************************

callers = [
    lambda func, args: func( ),
    lambda func, arg: func( arg ),
    lambda func, arg1, arg2: func( arg1, arg2 ),

    # 3, 4, and 5 argument functions don't recurse with lists more than one level
    # I have some ideas about how to improve this.
    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for a in arg1 for b in arg2 for c in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for a in arg1 for b in arg2 for c in arg3 for d in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for a in arg1 for b in arg2 for c in arg3 for d in arg4 for e in arg5 ],
]


#******************************************************************************
#
#  sideEffectOperators
#
#  This is a list of operators that execute without modifying the result
#  stack.
#
#******************************************************************************

sideEffectOperators = [
    'comma_mode',
    'hex_mode',
    'identify_mode',
    'leading_zero_mode',
    'octal_mode',
    'timer_mode',
]

