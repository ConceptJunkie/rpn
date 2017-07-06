#!/usr/bin/env python

# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2017, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import sys

from collections import OrderedDict

from rpnOperators import *

from rpnAliases import operatorAliases
from rpnOperators import constants
from rpnMeasurement import RPNMeasurement
from rpnPersistence import loadUnitNameData
from rpnTestUtils import *
from rpnUtils import getDataPath
from rpnVersion import PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE
from testConvert import *
from testHelp import *

from mpmath import *

slow = False


# //******************************************************************************
# //
# //  runCommandLineOptionsTests
# //
# //******************************************************************************

def runCommandLineOptionsTests( ):
    testOperator( '-a20 7 square_root' )

    testOperator( '100101011010011 -b2' )
    testOperator( '120012022211222012 -b3' )
    testOperator( 'rick -b36' )
    expectException( '9999 -b8' )

    testOperator( '6 8 ** -c' )

    testOperator( '-a3 7 square_root -d' )
    testOperator( '-a12 8 square_root -d5' )
    testOperator( '-a50 19 square_root -d10' )

    testOperator( '-a50 1 30 range fibonacci -g3' )
    testOperator( '-a50 1 30 range fibonacci -g4' )

    testOperator( '-h' )

    testOperator( '2 sqrt pi * -i' )

    testOperator( '-m50 planck_length' )

    testOperator( '1 10 range 3 ** -o' )

    testOperator( 'pi -p1000' )

    testOperator( '10 100 10 range2 -re' )
    testOperator( '10 100 10 range2 -rfac' )
    testOperator( '10 100 10 range2 -rfac2' )
    testOperator( '10 100 10 range2 -rfib' )
    testOperator( '10 100 10 range2 -rlucas' )
    testOperator( '10 100 10 range2 -rphi' )
    testOperator( '10 100 10 range2 -rpi' )
    testOperator( '10 100 10 range2 -rprimorial' )
    testOperator( '10 100 10 range2 -rsqr' )
    testOperator( '10 100 10 range2 -rsqrt2' )
    testOperator( '10 100 10 range2 -rtri' )

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
    expectException( '1 100 range -r1' )
    expectException( '1 100 range -r63' )

    testOperator( '1 100 range -re' )
    testOperator( '1 100 range -rfac' )
    testOperator( '1 100 range -rfac2' )
    testOperator( '1 100 range -rfib' )
    testOperator( '1 100 range -rlucas' )
    testOperator( '1 100 range -rphi' )
    testOperator( '1 100 range -rpi' )
    testOperator( '1 100 range -rprimorial' )
    testOperator( '1 100 range -rsqr' )
    testOperator( '1 100 range -rsqrt2' )
    testOperator( '1 100 range -rtri' )

    # testRPN compares values not output format
    #expectEqual( '1 10000 range -rtri', '462 oeis 10000 left' )
    #expectEqual( '1 40320 range -rtri', '7623 oeis 40320 left' )

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
    # add_polynomials
    expectEqual( '1 10 range 1 10 range add_polynomials', '2 20 2 range2' )
    expectException( '1 10 range add_polynomials' )

    # eval_polynomial
    testOperator( '1 10 range 6 eval_polynomial' )
    testOperator( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_polynomial' )
    expectException( '1 eval_polynomial' )
    expectException( '1 10 range eval_polynomial' )

    # find_polynomial
    expectEqual( 'phi 3 find_polynomial', '[ -1 1 1 ]' )
    expectException( '1 find_polynomial' )

    # multiply_polynomials
    testOperator( '1 10 range 1 10 range multiply_polynomials' )
    expectException( '1 10 range multiply_polynomials' )

    # polynomial_power
    testOperator( '[ 1 2 3 4 ] 5 polynomial_power' )
    expectException( '1 10 range polynomial_power' )

    # polynomial_product
    testOperator( '[ 1 10 range 1 10 range 2 11 range ] polynomial_product' )

    # polynomial_sum
    testOperator( '[ 1 10 range 2 11 range ] polynomial_sum' )

    # solve
    testOperator( '1 8 range solve' )
    expectException( '0 solve' )
    expectException( '1 solve' )
    expectException( '[ 0 1 ] solve' )
    expectException( '[ 0 0 1 ] solve' )
    expectException( '[ 0 0 0 ] solve' )

    # solve_cubic
    expectEquivalent( '1 0 0 0 solve_cubic', '[ 1 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 0 solve_cubic', '[ 0 1 0 0 ] solve' )
    expectEquivalent( '1 1 0 0 solve_cubic', '[ 1 1 0 0 ] solve' )
    expectEquivalent( '0 0 1 0 solve_cubic', '[ 0 0 1 0 ] solve' )
    expectEquivalent( '1 0 -3 0 solve_cubic', '[ 1 0 -3 0 ] solve' )
    expectEquivalent( '10 -10 10 -10 solve_cubic', '[ 10 -10 10 -10 ] solve' )
    expectEquivalent( '57 -43 15 28 solve_cubic', '[ 57 -43 15 28 ] solve' )
    expectException( '0 0 0 0 solve_cubic' )
    expectException( '0 0 0 1 solve_cubic' )

    # solve_quadratic
    expectEquivalent( '1 0 0 solve_quadratic', '[ 1 0 0 ] solve' )
    expectEquivalent( '1 1 0 solve_quadratic', '[ 1 1 0 ] solve' )
    expectEquivalent( '1 0 1 solve_quadratic', '[ 1 0 1 ] solve' )
    expectEquivalent( '0 1 0 solve_quadratic', '[ 0 1 0 ] solve' )
    expectEquivalent( '1 -1 1 solve_quadratic', '[ 1 -1 1 ] solve' )
    expectEquivalent( '8 9 10 solve_quadratic', '[ 8 9 10 ] solve' )
    expectEquivalent( '-36 150 93 solve_quadratic', '[ -36 150 93 ] solve' )
    expectException( '0 0 0 solve_quadratic' )
    expectException( '0 0 1 solve_quadratic' )

    # solve_quartic
    expectEquivalent( '1 0 0 0 0 solve_quartic', '[ 1 0 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 0 0 solve_quartic', '[ 0 1 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 1 0 solve_quartic', '[ 0 1 0 1 0 ] solve' )
    expectEquivalent( '0 0 1 0 0 solve_quartic', '[ 0 0 1 0 0 ] solve' )
    expectEquivalent( '0 0 0 1 0 solve_quartic', '[ 0 0 0 1 0 ] solve' )
    expectEquivalent( '1 0 -5 0 7 solve_quartic', '[ 1 0 -5 0 7 ] solve' )
    expectEquivalent( '2 -3 2 -3 2 solve_quartic', '[ 2 -3 2 -3 2 ] solve' )
    expectEquivalent( '54 23 -87 19 2042 solve_quartic', '[ 54 23 -87 19 2042 ] solve' )
    expectException( '0 0 0 0 0 solve_quadratic' )
    expectException( '0 0 0 0 1 solve_quadratic' )


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
    expectResult( '3 feet 7 inches + inches convert', RPNMeasurement( 43, 'inch' ) )
    testOperator( 'today 7 days +' )
    testOperator( 'today 3 weeks +' )
    testOperator( 'today 50 years +' )
    testOperator( '4 cups 13 teaspoons +' )
    expectResult( '55 mph 10 miles hour / +', RPNMeasurement( 65, 'mile/hour' ) )
    testOperator( '55 mph 10 meters second / +' )
    testOperator( '55 mph 10 furlongs fortnight / +' )
    testOperator( 'today 3 days add' )
    testOperator( 'today 3 weeks add' )
    testOperator( 'now 150 miles 10 furlongs fortnight / / add' )
    expectException( '2 cups 3 weeks +' )

    # ceiling
    expectResult( '9.99999 ceiling', 10 )
    expectResult( '-0.00001 ceiling', 0 )
    expectResult( '9.5 cups ceiling', RPNMeasurement( 10, 'cups' ) )
    expectEqual( '1 56 range lambda x x log * ceiling eval', '50502 oeis 56 left' )

    # decrement
    expectResult( '2 decrement', 1 )
    expectResult( '3 miles decrement', RPNMeasurement( 2, 'miles' ) )

    # divide
    testOperator( '12 13 divide' )
    testOperator( '10 days 7 / dhms' )
    testOperator( 'marathon 100 miles hour / / minutes convert' )
    testOperator( '2 zeta sqrt 24 sqrt / 12 *' )
    testOperator( 'now 2014-01-01 - minutes /' )
    expectResult( '4 cups 2 cups /', 2 )
    expectException( '1 0 divide' )

    # equals_one_of
    expectEqual( '1 33100 primes lambda x 40 mod [ 7 19 23 ] equals_one_of x 1 - 2 / is_prime and filter', '353 oeis 1000 left' )

    # floor
    expectResult( '-0.4 floor', -1 )
    expectResult( '1 floor', 1 )
    expectResult( '3.4 floor', 3 )
    expectEqual( '10.3 cups floor', '10 cups' )
    expectEqual( '88 mph 10 round_by_value', '90 mph' )
    expectEqual( '4.5 i 8.6 + floor', '4 i 8 +' )
    expectResult( '3.14 miles floor', RPNMeasurement( 3, 'miles' ) )
    expectEqual( '1 52 range lambda 2 log 1 1 x x 2 + * / + log / floor eval', '84587 oeis 52 left' )
    expectEqual( '1 1000 range ! log 7 log / floor', '127033 oeis 1000 left' )
    expectEqual( '1 1000 range lambda x 5 * x 5 * log + ceiling eval', '212454 oeis 1000 left' )
    expectEqual( '1 1000 range e 1 - * floor', '210 oeis 1000 left' )

    # gcd
    expectResult( '1 100 range gcd', 1 )
    expectResult( '[ 124 324 ] gcd', 4 )
    expectResult( '[ 8 64 ] gcd', 8 )
    testOperator( '1 2 10 range range gcd' )

    # geometric_mean
    testOperator( '1 10 range geometric_mean' )
    testOperator( '1 1 10 range range geometric_mean' )

    # harmonic_mean
    # expectEqual( '1 937 range lambda divisors harmonic_mean is_integer filter', '1599 oeis 937 left' )

    # increment
    expectResult( '2 increment', 3 )
    expectEqual( '2 i increment', '2 i 1 +' )
    expectResult( '3 miles increment', RPNMeasurement( 4, 'miles' ) )

    # is_divisible
    expectResult( '1000 10000 is_divisible', 0 )
    expectResult( '10000 1000 is_divisible', 1 )
    expectResult( '12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )
    expectException( '1 0 is_divisible' )
    expectException( '20 i 4 is_divisible' )
    expectEqual( '0 2810 range lambda x 2 has_digits x 2 is_divisible or filter', '92451 oeis 2001 left' )
    expectEqual( '0 2944 range lambda x 9 has_digits x 9 is_divisible or filter', '92457 oeis 1001 left' )

    # is_equal
    expectResult( '4 3 is_equal', 0 )
    expectResult( 'pi pi is_equal', 1 )

    # is_even
    expectResult( '-2 is_even', 1 )
    expectResult( '-1 is_even', 0 )
    expectResult( '0 is_even', 1 )
    expectResult( '1 is_even', 0 )
    expectResult( '2 is_even', 1 )
    expectException( '1 i is_even' )

    # is_greater
    expectResult( '4 3 is_greater', 1 )
    expectResult( '55 55 is_greater', 0 )
    expectResult( 'e pi is_greater', 0 )
    expectResult( '3 inches 2 inches is_greater', 1 )
    expectResult( '8 miles 40000 feet is_greater', 1 )
    expectResult( '1 light-year 1 parsec is_greater', 0 )

    expectException( '3 i 6 is_greater' )
    expectException( '4 cups 1 mile is_greater' )

    # is_less
    expectResult( '4 3 is_less', 0 )
    expectResult( '2 2 is_less', 0 )
    expectResult( '2 3 is_less', 1 )
    expectException( '5 i 4 is_less' )
    expectResult( '3 inches 2 inches is_less', 0 )
    expectResult( '8 miles 40000 feet is_less', 0 )
    expectResult( '1 light-year 1 parsec is_less', 1 )

    expectException( '1 gallon 1 watt is_not_equal' )

    # is_not_equal
    expectResult( '4 3 is_not_equal', 1 )
    expectResult( '3 3 is_not_equal', 0 )
    expectResult( '4 cups 1 quart is_not_equal', 0 )
    expectResult( '3 inches 2 inches is_not_equal', 1 )
    expectResult( '8 miles 40000 feet is_not_equal', 1 )
    expectResult( '1 light-year 1 parsec is_not_equal', 1 )
    expectResult( '1 inch 1 inch is_not_equal', 0 )

    expectException( '4 cups 1 is_not_equal' )
    expectException( '1 inch 1 cup is_not_equal' )

    # is_not_greater
    expectResult( '4 3 is_not_greater', 0 )
    expectResult( '77 77 is_not_greater', 1 )
    expectResult( '2 99 is_not_greater', 1 )
    expectResult( '2 miles 2 kilometers is_not_greater', 0 )

    expectException( '2 i 7 is_not_greater' )

    # is_not_less
    expectResult( '4 3 is_not_less', 1 )
    expectResult( '663 663 is_not_less', 1 )
    expectResult( '-100 100 is_not_less', 0 )
    expectResult( '3 inches 2 inches is_not_less', 1 )
    expectResult( '8 miles 40000 feet is_not_less', 1 )
    expectResult( '1 light-year 1 parsec is_not_less', 0 )
    expectResult( '12 inches 1 foot is_not_less', 1 )

    expectException( '8 i -14 is_not_less' )

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
    expectException( '5 i 3 + is_odd' )

    # is_square
    expectResult( '1024 is_square', 1 )
    expectResult( '5 is_square', 0 )

    # is_squarefree
    expectEqual( '1 1000 range lambda x is_prime not x is_squarefree and filter', '469 oeis 440 left' )

    if slow:
        expectEqual( '1 20203 range lambda x is_prime not x is_squarefree and filter', '469 oeis 10000 left' )

    # is_zero
    expectResult( '-1 is_zero', 0 )
    expectResult( '0 is_zero', 1 )
    expectResult( '1 is_zero', 0 )

    # larger
    expectResult( '7 -7 larger', 7 )
    expectException( '5 i 3 + 6 larger' )

    # lcm
    expectEqual( '1 10 range lcm', '[ 2 2 2 3 3 5 7 ] prod' )
    testOperator( '1 1 10 range range lcm' )

    # mantissa
    # This works on the command line, but not here.  I have no idea why.
    #expectEqual( '-p180 1 15000 range lambda pi x sqrt * exp mantissa 0.0001 less_than filter', '127029 oeis 4 left' )

    # max
    expectResult( '1 10 range max', 10 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] max', 9 )
    expectEqual( '1 1 10 range range max', '1 10 range' )
    expectException( '[ 5 i 3 6 7 ] max' )

    # mean
    expectResult( '1 10 range mean', 5.5 )
    expectEqual( '1 10000 range mean', '5000.5' )
    testOperator( '1 1 10 range range mean' )

    # min
    expectResult( '1 10 range min', 1 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] min', 2 )
    expectEqual( '1 1 10 range range min', '[ 1 10 dup ]' )
    expectException( '[ 5 i 3 6 7 ] min' )

    # modulo
    expectResult( '11001 100 modulo', 1 )
    expectResult( '-120 7 modulo', 6 )
    expectResult( '8875 49 modulo', 6 )
    expectResult( '199467 8876 modulo', 4195 )
    expectException( '20 i 3 modulo' )

    # multiply
    expectResult( '5 7 multiply', 35 )
    testOperator( '15 mph 10 hours *' )
    testOperator( 'c m/s convert 1 nanosecond * inches convert' )

    # nearest_int
    expectResult( '0.1 nearest_int', 0 )
    expectResult( '4.5 nearest_int', 4 )
    expectResult( 'pi nearest_int', 3 )

    # negative
    expectResult( '-4 negative', 4 )
    expectResult( '0 negative', 0 )
    expectResult( '4 negative', -4 )
    expectEqual( '5 i 7 + negative', '-5 i 7 -' )

    # product
    expectEqual( '-a200 1 100 range product', '-a200 100 !' )
    expectResult( '[ 2 cups ] product', RPNMeasurement( 2, 'cup' ) )
    expectResult( '[ 3 2 cups ] product', RPNMeasurement( 6, 'cup' ) )
    expectResult( '[ 2 cups 8 16 ] product', RPNMeasurement( 256, 'cup' ) )
    expectResult( '[ 3 2 cups 8 16 ] product', RPNMeasurement( 768, 'cup' ) )
    testOperator( '1 1 10 range range prod' )

    # reciprocal
    expectEqual( '6 7 / reciprocal', '7 6 /' )

    # round
    expectResult( '0.1 round', 0 )
    expectResult( '4.5 round', 5 )
    expectEqual( '9.9 W round', '10 W' )
    expectException( '5.4 i round' )

    # round_by_digits
    expectResult( '0.1 0 round_by_digits', 0 )
    expectResult( '4.5 0 round_by_digits', 5 )
    expectResult( '4.5 1 round_by_digits', 0 )
    expectResult( '8 1 round_by_digits', 10 )
    expectResult( '4500 3 round_by_digits', 5000 )
    expectEqual( 'pi -2 round_by_digits', '3.14' )
    expectEqual( '88 mph 1 round_by_digits', '90 mph' )
    expectEqual( 'avogadro 20 round_by_digits', '6.022e23' )
    expectException( '6.7 i 5 + 1 round_by_digits' )

    # round_by_value
    expectResult( '0.1 1 round_by_value', 0 )
    expectResult( '4.5 1 round_by_value', 5 )
    expectResult( '4.5 2 round_by_value', 4 )
    expectResult( '8 3 round_by_value', 9 )
    expectResult( '4500 7 round_by_value', 4501 )
    expectEqual( 'pi 0.01 round_by_value', '3.14' )
    expectEqual( '88 mph 10 round_by_value', '90 mph' )
    expectException( '12.3 i 1 round_by_value' )

    # sign
    expectResult( '1 sign', 1 )
    expectResult( '0 sign', 0 )
    expectResult( '-1 sign', -1 )
    expectResult( 'infinity sign', 1 )
    expectResult( 'negative_infinity sign', -1 )
    expectResult( '-2 cups sign', -1 )

    # smaller
    expectResult( '7 -7 smaller' , -7 )
    expectException( '2 i 5 + 3 smaller' )

    # stddev
    testOperator( '1 10 range stddev' )
    testOperator( '1 1 10 range range stddev' )

    # subtract
    testOperator( '3948 474 subtract' )
    expectResult( '4 cups 27 teaspoons - teaspoons convert', RPNMeasurement( 165, 'teaspoon' ) )
    testOperator( '57 hectares 23 acres -' )
    testOperator( '10 Mb second / 700 MB hour / -' )
    testOperator( 'today 3 days -' )
    testOperator( 'today 3 weeks -' )
    testOperator( 'today 3 months -' )
    testOperator( 'now earth_radius 2 pi * * miles convert 4 mph / -' )
    testOperator( 'today 2 months -' )
    testOperator( 'today 1965-03-31 -' )
    testOperator( '2015-01-01 1965-03-31 -' )

    expectException( '2 light-year 3 seconds -' )

    # sum
    expectResult( '1 10 range sum', 55 )
    testOperator( '[ 27 days 7 hour 43 minute 12 second ] sum' )
    testOperator( '1 1 10 range range sum' )
    expectEqual( '[ 2 cups 3 cups 4 cups 5 cups ] sum', '14 cups' )
    expectEqual( '2 1000 range factor sum', '1414 oeis 1000 left 999 right' )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    # antitransit_time
    testOperator( 'moon "Calais, France" location today antitransit_time' )
    testOperator( 'sun "Calais, France" today antitransit_time' )
    testOperator( 'jupiter "Las Vegas, NV" 2016 spring 1 20 range days + antitransit_time' )

    # astronomical_dawn
    testOperator( '"Chattanooga, TN" location today astronomical_dawn' )
    testOperator( '"Chattanooga, TN" today astronomical_dawn' )

    # astronomical_dusk
    testOperator( '"Perth, Australia" location today astronomical_dusk' )
    testOperator( '"Perth, Australia" today astronomical_dusk' )

    # autumnal_equinox
    testOperator( '2015 autumnal_equinox' )

    # dawn
    testOperator( '"Christchurch, NZ" location today dawn' )
    testOperator( '"Christchurch, NZ" today dawn' )

    # day_time
    testOperator( '"Toulouse, France" location today day_time' )
    testOperator( '"Nice, France" today day_time' )
    testOperator( '"Allentown, PA" 1975-03-31 0 20 range days + day_time' )

    # dusk
    testOperator( '"Vienna, Austria" location today dusk' )
    testOperator( '"Vienna, Austria" today dusk' )

    # jupiter
    testOperator( 'jupiter "Ottawa, Canada" location today next_setting' )
    testOperator( 'jupiter "Ottawa, Canada" today next_setting' )

    # mars
    testOperator( 'mars "Beijing, China" location today next_transit' )
    testOperator( 'mars "Beijing, China" today next_transit' )

    # mercury
    testOperator( 'mercury "Los Angeles, CA" location today next_rising' )
    testOperator( 'mercury "Los Angeles, CA" today next_rising' )

    # moon
    testOperator( 'saturn "Burlington, VT" location today next_antitransit' )
    testOperator( 'saturn "Burlington, VT" today next_antitransit' )

    # moon_antitransit
    testOperator( '"Madrid, Spain" location today moon_antitransit' )
    testOperator( '"Madrid, Spain" today moon_antitransit' )

    # moon_phase
    testOperator( 'today moon_phase' )

    # moon_transit
    testOperator( '"Riga, Latvia" location today moon_transit' )
    testOperator( '"Riga, Latvia" today moon_transit' )

    # moonrise
    testOperator( '"Las Cruces, NM" location today moonrise' )
    testOperator( '"Las Cruces, NM" today moonrise' )

    # moonset
    testOperator( '"Tacoma, WA" location today moonset' )
    testOperator( '"Tacoma, WA" today moonset' )

    # nautical_dawn
    testOperator( '"Columbia, SC" location today nautical_dawn' )
    testOperator( '"Columbia, SC" today nautical_dawn' )

    # nautical_dusk
    testOperator( '"Norfolk, VA" location today nautical_dusk' )
    testOperator( '"Norfolk, VA" today nautical_dusk' )

    # neptune
    testOperator( 'neptune "Hatfield, PA" location now next_rising' )
    testOperator( 'neptune "Hatfield, PA" now next_rising' )

    # next_antitransit
    testOperator( 'saturn "Blacksburg, VA" location today next_antitransit' )
    testOperator( 'saturn "Blacksburg, VA" today next_antitransit' )

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
    testOperator( 'moon "Leesburg, VA" now next_rising' )

    # next_setting
    testOperator( 'moon "Kyoto, Japan" location now next_setting' )
    testOperator( 'moon "Kyoto, Japan" now next_setting' )

    # next_transit
    testOperator( 'moon "Oslo, Norway" location now next_transit' )
    testOperator( 'moon "Oslo, Norway" now next_transit' )

    # night_time
    testOperator( '"Toulouse, France" location today night_time' )
    testOperator( '"Nice, France" today night_time' )
    testOperator( '"Cologne, Germany" 2015 winter 1 20 range days + night_time' )

    # pluto
    testOperator( 'pluto "Johannesburg, South Africa" location now next_rising' )
    testOperator( 'pluto "Johannesburg, South Africa" now next_rising' )

    # previous_antitransit
    testOperator( 'neptune "Leesburg, VA" location now previous_antitransit' )
    testOperator( 'neptune "Leesburg, VA" now previous_antitransit' )

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
    testOperator( 'jupiter "Leesburg, VA" now previous_rising' )

    # previous_setting
    testOperator( 'uranus "Leesburg, VA" location now previous_setting' )
    testOperator( 'uranus "Leesburg, VA" now previous_setting' )

    # previous_transit
    testOperator( 'mercury "Leesburg, VA" location now previous_transit' )
    testOperator( 'mercury "Leesburg, VA" now previous_transit' )

    # saturn
    testOperator( 'saturn "Leesburg, VA" location today next_rising' )
    testOperator( 'saturn "Leesburg, VA" today next_rising' )

    # sky_location
    testOperator( 'mars now sky_location' )

    # solar_noon
    testOperator( '"Leesburg, VA" location today solar_noon' )
    testOperator( '"Leesburg, VA" today solar_noon' )

    # summer_solstice
    testOperator( '2015 summer_solstice' )

    # sun
    testOperator( 'sun "Leesburg, VA" location today next_rising' )
    testOperator( 'sun "Leesburg, VA" today next_rising' )

    # sun_antitransit
    testOperator( '"Leesburg, VA" location today sun_antitransit' )
    testOperator( '"Leesburg, VA" today sun_antitransit' )

    # sunrise
    testOperator( '"Salzburg, Germany" location today sunrise' )
    testOperator( '"Salzburg, Germany" today sunrise' )

    # sunset
    testOperator( '"New Delhi, India" location today sunset' )
    testOperator( '"New Delhi, India" today sunset' )

    # transit_time
    testOperator( 'sun "Munich, Germany" location today transit_time' )
    testOperator( 'moon "Dusseldorf, Germany" today transit_time' )
    testOperator( 'mars "Dortmund, Germany" 2015 summer 1 20 range days + transit_time' )

    # uranus
    testOperator( 'uranus "Frankfurt, Germany" location today next_rising' )
    testOperator( 'uranus "Frankfurt, Germany" today next_rising' )

    # venus
    testOperator( 'venus "Butte, Montana" location today next_rising' )
    testOperator( 'venus "Butte, Montana" today next_rising' )

    # vernal_equinox
    testOperator( '2015 vernal_equinox' )

    # winter_solstice
    testOperator( '2015 winter_solstice' )


# //******************************************************************************
# //
# //  runBitwiseOperatorTests
# //
# //******************************************************************************

def runBitwiseOperatorTests( ):
    # bitwise_and
    testOperator( '0x7777 0xdcba bitwise_and' )

    # bitwise_nand
    testOperator( '-x 0x5543 0x7789 bitwise_nand' )

    # bitwise_nor
    testOperator( '-x 0x5543 0x7789 bitwise_nor' )

    # bitwise_not
    testOperator( '0xffffff ~' )
    testOperator( '142857 bitwise_not' )
    testOperator( '-x 0xefefefefefefef bitwise_not' )

    # bitwise_xor
    testOperator( '0x1939 0x3948 bitwise_xor' )

    # count_bits
    testOperator( '0xffff count_bits' )

    # not
    expectEqual( '[ 0 10 dup ] not', '[ 1 10 dup ]' )

    # or
    testOperator( '-x 0x5543 0x7789 bitwise_or' )

    # parity
    testOperator( '0xff889d8f parity' )
    expectEqual( '0 20000 range parity nonzero', '69 oeis 10001 left' )

    # shift_left
    testOperator( '-x 0x10 3 shift_left' )

    # shift_right
    testOperator( '-x 0x1000 4 shift_right' )


# //******************************************************************************
# //
# //  runCalendarOperatorTests
# //
# //******************************************************************************

def runCalendarOperatorTests( ):
    # ash_wednesday
    testOperator( '2015 ash_wednesday' )

    # calendar
    testOperator( '1965-03-31 calendar' )
    testOperator( '2014-10-01 calendar' )
    testOperator( 'today calendar' )

    # ascension
    testOperator( '2016 ascension' )

    # christmas
    testOperator( '2016 christmas' )

    # columbus_day
    testOperator( '2017 columbus_day' )

    # dst_end
    testOperator( '2015 dst_end' )

    # dst_start
    testOperator( '2015 dst_start' )

    # easter
    testOperator( '2015 easter' )

    # election_day
    testOperator( '2015 election_day' )

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

    # independence_day
    testOperator( '2017 independence_day' )

    # iso_date
    testOperator( 'today iso_date' )

    # labor_day
    testOperator( '2015 labor_day' )

    # martin_luther_king_day
    testOperator( '2017 martin_luther_king_day' )

    # memorial_day
    testOperator( '2015 memorial_day' )

    # nth_weekday
    testOperator( '2015 march 4 thursday nth_weekday' )
    testOperator( '2015 march -1 thursday nth_weekday' )

    # nth_weekday_of_year
    testOperator( '2015 20 thursday nth_weekday_of_year' )
    testOperator( '2015 -1 thursday nth_weekday_of_year' )

    # pentecost
    testOperator( '2016 pentecost' )

    # presidents_day
    testOperator( '2015 presidents_day' )

    # thanksgiving
    testOperator( '2015 thanksgiving' )

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

    # veterans_day
    testOperator( '2017 veterans_day' )

    # weekday
    testOperator( 'today weekday' )
    expectException( '2017-00-01 weekday' )
    expectException( '2017-13-01 weekday' )
    expectException( '2017-01-32 weekday' )
    expectException( '2017-04-31 weekday' )
    expectException( '1951-02-29 weekday' )

    # year_calendar
    testOperator( '1965 year_calendar' )
    testOperator( 'today year_calendar' )


# //******************************************************************************
# //
# //  runChemistryOperatorTests
# //
# //******************************************************************************

def runChemistryOperatorTests( ):
    # atomic_number
    expectResult( 'He atomic_number', 2 )
    expectResult( 'Ne atomic_number', 10 )
    expectResult( 'Fe atomic_number', 26 )
    expectResult( 'U atomic_number', 92 )
    expectException( 'Va atomic_number' )

    # atomic_symbol
    testOperator( '1 atomic_symbol' )
    testOperator( '118 atomic_symbol' )
    expectException( '119 atomic_symbol' )
    expectException( '0 atomic_symbol' )

    # atomic_weight
    testOperator( '1 118 range atomic_weight' )
    expectException( '119 atomic_symbol' )
    expectException( '0 atomic_symbol' )

    # element_block
    testOperator( '1 118 range element_block')
    expectException( '119 element_block' )
    expectException( '0 element_block' )

    # element_boiling_point
    testOperator( '1 118 range element_boiling_point')
    expectException( '119 element_boiling_point' )
    expectException( '0 element_boiling_point' )

    # element_density
    testOperator( '1 118 range element_density')
    expectException( '119 element_density' )
    expectException( '0 element_density' )

    # element_description
    testOperator( '1 118 range element_description' )
    expectException( '119 element_description' )
    expectException( '0 element_description' )

    # element_group
    testOperator( '1 118 range element_group')
    expectException( '119 element_group' )
    expectException( '0 element_group' )

    # element_melting_point
    testOperator( '1 118 range element_melting_point')
    expectException( '119 element_melting_point' )
    expectException( '0 element_melting_point' )

    # element_name
    testOperator( '1 118 range element_name' )
    expectException( '119 element_name' )
    expectException( '0 element_name' )

    # element_occurrence
    testOperator( '1 118 range element_occurrence' )
    expectException( '119 element_occurrence' )
    expectException( '0 element_occurrence' )

    # element_period
    testOperator( '1 118 range element_period' )
    expectException( '119 element_period' )
    expectException( '0 element_period' )

    # molar_mass
    testOperator( 'H2O molar_mass' )
    testOperator( 'C12H22O11 molar_mass' )
    expectException( 'ZoO2 molar_mass' )


# //******************************************************************************
# //
# //  runCombinatoricsOperatorTests
# //
# //******************************************************************************

def runCombinatoricsOperatorTests( ):
    # arrangements
    expectEqual( '5 arrangements', '5 0 5 range permutations sum' )
    expectEqual( '-a20 20 arrangements', '-a20 20 0 20 range permutations sum' )

    # bell_polynomal
    testOperator( '4 5 bell_polynomial' )
    testOperator( '5 5 10 range bell_polynomial' )

    from rpnSpecial import downloadOEISSequence

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
            expectEqual( str( i ) + ' ' + str( j ) + ' bell_polynomial',
                         bell_poly_str + str( j ) + ' eval_polynomial' )

    # binomial
    testOperator( '12 9 binomial' )
    testOperator( '-a20 -c 120 108 binomial' )
    expectEqual( '8 1 992 sized_range lambda x 2 * 8 - 7 binomial 8 / eval', '973 oeis 992 left' )
    expectEqual( '0 999 range lambda x 3 binomial x 2 binomial + x 1 binomial + x 0 binomial + eval', '125 oeis 1000 left' )
    expectEqual( '0 1002 range lambda x 4 binomial eval', '332 oeis 1003 left' )
    #expectEqual( '0 500 range lambda 2 2 x * 1 + ** 2 x * 1 + x 1 + binomial eval', '346 oeis 501 left' )

    # combinations

    # compositions
    testOperator( '5 2 compositions' )
    testOperator( '6 3 compositions' )
    testOperator( '7 2 4 range compositions' )

    # debruijn
    testOperator( '4 3 debruijn' )

    # lah
    testOperator( '5 6 lah' )

    # menage
    expectEqual( '-a160 0 100 range nth_menage', '-a160 179 oeis 101 left' )

    # multifactorial
    testOperator( '1 20 range 5 multifactorial' )
    expectEqual( '-a1000 0 805 range 2 multifactorial', '6882 oeis 806 left' )
    expectEqual( '-a125 0 200 range 3 multifactorial', '7661 oeis 201 left' )
    expectEqual( '-a285 0 500 range 4 multifactorial', '7662 oeis 501 left' )
    expectEqual( '0 36 range 5 multifactorial', '85157 oeis 37 left' )
    expectEqual( '0 38 range 6 multifactorial', '85158 oeis 39 left' )
    expectEqual( '0 40 range 7 multifactorial', '114799 oeis 41 left' )
    expectEqual( '0 42 range 8 multifactorial', '114800 oeis 43 left' )
    expectEqual( '0 43 range 9 multifactorial', '114806 oeis 44 left' )

    # multinomial
    testOperator( '[ 2 5 6 7 ] multinomial' )

    # narayana
    testOperator( '6 8 narayana' )

    # nth_apery
    testOperator( '-a20 12 nth_apery' )
    expectEqual( '0 99 range nth_apery', '5259 oeis 100 left' )

    if slow:
        expectEqual( '0 656 range nth_apery', '5259 oeis 657 left' )

    # nth_bell
    testOperator( '-a43 45 nth_bell' )
    expectEqual( '-a845 0 500 range nth_bell', '-a20 110 oeis 501 left' )

    # nth_bernoulli
    testOperator( '16 nth_bernoulli' )
    expectEqual( '-a222 0 200 range nth_bernoulli', '-a20 27641 oeis 201 left 27642 oeis 201 left /' )
    expectEqual( '1 551 range lambda 2 1 2 x ** - * x bernoulli * eval', '36968 oeis 551 left' )

    # nth_catalan
    testOperator( '-a50 85 nth_catalan' )
    expectEqual( '-a117 1 200 2 range2 nth_catalan', '24492 oeis 100 left' )

    # nth_delannoy
    testOperator( '-a80 100 nth_delannoy' )
    expectEqual( '-a80 0 99 range nth_delannoy', '1850 oeis 100 left' )

    if slow:
        expectEqual( '-a80 0 1308 range nth_delannoy', '1850 oeis 1309 left' )

    # nth_motzkin
    testOperator( '-a25 56 nth_motzkin' )
    expectEqual( '0 299 range nth_motzkin', '1006 oeis 300 left' )

    if slow:
        expectEqual( '0 2106 range nth_motzkin', '1006 oeis 2016 left' )

    # nth_pell
    testOperator( '13 nth_pell' )
    expectEqual( '-a383 1 100 range nth_pell', '129 oeis 100 left' )

    if slow:
        expectEqual( '-a383 1 1001 range nth_pell', '129 oeis 1001 left' )

    # nth_schroeder
    testOperator( '-a50 67 nth_schroeder' )
    expectEqual( '1 100 range nth_schroeder', '6318 oeis 100 left' )

    if slow:
        expectEqual( '0 1999 range nth_schroeder', '6318 oeis 2000 left' )

    # nth_sylvester
    testOperator( '45 nth_sylvester' )
    expectEqual( '1 13 range nth_sylvester', '58 oeis 13 left' )

    # partitions
    expectEqual( '0 1000 range partitions', '41 oeis 1001 left' )

    # permutations
    expectEqual( '8 3 permutations', '8 ! 5 ! /' )
    expectEqual( '-a20 17 12 permutations', '-a20 17 ! 5 ! /' )
    expectException( '6 7 permutations' )


# //******************************************************************************
# //
# //  runComplexMathOperatorTests
# //
# //******************************************************************************

def runComplexMathOperatorTests( ):
    # argument
    testOperator( '3 3 i + argument' )

    # conjugate
    expectEqual( '3 3 i + conjugate', '3 3 i -' )
    expectEqual( '3 3 i + conjugate', '3 3 i -' )
    expectEqual( '5 i 7 - conjugate', '-5 i 7 -' )

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
    expectResult( 'default', -1 )
    expectResult( 'false', 0 )
    expectResult( 'true', 1 )

    # infinity
    testOperator( 'infinity lambda x fib x 1 - fib / limit' )
    expectEqual( 'infinity lambda x fib x 1 - fib / limit', 'phi' )
    testOperator( 'infinity lambda x 1/x 1 + x ** limit' )

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

    # mathematical constants
    testOperator( 'apery_constant' )
    testOperator( 'catalan_constant' )
    testOperator( 'champernowne_constant' )
    testOperator( 'copeland_erdos_constant' )

    testOperator( 'e' )
    expectEqual( '-a150 e 0 300 range ** floor', '149 oeis 301 left' )

    testOperator( 'eddington_number' )
    testOperator( 'euler_mascheroni_constant' )
    testOperator( 'glaisher_constant' )
    testOperator( 'infinity' )
    testOperator( 'itoi' )
    testOperator( 'khinchin_constant' )
    testOperator( 'merten_constant' )
    testOperator( 'mills_constant' )
    testOperator( 'negative_infinity' )
    testOperator( 'omega_constant' )

    testOperator( 'phi' )
    expectEqual( '1 10000 range phi * floor', '201 oeis 10000 left' )

    testOperator( 'pi' )
    testOperator( 'plastic_constant' )
    testOperator( 'prevost_constant' )
    testOperator( 'robbins_constant' )
    testOperator( 'silver_ratio' )

    # physical quantities
    testOperator( 'aa_battery' )
    testOperator( 'gallon_of_ethanol' )
    testOperator( 'gallon_of_gasoline' )
    testOperator( 'density_of_water' )
    testOperator( 'density_of_hg' )

    # physical constants
    testOperator( 'avogadro_number' )
    testOperator( 'bohr_radius' )
    testOperator( 'boltzmann_constant' )
    testOperator( 'coulomb_constant' )
    testOperator( 'electric_constant' )
    testOperator( 'electron_charge' )
    testOperator( 'faraday_constant' )
    testOperator( 'fine_structure_constant' )
    testOperator( 'magnetic_constant' )
    testOperator( 'newton_constant' )
    testOperator( 'radiation_constant' )
    testOperator( 'rydberg_constant' )
    testOperator( 'speed_of_light' )
    testOperator( 'stefan_boltzmann_constant' )
    testOperator( 'vacuum_impedance' )
    testOperator( 'von_klitzing_constant' )

    # programming integer constants
    expectEqual( 'max_char', '2 7 ** 1 -' )
    testOperator( 'max_double' )
    testOperator( 'max_float' )
    expectEqual( 'max_long', '2 31 ** 1 -' )
    expectEqual( '-a20 max_longlong', '-a20 2 63 ** 1 -' )
    expectEqual( '-a40 max_quadlong', '-a40 2 127 ** 1 -' )
    expectEqual( 'max_short', '2 15 ** 1 -' )
    expectEqual( 'max_uchar', '2 8 ** 1 -' )
    expectEqual( 'max_ulong', '2 32 ** 1 -' )
    expectEqual( '-a20 max_ulonglong', '-a20 2 64 ** 1 -' )
    expectEqual( '-a40 max_uquadlong', '-a40 2 128 ** 1 -' )
    expectEqual( 'max_ushort', '2 16 ** 1 -' )

    expectEqual( 'min_char', '2 7 ** negative' )
    testOperator( 'min_double' )
    testOperator( 'min_float' )
    expectEqual( 'min_long', '2 31 ** negative' )
    expectEqual( '-a20 min_longlong', '-a20 2 63 ** negative' )
    expectEqual( '-a40 min_quadlong', '-a40 2 127 ** negative' )
    expectEqual( 'min_short', '2 15 ** negative' )
    expectResult( 'min_uchar', 0 )
    expectResult( 'min_ulong', 0 )
    expectResult( 'min_ulonglong', 0 )
    expectResult( 'min_uquadlong', 0 )
    expectResult( 'min_ushort', 0 )

    # Planck constants
    testOperator( 'planck_constant' )
    testOperator( 'reduced_planck_constant' )

    testOperator( 'planck_length' )
    testOperator( 'planck_mass' )
    testOperator( 'planck_time' )
    testOperator( 'planck_charge' )
    testOperator( 'planck_temperature' )

    testOperator( 'planck_angular_frequency' )
    testOperator( 'planck_area' )
    testOperator( 'planck_current' )
    testOperator( 'planck_density' )
    testOperator( 'planck_energy' )
    testOperator( 'planck_energy_density' )
    testOperator( 'planck_force' )
    testOperator( 'planck_impedance' )
    testOperator( 'planck_intensity' )
    testOperator( 'planck_momentum' )
    testOperator( 'planck_power' )
    testOperator( 'planck_pressure' )
    testOperator( 'planck_voltage' )
    testOperator( 'planck_volume' )

    # subatomic particle constants
    testOperator( 'alpha_particle_mass' )
    testOperator( 'deuteron_mass' )
    testOperator( 'electron_mass' )
    testOperator( 'helion_mass' )
    testOperator( 'muon_mass' )
    testOperator( 'neutron_mass' )
    testOperator( 'proton_mass' )
    testOperator( 'tau_mass' )
    testOperator( 'triton_mass' )

    # heavenly body constants
    testOperator( 'solar_luminosity' )
    testOperator( 'solar_mass' )
    testOperator( 'solar_radius' )
    testOperator( 'solar_volume' )

    testOperator( 'mercury_mass' )
    testOperator( 'mercury_radius' )
    testOperator( 'mercury_revolution' )
    testOperator( 'mercury_volume' )

    testOperator( 'venus_mass' )
    testOperator( 'venus_radius' )
    testOperator( 'venus_revolution' )
    testOperator( 'venus_volume' )

    testOperator( 'earth_gravity' )
    testOperator( 'earth_mass' )
    testOperator( 'earth_radius' )
    testOperator( 'earth_volume' )
    testOperator( 'sidereal_year' )
    testOperator( 'tropical_year' )

    testOperator( 'moon_gravity' )
    testOperator( 'moon_mass' )
    testOperator( 'moon_radius' )
    testOperator( 'moon_revolution' )
    testOperator( 'moon_volume' )

    testOperator( 'mars_mass' )
    testOperator( 'mars_radius' )
    testOperator( 'mars_revolution' )
    testOperator( 'mars_volume' )

    testOperator( 'jupiter_mass' )
    testOperator( 'jupiter_radius' )
    testOperator( 'jupiter_revolution' )
    testOperator( 'jupiter_volume' )

    testOperator( 'saturn_mass' )
    testOperator( 'saturn_radius' )
    testOperator( 'saturn_revolution' )
    testOperator( 'saturn_volume' )

    testOperator( 'uranus_mass' )
    testOperator( 'uranus_radius' )
    testOperator( 'uranus_revolution' )
    testOperator( 'uranus_volume' )

    testOperator( 'neptune_mass' )
    testOperator( 'neptune_radius' )
    testOperator( 'neptune_revolution' )
    testOperator( 'neptune_volume' )

    testOperator( 'pluto_mass' )
    testOperator( 'pluto_radius' )
    testOperator( 'pluto_revolution' )
    testOperator( 'pluto_volume' )


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

    # hms
    testOperator( '54658 seconds hms' )

    # integer
    testOperator( '456 8 integer' )

    # invert_units
    testOperator( '30 miles gallon / invert_units' )

    # latlong_to_nac
    testOperator( '"Detroit, MI" location_info latlong_to_nac' )

    # long
    testOperator( '3456789012 long' )

    # longlong
    testOperator( '1234567890123456789012 longlong' )

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
    # get_day
    testOperator( 'now get_day' )

    # get_hour
    testOperator( 'now get_hour' )

    # get_minute
    testOperator( 'now get_minute' )

    # get_month
    testOperator( 'now get_month' )

    # get_second
    testOperator( 'now get_second' )

    # get_year
    testOperator( 'now get_year' )

    # iso_day
    testOperator( 'today iso_day' )

    # make_datetime
    testOperator( '[ 1965 03 31 ] make_datetime' )

    # make_iso_time
    testOperator( '[ 2015 34 6 ] make_iso_time' )

    # make_julian_time
    testOperator( '[ 2015 7 5 4 3 ] make_julian_time' )

    # now
    testOperator( 'now' )

    # today
    testOperator( 'today' )

    # tomorrow
    testOperator( 'tomorrow' )

    # yesterday
    testOperator( 'yesterday' )


# //******************************************************************************
# //
# //  runFunctionOperatorTests
# //
# //******************************************************************************

def runFunctionOperatorTests( ):
    # break_on

    # eval
    testOperator( '10 lambda x 5 * eval' )
    testOperator( '-a20 57 lambda x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )
    expectEqual( '-a121 0 200 range lambda x 0 * 2 x 1 - power + 2 x power 1 - * eval', '6516 oeis 201 left' )
    expectEqual( '1 9999 range lambda x sqr 2 * 2 + eval', '5893 oeis 10000 left 9999 right' )

    # eval2
    testOperator( '7 8 lambda x 2 ** y 3 ** + eval2' )

    # eval3
    testOperator( '15 4 26 lambda x 2 ** y 3 ** + z 4 ** + eval3' )

    # filter
    testOperator( '-a20 1 80 range fib lambda x is_prime filter' )
    expectEqual( '1 10000 range lambda x is_prime filter', '1 1229 primes' )

    # filter_by_index
    expectEqual( '0 10000 range lambda x is_prime filter_by_index', '1 1229 primes' )

    # limit
    testOperator( 'infinity lambda 1 1 x / + x power limit' )
    testOperator( '0 lambda x x / 2 -1 x / power + 1/x limit' )
    testOperator( 'infinity lambda x x ! x root / limit' )   # This one isn't very precise...
    expectEqual( 'infinity lambda x fibonacci x 1 + fibonacci / limit', 'infinity lambda x lucas x 1 + lucas / limit' )
    expectEqual( 'infinity lambda 1 1 x / + x power limit', 'e' )
    expectEqual( 'infinity lambda x 1 x / sin * limit', '1' )
    expectEqual( 'inf lambda 7 x / 1 + 3 x * ** limit', 'e 7 3 * **' )

    # limitn
    testOperator( '0 lambda x x / 2 -1 x / power + 1/x limitn' )
    expectEqual( '0 lambda x x sin / limitn', '1' )

    # negate
    expectEqual( '[ 0 10 dup ] not', '[ 1 10 dup ]' )

    # nprod
    testOperator( '-a20 -p20 -d5 3 inf lambda x pi / 1/x cos nprod' )

    # nsum
    expectEqual( '1 infinity lambda x 3 ** 1/x nsum', '3 zeta' )
    expectEqual( '0 infinity lambda 1 x ! / nsum', 'e' )

    # These operators use the plotting GUI, so aren't included in the automated tests.
    # plot
    # plot2
    # plotc

    # recurrence
    expectEqual( '2 99 lambda x get_digits sqr sum recurrence', '216 oeis 100 left' )
    expectEqual( '3 99 lambda x get_digits sqr sum recurrence', '218 oeis 100 left' )
    expectEqual( '5 99 lambda x get_digits sqr sum recurrence', '221 oeis 100 left' )
    expectEqual( '-a1000 1 10000 lambda x tan recurrence floor', '319 oeis 10001 left' )

    # unfilter
    expectEqual( '1 10100 range lambda x is_square unfilter', '37 oeis 10000 left' )

    # unfilter_by_index
    expectEqual( '0 2000 range lambda x is_sphenic unfilter_by_index', '0 2000 range lambda x is_sphenic unfilter' )

    # x
    testOperator( '23 lambda x 4 ** 5 x 3 ** * + x sqrt - eval' )

    # y
    testOperator( '23 57 lambda x 4 ** 5 x 3 ** * + y sqrt - eval2' )

    # z
    testOperator( '23 57 86 lambda x 4 ** 5 y 3 ** * + z sqrt - eval3' )


# //******************************************************************************
# //
# //  runGeographyOperatorTests
# //
# //******************************************************************************

def runGeographyOperatorTests( ):
    # distance
    testOperator( '"Leesburg, VA" location "Smithfield, VA" location distance' )
    testOperator( '"Leesburg, VA" "Smithfield, VA" distance' )

    # latlong
    #testOperator( '"Leesburg, VA" 43 -80 latlong distance' )

    # location
    testOperator( '"Uppsala, Sweden" location today moonrise' )

    # location_info
    testOperator( '"Dakar, Senegal" location_info' )
    testOperator( '"Scottsdale, AZ" location_info' )


# //******************************************************************************
# //
# //  runGeometryOperatorTests
# //
# //******************************************************************************

def runGeometryOperatorTests( ):
    # antiprism_area
    testOperator( '8 5 antiprism_area' )

    # antiprism_volume
    testOperator( '3 8 antiprism_volume' )

    # cone_area
    testOperator( '4 5 cone_area' )

    # cone_volume
    testOperator( '3 8 cone_volume' )

    # dodecahedron_area
    testOperator( '1 dodecahedron_area' )

    # dodecahedron_volume
    testOperator( '1 dodecahedron_volume' )

    # icosahedron_area
    testOperator( '1 icosahedron_area' )

    # icosahedron_volume
    testOperator( '1 icosahedron_volume' )

    # n_sphere_area
    testOperator( '34 inches 8 n_sphere_area' )
    testOperator( '34 inches 4 ** 5 n_sphere_area' )
    testOperator( '34 inches 7 ** 7 n_sphere_area' )
    expectException( '34 cubic_inches 2 n_sphere_area' )

    # n_sphere_radius
    testOperator( '3 meters 4 n_sphere_radius' )
    testOperator( '3 meters 3 ** 4 n_sphere_radius' )
    testOperator( '3 cubic_meters 4 n_sphere_radius' )
    expectException( '3 cubic_meters 2 n_sphere_radius' )

    # n_sphere_volume
    testOperator( '6 inches 8 ** 9 n_sphere_volume' )
    testOperator( '3 feet 5 ** 6 n_sphere_volume' )
    testOperator( '50 cubic_centimeters sqr 7 n_sphere_volume' )
    expectException( '50 cubic_centimeters 1 n_sphere_volume' )

    # octahedron_area
    testOperator( '1 octahedron_area' )

    # octahedron_volume
    testOperator( '1 octahedron_volume' )

    # polygon_area
    testOperator( '13 1 inch polygon_area square_inches convert' )
    testOperator( '3 10 range 1 polygon_area' )

    # prism_area
    testOperator( '8 5 2 prism_area' )

    # prism_volume
    testOperator( '3 8 4 prism_volume' )

    # sphere_area
    testOperator( '8 inches sphere_area' )
    testOperator( '8 sq_inches sphere_area' )
    testOperator( '8 cu_inches sphere_area' )

    # sphere_radius
    testOperator( '4 inches sphere_radius' )
    testOperator( '4 square_inches sphere_radius' )
    testOperator( '4 cubic_inches sphere_radius' )

    # sphere_volume
    testOperator( '5 inches sphere_volume' )
    testOperator( '5 sq_inches sphere_volume' )
    testOperator( '5 cubic_in sphere_volume' )

    # tetrahedron_area
    testOperator( '1 tetrahedron_area' )

    # tetrahedron_volume
    testOperator( '1 tetrahedron_volume' )

    # torus_area
    testOperator( '12 5 torus_area' )

    # torus_volume
    testOperator( '20 8 torus_volume' )

    # triangle_area
    testOperator( '456 456 789 triangle_area' )


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

    # _dump_constants
    testOperator( '_dump_constants' )

    # _dump_units
    testOperator( '_dump_units' )

    # _stats
    testOperator( '_stats' )


# //******************************************************************************
# //
# //  runLexicographyOperatorTests
# //
# //******************************************************************************

def runLexicographyOperatorTests( ):
    # add_digits
    expectResult( '3 4 add_digits', 34 )
    expectResult( '3 45 add_digits', 345 )
    expectResult( '34 567 add_digits', 34567 )

    # build_numbers
    testOperator( '123d build_numbers' )
    testOperator( '[0-3]d0[3-5] build_numbers' )
    testOperator( '[246]d[7-9][12] build_numbers' )
    testOperator( '[123:1] build_numbers' )
    testOperator( '[123:2] build_numbers' )
    testOperator( '[123:3] build_numbers' )
    testOperator( '[1-3:2:3] build_numbers' )
    testOperator( '[1-38-9:2:3] build_numbers' )
    testOperator( '[1-3:2][8-9:2] build_numbers' )
    expectEqual( '[37:1:12] build_numbers', '143967 oeis 8190 left' )

    # combine_digits
    testOperator( '1 1 7 range primes combine_digits' )
    expectResult( '1 9 range combine_digits', 123456789 )
    expectEqual( '1 150 range lambda x 1 range combine_digits eval', '422 oeis 150 left' )

    # count_different_digits
    expectEqual( '1 2579 range lambda x sqr count_different_digits 5 equals filter', '54033 oeis 1000 left' )
    expectEqual( '1 20000 range triangular lambda x count_different_digits 2 equals filter', '62691 oeis 36 left' )

    # dup_digits
    expectResult( '543 2 dup_digits', 54343 )
    expectResult( '1024 1 4 range dup_digits', [ 10244, 102424, 1024024, 10241024 ] )

    # erdos_persistence
    expectResult( '55555555555555557777777777777 erdos_persistence', 12 )

    # find_palindrome
    testOperator( '-a30 10911 55 find_palindrome' )
    testOperator( '180 200 range 10 find_palindrome -s1' )

    # get_base_k_digits
    testOperator( '1 million 7 get_base_k_digits' )

    # get_digits
    testOperator( '123456789 get_digits' )
    expectEqual( '0 1000 range lambda x get_digits 1 left eval flatten', '30 oeis 1001 left' )

    if slow:
        expectEqual( '0 10000 range lambda x get_digits 1 left eval flatten', '30 oeis 10001 left' )

    # get_left_digits

    # get_left_truncations
    testOperator( '123456789 get_left_truncations' )

    # get_right_digits
    expectEqual( '-a420 1 2000 range lambda x fib x log10 floor 1 + get_right_digits x equals filter', '-a420 350 oeis 42 left 41 right' )

    if slow:
        expectEqual( '-a21000 dddd[159] build_numbers lambda x fib x log10 floor 1 + get_right_digits x equals filter', '-a420 350 oeis 573 left 572 right' )

    # get_right_truncations
    testOperator( '123456789 get_right_truncations' )

    # has_any_digits
    expectEqual( '1 1113 primes lambda x 2357 has_any_digits filter', '179336 oeis 1000 left' )

    if slow:
        expectEqual( '1 10776 primes lambda x 2357 has_any_digits filter', '179336 oeis 10000 left' )

    # has_digits
    expectEqual( '0 4005 range lambda x 0 has_digits filter', '11540 oeis 1000 left' )

    if slow:
        expectEqual( '0 30501 range lambda x 0 has_digits filter', '11540 oeis 10000 left' )

    # has_only_digits
    expectEqual( '1 20000 range lambda x triangular 120 has_only_digits filter', '119034 oeis 15 left' )

    # is_automorphic
    testOperator( '1 100 range lambda x is_automorphic filter' )
    expectResult( '-a30 59918212890625 is_automorphic', 1 )

    # is_bouncy

    # is_decreasing

    # is_digital_permutation

    # is_harshad

    # is_increasing

    # is_kaprekar
    expectResult( '533170 is_kaprekar', 1 )
    expectResult( '77777 is_kaprekar', 0 )
    expectResult( '77778 is_kaprekar', 1 )
    expectResult( '95121 is_kaprekar', 1 )
    expectResult( '7272 is_kaprekar', 1 )
    expectResult( '22223 is_kaprekar', 0 )
    expectEqual( '1 10000 range lambda x is_kaprekar filter', '53816 oeis 15 left' )

    # is_morphic
    testOperator( '1 100 range lambda x 7 is_morphic filter' )
    expectEqual( '1 10000 range lambda x x is_morphic filter', '82576 oeis 234 left' )

    # is_narcissistic
    expectResult( '152 is_narcissistic', 0 )
    expectResult( '153 is_narcissistic', 1 )
    expectResult( '154 is_narcissistic', 0 )
    expectEqual( '1 10000 range lambda x is_narcissistic filter', '5188 oeis 16 left' )

    # is_palindrome
    expectResult( '101 is_palindrome', 1 )
    expectResult( '1 22 range is_palindrome', [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1234567890 is_palindrome', 0 )
    expectEqual( '0 10000 range lambda x is_palindrome filter', '2113 oeis 199 left' )

    # is_pandigital
    expectResult( '1234567890 is_pandigital', 1 )
    expectResult( '123456789 is_pandigital', 1 )
    expectResult( '12345670 is_pandigital', 0 )
    expectResult( '12345 is_pandigital', 1 )
    expectResult( '321 is_pandigital', 1 )

    # is_trimorphic
    testOperator( '1 100 range is_trimorphic' )
    expectEqual( '1 1000 range lambda x is_trimorphic filter', '33819 oeis 26 left 25 right' )

    # multiply_digits
    expectEqual( '123456789 multiply_digits', '9 !' )

    # multiply_digit_powers

    # multiply_nonzero_digits

    # multiply_nonzero_digit_powers

    # n_persistence
    expectResult( '77 1 n_persistence', 4 )
    testOperator( '679 2 n_persistence' )
    testOperator( '6788 3 n_persistence' )
    testOperator( '68889 4 n_persistence' )

    # permute_digits
    testOperator( '12345 permute_digits' )
    expectEqual( '123456789 permute_digits 18 left', '50289 oeis 18 left' )

    # persistence
    expectResult( '77 persistence', 4 )
    expectResult( '679 persistence', 5 )
    expectResult( '6788 persistence', 6 )
    expectResult( '68889 persistence', 7 )
    expectResult( '2677889 persistence', 8 )

    # reversal_addition
    testOperator( '-a20 89 24 reversal_addition' )
    testOperator( '-a20 80 89 range 24 reversal_addition' )
    testOperator( '-a20 89 16 24 range reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition is_palindrome' )
    expectEqual( '-a120 1000004999700144385 259 reversal_addition', '-a120 281301 oeis 260 left' )

    # reverse_digits
    testOperator( '37 1 8 range * reverse_digits' )
    testOperator( '37 1 2 9 range range * reverse_digits' )
    expectEqual( '0 1102 range lambda x sqr reverse_digits x reverse_digits sqr equals filter', '61909 oeis 53 left' )

    # rotate_digits_left

    # rotate_digits_right

    # show_erdos_persistence
    testOperator( '-a30 55555555555555557777777777777 show_erdos_persistence' )

    # show_n_persistence
    testOperator( '-a60 3 2222222223333333778 3 show_n_persistence' )

    # show_persistence
    testOperator( '-a20 2222222223333333778 show_persistence' )

    # sum_digits
    testOperator( '2 32 ** 1 - sum_digits' )
    expectEqual( '0 10000 range sum_digits', '7953 oeis 10001 left' )


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

    # collate
    testOperator( '[ 1 10 range 1 10 range ] collate' )

    # count
    expectResult( '1 10 range count', 10 )

    # cumulative_diffs
    testOperator( '1 10 range cumulative_diffs' )
    testOperator( '1 10 range fib cumulative_diffs' )

    # cumulative_ratios
    testOperator( '1 10 range fib cumulative_ratios' )

    # diffs
    testOperator( '1 10 range diffs' )
    testOperator( '1 10 range fib diffs' )

    # element
    expectResult( '1 10 range 5 element', [ 6 ] )
    testOperator( '-a25 1 100 range fibonacci 55 element' )

    # enumerate
    testOperator( '1 5 range 1 enumerate' )

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
    #expectEqual( '1 10 range 5 group_elements', '[ 1 5 range 6 10 range ]' )
    testOperator( '1 10 range 5 group_elements' )

    # interleave
    testOperator( '1 10 range 1 10 range interleave' )
    expectEqual( '1 100 2 range2 2 100 2 range2 interleave', '1 100 range' )

    # intersection
    expectEqual( '1 10 range 1 8 range intersection', '1 8 range' )

    # interval_range
    expectResult( '1 23 2 interval_range', [ 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23 ] )

    # left
    expectResult( '1 10 range 5 left', [ 1, 2, 3, 4, 5 ] )

    # max_index
    expectResult( '1 10 range max_index', 9 )

    # min_index
    expectResult( '1 10 range min_index', 0 )

    # nonzero
    expectEqual( '1 10 range nonzero', '0 9 range' )

    # occurrence_cumulative
    testOperator( '4 100 random_integer_ occurrence_cumulative' )

    # occurrence_ratios
    testOperator( '4 100 random_integer_ occurrence_ratios' )

    # occurrences
    testOperator( '4 100 random_integer_ occurrences' )

    # range
    expectResult( '1 12 range', [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ] )

    # ratios
    testOperator( '1 10 range fib ratios' )

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

    # sized_range
    expectResult( '10 10 10 sized_range', [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ] )
    testOperator( '10 1 10 range 10 sized_range -s1' )
    testOperator( '1 10 range 1 10 range 10 sized_range -s1' )

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
    expectEqual( '-10 10 range zero', '[ 10 ]' )
    expectEqual( '1 10 range zero', '[ ]' )


# //******************************************************************************
# //
# //  runLogarithmsOperatorTests
# //
# //******************************************************************************

def runLogarithmsOperatorTests( ):
    # lambertw
    testOperator( '5 lambertw' )

    # li
    testOperator( '12 li' )

    # log
    testOperator( '1000 log' )
    expectEqual( '0 lambda 1 x ** 5 x * + log 13 x * / limitn', '5 13 /' )
    expectEqual( '1 10000 range log nearest_int', '193 oeis 10000 left' )
    expectEqual( '1 10000 range log floor', '195 oeis 10000 left' )

    # log10
    expectResult( '1000 log10', 3 )

    # log2
    testOperator( '1000 log2' )

    # logxy
    testOperator( '6561 3 logxy' )

    # polyexp
    testOperator( '4 5 polyexp' )

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
    testOperator( '[ "Philadelphia, PA" "Raleigh, NC" ] today sunrise' )

    # ]
    testOperator( '2 [ 4 5 6 ] eval_poly' )

    # dup_operator
    testOperator( '2 5 dup_operator sqr' )
    testOperator( '4 6 5 dup_operator *' )

    # dup_term
    testOperator( '[ 1 2 10 dup_term ] cf' )

    # previous
    expectResult( '6 previous *', 36 )

    # for_each

    # unlist
    expectResult( '[ 1 2 ] unlist +', 3 )

    # (
    testOperator( '"Leesburg, VA" location today ( sunrise sunset moonrise moonset )' )
    testOperator( '"Leesburg, VA" today ( sunrise sunset moonrise moonset )' )

    # )
    testOperator( '1 10 range ( is_prime is_pronic is_semiprime )' )


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    from rpnNumberTheory import getNthKFibonacciNumberTheSlowWay

    # abundance
    expectEqual( '0 10000 15 interval_range lambda x abundance abs x log not_greater filter', '88012 oeis 2 left' )

    # abundance_ratio
    expectResult( '6 abundance_ratio', 2 )
    expectResult( '28 abundance_ratio', 2 )
    expectResult( '8128 abundance_ratio', 2 )
    expectResult( '120 abundance_ratio', 3 )
    expectResult( '672 abundance_ratio', 3 )

    # aliquot
    testOperator( '276 10 aliquot' )

    # alternating_factorial
    testOperator( '13 alternating_factorial' )
    testOperator( '-a20 1 20 range alternating_factorial' )

    # base
    testOperator( '[ 1 1 1 1 1 1 ] 2 10 range base' )

    testOperator( '-a30 1 10 range 11 base' )
    testOperator( '-a30 1 11 range 12 base' )
    testOperator( '-a30 1 12 range 13 base' )
    testOperator( '-a30 1 13 range 14 base' )
    testOperator( '-a30 1 14 range 15 base' )
    testOperator( '-a30 1 15 range 16 base' )
    testOperator( '-a30 1 16 range 17 base' )
    testOperator( '-a30 1 17 range 18 base' )
    testOperator( '-a30 1 18 range 19 base' )
    testOperator( '-a30 1 19 range 20 base' )

    # barnesg
    testOperator( '2 i barnesg' )
    expectEqual( '-a30 3 12 range barnesg', '-a30 1 10 range superfac' )

    # beta
    testOperator( '5 2 beta' )

    # calkin_wilf
    testOperator( '1 100 range calkin_wilf' )

    # carol
    testOperator( '-a500 773 carol' )
    expectEqual( '1 25 range carol', '93112 oeis 25 left' )

    # cf
    testOperator( '1 10 range cf' )

    # count_divisors
    testOperator( '1024 count_divisors' )
    expectEqual( '1 104 range count_divisors', '5 oeis 104 left' )
    testOperator( '-a50 0 35 range ! count_divisors' )
    testOperator( '27423 oeis 36 left' )
    expectEqual( '-a50 0 35 range ! count_divisors', '-a50 27423 oeis 36 left' )

    # crt
    testOperator( '1 4 range 10 20 3 range2 crt' )

    # digamma
    testOperator( '3 digamma' )
    testOperator( '-1.1 digamma' )
    expectException( '0 digamma' )
    expectException( '-1 digamma' )

    # divisors
    testOperator( '2 3 ** 3 4 ** * divisors' )
    testOperator( '12 ! divisors' )
    testOperator( '-3690 divisors' )

    # double_factorial
    testOperator( '9 double_factorial' )
    expectEqual( '0 2 100 sized_range !!', '165 oeis 100 left' )

    # egypt
    testOperator( '45 67 egypt' )

    # eta
    testOperator( '4 eta' )
    expectEqual( '1 eta', '2 ln' )

    # euler_brick
    testOperator( '2 3 make_pyth_3 unlist euler_brick' )
    expectException( '1 2 3 euler_brick' )

    # euler_phi
    testOperator( '1 20 range euler_phi' )
    expectEqual( '1 1000 range euler_phi', '10 oeis 1000 left' )

    # factor
    testOperator( '-25 factor' )
    testOperator( '-1 factor' )
    testOperator( '0 factor' )
    testOperator( '1 factor' )
    testOperator( '883847311 factor' )
    testOperator( '1 40 range fibonacci factor -s1' )

    # factorial
    testOperator( '-a25 -c 23 factorial' )
    expectEqual( '0 100 range !', '142 oeis 101 left' )
    testOperator( '2.5 factorial' )
    expectException( '-1 factorial' )
    expectEqual( '0 100 range lambda x 2 * ! x 2 * 1 + ! * x ! sqr / eval', '909 oeis 101 left' )
    expectEqual( '1 99 range lambda 3 2 x * ! * x 2 + ! x 1 - ! * / eval', '245 oeis 100 left 99 right' )
    expectEqual( '-a20 1 8 range lambda 0 x range 3 * 1 + factorial 0 x range x + factorial divide prod eval', '36687 oeis 9 left 8 right' )

    # fibonacci
    testOperator( '1 50 range fibonacci' )
    testOperator( '-c -a8300 39399 fibonacci' )
    expectEqual( '0 999 range fibonacci', '45 oeis 1000 left' )
    expectResult( '0 100 range fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )

    # fibonorial
    testOperator( '5 fibonorial' )
    testOperator( '-a50 24 fibonorial' )

    # fraction
    testOperator( '2 sqrt 30 fraction' )
    # NOTE: fraction should be setting dps itself!
    expectEqual( '-p250 2 sqrt 2 199 range fraction flatten lambda x is_even filter_by_index', '1333 oeis 200 left 198 right' )
    expectEqual( '-p250 5 sqrt 2 200 range fraction flatten lambda x is_odd filter_by_index', '1076 oeis 201 left 199 right' )

    # frobenius
    testOperator( '10 20 3 range2 prime frobenius' )
    expectEqual( '2 1001 range lambda x 1 5 sized_range frobenius eval', '138985 oeis 1000 left' )

    # generate_polydivisibles
    testOperator( '3 generate_polydivisibles -r3' )
    expectEqual( '2 8 range lambda x generate_polydivisibles count eval 1 +', '271374 oeis 7 left' )

    # gamma
    testOperator( '3 gamma' )

    # geometric_recurrence
    expectEqual( '-a800 [ 1 1 ] [ 2 2 ] [ 0 1 ] 1 15 range geometric_recurrence', '283 oeis 15 left' )
    expectEqual( '-a800 [ 1 1 ] [ 3 1 ] [ 0 1 ] 1 18 range geometric_recurrence', '280 oeis 18 left' )
    expectEqual( '-a800 [ 1 1 ] [ 2 1 ] [ 0 1 ] 1 25 range geometric_recurrence', '278 oeis 25 left' )
    expectEqual( '-a800 [ 1 1 ] [ 1 3 ] [ 0 1 ] 1 11 range geometric_recurrence', '284 oeis 11 left' )

    # harmonic
    testOperator( '34 harmonic' )
    expectEqual( '1 1000 range lambda x harmonic x harmonic exp x harmonic log * + floor x sigma - eval', '57641 oeis 1000 left' )

    # heptanacci
    testOperator( '-a200 -c 623 heptanacci' )
    expectEqual( '0 49 range heptanacci', '122189 oeis 50 left' )
    expectResult( '0 100 range heptanacci', [ getNthKFibonacciNumberTheSlowWay( i, 7 ) for i in range( 0, 101 ) ] )

    if slow:
        expectEqual( '0 999 range heptanacci', '122189 oeis 1000 left' )
        expectResult( '0 100 range heptanacci', [ getNthKFibonacciNumberTheSlowWay( i, 7 ) for i in range( 0, 101 ) ] )

    # hexanacci
    testOperator( '-a300 -c 949 hexanacci' )
    expectEqual( '0 49 range hexanacci', '1592 oeis 50 left' )
    expectResult( '0 100 range hexanacci', [ getNthKFibonacciNumberTheSlowWay( i, 6 ) for i in range( 0, 101 ) ] )

    if slow:
        expectEqual( '0 3360 range hexanacci', '1592 oeis 3361 left' )
        expectResult( '0 1000 range hexanacci', [ getNthKFibonacciNumberTheSlowWay( i, 6 ) for i in range( 0, 1001 ) ] )

    # hurwitz_zeta
    testOperator( '4 3 hurwitz_zeta' )
    expectEqual( '1 1 100 range range square 1/x sum', '2 zeta 2 2 101 range hurwitz_zeta -' )  # function to compute generalized harmonic numbers

    # hyperfactorial
    testOperator( '-a160 -c 17 hyperfactorial' )

    # is_abundant
    testOperator( '1 20 range is_abundant' )
    expectEqual( '1 4038 range lambda x is_abundant filter', '5101 oeis 1000 left' )

    # is_achilles
    testOperator( '1 20 range is_achilles' )
    expectEqual( '1 1000 range lambda x is_achilles filter', '52486 oeis 13 left' )

    # is_composite
    expectEqual( '1 161 range lambda x is_squarefree x is_composite and filter', '120944 oeis 61 left' )

    # is_deficient
    testOperator( '1 20 range is_deficient' )
    expectEqual( '1 86 range lambda x is_deficient filter', '5100 oeis 66 left' )

    # is_k_hyperperfect
    expectEqual( '1 2100 range lambda x 12 is_k_hyperperfect filter', '[ 697 2041 ]' )

    # is_k_semiprime
    testOperator( '1 20 range 3 is_k_semiprime' )
    expectEqual( '-a30 1 100 range lambda x tribonacci is_semiprime filter', '101757 oeis 12 left' )

    # is_perfect
    testOperator( '1 30 range is_perfect' )

    # is_powerful
    testOperator( '1 20 range is_powerful' )

    # is_prime
    testOperator( '1000 1030 range is_prime' )
    testOperator( '2049 is_prime' )
    testOperator( '92348759911 is_prime' )
    expectEqual( '0 300 range lambda 90 x * 73 + is_prime filter 100 left', '195993 oeis 100 left' )

    # is_polydivisible
    expectEqual( '3608528850368400786036725 is_polydivisible', '1' )

    # is_pronic
    testOperator( '1 20 range is_pronic' )
    expectEqual( '0 9900 range lambda x is_pronic filter', '2378 oeis 100 left' )

    # is_rough
    testOperator( '1 20 range 2 is_rough' )

    # is_semiprime
    testOperator( '12 is_semiprime' )
    expectEqual( '1 205 range lambda x is_semiprime x is_squarefree and filter', '6881 oeis 60 left' )
    expectEqual( ' 1 141 range lambda x is_semiprime x is_squarefree and filter square', '85986 oeis 41 left' )

    # is_smooth
    testOperator( '128 4 is_smooth' )
    testOperator( '1 20 range 2 is_smooth' )

    # is_sphenic
    testOperator( '[ 2 3 5 ] prod is_sphenic' )
    expectEqual( '1 500 range lambda x is_sphenic filter 53 left', '7304 oeis 53 left' )
    expectEqual( '-a30 1 20 range 10 repunit 1 9 range * flatten lambda x is_sphenic filter sort 26 left', '268582 oeis 26 left' )

    # is_squarefree
    testOperator( '2013 sqr is_squarefree' )
    testOperator( '8 primorial is_squarefree' )
    testOperator( '1 20 range is_squarefree' )
    expectEqual( '1 113 range lambda x is_squarefree filter', '5117 oeis 71 left' )
    expectEqual( '1 100 range is_squarefree', '8966 oeis 100 left' )
    expectEqual( '1 515 range lambda x square 1 + is_squarefree not filter', '49532 oeis 54 left' )

    # is_unusual
    testOperator( '-a50 81 23 ** is_unusual' )
    testOperator( '1 20 range is_unusual' )

    # jacobsthal
    expectEqual( '0 99 range jacobsthal', '1045 oeis 100 left' )

    # kynea
    expectEqual( '-a20 1 25 range kynea', '93069 oeis 25 left' )

    # k_fibonacci
    expectResult( '0 100 range 2 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 5 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 10 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 10 ) for i in range( 0, 101 ) ] )
    expectResult( '1000 10 k_fibonacci', getNthKFibonacciNumberTheSlowWay( 1000, 10 ) )

    # leonardo
    expectEqual( '0 99 range leonardo', '1595 oeis 100 left' )

    # leyland
    testOperator( '7 8 leyland' )

    # linear_recurrence
    testOperator( '1 10 range 2 5 range 17 linear_recur' )
    expectEqual( '-a22 [ 1 -1 -2 3 ] [ 1 2 4 8 ] 1 200 range linear_recurrence', '126 oeis 200 left' )
    expectEqual( '-a22 [ -1, 2, 1, -5 4 ] [ 1, 2, 4, 8, 16 ] 1 201 range linear_recurrence', '128 oeis 201 left' )

    # log_gamma
    testOperator( '10 log_gamma' )

    # lucas
    testOperator( '-a21 99 lucas' )
    expectEqual( '0 999 range lucas', '32 oeis 1000 left' )

    # make_cf
    testOperator( 'e 20 make_cf' )
    expectEqual( '-a100 2 pi * 3 2 / power 1/x 1 4 / gamma sqr * 100 make_cf', '53002 oeis 100 left' )

    # make_pyth_3
    testOperator( '12 34 make_pyth_3' )

    # make_pyth_4
    testOperator( '18 29 make_pyth_4' )
    expectException( '17 29 make_pyth_4' )

    # merten
    expectEqual( '1 81 range merten', '2321 oeis 81 left' )

    # mobius
    testOperator( '20176 mobius' )
    expectEqual( '1 100 range mobius', '8683 oeis 100 left' )

    # nth_mersenne
    testOperator( '-a30 1 10 range nth_mersenne' )
    testOperator( '-c 25 nth_mersenne' )

    # nth_thue_morse
    expectEqual( '0 104 range nth_thue_morse', '10060 oeis 105 left' )

    # nth_padovan
    testOperator( '-c 76 nth_padovan' )
    expectEqual( '0 99 range nth_padovan', '931 oeis 104 left 100 right' )

    # octanacci
    testOperator( '-a300 -c 906 octanacci' )
    expectEqual( '0 99 range octanacci', '79262 oeis 100 left' )
    expectResult( '0 100 range octanacci', [ getNthKFibonacciNumberTheSlowWay( i, 8 ) for i in range( 0, 101 ) ] )

    # pascal_triangle
    testOperator( '12 pascal_triangle' )
    testOperator( '1 10 range pascal_triangle -s1' )

    # pentanacci
    testOperator( '16 pentanacci' )
    expectEqual( '0 99 range pentanacci', '1591 oeis 100 left' )
    expectResult( '0 100 range pentanacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )

    # polygamma
    testOperator( '4 5 polygamma' )

    # primorial
    testOperator( '1 10 range primorial' )
    expectEqual( '-a22 0 99 range primorial', '-a22 2110 oeis 100 left' )

    # repunit
    testOperator( '-a20 23 5 repunit' )

    # riesel
    testOperator( '23 riesel' )

    # sigma
    testOperator( '1 20 range sigma' )
    expectEqual( '1 500 range sigma', '203 oeis 500 left' )
    expectEqual( '1 499 range lambda x sigma 8 * 32 x 4 / sigma * 0 x 4 / is_integer if - eval', '118 oeis 500 left 499 right' )

    if slow:
        expectEqual( '1 100000 range sigma', '203 oeis 100000 left' )
        expectEqual( '1 49999 range lambda x sigma 8 * 32 x 4 / sigma * 0 x 4 / is_integer if - eval', '118 oeis 50000 left 49999 right' )

    # sigma_n
    testOperator( '1 20 3 range sigma_n' )
    expectEqual( '1 50 range 2 sigma_n', '1157 oeis 50 left' )
    expectEqual( '-p30 1 100 range 3 sigma_n', '1158 oeis 100 left' )
    expectEqual( '-p30 1 100 range 4 sigma_n', '1159 oeis 100 left' )
    expectEqual( '-p30 1 100 range 5 sigma_n', '1160 oeis 100 left' )
    expectEqual( '-p30 1 100 range 6 sigma_n', '13954 oeis 100 left' )
    expectEqual( '-p30 1 100 range 7 sigma_n', '13955 oeis 100 left' )
    expectEqual( '-p30 1 100 range 8 sigma_n', '13956 oeis 100 left' )
    expectEqual( '-p35 1 100 range 9 sigma_n', '13957 oeis 100 left' )
    expectEqual( '-p35 1 100 range 10 sigma_n', '13958 oeis 100 left' )
    expectEqual( '-p40 1 100 range 11 sigma_n', '13959 oeis 100 left' )
    expectEqual( '-p45 1 100 range 12 sigma_n', '13960 oeis 100 left' )
    expectEqual( '-p45 1 100 range 13 sigma_n', '13961 oeis 100 left' )
    expectEqual( '-p45 1 100 range 14 sigma_n', '13962 oeis 100 left' )
    expectEqual( '-p50 1 100 range 15 sigma_n', '13963 oeis 100 left' )
    expectEqual( '-p55 1 100 range 16 sigma_n', '13964 oeis 100 left' )
    expectEqual( '-p65 1 100 range 17 sigma_n', '13965 oeis 100 left' )
    expectEqual( '-p75 1 100 range 18 sigma_n', '13966 oeis 100 left' )
    expectEqual( '-p80 1 100 range 19 sigma_n', '13967 oeis 100 left' )
    expectEqual( '-p85 1 100 range 20 sigma_n', '13968 oeis 100 left' )
    expectEqual( '-p90 1 100 range 21 sigma_n', '13969 oeis 100 left' )
    expectEqual( '-p95 1 100 range 22 sigma_n', '13970 oeis 100 left' )
    expectEqual( '-p100 1 100 range 23 sigma_n', '13971 oeis 100 left' )
    expectEqual( '-p100 1 100 range 24 sigma_n', '13972 oeis 100 left' )

    if slow:
        expectEqual( '-p30 1 1000 range 3 sigma_n', '1158 oeis 1000 left' )
        expectEqual( '-p30 1 1000 range 4 sigma_n', '1159 oeis 1000 left' )
        expectEqual( '-p35 1 1000 range 5 sigma_n', '1160 oeis 1000 left' )
        expectEqual( '-p35 1 1000 range 6 sigma_n', '13954 oeis 1000 left' )
        expectEqual( '-p45 1 1000 range 7 sigma_n', '13955 oeis 1000 left' )
        expectEqual( '-p50 1 1000 range 8 sigma_n', '13956 oeis 1000 left' )
        expectEqual( '-p55 1 1000 range 9 sigma_n', '13957 oeis 1000 left' )
        expectEqual( '-p60 1 1000 range 10 sigma_n', '13958 oeis 1000 left' )
        expectEqual( '-p65 1 1000 range 11 sigma_n', '13959 oeis 1000 left' )
        expectEqual( '-p70 1 999 range 12 sigma_n', '13960 oeis 999 left' )
        expectEqual( '-p80 1 999 range 13 sigma_n', '13961 oeis 999 left' )
        expectEqual( '-p85 1 999 range 14 sigma_n', '13962 oeis 999 left' )
        expectEqual( '-p90 1 999 range 15 sigma_n', '13963 oeis 999 left' )
        expectEqual( '-p95 1 999 range 16 sigma_n', '13964 oeis 999 left' )
        expectEqual( '-p100 1 999 range 17 sigma_n', '13965 oeis 999 left' )
        expectEqual( '-p200 1 10000 range 18 sigma_n', '13966 oeis 10000 left' )
        expectEqual( '-p210 1 10000 range 19 sigma_n', '13967 oeis 10000 left' )
        expectEqual( '-p220 1 10000 range 20 sigma_n', '13968 oeis 10000 left' )
        expectEqual( '-p230 1 10000 range 21 sigma_n', '13969 oeis 10000 left' )
        expectEqual( '-p240 1 10000 range 22 sigma_n', '13970 oeis 10000 left' )
        expectEqual( '-p250 1 10000 range 23 sigma_n', '13971 oeis 10000 left' )
        expectEqual( '-p260 1 10000 range 24 sigma_n', '13972 oeis 10000 left' )

    # stern
    testOperator( '1 100 range stern' )
    expectEqual( '0 99 range stern', '2487 oeis 100 left' )

    if slow:
        expectEqual( '0 9999 range stern', '2487 oeis 10000 left' )

    # subfactorial
    testOperator( '-a20 -c 19 subfactorial' )
    expectEqual( '1 199 range subfactorial', '166 oeis 200 left 199 right' )

    # sums_of_k_powers
    testOperator( '1072 3 3 sums_of_k_powers' )
    expectEqual( '0 576 range lambda x 2 2 sums_of_k_powers count filter', '1481 oeis 200 left' )
    expectEqual( '0 99 range lambda x 3 2 sums_of_k_powers count eval', '164 oeis 100 left' )
    expectEqual( '0 99 range lambda x 5 2 sums_of_k_powers count eval', '174 oeis 100 left' )
    expectEqual( '0 99 range lambda x 6 2 sums_of_k_powers count eval', '177 oeis 100 left' )

    if slow:
        expectEqual( '0 9999 range lambda x 3 2 sums_of_k_powers count eval', '164 oeis 10000 left' )
        expectEqual( '0 39592 range lambda x 2 2 sums_of_k_powers count filter', '1481 oeis 10000 left' )
        expectEqual( '0 9999 range lambda x 5 2 sums_of_k_powers count eval', '174 oeis 10000 left' )
        expectEqual( '0 9999 range lambda x 6 2 sums_of_k_powers count eval', '177 oeis 10000 left' )

    # sums_of_k_nonzero_powers
    testOperator( '5104 3 3 sums_of_k_nonzero_powers' )
    expectEqual( '1 629 range lambda x 2 2 sums_of_k_nonzero_powers count filter', '404 oeis 200 left' )

    if slow:
        expectEqual( '1 40045 range lambda x 2 2 sums_of_k_nonzero_powers count filter', '404 oeis 10000 left' )

    # superfactorial
    testOperator( '-a50 -c 12 superfactorial' )
    expectEqual( '0 46 range superfactorial', '178 oeis 47 left' )

    # tetranacci
    testOperator( '-a30 -c 87 tetranacci' )
    expectEqual( '0 99 range tetranacci', '78 oeis 100 left' )
    expectResult( '0 100 range tetranacci', [ getNthKFibonacciNumberTheSlowWay( i, 4 ) for i in range( 0, 101 ) ] )

    # thabit
    testOperator( '-a20 -c 45 thabit' )
    expectEqual( '0 998 range thabit', '55010 oeis 1000 left 999 right' )

    # tribonacci
    testOperator( '1 20 range tribonacci' )
    testOperator( '-c -a2800 10239 tribonacci' )
    expectEqual( '0 99 range tribonacci', '73 oeis 100 left' )
    expectResult( '0 100 range tribonacci', [ getNthKFibonacciNumberTheSlowWay( i, 3 ) for i in range( 0, 101 ) ] )

    # trigamma
    testOperator( '3 trigamma' )

    # unit_roots
    testOperator( '7 unit_roots' )

    # zeta
    testOperator( '4 zeta' )

    # zeta_zero
    testOperator( '4 zeta_zero' )


# //******************************************************************************
# //
# //  runPhysicsOperatorTests
# //
# //******************************************************************************

def runPhysicsOperatorTests( ):
    # energy_equivalence
    testOperator( '1 gram energy_equivalence' )

    # escape_velocity
    testOperator( 'earth_mass earth_radius escape_velocity' )

    # kinetic_energy
    testOperator( '310 pounds 65 mph kinetic_energy' )
    testOperator( '65 mph 310 pounds kinetic_energy' )

    # mass_equivalence
    testOperator( '1 joule mass_equivalence' )

    # orbital_period
    testOperator( 'earth_mass earth_radius 640 km + orbital_period' )

    testOperator( 'earth_mass 6872.2568 mph orbital_period' )
    testOperator( '6872.2568 mph earth_mass orbital_period' )
    testOperator( 'earth_mass 26250.087 miles orbital_period' )
    testOperator( '26250.087 miles earth_mass orbital_period' )
    testOperator( '26250.087 miles 6872.2568 mph orbital_period' )
    testOperator( '6872.2568 mph 26250.087 miles orbital_period' )

    expectEqual( 'earth_mass 6872.2568 mph orbital_period', '6872.2568 mph earth_mass orbital_period' )
    expectEqual( 'earth_mass 26250.087 miles orbital_period', '26250.087 miles earth_mass orbital_period' )
    expectEqual( '26250.087 miles 6872.2568 mph orbital_period', '6872.2568 mph 26250.087 miles orbital_period' )

    expectException( '6872.2568 gallons 25620.087 mph orbital_mass' )

    # orbital_mass
    testOperator( '25620.087 miles 24 hours orbital_mass' )
    testOperator( '24 hours 25620.087 miles orbital_mass' )
    testOperator( '25620.087 miles 6872.2568 mph orbital_mass' )
    testOperator( '6872.2568 mph 25620.087 miles orbital_mass' )
    testOperator( '24 hours 6872.2568 mph orbital_mass' )
    testOperator( '6872.2568 mph 24 hours orbital_mass' )

    expectEqual( '25620.087 miles 24 hours orbital_mass', '24 hours 25620.087 miles orbital_mass' )
    expectEqual( '25620.087 miles 6872.2568 mph orbital_mass', '6872.2568 mph 25620.087 miles orbital_mass' )
    expectEqual( '24 hours 6872.2568 mph orbital_mass', '6872.2568 mph 24 hours orbital_mass' )

    expectException( '6872.2568 mph 25620.087 mph orbital_mass' )

    # orbital_radius
    testOperator( '24 hours 6872 mph orbital_radius' )
    testOperator( '6872 mph 24 hours orbital_radius' )
    testOperator( '6872 mph earth_mass orbital_radius' )
    testOperator( 'earth_mass 6872 mph orbital_radius' )
    testOperator( '24 hours earth_mass orbital_radius' )
    testOperator( 'earth_mass 24 hours orbital_radius' )

    expectEqual( '24 hours earth_mass orbital_radius', 'earth_mass 24 hours orbital_radius' )
    expectEqual( '6872 mph earth_mass orbital_radius', 'earth_mass 6872 mph orbital_radius' )
    expectEqual( '24 hours 6872 mph orbital_radius', '6872 mph 24 hours orbital_radius' )

    expectEqual( '24 hours 6872 mph orbital_radius', '6872 mph 24 hours orbital_radius' )

    expectException( '24 hours 6872 miles orbital_radius' )

    # orbital_velocity
    testOperator( 'earth_mass earth_radius 640 km + orbital_velocity' )

    testOperator( 'earth_mass 24 hours orbital_velocity mph convert' )
    testOperator( '24 hours earth_mass orbital_velocity mph convert' )
    testOperator( '26250.08 miles 24 hours orbital_velocity mph convert' )
    testOperator( '24 hours 26250.08 miles orbital_velocity mph convert' )
    testOperator( 'earth_mass 26250.08 miles orbital_velocity mph convert' )
    testOperator( 'earth_mass 26250.08 miles orbital_velocity mph convert' )

    expectEqual( 'earth_mass 24 hours orbital_velocity mph convert', '24 hours earth_mass orbital_velocity mph convert' )
    expectEqual( '26250.08 miles 24 hours orbital_velocity mph convert', '24 hours 26250.08 miles orbital_velocity mph convert' )
    expectEqual( 'earth_mass 26250.08 miles orbital_velocity mph convert', 'earth_mass 26250.08 miles orbital_velocity mph convert' )

    expectException( '24 hours 6872 pounds orbital_mass' )

    # schwarzchild_radius
    testOperator( 'earth_mass schwarzchild_radius' )

    # surface_gravity

    # mass length
    testOperator( 'earth_mass earth_radius surface_gravity' )
    testOperator( 'earth_radius earth_mass surface_gravity' )

    # volume density
    testOperator( 'earth_volume earth_density surface_gravity' )
    testOperator( 'earth_density earth_volume surface_gravity' )

    # mass density
    testOperator( 'earth_density earth_mass surface_gravity' )
    testOperator( 'earth_mass earth_density surface_gravity' )

    # mass volume
    testOperator( 'earth_volume earth_mass surface_gravity' )
    testOperator( 'earth_mass earth_volume surface_gravity' )

    # density length
    testOperator( 'earth_density earth_radius surface_gravity' )
    testOperator( 'earth_radius earth_density surface_gravity' )

    expectException( 'earth_radius earth_volume surface_gravity' )
    expectException( 'earth_mass sun_mass surface_gravity' )

    # time_dilation
    testOperator( '1 million miles hour / time_dilation' )


# //******************************************************************************
# //
# //  runFigurateNumberOperatorTests
# //
# //******************************************************************************

def runFigurateNumberOperatorTests( ):
    # centered_cube
    testOperator( '1 20 range centered_cube' )
    testOperator( '100 centered_cube' )
    expectEqual( '1 38 range centered_cube', '5898 oeis 38 left' )

    # centered_decagonal
    testOperator( '17 centered_decagonal' )

    # centered_dodecahedral
    testOperator( '1 20 range centered_dodecahedral' )
    testOperator( '60 centered_dodecahedral' )
    expectEqual( '1 36 range centered_dodecahedral', '5904 oeis 36 left' )

    # centered_heptagonal
    testOperator( '102 centered_heptagonal' )

    # centered_hexagonal
    testOperator( '103 centered_hexagonal' )

    # centered_icosahedral
    testOperator( '1 20 range centered_icosahedral' )
    testOperator( '30 centered_icosahedral' )
    expectEqual( '1 36 range centered_icosahedral', '5902 oeis 36 left' )

    # centered_nonagonal
    testOperator( '104 centered_nonagonal' )

    # centered_octagonal
    testOperator( '10 centered_octagonal' )

    # centered_octahedral
    testOperator( '1 20 range centered_octahedral' )
    testOperator( '70 centered_octahedral' )
    expectEqual( '1 40 range centered_octahedral', '1845 oeis 40 left' )

    # centered_pentagonal
    testOperator( '108 centered_pentagonal' )

    # centered_polygonal
    testOperator( '108 5 centered_polygonal' )

    # centered_square
    testOperator( '5 centered_square' )

    # centered_tetrahedral
    testOperator( '1 20 range centered_tetrahedral' )
    testOperator( '120 centered_tetrahedral' )
    expectEqual( '1 39 range centered_tetrahedral', '5894 oeis 39 left' )

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
    testOperator( '-a75 9 decagonal_nonagonal' )

    # decagonal_octagonal
    testOperator( '-a75 9 decagonal_octagonal' )

    # decagonal_pentagonal
    testOperator( '-a60 7 decagonal_pentagonal' )

    # decagonal_centered_square
    testOperator( '-a40 9 decagonal_centered_square' )

    # decagonal_triangular
    testOperator( '-a40 13 decagonal_triangular' )

    # dodecahedral
    testOperator( '44 dodecahedral' )

    # generalized_pentagonal
    testOperator( '187 generalized_pentagonal' )

    # heptagonal
    testOperator( '203 heptagonal' )
    expectEqual( '0 1000 range heptagonal', '566 oeis 1001 left' )

    # heptagonal_hexagonal
    testOperator( '2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal
    testOperator( '8684 heptagonal_pentagonal' )

    # heptagonal_square
    testOperator( '222 heptagonal_square' )

    # heptagonal_triangular
    testOperator( '-a1000 -c 399 heptagonal_triangular' )
    expectEqual( '-a40 1 14 range heptagonal_triangular', '-a40 46194 oeis 14 left' )

    # hexagonal
    testOperator( '340 hexagonal' )
    expectEqual( '0 1000 range hexagonal', '384 oeis 1001 left' )

    # hexagonal_pentagonal
    testOperator( '-a250 -c 107 hexagonal_pentagonal' )
    expectEqual( '-a40 1 14 range hexagonal_pentagonal', '-a40 46178 oeis 14 left' )

    # hexagonal_square
    testOperator( '-a70 -c 23 hexagonal_square' )
    expectEqual( '-a70 1 12 range hexagonal_square', '-a40 46177 oeis 12 left' )

    # icosahedral
    testOperator( '100 icosahedral' )

    # nonagonal
    testOperator( '554 nonagonal' )

    # nonagonal_heptagonal
    testOperator( '-a50 -c 12 nonagonal_heptagonal' )

    # nonagonal_hexagonal
    testOperator( '-a60 -c 13 nonagonal_hexagonal' )

    # nonagonal_octagonal
    testOperator( '-a75 -c 14 nonagonal_octagonal' )

    # nonagonal_pentagonal
    testOperator( '-a60 -c 15 nonagonal_pentagonal' )

    # nonagonal_square
    testOperator( '-a22 -c 16 nonagonal_square' )

    # nonagonal_triangular
    testOperator( '-a21 -c 17 nonagonal_triangular' )

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

    # octagonal
    testOperator( '102 octagonal' )
    expectEqual( '0 1000 range octagonal', '567 oeis 1001 left' )

    # octahedral
    testOperator( '23 octahedral' )

    # octagonal_heptagonal
    testOperator( '-a40 -c 8 octagonal_heptagonal' )

    # octagonal_hexagonal
    testOperator( '-a30 -c 7 octagonal_hexagonal' )

    # octagonal_pentagonal
    testOperator( '-a15 -c 6 octagonal_pentagonal' )

    # octagonal_square
    testOperator( '-a25 -c 11 octagonal_square' )

    # octagonal_triangular
    testOperator( '-a20 -c 10 octagonal_triangular' )

    # pentagonal
    testOperator( '16 pentagonal' )
    expectEqual( '0 1000 range pentagonal', '326 oeis 1001 left' )

    # pentagonal_square
    testOperator( '-a70 -c 10 pentagonal_square' )

    # pentagonal_triangular
    testOperator( '-a40 -c 17 pentagonal_triangular' )

    # pentatope
    testOperator( '12 pentatope' )

    # polygonal
    testOperator( '9 12 polygonal' )

    # polytope
    testOperator( '1 10 range 7 polytope' )
    testOperator( '10 2 8 range polytope' )
    testOperator( '1 10 range 2 8 range polytope' )
    testOperator( '-a20 -c 18 47 polytope' )

    # pyramid
    testOperator( '304 pyramid' )
    expectEqual( '0 1000 range pyramid', '330 oeis 1001 left' )

    # rhombdodec
    testOperator( '89 rhombdodec' )

    # square_triangular
    testOperator( '-a60 -c 34 square_triangular' )

    # star
    expectEqual( '1 43 range star', '3154 oeis 43 left' )

    # stella_octangula
    testOperator( '3945 stella_octangula' )

    # tetrahedral
    testOperator( '-a20 19978 tetrahedral' )

    # triangular
    testOperator( '203 triangular' )
    expectEqual( '1 102 range triangular lambda x count_different_digits 3 equals filter', '162304 oeis 47 left' )
    expectEqual( '0 29999 range triangular', '217 oeis 30000 left' )

    # truncated_octahedral
    testOperator( '394 truncated_octahedral' )

    # truncated_tetrahedral
    testOperator( '683 truncated_tetrahedral' )


# //******************************************************************************
# //
# //  runPowersAndRootsOperatorTests
# //
# //******************************************************************************

def runPowersAndRootsOperatorTests( ):
    # agm
    testOperator( '1 2 sqrt agm' )

    # cube
    testOperator( '3 cube' )
    expectEqual( '0 10000 range cube', '578 oeis 10001 left' )

    # cube_root
    testOperator( 'pi cube_root' )
    expectEqual( '17 cube_root 0 199 range ** nint', '18025 oeis 200 left' )
    expectEqual( '11 cube_root 0 199 range ** nint', '18007 oeis 200 left' )

    # exp
    testOperator( '13 exp' )
    expectEqual( '2 2001 range lambda euler_constant exp x log log x * * floor x sigma - eval', '58209 oeis 2000 left' )
    expectEqual( '1 999 range lambda x x sin exp * ceiling eval', '134892 oeis 999 left' )

    # exp10
    testOperator( '12 exp10' )

    # expphi
    testOperator( '100 expphi' )

    # hyper4_2
    testOperator( '-a160 -c 4 3 hyper4_2' )

    # power
    testOperator( '4 5 power' )
    testOperator( '4 1 i power' )
    testOperator( '1 10 range 2 10 range power' )
    expectEqual( '3 0 199 range power', '244 oeis 200 left' )
    expectEqual( '1 100 range lambda 1 x range 4 ** sum eval', '538 oeis 101 left 100 right' )
    expectEqual( '1 100 range lambda 1 x range 5 ** sum eval', '539 oeis 101 left 100 right' )
    expectEqual( '1 100 range lambda 1 x range 6 ** sum eval', '540 oeis 101 left 100 right' )
    expectEqual( '1 100 range lambda 1 x range 7 ** sum eval', '541 oeis 101 left 100 right' )
    expectEqual( '1 100 range lambda 1 x range 8 ** sum eval', '542 oeis 101 left 100 right' )

    if slow:
        expectEqual( '1 1000 range lambda 1 x range 4 ** sum eval', '538 oeis 1001 left 1000 right' )
        expectEqual( '1 1000 range lambda 1 x range 5 ** sum eval', '539 oeis 1001 left 1000 right' )
        expectEqual( '1 1000 range lambda 1 x range 6 ** sum eval', '540 oeis 1001 left 1000 right' )
        expectEqual( '1 1000 range lambda 1 x range 7 ** sum eval', '541 oeis 1001 left 1000 right' )
        expectEqual( '1 1000 range lambda 1 x range 8 ** sum eval', '542 oeis 1001 left 1000 right' )

    # powmod
    testOperator( '43 67 9 powmod' )

    # root
    expectEqual( '8 3 root', '8 cube_root' )

    # square
    expectEqual( '123 square', '123 123 *' )

    # square_root
    expectEqual( '2 square_root', '4 4 root' )
    expectEqual( '1 10000 range prime sqrt floor', '6 oeis 10000 left' )

    # tetrate
    testOperator( '3 2 tetrate' )

    # tower
    testOperator( '-c -a30 [ 2 3 2 ] tower' )

    # tower2
    testOperator( '-a160 -c [ 4 4 4 ] tower2' )


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
    # cousin primes are currently wrong starting with #99
    #expectEqual( '1 100 range lambda x cousin_prime_ product eval', '143206 oeis 100 left' )
    #expectEqual( '1001 1100 range lambda x cousin_prime_ product eval', '143206 oeis 1100 left 100 right' )
    #expectEqual( '9901 10000 range lambda x cousin_prime_ product eval', '143206 oeis 10000 left 100 right' )

    if slow:
        expectEqual( '1 10000 range lambda x cousin_prime_ product eval', '143206 oeis 10000 left' )

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

    # next_primes
    testOperator( '35 100 next_primes' )
    testOperator( '8783 50 next_primes' )
    testOperator( '142857 10 next_primes' )
    testOperator( '-c 6 13 ** 1 + 10 next_primes' )
    testOperator( '-c 7 13 ** 1 + 10 next_primes' )
    testOperator( '-a20 253931039382790 18 next_primes -s1' )

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

    # nth_quintuplet_prime
    testOperator( '1 100000 10000 range2 nth_quintuplet_prime' )
    testOperator( '23887 nth_quintuplet_prime' )
    testOperator( '13,000,000,000 nth_quintuplet_prime' )

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

    # prime_pi
    testOperator( '87 prime_pi' )
    expectEqual( '1 999 range lambda x x prime_pi combinations eval', '37031 oeis 999 left' )

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
    expectEqual( '1 10000 primes sqrt floor', '6 oeis 10000 left' )
    expectEqual( '1 10000 primes', '40 oeis 10000 left' )

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
    expectEqual( '1 100 range sexy_prime', '23201 oeis 100 left' )
    expectEqual( '901 1000 range sexy_prime', '23201 oeis 1000 left 100 right' )
    expectEqual( '4901 5000 range sexy_prime', '23201 oeis 5000 left 100 right' )
    expectEqual( '9901 10000 range sexy_prime', '23201 oeis 10000 left 100 right' )

    if slow:
        expectEqual( '1 10000 range sexy_prime', '23201 oeis 10000 left' )

    # sexy_prime_
    testOperator( '1 10 range sexy_prime_' )
    testOperator( '29 sexy_prime_' )
    testOperator( '21985 sexy_prime_' )
    testOperator( '-c 100,000,000 sexy_prime_' )
    expectEqual( '1 100 range lambda x sexy_prime_ product eval', '111192 oeis 100 left' )
    expectEqual( '1001 1100 range lambda x sexy_prime_ product eval', '111192 oeis 1100 left 100 right' )
    expectEqual( '9901 10000 range lambda x sexy_prime_ product eval', '111192 oeis 10000 left 100 right' )

    if slow:
        expectEqual( '1 10000 range lambda x sexy_prime_ product eval', '111192 oeis 10000 left' )

    # sexy_quadruplet
    testOperator( '1 10 range sexy_quadruplet' )
    testOperator( '29 sexy_quadruplet' )
    testOperator( '-c 289747 sexy_quadruplet' )
    #expectEqual( '1 39 range lambda x sexy_quadruplet_ 3 element eval flatten', '46124 oeis 39 left' )

    # sexy_quadruplet_
    testOperator( '1 10 range sexy_quadruplet_' )
    testOperator( '29 sexy_quadruplet_' )
    testOperator( '2459 sexy_quadruplet_' )

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

    # sophie_prime
    testOperator( '1 10 range sophie_prime' )
    testOperator( '87 sophie_prime' )
    testOperator( '6,500,000 sophie_prime' )
    expectEqual( '1 100 range sophie_prime', '5384 oeis 100 left' )
    expectEqual( '9900 10000 range sophie_prime', '5384 oeis 10000 left 101 right' )
    expectEqual( '99900 100000 range sophie_prime', '5384 oeis 100000 left 101 right' )

    if slow:
        expectEqual( '1 100000 range sophie_prime', '5384 oeis 100000 left' )

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
    expectEqual( '1 51 range lambda x twin_prime 1 + x twin_prime 1 + factors count - eval', '176915 oeis 51 left' )
    expectEqual( '1 100 range twin_prime', '1359 oeis 100 left' )
    expectEqual( '1001 1100 range twin_prime', '1359 oeis 1100 left 100 right' )
    expectEqual( '5001 5100 range twin_prime', '1359 oeis 5100 left 100 right' )
    expectEqual( '20001 20100 range twin_prime', '1359 oeis 20100 left 100 right' )
    expectEqual( '60001 60100 range twin_prime', '1359 oeis 60100 left 100 right' )
    expectEqual( '99901 100000 range twin_prime', '1359 oeis 100000 left 100 right' )

    if slow:
        expectEqual( '1 100000 range twin_prime', '1359 oeis 100000 left' )

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
    # constant

    # echo
    #testOperator( '1 10 range echo sqrt collate -s1' )

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
    testOperator( '150 gee * estimate' )
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
    testOperator( '280000 randint oeis' )

    # oeis_comment
    testOperator( '1000 oeis_comment' )
    testOperator( '280000 randint oeis_comment' )

    # oeis_ex
    testOperator( '1000 oeis_ex' )
    testOperator( '280000 randint oeis_ex' )

    # oeis_name
    testOperator( '1000 oeis_name' )
    testOperator( '280000 randint oeis_name' )

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

    # permute_dice
    testOperator( '3d6 permute_dice' )
    testOperator( '4d6x1 permute_dice occurrences -s1' )
    testOperator( '2d4+1 permute_dice occurrences -s1' )

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
    # testOperator( 'result' )

    # roll_dice
    testOperator( '20d6 roll_dice' )
    testOperator( '3d8+5 roll_dice' )
    testOperator( '10d12x2-4 roll_dice' )

    # roll_dice_
    testOperator( '3d6 6 roll_dice_' )
    testOperator( '4d6x1 6 roll_dice_' )

    # set - interactive mode

    # topic - interactive mode

    # value
    expectResult( '40 minutes value', 40 )
    expectResult( '756 light-years value', 756 )
    expectResult( '73 gallons value', 73 )


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
    expectEqual( '45 degrees cos', '2 sqrt 1/x' )
    testOperator( 'pi radians cos' )
    expectEqual( '0 lambda 1 x cos - x sqr / limitn', '0.5' )

    # cosh
    testOperator( 'pi 3 / cosh' )
    expectEqual( '0 250 range cosh floor', '501 oeis 251 left' )

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
    expectEqual( 'pi 4 / sin', '2 sqrt 1/x' )
    expectEqual( '0 lambda 2 x * sin 3 x * sin / limitn', '2 3 /' )

    # sinh
    testOperator( 'pi 2 / sinh' )
    expectEqual( '0 250 range sinh nearest_int', '495 oeis 251 left' )
    expectEqual( '0 200 range sinh floor', '471 oeis 201 left' )

    # tan
    testOperator( 'pi 3 / tan' )
    expectEqual( '0 999 range tan nearest_int', '209 oeis 1000 left' )
    expectEqual( '0 1000 range tan floor', '503 oeis 1001 left' )

    # tanh
    testOperator( 'pi 4 / tanh' )


# //******************************************************************************
# //
# //  runAdvancedTests
# //
# //  This is just for tests that are more complex than the single operator
# //  tests... and any random tests that don't fit in anywhere else.
# //
# //******************************************************************************

def runAdvancedTests( ):
    expectResult( '-0', 0 )
    testOperator( '2016 dst_end 2016 dst_start - 2016-12-31 2016-01-01 - /' )
    #testOperator( '"Leesburg, VA" today 0 20 range days + echo daytime collate -s1' )
    testOperator( '1 1 thousand range lambda x is_polydivisible filter' )
    expectEqual( '38[147][246]5[246][124679][246][124679]0 build_numbers lambda x is_polydivisible filter lambda x is_pandigital filter', '[ 3816547290 ]' )
    testOperator( '1 50 range twin_primes_ 1/x sum sum' )


# //******************************************************************************
# //
# //  tests
# //
# //******************************************************************************

rpnTestList = [
    ( 'algebra',            runAlgebraOperatorTests ),
    ( 'arithmetic',         runArithmeticOperatorTests ),
    ( 'astronomy',          runAstronomyOperatorTests ),
    ( 'bitwise',            runBitwiseOperatorTests ),
    ( 'calendar',           runCalendarOperatorTests ),
    ( 'chemistry',          runChemistryOperatorTests ),
    ( 'combinatorics',      runCombinatoricsOperatorTests ),
    ( 'complex',            runComplexMathOperatorTests ),
    ( 'constant',           runConstantOperatorTests ),
    ( 'conversion',         runConversionOperatorTests ),
    ( 'date_time',          runDateTimeOperatorTests ),
    ( 'figurate',           runFigurateNumberOperatorTests ),
    ( 'function',           runFunctionOperatorTests ),
    ( 'geography',          runGeographyOperatorTests ),
    ( 'geometry',           runGeometryOperatorTests ),
    ( 'lexicography',       runLexicographyOperatorTests ),
    ( 'list',               runListOperatorTests ),
    ( 'logarithms',         runLogarithmsOperatorTests ),
    ( 'modifier',           runModifierOperatorTests ),
    ( 'number_theory',      runNumberTheoryOperatorTests ),
    ( 'physics',            runPhysicsOperatorTests ),
    ( 'powers_and_roots',   runPowersAndRootsOperatorTests ),
    ( 'prime_number',       runPrimeNumberOperatorTests ),
    ( 'settings',           runSettingsOperatorTests ),
    ( 'special',            runSpecialOperatorTests ),
    ( 'trigonometry',       runTrigonometryOperatorTests ),

    ( 'advanced',           runAdvancedTests ),

    ( 'command-line',       runCommandLineOptionsTests ),
    ( 'unit_conversion',    runConvertTests ),
    ( 'help',               runHelpTests ),

    ( 'internal',           runInternalOperatorTests )
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
    if tests:
        for test in tests:
            if test in rpnTests:
                rpnTests[ test ]( )
            else:
                guess = difflib.get_close_matches( test, rpnTests, 1 )

                if ( len( guess ) == 1 ):
                    print( 'Interpreting \'' + test + '\' as \'' + guess[ 0 ] + '\'...' )
                    print( )
                    rpnTests[ guess[ 0 ] ]( )
                else:
                    print( 'I don\'t know what \'' + test + '\' means in this context.' )
    else:
        for test in rpnTests:
            rpnTests[ test ]( )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    getDataPath( )
    loadHelpData( )
    loadUnitNameData( )

    for alias in operatorAliases:
        if operatorAliases[ alias ] in operators:
            continue

        if operatorAliases[ alias ] in listOperators:
            continue

        if operatorAliases[ alias ] in modifiers:
            continue

        if operatorAliases[ alias ] in constants:
            continue

        if operatorAliases[ alias ] in g.unitOperatorNames:
            continue

        if operatorAliases[ alias ] in g.operatorCategories:
            continue

        if operatorAliases[ alias ] == 'unit_types':
            continue

        print( 'alias \'' + alias + '\' resolves to invalid name \'' + operatorAliases[ alias ] + '\'' )
        exit( )

    runTests( sys.argv[ 1 : ] )

# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

