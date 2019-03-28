#!/usr/bin/env python

# //******************************************************************************
# //
# //  testConvert
# //
# //  test script for RPN unit conversion
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn.rpnTestUtils import *
from rpn.rpnPersistence import loadUnitData
from rpn.rpnUnitClasses import getUnitType

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  runConvertTests
# //
# //******************************************************************************

def runConvertTests( ):
    # unit types... make sure every unit can be converted to every other unit
    if not g.unitOperators:
        loadUnitData( )

    for unit in g.unitOperators:
        unitInfo = g.unitOperators[ unit ]

        baseUnit = g.basicUnitTypes[ getUnitType( unit ) ].baseUnit

        if unit != baseUnit:
            if unitInfo.unitType == 'constant':
                if ( unit, baseUnit ) not in g.unitConversionMatrix:
                    raise ValueError( '( ' + unit + ', ' + baseUnit + ' ) is not found in the unit conversion matrix.' )
                if ( baseUnit, unit ) not in g.unitConversionMatrix:
                    raise ValueError( '( ' + unit + ', ' + baseUnit + ' ) is not found in the unit conversion matrix.' )
            else:
                testOperator( unit + ' ' + baseUnit + ' convert' )

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
    testOperator( 'lux lumen meter sqr / convert' )
    testOperator( 'mach meter/second convert' )
    testOperator( 'maxwell gauss centimeter sqr * convert' )
    testOperator( 'meter*newton newton meter * convert' )
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

    # additional test cases
    testOperator( '16800 mA hours * 5 volts * joule convert' )
    testOperator( '1/coulomb 1/ampere*second convert' )
    testOperator( 'kilogram/meter*second^2 joule/meter^3 convert' )
    testOperator( '34000 square_miles 8 feet 9 mph * / ydhms' )
    testOperator( 'second hertz convert' )
    testOperator( 'day hertz convert' )
    testOperator( 'second daily convert' )
    testOperator( 'day daily convert' )
    testOperator( '30 N 100 m * kWh convert' )
    testOperator( '1 20 range dBm watt convert' )
    testOperator( '0 100 10 range2 dBm watt convert -s1' )
    testOperator( '60 dBm kilowatt convert' )
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
    testOperator( 'coulomb^3/ampere^2*second^2 coulomb convert' )
    testOperator( 'mph miles hourly * convert' )
    testOperator( 'ohm/hertz', 'second/siemens' )
    testOperator( 'elementary_charge sqr [ 4 pi e0 electron_mass c sqr ] product / meter convert' )
    testOperator( 'coulomb^2 ampere^2*second^2 convert' )
    testOperator( 'h eV second * convert' )
    testOperator( 'h_bar c * MeV fm * convert' )
    testOperator( 'h foot*pound-force*second convert' )
    testOperator( '400 W/m^2 stefan_boltzmann / 4 root' )

    # let's check some answers
    expectEqual( 'newton*day kilonewton*second convert', '86.4 kilonewton*second' )
    expectEqual( '3 cups/second gallons/minute convert', '11.25 gallon/minute' )
    expectEqual( 'coulomb/ampere*second', '1' )
    expectEqual( '16800 mA hours * 5 volts * joule convert', '302400 joules' )
    expectEqual( '2 ampere 100 ohms * volts convert', '200 volts' )
    expectEqual( '120 volt 100 ohm / ampere convert', '1.2 amperes' )
    expectEqual( 'day second convert value', '86400' )
    expectEqual( '120 coulombs 10 ampere / second convert', '12 seconds' )
    expectEqual( '1 kilowatt 1 decavolt / ampere convert', '100 amperes' )
    expectEqual( '1 watt 1 ohm / ampere sqr convert', '1 ampere^2' )
    expectEqual( '50 watts 5 amperes^2 / ohm convert', '10 ohms' )
    expectEqual( '120 volts^2 50 watts / ohms convert', '2.4 ohms' )
    expectEqual( '200 ohms 4 watts * volts^2 convert', '800 volts^2' )
    expectEqual( '1 kilowatt 10 ohms / sqrt', '10 amperes' )
    expectEqual( 'volt meter / newton coulomb / convert', '1 newton coulomb /' )

    # unit exponentiation
    testOperator( '8 floz inch 3 ** convert' )
    testOperator( 'foot 4 power square_inch sqr convert' )

    # lists of units
    testOperator( '0 5000 284 range2 seconds [ hour minute second ] convert -s1' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runConvertTests( )

