# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import shlex

from rpnMeasurement import RPNMeasurement
from rpnTestUtils import *

from testConvert import *
from testHelp import *

from mpmath import *


# //******************************************************************************
# //
# //  runCommandLineOptionsTests
# //
# //******************************************************************************

def runCommandLineOptionsTests( ):
    testOperator( '-a20 7 square_root' )

    testOperator( '100101011010011 -b 2' )
    testOperator( '120012022211222012 -b 3' )
    testOperator( 'rick -b 36' )

    testOperator( '6 8 ** -c' )

    testOperator( '-a3 7 square_root -d' )
    testOperator( '-a12 8 square_root -d5' )
    testOperator( '-a50 19 square_root -d10' )

    testOperator( '-a50 1 30 range fibonacci -g 3' )
    testOperator( '-a50 1 30 range fibonacci -g 4' )

    testOperator( '-h' )

    testOperator( '2 sqrt pi * -i' )

    testOperator( '1 10 range 3 ** -o' )

    testOperator( 'pi -p 1000' )

    testOperator( '10 100 10 range2 -r phi' )

    testOperator( '1 100 range -r2' )
    testOperator( '1 100 range -r3' )
    testOperator( '1 100 range -r4' )
    testOperator( '1 100 range -r5' )
    testOperator( '1 100 range -r6' )
    testOperator( '1 100 range -r7' )
    testOperator( '1 100 range -r8' )
    testOperator( '1 100 range -r9' )
    testOperator( '1 100 range -r10' )
    testOperator( '1 100 range -r11' )
    testOperator( '1 100 range -r12' )
    testOperator( '1 100 range -r13' )
    testOperator( '1 100 range -r14' )
    testOperator( '1 100 range -r15' )
    testOperator( '1 100 range -r16' )
    testOperator( '1 100 range -r17' )
    testOperator( '1 100 range -r18' )
    testOperator( '1 100 range -r19' )
    testOperator( '1 100 range -r20' )
    testOperator( '1 100 range -r21' )
    testOperator( '1 100 range -r22' )
    testOperator( '1 100 range -r23' )
    testOperator( '1 100 range -r24' )
    testOperator( '1 100 range -r25' )
    testOperator( '1 100 range -r26' )
    testOperator( '1 100 range -r27' )
    testOperator( '1 100 range -r28' )
    testOperator( '1 100 range -r29' )
    testOperator( '1 100 range -r30' )
    testOperator( '1 100 range -r31' )
    testOperator( '1 100 range -r32' )
    testOperator( '1 100 range -r33' )
    testOperator( '1 100 range -r34' )
    testOperator( '1 100 range -r35' )
    testOperator( '1 100 range -r36' )
    testOperator( '1 100 range -r37' )
    testOperator( '1 100 range -r38' )
    testOperator( '1 100 range -r39' )
    testOperator( '1 100 range -r40' )
    testOperator( '1 100 range -r41' )
    testOperator( '1 100 range -r42' )
    testOperator( '1 100 range -r43' )
    testOperator( '1 100 range -r44' )
    testOperator( '1 100 range -r45' )
    testOperator( '1 100 range -r46' )
    testOperator( '1 100 range -r47' )
    testOperator( '1 100 range -r48' )
    testOperator( '1 100 range -r49' )
    testOperator( '1 100 range -r50' )
    testOperator( '1 100 range -r51' )
    testOperator( '1 100 range -r52' )
    testOperator( '1 100 range -r53' )
    testOperator( '1 100 range -r54' )
    testOperator( '1 100 range -r55' )
    testOperator( '1 100 range -r56' )
    testOperator( '1 100 range -r57' )
    testOperator( '1 100 range -r58' )
    testOperator( '1 100 range -r59' )
    testOperator( '1 100 range -r60' )
    testOperator( '1 100 range -r61' )
    testOperator( '1 100 range -r62' )
    testOperator( '1 100 range -rphi' )

    testOperator( '-a1000 -d5 7 square_root -r62' )
    testOperator( '-a1000 -d5 pi -r8' )
    testOperator( '2 1 32 range ** -r16' )

    testOperator( '-t 12 14 ** 1 + factor' )
    testOperator( '1 40 range fibonacci factor -s1' )

    testOperator( '3 1 20 range ** -x' )

    testOperator( '65537 4 ** -r16 -g8 -z' )


# //******************************************************************************
# //
# //  runAlgebraOperatorTests
# //
# //******************************************************************************

