#!/usr/bin/env python

# //******************************************************************************
# //
# //  testConvert
# //
# //  test script for RPN unit conversion
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpnTestUtils import *


# //******************************************************************************
# //
# //  runConvertTests
# //
# //******************************************************************************

def runConvertTests( ):
    testOperator( 'barn gigaparsec * cubic_inch convert' )
    testOperator( 'earth_radius 2 pi * * miles convert' )
    testOperator( 'gallon cup convert' )
    testOperator( 'marathon miles convert' )
    testOperator( 'marathon [ miles feet ] convert' )
    testOperator( 'mph miles hour / convert' )
    testOperator( 'miles hour / mph convert' )
    testOperator( '65 miles hour / furlongs fortnight / convert' )

    # compound units
    testOperator( 'watt second * watt-second convert' )
    testOperator( 'second watt * watt-second convert' )
    testOperator( 'watt-second watt second * convert' )
    testOperator( 'watt-second second watt * convert' )

    # complicated conversions
    # testOperator( '16800 mA hours * 5 volts * joule convert' )

    # unit exponentiation
    testOperator( '8 floz inch 3 ** convert' )
    testOperator( 'foot 4 power square_inch sqr convert' )

    # lists of units
    testOperator( '1 20 range dBm watt convert' )
    testOperator( '0 5000 284 range2 seconds [ hour minute second ] convert -s1' )

