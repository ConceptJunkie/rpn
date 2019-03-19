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

    # unit types... make sure every unit can be converted to every other unit

    # acceleration
    testOperator( 'galileo meter/second*second convert' )
    testOperator( 'leo meter/second*second convert' )
    testOperator( 'meter/second^2 meter/second*second convert' )

    # amount_of_substance - There's only one unit here!

    # angle
    testOperator( 'arcminute radian convert' )
    testOperator( 'arcsecond radian convert' )
    testOperator( 'centrad radian convert' )
    testOperator( 'circle radian convert' )
    testOperator( 'degree radian convert' )
    testOperator( 'furman radian convert' )
    testOperator( 'grad radian convert' )
    testOperator( 'octant radian convert' )
    testOperator( 'pointangle radian convert' )
    testOperator( 'quadrant radian convert' )
    testOperator( 'quintant radian convert' )
    testOperator( 'sextant radian convert' )
    testOperator( 'streck radian convert' )

    # area
    testOperator( 'acre meter*meter convert' )
    testOperator( 'are meter*meter convert' )
    testOperator( 'barn meter*meter convert' )
    testOperator( 'bovate meter*meter convert' )
    testOperator( 'carucate meter*meter convert' )
    testOperator( 'homestead meter*meter convert' )
    testOperator( 'imperial_square meter*meter convert' )
    testOperator( 'morgen meter*meter convert' )
    testOperator( 'nanoacre meter*meter convert' )
    testOperator( 'outhouse meter*meter convert' )
    testOperator( 'rood meter*meter convert' )
    testOperator( 'section meter*meter convert' )
    testOperator( 'shed meter*meter convert' )
    testOperator( 'square_foot meter*meter convert' )
    testOperator( 'square_meter meter*meter convert' )
    testOperator( 'square_yard meter*meter convert' )
    testOperator( 'township meter*meter convert' )
    testOperator( 'virgate meter*meter convert' )

    # capacitance
    #testOperator( '1/ohm*hertz farad convert' )
    testOperator( 'abfarad farad convert' )
    testOperator( 'ampere*second/volt farad convert' )
    testOperator( 'coulomb/volt farad convert' )
    testOperator( 'coulomb^2/joule farad convert' )
    testOperator( 'coulomb^2/newton*meter farad convert' )
    testOperator( 'jar farad convert' )
    testOperator( 'joule/volt^2 farad convert' )
    testOperator( 'newton*meter/volt^2 farad convert' )
    testOperator( 'second/ohm farad convert' )
    testOperator( 'second^2*coulomb^2/meter^2*kilogram farad convert' )
    testOperator( 'second^2/henry farad convert' )
    testOperator( 'second^4*ampere^2/meter^2*kilogram farad convert' )
    testOperator( 'statfarad farad convert' )
    testOperator( 'watt*second/volt^2 farad convert' )

    # charge
    testOperator( 'abcoulomb coulomb convert' )
    testOperator( 'ampere*second coulomb convert' )
    testOperator( 'farad*volt coulomb convert' )
    testOperator( 'franklin coulomb convert' )
    testOperator( 'faraday coulomb convert' )
    testOperator( 'joule/volt coulomb convert' )
    testOperator( 'statcoulomb coulomb convert' )

    # constant - This is a special unit type that can't be converted.

    # current
    testOperator( 'abampere ampere convert' )
    testOperator( 'coulomb/second ampere convert' )
    testOperator( 'statampere ampere convert' )
    testOperator( 'watt/volt ampere convert' )

    # data_rate
    testOperator( 'byte/second bit/second convert' )
    testOperator( 'oc1 bit/second convert' )
    testOperator( 'oc3 bit/second convert' )
    testOperator( 'oc12 bit/second convert' )
    testOperator( 'oc24 bit/second convert' )
    testOperator( 'oc48 bit/second convert' )
    testOperator( 'oc192 bit/second convert' )
    testOperator( 'oc768 bit/second convert' )
    testOperator( 'usb1 bit/second convert' )
    testOperator( 'usb2 bit/second convert' )
    testOperator( 'usb3.0 bit/second convert' )
    testOperator( 'usb3.1 bit/second convert' )

    # density
    testOperator( 'kilogram/liter kilogram/meter*meter*meter convert' )

    # dynamic_viscosity
    #testOperator( 'kilogram/meter*second pascal*second convert' )
    testOperator( 'newton*second/meter*meter pascal*second convert' )
    testOperator( 'poise pascal*second convert' )
    testOperator( 'reynolds pascal*second convert' )

    # electrical_conductance
    testOperator( 'abmho siemens convert' )
    testOperator( 'ampere/volt siemens convert' )
    testOperator( 'conductance_quantum siemens convert' )
    testOperator( 'ampere*ampere*second*second*second/kilogram*meter*meter siemens convert' )
    testOperator( 'coulomb*coulomb*second/kilogram*meter*meter siemens convert' )
    testOperator( 'siemens siemens convert' )
    testOperator( 'statmho siemens convert' )
    testOperator( 'statsiemens siemens convert' )

    # electric_potential
    testOperator( 'abvolt volt convert' )
    testOperator( 'coulomb/farad volt convert' )
    testOperator( 'watt/ampere volt convert' )
    testOperator( 'statvolt volt convert' )

    # electrical_resistance
    #testOperator( '1/siemens ohm convert' )
    testOperator( 'abohm ohm convert' )
    testOperator( 'german_mile ohm convert' )
    testOperator( 'jacobi ohm convert' )
    testOperator( 'joule*second/coulomb*coulomb ohm convert' )
    testOperator( 'joule/ampere*ampere*second ohm convert' )
    testOperator( 'kilogram*meter*meter/ampere*ampere*second*second*second ohm convert' )
    testOperator( 'matthiessen ohm convert' )
    testOperator( 'second/farad ohm convert' )
    testOperator( 'statohm ohm convert' )
    testOperator( 'varley ohm convert' )
    testOperator( 'volt/ampere ohm convert' )
    testOperator( 'watt/ampere*ampere ohm convert' )

    # energy
    testOperator( 'ampere*second*volt joule convert' )
    testOperator( 'btu joule convert' )
    testOperator( 'calorie joule convert' )
    testOperator( 'electron-volt joule convert' )
    testOperator( 'erg joule convert' )
    testOperator( 'foe joule convert' )
    testOperator( 'gram-equivalent joule convert' )
    testOperator( 'hartree joule convert' )
    testOperator( 'horsepower*second joule convert' )
    testOperator( 'kilogram*meter*meter/second*second joule convert' )
    testOperator( 'meter*newton joule convert' )
    testOperator( 'meter^3*pascal joule convert' )
    testOperator( 'pound_of_TNT joule convert' )
    testOperator( 'quad joule convert' )
    testOperator( 'rydberg joule convert' )
    testOperator( 'therm joule convert' )
    testOperator( 'toe joule convert' )
    testOperator( 'ton_of_coal joule convert' )
    testOperator( 'ton_of_TNT joule convert' )
    testOperator( 'volt*coulomb joule convert' )
    testOperator( 'watt*second joule convert' )

    # force
    testOperator( 'amp*weber/meter newton convert' )
    testOperator( 'dyne newton convert' )
    testOperator( 'gram-force newton convert' )
    testOperator( 'joule/meter newton convert' )
    testOperator( 'kilogram*meter/second*second newton convert' )
    testOperator( 'pond newton convert' )
    testOperator( 'pound*foot/second*second newton convert' )
    testOperator( 'poundal newton convert' )
    testOperator( 'sthene newton convert' )

    # frequency
    #testOperator( '1/second hertz convert' )
    testOperator( 'every_minute hertz convert' )
    testOperator( 'every_second hertz convert' )
    testOperator( 'hourly hertz convert' )
    testOperator( 'daily hertz convert' )
    testOperator( 'weekly hertz convert' )
    testOperator( 'monthly hertz convert' )
    testOperator( 'yearly hertz convert' )
    testOperator( 'becquerel hertz convert' )
    testOperator( 'curie hertz convert' )
    testOperator( 'rutherford hertz convert' )

    # illuminance
    testOperator( 'flame lux convert' )
    testOperator( 'footcandle lux convert' )
    testOperator( 'lumen/meter*meter lux convert' )
    testOperator( 'lumen/foot*foot lux convert' )
    testOperator( 'nox lux convert' )
    testOperator( 'phot lux convert' )

    # inductance
    testOperator( 'abhenry henry convert' )
    testOperator( 'joule/ampere^2 henry convert' )
    testOperator( 'kilogram*meter^2/coulomb^2 henry convert' )
    testOperator( 'kilogram*meter^2/second^2*ampere^2 henry convert' )
    testOperator( 'ohm*second henry convert' )
    testOperator( 'ohm/hertz henry convert' )
    testOperator( 'second^2/farad henry convert' )
    testOperator( 'stathenry henry convert' )
    testOperator( 'weber/ampere henry convert' )

    # information_entropy
    testOperator( 'ban bit convert' )
    testOperator( 'byte bit convert' )
    testOperator( 'btupf bit convert' )
    testOperator( 'clausius bit convert' )
    testOperator( 'dword bit convert' )
    testOperator( 'joule/kelvin bit convert' )
    testOperator( 'library_of_congress bit convert' )
    testOperator( 'nibble bit convert' )
    testOperator( 'nat bit convert' )
    testOperator( 'nyp bit convert' )
    testOperator( 'oword bit convert' )
    testOperator( 'qword bit convert' )
    testOperator( 'trit bit convert' )
    testOperator( 'tryte bit convert' )
    testOperator( 'word bit convert' )

    # jerk
    testOperator( 'stapp meter/second*second*second convert' )

    # jounce - There's only 1 jounce unit!

    # length
    testOperator( 'aln meter convert' )
    testOperator( 'angstrom meter convert' )
    testOperator( 'arpent meter convert' )
    testOperator( 'arshin meter convert' )
    testOperator( 'astronomical_unit meter convert' )
    testOperator( 'barleycorn meter convert' )
    testOperator( 'bolt meter convert' )
    testOperator( 'caliber meter convert' )
    testOperator( 'chain meter convert' )
    testOperator( 'cicero meter convert' )
    testOperator( 'cubit meter convert' )
    testOperator( 'diuym meter convert' )
    testOperator( 'ell meter convert' )
    testOperator( 'famn meter convert' )
    testOperator( 'farshimmelt_potrzebie meter convert' )
    testOperator( 'fathom meter convert' )
    testOperator( 'finger meter convert' )
    testOperator( 'fingerbreadth meter convert' )
    testOperator( 'foot meter convert' )
    testOperator( 'french meter convert' )
    testOperator( 'furlong meter convert' )
    testOperator( 'furshlugginer_potrzebie meter convert' )
    testOperator( 'fut meter convert' )
    testOperator( 'greek_cubit meter convert' )
    testOperator( 'gutenberg meter convert' )
    testOperator( 'hand meter convert' )
    testOperator( 'handbreadth meter convert' )
    testOperator( 'hubble meter convert' )
    testOperator( 'inch meter convert' )
    testOperator( 'ken meter convert' )
    testOperator( 'kosaya_sazhen meter convert' )
    testOperator( 'kyu meter convert' )
    testOperator( 'league meter convert' )
    testOperator( 'light-second meter convert' )
    testOperator( 'light-year meter convert' )
    testOperator( 'liniya meter convert' )
    testOperator( 'link meter convert' )
    testOperator( 'long_cubit meter convert' )
    testOperator( 'long_reed meter convert' )
    testOperator( 'marathon meter convert' )
    testOperator( 'mezhevaya_versta meter convert' )
    testOperator( 'metric_foot meter convert' )
    testOperator( 'micron meter convert' )
    testOperator( 'mil meter convert' )
    testOperator( 'mile meter convert' )
    testOperator( 'nail meter convert' )
    testOperator( 'nautical_mile meter convert' )
    testOperator( 'parsec meter convert' )
    testOperator( 'perch meter convert' )
    testOperator( 'pica meter convert' )
    testOperator( 'point meter convert' )
    testOperator( 'poppyseed meter convert' )
    testOperator( 'pyad meter convert' )
    testOperator( 'rack_unit meter convert' )
    testOperator( 'reed meter convert' )
    testOperator( 'rod meter convert' )
    testOperator( 'rope meter convert' )
    testOperator( 'potrzebie meter convert' )
    testOperator( 'sazhen meter convert' )
    testOperator( 'siriometer meter convert' )
    testOperator( 'skein meter convert' )
    testOperator( 'smoot meter convert' )
    testOperator( 'span meter convert' )
    testOperator( 'stadium meter convert' )
    testOperator( 'twip meter convert' )
    testOperator( 'vershok meter convert' )
    testOperator( 'versta meter convert' )
    testOperator( 'yard meter convert' )

    # luminance
    testOperator( 'apostilb candela/meter*meter convert' )
    testOperator( 'bril candela/meter*meter convert' )
    testOperator( 'footlambert candela/meter*meter convert' )
    testOperator( 'lambert candela/meter*meter convert' )
    testOperator( 'nit candela/meter*meter convert' )
    testOperator( 'skot candela/meter*meter convert' )
    testOperator( 'stilb candela/meter*meter convert' )

    # luminous_flux
    testOperator( 'candela*steradian lumen convert' )

    # luminous_intensity
    testOperator( 'hefnerkerze candela convert' )

    # magnetic_field_strength
    testOperator( 'oersted ampere/meter convert' )

    # magnetic_flux
    testOperator( 'centimeter*centimeter*gauss weber convert' )
    testOperator( 'magnetic_flux_quantum weber convert' )
    testOperator( 'maxwell weber convert' )
    testOperator( 'volt*second weber convert' )
    testOperator( 'unit_pole weber convert' )
    testOperator( 'meter*meter*tesla weber convert' )

    # magnetic_flux_density
    testOperator( 'gauss tesla convert' )
    testOperator( 'henry*ampere/meter^2 tesla convert' )
    testOperator( 'joule/ampere*meter^2 tesla convert' )
    testOperator( 'kilogram/ampere*second*second tesla convert' )
    testOperator( 'kilogram/coulomb*second tesla convert' )
    testOperator( 'maxwell/centimeter*centimeter tesla convert' )
    testOperator( 'newton*second/coulomb*meter tesla convert' )
    testOperator( 'newton/ampere*meter tesla convert' )
    testOperator( 'second*volt/meter*meter tesla convert' )
    testOperator( 'volt*second/meter^2 tesla convert' )
    testOperator( 'weber/meter*meter tesla convert' )

    # mass
    testOperator( 'berkovets gram convert' )
    testOperator( 'blintz gram convert' )
    testOperator( 'carat gram convert' )
    testOperator( 'chandrasekhar_limit gram convert' )
    testOperator( 'dalton gram convert' )
    testOperator( 'dolya gram convert' )
    testOperator( 'doppelzentner gram convert' )
    testOperator( 'farshimmelt_blintz gram convert' )
    testOperator( 'funt gram convert' )
    testOperator( 'furshlugginer_blintz gram convert' )
    testOperator( 'grain gram convert' )
    testOperator( 'joule*second*second/meter*meter gram convert' )
    testOperator( 'kip gram convert' )
    testOperator( 'lot gram convert' )
    testOperator( 'ounce gram convert' )
    testOperator( 'pennyweight gram convert' )
    testOperator( 'pfund gram convert' )
    testOperator( 'pood gram convert' )
    testOperator( 'pound gram convert' )
    testOperator( 'quintal gram convert' )
    testOperator( 'sheet gram convert' )
    testOperator( 'slinch gram convert' )
    testOperator( 'slug gram convert' )
    testOperator( 'stone gram convert' )
    testOperator( 'stone_us gram convert' )
    testOperator( 'ton gram convert' )
    testOperator( 'tonne gram convert' )
    testOperator( 'troy_ounce gram convert' )
    testOperator( 'troy_pound gram convert' )
    testOperator( 'wey gram convert' )
    testOperator( 'zentner gram convert' )
    testOperator( 'zolotnik gram convert' )

    # power
    testOperator( 'ampere*volt watt convert' )
    testOperator( 'dBm watt convert' )
    testOperator( 'erg/second watt convert' )
    testOperator( 'horsepower watt convert' )
    testOperator( 'joule/second watt convert' )
    testOperator( 'lusec watt convert' )
    testOperator( 'kilogram*meter*meter/second*second*second watt convert' )
    testOperator( 'meter*newton/second watt convert' )
    testOperator( 'pferdestarke watt convert' )
    testOperator( 'poncelet watt convert' )

    # pressure
    testOperator( 'atmosphere pascal convert' )
    testOperator( 'bar pascal convert' )
    testOperator( 'barye pascal convert' )
    testOperator( 'mmHg pascal convert' )
    testOperator( 'kilogram/meter*second*second pascal convert' )
    testOperator( 'newton/meter*meter pascal convert' )
    testOperator( 'pieze pascal convert' )
    testOperator( 'psi pascal convert' )
    testOperator( 'torr pascal convert' )

    # radiation_dose
    testOperator( 'banana_equivalent_dose sievert convert' )
    testOperator( 'gray sievert convert' )
    testOperator( 'joule/kilogram sievert convert' )
    testOperator( 'rem sievert convert' )

    # radiation_exposure
    testOperator( 'rad coulomb/kilogram convert' )
    testOperator( 'roentgen coulomb/kilogram convert' )

    # solid_angle
    testOperator( 'hemisphere steradian convert' )
    testOperator( 'radian*radian steradian convert' )
    testOperator( 'sphere steradian convert' )
    testOperator( 'square_arcminute steradian convert' )
    testOperator( 'square_arcsecond steradian convert' )
    testOperator( 'square_degree steradian convert' )
    testOperator( 'square_octant steradian convert' )
    testOperator( 'square_quadrant steradian convert' )
    testOperator( 'square_quintant steradian convert' )
    testOperator( 'square_sextant steradian convert' )
    testOperator( 'square_grad steradian convert' )

    # temperature
    testOperator( 'celsius kelvin convert' )
    testOperator( 'degree_newton kelvin convert' )
    testOperator( 'delisle kelvin convert' )
    testOperator( 'fahrenheit kelvin convert' )
    testOperator( 'rankine kelvin convert' )
    testOperator( 'reaumur kelvin convert' )
    testOperator( 'romer kelvin convert' )

    # time
    testOperator( 'beat second convert' )
    testOperator( 'blink second convert' )
    testOperator( 'century second convert' )
    testOperator( 'clarke second convert' )
    testOperator( 'cowznofski second convert' )
    testOperator( 'day second convert' )
    testOperator( 'decade second convert' )
    testOperator( 'eon second convert' )
    testOperator( 'fortnight second convert' )
    testOperator( 'gregorian_year second convert' )
    testOperator( 'hour second convert' )
    testOperator( 'kovac second convert' )
    testOperator( 'jiffy second convert' )
    testOperator( 'lustrum second convert' )
    testOperator( 'martin second convert' )
    testOperator( 'microcentury second convert' )
    testOperator( 'microfortnight second convert' )
    testOperator( 'mingo second convert' )
    testOperator( 'minute second convert' )
    testOperator( 'month second convert' )
    testOperator( 'nanocentury second convert' )
    testOperator( 'shake second convert' )
    testOperator( 'sidereal_day second convert' )
    testOperator( 'sidereal_hour second convert' )
    testOperator( 'sidereal_minute second convert' )
    testOperator( 'sidereal_month second convert' )
    testOperator( 'sidereal_second second convert' )
    testOperator( 'svedberg second convert' )
    testOperator( 'tropical_month second convert' )
    testOperator( 'tropical_year second convert' )
    testOperator( 'week second convert' )
    testOperator( 'wolverton second convert' )
    testOperator( 'wood second convert' )
    testOperator( 'year second convert' )

    expectResult( 'day second convert value', 86400 )

    # velocity
    testOperator( 'kine meter/second convert' )
    testOperator( 'knot meter/second convert' )
    testOperator( 'mach meter/second convert' )
    testOperator( 'mile/hour meter/second convert' )
    testOperator( 'kilometer/hour meter/second convert' )

    # volume
    testOperator( 'acre*foot liter convert' )
    testOperator( 'balthazar liter convert' )
    testOperator( 'beer_barrel liter convert' )
    testOperator( 'beer_keg liter convert' )
    testOperator( 'bottle liter convert' )
    testOperator( 'bucket liter convert' )
    testOperator( 'bushel liter convert' )
    testOperator( 'chopine liter convert' )
    testOperator( 'clavelin liter convert' )
    testOperator( 'coffeespoon liter convert' )
    testOperator( 'coomb liter convert' )
    testOperator( 'cord liter convert' )
    testOperator( 'cubic_foot liter convert' )
    testOperator( 'cubic_inch liter convert' )
    testOperator( 'cubic_meter liter convert' )
    testOperator( 'cup liter convert' )
    testOperator( 'dash liter convert' )
    testOperator( 'demi liter convert' )
    testOperator( 'dessertspoon liter convert' )
    testOperator( 'dram liter convert' )
    testOperator( 'dry_barrel liter convert' )
    testOperator( 'dry_gallon liter convert' )
    testOperator( 'dry_hogshead liter convert' )
    testOperator( 'dry_pint liter convert' )
    testOperator( 'dry_quart liter convert' )
    testOperator( 'dry_tun liter convert' )
    testOperator( 'farshimmelt_ngogn liter convert' )
    testOperator( 'fifth liter convert' )
    testOperator( 'firkin liter convert' )
    testOperator( 'fluid_ounce liter convert' )
    testOperator( 'furshlugginer_ngogn liter convert' )
    testOperator( 'gallon liter convert' )
    testOperator( 'gill liter convert' )
    testOperator( 'goliath liter convert' )
    testOperator( 'hogshead liter convert' )
    testOperator( 'hoppus_foot liter convert' )
    testOperator( 'hoppus_ton liter convert' )
    testOperator( 'imperial_bushel liter convert' )
    testOperator( 'imperial_butt liter convert' )
    testOperator( 'imperial_cup liter convert' )
    testOperator( 'imperial_gallon liter convert' )
    testOperator( 'imperial_gill liter convert' )
    testOperator( 'imperial_hogshead liter convert' )
    testOperator( 'imperial_peck liter convert' )
    testOperator( 'imperial_pint liter convert' )
    testOperator( 'imperial_quart liter convert' )
    testOperator( 'jack liter convert' )
    testOperator( 'jennie liter convert' )
    testOperator( 'jeroboam liter convert' )
    testOperator( 'jigger liter convert' )
    testOperator( 'kenning liter convert' )
    testOperator( 'kilderkin liter convert' )
    testOperator( 'liter liter convert' )
    testOperator( 'magnum liter convert' )
    testOperator( 'marie_jeanne liter convert' )
    testOperator( 'melchior liter convert' )
    testOperator( 'melchizedek liter convert' )
    testOperator( 'meter^3 liter convert' )
    testOperator( 'methuselah liter convert' )
    testOperator( 'minim liter convert' )
    testOperator( 'mordechai liter convert' )
    testOperator( 'nebuchadnezzar liter convert' )
    testOperator( 'ngogn liter convert' )
    testOperator( 'oil_barrel liter convert' )
    testOperator( 'peck liter convert' )
    testOperator( 'piccolo liter convert' )
    testOperator( 'pin liter convert' )
    testOperator( 'pinch liter convert' )
    testOperator( 'pint liter convert' )
    testOperator( 'pipe liter convert' )
    testOperator( 'pony liter convert' )
    testOperator( 'portuguese_almude liter convert' )
    testOperator( 'pottle liter convert' )
    testOperator( 'puncheon liter convert' )
    testOperator( 'quart liter convert' )
    testOperator( 'rehoboam liter convert' )
    testOperator( 'rundlet liter convert' )
    testOperator( 'salmanazar liter convert' )
    testOperator( 'saltspoon liter convert' )
    testOperator( 'scruple liter convert' )
    testOperator( 'smidgen liter convert' )
    testOperator( 'snit liter convert' )
    testOperator( 'solomon liter convert' )
    testOperator( 'sovereign liter convert' )
    testOperator( 'spanish_almude liter convert' )
    testOperator( 'standard liter convert' )
    testOperator( 'stein liter convert' )
    testOperator( 'stere liter convert' )
    testOperator( 'strike liter convert' )
    testOperator( 'sydharb liter convert' )
    testOperator( 'tablespoon liter convert' )
    testOperator( 'teaspoon liter convert' )
    testOperator( 'tierce liter convert' )
    testOperator( 'tun liter convert' )
    testOperator( 'wineglass liter convert' )
    testOperator( 'wine_barrel liter convert' )
    testOperator( 'wine_butt liter convert' )
    testOperator( 'wine_gallon liter convert' )
    testOperator( 'wine_hogshead liter convert' )
    testOperator( 'wine_pipe liter convert' )
    testOperator( 'wine_tun liter convert' )

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

    # complicated conversions
    testOperator( '16800 mA hours * 5 volts * joule convert' )
    testOperator( '1/coulomb 1/ampere*second convert' )
    testOperator( 'kilogram/meter*second^2 joule/meter^3 convert' )
    testOperator( '34000 square_miles 8 feet 9 mph * / ydhms' )
    testOperator( 'second hertz convert' )
    testOperator( 'day hertz convert' )
    testOperator( 'second daily convert' )
    testOperator( 'day daily convert' )

    # conversions I hope to make work
    #testOperator( 'mph miles hourly * convert' )
    #testOperator( 'ohm/hertz', 'second/siemens' )
    #testOperator( 'elementary_charge sqr [ 4 pi e0 electron_mass c sqr ] product / meter convert' )
    #testOperator( 'coulomb^2 ampere^2*second^2 convert' )
    #testOperator( 'h eV second * convert' )
    #testOperator( 'h_bar c * MeV fm * convert' )

    # unit exponentiation
    testOperator( '8 floz inch 3 ** convert' )
    testOperator( 'foot 4 power square_inch sqr convert' )

    # lists of units
    testOperator( '0 5000 284 range2 seconds [ hour minute second ] convert -s1' )

    # special conversions tests
    testOperator( '1 20 range dBm watt convert' )
    testOperator( '0 100 10 range2 dBm watt convert -s1' )
    testOperator( '60 dBm kilowatt convert' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runConvertTests( )

