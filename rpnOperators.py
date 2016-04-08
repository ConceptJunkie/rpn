#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import difflib
import inspect
import itertools
import struct

from enum import Enum
from random import randrange

from mpmath import acosh, acot, acoth, acsc, acsch, agm, arg, asec, asech, \
                   asin, asinh, atan, atanh, conj, cosh, cos, coth, csc, csch, \
                   fac2, fadd, fmod, floor, harmonic, hyperfac, lambertw, li, \
                   limit, ln, loggamma, nprod, nsum, polylog, plot, psi, rand, \
                   sec, sech, sin, sinh, superfac, tan, tanh, unitroots, zeta

from rpnAliases import dumpAliases

from rpnAstronomy import *
from rpnCalendar import *
from rpnCombinatorics import *
from rpnComputer import *
from rpnConstants import *
from rpnConstantUtils import *
from rpnDateTime import *
from rpnDice import *
from rpnDeclarations import *
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
from rpnPersistence import *
from rpnPhysics import *
from rpnPolynomials import *
from rpnPolytope import *
from rpnPrimeUtils import *
from rpnSettings import *
from rpnUtils import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNFunctionInfo
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  RPNFunctionInfo object.  However, it can't know how many of them it
# //  actually needs until it's time to evaluate the function, so we need to
# //  save all the terms we have so far, since we can't know until later how
# //  many of them we will need.
# //
# //  Once we are able to parse out how many arguments belong to the function
# //  declaration, then we can determine what arguments are left over to be used
# //  with the function operation.   All function operations take at least one
# //  argument before the function declaration.
# //
# //******************************************************************************

