#!/usr/bin/env python

# //******************************************************************************
# //
# //  testRPNWithAlpha
# //
# //  test script for RPN
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import sys
import wolframalpha

from collections import OrderedDict

from rpnOperators import *

from rpnAliases import operatorAliases
from rpnOperators import constants
from rpnMeasurement import RPNMeasurement
from rpnPersistence import cachedFunction, loadUnitNameData
from rpnTestUtils import *
from rpnUtils import getDataPath

from mpmath import *

client = None


# //******************************************************************************
# //
# //  initializeAlpha
# //
# //******************************************************************************

def initializeAlpha( ):
    with open( 'wolframalpha.key', "r" ) as input:
        key = input.read( ).replace( '\n', '' )

    return wolframalpha.Client( key )


# //******************************************************************************
# //
# //  queryAlpha
# //
# //******************************************************************************

@cachedFunction( 'wolfram' )
def queryAlpha( query ):
    res = client.query( query )
    return next( res.results ).text


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  #testOperator just evaluates an RPN expression to make sure nothing throws
# //  an exception.
# //
# //  #expectResult actually tests that the result from RPN matches the value
# //  given.
# //
# //  #expectEqual evaluates two RPN expressions and verifies that the results
# //  are the same.
# //
# //  #expectEquivalent evaluates two RPN expressions and verifies that the
# //  results are equivalent.  This means that if the results are lists, they
# //  need to have the same elements, but not necessarily be in the same order.
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  runAlgebraOperatorTests
# //
# //******************************************************************************

def runAlgebraOperatorTests( ):
    # add_polynomials
    #expectEqual( '1 10 range 1 10 range add_polynomials', '2 20 2 range2' )
    #expectException( '1 10 range add_polynomials' )

    # eval_polynomial
    #testOperator( '1 10 range 6 eval_polynomial' )
    #testOperator( '[ 4 -2 3 5 -6 20 ] 1 10 range eval_polynomial' )
    #expectException( '1 eval_polynomial' )
    #expectException( '1 10 range eval_polynomial' )

    # find_polynomial
    #expectEqual( 'phi 3 find_polynomial', '[ -1 1 1 ]' )
    #expectException( '1 find_polynomial' )

    # multiply_polynomials
    #testOperator( '1 10 range 1 10 range multiply_polynomials' )
    #expectException( '1 10 range multiply_polynomials' )

    # polynomial_power
    #testOperator( '[ 1 2 3 4 ] 5 polynomial_power' )
    #expectException( '1 10 range polynomial_power' )

    # polynomial_product
    #testOperator( '[ 1 10 range 1 10 range 2 11 range ] polynomial_product' )

    # polynomial_sum
    #testOperator( '[ 1 10 range 2 11 range ] polynomial_sum' )

    # solve
    #testOperator( '1 8 range solve' )
    #expectException( '0 solve' )
    #expectException( '1 solve' )
    #expectException( '[ 0 1 ] solve' )
    #expectException( '[ 0 0 1 ] solve' )
    #expectException( '[ 0 0 0 ] solve' )

    # solve_cubic
    #expectEquivalent( '1 0 0 0 solve_cubic', '[ 1 0 0 0 ] solve' )
    #expectEquivalent( '0 1 0 0 solve_cubic', '[ 0 1 0 0 ] solve' )
    #expectEquivalent( '1 1 0 0 solve_cubic', '[ 1 1 0 0 ] solve' )
    #expectEquivalent( '0 0 1 0 solve_cubic', '[ 0 0 1 0 ] solve' )
    #expectEquivalent( '1 0 -3 0 solve_cubic', '[ 1 0 -3 0 ] solve' )
    #expectEquivalent( '10 -10 10 -10 solve_cubic', '[ 10 -10 10 -10 ] solve' )
    #expectEquivalent( '57 -43 15 28 solve_cubic', '[ 57 -43 15 28 ] solve' )
    #expectException( '0 0 0 0 solve_cubic' )
    #expectException( '0 0 0 1 solve_cubic' )

    # solve_quadratic
    #expectEquivalent( '1 0 0 solve_quadratic', '[ 1 0 0 ] solve' )
    #expectEquivalent( '1 1 0 solve_quadratic', '[ 1 1 0 ] solve' )
    #expectEquivalent( '1 0 1 solve_quadratic', '[ 1 0 1 ] solve' )
    #expectEquivalent( '0 1 0 solve_quadratic', '[ 0 1 0 ] solve' )
    #expectEquivalent( '1 -1 1 solve_quadratic', '[ 1 -1 1 ] solve' )
    #expectEquivalent( '8 9 10 solve_quadratic', '[ 8 9 10 ] solve' )
    #expectEquivalent( '-36 150 93 solve_quadratic', '[ -36 150 93 ] solve' )
    #expectException( '0 0 0 solve_quadratic' )
    #expectException( '0 0 1 solve_quadratic' )

    # solve_quartic
    #expectEquivalent( '1 0 0 0 0 solve_quartic', '[ 1 0 0 0 0 ] solve' )
    #expectEquivalent( '0 1 0 0 0 solve_quartic', '[ 0 1 0 0 0 ] solve' )
    #expectEquivalent( '0 1 0 1 0 solve_quartic', '[ 0 1 0 1 0 ] solve' )
    #expectEquivalent( '0 0 1 0 0 solve_quartic', '[ 0 0 1 0 0 ] solve' )
    #expectEquivalent( '0 0 0 1 0 solve_quartic', '[ 0 0 0 1 0 ] solve' )
    #expectEquivalent( '1 0 -5 0 7 solve_quartic', '[ 1 0 -5 0 7 ] solve' )
    #expectEquivalent( '2 -3 2 -3 2 solve_quartic', '[ 2 -3 2 -3 2 ] solve' )
    #expectEquivalent( '54 23 -87 19 2042 solve_quartic', '[ 54 23 -87 19 2042 ] solve' )
    #expectException( '0 0 0 0 0 solve_quadratic' )
    #expectException( '0 0 0 0 1 solve_quadratic' )
    pass


# //******************************************************************************
# //
# //  runArithmeticOperatorTests
# //
# //******************************************************************************

