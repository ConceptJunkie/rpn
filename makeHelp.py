#!/usr/bin/env python

# //******************************************************************************
# //
# //  makeHelp
# //
# //  RPN command-line calculator help file generator
# //  copyright (c) 2015, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import bz2
import contextlib
import pickle
import os

from rpnDeclarations import *
from rpnVersion import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


# //******************************************************************************
# //
# //  basic help categories
# //
# //******************************************************************************

helpTopics = {
    'options' :
    'rpn ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE + '\n\n' +
    '''
command-line options:

    -a [n], --output_accuracy [n]
        maximum number of decimal places to display, irrespective of internal
        precision (default: ''' + str( g.defaultOutputAccuracy ) + ')' + '''

    -b n : --input_radix n
        specify the radix for input (default: ''' + str( g.defaultInputRadix ) + ')' + '''

    -c, --comma -
        add commas to result, e.g., 1,234,567.0

    -d [n], --decimal_grouping [n] -
        display decimal places separated into groups (default: ''' + str( g.defaultDecimalGrouping ) + ')' + '''

    -g [n], --integer_grouping [n]
        display integer separated into groups (default: ''' + str( g.defaultIntegerGrouping ) + ')' + '''

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
        output in a different base (2 to 62, fib, fac, fac2, tri, sqr, lucas, primorial,
        e, pi, phi, sqrt2 )

    -R n, --output_radix_numerals n
        output a list of digits, where each digit is a base-10 number

    -t, --timer
        display calculation time

    -w [n], --bitwise_group_size [n]
        bitwise operations group values by this size (default: ''' + str( g.defaultBitwiseGroupSize ) + ')' + '''

    -x, --hex
        hex mode: equivalent to '-r16 -w16 -i4 -z'

    -z, --leading_zero
        add leading zeros if needed with -g

    -!, --print_options
        print values for all options
    ''',
    'arguments' :
    '''
As its name implies, rpn uses Reverse Polish Notation, otherwise referred to
as postfix notation.  The operand(s) come first and then the operator.  This
notation works without the need for parentheses.  rpn supports brackets for
creating lists of operands, but this serves a different purpose and is
described later.

Some simple examples:

2 + 2:
    rpn 2 2 +

3 sqrt(2) / 4:
    rpn 3 2 sqrt * 4 /

( 5 + 6 ) * ( 7 + 8 )
    rpn 5 6 + 7 8 +

Lists are specified using the bracket operators.  Most operators can take
lists as operands, which results in the operation being performed on each
item in the list.  If the operator takes two or more operands, then any
operand can be a list.  If one operand is a list and the other is a single
value, then each value in the list will have the single operand applied to
it with the operator, and the result will be displayed as a list.

c:\>rpn [ 2 3 4 5 6 ] 10 +
[ 12, 13, 14, 15, 16, 17 ]

c:\>rpn 7 [ 1 2 3 4 5 6 7 ] *
[ 7, 14, 21, 28, 35, 42, 49 ]

If both operands are lists, then each element from the first list is applied
to the corresponding element in the second list.  If one list is shorter than
the other, then only that many elements will have the operator applied and the
resulting list will only be as long as the shorter list.  The rest of the
items in the longer list are ignored.

rpn [ 1 2 3 4 5 6 7 ] [ 1 2 3 4 5 6 7 ] **
[ 1, 4, 27, 256, 3125, 46656, 823543 ]

rpn [ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *
[ 30, 40, 90, 160 ]

Some operators take lists as operands 'natively'.  This means the operator
requires a list, because the operation does not make sense for a single
value.  For example, 'mean' averages the values of a list.  If the
required list argument is a single value, rpn will promote it to a list.

c:\>rpn 1 mean
1

If the list operator takes a list and a non-list argument, then the non-list
argument can be a list, and rpn will evaluate the operator for all values in
the list.

c:\>rpn [ 1 2 3 ] [ 4 5 6 ] eval_poly
[ 27, 38, 51 ]

List operands can also themselves be composed of lists and rpn will recurse.

c:\>rpn [ [ 1 2 3 ] [ 4 5 6 ] [ 2 3 5 ] ] mean
[ 2, 5, 3.33333333333 ]

This becomes more powerful when used with operators that return lists, such as
the 'range' operator.  Here is an rpn expression that calculates the first 10
harmonic numbers:

c:\>rpn 1 1 10 range range 1/x sum
[ 1, 1.5, 1.83333333333, 2.08333333333, 2.28333333333, 2.45, 2.59285714286,
2.71785714286, 2.82896825397, 2.92896825397 ]
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
        2014-09-02

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

    How long was the summer in 2015?

        c:\>rpn 2015 autumnal_equinox 2015 summer_solstice - dhms
        [ 93 days, 15 hours, 42 minutes, 22.6755 seconds ]
    ''',
    'user_functions' :
    '''
This feature allows the user to define a function for use with the eval, nsum,
nprod, limit and limitn operators, etc.  Basically 'x' starts an expression
that becomes a function.  Right now (5.28.0), a user-defined function must
start with 'x', but I hope to remove that limitation soon.

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
    16.09344 kilometers

    c:\>rpn 2 gallons cups convert
    32 cups

    c:\>rpn 153 pounds stone convert
    10.928571428571 stone

    c:\>rpn 65 mph kph convert
    104.60736 kilometers/hour

    c:\>rpn 60 miles hour / furlongs fortnight / convert
    161280 furlongs per fortnight

    c:\>rpn mars_day hms
    [ 24 hours, 37 minutes, 22.6632 seconds ]

    c:\>rpn 10 tons estimate
    'approximately 1.65 times the mass of an average male African bush elephant'

    c:\>rpn 78 kg [ pound ounce ] convert
    [ 171 pounds, 15.369032067272 ounces ]

    c:\>rpn 150,000 seconds [ day hour minute second ] convert
    [ 1 day, 17 hours, 39 minutes, 60 seconds ]

I fixed the rounding error... sort of!  In this case, the result works out to
be epsilon shy of the even amount it should be, and it ends up getting rounded
up to 60 seconds.

Here's a shortcut for "[ day hour minute second ] convert":

    c:\>rpn 150,000 seconds dhms
    [ 1 day, 17 hours, 39 minutes, 60 seconds ]

What is the radius of a sphere needed to hold 8 fluid ounces?

    c:\>rpn 8 floz inch 3 ** convert sphereradius
    1.510547765004

It should say '1.510547765004 inches', but I haven't worked out all the unit
stuff with the sphere functions yet.

I tried to make the unit conversion flexible and smart.  It is... sometimes.

    c:>rpn 16800 mA hours * 5 volts * joule convert
    302400 joules

    c:\>rpn gigaparsec barn * cubic_inches convert
    188.299599080441 cubic inches

And sometimes it isn't:

    c:\>rpn cubic_inches gigaparsec barn * convert
    1 gigaparsec barn

Help topics for individual units is coming someday, but not today.
    ''',
    'interactive_mode' :
    '''
Interactive mode is a new feature introduced with version 6.  If rpn is
launched with no expressions, then it will start an interactive prompt that
allows the user to enter successive expressions for evaluation.

Interactive mode also introduces some new operators.  Each expression that is
evaluated is given a successive number:

c:\>rpn
rpn 6.5.0 - RPN command-line calculator
copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)

Type "help" for more information, and "exit" to exit.
rpn (1)>2 3 +
5
rpn (2)>10 sqrt
3.162277660168

These numbers can be used to refer to previous results by prepending the
result number with '$':

rpn (3)>$1 5 +
10
rpn (4)>$2 sqr
10

rpn now allows for assigning variables using the 'set' operator:

rpn (5)>side1 3 set
3
rpn (6)>side2 4 set
4
rpn (7)>$side1 $side2 hypotenuse
5

The variable can be reference in any subsequent expression using the '$',
which denotes a variable.  Variable names must start with an alphabetic
character, and can contain alphanumeric characters.

rpn interactive mode respects the command-line options that are passed to it.
These settings can be changed with the new settings operators.

There are two kinds of settings operators, operators that change a setting
tempoarily only for the next operation, and operators that change the settings
permanently, until they are changed by a subsequent settings operator, or the
user exits interactive mode.

See the 'settings' operators for more details.

accuracy:  Changes the accuracy displayed on output.  Equivalent to the '-a'
command-line option.  If the precision is less than accuracy + 2, then it is
set to accuracy + 2.

comma:  Turns commas displayed in output on or off.  Equivalent to the '-c'
command-line option.

comma_mode:  Turns on commas only for the next operation.  Aliased to '-c'.

decimal_grouping:  Sets the decimal grouping number.  Equivalent to the '-d'
command-line option.

hex_mode:  Aliased to '-x'.

identify:

identify_mode:  Aliased to '-i'.

input_radix:

integer_grouping:

leading_zero:

leading_zero_mode:  Aliased to '-z'.

octal_mode:  Aliased to '-o'.

output_radix:

precision:

The precision will not be set lower than the accuracy + 2.

timer:

timer_mode:  Turns on the timer for the next operation.  Aliased to '-t'.
    ''',
    'about' :
    PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' +
    COPYRIGHT_MESSAGE +
    '''

rpn is a command-line Reverse-Polish Notation calculator that was first
written in C in 1988.  It was rewritten in Python 3 in 2012 and now uses the
mpmath library.  It was a Python-learning exercise for me, and a fun little
toy, but when I found mpmath, it became really cool, so props to Fredrik
Johansson, who did all the heavy lifting (http://mpmath.org).
    ''',
    'bugs' :
    '''
-u doesn't work with complex numbers

Polynomials should support being taken to positive integral powers, but don't
yet.

Unit conversion suffers from small rounding errors in some situations.  This
is unavoidable to a certain extent, but it's worse than I think it should be.

If rpn crashes converting a number to another base, increase the accuracy
using -a.  I really want to prevent this from happening, but don't know how
yet.

I've been making a concerted efforts to identify and fix bugs, but I'm certain
there are still more.
    ''',
    'old_release_notes' :
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

Added 'random_integer' operator.

5.19.1

Fixed several problems with 'to_unix_time' and 'from_unix_time'.

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

The operators 'double_balanced', double_balanced_', 'triple_balanced', and
'triple_balanced_' now work correctly.  The data files have been significantly
expanded as well.

5.28.4

Added the 'diffs2' operator.

More bug fixes thanks to the test script!

5.28.5

More bug fixes and code cleanup.  Added the 'unfloat' and 'undouble'
operators.
    ''',
    'release_notes' :
    '''
For notes about earlier versions, use 'help release_notes_5'.

6.0.0

Introduced interactive mode, including variable declaration and referencing
previous results by number.  (see 'rpn help interactive_mode')

Added caching for OEIS operators.  However, it turns out some OEIS text is
non-ASCII, so I'll have to deal with that.

Operator help now includes examples by default.

The 'time' operator type conflicted with the 'time' unit type, so I changed
the operator type to 'date'... because they were all about dates!

Fixed a long-standing precision problem with unit conversion.

Lots more bug fixes.

6.0.1

Added code to prevent scientific notation from messing up base conversions
for the integral part of the number (up to 1000 digits).

6.1.0

New operators:  'maxdouble', 'maxfloat', 'mindouble', 'minfloat'

Base conversion for output is no longer limited to 1000 digits.  There's no
reason to do that.

'rpn 0 cf' now throws an error rather than dividing by 0.

6.2.0

Experimental support for mpath plotting functionality using the new
operators, 'plot', 'plot2', 'plotc'.  These operators are not supported
in the Windows installer.

'quit' is now an alias for 'exit' in interactive mode and help mode.

Improvements in function definition.  'y' and 'z' are now operators, allowing
for defining functions on 2 or 3 variables.

Operators 'eval2' and 'eval3' allow for evaluation of 2 and 3 variable
operators.

rpn now throws an error if a user-defined function is invalidly specified,
instead of going into an infinite loop.

'filter' allows filtering a list based on a user-defined function.

If the units in a measurement cancel out, then the measurement is converted
back to a numerical value.

Added 'random_' and 'random_integer_' operators.

Added the 'debruijn' operator.

Fixed several minor bugs.

6.3.0

Fixed 'triangle_area'.  It's been wrong for a long time.  Sorry.

Added the 'fibonorial' operator.

Added the 'euler_brick' operator.

Added the 'unlist' operator.

Added the 'make_pyth_3' and 'make_pyth_4' operators.

Added the 'is_equal', 'is_greater', 'is_less', 'is_not_equal',
'is_not_greater', and 'is_not_less' operators.

Added the 'reduce' operator.

Added the 'geometric_mean', 'argument', 'conjugate', 'lcm' operators.

The 'pascal' operator was renamed to 'pascaltri' to avoid a collision with
the 'pascal' unit.

Fixed several minor bugs.

6.4.0

Added the 'faradays_constant', 'radiation_constant' and 'stefan_boltzmann'
operators.

Added the 'magnetic_constant', 'electric_constant', 'rydberg_constant',
'newtons_constant' and 'fine_structure' operators.

Revamped factorization to be much, much faster.

Added 'euler_phi' operator.

Added caching for factorizations.

Added the 'sigma, 'aliquot', 'polypower', 'mobius' and 'mertens' operators.
The old 'mertens' operator was renamed to 'mertens_constant'.

Added the 'frobenius', 'slice', 'sublist', 'left' and 'right' operators.

Added 'crt' operator.

...and the usual bug fixes.

6.5.0

Added 'ecm' operator.

Added the 'hexagonal_square' operator.

Added the 'dup_operator', 'add_digits', and 'dup_digits' operators.

Ctrl-c can no longer interrupt saving the cache files, causing corruption.

Added the 'reverse_digits', 'group_elements', and 'is_palindrome' operators.

Added the 'combine_digits', 'is_pandigital', 'compositions' operators.

Added the 'reversal_addition' and 'find_palindrome' operators.

Added the 'get_digits' and 'sum_digits' operators.

The Great Renaming!   Renamed a bunch of operators so that multi-word operator
names always contain underscores between words.  The change makes sense now
that there are hundreds of operators.  The old names remain as aliases.

Added the 'silver_ratio', 'is_deficient', 'is_abundant' and 'is_perfect'
operators.

Added support for a lot of new bases for output, including factorial,
double factorial, Fibonacci (which was there but had been left out of the
documentation somehow), Lucas, triangular, square, e, pi, and the square root
of 2.  These all now include support for fractions.

Added the 'multifactorial', 'invert_units', 'shuffle', and 'occurrences'
operators.

Converted the prime number data files in git to the input text files.  Added
preparePrimeData.py to pickle the files for use.  This will make setting up
rpn for use with Python 2 possible.

Added the 'latlong_to_nac' operator.

Added the 'is_even', 'is_odd', 'is_zero', 'is_not_zero' operators and renamed
the other similar binary-value operators to be consistent with the 'is-' and
'is_not-' naming.

Added the 'filter_by_index' and 'multiply_digits' operators.

Added support for "huge" primes, currently defined to be the one billionth
through the twelve billionth prime numbers.  Using my current scheme of only
recording every nth prime number (10000th for the huge primes) I am trying to
strike a balance between data size and speed.  Using this scheme, access of an
arbitrary prime number between the one billionth and twelve billionth ranges
from approximately 4 to 12 seconds (or 2 to 8 seconds on a machine equipped
with a solid-state drive).

Added the 'nand' and 'nor' operators.

Added 'is_smooth', 'is_rough', 'unfilter', 'unfilter_by_index', 'negate',
'is_semiprime', 'is_sphenic', 'is_k_semiprime', 'is_squarefree', 'is_unusual',
'is_powerful', 'is_achilles', 'is_pronic', and 'leonardo' operators.

Added the 'eddington_number' operator.

Added a new operator category:  Astronomy (thanks to pyephem).  Added the
'vernal_equinox', 'summer_solstice', 'autumnal_equinox', and 'winter_solstice'
operators.

Filled in a bunch of help text.

...and the usual bug fixes.
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
    1.4285714285714285714

Basic trigonometry usage:

    c:\>rpn 60 deg sin         # sine of 60 degrees
    0.86602540378443864676

    c:\>rpn 45 deg tan         # tangent of 45 degrees
    1

    c:\>rpn 2 pi * rad degrees convert      # 2 pi radians is how many degrees?
    360 degrees

    c:\>rpn 2 atan rad degrees convert      # What angle (in degrees) has a slope of 2?
    63.434948822922010648 degrees

Convert an IP address to a 32-bit value and back:

    c:\>rpn -x [ 192 168 0 1 ] 256 base
    c0a8 0001

    c:\>rpn -R 256 0xc0a80001
    [192, 168, 0, 1]

Construct the square root of two from a continued fraction:

    First, here's the square root of two to 20 places:

        c:\>rpn -a20 2 sqrt
        1.4142135623730950488

    Now let's make a continued fraction from that, calculated to 20 terms.

        c:\>rpn 2 sqrt 20 make_cf
        [ 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ]

    Here's the nearest fractional approximation of the square root of two:

        c:\>rpn 2 sqrt 20 frac
        [ 22619537, 15994428 ]

    And we can calculate the square root of two from the continued fraction.
    In reality, the continued fraction representation of the square root of
    two is infinite, so this is only an approximation.

        c:\>rpn -a20 [ 1 2 30 dup ] cf
        1.4142135623730950488

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        c:\>rpn 1 50 range fib is_prime nonzero 1 + fib
        [ 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437, 2971215073 ]

    List the indices of the primes in the first 50 fibonacci numbers:
        c:\>rpn 3 50 range fib factor count 1 - zeroes 3 +
        [ 3, 4, 5, 7, 11, 13, 17, 23, 29, 43, 47 ]

    This calculation works by listing the indices of fibonacci numbers with a
    single factor.  We are skipping fib( 1 ) and fib( 2 ) because they have a
    single factor (of 1), but of course, aren't prime.

    Which of the first thousand pentagonal numbers are also triangular:
        c:\>rpn 1000 pent tri?
        1731.262180554824

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
        c:\>rpn [ 1 1 ] 1 1 10 range linear_recur
        [ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55 ]



Calculations with absolute time:

    operators:
        c:\>rpn now
        2014-09-02 13:36:28

        c:\>rpn today
        2014-09-02

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

        So a falling object will be travelling at 321.7 ft/sec after 10
        seconds.

    Here's a little more advanced version of the problem.  Let's say we have
    launched a rocket that is accelerated at 5 Gs for 5 minutes.  How long
    would it take for it to reach Jupiter (assume Jupiter is 500,000,000 miles
    away)?

        c:\>rpn 500 million miles 5 G 5 minutes * /
            20000000 miles per minute standard gravity

    That's not too helpful.  It's necessary to convert to miles/second partway
    through the conversion because rpn isn't smart enough (yet) to deduce that
    you can go from minute-Gs to miles per minute.

    Here's the final velocity:

        c:\>rpn 5 G 5 minutes * miles second / convert
            9.14035470353 miles per second

    This is something we can use...

        c:\>rpn 500 million miles 5 G 5 minutes * miles second / convert /
                days convert
            633.130466458 days

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
        = rpn -a20 1 100 range 0.5 0.5 100 geometric_range ** prod

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
    Temperature                 K (theta)           kelvin (K)
    Luminous intensity          J                   candela (cd)
    Amount of substance         N                   mole (mol)

    Note:  The dimension symbol for Amount of Substance is traditionally the
           Greek letter theta, but K is used to maintain ASCII-compatibility.

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

    * Greek mu, but since rpn only uses ASCII symbols, it's a lower-case 'u'
''',
}


# //******************************************************************************
# //
# //  operator help
# //
# //******************************************************************************

operatorHelp = {
    '[' : [
'modifiers', 'begins a list',
'''
Any operand in rpn can be replaced with a list of operands.  The '[' and ']'
operators are used to delimit lists, with 1 or more operands included inside.

Lists can also be members of lists.

rpn will execute the operator once for each item in the list, and the results
will be returned in a list.  Lists can be recursive.

Some operators in rpn require list operands, and these can also accept
recursive lists as well.

If multiple operands are replaced with lists, rpn will execute the operator
once for each item in the first list and each respective item in each
subsequent list operand.  If the lists are not the same size, rpn performs
the operator for each item of the shortest list and ignores the extra list
items.

*** Note:  As of 6.5.0, there are a few operators that don't correctly support
replacing single operands with lists.  I'm working through these to make
sure they all work.
*** Specifically, operators that are not of the type 'list_operators' that
take three or more operands do not work with lists.
''',
'''
c:\>rpn [ 10 20 30 40 ] prime
[ 29, 71, 113, 173 ]

c:\>rpn [ 2 3 4 6 7 ] 3 +
[ 5, 6, 7, 9, 10 ]

c:\>rpn [ 1 2 3 4 ] [ 4 3 2 1 ] +
[ 5, 5, 5, 5 ]

c:\>rpn [ [ 1 2 3 4 ] [ 2 3 4 5 ] [ 3 4 5 6 ] ] [ 8 9 10 11 ] +
[ [ 9, 10, 11, 12 ], [ 11, 12, 13, 14 ], [ 13, 14, 15, 16 ] ]
''' ],
    ']' : [
'modifiers', 'ends a list',
'''
Any operand in rpn can be replaced with a list of operands.  The '[' and ']'
operators are used to delimit lists, with 1 or more operands included inside.

Lists can also be members of lists.

rpn will execute the operator once for each item in the list, and the results
will be returned in a list.  Lists can be recursive.

Some operators in rpn require list operands, and these can also accept
recursive lists as well.

If multiple operands are replaced with lists, rpn will execute the operator
once for each item in the first list and each respective item in each
subsequent list operand.  If the lists are not the same size, rpn performs
the operator for each item of the shortest list and ignores the extra list
items.

*** Note:  As of 6.5.0, there are a few operators that don't correctly support
replacing single operands with lists.  I'm working through these to make
sure they all work.

*** Specifically, operators that are not of the type 'list_operators' that
take three or more operands do not work with lists.
''',
'''
c:\>rpn [ 10 20 30 40 ] prime
[ 29, 71, 113, 173 ]

c:\>rpn [ 2 3 4 6 7 ] 3 +
[ 5, 6, 7, 9, 10 ]

c:\>rpn [ 1 2 3 4 ] [ 4 3 2 1 ] +
[ 5, 5, 5, 5 ]

c:\>rpn [ [ 1 2 3 4 ] [ 2 3 4 5 ] [ 3 4 5 6 ] ] [ 8 9 10 11 ] +
[ [ 9, 10, 11, 12 ], [ 11, 12, 13, 14 ], [ 13, 14, 15, 16 ] ]
''' ],
    'abs' : [
'arithmetic', 'calculates the absolute value of n',
'''
The absolute value of a number represents its magnitude, regardless of sign.

The absolute value of 0 or a postive number is the number itself.  The
absolute value of a negative number is the number without the negative sign.
''',
'''
c:\>rpn 1 abs
1

c:\>rpn -1 abs
1

c:\>rpn [ -10 20 -30 40 -50 ] abs
[ 10, 20, 30, 40, 50 ]
''' ],
    'accuracy' : [
'settings', 'sets output accuracy to n'
'''
This operator changes the accuracy displayed on output in interactive mode.  It
is equivalent to the '-a' command-line option.

The 'default' constant can be used to set the default accuracy.
''',
'''
rpn (1)>pi
3.141592653581
rpn (2)>30 accuracy
30
rpn (3)>pi
3.141592653589793238462643383271
rpn (4)>default accuracy
12
rpn (5)>pi
3.141592653581
rpn (6)>
''' ],
    'acos' : [
'trigonometry', 'calculates the arccosine of n',
'''
The arcosine is the inverse of cosine.  In other words, if cos( x ) = y, then
acos( y ) = x.

All trigonometric functions work on radians unless specified.
''',
'''
c:\>rpn 0 acos
1.570796326795

c:\>rpn 0.5 acos rad deg convert
60 degrees

c:\>rpn 45 degrees cos acos rad deg convert
45 degrees
''' ],
    'acosh' : [
'trigonometry', 'calculates the hyperbolic arccosine of n',
'''
The hyperbolic arccosine is the inverse of the hyperbolic cosine.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
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
The hyperbolic arccotangent is the inverse of the hyperbolic cotangent.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
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
The hyperbolic arccosecant is the inverse of the hyperbolic cosecant.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'add' : [
'arithmetic', 'adds n to k',
'''
This operator adds two terms together.  If one of the operands is a list, then
the other operand is added to each member of the list and the result is a
list.

If both operands are lists, then each member of the list is added to its
corresponding member in the other list and the result is a list.  If the lists
are not of equal length, then the resulting list is the length of the shorter
of the two.

Addition is supported for measurements..
''',
'''
c:\>rpn 2 2 add
4

c:\>rpn [ 1 2 3 4 5 6 ] 5 add
[ 6, 7, 8, 9, 10, 11 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 10 10 10 ] add
[ 11, 12, 13, 14, 15, 16 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 ] add
[ 11, 12, 13 ]

c:\>rpn 1 mile 1 km +
1.621371192237 miles
''' ],
    'add_digits' : [
'lexicographic', 'adds the digits of k to n',
'''
''',
'''
''' ],
    'aliquot' : [
'number_theory', 'returns the first k members of the aliquot sequence of n',
'''
''',
'''
''' ],
    'alternating_factorial' : [
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''' ],
    'alternate_signs' : [
'list_operators', 'alternates signs in the list by making every even element negative',
'''
The return value is a list of the same size as the original with the sign of
every second element reversed, starting with the second.
''',
'''
c:\>rpn 1 10 range alternate_signs
[ 1, -2, 3, -4, 5, -6, 7, -8, 9, -10 ]
''' ],
    'alternate_signs_2' : [
'list_operators', 'alternates signs in the list by making every odd element negative',
'''
The return value is a list of the same size as the original with the sign of
every other element reversed, starting with the first element.
''',
'''
c:\>rpn 1 10 range alterate_signs_2
[ -1, 2, -3, 4, -5, 6, -7, 8, -9, 10 ]

''' ],
    'alternating_sum' : [
'arithmetic', 'calculates the alternating sum of list n (addition first)',
'''
This operator calculates the sum of the list, alternating the signs of every
second element starting with the second.

This operator is the same as using 'alternate_signs sum'.
''',
'''
c:\>rpn 1 10 range alternate_signs sum
-5

c:\>rpn 1 10 range alternating_sum
-5

Calculating e:

c:\>rpn -a20 0 25 range factorial 1/x alternating_sum 1/x
2.7182818284590452354
''' ],
    'alternating_sum_2' : [
'arithmetic', 'calaculates the alternating sum of list n (subtraction first)',
'''
This operator calculates the sum of the list, alternating the signs of every
other element starting with the first.

This operator is the same as using 'alternating_signs_2 sum'.
''',
'''
c:\>rpn 1 10 range alternating_signs_2 sum
5

c:\>rpn 1 10 range alternating_signs_2
5
''' ],
    'and' : [
'bitwise', 'calculates the bitwise \'and\' of n and k',
'''
'and' is the logical operation which returns true if and only if the two
operands are true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'and'ed bits.
''',
'''
c:\>rpn -x 0xF0F0F0F0 0x12345678 and
1030 5070

c:\>rpn [ 0 0 1 1 ] [ 0 1 0 1 ] and
[ 0, 0, 0, 1 ]
''' ],
    'apery' : [
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
c:\>rpn -a50 -d5 apery
1.20205 69031 59594 28539 97381 61511 44999 07649 86292 3405

c:\>rpn -a50 -d5 3 zeta
1.20205 69031 59594 28539 97381 61511 44999 07649 86292 3405
''' ],
    'append' : [
'list_operators', 'appends the second list on to the first list',
'''
This operator appends the second list of items to the first list resulting
in a single list containing all items in order from the first operand list and
then the second operand list.
''',
'''
c:\>rpn 1 5 range 6 10 range append
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'april' : [
'constants', 'returns 4, which is the code for April',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn april
4

c:\>rpn 2015 april 3 tuesday nthweekday
2015-04-21
''' ],
    'argument' : [
'complex_math', 'calculates complex argument (phase) of n',
'''
The complex argument, or phase, of a complex number is defined as the the
signed angle between the positive real axis and n in the complex plane.
''',
'''
c:\>rpn 3 3 i + arg
0.785398163397

c:\>rpn 3 3 i + arg radians degrees convert
45 degrees
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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'asin' : [
'trigonometry', 'calculates the arcsine of n',
'''
The arcsine is the inverse of sine.  In other words, if sin( x ) = y, then
asin( y ) = x.

All trigonometric functions work on radians unless specified.
''',
'''
c:\>rpn 0.5 asin
0.523598775598

c:\>rpn 0.75 sqrt asin rad deg convert
60 degrees

c:\>rpn 2 sqrt 1/x asin rad deg convert
45 degrees
''',
'''
''' ],
    'asinh' : [
'trigonometry', 'calculates the hyperbolic arcsine of n',
'''
The hyperbolic arcsine is the inverse of the hyperbolic sine.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'ash_wednesday' : [
'date', 'calculates the date of Ash Wednesday for the year specified',
'''
''',
'''
''' ],
    'atan' : [
'trigonometry', 'calculates the arctangent of n',
'''
The arctangent is the inverse of tangent.  In other words, if tan( x ) = y, then
atan( y ) = x.

All trigonometric functions work on radians unless specified.
''',
'''
c:\>rpn 3 atan
1.249045772398

c:\>rpn 10 atan rad deg convert
84.2894068625 degrees

c:\>rpn 89 degrees tan atan rad deg convert
89 degrees
''' ],
    'atanh' : [
'trigonometry', 'calculates the hyperbolic arctangent of n',
'''
The hyperbolic arctangent is the inverse of the hyperbolic tangent.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'august' : [
'constants', 'returns 8, which is the code for August',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn august
8

c:\>rpn 2015 august 4 tuesday nthweekday
2015-08-25
''' ],
    'autumnal_equinox' : [
'astronomy', 'calculates the time of the autumnal equinox for year n',
'''
''',
'''
''' ],
    'avogadro' : [
'constants', 'returns Avogadro\'s number, the number of atoms in a mole',
'''
''',
'''
c:\>rpn avogadro
6.02214129e+23

c:\>rpn -a24 avogadro
602214129000000000000000
''' ],
    'balanced_prime' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'balanced_prime_' : [
'prime_numbers', 'calculates the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
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
    'bell_polynomial' : [
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
c:\>rpn -c 7 billion
7,000,000,000
''' ],
    'binomial' : [
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
''',
'''
''' ],
    'calendar' : [
'date', 'prints a month calendar for the date value',
'''
The 'calendar' operator is special in that what it prints out is a side-effect.
It actually returns the date value passed in as a result, so as far as rpn is
concerned, it's an operator that does nothing.
''',
'''
''' ],
    'carol' : [
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''' ],
    'catalan' : [
'constants', 'returns Catalan\'s constant',
'''
''',
'''
c:\>rpn catalan
0.915965594177
''' ],
    'centered_cube' : [
'polyhedral_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' ],
    'centered_decagonal' : [
'polygonal_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''' ],
    'centered_decagonal?' : [
'polygonal_numbers', 'finds the index of the centered decagonal number of value n',
'''
'centered_decagonal?' solves for the index of the equation used by
'centered_decagonal' to get the index i of the ith centered decagonal number
that corresponds to the value n.

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
'constants', 'returns the Champernowne constant for the input base',
'''
The Champernowne constant is a transcendental number created by successive
appending every natural number as a decimal value.

The Champernowne constant is normally defined for base 10, but this operator
can also apply the same concept for any input base.
''',
'''
c:\>rpn -a60 champernowne
0.123456789101112131415161718192021222324252627282930313233344

The base 7 Champernowne constant

c:\>rpn -a60 -b7 champernowne -r7
0.123456101112131415162021222324252630313233343536404142434445

The base 7 Champernowne constant converted to base 10

c:\>rpn -a60 -b7 champernowne
0.1944355350862405214758400930829085764529329710504220831702
''' ],
    'char' : [
'conversion', 'converts the value to a signed 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'centered_heptagonal' : [
'polygonal_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''' ],
    'centered_heptagonal?' : [
'polygonal_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'centered_heptagonal?' solves for the index of the equation used by
'centered_heptagonal' to get the index i of the ith centered heptagonal number
that corresponds to the value n.

If n is not a centered heptagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'centered_hexagonal' : [
'polygonal_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''' ],
    'centered_hexagonal?' : [
'polygonal_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'centered_hexagonal?' solves for the index of the equation used by
'centered_hexagonal' to get the index i of the ith centered hexagonal number
that corresponds to the value n.

If n is not a centered hexagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'centered_nonagonal' : [
'polygonal_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''' ],
    'centered_nonagonal?' : [
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
    'centered_octagonal' : [
'polygonal_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''' ],
    'centered_octagonal?' : [
'polygonal_numbers', 'finds the index of the centered octgonal number of value n',
'''
'centered_octagonal?' solves for the index of the equation used by
'centered_octagonal' to get the index i of the ith centered octagonal number
that corresponds to the value n.

If n is not a centered octagonal number, the result will not be a whole number.
''',
'''
''' ],
    'comma' : [
'settings', 'allows changing the comma option in interactive mode',
'''
''',
'''
rpn (1)>5 12 **
244140625
rpn (2)>true comma
1
rpn (3)>5 12 **
244,140,625
''' ],
    'comma_mode' : [
'settings', 'set temporary comma mode in interactive mode',
'''
''',
'''
''' ],
    'combine_digits' : [
'lexicographic', 'combines the digits of all elements of list n into a single number',
'''
''',
'''
c:\>rpn 9 0 range combine_digits
9876543210

c:\>rpn 1 1 7 range primes combine_digits
[ 2, 23, 235, 2357, 235711, 23571113, 2357111317 ]
''' ],
    'compositions' : [
'combinatorics', 'returns a list containing all distinct ordered k-tuples of positive integers whose elements sum to n',
'''
This is referred to as the compositions of n.  Non-integer arguments are
truncated to integers.
''',
'''
c:\>rpn 5 2 compositions
[ [ 1, 4 ], [ 2, 3 ], [ 3, 2 ], [ 4, 1 ] ]

c:\>rpn 5 3 compositions
[ [ 1, 1, 3 ], [ 1, 2, 2 ], [ 1, 3, 1 ], [ 2, 1, 2 ], [ 2, 2, 1 ], [ 3, 1, 1 ] ]

c:\>rpn 5 4 compositions
[ [ 1, 1, 1, 2 ], [ 1, 1, 2, 1 ], [ 1, 2, 1, 1 ], [ 2, 1, 1, 1 ] ]
''' ],
    'conjugate' : [
'complex_math', 'calculates complex conjugate of n',
'''
The complex conjugate is simply the nunmber with the same real part and an
imaginary part with the same magnitude but opposite sign.
''',
'''
c:\>rpn 3 3 i + conj
(3.0 - 3.0j)
''' ],
    'convert' : [
'conversion', 'performs unit conversion',
'''
Unit conversion is a pretty extensive feature and needs some serious help
text.  Some day, I'll write it.  In the meantime, see 'help unit_conversion'.
''',
'''
c:\>rpn 10 miles km convert
16.09344 kilometers

c:\>rpn 2 gallons cups convert
32 cups

c:\>rpn 3 cups 4 tablespoons + fluid_ounce convert
26 fluid ounces

c:\>rpn 153 pounds stone convert
10.928571428571 stone

c:\>rpn 65 mph kph convert
104.60736 kilometers/hour

c:\>rpn 60 miles hour / furlongs fortnight / convert
161280 furlongs per fortnight

c:\>rpn mars_day [ hour minute second ] convert
[ 24 hours, 37 minutes, 22.6632 seconds ]

c:\>rpn 78 kg [ pound ounce ] convert
[ 171 pounds, 15.369032067272 ounces ]

This conversions suffers from a minor rounding error I haven't been able to
fix yet:

c:\>rpn 150,000 seconds [ day hour minute second ] convert
[ 1 day, 17 hours, 39 minutes, 60 seconds ]
''' ],
    'copeland' : [
'constants', 'returns the Copeland Erdos constant',
'''
''',
'''
c:\>rpn -a60 copeland
0.235711131719232931374143475359616771737983899710110310710911
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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'count' : [
'list_operators', 'counts the elements of list n',
'''
This simply counts the number of elements in the list.
''',
'''
c:\>rpn 1 100 range count
100
''' ],
    'count_bits' : [
'bitwise', 'returns the number of set bits in the value of n',
'''
''',
'''
''' ],
    'count_divisors' : [
'number_theory', 'returns a count of the divisors of n',
'''
The count_divisors operator factors the argument and then calculates number of
divisors from the list of prime factors.  'divisors count' calculates the same
result, but the 'divisors' operator can generate prohibitively large lists for
numbers with a lot of factors.
''',
'''
c:\>rpn 98280 count_divisors
128

c:\>rpn 1 20 range count_divisors
[ 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6 ]
''' ],
    'cousin_prime' : [
'prime_numbers', 'returns the nth cousin prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'centered_pentagonal' : [
'polygonal_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''' ],
    'centered_pentagonal?' : [
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
    'centered_polygonal' : [
'polygonal_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''' ],
    'centered_polygonal?' : [
'polygonal_numbers', 'finds the index of the centered polygonal number of value n',
'''
'centered_polygonal?' solves for the index of the equation used by
'centered_polygonal' to get the index i of the ith centered k-sided polygonal
number that corresponds to the value n.

If n is not a centered k-sided polygonal number, the result will not be a whole
number.
''',
'''
''' ],
    'crt' : [
'number_theory', 'calculates Chinese Remainder Theorem result of a list n of values and a list k of modulos',
'''
So using the Chinese Remainder Theorem, this function calculates a number that
is equal to n[ x ] modulo k[ x ], where x iterating through the indices of each
list (which must be the same size).
''',
'''
''' ],
    'csc' : [
'trigonometry', 'calculates the cosecant of n',
'''
The cosecant function is defined to be the reciprocal of the sine function.
''',
'''
c:\>rpn 36 degrees csc
1.7013016167

c:\>rpn 36 degrees csc 1/x
0.587785252292

c:\>rpn 36 degrees sin
0.587785252292
''' ],
    'csch' : [
'trigonometry', 'calculates hyperbolic cosecant of n',
'''

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'centered_square' : [
'polygonal_numbers', 'calculates the nth centered square number',
'''
''',
'''
''' ],
    'centered_square?' : [
'polygonal_numbers', 'finds the index of the centered square number of value n',
'''
'centered_square?' solves for the index of the equation used by 'csquare' to
get the index i of the ith centered square number that corresponds to the
value n.

If n is not a centered square number, the result will not be a whole number.
''',
'''
''' ],
    'centered_triangular' : [
'polygonal_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''' ],
    'centered_triangular?' : [
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
    'debruijn' : [
'combinatorics', 'generates a deBruijn sequence of n symbols and word-size k',
'''
A deBruijn sequence is a sequence of minimal length that contains all
permutations of the n symbols (represented by the integers 1 to n) with a
word size of k.

In all k-sized words that contain any possible permutation of n symbols can
be found in the sequence of symbols represented by the deBruijn sequence.

In the example below, you can find every combination of the symbols 0, 1, and
2 taken 3 at a time.  This is a smaller list than just appending all
permutations of the 3 symbols in groups of 3 because the groups can overlap.
''',
'''
c:\>rpn 3 3 debruijn
[ 0, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 1, 2, 0, 2, 1, 0, 2, 2, 1, 1, 1, 2, 1, 2,
2, 2 ]
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
    'december' : [
'constants', 'returns 12, which is the code for December',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn [ 2016 dec 25 ] make_time
2016-12-25 00:00:00
''' ],
    'decillion' : [
'constants', 'returns the constant one decillion, i.e. 1.0e33',
'''
''',
'''
''' ],
    'decimal_grouping' : [
'settings', 'used in interactive mode to set the decimal grouping level',
'''
''',
'''
''' ],
    'default' : [
'constants', 'used with settings operators',
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
    'dhms' : [
'conversion', 'shortcut for \'[ day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ day hour minute second ]
convert' in order to convert a time interval to days, hours, minutes and
seconds.
''',
'''
c:\>rpn sidereal_year dhms
[ 365 days, 6 hours, 9 minutes, 9.7632 seconds ]
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
This operator divides the first operand by the second.  If the first
operand is a list, then the second operand is divided by each member of
the list and the result is a list.  If the second operand is a list, then
the first operand is divided by each member of the list and the result is a
list.

If both operands are lists, then each member of the first list is divided by
its corresponding member in the second list and the result is a list.  If
the lists are not of equal length, then the resulting list is the length of
the shorter of the two.

Division is supported for measurements.
''',
'''
c:\>rpn 1440 24 /
60

c:\>rpn 2520 1 10 range /
[ 2520, 1260, 840, 630, 504, 420, 360, 315, 280, 252 ]

c:\>rpn miles hour / furlongs fortnight / convert
2688 furlongs per fortnight
''' ],
    'divisors' : [
'number_theory', 'returns a list of divisors of n',
'''
This operator lists all proper divisors of an integer including 1 and the
integer itself, sorted in order of increasing size.
''',
'''
c:\>rpn 3600 divisors
[ 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40, 45, 48,
50, 60, 72, 75, 80, 90, 100, 120, 144, 150, 180, 200, 225, 240, 300, 360, 400,
450, 600, 720, 900, 1200, 1800, 3600 ]

c:\>rpn [ 2 3 5 ] prod divisors
[ 1, 2, 3, 5, 6, 10, 15, 30 ]
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
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn pi double -x
4009 21fb 5444 2d18

c:\>rpn -a20 0x400921fb54442d18 undouble
3.141592653589793116
''' ],
    'double_balanced' : [
'prime_numbers', 'returns the nth double balanced prime',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 50 double_balanced
931181

c:\>rpn 1 10 range double_balanced
[ 18713, 25621, 28069, 30059, 31051, 44741, 76913, 97441, 103669, 106681 ]
''' ],
    'double_balanced_' : [
'prime_numbers', 'returns the nth double balanced prime and its neighbors',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors.  This operator also returns the neighbors
and second neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 50 double_balanced_
[ 931163, 931169, 931181, 931193, 931199 ]

c:\>rpn 50 double_balanced_ diffs
[ 6, 12, 12, 6 ]
''' ],
    'double_factorial' : [
'number_theory', 'calculates the double factorial of n',
'''
The name 'double factorial' is a little misleading as the definition of this
function is that n is multiplied by every second number between it and 1.

So it could sort of be thought of as a "half factorial".
''',
'''
c:\>rpn 1 10 range double_factorial
[ 1, 2, 3, 8, 15, 48, 105, 384, 945, 3840 ]
''' ],
    'dst_end' : [
'date', 'calculates the ending date for Daylight Saving Time for the year specified',
'''
''',
'''
''' ],
    'dst_start' : [
'date', 'calculates the starting date for Daylight Saving Time for the year specified',
'''
''',
'''
''' ],
    'dup_term' : [
'modifiers', 'duplicates an argument n k times',
'''
This function duplicates terms, but requires the bracket operators to make the
resulting expression a list, rather than a set of k expressions.
''',
'''
c:\>rpn 10 2 dup +
20

c:\>rpn [ 10 10 dup ]
[ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10 ]

c:\>rpn [ 1 10 range 10 dup ]
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5,
6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6,
7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]

c:\>rpn [ 1 10 range 10 dup ] unique
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'dup_digits' : [
'lexicographic', 'append n with a copy of its last k digits',
'''
''',
'''
''' ],
    'dup_operator' : [
'modifiers', 'duplicates an operation n times',
'''
''',
'''
''' ],
    'e' : [
'constants', 'returns e (Euler\'s number)',
'''
''',
'''
''' ],
    'easter' : [
'date', 'calculates the date of Easter for the year specified',
'''
''',
'''
''' ],
    'ecm' : [
'number_theory', 'factors n using the elliptical curve method',
'''
''',
'''
''' ],
    'eddington_number' : [
'constants', 'returns Arthur Eddington\'s famous estimate of the number of subatomic particles in the Universe',
'''In 1938, Arthur Eddington famously claimed that, "I believe there are
15,747,724,136,275,002,577,605,653,961,181,555,468,044,717,914,527,116,709,366,231,425,076,185,631,031,296
protons in the universe and the same number of electrons."  This number is equal to 136 * 2^256.''',
'''
''' ],
    'egypt' : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' ],
    'election_day' : [
'date', 'calculates the date of Election Day (US) for the year specified',
'''
In the U.S., Election Day is defined to be the first Tuesday after the first
Monday in November.  This definition was established by the U.S. Congress in
1845.
''',
'''
c:\>rpn 2016 election_day
2016-11-08

c:\>rpn 1964 election_day
1964-11-03
''' ],
    'electric_constant' : [
'constants', 'returns the electric constant',
'''
''',
'''
''' ],
    'element' : [
'list_operators', 'returns a single element from a list',
'''
The index is zero-based.
''',
'''
c:\>rpn 1 10 range 5 element
6

c:\>rpn 0 1000 range 34 element
34
''' ],
    'electric_constant' : [
'constants', 'returns a electic constant',
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
    'euler_brick' : [
'number_theory', 'creates the dimensions of an Euler brick, given a Pythagorean triple',
'''
An Euler brick is a brick with three dimensions such that any two pairs form
a Pythogorean triples, therefore the face diagonals are also integers.
''',
'''
c:\>rpn 2 3 make_pyth_3 unlist euler_brick
[ 828, 2035, 3120 ]

c:\>rpn 828 2035 hypotenuse
2197

c:\>rpn 828 3120 hypotenuse
3228

c:\>rpn 2035 3120 hypotenuse
3725
''' ],
    'euler_phi' : [
'number_theory', 'calculates Euler\'s totient function for n',
'''
''',
'''
''' ],
    'eval' : [
'special', 'evaluates the function n for the given argument[s] k',
'''
'eval' is the simplest operator for user-defined functions.  It just plugs
in the value n into the function k and returns the result.
''',
'''
c:\>rpn 3 x 2 * eval
6

c:\>rpn 5 x 2 ** 1 - eval
24

c:\>rpn 1 10 range x 2 ** 1 - eval
[ 0, 3, 8, 15, 24, 35, 48, 63, 80, 99 ]
''' ],
    'eval2' : [
'special', 'evaluates the function c for the given arguments a and b',
'''
'eval2' is the simplest operator for user-defined functions with 2 variables.
It just plugs in the values a and b into the function c and returns the
result.
''',
'''
''' ],
    'eval3' : [
'special', 'evaluates the function d for the given arguments a, b, and c',
'''
'eval3' is the simplest operator for user-defined functions with 3 variables.
It just plugs in the values a, b, and c into the function d and returns the
result.
''',
'''
Solving a quadratic equation the hard way, using the quadratic formula:

c:\>rpn 1 -4 -21 y neg y sqr 4 x * z * - sqrt + 2 x * / eval3
7

c:\>rpn 1 -4 -21 y neg y sqr 4 x * z * - sqrt - 2 x * / eval3
-3

Of course, rpn has better ways to do this:

c:\>rpn 1 -4 -21 solve2
[ 7, -3 ]

c:\>rpn [ 1 -4 -21 ] solve
[ -3, 7 ]
''' ],
    'eval_poly' : [
'algebra', 'interprets the list as a polynomial and evaluates it for value k',
'''
''',
'''
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
    'exponential_range' : [
'list_operators', 'generates a list of exponential progression of numbers',
'''
a = starting value, b = step exponent, c = size of list to generate

Each successive item in the list is calculated by raising the previous item to
the bth power.  The list is expanded to contain c items.
''',
'''
c:\>rpn 2 2 10 exponential_range
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
c:\>rpn 1 10 range factorial
[ 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800 ]
''' ],
    'false' : [
'constants', 'used with boolean settings operators',
'''
'false' simply evaluates to 0
''',
'''
''' ],
    'faradays_constant' : [
'constants', 'returns Faraday\'s Constant',
'''
''',
'''
c:\>rpn faradays_constant
96485.33289 coulombs per mole
''' ],
    'february' : [
'constants', 'returns 2, which is the code for February',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'fibonacci' : [
'number_theory', 'calculates the nth Fibonacci number',
'''
This sequence of numbers is created by a recurrence relation where the first
two items defined to be 1 and 1 (or in some cases 0 and 1 which just offsets
the indices by 1), and each successive element is the sum of the previous two.

This sequence was first written about by Leonardo of Pisa (known as Fibonacci)
in the 13th century.  The sequence has many amazing properties.
''',
'''
c:\>rpn 1 20 range fibonacci
[ 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,
4181, 6765 ]

This shows the relationship between the Fibonacci numbers and the Lucas numbers

c:\>rpn 1 30 2 range2 fib x sqr 5 * 4 - eval sqrt 2 30 2 range2 fib x sqr 5 *
4 + eval sqrt interleave
[ 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571,
5778, 9349, 15127, 24476, 39603, 64079, 103682, 167761, 271443, 439204, 710647,
1149851, 1860498 ]

c:\>rpn 1 30 range lucas
[ 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571,
5778, 9349, 15127, 24476, 39603, 64079, 103682, 167761, 271443, 439204, 710647,
1149851, 1860498 ]

''' ],
    'fibonorial' : [
'number_theory', 'calculates the product of the first n Fibonacci numbers',
'''
The name is a portmanteau of 'fibonacci' and 'factorial'.
''',
'''
c:\>rpn 1 10 range fibonorial
[ 1, 1, 1, 2, 6, 30, 240, 3120, 65520, 2227680 ]
''' ],
    'filter' : [
'special', 'filters a list n using function k',
'''
The function is applied to each element of the list and a new list is returned
which consists only of those elements for which the function returned a
non-zero value.
''',
'''
Which of the first 80 fibonacci numbers is prime?

c:\>rpn -p80 1 80 range fib x is_prime filter
[ 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437, 2971215073 ]
''' ],
    'filter_by_index' : [
'special', 'filters a list n using function k applied to the list indexes',
'''
''',
'''
''' ],
    'find_palindrome' : [
'lexicographic', 'adds the reverse of n to itself up to k successive times to find a palindrome',
'''
''',
'''
c:\>rpn -a30 10911 55 find_palindrome
[ 55, 4668731596684224866951378664 ]
''' ],
    'find_poly' : [
'algebra', 'finds a polynomial for which n is a zero',
'''
''',
'''
''' ],
    'fine_structure' : [
'constants', 'returns the fine-structure constant',
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
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''',
'''
c:\>rpn pi float -x
4049 0fdb

c:\>rpn 0x40490fdb unfloat
3.14159274101
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
    'friday' : [
'constants', 'returns 5, which is the code for Friday',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'frobenius' : [
'number_theory', 'calculates the frobenius number of a list of values with gcd > 1'
'''
''',
'''
''' ],
    'from_unix_time' : [
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
    'geometric_mean' : [
'list_operators', 'calculates the geometric mean of a a list of numbers n',
'''
The geometric mean is calculated by taking the kth root of the product of k
values.
''',
'''
c:\>rpn [ 1 2 ] geometric_mean
1.41421356237

c:\>rpn [ 1 10 range ] geometric_mean
[ 4.52872868812 ]

Calculate the geometric mean of the first n numbers from 1 to 5:

c:\>rpn [ 1 1 5 range range ] geometric_mean
[ [ 1, 1.41421356237, 1.81712059283, 2.2133638394, 2.6051710847 ] ]
''' ],
    'geometric_range' : [
'list_operators', 'generates a list of geometric progression of numbers',
'''
The list starts at a, and each successive value is multiplied by b, until the
list contains c items.
''',
'''
c:\>rpn 1 2 10 geometric_range
[ 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 ]

The intervals of the chromatic scale:

c:\>rpn 1 2 12 // 13 geometric_range
[ 1, 1.05946309436, 1.12246204831, 1.189207115, 1.25992104989, 1.33483985417,
1.41421356237, 1.49830707688, 1.58740105197, 1.68179283051, 1.78179743628,
1.88774862536, 2 ]
''' ],
    'get_digits' : [
'lexicographic', 'returns the list of digits comprising integer n',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
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
    'group_elements' : [
'list_operators', 'groups the elements of list n into sublsts of k elements',
'''
If there are elements left over (i.e., not enough to create the final group
of k elements, then the remaining list elements are included in the final
group.
''',
'''
c:\>rpn 1 10 range 5 group_elements
[ [ 1, 2, 3, 4, 5 ], [ 6, 7, 8, 9, 10 ] ]

c:\>rpn 1 11 range 5 group_elements
[ [ 1, 2, 3, 4, 5 ], [ 6, 7, 8, 9, 10 ], [ 11 ] ]

c:\>rpn 1 11 range previous is_prime interleave 2 group_elements -s1
[
[ 1, 0 ],
[ 2, 1 ],
[ 3, 1 ],
[ 4, 0 ],
[ 5, 1 ],
[ 6, 0 ],
[ 7, 1 ],
[ 8, 0 ],
[ 9, 0 ],
[ 10, 0 ],
[ 11, 1 ],
]
''' ],
    'harmonic' : [
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
''',
'''
''' ],
    'help' : [
'special', 'displays help text',
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
'number_theory', 'calculates the nth Heptanacci number',
'''
''',
'''
''' ],
    'heptagonal_hexagonal' : [
'polygonal_numbers', 'calculates the nth heptagonal hexagonal number',
'''
''',
'''
''' ],
    'heptagonal_pentagonal' : [
'polygonal_numbers', 'calculates the nth heptagonal pentagonal number',
'''
''',
'''
''' ],
    'heptagonal_square' : [
'polygonal_numbers', 'calculates the nth heptagonal square number',
'''
''',
'''
''' ],
    'heptagonal_triangular' : [
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
    'hexagonal_pentagonal' : [
'polygonal_numbers', 'calculates the nth hexagonal pentagonal number',
'''
''',
'''
''' ],
    'hexagonal_square' : [
'polygonal_numbers', 'calculates the nth hexagonal square number',
'''
''',
'''
''' ],
    'hex_mode' : [
'settings', 'set temporary hex mode in interactive mode',
'''
''',
'''
''' ],
    'hms' : [
'conversion', 'shortcut for \'[ hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ hour minute second ] convert'
in order to convert a time interval to hours, minutes and seconds.
''',
'''
c:\>rpn 8 microcenturies hms
[ 7 hours, 0 minutes, 46.08 seconds ]

c:\>rpn 15,625 seconds hms
[ 4 hours, 20 minutes, 25 seconds ]
''' ],
    'hyper4_2' : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''' ],
    'hyperfactorial' : [
'number_theory', 'calculates the hyperfactorial of n',
'''
''',
'''
''' ],
    'hypotenuse' : [
'trigonometry', 'calculates the hypotenuse of n and k',
'''
Given a right triangle with sides of n and k, the 'hypotenuse' operator
calculates what the length of the hypotenuse would be.
''',
'''
c:\>rpn 3 4 hypotenuse
5

c:\>rpn 7 24 hypotenuse
25

c:\>rpn 1 1 hypotenuse
1.414213562373
''' ],
    'i' : [
'complex_math', 'multiplies n by i',
'''
''',
'''
c:\>rpn -a10 e pi i **
(-1.0 + 5.2405181056621568055e-22j)

There's a rounding error here, but this demonstrates Euler's famous equation:

e ^ ( pi * i ) = -1
''' ],
    'icosahedral' : [
'polyhedral_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''' ],
    'identify' : [
'settings', 'set identify mode in interactive mode',
'''
''',
'''
''' ],
    'identify_mode' : [
'settings', 'set temporary identify mode in interactive mode',
'''
''',
'''
''' ],
    'imaginary' : [
'complex_math', 'returns the imaginary part of n',
'''
''',
'''
c:\>rpn 3 4 i + imaginary
4

c:\>rpn 7 imaginary
0

c:\>rpn 7 i imaginary
7

''' ],
    'infinity' : [
'special', 'evaluates to infinity, used to describe ranges for nsum, nprod, and limit',
'''
''',
'''
d:\dev\trunk\idirect>rpn phi
1.618033988741

d:\dev\trunk\idirect>rpn inf x 1 + fib x fib / limit
1.618033988741
''' ],
    'input_radix' : [
'settings', 'used in interactive mode to set the input radix',
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
    'integer_grouping' : [
'settings', 'used in interactive mode to set the integer grouping',
'''
''',
'''
''' ],
    'interleave' : [
'list_operators', 'interleaves lists n and k into a single list',
'''
Given an input of two lists, n and k 'interleave' returns a single list in which the
members of n and k are interleaved alternately.  If one list is longer than the other
then the extra list elements from the longer list are ignored.
''',
'''
c:\>rpn [ 1 3 5 ] [ 2 4 6 ] interleave
[ 1, 2, 3, 4, 5, 6 ]

c:\>rpn [ 1 3 5 ] [ 2 4 6 8 10 ] interleave
[ 1, 2, 3, 4, 5, 6 ]

c:\>rpn 1 20 2 range2 2 20 2 range2 interleave
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 ]
''' ],
    'intersection' : [
'list_operators', 'returns the intersection of two lists',
'''
''',
'''
Find numbers that are triangular and square at the same time:

c:\>rpn 1 100 range tri 1 100 range sqr intersect
[ 1, 36, 1225 ]
''' ],
    'invert_units' : [
'conversion', 'inverts the units and takes the reciprocal of the value'
'''
This operation returns an equivalent measurement with the units inverted from
the original operand.
''',
'''
''' ],
    'isolated_prime' : [
'prime_numbers', 'returns the nth isolated prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'iso_day' : [
'date', 'returns the ISO day and week for a time value',
'''
''',
'''
''' ],
    'is_abundant' : [
'number_theory', 'returns whether or not n is an abundant number',
'''
''',
'''
''' ],
    'is_achilles' : [
'number_theory', 'returns whether or not n is an Achilles number',
'''
''',
'''
''' ],
    'is_deficient' : [
'number_theory', 'returns whether or not n is a deficient number',
'''
''',
'''
''' ],
    'is_divisible' : [
'arithmetic', 'returns whether n is n divisible by k',
'''
''',
'''
''' ],
    'is_equal' : [
'arithmetic', 'returns 1 if n equals k, otherwise returns 0',
'''
''',
'''
c:\>rpn 0 1 is_equal
0

c:\>rpn 1 0 is_equal
0

c:\>rpn 1 1 is_equal
1

c:\>rpn pi 2 / 1 asin is_equal
1
''' ],
    'is_even' : [
'arithmetic', 'returns whether n is an even number',
'''
''',
'''
''' ],
    'is_greater' : [
'arithmetic', 'returns 1 if n is greater than k, otherwise returns 0',
'''
''',
'''
c:\>rpn 0 1 is_greater
0

c:\>rpn 1 0 is_greater
1

c:\>rpn 1 1 is_greater
0

c:\>rpn 3 5 ** 5 3 ** is_greater
1
''' ],
    'is_k_semiprime' : [
'number_theory', 'returns whether n is a k-factor square-free number',
'''
''',
'''
''' ],
    'is_less' : [
'arithmetic', 'returns 1 if n is less than k, otherwise returns 0',
'''
''',
'''
c:\>rpn 1 0 is_less
0

c:\>rpn 0 1 is_less
1

c:\>rpn 1 1 is_less
0

c:\>rpn 3 5 ** 5 3 ** is_less
0
''' ],
    'is_not_equal' : [
'arithmetic', 'returns 1 if n does not equal k, otherwise returns 0',
'''
''',
'''
c:\>rpn 0 1 is_not_equal
1

c:\>rpn 1 0 is_not_equal
1

c:\>rpn 1 1 is_not_equal
0
''' ],
    'is_not_greater' : [
'arithmetic', 'returns 1 if n is not greater than k, otherwise returns 0',
'''
'is_not_greater' is the equivalent of "less than or equal".
''',
'''
c:\>rpn 0 1 is_not_greater
1

c:\>rpn 1 0 is_not_greater
0

c:\>rpn 1 1 is_not_greater
1

c:\>rpn 3 5 ** 5 3 ** is_not_greater
0
''' ],
    'is_not_less' : [
'arithmetic', 'returns 1 if n is not less than k, otherwise returns 0',
'''
'is_not_less' is the equivalent of "greater than or equal".
''',
'''
c:\>rpn 0 1 is_not_less
0

c:\>rpn 1 0 is_not_less
1

c:\>rpn 1 1 is_not_less
1

c:\>rpn 3 5 ** 5 3 ** is_not_less
1
''' ],
    'is_not_zero' : [
'arithmetic', 'returns whether n is not zero',
'''
''',
'''
''' ],
    'is_odd' : [
'arithmetic', 'returns whether n is an odd number',
'''
''',
'''
''' ],
    'is_palindrome' : [
'lexicographic', 'returns whether an integer n is palindromic',
'''
n is treated as an integer.  If its digits are palindromic, i.e., they
read the same forwards as backwards, then the operator returns 1.
''',
'''
c:\>rpn 101 is_palindrome
1

c:\>rpn 1201 is_palindrome
0
''' ],
    'is_pandigital' : [
'lexicographic', 'returns whether an integer n is pandigital',
'''
A pandigital number contains at least one of all the of the digits 0 through
9.
''',
'''
c:\>rpn 123456789 is_pandigital
0

c:\>rpn 1234567890 is_pandigital
1

c:\>rpn -a30 [ 3 3 7 19 928163 1111211111 ] prod is_pandigital
1
''' ],
    'is_perfect' : [
'number_theory', 'returns whether or not n is a perfect number',
'''
''',
'''
''' ],
    'is_prime' : [
'number_theory', 'returns whether n is prime',
'''
''',
'''
''' ],
    'is_pronic' : [
'number_theory', 'returns whether n is pronic',
'''
''',
'''
''' ],
    'is_powerful' : [
'number_theory', 'returns whether n is a powerful number',
'''
''',
'''
''' ],
    'is_rough' : [
'number_theory', 'returns whether n is a k-rough number',
'''
''',
'''
''' ],
    'is_semiprime' : [
'number_theory', 'returns whether n is a semiprime number',
'''
''',
'''
''' ],
    'is_smooth' : [
'number_theory', 'returns whether n is a k-smooth number',
'''
''',
'''
''' ],
    'is_sphenic' : [
'number_theory', 'returns whether n is a sphenic number',
'''
''',
'''
''' ],
    'is_square' : [
'arithmetic', 'returns whether n is a perfect square',
'''
''',
'''
''' ],
    'is_squarefree' : [
'number_theory', 'returns whether n is a square-free number',
'''
''',
'''
''' ],
    'is_unusual' : [
'number_theory', 'returns whether n is an unusual number',
'''
''',
'''
''' ],
    'is_zero' : [
'arithmetic', 'returns whether n is zero',
'''
''',
'''
''' ],
    'itoi' : [
'constants', 'returns i to the i power',
'''
''',
'''
c:\>rpn 1 i 1 i **
(0.20787957635076190855 + 0.0j)

c:\>rpn itoi
0.207879576351
''' ],
    'jacobsthal' : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
''',
'''
''' ],
    'january' : [
'constants', 'returns 1, which is the code for January',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'julian_day' : [
'date', 'returns the Julian day for a time value',
'''
''',
'''
''' ],
    'july' : [
'constants', 'returns 7, which is the code for July',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'june' : [
'constants', 'returns 6, which is the code for June',
'''
This constant operator is defined for convenience for use with date operators.
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
'date', 'calculates the date of Labor Day (US) for the year specified',
'''
In the U.S., Labor Day falls on the first Monday of September.
''',
'''
c:\>rpn 2016 labor_day
2016-09-05
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
    'latlong_to_nac' : [
'conversion', '',
'''
''',
'''
''' ],
    'lcm' : [
'arithmetic', 'calculates the least common multiple of elements in list n',
'''
''',
'''
''' ],
    'leading_zero' : [
'settings', 'when set to true and integer grouping is being used, output will include leading zeroes',
'''
''',
'''
''' ],
    'leading_zero_mode' : [
'settings', 'used in the interactive mode to set the leading zero mode for output',
'''
''',
'''
''' ],
    'left' : [
'list_operators', 'returns the left k items from list n',
'''
''',
'''
c:\>rpn 1 10 range 6 left
[ 1, 2, 3, 4, 5, 6 ]

c:\>rpn 1 10 range 4 left
[ 1, 2, 3, 4 ]

c:\>rpn 1 10 range 1 4 range left
[ [ 1 ], [ 1, 2 ], [ 1, 2, 3 ], [ 1, 2, 3, 4 ] ]
''' ],
    'is_less' : [
'arithmetic', 'returns 1 if n is less than k, otherwise returns 0',
'''
''',
'''
c:\>rpn 1 0 is_less
0

c:\>rpn 0 1 is_less
1

c:\>rpn 1 1 is_less
0

c:\>rpn 3 5 ** 5 3 ** is_less
0
''' ],
    'leonardo' : [
'number_theory', 'returns the nth Leonardo number',
'''
''',
'''
''' ],
    'leyland' : [
'number_theory', 'returns the Leyland number for n and k',
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
    'linear_recur' : [
'number_theory', 'calculates the cth value of a linear recurrence specified by a list of factors (a) and of seeds (b)',
'''
The factors (a) indicate the multiple of each preceding value to add to create
the next value in the recurrence list, listed from right to left (meaning the
last factor corresponds to the n - 1'th value in the sequence.  For the
Fibonacci or Lucas lists, this would be [ 1 1 ], meaning the previous value,
plus the one before that.  The tribonacci sequence would have a factor list of
[ 1 1 1 ].

The seeds (b), simply specify a list of initial values.  The number of seeds
cannot exceed the number of factors, but there may be fewer seeds.

The is some disagreement about whether the zeroes count as part of these linear
recurrence sequences.  In rpn, for the 'fib' and 'lucas', 'tribonacci' operators,
etc., in accordance with mpmath, they do not.  However, Sloane (oeis.org) does
count the zeroes.

Internally, rpn uses this same linear recurrence functionality in the
'jacobsthal', 'repunit', 'heptagonal_triangular', 'heptagonal_square', and
'nonagonal_hexagonal' operators.
''',
'''
The 250th Fibonacci number:

c:\>rpn -c -a55 [ 1 1 ] [ 1 1 ] 250 linear_recur
7,896,325,826,131,730,509,282,738,943,634,332,893,686,268,675,876,375

The Fibonacci sequence:

c:\>rpn [ 1 1 ] [ 0 1 ] 1 18 range linear_recur
[ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597 ]

The Lucas Sequence:

c:\>rpn [ 1 1 ] [ 1 3 ] 1 17 range linear_recur
[ 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571 ]

The Tribonacci sequence:

c:\>rpn [ 1 1 1 ] [ 0 0 1 ] 1 18 range linear_recur
[ 0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768 ]

The Octanacci sequence:

c:\>rpn [ 1 8 dup ] [ 0 7 dup 1 ] 1 20 range linear
[ 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 4, 8, 16, 32, 64, 128, 255, 509, 1016, 2028 ]

The Pell numbers:

c:\>rpn [ 1 2 ] [ 0 1 ] 1 15 range linear_recur
[ 0, 1, 2, 5, 12, 29, 70, 169, 408, 985, 2378, 5741, 13860, 33461, 80782 ]

The Perrin sequence:

c:\>rpn [ 1 1 0 ] [ 3 0 2 ] 1 20 range linear_recur
[ 3, 0, 2, 3, 2, 5, 5, 7, 10, 12, 17, 22, 29, 39, 51, 68, 90, 119, 158, 209 ]
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
The base-10 logarithm of n is the power to which 10 is raised to get the number
n.
''',
'''
c:\>rpn 10 log10
1

c:\>rpn 3221 log10
3.507990724811

c:\>rpn 10 3221 log10 1481 log10 + power
4770301
''' ],
    'log2' : [
'logarithms', 'calculates the base-2 logarithm of n',
'''
The base-2 logarithm of n is the power to which 2 is raised to get the number
n.

The base-2 logarithm also calculates the number of bits necessary to store n
different values.
''',
'''
c:\>rpn 8 log2
3

c:\>rpn 65536 log2
16
''' ],
    'logxy' : [
'logarithms', 'calculates the base-k logarithm of n',
'''
The base-k logarithm of n is the power to which k is raised to get the number
n.
''',
'''
c:\>rpn 1000 10 logxy
3

c:\>rpn 78125 5 logxy
7

c:\>rpn e sqr e logxy
2
''' ],
    'long' : [
'conversion', 'converts the value to a signed 32-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'longlong' : [
'conversion', 'converts the value to a signed 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'lucas' : [
'number_theory', 'calculates the nth Lucas number',
'''
The Lucas sequence works just like the Fibonacci sequence, but starts with
1 and 3, instead of 0 and 1.  It shares many properties with the Fibonacci
sequence.
''',
'''
c:\>rpn 1 17 range lucas
[ 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843, 1364, 2207, 3571 ]
''' ],
    'magnetic_constant' : [
'constants', 'returns the magnetic constant',
'''
TODO:  explain all the other names this has
''',
'''
''' ],
    'make_cf' : [
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''' ],
    'make_julian_time' : [
'conversion', 'interpret argument as absolute time specified by year, Julian day and optional time of day',
'''
''',
'''
''' ],
    'make_iso_time' : [
'conversion', 'interpret argument as absolute time specified in the ISO format',
'''
''',
'''
''' ],
    'make_pyth_3' : [
'conversion', 'makes a pythagorean triple given two integers, n and k, as seeds',
'''
''',
'''
''' ],
    'make_pyth_4' : [
'conversion', 'makes a pythagorean quadruple given two integers, n and k, as seeds',
'''
n and k cannot both be odd.
''',
'''
''' ],
    'make_time' : [
'conversion', 'interpret argument as absolute time',
'''
''',
'''
''' ],
    'march' : [
'constants', 'returns 3, which is the code for March',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn [ 2016 march 31 ] make_time
2016-03-31 00:00:00
''' ],
    'max' : [
'arithmetic', 'returns the largest value in list n',
'''
''',
'''
''' ],
    'max_char' : [
'constants', 'returns the maximum 8-bit signed integer',
'''
''',
'''
''' ],
    'max_double' : [
'constants', 'returns the largest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn max_double
1.79769313486e308

c:\>rpn max_double double -x
7fef ffff ffff ffff
''' ],
    'max_float' : [
'constants', 'returns the largest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn max_float
3.40282346639e38

c:\>rpn max_float float -x
7f7f ffff
''' ],
    'max_index' : [
'list_operators', 'returns the index of largest value in list n',
'''
''',
'''
''' ],
    'max_long' : [
'constants', 'returns the maximum 32-bit signed integer',
'''
This is the largest number that can be represented by a 32-bit signed
integer assuming two's complement representation.

''',
'''
c:\>rpn max_long
2147483647

When does a 32-bit time_t wrap?

c:\>rpn 1970-01-01 max_long seconds +
2038-01-19 03:14:07
''' ],
    'max_longlong' : [
'constants', 'returns the maximum 64-bit signed integer',
'''
This is the largest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn max_longlong
9223372036854775807

When does a 64-bit time_t wrap?

c:\>rpn 1970-01-01 max_longlong seconds +
rpn:  value is out of range to be converted into a time
0

c:\>rpn -c max_longlong seconds years convert
292,271,023,045 years

Not for a long while...
''' ],
    'max_quadlong' : [
'constants', 'returns the maximum 128-bit signed integer',
'''
This is the largest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
''' ],
    'max_short' : [
'constants', 'returns the maximum 16-bit signed integer',
'''
This is the largest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
''' ],
    'max_uchar' : [
'constants', 'returns the maximum 8-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
''' ],
    'max_ulong' : [
'constants', 'returns the maximum 32-bit unsigned integer',
'''
This is the largest number that can be represented by a 32-bit unsigned
integer.
''',
'''
''' ],
    'max_ulonglong' : [
'constants', 'returns the maximum 64-bit unsigned integer',
'''
This is the largest number that can be represented by a 64-bit unsigned
integer.
''',
'''
''' ],
    'max_uquadlong' : [
'constants', 'returns the maximum 128-bit unsigned integer',
'''
This is the largest number that can be represented by a 128-bit unsigned
integer.
''',
'''
''' ],
    'max_ushort' : [
'constants', 'returns the maximum 16-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
c:\>rpn max_ushort
65535
''' ],
    'may' : [
'constants', 'returns 5, which is the code for May',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn [ 2016 may 31 ] make_time
2016-05-31 00:00:00
''' ],
    'mean' : [
'arithmetic', 'calculates the mean of values in list n',
'''
This is the classic definition of 'mean', often called 'average':  the sum of
all items divided by the number of items.
''',
'''
c:\>rpn 1 10 range mean
5.5

c:\>rpn 1 1000 range sum_digits mean
13.501
''' ],
    'memorial_day' : [
'date', 'calculates the date of Memorial Day (US) for the year specified',
'''
In the U.S., Memorial Day occurs on the last Monday in May.  This holiday
is dedicated to the memorial of the men and women who gave their lives in the
armed services.
''',
'''
c:\>rpn 2016 memorial_day
2016-05-30

c:\>rpn 2020 2025 range memorial_day -s1
[
2020-05-25,
2021-05-31,
2022-05-30,
2023-05-29,
2024-05-27,
2025-05-26,
]
''' ],
    'mertens' : [
'number_theory', 'returns Merten\'s function for n',
'''
''',
'''
''' ],
    'mertens_constant' : [
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
    'min_char' : [
'constants', 'returns the minimum 8-bit signed integer',
'''
This is the smallest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn min_char
-128

c:\>rpn min_char -x
-0080

c:\>rpn max_char min_char -
255
''' ],
    'min_double' : [
'constants', 'returns the smallest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn min_double
2.22507385851e-308

c:\>rpn min_double double -x
0010 0000 0000 0000
''' ],
    'min_float' : [
'conversion', 'returns the smallest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn min_float
1.17549435082e-38

c:\>rpn min_float float -x
0080 0000
''' ],
    'min_index' : [
'list_operators', 'returns the index of smallest value in list n',
'''
''',
'''
''' ],
    'min_long' : [
'constants', 'returns the minimum 32-bit signed integer',
'''
This is the smallest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn min_long
-2147483648

c:\>rpn max_long min_long -
4294967295
''' ],
    'min_longlong' : [
'constants', 'returns the minimum 64-bit signed integer',
'''
This is the smallest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn min_longlong
-9223372036854775808

c:\>rpn max_longlong min_longlong - 1 + log2
64
''' ],
    'min_quadlong' : [
'constants', 'returns the minimum 128-bit signed integer',
'''
This is the smallest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn min_quadlong
-170141183460469231731687303715884105728

c:\>rpn max_quadlong min_quadlong - 1 + log2
128
''' ],
    'min_short' : [
'constants', 'returns the minimum 16-bit signed integer',
'''
This is the smallest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn min_short
-32768

c:\>rpn max_short min_short -
65535
''' ],
    'min_uchar' : [
'constants', 'returns the minimum 8-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn min_uchar
0

c:\>rpn max_uchar min_uchar -
255
''' ],
    'min_ulong' : [
'constants', 'returns the minimum 32-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn min_ulong
0

c:\>rpn max_ulong min_ulong - 1 + log2
32
''' ],
    'min_ulonglong' : [
'constants', 'returns the minimum 64-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn min_ulonglong
0

c:\>rpn max_ulonglong min_ulonglong - 1 + log2
64
''' ],
    'min_uquadlong' : [
'constants', 'returns the minimum 128-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn min_uquadlong
0

c:\>rpn max_uquadlong min_uquadlong - 1 + log2
128
''' ],
    'min_ushort' : [
'constants', 'returns the minimum 16-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn min_ushort
0

c:\>rpn max_ushort min_ushort -
65535
''' ],
    'mobius' : [
'number_theory', 'calculates the Mobius function for n',
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
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'motzkin' : [
'combinatorics', 'calculates the nth Motzkin number',
'''
''',
'''
''' ],
    'multifactorial' : [
'combinatorics', 'calculates the nth k-factorial',
'''
The multifactorial operation is defined to be the product of every k-th
integer from n down to 1.  Therefore, the 1-multifactorial function is the
same as the 'factorial' operator and the 2-multifactorial function is the
same as the 'doublefac' operator.
''',
'''
c:\>rpn 1 20 range 3 multifactorial
[ 1, 2, 3, 4, 10, 18, 28, 80, 162, 280, 880, 1944, 3640, 12320, 29160, 58240,
209440, 524880, 1106560, 4188800 ]

c:\>rpn 1 20 range 4 multifactorial
[ 1, 2, 3, 4, 5, 12, 21, 32, 45, 120, 231, 384, 585, 1680, 3465, 6144, 9945,
30240, 65835, 122880 ]

c:\>rpn 1 20 range 5 multifactorial
[ 1, 2, 3, 4, 5, 6, 14, 24, 36, 50, 66, 168, 312, 504, 750, 1056, 2856, 5616,
9576, 15000 ]
''' ],
    'multiply' : [
'arithmetic', 'multiplies n by k',
'''
This operator multiplies two terms together.  If one of the operands is a list,
then the other operand is multiplied to each member of the list and the result
is a list.

If both operands are lists, then each member of the list is multiplied by its
corresponding member in the other list and the result is a list.  If the lists
are not of equal length, then the resulting list is the length of the shorter
of the two.

Multiplication is supported for measurements.
''',
'''
c:\>rpn 32 56 *
1792

c:\>rpn 7 1 10 range *
[ 7, 14, 21, 28, 35, 42, 49, 56, 63, 70 ]

c:\>rpn 16800 mA hours * 5 volts * joule convert
302400 joules
''' ],
    'multiply_digits' : [
'lexicographic', 'calculates the product of the digits of integer n',
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
    'nand' : [
'bitwise', 'calculates the bitwise \'nand\' of n and k',
'''
'nand' is the logical operation, 'not and' which returns true if zero or one
of the operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'and'ed bits.
''',
'''
c:\>rpn -x 0x01234567 0xffff0000 nand
fedc ffff

c:\>rpn -x [ 0x0000 0x0000 0xffff 0xffff ] [ 0x0000 0xffff 0x0000 0xffff ] nand
[ ffff, ffff, ffff, 0000 ]
''' ],
    'narayana' : [
'combinatorics', '',
'''
''',
'''
''' ],
    'negate' : [
'special', 'returns 0 if n is not 0 and 1 if n is 0',
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
    'newtons_constant' : [
'constants', 'returns Newton\'s gravitational constant',
'''
''',
'''
''' ],
    'next_first_quarter_moon' : [
'astronomy', 'returns the date of the next First Quarter Moon after n',
'''
''',
'''
''' ],
    'next_full_moon' : [
'astronomy', 'returns the date of the next Full Moon after n',
'''
''',
'''
''' ],
    'next_last_quarter_moon' : [
'astronomy', 'returns the date of the next Last Quarter Moon after n',
'''
''',
'''
''' ],
    'next_new_moon' : [
'astronomy', 'returns the date of the next New Moon after n',
'''
''',
'''
''' ],
    'nint' : [
'arithmetic', 'returns the nearest integer to n',
'''
On a tie, 'nint' returns the nearest even number.
''',
'''
c:\>rpn 2 sqrt nint
1

c:\>rpn 3 sqrt neg nint
-2

c:\>rpn 0.5 nint
0

c:\>rpn 1.5 nint
2
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
    'nonagonal_heptagonal' : [
'polygonal_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonagonal_heptagonal' calculates the nth number that is both nonagonal and
heptagonal.
''',
'''
''' ],
    'nonagonal_hexagonal' : [
'polygonal_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonagonal_hexagonal' calculates the nth number that is both nonagonal and
hexagonal.
''',
'''
''' ],
    'nonagonal_octagonal' : [
'polygonal_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonagonal_octagonal' calculates the nth number that is both nonagonal and
octagonal.
''',
'''
''' ],
    'nonagonal_pentagonal' : [
'polygonal_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonagonal_pentagonal' calculates the nth number that is both nonagonal and
pentgonal.
''',
'''
''' ],
    'nonagonal_square' : [
'polygonal_numbers', 'calculates the nth nonagonal square number',
'''
'nonagonal_square' calculates the nth number that is both nonagonal and square.
''',
'''
''' ],
    'nonagonal_triangular' : [
'polygonal_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonagonal_triangular' calculates the nth number that is both nonagonal and
triangular.

TODO: fix me
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
This operator is useful for applying an operator that returns a binary value
on a list, and getting a summary of the results.

Indices are zero-based.

(see 'nonzero')
''',
'''
c:\>rpn [ 1 0 2 0 3 0 4 ] nonzero
[ 0, 2, 4, 6 ]

List the prime Fibonacci numbers:

c:\>rpn 0 20 range fib is_prime nonzero fib
[ 2, 3, 5, 13, 89, 233, 1597 ]
''' ],
    'nor' : [
'bitwise', 'calculates the bitwise \'nor\' of n and k',
'''
'nor' is the logical operation 'not or', which returns true if and only if
neither of the two operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'nor'ed bits.
''',
'''
c:\>rpn -x 0x01234567 0x0000ffff nor
fedc 0000

c:\>rpn -x [ 0x0000 0x0000 0xffff 0xffff ] [ 0x0000 0xffff 0x0000 0xffff ] nor
[ ffff, 0000, 0000, 0000 ]
''' ],
    'not' : [
'bitwise', 'calculates the bitwise negation of n',
'''
'not' is the logical operation, which returns the opposite of the operand.

The operand is converted to a string of bits large enough to represent the
value, rounded up to the next highest multiple of the bitwise group size,
which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each bit in
the binary representation of the operand.  The result is the numerical
representation of the string of 'not'ed bits.
''',
'''
c:\>rpn -x 0xF0F0F0F0 not
0f0f 0f0f

c:\>rpn -x [ 0 1 ] not
[ ffff, fffe ]
''' ],
    'november' : [
'constants', 'returns 11, which is the code for November',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'now' : [
'date', 'returns the current date and time',
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
    'nsphere_area' : [
'trigonometry', 'calculates the surface area of an n-sphere of size k (radius or volume)',
'''
''',
'''
''' ],
    'nsphere_radius' : [
'trigonometry', 'calculates the radius of an n-sphere of size k (surface area or volume)',
'''
''',
'''
''' ],
    'nsphere_volume' : [
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
    'nth_apery' : [
'combinatorics', 'calculates the nth Apery number',
'''
''',
'''
''' ],
    'nth_catalan' : [
'combinatorics', 'calculates nth Catalan number',
'''
''',
'''
''' ],
    'nth_prime?' : [
'prime_numbers', 'finds the index of the closest prime over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'nth_quad?' : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'nth_weekday' : [
'date', 'finds the nth day (1 = Monday, etc.) of the month',
'''
a = four-digit year, b = month (1-12), c = week (1-5 for first through 5th),
d = day (1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''' ],
    'nth_weekday_of_year' : [
'date', 'finds the nth day (1 = Monday) of the year',
'''
a = four-digit year, b = week (negative values count from the end), c = day
(1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''' ],
    'occurrences' : [
'list_operators', 'returns the number of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
count.  The result will be sorted by values.
''',
'''
c:\>rpn 1 10 range occurrences
[ [ 1, 1 ], [ 2, 1 ], [ 3, 1 ], [ 4, 1 ], [ 5, 1 ], [ 6, 1 ], [ 7, 1 ],
[ 8, 1 ], [ 9, 1 ], [ 10, 1 ] ]

c:\>rpn 10 100 random_integer_ occurrences
[ [ 0, 9 ], [ 1, 8 ], [ 2, 6 ], [ 3, 10 ], [ 4, 12 ], [ 5, 11 ], [ 6, 7 ],
[ 7, 13 ], [ 8, 12 ], [ 9, 12 ] ]

c:\>rpn 5 6 debruijn occurrences
[ [ 0, 3125 ], [ 1, 3125 ], [ 2, 3125 ], [ 3, 3125 ], [ 4, 3125 ] ]
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
    'octal_mode' : [
'settings', 'set temporary octal mode in interactive mode',
'''
''',
'''
''' ],
    'octagonal_heptagonal' : [
'polygonal_numbers', 'returns the nth octagonal heptagonal number',
'''
''',
'''
''' ],
    'octagonal_hexagonal' : [
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
    'october' : [
'constants', 'returns 10, which is the code for October',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'octagonal_pentagonal' : [
'polygonal_numbers', 'calculates the nth octagonal pentagonal number',
'''
''',
'''
''' ],
    'octagonal_square' : [
'polygonal_numbers', 'calculates the nth octagonal square number',
'''
''',
'''
''' ],
    'octagonal_triangular' : [
'polygonal_numbers', 'calculates the nth octagonal triangular number',
'''
''',
'''
''' ],
    'oeis' : [
'special', 'downloads the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
c:\>rpn 10349 oeis
[ 1, 2, 3, 4, 5, 6, 13, 34, 44, 63, 250, 251, 305, 505, 12205, 12252, 13350,
13351, 15124, 36034, 205145, 1424553, 1433554, 3126542, 4355653, 6515652,
125543055, 161340144, 254603255, 336133614, 542662326 ]
''' ],
    'oeis_comment' : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
c:\>rpn 98593 oeiscomment
'Row sums are A009545(n+1), with e.g.f. exp(x)(cos(x)+sin(x)). Diagonal sums
are A077948.\nThe rows are the diagonals of the Krawtchouk matrices. Coincides
with the Riordan array (1/(1-x),(1-2x)/(1-x)). - _Paul Barry_, Sep 24
2004\nCorresponds to Pascal-(1,-2,1) array, read by anti-diagonals. The
Pascal-(1,-2,1) array has n-th row generated by (1-2x)^n/(1-x)^(n+1). - _Paul
Barry_, Sep 24 2004\nA modified version (different signs) of this triangle is
given by T(n,k)=sum{j=0..n, C(n-k,j)C(k,j)cos(Pi*(k-j))}. - _Paul Barry_, Jun
14 2007'
''' ],
    'oeis_ex' : [
'special', 'downloads the extra information field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
c:\>rpn 178 oeisex
'One more term from _Stefan Steinerberger_, Mar 10 2006'
''' ],
    'oeis_name' : [
'special', 'downloads the name of the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
c:\>rpn 10349 oeisname
'Base 7 Armstrong or narcissistic numbers.'
''' ],
    'old_factor' : [
'number_theory', 'the old version of \'factor\', this is going away',
'''
''',
'''
''' ],
    'omega' : [
'constants', 'returns the Omega constant',
'''
''',
'''
c:\>rpn omega
0.56714329041
''' ],
    'or' : [
'bitwise', 'calculates the bitwise \'or\' of n and k',
'''
'or' is the logical operation which returns true if at least one of the two
operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'or'ed bits.
''',
'''
c:\>rpn -x 0xf0f0f0f0 0x0f0f0f0f or
ffff ffff

c:\>rpn [ 0 0 1 1 ] [ 0 1 0 1 ] or
[ 0, 1, 1, 1 ]
''' ],
    'output_radix' : [
'settings', 'used in the interactive mode to set the output radix',
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
    'pack' : [
'conversion', 'packs an integer using a values list n and a list of bit fields k',
'''
''',
'''
''' ],
    'parity' : [
'bitwise', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
''',
'''
''' ],
    'partitions' : [
'combinatorics', 'returns the partition number for n',
'''
''',
'''
''' ],
    'pascal_triangle' : [
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
    'pentagonal_square' : [
'polygonal_numbers', 'calculates the nth pentagonal square number',
'''
''',
'''
''' ],
    'pentagonal_triangular' : [
'polygonal_numbers', 'calculates the nth pentagonal triangular number',
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
    'plot' : [
'special', 'plot function c for values of x between a and b',
'''
'plot' is very much considered experimental.  It's easy to construct an
incompletely-defined function and cause mpmath to go into an infinite loop.

I suppose I need to make my function evaluation logic smarter.   That would
also allow me to plot more than one function at a time.

'plot' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
c:\>rpn 0 pi x sin plot

c:\>rpn -5 5 x 4 ** 3 x 3 ** * + 25 x * - plot

c:\>rpn 1 50 x fib plot

c:\>rpn 1 10 x 1 + fib x fib / plot

''' ],
    'plot2' : [
'special', 'plot a 3D function '
'''
'plot2' is very much considered experimental.

Here's an example to try:

c:\>rpn -2 2 -2 2 x 2 ** y 2 ** - plot2

'plot2' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
''' ],
    'plotc' : [
'special', 'plot a complex function e for values of x between a and b real, c and d imaginary',
'''
'plotc' is very much considered experimental.

'plotc' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
''' ],
    'polyadd' : [
'algebra', 'interprets two lists as polynomials and adds them',
'''
''',
'''
''' ],
    'polygon_area' : [
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
'polygonal_numbers', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' ],
    'polygonal?' : [
'polygonal_numbers', 'finds the index of the polygonal number with k sides of value n',
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
    'polypower' : [
'algebra', 'exponentiates polynomial n by the integer power k',
'''
''',
'''
''' ],
    'polyprime' : [
'prime_numbers', 'returns the nth prime, recursively k times',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
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
    'power' : [
'powers_and_roots', 'calculates the kth power of n',
'''
This operator raises the first term to the power of the second.  If the first
operand is a list, then each item is raised to the power of the other operand
and the result is a list.  If the second operand is a list, then the first
operand is raised to the power of each member in the list and the result is a list.

If both operands are lists, then each member of the list is raised to the power
of its corresponding member in the other list and the result is a list.  If the
lists are not of equal length, then the resulting list is the length of the
shorter of the two.
''',
'''
c:\>rpn 4 5 **
1024

c:\>rpn 1 10 range 3 **
[ 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000 ]

c:\>rpn 1 foot 3 ** gallon convert
7.480519480519 gallons
''' ],
    'powmod' : [
'powers_and_roots', 'calculates a to the bth power modulo c',
'''
a, b and c are assumed to be integers.  TODO:  rpn should truncate them.
''',
'''
c:\>rpn 4 5 **
1024

c:\>rpn 1 10 range 3 **
[ 1, 8, 27, 64, 125, 216, 343, 512, 729, 1000 ]

c:\>rpn 1 foot 3 ** gallon convert
7.480519480519 gallons
''' ],
    'precision' : [
'settings', 'used in the interactive mode to set the output precision',
'''
''',
'''
''' ],
    'presidents_day' : [
'date', 'calculates the date of Presidents Day (US) for the year specified',
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
    'previous_first_quarter_moon' : [
'astronomy', 'returns the date of the previous First Quarter Moon before n',
'''
''',
'''
''' ],
    'previous_full_moon' : [
'astronomy', 'returns the date of the previous Full Moon before n',
'''
''',
'''
''' ],
    'previous_last_quarter_moon' : [
'astronomy', 'returns the date of the previous Last Quarter Moon before n',
'''
''',
'''
''' ],
    'previous_new_moon' : [
'astronomy', 'returns the date of the previous New Moon before n',
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
    'prime' : [
'prime_numbers', 'returns the nth prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primepi' : [
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primes' : [
'prime_numbers', 'generates a range of k primes starting from index n',
'''
This operator is much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 1 20 primes
[ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71 ]

c:\>rpn 320620307 10 primes
[ 6927837559, 6927837563, 6927837571, 6927837583, 6927837599, 6927837617,
6927837641, 6927837673, 6927837713, 6927837757 ]
''' ],
    'prime?' : [
'prime_numbers', 'finds the index of the closest prime at n or above',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primorial' : [
'prime_numbers', 'calculates the nth primorial',
'''
This function calculates the product of the first n prime numbers.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'product' : [
'arithmetic', 'calculates the product of values in list n',
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
    'quadruplet_prime?' : [
'prime_numbers', 'finds the closest set of quadruplet primes above n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quadruplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quadruplet_prime_' : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
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
    'quintuplet_prime?' : [
'prime_numbers', 'finds the closest set of quintuplet primes above n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quintuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quintuplet_prime_' : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'radiation_constant' : [
'constants', 'returns the Radiation Constant',
'''
''',
'''
c:\>rpn radiation_constant
7.5657e-16 joules per meter^3 kelvin^4
''' ],
    'random_integer' : [
'special', 'returns a random integer from 0 to n - 1',
'''
''',
'''
''' ],
    'random_integer_' : [
'special', 'returns a list of k random integers from 0 to n - 1',
'''

''',
'''
Test the birthday paradox:

rpn -D 365 23 random_integer_ sort

You will see a duplicate approximately 50% of the time.
''' ],
    'random' : [
'special', 'returns a random value from 0 to 1',
'''
''',
'''
''' ],
    'random_' : [
'special', 'returns a list of n random values from 0 to 1',
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
This operator is analogous to the 'diffs' operator.
''',
'''
''' ],
    'real' : [
'complex_math', 'returns the real part of n',
'''
''',
'''
c:\>rpn 3 4 i + real
3

c:\>rpn 7 i real
0

c:\>rpn 7 real
7
''' ],
    'reciprocal' : [
'arithmetic', 'returns the reciprocal of n',
'''
''',
'''
''' ],
    'reduce' : [
'list_operators', 'reduces out the common factors from each element of a list',
'''
In other words, each element of the list is divided by the greatest common
denominator of the whole list.
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
    'reversal_addition' : [
'lexicographic', 'TODO: describe me',
'''
''',
'''
c:\>rpn -a20 89 24 rev_add
8813200023188
''' ],
    'reverse_digits' : [
'lexicographic', 'returns n with its digits reversed',
'''
'reverse_digits' converts the argument to an integer.
''',
'''
c:\>rpn 123456789 reverse_digits
987654321

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
    'right' : [
'list_operators', 'returns the right k items from list n',
'''
''',
'''
c:\>rpn 1 10 range 6 right
[ 5, 6, 7, 8, 9, 10 ]

c:\>rpn 1 10 range 4 right
[ 7, 8, 9, 10 ]

c:\>rpn 1 10 range 1 4 range right
[ [ 10 ], [ 9, 10 ], [ 8, 9, 10 ], [ 7, 8, 9, 10 ] ]
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
    'rydberg_constant' : [
'constants', 'returns a Rydberg constant',
'''
''',
'''
''' ],
    'safe_prime' : [
'prime_numbers', 'returns the nth safe prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'safe_prime?' : [
'prime_numbers', '',
'''
''',
'''
''' ],
    'saturday' : [
'constants', 'returns 6, which is the code for Saturday',
'''
This constant operator is defined for convenience for use with date operators.
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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'september' : [
'constants', 'returns 9, which is the code for September',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'septillion' : [
'constants', 'returns the constant one septillion, i.e. 1.0e24',
'''
''',
'''
''' ],
    'set' : [
'special', 'sets variable n (which must start with \'$\') to value k in interactive mode',
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
    'sextuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sextuplet_prime_' : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexy_prime' : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns the smaller of
nth set of sexy primes, so the value of the result + 6 will also be prime.
''',
'''
c:\>rpn 16387 sexy_prime
1000033

c:\>rpn 1 10 range sexy_prime
[ 5, 7, 11, 13, 17, 23, 31, 37, 41, 47 ]
''' ],
    'sexy_prime_' : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns both members
of the nth set of sexy primes, which will differ by 6.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 213819 sexy_prime_
[ 20000063, 20000069 ]

c:\>rpn 1001 1010 range sexy_prime_
[ [ 31957, 31963 ], [ 32003, 32009 ], [ 32051, 32057 ], [ 32057, 32063 ],
[ 32063, 32069 ], [ 32077, 32083 ], [ 32083, 32089 ], [ 32183, 32189 ],
[ 32251, 32257 ], [ 32297, 32303 ] ]
''' ],
    'sexy_triplet' : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexy_triplet_' : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexy_quadruplet' : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexy_quadruplet_' : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'short' : [
'conversion', 'converts the value to a signed 16-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'shuffle' : [
'list_operators', 'randomly shuffles the elements in a list',
'''
''',
'''
''' ],
    'sigma' : [
'number_theory', 'returns the sum of the proper divisors of n'
'''
''',
'''
''' ],
    'silver_ratio' : [
'constants', 'returns the "silver ratio", defined to be 1 + sqrt( 2 )'
'''
''',
'''
''' ],
    'sign' : [
'arithmetic', 'returns the sign of a value',
'''
For real numbers, 'sign' returns 1 for positive, -1 for negative and 0 for
zero.

For complex numbers, it gives the projection onto the unit circle.
''',
'''
c:\>rpn 37 sign
1

c:\>rpn -8 sign
-1

c:\>rpn 0 sign
0

c:\>rpn 3 4 i + sign
(0.6 + 0.8j)

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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'shift_left' : [
'bitwise', 'performs a bitwise left shift of value n by k bits',
'''
''',
'''
''' ],
    'shift_right' : [
'bitwise', 'performs a bitwise right shift of value n by k bits',
'''
''',
'''
''' ],
    'slice' : [
'list_operators', 'returns a slice of list a from starting index b to ending index c',
'''
Indices are zero-based, and the ending index is not included in the slice.
This functionality echoes the Python slicing semantics.  As in Python, a
negative ending index represents counting backwards from the end of the list.

The starting and ending indices can, of course, be lists, and if they
are multiple lists will be returned iterating through one or both of the
operands as needed.
''',
'''
c:\>rpn 1 10 range 0 5 slice
[ 1, 2, 3, 4, 5 ]

c:\>rpn 1 10 range 5 10 slice
[ 6, 7, 8, 9, 10 ]

c:\>rpn 1 10 range 2 -1 slice
[ 3, 4, 5, 6, 7, 8, 9 ]

c:\>rpn 1 10 range 2 -2 slice
[ 3, 4, 5, 6, 7, 8 ]

c:\>rpn 1 10 range 0 4 range 6 8 range slice -s1
[
[ 1, 2, 3, 4, 5, 6 ],
[ 1, 2, 3, 4, 5, 6, 7 ],
[ 1, 2, 3, 4, 5, 6, 7, 8 ],
[ 2, 3, 4, 5, 6 ],
[ 2, 3, 4, 5, 6, 7 ],
[ 2, 3, 4, 5, 6, 7, 8 ],
[ 3, 4, 5, 6 ],
[ 3, 4, 5, 6, 7 ],
[ 3, 4, 5, 6, 7, 8 ],
[ 4, 5, 6 ],
[ 4, 5, 6, 7 ],
[ 4, 5, 6, 7, 8 ],
[ 5, 6 ],
[ 5, 6, 7 ],
[ 5, 6, 7, 8 ],
]
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
    'sophie_prime' : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
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
    'sort_descending' : [
'list_operators', 'sorts the elements of list n numerically in descending order',
'''
The 'sort_descending' operator works exactly like the sort operator, sorting
the list (and all sublists), except in descending order.
''',
'''
c:\>rpn 1 70 6 range2 sort_descending
[ 67, 61, 55, 49, 43, 37, 31, 25, 19, 13, 7, 1 ]

c:\>rpn 1 20 range countdiv sort_descending
[ 6, 6, 6, 5, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1 ]
''' ],
    'sphere_area' : [
'trigonometry', 'calculates the surface area of an sphere of size n (radius or volume)',
'''
''',
'''
''' ],
    'sphere_radius' : [
'trigonometry', 'calculates the radius of an sphere of size n (surface area or volume)',
'''
''',
'''
''' ],
    'sphere_volume' : [
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
    'square_triangular' : [
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
    'stefan_boltzmann' : [
'constants', 'returns the Stefan-Boltzmann constant',
'''
''',
'''
c:\>rpn stefan_boltzmann
5.670373e-8 watts per meter^2 kelvin^4
''' ],
    'stella_octangula' : [
'polyhedral_numbers', 'calculates the nth stella octangula number',
'''
A stella octangula number is a figurate number based on the stella octangula,
of the form n(2n^2 - 1).

The "stella octangula" is otherwise known as a "stellated octahedron".

https://en.wikipedia.org/wiki/Stella_octangula_number
http://oeis.org/A007588
''',
'''
c:\>rpn 1 8 range steloct
[ 2, 14, 34, 62, 98, 142, 194, 254 ]
''' ],
    'subfactorial' : [
'number_theory', 'calculates the subfactorial of n',
'''
''',
'''
''' ],
    'sublist' : [
'list_operators', 'returns a sublist of list a from starting index b consisting of c items',
'''
The index is zero-based.  If c items cannot be returned, then however many
existing items will be returned instead.

The starting index and count operands can, of course, be lists, and if they
are multiple lists will be returned iterating through one or both of the
operands as needed.
''',
'''
c:\>rpn 1 10 range 0 5 sublist
[ 1, 2, 3, 4, 5 ]

c:\>rpn 1 10 range 1 5 sublist
[ 2, 3, 4, 5, 6 ]

c:\>rpn 1 10 range 1 3 sublist
[ 2, 3, 4 ]

Print multiple sublists of 3 items each starting with the first 5 items in
the list:

c:\>rpn 1 10 range 0 4 range 3 sublist
[ [ 1, 2, 3 ], [ 2, 3, 4 ], [ 3, 4, 5 ], [ 4, 5, 6 ], [ 5, 6, 7 ] ]

Print multiple sublists of 1 to 3 items, inclusive, starting with the first
4 items in the list:

c:\>rpn 1 10 range 0 3 range 1 3 range sublist -s1
[
[ 1 ],
[ 1, 2 ],
[ 1, 2, 3 ],
[ 2 ],
[ 2, 3 ],
[ 2, 3, 4 ],
[ 3 ],
[ 3, 4 ],
[ 3, 4, 5 ],
[ 4 ],
[ 4, 5 ],
[ 4, 5, 6 ],
]
''' ],
    'subtract' : [
'arithmetic', 'subtracts k from n',
'''
This operator subtracts the first operand from the second.  If the first
operand is a list, then the second operand is subtracted from each member of
the list and the result is a list.  If the second operand is a list, then each
member of the second list is subtracted from the first operand and the result
is a list.

If both operands are lists, then each member of the second list is subtracted
from its corresponding member in the first list and the result is a list.  If
the lists are not of equal length, then the resulting list is the length of
the shorter of the two.

Subtraction is supported for measurements.
''',
'''
c:\>rpn 17 8 -
9

c:\>rpn 10 [ 1 2 3 4 ] -
[ 9, 8, 7, 6 ]

c:\>rpn 1 gallon 4 cups -
0.75 gallon
''' ],
    'sum' : [
'arithmetic', 'calculates the sum of values in list n',
'''
''',
'''
''' ],
    'sum_digits' : [
'lexicographic', 'calculates the sum of the digits of integer n',
'''
''',
'''
''' ],
    'summer_solstice' : [
'astronomy', 'calculates the time of the summer solstice for year n',
'''
''',
'''
''' ],
    'sunday' : [
'constants', 'returns 7, which is the code for Sunday',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'superfactorial' : [
'number_theory', 'calculates the superfactorial of n',
'''
''',
'''
''' ],
    'superprime' : [
'prime_numbers', 'returns the nth superprime (the nth primeth prime)',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
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

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' ],
    'tetrate' : [
'powers_and_roots', 'tetrates n by k',
'''
Tetration is the process of repeated exponentiation.  n is exponentiated by
itself k times.
''',
'''
c:\>rpn 3 3 tetrate
19683

c:\>rpn 10 10 tetrate
1.0e+1000000000

c:\>rpn 2 1 6 range tetrate
[ 2, 4, 16, 256, 65536, 4294967296 ]
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
'date', 'calculates the date of Thanksgiving (US) for the year specified',
'''
''',
'''
''' ],
    'thursday' : [
'constants', 'returns 4, which is the code for Thursday',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'timer' : [
'settings', 'set timer mode in interactive mode',
'''
''',
'''
''' ],
    'timer_mode' : [
'settings', 'set temporary timer mode in interactive mode',
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
    'topic' : [
'special', 'prints a help topic in interactive mode',
'''
''',
'''
''' ],
    'to_unix_time' : [
'conversion', 'converts from date-time list to Unix time (seconds since epoch)',
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
    'triangle_area' : [
'trigonometry', 'calculates the area of a triangle with sides of length a, b, and c',
'''
This operator uses Heron's formula, which takes the square root of the product
of the semiperimeter and the respective differences of the semiperimeter and
the lengths of each side.

area = sqrt( s( s - a )( s - b )( s - c ) )
''',
'''
c:\>rpn 3 4 5 triangle_area
6

c:\>rpn 2 3 make_pyth_3 unlist triangle_area
30
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
    'triple_balanced' : [
'prime_numbers', 'returns the nth triple balanced prime',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 triple_balanced
14907649
''' ],
    'triple_balanced_' : [
'prime_numbers', 'returns the nth triple balanced prime and its neighbors',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.  This operator also
returns the neighbors, second neighbors, and third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 triple_balanced_
[ 14907619, 14907631, 14907637, 14907649, 14907661, 14907667, 14907679 ]

c:\>rpn 10 triple_balanced_ diffs
[ 12, 6, 12, 12, 6, 12 ]
''' ],
    'triplet_prime' : [
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
only the first prime of the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 triplet_prime
101

c:\>rpn 1 10 range triplet_prime
[ 5, 7, 11, 13, 17, 37, 41, 67, 97, 101 ]
''' ],
    'triplet_prime_' : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
a list of the three primes in the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 triplet_prime_
[ 101, 103, 107 ]

c:\>rpn 1 10 range triplet_prime_
[ [ 5, 7, 11 ], [ 7, 11, 13 ], [ 11, 15, 17 ], [ 13, 17, 19 ], [ 17, 19, 23 ],
[ 37, 41, 43 ], [ 41, 43, 47 ], [ 67, 71, 73 ], [ 97, 101, 103 ],
[ 101, 103, 107 ] ]
''' ],
    'true' : [
'constants', 'used with boolean settings operators',
'''
'true' simply evaluates to 1
''',
'''
rpn (1)>5 12 **
244140625
rpn (2)>true comma
1
rpn (3)>5 12 **
244,140,625
''' ],
    'truncated_octahedral' : [
'polyhedral_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' ],
    'truncated_tetrahedral' : [
'polyhedral_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' ],
    'tuesday' : [
'constants', 'returns 2, which is the code for Tuesday',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
''' ],
    'twin_prime' : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'twin_prime_' : [
'prime_numbers', 'returns the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'uchar' : [
'conversion', 'converts the value to an unsigned 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
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
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'ulonglong' : [
'conversion', 'converts the value to an unsigned 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' ],
    'undouble' : [
'conversion', 'interprets a 64-bit integer as a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn pi double -x
4009 21fb 5444 2d18

c:\>rpn -a20 0x400921fb54442d18 undouble
3.141592653589793116
''' ],
    'unfilter' : [
'special', 'filters a list n using the inverse of function k',
'''
The function is applied to each element of the list and a new list is returned
which consists only of those elements for which the function returns a zero
value.
''',
'''
''' ],
    'unfilter_by_index' : [
'special', 'filters a list n using the inverse of function k applied to the list indexes',
'''
''',
'''
''' ],
    'unfloat' : [
'conversion', 'interprets a 32-bit integer as a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn pi float -x
4049 0fdb

c:\>rpn 0x40490fdb unfloat
3.14159274101
''' ],
    'union' : [
'list_operators', 'returns the union of two lists',
'''
''',
'''
TODO:  appends instead of makes a union, please fix
''' ],
    'unique' : [
'list_operators', 'replaces list n with a list of its unique elements',
'''
''',
'''
c:\>rpn 1 8 range 2 9 range append 3 10 range append unique
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'unit_roots' : [
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
c:\>rpn 2 unit_roots
[ 1, -1 ]

c:\>rpn 3 unit_roots
[ 1, (-0.5 + 0.86602540378443864676j), (-0.5 - 0.86602540378443864676j) ]

c:\>rpn 4 unit_roots
[ 1, (0.0 + 1.0j), -1, (0.0 - 1.0j) ]
''' ],
    'unlist' : [
'modifiers', 'expands a list into separate arguments',
'''
''',
'''
Here, we use 'unlist' to make arguments for 'euler_brick':

c:\>rpn 4 5 make_pyth_3
[ 9, 40, 41 ]

c:\>rpn 4 5 make_pyth_3 unlist euler_brick
[ 42471, 54280, 59040 ]
''' ],
    'unpack' : [
'conversion', 'unpacks an integer value n into bit fields k',
'''
''',
'''
''' ],
    'use_members' : [
'modifiers', 'instructs the next non-recursive list operation to act on list members'
'''
''',
'''
''' ],
    'ushort' : [
'conversion', 'converts the value to an unsigned 16-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
c:\>rpn 10 ushort
10

c:\>rpn 100000 ushort
34464

rjg:  Um, this is unexpected.  TODO: investigate

c:\>rpn -2000 ushort
63536
''' ],
    'value' : [
'special', 'converts a measurement to a numerical value',
'''
If a value as the result of evaluation is a measurement, i.e., contains a unit
of measurement, then this operator will evaluate that value as a number, the
numerical part of the measurement value.
''',
'''
c:\>rpn 1000 light-years value
1000
''' ],
    'vernal_equinox' : [
'astronomy', 'calculates the time of the vernal equinox for year n',
'''
''',
'''
''' ],
    'wednesday' : [
'constants', 'returns 3, which is the code for Wednesday',
'''
This constant operator is defined for convenience for use with date operators.
''',
'''
c:\>rpn 2015 august 4 wednesday nthweekday
2015-08-26
''' ],
    'weekday' : [
'conversion', 'calculates the day of the week of an absolute time',
'''
Given any date, the 'weekday' operator will determine what day of the week
that date occurred on.

This operator is special in that it returns a string.  rpn cannot use a string
as an operand, so this function cannot be combined with other operators.

*** 'weekday' does not currently work with list operands.
''',
'''
c:\>rpn today weekday
'Friday'

c:\>rpn 1776-07-04 weekday
'Thursday'

c:\>rpn 1965-03-31 weekday
'Wednesday'

c:\>rpn 2043-04-17 weekday
'Friday'
''' ],
    'winter_solstice' : [
'astronomy', 'calculates the time of the winter solstice for year n',
'''
''',
'''
''' ],
    'x' : [
'special', '\'x\' is used to create functions',
'''
Allows the user to define a function for use with the eval, nsum, nprod,
and limit operators, etc.  Basically 'x' starts an expression that
becomes a function.  As of version 6.5.0 a user-defined function must start
with 'x', but I hope to remove that limitation.

See the 'user_functions' help topic for more details.
''',
'''
c:\>rpn 3 x 2 * eval
6

c:\>rpn 5 x 2 ** 1 - eval
24

c:\>rpn inf x 1 + fib x fib / limit
1.6180339887
''' ],
    'xor' : [
'bitwise', 'calculates the bitwise \'xor\' of n and k',
'''
'xor' is the 'exclusive or' logical operation, which returns true if and only
if the two operands are different.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to '''  + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'xor'ed bits.
''',
'''
c:\>rpn -x 0xffff0000 0x12345678 xor
edcb 5678

c:\>rpn [ 0 0 1 1 ] [ 0 1 0 1 ] xor
[ 0, 1, 1, 0 ]
''' ],
    'y' : [
'special', '\'y\' is used to create functions',
'''
''',
'''
''' ],
    'ydhms' : [
'conversion', 'shortcut for \'[ year day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ year day hour minute
second ] convert' in order to convert a time interval to days, hours, minutes
and seconds.
''',
'''
''' ],
    'year_calendar' : [
'date', 'prints a month calendar for the date value',
'''
The 'year_calendar' operator is special in that what it prints out is a
side-effect.  It actually returns the date value passed in as a result, so as
far as rpn is concerned, it's an operator that does nothing.
''',
'''
''' ],
    'z' : [
'special', '\'z\' is used to create functions',
'''
''',
'''
''' ],
    'zero' : [
'list_operators', 'returns a list of the indices of elements in list n that are zero',
'''
This operator is useful for applying an operator that returns a binary value
on a list, and getting a summary of the results.

Indices are zero-based.

(see 'nonzero')
''',
'''
c:\>rpn [ 1 0 2 0 3 0 4 ] zero
[ 1, 3, 5 ]

List the non-prime Fibonacci numbers:

c:\>rpn 0 20 range fib is_prime zero fib
[ 0, 1, 1, 8, 21, 34, 55, 144, 377, 610, 987, 2584, 4181, 6765 ]
''' ],
    'zeta' : [
'number_theory', 'calculates the zeta function for n',
'''
''',
'''
''' ],
    '_dump_aliases' : [
'internal', 'dumps the list of aliases for operators',
'''
rpn maintains a list of aliases for operators and units.  As of 6.5.0, there
are almost 7000 aliases.  A lot of these are automatically generated for
metric unit types and certain compound units.  The rest are defined as manually
defined aliases for units and operator names.
''',
'''
''' ],
    '_dump_operators' : [
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_stats' : [
'internal', 'dumps rpn statistics',
'''
''',
'''
''' ],
#   'antitet' : [ findTetrahedralNumber, 1 ],
#   'bernfrac' : [ bernfrac, 1 ],
#   'powmod' : [ getPowMod, 3 ],

# operators to be sorted:

}


# //******************************************************************************
# //
# //  makeHelp
# //
# //******************************************************************************

def makeHelp( helpTopics ):
    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + g.dataDir )
    fileName = dataPath + os.sep + 'help.pckl.bz2'

    if not os.path.isdir( dataPath ):
        os.makedirs( dataPath )

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( helpTopics, pickleFile )
        pickle.dump( operatorHelp, pickleFile )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    print( 'makeHelp', PROGRAM_VERSION, '-', 'RPN command-line calculator help file generator' )
    print( COPYRIGHT_MESSAGE )
    print( )

    makeHelp( helpTopics )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

