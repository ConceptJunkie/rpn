#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnModifiers.py
# //
# //  rpnChilada term modifier operators
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import floor, nint

import rpn.rpnGlobals as g


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

def decrementNestedListLevel( _ ):
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
        raise ValueError( 'mismatched operator list ending (\'}\')' )

    g.operatorList = False

    del valueList[ g.lastOperand - ( g.operandsToRemove - 1 ) : g.lastOperand + 2 ]

    result = [ ]

    for _ in range( 0, g.operatorsInList ):
        operator = valueList.pop( )
        #print( 'operator', operator )
        result.insert( 0, operator )

    valueList.append( result )


# //******************************************************************************
# //
# //  duplicateTerm
# //
# //******************************************************************************

def duplicateTerm( valueList ):
    count = valueList.pop( )
    value = valueList.pop( )

    for _ in range( 0, int( count ) ):
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
        raise ValueError( "'duplicate_operator' must be followed by another operation" )

    if isinstance( valueList[ -1 ], list ):
        raise ValueError( "'duplicate_operator' cannot accept a list argument" )

    argument = nint( floor( valueList.pop( ) ) )

    if argument < 1:
        raise ValueError( "'duplicate_operator' requires an argument of 1 or more (n.b., 1 has no effect)" )

    g.duplicateOperations = argument


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
# //  getPrevious
# //
# //******************************************************************************

def getPrevious( valueList ):
    valueList.append( valueList[ -1 ] )

