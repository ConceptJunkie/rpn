#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnOperators.py
# //
# //  RPN command-line calculator operator definitions
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import struct

from mpmath import *

from random import randrange

from rpnCombinatorics import *
from rpnComputer import *
from rpnConstants import *
from rpnDate import *
from rpnDeclarations import *
from rpnGeometry import *
from rpnList import *
from rpnMath import *
from rpnModifiers import *
from rpnName import *
from rpnNumberTheory import *
from rpnPolynomials import *
from rpnPolytope import *
from rpnPrimeUtils import *
from rpnUtils import *

from rpnOutput import printHelp


# //******************************************************************************
# //
# //  getCurrentArgList
# //
# //******************************************************************************

def getCurrentArgList( valueList ):
    argList = valueList

    for i in range( 0, g.nestedListLevel ):
        argList = argList[ -1 ]

    return argList


# //******************************************************************************
# //
# //  applyNumberValueToUnit
# //
# //  We have to treat constant units differently because they become plain
# //  numbers.
# //
# //******************************************************************************

def applyNumberValueToUnit( number, term ):
    if g.unitOperators[ term ].unitType == 'constant':
        value = mpf( Measurement( number, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
    else:
        value = Measurement( number, term, g.unitOperators[ term ].representation, g.unitOperators[ term ].plural )

    return value


# //******************************************************************************
# //
# //  abortArgsNeeded
# //
# //******************************************************************************

def abortArgsNeeded( term, index, argsNeeded ):
    print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
           format( argsNeeded ) + ' argument', end='' )

    print( 's' if argsNeeded > 1 else '' )


# //******************************************************************************
# //
# //  evaluateTerm
# //
# //  This looks worse than it is.  It just has to do slightly different things
# //  depending on what kind of term or operator is involved.  Plus, there's a
# //  lot of exception handling.
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

        elif not isList and term in g.unitOperators:
            # handle a unit operator
            # look for unit without a value (in which case we give it a value of 1)
            if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], Measurement ) or \
               isinstance( currentValueList[ -1 ], arrow.Arrow ) or ( isinstance( currentValueList[ -1 ], list ) and
                                                                      isinstance( currentValueList[ -1 ][ 0 ], Measurement ) ):
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

        elif not isList and term in operators:
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

                for i in range( 0, argsNeeded ):
                    arg = currentValueList.pop( )
                    argList.append( arg if isinstance( arg, list ) else [ arg ] )

                result = callers[ argsNeeded ]( operatorInfo.function, *argList )

            newResult = list( )

            for item in result:
                if isinstance( item, Measurement ) and item.getUnits( ) == { }:
                    newResult.append( mpf( item ) )
                else:
                    newResult.append( item )

            if len( newResult ) == 1:
                newResult = newResult[ 0 ]

            if term not in sideEffectOperators:
                currentValueList.append( newResult )
        elif not isList and term in listOperators:
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
# //  handleIdentify
# //
# //******************************************************************************

def handleIdentify( result ):
    formula = identify( result )

    if formula is None:
        base = [ 'pi', 'e', 'euler' ]
        formula = identify( result, base )

    if formula is None:
        print( '    = [formula cannot be found]' )
    else:
        print( '    = ' + formula )


# //******************************************************************************
# //
# //  findPolynomial
# //
# //******************************************************************************

def findPolynomial( n, k ):
    poly = findpoly( n, int( k ) )

    if poly is None:
        poly = findpoly( n, int( k ), tol=1e-10 )

    if poly is None:
        poly = findpoly( n, int( k ), tol=1e-7 )

    if poly is None:
        return [ 0 ]
    else:
        return poly


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

def evaluateFunction( a, b, c, d ):
    #print( 'a, b, c, d', a, b, c, d.valueList )
    if not isinstance( d, FunctionInfo ):
        raise ValueError( '\'eval\' expects a function argument' )

    if isinstance( a, list ) or isinstance( b, list ) or isinstance( c, list ):
        result = [ ]

        for item in a:
            result.append( k.evaluate( item ) )

        return result
    else:
        valueList = [ ]

        for index, item in enumerate( d.valueList ):
            if index < d.startingIndex:
                continue

            #print( 'item', item )

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
            #print( valueList )
            #print( len( valueList ) )
            listLength = len( valueList )

            term = valueList.pop( 0 )

            if not isinstance( term, list ) and term in g.operatorAliases:
                term = g.operatorAliases[ term ]

            g.creatingFunction = False

            try:
                if not evaluateTerm( term, index, valueList ):
                    break
            except:
                return 0

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
    plot( lambda x: evaluateFunction1( x, func ), [ start , end ] )
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
# //  filterList
# //
# //******************************************************************************

def filterList( n, k ) :
    if not isinstance( n, list ):
        n = [ n ]

    if not isinstance( k, FunctionInfo ):
        raise ValueError( '\'filter\' expects a function argument' )

    result = [ ]

    for item in n:
        value = evaluateFunction( item, 0, 0, k )

        if value != 0:
            result.append( item )

    return result


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
           points=10000 )
    return 0


# //******************************************************************************
# //
# //  loadResult
# //
# //******************************************************************************

def loadResult( valueList ):
    try:
        fileName = g.dataPath + os.sep + 'result.pckl.bz2'

        with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError:
        result = mapmathify( 0 )

    return result


# //******************************************************************************
# //
# //  saveResult
# //
# //******************************************************************************

def saveResult( result ):
    if not os.path.isdir( g.dataPath ):
        os.makedirs( g,dataPath )

    fileName = g.dataPath + os.sep + 'result.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( result, pickleFile )


# //******************************************************************************
# //
# //  dumpOperators
# //
# //******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )

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
# //  dumpAliases
# //
# //******************************************************************************

def dumpAliases( ):
    for alias in sorted( [ key for key in g.operatorAliases ] ):
        print( alias, g.operatorAliases[ alias ] )

    return len( g.operatorAliases )


