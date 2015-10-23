#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnFactor.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import collections
import contextlib
import fractions
import os
import pickle
import random

import rpnGlobals as g

from rpnPrimes import primes
from rpnSettings import setAccuracy
from rpnUtils import DelayedKeyboardInterrupt


# //******************************************************************************
# //
# //  loadFactorCache
# //
# //******************************************************************************

def loadFactorCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'rb' ) ) as pickleFile:
            factorCache = pickle.load( pickleFile )
    except FileNotFoundError:
        factorCache = { }

    return factorCache


# //******************************************************************************
# //
# //  saveFactorCache
# //
# //******************************************************************************

def saveFactorCache( factorCache ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( factorCache, pickleFile )


