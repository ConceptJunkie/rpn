#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPersistence.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

if not six.PY3:
    FileNotFoundError = IOError

import bz2
import contextlib
import functools
import os
import pickle
import sqlite3
import types

from mpmath import autoprec, mp, mpf, mpmathify, nstr

import rpnGlobals as g

from rpnGenerator import RPNGenerator
from rpnSettings import setPrecision
from rpnUtils import debugPrint, DelayedKeyboardInterrupt
from rpnVersion import PROGRAM_VERSION


# //******************************************************************************
# //
# //  loadFactorCache
# //
# //******************************************************************************

def loadFactorCache( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'rb' ) ) as pickleFile:
            g.factorCache = pickle.load( pickleFile )
    except FileNotFoundError:
        g.factorCache = { }


# //******************************************************************************
# //
# //  saveFactorCache
# //
# //******************************************************************************

def saveFactorCache( ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'factors.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( g.factorCache, pickleFile )


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

    # TODO:  handle RPNGenerator and RPNMeasurement
    try:
        with DelayedKeyboardInterrupt( ):
            with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
                pickle.dump( result, pickleFile )
    except:
        pass #print( 'error:  failed to save result' )


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


# //******************************************************************************
# //
# //  loadOperatorCache
# //
# //******************************************************************************

def loadOperatorCache( name ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + name + '.pckl.bz2', 'rb' ) ) as pickleFile:
            operatorCache = pickle.load( pickleFile )
    except FileNotFoundError:
        operatorCache = { }

    return operatorCache


# //******************************************************************************
# //
# //  saveOperatorCache
# //
# //******************************************************************************

