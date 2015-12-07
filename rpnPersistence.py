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
import contextlib
import os
import pickle
import types

import rpnGlobals as g

from rpnGenerator import RPNGenerator
from rpnUtils import DelayedKeyboardInterrupt
from rpnVersion import PROGRAM_VERSION


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


# //******************************************************************************
# //
# //  loadUnitNameData
# //
# //******************************************************************************

def loadUnitNameData( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_names.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitsVersion = pickle.load( pickleFile )
            g.unitOperatorNames = pickle.load( pickleFile )
            g.operatorAliases.update( pickle.load( pickleFile ) )
    except IOError:
        print( 'rpn:  Unable to load unit names.  Run makeUnits.py to make the unit data files.' )
        return False

    if g.unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch' )

    return True


# //******************************************************************************
# //
# //  loadUnitConversionMatrix
# //
# //******************************************************************************

def loadUnitConversionMatrix( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitConversionMatrix.update( pickle.load( pickleFile ) )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit conversion data.  Unit conversion will be unavailable.  Run makeUnits.py to make the unit data files.' )


# //******************************************************************************
# //
# //  loadUnitData
# //
# //******************************************************************************

def loadUnitData( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitsVersion = pickle.load( pickleFile )
            g.basicUnitTypes.update( pickle.load( pickleFile ) )
            g.unitOperators.update( pickle.load( pickleFile ) )
    except IOError:
        print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.  Run makeUnits.py to make the unit data files.' )
        return False

    if g.unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch' )

    return True


# //******************************************************************************
# //
# //  loadHelpData
# //
# //******************************************************************************

def loadHelpData( ):
    if g.helpLoaded:
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.helpVersion = pickle.load( pickleFile )
            g.helpTopics = pickle.load( pickleFile )
            g.operatorHelp = pickle.load( pickleFile )
    except FileNotFoundError:
        print( 'rpn:  Unable to load help file.  Help will be unavailable.  Run makeHelp.py to create the help files.' )
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitTypeDict = pickle.load( pickleFile )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit help data.  Run makeUnits.py to make the unit data files.' )
        return False

    g.operatorCategories = set( g.operatorHelp[ key ][ 0 ] for key in g.operatorHelp )

    g.helpLoaded = True

    return True


# //******************************************************************************
# //
# //  loadResult
# //
# //******************************************************************************

def loadResult( ):
    try:
        fileName = g.dataPath + os.sep + 'result.pckl.bz2'

        with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError:
        result = 0

    return result


# //******************************************************************************
# //
# //  saveResult
# //
# //******************************************************************************

def saveResult( result ):
    if not os.path.isdir( g.dataPath ):
        os.makedirs( g.dataPath )

    fileName = g.dataPath + os.sep + 'result.pckl.bz2'

    # TODO:  handle RPNGenerator
    try:
        with DelayedKeyboardInterrupt( ):
            with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
                pickle.dump( result, pickleFile )
    except:
        pass


# //******************************************************************************
# //
# //  loadUserConstants
# //
# //******************************************************************************

def loadConstants( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'constants.pckl.bz2', 'rb' ) ) as pickleFile:
            constants = pickle.load( pickleFile )
    except FileNotFoundError:
        constants = { }

    return constants


# //******************************************************************************
# //
# //  saveConstants
# //
# //******************************************************************************

def saveConstants( constants ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'constants.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( constants, pickleFile )

