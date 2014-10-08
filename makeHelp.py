#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeHelp
#//
#//  RPN command-line calculator help file generator
#//  copyright (c) 2014, Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import bz2
import contextlib
import pickle
import os

from rpnDeclarations import *
from rpnVersion import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


#//******************************************************************************
#//
#//  basic help categories
#//
#//******************************************************************************

basicCategories = {
'options' :
'rpn ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE + '\n\n' +
'''
command-line options:

    -a [n], --output_accuracy [n]
        maximum number of decimal places to display, irrespective of internal
        precision (default: ''' + str( defaultAccuracy ) + ')' + '''

    -b n : --input_radix n
        specify the radix for input (default: ''' + str( defaultInputRadix ) + ')' + '''

    -c, --comma -
        add commas to result, e.g., 1,234,567.0

    -d [n], --decimal_grouping [n] -
        display decimal places separated into groups (default: ''' + str( defaultDecimalGrouping ) + ')' + '''

    -g [n], --integer_grouping [n]
        display integer separated into groups (default: ''' + str( defaultIntegerGrouping ) + ')' + '''

    -h, --help -
        displays basic help information

    -i, --identify
        identify the result (may repeat input)

    -l n, -- line_length
        line length to use for formatting help (default: 80)

    -n str, --numerals str
        characters set to use as numerals for output

    -o, --octal
        octal mode: equivalent to \'-r8 -w9 -i3 -z\'

    -p n, --precision n
        precision, i.e., number of significant digits to use

    -r n, --output_radix n
        output in a different base (2 to 62, or phi)

    -R n, --output_radix_numerals n
        output each digit is a space-delimited base-10 number

    -t, --time
        display calculation time

    -u, --find_poly
        find a polynomial such that P(x) ~= 0 of degree <= N (default: 1000)

    -w [n], --bitwise_group_size [n]
        bitwise operations group values by this size (default: ''' + str( defaultBitwiseGroupSize ) + ')' + '''

    -x, --hex
        hex mode: equivalent to '-r16 -w16 -i4 -z'

    -z, --leading_zero
        add leading zeros if needed with -g

    -!, --print_options
        print values for all options
''',
'arguments' :
'''
Arguments:

    As its name implies, rpn uses Reverse Polish Notation, otherwise referred
    to as postfix notation.  The operand(s) come first and then the operator.
    This notation works without the need for parentheses.  rpn supports
    brackets for creating lists of operands, but this serves a different
    purpose and is described later.

    Some simple examples:

    2 + 2:
        rpn 2 2 +

    3 sqrt(2) / 4:
        rpn 3 2 sqrt * 4 /

    Lists are specified using the bracket operators.  Most operators can take
    lists as operands, which results in the operation being performed on each
    item in the list.  If the operator takes two operands, then either operand
    can be a list.  If one operand is a list and the other is a single value,
    then each value in the list will have the single operand applied to it
    with the operator, and the result will be displayed as a list.

    It is possible in certain cases to nest lists.  rpn tries to figure out
    a logical way (and unequivocal) to apply the operators to the operands.

    *** Special note:  I have not exhaustively tested every possible
    scenario with lists, but in general, if it makes sense, rpn will work
    correctly.

    For example:

    c:\>rpn [ 2 3 4 5 6 ] 10 +
    [ 12, 13, 14, 15, 16, 17 ]

    c:\>rpn 7 [ 1 2 3 4 5 6 7 ] *
    [ 7, 14, 21, 28, 35, 42, 49 ]

    If both operands are lists, then each element from the first list is
    applied to the corresponding element in the second list.  If one list
    is shorter than the other, then only that many elements will have the
    operator applied and the resulting list will only be as long as the
    shorter list.

    For example:

    rpn [ 1 2 3 4 5 6 7 ] [ 1 2 3 4 5 6 7 ] **
    [ 1, 4, 27, 256, 3125, 46656, 823543 ]

    rpn [ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *
    [ 30, 40, 90, 160 ]

    Some operators take lists as operands 'natively'.  This means the operator
    requires a list, because the operation does not make sense for a single
    value.  For example, 'mean' averages the values of a list.  If the
    required list argument is a single value, rpn will promote it to a list.

    For example:

    c:\>rpn [ 1 2 3 ] [ 4 5 6 ] polyval
    [ 27, 38, 51 ]

''',
'input' :
'''
    For integers, rpn understands hexidecimal input of the form '0x....'.

    A number consisting solely of 0s and 1s with a trailing 'b' or 'B' is
    interpreted as binary.

    Otherwise, a leading '0' is interpreted as octal.

    Decimal points are not allowed for binary, octal or hexadecimal modes,
    but fractional numbers in bases other than 10 can be input using -b.

    A leading '\\' forces the term to be a number rather than an operator (for
    use with higher bases with -b).
''',
'output' :
'''
    [ TODO: describe output formats supported by rpn ]
''',
'time_features' :
'''
    [ TODO: describe time features supported by rpn ]

For now, here are some examples:

    operators:
        c:\>rpn now
        2014-09-02 13:36:28

        c:\>rpn today
        2014-09-02 00:00:00

    ISO-8601 format ("YYYY-MM-DD[T| ][HH:mm:SS]", no timezones):
        c:\>rpn 2014-09-02T13:36:28
        2014-09-02 13:36:28

        c:\>rpn "2014-09-02 13:36:28"
        2014-09-02 13:36:28

        c:\>rpn 2014-09-02
        2014-09-02 00:00:00

    'maketime' operator:
        c:\>rpn [ 2014 ] maketime
        2014-01-01 00:00:00

        c:\>rpn [ 2014 9 ] maketime
        2014-09-01 00:00:00

        c:\>rpn [ 2014 9 2 ] maketime
        2014-09-02 00:00:00

        c:\>rpn [ 2014 9 2 13 ] maketime
        2014-09-02 13:00:00

        c:\>rpn [ 2014 9 2 13 36 ] maketime
        2014-09 02 13:36:00

        c:\>rpn [ 2014 9 2 13 36 28 ] maketime
        2014-09-02 13:36:28

    How many days old am I?
        c:\>rpn today 1965-03-31 -
        18052 days

    When will I be 20,000 days old?
        c:\>rpn 1965-03-31 20000 days +
        2020-01-02 00:00:00

    How many seconds old am I (to within an hour or so)?
        c:\>rpn -c now "1965-03-31 05:00:00" - seconds convert
        1,559,739,194.098935 seconds

    What day of the week was I born on?
        c:\>rpn 1965-03-31 weekday
        'Wednesday'

    How many days until Christmas?
        c:\>rpn 2014-12-25 today -
        114 days

    How many days older am I than my first child?
        c:\>rpn 1994-03-06 1965-03-31 -
        10567 days

    What date is 4 weeks from now?
        c:\>rpn today 4 weeks +
        2014-09-30 00:00:00

    What date is 4 months from now?
        c:\>rpn today 4 months +
        2015-01-02 00:00:00

    What about 6 months from 2 days ago?
        c:\>rpn today 2 days - 6 months +
        2015-02-28 00:00:00

    There is no February 30, so we use the real last day of the month.  Months
    are handled differently from the other time units with respect to time math
    because they can differ in length.

    However, the month as an absolute unit of time is simply equated to 30
    days:
        c:\>rpn month days convert
        30 days
''',
'user_functions' :
'''
    [ TODO: finish explaining user-defined formulas ]

Allows the user to define a function for use with the eval, nsum, nprod,
limit and limitn operators, etc.  Basically 'x' starts an expression that
becomes a function.  Right now (5.28.0), a user-defined function must start
with 'x', but I hope to remove that limitation soon.

Some examples:

c:\>rpn 3 x 2 * eval
6

c:\>rpn 5 x 2 ** 1 - eval
24

c:\>rpn inf x 1 + fib x fib / limit
1.6180339887

Here is the kludge to work around having to have 'x' be first:

c:\>rpn 1 inf x 0 * 2 x ** + 1/x nsum
1

Basically, all you have to do is add x * 0 to the expression.  It's cheesy,
but it works for now.
''',
'unit_conversion' :
'''
    [ TODO: describe unit conversions in rpn ]

For now, here are some examples:

c:\>rpn 10 miles km convert
16.0934399991 kilometers

c:\>rpn 2 gallons cups convert
32 cups

c:\>rpn 153 pounds stone convert
10.9285714286 stone

c:\>rpn 10 miles km convert
16.0934399991 kilometers

c:\>rpn 65 mph kph convert
104.60736 kilometers/hour

c:\>rpn 60 miles hour / furlongs fortnight / convert
161280 furlongs per fortnight

c:\>rpn barn gigaparsec * cubic_inch convert
188.2995990804 cubic inches

c:\>rpn mars_day hms
[ 24 hours, 37 minutes, 22.6631999991 seconds ]

c:\>rpn 10 tons estimate
'approximately 1.65 times the mass of an average male African bush elephant'

c:\>rpn 78 kg [ pound ounce ] convert
[ 171 pounds, 15.3690320673 ounces ]

c:\>rpn 150,000 seconds [ day hour minute second ] convert
[ 1 day, 17 hours, 39 minutes, 59.9999999991 seconds ]

Here's a shortcut for "[ day hour minute second ] convert":

c:\>rpn 150,000 seconds dhms
[ 1 day, 17 hours, 39 minutes, 59.9999999991 seconds ]

Yes, I'd really like to do something about that rounding error.


Help topics for individual units is coming someday, but not today.
''',
'about' :
PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' +
COPYRIGHT_MESSAGE + '''

rpn is a command-line Reverse-Polish Notation calculator that was first
written in C in 1988.  It was rewritten in Python 3 in 2012 and now uses the
mpmath library.
''',
'bugs' :
'''
-u doesn't work with complex numbers

Polynomials should support being taken to positive integral powers, but don't
yet.

I also want to support taking units to integral powers, but it doesn't yet.

This requires implicit conversion between unit types, and doesn't work yet:
    rpn -D 16800 mA hours * 5 volts * joule convert

Unit conversion suffers from small rounding errors in some situations.  This
is unavoidable to a certain extent, but it's worse than I think it should be.

In general, I've been doing better testing for 5.28.0, and it's not done yet,
but I wanted to push a release anyway.
''',
'release_notes' :
'''
5.18.1

It's clear I haven't done any unit conversions in a while because there were
still issues with declarations of variables.  Now, I've started eliminating
the use of "global" in favor of a global module.

5.18.2

Made a bunch of bug fixes that showed up as a result of reorganizing the code.

5.18.3

Added 'split' as an alias for 'unpack' because I couldn't remember what it was
called.

Made some minor fixes made based on running pyflakes, pylint pep8, and the
test script.

5.18.4

rpn now correctly parses "-0" as a value again.

5.18.5

Fixed a bug concerning adding dissimilar units.

5.18.6

rpn now prints out an error message if you try to get help for an unknown
topic.

5.18.7

compoundUnits was still being referred to without the "g." global specifier.

5.19.0

Added 'randint' operator.

5.19.1

Fixed several problems with 'tounixtime' and 'fromunixtime'.

5.19.2

rpn now outputs an empty list correctly.  The 'append' operator (to append
lists) has been fixed.

The first version of a test script is available as a batch file.

5.19.3

The test script has been rewritten in Python.  It's still very basic and only
does a sanity test to show every operator works without crashing.  It doesn't
test for correct answers yet.

5.20.0

rpn finally comes with an installer for Windows, in 32-bit and 64-bit flavors.

5.20.1

Several calls to polyval( ) had hard-coded fractions in them instead of calls
to fdiv( ), resulting in rounding errors.

5.20.2

Fixed the list operator parsing so polyprod and polysum work correctly.

5.20.3

Made a fix to improve rpn's reporting of the argument in question when there
is an error.  It's probably not 100% correct yet.

5.20.4

rpn now correctly reports the argument in question on any error.

5.20.5

rpn now throws an error when attempting to get the 0th or less prime number.

5.20.6

The prime? operator wasn't working correctly for small values.

5.20.7

Added help for unit types.   Help for individual units will come eventually,
but they are pretty self-explanatory.

5.21.0

The long-awaited absolute time feature:  rpn can now handle absolute time
values.  For input, just use ISO 8601 format, or a reasonable subset thereof.
There is also the 'maketime' operator, which takes a list similar to the old
'tounixtime' operator.

5.21.1

Added percent operator, weekday now throws a proper error is the operand isn't
a time value.

5.21.2

Added -l to format help output for different line lengths.  However, it still
doesn't format the blockquoted help text.

5.22.0

Added a bunch of new constants for powers of 10.

5.23.0

Help will now search topics for partial matches if a complete match isn't found.

5.23.1

The help improvements actually work now.  So much for testing.

There are now some examples of absolute time handling.

5.24.0

A few more bug fixes, plus new calendar-related operators:  easter.
election_day, labor_day, memorial_day, nthday, presidents_day, thanksgiving

5.25.0

Added Julian date operators, ISO date operators, calendar operators and the
'ash_wednesday' operator.  Added support for the density unit type and
several small bug fixes.

5.26.0

Added dynamic_visocity and frequency unit types and a few bug fixes.

Added units for the days and years of the other 8 planets in the Solar System.

Added several constant units for quaint or archaic number terms like 'score'
and 'gross'.

Added mass units for common particle masses.

Updated some natural values (electron mass, etc.).

Fixed some problems with generating and interpreting compound units.

Added the 'prevost' operator.

5.27.0

Added the 'name' operator.

5.27.1

Added an error message if the 'name' operand is out of range, and added
support for negative numbers.

5.27.2

Help for unit types now prints out all aliases for the unit operators.

5.28.0

Added 'x', 'eval', 'nsum', 'nprod', 'limit', 'limitn', 'infinity', and
'negative_infinity', and 'value' operators.

5.28.1

Added separate installers for the plain-vanilla rpn (with only the "small
primes" data file, i.e., the first million primes), and the installer with all
of the prime data files.

The 'primes' operator has been fixed so it works correctly for small values.

I'm currently testing the prime functions, which I haven't touched in a long
time, so more fixes will definitely be coming.  The balanced prime functions
are currently broken and will be fixed shortly, including updated data files.

5.28.2

Several bug fixes relating to 'estimate' and unit conversion.   Some unit
types were folded together because they had the same basic units (e.g.,
frequency and radioactivity were both time ^ -1, which confused the conversion
logic).

5.28.3

The operators 'doublebal', doublebal_', 'triplebal', and 'triplebal_' now work
correctly.  The data files have been significantly expanded as well.

5.28.4

Added the 'diffs2' operator.

More bug fixes thanks to the test script!
''',
'license' :
'''
rpn is licensed under the GPL, version 3.0 and is ''' +

'\n' + COPYRIGHT_MESSAGE +

'''

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/gpl.html> for more information.
''',
'examples' :
'''
Here are some examples of using rpn:

Basic arithmetic operations:

    c:\>rpn 2 3 +
    5

    c:\>rpn 12 9 -
    3

    c:\>rpn 23 47 *
    1081

    c:\>rpn 10 7 /
    1.4285714286

Basic trigonometry usage:

    c:\>rpn 60 deg sin         # sine of 60 degrees
    0.8660254038

    c:\>rpn 45 deg tan         # tangent of 45 degrees
    1

    c:\>rpn 2 pi * rad         # 2 pi radians is how many degrees?
    360

    c:\>rpn 2 atan rad         # What angle (in degrees) has a slope of 2?
    63.4349488229

Convert an IP address to a 32-bit value and back:

    c:\>rpn -x [ 192 168 0 1 ] 256 base
    c0a8 0001

    c:\>rpn -R 256 0xc0a80001
    192 168 0 1

Construct the square root of two from a continued fraction:

    First, here's the square root of two to 20 places:

        c:\>rpn -a20 2 sqrt
        1.41421356237309504880

    Now let's make a continued fraction from that, calculated to 20 terms.

        c:\>rpn 2 sqrt 20 makecf
        [ 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ]

    Here's the nearest fractional approximation of the square root of two:

        c:\>rpn 2 sqrt 20 frac
        [ 22619537, 15994428 ]

    And we can calculate the square root of two from the continued fraction.
    In reality, the continued fraction representation of the square root of
    two is infinite, so this is only an approximation.

        c:\>rpn -a20 [ 1 2 30 dup ] cf
        1.41421356237309504880

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        c:\>rpn 1 50 range fib isprime nonzero 1 + fib
        [ 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437, 2971215073 ]

    Which of the first thousand pentagonal numbers are also triangular:
        c:\>rpn 1000 pent tri?
        1731.26218055

    So the thousandth pentagonal number is a little bigger than the 1731st
    triangular number.  That tells us how many triangular numbers to look at.

        c:\>rpn 1 1000 range pent 1 1732 range tri intersection
        [ 1, 210, 40755 ]

    So, 1, 210, and 40755 are triangular and pentagonal.

    Which triangular numbers are those?
        c:\>rpn 1 1000 range pent 1 1732 range tri intersection tri?
        [ 1, 20, 285 ]

    The first, 20th, and 285th.

    Which pentagonal numbers are those?
        c:\>rpn 1 1000 range pent 1 1732 range tri intersection pent?
        [ 1, 12, 165 ]

    The first, 12th, and 165th pentagonal numbers are also triangular.

    Calculate the first 10 Fibonacci numbers without using the 'fib' operator:
        c:\>rpn [ 1 1 ] 1 1 10 range linearrecur
        [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55 ]

Calculations with absolute time:

    operators:
        c:\>rpn now
        2014-09-02 13:36:28

        c:\>rpn today
        2014-09-02 00:00:00

    ISO-8601 format ("YYYY-MM-DD[T| ][HH:mm:SS]", no timezones):
        c:\>rpn 2014-09-02T13:36:28
        2014-09-02 13:36:28

        c:\>rpn "2014-09-02 13:36:28"
        2014-09-02 13:36:28

        c:\>rpn 2014-09-02
        2014-09-02 00:00:00

    'maketime' operator:
        c:\>rpn [ 2014 ] maketime
        2014-01-01 00:00:00

        c:\>rpn [ 2014 9 ] maketime
        2014-09-01 00:00:00

        c:\>rpn [ 2014 9 2 ] maketime
        2014-09-02 00:00:00

        c:\>rpn [ 2014 9 2 13 ] maketime
        2014-09-02 13:00:00

        c:\>rpn [ 2014 9 2 13 36 ] maketime
        2014-09 02 13:36:00

        c:\>rpn [ 2014 9 2 13 36 28 ] maketime
        2014-09-02 13:36:28

    How many days old am I?
        c:\>rpn today 1965-03-31 -
        18052 days

    When will I be 20,000 days old?
        c:\>rpn 1965-03-31 20000 days +
        2020-01-02 00:00:00

    How many seconds old am I (to within an hour or so)?
        c:\>rpn -c now "1965-03-31 05:00:00" - seconds convert
        1,559,739,194.098935 seconds

    What day of the week was I born on?
        c:\>rpn 1965-03-31 weekday
        'Wednesday'

    How many days until Christmas?
        c:\>rpn 2014-12-25 today -
        114 days

    How many days older am I than my first child?
        c:\>rpn 1994-03-06 1965-03-31 -
        10567 days

    What date is 4 weeks from now?
        c:\>rpn today 4 weeks +
        2014-09-30 00:00:00

    What date is 4 months from now?
        c:\>rpn today 4 months +
        2015-01-02 00:00:00

    What about 6 months from 2 days ago?
        c:\>rpn today 2 days - 6 months +
        2015-02-28 00:00:00

    There is no February 30, so we use the real last day of the month.  Months
    are handled differently from the other time units with respect to time math
    because they can differ in length.

    However, the month as an absolute unit of time is simply equated to 30
    days:
        c:\>rpn month days convert
        30 days

Unit conversions:

    Unit conversions should be very intuitive.

        c:\>rpn 10 miles km convert
        16.0934399991 kilometers

        c:\>rpn 2 gallons cups convert
        32 cups

        c:\>rpn 153 pounds stone convert
        10.9285714286 stone

    rpn supports compound units:

        c:\>rpn 65 miles hour / meters second / convert
        29.0575999991 meters per second

        c:\>rpn 65 miles hour / furlongs fortnight / convert
        174720 furlongs per fortnight

    rpn can handle combinations of different types of units, but sometimes
    it needs help to get them into meaningful terms.

        c:\>rpn G
        1 standard gravity

        c:\>rpn G 10 seconds *
        10 standard gravities seconds

        c:\>rpn G 10 seconds * ft s / convert
        321.7404855643 feet per second

    [ TODO:  finish unit conversion examples ]

Advanced examples:

Please note that several of the following commands are broken up into multiple
lines for readability, but all of them are single commands to rpn.

In some commands, the precision is explicitly set such to limit the output to
what is accurately calculated.   If there are alternate versions to calculate
the value, the same precision is used.

Calculation (or approximation) of various mathematical constants:

    Polya Random Walk Constant
        = rpn -p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 /
                    gamma 7 24 / gamma 11 24 / gamma ] prod 1/x * -

    Schwartzchild Constant (Conic Constant)
        = rpn -a20 2 0 30 range ** 0 30 range ! / sum
        = rpn e 2 **

    Somos\' Quadratic Recurrence Constant
        = rpn -a20 1 100 range 0.5 0.5 100 georange ** prod

    Prevost Constant
        = rpn -a20 1 100 range fib 1/x sum

    Euler's number = rpn -a20 0 100 range fac 1/x sum
                   = rpn -a20 e

    Gelfond Constant
        = rpn -a20 pi 0 100 range power 0 100 range ! / sum
        = rpn -a20 e pi power

    Bloch-Landau Constant
        = rpn -a20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /

    Hausdorff Dimension
        = rpn -a20 2 0 100 range 2 * 1 + power 0 100 range 2 * 1 + *
            1/x sum 3 0 100 range 2 * 1 + power 0 100 range 2 * 1 +
            * 1/x sum /
        = rpn -a20 3 log 2 log /

    Machin-Gregory Series
        = rpn -a20 1 1000 2 range2 2 1 1000 2 range2 power * 1/x altsum
        = rpn -a20 1 2 / atan

    Beta( 3 )
        = rpn -a17 1 1000000 2 range2 3 power 1/x altsum
        = rpn -a17 pi 3 power 32 /

    Cahen's constant
        = rpn -a20 1 20 range sylvester 1 - 1/x altsum

    Lemniscate Constant
        = rpn 4 2 pi / sqrt * 0.25 ! sqr *

    sqrt( e )
        = rpn -a20 2 0 20 range power [ 0 20 range ] ! * 1/x sum
        = rpn -a20 0 20 range 2 * !! 1/x sum
        = rpn -a20 e sqrt

    1/e
        = rpn -a20 0 25 range fac 1/x altsum
        = rpn -a20 e 1/x

    Zeta( 6 )           goobles - look into this!
        = rpn -a20 -p30 1 1 1000 primes -6 power - 1/x prod
        = rpn -a20 pi 6 power 945 /
        = rpn -a20 6 zeta

    Pythagoras' constant
        = rpn -a20 [ 1 2 25 dup ] cf
        = rpn -a20 2 sqrt

    Digamma
        = rpn -p25 -a20 1 1 1000 primes -6 power - 1/x prod
        = rpn -a5 [ 0 100000 range ] 1 + 1/x
                        [ 0 100000 range ] 1 4 / + 1/x - sum euler -

    Strongly Carefree Constant
        = rpn -a6 1 1 100000 primes 3 * 2 - 1 100000 primes 3 power / - prod
        = rpn -a7 6 pi sqr / 1 2
                1 100000 primes 1 100000 primes 1 + * 1/x * - prod *

    Ramanujan-Forsythe Constant
        = rpn 0 100000 range 2 * 3 - fac2 0 100000 range 2 * fac2 / sqr sum

    Apery's Constant
        = rpn -a20 1 5000 range 3 power 1/x sum
        = rpn -a20 3 zeta
        = rpn -a20 apery

    Omega Constant
        = rpn -a20 [ e 1/x 100 dup ] tower
        = rpn -a20 omega

    Liouville Number
        = rpn -a120 10 1 10 range ! power 1/x sum

    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                0 100000 range 3 * 2 + sqr 1/x sum -
                1 100000 range 3 * 1 + sqr 1/x sum + *

    Hafner-Sarnak-McCurley Constant (2)
        = rpn -a7 1 1 100000 primes sqr 1/x - prod
        = rpn 2 zeta 1/x

    Infinite Tetration of i
        = rpn -a20 [ 1 i 1000 dup ] tower
''',
'notes' :
'''
When converting fractional output to other bases, rpn adjusts the precision
to the approximate equivalent for the new base since the precision is
applicable to base 10.

Tetration (hyperexponentiation) forces the second argument to an integer.

Polynomials can only be raised to an integral power.

To compute the nth Fibonacci number accurately, rpn sets the precision to
a level sufficient to guarantee a correct answer.

Bitwise operators force all arguments to integers by truncation if necessary.
''',
'metric' :
'''
SI Base Units:

    Quantity                    Dimension           SI unit and symbol

    Time                        T                   second (s)
    Length                      L                   meter (m)
    Mass                        M                   kilogram (kg)
    Electric current            I                   ampere (A)
    Temperature                 K                   kelvin (K)
    Luminous intensity          J                   candela (cd)
    Amount of substance **      N                   mole (mol)

SI Derived Units:

    Absorbed [radiation] dose   L^2 T^-2            gray (Gy)
    Acceleration                L T^-2              meter/second^2 (m*s^-2)
    Area                        L^2                 are (are)
    Capacitance                 L^-2 M^-1 T^4 I^2   farad (F)
    Catalytic activity **       N T^-1              katal (kat)
    Dynamic viscosity           M L^-1 T^-1         pascal-second (Pa*s)
    Electric charge             I T                 coulomb (C)
    Electric conductance        L^-2 M^-1 T^3 I^2   siemens (S)
    Electric resistance         L^2 M T^-3 I^-2     ohm ([omega])
    Energy                      L^2 M T^-2          joule (J)
    Force                       L M T^-2            newton (N)
    Frequency                   T^-1                hertz (Hz)
    Illuminance                 J L^-2              lux (lx)
    Inductance                  L^2 M T^-2 I^-2     henry (H)
    Kinematic viscosity         L^2 T^-1            meter^2/second (m2*s^-1)
    Luminous flux               J                   lumen (lm)
    Magnetic field strength     I L^-1              ampere/meter (A/m)
    Magnetic flux               L^2 M T^-2 I^-1     weber (Wb)
    Magnetic flux density       M T^-2 I^-1         tesla (T)
    Potential difference        L^2 M T^-3 I^-1     volt (V)
    Power                       L^2 M T^-3          watt (W)
    Pressure                    L^-1 M T^-2         pascal (Pa)
    Radiation dose equivalent   L^2 T^-2            sievert (Sv)
    Volume                      L^3                 liter (l)
    [Radioactive] activity      T^-1                becquerel (Bq)

    ** not supported in rpn

SI Prefixes:

    Prefix      Abbreviation    Factor

    yotta            Y          10^24
    zetta            Z          10^21
    exa              E          10^18
    peta             P          10^15
    tera             T          10^12
    giga             G          10^9
    mega             M          10^6
    kilo             k          10^3
    hecto            h          10^2
    deca             da         10^1
    deci             d          10^-1
    centi            c          10^-2
    milli            m          10^-3
    micro            u *        10^-6
    nano             n          10^-9
    pico             p          10^-12
    femto            f          10^-15
    atto             a          10^-18
    zepto            z          10^-21
    yocto            y          10^-24

    * Greek mu
''',
}