def runArithmeticOperatorTests( ):
    # abs
    #expectResult( '-394 abs', 394 )
    #expectResult( '0 abs', 0 )
    #expectResult( '394 abs', 394 )

    # add
    #expectResult( '4 3 add', 7 )
    #expectResult( '3 feet 7 inches + inches convert', RPNMeasurement( 43, 'inch' ) )
    #testOperator( 'today 7 days +' )
    #testOperator( 'today 3 weeks +' )
    #testOperator( 'today 50 years +' )
    #testOperator( '4 cups 13 teaspoons +' )
    #expectResult( '55 mph 10 miles hour / +', RPNMeasurement( 65, 'mile/hour' ) )
    #testOperator( '55 mph 10 meters second / +' )
    #testOperator( '55 mph 10 furlongs fortnight / +' )
    #testOperator( 'today 3 days add' )
    #testOperator( 'today 3 weeks add' )
    #testOperator( 'now 150 miles 10 furlongs fortnight / / add' )

    # ceiling
    #expectResult( '9.99999 ceiling', 10 )
    #expectResult( '-0.00001 ceiling', 0 )

    # decrement
    #expectResult( '2 decrement', 1 )

    # divide
    #testOperator( '12 13 divide' )
    #testOperator( '10 days 7 / dhms' )
    #testOperator( 'marathon 100 miles hour / / minutes convert' )
    #testOperator( '2 zeta sqrt 24 sqrt / 12 *' )
    #testOperator( 'now 2014-01-01 - minutes /' )
    #expectException( '1 0 divide' )

    # floor
    #expectResult( '-0.4 floor', -1 )
    #expectResult( '1 floor', 1 )
    #expectResult( '3.4 floor', 3 )
    #expectEqual( '10.3 cups floor', '10 cups' )
    #expectEqual( '88 mph 10 round_by_value', '90 mph' )

    # gcd
    expectEqual( '[ 124 324 ] gcd', queryAlpha( 'gcd of 324 and 124' ) )
    expectEqual( '[ 1296 1440 ] gcd', queryAlpha( 'gcd of 1296 and 1440' ) )

    # geometric_mean
    #testOperator( '1 10 range geometric_mean' )
    #testOperator( '1 1 10 range range geometric_mean' )

    # increment
    #expectResult( '2 increment', 3 )

    # is_divisible
    #expectResult( '1000 10000 is_divisible', 0 )
    #expectResult( '10000 1000 is_divisible', 1 )
    #expectResult( '12 1 12 range is_divisible', [ 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1 ] )
    #expectResult( '1 20 range 6 is_divisible', [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0 ] )
    #expectException( '1 0 is_divisible' )
    ##expectException( '2 i 1 is_divisible' )

    # is_equal
    #expectResult( '4 3 is_equal', 0 )
    #expectResult( 'pi pi is_equal', 1 )

    # is_even
    #expectResult( '-2 is_even', 1 )
    #expectResult( '-1 is_even', 0 )
    #expectResult( '0 is_even', 1 )
    #expectResult( '1 is_even', 0 )
    #expectResult( '2 is_even', 1 )
    #expectException( '1 i is_even' )

    # is_greater
    #expectResult( '4 3 is_greater', 1 )
    #expectResult( '55 55 is_greater', 0 )
    #expectResult( 'e pi is_greater', 0 )

    # is_less
    #expectResult( '4 3 is_less', 0 )
    #expectResult( '2 2 is_less', 0 )
    #expectResult( '2 3 is_less', 1 )

    # is_not_equal
    #expectResult( '4 3 is_not_equal', 1 )
    #expectResult( '3 3 is_not_equal', 0 )

    # is_not_greater
    #expectResult( '4 3 is_not_greater', 0 )
    #expectResult( '77 77 is_not_greater', 1 )
    #expectResult( '2 99 is_not_greater', 1 )

    # is_not_less
    #expectResult( '4 3 is_not_less', 1 )
    #expectResult( '663 663 is_not_less', 1 )
    #expectResult( '-100 100 is_not_less', 0 )

    # is_not_zero
    #expectResult( '-1 is_not_zero', 1 )
    #expectResult( '0 is_not_zero', 0 )
    #expectResult( '1 is_not_zero', 1 )

    # is_odd
    #expectResult( '-2 is_odd', 0 )
    #expectResult( '-1 is_odd', 1 )
    #expectResult( '0 is_odd', 0 )
    #expectResult( '1 is_odd', 1 )
    #expectResult( '2 is_odd', 0 )

    # is_square
    #expectResult( '1024 is_square', 1 )
    #expectResult( '5 is_square', 0 )

    # is_zero
    #expectResult( '-1 is_zero', 0 )
    #expectResult( '0 is_zero', 1 )
    #expectResult( '1 is_zero', 0 )

    # larger
    #expectResult( '7 -7 larger' , 7 )

    # lcm
    expectEqual( '[ 3 12 36 65 10 ] lcm', queryAlpha( 'least common multiple of 3 12 36 65 10' ) )
    expectEqual( '[ 1296 728 3600 460 732 ] lcm', queryAlpha( 'least common multiple of 1296 728 3600 460 732' ) )

    # max
    #expectResult( '1 10 range max', 10 )
    #expectResult( '10 1 range min', 1 )
    #expectResult( '[ 9 4 7 2 5 6 3 8 ] max', 9 )
    #expectEqual( '1 1 10 range range max', '1 10 range' )

    # mean
    #expectResult( '1 10 range mean', 5.5 )
    #expectEqual( '1 10000 range mean', '5000.5' )
    #testOperator( '1 1 10 range range mean' )

    # min
    #expectResult( '1 10 range min', 1 )
    #expectResult( '10 1 range min', 1 )
    #expectResult( '[ 9 4 7 2 5 6 3 8 ] min', 2 )
    #expectEqual( '1 1 10 range range min', '[ 1 10 dup ]' )

    # modulo
    #expectResult( '11001 100 modulo', 1 )
    #expectResult( '-120 7 modulo', 6 )
    #expectResult( '8875 49 modulo', 6 )
    #expectResult( '199467 8876 modulo', 4195 )

    # multiply
    #expectResult( '5 7 multiply', 35 )
    #testOperator( '15 mph 10 hours *' )
    #testOperator( 'c m/s convert 1 nanosecond * inches convert' )

    # nearest_int
    #expectResult( '0.1 nearest_int', 0 )
    #expectResult( '4.5 nearest_int', 4 )
    #expectResult( 'pi nearest_int', 3 )

    # negative
    #expectResult( '-4 negative', 4 )
    #expectResult( '0 negative', 0 )
    #expectResult( '4 negative', -4 )

    # product
    #expectEqual( '-a200 1 100 range product', '-a200 100 !' )
    #expectResult( '[ 2 cups ] product', RPNMeasurement( 2, 'cup' ) )
    #expectResult( '[ 3 2 cups ] product', RPNMeasurement( 6, 'cup' ) )
    #expectResult( '[ 2 cups 8 16 ] product', RPNMeasurement( 256, 'cup' ) )
    #expectResult( '[ 3 2 cups 8 16 ] product', RPNMeasurement( 768, 'cup' ) )
    #testOperator( '1 1 10 range range prod' )

    # reciprocal
    #expectEqual( '6 7 / reciprocal', '7 6 /' )

    # round
    #expectResult( '0.1 round', 0 )
    #expectResult( '4.5 round', 5 )
    #expectEqual( '9.9 W round', '10 W' )

    # round_by_digits
    #expectResult( '0.1 0 round_by_digits', 0 )
    #expectResult( '4.5 0 round_by_digits', 5 )
    #expectResult( '4.5 1 round_by_digits', 0 )
    #expectResult( '8 1 round_by_digits', 10 )
    #expectResult( '4500 3 round_by_digits', 5000 )
    #expectEqual( 'pi -2 round_by_digits', '3.14' )
    #expectEqual( '88 mph 1 round_by_digits', '90 mph' )
    #expectEqual( 'avogadro 20 round_by_digits', '6.022e23' )

    # round_by_value
    #expectResult( '0.1 1 round_by_value', 0 )
    #expectResult( '4.5 1 round_by_value', 5 )
    #expectResult( '4.5 2 round_by_value', 4 )
    #expectResult( '8 3 round_by_value', 9 )
    #expectResult( '4500 7 round_by_value', 4501 )
    #expectEqual( 'pi 0.01 round_by_value', '3.14' )
    #expectEqual( '88 mph 10 round_by_value', '90 mph' )

    # sign
    #expectResult( '1 sign', 1 )
    #expectResult( '0 sign', 0 )
    #expectResult( '-1 sign', -1 )
    #expectResult( 'infinity sign', 1 )
    #expectResult( 'negative_infinity sign', -1 )
    #expectResult( '-2 cups sign', -1 )

    # smaller
    #expectResult( '7 -7 smaller' , -7 )

    # stddev
    #testOperator( '1 10 range stddev' )
    #testOperator( '1 1 10 range range stddev' )

    # subtract
    #testOperator( '3948 474 subtract' )
    #expectResult( '4 cups 27 teaspoons - teaspoons convert', RPNMeasurement( 165, 'teaspoon' ) )
    #testOperator( '57 hectares 23 acres -' )
    #testOperator( '10 Mb second / 700 MB hour / -' )
    #testOperator( 'today 3 days -' )
    #testOperator( 'today 3 weeks -' )
    #testOperator( 'today 3 months -' )
    #testOperator( 'now earth_radius 2 pi * * miles convert 4 mph / -' )
    #testOperator( 'today 2 months -' )
    #testOperator( 'today 1965-03-31 -' )
    #testOperator( '2015-01-01 1965-03-31 -' )

    # sum
    #expectResult( '1 10 range sum', 55 )
    #testOperator( '[ 27 days 7 hour 43 minute 12 second ] sum' )
    #testOperator( '1 1 10 range range sum' )


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    # antitransit_time
    #testOperator( 'moon "Calais, France" location today antitransit_time' )
    #testOperator( 'sun "Calais, France" today antitransit_time' )
    #testOperator( 'jupiter "Las Vegas, NV" 2016 spring 1 20 range days + antitransit_time' )

    # astronomical_dawn
    #testOperator( '"Chattanooga, TN" location today astronomical_dawn' )
    #testOperator( '"Chattanooga, TN" today astronomical_dawn' )

    # astronomical_dusk
    #testOperator( '"Perth, Australia" location today astronomical_dusk' )
    #testOperator( '"Perth, Australia" today astronomical_dusk' )

    # autumnal_equinox
    #testOperator( '2015 autumnal_equinox' )

    # dawn
    #testOperator( '"Christchurch, NZ" location today dawn' )
    #testOperator( '"Christchurch, NZ" today dawn' )

    # day_time
    #testOperator( '"Toulouse, France" location today day_time' )
    #testOperator( '"Nice, France" today day_time' )
    #testOperator( '"Allentown, PA" 1975-03-31 0 20 range days + day_time' )

    # dusk
    #testOperator( '"Vienna, Austria" location today dusk' )
    #testOperator( '"Vienna, Austria" today dusk' )

    # jupiter
    #testOperator( 'jupiter "Ottawa, Canada" location today next_setting' )
    #testOperator( 'jupiter "Ottawa, Canada" today next_setting' )

    # mars
    #testOperator( 'mars "Beijing, China" location today next_transit' )
    #testOperator( 'mars "Beijing, China" today next_transit' )

    # mercury
    #testOperator( 'mercury "Los Angeles, CA" location today next_rising' )
    #testOperator( 'mercury "Los Angeles, CA" today next_rising' )

    # moon
    #testOperator( 'saturn "Burlington, VT" location today next_antitransit' )
    #testOperator( 'saturn "Burlington, VT" today next_antitransit' )

    # moon_antitransit
    #testOperator( '"Madrid, Spain" location today moon_antitransit' )
    #testOperator( '"Madrid, Spain" today moon_antitransit' )

    # moon_phase
    #testOperator( 'today moon_phase' )

    # moon_transit
    #testOperator( '"Riga, Latvia" location today moon_transit' )
    #testOperator( '"Riga, Latvia" today moon_transit' )

    # moonrise
    #testOperator( '"Las Cruces, NM" location today moonrise' )
    #testOperator( '"Las Cruces, NM" today moonrise' )

    # moonset
    #testOperator( '"Tacoma, WA" location today moonset' )
    #testOperator( '"Tacoma, WA" today moonset' )

    # nautical_dawn
    #testOperator( '"Columbia, SC" location today nautical_dawn' )
    #testOperator( '"Columbia, SC" today nautical_dawn' )

    # nautical_dusk
    #testOperator( '"Norfolk, VA" location today nautical_dusk' )
    #testOperator( '"Norfolk, VA" today nautical_dusk' )

    # neptune
    #testOperator( 'neptune "Hatfield, PA" location now next_rising' )
    #testOperator( 'neptune "Hatfield, PA" now next_rising' )

    # next_antitransit
    #testOperator( 'saturn "Blacksburg, VA" location today next_antitransit' )
    #testOperator( 'saturn "Blacksburg, VA" today next_antitransit' )

    # next_first_quarter_moon
    #testOperator( 'today next_first_quarter_moon' )

    # next_full_moon
    #testOperator( 'today next_full_moon' )

    # next_last_quarter_moon
    #testOperator( 'today next_last_quarter_moon' )

    # next_new_moon
    #testOperator( 'today next_new_moon' )

    # next_rising
    #testOperator( 'moon "Leesburg, VA" location now next_rising' )
    #testOperator( 'moon "Leesburg, VA" now next_rising' )

    # next_setting
    #testOperator( 'moon "Kyoto, Japan" location now next_setting' )
    #testOperator( 'moon "Kyoto, Japan" now next_setting' )

    # next_transit
    #testOperator( 'moon "Oslo, Norway" location now next_transit' )
    #testOperator( 'moon "Oslo, Norway" now next_transit' )

    # night_time
    #testOperator( '"Toulouse, France" location today night_time' )
    #testOperator( '"Nice, France" today night_time' )
    #testOperator( '"Cologne, Germany" 2015 winter 1 20 range days + night_time' )

    # pluto
    #testOperator( 'pluto "Johannesburg, South Africa" location now next_rising' )
    #testOperator( 'pluto "Johannesburg, South Africa" now next_rising' )

    # previous_antitransit
    #testOperator( 'neptune "Leesburg, VA" location now previous_antitransit' )
    #testOperator( 'neptune "Leesburg, VA" now previous_antitransit' )

    # previous_first_quarter_moon
    #testOperator( 'today previous_first_quarter_moon' )

    # previous_full_moon
    #testOperator( 'today previous_full_moon' )

    # previous_last_quarter_moon
    #testOperator( 'today previous_last_quarter_moon' )

    # previous_new_moon
    #testOperator( 'today previous_new_moon' )

    # previous_rising
    #testOperator( 'jupiter "Leesburg, VA" location now previous_rising' )
    #testOperator( 'jupiter "Leesburg, VA" now previous_rising' )

    # previous_setting
    #testOperator( 'uranus "Leesburg, VA" location now previous_setting' )
    #testOperator( 'uranus "Leesburg, VA" now previous_setting' )

    # previous_transit
    #testOperator( 'mercury "Leesburg, VA" location now previous_transit' )
    #testOperator( 'mercury "Leesburg, VA" now previous_transit' )

    # saturn
    #testOperator( 'saturn "Leesburg, VA" location today next_rising' )
    #testOperator( 'saturn "Leesburg, VA" today next_rising' )

    # sky_location
    #testOperator( 'mars now sky_location' )

    # solar_noon
    #testOperator( '"Leesburg, VA" location today solar_noon' )
    #testOperator( '"Leesburg, VA" today solar_noon' )

    # summer_solstice
    #testOperator( '2015 summer_solstice' )

    # sun
    #testOperator( 'sun "Leesburg, VA" location today next_rising' )
    #testOperator( 'sun "Leesburg, VA" today next_rising' )

    # sun_antitransit
    #testOperator( '"Leesburg, VA" location today sun_antitransit' )
    #testOperator( '"Leesburg, VA" today sun_antitransit' )

    # sunrise
    #testOperator( '"Salzburg, Germany" location today sunrise' )
    #testOperator( '"Salzburg, Germany" today sunrise' )

    # sunset
    #testOperator( '"New Delhi, India" location today sunset' )
    #testOperator( '"New Delhi, India" today sunset' )

    # transit_time
    #testOperator( 'sun "Munich, Germany" location today transit_time' )
    #testOperator( 'moon "Dusseldorf, Germany" today transit_time' )
    #testOperator( 'mars "Dortmund, Germany" 2015 summer 1 20 range days + transit_time' )

    # uranus
    #testOperator( 'uranus "Frankfurt, Germany" location today next_rising' )
    #testOperator( 'uranus "Frankfurt, Germany" today next_rising' )

    # venus
    #testOperator( 'venus "Butte, Montana" location today next_rising' )
    #testOperator( 'venus "Butte, Montana" today next_rising' )

    # vernal_equinox
    #testOperator( '2015 vernal_equinox' )

    # winter_solstice
    #testOperator( '2015 winter_solstice' )
    pass


# //******************************************************************************
# //
# //  runBitwiseOperatorTests
# //
# //******************************************************************************

def runBitwiseOperatorTests( ):
    # and
    #testOperator( '0x7777 0xdcba and' )

    # count_bits
    #testOperator( '0xffff count_bits' )

    # nand
    #testOperator( '-x 0x5543 0x7789 nand' )

    # nor
    #testOperator( '-x 0x5543 0x7789 nor' )

    # not
    #testOperator( '0xffffff ~' )
    #testOperator( '142857 not' )
    #testOperator( '-x 0xefefefefefefef not' )

    # or
    #testOperator( '-x 0x5543 0x7789 or' )

    # parity
    #testOperator( '0xff889d8f parity' )
    #expectEqual( '1 128 range parity nonzero 1 +', '69 oeis 65 left -D' )

    # shift_left
    #testOperator( '-x 0x10 3 shift_left' )

    # shift_right
    #testOperator( '-x 0x1000 4 shift_right' )

    # xor
    #testOperator( '0x1939 0x3948 xor' )
    pass


# //******************************************************************************
# //
# //  runCalendarOperatorTests
# //
# //******************************************************************************

