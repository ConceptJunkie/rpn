#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six
import struct

from mpmath import *

from random import randrange

from rpnAliases import *
from rpnAstronomy import *
from rpnCalendar import *
from rpnCombinatorics import *
from rpnComputer import *
from rpnConstants import *
from rpnConstantUtils import *
from rpnDateTime import *
from rpnFactor import *
from rpnGeometry import *
from rpnInput import *
from rpnLexicographic import *
from rpnList import *
from rpnLocation import *
from rpnMath import *
from rpnMeasurement import *
from rpnModifiers import *
from rpnName import *
from rpnNumberTheory import *
from rpnPolynomials import *
from rpnPolytope import *
from rpnPrimeUtils import *
from rpnSettings import *
from rpnUtils import *


# //******************************************************************************
# //
# //  class OperatorInfo
# //
# //******************************************************************************

class OperatorInfo( ):
    def __init__( self, function, argCount = 0 ):
        self.function = function
        self.argCount = argCount


# //******************************************************************************
# //
# //  evaluateConstantOperator
# //
# //  We know there are no arguments.  Although none of the constants currently
# //  return a list, maybe one will in the future, so I'll handle list results.
# //
# //******************************************************************************

def evaluateConstantOperator( term, index, currentValueList ):
    # handle a constant operator
    operatorInfo = constants[ term ]
    result = callers[ 0 ]( operatorInfo.function, None )

    newResult = list( )

    if not isinstance( result, list ):
        result = [ result ]

    for item in result:
        if isinstance( item, RPNMeasurement ) and item.getUnits( ) == { }:
            newResult.append( mpf( item ) )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    currentValueList.append( newResult )

    return True


# //******************************************************************************
# //
# //  evaluateOperator
# //
# //******************************************************************************

def evaluateOperator( term, index, currentValueList ):
    # handle a regular operator
    operatorInfo = operators[ term ]
    argsNeeded = operatorInfo.argCount

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    if argsNeeded == 0:
        result = callers[ 0 ]( operatorInfo.function, None )
    else:
        argList = list( )

        if g.operatorList:
            g.operatorsInList += 1

        for i in range( 0, argsNeeded ):
            if g.operatorList:
                arg = currentValueList[ g.lastOperand - i ]

                if argsNeeded > g.operandsToRemove:
                    g.operandsToRemove = argsNeeded
            else:
                arg = currentValueList.pop( )

            argList.append( arg if isinstance( arg, list ) else [ arg ] )

        result = callers[ argsNeeded ]( operatorInfo.function, *argList )

    newResult = list( )

    if not isinstance( result, list ):
        result = [ result ]

    for item in result:
        if isinstance( item, RPNMeasurement ) and item.getUnits( ) == { }:
            newResult.append( mpf( item ) )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    if term not in sideEffectOperators:
        currentValueList.append( newResult )

    return True


# //******************************************************************************
# //
# //  evaluateListOperator
# //
# //******************************************************************************

def evaluateListOperator( term, index, currentValueList ):
    # handle a list operator
    operatorInfo = listOperators[ term ]
    argsNeeded = operatorInfo.argCount

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    # handle the call depending on the number of arguments needed
    if argsNeeded == 0:
        currentValueList.append( operatorInfo.function( currentValueList ) )
    elif argsNeeded == 1:
        currentValueList.append( evaluateOneListFunction( operatorInfo.function,
                                                          currentValueList.pop( ) ) )
    else:
        listArgs = [ ]

        for i in range( 0, argsNeeded ):
            listArgs.insert( 0, currentValueList.pop( ) )

        currentValueList.append( operatorInfo.function( *listArgs ) )

    return True


# //******************************************************************************
# //
# //  dumpOperators
# //
# //******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        # print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )
        print( '   ' + i )

    print( )
    print( 'constants:' )

    for i in sorted( [ key for key in constants ] ):
        print( '   ' + i )

    print( )
    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )
    print( 'modifer operators:' )

    for i in sorted( [ key for key in modifiers ] ):
        print( '   ' + i )

    print( )
    print( 'internal operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )

    print( )


    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


# //******************************************************************************
# //
# //  evaluateOneListFunction
# //
# //******************************************************************************

def evaluateOneListFunction( func, args ):
    if isinstance( args, list ):
        for arg in args:
            if isinstance( arg, list ) and isinstance( arg[ 0 ], list ):
                return [ evaluateOneListFunction( func, arg ) for arg in args ]

        return func( args )
    else:
        return func( [ args ] )


# //******************************************************************************
# //
# //  evaluateOneArgFunction
# //
# //******************************************************************************

def evaluateOneArgFunction( func, args ):
    if isinstance( args, list ):
        return [ evaluateOneArgFunction( func, i ) for i in args ]
    else:
        return func( args )


# //******************************************************************************
# //
# //  evaluateTwoArgFunction
# //
# //  This seems somewhat non-pythonic...
# //
# //******************************************************************************

def evaluateTwoArgFunction( func, _arg1, _arg2 ):
    if isinstance( _arg1, list ):
        len1 = len( _arg1 )
        if len1 == 1:
            arg1 = _arg1[ 0 ]
            list1 = False
        else:
            arg1 = _arg1
            list1 = True
    else:
        arg1 = _arg1
        list1 = False

    if isinstance( _arg2, list ):
        len2 = len( _arg2 )
        if len2 == 1:
            arg2 = _arg2[ 0 ]
            list2 = False
        else:
            arg2 = _arg2
            list2 = True
    else:
        arg2 = _arg2
        list2 = False

    if list1:
        if list2:
            return [ evaluateTwoArgFunction( func, arg1[ index ], arg2[ index ] ) for index in range( 0, min( len1, len2 ) ) ]
        else:
            return [ evaluateTwoArgFunction( func, i, arg2 ) for i in arg1 ]

    else:
        if list2:
            return [ evaluateTwoArgFunction( func, arg1, j ) for j in arg2 ]
        else:
            return func( arg2, arg1 )


# //******************************************************************************
# //
# //  callers
# //
# //******************************************************************************

callers = [
    lambda func, args: [ func( ) ],
    evaluateOneArgFunction,
    evaluateTwoArgFunction,

    # 3, 4, and 5 argument functions don't recurse with lists more than one level

    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for c in arg1 for b in arg2 for a in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for d in arg1 for c in arg2 for b in arg3 for a in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for e in arg1 for d in arg2 for c in arg3 for b in arg4 for a in arg5 ],
]


# //******************************************************************************
# //
# //  class FunctionInfo
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  FunctionInfo object.  However, it can't know how many of them it actually
# //  needs until it's time to evaluate the function, so we need to save all the
# //  terms we have so far, since we can't know until later how many of them we
# //  will need.
# //
# //  Once we are able to parse out how many arguments belong to the function
# //  declaration, then we can determine what arguments are left over to be used
# //  with the function operation.   All function operations take at least one
# //  argument before the function declaration.
# //
# //******************************************************************************

