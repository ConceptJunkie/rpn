#!/usr/bin/env python

# //******************************************************************************
# //
# //  preparePrimeData.py
# //
# //  RPN command-line calculator prime number data file compiler
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

import rpnGlobals as g


# //******************************************************************************
# //
# //  preparePrimeData
# //
# //******************************************************************************

def preparePrimeData( baseName ):
    print( 'processing ' + baseName + '...' )

    inputFileName = g.dataDir + os.sep + baseName + '.txt'

    with open( inputFileName, "r" ) as input:
        data = eval( input.read( ).replace( '\n', '' ) )

    pickleFileName = g.dataDir + os.sep + baseName + '.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( pickleFileName, 'wb' ) ) as pickleFile:
        pickle.dump( data, pickleFile )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
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

