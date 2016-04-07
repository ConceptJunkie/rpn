#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDeclarations.py
# //
# //  RPN command-line calculator declarations
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
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
# //  class RPNOperatorType
# //
# //******************************************************************************

class RPNOperatorType( Enum ):
    """This enum is used to identify among the different types of operator."""
    Default = 0,                    # any argument is valid
    List = 1,                       # the argument must be a list or a generator
    Real = 2,                       # the argument must be a real number
    Integer = 3,
    PositiveInteger = 4,            # the argument must be a positive integer
    NonnegativeInteger = 5,
    String = 6,
    Date = 7,
    Location = 8,
    Generator = 9,
    Function = 10


# //******************************************************************************
# //
# //  class RPNOperatorInfo
# //
# //******************************************************************************

class RPNOperatorInfo( object ):
    """This class represents all the data needed to define an operator."""
    def __init__( self, function, argCount, argTypes = list( ) ):
        self.function = function
        self.argCount = argCount
        self.argTypes = argTypes