def runCalendarOperatorTests( ):
    # ash_wednesday
    #testOperator( '2015 ash_wednesday' )

    # calendar
    #testOperator( '1965-03-31 calendar' )
    #testOperator( '2014-10-01 calendar' )
    #testOperator( 'today calendar' )

    # dst_end
    #testOperator( '2015 dst_end' )

    # dst_start
    #testOperator( '2015 dst_start' )

    # easter
    #testOperator( '2015 easter' )

    # election_day
    #testOperator( '2015 election_day' )

    # from_bahai
    #testOperator( '172 12 4 from_bahai' )

    # from_hebrew
    #testOperator( '5776 8 6 from_hebrew' )

    # from_indian_civil
    #testOperator( '1937 7 27 from_indian_civil' )

    # from_islamic
    #testOperator( '1437 1 5 from_islamic' )

    # from_julian
    #testOperator( '2015 10 6 from_julian' )

    # from_mayan
    #testOperator( '13 0 2 15 12 from_mayan' )

    # from_persian
    #testOperator( '1394 7 27 from_persian' )

    # iso_date
    #testOperator( 'today iso_date' )

    # labor_day
    #testOperator( '2015 labor_day' )

    # memorial_day
    #testOperator( '2015 memorial_day' )

    # nth_weekday
    #testOperator( '2015 march 4 thursday nth_weekday' )
    #testOperator( '2015 march -1 thursday nth_weekday' )

    # nth_weekday_of_year
    #testOperator( '2015 20 thursday nth_weekday_of_year' )
    #testOperator( '2015 -1 thursday nth_weekday_of_year' )

    # presidents_day
    #testOperator( '2015 presidents_day' )

    # thanksgiving
    #testOperator( '2015 thanksgiving' )

    # to_bahai
    #testOperator( 'today to_bahai' )

    # to_bahai_name
    #testOperator( 'today to_bahai_name' )

    # to_hebrew
    #testOperator( 'today to_hebrew' )

    # to_hebrew_name
    #testOperator( 'today to_hebrew_name' )

    # to_indian_civil
    #testOperator( 'today to_indian_civil' )

    # to_indian_civil_name
    #testOperator( 'today to_indian_civil_name' )

    # to_islamic
    #testOperator( 'today to_islamic' )

    # to_islamic_name
    #testOperator( 'today to_islamic_name' )

    # to_iso
    #testOperator( 'today to_iso' )

    # to_iso_name
    #testOperator( 'today to_iso_name' )

    # to_julian
    #testOperator( 'today to_julian' )

    # to_julian_day
    #testOperator( 'today to_julian_day' )

    # to_lilian_day
    #testOperator( 'today to_lilian_day' )

    # to_mayan
    #testOperator( 'today to_mayan' )

    # to_ordinal_date
    #testOperator( 'today to_ordinal_date' )

    # to_persian
    #testOperator( 'today to_persian' )

    # to_persian_name
    #testOperator( 'today to_persian_name' )

    # weekday
    #testOperator( 'today weekday' )

    # year_calendar
    #testOperator( '1965 year_calendar' )
    #testOperator( 'today year_calendar' )
    pass


# //******************************************************************************
# //
# //  runCombinatoricsOperatorTests
# //
# //******************************************************************************

def runCombinatoricsOperatorTests( ):
    # bell_polynomal
    #testOperator( '4 5 bell_polynomial' )
    #testOperator( '5 5 10 range bell_polynomial' )

    #from rpnUtils import downloadOEISSequence
    #
    #bell_terms = downloadOEISSequence( 106800 )
    #
    #bell_term_offsets = [ ]
    #
    #total = 0
    #
    #polynomials_to_check = 10
    #
    #for i in range( 1, polynomials_to_check + 2 ):
    #    bell_term_offsets.append( total )
    #    total += i
    #
    #for i in range( 0, polynomials_to_check ):
    #    bell_poly = bell_terms[ bell_term_offsets[ i ] : bell_term_offsets[ i + 1 ] ]
    #
    #    bell_poly_str = '[ '
    #    bell_poly_str += ' '.join( [ str( k ) for k in bell_poly ] )
    #
    #    bell_poly_str += ' ] '
    #
    #    for j in [ -300, -84, -1, 0, 1, 8, 23, 157 ]:
    #        expectEqual( str( i ) + ' ' + str( j ) + ' bell_polynomial',
    #                     bell_poly_str + str( j ) + ' eval_polynomial' )

    # binomial
    expectEqual( '12 9 binomial', queryAlpha( '12 choose 9' ) )
    expectEqual( '-a20 120 108 binomial', queryAlpha( '120 choose 108' ) )
    #testOperator( '-a20 -c 120 108 binomial' )

    # compositions
    #testOperator( '5 2 compositions' )
    #testOperator( '6 3 compositions' )
    #testOperator( '7 2 4 range compositions' )

    # debruijn
    #testOperator( '4 3 debruijn' )

    # lah
    #testOperator( '5 6 lah' )

    # multifactorial
    #testOperator( '1 20 range 5 multifactorial' )
    #expectEqual( '-a20 0 26 range 2 multifactorial', '6882 oeis 27 left' )
    #expectEqual( '0 29 range 3 multifactorial', '7661 oeis 30 left' )
    #expectEqual( '0 33 range 4 multifactorial', '7662 oeis 34 left' )
    #expectEqual( '0 36 range 5 multifactorial', '85157 oeis 37 left' )
    #expectEqual( '0 38 range 6 multifactorial', '85158 oeis 39 left' )
    #expectEqual( '0 40 range 7 multifactorial', '114799 oeis 41 left' )
    #expectEqual( '0 42 range 8 multifactorial', '114800 oeis 43 left' )
    #expectEqual( '0 43 range 9 multifactorial', '114806 oeis 44 left' )

    # multinomial
    #testOperator( '[ 2 5 6 7 ] multinomial' )

    # narayana
    #testOperator( '6 8 narayana' )

    # nth_apery
    #testOperator( '-a20 12 nth_apery' )

    # nth_bell
    #testOperator( '-a43 45 nth_bell' )
    #expectEqual( '-a20 0 26 range nth_bell', '-a20 110 oeis 27 left' )

    # nth_bernoulli
    #testOperator( '16 nth_bernoulli' )
    #expectEqual( '-a20 0 39 range nth_bernoulli', '-a20 27641 oeis 40 left 27642 oeis 40 left /' )

    # nth_catalan
    #testOperator( '-a50 85 nth_catalan' )
    #expectEqual( '-a20 1 34 2 range2 nth_catalan', '24492 oeis 17 left' )

    # nth_delannoy
    #testOperator( '-a80 100 nth_delannoy' )
    #expectEqual( '-a20 0 22 range nth_delannoy', '-a20 1850 oeis 23 left' )

    # nth_motzkin
    #testOperator( '-a25 56 nth_motzkin' )
    #expectEqual( '-a20 0 29 range nth_motzkin', '-a20 1006 oeis 30 left' )

    # nth_pell
    #testOperator( '13 nth_pell' )

    # nth_schroeder
    #testOperator( '-a50 67 nth_schroeder' )

    # nth_sylvester
    #testOperator( '45 nth_sylvester' )
    #expectEqual( '-a60 1 9 range nth_sylvester', '-a60 58 oeis 9 left' )

    # partitions
    #expectEqual( '125 partitions', queryAlpha( 'integer partitions of 125' ) )

    # permutations
    #expectEqual( '8 3 permutations', '8 ! 5 ! /' )
    #expectEqual( '-a20 17 12 permutations', '-a20 17 ! 5 ! /' )
    #expectException( '6 7 permutations' )


# //******************************************************************************
# //
# //  runComplexMathOperatorTests
# //
# //******************************************************************************

def runComplexMathOperatorTests( ):
    # argument
    #testOperator( '3 3 i + argument' )

    # conjugate
    #testOperator( '3 3 i + conjugate' )

    # i
    #expectEqual( '3 i', '-9 sqrt' )

    # imaginary
    #expectResult( '3 i 4 + imaginary', 3 )
    #expectResult( '5 imaginary', 0 )
    #expectResult( '7 i imaginary', 7 )

    # real
    #expectResult( '3 i 4 + real', 4 )
    #expectResult( '5 real', 5 )
    #expectResult( '7 i real', 0 )
    pass


# //******************************************************************************
# //
# //  runConstantOperatorTests
# //
# //******************************************************************************

def runConstantOperatorTests( ):
    #expectResult( 'default', -1 )
    #expectResult( 'false', 0 )
    #expectResult( 'true', 1 )

    # infinity
    #testOperator( 'infinity lambda x fib x 1 - fib / limit' )
    #expectEqual( 'infinity lambda x fib x 1 - fib / limit', 'phi' )
    #testOperator( 'infinity lambda x 1/x 1 + x ** limit' )

    # days of the week
    #expectResult( 'monday', 1 )
    #expectResult( 'tuesday', 2 )
    #expectResult( 'wednesday', 3 )
    #expectResult( 'thursday', 4 )
    #expectResult( 'friday', 5 )
    #expectResult( 'saturday', 6 )
    #expectResult( 'sunday', 7 )

    # months
    #expectResult( 'january', 1 )
    #expectResult( 'february', 2 )
    #expectResult( 'march', 3 )
    #expectResult( 'april', 4 )
    #expectResult( 'may', 5 )
    #expectResult( 'june', 6 )
    #expectResult( 'july', 7 )
    #expectResult( 'august', 8 )
    #expectResult( 'september', 9 )
    #expectResult( 'october', 10 )
    #expectResult( 'november', 11 )
    #expectResult( 'december', 12 )

    # mathematical constants
    #testOperator( 'apery_constant' )
    #testOperator( 'catalan_constant' )
    #testOperator( 'champernowne_constant' )
    #testOperator( 'copeland_erdos_constant' )
    #testOperator( 'e' )
    #testOperator( 'eddington_number' )
    #testOperator( 'euler_mascheroni_constant' )
    #testOperator( 'glaisher_constant' )
    #testOperator( 'infinity' )
    #testOperator( 'itoi' )
    #testOperator( 'khinchin_constant' )
    #testOperator( 'merten_constant' )
    #testOperator( 'mills_constant' )
    #testOperator( 'negative_infinity' )
    #testOperator( 'omega_constant' )
    #testOperator( 'phi' )
    #testOperator( 'pi' )
    #testOperator( 'plastic_constant' )
    #testOperator( 'prevost_constant' )
    #testOperator( 'robbins_constant' )
    #testOperator( 'silver_ratio' )

    # physical quantities
    #testOperator( 'aa_battery' )
    #testOperator( 'gallon_of_ethanol' )
    #testOperator( 'gallon_of_gasoline' )
    #testOperator( 'density_of_water' )
    #testOperator( 'density_of_hg' )

    # physical constants
    #testOperator( 'avogadro_number' )
    #testOperator( 'bohr_radius' )
    #testOperator( 'boltzmann_constant' )
    #testOperator( 'coulomb_constant' )
    #testOperator( 'electric_constant' )
    #testOperator( 'electron_charge' )
    #testOperator( 'faraday_constant' )
    #testOperator( 'fine_structure_constant' )
    #testOperator( 'magnetic_constant' )
    #testOperator( 'newton_constant' )
    #testOperator( 'radiation_constant' )
    #testOperator( 'rydberg_constant' )
    #testOperator( 'speed_of_light' )
    #testOperator( 'stefan_boltzmann_constant' )
    #testOperator( 'vacuum_impedance' )
    #testOperator( 'von_klitzing_constant' )

    # programming integer constants
    #expectEqual( 'max_char', '2 7 ** 1 -' )
    #testOperator( 'max_double' )
    #testOperator( 'max_float' )
    #expectEqual( 'max_long', '2 31 ** 1 -' )
    #expectEqual( '-a20 max_longlong', '-a20 2 63 ** 1 -' )
    #expectEqual( '-a40 max_quadlong', '-a40 2 127 ** 1 -' )
    #expectEqual( 'max_short', '2 15 ** 1 -' )
    #expectEqual( 'max_uchar', '2 8 ** 1 -' )
    #expectEqual( 'max_ulong', '2 32 ** 1 -' )
    #expectEqual( '-a20 max_ulonglong', '-a20 2 64 ** 1 -' )
    #expectEqual( '-a40 max_uquadlong', '-a40 2 128 ** 1 -' )
    #expectEqual( 'max_ushort', '2 16 ** 1 -' )

    #expectEqual( 'min_char', '2 7 ** negative' )
    #testOperator( 'min_double' )
    #testOperator( 'min_float' )
    #expectEqual( 'min_long', '2 31 ** negative' )
    #expectEqual( '-a20 min_longlong', '-a20 2 63 ** negative' )
    #expectEqual( '-a40 min_quadlong', '-a40 2 127 ** negative' )
    #expectEqual( 'min_short', '2 15 ** negative' )
    #expectResult( 'min_uchar', 0 )
    #expectResult( 'min_ulong', 0 )
    #expectResult( 'min_ulonglong', 0 )
    #expectResult( 'min_uquadlong', 0 )
    #expectResult( 'min_ushort', 0 )

    # Planck constants
    #testOperator( 'planck_constant' )
    #testOperator( 'reduced_planck_constant' )

    #testOperator( 'planck_length' )
    #testOperator( 'planck_mass' )
    #testOperator( 'planck_time' )
    #testOperator( 'planck_charge' )
    #testOperator( 'planck_temperature' )

    #testOperator( 'planck_angular_frequency' )
    #testOperator( 'planck_area' )
    #testOperator( 'planck_current' )
    #testOperator( 'planck_density' )
    #testOperator( 'planck_energy' )
    #testOperator( 'planck_energy_density' )
    #testOperator( 'planck_force' )
    #testOperator( 'planck_impedance' )
    #testOperator( 'planck_intensity' )
    #testOperator( 'planck_momentum' )
    #testOperator( 'planck_power' )
    #testOperator( 'planck_pressure' )
    #testOperator( 'planck_voltage' )
    #testOperator( 'planck_volume' )

    # subatomic particle constants
    #testOperator( 'alpha_particle_mass' )
    #testOperator( 'deuteron_mass' )
    #testOperator( 'electron_mass' )
    #testOperator( 'helion_mass' )
    #testOperator( 'muon_mass' )
    #testOperator( 'neutron_mass' )
    #testOperator( 'proton_mass' )
    #testOperator( 'tau_mass' )
    #testOperator( 'triton_mass' )

    # heavenly body constants
    #testOperator( 'solar_luminosity' )
    #testOperator( 'solar_mass' )
    #testOperator( 'solar_radius' )
    #testOperator( 'solar_volume' )

    #testOperator( 'mercury_mass' )
    #testOperator( 'mercury_radius' )
    #testOperator( 'mercury_revolution' )
    #testOperator( 'mercury_volume' )

    #testOperator( 'venus_mass' )
    #testOperator( 'venus_radius' )
    #testOperator( 'venus_revolution' )
    #testOperator( 'venus_volume' )

    #testOperator( 'earth_gravity' )
    #testOperator( 'earth_mass' )
    #testOperator( 'earth_radius' )
    #testOperator( 'earth_volume' )
    #testOperator( 'sidereal_year' )
    #testOperator( 'tropical_year' )

    #testOperator( 'moon_gravity' )
    #testOperator( 'moon_mass' )
    #testOperator( 'moon_radius' )
    #testOperator( 'moon_revolution' )
    #testOperator( 'moon_volume' )

    #testOperator( 'mars_mass' )
    #testOperator( 'mars_radius' )
    #testOperator( 'mars_revolution' )
    #testOperator( 'mars_volume' )

    #testOperator( 'jupiter_mass' )
    #testOperator( 'jupiter_radius' )
    #testOperator( 'jupiter_revolution' )
    #testOperator( 'jupiter_volume' )

    #testOperator( 'saturn_mass' )
    #testOperator( 'saturn_radius' )
    #testOperator( 'saturn_revolution' )
    #testOperator( 'saturn_volume' )

    #testOperator( 'uranus_mass' )
    #testOperator( 'uranus_radius' )
    #testOperator( 'uranus_revolution' )
    #testOperator( 'uranus_volume' )

    #testOperator( 'neptune_mass' )
    #testOperator( 'neptune_radius' )
    #testOperator( 'neptune_revolution' )
    #testOperator( 'neptune_volume' )

    #testOperator( 'pluto_mass' )
    #testOperator( 'pluto_radius' )
    #testOperator( 'pluto_revolution' )
    #testOperator( 'pluto_volume' )
    pass