#//******************************************************************************
#//
#//  operator help
#//
#//******************************************************************************

operatorHelp = {
    '[' : [
'modifiers', 'begins a list',
'''
''',
'''
''' ],
    ']' : [
'modifiers', 'ends a list',
'''
''',
'''
''' ],
    'abs' : [
'arithmetic', 'calculates the absolute value of n',
'''
''',
'''
''' ],
    'acos' : [
'trigonometry', 'calculates the arccosine of n',
'''
''',
'''
''' ],
    'acosh' : [
'trigonometry', 'calculates the hyperbolic arccosine of n',
'''
''',
'''
''' ],
    'acot' : [
'trigonometry', 'calcuates the arccotangent of n',
'''
''',
'''
''' ],
    'acoth' : [
'trigonometry', 'calculates the hyperbolic arccotangent of n',
'''
''',
'''
''' ],
    'acsc' : [
'trigonometry', 'calculates the arccosecant of n',
'''
''',
'''
''' ],
    'acsch' : [
'trigonometry', 'calculates the hyperbolic arccosecant of n',
'''
''',
'''
''' ],
    'add' : [
'arithmetic', 'adds n to k',
'''
This operator adds two terms together.
''',
'''
c:\>rpn 2 2 add
4

c:\>rpn [ 1 2 3 4 5 6 ] 5 add
[ 6, 7, 8, 9, 10, 11 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 10 10 10 ] add
[ 11, 12, 13, 14, 15, 16 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 ] add
[ 11, 12, 13 ]''' ],
    'altfac' : [
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''' ],
    'altsign' : [
'list_operators', 'alternates signs in the list by making every even element negative',
'''
''',
'''
''' ],
    'altsign2' : [
'list_operators', 'alternates signs in the list by making every odd element negative',
'''
''',
'''
''' ],
    'altsum' : [
'arithmetic', 'calculates the alternating sum of list n (addition first)',
'''
''',
'''
''' ],
    'altsum2' : [
'arithmetic', 'calaculates the alternating sum of list n (subtraction first)',
'''
''',
'''
''' ],
    'and' : [
'logical', 'calculates the bitwise \'and\' of n and k',
'''
''',
'''
''' ],
    'apery' : [
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
''' ],
    'aperynum' : [
'combinatorics', 'calculates the nth Apery number',
'''
''',
'''
''' ],
    'append' : [
'list_operators', 'appends the second list on to the first list',
'''
''',
'''
''' ],
    'asec' : [
'trigonometry', 'calculates the arcsecant of n',
'''
''',
'''
''' ],
    'asech' : [
'trigonometry', 'calculates the hyperbolic arcsecant of n',
'''
''',
'''
''' ],
    'asin' : [
'trigonometry', 'calculates the arcsine of n',
'''
''',
'''
''' ],
    'asinh' : [
'trigonometry', 'calculates the hyperbolic arcsine of n',
'''
''',
'''
''' ],
    'ash_wednesday' : [
'time', 'calculates the date of Ash Wednesday for the year specified',
'''
''',
'''
''' ],
    'atan' : [
'trigonometry', 'calculates the arctangent of n',
'''
''',
'''
''' ],
    'atanh' : [
'trigonometry', 'calculates the hyperbolic arctangent of n',
'''
''',
'''
''' ],
    'avogadro' : [
'constants', 'returns Avogadro\'s number, the number of atoms in a mole',
'''
''',
'''
''' ],
    'balanced' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''
''',
'''
''' ],
    'balanced_' : [
'prime_numbers', 'calculates the nth set of balanced primes',
'''
''',
'''
''' ],
    'base' : [
'number_theory', 'interprets list elements as base k digits',
'''
''',
'''
''' ],
    'bell' : [
'combinatorics', 'calculates the nth Bell number',
'''
''',
'''
''' ],
    'bellpoly' : [
'algebra', 'evaluates the nth Bell polynomial with k',
'''
''',
'''
''' ],
    'bernoulli' : [
'combinatorics', 'calculates the nth Bernoulli number',
'''
''',
'''
''' ],
    'billion' : [
'constants', 'returns the constant one billion, i.e. 1.0e9, or 1,000,000,000',
'''
''',
'''
''' ],
    'binomial' : [
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
''',
'''
''' ],
    'calendar' : [
'time', 'prints a month calendar for the date value',
'''
The 'calendar' operator is special in that what it prints out is a side-effect.
It actually returns the date value passed in as a result, so as far as rpn is
concerned, it's an operator that does nothing.
''',
'''
''' ],
    'catalan' : [
'combinatorics', 'calculates nth Catalan number',
'''
''',
'''
''' ],
    'carol' : [
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''' ],
    'catalans' : [
'constants', 'returns Catalan\'s constant',
'''
''',
'''
''' ],
    'centeredcube' : [
'polyhedral_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' ],
    'cdecagonal' : [
'polygonal_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''' ],
    'cdecagonal?' : [
'polygonal_numbers', 'finds the index of the centered decagonal number of value n',
'''
'cdecagonal?' solves for the index of the equation used by 'cdecagonal' to
get the index i of the ith centered decagonal number that corresponds to the
value n.

If n is not a centered decagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'ceiling' : [
'arithmetic', 'returns the next highest integer for n',
'''
''',
'''
''' ],
    'cf' : [
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''' ],
    'champernowne' : [
'constants', 'returns the Champernowne constant',
'''
''',
'''
''' ],
    'char' : [
'conversion', 'converts the value to a signed 8-bit integer',
'''
''',
'''
''' ],
    'cheptagonal' : [
'polygonal_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''' ],
    'cheptagonal?' : [
'polygonal_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'cheptagonal?' solves for the index of the equation used by 'cheptagonal' to
get the index i of the ith centered heptagonal number that corresponds to the
value n.

If n is not a centered heptagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'chexagonal' : [
'polygonal_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''' ],
    'chexagonal?' : [
'polygonal_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'chexagonal?' solves for the index of the equation used by 'chexagonal' to
get the index i of the ith centered hexagonal number that corresponds to the
value n.

If n is not a centered hexagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cnonagonal' : [
'polygonal_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''' ],
    'cnonagonal?' : [
'polygonal_numbers', 'finds the index of the centered nonagonal number of value n',
'''
'cnonagonal?' solves for the index of the equation used by 'cnonagonal' to
get the index i of the ith centered nonagonal number that corresponds to the
value n.

If n is not a centered nonagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'coctagonal' : [
'polygonal_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''' ],
    'coctagonal?' : [
'polygonal_numbers', 'finds the index of the centered octgonal number of value n',
'''
'coctagonal?' solves for the index of the equation used by 'coctagonal' to
get the index i of the ith centered octagonal number that corresponds to the
value n.

If n is not a centered octagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'convert' : [
'conversion', 'performs unit conversion',
'''
''',
'''
''' ],
    'copeland' : [
'constants', 'returns the Copeland Erdos constant',
'''
''',
'''
''' ],
    'cos' : [
'trigonometry', 'calculates the cosine of n',
'''
''',
'''
''' ],
    'cosh' : [
'trigonometry', 'calculates the hyperbolic cosine of n',
'''
''',
'''
''' ],
    'cot' : [
'trigonometry', 'calculates the cotangent of n',
'''
''',
'''
''' ],
    'coth' : [
'trigonometry', 'calculates the hyperbolic cotangent of n',
'''
''',
'''
''' ],
    'count' : [
'list_operators', 'counts the elements of list n',
'''
''',
'''
''' ],
    'countbits' : [
'logical', 'returns the number of set bits in the value of n',
'''
''',
'''
''' ],
    'countdiv' : [
'number_theory', 'returns a count of the divisors of n',
'''
The divcount operator factors the argument and then calculates number of divisors
from the list of prime factors.  'divisors count' calculates the same result, but
the 'divisors' operator can generate prohibitively large lists for numbers with a
lot of factors.
''',
'''
c:\>rpn 98280 divcount
128

c:\>rpn 1 20 range divcount
[ 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6 ]
''' ],
    'cousinprime' : [
'prime_numbers', 'returns the nth cousin prime',
'''
''',
'''
''' ],
    'cpentagonal' : [
'polygonal_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''' ],
    'cpentagonal?' : [
'polygonal_numbers', 'finds the index of the centered pentagonal number of value n',
'''
'cpentagonal?' solves for the index of the equation used by 'cpentagonal' to
get the index i of the ith centered pentagonal number that corresponds to the
value n.

If n is not a centered pentagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cpolygonal' : [
'polygonal_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''' ],
    'cpolygonal?' : [
'polygonal_numbers', 'finds the index of the centered polygonal number of value n',
'''
'cpolygonal?' solves for the index of the equation used by 'cpolygonal' to
get the index i of the ith centered k-sided polygonal number that corresponds
to the value n.

If n is not a centered k-sided polygonal number, the result will not be a whole
number.
''',
'''
''' ],
    'csc' : [
'trigonometry', 'calculates the cosecant of n',
'''
''',
'''
''' ],
    'csch' : [
'trigonometry', 'calculates hyperbolic cosecant of n',
'''
''',
'''
''' ],
    'csquare' : [
'polygonal_numbers', 'calculates the nth centered square number',
'''
''',
'''
''' ],
    'csquare?' : [
'polygonal_numbers', 'finds the index of the centered square number of value n',
'''
'csquare?' solves for the index of the equation used by 'csquare' to get the
index i of the ith centered square number that corresponds to the value n.

If n is not a centered square number, the result will not be a whole number.
''',
'''
''' ],
    'ctriangular' : [
'polygonal_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''' ],
    'ctriangular?' : [
'polygonal_numbers', 'finds the index of the centered triangular number of value n',
'''
'ctriangular?' solves for the index of the equation used by 'ctriangular' to
get the index i of the ith centered triangular number that corresponds to the
value n.

If n is not a centered triangular number, the result will not be a whole
number.
''',
'''
''' ],
    'cube' : [
'powers_and_roots', 'calculates the cube of n',
'''
'cube' simply returns the value of n to the third power.
''',
'''
''' ],
    'decagonal' : [
'polygonal_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''' ],
    'decagonal?' : [
'polygonal_numbers', 'finds the index of the decagonal number of value n',
'''
''',
'''
''' ],
    'decillion' : [
'constants', 'returns the constant one decillion, i.e. 1.0e33',
'''
''',
'''
''' ],
    'degrees' : [
'trigonometry', 'interprets n as degrees and converts to radians',
'''
''',
'''
''' ],
    'delannoy' : [
'combinatorics', 'calculates the nth Delannoy number',
'''
''',
'''
''' ],
    'diffs' : [
'list_operators', 'returns a list with the differences between successive elements of list n',
'''
''',
'''
''' ],
    'diffs2' : [
'list_operators', 'returns a list with the differences between each element of list n with the first element',
'''
''',
'''
''' ],
    'divide' : [
'arithmetic', 'divides n by k',
'''
''',
'''
''' ],
    'divisors' : [
'number_theory', 'returns a list of divisors of n',
'''
''',
'''
''' ],
    'dhms' : [
'time', 'shortcut for \'[ day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ day hour minute second ]
convert' in order to convert a time interval to days, hours, minutes and
seconds.
''',
'''
c:\>rpn siderial_year dhms
[ 365 days, 6 hours, 9 minutes, 9.7632 seconds ]
''' ],
    'dms' : [
'conversion', 'shortcut for \'[ degree arcminute arcsecond ] convert\'',
'''
This shortcut operator replaces having to type '[ degree arcminute arcsecond ]
convert' in order to convert an angle to degrees, arcminutes and arcseconds.
''',
'''
c:\>rpn pi 7 / radians dms
[ 25 degrees, 42 arcminutes, 51.4285714285 arcseconds ]
''' ],
    'dodecahedral' : [
'polyhedral_numbers', 'returns the nth dodecahedral number',
'''
''',
'''
''' ],
    'double' : [
'conversion', 'converts n to the representation of a 64-bit IEEE 754 float',
'''
''',
'''
''' ],
    'doublebal' : [
'prime_numbers', 'returns the nth double balanced prime',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.
''',
'''
c:\>rpn 50 doublebal
931181

c:\>rpn 1 10 range doublebal
[ 18713, 25621, 28069, 30059, 31051, 44741, 76913, 97441, 103669, 106681 ]
''' ],
    'doublebal_' : [
'prime_numbers', 'returns the nth double balanced prime and its neighbors',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors.  This operator also returns the neighbors
and second neighbors.
''',
'''
c:\>rpn 50 doublebal_
[ 931163, 931169, 931181, 931193, 931199 ]

c:\>rpn 50 doublebal_ diffs
[ 6, 12, 12, 6 ]
''' ],
    'doublefac' : [
'number_theory', 'calculates the double factorial of n',
'''
''',
'''
''' ],
    'dst_end' : [
'time', 'calculates the ending date for Daylight Saving Time for the year specified',
'''
''',
'''
''' ],
    'dst_start' : [
'time', 'calculates the starting date for Daylight Saving Time for the year specified',
'''
''',
'''
''' ],
    'dup' : [
'modifiers', 'duplicates an argument n k times',
'''
This function duplicates terms, but requires the bracket operators to make the
resulting expression a list, rather than a set of k expressions.
''',
'''
c:\sys\ut>rpn [ 10 10 dup ]
[ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 ]

c:\sys\ut>rpn [ 1 10 range 10 dup ]
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5,
6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6,
7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]

c:\sys\ut>rpn [ 1 10 range 10 dup ] unique
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'e' : [
'constants', 'returns e (Euler\'s number)',
'''
''',
'''
''' ],
    'easter' : [
'time', 'calculates the date of Easter for the year specified',
'''
''',
'''
''' ],
    'egypt' : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' ],
    'election_day' : [
'time', 'calculates the date of Election Day (US) for the year specified',
'''
''',
'''
''' ],
    'element' : [
'list_operators', 'returns a single element from a list',
'''
''',
'''
''' ],
    'estimate' : [
'special', 'estimates the value of a measurement in common terms',
'''
''',
'''
''' ],
    'euler' : [
'constants', 'returns the Euler-Mascheroni constant',
'''
''',
'''
''' ],
    'eval' : [
'special', 'evaluates the function n for the given argument[s] k',
'''
'eval' is the boring trivial operator for user-defined functions.

Once this works, some really interesting new operators can be made.
''',
'''
c:\>rpn 3 x 2 * eval
6

c:\>rpn 5 x 2 ** 1 - eval
24
''' ],
    'exp' : [
'powers_and_roots', 'calculates the nth power of e',
'''
''',
'''
''' ],
    'exp10' : [
'powers_and_roots', 'calculates nth power of 10',
'''
''',
'''
''' ],
    'expphi' : [
'powers_and_roots', 'calculates the nth power of phi',
'''
expphi simply takes phi (the Golden Ratio) to the power of the argument n.

It was originally added to make testing the base phi output easier.
''',
'''
c:\>rpn 2 expphi
2.61803398875

c:\>rpn 3 expphi 2 expphi -
1.61803398875
''' ],
    'exprange' : [
'list_operators', 'generates a list of exponential progression of numbers',
'''
a = starting value, b = step exponent, c = size of list to generate

Each successive item in the list is calculated by raising the previous item to
the bth power.
''',
'''
c:\>rpn 2 2 10 exprange
[ 2, 4, 16, 256, 65536, 4294967296, 18446744073709551616, 3.4028236692e38,
1.1579208924e77, 1.34078079210e154 ]
''' ],
    'factor' : [
'number_theory', 'calculates the prime factorization of n',
'''
''',
'''
''' ],
    'factorial' : [
'number_theory', 'calculates the prime factorization of n',
'''
'factorial' calculates the product of all whole numbers from 1 to n.
''',
'''
''' ],
    'fibonacci' : [
'number_theory', 'calculates the nth Fibonacci number',
'''
''',
'''
''' ],
    'flatten' : [
'list_operators', 'flattens a nested lists in list n to a single level',
'''
''',
'''
''' ],
    'float' : [
'conversion', 'converts n to the representation of a 32-bit IEEE 754 float',
'''
''',
'''
''' ],
    'floor' : [
'arithmetic', 'calculates the next lowest integer for n',
'''
''',
'''
''' ],
    'fraction' : [
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''' ],
    'fromunixtime' : [
'conversion', 'converts Unix time (seconds since epoch) to a date-time format'
'''
''',
'''
''' ],
    'gamma' : [
'number_theory', 'calculates the gamma function for n',
'''
''',
'''
''' ],
    'gcd' : [
'arithmetic', 'calculates the greatest common denominator of elements in list n',
'''
''',
'''
''' ],
    'georange' : [
'list_operators', 'generates a list of geometric progression of numbers',
'''
''',
'''
''' ],
    'glaisher' : [
'constants', 'returns Glaisher\'s constant',
'''
''',
'''
''' ],
    'googol' : [
'constants', 'returns the constant one googol, i.e., 1.0e100',
'''
''',
'''
''' ],
    'harmonic' : [
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
''',
'''
''' ],
    'heptagonal' : [
'polygonal_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''' ],
    'heptagonal?' : [
'polygonal_numbers', 'finds the index of the heptagonal number of value n',
'''
''',
'''
''' ],
    'heptanacci' : [
'polygonal_numbers', 'calculates the nth Heptanacci number',
'''
''',
'''
''' ],
    'hepthex' : [
'polygonal_numbers', 'calculates the nth heptagonal hexagonal number',
'''
''',
'''
''' ],
    'heptpent' : [
'polygonal_numbers', 'calculates the nth heptagonal pentagonal number',
'''
''',
'''
''' ],
    'heptsquare' : [
'polygonal_numbers', 'calculates the nth heptagonal square number',
'''
''',
'''
''' ],
    'hepttri' : [
'polygonal_numbers', 'calculates the nth heptagonal triangular number',
'''
''',
'''
''' ],
    'hexagonal' : [
'polygonal_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''' ],
    'hexagonal?' : [
'polygonal_numbers', 'finds the index of the hexagonal number of value n',
'''
''',
'''
''' ],
    'hexanacci' : [
'number_theory', 'calculates the nth Hexanacci number',
'''
''',
'''
''' ],
    'hexpent' : [
'polygonal_numbers', 'calculates the nth hexagonal pentagonal number',
'''
''',
'''
''' ],
    'hms' : [
'time', 'shortcut for \'[ hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ hour minute second ] convert'
in order to convert a time interval to hours, minutes and seconds.
''',
'''
c:\>rpn 8 microcenturies hms convert
[ 7 hours, 0 minutes, 46.0799999991 seconds ]

Note:  Not sure why the rounding error is so large.
''' ],
    'hyper4_2' : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''' ],
    'hyperfac' : [
'number_theory', 'calculates the hyperfactorial of n',
'''
''',
'''
''' ],
    'hypot' : [
'trigonometry', 'calculates the hypotenuse of n and k',
'''
''',
'''
''' ],
    'i' : [
'complex_math', 'multiplies n by i',
'''
''',
'''
''' ],
    'icosahedral' : [
'polyhedral_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''' ],
    'infinity' : [
'special', 'evaluates to infinity, used to describe ranges for nsum, nprod, and limit',
'''
''',
'''
''' ],
    'integer' : [
'conversion', 'converts the value to an signed k-bit integer',
'''
''',
'''
''' ],
    'interleave' : [
'list_operators', 'interleaves lists n and k into a single list',
'''
''',
'''
''' ],
    'intersection' : [
'list_operators', 'returns the intersection of two lists',
'''
''',
'''
''' ],
    'isdivisible' : [
'arithmetic', 'returns whether n is n divisible by k',
'''
''',
'''
''' ],
    'iso_day' : [
'time', 'returns the ISO day and week for a time value',
'''
''',
'''
''' ],
    'isolated' : [
'prime_numbers', 'returns the nth isolated prime',
'''
''',
'''
''' ],
    'isprime' : [
'number_theory', 'returns whether n is prime',
'''
''',
'''
''' ],
    'issquare' : [
'arithmetic', 'returns whether n is a perfect square',
'''
''',
'''
''' ],
    'itoi' : [
'constants', 'returns i to the i power',
'''
''',
'''
''' ],
    'jacobsthal' : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
''',
'''
''' ],
    'julian_day' : [
'time', 'returns the Julian day for a time value',
'''
''',
'''
''' ],
    'khinchin' : [
'constants', 'returns Khinchin\'s constant',
'''
''',
'''
''' ],
    'kynea' : [
'number_theory', 'gets the nth Kynea number',
'''
''',
'''
''' ],
    'labor_day' : [
'time', 'calculates the date of Labor Day (US) for the year specified',
'''
''',
'''
''' ],
    'lah' : [
'combinatorics', '',
'''
''',
'''
''' ],
    'lambertw' : [
'logarithms', '',
'''
''',
'''
''' ],
    'leyland' : [
'number_theory', 'gets the Leyland number for n and k',
'''
''',
'''
''' ],
    'lgamma' : [
'number_theory', 'calculates the loggamma function for n',
'''
''',
'''
''' ],
    'li' : [
'logarithms', 'calculates the logarithmic interval of n',
'''
''',
'''
''' ],
    'limit' : [
'special', 'calculates the limit of function k( x ) as x approaches n',
'''
''',
'''
''' ],
    'limitn' : [
'special', 'calculates the limit of function k( x ) as x approaches n from above',
'''
''',
'''
''' ],
    'linearrecur' : [
'number_theory', 'calculates the nth value of a linear recurrence specified by a list of seeds and of factors'
'''
''',
'''
''' ],
    'ln' : [
'logarithms', 'calculates the natural logarithm of n',
'''
''',
'''
''' ],
    'log10' : [
'logarithms', 'calculates the base-10 logarithm of n',
'''
''',
'''
''' ],
    'log2' : [
'logarithms', 'calculates the base-2 logarithm of n',
'''
''',
'''
''' ],
    'logxy' : [
'logarithms', 'calculates the base-k logarithm of n',
'''
''',
'''
''' ],
    'long' : [
'conversion', 'converts the value to a signed 32-bit integer',
'''
''',
'''
''' ],
    'longlong' : [
'conversion', 'converts the value to a signed 64-bit integer',
'''
''',
'''
''' ],
    'lucas' : [
'number_theory', 'calculates the nth Lucas number',
'''
''',
'''
''' ],
    'makecf' : [
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''' ],
    'makejuliantime' : [
'conversion', 'interpret argument as absolute time specified by year, Julian day and optional time of day',
'''
''',
'''
''' ],
    'makeisotime' : [
'conversion', 'interpret argument as absolute time specified in the ISO format',
'''
''',
'''
''' ],
    'maketime' : [
'conversion', 'interpret argument as absolute time',
'''
''',
'''
''' ],
    'max' : [
'arithmetic', 'returns the largest value in list n',
'''
''',
'''
''' ],
    'maxchar' : [
'conversion', 'returns the maximum 8-bit signed integer',
'''
''',
'''
''' ],
    'maxindex' : [
'arithmetic', 'returns the index of largest value in list n',
'''
''',
'''
''' ],
    'maxlong' : [
'conversion', 'returns the maximum 32-bit signed integer',
'''
''',
'''
''' ],
    'maxlonglong' : [
'conversion', 'returns the maximum 64-bit signed integer',
'''
''',
'''
''' ],
    'maxquadlong' : [
'conversion', 'returns the maximum 128-bit signed integer',
'''
''',
'''
''' ],
    'maxshort' : [
'conversion', 'returns the maximum 16-bit signed integer',
'''
''',
'''
''' ],
    'maxuchar' : [
'conversion', 'returns the maximum 8-bit unsigned integer',
'''
''',
'''
''' ],
    'maxulong' : [
'conversion', 'returns the maximum 32-bit unsigned integer',
'''
''',
'''
''' ],
    'maxulonglong' : [
'conversion', 'returns the maximum 64-bit unsigned integer',
'''
''',
'''
''' ],
    'maxuquadlong' : [
'conversion', 'returns the maximum 128-bit unsigned integer',
'''
''',
'''
''' ],
    'maxushort' : [
'conversion', 'returns the maximum 16-bit unsigned integer',
'''
''',
'''
''' ],
    'mean' : [
'arithmetic', 'calculates the mean of values in list n',
'''
''',
'''
''' ],
    'mertens' : [
'constants', 'returns Merten\'s constant',
'''
''',
'''
''' ],
    'million' : [
'constants', 'returns the constant one million (i.e., 1.0e6, or 1,000,000)',
'''
''',
'''
''' ],
    'mills' : [
'constants', 'returns the Mills constant',
'''
from http://primes.utm.edu/glossary/page.php?sort=MillsConstant:

In the late forties Mills proved that there was a real number A > 1 for which
A ^ 3 ^ n is always a prime (n = 1,2,3,...).  He proved existence only, and did
not attempt to find such an A.  Later others proved that there are uncountably
many choices for A, but again gave no value for A. It is still not yet possible
to calculate a proven value for A, but if you are willing to accept the Riemann
Hypothesis, then the least possible value for Mills' constant (usually called
"the Mills Constant") [is this].
''',
'''
''' ],
    'min' : [
'arithmetic', 'returns the smallest value in list n',
'''
''',
'''
''' ],
    'minchar' : [
'conversion', 'returns the minimum 8-bit signed integer',
'''
''',
'''
''' ],
    'memorial_day' : [
'time', 'calculates the date of Memorial Day (US) for the year specified',
'''
''',
'''
''' ],
    'minindex' : [
'arithmetic', 'returns the index of smallest value in list n',
'''
''',
'''
''' ],
    'minlong' : [
'conversion', 'returns the minimum 32-bit signed integer',
'''
''',
'''
''' ],
    'minlonglong' : [
'conversion', 'returns the minimum 64-bit signed integer',
'''
''',
'''
''' ],
    'minquadlong' : [
'conversion', 'returns the minimum 128-bit signed integer',
'''
''',
'''
''' ],
    'minshort' : [
'conversion', 'returns the minimum 16-bit signed integer',
'''
''',
'''
''' ],
    'minuchar' : [
'conversion', 'returns the minimum 8-bit unsigned integer',
'''
''',
'''
''' ],
    'minulong' : [
'conversion', 'returns the minimum 32-bit unsigned integer',
'''
''',
'''
''' ],
    'minulonglong' : [
'conversion', 'returns the minimum 64-bit unsigned integer',
'''
''',
'''
''' ],
    'minuquadlong' : [
'conversion', 'returns the minimum 128-bit unsigned integer',
'''
''',
'''
''' ],
    'minushort' : [
'conversion', 'returns the minimum 16-bit unsigned integer',
'''
''',
'''
''' ],
    'modulo' : [
'arithmetic', 'calculates n modulo k',
'''
''',
'''
''' ],
    'monday' : [
'constants', 'returns 1, which is the code for Monday',
'''
''',
'''
''' ],
    'motzkin' : [
'combinatorics', 'calculates the nth Motzkin number',
'''
''',
'''
''' ],
    'multiply' : [
'arithmetic', 'multiplies n by k',
'''
''',
'''
''' ],
    'name' : [
'special', 'returns the English name for the integer value n',
'''
''',
'''
''' ],
    'narayana' : [
'combinatorics', '',
'''
''',
'''
''' ],
    'negative' : [
'arithmetic', 'calculates the negative of n',
'''
''',
'''
''' ],
    'negative_infinity' : [
'special', 'evaluates to negative infinity, used to describe ranges for nsum, nprod, and limit',
'''
''',
'''
''' ],
    'nonagonal' : [
'polygonal_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''' ],
    'nonagonal?' : [
'polygonal_numbers', 'finds the index of the nonagonal number of value n',
'''
''',
'''
''' ],
    'nonahept' : [
'polygonal_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and heptagonal.
''',
'''
''' ],
    'nonahex' : [
'polygonal_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and hexagonal.
''',
'''
''' ],
    'nonaoct' : [
'polygonal_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and octagonal.
''',
'''
''' ],
    'nonapent' : [
'polygonal_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and pentgonal.
''',
'''
''' ],
    'nonasquare' : [
'polygonal_numbers', 'calculates the nth nonagonal square number',
'''
'nonasquare' calculates the nth number that is both nonagonal and square.
''',
'''
''' ],
    'nonatri' : [
'polygonal_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonatri' calculates the nth number that is both nonagonal and triangular.
''',
'''
''' ],
    'nonillion' : [
'constants', 'returns the constant one nonillion, i.e. 1.0e30',
'''
''',
'''
''' ],
    'nonzero' : [
'list_operators', 'returns the indices of elements of list n that are not zero',
'''
''',
'''
''' ],
    'nprod' : [
'special', 'calculates the product of function c over the range of a through b',
'''
''',
'''
''' ],
    'not' : [
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
    'now' : [
'conversion', 'returns the current date and time',
'''
''',
'''
''' ],
    'nspherearea' : [
'trigonometry', 'calculates the surface area of an n-sphere of size k (radius or volume)',
'''
''',
'''
''' ],
    'nsphereradius' : [
'trigonometry', 'calculates the radius of an n-sphere of size k (surface area or volume)',
'''
''',
'''
''' ],
    'nspherevolume' : [
'trigonometry', 'calculates the volume of an n-sphere of size k (radius or surface area)',
'''
''',
'''
''' ],
    'nsum' : [
'special', 'calculates the sum of function c over the range of a through b',
'''
''',
'''
''' ],
    'nthweekday' : [
'time', 'finds the nth day (0 = Monday) of the month',
'''
a = four-digit year, b = month (1-12), c = week (1-5 for first through 5th),
d = day (0 = Monday, 1 = Tuesday, etc. through 6 = Sunday)
''',
'''
''' ],
    'nthweekdayofyear' : [
'time', 'finds the nth day (0 = Monday) of the year',
'''
a = four-digit year, b = week (negative values count from the end), c = day
(0 = Monday, 1 = Tuesday, etc. through 6 = Sunday)
''',
'''
''' ],
    'nthprime?' : [
'prime_numbers', 'finds the index of the closest prime over n',
'''
''',
'''
''' ],
    'nthquad?' : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''
''',
'''
''' ],
    'octagonal' : [
'polygonal_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''' ],
    'octagonal?' : [
'polygonal_numbers', 'finds the index of the octagonal number of value n',
'''
''',
'''
''' ],
    'octahedral' : [
'polyhedral_numbers', 'calculates the nth octahedral number',
'''
''',
'''
''' ],
    'octhept' : [
'polygonal_numbers', 'returns the nth octagonal heptagonal number',
'''
''',
'''
''' ],
    'octhex' : [
'polygonal_numbers', 'calculates the nth octagonal hexagonal number',
'''
''',
'''
''' ],
    'octillion' : [
'constants', 'returns the constant one octillion, i.e. 1.0e27',
'''
''',
'''
''' ],
    'octpent' : [
'polygonal_numbers', 'calculates the nth octagonal pentagonal number',
'''
''',
'''
''' ],
    'octsquare' : [
'polygonal_numbers', 'calculates the nth octagonal square number',
'''
''',
'''
''' ],
    'octtri' : [
'polygonal_numbers', 'calculates the nth octagonal triangular number',
'''
''',
'''
''' ],
    'oeis' : [
'special', 'downloads the OEIS integer series n',
'''
''',
'''
''' ],
    'oeiscomment' : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisex' : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisname' : [
'special', 'downloads the name of the OEIS integer series n',
'''
''',
'''
''' ],
    'omega' : [
'constants', 'returns the Omega constant',
'''
''',
'''
''' ],
    'or' : [
'logical', 'calculates the bitwise \'or\' of n and k',
'''
''',
'''
''' ],
    'padovan' : [
'number_theory', 'calculates the the nth Padovan number',
'''
''',
'''
''' ],
    'parity' : [
'logical', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
''',
'''
''' ],
    'pascal' : [
'number_theory', 'calculates the nth line of Pascal\'s triangle',
'''
''',
'''
''' ],
    'pell' : [
'combinatorics', 'calculates the nth Pell number',
'''
''',
'''
''' ],
    'pentagonal' : [
'polygonal_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''' ],
    'pentagonal?' : [
'polygonal_numbers', 'finds the index of the pentagonal number of value n',
'''
''',
'''
''' ],
    'pentanacci' : [
'number_theory', 'calculates the nth Pentanacci number',
'''
''',
'''
''' ],
    'pentatope' : [
'polyhedral_numbers', 'calculates the nth pentatope number',
'''
''',
'''
''' ],
    'percent' : [
'arithmetic', 'represents n as a percent (i.e., n / 100)',
'''
''',
'''
''' ],
    'perm' : [
'combinatorics', 'calculates the number of permutations of k out of n objects',
'''
''',
'''
''' ],
    'phi' : [
'constants', 'returns phi (the Golden Ratio)',
'''
''',
'''
''' ],
    'pi' : [
'constants', 'returns pi (Archimedes\' constant)',
'''
''',
'''
''' ],
    'plastic' : [
'constants', 'returns the Plastic constant',
'''
''',
'''
''' ],
    'polyadd' : [
'algebra', 'interprets two lists as polynomials and adds them',
'''
''',
'''
''' ],
    'polyarea' : [
'trigonometry', 'calculates the area of an regular n-sided polygon with sides of unit length',
'''
''',
'''
''' ],
    'polygamma' : [
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''' ],
    'polygonal' : [
'number_theory', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' ],
    'polygonal?' : [
'number_theory', 'finds the index of the polygonal number with k sides of value n',
'''
''',
'''
''' ],
    'polylog' : [
'logarithms', 'calculates the polylogarithm of n, k',
'''
''',
'''
''' ],
    'polymul' : [
'algebra', 'interprets two lists as polynomials and multiplies them',
'''
''',
'''
''' ],
    'polyprime' : [
'prime_numbers', 'returns the nth prime, recursively k times',
'''
''',
'''
''' ],
    'polyprod' : [
'algebra', 'interprets elements of list n as polynomials and calculates their product',
'''
''',
'''
''' ],
    'polysum' : [
'algebra', 'interprets elements of list n as polynomials and calculates their sum',
'''
''',
'''
''' ],
    'polytope' : [
'polyhedral_numbers', 'calculates nth polytope number of dimension k',
'''
''',
'''
''' ],
    'polyval' : [
'algebra', 'interprets the list as a polynomial and evaluates it for value k',
'''
''',
'''
''' ],
    'power' : [
'powers_and_roots', 'calculates the kth power of n',
'''
''',
'''
''' ],
    'presidents_day' : [
'time', 'calculates the date of Presidents Day (US) for the year specified',
'''
''',
'''
''' ],
    'previous' : [
'modifiers', 'duplicates the previous argument (identical to \'n 2 dup\')',
'''
''',
'''
''' ],
    'prevost' : [
'constants', 'returns Prevost\'s constant',
'''
Prevost's constant is the sum of the reciprocals of the Fibonacci numbers.
''',
'''
''' ],
    'product' : [
'arithmetic', 'calculates the product of values in list n',
'''
''',
'''
''' ],
    'prime' : [
'prime_numbers', 'returns the nth prime',
'''
''',
'''
''' ],
    'primepi' : [
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''
''',
'''
''' ],
    'primes' : [
'prime_numbers', 'generates a range of k primes starting from index n',
'''
This operator
 is much faster than using 'range' with 'prime'.
''',
'''
c:\>rpn 320620307 10 primes
[ 6927837559, 6927837563, 6927837571, 6927837583, 6927837599, 6927837617,
6927837641, 6927837673, 6927837713, 6927837757 ]
''' ],
    'prime?' : [
'prime_numbers', 'finds the index of the closest prime at n or above',
'''
''',
'''
''' ],
    'primorial' : [
'prime_numbers', 'calculates the nth primorial',
'''
''',
'''
''' ],
    'pyramid' : [
'polyhedral_numbers', 'calculates the nth square pyramidal number',
'''
''',
'''
''' ],
    'quadprime?' : [
'prime_numbers', 'finds the closest set of quadruplet primes above n',
'''
''',
'''
''' ],
    'quadprime' : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quadprime_' : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quadrillion' : [
'constants', 'returns the constant one quadrillion, i.e. 1.0e15',
'''
''',
'''
''' ],
    'quintillion' : [
'constants', 'returns the constant one quintillion, i.e. 1.0e18',
'''
''',
'''
''' ],
    'quintprime' : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'quintprime_' : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'radians' : [
'trigonometry', 'interprets n as radians and converts to degrees',
'''
''',
'''
''' ],
    'randint' : [
'special', 'returns a random integer from 0 to n - 1',
'''
''',
'''
''' ],
    'random' : [
'special', 'returns a random value from 0 to 1',
'''
''',
'''
''' ],
    'range' : [
'list_operators', 'generates a list of successive integers from n to k',
'''
''',
'''
''' ],
    'range2' : [
'list_operators', 'generates a list of arithmetic progression of numbers',
'''
''',
'''
''' ],
    'ratios' : [
'list_operators', 'returns a list with the ratios between successive elements of list n',
'''
''',
'''
''' ],
    'reciprocal' : [
'arithmetic', 'returns the reciprocal of n',
'''
''',
'''
''' ],
    'repunit' : [
'algebra', 'returns the nth repunit in base k',
'''
''',
'''
''' ],
    'result' : [
'special', 'loads the result from the previous invokation of rpn',
'''
''',
'''
''' ],
    'reverse' : [
'list_operators', 'returns list n with its elements reversed',
'''
''',
'''
''' ],
    'rhombdodec' : [
'polyhedral_numbers', 'calculates the nth rhombic dodecahedral number',
'''
''',
'''
''' ],
    'riesel' : [
'number_theory', 'calculates the nth Riesel (or Woodall) number',
'''
''',
'''
''' ],
    'robbins' : [
'constants', 'returns Robbins\' constant',
'''
Robbins' constant represents the average distance between two points selected
at random within a unit cube.
''',
'''
''' ],
    'root' : [
'powers_and_roots', 'calculates the kth root of n',
'''
''',
'''
''' ],
    'root2' : [
'powers_and_roots', 'calculates the square root of n',
'''
This operator is the equivalent of 'n 2 root'.
''',
'''
''' ],
    'root3' : [
'powers_and_roots', 'calculates the cube root of n',
'''
This operator is the equivalent of 'n 3 root'.
''',
'''
''' ],
    'round' : [
'arithmetic', 'rounds n to the nearest integer',
'''
''',
'''
''' ],
    'safeprime' : [
'prime_numbers', 'returns the nth safe prime',
'''
''',
'''
''' ],
    'schroeder' : [
'combinatorics', 'calculates the nth Schroeder number',
'''
''',
'''
''' ],
    'sec' : [
'trigonometry', 'calculates the secant of n',
'''
''',
'''
''' ],
    'sech' : [
'trigonometry', 'calculates the hyperbolic secant of n',
'''
''',
'''
''' ],
    'septillion' : [
'constants', 'returns the constant one septillion, i.e. 1.0e24',
'''
''',
'''
''' ],
    'sextillion' : [
'constants', 'returns the constant one sextillion, i.e. 1.0e21',
'''
''',
'''
''' ],
    'sextprime' : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sextprime_' : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sexyprime' : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexyprime_' : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexytriplet' : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexytriplet_' : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexyquad' : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'sexyquad_' : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'short' : [
'conversion', 'converts the value to a signed 16-bit integer',
'''
''',
'''
''' ],
    'sin' : [
'trigonometry', 'calculates the sine of n',
'''
''',
'''
''' ],
    'sinh' : [
'trigonometry', 'calculates the hyperbolic sine of n',
'''
''',
'''
''' ],
    'shiftleft' : [
'logical', 'performs a bitwise left shift of value n by k bits',
'''
''',
'''
''' ],
    'shiftright' : [
'logical', 'performs a bitwise right shift of value n by k bits',
'''
''',
'''
''' ],
    'solve' : [
'algebra', 'interprets list n as a polynomial and solves for its roots',
'''
''',
'''
''' ],
    'solve2' : [
'algebra', 'solves a quadratic equation',
'''
''',
'''
''' ],
    'solve3' : [
'algebra', 'solves a cubic equation',
'''
''',
'''
''' ],
    'solve4' : [
'algebra', 'solves a quartic equation',
'''
''',
'''
''' ],
    'sophieprime' : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''
