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
        RPNUnitInfo( '_null_type', '_null_unit', '_null_unit', '',
                     [ ], [ ],
                     '''
This unit type is used internally by rpnChilada.
''' ),

    # acceleration
    'celo' :
        RPNUnitInfo( 'acceleration', 'celo', 'celos', '',
                     [ ], [ 'CGS' ],
                     '''
The celo is a unit of acceleration equal to the acceleration of a body whose
velocity changes uniformly by 1 foot (0.3048 meter) per second in 1 second."

Ref:  http://automationwiki.com/index.php/Engineering_Units_-_Celo
''' ),

    'galileo' :
        RPNUnitInfo( 'acceleration', 'galileo', 'galileos', '',
                     [ 'gal', 'gals' ], [ 'CGS' ],
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
        RPNUnitInfo( 'acceleration', 'leo', 'leos', '',
                     [ ], [ 'CGS' ],
                     '''
The leo is a unit of acceleration equal to 10 meters/second^2, which is 1000
times the acceleration represented by the galileo, and is very close to the
acceleration due to gravity on the surface of the Earth.

Ref:  http://automationwiki.com/index.php/Engineering_Units_-_Leo
''' ),

    'meter/second^2' :
        RPNUnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),


    # amount of substance
    'mole' :
        RPNUnitInfo( 'amount_of_substance', 'mole', 'mole', 'mol',
                     [ 'einstein', 'einsteins' ], [ 'SI' ],
                     '''
''' ),

    # angle
    'arcminute' :
        RPNUnitInfo( 'angle', 'arcminute', 'arcminutes', '',
                     [ 'arcmin', 'arcmins' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'arcsecond' :
        RPNUnitInfo( 'angle', 'arcsecond', 'arcseconds', '',
                     [ 'arcsec', 'arcsecs' ], [ 'astronomy', 'mathematics' ],
                     '''
''' ),

    'centrad' :
        RPNUnitInfo( 'angle', 'centrad', 'centrads', '',
                     [ ], [ 'mathematics', 'science' ],
                     '''
''' ),

    'circle' :
        RPNUnitInfo( 'angle', 'circle', 'circles', '',
                     [ ], [ 'mathematics' ],
                     '''
The whole circle, all 360 degrees.
''' ),

    'degree' :
        RPNUnitInfo( 'angle', 'degree', 'degrees', 'deg',
                     [ ], [ 'astronomy', 'mathematics', 'traditional' ],
                     '''
The traditional degree, 1/360th of a circle.
''' ),

    'furman' :
        RPNUnitInfo( 'angle', 'furman', 'furmans', '',
                     [ ], [ 'non-standard' ],
                     '''
From https://en.wikipedia.org/wiki/List_of_unusual_units_of_measurement#Furman:

The Furman is a unit of angular measure equal to 1/65,536 of a circle, or just
under 20 arcseconds.  It is named for Alan T. Furman, the American
mathematician who adapted the CORDIC algorithm for 16-bit fixed-point
arithmetic sometime around 1980.
''' ),

    'grad' :
        RPNUnitInfo( 'angle', 'grad', 'grads', '',
                     [ 'gon', 'gons' ], [ 'mathematics' ],
                     '''
''' ),

    'octant' :
        RPNUnitInfo( 'angle', 'octant', 'octants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'pointangle' :
        RPNUnitInfo( 'angle', 'pointangle', 'pointangles', '',
                     [ ], [ 'navigation' ],
                     '''
''' ),

    'quadrant' :
        RPNUnitInfo( 'angle', 'quadrant', 'quadrants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'quintant' :
        RPNUnitInfo( 'angle', 'quintant', 'quintants', '',
                     [ ], [ 'mathematics' ],
                     '''
''' ),

    'radian' :
        RPNUnitInfo( 'angle', 'radian', 'radians', '',
                     [ ], [ 'mathematics', 'SI' ],
                     '''
''' ),

    'sextant' :
        RPNUnitInfo( 'angle', 'sextant', 'sextants', '',
                     [ 'flat', 'flats' ], [ 'mathematics' ],
                     '''
''' ),

    'streck' :
        RPNUnitInfo( 'angle', 'streck', 'strecks', '',
                     [ ], [ 'Sweden' ],
                     '''
''' ),

    # area
    'acre' :
        RPNUnitInfo( 'area', 'acre', 'acres', 'ac',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'are' :
        RPNUnitInfo( 'area', 'are', 'ares', 'a',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'barn' :
        RPNUnitInfo( 'area', 'barn', 'barns', '',
                     [ 'bethe', 'bethes', 'oppenheimer', 'oppenheimers' ], [ 'science' ],
                     '''
''' ),

    'bovate' :
        RPNUnitInfo( 'area', 'bovate', 'bovates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'carucate' :
        RPNUnitInfo( 'area', 'carucate', 'carucates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'circular_inch' :
        RPNUnitInfo( 'area', 'circular_inch', 'circular_inch', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'circular_mil' :
        RPNUnitInfo( 'area', 'circular_mil', 'circular_mils', 'cmil',
                     [ ], [ 'imperial' ],
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
        RPNUnitInfo( 'area', 'foot^2', 'foot^2', '',
                     [ 'sqft', 'sq_ft', 'square_ft', 'square_foot', 'square_feet', 'sq_foot', 'sq_feet', 'sqfoot', 'sqfeet' ], [ 'imperial' ],
                     '''
''' ),

    'homestead' :
        RPNUnitInfo( 'area', 'homestead', 'homesteads', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'imperial_square' :
        RPNUnitInfo( 'area', 'imperial_sqaure', 'imperial_squares', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'meter^2' :
        RPNUnitInfo( 'area', 'meter^2', 'meter^2', '',
                     [ 'sqm', 'sq_m', 'square_m', 'square_meter', 'square_meters', 'sq_meter', 'sq_meters', 'sqmeter', 'sqmeters' ], [ 'SI' ],
                     '''
''' ),

    'morgen' :
        RPNUnitInfo( 'area', 'morgen', 'morgens', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'nanoacre' :
        RPNUnitInfo( 'area', 'nanoacre', 'nanoacres', 'nac',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'outhouse' :
        RPNUnitInfo( 'area', 'outhouse', 'outhouse', '',
                     [ ], [ 'science', 'humorous' ],
                     '''
''' ),

    'rood' :
        RPNUnitInfo( 'area', 'rood', 'roods', '',
                     [ 'farthingdale' ], [ 'imperial' ],
                     '''
''' ),

    'section' :
        RPNUnitInfo( 'area', 'section', 'sections', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'shed' :
        RPNUnitInfo( 'area', 'shed', 'sheds', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'township' :
        RPNUnitInfo( 'area', 'township', 'townships', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'virgate' :
        RPNUnitInfo( 'area', 'virgate', 'virgates', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    # capacitance
    'abfarad' :
        RPNUnitInfo( 'capacitance', 'abfarad', 'abfarads', 'abF',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'ampere^2*second^4/kilogram*meter^2' :
        RPNUnitInfo( 'capacitance', 'ampere^2*second^4/kilogram*meter^2', 'ampere^2*second^4/kilogram*meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'farad' :
        RPNUnitInfo( 'capacitance', 'farad', 'farads', 'F',
                     [ ], [ 'SI' ],
                     '''
The SI unit for capacitance.
''' ),

    'jar' :
        RPNUnitInfo( 'capacitance', 'jar', 'jars', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'statfarad' :
        RPNUnitInfo( 'capacitance', 'statfarad', 'statfarads', 'statF',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # charge
    'abcoulomb' :
        RPNUnitInfo( 'charge', 'abcoulomb', 'abcoulombs', 'abC',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'coulomb' :
        RPNUnitInfo( 'charge', 'coulomb', 'coulombs', 'C',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'ampere*second' :
        RPNUnitInfo( 'charge', 'ampere*second', 'ampere*seconds', 'As',
                     [ 'second*ampere', 'second*amperes', 'ampere-second', 'ampere-seconds', 'amp-second', 'amp-seconds' ], [ 'SI' ],
                     '''
''' ),

    'franklin' :
        RPNUnitInfo( 'charge', 'franklin', 'franklins', 'Fr',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'faraday' :
        RPNUnitInfo( 'charge', 'faraday', 'faradays', 'Fd',
                     [ ], [ 'natural' ],   # electron_charge * Avogradro's number!
                     '''
''' ),

    'statcoulomb' :
        RPNUnitInfo( 'charge', 'statcoulomb', 'statcoulombs', 'statC',
                     [ 'esu_charge' ], [ 'CGS' ],
                     '''
''' ),

    # catalysis
    'enzyme_unit' :
        RPNUnitInfo( 'catalysis', 'enzyme_unit', 'enzyme_units', '',    # 'U' is the symbol, but that is already used for Uranium
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
        RPNUnitInfo( 'catalysis', 'katal', 'katal', 'kat',
                     [ ], [ 'SI' ],
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
        RPNUnitInfo( 'catalysis', 'mole/second', 'mole/second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),


# constant - Constant is a special type that is immediately converted to a numerical value when used.
#            It's not intended to be used as a unit, per se.  Also, these units are in order of their
#            value instead of alphabetical order like all the others
    'decillionth' :
        RPNUnitInfo( 'constant', 'decillionth', 'decillionths', '',
                     [ ], [ 'constant' ],
                     '''
One decillionth:  10e-33 or 1/1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'nonillionth' :
        RPNUnitInfo( 'constant', 'nonillionth', 'nonillionths', '',
                     [ ], [ 'constant' ],
                     '''
One nonillionth:  10e-30 or 1/1,000,000,000,000,000,000,000,000,000,000
''' ),

    'octillionth' :
        RPNUnitInfo( 'constant', 'octillionth', 'octillionths', '',
                     [ ], [ 'constant' ],
                     '''
One octillionth:  10e-27 or 1/1,000,000,000,000,000,000,000,000,000
''' ),

    # 'y' can't be used here since it's an operator
    'septillionth' :
        RPNUnitInfo( 'constant', 'septillionth', 'septillionths', '',
                     [ 'yocto' ], [ 'constant' ],
                     '''
One septillionth:  10e-24 or 1/1,000,000,000,000,000,000,000,000
''' ),

    # 'z' can't be used here since it's an operator
    'sextillionth' :
        RPNUnitInfo( 'constant', 'sextillionth', 'sextillionths', '',
                     [ 'zepto' ], [ 'constant' ],
                     '''
One sextillionth:  10e-21 or 1/1,000,000,000,000,000,000,000
''' ),

    # 'a' can't be used here since it's used for 'are'
    'quintillionth' :
        RPNUnitInfo( 'constant', 'quintillionth', 'quintillionths', '',
                     [ 'atto' ], [ 'constant' ],
                     '''
One quintillionth:  10e-18 or 1/1,000,000,000,000,000,000
''' ),

    'quadrillionth' :
        RPNUnitInfo( 'constant', 'quadrillionth', 'quadrillionths', 'f',
                     [ 'femto' ], [ 'constant' ],
                     '''
One quadrillionth:  10e-15 or 1/1,000,000,000,000,000
''' ),

    'trillionth' :
        RPNUnitInfo( 'constant', 'trillionth', 'trillionths', 'p',
                     [ 'pico' ], [ 'constant' ],
                     '''
One trillionth:  10e-12 or 1/1,000,000,000,000
''' ),

    'billionth' :
        RPNUnitInfo( 'constant', 'billionth', 'billionths', 'n',
                     [ 'nano' ], [ 'constant' ],
                     '''
One billionth:  10e-9 or 1/1,000,000,000
''' ),

    'millionth' :
        RPNUnitInfo( 'constant', 'millionth', 'millionths', 'u',
                     [ 'micro' ], [ 'constant' ],
                     '''
One millionth:  10e-6 or 1/1,000,000
''' ),

    # 'm' can't be used here since it's used for 'meter'
    'thousandth' :
        RPNUnitInfo( 'constant', 'thousandth', 'thousandths', '',
                     [ 'milli' ], [ 'constant' ],
                     '''
One thousandth:  10e-3 or 1/1,000
''' ),

    'percent' :
        RPNUnitInfo( 'constant', 'percent', 'percent', '%',
                     [ 'hundredth', 'centi' ], [ 'constant' ],
                     '''
One hundredth:  10e-2 or 1/100
''' ),

    'tenth' :
        RPNUnitInfo( 'constant', 'tenth', 'tenths', '',
                     [ 'deci', 'tithe' ], [ 'constant' ],
                     '''
One tenth:  10e-1 or 1/10
''' ),

    'quarter' :
        RPNUnitInfo( 'constant', 'quarter', 'quarters', '',
                     [ 'fourth', 'fourths' ], [ 'constant' ],
                     '''
One quarter:  1/4 or 0.25
''' ),

    'third' :
        RPNUnitInfo( 'constant', 'third', 'thirds', '',
                     [ ], [ 'constant' ],
                     '''
One third:  1/3 or 0.333333...
''' ),

    'half' :
        RPNUnitInfo( 'constant', 'half', 'halves', '',
                     [ ], [ 'constant' ],
                     '''
One half:  1/2 or 0.5
''' ),

    'unity' :
        RPNUnitInfo( 'constant', 'x unity', 'x unity', '',
                     [ 'one', 'ones' ], [ 'constant' ],
                     '''
Unity, one, 1
''' ),

    'two' :
        RPNUnitInfo( 'constant', 'two', 'twos', '',
                     [ 'pair', 'pairs' ], [ 'constant' ],
                     '''
two, 2
''' ),

    'three' :
        RPNUnitInfo( 'constant', 'three', 'threes', '',
                     [ ], [ 'constant' ],
                     '''
three, 3
''' ),

    'four' :
        RPNUnitInfo( 'constant', 'four', 'fours', '',
                     [ ], [ 'constant' ],
                     '''
four, 4
''' ),

    'five' :
        RPNUnitInfo( 'constant', 'five', 'fives', '',
                     [ ], [ 'constant' ],
                     '''
five, 5
''' ),

    'six' :
        RPNUnitInfo( 'constant', 'six', 'sixes', '',
                     [ ], [ 'constant' ],
                     '''
six, 6
''' ),

    'seven' :
        RPNUnitInfo( 'constant', 'seven', 'sevens', '',
                     [ ], [ 'constant' ],
                     '''
seven, 7
''' ),

    'eight' :
        RPNUnitInfo( 'constant', 'eight', 'eights', '',
                     [ ], [ 'constant' ],
                     '''
eight, 8
''' ),

    'nine' :
        RPNUnitInfo( 'constant', 'nine', 'nines', '',
                     [ ], [ 'constant' ],
                     '''
nine, 9
''' ),

    'ten' :
        RPNUnitInfo( 'constant', 'ten', 'tens', '',
                     [ 'deca', 'deka', 'dicker', 'dickers' ], [ 'constant' ],
                     '''
Ten:  10e1, or 10
''' ),

    'eleven' :
        RPNUnitInfo( 'constant', 'eleven', 'elevens', '',
                     [ ], [ 'constant' ],
                     '''
eleven, 11
''' ),

    'dozen' :
        RPNUnitInfo( 'constant', 'dozen', 'dozen', '',
                     [ 'twelve', 'twelves' ], [ 'constant' ],
                     '''
A dozen is 12.
''' ),

    'bakers_dozen' :
        RPNUnitInfo( 'constant', 'bakers_dozen', 'bakers_dozens', '',
                     [ 'thirteen', 'thirteens' ], [ 'constant' ],
                     '''
A baker's dozen is 13.
''' ),

    'fourteen' :
        RPNUnitInfo( 'constant', 'fourteen', 'fourteens', '',
                     [ ], [ 'constant' ],
                     '''
fourteen, 14
''' ),

    'fifteen' :
        RPNUnitInfo( 'constant', 'fifteen', 'fifteens', '',
                     [ ], [ 'constant' ],
                     '''
fifteen, 15
''' ),

    'sixteen' :
        RPNUnitInfo( 'constant', 'sixteen', 'sixteens', '',
                     [ ], [ 'constant' ],
                     '''
sixteen, 16
''' ),

    'seventeen' :
        RPNUnitInfo( 'constant', 'seventeen', 'seventeens', '',
                     [ ], [ 'constant' ],
                     '''
seventeen, 17
''' ),

    'eighteen' :
        RPNUnitInfo( 'constant', 'eighteen', 'eighteens', '',
                     [ ], [ 'constant' ],
                     '''
eighteen, 18
''' ),

    'nineteen' :
        RPNUnitInfo( 'constant', 'nineteen', 'nineteens', '',
                     [ ], [ 'constant' ],
                     '''
nineteen, 19
''' ),

    'score' :
        RPNUnitInfo( 'constant', 'score', 'score', '',
                     [ 'twenty', 'twenties' ], [ 'constant' ],
                     '''
A score is 20.
''' ),

    'thirty' :
        RPNUnitInfo( 'constant', 'thirty', 'thirties', '',
                     [ ], [ 'constant' ],
                     '''
thirty, 30
''' ),

    'flock' :
        RPNUnitInfo( 'constant', 'flock', 'flocks', '',
                     [ 'forty', 'forties' ], [ 'constant', 'obsolete' ],
                     '''
A flock is an archaic name for 40.
''' ),

    'fifty' :
        RPNUnitInfo( 'constant', 'fifty', 'fifties', '',
                     [ ], [ 'constant' ],
                     '''
fifty, 50
''' ),

    'shock' :
        RPNUnitInfo( 'constant', 'shock', 'shocks', '',
                     [ 'shook', 'shooks', 'sixty', 'sixties' ], [ 'constant', 'obsolete' ],
                     '''
A shock is an archaic name for 60.
''' ),

    'seventy' :
        RPNUnitInfo( 'constant', 'seventy', 'seventies', '',
                     [ ], [ 'constant' ],
                     '''
seventy, 70
''' ),

    'eighty' :
        RPNUnitInfo( 'constant', 'eighty', 'eighties', '',
                     [ ], [ 'constant' ],
                     '''
eighty, 80
''' ),

    'ninety' :
        RPNUnitInfo( 'constant', 'ninety', 'nineties', '',
                     [ ], [ 'constant' ],
                     '''
ninety, 90
''' ),

    'hundred' :
        RPNUnitInfo( 'constant', 'hundred', 'hundred', '',
                     [ 'hecto', 'toncount', 'toncounts' ], [ 'constant' ],
                     '''
One hundred:  10e2, or 100
''' ),

    'long_hundred' :
        RPNUnitInfo( 'constant', 'long_hundred', 'long_hundreds', '',
                     [ ], [ 'constant', 'obsolete' ],
                     '''
\'long\' hundred is an archaic term for 120.
''' ),

    'gross' :
        RPNUnitInfo( 'constant', 'gross', 'gross', '',
                     [ ], [ 'constant' ],
                     '''
A gross is a dozen dozen, or 144.
''' ),

    'thousand' :
        RPNUnitInfo( 'constant', 'thousand', 'thousand', 'k',
                     [ 'kilo', 'chiliad' ], [ 'constant' ],
                     '''
One thousand:  10e3, or 1,000
''' ),

    'great_gross' :
        RPNUnitInfo( 'constant', 'great_gross', 'great_gross', '',
                     [ ], [ 'constant' ],
                     '''
A great gross is a dozen gross, or 1728.
''' ),

    'million' :
        RPNUnitInfo( 'constant', 'million', 'million', 'M',
                     [ 'mega' ], [ 'constant' ],
                     '''
One million:  10e6 or 1,000,000
''' ),

    # 'G' can't be used here since it's used for 'standard gravity'
    'billion' :
        RPNUnitInfo( 'constant', 'billion', 'billion', '',
                     [ 'giga', 'gigas', 'milliard', 'milliards' ], [ 'constant' ],
                     '''
One billion:  10e9 or 1,000,000,000
''' ),

    # 'T' can't be used here since it's used for 'tesla'
    'trillion' :
        RPNUnitInfo( 'constant', 'trillion', 'trillion', '',
                     [ 'tera' ], [ 'constant' ],
                     '''
One trillion:  10e12 or 1,000,000,000,000
''' ),

    # 'P' can't be used here since it's used for 'Phosphorus'
    'quadrillion' :
        RPNUnitInfo( 'constant', 'quadrillion', 'quadrillion', '',
                     [ 'peta', 'petas', 'billiard', 'billiards' ], [ 'constant' ],
                     '''
One quadrillion:  10e15 or 1,000,000,000,000,000
''' ),

    'quintillion' :
        RPNUnitInfo( 'constant', 'quintillion', 'quintillion', 'E',
                     [ 'exa' ], [ 'constant' ],
                     '''
One quintillion:  10e18 or 1,000,000,000,000,000,000
''' ),

    'sextillion' :
        RPNUnitInfo( 'constant', 'sextillion', 'sextillion', 'Z',
                     [ 'zetta', 'zettas', 'trilliard', 'trilliards' ], [ 'constant' ],
                     '''
One sextillion:  10e21 or 1,000,000,000,000,000,000,000
''' ),

    # 'Y' can't be used here since it's used for 'Yttrium'
    'septillion' :
        RPNUnitInfo( 'constant', 'septillion', 'septillion', '',
                     [ 'yotta' ], [ 'constant' ],
                     '''
One septillion:  10e24 or 1,000,000,000,000,000,000,000,000
''' ),

    'octillion' :
        RPNUnitInfo( 'constant', 'octillion', 'octillion', '',
                     [ ], [ 'constant' ],
                     '''
One octillion:  10e27 or 1,000,000,000,000,000,000,000,000,000
''' ),

    'nonillion' :
        RPNUnitInfo( 'constant', 'nonillion', 'nonillion', '',
                     [ ], [ 'constant' ],
                     '''
One nonillion:  10e30 or 1,000,000,000,000,000,000,000,000,000,000
''' ),

    'decillion' :
        RPNUnitInfo( 'constant', 'decillion', 'decillion', '',
                     [ ], [ 'constant' ],
                     '''
One decillion:  10e33 or 1,000,000,000,000,000,000,000,000,000,000,000
''' ),

    'undecillion' :
        RPNUnitInfo( 'constant', 'undecillion', 'undecillion', '',
                     [ ], [ 'constant' ],
                     '''
One undecillion:  10e36
''' ),

    'duodecillion' :
        RPNUnitInfo( 'constant', 'duodecillion', 'duodecillion', '',
                     [ ], [ 'constant' ],
                     '''
One duodecillion:  10e39
''' ),

    'tredecillion' :
        RPNUnitInfo( 'constant', 'tredecillion', 'tredecillion', '',
                     [ ], [ 'constant' ],
                     '''
One tredecillion:  10e42
''' ),

    'quattuordecillion' :
        RPNUnitInfo( 'constant', 'quattuordecillion', 'quattuordecillion', '',
                     [ ], [ 'constant' ],
                     '''
One quattuordecillion:  10e45
''' ),

    'quindecillion' :
        RPNUnitInfo( 'constant', 'quindecillion', 'quindecillion', '',
                     [ 'quinquadecillion' ], [ 'constant' ],
                     '''
One quindecillion:  10e48
''' ),

    'sexdecillion' :
        RPNUnitInfo( 'constant', 'sexdecillion', 'sexdecillion', '',
                     [ ], [ 'constant' ],
                     '''
One sexdecillion:  10e51
''' ),

    'septendecillion' :
        RPNUnitInfo( 'constant', 'septemdecillion', 'septemdecillion', '',
                     [ ], [ 'constant' ],
                     '''
One septendecillion:  10e54
''' ),

    'octodecillion' :
        RPNUnitInfo( 'constant', 'octodecillion', 'octodecillion', '',
                     [ ], [ 'constant' ],
                     '''
One octodecillion:  10e57
''' ),

    'novemdecillion' :
        RPNUnitInfo( 'constant', 'novemdecillion', 'novemdecillion', '',
                     [ 'novendecillion' ], [ 'constant' ],
                     '''
One novemdecillion:  10e60
''' ),

    'vigintillion' :
        RPNUnitInfo( 'constant', 'vigintillion', 'vigintillion', '',
                     [ ], [ 'constant' ],
                     '''
One vigintdecillion:  10e63
''' ),

    'googol' :
        RPNUnitInfo( 'constant', 'googol', 'googols', '',
                     [ ], [ 'constant' ],
                     '''
One googol:  10e100 or ten duotrigintillion, famously named in 1920 by
9-year-old Milton Sirotta.
''' ),

    'centillion' :
        RPNUnitInfo( 'constant', 'centillion', 'centillion', '',
                     [ ], [ 'constant' ],
                     '''
One centillion:  10e303
''' ),

    # current
    'abampere' :
        RPNUnitInfo( 'current', 'abampere', 'abamperes', 'abA',
                     [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ],
                     '''
''' ),

    'ampere' :
        RPNUnitInfo( 'current', 'ampere', 'amperes', 'A',
                     [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ],
                     '''
''' ),

    'statampere' :
        RPNUnitInfo( 'current', 'statampere', 'statamperes', 'statA',
                     [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ],
                     '''
''' ),

    # data_rate
    'bit/second' :
        RPNUnitInfo( 'data_rate', 'bit/second', 'bits/second', 'bps',
                     [ 'bips' ], [ 'computing' ],
                     '''
''' ),

    'byte/second' :
        RPNUnitInfo( 'data_rate', 'byte/second', 'bytes/second', 'Bps',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc1' :
        RPNUnitInfo( 'data_rate', 'oc1', 'x_oc1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc3' :
        RPNUnitInfo( 'data_rate', 'oc3', 'x_oc3', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc12' :
        RPNUnitInfo( 'data_rate', 'oc12', 'x_oc12', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc24' :
        RPNUnitInfo( 'data_rate', 'oc24', 'x_oc24', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc48' :
        RPNUnitInfo( 'data_rate', 'oc48', 'x_oc24', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc192' :
        RPNUnitInfo( 'data_rate', 'oc192', 'x_oc192', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'oc768' :
        RPNUnitInfo( 'data_rate', 'oc768', 'x_oc768', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb1' :
        RPNUnitInfo( 'data_rate', 'usb1', 'x_usb1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb2' :
        RPNUnitInfo( 'data_rate', 'usb2', 'x_usb2', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.0' :
        RPNUnitInfo( 'data_rate', 'usb3.0', 'x_usb3.0', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'usb3.1' :
        RPNUnitInfo( 'data_rate', 'usb3.1', 'x_usb3.1', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    # density
    'kilogram/liter' :
        RPNUnitInfo( 'density', 'kilogram/liter', 'kilograms/liter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram/meter^3' :
        RPNUnitInfo( 'density', 'kilogram/meter^3', 'kilograms/meter^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # dynamic_viscosity
    'kilogram/meter*second' :
        RPNUnitInfo( 'dynamic_viscosity', 'kilogram/meter*second', 'kilogram/meter*second', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pascal*second' :
        RPNUnitInfo( 'dynamic_viscosity', 'pascal*second', 'pascal*seconds', 'Pas',
                     [ 'poiseuille', 'poiseuilles', 'pascal-second', 'pascal-seconds' ], [ 'SI' ],
                     '''
''' ),

    'poise' :
        RPNUnitInfo( 'dynamic_viscosity', 'poise', 'poise', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'reynolds' :
        RPNUnitInfo( 'dynamic_viscosity', 'reynolds', 'reynolds', '',
                     [ 'reyn', 'reyns' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_conductance
    'abmho' :
        RPNUnitInfo( 'electrical_conductance', 'abmho', 'abmhos', '',
                     [ 'absiemens' ], [ 'CGS' ],
                     '''
''' ),

    'conductance_quantum' :
        RPNUnitInfo( 'electrical_conductance', 'conductance_quantum', 'conductance_quanta', 'G0',
                     [ ], [ 'SI' ],
                     '''
The conductance quantum appears when measuring the conductance of a quantum
point contact, and, more generally, is a key component of Landauer formula
which relates the electrical conductance of a quantum conductor to its quantum
properties.  It is twice the reciprocal of the von Klitzing constant (2/RK).

https://en.wikipedia.org/wiki/Conductance_quantum
''' ),

    'ampere^2*second^3/kilogram*meter^2':
        RPNUnitInfo( 'electrical_conductance', 'ampere^2*second^3/kilogram*meter^2', 'ampere^2*second^3/kilogram*meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'siemens' :
        RPNUnitInfo( 'electrical_conductance', 'siemens', 'siemens', 'S',
                     [ 'mho', 'mhos' ], [ 'SI' ],
                     '''
''' ),

    'statmho' :
        RPNUnitInfo( 'electrical_conductance', 'statmho', 'statmhos', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'statsiemens' :
        RPNUnitInfo( 'electrical_conductance', 'statsiemens', 'statsiemens', 'statS',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # electric_potential
    'abvolt' :
        RPNUnitInfo( 'electric_potential', 'abvolt', 'abvolts', 'abV',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'decibel-volt' :
        RPNUnitInfo( 'electric_potential', 'decibel-volt', 'decibel-volt', 'dBV',
                     [ ], [ 'engineering' ],
                     '''
''' ),

    'kilogram*meter^2/ampere*second^3' :
        RPNUnitInfo( 'electric_potential', 'kilogram*meter^2/ampere*second^3', 'kilogram*meter^2/ampere*second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'volt' :
        RPNUnitInfo( 'electric_potential', 'volt', 'volts', 'V',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statvolt' :
        RPNUnitInfo( 'electric_potential', 'statvolt', 'statvolts', 'statV',
                     [ 'esu_potential' ], [ 'CGS' ],
                     '''
''' ),

    # electrical_resistance
    '1/siemens' :
        RPNUnitInfo( 'electrical_resistance', '1/siemens', '1/siemens', '',
                     [ '1/mho' ], [ 'SI' ],
                     '''
''' ),

    'abohm' :
        RPNUnitInfo( 'electrical_resistance', 'abohm', 'abohms', 'o',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'german_mile' :
        RPNUnitInfo( 'electrical_resistance', 'german_mile', 'german_miles', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'jacobi' :
        RPNUnitInfo( 'electrical_resistance', 'jacobi', 'jacobis', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^3' :
        RPNUnitInfo( 'electrical_resistance', 'kilogram*meter^2/ampere^2*second^3', 'kilogram*meter^2/ampere^2*second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'matthiessen' :
        RPNUnitInfo( 'electrical_resistance', 'matthiessen', 'matthiessens', '',
                     [ ], [ 'obsolete' ],   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),

    'ohm' :
        RPNUnitInfo( 'electrical_resistance', 'ohm', 'ohms', 'O',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'statohm' :
        RPNUnitInfo( 'electrical_resistance', 'statohm', 'statohms', 'statO',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'varley' :
        RPNUnitInfo( 'electrical_resistance', 'varley', 'varleys', '',
                     [ ], [ 'obsolete' ],  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C
                     '''
''' ),


    # energy
    'btu' :
        RPNUnitInfo( 'energy', 'BTU', 'BTUs', '', [ 'btus' ],
                     [ 'England', 'US' ],
                     '''
''' ),

    'calorie' :
        RPNUnitInfo( 'energy', 'calorie', 'calories', '', [ ], [ 'CGS' ],
                     '''
''' ),

    'electron-volt' :
        RPNUnitInfo( 'energy', 'electron-volt', 'electron-volts', 'eV',
                     [ 'electronvolt', 'electronvolts' ], [ 'science' ],
                     '''
''' ),

    'erg' :
        RPNUnitInfo( 'energy', 'erg', 'ergs', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'foe' :
        RPNUnitInfo( 'energy', 'foe', 'foes', '',
                     [ 'bethe', 'bethes' ], [ 'astrophysics' ],
                     '''
A foe is a unit of energy equal to 10^44 joules or 10^51 ergs, used to measure
the large amount of energy released by a supernova.  The word is an acronym
derived from the phrase [ten to the power of] fifty-one ergs.  It was coined
by Gerald Brown of Stony Brook University in his work with Hans Bethe, because
"it came up often enough in our work".
''' ),

    'gram-equivalent' :
        RPNUnitInfo( 'energy', 'gram-equivalent', 'grams-equivalent', 'gE',
                     [ 'gram-energy', 'grams-energy', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ],
                     '''
''' ),

    'hartree' :
        RPNUnitInfo( 'energy', 'hartree', 'hartrees', 'Eh',
                     [ ], [ 'science' ],
                     '''
''' ),

    'joule' :
        RPNUnitInfo( 'energy', 'joule', 'joules', 'J',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kayser' :
        RPNUnitInfo( 'energy', 'kayser', 'kaysers', '',
                     [ ], [ 'science', 'CGS' ],
                     '''
Kayser is a unit of energy used in atomic and molecular physics.  Since the
frequency of a photon is proportional to the energy it carries, the kayser is
also equivalent to an energy of 123.984 microelectronvolt.

Ref:  https://www.ibiblio.org/units/dictK.html
''' ),

    'kilogram*meter^2/second^2' :
        RPNUnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pound_of_TNT' :
        RPNUnitInfo( 'energy', 'pound_of_TNT', 'pounds_of_TNT', 'pTNT',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'quad' :
        RPNUnitInfo( 'energy', 'quad', 'quads', '',
                     [ ], [ 'US' ],
                     '''
A quad is a unit of energy equal to 10^15 (a short-scale quadrillion) BTU, or
1.055e18 joules (1.055 exajoules or EJ) in SI units.  The unit is used by
the U.S. Department of Energy in discussing world and national energy budgets.
The global primary energy production in 2004 was 446 quad, equivalent to 471 EJ.

(https://en.wikipedia.org/wiki/Quad_%28unit%29)
''' ),

    'rydberg' :
        RPNUnitInfo( 'energy', 'rydberg', 'rydbergs', 'Ry',
                     [ ], [ 'science' ],
                     '''
''' ),

    'second*watt' :
        RPNUnitInfo( 'energy', 'second*watt', 'second*watt', 'Ws',
                     [ 'watt-second', 'watt-seconds' ], [ 'SI' ],
                     '''
''' ),

    'therm' :
        RPNUnitInfo( 'energy', 'therm', 'therms', '',
                     [ 'thm' ], [ 'England', 'US' ],
                     '''
The therm (symbol thm) is a non-SI unit of heat energy equal to 100,000
British thermal units (BTU).  It is approximately the energy equivalent of
burning 100 cubic feet (often referred to as 1 CCF) of natural gas.

(https://en.wikipedia.org/wiki/Therm)
''' ),

    'toe' :
        RPNUnitInfo( 'energy', 'toe', 'toes', '',
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
        RPNUnitInfo( 'energy', 'ton_of_coal', 'tons_of_coal', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'ton_of_TNT' :
        RPNUnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT',
                     [ ], [ 'informal' ],
                     '''
''' ),

    # force
    'dyne' :
        RPNUnitInfo( 'force', 'dyne', 'dynes', 'dyn',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'gram-force' :
        RPNUnitInfo( 'force', 'gram-force', 'grams-force', 'g-m',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'kilogram*meter/second^2' :
        RPNUnitInfo( 'force', 'kilogram*meter/second^2', 'kilogram*meter/second^2', '',
                     [ ], [ 'SI' ],
                     '''
This is the definition of the SI derived unit Newton (N).
''' ),

    'newton' :
        RPNUnitInfo( 'force', 'newton', 'newtons', 'N',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pond' :
        RPNUnitInfo( 'force', 'pond', 'ponds', '',
                     [ ], [ 'metric' ],
                     '''
''' ),

    'pound-force' :
        RPNUnitInfo( 'force', 'pound-force', 'pound-force', '',
                     [ ], [ 'FPS' ],
                     '''
''' ),

    'poundal' :
        RPNUnitInfo( 'force', 'poundal', 'poundals', 'pdl',
                     [ ], [ 'England' ],
                     '''
''' ),

    'sthene' :
        RPNUnitInfo( 'force', 'sthene', 'sthenes', 'sn',
                     [ 'funal' ], [ 'MTS' ],
                     '''
''' ),

    # frequency
    '1/second' :
        RPNUnitInfo( 'frequency', '1/second', '1/second', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'every_minute' :
        RPNUnitInfo( 'frequency', 'x_every_minute', 'x_every_minute', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'every_second' :
        RPNUnitInfo( 'frequency', 'x_every_second', 'x_every_second', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'hertz' :
        RPNUnitInfo( 'frequency', 'hertz', 'hertz', 'Hz',
                     [ 'cycle', 'cycles' ], [ 'SI' ],
                     '''
''' ),

    'hourly' :
        RPNUnitInfo( 'frequency', 'x_hourly', 'x_hourly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'daily' :
        RPNUnitInfo( 'frequency', 'x_daily', 'x_daily', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'weekly' :
        RPNUnitInfo( 'frequency', 'x_weekly', 'x_weekly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'monthly' :
        RPNUnitInfo( 'frequency', 'x_monthly', 'x_monthly', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'yearly' :
        RPNUnitInfo( 'frequency', 'x_yearly', 'x_yearly', '',
                     [ 'annually' ], [ 'traditional' ],
                     '''
''' ),

    'becquerel' :
        RPNUnitInfo( 'frequency', 'becquerel', 'becquerels', 'Bq',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'curie' :
        RPNUnitInfo( 'frequency', 'curie', 'curies', 'Ci',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'rutherford' :
        RPNUnitInfo( 'frequency', 'rutherford', 'rutherfords', 'rd',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    # illuminance
    'candela*radian^2/meter^2' :
        RPNUnitInfo( 'illuminance', 'candela*radian^2/meter^2', 'candela*radian^2/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'flame' :
        RPNUnitInfo( 'illuminance', 'flame', 'flame', '',
                     [ ], [ ],
                     '''
''' ),

    'footcandle' :
        RPNUnitInfo( 'illuminance', 'footcandle', 'footcandles', 'fc',
                     [ ], [ 'FPS' ],
                     '''
''' ),

    'lux' :
        RPNUnitInfo( 'illuminance', 'lux', 'lux', 'lx',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'lumen/meter^2' :
        RPNUnitInfo( 'illuminance', 'lumen/meter^2', 'lumens/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'nox' :
        RPNUnitInfo( 'illuminance', 'nox', 'nox', 'nx',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'phot' :
        RPNUnitInfo( 'illuminance', 'phot', 'phots', 'ph',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # inductance
    'abhenry' :
        RPNUnitInfo( 'inductance', 'abhenry', 'abhenries', 'abH',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'henry' :
        RPNUnitInfo( 'inductance', 'henry', 'henries', 'H',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/ampere^2*second^2' :
        RPNUnitInfo( 'inductance', 'kilogram*meter^2/ampere^2*second^2', 'kilogram*meter^2/ampere^2*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'stathenry' :
        RPNUnitInfo( 'inductance', 'stathenry', 'stathenries', 'statH',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # information_entropy
    'ban' :
        RPNUnitInfo( 'information_entropy', 'ban', 'bans', '',
                     [ 'hartley', 'hartleys', 'dit', 'dits' ], [ 'IEC' ],
                     '''
''' ),

    'bit' :
        RPNUnitInfo( 'information_entropy', 'bit', 'bits', 'b',
                     [ 'shannon', 'shannons' ], [ 'computing' ],
                     '''
A 'binary digit', which can store two values.
''' ),

    'byte' :
        RPNUnitInfo( 'information_entropy', 'byte', 'bytes', 'B',
                     [ 'octet', 'octets' ], [ 'computing' ],
                     '''
The traditional unit of computer storage, whose value has varied over the years
and on different platforms, but is now commonly defined to be 8 bits in size.
''' ),

    'btupf' :
        RPNUnitInfo( 'information_entropy', 'btupf', 'btupf', '',
                     [ ], [ 'England' ],
                     '''
''' ),

    'clausius' :
        RPNUnitInfo( 'information_entropy', 'clausius', 'clausius', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'dword' :
        RPNUnitInfo( 'information_entropy', 'dword', 'dwords', '',
                     [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ],
                     '''
A 'double-word' consisting of 2 16-bits words, or 32 bits total.
''' ),

    'joule/kelvin' :
        RPNUnitInfo( 'information_entropy', 'joule/kelvin', 'joules/kelvin', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'kilogram*meter^2/kelvin*second^2' :
        RPNUnitInfo( 'information_entropy', 'kilogram*meter^2/kelvin*second^2', 'kilogram*meter^2/kelvin*second^2', '',
                     [ ], [ 'physics' ],
                     '''
This is the unit of the Boltzmann constant.
''' ),

    'library_of_congress' :
        RPNUnitInfo( 'information_entropy', 'library_of_congress', 'x_library_of_congress', 'LoC',
                     [ 'congress', 'congresses', 'loc' ], [ 'computing' ],
                     '''
An informal unit of information measurement based on the contents of the U.S.
Library of Congress, estimated to be the equivalent of 10 terabytes in size.
''' ),

    'nibble' :
        RPNUnitInfo( 'information_entropy', 'nibble', 'nibbles', '',
                     [ 'nybble', 'nybbles' ], [ 'computing' ],
                     '''
A nybble is a half-byte, or 4 bits.  A nybble can be represented by a single
hexadecimal digit.
''' ),

    'nat' :
        RPNUnitInfo( 'information_entropy', 'nat', 'nats', '',
                     [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ],
                     '''
''' ),

    'nyp' :
        RPNUnitInfo( 'information_entropy', 'nyp', 'nyps', '',
                     [ ], [ 'computing' ],   # suggested by Donald Knuth
                     '''
A nyp is a term suggested by Knuth to represent two bits.  It is not a
commonly used term.
''' ),

    'oword' :
        RPNUnitInfo( 'information_entropy', 'oword', 'owords', '',
                     [ 'octaword', 'octawords', 'octoword', 'octowords' ], [ 'computing' ],
                     '''
An 'octo-word' consisting of 8 16-bit words or 128 bits total.
''' ),

    'qword' :
        RPNUnitInfo( 'information_entropy', 'qword', 'qwords', '',
                     [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ],
                     '''
A 'quad-word' consisting of 4 16-bit words, or 64 bits total.
''' ),

    'trit' :
        RPNUnitInfo( 'information_entropy', 'trit', 'trits', '',
                     [ ], [ 'computing' ],
                     '''
A trit is a 'ternary digit', by extension from the term 'bit' for 'binary
digit'.  In 1958 the Setun balanced ternary computer was developed at Moscow
State University, which used trits and 6-trit trytes.
''' ),

    'tryte' :
        RPNUnitInfo( 'information_entropy', 'tryte', 'trytes', '',
                     [ ], [ 'computing' ],
                     '''
A tryte consists of 6 trits (i.e., 'ternary digits'), and is named by extension
from the term 'byte'.  In 1958 the Setun balanced ternary computer was
developed at Moscow State University, which used trits and 6-trit trytes.
''' ),

    'word' :
        RPNUnitInfo( 'information_entropy', 'word', 'words', '',
                     [ 'short_integer', 'short_integers', 'short_int', 'short_ints', 'wyde' ], [ 'computing' ],
                     '''
A word is traditionally two bytes, or 16 bits.  The term 'wyde' was suggested
by Knuth.
''' ),

    # jerk
    'meter/second^3' :
        RPNUnitInfo( 'jerk', 'meter/second^3', 'meter/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'stapp' :
        RPNUnitInfo( 'jerk', 'stapp', 'stapps', '',
                     [ ], [ 'SI' ],
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
        RPNUnitInfo( 'jounce', 'meter/second^4', 'meter/second^4', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # length
    'aln' :
        RPNUnitInfo( 'length', 'aln', 'alns', '',
                     [ 'alen', 'alens' ], [ 'obsolete' ],
                     '''
''' ),

    'angstrom' :
        RPNUnitInfo( 'length', 'angstrom', 'angstroms', '',
                     [ 'angstroem', 'angstroems' ], [ 'science' ],
                     '''
''' ),

    'arpent' :
        RPNUnitInfo( 'length', 'arpent', 'arpents', '',
                     [ ], [ 'obsolete', 'France' ],
                     '''
''' ),

    'arshin' :
        RPNUnitInfo( 'length', 'arshin', 'arshins', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'astronomical_unit' :
        RPNUnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au',
                     [ ], [ 'science' ],
                     '''
''' ),

    'barleycorn' :
        RPNUnitInfo( 'length', 'barleycorn', 'barleycorns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'bolt' :
        RPNUnitInfo( 'length', 'bolt', 'bolts', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'caliber' :
        RPNUnitInfo( 'length', 'caliber', 'caliber', '',
                     [ 'calibre' ], [ 'US' ],
                     '''
''' ),

    'chain' :
        RPNUnitInfo( 'length', 'chain', 'chains', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'cicero' :
        RPNUnitInfo( 'length', 'cicero', 'ciceros', '',
                     [ ], [ 'typography', 'obsolete' ],
                     '''
''' ),

    'cubit' :
        RPNUnitInfo( 'length', 'cubit', 'cubits', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'diuym' :
        RPNUnitInfo( 'length', 'diuym', 'diuyms', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ell' :
        RPNUnitInfo( 'length', 'ell', 'ells', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'famn' :
        RPNUnitInfo( 'length', 'famn', 'famns', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'farshimmelt_potrzebie' :
        RPNUnitInfo( 'length', 'farshimmelt_potrzebie', 'farshimmelt_potrzebies', 'fpz',
                     [ 'far-potrzebie', 'far-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fathom' :
        RPNUnitInfo( 'length', 'fathom', 'fathoms', 'fath',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'finger' :
        RPNUnitInfo( 'length', 'finger', 'fingers', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'fingerbreadth' :
        RPNUnitInfo( 'length', 'fingerbreadth', 'fingerbreadths', '',
                     [ 'fingersbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'foot' :
        RPNUnitInfo( 'length', 'foot', 'feet', 'ft',
                     [ ], [ 'traditional', 'FPS' ],
                     '''
''' ),

    'french' :
        RPNUnitInfo( 'length', 'french', 'French', '',
                     [ 'french_gauge', 'french_scale', 'charrier' ], [ 'France' ],
                     '''
The French scale or French gauge system is commonly used to measure the size of
a catheter.  It is most often abbreviated as Fr, but can often be seen
abbreviated as Fg, Ga, FR or F.  It may also be abbreviated as CH or Ch (for
Charriere, its inventor).

https://en.wikipedia.org/wiki/French_catheter_scale
''' ),

    'furlong' :
        RPNUnitInfo( 'length', 'furlong', 'furlongs', '', [ ], [ 'imperial' ],
                     '''
''' ),

    'furshlugginer_potrzebie' :
        RPNUnitInfo( 'length', 'furshlugginer_potrzebie', 'furshlugginer_potrzebies', 'Fpz',
                     [ 'fur-potrzebie', 'fur-potrzebies', 'Fur-potrzebie', 'Fur-potrzebies' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fut' :
        RPNUnitInfo( 'length', 'fut', 'futs', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'greek_cubit' :
        RPNUnitInfo( 'length', 'greek_cubit', 'greek_cubits', '',
                     [ ], [ 'obsolete', 'Greece' ],
                     '''
''' ),

    'gutenberg' :
        RPNUnitInfo( 'length', 'gutenberg', 'gutenbergs', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'hand' :
        RPNUnitInfo( 'length', 'hand', 'hands', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'handbreadth' :
        RPNUnitInfo( 'length', 'handbreadth', 'handbreadths', '',
                     [ 'handsbreadth' ], [ 'obsolete' ],
                     '''
''' ),

    'hubble' :
        RPNUnitInfo( 'length', 'hubble', 'hubbles', '',
                     [ ], [ 'astronomy' ],
                     '''
''' ),

    'inch' :
        RPNUnitInfo( 'length', 'inch', 'inches', 'in',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'ken' :
        RPNUnitInfo( 'length', 'ken', 'kens', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'kosaya_sazhen' :
        RPNUnitInfo( 'length', 'kosaya_sazhen', 'kosaya_sazhens', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'kyu' :
        RPNUnitInfo( 'length', 'kyu', 'kyus', '',
                     [ 'Q' ], [ 'typography', 'computing' ],
                     '''
''' ),

    'league' :
        RPNUnitInfo( 'length', 'league', 'leagues', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'light-second' :
        RPNUnitInfo( 'length', 'light-second', 'light-seconds', '',
                      [ ], [ 'science' ],
                     '''
''' ),

    'light-year' :
        RPNUnitInfo( 'length', 'light-year', 'light-years', 'ly',
                     [ 'a1' ], [ 'science' ],
                     '''
''' ),

    'liniya' :
        RPNUnitInfo( 'length', 'liniya', 'liniya', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'link' :
        RPNUnitInfo( 'length', 'link', 'links', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'long_cubit' :
        RPNUnitInfo( 'length', 'long_cubit', 'long_cubits', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'long_reed' :
        RPNUnitInfo( 'length', 'long_reed', 'long_reeds', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'marathon' :
        RPNUnitInfo( 'length', 'marathon', 'marathons', '',
                     [ ], [ 'informal' ],
                     '''
''' ),

    'mezhevaya_versta' :
        RPNUnitInfo( 'length', 'mezhevaya_versta', 'mezhevaya_verstas', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'meter' :
        RPNUnitInfo( 'length', 'meter', 'meters', 'm',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'metric_foot' :
        RPNUnitInfo( 'length', 'metric_foot', 'metric_feet', '',
                     [ ], [ 'UK', 'unofficial' ],
                     '''
''' ),

    'micron' :
        RPNUnitInfo( 'length', 'micron', 'microns', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'mil' :
        RPNUnitInfo( 'length', 'mil', 'mils', '',
                     [ 'thou' ], [ 'US' ],
                     '''
''' ),

    'mile' :
        RPNUnitInfo( 'length', 'mile', 'miles', 'mi',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'nail' :
        RPNUnitInfo( 'length', 'nail', 'nails', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'nautical_mile' :
        RPNUnitInfo( 'length', 'nautical_mile', 'nautical_miles', '',
                     [ ], [ 'nautical' ],
                     '''
''' ),

    'parsec' :
        RPNUnitInfo( 'length', 'parsec', 'parsecs', 'pc',
                     [ ], [ 'science' ],
                     '''
''' ),

    'perch' :
        RPNUnitInfo( 'length', 'perch', 'perches', '',
                     [ 'pole', 'poles' ], [ 'imperial' ],
                     '''
''' ),

    'pica' :
        RPNUnitInfo( 'length', 'pica', 'picas', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'point' :
        RPNUnitInfo( 'length', 'point', 'points', '',
                     [ ], [ 'typography' ],
                     '''
''' ),

    'poppyseed' :
        RPNUnitInfo( 'length', 'poppyseed', 'poppyseeds', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'pyad' :
        RPNUnitInfo( 'length', 'pyad', 'pyads', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'rack_unit' :
        RPNUnitInfo( 'length', 'rack_unit', 'rack_units', '',
                     [ ], [ 'computers' ],
                     '''
A rack unit (abbreviated U or RU) is a unit of measure defined as 44.50
millimetres (1.752 in).  It is most frequently used as a measurement of the
overall height of 19-inch and 23-inch rack frames, as well as the height of
equipment that mounts in these frames, whereby the height of the frame or
equipment is expressed as multiples of rack units.

https://en.wikipedia.org/wiki/Rack_unit
''' ),

    'reed' :
        RPNUnitInfo( 'length', 'reed', 'reeds', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'rod' :
        RPNUnitInfo( 'length', 'rod', 'rods', 'rd',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'rope' :
        RPNUnitInfo( 'length', 'rope', 'ropes', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'potrzebie' :
        RPNUnitInfo( 'length', 'potrzebie', 'potrzebies', 'pz',
                     [ ], [ 'Potrzebie', 'humorous' ],
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
        RPNUnitInfo( 'length', 'sazhen', 'sazhens', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'siriometer' :
        RPNUnitInfo( 'length', 'siriometer', 'siriometers', '',
                     [ ], [ 'science' ],  # proposed in 1911 by Cark V. L. Charlier
                     '''
''' ),

    'skein' :
        RPNUnitInfo( 'length', 'skein', 'skeins', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'smoot' :
        RPNUnitInfo( 'length', 'smoot', 'smoots', '',
                     [ ], [ 'humorous' ],
                     '''
''' ),

    'span' :
        RPNUnitInfo( 'length', 'span', 'spans', '',
                     [ 'breadth' ], [ 'imperial' ],
                     '''
''' ),

    'stadium' :
        RPNUnitInfo( 'length', 'stadium', 'stadia', '',
                     [ ], [ 'Rome' ],
                     '''
''' ),

    'twip' :
        RPNUnitInfo( 'length', 'twip', 'twips', 'twp',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'vershok' :
        RPNUnitInfo( 'length', 'vershok', 'vershoks', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'versta' :
        RPNUnitInfo( 'length', 'versta', 'verstas', '',
                     [ 'verst', 'versts' ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'yard' :
        RPNUnitInfo( 'length', 'yard', 'yards', 'yd',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    # luminance
    'apostilb' :
        RPNUnitInfo( 'luminance', 'apostilb', 'apostilbs', 'asb',
                     [ 'blondel', 'blondels' ], [ 'CGS' ],
                     '''
''' ),

    'bril' :
        RPNUnitInfo( 'luminance', 'bril', 'brils', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'candela/meter^2' :
        RPNUnitInfo( 'luminance', 'candela/meter^2', 'candelas/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'footlambert' :
        RPNUnitInfo( 'luminance', 'footlambert', 'footlamberts', '',
                     [ 'foot*lambert', 'foot*lamberts', 'feet*lambert' ], [ 'US', 'obsolete' ],
                     '''
''' ),

    'lambert' :
        RPNUnitInfo( 'luminance', 'lambert', 'lamberts', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'nit' :
        RPNUnitInfo( 'luminance', 'nit', 'nits', 'nt',
                     [ 'meterlambert', 'meter*lambert', 'meterlamberts', 'meter*lamberts' ], [ 'obsolete' ],
                     '''
''' ),

    'skot' :
        RPNUnitInfo( 'luminance', 'skot', 'skots', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'stilb' :
        RPNUnitInfo( 'luminance', 'stilb', 'stilbs', 'sb',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # luminous_flux
    'lumen' :
        RPNUnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'candela*radian^2' :
        RPNUnitInfo( 'luminous_flux', 'candela*radian^2', 'candela*radians^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # luminous_intensity
    'candela' :
        RPNUnitInfo( 'luminous_intensity', 'candela', 'candelas', 'cd',
                     [ 'candle', 'candles', 'bougie', 'bougies' ], [ 'SI' ],
                     '''
''' ),

    'hefnerkerze' :
        RPNUnitInfo( 'luminous_intensity', 'hefnerkerze', 'hefnerkerze', 'HK',
                     [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    # magnetic_field_strength
    'ampere/meter' :
        RPNUnitInfo( 'magnetic_field_strength', 'ampere/meter', 'amperes/meter', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'oersted' :
        RPNUnitInfo( 'magnetic_field_strength', 'oersted', 'oersted', 'Oe',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    # magnetic_flux
    'kilogram*meter^2/ampere*second^2' :
        RPNUnitInfo( 'magnetic_flux', 'kilogram*meter^2/ampere*second^2', 'kilogram*meter^2/ampere*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),


    'maxwell' :
        RPNUnitInfo( 'magnetic_flux', 'maxwell', 'maxwells', 'Mx',
                     [ 'line', 'lines' ], [ 'CGS' ],
                     '''
''' ),

    'unit_pole' :
        RPNUnitInfo( 'magnetic_flux', 'unit_pole', 'unit_poles', '',
                     [ 'unitpole', 'unitpoles' ], [ 'CGS' ],
                     '''
''' ),

    'weber' :
        RPNUnitInfo( 'magnetic_flux', 'weber', 'webers', 'Wb',
                     [ 'promaxwell', 'promaxwells' ], [ 'SI' ],
                     '''
''' ),

    # magnetic_flux_density
    'gauss' :
        RPNUnitInfo( 'magnetic_flux_density', 'gauss', 'gauss', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'kilogram/ampere*second^2' :
        RPNUnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', 'kilogram/ampere*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'tesla' :
        RPNUnitInfo( 'magnetic_flux_density', 'tesla', 'teslas', 'T',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # mass
    'berkovets' :
        RPNUnitInfo( 'mass', 'berkovets', 'berkovets', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'blintz' :
        RPNUnitInfo( 'mass', 'blintz', 'blintzes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'carat' :
        RPNUnitInfo( 'mass', 'carat', 'carats', 'ct',
                     [ ], [ 'US' ],
                     '''
''' ),

    'chandrasekhar_limit' :
        RPNUnitInfo( 'mass', 'chandrasekhar_limit', 'x chandrasekhar_limit', '',
                     [ 'chandrasekhar', 'chandrasekhars' ], [ 'science' ],
                     '''
''' ),

    'dalton' :
        RPNUnitInfo( 'mass', 'dalton', 'daltons', '',
                     [ 'amu', 'atomic_mass_unit' ], [ 'science' ],
                     '''
''' ),

    'dolya' :
        RPNUnitInfo( 'mass', 'dolya', 'dolyas', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'doppelzentner' :
        RPNUnitInfo( 'mass', 'doppelzentner', 'doppelzentners', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'farshimmelt_blintz' :
        RPNUnitInfo( 'mass', 'farshimmelt_blintz', 'farshimmelt_blintzes', 'fb',
                     [ 'far-blintz', 'far-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'funt' :
        RPNUnitInfo( 'mass', 'funt', 'funts', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'furshlugginer_blintz' :
        RPNUnitInfo( 'mass', 'furshlugginer_blintz', 'furshlugginer_blintzes', 'Fb',
                     [ 'fur-blintz', 'fur-blintzes', 'Fur-blintz', 'Fur-blintzes' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'grain' :
        RPNUnitInfo( 'mass', 'grain', 'grains', 'gr',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'gram' :
        RPNUnitInfo( 'mass', 'gram', 'grams', 'g',
                     [ 'gramme', 'grammes' ], [ 'SI' ],
                     '''
''' ),

# hyl, metric_slug, technical_mass_unit, technische_masseseinheit, 9.80665 kg

    'joule*second^2/meter^2' :
        RPNUnitInfo( 'mass', 'joule*second^2/meter^2', 'joule*second^2/meter^2', '',
                     [ ], [ 'SI' ],
                     '''
This conversion is required to do mass-energy equivalence calculations.
''' ),

    'kip' :
        RPNUnitInfo( 'mass', 'kip', 'kips', '',
                     [ 'kilopound', 'kilopounds' ], [ 'US' ],
                     '''
''' ),

    'lot' :
        RPNUnitInfo( 'mass', 'lot', 'lots', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'ounce' :
        RPNUnitInfo( 'mass', 'ounce', 'ounces', 'oz',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'pennyweight' :
        RPNUnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt',
                     [ 'pwt' ], [ 'traditional', 'England' ],
                     '''
''' ),

    'pfund' :
        RPNUnitInfo( 'mass', 'pfund', 'pfunds', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'pood' :
        RPNUnitInfo( 'mass', 'pood', 'poods', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    'pound' :
        RPNUnitInfo( 'mass', 'pound', 'pounds', 'lb',
                     [ ], [ 'US', 'traditional', 'FPS' ],
                     '''
''' ),

    'quintal' :
        RPNUnitInfo( 'mass', 'quintal', 'quintals', 'q',
                     [ 'cantar', 'cantars' ], [ ],
                     '''
''' ),

    'sheet' :
        RPNUnitInfo( 'mass', 'sheet', 'sheets', '',
                     [ ], [ ],
                     '''
''' ),

    'slinch' :
        RPNUnitInfo( 'mass', 'slinch', 'slinches', '',
                     [ 'mug', 'mugs', 'snail', 'snails' ], [ 'NASA' ],
                     '''
''' ),

    'slug' :
        RPNUnitInfo( 'mass', 'slug', 'slugs', '',
                     [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ],
                     '''
''' ),

    'stone' :
        RPNUnitInfo( 'mass', 'stone', 'stones', '',
                     [ ], [ 'traditional', 'England' ],
                     '''
''' ),

    'stone_us' :
        RPNUnitInfo( 'mass', 'stone_us', 'stones_us', '',
                     [ 'us_stone', 'us_stones' ], [ 'US' ],
                     '''
''' ),

    'ton' :
        RPNUnitInfo( 'mass', 'ton', 'tons', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'tonne' :
        RPNUnitInfo( 'mass', 'tonne', 'tonnes', '',
                     [ 'metric_ton', 'metric_tons' ], [ 'MTS' ],
                     '''
''' ),

    'troy_ounce' :
        RPNUnitInfo( 'mass', 'troy_ounce', 'troy_ounces', 'toz',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'troy_pound' :
        RPNUnitInfo( 'mass', 'troy_pound', 'troy_pounds', '',
                     [ ], [ 'traditional'  ],
                     '''
''' ),

    'wey' :
        RPNUnitInfo( 'mass', 'wey', 'weys', '',
                     [ ], [ 'obsolete', 'England' ],
                     '''
''' ),

    'zentner' :
        RPNUnitInfo( 'mass', 'zentner', 'zentners', '',
                     [ ], [ 'Germany' ],
                     '''
''' ),

    'zolotnik' :
        RPNUnitInfo( 'mass', 'zolotnik', 'zolotniks', '',
                     [ ], [ 'Russia', 'obsolete' ],
                     '''
''' ),

    # power
    'decibel-milliwatt' :
        RPNUnitInfo( 'power', 'decibel-milliwatt', 'decibel-milliwatts', 'dBm',
                     [ 'dBmW', ], [ 'engineering' ],
                     '''
''' ),

    'decibel-watt' :
        RPNUnitInfo( 'power', 'decibel-watt', 'decibel-watt', 'dBW',
                     [ ], [ 'engineering' ],
                     '''
''' ),

    'horsepower' :
        RPNUnitInfo( 'power', 'horsepower', 'horsepower', 'hp',
                     [ ], [ 'US' ],
                     '''
''' ),

    'lusec' :
        RPNUnitInfo( 'power', 'lusec', 'lusecs', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'kilogram*meter^2/second^3' :
        RPNUnitInfo( 'power', 'kilogram*meter^2/second^3', 'kilogram*meter^2/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pferdestarke' :
        RPNUnitInfo( 'power', 'pferdestarke', 'pferdestarke', 'PS',
                     [ ], [ 'obsolete', 'Germany' ],
                     '''
''' ),

    'poncelet' :
        RPNUnitInfo( 'power', 'poncelet', 'poncelets', '',
                     [ ], [ 'obsolete' ],
                     '''
''' ),

    'watt' :
        RPNUnitInfo( 'power', 'watt', 'watts', 'W',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # pressure
    'atmosphere' :
        RPNUnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm',
                     [ ], [ 'natural' ],
                     '''
''' ),

    'bar' :
        RPNUnitInfo( 'pressure', 'bar', 'bars', '',
                     [ ], [ ],
                     '''
''' ),

    'barye' :
        RPNUnitInfo( 'pressure', 'barye', 'baryes', 'Ba',
                     [ 'barad', 'barads' ], [ 'CGS' ],
                     '''
''' ),

    'mmHg' :
        RPNUnitInfo( 'pressure', 'mmHg', 'mmHg', '',
                     [ ], [ 'metric' ],
                     '''
''' ),

    'kilogram/meter*second^2' :
        RPNUnitInfo( 'pressure', 'kilogram/meter*second^2', 'kilogram/meter*second^2', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pascal' :
        RPNUnitInfo( 'pressure', 'pascal', 'pascals', 'Pa',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'pieze' :
        RPNUnitInfo( 'pressure', 'pieze', 'piezes', '',
                     [ ], [ 'MTS' ],
                     '''
''' ),

    'psi' :
        RPNUnitInfo( 'pressure', 'pound/inch^2', 'pounds/inch^2', '',
                     [ ], [ 'FPS' ],
                     '''
''' ),

# technical_atmosphere (at) 98.0665 kPa

    'torr' :
        RPNUnitInfo( 'pressure', 'torr', 'torr', '',
                     [ ], [ ],
                     '''
''' ),

    # radiation_dose
    'banana_equivalent_dose' :
        RPNUnitInfo( 'radiation_dose', 'banana_equivalent_dose', 'banana_equivalent_doses', '',
                     [ 'banana', 'bananas' ], [ 'natural', 'informal' ],
                     '''
''' ),

    'gray' :
        RPNUnitInfo( 'radiation_dose', 'gray', 'grays', 'Gy',
                     [ ], [ 'SI' ],   # or should 'Gy' be giga-years?
                     '''
''' ),

    'meter^2/second^2' :
        RPNUnitInfo( 'radiation_dose', 'meter^2/second^2', 'meter^2/second^2', '',
                     [ ], [ 'SI' ],   # This doesn't seem to make sense, but joule/kilogram reduces to this!
                     '''
''' ),

    'rem' :
        RPNUnitInfo( 'radiation_dose', 'rem', 'rems', '',
                     [ 'roentgen_equivalent_man' ], [ 'CGS' ],
                     '''
''' ),

    'sievert' :
        RPNUnitInfo( 'radiation_dose', 'sievert', 'sieverts', 'Sv',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # radiation_exposure
    'coulomb/kilogram' :
        RPNUnitInfo( 'radiation_exposure', 'coulomb/kilogram', 'coulombs/kilogram', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    'rad' :
        RPNUnitInfo( 'radiation_exposure', 'rad', 'rads', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'roentgen' :
        RPNUnitInfo( 'radiation_exposure', 'roentgen', 'roentgens', 'R',
                     [ 'parker', 'parkers', 'rep', 'reps' ], [ 'NIST' ],
                     '''
''' ),

    # radiosity
    'kilogram/second^3' :
        RPNUnitInfo( 'radiosity', 'kilogram/second^3', 'kilogram/second^3', '',
                     [ ], [ 'SI' ],
                     '''
''' ),

    # ratio

    # Bel
    # Neper
    # karat (1/24)

    # solid_angle
    'hemisphere' :
        RPNUnitInfo( 'solid_angle', 'hemisphere', 'hemisphere', '',
                     [ 'half_sphere', 'half_spheres', 'halfsphere', 'halfspheres' ], [ 'mathematics' ],
                     '''
''' ),

    'radian^2' :
        RPNUnitInfo( 'solid_angle', 'radian^2', 'radian^2', '',
                     [ ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    'sphere' :
        RPNUnitInfo( 'solid_angle', 'sphere', 'spheres', '',
                     [ 'spat', 'spats' ], [ 'mathematics' ],
                     '''
''' ),

    'square_arcminute' :
        RPNUnitInfo( 'solid_angle', 'arcminute^2', 'arcminutes^2', '',
                     [ 'square_arcminutes', 'solid_arcminute', 'solid_arcminutes', 'sq_arcminute', 'sq_arcminutes', 'sqarcmin', 'sqarcmins', 'arcmins^2', 'spherical_minute', 'spherical_minutes' ], [ 'mathematics' ],
                     '''
''' ),

    'square_arcsecond' :
        RPNUnitInfo( 'solid_angle', 'arcsecond^2', 'arcseconds^2', '',
                     [ 'square_arcseconds', 'solid_arcsecond', 'solid_arcseconds', 'sq_arcsecond', 'sq_arcseconds', 'sqarcsec', 'sqarcsecs', 'arcsecs^2', 'spherical_second', 'spherical_seconds' ], [ 'mathematics' ],
                     '''
''' ),

    'square_degree' :
        RPNUnitInfo( 'solid_angle', 'degree^2', 'degrees^2', '',
                     [ 'square_degrees', 'sqdeg', 'solid_degree', 'solid_degrees', 'sq_degree', 'sq_degrees', 'sqdeg', 'sqdegs', 'spherical_degree', 'spherical_degrees' ], [ 'mathematics' ],
                     '''
''' ),

    'square_octant' :
        RPNUnitInfo( 'solid_angle', 'octant^2', 'octants^2', '',
                     [ 'square_octants', 'sqoctant', 'sqoctants', 'solid_octant', 'solid_octants', 'sq_octant', 'sq_octants', 'spherical_octant', 'spherical_octants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_quadrant' :
        RPNUnitInfo( 'solid_angle', 'quadrant^2', 'quadrants^2', '',
                     [ 'square_quadrants', 'sqquadrant', 'sqquadrants', 'solid_quadrant', 'solid_quadrants', 'sq_quadrant', 'sq_quadrants', 'spherical_quadrant', 'spherical_quadrants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_quintant' :
        RPNUnitInfo( 'solid_angle', 'quintant^2', 'quintants^2', '',
                     [ 'square_quintants', 'sqquintant', 'sqquintants', 'solid_quintant', 'solid_quintants', 'sq_quintant', 'sq_quintants', 'spherical_quintant', 'spherical_quintants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_sextant' :
        RPNUnitInfo( 'solid_angle', 'sextant^2', 'sextants^2', '',
                     [ 'square_sextants', 'sqsextant', 'sqsextants', 'solid_sextant', 'solid_sextants', 'sq_sextant', 'sq_sextants', 'spherical_sextant', 'spherical_sextants' ], [ 'mathematics' ],
                     '''
''' ),

    'square_grad' :
        RPNUnitInfo( 'solid_angle', 'grad^2', 'grads^2', '',
                     [ 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'sq_gon', 'sq_gons', 'sqgon', 'sqgons', 'grad^2', 'grads^2', 'gon^2', 'gons^2', 'spherical_gon', 'spherical_gons', 'spherical_grad', 'spherical_grads' ], [ 'mathematics' ],
                     '''
''' ),

    'steradian' :
        RPNUnitInfo( 'solid_angle', 'steradian', 'steradians', 'sr',
                     [ 'square_radian', 'square_radians', 'sq_radian', 'sq_radians', 'sq_rad', 'sqrad', 'spherical_radian', 'spherical_radians' ], [ 'SI', 'mathematics' ],
                     '''
''' ),

    # temperature
    'celsius' :
        RPNUnitInfo( 'temperature', 'celsius', 'degrees_celsius', 'Cel',
                     [ 'centigrade', 'degC', 'degreeC', 'degreesC', 'degree_centigrade', 'degrees_centigrade', 'degrees_C' ], [ 'SI' ],
                     '''
''' ),

    'degree_newton' :
        RPNUnitInfo( 'temperature', 'degree_newton', 'degrees_newton', '',
                     [ 'degN', 'degreeN', 'degreesN', 'degrees_N' ], [ 'obsolete' ],
                     '''
''' ),

    'delisle' :
        RPNUnitInfo( 'temperature', 'delisle', 'degrees_delisle', 'De',
                     [ 'degD', 'degreeD', 'degreesD', 'degree_delisle', 'degrees_D' ], [ 'obsolete' ],
                     '''
''' ),

    'fahrenheit' :
        RPNUnitInfo( 'temperature', 'fahrenheit', 'degrees_fahrenheit', '',
                     [ 'fahr', 'degF', 'degreeF', 'degreesF', 'degree_fahrenheit', 'degrees_F' ], [ 'US', 'traditional' ],
                     '''
''' ),

    'kelvin' :
        RPNUnitInfo( 'temperature', 'kelvin', 'degrees_kelvin', 'K',
                     [ 'degK', 'degreeK', 'degreesK', 'degree_kelvin', 'degrees_K' ], [ 'SI' ],
                     '''
The Kelvin scale is an absolute thermodynamic temperature scale using as its
null point absolute zero, the temperature at which all thermal motion ceases
in the classical description of thermodynamics. The kelvin (symbol: K) is the
base unit of temperature in the International System of Units (SI).

Ref:  https://en.wikipedia.org/wiki/Kelvin
''' ),

    'rankine' :
        RPNUnitInfo( 'temperature', 'rankine', 'degrees_rankine', 'R',
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
        RPNUnitInfo( 'temperature', 'reaumur', 'degrees_reaumur', 'Re',
                     [ 'degRe', 'degreeRe', 'degreesRe', 'degree_reaumur', 'degrees_Re' ], [ 'obsolete' ],
                     '''
''' ),

    'romer' :
        RPNUnitInfo( 'temperature', 'romer', 'degrees_romer', 'Ro',
                     [ 'degRo', 'degreeRo', 'degreesRo', 'degree_romer', 'degrees_Ro' ], [ 'obsolete' ],
                     '''
''' ),

    # time
    '1/hertz' :
        RPNUnitInfo( 'time', '1/hertz', '1/hertz', '',
                     [ ], [ ],
                     '''
''' ),

    'beat' :
        RPNUnitInfo( 'time', 'beat', 'beat', '',
                     [ ], [ ],
                     '''
''' ),

    'blink' :
        RPNUnitInfo( 'time', 'blink', 'blinks', '',
                     [ 'metric_second', 'metric_seconds' ], [ ],
                     '''
''' ),

    'century' :
        RPNUnitInfo( 'time', 'century', 'centuries', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'clarke' :
        RPNUnitInfo( 'time', 'clarke', 'clarkes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'cowznofski' :
        RPNUnitInfo( 'time', 'cowznofski', 'cowznofskis', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'day' :
        RPNUnitInfo( 'time', 'day', 'days', '', [ 'ephemeris_day' ],
                     [ 'traditional' ],
                     '''
''' ),

    'decade' :
        RPNUnitInfo( 'time', 'decade', 'decades', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'eon' :
        RPNUnitInfo( 'time', 'eon', 'eons', '',
                     [ ], [ 'traditional', 'years' ],
                     '''
''' ),

    'fortnight' :
        RPNUnitInfo( 'time', 'fortnight', 'fortnights', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'gregorian_year' :
        RPNUnitInfo( 'time', 'gregorian_year', 'gregorian_years', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'hour' :
        RPNUnitInfo( 'time', 'hour', 'hours', 'hr',
                     [ ], [ 'traditional' ],
                     '''
An hour (abbreviated 'hr') is a unit of time conventionally reckoned as 1/24
of a day, or 60 minutes.

Ref:  https://en.wikipedia.org/wiki/Hour
''' ),

    'kovac' :
        RPNUnitInfo( 'time', 'kovac', 'kovacs', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'jiffy' :
        RPNUnitInfo( 'time', 'jiffy', 'jiffies', '',
                     [ ], [ 'computing' ],
                     '''
''' ),

    'lustrum' :
        RPNUnitInfo( 'time', 'lustrum', 'lustra', '',
                     [ ], [ 'obsolete', 'years' ],
                     '''
''' ),

    'martin' :
        RPNUnitInfo( 'time', 'martin', 'martins', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'microcentury' :
        RPNUnitInfo( 'time', 'microcentury', 'microcenturies', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'microfortnight' :
        RPNUnitInfo( 'time', 'microfortnight', 'microfortnights', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'mingo' :
        RPNUnitInfo( 'time', 'mingo', 'mingoes', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'minute' :
        RPNUnitInfo( 'time', 'minute', 'minutes', '',
                     [ ], [ 'traditional' ],  # 'min' is already an operator
                     '''
The minute is a unit of time or angle (the minute angle unit in rpn is the
'arcminute').  As a unit of time, the minute is most of times equal to 1/60 of
an hour, or 60 seconds.

https://en.wikipedia.org/wiki/Minute
''' ),

    'month' :
        RPNUnitInfo( 'time', 'month', 'months', 'mo',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'nanocentury' :
        RPNUnitInfo( 'time', 'nanocentury', 'nanocenturies', '',
                     [ ], [ 'humorous', 'computing' ],
                     '''
''' ),

    'second' :
        RPNUnitInfo( 'time', 'second', 'seconds', 's',
                     [ ], [ 'SI', 'traditional', 'FPS' ],   # 'sec' is already an operator
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
        RPNUnitInfo( 'time', 'shake', 'shakes', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_day' :
        RPNUnitInfo( 'time', 'sidereal_day', 'sidereal_days', '',
                     [ 'earth_day', 'earth_days' ], [ 'science' ],
                     '''
''' ),

    'sidereal_hour' :
        RPNUnitInfo( 'time', 'sidereal_hour', 'sidereal_hours', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_minute' :
        RPNUnitInfo( 'time', 'sidereal_minute', 'sidereal_minutes', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'sidereal_second' :
        RPNUnitInfo( 'time', 'sidereal_second', 'sidereal_seconds', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'svedberg' :
        RPNUnitInfo( 'time', 'svedberg', 'svedbergs', '',
                     [ ], [ ],
                     '''
''' ),

    'tropical_month' :
        RPNUnitInfo( 'time', 'tropical_month', 'tropical_months', '',
                     [ ], [ 'science' ],
                     '''
''' ),

    'week' :
        RPNUnitInfo( 'time', 'week', 'weeks', 'wk', [ 'sennight' ],
                     [ 'traditional' ],
                     '''
''' ),

    'wolverton' :
        RPNUnitInfo( 'time', 'wolverton', 'wolvertons', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'wood' :
        RPNUnitInfo( 'time', 'wood', 'woods', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'year' :
        RPNUnitInfo( 'time', 'year', 'years', '',
                     [ 'annum', 'annums', 'julian_year', 'julian_years', 'twelvemonth', 'twelvemonths' ], [ 'traditional', 'years' ],
                     '''
''' ),

    # velocity
    'bubnoff_unit' :
        RPNUnitInfo( 'velocity', 'bubnoff_unit', 'bubnoff_units', '',
                     [ 'bubnoff', 'bubnoffs' ], [ 'science' ],
                     '''
The Bubnoff unit is employed in geology to measure rates of lowering of earth
surfaces due to erosion and is named after the Russian (German-Baltic)
geologist Serge von Bubnoff (1888-1957).  An erosion speed of 1 B also means
that 1 cubic meter of earth is being removed from an area of 1 square km in 1
year.

https://en.wikipedia.org/wiki/Bubnoff_unit
''' ),

    'kine' :
        RPNUnitInfo( 'velocity', 'kine', 'kine', '',
                     [ ], [ 'CGS' ],
                     '''
''' ),

    'meter/second' :
        RPNUnitInfo( 'velocity', 'meter/second', 'meters/second', 'mps',
                     [ 'benz' ], [ 'SI' ],
                     '''
''' ),

    'knot' :
        RPNUnitInfo( 'velocity', 'knot', 'knots', 'kt',
                     [ ], [ 'nautical' ],
                     '''
''' ),

    'mach' :
        RPNUnitInfo( 'velocity', 'mach', 'mach', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'mile/hour' :
        RPNUnitInfo( 'velocity', 'mile/hour', 'miles/hour', 'mph',
                     [ ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'kilometer/hour' :
        RPNUnitInfo( 'velocity', 'kilometer/hour', 'kilometers/hour', 'kph',
                     [ ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'speed_of_sound' :
        RPNUnitInfo( 'velocity', 'speed_of_sound', 'x speed_of_sound', '',
                     [ ], [ 'natural' ],
                     '''
''' ),

    # volume
    'acre*foot' :
        RPNUnitInfo( 'volume', 'acre*foot', 'acre*feet', '',
                     [ 'acre-foot', 'acre-feet', 'acre_foot', 'acre_feet' ], [ 'FPS', 'imperial' ],
                     '''
''' ),

    'balthazar' :
        RPNUnitInfo( 'volume', 'balthazar', 'balthazars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'beer_barrel' :
        RPNUnitInfo( 'volume', 'beer_barrel', 'beer_barrel', '',
                     [ ], [ 'US', 'beer' ],
                     '''
''' ),

    'beer_keg' :
        RPNUnitInfo( 'volume', 'beer_keg', 'beer_kegs', '',
                     [ ], [ 'US', 'beer' ],
                     '''
''' ),

    'bottle' :
        RPNUnitInfo( 'volume', 'bottle', 'bottles', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'bucket' :
        RPNUnitInfo( 'volume', 'bucket', 'buckets', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'bushel' :
        RPNUnitInfo( 'volume', 'bushel', 'bushels', 'bu',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'chopine' :
        RPNUnitInfo( 'volume', 'chopine', 'chopines', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'clavelin' :
        RPNUnitInfo( 'volume', 'clavelin', 'clavelins', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'coffeespoon' :
        RPNUnitInfo( 'volume', 'coffeespoon', 'coffeespoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'coomb' :
        RPNUnitInfo( 'volume', 'coomb', 'coombs', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'cord' :
        RPNUnitInfo( 'volume', 'cord', 'cords', '',
                     [ ], [ 'traditional' ],
                     '''
''' ),

    'foot^3' :
        RPNUnitInfo( 'volume', 'foot^3', 'foot^3', '',
                     [ 'cuft', 'cu_ft', 'cubic_ft', 'cubic_foot', 'cubic_feet', 'cu_foot', 'cu_feet', 'cufoot', 'cufeet'  ], [ 'traditional', 'FPS' ],
                     '''
''' ),

    'cup' :
        RPNUnitInfo( 'volume', 'cup', 'cups', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'dash' :
        RPNUnitInfo( 'volume', 'dash', 'dashes', '',
                    [ ], [ 'cooking' ],
                     '''
''' ),

    'demi' :
        RPNUnitInfo( 'volume', 'demi', 'demis', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'dessertspoon' :
        RPNUnitInfo( 'volume', 'dessertspoon', 'dessertspoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'dram' :
        RPNUnitInfo( 'volume', 'dram', 'drams', '',
                     [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ],
                     '''
''' ),

    'dry_barrel' :
        RPNUnitInfo( 'volume', 'dry_barrel', 'dry_barrels', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'dry_hogshead' :
        RPNUnitInfo( 'volume', 'dry_hogshead', 'dry_hogsheads', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'dry_gallon' :
        RPNUnitInfo( 'volume', 'dry_gallon', 'dry_gallons', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_pint' :
        RPNUnitInfo( 'volume', 'dry_pint', 'dry_pints', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_quart' :
        RPNUnitInfo( 'volume', 'dry_quart', 'dry_quarts', '',
                     [ ], [ 'traditional', 'US' ],
                     '''
''' ),

    'dry_tun' :
        RPNUnitInfo( 'volume', 'dry_tun', 'dry_tuns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'farshimmelt_ngogn' :
        RPNUnitInfo( 'volume', 'farshimmelt_ngogn', 'farshimmelt_ngogns', 'fn',
                     [ 'far-ngogn', 'far-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'fifth' :
        RPNUnitInfo( 'volume', 'fifth', 'fifths', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'firkin' :
        RPNUnitInfo( 'volume', 'firkin', 'firkins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'fluid_ounce' :
        RPNUnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', '',
                     [ 'floz' ], [ 'traditional' ],
                     '''
''' ),

    'furshlugginer_ngogn' :
        RPNUnitInfo( 'volume', 'furshlugginer_ngogn', 'furshlugginer_ngogns', 'Fn',
                     [ 'Fur-ngogn', 'Fur-ngogns', 'fur-ngogn', 'fur-ngogns' ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'gallon' :
        RPNUnitInfo( 'volume', 'gallon', 'gallons', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'gill' :
        RPNUnitInfo( 'volume', 'gill', 'gills', '',
                     [ 'noggin', 'noggins', 'teacup', 'teacups' ], [ 'imperial' ],
                     '''
''' ),

    'goliath' :
        RPNUnitInfo( 'volume', 'goliath', 'goliaths', '',
                     [ 'primat' ], [ 'wine' ],
                     '''
''' ),

    'hogshead' :
        RPNUnitInfo( 'volume', 'hogshead', 'hogsheads', '',
                     [ ], [ 'traditional', 'wine' ],
                     '''
''' ),

    'hoppus_foot' :
        RPNUnitInfo( 'volume', 'hoppus_foot', 'hoppus_feet', '',
                     [ 'hoppus_cube', 'hoppus_cubes' ], [ 'England', 'obsolete' ],
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
        RPNUnitInfo( 'volume', 'hoppus_ton', 'hoppus_tons', '',
                     [ ], [ 'England', 'obsolete' ],
                     '''
The hoppus ton (HT) was also a traditionally used unit of volume in British
forestry. One hoppus ton is equal to 50 hoppus feet or 1.8027 cubic metres.
Some shipments of tropical hardwoods, especially shipments of teak from
Myanmar (Burma), are still stated in hoppus tons.

Ref:  https://en.wikipedia.org/wiki/Hoppus
''' ),

    'imperial_bushel' :
        RPNUnitInfo( 'volume', 'imperial_bushel', 'imperial_bushels', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_butt' :
        RPNUnitInfo( 'volume', 'imperial_butt', 'imperial_butts', '',
                     [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_cup' :
        RPNUnitInfo( 'volume', 'imperial_cup', 'imperial_cups', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gallon' :
        RPNUnitInfo( 'volume', 'imperial_gallon', 'imperial_gallons', '',
                     [ 'congius', 'congii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_gill' :
        RPNUnitInfo( 'volume', 'imperial_gill', 'imperial_gills', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_hogshead' :
        RPNUnitInfo( 'volume', 'imperial_hogshead', 'imperial_hogsheads', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_peck' :
        RPNUnitInfo( 'volume', 'imperial_peck', 'imperial_pecks', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'imperial_pint' :
        RPNUnitInfo( 'volume', 'imperial_pint', 'imperial_pints', '',
                     [ 'octarius', 'octarii' ], [ 'imperial' ],
                     '''
''' ),

    'imperial_quart' :
        RPNUnitInfo( 'volume', 'imperial_quart', 'imperial_quarts', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'jack' :
        RPNUnitInfo( 'volume', 'jack', 'jacks', '',
                     [ 'jackpot', 'jackpots' ], [ 'imperial' ],
                     '''
''' ),

    'jennie' :
        RPNUnitInfo( 'volume', 'jennie', 'jennies', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'jeroboam' :
        RPNUnitInfo( 'volume', 'jeroboam', 'jeroboams', '',
                     [ 'double_magnum', 'double_magnums' ], [ 'wine' ],
                     '''
''' ),

    'jigger' :
        RPNUnitInfo( 'volume', 'jigger', 'jiggers', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'kenning' :
        RPNUnitInfo( 'volume', 'kenning', 'kennings', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'kilderkin' :
        RPNUnitInfo( 'volume', 'kilderkin', 'kilderkins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'liter' :
        RPNUnitInfo( 'volume', 'liter', 'liters', 'L',    # The U.S. standard is to use uppercase "L" because the lower case 'l' looks like a 1
                     [ ], [ 'SI' ],
                     '''
''' ),

    'magnum' :
        RPNUnitInfo( 'volume', 'magnum', 'magnums', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'marie_jeanne' :
        RPNUnitInfo( 'volume', 'marie_jeanne', 'marie_jeannes', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'melchior' :
        RPNUnitInfo( 'volume', 'melchior', 'melchiors', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'melchizedek' :
        RPNUnitInfo( 'volume', 'melchizedek', 'melchizedeks', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'meter^3' :
        RPNUnitInfo( 'volume', 'meter^3', 'meter^3', '',
                     [ 'cum', 'cu_m', 'cubic_m', 'cubic_meter', 'cubic_meters', 'cu_meter', 'cu_meters', 'cumeter', 'cumeters' ], [ 'SI' ],
                     '''
''' ),

    'methuselah' :
        RPNUnitInfo( 'volume', 'methuselah', 'methuselahs', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'minim' :
        RPNUnitInfo( 'volume', 'minim', 'minims', 'gtt',
                     [ 'drop' ], [ 'traditional' ],
                     '''
''' ),

    'mordechai' :
        RPNUnitInfo( 'volume', 'mordechai', 'mordechais', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'nebuchadnezzar' :
        RPNUnitInfo( 'volume', 'nebuchadnezzar', 'nebuchadnezzars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'ngogn' :
        RPNUnitInfo( 'volume', 'ngogn', 'ngogns', '',
                     [ ], [ 'Potrzebie', 'humorous' ],
                     '''
''' ),

    'oil_barrel' :
        RPNUnitInfo( 'volume', 'oil_barrel', 'oil_barrels', 'bbl',
                     [ ], [ 'US' ],
                     '''
''' ),

    'peck' :
        RPNUnitInfo( 'volume', 'peck', 'pecks', 'pk',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'piccolo' :
        RPNUnitInfo( 'volume', 'piccolo', 'piccolos', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'pinch' :
        RPNUnitInfo( 'volume', 'pinch', 'pinches', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'pin' :
        RPNUnitInfo( 'volume', 'pin', 'pins', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'pint' :
        RPNUnitInfo( 'volume', 'pint', 'pints', 'pt',
                     [ ], [ 'traditional', 'cooking', 'US' ],
                     '''
''' ),

    'pipe' :
        RPNUnitInfo( 'volume', 'pipe', 'pipes', '',
                     [ 'butt', 'butts' ], [ 'imperial' ],
                     '''
''' ),

    'pony' :
        RPNUnitInfo( 'volume', 'pony', 'ponies', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'portuguese_almude' :
        RPNUnitInfo( 'volume', 'portuguese_almude', 'portuguese_almudes', '',
                     [ ], [ 'Portugal' ],
                     '''
''' ),

    'pottle' :
        RPNUnitInfo( 'volume', 'pottle', 'pottles', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'puncheon' :
        RPNUnitInfo( 'volume', 'puncheon', 'puncheons', '',
                     [ 'tertian', 'tertians' ], [ 'wine' ],
                     '''
''' ),

    'quart' :
        RPNUnitInfo( 'volume', 'quart', 'quarts', '',
                     [ ], [ 'US' ],
                     '''
''' ),

    'rehoboam' :
        RPNUnitInfo( 'volume', 'rehoboam', 'rehoboams', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'rundlet' :
        RPNUnitInfo( 'volume', 'rundlet', 'rundlets', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'salmanazar' :
        RPNUnitInfo( 'volume', 'salmanazar', 'salmanazars', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'saltspoon' :
        RPNUnitInfo( 'volume', 'saltspoon', 'saltspoons', '',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'scruple' :
        RPNUnitInfo( 'volume', 'scruple', 'scruples', '',
                     [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ],
                     '''
''' ),

    'smidgen' :
        RPNUnitInfo( 'volume', 'smidgen', 'smidgens', '',
                     [ 'smidgeon', 'smidgeons' ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'snit' :
        RPNUnitInfo( 'volume', 'snit', 'snits', '',
                     [ ], [ 'U.S.' ],
                     '''
http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'spanish_almude' :
        RPNUnitInfo( 'volume', 'spanish_almude', 'spanish_almudes', '',
                     [ ], [ 'Spain' ],
                     '''
''' ),

    'solomon' :
        RPNUnitInfo( 'volume', 'solomon', 'solomons', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'sovereign' :
        RPNUnitInfo( 'volume', 'sovereign', 'sovereigns', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'standard' :
        RPNUnitInfo( 'volume', 'standard', 'standards', '',
                     [ ], [ 'wine' ],
                     '''
''' ),

    'stein' :
        RPNUnitInfo( 'volume', 'stein', 'steins', '',
                     [ ], [ 'Germany' ],
                     '''
A stein is a German beer mug.  Steins come in various sizes, but the most
common size seems to be 1/2 liter (1.057 U.S pint or 0.880 British Imperial
pint).

http://www.unc.edu/~rowlett/units/dictS.html
''' ),

    'stere' :
        RPNUnitInfo( 'volume', 'stere', 'steres', 'st',
                     [ ], [ 'metric', 'obsolete' ],  # ... but not SI
                     '''
''' ),

    'strike' :
        RPNUnitInfo( 'volume', 'strike', 'strikes', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'sydharb' :
        RPNUnitInfo( 'volume', 'sydharb', 'sydharbs', '',
                     [ ], [ 'informal' ],
                     '''
The approximate volume of the Syndey Harbor at high tide, considered to be
equal to 562,000 megaliters.
''' ),

    'tablespoon' :
        RPNUnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'teaspoon' :
        RPNUnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp',
                     [ ], [ 'traditional', 'cooking' ],
                     '''
''' ),

    'tierce' :
        RPNUnitInfo( 'volume', 'tierce', 'tierces', '',
                     [ ], [ 'wine', 'imperial' ],
                     '''
''' ),

    'tun' :
        RPNUnitInfo( 'volume', 'tun', 'tuns', '',
                     [ ], [ 'imperial' ],
                     '''
''' ),

    'wineglass' :
        RPNUnitInfo( 'volume', 'wineglass', 'wineglasses', '',
                     [ 'wine_glass', 'wine_glasses' ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_barrel' :
        RPNUnitInfo( 'volume', 'wine_barrel', 'wine_barrels', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_butt' :
        RPNUnitInfo( 'volume', 'wine_butt', 'wine_butts', '',
                     [ 'wine_pipe', 'wine_pipes' ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_gallon' :
        RPNUnitInfo( 'volume', 'wine_gallon', 'wine_gallons', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_hogshead' :
        RPNUnitInfo( 'volume', 'wine_hogshead', 'wine_hogsheads', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
''' ),

    'wine_tun' :
        RPNUnitInfo( 'volume', 'wine_tun', 'wine_tuns', '',
                     [ ], [ 'imperial', 'wine' ],
                     '''
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

metricUnits = {
    'ampere'            : ( 'amperes',          'A',    [ 'amp' ], [ 'amps' ] ),
    'ampere*second'     : ( '',                 'As',   [ 'amp-second' ], [ 'amp-seconds' ] ),
    'arcsecond'         : ( 'arcseconds',       'as',   [ ], [ ] ),
    'are'               : ( 'ares',             'a',    [ ], [ ] ),
    'bar'               : ( 'bars',             'bar',  [ ], [ ] ),
    'barn'              : ( 'barns',            '',     [ ], [ ] ),
    'becquerel'         : ( 'becquerels',       'Bq',   [ ], [ ] ),
    'blintz'            : ( 'blintzes',         'bl',   [ ], [ ] ),
    'calorie'           : ( 'calories',         'cal',  [ ], [ 'cals' ] ),
    'circular_mil'      : ( 'circular_mils',    'cmil', [ ], [ ] ),
    'coulomb'           : ( 'coulombs',         'C',    [ ], [ ] ),
    'curie'             : ( 'cruies',           'Ci',   [ ], [ ] ),
    'dyne'              : ( 'dynes',            '',     [ ], [ ] ),
    'electron-volt'     : ( 'electron-volts',   'eV',   [ ], [ ] ),
    'erg'               : ( 'ergs',             '',     [ ], [ ] ),
    'farad'             : ( 'farads',           'F',    [ ], [ ] ),
    'galileo'           : ( 'galileos',         '',     [ 'gal' ], [ 'gals' ] ),
    'gauss'             : ( 'gauss',            '',     [ ], [ ] ),
    'gram'              : ( 'grams',            'g',    [ 'gramme' ], [ 'grammes' ] ),
    'gram-equivalent'   : ( 'grams-equivalent', 'gE',   [ 'gram-energy', 'gramme-energy' ], [ 'grams-energy', 'grammes-energy' ] ),
    'gram-force'        : ( 'grams-force',      'gf',   [ 'gramme-force' ], [ 'grammes-force' ] ),
    'gray'              : ( 'grays',            'Gy',   [ ], [ ] ),
    'henry'             : ( 'henries',          'H',    [ ], [ ] ),
    'hertz'             : ( 'hertz',            'Hz',   [ 'cycle' ], [ 'cycles' ] ),
    'joule'             : ( 'joules',           'J',    [ ], [ ] ),
    'katal'             : ( 'katals',           'kat',  [ ], [ ] ),
    'kelvin'            : ( 'kelvins',          'K',    [ ], [ ] ),
    'liter'             : ( 'liters',           'L',    [ 'litre' ], [ 'litres' ] ),
    'lumen'             : ( 'lumens',           'lm ',  [ ], [ ] ),
    'lux'               : ( 'lux',              'lx',   [ ], [ ] ),
    'maxwell'           : ( 'maxwells',         'Mx',   [ ], [ ] ),
    'meter'             : ( 'meters',           'm',    [ 'metre' ], [ 'metres' ] ),
    'mole'              : ( 'moles',            'mol',  [ ], [ ] ),
    'newton'            : ( 'newtons',          'N',    [ ], [ ] ),
    'ngogn'             : ( 'ngogns',           'ng',   [ ], [ ] ),
    'ohm'               : ( 'ohms',             'O',    [ ], [ ] ),
    'parsec'            : ( 'parsecs',          'pc',   [ ], [ ] ),
    'pascal'            : ( 'pascals',          'Pa',   [ ], [ ] ),
    'pascal*second'     : ( '',                 'Pas',  [ 'pascal-second' ], [ 'pascal-seconds' ] ),
    'poise'             : ( 'poise',            '',     [ ], [ ] ),
    'pond'              : ( 'ponds',            '',     [ ], [ ] ),
    'potrzebie'         : ( 'potrzebies',       'pz',   [ ], [ ] ),
    'rad'               : ( 'rads',             'rad',  [ ], [ ] ),
    'radian'            : ( 'radians',          '',     [ ], [ ] ),
    'rem'               : ( 'rems',             'rem',  [ ], [ ] ),
    'second'            : ( 'seconds',          's',    [ ], [ ] ),
    'siemens'           : ( 'siemens',          'S',    [ 'mho' ], [ 'mhos' ] ),
    'sievert'           : ( 'sieverts',         'Sv',   [ ], [ ] ),
    'steradian'         : ( 'steradians',       '',     [ ], [ ] ),
    'stere'             : ( 'steres',           'st',   [ ], [ ] ),
    'tesla'             : ( 'teslas',           'T',    [ ], [ ] ),
    'volt'              : ( 'volts',            'V',    [ ], [ ] ),
    'watt'              : ( 'watts',            'W',    [ ], [ ] ),
    'second*watt'       : ( '',                 'Ws',   [ 'watt-second' ], [ 'watt-seconds' ] ),
    'weber'             : ( 'webers',           'Wb',   [ ], [ ] ),
}


# //******************************************************************************
# //
# //  integralMetricUnits
# //
# //  Any units that should get the SI prefixes with positive powers.
# //
# //  ( name, plural name, abbreviation, aliases, plural aliases )
# //
# //******************************************************************************

integralMetricUnits = {
    'light-year'        : ( 'light-years',      'ly',   [ ], [ ] ),
    'ton'               : ( 'tons',             '',     [ ], [ ] ),
    'tonne'             : ( 'tonnes',           '',     [ ], [ ] ),
    'ton_of_TNT'        : ( 'tons_of_TNT',      'tTNT', [ ], [ ] ),
    'year'              : ( 'years',            'y',    [ ], [ ] ),
}


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
    ( 'bit',            'bits',             'b',    [ ], [ ] ),
    ( 'bit/second',     'bits/second',      'bps',  [ ], [ ] ),
    ( 'byte',           'bytes',            'B',    [ ], [ ] ),
    ( 'byte/second',    'bytes/second',     'Bps',  [ ], [ ] ),
]


# //******************************************************************************
# //
# //  timeUnits
# //
# //******************************************************************************

timeUnits = [
    ( 'minute',     'minutes',      'm',        '60' ),
    ( 'hour',       'hours',        'h',        '3600' ),
    ( 'day',        'days',         'd',        '86400' ),
    ( 'year',       'years',        'y',        '31557600' ),   # Julian year == 365.25 days
]


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
    ( 'abampere',                   'ampere' )                              : mpmathify( '10' ),
    ( 'abcoulomb',                  'coulomb' )                             : mpmathify( '10' ),
    ( 'abfarad',                    'farad' )                               : mpmathify( '1.0e9' ),
    ( 'abmho',                      'siemens' )                             : mpmathify( '1.0e9' ),
    ( 'acre',                       'foot^2' )                              : mpmathify( '43560' ),
    ( 'acre',                       'nanoacre' )                            : mpmathify( '1.0e9' ),
    ( 'acre*foot',                  'foot^3' )                              : mpmathify( '43560' ),
    ( 'aln',                        'inch' )                                : mpmathify( '23.377077865' ),
    ( 'ampere',                     'statampere' )                          : mpmathify( '299792458' ),
    ( 'arcminute',                  'arcsecond' )                           : mpmathify( '60' ),
    ( 'are',                        'meter^2' )                             : mpmathify( '100' ),
    ( 'arpent',                     'foot' )                                : mpmathify( '192' ),
    ( 'arshin',                     'pyad' )                                : mpmathify( '4' ),
    ( 'astronomical_unit',          'meter' )                               : mpmathify( '149597870691' ),
    ( 'atmosphere',                 'pascal' )                              : mpmathify( '101325' ),
    ( 'bakers_dozen',               'unity' )                               : mpmathify( '13' ),
    ( 'balthazar',                  'liter' )                               : mpmathify( '12.0' ),
    ( 'ban',                        'nat' )                                 : log( 10 ),
    ( 'banana_equivalent_dose',     'sievert' )                             : mpmathify( '9.8e-8' ),
    ( 'bar',                        'pascal' )                              : mpmathify( '1.0e5' ),
    ( 'barleycorn',                 'poppyseed' )                           : mpmathify( '4' ),
    ( 'beat',                       'blink' )                               : mpmathify( '100' ),
    ( 'beer_barrel',                'beer_keg' )                            : mpmathify( '2' ),
    ( 'beer_barrel',                'gallon' )                              : mpmathify( '31' ),
    ( 'berkovets',                  'dolya' )                               : mpmathify( '3686400' ),
    ( 'billion',                    'unity' )                               : mpmathify( '1.0e9' ),
    ( 'bit',                        'kilogram*meter^2/kelvin*second^2' )    : fmul( mpmathify( '1.38064852e-23' ), log( 2 ) ),
    ( 'bit',                        'nat' )                                 : log( 2 ),
    ( 'blintz',                     'farshimmelt_blintz' )                  : mpmathify( '1.0e5' ),
    ( 'blintz',                     'furshlugginer_blintz' )                : mpmathify( '1.0e-6' ),
    ( 'blintz',                     'gram' )                                : mpmathify( '36.42538631' ),
    ( 'bolt',                       'foot' )                                : mpmathify( '120' ),
    ( 'btu',                        'joule' )                               : mpmathify( '1054.5' ),
    ( 'btupf',                      'joule/kelvin' )                        : mpmathify( '1899.100534716' ),
    ( 'bucket',                     'gallon' )                              : mpmathify( '4' ),
    ( 'bushel',                     'peck' )                                : mpmathify( '4' ),
    ( 'byte',                       'bit' )                                 : mpmathify( '8' ),
    ( 'byte/second',                'bit/second' )                          : mpmathify( '8' ),
    ( 'calorie',                    'joule' )                               : mpmathify( '4.184' ),
    ( 'candela*radian^2/meter^2',   'lumen/meter^2' )                       : mpmathify( '1' ),
    ( 'carat',                      'grain' )                               : fadd( 3, fdiv( 1, 6 ) ),
    ( 'carucate',                   'acre' )                                : mpmathify( '120' ),
    ( 'carucate',                   'bovate' )                              : mpmathify( '8' ),
    ( 'celo',                       'meter/second^2' )                      : mpmathify( '0.3048' ),
    ( 'celsius',                    'degree_newton' )                       : fdiv( 33, 100 ),
    ( 'celsius',                    'reaumur' )                             : fdiv( 4, 5 ),
    ( 'centillion',                 'unity' )                               : mpmathify( '1.0e303' ),
    ( 'century',                    'microcentury' )                        : mpmathify( '1.0e6' ),
    ( 'century',                    'nanocentury' )                         : mpmathify( '1.0e9' ),
    ( 'century',                    'year' )                                : mpmathify( '100' ),
    ( 'chain',                      'yard' )                                : mpmathify( '22' ),
    ( 'chandrasekhar_limit',        'gram' )                                : mpmathify( '2.765e33' ),
    ( 'chopine',                    'liter' )                               : mpmathify( '0.25' ),
    ( 'circle',                     'degree' )                              : mpmathify( '360' ),
    ( 'circular_inch',              'circular_mil' )                        : mpmathify( '1.0e6' ),
    ( 'circular_mil',               'meter^2' )                             : mpmathify( '5.06707479097e-10' ),
    ( 'clarke',                     'day' )                                 : mpmathify( '1' ),
    ( 'clarke',                     'wolverton' )                           : mpmathify( '1.0e6' ),
    ( 'clausius',                   'joule/kelvin' )                        : mpmathify( '4186.8' ),
    ( 'clavelin',                   'liter' )                               : mpmathify( '0.62' ),
    ( 'conductance_quantum',        'siemens' )                             : mpmathify( '7.7480917310e-5' ),
    ( 'coomb',                      'strike' )                              : mpmathify( '2' ),
    ( 'cord',                       'foot^3' )                              : mpmathify( '128' ),
    ( 'coulomb',                    'ampere*second' )                       : mpmathify( '1' ),
    ( 'coulomb/kilogram',           'roentgen' )                            : mpmathify( '3876' ),
    ( 'cowznofski',                 'mingo' )                               : mpmathify( '10' ),
    ( 'cubit',                      'inch' )                                : mpmathify( '18' ),
    ( 'cup',                        'dram' )                                : mpmathify( '64' ),
    ( 'cup',                        'fluid_ounce' )                         : mpmathify( '8' ),
    ( 'cup',                        'gill' )                                : mpmathify( '2' ),
    ( 'cup',                        'wineglass' )                           : mpmathify( '4' ),
    ( 'curie',                      'becquerel' )                           : mpmathify( '3.7e10' ),
    ( 'daily',                      'monthly' )                             : mpmathify( '30' ),
    ( 'daily',                      'weekly' )                              : mpmathify( '7' ),
    ( 'daily',                      'yearly' )                              : mpmathify( '365.25' ),
    ( 'dalton',                     'gram' )                                : mpmathify( '1.660539040e-24' ),
    ( 'day',                        'beat' )                                : mpmathify( '1000' ),
    ( 'day',                        'hour' )                                : mpmathify( '24' ),
    ( 'decade',                     'year' )                                : mpmathify( '10' ),
    ( 'decibel-watt',               'decibel-milliwatt' )                   : mpmathify( '30' ),
    ( 'decillion',                  'unity' )                               : mpmathify( '1.0e33' ),
    ( 'degree',                     'arcminute' )                           : mpmathify( '60' ),
    ( 'degree',                     'furman' )                              : mpmathify( '65536' ),
    ( 'degree',                     'streck' )                              : mpmathify( '17.5' ),
    ( 'demi',                       'liter' )                               : mpmathify( '0.375' ),
    ( 'dessertspoon',               'teaspoon' )                            : mpmathify( '2' ),
    ( 'diuym',                      'inch' )                                : mpmathify( '1' ),
    ( 'diuym',                      'liniya' )                              : mpmathify( '10' ),
    ( 'doppelzentner',              'zentner' )                             : mpmathify( '2' ),
    ( 'dozen',                      'unity' )                               : mpmathify( '12' ),
    ( 'dram',                       'scruple' )                             : mpmathify( '3' ),
    ( 'dry_barrel',                 'bushel' )                              : mpmathify( '4' ),
    ( 'dry_barrel',                 'foot^3' )                              : fdiv( 49, 12 ),
    ( 'dry_gallon',                 'dry_quart' )                           : mpmathify( '4' ),
    ( 'dry_hogshead',               'dry_barrel' )                          : mpmathify( '2' ),
    ( 'dry_pint',                   'foot^3' )                              : mpmathify( '0.0194446252894' ),
    ( 'dry_quart',                  'dry_pint' )                            : mpmathify( '2' ),
    ( 'dry_tun',                    'dry_hogshead' )                        : mpmathify( '4' ),
    ( 'duodecillion',               'unity' )                               : mpmathify( '1.0e39' ),
    ( 'dword',                      'bit' )                                 : mpmathify( '32' ),
    ( 'eight',                      'unity' )                               : mpmathify( '8' ),
    ( 'eighteen',                   'unity' )                               : mpmathify( '18' ),
    ( 'eighty',                     'unity' )                               : mpmathify( '80' ),
    ( 'electron-volt',              'joule' )                               : mpmathify( '1.6021766208e-19' ),
    ( 'eleven',                     'unity' )                               : mpmathify( '11' ),
    ( 'ell',                        'inch' )                                : mpmathify( '45' ),
    ( 'eon',                        'year' )                                : mpmathify( '1e9' ),
    ( 'every_minute',               'hourly' )                              : mpmathify( '60' ),
    ( 'every_second',               '1/second' )                            : mpmathify( '1' ),
    ( 'every_second',               'every_minute' )                        : mpmathify( '60' ),
    ( 'famn',                       'aln' )                                 : mpmathify( '3' ),
    ( 'farad',                      'ampere^2*second^4/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'farad',                      'jar' )                                 : mpmathify( '9.0e8' ),
    ( 'farad',                      'statfarad' )                           : mpmathify( '898755178736.5' ),
    ( 'faraday',                    'coulomb' )                             : mpmathify( '96485.3383' ),
    ( 'fathom',                     'foot' )                                : mpmathify( '6' ),
    ( 'fifteen',                    'unity' )                               : mpmathify( '15' ),
    ( 'fifty',                      'unity' )                               : mpmathify( '50' ),
    ( 'finger',                     'inch' )                                : mpmathify( '4.5' ),
    ( 'fingerbreadth',              'inch' )                                : mpmathify( '0.75' ),
    ( 'firkin',                     'gallon' )                              : mpmathify( '9' ),
    ( 'firkin',                     'pin' )                                 : mpmathify( '2' ),
    ( 'five',                       'unity' )                               : mpmathify( '5' ),
    ( 'flame',                      'lux' )                                 : mpmathify( '43.0556416668' ),
    ( 'flock',                      'unity' )                               : mpmathify( '40' ),
    ( 'fluid_ounce',                'dram' )                                : mpmathify( '8' ),
    ( 'fluid_ounce',                'tablespoon' )                          : mpmathify( '2' ),
    ( 'foe',                        'joule' )                               : mpmathify( '10e44' ),
    ( 'foot',                       'inch' )                                : mpmathify( '12' ),
    ( 'footcandle',                 'lux' )                                 : mpmathify( '10.763910417' ),            # (m/ft)^2
    ( 'footlambert',                'candela/meter^2' )                     : mpmathify( '3.42625909963539052691' ),  # 1/pi cd/ft^2
    ( 'fortnight',                  'day' )                                 : mpmathify( '14' ),
    ( 'fortnight',                  'microfortnight' )                      : mpmathify( '1.0e6' ),
    ( 'four',                       'unity' )                               : mpmathify( '4' ),
    ( 'fourteen',                   'unity' )                               : mpmathify( '14' ),
    ( 'funt',                       'dolya' )                               : mpmathify( '9216' ),
    ( 'furlong',                    'yard' )                                : mpmathify( '220' ),
    ( 'fut',                        'foot' )                                : mpmathify( '1' ),
    ( 'galileo',                    'meter/second^2' )                      : mpmathify( '0.01' ),
    ( 'gallon',                     'fifth' )                               : mpmathify( '5' ),
    ( 'gallon',                     'quart' )                               : mpmathify( '4' ),
    ( 'goliath',                    'liter' )                               : mpmathify( '27.0' ),
    ( 'googol',                     'unity' )                               : mpmathify( '1.0e100' ),
    ( 'grad',                       'degree' )                              : mpmathify( '0.9' ),
    ( 'gram',                       'dolya' )                               : mpmathify( '22.50481249152' ),
    ( 'gram-equivalent',            'joule' )                               : fdiv( power( 299792458, 2 ), 1000 ),
    ( 'gram-force',                 'newton' )                              : mpmathify( '0.00980665' ),
    ( 'gray',                       'meter^2/second^2' )                    : mpmathify( '1' ),
    ( 'gray',                       'rad' )                                 : mpmathify( '100' ),
    ( 'gray',                       'sievert' )                             : mpmathify( '1' ),
    ( 'great_gross',                'gross' )                               : mpmathify( '12' ),
    ( 'greek_cubit',                'inch' )                                : mpmathify( '18.22' ),
    ( 'gregorian_year',             'second' )                              : mpmathify( '31556952' ),
    ( 'gross',                      'unity' )                               : mpmathify( '144' ),
    ( 'hand',                       'inch' )                                : mpmathify( '4' ),
    ( 'handbreadth',                'inch' )                                : mpmathify( '3' ),
    ( 'hartree',                    'rydberg' )                             : mpmathify( '2' ),
    ( 'hefnerkerze',                'candela' )                             : mpmathify( '0.920' ),  # approx.
    ( 'henry',                      'abhenry' )                             : mpmathify( '1.0e9' ),
    ( 'henry',                      'kilogram*meter^2/ampere^2*second^2' )  : mpmathify( '1' ),
    ( 'hertz',                      '1/second' )                            : mpmathify( '1' ),
    ( 'hertz',                      'becquerel' )                           : mpmathify( '1' ),
    ( 'hogshead',                   'liter' )                               : mpmathify( '238.481' ),
    ( 'homestead',                  'acre' )                                : mpmathify( '160' ),
    ( 'hoppus_ton',                 'hoppus_foot' )                         : mpmathify( '50' ),
    ( 'hoppus_ton',                 'meter^3' )                             : mpmathify( '1.8027' ),
    ( 'horsepower',                 'watt' )                                : mpmathify( '745.69987158227022' ),
    ( 'hour',                       'minute' )                              : mpmathify( '60' ),
    ( 'hourly',                     'daily' )                               : mpmathify( '24' ),
    ( 'hubble',                     'light-year' )                          : mpmathify( '1.0e9' ),
    ( 'hundred',                    'unity' )                               : mpmathify( '100' ),
    ( 'imperial_bushel',            'kenning' )                             : mpmathify( '2' ),
    ( 'imperial_butt',              'imperial_hogshead' )                   : mpmathify( '2' ),
    ( 'imperial_cup',               'imperial_gill' )                       : mpmathify( '2' ),
    ( 'imperial_gallon',            'pottle' )                              : mpmathify( '2' ),
    ( 'imperial_gill',              'jack' )                                : mpmathify( '2' ),
    ( 'imperial_hogshead',          'coomb' )                               : mpmathify( '2' ),
    ( 'imperial_peck',              'imperial_quart' )                      : mpmathify( '2' ),
    ( 'imperial_pint',              'imperial_cup' )                        : mpmathify( '2' ),
    ( 'imperial_quart',             'imperial_pint' )                       : mpmathify( '2' ),
    ( 'imperial_square',            'foot^2' )                              : mpmathify( '100' ),
    ( 'inch',                       'barleycorn' )                          : mpmathify( '3' ),
    ( 'inch',                       'caliber' )                             : mpmathify( '100' ),
    ( 'inch',                       'cicero' )                              : fdiv( mpmathify( '50.8' ), 9 ),
    ( 'inch',                       'gutenberg' )                           : mpmathify( '7200' ),
    ( 'inch',                       'meter' )                               : mpmathify( '0.0254' ),
    ( 'inch',                       'mil' )                                 : mpmathify( '1000' ),
    ( 'inch',                       'pica' )                                : mpmathify( '6' ),
    ( 'inch',                       'point' )                               : mpmathify( '72' ),
    ( 'inch',                       'twip' )                                : mpmathify( '1440' ),
    ( 'jack',                       'tablespoon' )                          : mpmathify( '5' ),
    ( 'jennie',                     'liter' )                               : mpmathify( '0.5' ),
    ( 'jeroboam',                   'liter' )                               : mpmathify( '3.0' ),  # some French regions use 4.5
    ( 'jigger',                     'pony' )                                : mpmathify( '2' ),
    ( 'joule',                      'erg' )                                 : mpmathify( '1.0e7' ),
    ( 'joule',                      'kilogram*meter^2/second^2' )           : mpmathify( '1' ),
    ( 'joule*second^2/meter^2',     'gram' )                                : mpmathify( '1000' ),
    ( 'katal',                      'enzyme_unit' )                         : mpmathify( '6.0e7' ),
    ( 'katal',                      'mole/second' )                         : mpmathify( '1' ),
    ( 'kayser',                     'electron-volt' )                       : mpmathify( '123.984e-6' ),
    ( 'kelvin',                     'rankine' )                             : fdiv( 9, 5 ),
    ( 'ken',                        'inch' )                                : mpmathify( '83.4' ),
    ( 'kenning',                    'imperial_peck' )                       : mpmathify( '2' ),
    ( 'kilderkin',                  'firkin' )                              : mpmathify( '2' ),
    ( 'kilogram/meter^3',           'kilogram/liter' )                      : mpmathify( '1000' ),
    ( 'kip',                        'pound' )                               : mpmathify( '1000' ),
    ( 'kosaya_sazhen',              'meter' )                               : mpmathify( '2.48' ),
    ( 'kovac',                      'wolverton' )                           : mpmathify( '10' ),
    ( 'lambert',                    'candela/meter^2' )                     : fdiv( 10000, pi ),
    ( 'league',                     'mile' )                                : mpmathify( '3' ),
    ( 'leo',                        'meter/second^2' )                      : mpmathify( '10' ),
    ( 'library_of_congress',        'byte' )                                : mpmathify( '1.0e13' ),
    ( 'light-second',               'meter' )                               : mpmathify( '299792458' ),
    ( 'light-year',                 'light-second' )                        : mpmathify( '31557600' ),
    ( 'link',                       'inch' )                                : mpmathify( '7.92' ),
    ( 'liter',                      'ngogn' )                               : mpmathify( '86.2477899004' ),
    ( 'liter',                      'stein' )                               : mpmathify( '2' ),
    ( 'long_cubit',                 'inch' )                                : mpmathify( '21' ),
    ( 'long_hundred',               'unity' )                               : mpmathify( '120' ),
    ( 'long_reed',                  'foot' )                                : mpmathify( '10.5' ),
    ( 'lot',                        'dolya' )                               : mpmathify( '288' ),
    ( 'lumen',                      'candela*radian^2' )                    : mpmathify( '1' ),
    ( 'lustrum',                    'year' )                                : mpmathify( '5' ),
    ( 'lux',                        'lumen/meter^2' )                       : mpmathify( '10.7639104167' ),
    ( 'lux',                        'nox' )                                 : mpmathify( '1000' ),
    ( 'mach',                       'meter/second' )                        : mpmathify( '340.2868' ),
    ( 'magnum',                     'bottle' )                              : mpmathify( '2' ),
    ( 'magnum',                     'liter' )                               : mpmathify( '1.5' ),
    ( 'marathon',                   'yard' )                                : mpmathify( '46145' ),
    ( 'marie_jeanne',               'liter' )                               : mpmathify( '2.25' ),
    ( 'martin',                     'kovac' )                               : mpmathify( '100' ),
    ( 'melchior',                   'liter' )                               : mpmathify( '18.0' ),
    ( 'melchizedek',                'liter' )                               : mpmathify( '30.0' ),
    ( 'meter',                      'angstrom' )                            : mpmathify( '1.0e10' ),
    ( 'meter',                      'french' )                              : mpmathify( '3000' ),
    ( 'meter',                      'kyu' )                                 : mpmathify( '4000' ),
    ( 'meter',                      'micron' )                              : mpmathify( '1.0e6' ),
    ( 'meter/second',               'bubnoff_unit' )                        : mpmathify( '3.15576e13' ),
    ( 'meter/second',               'kine' )                                : mpmathify( '100' ),
    ( 'meter/second',               'knot' )                                : mpmathify( '1.943844492' ),
    ( 'meter^2',                    'barn' )                                : mpmathify( '1.0e28' ),
    ( 'meter^2',                    'foot^2' )                              : mpmathify( '10.7639104167' ),
    ( 'meter^2',                    'outhouse' )                            : mpmathify( '1.0e34' ),
    ( 'meter^2',                    'shed' )                                : mpmathify( '1.0e52' ),
    ( 'meter^3',                    'foot^3' )                              : mpmathify( '35.3146667215' ),
    ( 'meter^3',                    'liter' )                               : mpmathify( '1000' ),
    ( 'meter^3',                    'liter' )                               : mpmathify( '1000' ),
    ( 'methuselah',                 'liter' )                               : mpmathify( '6.0' ),
    ( 'metric_foot',                'meter' )                               : mpmathify( '0.3' ),
    ( 'mezhevaya_versta',           'versta' )                              : mpmathify( '2' ),
    ( 'mile',                       'foot' )                                : mpmathify( '5280' ),
    ( 'mile/hour',                  'kilometer/hour' )                      : mpmathify( '1.609344' ),
    ( 'mile/hour',                  'meter/second' )                        : mpmathify( '0.44704' ),
    ( 'million',                    'unity' )                               : mpmathify( '1.0e6' ),
    ( 'mingo',                      'clarke' )                              : mpmathify( '10' ),
    ( 'minute',                     'second' )                              : mpmathify( '60' ),
    ( 'mmHg',                       'pascal' )                              : mpmathify( '133.3224' ),        # approx.
    ( 'month',                      'day' )                                 : mpmathify( '30' ),
    ( 'mordechai',                  'liter' )                               : mpmathify( '9.0' ),
    ( 'morgen',                     'are' )                                 : mpmathify( '85.6532' ),
    ( 'nail',                       'inch' )                                : mpmathify( '2.25' ),
    ( 'nat',                        'joule/kelvin' )                        : mpmathify( '1.380650e-23' ),
    ( 'nautical_mile',              'meter' )                               : mpmathify( '1852' ),
    ( 'nebuchadnezzar',             'liter' )                               : mpmathify( '15.0' ),
    ( 'newton',                     'dyne' )                                : mpmathify( '1.0e5' ),
    ( 'newton',                     'kilogram*meter/second^2' )             : mpmathify( '1' ),
    ( 'newton',                     'pond' )                                : mpmathify( '101.97161298' ),
    ( 'newton',                     'poundal' )                             : mpmathify( '7.233013851' ),
    ( 'ngogn',                      'farshimmelt_ngogn' )                   : mpmathify( '1.0e5' ),
    ( 'ngogn',                      'furshlugginer_ngogn' )                 : mpmathify( '1.0e-6' ),
    ( 'nibble',                     'bit' )                                 : mpmathify( '4' ),
    ( 'nine',                       'unity' )                               : mpmathify( '9' ),
    ( 'nineteen',                   'unity' )                               : mpmathify( '19' ),
    ( 'ninety',                     'unity' )                               : mpmathify( '90' ),
    ( 'nit',                        'apostilb' )                            : pi,
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'nonillion',                  'unity' )                               : mpmathify( '1.0e30' ),
    ( 'novemdecillion',             'unity' )                               : mpmathify( '1.0e60' ),
    ( 'nyp',                        'bit' )                                 : mpmathify( '2' ),
    ( 'oc1',                        'bit/second' )                          : mpmathify( '5.184e7' ),
    ( 'oc12',                       'oc1' )                                 : mpmathify( '12' ),
    ( 'oc192',                      'oc1' )                                 : mpmathify( '192' ),
    ( 'oc24',                       'oc1' )                                 : mpmathify( '24' ),
    ( 'oc3',                        'oc1' )                                 : mpmathify( '3' ),
    ( 'oc48',                       'oc1' )                                 : mpmathify( '48' ),
    ( 'oc768',                      'oc1' )                                 : mpmathify( '768' ),
    ( 'octant',                     'degree' )                              : mpmathify( '45' ),
    ( 'octillion',                  'unity' )                               : mpmathify( '1.0e27' ),
    ( 'octodecillion',              'unity' )                               : mpmathify( '1.0e57' ),
    ( 'oersted',                    'ampere/meter' )                        : mpmathify( '79.5774715' ),
    ( 'ohm',                        '1/siemens' )                           : mpmathify( '1' ),
    ( 'ohm',                        'abohm' )                               : mpmathify( '1e9' ),
    ( 'ohm',                        'german_mile' )                         : mpmathify( '57.44' ),
    ( 'ohm',                        'jacobi' )                              : mpmathify( '0.6367' ),
    ( 'ohm',                        'kilogram*meter^2/ampere^2*second^3' )  : mpmathify( '1' ),
    ( 'ohm',                        'matthiessen' )                         : mpmathify( '13.59' ),
    ( 'ohm',                        'varley' )                              : mpmathify( '25.61' ),
    ( 'oil_barrel',                 'gallon' )                              : mpmathify( '42' ),
    ( 'ounce',                      'gram' )                                : mpmathify( '28.349523125' ),
    ( 'oword',                      'bit' )                                 : mpmathify( '128' ),
    ( 'parsec',                     'light-year' )                          : mpmathify( '3.261563776971' ),
    ( 'pascal',                     'barye' )                               : mpmathify( '10' ),
    ( 'pascal',                     'kilogram/meter*second^2' )             : mpmathify( '1' ),
    ( 'peck',                       'dry_gallon' )                          : mpmathify( '2' ),
    ( 'pennyweight',                'gram' )                                : mpmathify( '1.55517384' ),
    ( 'perch',                      'foot' )                                : mpmathify( '16.5' ),
    ( 'pferdestarke',               'watt' )                                : mpmathify( '735.49875' ),
    ( 'pfund',                      'gram' )                                : mpmathify( '500' ),
    ( 'phot',                       'lux' )                                 : mpmathify( '10000' ),
    ( 'piccolo',                    'liter' )                               : mpmathify( '0.1875' ),
    ( 'pieze',                      'pascal' )                              : mpmathify( '1000' ),
    ( 'pointangle',                 'degree' )                              : fdiv( 360, 32 ),
    ( 'poise',                      'kilogram/meter*second' )               : mpmathify( '10' ),
    ( 'poise',                      'pascal*second' )                       : mpmathify( '10' ),
    ( 'poncelet',                   'watt' )                                : mpmathify( '980.665' ),
    ( 'pony',                       'dram' )                                : mpmathify( '6' ),
    ( 'pood',                       'dolya' )                               : mpmathify( '368640' ),
    ( 'portuguese_almude',          'liter' )                               : mpmathify( '16.7' ),
    ( 'potrzebie',                  'farshimmelt_potrzebie' )               : mpmathify( '1.0e5' ),
    ( 'potrzebie',                  'furshlugginer_potrzebie' )             : mpmathify( '1.0e-6' ),
    ( 'potrzebie',                  'meter' )                               : mpmathify( '0.002263348517438173216473' ),  # see Mad #33
    ( 'pottle',                     'imperial_quart' )                      : mpmathify( '2' ),
    ( 'pound',                      'grain' )                               : mpmathify( '7000' ),
    ( 'pound',                      'ounce' )                               : mpmathify( '16' ),
    ( 'pound',                      'sheet' )                               : mpmathify( '700' ),
    ( 'pound-force',                'newton' )                              : mpmathify( '4.4482216152605' ),
    ( 'psi',                        'pascal' )                              : mpmathify( '6894.75728' ),      # approx.
    ( 'pyad',                       'inch' )                                : mpmathify( '7' ),
    ( 'pyad',                       'vershok' )                             : mpmathify( '4' ),
    ( 'quad',                       'btu' )                                 : mpmathify( '10e15' ),
    ( 'quadrant',                   'degree' )                              : mpmathify( '90' ),
    ( 'quadrillion',                'unity' )                               : mpmathify( '1.0e15' ),
    ( 'quart',                      'cup' )                                 : mpmathify( '4' ),
    ( 'quart',                      'liter' )                               : mpmathify( '0.946352946' ),
    ( 'quart',                      'pint' )                                : mpmathify( '2' ),
    ( 'quattuordecillion',          'unity' )                               : mpmathify( '1.0e45' ),
    ( 'quindecillion',              'unity' )                               : mpmathify( '1.0e48' ),
    ( 'quintal',                    'gram' )                                : mpmathify( '100000' ),
    ( 'quintant',                   'degree' )                              : mpmathify( '72' ),
    ( 'quintillion',                'unity' )                               : mpmathify( '1.0e18' ),
    ( 'qword',                      'bit' )                                 : mpmathify( '64' ),
    ( 'rack_unit',                  'meter' )                               : mpmathify( '0.0445' ),
    ( 'radian',                     'centrad' )                             : mpmathify( '100' ),
    ( 'radian',                     'degree' )                              : fdiv( 180, pi ),
    ( 'reaumur',                    'degree_newton' )                       : fdiv( 33, 80 ),
    ( 'reed',                       'foot' )                                : mpmathify( '9' ),
    ( 'rehoboam',                   'liter' )                               : mpmathify( '4.5' ),
    ( 'reynolds',                   'pascal*second' )                       : mpmathify( '6894.75729' ),
    ( 'rod',                        'foot' )                                : mpmathify( '16.5' ),
    ( 'roentgen',                   'rad' )                                 : mpmathify( '0.877' ),
    ( 'rood',                       'foot^2' )                              : mpmathify( '10890' ),
    ( 'rope',                       'foot' )                                : mpmathify( '20' ),
    ( 'rutherford',                 'becquerel' )                           : mpmathify( '1.0e6' ),
    ( 'rydberg',                    'joule' )                               : mpmathify( '2.17987232498e-18' ),
    ( 'salmanazar',                 'liter' )                               : mpmathify( '9.0' ),
    ( 'sazhen',                     'meter' )                               : mpmathify( '2.1336' ),
    ( 'score',                      'unity' )                               : mpmathify( '20' ),
    ( 'scruple',                    'minim' )                               : mpmathify( '20' ),
    ( 'second',                     '1/hertz' )                             : mpmathify( '1' ),
    ( 'second',                     'jiffy' )                               : mpmathify( '100' ),
    ( 'second',                     'shake' )                               : mpmathify( '1.0e8' ),
    ( 'second',                     'svedberg' )                            : mpmathify( '1.0e13' ),
    ( 'section',                    'acre' )                                : mpmathify( '640' ),
    ( 'septendecillion',            'unity' )                               : mpmathify( '1.0e54' ),
    ( 'septillion',                 'unity' )                               : mpmathify( '1.0e24' ),
    ( 'seven',                      'unity' )                               : mpmathify( '7' ),
    ( 'seventeen',                  'unity' )                               : mpmathify( '17' ),
    ( 'seventy',                    'unity' )                               : mpmathify( '70' ),
    ( 'sexdecillion',               'unity' )                               : mpmathify( '1.0e51' ),
    ( 'sextant',                    'degree' )                              : mpmathify( '60' ),
    ( 'sextillion',                 'unity' )                               : mpmathify( '1.0e21' ),
    ( 'shock',                      'unity' )                               : mpmathify( '60' ),
    ( 'sidereal_day',               'second' )                              : mpmathify( '86164.0905' ),   # https://en.wikipedia.org/wiki/Sidereal_time
    ( 'sidereal_day',               'sidereal_hour' )                       : mpmathify( '24' ),
    ( 'sidereal_hour',              'sidereal_minute' )                     : mpmathify( '60' ),
    ( 'sidereal_minute',            'sidereal_second' )                     : mpmathify( '60' ),
    ( 'siemens',                    'ampere^2*second^3/kilogram*meter^2' )  : mpmathify( '1' ),
    ( 'siemens',                    'statsiemens' )                         : mpmathify( '898755178736.5' ),
    ( 'sievert',                    'rem' )                                 : mpmathify( '100' ),
    ( 'siriometer',                 'astronomical_unit' )                   : mpmathify( '1.0e6' ),
    ( 'six',                        'unity' )                               : mpmathify( '6' ),
    ( 'sixteen',                    'unity' )                               : mpmathify( '16' ),
    ( 'skein',                      'foot' )                                : mpmathify( '360' ),
    ( 'skot',                       'bril' )                                : mpmathify( '1.0e4' ),
    ( 'skot',                       'lambert' )                             : mpmathify( '1.0e7' ),
    ( 'slug',                       'pound' )                               : mpmathify( '32.174048556' ),
    ( 'slug',                       'slinch' )                              : mpmathify( '12' ),
    ( 'smoot',                      'inch' )                                : mpmathify( '67' ),
    ( 'snit',                       'jigger' )                              : mpmathify( '2' ),
    ( 'solomon',                    'liter' )                               : mpmathify( '20.0' ),
    ( 'sovereign',                  'liter' )                               : mpmathify( '25.0' ),
    ( 'span',                       'inch' )                                : mpmathify( '9' ),
    ( 'spanish_almude',             'liter' )                               : mpmathify( '4.625' ),
    ( 'speed_of_sound',             'meter/second' )                        : mpmathify( '343' ),
    ( 'sphere',                     'hemisphere' )                          : mpmathify( '2' ),
    ( 'sphere',                     'steradian' )                           : fmul( 4, pi ),
    ( 'square_arcminute',           'square_arcsecond' )                    : mpmathify( '3600' ),
    ( 'square_degree',              'square_arcminute' )                    : mpmathify( '3600' ),
    ( 'square_octant',              'square_degree' )                       : mpmathify( '2025' ),
    ( 'square_quadrant',            'square_degree' )                       : mpmathify( '8100' ),
    ( 'square_quintant',            'square_degree' )                       : mpmathify( '5184' ),
    ( 'square_sextant',             'square_degree' )                       : mpmathify( '3600' ),
    ( 'stadium',                    'foot' )                                : mpmathify( '606.95' ),
    ( 'standard',                   'liter' )                               : mpmathify( '0.75' ),
    ( 'stapp',                      'meter/second^3' )                      : mpmathify( '9.80665' ),
    ( 'statcoulomb',                'coulomb' )                             : mpmathify( '3.335641e-10' ),  # 0.1A*m/c, approx.
    ( 'statcoulomb',                'franklin' )                            : mpmathify( '1' ),
    ( 'stathenry',                  'henry' )                               : mpmathify( '898755178740' ),
    ( 'statmho',                    'siemens' )                             : mpmathify( '8.99e11' ),
    ( 'statohm',                    'ohm' )                                 : mpmathify( '898755178740' ),
    ( 'statvolt',                   'volt' )                                : fdiv( 299792458, 1000000 ),
    ( 'steradian',                  'radian^2' )                            : mpmathify( '1' ),
    ( 'steradian',                  'square_degree' )                       : power( fdiv( 180, pi ), 2 ),
    ( 'steradian',                  'square_grad' )                         : power( fdiv( 200, pi ), 2 ),
    ( 'stere',                      'liter' )                               : mpmathify( '1000' ),
    ( 'sthene',                     'newton' )                              : mpmathify( '1000' ),
    ( 'stilb',                      'candela/meter^2' )                     : mpmathify( '10000' ),
    ( 'stone',                      'pound' )                               : mpmathify( '14' ),
    ( 'stone_us',                   'pound' )                               : mpmathify( '12.5' ),
    ( 'strike',                     'imperial_bushel' )                     : mpmathify( '2' ),
    ( 'sydharb',                    'liter' )                               : mpmathify( '5.62e11' ),
    ( 'tablespoon',                 'teaspoon' )                            : mpmathify( '3' ),
    ( 'teaspoon',                   'coffeespoon' )                         : mpmathify( '2' ),
    ( 'teaspoon',                   'dash' )                                : mpmathify( '8' ),
    ( 'teaspoon',                   'pinch' )                               : mpmathify( '16' ),
    ( 'teaspoon',                   'saltspoon' )                           : mpmathify( '4' ),
    ( 'teaspoon',                   'smidgen' )                             : mpmathify( '32' ),
    ( 'ten',                        'unity' )                               : mpmathify( '10' ),
    ( 'tesla',                      'gauss' )                               : mpmathify( '10000' ),
    ( 'tesla',                      'kilogram/ampere*second^2' )            : mpmathify( '1' ),
    ( 'therm',                      'btu' )                                 : mpmathify( '100000' ),
    ( 'thirty',                     'unity' )                               : mpmathify( '30' ),
    ( 'thousand',                   'unity' )                               : mpmathify( '1000' ),
    ( 'three',                      'unity' )                               : mpmathify( '3' ),
    ( 'toe',                        'calorie' )                             : mpmathify( '1.0e10' ),
    ( 'ton',                        'pound' )                               : mpmathify( '2000' ),
    ( 'tonne',                      'gram' )                                : mpmathify( '1.0e6' ),
    ( 'ton_of_coal',                'joule' )                               : mpmathify( '29.288e9' ),
    ( 'ton_of_TNT',                 'joule' )                               : mpmathify( '4.184e9' ),
    ( 'ton_of_TNT',                 'pound_of_TNT' )                        : mpmathify( '2000' ),
    ( 'torr',                       'mmHg' )                                : mpmathify( '1' ),
    ( 'township',                   'acre' )                                : mpmathify( '23040' ),
    ( 'tredecillion',               'unity' )                               : mpmathify( '1.0e42' ),
    ( 'trillion',                   'unity' )                               : mpmathify( '1.0e12' ),
    ( 'trit',                       'nat' )                                 : log( 3 ),
    ( 'tropical_month',             'day' )                                 : mpmathify( '27.321582' ),
    ( 'troy_ounce',                 'gram' )                                : mpmathify( '31.1034768' ),
    ( 'troy_pound',                 'pound' )                               : mpmathify( '12' ),
    ( 'tryte',                      'trit' )                                : mpmathify( '6' ),   # as defined by the Setun computer
    ( 'tun',                        'gallon' )                              : mpmathify( '252' ),
    ( 'tun',                        'pipe' )                                : mpmathify( '2' ),
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
    ( 'usb1',                       'bit/second' )                          : mpmathify( '1.2e7' ),
    ( 'usb2',                       'bit/second' )                          : mpmathify( '2.8e8' ),
    ( 'usb3.0',                     'bit/second' )                          : mpmathify( '5.0e9' ),
    ( 'usb3.1',                     'bit/second' )                          : mpmathify( '1.0e10' ),
    ( 'versta',                     'meter' )                               : mpmathify( '1066.8' ),
    ( 'vigintillion',               'unity' )                               : mpmathify( '1.0e63' ),
    ( 'virgate',                    'bovate' )                              : mpmathify( '30' ),
    ( 'volt',                       'abvolt' )                              : mpmathify( '1.0e8' ),
    ( 'volt',                       'kilogram*meter^2/ampere*second^3' )    : mpmathify( '1' ),
    ( 'watt',                       'kilogram*meter^2/second^3' )           : mpmathify( '1' ),
    ( 'watt',                       'lusec' )                               : mpmathify( '7500' ),
    ( 'weber',                      'kilogram*meter^2/ampere*second^2' )    : mpmathify( '1' ),
    ( 'weber',                      'maxwell' )                             : mpmathify( '1.0e8' ),
    ( 'weber',                      'unit_pole' )                           : mpmathify( '7957747.154594' ),
    ( 'week',                       'day' )                                 : mpmathify( '7' ),
    ( 'wey',                        'pound' )                               : mpmathify( '252' ),
    ( 'wine_barrel',                'wine_gallon' )                         : mpmathify( '31.5' ),
    ( 'wine_butt',                  'wine_gallon' )                         : mpmathify( '126' ),
    ( 'wine_gallon',                'gallon' )                              : mpmathify( '1' ),
    ( 'wine_hogshead',              'gallon' )                              : mpmathify( '63' ),
    ( 'wine_tun',                   'gallon' )                              : mpmathify( '252' ),
    ( 'wine_tun',                   'puncheon' )                            : mpmathify( '3' ),
    ( 'wine_tun',                   'rundlet' )                             : mpmathify( '14' ),
    ( 'wine_tun',                   'tierce' )                              : mpmathify( '6' ),
    ( 'wood',                       'martin' )                              : mpmathify( '100' ),
    ( 'word',                       'bit' )                                 : mpmathify( '16' ),
    ( 'yard',                       'foot' )                                : mpmathify( '3' ),
    ( 'year',                       'day' )                                 : mpmathify( '365.25' ),   # Julian year = 365 and 1/4 days
    ( 'zentner',                    'gram' )                                : mpmathify( '50000' ),
    ( 'zolotnik',                   'dolya' )                               : mpmathify( '96' ),
}

