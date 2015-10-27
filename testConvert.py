#!/usr/bin/env python

# //******************************************************************************
# //
# //  testConvert
# //
# //  test script for RPN unit conversion
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn import rpn

from rpnTestUtils import *


# //******************************************************************************
# //
# //  runConvertTests
# //
# //******************************************************************************

def runConvertTests( ):
    testOperator( 'barn gigaparsec * cubic_inch convert' )
    testOperator( 'c m/s convert' )
    testOperator( 'earth_radius 2 pi * * miles convert' )
    testOperator( 'gallon cup convert' )
    testOperator( 'marathon miles convert' )
    testOperator( 'marathon [ miles feet ] convert' )
    testOperator( 'mph miles hour / convert' )
    testOperator( '65 miles hour / furlongs fortnight / convert' )

    # compound units
    testOperator( 'watt second * watt-second convert' )
    testOperator( 'second watt * watt-second convert' )
    testOperator( 'watt-second watt second * convert' )
    testOperator( 'watt-second second watt * convert' )

    # complicated conversions
    testOperator( '16800 mA hours * 5 volts * joule convert' )

    # unit exponentiation
    testOperator( '8 floz inch 3 ** convert' )
    testOperator( 'foot 4 power square_inch sqr convert' )

