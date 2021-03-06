#!/usr/bin/env python

#******************************************************************************
#
#  unpickle.py
#
#******************************************************************************

import bz2
import contextlib
import pickle
import sys


#******************************************************************************
#
#  unpickle
#
#******************************************************************************

def unpickle( fileName ):
    with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
        result = repr( pickle.load( pickleFile ) )
        #print( result.replace( ',', ',\n' ) )
        print( result.replace( ', (', ',\n(' ) )


#******************************************************************************
#
#  __main__
#
#******************************************************************************

if __name__ == '__main__':
    unpickle( sys.argv[ 1 ] )

