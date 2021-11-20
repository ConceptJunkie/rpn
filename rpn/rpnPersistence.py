#!/usr/bin/env python

#******************************************************************************
#
#  rpnPersistence.py
#
#  rpnChilada persistence functions
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import bz2
import configparser
import contextlib
import functools
import os
import pickle
import sqlite3

from collections.abc import MutableMapping
from functools import lru_cache
from shutil import copyfile

from rpn.rpnDebug import debugPrint
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnKeyboard import DelayedKeyboardInterrupt
from rpn.rpnUtils import getUserDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_NAME

import rpn.rpnGlobals as g


#******************************************************************************
#
#  loadFactorCache
#
#******************************************************************************

@lru_cache( 1 )
def loadFactorCache( ):
    g.factorCache = PersistentDict( getUserDataPath( ) + os.sep + 'factors.cache' )


#******************************************************************************
#
#  loadUnitNameData
#
#******************************************************************************

def loadUnitNameData( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'unit_names.pckl.bz2', 'rb' ) ) \
                as pickleFile:
            unitsVersion = pickle.load( pickleFile )
            g.unitOperatorNames = pickle.load( pickleFile )
            g.constantOperatorNames = pickle.load( pickleFile )
            g.aliases.update( pickle.load( pickleFile ) )
    except IOError:
        print( 'rpn:  Unable to load unit names.  Run "makeUnits" to generate the unit data files.' )
        return False

    if unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch.  Run "makeUnits" to generate the unit data files.' )

    return True


#******************************************************************************
#
#  loadUnitConversionMatrix
#
#******************************************************************************

def loadUnitConversionMatrix( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) \
                as pickleFile:
            g.unitConversionMatrix.update( pickle.load( pickleFile ) )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit conversion data.  Run "makeUnits" to generate the unit data files.' )


#******************************************************************************
#
#  loadUnitData
#
#******************************************************************************

def loadUnitData( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'units.pckl.bz2', 'rb' ) ) \
                as pickleFile:
            unitsVersion = pickle.load( pickleFile )
            g.basicUnitTypes.update( pickle.load( pickleFile ) )
            g.unitOperators.update( pickle.load( pickleFile ) )
            g.constantOperators.update( pickle.load( pickleFile ) )
    except IOError:
        print( 'rpn:  Unable to load unit info data.  Run "makeUnits" to generate the unit data files.' )
        return False

    if unitsVersion != PROGRAM_VERSION:
        print( 'rpn:  units data file version mismatch.  Run "makeUnits" to generate the unit data files.' )
        return False

    return True


#******************************************************************************
#
#  loadHelpData
#
#******************************************************************************

def loadHelpData( ):
    if g.helpLoaded:
        return True

    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.helpVersion = pickle.load( pickleFile )
            g.HELP_TOPICS = pickle.load( pickleFile )
            g.OPERATOR_HELP = pickle.load( pickleFile )
    except FileNotFoundError:
        raise ValueError( 'rpn:  Unable to load help.  Run "makeHelp" to generate the help data files.' )

    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'unit_help.pckl.bz2', 'rb' ) ) \
                as pickleFile:
            g.unitTypeDict = pickle.load( pickleFile )
    except FileNotFoundError:
        raise ValueError( 'rpn:  Unable to load unit help data.  Run "makeHelp" to generate the help data files.' )

    g.operatorCategories = set( g.OPERATOR_HELP[ key ][ 0 ] for key in g.OPERATOR_HELP )

    g.helpLoaded = True

    return True


#******************************************************************************
#
#  loadResultOperator
#
#******************************************************************************

def loadResultOperator( ):
    try:
        fileName = getUserDataPath( ) + os.sep + 'result.pckl.bz2'

        with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError:
        result = 0

    return result


#******************************************************************************
#
#  saveResult
#
#******************************************************************************

def saveResult( result ):
    fileName = getUserDataPath( ) + os.sep + 'result.pckl.bz2'

    # TODO: handle RPNGenerator and RPNMeasurement
    try:
        with DelayedKeyboardInterrupt( ):
            with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
                pickle.dump( result, pickleFile )
    except TypeError:
        #print( 'error:  failed to save result' )
        pass


#******************************************************************************
#
#  loadUserConstants
#
#******************************************************************************

def loadConstants( ):
    try:
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'constants.pckl.bz2', 'rb' ) ) \
                as pickleFile:
            constants = pickle.load( pickleFile )
    except FileNotFoundError:
        constants = { }

    return constants


#******************************************************************************
#
#  saveConstants
#
#******************************************************************************

