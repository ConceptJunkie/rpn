#!/usr/bin/env python

#******************************************************************************
#
#  rpnSettings.py
#
#  rpnChilada command-line interactive mode settings functions
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#  NOTE:  The usual operator decorators can't be used here, because these
#         operators don't return a value.  They only have a side-effect.

#******************************************************************************

from mpmath import mp

import rpn.util.rpnGlobals as g

from rpn.util.rpnDebug import debugPrint


#******************************************************************************
#
#  getAccuracy
#
#******************************************************************************

def getAccuracy( ):
    return mp.dps

#******************************************************************************
#
#  setAccuracyOperator
#
#  Setting the accuracy sets the precision to the same value.  So if you want
#  precision to be different, you need to set it afterwards.
#
#******************************************************************************

def setAccuracy( n, force=False ):
    '''
    This function make sure that the accuracy is at least as high as n.  If it's
    already higher, it doesn't lower it.
    '''
    if n < -1:
        raise ValueError( '\'default\', or a non-negative value expected' )

    if n == -1:
        g.outputAccuracy = g.defaultOutputAccuracy
    else:
        g.outputAccuracy = max( int( n ), g.defaultOutputAccuracy )

    if mp.dps < g.outputAccuracy or force:
        mp.dps = g.outputAccuracy
        debugPrint( 'setAccuracy', g.outputAccuracy )

    return g.outputAccuracy


def setAccuracyOperator( n ):
    return setAccuracy( n[ 0 ] )


#******************************************************************************
#
#  setPrecisionOperator
#
#  Accuracy can't be set lower, but precision can.
#
#******************************************************************************

def setPrecision( n ):
    if n < -1:
        raise ValueError( '\'default\', or a non-negative value expected' )

    g.outputPrecision = int( n )

    # make sure the accuracy is at least as high as the precision
    setAccuracy( g.outputPrecision + 2 )

    return g.outputPrecision


def setPrecisionOperator( n ):
    return setPrecision( n[ 0 ] )


#******************************************************************************
#
#  setCommaOperator
#
#******************************************************************************

def setCommaOperator( n ):
    n = n[ 0 ]

    if n not in ( -1, 0, 1 ):
        raise ValueError( '\'true\', \'false\', or \'default\' expected' )

    if n == 1:
        g.comma = True
    else:
        g.comma = False

    return 1 if g.comma else 0


#******************************************************************************
#
#  setTimerOperator
#
#******************************************************************************

def setTimerOperator( n ):
    n = n[ 0 ]

    if n not in ( -1, 0, 1 ):
        raise ValueError( '\'true\', \'false\', or \'default\' expected' )

    if n == 1:
        g.timer = True
    else:
        g.timer = False

    return 1 if g.timer else 0


#******************************************************************************
#
#  setIntegerGroupingOperator
#
#******************************************************************************

def setIntegerGroupingOperator( n ):
    n = n[ 0 ]

    if n < -1:
        raise ValueError( '\'default\', or a non-negative value expected' )

    if n == -1:
        g.integerGrouping = g.defaultIntegerGrouping
    else:
        g.integerGrouping = int( n )

    return g.integerGrouping


#******************************************************************************
#
#  setDecimalGroupingOperator
#
#******************************************************************************

def setDecimalGroupingOperator( n ):
    n = n[ 0 ]

    if n < -1:
        raise ValueError( '\'default\', or a non-negative value expected' )

    if n == -1:
        g.decimalGrouping = g.defaultDecimalGrouping
    else:
        g.decimalGrouping = int( n )

    return g.decimalGrouping


#******************************************************************************
#
#  setInputRadixOperator
#
#******************************************************************************

def setInputRadixOperator( n ):
    n = n[ 0 ]

    if n < -1:
        raise ValueError( '\'default\', or a non-negative value expected' )

    if n in [ 0, -1 ]:
        g.inputRadix = g.defaultInputRadix
    else:
        g.inputRadix = int( n )

    return g.inputRadix


#******************************************************************************
#
#  setOutputRadixOperator
#
#******************************************************************************

def setOutputRadixOperator( n ):
    n = n[ 0 ]

    if n in [ 0, -1 ]:
        g.outputRadix = g.defaultOutputRadix
    else:
        g.outputRadix = int( n )

    return g.outputRadix


#******************************************************************************
#
#  setLeadingZeroOperator
#
#******************************************************************************

def setLeadingZeroOperator( n ):
    n = n[ 0 ]

    if n not in ( -1, 0, 1 ):
        raise ValueError( '\'true\', \'false\', or \'default\' expected' )

    result = 1 if g.leadingZero else 0

    if n == 0:
        g.leadingZero = False
    else:
        g.leadingZero = True

    return result


#******************************************************************************
#
#  setIdentifyOperator
#
#******************************************************************************

def setIdentifyOperator( n ):
    n = n[ 0 ]

    if n not in ( -1, 0, 1 ):
        raise ValueError( '\'true\', \'false\', or \'default\' expected' )

    result = 1 if g.identify else 0

    if n in ( -1, 0 ):
        g.identify = False
    else:
        g.identify = True

    return result


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
