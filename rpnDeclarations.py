#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDeclarations.py
# //
# //  RPN command-line calculator declarations
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from enum import Enum

from mpmath import nan

from rpnUtils import debugPrint

import rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNOperatorType
# //
# //******************************************************************************

class RPNOperatorType( Enum ):
    """This enum is used to identify among the different types of operator."""
    Normal = 0,                 # any normal operator
    List = 1,                   # a list operator that prefers list arguments
    Generator = 2               # a list operator that expects a generator argument


# //******************************************************************************
# //
# //  class RPNVariable
# //
# //******************************************************************************

class RPNVariable( object ):
    """This class represents a variable in rpn, and it maintains a global
       dictionary of all variables keyed by name."""
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
# //  class RPNOperatorInfo
# //
# //******************************************************************************

class RPNOperatorInfo( object ):
    """This class represents all the data needed to define an operator."""
    def __init__( self, function, argCount, operatorType = RPNOperatorType.Normal ):
        self.function = function
        self.argCount = argCount
        self.type = operatorType


