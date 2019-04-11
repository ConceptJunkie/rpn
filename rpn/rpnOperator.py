#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperator.py
# //
# //  RPN command-line calculator RPNOperator class definitions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from enum import Enum
from mpmath import exp, fadd, fmul, nan, nstr

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnSpecial import getRandomInteger, getRandomNumber
from rpn.rpnUtils import abortArgsNeeded

import random

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  RPNArgumentType class
# //
# //******************************************************************************

class RPNArgumentType( Enum ):
    Default = 0                 # any argument is valid
    Real = 1
    NonnegativeReal = 2         # real >= 0
    Integer = 3
    PositiveInteger = 4         # integer >= 1
    NonnegativeInteger = 5      # integer >= 0
    PrimeInteger = 6,
    String = 7
    DateTime = 8
    Location = 9                # location object (operators will automatically convert a string)
    Boolean = 10                # 0 or 1
    Measurement = 11
    AstronomicalObject = 12
    List = 13                   # the argument must be a list
    Generator = 14              # Generator needs to be a separate type now, but eventually it should be equivalent to List
    Function = 15


# //******************************************************************************
# //
# //  generateDefaultArgument
# //
# //******************************************************************************

def generateDefaultArgument( ):
    return 'argument'


# //******************************************************************************
# //
# //  generateRealArgument
# //
# //  for real numbers we are treating the range as logarithms
# //
# //******************************************************************************

def generateRealArgument( range = [ 0, 10 ], allowNegative = True ):
    factor = 1

    if allowNegative and getRandomInteger( 2 ) == 1:
        factor = -1

    return nstr( fmul( exp( fmul( getRandomNumber( ), random.uniform( *range ) ) ), factor ) )


# //******************************************************************************
# //
# //  generateNonnegativeRealArgument
# //
# //******************************************************************************

def generateNonnegativeRealArgument( range = [ 0, 10 ]  ):
    return generateRealArgument( range, allowNegative = False )


def generateIntegerArgument( range = [ 0, 1_000_000_000 ], allowNegative = True ):
    factor = 1

    if allowNegative and getRandomInteger( 2 ) == 1:
        factor = -1

    return str( fmul( fadd( getRandomInteger( range[ 1 ] ), range[ 0 ] ), factor ) )


def generatePositiveIntegerArgument( range = [ 1, 1_000_000_000 ], allowNegative = True  ):
    return generateIntegerArgument( range, allowNegative = False )

def generateNonnegativeIntegerArgument( range = [ 0, 1_000_000_000 ] ):
    return generateIntegerArgument( range, allowNegative = False )

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


# //******************************************************************************
# //
# //  argumentGenerators dict
# //
# //******************************************************************************

argumentGenerators = {
    RPNArgumentType.Default             : generateDefaultArgument,
    RPNArgumentType.Real                : generateRealArgument,
    RPNArgumentType.NonnegativeReal     : generateNonnegativeRealArgument,
    RPNArgumentType.Integer             : generateIntegerArgument,
    RPNArgumentType.PositiveInteger     : generatePositiveIntegerArgument,
    RPNArgumentType.NonnegativeInteger  : generateNonnegativeIntegerArgument,
    RPNArgumentType.PrimeInteger        : generatePrimeArgument,
    RPNArgumentType.String              : generateStringArgument,
    RPNArgumentType.DateTime            : generateDateTimeArgument,
    RPNArgumentType.Location            : generateLocationArgument,
    RPNArgumentType.Boolean             : generateBooleanArgument,
    RPNArgumentType.Measurement         : generateMeasurementArgument,
    RPNArgumentType.AstronomicalObject  : generateAstronomicalObjectArgument,
    RPNArgumentType.List                : generateListArgument,
    RPNArgumentType.Generator           : generateGeneratorArgument,
    RPNArgumentType.Function            : generateFunctionArgument,
}


# //******************************************************************************
# //
# //  class RPNVariable
# //
# //******************************************************************************

class RPNVariable( object ):
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

            if ( 0 < prompt < g.promptCount ):
                self.value = g.results[ prompt ]
            else:
                raise ValueError( 'result index out of range' )

        return self.value


# //******************************************************************************
# //
# //  class RPNOperator
# //
# //******************************************************************************