class FunctionInfo( ):
    def __init__( self, valueList = [ ], startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        else:
            self.valueList.append( valueList )

        self.startingIndex = startingIndex

    def evaluate( self, arg ):
        return arg

    def add( self, arg ):
        self.valueList.append( arg )


# //******************************************************************************
# //
# //  createFunction
# //
# //  This only gets called if we are not already creating a function.
# //
# //******************************************************************************

def createFunction( var, valueList ):
    g.creatingFunction = True
    valueList.append( FunctionInfo( valueList, len( valueList ) ) )
    valueList[ -1 ].add( var )


# //******************************************************************************
# //
# //  createXFunction
# //
# //******************************************************************************

def createXFunction( valueList ):
    createFunction( 'x', valueList )


# //******************************************************************************
# //
# //  createYFunction
# //
# //******************************************************************************

def createYFunction( valueList ):
    createFunction( 'y', valueList )


# //******************************************************************************
# //
# //  createZFunction
# //
# //******************************************************************************

def createZFunction( valueList ):
    createFunction( 'z', valueList )


# //******************************************************************************
# //
# //  evaluateFunction
# //
# //  Evaluate a user-defined function.  This is the simplest operator to use
# //  user-defined functions.   Eventually I want to compile the user-defined
# //  function into Python code, so when I start passing them to mpmath they'll
# //  run faster.
# //
# //******************************************************************************

def evaluateFunction( a, b, c, func ):
    if not isinstance( func, FunctionInfo ):
        raise ValueError( '\'eval\' expects a function argument' )

    if isinstance( a, list ) or isinstance( b, list ) or isinstance( c, list ):
        result = [ ]

        for item in a:
            result.append( k.evaluate( item ) )

        return result
    else:
        valueList = [ ]

        for index, item in enumerate( func.valueList ):
            if index < func.startingIndex:
                continue

            if item == 'x':
                valueList.append( a )
            elif item == 'y':
                valueList.append( b )
            elif item == 'z':
                valueList.append( c )
            else:
                valueList.append( item )

        index = 1

        while len( valueList ) > 1:
            oldValueList = list( valueList )
            listLength = len( valueList )

            term = valueList.pop( 0 )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            g.creatingFunction = False

            try:
                if not evaluateTerm( term, index, valueList ):
                    break
            except:
                return nan

            index = index + 1

            validFormula = True

            if len( valueList ) > 1:
                validFormula = False

                for value in valueList:
                    if not isinstance( value, mpf ):
                        validFormula = True
                        break

            if not validFormula:
                raise ValueError( 'evaluateFunction:  incompletely specified function' )

        return valueList[ 0 ]


# //******************************************************************************
# //
# //  evaluateFunction1
# //
# //******************************************************************************

def evaluateFunction1( n, k ):
    return evaluateFunction( n, 0, 0, k )


# //******************************************************************************
# //
# //  evaluateFunction2
# //
# //******************************************************************************

def evaluateFunction2( a, b, c ):
    return evaluateFunction( a, b, 0, c )


# //******************************************************************************
# //
# //  evaluateFunction3
# //
# //******************************************************************************

def evaluateFunction3( a, b, c, d ):
    return evaluateFunction( a, b, c, d )


# //******************************************************************************
# //
# //  plotFunction
# //
# //******************************************************************************

def plotFunction( start, end, func ):
    plot( lambda x: evaluateFunction1( x, func ), [ start, end ] )
    return 0


# //******************************************************************************
# //
# //  plot2DFunction
# //
# //******************************************************************************

def plot2DFunction( start1, end1, start2, end2, func ):
    splot( lambda x, y: evaluateFunction( x, y, 0, func ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


# //******************************************************************************
# //
# //  plot2DFunction
# //
# //******************************************************************************

def plot2DFunction( start1, end1, start2, end2, func ):
    splot( lambda x, y: evaluateFunction( x, y, 0, func ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


# //******************************************************************************
# //
# //  plotComplexFunction
# //
# //******************************************************************************

def plotComplexFunction( start1, end1, start2, end2, func ):
    cplot( lambda x: evaluateFunction( x, 0, 0, func ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ],
           points = 10000 )
    return 0


# //******************************************************************************
# //
# //  filterList
# //
# //******************************************************************************

def filterList( n, k, invert = False ) :
    if not isinstance( n, list ):
        n = [ n ]

    if not isinstance( k, FunctionInfo ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )
        else:
            raise ValueError( '\'filter\' expects a function argument' )

    result = [ ]

    for item in n:
        value = evaluateFunction( item, 0, 0, k )

        if ( value != 0 ) != invert:
            result.append( item )

    return result


# //******************************************************************************
# //
# //  filterListByIndex
# //
# //******************************************************************************

def filterListByIndex( n, k, invert = False ) :
    if not isinstance( n, list ):
        n = [ n ]

    if not isinstance( k, FunctionInfo ):
        if invert:
            raise ValueError( '\'unfilter_by_index\' expects a function argument' )
        else:
            raise ValueError( '\'filter_by_index\' expects a function argument' )

    result = [ ]

    for index, item in enumerate( n ):
        value = evaluateFunction( index, 0, 0, k )

        if ( value != 0 ) != invert:
            result.append( item )

    return result


# //******************************************************************************
# //
# //  dumpStats
# //
# //******************************************************************************

def dumpStats( ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) +
                                             len( modifiers ) ) )
    print( '{:10,} constants'.format( len( constants ) ) )
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( g.dataPath ), 'small primes' )
    printStats( loadLargePrimes( g.dataPath ), 'large primes' )
    printStats( loadHugePrimes( g.dataPath ), 'huge primes' )
    printStats( loadIsolatedPrimes( g.dataPath ), 'isolated primes' )
    printStats( loadTwinPrimes( g.dataPath ), 'twin primes' )
    printStats( loadBalancedPrimes( g.dataPath ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( g.dataPath ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( g.dataPath ), 'triple balanced primes' )
    printStats( loadSophiePrimes( g.dataPath ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( g.dataPath ), 'cousin primes' )
    printStats( loadSexyPrimes( g.dataPath ), 'sexy primes' )
    printStats( loadTripletPrimes( g.dataPath ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( g.dataPath ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( g.dataPath ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( g.dataPath ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( g.dataPath ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( g.dataPath ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]

# //******************************************************************************
# //
# //  evaluateTerm
# //
# //  This looks worse than it is.  It just has to do slightly different things
# //  depending on what kind of term or operator is involved.  Plus, there's a
# //  lot of exception handling.
# //
# //  This function assumes operator alias replacements have already occurred.
# //
# //******************************************************************************

def evaluateTerm( term, index, currentValueList ):
    # first check for a variable name or history expression
    if isinstance( term, str ) and term[ 0 ] == '$':
        if term[ 1 ].isalpha( ):
            if term[ 1 : ] in g.variables:
                currentValueList.append( g.variables[ term[ 1 : ] ] )
                return True
            else:
                g.variables[ term[ 1 : ] ] = None
                currentValueList.append( term[ 1 : ] )
                return True
        else:
            prompt = int( term[ 1 : ] )

            if ( prompt > 0 ) and ( prompt < g.promptCount ):
                currentValueList.append( g.results[ prompt ] )
                return True
            else:
                raise ValueError( 'result index out of range' )

    isList = isinstance( term, list )

    try:
        # handle a modifier operator
        if not isList and term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )
        elif not isList and term in g.unitOperatorNames:
            # handle a unit operator
            if not g.unitOperators:
                loadUnitData( )

            # look for unit without a value (in which case we give it a value of 1)
            if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], RPNMeasurement ) or \
                isinstance( currentValueList[ -1 ], RPNDateTime ) or ( isinstance( currentValueList[ -1 ], list ) and
                                                                       isinstance( currentValueList[ -1 ][ 0 ], RPNMeasurement ) ):
                    currentValueList.append( applyNumberValueToUnit( 1, term ) )
            # if the unit comes after a list, then apply it to every item in the list
            elif isinstance( currentValueList[ -1 ], list ):
                argList = currentValueList.pop( )

                newArg = [ ]

                for listItem in argList:
                    newArg.append( applyNumberValueToUnit( listItem, term ) )

                currentValueList.append( newArg )
            # and if it's a plain old number, then apply it to the unit
            elif isinstance( currentValueList[ -1 ], ( mpf, int ) ):
                currentValueList.append( applyNumberValueToUnit( currentValueList.pop( ), term ) )
            else:
                raise ValueError( 'unsupported type for a unit operator' )
        elif not isList and ( term in constants ):
            if not g.unitOperators:
                loadUnitData( )

            if not evaluateConstantOperator( term, index, currentValueList ):
                return False
        elif not isList and ( term in operators ):
            if g.duplicateOperations > 0:
                operatorInfo = operators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not evaluateOperator( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not evaluateOperator( term, index, currentValueList ):
                    return False
        elif not isList and term in listOperators:
            if g.duplicateOperations > 0:
                operatorInfo = operators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not evaluateListOperator( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not evaluateListOperator( term, index, currentValueList ):
                    return False
        else:
            # handle a plain old value (i.e., a number or list, not an operator)
            try:
                currentValueList.append( parseInputValue( term, g.inputRadix ) )

            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise
                else:
                    return False

            except ( AttributeError, TypeError ):
                currentValueList.append( term )
                return True

    except KeyboardInterrupt as error:
        print( 'rpn:  keyboard interrupt' )

        if g.debugMode:
            raise
        else:
            return False

    except ( ValueError, AttributeError, TypeError ) as error:
        print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

        if g.debugMode:
            raise
        else:
            return False

    except ZeroDivisionError as error:
        print( 'rpn:  division by zero' )

        if g.debugMode:
            raise
        else:
            return False

    except IndexError as error:
        print( 'rpn:  index error for list operator at arg ' + format( index ) +
               '.  Are your arguments in the right order?' )

        if g.debugMode:
            raise
        else:
            return False

    return True


# //******************************************************************************
# //
# //  printHelpMessage
# //
# //******************************************************************************

def printHelpMessage( ):
    from rpnOutput import printHelp
    printHelp( operators, constants, listOperators, modifiers, '', True )
    return 0


# //******************************************************************************
# //
# //  printHelpTopic
# //
# //******************************************************************************

def printHelpTopic( n ):
    from rpnOutput import printHelp

    if isinstance( n, str ):
        printHelp( operators, listOperators, modifiers, n, True )
    elif isinstance( n, RPNMeasurement ):
        units = n.getUnits( )
        # help for units isn't implemented yet, but now it will work
        printHelp( operators, constants, listOperators, modifiers, list( units.keys( ) )[ 0 ], True )
    else:
        print( 'The \'topic\' operator requires a string argument.' )

    return 0


# //******************************************************************************
# //
# //  functionOperators
# //
# //  This is a list of operators that terminate the function creation state.
# //
# //******************************************************************************

functionOperators = [
    'eval',
    'eval2',
    'eval3',
    'filter',
    'filter_by_index',
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plotc',
    'unfilter',
    'unfilter_by_index',
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


# //******************************************************************************
# //
# //  Modifiers are operators that directly modify the argument stack or global
# //  state in addition to or instead of just returning a value.
# //
# //  Modifiers also don't adhere to the 'language' of rpn, which is strictly
# //  postfix and context-free.  Unlike other operators consume one or more
# //  values and return either a single list (possibly with sublists) or a single
# //  value.  Also by changing global state, they can modify what comes _after_
# //  them, which is not how the rpn language is defined.  However, this gives me
# //  the flexibility to do some useful things that I am not otherwise able to
# //  do.
# //
# //******************************************************************************

modifiers = {
    'dup_term'          : OperatorInfo( duplicateTerm ),
    'dup_operator'      : OperatorInfo( duplicateOperation ),
    'previous'          : OperatorInfo( getPrevious ),
    'unlist'            : OperatorInfo( unlist ),
    'use_members'       : OperatorInfo( handleUseMembersOperator ),
    'x'                 : OperatorInfo( createXFunction ),
    'y'                 : OperatorInfo( createYFunction ),
    'z'                 : OperatorInfo( createZFunction ),
    '['                 : OperatorInfo( incrementNestedListLevel ),
    ']'                 : OperatorInfo( decrementNestedListLevel ),
    '{'                 : OperatorInfo( startOperatorList ),
    '}'                 : OperatorInfo( endOperatorList ),
}


# //******************************************************************************
# //
# //  listOperators are operators that handle whether or not an argument is a
# //  list themselves (because they require a list argument).  Unlike regular
# //  operators, we don't want listOperators permutated over each list element,
# //  and if we do for auxillary arguments, these operator handlers will do that
# //  themselves.
# //
# //******************************************************************************

listOperators = {
    # algebra
    'add_polynomials'       : OperatorInfo( addPolynomials, 2 ),
    'eval_polynomial'       : OperatorInfo( evaluatePolynomial, 2 ),
    'multiply_polynomials'  : OperatorInfo( multiplyPolynomials, 2 ),
    'polynomial_power'      : OperatorInfo( exponentiatePolynomial, 2 ),
    'polynomial_product'    : OperatorInfo( multiplyListOfPolynomials, 1 ),
    'polynomial_sum'        : OperatorInfo( addListOfPolynomials, 1 ),
    'solve'                 : OperatorInfo( solvePolynomial, 1 ),

    # arithmetic
    'gcd'                   : OperatorInfo( getGCD, 1 ),
    'lcm'                   : OperatorInfo( getLCM, 1 ),
    'max'                   : OperatorInfo( getMax, 1 ),
    'mean'                  : OperatorInfo( calculateMean, 1 ),
    'min'                   : OperatorInfo( getMin, 1 ),
    'product'               : OperatorInfo( getProduct, 1 ),
    'stddev'                : OperatorInfo( getStandardDeviation, 1 ),
    'sum'                   : OperatorInfo( getSum, 1 ),

    # conversion
    'convert'               : OperatorInfo( convertUnits, 2 ),   # list arguments are special
    'latlong_to_nac'        : OperatorInfo( convertLatLongToNAC, 1 ),
    'make_time'             : OperatorInfo( makeTime, 1 ),
    'unpack'                : OperatorInfo( unpackInteger, 2 ),
    'pack'                  : OperatorInfo( packInteger, 2 ),

    # date_time
    'make_iso_time'         : OperatorInfo( makeISOTime, 1 ),
    'make_julian_time'      : OperatorInfo( makeJulianTime, 1 ),

    # function
    'filter'                : OperatorInfo( filterList, 2 ),
    'filter_by_index'       : OperatorInfo( filterListByIndex, 2 ),
    'unfilter'              : OperatorInfo( lambda n, k: filterList( n, k, True ), 2 ),
    'unfilter_by_index'     : OperatorInfo( lambda n, k: filterListByIndex( n, k, True ), 2 ),

    # list
    'alternate_signs'       : OperatorInfo( alternateSigns, 1 ),
    'alternate_signs_2'     : OperatorInfo( alternateSigns2, 1 ),
    'alternating_sum'       : OperatorInfo( getAlternatingSum, 1 ),
    'alternating_sum_2'     : OperatorInfo( getAlternatingSum2, 1 ),
    'append'                : OperatorInfo( appendLists, 2 ),
    'count'                 : OperatorInfo( countElements, 1 ),
    'diffs'                 : OperatorInfo( getListDiffs, 1 ),
    'diffs2'                : OperatorInfo( getListDiffsFromFirst, 1 ),
    'element'               : OperatorInfo( getListElement, 2 ),
    'flatten'               : OperatorInfo( flatten, 1 ),
    'geometric_mean'        : OperatorInfo( calculateGeometricMean, 1 ),
    'group_elements'        : OperatorInfo( groupElements, 2 ),
    'interleave'            : OperatorInfo( interleave, 2 ),
    'intersection'          : OperatorInfo( makeIntersection, 2 ),
    'left'                  : OperatorInfo( getLeft, 2 ),
    'max_index'             : OperatorInfo( getIndexOfMax, 1 ),
    'min_index'             : OperatorInfo( getIndexOfMin, 1 ),
    'nonzero'               : OperatorInfo( getNonzeroes, 1 ),
    'occurrences'           : OperatorInfo( getOccurrences, 1 ),
    'ratios'                : OperatorInfo( getListRatios, 1 ),
    'reduce'                : OperatorInfo( reduceList, 1 ),
    'reverse'               : OperatorInfo( getReverse, 1 ),
    'right'                 : OperatorInfo( getRight, 2 ),
    'shuffle'               : OperatorInfo( shuffleList, 1 ),
    'slice'                 : OperatorInfo( getSlice, 3 ),
    'sort'                  : OperatorInfo( sortAscending, 1 ),
    'sort_descending'       : OperatorInfo( sortDescending, 1 ),
    'sublist'               : OperatorInfo( getSublist, 3 ),
    'union'                 : OperatorInfo( makeUnion, 2 ),
    'unique'                : OperatorInfo( getUniqueElements, 1 ),
    'zero'                  : OperatorInfo( getZeroes, 1 ),

    # number_theory
    'base'                  : OperatorInfo( interpretAsBase, 2 ),
    'cf'                    : OperatorInfo( convertFromContinuedFraction, 1 ),
    'crt'                   : OperatorInfo( calculateChineseRemainderTheorem, 2 ),
    'frobenius'             : OperatorInfo( getFrobeniusNumber, 1 ),
    'linear_recurrence'     : OperatorInfo( getNthLinearRecurrence, 3 ),

    # lexicographic
    'combine_digits'        : OperatorInfo( combineDigits, 1 ),

    # powers_and_roots
    'tower'                 : OperatorInfo( calculatePowerTower, 1 ),
    'tower2'                : OperatorInfo( calculatePowerTower2, 1 ),
}


# //******************************************************************************
# //
# //  operators
# //
# //  Regular operators expect zero or more single values and if those arguments
# //  are lists, rpn will iterate calls to the operator handler for each element
# //  in the list.   Multiple lists for arguments are not permutated.  Instead,
# //  the operator handler is called for each element in the first list, along
# //  with the nth element of each other argument that is also a list.
# //
# //******************************************************************************

operators = {
    # algebra
    'find_polynomial'               : OperatorInfo( findPolynomial, 2 ),
    'solve_cubic'                   : OperatorInfo( solveCubicPolynomial, 4 ),
    'solve_quadratic'               : OperatorInfo( solveQuadraticPolynomial, 3 ),
    'solve_quartic'                 : OperatorInfo( solveQuarticPolynomial, 5 ),

    # arithmetic
    'abs'                           : OperatorInfo( fabs, 1 ),
    'add'                           : OperatorInfo( add, 2, ),
    'ceiling'                       : OperatorInfo( ceil, 1 ),
    'divide'                        : OperatorInfo( divide, 2 ),
    'floor'                         : OperatorInfo( floor, 1 ),
    'is_divisible'                  : OperatorInfo( lambda n, k: 1 if fmod( real( n ), k ) == 0 else 0, 2 ),
    'is_equal'                      : OperatorInfo( isEqual, 2 ),
    'is_even'                       : OperatorInfo( lambda n: 1 if fmod( real( n ), 2 ) == 0 else 0, 1 ),
    'is_greater'                    : OperatorInfo( isGreater, 2 ),
    'is_less'                       : OperatorInfo( isLess, 2 ),
    'is_not_equal'                  : OperatorInfo( isNotEqual, 2 ),
    'is_not_greater'                : OperatorInfo( isNotGreater, 2 ),
    'is_not_less'                   : OperatorInfo( isNotLess, 2 ),
    'is_not_zero'                   : OperatorInfo( lambda n: 0 if n == 0 else 1, 1 ),
    'is_odd'                        : OperatorInfo( lambda n: 1 if fmod( real( n ), 2 ) == 1 else 0, 1 ),
    'is_square'                     : OperatorInfo( isSquare, 1 ),
    'is_zero'                       : OperatorInfo( lambda n: 1 if n == 0 else 0, 1 ),
    'modulo'                        : OperatorInfo( lambda n, k: fmod( real( n ), real( k ) ), 2 ),
    'multiply'                      : OperatorInfo( multiply, 2 ),
    'nearest_int'                   : OperatorInfo( nint, 1 ),
    'negative'                      : OperatorInfo( getNegative, 1 ),
    'reciprocal'                    : OperatorInfo( takeReciprocal, 1 ),
    'round'                         : OperatorInfo( lambda n: floor( fadd( n, 0.5 ) ), 1 ),
    'sign'                          : OperatorInfo( sign, 1 ),
    'subtract'                      : OperatorInfo( subtract, 2, ),

    # astronomy
    'astronomical_dawn'             : OperatorInfo( lambda n, k: getNextDawn( n, k, -18 ), 2 ),
    'astronomical_dusk'             : OperatorInfo( lambda n, k: getNextDawn( n, k, -18 ), 2 ),
    'autumnal_equinox'              : OperatorInfo( getAutumnalEquinox, 1 ),
    'dawn'                          : OperatorInfo( getNextDawn, 2 ),
    'dusk'                          : OperatorInfo( getNextDusk, 2 ),
    'moonrise'                      : OperatorInfo( lambda n, k: getNextRising( ephem.Moon( ), n, k ), 2 ),
    'moonset'                       : OperatorInfo( lambda n, k: getNextSetting( ephem.Moon( ), n, k ), 2 ),
    'moon_antitransit'              : OperatorInfo( lambda n, k: getNextAntitransit( ephem.Moon( ), n, k ), 2 ),
    'moon_phase'                    : OperatorInfo( getMoonPhase, 1 ),
    'moon_transit'                  : OperatorInfo( lambda n, k: getNextTransit( ephem.Moon( ), n, k ), 2 ),
    'nautical_dawn'                 : OperatorInfo( lambda n, k: getNextDawn( n, k, -12 ), 2 ),
    'nautical_dusk'                 : OperatorInfo( lambda n, k: getNextDawn( n, k, -12 ), 2 ),
    'next_antitransit'              : OperatorInfo( getNextAntitransit, 3 ),
    'next_first_quarter_moon'       : OperatorInfo( lambda n: getEphemTime( n, ephem.next_first_quarter_moon ), 1 ),
    'next_full_moon'                : OperatorInfo( lambda n: getEphemTime( n, ephem.next_full_moon ), 1 ),
    'next_last_quarter_moon'        : OperatorInfo( lambda n: getEphemTime( n, ephem.next_last_quarter_moon ), 1 ),
    'next_new_moon'                 : OperatorInfo( lambda n: getEphemTime( n, ephem.next_new_moon ), 1 ),
    'next_rising'                   : OperatorInfo( getNextRising, 3 ),
    'next_setting'                  : OperatorInfo( getNextSetting, 3 ),
    'next_transit'                  : OperatorInfo( getNextTransit, 3 ),
    'previous_antitransit'          : OperatorInfo( getPreviousAntitransit, 3 ),
    'previous_first_quarter_moon'   : OperatorInfo( lambda n: getEphemTime( n, ephem.previous_first_quarter_moon ), 1 ),
    'previous_full_moon'            : OperatorInfo( lambda n: getEphemTime( n, ephem.previous_full_moon ), 1 ),
    'previous_last_quarter_moon'    : OperatorInfo( lambda n: getEphemTime( n, ephem.previous_last_quarter_moon ), 1 ),
    'previous_new_moon'             : OperatorInfo( lambda n: getEphemTime( n, ephem.previous_new_moon ), 1 ),
    'previous_rising'               : OperatorInfo( getPreviousRising, 3 ),
    'previous_setting'              : OperatorInfo( getPreviousSetting, 3 ),
    'previous_transit'              : OperatorInfo( getPreviousTransit, 3 ),
    'sky_location'                  : OperatorInfo( getSkyLocation, 2 ),
    'solar_noon'                    : OperatorInfo( lambda n, k: getNextTransit( ephem.Sun( ), n, k ), 2 ),
    'summer_solstice'               : OperatorInfo( getSummerSolstice, 1 ),
    'sunrise'                       : OperatorInfo( lambda n, k: getNextRising( ephem.Sun( ), n, k ), 2 ),
    'sunset'                        : OperatorInfo( lambda n, k: getNextSetting( ephem.Sun( ), n, k ), 2 ),
    'sun_antitransit'               : OperatorInfo( lambda n, k: getNextAntitransit( ephem.Sun( ), n, k ), 2 ),
    'vernal_equinox'                : OperatorInfo( getVernalEquinox, 1 ),
    'winter_solstice'               : OperatorInfo( getWinterSolstice, 1 ),

    # astronomy - heavenly body operators
    'sun'                           : OperatorInfo( ephem.Sun, 0 ),
    'mercury'                       : OperatorInfo( ephem.Mercury, 0 ),
    'venus'                         : OperatorInfo( ephem.Venus, 0 ),
    'moon'                          : OperatorInfo( ephem.Moon, 0 ),
    'mars'                          : OperatorInfo( ephem.Mars, 0 ),
    'jupiter'                       : OperatorInfo( ephem.Jupiter, 0 ),
    'saturn'                        : OperatorInfo( ephem.Saturn, 0 ),
    'uranus'                        : OperatorInfo( ephem.Uranus, 0 ),
    'neptune'                       : OperatorInfo( ephem.Neptune, 0 ),
    'pluto'                         : OperatorInfo( ephem.Pluto, 0 ),

    # bitwise
    'and'                           : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x & y ), 2 ),
    'count_bits'                    : OperatorInfo( getBitCount, 1 ),
    'nand'                          : OperatorInfo( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x & y ) ), 2 ),
    'nor'                           : OperatorInfo( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x | y ) ), 2 ),
    'not'                           : OperatorInfo( getInvertedBits, 1 ),
    'or'                            : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x | y ), 2 ),
    'parity'                        : OperatorInfo( lambda n: getBitCount( n ) & 1, 1 ),
    'shift_left'                    : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2 ),
    'shift_right'                   : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2 ),
    'xor'                           : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x ^ y ), 2 ),

    # calendar
    'calendar'                      : OperatorInfo( generateMonthCalendar, 2 ),
    'from_bahai'                    : OperatorInfo( convertBahaiDate, 3 ),
    'from_hebrew'                   : OperatorInfo( convertHebrewDate, 3 ),
    'from_indian_civil'             : OperatorInfo( convertIndianCivilDate, 3 ),
    'from_islamic'                  : OperatorInfo( convertIslamicDate, 3 ),
    'from_julian'                   : OperatorInfo( convertJulianDate, 3 ),
    'from_mayan'                    : OperatorInfo( convertMayanDate, 5 ),
    'from_persian'                  : OperatorInfo( convertPersianDate, 3 ),
    'to_bahai'                      : OperatorInfo( getBahaiCalendarDate, 1 ),
    'to_bahai_name'                 : OperatorInfo( getBahaiCalendarDateName, 1 ),
    'to_hebrew'                     : OperatorInfo( getHebrewCalendarDate, 1 ),
    'to_hebrew_name'                : OperatorInfo( getHebrewCalendarDateName, 1 ),
    'to_indian_civil'               : OperatorInfo( getIndianCivilCalendarDate, 1 ),
    'to_indian_civil_name'          : OperatorInfo( getIndianCivilCalendarDateName, 1 ),
    'to_islamic'                    : OperatorInfo( getIslamicCalendarDate, 1 ),
    'to_islamic_name'               : OperatorInfo( getIslamicCalendarDateName, 1 ),
    'to_iso'                        : OperatorInfo( getISODate, 1 ),
    'to_iso_name'                   : OperatorInfo( getISODateName, 1 ),
    'to_julian'                     : OperatorInfo( getJulianCalendarDate, 1 ),
    'to_julian_day'                 : OperatorInfo( getJulianDay, 1 ),
    'to_lilian_day'                 : OperatorInfo( getLilianDay, 1 ),
    'to_mayan'                      : OperatorInfo( getMayanCalendarDate, 1 ),
    'to_ordinal_date'               : OperatorInfo( getOrdinalDate, 1 ),
    'to_persian'                    : OperatorInfo( getPersianCalendarDate, 1 ),
    'to_persian_name'               : OperatorInfo( getPersianCalendarDateName, 1 ),
    'year_calendar'                 : OperatorInfo( generateYearCalendar, 1 ),

    # combinatoric
    'bell_polynomial'               : OperatorInfo( bell, 2 ),
    'binomial'                      : OperatorInfo( binomial, 2 ),
    'compositions'                  : OperatorInfo( getCompositions, 2 ),
    'debruijn'                      : OperatorInfo( createDeBruijnSequence, 2 ),
    'lah'                           : OperatorInfo( lambda n, k: fdiv( fmul( binomial( real( n ), real( k ) ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2 ),
    'multifactorial'                : OperatorInfo( getNthMultifactorial, 2 ),
    'narayana'                      : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2 ),
    'nth_apery'                     : OperatorInfo( getNthAperyNumber, 1 ),
    'nth_bell'                      : OperatorInfo( bell, 1 ),
    'nth_bernoulli'                 : OperatorInfo( bernoulli, 1 ),
    'nth_catalan'                   : OperatorInfo( lambda n: fdiv( binomial( fmul( 2, real( n ) ), n ), fadd( n, 1 ) ), 1 ),
    'nth_delannoy'                  : OperatorInfo( getNthDelannoyNumber, 1 ),
    'nth_motzkin'                   : OperatorInfo( getNthMotzkinNumber, 1 ),
    'nth_pell'                      : OperatorInfo( getNthPellNumber, 1 ),
    'nth_schroeder'                 : OperatorInfo( getNthSchroederNumber, 1 ),
    'nth_sylvester'                 : OperatorInfo( getNthSylvester, 1 ),
    'partitions'                    : OperatorInfo( lambda n: getPartitionNumber( n, 1 ), 1 ),
    'permutations'                  : OperatorInfo( getPermutations, 2 ),

    # complex
    'argument'                      : OperatorInfo( arg, 1 ),
    'conjugate'                     : OperatorInfo( conj, 1 ),
    'i'                             : OperatorInfo( lambda n: mpc( real = '0.0', imag = n ), 1 ),
    'imaginary'                     : OperatorInfo( im, 1 ),
    'real'                          : OperatorInfo( re, 1 ),

    # conversion
    'char'                          : OperatorInfo( lambda n: convertToSignedInt( n, 8 ), 1 ),
    'dhms'                          : OperatorInfo( convertToDHMS, 1 ),
    'dms'                           : OperatorInfo( convertToDMS, 1 ),
    'double'                        : OperatorInfo( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( real( n ) ) ) ) ), 1 ),
    'float'                         : OperatorInfo( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( real( n ) ) ) ) ), 1 ),
    'from_unix_time'                : OperatorInfo( convertFromUnixTime, 1 ),
    'long'                          : OperatorInfo( lambda n: convertToSignedInt( n, 32 ), 1 ),
    'longlong'                      : OperatorInfo( lambda n: convertToSignedInt( n, 64 ), 1 ),
    'hms'                           : OperatorInfo( convertToHMS, 1 ),
    'integer'                       : OperatorInfo( convertToSignedInt, 2 ),
    'invert_units'                  : OperatorInfo( invertUnits, 1 ),
    'uchar'                         : OperatorInfo( lambda n: fmod( real_int( n ), power( 2, 8 ) ), 1 ),
    'uinteger'                      : OperatorInfo( lambda n, k: fmod( real_int( n ), power( 2, real( k ) ) ), 2 ),
    'ulong'                         : OperatorInfo( lambda n: fmod( real_int( n ), power( 2, 32 ) ), 1 ),
    'ulonglong'                     : OperatorInfo( lambda n: fmod( real_int( n ), power( 2, 64 ) ), 1 ),
    'undouble'                      : OperatorInfo( interpretAsDouble, 1 ),
    'unfloat'                       : OperatorInfo( interpretAsFloat, 1 ),
    'ushort'                        : OperatorInfo( lambda n: fmod( real_int( n ), power( 2, 16 ) ), 1 ),
    'short'                         : OperatorInfo( lambda n: convertToSignedInt( n, 16 ), 1 ),
    'to_unix_time'                  : OperatorInfo( convertToUnixTime, 1 ),
    'ydhms'                         : OperatorInfo( convertToYDHMS, 1 ),

    # date_time
    'ash_wednesday'                 : OperatorInfo( calculateAshWednesday, 1 ),
    'dst_end'                       : OperatorInfo( calculateDSTEnd, 1 ),
    'dst_start'                     : OperatorInfo( calculateDSTStart, 1 ),
    'easter'                        : OperatorInfo( calculateEaster, 1 ),
    'election_day'                  : OperatorInfo( calculateElectionDay, 1 ),
    'iso_day'                       : OperatorInfo( getISODay, 1 ),
    'labor_day'                     : OperatorInfo( calculateLaborDay, 1 ),
    'memorial_day'                  : OperatorInfo( calculateMemorialDay, 1 ),
    'now'                           : OperatorInfo( RPNDateTime.getNow, 0 ),
    'nth_weekday'                   : OperatorInfo( calculateNthWeekdayOfMonth, 4 ),
    'nth_weekday_of_year'           : OperatorInfo( calculateNthWeekdayOfYear, 3 ),
    'presidents_day'                : OperatorInfo( calculatePresidentsDay, 1 ),
    'thanksgiving'                  : OperatorInfo( calculateThanksgiving, 1 ),
    'today'                         : OperatorInfo( getToday, 0 ),
    'tomorrow'                      : OperatorInfo( getTomorrow, 0 ),
    'weekday'                       : OperatorInfo( getWeekday, 1, ),
    'yesterday'                     : OperatorInfo( getYesterday, 0 ),

    # function
    'eval'                          : OperatorInfo( evaluateFunction1, 2 ),
    'eval2'                         : OperatorInfo( evaluateFunction2, 3 ),
    'eval3'                         : OperatorInfo( evaluateFunction3, 4 ),
    'limit'                         : OperatorInfo( lambda n, func: limit( lambda x: evaluateFunction1( x, func ), n ), 2 ),
    'limitn'                        : OperatorInfo( lambda n, func: limit( lambda x: evaluateFunction1( x, func ), n, direction = -1 ), 2 ),
    'negate'                        : OperatorInfo( lambda n: 1 if n == 0 else 0, 1 ),
    'nprod'                         : OperatorInfo( lambda start, end, func: nprod( lambda x: evaluateFunction1( x, func ), [ start, end ] ), 3 ),
    'nsum'                          : OperatorInfo( lambda start, end, func: nsum( lambda x: evaluateFunction1( x, func ), [ start, end ] ), 3 ),
    'plot'                          : OperatorInfo( plotFunction, 3 ),
    'plot2'                         : OperatorInfo( plot2DFunction, 5 ),
    'plotc'                         : OperatorInfo( plotComplexFunction, 5 ),

    # geography
    'distance'                      : OperatorInfo( getDistance, 2 ),
    'latlong'                       : OperatorInfo( lambda n, k: RPNLocation( n, k ), 2 ),
    'location'                      : OperatorInfo( getLocation, 1 ),
    'location_info'                 : OperatorInfo( getLocationInfo, 1 ),

    # geometry
    'antiprism_area'                : OperatorInfo( getAntiprismSurfaceArea, 2 ),
    'antiprism_volume'              : OperatorInfo( getAntiprismVolume, 2 ),
    'cone_area'                     : OperatorInfo( getConeSurfaceArea, 2 ),
    'cone_volume'                   : OperatorInfo( getConeVolume, 2 ),
    'dodecahedron_area'             : OperatorInfo( getDodecahedronSurfaceArea, 1 ),
    'dodecahedron_volume'           : OperatorInfo( getDodecahedronVolume, 1 ),
    'icosahedron_area'              : OperatorInfo( getIcosahedronSurfaceArea, 1 ),
    'icosahedron_volume'            : OperatorInfo( getIcosahedronVolume, 1 ),
    'n_sphere_area'                 : OperatorInfo( getNSphereSurfaceArea, 2 ),
    'n_sphere_radius'               : OperatorInfo( getNSphereRadius, 2 ),
    'n_sphere_volume'               : OperatorInfo( getNSphereVolume, 2 ),
    'octahedron_area'               : OperatorInfo( getOctahedronSurfaceArea, 1 ),
    'octahedron_volume'             : OperatorInfo( getOctahedronVolume, 1 ),
    'polygon_area'                  : OperatorInfo( getRegularPolygonArea, 1 ),
    'prism_area'                    : OperatorInfo( getPrismSurfaceArea, 3 ),
    'prism_volume'                  : OperatorInfo( getPrismVolume, 3 ),
    'sphere_area'                   : OperatorInfo( lambda n: getNSphereSurfaceArea( n, 3 ), 1 ),
    'sphere_radius'                 : OperatorInfo( lambda n: getNSphereRadius( n, 3 ), 1 ),
    'sphere_volume'                 : OperatorInfo( lambda n: getNSphereVolume( n, 3 ), 1 ),
    'tetrahedron_area'              : OperatorInfo( getTetrahedronSurfaceArea, 1 ),
    'tetrahedron_volume'            : OperatorInfo( getTetrahedronVolume, 1 ),
    'torus_area'                    : OperatorInfo( getTorusSurfaceArea, 2 ),
    'torus_volume'                  : OperatorInfo( getTorusVolume, 2 ),
    'triangle_area'                 : OperatorInfo( getTriangleArea, 3 ),

    # lexicographic
    'add_digits'                    : OperatorInfo( addDigits, 2 ),
    'dup_digits'                    : OperatorInfo( duplicateDigits, 2 ),
    'find_palindrome'               : OperatorInfo( findPalindrome, 2 ),
    'get_digits'                    : OperatorInfo( getDigits, 1 ),
    'is_narcissistic'               : OperatorInfo( isNarcissistic, 1 ),
    'is_palindrome'                 : OperatorInfo( isPalindrome, 1 ),
    'is_pandigital'                 : OperatorInfo( isPandigital, 1 ),
    'multiply_digits'               : OperatorInfo( multiplyDigits, 1 ),
    'reversal_addition'             : OperatorInfo( getNthReversalAddition, 2 ),
    'reverse_digits'                : OperatorInfo( reverseDigits, 1 ),
    'sum_digits'                    : OperatorInfo( sumDigits, 1 ),

    # list
    'exponential_range'             : OperatorInfo( expandExponentialRange, 3 ),
    'geometric_range'               : OperatorInfo( expandGeometricRange, 3 ),
    'range'                         : OperatorInfo( expandRange, 2 ),
    'range2'                        : OperatorInfo( expandSteppedRange, 3 ),

    # logarithms
    'lambertw'                      : OperatorInfo( lambertw, 1 ),
    'li'                            : OperatorInfo( li, 1 ),
    'ln'                            : OperatorInfo( ln, 1 ),
    'log10'                         : OperatorInfo( log10, 1 ),
    'log2'                          : OperatorInfo( lambda n: log( n, 2 ), 1 ),
    'logxy'                         : OperatorInfo( log, 2 ),
    'polylog'                       : OperatorInfo( polylog, 2 ),

    # number_theory
    'aliquot'                       : OperatorInfo( getAliquotSequence, 2 ),
    'alternating_factorial'         : OperatorInfo( getNthAlternatingFactorial, 1 ),
    'carol'                         : OperatorInfo( lambda n: fsub( power( fsub( power( 2, real( n ) ), 1 ), 2 ), 2 ), 1 ),
    'count_divisors'                : OperatorInfo( getDivisorCount, 1 ),
    'divisors'                      : OperatorInfo( getDivisors, 1 ),
    'double_factorial'              : OperatorInfo( fac2, 1 ),
    'ecm'                           : OperatorInfo( getECMFactorList, 1 ),
    'egypt'                         : OperatorInfo( getGreedyEgyptianFraction, 2 ),
    'euler_brick'                   : OperatorInfo( makeEulerBrick, 3 ),
    'euler_phi'                     : OperatorInfo( getEulerPhi, 1 ),
    'factor'                        : OperatorInfo( getFactorList, 1 ),
    'factorial'                     : OperatorInfo( fac, 1 ),
    'fibonacci'                     : OperatorInfo( fib, 1 ),
    'fibonorial'                    : OperatorInfo( getNthFibonorial, 1 ),
    'fraction'                      : OperatorInfo( interpretAsFraction, 2 ),
    'gamma'                         : OperatorInfo( gamma, 1 ),
    'harmonic'                      : OperatorInfo( harmonic, 1 ),
    'heptanacci'                    : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 7 ), 1 ),
    'hexanacci'                     : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 6 ), 1 ),
    'hyperfactorial'                : OperatorInfo( hyperfac, 1 ),
    'is_abundant'                   : OperatorInfo( isAbundant, 1 ),
    'is_achilles'                   : OperatorInfo( isAchillesNumber, 1 ),
    'is_deficient'                  : OperatorInfo( isDeficient, 1 ),
    'is_k_semiprime'                : OperatorInfo( isKSemiPrime, 2 ),
    'is_perfect'                    : OperatorInfo( isPerfect, 1 ),
    'is_powerful'                   : OperatorInfo( isPowerful, 1 ),
    'is_prime'                      : OperatorInfo( lambda n: 1 if isPrime( n ) else 0, 1 ),
    'is_pronic'                     : OperatorInfo( isPronic, 1 ),
    'is_rough'                      : OperatorInfo( isRough, 2 ),
    'is_semiprime'                  : OperatorInfo( lambda n: isKSemiPrime( n, 2 ), 1 ),
    'is_smooth'                     : OperatorInfo( isSmooth, 2 ),
    'is_sphenic'                    : OperatorInfo( isSphenic, 1 ),
    'is_squarefree'                 : OperatorInfo( isSquareFree, 1 ),
    'is_unusual'                    : OperatorInfo( isUnusual, 1 ),
    'jacobsthal'                    : OperatorInfo( getNthJacobsthalNumber, 1 ),
    'kynea'                         : OperatorInfo( lambda n: fsub( power( fadd( power( 2, real( n ) ), 1 ), 2 ), 2 ), 1 ),
    'leonardo'                      : OperatorInfo( lambda n: fsub( fmul( 2, fib( fadd( real( n ), 1 ) ) ), 1 ), 1 ),
    'leyland'                       : OperatorInfo( lambda n, k: fadd( power( n, k ), power( k, n ) ), 2 ),
    'log_gamma'                     : OperatorInfo( loggamma, 1 ),
    'lucas'                         : OperatorInfo( getNthLucasNumber, 1 ),
    'make_cf'                       : OperatorInfo( lambda n, k: ContinuedFraction( real( n ), maxterms = real( k ), cutoff = power( 10, -( mp.dps - 2 ) ) ), 2 ),
    'make_pyth_3'                   : OperatorInfo( makePythagoreanTriple, 2 ),
    'make_pyth_4'                   : OperatorInfo( makePythagoreanQuadruple, 2 ),
    'merten'                        : OperatorInfo( getNthMerten, 1 ),
    'mobius'                        : OperatorInfo( getMobius, 1 ),
    'nth_padovan'                   : OperatorInfo( getNthPadovanNumber, 1 ),
    'n_fibonacci'                   : OperatorInfo( getNthKFibonacciNumber, 2 ),
    'octanacci'                     : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 8 ), 1 ),
    'pascal_triangle'               : OperatorInfo( getNthPascalLine, 1 ),
    'pentanacci'                    : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 5 ), 1 ),
    'polygamma'                     : OperatorInfo( psi, 2 ),
    'repunit'                       : OperatorInfo( getNthBaseKRepunit, 2 ),
    'riesel'                        : OperatorInfo( lambda n: fsub( fmul( real( n ), power( 2, n ) ), 1 ), 1 ),
    'sigma'                         : OperatorInfo( getSigma, 1 ),
    'subfactorial'                  : OperatorInfo( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1 ),
    'superfactorial'                : OperatorInfo( superfac, 1 ),
    'tetranacci'                    : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 4 ), 1 ),
    'thabit'                        : OperatorInfo( lambda n: fsub( fmul( 3, power( 2, n ) ), 1 ), 1 ),
    'tribonacci'                    : OperatorInfo( lambda n: getNthKFibonacciNumber( n, 3 ), 1 ),
    'unit_roots'                    : OperatorInfo( lambda n: unitroots( real_int( n ) ), 1 ),
    'zeta'                          : OperatorInfo( zeta, 1 ),

    # polygonal
    'centered_decagonal'            : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 10 ), 1 ),
    'centered_heptagonal'           : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 7 ), 1 ),
    'centered_hexagonal'            : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 6 ), 1 ),
    'centered_nonagonal'            : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 9 ), 1 ),
    'centered_octagonal'            : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 8 ), 1 ),
    'centered_pentagonal'           : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 5 ), 1 ),
    'centered_polygonal'            : OperatorInfo( getCenteredPolygonalNumber, 2 ),
    'centered_square'               : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 4 ), 1 ),
    'centered_triangular'           : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 3 ), 1 ),
    'decagonal'                     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 10 ), 1 ),
    'decagonal_centered_square'     : OperatorInfo( getNthDecagonalCenteredSquareNumber, 1 ),
    'decagonal_heptagonal'          : OperatorInfo( getNthDecagonalHeptagonalNumber, 1 ),
    'decagonal_hexagonal'           : OperatorInfo( getNthDecagonalHexagonalNumber, 1 ),
    'decagonal_nonagonal'           : OperatorInfo( getNthDecagonalNonagonalNumber, 1 ),
    'decagonal_octagonal'           : OperatorInfo( getNthDecagonalOctagonalNumber, 1 ),
    'decagonal_pentagonal'          : OperatorInfo( getNthDecagonalPentagonalNumber, 1 ),
    'decagonal_triangular'          : OperatorInfo( getNthDecagonalTriangularNumber, 1 ),
    'heptagonal'                    : OperatorInfo( lambda n: getNthPolygonalNumber( n, 7 ), 1 ),
    'heptagonal_hexagonal'          : OperatorInfo( getNthHeptagonalHexagonalNumber, 1 ),
    'heptagonal_pentagonal'         : OperatorInfo( getNthHeptagonalPentagonalNumber, 1 ),
    'heptagonal_square'             : OperatorInfo( getNthHeptagonalSquareNumber, 1 ),
    'heptagonal_triangular'         : OperatorInfo( getNthHeptagonalTriangularNumber, 1 ),
    'hexagonal'                     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 6 ), 1 ),
    'hexagonal_pentagonal'          : OperatorInfo( getNthHexagonalPentagonalNumber, 1 ),
    'hexagonal_square'              : OperatorInfo( getNthHexagonalSquareNumber, 1 ),
    'nonagonal'                     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 9 ), 1 ),
    'nonagonal_heptagonal'          : OperatorInfo( getNthNonagonalHeptagonalNumber, 1 ),
    'nonagonal_hexagonal'           : OperatorInfo( getNthNonagonalHexagonalNumber, 1 ),
    'nonagonal_octagonal'           : OperatorInfo( getNthNonagonalOctagonalNumber, 1 ),
    'nonagonal_pentagonal'          : OperatorInfo( getNthNonagonalPentagonalNumber, 1 ),
    'nonagonal_square'              : OperatorInfo( getNthNonagonalSquareNumber, 1 ),
    'nonagonal_triangular'          : OperatorInfo( getNthNonagonalTriangularNumber, 1 ),
    'nth_centered_decagonal'        : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 10 ), 1 ),
    'nth_centered_heptagonal'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 7 ), 1 ),
    'nth_centered_hexagonal'        : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 6 ), 1 ),
    'nth_centered_nonagonal'        : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 9 ), 1 ),
    'nth_centered_octagonal'        : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 8 ), 1 ),
    'nth_centered_pentagonal'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 5 ), 1 ),
    'nth_centered_polygonal'        : OperatorInfo( findCenteredPolygonalNumber, 2 ),
    'nth_centered_square'           : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 4 ), 1 ),
    'nth_centered_triangular'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 3 ), 1 ),
    'nth_decagonal'                 : OperatorInfo( lambda n: findNthPolygonalNumber( n, 10 ), 1 ),
    'nth_heptagonal'                : OperatorInfo( lambda n: findNthPolygonalNumber( n, 7 ), 1 ),
    'nth_hexagonal'                 : OperatorInfo( lambda n: findNthPolygonalNumber( n, 6 ), 1 ),
    'nth_nonagonal'                 : OperatorInfo( lambda n: findNthPolygonalNumber( n, 9 ), 1 ),
    'nth_octagonal'                 : OperatorInfo( lambda n: findNthPolygonalNumber( n, 8 ), 1 ),
    'nth_pentagonal'                : OperatorInfo( lambda n: findNthPolygonalNumber( n, 5 ), 1 ),
    'nth_polygonal'                 : OperatorInfo( findNthPolygonalNumber, 2 ),
    'nth_square'                    : OperatorInfo( lambda n: findNthPolygonalNumber( n, 4 ), 1 ),
    'nth_triangular'                : OperatorInfo( lambda n: findNthPolygonalNumber( n, 3 ), 1 ),
    'octagonal'                     : OperatorInfo( lambda n: getNthPolygonalNumber( n, 8 ), 1 ),
    'octagonal_heptagonal'          : OperatorInfo( getNthOctagonalHeptagonalNumber, 1 ),
    'octagonal_hexagonal'           : OperatorInfo( getNthOctagonalHexagonalNumber, 1 ),
    'octagonal_pentagonal'          : OperatorInfo( getNthOctagonalPentagonalNumber, 1 ),
    'octagonal_square'              : OperatorInfo( getNthOctagonalSquareNumber, 1 ),
    'octagonal_triangular'          : OperatorInfo( getNthOctagonalTriangularNumber, 1 ),
    'pentagonal'                    : OperatorInfo( lambda n: getNthPolygonalNumber( n, 5 ), 1 ),
    'pentagonal_square'             : OperatorInfo( getNthPentagonalSquareNumber, 1 ),
    'pentagonal_triangular'         : OperatorInfo( getNthPentagonalTriangularNumber, 1 ),
    'polygonal'                     : OperatorInfo( getNthPolygonalNumber, 2 ),
    'square_triangular'             : OperatorInfo( getNthSquareTriangularNumber, 1 ),
    'triangular'                    : OperatorInfo( lambda n: getNthPolygonalNumber( n, 3 ), 1 ),

    # polyhedral
    'centered_cube'                 : OperatorInfo( getNthCenteredCubeNumber, 1 ),
    'dodecahedral'                  : OperatorInfo( lambda n: polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], real( n ) ), 1 ),
    'icosahedral'                   : OperatorInfo( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], real( n ) ), 1 ),
    'octahedral'                    : OperatorInfo( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], real( n ) ), 1 ),
    'pentatope'                     : OperatorInfo( getNthPentatopeNumber, 1 ),
    'polytope'                      : OperatorInfo( getNthPolytopeNumber, 2 ),
    'pyramid'                       : OperatorInfo( lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1 ),
    'rhombdodec'                    : OperatorInfo( getNthRhombicDodecahedralNumber, 1 ),
    'stella_octangula'              : OperatorInfo( getNthStellaOctangulaNumber, 1 ),
    'tetrahedral'                   : OperatorInfo( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ), 1 ),
    'truncated_octahedral'          : OperatorInfo( getNthTruncatedOctahedralNumber, 1 ),
    'truncated_tetrahedral'         : OperatorInfo( getNthTruncatedTetrahedralNumber, 1 ),

    # powers_and_roots
    'cube'                          : OperatorInfo( lambda n: exponentiate( n, 3 ), 1 ),
    'cube_root'                     : OperatorInfo( lambda n: getRoot( n, 3 ), 1 ),
    'exp'                           : OperatorInfo( exp, 1 ),
    'exp10'                         : OperatorInfo( lambda n: power( 10, n ), 1 ),
    'expphi'                        : OperatorInfo( lambda n: power( phi, n ), 1 ),
    'hyper4_2'                      : OperatorInfo( tetrateLarge, 2 ),
    'power'                         : OperatorInfo( exponentiate, 2 ),
    'powmod'                        : OperatorInfo( getPowMod, 3 ),
    'root'                          : OperatorInfo( lambda n, k: getRoot( n, k ), 2 ),
    'square'                        : OperatorInfo( lambda n: exponentiate( n, 2 ), 1 ),
    'square_root'                   : OperatorInfo( lambda n: getRoot( n, 2 ), 1 ),
    'tetrate'                       : OperatorInfo( tetrate, 2 ),

    # prime_number
    'balanced_prime'                : OperatorInfo( getNthBalancedPrime, 1 ),
    'balanced_prime_'               : OperatorInfo( getNthBalancedPrimeList, 1 ),
    'cousin_prime'                  : OperatorInfo( getNthCousinPrime, 1 ),
    'cousin_prime_'                 : OperatorInfo( getNthCousinPrimeList, 1 ),
    'double_balanced'               : OperatorInfo( getNthDoubleBalancedPrime, 1 ),
    'double_balanced_'              : OperatorInfo( getNthDoubleBalancedPrimeList, 1 ),
    'isolated_prime'                : OperatorInfo( getNthIsolatedPrime, 1 ),
    'next_prime'                    : OperatorInfo( lambda n: findPrime( n )[ 1 ], 1 ),
    'next_quadruplet_prime'         : OperatorInfo( lambda n: findQuadrupletPrimes( n )[ 1 ], 1 ),
    'next_quintuplet_prime'         : OperatorInfo( lambda n: findQuintupletPrimes( n )[ 1 ], 1 ),
    'nth_prime'                     : OperatorInfo( lambda n: findPrime( n )[ 0 ], 1 ),
    'nth_quadruplet_prime'          : OperatorInfo( lambda n: findQuadrupletPrimes( n )[ 0 ], 1 ),
    'nth_quintuplet_prime'          : OperatorInfo( lambda n: findQuintupletPrimes( n )[ 0 ], 1 ),
    'polyprime'                     : OperatorInfo( getNthPolyPrime, 2 ),
    'prime'                         : OperatorInfo( getNthPrime, 1 ),
    'primes'                        : OperatorInfo( getPrimes, 2 ),
    'prime_pi'                      : OperatorInfo( getPrimePi, 1 ),
    'primorial'                     : OperatorInfo( getNthPrimorial, 1 ),
    'quadruplet_prime'              : OperatorInfo( getNthQuadrupletPrime, 1 ),
    'quadruplet_prime_'             : OperatorInfo( getNthQuadrupletPrimeList, 1 ),
    'quintuplet_prime'              : OperatorInfo( getNthQuintupletPrime, 1 ),
    'quintuplet_prime_'             : OperatorInfo( getNthQuintupletPrimeList, 1 ),
    'safe_prime'                    : OperatorInfo( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1 ),
    'sextuplet_prime'               : OperatorInfo( getNthSextupletPrime, 1 ),
    'sextuplet_prime_'              : OperatorInfo( getNthSextupletPrimeList, 1 ),
    'sexy_prime'                    : OperatorInfo( getNthSexyPrime, 1 ),
    'sexy_prime_'                   : OperatorInfo( getNthSexyPrimeList, 1 ),
    'sexy_quadruplet'               : OperatorInfo( getNthSexyQuadruplet, 1 ),
    'sexy_quadruplet_'              : OperatorInfo( getNthSexyQuadrupletList, 1 ),
    'sexy_triplet'                  : OperatorInfo( getNthSexyTriplet, 1 ),
    'sexy_triplet_'                 : OperatorInfo( getNthSexyTripletList, 1 ),
    'sophie_prime'                  : OperatorInfo( getNthSophiePrime, 1 ),
    'superprime'                    : OperatorInfo( getNthSuperPrime, 1 ),
    'triplet_prime'                 : OperatorInfo( getNthTripletPrime, 1 ),
    'triplet_prime_'                : OperatorInfo( getNthTripletPrimeList, 1 ),
    'triple_balanced'               : OperatorInfo( getNthTripleBalancedPrime, 1 ),
    'triple_balanced_'              : OperatorInfo( getNthTripleBalancedPrimeList, 1 ),
    'twin_prime'                    : OperatorInfo( getNthTwinPrime, 1 ),
    'twin_prime_'                   : OperatorInfo( getNthTwinPrimeList, 1 ),

    # settings
    'accuracy'                      : OperatorInfo( lambda n: setAccuracy( fadd( n, 2 ) ), 1 ),
    'comma'                         : OperatorInfo( setComma, 1 ),
    'comma_mode'                    : OperatorInfo( setCommaMode, 0 ),
    'decimal_grouping'              : OperatorInfo( setDecimalGrouping, 1 ),
    'hex_mode'                      : OperatorInfo( setHexMode, 0 ),
    'identify'                      : OperatorInfo( setIdentify, 1 ),
    'identify_mode'                 : OperatorInfo( setIdentifyMode, 0 ),
    'input_radix'                   : OperatorInfo( setInputRadix, 1 ),
    'integer_grouping'              : OperatorInfo( setIntegerGrouping, 1 ),
    'leading_zero'                  : OperatorInfo( setLeadingZero, 1 ),
    'leading_zero_mode'             : OperatorInfo( setLeadingZeroMode, 0 ),
    'octal_mode'                    : OperatorInfo( setOctalMode, 0 ),
    'output_radix'                  : OperatorInfo( setOutputRadix, 1 ),
    'precision'                     : OperatorInfo( setPrecision, 1 ),
    'random'                        : OperatorInfo( rand, 0 ),
    'random_'                       : OperatorInfo( rand_, 1 ),
    'random_integer'                : OperatorInfo( randrange, 1 ),
    'random_integer_'               : OperatorInfo( randrange_, 2 ),
    'timer'                         : OperatorInfo( setTimer, 1 ),
    'timer_mode'                    : OperatorInfo( setTimerMode, 0 ),

    # special
    'estimate'                      : OperatorInfo( estimate, 1 ),
    'help'                          : OperatorInfo( printHelpMessage, 0 ),
    'name'                          : OperatorInfo( getNumberName, 1 ),
    'oeis'                          : OperatorInfo( lambda n: downloadOEISSequence( real_int( n ) ), 1 ),
    'oeis_comment'                  : OperatorInfo( lambda n: downloadOEISText( real_int( n ), 'C', True ), 1 ),
    'oeis_ex'                       : OperatorInfo( lambda n: downloadOEISText( real_int( n ), 'E', True ), 1 ),
    'oeis_name'                     : OperatorInfo( lambda n: downloadOEISText( real_int( n ), 'N', True ), 1 ),
    'ordinal_name'                  : OperatorInfo( getOrdinalName, 1 ),
    'result'                        : OperatorInfo( loadResult, 0 ),
    'set'                           : OperatorInfo( setVariable, 2 ),
    'topic'                         : OperatorInfo( printHelpTopic, 1 ),
    'value'                         : OperatorInfo( lambda n: mpf( n ), 1 ),

    # trigonometry
    'acos'                          : OperatorInfo( lambda n: performTrigOperation( n, acos ), 1 ),
    'acosh'                         : OperatorInfo( lambda n: performTrigOperation( n, acosh ), 1 ),
    'acot'                          : OperatorInfo( lambda n: performTrigOperation( n, acot ), 1 ),
    'acoth'                         : OperatorInfo( lambda n: performTrigOperation( n, acoth ), 1 ),
    'acsc'                          : OperatorInfo( lambda n: performTrigOperation( n, acsc ), 1 ),
    'acsch'                         : OperatorInfo( lambda n: performTrigOperation( n, acsch ), 1 ),
    'asec'                          : OperatorInfo( lambda n: performTrigOperation( n, asec ), 1 ),
    'asech'                         : OperatorInfo( lambda n: performTrigOperation( n, asech ), 1 ),
    'asin'                          : OperatorInfo( lambda n: performTrigOperation( n, asin ), 1 ),
    'asinh'                         : OperatorInfo( lambda n: performTrigOperation( n, asinh ), 1 ),
    'atan'                          : OperatorInfo( lambda n: performTrigOperation( n, atan ), 1 ),
    'atanh'                         : OperatorInfo( lambda n: performTrigOperation( n, atanh ), 1 ),
    'cos'                           : OperatorInfo( lambda n: performTrigOperation( n, cos ), 1 ),
    'cosh'                          : OperatorInfo( lambda n: performTrigOperation( n, cosh ), 1 ),
    'cot'                           : OperatorInfo( lambda n: performTrigOperation( n, cot ), 1 ),
    'coth'                          : OperatorInfo( lambda n: performTrigOperation( n, coth ), 1 ),
    'csc'                           : OperatorInfo( lambda n: performTrigOperation( n, csc ), 1 ),
    'csch'                          : OperatorInfo( lambda n: performTrigOperation( n, csch ), 1 ),
    'hypotenuse'                    : OperatorInfo( hypot, 2 ),
    'sec'                           : OperatorInfo( lambda n: performTrigOperation( n, sec ), 1 ),
    'sech'                          : OperatorInfo( lambda n: performTrigOperation( n, sech ), 1 ),
    'sin'                           : OperatorInfo( lambda n: performTrigOperation( n, sin ), 1 ),
    'sinh'                          : OperatorInfo( lambda n: performTrigOperation( n, sinh ), 1 ),
    'tan'                           : OperatorInfo( lambda n: performTrigOperation( n, tan ), 1 ),
    'tanh'                          : OperatorInfo( lambda n: performTrigOperation( n, tanh ), 1 ),

    # internal
    '_dump_aliases'                 : OperatorInfo( dumpAliases, 0 ),
    '_dump_operators'               : OperatorInfo( dumpOperators, 0 ),
    '_stats'                        : OperatorInfo( dumpStats, 0 ),

#   'antitet'                       : OperatorInfo( findTetrahedralNumber, 0 ),
#   'bernfrac'                      : OperatorInfo( bernfrac, 1 ),
}

