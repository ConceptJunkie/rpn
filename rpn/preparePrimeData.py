#!/usr/bin/env python

# //******************************************************************************
# //
# //  preparePrimeData.py
# //
# //  RPN command-line calculator prime number data file compiler
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

import bz2
import contextlib
import os
import pickle

import rpn.rpnGlobals as g

from rpn.rpnPersistence import createPrimeCache, deleteCache, saveToCache
from rpn.rpnUtils import getDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE


# //******************************************************************************
# //
# //  preparePrimeData
# //
# //******************************************************************************

def preparePrimeData( baseName ):
    print( 'processing ' + baseName + '...' )

    inputFileName = g.dataPath + os.sep + baseName + '.txt'

    deleteCache( baseName )
    db, cursor = createPrimeCache( baseName )

    with open( inputFileName, "rU" ) as input:
        for line in input:
            try:
                key, value = line.split( )
                saveToCache( db, cursor, key, value, commit=False )
            except:
                print( 'parsing error in file ' + inputFileName + ': \'' + line + '\'' )

    db.commit( )
    db.close( )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    getDataPath( )

    print( 'preparePrimeData' + PROGRAM_VERSION_STRING + 'RPN command-line calculator help file generator' )
    print( COPYRIGHT_MESSAGE )
    print( )

    preparePrimeData( "balanced_primes" )
    preparePrimeData( "cousin_primes" )
    preparePrimeData( "double_balanced_primes" )
    preparePrimeData( "huge_primes" )
    preparePrimeData( "isolated_primes" )
    preparePrimeData( "large_primes" )
    preparePrimeData( "quad_primes" )
    preparePrimeData( "quint_primes" )
    preparePrimeData( "sext_primes" )
    preparePrimeData( "sexy_primes" )
    preparePrimeData( "sexy_quadruplets" )
    preparePrimeData( "sexy_triplets" )
    preparePrimeData( "small_primes" )
    preparePrimeData( "sophie_primes" )
    preparePrimeData( "super_primes" )
    preparePrimeData( "triplet_primes" )
    preparePrimeData( "triple_balanced_primes" )
    preparePrimeData( "twin_primes" )

    print( )

# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