def runAlgebraOperatorTests( ):
    # bell_polynomal
    testOperator( '4 5 bell_polynomial' )

    # eval_poly
    testOperator( '1 10 range 6 eval_poly' )
    testOperator( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_poly' )

    # find_poly

    # polyadd
    testOperator( '1 10 range 1 10 range polyadd' )

    # polymul
    testOperator( '1 10 range 1 10 range polymul' )

    # polypower
    testOperator( '[ 1 2 3 4 ] 5 polypower' )

    # polyprod
    testOperator( '[ [ 1 10 range ] [ 1 10 range ] [ 2 11 range ] ] polyprod' )

    # polysum
    testOperator( '[ [ 1 10 range ] [ 2 11 range ] ] polysum' )

    # solve
    testOperator( '1 8 range solve' )

    # solve2
    testOperator( '8 9 10 solve2' )

    # solve3
    testOperator( '10 -10 10 -10 solve3' )

    # solve4
    testOperator( '2 -3 2 -3 2 solve4' )


# //******************************************************************************
# //
# //  runArithmeticOperatorTests
# //
# //******************************************************************************

def runArithmeticOperatorTests( ):
    # abs
    expectRPN( '-394 abs', 394 )
    expectRPN( '0 abs', 0 )
    expectRPN( '394 abs', 394 )

    # add
    expectRPN( '4 3 add', 7 )
    expectRPN( '3 feet 7 inches + inches convert', RPNMeasurement( mpmathify( '43' ), [ { 'inch' : 1 } ] ) )
    testOperator( 'today 7 days +' )
    testOperator( 'today 3 weeks +' )
    testOperator( 'today 50 years +' )
    testOperator( '4 cups 13 teaspoons +' )
    testOperator( '55 mph 10 miles hour / +' )
    testOperator( '55 mph 10 meters second / +' )
    testOperator( '55 mph 10 furlongs fortnight / +' )
    testOperator( 'today 3 days add' )
    testOperator( 'today 3 weeks add' )
    testOperator( 'now 150 miles 10 furlongs fortnight / / add' )

    # ceiling
    expectRPN( '9.99999 ceiling', 10 )
    expectRPN( '-0.00001 ceiling', 0 )

    # divide
    testOperator( '12 13 divide' )
    testOperator( '10 days 7 / dhms' )
    testOperator( 'marathon 100 miles hour / / minutes convert' )
    testOperator( '2 zeta sqrt 24 sqrt / 12 *' )
    testOperator( 'now 2014-01-01 - minutes /' )

    # floor
    expectRPN( '-0.4 floor', -1 )
    expectRPN( '1 floor', 1 )
    expectRPN( '3.4 floor', 3 )

    # gcd
    expectRPN( '1 100 range gcd', 1 )
    expectRPN( '[ 124 324 ] gcd', 4 )
    expectRPN( '[ 8 64 ] gcd', 8 )

    # is_divisible
    expectRPN( '1000 10000 is_divisible', 0 )
    expectRPN( '10000 1000 is_divisible', 1 )
    expectRPN( '12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    expectRPN( '1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )

    # is_equal
    expectRPN( '4 3 is_equal', 0 )
    expectRPN( 'pi pi is_equal', 1 )

    # is_even
    expectRPN( '-2 is_even', 1 )
    expectRPN( '-1 is_even', 0 )
    expectRPN( '0 is_even', 1 )
    expectRPN( '1 is_even', 0 )
    expectRPN( '2 is_even', 1 )

    # is_greater
    expectRPN( '4 3 is_greater', 1 )
    expectRPN( '55 55 is_greater', 0 )
    expectRPN( 'e pi is_greater', 0 )

    # is_less
    expectRPN( '4 3 is_less', 0 )
    expectRPN( '2 2 is_less', 0 )
    expectRPN( '2 3 is_less', 1 )

    # is_not_equal
    expectRPN( '4 3 is_not_equal', 1 )
    expectRPN( '3 3 is_not_equal', 0 )

    # is_not_greater
    expectRPN( '4 3 is_not_greater', 0 )
    expectRPN( '77 77 is_not_greater', 1 )
    expectRPN( '2 99 is_not_greater', 1 )

    # is_not_less
    expectRPN( '4 3 is_not_less', 1 )
    expectRPN( '663 663 is_not_less', 1 )
    expectRPN( '-100 100 is_not_less', 0 )

    # is_not_zero
    expectRPN( '-1 is_not_zero', 1 )
    expectRPN( '0 is_not_zero', 0 )
    expectRPN( '1 is_not_zero', 1 )

    # is_odd
    expectRPN( '-2 is_odd', 0 )
    expectRPN( '-1 is_odd', 1 )
    expectRPN( '0 is_odd', 0 )
    expectRPN( '1 is_odd', 1 )
    expectRPN( '2 is_odd', 0 )

    # is_square
    expectRPN( '1024 is_square', 1 )
    expectRPN( '5 is_square', 0 )

    # is_zero
    expectRPN( '-1 is_zero', 0 )
    expectRPN( '0 is_zero', 1 )
    expectRPN( '1 is_zero', 0 )

    # lcm
    expectEqual( '1 10 range lcm', '[ 2 2 2 3 3 5 7 ] prod' )

    # max
    expectRPN( '1 10 range max', 10 )
    expectRPN( '10 1 range min', 1 )
    expectRPN( '[ 9 4 7 2 5 6 3 8 ] max', 9 )

    # mean
    expectRPN( '1 10 range mean', 5.5 )
    expectRPN( '1 10000 range mean', 5000.5 )

    # min
    expectRPN( '1 10 range min', 1 )
    expectRPN( '10 1 range min', 1 )
    expectRPN( '[ 9 4 7 2 5 6 3 8 ] min', 2 )

    # modulo
    expectRPN( '11001 100 modulo', 1 )
    expectRPN( '-120 7 modulo', 6 )
    expectRPN( '8875 49 modulo', 6 )
    expectRPN( '199467 8876 modulo', 4195 )

    # multiply
    expectRPN( '5 7 multiply', 35 )
    testOperator( '15 mph 10 hours *' )
    testOperator( 'c m/s convert 1 nanosecond * inches convert' )
    testOperator( 'barn gigaparsec * cubic_inch convert' )

    # negative
    expectRPN( '-4 negative', 4 )
    expectRPN( '0 negative', 0 )
    expectRPN( '4 negative', -4 )

    # nearest_int
    expectRPN( '0.1 nearest_int', 0 )
    expectRPN( '4.5 nearest_int', 4 )

    # product
    testOperator( '1 10 range product' )

    # reciprocal
    testOperator( '6 7 / reciprocal' )

    # round
    expectRPN( '0.1 round', 0 )
    expectRPN( '4.5 round', 5 )

    # sign
    expectRPN( '1 sign', 1 )
    expectRPN( '0 sign', 0 )
    expectRPN( '-1 sign', -1 )
    expectRPN( 'infinity sign', 1 )
    expectRPN( 'negative_infinity sign', -1 )

    # stddev
    testOperator( '1 10 range stddev' )

    # subtract
    testOperator( '3948 474 subtract' )
    testOperator( '4 cups 27 teaspoons -' )
    testOperator( '57 hectares 23 acres -' )
    testOperator( '10 Mb second / 700 MB hour / -' )
    testOperator( 'today 3 days -' )
    testOperator( 'today 3 weeks -' )
    testOperator( 'today 3 months -' )
    testOperator( 'now earth_radius 2 pi * * miles convert 4 mph / -' )
    testOperator( 'today 2 months -' )
    testOperator( 'today 1965-03-31 -' )
    testOperator( '2015-01-01 1965-03-31 -' )

    # sum
    expectRPN( '1 10 range sum', 55 )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    # astronomical_dawn
    testOperator( '"Leesburg, VA" location today astronomical_dawn' )

    # astronomical_dusk
    testOperator( '"Leesburg, VA" location today astronomical_dusk' )

    # autumnal_equinox
    testOperator( '2015 autumnal_equinox' )

    # distance
    testOperator( '"Leesburg, VA" location "Smithfield, VA" location distance' )

    # dawn
    testOperator( '"Leesburg, VA" location today dawn' )

    # dusk
    testOperator( '"Leesburg, VA" location today dusk' )

    # jupiter

    # latlong

    # location

    # location_info

    # mars

    # mercury

    # moon

    # moonrise
    testOperator( '"Leesburg, VA" location today moonrise' )

    # moonset
    testOperator( '"Leesburg, VA" location today moonset' )

    # moon_antitransit
    testOperator( '"Leesburg, VA" location today moon_antitransit' )

    # moon_phase
    testOperator( 'today moon_phase' )

    # moon_transit
    testOperator( '"Leesburg, VA" location today moon_transit' )

    # nautical_dawn
    testOperator( '"Leesburg, VA" location today nautical_dawn' )

    # nautical_dusk
    testOperator( '"Leesburg, VA" location today nautical_dusk' )

    # neptune
    testOperator( 'neptune "Leesburg, VA" location now next_rising' )

    # next_antitransit
    testOperator( 'saturn "Leesburg, VA" location today next_antitransit' )

    # next_first_quarter_moon
    testOperator( 'today next_first_quarter_moon' )

    # next_full_moon
    testOperator( 'today next_full_moon' )

    # next_last_quarter_moon
    testOperator( 'today next_last_quarter_moon' )

    # next_new_moon
    testOperator( 'today next_new_moon' )

    # next_rising
    testOperator( 'moon "Leesburg, VA" location now next_rising' )

    # next_setting
    testOperator( 'moon "Leesburg, VA" location now next_setting' )

    # next_transit
    testOperator( 'moon "Leesburg, VA" location now next_transit' )

    # pluto
    testOperator( 'pluto "Leesburg, VA" location now next_rising' )

    # previous_antitransit
    testOperator( 'neptune "Leesburg, VA" location now previous_antitransit' )

    # previous_first_quarter_moon
    testOperator( 'today previous_first_quarter_moon' )

    # previous_full_moon
    testOperator( 'today previous_full_moon' )

    # previous_last_quarter_moon
    testOperator( 'today previous_last_quarter_moon' )

    # previous_new_moon
    testOperator( 'today previous_new_moon' )

    # previous_rising
    testOperator( 'jupiter "Leesburg, VA" location now previous_rising' )

    # previous_setting
    testOperator( 'jupiter "Leesburg, VA" location now previous_setting' )

    # previous_transit
    testOperator( 'mercury "Leesburg, VA" location now previous_transit' )

    # saturn
    testOperator( 'saturn "Leesburg, VA" location today next_rising' )

    # sky_location
    testOperator( 'mars now sky_location' )

    # solar_noon
    testOperator( '"Leesburg, VA" location today solar_noon' )

    # summer_solstice
    testOperator( '2015 summer_solstice' )

    # sun
    testOperator( 'sun "Leesburg, VA" location today next_rising' )

    # sunrise
    testOperator( '"Leesburg, VA" location today sunrise' )

    # sunset
    testOperator( '"Leesburg, VA" location today sunset' )

    # sun_antitransit
    testOperator( '"Leesburg, VA" location today sun_antitransit' )

    # vernal_equinox
    testOperator( '2015 vernal_equinox' )

    # uranus
    testOperator( 'uranus "Leesburg, VA" location today next_rising' )

    # venus
    testOperator( 'venus "Leesburg, VA" location today next_rising' )

    # winter_solstice
    testOperator( '2015 winter_solstice' )


# //******************************************************************************
# //
# //  runBitwiseOperatorTests
# //
# //******************************************************************************

def runBitwiseOperatorTests( ):
    # and
    testOperator( '0x7777 0xdcba and' )

    # count_bits
    testOperator( '0xffff count_bits' )

    # nand
    testOperator( '-x 0x5543 0x7789 nand' )

    # nor
    testOperator( '-x 0x5543 0x7789 nor' )

    # not
    testOperator( '0xffffff ~' )
    testOperator( '142857 not' )
    testOperator( '-x 0xefefefefefefef not' )

    # or
    testOperator( '-x 0x5543 0x7789 or' )

    # parity
    testOperator( '0xff889d8f parity' )

    # shift_left
    testOperator( '-x 0x10 3 shift_left' )

    # shift_right
    testOperator( '-x 0x1000 4 shift_right' )

    # xor
    testOperator( '0x1939 0x3948 xor' )


# //******************************************************************************
# //
# //  runCalendarOperatorTests
# //
# //******************************************************************************

def runCalendarOperatorTests( ):
    # calendar
    testOperator( '1965-03 calendar' )
    testOperator( '2014-10 calendar' )

    # from_bahai

    # from_hebrew

    # from_indian_civil

    # from_islamic

    # from_julian

    # from_mayan

    # from_persian

    # iso_date

    # to_bahai

    # to_bahai_name

    # to_hebrew

    # to_hebrew_name

    # to_indian_civil

    # to_indian_civil_name

    # to_islamic

    # to_islamic_name

    # to_iso

    # to_iso_name

    # to_julian

    # to_julian_day
    testOperator( 'today to_julian_day' )

    # to_lilian_day

    # to_mayan

    # to_mayan_name

    # to_ordinal_date

    # to_persian

    # to_persian_name

    # year_calendar
    testOperator( '1965 year_calendar' )
    testOperator( 'today year_calendar' )


# //******************************************************************************
# //
# //  runCombinatoricOperatorTests
# //
# //******************************************************************************

def runCombinatoricOperatorTests( ):
    # bell
    testOperator( '-a43 45 bell' )

    # bernoulli
    testOperator( '16 bernoulli' )

    # binomial
    testOperator( '12 9 binomial' )
    testOperator( '-a20 -c 120 108 binomial' )

    # compositions

    # debruijn
    testOperator( '4 3 debruijn' )

    # delannoy
    testOperator( '-a80 100 delannoy' )

    # lah
    testOperator( '5 6 lah' )

    # motzkin
    testOperator( '-a25 56 motzkin' )

    # multifactorial

    # narayana
    testOperator( '6 8 narayana' )

    # nth_apery
    testOperator( '-a20 12 nth_apery' )

    # nth_catalan
    testOperator( '-a50 85 nth_catalan' )

    # partitions
    expectEqual( '-t 0 30 range partitions', '41 oeis 31 left' )

    # pell
    testOperator( '13 pell' )

    # permutations
    testOperator( '8 3 permutations' )

    # schroeder
    testOperator( '-a50 67 schroeder' )

    # sylvester
    testOperator( '45 sylvester' )


# //******************************************************************************
# //
# //  runComplexMathOperatorTests
# //
# //******************************************************************************

def runComplexMathOperatorTests( ):
    # argument
    testOperator( '3 3 i + argument' )

    # conjugate
    testOperator( '3 3 i + conjugate' )

    # i
    testOperator( '3 i' )

    # imaginary

    # real


# //******************************************************************************
# //
# //  runConstantOperatorTests
# //
# //******************************************************************************

def runConstantOperatorTests( ):
    # apery
    testOperator( 'apery' )

    # avogadro
    testOperator( '-a25 avogadro' )

    # catalan
    testOperator( 'catalan' )

    # champernowne
    testOperator( '-a100 champernowne' )

    # copeland
    testOperator( '-a 1000 copeland' )

    # default
    expectRPN( 'default', -1 )

    # e
    testOperator( 'e' )

    # eddington_number
    testOperator( 'eddington_number' )

    # electric_constant
    testOperator( 'electric_constant' )

    # euler
    testOperator( 'euler' )

    # false
    expectRPN( 'false', 0 )

    # faradays_constant
    testOperator( 'faradays_constant' )

    # fine_structure
    testOperator( 'fine_structure' )

    # glaisher
    testOperator( 'glaisher' )

    # infinity
    testOperator( 'infinity x fib x 1 - fib / limit' )
    expectEqual( 'infinity x fib x 1 - fib / limit', 'phi' )
    testOperator( 'infinity x 1/x 1 + x ** limit' )

    # itoi
    testOperator( 'itoi' )

    # khinchin
    testOperator( 'khinchin' )

    # magnetic_constant
    testOperator( 'magnetic_constant' )

    # max_char
    expectEqual( 'max_char', '2 7 ** 1 -' )

    # max_double
    testOperator( 'max_double' )

    # max_float
    testOperator( 'max_float' )

    # max_long
    expectEqual( 'max_long', '2 31 ** 1 -' )

    # max_longlong
    expectEqual( '-a20 max_longlong', '-a20 2 63 ** 1 -' )

    # max_quadlong
    expectEqual( '-a40 max_quadlong', '-a40 2 127 ** 1 -' )

    # max_short
    expectEqual( 'max_short', '2 15 ** 1 -' )

    # max_uchar
    expectEqual( 'max_uchar', '2 8 ** 1 -' )

    # max_ulong
    expectEqual( 'max_ulong', '2 32 ** 1 -' )

    # max_ulonglong
    expectEqual( '-a20 max_ulonglong', '-a20 2 64 ** 1 -' )

    # max_uquadlong
    expectEqual( '-a40 max_uquadlong', '-a40 2 128 ** 1 -' )

    # max_ushort
    expectEqual( 'max_ushort', '2 16 ** 1 -' )

    # mertens_constant
    testOperator( 'mertens_constant' )

    # mills
    testOperator( 'mills' )

    # min_char
    expectEqual( 'min_char', '2 7 ** negative' )

    # min_double
    testOperator( 'min_double' )

    # min_float
    testOperator( 'min_float' )

    # min_long
    expectEqual( 'min_long', '2 31 ** negative' )

    # min_longlong
    expectEqual( '-a20 min_longlong', '-a20 2 63 ** negative' )

    # min_quadlong
    expectEqual( '-a40 min_quadlong', '-a40 2 127 ** negative' )

    # min_short
    expectEqual( 'min_short', '2 15 ** negative' )

    # min_uchar
    expectRPN( 'min_uchar', 0 )

    # min_ulong
    expectRPN( 'min_ulong', 0 )

    # min_ulonglong
    expectRPN( 'min_ulonglong', 0 )

    # min_uquadlong
    expectRPN( 'min_uquadlong', 0 )

    # min_ushort
    expectRPN( 'min_ushort', 0 )

    # negative_infinity
    testOperator( 'negative_infinity' )

    # newtons_constant
    testOperator( 'newtons_constant' )

    # omega
    testOperator( 'omega' )

    # phi
    testOperator( 'phi' )

    # pi
    testOperator( 'pi' )

    # plastic
    testOperator( 'plastic' )

    # prevost
    testOperator( 'prevost' )

    # radiation_constant
    testOperator( 'radiation_constant' )

    # robbins
    testOperator( 'robbins' )

    # rydberg_constant
    testOperator( 'rydberg_constant' )

    # silver_ratio
    testOperator( 'silver_ratio' )

    # stefan_boltzmann
    testOperator( 'stefan_boltzmann' )

    # true
    expectRPN( 'true', 1 )

    # days of the week
    expectRPN( 'monday', 1 )
    expectRPN( 'tuesday', 2 )
    expectRPN( 'wednesday', 3 )
    expectRPN( 'thursday', 4 )
    expectRPN( 'friday', 5 )
    expectRPN( 'saturday', 6 )
    expectRPN( 'sunday', 7 )

    # months
    expectRPN( 'january', 1 )
    expectRPN( 'february', 2 )
    expectRPN( 'march', 3 )
    expectRPN( 'april', 4 )
    expectRPN( 'may', 5 )
    expectRPN( 'june', 6 )
    expectRPN( 'july', 7 )
    expectRPN( 'august', 8 )
    expectRPN( 'september', 9 )
    expectRPN( 'october', 10 )
    expectRPN( 'november', 11 )
    expectRPN( 'december', 12 )


# //******************************************************************************
# //
# //  runConversionOperatorTests
# //
# //******************************************************************************

def runConversionOperatorTests( ):
    # char
    testOperator( '0x101 char' )

    # convert - convert is handled separately

    # dhms
    testOperator( '8 million seconds dhms' )

    # dms
    testOperator( '1 radian dms' )

    # double
    testOperator( '-x 10 20 ** double' )
    testOperator( '-x pi double' )

    # float
    testOperator( '-x 1029.3 float' )
    testOperator( 'pi float' )

    # from_unix_time
    testOperator( '1234567890 from_unix_time' )

    # long
    testOperator( '3456789012 long' )

    # longlong
    testOperator( '1234567890123456789012 longlong' )

    # hms
    testOperator( '54658 seconds hms' )

    # integer
    testOperator( '456 8 integer' )

    # invert_units
    testOperator( '30 miles gallon / invert_units' )

    # latlong_to_nac

    # make_pyth_3

    # make_pyth_4

    # make_time

    # pack
    testOperator( '-x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    # short
    testOperator( '32800 short' )

    # to_unix_time
    testOperator( '[ 2014 4 30 0 0 0 ] make_time to_unix_time' )

    # uchar
    testOperator( '290 uchar' )

    # uinteger
    testOperator( '200 8 uinteger' )

    # ulong
    testOperator( '234567890 ulong' )

    # ulonglong
    testOperator( '-a20 12345678901234567890 ulonglong' )

    # undouble
    testOperator( '0x400921fb54442d18 undouble' )
    testOperator( '0xcdcdcdcdcdcdcdcd undouble' )

    # unfloat
    testOperator( '0x40490fdb unfloat' )
    testOperator( '0xcdcdcdcd unfloat' )

    # unpack
    testOperator( '503942034 [ 3 4 5 11 4 4 ] unpack' )

    # ushort
    testOperator( '23456 ushort' )

    # ydhms
    testOperator( '14578 seconds ydhms' )


# //******************************************************************************
# //
# //  runDateTimeOperatorTests
# //
# //******************************************************************************

def runDateTimeOperatorTests( ):
    # ash_wednesday
    testOperator( '2015 ash_wednesday' )

    # dst_end
    testOperator( '2015 dst_end' )

    # dst_start
    testOperator( '2015 dst_start' )

    # easter
    testOperator( '2015 easter' )

    # election_day
    testOperator( '2015 election_day' )

    # iso_day
    testOperator( 'today iso_day' )

    # labor_day
    testOperator( '2015 labor_day' )

    # make_julian_time
    testOperator( '[ 2015 7 5 4 3 ] make_julian_time' )

    # make_iso_time

    # memorial_day
    testOperator( '2015 memorial_day' )

    # now
    testOperator( 'now' )

    # nth_weekday
    testOperator( '2015 march 4 thursday nth_weekday' )
    testOperator( '2015 march -1 thursday nth_weekday' )

    # nth_weekday_of_year
    testOperator( '2015 20 thursday nth_weekday_of_year' )
    testOperator( '2015 -1 thursday nth_weekday_of_year' )

    # presidents_day
    testOperator( '2015 presidents_day' )

    # thanksgiving
    testOperator( '2015 thanksgiving' )

    # today
    testOperator( 'today' )

    # tomorrow
    testOperator( 'tomorrow' )

    # weekday
    testOperator( 'today weekday' )

    # yesterday
    testOperator( 'yesterday' )


# //******************************************************************************
# //
# //  runFunctionOperatorTests
# //
# //******************************************************************************

def runFunctionOperatorTests( ):
    # eval
    testOperator( '10 x 5 * eval' )
    testOperator( '-a20 57 x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )

    # eval2
    # eval3
    # filter
    # filter_by_index
    # limit
    # limitn
    # negate
    # nprod
    # nsum
    # plot
    # plot2
    # plotc
    # unfilter
    # unfilter_by_index
    # x
    # y
    # z


# //******************************************************************************
# //
# //  runGeometryOperatorTests
# //
# //******************************************************************************

def runGeometryOperatorTests( ):
    # n_sphere_area
    testOperator( '34 inches 3 n_sphere_area' )
    testOperator( '34 square_inches 3 n_sphere_area' )
    testOperator( '34 cubic_inches 3 n_sphere_area' )

    # n_sphere_radius
    testOperator( '3 meters 4 n_sphere_radius' )
    testOperator( '3 square_meters 4 n_sphere_radius' )
    testOperator( '3 cubic_meters 4 n_sphere_radius' )

    # n_sphere_volume
    testOperator( '3 square_feet 6 nsphere_volume' )

    # polygon_area
    testOperator( '13 polygon_area' )

    # sphere_area
    testOperator( '8 inches sphere_area' )
    testOperator( '8 sq_inches sphere_area' )
    #testOperator( '8 cu_inches sphere_area' )    # not implemented yet

    # sphere_radius
    testOperator( '4 inches sphere_radius' )
    testOperator( '4 square_inches sphere_radius' )
    testOperator( '4 cubic_inches sphere_radius' )

    # sphere_volume
    testOperator( '5 inches sphere_volume' )
    #testOperator( '5 sq_inches sphere_volume' )  # not implemented yet
    testOperator( '5 cubic_in sphere_volume' )

    # triangle_area
    testOperator( '123 456 789 triangle_area' )


# //******************************************************************************
# //
# //  runInternalOperatorTests
# //
# //******************************************************************************

def runInternalOperatorTests( ):
    # _dump_aliases
    testOperator( '_dump_aliases' )

    # _dump_operators
    testOperator( '_dump_operators' )

    # _stats
    testOperator( '_stats' )


# //******************************************************************************
# //
# //  runLexicographicOperatorTests
# //
# //******************************************************************************

def runLexicographicOperatorTests( ):
    # add_digits
    expectRPN( '3 4 add_digits', 34 )
    expectRPN( '3 45 add_digits', 345 )
    expectRPN( '34 567 add_digits', 34567 )

    # combine_digits
    testOperator( '1 9 range combine_digits' )

    # dup_digits
    testOperator( '543 2 dup_digits' )

    # find_palindrome
    testOperator( '-a30 10911 55 find_palindrome' )
    testOperator( '180 200 range 10 find_palindrome -s1' )

    # get_digits
    testOperator( '123456789 get_digits' )

    # is_palindrome
    testOperator( '101 is_palindrome' )
    testOperator( '1 22 range is_palindrome' )
    testOperator( '1234567890 is_palindrome' )

    # is_pandigital
    testOperator( '1234567890 is_pandigital' )

    # multiply_digits
    testOperator( '123456789 multiply_digits' )

    # reversal_addition
    testOperator( '-a20 89 24 reversal_addition' )
    testOperator( '-a20 80 89 range 24 reversal_addition' )
    testOperator( '-a20 89 16 24 range reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    # reverse_digits
    testOperator( '37 1 8 range * reverse_digits' )
    testOperator( '37 1 2 9 range range * reverse_digits' )

    # sum_digits
    testOperator( '2 32 ** 1 - sum_digits' )


# //******************************************************************************
# //
# //  runListOperatorTests
# //
# //******************************************************************************

def runListOperatorTests( ):
    # alternate_signs
    testOperator( '1 10 range alternate_signs' )

    # alternate_signs_2
    testOperator( '1 10 range alternate_signs_2' )

    # alternating_sum
    testOperator( '1 10 range alternating_sum' )

    # alternating_sum_2
    testOperator( '1 10 range alternating_sum_2' )

    # append
    testOperator( '1 10 range 45 50 range append' )
    testOperator( '1 10 range 11 20 range append 21 30 range append' )

    # count
    expectRPN( '1 10 range count', 10 )

    # diffs
    testOperator( '1 10 range diffs' )
    testOperator( '1 10 range fib diffs' )

    # diffs2
    testOperator( '1 10 range diffs2' )
    testOperator( '1 10 range fib diffs2' )

    # element
    testOperator( '1 10 range 5 element' )
    testOperator( '-a25 1 100 range fibonacci 55 element' )

    # exponential_range
    testOperator( '1.1 1.1 10 exponential_range' )

    # flatten
    expectEqual( '[ 1 2 [ 3 4 5 ] [ 6 [ 7 [ 8 9 ] ] 10 ] ] flatten', '1 10 range' )

    # geometric_mean
    testOperator( '1 100 range geometric_mean' )
    testOperator( '[ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    # geometric_range
    testOperator( '2 8 8 geometric_range' )

    # group_elements

    # interleave
    testOperator( '1 10 range 1 10 range interleave' )

    # intersection
    testOperator( '1 10 range 1 8 range intersection' )

    # left
    testOperator( '1 10 range 5 left' )

    # max_index
    testOperator( '1 10 range max_index' )

    # min_index
    testOperator( '1 10 range min_index' )

    # nonzero
    testOperator( '1 10 range nonzero' )

    # occurrences
    testOperator( '4 100 random_integer_ occurrences' )

    # range
    testOperator( '1 23 range' )

    # range2
    testOperator( '1 23 2 range2' )

    # ratios
    testOperator( '1 10 range ratios' )

    # reduce
    testOperator( '[ 4 8 12 ] reduce' )

    # reverse
    testOperator( '1 10 range reverse' )
    testOperator( '1 2 10 range range reverse' )
    testOperator( '1 2 10 range reverse range reverse' )
    testOperator( '1 2 10 range reverse range' )

    # right
    testOperator( '1 10 range 5 right' )

    # shuffle

    # slice
    testOperator( '1 10 range 3 5 slice' )
    testOperator( '1 10 range 2 -5 slice' )

    # sort
    testOperator( '10 1 -1 range2 sort' )

    # sort_descending
    testOperator( '1 10 range sort_descending' )

    # sublist
    testOperator( '1 10 range 1 5 sublist' )

    # union
    testOperator( '1 10 range 11 20 range union' )

    # unique
    testOperator( '1 10 range unique' )
    testOperator( '1 10 range 1 10 range append unique' )
    testOperator( '[ 1 10 range 10 dup ] unique' )

    # zero
    testOperator( '-10 10 range zero' )
    testOperator( '1 10 range zero' )


# //******************************************************************************
# //
# //  runLogarithmOperatorTests
# //
# //******************************************************************************

def runLogarithmOperatorTests( ):
    # lambertw
    testOperator( '5 lambertw' )

    # li
    testOperator( '12 li' )

    # ln
    testOperator( '1000 ln' )

    # log10
    testOperator( '1000 log10' )

    # log2
    testOperator( '1000 log2' )

    # logxy
    testOperator( '6561 3 logxy' )

    # polylog
    testOperator( '9 3 polylog' )


# //******************************************************************************
# //
# //  runModifierOperatorTests
# //
# //******************************************************************************

def runModifierOperatorTests( ):
    # [

    # ]

    # {
    testOperator( '"Leesburg, VA" location today { sunrise sunset moonrise moonset }' )

    # }
    testOperator( '1 10 range { is_prime is_pronic is_semiprime }' )

    # dup_term
    testOperator( '[ 1 2 10 dup_term ] cf' )

    # dup_operator
    testOperator( '2 5 dup_operator sqr' )
    testOperator( '4 6 5 dup_operator *' )

    # previous
    expectRPN( '6 previous *', 36 )

    # unlist
    testOperator( '[ 1 2 ] unlist +' )

    # use_members


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    # aliquot
    testOperator( '276 10 aliquot' )

    # alternating_factorial
    testOperator( '13 alternating_factorial' )
    testOperator( '-a20 1 20 range alternating_factorial' )

    # base
    testOperator( '1 10 range 2 base' )
    testOperator( '1 10 range 3 base' )
    testOperator( '1 10 range 4 base' )
    testOperator( '1 10 range 5 base' )
    testOperator( '1 10 range 6 base' )
    testOperator( '1 10 range 7 base' )
    testOperator( '1 10 range 8 base' )
    testOperator( '1 10 range 9 base' )

    testOperator( '-a30 1 20 range 11 base' )
    testOperator( '-a30 1 20 range 12 base' )
    testOperator( '-a30 1 20 range 13 base' )
    testOperator( '-a30 1 20 range 14 base' )
    testOperator( '-a30 1 20 range 15 base' )
    testOperator( '-a30 1 20 range 16 base' )
    testOperator( '-a30 1 20 range 17 base' )
    testOperator( '-a30 1 20 range 18 base' )
    testOperator( '-a30 1 20 range 19 base' )
    testOperator( '-a30 1 20 range 20 base' )

    # carol
    testOperator( '-a500 773 carol' )

    # cf
    testOperator( '1 10 range cf' )

    # count_divisors
    testOperator( '1024 count_divisors' )

    # crt
    testOperator( '1 3 range 10 20 range 3 primes crt' )

    # divisors
    testOperator( '2 3 ** 3 4 ** * divisors' )
    testOperator( '12 ! divisors' )

    # double_factorial
    testOperator( '9 double_factorial' )

    # ecm
    testOperator( '-a40 10 30 ** random_integer ecm' )

    # egypt
    testOperator( '45 67 egypt' )

    # euler_brick
    testOperator( '2 3 make_pyth_3 unlist euler_brick' )

    # euler_phi
    testOperator( '1 20 range euler_phi' )

    # factor
    testOperator( '883847311 factor' )
    testOperator( '1 40 range fibonacci factor -s1' )

    # factorial
    testOperator( '-a25 23 factorial' )

    # fibonacci
    testOperator( '1 50 range fibonacci' )
    testOperator( '-c -a 8300 39399 fibonacci' )

    # fibonorial
    testOperator( '5 fibonorial' )
    testOperator( '-a50 24 fibonorial' )

    # fraction
    testOperator( '12 23 fraction' )

    # frobenius
    testOperator( '10 20 range 3 primes frobenius' )

    # gamma
    testOperator( '3 gamma' )

    # harmonic
    testOperator( '34 harmonic' )

    # heptanacci
    testOperator( '224623 heptanacci' )

    # hexanacci
    testOperator( '949 hexanacci' )

    # hyperfactorial
    testOperator( '-a160 17 hyperfactorial' )

    # is_abundant
    testOperator( '1 20 range is_abundant' )

    # is_achilles
    testOperator( '1 20 range is_achilles' )

    # is_deficient
    testOperator( '1 20 range is_deficient' )

    # is_k_semiprime
    testOperator( '1 20 range 3 is_k_semiprime' )

    # is_perfect
    testOperator( '1 30 range is_perfect' )

    # is_prime
    testOperator( '1000 1030 range is_prime' )
    testOperator( '2049 is_prime' )
    testOperator( '92348759911 is_prime' )

    # is_pronic
    testOperator( '1 20 range is_pronic' )

    # is_powerful
    testOperator( '1 20 range is_powerful' )

    # is_rough
    testOperator( '1 20 range 2 is_rough' )

    # is_semiprime
    testOperator( '12 is_semiprime' )

    # is_smooth
    testOperator( '128 4 is_smooth' )
    testOperator( '1 20 range 2 is_smooth' )

    # is_sphenic
    testOperator( '[ 2 3 5 ] prime is_sphenic' )

    # is_squarefree
    testOperator( '2013 sqr is_squarefree' )
    testOperator( '8 primorial is_squarefree' )
    testOperator( '1 20 range is_squarefree' )

    # is_unusual
    testOperator( '-a50 81 23 ** is_unusual' )
    testOperator( '1 20 range is_unusual' )

    # jacobsthal
    testOperator( '10 jacobsthal' )

    # kynea
    testOperator( '8 kynea' )

    # leonardo
    testOperator( '1 10 range leonardo' )

    # leyland
    testOperator( '7 8 leyland' )

    # lgamma
    testOperator( '10 lgamma' )

    # linear_recurrence
    testOperator( '1 10 range 2 5 range 17 linear_recur' )

    # lucas
    testOperator( '-a21 99 lucas' )

    # make_cf
    testOperator( 'e 20 make_cf' )

    # mertens
    testOperator( '20 mertens' )
    testOperator( '1 10 range mertens' )

    # mobius
    testOperator( '20176 mobius' )
    testOperator( '1 20 range mobius' )

    # padovan
    testOperator( '76 padovan' )
    testOperator( '1 20 range padovan' )

    # pascal_triangle
    testOperator( '12 pascal_triangle' )
    testOperator( '1 10 range pascal_triangle -s1' )

    # pentanacci
    testOperator( '16 pentanacci' )

    # polygamma
    testOperator( '4 5 polygamma' )

    # repunit
    testOperator( '-a20 23 5 repunit' )

    # riesel
    testOperator( '23 riesel' )

    # sigma
    testOperator( '1 20 range sigma' )

    # subfactorial
    testOperator( '-a20 19 subfactorial' )

    # superfactorial
    testOperator( '-a50 12 superfactorial' )

    # tetranacci
    testOperator( '-a30 87 tetranacci' )

    # thabit
    testOperator( '-a20 45 thabit' )

    # tribonacci
    testOperator( '1 20 range tribonacci' )
    testOperator( '-c -a 2800 10239 tribonacci' )

    # unit_roots
    testOperator( '7 unit_roots' )

    # zeta
    testOperator( '4 zeta' )


# //******************************************************************************
# //
# //  runPolygonalOperatorTests
# //
# //******************************************************************************

def runPolygonalOperatorTests( ):
    # centered_decagonal
    testOperator( '17 centered_decagonal' )

    # centered_heptagonal
    testOperator( '102 centered_heptagonal' )

    # centered_hexagonal
    testOperator( '103 centered_hexagonal' )

    # centered_nonagonal
    testOperator( '104 centered_nonagonal' )

    # centered_octagonal
    testOperator( '10 centered_octagonal' )

    # centered_pentagonal
    testOperator( '108 centered_pentagonal' )

    # centered_polygonal
    testOperator( '108 5 centered_polygonal' )

    # centered_square
    testOperator( '5 centered_square' )

    # centered_triangular
    testOperator( '100 centered_triangular' )

    # decagonal
    testOperator( '151 decagonal' )

    # decagonal?
    testOperator( '123454321 decagonal?' )

    # decagonal_heptagonal
    testOperator( '-a50 8 decagonal_heptagonal' )

    # decagonal_hexagonal
    testOperator( '-a60 9 decagonal_hexagonal' )

    # decagonal_octagonal
    testOperator( '-a 75 9 decagonal_nonagonal' )

    # decagonal_octagonal
    testOperator( '-a 75 9 decagonal_octagonal' )

    # decagonal_pentagonal
    testOperator( '-a60 7 decagonal_pentagonal' )

    # decagonal_square
    testOperator( '-a40 9 decagonal_square' )

    # decagonal_triangular
    testOperator( '-a40 13 decagonal_triangular' )

    # heptagonal
    testOperator( '203 heptagonal' )

    # heptagonal?
    testOperator( '99999 heptagonal?' )

    # heptagonal_hexagonal
    testOperator( '2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal
    testOperator( '8684 heptagonal_pentagonal' )

    # heptagonal_square
    testOperator( '222 heptagonal_square' )

    # heptagonal_triangular
    testOperator( '399 heptagonal_triangular' )

    # hexagonal
    testOperator( '340 hexagonal' )

    # hexagonal_pentagonal
    testOperator( '107 hexagonal_pentagonal' )

    # hexagonal_square
    testOperator( '-a70 23 hexagonal_square' )

    # nth_centered_decagonal
    testOperator( '1000 nth_centered_decagonal' )

    # nth_centered_heptagonal
    testOperator( '100000 nth_centered_heptagonal' )

    # nth_centered_hexagonal
    testOperator( '7785961 nth_centered_hexagonal' )

    # nth_centered_nonagonal
    testOperator( '5,000,000 nth_centered_nonagonal' )

    # nth_centered_octagonal
    testOperator( '361 nth_centered_octagonal' )

    # nth_centered_pentagonal
    testOperator( '9999 nth_centered_pentagonal' )

    # nth_centered_polygonal
    testOperator( '9999 5 nth_centered_polygonal' )

    # nth_centered_square
    testOperator( '49 nth_centered_square' )

    # nth_centered_triangular
    testOperator( '10000 nth_centered_triangular' )

    # nth_hexagonal
    testOperator( '230860 nth_hexagonal' )

    # nth_nonagonal
    testOperator( '9 6 ** nth_nonagonal' )

    # nth_octagonal
    testOperator( '8 4 ** 1 + nth_octagonal' )

    # nth_pentagonal
    testOperator( '5 5 ** 5 + nth_pentagonal' )

    # nth_polygonal
    testOperator( '12 12 ** 12 nth_polygonal' )

    # nth_square
    testOperator( '111333111 nth_square' )

    # nth_triangular
    testOperator( '20706 nth_triangular' )

    # nonagonal
    testOperator( '554 nonagonal' )

    # nonagonal_heptagonal
    testOperator( '-a50 12 nonagonal_heptagonal' )

    # nonagonal_hexagonal
    testOperator( '-a60 13 nonagonal_hexagonal' )

    # nonagonal_octagonal
    testOperator( '-a 75 14 nonagonal_octagonal' )

    # nonagonal_pentagonal
    testOperator( '-a60 15 nonagonal_pentagonal' )

    # nonagonal_square
    testOperator( '-a22 16 nonagonal_square' )

    # nonagonal_triangular
    testOperator( '-a21 17 nonagonal_triangular' )

    # octagonal
    testOperator( '102 octagonal' )

    # octagonal_heptagonal
    testOperator( '-a40 8 octagonal_heptagonal' )

    # octagonal_hexagonal
    testOperator( '-a30 7 octagonal_hexagonal' )

    # octagonal_pentagonal
    testOperator( '-a15 6 octagonal_pentagonal' )

    # octagonal_square
    testOperator( '-a25 11 octagonal_square' )

    # octagonal_triangular
    testOperator( '-a20 10 octagonal_triangular' )

    # pentagonal
    testOperator( '16 pentagonal' )

    # pentagonal_square
    testOperator( '-a70 10 pentagonal_square' )

    # pentagonal_triangular
    testOperator( '-a40 17 pentagonal_triangular' )

    # polygonal
    testOperator( '9 12 polygonal' )

    # square_triangular
    testOperator( '-a60 34 square_triangular' )

    # triangular
    testOperator( '203 triangular' )


# //******************************************************************************
# //
# //  runPolyhedralOperatorTests
# //
# //******************************************************************************

def runPolyhedralOperatorTests( ):
    # centered_cube
    testOperator( '100 centered_cube' )

    # dodecahedral
    testOperator( '44 dodecahedral' )

    # icosahedral
    testOperator( '100 icosahedral' )

    # polytope
    testOperator( '1 10 range 7 polytope' )
    testOperator( '10 2 8 range polytope' )
    testOperator( '1 10 range 2 8 range polytope' )
    testOperator( '-a20 -c 18 47 polytope' )

    # pyramid
    testOperator( '304 pyramid' )

    # rhombdodec
    testOperator( '89 rhombdodec' )

    # stella_octangula
    testOperator( '3945 stella_octangula' )

    # tetrahedral
    testOperator( '-a20 19978 tetrahedral' )

    # truncated_octahedral
    testOperator( '394 truncated_octahedral' )

    # truncated_tetrahedral
    testOperator( '683 truncated_tetrahedral' )

    # octahedral
    testOperator( '23 octahedral' )

    # pentatope
    testOperator( '12 pentatope' )


# //******************************************************************************
# //
# //  runPowersAndRootsOperatorTests
# //
# //******************************************************************************

def runPowersAndRootsOperatorTests( ):
    # cube
    testOperator( '3 cube' )

    # cube_root
    testOperator( 'pi cube_root' )

    # exp
    testOperator( '13 exp' )

    # exp10
    testOperator( '12 exp10' )

    # expphi
    testOperator( '100 expphi' )

    # hyper4_2
    testOperator( '-a160 4 3 hyper4_2' )

    # power
    testOperator( '4 5 power' )
    testOperator( '4 1 i power' )
    testOperator( '1 10 range 2 10 range power' )

    # powmod
    testOperator( '43 67 9 powmod' )

    # root
    testOperator( '8 3 root' )

    # root2
    testOperator( '2 square_root' )

    # square
    testOperator( '45 square' )

    # tetrate
    testOperator( '3 2 tetrate' )

    # tower
    testOperator( '-c -a30 [ 2 3 2 ] tower' )

    # tower2
    testOperator( '[ 4 4 4 ] tower2' )


# //******************************************************************************
# //
# //  runPrimeNumberOperatorTests
# //
# //******************************************************************************

def runPrimeNumberOperatorTests( ):
    # balanced_prime
    testOperator( '1 10 range balanced' )
    testOperator( '53 balanced' )
    testOperator( '153 balanced' )
    testOperator( '2153 balanced' )

    # balanced_prime_
    testOperator( '1 10 range balanced_' )
    testOperator( '53 balanced_' )
    testOperator( '153 balanced_' )
    testOperator( '2153 balanced_' )

    # cousin_prime
    testOperator( '1 10 range cousin_prime' )
    testOperator( '77 cousin_prime' )
    testOperator( '5176 cousin_prime' )

    # cousin_prime_
    testOperator( '1 10 range cousin_prime_' )
    testOperator( '4486 cousin_prime_' )
    testOperator( '192765 cousin_prime_' )

    # double_balanced
    testOperator( '1 5 range double_balanced' )
    testOperator( '54 double_balanced' )
    testOperator( '82154 double_balanced' )

    # double_balanced_
    testOperator( '1 5 range double_balanced_' )
    testOperator( '54 double_balanced_' )
    testOperator( '100000 double_balanced_' )

    # isolated_prime
    testOperator( '102 isolated_prime' )
    testOperator( '1902 isolated_prime' )

    # next_prime
    testOperator( '1 100 range next_prime' )
    testOperator( '35 next_prime' )
    testOperator( '8783 next_prime' )
    testOperator( '142857 next_prime' )
    testOperator( '-c 6 13 ** 1 + next_prime' )
    testOperator( '-c 7 13 ** 1 + next_prime' )

    # nth_prime?
    testOperator( '1 10 range nth_prime?' )
    testOperator( '67 nth_prime?' )
    testOperator( '16467 nth_prime?' )
    testOperator( '-c 13,000,000,000 nth_prime?' )
    testOperator( '-c 256,000,000,000 nth_prime?' )

    # nth_quad?
    testOperator( '1 100000 10000 range2 nth_quad?' )
    testOperator( '453456 nth_quad?' )
    testOperator( '74,000,000,000 nth_quad?' )

    # polyprime
    testOperator( '1 5 range 1 5 range polyprime' )
    testOperator( '4 3 polyprime' )
    testOperator( '5 8 polyprime' )

    # prime
    testOperator( '1 101 range prime' )
    testOperator( '8783 prime' )
    testOperator( '142857 prime' )
    testOperator( '367981443 prime' )
    testOperator( '9113486725 prime' )

    # primepi
    testOperator( '87 primepi' )

    # primes
    testOperator( '1 5 range 5 primes' )
    testOperator( '1 1 5 range primes' )
    testOperator( '2 1 5 range primes' )
    testOperator( '3 1 5 range primes' )
    testOperator( '4 1 5 range primes' )
    testOperator( '150 10 primes' )
    testOperator( '98765 20 primes' )
    testOperator( '176176176 25 primes' )
    testOperator( '11,000,000,000 25 primes' )

    # primorial
    testOperator( '1 10 range primorial' )

    # quadruplet_prime?
    testOperator( '8 quadruplet_prime?' )
    testOperator( '8871 quadruplet_prime?' )

    # quadruplet_prime
    testOperator( '17 quadruplet_prime' )
    testOperator( '99831 quadruplet_prime' )

    # quadruplet_prime_
    testOperator( '17 quadruplet_prime_' )
    testOperator( '55731 quadruplet_prime_' )

    # quintuplet_prime?
    testOperator( '147951 quintuplet_prime?' )
    testOperator( '2,300,000 quintuplet_prime?' )

    # quintuplet_prime
    testOperator( '18 quintuplet_prime' )
    testOperator( '9387 quintuplet_prime' )

    # quintuplet_prime_
    testOperator( '62 quintuplet_prime_' )
    testOperator( '74238 quintuplet_prime_' )

    # safe_prime
    testOperator( '45 safe_prime' )
    testOperator( '5199846 safe_prime' )

    # sextuplet_prime
    testOperator( '29 sextuplet_prime' )
    testOperator( '1176 sextuplet_prime' )
    testOperator( '556 sextuplet_prime' )

    # sextuplet_prime_
    testOperator( '1 sextuplet_prime_' )
    testOperator( '587 sextuplet_prime_' )
    testOperator( '835 sextuplet_prime_' )
    testOperator( '29 sextuplet_prime_' )

    # sexy_prime
    testOperator( '-c 89,999,999 sexy_prime' )
    testOperator( '1 sexy_prime' )
    testOperator( '1487 sexy_prime' )
    testOperator( '2 sexy_prime' )
    testOperator( '23235 sexy_prime' )
    testOperator( '29 sexy_prime' )

    # sexy_prime_
    testOperator( '1 10 range sexy_prime_' )
    testOperator( '29 sexy_prime_' )
    testOperator( '21985 sexy_prime_' )
    testOperator( '-c 100,000,000 sexy_prime_' )

    # sexy_triplet
    testOperator( '1 10 range sexy_triplet' )
    testOperator( '29 sexy_triplet' )
    testOperator( '-c 593847 sexy_triplet' )
    testOperator( '-c 8574239 sexy_triplet' )

    # sexy_triplet_
    testOperator( '1 10 range sexy_triplet_' )
    testOperator( '52 sexy_triplet_' )
    testOperator( '5298 sexy_triplet_' )
    testOperator( '-c 10984635 sexy_triplet_' )

    # sexy_quadruplet
    testOperator( '1 10 range sexy_quadruplet' )
    testOperator( '29 sexy_quadruplet' )
    testOperator( '-c 289747 sexy_quadruplet' )

    # sexy_quadruplet_
    testOperator( '1 10 range sexy_quadruplet_' )
    testOperator( '29 sexy_quadruplet_' )
    testOperator( '2459 sexy_quadruplet_' )

    # sophie_prime
    testOperator( '1 10 range sophie_prime' )
    testOperator( '87 sophie_prime' )
    testOperator( '6,500,000 sophie_prime' )

    # superprime
    testOperator( '89 superprime' )

    # triple_balanced
    testOperator( '1 10 range triple_balanced' )
    testOperator( '5588 triple_balanced' )

    # triple_balanced_
    testOperator( '1 10 range triple_balanced_' )
    testOperator( '6329 triple_balanced_' )

    # triplet_prime
    testOperator( '1 10 range triplet_prime' )
    testOperator( '192834 triplet_prime' )

    # triplet_prime_
    testOperator( '1 10 range triplet_prime_' )
    testOperator( '192834 triplet_prime_' )

    # twin_prime
    testOperator( '1 10 range twin_prime_' )
    testOperator( '57454632 twin_prime_' )

    # twin_prime_
    testOperator( '1 20 range twin_prime' )
    testOperator( '39485 twin_prime' )


# //******************************************************************************
# //
# //  runSettingsOperatorTests
# //
# //******************************************************************************

def runSettingsOperatorTests( ):
    # accuracy

    # comma

    # comma_mode

    # decimal_grouping

    # hex_mode

    # identify

    # identify_mode

    # input_radix

    # integer_grouping

    # leading_zero

    # leading_zero_mode

    # octal_mode

    # output_radix

    # precision

    # timer

    # timer_mode
    pass


# //******************************************************************************
# //
# //  runSpecialOperatorTests
# //
# //******************************************************************************

def runSpecialOperatorTests( ):
    # estimate
    testOperator( '150 amps estimate' )
    testOperator( '150 barns estimate' )
    testOperator( '150 bytes second / estimate' )
    testOperator( '150 candelas estimate' )
    testOperator( '150 cd meter meter * / estimate' )
    testOperator( '150 coulombs estimate' )
    testOperator( '150 cubic_feet estimate' )
    testOperator( '150 cubic_inches estimate' )
    testOperator( '150 cubic_miles estimate' )
    testOperator( '150 cubic_mm estimate' )
    testOperator( '150 cubic_nm estimate' )
    testOperator( '150 cubic_parsecs estimate' )
    testOperator( '150 days estimate' )
    testOperator( '150 degC estimate' )
    testOperator( '150 degrees estimate' )
    testOperator( '150 farads estimate' )
    testOperator( '150 feet estimate' )
    testOperator( '150 G estimate' )
    testOperator( '150 gallons estimate' )
    testOperator( '150 grams estimate' )
    testOperator( '150 GW estimate' )
    testOperator( '150 Hz estimate' )
    testOperator( '150 joules estimate' )
    testOperator( '150 K estimate' )
    testOperator( '150 kg liter / estimate' )
    testOperator( '150 light-years estimate' )
    testOperator( '150 liters estimate' )
    testOperator( '150 lumens estimate' )
    testOperator( '150 lux estimate' )
    testOperator( '150 mach estimate' )
    testOperator( '150 MB estimate' )
    testOperator( '150 megapascals estimate' )
    testOperator( '150 meter second second * / estimate' )
    testOperator( '150 mhos estimate' )
    testOperator( '150 microfarads estimate' )
    testOperator( '150 miles estimate' )
    testOperator( '150 minutes estimate' )
    testOperator( '150 months estimate' )
    testOperator( '150 mph estimate' )
    testOperator( '150 mps estimate' )
    testOperator( '150 newtons estimate' )
    testOperator( '150 ohms estimate' )
    testOperator( '150 pascal-seconds estimate' )
    testOperator( '150 pascals estimate' )
    testOperator( '150 Pg estimate' )
    testOperator( '150 picofarads estimate' )
    testOperator( '150 pounds estimate' )
    testOperator( '150 radians estimate' )
    testOperator( '150 seconds estimate' )
    testOperator( '150 sieverts estimate' )
    testOperator( '150 square_degrees estimate' )
    testOperator( '150 square_feet estimate' )
    testOperator( '150 square_inches estimate' )
    testOperator( '150 square_light-years estimate' )
    testOperator( '150 square_miles estimate' )
    testOperator( '150 square_mm estimate' )
    testOperator( '150 square_nm estimate' )
    testOperator( '150 stilbs estimate' )
    testOperator( '150 teaspoons estimate' )
    testOperator( '150 tesla estimate' )
    testOperator( '150 tons estimate' )
    testOperator( '150 tTNT estimate' )
    testOperator( '150 volts estimate' )
    testOperator( '150 watts estimate' )
    testOperator( '150 weeks estimate' )
    testOperator( '150 years estimate' )
    testOperator( 'c 150 / estimate' )

    # help - help is handled separately

    # name
    expectRPN( '0 name', 'zero' )
    expectRPN( '1 name', 'one' )
    expectRPN( '10 name', 'ten' )
    expectRPN( '100 name', 'one hundred' )
    expectRPN( '1000 name', 'one thousand' )
    expectRPN( '10000 name', 'ten thousand' )
    expectRPN( '100000 name', 'one hundred thousand' )
    expectRPN( '23 name', 'twenty-three' )
    expectRPN( '47 name', 'forty-seven' )
    expectRPN( '-1 name', 'negative one' )
    testOperator( '-a100 45 primorial name' )

    # oeis
    testOperator( '1000 oeis' )
    testOperator( '250000 randint oeis' )

    # oeis_comment
    testOperator( '1000 oeis_comment' )
    testOperator( '250000 randint oeis_comment' )

    # oeis_ex
    testOperator( '1000 oeis_ex' )
    testOperator( '250000 randint oeis_ex' )

    # oeis_name
    testOperator( '1000 oeis_name' )
    testOperator( '250000 randint oeis_name' )

    # ordinal_name
    testOperator( '-1 ordinal_name' )
    testOperator( '0 ordinal_name' )
    testOperator( '1 ordinal_name' )
    testOperator( '2 26 ** ordinal_name' )

    # random
    testOperator( 'random' )

    # random_
    testOperator( '50 random_' )

    # random_integer
    testOperator( '100 random_integer' )
    testOperator( '10 12 ^ random_integer' )

    # random_integer_
    testOperator( '23 265 random_integer_' )

    # result
    testOperator( 'result' )

    # set

    # topic

    # value
    expectRPN( '40 minutes value', 40 )


# //******************************************************************************
# //
# //  runTrigonometryOperatorTests
# //
# //******************************************************************************

def runTrigonometryOperatorTests( ):
    # acos
    testOperator( '0.8 acos' )

    # acosh
    testOperator( '0.6 acosh' )

    # acot
    testOperator( '0.4 acot' )

    # acoth
    testOperator( '0.3 acoth' )

    # acsc
    testOperator( '0.2 acsc' )

    # acsch
    testOperator( '0.67 acsch' )

    # asec
    testOperator( '0.4 asec' )

    # asech
    testOperator( '0.1 asech' )

    # asin
    testOperator( '0.8 asin' )

    # asinh
    testOperator( '0.3 asinh' )

    # atan
    testOperator( '0.2 atan' )

    # atanh
    testOperator( '0.45 atanh' )

    # cos
    testOperator( '45 degrees cos' )
    testOperator( 'pi radians cos' )

    # cosh
    testOperator( 'pi 3 / cosh' )

    # cot
    testOperator( 'pi 7 / cot' )

    # coth
    testOperator( 'pi 9 / coth' )

    # csc
    testOperator( 'pi 12 / csc' )

    # csch
    testOperator( 'pi 13 / csch' )

    # hypotenuse
    testOperator( '3 4 hypotenuse' )

    # sec
    testOperator( 'pi 7 / sec' )

    # sech
    testOperator( 'pi 7 / sech' )

    # sin
    testOperator( 'pi 2 / sin' )

    # sinh
    testOperator( 'pi 2 / sinh' )

    # tan
    testOperator( 'pi 3 / tan' )

    # tanh
    testOperator( 'pi 4 / tanh' )


# //******************************************************************************
# //
# //  runTests
# //
# //******************************************************************************

def runTests( ):
    runCommandLineOptionsTests( )
    runAlgebraOperatorTests( )
    runArithmeticOperatorTests( )
    runAstronomyOperatorTests( )
    runBitwiseOperatorTests( )
    runCalendarOperatorTests( )
    runCombinatoricOperatorTests( )
    runComplexMathOperatorTests( )
    runConstantOperatorTests( )
    runConversionOperatorTests( )
    runDateTimeOperatorTests( )
    runFunctionOperatorTests( )
    runGeometryOperatorTests( )
    runLexicographicOperatorTests( )
    runListOperatorTests( )
    runLogarithmOperatorTests( )
    runModifierOperatorTests( )
    runNumberTheoryOperatorTests( )
    runPolygonalOperatorTests( )
    runPolyhedralOperatorTests( )
    runPowersAndRootsOperatorTests( )
    runPrimeNumberOperatorTests( )
    runSettingsOperatorTests( )
    runTrigonometryOperatorTests( )

    runConvertTests( )
    runHelpTests( )

    runInternalOperatorTests( )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runTests( )