def saveConstants( constants ):
    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( getUserDataPath( ) + os.sep + 'constants.pckl.bz2', 'wb' ) ) \
                as pickleFile:
            pickle.dump( constants, pickleFile )


#******************************************************************************
#
#  getCacheFileName
#
#******************************************************************************

@lru_cache( 10 )
def getCacheFileName( name ):
    return getUserDataPath( ) + os.sep + name + '.cache'


#******************************************************************************
#
#  getPrimeCacheFileName
#
#******************************************************************************

@lru_cache( 10 )
def getPrimeCacheFileName( name ):
    return getUserDataPath( ) + os.sep + name + '.cache'


#******************************************************************************
#
#  deleteCache
#
#******************************************************************************

def deleteCache( name ):
    if doesCacheExist( name ):
        os.remove( getCacheFileName( name ) )


#******************************************************************************
#
#  saveToCache
#
#******************************************************************************

def saveToCache( cacheDB, cursor, key, value, commit=True ):
    cursor.execute( '''INSERT INTO cache( id, value ) VALUES( ?, ? )''', ( key, value ) )

    if commit:
        cacheDB.commit( )


#******************************************************************************
#
#  doesCacheExist
#
#******************************************************************************

def doesCacheExist( name ):
    return os.path.isfile( getCacheFileName( name ) )


#******************************************************************************
#
#  createPrimeCache
#
#******************************************************************************

def createPrimeCache( name ):
    cacheDB = sqlite3.connect( getCacheFileName( name ) )

    cursor = cacheDB.cursor( )
    cursor.execute( '''CREATE TABLE cache( id INTEGER PRIMARY KEY, value INTEGER )''' )
    cacheDB.commit( )

    return cacheDB, cursor


#******************************************************************************
#
#  openPrimeCache
#
#******************************************************************************

def openPrimeCache( name ):
    if name not in g.cursors:
        try:
            g.databases[ name ] = sqlite3.connect( getPrimeCacheFileName( name ) )
            g.cursors[ name ] = g.databases[ name ].cursor( )
        except sqlite3.OperationalError:
            raise ValueError( 'prime number table ' + name +
                              ' cannot be found.  Run "preparePrimeData" to create the prime data.' )

    return g.cursors[ name ]


#******************************************************************************
#
#  class PersistentDict
#
#  http://stackoverflow.com/questions/9320463/persistent-memoization-in-python
#
#******************************************************************************

class PersistentDict( MutableMapping ):
    def __init__( self, dbpath, iterable=None, **kwargs ):
        self.dbpath = dbpath

        with self.getConnection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute( 'create table if not exists memo '
                            '(key blob primary key not null, value blob not null)' )

        if iterable is not None:
            self.update( iterable )

        self.update( kwargs )

    @staticmethod
    def encode( obj ):
        return pickle.dumps( obj )

    @staticmethod
    def decode( blob ):
        return pickle.loads( blob )

    def getConnection( self ):
        return sqlite3.connect( self.dbpath )

    def __getitem__( self, key ):
        key = self.encode( key )

        with self.getConnection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute( 'select value from memo where key=?', ( key, ) )

            value = cursor.fetchone( )

        if value is None:
            raise KeyError( key )

        return self.decode( value[ 0 ] )

    def __setitem__( self, key, value ):
        key = self.encode( key )
        value = self.encode( value )

        with self.getConnection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute( 'insert or replace into memo values (?, ?)', ( key, value ) )

    def __delitem__( self, key ):
        key = self.encode( key )

        with self.getConnection( ) as connection:
            cursor = connection.cursor( )

            cursor.execute( 'select count(*) from memo where key=?', ( key, ) )

            if cursor.fetchone( )[ 0 ] == 0:
                raise KeyError( key )

            cursor.execute( 'delete from memo where key=?', ( key, ) )

    def __iter__( self ):
        with self.getConnection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute( 'select key from memo' )

            records = cursor.fetchall( )

        for record in records:
            yield self.decode( record[ 0 ] )

    def __len__( self ):
        with self.getConnection( ) as connection:
            cursor = connection.cursor( )
            cursor.execute( 'select count(*) from memo' )

            return cursor.fetchone( )[ 0 ]


#******************************************************************************
#
#  getUserVariablesFileName
#
#******************************************************************************

@lru_cache( 1 )
def getUserVariablesFileName( ):
    return getUserDataPath( ) + os.sep + PROGRAM_NAME + '_user_variables.cfg'


#******************************************************************************
#
#  getUserFunctionsFileName
#
#******************************************************************************