# //******************************************************************************
# //
# //  runConversionOperatorTests
# //
# //******************************************************************************

def runConversionOperatorTests( ):
    # char
    #testOperator( '0x101 char' )

    # convert - convert is handled separately

    # dhms
    #testOperator( '8 million seconds dhms' )

    # dms
    #testOperator( '1 radian dms' )

    # double
    #testOperator( '-x 10 20 ** double' )
    #testOperator( '-x pi double' )

    # float
    #testOperator( '-x 1029.3 float' )
    #testOperator( 'pi float' )

    # from_unix_time
    #testOperator( '1234567890 from_unix_time' )

    # hms
    #testOperator( '54658 seconds hms' )

    # integer
    #testOperator( '456 8 integer' )

    # invert_units
    #testOperator( '30 miles gallon / invert_units' )

    # latlong_to_nac
    #testOperator( '"Detroit, MI" location_info latlong_to_nac' )

    # long
    #testOperator( '3456789012 long' )

    # longlong
    #testOperator( '1234567890123456789012 longlong' )

    # pack
    #testOperator( '-x [ 192 168 0 1 ] [ 8 8 8 8 ] pack' )

    # short
    #testOperator( '32800 short' )

    # to_unix_time
    #testOperator( '[ 2014 4 30 0 0 0 ] make_time to_unix_time' )

    # uchar
    #testOperator( '290 uchar' )

    # uinteger
    #testOperator( '200 8 uinteger' )

    # ulong
    #testOperator( '234567890 ulong' )

    # ulonglong
    #testOperator( '-a20 12345678901234567890 ulonglong' )

    # undouble
    #testOperator( '0x400921fb54442d18 undouble' )
    #testOperator( '0xcdcdcdcdcdcdcdcd undouble' )

    # unfloat
    #testOperator( '0x40490fdb unfloat' )
    #testOperator( '0xcdcdcdcd unfloat' )

    # unpack
    #testOperator( '503942034 [ 3 4 5 11 4 4 ] unpack' )

    # ushort
    #testOperator( '23456 ushort' )

    # ydhms
    #testOperator( '14578 seconds ydhms' )
    pass


# //******************************************************************************
# //
# //  runDateTimeOperatorTests
# //
# //******************************************************************************

def runDateTimeOperatorTests( ):
    # get_day
    #testOperator( 'now get_day' )

    # get_hour
    #testOperator( 'now get_hour' )

    # get_minute
    #testOperator( 'now get_minute' )

    # get_month
    #testOperator( 'now get_month' )

    # get_second
    #testOperator( 'now get_second' )

    # get_year
    #testOperator( 'now get_year' )

    # iso_day
    #testOperator( 'today iso_day' )

    # make_datetime
    #testOperator( '[ 1965 03 31 ] make_datetime' )

    # make_iso_time
    #testOperator( '[ 2015 34 6 ] make_iso_time' )

    # make_julian_time
    #testOperator( '[ 2015 7 5 4 3 ] make_julian_time' )

    # now
    #testOperator( 'now' )

    # today
    #testOperator( 'today' )

    # tomorrow
    #testOperator( 'tomorrow' )

    # yesterday
    #testOperator( 'yesterday' )
    pass


# //******************************************************************************
# //
# //  runFunctionOperatorTests
# //
# //******************************************************************************

def runFunctionOperatorTests( ):
    # eval
    #testOperator( '10 lambda x 5 * eval' )
    #testOperator( '-a20 57 lambda x 8 ** x 7 ** + x 6 ** x 5 ** + + x 4 ** x 3 ** + x 2 ** x + + + eval' )
    #expectEqual( '-a20 0 23 range lambda x 0 * 2 x 1 - power + 2 x power 1 - * eval', '6516 oeis 24 left' )
    #expectEqual( '1 46 range lambda x sqr 2 * 2 + eval', '5893 oeis 47 left 46 right' )

    # eval2
    #testOperator( '7 8 lambda x 2 ** y 3 ** + eval2' )

    # eval3
    #testOperator( '15 4 26 lambda x 2 ** y 3 ** + z 4 ** + eval3' )

    # filter
    #testOperator( '-a20 1 80 range fib lambda x is_prime filter' )
    #expectEqual( '1 100 range lambda x is_prime filter', '1 25 range prime' )

    # filter_by_index
    #expectEqual( '0 1000 range lambda x is_prime filter_by_index', '1 168 primes' )

    # limit
    #testOperator( 'infinity lambda 1 1 x / + x power limit' )
    #testOperator( '0 lambda x x / 2 -1 x / power + 1/x limit' )
    #testOperator( 'infinity lambda x x ! x root / limit' )   # This one isn't very precise...
    #expectEqual( 'infinity lambda x fibonacci x 1 + fibonacci / limit', 'infinity lambda x lucas x 1 + lucas / limit' )
    #expectEqual( 'infinity lambda 1 1 x / + x power limit', 'e' )
    #expectEqual( 'infinity lambda x 1 x / sin * limit', '1' )
    #expectEqual( 'inf lambda 7 x / 1 + 3 x * ** limit', 'e 7 3 * **' )

    # limitn
    #testOperator( '0 lambda x x / 2 -1 x / power + 1/x limitn' )
    #expectEqual( '0 lambda x x sin / limitn', '1' )

    # negate
    #expectEqual( '[ 0 10 dup ] negate', '[ 1 10 dup ]' )

    # nprod
    #testOperator( '-a20 -p20 -d5 3 inf lambda x pi / 1/x cos nprod' )

    # nsum
    #expectEqual( '1 infinity lambda x 3 ** 1/x nsum', '3 zeta' )
    #expectEqual( '0 infinity lambda 1 x ! / nsum', 'e' )

    # These operators use the plotting GUI, so aren't included in the automated tests.
    # plot
    # plot2
    # plotc

    # unfilter
    #expectEqual( '1 100 range lambda x is_square unfilter', '37 oeis 90 left' )

    # unfilter_by_index
    #expectEqual( '0 200 range lambda x is_sphenic unfilter_by_index', '0 200 range lambda x is_sphenic unfilter' )

    # x
    #testOperator( '23 lambda x 4 ** 5 x 3 ** * + x sqrt - eval' )

    # y
    #testOperator( '23 57 lambda x 4 ** 5 x 3 ** * + y sqrt - eval2' )

    # z
    #testOperator( '23 57 86 lambda x 4 ** 5 y 3 ** * + z sqrt - eval3' )
    pass


# //******************************************************************************
# //
# //  runGeographyOperatorTests
# //
# //******************************************************************************

def runGeographyOperatorTests( ):
    # distance
    #testOperator( '"Leesburg, VA" location "Smithfield, VA" location distance' )
    #testOperator( '"Leesburg, VA" "Smithfield, VA" distance' )

    # lat_long
    ##testOperator( '"Leesburg, VA" 43 -80 lat_long distance' )

    # location
    #testOperator( '"Uppsala, Sweden" location today moonrise' )

    # location_info
    #testOperator( '"Dakar, Senegal" location_info' )
    #testOperator( '"Scottsdale, AZ" location_info' )
    pass


# //******************************************************************************
# //
# //  runGeometryOperatorTests
# //
# //******************************************************************************

def runGeometryOperatorTests( ):
    # antiprism_area
    #testOperator( '8 5 antiprism_area' )

    # antiprism_volume
    #testOperator( '3 8 antiprism_volume' )

    # cone_area
    #testOperator( '4 5 cone_area' )

    # cone_volume
    #testOperator( '3 8 cone_volume' )

    # dodecahedron_area
    #testOperator( '1 dodecahedron_area' )

    # dodecahedron_volume
    #testOperator( '1 dodecahedron_volume' )

    # icosahedron_area
    #testOperator( '1 icosahedron_area' )

    # icosahedron_volume
    #testOperator( '1 icosahedron_volume' )

    # n_sphere_area
    #testOperator( '34 inches 8 n_sphere_area' )
    #testOperator( '34 inches 4 ** 5 n_sphere_area' )
    #testOperator( '34 inches 7 ** 7 n_sphere_area' )
    #expectException( '34 cubic_inches 2 n_sphere_area' )

    # n_sphere_radius
    #testOperator( '3 meters 4 n_sphere_radius' )
    #testOperator( '3 meters 3 ** 4 n_sphere_radius' )
    #testOperator( '3 cubic_meters 4 n_sphere_radius' )
    #expectException( '3 cubic_meters 2 n_sphere_radius' )

    # n_sphere_volume
    #testOperator( '6 inches 8 ** 9 n_sphere_volume' )
    #testOperator( '3 feet 5 ** 6 n_sphere_volume' )
    #testOperator( '50 cubic_centimeters sqr 7 n_sphere_volume' )
    #expectException( '50 cubic_centimeters 1 n_sphere_volume' )

    # octahedron_area
    #testOperator( '1 octahedron_area' )

    # octahedron_volume
    #testOperator( '1 octahedron_volume' )

    # polygon_area
    #testOperator( '13 polygon_area' )
    #testOperator( '3 10 range polygon_area' )

    # prism_area
    #testOperator( '8 5 2 prism_area' )

    # prism_volume
    #testOperator( '3 8 4 prism_volume' )

    # sphere_area
    #testOperator( '8 inches sphere_area' )
    #testOperator( '8 sq_inches sphere_area' )
    #testOperator( '8 cu_inches sphere_area' )

    # sphere_radius
    #testOperator( '4 inches sphere_radius' )
    #testOperator( '4 square_inches sphere_radius' )
    #testOperator( '4 cubic_inches sphere_radius' )

    # sphere_volume
    #testOperator( '5 inches sphere_volume' )
    #testOperator( '5 sq_inches sphere_volume' )
    #testOperator( '5 cubic_in sphere_volume' )

    # tetrahedron_area
    #testOperator( '1 tetrahedron_area' )

    # tetrahedron_volume
    #testOperator( '1 tetrahedron_volume' )

    # torus_area
    #testOperator( '12 5 torus_area' )

    # torus_volume
    #testOperator( '20 8 torus_volume' )

    # triangle_area
    #testOperator( '123 456 789 triangle_area' )
    pass


# //******************************************************************************
# //
# //  runInternalOperatorTests
# //
# //******************************************************************************

