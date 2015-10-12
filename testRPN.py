
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

from testConvert import *
from testHelp import *


# //******************************************************************************
# //
# //  testEqual
# //
# //******************************************************************************

def testEqual( command1, command2 ):
    print( command1 )
    print( command2 )
    result1 = rpn( command1.split( ' ' )[ 1 : ] )[ 0 ]
    result2 = rpn( command2.split( ' ' )[ 1 : ] )[ 0 ]

    if result1 != result2:
        print( '**** error in equivalence test \'' + command1 + '\' and \'' + command2 + '\'' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
    else:
        print( 'passed!' )

    print( )


# //******************************************************************************
# //
# //  testRPN
# //
# //******************************************************************************

def testRPN( command ):
    print( command )
    result = rpn( command.split( ' ' )[ 1 : ] )[ 0 ]

    if not result is None:
        handleOutput( result )

    print( )


# //******************************************************************************
# //
# //  expectRPN
# //
# //******************************************************************************

def expectRPN( command, expected ):
    print( command )
    result = rpn( command.split( ' ' )[ 1 : ] )

    if not result is None:
        if result != expected:
            print( '**** error in test \'' + command + '\'' )
            print( '    expected: ', expected )
            print( '    but got: ', result )
        else:
            print( 'passed!' )

    print( )


# //******************************************************************************
# //
# //  runTests
# //
# //  At this point, there is no validation of the answers.  Mostly this tests
# //  that every operator works without throwing unhandled exceptions.
# //
# //******************************************************************************

def runTests( ):
    # command-line options
    testRPN( 'rpn -a20 7 square_root' )

    testRPN( 'rpn 100101011010011 -b 2' )
    testRPN( 'rpn 120012022211222012 -b 3' )
    testRPN( 'rpn rick -b 36' )

    testRPN( 'rpn 6 8 ** -c' )

    testRPN( 'rpn -a3 7 square_root -d' )
    testRPN( 'rpn -a12 8 square_root -d5' )
    testRPN( 'rpn -a50 19 square_root -d10' )

    testRPN( 'rpn -a50 1 30 range fibonacci -g 3' )
    testRPN( 'rpn -a50 1 30 range fibonacci -g 4' )

    testRPN( 'rpn -h' )

    testRPN( 'rpn 2 sqrt pi * -i' )

    testRPN( 'rpn 1 10 range 3 ** -o' )

    testRPN( 'rpn pi -p 1000' )

    testRPN( 'rpn 10 100 10 range2 -r phi' )

    testRPN( 'rpn 1 100 range -r2' )
    testRPN( 'rpn 1 100 range -r3' )
    testRPN( 'rpn 1 100 range -r4' )
    testRPN( 'rpn 1 100 range -r5' )
    testRPN( 'rpn 1 100 range -r6' )
    testRPN( 'rpn 1 100 range -r7' )
    testRPN( 'rpn 1 100 range -r8' )
    testRPN( 'rpn 1 100 range -r9' )
    testRPN( 'rpn 1 100 range -r10' )
    testRPN( 'rpn 1 100 range -r11' )
    testRPN( 'rpn 1 100 range -r12' )
    testRPN( 'rpn 1 100 range -r13' )
    testRPN( 'rpn 1 100 range -r14' )
    testRPN( 'rpn 1 100 range -r15' )
    testRPN( 'rpn 1 100 range -r16' )
    testRPN( 'rpn 1 100 range -r17' )
    testRPN( 'rpn 1 100 range -r18' )
    testRPN( 'rpn 1 100 range -r19' )
    testRPN( 'rpn 1 100 range -r20' )
    testRPN( 'rpn 1 100 range -r21' )
    testRPN( 'rpn 1 100 range -r22' )
    testRPN( 'rpn 1 100 range -r23' )
    testRPN( 'rpn 1 100 range -r24' )
    testRPN( 'rpn 1 100 range -r25' )
    testRPN( 'rpn 1 100 range -r26' )
    testRPN( 'rpn 1 100 range -r27' )
    testRPN( 'rpn 1 100 range -r28' )
    testRPN( 'rpn 1 100 range -r29' )
    testRPN( 'rpn 1 100 range -r30' )
    testRPN( 'rpn 1 100 range -r31' )
    testRPN( 'rpn 1 100 range -r32' )
    testRPN( 'rpn 1 100 range -r33' )
    testRPN( 'rpn 1 100 range -r34' )
    testRPN( 'rpn 1 100 range -r35' )
    testRPN( 'rpn 1 100 range -r36' )
    testRPN( 'rpn 1 100 range -r37' )
    testRPN( 'rpn 1 100 range -r38' )
    testRPN( 'rpn 1 100 range -r39' )
    testRPN( 'rpn 1 100 range -r40' )
    testRPN( 'rpn 1 100 range -r41' )
    testRPN( 'rpn 1 100 range -r42' )
    testRPN( 'rpn 1 100 range -r43' )
    testRPN( 'rpn 1 100 range -r44' )
    testRPN( 'rpn 1 100 range -r45' )
    testRPN( 'rpn 1 100 range -r46' )
    testRPN( 'rpn 1 100 range -r47' )
    testRPN( 'rpn 1 100 range -r48' )
    testRPN( 'rpn 1 100 range -r49' )
    testRPN( 'rpn 1 100 range -r50' )
    testRPN( 'rpn 1 100 range -r51' )
    testRPN( 'rpn 1 100 range -r52' )
    testRPN( 'rpn 1 100 range -r53' )
    testRPN( 'rpn 1 100 range -r54' )
    testRPN( 'rpn 1 100 range -r55' )
    testRPN( 'rpn 1 100 range -r56' )
    testRPN( 'rpn 1 100 range -r57' )
    testRPN( 'rpn 1 100 range -r58' )
    testRPN( 'rpn 1 100 range -r59' )
    testRPN( 'rpn 1 100 range -r60' )
    testRPN( 'rpn 1 100 range -r61' )
    testRPN( 'rpn 1 100 range -r62' )
    testRPN( 'rpn 1 100 range -rphi' )

    testRPN( 'rpn -a1000 -d5 7 square_root -r62' )
    testRPN( 'rpn -a1000 -d5 pi -r8' )
    testRPN( 'rpn 2 1 32 range ** -r16' )

    testRPN( 'rpn -t 12 14 ** 1 + factor' )
    testRPN( 'rpn 1 40 range fibonacci factor -s1' )

    testRPN( 'rpn 3 1 20 range ** -x' )

    testRPN( 'rpn 65537 4 ** -r16 -g8 -z' )


    # //******************************************************************************
    # //
    # //  algebra operators
    # //
    # //******************************************************************************

    # bell_polynomal

    testRPN( 'rpn 4 5 bell_polynomial' )

    # eval_poly

    testRPN( 'rpn 1 10 range 6 eval_poly' )
    testRPN( 'rpn [ 4 -2 3 5 -6 20 ] 1 10 range eval_poly' )

    # find_poly
    # polyadd

    testRPN( 'rpn 1 10 range 1 10 range polyadd' )

    # polymul

    testRPN( 'rpn 1 10 range 1 10 range polymul' )

    # polypower

    testRPN( 'rpn [ 1 2 3 4 ] 5 polypower' )

    # polyprod

    testRPN( 'rpn [ [ 1 10 range ] [ 1 10 range ] [ 2 11 range ] ] polyprod' )

    # polysum

    testRPN( 'rpn [ [ 1 10 range ] [ 2 11 range ] ] polysum' )

    # solve

    testRPN( 'rpn 1 8 range solve' )

    # solve2

    testRPN( 'rpn 8 9 10 solve2' )

    # solve3

    testRPN( 'rpn 10 -10 10 -10 solve3' )

    # solve4

    testRPN( 'rpn 2 -3 2 -3 2 solve4' )


    # //******************************************************************************
    # //
    # //  arithmetic operators
    # //
    # //******************************************************************************

    # abs

    expectRPN( 'rpn -394 abs', 394 )
    expectRPN( 'rpn 0 abs', 0 )
    expectRPN( 'rpn 394 abs', 394 )

    # add

    expectRPN( 'rpn 4 3 add', 7 )
    testRPN( 'rpn today 7 days +' )
    testRPN( 'rpn today 3 weeks +' )
    testRPN( 'rpn today 50 years +' )
    testRPN( 'rpn 4 cups 13 teaspoons +' )
    testRPN( 'rpn 55 mph 10 miles hour / +' )
    testRPN( 'rpn 55 mph 10 meters second / +' )
    testRPN( 'rpn 55 mph 10 furlongs fortnight / +' )
    testRPN( 'rpn today 3 days add' )
    testRPN( 'rpn today 3 weeks add' )
    testRPN( 'rpn now 150 miles 10 furlongs fortnight / / add' )

    # ceiling

    expectRPN( 'rpn 9.99999 ceiling', 10 )

    # divide

    testRPN( 'rpn 12 13 divide' )
    testRPN( 'rpn 10 days 7 / dhms' )
    testRPN( 'rpn marathon 100 miles hour / / minutes convert' )
    testRPN( 'rpn 2 zeta sqrt 24 sqrt / 12 *' )
    testRPN( 'rpn now 2014-01-01 - minutes /' )

    # floor

    expectRPN( 'rpn -0.4 floor', -1 )
    expectRPN( 'rpn 1 floor', 1 )
    expectRPN( 'rpn 3.4 floor', 3 )

    # gcd

    testRPN( 'rpn 1 100 range gcd' )

    # is_divisible

    expectRPN( 'rpn 1000 10000 is_divisible', 0 )
    expectRPN( 'rpn 10000 1000 is_divisible', 1 )
    expectRPN( 'rpn 12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    expectRPN( 'rpn 1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )

    # is_equal

    expectRPN( 'rpn 4 3 is_equal', 0 )
    expectRPN( 'rpn pi pi is_equal', 1 )

    # is_even

    expectRPN( 'rpn -2 is_even', 1 )
    expectRPN( 'rpn -1 is_even', 0 )
    expectRPN( 'rpn 0 is_even', 1 )
    expectRPN( 'rpn 1 is_even', 0 )
    expectRPN( 'rpn 2 is_even', 1 )

    # is_greater

    expectRPN( 'rpn 4 3 is_greater', 1 )
    expectRPN( 'rpn 55 55 is_greater', 0 )
    expectRPN( 'rpn e pi is_greater', 0 )

    # is_less

    expectRPN( 'rpn 4 3 is_less', 0 )
    expectRPN( 'rpn 2 2 is_less', 0 )
    expectRPN( 'rpn 2 3 is_less', 1 )

    # is_not_equal

    expectRPN( 'rpn 4 3 is_not_equal', 1 )
    expectRPN( 'rpn 3 3 is_not_equal', 0 )

    # is_not_greater

    expectRPN( 'rpn 4 3 is_not_greater', 0 )
    expectRPN( 'rpn 77 77 is_not_greater', 1 )
    expectRPN( 'rpn 2 99 is_not_greater', 1 )

    # is_not_less

    expectRPN( 'rpn 4 3 is_not_less', 1 )
    expectRPN( 'rpn 663 663 is_not_less', 1 )
    expectRPN( 'rpn -100 100 is_not_less', 0 )

    # is_not_zero

    expectRPN( 'rpn -1 is_not_zero', 1 )
    expectRPN( 'rpn 0 is_not_zero', 0 )
    expectRPN( 'rpn 1 is_not_zero', 1 )

    # is_odd

    expectRPN( 'rpn -2 is_odd', 0 )
    expectRPN( 'rpn -1 is_odd', 1 )
    expectRPN( 'rpn 0 is_odd', 0 )
    expectRPN( 'rpn 1 is_odd', 1 )
    expectRPN( 'rpn 2 is_odd', 0 )

    # is_square

    expectRPN( 'rpn 1024 is_square', 1 )
    expectRPN( 'rpn 5 is_square', 0 )

    # is_zero

    expectRPN( 'rpn -1 is_zero', 0 )
    expectRPN( 'rpn 0 is_zero', 1 )
    expectRPN( 'rpn 1 is_zero', 0 )

    # lcm

    # max

    expectRPN( 'rpn 1 10 range max', 10 )

    # mean

    expectRPN( 'rpn 1 10 range mean', 5.5 )

    # min

    expectRPN( 'rpn 1 10 range min', 1 )

    # modulo

    expectRPN( 'rpn 11001 100 modulo', 1 )

    # multiply

    expectRPN( 'rpn 5 7 multiply', 35 )
    testRPN( 'rpn 15 mph 10 hours *' )
    testRPN( 'rpn c m/s convert 1 nanosecond * inches convert' )
    testRPN( 'rpn barn gigaparsec * cubic_inch convert' )

    # negative

    expectRPN( 'rpn -4 negative', 4 )
    expectRPN( 'rpn 0 negative', 0 )
    expectRPN( 'rpn 4 negative', -4 )

    # nearest_int

    # percent

    # product

    testRPN( 'rpn 1 10 range product' )

    # reciprocal

    testRPN( 'rpn 6 7 / reciprocal' )

    # round

    testRPN( 'rpn 4.5 round' )

    # sign

    # stddev

    testRPN( 'rpn 1 10 range stddev' )

    # subtract

    testRPN( 'rpn 3948 474 subtract' )
    testRPN( 'rpn 4 cups 27 teaspoons -' )
    testRPN( 'rpn 57 hectares 23 acres -' )
    testRPN( 'rpn 10 Mb second / 700 MB hour / -' )
    testRPN( 'rpn today 3 days -' )
    testRPN( 'rpn today 3 weeks -' )
    testRPN( 'rpn today 3 months -' )
    testRPN( 'rpn now earth_radius 2 pi * * miles convert 4 mph / -' )
    testRPN( 'rpn today 2 months -' )
    testRPN( 'rpn today 1965-03-31 -' )
    testRPN( 'rpn 2015-01-01 1965-03-31 -' )

    # sum

    testRPN( 'rpn 1 10 range sum' )


    # //******************************************************************************
    # //
    # //  astronomy operators
    # //
    # //******************************************************************************

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

    # //******************************************************************************
    # //
    # //  bitwise operators
    # //
    # //******************************************************************************

    # and

    testRPN( 'rpn 0x7777 0xdcba and' )

    # count_bits

    testRPN( 'rpn 0xffff count_bits' )

    # nand
    # nor
    # not

    testRPN( 'rpn 0xffffff ~' )
    testRPN( 'rpn 142857 not' )
    testRPN( 'rpn -x 0xefefefefefefef not' )

    # or

    testRPN( 'rpn -x 0x5543 0x7789 or' )

    # parity

    testRPN( 'rpn 0xff889d8f parity' )

    # shift_left

    testRPN( 'rpn -x 0x10 3 shift_left' )

    # shift_right

    testRPN( 'rpn -x 0x1000 4 shift_right' )

    # xor

    testRPN( 'rpn 0x1939 0x3948 xor' )


    # //******************************************************************************
    # //
    # //  calendar operators
    # //
    # //******************************************************************************

    # calendar

    testRPN( 'rpn 1965-03 calendar' )
    testRPN( 'rpn 2014-10 calendar' )

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

    testRPN( 'rpn today to_julian_day' )

    # to_lilian_day
    # to_mayan
    # to_mayan_name
    # to_ordinal_date
    # to_persian
    # to_persian_name
    # year_calendar

    testRPN( 'rpn 1965 year_calendar' )
    testRPN( 'rpn today year_calendar' )

    # //******************************************************************************
    # //
    # //  combinatoric operators
    # //
    # //******************************************************************************

    # bell

    testRPN( 'rpn -a43 45 bell' )

    # bernoulli

    testRPN( 'rpn 16 bernoulli' )

    # binomial

    testRPN( 'rpn 12 9 binomial' )
    testRPN( 'rpn -a20 -c 120 108 binomial' )

    # compositions
    # debruijn

    testRPN( 'rpn 4 3 debruijn' )

    # delannoy

    testRPN( 'rpn -a80 100 delannoy' )

    # lah

    testRPN( 'rpn 5 6 lah' )

    # motzkin

    testRPN( 'rpn -a25 56 motzkin' )

    # multifactorial
    # narayana

    testRPN( 'rpn 6 8 narayana' )

    # nth_apery

    testRPN( 'rpn -a20 12 nth_apery' )

    # nth_catalan

    testRPN( 'rpn -a50 85 nth_catalan' )
    # partitions
    # pell

    testRPN( 'rpn 13 pell' )

    # permutations

    testRPN( 'rpn 8 3 permutations' )

    # schroeder

    testRPN( 'rpn -a50 67 schroeder' )

    # sylvester

    testRPN( 'rpn 45 sylvester' )


    # //******************************************************************************
    # //
    # //  complex math operators
    # //
    # //******************************************************************************

    # argument

    testRPN( 'rpn 3 3 i + argument' )

    # conjugate

    testRPN( 'rpn 3 3 i + conjugate' )

    # i

    testRPN( 'rpn 3 i' )

    # imaginary
    # real


    # //******************************************************************************
    # //
    # //  constants operators
    # //
    # //******************************************************************************

    # apery

    testRPN( 'rpn apery' )

    # avogadro

    testRPN( 'rpn -a25 avogadro' )

    # catalan

    testRPN( 'rpn catalan' )

    # champernowne

    testRPN( 'rpn -a100 champernowne' )

    # copeland

    testRPN( 'rpn -a 1000 copeland' )

    # default

    # e

    testRPN( 'rpn e' )

    # eddington_number

    testRPN( 'rpn eddington_number' )

    # electric_constant

    testRPN( 'rpn electric_constant' )

    # euler

    testRPN( 'rpn euler' )

    # false

    # faradays_constant

    testRPN( 'rpn faradays_constant' )

    # fine_structure

    testRPN( 'rpn fine_structure' )

    # glaisher

    testRPN( 'rpn glaisher' )

    # infinity

    testRPN( 'rpn infinity x fib x 1 - fib / limit' )
    testEqual( 'rpn infinity x fib x 1 - fib / limit', 'rpn phi' )
    testRPN( 'rpn infinity x 1/x 1 + x ** limit' )

    # itoi

    testRPN( 'rpn itoi' )

    # khinchin

    testRPN( 'rpn khinchin' )

    # magnetic_constant

    testRPN( 'rpn magnetic_constant' )

    # max_char

    testRPN( 'rpn max_char' )

    # max_double

    testRPN( 'rpn max_double' )

    # max_float

    testRPN( 'rpn max_float' )

    # max_long

    testRPN( 'rpn max_long' )

    # max_longlong

    testRPN( 'rpn -a20 max_longlong' )

    # max_quadlong

    testRPN( 'rpn -a40 max_quadlong' )

    # max_short

    testRPN( 'rpn max_short' )

    # max_uchar

    testRPN( 'rpn max_uchar' )

    # max_ulong

    testRPN( 'rpn max_ulong' )

    # max_ulonglong

    testRPN( 'rpn -a20 max_ulonglong' )

    # max_uquadlong

    testRPN( 'rpn -a40 max_uquadlong' )

    # max_ushort

    testRPN( 'rpn max_ushort' )

    # mertens_constant

    testRPN( 'rpn mertens_constant' )

    # mills

    testRPN( 'rpn mills' )

    # min_char

    testRPN( 'rpn min_char' )

    # min_double

    testRPN( 'rpn min_double' )

    # min_float

    testRPN( 'rpn min_float' )

    # min_long

    testRPN( 'rpn min_long' )

    # min_longlong

    testRPN( 'rpn -a20 min_longlong' )

    # min_quadlong

    testRPN( 'rpn -a40 min_quadlong' )

    # min_short

    testRPN( 'rpn min_short' )

    # min_uchar

    testRPN( 'rpn min_uchar' )

    # min_ulong

    testRPN( 'rpn min_ulong' )

    # min_ulonglong

    testRPN( 'rpn min_ulonglong' )

    # min_uquadlong

    testRPN( 'rpn min_uquadlong' )

    # min_ushort

    testRPN( 'rpn min_ushort' )

    # negative_infinity
    # newtons_constant

    testRPN( 'rpn newtons_constant' )

    # omega

    testRPN( 'rpn omega' )

    # phi

    testRPN( 'rpn phi' )

    # pi

    testRPN( 'rpn pi' )

    # plastic

    testRPN( 'rpn plastic' )

    # prevost

    testRPN( 'rpn prevost' )

    # radiation_constant

    testRPN( 'rpn radiation_constant' )

    # robbins

    testRPN( 'rpn robbins' )

    # rydberg_constant

    testRPN( 'rpn rydberg_constant' )

    # silver_ratio

    testRPN( 'rpn silver_ratio' )

    # stefan_boltzmann

    testRPN( 'rpn stefan_boltzmann' )

    # true

    # monday
    # tuesday
    # wednesday
    # thursday
    # friday
    # saturday
    # sunday

    # january
    # february
    # march
    # april
    # may
    # june
    # july
    # august
    # september
    # october
    # november
    # december

    # //******************************************************************************
    # //
    # //  conversion operators
    # //
    # //******************************************************************************

    # char

    testRPN( 'rpn 0x101 char' )

    # convert
    # dhms

    testRPN( 'rpn 8 million seconds dhms' )

    # dms

    testRPN( 'rpn 1 radian dms' )

    # double

    testRPN( 'rpn -x 10 20 ** double' )
    testRPN( 'rpn -x pi double' )

    # float

    testRPN( 'rpn -x 1029.3 float' )
    testRPN( 'rpn pi float' )

    # from_unix_time

    testRPN( 'rpn 1234567890 from_unix_time' )

    # long

    testRPN( 'rpn 3456789012 long' )

    # longlong

    testRPN( 'rpn 1234567890123456789012 longlong' )

    # hms

    testRPN( 'rpn 54658 seconds hms' )

    # integer

    testRPN( 'rpn 456 8 integer' )

    # invert_units

    testRPN( 'rpn 30 miles gallon / invert_units' )

    # latlong_to_nac
    # make_pyth_3
    # make_pyth_4
    # make_time
    # pack

    testRPN( 'rpn -x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    # short

    testRPN( 'rpn 32800 short' )

    # to_unix_time

    testRPN( 'rpn [ 2014 4 30 0 0 0 ] make_time to_unix_time' )

    # uchar

    testRPN( 'rpn 290 uchar' )

    # uinteger

    testRPN( 'rpn 200 8 uinteger' )

    # ulong

    testRPN( 'rpn 234567890 ulong' )

    # ulonglong

    testRPN( 'rpn -a20 12345678901234567890 ulonglong' )

    # undouble

    testRPN( 'rpn 0x400921fb54442d18 undouble' )
    testRPN( 'rpn 0xcdcdcdcdcdcdcdcd undouble' )

    # unfloat

    testRPN( 'rpn 0x40490fdb unfloat' )
    testRPN( 'rpn 0xcdcdcdcd unfloat' )

    # unpack

    testRPN( 'rpn 503942034 [ 3 4 5 11 4 4 ] unpack' )

    # ushort

    testRPN( 'rpn 23456 ushort' )

    # ydhms

    testRPN( 'rpn 14578 seconds ydhms' )


    # //******************************************************************************
    # //
    # //  date-time operators
    # //
    # //******************************************************************************

    # ash_wednesday
    # dst_end

    testRPN( 'rpn 2015 dst_end' )

    # dst_start

    testRPN( 'rpn 2015 dst_start' )

    # easter

    testRPN( 'rpn 2015 easter' )

    # election_day

    testRPN( 'rpn 2015 election_day' )

    # iso_day

    testRPN( 'rpn today iso_day' )

    # labor_day

    testRPN( 'rpn 2015 labor_day' )

    # make_julian_time

    testRPN( 'rpn [ 2015 7 5 4 3 ] make_julian_time' )

    # make_iso_time
    # memorial_day

    testRPN( 'rpn 2015 memorial_day' )

    # now

    testRPN( 'rpn now' )

    # nth_weekday

    testRPN( 'rpn 2015 march 4 thursday nth_weekday' )
    testRPN( 'rpn 2015 march -1 thursday nth_weekday' )

    # nth_weekday_of_year

    testRPN( 'rpn 2015 20 thursday nth_weekday_of_year' )
    testRPN( 'rpn 2015 -1 thursday nth_weekday_of_year' )

    # presidents_day

    testRPN( 'rpn 2015 presidents_day' )

    # thanksgiving

    testRPN( 'rpn 2015 thanksgiving' )

    # today
    # tomorrow
    # weekday
    # yesterday

    # //******************************************************************************
    # //
    # //  function operators
    # //
    # //******************************************************************************

    # eval

    testRPN( 'rpn 10 x 5 * eval' )
    testRPN( 'rpn -a20 57 x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )

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
    # //  geometry operators
    # //
    # //******************************************************************************

    # n_sphere_area

    testRPN( 'rpn 34 inches 3 n_sphere_area' )
    testRPN( 'rpn 34 square_inches 3 n_sphere_area' )
    testRPN( 'rpn 34 cubic_inches 3 n_sphere_area' )

    # n_sphere_radius

    testRPN( 'rpn 3 meters 4 n_sphere_radius' )
    testRPN( 'rpn 3 square_meters 4 n_sphere_radius' )
    testRPN( 'rpn 3 cubic_meters 4 n_sphere_radius' )

    # n_sphere_volume

    testRPN( 'rpn 3 square_feet 6 nsphere_volume' )

    # polygon_area

    testRPN( 'rpn 13 polygon_area' )

    # sphere_area

    testRPN( 'rpn 8 inches sphere_area' )
    testRPN( 'rpn 8 sq_inches sphere_area' )
    #testRPN( 'rpn 8 cu_inches sphere_area' )    # not implemented yet

    # sphere_radius

    testRPN( 'rpn 4 inches sphere_radius' )
    testRPN( 'rpn 4 square_inches sphere_radius' )
    testRPN( 'rpn 4 cubic_inches sphere_radius' )

    # sphere_volume

    testRPN( 'rpn 5 inches sphere_volume' )
    #testRPN( 'rpn 5 sq_inches sphere_volume' )  # not implemented yet
    testRPN( 'rpn 5 cubic_in sphere_volume' )

    # triangle_area

    testRPN( 'rpn 123 456 789 triangle_area' )


    # //******************************************************************************
    # //
    # //  internal operators
    # //
    # //******************************************************************************

    # _dump_aliases

    testRPN( 'rpn _dump_aliases' )

    # _dump_operators

    testRPN( 'rpn _dump_operators' )

    # _stats

    testRPN( 'rpn _stats' )


    # //******************************************************************************
    # //
    # //  lexicographic operators
    # //
    # //******************************************************************************

    # add_digits

    testRPN( 'rpn 3 4 add_digits' )
    testRPN( 'rpn 3 45 add_digits' )
    testRPN( 'rpn 34 567 add_digits' )

    # combine_digits
    # dup_digits

    testRPN( 'rpn 543 2 dup_digits' )

    # find_palindrome

    testRPN( 'rpn -a30 10911 55 find_palindrome' )
    testRPN( 'rpn 180 200 range 10 find_palindrome -s1' )

    # get_digits
    # is_palindrome

    testRPN( 'rpn 101 is_palindrome' )
    testRPN( 'rpn 1 22 range is_palindrome' )
    testRPN( 'rpn 1234567890 is_palindrome' )

    # is_pandigital
    # multiply_digits
    # reversal_addition

    testRPN( 'rpn -a20 89 24 reversal_addition' )
    testRPN( 'rpn -a20 80 89 range 24 reversal_addition' )
    testRPN( 'rpn -a20 89 16 24 range reversal_addition' )
    testRPN( 'rpn -a90 14,104,229,999,995 185 reversal_addition' )
    testRPN( 'rpn -a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    # reverse_digits

    testRPN( 'rpn 37 1 8 range * reverse_digits' )
    testRPN( 'rpn 37 1 2 9 range range * reverse_digits' )

    # sum_digits


    # //******************************************************************************
    # //
    # //  list operators
    # //
    # //******************************************************************************

    # alternate_signs

    testRPN( 'rpn 1 10 range alternate_signs' )

    # alternate_signs_2

    testRPN( 'rpn 1 10 range alternate_signs_2' )

    # alternating_sum

    testRPN( 'rpn 1 10 range alternating_sum' )

    # alternating_sum_2

    testRPN( 'rpn 1 10 range alternating_sum_2' )

    # append

    testRPN( 'rpn 1 10 range 45 50 range append' )
    testRPN( 'rpn 1 10 range 11 20 range append 21 30 range append' )

    # count

    testRPN( 'rpn 1 10 range count' )

    # diffs

    testRPN( 'rpn 1 10 range diffs' )
    testRPN( 'rpn 1 10 range fib diffs' )

    # diffs2

    testRPN( 'rpn 1 10 range diffs2' )
    testRPN( 'rpn 1 10 range fib diffs2' )

    # element

    testRPN( 'rpn 1 10 range 5 element' )
    testRPN( 'rpn -a25 1 100 range fibonacci 55 element' )

    # exponential_range

    testRPN( 'rpn 1.1 1.1 10 exponential_range' )

    # flatten
    # geometric_mean

    testRPN( 'rpn 1 100 range geometric_mean' )
    testRPN( 'rpn [ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    # geometric_range

    testRPN( 'rpn 2 8 8 geometric_range' )

    # group_elements
    # interleave

    testRPN( 'rpn 1 10 range 1 10 range interleave' )

    # intersection

    testRPN( 'rpn 1 10 range 1 8 range intersection' )

    # left

    testRPN( 'rpn 1 10 range 5 left' )

    # max_index

    testRPN( 'rpn 1 10 range max_index' )

    # min_index

    testRPN( 'rpn 1 10 range min_index' )

    # nonzero

    testRPN( 'rpn 1 10 range nonzero' )

    # occurrences
    # range

    testRPN( 'rpn 1 23 range' )

    # range2

    testRPN( 'rpn 1 23 2 range2' )

    # ratios
    # reduce
    # reverse

    testRPN( 'rpn 1 10 range reverse' )
    testRPN( 'rpn 1 2 10 range range reverse' )
    testRPN( 'rpn 1 2 10 range reverse range reverse' )
    testRPN( 'rpn 1 2 10 range reverse range' )

    # right

    testRPN( 'rpn 1 10 range 5 right' )

    # shuffle
    # slice

    testRPN( 'rpn 1 10 range 3 5 slice' )
    testRPN( 'rpn 1 10 range 2 -5 slice' )

    # sort

    testRPN( 'rpn 10 1 -1 range2 sort' )

    # sort_descending

    testRPN( 'rpn 1 10 range sort_descending' )

    # sublist

    testRPN( 'rpn 1 10 range 1 5 sublist' )

    # union

    testRPN( 'rpn 1 10 range 11 20 range union' )

    # unique

    testRPN( 'rpn 1 10 range unique' )
    testRPN( 'rpn 1 10 range 1 10 range append unique' )
    testRPN( 'rpn [ 1 10 range 10 dup ] unique' )

    # zero

    testRPN( 'rpn -10 10 range zero' )
    testRPN( 'rpn 1 10 range zero' )


    # //******************************************************************************
    # //
    # //  logarithm operators
    # //
    # //******************************************************************************

    # lambertw

    testRPN( 'rpn 5 lambertw' )

    # li

    testRPN( 'rpn 12 li' )

    # ln

    testRPN( 'rpn 1000 ln' )

    # log10

    testRPN( 'rpn 1000 log10' )

    # log2

    testRPN( 'rpn 1000 log2' )

    # logxy

    testRPN( 'rpn 6561 3 logxy' )

    # polylog

    testRPN( 'rpn 9 3 polylog' )


    # //******************************************************************************
    # //
    # //  modifier operators
    # //
    # //******************************************************************************

    # [
    # ]
    # {
    # }
    # dup_term
    # dup_operator

    testRPN( 'rpn 2 5 dup_operator sqr' )
    testRPN( 'rpn 4 6 5 dup_operator *' )

    # previous
    # unlist
    # use_members

    # //******************************************************************************
    # //
    # //  number theory operators
    # //
    # //******************************************************************************

    # aliquot

    testRPN( 'rpn 276 10 aliquot' )

    # alternating_factorial

    testRPN( 'rpn 13 alternating_factorial' )
    testRPN( 'rpn -a20 1 20 range alternating_factorial' )

    # base

    testRPN( 'rpn 1 10 range 2 base' )
    testRPN( 'rpn 1 10 range 3 base' )
    testRPN( 'rpn 1 10 range 4 base' )
    testRPN( 'rpn 1 10 range 5 base' )
    testRPN( 'rpn 1 10 range 6 base' )
    testRPN( 'rpn 1 10 range 7 base' )
    testRPN( 'rpn 1 10 range 8 base' )
    testRPN( 'rpn 1 10 range 9 base' )

    testRPN( 'rpn -a30 1 20 range 11 base' )
    testRPN( 'rpn -a30 1 20 range 12 base' )
    testRPN( 'rpn -a30 1 20 range 13 base' )
    testRPN( 'rpn -a30 1 20 range 14 base' )
    testRPN( 'rpn -a30 1 20 range 15 base' )
    testRPN( 'rpn -a30 1 20 range 16 base' )
    testRPN( 'rpn -a30 1 20 range 17 base' )
    testRPN( 'rpn -a30 1 20 range 18 base' )
    testRPN( 'rpn -a30 1 20 range 19 base' )
    testRPN( 'rpn -a30 1 20 range 20 base' )

    # carol

    testRPN( 'rpn -a500 773 carol' )

    # cf

    testRPN( 'rpn 1 10 range cf' )

    # count_divisors

    testRPN( 'rpn 1024 count_divisors' )

    # crt

    testRPN( 'rpn 1 3 range 10 20 range 3 primes crt' )

    # divisors

    testRPN( 'rpn 2 3 ** 3 4 ** * divisors' )
    testRPN( 'rpn 12 ! divisors' )

    # double_factorial

    testRPN( 'rpn 9 double_factorial' )

    # ecm

    testRPN( 'rpn -a40 10 30 ** random_integer ecm' )

    # egypt

    testRPN( 'rpn 45 67 egypt' )

    # euler_brick
    # euler_phi
    # factor

    testRPN( 'rpn 883847311 factor' )
    testRPN( 'rpn 1 40 range fibonacci factor -s1' )

    # factorial

    testRPN( 'rpn -a25 23 factorial' )

    # fibonacci

    testRPN( 'rpn 1 50 range fibonacci' )
    testRPN( 'rpn -c -a 8300 39399 fibonacci' )

    # fibonorial

    testRPN( 'rpn 5 fibonorial' )
    testRPN( 'rpn -a50 24 fibonorial' )

    # fraction

    testRPN( 'rpn 12 23 fraction' )

    # frobenius

    testRPN( 'rpn 10 20 range 3 primes frobenius' )

    # gamma

    testRPN( 'rpn 3 gamma' )

    # harmonic

    testRPN( 'rpn 34 harmonic' )

    # heptanacci

    testRPN( 'rpn 224623 heptanacci' )

    # hexanacci

    testRPN( 'rpn 949 hexanacci' )

    # hyperfactorial

    testRPN( 'rpn -a160 17 hyperfactorial' )

    # is_abundant
    # is_achilles
    # is_deficient
    # is_k_semiprime
    # is_perfect
    # is_prime

    testRPN( 'rpn 1000 1030 range is_prime' )
    testRPN( 'rpn 2049 is_prime' )
    testRPN( 'rpn 92348759911 is_prime' )

    # is_pronic
    # is_powerful
    # is_rough
    # is_semiprime
    # is_smooth
    # is_sphenic
    # is_squarefree
    # is_unusual
    # jacobsthal

    testRPN( 'rpn 10 jacobsthal' )

    # kynea

    testRPN( 'rpn 8 kynea' )

    # leonardo
    # leyland

    testRPN( 'rpn 7 8 leyland' )

    # lgamma

    testRPN( 'rpn 10 lgamma' )

    # linear_recurrence

    testRPN( 'rpn 1 10 range 2 5 range 17 linear_recur' )

    # lucas

    testRPN( 'rpn -a21 99 lucas' )

    # make_cf

    testRPN( 'rpn e 20 make_cf' )

    # mertens

    testRPN( 'rpn 20 mertens' )
    testRPN( 'rpn 1 10 range mertens' )

    # mobius
    # padovan

    testRPN( 'rpn 76 padovan' )

    # pascal_triangle

    testRPN( 'rpn 12 pascal_triangle' )

    # pentanacci

    testRPN( 'rpn 16 pentanacci' )

    # polygamma

    testRPN( 'rpn 4 5 polygamma' )

    # repunit

    testRPN( 'rpn -a20 23 5 repunit' )

    # riesel

    testRPN( 'rpn 23 riesel' )

    # sigma

    testRPN( 'rpn 1 20 range sigma' )

    # subfactorial

    testRPN( 'rpn -a20 19 subfactorial' )

    # superfactorial

    testRPN( 'rpn -a50 12 superfactorial' )

    # tetranacci

    testRPN( 'rpn -a30 87 tetranacci' )

    # thabit

    testRPN( 'rpn -a20 45 thabit' )

    # tribonacci

    testRPN( 'rpn 1 20 range tribonacci' )
    testRPN( 'rpn -c -a 2800 10239 tribonacci' )

    # unit_roots

    testRPN( 'rpn 7 unit_roots' )

    # zeta

    testRPN( 'rpn 4 zeta' )


    # //******************************************************************************
    # //
    # //  polygonal number operators
    # //
    # //******************************************************************************

    # centered_decagonal

    testRPN( 'rpn 17 centered_decagonal' )

    # centered_decagonal?

    testRPN( 'rpn 1000 centered_decagonal?' )

    # centered_heptagonal

    testRPN( 'rpn 102 centered_heptagonal' )

    # centered_heptagonal?

    testRPN( 'rpn 100000 centered_heptagonal?' )

    # centered_hexagonal

    testRPN( 'rpn 103 centered_hexagonal' )

    # centered_hexagonal?

    # centered_nonagonal

    testRPN( 'rpn 104 centered_nonagonal' )

    # centered_nonagonal?

    testRPN( 'rpn 5,000,000 centered_nonagonal?' )

    # centered_octagonal

    testRPN( 'rpn 10 centered_octagonal' )

    # centered_octagonal?

    testRPN( 'rpn 361 centered_octagonal?' )

    # centered_pentagonal

    testRPN( 'rpn 108 centered_pentagonal' )

    # centered_pentagonal?

    testRPN( 'rpn 9999 centered_pentagonal?' )

    # centered_polygonal

    testRPN( 'rpn 108 5 centered_polygonal' )

    # centered_polygonal?

    testRPN( 'rpn 9999 5 centered_polygonal?' )

    # centered_square

    testRPN( 'rpn 5 centered_square' )

    # centered_square?

    testRPN( 'rpn 49 centered_square?' )

    # centered_triangular

    testRPN( 'rpn 100 centered_triangular' )

    # centered_triangular?

    testRPN( 'rpn 10000 centered_triangular?' )

    # decagonal

    testRPN( 'rpn 151 decagonal' )

    # decagonal?

    testRPN( 'rpn 123454321 decagonal?' )

    # heptagonal

    testRPN( 'rpn 203 heptagonal' )

    # heptagonal?

    testRPN( 'rpn 99999 heptagonal?' )

    # heptagonal_hexagonal

    testRPN( 'rpn 2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal

    testRPN( 'rpn 8684 heptagonal_pentagonal' )

    # heptagonal_square

    testRPN( 'rpn 222 heptagonal_square' )

    # heptagonal_triangular

    testRPN( 'rpn 399 heptagonal_triangular' )

    # hexagonal

    testRPN( 'rpn 340 hexagonal' )

    # hexagonal?

    testRPN( 'rpn 230860 hexagonal?' )

    # hexagonal_pentagonal

    testRPN( 'rpn 107 hexagonal_pentagonal' )

    # hexagonal_square
    # nonagonal

    testRPN( 'rpn 554 nonagonal' )

    # nonagonal?

    testRPN( 'rpn 9 6 ** nonagonal?' )

    # nonagonal_heptagonal

    testRPN( 'rpn -a50 12 nonagonal_heptagonal' )

    # nonagonal_hexagonal

    testRPN( 'rpn -a60 13 nonagonal_hexagonal' )

    # nonagonal_octagonal

    testRPN( 'rpn -a 75 14 nonagonal_octagonal' )

    # nonagonal_pentagonal

    testRPN( 'rpn -a60 15 nonagonal_pentagonal' )

    # nonagonal_square

    testRPN( 'rpn -a22 16 nonagonal_square' )

    # nonagonal_triangular

    testRPN( 'rpn -a21 17 nonagonal_triangular' )

    # octagonal

    testRPN( 'rpn 102 octagonal' )

    # octagonal?

    testRPN( 'rpn 8 4 ** 1 + octagonal?' )

    # octagonal_heptagonal

    testRPN( 'rpn -a40 8 octagonal_heptagonal' )

    # octagonal_hexagonal

    testRPN( 'rpn -a30 7 octagonal_hexagonal' )

    # octagonal_pentagonal

    testRPN( 'rpn -a15 6 octagonal_pentagonal' )

    # octagonal_square

    testRPN( 'rpn -a25 11 octagonal_square' )

    # octagonal_triangular

    testRPN( 'rpn -a20 10 octagonal_triangular' )

    # pentagonal

    testRPN( 'rpn 16 pentagonal' )

    # pentagonal?

    testRPN( 'rpn 5 5 ** 5 + pentagonal?' )

    # pentagonal_square
    # pentagonal_triangular
    # polygonal

    testRPN( 'rpn 9 12 polygonal' )

    # polygonal?

    testRPN( 'rpn 12 12 ** 12 polygonal?' )

    # square_triangular

    testRPN( 'rpn -a60 34 square_triangular' )

    # triangular

    testRPN( 'rpn 203 triangular' )

    # triangular?

    testRPN( 'rpn 20706 triangular?' )


    # //******************************************************************************
    # //
    # //  polyhedral number operators
    # //
    # //******************************************************************************

    # centered_cube

    testRPN( 'rpn 100 centered_cube' )

    # dodecahedral

    testRPN( 'rpn 44 dodecahedral' )

    # icosahedral

    testRPN( 'rpn 100 icosahedral' )

    # polytope

    testRPN( 'rpn 1 10 range 7 polytope' )
    testRPN( 'rpn 10 2 8 range polytope' )
    testRPN( 'rpn 1 10 range 2 8 range polytope' )
    testRPN( 'rpn -a20 -c 18 47 polytope' )

    # pyramid

    testRPN( 'rpn 304 pyramid' )

    # rhombdodec

    testRPN( 'rpn 89 rhombdodec' )

    # stella_octangula

    testRPN( 'rpn 3945 stella_octangula' )

    # tetrahedral

    testRPN( 'rpn -a20 19978 tetrahedral' )

    # truncated_octahedral

    testRPN( 'rpn 394 truncated_octahedral' )

    # truncated_tetrahedral

    testRPN( 'rpn 683 truncated_tetrahedral' )

    # octahedral

    testRPN( 'rpn 23 octahedral' )

    # pentatope

    testRPN( 'rpn 12 pentatope' )


    # //******************************************************************************
    # //
    # //  powers and roots operators
    # //
    # //******************************************************************************

    # cube

    testRPN( 'rpn 3 cube' )

    # cube_root

    testRPN( 'rpn pi cube_root' )

    # exp

    testRPN( 'rpn 13 exp' )

    # exp10

    testRPN( 'rpn 12 exp10' )

    # expphi

    testRPN( 'rpn 100 expphi' )

    # hyper4_2

    testRPN( 'rpn -a160 4 3 hyper4_2' )

    # power

    testRPN( 'rpn 4 5 power' )
    testRPN( 'rpn 4 1 i power' )
    testRPN( 'rpn 1 10 range 2 10 range power' )

    # powmod
    # root

    testRPN( 'rpn 8 3 root' )

    # root2

    testRPN( 'rpn 2 square_root' )

    # square

    testRPN( 'rpn 45 square' )

    # tetrate

    testRPN( 'rpn 3 2 tetrate' )

    # tower

    testRPN( 'rpn -c -a30 [ 2 3 2 ] tower' )

    # tower2

    testRPN( 'rpn [ 4 4 4 ] tower2' )


    # //******************************************************************************
    # //
    # //  prime number operators
    # //
    # //******************************************************************************

    # balanced_prime

    testRPN( 'rpn 1 10 range balanced' )
    testRPN( 'rpn 53 balanced' )
    testRPN( 'rpn 153 balanced' )
    testRPN( 'rpn 2153 balanced' )

    # balanced_prime_

    testRPN( 'rpn 1 10 range balanced_' )
    testRPN( 'rpn 53 balanced_' )
    testRPN( 'rpn 153 balanced_' )
    testRPN( 'rpn 2153 balanced_' )

    # cousin_prime

    testRPN( 'rpn 1 10 range cousin_prime' )
    testRPN( 'rpn 77 cousin_prime' )
    testRPN( 'rpn 5176 cousin_prime' )

    # cousin_prime_
    # double_balanced

    testRPN( 'rpn 1 5 range double_balanced' )
    testRPN( 'rpn 54 double_balanced' )
    testRPN( 'rpn 82154 double_balanced' )

    # double_balanced_

    testRPN( 'rpn 1 5 range double_balanced_' )
    testRPN( 'rpn 54 double_balanced_' )
    testRPN( 'rpn 100000 double_balanced_' )

    # isolated_prime

    testRPN( 'rpn 102 isolated_prime' )
    testRPN( 'rpn 1902 isolated_prime' )

    # next_prime

    testRPN( 'rpn 1 100 range next_prime' )
    testRPN( 'rpn 35 next_prime' )
    testRPN( 'rpn 8783 next_prime' )
    testRPN( 'rpn 142857 next_prime' )
    testRPN( 'rpn -c 6 13 ** 1 + next_prime' )
    testRPN( 'rpn -c 7 13 ** 1 + next_prime' )

    # nth_prime?

    testRPN( 'rpn 1 10 range nth_prime?' )
    testRPN( 'rpn 67 nth_prime?' )
    testRPN( 'rpn 16467 nth_prime?' )
    testRPN( 'rpn -c 13,000,000,000 nth_prime?' )
    testRPN( 'rpn -c 256,000,000,000 nth_prime?' )

    # nth_quad?

    testRPN( 'rpn 1 100000 10000 range2 nth_quad?' )
    testRPN( 'rpn 453456 nth_quad?' )
    testRPN( 'rpn 74,000,000,000 nth_quad?' )

    # polyprime

    testRPN( 'rpn 1 5 range 1 5 range polyprime' )
    testRPN( 'rpn 4 3 polyprime' )
    testRPN( 'rpn 5 8 polyprime' )

    # prime

    testRPN( 'rpn 1 101 range prime' )
    testRPN( 'rpn 8783 prime' )
    testRPN( 'rpn 142857 prime' )
    testRPN( 'rpn 367981443 prime' )
    testRPN( 'rpn 9113486725 prime' )

    # primepi

    testRPN( 'rpn 87 primepi' )

    # primes

    testRPN( 'rpn 1 5 range 5 primes' )
    testRPN( 'rpn 1 1 5 range primes' )
    testRPN( 'rpn 2 1 5 range primes' )
    testRPN( 'rpn 3 1 5 range primes' )
    testRPN( 'rpn 4 1 5 range primes' )
    testRPN( 'rpn 150 10 primes' )
    testRPN( 'rpn 98765 20 primes' )
    testRPN( 'rpn 176176176 25 primes' )
    testRPN( 'rpn 11,000,000,000 25 primes' )

    # primorial
    # quadruplet_prime?

    testRPN( 'rpn 8 quadruplet_prime?' )
    testRPN( 'rpn 8871 quadruplet_prime?' )

    # quadruplet_prime

    testRPN( 'rpn 17 quadruplet_prime' )
    testRPN( 'rpn 99831 quadruplet_prime' )

    # quadruplet_prime_

    testRPN( 'rpn 17 quadruplet_prime_' )
    testRPN( 'rpn 55731 quadruplet_prime_' )

    # quintuplet_prime?

    # quintuplet_prime

    testRPN( 'rpn 18 quintuplet_prime' )
    testRPN( 'rpn 9387 quintuplet_prime' )

    # quintuplet_prime_

    testRPN( 'rpn 62 quintuplet_prime_' )
    testRPN( 'rpn 74238 quintuplet_prime_' )

    # safe_prime

    testRPN( 'rpn 45 safe_prime' )
    testRPN( 'rpn 5199846 safe_prime' )

    # safe_prime?
    # sextuplet_prime

    testRPN( 'rpn 29 sextuplet_prime' )
    testRPN( 'rpn 1176 sextuplet_prime' )
    testRPN( 'rpn 556 sextuplet_prime' )

    # sextuplet_prime_

    testRPN( 'rpn 1 sextuplet_prime_' )
    testRPN( 'rpn 587 sextuplet_prime_' )
    testRPN( 'rpn 835 sextuplet_prime_' )
    testRPN( 'rpn 29 sextuplet_prime_' )

    # sexy_prime

    testRPN( 'rpn -c 89,999,999 sexy_prime' )
    testRPN( 'rpn 1 sexy_prime' )
    testRPN( 'rpn 1487 sexy_prime' )
    testRPN( 'rpn 2 sexy_prime' )
    testRPN( 'rpn 23235 sexy_prime' )
    testRPN( 'rpn 29 sexy_prime' )

    # sexy_prime_

    testRPN( 'rpn 1 10 range sexy_prime_' )
    testRPN( 'rpn 29 sexy_prime_' )
    testRPN( 'rpn 21985 sexy_prime_' )
    testRPN( 'rpn -c 100,000,000 sexy_prime_' )

    # sexy_triplet

    testRPN( 'rpn 1 10 range sexy_triplet' )
    testRPN( 'rpn 29 sexy_triplet' )
    testRPN( 'rpn -c 593847 sexy_triplet' )
    testRPN( 'rpn -c 8574239 sexy_triplet' )

    # sexy_triplet_

    testRPN( 'rpn 1 10 range sexy_triplet_' )
    testRPN( 'rpn 52 sexy_triplet_' )
    testRPN( 'rpn 5298 sexy_triplet_' )
    testRPN( 'rpn -c 10984635 sexy_triplet_' )

    # sexy_quadruplet

    testRPN( 'rpn 1 10 range sexy_quadruplet' )
    testRPN( 'rpn 29 sexy_quadruplet' )
    testRPN( 'rpn -c 289747 sexy_quadruplet' )

    # sexy_quadruplet_

    testRPN( 'rpn 1 10 range sexy_quadruplet_' )
    testRPN( 'rpn 29 sexy_quadruplet_' )
    testRPN( 'rpn 2459 sexy_quadruplet_' )

    # sophie_prime

    testRPN( 'rpn 1 10 range sophie_prime' )
    testRPN( 'rpn 87 sophie_prime' )
    testRPN( 'rpn 6,500,000 sophie_prime' )

    # superprime

    testRPN( 'rpn 89 superprime' )

    # triple_balanced

    testRPN( 'rpn 1 10 range triple_balanced' )
    testRPN( 'rpn 5588 triple_balanced' )

    # triple_balanced_

    testRPN( 'rpn 1 10 range triple_balanced_' )
    testRPN( 'rpn 6329 triple_balanced_' )

    # triplet_prime

    testRPN( 'rpn 1 10 range triplet_prime' )
    testRPN( 'rpn 192834 triplet_prime' )

    # triplet_prime_

    testRPN( 'rpn 1 10 range triplet_prime_' )
    testRPN( 'rpn 192834 triplet_prime_' )

    # twin_prime

    testRPN( 'rpn 1 10 range twin_prime_' )
    testRPN( 'rpn 57454632 twin_prime_' )

    # twin_prime_

    testRPN( 'rpn 1 20 range twin_prime' )
    testRPN( 'rpn 39485 twin_prime' )


    # //******************************************************************************
    # //
    # //  settings operators (for use in interactive mode)
    # //
    # //******************************************************************************

    # accuracy
    # comma
    # comma_mode
    # decimal_grouping
    # # hex_mode
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

    # //******************************************************************************
    # //
    # //  special operators
    # //
    # //******************************************************************************

    # estimate

    testRPN( 'rpn 150 amps estimate' )
    testRPN( 'rpn 150 barns estimate' )
    testRPN( 'rpn 150 bytes second / estimate' )
    testRPN( 'rpn 150 candelas estimate' )
    testRPN( 'rpn 150 cd meter meter * / estimate' )
    testRPN( 'rpn 150 coulombs estimate' )
    testRPN( 'rpn 150 cubic_feet estimate' )
    testRPN( 'rpn 150 cubic_inches estimate' )
    testRPN( 'rpn 150 cubic_miles estimate' )
    testRPN( 'rpn 150 cubic_mm estimate' )
    testRPN( 'rpn 150 cubic_nm estimate' )
    testRPN( 'rpn 150 cubic_parsecs estimate' )
    testRPN( 'rpn 150 days estimate' )
    testRPN( 'rpn 150 degC estimate' )
    testRPN( 'rpn 150 degrees estimate' )
    testRPN( 'rpn 150 farads estimate' )
    testRPN( 'rpn 150 feet estimate' )
    testRPN( 'rpn 150 G estimate' )
    testRPN( 'rpn 150 gallons estimate' )
    testRPN( 'rpn 150 grams estimate' )
    testRPN( 'rpn 150 GW estimate' )
    testRPN( 'rpn 150 Hz estimate' )
    testRPN( 'rpn 150 joules estimate' )
    testRPN( 'rpn 150 K estimate' )
    testRPN( 'rpn 150 kg liter / estimate' )
    testRPN( 'rpn 150 light-years estimate' )
    testRPN( 'rpn 150 liters estimate' )
    testRPN( 'rpn 150 lumens estimate' )
    testRPN( 'rpn 150 lux estimate' )
    testRPN( 'rpn 150 mach estimate' )
    testRPN( 'rpn 150 MB estimate' )
    testRPN( 'rpn 150 megapascals estimate' )
    testRPN( 'rpn 150 meter second second * / estimate' )
    testRPN( 'rpn 150 mhos estimate' )
    testRPN( 'rpn 150 microfarads estimate' )
    testRPN( 'rpn 150 miles estimate' )
    testRPN( 'rpn 150 minutes estimate' )
    testRPN( 'rpn 150 months estimate' )
    testRPN( 'rpn 150 mph estimate' )
    testRPN( 'rpn 150 mps estimate' )
    testRPN( 'rpn 150 newtons estimate' )
    testRPN( 'rpn 150 ohms estimate' )
    testRPN( 'rpn 150 pascal-seconds estimate' )
    testRPN( 'rpn 150 pascals estimate' )
    testRPN( 'rpn 150 Pg estimate' )
    testRPN( 'rpn 150 picofarads estimate' )
    testRPN( 'rpn 150 pounds estimate' )
    testRPN( 'rpn 150 radians estimate' )
    testRPN( 'rpn 150 seconds estimate' )
    testRPN( 'rpn 150 sieverts estimate' )
    testRPN( 'rpn 150 square_degrees estimate' )
    testRPN( 'rpn 150 square_feet estimate' )
    testRPN( 'rpn 150 square_inches estimate' )
    testRPN( 'rpn 150 square_light-years estimate' )
    testRPN( 'rpn 150 square_miles estimate' )
    testRPN( 'rpn 150 square_mm estimate' )
    testRPN( 'rpn 150 square_nm estimate' )
    testRPN( 'rpn 150 stilbs estimate' )
    testRPN( 'rpn 150 teaspoons estimate' )
    testRPN( 'rpn 150 tesla estimate' )
    testRPN( 'rpn 150 tons estimate' )
    testRPN( 'rpn 150 tTNT estimate' )
    testRPN( 'rpn 150 volts estimate' )
    testRPN( 'rpn 150 watts estimate' )
    testRPN( 'rpn 150 weeks estimate' )
    testRPN( 'rpn 150 years estimate' )
    testRPN( 'rpn c 150 / estimate' )

    # help

    testRPN( 'rpn help' )
    testRPN( 'rpn help about' )
    testRPN( 'rpn help arithmetic' )
    testRPN( 'rpn help add' )

    # name

    testRPN( 'rpn -c -a100 45 primorial name' )

    # oeis

    testRPN( 'rpn 1000 oeis' )
    testRPN( 'rpn 250000 randint oeis' )

    # oeis_comment

    testRPN( 'rpn 1000 oeis_comment' )
    testRPN( 'rpn 250000 randint oeis_comment' )

    # oeis_ex

    testRPN( 'rpn 1000 oeis_ex' )
    testRPN( 'rpn 250000 randint oeis_ex' )

    # oeis_name

    testRPN( 'rpn 1000 oeis_name' )
    testRPN( 'rpn 250000 randint oeis_name' )

    # ordinal_name

    testRPN( 'rpn -1 ordinal_name' )
    testRPN( 'rpn 0 ordinal_name' )
    testRPN( 'rpn 1 ordinal_name' )
    testRPN( 'rpn 2 26 ** ordinal_name' )

    # random

    testRPN( 'rpn random' )

    # random_

    testRPN( 'rpn 50 random_' )

    # random_integer

    testRPN( 'rpn 100 random_integer' )
    testRPN( 'rpn 10 12 ^ random_integer' )

    # random_integer_

    testRPN( 'rpn 23 265 random_integer_' )

    # result

    testRPN( 'rpn result' )

    # set
    # topic
    # value

    # //******************************************************************************
    # //
    # //  trigonometry operators
    # //
    # //******************************************************************************

    # acos

    testRPN( 'rpn 0.8 acos' )

    # acosh

    testRPN( 'rpn 0.6 acosh' )

    # acot

    testRPN( 'rpn 0.4 acot' )

    # acoth

    testRPN( 'rpn 0.3 acoth' )

    # acsc

    testRPN( 'rpn 0.2 acsc' )

    # acsch

    testRPN( 'rpn 0.67 acsch' )

    # asec

    testRPN( 'rpn 0.4 asec' )

    # asech

    testRPN( 'rpn 0.1 asech' )

    # asin

    testRPN( 'rpn 0.8 asin' )

    # asinh

    testRPN( 'rpn 0.3 asinh' )

    # atan

    testRPN( 'rpn 0.2 atan' )

    # atanh

    testRPN( 'rpn 0.45 atanh' )

    # cos

    testRPN( 'rpn 45 degrees cos' )
    testRPN( 'rpn pi radians cos' )

    # cosh

    testRPN( 'rpn pi 3 / cosh' )

    # cot

    testRPN( 'rpn pi 7 / cot' )

    # coth

    testRPN( 'rpn pi 9 / coth' )

    # csc

    testRPN( 'rpn pi 12 / csc' )

    # csch

    testRPN( 'rpn pi 13 / csch' )

    # hypotenuse

    testRPN( 'rpn 3 4 hypotenuse' )

    # sec

    testRPN( 'rpn pi 7 / sec' )

    # sech

    testRPN( 'rpn pi 7 / sech' )

    # sin

    testRPN( 'rpn pi 2 / sin' )

    # sinh

    testRPN( 'rpn pi 2 / sinh' )

    # tan

    testRPN( 'rpn pi 3 / tan' )

    # tanh

    testRPN( 'rpn pi 4 / tanh' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runTests( )
    runConvertTests( )
    runHelpTests( )

