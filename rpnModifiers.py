#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnModifiers.py
# //
# //  RPN command-line calculator term modifier operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpnDeclarations import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  incrementNestedListLevel
# //
# //******************************************************************************

def incrementNestedListLevel( valueList ):
    g.nestedListLevel += 1

    valueList.append( list( ) )


# //******************************************************************************
# //
# //  decrementNestedListLevel
# //
# //******************************************************************************

def decrementNestedListLevel( valueList ):
    g.nestedListLevel -= 1

    if g.nestedListLevel < 0:
        raise ValueError( 'negative list level (too many \']\'s)' )


# //******************************************************************************
# //
# //  startOperatorList
# //
# //******************************************************************************

def startOperatorList( valueList ):
    if g.operatorList:
        raise ValueError( 'nested operator lists are not supported' )

    g.operatorList = True
    g.lastOperand = len( valueList ) - 1
    g.operandsToRemove = 0
    g.operatorsInList = 0

    valueList.append( list( ) )


# //******************************************************************************
# //
# //  endOperatorList
# //
# //******************************************************************************

def endOperatorList( valueList ):
    if not g.operatorList:
        raise ValueError( 'mismatched operator list ending' )

    g.operatorList = False

    del valueList[ g.lastOperand - ( g.operandsToRemove - 1 ) : g.lastOperand + 2 ]

    result = [ ]

    for i in range( 0, g.operatorsInList ):
        result.insert( 0, valueList.pop( ) )

    valueList.append( result )


# //******************************************************************************
# //
# //  duplicateTerm
# //
# //******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for i in range( 0, int( count ) ):
        if isinstance( value, list ):
            for j in value:
                valueList.append( j )
        else:
            valueList.append( value )


# //******************************************************************************
# //
# //  duplicateOperation
# //
# //******************************************************************************

def duplicateOperation( valueList ):
    if g.duplicateOperations > 0:
        raise ValueError( "'dupop' must be followed by another operation" )

    if isinstance( valueList[ -1 ], list ):
        raise ValueError( "'dupop' cannot accept a list argument" )

    g.duplicateOperations = nint( floor( valueList.pop( ) ) )


# //******************************************************************************
# //
# //  unlist
# //
# //******************************************************************************

def unlist( valueList ):
    arg = valueList.pop( )

    if isinstance( arg, list ):
        for i in arg:
            valueList.append( i )
    else:
        valueList.append( arg )


# //******************************************************************************
# //
# //  handleUseMembersOperator
# //
# //******************************************************************************

def handleUseMembersOperator( valueList ):
    g.useMembers += 1


# //******************************************************************************
# //
# //  flatten
# //
# //  http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
# //
# //******************************************************************************

def _flatten( L, containers = ( list, tuple ) ):
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


# //******************************************************************************
# //
# //  getPrevious
# //
# //******************************************************************************

def getPrevious( valueList ):
    valueList.append( valueList[ -1 ] )


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