class RPNFunctionInfo( object ):
    """This class represents a user-defined function in rpn."""
    def __init__( self, valueList, startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        else:
            self.valueList.append( valueList )

        self.startingIndex = startingIndex
        self.code = ''
        self.code_locals = { }
        self.compiled = None
        self.function = None
        self.argCount = 0

    def add( self, arg ):
        self.valueList.append( arg )

    def evaluate( self, x, y = 0, z = 0 ):
        if not self.function:
            self.compile( )

        if self.argCount == 1:
            return self.function( x )
        elif self.argCount == 2:
            return self.function( x, y )
        elif self.argCount == 3:
            return self.function( x, y, z )

    def getFunction( self ):
        if not self.function:
            self.compile( )

        return self.function

    def compile( self ):
        valueList = [ ]

        xArg = False
        yArg = False
        zArg = False

        for index, item in enumerate( self.valueList ):
            if index < self.startingIndex:
                continue

            if item == 'x':
                xArg = True
            elif item == 'y':
                yArg = True
            elif item == 'z':
                zArg = True

            valueList.append( item )

        self.code = 'def rpnInternalFunction('

        first = True

        self.argCount = 0

        if xArg:
            self.code += ' x'
            first = False
            self.argCount += 1

        if yArg:
            if first:
                first = False
            else:
                self.code += ','

            self.code += ' y'
            self.argCount += 1

        if zArg:
            if not first:
                self.code += ','

            self.code += ' z'
            self.argCount += 1

        self.code += ' ): return '

        args = [ ]

        debugPrint( 'terms', valueList )

        while valueList:
            term = valueList.pop( 0 )
            debugPrint( 'term:', term, 'args:', args )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            if term in operators:
                function = operators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( operators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperatorInfo'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = operators[ term ].argCount

                if len( args ) < operands:
                    raise ValueError( '{1} expects {2} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                args.append( function )

                if not valueList:
                    self.code += function
            else:
                args.append( term )

        debugPrint( 'valueList:', self.valueList[ self.startingIndex : ] )
        debugPrint( 'code:', self.code )

        self.compiled = compile( self.code, '<string>', 'exec' )

        exec( self.compiled, globals( ), self.code_locals )
        self.function = self.code_locals[ 'rpnInternalFunction' ]


# //******************************************************************************
# //
# //  createFunction
# //
# //  This only gets called if we are not already creating a function.
# //
# //******************************************************************************

def createFunction( valueList ):
    g.creatingFunction = True
    valueList.append( RPNFunctionInfo( valueList, len( valueList ) ) )


# //******************************************************************************
# //
# //  addX
# //
# //******************************************************************************

def addX( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'x\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'x' )


# //******************************************************************************
# //
# //  addY
# //
# //******************************************************************************

def addY( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'y\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'y' )


# //******************************************************************************
# //
# //  addZ
# //
# //******************************************************************************

def addZ( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'z\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'z' )


# //******************************************************************************
# //
# //  plotFunction
# //
# //******************************************************************************

def plotFunction( start, end, func ):
    plot( lambda x: func.evaluate( x, func ), [ start, end ] )
    return 0


# //******************************************************************************
# //
# //  plot2DFunction
# //
# //******************************************************************************

def plot2DFunction( start1, end1, start2, end2, func ):
    splot( lambda x, y: func.evaluate( x, y ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


# //******************************************************************************
# //
# //  plotComplexFunction
# //
# //******************************************************************************

def plotComplexFunction( start1, end1, start2, end2, func ):
    cplot( lambda x: func.evaluate( x ),
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ],
           points = 10000 )
    return 0


# //******************************************************************************
# //
# //  filterList
# //
# //******************************************************************************

def filterList( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunctionInfo ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )
        else:
            raise ValueError( '\'filter\' expects a function argument' )

    result = [ ]

    if isinstance( n, RPNGenerator ):
        return RPNGenerator.createFilter( n.generator, k.getFunction( ) )

    for i in n:
        value = k.evaluate( i )

        if ( value != 0 ) != invert:
            result.append( i )

    return result


# //******************************************************************************
# //
# //  filterListByIndex
# //
# //******************************************************************************

def filterListByIndex( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunctionInfo ):
        if invert:
            raise ValueError( '\'unfilter_by_index\' expects a function argument' )
        else:
            raise ValueError( '\'filter_by_index\' expects a function argument' )

    result = [ ]

    for index, item in enumerate( n ):
        value = k.evaluate( index )

        if ( value != 0 ) != invert:
            result.append( item )

    return result


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
            newResult.append( item.getValue( ) )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    currentValueList.append( newResult )

    return True


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

    return RPNVariable( term[ 1 : ] )


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
                arg = checkForVariable( currentValueList.pop( ) )

                if term != 'set' and isinstance( arg, RPNVariable ):
                    arg = arg.getValue( )

            argList.append( arg if isinstance( arg, list ) else [ arg ] )

        result = callers[ argsNeeded ]( operatorInfo.function, *argList )

    newResult = list( )

    if not isinstance( result, list ):
        result = [ result ]

    for item in result:
        if isinstance( item, RPNMeasurement ) and item.getUnits( ) == { }:
            newResult.append( item.value )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    if term not in sideEffectOperators:
        currentValueList.append( newResult )

    return True


# //******************************************************************************
# //
# //  handleOneArgListOperator
# //
# //  Each operator is going to have to be responsible for how it handles
# //  recursive lists.  In some cases, handling recursive lists makes sense.
# //
# //******************************************************************************

def handleOneArgListOperator( func, args, currentValueList ):
    recursive = False

    if isinstance( args, RPNGenerator ):
        args = list( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if not isinstance( args, list ):
        currentValueList.append( func( [ args ] ) )
    else:
        currentValueList.append( func( args ) )


# //******************************************************************************
# //
# //  handleOneArgGeneratorOperator
# //
# //******************************************************************************

def handleOneArgGeneratorOperator( func, args, currentValueList ):
    recursive = False

    if isinstance( args, list ):
        args = RPNGenerator.create( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if not isinstance( args, RPNGenerator ):
        currentValueList.append( func( RPNGenerator.create( ) ) )
    else:
        currentValueList.append( func( args ) )


# //******************************************************************************
# //
# //  handleMultiArgListOperator
# //
# //  Each operator is going to have to be responsible for how it handles
# //  recursive lists.  In some cases, handling recursive lists makes sense.
# //
# //******************************************************************************

def handleMultiArgListOperator( func, argList, currentValueList ):
    newArgList = [ ]

    for arg in argList:
        if isinstance( arg, RPNGenerator ):
            newArgList.append( list( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


# //******************************************************************************
# //
# //  handleMultiArgGeneratorOperator
# //
# //******************************************************************************

def handleMultiArgGeneratorOperator( func, args, currentValueList ):
    newArgList = [ ]

    for arg in args:
        if isinstance( arg, list ):
            newArgList.append( RPNGenerator.create( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


# //******************************************************************************
# //
# //  evaluateListOperator
# //
# //******************************************************************************

def evaluateListOperator( term, index, currentValueList ):
    # handle a list operator
    operatorInfo = listOperators[ term ]
    argsNeeded = operatorInfo.argCount
    argTypes = operatorInfo.argTypes

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    # handle the call depending on the number of arguments needed
    if argsNeeded == 0:
        currentValueList.append( operatorInfo.function( currentValueList ) )
    elif argsNeeded == 1:
        args = currentValueList.pop( )

        if argTypes[ 0 ] == RPNOperatorType.Generator:
            handleOneArgGeneratorOperator( operatorInfo.function, args, currentValueList )
        else:
            handleOneArgListOperator( operatorInfo.function, args, currentValueList )
    else:
        argList = [ ]

        for i in range( 0, argsNeeded ):
            argList.insert( 0, currentValueList.pop( ) )

        if argTypes[ 0 ] == RPNOperatorType.Generator:
            handleMultiArgGeneratorOperator( operatorInfo.function, argList, currentValueList )
        else:
            handleMultiArgListOperator( operatorInfo.function, argList, currentValueList )

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
# //  evaluateOneArgFunction
# //
# //******************************************************************************

def evaluateOneArgFunction( func, args, level = 0 ):
    if isinstance( args, list ):
        result = [ evaluateOneArgFunction( func, i, level + 1 ) for i in args ]
    elif isinstance( args, RPNGenerator ):
        result =  RPNGenerator.createChained( args.getGenerator( ), func )
    else:
        result = func( args )

    # if this is the 'echo' operator, just return the result
    if func.__name__ == 'addEchoArgument':
        return result

    # otherwise, check for arguments to be echoed, and echo them before the result
    if level == 0 and not g.operatorList and len( g.echoArguments ) > 0:
        returnValue = list( g.echoArguments )
        returnValue.append( result )
        g.echoArguments = [ ]
        return returnValue
    else:
        return result


# //******************************************************************************
# //
# //  evaluateTwoArgFunction
# //
# //  This seems somewhat non-pythonic...
# //
# //******************************************************************************

def evaluateTwoArgFunction( func, _arg1, _arg2, level = 0 ):
    if isinstance( _arg1, list ):
        len1 = len( _arg1 )

        if len1 == 1:
            arg1 = _arg1[ 0 ]
            list1 = False
        else:
            arg1 = _arg1
            list1 = True

        generator1 = False
    else:
        arg1 = _arg1
        list1 = False

    generator1 = isinstance( arg1, RPNGenerator )

    if isinstance( _arg2, list ):
        len2 = len( _arg2 )

        if len2 == 1:
            arg2 = _arg2[ 0 ]
            list2 = False
        else:
            arg2 = _arg2
            list2 = True

        generator2 = False
    else:
        arg2 = _arg2
        list2 = False

    generator2 = isinstance( arg2, RPNGenerator )

    if generator1:
        if generator2:
            iter1 = iter( arg1 )
            iter2 = iter( arg2 )

            result = [ ]

            while True:
                try:
                    i1 = iter1.__next__( )
                    i2 = iter2.__next__( )

                    result.append( func( i1, i2 ) )
                except:
                    break
        else:
            result = [ evaluateTwoArgFunction( func, i, arg2, level + 1 ) for i in arg1.getGenerator( ) ]
    elif generator2:
        result = [ evaluateTwoArgFunction( func, arg1, i, level + 1 ) for i in arg2.getGenerator( ) ]
    elif list1:
        if list2:
            result = [ evaluateTwoArgFunction( func, arg1[ index ], arg2[ index ], level + 1 ) for index in range( 0, min( len1, len2 ) ) ]
        else:
            result = [ evaluateTwoArgFunction( func, i, arg2, level + 1 ) for i in arg1 ]

    else:
        if list2:
            result = [ evaluateTwoArgFunction( func, arg1, j, level + 1 ) for j in arg2 ]
        else:
            result = func( arg2, arg1 )

    # check for arguments to be echoed, and echo them before the result
    if level == 0 and not g.operatorList and len( g.echoArguments ) > 0:
        returnValue = list( g.echoArguments )
        returnValue.append( result )
        g.echoArguments = [ ]
        return returnValue
    else:
        return result


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

def evaluateTerm( term, index, currentValueList, lastArg = True ):
    isList = isinstance( term, list )
    isGenerator = isinstance( term, RPNGenerator )

    try:
        # handle a modifier operator
        if not isList and not isGenerator and term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )
        elif not isList and term in g.unitOperatorNames or \
             ( '*' in term or '^' in term or '/' in term ) and \
             any( c in term for c in string.ascii_letters ):

            # handle a unit operator
            if not g.unitOperators:
                loadUnitData( )

            if term not in g.unitOperatorNames:
                term = RPNUnits( term )

            # look for unit without a value (in which case we give it a value of 1)
            if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], RPNMeasurement ) or \
                isinstance( currentValueList[ -1 ], RPNDateTime ) or ( isinstance( currentValueList[ -1 ], list ) and
                                                                       isinstance( currentValueList[ -1 ][ 0 ], RPNMeasurement ) ):
                    currentValueList.append( applyNumberValueToUnit( 1, term ) )
            # if the unit comes after a generator, convert it to a list and apply the unit to each
            elif isinstance( currentValueList[ -1 ], RPNGenerator ):
                newArg = [ ]

                for value in list( currentValueList.pop( ) ):
                    newArg.append( applyNumberValueToUnit( value, term ) )

                currentValueList.append( newArg )
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
        elif term in constants:
            if not g.unitOperators:
                loadUnitData( )

            if not evaluateConstantOperator( term, index, currentValueList ):
                return False
        elif term in operators:
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
        elif term in listOperators:
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
                if not lastArg:
                    currentValueList.append( term )
                    return True

                # build keyword list if needed
                if len( g.keywords ) == 0:
                    g.keywords = list( operators.keys( ) )
                    g.keywords.extend( list( listOperators.keys( ) ) )
                    g.keywords.extend( constants )
                    g.keywords.extend( g.unitOperatorNames )
                    g.keywords.extend( g.operatorAliases )

                guess = difflib.get_close_matches( term, g.keywords, 1 )

                if ( len( guess ) == 1 ):
                    guess = guess[ 0 ]

                    if guess in g.operatorAliases:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  Did you mean \'{1}\', i.e., an alias for \'{2}\'?'.format( term, guess, g.operatorAliases[ guess ] ) )
                    else:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  Did you mean \'{1}\'?'.format( term, guess ) )
                else:
                    print( 'rpn:  Unrecognized operator \'{0}\'.'.format( term ) )

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
    'dup_term'          : RPNOperatorInfo( duplicateTerm, 1 ),

    'dup_operator'      : RPNOperatorInfo( duplicateOperation, 1 ),

    'previous'          : RPNOperatorInfo( getPrevious, 0 ),

    'unlist'            : RPNOperatorInfo( unlist, 0 ),

    #'for_each'          : RPNOperatorInfo( forEach, 0 ),

    'lambda'            : RPNOperatorInfo( createFunction, 0 ),

    'x'                 : RPNOperatorInfo( addX, 0 ),

    'y'                 : RPNOperatorInfo( addY, 0 ),

    'z'                 : RPNOperatorInfo( addZ, 0 ),

    '['                 : RPNOperatorInfo( incrementNestedListLevel, 0 ),

    ']'                 : RPNOperatorInfo( decrementNestedListLevel, 0 ),

    '{'                 : RPNOperatorInfo( startOperatorList, 0 ),

    '}'                 : RPNOperatorInfo( endOperatorList, 0 ),
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
    'add_polynomials'       : RPNOperatorInfo( addPolynomials,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'eval_polynomial'       : RPNOperatorInfo( evaluatePolynomial,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'multiply_polynomials'  : RPNOperatorInfo( multiplyPolynomials,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'polynomial_power'      : RPNOperatorInfo( exponentiatePolynomial,
                                               2, [ RPNOperatorType.List, RPNOperatorType.PositiveInteger ] ),

    'polynomial_product'    : RPNOperatorInfo( multiplyListOfPolynomials,
                                               1, [ RPNOperatorType.List ] ),

    'polynomial_sum'        : RPNOperatorInfo( addListOfPolynomials,
                                               1, [ RPNOperatorType.List ] ),

    'solve'                 : RPNOperatorInfo( solvePolynomial,
                                               1, [ RPNOperatorType.List ] ),

    # arithmetic
    'gcd'                   : RPNOperatorInfo( getGCD,
                                               1, [ RPNOperatorType.List ] ),

    'lcm'                   : RPNOperatorInfo( getLCM,
                                               1, [ RPNOperatorType.List ] ),

    'max'                   : RPNOperatorInfo( max,
                                               1, [ RPNOperatorType.List ] ),

    'mean'                  : RPNOperatorInfo( calculateArithmeticMean,
                                               1, [ RPNOperatorType.List ] ),

    'geometric_mean'        : RPNOperatorInfo( calculateGeometricMean,
                                               1, [ RPNOperatorType.List ] ),

    'min'                   : RPNOperatorInfo( min,
                                               1, [ RPNOperatorType.List ] ),

    'product'               : RPNOperatorInfo( getProduct,
                                               1, [ RPNOperatorType.List ] ),

    'stddev'                : RPNOperatorInfo( getStandardDeviation,
                                               1, [ RPNOperatorType.List ] ),

    'sum'                   : RPNOperatorInfo( getSum,
                                               1, [ RPNOperatorType.List ] ),

    # combinatoric
    'multinomial'           : RPNOperatorInfo( getMultinomial,
                                               1, [ RPNOperatorType.List ] ),

    # conversion
    'convert'               : RPNOperatorInfo( convertUnits,
                                               2, [ RPNOperatorType.List ] ),   # list arguments are special

    'latlong_to_nac'        : RPNOperatorInfo( convertLatLongToNAC,
                                               1, [ RPNOperatorType.List ] ),

    'unpack'                : RPNOperatorInfo( unpackInteger,
                                               2, [ RPNOperatorType.List ] ),

    'pack'                  : RPNOperatorInfo( packInteger,
                                               2, [ RPNOperatorType.List ] ),

    # date_time
    'make_datetime'         : RPNOperatorInfo( makeDateTime,
                                               1, [ RPNOperatorType.List ] ),

    'make_iso_time'         : RPNOperatorInfo( makeISOTime,
                                               1, [ RPNOperatorType.List ] ),

    'make_julian_time'      : RPNOperatorInfo( makeJulianTime,
                                               1, [ RPNOperatorType.List ] ),

    # function
    'filter'                : RPNOperatorInfo( filterList,
                                               2, [ RPNOperatorType.Generator, RPNOperatorType.Function ] ),

    'filter_by_index'       : RPNOperatorInfo( filterListByIndex,
                                               2, [ RPNOperatorType.List, RPNOperatorType.Function ] ),

    'unfilter'              : RPNOperatorInfo( lambda n, k: filterList( n, k, True ),
                                               2, [ RPNOperatorType.List, RPNOperatorType.Function ] ),

    'unfilter_by_index'     : RPNOperatorInfo( lambda n, k: filterListByIndex( n, k, True ),
                                               2, [ RPNOperatorType.List, RPNOperatorType.Function ] ),

    # list
    'alternate_signs'       : RPNOperatorInfo( lambda n: RPNGenerator( alternateSigns( n, False ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'alternate_signs_2'     : RPNOperatorInfo( lambda n: RPNGenerator( alternateSigns( n, True ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'alternating_sum'       : RPNOperatorInfo( lambda n: getAlternatingSum( n, False ),
                                               1, [ RPNOperatorType.Generator ] ),

    'alternating_sum_2'     : RPNOperatorInfo( lambda n: getAlternatingSum( n, False ),
                                               1, [ RPNOperatorType.Generator ] ),

    'and_all'               : RPNOperatorInfo( getAndAll,
                                               1, [ RPNOperatorType.List ] ),

    'append'                : RPNOperatorInfo( appendLists,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'collate'               : RPNOperatorInfo( collate,
                                               1, [ RPNOperatorType.List ] ),

    'count'                 : RPNOperatorInfo( countElements,
                                               1, [ RPNOperatorType.Generator ] ),

    'diffs'                 : RPNOperatorInfo( lambda n: RPNGenerator( getListDiffs( n ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'diffs2'                : RPNOperatorInfo( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'element'               : RPNOperatorInfo( getListElement,
                                               2, [ RPNOperatorType.List, RPNOperatorType.NonnegativeInteger ] ),

    'flatten'               : RPNOperatorInfo( flatten,
                                               1, [ RPNOperatorType.List ] ),

    'group_elements'        : RPNOperatorInfo( groupElements,
                                               2, [ RPNOperatorType.List ] ),

    'interleave'            : RPNOperatorInfo( interleave,
                                               2, [ RPNOperatorType.List ] ),

    'intersection'          : RPNOperatorInfo( makeIntersection,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'left'                  : RPNOperatorInfo( getLeft,
                                               2, [ RPNOperatorType.List ] ),

    'max_index'             : RPNOperatorInfo( getIndexOfMax,
                                               1, [ RPNOperatorType.List ] ),

    'min_index'             : RPNOperatorInfo( getIndexOfMin,
                                               1, [ RPNOperatorType.List ] ),

    'nand_all'              : RPNOperatorInfo( getNandAll,
                                               1, [ RPNOperatorType.List ] ),

    'nonzero'               : RPNOperatorInfo( getNonzeroes,
                                               1, [ RPNOperatorType.List ] ),

    'nor_all'               : RPNOperatorInfo( getNorAll,
                                               1, [ RPNOperatorType.List ] ),

    'occurrences'           : RPNOperatorInfo( getOccurrences,
                                               1, [ RPNOperatorType.List ] ),

    'occurrence_cumulative' : RPNOperatorInfo( getCumulativeOccurrenceRatios,
                                               1, [ RPNOperatorType.List ] ),

    'occurrence_ratios'     : RPNOperatorInfo( getOccurrenceRatios,
                                               1, [ RPNOperatorType.List ] ),

    'or_all'                : RPNOperatorInfo( getOrAll,
                                               1, [ RPNOperatorType.List ] ),

    'ratios'                : RPNOperatorInfo( lambda n: RPNGenerator( getListRatios( n ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'ratios2'               : RPNOperatorInfo( lambda n: RPNGenerator( getCumulativeListRatios( n ) ),
                                               1, [ RPNOperatorType.Generator ] ),

    'reduce'                : RPNOperatorInfo( reduceList,
                                               1, [ RPNOperatorType.List ] ),

    'reverse'               : RPNOperatorInfo( getReverse,
                                               1, [ RPNOperatorType.List ] ),

    'right'                 : RPNOperatorInfo( getRight,
                                               2, [ RPNOperatorType.List ] ),

    'shuffle'               : RPNOperatorInfo( shuffleList,
                                               1, [ RPNOperatorType.List ] ),

    'slice'                 : RPNOperatorInfo( getSlice,
                                               3, [ RPNOperatorType.List, RPNOperatorType.Integer, RPNOperatorType.Integer ] ),

    'sort'                  : RPNOperatorInfo( sortAscending,
                                               1, [ RPNOperatorType.List ] ),

    'sort_descending'       : RPNOperatorInfo( sortDescending,
                                               1, [ RPNOperatorType.List ] ),

    'sublist'               : RPNOperatorInfo( getSublist,
                                               3, [ RPNOperatorType.List, RPNOperatorType.Integer, RPNOperatorType.Integer ] ),

    'union'                 : RPNOperatorInfo( makeUnion,
                                               2, [ RPNOperatorType.List, RPNOperatorType.List ] ),

    'unique'                : RPNOperatorInfo( getUniqueElements,
                                               1, [ RPNOperatorType.List ] ),

    'zero'                  : RPNOperatorInfo( getZeroes,
                                               1, [ RPNOperatorType.List ] ),

    # number_theory
    'base'                  : RPNOperatorInfo( interpretAsBase,
                                               2, [ RPNOperatorType.List ] ),

    'cf'                    : RPNOperatorInfo( convertFromContinuedFraction,
                                               1, [ RPNOperatorType.List ] ),

    'crt'                   : RPNOperatorInfo( calculateChineseRemainderTheorem,
                                               2, [ RPNOperatorType.List ] ),

    'frobenius'             : RPNOperatorInfo( getFrobeniusNumber,
                                               1, [ RPNOperatorType.List ] ),

    'linear_recurrence'     : RPNOperatorInfo( getNthLinearRecurrence,
                                               3, [ RPNOperatorType.List ] ),

    # lexicographic
    'combine_digits'        : RPNOperatorInfo( combineDigits,
                                               1, [ RPNOperatorType.Generator ] ),

    # powers_and_roots
    'tower'                 : RPNOperatorInfo( calculatePowerTower,
                                               1, [ RPNOperatorType.List ] ),

    'tower2'                : RPNOperatorInfo( calculatePowerTower2,
                                               1, [ RPNOperatorType.List ] ),

    # special
    'echo'                  : RPNOperatorInfo( addEchoArgument,
                                               1, [ RPNOperatorType.Default ] ),
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
    'find_polynomial'               : RPNOperatorInfo( findPolynomial,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.PositiveInteger ] ),

    'solve_cubic'                   : RPNOperatorInfo( solveCubicPolynomial,
                                                       4, [ RPNOperatorType.Default, RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Default ] ),

    'solve_quadratic'               : RPNOperatorInfo( solveQuadraticPolynomial,
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'solve_quartic'                 : RPNOperatorInfo( solveQuarticPolynomial,
                                                       5, [ RPNOperatorType.Default, RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Default, RPNOperatorType.Default ] ),

    # arithmetic
    'abs'                           : RPNOperatorInfo( fabs,
                                                       1, [ RPNOperatorType.Default ] ),

    'add'                           : RPNOperatorInfo( add,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'ceiling'                       : RPNOperatorInfo( ceil,
                                                       1, [ RPNOperatorType.Default ] ),

    'decrement'                     : RPNOperatorInfo( lambda n: subtract( n, 1 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'divide'                        : RPNOperatorInfo( divide,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'floor'                         : RPNOperatorInfo( floor,
                                                       1, [ RPNOperatorType.Default ] ),

    'increment'                     : RPNOperatorInfo( lambda n: add( n, 1 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'is_divisible'                  : RPNOperatorInfo( isDivisible,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'is_equal'                      : RPNOperatorInfo( isEqual,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'is_even'                       : RPNOperatorInfo( lambda n: 1 if fmod( real( n ), 2 ) == 0 else 0,
                                                       1, [ RPNOperatorType.Real ] ),

    'is_greater'                    : RPNOperatorInfo( isGreater,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'is_less'                       : RPNOperatorInfo( isLess,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'is_not_equal'                  : RPNOperatorInfo( isNotEqual,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'is_not_greater'                : RPNOperatorInfo( isNotGreater,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'is_not_less'                   : RPNOperatorInfo( isNotLess,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'is_not_zero'                   : RPNOperatorInfo( lambda n: 0 if n == 0 else 1,
                                                       1, [ RPNOperatorType.Default ] ),

    'is_odd'                        : RPNOperatorInfo( lambda n: 1 if fmod( real( n ), 2 ) == 1 else 0,
                                                       1, [ RPNOperatorType.Real ] ),

    'is_square'                     : RPNOperatorInfo( isSquare,
                                                       1, [ RPNOperatorType.Default ] ),

    'is_zero'                       : RPNOperatorInfo( lambda n: 1 if n == 0 else 0,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'larger'                        : RPNOperatorInfo( getLarger,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'modulo'                        : RPNOperatorInfo( lambda n, k: fmod( real( n ), real( k ) ),
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'multiply'                      : RPNOperatorInfo( multiply,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'nearest_int'                   : RPNOperatorInfo( nint,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'negative'                      : RPNOperatorInfo( getNegative,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'reciprocal'                    : RPNOperatorInfo( takeReciprocal,
                                                       1, [ RPNOperatorType.Default ] ),

    'round'                         : RPNOperatorInfo( lambda n: floor( fadd( n, 0.5 ) ),
                                                       1, [ RPNOperatorType.Default ] ),

    'sign'                          : RPNOperatorInfo( getSign,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'smaller'                       : RPNOperatorInfo( getSmaller,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'subtract'                      : RPNOperatorInfo( subtract,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    # astronomy
    'antitransit_time'              : RPNOperatorInfo( getAntitransitTime,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'astronomical_dawn'             : RPNOperatorInfo( lambda n, k: getNextDawn( n, k, -18 ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'astronomical_dusk'             : RPNOperatorInfo( lambda n, k: getNextDawn( n, k, -18 ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'autumnal_equinox'              : RPNOperatorInfo( getAutumnalEquinox,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'dawn'                          : RPNOperatorInfo( getNextDawn,
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'day_time'                      : RPNOperatorInfo( lambda n, k: getTransitTime( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'dusk'                          : RPNOperatorInfo( getNextDusk,
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'moonrise'                      : RPNOperatorInfo( lambda n, k: getNextRising( ephem.Moon( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'moonset'                       : RPNOperatorInfo( lambda n, k: getNextSetting( ephem.Moon( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'moon_antitransit'              : RPNOperatorInfo( lambda n, k: getNextAntitransit( ephem.Moon( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'moon_phase'                    : RPNOperatorInfo( getMoonPhase,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'moon_transit'                  : RPNOperatorInfo( lambda n, k: getNextTransit( ephem.Moon( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'nautical_dawn'                 : RPNOperatorInfo( lambda n, k: getNextDawn( n, k, -12 ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'nautical_dusk'                 : RPNOperatorInfo( lambda n, k: getNextDawn( n, k, -12 ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'next_antitransit'              : RPNOperatorInfo( getNextAntitransit,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'next_first_quarter_moon'       : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.next_first_quarter_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'next_full_moon'                : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.next_full_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'next_last_quarter_moon'        : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.next_last_quarter_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'next_new_moon'                 : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.next_new_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'next_rising'                   : RPNOperatorInfo( getNextRising,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'next_setting'                  : RPNOperatorInfo( getNextSetting,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'next_transit'                  : RPNOperatorInfo( getNextTransit,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'night_time'                    : RPNOperatorInfo( lambda n, k: getAntitransitTime( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'previous_antitransit'          : RPNOperatorInfo( getPreviousAntitransit,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'previous_first_quarter_moon'   : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.previous_first_quarter_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'previous_full_moon'            : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.previous_full_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'previous_last_quarter_moon'    : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.previous_last_quarter_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'previous_new_moon'             : RPNOperatorInfo( lambda n: getEphemTime( n, ephem.previous_new_moon ),
                                                       1, [ RPNOperatorType.DateTime ] ),

    'previous_rising'               : RPNOperatorInfo( getPreviousRising,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'previous_setting'              : RPNOperatorInfo( getPreviousSetting,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'previous_transit'              : RPNOperatorInfo( getPreviousTransit,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'sky_location'                  : RPNOperatorInfo( getSkyLocation,
                                                       2, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.DateTime ] ),

    'solar_noon'                    : RPNOperatorInfo( lambda n, k: getNextTransit( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'summer_solstice'               : RPNOperatorInfo( getSummerSolstice,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sunrise'                       : RPNOperatorInfo( lambda n, k: getNextRising( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'sunset'                        : RPNOperatorInfo( lambda n, k: getNextSetting( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'sun_antitransit'               : RPNOperatorInfo( lambda n, k: getNextAntitransit( ephem.Sun( ), n, k ),
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.DateTime ] ),

    'transit_time'                  : RPNOperatorInfo( getTransitTime,
                                                       3, [ RPNOperatorType.AstronomicalObject, RPNOperatorType.Location,
                                                            RPNOperatorType.DateTime ] ),

    'vernal_equinox'                : RPNOperatorInfo( getVernalEquinox,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'winter_solstice'               : RPNOperatorInfo( getWinterSolstice,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    # astronomy - heavenly body operators
    'sun'                           : RPNOperatorInfo( ephem.Sun,
                                                       0, [ ] ),

    'mercury'                       : RPNOperatorInfo( ephem.Mercury,
                                                       0, [ ] ),

    'venus'                         : RPNOperatorInfo( ephem.Venus,
                                                       0, [ ] ),

    'moon'                          : RPNOperatorInfo( ephem.Moon,
                                                       0, [ ] ),

    'mars'                          : RPNOperatorInfo( ephem.Mars,
                                                       0, [ ] ),

    'jupiter'                       : RPNOperatorInfo( ephem.Jupiter,
                                                       0, [ ] ),

    'saturn'                        : RPNOperatorInfo( ephem.Saturn,
                                                       0, [ ] ),

    'uranus'                        : RPNOperatorInfo( ephem.Uranus,
                                                       0, [ ] ),

    'neptune'                       : RPNOperatorInfo( ephem.Neptune,
                                                       0, [ ] ),

    'pluto'                         : RPNOperatorInfo( ephem.Pluto,
                                                       0, [ ] ),


    # bitwise
    'and'                           : RPNOperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x & y ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'count_bits'                    : RPNOperatorInfo( getBitCount,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'nand'                          : RPNOperatorInfo( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x & y ) ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'nor'                           : RPNOperatorInfo( lambda n, k: getInvertedBits( performBitwiseOperation( n, k, lambda x, y: x | y ) ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'not'                           : RPNOperatorInfo( getInvertedBits,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'or'                            : RPNOperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x | y ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'parity'                        : RPNOperatorInfo( lambda n: getBitCount( n ) & 1,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'shift_left'                    : RPNOperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x << y ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'shift_right'                   : RPNOperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x >> y ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'xor'                           : RPNOperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y: x ^ y ),
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    # calendar
    'ash_wednesday'                 : RPNOperatorInfo( calculateAshWednesday,
                                                       1, [ RPNOperatorType.Integer ] ),

    'calendar'                      : RPNOperatorInfo( generateMonthCalendar,
                                                       1, [ RPNOperatorType.Integer ] ),

    'dst_end'                       : RPNOperatorInfo( calculateDSTEnd,
                                                       1, [ RPNOperatorType.Integer ] ),

    'dst_start'                     : RPNOperatorInfo( calculateDSTStart,
                                                       1, [ RPNOperatorType.Integer ] ),

    'easter'                        : RPNOperatorInfo( calculateEaster,
                                                       1, [ RPNOperatorType.Integer ] ),

    'election_day'                  : RPNOperatorInfo( calculateElectionDay,
                                                       1, [ RPNOperatorType.Integer ] ),

    'from_bahai'                    : RPNOperatorInfo( convertBahaiDate,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_hebrew'                   : RPNOperatorInfo( convertHebrewDate,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_indian_civil'             : RPNOperatorInfo( convertIndianCivilDate,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_islamic'                  : RPNOperatorInfo( convertIslamicDate,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_julian'                   : RPNOperatorInfo( convertJulianDate,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_mayan'                    : RPNOperatorInfo( convertMayanDate,
                                                       5, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger,
                                                            RPNOperatorType.PositiveInteger ] ),

    'from_persian'                  : RPNOperatorInfo( convertPersianDate,
                                                       3, [ RPNOperatorType.Integer, RPNOperatorType.Integer, RPNOperatorType.Integer ] ),

    'iso_date'                      : RPNOperatorInfo( getISODate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'labor_day'                     : RPNOperatorInfo( calculateLaborDay,
                                                       1, [ RPNOperatorType.Integer ] ),

    'memorial_day'                  : RPNOperatorInfo( calculateMemorialDay,
                                                       1, [ RPNOperatorType.Integer ] ),

    'nth_weekday'                   : RPNOperatorInfo( calculateNthWeekdayOfMonth,
                                                       4, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger, RPNOperatorType.Integer, RPNOperatorType.PositiveInteger ] ),

    'nth_weekday_of_year'           : RPNOperatorInfo( calculateNthWeekdayOfYear,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.Integer, RPNOperatorType.PositiveInteger ] ),

    'presidents_day'                : RPNOperatorInfo( calculatePresidentsDay,
                                                       1, [ RPNOperatorType.Integer ] ),

    'thanksgiving'                  : RPNOperatorInfo( calculateThanksgiving,
                                                       1, [ RPNOperatorType.Integer ] ),

    'to_bahai'                      : RPNOperatorInfo( getBahaiCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_bahai_name'                 : RPNOperatorInfo( getBahaiCalendarDateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_hebrew'                     : RPNOperatorInfo( getHebrewCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_hebrew_name'                : RPNOperatorInfo( getHebrewCalendarDateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_indian_civil'               : RPNOperatorInfo( getIndianCivilCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_indian_civil_name'          : RPNOperatorInfo( getIndianCivilCalendarDateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_islamic'                    : RPNOperatorInfo( getIslamicCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_islamic_name'               : RPNOperatorInfo( getIslamicCalendarDateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_iso'                        : RPNOperatorInfo( getISODate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_iso_name'                   : RPNOperatorInfo( getISODateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_julian'                     : RPNOperatorInfo( getJulianCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_julian_day'                 : RPNOperatorInfo( getJulianDay,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_lilian_day'                 : RPNOperatorInfo( getLilianDay,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_mayan'                      : RPNOperatorInfo( getMayanCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_ordinal_date'               : RPNOperatorInfo( getOrdinalDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_persian'                    : RPNOperatorInfo( getPersianCalendarDate,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'to_persian_name'               : RPNOperatorInfo( getPersianCalendarDateName,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'weekday'                       : RPNOperatorInfo( getWeekday,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'year_calendar'                 : RPNOperatorInfo( generateYearCalendar,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    # combinatoric
    'bell_polynomial'               : RPNOperatorInfo( bell,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'binomial'                      : RPNOperatorInfo( binomial,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'compositions'                  : RPNOperatorInfo( getCompositions,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'debruijn'                      : RPNOperatorInfo( createDeBruijnSequence,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'lah'                           : RPNOperatorInfo( lambda n, k: fdiv( fmul( binomial( real( n ), real( k ) ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ),
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'multifactorial'                : RPNOperatorInfo( getNthMultifactorial,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'narayana'                      : RPNOperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ),
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'nth_apery'                     : RPNOperatorInfo( getNthAperyNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_bell'                      : RPNOperatorInfo( bell,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_bernoulli'                 : RPNOperatorInfo( bernoulli,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_catalan'                   : RPNOperatorInfo( lambda n: fdiv( binomial( fmul( 2, real( n ) ), n ), fadd( n, 1 ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_delannoy'                  : RPNOperatorInfo( getNthDelannoyNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_motzkin'                   : RPNOperatorInfo( getNthMotzkinNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_pell'                      : RPNOperatorInfo( getNthPellNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_schroeder'                 : RPNOperatorInfo( getNthSchroederNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_sylvester'                 : RPNOperatorInfo( getNthSylvester,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'partitions'                    : RPNOperatorInfo( lambda n: getPartitionNumber( n ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'permutations'                  : RPNOperatorInfo( getPermutations,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    # complex
    'argument'                      : RPNOperatorInfo( arg,
                                                       1, [ RPNOperatorType.Default ] ),

    'conjugate'                     : RPNOperatorInfo( conj,
                                                       1, [ RPNOperatorType.Default ] ),

    'i'                             : RPNOperatorInfo( lambda n: mpc( real = '0.0', imag = n ),
                                                       1, [ RPNOperatorType.Real ] ),

    'imaginary'                     : RPNOperatorInfo( im,
                                                       1, [ RPNOperatorType.Default ] ),

    'real'                          : RPNOperatorInfo( re,
                                                       1, [ RPNOperatorType.Default ] ),

    # conversion
    'char'                          : RPNOperatorInfo( lambda n: convertToSignedInt( n, 8 ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'dhms'                          : RPNOperatorInfo( convertToDHMS,
                                                       1, [ RPNOperatorType.Measurement ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'dms'                           : RPNOperatorInfo( convertToDMS,
                                                       1, [ RPNOperatorType.Measurement ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'double'                        : RPNOperatorInfo( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( real( n ) ) ) ) ),
                                                       1, [ RPNOperatorType.Real ] ),

    'float'                         : RPNOperatorInfo( lambda n: fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( real( n ) ) ) ) ),
                                                       1, [ RPNOperatorType.Real ] ),

    'from_unix_time'                : RPNOperatorInfo( convertFromUnixTime,
                                                       1, [ RPNOperatorType.Integer ] ),

    'long'                          : RPNOperatorInfo( lambda n: convertToSignedInt( n, 32 ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'longlong'                      : RPNOperatorInfo( lambda n: convertToSignedInt( n, 64 ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'hms'                           : RPNOperatorInfo( convertToHMS,
                                                       1, [ RPNOperatorType.Measurement ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'integer'                       : RPNOperatorInfo( convertToSignedInt,
                                                       1, [ RPNOperatorType.Integer ] ),

    'invert_units'                  : RPNOperatorInfo( invertUnits,
                                                       1, [ RPNOperatorType.Measurement ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'uchar'                         : RPNOperatorInfo( lambda n: fmod( real_int( n ), power( 2, 8 ) ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'uinteger'                      : RPNOperatorInfo( lambda n, k: fmod( real_int( n ), power( 2, real( k ) ) ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'ulong'                         : RPNOperatorInfo( lambda n: fmod( real_int( n ), power( 2, 32 ) ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'ulonglong'                     : RPNOperatorInfo( lambda n: fmod( real_int( n ), power( 2, 64 ) ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'undouble'                      : RPNOperatorInfo( interpretAsDouble,
                                                       1, [ RPNOperatorType.Integer ] ),

    'unfloat'                       : RPNOperatorInfo( interpretAsFloat,
                                                       1, [ RPNOperatorType.Integer ] ),

    'ushort'                        : RPNOperatorInfo( lambda n: fmod( real_int( n ), power( 2, 16 ) ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'short'                         : RPNOperatorInfo( lambda n: convertToSignedInt( n, 16 ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'to_unix_time'                  : RPNOperatorInfo( convertToUnixTime,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'ydhms'                         : RPNOperatorInfo( convertToYDHMS,
                                                       1, [ RPNOperatorType.Measurement ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    # date_time
    'get_year'                      : RPNOperatorInfo( getYear,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'get_month'                     : RPNOperatorInfo( getMonth,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'get_day'                       : RPNOperatorInfo( getDay,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'get_hour'                      : RPNOperatorInfo( getHour,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'get_minute'                    : RPNOperatorInfo( getMinute,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'get_second'                    : RPNOperatorInfo( getSecond,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'iso_day'                       : RPNOperatorInfo( getISODay,
                                                       1, [ RPNOperatorType.DateTime ] ),

    'now'                           : RPNOperatorInfo( RPNDateTime.getNow,
                                                       0, [ ] ),

    'today'                         : RPNOperatorInfo( getToday,
                                                       0, [ ] ),

    'tomorrow'                      : RPNOperatorInfo( getTomorrow,
                                                       0, [ ] ),

    'yesterday'                     : RPNOperatorInfo( getYesterday,
                                                       0, [ ] ),

    # function
    'eval'                          : RPNOperatorInfo( lambda n, func: func.evaluate( n ),
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Function ] ),

    'eval2'                         : RPNOperatorInfo( lambda a, b, func: func.evaluate( a, b ),
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    'eval3'                         : RPNOperatorInfo( lambda a, b, c, func: func.evaluate( a, b, c ),
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Default, RPNOperatorType.Function ] ),

    'limit'                         : RPNOperatorInfo( lambda n, func: limit( lambda x: func.evaluate( x ), n ),
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Function ] ),

    'limitn'                        : RPNOperatorInfo( lambda n, func: limit( lambda x: func.evaluate( x ), n, direction = -1 ),
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Function ] ),

    'negate'                        : RPNOperatorInfo( lambda n: 1 if n == 0 else 0,
                                                       1, [ RPNOperatorType.Boolean ] ),

    'nprod'                         : RPNOperatorInfo( lambda start, end, func: nprod( lambda x: func.evaluate( x ), [ start, end ] ),
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    'nsum'                          : RPNOperatorInfo( lambda start, end, func: nsum( lambda x: func.evaluate( x, func ), [ start, end ] ),
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    'plot'                          : RPNOperatorInfo( plotFunction,
                                                       3, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    'plot2'                         : RPNOperatorInfo( plot2DFunction,
                                                       5, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    'plotc'                         : RPNOperatorInfo( plotComplexFunction,
                                                       5, [ RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Default, RPNOperatorType.Default,
                                                            RPNOperatorType.Function ] ),

    # geography
    'distance'                      : RPNOperatorInfo( getDistance,
                                                       2, [ RPNOperatorType.Location, RPNOperatorType.Location ] ),

    'latlong'                       : RPNOperatorInfo( lambda n, k: RPNLocation( n, k ),
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'location'                      : RPNOperatorInfo( getLocation,
                                                       1, [ RPNOperatorType.String ] ),

    'location_info'                 : RPNOperatorInfo( getLocationInfo,
                                                       1, [ RPNOperatorType.String ] ),

    # geometry
    'antiprism_area'                : RPNOperatorInfo( getAntiprismSurfaceArea,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal ] ),

    'antiprism_volume'              : RPNOperatorInfo( getAntiprismVolume,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal ] ),

    'cone_area'                     : RPNOperatorInfo( getConeSurfaceArea,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'cone_volume'                   : RPNOperatorInfo( getConeVolume,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'dodecahedron_area'             : RPNOperatorInfo( getDodecahedronSurfaceArea,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'dodecahedron_volume'           : RPNOperatorInfo( getDodecahedronVolume,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'icosahedron_area'              : RPNOperatorInfo( getIcosahedronSurfaceArea,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'icosahedron_volume'            : RPNOperatorInfo( getIcosahedronVolume,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'n_sphere_area'                 : RPNOperatorInfo( getNSphereSurfaceArea,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'n_sphere_radius'               : RPNOperatorInfo( getNSphereRadius,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'n_sphere_volume'               : RPNOperatorInfo( getNSphereVolume,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'octahedron_area'               : RPNOperatorInfo( getOctahedronSurfaceArea,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'octahedron_volume'             : RPNOperatorInfo( getOctahedronVolume,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'polygon_area'                  : RPNOperatorInfo( getRegularPolygonArea,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'prism_area'                    : RPNOperatorInfo( getPrismSurfaceArea,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal,
                                                            RPNOperatorType.NonnegativeReal ] ),

    'prism_volume'                  : RPNOperatorInfo( getPrismVolume,
                                                       3, [ RPNOperatorType.PositiveInteger, RPNOperatorType.NonnegativeReal,
                                                            RPNOperatorType.NonnegativeReal ] ),

    'sphere_area'                   : RPNOperatorInfo( lambda n: getNSphereSurfaceArea( n, 3 ),
                                                       1, [ RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'sphere_radius'                 : RPNOperatorInfo( lambda n: getNSphereRadius( n, 3 ),
                                                       1, [ RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'sphere_volume'                 : RPNOperatorInfo( lambda n: getNSphereVolume( n, 3 ),
                                                       1, [ RPNOperatorType.NonnegativeReal ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'tetrahedron_area'              : RPNOperatorInfo( getTetrahedronSurfaceArea,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'tetrahedron_volume'            : RPNOperatorInfo( getTetrahedronVolume,
                                                       1, [ RPNOperatorType.NonnegativeReal ] ),

    'torus_area'                    : RPNOperatorInfo( getTorusSurfaceArea,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'torus_volume'                  : RPNOperatorInfo( getTorusVolume,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'triangle_area'                 : RPNOperatorInfo( getTriangleArea,
                                                       3, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal,
                                                            RPNOperatorType.NonnegativeReal ] ),

    # lexicographic
    'add_digits'                    : RPNOperatorInfo( addDigits,
                                                       2, [ RPNOperatorType.Integer, RPNOperatorType.NonnegativeInteger ] ),

    'build_numbers'                 : RPNOperatorInfo( buildNumbers,
                                                       1, [ RPNOperatorType.String ] ),

    'dup_digits'                    : RPNOperatorInfo( duplicateDigits,
                                                       2, [ RPNOperatorType.Integer, RPNOperatorType.NonnegativeInteger ] ),

    'find_palindrome'               : RPNOperatorInfo( findPalindrome,
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.NonnegativeInteger ] ),

    'get_digits'                    : RPNOperatorInfo( getDigits,
                                                       1, [ RPNOperatorType.Integer ] ),

    'get_left_truncations'          : RPNOperatorInfo( lambda n: RPNGenerator.createGenerator( getLeftTruncations, n ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'get_right_truncations'         : RPNOperatorInfo( lambda n: RPNGenerator.createGenerator( getRightTruncations, n ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'is_automorphic'                : RPNOperatorInfo( lambda n: isMorphic( n, 2 ),
                                                       1, [ RPNOperatorType.Integer ] ),

    'is_kaprekar'                   : RPNOperatorInfo( isKaprekar,
                                                       1, [ RPNOperatorType.Integer ] ),

    'is_morphic'                    : RPNOperatorInfo( isMorphic,
                                                       1, [ RPNOperatorType.Integer, RPNOperatorType.PositiveInteger ] ),

    'is_narcissistic'               : RPNOperatorInfo( isNarcissistic,
                                                       1, [ ] ),

    'is_palindrome'                 : RPNOperatorInfo( isPalindrome,
                                                       1, [ ] ),

    'is_pandigital'                 : RPNOperatorInfo( isPandigital,
                                                       1, [ ] ),

    'is_trimorphic'                 : RPNOperatorInfo( lambda n: isMorphic( n, 3 ),
                                                       1, [ ] ),

    'multiply_digits'               : RPNOperatorInfo( multiplyDigits,
                                                       1, [ ] ),

    'permute_digits'                : RPNOperatorInfo( lambda n: RPNGenerator.createPermutations( getMPFIntegerAsString( n ) ),
                                                       1, [ ] ),

    'reversal_addition'             : RPNOperatorInfo( getNthReversalAddition,
                                                       2, [ ] ),

    'reverse_digits'                : RPNOperatorInfo( reverseDigits,
                                                       1, [ ] ),

    'sum_digits'                    : RPNOperatorInfo( sumDigits,
                                                       1, [ ] ),

    # list
    'exponential_range'             : RPNOperatorInfo( RPNGenerator.createExponential,
                                                       3, [ ] ),

    'geometric_range'               : RPNOperatorInfo( RPNGenerator.createGeometric,
                                                       3, [ ] ),

    'range'                         : RPNOperatorInfo( RPNGenerator.createRange,
                                                       2, [ ] ),

    'range2'                        : RPNOperatorInfo( RPNGenerator.createRange,
                                                       3, [ ] ),

    # logarithms
    'lambertw'                      : RPNOperatorInfo( lambertw,
                                                       1, [ ] ),

    'li'                            : RPNOperatorInfo( li,
                                                       1, [ ] ),

    'ln'                            : RPNOperatorInfo( ln,
                                                       1, [ ] ),

    'log10'                         : RPNOperatorInfo( log10,
                                                       1, [ ] ),

    'log2'                          : RPNOperatorInfo( lambda n: log( n, 2 ),
                                                       1, [ ] ),

    'logxy'                         : RPNOperatorInfo( log,
                                                       2, [ ] ),

    'polylog'                       : RPNOperatorInfo( polylog,
                                                       2, [ ] ),

    # number_theory
    'aliquot'                       : RPNOperatorInfo( lambda n, k: RPNGenerator.createGenerator( getAliquotSequence, [ n, k ] ),
                                                       2, [ ] ),

    'alternating_factorial'         : RPNOperatorInfo( getNthAlternatingFactorial,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'calkin_wilf'                   : RPNOperatorInfo( getNthCalkinWilf,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'carol'                         : RPNOperatorInfo( lambda n: fsub( power( fsub( power( 2, real( n ) ), 1 ), 2 ), 2 ),
                                                       1, [ ] ),

    'count_divisors'                : RPNOperatorInfo( getDivisorCount,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'divisors'                      : RPNOperatorInfo( getDivisors,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'double_factorial'              : RPNOperatorInfo( lambda n: fac2( n ),
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'ecm'                           : RPNOperatorInfo( getECMFactorList,
                                                       1, [ RPNOperatorType.Integer ] ),

    'egypt'                         : RPNOperatorInfo( getGreedyEgyptianFraction,
                                                       2, [ ] ),

    'euler_brick'                   : RPNOperatorInfo( makeEulerBrick,
                                                       3, [ ] ),

    'euler_phi'                     : RPNOperatorInfo( getEulerPhi,
                                                       1, [ ] ),

    'factor'                        : RPNOperatorInfo( getFactorList,
                                                       1, [ RPNOperatorType.Integer ] ),

    'factorial'                     : RPNOperatorInfo( lambda n: fac( n ),
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'fibonacci'                     : RPNOperatorInfo( getNthFibonacci,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'fibonorial'                    : RPNOperatorInfo( getNthFibonorial,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'generate_polydivisibles'       : RPNOperatorInfo( lambda n: RPNGenerator.createGenerator( generatePolydivisibles, n ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'fraction'                      : RPNOperatorInfo( interpretAsFraction,
                                                       2, [ ] ),

    'gamma'                         : RPNOperatorInfo( gamma,
                                                       1, [ ] ),

    'harmonic'                      : RPNOperatorInfo( harmonic,
                                                       1, [ ] ),

    'heptanacci'                    : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 7 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hexanacci'                     : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 6 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hyperfactorial'                : RPNOperatorInfo( hyperfac,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_abundant'                   : RPNOperatorInfo( isAbundant,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_achilles'                   : RPNOperatorInfo( isAchillesNumber,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_deficient'                  : RPNOperatorInfo( isDeficient,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_k_semiprime'                : RPNOperatorInfo( isKSemiPrime,
                                                       2, [ ] ),

    'is_perfect'                    : RPNOperatorInfo( isPerfect,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_polydivisible'              : RPNOperatorInfo( isPolydivisible,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_powerful'                   : RPNOperatorInfo( isPowerful,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_prime'                      : RPNOperatorInfo( lambda n: 1 if isPrime( n ) else 0,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_pronic'                     : RPNOperatorInfo( isPronic,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_rough'                      : RPNOperatorInfo( isRough,
                                                       2, [ ] ),

    'is_semiprime'                  : RPNOperatorInfo( lambda n: isKSemiPrime( n, 2 ),
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_smooth'                     : RPNOperatorInfo( isSmooth,
                                                       2, [ ] ),

    'is_sphenic'                    : RPNOperatorInfo( isSphenic,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_squarefree'                 : RPNOperatorInfo( isSquareFree,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'is_unusual'                    : RPNOperatorInfo( isUnusual,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'jacobsthal'                    : RPNOperatorInfo( getNthJacobsthalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'kynea'                         : RPNOperatorInfo( lambda n: fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ),
                                                       1, [ RPNOperatorType.Real ] ),

    'leonardo'                      : RPNOperatorInfo( lambda n: fsub( fmul( 2, fib( fadd( n, 1 ) ) ), 1 ),
                                                       1, [ RPNOperatorType.Real ] ),

    'leyland'                       : RPNOperatorInfo( lambda n, k: fadd( power( n, k ), power( k, n ) ),
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'log_gamma'                     : RPNOperatorInfo( loggamma,
                                                       1, [ RPNOperatorType.Default ] ),

    'lucas'                         : RPNOperatorInfo( getNthLucasNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'make_cf'                       : RPNOperatorInfo( lambda n, k: RPNContinuedFraction( real( n ), maxterms = real( k ), cutoff = power( 10, -( mp.dps - 2 ) ) ),
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.PositiveInteger ] ),

    'make_pyth_3'                   : RPNOperatorInfo( makePythagoreanTriple,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'make_pyth_4'                   : RPNOperatorInfo( makePythagoreanQuadruple,
                                                       2, [ RPNOperatorType.NonnegativeReal, RPNOperatorType.NonnegativeReal ] ),

    'merten'                        : RPNOperatorInfo( getNthMerten,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'mobius'                        : RPNOperatorInfo( getMobius,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_padovan'                   : RPNOperatorInfo( getNthPadovanNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'n_fibonacci'                   : RPNOperatorInfo( getNthKFibonacciNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'octanacci'                     : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 8 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pascal_triangle'               : RPNOperatorInfo( lambda n: RPNGenerator.createGenerator( getNthPascalLine, n ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pentanacci'                    : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'polygamma'                     : RPNOperatorInfo( psi,
                                                       2, [ ] ),

    'repunit'                       : RPNOperatorInfo( getNthBaseKRepunit,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'riesel'                        : RPNOperatorInfo( lambda n: fsub( fmul( real( n ), power( 2, n ) ), 1 ),
                                                       1, [ RPNOperatorType.Real ] ),

    'sigma'                         : RPNOperatorInfo( getSigma,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'sigma_n'                       : RPNOperatorInfo( getSigmaN,
                                                       2, [ RPNOperatorType.NonnegativeInteger, RPNOperatorType.PositiveInteger ] ),

    'stern'                         : RPNOperatorInfo( getNthStern,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'subfactorial'                  : RPNOperatorInfo( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ),
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'superfactorial'                : RPNOperatorInfo( superfac,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'tetranacci'                    : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 4 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'thabit'                        : RPNOperatorInfo( lambda n: fsub( fmul( 3, power( 2, n ) ), 1 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'tribonacci'                    : RPNOperatorInfo( lambda n: getNthKFibonacciNumber( n, 3 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'unit_roots'                    : RPNOperatorInfo( lambda n: unitroots( real_int( n ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'zeta'                          : RPNOperatorInfo( zeta,
                                                       1, [ RPNOperatorType.Default ] ),

    # physics
    'schwarzchild_radius'           : RPNOperatorInfo( getSchwarzchildRadius,
                                                       1, [ RPNOperatorType.Measurement ] ),

    # polygonal
    'centered_decagonal'            : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 10 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_heptagonal'           : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 7 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_hexagonal'            : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 6 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_nonagonal'            : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 9 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_octagonal'            : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 8 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_pentagonal'           : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_polygonal'            : RPNOperatorInfo( getCenteredPolygonalNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'centered_square'               : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 4 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_triangular'           : RPNOperatorInfo( lambda n: getCenteredPolygonalNumber( n, 3 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal'                     : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 10 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_centered_square'     : RPNOperatorInfo( getNthDecagonalCenteredSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_heptagonal'          : RPNOperatorInfo( getNthDecagonalHeptagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_hexagonal'           : RPNOperatorInfo( getNthDecagonalHexagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_nonagonal'           : RPNOperatorInfo( getNthDecagonalNonagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_octagonal'           : RPNOperatorInfo( getNthDecagonalOctagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_pentagonal'          : RPNOperatorInfo( getNthDecagonalPentagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'decagonal_triangular'          : RPNOperatorInfo( getNthDecagonalTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'generalized_pentagonal'        : RPNOperatorInfo( lambda n: getNthGeneralizedPolygonalNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'heptagonal'                    : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 7 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'heptagonal_hexagonal'          : RPNOperatorInfo( getNthHeptagonalHexagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'heptagonal_pentagonal'         : RPNOperatorInfo( getNthHeptagonalPentagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'heptagonal_square'             : RPNOperatorInfo( getNthHeptagonalSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'heptagonal_triangular'         : RPNOperatorInfo( getNthHeptagonalTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hexagonal'                     : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 6 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hexagonal_pentagonal'          : RPNOperatorInfo( getNthHexagonalPentagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hexagonal_square'              : RPNOperatorInfo( getNthHexagonalSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal'                     : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 9 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_heptagonal'          : RPNOperatorInfo( getNthNonagonalHeptagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_hexagonal'           : RPNOperatorInfo( getNthNonagonalHexagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_octagonal'           : RPNOperatorInfo( getNthNonagonalOctagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_pentagonal'          : RPNOperatorInfo( getNthNonagonalPentagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_square'              : RPNOperatorInfo( getNthNonagonalSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nonagonal_triangular'          : RPNOperatorInfo( getNthNonagonalTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_decagonal'        : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 10 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_heptagonal'       : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 7 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_hexagonal'        : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 6 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_nonagonal'        : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 9 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_octagonal'        : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 8 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_pentagonal'       : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_polygonal'        : RPNOperatorInfo( findCenteredPolygonalNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'nth_centered_square'           : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 4 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_centered_triangular'       : RPNOperatorInfo( lambda n: findCenteredPolygonalNumber( n, 3 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_decagonal'                 : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 10 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_heptagonal'                : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 7 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_hexagonal'                 : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 6 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_nonagonal'                 : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 9 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_octagonal'                 : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 8 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_pentagonal'                : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_polygonal'                 : RPNOperatorInfo( findNthPolygonalNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'nth_square'                    : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 4 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_triangular'                : RPNOperatorInfo( lambda n: findNthPolygonalNumber( n, 3 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal'                     : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 8 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal_heptagonal'          : RPNOperatorInfo( getNthOctagonalHeptagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal_hexagonal'           : RPNOperatorInfo( getNthOctagonalHexagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal_pentagonal'          : RPNOperatorInfo( getNthOctagonalPentagonalNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal_square'              : RPNOperatorInfo( getNthOctagonalSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octagonal_triangular'          : RPNOperatorInfo( getNthOctagonalTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pentagonal'                    : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 5 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pentagonal_square'             : RPNOperatorInfo( getNthPentagonalSquareNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pentagonal_triangular'         : RPNOperatorInfo( getNthPentagonalTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'polygonal'                     : RPNOperatorInfo( getNthPolygonalNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'square_triangular'             : RPNOperatorInfo( getNthSquareTriangularNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'star'                          : RPNOperatorInfo( getNthStarNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'triangular'                    : RPNOperatorInfo( lambda n: getNthPolygonalNumber( n, 3 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    # polyhedral
    'centered_cube'                 : RPNOperatorInfo( getNthCenteredCubeNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_dodecahedral'         : RPNOperatorInfo( getNthCenteredDodecahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_icosahedral'          : RPNOperatorInfo( getNthCenteredIcosahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_octahedral'           : RPNOperatorInfo( getNthCenteredOctahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'centered_tetrahedral'          : RPNOperatorInfo( getNthCenteredTetrahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'dodecahedral'                  : RPNOperatorInfo( lambda n: polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], real( n ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'icosahedral'                   : RPNOperatorInfo( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], real( n ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'octahedral'                    : RPNOperatorInfo( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], real( n ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'pentatope'                     : RPNOperatorInfo( getNthPentatopeNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'polytope'                      : RPNOperatorInfo( getNthPolytopeNumber,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'pyramid'                       : RPNOperatorInfo( lambda n: getNthPolygonalPyramidalNumber( n, 4 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'rhombdodec'                    : RPNOperatorInfo( getNthRhombicDodecahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'stella_octangula'              : RPNOperatorInfo( getNthStellaOctangulaNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'tetrahedral'                   : RPNOperatorInfo( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'truncated_octahedral'          : RPNOperatorInfo( getNthTruncatedOctahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'truncated_tetrahedral'         : RPNOperatorInfo( getNthTruncatedTetrahedralNumber,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    # powers_and_roots
    'agm'                           : RPNOperatorInfo( agm,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ] ),

    'cube'                          : RPNOperatorInfo( lambda n: exponentiate( n, 3 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'cube_root'                     : RPNOperatorInfo( lambda n: getRoot( n, 3 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'exp'                           : RPNOperatorInfo( lambda n: exp( n ),
                                                       1, [ RPNOperatorType.Default ] ),

    'exp10'                         : RPNOperatorInfo( lambda n: power( 10, n ),
                                                       1, [ RPNOperatorType.Default ] ),

    'expphi'                        : RPNOperatorInfo( lambda n: power( phi, n ),
                                                       1, [ RPNOperatorType.Default ] ),

    'hyper4_2'                      : RPNOperatorInfo( tetrateLarge,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Real ] ),

    'power'                         : RPNOperatorInfo( exponentiate,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'powmod'                        : RPNOperatorInfo( getPowMod,
                                                       3, [ ] ),

    'root'                          : RPNOperatorInfo( getRoot,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Real ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'square'                        : RPNOperatorInfo( lambda n: exponentiate( n, 2 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'square_root'                   : RPNOperatorInfo( lambda n: getRoot( n, 2 ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'tetrate'                       : RPNOperatorInfo( tetrate,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.Real ] ),

    # prime_number
    'balanced_prime'                : RPNOperatorInfo( getNthBalancedPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'balanced_prime_'               : RPNOperatorInfo( getNthBalancedPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'cousin_prime'                  : RPNOperatorInfo( getNthCousinPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'cousin_prime_'                 : RPNOperatorInfo( getNthCousinPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'double_balanced'               : RPNOperatorInfo( getNthDoubleBalancedPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'double_balanced_'              : RPNOperatorInfo( getNthDoubleBalancedPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'isolated_prime'                : RPNOperatorInfo( getNthIsolatedPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'next_prime'                    : RPNOperatorInfo( lambda n: findPrime( n )[ 1 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'next_quadruplet_prime'         : RPNOperatorInfo( lambda n: findQuadrupletPrimes( n )[ 1 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'next_quintuplet_prime'         : RPNOperatorInfo( lambda n: findQuintupletPrimes( n )[ 1 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_prime'                     : RPNOperatorInfo( lambda n: findPrime( n )[ 0 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_quadruplet_prime'          : RPNOperatorInfo( lambda n: findQuadrupletPrimes( n )[ 0 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'nth_quintuplet_prime'          : RPNOperatorInfo( lambda n: findQuintupletPrimes( n )[ 0 ],
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'polyprime'                     : RPNOperatorInfo( getNthPolyPrime,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'prime'                         : RPNOperatorInfo( getNthPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'primes'                        : RPNOperatorInfo( getPrimes,
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'prime_pi'                      : RPNOperatorInfo( getPrimePi,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'primorial'                     : RPNOperatorInfo( getNthPrimorial,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'quadruplet_prime'              : RPNOperatorInfo( getNthQuadrupletPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'quadruplet_prime_'             : RPNOperatorInfo( getNthQuadrupletPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'quintuplet_prime'              : RPNOperatorInfo( getNthQuintupletPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'quintuplet_prime_'             : RPNOperatorInfo( getNthQuintupletPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'safe_prime'                    : RPNOperatorInfo( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sextuplet_prime'               : RPNOperatorInfo( getNthSextupletPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sextuplet_prime_'              : RPNOperatorInfo( getNthSextupletPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_prime'                    : RPNOperatorInfo( getNthSexyPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_prime_'                   : RPNOperatorInfo( getNthSexyPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_quadruplet'               : RPNOperatorInfo( getNthSexyQuadruplet,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_quadruplet_'              : RPNOperatorInfo( getNthSexyQuadrupletList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_triplet'                  : RPNOperatorInfo( getNthSexyTriplet,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sexy_triplet_'                 : RPNOperatorInfo( getNthSexyTripletList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'sophie_prime'                  : RPNOperatorInfo( getNthSophiePrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'superprime'                    : RPNOperatorInfo( getNthSuperPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'triplet_prime'                 : RPNOperatorInfo( getNthTripletPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'triplet_prime_'                : RPNOperatorInfo( getNthTripletPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'triple_balanced'               : RPNOperatorInfo( getNthTripleBalancedPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'triple_balanced_'              : RPNOperatorInfo( getNthTripleBalancedPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'twin_prime'                    : RPNOperatorInfo( getNthTwinPrime,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'twin_prime_'                   : RPNOperatorInfo( getNthTwinPrimeList,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    # settings
    'accuracy'                      : RPNOperatorInfo( lambda n: setAccuracy( fadd( n, 2 ) ),
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'comma'                         : RPNOperatorInfo( setComma,
                                                       1, [ RPNOperatorType.Boolean ] ),

    'comma_mode'                    : RPNOperatorInfo( setCommaMode,
                                                       0, [ ] ),

    'decimal_grouping'              : RPNOperatorInfo( setDecimalGrouping,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'hex_mode'                      : RPNOperatorInfo( setHexMode,
                                                       0, [ ] ),

    'identify'                      : RPNOperatorInfo( setIdentify,
                                                       1, [ RPNOperatorType.Boolean ] ),

    'identify_mode'                 : RPNOperatorInfo( setIdentifyMode,
                                                       0, [ ] ),

    'input_radix'                   : RPNOperatorInfo( setInputRadix,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'integer_grouping'              : RPNOperatorInfo( setIntegerGrouping,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'leading_zero'                  : RPNOperatorInfo( setLeadingZero,
                                                       1, [ RPNOperatorType.Boolean ] ),

    'leading_zero_mode'             : RPNOperatorInfo( setLeadingZeroMode,
                                                       0, [ ] ),

    'octal_mode'                    : RPNOperatorInfo( setOctalMode,
                                                       0, [ ] ),

    'output_radix'                  : RPNOperatorInfo( setOutputRadix,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'precision'                     : RPNOperatorInfo( setPrecision,
                                                       1, [ RPNOperatorType.NonnegativeInteger ] ),

    'random'                        : RPNOperatorInfo( rand,
                                                       0, [ ] ),

    'random_'                       : RPNOperatorInfo( lambda n: RPNGenerator.createGenerator( getMultipleRandoms, n ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'random_integer'                : RPNOperatorInfo( randrange,
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'random_integer_'               : RPNOperatorInfo( lambda n, k: RPNGenerator.createGenerator( getRandomIntegers, [ n, k ] ),
                                                       2, [ RPNOperatorType.PositiveInteger, RPNOperatorType.PositiveInteger ] ),

    'timer'                         : RPNOperatorInfo( setTimer,
                                                       1, [ RPNOperatorType.Boolean ] ),

    'timer_mode'                    : RPNOperatorInfo( setTimerMode,
                                                       0, [ ] ),

    # special
    'constant'                      : RPNOperatorInfo( createConstant,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.String ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'estimate'                      : RPNOperatorInfo( estimate,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'help'                          : RPNOperatorInfo( printHelpMessage,
                                                       0, [ ] ),

    'name'                          : RPNOperatorInfo( getNumberName,
                                                       1, [ RPNOperatorType.Integer ] ),

    'oeis'                          : RPNOperatorInfo( lambda n: downloadOEISSequence( real_int( n ) ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'oeis_comment'                  : RPNOperatorInfo( lambda n: downloadOEISText( real_int( n ), 'C', True ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'oeis_ex'                       : RPNOperatorInfo( lambda n: downloadOEISText( real_int( n ), 'E', True ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'oeis_name'                     : RPNOperatorInfo( lambda n: downloadOEISText( real_int( n ), 'N', True ),
                                                       1, [ RPNOperatorType.PositiveInteger ] ),

    'ordinal_name'                  : RPNOperatorInfo( getOrdinalName,
                                                       1, [ RPNOperatorType.Integer ] ),

    'result'                        : RPNOperatorInfo( loadResult,
                                                       0, [ ] ),

    'permute_dice'                  : RPNOperatorInfo( permuteDice,
                                                       1, [ RPNOperatorType.String ] ),

    'roll_dice'                     : RPNOperatorInfo( rollDice,
                                                       1, [ RPNOperatorType.String ] ),

    'roll_dice_'                    : RPNOperatorInfo( rollMultipleDice,
                                                       2, [ RPNOperatorType.String, RPNOperatorType.PositiveInteger ] ),

    'set'                           : RPNOperatorInfo( setVariable,
                                                       2, [ RPNOperatorType.Default, RPNOperatorType.String ] ),

    'topic'                         : RPNOperatorInfo( printHelpTopic,
                                                       1, [ RPNOperatorType.String ] ),

    'value'                         : RPNOperatorInfo( getValue,
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    # trigonometry
    'acos'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, acos ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'acosh'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, acosh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'acot'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, acot ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'acoth'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, acoth ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'acsc'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, acsc ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'acsch'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, acsch ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'asec'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, asec ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'asech'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, asech ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'asin'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, asin ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'asinh'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, asinh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'atan'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, atan ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'atanh'                         : RPNOperatorInfo( lambda n: performTrigOperation( n, atanh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'cos'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, cos ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'cosh'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, cosh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'cot'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, cot ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'coth'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, coth ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'csc'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, csc ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'csch'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, csch ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'hypotenuse'                    : RPNOperatorInfo( hypot,
                                                       2, [ RPNOperatorType.Real, RPNOperatorType.Real ] ),

    'sec'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, sec ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'sech'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, sech ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'sin'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, sin ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'sinh'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, sinh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'tan'                           : RPNOperatorInfo( lambda n: performTrigOperation( n, tan ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    'tanh'                          : RPNOperatorInfo( lambda n: performTrigOperation( n, tanh ),
                                                       1, [ RPNOperatorType.Default ],
                                                       RPNOperatorInfo.measurementsAllowed ),

    # internal
    '_dump_aliases'                 : RPNOperatorInfo( dumpAliases,
                                                       0, [ ] ),

    '_dump_operators'               : RPNOperatorInfo( dumpOperators,
                                                       0, [ ] ),

    '_stats'                        : RPNOperatorInfo( dumpStats,
                                                       0, [ ] ),

    #   'antitet'                       : RPNOperatorInfo( findTetrahedralNumber, 0 ),
    #   'bernfrac'                      : RPNOperatorInfo( bernfrac, 1 ),
}

