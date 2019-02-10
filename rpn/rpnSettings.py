#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnSettings.py
# //
# //  RPN command-line interactive mode settings functions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import mp

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  setAccuracy
# //
# //******************************************************************************

def setAccuracy( n ):
    if n == -1:
        g.outputAccuracy = g.defaultOutputAccuracy
    else:
        g.outputAccuracy = int( n )

    if mp.dps < g.outputAccuracy:
        mp.dps = g.outputAccuracy

    return g.outputAccuracy


# //******************************************************************************
# //
# //  setPrecision
# //
# //******************************************************************************

def setPrecision( n ):
    if n == -1:
        mp.dps = g.defaultPrecision
    else:
        mp.dps = int( n )

    if mp.dps < g.outputAccuracy:
        mp.dps = g.outputAccuracy

    return mp.dps


# //******************************************************************************
# //
# //  setComma
# //
# //******************************************************************************

def setComma( n ):
    if n == 1:
        g.comma = True
    else:
        g.comma = False

    return 1 if g.comma else 0


# //******************************************************************************
# //
# //  setTimer
# //
# //******************************************************************************

def setTimer( n ):
    if n == 1:
        g.timer = True
    else:
        g.timer = False

    return 1 if g.timer else 0


# //******************************************************************************
# //
# //  setIntegerGrouping
# //
# //******************************************************************************

def setIntegerGrouping( n ):
    if n == -1:
        g.integerGrouping = g.defaultIntegerGrouping
    else:
        g.integerGrouping = int( n )

    return g.integerGrouping


# //******************************************************************************
# //
# //  setDecimalGrouping
# //
# //******************************************************************************

def setDecimalGrouping( n ):
    if n == -1:
        g.decimalGrouping = g.defaultDecimalGrouping
    else:
        g.decimalGrouping = int( n )

    return g.decimalGrouping


# //******************************************************************************
# //
# //  setInputRadix
# //
# //******************************************************************************

def setInputRadix( n ):
    if n in [ 0, -1 ]:
        g.inputRadix = g.defaultInputRadix
    else:
        g.inputRadix = int( n )

    return g.inputRadix


# //******************************************************************************
# //
# //  setOutputRadix
# //
# //******************************************************************************

def setOutputRadix( n ):
    if n in [ 0, -1 ]:
        g.outputRadix = g.defaultOutputRadix
    else:
        g.outputRadix = int( n )

    return g.outputRadix


# //******************************************************************************
# //
# //  setLeadingZero
# //
# //******************************************************************************

def setLeadingZero( n ):
    result = 1 if g.leadingZero else 0

    if ( n == 0 ):
        g.leadingZero = False
    else:
        g.leadingZero = True

    return result


# //******************************************************************************
# //
# //  setIdentify
# //
# //******************************************************************************

def setIdentify( n ):
    result = 1 if g.identify else 0

    if ( n == 0 ):
        g.identify = False
    else:
        g.identify = True

    return result


# //******************************************************************************
# //
# //  setHexMode
# //
# //******************************************************************************

def setHexMode( ):
    g.tempHexMode = True
    return 0


# //******************************************************************************
# //
# //  setOctalMode
# //
# //******************************************************************************

def setOctalMode( ):
    g.tempOctalMode = True
    return 0


# //******************************************************************************
# //
# //  setCommaMode
# //
# //******************************************************************************

def setCommaMode( ):
    g.tempCommaMode = True
    return 0


# //******************************************************************************
# //
# //  setTimerMode
# //
# //******************************************************************************

def setTimerMode( ):
    g.tempTimerMode = True
    return 0


# //******************************************************************************
# //
# //  setLeadingZeroMode
# //
# //******************************************************************************

def setLeadingZeroMode( ):
    g.tempLeadingZeroMode = True
    return 0


# //******************************************************************************
# //
# //  setIdentifyMode
# //
# //******************************************************************************

def setIdentifyMode( ):
    g.tempIdentifyMode = True
    return 0

