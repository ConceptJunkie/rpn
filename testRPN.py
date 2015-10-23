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
import sys

from collections import OrderedDict

from rpnMeasurement import RPNMeasurement
from rpnTestUtils import *
from testConvert import *
from testHelp import *

from mpmath import *


# //******************************************************************************
# //
# //  testOperator just evaluates an RPN expression to make sure nothing throws
# //  an exception.
# //
# //  expectResult actually tests that the result from RPN matches the value
# //  given.
# //
# //  expectEqual evaluates two RPN expressions and verifies that the results
# //  are the same.
# //
# //  expectEquivalent evaluates two RPN expressions and verifies that the
# //  results are equivalent.  This means that if the results are lists, they
# //  need to have the same elements, but not necessarily be in the same order.
# //
# //******************************************************************************

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
    testOperator( '5 5 10 range bell_polynomial' )

    from rpnUtils import downloadOEISSequence

    bell_terms = downloadOEISSequence( 106800 )

    bell_term_offsets = [ ]

    total = 0

    polynomials_to_check = 10

    for i in range( 1, polynomials_to_check + 2 ):
        bell_term_offsets.append( total )
        total += i

    for i in range( 0, polynomials_to_check ):
        bell_poly = bell_terms[ bell_term_offsets[ i ] : bell_term_offsets[ i + 1 ] ]

        bell_poly_str = '[ '
        bell_poly_str += ' '.join( [ str( k ) for k in bell_poly ] )

        bell_poly_str += ' ] '

        for j in [ -300, -84, -1, 0, 1, 8, 23, 157 ]:
            expectEqual( str( i ) + ' ' + str( j ) + ' bell_polynomial', bell_poly_str + str( j ) + ' eval_poly' )

    # eval_poly
    testOperator( '1 10 range 6 eval_poly' )
    testOperator( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_poly' )

    # find_poly
    testOperator( 'phi 3 find_poly' )

    # polyadd
    testOperator( '1 10 range 1 10 range polyadd' )

    # polymul
    testOperator( '1 10 range 1 10 range polymul' )

    # polypower
    testOperator( '[ 1 2 3 4 ] 5 polypower' )

    # polyprod
    testOperator( '[ 1 10 range 1 10 range 2 11 range ] polyprod' )

    # polysum
    testOperator( '[ 1 10 range 2 11 range ] polysum' )

    # solve
    testOperator( '1 8 range solve' )

    # solve2
    expectEquivalent( '1 -1 1 solve2', '[ 1 -1 1 ] solve' )
    expectEquivalent( '8 9 10 solve2', '[ 8 9 10 ] solve' )
    expectEquivalent( '-36 150 93 solve2', '[ -36 150 93 ] solve' )

    # solve3
    #expectEquivalent( '1 0 0 0 solve3', '[ 1 0 0 0 ] solve' )
    expectEquivalent( '1 0 -3 0 solve3', '[ 1 0 -3 0 ] solve' )
    expectEquivalent( '10 -10 10 -10 solve3', '[ 10 -10 10 -10 ] solve' )
    expectEquivalent( '57 -43 15 28 solve3', '[ 57 -43 15 28 ] solve' )

    # solve4
    #expectEquivalent( '1 0 -5 0 7 solve4', '[ 1 0 -5 0 7 ] solve' )
    expectEquivalent( '2 -3 2 -3 2 solve4', '[ 2 -3 2 -3 2 ] solve' )
    expectEquivalent( '54 23 -87 19 2042 solve4', '[ 54 23 -87 19 2042 ] solve' )


# //******************************************************************************
# //
# //  runArithmeticOperatorTests
# //
# //******************************************************************************

def runArithmeticOperatorTests( ):
    # abs
    expectResult( '-394 abs', 394 )
    expectResult( '0 abs', 0 )
    expectResult( '394 abs', 394 )

    # add
    expectResult( '4 3 add', 7 )
    expectResult( '3 feet 7 inches + inches convert', RPNMeasurement( mpmathify( '43' ), [ { 'inch' : 1 } ] ) )
    testOperator( 'today 7 days +' )
    testOperator( 'today 3 weeks +' )
    testOperator( 'today 50 years +' )
    testOperator( '4 cups 13 teaspoons +' )
    expectResult( '55 mph 10 miles hour / +', RPNMeasurement( mpmathify( '65' ), [ { 'mile' : 1 }, { 'hour' : -1 } ] ) )
    testOperator( '55 mph 10 meters second / +' )
    testOperator( '55 mph 10 furlongs fortnight / +' )
    testOperator( 'today 3 days add' )
    testOperator( 'today 3 weeks add' )
    testOperator( 'now 150 miles 10 furlongs fortnight / / add' )

    # ceiling
    expectResult( '9.99999 ceiling', 10 )
    expectResult( '-0.00001 ceiling', 0 )

    # divide
    testOperator( '12 13 divide' )
    testOperator( '10 days 7 / dhms' )
    testOperator( 'marathon 100 miles hour / / minutes convert' )
    testOperator( '2 zeta sqrt 24 sqrt / 12 *' )
    testOperator( 'now 2014-01-01 - minutes /' )

    # floor
    expectResult( '-0.4 floor', -1 )
    expectResult( '1 floor', 1 )
    expectResult( '3.4 floor', 3 )

    # gcd
    expectResult( '1 100 range gcd', 1 )
    expectResult( '[ 124 324 ] gcd', 4 )
    expectResult( '[ 8 64 ] gcd', 8 )

    # is_divisible
    expectResult( '1000 10000 is_divisible', 0 )
    expectResult( '10000 1000 is_divisible', 1 )
    expectResult( '12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )

    # is_equal
    expectResult( '4 3 is_equal', 0 )
    expectResult( 'pi pi is_equal', 1 )

    # is_even
    expectResult( '-2 is_even', 1 )
    expectResult( '-1 is_even', 0 )
    expectResult( '0 is_even', 1 )
    expectResult( '1 is_even', 0 )
    expectResult( '2 is_even', 1 )

    # is_greater
    expectResult( '4 3 is_greater', 1 )
    expectResult( '55 55 is_greater', 0 )
    expectResult( 'e pi is_greater', 0 )

    # is_less
    expectResult( '4 3 is_less', 0 )
    expectResult( '2 2 is_less', 0 )
    expectResult( '2 3 is_less', 1 )

    # is_not_equal
    expectResult( '4 3 is_not_equal', 1 )
    expectResult( '3 3 is_not_equal', 0 )

    # is_not_greater
    expectResult( '4 3 is_not_greater', 0 )
    expectResult( '77 77 is_not_greater', 1 )
    expectResult( '2 99 is_not_greater', 1 )

    # is_not_less
    expectResult( '4 3 is_not_less', 1 )
    expectResult( '663 663 is_not_less', 1 )
    expectResult( '-100 100 is_not_less', 0 )

    # is_not_zero
    expectResult( '-1 is_not_zero', 1 )
    expectResult( '0 is_not_zero', 0 )
    expectResult( '1 is_not_zero', 1 )

    # is_odd
    expectResult( '-2 is_odd', 0 )
    expectResult( '-1 is_odd', 1 )
    expectResult( '0 is_odd', 0 )
    expectResult( '1 is_odd', 1 )
    expectResult( '2 is_odd', 0 )

    # is_square
    expectResult( '1024 is_square', 1 )
    expectResult( '5 is_square', 0 )

    # is_zero
    expectResult( '-1 is_zero', 0 )
    expectResult( '0 is_zero', 1 )
    expectResult( '1 is_zero', 0 )

    # lcm
    expectEqual( '1 10 range lcm', '[ 2 2 2 3 3 5 7 ] prod' )

    # max
    expectResult( '1 10 range max', 10 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] max', 9 )

    # mean
    expectResult( '1 10 range mean', 5.5 )
    expectResult( '1 10000 range mean', 5000.5 )

    # min
    expectResult( '1 10 range min', 1 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] min', 2 )

    # modulo
    expectResult( '11001 100 modulo', 1 )
    expectResult( '-120 7 modulo', 6 )
    expectResult( '8875 49 modulo', 6 )
    expectResult( '199467 8876 modulo', 4195 )

    # multiply
    expectResult( '5 7 multiply', 35 )
    testOperator( '15 mph 10 hours *' )
    testOperator( 'c m/s convert 1 nanosecond * inches convert' )
    testOperator( 'barn gigaparsec * cubic_inch convert' )

    # negative
    expectResult( '-4 negative', 4 )
    expectResult( '0 negative', 0 )
    expectResult( '4 negative', -4 )

    # nearest_int
    expectResult( '0.1 nearest_int', 0 )
    expectResult( '4.5 nearest_int', 4 )

    # product
    expectEqual( '-a200 1 100 range product', '-a200 100 !' )

    # reciprocal
    expectEqual( '6 7 / reciprocal', '7 6 /' )

    # round
    expectResult( '0.1 round', 0 )
    expectResult( '4.5 round', 5 )

    # sign
    expectResult( '1 sign', 1 )
    expectResult( '0 sign', 0 )
    expectResult( '-1 sign', -1 )
    expectResult( 'infinity sign', 1 )
    expectResult( 'negative_infinity sign', -1 )

    # stddev
    testOperator( '1 10 range stddev' )

    # subtract
    testOperator( '3948 474 subtract' )
    expectResult( '4 cups 27 teaspoons - teaspoons convert', RPNMeasurement( mpmathify( '165' ), [ { 'teaspoon' : 1 } ] ) )
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
    expectResult( '1 10 range sum', 55 )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    # astronomical_dawn
    testOperator( '"Chattanooga, TN" location today astronomical_dawn' )

    # astronomical_dusk
    testOperator( '"Perth, Australia" location today astronomical_dusk' )

    # autumnal_equinox
    testOperator( '2015 autumnal_equinox' )

    # dawn
    testOperator( '"Christchurch, NZ" location today dawn' )

    # dusk
    testOperator( '"Vienna, Austria" location today dusk' )

    # jupiter
    testOperator( 'saturn "Ottawa, Canada" location today next_setting' )

    # latlong

    # location

    # location_info
    testOperator( '"Scottsdale, AZ" location_info' )

    # mars
    testOperator( 'mars "Beijing, China" location today next_transit' )

    # mercury
    testOperator( 'mercury "Los Angeles, CA" location today next_rising' )

    # moon
    testOperator( 'saturn "Burlington, VT" location today next_antitransit' )

    # moonrise
    testOperator( '"Las Cruces, NM" location today moonrise' )

    # moonset
    testOperator( '"Tacoma, WA" location today moonset' )

    # moon_antitransit
    testOperator( '"Madrid, Spain" location today moon_antitransit' )

    # moon_phase
    testOperator( 'today moon_phase' )

    # moon_transit
    testOperator( '"Riga, Latvia" location today moon_transit' )

    # nautical_dawn
    testOperator( '"Columbia, SC" location today nautical_dawn' )

    # nautical_dusk
    testOperator( '"Roanoke Rapids, NC" location today nautical_dusk' )

    # neptune
    testOperator( 'neptune "Hatfield, PA" location now next_rising' )

    # next_antitransit
    testOperator( 'saturn "Blacksburg, VA" location today next_antitransit' )

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
    testOperator( 'moon "Kyoto, Japan" location now next_setting' )

    # next_transit
    testOperator( 'moon "Oslo, Norway" location now next_transit' )

    # pluto
    testOperator( 'pluto "Johannesburg, South Africa" location now next_rising' )

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
    testOperator( 'uranus "Leesburg, VA" location now previous_setting' )

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
    testOperator( '"Salzburg, Germany" location today sunrise' )

    # sunset
    testOperator( '"New Delhi, India" location today sunset' )

    # sun_antitransit
    testOperator( '"Nice, France" location today sun_antitransit' )

    # vernal_equinox
    testOperator( '2015 vernal_equinox' )

    # uranus
    testOperator( 'uranus "Frankfurt, Germany" location today next_rising' )

    # venus
    testOperator( 'venus "Butte, Montana" location today next_rising' )

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
    expectEqual( '1 128 range parity nonzero 1 +', '69 oeis 65 left' )

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
    testOperator( '172 12 4 from_bahai' )

    # from_hebrew
    testOperator( '5776 8 6 from_hebrew' )

    # from_indian_civil
    testOperator( '1937 7 27 from_indian_civil' )

    # from_islamic
    testOperator( '1437 1 5 from_islamic' )

    # from_julian
    testOperator( '2015 10 6 from_julian' )

    # from_mayan
    testOperator( '13 0 2 15 12 from_mayan' )

    # from_persian
    testOperator( '1394 7 27 from_persian' )

    # iso_date
    testOperator( 'today iso_date' )

    # to_bahai
    testOperator( 'today to_bahai' )

    # to_bahai_name
    testOperator( 'today to_bahai_name' )

    # to_hebrew
    testOperator( 'today to_hebrew' )

    # to_hebrew_name
    testOperator( 'today to_hebrew_name' )

    # to_indian_civil
    testOperator( 'today to_indian_civil' )

    # to_indian_civil_name
    testOperator( 'today to_indian_civil_name' )

    # to_islamic
    testOperator( 'today to_islamic' )

    # to_islamic_name
    testOperator( 'today to_islamic_name' )

    # to_iso
    testOperator( 'today to_iso' )

    # to_iso_name
    testOperator( 'today to_iso_name' )

    # to_julian
    testOperator( 'today to_julian' )

    # to_julian_day
    testOperator( 'today to_julian_day' )

    # to_lilian_day
    testOperator( 'today to_lilian_day' )

    # to_mayan
    testOperator( 'today to_mayan' )

    # to_ordinal_date
    testOperator( 'today to_ordinal_date' )

    # to_persian
    testOperator( 'today to_persian' )

    # to_persian_name
    testOperator( 'today to_persian_name' )

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
    expectEqual( '-a20 0 26 range bell', '-a20 110 oeis 27 left' )

    # bernoulli
    testOperator( '16 bernoulli' )
    expectEqual( '-a20 0 39 range bernoulli', '-a20 27641 oeis 40 left 27642 oeis 40 left /' )

    # binomial
    testOperator( '12 9 binomial' )
    testOperator( '-a20 -c 120 108 binomial' )

    # compositions
    testOperator( '5 2 compositions' )
    testOperator( '6 3 compositions' )
    testOperator( '7 2 4 range compositions' )

    # debruijn
    testOperator( '4 3 debruijn' )

    # delannoy
    testOperator( '-a80 100 delannoy' )
    expectEqual( '-a20 0 22 range delannoy', '-a20 1850 oeis 23 left' )

    # lah
    testOperator( '5 6 lah' )

    # motzkin
    testOperator( '-a25 56 motzkin' )
    expectEqual( '-a20 0 29 range motzkin', '1006 oeis 30 left' )

    # multifactorial
    testOperator( '1 20 range 5 multifactorial' )
    expectEqual( '-a20 0 26 range 2 multifactorial', '6882 oeis 27 left' )
    expectEqual( '0 29 range 3 multifactorial', '7661 oeis 30 left' )
    expectEqual( '0 33 range 4 multifactorial', '7662 oeis 34 left' )
    expectEqual( '0 36 range 5 multifactorial', '85157 oeis 37 left' )
    expectEqual( '0 38 range 6 multifactorial', '85158 oeis 39 left' )
    expectEqual( '0 40 range 7 multifactorial', '114799 oeis 41 left' )
    expectEqual( '0 42 range 8 multifactorial', '114800 oeis 43 left' )
    expectEqual( '0 43 range 9 multifactorial', '114806 oeis 44 left' )

    # narayana
    testOperator( '6 8 narayana' )

    # nth_apery
    testOperator( '-a20 12 nth_apery' )

    # nth_catalan
    testOperator( '-a50 85 nth_catalan' )
    expectEqual( '-a20 1 34 2 range2 nth_catalan', '24492 oeis 17 left' )

    # partitions
    expectEqual( '-t 0 20 range partitions', '41 oeis 21 left' )

    # pell
    testOperator( '13 pell' )

    # permutations
    testOperator( '8 3 permutations' )

    # schroeder
    testOperator( '-a50 67 schroeder' )

    # sylvester
    testOperator( '45 sylvester' )
    expectEqual( '-a60 1 9 range sylvester', '-a60 58 oeis 9 left' )


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
    expectEqual( '3 i', '-9 sqrt' )

    # imaginary
    expectResult( '3 i 4 + imaginary', 3 )
    expectResult( '5 imaginary', 0 )
    expectResult( '7 i imaginary', 7 )

    # real
    expectResult( '3 i 4 + real', 4 )
    expectResult( '5 real', 5 )
    expectResult( '7 i real', 0 )


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
    expectResult( 'default', -1 )

    # e
    testOperator( 'e' )

    # eddington_number
    testOperator( 'eddington_number' )

    # electric_constant
    testOperator( 'electric_constant' )

    # euler
    testOperator( 'euler' )

    # false
    expectResult( 'false', 0 )

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
    expectResult( 'min_uchar', 0 )

    # min_ulong
    expectResult( 'min_ulong', 0 )

    # min_ulonglong
    expectResult( 'min_ulonglong', 0 )

    # min_uquadlong
    expectResult( 'min_uquadlong', 0 )

    # min_ushort
    expectResult( 'min_ushort', 0 )

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
    expectResult( 'true', 1 )

    # days of the week
    expectResult( 'monday', 1 )
    expectResult( 'tuesday', 2 )
    expectResult( 'wednesday', 3 )
    expectResult( 'thursday', 4 )
    expectResult( 'friday', 5 )
    expectResult( 'saturday', 6 )
    expectResult( 'sunday', 7 )

    # months
    expectResult( 'january', 1 )
    expectResult( 'february', 2 )
    expectResult( 'march', 3 )
    expectResult( 'april', 4 )
    expectResult( 'may', 5 )
    expectResult( 'june', 6 )
    expectResult( 'july', 7 )
    expectResult( 'august', 8 )
    expectResult( 'september', 9 )
    expectResult( 'october', 10 )
    expectResult( 'november', 11 )
    expectResult( 'december', 12 )


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
    testOperator( '"Detroit, MI" location_info latlong_to_nac' )

    # make_pyth_3
    testOperator( '12 34 make_pyth_3' )

    # make_pyth_4
    testOperator( '17 29 make_pyth_4' )

    # make_time
    testOperator( '[ 1965 03 31 ] make_time' )

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
    testOperator( '[ 2015 34 6 ] make_iso_time' )

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
    expectEqual( '-a20 0 23 range x 0 * 2 x 1 - power + 2 x power 1 - * eval', '6516 oeis 24 left' )
    expectEqual( '1 46 range x sqr 2 * 2 + eval', '5893 oeis 47 left 46 right' )

    # eval2
    testOperator( '7 8 x 2 ** y 3 ** + eval2' )

    # eval3
    testOperator( '15 4 26 x 2 ** y 3 ** + z 4 ** + eval3' )

    # filter
    testOperator( '-a20 1 80 range fib x is_prime filter' )

    # filter_by_index
    expectEqual( '0 1000 range x is_prime filter_by_index', '1 168 primes' )

    # limit
    testOperator( '0 x x / 2 -1 x / power + 1/x limit' )
    expectEqual( 'infinity x fibonacci x 1 + fibonacci / limit', 'infinity x lucas x 1 + lucas / limit' )

    # limitn
    testOperator( '0 x x / 2 -1 x / power + 1/x limitn' )

    # negate
    expectEqual( '[ 0 10 dup ] negate', '[ 1 10 dup ]' )

    # nprod
    testOperator( '-a20 -p20 -d 5 3 inf x pi / 1/x cos nprod' )

    # nsum
    expectEqual( '1 infinity x 3 ** 1/x nsum', '3 zeta' )

    # plot
    # plot2
    # plotc

    # unfilter
    expectEqual( '1 100 range x is_square unfilter', '37 oeis 90 left' )

    # unfilter_by_index
    expectEqual( '0 200 range x is_sphenic unfilter_by_index', '0 200 range x is_sphenic unfilter' )

    # x
    testOperator( '23 x 4 ** 5 x 3 ** * + x sqrt - eval' )

    # y
    testOperator( '23 57 x 4 ** 5 x 3 ** * + y sqrt - eval2' )

    # z
    testOperator( '23 57 86 x 4 ** 5 y 3 ** * + z sqrt - eval3' )


# //******************************************************************************
# //
# //  runGeometricOperatorTests
# //
# //******************************************************************************

def runGeometricOperatorTests( ):
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
# //  runGeographicOperatorTests
# //
# //******************************************************************************

def runGeographicOperatorTests( ):
    # distance
    testOperator( '"Leesburg, VA" location "Smithfield, VA" location distance' )

    # location
    testOperator( '"Uppsala, Sweden" location today moonrise' )

    # location_info
    testOperator( '"Dakar, Senegal" location_info' )


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
    expectResult( '3 4 add_digits', 34 )
    expectResult( '3 45 add_digits', 345 )
    expectResult( '34 567 add_digits', 34567 )

    # combine_digits
    expectResult( '1 9 range combine_digits', 123456789 )

    # dup_digits
    expectResult( '543 2 dup_digits', 54343 )
    expectResult( '1024 1 4 range dup_digits', [ 10244, 102424, 1024024, 10241024 ] )

    # find_palindrome
    testOperator( '-a30 10911 55 find_palindrome' )
    testOperator( '180 200 range 10 find_palindrome -s1' )

    # get_digits
    testOperator( '123456789 get_digits' )
    # expectEqual   30 oeis 85 left

    # is_palindrome
    expectResult( '101 is_palindrome', 1 )
    expectResult( '1 22 range is_palindrome', [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1234567890 is_palindrome', 0 )

    # is_pandigital
    expectResult( '1234567890 is_pandigital', 1 )
    expectResult( '123456789 is_pandigital', 0 )

    # multiply_digits
    expectEqual( '123456789 multiply_digits', '9 !' )

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
    expectResult( '1 10 range count', 10 )

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
    expectResult( '1 10 range 5 left', [ 1, 2, 3, 4, 5 ] )

    # max_index
    testOperator( '1 10 range max_index' )

    # min_index
    testOperator( '1 10 range min_index' )

    # nonzero
    testOperator( '1 10 range nonzero' )

    # occurrences
    testOperator( '4 100 random_integer_ occurrences' )

    # range
    expectResult( '1 12 range', [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ] )

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
    expectEqual( '1 10 range 5 right', '6 10 range' )

    # shuffle
    testOperator( '1 20 range shuffle' )

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
    expectResult( '1000 log10', 3 )

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
    testOperator( '[ "Philadelphia, PA" location "Raleigh, NC" location ] today sunrise' )

    # ]
    testOperator( '2 [ 4 5 6 ] eval_poly' )

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
    expectResult( '6 previous *', 36 )

    # unlist
    expectResult( '[ 1 2 ] unlist +', 3 )

    # use_members


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    from rpnNumberTheory import getNthKFibonacciNumberTheSlowWay

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
    expectEqual( '1 25 range carol', '93112 oeis 25 left' )

    # cf
    testOperator( '1 10 range cf' )

    # count_divisors
    testOperator( '1024 count_divisors' )
    expectEqual( '1 104 range count_divisors', '5 oeis 104 left' )

    # crt
    testOperator( '1 3 range 10 20 range 3 primes crt' )

    # divisors
    testOperator( '2 3 ** 3 4 ** * divisors' )
    testOperator( '12 ! divisors' )

    # double_factorial
    testOperator( '9 double_factorial' )

    # ecm
    testOperator( '-a40 10 20 ** random_integer ecm' )

    # egypt
    testOperator( '45 67 egypt' )

    # euler_brick
    testOperator( '2 3 make_pyth_3 unlist euler_brick' )

    # euler_phi
    testOperator( '1 20 range euler_phi' )
    expectEqual( '1 69 range euler_phi', '10 oeis 69 left' )

    # factor
    testOperator( '883847311 factor' )
    testOperator( '1 40 range fibonacci factor -s1' )

    # factorial
    testOperator( '-a25 -c 23 factorial' )
    expectEqual( '0 22 range !', '142 oeis 23 left' )

    # fibonacci
    testOperator( '1 50 range fibonacci' )
    testOperator( '-c -a 8300 39399 fibonacci' )
    expectEqual( '0 38 range fibonacci', '45 oeis 39 left' )
    expectResult( '0 100 range fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )

    # fibonorial
    testOperator( '5 fibonorial' )
    testOperator( '-a50 24 fibonorial' )

    # fraction
    testOperator( '2 sqrt 30 fraction' )

    # frobenius
    testOperator( '10 20 range 3 primes frobenius' )

    # gamma
    testOperator( '3 gamma' )

    # harmonic
    testOperator( '34 harmonic' )

    # heptanacci
    testOperator( '623 heptanacci' )
    expectEqual( '0 38 range heptanacci', '122189 oeis 39 left' )
    expectResult( '0 100 range heptanacci', [ getNthKFibonacciNumberTheSlowWay( i, 7 ) for i in range( 0, 101 ) ] )

    # hexanacci
    testOperator( '949 hexanacci' )
    expectEqual( '0 38 range hexanacci', '1592 oeis 39 left' )
    expectResult( '0 100 range hexanacci', [ getNthKFibonacciNumberTheSlowWay( i, 6 ) for i in range( 0, 101 ) ] )

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
    expectEqual( '0 34 range jacobsthal', '1045 oeis 35 left' )

    # kynea
    expectEqual( '-a20 1 25 range kynea', '93069 oeis 25 left' )

    # leonardo
    expectEqual( '0 37 range leonardo', '1595 oeis 38 left' )

    # leyland
    testOperator( '7 8 leyland' )

    # lgamma
    testOperator( '10 lgamma' )

    # linear_recurrence
    testOperator( '1 10 range 2 5 range 17 linear_recur' )

    # lucas
    testOperator( '-a21 99 lucas' )
    expectEqual( '0 36 range lucas', '32 oeis 37 left' )

    # make_cf
    testOperator( 'e 20 make_cf' )
    expectEqual( '-a100 2 pi * 3 2 / power 1/x 1 4 / gamma sqr * 100 make_cf', '53002 oeis 100 left' )

    # mertens
    expectEqual( '1 81 range mertens', '2321 oeis 81 left' )

    # mobius
    testOperator( '20176 mobius' )
    expectEqual( '1 77 range mobius', '8683 oeis 77 left' )

    # n_fibonacci
    expectResult( '0 100 range 2 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 5 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 10 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 10 ) for i in range( 0, 101 ) ] )
    expectResult( '1000 10 n_fibonacci', getNthKFibonacciNumberTheSlowWay( 1000, 10 ) )

    # octanacci
    testOperator( '906 octanacci' )
    expectEqual( '0 39 range octanacci', '79262 oeis 40 left' )
    expectResult( '0 100 range octanacci', [ getNthKFibonacciNumberTheSlowWay( i, 8 ) for i in range( 0, 101 ) ] )

    # padovan
    testOperator( '76 padovan' )
    expectEqual( '0 45 range padovan', '931 oeis 50 left 46 right' )

    # pascal_triangle
    testOperator( '12 pascal_triangle' )
    testOperator( '1 10 range pascal_triangle -s1' )

    # pentanacci
    testOperator( '16 pentanacci' )
    expectEqual( '-a20 0 37 range pentanacci', '-a20 1591 oeis 38 left' )
    expectResult( '0 100 range pentanacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )

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
    # A000166

    # superfactorial
    testOperator( '-a50 12 superfactorial' )
    expectEqual( ' -a50 0 12 range superfactorial', '178 oeis 13 left' )

    # tetranacci
    testOperator( '-a30 87 tetranacci' )
    expectEqual( '0 37 range tetranacci', '78 oeis 38 left' )
    expectResult( '0 100 range tetranacci', [ getNthKFibonacciNumberTheSlowWay( i, 4 ) for i in range( 0, 101 ) ] )

    # thabit
    testOperator( '-a20 45 thabit' )
    # A055010

    # tribonacci
    testOperator( '1 20 range tribonacci' )
    testOperator( '-c -a 2800 10239 tribonacci' )
    expectEqual( '0 37 range tribonacci', '73 oeis 38 left' )
    expectResult( '0 100 range tribonacci', [ getNthKFibonacciNumberTheSlowWay( i, 3 ) for i in range( 0, 101 ) ] )

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

    # decagonal_centered_square
    testOperator( '-a40 9 decagonal_centered_square' )

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

    # decagonal_centered_square
    testOperator( '-a40 9 decagonal_centered_square' )

    # decagonal_triangular
    testOperator( '-a40 13 decagonal_triangular' )

    # heptagonal
    testOperator( '203 heptagonal' )

    # heptagonal_hexagonal
    testOperator( '2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal
    testOperator( '8684 heptagonal_pentagonal' )

    # heptagonal_square
    testOperator( '222 heptagonal_square' )

    # heptagonal_triangular
    testOperator( '399 heptagonal_triangular' )
    expectEqual( '-a40 1 14 range heptagonal_triangular', '-a40 46194 oeis 14 left' )

    # hexagonal
    testOperator( '340 hexagonal' )

    # hexagonal_pentagonal
    testOperator( '107 hexagonal_pentagonal' )
    expectEqual( '-a40 1 14 range hexagonal_pentagonal', '-a40 46178 oeis 14 left' )

    # hexagonal_square
    testOperator( '-a70 23 hexagonal_square' )
    expectEqual( '-a70 1 12 range hexagonal_square', '-a40 46177 oeis 12 left' )

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

    # nth_decagonal
    testOperator( '123454321 nth_decagonal' )

    # nth_heptagonal
    testOperator( '99999 nth_heptagonal' )

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
    expectEqual( '8 3 root', '8 cube_root' )

    # root2
    expectEqual( '2 square_root', '4 4 root' )

    # square
    expectEqual( '123 square', '123 123 *' )

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

    # next_quadruplet_prime
    testOperator( '8 next_quadruplet_prime' )
    testOperator( '8871 next_quadruplet_prime' )

    # next_quintuplet_prime
    testOperator( '147951 next_quintuplet_prime' )
    testOperator( '2,300,000 next_quintuplet_prime' )

    # nth_prime
    testOperator( '1 10 range nth_prime' )
    testOperator( '67 nth_prime' )
    testOperator( '16467 nth_prime' )
    testOperator( '-c 13,000,000,000 nth_prime' )
    testOperator( '-c 256,000,000,000 nth_prime' )

    # nth_quadruplet_prime
    testOperator( '1 100000 10000 range2 nth_quadruplet_prime' )
    testOperator( '453456 nth_quadruplet_prime' )
    testOperator( '74,000,000,000 nth_quadruplet_prime' )

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
    testOperator( '87 prime_pi' )

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
    expectEqual( '1 71 primes sqrt floor', '6 oeis 71 left' )

    # primorial
    testOperator( '1 10 range primorial' )

    # quadruplet_prime
    testOperator( '17 quadruplet_prime' )
    testOperator( '99831 quadruplet_prime' )

    # quadruplet_prime_
    testOperator( '17 quadruplet_prime_' )
    testOperator( '55731 quadruplet_prime_' )

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
# //  These operators need to be tested in interactive mode.
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
    expectResult( '0 name', 'zero' )
    expectResult( '1 name', 'one' )
    expectResult( '10 name', 'ten' )
    expectResult( '100 name', 'one hundred' )
    expectResult( '1000 name', 'one thousand' )
    expectResult( '10000 name', 'ten thousand' )
    expectResult( '100000 name', 'one hundred thousand' )
    expectResult( '23 name', 'twenty-three' )
    expectResult( '47 name', 'forty-seven' )
    expectResult( '-1 name', 'negative one' )
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
    testOperator( '0 10 range ordinal_name -s1' )
    testOperator( '2 26 ** ordinal_name' )
    expectResult( '-1 ordinal_name', 'negative first' )
    expectResult( '0 ordinal_name', 'zeroth' )
    expectResult( '1 ordinal_name', 'first' )
    expectResult( '100 ordinal_name', 'one hundredth' )
    expectResult( '1000 ordinal_name', 'one thousandth' )
    expectResult( '10000 ordinal_name', 'ten thousandth' )
    expectResult( '100000 ordinal_name', 'one hundred thousandth' )

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

    # set - interactive mode

    # topic - interactive mode

    # value
    expectResult( '40 minutes value', 40 )
    expectResult( '756 light-years value', 756 )
    expectResult( '73 gallons value', 73 )


# //******************************************************************************
# //
# //  runTrigonometricOperatorTests
# //
# //******************************************************************************

def runTrigonometricOperatorTests( ):
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
# //  tests
# //
# //******************************************************************************

rpnTestList = [
    ( 'algebra',          runAlgebraOperatorTests ),
    ( 'arithmetic',       runArithmeticOperatorTests ),
    ( 'astronomy',        runAstronomyOperatorTests ),
    ( 'bitwise',          runBitwiseOperatorTests ),
    ( 'calendar',         runCalendarOperatorTests ),
    ( 'combinatoric',     runCombinatoricOperatorTests ),
    ( 'complex',          runComplexMathOperatorTests ),
    ( 'constant',         runConstantOperatorTests ),
    ( 'conversion',       runConversionOperatorTests ),
    ( 'date_time',        runDateTimeOperatorTests ),
    ( 'function',         runFunctionOperatorTests ),
    ( 'geographic',       runGeographicOperatorTests ),
    ( 'geometric',        runGeometricOperatorTests ),
    ( 'lexicographic',    runLexicographicOperatorTests ),
    ( 'list',             runListOperatorTests ),
    ( 'logarithmic',      runLogarithmOperatorTests ),
    ( 'modifier',         runModifierOperatorTests ),
    ( 'number_theory',    runNumberTheoryOperatorTests ),
    ( 'polygonal',        runPolygonalOperatorTests ),
    ( 'polyhedral',       runPolyhedralOperatorTests ),
    ( 'powers_and_roots', runPowersAndRootsOperatorTests ),
    ( 'prime_number',     runPrimeNumberOperatorTests ),
    ( 'settings',         runSettingsOperatorTests ),
    ( 'special',          runSpecialOperatorTests ),
    ( 'trigonometric',    runTrigonometricOperatorTests ),

    ( 'command-line',     runCommandLineOptionsTests ),
    ( 'convert',          runConvertTests ),
    ( 'help',             runHelpTests ),

    ( 'internal',         runInternalOperatorTests )
]

rpnTests = OrderedDict( )

for test in rpnTestList:
    rpnTests[ test[ 0 ] ] = test[ 1 ]


# //******************************************************************************
# //
# //  runTests
# //
# //******************************************************************************

def runTests( tests ):
    if len( tests ) == 0:
        for test in rpnTests:
            rpnTests[ test ]( )
    else:
        for test in tests:
            if test in rpnTests:
                rpnTests[ test ]( )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runTests( sys.argv[ 1 : ] )

