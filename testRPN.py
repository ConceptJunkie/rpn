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

from rpn import rpn, handleOutput

from rpnMeasurement import RPNMeasurement

from testConvert import *
from testHelp import *

from mpmath import *


# //******************************************************************************
# //
# //  expectEqual
# //
# //******************************************************************************

def expectEqual( command1, command2 ):
    print( 'rpn', command1 )
    print( 'rpn', command2 )

    result1 = rpn( command1.split( ' ' ) )[ 0 ]
    result2 = rpn( command2.split( ' ' ) )[ 0 ]

    if result1 != result2:
        print( '**** error in equivalence test \'' + command1 + '\' and \'' + command2 + '\'' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
    else:
        print( 'both are equal!' )

    print( )


# //******************************************************************************
# //
# //  testRPN
# //
# //******************************************************************************

def testRPN( command ):
    print( 'rpn', command )
    result = rpn( command.split( ' ' ) )

    if not result is None:
        handleOutput( result )

    print( )


# //******************************************************************************
# //
# //  expectRPN
# //
# //******************************************************************************

def expectRPN( command, expected ):
    print( 'rpn', command )
    result = rpn( command.split( ' ' ) )[ 0 ]

    compare = None

    if isinstance( expected, list ):
        compare = [ ]

        for i in expected:
            if isinstance( i, int ) or isinstance( i, float ) or isinstance( i, complex ):
                compare.append( mpmathify( i ) )
            else:
                compare.append( i )
    else:
        if isinstance( expected, int ) or isinstance( expected, float ) or isinstance( expected, complex ):
            compare = mpmathify( expected )
        else:
            compare = expected

    if not result is None:
        if result == compare:
            print( result )
            print( 'passed!' )
        else:
            print( '**** error in test \'' + command + '\'' )
            print( '    expected: ', expected )
            print( '    but got: ', result )

            raise ValueError( 'unit test failed' )

    print( )


# //******************************************************************************
# //
# //  runCommandLineOptionsTests
# //
# //******************************************************************************

def runCommandLineOptionsTests( ):
    testRPN( '-a20 7 square_root' )

    testRPN( '100101011010011 -b 2' )
    testRPN( '120012022211222012 -b 3' )
    testRPN( 'rick -b 36' )

    testRPN( '6 8 ** -c' )

    testRPN( '-a3 7 square_root -d' )
    testRPN( '-a12 8 square_root -d5' )
    testRPN( '-a50 19 square_root -d10' )

    testRPN( '-a50 1 30 range fibonacci -g 3' )
    testRPN( '-a50 1 30 range fibonacci -g 4' )

    testRPN( '-h' )

    testRPN( '2 sqrt pi * -i' )

    testRPN( '1 10 range 3 ** -o' )

    testRPN( 'pi -p 1000' )

    testRPN( '10 100 10 range2 -r phi' )

    testRPN( '1 100 range -r2' )
    testRPN( '1 100 range -r3' )
    testRPN( '1 100 range -r4' )
    testRPN( '1 100 range -r5' )
    testRPN( '1 100 range -r6' )
    testRPN( '1 100 range -r7' )
    testRPN( '1 100 range -r8' )
    testRPN( '1 100 range -r9' )
    testRPN( '1 100 range -r10' )
    testRPN( '1 100 range -r11' )
    testRPN( '1 100 range -r12' )
    testRPN( '1 100 range -r13' )
    testRPN( '1 100 range -r14' )
    testRPN( '1 100 range -r15' )
    testRPN( '1 100 range -r16' )
    testRPN( '1 100 range -r17' )
    testRPN( '1 100 range -r18' )
    testRPN( '1 100 range -r19' )
    testRPN( '1 100 range -r20' )
    testRPN( '1 100 range -r21' )
    testRPN( '1 100 range -r22' )
    testRPN( '1 100 range -r23' )
    testRPN( '1 100 range -r24' )
    testRPN( '1 100 range -r25' )
    testRPN( '1 100 range -r26' )
    testRPN( '1 100 range -r27' )
    testRPN( '1 100 range -r28' )
    testRPN( '1 100 range -r29' )
    testRPN( '1 100 range -r30' )
    testRPN( '1 100 range -r31' )
    testRPN( '1 100 range -r32' )
    testRPN( '1 100 range -r33' )
    testRPN( '1 100 range -r34' )
    testRPN( '1 100 range -r35' )
    testRPN( '1 100 range -r36' )
    testRPN( '1 100 range -r37' )
    testRPN( '1 100 range -r38' )
    testRPN( '1 100 range -r39' )
    testRPN( '1 100 range -r40' )
    testRPN( '1 100 range -r41' )
    testRPN( '1 100 range -r42' )
    testRPN( '1 100 range -r43' )
    testRPN( '1 100 range -r44' )
    testRPN( '1 100 range -r45' )
    testRPN( '1 100 range -r46' )
    testRPN( '1 100 range -r47' )
    testRPN( '1 100 range -r48' )
    testRPN( '1 100 range -r49' )
    testRPN( '1 100 range -r50' )
    testRPN( '1 100 range -r51' )
    testRPN( '1 100 range -r52' )
    testRPN( '1 100 range -r53' )
    testRPN( '1 100 range -r54' )
    testRPN( '1 100 range -r55' )
    testRPN( '1 100 range -r56' )
    testRPN( '1 100 range -r57' )
    testRPN( '1 100 range -r58' )
    testRPN( '1 100 range -r59' )
    testRPN( '1 100 range -r60' )
    testRPN( '1 100 range -r61' )
    testRPN( '1 100 range -r62' )
    testRPN( '1 100 range -rphi' )

    testRPN( '-a1000 -d5 7 square_root -r62' )
    testRPN( '-a1000 -d5 pi -r8' )
    testRPN( '2 1 32 range ** -r16' )

    testRPN( '-t 12 14 ** 1 + factor' )
    testRPN( '1 40 range fibonacci factor -s1' )

    testRPN( '3 1 20 range ** -x' )

    testRPN( '65537 4 ** -r16 -g8 -z' )


# //******************************************************************************
# //
# //  runAlgebraOperatorTests
# //
# //******************************************************************************

def runAlgebraOperatorTests( ):
    # bell_polynomal
    testRPN( '4 5 bell_polynomial' )

    # eval_poly
    testRPN( '1 10 range 6 eval_poly' )
    testRPN( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_poly' )

    # find_poly

    # polyadd
    testRPN( '1 10 range 1 10 range polyadd' )

    # polymul
    testRPN( '1 10 range 1 10 range polymul' )

    # polypower
    testRPN( '[ 1 2 3 4 ] 5 polypower' )

    # polyprod
    testRPN( '[ [ 1 10 range ] [ 1 10 range ] [ 2 11 range ] ] polyprod' )

    # polysum
    testRPN( '[ [ 1 10 range ] [ 2 11 range ] ] polysum' )

    # solve
    testRPN( '1 8 range solve' )

    # solve2
    testRPN( '8 9 10 solve2' )

    # solve3
    testRPN( '10 -10 10 -10 solve3' )

    # solve4
    testRPN( '2 -3 2 -3 2 solve4' )


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
    testRPN( 'today 7 days +' )
    testRPN( 'today 3 weeks +' )
    testRPN( 'today 50 years +' )
    testRPN( '4 cups 13 teaspoons +' )
    testRPN( '55 mph 10 miles hour / +' )
    testRPN( '55 mph 10 meters second / +' )
    testRPN( '55 mph 10 furlongs fortnight / +' )
    testRPN( 'today 3 days add' )
    testRPN( 'today 3 weeks add' )
    testRPN( 'now 150 miles 10 furlongs fortnight / / add' )

    # ceiling
    expectRPN( '9.99999 ceiling', 10 )
    expectRPN( '-0.00001 ceiling', 0 )

    # divide
    testRPN( '12 13 divide' )
    testRPN( '10 days 7 / dhms' )
    testRPN( 'marathon 100 miles hour / / minutes convert' )
    testRPN( '2 zeta sqrt 24 sqrt / 12 *' )
    testRPN( 'now 2014-01-01 - minutes /' )

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
    testRPN( '15 mph 10 hours *' )
    testRPN( 'c m/s convert 1 nanosecond * inches convert' )
    testRPN( 'barn gigaparsec * cubic_inch convert' )

    # negative
    expectRPN( '-4 negative', 4 )
    expectRPN( '0 negative', 0 )
    expectRPN( '4 negative', -4 )

    # nearest_int
    expectRPN( '0.1 nearest_int', 0 )
    expectRPN( '4.5 nearest_int', 4 )

    # product
    testRPN( '1 10 range product' )

    # reciprocal
    testRPN( '6 7 / reciprocal' )

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
    testRPN( '1 10 range stddev' )

    # subtract
    testRPN( '3948 474 subtract' )
    testRPN( '4 cups 27 teaspoons -' )
    testRPN( '57 hectares 23 acres -' )
    testRPN( '10 Mb second / 700 MB hour / -' )
    testRPN( 'today 3 days -' )
    testRPN( 'today 3 weeks -' )
    testRPN( 'today 3 months -' )
    testRPN( 'now earth_radius 2 pi * * miles convert 4 mph / -' )
    testRPN( 'today 2 months -' )
    testRPN( 'today 1965-03-31 -' )
    testRPN( '2015-01-01 1965-03-31 -' )

    # sum
    expectRPN( '1 10 range sum', 55 )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    # astronomical_dawn

    # astronomical_dusk

    # autumnal_equinox

    # dawn

    # dusk

    # jupiter

    # latlong

    # location

    # location_info

    # mars

    # mercury

    # moon

    # moonrise

    # moonset

    # moon_antitransit

    # moon_phase

    # moon_transit

    # nautical_dawn

    # nautical_dusk

    # neptune

    # next_antitransit

    # next_first_quarter_moon

    # next_full_moon

    # next_last_quarter_moon

    # next_new_moon

    # next_rising

    # next_setting

    # next_transit

    # pluto

    # previous_antitransit

    # previous_first_quarter_moon

    # previous_full_moon

    # previous_last_quarter_moon

    # previous_new_moon

    # previous_rising

    # previous_setting

    # previous_transit

    # saturn

    # sky_location

    # solar_noon

    # summer_solstice

    # sun

    # sunrise

    # sunset

    # sun_antitransit

    # vernal_equinox

    # uranus

    # venus

    # winter_solstice
    pass


# //******************************************************************************
# //
# //  runBitwiseOperatorTests
# //
# //******************************************************************************

def runBitwiseOperatorTests( ):
    # and
    testRPN( '0x7777 0xdcba and' )

    # count_bits
    testRPN( '0xffff count_bits' )

    # nand
    testRPN( '-x 0x5543 0x7789 nand' )

    # nor
    testRPN( '-x 0x5543 0x7789 nor' )

    # not
    testRPN( '0xffffff ~' )
    testRPN( '142857 not' )
    testRPN( '-x 0xefefefefefefef not' )

    # or
    testRPN( '-x 0x5543 0x7789 or' )

    # parity
    testRPN( '0xff889d8f parity' )

    # shift_left
    testRPN( '-x 0x10 3 shift_left' )

    # shift_right
    testRPN( '-x 0x1000 4 shift_right' )

    # xor
    testRPN( '0x1939 0x3948 xor' )


# //******************************************************************************
# //
# //  runCalendarOperatorTests
# //
# //******************************************************************************

def runCalendarOperatorTests( ):
    # calendar
    testRPN( '1965-03 calendar' )
    testRPN( '2014-10 calendar' )

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
    testRPN( 'today to_julian_day' )

    # to_lilian_day

    # to_mayan

    # to_mayan_name

    # to_ordinal_date

    # to_persian

    # to_persian_name

    # year_calendar
    testRPN( '1965 year_calendar' )
    testRPN( 'today year_calendar' )


# //******************************************************************************
# //
# //  runCombinatoricOperatorTests
# //
# //******************************************************************************

def runCombinatoricOperatorTests( ):
    # bell
    testRPN( '-a43 45 bell' )

    # bernoulli
    testRPN( '16 bernoulli' )

    # binomial
    testRPN( '12 9 binomial' )
    testRPN( '-a20 -c 120 108 binomial' )

    # compositions

    # debruijn
    testRPN( '4 3 debruijn' )

    # delannoy
    testRPN( '-a80 100 delannoy' )

    # lah
    testRPN( '5 6 lah' )

    # motzkin
    testRPN( '-a25 56 motzkin' )

    # multifactorial

    # narayana
    testRPN( '6 8 narayana' )

    # nth_apery
    testRPN( '-a20 12 nth_apery' )

    # nth_catalan
    testRPN( '-a50 85 nth_catalan' )

    # partitions
    expectEqual( '-t 0 30 range partitions', '41 oeis 31 left' )

    # pell
    testRPN( '13 pell' )

    # permutations
    testRPN( '8 3 permutations' )

    # schroeder
    testRPN( '-a50 67 schroeder' )

    # sylvester
    testRPN( '45 sylvester' )


# //******************************************************************************
# //
# //  runComplexMathOperatorTests
# //
# //******************************************************************************

def runComplexMathOperatorTests( ):
    # argument
    testRPN( '3 3 i + argument' )

    # conjugate
    testRPN( '3 3 i + conjugate' )

    # i
    testRPN( '3 i' )

    # imaginary

    # real


# //******************************************************************************
# //
# //  runConstantOperatorTests
# //
# //******************************************************************************

def runConstantOperatorTests( ):
    # apery
    testRPN( 'apery' )

    # avogadro
    testRPN( '-a25 avogadro' )

    # catalan
    testRPN( 'catalan' )

    # champernowne
    testRPN( '-a100 champernowne' )

    # copeland
    testRPN( '-a 1000 copeland' )

    # default
    expectRPN( 'default', -1 )

    # e
    testRPN( 'e' )

    # eddington_number
    testRPN( 'eddington_number' )

    # electric_constant
    testRPN( 'electric_constant' )

    # euler
    testRPN( 'euler' )

    # false
    expectRPN( 'false', 0 )

    # faradays_constant
    testRPN( 'faradays_constant' )

    # fine_structure
    testRPN( 'fine_structure' )

    # glaisher
    testRPN( 'glaisher' )

    # infinity
    testRPN( 'infinity x fib x 1 - fib / limit' )
    expectEqual( 'infinity x fib x 1 - fib / limit', 'phi' )
    testRPN( 'infinity x 1/x 1 + x ** limit' )

    # itoi
    testRPN( 'itoi' )

    # khinchin
    testRPN( 'khinchin' )

    # magnetic_constant
    testRPN( 'magnetic_constant' )

    # max_char
    expectEqual( 'max_char', '2 7 ** 1 -' )

    # max_double
    testRPN( 'max_double' )

    # max_float
    testRPN( 'max_float' )

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
    testRPN( 'mertens_constant' )

    # mills
    testRPN( 'mills' )

    # min_char
    expectEqual( 'min_char', '2 7 ** negative' )

    # min_double
    testRPN( 'min_double' )

    # min_float
    testRPN( 'min_float' )

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
    testRPN( 'negative_infinity' )

    # newtons_constant
    testRPN( 'newtons_constant' )

    # omega
    testRPN( 'omega' )

    # phi
    testRPN( 'phi' )

    # pi
    testRPN( 'pi' )

    # plastic
    testRPN( 'plastic' )

    # prevost
    testRPN( 'prevost' )

    # radiation_constant
    testRPN( 'radiation_constant' )

    # robbins
    testRPN( 'robbins' )

    # rydberg_constant
    testRPN( 'rydberg_constant' )

    # silver_ratio
    testRPN( 'silver_ratio' )

    # stefan_boltzmann
    testRPN( 'stefan_boltzmann' )

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
    testRPN( '0x101 char' )

    # convert - convert is handled separately

    # dhms
    testRPN( '8 million seconds dhms' )

    # dms
    testRPN( '1 radian dms' )

    # double
    testRPN( '-x 10 20 ** double' )
    testRPN( '-x pi double' )

    # float
    testRPN( '-x 1029.3 float' )
    testRPN( 'pi float' )

    # from_unix_time
    testRPN( '1234567890 from_unix_time' )

    # long
    testRPN( '3456789012 long' )

    # longlong
    testRPN( '1234567890123456789012 longlong' )

    # hms
    testRPN( '54658 seconds hms' )

    # integer
    testRPN( '456 8 integer' )

    # invert_units
    testRPN( '30 miles gallon / invert_units' )

    # latlong_to_nac

    # make_pyth_3

    # make_pyth_4

    # make_time

    # pack
    testRPN( '-x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    # short
    testRPN( '32800 short' )

    # to_unix_time
    testRPN( '[ 2014 4 30 0 0 0 ] make_time to_unix_time' )

    # uchar
    testRPN( '290 uchar' )

    # uinteger
    testRPN( '200 8 uinteger' )

    # ulong
    testRPN( '234567890 ulong' )

    # ulonglong
    testRPN( '-a20 12345678901234567890 ulonglong' )

    # undouble
    testRPN( '0x400921fb54442d18 undouble' )
    testRPN( '0xcdcdcdcdcdcdcdcd undouble' )

    # unfloat
    testRPN( '0x40490fdb unfloat' )
    testRPN( '0xcdcdcdcd unfloat' )

    # unpack
    testRPN( '503942034 [ 3 4 5 11 4 4 ] unpack' )

    # ushort
    testRPN( '23456 ushort' )

    # ydhms
    testRPN( '14578 seconds ydhms' )


# //******************************************************************************
# //
# //  runDateTimeOperatorTests
# //
# //******************************************************************************

def runDateTimeOperatorTests( ):
    # ash_wednesday
    testRPN( '2015 ash_wednesday' )

    # dst_end
    testRPN( '2015 dst_end' )

    # dst_start
    testRPN( '2015 dst_start' )

    # easter
    testRPN( '2015 easter' )

    # election_day
    testRPN( '2015 election_day' )

    # iso_day
    testRPN( 'today iso_day' )

    # labor_day
    testRPN( '2015 labor_day' )

    # make_julian_time
    testRPN( '[ 2015 7 5 4 3 ] make_julian_time' )

    # make_iso_time

    # memorial_day
    testRPN( '2015 memorial_day' )

    # now
    testRPN( 'now' )

    # nth_weekday
    testRPN( '2015 march 4 thursday nth_weekday' )
    testRPN( '2015 march -1 thursday nth_weekday' )

    # nth_weekday_of_year
    testRPN( '2015 20 thursday nth_weekday_of_year' )
    testRPN( '2015 -1 thursday nth_weekday_of_year' )

    # presidents_day
    testRPN( '2015 presidents_day' )

    # thanksgiving
    testRPN( '2015 thanksgiving' )

    # today
    testRPN( 'today' )

    # tomorrow
    testRPN( 'tomorrow' )

    # weekday
    testRPN( 'today weekday' )

    # yesterday
    testRPN( 'yesterday' )


# //******************************************************************************
# //
# //  runFunctionOperatorTests
# //
# //******************************************************************************

def runFunctionOperatorTests( ):
    # eval
    testRPN( '10 x 5 * eval' )
    testRPN( '-a20 57 x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )

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
    testRPN( '34 inches 3 n_sphere_area' )
    testRPN( '34 square_inches 3 n_sphere_area' )
    testRPN( '34 cubic_inches 3 n_sphere_area' )

    # n_sphere_radius
    testRPN( '3 meters 4 n_sphere_radius' )
    testRPN( '3 square_meters 4 n_sphere_radius' )
    testRPN( '3 cubic_meters 4 n_sphere_radius' )

    # n_sphere_volume
    testRPN( '3 square_feet 6 nsphere_volume' )

    # polygon_area
    testRPN( '13 polygon_area' )

    # sphere_area
    testRPN( '8 inches sphere_area' )
    testRPN( '8 sq_inches sphere_area' )
    #testRPN( '8 cu_inches sphere_area' )    # not implemented yet

    # sphere_radius
    testRPN( '4 inches sphere_radius' )
    testRPN( '4 square_inches sphere_radius' )
    testRPN( '4 cubic_inches sphere_radius' )

    # sphere_volume
    testRPN( '5 inches sphere_volume' )
    #testRPN( '5 sq_inches sphere_volume' )  # not implemented yet
    testRPN( '5 cubic_in sphere_volume' )

    # triangle_area
    testRPN( '123 456 789 triangle_area' )


# //******************************************************************************
# //
# //  runInternalOperatorTests
# //
# //******************************************************************************

def runInternalOperatorTests( ):
    # _dump_aliases
    testRPN( '_dump_aliases' )

    # _dump_operators
    testRPN( '_dump_operators' )

    # _stats
    testRPN( '_stats' )


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
    testRPN( '1 9 range combine_digits' )

    # dup_digits
    testRPN( '543 2 dup_digits' )

    # find_palindrome
    testRPN( '-a30 10911 55 find_palindrome' )
    testRPN( '180 200 range 10 find_palindrome -s1' )

    # get_digits
    testRPN( '123456789 get_digits' )

    # is_palindrome
    testRPN( '101 is_palindrome' )
    testRPN( '1 22 range is_palindrome' )
    testRPN( '1234567890 is_palindrome' )

    # is_pandigital
    testRPN( '1234567890 is_pandigital' )

    # multiply_digits
    testRPN( '123456789 multiply_digits' )

    # reversal_addition
    testRPN( '-a20 89 24 reversal_addition' )
    testRPN( '-a20 80 89 range 24 reversal_addition' )
    testRPN( '-a20 89 16 24 range reversal_addition' )
    testRPN( '-a90 14,104,229,999,995 185 reversal_addition' )
    testRPN( '-a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    # reverse_digits
    testRPN( '37 1 8 range * reverse_digits' )
    testRPN( '37 1 2 9 range range * reverse_digits' )

    # sum_digits
    testRPN( '2 32 ** 1 - sum_digits' )


# //******************************************************************************
# //
# //  runListOperatorTests
# //
# //******************************************************************************

def runListOperatorTests( ):
    # alternate_signs
    testRPN( '1 10 range alternate_signs' )

    # alternate_signs_2
    testRPN( '1 10 range alternate_signs_2' )

    # alternating_sum
    testRPN( '1 10 range alternating_sum' )

    # alternating_sum_2
    testRPN( '1 10 range alternating_sum_2' )

    # append
    testRPN( '1 10 range 45 50 range append' )
    testRPN( '1 10 range 11 20 range append 21 30 range append' )

    # count
    expectRPN( '1 10 range count', 10 )

    # diffs
    testRPN( '1 10 range diffs' )
    testRPN( '1 10 range fib diffs' )

    # diffs2
    testRPN( '1 10 range diffs2' )
    testRPN( '1 10 range fib diffs2' )

    # element
    testRPN( '1 10 range 5 element' )
    testRPN( '-a25 1 100 range fibonacci 55 element' )

    # exponential_range
    testRPN( '1.1 1.1 10 exponential_range' )

    # flatten
    expectEqual( '[ 1 2 [ 3 4 5 ] [ 6 [ 7 [ 8 9 ] ] 10 ] ] flatten', '1 10 range' )

    # geometric_mean
    testRPN( '1 100 range geometric_mean' )
    testRPN( '[ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    # geometric_range
    testRPN( '2 8 8 geometric_range' )

    # group_elements

    # interleave
    testRPN( '1 10 range 1 10 range interleave' )

    # intersection
    testRPN( '1 10 range 1 8 range intersection' )

    # left
    testRPN( '1 10 range 5 left' )

    # max_index
    testRPN( '1 10 range max_index' )

    # min_index
    testRPN( '1 10 range min_index' )

    # nonzero
    testRPN( '1 10 range nonzero' )

    # occurrences
    testRPN( '4 100 random_integer_ occurrences' )

    # range
    testRPN( '1 23 range' )

    # range2
    testRPN( '1 23 2 range2' )

    # ratios
    testRPN( '1 10 range ratios' )

    # reduce
    testRPN( '[ 4 8 12 ] reduce' )

    # reverse
    testRPN( '1 10 range reverse' )
    testRPN( '1 2 10 range range reverse' )
    testRPN( '1 2 10 range reverse range reverse' )
    testRPN( '1 2 10 range reverse range' )

    # right
    testRPN( '1 10 range 5 right' )

    # shuffle

    # slice
    testRPN( '1 10 range 3 5 slice' )
    testRPN( '1 10 range 2 -5 slice' )

    # sort
    testRPN( '10 1 -1 range2 sort' )

    # sort_descending
    testRPN( '1 10 range sort_descending' )

    # sublist
    testRPN( '1 10 range 1 5 sublist' )

    # union
    testRPN( '1 10 range 11 20 range union' )

    # unique
    testRPN( '1 10 range unique' )
    testRPN( '1 10 range 1 10 range append unique' )
    testRPN( '[ 1 10 range 10 dup ] unique' )

    # zero
    testRPN( '-10 10 range zero' )
    testRPN( '1 10 range zero' )


# //******************************************************************************
# //
# //  runLogarithmOperatorTests
# //
# //******************************************************************************

def runLogarithmOperatorTests( ):
    # lambertw
    testRPN( '5 lambertw' )

    # li
    testRPN( '12 li' )

    # ln
    testRPN( '1000 ln' )

    # log10
    testRPN( '1000 log10' )

    # log2
    testRPN( '1000 log2' )

    # logxy
    testRPN( '6561 3 logxy' )

    # polylog
    testRPN( '9 3 polylog' )


# //******************************************************************************
# //
# //  runModifierOperatorTests
# //
# //******************************************************************************

def runModifierOperatorTests( ):
    # [

    # ]

    # {
    testRPN( '"Leesburg, VA" location today { sunrise sunset moonrise moonset }' )

    # }
    testRPN( '1 10 range { is_prime is_pronic is_semiprime }' )

    # dup_term
    testRPN( '[ 1 2 10 dup_term ] cf' )

    # dup_operator
    testRPN( '2 5 dup_operator sqr' )
    testRPN( '4 6 5 dup_operator *' )

    # previous
    expectRPN( '6 previous *', 36 )

    # unlist
    testRPN( '[ 1 2 ] unlist +' )

    # use_members


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    # aliquot
    testRPN( '276 10 aliquot' )

    # alternating_factorial
    testRPN( '13 alternating_factorial' )
    testRPN( '-a20 1 20 range alternating_factorial' )

    # base
    testRPN( '1 10 range 2 base' )
    testRPN( '1 10 range 3 base' )
    testRPN( '1 10 range 4 base' )
    testRPN( '1 10 range 5 base' )
    testRPN( '1 10 range 6 base' )
    testRPN( '1 10 range 7 base' )
    testRPN( '1 10 range 8 base' )
    testRPN( '1 10 range 9 base' )

    testRPN( '-a30 1 20 range 11 base' )
    testRPN( '-a30 1 20 range 12 base' )
    testRPN( '-a30 1 20 range 13 base' )
    testRPN( '-a30 1 20 range 14 base' )
    testRPN( '-a30 1 20 range 15 base' )
    testRPN( '-a30 1 20 range 16 base' )
    testRPN( '-a30 1 20 range 17 base' )
    testRPN( '-a30 1 20 range 18 base' )
    testRPN( '-a30 1 20 range 19 base' )
    testRPN( '-a30 1 20 range 20 base' )

    # carol
    testRPN( '-a500 773 carol' )

    # cf
    testRPN( '1 10 range cf' )

    # count_divisors
    testRPN( '1024 count_divisors' )

    # crt
    testRPN( '1 3 range 10 20 range 3 primes crt' )

    # divisors
    testRPN( '2 3 ** 3 4 ** * divisors' )
    testRPN( '12 ! divisors' )

    # double_factorial
    testRPN( '9 double_factorial' )

    # ecm
    testRPN( '-a40 10 30 ** random_integer ecm' )

    # egypt
    testRPN( '45 67 egypt' )

    # euler_brick
    testRPN( '2 3 make_pyth_3 unlist euler_brick' )

    # euler_phi
    testRPN( '1 20 range euler_phi' )

    # factor
    testRPN( '883847311 factor' )
    testRPN( '1 40 range fibonacci factor -s1' )

    # factorial
    testRPN( '-a25 23 factorial' )

    # fibonacci
    testRPN( '1 50 range fibonacci' )
    testRPN( '-c -a 8300 39399 fibonacci' )

    # fibonorial
    testRPN( '5 fibonorial' )
    testRPN( '-a50 24 fibonorial' )

    # fraction
    testRPN( '12 23 fraction' )

    # frobenius
    testRPN( '10 20 range 3 primes frobenius' )

    # gamma
    testRPN( '3 gamma' )

    # harmonic
    testRPN( '34 harmonic' )

    # heptanacci
    testRPN( '224623 heptanacci' )

    # hexanacci
    testRPN( '949 hexanacci' )

    # hyperfactorial
    testRPN( '-a160 17 hyperfactorial' )

    # is_abundant
    testRPN( '1 20 range is_abundant' )

    # is_achilles
    testRPN( '1 20 range is_achilles' )

    # is_deficient
    testRPN( '1 20 range is_deficient' )

    # is_k_semiprime
    testRPN( '1 20 range 3 is_k_semiprime' )

    # is_perfect
    testRPN( '1 30 range is_perfect' )

    # is_prime
    testRPN( '1000 1030 range is_prime' )
    testRPN( '2049 is_prime' )
    testRPN( '92348759911 is_prime' )

    # is_pronic
    testRPN( '1 20 range is_pronic' )

    # is_powerful
    testRPN( '1 20 range is_powerful' )

    # is_rough
    testRPN( '1 20 range is_rough' )

    # is_semiprime
    testRPN( '12 is_semiprime' )

    # is_smooth
    testRPN( '3 4 is_smooth' )
    testRPN( '2 1 20 is_smooth' )

    # is_sphenic
    testRPN( '[ 2 3 5 ] prime is_sphenic' )

    # is_squarefree
    testRPN( '2013 sqr is_squarefree' )
    testRPN( '8 primorial is_squarefree' )
    testRPN( '1 20 range is_squarefree' )

    # is_unusual
    testRPN( '-a50 81 23 ** is_unusual' )
    testRPN( '1 20 range is_unusual' )

    # jacobsthal
    testRPN( '10 jacobsthal' )

    # kynea
    testRPN( '8 kynea' )

    # leonardo
    testRPN( '1 10 range leonardo' )

    # leyland
    testRPN( '7 8 leyland' )

    # lgamma
    testRPN( '10 lgamma' )

    # linear_recurrence
    testRPN( '1 10 range 2 5 range 17 linear_recur' )

    # lucas
    testRPN( '-a21 99 lucas' )

    # make_cf
    testRPN( 'e 20 make_cf' )

    # mertens
    testRPN( '20 mertens' )
    testRPN( '1 10 range mertens' )

    # mobius
    testRPN( '20176 mobius' )
    testRPN( '1 20 range mobius' )

    # padovan
    testRPN( '76 padovan' )
    testRPN( '1 20 range padovan' )

    # pascal_triangle
    testRPN( '12 pascal_triangle' )
    testRPN( '1 10 range pascal_triangle -s1' )

    # pentanacci
    testRPN( '16 pentanacci' )

    # polygamma
    testRPN( '4 5 polygamma' )

    # repunit
    testRPN( '-a20 23 5 repunit' )

    # riesel
    testRPN( '23 riesel' )

    # sigma
    testRPN( '1 20 range sigma' )

    # subfactorial
    testRPN( '-a20 19 subfactorial' )

    # superfactorial
    testRPN( '-a50 12 superfactorial' )

    # tetranacci
    testRPN( '-a30 87 tetranacci' )

    # thabit
    testRPN( '-a20 45 thabit' )

    # tribonacci
    testRPN( '1 20 range tribonacci' )
    testRPN( '-c -a 2800 10239 tribonacci' )

    # unit_roots
    testRPN( '7 unit_roots' )

    # zeta
    testRPN( '4 zeta' )


# //******************************************************************************
# //
# //  runPolygonalOperatorTests
# //
# //******************************************************************************

def runPolygonalOperatorTests( ):
    # centered_decagonal
    testRPN( '17 centered_decagonal' )

    # centered_decagonal?
    testRPN( '1000 centered_decagonal?' )

    # centered_heptagonal
    testRPN( '102 centered_heptagonal' )

    # centered_heptagonal?
    testRPN( '100000 centered_heptagonal?' )

    # centered_hexagonal
    testRPN( '103 centered_hexagonal' )

    # centered_hexagonal?

    # centered_nonagonal
    testRPN( '104 centered_nonagonal' )

    # centered_nonagonal?
    testRPN( '5,000,000 centered_nonagonal?' )

    # centered_octagonal
    testRPN( '10 centered_octagonal' )

    # centered_octagonal?
    testRPN( '361 centered_octagonal?' )

    # centered_pentagonal
    testRPN( '108 centered_pentagonal' )

    # centered_pentagonal?
    testRPN( '9999 centered_pentagonal?' )

    # centered_polygonal
    testRPN( '108 5 centered_polygonal' )

    # centered_polygonal?
    testRPN( '9999 5 centered_polygonal?' )

    # centered_square
    testRPN( '5 centered_square' )

    # centered_square?
    testRPN( '49 centered_square?' )

    # centered_triangular
    testRPN( '100 centered_triangular' )

    # centered_triangular?
    testRPN( '10000 centered_triangular?' )

    # decagonal
    testRPN( '151 decagonal' )

    # decagonal?
    testRPN( '123454321 decagonal?' )

    # heptagonal
    testRPN( '203 heptagonal' )

    # heptagonal?
    testRPN( '99999 heptagonal?' )

    # heptagonal_hexagonal
    testRPN( '2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal
    testRPN( '8684 heptagonal_pentagonal' )

    # heptagonal_square
    testRPN( '222 heptagonal_square' )

    # heptagonal_triangular
    testRPN( '399 heptagonal_triangular' )

    # hexagonal
    testRPN( '340 hexagonal' )

    # hexagonal?
    testRPN( '230860 hexagonal?' )

    # hexagonal_pentagonal
    testRPN( '107 hexagonal_pentagonal' )

    # hexagonal_square
    testRPN( '-a70 23 hexagonal_square' )

    # nonagonal
    testRPN( '554 nonagonal' )

    # nonagonal?
    testRPN( '9 6 ** nonagonal?' )

    # nonagonal_heptagonal
    testRPN( '-a50 12 nonagonal_heptagonal' )

    # nonagonal_hexagonal
    testRPN( '-a60 13 nonagonal_hexagonal' )

    # nonagonal_octagonal
    testRPN( '-a 75 14 nonagonal_octagonal' )

    # nonagonal_pentagonal
    testRPN( '-a60 15 nonagonal_pentagonal' )

    # nonagonal_square
    testRPN( '-a22 16 nonagonal_square' )

    # nonagonal_triangular
    testRPN( '-a21 17 nonagonal_triangular' )

    # octagonal
    testRPN( '102 octagonal' )

    # octagonal?
    testRPN( '8 4 ** 1 + octagonal?' )

    # octagonal_heptagonal
    testRPN( '-a40 8 octagonal_heptagonal' )

    # octagonal_hexagonal
    testRPN( '-a30 7 octagonal_hexagonal' )

    # octagonal_pentagonal
    testRPN( '-a15 6 octagonal_pentagonal' )

    # octagonal_square
    testRPN( '-a25 11 octagonal_square' )

    # octagonal_triangular
    testRPN( '-a20 10 octagonal_triangular' )

    # pentagonal
    testRPN( '16 pentagonal' )

    # pentagonal?
    testRPN( '5 5 ** 5 + pentagonal?' )

    # pentagonal_square
    testRPN( '-a70 10 pentagonal_square' )

    # pentagonal_triangular
    testRPN( '-a40 17 pentagonal_triangular' )

    # polygonal
    testRPN( '9 12 polygonal' )

    # polygonal?
    testRPN( '12 12 ** 12 polygonal?' )

    # square_triangular
    testRPN( '-a60 34 square_triangular' )

    # triangular
    testRPN( '203 triangular' )

    # triangular?
    testRPN( '20706 triangular?' )


# //******************************************************************************
# //
# //  runPolyhedralOperatorTests
# //
# //******************************************************************************

def runPolyhedralOperatorTests( ):
    # centered_cube
    testRPN( '100 centered_cube' )

    # dodecahedral
    testRPN( '44 dodecahedral' )

    # icosahedral
    testRPN( '100 icosahedral' )

    # polytope
    testRPN( '1 10 range 7 polytope' )
    testRPN( '10 2 8 range polytope' )
    testRPN( '1 10 range 2 8 range polytope' )
    testRPN( '-a20 -c 18 47 polytope' )

    # pyramid
    testRPN( '304 pyramid' )

    # rhombdodec
    testRPN( '89 rhombdodec' )

    # stella_octangula
    testRPN( '3945 stella_octangula' )

    # tetrahedral
    testRPN( '-a20 19978 tetrahedral' )

    # truncated_octahedral
    testRPN( '394 truncated_octahedral' )

    # truncated_tetrahedral
    testRPN( '683 truncated_tetrahedral' )

    # octahedral
    testRPN( '23 octahedral' )

    # pentatope
    testRPN( '12 pentatope' )


# //******************************************************************************
# //
# //  runPowersAndRootsOperatorTests
# //
# //******************************************************************************

def runPowersAndRootsOperatorTests( ):
    # cube
    testRPN( '3 cube' )

    # cube_root
    testRPN( 'pi cube_root' )

    # exp
    testRPN( '13 exp' )

    # exp10
    testRPN( '12 exp10' )

    # expphi
    testRPN( '100 expphi' )

    # hyper4_2
    testRPN( '-a160 4 3 hyper4_2' )

    # power
    testRPN( '4 5 power' )
    testRPN( '4 1 i power' )
    testRPN( '1 10 range 2 10 range power' )

    # powmod
    testRPN( '43 67 9 powmod' )

    # root
    testRPN( '8 3 root' )

    # root2
    testRPN( '2 square_root' )

    # square
    testRPN( '45 square' )

    # tetrate
    testRPN( '3 2 tetrate' )

    # tower
    testRPN( '-c -a30 [ 2 3 2 ] tower' )

    # tower2
    testRPN( '[ 4 4 4 ] tower2' )


# //******************************************************************************
# //
# //  runPrimeNumberOperatorTests
# //
# //******************************************************************************

def runPrimeNumberOperatorTests( ):
    # balanced_prime
    testRPN( '1 10 range balanced' )
    testRPN( '53 balanced' )
    testRPN( '153 balanced' )
    testRPN( '2153 balanced' )

    # balanced_prime_
    testRPN( '1 10 range balanced_' )
    testRPN( '53 balanced_' )
    testRPN( '153 balanced_' )
    testRPN( '2153 balanced_' )

    # cousin_prime
    testRPN( '1 10 range cousin_prime' )
    testRPN( '77 cousin_prime' )
    testRPN( '5176 cousin_prime' )

    # cousin_prime_
    testRPN( '1 10 range cousin_prime_' )
    testRPN( '4486 cousin_prime_' )
    testRPN( '192765 cousin_prime_' )

    # double_balanced
    testRPN( '1 5 range double_balanced' )
    testRPN( '54 double_balanced' )
    testRPN( '82154 double_balanced' )

    # double_balanced_
    testRPN( '1 5 range double_balanced_' )
    testRPN( '54 double_balanced_' )
    testRPN( '100000 double_balanced_' )

    # isolated_prime
    testRPN( '102 isolated_prime' )
    testRPN( '1902 isolated_prime' )

    # next_prime
    testRPN( '1 100 range next_prime' )
    testRPN( '35 next_prime' )
    testRPN( '8783 next_prime' )
    testRPN( '142857 next_prime' )
    testRPN( '-c 6 13 ** 1 + next_prime' )
    testRPN( '-c 7 13 ** 1 + next_prime' )

    # nth_prime?
    testRPN( '1 10 range nth_prime?' )
    testRPN( '67 nth_prime?' )
    testRPN( '16467 nth_prime?' )
    testRPN( '-c 13,000,000,000 nth_prime?' )
    testRPN( '-c 256,000,000,000 nth_prime?' )

    # nth_quad?
    testRPN( '1 100000 10000 range2 nth_quad?' )
    testRPN( '453456 nth_quad?' )
    testRPN( '74,000,000,000 nth_quad?' )

    # polyprime
    testRPN( '1 5 range 1 5 range polyprime' )
    testRPN( '4 3 polyprime' )
    testRPN( '5 8 polyprime' )

    # prime
    testRPN( '1 101 range prime' )
    testRPN( '8783 prime' )
    testRPN( '142857 prime' )
    testRPN( '367981443 prime' )
    testRPN( '9113486725 prime' )

    # primepi
    testRPN( '87 primepi' )

    # primes
    testRPN( '1 5 range 5 primes' )
    testRPN( '1 1 5 range primes' )
    testRPN( '2 1 5 range primes' )
    testRPN( '3 1 5 range primes' )
    testRPN( '4 1 5 range primes' )
    testRPN( '150 10 primes' )
    testRPN( '98765 20 primes' )
    testRPN( '176176176 25 primes' )
    testRPN( '11,000,000,000 25 primes' )

    # primorial
    testRPN( '1 10 range primorial' )

    # quadruplet_prime?
    testRPN( '8 quadruplet_prime?' )
    testRPN( '8871 quadruplet_prime?' )

    # quadruplet_prime
    testRPN( '17 quadruplet_prime' )
    testRPN( '99831 quadruplet_prime' )

    # quadruplet_prime_
    testRPN( '17 quadruplet_prime_' )
    testRPN( '55731 quadruplet_prime_' )

    # quintuplet_prime?
    testRPN( '147951 quintuplet_prime?' )
    testRPN( '2,300,000 quintuplet_prime?' )

    # quintuplet_prime
    testRPN( '18 quintuplet_prime' )
    testRPN( '9387 quintuplet_prime' )

    # quintuplet_prime_
    testRPN( '62 quintuplet_prime_' )
    testRPN( '74238 quintuplet_prime_' )

    # safe_prime
    testRPN( '45 safe_prime' )
    testRPN( '5199846 safe_prime' )

    # sextuplet_prime
    testRPN( '29 sextuplet_prime' )
    testRPN( '1176 sextuplet_prime' )
    testRPN( '556 sextuplet_prime' )

    # sextuplet_prime_
    testRPN( '1 sextuplet_prime_' )
    testRPN( '587 sextuplet_prime_' )
    testRPN( '835 sextuplet_prime_' )
    testRPN( '29 sextuplet_prime_' )

    # sexy_prime
    testRPN( '-c 89,999,999 sexy_prime' )
    testRPN( '1 sexy_prime' )
    testRPN( '1487 sexy_prime' )
    testRPN( '2 sexy_prime' )
    testRPN( '23235 sexy_prime' )
    testRPN( '29 sexy_prime' )

    # sexy_prime_
    testRPN( '1 10 range sexy_prime_' )
    testRPN( '29 sexy_prime_' )
    testRPN( '21985 sexy_prime_' )
    testRPN( '-c 100,000,000 sexy_prime_' )

    # sexy_triplet
    testRPN( '1 10 range sexy_triplet' )
    testRPN( '29 sexy_triplet' )
    testRPN( '-c 593847 sexy_triplet' )
    testRPN( '-c 8574239 sexy_triplet' )

    # sexy_triplet_
    testRPN( '1 10 range sexy_triplet_' )
    testRPN( '52 sexy_triplet_' )
    testRPN( '5298 sexy_triplet_' )
    testRPN( '-c 10984635 sexy_triplet_' )

    # sexy_quadruplet
    testRPN( '1 10 range sexy_quadruplet' )
    testRPN( '29 sexy_quadruplet' )
    testRPN( '-c 289747 sexy_quadruplet' )

    # sexy_quadruplet_
    testRPN( '1 10 range sexy_quadruplet_' )
    testRPN( '29 sexy_quadruplet_' )
    testRPN( '2459 sexy_quadruplet_' )

    # sophie_prime
    testRPN( '1 10 range sophie_prime' )
    testRPN( '87 sophie_prime' )
    testRPN( '6,500,000 sophie_prime' )

    # superprime
    testRPN( '89 superprime' )

    # triple_balanced
    testRPN( '1 10 range triple_balanced' )
    testRPN( '5588 triple_balanced' )

    # triple_balanced_
    testRPN( '1 10 range triple_balanced_' )
    testRPN( '6329 triple_balanced_' )

    # triplet_prime
    testRPN( '1 10 range triplet_prime' )
    testRPN( '192834 triplet_prime' )

    # triplet_prime_
    testRPN( '1 10 range triplet_prime_' )
    testRPN( '192834 triplet_prime_' )

    # twin_prime
    testRPN( '1 10 range twin_prime_' )
    testRPN( '57454632 twin_prime_' )

    # twin_prime_
    testRPN( '1 20 range twin_prime' )
    testRPN( '39485 twin_prime' )


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
    testRPN( '150 amps estimate' )
    testRPN( '150 barns estimate' )
    testRPN( '150 bytes second / estimate' )
    testRPN( '150 candelas estimate' )
    testRPN( '150 cd meter meter * / estimate' )
    testRPN( '150 coulombs estimate' )
    testRPN( '150 cubic_feet estimate' )
    testRPN( '150 cubic_inches estimate' )
    testRPN( '150 cubic_miles estimate' )
    testRPN( '150 cubic_mm estimate' )
    testRPN( '150 cubic_nm estimate' )
    testRPN( '150 cubic_parsecs estimate' )
    testRPN( '150 days estimate' )
    testRPN( '150 degC estimate' )
    testRPN( '150 degrees estimate' )
    testRPN( '150 farads estimate' )
    testRPN( '150 feet estimate' )
    testRPN( '150 G estimate' )
    testRPN( '150 gallons estimate' )
    testRPN( '150 grams estimate' )
    testRPN( '150 GW estimate' )
    testRPN( '150 Hz estimate' )
    testRPN( '150 joules estimate' )
    testRPN( '150 K estimate' )
    testRPN( '150 kg liter / estimate' )
    testRPN( '150 light-years estimate' )
    testRPN( '150 liters estimate' )
    testRPN( '150 lumens estimate' )
    testRPN( '150 lux estimate' )
    testRPN( '150 mach estimate' )
    testRPN( '150 MB estimate' )
    testRPN( '150 megapascals estimate' )
    testRPN( '150 meter second second * / estimate' )
    testRPN( '150 mhos estimate' )
    testRPN( '150 microfarads estimate' )
    testRPN( '150 miles estimate' )
    testRPN( '150 minutes estimate' )
    testRPN( '150 months estimate' )
    testRPN( '150 mph estimate' )
    testRPN( '150 mps estimate' )
    testRPN( '150 newtons estimate' )
    testRPN( '150 ohms estimate' )
    testRPN( '150 pascal-seconds estimate' )
    testRPN( '150 pascals estimate' )
    testRPN( '150 Pg estimate' )
    testRPN( '150 picofarads estimate' )
    testRPN( '150 pounds estimate' )
    testRPN( '150 radians estimate' )
    testRPN( '150 seconds estimate' )
    testRPN( '150 sieverts estimate' )
    testRPN( '150 square_degrees estimate' )
    testRPN( '150 square_feet estimate' )
    testRPN( '150 square_inches estimate' )
    testRPN( '150 square_light-years estimate' )
    testRPN( '150 square_miles estimate' )
    testRPN( '150 square_mm estimate' )
    testRPN( '150 square_nm estimate' )
    testRPN( '150 stilbs estimate' )
    testRPN( '150 teaspoons estimate' )
    testRPN( '150 tesla estimate' )
    testRPN( '150 tons estimate' )
    testRPN( '150 tTNT estimate' )
    testRPN( '150 volts estimate' )
    testRPN( '150 watts estimate' )
    testRPN( '150 weeks estimate' )
    testRPN( '150 years estimate' )
    testRPN( 'c 150 / estimate' )

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
    testRPN( '-a100 45 primorial name' )

    # oeis
    testRPN( '1000 oeis' )
    testRPN( '250000 randint oeis' )

    # oeis_comment
    testRPN( '1000 oeis_comment' )
    testRPN( '250000 randint oeis_comment' )

    # oeis_ex
    testRPN( '1000 oeis_ex' )
    testRPN( '250000 randint oeis_ex' )

    # oeis_name
    testRPN( '1000 oeis_name' )
    testRPN( '250000 randint oeis_name' )

    # ordinal_name
    testRPN( '-1 ordinal_name' )
    testRPN( '0 ordinal_name' )
    testRPN( '1 ordinal_name' )
    testRPN( '2 26 ** ordinal_name' )

    # random
    testRPN( 'random' )

    # random_
    testRPN( '50 random_' )

    # random_integer
    testRPN( '100 random_integer' )
    testRPN( '10 12 ^ random_integer' )

    # random_integer_
    testRPN( '23 265 random_integer_' )

    # result
    testRPN( 'result' )

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
    testRPN( '0.8 acos' )

    # acosh
    testRPN( '0.6 acosh' )

    # acot
    testRPN( '0.4 acot' )

    # acoth
    testRPN( '0.3 acoth' )

    # acsc
    testRPN( '0.2 acsc' )

    # acsch
    testRPN( '0.67 acsch' )

    # asec
    testRPN( '0.4 asec' )

    # asech
    testRPN( '0.1 asech' )

    # asin
    testRPN( '0.8 asin' )

    # asinh
    testRPN( '0.3 asinh' )

    # atan
    testRPN( '0.2 atan' )

    # atanh
    testRPN( '0.45 atanh' )

    # cos
    testRPN( '45 degrees cos' )
    testRPN( 'pi radians cos' )

    # cosh
    testRPN( 'pi 3 / cosh' )

    # cot
    testRPN( 'pi 7 / cot' )

    # coth
    testRPN( 'pi 9 / coth' )

    # csc
    testRPN( 'pi 12 / csc' )

    # csch
    testRPN( 'pi 13 / csch' )

    # hypotenuse
    testRPN( '3 4 hypotenuse' )

    # sec
    testRPN( 'pi 7 / sec' )

    # sech
    testRPN( 'pi 7 / sech' )

    # sin
    testRPN( 'pi 2 / sin' )

    # sinh
    testRPN( 'pi 2 / sinh' )

    # tan
    testRPN( 'pi 3 / tan' )

    # tanh
    testRPN( 'pi 4 / tanh' )


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

