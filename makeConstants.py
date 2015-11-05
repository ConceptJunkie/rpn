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

from mpmath import *

#  This has to go here so the mpf's in the import get created with 50 places of precision.
mp.dps = 50

from rpnUnits import *
from rpnVersion import *


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

    lineCount = 0

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

        name = token[ 0 ]
        value = token[ 2 : ]


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