@lru_cache( 1 )
def getUserFunctionsFileName( ):
    return getUserDataPath( ) + os.sep + PROGRAM_NAME + '_user_functions.cfg'


#******************************************************************************
#
#  getUserConfigurationFileName
#
#******************************************************************************

@lru_cache( 1 )
def getUserConfigurationFileName( ):
    return getUserDataPath( ) + os.sep + PROGRAM_NAME + '_user_config.cfg'


#******************************************************************************
#
#  loadUserVariablesFile
#
#******************************************************************************

def loadUserVariablesFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserVariablesFileName( ) )

    try:
        items = config.items( 'User Variables' )
    except configparser.NoSectionError:
        return

    for item in items:
        g.userVariables[ item[ 0 ] ] = item[ 1 ]


#******************************************************************************
#
#  saveUserVariablesFile
#
#******************************************************************************

def saveUserVariablesFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Variables' ] = { }

    for key in g.userVariables:
        config[ 'User Variables' ][ key ] = str( g.userVariables[ key ] )

    if os.path.isfile( getUserVariablesFileName( ) ):
        copyfile( getUserVariablesFileName( ), getUserVariablesFileName( ) + '.backup' )

    with open( getUserVariablesFileName( ), 'w' ) as userVariablesFile:
        config.write( userVariablesFile )


#******************************************************************************
#
#  openFunctionCache
#
#******************************************************************************

def openFunctionCache( name ):
    if name in g.functionCaches:
        return g.functionCaches[ name ]

    debugPrint( 'opening', name, 'function cache database' )
    g.functionCaches[ name ] = PersistentDict( getCacheFileName( name ) )
    return g.functionCaches[ name ]


#******************************************************************************
#
#  deleteFromFunctionCache
#
#******************************************************************************

#def deleteFromFunctionCache( name, key ):
#    pass
#    #goobles
#    #if name in g.functionCaches:
#    #    return g.functionCaches[ name ]
#    #else:
#    #    debugPrint( 'opening', name, 'function cache database' )
#    #    g.functionCaches[ name ] = PersistentDict( getCacheFileName( name ) )
#    #    return g.functionCaches[ name ]


#******************************************************************************
#
#  cachedFunction
#
#  This is a decorator for any function that wishes to cache its calculations
#  to disk.
#
#******************************************************************************

def cachedFunction( name, overrideIgnore=False ):
    def namedCachedFunction( func ):
        @functools.wraps( func )
        def cacheResults( *args, **kwargs ):
            cache = openFunctionCache( name )

            if not g.ignoreCache or overrideIgnore:
                if ( args, kwargs ) in cache:
                    return cache[ ( args, kwargs ) ]

            result = func( *args, **kwargs )

            if isinstance( result, RPNGenerator ):
                result = list( result )

            if not g.ignoreCache or overrideIgnore:
                cache[ ( args, kwargs ) ] = result

            return result

        return cacheResults

    return namedCachedFunction


#******************************************************************************
#
#  cachedOEISFunction
#
#  This is a modified version of cachedFunction( ) that will ignore (and
#  overwrite) the cached result if it equals 0.  This prevents a failed
#  HTTP connection from polluting the OEIS cache with invalid data.
#
#******************************************************************************

def cachedOEISFunction( name ):
    def namedCachedFunction( func ):
        @functools.wraps( func )
        def cacheResults( *args, **kwargs ):
            cache = openFunctionCache( name )

            if not g.refreshOEISCache:
                if ( args, kwargs ) in cache:
                    result = cache[ ( args, kwargs ) ]

                    if result != 0:
                        return result

            result = func( *args, **kwargs )

            if not g.refreshOEISCache:
                cache[ ( args, kwargs ) ] = result

            return result

        return cacheResults

    return namedCachedFunction


#******************************************************************************
#
#  loadUserConfigurationFile
#
#******************************************************************************

def loadUserConfigurationFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserConfigurationFileName( ) )

    try:
        items = config.items( 'User Configuration' )
    except configparser.NoSectionError:
        return

    for item in items:
        g.userConfiguration[ item[ 0 ] ] = item[ 1 ]


#******************************************************************************
#
#  saveUserConfigurationFile
#
#******************************************************************************

def saveUserConfigurationFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Configuration' ] = { }

    for key in g.userConfiguration:
        config[ 'User Configuration' ][ key ] = g.userConfiguration[ key ]

    if os.path.isfile( getUserConfigurationFileName( ) ):
        copyfile( getUserConfigurationFileName( ), getUserConfigurationFileName( ) + '.backup' )

    with open( getUserConfigurationFileName( ), 'w' ) as userConfigurationFile:
        config.write( userConfigurationFile )

