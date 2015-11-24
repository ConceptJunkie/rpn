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

from mpmath import *

from rpnUtils import debugPrint

import rpnGlobals as g


# //******************************************************************************
# //
# //  class RPNOperatorType
# //
# //******************************************************************************

class RPNOperatorType( Enum ):
    Normal = 0,                 # any normal operator
    List = 1,                   # a list operator that prefers list arguments
    Generator = 2               # a list operator that expects a generator argument


# //******************************************************************************
# //
# //  class RPNVariable
# //
# //******************************************************************************

class RPNVariable( object ):
    def __init__( self, name ):
        self.name = name

        if name in g.variables:
            self.value = g.variables[ name ]
        else:
            self.value = nan

    def setValue( self, value ):
        self.value = value
        g.variables[ name ] = value

    def getValue( self ):
        return self.value


# //******************************************************************************
# //
# //  class RPNOperatorInfo
# //
# //******************************************************************************

class RPNOperatorInfo( object ):
    def __init__( self, function, argCount, operatorType = RPNOperatorType.Normal ):
        self.function = function
        self.argCount = argCount
        self.type = operatorType


