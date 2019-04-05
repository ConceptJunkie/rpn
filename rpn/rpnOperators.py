#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import configparser
import difflib
import inspect
import itertools
import struct

from enum import Enum
from mpmath import apery, bell, bernoulli, catalan, cplot, euler, fadd, glaisher, \
                   khinchin, lambertw, limit, mertens, nint, nprod, nsum, phi, \
                   pi, plot, splot

from random import randrange

from rpn.rpnAliases import dumpAliases
from rpn.rpnOperator import callers, RPNArgumentType, RPNOperator

from rpn.rpnAstronomy import *
from rpn.rpnCalendar import *
from rpn.rpnChemistry import *
from rpn.rpnCombinatorics import *
from rpn.rpnComputer import *
from rpn.rpnConstantUtils import *
from rpn.rpnDateTime import *
from rpn.rpnDice import *
from rpn.rpnFactor import *
from rpn.rpnGeometry import *
from rpn.rpnInput import *
from rpn.rpnLexicographic import *
from rpn.rpnList import *
from rpn.rpnLocation import *
from rpn.rpnMath import *
from rpn.rpnMeasurement import *
from rpn.rpnModifiers import *
from rpn.rpnName import *
from rpn.rpnNumberTheory import *
from rpn.rpnPersistence import *
from rpn.rpnPhysics import *
from rpn.rpnPolynomials import *
from rpn.rpnPolytope import *
from rpn.rpnPrimeUtils import *
from rpn.rpnSettings import *
from rpn.rpnSpecial import *
from rpn.rpnUtils import *

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //  Constants are always operators that take no arguments.
# //
# //  Please note that the last two RPNOperator arguments must go on a new line
# //  because the 'lambda' functionality parses the lambdas in RPNOperator objects
# //  to build Python code out of them.
# //
# //******************************************************************************

constants = {
    # mathematical constants
    # we use mpf( ) so the type returned is mpf rather than the mpmath constant type
    'apery_constant'                : RPNOperator( lambda: mpf( apery ),
                                                   0, [ ] ),
    'catalan_constant'              : RPNOperator( lambda: mpf( catalan ),
                                                   0, [ ] ),
    'champernowne_constant'         : RPNOperator( getChampernowneConstant,
                                                   0, [ ] ),
    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant,
                                                   0, [ ] ),
    'e'                             : RPNOperator( lambda: mpf( e ),
                                                   0, [ ] ),
    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ),
                                                   0, [ ] ),
    'euler_mascheroni_constant'     : RPNOperator( lambda: mpf( euler ),
                                                   0, [ ] ),
    'glaisher_constant'             : RPNOperator( lambda: mpf( glaisher ),
                                                   0, [ ] ),
    'infinity'                      : RPNOperator( lambda: inf,
                                                   0, [ ] ),
    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ),
                                                   0, [ ] ),
    'khinchin_constant'             : RPNOperator( lambda: mpf( khinchin ),
                                                   0, [ ] ),
    'merten_constant'               : RPNOperator( lambda: mpf( mertens ),
                                                   0, [ ] ),
    'mills_constant'                : RPNOperator( getMillsConstant,
                                                   0, [ ] ),
    'negative_infinity'             : RPNOperator( lambda: -inf,
                                                   0, [ ] ),
    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ),
                                                   0, [ ] ),
    'phi'                           : RPNOperator( lambda: mpf( phi ),
                                                   0, [ ] ),
    'pi'                            : RPNOperator( lambda: mpf( pi ),
                                                   0, [ ] ),
    'plastic_constant'              : RPNOperator( getPlasticConstant,
                                                   0, [ ] ),
    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ),
                                                   0, [ ] ),
    'robbins_constant'              : RPNOperator( getRobbinsConstant,
                                                   0, [ ] ),
    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ),
                                                   0, [ ] ),
    'thue_morse_constant'           : RPNOperator( getThueMorseConstant,
                                                   0, [ ] ),

    # physical constants
    'faraday_constant'              : RPNOperator( getFaradayConstant,
                                                   0, [ ] ),
    'fine_structure_constant'       : RPNOperator( getFineStructureConstant,
                                                   0, [ ] ),
    'radiation_constant'            : RPNOperator( getRadiationConstant,
                                                   0, [ ] ),
    'stefan_boltzmann_constant'     : RPNOperator( getStefanBoltzmannConstant,
                                                   0, [ ] ),
    'vacuum_impedance'              : RPNOperator( getVacuumImpedance,
                                                   0, [ ] ),

    # Planck constants
    'planck_length'                 : RPNOperator( getPlanckLength,
                                                   0, [ ] ),
    'planck_mass'                   : RPNOperator( getPlanckMass,
                                                   0, [ ] ),
    'planck_time'                   : RPNOperator( getPlanckTime,
                                                   0, [ ] ),
    'planck_charge'                 : RPNOperator( getPlanckCharge,
                                                   0, [ ] ),
    'planck_temperature'            : RPNOperator( getPlanckTemperature,
                                                   0, [ ] ),

    'planck_acceleration'           : RPNOperator( getPlanckAcceleration,
                                                   0, [ ] ),
    'planck_angular_frequency'      : RPNOperator( getPlanckAngularFrequency,
                                                   0, [ ] ),
    'planck_area'                   : RPNOperator( getPlanckArea,
                                                   0, [ ] ),
    'planck_current'                : RPNOperator( getPlanckCurrent,
                                                   0, [ ] ),
    'planck_density'                : RPNOperator( getPlanckDensity,
                                                   0, [ ] ),
    'planck_energy'                 : RPNOperator( getPlanckEnergy,
                                                   0, [ ] ),
    'planck_electrical_inductance'  : RPNOperator( getPlanckElectricalInductance,
                                                   0, [ ] ),
    'planck_energy_density'         : RPNOperator( getPlanckEnergyDensity,
                                                   0, [ ] ),
    'planck_force'                  : RPNOperator( getPlanckForce,
                                                   0, [ ] ),
    'planck_impedance'              : RPNOperator( getPlanckImpedance,
                                                   0, [ ] ),
    'planck_intensity'              : RPNOperator( getPlanckIntensity,
                                                   0, [ ] ),
    'planck_magnetic_inductance'    : RPNOperator( getPlanckMagneticInductance,
                                                   0, [ ] ),
    'planck_momentum'               : RPNOperator( getPlanckMomentum,
                                                   0, [ ] ),
    'planck_power'                  : RPNOperator( getPlanckPower,
                                                   0, [ ] ),
    'planck_pressure'               : RPNOperator( getPlanckPressure,
                                                   0, [ ] ),
    'planck_viscosity'              : RPNOperator( getPlanckViscosity,
                                                   0, [ ] ),
    'planck_voltage'                : RPNOperator( getPlanckVoltage,
                                                   0, [ ] ),
    'planck_volumetric_flow_rate'   : RPNOperator( getPlanckVolumetricFlowRate,
                                                   0, [ ] ),
    'planck_volume'                 : RPNOperator( getPlanckVolume,
                                                   0, [ ] ),
}


# //******************************************************************************
# //
# //  class RPNFunction
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  RPNFunction object.  However, it can't know how many of them it
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