class RPNOperator( object ):
    measurementsAllowed = True
    measurementsNotAllowed = False

    '''This class represents all the data needed to define an operator.'''
    def __init__( self, function, argCount, argTypes = None, argTestRanges = None,
                  allowMeasurements = measurementsNotAllowed ):
        self.function = function
        self.argCount = argCount

        if argTypes is None:
            self.argTypes = list( )
        else:
            self.argTypes = argTypes

        if argTestRanges is None:
            self.argTestRanges = list( )
        else:
            self.argTestRanges = argTestRanges

        self.allowMeasurements = allowMeasurements

    # This method isn't used yet, but I hope to start using it soon.
    @staticmethod
    def validateArgType( self, term, arg, argType ):
        if isinstance( arg, ( list, RPNGenerator ) ) and argType not in ( RPNArgumentType.List, RPNArgumentType.Generator ):
            return True

        if argType == RPNArgumentType.Default:
            pass
        elif argType == RPNArgumentType.Real and im( arg ):
            raise ValueError( '\'' + term + '\':  real argument expected' )
        elif argType == RPNArgumentType.NonnegativeReal and ( im( arg ) or arg < 0 ):
            raise ValueError( '\'' + term + '\':  non-negative real argument expected' )
        elif argType == RPNArgumentType.Integer and arg != floor( arg ):
            raise ValueError( '\'' + term + '\':  integer argument expected' )
        elif argType == RPNArgumentType.NonnegativeInteger and arg != floor( arg ) or arg < 0:
            raise ValueError( '\'' + term + '\':  non-negative integer argument expected' )
        elif argType == RPNArgumentType.PositiveInteger and arg != floor( arg ) or arg < 1:
            raise ValueError( '\'' + term + '\':  positive integer argument expected' )
        elif argType == RPNArgumentType.String and not isinstance( arg, str ):
            raise ValueError( '\'' + term + '\':  string argument expected' )
        elif argType == RPNArgumentType.DateTime and not isinstance( arg, RPNDateTime ):
            raise ValueError( '\'' + term + '\':  date-time argument expected' )
        elif argType == RPNArgumentType.Location and not isinstance( arg, ( RPNLocation, str ) ):
            raise ValueError( '\'' + term + '\':  location argument expected' )
        elif argType == RPNArgumentType.Boolean and arg != 0 and arg != 1:
            raise ValueError( '\'' + term + '\':  boolean argument expected (0 or 1)' )
        elif argType == RPNArgumentType.Measurement and not isinstance( arg, RPNMeasurement ):
            raise ValueError( '\'' + term + '\':  measurement argument expected' )
        elif argType == RPNArgumentType.AstronomicalObject:
            pass
        elif argType == RPNArgumentType.List and not isinstance( arg, ( list, RPNGenerator ) ):
            raise ValueError( '\'' + term + '\':  list argument expected' )
        elif argType == RPNArgumentType.Generator and not isinstance( arg, RPNGenerator ):
            raise ValueError( '\'' + term + '\':  generator argument expected' )
        elif argType == RPNArgumentType.Function and not isinstance( arg, RPNFunction ):
            raise ValueError( '\'' + term + '\':  function argument expected' )

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

                    if term != 'set' and isinstance( arg, RPNVariable ):
                        arg = arg.getValue( )

                argList.append( arg if isinstance( arg, ( list, RPNGenerator ) ) else [ arg ] )

            # argument validation
            #for i, arg in enumerate( argList ):
            #    self.validateArgType( term, arg, self.argTypes[ i ] )

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


# //******************************************************************************
# //
# //  checkForVariable
# //
# //******************************************************************************

def checkForVariable( term ):
    if not isinstance( term, str ):
        return term

    # first check for a variable name or history expression
    if not term or term[ 0 ] != '$':
        return term

    if not g.interactive and term[ 1 : ] in g.userVariables:
        return g.userVariables[ term[ 1 : ] ]

    return RPNVariable( term[ 1 : ] )


# //******************************************************************************
# //
# //  callers
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  sideEffectOperators
# //
# //  This is a list of operators that execute without modifying the result
# //  stack.
# //
# //******************************************************************************

sideEffectOperators = [
    'comma_mode',
    'hex_mode',
    'identify_mode',
    'leading_zero_mode',
    'octal_mode',
    'timer_mode',
]

