#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnModifiers.py
# //
# //  RPN command-line calculator term modifier operators
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
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
# //  Unlike all other operators, '[' and ']' change global state.
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
        raise ValueError( "negative list level (too many ']'s)" )


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
# //  flatten
# //
# //  http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
# //
# //******************************************************************************

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