# //******************************************************************************
# //
# //  printStats
# //
# //******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:13,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


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
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( g.dataPath ), 'small primes' )
    printStats( loadLargePrimes( g.dataPath ), 'large primes' )
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
# //  setAccuracy
# //
# //******************************************************************************

def setAccuracy( n ):
    if n == -1:
        g.outputAccuracy = g.defaultOutputAccuracy
    else:
        g.outputAccuracy = int( n )

    if mp.dps < g.outputAccuracy + 2:
        mp.dps = g.outputAccuracy + 2

    return g.outputAccuracy


# //******************************************************************************
# //
# //  setPrecision
# //
# //******************************************************************************

def setPrecision( n ):
    if n == -1:
        mp.dps = g.defaultPrecision
    else:
        mp.dps = int( n )

    if mp.dps < g.outputAccuracy + 2:
        mp.dps = g.outputAccuracy + 2

    return mp.dps


# //******************************************************************************
# //
# //  setComma
# //
# //******************************************************************************

def setComma( n ):
    if n == 1:
        g.comma = True
    else:
        g.comma = False

    return 1 if g.comma else 0


# //******************************************************************************
# //
# //  setTimer
# //
# //******************************************************************************

def setTimer( n ):
    if n == 1:
        g.timer = True
    else:
        g.timer = False

    return 1 if g.timer else 0


# //******************************************************************************
# //
# //  setIntegerGrouping
# //
# //******************************************************************************

def setIntegerGrouping( n ):
    if n == -1:
        g.integerGrouping = g.defaultIntegerGrouping
    else:
        g.integerGrouping = int( n )

    return g.integerGrouping


# //******************************************************************************
# //
# //  setDecimalGrouping
# //
# //******************************************************************************

def setDecimalGrouping( n ):
    if n == -1:
        g.decimalGrouping = g.defaultDecimalGrouping
    else:
        g.decimalGrouping = int( n )

    return g.decimalGrouping


# //******************************************************************************
# //
# //  setInputRadix
# //
# //******************************************************************************

def setInputRadix( n ):
    if ( n == 0 ) or ( n == -1 ):
        g.inputRadix = g.defaultInputRadix
    else:
        g.inputRadix = int( n )

    return g.inputRadix


# //******************************************************************************
# //
# //  setOutputRadix
# //
# //******************************************************************************

def setOutputRadix( n ):
    if ( n == 0 ) or ( n == -1 ):
        g.outputRadix = g.defaultOutputRadix
    else:
        g.outputRadix = int( n )

    return g.outputRadix


# //******************************************************************************
# //
# //  setLeadingZero
# //
# //******************************************************************************

def setLeadingZero( n ):
    result = 1 if g.leadingZero else 0

    if ( n == 0 ):
        g.leadingZero = False
    else:
        g.leadingZero = True

    return result


# //******************************************************************************
# //
# //  setIdentify
# //
# //******************************************************************************

def setIdentify( n ):
    result = 1 if g.identify else 0

    if ( n == 0 ):
        g.identify = False
    else:
        g.identify = True

    return result


# //******************************************************************************
# //
# //  setVariable
# //
# //  set variable n with value k
# //
# //******************************************************************************

def setVariable( n, k ):
    if isinstance( n, str ):
        g.variables[ n ] = k
    else:
        raise ValueError( 'variable name expected' )

    return k


# //******************************************************************************
# //
# //  printHelpMessage
# //
# //******************************************************************************

def printHelpMessage( ):
    printHelp( operators, listOperators, modifiers, '', True )
    return 0


# //******************************************************************************
# //
# //  printHelpTopic
# //
# //******************************************************************************

def printHelpTopic( n ):
    if isinstance( n, str ):
        printHelp( operators, listOperators, modifiers, n, True )
    elif isinstance( n, Measurement ):
        units = n.getUnits( )
        # help for units isn't implemented yet, but now it will work
        printHelp( operators, listOperators, modifiers, list( units.keys( ) )[ 0 ], True )
    else:
        print( 'The \'topic\' operator requires a string argument.' )

    return 0



# //******************************************************************************
# //
# //  setHexMode
# //
# //******************************************************************************

def setHexMode( ):
    g.tempHexMode = True
    return 0


# //******************************************************************************
# //
# //  setOctalMode
# //
# //******************************************************************************

def setOctalMode( ):
    g.tempOctalMode = True
    return 0


# //******************************************************************************
# //
# //  setCommaMode
# //
# //******************************************************************************

def setCommaMode( ):
    g.tempCommaMode = True
    return 0


# //******************************************************************************
# //
# //  setTimerMode
# //
# //******************************************************************************

def setTimerMode( ):
    g.tempTimerMode = True
    return 0


# //******************************************************************************
# //
# //  setLeadingZeroMode
# //
# //******************************************************************************

def setLeadingZeroMode( ):
    g.tempLeadingZeroMode = True
    return 0


# //******************************************************************************
# //
# //  setIdentifyMode
# //
# //******************************************************************************

def setIdentifyMode( ):
    g.tempIdentifyMode = True
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
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plotc',
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
# //  modifiers are operators that directly modify the argument stack instead of
# //  just returning a value.
# //
# //  '[' and ']' are special arguments that change global state in order to
# //  create list operands.
# //
# //******************************************************************************