def runInternalOperatorTests( ):
    # _dump_aliases
    #testOperator( '_dump_aliases' )

    # _dump_operators
    #testOperator( '_dump_operators' )

    # _stats
    #testOperator( '_stats' )
    pass


# //******************************************************************************
# //
# //  runLexicographyOperatorTests
# //
# //******************************************************************************

def runLexicographyOperatorTests( ):
    # add_digits
    #expectResult( '3 4 add_digits', 34 )
    #expectResult( '3 45 add_digits', 345 )
    #expectResult( '34 567 add_digits', 34567 )

    # build_numbers
    #testOperator( '123d build_numbers' )
    #testOperator( '[0-3]d0[3-5] build_numbers' )
    #testOperator( '[246]d[7-9][12] build_numbers' )
    #testOperator( '[123:1] build_numbers' )
    #testOperator( '[123:2] build_numbers' )
    #testOperator( '[123:3] build_numbers' )
    #testOperator( '[1-3:2:3] build_numbers' )
    #testOperator( '[1-38-9:2:3] build_numbers' )
    #testOperator( '[1-3:2][8-9:2] build_numbers' )

    # combine_digits
    #expectResult( '1 9 range combine_digits', 123456789 )

    # duplicate_digits
    #expectResult( '543 2 duplicate_digits', 54343 )
    #expectResult( '1024 1 4 range duplicate_digits', [ 10244, 102424, 1024024, 10241024 ] )

    # erdos_persistence
    #expectResult( '55555555555555557777777777777 erdos_persistence', 12 )

    # find_palindrome
    #testOperator( '-a30 10911 55 find_palindrome' )
    #testOperator( '180 200 range 10 find_palindrome -s1' )

    # get_digits
    #testOperator( '123456789 get_digits' )
    # #expectEqual   30 oeis 85 left

    # is_automorphic
    #testOperator( '1 100 range lambda x is_automorphic filter' )
    #expectResult( '-a30 59918212890625 is_automorphic', 1 )

    # is_kaprekar
    #expectResult( '533170 is_kaprekar', 1 )
    #expectResult( '77777 is_kaprekar', 0 )
    #expectResult( '77778 is_kaprekar', 1 )
    #expectResult( '95121 is_kaprekar', 1 )
    #expectResult( '7272 is_kaprekar', 1 )
    #expectResult( '22223 is_kaprekar', 0 )

    # is_morphic
    #testOperator( '1 100 range lambda x 7 is_morphic filter' )
    #expectEqual( '-a3000 1 1000 range lambda x x is_morphic filter', '-a3000 82576 oeis 58 left' )

    # is_narcissistic
    #expectResult( '152 is_narcissistic', 0 )
    #expectResult( '153 is_narcissistic', 1 )
    #expectResult( '154 is_narcissistic', 0 )

    # is_palindrome
    #expectResult( '101 is_palindrome', 1 )
    #expectResult( '1 22 range is_palindrome', [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ] )
    #expectResult( '1234567890 is_palindrome', 0 )

    # is_pandigital
    #expectResult( '1234567890 is_pandigital', 1 )
    #expectResult( '123456789 is_pandigital', 0 )

    # is_trimorphic
    #testOperator( '1 100 range is_trimorphic' )
    #expectEqual( '1 1000 range lambda x is_trimorphic filter', '33819 oeis 26 left 25 right' )

    # multiply_digits
    #expectEqual( '123456789 multiply_digits', '9 !' )

    # n_persistence
    #expectResult( '77 1 n_persistence', 4 )
    #testOperator( '679 2 n_persistence' )
    #testOperator( '6788 3 n_persistence' )
    #testOperator( '68889 4 n_persistence' )

    # permute_digits
    #testOperator( '12345 permute_digits' )

    # persistence
    #expectResult( '77 persistence', 4 )
    #testOperator( '679 persistence' )
    #testOperator( '6788 persistence' )
    #testOperator( '68889 persistence' )

    # reversal_addition
    #testOperator( '-a20 89 24 reversal_addition' )
    #testOperator( '-a20 80 89 range 24 reversal_addition' )
    #testOperator( '-a20 89 16 24 range reversal_addition' )
    #testOperator( '-a90 14,104,229,999,995 185 reversal_addition' )
    #testOperator( '-a90 14,104,229,999,995 185 reversal_addition is_palindrome' )

    # reverse_digits
    #testOperator( '37 1 8 range * reverse_digits' )
    #testOperator( '37 1 2 9 range range * reverse_digits' )

    # show_erdos_persistence
    #testOperator( '-a30 55555555555555557777777777777 show_erdos_persistence' )

    # show_n_persistence
    #testOperator( '-a60 3 2222222223333333778 3 show_n_persistence' )

    # show_persistence
    #testOperator( '-a20 2222222223333333778 show_persistence' )

    # sum_digits
    #testOperator( '2 32 ** 1 - sum_digits' )
    pass


# //******************************************************************************
# //
# //  runListOperatorTests
# //
# //******************************************************************************

def runListOperatorTests( ):
    # alternate_signs
    #testOperator( '1 10 range alternate_signs' )

    # alternate_signs_2
    #testOperator( '1 10 range alternate_signs_2' )

    # alternating_sum
    #testOperator( '1 10 range alternating_sum' )

    # alternating_sum_2
    #testOperator( '1 10 range alternating_sum_2' )

    # append
    #testOperator( '1 10 range 45 50 range append' )
    #testOperator( '1 10 range 11 20 range append 21 30 range append' )

    # collate
    #testOperator( '[ 1 10 range 1 10 range ] collate' )

    # count
    #expectResult( '1 10 range count', 10 )

    # diffs
    #testOperator( '1 10 range diffs' )
    #testOperator( '1 10 range fib diffs' )

    # diffs2
    #testOperator( '1 10 range diffs2' )
    #testOperator( '1 10 range fib diffs2' )

    # element
    #testOperator( '1 10 range 5 element' )
    #testOperator( '-a25 1 100 range fibonacci 55 element' )

    # exponential_range
    #testOperator( '1.1 1.1 10 exponential_range' )

    # flatten
    #expectEqual( '[ 1 2 [ 3 4 5 ] [ 6 [ 7 [ 8 9 ] ] 10 ] ] flatten', '1 10 range' )

    # geometric_mean
    #testOperator( '1 100 range geometric_mean' )
    #testOperator( '[ 1 10 range 1 20 range 1 30 range ] geometric_mean' )

    # geometric_range
    #testOperator( '2 8 8 geometric_range' )

    # group_elements
    #testOperator( '1 10 range 5 group_elements' )

    # interleave
    #testOperator( '1 10 range 1 10 range interleave' )
    #expectEqual( '1 100 2 range2 2 100 2 range2 interleave', '1 100 range' )

    # intersection
    #testOperator( '1 10 range 1 8 range intersection' )

    # left
    #expectResult( '1 10 range 5 left', [ 1, 2, 3, 4, 5 ] )

    # max_index
    #testOperator( '1 10 range max_index' )

    # min_index
    #testOperator( '1 10 range min_index' )

    # nonzero
    #testOperator( '1 10 range nonzero' )

    # occurrence_cumulative
    #testOperator( '4 100 random_integer_ occurrence_cumulative' )

    # occurrence_ratios
    #testOperator( '4 100 random_integer_ occurrence_ratios' )

    # occurrences
    #testOperator( '4 100 random_integer_ occurrences' )

    # range
    #expectResult( '1 12 range', [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ] )

    # range2
    #testOperator( '1 23 2 range2' )

    # ratios
    #testOperator( '1 10 range fib ratios' )

    # ratios2
    #testOperator( '1 10 range fib ratios2' )

    # reduce
    #testOperator( '[ 4 8 12 ] reduce' )

    # reverse
    #testOperator( '1 10 range reverse' )
    ##testOperator( '1 2 10 range range reverse' )
    ##testOperator( '1 2 10 range reverse range reverse' )
    ##testOperator( '1 2 10 range reverse range' )

    # right
    #expectEqual( '1 10 range 5 right', '6 10 range' )

    # shuffle
    #testOperator( '1 20 range shuffle' )

    # slice
    #testOperator( '1 10 range 3 5 slice' )
    #testOperator( '1 10 range 2 -5 slice' )

    # sort
    #testOperator( '10 1 -1 range2 sort' )

    # sort_descending
    #testOperator( '1 10 range sort_descending' )

    # sublist
    #testOperator( '1 10 range 1 5 sublist' )

    # union
    #testOperator( '1 10 range 11 20 range union' )

    # unique
    #testOperator( '1 10 range unique' )
    #testOperator( '1 10 range 1 10 range append unique' )
    #testOperator( '[ 1 10 range 10 dup ] unique' )

    # zero
    #expectEqual( '-10 10 range zero', '[ 10 ]' )
    #expectEqual( '1 10 range zero', '[ ]' )
    pass


# //******************************************************************************
# //
# //  runLogarithmsOperatorTests
# //
# //******************************************************************************

def runLogarithmsOperatorTests( ):
    # lambertw
    #testOperator( '5 lambertw' )

    # li
    #testOperator( '12 li' )

    # ln
    #testOperator( '1000 ln' )
    #expectEqual( '0 lambda 1 x ** 5 x * + ln 13 x * / limitn', '5 13 /' )

    # log10
    #expectResult( '1000 log10', 3 )

    # log2
    #testOperator( '1000 log2' )

    # logxy
    #testOperator( '6561 3 logxy' )

    # polylog
    #testOperator( '9 3 polylog' )
    pass


# //******************************************************************************
# //
# //  runModifierOperatorTests
# //
# //******************************************************************************

