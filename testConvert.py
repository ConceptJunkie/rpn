# //******************************************************************************
# //
# //  testConvert
# //
# //  test script for RPN unit conversion
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
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
    testRPN( 'rpn barn gigaparsec * cubic_inch convert' )
    testRPN( 'rpn c m/s convert' )
    testRPN( 'rpn earth_radius 2 pi * * miles convert' )
    testRPN( 'rpn gallon cup convert' )
    testRPN( 'rpn marathon miles convert' )
    testRPN( 'rpn marathon [ miles feet ] convert' )
    testRPN( 'rpn mph miles hour / convert' )
    testRPN( 'rpn 65 miles hour / furlongs fortnight / convert' )

    # compound units
    testRPN( 'rpn watt second * watt-second convert' )
    testRPN( 'rpn second watt * watt-second convert' )
    testRPN( 'rpn watt-second watt second * convert' )
    testRPN( 'rpn watt-second second watt * convert' )

    # complicated conversions
    testRPN( 'rpn 16800 mA hours * 5 volts * joule convert' )

    # unit exponentiation
    testRPN( 'rpn 8 floz inch 3 ** convert' )
    testRPN( 'rpn foot 4 power square_inch sqr convert' )

