#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPhysics.py
# //
# //  RPN command-line calculator physics operators
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import struct

from rpnConstants import getNewtonsConstant, getSpeedOfLight
from rpnGenerator import RPNGenerator
from rpnList import getProduct
from rpnMath import exponentiate
from rpnMeasurement import RPNMeasurement, validateUnits
from rpnUtils import real_int

import rpnGlobals as g


# //******************************************************************************
# //
# //  getSchwarzchildRadius
# //
# //******************************************************************************

def getSchwarzchildRadius( mass ):
    validateUnits( mass, 'mass' )

    return getProduct( [ 2, getNewtonsConstant( ), mass ] ).divide( exponentiate( getSpeedOfLight( ), 2 ) )


