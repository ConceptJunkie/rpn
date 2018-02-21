#!/usr/bin/env python

# //******************************************************************************
# //
# //  testConvert
# //
# //  test script for RPN unit conversion
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn.rpnTestUtils import *


# //******************************************************************************
# //
# //  runConvertTests
# //
# //******************************************************************************

def runConvertTests( ):
    testOperator( 'barn gigaparsec * cubic_inch convert' )
    testOperator( 'cubic_inch barn gigaparsec * convert' )
    testOperator( 'earth_radius 2 pi * * miles convert' )
    testOperator( 'gallon cup convert' )
    testOperator( 'marathon miles convert' )
    testOperator( 'marathon [ miles feet ] convert' )
    testOperator( 'mph miles hour / convert' )
    testOperator( 'miles hour / mph convert' )
    testOperator( '65 miles hour / furlongs fortnight / convert' )
    testOperator( '1 watt dBm convert' )

    # compound units
    testOperator( 'ampere coulomb/second convert' )
    testOperator( 'btupf joule/kelvin convert' )
    testOperator( 'candela meter sqr / lambert convert' )
    testOperator( 'clausius joule/kelvin convert' )
    testOperator( 'coulomb/farad volt convert' )
    testOperator( 'coulomb/kilogram roentgen convert' )
    testOperator( 'coulomb/volt farad convert' )
    testOperator( 'footcandle lumen square_foot / convert' )
    testOperator( 'footlambert candela square_meter / convert' )
    testOperator( 'galileo meter second sqr / convert' )
    testOperator( 'gauss maxwell centimeter sqr / convert' )
    testOperator( 'gray joule/kilogram convert' )
    testOperator( 'henry weber/ampere convert' )
    testOperator( 'joule kilogram meter sqr * second sqr / convert' )
    testOperator( 'joule pascal meter cubed * convert' )
    testOperator( 'joule/second watt convert' )
    testOperator( 'kine meter/second convert' )
    testOperator( 'light meter/second convert' )
    testOperator( 'lux lumen meter sqr / convert' )
    testOperator( 'mach meter/second convert' )
    testOperator( 'maxwell gauss centimeter sqr * convert' )
    testOperator( 'meter-newton newton meter * convert' )
    testOperator( 'nat joule/kelvin convert' )
    testOperator( 'newton joule/meter convert' )
    testOperator( 'newton kilogram meter * second sqr / convert' )
    testOperator( 'newton meter sqr / pascal convert' )
    testOperator( 'newton second * meter sqr / pascal-second convert' )
    testOperator( 'nit candela meter sqr / convert' )
    testOperator( 'oc1 bit/second convert' )
    testOperator( 'oersted ampere/meter convert' )
    testOperator( 'ohm joule second * coulomb sqr / convert' )
    testOperator( 'ohm kilogram meter sqr * second cubed ampere sqr * / convert' )
    testOperator( 'ohm second/farad convert' )
    testOperator( 'ohm volt/ampere convert' )
    testOperator( 'ohm watt ampere sqr / convert' )
    testOperator( 'pascal kilogram meter second sqr * / convert' )
    testOperator( 'pascal second * kilogram meter second * / convert' )
    testOperator( 'second watt * watt-second convert' )
    testOperator( 'siemens ampere/volt convert' )
    testOperator( 'siemens second cubed ampere sqr * kilogram meter sqr * / convert' )
    testOperator( 'stilb candela meter sqr / convert' )
    testOperator( 'tesla kilogram ampere second sqr * / convert' )
    testOperator( 'tesla volt second * meter sqr / convert' )
    testOperator( 'tesla weber meter sqr / convert' )
    testOperator( 'watt erg/second convert' )
    testOperator( 'watt joule/second convert' )
    testOperator( 'watt kilogram meter sqr * second cubed / convert' )
    testOperator( 'watt newton meter * second / convert' )
    testOperator( 'watt second * watt-second convert' )
    testOperator( 'watt-second second watt * convert' )
    testOperator( 'watt-second watt second * convert' )
    testOperator( 'weber tesla meter sqr * convert' )

    # complicated conversions
    testOperator( '16800 mA hours * 5 volts * joule convert' )

    # unit exponentiation
    testOperator( '8 floz inch 3 ** convert' )
    testOperator( 'foot 4 power square_inch sqr convert' )

    # lists of units
    testOperator( '1 20 range dBm watt convert' )
    testOperator( '0 5000 284 range2 seconds [ hour minute second ] convert -s1' )

    # special conversions tests
    testOperator( '0 100 10 range2 dBm watt convert -s1' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runConvertTests( )