def runModifierOperatorTests( ):
    # [
    #testOperator( '[ "Philadelphia, PA" location "Raleigh, NC" location ] today sunrise' )
    #testOperator( '[ "Philadelphia, PA" "Raleigh, NC" ] today sunrise' )

    # ]
    #testOperator( '2 [ 4 5 6 ] eval_poly' )

    # duplicate_operator
    #testOperator( '2 5 duplicate_operator sqr' )
    #testOperator( '4 6 5 duplicate_operator *' )

    # duplicate_term
    #testOperator( '[ 1 2 10 duplicate_term ] cf' )

    # previous
    #expectResult( '6 previous *', 36 )

    # for_each

    # unlist
    #expectResult( '[ 1 2 ] unlist +', 3 )

    # {
    #testOperator( '"Leesburg, VA" location today { sunrise sunset moonrise moonset }' )
    #testOperator( '"Leesburg, VA" today { sunrise sunset moonrise moonset }' )

    # }
    #testOperator( '1 10 range { is_prime is_pronic is_semiprime }' )
    pass


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    #from rpnNumberTheory import getNthKFibonacciNumberTheSlowWay

    # aliquot
    #testOperator( '276 10 aliquot' )

    # alternating_factorial
    #testOperator( '13 alternating_factorial' )
    #testOperator( '-a20 1 20 range alternating_factorial' )

    # base
    #testOperator( '[ 1 1 1 1 1 1 ] 2 10 range base' )

    #testOperator( '-a30 1 10 range 11 base' )
    #testOperator( '-a30 1 11 range 12 base' )
    #testOperator( '-a30 1 12 range 13 base' )
    #testOperator( '-a30 1 13 range 14 base' )
    #testOperator( '-a30 1 14 range 15 base' )
    #testOperator( '-a30 1 15 range 16 base' )
    #testOperator( '-a30 1 16 range 17 base' )
    #testOperator( '-a30 1 17 range 18 base' )
    #testOperator( '-a30 1 18 range 19 base' )
    #testOperator( '-a30 1 19 range 20 base' )

    # barnesg
    #testOperator( '2 i barnesg' )
    #expectEqual( '-a30 3 12 range barnesg', '-a30 1 10 range superfac' )

    # beta
    #testOperator( '5 2 beta' )

    # calkin_wilf
    #testOperator( '1 100 range calkin_wilf' )

    # carol
    #testOperator( '-a500 773 carol' )
    #expectEqual( '1 25 range carol', '93112 oeis 25 left' )

    # cf
    #testOperator( '1 10 range cf' )

    # count_divisors
    #testOperator( '1024 count_divisors' )
    #expectEqual( '1 104 range count_divisors', '5 oeis 104 left' )

    # crt
    #testOperator( '1 3 range 10 20 range 3 primes crt' )

    # digamma
    #testOperator( '3 digamma' )

    # divisors
    #testOperator( '2 3 ** 3 4 ** * divisors' )
    #testOperator( '12 ! divisors' )

    # double_factorial
    #testOperator( '9 double_factorial' )

    # ecm
    #testOperator( '-a40 10 20 ** random_integer ecm' )

    # egypt
    #testOperator( '45 67 egypt' )

    # euler_brick
    #testOperator( '2 3 make_pyth_3 unlist euler_brick' )

    # euler_phi
    #testOperator( '1 20 range euler_phi' )
    #expectEqual( '1 69 range euler_phi', '10 oeis 69 left' )

    # factor
    #testOperator( '883847311 factor' )
    #testOperator( '1 40 range fibonacci factor -s1' )

    # factorial
    #testOperator( '-a25 -c 23 factorial' )
    #expectEqual( '0 22 range !', '142 oeis 23 left' )

    # fibonacci
    #testOperator( '1 50 range fibonacci' )
    #testOperator( '-c -a8300 39399 fibonacci' )
    #expectEqual( '0 38 range fibonacci', '45 oeis 39 left' )
    #expectResult( '0 100 range fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )

    # fibonorial
    #testOperator( '5 fibonorial' )
    #testOperator( '-a50 24 fibonorial' )

    # generate_polydivisibles
    #testOperator( '3 generate_polydivisibles -r3' )

    # fraction
    #testOperator( '2 sqrt 30 fraction' )

    # frobenius
    #testOperator( '10 20 range 3 primes frobenius' )
    expectEqual( '[ 4, 7, 12 ] frobenius', queryAlpha( 'Frobenius number {4, 7, 12}' ) )
    expectEqual( '[ 23, 29, 47 ] frobenius', queryAlpha( 'Frobenius number {23, 29, 47}' ) )

    # gamma
    #testOperator( '3 gamma' )

    # harmonic
    #testOperator( '34 harmonic' )

    # heptanacci
    #testOperator( '-a200 -c 623 heptanacci' )
    #expectEqual( '0 38 range heptanacci', '122189 oeis 39 left' )
    #expectResult( '0 100 range heptanacci', [ getNthKFibonacciNumberTheSlowWay( i, 7 ) for i in range( 0, 101 ) ] )

    # hexanacci
    #testOperator( '-a300 -c 949 hexanacci' )
    #expectEqual( '0 38 range hexanacci', '1592 oeis 39 left' )
    #expectResult( '0 100 range hexanacci', [ getNthKFibonacciNumberTheSlowWay( i, 6 ) for i in range( 0, 101 ) ] )

    # hyperfactorial
    #testOperator( '-a160 -c 17 hyperfactorial' )

    # is_abundant
    #testOperator( '1 20 range is_abundant' )

    # is_achilles
    #testOperator( '1 20 range is_achilles' )

    # is_deficient
    #testOperator( '1 20 range is_deficient' )

    # is_k_semiprime
    #testOperator( '1 20 range 3 is_k_semiprime' )

    # is_perfect
    #testOperator( '1 30 range is_perfect' )

    # is_powerful
    #testOperator( '1 20 range is_powerful' )

    # is_prime
    #testOperator( '1000 1030 range is_prime' )
    #testOperator( '2049 is_prime' )
    #testOperator( '92348759911 is_prime' )

    # is_polydivisible
    #expectEqual( '3608528850368400786036725 is_polydivisible', '1' )

    # is_pronic
    #testOperator( '1 20 range is_pronic' )

    # is_rough
    #testOperator( '1 20 range 2 is_rough' )

    # is_semiprime
    #testOperator( '12 is_semiprime' )

    # is_smooth
    #testOperator( '128 4 is_smooth' )
    #testOperator( '1 20 range 2 is_smooth' )

    # is_sphenic
    #testOperator( '[ 2 3 5 ] prime is_sphenic' )

    # is_squarefree
    #testOperator( '2013 sqr is_squarefree' )
    #testOperator( '8 primorial is_squarefree' )
    #testOperator( '1 20 range is_squarefree' )

    # is_unusual
    #testOperator( '-a50 81 23 ** is_unusual' )
    #testOperator( '1 20 range is_unusual' )

    # jacobsthal
    #expectEqual( '0 34 range jacobsthal', '1045 oeis 35 left' )

    # kynea
    #expectEqual( '-a20 1 25 range kynea', '93069 oeis 25 left' )

    # leonardo
    #expectEqual( '0 37 range leonardo', '1595 oeis 38 left' )

    # leyland
    #testOperator( '7 8 leyland' )

    # linear_recurrence
    #testOperator( '1 10 range 2 5 range 17 linear_recur' )

    # log_gamma
    #testOperator( '10 log_gamma' )

    # lucas
    #testOperator( '-a21 99 lucas' )
    #expectEqual( '0 36 range lucas', '32 oeis 37 left' )

    # make_cf
    #testOperator( 'e 20 make_cf' )
    #expectEqual( '-a100 2 pi * 3 2 / power 1/x 1 4 / gamma sqr * 100 make_cf', '53002 oeis 100 left' )

    # make_pyth_3
    #testOperator( '12 34 make_pyth_3' )

    # make_pyth_4
    #testOperator( '18 29 make_pyth_4' )
    #expectException( '17 29 make_pyth_4' )

    # merten
    #expectEqual( '1 81 range merten', '2321 oeis 81 left' )

    # mobius
    #testOperator( '20176 mobius' )
    #expectEqual( '1 77 range mobius', '8683 oeis 77 left' )

    # n_fibonacci
    #expectResult( '0 100 range 2 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 2 ) for i in range( 0, 101 ) ] )
    #expectResult( '0 100 range 5 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )
    #expectResult( '0 100 range 10 n_fibonacci', [ getNthKFibonacciNumberTheSlowWay( i, 10 ) for i in range( 0, 101 ) ] )
    #expectResult( '1000 10 n_fibonacci', getNthKFibonacciNumberTheSlowWay( 1000, 10 ) )

    # nth_padovan
    #testOperator( '-c 76 nth_padovan' )
    #expectEqual( '0 45 range nth_padovan', '931 oeis 50 left 46 right' )

    # octanacci
    #testOperator( '-a300 -c 906 octanacci' )
    #expectEqual( '0 39 range octanacci', '79262 oeis 40 left' )
    #expectResult( '0 100 range octanacci', [ getNthKFibonacciNumberTheSlowWay( i, 8 ) for i in range( 0, 101 ) ] )

    # nth_padovan
    #testOperator( '-c 76 nth_padovan' )
    #expectEqual( '0 45 range nth_padovan', '931 oeis 50 left 46 right' )

    # pascal_triangle
    #testOperator( '12 pascal_triangle' )
    #testOperator( '1 10 range pascal_triangle -s1' )

    # pentanacci
    #testOperator( '16 pentanacci' )
    #expectEqual( '-a20 0 37 range pentanacci', '-a20 1591 oeis 38 left' )
    #expectResult( '0 100 range pentanacci', [ getNthKFibonacciNumberTheSlowWay( i, 5 ) for i in range( 0, 101 ) ] )

    # polygamma
    #testOperator( '4 5 polygamma' )

    # primorial
    #testOperator( '1 10 range primorial' )

    # repunit
    #testOperator( '-a20 23 5 repunit' )

    # riesel
    #testOperator( '23 riesel' )

    # sigma
    #testOperator( '1 20 range sigma' )
    #expectEqual( '1 70 range sigma', '203 oeis 70 left' )

    # sigma_k
    #testOperator( '1 20 3 range sigma_k' )
    #expectEqual( '1 50 range 2 sigma_k', '1157 oeis 50 left' )
    #expectEqual( '1 39 range 3 sigma_k', '1158 oeis 39 left' )
    #expectEqual( '1 33 range 4 sigma_k', '1159 oeis 33 left' )
    #expectEqual( '1 29 range 5 sigma_k', '1160 oeis 29 left' )
    #expectEqual( '1 23 range 6 sigma_k', '13954 oeis 23 left' )
    #expectEqual( '1 22 range 7 sigma_k', '13955 oeis 22 left' )
    #expectEqual( '1 20 range 8 sigma_k', '13956 oeis 20 left' )
    #expectEqual( '1 20 range 9 sigma_k', '13957 oeis 20 left' )
    #expectEqual( '1 17 range 10 sigma_k', '13958 oeis 17 left' )
    #expectEqual( '-a20 -p30 1 17 range 11 sigma_k', '-a20 13959 oeis 17 left' )
    #expectEqual( '-a20 -p30 1 16 range 12 sigma_k', '-a20 13960 oeis 16 left' )
    #expectEqual( '-a20 -p30 1 15 range 13 sigma_k', '-a20 13961 oeis 15 left' )
    #expectEqual( '-a20 -p30 1 15 range 14 sigma_k', '-a20 13962 oeis 15 left' )
    #expectEqual( '-a20 -p30 1 14 range 15 sigma_k', '-a20 13963 oeis 14 left' )
    #expectEqual( '-a20 -p30 1 13 range 16 sigma_k', '-a20 13964 oeis 13 left' )
    #expectEqual( '-a25 -p30 1 13 range 17 sigma_k', '-a25 13965 oeis 13 left' )
    #expectEqual( '-a25 -p30 1 12 range 18 sigma_k', '-a25 13966 oeis 12 left' )
    #expectEqual( '-a25 -p30 1 12 range 19 sigma_k', '-a25 13967 oeis 12 left' )
    #expectEqual( '-a25 -p30 1 12 range 20 sigma_k', '-a25 13968 oeis 12 left' )
    #expectEqual( '-a25 -p35 1 12 range 21 sigma_k', '-a25 13969 oeis 12 left' )
    #expectEqual( '-a25 -p35 1 11 range 22 sigma_k', '-a25 13970 oeis 11 left' )
    #expectEqual( '-a25 -p40 1 11 range 23 sigma_k', '-a25 13971 oeis 11 left' )
    #expectEqual( '-a25 -p40 1 11 range 24 sigma_k', '-a25 13972 oeis 11 left' )

    # stern
    #testOperator( '1 100 range stern' )

    # subfactorial
    #testOperator( '-a20 -c 19 subfactorial' )
    # A000166

    # superfactorial
    #testOperator( '-a50 -c 12 superfactorial' )
    #expectEqual( '-a50 0 12 range superfactorial', '178 oeis 13 left' )

    # tetranacci
    #testOperator( '-a30 -c 87 tetranacci' )
    #expectEqual( '0 37 range tetranacci', '78 oeis 38 left' )
    #expectResult( '0 100 range tetranacci', [ getNthKFibonacciNumberTheSlowWay( i, 4 ) for i in range( 0, 101 ) ] )

    # thabit
    #testOperator( '-a20 -c 45 thabit' )
    # A055010

    # tribonacci
    #testOperator( '1 20 range tribonacci' )
    #testOperator( '-c -a2800 10239 tribonacci' )
    #expectEqual( '0 37 range tribonacci', '73 oeis 38 left' )
    #expectResult( '0 100 range tribonacci', [ getNthKFibonacciNumberTheSlowWay( i, 3 ) for i in range( 0, 101 ) ] )

    # trigamma
    #testOperator( '3 trigamma' )

    # unit_roots
    #testOperator( '7 unit_roots' )

    # zeta
    #testOperator( '4 zeta' )


# //******************************************************************************
# //
# //  runPhysicsOperatorTests
# //
# //******************************************************************************

def runPhysicsOperatorTests( ):
    # schwarzchild_radius
    #testOperator( 'earth_mass schwarzchild_radius' )

    # time_dilation
    #testOperator( '1 million miles hour / time_dilation' )
    pass


# //******************************************************************************
# //
# //  runPolygonalOperatorTests
# //
# //******************************************************************************