modifiers = {
    'dup'               : OperatorInfo( duplicateTerm, 2 ),
    'flatten'           : OperatorInfo( flatten, 1 ),
    'previous'          : OperatorInfo( getPrevious, 1 ),
    'unlist'            : OperatorInfo( unlist, 1 ),
    'x'                 : OperatorInfo( createXFunction, 0 ),
    'y'                 : OperatorInfo( createYFunction, 0 ),
    'z'                 : OperatorInfo( createZFunction, 0 ),
    '['                 : OperatorInfo( incrementNestedListLevel, 0 ),
    ']'                 : OperatorInfo( decrementNestedListLevel, 0 ),
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
    'altsign'           : OperatorInfo( alternateSigns, 1 ),
    'altsign2'          : OperatorInfo( alternateSigns2, 1 ),
    'altsum'            : OperatorInfo( getAlternatingSum, 1 ),
    'altsum2'           : OperatorInfo( getAlternatingSum2, 1 ),
    'append'            : OperatorInfo( appendLists, 2 ),
    'base'              : OperatorInfo( interpretAsBase, 2 ),
    'calendar'          : OperatorInfo( generateMonthCalendar, 1 ),
    'cf'                : OperatorInfo( convertFromContinuedFraction, 1 ),
    'convert'           : OperatorInfo( convertUnits, 2 ),
    'count'             : OperatorInfo( countElements, 1 ),
    'diffs'             : OperatorInfo( getListDiffs, 1 ),
    'diffs2'            : OperatorInfo( getListDiffsFromFirst, 1 ),
    'filter'            : OperatorInfo( filterList, 2 ),
    'gcd'               : OperatorInfo( getGCD, 1 ),
    'geomean'           : OperatorInfo( calculateGeometricMean, 1 ),
    'interleave'        : OperatorInfo( interleave, 2 ),
    'intersection'      : OperatorInfo( makeIntersection, 2 ),
    'linearrecur'       : OperatorInfo( getNthLinearRecurrence, 3 ),
    'makeisotime'       : OperatorInfo( makeISOTime, 1 ),
    'makejuliantime'    : OperatorInfo( makeJulianTime, 1 ),
    'maketime'          : OperatorInfo( makeTime, 1 ),
    'max'               : OperatorInfo( max, 1 ),
    'maxindex'          : OperatorInfo( getIndexOfMax, 1 ),
    'mean'              : OperatorInfo( lambda n: fdiv( fsum( n ), len( n ) ), 1 ),
    'min'               : OperatorInfo( min, 1 ),
    'minindex'          : OperatorInfo( getIndexOfMin, 1 ),
    'nonzero'           : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e != 0 ], 1 ),
    'pack'              : OperatorInfo( packInteger, 2 ),
    'polyadd'           : OperatorInfo( addPolynomials, 2 ),
    'polymul'           : OperatorInfo( multiplyPolynomials, 2 ),
    'polyprod'          : OperatorInfo( multiplyListOfPolynomials, 1 ),
    'polysum'           : OperatorInfo( addListOfPolynomials, 1 ),
    'polyval'           : OperatorInfo( evaluatePolynomial, 2 ),
    'product'           : OperatorInfo( getProduct, 1 ),
    'ratios'            : OperatorInfo( getListRatios, 1 ),
    'reduce'            : OperatorInfo( reduceList, 1 ),
    'result'            : OperatorInfo( loadResult, 0 ),
    'reverse'           : OperatorInfo( getReverse, 1 ),
    'solve'             : OperatorInfo( solvePolynomial, 1 ),
    'sort'              : OperatorInfo( sortAscending, 1 ),
    'sortdesc'          : OperatorInfo( sortDescending, 1 ),
    'stddev'            : OperatorInfo( getStandardDeviation, 1 ),
    'sum'               : OperatorInfo( getSum, 1 ),
    'tower'             : OperatorInfo( calculatePowerTower, 1 ),
    'tower2'            : OperatorInfo( calculatePowerTower2, 1 ),
    'union'             : OperatorInfo( makeUnion, 2 ),
    'unique'            : OperatorInfo( getUniqueElements, 1 ),
    'unpack'            : OperatorInfo( unpackInteger, 2 ),
    'zero'              : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e == 0 ], 1 ),
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
    'abs'               : OperatorInfo( fabs, 1 ),
    'accuracy'          : OperatorInfo( setAccuracy, 1 ),
    'acos'              : OperatorInfo( lambda n: performTrigOperation( n, acos ), 1 ),
    'acosh'             : OperatorInfo( lambda n: performTrigOperation( n, acosh ), 1 ),
    'acot'              : OperatorInfo( lambda n: performTrigOperation( n, acot ), 1 ),
    'acoth'             : OperatorInfo( lambda n: performTrigOperation( n, acoth ), 1 ),
    'acsc'              : OperatorInfo( lambda n: performTrigOperation( n, acsc ), 1 ),
    'acsch'             : OperatorInfo( lambda n: performTrigOperation( n, acsch ), 1 ),
    'add'               : OperatorInfo( add, 2, ),
    'altfac'            : OperatorInfo( getNthAlternatingFactorial, 1 ),
    'and'               : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x & y ), 2 ),
    'apery'             : OperatorInfo( apery, 0 ),
    'aperynum'          : OperatorInfo( getNthAperyNumber, 1 ),
    'april'             : OperatorInfo( lambda: 4, 0 ),
    'argument'          : OperatorInfo( arg, 1 ),
    'asec'              : OperatorInfo( lambda n: performTrigOperation( n, asec ), 1 ),
    'asech'             : OperatorInfo( lambda n: performTrigOperation( n, asech ), 1 ),
    'ash_wednesday'     : OperatorInfo( calculateAshWednesday, 1 ),
    'asin'              : OperatorInfo( lambda n: performTrigOperation( n, asin ), 1 ),
    'asinh'             : OperatorInfo( lambda n: performTrigOperation( n, asinh ), 1 ),
    'atan'              : OperatorInfo( lambda n: performTrigOperation( n, atan ), 1 ),
    'atanh'             : OperatorInfo( lambda n: performTrigOperation( n, atanh ), 1 ),
    'august'            : OperatorInfo( lambda: 8, 0 ),
    'avogadro'          : OperatorInfo( getAvogadrosNumber, 0 ),
    'balanced'          : OperatorInfo( getNthBalancedPrime, 1 ),
    'balanced_'         : OperatorInfo( getNthBalancedPrimeList, 1 ),
    'bell'              : OperatorInfo( bell, 1 ),
    'bellpoly'          : OperatorInfo( bell, 2 ),
    'bernoulli'         : OperatorInfo( bernoulli, 1 ),
    'binomial'          : OperatorInfo( binomial, 2 ),
    'carol'             : OperatorInfo( lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1 ),
    'catalan'           : OperatorInfo( lambda n: fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) ), 1 ),
    'catalans'          : OperatorInfo( catalan, 0 ),
    'cdecagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 10 ), 1 ),
    'cdecagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 10 ), 1 ),
    'ceiling'           : OperatorInfo( ceil, 1 ),
    'centeredcube'      : OperatorInfo( getNthCenteredCubeNumber, 1 ),
    'champernowne'      : OperatorInfo( getChampernowneConstant, 0 ),
    'char'              : OperatorInfo( lambda n: convertToSignedInt( n , 8 ), 1 ),
    'cheptagonal'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 7 ), 1 ),
    'cheptagonal?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 7 ), 1 ),
    'chexagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 6 ), 1 ),
    'cnonagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 9 ), 1 ),
    'cnonagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 9 ), 1 ),
    'coctagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 8 ), 1 ),
    'coctagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 8 ), 1 ),
    'comma'             : OperatorInfo( setComma, 1 ),
    'comma_mode'        : OperatorInfo( setCommaMode, 0 ),
    'conjugate'         : OperatorInfo( conj, 1 ),
    'copeland'          : OperatorInfo( getCopelandErdosConstant, 0 ),
    'cos'               : OperatorInfo( lambda n: performTrigOperation( n, cos ), 1 ),
    'cosh'              : OperatorInfo( lambda n: performTrigOperation( n, cosh ), 1 ),
    'cot'               : OperatorInfo( lambda n: performTrigOperation( n, cot ), 1 ),
    'coth'              : OperatorInfo( lambda n: performTrigOperation( n, coth ), 1 ),
    'countbits'         : OperatorInfo( getBitCount, 1 ),
    'countdiv'          : OperatorInfo( getDivisorCount, 1 ),
    'cousinprime'       : OperatorInfo( getNthCousinPrime, 1 ),
    'cpentagonal'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 5 ), 1 ),
    'cpentagonal?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 5 ), 1 ),
    'cpolygonal'        : OperatorInfo( lambda n, k: getCenteredPolygonalNumber( n, k ), 2 ),
    'cpolygonal?'       : OperatorInfo( lambda n, k: findCenteredPolygonalNumber( n, k ), 2 ),
    'csc'               : OperatorInfo( lambda n: performTrigOperation( n, csc ), 1 ),
    'csch'              : OperatorInfo( lambda n: performTrigOperation( n, csch ), 1 ),
    'csquare'           : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 4 ), 1 ),
    'csquare?'          : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 4 ), 1 ),
    'ctriangular'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 3 ), 1 ),
    'ctriangular?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 3 ), 1 ),
    'cube'              : OperatorInfo( lambda n: exponentiate( n, 3 ), 1 ),
    'debruijn'          : OperatorInfo( createDeBruijnSequence, 2 ),
    'decagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 10 ), 1 ),
    'decagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 10 ), 1 ),
    'december'          : OperatorInfo( lambda: 12, 0 ),
    'decimal_grouping'  : OperatorInfo( setDecimalGrouping, 1 ),
    'default'           : OperatorInfo( lambda: -1, 0 ),
    'delannoy'          : OperatorInfo( getNthDelannoyNumber, 1 ),
    'dhms'              : OperatorInfo( convertToDHMS, 1 ),
    'divide'            : OperatorInfo( divide, 2 ),
    'divisors'          : OperatorInfo( getDivisors, 1 ),
    'dms'               : OperatorInfo( convertToDMS, 1 ),
    'dodecahedral'      : OperatorInfo( lambda n : polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], n ), 1 ),
    'double'            : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( n ) ) ) ), 1 ),
    'doublebal'         : OperatorInfo( getNthDoubleBalancedPrime, 1 ),
    'doublebal_'        : OperatorInfo( getNthDoubleBalancedPrimeList, 1 ),
    'doublefac'         : OperatorInfo( fac2, 1 ),
    'dst_end'           : OperatorInfo( calculateDSTEnd, 1 ),
    'dst_start'         : OperatorInfo( calculateDSTStart, 1 ),
    'e'                 : OperatorInfo( e, 0 ),
    'easter'            : OperatorInfo( calculateEaster, 1 ),
    'egypt'             : OperatorInfo( getGreedyEgyptianFraction, 2 ),
    'election_day'      : OperatorInfo( calculateElectionDay, 1 ),
    'element'           : OperatorInfo( getListElement, 2 ),
    'equal'             : OperatorInfo( isEqual, 2 ),
    'estimate'          : OperatorInfo( estimate, 1 ),
    'euler'             : OperatorInfo( euler, 0 ),
    'eulerbrick'        : OperatorInfo( makeEulerBrick, 3 ),
    'eval'              : OperatorInfo( evaluateFunction1, 2 ),
    'eval2'             : OperatorInfo( evaluateFunction2, 3 ),
    'eval3'             : OperatorInfo( evaluateFunction3, 4 ),
    'exp'               : OperatorInfo( exp, 1 ),
    'exp10'             : OperatorInfo( lambda n: power( 10, n ), 1 ),
    'expphi'            : OperatorInfo( lambda n: power( phi, n ), 1 ),
    'exprange'          : OperatorInfo( expandExponentialRange, 3 ),
    'factor'            : OperatorInfo( lambda i: getExpandedFactorList( factor( i ) ), 1 ),
    'factorial'         : OperatorInfo( fac, 1 ),
    'false'             : OperatorInfo( lambda: 0, 0 ),
    'february'          : OperatorInfo( lambda: 2, 0 ),
    'fibonacci'         : OperatorInfo( fib, 1 ),
    'fibonorial'        : OperatorInfo( getNthFibonorial, 1 ),
    'find_poly'         : OperatorInfo( findPolynomial, 2 ),
    'float'             : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( n ) ) ) ), 1 ),
    'floor'             : OperatorInfo( floor, 1 ),
    'fraction'          : OperatorInfo( interpretAsFraction, 2 ),
    'friday'            : OperatorInfo( lambda: 5, 0 ),
    'fromunixtime'      : OperatorInfo( lambda n: arrow.get( n ), 1 ),
    'gamma'             : OperatorInfo( gamma, 1 ),
    'georange'          : OperatorInfo( expandGeometricRange, 3 ),
    'glaisher'          : OperatorInfo( glaisher, 0 ),
    'greater'           : OperatorInfo( isGreater, 2 ),
    'harmonic'          : OperatorInfo( harmonic, 1 ),
    'help'              : OperatorInfo( printHelpMessage, 0 ),
    'heptagonal'        : OperatorInfo( lambda n: getNthPolygonalNumber( n, 7 ), 1 ),
    'heptagonal?'       : OperatorInfo( lambda n: findNthPolygonalNumber( n, 7 ), 1 ),
    'heptanacci'        : OperatorInfo( getNthHeptanacci, 1 ),
    'hepthex'           : OperatorInfo( getNthHeptagonalHexagonalNumber, 1 ),
    'heptpent'          : OperatorInfo( getNthHeptagonalPentagonalNumber, 1 ),
    'heptsquare'        : OperatorInfo( getNthHeptagonalSquareNumber, 1 ),
    'hepttri'           : OperatorInfo( getNthHeptagonalTriangularNumber, 1 ),
    'hexagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 6 ), 1 ),
    'hexagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 6 ), 1 ),
    'hexanacci'         : OperatorInfo( getNthHexanacci, 1 ),
    'hexpent'           : OperatorInfo( getNthHexagonalPentagonalNumber, 1 ),
    'hex_mode'          : OperatorInfo( setHexMode, 0 ),
    'hms'               : OperatorInfo( convertToHMS, 1 ),
    'hyper4_2'          : OperatorInfo( tetrateLarge, 2 ),
    'hyperfac'          : OperatorInfo( hyperfac, 1 ),
    'hypot'             : OperatorInfo( hypot, 2 ),
    'i'                 : OperatorInfo( lambda n: mpc( real='0.0', imag=n ), 1 ),
    'icosahedral'       : OperatorInfo( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], n ), 1 ),
    'identify'          : OperatorInfo( setIdentify, 1 ),
    'identify_mode'     : OperatorInfo( setIdentifyMode, 0 ),
    'imaginary'         : OperatorInfo( im, 1 ),
    'infinity'          : OperatorInfo( lambda: inf, 0 ),
    'input_radix'       : OperatorInfo( setInputRadix, 1 ),
    'integer'           : OperatorInfo( convertToSignedInt, 2 ),
    'integer_grouping'  : OperatorInfo( setIntegerGrouping, 1 ),
    'isdivisible'       : OperatorInfo( lambda n, k: 1 if fmod( n, k ) == 0 else 0, 2 ),
    'isolated'          : OperatorInfo( getNthIsolatedPrime, 1 ),
    'iso_day'           : OperatorInfo( getISODay, 1 ),
    'isprime'           : OperatorInfo( lambda n: 1 if isPrime( n ) else 0, 1 ),
    'issquare'          : OperatorInfo( isSquare, 1 ),
    'itoi'              : OperatorInfo( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'jacobsthal'        : OperatorInfo( getNthJacobsthalNumber, 1 ),
    'january'           : OperatorInfo( lambda: 1, 0 ),
    'julian_day'        : OperatorInfo( getJulianDay, 1 ),
    'july'              : OperatorInfo( lambda: 7, 0 ),
    'june'              : OperatorInfo( lambda: 6, 0 ),
    'khinchin'          : OperatorInfo( khinchin, 0 ),
    'kynea'             : OperatorInfo( lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1 ),
    'labor_day'         : OperatorInfo( calculateLaborDay, 1 ),
    'lah'               : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2 ),
    'lambertw'          : OperatorInfo( lambertw, 1 ),
    'leading_zero'      : OperatorInfo( setLeadingZero, 1 ),
    'leading_zero_mode' : OperatorInfo( setLeadingZeroMode, 0 ),
    'less'              : OperatorInfo( isLess, 2 ),
    'leyland'           : OperatorInfo( lambda x, y : fadd( power( x, y ), power( y, x ) ), 2 ),
    'lgamma'            : OperatorInfo( loggamma, 1 ),
    'li'                : OperatorInfo( li, 1 ),
    'limit'             : OperatorInfo( lambda n, func: limit( lambda x: evaluateFunction1( x, func ), n ), 2 ),
    'limitn'            : OperatorInfo( lambda n, func: limit( lambda x: evaluateFunction1( x, func ), n, direction=-1 ), 2 ),
    'ln'                : OperatorInfo( ln, 1 ),
    'log10'             : OperatorInfo( log10, 1 ),
    'log2'              : OperatorInfo( lambda n: log( n, 2 ), 1 ),
    'logxy'             : OperatorInfo( log, 2 ),
    'long'              : OperatorInfo( lambda n: convertToSignedInt( n , 32 ), 1 ),
    'longlong'          : OperatorInfo( lambda n: convertToSignedInt( n , 64 ), 1 ),
    'lucas'             : OperatorInfo( getNthLucasNumber, 1 ),
    'makecf'            : OperatorInfo( lambda n, k: ContinuedFraction( n, maxterms=k, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2 ),
    'makepyth3'         : OperatorInfo( makePythagoreanTriple, 2 ),
    'makepyth4'         : OperatorInfo( makePythagoreanQuadruple, 2 ),
    'march'             : OperatorInfo( lambda: 3, 0 ),
    'maxchar'           : OperatorInfo( lambda: ( 1 << 7 ) - 1, 0 ),
    'maxdouble'         : OperatorInfo( lambda: interpretAsDouble( mpmathify( 0x7fefffffffffffff ) ), 0 ),
    'maxfloat'          : OperatorInfo( lambda: interpretAsFloat( mpmathify( 0x7f7fffff ) ), 0 ),
    'maxlong'           : OperatorInfo( lambda: ( 1 << 31 ) - 1, 0 ),
    'maxlonglong'       : OperatorInfo( lambda: ( 1 << 63 ) - 1, 0 ),
    'maxquadlong'       : OperatorInfo( lambda: ( 1 << 127 ) - 1, 0 ),
    'maxshort'          : OperatorInfo( lambda: ( 1 << 15 ) - 1, 0 ),
    'maxuchar'          : OperatorInfo( lambda: ( 1 << 8 ) - 1, 0 ),
    'maxulong'          : OperatorInfo( lambda: ( 1 << 32 ) - 1, 0 ),
    'maxulonglong'      : OperatorInfo( lambda: ( 1 << 64 ) - 1, 0 ),
    'maxuquadlong'      : OperatorInfo( lambda: ( 1 << 128 ) - 1, 0 ),
    'maxushort'         : OperatorInfo( lambda: ( 1 << 16 ) - 1, 0 ),
    'may'               : OperatorInfo( lambda: 5, 0 ),
    'memorial_day'      : OperatorInfo( calculateMemorialDay, 1 ),
    'mertens'           : OperatorInfo( mertens, 0 ),
    'mills'             : OperatorInfo( getMillsConstant, 0 ),
    'minchar'           : OperatorInfo( lambda: -( 1 << 7 ), 0 ),
    'mindouble'         : OperatorInfo( lambda: interpretAsDouble( mpmathify( 0x0010000000000000 ) ), 0 ),
    'minfloat'          : OperatorInfo( lambda: interpretAsFloat( mpmathify( 0x00800000 ) ), 0 ),
    'minlong'           : OperatorInfo( lambda: -( 1 << 31 ), 0 ),
    'minlonglong'       : OperatorInfo( lambda: -( 1 << 63 ), 0 ),
    'minquadlong'       : OperatorInfo( lambda: -( 1 << 127 ), 0 ),
    'minshort'          : OperatorInfo( lambda: -( 1 << 15 ), 0 ),
    'minuchar'          : OperatorInfo( lambda: 0, 0 ),
    'minulong'          : OperatorInfo( lambda: 0, 0 ),
    'minulonglong'      : OperatorInfo( lambda: 0, 0 ),
    'not_equal'         : OperatorInfo( isNotEqual, 2 ),
    'not_greater'       : OperatorInfo( isNotGreater, 2 ),
    'not_less'          : OperatorInfo( isNotLess, 2 ),
    'minuquadlong'      : OperatorInfo( lambda: 0, 0 ),
    'minushort'         : OperatorInfo( lambda: 0, 0 ),
    'modulo'            : OperatorInfo( fmod, 2 ),
    'monday'            : OperatorInfo( lambda: 1, 0 ),
    'motzkin'           : OperatorInfo( getNthMotzkinNumber, 1 ),
    'multiply'          : OperatorInfo( multiply, 2 ),
    'name'              : OperatorInfo( getNumberName, 1 ),
    'narayana'          : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2 ),
    'negative'          : OperatorInfo( getNegative, 1 ),
    'negative_infinity' : OperatorInfo( lambda: -inf, 0 ),
    'nint'              : OperatorInfo( nint, 1 ),
    'nonagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 9 ), 1 ),
    'nonagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 9 ), 1 ),
    'nonahept'          : OperatorInfo( getNthNonagonalHeptagonalNumber, 1 ),
    'nonahex'           : OperatorInfo( getNthNonagonalHexagonalNumber, 1 ),
    'nonaoct'           : OperatorInfo( getNthNonagonalOctagonalNumber, 1 ),
    'nonapent'          : OperatorInfo( getNthNonagonalPentagonalNumber, 1 ),
    'nonasquare'        : OperatorInfo( getNthNonagonalSquareNumber, 1 ),
    'nonatri'           : OperatorInfo( getNthNonagonalTriangularNumber, 1 ),
    'not'               : OperatorInfo( getInvertedBits, 1 ),
    'november'          : OperatorInfo( lambda: 11, 0 ),
    'now'               : OperatorInfo( getNow, 0 ),
    'nprod'             : OperatorInfo( lambda start, end, func: nprod( lambda x: evaluateFunction1( x, func ), [ start, end ] ), 3 ),
    'nspherearea'       : OperatorInfo( getNSphereSurfaceArea, 2 ),
    'nsphereradius'     : OperatorInfo( getNSphereRadius, 2 ),
    'nspherevolume'     : OperatorInfo( getNSphereVolume, 2 ),
    'nsum'              : OperatorInfo( lambda start, end, func: nsum( lambda x: evaluateFunction1( x, func ), [ start, end ] ), 3 ),
    'nthprime?'         : OperatorInfo( lambda i: findPrime( i )[ 0 ], 1 ),
    'nthquad?'          : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 0 ], 1 ),
    'nthweekday'        : OperatorInfo( calculateNthWeekdayOfMonth , 4 ),
    'nthweekdayofyear'  : OperatorInfo( calculateNthWeekdayOfYear, 3 ),
    'octagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 8 ), 1 ),
    'octagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 8 ), 1 ),
    'octahedral'        : OperatorInfo( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], n ), 1 ),
    'octal_mode'        : OperatorInfo( setOctalMode, 0 ),
    'octhept'           : OperatorInfo( getNthOctagonalHeptagonalNumber, 1 ),
    'octhex'            : OperatorInfo( getNthOctagonalHexagonalNumber, 1 ),
    'october'           : OperatorInfo( lambda: 10, 0 ),
    'octpent'           : OperatorInfo( getNthOctagonalPentagonalNumber, 1 ),
    'octsquare'         : OperatorInfo( getNthOctagonalSquareNumber, 1 ),
    'octtri'            : OperatorInfo( getNthOctagonalTriangularNumber, 1 ),
    'oeis'              : OperatorInfo( lambda n: downloadOEISSequence( int( n ) ), 1 ),
    'oeiscomment'       : OperatorInfo( lambda n: downloadOEISText( int( n ), 'C', True ), 1 ),
    'oeisex'            : OperatorInfo( lambda n: downloadOEISText( int( n ), 'E', True ), 1 ),
    'oeisname'          : OperatorInfo( lambda n: downloadOEISText( int( n ), 'N', True ), 1 ),
    'omega'             : OperatorInfo( lambda: lambertw( 1 ), 0 ),
    'or'                : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2 ),
    'output_radix'      : OperatorInfo( setOutputRadix, 1 ),
    'padovan'           : OperatorInfo( getNthPadovanNumber, 1 ),
    'parity'            : OperatorInfo( lambda n : getBitCount( n ) & 1, 1 ),
    'pascal'            : OperatorInfo( getNthPascalLine, 1 ),
    'pell'              : OperatorInfo( getNthPellNumber, 1 ),
    'pentagonal'        : OperatorInfo( lambda n: getNthPolygonalNumber( n, 5 ), 1 ),
    'pentagonal?'       : OperatorInfo( lambda n: findNthPolygonalNumber( n, 5 ), 1 ),
    'pentanacci'        : OperatorInfo( getNthPentanacci, 1 ),
    'pentatope'         : OperatorInfo( getNthPentatopeNumber, 1 ),
    'perm'              : OperatorInfo( getPermutations, 2 ),
    'phi'               : OperatorInfo( phi, 0 ),
    'pi'                : OperatorInfo( pi, 0 ),
    'plastic'           : OperatorInfo( getPlasticConstant, 0 ),
    'plot'              : OperatorInfo( plotFunction, 3 ),
    'plot2'             : OperatorInfo( plot2DFunction, 5 ),
    'plotc'             : OperatorInfo( plotComplexFunction, 5 ),
    'polyarea'          : OperatorInfo( getRegularPolygonArea, 1 ),
    'polygamma'         : OperatorInfo( psi, 2 ),
    'polygonal'         : OperatorInfo( getNthPolygonalNumber, 2 ),
    'polygonal?'        : OperatorInfo( findNthPolygonalNumber, 2 ),
    'polylog'           : OperatorInfo( polylog, 2 ),
    'polyprime'         : OperatorInfo( getNthPolyPrime, 2 ),
    'polytope'          : OperatorInfo( getNthPolytopeNumber, 2 ),
    'power'             : OperatorInfo( exponentiate, 2 ),
    'precision'         : OperatorInfo( setPrecision, 1 ),
    'presidents_day'    : OperatorInfo( calculatePresidentsDay, 1 ),
    'prevost'           : OperatorInfo( getPrevostConstant, 0 ),
    'prime'             : OperatorInfo( getNthPrime, 1 ),
    'prime?'            : OperatorInfo( lambda n: findPrime( n )[ 1 ], 1 ),
    'primepi'           : OperatorInfo( getPrimePi, 1 ),
    'primes'            : OperatorInfo( getPrimes, 2 ),
    'primorial'         : OperatorInfo( getPrimorial, 1 ),
    'pyramid'           : OperatorInfo( lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1 ),
    'quadprime'         : OperatorInfo( getNthQuadrupletPrime, 1 ),
    'quadprime?'        : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 1 ], 1 ),
    'quadprime_'        : OperatorInfo( getNthQuadrupletPrimeList, 1 ),
    'quintprime'        : OperatorInfo( getNthQuintupletPrime, 1 ),
    'quintprime_'       : OperatorInfo( getNthQuintupletPrimeList, 1 ),
    'randint'           : OperatorInfo( randrange, 1 ),
    'randint_'          : OperatorInfo( randrange_, 2 ),
    'random'            : OperatorInfo( rand, 0 ),
    'random_'           : OperatorInfo( rand_, 0 ),
    'range'             : OperatorInfo( expandRange, 2 ),
    'range2'            : OperatorInfo( expandSteppedRange, 3 ),
    'real'              : OperatorInfo( re, 1 ),
    'reciprocal'        : OperatorInfo( takeReciprocal, 1 ),
    'repunit'           : OperatorInfo( getNthBaseKRepunit, 2 ),
    'rhombdodec'        : OperatorInfo( getNthRhombicDodecahedralNumber, 1 ),
    'riesel'            : OperatorInfo( lambda n: fsub( fmul( n, power( 2, n ) ), 1 ), 1 ),
    'robbins'           : OperatorInfo( getRobbinsConstant, 0 ),
    'root'              : OperatorInfo( root, 2 ),
    'root2'             : OperatorInfo( sqrt, 1 ),
    'root3'             : OperatorInfo( cbrt, 1 ),
    'round'             : OperatorInfo( lambda n: floor( fadd( n, 0.5 ) ), 1 ),
    'safeprime'         : OperatorInfo( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1 ),
    'saturday'          : OperatorInfo( lambda: 6, 0 ),
    'schroeder'         : OperatorInfo( getNthSchroederNumber, 1 ),
    'sec'               : OperatorInfo( lambda n: performTrigOperation( n, sec ), 1 ),
    'sech'              : OperatorInfo( lambda n: performTrigOperation( n, sech ), 1 ),
    'september'         : OperatorInfo( lambda: 9, 0 ),
    'set'               : OperatorInfo( setVariable, 2 ),
    'sextprime'         : OperatorInfo( getNthSextupletPrime, 1 ),
    'sextprime_'        : OperatorInfo( getNthSextupletPrimeList, 1 ),
    'sexyprime'         : OperatorInfo( getNthSexyPrime, 1 ),
    'sexyprime_'        : OperatorInfo( getNthSexyPrimeList, 1 ),
    'sexyquad'          : OperatorInfo( getNthSexyQuadruplet, 1 ),
    'sexyquad_'         : OperatorInfo( getNthSexyQuadrupletList, 1 ),
    'sexytriplet'       : OperatorInfo( getNthSexyTriplet, 1 ),
    'sexytriplet_'      : OperatorInfo( getNthSexyTripletList, 1 ),
    'shiftleft'         : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2 ),
    'shiftright'        : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2 ),
    'short'             : OperatorInfo( lambda n: convertToSignedInt( n , 16 ), 1 ),
    'sign'              : OperatorInfo( sign, 1 ),
    'sin'               : OperatorInfo( lambda n: performTrigOperation( n, sin ), 1 ),
    'sinh'              : OperatorInfo( lambda n: performTrigOperation( n, sinh ), 1 ),
    'solve2'            : OperatorInfo( solveQuadraticPolynomial, 3 ),
    'solve3'            : OperatorInfo( solveCubicPolynomial, 4 ),
    'solve4'            : OperatorInfo( solveQuarticPolynomial, 5 ),
    'sophieprime'       : OperatorInfo( getNthSophiePrime, 1 ),
    'spherearea'        : OperatorInfo( lambda n: getNSphereSurfaceArea( 3, n ), 1 ),
    'sphereradius'      : OperatorInfo( lambda n: getNSphereRadius( 3, n ), 1 ),
    'spherevolume'      : OperatorInfo( lambda n: getNSphereVolume( 3, n ), 1 ),
    'square'            : OperatorInfo( lambda i: exponentiate( i, 2 ), 1 ),
    'squaretri'         : OperatorInfo( getNthSquareTriangularNumber, 1 ),
    'steloct'           : OperatorInfo( getNthStellaOctangulaNumber, 1 ),
    'subfac'            : OperatorInfo( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1 ),
    'subtract'          : OperatorInfo( subtract, 2, ),
    'sunday'            : OperatorInfo( lambda: 7, 0 ),
    'superfac'          : OperatorInfo( superfac, 1 ),
    'superprime'        : OperatorInfo( getNthSuperPrime, 1 ),
    'sylvester'         : OperatorInfo( getNthSylvester, 1 ),
    'tan'               : OperatorInfo( lambda n: performTrigOperation( n, tan ), 1 ),
    'tanh'              : OperatorInfo( lambda n: performTrigOperation( n, tanh ), 1 ),
    'tetrahedral'       : OperatorInfo( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ), 1 ),
    'tetranacci'        : OperatorInfo( getNthTetranacci, 1 ),
    'tetrate'           : OperatorInfo( tetrate, 2 ),
    'thabit'            : OperatorInfo( lambda n : fsub( fmul( 3, power( 2, n ) ), 1 ), 1 ),
    'thanksgiving'      : OperatorInfo( calculateThanksgiving, 1 ),
    'thursday'          : OperatorInfo( lambda: 4, 0 ),
    'timer'             : OperatorInfo( setTimer, 1 ),
    'timer_mode'        : OperatorInfo( setTimerMode, 0 ),
    'today'             : OperatorInfo( getToday, 0 ),
    'topic'             : OperatorInfo( printHelpTopic, 1 ),
    'tounixtime'        : OperatorInfo( convertToUnixTime, 1 ),
    'trianglearea'      : OperatorInfo( getTriangleArea, 3 ),
    'triangular'        : OperatorInfo( lambda n : getNthPolygonalNumber( n, 3 ), 1 ),
    'triangular?'       : OperatorInfo( lambda n : findNthPolygonalNumber( n, 3 ), 1 ),
    'tribonacci'        : OperatorInfo( getNthTribonacci, 1 ),
    'triplebal'         : OperatorInfo( getNthTripleBalancedPrime, 1 ),
    'triplebal_'        : OperatorInfo( getNthTripleBalancedPrimeList, 1 ),
    'tripletprime'      : OperatorInfo( getNthTripletPrime, 1 ),
    'tripletprime'      : OperatorInfo( getNthTripletPrimeList, 1 ),
    'true'              : OperatorInfo( lambda: 1, 0 ),
    'truncoct'          : OperatorInfo( getNthTruncatedOctahedralNumber, 1 ),
    'trunctet'          : OperatorInfo( getNthTruncatedTetrahedralNumber, 1 ),
    'tuesday'           : OperatorInfo( lambda: 2, 0 ),
    'twinprime'         : OperatorInfo( getNthTwinPrime, 1 ),
    'twinprime_'        : OperatorInfo( getNthTwinPrimeList, 1 ),
    'uchar'             : OperatorInfo( lambda n: int( fmod( n, power( 2, 8 ) ) ), 1 ),
    'uinteger'          : OperatorInfo( lambda n, k: int( fmod( n, power( 2, k ) ) ), 2 ),
    'ulong'             : OperatorInfo( lambda n: int( fmod( n, power( 2, 32 ) ) ), 1 ),
    'ulonglong'         : OperatorInfo( lambda n: int( fmod( n, power( 2, 64 ) ) ), 1 ),
    'undouble'          : OperatorInfo( interpretAsDouble, 1 ),
    'unfloat'           : OperatorInfo( interpretAsFloat, 1 ),
    'unitroots'         : OperatorInfo( lambda i: unitroots( int( i ) ), 1 ),
    'unlist'            : OperatorInfo( unlist, 1 ),
    'ushort'            : OperatorInfo( lambda n: int( fmod( n, power( 2, 16 ) ) ), 1 ),
    'value'             : OperatorInfo( lambda n: mpf( n ), 1 ),
    'wednesday'         : OperatorInfo( lambda: 3, 0 ),
    'weekday'           : OperatorInfo( getWeekday, 1, ),
    'xor'               : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2 ),
    'ydhms'             : OperatorInfo( convertToYDHMS, 1 ),
    'year_calendar'     : OperatorInfo( generateYearCalendar, 1 ),
    'zeta'              : OperatorInfo( zeta, 1 ),
    '_dumpalias'        : OperatorInfo( dumpAliases, 0 ),
    '_dumpops'          : OperatorInfo( dumpOperators, 0 ),
    '_stats'            : OperatorInfo( dumpStats, 0 ),
    '~'                 : OperatorInfo( getInvertedBits, 1 ),
#   'antitet'           : OperatorInfo( findTetrahedralNumber, 1 ),
#   'bernfrac'          : OperatorInfo( bernfrac, 1 ),
#   'powmod'            : OperatorInfo( getPowMod, 3 ),
}


