#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnFunction.py
# //
# //  RPN command-line calculator function operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import *

from rpnDeclarations import *


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

    print( 'func', func.valueList )

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

