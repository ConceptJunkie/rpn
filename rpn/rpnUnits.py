#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUnits.py
# //
# //  RPN command-line calculator unit conversion declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import fadd, fdiv, fmul, fprod, log, mpf, mpmathify, pi, power

from rpn.rpnConstantUtils import *
from rpn.rpnUnitClasses import RPNUnitInfo, RPNUnitTypeInfo


# jansky (Jy)
# a unit used in radio astronomy to measure the strength, or more precisely the flux
# density, of radio signals from space. In measuring signal strength, it's necessary
# to take into account both the area of the receiving antenna and the width of the
# frequency band in which the signal occurs. Accordingly, one jansky equals a flux
# of 10-26 watts per square meter of receiving area per hertz of frequency band
# (W/m2Hz). Although it is not an SI unit, the jansky is approved by the
# International Astronomical Union and is widely used by astronomers. It honors
# Karl G. Jansky (1905-1950), the American electrical engineer who discovered
# radio waves from space in 1930.  The jansky is sometimes called the flux unit.

#langley (Ly)
# a CGS unit of heat transmission equal to one thermochemical calorie per
# square centimeter, or exactly 41.84 kilojoules per square meter (kJ/m2).
# Named for the American astronomer Samuel P. Langley (1834-1906), the langley
# is used to express the rate of solar radiation received by the earth.

# lunar day
# another name for the tidal day, a unit of time equal to 24 hours 50 minutes
# used in tidal predictions.

# MED
# a common symbol for "minimum erythemal dose," the smallest amount of ultraviolet
# radiation that produces observable reddening (erythema) of the skin. (Skin is
# sensitive to reddening by radiation in only a narrow band of wavelengths around
# 300 nanometers.) The MED obviously varies from one person to another.  Doctors
# and tanning salon operators typically use a value of 200 joules per square meter
# (J/m2), which represents the MED of a highly sensitive individual; persons with
# dark skin have MED's in the range of 1000 J/m2. Regulatory agencies are moving
# to use of the standard erythemal dose (SED), a unit equal to exactly 100 J/m2.
# In tanning, a dose rate of one MED per hour is equivalent to 55.55 milliwatts
# per square meter of skin surface.

# //******************************************************************************
# //
# //  unitOperators
# //
# //  unit name : unitType, representation, plural, abbrev,
# //              aliases, categories,
# //              description
# //
# //  When unit types are multiplied in compound units, they need to be
# //  specified in alphabetical order in the name, but not the representations.
# //
# //******************************************************************************