def runPolygonalOperatorTests( ):
    # centered_decagonal
    #testOperator( '17 centered_decagonal' )

    # centered_heptagonal
    #testOperator( '102 centered_heptagonal' )

    # centered_hexagonal
    #testOperator( '103 centered_hexagonal' )

    # centered_nonagonal
    #testOperator( '104 centered_nonagonal' )

    # centered_octagonal
    #testOperator( '10 centered_octagonal' )

    # centered_pentagonal
    #testOperator( '108 centered_pentagonal' )

    # centered_polygonal
    #testOperator( '108 5 centered_polygonal' )

    # centered_square
    #testOperator( '5 centered_square' )

    # centered_triangular
    #testOperator( '100 centered_triangular' )

    # decagonal
    #testOperator( '151 decagonal' )

    # decagonal_centered_square
    #testOperator( '-a40 9 decagonal_centered_square' )

    # decagonal_heptagonal
    #testOperator( '-a50 8 decagonal_heptagonal' )

    # decagonal_hexagonal
    #testOperator( '-a60 9 decagonal_hexagonal' )

    # decagonal_octagonal
    #testOperator( '-a75 9 decagonal_nonagonal' )

    # decagonal_octagonal
    #testOperator( '-a75 9 decagonal_octagonal' )

    # decagonal_pentagonal
    #testOperator( '-a60 7 decagonal_pentagonal' )

    # decagonal_centered_square
    #testOperator( '-a40 9 decagonal_centered_square' )

    # decagonal_triangular
    #testOperator( '-a40 13 decagonal_triangular' )

    # generalized_pentagonal
    #testOperator( '187 generalized_pentagonal' )

    # heptagonal
    #testOperator( '203 heptagonal' )

    # heptagonal_hexagonal
    #testOperator( '2039 heptagonal_hexagonal' )

    # heptagonal_pentagonal
    #testOperator( '8684 heptagonal_pentagonal' )

    # heptagonal_square
    #testOperator( '222 heptagonal_square' )

    # heptagonal_triangular
    #testOperator( '-a1000 -c 399 heptagonal_triangular' )
    #expectEqual( '-a40 1 14 range heptagonal_triangular', '-a40 46194 oeis 14 left' )

    # hexagonal
    #testOperator( '340 hexagonal' )

    # hexagonal_pentagonal
    #testOperator( '-a250 -c 107 hexagonal_pentagonal' )
    #expectEqual( '-a40 1 14 range hexagonal_pentagonal', '-a40 46178 oeis 14 left' )

    # hexagonal_square
    #testOperator( '-a70 -c 23 hexagonal_square' )
    #expectEqual( '-a70 1 12 range hexagonal_square', '-a40 46177 oeis 12 left' )

    # nonagonal
    #testOperator( '554 nonagonal' )

    # nonagonal_heptagonal
    #testOperator( '-a50 -c 12 nonagonal_heptagonal' )

    # nonagonal_hexagonal
    #testOperator( '-a60 -c 13 nonagonal_hexagonal' )

    # nonagonal_octagonal
    #testOperator( '-a75 -c 14 nonagonal_octagonal' )

    # nonagonal_pentagonal
    #testOperator( '-a60 -c 15 nonagonal_pentagonal' )

    # nonagonal_square
    #testOperator( '-a22 -c 16 nonagonal_square' )

    # nonagonal_triangular
    #testOperator( '-a21 -c 17 nonagonal_triangular' )

    # nth_centered_decagonal
    #testOperator( '1000 nth_centered_decagonal' )

    # nth_centered_heptagonal
    #testOperator( '100000 nth_centered_heptagonal' )

    # nth_centered_hexagonal
    #testOperator( '7785961 nth_centered_hexagonal' )

    # nth_centered_nonagonal
    #testOperator( '5,000,000 nth_centered_nonagonal' )

    # nth_centered_octagonal
    #testOperator( '361 nth_centered_octagonal' )

    # nth_centered_pentagonal
    #testOperator( '9999 nth_centered_pentagonal' )

    # nth_centered_polygonal
    #testOperator( '9999 5 nth_centered_polygonal' )

    # nth_centered_square
    #testOperator( '49 nth_centered_square' )

    # nth_centered_triangular
    #testOperator( '10000 nth_centered_triangular' )

    # nth_decagonal
    #testOperator( '123454321 nth_decagonal' )

    # nth_heptagonal
    #testOperator( '99999 nth_heptagonal' )

    # nth_hexagonal
    #testOperator( '230860 nth_hexagonal' )

    # nth_nonagonal
    #testOperator( '9 6 ** nth_nonagonal' )

    # nth_octagonal
    #testOperator( '8 4 ** 1 + nth_octagonal' )

    # nth_pentagonal
    #testOperator( '5 5 ** 5 + nth_pentagonal' )

    # nth_polygonal
    #testOperator( '12 12 ** 12 nth_polygonal' )

    # nth_square
    #testOperator( '111333111 nth_square' )

    # nth_triangular
    #testOperator( '20706 nth_triangular' )

    # octagonal
    #testOperator( '102 octagonal' )

    # octagonal_heptagonal
    #testOperator( '-a40 -c 8 octagonal_heptagonal' )

    # octagonal_hexagonal
    #testOperator( '-a30 -c 7 octagonal_hexagonal' )

    # octagonal_pentagonal
    #testOperator( '-a15 -c 6 octagonal_pentagonal' )

    # octagonal_square
    #testOperator( '-a25 -c 11 octagonal_square' )

    # octagonal_triangular
    #testOperator( '-a20 -c 10 octagonal_triangular' )

    # pentagonal
    #testOperator( '16 pentagonal' )

    # pentagonal_square
    #testOperator( '-a70 -c 10 pentagonal_square' )

    # pentagonal_triangular
    #testOperator( '-a40 -c 17 pentagonal_triangular' )

    # polygonal
    #testOperator( '9 12 polygonal' )

    # square_triangular
    #testOperator( '-a60 -c 34 square_triangular' )

    # star
    #expectEqual( '1 43 range star', '3154 oeis 43 left' )

    # triangular
    expectEqual( '203 triangular', queryAlpha( '203rd triangular number' ) )


# //******************************************************************************
# //
# //  runPolyhedralOperatorTests
# //
# //******************************************************************************

def runPolyhedralOperatorTests( ):
    # centered_cube
    #testOperator( '1 20 range centered_cube' )
    #testOperator( '100 centered_cube' )
    #expectEqual( '1 38 range centered_cube', '5898 oeis 38 left' )

    # centered_dodecahedral
    #testOperator( '1 20 range centered_dodecahedral' )
    #testOperator( '60 centered_dodecahedral' )
    #expectEqual( '1 36 range centered_dodecahedral', '5904 oeis 36 left' )

    # centered_icosahedral
    #testOperator( '1 20 range centered_icosahedral' )
    #testOperator( '30 centered_icosahedral' )
    #expectEqual( '1 36 range centered_icosahedral', '5902 oeis 36 left' )

    # centered_octahedral
    #testOperator( '1 20 range centered_octahedral' )
    #testOperator( '70 centered_octahedral' )
    #expectEqual( '1 40 range centered_octahedral', '1845 oeis 40 left' )

    # centered_tetrahedral
    #testOperator( '1 20 range centered_tetrahedral' )
    #testOperator( '120 centered_tetrahedral' )
    #expectEqual( '1 39 range centered_tetrahedral', '5894 oeis 39 left' )

    # dodecahedral
    #testOperator( '44 dodecahedral' )

    # icosahedral
    #testOperator( '100 icosahedral' )

    # octahedral
    #testOperator( '23 octahedral' )

    # pentatope
    #testOperator( '12 pentatope' )

    # polytope
    #testOperator( '1 10 range 7 polytope' )
    #testOperator( '10 2 8 range polytope' )
    #testOperator( '1 10 range 2 8 range polytope' )
    #testOperator( '-a20 -c 18 47 polytope' )

    # pyramid
    #testOperator( '304 pyramid' )

    # rhombdodec
    #testOperator( '89 rhombdodec' )

    # stella_octangula
    #testOperator( '3945 stella_octangula' )

    # tetrahedral
    #testOperator( '-a20 19978 tetrahedral' )

    # truncated_octahedral
    #testOperator( '394 truncated_octahedral' )

    # truncated_tetrahedral
    #testOperator( '683 truncated_tetrahedral' )
    pass


# //******************************************************************************
# //
# //  runPowersAndRootsOperatorTests
# //
# //******************************************************************************

def runPowersAndRootsOperatorTests( ):
    # agm
    #testOperator( '1 2 sqrt agm' )

    # cube
    #testOperator( '3 cube' )

    # cube_root
    #testOperator( 'pi cube_root' )

    # exp
    #testOperator( '13 exp' )

    # exp10
    #testOperator( '12 exp10' )

    # expphi
    #testOperator( '100 expphi' )

    # hyper4_2
    #testOperator( '-a160 -c 4 3 hyper4_2' )

    # power
    #testOperator( '4 5 power' )
    #testOperator( '4 1 i power' )
    #testOperator( '1 10 range 2 10 range power' )

    # powmod
    #testOperator( '43 67 9 powmod' )

    # root
    #expectEqual( '8 3 root', '8 cube_root' )

    # square
    #expectEqual( '123 square', '123 123 *' )

    # square_root
    #expectEqual( '2 square_root', '4 4 root' )

    # tetrate
    #testOperator( '3 2 tetrate' )

    # tower
    #testOperator( '-c -a30 [ 2 3 2 ] tower' )

    # tower2
    #testOperator( '-a160 -c [ 4 4 4 ] tower2' )
    pass


# //******************************************************************************
# //
# //  runPrimeNumberOperatorTests
# //
# //******************************************************************************

