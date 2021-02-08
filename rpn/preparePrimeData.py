#!/usr/bin/env python

#******************************************************************************
#
#  preparePrimeData.py
#
#  rpnChilada prime number data file compiler
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  *** NOTE:  Don't run this file directly.  Use ../preparePrimeData.py.
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import os
import sqlite3
import time

from rpn.rpnPersistence import createPrimeCache, deleteCache, saveToCache
from rpn.rpnUtils import getSourcePath
from rpn.rpnVersion import PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE

if not hasattr( time, 'time_ns' ):
    from rpn.rpnNanoseconds import time_ns
else:
    from time import time_ns


#******************************************************************************
#
#  preparePrimeData
#
#******************************************************************************

def preparePrimeData( baseName ):
    print( 'processing ' + baseName + '...' )

    inputFileName = getSourcePath( ) + os.sep + baseName + '.txt'

    deleteCache( baseName )
    db, cursor = createPrimeCache( baseName )

    with open( inputFileName, 'r' ) as inputFile:
        for line in inputFile:
            try:
                key, value = line.split( )
                saveToCache( db, cursor, key, value, commit=False )
            except sqlite3.OperationalError:
                print( 'key', key )
                print( 'value', value )
                print( 'parsing error in file ' + inputFileName + ': \'' + line + '\'' )
                break

    db.commit( )
    db.close( )


#******************************************************************************
#
#  main
#
#******************************************************************************

def main( ):
    print( 'preparePrimeData' + PROGRAM_VERSION_STRING + ' - rpnChilada prime number data file converter' )
    print( COPYRIGHT_MESSAGE )
    print( )

    startTime = time_ns( )

    preparePrimeData( 'balanced_primes' )
    preparePrimeData( 'cousin_primes' )
    preparePrimeData( 'double_balanced_primes' )
    preparePrimeData( 'huge_primes' )
    preparePrimeData( 'isolated_primes' )
    preparePrimeData( 'large_primes' )
    preparePrimeData( 'octy_primes' )
    preparePrimeData( 'quadruple_balanced_primes' )
    preparePrimeData( 'quad_primes' )
    preparePrimeData( 'quint_primes' )
    preparePrimeData( 'sext_primes' )
    preparePrimeData( 'sexy_primes' )
    preparePrimeData( 'sexy_quadruplets' )
    preparePrimeData( 'sexy_triplets' )
    preparePrimeData( 'small_primes' )
    preparePrimeData( 'sophie_primes' )
    preparePrimeData( 'triplet_primes' )
    preparePrimeData( 'triple_balanced_primes' )
    preparePrimeData( 'twin_primes' )

    print( )
    print( 'Prime number data prepared.  '
           'Time elapsed:  {:.3f} seconds'.format( ( time_ns( ) - startTime ) / 1000000000 ) )


#******************************************************************************
#
#  __main__
#
#******************************************************************************

if __name__ == '__main__':
    main( )
