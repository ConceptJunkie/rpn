#!/usr/bin/env python

#******************************************************************************
#
#  rpnDebug.py
#
#  rpnChilada debug utility functions
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import builtins

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  debugPrint
#
#******************************************************************************

def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


#******************************************************************************
#
#  debugPrintNoNewLine
#
#******************************************************************************

def debugPrintNoNewLine( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs, end='\r' )
    else:
        return