class RPNFunction( object ):
    '''This class represents a user-defined function in rpn.'''
    def __init__( self, valueList = None, startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        elif valueList:
            self.valueList.append( valueList )
        else:
            self.valueList = None

        self.startingIndex = startingIndex
        self.code = ''
        self.code_locals = { }
        self.compiled = None
        self.function = None
        self.argCount = 0

    def add( self, arg ):
        self.valueList.append( arg )

    def evaluate( self, x = 0, y = 0, z = 0 ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        if self.argCount == 0:
            return self.function( )
        elif self.argCount == 1:
            return self.function( x )
        elif self.argCount == 2:
            return self.function( x, y )
        elif self.argCount == 3:
            return self.function( x, y, z )

    def setCode( self, code ):
        if code.find( 'rpnInternalFunction( ):' ) != -1:
            self.argCount = 0
        elif code.find( 'rpnInternalFunction( x ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( z ):' ) != -1:
            self.argCount = 1
        elif code.find( 'rpnInternalFunction( x, y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( x, z ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y, z ):' ) != -1:
            self.argCount = 2
        else:
            self.argCount = 3

        self.code = code
        self.compile( )

    def getCode( self ):
        if not self.code:
            self.buildCode( )
            self.compile( )

        return self.code

    def getFunction( self ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        return self.function

    def buildCode( self ):
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

        emptyFunction = True

        args = [ ]
        listArgs = [ ]
        listDepth = 0

        debugPrint( 'terms', valueList )

        while valueList:
            term = valueList.pop( 0 )
            debugPrint( 'term:', term, 'args:', args )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            if term in ( 'x', 'y', 'z' ) and not valueList:
                self.code += term
                emptyFunction = False
            elif term in constants:
                function = constants[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( constants[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) - 1 ] + ' )'

                function += '( )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term == '[':
                listArgs.append( [ ] )
                listDepth += 1
            elif term == ']':
                arg = '[ '

                for listArg in listArgs[ listDepth - 1 ]:
                    if arg != '[ ':
                        arg += ', '

                    arg += listArg

                arg += ' ]'

                args.append( arg )

                del listArgs[ listDepth - 1 ]

                listDepth -= 1
            #elif term in specialFormatOperators:
            elif term in operators:
                function = operators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( operators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = operators[ term ].argCount

                if listDepth > 0:
                    if len( listArgs[ listDepth - 1 ] ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for i in range( 0, operands ):
                        argList.insert( 0, listArgs[ listDepth - 1 ].pop( ) )
                else:
                    if len( args ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for i in range( 0, operands ):
                        argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term in listOperators:
                function = listOperators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( listOperators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) : function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = listOperators[ term ].argCount

                if len( args ) < operands:
                    raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term[ 0 ] == '@' and term[ 1 : ] in g.userFunctions:
                function2 = g.userFunctions[ term[ 1 : ] ].getCode( )
                debugPrint( 'function:', function2 )

                function2 = function2.replace( 'def rpnInternalFunction(', '( lambda' )
                function2 = function2.replace( ' ): return', ':' )

                function2 += ' )( '

                first = True

                argList = [ ]

                operands = g.userFunctions[ term[ 1 : ] ].argCount

                if len( args ) < operands:
                    raise ValueError( '{0} expects {1} operands'.format( term, operands ) )

                for i in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function2 += ', '

                    function2 += arg

                function2 += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function2 )
                else:
                    args.append( function2 )

                if not valueList:
                    self.code += function2
                    emptyFunction = False
            elif term[ 0 ] == '$' and term[ 1 : ] in g.userVariables:
                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( g.userVariables[ term[ 1 : ] ] )
                else:
                    args.append( g.userVariables[ term[ 1 : ] ] )
            else:
                if term not in ( 'x', 'y', 'z' ):
                    term = str( parseInputValue( term, g.inputRadix ) )

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( term )
                else:
                    args.append( term )

        if emptyFunction:
            self.code += args[ 0 ]

        debugPrint( 'args:', args )
        debugPrint( 'valueList:', self.valueList[ self.startingIndex : ] )
        debugPrint( 'code:', self.code )

    def compile( self ):
        if not self.code:
            self.buildCode( )

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
    valueList.append( RPNFunction( valueList, len( valueList ) ) )


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
# //  loadUserFunctionsFile
# //
# //******************************************************************************

def loadUserFunctionsFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserFunctionsFileName( ) )

    try:
        items = config.items( 'User Functions' )
    except:
        return

    for tuple in items:
        func = RPNFunction( )
        func.setCode( tuple[ 1 ] )
        g.userFunctions[ tuple[ 0 ] ] = func


# //******************************************************************************
# //
# //  saveUserFunctionsFile
# //
# //******************************************************************************

def saveUserFunctionsFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Functions' ] = { }

    for key in g.userFunctions.keys( ):
        config[ 'User Functions' ][ key ] = g.userFunctions[ key ].getCode( )

    import os.path

    if os.path.isfile( getUserFunctionsFileName( ) ):
        from shutil import copyfile
        copyfile( getUserFunctionsFileName( ), getUserFunctionsFileName( ) + '.backup' )

    with open( getUserFunctionsFileName( ), 'w' ) as userFunctionsFile:
        config.write( userFunctionsFile )


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
# //  evaluateRecurrence
# //
# //******************************************************************************

def evaluateRecurrence( start, count, func ):
    arg = start
    result = [ start ]

    for i in arange( count ):
        arg = func.evaluate( arg )
        result.append( arg )

    return result


# //******************************************************************************
# //
# //  repeatGenerator
# //
# //******************************************************************************

def repeatGenerator( n, func ):
    for i in arange( 0, n ):
        yield func.evaluate( )


# //******************************************************************************
# //
# //  repeatGenerator
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def repeat( n, func ):
    return RPNGenerator( repeatGenerator( n, func ) )


# //******************************************************************************
# //
# //  filterList
# //
# //******************************************************************************

def filterList( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )
        else:
            raise ValueError( '\'filter\' expects a function argument' )

    for i in n:
        value = k.evaluate( i )

        if ( value != 0 ) != invert:
            yield i


# //******************************************************************************
# //
# //  filterListByIndex
# //
# //******************************************************************************

def filterListByIndex( n, k, invert = False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter_by_index\' expects a function argument' )
        else:
            raise ValueError( '\'filter_by_index\' expects a function argument' )

    for index, item in enumerate( n ):
        value = k.evaluate( index )

        if ( value != 0 ) != invert:
            yield item


# //******************************************************************************
# //
# //  forEach
# //
# //******************************************************************************

def forEach( list, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each\' expects a function argument' )

    for i in list:
        yield func.evaluate( *i )


# //******************************************************************************
# //
# //  forEachList
# //
# //******************************************************************************

def forEachList( list, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each_list\' expects a function argument' )

    for i in list:
        yield func.evaluate( i )


# //******************************************************************************
# //
# //  breakOnCondition
# //
# //******************************************************************************

def breakOnCondition( n, k ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        raise ValueError( '\'break_on\' expects a function argument' )

    for i in n:
        value = k.evaluate( i )

        if value:
            return i


# //******************************************************************************
# //
# //  createRange
# //
# //  Used by 'lambda'.
# //
# //******************************************************************************

def createRange( start, end ):
    return arange( start, fadd( end, 1 ) )


# //******************************************************************************
# //
# //  createSizedRange
# //
# //  Used by 'lambda'.
# //
# //******************************************************************************

def createSizedRange( start, interval, size ):
    return arange( start, fadd( start, fmul( interval, size ) ), interval )


# //******************************************************************************
# //
# //  preprocessTerms
# //
# //  *** Not used yet! ***
# //
# //******************************************************************************

def preprocessTerms( terms ):
    '''
    Given the initial list of arguments form the user, there are several
    things we want to do to the list before handing it off to the actual
    operator evaluator.  This logic used to be part of the evaluator, but
    that made the code a lot more complicated.  Hopefully, this will make
    the code simpler and easier to read.

    If this function returns an empty list, then rpn should abort.  This
    function should print out any error messages.
    '''
    result = [ ]

    # do some basic validation of the arguments we were given...
    if not validateArguments( terms ):
        return result

    print( 'operators', operators )

    for term in terms:
        # translate the aliases into their real names
        if term in g.operatorAliases:
            result.append( g.operatorAliases[ term ] )
        # operators and unit operator names can be stuck right back in the list
        elif term in g.unitOperatorNames or term in g.constantOperatorNames:
            result.append( term )
        # translate compound units in the equivalent operators
        elif ( '*' in term or '^' in term or '/' in term ) and \
            any( c in term for c in string.ascii_letters ):
            result.append( RPNUnits.parseUnitExpression( term ) )
        else:
            result.append( term )

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

    if isinstance( args, RPNGenerator ):
        currentValueList.append( func( args ) )
    else:
        raise ValueError( 'then you shouldn\'t call handleOneArgGeneratorOperator, should you?' )


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

        if argTypes[ 0 ] == RPNArgumentType.Generator:
            handleOneArgGeneratorOperator( operatorInfo.function, args, currentValueList )
        else:
            handleOneArgListOperator( operatorInfo.function, args, currentValueList )
    else:
        argList = [ ]

        for i in range( 0, argsNeeded ):
            argList.insert( 0, currentValueList.pop( ) )

        if argTypes[ 0 ] == RPNArgumentType.Generator:
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
    #TODO:  Use g.operatorNames, etc.
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        # print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )
        print( '   ' + i )

    print( )
    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )
    print( 'constant operators:' )

    constantNames = [ key for key in g.constantOperators ]
    constantNames.extend( [ key for key in constants ] )

    for i in sorted( constantNames ):
        print( '   ' + i )

    print( )
    print( 'modifer operators:' )

    for i in sorted( [ key for key in modifiers ] ):
        print( '   ' + i )

    print( )
    print( 'internal operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i )

    print( )

    return len( operators ) + len( listOperators ) + len( modifiers ) + len( constantNames )


# //******************************************************************************
# //
# //  dumpConstants
# //
# //******************************************************************************

def dumpConstants( ):
    if not g.constantOperators:
        loadUnitData( )
        loadConstants( )

    for i in sorted( [ key for key in g.constantOperators ] ):
        print( i, g.constantOperators[ i ].value )

    print( )

    return len( g.constantOperators )


# //******************************************************************************
# //
# //  dumpUnits
# //
# //******************************************************************************

def dumpUnits( ):
    if not g.unitOperators:
        loadUnitData( )
        loadConstants( )

    for i in sorted( [ key for key in g.unitOperators ] ):
        print( i )

    print( )

    return len( g.unitOperators )


# //******************************************************************************
# //
# //  dumpUnitConversions
# //
# //******************************************************************************

def dumpUnitConversions( ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    for i in sorted( [ key for key in g.unitConversionMatrix ] ):
        print( i, g.unitConversionMatrix[ i ] )

    print( )

    return len( g.unitConversionMatrix )


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

    if g.primeDataAvailable:
        printStats( 'small_primes', 'small primes' )
        printStats( 'large_primes', 'large primes' )
        printStats( 'huge_primes', 'huge primes' )
        printStats( 'isolated_primes', 'isolated primes' )
        printStats( 'twin_primes', 'twin primes' )
        printStats( 'balanced_primes', 'balanced primes' )
        printStats( 'double_balanced_primes', 'double balanced primes' )
        printStats( 'triple_balanced_primes', 'triple balanced primes' )
        printStats( 'sophie_primes', 'Sophie Germain primes' )
        printStats( 'cousin_primes', 'cousin primes' )
        printStats( 'sexy_primes', 'sexy primes' )
        printStats( 'triplet_primes', 'triplet primes' )
        printStats( 'sexy_triplets', 'sexy triplet primes' )
        printStats( 'quad_primes', 'quadruplet primes' )
        printStats( 'sexy_quadruplets', 'sexy quadruplet primes' )
        printStats( 'quint_primes', 'quintuplet primes' )
        printStats( 'sext_primes', 'sextuplet primes' )

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
    listDepth = 0

    try:
        # handle a modifier operator
        if not isList and not isGenerator and term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )
        elif not isList and term in g.unitOperatorNames or term in g.constantOperatorNames or \
             ( '*' in term or '^' in term or '/' in term ) and \
             any( c in term for c in string.ascii_letters ):

            multipliable = True

            if term in g.unitOperatorNames:
                isConstant = False
            elif term in g.constantOperatorNames:
                isConstant = True
                multipliable = g.constantOperators[ term ].multipliable
            else:
                isConstant = False
                term = RPNUnits.parseUnitString( term )

            if multipliable:
                # look for unit without a value (in which case we give it a value of 1)
                if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], RPNMeasurement ) or \
                    isinstance( currentValueList[ -1 ], RPNDateTime ) or ( isinstance( currentValueList[ -1 ], list ) and
                                                                           isinstance( currentValueList[ -1 ][ 0 ], RPNMeasurement ) ):
                        currentValueList.append( applyNumberValueToUnit( 1, term, isConstant ) )
                # if the unit comes after a generator, convert it to a list and apply the unit to each
                elif isinstance( currentValueList[ -1 ], RPNGenerator ):
                    newArg = [ ]

                    for value in list( currentValueList.pop( ) ):
                        newArg.append( applyNumberValueToUnit( value, term, isConstant ) )

                    currentValueList.append( newArg )
                # if the unit comes after a list, then apply it to every item in the list
                elif isinstance( currentValueList[ -1 ], list ):
                    argList = currentValueList.pop( )

                    newArg = [ ]

                    for listItem in argList:
                        newArg.append( applyNumberValueToUnit( listItem, term, isConstant ) )

                    currentValueList.append( newArg )
                # and if it's a plain old number, then apply it to the unit
                elif isinstance( currentValueList[ -1 ], ( mpf, int ) ):
                    currentValueList.append( applyNumberValueToUnit( currentValueList.pop( ), term, isConstant ) )
                else:
                    print( type( currentValueList[ -1 ] ) )
                    raise ValueError( 'unsupported type for a unit operator' )
            else:
                # only constant operators can be non-multipliable
                constantInfo = g.constantOperators[ term ]

                if constantInfo.unit == '':
                    currentValueList.append( mpmathify( constantInfo.value ) )
                else:
                    currentValueList.append( RPNMeasurement( constantInfo.value, constantInfo.unit ) )
        elif term in constants:
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

                    if not operators[ term ].evaluate( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not operators[ term ].evaluate( term, index, currentValueList ):
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
            # handle a plain old value (i.e., a number or list, not an operator)... or
            # a reference to a user-defined function
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
                    g.keywords.extend( g.constantOperatorNames )
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

            # handle a user-defined function
            if isinstance( currentValueList[ -1 ], RPNFunction ):
                if currentValueList[ -1 ].argCount == 0:
                    if not operators[ 'eval0' ].evaluate( 'eval0', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 1:
                    if not operators[ 'eval' ].evaluate( 'eval', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 2:
                    if not operators[ 'eval2' ].evaluate( 'eval2', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 3:
                    if not operators[ 'eval3' ].evaluate( 'eval3', index, currentValueList ):
                        return False

                return True

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
    printHelp( '', True )
    return 0


# //******************************************************************************
# //
# //  printHelpTopic
# //
# //******************************************************************************

def printHelpTopic( n ):
    from rpnOutput import printHelp

    if isinstance( n, str ):
        printHelp( n, True )
    elif isinstance( n, RPNMeasurement ):
        units = n.getUnits( )
        # help for units isn't implemented yet, but now it will work
        printHelp( list( units.keys( ) )[ 0 ], True )
    else:
        print( 'The \'topic\' operator requires a string argument.' )

    return 0


# //******************************************************************************
# //
# //  getUserVariable
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getUserVariable( key ):
    if key in g.userVariables:
        return g.userVariables[ key ]
    else:
        return ""


# //******************************************************************************
# //
# //  setUserVariable
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def setUserVariable( key, value ):
    g.userVariables[ key ] = value
    g.userVariablesAreDirty = True

    return value


# //******************************************************************************
# //
# //  getUserConfiguration
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getUserConfiguration( key ):
    if key in g.userConfiguration:
        return g.userConfiguration[ key ]
    else:
        return ""


# //******************************************************************************
# //
# //  setUserConfiguration
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def setUserConfiguration( key, value ):
    g.userConfiguration[ key ] = value
    g.userConfigurationIsDirty = True

    return value


# //******************************************************************************
# //
# //  deleteUserConfiguration
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def deleteUserConfiguration( key ):
    if key not in g.userConfiguration:
        raise ValueError( 'key \'' + key + '\' not found' )

    del g.userConfiguration[ key ]
    g.userConfigurationIsDirty = True

    return key


# //******************************************************************************
# //
# //  dumpUserConfiguration
# //
# //******************************************************************************

def dumpUserConfiguration( ):
    for i in g.userConfiguration:
        print( i + ':', '"' + g.userConfiguration[ i ] + '"' );

    print( )

    return len( g.userConfiguration )


# //******************************************************************************
# //
# //  createUserFunction
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def createUserFunction( key, func ):
    g.userFunctions[ key ] = func
    g.userFunctionsAreDirty = True

    return key


@oneArgFunctionEvaluator( )
def evaluateFunction0( func ):
    return func.evaluate( )

@twoArgFunctionEvaluator( )
def evaluateFunction( n, func ):
    return func.evaluate( n )

def evaluateFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )

@listAndOneArgFunctionEvaluator( )
def evaluateListFunction( n, func ):
    return func.evaluate( n )

def evaluateListFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateListFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )

@listAndOneArgFunctionEvaluator( )
def filterListOfLists( n, func ):
    return func.evaluate( n )

@twoArgFunctionEvaluator( )
def evaluateLimit( n, func ):
    return limit( lambda x: func.evaluate( x ), n )

@twoArgFunctionEvaluator( )
def evaluateReverseLimit( n, func ):
    return limit( lambda x: func.evaluate( x ), n, direction = -1 )

def evaluateProduct( start, end, func ):
    return nprod( lambda x: func.evaluate( x ), [ start, end ] )

def evaluateSum( start, end, func ):
    return nsum( lambda x: func.evaluate( x, func ), [ start, end ] )

def createExponentialRange( a, b, c ):
    return RPNGenerator.createExponential( a, b, c )

def createGeometricRange( a, b, c ):
    return RPNGenerator.createGeometric( a, b, c )

@twoArgFunctionEvaluator( )
def createRange( start, end ):
    return RPNGenerator.createRange( start, end )

def createIntervalRangeOperator( a, b, c ):
    return RPNGenerator.createRange( a, b, c )

def createSizedRangeOperator( a, b, c ):
    return RPNGenerator.createSizedRange( a, b, c )


# //******************************************************************************
# //
# //  specialFormatOperators
# //
# //******************************************************************************

specialFormatOperators = {
    'and'       : '( {0} and {1} )',
    'nand'      : '( not ( {0} and {1} ) )',
    'or'        : '( {0} or {1} )',
    'nor'       : '( not ( {0} or {1} ) )',
}


# //******************************************************************************
# //
# //  functionOperators
# //
# //  This is a list of operators that terminate the function creation state.
# //
# //******************************************************************************

functionOperators = [
    'break_on',
    'eval0',
    'eval',
    'eval2',
    'eval3',
    'eval_list',
    'eval_list2',
    'eval_list3',
    'filter',
    'filter_by_index',
    'for_each',
    'for_each_list',
    'function',
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plotc',
    'recurrence',
    'repeat',
    'unfilter',
    'unfilter_by_index',
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
    'duplicate_term'        : RPNOperator( duplicateTerm, 1 ),

    'duplicate_operator'    : RPNOperator( duplicateOperation, 1 ),

    'previous'              : RPNOperator( getPrevious, 0 ),

    'unlist'                : RPNOperator( unlist, 0 ),

    'lambda'                : RPNOperator( createFunction, 0 ),

    'x'                     : RPNOperator( addX, 0 ),

    'y'                     : RPNOperator( addY, 0 ),

    'z'                     : RPNOperator( addZ, 0 ),

    '['                     : RPNOperator( incrementNestedListLevel, 0 ),

    ']'                     : RPNOperator( decrementNestedListLevel, 0 ),

    '('                     : RPNOperator( startOperatorList, 0 ),

    ')'                     : RPNOperator( endOperatorList, 0 ),
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
    'add_polynomials'       : RPNOperator( addPolynomials,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'discriminant'          : RPNOperator( getPolynomialDiscriminant,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'eval_polynomial'       : RPNOperator( evaluatePolynomial,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'multiply_polynomials'  : RPNOperator( multiplyPolynomials,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'polynomial_power'      : RPNOperator( exponentiatePolynomial,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'polynomial_product'    : RPNOperator( multiplyListOfPolynomials,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'polynomial_sum'        : RPNOperator( sumListOfPolynomials,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'solve'                 : RPNOperator( solvePolynomial,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # arithmetic
    'equals_one_of'         : RPNOperator( equalsOneOf,
                                           2, [ RPNArgumentType.Default, RPNArgumentType.List ], [ ],
                                           RPNOperator.measurementsAllowed ),

    'gcd'                   : RPNOperator( getGCDOfList,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'geometric_mean'        : RPNOperator( calculateGeometricMean,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'harmonic_mean'         : RPNOperator( calculateHarmonicMean,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'lcm'                   : RPNOperator( getLCMOfList,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'maximum'               : RPNOperator( getMaximum,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'mean'                  : RPNOperator( calculateArithmeticMean,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'minimum'               : RPNOperator( getMinimum,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'product'               : RPNOperator( getProduct,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'stddev'                : RPNOperator( getStandardDeviation,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'sum'                   : RPNOperator( getSum,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # combinatoric
    'denomination_combinations' : RPNOperator( getDenominationCombinations,
                                               2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'multinomial'           : RPNOperator( getMultinomial,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # conversion
    'convert'               : RPNOperator( convertUnits,
                                           2, [ RPNArgumentType.List ], [ ] ),   # list arguments are special

    'latlong_to_nac'        : RPNOperator( convertLatLongToNAC,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'unpack'                : RPNOperator( unpackInteger,
                                           2, [ RPNArgumentType.Integer, RPNArgumentType.List ], [ ] ),

    'pack'                  : RPNOperator( packInteger,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    # date_time
    'make_datetime'         : RPNOperator( makeDateTime,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'make_iso_time'         : RPNOperator( makeISOTime,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'make_julian_time'      : RPNOperator( makeJulianTime,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # function
    'break_on'              : RPNOperator( breakOnCondition,
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'filter'                : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'filter_list'           : RPNOperator( lambda n, k: RPNGenerator( filterListOfLists( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'filter_by_index'       : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'for_each'              : RPNOperator( lambda n, k: RPNGenerator( forEach( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'for_each_list'         : RPNOperator( lambda n, k: RPNGenerator( forEachList( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'unfilter'              : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k, True ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    'unfilter_by_index'     : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k, True ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Function ], [ ] ),

    # lexicographic
    'combine_digits'        : RPNOperator( combineDigits,
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    # list
    'alternate_signs'       : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, False ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'alternate_signs_2'     : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, True ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'alternating_sum'       : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'alternating_sum_2'     : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'and_all'               : RPNOperator( getAndAll,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'append'                : RPNOperator( appendLists,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'collate'               : RPNOperator( lambda n: RPNGenerator( collate( n ) ),
                                           1, [ RPNArgumentType.List ], [ ] ),

    'compare_lists'         : RPNOperator( compareLists,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'count'                 : RPNOperator( countElements,
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'cumulative_diffs'      : RPNOperator( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'cumulative_ratios'     : RPNOperator( lambda n: RPNGenerator( getCumulativeListRatios( n ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'difference'            : RPNOperator( getDifference,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'diffs'                 : RPNOperator( lambda n: RPNGenerator( getListDiffs( n ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'element'               : RPNOperator( getListElement,
                                           2, [ RPNArgumentType.List, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'enumerate'             : RPNOperator( lambda n, k: RPNGenerator( enumerateList( n, k ) ),
                                           2, [ RPNArgumentType.List, RPNArgumentType.Integer ], [ ] ),

    'find'                  : RPNOperator( findInList,
                                           2, [ RPNArgumentType.List, RPNArgumentType.Default ], [ ] ),

    'flatten'               : RPNOperator( flatten,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'get_combinations'      : RPNOperator( getListCombinations,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'get_repeat_combinations'   : RPNOperator( getListCombinationsWithRepeats,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'get_permutations'      : RPNOperator( getListPermutations,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'get_repeat_permutations'   : RPNOperator( getListPermutationsWithRepeats,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'group_elements'        : RPNOperator( groupElements,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'interleave'            : RPNOperator( interleave,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'intersection'          : RPNOperator( makeIntersection,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'is_palindrome_list'    : RPNOperator( isPalindromeList,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'left'                  : RPNOperator( getLeft,
                                           2, [ RPNArgumentType.List, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'max_index'             : RPNOperator( getIndexOfMax,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'min_index'             : RPNOperator( getIndexOfMin,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'nand_all'              : RPNOperator( getNandAll,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'nonzero'               : RPNOperator( getNonzeroes,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'nor_all'               : RPNOperator( getNorAll,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'occurrences'           : RPNOperator( getOccurrences,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'occurrence_cumulative' : RPNOperator( getCumulativeOccurrenceRatios,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'occurrence_ratios'     : RPNOperator( getOccurrenceRatios,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'or_all'                : RPNOperator( getOrAll,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'permute_lists'         : RPNOperator( permuteLists,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'powerset'              : RPNOperator( lambda n: RPNGenerator( getPowerset( n ) ),
                                           1, [ RPNArgumentType.List ], [ ] ),

    'random_element'        : RPNOperator( getRandomElement,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'ratios'                : RPNOperator( lambda n: RPNGenerator( getListRatios( n ) ),
                                           1, [ RPNArgumentType.Generator ], [ ] ),

    'reduce'                : RPNOperator( reduceList,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'reverse'               : RPNOperator( getReverse,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'right'                 : RPNOperator( getRight,
                                           2, [ RPNArgumentType.List, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'shuffle'               : RPNOperator( shuffleList,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'slice'                 : RPNOperator( lambda a, b, c: RPNGenerator( getSlice( a, b, c ) ),
                                           3, [ RPNArgumentType.List, RPNArgumentType.Integer,
                                                RPNArgumentType.Integer ], [ ] ),

    'sort'                  : RPNOperator( sortAscending,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'sort_descending'       : RPNOperator( sortDescending,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'sublist'               : RPNOperator( lambda a, b, c: RPNGenerator( getSublist( a, b, c ) ),
                                           3, [ RPNArgumentType.List, RPNArgumentType.Integer,
                                                RPNArgumentType.Integer ], [ ] ),

    'union'                 : RPNOperator( makeUnion,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'unique'                : RPNOperator( getUniqueElements,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'zero'                  : RPNOperator( getZeroes,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # number_theory
    'base'                  : RPNOperator( interpretAsBaseOperator,
                                           2, [ RPNArgumentType.List, RPNArgumentType.PositiveInteger ], [ ] ),

    'cf'                    : RPNOperator( convertFromContinuedFraction,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'crt'                   : RPNOperator( calculateChineseRemainderTheorem,
                                           2, [ RPNArgumentType.List, RPNArgumentType.List ], [ ] ),

    'frobenius'             : RPNOperator( getFrobeniusNumber,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'geometric_recurrence'  : RPNOperator( lambda a, b, c, d: RPNGenerator( getGeometricRecurrence( a, b, c, d ) ),
                                           4, [ RPNArgumentType.List, RPNArgumentType.List, RPNArgumentType.List,
                                                RPNArgumentType.PositiveInteger ], [ ] ),

    'is_friendly'           : RPNOperator( isFriendly,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'linear_recurrence'     : RPNOperator( lambda a, b, c: RPNGenerator( getLinearRecurrence( a, b, c ) ),
                                           3, [ RPNArgumentType.List, RPNArgumentType.List,
                                                RPNArgumentType.PositiveInteger ], [ ] ),

    'linear_recurrence_with_modulo' : RPNOperator( lambda a, b, c, d: RPNGenerator( getLinearRecurrenceWithModulo( a, b, c, d ) ),
                                           4, [ RPNArgumentType.List, RPNArgumentType.List,
                                                RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    # powers_and_roots
    'power_tower'           : RPNOperator( calculatePowerTower,
                                           1, [ RPNArgumentType.List ], [ ] ),

    'power_tower2'          : RPNOperator( calculatePowerTower2,
                                           1, [ RPNArgumentType.List ], [ ] ),

    # special
    'echo'                  : RPNOperator( addEchoArgument,
                                           1, [ RPNArgumentType.Default ], [ ] ),
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
# //  Note:  There is something about the way some of the mpmath functions are
# //  defined causes them not to work when used in a user-defined function.  So,
# //  they are all wrapped in a lambda.
# //
# //******************************************************************************

operators = {
    # algebra
    'find_polynomial'                : RPNOperator( findPolynomial,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.PositiveInteger ], [ ] ),

    'solve_cubic'                    : RPNOperator( solveCubicPolynomial,
                                                    4, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'solve_quadratic'                : RPNOperator( solveQuadraticPolynomial,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default ], [ ] ),

    'solve_quartic'                  : RPNOperator( solveQuarticPolynomial,
                                                    5, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default ], [ ] ),

    # arithmetic
    'abs'                            : RPNOperator( getAbsoluteValue,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'add'                            : RPNOperator( add,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'ceiling'                        : RPNOperator( getCeiling,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'decrement'                      : RPNOperator( decrement,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'divide'                         : RPNOperator( divide,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'floor'                          : RPNOperator( getFloor,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'gcd2'                           : RPNOperator( getGCD,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'increment'                      : RPNOperator( increment,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'is_divisible'                   : RPNOperator( isDivisible,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'is_equal'                       : RPNOperator( isEqual,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'is_even'                        : RPNOperator( isEven,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'is_greater'                     : RPNOperator( isGreater,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'is_integer'                     : RPNOperator( isInteger,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'is_kth_power'                   : RPNOperator( isKthPower,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_less'                        : RPNOperator( isLess,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'is_not_equal'                   : RPNOperator( isNotEqual,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'is_not_greater'                 : RPNOperator( isNotGreater,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'is_not_less'                    : RPNOperator( isNotLess,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'is_not_zero'                    : RPNOperator( isNotZero,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'is_odd'                         : RPNOperator( isOdd,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'is_power_of_k'                  : RPNOperator( isPower,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_square'                      : RPNOperator( isSquare,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'is_zero'                        : RPNOperator( isZero,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'larger'                         : RPNOperator( getLarger,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'lcm2'                           : RPNOperator( getLCM,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'mantissa'                       : RPNOperator( getMantissa,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'modulo'                         : RPNOperator( getModulo,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'multiply'                       : RPNOperator( multiply,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'nearest_int'                    : RPNOperator( getNearestInt,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'negative'                       : RPNOperator( getNegative,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'reciprocal'                     : RPNOperator( takeReciprocal,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'round'                          : RPNOperator( roundOff,
                                                    1, [ RPNArgumentType.Real ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'round_by_digits'                : RPNOperator( roundByDigits,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Integer ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'round_by_value'                 : RPNOperator( roundByValue,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.NonnegativeReal ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sign'                           : RPNOperator( getSign,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'smaller'                        : RPNOperator( getSmaller,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'subtract'                       : RPNOperator( subtract,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    # astronomy
    'angular_separation'             : RPNOperator( getAngularSeparation,
                                                    4, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.AstronomicalObject,
                                                         RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'angular_size'                   : RPNOperator( getAngularSize,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'antitransit_time'               : RPNOperator( getAntitransitTime,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'astronomical_dawn'              : RPNOperator( getNextAstronomicalDawn,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'astronomical_dusk'              : RPNOperator( getNextAstronomicalDusk,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'autumnal_equinox'               : RPNOperator( getAutumnalEquinox,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'dawn'                           : RPNOperator( getNextCivilDawn,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'day_time'                       : RPNOperator( getDayTime,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'distance_from_earth'            : RPNOperator( getDistanceFromEarth,
                                                    2, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.DateTime ], [ ] ),

    'dusk'                           : RPNOperator( getNextCivilDusk,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'eclipse_totality'               : RPNOperator( getEclipseTotality,
                                                    4, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.AstronomicalObject,
                                                         RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'moonrise'                       : RPNOperator( getNextMoonRise,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'moonset'                        : RPNOperator( getNextMoonSet,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'moon_antitransit'               : RPNOperator( getNextMoonAntitransit,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'moon_phase'                     : RPNOperator( getMoonPhase,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'moon_transit'                   : RPNOperator( getNextMoonTransit,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'nautical_dawn'                  : RPNOperator( getNextNauticalDawn,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'nautical_dusk'                  : RPNOperator( getNextNauticalDusk,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'next_antitransit'               : RPNOperator( getNextAntitransit,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'next_first_quarter_moon'        : RPNOperator( getNextFirstQuarterMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'next_full_moon'                 : RPNOperator( getNextFullMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'next_last_quarter_moon'         : RPNOperator( getNextLastQuarterMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'next_new_moon'                  : RPNOperator( getNextNewMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'next_rising'                    : RPNOperator( getNextRising,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'next_setting'                   : RPNOperator( getNextSetting,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'next_transit'                   : RPNOperator( getNextTransit,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'night_time'                     : RPNOperator( getNightTime,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'previous_antitransit'           : RPNOperator( getPreviousAntitransit,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'previous_first_quarter_moon'    : RPNOperator( getPreviousFirstQuarterMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'previous_full_moon'             : RPNOperator( getPreviousFullMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'previous_last_quarter_moon'     : RPNOperator( getPreviousLastQuarterMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'previous_new_moon'              : RPNOperator( getPreviousNewMoon,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'previous_rising'                : RPNOperator( getPreviousRising,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'previous_setting'               : RPNOperator( getPreviousSetting,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'previous_transit'               : RPNOperator( getPreviousTransit,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'sky_location'                   : RPNOperator( getSkyLocation,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'solar_noon'                     : RPNOperator( getSolarNoon,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'summer_solstice'                : RPNOperator( getSummerSolstice,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sunrise'                        : RPNOperator( getNextSunrise,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'sunset'                         : RPNOperator( getNextSunset,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'sun_antitransit'                : RPNOperator( getNextSunAntitransit,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.DateTime ], [ ] ),

    'transit_time'                   : RPNOperator( getTransitTime,
                                                    3, [ RPNArgumentType.AstronomicalObject, RPNArgumentType.Location,
                                                         RPNArgumentType.DateTime ], [ ] ),

    'vernal_equinox'                 : RPNOperator( getVernalEquinox,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'winter_solstice'                : RPNOperator( getWinterSolstice,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    # astronomy - heavenly body operators
    'sun'                            : RPNOperator( lambda: RPNAstronomicalObject( ephem.Sun( ) ),
                                                    0, [ ], [ ] ),

    'mercury'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mercury( ) ),
                                                    0, [ ], [ ] ),

    'venus'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Venus( ) ),
                                                    0, [ ], [ ] ),

    'moon'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Moon( ) ),
                                                    0, [ ], [ ] ),

    'mars'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mars( ) ),
                                                    0, [ ], [ ] ),

    'jupiter'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Jupiter( ) ),
                                                    0, [ ], [ ] ),

    'saturn'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Saturn( ) ),
                                                    0, [ ], [ ] ),

    'uranus'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Uranus( ) ),
                                                    0, [ ], [ ] ),

    'neptune'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Neptune( ) ),
                                                    0, [ ], [ ] ),

    'pluto'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Pluto( ) ),
                                                    0, [ ], [ ] ),

    # bitwise
    'bitwise_and'                    : RPNOperator( getBitwiseAnd,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'bitwise_nand'                   : RPNOperator( getBitwiseNand,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'bitwise_nor'                    : RPNOperator( getBitwiseNor,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'bitwise_not'                    : RPNOperator( getInvertedBits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'bitwise_or'                     : RPNOperator( getBitwiseOr,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'bitwise_xor'                    : RPNOperator( getBitwiseXor,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'count_bits'                     : RPNOperator( getBitCountOperator,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'parity'                         : RPNOperator( getParity,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'shift_left'                     : RPNOperator( shiftLeft,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'shift_right'                    : RPNOperator( shiftRight,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    # calendar
    'advent'                         : RPNOperator( calculateAdvent,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'ascension'                      : RPNOperator( calculateAscensionThursday,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'ash_wednesday'                  : RPNOperator( calculateAshWednesday,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'calendar'                       : RPNOperator( generateMonthCalendar,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'christmas'                      : RPNOperator( getChristmasDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'columbus_day'                   : RPNOperator( calculateColumbusDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'dst_end'                        : RPNOperator( calculateDSTEnd,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'dst_start'                      : RPNOperator( calculateDSTStart,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'easter'                         : RPNOperator( calculateEaster,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'election_day'                   : RPNOperator( calculateElectionDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'epiphany'                       : RPNOperator( getEpiphanyDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'fathers_day'                    : RPNOperator( calculateFathersDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'from_bahai'                     : RPNOperator( convertBahaiDate,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_hebrew'                    : RPNOperator( convertHebrewDate,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_indian_civil'              : RPNOperator( convertIndianCivilDate,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_islamic'                   : RPNOperator( convertIslamicDate,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_julian'                    : RPNOperator( convertJulianDate,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_mayan'                     : RPNOperator( convertMayanDate,
                                                    5, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'from_persian'                   : RPNOperator( convertPersianDate,
                                                    3, [ RPNArgumentType.Integer, RPNArgumentType.Integer,
                                                         RPNArgumentType.Integer ], [ ] ),

    'good_friday'                    : RPNOperator( calculateGoodFriday,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'independence_day'               : RPNOperator( getIndependenceDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'iso_date'                       : RPNOperator( getISODate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'labor_day'                      : RPNOperator( calculateLaborDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'martin_luther_king_day'         : RPNOperator( calculateMartinLutherKingDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'memorial_day'                   : RPNOperator( calculateMemorialDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'mothers_day'                    : RPNOperator( calculateMothersDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'new_years_day'                  : RPNOperator( getNewYearsDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_weekday'                    : RPNOperator( calculateNthWeekdayOfMonth,
                                                    4, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                         RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_weekday_of_year'            : RPNOperator( calculateNthWeekdayOfYear,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.Integer,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'pentecost'                      : RPNOperator( calculatePentecostSunday,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'presidents_day'                 : RPNOperator( calculatePresidentsDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'thanksgiving'                   : RPNOperator( calculateThanksgiving,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'to_bahai'                       : RPNOperator( getBahaiCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_bahai_name'                  : RPNOperator( getBahaiCalendarDateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_hebrew'                      : RPNOperator( getHebrewCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_hebrew_name'                 : RPNOperator( getHebrewCalendarDateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_indian_civil'                : RPNOperator( getIndianCivilCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_indian_civil_name'           : RPNOperator( getIndianCivilCalendarDateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_islamic'                     : RPNOperator( getIslamicCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_islamic_name'                : RPNOperator( getIslamicCalendarDateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_iso'                         : RPNOperator( getISODate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_iso_name'                    : RPNOperator( getISODateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_julian'                      : RPNOperator( getJulianCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_julian_day'                  : RPNOperator( getJulianDay,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_lilian_day'                  : RPNOperator( getLilianDay,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_mayan'                       : RPNOperator( getMayanCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_ordinal_date'                : RPNOperator( getOrdinalDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_persian'                     : RPNOperator( getPersianCalendarDate,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'to_persian_name'                : RPNOperator( getPersianCalendarDateName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'veterans_day'                   : RPNOperator( getVeteransDay,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'weekday'                        : RPNOperator( getWeekday,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'weekday_name'                   : RPNOperator( getWeekdayName,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'year_calendar'                  : RPNOperator( generateYearCalendar,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    # chemistry
    'atomic_number'                  : RPNOperator( getAtomicNumber,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'atomic_symbol'                  : RPNOperator( getAtomicSymbol,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'atomic_weight'                  : RPNOperator( getAtomicWeight,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'element_block'                  : RPNOperator( getElementBlock,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_boiling_point'          : RPNOperator( getElementBoilingPoint,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_density'                : RPNOperator( getElementDensity,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_description'            : RPNOperator( getElementDescription,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_group'                  : RPNOperator( getElementGroup,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_melting_point'          : RPNOperator( getElementMeltingPoint,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_name'                   : RPNOperator( getElementName,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_occurrence'             : RPNOperator( getElementOccurrence,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_period'                 : RPNOperator( getElementPeriod,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'element_state'                  : RPNOperator( getElementState,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'molar_mass'                     : RPNOperator( getMolarMass,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    # combinatoric
    'arrangements'                   : RPNOperator( getArrangements,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'bell_polynomial'                : RPNOperator( getBellPolynomial,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'binomial'                       : RPNOperator( getBinomial,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'combinations'                   : RPNOperator( getCombinations,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'compositions'                   : RPNOperator( getCompositions,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'debruijn'                       : RPNOperator( getDeBruijnSequence,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'lah'                            : RPNOperator( getLahNumber,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'nth_menage'                     : RPNOperator( getNthMenageNumber,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'multifactorial'                 : RPNOperator( getNthMultifactorial,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'narayana'                       : RPNOperator( getNarayanaNumber,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'nth_apery'                      : RPNOperator( getNthAperyNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_bell'                       : RPNOperator( getNthBell,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_bernoulli'                  : RPNOperator( getNthBernoulli,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_catalan'                    : RPNOperator( getNthCatalanNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_delannoy'                   : RPNOperator( getNthDelannoyNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_motzkin'                    : RPNOperator( getNthMotzkinNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_pell'                       : RPNOperator( getNthPellNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_schroeder'                  : RPNOperator( getNthSchroederNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_schroeder_hipparchus'       : RPNOperator( getNthSchroederHipparchusNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_sylvester'                  : RPNOperator( getNthSylvesterNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'partitions'                     : RPNOperator( getPartitionNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'permutations'                   : RPNOperator( getPermutations,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    # complex
    'argument'                       : RPNOperator( getArgument,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'conjugate'                      : RPNOperator( getConjugate,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'i'                              : RPNOperator( getI,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'imaginary'                      : RPNOperator( getImaginary,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'real'                           : RPNOperator( getReal,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    # conversion
    'char'                           : RPNOperator( convertToChar,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'dhms'                           : RPNOperator( convertToDHMS,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'dms'                            : RPNOperator( convertToDMS,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'double'                         : RPNOperator( convertToDouble,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'float'                          : RPNOperator( convertToFloat,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'from_unix_time'                 : RPNOperator( convertFromUnixTime,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'hms'                            : RPNOperator( convertToHMS,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'integer'                        : RPNOperator( convertToSignedIntOperator,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'invert_units'                   : RPNOperator( invertUnits,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'long'                           : RPNOperator( convertToLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'longlong'                       : RPNOperator( convertToLongLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'quadlong'                       : RPNOperator( convertToQuadLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    # pack ???

    'short'                          : RPNOperator( convertToShort,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'to_unix_time'                   : RPNOperator( convertToUnixTime,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'uchar'                          : RPNOperator( convertToUnsignedChar,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'uinteger'                       : RPNOperator( convertToUnsignedInt,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'ulong'                          : RPNOperator( convertToUnsignedLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'ulonglong'                      : RPNOperator( convertToUnsignedLongLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'undouble'                       : RPNOperator( interpretAsDouble,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'unfloat'                        : RPNOperator( interpretAsFloat,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    # unpack ???

    'uquadlong'                      : RPNOperator( convertToUnsignedQuadLong,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'ushort'                         : RPNOperator( convertToUnsignedShort,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'ydhms'                          : RPNOperator( convertToYDHMS,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),
    # date_time
    'get_year'                       : RPNOperator( getYear,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'get_month'                      : RPNOperator( getMonth,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'get_day'                        : RPNOperator( getDay,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'get_hour'                       : RPNOperator( getHour,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'get_minute'                     : RPNOperator( getMinute,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'get_second'                     : RPNOperator( getSecond,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'iso_day'                        : RPNOperator( getISODay,
                                                    1, [ RPNArgumentType.DateTime ], [ ] ),

    'now'                            : RPNOperator( RPNDateTime.getNow,
                                                    0, [ ], [ ] ),

    'today'                          : RPNOperator( getToday,
                                                    0, [ ], [ ] ),

    'tomorrow'                       : RPNOperator( getTomorrow,
                                                    0, [ ], [ ] ),

    'yesterday'                      : RPNOperator( getYesterday,
                                                    0, [ ], [ ] ),

    # figurate
    'centered_cube'                  : RPNOperator( getNthCenteredCubeNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_decagonal'             : RPNOperator( getNthCenteredDecagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_dodecahedral'          : RPNOperator( getNthCenteredDodecahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_heptagonal'            : RPNOperator( getNthCenteredHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_hexagonal'             : RPNOperator( getNthCenteredHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_icosahedral'           : RPNOperator( getNthCenteredIcosahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_nonagonal'             : RPNOperator( getNthCenteredNonagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_octagonal'             : RPNOperator( getNthCenteredOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_octahedral'            : RPNOperator( getNthCenteredOctahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_pentagonal'            : RPNOperator( getNthCenteredPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_polygonal'             : RPNOperator( getNthCenteredPolygonalNumberOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_square'                : RPNOperator( getNthCenteredSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_tetrahedral'           : RPNOperator( getNthCenteredTetrahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'centered_triangular'            : RPNOperator( getNthCenteredTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal'                      : RPNOperator( getNthDecagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_centered_square'      : RPNOperator( getNthDecagonalCenteredSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_heptagonal'           : RPNOperator( getNthDecagonalHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_hexagonal'            : RPNOperator( getNthDecagonalHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_nonagonal'            : RPNOperator( getNthDecagonalNonagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_octagonal'            : RPNOperator( getNthDecagonalOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_pentagonal'           : RPNOperator( getNthDecagonalPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'decagonal_triangular'           : RPNOperator( getNthDecagonalTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'dodecahedral'                   : RPNOperator( getNthDodecahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'generalized_pentagonal'         : RPNOperator( getNthGeneralizedPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'heptagonal'                     : RPNOperator( getNthHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'heptagonal_hexagonal'           : RPNOperator( getNthHeptagonalHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'heptagonal_pentagonal'          : RPNOperator( getNthHeptagonalPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'heptagonal_square'              : RPNOperator( getNthHeptagonalSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'heptagonal_triangular'          : RPNOperator( getNthHeptagonalTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hexagonal'                      : RPNOperator( getNthHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hexagonal_pentagonal'           : RPNOperator( getNthHexagonalPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hexagonal_square'               : RPNOperator( getNthHexagonalSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'icosahedral'                    : RPNOperator( getNthIcosahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal'                      : RPNOperator( getNthNonagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_heptagonal'           : RPNOperator( getNthNonagonalHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_hexagonal'            : RPNOperator( getNthNonagonalHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_octagonal'            : RPNOperator( getNthNonagonalOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_pentagonal'           : RPNOperator( getNthNonagonalPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_square'               : RPNOperator( getNthNonagonalSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nonagonal_triangular'           : RPNOperator( getNthNonagonalTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_decagonal'         : RPNOperator( findCenteredDecagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_heptagonal'        : RPNOperator( findCenteredHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_hexagonal'         : RPNOperator( findCenteredHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_nonagonal'         : RPNOperator( findCenteredNonagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_octagonal'         : RPNOperator( findCenteredOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_pentagonal'        : RPNOperator( findCenteredPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_polygonal'         : RPNOperator( findCenteredPolygonalNumberOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_square'            : RPNOperator( findCenteredSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_centered_triangular'        : RPNOperator( findCenteredTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_decagonal'                  : RPNOperator( findDecagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_heptagonal'                 : RPNOperator( findHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_hexagonal'                  : RPNOperator( findHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_nonagonal'                  : RPNOperator( findNonagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_octagonal'                  : RPNOperator( findOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_pentagonal'                 : RPNOperator( findPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_polygonal'                  : RPNOperator( findPolygonalNumberOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_square'                     : RPNOperator( findSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_triangular'                 : RPNOperator( findTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal'                      : RPNOperator( getNthOctagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal_heptagonal'           : RPNOperator( getNthOctagonalHeptagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal_hexagonal'            : RPNOperator( getNthOctagonalHexagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal_pentagonal'           : RPNOperator( getNthOctagonalPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal_square'               : RPNOperator( getNthOctagonalSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octagonal_triangular'           : RPNOperator( getNthOctagonalTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octahedral'                     : RPNOperator( getNthOctahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pentagonal'                     : RPNOperator( getNthPentagonalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pentagonal_square'              : RPNOperator( getNthPentagonalSquareNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pentagonal_triangular'          : RPNOperator( getNthPentagonalTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pentatope'                      : RPNOperator( getNthPentatopeNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'polygonal'                      : RPNOperator( getNthPolygonalNumberOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'polytope'                       : RPNOperator( getNthPolytopeNumber,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'pyramid'                        : RPNOperator( getNthPyramidalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'rhombic_dodecahedral'           : RPNOperator( getNthRhombicDodecahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'square_triangular'              : RPNOperator( getNthSquareTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'star'                           : RPNOperator( getNthStarNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'stella_octangula'               : RPNOperator( getNthStellaOctangulaNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'tetrahedral'                    : RPNOperator( getNthTetrahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'triangular'                     : RPNOperator( getNthTriangularNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'truncated_octahedral'           : RPNOperator( getNthTruncatedOctahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'truncated_tetrahedral'          : RPNOperator( getNthTruncatedTetrahedralNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    # function
    'eval0'                           : RPNOperator( evaluateFunction0,
                                                    1, [ RPNArgumentType.Function ], [ ] ),

    'eval'                           : RPNOperator( evaluateFunction,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'eval2'                          : RPNOperator( evaluateFunction2,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Function ], [ ] ),

    'eval3'                          : RPNOperator( evaluateFunction3,
                                                    4, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'eval_list'                      : RPNOperator( evaluateListFunction,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'eval_list2'                     : RPNOperator( evaluateListFunction2,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Function ], [ ] ),

    'eval_list3'                     : RPNOperator( evaluateListFunction3,
                                                    4, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'function'                       : RPNOperator( createUserFunction,
                                                    2, [ RPNArgumentType.String, RPNArgumentType.Function ], [ ] ),

    'limit'                          : RPNOperator( evaluateLimit,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'limitn'                         : RPNOperator( evaluateReverseLimit,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'nprod'                          : RPNOperator( evaluateProduct,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Function ], [ ] ),

    'nsum'                           : RPNOperator( evaluateSum,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Function ], [ ] ),

    'plot'                           : RPNOperator( plotFunction,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Function ], [ ] ),

    'plot2'                          : RPNOperator( plot2DFunction,
                                                    5, [ RPNArgumentType.Default, RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'plotc'                          : RPNOperator( plotComplexFunction,
                                                    5, [ RPNArgumentType.Default, RPNArgumentType.Default, RPNArgumentType.Default,
                                                         RPNArgumentType.Default, RPNArgumentType.Function ], [ ] ),

    'recurrence'                     : RPNOperator( evaluateRecurrence,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.PositiveInteger, RPNArgumentType.Function ], [ ] ),

    'repeat'                         : RPNOperator( repeat,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.Function ], [ ] ),

    # geography
    'geo_distance'                   : RPNOperator( getDistance,
                                                    2, [ RPNArgumentType.Location, RPNArgumentType.Location ], [ ] ),

    'get_timezone'                   : RPNOperator( getTimeZone,
                                                    1, [ RPNArgumentType.Location ], [ ] ),

    'lat_long'                       : RPNOperator( lambda n, k: RPNLocation( n, k ),
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'location'                       : RPNOperator( getLocation,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'location_info'                  : RPNOperator( getLocationInfo,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    # geometry
    'antiprism_area'                 : RPNOperator( getAntiprismSurfaceArea,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal ], [ ] ),

    'antiprism_volume'               : RPNOperator( getAntiprismVolume,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal ], [ ] ),

    'cone_area'                      : RPNOperator( getConeSurfaceArea,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'cone_volume'                    : RPNOperator( getConeVolume,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'dodecahedron_area'              : RPNOperator( getDodecahedronSurfaceArea,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'dodecahedron_volume'            : RPNOperator( getDodecahedronVolume,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'hypotenuse'                     : RPNOperator( calculateHypotenuse,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'icosahedron_area'               : RPNOperator( getIcosahedronSurfaceArea,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'icosahedron_volume'             : RPNOperator( getIcosahedronVolume,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'k_sphere_area'                  : RPNOperator( getKSphereSurfaceAreaOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal ], [ ],
                                                         RPNOperator.measurementsAllowed ),

    'k_sphere_radius'                : RPNOperator( getKSphereRadiusOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal ], [ ],
                                                             RPNOperator.measurementsAllowed ),

    'k_sphere_volume'                : RPNOperator( getKSphereVolumeOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal ], [ ],
                                                         RPNOperator.measurementsAllowed ),

    'octahedron_area'                : RPNOperator( getOctahedronSurfaceArea,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'octahedron_volume'              : RPNOperator( getOctahedronVolume,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'polygon_area'                   : RPNOperator( getRegularPolygonAreaOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.Measurement ], [ ] ),

    'prism_area'                     : RPNOperator( getPrismSurfaceArea,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal,
                                                         RPNArgumentType.NonnegativeReal ], [ ] ),

    'prism_volume'                   : RPNOperator( getPrismVolume,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.NonnegativeReal,
                                                         RPNArgumentType.NonnegativeReal ], [ ] ),

    'sphere_area'                    : RPNOperator( getSphereArea,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_radius'                  : RPNOperator( getSphereRadius,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sphere_volume'                  : RPNOperator( getSphereVolume,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'tetrahedron_area'               : RPNOperator( getTetrahedronSurfaceArea,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'tetrahedron_volume'             : RPNOperator( getTetrahedronVolume,
                                                    1, [ RPNArgumentType.NonnegativeReal ], [ ] ),

    'torus_area'                     : RPNOperator( getTorusSurfaceArea,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'torus_volume'                   : RPNOperator( getTorusVolume,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'triangle_area'                  : RPNOperator( getTriangleArea,
                                                    3, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal,
                                                         RPNArgumentType.NonnegativeReal ], [ ] ),

    # lexicographic
    'add_digits'                     : RPNOperator( addDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'build_numbers'                  : RPNOperator( buildNumbers,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'build_step_numbers'             : RPNOperator( buildStepNumbers,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'count_different_digits'         : RPNOperator( countDifferentDigits,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'count_digits'                   : RPNOperator( countDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'cyclic_permutations'            : RPNOperator( getCyclicPermutations,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'digits'                         : RPNOperator( getDigitCount,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'duplicate_digits'               : RPNOperator( duplicateDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'duplicate_number'               : RPNOperator( duplicateNumber,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'erdos_persistence'              : RPNOperator( getErdosPersistence,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'find_palindrome'                : RPNOperator( findPalindrome,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'get_base_k_digits'              : RPNOperator( getBaseKDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'get_digits'                     : RPNOperator( getDigits,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'get_left_digits'                : RPNOperator( getLeftDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'get_left_truncations'           : RPNOperator( getLeftTruncationsGenerator,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'get_nonzero_base_k_digits'      : RPNOperator( getNonzeroBaseKDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'get_nonzero_digits'             : RPNOperator( getNonzeroDigits,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'get_right_digits'                : RPNOperator( getRightDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'get_right_truncations'          : RPNOperator( getRightTruncationsGenerator,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'has_any_digits'                 : RPNOperator( containsAnyDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'has_digits'                     : RPNOperator( containsDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'has_only_digits'                : RPNOperator( containsOnlyDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'is_automorphic'                 : RPNOperator( isAutomorphic,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_base_k_pandigital'           : RPNOperator( isBaseKPandigital,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_base_k_smith_number'         : RPNOperator( isBaseKSmithNumber,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_bouncy'                      : RPNOperator( isBouncy,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_decreasing'                  : RPNOperator( isDecreasing,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_digital_permutation'         : RPNOperator( isDigitalPermutation,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_generalized_dudeney'         : RPNOperator( isGeneralizedDudeneyNumber,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_harshad'                     : RPNOperator( isHarshadNumber,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_increasing'                  : RPNOperator( isIncreasing,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_kaprekar'                    : RPNOperator( isKaprekar,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_k_morphic'                   : RPNOperator( isKMorphicOperator,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_k_narcissistic'              : RPNOperator( isBaseKNarcissistic,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_narcissistic'                : RPNOperator( isNarcissistic,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_order_k_smith_number'        : RPNOperator( isOrderKSmithNumber,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_palindrome'                  : RPNOperator( isPalindrome,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_pandigital'                  : RPNOperator( isPandigital,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_pddi'                        : RPNOperator( isPerfectDigitToDigitInvariant,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_pdi'                         : RPNOperator( isPerfectDigitalInvariant,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_smith_number'                : RPNOperator( isSmithNumber,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_step_number'                 : RPNOperator( isStepNumber,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_sum_product'                 : RPNOperator( isSumProductNumber,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_trimorphic'                  : RPNOperator( isTrimorphic,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'k_persistence'                  : RPNOperator( getKPersistence,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'multiply_digits'                : RPNOperator( multiplyDigits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'multiply_digit_powers'          : RPNOperator( multiplyDigitPowers,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'multiply_nonzero_digits'        : RPNOperator( multiplyNonzeroDigits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'multiply_nonzero_digit_powers'  : RPNOperator( multiplyNonzeroDigitPowers,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'permute_digits'                 : RPNOperator( permuteDigits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'persistence'                    : RPNOperator( getPersistence,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'replace_digits'                 : RPNOperator( replaceDigits,
                                                    3, [ RPNArgumentType.Integer, RPNArgumentType.NonnegativeInteger,
                                                         RPNArgumentType.NonnegativeInteger ], [ ] ),

    'reverse_digits'                 : RPNOperator( reverseDigits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'rotate_digits_left'             : RPNOperator( rotateDigitsLeft,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.Integer ], [ ] ),

    'rotate_digits_right'            : RPNOperator( rotateDigitsRight,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.Integer ], [ ] ),

    'show_erdos_persistence'         : RPNOperator( showErdosPersistence,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'show_k_persistence'             : RPNOperator( showKPersistence,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'show_persistence'               : RPNOperator( showPersistence,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'square_digit_chain'             : RPNOperator( generateSquareDigitChain,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sum_digits'                     : RPNOperator( sumDigits,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    # list
    'exponential_range'              : RPNOperator( createExponentialRange,
                                                    3, [ RPNArgumentType.Real, RPNArgumentType.Real,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'geometric_range'                : RPNOperator( createGeometricRange,
                                                    3, [ RPNArgumentType.Real, RPNArgumentType.Real,
                                                         RPNArgumentType.PositiveInteger ], [ ] ),

    'interval_range'                 : RPNOperator( createIntervalRangeOperator,
                                                    3, [ RPNArgumentType.Real, RPNArgumentType.Real,
                                                         RPNArgumentType.Real ], [ ] ),

    'range'                          : RPNOperator( createRange,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'sized_range'                    : RPNOperator( createSizedRangeOperator,
                                                    3, [ RPNArgumentType.Real, RPNArgumentType.Real,
                                                         RPNArgumentType.Real ], [ ] ),

    # logarithms
    'lambertw'                       : RPNOperator( getLambertW,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'li'                             : RPNOperator( getLI,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'log'                            : RPNOperator( getLog,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'log10'                          : RPNOperator( getLog10,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'log2'                           : RPNOperator( getLog2,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'logxy'                          : RPNOperator( getLogXY,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'polyexp'                        : RPNOperator( getPolyexp,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'polylog'                        : RPNOperator( getPolylog,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    # logical
    'and'                            : RPNOperator( andOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'nand'                           : RPNOperator( nandOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'nor'                            : RPNOperator( norOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'not'                            : RPNOperator( notOperand,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'or'                             : RPNOperator( orOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'xnor'                           : RPNOperator( xnorOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'xor'                            : RPNOperator( xorOperands,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    # number_theory
    'abundance'                      : RPNOperator( getAbundance,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'abundance_ratio'                : RPNOperator( getAbundanceRatio,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'aliquot'                        : RPNOperator( getAliquotSequence,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'aliquot_limit'                  : RPNOperator( getLimitedAliquotSequence,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'alternating_factorial'          : RPNOperator( getNthAlternatingFactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'barnesg'                        : RPNOperator( getBarnesG,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'beta'                           : RPNOperator( getBeta,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'calkin_wilf'                    : RPNOperator( getNthCalkinWilf,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'collatz'                        : RPNOperator( getCollatzSequence,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'count_divisors'                 : RPNOperator( getDivisorCount,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'cyclotomic'                     : RPNOperator( getCyclotomic,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.Default ], [ ] ),

    'digamma'                        : RPNOperator( getDigamma,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'digital_root'                   : RPNOperator( getDigitalRoot,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'divisors'                       : RPNOperator( getDivisors,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'double_factorial'               : RPNOperator( getNthDoubleFactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'egypt'                          : RPNOperator( getGreedyEgyptianFraction,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'eta'                            : RPNOperator( getAltZeta,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'euler_brick'                    : RPNOperator( makeEulerBrick,
                                                    3, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger,
                                                    RPNArgumentType.PositiveInteger ], [ ] ),

    'euler_phi'                      : RPNOperator( getEulerPhi,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'factor'                         : RPNOperator( getFactors,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'factorial'                      : RPNOperator( getNthFactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'fibonacci'                      : RPNOperator( getNthFibonacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'fibonorial'                     : RPNOperator( getNthFibonorial,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'find_sum_of_cubes'              : RPNOperator( findNthSumOfCubes,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'find_sum_of_squares'            : RPNOperator( findNthSumOfSquares,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'fraction'                       : RPNOperator( interpretAsFraction,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.Integer ], [ ] ),

    'gamma'                          : RPNOperator( getGamma,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'generate_polydivisibles'        : RPNOperator( generatePolydivisibles,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'get_base_k_digits'              : RPNOperator( getBaseKDigits,
                                                    2, [ RPNArgumentType.Integer, RPNArgumentType.PositiveInteger ], [ ] ),

    'harmonic'                       : RPNOperator( getHarmonic,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'heptanacci'                     : RPNOperator( getNthHeptanacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hexanacci'                      : RPNOperator( getNthHexanacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hurwitz_zeta'                   : RPNOperator( getHurwitzZeta,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'hyperfactorial'                 : RPNOperator( getNthHyperfactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_abundant'                    : RPNOperator( isAbundant,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_achilles'                    : RPNOperator( isAchillesNumber,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_carmichael'                  : RPNOperator( isCarmichaelNumberOperator,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_composite'                   : RPNOperator( isComposite,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_deficient'                   : RPNOperator( isDeficient,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    # is_friendly

    'is_k_hyperperfect'              : RPNOperator( isKHyperperfect,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_k_semiprime'                 : RPNOperator( isKSemiPrimeOperator,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_k_sphenic'                   : RPNOperator( isKSphenicOperator,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'is_perfect'                     : RPNOperator( isPerfect,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_polydivisible'               : RPNOperator( isPolydivisible,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_powerful'                    : RPNOperator( isPowerful,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_prime'                       : RPNOperator( isPrime,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_pronic'                      : RPNOperator( isPronic,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_rough'                       : RPNOperator( isRoughOperator,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PrimeInteger ], [ ] ),

    'is_ruth_aaron'                  : RPNOperator( isRuthAaronNumber,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_semiprime'                   : RPNOperator( isSemiPrime,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_smooth'                      : RPNOperator( isSmoothOperator,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PrimeInteger ], [ ] ),

    'is_sphenic'                     : RPNOperator( isSphenic,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_squarefree'                  : RPNOperator( isSquareFree,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_strong_pseudoprime'          : RPNOperator( isStrongPseudoprime,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.NonnegativeInteger ], [ ] ),

    'is_unusual'                     : RPNOperator( isUnusual,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'k_fibonacci'                    : RPNOperator( getNthKFibonacciNumber,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'leyland'                        : RPNOperator( getLeyland,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.Real ], [ ] ),

    'log_gamma'                      : RPNOperator( getLogGamma,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'lucas'                          : RPNOperator( getNthLucasNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'make_cf'                        : RPNOperator( makeContinuedFraction,
                                                    2, [ RPNArgumentType.Real, RPNArgumentType.PositiveInteger ], [ ] ),

    'make_pyth_3'                    : RPNOperator( makePythagoreanTriple,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'make_pyth_4'                    : RPNOperator( makePythagoreanQuadruple,
                                                    2, [ RPNArgumentType.NonnegativeReal, RPNArgumentType.NonnegativeReal ], [ ] ),

    'merten'                         : RPNOperator( getNthMerten,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'mobius'                         : RPNOperator( getMobius,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_carol'                      : RPNOperator( getNthCarolNumber,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'nth_jacobsthal'                 : RPNOperator( getNthJacobsthalNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_kynea'                      : RPNOperator( getNthKyneaNumber,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'nth_leonardo'                   : RPNOperator( getNthLeonardoNumber,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'nth_mersenne_exponent'          : RPNOperator( getNthMersenneExponent,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_mersenne_prime'             : RPNOperator( getNthMersennePrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_padovan'                    : RPNOperator( getNthPadovanNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_perfect_number'             : RPNOperator( getNthPerfectNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_stern'                      : RPNOperator( getNthStern,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_thue_morse'                 : RPNOperator( getNthThueMorse,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'octanacci'                      : RPNOperator( getNthOctanacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pascal_triangle'                : RPNOperator( getNthPascalLine,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'pentanacci'                     : RPNOperator( getNthPentanacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'polygamma'                      : RPNOperator( getPolygamma,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.Default ], [ ] ),

    'radical'                        : RPNOperator( getRadical,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'repunit'                        : RPNOperator( getNthBaseKRepunit,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'reversal_addition'              : RPNOperator( getNthReversalAddition,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'riesel'                         : RPNOperator( getNthRieselNumber,
                                                    1, [ RPNArgumentType.Real ], [ ] ),

    'sigma'                          : RPNOperator( getSigmaOperator,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'sigma_k'                        : RPNOperator( getSigmaK,
                                                    2, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'subfactorial'                   : RPNOperator( getNthSubfactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'sums_of_k_powers'               : RPNOperator( findSumsOfKPowers,
                                                    3, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'sums_of_k_nonzero_powers'       : RPNOperator( findSumsOfKNonzeroPowers,
                                                    3, [ RPNArgumentType.NonnegativeInteger, RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'superfactorial'                 : RPNOperator( getNthSuperfactorial,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'tetranacci'                     : RPNOperator( getNthTetranacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'thabit'                         : RPNOperator( getNthThabitNumber,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'tribonacci'                     : RPNOperator( getNthTribonacci,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'trigamma'                       : RPNOperator( getTrigamma,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'unit_roots'                     : RPNOperator( getUnitRoots,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'zeta'                           : RPNOperator( getZeta,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'zeta_zero'                      : RPNOperator( getNthZetaZero,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    # physics
    'acceleration'                   : RPNOperator( calculateAcceleration,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'black_hole_entropy'             : RPNOperator( calculateBlackHoleEntropy,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_lifetime'            : RPNOperator( calculateBlackHoleLifetime,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_luminosity'          : RPNOperator( calculateBlackHoleLuminosity,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_mass'                : RPNOperator( calculateBlackHoleMass,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_radius'              : RPNOperator( calculateBlackHoleRadius,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_temperature'         : RPNOperator( calculateBlackHoleTemperature,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_surface_area'        : RPNOperator( calculateBlackHoleSurfaceArea,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'black_hole_surface_gravity'     : RPNOperator( calculateBlackHoleSurfaceGravity,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'distance'                       : RPNOperator( calculateDistance,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'energy_equivalence'             : RPNOperator( calculateEnergyEquivalence,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'escape_velocity'                : RPNOperator( calculateEscapeVelocity,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'horizon_distance'               : RPNOperator( lambda n: calculateHorizonDistance( n, constants[ 'earth_radius' ].function( ) ),
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'kinetic_energy'                 : RPNOperator( calculateKineticEnergy,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'mass_equivalence'               : RPNOperator( calculateMassEquivalence,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'orbital_mass'                   : RPNOperator( calculateOrbitalMass,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'orbital_period'                 : RPNOperator( calculateOrbitalPeriod,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'orbital_radius'                 : RPNOperator( calculateOrbitalRadius,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'orbital_velocity'               : RPNOperator( calculateOrbitalVelocity,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'surface_gravity'                : RPNOperator( calculateSurfaceGravity,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'time_dilation'                  : RPNOperator( calculateTimeDilation,
                                                    1, [ RPNArgumentType.Measurement ], [ ] ),

    'velocity'                       : RPNOperator( calculateVelocity,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    'wind_chill'                     : RPNOperator( calculateWindChill,
                                                    2, [ RPNArgumentType.Measurement, RPNArgumentType.Measurement ], [ ] ),

    # powers_and_roots
    'agm'                            : RPNOperator( getAGM,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ] ),

    'cube'                           : RPNOperator( cube,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'cube_root'                      : RPNOperator( getCubeRoot,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'exp'                            : RPNOperator( getExp,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'exp10'                          : RPNOperator( getExp10,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'expphi'                         : RPNOperator( getExpPhi,
                                                    1, [ RPNArgumentType.Default ], [ ] ),

    'hyper4_2'                       : RPNOperator( tetrateLarge,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Real ], [ ] ),

    'power'                          : RPNOperator( getPower,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'powmod'                         : RPNOperator( getPowModOperator,
                                                    3, [ RPNArgumentType.Integer, RPNArgumentType.Integer,
                                                         RPNArgumentType.Integer ], [ ] ),

    'root'                           : RPNOperator( getRoot,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Real ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'square'                         : RPNOperator( square,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'square_root'                    : RPNOperator( getSquareRoot,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'tetrate'                        : RPNOperator( tetrate,
                                                    2, [ RPNArgumentType.Default, RPNArgumentType.Real ], [ ] ),

    # prime_number
    'balanced_prime'                 : RPNOperator( getNthBalancedPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'balanced_prime_'                : RPNOperator( getNthBalancedPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'cousin_prime'                   : RPNOperator( getNthCousinPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'cousin_prime_'                  : RPNOperator( getNthCousinPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'double_balanced'                : RPNOperator( getNthDoubleBalancedPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'double_balanced_'               : RPNOperator( getNthDoubleBalancedPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'isolated_prime'                 : RPNOperator( getNthIsolatedPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'next_prime'                     : RPNOperator( getNextPrimeOperator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'next_primes'                    : RPNOperator( getNextPrimesOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'next_quadruplet_prime'          : RPNOperator( getNextQuadrupletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'next_quintuplet_prime'          : RPNOperator( getNextQuintupletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_prime'                      : RPNOperator( findPrimeOperator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_quadruplet_prime'           : RPNOperator( findQuadrupletPrimeOperator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'nth_quintuplet_prime'           : RPNOperator( findQuintupletPrimeOperator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'polyprime'                      : RPNOperator( getNthPolyPrime,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'previous_prime'                 : RPNOperator( getPreviousPrimeOperator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'previous_primes'                : RPNOperator( getPreviousPrimesOperator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'prime'                          : RPNOperator( getNthPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'primes'                         : RPNOperator( getPrimesGenerator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'prime_pi'                       : RPNOperator( getPrimePi,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'prime_range'                    : RPNOperator( getPrimeRange,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'primorial'                      : RPNOperator( getNthPrimorial,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'quadruplet_prime'               : RPNOperator( getNthQuadrupletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'quadruplet_prime_'              : RPNOperator( getNthQuadrupletPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'quintuplet_prime'               : RPNOperator( getNthQuintupletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'quintuplet_prime_'              : RPNOperator( getNthQuintupletPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'safe_prime'                     : RPNOperator( getSafePrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sextuplet_prime'                : RPNOperator( getNthSextupletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sextuplet_prime_'               : RPNOperator( getNthSextupletPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_prime'                     : RPNOperator( getNthSexyPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_prime_'                    : RPNOperator( getNthSexyPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_quadruplet'                : RPNOperator( getNthSexyQuadruplet,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_quadruplet_'               : RPNOperator( getNthSexyQuadrupletList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_triplet'                   : RPNOperator( getNthSexyTriplet,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sexy_triplet_'                  : RPNOperator( getNthSexyTripletList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'sophie_prime'                   : RPNOperator( getNthSophiePrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'superprime'                     : RPNOperator( getNthSuperPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'triplet_prime'                  : RPNOperator( getNthTripletPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'triplet_prime_'                 : RPNOperator( getNthTripletPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'triple_balanced'                : RPNOperator( getNthTripleBalancedPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'triple_balanced_'               : RPNOperator( getNthTripleBalancedPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'twin_prime'                     : RPNOperator( getNthTwinPrime,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'twin_prime_'                    : RPNOperator( getNthTwinPrimeList,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    # settings
    'accuracy'                       : RPNOperator( lambda n: setAccuracy( fadd( n, 2 ) ),
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'comma'                          : RPNOperator( setComma,
                                                    1, [ RPNArgumentType.Boolean ], [ ] ),

    'comma_mode'                     : RPNOperator( setCommaMode,
                                                    0, [ ], [ ] ),

    'decimal_grouping'               : RPNOperator( setDecimalGrouping,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'hex_mode'                       : RPNOperator( setHexMode,
                                                    0, [ ], [ ] ),

    'identify'                       : RPNOperator( setIdentify,
                                                    1, [ RPNArgumentType.Boolean ], [ ] ),

    'identify_mode'                  : RPNOperator( setIdentifyMode,
                                                    0, [ ], [ ] ),

    'input_radix'                    : RPNOperator( setInputRadix,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'integer_grouping'               : RPNOperator( setIntegerGrouping,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'leading_zero'                   : RPNOperator( setLeadingZero,
                                                    1, [ RPNArgumentType.Boolean ], [ ] ),

    'leading_zero_mode'              : RPNOperator( setLeadingZeroMode,
                                                    0, [ ], [ ] ),

    'octal_mode'                     : RPNOperator( setOctalMode,
                                                    0, [ ], [ ] ),

    'output_radix'                   : RPNOperator( setOutputRadix,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'precision'                      : RPNOperator( setPrecision,
                                                    1, [ RPNArgumentType.NonnegativeInteger ], [ ] ),

    'timer'                          : RPNOperator( setTimer,
                                                    1, [ RPNArgumentType.Boolean ], [ ] ),

    'timer_mode'                     : RPNOperator( setTimerMode,
                                                    0, [ ], [ ] ),

    # special
    'base_units'                     : RPNOperator( convertToBaseUnits,
                                                    1, [ RPNArgumentType.Measurement ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'delete_config'                  : RPNOperator( deleteUserConfiguration,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'describe'                       : RPNOperator( describeInteger,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'dimensions'                     : RPNOperator( getDimensions,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'dump_config'                    : RPNOperator( dumpUserConfiguration,
                                                    0, [ ], [ ] ),

    'enumerate_dice'                 : RPNOperator( enumerateDiceGenerator,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'enumerate_dice_'                : RPNOperator( enumerateMultipleDiceGenerator,
                                                    2, [ RPNArgumentType.String, RPNArgumentType.PositiveInteger ], [ ] ),

    'estimate'                       : RPNOperator( estimate,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'help'                           : RPNOperator( printHelpMessage,
                                                    0, [ ], [ ] ),

    'get_config'                     : RPNOperator( getUserConfiguration,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'get_variable'                   : RPNOperator( getUserVariable,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'if'                             : RPNOperator( lambda a, b, c: a if c else b,
                                                    3, [ RPNArgumentType.Default, RPNArgumentType.Default, RPNArgumentType.Integer ], [ ] ),

    'list_from_file'                 : RPNOperator( readListFromFile,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'name'                           : RPNOperator( getName,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'oeis'                           : RPNOperator( downloadOEISSequence,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'oeis_comment'                   : RPNOperator( downloadOEISComment,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'oeis_ex'                        : RPNOperator( downloadOEISExtra,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'oeis_name'                      : RPNOperator( downloadOEISName,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'oeis_offset'                    : RPNOperator( downloadOEISOffset,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'ordinal_name'                   : RPNOperator( getOrdinalName,
                                                    1, [ RPNArgumentType.Integer ], [ ] ),

    'result'                         : RPNOperator( loadResult,
                                                    0, [ ], [ ] ),

    'permute_dice'                   : RPNOperator( permuteDiceGenerator,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'random'                         : RPNOperator( getRandomNumber,
                                                    0, [ ], [ ] ),

    'random_'                        : RPNOperator( getMultipleRandomsGenerator,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'random_integer'                 : RPNOperator( getRandomInteger,
                                                    1, [ RPNArgumentType.PositiveInteger ], [ ] ),

    'random_integer_'                : RPNOperator( getRandomIntegersGenerator,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'roll_dice'                      : RPNOperator( rollDice,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'roll_simple_dice'               : RPNOperator( rollSimpleDice,
                                                    2, [ RPNArgumentType.PositiveInteger, RPNArgumentType.PositiveInteger ], [ ] ),

    'roll_dice_'                     : RPNOperator( rollMultipleDiceGenerator,
                                                    2, [ RPNArgumentType.String, RPNArgumentType.PositiveInteger ], [ ] ),

    'set_config'                     : RPNOperator( setUserConfiguration,
                                                    2, [ RPNArgumentType.String, RPNArgumentType.String ], [ ] ),

    'set_variable'                   : RPNOperator( setUserVariable,
                                                    2, [ RPNArgumentType.String, RPNArgumentType.String ], [ ] ),

    'topic'                          : RPNOperator( printHelpTopic,
                                                    1, [ RPNArgumentType.String ], [ ] ),

    'uuid'                           : RPNOperator( generateUUID,
                                                    0, [ ], [ ] ),

    'uuid_random'                    : RPNOperator( generateRandomUUID,
                                                    0, [ ], [ ] ),

    'value'                          : RPNOperator( getValue,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    # trigonometry
    'acos'                           : RPNOperator( get_acos,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'acosh'                          : RPNOperator( get_acosh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'acot'                           : RPNOperator( get_acot,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'acoth'                          : RPNOperator( get_acoth,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'acsc'                           : RPNOperator( get_acsc,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'acsch'                          : RPNOperator( get_acsch,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'asec'                           : RPNOperator( get_asec,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'asech'                          : RPNOperator( get_asech,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'asin'                           : RPNOperator( get_asin,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'asinh'                          : RPNOperator( get_asinh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'atan'                           : RPNOperator( get_atan,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'atanh'                          : RPNOperator( get_atanh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'cos'                            : RPNOperator( get_cos,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'cosh'                           : RPNOperator( get_cosh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'cot'                            : RPNOperator( get_cot,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'coth'                           : RPNOperator( get_coth,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'csc'                            : RPNOperator( get_csc,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'csch'                           : RPNOperator( get_csch,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sec'                            : RPNOperator( get_sec,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sech'                           : RPNOperator( get_sech,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sin'                            : RPNOperator( get_sin,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'sinh'                           : RPNOperator( get_sinh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'tan'                            : RPNOperator( get_tan,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    'tanh'                           : RPNOperator( get_tanh,
                                                    1, [ RPNArgumentType.Default ], [ ],
                                                    RPNOperator.measurementsAllowed ),

    # internal
    '_dump_aliases'                  : RPNOperator( dumpAliases,
                                                    0, [ ], [ ] ),

    '_dump_constants'                : RPNOperator( dumpConstants,
                                                    0, [ ], [ ] ),

    '_dump_conversions'              : RPNOperator( dumpUnitConversions,
                                                    0, [ ], [ ] ),

    '_dump_operators'                : RPNOperator( dumpOperators,
                                                    0, [ ], [ ] ),

    '_dump_units'                    : RPNOperator( dumpUnits,
                                                    0, [ ], [ ] ),

    '_stats'                         : RPNOperator( dumpStats,
                                                    0, [ ], [ ] ),

    #   'antitet'                       : RPNOperator( findTetrahedralNumber, 0 ),
    #   'bernfrac'                      : RPNOperator( bernfrac, 1 ),
}

