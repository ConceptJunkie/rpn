#!/usr/bin/env python

#******************************************************************************
#
#  rpnExpression.py
#
#  rpnChilada expression class and related utilities
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import mpmathify

from rpn.rpnDebug import debugPrint

import rpn.rpnGlobals as g


#******************************************************************************
#
#  class RPNExpression
#
#******************************************************************************

class RPNExpression( object ):
    '''This class defines an expression used for parsing rpnChilada.'''
    def __init__( self, operators, arguments ):
        self.operators = [ ]
        self.argumemts = [ ]

    def parse( self ):
        '''.'''
        return self

