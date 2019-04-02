#!/usr/bin/env python

# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import os
import sys
import time

from collections import OrderedDict
from pathlib import Path

from rpn.rpnOperators import *

from rpn.rpnAliases import operatorAliases
from rpn.rpnOperators import constants, listOperators, operators
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnPersistence import loadUnitNameData
from rpn.rpnPrimeUtils import checkForPrimeData
from rpn.rpnTestUtils import *
from rpn.rpnUtils import getDataPath, loadAstronomyData
from rpn.rpnVersion import PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE
from rpn.testConvert import *
from rpn.testHelp import *

from mpmath import *

import rpn.rpnGlobals as g

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

    expectException( '9999 -b8' )   # invalid base 8 number
    expectException( '123g -b16' )  # invalid base 16 number

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

    expectException( '1 100 range -r1' )        # invalid output base
    expectException( '1 100 range -r63' )       # invalid output base
    expectException( '1 100 range -rsqrt3' )    # invalid output base

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
    testOperator( '[ 2 4 6 8 10 ] [ 3 5 7 ] add_polynomials' )
    testOperator( '1 13 3 range2 [ 3 5 7 ] add_polynomials' )
    testOperator( '[ 3 5 7 ] 1 5 range add_polynomials' )
    testOperator( '1 8 range 8 1 range add_polynomials' )
    #testOperator( '[ [ 1 2 3 ] [ 2 2 3 ] ] [ 8 7 6 ] add_polynomials' )

    expectEqual( '[ 10 56 10 ] [ 78 -45 20 ] add_polynomials', '[ 10 56 10 ] [ 78 -45 20 ] add' )
    expectEqual( '1 1000 range 1001 2000 range add_polynomials', '1 1000 range 1001 2000 range add' )
    expectEqual( '1 10 range 1 10 range add_polynomials', '2 20 2 range2' )

    expectException( '1 10 range add_polynomials' )   # too few arguments

    # eval_polynomial
    testOperator( '1 10 range 6 eval_polynomial' )
    testOperator( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_polynomial' )

    expectException( '1 eval_polynomial' )            # too few arguments
    expectException( '1 10 range eval_polynomial' )   # too few arguments

    # find_polynomial
    expectEqual( 'phi 3 find_polynomial', '[ -1 1 1 ]' )

    expectException( '1 find_polynomial' )            # too few arguments

    # multiply_polynomials
    testOperator( '1 10 range 1 10 range multiply_polynomials' )

    expectException( '1 10 range multiply_polynomials' )   # too few arguments

    # polynomial_power
    testOperator( '[ 1 2 3 4 ] 5 polynomial_power' )
    testOperator( '[ 1 1 1 ] 1 10 range polynomial_power -s1' )

    expectEqual( '[ 1 1 ] 5 polynomial_power', '6 pascal_triangle' )
    expectEqual( '[ 1 1 ] 15 polynomial_power', '16 pascal_triangle' )
    expectEqual( '-a50 [ 1 1 ] 150 polynomial_power', '-a50 151 pascal_triangle' )
    expectEqual( '-a150 [ 1 1 ] 500 polynomial_power', '-a150 501 pascal_triangle' )

    expectException( '1 10 range polynomial_power' )    # too few arguments

    # polynomial_product
    testOperator( '[ 1 10 range 1 10 range 2 11 range ] polynomial_product' )
    testOperator( '[ [ 1 10 range 1 10 range 2 11 range ] [ 1 5 range 2 6 range ] ] polynomial_product' )

    expectEqual( '[ [ 1 1 ] [ 1 1 ] [ 1 1 ] [ 1 1 ] [ 1 1 ] ] polynomial_product', '6 pascal_triangle' )

    # polynomial_sum
    testOperator( '[ 1 10 range 2 11 range ] polynomial_sum' )
    testOperator( '[ [ 1 10 range 1 10 range 2 11 range ] [ 1 5 range 2 6 range ] ] polynomial_sum' )

    # solve
    testOperator( '1 8 range solve' )

    expectException( '0 solve' )            # order too low
    expectException( '1 solve' )            # order too low
    expectException( '[ 0 1 ] solve' )      # order too low
    expectException( '[ 0 0 1 ] solve' )    # order too low
    expectException( '[ 0 0 0 ] solve' )    # order too low

    # solve_cubic
    expectEquivalent( '1 0 0 0 solve_cubic', '[ 1 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 0 solve_cubic', '[ 0 1 0 0 ] solve' )
    expectEquivalent( '1 1 0 0 solve_cubic', '[ 1 1 0 0 ] solve' )
    expectEquivalent( '0 0 1 0 solve_cubic', '[ 0 0 1 0 ] solve' )
    expectEquivalent( '1 0 -3 0 solve_cubic', '[ 1 0 -3 0 ] solve' )
    expectEquivalent( '10 -10 10 -10 solve_cubic', '[ 10 -10 10 -10 ] solve' )
    expectEquivalent( '57 -43 15 28 solve_cubic', '[ 57 -43 15 28 ] solve' )

    expectException( '0 0 0 0 solve_cubic' )   # order too low
    expectException( '0 0 0 1 solve_cubic' )   # order too low

    # solve_quadratic
    expectEquivalent( '1 0 0 solve_quadratic', '[ 1 0 0 ] solve' )
    expectEquivalent( '1 1 0 solve_quadratic', '[ 1 1 0 ] solve' )
    expectEquivalent( '1 0 1 solve_quadratic', '[ 1 0 1 ] solve' )
    expectEquivalent( '0 1 0 solve_quadratic', '[ 0 1 0 ] solve' )
    expectEquivalent( '1 -1 1 solve_quadratic', '[ 1 -1 1 ] solve' )
    expectEquivalent( '8 9 10 solve_quadratic', '[ 8 9 10 ] solve' )
    expectEquivalent( '-36 150 93 solve_quadratic', '[ -36 150 93 ] solve' )

    expectException( '0 0 0 solve_quadratic' )   # order too low
    expectException( '0 0 1 solve_quadratic' )   # order too low

    # solve_quartic
    expectEquivalent( '1 0 0 0 0 solve_quartic', '[ 1 0 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 0 0 solve_quartic', '[ 0 1 0 0 0 ] solve' )
    expectEquivalent( '0 1 0 1 0 solve_quartic', '[ 0 1 0 1 0 ] solve' )
    expectEquivalent( '0 0 1 0 0 solve_quartic', '[ 0 0 1 0 0 ] solve' )
    expectEquivalent( '0 0 0 1 0 solve_quartic', '[ 0 0 0 1 0 ] solve' )
    expectEquivalent( '1 0 -5 0 7 solve_quartic', '[ 1 0 -5 0 7 ] solve' )
    expectEquivalent( '2 -3 2 -3 2 solve_quartic', '[ 2 -3 2 -3 2 ] solve' )
    expectEquivalent( '54 23 -87 19 2042 solve_quartic', '[ 54 23 -87 19 2042 ] solve' )

    expectException( '0 0 0 0 0 solve_quartic' )   # order too low
    expectException( '0 0 0 0 1 solve_quartic' )   # order too low


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
    expectResult( '2 i abs', 2 )
    expectResult( '-7 i abs', 7 )
    expectResult( '3 i 4 + abs', 5 )
    expectResult( '-3 i 4 + abs', 5 )

    # add
    testOperator( 'today 7 days +' )
    testOperator( 'today 3 weeks +' )
    testOperator( 'today 50 years +' )
    testOperator( '4 cups 13 teaspoons +' )
    testOperator( '55 mph 10 meters second / +' )
    testOperator( '55 mph 10 furlongs fortnight / +' )
    testOperator( 'today 3 days add' )
    testOperator( 'today 3 weeks add' )
    testOperator( 'now 150 miles 10 furlongs fortnight / / add' )

    expectResult( '55 mph 10 miles hour / +', RPNMeasurement( 65, 'mile/hour' ) )
    expectResult( '4 3 add', 7 )
    expectResult( '3 feet 7 inches + inches convert', RPNMeasurement( 43, 'inch' ) )

    expectException( '2 cups 3 weeks +' )   # incompatible measurements

    # ceiling
    expectResult( '9.99999 ceiling', 10 )
    expectResult( '-0.00001 ceiling', 0 )
    expectResult( '9.5 cups ceiling', RPNMeasurement( 10, 'cups' ) )

    expectEqual( '1 56 range lambda x x log * ceiling eval', '50502 oeis 56 left' )

    # decrement
    expectResult( '2 decrement', 1 )
    expectResult( '3 miles decrement', RPNMeasurement( 2, 'miles' ) )

    #expectEqual( 'infinity decrement', 'infinity' )        # The test can't compare infinity.
    #expectEqual( 'negative_infinity decrement', 'negative_infinity' )

    expectEqual( '2 i decrement', '2 i 1 -' )

    # divide
    testOperator( '12 13 divide' )
    testOperator( '10 days 7 / dhms' )
    testOperator( 'marathon 100 miles hour / / minutes convert' )
    testOperator( '2 zeta sqrt 24 sqrt / 12 *' )
    testOperator( 'now 2014-01-01 - minutes /' )

    expectResult( '4 cups 2 cups /', 2 )

    expectException( '1 0 divide' )     # division by zero

    # equals_one_of
    if g.primeDataAvailable:
        expectEqual( '1 33100 primes lambda x 40 mod [ 7 19 23 ] equals_one_of x 1 - 2 / is_prime and filter', '353 oeis 1000 left' )

    # floor
    expectResult( '-0.4 floor', -1 )
    expectResult( '1 floor', 1 )
    expectResult( '3.4 floor', 3 )
    expectResult( '3.14 miles floor', RPNMeasurement( 3, 'miles' ) )

    expectEqual( '10.3 cups floor', '10 cups' )
    expectEqual( '88 mph 10 round_by_value', '90 mph' )
    expectEqual( '4.5 i 8.6 + floor', '4 i 8 +' )
    expectEqual( '1 52 range lambda 2 log 1 1 x x 2 + * / + log / floor eval', '84587 oeis 52 left' )
    expectEqual( '1 1000 range ! log 7 log / floor', '127033 oeis 1000 left' )
    expectEqual( '1 1000 range lambda x 5 * x 5 * log + ceiling eval', '212454 oeis 1000 left' )
    expectEqual( '1 1000 range e 1 - * floor', '210 oeis 1000 left' )
    expectEqual( '-a2003 2 0 4999 range 2 / floor **', '16116 oeis 5000 left' )

    # gcd
    testOperator( '1 2 10 range range gcd' )

    expectResult( '1 100 range gcd', 1 )
    expectResult( '[ 124 324 ] gcd', 4 )
    expectResult( '[ 8 64 ] gcd', 8 )
    expectResult( '[ 6 10 15 ] gcd', 1 )
    expectResult( '[ 14 22 77 ] gcd', 1 )

    # gcd2
    testOperator( '123 78 gcd2' )

    expectEqual( '-a4200 0 20000 range lambda x x fib gcd2 eval', '104714 oeis 20001 left' )
    expectEqual( '-a500 1 1000 range lambda 2 x ** 1 - 3 x ** 1 - gcd2 eval', '86892 oeis 1000 left' )

    # harmonic_mean
    testOperator( '1 5 range harmonic_mean' )

    expectEqual( '1 1000 range lambda x divisors harmonic_mean -10 round_by_digits is_integer filter', '1599 oeis lambda x 1000 is_not_greater filter' )

    if slow:
        expectEqual( '1 100000 range lambda x divisors harmonic_mean -10 round_by_digits is_integer filter', '1599 oeis lambda x 100000 is_not_greater filter' )

    # increment
    expectResult( '2 increment', 3 )
    expectResult( '-1 increment', 0 )
    expectResult( '0.5 increment', 1.5 )
    expectResult( '3 miles increment', RPNMeasurement( 4, 'miles' ) )

    #expectEqual( 'infinity increment', 'infinity' )        # The test can't compare infinity.
    #expectEqual( 'negative_infinity increment', 'negative_infinity' )
    expectEqual( '2 i increment', '2 i 1 +' )

    # is_divisible
    expectResult( '1000 10000 is_divisible', 0 )
    expectResult( '10000 1000 is_divisible', 1 )
    expectResult( '12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )

    expectEqual( '0 2810 range lambda x 2 has_digits x 2 is_divisible or filter', '92451 oeis 2001 left' )
    expectEqual( '0 2944 range lambda x 9 has_digits x 9 is_divisible or filter', '92457 oeis 1001 left' )
    expectEqual( '2 14349 range lambda x 1 + x sum_digits x 2 + sum_digits + is_divisible filter', '127271 oeis 1000 left' )

    expectException( '1 0 is_divisible' )       # division by zero
    expectException( '20 i 4 is_divisible' )    # real arguments required
    expectException( '20 4 i is_divisible' )    # real arguments required

    # is_equal
    expectResult( '4 3 is_equal', 0 )
    expectResult( 'pi pi is_equal', 1 )
    expectResult( '2 cups 3 cups is_equal', 0 )
    expectResult( '2 cups 1 pint is_equal', 1 )
    expectResult( '128 fluid_ounces 1 gallon is_equal', 1 )
    expectResult( '4 1 cup is_equal', 0 )

    expectException( '4 cups 1 is_equal' )      # can't compare a measurement with an integer

    # is_even
    expectResult( '-2 is_even', 1 )
    expectResult( '-1 is_even', 0 )
    expectResult( '0 is_even', 1 )
    expectResult( '1 is_even', 0 )
    expectResult( '2 is_even', 1 )

    expectEqual( '0 20000 range lambda x is_even filter', '5843 oeis 10001 left' )

    expectException( '1 i is_even' )    # real argument required

    # is_greater
    expectResult( '4 3 is_greater', 1 )
    expectResult( '55 55 is_greater', 0 )
    expectResult( 'e pi is_greater', 0 )
    expectResult( '3 inches 2 inches is_greater', 1 )
    expectResult( '8 miles 40000 feet is_greater', 1 )
    expectResult( '1 light-year 1 parsec is_greater', 0 )

    expectException( '3 i 6 is_greater' )           # real arguments required
    expectException( '3 6 i is_greater' )           # real arguments required
    expectException( '4 cups 1 mile is_greater' )   # incompatible measurements

    # is_integer
    expectResult( '1 is_integer', 1 )
    expectResult( '3 2 i + is_integer', 1 )
    expectResult( '3 2.5 i + is_integer', 0 )
    expectResult( '3.5 2 i + is_integer', 0 )
    expectResult( '3.5 is_integer', 0 )

    # is_kth_power
    expectResult( '1024 2 is_kth_power', 1 )
    expectResult( '32 2 is_kth_power', 0 )
    expectResult( '36864 2 is_kth_power', 1 )
    expectResult( '32 i 2 is_kth_power', 1 )
    expectResult( '128 i 128 - 3 is_kth_power', 1 )

    # is_less
    expectResult( '4 3 is_less', 0 )
    expectResult( '2 2 is_less', 0 )
    expectResult( '2 3 is_less', 1 )
    expectResult( '3 inches 2 inches is_less', 0 )
    expectResult( '8 miles 40000 feet is_less', 0 )
    expectResult( '1 light-year 1 parsec is_less', 1 )

    expectException( '5 i 4 is_less' )                  # real arguments required
    expectException( '5 4 i is_less' )                  # real arguments required
    expectException( '1 gallon 1 watt is_not_equal' )   # incompatible measurements

    # is_not_equal
    expectResult( '4 3 is_not_equal', 1 )
    expectResult( '3 3 is_not_equal', 0 )
    expectResult( '4 cups 1 quart is_not_equal', 0 )
    expectResult( '3 inches 2 inches is_not_equal', 1 )
    expectResult( '8 miles 40000 feet is_not_equal', 1 )
    expectResult( '1 light-year 1 parsec is_not_equal', 1 )
    expectResult( '1 inch 1 inch is_not_equal', 0 )
    expectResult( '4 1 cup is_not_equal', 1 )

    expectException( '4 cups 1 is_not_equal' )         # can't compare a measurement with an integer
    expectException( '1 inch 1 cup is_not_equal' )  # incompatible measurements

    # is_not_greater
    expectResult( '4 3 is_not_greater', 0 )
    expectResult( '77 77 is_not_greater', 1 )
    expectResult( '2 99 is_not_greater', 1 )
    expectResult( '2 miles 2 kilometers is_not_greater', 0 )
    expectResult( '129 fluid_ounces 1 gallon is_not_greater', 0 )

    expectException( '2 i 7 is_not_greater' )   # real arguments required
    expectException( '2 7 i is_not_greater' )   # real arguments required

    # is_not_less
    expectResult( '4 3 is_not_less', 1 )
    expectResult( '663 663 is_not_less', 1 )
    expectResult( '-100 100 is_not_less', 0 )
    expectResult( '3 inches 2 inches is_not_less', 1 )
    expectResult( '8 miles 40000 feet is_not_less', 1 )
    expectResult( '1 light-year 1 parsec is_not_less', 0 )
    expectResult( '12 inches 1 foot is_not_less', 1 )
    expectResult( '129 fluid_ounces 1 gallon is_not_less', 1 )

    expectException( '8 i -14 is_not_less' )    # real arguments required
    expectException( '8 -14 i is_not_less' )    # real arguments required

    # is_not_zero
    expectResult( '-1 is_not_zero', 1 )
    expectResult( '0 is_not_zero', 0 )
    expectResult( '1 is_not_zero', 1 )
    expectResult( '1 i is_not_zero', 1 )

    # is_odd
    expectResult( '-2 is_odd', 0 )
    expectResult( '-1 is_odd', 1 )
    expectResult( '0 is_odd', 0 )
    expectResult( '1 is_odd', 1 )
    expectResult( '2 is_odd', 0 )

    expectEqual( '0 20001 range lambda x is_odd filter', '5408 oeis 10001 left' )

    expectException( '5 i 3 + is_odd' )  # real arguments required
    expectException( '5 3 i - is_odd' )  # real arguments required

    # is_power
    expectResult( '1024 2 is_power_of_k', 1 )
    expectResult( '65 2 is_power_of_k', 0 )
    expectResult( '36864 2 is_power_of_k', 0 )

    # is_square
    expectResult( '1024 is_square', 1 )
    expectResult( '5 is_square', 0 )
    expectResult( '12 16 i + is_square', 1 )

    # is_zero
    expectResult( '-1 is_zero', 0 )
    expectResult( '0 is_zero', 1 )
    expectResult( '1 is_zero', 0 )
    expectResult( '1 i is_zero', 0 )

    # larger
    expectResult( '7 -7 larger', 7 )

    expectEqual( '45 pounds 30 kilograms larger' , '30 kilograms' )
    expectEqual( '3 miles 3 kilometers larger' , '3 miles' )

    expectException( '5 i 3 + 6 larger' )

    # lcm
    expectEqual( '1 10 range lcm', '[ 2 2 2 3 3 5 7 ] prod' )
    testOperator( '1 1 10 range range lcm' )

    expectEqual( '-a500 1 300 range lambda 1 x range lcm eval', '3418 oeis 301 left 300 right' )

    if slow:
        expectEqual( '-a3800 1 2308 range lambda 1 x range lcm eval', '3418 oeis 2309 left 2308 right' )

    # lcm2
    testOperator( '12 14 lcm2' )

    # mantissa
    # This works on the command line, but not here.  I have no idea why.
    #expectEqual( '-p180 1 15000 range lambda pi x sqrt * exp mantissa 0.0001 is_less filter', '127029 oeis 4 left' )

    # max
    testOperator( '[ 2 miles 11000 feet 127000 inches ] max' )

    expectResult( '1 10 range max', 10 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] max', 9 )

    expectEqual( '1 1 10 range range max', '1 10 range' )
    expectEqual( '[ 1 gallon 7 cups 250 tablespoons ] min', '7 cups' )

    expectException( '[ 6 pounds 12 inches ] max' )
    expectException( '[ 5 i 3 6 7 ] max' )

    # mean
    testOperator( '1 1 10 range range mean' )

    expectResult( '1 10 range mean', 5.5 )

    expectEqual( '1 10000 range mean', '5000.5' )

    # min
    testOperator( '[ 2 miles 11000 feet 127000 inches ] min' )

    expectResult( '1 10 range min', 1 )
    expectResult( '10 1 range min', 1 )
    expectResult( '[ 9 4 7 2 5 6 3 8 ] min', 2 )

    expectEqual( '1 1 10 range range min', '[ 1 10 dup ]' )
    expectEqual( '[ 2 cups 5 cups 1 cup ] min', '1 cup' )

    expectException( '[ 5 i 3 6 7 ] min' )
    expectException( '[ 120 volts 10 amps ] min' )

    # modulo
    expectResult( '11001 100 modulo', 1 )
    expectResult( '-120 7 modulo', 6 )
    expectResult( '8875 49 modulo', 6 )
    expectResult( '199467 8876 modulo', 4195 )

    expectEqual( '1 1000 range lambda x divisors product x divisors sum mod 1 equals filter', '188061 oeis lambda x 1001 is_less filter' )

    # FIXME:
    #if slow:
    #    expectEqual( '-a32 1 10000 range lambda x divisors product x divisors sum mod 1 equals filter', '188061 oeis lambda x 10001 is_less filter' )

    expectException( '20 i 3 modulo' )

    # multiply
    testOperator( '15 mph 10 hours *' )
    testOperator( 'c m/s convert 1 nanosecond * inches convert' )
    testOperator( '10 5 i + 20 4 i + *' )

    expectResult( '5 7 multiply', 35 )

    # nearest_int
    expectResult( '0.1 nearest_int', 0 )
    expectResult( '4.5 nearest_int', 4 )
    expectResult( 'pi nearest_int', 3 )

    expectEqual( '2 i 3.4 + nearest_int', '2 i 3 +' )
    expectEqual( '2.6 i 4 + nearest_int', '3 i 4 +' )
    expectEqual( '0 1000 range phi * nearest_int', '7067 oeis 1001 left' )

    # negative
    expectResult( '-4 negative', 4 )
    expectResult( '0 negative', 0 )
    expectResult( '4 negative', -4 )

    expectEqual( '5 i 7 + negative', '-5 i 7 -' )

    # product
    testOperator( '1 1 10 range range prod' )

    expectResult( '[ 2 cups ] product', RPNMeasurement( 2, 'cup' ) )
    expectResult( '[ 3 2 cups ] product', RPNMeasurement( 6, 'cup' ) )
    expectResult( '[ 2 cups 8 16 ] product', RPNMeasurement( 256, 'cup' ) )
    expectResult( '[ 3 2 cups 8 16 ] product', RPNMeasurement( 768, 'cup' ) )

    expectEqual( '-a200 1 100 range product', '-a200 100 !' )

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
    expectEqual( '3 cups 2 cups smaller' , '2 cups' )
    expectEqual( '3 miles 3 km smaller' , '3 km' )

    expectResult( '7 -7 smaller' , -7 )

    expectException( '2 i 5 + 3 smaller' )

    # stddev
    testOperator( '1 10 range stddev' )
    testOperator( '1 1 10 range range stddev' )

    expectEqual( '1 7654 oeis 6 left 5 right range stddev', '7655 oeis 6 left 5 right' )

    if slow:
        expectEqual( '1 7654 oeis 7 left 6 right range stddev', '7655 oeis 7 left 6 right' )

    # subtract
    testOperator( '3948 474 subtract' )
    testOperator( '57 hectares 23 acres -' )
    testOperator( '10 Mb second / 700 MB hour / -' )
    testOperator( 'today 3 days -' )
    testOperator( 'today 3 weeks -' )
    testOperator( 'today 3 months -' )
    testOperator( 'now earth_radius 2 pi * * miles convert 4 mph / -' )
    testOperator( 'today 2 months -' )
    testOperator( 'today 1965-03-31 -' )
    testOperator( '2015-01-01 1965-03-31 -' )

    expectResult( '4 cups 27 teaspoons - teaspoons convert', RPNMeasurement( 165, 'teaspoon' ) )

    expectException( '2 light-year 3 seconds -' )

    # sum
    testOperator( '[ 27 days 7 hour 43 minute 12 second ] sum' )
    testOperator( '1 1 10 range range sum' )

    expectResult( '1 10 range sum', 55 )

    expectEqual( '[ 2 cups 3 cups 4 cups 5 cups ] sum', '14 cups' )
    expectEqual( '2 1000 range factor sum', '1414 oeis 1000 left 999 right' )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    loadAstronomyData( )

    if not g.astroDataAvailable:
        return

    # angular_separation
    testOperator( 'sun moon "Corolla, NC" "2017-08-21 14:50" angular_separation dms' )

    # angular_size
    testOperator( 'sun "Herndon, VA" now angular_size dms' )

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

    # distance_from_earth
    testOperator( 'mars now distance_from_earth miles convert' )

    # dusk
    testOperator( '"Vienna, Austria" location today dusk' )
    testOperator( '"Vienna, Austria" today dusk' )

    # eclipse_totality
    testOperator( 'sun moon "Corolla, NC" "2017-08-21 14:50" eclipse_totality' )

    # moonrise
    testOperator( '"Las Cruces, NM" location today moonrise' )
    testOperator( '"Las Cruces, NM" today moonrise' )

    # moonset
    testOperator( '"Tacoma, WA" location today moonset' )
    testOperator( '"Tacoma, WA" today moonset' )

    # moon_antitransit
    testOperator( '"Madrid, Spain" location today moon_antitransit' )
    testOperator( '"Madrid, Spain" today moon_antitransit' )

    # moon_phase
    testOperator( 'today moon_phase' )

    # moon_transit
    testOperator( '"Riga, Latvia" location today moon_transit' )
    testOperator( '"Riga, Latvia" today moon_transit' )

    # nautical_dawn
    testOperator( '"Columbia, SC" location today nautical_dawn' )
    testOperator( '"Columbia, SC" today nautical_dawn' )

    # nautical_dusk
    testOperator( '"Norfolk, VA" location today nautical_dusk' )
    testOperator( '"Norfolk, VA" today nautical_dusk' )

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

    # sky_location
    testOperator( 'mars "Leesburg, VA" now sky_location' )

    # solar_noon
    testOperator( '"Leesburg, VA" location today solar_noon' )
    testOperator( '"Leesburg, VA" today solar_noon' )

    # summer_solstice
    testOperator( '2015 summer_solstice' )

    # sunrise
    testOperator( '"Salzburg, Germany" location today sunrise' )
    testOperator( '"Salzburg, Germany" today sunrise' )

    # sunset
    testOperator( '"New Delhi, India" location today sunset' )
    testOperator( '"New Delhi, India" today sunset' )

    # sun_antitransit
    testOperator( '"Leesburg, VA" location today sun_antitransit' )
    testOperator( '"Leesburg, VA" today sun_antitransit' )

    # transit_time
    testOperator( 'sun "Munich, Germany" location today transit_time' )
    testOperator( 'moon "Dusseldorf, Germany" today transit_time' )
    testOperator( 'mars "Dortmund, Germany" 2015 summer 1 20 range days + transit_time' )

    # vernal_equinox
    testOperator( '2015 vernal_equinox' )

    # winter_solstice
    testOperator( '2015 winter_solstice' )

    # heavenly body operators
    # sun
    testOperator( 'sun "Leesburg, VA" location today next_rising' )
    testOperator( 'sun "Leesburg, VA" today next_rising' )

    # mercury
    testOperator( 'mercury "Los Angeles, CA" location today next_rising' )
    testOperator( 'mercury "Los Angeles, CA" today next_rising' )

    # venus
    testOperator( 'venus "Butte, Montana" location today next_rising' )
    testOperator( 'venus "Butte, Montana" today next_rising' )

    # moon
    testOperator( 'saturn "Burlington, VT" location today next_antitransit' )
    testOperator( 'saturn "Burlington, VT" today next_antitransit' )

    # mars
    testOperator( 'mars "Beijing, China" location today next_transit' )
    testOperator( 'mars "Beijing, China" today next_transit' )

    # jupiter
    testOperator( 'jupiter "Ottawa, Canada" location today next_setting' )
    testOperator( 'jupiter "Ottawa, Canada" today next_setting' )

    # saturn
    testOperator( 'saturn "Leesburg, VA" location today next_rising' )
    testOperator( 'saturn "Leesburg, VA" today next_rising' )

    # uranus
    testOperator( 'uranus "Frankfurt, Germany" location today next_rising' )
    testOperator( 'uranus "Frankfurt, Germany" today next_rising' )

    # neptune
    testOperator( 'neptune "Hatfield, PA" location now next_rising' )
    testOperator( 'neptune "Hatfield, PA" now next_rising' )

    # pluto
    testOperator( 'pluto "Johannesburg, South Africa" location now next_rising' )
    testOperator( 'pluto "Johannesburg, South Africa" now next_rising' )


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
    # ascension
    testOperator( '2016 ascension' )

    # ash_wednesday
    testOperator( '2015 ash_wednesday' )

    # calendar
    testOperator( '1965-03-31 calendar' )
    testOperator( '2014-10-01 calendar' )
    testOperator( 'today calendar' )

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

    # epiphany
    testOperator( '2018 epiphany' )

    # fathers_day
    testOperator( '2018 fathers_day' )

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

    # good_friday
    testOperator( '2018 good_friday' )

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

    # mothers_day
    testOperator( '2018 mothers_day' )

    # new_years_day
    testOperator( '2018 new_years_day' )

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

    # weekday_name
    testOperator( 'today weekday_name' )

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

    expectException( 'Va atomic_number' )   # invalid atomic symbol

    # atomic_symbol
    testOperator( '1 atomic_symbol' )
    testOperator( '118 atomic_symbol' )

    expectException( '119 atomic_symbol' )  # atomic number out of range
    expectException( '0 atomic_symbol' )    # atomic number out of range

    # atomic_weight
    testOperator( '1 118 range atomic_weight' )

    expectException( '119 atomic_symbol' )  # atomic number out of range
    expectException( '0 atomic_symbol' )    # atomic number out of range

    # element_block
    testOperator( '1 118 range element_block')

    expectException( '119 element_block' )  # atomic number out of range
    expectException( '0 element_block' )    # atomic number out of range

    # element_boiling_point
    testOperator( '1 118 range element_boiling_point')

    expectException( '119 element_boiling_point' )   # atomic number out of range
    expectException( '0 element_boiling_point' )     # atomic number out of range

    # element_density
    testOperator( '1 118 range element_density')

    expectException( '119 element_density' )   # atomic number out of range
    expectException( '0 element_density' )     # atomic number out of range

    # element_description
    testOperator( '1 118 range element_description' )

    expectException( '119 element_description' )   # atomic number out of range
    expectException( '0 element_description' )     # atomic number out of range

    # element_group
    testOperator( '1 118 range element_group')

    expectException( '119 element_group' )   # atomic number out of range
    expectException( '0 element_group' )     # atomic number out of range

    # element_melting_point
    testOperator( '1 118 range element_melting_point')

    expectException( '119 element_melting_point' )   # atomic number out of range
    expectException( '0 element_melting_point' )     # atomic number out of range

    # element_name
    testOperator( '1 118 range element_name' )

    expectException( '119 element_name' )    # atomic number out of range
    expectException( '0 element_name' )      # atomic number out of range

    # element_occurrence
    testOperator( '1 118 range element_occurrence' )

    expectException( '119 element_occurrence' )   # atomic number out of range
    expectException( '0 element_occurrence' )     # atomic number out of range

    # element_period
    testOperator( '1 118 range element_period' )

    expectException( '119 element_period' )    # atomic number out of range
    expectException( '0 element_period' )      # atomic number out of range

    # element_state
    testOperator( '1 118 range element_state' )

    expectException( '119 element_state' )     # atomic number out of range
    expectException( '0 element_state' )       # atomic number out of range

    # molar_mass
    testOperator( 'H2O molar_mass' )
    testOperator( 'C12H22O11 molar_mass' )

    expectException( 'ZoO2 molar_mass' )       # invalid molecule expression

    expectException( '2 H atomic_number' )     # non-unit measurement can't be a validly expressed atomic symbol

    # Check to see where atomic symbols collide with other aliases, and if the exception handling deals with it correctly.
    testOperator( 'H molar_mass' )
    testOperator( 'H element_description' )

    testOperator( 'H atomic_number' )       # henry
    testOperator( 'He atomic_number' )
    testOperator( 'Li atomic_number' )
    testOperator( 'Be atomic_number' )
    testOperator( 'B atomic_number' )       # byte
    testOperator( 'C atomic_number' )       # coulomb
    testOperator( 'N atomic_number' )       # newton
    testOperator( 'O atomic_number' )       # ohm
    testOperator( 'F atomic_number' )       # farad
    testOperator( 'Ne atomic_number' )

    testOperator( 'Na atomic_number' )
    testOperator( 'Mg atomic_number' )      # megagram
    testOperator( 'Al atomic_number' )
    testOperator( 'Si atomic_number' )
    testOperator( 'P atomic_number' )
    testOperator( 'S atomic_number' )       # siemens
    testOperator( 'Cl atomic_number' )
    testOperator( 'Ar atomic_number' )
    testOperator( 'K atomic_number' )       # kelvin
    testOperator( 'Ca atomic_number' )

    testOperator( 'Sc atomic_number' )
    testOperator( 'Ti atomic_number' )
    testOperator( 'V atomic_number' )       # volt
    testOperator( 'Cr atomic_number' )
    testOperator( 'Mn atomic_number' )
    testOperator( 'Fe atomic_number' )
    testOperator( 'Co atomic_number' )
    testOperator( 'Ni atomic_number' )
    testOperator( 'Cu atomic_number' )
    testOperator( 'Zn atomic_number' )

    testOperator( 'Ga atomic_number' )      # gigare
    testOperator( 'Ge atomic_number' )
    testOperator( 'As atomic_number' )      # ampere-second
    testOperator( 'Se atomic_number' )
    testOperator( 'Br atomic_number' )
    testOperator( 'Kr atomic_number' )
    testOperator( 'Rb atomic_number' )
    testOperator( 'Sr atomic_number' )
    testOperator( 'Y atomic_number' )
    testOperator( 'Zr atomic_number' )

    testOperator( 'Nb atomic_number' )
    testOperator( 'Mo atomic_number' )
    testOperator( 'Tc atomic_number' )
    testOperator( 'Ru atomic_number' )
    testOperator( 'Rh atomic_number' )
    testOperator( 'Pd atomic_number' )
    testOperator( 'Ag atomic_number' )
    testOperator( 'Cd atomic_number' )
    testOperator( 'In atomic_number' )
    testOperator( 'Sn atomic_number' )

    testOperator( 'Sb atomic_number' )
    testOperator( 'Te atomic_number' )
    testOperator( 'I atomic_number' )
    testOperator( 'Xe atomic_number' )
    testOperator( 'Cs atomic_number' )
    testOperator( 'Ba atomic_number' )      # barye
    testOperator( 'La atomic_number' )
    testOperator( 'Ce atomic_number' )
    testOperator( 'Pr atomic_number' )
    testOperator( 'Nd atomic_number' )

    testOperator( 'Pm atomic_number' )      # petameter
    testOperator( 'Sm atomic_number' )
    testOperator( 'Eu atomic_number' )
    testOperator( 'Gd atomic_number' )
    testOperator( 'Tb atomic_number' )      # terabit
    testOperator( 'Dy atomic_number' )
    testOperator( 'Ho atomic_number' )
    testOperator( 'Er atomic_number' )
    testOperator( 'Tm atomic_number' )      # terameter
    testOperator( 'Yb atomic_number' )      # yottabit

    testOperator( 'Lu atomic_number' )
    testOperator( 'Hf atomic_number' )
    testOperator( 'Ta atomic_number' )      # terare
    testOperator( 'W atomic_number' )       # watt
    testOperator( 'Re atomic_number' )      # reaumur
    testOperator( 'Os atomic_number' )
    testOperator( 'Ir atomic_number' )
    testOperator( 'Pt atomic_number' )
    testOperator( 'Au atomic_number' )
    testOperator( 'Hg atomic_number' )

    testOperator( 'Tl atomic_number' )
    testOperator( 'Pb atomic_number' )      # petabit
    testOperator( 'Bi atomic_number' )
    testOperator( 'Po atomic_number' )
    testOperator( 'At atomic_number' )
    testOperator( 'Rn atomic_number' )
    testOperator( 'Fr atomic_number' )      # franklin
    testOperator( 'Ra atomic_number' )
    testOperator( 'Ac atomic_number' )
    testOperator( 'Th atomic_number' )

    testOperator( 'Pa atomic_number' )      # petare
    testOperator( 'U atomic_number' )
    testOperator( 'Np atomic_number' )
    testOperator( 'Pu atomic_number' )
    testOperator( 'Am atomic_number' )      # ampere-minute
    testOperator( 'Cm atomic_number' )
    testOperator( 'Bk atomic_number' )
    testOperator( 'Cf atomic_number' )
    testOperator( 'Es atomic_number' )      # exasecond
    testOperator( 'Fm atomic_number' )

    testOperator( 'Md atomic_number' )
    testOperator( 'No atomic_number' )
    testOperator( 'Lr atomic_number' )
    testOperator( 'Rf atomic_number' )
    testOperator( 'Db atomic_number' )
    testOperator( 'Sg atomic_number' )
    testOperator( 'Bh atomic_number' )
    testOperator( 'Hs atomic_number' )
    testOperator( 'Mt atomic_number' )
    testOperator( 'Ds atomic_number' )

    testOperator( 'Rg atomic_number' )
    testOperator( 'Cn atomic_number' )
    testOperator( 'Nh atomic_number' )
    testOperator( 'Fl atomic_number' )
    testOperator( 'Mc atomic_number' )
    testOperator( 'Lv atomic_number' )
    testOperator( 'Ts atomic_number' )      # terasecond
    testOperator( 'Og atomic_number' )


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

    from rpn.rpnSpecial import downloadOEISSequence

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
    expectEqual( '0 27 range lambda 10 x + 1 - x binomial 1 - eval', '35927 oeis 28 left' )

    # combinations
    expectEqual( '0 99 range lambda x 2 * x combinations sqr x 2 * x combinations + 2 / eval', '37967 oeis 100 left' )

    # compositions
    testOperator( '5 2 compositions' )
    testOperator( '6 3 compositions' )
    testOperator( '7 2 4 range compositions' )

    # debruijn
    testOperator( '4 3 debruijn' )

    # denomination_combinations
    expectResult( '[ 1 5 10 25 50 100 ] 100 denomination_combinations', 293 )

    expectEqual( '0 999 range lambda [ 1 5 10 ] x denomination_combinations eval', '187243 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 ] x denomination_combinations eval', '8 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 5 10 25 ] x denomination_combinations eval', '1299 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 5 10 25 50 ] x denomination_combinations eval', '1300 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 25 ] x denomination_combinations eval', '1301 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 25 50 ] x denomination_combinations eval', '1302 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 4 10 20 40 100 ] x denomination_combinations eval', '1310 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 50 100 ] x denomination_combinations eval', '1312 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 20 50 ] x denomination_combinations eval', '1313 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 2 5 10 20 50 ] x denomination_combinations eval', '1319 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 4 10 ] x denomination_combinations eval', '1362 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 5 10 20 50 100 ] x denomination_combinations eval', '1343 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 2 4 12 24 48 96 120 ] x denomination_combinations eval', '1364 oeis 1000 left' )
    expectEqual( '0 999 range lambda [ 1 5 10 25 50 100 ] x denomination_combinations eval', '169718 oeis 1000 left' )
    expectEqual( '0 54 range lambda [ 1 2 3 5 10 20 25 50 100 ] x denomination_combinations eval', '67996 oeis 55 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 20 50 100 200 500 1000 2000 5000 10000 20000 50000 ] x denomination_combinations eval', '57537 oeis 1000 left' )
    expectEqual( '0 99 range lambda [ 1 5 10 25 50 100 ] x 100 * denomination_combinations eval', '85502 oeis 100 left' )
    expectEqual( '0 999 range lambda [ 1 2 5 10 50 100 200 500 ] x denomination_combinations eval', '182086 oeis 1000 left' )
    expectEqual( '0 20 range lambda [ 1 5 10 25 ] x 100 * denomination_combinations eval', '160551 oeis 21 left' )

    if slow:
        expectEqual( '0 9999 range lambda [ 1 5 10 25 ] x denomination_combinations eval', '1299 oeis 10000 left' )
        expectEqual( '0 9999 range lambda [ 1 5 10 25 50 ] x denomination_combinations eval', '1300 oeis 10000 left' )
        expectEqual( '0 999 range lambda [ 1 5 10 25 50 100 ] x 100 * denomination_combinations eval', '85502 oeis 1000 left' )

    # get_combinations
    testOperator( '1 5 range 2 get_combinations' )

    # get_permutations
    testOperator( '1 5 range 2 get_permutations' )

    # lah
    testOperator( '5 6 lah' )

    expectEqual( '-a170 1 100 range lambda x 1 x range lah eval flatten', '8297 oeis 5050 left' )

    # menage
    testOperator( '10 menage' )

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

    expectEqual( '-a15 1 27 range lambda x 1 x range narayana eval flatten 364 left', '1263 oeis 364 left' )

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
        expectEqual( '-a1000 0 2106 range nth_motzkin', '1006 oeis 2016 left' )

    # nth_pell
    testOperator( '13 nth_pell' )

    expectEqual( '-a383 1 100 range nth_pell', '129 oeis 100 left' )

    if slow:
        expectEqual( '-a383 1 1001 range nth_pell', '129 oeis 1001 left' )

    # nth_schroeder
    testOperator( '-a50 67 nth_schroeder' )

    expectEqual( '-a80 1 100 range nth_schroeder', '6318 oeis 100 left' )

    if slow:
        expectEqual( '-a1600 1 2000 range nth_schroeder', '6318 oeis 2000 left' )

    # nth_schroeder_hipparchus
    testOperator( '1 10 range nth_schroeder_hipparchus' )

    expectEqual( '-a80 0 99 range nth_schroeder_hipparchus', '1003 oeis 100 left' )

    if slow:
        expectEqual( '-a1000 0 1311 range nth_schroeder_hipparchus', '1003 oeis 1312 left' )

    # nth_sylvester
    testOperator( '45 nth_sylvester' )

    expectEqual( '1 13 range nth_sylvester', '58 oeis 13 left' )

    # partitions
    testOperator( '1 10 range partitions' )

    # This function is extremely slow without caching.
    expectEqual( '0 15 range partitions', '41 oeis 16 left' )

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

    expectEqual( '-a70 1 2 i + 0 199 range ** real', '6495 oeis 200 left' )

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
    testOperator( 'infinity lambda x 1/x 1 + x ** limit' )

    expectEqual( 'infinity lambda x fib x 1 - fib / limit', 'phi' )

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
    testOperator( 'pi' )
    testOperator( 'plastic_constant' )
    testOperator( 'prevost_constant' )
    testOperator( 'robbins_constant' )
    testOperator( 'silver_ratio' )

    expectEqual( '-a150 e 0 300 range ** floor', '149 oeis 301 left' )
    expectEqual( '1 10000 range phi * floor', '201 oeis 10000 left' )

    # programming integer constants
    expectResult( 'min_uchar', 0 )
    expectResult( 'min_ulong', 0 )
    expectResult( 'min_ulonglong', 0 )
    expectResult( 'min_uquadlong', 0 )
    expectResult( 'min_ushort', 0 )

    expectEqual( 'max_char', '2 7 ** 1 -' )
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
    expectEqual( 'min_long', '2 31 ** negative' )
    expectEqual( '-a20 min_longlong', '-a20 2 63 ** negative' )
    expectEqual( '-a40 min_quadlong', '-a40 2 127 ** negative' )
    expectEqual( 'min_short', '2 15 ** negative' )

    # Planck constants
    testOperator( 'planck_length' )
    testOperator( 'planck_mass' )
    testOperator( 'planck_time' )
    testOperator( 'planck_charge' )
    testOperator( 'planck_temperature' )

    testOperator( 'planck_acceleration' )
    testOperator( 'planck_angular_frequency' )
    testOperator( 'planck_area' )
    testOperator( 'planck_current' )
    testOperator( 'planck_density' )
    testOperator( 'planck_electrical_inductance' )
    testOperator( 'planck_energy' )
    testOperator( 'planck_energy_density' )
    testOperator( 'planck_force' )
    testOperator( 'planck_impedance' )
    testOperator( 'planck_intensity' )
    testOperator( 'planck_magnetic_inductance' )
    testOperator( 'planck_momentum' )
    testOperator( 'planck_power' )
    testOperator( 'planck_pressure' )
    testOperator( 'planck_viscosity' )
    testOperator( 'planck_voltage' )
    testOperator( 'planck_volumetric_flow_rate' )
    testOperator( 'planck_volume' )


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

    # expectEqual can't handle date values
    #expectEqual( '[ 1965 03 31 ] make_datetime', '1965-03-31' )

    expectException( '[ 1965 0 12 ] make_datetime' )
    expectException( '[ 1965 3 0 ] make_datetime' )
    expectException( '[ 1965 3 32 ] make_datetime' )
    expectException( '[ 1965 13 13 ] make_datetime' )
    expectException( '[ 1965 4 31 ] make_datetime' )
    expectException( '[ 1965 2 29 ] make_datetime' )

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
# //  runFigurateNumberOperatorTests
# //
# //******************************************************************************

def runFigurateNumberOperatorTests( ):
    # centered_cube
    testOperator( '1 20 range centered_cube' )
    testOperator( '100 centered_cube' )

    expectEqual( '1 1000 range centered_cube', '5898 oeis 1000 left' )

    # centered_decagonal
    testOperator( '17 centered_decagonal' )

    expectEqual( '1 1000 range centered_decagonal', '62786 oeis 1000 left' )

    # centered_dodecahedral
    testOperator( '1 20 range centered_dodecahedral' )
    testOperator( '60 centered_dodecahedral' )

    expectEqual( '1 36 range centered_dodecahedral', '5904 oeis 36 left' )

    # centered_heptagonal
    testOperator( '102 centered_heptagonal' )

    expectEqual( '1 1000 range centered_heptagonal', '69099 oeis 1000 left' )

    # centered_hexagonal
    testOperator( '103 centered_hexagonal' )

    expectEqual( '1 1000 range centered_hexagonal', '3215 oeis 1000 left' )

    # centered_icosahedral
    testOperator( '1 20 range centered_icosahedral' )
    testOperator( '30 centered_icosahedral' )

    expectEqual( '1 36 range centered_icosahedral', '5902 oeis 36 left' )

    # centered_nonagonal
    testOperator( '104 centered_nonagonal' )

    expectEqual( '1 1000 range centered_nonagonal', '60544 oeis 1000 left' )

    # centered_octagonal
    testOperator( '10 centered_octagonal' )

    expectEqual( '1 1000 range centered_octagonal', '16754 oeis 1000 left' )

    # centered_octahedral
    testOperator( '1 20 range centered_octahedral' )
    testOperator( '70 centered_octahedral' )

    expectEqual( '1 40 range centered_octahedral', '1845 oeis 40 left' )

    # centered_pentagonal
    testOperator( '108 centered_pentagonal' )

    expectEqual( '1 1000 range centered_pentagonal', '5891 oeis 1000 left' )

    # centered_polygonal
    testOperator( '108 5 centered_polygonal' )

    # centered_square
    testOperator( '5 centered_square' )

    expectEqual( '1 1000 range centered_square', '1844 oeis 1000 left' )

    # centered_tetrahedral
    testOperator( '1 20 range centered_tetrahedral' )
    testOperator( '120 centered_tetrahedral' )

    expectEqual( '1 39 range centered_tetrahedral', '5894 oeis 39 left' )

    # centered_triangular
    testOperator( '100 centered_triangular' )

    expectEqual( '1 10000 range centered_triangular', '5448 oeis 10000 left' )

    # decagonal
    testOperator( '151 decagonal' )

    expectEqual( '0 1000 range decagonal', '1107 oeis 1001 left' )

    # decagonal_centered_square
    testOperator( '-a40 9 decagonal_centered_square' )

    expectEqual( '-a1000 1 317 range decagonal_centered_square', '133142 oeis 317 left' )

    # decagonal_heptagonal
    testOperator( '-a50 8 decagonal_heptagonal' )

    #expectEqual( '-a100 1 12 range decagonal_heptagonal', '203408 oeis 12 left' )

    # decagonal_hexagonal
    testOperator( '-a60 9 decagonal_hexagonal' )

    #expectEqual( '-a50 1 12 range decagonal_hexagonal', '203134 oeis 12 left' )

    # decagonal_nonagonal
    testOperator( '-a75 9 decagonal_nonagonal' )

    expectEqual( '-a50 1 9 range decagonal_nonagonal', '203627 oeis 9 left' )

    # decagonal_octagonal
    testOperator( '-a75 9 decagonal_octagonal' )

    #expectEqual( '-a50 1 10 range decagonal_octagonal', '203624 oeis 10 left' )

    # decagonal_pentagonal
    testOperator( '-a60 7 decagonal_pentagonal' )

    #expectEqual( '-a400 1 100 range decagonal_pentagonal', '202563 oeis 100 left' )

    # decagonal_triangular
    testOperator( '-a40 13 decagonal_triangular' )

    #expectEqual( '-a50 0 17 range decagonal_triangular', '113216 oeis 18 left' )

    # dodecahedral
    testOperator( '44 dodecahedral' )

    # generalized_pentagonal
    testOperator( '187 generalized_pentagonal' )

    # heptagonal
    testOperator( '203 heptagonal' )

    expectEqual( '0 1000 range heptagonal', '566 oeis 1001 left' )

    # heptagonal_hexagonal
    testOperator( '2039 heptagonal_hexagonal' )

    #expectEqual( '-a500 1 200 range heptagonal_hexagonal', '48901 oeis 200 left' )

    # heptagonal_pentagonal
    testOperator( '8684 heptagonal_pentagonal' )

    #expectEqual( '-a2000 1 558 range heptagonal_pentagonal', '46198 oeis 558 left' )

    # heptagonal_square
    testOperator( '222 heptagonal_square' )

    #expectEqual( '-a2000 1 950 range heptagonal_pentagonal', '46195 oeis 950 left' )

    # heptagonal_triangular
    testOperator( '-a1000 -c 399 heptagonal_triangular' )

    #expectEqual( '-a1000 1 399 range heptagonal_triangular', '46194 oeis 399 left' )

    # hexagonal
    testOperator( '340 hexagonal' )

    expectEqual( '0 1000 range hexagonal', '384 oeis 1001 left' )

    # hexagonal_pentagonal
    testOperator( '-a250 -c 107 hexagonal_pentagonal' )

    #expectEqual( '-a1000 1 438 range hexagonal_pentagonal', '46178 oeis 438 left' )

    # hexagonal_square
    testOperator( '-a70 -c 23 hexagonal_square' )

    #expectEqual( '-a1000 1 327 range hexagonal_square', '46177 oeis 327 left' )

    # icosahedral
    testOperator( '100 icosahedral' )

    # nonagonal
    testOperator( '554 nonagonal' )

    # nonagonal_heptagonal
    testOperator( '-a50 -c 12 nonagonal_heptagonal' )

    #expectEqual( '-a1000 1 233 range nonagonal_heptagonal', '48921 oeis 233 left' )

    # nonagonal_hexagonal
    testOperator( '-a60 -c 13 nonagonal_hexagonal' )

    #expectEqual( '-a1000 1 208 range nonagonal_hexagonal', '48918 oeis 208 left' )

    # nonagonal_octagonal
    testOperator( '-a75 -c 14 nonagonal_octagonal' )

    #expectEqual( '-a600 1 100 range nonagonal_octagonal', '48924 oeis 100 left' )

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

    # rhombic_dodecahedral
    testOperator( '89 rhombic_dodecahedral' )

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

    # filter_list

    # for_each
    testOperator( '[ [ 2 3 ] [ 4 5 ] ] lambda x y add for_each' )

    # for_each_list
    testOperator( '[ [ 2 3 ] [ 4 5 ] [ 6 7 ] [ 8 9 ] ] lambda x -1 element for_each_list' )

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
    expectEqual( '1 310 range lambda 2 x ** get_digits 1 left 2 equals filter', '67469 oeis 56 left' )

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
    testOperator( '"Leesburg, VA" location "Smithfield, VA" location geo_distance' )
    testOperator( '"Leesburg, VA" "Smithfield, VA" geo_distance' )

    # get_timezone
    testOperator( '"Leesburg, VA" get_timezone' )

    # lat_long
    #testOperator( '"Leesburg, VA" 43 -80 lat_long geo_distance' )

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

    expectEqual( '-a125 1 dodecahedron_area value 10 121 ** * get_digits 120 left', '131595 oeis 120 left' )

    # dodecahedron_volume
    testOperator( '1 dodecahedron_volume' )

    expectEqual( '-a1001 1 dodecahedron_volume value 10 1001 ** * get_digits 1000 left', '102769 oeis 1000 left' )

    # hypotenuse
    testOperator( '3 4 hypotenuse' )

    # icosahedron_area
    testOperator( '1 icosahedron_area' )

    expectEqual( '0 9999 range icosahedron_area value round', '71398 oeis 10000 left' )

    # icosahedron_volume
    testOperator( '1 icosahedron_volume' )

    expectEqual( '-a1001 1 icosahedron_volume value 10 1001 ** * get_digits 1000 left', '102208 oeis 1000 left' )

    # k_sphere_area
    testOperator( '34 inches 8 k_sphere_area' )
    testOperator( '34 inches 4 ** 5 k_sphere_area' )
    testOperator( '34 inches 7 ** 7 k_sphere_area' )

    expectException( '34 cubic_inches 2 k_sphere_area' )

    # k_sphere_radius
    testOperator( '3 meters 4 k_sphere_radius' )
    testOperator( '3 meters 3 ** 4 k_sphere_radius' )
    testOperator( '3 cubic_meters 4 k_sphere_radius' )

    expectException( '3 cubic_meters 2 k_sphere_radius' )

    # k_sphere_volume
    testOperator( '6 inches 8 ** 9 k_sphere_volume' )
    testOperator( '3 feet 5 ** 6 k_sphere_volume' )
    testOperator( '50 cubic_centimeters sqr 7 k_sphere_volume' )

    expectException( '50 cubic_centimeters 1 k_sphere_volume' )

    # octahedron_area
    testOperator( '1 octahedron_area' )

    expectEqual( '0 9999 range octahedron_area value round', '71396 oeis 10000 left' )

    # octahedron_volume
    testOperator( '1 octahedron_volume' )
    expectEqual( '-a1001 1 octahedron_volume value 10 1001 ** * get_digits 1000 left', '131594 oeis 1000 left' )

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

    # count_digits

    # duplicate_digits
    expectResult( '543 2 duplicate_digits', 54343 )
    expectResult( '1024 1 4 range duplicate_digits', [ 10244, 102424, 1024024, 10241024 ] )

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
    testOperator( '123456789 5 get_left_digits' )

    # get_left_truncations
    testOperator( '123456789 get_left_truncations' )

    # get_nonzero_base_k_digits
    testOperator( '1234567890 23 get_nonzero_base_k_digits' )

    # get_nonzero_digits
    testOperator( '1234567890 get_nonzero_digits' )

    # get_right_digits
    expectEqual( '-a420 1 2000 range lambda x fib x log10 floor 1 + get_right_digits x equals filter', '-a420 350 oeis 42 left 41 right' )

    if slow:
        expectEqual( '-a21000 dddd[159] build_numbers lambda x fib x log10 floor 1 + get_right_digits x equals filter', '-a420 350 oeis 573 left 572 right' )

    # get_right_truncations
    testOperator( '123456789 get_right_truncations' )

    # has_any_digits
    if g.primeDataAvailable:
        expectEqual( '1 1113 primes lambda x 2357 has_any_digits filter', '179336 oeis 1000 left' )

    if g.primeDataAvailable and slow:
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

    # is_base_k_pandigital
    testOperator( '18475 12 is_base_k_pandigital' )

    expectResult( '970 5 is_base_k_pandigital', 1 )
    expectResult( '54480996 9 is_base_k_pandigital', 1 )

    # is_bouncy
    testOperator( '23 is_bouncy' )

    # is_decreasing
    testOperator( '13884576 is_decreasing' )

    expectResult( '12234566 is_decreasing', 0 )
    expectResult( '66633322 is_decreasing', 1 )
    expectResult( '987654321 is_decreasing', 1 )
    expectResult( ' 1111111 is_decreasing', 1 )
    expectResult( ' 11111112 is_decreasing', 0 )

    # is_digital_permutation
    testOperator( '12 21 is_digital_permutation' )

    expectResult( '12 21 is_digital_permutation', 1 )
    expectResult( '123456 625143 is_digital_permutation', 1 )
    expectResult( '123456 25143 is_digital_permutation', 0 )
    expectResult( '123456 725143 is_digital_permutation', 0 )

    # is_generalized_dudeney
    testOperator( '2 5 is_generalized_dudeney' )

    # is_harshad
    testOperator( '3 6 is_harshad' )

    # is_increasing
    testOperator( '30458356 is_increasing' )

    expectResult( '12234566 is_increasing', 1 )
    expectResult( '66633322 is_increasing', 0 )
    expectResult( '987654321 is_increasing', 0 )
    expectResult( ' 1111111 is_increasing', 1 )
    expectResult( ' 11111112 is_increasing', 1 )

    # is_kaprekar
    testOperator( '533170 is_kaprekar' )

    expectResult( '533170 is_kaprekar', 1 )
    expectResult( '77777 is_kaprekar', 0 )
    expectResult( '77778 is_kaprekar', 1 )
    expectResult( '95121 is_kaprekar', 1 )
    expectResult( '7272 is_kaprekar', 1 )
    expectResult( '22223 is_kaprekar', 0 )
    expectEqual( '1 10000 range lambda x is_kaprekar filter', '53816 oeis 15 left' )

    # is_k_morphic
    testOperator( '1 100 range lambda x 7 is_k_morphic filter' )

    expectEqual( '1 10000 range lambda x x is_k_morphic filter', '82576 oeis 234 left' )

    # is_narcissistic
    testOperator( '152 is_narcissistic' )

    expectResult( '152 is_narcissistic', 0 )
    expectResult( '153 is_narcissistic', 1 )
    expectResult( '154 is_narcissistic', 0 )

    expectEqual( '1 10000 range lambda x is_narcissistic filter', '5188 oeis 16 left' )

    # is_palindrome
    testOperator( '101 is_palindrome' )

    expectResult( '101 is_palindrome', 1 )
    expectResult( '1 22 range is_palindrome', [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ] )
    expectResult( '1234567890 is_palindrome', 0 )

    expectEqual( '0 10000 range lambda x is_palindrome filter', '2113 oeis 199 left' )

    # is_pandigital
    testOperator( '1234567890 is_pandigital' )

    expectResult( '1234567890 is_pandigital', 1 )
    expectResult( '123456789 is_pandigital', 1 )
    expectResult( '12345670 is_pandigital', 0 )
    expectResult( '12345 is_pandigital', 1 )
    expectResult( '321 is_pandigital', 1 )

    # is_pddi
    testOperator( '1253 4 is_pddi' )

    # is_pdi
    testOperator( '1253 4 is_pdi' )

    # is_sum_product
    testOperator( '3 5 is_sum_product' )

    # is_trimorphic
    testOperator( '1 100 range is_trimorphic' )

    expectEqual( '1 1000 range lambda x is_trimorphic filter', '33819 oeis 26 left 25 right' )

    # k_persistence
    testOperator( '679 2 k_persistence' )
    testOperator( '6788 3 k_persistence' )
    testOperator( '68889 4 k_persistence' )

    expectResult( '77 1 k_persistence', 4 )

    # multiply_digits
    testOperator( '243384 multiply_digits' )

    expectEqual( '123456789 multiply_digits', '9 !' )
    expectEqual( '1 33883 range lambda x 0 has_digits not filter lambda x multiply_digits 3 is_kth_power filter', '237767 oeis 1000 left' )

    # multiply_digit_powers
    testOperator( '5734475 2 multiply_digit_powers' )

    # multiply_nonzero_digits
    testOperator( '385202358 multiply_nonzero_digits' )

    # multiply_nonzero_digit_powers
    testOperator( '385202358 3 multiply_nonzero_digit_powers' )

    # permute_digits
    testOperator( '12345 permute_digits' )

    expectEqual( '12345 permute_digits', '30299 oeis 153 left 120 right' )
    expectEqual( '123456 permute_digits', '30299 oeis 873 left 720 right' )
    expectEqual( '1234567 permute_digits', '30299 oeis 5913 left 5040 right' )
    expectEqual( '123456789 permute_digits 18 left', '50289 oeis 18 left' )

    # persistence
    expectResult( '77 persistence', 4 )
    expectResult( '679 persistence', 5 )
    expectResult( '6788 persistence', 6 )
    expectResult( '68889 persistence', 7 )
    expectResult( '2677889 persistence', 8 )

    # replace_digits
    testOperator( '1 2 134958' )

    # reverse_digits
    testOperator( '37 1 8 range * reverse_digits' )
    testOperator( '37 1 2 9 range range * reverse_digits' )

    expectEqual( '0 1102 range lambda x sqr reverse_digits x reverse_digits sqr equals filter', '61909 oeis 53 left' )

    # rotate_digits_left
    testOperator( '12345 1 rotate_digits_left' )

    # rotate_digits_right
    testOperator( '12345 1 rotate_digits_right' )

    # show_erdos_persistence
    testOperator( '-a30 55555555555555557777777777777 show_erdos_persistence' )

    # show_k_persistence
    testOperator( '-a60 3 2222222223333333778 3 show_k_persistence' )
    testOperator( '-a30 1 10 range 5 show_k_persistence -s1' )

    # show_persistence
    testOperator( '-a20 2222222223333333778 show_persistence' )

    # square_digit_chain
    testOperator( '12345 square_digit_chain' )

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

    # and_all
    testOperator( '[ 1 0 1 1 1 1 0 1 ] and_all' )

    expectResult( '[ 1 0 1 1 1 1 0 1 ] and_all', 0 )
    expectResult( '[ 1 1 1 1 1 1 1 1 ] and_all', 1 )

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
    expectResult( '1 10 range 5 element', 6 )
    testOperator( '-a25 1 100 range fibonacci 55 element' )

    # enumerate
    testOperator( '1 5 range 1 enumerate' )

    # exponential_range
    testOperator( '1.1 1.1 10 exponential_range' )

    # find
    testOperator( '1 10 range 4 find' )

    # flatten
    expectEqual( '[ 1 2 [ 3 4 5 ] [ 6 [ 7 [ 8 9 ] ] 10 ] ] flatten', '1 10 range' )

    # geometric_mean
    testOperator( '1 1 10 range range geometric_mean' )
    testOperator( '1 100 range geometric_mean' )
    testOperator( '[ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    # geometric_range
    testOperator( '2 8 8 geometric_range' )

    # get_combinations
    testOperator( '[ 1 2 3 4 ] 2 get_combinations' )

    # get_repeat_combinations
    testOperator( '[ 1 2 3 4 ] 2 get_repeat_combinations' )

    # get_permutations
    testOperator( '[ 1 2 3 4 ] 2 get_permutations' )

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

    # nand_all
    testOperator( '[ 1 0 1 1 1 1 0 1 ] nand_all' )

    # nonzero
    expectEqual( '1 10 range nonzero', '0 9 range' )

    # nor_all
    testOperator( '[ 1 0 1 1 1 1 0 1 ] nor_all' )

    # occurrences
    testOperator( '4 100 random_integer_ occurrences' )

    # occurrence_cumulative
    testOperator( '4 100 random_integer_ occurrence_cumulative' )

    # occurrence_ratios
    testOperator( '4 100 random_integer_ occurrence_ratios' )

    # or_all
    testOperator( '[ 1 0 1 1 1 1 0 1 ] or_all' )

    expectResult( '[ 0 0 0 0 0 0 0 0 ] or_all', 0 )
    expectResult( '[ 1 0 1 1 1 1 0 1 ] or_all', 1 )
    expectResult( '[ 1 1 1 1 1 1 1 1 ] or_all', 1 )

    # permute_lists
    testOperator( '[ [ 1 2 3 4 ] [ 5 6 7 8 ] [ 9 10 11 12 ] ] permute_lists' )

    # powerset
    testOperator( '1 5 range powerset' )

    # right
    testOperator( '1 10 range random_element' )
    testOperator( '[ 1 10 range 11 20 range 21 30 range ] random_element' )

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
    testOperator( '10 1 10 range 10 sized_range -s1' )
    testOperator( '1 10 range 1 10 range 10 sized_range -s1' )

    expectResult( '10 10 10 sized_range', [ 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ] )

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
    expectEqual( '-a5005 phi log 10 5002 ** * get_digits 5000 left', '2390 oeis 5000 left' )

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
# //  runLogicOperatorTests
# //
# //******************************************************************************

def runLogicOperatorTests( ):
    # and
    testOperator( '1 1 and' )

    # nand
    testOperator( '1 1 nand' )

    # nor
    testOperator( '1 1 nor' )

    # not
    expectEqual( '[ 0 10 dup ] not', '[ 1 10 dup ]' )

    # or
    testOperator( '1 1 or' )

    # xnor
    testOperator( '1 1 xnor' )

    # xor
    testOperator( '1 1 xor' )


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

    # duplicate_operator
    testOperator( '2 5 duplicate_operator sqr' )
    testOperator( '4 6 5 duplicate_operator *' )

    # duplicate_term
    testOperator( '[ 1 2 10 duplicate_term ] cf' )

    # previous
    expectResult( '6 previous *', 36 )

    # unlist
    expectResult( '[ 1 2 ] unlist +', 3 )

    # (
    testOperator( '"Leesburg, VA" today ( sunrise sunset moonrise moonset )' )

    # )
    testOperator( '1 10 range ( is_prime is_pronic is_semiprime )' )


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    from rpn.rpnNumberTheory import getNthKFibonacciNumberTheSlowWay

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

    # cf
    testOperator( '1 10 range cf' )

    # collatz
    testOperator( '127 10 collatz' )

    # count_divisors
    testOperator( '1024 count_divisors' )

    expectEqual( '1 104 range count_divisors', '5 oeis 104 left' )
    expectEqual( '-a50 0 35 range ! count_divisors', '-a50 27423 oeis 36 left' )

    # crt
    testOperator( '1 4 range 10 20 3 range2 crt' )

    expectResult( '[ 2 3 2 ] [ 3 5 7 ] crt', 23 )

    # cyclotomic

    # digamma
    testOperator( '3 digamma' )
    testOperator( '-1.1 digamma' )

    expectEqual( '-a110 1 8 / digamma negative 10 107 ** * get_digits 105 left', '250129 oeis 105 left' )

    expectException( '0 digamma' )
    expectException( '-1 digamma' )

    # digital_root

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

    expectEqual( '1 100 range euler_phi', '10 oeis 100 left' )

    if slow:
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
    testOperator( '2.5 factorial' )

    expectEqual( '0 100 range !', '142 oeis 101 left' )
    expectEqual( '0 100 range lambda x 2 * ! x 2 * 1 + ! * x ! sqr / eval', '909 oeis 101 left' )
    expectEqual( '1 99 range lambda 3 2 x * ! * x 2 + ! x 1 - ! * / eval', '245 oeis 100 left 99 right' )
    expectEqual( '-a20 1 8 range lambda 0 x range 3 * 1 + factorial 0 x range x + factorial divide prod eval', '36687 oeis 9 left 8 right' )

    expectException( '-1 factorial' )

    # fibonacci
    testOperator( '1 50 range fibonacci' )
    testOperator( '-c -a8300 39399 fibonacci' )

    expectEqual( '0 99 range fibonacci', '45 oeis 100 left' )

    if slow:
        expectEqual( '0 999 range fibonacci', '45 oeis 1000 left' )

    expectResult( '0 100 range fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )

    # fibonorial
    testOperator( '5 fibonorial' )
    testOperator( '-a50 24 fibonorial' )

    expectEqual( '1 100 range fibonorial', '3266 oeis 100 left' )

    # fraction
    testOperator( '2 sqrt 30 fraction' )
    # NOTE: fraction should be setting dps itself!

    expectEqual( '-p250 2 sqrt 2 199 range fraction flatten lambda x is_even filter_by_index', '1333 oeis 200 left 198 right' )
    expectEqual( '-p250 5 sqrt 2 200 range fraction flatten lambda x is_odd filter_by_index', '1076 oeis 201 left 199 right' )

    # frobenius
    testOperator( '10 20 3 range2 prime frobenius' )

    expectEqual( '2 1001 range lambda x 1 5 sized_range frobenius eval', '138985 oeis 1000 left' )
    expectEqual( '2 59 range lambda x 1 6 sized_range frobenius eval', '138986 oeis 58 left' )
    expectEqual( '2 60 range lambda x 1 7 sized_range frobenius eval', '138987 oeis 59 left' )
    expectEqual( '2 60 range lambda x 1 8 sized_range frobenius eval', '138988 oeis 59 left' )
    expectEqual( '1 999 range lambda x 2 primes frobenius eval', '37165 oeis 999 left' )
    expectEqual( '1 46 range lambda x 3 primes frobenius eval', '138989 oeis 46 left' )
    expectEqual( '1 1000 range lambda x 4 primes frobenius eval', '138990 oeis 1000 left' )
    expectEqual( '1 48 range lambda x 5 primes frobenius eval', '138991 oeis 48 left' )
    expectEqual( '1 49 range lambda x 6 primes frobenius eval', '138992 oeis 49 left' )
    expectEqual( '1 50 range lambda x 7 primes frobenius eval', '138993 oeis 50 left' )
    expectEqual( '1 50 range lambda x 8 primes frobenius eval', '138994 oeis 50 left' )
    expectEqual( '2 100 range lambda [ x x 1 + x 2 + ] triangular frobenius eval', '69755 oeis 99 left' )
    expectEqual( '3 30 range lambda [ x x 1 + ] fib frobenius eval', '59769 oeis 28 left' )

    if slow:
        expectEqual( '2 1000 range lambda [ x x 1 + x 2 + ] triangular frobenius eval', '69755 oeis 999 left' )

    # gamma
    testOperator( '3 gamma' )

    # generate_polydivisibles
    testOperator( '3 generate_polydivisibles -r3' )

    expectEqual( '2 9 range lambda x generate_polydivisibles count eval', '271374 oeis 8 left' )

    # geometric_recurrence
    expectEqual( '-a800 [ 1 1 ] [ 2 2 ] [ 0 1 ] 15 geometric_recurrence', '-a800 283 oeis 15 left' )
    expectEqual( '-a800 [ 1 1 ] [ 3 1 ] [ 0 1 ] 18 geometric_recurrence', '280 oeis 18 left' )
    expectEqual( '-a800 [ 1 1 ] [ 2 1 ] [ 0 1 ] 25 geometric_recurrence', '278 oeis 25 left' )
    expectEqual( '-a800 [ 1 1 ] [ 1 3 ] [ 0 1 ] 11 geometric_recurrence', '284 oeis 11 left' )

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

    expectEqual( '1 1000 range lambda x is_abundant filter', '5101 oeis lambda x 1000 is_not_greater filter' )

    if slow:
        expectEqual( '1 4038 range lambda x is_abundant filter', '5101 oeis 1000 left' )

    # is_achilles
    testOperator( '1 20 range is_achilles' )

    expectEqual( '1 500 range lambda x is_achilles filter', '52486 oeis lambda x 500 is_not_greater filter' )

    # is_carmichael
    expectEqual( '1 10000 2 interval_range lambda x is_carmichael filter', '2997 oeis 7 left' )

    expectResult( '-a15 2997 oeis 200 left is_carmichael and_all', 1 )

    if slow:
        expectResult( '2997 oeis is_carmichael and_all', 1 )

    # is_composite
    expectEqual( '1 161 range lambda x is_squarefree x is_composite and filter', '120944 oeis 61 left' )

    # is_deficient
    testOperator( '1 20 range is_deficient' )

    expectEqual( '1 86 range lambda x is_deficient filter', '5100 oeis 66 left' )

    # is_friendly
    testOperator( '[ 220 264 ] is_friendly' )

    # is_k_hyperperfect
    expectEqual( '1 2100 range lambda x 12 is_k_hyperperfect filter', '[ 697 2041 ]' )

    # is_k_semiprime
    testOperator( '1 20 range 3 is_k_semiprime' )

    expectEqual( '-a30 1 100 range lambda x tribonacci is_semiprime filter', '101757 oeis lambda x 100 is_not_greater filter' )

    # is_k_sphenic
    testOperator( '30 3 is_k_sphenic' )

    expectResult( '210 4 is_k_sphenic', 1 )

    # is_perfect
    testOperator( '1 30 range is_perfect' )

    # is_polydivisible
    expectResult( '3608528850368400786036725 is_polydivisible', 1 )

    # is_powerful
    testOperator( '1 20 range is_powerful' )

    expectEqual( '1 1000 range lambda x is_powerful filter', '1694 oeis 54 left' )

    if slow:
        expectEqual( '1 100000 range lambda x is_powerful filter', '1694 oeis 619 left' )

    # is_prime
    testOperator( '1000 1030 range is_prime' )
    testOperator( '2049 is_prime' )
    testOperator( '92348759911 is_prime' )

    expectResult( '-a700 1 16 range nth_mersenne_prime is_prime and_all', 1 )

    expectEqual( '0 300 range lambda 90 x * 73 + is_prime filter 100 left', '195993 oeis 100 left' )

    # is_pronic
    testOperator( '1 20 range is_pronic' )

    expectEqual( '0 9900 range lambda x is_pronic filter', '2378 oeis 100 left' )

    # is_rough
    testOperator( '1 20 range 2 is_rough' )

    expectEqual( '1 500 range lambda x 11 is_rough filter', '8364 oeis lambda x 500 is_not_greater filter' )
    expectEqual( '1 500 range lambda x 19 is_rough filter', '166061 oeis lambda x 500 is_not_greater filter' )
    expectEqual( '1 500 range lambda x 23 is_rough filter', '166063 oeis lambda x 500 is_not_greater filter' )

    expectException( '1 20 range 12 is_rough' )

    if slow:
        expectEqual( '1 43747 range lambda x 11 is_rough filter', '8364 oeis 10000 left 9999 right' )

    # is_ruth_aaron
    testOperator( '1 20 range is_ruth_aaron' )

    expectEqual( '1 1000 range lambda x is_ruth_aaron filter', '39752 oeis lambda x 1000 is_not_greater filter' )

    # is_semiprime
    testOperator( '12 is_semiprime' )

    expectEqual( '1 205 range lambda x is_semiprime x is_squarefree and filter', '6881 oeis 60 left' )
    expectEqual( ' 1 141 range lambda x is_semiprime x is_squarefree and filter square', '85986 oeis 41 left' )

    # is_smooth
    testOperator( '128 3 is_smooth' )
    testOperator( '1 20 range 5 is_smooth' )

    expectEqual( '1 500 range lambda x 3 is_smooth filter', '3586 oeis lambda x 500 is_not_greater filter' )
    expectEqual( '1 500 range lambda x 7 is_smooth filter', '2473 oeis lambda x 500 is_not_greater filter' )
    expectEqual( '1 500 range lambda x 17 is_smooth filter', '80681 oeis lambda x 500 is_not_greater filter' )

    expectException( '1 20 range 12 is_smooth' )

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
    expectEqual( '1 1000 range lambda x is_prime not x is_squarefree and filter', '469 oeis 440 left' )

    if slow:
        expectEqual( '1 20203 range lambda x is_prime not x is_squarefree and filter', '469 oeis 10000 left' )

    # is_strong_pseudoprime
    expectResult( '1543267864443420616877677640751301 1 19 primes is_strong_pseudoprime and_all', 1 )

    expectEqual( '1 100000 range lambda x 2 is_strong_pseudoprime filter', '1262 oeis 16 left' )
    expectEqual( '1 100000 range lambda x 3 is_strong_pseudoprime filter', '20229 oeis 23 left' )
    expectEqual( '1 100000 range lambda x 4 is_strong_pseudoprime filter', '20230 oeis 31 left' )
    expectEqual( '1 100000 range lambda x 5 is_strong_pseudoprime filter', '20231 oeis 16 left' )
    expectEqual( '1 100000 range lambda x 6 is_strong_pseudoprime filter', '20232 oeis 30 left' )
    expectEqual( '1 100000 range lambda x 7 is_strong_pseudoprime filter', '20233 oeis 21 left' )
    expectEqual( '1 100000 range lambda x 8 is_strong_pseudoprime filter', '20234 oeis 44 left' )

    expectResult( '1262 oeis 2 is_strong_pseudoprime and_all', 1 )
    expectResult( '20229 oeis 3 is_strong_pseudoprime and_all', 1 )
    expectResult( '20230 oeis 4 is_strong_pseudoprime and_all', 1 )
    expectResult( '20231 oeis 5 is_strong_pseudoprime and_all', 1 )
    expectResult( '20232 oeis 6 is_strong_pseudoprime and_all', 1 )
    expectResult( '20233 oeis 7 is_strong_pseudoprime and_all', 1 )
    expectResult( '20234 oeis 8 is_strong_pseudoprime and_all', 1 )

    # is_unusual
    testOperator( '-a50 81 23 ** is_unusual' )
    testOperator( '1 20 range is_unusual' )

    expectEqual( '1 1389 range lambda x is_unusual filter', '64052 oeis 1000 left' )

    # k_fibonacci
    expectResult( '0 100 range 2 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 5 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )
    expectResult( '0 100 range 10 k_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 10 ) for i in range( 0, 101 ) ] )
    expectResult( '1000 10 k_fibonacci', getNthKFibonacciNumberTheSlowWay( 1000, 10 ) )

    # leyland
    testOperator( '7 8 leyland' )

    expectEqual( '-a121 [ 2 60 range 2 60 range ] permute_lists lambda x y leyland for_each unique 76980 oeis intersection sort',
                 '-a121 [ 2 60 range 2 60 range ] permute_lists lambda x y leyland for_each unique sort' )

    # linear_recurrence
    testOperator( '2 5 17 linear_recurrence' )

    expectEqual( '-a50 [ 1 -1 -2 3 ] [ 1 2 4 8 ] 200 linear_recurrence', '-a50 126 oeis 200 left' )
    expectEqual( '-a50 [ -1, 2, 1, -5 4 ] [ 1, 2, 4, 8, 16 ] 201 linear_recurrence', '-a50 128 oeis 201 left' )

    # linear_recurrence_with_modulo

    # log_gamma
    testOperator( '10 log_gamma' )

    # lucas
    testOperator( '-a21 99 lucas' )

    expectEqual( '0 999 range lucas', '32 oeis 1000 left' )

    # make_cf
    testOperator( 'e 20 make_cf' )

    expectEqual( '-a100 2 pi * 3 2 / power 1/x 1 4 / gamma sqr * 100 make_cf', '53002 oeis 100 left' )
    expectEqual( '-a130 phi phi sqr 4 + sqrt + 2 / 116 make_cf', '188635 oeis 116 left' )
    expectEqual( '-a2050 pi 2000 make_cf', '1203 oeis 2000 left' )

    if slow:
        expectEqual( '-a21000 pi 20000 make_cf', '1203 oeis 20000 left' )

    # make_pyth_3
    testOperator( '12 34 make_pyth_3' )

    # make_pyth_4
    testOperator( '18 29 make_pyth_4' )

    expectException( '17 29 make_pyth_4' )

    # merten
    testOperator( '1 10 range merten' )

    expectEqual( '1 81 range merten', '2321 oeis 81 left' )

    # mobius
    testOperator( '20176 mobius' )

    expectEqual( '1 1000 range mobius', '8683 oeis 1000 left' )

    if slow:
        expectEqual( '1 10000 range mobius', '8683 oeis 10000 left' )

    # nth_carol
    testOperator( '-a500 -c 773 nth_carol' )

    expectEqual( '1 25 range nth_carol', '93112 oeis 25 left' )

    # nth_jacobsthal
    testOperator( '1 10 range nth_jacobsthal' )

    expectEqual( '-a302 0 999 range nth_jacobsthal', '1045 oeis 1000 left' )

    if slow:
        expectEqual( '-a1002 0 3316 range nth_jacobsthal', '1045 oeis 3317 left' )

    # nth_kynea
    testOperator( '1 10 range nth_kynea' )

    expectEqual( '-a20 1 25 range nth_kynea', '93069 oeis 25 left' )

    # nth_leonardo
    testOperator( '1 10 range nth_leonardo' )

    expectEqual( '-a106 0 499 range nth_leonardo', '1595 oeis 500 left' )

    # nth_mersenne_exponent
    testOperator( '1 10 range nth_mersenne_exponent' )

    # nth_mersenne_prime
    testOperator( '-a30 1 10 range nth_mersenne_prime' )
    testOperator( '-c 25 nth_mersenne_prime' )

    # nth_padovan
    testOperator( '-c 76 nth_padovan' )

    expectEqual( '0 99 range nth_padovan', '931 oeis 104 left 100 right' )

    # nth_perfect_number
    testOperator( '12 nth_perfect_number' )

    expectEqual( '1 14 range nth_perfect_number', '396 oeis 14 left' )

    # nth_stern
    testOperator( '1 100 range nth_stern' )

    expectEqual( '0 99 range nth_stern', '2487 oeis 100 left' )

    if slow:
        expectEqual( '0 9999 range nth_stern', '2487 oeis 10000 left' )

    # nth_thue_morse
    testOperator( '1 10 range nth_thue_morse' )

    expectEqual( '0 104 range nth_thue_morse', '10060 oeis 105 left' )

    # octanacci
    testOperator( '-a300 -c 906 octanacci' )

    expectEqual( '0 99 range octanacci', '79262 oeis 100 left' )

    expectResult( '0 100 range octanacci', [ getNthKFibonacciNumberTheSlowWay( i, 8 ) for i in range( 0, 101 ) ] )

    # pascal_triangle
    testOperator( '12 pascal_triangle' )
    testOperator( '1 10 range pascal_triangle -s1' )

    expectEqual( '1 142 range pascal_triangle flatten', '7318 oeis 10153 left' )

    # pentanacci
    testOperator( '16 pentanacci' )

    expectEqual( '0 99 range pentanacci', '1591 oeis 100 left' )

    expectResult( '0 100 range pentanacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )

    # polygamma
    testOperator( '4 5 polygamma' )

    expectEqual( '-a105 1 1 5 sqrt + 4 / polygamma 1 3 5 sqrt + 4 / polygamma - 2 / 10 105 ** * get_digits 102 left', '91659 oeis 102 left' )

    # primorial
    testOperator( '1 10 range primorial' )

    expectEqual( '-a22 0 99 range primorial', '-a22 2110 oeis 100 left' )

    # radical
    testOperator( '1 10 range radical' )

    # repunit
    testOperator( '-a20 23 5 repunit' )

    expectEqual( '-a300 1 250 range 15 repunit', '135518 oeis 250 left' )
    expectEqual( '-a300 1 250 range 14 repunit', '135519 oeis 250 left' )

    if slow:
        expectEqual( '-a1000 1 873 range 14 repunit', '135519 oeis 873 left' )

    # reversal_addition
    testOperator( '-a20 89 24 reversal_addition' )
    testOperator( '-a20 80 89 range 24 reversal_addition' )
    testOperator( '-a20 89 16 24 range reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition' )
    testOperator( '-a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    expectEqual( '-a120 1000004999700144385 260 reversal_addition', '-a120 281301 oeis 260 left' )

    # riesel
    testOperator( '23 riesel' )

    expectEqual( '-a100 1 300 range riesel', '3261 oeis 300 left' )

    # sigma
    testOperator( '1 20 range sigma' )

    expectEqual( '1 500 range sigma', '203 oeis 500 left' )
    expectEqual( '1 499 range lambda x sigma 8 * 32 x 4 / sigma * 0 x 4 / is_integer if - eval', '118 oeis 500 left 499 right' )

    if slow:
        expectEqual( '1 100000 range sigma', '203 oeis 100000 left' )
        expectEqual( '1 49999 range lambda x sigma 8 * 32 x 4 / sigma * 0 x 4 / is_integer if - eval', '118 oeis 50000 left 49999 right' )

    # sigma_k
    testOperator( '1 20 3 range sigma_k' )

    expectEqual( '1 50 range 2 sigma_k', '1157 oeis 50 left' )
    expectEqual( '-p30 1 100 range 3 sigma_k', '1158 oeis 100 left' )
    expectEqual( '-p30 1 100 range 4 sigma_k', '1159 oeis 100 left' )
    expectEqual( '-p30 1 100 range 5 sigma_k', '1160 oeis 100 left' )
    expectEqual( '-p30 1 100 range 6 sigma_k', '13954 oeis 100 left' )
    expectEqual( '-p30 1 100 range 7 sigma_k', '13955 oeis 100 left' )
    expectEqual( '-p30 1 100 range 8 sigma_k', '13956 oeis 100 left' )
    expectEqual( '-p35 1 100 range 9 sigma_k', '13957 oeis 100 left' )
    expectEqual( '-p35 1 100 range 10 sigma_k', '13958 oeis 100 left' )
    expectEqual( '-p40 1 100 range 11 sigma_k', '13959 oeis 100 left' )
    expectEqual( '-p45 1 100 range 12 sigma_k', '13960 oeis 100 left' )
    expectEqual( '-p45 1 100 range 13 sigma_k', '13961 oeis 100 left' )
    expectEqual( '-p45 1 100 range 14 sigma_k', '13962 oeis 100 left' )
    expectEqual( '-p50 1 100 range 15 sigma_k', '13963 oeis 100 left' )
    expectEqual( '-p55 1 100 range 16 sigma_k', '13964 oeis 100 left' )
    expectEqual( '-p65 1 100 range 17 sigma_k', '13965 oeis 100 left' )
    expectEqual( '-p75 1 100 range 18 sigma_k', '13966 oeis 100 left' )
    expectEqual( '-p80 1 100 range 19 sigma_k', '13967 oeis 100 left' )
    expectEqual( '-p85 1 100 range 20 sigma_k', '13968 oeis 100 left' )
    expectEqual( '-p90 1 100 range 21 sigma_k', '13969 oeis 100 left' )
    expectEqual( '-p95 1 100 range 22 sigma_k', '13970 oeis 100 left' )
    expectEqual( '-p100 1 100 range 23 sigma_k', '13971 oeis 100 left' )
    expectEqual( '-p100 1 100 range 24 sigma_k', '13972 oeis 100 left' )

    if slow:
        expectEqual( '-p30 1 1000 range 3 sigma_k', '1158 oeis 1000 left' )
        expectEqual( '-p30 1 1000 range 4 sigma_k', '1159 oeis 1000 left' )
        expectEqual( '-p35 1 1000 range 5 sigma_k', '1160 oeis 1000 left' )
        expectEqual( '-p35 1 1000 range 6 sigma_k', '13954 oeis 1000 left' )
        expectEqual( '-p45 1 1000 range 7 sigma_k', '13955 oeis 1000 left' )
        expectEqual( '-p50 1 1000 range 8 sigma_k', '13956 oeis 1000 left' )
        expectEqual( '-p55 1 1000 range 9 sigma_k', '13957 oeis 1000 left' )
        expectEqual( '-p60 1 1000 range 10 sigma_k', '13958 oeis 1000 left' )
        expectEqual( '-p65 1 1000 range 11 sigma_k', '13959 oeis 1000 left' )
        expectEqual( '-p70 1 999 range 12 sigma_k', '13960 oeis 999 left' )
        expectEqual( '-p80 1 999 range 13 sigma_k', '13961 oeis 999 left' )
        expectEqual( '-p85 1 999 range 14 sigma_k', '13962 oeis 999 left' )
        expectEqual( '-p90 1 999 range 15 sigma_k', '13963 oeis 999 left' )
        expectEqual( '-p95 1 999 range 16 sigma_k', '13964 oeis 999 left' )
        expectEqual( '-p100 1 999 range 17 sigma_k', '13965 oeis 999 left' )
        expectEqual( '-p200 1 10000 range 18 sigma_k', '13966 oeis 10000 left' )
        expectEqual( '-p210 1 10000 range 19 sigma_k', '13967 oeis 10000 left' )
        expectEqual( '-p220 1 10000 range 20 sigma_k', '13968 oeis 10000 left' )
        expectEqual( '-p230 1 10000 range 21 sigma_k', '13969 oeis 10000 left' )
        expectEqual( '-p240 1 10000 range 22 sigma_k', '13970 oeis 10000 left' )
        expectEqual( '-p250 1 10000 range 23 sigma_k', '13971 oeis 10000 left' )
        expectEqual( '-p260 1 10000 range 24 sigma_k', '13972 oeis 10000 left' )

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

    expectResult( '0 100 range tetranacci', [ getNthKFibonacciNumberTheSlowWay( i, 4 ) for i in range( 0, 101 ) ] )

    expectEqual( '0 99 range tetranacci', '78 oeis 100 left' )

    # thabit
    testOperator( '-a20 -c 45 thabit' )

    expectEqual( '0 998 range thabit', '55010 oeis 1000 left 999 right' )

    # tribonacci
    testOperator( '1 20 range tribonacci' )
    testOperator( '-c -a2800 10239 tribonacci' )

    expectResult( '0 100 range tribonacci', [ getNthKFibonacciNumberTheSlowWay( i, 3 ) for i in range( 0, 101 ) ] )

    expectEqual( '0 99 range tribonacci', '73 oeis 100 left' )

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
    # distance
    testOperator( '10 feet 10 seconds distance' )   # trivial version
    testOperator( '65 mph 10 seconds distance' )
    testOperator( 'gee 10 seconds distance' )
    testOperator( '10 m/s^3 10 seconds distance' )
    testOperator( '10 m/s^4 10 seconds distance' )

    # black_hole_entropy
    testOperator( 'sun_mass black_hole_entropy' )
    testOperator( '1 square_centimeter black_hole_entropy' )
    testOperator( 'earth_gravity black_hole_entropy' )
    testOperator( '100 kelvin black_hole_entropy' )
    testOperator( '1 watt black_hole_entropy' )
    testOperator( '1 trillion years black_hole_entropy' )
    testOperator( '1 angstrom years black_hole_entropy' )

    # black_hole_lifetime
    testOperator( '1.0e100 years black_hole_lifetime' )
    testOperator( 'sun_mass black_hole_lifetime' )
    testOperator( '1 square_centimeter black_hole_lifetime' )
    testOperator( 'earth_gravity black_hole_lifetime' )
    testOperator( '1 kelvin black_hole_lifetime' )
    testOperator( '1.5 PW black_hole_lifetime' )
    testOperator( '100 miles black_hole_lifetime' )

    # black_hole_luminosity
    testOperator( '1 gram black_hole_luminosity' )
    testOperator( '10 square_miles black_hole_luminosity' )
    testOperator( 'earth_gravity black_hole_luminosity' )
    testOperator( '273.16 kelvin black_hole_luminosity' )
    testOperator( '1 day black_hole_luminosity' )
    testOperator( '1000 miles black_hole_luminosity' )
    testOperator( '1.0e20 W black_hole_mass' )

    # black_hole_mass
    testOperator( '1000 watts black_hole_mass' )
    testOperator( '1 barn black_hole_mass' )
    testOperator( '1000000 meters/second^2 black_hole_mass' )
    testOperator( '1.0e12 kelvin black_hole_mass' )
    testOperator( '1 quadrillion years black_hole_mass' )
    testOperator( '1 millimeter black_hole_mass' )
    testOperator( '1 horsepower black_hole_mass' )

    # black_hole_radius
    testOperator( '1 mile black_hole_radius' )
    testOperator( 'earth_mass black_hole_radius' )
    testOperator( '100 square_miles black_hole_radius' )
    testOperator( '10 gee black_hole_radius' )
    testOperator( '10000 kelvin black_hole_radius' )
    testOperator( '1 TW black_hole_radius' )
    testOperator( '1 billion years black_hole_radius' )

    # black_hole_temperature
    testOperator( '50 K black_hole_temperature' )
    testOperator( '1e20 watts black_hole_temperature' )
    testOperator( '1 square_light-year black_hole_temperature' )
    testOperator( '1.0e-9 meters/second^2 black_hole_temperature' )
    testOperator( '1.0e15 kg black_hole_temperature' )
    testOperator( '1 minute black_hole_temperature' )
    testOperator( '1 mile black_hole_temperature' )

    # black_hole_surface_area
    testOperator( '1 acre black_hole_surface_area' )
    testOperator( '1e20 watts black_hole_surface_area' )
    testOperator( '1 K black_hole_surface_area' )
    testOperator( '1.0e25 meters/second^2 black_hole_surface_area' )
    testOperator( '1.0e-15 kg black_hole_surface_area' )
    testOperator( '1 hour black_hole_surface_area' )
    testOperator( '1 parsec black_hole_surface_area' )

    # black_hole_surface_gravity
    testOperator( 'moon_gravity black_hole_surface_gravity' )
    testOperator( '1e25 watts black_hole_surface_gravity' )
    testOperator( '1e12 K black_hole_surface_gravity' )
    testOperator( '1.0e30 meters/second^2 black_hole_surface_gravity' )
    testOperator( '1.0e20 kg black_hole_surface_gravity' )
    testOperator( '1 quintillion years black_hole_surface_gravity' )
    testOperator( '1 foot black_hole_surface_gravity' )

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
    testOperator( '4 [ 5 7 9 ] power' )
    testOperator( '4 1 6 range power' )
    testOperator( '[ 5 7 9 ] 4 power' )
    testOperator( '1 6 4 range power' )
    testOperator( '[ 5 7 9 ] [ 2 3 4 ] power' )
    testOperator( '3 5 range [ 2 3 4 ] power' )
    testOperator( '[ 2 3 4 ] 3 5 range power' )
    testOperator( '2 4 range 3 5 range power' )
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

    # power_tower
    testOperator( '-c -a30 [ 2 3 2 ] power_tower' )
    testOperator( '[ [ 2 5 4 ] [ 3 2 4 ] [ 3 2 2 ] ] power_tower' )
    testOperator( '[ 2 3 range 2 4 range ] power_tower' )
    testOperator( '[ 1 i 1 i 1 i 1 i 1 i 1 i ] power_tower' )

    # power_tower2
    testOperator( '-a160 -c [ 4 4 4 ] power_tower2' )
    testOperator( '[ [ 2 5 4 ] [ 3 2 4 ] [ 3 2 2 ] ] power_tower2' )
    testOperator( '[ 2 3 range 2 4 range ] power_tower2' )
    testOperator( '[ 1 i 1 i 1 i 1 i 1 i 1 i ] power_tower2' )

    # powmod
    testOperator( '43 67 9 powmod' )

    # pseudoprimes to base 2
    expectEqual( '3 100000 2 range2 lambda x is_prime not filter lambda 2 x 1 - x powmod 1 equals filter',
                 '1567 oeis lambda x 100000 is_less filter' )
    # pseudoprimes to base 3
    expectEqual( '2 50000 range lambda x is_prime not filter lambda 3 x 1 - x powmod 1 equals filter',
                 '5935 oeis lambda x 50000 is_less filter' )
    # pseudoprimes to base 4
    expectEqual( '2 50000 range lambda x is_prime not filter lambda 4 x 1 - x powmod 1 equals filter',
                 '20136 oeis lambda x 50000 is_less filter' )
    # pseudoprimes to base 5
    expectEqual( '2 50000 range lambda x is_prime not filter lambda 5 x 1 - x powmod 1 equals filter',
                 '5936 oeis lambda x 50000 is_less filter' )
    # pseudoprimes to base 6
    expectEqual( '2 50000 range lambda x is_prime not filter lambda 6 x 1 - x powmod 1 equals filter',
                 '5937 oeis lambda x 50000 is_less filter' )
    # psuedoprimes to base 100
    expectEqual( '2 50000 range lambda x is_prime not filter lambda 100 x 1 - x powmod 1 equals filter',
                 '20228 oeis lambda x 50000 is_less filter' )

    expectException( '9 i 6 4 powmod' )
    expectException( '3 12 i 5 powmod' )
    expectException( '21 33 67 i powmod' )

    # root
    testOperator( '4 3 root' )
    testOperator( '4 i 6 + 3 root' )

    expectResult( '8 0.5 root', 64 )

    expectEqual( '8 3 root', '8 cube_root' )

    # square
    expectEqual( '123 square', '123 123 *' )

    # square_root
    expectEqual( '2 square_root', '4 4 root' )

    if g.primeDataAvailable:
        expectEqual( '1 10000 primes sqrt floor', '6 oeis 10000 left' )

    # tetrate
    testOperator( '3 2 tetrate' )


# //******************************************************************************
# //
# //  runPrimeNumberOperatorTests
# //
# //******************************************************************************

def runPrimeNumberOperatorTests( ):
    if not g.primeDataAvailable:
        return

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

    expectEqual( '-a202 0 199 range lambda 10 x ** next_prime 10 x ** - eval', '33873 oeis 200 left' )

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

    # previous_prime
    testOperator( '10 previous_prime' )

    # previous_primes
    testOperator( '1000 100 previous_primes' )

    expectEqual( '220 47 previous_primes sort', '1 47 primes' )
    expectEqual( '-a202 1 200 range lambda 10 x ** previous_prime 10 x ** - eval neg', '33874 oeis 200 left' )

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
    #expectEqual( '1 39 range lambda x sexy_quadruplet_ 3 element eval', '46124 oeis 39 left' )

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
    # base_units
    testOperator( '10 MeV c sqr / base_units' )

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
    testOperator( '150 gee estimate' )
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

    # describe
    # Note: the cache is turned off, so only test really small numbers
    testOperator( '1 describe' )
    testOperator( '10 describe' )
    testOperator( '121 describe' )

    # dimensions
    testOperator( '10 MeV c sqr / dimensions' )

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
    testOperator( '2000 oeis' )

    # oeis_comment
    testOperator( '2000 oeis_comment' )

    # oeis_ex
    testOperator( '2000 oeis_ex' )

    # oeis_name
    testOperator( '2000 oeis_name' )

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

    expectEqual( '-a105 2 pi / acos 10 103 ** * get_digits 102 left', '275477 oeis 102 left' )
    expectEqual( '-a110 -1 4 / acos 10 107 ** * get_digits 105 left', '140244 oeis 105 left' )
    expectEqual( '-a110 180 -1 4 / acos * pi / 10 107 ** * get_digits 105 left', '140245 oeis 105 left' )
    expectEqual( '-a110 7 8 / acos 10 107 ** * get_digits 105 left', '140240 oeis 105 left' )
    expectEqual( '-a110 180 7 8 / acos * pi / 10 107 ** * get_digits 105 left', '140241 oeis 105 left' )
    expectEqual( '-a110 11 16 / acos 10 107 ** * get_digits 105 left', '140242 oeis 105 left' )
    expectEqual( '-a110 180 11 16 / acos * pi / 10 107 ** * get_digits 105 left', '140243 oeis 105 left' )

    # acosh
    testOperator( '0.6 acosh' )

    expectEqual( '-a1005 2 sqrt acosh 10 1001 ** * get_digits 1001 left', '91648 oeis 1001 left' )

    # acot
    testOperator( '0.4 acot' )

    expectEqual( '-a105 9 acot 10 101 ** * get_digits 100 left', '195786 oeis 100 left' )
    expectEqual( '-a105 10 acot 10 101 ** * get_digits 99 left', '195790 oeis 100 left 99 right' )

    # acoth
    testOperator( '0.3 acoth' )

    expectEqual( '-a110 3 4 / 3 sqrt * 3 sqrt acoth * 10 108 ** * get_digits 100 left', '257436 oeis 100 left' )

    # acsc
    testOperator( '0.2 acsc' )

    expectEqual( '-a105 9 acsc 10 101 ** * get_digits 100 left', '195788 oeis 100 left' )
    expectEqual( '-a105 8 acsc 10 101 ** * get_digits 100 left', '195784 oeis 100 left' )

    # acsch
    testOperator( '0.67 acsch' )

    expectEqual( '-a110 2 5 sqrt * 5 / 2 acsch * 10 108 ** * get_digits 102 left', '86466 oeis 102 left' )

    # asec
    testOperator( '0.4 asec' )

    expectEqual( '-a105 9 asec 10 101 ** * get_digits 100 left', '195787 oeis 100 left' )
    expectEqual( '-a105 8 asec 10 101 ** * get_digits 100 left', '195783 oeis 100 left' )

    # asech
    testOperator( '0.1 asech' )

    # asin
    testOperator( '0.8 asin' )

    expectEqual( '-a40 0 1000 range lambda x asin x acos - sin sqr eval', '239607 oeis 1001 left' )

    # asinh
    testOperator( '0.3 asinh' )

    expectEqual( '-a5005 2 2 sqrt + 1 asinh 5 * + 15 / 10 5002 ** * get_digits 5001 left', '91505 oeis 5001 left' )

    # atan
    testOperator( '0.2 atan' )

    expectEqual( '-a2005 e atan 10 2002 ** * get_digits 2000 left', '257777 oeis 2000 left' )
    expectEqual( '-a2005 1 e / atan 10 2002 ** * get_digits 2000 left', '258428 oeis 2000 left' )
    expectEqual( '-a2005 pi e atan - 2 pi * / 10 2002 ** * get_digits 2000 left', '257896 oeis 2000 left' )
    expectEqual( '-a105 10 atan 10 101 ** * get_digits 100 left', '195789 oeis 100 left' )
    expectEqual( '-a105 9 atan 10 101 ** * get_digits 100 left', '195785 oeis 100 left' )
    expectEqual( '-a105 8 atan 10 101 ** * get_digits 100 left', '195781 oeis 100 left' )

    # atanh
    testOperator( '0.45 atanh' )

    expectEqual( '-a112 4 -14 pi 7 / sin pi 7 / tan * 2 / sqrt asinh * exp atanh * exp 1 - sqrt 10 110 ** * get_digits 108 left', '293415 oeis 108 left' )
    expectEqual( '-a112 4 -18 pi 9 / sin pi 9 / tan * 2 / sqrt asinh * exp atanh * exp 1 - sqrt 10 110 ** * get_digits 108 left', '293416 oeis 108 left' )

    # cos
    testOperator( 'pi radians cos' )

    expectEqual( '45 degrees cos', '2 sqrt 1/x' )
    expectEqual( '0 lambda 1 x cos - x sqr / limitn', '0.5' )

    expectEqual( '-a105 1 cos 10 100 ** * get_digits 98 left', '49470 oeis 98 left' )

    # cosh
    testOperator( 'pi 3 / cosh' )

    expectEqual( '0 250 range cosh floor', '501 oeis 251 left' )
    expectEqual( '-a1005 1 cosh 10 1000 ** * get_digits 1000 left', '73743 oeis 1000 left' )

    # cot
    testOperator( 'pi 7 / cot' )

    expectEqual( '-a110 1 coth 10 105 ** * get_digits 103 left', '73747 oeis 103 left' )

    # coth
    testOperator( 'pi 9 / coth' )

    expectEqual( '-a1005 1 coth 10 1000 ** * get_digits 1000 left', '73747 oeis 1000 left' )

    # csc
    testOperator( 'pi 12 / csc' )

    expectEqual( '-a110 1 csc 10 107 ** * get_digits 105 left', '73447 oeis 105 left' )
    expectEqual( '-a1005 phi csc 10 1002 ** * get_digits 1000 left', '139350 oeis 1000 left' )
    expectEqual( '-a110 pi 8 / csc 10 107 ** * get_digits 105 left', '121601 oeis 105 left' )
    expectEqual( '-a110 pi 7 / csc 10 107 ** * get_digits 105 left', '121598 oeis 105 left' )
    expectEqual( '-a110 pi 5 / csc 10 107 ** * get_digits 105 left', '121570 oeis 105 left' )
    expectEqual( '1 2000 range lambda x csc x 1 + csc is_less filter', '246410 oeis 1000 left' )
    expectEqual( '1 2000 range lambda x csc x 1 + csc is_greater filter', '246413 oeis 1000 left' )

    # csch
    testOperator( 'pi 13 / csch' )

    expectEqual( '-a1005 1 csch 10 1002 ** * get_digits 1001 left', '73745 oeis 1001 left' )

    # sec
    testOperator( 'pi 7 / sec' )

    expectEqual( '-a110 1 sec 10 107 ** * get_digits 105 left', '73448 oeis 105 left' )

    # sech
    testOperator( 'pi 7 / sech' )

    expectEqual( '-a1005 1 sech 10 1001 ** * get_digits 1001 left', '73746 oeis 1001 left' )

    # sin
    expectEqual( 'pi 4 / sin', '2 sqrt 1/x' )
    expectEqual( '0 lambda 2 x * sin 3 x * sin / limitn', '2 3 /' )

    expectEqual( '-a105 1 sin 10 100 ** * get_digits 98 left', '49469 oeis 98 left' )

    # sinh
    testOperator( 'pi 2 / sinh' )

    expectEqual( '0 250 range sinh nearest_int', '495 oeis 251 left' )
    expectEqual( '0 200 range sinh floor', '471 oeis 201 left' )
    expectEqual( '-a1005 1 sinh 10 1001 ** * get_digits 1001 left', '73742 oeis 1001 left' )

    # tan
    testOperator( 'pi 3 / tan' )

    expectEqual( '0 999 range tan nearest_int', '209 oeis 1000 left' )
    expectEqual( '0 1000 range tan floor', '503 oeis 1001 left' )

    # tanh
    testOperator( 'pi 4 / tanh' )

    expectEqual( '-a1005 1 tanh 10 1002 ** * get_digits 1001 left', '73744 oeis 1001 left' )


# //******************************************************************************
# //
# //  runAdvancedTests
# //
# //  This is just for tests that are more complex than the single operator
# //  tests... and any random tests that don't fit in anywhere else.
# //
# //******************************************************************************

def runAdvancedTests( ):
    testOperator( '2016 dst_end 2016 dst_start - 2016-12-31 2016-01-01 - /' )
    #testOperator( '"Leesburg, VA" today 0 20 range days + echo daytime collate -s1' )
    testOperator( '1 1 thousand range lambda x is_polydivisible filter' )
    testOperator( '1 50 range twin_primes_ 1/x sum sum' )

    expectResult( '-0', 0 )

    expectEqual( '38[147][246]5[246][124679][246][124679]0 build_numbers lambda x is_polydivisible filter lambda x is_pandigital filter', '[ 3816547290 ]' )



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
    ( 'logic',              runLogicOperatorTests ),
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
    args = [ ]

    for arg in sys.argv[ 1 : ]:
        if arg == '-D':
            g.debugMode = True
        else:
            args.append( arg )

    startTime = time.process_time( )

    checkForPrimeData( )

    unitsFile = Path( getDataPath( ) + os.sep + 'units.pckl.bz2' )

    if not unitsFile.is_file( ):
        print( 'Please run "makeUnits" to initialize the unit conversion data files.' )
        sys.exit( 0 )

    helpFile = Path( getDataPath( ) + os.sep + 'help.pckl.bz2' )

    if not helpFile.is_file( ):
        print( 'Please run "makeHelp" to initialize the help files.' )
        sys.exit( 0 )

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

    #for i in operators:
    #    print( operators[ i ].generateCall( i ) )

    runTests( args )

    if ( g.astroDataLoaded and not g.astroDataAvailable ):
        print( 'Astronomy tests were skipped because data could not be downloaded.' )
        print( )

    if ( not g.primeDataAvailable ):
        print( 'Prime number tests were skipped because the prime number data is not available.' )
        print( )

    print( 'Tests complete.  Time elapsed:  {:.3f} seconds'.format( time.process_time( ) - startTime ) )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