def runPrimeNumberOperatorTests( ):
    # balanced_prime
    #testOperator( '1 10 range balanced' )
    #testOperator( '53 balanced' )
    #testOperator( '153 balanced' )
    #testOperator( '2153 balanced' )

    # balanced_prime_
    #testOperator( '1 10 range balanced_' )
    #testOperator( '53 balanced_' )
    #testOperator( '153 balanced_' )
    #testOperator( '2153 balanced_' )

    # cousin_prime
    #testOperator( '1 10 range cousin_prime' )
    #testOperator( '77 cousin_prime' )
    #testOperator( '5176 cousin_prime' )

    # cousin_prime_
    #testOperator( '1 10 range cousin_prime_' )
    #testOperator( '4486 cousin_prime_' )
    #testOperator( '192765 cousin_prime_' )

    # double_balanced
    #testOperator( '1 5 range double_balanced' )
    #testOperator( '54 double_balanced' )
    #testOperator( '82154 double_balanced' )

    # double_balanced_
    #testOperator( '1 5 range double_balanced_' )
    #testOperator( '54 double_balanced_' )
    #testOperator( '100000 double_balanced_' )

    # isolated_prime
    #testOperator( '102 isolated_prime' )
    #testOperator( '1902 isolated_prime' )

    # next_prime
    #testOperator( '1 100 range next_prime' )
    #testOperator( '35 next_prime' )
    #testOperator( '8783 next_prime' )
    #testOperator( '142857 next_prime' )
    #testOperator( '-c 6 13 ** 1 + next_prime' )
    #testOperator( '-c 7 13 ** 1 + next_prime' )

    # next_quadruplet_prime
    #testOperator( '8 next_quadruplet_prime' )
    #testOperator( '8871 next_quadruplet_prime' )

    # next_quintuplet_prime
    #testOperator( '147951 next_quintuplet_prime' )
    #testOperator( '2,300,000 next_quintuplet_prime' )

    # nth_prime
    #testOperator( '1 10 range nth_prime' )
    #testOperator( '67 nth_prime' )
    #testOperator( '16467 nth_prime' )
    #testOperator( '-c 13,000,000,000 nth_prime' )
    #testOperator( '-c 256,000,000,000 nth_prime' )

    # nth_quadruplet_prime
    #testOperator( '1 100000 10000 range2 nth_quadruplet_prime' )
    #testOperator( '453456 nth_quadruplet_prime' )
    #testOperator( '74,000,000,000 nth_quadruplet_prime' )

    # nth_quintuplet_prime
    #testOperator( '1 100000 10000 range2 nth_quintuplet_prime' )
    #testOperator( '23887 nth_quintuplet_prime' )
    #testOperator( '13,000,000,000 nth_quintuplet_prime' )

    # polyprime
    #testOperator( '1 5 range 1 5 range polyprime' )
    #testOperator( '4 3 polyprime' )
    #testOperator( '5 8 polyprime' )

    # prime
    #testOperator( '1 101 range prime' )
    #testOperator( '8783 prime' )
    #testOperator( '142857 prime' )
    #testOperator( '367981443 prime' )
    #testOperator( '9113486725 prime' )

    # prime_pi
    #testOperator( '87 prime_pi' )

    # primes
    #testOperator( '1 5 range 5 primes' )
    #testOperator( '1 1 5 range primes' )
    #testOperator( '2 1 5 range primes' )
    #testOperator( '3 1 5 range primes' )
    #testOperator( '4 1 5 range primes' )
    #testOperator( '150 10 primes' )
    #testOperator( '98765 20 primes' )
    #testOperator( '176176176 25 primes' )
    #testOperator( '11,000,000,000 25 primes' )
    #expectEqual( '1 71 primes sqrt floor', '6 oeis 71 left' )

    # quadruplet_prime
    #testOperator( '17 quadruplet_prime' )
    #testOperator( '99831 quadruplet_prime' )

    # quadruplet_prime_
    #testOperator( '17 quadruplet_prime_' )
    #testOperator( '55731 quadruplet_prime_' )

    # quintuplet_prime
    #testOperator( '18 quintuplet_prime' )
    #testOperator( '9387 quintuplet_prime' )

    # quintuplet_prime_
    #testOperator( '62 quintuplet_prime_' )
    #testOperator( '74238 quintuplet_prime_' )

    # safe_prime
    #testOperator( '45 safe_prime' )
    #testOperator( '5199846 safe_prime' )

    # sextuplet_prime
    #testOperator( '29 sextuplet_prime' )
    #testOperator( '1176 sextuplet_prime' )
    #testOperator( '556 sextuplet_prime' )

    # sextuplet_prime_
    #testOperator( '1 sextuplet_prime_' )
    #testOperator( '587 sextuplet_prime_' )
    #testOperator( '835 sextuplet_prime_' )
    #testOperator( '29 sextuplet_prime_' )

    # sexy_prime
    #testOperator( '-c 89,999,999 sexy_prime' )
    #testOperator( '1 sexy_prime' )
    #testOperator( '1487 sexy_prime' )
    #testOperator( '2 sexy_prime' )
    #testOperator( '23235 sexy_prime' )
    #testOperator( '29 sexy_prime' )

    # sexy_prime_
    #testOperator( '1 10 range sexy_prime_' )
    #testOperator( '29 sexy_prime_' )
    #testOperator( '21985 sexy_prime_' )
    #testOperator( '-c 100,000,000 sexy_prime_' )

    # sexy_quadruplet
    #testOperator( '1 10 range sexy_quadruplet' )
    #testOperator( '29 sexy_quadruplet' )
    #testOperator( '-c 289747 sexy_quadruplet' )

    # sexy_quadruplet_
    #testOperator( '1 10 range sexy_quadruplet_' )
    #testOperator( '29 sexy_quadruplet_' )
    #testOperator( '2459 sexy_quadruplet_' )

    # sexy_triplet
    #testOperator( '1 10 range sexy_triplet' )
    #testOperator( '29 sexy_triplet' )
    #testOperator( '-c 593847 sexy_triplet' )
    #testOperator( '-c 8574239 sexy_triplet' )

    # sexy_triplet_
    #testOperator( '1 10 range sexy_triplet_' )
    #testOperator( '52 sexy_triplet_' )
    #testOperator( '5298 sexy_triplet_' )
    #testOperator( '-c 10984635 sexy_triplet_' )

    # sophie_prime
    #testOperator( '1 10 range sophie_prime' )
    #testOperator( '87 sophie_prime' )
    #testOperator( '6,500,000 sophie_prime' )

    # superprime
    #testOperator( '89 superprime' )

    # triple_balanced
    #testOperator( '1 10 range triple_balanced' )
    #testOperator( '5588 triple_balanced' )

    # triple_balanced_
    #testOperator( '1 10 range triple_balanced_' )
    #testOperator( '6329 triple_balanced_' )

    # triplet_prime
    #testOperator( '1 10 range triplet_prime' )
    #testOperator( '192834 triplet_prime' )

    # triplet_prime_
    #testOperator( '1 10 range triplet_prime_' )
    #testOperator( '192834 triplet_prime_' )

    # twin_prime
    #testOperator( '1 10 range twin_prime_' )
    #testOperator( '57454632 twin_prime_' )

    # twin_prime_
    #testOperator( '1 20 range twin_prime' )
    #testOperator( '39485 twin_prime' )
    pass


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
    #testOperator( '150 amps estimate' )
    #testOperator( '150 barns estimate' )
    #testOperator( '150 bytes second / estimate' )
    #testOperator( '150 candelas estimate' )
    #testOperator( '150 cd meter meter * / estimate' )
    #testOperator( '150 coulombs estimate' )
    #testOperator( '150 cubic_feet estimate' )
    #testOperator( '150 cubic_inches estimate' )
    #testOperator( '150 cubic_miles estimate' )
    #testOperator( '150 cubic_mm estimate' )
    #testOperator( '150 cubic_nm estimate' )
    #testOperator( '150 cubic_parsecs estimate' )
    #testOperator( '150 days estimate' )
    #testOperator( '150 degC estimate' )
    #testOperator( '150 degrees estimate' )
    #testOperator( '150 farads estimate' )
    #testOperator( '150 feet estimate' )
    #testOperator( '150 gee * estimate' )
    #testOperator( '150 gallons estimate' )
    #testOperator( '150 grams estimate' )
    #testOperator( '150 GW estimate' )
    #testOperator( '150 Hz estimate' )
    #testOperator( '150 joules estimate' )
    #testOperator( '150 K estimate' )
    #testOperator( '150 kg liter / estimate' )
    #testOperator( '150 light-years estimate' )
    #testOperator( '150 liters estimate' )
    #testOperator( '150 lumens estimate' )
    #testOperator( '150 lux estimate' )
    #testOperator( '150 mach estimate' )
    #testOperator( '150 MB estimate' )
    #testOperator( '150 megapascals estimate' )
    #testOperator( '150 meter second second * / estimate' )
    #testOperator( '150 mhos estimate' )
    #testOperator( '150 microfarads estimate' )
    #testOperator( '150 miles estimate' )
    #testOperator( '150 minutes estimate' )
    #testOperator( '150 months estimate' )
    #testOperator( '150 mph estimate' )
    #testOperator( '150 mps estimate' )
    #testOperator( '150 newtons estimate' )
    #testOperator( '150 ohms estimate' )
    #testOperator( '150 pascal-seconds estimate' )
    #testOperator( '150 pascals estimate' )
    #testOperator( '150 Pg estimate' )
    #testOperator( '150 picofarads estimate' )
    #testOperator( '150 pounds estimate' )
    #testOperator( '150 radians estimate' )
    #testOperator( '150 seconds estimate' )
    #testOperator( '150 sieverts estimate' )
    #testOperator( '150 square_degrees estimate' )
    #testOperator( '150 square_feet estimate' )
    #testOperator( '150 square_inches estimate' )
    #testOperator( '150 square_light-years estimate' )
    #testOperator( '150 square_miles estimate' )
    #testOperator( '150 square_mm estimate' )
    #testOperator( '150 square_nm estimate' )
    #testOperator( '150 stilbs estimate' )
    #testOperator( '150 teaspoons estimate' )
    #testOperator( '150 tesla estimate' )
    #testOperator( '150 tons estimate' )
    #testOperator( '150 tTNT estimate' )
    #testOperator( '150 volts estimate' )
    #testOperator( '150 watts estimate' )
    #testOperator( '150 weeks estimate' )
    #testOperator( '150 years estimate' )
    #testOperator( 'c 150 / estimate' )

    # help - help is handled separately

    # name
    #expectResult( '0 name', 'zero' )
    #expectResult( '1 name', 'one' )
    #expectResult( '10 name', 'ten' )
    #expectResult( '100 name', 'one hundred' )
    #expectResult( '1000 name', 'one thousand' )
    #expectResult( '10000 name', 'ten thousand' )
    #expectResult( '100000 name', 'one hundred thousand' )
    #expectResult( '23 name', 'twenty-three' )
    #expectResult( '47 name', 'forty-seven' )
    #expectResult( '-1 name', 'negative one' )
    #testOperator( '-a100 45 primorial name' )

    # oeis
    #testOperator( '1000 oeis' )
    #testOperator( '250000 randint oeis' )

    # oeis_comment
    #testOperator( '1000 oeis_comment' )
    #testOperator( '250000 randint oeis_comment' )

    # oeis_ex
    #testOperator( '1000 oeis_ex' )
    #testOperator( '250000 randint oeis_ex' )

    # oeis_name
    #testOperator( '1000 oeis_name' )
    #testOperator( '250000 randint oeis_name' )

    # ordinal_name
    #testOperator( '0 10 range ordinal_name -s1' )
    #testOperator( '2 26 ** ordinal_name' )
    #expectResult( '-1 ordinal_name', 'negative first' )
    #expectResult( '0 ordinal_name', 'zeroth' )
    #expectResult( '1 ordinal_name', 'first' )
    #expectResult( '100 ordinal_name', 'one hundredth' )
    #expectResult( '1000 ordinal_name', 'one thousandth' )
    #expectResult( '10000 ordinal_name', 'ten thousandth' )
    #expectResult( '100000 ordinal_name', 'one hundred thousandth' )

    # permute_dice
    #testOperator( '3d6 permute_dice' )
    #testOperator( '4d6x1 permute_dice occurrences -s1' )
    #testOperator( '2d4+1 permute_dice occurrences -s1' )

    # random
    #testOperator( 'random' )

    # random_
    #testOperator( '50 random_' )

    # random_integer
    #testOperator( '100 random_integer' )
    #testOperator( '10 12 ^ random_integer' )

    # random_integer_
    #testOperator( '23 265 random_integer_' )

    # result
    # #testOperator( 'result' )

    # roll_dice
    #testOperator( '20d6 roll_dice' )
    #testOperator( '3d8+5 roll_dice' )
    #testOperator( '10d12x2-4 roll_dice' )

    # roll_dice_
    #testOperator( '3d6 6 roll_dice_' )
    #testOperator( '4d6x1 6 roll_dice_' )

    # set - interactive mode

    # topic - interactive mode

    # value
    #expectResult( '40 minutes value', 40 )
    #expectResult( '756 light-years value', 756 )
    #expectResult( '73 gallons value', 73 )
    pass


# //******************************************************************************
# //
# //  runTrigonometryOperatorTests
# //
# //******************************************************************************

def runTrigonometryOperatorTests( ):
    # acos
    #expectEqual( '0.8 acos', queryAlpha( 'arcos of 0.8 to 19 decimal places' ) )

    # acosh
    #testOperator( '0.6 acosh' )

    # acot
    #testOperator( '0.4 acot' )

    # acoth
    #testOperator( '0.3 acoth' )

    # acsc
    #testOperator( '0.2 acsc' )

    # acsch
    #testOperator( '0.67 acsch' )

    # asec
    #testOperator( '0.4 asec' )

    # asech
    #testOperator( '0.1 asech' )

    # asin
    #testOperator( '0.8 asin' )

    # asinh
    #testOperator( '0.3 asinh' )

    # atan
    #testOperator( '0.2 atan' )

    # atanh
    #testOperator( '0.45 atanh' )

    # cos
    #expectEqual( '45 degrees cos', '2 sqrt 1/x' )
    #testOperator( 'pi radians cos' )
    #expectEqual( '0 lambda 1 x cos - x sqr / limitn', '0.5' )

    # cosh
    #testOperator( 'pi 3 / cosh' )

    # cot
    #testOperator( 'pi 7 / cot' )

    # coth
    #testOperator( 'pi 9 / coth' )

    # csc
    #testOperator( 'pi 12 / csc' )

    # csch
    #testOperator( 'pi 13 / csch' )

    # hypotenuse
    #testOperator( '3 4 hypotenuse' )

    # sec
    #testOperator( 'pi 7 / sec' )

    # sech
    #testOperator( 'pi 7 / sech' )

    # sin
    #expectEqual( 'pi 4 / sin', '2 sqrt 1/x' )
    #expectEqual( '0 lambda 2 x * sin 3 x * sin / limitn', '2 3 /' )

    # sinh
    #testOperator( 'pi 2 / sinh' )

    # tan
    #testOperator( 'pi 3 / tan' )

    # tanh
    #testOperator( 'pi 4 / tanh' )
    pass


# //******************************************************************************
# //
# //  runAdvancedTests
# //
# //  This is just for tests that are more complex than the single operator
# //  tests.
# //
# //******************************************************************************

def runAdvancedTests( ):
    #testOperator( '2016 dst_end 2016 dst_start - 2016-12-31 2016-01-01 - /' )
    #testOperator( '"Leesburg, VA" today 0 20 range days + echo daytime collate -s1' )
    #testOperator( '1 1 thousand range lambda x is_polydivisible filter' )
    #expectEqual( '38[147][246]5[246][124679][246][124679]0 build_numbers lambda x is_polydivisible filter lambda x is_pandigital filter', '[ 3816547290 ]' )
    pass


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
    ( 'combinatorics',      runCombinatoricsOperatorTests ),
    ( 'complex',            runComplexMathOperatorTests ),
    ( 'constant',           runConstantOperatorTests ),
    ( 'conversion',         runConversionOperatorTests ),
    ( 'date_time',          runDateTimeOperatorTests ),
    ( 'function',           runFunctionOperatorTests ),
    ( 'geography',          runGeographyOperatorTests ),
    ( 'geometry',           runGeometryOperatorTests ),
    ( 'lexicography',       runLexicographyOperatorTests ),
    ( 'list',               runListOperatorTests ),
    ( 'logarithms',         runLogarithmsOperatorTests ),
    ( 'modifier',           runModifierOperatorTests ),
    ( 'number_theory',      runNumberTheoryOperatorTests ),
    ( 'physics',            runPhysicsOperatorTests ),
    ( 'polygonal',          runPolygonalOperatorTests ),
    ( 'polyhedral',         runPolyhedralOperatorTests ),
    ( 'powers_and_roots',   runPowersAndRootsOperatorTests ),
    ( 'prime_number',       runPrimeNumberOperatorTests ),
    ( 'settings',           runSettingsOperatorTests ),
    ( 'special',            runSpecialOperatorTests ),
    ( 'trigonometry',       runTrigonometryOperatorTests ),
    ( 'advanced',           runAdvancedTests ),

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
        for test in rpnTests:
            rpnTests[ test ]( )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    getDataPath( )
    loadUnitNameData( )
    client = initializeAlpha( )

    runTests( sys.argv[ 1 : ] )

