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

from rpn import rpn

from testConvert import *
from testHelp import *


# //******************************************************************************
# //
# //  testRPN
# //
# //******************************************************************************

def testRPN( command ):
    print( command )
    rpn( command.split( ' ' )[ 1 : ] )
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
    testRPN( 'rpn -a20 7 sqrt' )

    testRPN( 'rpn 100101011010011 -b 2' )
    testRPN( 'rpn 120012022211222012 -b 3' )
    testRPN( 'rpn rick -b 36' )

    testRPN( 'rpn 6 8 ** -c' )

    testRPN( 'rpn -a3 7 sqrt -d' )
    testRPN( 'rpn -a12 8 sqrt -d5' )
    testRPN( 'rpn -a50 19 sqrt -d10' )

    testRPN( 'rpn -a50 1 30 range fib -g 3' )
    testRPN( 'rpn -a50 1 30 range fib -g 4' )

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

    testRPN( 'rpn -a1000 -d5 7 sqrt -r62' )
    testRPN( 'rpn -a1000 -d5 pi -r8' )
    testRPN( 'rpn 2 1 32 range ** -r16' )

    testRPN( 'rpn -t 12 14 ** 1 + factor' )
    testRPN( 'rpn 1 40 range fib factor -s1' )

    testRPN( 'rpn 3 1 20 range ** -x' )

    testRPN( 'rpn 65537 4 ** -r 16 -g8 -z' )

    # operators
    testRPN( 'rpn -394 abs' )

    testRPN( 'rpn 0.8 acos' )

    testRPN( 'rpn 0.6 acosh' )

    testRPN( 'rpn 0.4 acot' )

    testRPN( 'rpn 0.3 acoth' )

    testRPN( 'rpn 0.2 acsc' )

    testRPN( 'rpn 0.67 acsch' )

    testRPN( 'rpn 4 3 add' )
    testRPN( 'rpn 4 cups 13 teaspoons +' )
    testRPN( 'rpn 55 mph 10 miles hour / +' )
    testRPN( 'rpn 55 mph 10 meters second / +' )
    testRPN( 'rpn 55 mph 10 furlongs fortnight / +' )
    testRPN( 'rpn today 3 days add' )
    testRPN( 'rpn today 3 weeks add' )
    testRPN( 'rpn now 150 miles 10 furlongs fortnight / / add' )

    testRPN( 'rpn 3 4 add_digits' )
    testRPN( 'rpn 3 45 add_digits' )
    testRPN( 'rpn 34 567 add_digits' )

    testRPN( 'rpn 13 alternating_factorial' )
    testRPN( 'rpn -a20 1 20 range alternating_factorial' )

    testRPN( 'rpn 0x7777 0xdcba and' )

    testRPN( 'rpn apery' )

    testRPN( 'rpn 0.4 asec' )

    testRPN( 'rpn 0.1 asech' )

    testRPN( 'rpn 0.8 asin' )

    testRPN( 'rpn 0.3 asinh' )

    testRPN( 'rpn 0.2 atan' )

    testRPN( 'rpn 0.45 atanh' )

    testRPN( 'rpn -a25 avogadro' )

    testRPN( 'rpn 1 10 range balanced' )
    testRPN( 'rpn 53 balanced' )
    testRPN( 'rpn 153 balanced' )
    testRPN( 'rpn 2153 balanced' )

    testRPN( 'rpn 1 10 range balanced_' )
    testRPN( 'rpn 53 balanced_' )
    testRPN( 'rpn 153 balanced_' )
    testRPN( 'rpn 2153 balanced_' )

    testRPN( 'rpn -a43 45 bell' )

    testRPN( 'rpn 4 5 bell_polynomial' )

    testRPN( 'rpn 16 bernoulli' )

    testRPN( 'rpn 12 9 binomial' )
    testRPN( 'rpn -a20 -c 120 108 binomial' )

    testRPN( 'rpn -a500 773 carol' )

    testRPN( 'rpn -a50 85 nth_catalan' )

    testRPN( 'rpn 1965-03 calendar' )
    testRPN( 'rpn 2014-10 calendar' )

    testRPN( 'rpn catalan' )

    testRPN( 'rpn 17 centered_decagonal' )

    testRPN( 'rpn 1000 centered_decagonal?' )

    testRPN( 'rpn 9.99999 ceiling' )

    testRPN( 'rpn 100 centered_cube' )

    testRPN( 'rpn -a100 champernowne' )

    testRPN( 'rpn 0x101 char' )

    testRPN( 'rpn 102 centered_heptagonal' )

    testRPN( 'rpn 100000 centered_heptagonal?' )

    testRPN( 'rpn 103 centered_hexagonal' )

    testRPN( 'rpn 104 centered_nonagonal' )

    testRPN( 'rpn 5,000,000 centered_nonagonal?' )

    testRPN( 'rpn 10 centered_octagonal' )

    testRPN( 'rpn 361 centered_octagonal?' )

    testRPN( 'rpn -a 1000 copeland' )

    testRPN( 'rpn 45 degrees cos' )
    testRPN( 'rpn pi radians cos' )

    testRPN( 'rpn pi 3 / cosh' )

    testRPN( 'rpn pi 7 / cot' )

    testRPN( 'rpn pi 9 / coth' )

    testRPN( 'rpn 0xffff count_bits' )

    testRPN( 'rpn 1024 count_divisors' )

    testRPN( 'rpn 1 10 range cousin_prime' )
    testRPN( 'rpn 77 cousin_prime' )
    testRPN( 'rpn 5176 cousin_prime' )

    testRPN( 'rpn 108 centered_pentagonal' )

    testRPN( 'rpn 9999 centered_pentagonal?' )

    testRPN( 'rpn 108 5 centered_polygonal' )

    testRPN( 'rpn 9999 5 centered_polygonal?' )

    testRPN( 'rpn pi 12 / csc' )

    testRPN( 'rpn pi 13 / csch' )

    testRPN( 'rpn 5 centered_square' )

    testRPN( 'rpn 49 centered_square?' )

    testRPN( 'rpn 100 centered_triangular' )

    testRPN( 'rpn 10000 centered_triangular?' )

    testRPN( 'rpn 3 cube' )

    testRPN( 'rpn 151 decagonal' )

    testRPN( 'rpn 123454321 decagonal?' )

    testRPN( 'rpn -a80 100 delannoy' )

    testRPN( 'rpn 8 million seconds dhms' )

    testRPN( 'rpn 12 13 divide' )
    testRPN( 'rpn 10 days 7 / dhms' )
    testRPN( 'rpn marathon 100 miles hour / / minutes convert' )
    testRPN( 'rpn 2 zeta sqrt 24 sqrt / 12 *' )
    testRPN( 'rpn now 2014-01-01 - minutes /' )

    testRPN( 'rpn 2 3 ** 3 4 ** * divisors' )
    testRPN( 'rpn 12 ! divisors' )

    testRPN( 'rpn 1 radian dms' )

    testRPN( 'rpn 44 dodecahedral' )

    testRPN( 'rpn -x 10 20 ** double' )

    testRPN( 'rpn 1 5 range double_balanced' )
    testRPN( 'rpn 54 double_balanced' )
    testRPN( 'rpn 82154 double_balanced' )

    testRPN( 'rpn 1 5 range double_balanced_' )
    testRPN( 'rpn 54 double_balanced_' )
    testRPN( 'rpn 100000 double_balanced_' )

    testRPN( 'rpn 9 double_factorial' )

    testRPN( 'rpn 2 5 dup_operator sqr' )
    testRPN( 'rpn 4 6 5 dup_operator *' )

    testRPN( 'rpn 543 2 dup_digits' )

    testRPN( 'rpn e' )

    testRPN( 'rpn -a40 10 30 ** random_int ecm' )

    testRPN( 'rpn 1 40 range fib factor -s1' )

    testRPN( 'rpn 45 67 egypt' )

    testRPN( 'rpn 1 10 range 5 element' )
    testRPN( 'rpn -a25 1 100 range fib 55 element' )

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

    testRPN( 'rpn euler' )

    testRPN( 'rpn 10 x 5 * eval' )
    testRPN( 'rpn -a20 57 x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )

    testRPN( 'rpn 13 exp' )

    testRPN( 'rpn 12 exp10' )

    testRPN( 'rpn 100 expphi' )

    testRPN( 'rpn 1.1 1.1 10 exponential_range' )

    testRPN( 'rpn 883847311 factor' )

    testRPN( 'rpn -a25 23 factorial' )

    testRPN( 'rpn -a30 10911 55 find_palindrome' )
    testRPN( 'rpn 180 200 range 10 find_palindrome -s1' )

    testRPN( 'rpn 1 50 range fibonacci' )
    testRPN( 'rpn -c -a 8300 39399 fibonacci' )

    testRPN( 'rpn -x 1029.3 float' )

    testRPN( 'rpn 3.4 floor' )

    testRPN( 'rpn 12 23 fraction' )

    testRPN( 'rpn 1234567890 from_unix_time' )

    testRPN( 'rpn 3 gamma' )

    testRPN( 'rpn 2 8 8 geometric_range' )

    testRPN( 'rpn glaisher' )

    testRPN( 'rpn 34 harmonic' )

    testRPN( 'rpn 203 heptagonal' )

    testRPN( 'rpn 99999 heptagonal?' )

    testRPN( 'rpn 224623 heptanacci' )

    testRPN( 'rpn 2039 heptagonal_hexagonal' )

    testRPN( 'rpn 8684 heptagonal_pentagonal' )

    testRPN( 'rpn 222 heptagonal_square' )

    testRPN( 'rpn 399 heptagonal_triangular' )

    testRPN( 'rpn 340 hexagonal' )

    testRPN( 'rpn 230860 hexagonal?' )

    testRPN( 'rpn 949 hexanacci' )

    testRPN( 'rpn 107 hexagonal_pentagonal' )

    testRPN( 'rpn 54658 seconds hms' )

    testRPN( 'rpn -a160 4 3 hyper4_2' )

    testRPN( 'rpn -a160 17 hyperfactorial' )

    testRPN( 'rpn 3 4 hypotenuse' )

    testRPN( 'rpn 3 i' )

    testRPN( 'rpn 100 icosahedral' )

    testRPN( 'rpn 456 8 integer' )

    testRPN( 'rpn 30 miles gallon / invert_units' )

    testRPN( 'rpn 1000 10000 is_divisible' )
    testRPN( 'rpn 12 1 12 range is_divisible' )
    testRPN( 'rpn 1 20 range 6 is_divisible' )

    testRPN( 'rpn 102 isolated_prime' )
    testRPN( 'rpn 1902 isolated_prime' )

    testRPN( 'rpn 101 is_palindrome' )
    testRPN( 'rpn 1 22 range is_palindrome' )

    testRPN( 'rpn 1234567890 is_palindrome' )

    testRPN( 'rpn 1000 1030 range is_prime' )
    testRPN( 'rpn 2049 is_prime' )
    testRPN( 'rpn 92348759911 is_prime' )

    testRPN( 'rpn 1024 issquare' )

    testRPN( 'rpn itoi' )

    testRPN( 'rpn 10 jacobsthal' )

    testRPN( 'rpn khinchin' )

    testRPN( 'rpn 8 kynea' )

    testRPN( 'rpn 5 6 lah' )

    testRPN( 'rpn 5 lambertw' )

    testRPN( 'rpn 7 8 leyland' )

    testRPN( 'rpn 10 lgamma' )

    testRPN( 'rpn 12 li' )

    testRPN( 'rpn inf x fib x 1 - fib / limit' )
    testRPN( 'rpn inf x 1/x 1 + x ** limit' )

    testRPN( 'rpn 1000 ln' )
    testRPN( 'rpn 1000 log10' )

    testRPN( 'rpn 1000 log2' )

    testRPN( 'rpn 6561 3 logxy' )

    testRPN( 'rpn 3456789012 long' )

    testRPN( 'rpn 1234567890123456789012 longlong' )

    testRPN( 'rpn -a21 99 lucas' )

    testRPN( 'rpn e 20 make_cf' )

    testRPN( 'rpn max_char' )
    testRPN( 'rpn max_long' )

    testRPN( 'rpn -a20 max_longlong' )

    testRPN( 'rpn -a40 max_quadlong' )

    testRPN( 'rpn max_short' )

    testRPN( 'rpn max_uchar' )

    testRPN( 'rpn max_ulong' )

    testRPN( 'rpn -a20 max_ulonglong' )

    testRPN( 'rpn -a40 max_uquadlong' )

    testRPN( 'rpn max_ushort' )

    testRPN( 'rpn 20 mertens' )
    testRPN( 'rpn 1 10 range mertens' )

    testRPN( 'rpn min_char' )

    testRPN( 'rpn min_long' )

    testRPN( 'rpn -a20 min_longlong' )

    testRPN( 'rpn -a40 min_quadlong' )

    testRPN( 'rpn min_short' )

    testRPN( 'rpn min_uchar' )

    testRPN( 'rpn min_ulong' )

    testRPN( 'rpn min_ulonglong' )

    testRPN( 'rpn min_uquadlong' )

    testRPN( 'rpn min_ushort' )

    testRPN( 'rpn 11001 100 modulo' )

    testRPN( 'rpn -a25 56 motzkin' )

    testRPN( 'rpn 5 7 multiply' )
    testRPN( 'rpn 15 mph 10 hours *' )
    testRPN( 'rpn c m/s convert 1 nanosecond * inches convert' )
    testRPN( 'rpn barn gigaparsec * cubic_inch convert' )

    testRPN( 'rpn -c -a100 45 primorial name' )

    testRPN( 'rpn 6 8 narayana' )

    testRPN( 'rpn 4 negative' )

    testRPN( 'rpn 554 nonagonal' )

    testRPN( 'rpn 9 6 ** nonagonal?' )

    testRPN( 'rpn -a50 12 nonagonal_heptagonal' )

    testRPN( 'rpn -a60 13 nonagonal_hexagonal' )

    testRPN( 'rpn -a 75 14 nonagonal_octagonal' )

    testRPN( 'rpn -a60 15 nonagonal_pentagonal' )

    testRPN( 'rpn -a22 16 nonagonal_square' )

    testRPN( 'rpn -a21 17 nonagonal_triangular' )

    testRPN( 'rpn -x 0xefefefefefefef not' )

    testRPN( 'rpn now' )

    testRPN( 'rpn 34 inches 3 nsphere_area' )
    testRPN( 'rpn 34 square_inches 3 nsphere_area' )
    testRPN( 'rpn 34 cubic_inches 3 nsphere_area' )

    testRPN( 'rpn 3 meters 4 nsphere_radius' )
    testRPN( 'rpn 3 square_meters 4 nsphere_radius' )
    testRPN( 'rpn 3 cubic_meters 4 nsphere_radius' )

    testRPN( 'rpn 3 square_feet 6 nsphere_volume' )

    testRPN( 'rpn -a20 12 nth_apery' )

    testRPN( 'rpn 1 10 range nth_prime?' )
    testRPN( 'rpn 67 nth_prime?' )
    testRPN( 'rpn 16467 nth_prime?' )
    testRPN( 'rpn -c 13,000,000,000 nth_prime?' )
    testRPN( 'rpn -c 256,000,000,000 nth_prime?' )

    testRPN( 'rpn 1 100000 10000 range2 nth_quad?' )
    testRPN( 'rpn 453456 nth_quad?' )
    testRPN( 'rpn 74,000,000,000 nth_quad?' )

    testRPN( 'rpn 102 octagonal' )

    testRPN( 'rpn 8 4 ** 1 + octagonal?' )

    testRPN( 'rpn 23 octahedral' )

    testRPN( 'rpn -a40 8 octagonal_heptagonal' )

    testRPN( 'rpn -a30 7 octagonal_hexagonal' )

    testRPN( 'rpn -a15 6 octagonal_pentagonal' )

    testRPN( 'rpn -a25 11 octagonal_square' )

    testRPN( 'rpn -a20 10 octagonal_triangular' )

    testRPN( 'rpn 1000 oeis' )
    testRPN( 'rpn 250000 randint oeis' )

    testRPN( 'rpn 1000 oeis_comment' )
    testRPN( 'rpn 250000 randint oeis_comment' )

    testRPN( 'rpn 1000 oeis_ex' )
    testRPN( 'rpn 250000 randint oeis_ex' )

    testRPN( 'rpn 1000 oeis_name' )
    testRPN( 'rpn 250000 randint oeis_name' )

    testRPN( 'rpn omega' )

    testRPN( 'rpn -x 0x5543 0x7789 or' )

    testRPN( 'rpn 76 padovan' )

    testRPN( 'rpn 0xff889d8f parity' )

    testRPN( 'rpn 12 pascal' )

    testRPN( 'rpn 13 pell' )

    testRPN( 'rpn 16 pentagonal' )

    testRPN( 'rpn 5 5 ** 5 + pentagonal?' )

    testRPN( 'rpn 16 pentanacci' )

    testRPN( 'rpn 12 pentatope' )

    testRPN( 'rpn 8 3 perm' )

    testRPN( 'rpn phi' )

    testRPN( 'rpn pi' )

    testRPN( 'rpn plastic' )

    testRPN( 'rpn 13 polygon_area' )

    testRPN( 'rpn 4 5 polygamma' )

    testRPN( 'rpn 9 12 polygonal' )

    testRPN( 'rpn 12 12 ** 12 polygonal?' )

    testRPN( 'rpn 9 3 polylog' )

    testRPN( 'rpn 1 5 range 1 5 range polyprime' )
    testRPN( 'rpn 4 3 polyprime' )
    testRPN( 'rpn 5 8 polyprime' )

    testRPN( 'rpn 1 10 range 7 polytope' )
    testRPN( 'rpn 10 2 8 range polytope' )
    testRPN( 'rpn 1 10 range 2 8 range polytope' )
    testRPN( 'rpn -a20 -c 18 47 polytope' )

    testRPN( 'rpn 4 5 power' )
    testRPN( 'rpn 4 1 i power' )
    testRPN( 'rpn 1 10 range 2 10 range power' )

    testRPN( 'rpn 1 101 range prime' )
    testRPN( 'rpn 8783 prime' )
    testRPN( 'rpn 142857 prime' )
    testRPN( 'rpn 367981443 prime' )
    testRPN( 'rpn 9113486725 prime' )

    testRPN( 'rpn 1 100 range prime?' )
    testRPN( 'rpn 35 prime?' )
    testRPN( 'rpn 8783 prime?' )
    testRPN( 'rpn 142857 prime?' )
    testRPN( 'rpn -c 6 13 ** 1 + prime?' )
    testRPN( 'rpn -c 7 13 ** 1 + prime?' )

    testRPN( 'rpn 87 primepi' )

    testRPN( 'rpn 1 5 range 5 primes' )
    testRPN( 'rpn 1 1 5 range primes' )
    testRPN( 'rpn 2 1 5 range primes' )
    testRPN( 'rpn 3 1 5 range primes' )
    testRPN( 'rpn 4 1 5 range primes' )
    testRPN( 'rpn 150 10 primes' )
    testRPN( 'rpn 98765 20 primes' )
    testRPN( 'rpn 176176176 25 primes' )
    testRPN( 'rpn 11,000,000,000 25 primes' )

    testRPN( 'rpn 304 pyramid' )

    testRPN( 'rpn 17 quadruplet_prime' )
    testRPN( 'rpn 99831 quadruplet_prime' )

    testRPN( 'rpn 8 quadruplet_prime?' )
    testRPN( 'rpn 8871 quadruplet_prime?' )

    testRPN( 'rpn 17 quadruplet_prime_' )
    testRPN( 'rpn 55731 quadruplet_prime_' )

    testRPN( 'rpn 18 quintuplet_prime' )
    testRPN( 'rpn 9387 quintuplet_prime' )

    testRPN( 'rpn 62 quintuplet_prime_' )
    testRPN( 'rpn 74238 quintuplet_prime_' )

    testRPN( 'rpn random' )

    testRPN( 'rpn 50 random_' )

    testRPN( 'rpn 100 random_int' )
    testRPN( 'rpn 10 12 ^ random_int' )

    testRPN( 'rpn 23 265 random_int_' )

    testRPN( 'rpn 1 23 range' )

    testRPN( 'rpn 1 23 2 range2' )

    testRPN( 'rpn 6 7 / reciprocal' )

    testRPN( 'rpn -a20 23 5 repunit' )

    testRPN( 'rpn -a20 89 24 rev_add' )
    testRPN( 'rpn -a20 80 89 range 24 rev_add' )
    testRPN( 'rpn -a20 89 16 24 range rev_add' )

    testRPN( 'rpn 1 10 range reverse' )
    testRPN( 'rpn 1 2 10 range range reverse' )
    testRPN( 'rpn 1 2 10 range reverse range reverse' )
    testRPN( 'rpn 1 2 10 range reverse range' )

    testRPN( 'rpn -a90 14,104,229,999,995 185 reversal_addition' )
    testRPN( 'rpn -a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    testRPN( 'rpn 37 1 8 range * reverse_digits' )
    testRPN( 'rpn 37 1 2 9 range range * reverse_digits' )

    testRPN( 'rpn 89 rhombdodec' )

    testRPN( 'rpn 23 riesel' )

    testRPN( 'rpn 8 3 root' )

    testRPN( 'rpn 2 root2' )

    testRPN( 'rpn pi root3' )

    testRPN( 'rpn 4.5 round' )

    testRPN( 'rpn 45 safe_prime' )
    testRPN( 'rpn 5199846 safe_prime' )

    testRPN( 'rpn -a50 67 schroeder' )

    testRPN( 'rpn pi 7 / sec' )

    testRPN( 'rpn pi 7 / sech' )

    testRPN( 'rpn 29 sextuplet_prime' )
    testRPN( 'rpn 1176 sextuplet_prime' )

    testRPN( 'rpn 29 sextuplet_prime_' )
    testRPN( 'rpn 556 sextuplet_prime' )

    testRPN( 'rpn 1 sextuplet_prime_' )
    testRPN( 'rpn 587 sextuplet_prime_' )
    testRPN( 'rpn 835 sextuplet_prime_' )

    testRPN( 'rpn 29 sexy_prime' )
    testRPN( 'rpn 23235 sexy_prime' )

    testRPN( 'rpn 1 sexy_prime' )
    testRPN( 'rpn 2 sexy_prime' )
    testRPN( 'rpn 1487 sexy_prime' )
    testRPN( 'rpn -c 89,999,999 sexy_prime' )

    testRPN( 'rpn 1 10 range sexy_prime_' )
    testRPN( 'rpn 29 sexy_prime_' )
    testRPN( 'rpn 21985 sexy_prime_' )
    testRPN( 'rpn -c 100,000,000 sexy_prime_' )

    testRPN( 'rpn 1 10 range sexy_quadruplet' )
    testRPN( 'rpn 29 sexy_quadruplet' )
    testRPN( 'rpn -c 289747 sexy_quadruplet' )

    testRPN( 'rpn 1 10 range sexy_quadruplet_' )
    testRPN( 'rpn 29 sexy_quadruplet_' )
    testRPN( 'rpn 2459 sexy_quadruplet_' )

    testRPN( 'rpn 1 10 range sexy_triplet' )
    testRPN( 'rpn 29 sexy_triplet' )
    testRPN( 'rpn -c 593847 sexy_triplet' )
    testRPN( 'rpn -c 8574239 sexy_triplet' )

    testRPN( 'rpn 1 10 range sexy_triplet_' )
    testRPN( 'rpn 52 sexy_triplet_' )
    testRPN( 'rpn 5298 sexy_triplet_' )
    testRPN( 'rpn -c 10984635 sexy_triplet_' )

    testRPN( 'rpn -x 0x10 3 shift_left' )

    testRPN( 'rpn -x 0x1000 4 shift_right' )

    testRPN( 'rpn 32800 short' )

    testRPN( 'rpn pi 2 / sin' )

    testRPN( 'rpn pi 2 / sinh' )

    testRPN( 'rpn 8 9 10 solve2' )

    testRPN( 'rpn 10 -10 10 -10 solve3' )

    testRPN( 'rpn 2 -3 2 -3 2 solve4' )

    testRPN( 'rpn 1 10 range sophie_prime' )
    testRPN( 'rpn 87 sophie_prime' )
    testRPN( 'rpn 6,500,000 sophie_prime' )

    testRPN( 'rpn 8 inches sphere_area' )
    testRPN( 'rpn 8 sq_inches sphere_area' )
    #testRPN( 'rpn 8 cu_inches sphere_area' )    # not implemented yet

    testRPN( 'rpn 4 inches sphere_radius' )
    testRPN( 'rpn 4 square_inches sphere_radius' )
    testRPN( 'rpn 4 cubic_inches sphere_radius' )

    testRPN( 'rpn 5 inches sphere_volume' )
    #testRPN( 'rpn 5 sq_inches sphere_volume' )  # not implemented yet
    testRPN( 'rpn 5 cubic_in sphere_volume' )

    testRPN( 'rpn 45 square' )

    testRPN( 'rpn -a60 34 squaretri' )

    testRPN( 'rpn 3945 stella_octangula' )

    testRPN( 'rpn -a20 19 subfactorial' )

    testRPN( 'rpn 3948 474 subtract' )
    testRPN( 'rpn 4 cups 27 teaspoons -' )
    testRPN( 'rpn 57 hectares 23 acres -' )
    testRPN( 'rpn 10 Mb second / 700 MB hour / -' )
    testRPN( 'rpn today 3 days -' )
    testRPN( 'rpn today 3 weeks -' )
    testRPN( 'rpn today 3 months -' )
    testRPN( 'rpn now earth_radius 2 pi * * miles convert 4 mph / -' )

    testRPN( 'rpn -a50 12 superfactorial' )

    testRPN( 'rpn 89 superprime' )

    testRPN( 'rpn 45 sylvester' )

    testRPN( 'rpn pi 3 / tan' )

    testRPN( 'rpn pi 4 / tanh' )

    testRPN( 'rpn -a20 19978 tetrahedral' )

    testRPN( 'rpn -a30 87 tetranacci' )

    testRPN( 'rpn 3 2 tetrate' )

    testRPN( 'rpn -a20 45 thabit' )

    testRPN( 'rpn 123 456 789 triangle_area' )

    testRPN( 'rpn 203 triangular' )

    testRPN( 'rpn 20706 triangular?' )

    testRPN( 'rpn 1 20 range tribonacci' )
    testRPN( 'rpn -c -a 2800 10239 tribonacci' )

    testRPN( 'rpn 1 10 range triple_balanced' )
    testRPN( 'rpn 5588 triple_balanced' )

    testRPN( 'rpn 1 10 range triple_balanced_' )
    testRPN( 'rpn 6329 triple_balanced_' )

    testRPN( 'rpn 1 10 range triplet_prime' )
    testRPN( 'rpn 192834 triplet_prime' )

    testRPN( 'rpn 1 10 range triplet_prime_' )
    testRPN( 'rpn 192834 triplet_prime_' )

    testRPN( 'rpn 394 truncated_octahedral' )

    testRPN( 'rpn 683 truncated_tetrahedral' )

    testRPN( 'rpn 1 20 range twin_prime' )
    testRPN( 'rpn 39485 twin_prime' )

    testRPN( 'rpn 1 10 range twin_prime_' )
    testRPN( 'rpn 57454632 twin_prime_' )

    # twin_prime?

    testRPN( 'rpn 290 uchar' )

    testRPN( 'rpn 200 8 uinteger' )

    testRPN( 'rpn 234567890 ulong' )

    testRPN( 'rpn -a20 12345678901234567890 ulonglong' )

    testRPN( 'rpn 7 unit_roots' )

    testRPN( 'rpn 23456 ushort' )

    testRPN( 'rpn 0x1939 0x3948 xor' )

    testRPN( 'rpn 14578 seconds ydhms' )

    testRPN( 'rpn 4 zeta' )

    testRPN( 'rpn 142857 ~' )

    testRPN( 'rpn 1 10 range alternate_signs' )

    testRPN( 'rpn 1 10 range alternate_signs_2' )

    testRPN( 'rpn 1 10 range alternating_sum' )

    testRPN( 'rpn 1 10 range alternating_sum_2' )

    testRPN( 'rpn 1 10 range 45 50 range append' )
    testRPN( 'rpn 1 10 range 11 20 range append 21 30 range append' )

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

    testRPN( 'rpn 1 10 range cf' )

    testRPN( 'rpn 1 10 range count' )

    testRPN( 'rpn 1 10 range diffs' )
    testRPN( 'rpn 1 10 range fib diffs' )

    testRPN( 'rpn 1 10 range diffs2' )
    testRPN( 'rpn 1 10 range fib diffs2' )

    testRPN( 'rpn -x pi double' )
    testRPN( 'rpn 0x400921fb54442d18 undouble' )
    testRPN( 'rpn 0xcdcdcdcdcdcdcdcd undouble' )

    testRPN( 'rpn pi float' )
    testRPN( 'rpn 0x40490fdb unfloat' )
    testRPN( 'rpn 0xcdcdcdcd unfloat' )

    testRPN( 'rpn 1 100 range gcd' )

    testRPN( 'rpn 1 10 range 1 10 range interleave' )

    testRPN( 'rpn 1 10 range 1 8 range intersection' )

    testRPN( 'rpn 1 10 range 2 5 range 17 linear_recur' )

    testRPN( 'rpn 1 10 range max' )

    testRPN( 'rpn max_double' )

    testRPN( 'rpn max_float' )

    testRPN( 'rpn 1 10 range max_index' )

    testRPN( 'rpn 1 10 range mean' )

    testRPN( 'rpn 1 10 range min' )

    testRPN( 'rpn min_double' )

    testRPN( 'rpn min_float' )

    testRPN( 'rpn 1 10 range min_index' )

    testRPN( 'rpn 1 10 range nonzero' )

    testRPN( 'rpn -x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    testRPN( 'rpn 1 10 range 1 10 range polyadd' )

    testRPN( 'rpn 1 10 range 1 10 range polymul' )

    testRPN( 'rpn [ [ 1 10 range ] [ 1 10 range ] [ 2 11 range ] ] polyprod' )

    testRPN( 'rpn [ [ 1 10 range ] [ 2 11 range ] ] polysum' )

    testRPN( 'rpn 1 10 range 6 eval_poly' )
    testRPN( 'rpn [ 4 -2 3 5 -6 20 ] 1 10 range eval_poly' )

    testRPN( 'rpn 1 10 range product' )

    testRPN( 'rpn result' )

    testRPN( 'rpn 1 8 range solve' )

    testRPN( 'rpn 10 1 -1 range2 sort' )

    testRPN( 'rpn 1 10 range sort_descending' )

    testRPN( 'rpn 1 10 range stddev' )

    testRPN( 'rpn 1 10 range sum' )

    testRPN( 'rpn [ 2014 4 30 0 0 0 ] make_time to_unix_time' )

    testRPN( 'rpn -c -a30 [ 2 3 2 ] tower' )

    testRPN( 'rpn [ 4 4 4 ] tower2' )

    testRPN( 'rpn 1 10 range 11 20 range union' )

    testRPN( 'rpn 1 10 range unique' )
    testRPN( 'rpn 1 10 range 1 10 range append unique' )
    testRPN( 'rpn [ 1 10 range 10 dup ] unique' )

    testRPN( 'rpn 503942034 [ 3 4 5 11 4 4 ] unpack' )

    testRPN( 'rpn 1965 year_calendar' )
    testRPN( 'rpn today year_calendar' )

    testRPN( 'rpn -10 10 range zero' )
    testRPN( 'rpn 1 10 range zero' )

    testRPN( 'rpn today 7 days +' )
    testRPN( 'rpn today 2 months -' )
    testRPN( 'rpn today 3 weeks +' )
    testRPN( 'rpn today 50 years +' )

    testRPN( 'rpn today 1965-03-31 -' )
    testRPN( 'rpn 2015-01-01 1965-03-31 -' )
    testRPN( 'rpn 2015 dst_start' )
    testRPN( 'rpn 2015 dst_end' )
    testRPN( 'rpn 2015 easter' )
    testRPN( 'rpn 2015 election_day' )
    testRPN( 'rpn today iso_day' )
    testRPN( 'rpn [ 2015 7 5 4 3 ] make_julian_time' )
    testRPN( 'rpn today julian_day' )
    testRPN( 'rpn 2015 labor_day' )
    testRPN( 'rpn 2015 memorial_day' )
    testRPN( 'rpn 2015 presidents_day' )
    testRPN( 'rpn 2015 thanksgiving' )
    testRPN( 'rpn 2015 march 4 thursday nth_weekday' )
    testRPN( 'rpn 2015 march -1 thursday nth_weekday' )
    testRPN( 'rpn 2015 20 thursday nth_weekday_of_year' )
    testRPN( 'rpn 2015 -1 thursday nth_weekday_of_year' )

    testRPN( 'rpn 4 3 debruijn' )

    testRPN( 'rpn 4 3 is_less' )
    testRPN( 'rpn 4 3 is_greater' )
    testRPN( 'rpn 4 3 is_equal' )
    testRPN( 'rpn 4 3 is_not_equal' )
    testRPN( 'rpn 4 3 is_not_less' )
    testRPN( 'rpn 4 3 is_not_greater' )

    testRPN( 'rpn 5 fibonorial' )
    testRPN( 'rpn -a50 24 fibonorial' )

    testRPN( 'rpn 3 3 i + arg' )
    testRPN( 'rpn 3 3 i + conj' )

    testRPN( 'rpn 1 100 range geometric_mean' )
    testRPN( 'rpn [ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    testRPN( 'rpn 10 20 range 3 primes frobenius' )

    testRPN( 'rpn 1 10 range 3 5 slice' )
    testRPN( 'rpn 1 10 range 2 -5 slice' )

    testRPN( 'rpn 1 10 range 1 5 sublist' )

    testRPN( 'rpn 1 10 range 5 left' )
    testRPN( 'rpn 1 10 range 5 right' )

    testRPN( 'rpn 1 3 range 10 20 range 3 primes crt' )

    testRPN( 'rpn 1 20 range sigma' )

    testRPN( 'rpn 276 10 aliquot' )

    testRPN( 'rpn [ 1 2 3 4 ] 5 polypower' )

    testRPN( 'rpn help' )
    testRPN( 'rpn help about' )
    testRPN( 'rpn help arithmetic' )
    testRPN( 'rpn help add' )

    testRPN( 'rpn _dump_aliases' )
    testRPN( 'rpn _dump_operators' )
    testRPN( 'rpn _stats' )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    runTests( )
    runConvertTests( )
    runHelpTests( )