''',
'''
''' ],
    'sort' : [
'list_operators', 'sorts the elements of list n numerically in ascending order',
'''
The 'sort' operator gets applied recursively, so all sublists will be sorted as
well.  I might have to reconsider that.
''',
'''
c:\>rpn [ rand rand rand ] sort
[ 0.782934612763, 0.956555810967, 0.97728726503 ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] sort
[ [ 10 ], [ 9 ], [ 8 ], [ 5, 6, 7 ], [ 4 ], [ 3 ], [ 1, 2 ], [ 0 ], [ -1 ] ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] flatten sort
[ -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'sortdesc' : [
'list_operators', 'sorts the elements of list n numerically in descending order',
'''
The 'sortdesc' operator works exactly like the sort operator, sorting the list
(and all sublists), except in descending order.
''',
'''
c:\>rpn 1 70 6 range2 sortdesc
[ 67, 61, 55, 49, 43, 37, 31, 25, 19, 13, 7, 1 ]

c:\>rpn 1 20 range countdiv sortdesc
[ 6, 6, 6, 5, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1 ]
''' ],
    'spherearea' : [
'trigonometry', 'calculates the surface area of an sphere of size n (radius or volume)',
'''
''',
'''
''' ],
    'sphereradius' : [
'trigonometry', 'calculates the radius of an sphere of size n (surface area or volume)',
'''
''',
'''
''' ],
    'spherevolume' : [
'trigonometry', 'calculates the volume of an sphere of size n (radius or surface area)',
'''
''',
'''
''' ],
    'square' : [
'powers_and_roots', 'calculates the square of n',
'''
''',
'''
''' ],
    'squaretri' : [
'polygonal_numbers', 'calculates the nth square triangular number',
'''
''',
'''
''' ],
    'stddev' : [
'arithmetic', 'calculates the standard deviation of values in list n',
'''
''',
'''
c:\>rpn 1 50 range countdiv stddev
2.14485430741
''' ],
    'steloct' : [
'polyhedral_numbers', 'calculates the nth stella octangula number',
'''
''',
'''
''' ],
    'subfac' : [
'number_theory', 'calculates the subfactorial of n',
'''
''',
'''
''' ],
    'subtract' : [
'arithmetic', 'subtracts k from n',
'''
''',
'''
''' ],
    'sum' : [
'arithmetic', 'calculates the sum of values in list n',
'''
''',
'''
''' ],
    'superfac' : [
'number_theory', 'calculates the superfactorial of n',
'''
''',
'''
''' ],
    'superprime' : [
'prime_numbers', 'returns the nth superprime (the nth primeth prime)',
'''
''',
'''
''' ],
    'sylvester' : [
'combinatorics', 'calculates the nth Sylvester number',
'''
''',
'''
''' ],
    'tan' : [
'trigonometry', 'calculates the tangent of n',
'''
''',
'''
''' ],
    'tanh' : [
'trigonometry', 'calculates the hyperbolic tangent of n',
'''
''',
'''
''' ],
    'tetrate' : [
'powers_and_roots', 'tetrates n by k',
'''
''',
'''
''' ],
    'tetrahedral' : [
'polyhedral_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' ],
    'tetranacci' : [
'number_theory', 'calculates the nth Tetranacci number',
'''
''',
'''
''' ],
    'thabit' : [
'number_theory', 'gets the nth Thabit number',
'''
''',
'''
''' ],
    'thanksgiving' : [
'time', 'calculates the date of Thanksgiving (US) for the year specified',
'''
''',
'''
''' ],
    'today' : [
'conversion', 'returns the current date',
'''
''',
'''
''' ],
    'tounixtime' : [
'conversion', 'converts from date-time list to Unix time (seconds since epoch)'
'''
''',
'''
''' ],
    'tower' : [
'powers_and_roots', 'calculates list n as a power tower',
'''
''',
'''
''' ],
    'tower2' : [
'powers_and_roots', 'calculates list n as a right-associative power tower',
'''
''',
'''
''' ],
    'trianglearea' : [
'trigonometry', 'calculates the area of a triangle with sides of length a, b, and c'
'''
''',
'''
''' ],
    'triangular' : [
'polygonal_numbers', 'calcuates the nth triangular number',
'''
''',
'''
''' ],
    'triangular?' : [
'polygonal_numbers', 'finds the index of the triangular number of value n',
'''
''',
'''
''' ],
    'tribonacci' : [
'number_theory', 'calculates the nth Tribonacci number',
'''
''',
'''
''' ],
    'trillion' : [
'constants', 'returns the constant one trillion, i.e. 1.0e12',
'''
''',
'''
''' ],
    'triplebal' : [
'prime_numbers', 'returns the nth triple balanced prime',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.
''',
'''
c:\>rpn 10 triplebal
14907649
''' ],
    'triplebal_' : [
'prime_numbers', 'returns the nth triple balanced prime and its neighbors',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.  This operator also
returns the neighbors, second neighbors, and third neighbors.
''',
'''
c:\>rpn 10 triplebal_
[ 14907619, 14907631, 14907637, 14907649, 14907661, 14907667, 14907679 ]

c:\>rpn 10 triplebal_ diffs
[ 12, 6, 12, 12, 6, 12 ]
''' ],
    'tripletprime' : [
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
''',
'''
''' ],
    'tripletprime' : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
''',
'''
''' ],
    'truncoct' : [
'polyhedral_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' ],
    'trunctet' : [
'polyhedral_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' ],
    'tuesday' : [
'constants', 'returns 2, which is the code for Tuesday',
'''
''',
'''
''' ],
    'twinprime' : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''
''',
'''
''' ],
    'twinprime_' : [
'prime_numbers', 'returns the nth set of twin primes',
'''
''',
'''
''' ],
    'uchar' : [
'conversion', 'converts the value to an unsigned 8-bit integer',
'''
''',
'''
''' ],
    'uinteger' : [
'conversion', 'converts the value to an unsigned k-bit integer',
'''
''',
'''
''' ],
    'ulong' : [
'conversion', 'converts the value to an unsigned 32-bit integer',
'''
''',
'''
''' ],
    'ulonglong' : [
'conversion', 'converts the value to an unsigned 64-bit integer',
'''
''',
'''
''' ],
    'union' : [
'list_operators', 'returns the union of two lists',
'''
''',
'''
''' ],
    'unique' : [
'list_operators', 'replaces list n with a list of its unique elements',
'''
''',
'''
''' ],
    'unitroots' : [
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
''' ],
    'unlist' : [
'modifiers', 'expands list n to individual arguments',
'''
''',
'''
''' ],
    'unpack' : [
'conversion', 'unpacks an integer value n into bit fields k',
'''
''',
'''
''' ],
    'ushort' : [
'conversion', 'converts the value to an unsigned 16-bit integer',
'''
''',
'''
''' ],
    'value' : [
'special', 'converts a measurement to a numerical value',
'''
''',
'''
''' ],
    'weekday' : [
'conversion', 'calculates the day of the week of an absolute time',
'''
''',
'''
''' ],
    'x' : [
'special', '\'x\' is used to create functions',
'''
Allows the user to define a function for use with the eval, nsum, nprod,
and limit operators, etc.  Basically 'x' starts an expression that
becomes a function.  Right now (5.28.0), a user-defined function must start
with 'x', but I hope to remove that limitation soon.

See the 'user_functions' help topic for more details.
''',
'''
c:\>rpn 3 x 2 * eval
6

c:\>rpn 5 x 2 ** 1 - eval
24

c:\>rpn inf x 1 + fib x fib / limit
1.6180339887

Once this works, some really interesting new operators can be made.
''' ],
    'xor' : [
'logical', 'calculates the bitwise \'xor\' of n and k',
'''
''',
'''
''' ],
    'ydhms' : [
'time', 'shortcut for \'[ year day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ year day hour minute
second ] convert' in order to convert a time interval to days, hours, minutes
and seconds.
''',
'''
''' ],
    'year_calendar' : [
'time', 'prints a month calendar for the date value',
'''
The 'year_calendar' operator is special in that what it prints out is a
side-effect.  It actually returns the date value passed in as a result, so as
far as rpn is concerned, it's an operator that does nothing.
''',
'''
''' ],
    'zero' : [
'list_operators', 'returns a list of the indices of elements in list n that are zero',
'''
''',
'''
''' ],
    'zeta' : [
'number_theory', 'calculates the zeta function for n',
'''
''',
'''
''' ],
    '_dumpalias' : [
'internal', 'dumps the list of aliases for operators',
'''
''',
'''
''' ],
    '_dumpbal' : [
'internal', 'dumps the cached list of balanced primes',
'''
''',
'''
''' ],
    '_dumpcousin' : [
'internal', 'dumps the cached list of cousin primes',
'''
''',
'''
''' ],
    '_dumpdouble' : [
'internal', 'dumps the cached list of double balanced primes',
'''
''',
'''
''' ],
    '_dumpiso' : [
'internal', 'dumps the cached list of isolated primes',
'''
''',
'''
''' ],
    '_dumpops' : [
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_dumpprimes' : [
'internal', 'dumps the cached list of large primes',
'''
''',
'''
''' ],
    '_dumpquad' : [
'internal', 'dumps the cached list of quadruplet primes',
'''
''',
'''
''' ],
    '_dumpquint' : [
'internal', 'dumps the cached list of quintuplet primes',
'''
''',
'''
''' ],
    '_dumpsext' : [
'internal', 'dumps the cached list of sextuplet primes',
'''
''',
'''
''' ],
    '_dumpsexy' : [
'internal', 'dumps the cached list of sexy primes',
'''
''',
'''
''' ],
    '_dumpsmall' : [
'internal', 'dumps the cached list of small primes',
'''
''',
'''
''' ],
    '_dumpsophie' : [
'internal', 'dumps the cached list of Sophie Germain primes',
'''
''',
'''
''' ],
    '_dumptriple' : [
'internal', 'dumps the cached list of triple balanced primes',
'''
''',
'''
''' ],
    '_dumptriplet' : [
'internal', 'dumps the cached list of triplet primes',
'''
''',
'''
''' ],
    '_dumptwin' : [
'internal', 'dumps the cached list of twin primes',
'''
''',
'''
''' ],
    '_importbal' : [
'internal', 'imports balanced primes from file n',
'''
''',
'''
''' ],
    '_importcousin' : [
'internal', 'imports cousin primes from file n',
'''
''',
'''
''' ],
    '_importdouble' : [
'internal', 'imports double balanced primes from file n',
'''
''',
'''
''' ],
    '_importiso' : [
'internal', 'imports isolated primes from file n',
'''
''',
'''
''' ],
    '_importprimes' : [
'internal', 'imports large primes from file n',
'''
''',
'''
''' ],
    '_importquad' : [
'internal', 'imports quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importquint' : [
'internal', 'imports quintuplet primes from file n',
'''
''',
'''
''' ],
    '_importsext' : [
'internal', 'imports sextuplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy' : [
'internal', 'imports sexy primes from file n',
'''
''',
'''
''' ],
    '_importsexy3' : [
'internal', 'imports sexy triplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy4' : [
'internal', 'imports sexy quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importsmall' : [
'internal', 'imports small primes from file n',
'''
''',
'''
''' ],
    '_importsophie' : [
'internal', 'imports Sophie Germain primes from file n',
'''
''',
'''
''' ],
    '_importtriple' : [
'internal', 'imports triple balanced primes from file n',
'''
''',
'''
''' ],
    '_importtriplet': [
'internal', 'imports triplet primes from file n',
'''
''',
'''
''' ],
    '_importtwin' : [
'internal', 'imports twin primes from file n',
'''
''',
'''
''' ],
    '_dumpops' : [
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_makebal' : [
'internal', 'calculates and caches balanced primes',
'''
_makebal start end interval
''',
'''
''' ],
    '_makecousin' : [
'internal', 'calculates and caches cousin primes',
'''
_makecousin start end interval
''',
'''
''' ],
    '_makedouble' : [
'internal', 'calculates and caches double balanced primes',
'''
_makedouble start end interval
''',
'''
''' ],
    '_makeiso' : [
'internal', 'calculates and caches isolated primes',
'''
_makeiso start end interval
''',
'''
''' ],
    '_makeprimes' : [
'internal', 'calculates and caches large primes',
'''
_makeprimes start end interval
''',
'''
''' ],
    '_makequad' : [
'internal', 'calculates and caches quaduplet primes',
'''
_makequad start end interval
''',
'''
''' ],
    '_makequint' : [
'internal', 'calculates and caches quintuplet primes',
'''
_makequint start end interval
''',
'''
''' ],
    '_makesext' : [
'internal', 'calculates and caches sextuplet primes',
'''
_makesext start end interval
''',
'''
''' ],
    '_makesexy' : [
'internal', 'calculates and caches sexy primes',
'''
_makesexy start end interval
''',
'''
''' ],
    '_makesexy3' : [
'internal', 'calculates and caches sexy triplet primes',
'''
_makesexy3 start end interval
''',
'''
''' ],
    '_makesexy4' : [
'internal', 'calculates and caches sexy quadruplet primes',
'''
_makesexy4 start end interval
''',
'''
''' ],
    '_makesmall' : [
'internal', 'calculates and caches small primes',
'''
_makesmall start end interval
''',
'''
''' ],
    '_makesophie' : [
'internal', 'calculates and caches Sophie Germain primes',
'''
_makesophie start end interval
''',
'''
''' ],
    '_makesuper' : [
'internal', 'calculates and caches super primes',
'''
_makesuper start end interval
''',
'''
''' ],
    '_maketriple' : [
'internal', 'calculates and caches triple balanced primes',
'''
_maketriple start end interval
''',
'''
''' ],
    '_maketriplet' : [
'internal', 'calculates and caches triplet primes',
'''
_maketriplet start end interval
''',
'''
''' ],
    '_maketwin' : [
'internal', 'calculates and caches twin primes',
'''
_maketwin start end interval
''',
'''
''' ],
    '_stats' : [
'internal', 'dumps rpn statistics',
'''
''',
'''
''' ],
    '~' : [
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
#   'antitet' : [ findTetrahedralNumber, 1 ],
#   'bernfrac' : [ bernfrac, 1 ],
#   'powmod' : [ getPowMod, 3 ],

# operators to be sorted:

    'wednesday' : [
'constants', 'returns 3, which is the code for Wednesday',
'''
''',
'''
''' ],
    'thursday' : [
'constants', 'returns 4, which is the code for Thursday',
'''
''',
'''
''' ],
    'friday' : [
'constants', 'returns 5, which is the code for Friday',
'''
''',
'''
''' ],
    'saturday' : [
'constants', 'returns 6, which is the code for Saturday',
'''
''',
'''
''' ],
    'sunday' : [
'constants', 'returns 7, which is the code for Sunday',
'''
''',
'''
''' ],
    'january' : [
'constants', 'returns 1, which is the code for January',
'''
''',
'''
''' ],
    'february' : [
'constants', 'returns 2, which is the code for February',
'''
''',
'''
''' ],
    'march' : [
'constants', 'returns 3, which is the code for March',
'''
''',
'''
''' ],
    'april' : [
'constants', 'returns 4, which is the code for April',
'''
''',
'''
''' ],
    'may' : [
'constants', 'returns 5, which is the code for May',
'''
''',
'''
''' ],
    'june' : [
'constants', 'returns 6, which is the code for June',
'''
''',
'''
''' ],
    'july' : [
'constants', 'returns 7, which is the code for July',
'''
''',
'''
''' ],
    'august' : [
'constants', 'returns 8, which is the code for August',
'''
''',
'''
''' ],
    'september' : [
'constants', 'returns 9, which is the code for September',
'''
''',
'''
''' ],
    'october' : [
'constants', 'returns 10, which is the code for October',
'''
''',
'''
''' ],
    'november' : [
'constants', 'returns 11, which is the code for November',
'''
''',
'''
''' ],
    'december' : [
'constants', 'returns 12, which is the code for December',
'''
''',
'''
''' ],
}


#//******************************************************************************
#//
#//  makeHelp
#//
#//******************************************************************************

def makeHelp( basicCategories ):
    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
    fileName = dataPath + os.sep + 'help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicCategories, pickleFile )
        pickle.dump( operatorHelp, pickleFile )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    print( 'makeHelp', PROGRAM_VERSION, '-', 'RPN command-line calculator help file generator' )
    print( COPYRIGHT_MESSAGE )
    print( )

    makeHelp( basicCategories )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

