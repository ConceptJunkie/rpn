#!/usr/bin/env python

#******************************************************************************
#
#  rpnExpression.py
#
#  rpnChilada expression class and related utilities
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

#******************************************************************************
#
#  class RPNExpression
#
#******************************************************************************

class RPNExpression( ):
    '''
    This class defines an expression used for parsing rpnChilada.
    '''
    def __init__( self, operators, arguments ):
        self.operators = operators
        self.arguments = arguments

    def parse( self ):
        '''.'''
        return self

    def generateCode( self ):
        '''.'''
        return self.arguments
