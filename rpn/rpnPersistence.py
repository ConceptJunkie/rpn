#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPersistence.py
# //
# //  RPN command-line calculator factoring utilities
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

if six.PY3:
    from functools import lru_cache
else:
    from pylru import lrudecorator as lru_cache
    FileNotFoundError = IOError

import bz2
import configparser
import contextlib
import functools
import os
import pickle
import sqlite3
import types

from mpmath import autoprec, mp, mpf, mpmathify, nstr

from rpn.rpnDebug import debugPrint
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnSettings import setPrecision
from rpn.rpnVersion import PROGRAM_VERSION

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  loadFactorCache
# //
# //******************************************************************************

@lru_cache( 1 )
def loadFactorCache( ):
    g.factorCache = PersistentDict( g.dataPath + os.sep + 'factors.cache' )


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
        print( 'rpn:  Unable to load unit names.  Run "makeRPNUnits" to generate the unit data files.' )
        return False

    if g.unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch.  Run "makeRPNUnits" to generate the unit data files.' )

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
        print( 'rpn:  Unable to load unit conversion data.  Run "makeRPNUnits" to generate the unit data files.' )


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
        print( 'rpn:  Unable to load unit info data.  Run "makeRPNUnits" to generate the unit data files.' )
        return False

    if g.unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch.  Run "makeRPNUnits" to generate the unit data files.' )
        return False

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
        raise ValueError( 'rpn:  Unable to load help.  Run "makeRPNHelp" to generate the help data files.' )

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitTypeDict = pickle.load( pickleFile )
    except FileNotFoundError:
        raise ValueError( 'rpn:  Unable to load unit help data.  Run "makeRPNHelp" to generate the help data files.' )

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
# //  getCacheFileName
# //
# //******************************************************************************

@lru_cache( 1 )
def getCacheFileName( name ):
    return g.dataPath + os.sep + name + '.cache'


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
# //  saveToCache
# //
# //******************************************************************************

def saveToCache( db, cursor, key, value, commit=True ):
    cursor.execute( '''INSERT INTO cache( id, value ) VALUES( ?, ? )''', ( key, value ) )

    if commit:
        db.commit( )


# //******************************************************************************
# //
# //  doesCacheExist
# //
# //******************************************************************************

def doesCacheExist( name ):
    return os.path.isfile( getCacheFileName( name ) )


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
            raise ValueError( 'prime number table ' + name + ' can\'t be found.  Run "prepareRPNPrimeData" to create the prime data.' )


# //******************************************************************************
# //
# //  class PersistentDict
# //
# //  http://stackoverflow.com/questions/9320463/persistent-memoization-in-python
# //
# //******************************************************************************

from collections import MutableMapping

class PersistentDict( MutableMapping ):
    def __init__( self, dbpath, iterable=None, **kwargs ):
        self.dbpath = dbpath

        with self.get_connection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute(
                'create table if not exists memo '
                '(key blob primary key not null, value blob not null)'
            )

        if iterable is not None:
            self.update( iterable )

        self.update( kwargs )

    def encode( self, obj ):
        return pickle.dumps( obj )

    def decode( self, blob ):
        return pickle.loads( blob )

    def get_connection( self ):
        return sqlite3.connect( self.dbpath )

    def  __getitem__( self, key ):
        key = self.encode( key )

        with self.get_connection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute(
                'select value from memo where key=?',
                ( key, )
            )

            value = cursor.fetchone( )

        if value is None:
            raise KeyError( key )

        return self.decode( value[ 0 ] )

    def __setitem__( self, key, value ):
        key = self.encode( key )
        value = self.encode( value )

        with self.get_connection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute(
                'insert or replace into memo values (?, ?)',
                ( key, value )
            )

    def __delitem__( self, key ):
        key = self.encode( key )
        with self.get_connection( ) as connection:
            cursor = connection.cursor( )

            cursor.execute(
                'select count(*) from memo where key=?',
                ( key, )
            )

            if cursor.fetchone( )[ 0 ] == 0:
                raise KeyError( key )

            cursor.execute(
                'delete from memo where key=?',
                ( key, )
            )

    def __iter__( self ):
        with self.get_connection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute(
                'select key from memo'
            )

            records = cursor.fetchall( )

        for r in records:
            yield self.decode( r[ 0 ] )

    def __len__( self ):
        with self.get_connection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute(
                'select count(*) from memo'
            )

            return cursor.fetchone( )[ 0 ]


# //******************************************************************************
# //
# //  getUserVariablesFileName
# //
# //******************************************************************************

@lru_cache( 1 )
def getUserVariablesFileName( ):
    return g.dataPath + os.sep + 'user_variables.cfg'


# //******************************************************************************
# //
# //  getUserFunctionsFileName
# //
# //******************************************************************************

@lru_cache( 1 )
def getUserFunctionsFileName( ):
    return g.dataPath + os.sep + 'user_functions.cfg'


# //******************************************************************************
# //
# //  loadUserVariablesFile
# //
# //******************************************************************************

def loadUserVariablesFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserVariablesFileName( ) )

    try:
        items = config.items( 'User Variables' )
    except:
        return

    for tuple in items:
        g.userVariables[ tuple[ 0 ] ] = tuple[ 1 ]


# //******************************************************************************
# //
# //  saveUserVariablesFile
# //
# //******************************************************************************

def saveUserVariablesFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Variables' ] = { }

    for key in g.userVariables.keys( ):
        config[ 'User Variables' ][ key ] = str( g.userVariables[ key ] )

    import os.path

    if os.path.isfile( getUserVariablesFileName( ) ):
        from shutil import copyfile
        copyfile( getUserVariablesFileName( ), getUserVariablesFileName( ) + '.backup' )

    with open( getUserVariablesFileName( ), 'w' ) as userVariablesFile:
        config.write( userVariablesFile )


# //******************************************************************************
# //
# //  openFunctionCache
# //
# //******************************************************************************

def openFunctionCache( name ):
    if name in g.functionCaches:
        return g.functionCaches[ name ]
    else:
        debugPrint( 'opening', name, 'function cache database' )
        g.functionCaches[ name ] = PersistentDict( getCacheFileName( name ) )
        return g.functionCaches[ name ]


# //******************************************************************************
# //
# //  cachedFunction
# //
# //******************************************************************************

def cachedFunction( name, override=False ):
    def namedCachedFunction( func ):
        @functools.wraps( func )

        def cacheResults( *args, **kwargs ):
            cache = openFunctionCache( name )

            if not g.ignoreCache and not override:
                if ( args, kwargs ) in cache:
                    return cache[ ( args, kwargs ) ]

            result = func( *args, **kwargs )

            if not g.ignoreCache and not override:
                cache[ ( args, kwargs ) ] = result
            return result

        return cacheResults

    return namedCachedFunction

