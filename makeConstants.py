#!/usr/bin/env python

# //******************************************************************************
# //
# //  makeConstants.py
# //
# //  RPN command-line calculator constant compiler
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

import bz2
import codecs
import contextlib
import itertools
import os
import pickle
import re as regex

from collections import namedtuple

from mpmath import *

#  This has to go here so the mpf's in the import get created with 50 places of precision.
mp.dps = 50

from rpnMeasurement import *
from rpnPersistence import *
from rpnUnits import *
from rpnVersion import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'makeConstants'
PROGRAM_DESCRIPTION = 'RPN command-line calculator constant compiler'


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    print( PROGRAM_NAME + PROGRAM_VERSION_STRING + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    g.dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + g.dataDir

    lineCount = 0

    definitions = { }

    errors = False

    Definition = namedtuple( 'Definition', [ 'line', 'value', 'units', 'reference' ] )

    # compile the data file

    for line in codecs.open( 'rpnConstants.txt', 'rU', 'ascii', 'replace' ):
        lineCount += 1

        line = line.rstrip( )
        comment = line.find( '#' )

        if comment >= 0:
            line = line[ : comment ]

        tokens = regex.split( ' +', line )

        tokenCount = len( tokens )

        if tokenCount == 0:
            continue
        elif tokenCount == 1 and tokens[ 0 ] == '' :
            continue
        elif ( 2 > tokenCount > 5 ) or ( tokens[ 1 ] != '=' ):
            print( 'error parsing line ' + str( lineCount ) + ':' )
            print( line )
            print( )
            errors = True

        name = tokens[ 0 ]
        value = tokens[ 2 ]

        if tokenCount > 3:
            units = tokens[ 3 ]
        else:
            units = ''

        if not name.isidentifier( ):
            print( 'invalid identifier \'' + name + '\' on line ' + str( lineCount ) )
            print( )
            errors = True

        if name in definitions:
            print( 'duplicate identifier \'' + name + '\' on line ' + str( lineCount ) +
                   ' (originally defined on line ' + str( definitions[ name ].line ) + ')' )
            print( )
            errors = True

        definitions[ name ] = Definition( lineCount, value, units, False )

    if errors:
        return

    constants = { }

    # first parsing pass
    for name in definitions:
        try:
            value = mpmathify( definitions[ name ].value )
        except:
            value = 'parse me'

        if value == 'parse me':
            continue

        if definitions[ name ].units == '':
            constants[ name ] = value
        else:
            constants[ name ] = RPNMeasurement( value, definitions[ name ].units )

        print( constants[ name ] )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

