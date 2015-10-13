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
from testRPN import testRPN


# //******************************************************************************
# //
# //  runConvertTests
# //
# //******************************************************************************

def runConvertTests( ):
    testRPN( 'barn gigaparsec * cubic_inch convert' )
    testRPN( 'c m/s convert' )
    testRPN( 'earth_radius 2 pi * * miles convert' )
    testRPN( 'gallon cup convert' )
    testRPN( 'marathon miles convert' )
    testRPN( 'marathon [ miles feet ] convert' )
    testRPN( 'mph miles hour / convert' )
    testRPN( '65 miles hour / furlongs fortnight / convert' )

    # compound units
    testRPN( 'watt second * watt-second convert' )
    testRPN( 'second watt * watt-second convert' )
    testRPN( 'watt-second watt second * convert' )
    testRPN( 'watt-second second watt * convert' )

    # complicated conversions
    testRPN( '16800 mA hours * 5 volts * joule convert' )

    # unit exponentiation
    testRPN( '8 floz inch 3 ** convert' )
    testRPN( 'foot 4 power square_inch sqr convert' )

