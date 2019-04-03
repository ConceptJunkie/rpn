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
    testOperator( 'lumen candela*steradian' )
    testOperator( 'candela*steradian lumen' )

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
    testOperator( 'second^2/henry farad convert' )
    testOperator( 'farad second^2/henry convert' )
    testOperator( 'second^2/farad henry convert' )
    testOperator( 'henry second^2/farad convert' )
    testOperator( 'coulomb/volt farad convert' )
    testOperator( 'farad coulomb/volt convert' )
    testOperator( 'ampere*second/volt farad convert' )
    testOperator( 'farad ampere*second/volt convert' )
    testOperator( 'farad 1/hertz*ohm convert' )
    testOperator( 'farad joule/volt^2 convert' )
    testOperator( 'farad meter*newton/volt^2 convert' )
    testOperator( 'farad second*watt/volt^2 convert' )
    testOperator( 'farad second/ohm convert' )
    testOperator( '1/hertz*ohm farad convert' )
    testOperator( 'joule/volt^2 farad convert' )
    testOperator( 'meter*newton/volt^2 farad convert' )
    testOperator( 'second*watt/volt^2 farad convert' )
    testOperator( 'second/ohm farad convert' )
    testOperator( 'coulomb ampere*second convert' )
    testOperator( 'coulomb farad*volt convert' )
    testOperator( 'coulomb joule/volt convert' )
    testOperator( 'ampere*second coulomb convert' )
    testOperator( 'farad*volt coulomb convert' )
    testOperator( 'joule/volt coulomb convert' )
    testOperator( 'coulomb/second ampere convert' )
    testOperator( 'ampere coulomb/second convert' )
    testOperator( 'watt/volt ampere convert' )
    testOperator( 'ampere watt/volt convert' )
    testOperator( 'siemens ampere/volt convert' )
    testOperator( 'siemens coulomb^2*second/kilogram*meter^2 convert' )
    testOperator( 'ampere/volt siemens convert' )
    testOperator( 'coulomb^2*second/kilogram*meter^2 siemens convert' )
    testOperator( 'coulomb/farad volt convert' )
    testOperator( 'joule/coulomb volt convert' )
    testOperator( 'watt/ampere volt convert' )
    testOperator( 'volt coulomb/farad convert' )
    testOperator( 'volt joule/coulomb convert' )
    testOperator( 'volt watt/ampere convert' )
    testOperator( 'watt meter*newton/second convert' )
    testOperator( 'meter*newton/second watt convert' )
    testOperator( 'watt ampere*volt convert' )
    testOperator( 'ampere*volt watt convert' )
    testOperator( 'erg/second watt convert' )
    testOperator( 'joule/second watt convert' )
    testOperator( 'watt erg/second convert' )
    testOperator( 'watt joule/second convert' )
    testOperator( 'joule*second/coulomb^2 ohm convert' )
    testOperator( 'joule/ampere^2*second ohm convert' )
    testOperator( 'second/farad ohm convert' )
    testOperator( 'volt/ampere ohm convert' )
    testOperator( 'watt/ampere^2 ohm convert' )
    testOperator( 'ohm joule*second/coulomb^2 convert' )
    testOperator( 'ohm joule/ampere^2*second convert' )
    testOperator( 'ohm second/farad convert' )
    testOperator( 'ohm volt/ampere convert' )
    testOperator( 'ohm watt/ampere^2 convert' )
    testOperator( 'kilogram/meter*second pascal*second convert' )
    testOperator( 'newton*second/meter^2 pascal*second convert' )
    testOperator( 'pascal*second kilogram/meter*second convert' )
    testOperator( 'pascal*second newton*second/meter^2 convert' )
    testOperator( 'newton/meter^2 pascal convert' )
    testOperator( 'pascal newton/meter^2 convert' )
    testOperator( 'ampere*second*volt joule convert' )
    testOperator( 'joule ampere*second*volt convert' )
    testOperator( 'meter*newton joule convert' )
    testOperator( 'meter^3*pascal joule convert' )
    testOperator( 'joule meter*newton convert' )
    testOperator( 'joule meter^3*pascal convert' )
    testOperator( 'coulomb*volt joule convert' )
    testOperator( 'second*watt joule convert' )
    testOperator( 'joule coulomb*volt convert' )
    testOperator( 'joule second*watt convert' )
    testOperator( 'horsepower*second joule convert' )
    testOperator( 'joule horsepower*second convert' )
    testOperator( 'lux lumen/foot^2 convert' )
    testOperator( 'lumen/foot^2 lux convert' )
    testOperator( 'joule/ampere^2 henry convert' )
    testOperator( 'ohm*second henry convert' )
    testOperator( 'ohm/hertz henry convert' )
    testOperator( 'weber/ampere henry convert' )
    testOperator( 'henry joule/ampere^2 convert' )
    testOperator( 'henry ohm*second convert' )
    testOperator( 'henry ohm/hertz convert' )
    testOperator( 'henry weber/ampere convert' )
    testOperator( 'joule/kilogram meter^2/second^2 convert' )
    testOperator( 'meter^2/second^2 joule/kilogram convert' )
    testOperator( 'joule/kilogram gray convert' )
    testOperator( 'gray joule/kilogram convert' )
    testOperator( 'meter^2/second^2 gray convert' )
    testOperator( 'gray meter^2/second^2 convert' )
    testOperator( 'kilogram/second^3 watt/meter^2' )
    testOperator( 'watt/meter^2 kilogram/second^3' )
    testOperator( 'tesla kilogram/coulomb*second convert' )
    testOperator( 'tesla joule/ampere*meter^2 convert' )
    testOperator( 'tesla ampere*henry/meter^2 convert' )
    testOperator( 'tesla maxwell/centimeter^2 convert' )
    testOperator( 'tesla newton/ampere*meter convert' )
    testOperator( 'tesla newton*second/coulomb*meter convert' )
    testOperator( 'tesla second*volt/meter^2 convert' )
    testOperator( 'tesla weber/meter^2 convert' )
    testOperator( 'kilogram/coulomb*second tesla convert' )
    testOperator( 'joule/ampere*meter^2 tesla convert' )
    testOperator( 'ampere*henry/meter^2 tesla convert' )
    testOperator( 'maxwell/centimeter^2 tesla convert' )
    testOperator( 'newton/ampere*meter tesla convert' )
    testOperator( 'newton*second/coulomb*meter tesla convert' )
    testOperator( 'second*volt/meter^2 tesla convert' )
    testOperator( 'weber/meter^2 tesla convert' )
    testOperator( 'second*volt weber convert' )
    testOperator( 'meter^2*tesla weber convert' )
    testOperator( 'centimeter^2*gauss weber convert' )
    testOperator( 'weber second*volt convert' )
    testOperator( 'weber meter^2*tesla convert' )
    testOperator( 'weber centimeter^2*gauss convert' )
    testOperator( 'newton ampere*weber/meter convert' )
    testOperator( 'newton joule/meter convert' )
    testOperator( 'ampere*weber/meter newton convert' )
    testOperator( 'joule/meter newton convert' )
    testOperator( 'poise pascal*second convert' )
    testOperator( 'pascal*second poise convert' )

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

