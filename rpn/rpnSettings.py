#!/usr/bin/env python

#******************************************************************************
#
#  rpnSettings.py
#
#  rpnChilada command-line interactive mode settings functions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import fadd, mp

import rpn.rpnGlobals as g

from rpn.rpnValidator import argValidator, IntValidator


#******************************************************************************
#
#  setAccuracy
#
#******************************************************************************

def setAccuracy( n ):
    '''
    This function make sure that the accuracy is at least as high as n.  If it's
    already higher, it doesn't lower it.
    '''
    if n == -1:
        g.outputAccuracy = g.defaultOutputAccuracy
    else:
        g.outputAccuracy = int( n )

    if mp.dps < g.outputAccuracy:
        mp.dps = g.outputAccuracy

    return g.outputAccuracy


@argValidator( [ IntValidator( 0 ) ] )
def setAccuracyOperator( n ):
    return setAccuracy( fadd( n, 2 ) )


#******************************************************************************
#
#  setPrecision
#
#******************************************************************************

def setPrecision( n ):
    if n == -1:
        mp.dps = g.defaultPrecision
    else:
        mp.dps = int( n )

    if mp.dps < g.outputAccuracy:
        mp.dps = g.outputAccuracy

    return mp.dps


@argValidator( [ IntValidator( 0 ) ] )
def setPrecisionOperator( n ):
    setPrecision( n )


#******************************************************************************
#
#  setComma
#
#******************************************************************************

def setComma( n ):
    if n == 1:
        g.comma = True
    else:
        g.comma = False

    return 1 if g.comma else 0


@argValidator( [ IntValidator( 0, 1 ) ] )
def setCommaOperator( n ):
    setComma( n )


#******************************************************************************
#
#  setTimer
#
#******************************************************************************

def setTimer( n ):
    if n == 1:
        g.timer = True
    else:
        g.timer = False

    return 1 if g.timer else 0


@argValidator( [ IntValidator( 0, 1 ) ] )
def setTimerOperator( n ):
    setTimer( n )


#******************************************************************************
#
#  setIntegerGrouping
#
#******************************************************************************

def setIntegerGrouping( n ):
    if n == -1:
        g.integerGrouping = g.defaultIntegerGrouping
    else:
        g.integerGrouping = int( n )

    return g.integerGrouping


@argValidator( [ IntValidator( -1 ) ] )
def setIntegerGroupingOperator( n ):
    setIntegerGrouping( n )


#******************************************************************************
#
#  setDecimalGrouping
#
#******************************************************************************

def setDecimalGrouping( n ):
    if n == -1:
        g.decimalGrouping = g.defaultDecimalGrouping
    else:
        g.decimalGrouping = int( n )

    return g.decimalGrouping


@argValidator( [ IntValidator( -1 ) ] )
def setDecimalGroupingOperator( n ):
    setDecimalGrouping( n )


#******************************************************************************
#
#  setInputRadix
#
#******************************************************************************

def setInputRadix( n ):
    if n in [ 0, -1 ]:
        g.inputRadix = g.defaultInputRadix
    else:
        g.inputRadix = int( n )

    return g.inputRadix


@argValidator( [ IntValidator( -1 ) ] )
def setInputRadixOperator( n ):
    setInputRadix( n )


#******************************************************************************
#
#  setOutputRadix
#
#******************************************************************************

def setOutputRadix( n ):
    if n in [ 0, -1 ]:
        g.outputRadix = g.defaultOutputRadix
    else:
        g.outputRadix = int( n )

    return g.outputRadix


@argValidator( [ IntValidator( -1 ) ] )
def setOutputRadixOperator( n ):
    setOutputRadix( n )


#******************************************************************************
#
#  setLeadingZero
#
#******************************************************************************

def setLeadingZero( n ):
    result = 1 if g.leadingZero else 0

    if n == 0:
        g.leadingZero = False
    else:
        g.leadingZero = True

    return result


@argValidator( [ IntValidator( 0, 1 ) ] )
def setLeadingZeroOperator( n ):
    setLeadingZero( n )


#******************************************************************************
#
#  setIdentify
#
#******************************************************************************

def setIdentify( n ):
    result = 1 if g.identify else 0

    if n == 0:
        g.identify = False
    else:
        g.identify = True

    return result


@argValidator( [ IntValidator( 0, 1 ) ] )
def setIdentifyOperator( n ):
    setIdentify( n )


#******************************************************************************
#
#  setHexModeOperator
#
#******************************************************************************

def setHexModeOperator( ):
    g.tempHexMode = True
    return 0


#******************************************************************************
#
#  setOctalModeOperator
#
#******************************************************************************

def setOctalModeOperator( ):
    g.tempOctalMode = True
    return 0


#******************************************************************************
#
#  setCommaModeOperator
#
#******************************************************************************

def setCommaModeOperator( ):
    g.tempCommaMode = True
    return 0


#******************************************************************************
#
#  setTimerModeOperator
#
#******************************************************************************

def setTimerModeOperator( ):
    g.tempTimerMode = True
    return 0


#******************************************************************************
#
#  setLeadingZeroModeOperator
#
#******************************************************************************

def setLeadingZeroModeOperator( ):
    g.tempLeadingZeroMode = True
    return 0


#******************************************************************************
#
#  setIdentifyModeOperator
#
#******************************************************************************

def setIdentifyModeOperator( ):
    g.tempIdentifyMode = True
    return 0