unitOperators = {
    # _null_type - used internally
    '_null_unit' :
        RPNUnitInfo( '_null_type', '_null_unit', '', [ ], [ ],
                     '''
This unit type is used internally by rpnChilada.
''' ),

    # acceleration
    'celo' :
        RPNUnitInfo( 'acceleration', 'celos', '', [ ], [ 'CGS' ],
                     '''
The celo is a unit of acceleration equal to the acceleration of a body whose
velocity changes uniformly by 1 foot (0.3048 meter) per second in 1 second."

Ref:  http://automationwiki.com/index.php/Engineering_Units_-_Celo
''' ),

    'galileo' :
        RPNUnitInfo( 'acceleration', 'galileos', '', [ 'gal', 'gals' ], [ 'CGS' ],
                     '''
The gal, sometimes called galileo after Galileo Galilei, is a unit of
acceleration used extensively in the science of gravimetry.  The gal is defined
as 1 centimeter per second squared (1 cm/s2).  The milligal (mGal) and microgal
(uGal) refer respectively to one thousandth and one millionth of a gal.

The gal is not part of the International System of Units (known by its
French-language initials "SI").  In 1978 the CIPM decided that it was
permissible to use the gal "with the SI until the CIPM considers that [its] use
is no longer necessary".  However, use of the gal is deprecated by ISO
80000-3:2006.
''' ),

    'leo' :
        RPNUnitInfo( 'acceleration', 'leos', '', [ ], [ 'CGS' ],
                     '''
The leo is a unit of acceleration equal to 10 meters/second^2, which is 1000
times the acceleration represented by the galileo, and is very close to the
acceleration due to gravity on the surface of the Earth.

Ref:  http://automationwiki.com/index.php/Engineering_Units_-_Leo
''' ),

    'meter/second^2' :
        RPNUnitInfo( 'acceleration', 'meters/second^2', '', [ ], [ 'SI' ],
                     '''
''' ),


    # amount of substance
    'mole' :
        RPNUnitInfo( 'amount_of_substance', 'moles', 'mol', [ 'einstein', 'einsteins' ], [ 'SI' ],
                     '''
''' ),

    # angle
    'arcminute' :
        RPNUnitInfo( 'angle', 'arcminutes', '', [ 'arcmin', 'arcmins' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'arcsecond' :
        RPNUnitInfo( 'angle', 'arcseconds', 'arcsec',
                     [ 'arcsec', 'arcsecs' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'centrad' :
        RPNUnitInfo( 'angle', 'centrads', '',
                     [ ], [ 'mathematics', 'science' ],
                     '''
''' ),

    'circle' :
        RPNUnitInfo( 'angle', 'circles', '', [ ], [ 'mathematics' ],
                     '''
The whole circle, all 360 degrees.
''' ),

    'degree' :
        RPNUnitInfo( 'angle', 'degrees', 'deg',
                     [ ], [ 'astronomy', 'mathematics', 'traditional' ],
                     '''
The traditional degree, 1/360th of a circle.
''' ),

    'furman' :
        RPNUnitInfo( 'angle', 'furmans', '', [ ], [ 'non-standard' ],
                     '''
From https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement#Furman:

The Furman is a unit of angular measure equal to 1/65,536 of a circle, or just
under 20 arcseconds.  It is named for Alan T. Furman, the American
mathematician who adapted the CORDIC algorithm for 16-bit fixed-point
arithmetic sometime around 1980.
''' ),

    'grad' :
        RPNUnitInfo( 'angle', 'grads', '', [ 'gon', 'gons' ], [ 'mathematics' ],
                     '''
''' ),

    'octant' :
        RPNUnitInfo( 'angle', 'octants', '', [ ], [ 'mathematics' ],
                     '''
''' ),

    'pointangle' :
        RPNUnitInfo( 'angle', 'pointangles', '', [ ], [ 'navigation' ],
                     '''
''' ),

    'quadrant' :
        RPNUnitInfo( 'angle', 'quadrants', '', [ ], [ 'mathematics' ],
                     '''
''' ),

    'quintant' :
        RPNUnitInfo( 'angle', 'quintants', '', [ ], [ 'mathematics' ],
                     '''
''' ),

    'radian' :
        RPNUnitInfo( 'angle', 'radians', '', [ ], [ 'mathematics', 'SI' ],
                     '''
''' ),

    'sextant' :
        RPNUnitInfo( 'angle', 'sextants', '', [ 'flat', 'flats' ], [ 'mathematics' ],
                     '''
''' ),

    'streck' :
        RPNUnitInfo( 'angle', 'strecks', '', [ ], [ 'Sweden' ],
                     '''
''' ),

    # area
    'acre' :
        RPNUnitInfo( 'area', 'acres', 'ac', [ ], [ 'U.S.', 'U.K.' ],
                     '''
''' ),

    'are' :
        RPNUnitInfo( 'area', 'ares', 'a', [ ], [ 'SI' ],
                     '''
''' ),

    'barn' :
        RPNUnitInfo( 'area', 'barns', '', [ 'bethe', 'bethes', 'oppenheimer', 'oppenheimers' ], [ 'science' ],
                     '''
''' ),

    'bovate' :
        RPNUnitInfo( 'area', 'bovates', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'carucate' :
        RPNUnitInfo( 'area', 'carucates', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'circular_inch' :
        RPNUnitInfo( 'area', 'circular_inch', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'circular_mil' :
        RPNUnitInfo( 'area', 'circular_mils', 'cmil', [ ], [ 'U.S.' ],
                     '''
A circular mil is a unit of area, equal to the area of a circle with a
diameter of one mil (one thousandth of an inch).  It corresponds to 5.067x10e-4
mm^2.  It is a unit intended for referring to the area of a wire with a
circular cross section.  As the area in circular mils can be calculated without
reference to pi, the unit makes conversion between cross section and diameter
of a wire considerably easier.

Ref:  https://en.wikipedia.org/wiki/Circular_mil
''' ),

    'foot^2' :
        RPNUnitInfo( 'area', 'foot^2', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'homestead' :
        RPNUnitInfo( 'area', 'homesteads', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'imperial_square' :
        RPNUnitInfo( 'area', 'imperial_squares', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'meter^2' :
        RPNUnitInfo( 'area', 'meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'morgen' :
        RPNUnitInfo( 'area', 'morgens', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'nanoacre' :
        RPNUnitInfo( 'area', 'nanoacres', 'nac', [ ], [ 'computing' ],
                     '''
''' ),

    'outhouse' :
        RPNUnitInfo( 'area', 'outhouse', '', [ ], [ 'science', 'humorous' ],
                     '''
''' ),

    'rood' :
        RPNUnitInfo( 'area', 'roods', '', [ 'farthingdale' ], [ 'U.K.' ],
                     '''
''' ),

    'section' :
        RPNUnitInfo( 'area', 'sections', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'shed' :
        RPNUnitInfo( 'area', 'sheds', '', [ ], [ 'science' ],
                     '''
''' ),

    'township' :
        RPNUnitInfo( 'area', 'townships', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'virgate' :
        RPNUnitInfo( 'area', 'virgates', '', [ ], [ 'imperial' ],
                     '''
''' ),

    # capacitance
    'abfarad' :
        RPNUnitInfo( 'capacitance', 'abfarads', 'abF', [ ], [ 'CGS' ],
                     '''
''' ),

    'ampere^2*second^4/kilogram*meter^2' :
        RPNUnitInfo( 'capacitance', 'ampere^2*second^4/kilogram*meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'farad' :
        RPNUnitInfo( 'capacitance', 'farads', 'F', [ ], [ 'SI' ],
                     '''
The SI unit for capacitance.
''' ),

    'jar' :
        RPNUnitInfo( 'capacitance', 'jars', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'statfarad' :
        RPNUnitInfo( 'capacitance', 'statfarads', 'statF', [ ], [ 'CGS' ],
                     '''
''' ),

    # charge
    'abcoulomb' :
        RPNUnitInfo( 'charge', 'abcoulombs', 'abC', [ ], [ 'CGS' ],
                     '''
''' ),

    'coulomb' :
        RPNUnitInfo( 'charge', 'coulombs', 'C', [ ], [ 'SI' ],
                     '''
''' ),

    'franklin' :
        RPNUnitInfo( 'charge', 'franklins', 'Fr', [ ], [ 'CGS' ],
                     '''
''' ),

    'faraday' :
        RPNUnitInfo( 'charge', 'faradays', 'Fd', [ ], [ 'natural' ],   # electron_charge * Avogradro's number!
                     '''
''' ),

    'statcoulomb' :
        RPNUnitInfo( 'charge', 'statcoulombs', 'statC', [ 'esu_charge' ], [ 'CGS' ],
                     '''
''' ),

    # catalysis
    'enzyme_unit' :
        RPNUnitInfo( 'catalysis', 'enzyme_units', '',    # 'U' is the symbol, but that is already used for Uranium
                     [ 'IU' ], [ 'SI' ],
                     '''
The enzyme unit, or international unit for enzyme is a unit of enzyme's
catalytic activity.

1 U (umol/min) is defined as the amount of the enzyme that catalyzes the
conversion of one micromole of substrate per minute under the specified
conditions of the assay method.

The specified conditions will usually be the optimum conditions, which
including but not limited to temperature, pH and substrate concentration, that
yield the maximal substrate conversion rate for that particular enzyme. In some
assay method, one usually takes a temperature of 25 degrees C.

The enzyme unit was adopted by the International Union of Biochemistry in 1964.
Since the minute is not an SI base unit of time, the enzyme unit is discouraged
in favor of the katal, the unit recommended by the General Conference on
Weights and Measures in 1978 and officially adopted in 1999.

Ref:  https://en.wikipedia.org/wiki/Enzyme_unit
''' ),

    'katal' :
        RPNUnitInfo( 'catalysis', 'katals', 'kat', [ ], [ 'SI' ],
                     '''
The katal ('kat') is the unit of catalytic activity in the International System
of Units (SI).  It is a derived SI unit for quantifying the catalytic activity
of enzymes (that is, measuring the enzymatic activity level in enzyme
catalysis) and other catalysts.

The General Conference on Weights and Measures and other international
organizations recommend use of the katal.  It replaces the non-SI enzyme unit
of catalytic activity.  Enzyme units are, however, still more commonly used
than the katal, especially in biochemistry.

Ref:  https://en.wikipedia.org/wiki/Katal
''' ),

    'mole/second' :
        RPNUnitInfo( 'catalysis', 'mole/second', '', [ ], [ 'SI' ],
                     '''
''' ),


# constant - Constant is a special type that is immediately converted to a numerical value when used.
#            It's not intended to be used as a unit, per se.  Also, these units are in order of their
#            value instead of alphabetical order like all the others
    'decillionth' :
        RPNUnitInfo( 'constant', 'decillionths', '', [ ], [ 'constant' ],
                     '''
One decillionth:  10e-33 or 1/1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'nonillionth' :
        RPNUnitInfo( 'constant', 'nonillionths', '', [ ], [ 'constant' ],
                     '''
One nonillionth:  10e-30 or 1/1,000,000,000,000,000,000,000,000,000,000
''' ),

    'octillionth' :
        RPNUnitInfo( 'constant', 'octillionths', '', [ ], [ 'constant' ],
                     '''
One octillionth:  10e-27 or 1/1,000,000,000,000,000,000,000,000,000
''' ),

    # 'y' can't be used here since it's an operator
    'septillionth' :
        RPNUnitInfo( 'constant', 'septillionths', '', [ 'yocto' ], [ 'constant' ],
                     '''
One septillionth:  10e-24 or 1/1,000,000,000,000,000,000,000,000
''' ),

    # 'z' can't be used here since it's an operator
    'sextillionth' :
        RPNUnitInfo( 'constant', 'sextillionths', '', [ 'zepto' ], [ 'constant' ],
                     '''
One sextillionth:  10e-21 or 1/1,000,000,000,000,000,000,000
''' ),

    # 'a' can't be used here since it's used for 'are'
    'quintillionth' :
        RPNUnitInfo( 'constant', 'quintillionths', '', [ 'atto' ], [ 'constant' ],
                     '''
One quintillionth:  10e-18 or 1/1,000,000,000,000,000,000
''' ),

    'quadrillionth' :
        RPNUnitInfo( 'constant', 'quadrillionths', 'f', [ 'femto' ], [ 'constant' ],
                     '''
One quadrillionth:  10e-15 or 1/1,000,000,000,000,000
''' ),

    'trillionth' :
        RPNUnitInfo( 'constant', 'trillionths', 'p', [ 'pico' ], [ 'constant' ],
                     '''
One trillionth:  10e-12 or 1/1,000,000,000,000
''' ),

    'billionth' :
        RPNUnitInfo( 'constant', 'billionths', 'n', [ 'nano' ], [ 'constant' ],
                     '''
One billionth:  10e-9 or 1/1,000,000,000
''' ),

    'millionth' :
        RPNUnitInfo( 'constant', 'millionths', 'u', [ 'micro' ], [ 'constant' ],
                     '''
One millionth:  10e-6 or 1/1,000,000
''' ),

    # 'm' can't be used here since it's used for 'meter'
    'thousandth' :
        RPNUnitInfo( 'constant', 'thousandths', '', [ 'milli' ], [ 'constant' ],
                     '''
One thousandth:  10e-3 or 1/1,000
''' ),

    'percent' :
        RPNUnitInfo( 'constant', 'percent', '%', [ 'hundredth', 'centi' ], [ 'constant' ],
                     '''
One hundredth:  10e-2 or 1/100
''' ),

    'tenth' :
        RPNUnitInfo( 'constant', 'tenths', '', [ 'deci', 'tithe' ], [ 'constant' ],
                     '''
One tenth:  10e-1 or 1/10
''' ),

    'quarter' :
        RPNUnitInfo( 'constant', 'quarters', '', [ 'fourth', 'fourths' ], [ 'constant' ],
                     '''
One quarter:  1/4 or 0.25
''' ),

    'third' :
        RPNUnitInfo( 'constant', 'thirds', '',
                     [ ], [ 'constant' ],
                     '''
One third:  1/3 or 0.333333...
''' ),

    'half' :
        RPNUnitInfo( 'constant', 'halves', '', [ ], [ 'constant' ],
                     '''
One half:  1/2 or 0.5
''' ),

    'unity' :
        RPNUnitInfo( 'constant', 'unities', '', [ 'one', 'ones' ], [ 'constant' ],
                     '''
Unity, one, 1
''' ),

    'two' :
        RPNUnitInfo( 'constant', 'twos', '', [ 'pair', 'pairs' ], [ 'constant' ],
                     '''
two, 2
''' ),

    'three' :
        RPNUnitInfo( 'constant', 'threes', '', [ ], [ 'constant' ],
                     '''
three, 3
''' ),

    'four' :
        RPNUnitInfo( 'constant', 'fours', '', [ ], [ 'constant' ],
                     '''
four, 4
''' ),

    'five' :
        RPNUnitInfo( 'constant', 'fives', '', [ ], [ 'constant' ],
                     '''
five, 5
''' ),

    'six' :
        RPNUnitInfo( 'constant', 'sixes', '', [ ], [ 'constant' ],
                     '''
six, 6
''' ),

    'seven' :
        RPNUnitInfo( 'constant', 'sevens', '', [ ], [ 'constant' ],
                     '''
seven, 7
''' ),

    'eight' :
        RPNUnitInfo( 'constant', 'eights', '', [ ], [ 'constant' ],
                     '''
eight, 8
''' ),

    'nine' :
        RPNUnitInfo( 'constant', 'nines', '', [ ], [ 'constant' ],
                     '''
nine, 9
''' ),

    'ten' :
        RPNUnitInfo( 'constant', 'tens', '', [ 'deca', 'deka', 'dicker', 'dickers' ], [ 'constant' ],
                     '''
Ten:  10e1, or 10
''' ),

    'eleven' :
        RPNUnitInfo( 'constant', 'elevens', '', [ ], [ 'constant' ],
                     '''
eleven, 11
''' ),

    'twelve' :
        RPNUnitInfo( 'constant', 'twelve', '', [ 'dozen', 'dozens' ], [ 'constant' ],
                     '''
twelve, 12

A dozen is 12.
''' ),

    'thirteen' :
        RPNUnitInfo( 'constant', 'thirteens', '', [ 'bakers_dozen', 'bakers_donzens' ], [ 'constant' ],
                     '''
thirteen, 13

A baker's dozen is 13.
''' ),

    'fourteen' :
        RPNUnitInfo( 'constant', 'fourteens', '', [ ], [ 'constant' ],
                     '''
fourteen, 14
''' ),

    'fifteen' :
        RPNUnitInfo( 'constant', 'fifteens', '', [ ], [ 'constant' ],
                     '''
fifteen, 15
''' ),

    'sixteen' :
        RPNUnitInfo( 'constant', 'sixteens', '', [ ], [ 'constant' ],
                     '''
sixteen, 16
''' ),

    'seventeen' :
        RPNUnitInfo( 'constant', 'seventeens', '', [ ], [ 'constant' ],
                     '''
seventeen, 17
''' ),

    'eighteen' :
        RPNUnitInfo( 'constant', 'eighteens', '', [ ], [ 'constant' ],
                     '''
eighteen, 18
''' ),

    'nineteen' :
        RPNUnitInfo( 'constant', 'nineteens', '', [ ], [ 'constant' ],
                     '''
nineteen, 19
''' ),

    'twenty' :
        RPNUnitInfo( 'constant', 'twenties', '', [ 'score', 'scores' ], [ 'constant' ],
                     '''
twenty, 20
''' ),

    'thirty' :
        RPNUnitInfo( 'constant', 'thirties', '', [ ], [ 'constant' ],
                     '''
thirty, 30
''' ),

    'forty' :
        RPNUnitInfo( 'constant', 'forties', '', [ 'flock', 'flocks', ], [ 'constant' ],
                     '''
forty, 40

A flock is an archaic name for 40.
''' ),

    'fifty' :
        RPNUnitInfo( 'constant', 'fifties', '', [ ], [ 'constant' ],
                     '''
fifty, 50
''' ),

    'sixty' :
        RPNUnitInfo( 'constant', 'sixties', '', [ 'shock', 'shocks', 'shook', 'shooks', ], [ 'constant' ],
                     '''
sicty, 60

A shock is an archaic name for 60.
''' ),

    'seventy' :
        RPNUnitInfo( 'constant', 'seventies', '', [ ], [ 'constant' ],
                     '''
seventy, 70
''' ),

    'eighty' :
        RPNUnitInfo( 'constant', 'eighties', '', [ ], [ 'constant' ],
                     '''
eighty, 80
''' ),

    'ninety' :
        RPNUnitInfo( 'constant', 'nineties', '', [ ], [ 'constant' ],
                     '''
ninety, 90
''' ),

    'hundred' :
        RPNUnitInfo( 'constant', 'hundreds', '', [ 'hecto', 'toncount', 'toncounts' ], [ 'constant' ],
                     '''
One hundred:  10e2, or 100
''' ),

    'long_hundred' :
        RPNUnitInfo( 'constant', 'long_hundreds', '', [ ], [ 'constant', 'obsolete' ],
                     '''
\'long\' hundred is an archaic term for 120.
''' ),

    'gross' :
        RPNUnitInfo( 'constant', 'gross', '', [ ], [ 'constant' ],
                     '''
A gross is a dozen dozen, or 144.
''' ),

    'thousand' :
        RPNUnitInfo( 'constant', 'thousands', 'k', [ 'kilo', 'chiliad' ], [ 'constant' ],
                     '''
One thousand:  10e3, or 1,000
''' ),

    'great_gross' :
        RPNUnitInfo( 'constant', 'great_gross', '', [ ], [ 'constant' ],
                     '''
A great gross is a dozen gross, or 1728.
''' ),

    'million' :
        RPNUnitInfo( 'constant', 'million', 'M', [ 'mega', 'megas' ], [ 'constant' ],
                     '''
One million:  10e6 or 1,000,000
''' ),

    # 'G' can't be used here since it's used for 'standard gravity'
    'billion' :
        RPNUnitInfo( 'constant', 'billion', '', [ 'giga', 'gigas', 'milliard', 'milliards' ], [ 'constant' ],
                     '''
One billion:  10e9 or 1,000,000,000
''' ),

    # 'T' can't be used here since it's used for 'tesla'
    'trillion' :
        RPNUnitInfo( 'constant', 'trillions', '', [ 'tera' ], [ 'constant' ],
                     '''
One trillion:  10e12 or 1,000,000,000,000
''' ),

    # 'P' can't be used here since it's used for 'Phosphorus'
    'quadrillion' :
        RPNUnitInfo( 'constant', 'quadrillions', '',
                     [ 'peta', 'petas', 'billiard', 'billiards' ], [ 'constant' ],
                     '''
One quadrillion:  10e15 or 1,000,000,000,000,000
''' ),

    'quintillion' :
        RPNUnitInfo( 'constant', 'quintillions', 'E', [ 'exa' ], [ 'constant' ],
                     '''
One quintillion:  10e18 or 1,000,000,000,000,000,000
''' ),

    'sextillion' :
        RPNUnitInfo( 'constant', 'sextillions', 'Z',
                     [ 'zetta', 'zettas', 'trilliard', 'trilliards' ], [ 'constant' ],
                     '''
One sextillion:  10e21 or 1,000,000,000,000,000,000,000
''' ),

    # 'Y' can't be used here since it's used for 'Yttrium'
    'septillion' :
        RPNUnitInfo( 'constant', 'septillions', '', [ 'yotta' ], [ 'constant' ],
                     '''
One septillion:  10e24 or 1,000,000,000,000,000,000,000,000
''' ),

    'octillion' :
        RPNUnitInfo( 'constant', 'octillions', '', [ ], [ 'constant' ],
                     '''
One octillion:  10e27 or 1,000,000,000,000,000,000,000,000,000
''' ),

    'nonillion' :
        RPNUnitInfo( 'constant', 'nonillions', '', [ ], [ 'constant' ],
                     '''
One nonillion:  10e30 or 1,000,000,000,000,000,000,000,000,000,000
''' ),

    'decillion' :
        RPNUnitInfo( 'constant', 'decillion', '', [ ], [ 'constant' ],
                     '''
One decillion:  10e33 or 1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'undecillion' :
        RPNUnitInfo( 'constant', 'undecillions', '', [ ], [ 'constant' ],
                     '''
One undecillion:  10e36
''' ),

    'duodecillion' :
        RPNUnitInfo( 'constant', 'duodecillions', '', [ ], [ 'constant' ],
                     '''
One duodecillion:  10e39
''' ),

    'tredecillion' :
        RPNUnitInfo( 'constant', 'tredecillions', '', [ ], [ 'constant' ],
                     '''
One tredecillion:  10e42
''' ),

    'quattuordecillion' :
        RPNUnitInfo( 'constant', 'quattuordecillions', '',
                     [ ], [ 'constant' ],
                     '''
One quattuordecillion:  10e45
''' ),

    'quindecillion' :
        RPNUnitInfo( 'constant', 'quindecillion', '', [ 'quinquadecillion' ], [ 'constant' ],
                     '''
One quindecillion:  10e48
''' ),

    'sexdecillion' :
        RPNUnitInfo( 'constant', 'sexdecillions', '', [ ], [ 'constant' ],
                     '''
One sexdecillion:  10e51
''' ),

    'septendecillion' :
        RPNUnitInfo( 'constant', 'septemdecillions', '', [ ], [ 'constant' ],
                     '''
One septendecillion:  10e54
''' ),

    'octodecillion' :
        RPNUnitInfo( 'constant', 'octodecillions', '', [ ], [ 'constant' ],
                     '''
One octodecillion:  10e57
''' ),

    'novemdecillion' :
        RPNUnitInfo( 'constant', 'novemdecillions', '', [ 'novendecillion' ], [ 'constant' ],
                     '''
One novemdecillion:  10e60
''' ),

    'vigintillion' :
        RPNUnitInfo( 'constant', 'vigintillions', '', [ ], [ 'constant' ],
                     '''
One vigintdecillion:  10e63
''' ),

    'googol' :
        RPNUnitInfo( 'constant', 'googols', '', [ ], [ 'constant' ],
                     '''
One googol:  10e100 or ten duotrigintillion, famously named in 1920 by
9-year-old Milton Sirotta.
''' ),

    'centillion' :
        RPNUnitInfo( 'constant', 'centillion', '', [ ], [ 'constant' ],
                     '''
One centillion:  10e303
''' ),

    # current
    'abampere' :
        RPNUnitInfo( 'current', 'abamperes', 'abA',
                     [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ],
                     '''
''' ),

    'ampere' :
        RPNUnitInfo( 'current', 'amperes', 'A',
                     [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ],
                     '''
''' ),

    'statampere' :
        RPNUnitInfo( 'current', 'statamperes', 'statA',
                     [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ],
                     '''
''' ),

    # data_rate
    'bit/second' :
        RPNUnitInfo( 'data_rate', 'bits/second', 'bps', [ 'bips' ], [ 'computing' ],
                     '''
''' ),

    'byte/second' :
        RPNUnitInfo( 'data_rate', 'bytes/second', 'Bps', [ ], [ 'computing' ],
                     '''
''' ),

    'oc1' :
        RPNUnitInfo( 'data_rate', 'x_oc1', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc3' :
        RPNUnitInfo( 'data_rate', 'x_oc3', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc12' :
        RPNUnitInfo( 'data_rate', 'x_oc12', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc24' :
        RPNUnitInfo( 'data_rate', 'x_oc24', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc48' :
        RPNUnitInfo( 'data_rate', 'x_oc24', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc192' :
        RPNUnitInfo( 'data_rate', 'x_oc192', '', [ ], [ 'computing' ],
                     '''
''' ),

    'oc768' :
        RPNUnitInfo( 'data_rate', 'x_oc768', '', [ ], [ 'computing' ],
                     '''
''' ),

    'usb1' :
        RPNUnitInfo( 'data_rate', 'x_usb1', '', [ ], [ 'computing' ],
                     '''
''' ),

    'usb2' :
        RPNUnitInfo( 'data_rate', 'x_usb2', '', [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.0' :
        RPNUnitInfo( 'data_rate', 'x_usb3.0', '', [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.1' :
        RPNUnitInfo( 'data_rate', 'x_usb3.1', '', [ ], [ 'computing' ],
                     '''
''' ),

    # density
    'kilogram/meter^3' :
        RPNUnitInfo( 'density', 'kilogram/meter^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    # dynamic_viscosity
    'kilogram/meter*second' :
        RPNUnitInfo( 'dynamic_viscosity', 'kilogram/meter*second', '', [ ], [ 'SI' ],
                     '''
''' ),

    'poise' :
        RPNUnitInfo( 'dynamic_viscosity', 'poise', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'reynolds' :
        RPNUnitInfo( 'dynamic_viscosity', 'reynolds', '', [ 'reyn', 'reyns' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_conductance
    'abmho' :
        RPNUnitInfo( 'electrical_conductance', 'abmhos', '', [ 'absiemens' ], [ 'CGS' ],
                     '''
''' ),

    'conductance_quantum' :
        RPNUnitInfo( 'electrical_conductance', 'conductance_quanta', 'G0', [ ], [ 'SI' ],
                     '''
The conductance quantum appears when measuring the conductance of a quantum
point contact, and, more generally, is a key component of Landauer formula
which relates the electrical conductance of a quantum conductor to its quantum
properties.  It is twice the reciprocal of the von Klitzing constant (2/RK).

https://en.wikipedia.org/wiki/Conductance_quantum
''' ),

    'ampere^2*second^3/kilogram*meter^2':
        RPNUnitInfo( 'electrical_conductance', 'ampere^2*second^3/kilogram*meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'siemens' :
        RPNUnitInfo( 'electrical_conductance', 'siemens', 'S', [ 'mho', 'mhos' ], [ 'SI' ],
                     '''
''' ),

    'statmho' :
        RPNUnitInfo( 'electrical_conductance', 'statmhos', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'statsiemens' :
        RPNUnitInfo( 'electrical_conductance', 'statsiemens', 'statS', [ ], [ 'SI' ],
                     '''
''' ),

    # electric_potential
    'abvolt' :
        RPNUnitInfo( 'electric_potential', 'abvolts', 'abV', [ ], [ 'CGS' ],
                     '''
''' ),

    'decibel-volt' :
        RPNUnitInfo( 'electric_potential', 'decibel-volts', 'dBV', [ ], [ 'engineering' ],
                     '''
''' ),

    'kilogram*meter^2/ampere*second^3' :
        RPNUnitInfo( 'electric_potential', 'kilogram*meter^2/ampere*second^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    'volt' :
        RPNUnitInfo( 'electric_potential', 'volts', 'V', [ ], [ 'SI' ],
                     '''
''' ),

    'statvolt' :
        RPNUnitInfo( 'electric_potential', 'statvolts', 'statV', [ 'esu_potential' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_resistance
    '1/siemens' :
        RPNUnitInfo( 'electrical_resistance', '1/siemens', '', [ ], [ 'SI' ],
                     '''
''' ),

    'abohm' :
        RPNUnitInfo( 'electrical_resistance', 'abohms', 'o', [ ], [ 'CGS' ],
                     '''
''' ),

    'german_mile' :
        RPNUnitInfo( 'electrical_resistance', 'german_miles', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'jacobi' :
        RPNUnitInfo( 'electrical_resistance', 'jacobis', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^3' :
        RPNUnitInfo( 'electrical_resistance', 'kilogram*meter^2/ampere^2*second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'matthiessen' :
        RPNUnitInfo( 'electrical_resistance', 'matthiessens', '',
                     [ ], [ 'obsolete' ],   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),

    'ohm' :
        RPNUnitInfo( 'electrical_resistance', 'ohms', 'O', [ ], [ 'SI' ],
                     '''
''' ),

    'statohm' :
        RPNUnitInfo( 'electrical_resistance', 'statohms', 'statO', [ ], [ 'SI' ],
                     '''
''' ),

    'varley' :
        RPNUnitInfo( 'electrical_resistance', 'varleys', '',
                     [ ], [ 'obsolete' ],  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),

    # energy
    'btu' :
        RPNUnitInfo( 'energy', 'BTUs', '', [ 'btus' ], [ 'England', 'U.S.' ],
                     '''
''' ),

    'calorie' :
        RPNUnitInfo( 'energy', 'calories', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'electron-volt' :
        RPNUnitInfo( 'energy', 'electron-volts', 'eV', [ 'electronvolt', 'electronvolts' ], [ 'science' ],
                     '''
''' ),

    'erg' :
        RPNUnitInfo( 'energy', 'ergs', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'foe' :
        RPNUnitInfo( 'energy', 'foes', '', [ 'bethe', 'bethes' ], [ 'astrophysics' ],
                     '''
A foe is a unit of energy equal to 10^44 joules or 10^51 ergs, used to measure
the large amount of energy released by a supernova.  The word is an acronym
derived from the phrase [ten to the power of] fifty-one ergs.  It was coined
by Gerald Brown of Stony Brook University in his work with Hans Bethe, because
"it came up often enough in our work".
''' ),

    'gram_equivalent' :
        RPNUnitInfo( 'energy', 'grams_equivalent', 'gE',
                     [ 'gram-energy', 'grams-energy', 'gram-equivalent', 'grame-equivalent', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ],
                     '''
''' ),

    'hartree' :
        RPNUnitInfo( 'energy', 'hartrees', 'Eh', [ ], [ 'science' ],
                     '''
''' ),

    'joule' :
        RPNUnitInfo( 'energy', 'joules', 'J', [ ], [ 'SI' ],
                     '''
''' ),

    'kayser' :
        RPNUnitInfo( 'energy', 'kaysers', '', [ ], [ 'science', 'CGS' ],
                     '''
Kayser is a unit of energy used in atomic and molecular physics.  Since the
frequency of a photon is proportional to the energy it carries, the kayser is
also equivalent to an energy of 123.984 microelectronvolt.

Ref:  https://www.ibiblio.org/units/dictK.html
''' ),

    'kilogram*meter^2/second^2' :
        RPNUnitInfo( 'energy', 'kilogram*meter^2/second^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'pound_of_TNT' :
        RPNUnitInfo( 'energy', 'pounds_of_TNT', 'pTNT', [ ], [ 'informal' ],
                     '''
''' ),

    'quad' :
        RPNUnitInfo( 'energy', 'quads', '', [ ], [ 'U.S.' ],
                     '''
A quad is a unit of energy equal to 10^15 (a short-scale quadrillion) BTU, or
1.055e18 joules (1.055 exajoules or EJ) in SI units.  The unit is used by
the U.S. Department of Energy in discussing world and national energy budgets.
The global primary energy production in 2004 was 446 quad, equivalent to 471 EJ.

(https://en.wikipedia.org/wiki/Quad_%28unit%29)
''' ),

    'rydberg' :
        RPNUnitInfo( 'energy', 'rydbergs', 'Ry', [ ], [ 'science' ],
                     '''
''' ),

    'therm' :
        RPNUnitInfo( 'energy', 'therms', '', [ 'thm' ], [ 'England', 'U.S.' ],
                     '''
The therm (symbol thm) is a non-SI unit of heat energy equal to 100,000
British thermal units (BTU).  It is approximately the energy equivalent of
burning 100 cubic feet (often referred to as 1 CCF) of natural gas.

(https://en.wikipedia.org/wiki/Therm)
''' ),

    'toe' :
        RPNUnitInfo( 'energy', 'toes', '',
                     [ 'tonne_of_oil_equivalent', 'tonnes_of_oil_equivalent' ], [ 'international' ],
                     '''
"Toe" is a symbol for tonne of oil equivalent, a unit of energy used in the
international energy industry.  One toe represents the energy available from
burning approximately one tonne (metric ton) of crude oil; this is defined by
the International Energy Agency to be exactly 10^7 kilocalories, equivalent to
approximately 7.4 barrels of oil, 1270 cubic meters of natural gas, or 1.4
tonnes of coal. 1 toe is also equivalent to 41.868 gigajoules (GJ), 39.683
million Btu (MM Btu) or dekatherms, or 11.630 megawatt hours (MWh).

http://www.unc.edu/~rowlett/units/dictT.html
''' ),

    'ton_of_coal' :
        RPNUnitInfo( 'energy', 'tons_of_coal', '', [ ], [ 'informal' ],
                     '''
''' ),

    'ton_of_TNT' :
        RPNUnitInfo( 'energy', 'tons_of_TNT', 'tTNT', [ ], [ 'informal' ],
                     '''
''' ),

    # force
    'dyne' :
        RPNUnitInfo( 'force', 'dynes', 'dyn', [ ], [ 'CGS' ],
                     '''
''' ),

    'gram_force' :
        RPNUnitInfo( 'force', 'grams_force', 'gf',
                     [ 'gram-force', 'gramme-force', 'grams-force', 'grammes-force' ], [ 'CGS' ],
                     '''
''' ),

    'kilogram*meter/second^2' :
        RPNUnitInfo( 'force', 'kilogram*meter/second^2', '', [ ], [ 'SI' ],
                     '''
This is the definition of the SI derived unit Newton (N).
''' ),

    'newton' :
        RPNUnitInfo( 'force', 'newtons', 'N', [ ], [ 'SI' ],
                     '''
''' ),

    'pond' :
        RPNUnitInfo( 'force', 'ponds', '', [ ], [ 'metric' ],
                     '''
''' ),

    'pound-force' :
        RPNUnitInfo( 'force', 'pounds-force', '', [ ], [ 'FPS' ],
                     '''
''' ),

    'poundal' :
        RPNUnitInfo( 'force', 'poundals', 'pdl', [ ], [ 'England' ],
                     '''
''' ),

    'sthene' :
        RPNUnitInfo( 'force', 'sthenes', 'sn', [ 'funal' ], [ 'MTS' ],
                     '''
''' ),

    # frequency
    '1/second' :
        RPNUnitInfo( 'frequency', '1/second', '', [ ], [ 'traditional' ],
                     '''
''' ),

    'hertz' :
        RPNUnitInfo( 'frequency', 'hertz', 'Hz', [ 'cycle', 'cycles', 'every_second' ], [ 'SI' ],
                     '''
''' ),

    'becquerel' :
        RPNUnitInfo( 'frequency', 'becquerels', 'Bq', [ ], [ 'SI' ],
                     '''
''' ),

    'curie' :
        RPNUnitInfo( 'frequency', 'curies', 'Ci', [ ], [ 'obsolete' ],
                     '''
''' ),

    'rutherford' :
        RPNUnitInfo( 'frequency', 'rutherfords', 'rd', [ ], [ 'obsolete' ],
                     '''
''' ),

    # illuminance
    'candela*radian^2/meter^2' :
        RPNUnitInfo( 'illuminance', 'candela*radian^2/meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'flame' :
        RPNUnitInfo( 'illuminance', 'flames', '', [ ], [ ],
                     '''
''' ),

    'footcandle' :
        RPNUnitInfo( 'illuminance', 'footcandles', 'fc', [ ], [ 'FPS' ],
                     '''
''' ),

    'lux' :
        RPNUnitInfo( 'illuminance', 'lux', 'lx', [ ], [ 'SI' ],
                     '''
''' ),

    'lumen/meter^2' :
        RPNUnitInfo( 'illuminance', 'lumen/meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'nox' :
        RPNUnitInfo( 'illuminance', 'nox', 'nx', [ ], [ 'obsolete' ],
                     '''
''' ),

    'phot' :
        RPNUnitInfo( 'illuminance', 'phots', 'ph', [ ], [ 'CGS' ],
                     '''
''' ),

    # inductance
    'abhenry' :
        RPNUnitInfo( 'inductance', 'abhenries', 'abH', [ ], [ 'CGS' ],
                     '''
''' ),

    'henry' :
        RPNUnitInfo( 'inductance', 'henries', 'H', [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^2' :
        RPNUnitInfo( 'inductance', 'kilogram*meter^2/ampere^2*second^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'stathenry' :
        RPNUnitInfo( 'inductance', 'stathenries', 'statH', [ ], [ 'CGS' ],
                     '''
''' ),

    # information_entropy
    'bit' :
        RPNUnitInfo( 'information_entropy', 'bits', 'b',
                     [ 'shannon', 'shannons' ], [ 'computing' ],
                     '''
A 'binary digit', which can store two values.
''' ),

    'byte' :
        RPNUnitInfo( 'information_entropy', 'bytes', 'B',
                     [ 'octet', 'octets' ], [ 'computing' ],
                     '''
The traditional unit of computer storage, whose value has varied over the years
and on different platforms, but is now commonly defined to be 8 bits in size.
''' ),

    'btupf' :
        RPNUnitInfo( 'information_entropy', 'btupf', '', [ ], [ 'England' ],
                     '''
''' ),

    'clausius' :
        RPNUnitInfo( 'information_entropy', 'clausius', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'dword' :
        RPNUnitInfo( 'information_entropy', 'dwords', '',
                     [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ],
                     '''
A 'double-word' consisting of 2 16-bits words, or 32 bits total.
''' ),

    'hartley' :
        RPNUnitInfo( 'information_entropy', 'hartleys', 'Hart',
                     [ 'dit', 'dits', 'ban', 'bans' ], [ 'IEC' ],
                     '''
The hartley (symbol Hart), also called a ban, or a dit (short for decimal
digit), is a logarithmic unit which measures information or entropy, based on
base 10 logarithms and powers of 10, rather than the powers of 2 and base 2
logarithms which define the bit, or shannon.  One ban or hartley is the
information content of an event if the probability of that event occurring is
1/10.  It is therefore equal to the information contained in one decimal digit
(or dit), assuming a priori equiprobability of each possible value.

Ref:  https://en.wikipedia.org/wiki/Hartley_(unit)
''' ),

    'joule/kelvin' :
        RPNUnitInfo( 'information_entropy', 'joule/kelvin', '', [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/kelvin*second^2' :
        RPNUnitInfo( 'information_entropy', 'kilogram*meter^2/kelvin*second^2', '', [ ], [ 'physics' ],
                     '''
This is the unit of the Boltzmann constant.
''' ),

    'library_of_congress' :
        RPNUnitInfo( 'information_entropy', 'x_library_of_congress', 'LoC',
                     [ 'congress', 'congresses', 'loc' ], [ 'computing' ],
                     '''
An informal unit of information measurement based on the contents of the U.S.
Library of Congress, estimated to be the equivalent of 10 terabytes in size.
''' ),

    'nibble' :
        RPNUnitInfo( 'information_entropy', 'nibbles', '', [ 'nybble', 'nybbles' ], [ 'computing' ],
                     '''
A nybble is a half-byte, or 4 bits.  A nybble can be represented by a single
hexadecimal digit.
''' ),

    'nat' :
        RPNUnitInfo( 'information_entropy', 'nats', '',
                     [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ],
                     '''
''' ),

    'nyp' :
        RPNUnitInfo( 'information_entropy', 'nyps', '', [ ], [ 'computing' ],   # suggested by Donald Knuth
                     '''
A nyp is a term suggested by Knuth to represent two bits.  It is not a
commonly used term.
''' ),

    'oword' :
        RPNUnitInfo( 'information_entropy', 'owords', '',
                     [ 'octaword', 'octawords', 'octoword', 'octowords' ], [ 'computing' ],
                     '''
An 'octo-word' consisting of 8 16-bit words or 128 bits total.
''' ),

    'qword' :
        RPNUnitInfo( 'information_entropy', 'qwords', '',
                     [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ],
                     '''
A 'quad-word' consisting of 4 16-bit words, or 64 bits total.
''' ),

    'trit' :
        RPNUnitInfo( 'information_entropy', 'trits', '', [ ], [ 'computing' ],
                     '''
A trit is a 'ternary digit', by extension from the term 'bit' for 'binary
digit'.  In 1958 the Setun balanced ternary computer was developed at Moscow
State University, which used trits and 6-trit trytes.
''' ),

    'tryte' :
        RPNUnitInfo( 'information_entropy', 'trytes', '', [ ], [ 'computing' ],
                     '''
A tryte consists of 6 trits (i.e., 'ternary digits'), and is named by extension
from the term 'byte'.  In 1958 the Setun balanced ternary computer was
developed at Moscow State University, which used trits and 6-trit trytes.
''' ),

    'word' :
        RPNUnitInfo( 'information_entropy', 'words', '',
                     [ 'short_integer', 'short_integers', 'short_int', 'short_ints', 'wyde' ], [ 'computing' ],
                     '''
A word is traditionally two bytes, or 16 bits.  The term 'wyde' was suggested
by Knuth.
''' ),

    # jerk
    'meter/second^3' :
        RPNUnitInfo( 'jerk', 'meter/second^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    'stapp' :
        RPNUnitInfo( 'jerk', 'stapps', '', [ ], [ 'SI' ],
                     '''
The stapp a unit used to express the effects of acceleration or deceleration on
the human body.  One stapp represents an acceleration of 1 g for a period of 1
second, or 9.80665 meters per second per second for 1 second.  The unit is
named for the U.S. Air Force physician John P. Stapp (1910-1999), a pioneer in
research on the human effects of acceleration during the 1940s and 1950s.

http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    # jounce
    'meter/second^4' :
        RPNUnitInfo( 'jounce', 'meter/second^4', '', [ ], [ 'SI' ],
                     '''
''' ),

    # length
    'aln' :
        RPNUnitInfo( 'length', 'alns', '', [ 'alen', 'alens' ], [ 'obsolete' ],
                     '''
''' ),

    'angstrom' :
        RPNUnitInfo( 'length', 'angstroms', '', [ 'angstroem', 'angstroems' ], [ 'science' ],
                     '''
''' ),

    'arpent' :
        RPNUnitInfo( 'length', 'arpents', '', [ ], [ 'obsolete', 'France' ],
                     '''
''' ),

    'arshin' :
        RPNUnitInfo( 'length', 'arshins', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'astronomical_unit' :
        RPNUnitInfo( 'length', 'astronomical_units', 'au', [ ], [ 'science' ],
                     '''
''' ),

    'barleycorn' :
        RPNUnitInfo( 'length', 'barleycorns', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'bolt' :
        RPNUnitInfo( 'length', 'bolts', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'caliber' :
        RPNUnitInfo( 'length', 'caliber', '', [ 'calibre' ], [ 'U.S.' ],
                     '''
''' ),

    'chain' :
        RPNUnitInfo( 'length', 'chains', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'cicero' :
        RPNUnitInfo( 'length', 'ciceros', '', [ ], [ 'typography', 'obsolete' ],
                     '''
''' ),

    'cubit' :
        RPNUnitInfo( 'length', 'cubits', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'diuym' :
        RPNUnitInfo( 'length', 'diuyms', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ell' :
        RPNUnitInfo( 'length', 'ells', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'famn' :
        RPNUnitInfo( 'length', 'famns', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'farshimmelt_potrzebie' :
        RPNUnitInfo( 'length', 'farshimmelt_potrzebies', 'fpz',
                     [ 'far-potrzebie', 'far-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fathom' :
        RPNUnitInfo( 'length', 'fathoms', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'finger' :
        RPNUnitInfo( 'length', 'fingers', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'fingerbreadth' :
        RPNUnitInfo( 'length', 'fingerbreadths', '', [ 'fingersbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'foot' :
        RPNUnitInfo( 'length', 'feet', 'ft', [ ], [ 'traditional', 'FPS' ],
                     '''
''' ),

    'french' :
        RPNUnitInfo( 'length', 'french', '',
                     [ 'french_gauge', 'french_scale', 'charrier' ], [ 'France' ],
                     '''
The French scale or French gauge system is commonly used to measure the size of
a catheter.  It is most often abbreviated as Fr, but can often be seen
abbreviated as Fg, Ga, FR or F.  It may also be abbreviated as CH or Ch (for
Charriere, its inventor).

https://en.wikipedia.org/wiki/French_catheter_scale
''' ),

    'furlong' :
        RPNUnitInfo( 'length', 'furlongs', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'furshlugginer_potrzebie' :
        RPNUnitInfo( 'length', 'furshlugginer_potrzebies', 'Fpz',
                     [ 'fur-potrzebie', 'fur-potrzebies', 'Fur-potrzebie', 'Fur-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fut' :
        RPNUnitInfo( 'length', 'futs', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'greek_cubit' :
        RPNUnitInfo( 'length', 'greek_cubits', '', [ ], [ 'obsolete', 'Greece' ],
                     '''
''' ),

    'gutenberg' :
        RPNUnitInfo( 'length', 'gutenbergs', '', [ ], [ 'typography' ],
                     '''
''' ),

    'hand' :
        RPNUnitInfo( 'length', 'hands', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'handbreadth' :
        RPNUnitInfo( 'length', 'handbreadths', '', [ 'handsbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'hubble' :
        RPNUnitInfo( 'length', 'hubbles', '', [ ], [ 'astronomy' ],
                     '''
''' ),

    'inch' :
        RPNUnitInfo( 'length', 'inches', 'in', [ ], [ 'U.S.' ],
                     '''
''' ),

    'ken' :
        RPNUnitInfo( 'length', 'kens', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'kosaya_sazhen' :
        RPNUnitInfo( 'length', 'kosaya_sazhens', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'kyu' :
        RPNUnitInfo( 'length', 'kyus', '', [ 'Q' ], [ 'typography', 'computing' ],
                     '''
''' ),

    'league' :
        RPNUnitInfo( 'length', 'leagues', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'light-second' :
        RPNUnitInfo( 'length', 'light-seconds', '', [ ], [ 'science' ],
                     '''
''' ),

    'light-year' :
        RPNUnitInfo( 'length', 'light-years', 'ly', [ 'a1' ], [ 'science' ],
                     '''
''' ),

    'liniya' :
        RPNUnitInfo( 'length', 'liniya', '', [ ], [ 'informal' ],
                     '''
''' ),

    'link' :
        RPNUnitInfo( 'length', 'links', '', [ ], [ 'informal' ],
                     '''
''' ),

    'long_cubit' :
        RPNUnitInfo( 'length', 'long_cubits', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'long_reed' :
        RPNUnitInfo( 'length', 'long_reeds', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'marathon' :
        RPNUnitInfo( 'length', 'marathons', '', [ ], [ 'informal' ],
                     '''
''' ),

    'mezhevaya_versta' :
        RPNUnitInfo( 'length', 'mezhevaya_verstas', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'meter' :
        RPNUnitInfo( 'length', 'meters', 'm', [ 'metre', 'metres' ], [ 'SI' ],
                     '''
''' ),

    'metric_foot' :
        RPNUnitInfo( 'length', 'metric_feet', '', [ ], [ 'UK', 'unofficial' ],
                     '''
''' ),

    'micron' :
        RPNUnitInfo( 'length', 'microns', '', [ ], [ 'science' ],
                     '''
''' ),

    'mil' :
        RPNUnitInfo( 'length', 'mils', '', [ 'thou' ], [ 'U.S.' ],
                     '''
''' ),

    'mile' :
        RPNUnitInfo( 'length', 'miles', 'mi', [ ], [ 'U.S.' ],
                     '''
''' ),

    'nail' :
        RPNUnitInfo( 'length', 'nails', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'nautical_mile' :
        RPNUnitInfo( 'length', 'nautical_miles', '', [ ], [ 'nautical' ],
                     '''
''' ),

    'parsec' :
        RPNUnitInfo( 'length', 'parsecs', 'pc', [ ], [ 'science' ],
                     '''
''' ),

    'pica' :
        RPNUnitInfo( 'length', 'picas', '', [ ], [ 'typography' ],
                     '''
''' ),

    'point' :
        RPNUnitInfo( 'length', 'points', '', [ ], [ 'typography' ],
                     '''
''' ),

    'poppyseed' :
        RPNUnitInfo( 'length', 'poppyseeds', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'pyad' :
        RPNUnitInfo( 'length', 'pyads', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'rack_unit' :
        RPNUnitInfo( 'length', 'rack_units', '', [ ], [ 'computers' ],
                     '''
A rack unit (abbreviated U or RU) is a unit of measure defined as 44.50
millimeters (1.752 in).  It is most frequently used as a measurement of the
overall height of 19-inch and 23-inch rack frames, as well as the height of
equipment that mounts in these frames, whereby the height of the frame or
equipment is expressed as multiples of rack units.

https://en.wikipedia.org/wiki/Rack_unit
''' ),

    'reed' :
        RPNUnitInfo( 'length', 'reeds', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'rod' :
        RPNUnitInfo( 'length', 'rods', '', [ 'pole', 'poles', 'perch', 'perches' ], [ 'U.S.' ],
                     '''
''' ),

    'rope' :
        RPNUnitInfo( 'length', 'ropes', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'potrzebie' :
        RPNUnitInfo( 'length', 'potrzebies', 'pz', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
In issue 33, "Mad" magazine published a partial table of the "Potrzebie System
of Weights and Measures", developed by 19-year-old Donald E. Knuth, later a
famed computer scientist.  According to Knuth, the basis of this new
revolutionary system is the potrzebie, which equals the thickness of Mad issue
26, or 2.2633484517438173216473 mm, although a digit was mistakenly dropped and
the thickness appeared as 2.263348517438173216473 mm in the MAD article.  A
standardization in terms of the wavelength of the red line of the emission
spectrum of cadmium is also given, which if the 1927 definition of the Angstrom
is taken for the value of that wavelength, would equal 2.263347539605392 mm.

The Potrzebie units are included in rpnChilada as a tribute to Knuth, and
because it is a very silly system that amuses the author.

Ref:  https://en.wikipedia.org/wiki/Potrzebie
Ref:  https://blog.codinghorror.com/the-enduring-art-of-computer-programming/
''' ),

    'sazhen' :
        RPNUnitInfo( 'length', 'sazhens', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'siriometer' :
        RPNUnitInfo( 'length', 'siriometers', '', [ ], [ 'science' ],  # proposed in 1911 by Cark V. L. Charlier
                     '''
''' ),

    'skein' :
        RPNUnitInfo( 'length', 'skeins', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'smoot' :
        RPNUnitInfo( 'length', 'smoots', '', [ ], [ 'humorous' ],
                     '''
The Smoot is a unit of length, defined as the height in 1958 of Oliver R.
Smoot, who later became the Chairman of the American National Standards
Institute (ANSI), and then the president of the International Organization for
Standardization (ISO). The unit is used to measure the length of the Harvard
Bridge.  Canonically, and originally, in 1958 when Smoot was a Lambda Chi Alpha
pledge at MIT (class of 1962), the bridge was measured to be 364.4 Smoots, plus
or minus one ear, using Mr. Smoot himself as a ruler.  At the time, Smoot was 5
feet, 7 inches, or 170 cm, tall.

https://en.wikipedia.org/wiki/List_of_humorous_units_of_measurement#Smoot
''' ),

    'span' :
        RPNUnitInfo( 'length', 'spans', '', [ 'breadth' ], [ 'imperial' ],
                     '''
''' ),

    'stadium' :
        RPNUnitInfo( 'length', 'stadia', '', [ ], [ 'Rome' ],
                     '''
''' ),

    'survey_foot' :
        RPNUnitInfo( 'length', 'survey_feet', '', [ ], [ 'U.S.' ],
                     '''
In 1893 the United States fixed the yard at 3600/3937 meters, making the yard
0.9144018 meters and 1896 the British authorities fixed the yard as being
0.9143993 meters.  At the time the discrepancy of about two parts per million
was considered to be insignificant.  In 1960, the United Kingdom, United
States, Australia, Canada and South Africa standardised their units of length
by defining the "international yard" as being 0.9144 meters exactly.  This
change affected land surveyors in the United States and led to the old units
being renamed "survey feet", "survey miles" etc.

https://en.wikipedia.org/wiki/Imperial_and_US_customary_measurement_systems#Units_of_length
''' ),

    'twip' :
        RPNUnitInfo( 'length', 'twips', 'twp', [ ], [ 'computing' ],
                     '''
''' ),

    'vershok' :
        RPNUnitInfo( 'length', 'vershoks', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'versta' :
        RPNUnitInfo( 'length', 'verstas', '', [ 'verst', 'versts' ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'yard' :
        RPNUnitInfo( 'length', 'yards', 'yd', [ ], [ 'U.S.' ],
                     '''
''' ),

    # luminance
    'apostilb' :
        RPNUnitInfo( 'luminance', 'apostilbs', 'asb', [ 'blondel', 'blondels' ], [ 'CGS' ],
                     '''
''' ),

    'bril' :
        RPNUnitInfo( 'luminance', 'brils', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'candela/meter^2' :
        RPNUnitInfo( 'luminance', 'candela/meter^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'footlambert' :
        RPNUnitInfo( 'luminance', 'footlamberts', '', [ ], [ 'U.S.', 'obsolete' ],
                     '''
''' ),

    'lambert' :
        RPNUnitInfo( 'luminance', 'lamberts', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'nit' :
        RPNUnitInfo( 'luminance', 'nits', 'nt',
                     [ 'meterlambert', 'meter*lambert', 'meterlamberts', 'meter*lamberts' ], [ 'obsolete' ],
                     '''
''' ),

    'skot' :
        RPNUnitInfo( 'luminance', 'skots', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'stilb' :
        RPNUnitInfo( 'luminance', 'stilbs', 'sb', [ ], [ 'CGS' ],
                     '''
''' ),

    # luminous_flux
    'lumen' :
        RPNUnitInfo( 'luminous_flux', 'lumens', 'lm', [ ], [ 'SI' ],
                     '''
''' ),

    'candela*radian^2' :
        RPNUnitInfo( 'luminous_flux', 'candela*radian^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    # luminous_intensity
    'candela' :
        RPNUnitInfo( 'luminous_intensity', 'candelas', 'cd',
                     [ 'candle', 'candles', 'bougie', 'bougies' ], [ 'SI' ],
                     '''
''' ),

    'hefnerkerze' :
        RPNUnitInfo( 'luminous_intensity', 'hefnerkerze', 'HK', [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    # magnetic_field_strength
    'ampere/meter' :
        RPNUnitInfo( 'magnetic_field_strength', 'ampere/meter', '', [ ], [ 'SI' ],
                     '''
''' ),

    'oersted' :
        RPNUnitInfo( 'magnetic_field_strength', 'oersted', 'Oe', [ ], [ 'CGS' ],
                     '''
''' ),

    # magnetic_flux
    'kilogram*meter^2/ampere*second^2' :
        RPNUnitInfo( 'magnetic_flux', 'kilogram*meter^2/ampere*second^2', '', [ ], [ 'SI' ],
                     '''
''' ),


    'maxwell' :
        RPNUnitInfo( 'magnetic_flux', 'maxwells', 'Mx', [ 'line', 'lines' ], [ 'CGS' ],
                     '''
''' ),

    'unit_pole' :
        RPNUnitInfo( 'magnetic_flux', 'unit_poles', '', [ 'unitpole', 'unitpoles' ], [ 'CGS' ],
                     '''
''' ),

    'weber' :
        RPNUnitInfo( 'magnetic_flux', 'webers', 'Wb', [ 'promaxwell', 'promaxwells' ], [ 'SI' ],
                     '''
''' ),

    # magnetic_flux_density
    'gauss' :
        RPNUnitInfo( 'magnetic_flux_density', 'gauss', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'kilogram/ampere*second^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'tesla' :
        RPNUnitInfo( 'magnetic_flux_density', 'teslas', 'T', [ ], [ 'SI' ],
                     '''
''' ),

    # mass
    'berkovets' :
        RPNUnitInfo( 'mass', 'berkovets', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'blintz' :
        RPNUnitInfo( 'mass', 'blintzes', 'bl', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'carat' :
        RPNUnitInfo( 'mass', 'carats', 'ct', [ ], [ 'U.S.' ],
                     '''
''' ),

    'chandrasekhar_limit' :
        RPNUnitInfo( 'mass', 'x chandrasekhar_limit', '',
                     [ 'chandrasekhar', 'chandrasekhars' ], [ 'science' ],
                     '''
''' ),

    'dalton' :
        RPNUnitInfo( 'mass', 'daltons', '', [ 'amu', 'atomic_mass_unit' ], [ 'science' ],
                     '''
''' ),

    'dolya' :
        RPNUnitInfo( 'mass', 'dolyas', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'doppelzentner' :
        RPNUnitInfo( 'mass', 'doppelzentners', '', [ ], [ 'Germany' ],
                     '''
''' ),

    'farshimmelt_blintz' :
        RPNUnitInfo( 'mass', 'farshimmelt_blintzes', 'fb',
                     [ 'far-blintz', 'far-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'funt' :
        RPNUnitInfo( 'mass', 'funts', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'furshlugginer_blintz' :
        RPNUnitInfo( 'mass', 'furshlugginer_blintzes', 'Fb',
                     [ 'fur-blintz', 'fur-blintzes', 'Fur-blintz', 'Fur-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'grain' :
        RPNUnitInfo( 'mass', 'grains', 'gr', [ ], [ 'traditional' ],
                     '''
''' ),

    'gram' :
        RPNUnitInfo( 'mass', 'grams', 'g', [ 'gramme', 'grammes' ], [ 'SI' ],
                     '''
''' ),

# hyl, metric_slug, technical_mass_unit, technische_masseseinheit, 9.80665 kg

    'joule*second^2/meter^2' :
        RPNUnitInfo( 'mass', 'joule*second^2/meter^2', '', [ ], [ 'SI' ],
                     '''
This conversion is required to do mass-energy equivalence calculations.
''' ),

    'kip' :
        RPNUnitInfo( 'mass', 'kips', '', [ 'kilopound', 'kilopounds' ], [ 'U.S.' ],
                     '''
''' ),

    'lot' :
        RPNUnitInfo( 'mass', 'lots', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ounce' :
        RPNUnitInfo( 'mass', 'ounces', 'oz', [ ], [ 'traditional' ],
                     '''
''' ),

    'pennyweight' :
        RPNUnitInfo( 'mass', 'pennyweights', 'dwt', [ 'pwt' ], [ 'traditional', 'England' ],
                     '''
''' ),

    'pfund' :
        RPNUnitInfo( 'mass', 'pfunds', '', [ ], [ 'Germany' ],
                     '''
''' ),

    'pood' :
        RPNUnitInfo( 'mass', 'poods', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'pound' :
        RPNUnitInfo( 'mass', 'pounds', 'lb', [ ], [ 'U.S.', 'traditional', 'FPS' ],
                     '''
''' ),

    'quintal' :
        RPNUnitInfo( 'mass', 'quintals', 'q', [ 'cantar', 'cantars' ], [ ],
                     '''
''' ),

    'sheet' :
        RPNUnitInfo( 'mass', 'sheets', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'slinch' :
        RPNUnitInfo( 'mass', 'slinches', '', [ 'mug', 'mugs', 'snail', 'snails' ], [ 'NASA' ],
                     '''
''' ),

    'slug' :
        RPNUnitInfo( 'mass', 'slugs', '',
                     [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ],
                     '''
''' ),

    'stone' :
        RPNUnitInfo( 'mass', 'stones', '', [ ], [ 'traditional', 'England' ],
                     '''
''' ),

    'stone_us' :
        RPNUnitInfo( 'mass', 'stones_us', '', [ 'us_stone', 'us_stones' ], [ 'U.S.' ],
                     '''
''' ),

    'ton' :
        RPNUnitInfo( 'mass', 'tons', '', [ ], [ 'traditional', 'U.S.' ],
                     '''
''' ),

    'tonne' :
        RPNUnitInfo( 'mass', 'tonnes', '', [ 'metric_ton', 'metric_tons' ], [ 'MTS' ],
                     '''
''' ),

    'troy_ounce' :
        RPNUnitInfo( 'mass', 'troy_ounces', 'toz', [ ], [ 'traditional' ],
                     '''
''' ),

    'troy_pound' :
        RPNUnitInfo( 'mass', 'troy_pounds', '', [ ], [ 'traditional'  ],
                     '''
''' ),

    'wey' :
        RPNUnitInfo( 'mass', 'weys', '', [ ], [ 'obsolete', 'England' ],
                     '''
''' ),

    'zentner' :
        RPNUnitInfo( 'mass', 'zentners', '', [ ], [ 'Germany' ],
                     '''
''' ),

    'zolotnik' :
        RPNUnitInfo( 'mass', 'zolotniks', '', [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    # power
    'decibel-milliwatt' :
        RPNUnitInfo( 'power', 'decibel-milliwatts', 'dBm', [ 'dBmW', ], [ 'engineering' ],
                     '''
''' ),

    'decibel-watt' :
        RPNUnitInfo( 'power', 'decibel-watts', 'dBW', [ ], [ 'engineering' ],
                     '''
''' ),

    'horsepower' :
        RPNUnitInfo( 'power', 'horsepower', 'hp', [ ], [ 'U.S.' ],
                     '''
''' ),

    'lusec' :
        RPNUnitInfo( 'power', 'lusecs', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'kilogram*meter^2/second^3' :
        RPNUnitInfo( 'power', 'kilogram*meter^2/second^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    'pferdestarke' :
        RPNUnitInfo( 'power', 'pferdestarke', 'PS', [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    'poncelet' :
        RPNUnitInfo( 'power', 'poncelets', '', [ ], [ 'obsolete' ],
                     '''
''' ),

    'watt' :
        RPNUnitInfo( 'power', 'watts', 'W', [ ], [ 'SI' ],
                     '''
''' ),

    # pressure
    'atmosphere' :
        RPNUnitInfo( 'pressure', 'atmospheres', 'atm', [ ], [ 'natural' ],
                     '''
''' ),

    'bar' :
        RPNUnitInfo( 'pressure', 'bars', '', [ ], [ ],
                     '''
''' ),

    'barye' :
        RPNUnitInfo( 'pressure', 'baryes', 'Ba', [ 'barad', 'barads' ], [ 'CGS' ],
                     '''
''' ),

    'mmHg' :
        RPNUnitInfo( 'pressure', 'mmHg', '', [ ], [ 'metric' ],
                     '''
''' ),

    'kilogram/meter*second^2' :
        RPNUnitInfo( 'pressure', 'kilogram/meter*second^2', '', [ ], [ 'SI' ],
                     '''
''' ),

    'pascal' :
        RPNUnitInfo( 'pressure', 'pascals', 'Pa', [ ], [ 'SI' ],
                     '''
''' ),

    'pieze' :
        RPNUnitInfo( 'pressure', 'piezes', '', [ ], [ 'MTS' ],
                     '''
''' ),

    'psi' :
        RPNUnitInfo( 'pressure', 'pound/inch^2', '', [ ], [ 'FPS' ],
                     '''
''' ),

# technical_atmosphere (at) 98.0665 kPa

    'torr' :
        RPNUnitInfo( 'pressure', 'torr', '', [ ], [ ],
                     '''
''' ),

    # radiation_dose
    'banana_equivalent_dose' :
        RPNUnitInfo( 'radiation_dose', 'banana_equivalent_doses', '',
                     [ 'banana', 'bananas' ], [ 'natural', 'informal' ],
                     '''
''' ),

    'gray' :
        RPNUnitInfo( 'radiation_dose', 'grays', '', [ ], [ 'SI' ],   # or should 'Gy' be giga-years?
                     '''
''' ),

    'meter^2/second^2' :
        RPNUnitInfo( 'radiation_dose', 'meter^2/second^2', '',
                     [ ], [ 'SI' ],   # This doesn't seem to make sense, but joule/kilogram reduces to this!
                     '''
''' ),

    'rem' :
        RPNUnitInfo( 'radiation_dose', 'rems', '', [ 'roentgen_equivalent_man' ], [ 'CGS' ],
                     '''
''' ),

    'sievert' :
        RPNUnitInfo( 'radiation_dose', 'sieverts', 'Sv', [ ], [ 'SI' ],
                     '''
''' ),

    # radiation_exposure
    'coulomb/kilogram' :
        RPNUnitInfo( 'radiation_exposure', 'coulomb/kilogram', '', [ ], [ 'SI' ],
                     '''
''' ),

    'rad' :
        RPNUnitInfo( 'radiation_exposure', 'rads', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'roentgen' :
        RPNUnitInfo( 'radiation_exposure', 'roentgens', 'R',
                     [ 'parker', 'parkers', 'rep', 'reps' ], [ 'NIST' ],
                     '''
''' ),

    # radiosity
    'kilogram/second^3' :
        RPNUnitInfo( 'radiosity', 'kilogram/second^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    # ratio

    # Bel
    # Neper
    # karat (1/24)

    # solid_angle
    'arcminute^2' :
        RPNUnitInfo( 'solid_angle', 'arcminute^2', '',
                     [ 'square_arcminute', 'square_arcminutes', 'solid_arcminute', 'solid_arcminutes', 'sq_arcminute', 'sq_arcminutes', 'sqarcmin', 'sqarcmins', 'spherical_minute', 'spherical_minutes' ], [ 'mathematics' ],
                     '''
''' ),

    'arcsecond^2' :
        RPNUnitInfo( 'solid_angle', 'arcsecond^2', '',
                     [ 'square_arcsecond', 'square_arcseconds', 'solid_arcsecond', 'solid_arcseconds', 'sq_arcsecond', 'sq_arcseconds', 'sqarcsec', 'sqarcsecs', 'spherical_second', 'spherical_seconds' ], [ 'mathematics' ],
                     '''
''' ),

    'degree^2' :
        RPNUnitInfo( 'solid_angle', 'degree^2', '',
                     [ 'square_degree', 'square_degrees', 'sqdeg', 'solid_degree', 'solid_degrees', 'sq_degree', 'sq_degrees', 'sqdeg', 'sqdegs', 'spherical_degree', 'spherical_degrees' ], [ 'mathematics' ],
                     '''
''' ),

    'grad^2' :
        RPNUnitInfo( 'solid_angle', 'grad^2', '',
                     [ 'square_grad', 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'sq_gon', 'sq_gons', 'sqgon', 'sqgons', 'spherical_gon', 'spherical_gons', 'spherical_grad', 'spherical_grads' ], [ 'mathematics' ],
                     '''
''' ),

    'hemisphere' :
        RPNUnitInfo( 'solid_angle', 'hemispheres', '',
                     [ 'half_sphere', 'half_spheres', 'halfsphere', 'halfspheres' ], [ 'mathematics' ],
                     '''
''' ),

    'radian^2' :
        RPNUnitInfo( 'solid_angle', 'radian^2', '', [ ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    'octant^2' :
        RPNUnitInfo( 'solid_angle', 'octant^2', '',
                     [ 'octant_square', 'square_octants', 'sqoctant', 'sqoctants', 'solid_octant', 'solid_octants', 'sq_octant', 'sq_octants', 'spherical_octant', 'spherical_octants' ], [ 'mathematics' ],
                     '''
''' ),

    'quadrant^2' :
        RPNUnitInfo( 'solid_angle', 'quadrant^2', '',
                     [ 'square_quadrant', 'square_quadrants', 'sqquadrant', 'sqquadrants', 'solid_quadrant', 'solid_quadrants', 'sq_quadrant', 'sq_quadrants', 'spherical_quadrant', 'spherical_quadrants' ], [ 'mathematics' ],
                     '''
''' ),

    'quintant^2' :
        RPNUnitInfo( 'solid_angle', 'quintant^2', '',
                     [ 'square_quintant', 'square_quintants', 'sqquintant', 'sqquintants', 'solid_quintant', 'solid_quintants', 'sq_quintant', 'sq_quintants', 'spherical_quintant', 'spherical_quintants' ], [ 'mathematics' ],
                     '''
''' ),

    'sextant^2' :
        RPNUnitInfo( 'solid_angle', 'sextant^2', '',
                     [ 'square_sextant', 'square_sextants', 'sqsextant', 'sqsextants', 'solid_sextant', 'solid_sextants', 'sq_sextant', 'sq_sextants', 'spherical_sextant', 'spherical_sextants' ], [ 'mathematics' ],
                     '''
''' ),

    'sphere' :
        RPNUnitInfo( 'solid_angle', 'spheres', '', [ 'spat', 'spats' ], [ 'mathematics' ],
                     '''
''' ),

    'steradian' :
        RPNUnitInfo( 'solid_angle', 'steradians', 'sr',
                     [ 'square_radian', 'square_radians', 'sq_radian', 'sq_radians', 'sq_rad', 'sqrad', 'spherical_radian', 'spherical_radians' ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    # temperature
    'celsius' :
        RPNUnitInfo( 'temperature', 'degrees_celsius', 'Cel',
                     [ 'centigrade', 'degC', 'degreeC', 'degreesC', 'degree_centigrade', 'degrees_centigrade', 'degrees_C' ], [ 'SI' ],
                     '''
''' ),

    'degree_newton' :
        RPNUnitInfo( 'temperature', 'degrees_newton', '',
                     [ 'degN', 'degreeN', 'degreesN', 'degrees_N' ], [ 'obsolete' ],
                     '''
''' ),

    'delisle' :
        RPNUnitInfo( 'temperature', 'degrees_delisle', 'De',
                     [ 'degD', 'degreeD', 'degreesD', 'degree_delisle', 'degrees_D' ], [ 'obsolete' ],
                     '''
''' ),

    'fahrenheit' :
        RPNUnitInfo( 'temperature', 'degrees_fahrenheit', '',
                     [ 'fahr', 'degF', 'degreeF', 'degreesF', 'degree_fahrenheit', 'degrees_F' ], [ 'U.S.', 'traditional' ],
                     '''
''' ),

    'kelvin' :
        RPNUnitInfo( 'temperature', 'kelvins', 'K',
                     [ 'degK', 'degreeK', 'degreesK', 'degree_kelvin', 'degrees_kelvin', 'degrees_K' ], [ 'SI' ],
                     '''
The Kelvin scale is an absolute thermodynamic temperature scale using as its
null point absolute zero, the temperature at which all thermal motion ceases
in the classical description of thermodynamics. The kelvin (symbol: K) is the
base unit of temperature in the International System of Units (SI).

Ref:  https://en.wikipedia.org/wiki/Kelvin
''' ),

    'rankine' :
        RPNUnitInfo( 'temperature', 'degrees_rankine', 'R',
                     [ 'degR', 'degreeR', 'degreesR', 'degree_rankine', 'degrees_R' ], [ 'obsolete' ],
                     '''
The Rankine scale is an absolute scale of thermodynamic temperature named after
the Glasgow University engineer and physicist William John Macquorn Rankine,
who proposed it in 1859. (The Kelvin scale was first proposed in 1848.)  It may
be used in engineering systems where heat computations are done using degrees
Fahrenheit.

Ref:  https://en.wikipedia.org/wiki/Rankine_scale
''' ),

    'reaumur' :
        RPNUnitInfo( 'temperature', 'degrees_reaumur', 'Re',
                     [ 'degRe', 'degreeRe', 'degreesRe', 'degree_reaumur', 'degrees_Re' ], [ 'obsolete' ],
                     '''
''' ),

    'romer' :
        RPNUnitInfo( 'temperature', 'degrees_romer', 'Ro',
                     [ 'degRo', 'degreeRo', 'degreesRo', 'degree_romer', 'degrees_Ro' ], [ 'obsolete' ],
                     '''
''' ),

    # time
    'beat' :
        RPNUnitInfo( 'time', 'beats', '', [ ], [ ],
                     '''
''' ),

    'blink' :
        RPNUnitInfo( 'time', 'blinks', '', [ 'metric_second', 'metric_seconds' ], [ ],
                     '''
''' ),

    'century' :
        RPNUnitInfo( 'time', 'centuries', '', [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'clarke' :
        RPNUnitInfo( 'time', 'clarkes', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'cowznofski' :
        RPNUnitInfo( 'time', 'cowznofskis', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'day' :
        RPNUnitInfo( 'time', 'days', '', [ 'ephemeris_day' ], [ 'traditional' ],
                     '''
''' ),

    'decade' :
        RPNUnitInfo( 'time', 'decades', '', [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'eon' :
        RPNUnitInfo( 'time', 'eons', '', [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'fortnight' :
        RPNUnitInfo( 'time', 'fortnights', '', [ ], [ 'traditional' ],
                     '''
''' ),

    'gregorian_year' :
        RPNUnitInfo( 'time', 'gregorian_years', '', [ ], [ 'traditional' ],
                     '''
''' ),

    'hour' :
        RPNUnitInfo( 'time', 'hours', 'hr', [ ], [ 'traditional' ],
                     '''
An hour (abbreviated 'hr') is a unit of time conventionally reckoned as 1/24
of a day, or 60 minutes.

Ref:  https://en.wikipedia.org/wiki/Hour
''' ),

    'kovac' :
        RPNUnitInfo( 'time', 'kovacs', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'jiffy' :
        RPNUnitInfo( 'time', 'jiffies', '', [ ], [ 'computing' ],
                     '''
''' ),

    'lustrum' :
        RPNUnitInfo( 'time', 'lustra', '', [ ], [ 'obsolete', 'years' ],
                     '''
''' ),

    'martin' :
        RPNUnitInfo( 'time', 'martins', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'microcentury' :
        RPNUnitInfo( 'time', 'microcenturies', '', [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'microfortnight' :
        RPNUnitInfo( 'time', 'microfortnights', '', [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'mingo' :
        RPNUnitInfo( 'time', 'mingoes', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'minute' :
        RPNUnitInfo( 'time', 'minutes', '', [ ], [ 'traditional' ],  # 'min' is already an operator
                     '''
The minute is a unit of time or angle (the minute angle unit in rpn is the
'arcminute').  As a unit of time, the minute is most of times equal to 1/60 of
an hour, or 60 seconds.

https://en.wikipedia.org/wiki/Minute
''' ),

    'month' :
        RPNUnitInfo( 'time', 'months', 'mo', [ ], [ 'traditional' ],
                     '''
''' ),

    'nanocentury' :
        RPNUnitInfo( 'time', 'nanocenturies', '', [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'second' :
        RPNUnitInfo( 'time', 'seconds', 's', [ ], [ 'SI', 'traditional', 'FPS' ],   # 'sec' is already an operator
                     '''
The second is the base unit of time in the International System of Units (SI),
commonly understood and historically defined as 1/86400 of a day - this factor
derived from the division of the day first into 24 hours, then to 60 minutes
and finally to 60 seconds each.

Although the historical definition of the unit was based on this division of
the Earth's rotation cycle, the formal definition in the International System
of Units (SI) is a much steadier timekeeper: 1 second is defined to be exactly
"the duration of 9,192,631,770 periods of the radiation corresponding to the
transition between the two hyperfine levels of the ground state of the
cesium-133 atom".

Ref:  https://en.wikipedia.org/wiki/Second
''' ),

    'shake' :
        RPNUnitInfo( 'time', 'shakes', '', [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_day' :
        RPNUnitInfo( 'time', 'sidereal_days', '', [ 'earth_day', 'earth_days' ], [ 'science' ],
                     '''
''' ),

    'sidereal_hour' :
        RPNUnitInfo( 'time', 'sidereal_hours', '', [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_minute' :
        RPNUnitInfo( 'time', 'sidereal_minutes', '', [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_second' :
        RPNUnitInfo( 'time', 'sidereal_seconds', '', [ ], [ 'science' ],
                     '''
''' ),

    'svedberg' :
        RPNUnitInfo( 'time', 'svedbergs', '', [ ], [ ],
                     '''
''' ),

    'tropical_month' :
        RPNUnitInfo( 'time', 'tropical_months', '', [ ], [ 'science' ],
                     '''
''' ),

    'week' :
        RPNUnitInfo( 'time', 'weeks', 'wk', [ 'sennight', 'sennights' ], [ 'traditional' ],
                     '''
''' ),

    'wolverton' :
        RPNUnitInfo( 'time', 'wolvertons', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'wood' :
        RPNUnitInfo( 'time', 'woods', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'year' :
        RPNUnitInfo( 'time', 'years', '',
                     [ 'annum', 'annums', 'julian_year', 'julian_years', 'twelvemonth', 'twelvemonths' ], [ 'traditional', 'years' ],
                     '''
''' ),

    # velocity
    'bubnoff_unit' :
        RPNUnitInfo( 'velocity', 'bubnoff_units', '', [ 'bubnoff', 'bubnoffs' ], [ 'science' ],
                     '''
The Bubnoff unit is employed in geology to measure rates of lowering of earth
surfaces due to erosion and is named after the Russian (German-Baltic)
geologist Serge von Bubnoff (1888-1957).  An erosion speed of 1 B also means
that 1 cubic meter of earth is being removed from an area of 1 square km in 1
year.

https://en.wikipedia.org/wiki/Bubnoff_unit
''' ),

    'kine' :
        RPNUnitInfo( 'velocity', 'kine', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'meter/second' :
        RPNUnitInfo( 'velocity', 'meter/second', 'mps', [ 'benz' ], [ 'SI' ],
                     '''
''' ),

    'knot' :
        RPNUnitInfo( 'velocity', 'knots', 'kt', [ ], [ 'nautical' ],
                     '''
''' ),

    'mach' :
        RPNUnitInfo( 'velocity', 'mach', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'speed_of_sound' :
        RPNUnitInfo( 'velocity', 'x speed_of_sound', '', [ ], [ 'natural' ],
                     '''
''' ),

    # volume
    'balthazar' :
        RPNUnitInfo( 'volume', 'balthazars', '', [ 'belshazzar', 'belshazzars' ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'beer_barrel' :
        RPNUnitInfo( 'volume', 'beer_barrel', '', [ ], [ 'U.S.', 'beer' ],
                     '''
https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measurements
''' ),

    'beer_keg' :
        RPNUnitInfo( 'volume', 'beer_kegs', '', [ ], [ 'U.S.', 'beer' ],
                     '''
https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measurements
''' ),

    'bucket' :
        RPNUnitInfo( 'volume', 'buckets', '', [ ], [ 'U.S.' ],
                     '''
''' ),

    'bushel' :
        RPNUnitInfo( 'volume', 'bushels', 'bu', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/United_States_customary_units
''' ),

    'butt' :
        RPNUnitInfo( 'volume', 'butts', '', [ 'pipe', 'pipes' ], [ 'U.S.', 'wine' ],
                     '''
''' ),

    'chopine' :
        RPNUnitInfo( 'volume', 'chopines', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'clavelin' :
        RPNUnitInfo( 'volume', 'clavelins', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'coffeespoon' :
        RPNUnitInfo( 'volume', 'coffeespoons', '', [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'cord' :
        RPNUnitInfo( 'volume', 'cords', '', [ ], [ 'traditional' ],
                     '''
''' ),

    'cup' :
        RPNUnitInfo( 'volume', 'cups', '', [ ], [ 'traditional', 'cooking' ],
                     '''
The cup is a cooking measure of volume, commonly associated with cooking and
serving sizes.  It is traditionally equal to half a liquid pint in U.S.
customary units but is now separately defined in terms of the metric system at
values between 1/5 and 1/4 of a liter.  Because actual drinking cups may differ
greatly from the size of this unit, standard measuring cups are usually used
instead.

In the U.S., the cup is defined to be 8 fluid ounces.

https://en.wikipedia.org/wiki/Cup_(unit)
''' ),

    'dash' :
        RPNUnitInfo( 'volume', 'dashes', '', [ ], [ 'cooking' ],
                     '''
''' ),

    'demi' :
        RPNUnitInfo( 'volume', 'demis', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'dessertspoon' :
        RPNUnitInfo( 'volume', 'dessertspoons', '', [ ], [ 'traditional', 'cooking' ],
                     '''
A dessert spoon is a spoon designed specifically for eating dessert and
sometimes used for soup or cereals.  Similar in size to a soup spoon
(intermediate between a teaspoon and a tablespoon) but with an oval rather than
round bowl, it typically has a capacity around twice that of a teaspoon.

By extension the term 'dessert spoon' is used as a cooking measure of volume,
usually of 10ml or 1/3 fl oz.

Ref:  https://en.wikipedia.org/wiki/Dessert_spoon

Note:  Wikipedia is mistaken.  10 mL is approximately 1/3 fluid ounce, not 0.4
fluid ounce.
''' ),

    'dram' :
        RPNUnitInfo( 'volume', 'drams', '',
                     [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ],
                     '''
''' ),

    'dry_barrel' :
        RPNUnitInfo( 'volume', 'dry_barrels', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
Defined as length of stave 28-1/2 inches (72 cm), diameter of head 17-1/8
inches (43 cm), distance between heads 26 inches (66 cm), circumference of
bulge 64 inches (1.6 m) outside measurement; representing as nearly as
possible 7,056 cubic inches; and the thickness of staves not greater than
4/10 inch (10 mm).  This is exactly equal to 26.25 U.S. dry gallons.

Ref:  https://en.wikipedia.org/wiki/Barrel_(unit)#Dry_goods_in_the_US
''' ),

    'dry_hogshead' :
        RPNUnitInfo( 'volume', 'dry_hogsheads', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
''' ),

    'dry_gallon' :
        RPNUnitInfo( 'volume', 'dry_gallons', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
THe dry gallon is defined to be 1/2 peck, or 4 dry quarts.  The U.S. customary
dry volume measurements correspond with each other the same way the liquid
measurements do.

https://en.wikipedia.org/wiki/United_States_customary_units#Dry_volume
''' ),

    'dry_pint' :
        RPNUnitInfo( 'volume', 'dry_pints', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
THe dry pint is defined to be 1/2 dry quart.  The U.S. customary dry volume
measurements correspond with each other the same way the liquid measurements
do.

https://en.wikipedia.org/wiki/United_States_customary_units#Dry_volume
''' ),

    'dry_quart' :
        RPNUnitInfo( 'volume', 'dry_quarts', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
THe dry quart is defined to be 1/4 dry gallon, or two dry pints.  The U.S.
customary dry volume measurements correspond with each other the same way the
liquid measurements do.

https://en.wikipedia.org/wiki/United_States_customary_units#Dry_volume
''' ),

    'dry_tun' :
        RPNUnitInfo( 'volume', 'dry_tuns', '', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
''' ),

    'farshimmelt_ngogn' :
        RPNUnitInfo( 'volume', 'farshimmelt_ngogns', 'fn',
                     [ 'far-ngogn', 'far-ngogns', 'farshimmelt-ngogn', 'farshimmelt-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fifth' :
        RPNUnitInfo( 'volume', 'fifths', '', [ ], [ 'U.S.', 'liquor' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Liquor_bottles
''' ),

    'firkin' :
        RPNUnitInfo( 'volume', 'firkins', '', [ ], [ 'U.S.', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measures
''' ),

    'fluid_ounce' :
        RPNUnitInfo( 'volume', 'fluid_ounces', '', [ 'floz' ], [ 'traditional' ],
                     '''
A fluid ounce (abbreviated fl oz, fl. oz. or oz. fl.,) is a unit of volume
(also called capacity) typically used for measuring liquids.  Various
definitions have been used throughout history, but only two are still in common
use: the British Imperial and the United States customary fluid ounce.

A U.S. fluid ounce is 1/16 of a US fluid pint and 1/128 of a US liquid gallon
or approximately 29.57 ml, making it about 4% larger than the imperial fluid
ounce.

Ref:  https://en.wikipedia.org/wiki/Fluid_ounce
''' ),

    'foot^3' :
        RPNUnitInfo( 'volume', 'foot^3', '', [ ], [ 'traditional', 'FPS' ],
                     '''
The cubic foot is an imperial and U.S. customary (non-metric) unit of volume,
used in the United States, and partially in Canada, and the United Kingdom.  It
is defined as the volume of a cube with sides of one foot (0.3048 m) in length.

Its volume is 28.3168 liters or about 1/35 of a cubic meter.

https://en.wikipedia.org/wiki/Cubic_foot
''' ),

    'furshlugginer_ngogn' :
        RPNUnitInfo( 'volume', 'furshlugginer_ngogns', 'Fn',
                     [ 'Fur-ngogn', 'Fur-ngogns', 'fur-ngogn', 'fur-ngogns', 'furshlugginer-ngogn', 'furshlugginer-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'gallon' :
        RPNUnitInfo( 'volume', 'gallons', '', [ ], [ 'U.S.' ],
                     '''
The gallon is a unit of measurement for volume and fluid capacity in both the
U.S. customary units and the British imperial systems of measurement.

The U.S. gallon is defined as 231 cubic inches (4 U.S. liquid quarts or 8 U.S.
liquid pints) or exactly 3.785411784 liters,

Ref:  https://en.wikipedia.org/wiki/Gallon
''' ),

    'gill' :
        RPNUnitInfo( 'volume', 'gills', '',
                     [ 'noggin', 'noggins', 'teacup', 'teacups' ], [ 'U.S.' ],
                     '''
''' ),

    'goliath' :
        RPNUnitInfo( 'volume', 'goliaths', '', [ 'primat' ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'grand_canyon' :
        RPNUnitInfo( 'volume', 'grand_canyons', '', [ ], [ 'informal' ],
                     '''
With a volume measure approximately 4 orders of magnitude greater than a
sydharb, the volume of the Grand Canyon may be used to visualize even larger
things, like the magma chamber underneath Yellowstone and other things.

According to the National Park Service, the volume of the Grand Canyon is
4.17 trillion cubic metres (5.45 trillion cubic yards).

Ref:  https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement#The_Grand_Canyon
''' ),

    'growler' :
        RPNUnitInfo( 'volume', 'growlers', '', [ ], [ 'U.S.', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measures
''' ),

    'hoppus_foot' :
        RPNUnitInfo( 'volume', 'hoppus_feet', '', [ 'hoppus_cube', 'hoppus_cubes' ], [ 'England', 'obsolete' ],
                     '''
The hoppus cubic foot (or 'hoppus cube') was the standard volume measurement
used for timber in the British Empire and countries in the British sphere of
influence before the introduction of metric units.  It is still used in the
hardwood trade of some countries.  This volume measurement was developed to
estimate what volume of a round log would be usable timber after processing,
in effect attempting to 'square' the log and allow for waste.

The English surveyor Edward Hoppus introduced the eponymous unit in his 1736
manual of practical calculations.

Ref:  https://en.wikipedia.org/wiki/Hoppus
''' ),

    'hoppus_ton' :
        RPNUnitInfo( 'volume', 'hoppus_tons', '', [ ], [ 'England', 'obsolete' ],
                     '''
The hoppus ton (HT) was also a traditionally used unit of volume in British
forestry. One hoppus ton is equal to 50 hoppus feet or 1.8027 cubic meters.
Some shipments of tropical hardwoods, especially shipments of teak from
Myanmar (Burma), are still stated in hoppus tons.

Ref:  https://en.wikipedia.org/wiki/Hoppus
''' ),

    'imperial_barrel' :
        RPNUnitInfo( 'volume', 'imperial_barrels', '', [ ], [ 'imperial', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'imperial_bushel' :
        RPNUnitInfo( 'volume', 'imperial_bushels', '', [ ], [ 'imperial', 'dry_measure' ],
                     '''
''' ),

    'imperial_butt' :
        RPNUnitInfo( 'volume', 'imperial_butts', '', [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'imperial_cup' :
        RPNUnitInfo( 'volume', 'imperial_cups', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gallon' :
        RPNUnitInfo( 'volume', 'imperial_gallons', '', [ 'congius', 'congii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gill' :
        RPNUnitInfo( 'volume', 'imperial_gills', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_hogshead' :
        RPNUnitInfo( 'volume', 'imperial_hogsheads', '', [ ], [ 'imperial', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'imperial_peck' :
        RPNUnitInfo( 'volume', 'imperial_pecks', '', [ ], [ 'imperial', 'dry_measure' ],
                     '''
A peck is an imperial and United States customary unit of dry volume,
equivalent to 2 dry gallons or 8 dry quarts or 16 dry pints.  Two pecks make a
kenning (obsolete), and four pecks make a bushel.  Although the peck is no
longer widely used, some produce, such as apples, is still often sold by the peck.

Ref:  https://en.wikipedia.org/wiki/Peck
''' ),

    'imperial_pint' :
        RPNUnitInfo( 'volume', 'imperial_pints', '', [ 'octarius', 'octarii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_puncheon' :
        RPNUnitInfo( 'volume', 'imperial_puncheons', '', [ 'imperial_tertian', 'imperial_tertians' ], [ 'imperial', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'imperial_quart' :
        RPNUnitInfo( 'volume', 'imperial_quarts', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_tun' :
        RPNUnitInfo( 'volume', 'wine_tuns', '', [ ], [ 'imperial', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'inch^3' :
        RPNUnitInfo( 'volume', 'inch^3', '', [ ], [ 'traditional' ],
                     '''
''' ),

    'jennie' :
        RPNUnitInfo( 'volume', 'jennies', '', [ ], [ 'wine' ],
                     '''
''' ),

    'jeroboam' :
        RPNUnitInfo( 'volume', 'jeroboams', '', [ 'double_magnum', 'double_magnums' ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'jigger' :
        RPNUnitInfo( 'volume', 'jiggers', '', [ 'short_shot', 'short_shots' ], [ 'U.S.', 'liquor' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Liquor_measurements
''' ),

    'kenning' :
        RPNUnitInfo( 'volume', 'kennings', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'kilderkin' :
        RPNUnitInfo( 'volume', 'kilderkins', '', [ ], [ 'imperial', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measures
''' ),

    'liter' :
        RPNUnitInfo( 'volume', 'liters', 'L', [ 'litre', 'litres' ], [ 'SI' ],
        # The U.S. standard is to use uppercase "L" because the lower case 'l' looks like a 1
                     '''
The liter is an SI  accepted metric system unit of volume equal to 1 cubic
decimeter (dm^3), 1,000 cubic centimeters (cm^3) or 1/1,000 cubic meter.

Ref:  https://en.wikipedia.org/wiki/Litre
''' ),

    'magnum' :
        RPNUnitInfo( 'volume', 'magnums', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'marie_jeanne' :
        RPNUnitInfo( 'volume', 'marie_jeannes', '', [ 'dame_jeanne', 'dame_jeannes' ], [ 'France', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Liquor_bottles
''' ),

    'melchior' :
        RPNUnitInfo( 'volume', 'melchiors', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'melchizedek' :
        RPNUnitInfo( 'volume', 'melchizedeks', '', [ 'midas', 'midases' ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'meter^3' :
        RPNUnitInfo( 'volume', 'meter^3', '', [ ], [ 'SI' ],
                     '''
''' ),

    'methuselah' :
        RPNUnitInfo( 'volume', 'methuselahs', '', [ 'mathusalem', 'mathusalems' ], [ 'France', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Liquor_bottles
''' ),

    'minim' :
        RPNUnitInfo( 'volume', 'minims', 'gtt', [ 'drop' ], [ 'traditional' ],
                     '''
''' ),

    'mordechai' :
        RPNUnitInfo( 'volume', 'mordechais', '', [ ], [ 'wine' ],
                     '''
''' ),

    'nebuchadnezzar' :
        RPNUnitInfo( 'volume', 'nebuchadnezzars', '', [ 'nabuchodonosor', 'nabuchodonosors' ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'ngogn' :
        RPNUnitInfo( 'volume', 'ngogns', '', [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'oil_barrel' :
        RPNUnitInfo( 'volume', 'oil_barrels', 'bbl', [ ], [ 'U.S.' ],
                     '''
''' ),

    'peck' :
        RPNUnitInfo( 'volume', 'pecks', 'pk', [ ], [ 'U.S.', 'dry_measure' ],
                     '''
A peck is an imperial and United States customary unit of dry volume,
equivalent to 2 dry gallons or 8 dry quarts or 16 dry pints.  Two pecks make a
kenning (obsolete), and four pecks make a bushel.  Although the peck is no
longer widely used, some produce, such as apples, is still often sold by the peck.

Ref:  https://en.wikipedia.org/wiki/Peck
''' ),

    'piccolo' :
        RPNUnitInfo( 'volume', 'piccolos', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'pinch' :
        RPNUnitInfo( 'volume', 'pinches', '', [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'pin' :
        RPNUnitInfo( 'volume', 'pins', '', [ ], [ 'imperial', 'beer' ],
                     '''
''' ),

    'pint' :
        RPNUnitInfo( 'volume', 'pints', 'pt', [ ], [ 'traditional', 'cooking', 'U.S.' ],
                     '''
The pint, symbol pt, is a unit of volume or capacity in both the imperial and
United States customary measurement systems.  In both of those systems it is
traditionally one-eighth of a gallon.

https://en.wikipedia.org/wiki/Pint
''' ),

    'pony' :
        RPNUnitInfo( 'volume', 'ponies', '', [ ], [ 'U.S.', 'liquor' ],
                     '''
''' ),

    'pony_keg' :
        RPNUnitInfo( 'volume', 'pony_kegs', '', [ ], [ 'U.S.', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Beer_measures
''' ),

    'portuguese_almude' :
        RPNUnitInfo( 'volume', 'portuguese_almudes', '', [ ], [ 'Portugal' ],
                     '''
''' ),

    'pottle' :
        RPNUnitInfo( 'volume', 'pottles', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'puncheon' :
        RPNUnitInfo( 'volume', 'puncheons', '', [ ], [ 'U.S.', 'wine', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'quart' :
        RPNUnitInfo( 'volume', 'quarts', 'qt', [ ], [ 'U.S.' ],
                     '''
The quart (abbreviation qt.) is an English unit of volume equal to a quarter
gallon.  It is divided into two pints or four cups.  Historically, the exact
size of the quart has varied with the different values of gallons over time and
in reference to different commodities.  Presently, three kinds of quarts remain
in use: the liquid quart and dry quart of the U.S. customary system and the
imperial quart of the British imperial system. All are roughly equal to one
metric liter.

In the U.S., the quart is defined to be 32 fluid ounces.

Ref:  https://en.wikipedia.org/wiki/Quart
''' ),

    'rehoboam' :
        RPNUnitInfo( 'volume', 'rehoboams', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'rundlet' :
        RPNUnitInfo( 'volume', 'rundlets', '', [ ], [ 'U.S.', 'wine' ],
                     '''
https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'salmanazar' :
        RPNUnitInfo( 'volume', 'salmanazars', '', [ ], [ 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Alcohol_measurements#Wine_measurements
''' ),

    'saltspoon' :
        RPNUnitInfo( 'volume', 'saltspoons', '', [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'scruple' :
        RPNUnitInfo( 'volume', 'scruples', '',
                     [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ],
                     '''
''' ),

    'smidgen' :
        RPNUnitInfo( 'volume', 'smidgens', '',
                     [ 'smidgeon', 'smidgeons' ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'snit' :
        RPNUnitInfo( 'volume', 'snits', '', [ ], [ 'U.S.', 'liquor' ],
                     '''
http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'spanish_almude' :
        RPNUnitInfo( 'volume', 'spanish_almudes', '', [ ], [ 'Spain' ],
                     '''
''' ),

    'solomon' :
        RPNUnitInfo( 'volume', 'solomons', '', [ ], [ 'France', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'sovereign' :
        RPNUnitInfo( 'volume', 'sovereigns', '', [ ], [ 'France', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'stein' :
        RPNUnitInfo( 'volume', 'steins', '', [ ], [ 'Germany' ],
                     '''
A stein is a German beer mug.  Steins come in various sizes, but the most
common size seems to be 1/2 liter (1.057 U.S pint or 0.880 British Imperial
pint).

http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'stere' :
        RPNUnitInfo( 'volume', 'steres', 'st', [ ], [ 'metric', 'obsolete' ],  # ... but not SI
                     '''
''' ),

    'sydharb' :
        RPNUnitInfo( 'volume', 'sydharbs', '', [ ], [ 'informal' ],
                     '''
The approximate volume of the Syndey Harbor at high tide, considered to be
equal to 562,000 megaliters.

https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement#Sydney_Harbour
''' ),

    'tablespoon' :
        RPNUnitInfo( 'volume', 'tablespoons', 'tbsp', [ ], [ 'traditional', 'cooking' ],
                     '''
A tablespoon is a large spoon used for serving or eating.

By extension, the term is also used as a cooking measure of volume.  In this
capacity, it is most commonly abbreviated tbsp, and occasionally referred to
as a tablespoonful to distinguish it from the utensil.  A United States
tablespoon is approximately 14.8 ml (0.50 U.S. fl oz).

Ref:  https://en.wikipedia.org/wiki/Tablespoon
''' ),

    'teaspoon' :
        RPNUnitInfo( 'volume', 'teaspoons', 'tsp', [ ], [ 'traditional', 'cooking' ],
                     '''
A teaspoon is an item of cutlery, a small spoon.

By extension the term 'teaspoon' (usually abbreviated tsp.) is used as a
cooking measure of volume, of approximately 5 ml.

Ref:  https://en.wikipedia.org/wiki/Teaspoon
''' ),

    'tierce' :
        RPNUnitInfo( 'volume', 'tierces', '', [ ], [ 'U.S.', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'tun' :
        RPNUnitInfo( 'volume', 'tuns', '', [ ], [ 'U.S.', 'wine', 'beer' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'wine_barrel' :
        RPNUnitInfo( 'volume', 'wine_barrels', '', [ ], [ 'U.S.', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'wine_bottle' :
        RPNUnitInfo( 'volume', 'wine_bottles', '', [ 'bottle', 'bottles' ], [ 'wine' ],
                     '''
A wine bottle is a bottle, generally made of glass, that is used for holding
wine.  Some wines are fermented in the bottle, others are bottled only after
fermentation.  Recently the bottle has become a standard unit of volume to
describe sales in the wine industry, measuring 750 milliliters (26.40 imp. fl.
oz.; 25.36 U.S. fl. oz.).

Ref:  https://en.wikipedia.org/wiki/Wine_bottle
''' ),

    'wine_hogshead' :
        RPNUnitInfo( 'volume', 'hogsheads', '', [ ], [ 'U.S.', 'wine' ],
                     '''
Ref:  https://en.wikipedia.org/wiki/Tun_(unit)
''' ),

    'wineglass' :
        RPNUnitInfo( 'volume', 'wineglasses', '',
                     [ 'wine_glass', 'wine_glasses' ], [ 'imperial', 'wine' ],
                     '''
As a supplemental unit of apothecary measure, the wineglass (also known as
wineglassful, pl. wineglassesful, or cyathus vinarius in pharmaceutical Latin)
was defined as 1/8 of a pint, or 2 fluid ounces.

Ref:  https://en.wikipedia.org/wiki/Wine_glass#Capacity_measure
''' ),
}


# //******************************************************************************
# //
# //  metricUnits
# //
# //  ... or any units that should get the SI prefixes
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

metricUnits = [
    'ampere',
    'arcsecond',
    'are',
    'bar',
    'barn',
    'becquerel',
    'blintz',
    'calorie',
    'circular_mil',
    'coulomb',
    'curie',
    'dyne',
    'electron-volt',
    'erg',
    'farad',
    'galileo',
    'gauss',
    'gram',
    'gram_equivalent',
    'gram_force',
    'gray',
    'henry',
    'hertz',
    'joule',
    'katal',
    'kelvin',
    'liter',
    'lumen',
    'lux',
    'maxwell',
    'meter',
    'mole',
    'newton',
    'ngogn',
    'ohm',
    'parsec',
    'pascal',
    'poise',
    'pond',
    'potrzebie',
    'rad',
    'radian',
    'rem',
    'second',
    'siemens',
    'sievert',
    'steradian',
    'stere',
    'tesla',
    'volt',
    'watt',
    'weber',
]


# //******************************************************************************
# //
# //  integralMetricUnits
# //
# //  Any units that should get the SI prefixes with positive powers.
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

integralMetricUnits = [
    'light-year',
    'ton',
    'tonne',
    'ton_of_TNT',
    'year',
]


# //******************************************************************************
# //
# //  dataUnits
# //
# //  ... or any units that should get the SI prefixes (positive powers of 10)
# //  and the binary prefixes
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

dataUnits = [
    'bit',
    'bit/second',
    'byte',
    'byte/second',
]


# //******************************************************************************
# //
# //  units that compound with time
# //
# //  Anything that goes here needs to have an abbreviation.
# //
# //******************************************************************************

compoundTimeUnits = [
    'ampere',
    'pascal',
    'watt',
]


# //******************************************************************************
# //
# //  timeUnits
# //
# //******************************************************************************

timeUnits = {
    'second' : 's',
    'minute' : 'm',
    'hour'   : 'h',
    'day'    : 'd',
    'year'   : 'y',
}


# //******************************************************************************
# //
# //  metricPrefixes
# //
# //  ( name, abbreviation, power of 10 )
# //
# //******************************************************************************

metricPrefixes = [
    ( 'yotta',      'Y',      24 ),
    ( 'zetta',      'Z',      21 ),
    ( 'exa',        'E',      18 ),
    ( 'peta',       'P',      15 ),
    ( 'tera',       'T',      12 ),
    ( 'giga',       'G',      9 ),
    ( 'mega',       'M',      6 ),
    ( 'kilo',       'k',      3 ),
    ( 'hecto',      'h',      2 ),
    ( 'deca',       'da',     1 ),
    ( 'deci',       'd',      -1 ),
    ( 'centi',      'c',      -2 ),
    ( 'milli',      'm',      -3 ),
    ( 'micro',      'u',      -6 ),  # it's really a mu
    ( 'nano',       'n',      -9 ),
    ( 'pico',       'p',      -12 ),
    ( 'femto',      'f',      -15 ),
    ( 'atto',       'a',      -18 ),
    ( 'zepto',      'z',      -21 ),
    ( 'yocto',      'y',      -24 ),
]

# //******************************************************************************
# //
# //  dataPrefixes
# //
# //  ( name, abbreviation, power of 10 )
# //
# //******************************************************************************

dataPrefixes = [
    ( 'yotta',      'Y',      24 ),
    ( 'zetta',      'Z',      21 ),
    ( 'exa',        'E',      18 ),
    ( 'peta',       'P',      15 ),
    ( 'tera',       'T',      12 ),
    ( 'giga',       'G',      9 ),
    ( 'mega',       'M',      6 ),
    ( 'kilo',       'k',      3 ),
]


# //******************************************************************************
# //
# //  binaryPrefixes
# //
# //  ( name, abbreviation, power of 2 )
# //
# //******************************************************************************

binaryPrefixes = [
    ( 'yobi',       'Yi',     80 ),
    ( 'zebi',       'Zi',     70 ),
    ( 'exi',        'Ei',     60 ),
    ( 'pebi',       'Pi',     50 ),
    ( 'tebi',       'Ti',     40 ),
    ( 'gibi',       'Gi',     30 ),
    ( 'mebi',       'Mi',     20 ),
    ( 'kibi',       'ki',     10 ),
]


# //******************************************************************************
# //
# //  unitConversionMatrix
# //
# //  ( first unit, second unit, conversion factor )
# //
# //******************************************************************************

unitConversionMatrix = {
    # acceleration

    ( 'celo',                       'meter/second^2' )                      : mpmathify( '0.3048' ),
    ( 'galileo',                    'meter/second^2' )                      : mpmathify( '0.01' ),
    ( 'leo',                        'meter/second^2' )                      : mpmathify( '10' ),

    # amount_of_substance

    # angle

    ( 'arcminute',                  'arcsecond' )                           : mpmathify( '60' ),
    ( 'circle',                     'degree' )                              : mpmathify( '360' ),
    ( 'degree',                     'arcminute' )                           : mpmathify( '60' ),
    ( 'degree',                     'furman' )                              : mpmathify( '65536' ),
    ( 'degree',                     'streck' )                              : mpmathify( '17.5' ),
    ( 'grad',                       'degree' )                              : mpmathify( '0.9' ),
    ( 'octant',                     'degree' )                              : mpmathify( '45' ),
    ( 'pointangle',                 'degree' )                              : fdiv( 360, 32 ),
    ( 'quadrant',                   'degree' )                              : mpmathify( '90' ),
    ( 'quintant',                   'degree' )                              : mpmathify( '72' ),
    ( 'radian',                     'centrad' )                             : mpmathify( '100' ),
    ( 'radian',                     'degree' )                              : fdiv( 180, pi ),
    ( 'sextant',                    'degree' )                              : mpmathify( '60' ),

    # area

    ( 'acre',                       'foot^2' )                              : mpmathify( '43560' ),
    ( 'acre',                       'nanoacre' )                            : mpmathify( '1.0e9' ),
    ( 'are',                        'meter^2' )                             : mpmathify( '100' ),
    ( 'carucate',                   'acre' )                                : mpmathify( '120' ),
    ( 'carucate',                   'bovate' )                              : mpmathify( '8' ),
    ( 'circular_inch',              'circular_mil' )                        : mpmathify( '1.0e6' ),
    ( 'circular_mil',               'meter^2' )                             : mpmathify( '5.06707479097497751431639751289151020192161452425209293e-10' ), # rpn -a54 1 2000 / inch meter convert 2 ^ pi *
    ( 'homestead',                  'acre' )                                : mpmathify( '160' ),
    ( 'imperial_square',            'foot^2' )                              : mpmathify( '100' ),
    ( 'meter^2',                    'barn' )                                : mpmathify( '1.0e28' ),
    ( 'meter^2',                    'foot^2' )                              : mpmathify( '10.7639104167097223083335055559000006888902666694223868' ),  # (meter/foot)^2
    ( 'meter^2',                    'outhouse' )                            : mpmathify( '1.0e34' ),
    ( 'meter^2',                    'shed' )                                : mpmathify( '1.0e52' ),
    ( 'morgen',                     'are' )                                 : mpmathify( '85.6532' ),
    ( 'rood',                       'foot^2' )                              : mpmathify( '272.25' ),   # same as a square rod!
    ( 'section',                    'acre' )                                : mpmathify( '640' ),
    ( 'township',                   'acre' )                                : mpmathify( '23040' ),   # 36 square miles
    ( 'virgate',                    'bovate' )                              : mpmathify( '30' ),

    # capacitance

    ( 'abfarad',                    'farad' )                               : mpmathify( '1.0e9' ),
    ( 'farad',                      'ampere^2*second^4/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'farad',                      'jar' )                                 : mpmathify( '9.0e8' ),
    ( 'farad',                      'statfarad' )                           : mpmathify( '898755178736.5' ),

    # catalysis

    ( 'katal',                      'enzyme_unit' )                         : mpmathify( '6.0e7' ),
    ( 'katal',                      'mole/second' )                         : mpmathify( '1' ),

    # charge

    ( 'abcoulomb',                  'coulomb' )                             : mpmathify( '10' ),
    ( 'coulomb',                    'ampere*second' )                       : mpmathify( '1' ),
    ( 'faraday',                    'coulomb' )                             : mpmathify( '96485.3383' ),
    ( 'statcoulomb',                'coulomb' )                             : mpmathify( '3.335641e-10' ),  # 0.1A*m/c, approx.
    ( 'statcoulomb',                'franklin' )                            : mpmathify( '1' ),

    # constant

    ( 'billion',                    'unity' )                               : mpmathify( '1.0e9' ),
    ( 'centillion',                 'unity' )                               : mpmathify( '1.0e303' ),
    ( 'decillion',                  'unity' )                               : mpmathify( '1.0e33' ),
    ( 'duodecillion',               'unity' )                               : mpmathify( '1.0e39' ),
    ( 'eight',                      'unity' )                               : mpmathify( '8' ),
    ( 'eighteen',                   'unity' )                               : mpmathify( '18' ),
    ( 'eighty',                     'unity' )                               : mpmathify( '80' ),
    ( 'eleven',                     'unity' )                               : mpmathify( '11' ),
    ( 'fifteen',                    'unity' )                               : mpmathify( '15' ),
    ( 'fifty',                      'unity' )                               : mpmathify( '50' ),
    ( 'five',                       'unity' )                               : mpmathify( '5' ),
    ( 'forty',                      'unity' )                               : mpmathify( '40' ),
    ( 'four',                       'unity' )                               : mpmathify( '4' ),
    ( 'fourteen',                   'unity' )                               : mpmathify( '14' ),
    ( 'googol',                     'unity' )                               : mpmathify( '1.0e100' ),
    ( 'great_gross',                'gross' )                               : mpmathify( '12' ),
    ( 'gross',                      'unity' )                               : mpmathify( '144' ),
    ( 'hundred',                    'unity' )                               : mpmathify( '100' ),
    ( 'long_hundred',               'unity' )                               : mpmathify( '120' ),
    ( 'million',                    'unity' )                               : mpmathify( '1.0e6' ),
    ( 'nine',                       'unity' )                               : mpmathify( '9' ),
    ( 'nineteen',                   'unity' )                               : mpmathify( '19' ),
    ( 'ninety',                     'unity' )                               : mpmathify( '90' ),
    ( 'nonillion',                  'unity' )                               : mpmathify( '1.0e30' ),
    ( 'novemdecillion',             'unity' )                               : mpmathify( '1.0e60' ),
    ( 'octillion',                  'unity' )                               : mpmathify( '1.0e27' ),
    ( 'octodecillion',              'unity' )                               : mpmathify( '1.0e57' ),
    ( 'quadrillion',                'unity' )                               : mpmathify( '1.0e15' ),
    ( 'quattuordecillion',          'unity' )                               : mpmathify( '1.0e45' ),
    ( 'quindecillion',              'unity' )                               : mpmathify( '1.0e48' ),
    ( 'quintillion',                'unity' )                               : mpmathify( '1.0e18' ),
    ( 'septendecillion',            'unity' )                               : mpmathify( '1.0e54' ),
    ( 'septillion',                 'unity' )                               : mpmathify( '1.0e24' ),
    ( 'seven',                      'unity' )                               : mpmathify( '7' ),
    ( 'seventeen',                  'unity' )                               : mpmathify( '17' ),
    ( 'seventy',                    'unity' )                               : mpmathify( '70' ),
    ( 'sexdecillion',               'unity' )                               : mpmathify( '1.0e51' ),
    ( 'sextillion',                 'unity' )                               : mpmathify( '1.0e21' ),
    ( 'six',                        'unity' )                               : mpmathify( '6' ),
    ( 'sixteen',                    'unity' )                               : mpmathify( '16' ),
    ( 'sixty',                      'unity' )                               : mpmathify( '60' ),
    ( 'ten',                        'unity' )                               : mpmathify( '10' ),
    ( 'thirteen',                   'unity' )                               : mpmathify( '13' ),
    ( 'thirty',                     'unity' )                               : mpmathify( '30' ),
    ( 'thousand',                   'unity' )                               : mpmathify( '1000' ),
    ( 'three',                      'unity' )                               : mpmathify( '3' ),
    ( 'tredecillion',               'unity' )                               : mpmathify( '1.0e42' ),
    ( 'trillion',                   'unity' )                               : mpmathify( '1.0e12' ),
    ( 'twelve',                     'unity' )                               : mpmathify( '12' ),
    ( 'twenty',                     'unity' )                               : mpmathify( '20' ),
    ( 'two',                        'unity' )                               : mpmathify( '2' ),
    ( 'undecillion',                'unity' )                               : mpmathify( '1.0e36' ),
    ( 'unity',                      'billionth' )                           : mpmathify( '1.0e9' ),
    ( 'unity',                      'decillionth' )                         : mpmathify( '1.0e33' ),
    ( 'unity',                      'half' )                                : mpmathify( '2' ),
    ( 'unity',                      'millionth' )                           : mpmathify( '1.0e6' ),
    ( 'unity',                      'nonillionth' )                         : mpmathify( '1.0e30' ),
    ( 'unity',                      'octillionth' )                         : mpmathify( '1.0e27' ),
    ( 'unity',                      'percent' )                             : mpmathify( '100' ),
    ( 'unity',                      'quadrillionth' )                       : mpmathify( '1.0e15' ),
    ( 'unity',                      'quarter' )                             : mpmathify( '4' ),
    ( 'unity',                      'quintillionth' )                       : mpmathify( '1.0e18' ),
    ( 'unity',                      'septillionth' )                        : mpmathify( '1.0e24' ),
    ( 'unity',                      'sextillionth' )                        : mpmathify( '1.0e21' ),
    ( 'unity',                      'tenth' )                               : mpmathify( '10' ),
    ( 'unity',                      'third' )                               : mpmathify( '3' ),
    ( 'unity',                      'thousandth' )                          : mpmathify( '1000' ),
    ( 'unity',                      'trillionth' )                          : mpmathify( '1.0e12' ),
    ( 'vigintillion',               'unity' )                               : mpmathify( '1.0e63' ),

    # current

    ( 'abampere',                   'ampere' )                              : mpmathify( '10' ),
    ( 'ampere',                     'statampere' )                          : mpmathify( '299792458' ),

    # data_rate

    ( 'byte/second',                'bit/second' )                          : mpmathify( '8' ),
    ( 'oc1',                        'bit/second' )                          : mpmathify( '5.184e7' ),
    ( 'oc12',                       'oc1' )                                 : mpmathify( '12' ),
    ( 'oc192',                      'oc1' )                                 : mpmathify( '192' ),
    ( 'oc24',                       'oc1' )                                 : mpmathify( '24' ),
    ( 'oc3',                        'oc1' )                                 : mpmathify( '3' ),
    ( 'oc48',                       'oc1' )                                 : mpmathify( '48' ),
    ( 'oc768',                      'oc1' )                                 : mpmathify( '768' ),
    ( 'usb1',                       'bit/second' )                          : mpmathify( '1.2e7' ),
    ( 'usb2',                       'bit/second' )                          : mpmathify( '2.8e8' ),
    ( 'usb3.0',                     'bit/second' )                          : mpmathify( '5.0e9' ),
    ( 'usb3.1',                     'bit/second' )                          : mpmathify( '1.0e10' ),

    # density

    # dynamic_viscosity

    ( 'poise',                      'kilogram/meter*second' )               : mpmathify( '10' ),
    ( 'reynolds',                   'kilogram/meter*second' )               : mpmathify( '6894.75729' ),

    # electrical_conductance

    ( 'abmho',                      'siemens' )                             : mpmathify( '1.0e9' ),
    ( 'conductance_quantum',        'siemens' )                             : mpmathify( '7.7480917310e-5' ),
    ( 'siemens',                    'ampere^2*second^3/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'siemens',                    'statsiemens' )                         : mpmathify( '898755178736.5' ),
    ( 'statmho',                    'siemens' )                             : mpmathify( '8.99e11' ),

    # electrical_resistance

    ( 'ohm',                        '1/siemens' )                           : mpmathify( '1' ),
    ( 'ohm',                        'abohm' )                               : mpmathify( '1e9' ),
    ( 'ohm',                        'german_mile' )                         : mpmathify( '57.44' ),
    ( 'ohm',                        'jacobi' )                              : mpmathify( '0.6367' ),
    ( 'ohm',                        'kilogram*meter^2/ampere^2*second^3' )  : mpmathify( '1' ),
    ( 'ohm',                        'matthiessen' )                         : mpmathify( '13.59' ),
    ( 'ohm',                        'varley' )                              : mpmathify( '25.61' ),
    ( 'statohm',                    'ohm' )                                 : mpmathify( '898755178740' ),

    # electric_potential

    ( 'statvolt',                   'volt' )                                : fdiv( 299792458, 1000000 ),
    ( 'volt',                       'abvolt' )                              : mpmathify( '1.0e8' ),
    ( 'volt',                       'kilogram*meter^2/ampere*second^3' )    : mpmathify( '1' ),

    # energy

    ( 'btu',                        'joule' )                               : mpmathify( '1054.5' ),
    ( 'calorie',                    'joule' )                               : mpmathify( '4.184' ),
    ( 'electron-volt',              'joule' )                               : mpmathify( '1.6021766208e-19' ),
    ( 'foe',                        'joule' )                               : mpmathify( '10e44' ),
    ( 'gram_equivalent',            'joule' )                               : fdiv( power( 299792458, 2 ), 1000 ),
    ( 'hartree',                    'rydberg' )                             : mpmathify( '2' ),
    ( 'joule',                      'erg' )                                 : mpmathify( '1.0e7' ),
    ( 'joule',                      'kilogram*meter^2/second^2' )           : mpmathify( '1' ),
    ( 'kayser',                     'electron-volt' )                       : mpmathify( '123.984e-6' ),
    ( 'quad',                       'btu' )                                 : mpmathify( '10e15' ),
    ( 'rydberg',                    'joule' )                               : mpmathify( '2.17987232498e-18' ),
    ( 'therm',                      'btu' )                                 : mpmathify( '100000' ),
    ( 'toe',                        'calorie' )                             : mpmathify( '1.0e10' ),
    ( 'ton_of_coal',                'joule' )                               : mpmathify( '29.288e9' ),
    ( 'ton_of_TNT',                 'joule' )                               : mpmathify( '4.184e9' ),
    ( 'ton_of_TNT',                 'pound_of_TNT' )                        : mpmathify( '2000' ),

    # force

    ( 'gram_force',                 'newton' )                              : mpmathify( '0.00980665' ),
    ( 'newton',                     'dyne' )                                : mpmathify( '1.0e5' ),
    ( 'newton',                     'kilogram*meter/second^2' )             : mpmathify( '1' ),
    ( 'newton',                     'pond' )                                : mpmathify( '101.97161298' ),
    ( 'newton',                     'poundal' )                             : mpmathify( '7.233013851' ),
    ( 'pound-force',                'newton' )                              : mpmathify( '4.4482216152605' ),
    ( 'sthene',                     'newton' )                              : mpmathify( '1000' ),

    # frequency

    ( 'curie',                      'becquerel' )                           : mpmathify( '3.7e10' ),
    ( 'hertz',                      '1/second' )                            : mpmathify( '1' ),
    ( 'hertz',                      'becquerel' )                           : mpmathify( '1' ),
    ( 'rutherford',                 'becquerel' )                           : mpmathify( '1.0e6' ),

    # illuminance

    ( 'candela*radian^2/meter^2',   'lumen/meter^2' )                       : mpmathify( '1' ),
    ( 'flame',                      'lux' )                                 : mpmathify( '43.0556416668' ),
    ( 'footcandle',                 'lux' )                                 : mpmathify( '10.7639104167097223083335055559000006888902666694223868' ), # rpn -a54 meter foot convert sqr value
    ( 'lux',                        'lumen/meter^2' )                       : mpmathify( '10.7639104167' ),
    ( 'lux',                        'nox' )                                 : mpmathify( '1000' ),
    ( 'phot',                       'lux' )                                 : mpmathify( '10000' ),

    # inductance

    ( 'henry',                      'abhenry' )                             : mpmathify( '1.0e9' ),
    ( 'henry',                      'kilogram*meter^2/ampere^2*second^2' )  : mpmathify( '1' ),
    ( 'stathenry',                  'henry' )                               : mpmathify( '898755178740' ),

    # information_entropy

    ( 'bit',                        'kilogram*meter^2/kelvin*second^2' )    : fmul( mpmathify( '1.38064852e-23' ), log( 2 ) ),
    ( 'bit',                        'nat' )                                 : log( 2 ),
    ( 'btupf',                      'joule/kelvin' )                        : mpmathify( '1899.100534716' ),
    ( 'byte',                       'bit' )                                 : mpmathify( '8' ),
    ( 'clausius',                   'joule/kelvin' )                        : mpmathify( '4186.8' ),
    ( 'dword',                      'bit' )                                 : mpmathify( '32' ),
    ( 'hartley',                    'nat' )                                 : log( 10 ),
    ( 'library_of_congress',        'byte' )                                : mpmathify( '1.0e13' ),
    ( 'nat',                        'joule/kelvin' )                        : mpmathify( '1.380650e-23' ),
    ( 'nibble',                     'bit' )                                 : mpmathify( '4' ),
    ( 'nyp',                        'bit' )                                 : mpmathify( '2' ),
    ( 'oword',                      'bit' )                                 : mpmathify( '128' ),
    ( 'qword',                      'bit' )                                 : mpmathify( '64' ),
    ( 'trit',                       'nat' )                                 : log( 3 ),
    ( 'tryte',                      'trit' )                                : mpmathify( '6' ),   # as defined by the Setun computer
    ( 'word',                       'bit' )                                 : mpmathify( '16' ),

    # jerk

    ( 'stapp',                      'meter/second^3' )                      : mpmathify( '9.80665' ),

    # jounce

    # length

    ( 'aln',                        'inch' )                                : mpmathify( '23.377077865' ),
    ( 'arpent',                     'foot' )                                : mpmathify( '192' ),
    ( 'arshin',                     'pyad' )                                : mpmathify( '4' ),
    ( 'astronomical_unit',          'meter' )                               : mpmathify( '149597870691' ),
    ( 'barleycorn',                 'poppyseed' )                           : mpmathify( '4' ),
    ( 'bolt',                       'foot' )                                : mpmathify( '120' ),
    ( 'chain',                      'yard' )                                : mpmathify( '22' ),
    ( 'cubit',                      'inch' )                                : mpmathify( '18' ),
    ( 'diuym',                      'inch' )                                : mpmathify( '1' ),
    ( 'diuym',                      'liniya' )                              : mpmathify( '10' ),
    ( 'ell',                        'inch' )                                : mpmathify( '45' ),
    ( 'famn',                       'aln' )                                 : mpmathify( '3' ),
    ( 'fathom',                     'foot' )                                : mpmathify( '6' ),
    ( 'finger',                     'inch' )                                : mpmathify( '4.5' ),
    ( 'fingerbreadth',              'inch' )                                : mpmathify( '0.75' ),
    ( 'foot',                       'inch' )                                : mpmathify( '12' ),
    ( 'furlong',                    'yard' )                                : mpmathify( '220' ),
    ( 'fut',                        'foot' )                                : mpmathify( '1' ),
    ( 'greek_cubit',                'inch' )                                : mpmathify( '18.22' ),
    ( 'hand',                       'inch' )                                : mpmathify( '4' ),
    ( 'handbreadth',                'inch' )                                : mpmathify( '3' ),
    ( 'hubble',                     'light-year' )                          : mpmathify( '1.0e9' ),
    ( 'inch',                       'barleycorn' )                          : mpmathify( '3' ),
    ( 'inch',                       'caliber' )                             : mpmathify( '100' ),
    ( 'inch',                       'cicero' )                              : fdiv( mpmathify( '50.8' ), 9 ),
    ( 'inch',                       'gutenberg' )                           : mpmathify( '7200' ),
    ( 'inch',                       'meter' )                               : mpmathify( '0.0254' ),
    ( 'inch',                       'mil' )                                 : mpmathify( '1000' ),
    ( 'inch',                       'pica' )                                : mpmathify( '6' ),
    ( 'inch',                       'point' )                               : mpmathify( '72' ),
    ( 'inch',                       'twip' )                                : mpmathify( '1440' ),
    ( 'ken',                        'inch' )                                : mpmathify( '83.4' ),
    ( 'kosaya_sazhen',              'meter' )                               : mpmathify( '2.48' ),
    ( 'league',                     'mile' )                                : mpmathify( '3' ),
    ( 'light-second',               'meter' )                               : mpmathify( '299792458' ),
    ( 'light-year',                 'light-second' )                        : mpmathify( '31557600' ),
    ( 'link',                       'inch' )                                : mpmathify( '7.92' ),
    ( 'long_cubit',                 'inch' )                                : mpmathify( '21' ),
    ( 'long_reed',                  'foot' )                                : mpmathify( '10.5' ),
    ( 'marathon',                   'yard' )                                : mpmathify( '46145' ),
    ( 'meter',                      'angstrom' )                            : mpmathify( '1.0e10' ),
    ( 'meter',                      'french' )                              : mpmathify( '3000' ),
    ( 'meter',                      'kyu' )                                 : mpmathify( '4000' ),
    ( 'meter',                      'micron' )                              : mpmathify( '1.0e6' ),
    ( 'metric_foot',                'meter' )                               : mpmathify( '0.3' ),
    ( 'mezhevaya_versta',           'versta' )                              : mpmathify( '2' ),
    ( 'mile',                       'foot' )                                : mpmathify( '5280' ),
    ( 'nail',                       'inch' )                                : mpmathify( '2.25' ),
    ( 'nautical_mile',              'meter' )                               : mpmathify( '1852' ),
    ( 'parsec',                     'light-year' )                          : mpmathify( '3.261563776971' ),
    ( 'rod',                        'foot' )                                : mpmathify( '16.5' ),
    ( 'potrzebie',                  'farshimmelt_potrzebie' )               : mpmathify( '1.0e5' ),
    ( 'potrzebie',                  'furshlugginer_potrzebie' )             : mpmathify( '1.0e-6' ),
    ( 'potrzebie',                  'meter' )                               : mpmathify( '0.002263348517438173216473' ),  # see Mad #33
    ( 'pyad',                       'inch' )                                : mpmathify( '7' ),
    ( 'pyad',                       'vershok' )                             : mpmathify( '4' ),
    ( 'rack_unit',                  'meter' )                               : mpmathify( '0.0445' ),
    ( 'reed',                       'foot' )                                : mpmathify( '9' ),
    ( 'rope',                       'foot' )                                : mpmathify( '20' ),
    ( 'sazhen',                     'meter' )                               : mpmathify( '2.1336' ),
    ( 'siriometer',                 'astronomical_unit' )                   : mpmathify( '1.0e6' ),
    ( 'skein',                      'foot' )                                : mpmathify( '360' ),
    ( 'smoot',                      'inch' )                                : mpmathify( '67' ),
    ( 'span',                       'inch' )                                : mpmathify( '9' ),
    ( 'stadium',                    'foot' )                                : mpmathify( '606.95' ),
    ( 'survey_foot',                'meter' )                               : fdiv( 1200, 3937 ),
    ( 'versta',                     'meter' )                               : mpmathify( '1066.8' ),
    ( 'yard',                       'foot' )                                : mpmathify( '3' ),

    # luminance

    ( 'footlambert',                'candela/meter^2' )                     : mpmathify( '3.42625909963539052691674596165021859423458362052434022' ), # rpn -a54 meter foot convert sqr value pi /
    ( 'lambert',                    'candela/meter^2' )                     : fdiv( 10000, pi ),
    ( 'nit',                        'apostilb' )                            : pi,
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'skot',                       'bril' )                                : mpmathify( '1.0e4' ),
    ( 'skot',                       'lambert' )                             : mpmathify( '1.0e7' ),
    ( 'stilb',                      'candela/meter^2' )                     : mpmathify( '10000' ),

    # luminous_flux

    ( 'lumen',                      'candela*radian^2' )                    : mpmathify( '1' ),

    # luminous_intensity

    ( 'hefnerkerze',                'candela' )                             : mpmathify( '0.920' ),  # approx.

    # magnetic_field_strength

    ( 'oersted',                    'ampere/meter' )                        : mpmathify( '79.5774715' ),

    # 'magnetic_flux

    ( 'weber',                      'kilogram*meter^2/ampere*second^2' )    : mpmathify( '1' ),
    ( 'weber',                      'maxwell' )                             : mpmathify( '1.0e8' ),
    ( 'weber',                      'unit_pole' )                           : mpmathify( '7957747.154594' ),

    # magnetic_flux_density

    ( 'tesla',                      'gauss' )                               : mpmathify( '10000' ),
    ( 'tesla',                      'kilogram/ampere*second^2' )            : mpmathify( '1' ),

    # mass

    ( 'berkovets',                  'dolya' )                               : mpmathify( '3686400' ),
    ( 'blintz',                     'farshimmelt_blintz' )                  : mpmathify( '1.0e5' ),
    ( 'blintz',                     'furshlugginer_blintz' )                : mpmathify( '1.0e-6' ),
    ( 'blintz',                     'gram' )                                : mpmathify( '36.42538631' ),
    ( 'carat',                      'grain' )                               : fadd( 3, fdiv( 1, 6 ) ),
    ( 'chandrasekhar_limit',        'gram' )                                : mpmathify( '2.765e33' ),
    ( 'dalton',                     'gram' )                                : mpmathify( '1.660539040e-24' ),
    ( 'doppelzentner',              'zentner' )                             : mpmathify( '2' ),
    ( 'fortnight',                  'day' )                                 : mpmathify( '14' ),
    ( 'funt',                       'dolya' )                               : mpmathify( '9216' ),
    ( 'gram',                       'dolya' )                               : mpmathify( '22.50481249152' ),
    ( 'joule*second^2/meter^2',     'gram' )                                : mpmathify( '1000' ),
    ( 'kip',                        'pound' )                               : mpmathify( '1000' ),
    ( 'lot',                        'dolya' )                               : mpmathify( '288' ),
    ( 'month',                      'day' )                                 : mpmathify( '30' ),
    ( 'ounce',                      'gram' )                                : mpmathify( '28.349523125' ),
    ( 'pennyweight',                'gram' )                                : mpmathify( '1.55517384' ),
    ( 'pfund',                      'gram' )                                : mpmathify( '500' ),
    ( 'pood',                       'dolya' )                               : mpmathify( '368640' ),
    ( 'pound',                      'grain' )                               : mpmathify( '7000' ),
    ( 'pound',                      'ounce' )                               : mpmathify( '16' ),
    ( 'pound',                      'sheet' )                               : mpmathify( '700' ),
    ( 'quintal',                    'gram' )                                : mpmathify( '100000' ),
    ( 'slug',                       'pound' )                               : mpmathify( '32.174048556' ),
    ( 'slug',                       'slinch' )                              : mpmathify( '12' ),
    ( 'stone',                      'pound' )                               : mpmathify( '14' ),
    ( 'stone_us',                   'pound' )                               : mpmathify( '12.5' ),
    ( 'ton',                        'pound' )                               : mpmathify( '2000' ),
    ( 'tonne',                      'gram' )                                : mpmathify( '1.0e6' ),
    ( 'tropical_month',             'day' )                                 : mpmathify( '27.321582' ),
    ( 'troy_ounce',                 'gram' )                                : mpmathify( '31.1034768' ),
    ( 'troy_pound',                 'pound' )                               : mpmathify( '12' ),
    ( 'week',                       'day' )                                 : mpmathify( '7' ),
    ( 'wey',                        'pound' )                               : mpmathify( '252' ),
    ( 'zentner',                    'gram' )                                : mpmathify( '50000' ),
    ( 'zolotnik',                   'dolya' )                               : mpmathify( '96' ),

    # power

    ( 'decibel-watt',               'decibel-milliwatt' )                   : mpmathify( '30' ),
    ( 'horsepower',                 'watt' )                                : mpmathify( '745.69987158227022' ),
    ( 'pferdestarke',               'watt' )                                : mpmathify( '735.49875' ),
    ( 'poncelet',                   'watt' )                                : mpmathify( '980.665' ),
    ( 'watt',                       'lusec' )                               : mpmathify( '7500' ),
    ( 'watt',                       'kilogram*meter^2/second^3' )           : mpmathify( '1' ),

    # pressure

    ( 'atmosphere',                 'pascal' )                              : mpmathify( '101325' ),
    ( 'bar',                        'pascal' )                              : mpmathify( '1.0e5' ),
    ( 'mmHg',                       'pascal' )                              : mpmathify( '133.3224' ),        # approx.
    ( 'pascal',                     'barye' )                               : mpmathify( '10' ),
    ( 'pascal',                     'kilogram/meter*second^2' )             : mpmathify( '1' ),
    ( 'pieze',                      'pascal' )                              : mpmathify( '1000' ),
    ( 'psi',                        'pascal' )                              : mpmathify( '6894.75728' ),      # approx.
    ( 'torr',                       'mmHg' )                                : mpmathify( '1' ),

    # radiation_dose

    ( 'banana_equivalent_dose',     'sievert' )                             : mpmathify( '9.8e-8' ),
    ( 'gray',                       'meter^2/second^2' )                    : mpmathify( '1' ),
    ( 'gray',                       'rad' )                                 : mpmathify( '100' ),
    ( 'gray',                       'sievert' )                             : mpmathify( '1' ),
    ( 'sievert',                    'rem' )                                 : mpmathify( '100' ),

    # radiation_exposure

    ( 'coulomb/kilogram',           'roentgen' )                            : mpmathify( '3876' ),
    ( 'roentgen',                   'rad' )                                 : mpmathify( '0.877' ),

    # radiosity

    # solid_angle

    ( 'arcminute^2',                'arcsecond^2' )                         : mpmathify( '3600' ),
    ( 'degree^2',                   'arcminute^2' )                         : mpmathify( '3600' ),
    ( 'octant^2',                   'degree^2' )                            : mpmathify( '2025' ),
    ( 'quadrant^2',                 'degree^2' )                            : mpmathify( '8100' ),
    ( 'quintant^2',                 'degree^2' )                            : mpmathify( '5184' ),
    ( 'sextant^2',                  'degree^2' )                            : mpmathify( '3600' ),
    ( 'sphere',                     'hemisphere' )                          : mpmathify( '2' ),
    ( 'sphere',                     'steradian' )                           : fmul( 4, pi ),
    ( 'steradian',                  'degree^2' )                            : power( fdiv( 180, pi ), 2 ),
    ( 'steradian',                  'grad^2' )                              : power( fdiv( 200, pi ), 2 ),
    ( 'steradian',                  'radian^2' )                            : mpmathify( '1' ),

    # temperature

    ( 'celsius',                    'degree_newton' )                       : fdiv( 33, 100 ),
    ( 'celsius',                    'reaumur' )                             : fdiv( 4, 5 ),
    ( 'kelvin',                     'rankine' )                             : fdiv( 9, 5 ),
    ( 'reaumur',                    'degree_newton' )                       : fdiv( 33, 80 ),

    # time

    ( 'beat',                       'blink' )                               : mpmathify( '100' ),
    ( 'century',                    'microcentury' )                        : mpmathify( '1.0e6' ),
    ( 'century',                    'nanocentury' )                         : mpmathify( '1.0e9' ),
    ( 'century',                    'year' )                                : mpmathify( '100' ),
    ( 'clarke',                     'day' )                                 : mpmathify( '1' ),
    ( 'clarke',                     'wolverton' )                           : mpmathify( '1.0e6' ),
    ( 'cowznofski',                 'mingo' )                               : mpmathify( '10' ),
    ( 'day',                        'beat' )                                : mpmathify( '1000' ),
    ( 'day',                        'hour' )                                : mpmathify( '24' ),
    ( 'decade',                     'year' )                                : mpmathify( '10' ),
    ( 'eon',                        'year' )                                : mpmathify( '1e9' ),
    ( 'fortnight',                  'microfortnight' )                      : mpmathify( '1.0e6' ),
    ( 'gregorian_year',             'second' )                              : mpmathify( '31556952' ),
    ( 'hour',                       'minute' )                              : mpmathify( '60' ),
    ( 'kovac',                      'wolverton' )                           : mpmathify( '10' ),
    ( 'lustrum',                    'year' )                                : mpmathify( '5' ),
    ( 'martin',                     'kovac' )                               : mpmathify( '100' ),
    ( 'mingo',                      'clarke' )                              : mpmathify( '10' ),
    ( 'minute',                     'second' )                              : mpmathify( '60' ),
    ( 'second',                     'jiffy' )                               : mpmathify( '100' ),
    ( 'second',                     'shake' )                               : mpmathify( '1.0e8' ),
    ( 'second',                     'svedberg' )                            : mpmathify( '1.0e13' ),
    ( 'sidereal_day',               'second' )                              : mpmathify( '86164.0905' ),   # https://en.wikipedia.org/wiki/Sidereal_time
    ( 'sidereal_day',               'sidereal_hour' )                       : mpmathify( '24' ),
    ( 'sidereal_hour',              'sidereal_minute' )                     : mpmathify( '60' ),
    ( 'sidereal_minute',            'sidereal_second' )                     : mpmathify( '60' ),
    ( 'wood',                       'martin' )                              : mpmathify( '100' ),
    ( 'year',                       'day' )                                 : mpmathify( '365.25' ),   # Julian year = 365 and 1/4 days

    # velocity

    ( 'mach',                       'meter/second' )                        : mpmathify( '340.2868' ),
    ( 'meter/second',               'bubnoff_unit' )                        : mpmathify( '3.15576e13' ),
    ( 'meter/second',               'kine' )                                : mpmathify( '100' ),
    ( 'meter/second',               'knot' )                                : mpmathify( '1.943844492' ),
    ( 'speed_of_sound',             'meter/second' )                        : mpmathify( '343' ),

    # volume

    # volume - U.S. measures

    ( 'bucket',                     'gallon' )                              : mpmathify( '4' ),
    ( 'cup',                        'dram' )                                : mpmathify( '64' ),
    ( 'cup',                        'fluid_ounce' )                         : mpmathify( '8' ),
    ( 'cup',                        'gill' )                                : mpmathify( '2' ),
    ( 'cup',                        'wineglass' )                           : mpmathify( '4' ),
    ( 'dessertspoon',               'teaspoon' )                            : mpmathify( '2' ),
    ( 'dram',                       'scruple' )                             : mpmathify( '3' ),
    ( 'fluid_ounce',                'dram' )                                : mpmathify( '8' ),
    ( 'fluid_ounce',                'tablespoon' )                          : mpmathify( '2' ),
    ( 'gallon',                     'fifth' )                               : mpmathify( '5' ),
    ( 'gallon',                     'inch^3' )                              : mpmathify( '231' ),
    ( 'gallon',                     'liter' )                               : mpmathify( '3.785411784' ),   # This is exact!
    ( 'gallon',                     'quart' )                               : mpmathify( '4' ),
    ( 'oil_barrel',                 'gallon' )                              : mpmathify( '42' ),
    ( 'quart',                      'cup' )                                 : mpmathify( '4' ),
    ( 'quart',                      'pint' )                                : mpmathify( '2' ),
    ( 'scruple',                    'minim' )                               : mpmathify( '20' ),
    ( 'tablespoon',                 'teaspoon' )                            : mpmathify( '3' ),
    ( 'teaspoon',                   'coffeespoon' )                         : mpmathify( '2' ),
    ( 'teaspoon',                   'dash' )                                : mpmathify( '8' ),
    ( 'teaspoon',                   'pinch' )                               : mpmathify( '16' ),
    ( 'teaspoon',                   'saltspoon' )                           : mpmathify( '4' ),
    ( 'teaspoon',                   'smidgen' )                             : mpmathify( '32' ),

    # volume - wine bottles

    ( 'balthazar',                  'wine_bottle' )                         : mpmathify( '16' ),
    ( 'clavelin',                   'liter' )                               : mpmathify( '0.62' ),
    ( 'goliath',                    'wine_bottle' )                         : mpmathify( '36' ),
    ( 'jeroboam',                   'wine_bottle' )                         : mpmathify( '4' ),  # some French regions use 6
    ( 'magnum',                     'wine_bottle' )                         : mpmathify( '2' ),
    ( 'marie_jeanne',               'wine_bottle' )                         : mpmathify( '3' ),
    ( 'melchior',                   'wine_bottle' )                         : mpmathify( '24' ),
    ( 'melchizedek',                'wine_bottle' )                         : mpmathify( '40' ),
    ( 'methuselah',                 'wine_bottle' )                         : mpmathify( '8' ),
    ( 'mordechai',                  'wine_bottle' )                         : mpmathify( '12' ),
    ( 'nebuchadnezzar',             'wine_bottle' )                         : mpmathify( '20' ),
    ( 'rehoboam',                   'wine_bottle' )                         : mpmathify( '6' ),
    ( 'salmanazar',                 'wine_bottle' )                         : mpmathify( '12' ),
    ( 'solomon',                    'wine_bottle' )                         : mpmathify( '24' ),
    ( 'sovereign',                  'wine_bottle' )                         : mpmathify( '35' ),
    ( 'wine_bottle',                'chopine' )                             : mpmathify( '3' ),
    ( 'wine_bottle',                'demi' )                                : mpmathify( '2' ),
    ( 'wine_bottle',                'jennie' )                              : mpmathify( '1.5' ),
    ( 'wine_bottle',                'liter' )                               : mpmathify( '0.75' ),
    ( 'wine_bottle',                'piccolo' )                             : mpmathify( '4' ),

    # volume - wine

    ( 'tun',                        'butt' )                                : mpmathify( '2' ),
    ( 'tun',                        'gallon' )                              : mpmathify( '252' ),
    ( 'tun',                        'puncheon' )                            : mpmathify( '3' ),
    ( 'tun',                        'rundlet' )                             : mpmathify( '14' ),
    ( 'tun',                        'tierce' )                              : mpmathify( '6' ),
    ( 'tun',                        'wine_barrel' )                         : mpmathify( '8' ),
    ( 'tun',                        'wine_hogshead' )                       : mpmathify( '4' ),

    # volume - beer

    ( 'beer_barrel',                'beer_keg' )                            : mpmathify( '2' ),
    ( 'beer_barrel',                'gallon' )                              : mpmathify( '31' ),
    ( 'beer_keg',                   'pony_keg' )                            : mpmathify( '2' ),
    ( 'growler',                    'fluid_ounce' )                         : mpmathify( '64' ),
    ( 'firkin',                     'gallon' )                              : mpmathify( '9' ),
    ( 'firkin',                     'pin' )                                 : mpmathify( '2' ),
    ( 'kilderkin',                  'firkin' )                              : mpmathify( '2' ),
    ( 'liter',                      'stein' )                               : mpmathify( '2' ),

    # volume - imperial

    ( 'kenning',                    'imperial_peck' )                       : mpmathify( '2' ),
    ( 'imperial_bushel',            'kenning' )                             : mpmathify( '2' ),
    ( 'imperial_cup',               'imperial_gill' )                       : mpmathify( '2' ),
    ( 'imperial_gallon',            'liter' )                               : mpmathify( '4.54609' ),   # This is the exact definition.
    ( 'imperial_gallon',            'pottle' )                              : mpmathify( '2' ),
    ( 'imperial_peck',              'imperial_quart' )                      : mpmathify( '8' ),
    ( 'imperial_pint',              'imperial_cup' )                        : mpmathify( '2' ),
    ( 'imperial_quart',             'imperial_pint' )                       : mpmathify( '2' ),
    ( 'imperial_tun',               'imperial_barrel' )                     : mpmathify( '8' ),
    ( 'imperial_tun',               'imperial_butt' )                       : mpmathify( '2' ),
    ( 'imperial_tun',               'imperial_gallon' )                     : mpmathify( '210' ),
    ( 'imperial_tun',               'imperial_hogshead' )                   : mpmathify( '4' ),
    ( 'imperial_tun',               'imperial_puncheon' )                   : mpmathify( '3' ),
    ( 'imperial_tun',               'imperial_rundlet' )                    : mpmathify( '14' ),
    ( 'imperial_tun',               'imperial_tierce' )                     : mpmathify( '6' ),
    ( 'pottle',                     'imperial_quart' )                      : mpmathify( '2' ),

    # volume - liquor

    ( 'jigger',                     'fluid_ounce' )                         : mpmathify( '1.5' ),
    ( 'snit',                       'jigger' )                              : mpmathify( '2' ),
    ( 'pony',                       'fluid_ounce' )                         : mpmathify( '1' ),

    # volume - Potrzebie

    ( 'liter',                      'ngogn' )                               : mpmathify( '86.2473382128925178993463552296954874904688556293757985' ),
    ( 'ngogn',                      'farshimmelt_ngogn' )                   : mpmathify( '1.0e5' ),
    ( 'ngogn',                      'furshlugginer_ngogn' )                 : mpmathify( '1.0e-6' ),

    # volume - dry measure

    ( 'bushel',                     'dry_gallon' )                          : mpmathify( '8' ),
    ( 'bushel',                     'liter' )                               : mpmathify( '35.23907016688' ), # exact!
    ( 'bushel',                     'peck' )                                : mpmathify( '4' ),
    ( 'dry_barrel',                 'inch^3' )                              : mpmathify( '7056' ),
    ( 'dry_gallon',                 'dry_quart' )                           : mpmathify( '4' ),
    ( 'dry_hogshead',               'dry_barrel' )                          : mpmathify( '2' ),
    ( 'dry_quart',                  'dry_pint' )                            : mpmathify( '2' ),
    ( 'dry_tun',                    'dry_hogshead' )                        : mpmathify( '4' ),
    ( 'peck',                       'dry_gallon' )                          : mpmathify( '2' ),

    # volume - other

    ( 'cord',                       'foot^3' )                              : mpmathify( '128' ),
    ( 'grand_canyon',               'meter^3' )                             : mpmathify( '4.17e12' ),
    ( 'hoppus_ton',                 'hoppus_foot' )                         : mpmathify( '50' ),
    ( 'hoppus_ton',                 'meter^3' )                             : mpmathify( '1.802706436' ),
    ( 'meter^3',                    'foot^3' )                              : mpmathify( '35.3146667214885902504380103540026269320546806739574396' ), # This is needed for 'cord'
    ( 'meter^3',                    'liter' )                               : mpmathify( '1000' ),
    ( 'portuguese_almude',          'liter' )                               : mpmathify( '16.7' ),
    ( 'spanish_almude',             'liter' )                               : mpmathify( '4.625' ),
    ( 'stere',                      'liter' )                               : mpmathify( '1000' ),    # metric, but not SI
    ( 'sydharb',                    'liter' )                               : mpmathify( '5.62e11' ),
}