def saveOperatorCache( operatorCache, name ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + name + '.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( operatorCache, pickleFile )


# //******************************************************************************
# //
# //  pickledFunction
# //
# //  The caches are saved once when flushDirtyCaches is called by main( ).
# //
# //******************************************************************************

def pickledFunction( name ):
    def namedPickledFunction( func ):
        @functools.wraps( func )
        def cacheResults( *args, **kwargs ):
            if name not in g.operatorCaches:
                g.operatorCaches[ name ] = loadOperatorCache( name )

            if args in g.operatorCaches[ name ]:
                return g.operatorCaches[ name ][ args ]
            else:
                result = func( *args, **kwargs )

                g.operatorCaches[ name ][ args ] = result

                if name not in g.dirtyCaches:
                    g.dirtyCaches.add( name )

                return result

        return cacheResults

    return namedPickledFunction


# //******************************************************************************
# //
# //  openFunctionCache
# //
# //******************************************************************************

def openFunctionCache( name ):
    if name in g.cursors:
        return g.cursors[ name ]
    else:
        debugPrint( 'opening', name, 'function cache database' )
        g.databases[ name ] = sqlite3.connect( getCacheFileName( name ) )
        g.cursors[ name ] = g.databases[ name ].cursor( )
        g.cursors[ name ].execute(
            '''CREATE TABLE IF NOT EXISTS cache( id TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL, precision INTEGER )'''
        )

        return g.cursors[ name ]


# //******************************************************************************
# //
# //  cachedFunctionWithPrecision
# //
# //  This can only be used with a function that returns a single mpf value.
# //
# //******************************************************************************

def cachedFunctionWithPrecision( name ):
    def namedCachedFunction( func ):
        @functools.wraps( func )
        def cacheResults( *args, **kwargs ):
            openFunctionCache( name )
            lookup, result, precision = lookUpFunctionCacheWithPrecision( g.cursors[ name ], repr( args ) )

            if lookup and mp.dps <= precision:
                return result

            result = func( *args, **kwargs )
            saveToFunctionCacheWithPrecision( g.databases[ name ], g.cursors[ name ], repr( args ), nstr( result, n=mp.dps ), mp.dps, update=lookup )
            return result

        return cacheResults

    return namedCachedFunction


# //******************************************************************************
# //
# //  cachedFunction
# //
# //  Use this version if the function is smart enough to determine what
# //  precision it should use.  The primary use-case if for functions that
# //  return one or more integer values and which determine the precision
# //  automatically.
# //
# //******************************************************************************

def cachedFunction( name ):
    def namedCachedFunction( func ):
        @functools.wraps( func )
        def cacheResults( *args, **kwargs ):
            openFunctionCache( name )
            lookup, result = lookUpFunctionCache( g.cursors[ name ], repr( args ) )

            if lookup:
                return result

            result = func( *args, **kwargs )
            saveToCache( g.databases[ name ], g.cursors[ name ], repr( args ), nstr( result, n=mp.dps ) )
            return result

        return cacheResults

    return namedCachedFunction


# //******************************************************************************
# //
# //  flushDirtyCaches
# //
# //******************************************************************************

def flushDirtyCaches( ):
    for name in g.dirtyCaches:
        saveOperatorCache( g.operatorCaches[ name ], name )

    g.dirtyCaches.clear( )

    if g.factorCacheIsDirty:
        saveFactorCache( )

    for name in g.dirtyCaches:
        debugPrint( 'flushing the', name, 'pickle cache' )
        saveOperatorCache( g.operatorCaches[ name ], name )

    for name in g.databases:
        debugPrint( 'closing the', name, 'function cache database' )
        g.databases[ name ].close( )


# //******************************************************************************
# //
# //  getCacheFileName
# //
# //******************************************************************************

def getCacheFileName( name ):
    return g.dataPath + os.sep + name


# //******************************************************************************
# //
# //  doesCacheExist
# //
# //******************************************************************************

def doesCacheExist( name ):
    return os.path.isfile( getCacheFileName( name ) )


# //******************************************************************************
# //
# //  deleteCache
# //
# //******************************************************************************

def deleteCache( name ):
    if doesCacheExist( name ):
        os.remove( getCacheFileName( name ) )


# //******************************************************************************
# //
# //  lookUpCache
# //
# //******************************************************************************

def lookUpCache( cursor, key ):
    try:
        cursor.execute( '''SELECT value FROM cache WHERE id=?''', ( key, ) )
    except sqlite3.DatabaseError:
        return False, None
    except sqlite3.IntegrityError:
        return False, None

    result = cursor.fetchone( )

    if result is None:
        return False, None
    else:
        return True, eval( result[ 0 ] )


# //******************************************************************************
# //
# //  lookUpFunctionCache
# //
# //******************************************************************************

def lookUpFunctionCache( cursor, key ):
    try:
        cursor.execute( '''SELECT value FROM cache WHERE id=?''', ( key, ) )
    except sqlite3.DatabaseError:
        return False, None
    except sqlite3.IntegrityError:
        return False, None

    result = cursor.fetchone( )

    if result is None:
        return False, None
    else:
        return True, eval( result[ 0 ] )


# //******************************************************************************
# //
# //  lookUpFunctionCacheWithPrecision
# //
# //******************************************************************************

def lookUpFunctionCacheWithPrecision( cursor, key ):
    try:
        cursor.execute( '''SELECT value, precision FROM cache WHERE id=?''', ( key, ) )
    except sqlite3.DatabaseError:
        return False, None
    except sqlite3.IntegrityError:
        return False, None

    result = cursor.fetchone( )

    if result is None:
        return False, None, 0
    else:
        return True, mpmathify( result[ 0 ] ), result[ 1 ]


# //******************************************************************************
# //
# //  saveToCache
# //
# //******************************************************************************

def saveToCache( db, cursor, key, value, commit=True ):
    cursor.execute( '''INSERT INTO cache( id, value ) VALUES( ?, ? )''', ( key, value ) )

    if commit:
        db.commit( )


# //******************************************************************************
# //
# //  saveToFunctionCacheWithPrecision
# //
# //******************************************************************************

def saveToFunctionCacheWithPrecision( db, cursor, key, value, precision, commit=True, update=False ):
    if update:
        cursor.execute( '''UPDATE cache SET value = ?, precision = ? WHERE id = ?''', ( value, precision, key ) )
    else:
        cursor.execute( '''INSERT INTO cache( id, value, precision ) VALUES( ?, ?, ? )''', ( key, value, precision ) )

    if commit:
        db.commit( )


# //******************************************************************************
# //
# //  createPrimeCache
# //
# //******************************************************************************

def createPrimeCache( name ):
    db = sqlite3.connect( getCacheFileName( name ) )

    cursor = db.cursor( )
    cursor.execute( '''CREATE TABLE cache( id INTEGER PRIMARY KEY, value INTEGER )''' )
    db.commit( )

    return db, cursor


# //******************************************************************************
# //
# //  openPrimeCache
# //
# //******************************************************************************

def openPrimeCache( name ):
    if name in g.cursors:
        return g.cursors[ name ]
    else:
        try:
            g.databases[ name ] = sqlite3.connect( getCacheFileName( name ) )
            g.cursors[ name ] = g.databases[ name ].cursor( )
        except:
            print( 'prime number table ' + name + ' can\'t be found, please run preparePrimeData.py' )


