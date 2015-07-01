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
        output in a different base (2 to 62, or phi)

    -R n, --output_radix_numerals n
        output each digit is a space-delimited base-10 number

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

c:\>rpn [ 1 2 3 ] [ 4 5 6 ] polyval
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
rpn 6.4.0 - RPN command-line calculator
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
rpn (7)>$side1 $side2 hypot
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

Added 'rand_' and 'randint_' operators.

Added the 'debruijn' operator.

Fixed several minor bugs.

6.3.0

Added the 'geomean' operator.

Added the 'argument' and 'conjugate' operators.

Fixed 'trianglearea'.  It's been wrong for a long time.  Sorry.

Added the 'fibonorial' operator.

Added the 'eulerbrick' operator.

Added the 'unlist' operator.

Added the 'makepyth3' and 'makepyth4' operators.

Added the 'equal', 'greater', 'less', 'not_equal', 'not_greater', and
'not_less' operators.

Added the 'reduce' operator.

Added the 'geomean', 'argument', 'conjugate', 'lcm' operators.

The 'pascal' operator was renamed to 'pascaltri' to avoid a collision with
the 'pascal' unit.

Fixed several minor bugs.

6.4.0

Added the 'magnetic_constant', 'electric_constant', 'rydberg_constant',
'newtons_constant' and 'fine_structure' operators.

Revamped factorization to be much, much faster.

Added 'eulerphi' operator.

Added caching for factorizations.

Added the 'sigma, 'aliquot', 'polypower', 'mobius' and 'mertens' operators.
The old 'mertens' operator was renamed to 'mertens_constant'.

Added the 'frobenius', 'slice', 'sublist', 'left' and 'right' operators.

Added 'crt' operator.
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
    192 168 0 1

Construct the square root of two from a continued fraction:

    First, here's the square root of two to 20 places:

        c:\>rpn -a20 2 sqrt
        1.4142135623730950488

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
        1.4142135623730950488

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        c:\>rpn 1 50 range fib isprime nonzero 1 + fib
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
    'aliquot' : [
'number_theory', 'returns the first k members of the aliquot sequence of n',
'''
''',
'''
''' ],
    'altfac' : [
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''' ],
    'altsign' : [
'list_operators', 'alternates signs in the list by making every even element negative',
'''
The return value is a list of the same size as the original with the sign of
every second element reversed, starting with the second.
''',
'''
c:\>rpn 1 10 range altsign
[ 1, -2, 3, -4, 5, -6, 7, -8, 9, -10 ]
''' ],
    'altsign2' : [
'list_operators', 'alternates signs in the list by making every odd element negative',
'''
The return value is a list of the same size as the original with the sign of
every other element reversed, starting with the first element.
''',
'''
c:\>rpn 1 10 range altsign2
[ -1, 2, -3, 4, -5, 6, -7, 8, -9, 10 ]

''' ],
    'altsum' : [
'arithmetic', 'calculates the alternating sum of list n (addition first)',
'''
This operator calculates the sum of the list, alternating the signs of every
second element starting with the second.

This operator is the same as using 'altsign sum'.
''',
'''
c:\>rpn 1 10 range altsign sum
-5

c:\>rpn 1 10 range altsum
-5

Calculating e:

c:\>rpn -a20 0 25 range fac 1/x altsum 1/x
2.7182818284590452354
''' ],
    'altsum2' : [
'arithmetic', 'calaculates the alternating sum of list n (subtraction first)',
'''
This operator calculates the sum of the list, alternating the signs of every
other element starting with the first.

This operator is the same as using 'altsign2 sum'.
''',
'''
c:\>rpn 1 10 range altsign2 sum
5

c:\>rpn 1 10 range altsum2
5
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
c:\>rpn -a50 -d5 apery
1.20205 69031 59594 28539 97381 61511 44999 07649 86292 3405

c:\>rpn -a50 -d5 3 zeta
1.20205 69031 59594 28539 97381 61511 44999 07649 86292 3405
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
This is defined for convenience for use with date operators.
''',
'''
c:\>rpn april
4

c:\>rpn 2015 april 3 tuesday nthweekday
2015-04-21 00:00:00
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
''',
'''
''' ],
    'august' : [
'constants', 'returns 8, which is the code for August',
'''
This is defined for convenience for use with date operators.
''',
'''
c:\>rpn august
8

c:\>rpn 2015 august 4 tuesday nthweekday
2015-08-25 00:00:00
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
    'balanced' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'balanced_' : [
'prime_numbers', 'calculates the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
c:\>rpn catalans
0.915965594177
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
c:\>rpn -a60 champernowne
0.123456789101112131415161718192021222324252627282930313233344
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
    'comma' : [
'settings', 'allows changing the comma option in interactive mode',
'''
TODO: fill me out
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
c:\>rpn 1 100 range count
100
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

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
    'debruijn' : [
'combinatorics', 'generates a deBruijn sequence of n symbols and word-size k',
'''
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
    'december' : [
'constants', 'returns 12, which is the code for December',
'''
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'decillion' : [
'constants', 'returns the constant one decillion, i.e. 1.0e33',
'''
''',
'''
''' ],
    'decimal_grouping' : [
'settings', 'TODO: describe me',
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
''',
'''
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
    'doublebal' : [
'prime_numbers', 'returns the nth double balanced prime',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
    'dup' : [
'modifiers', 'duplicates an argument n k times',
'''
This function duplicates terms, but requires the bracket operators to make the
resulting expression a list, rather than a set of k expressions.
''',
'''
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
    'egypt' : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' ],
    'election_day' : [
'date', 'calculates the date of Election Day (US) for the year specified',
'''
''',
'''
''' ],
    'electric_constant' : [
'constants', 'returns the electric constant',
'''
TODO:  explain all the other names this has
''',
'''
''' ],
    'element' : [
'list_operators', 'returns a single element from a list',
'''
''',
'''
''' ],
    'electric_constant' : [
'constants', 'returns a electic constant',
'''
''',
'''
''' ],
    'equal' : [
'arithmetic', 'returns 1 if n equals k, otherwise returns 0',
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
    'eulerbrick' : [
'number_theory', 'creates the dimensions of an Euler brick, given a Pythagorean triple',
'''
An Euler brick is a brick with three dimensions such that any two pairs form
a Pythogorean triples, therefore the face diagonals are also integers.
''',
'''
c:\>rpn 2 3 makepyth3 unlist eulerbrick
[ 828, 2035, 3120 ]

c:\>rpn 828 2035 hypot
2197

c:\>rpn 828 3120 hypot
3228

c:\>rpn 2035 3120 hypot
3725
''' ],
    'eulerphi' : [
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
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'fibonacci' : [
'number_theory', 'calculates the nth Fibonacci number',
'''
''',
'''
''' ],
    'fibonorial' : [
'number_theory', 'calculates the product of the first n Fibonacci numbers',
'''
The name is a portmanteau of 'fibonacci' and 'factorial'.
''',
'''
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

c:\>rpn -p80 1 80 range fib x isprime filter
[ 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, 433494437, 2971215073 ]
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
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'frobenius' : [
'number_theory', 'calculates the frobenius number of a list of values with gcd > 1'
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
    'geomean' : [
'list_operators', 'calculates the geometric mean of a a list of numbers n',
'''
The geometric mean is calculated by taking the kth root of the product of k
values.
''',
'''
c:\>rpn [ 1 2 ] geomean
1.41421356237

c:\>rpn [ 1 10 range ] geomean
[ 4.52872868812 ]

Calculate the geometric mean of the first n numbers from 1 to 5:

c:\>rpn [ 1 1 5 range range ] geomean
[ [ 1, 1.41421356237, 1.81712059283, 2.2133638394, 2.6051710847 ] ]
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
    'greater' : [
'arithmetic', 'returns 1 if n is greater than k, otherwise returns 0',
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
    'hyperfac' : [
'number_theory', 'calculates the hyperfactorial of n',
'''
''',
'''
''' ],
    'hypot' : [
'trigonometry', 'calculates the hypotenuse of n and k',
'''
Given a right triangle with sides of n and k, the 'hypot' operator calculates
what the length of the hypotenuse would be.
''',
'''
c:\>rpn 3 4 hypot
5

c:\>rpn 7 24 hypot
25

c:\>rpn 1 1 hypot
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
'settings', 'TODO: describe me',
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
'settings', 'TODO: describe me',
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
    'isdivisible' : [
'arithmetic', 'returns whether n is n divisible by k',
'''
''',
'''
''' ],
    'iso_day' : [
'date', 'returns the ISO day and week for a time value',
'''
''',
'''
''' ],
    'isolated' : [
'prime_numbers', 'returns the nth isolated prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
This is defined for convenience for use with date operators.
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
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'june' : [
'constants', 'returns 6, which is the code for June',
'''
This is defined for convenience for use with date operators.
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
'settings', 'TODO:',
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
    'less' : [
'arithmetic', 'returns 1 if n is less than k, otherwise returns 0',
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
'jacobsthal', 'repunit', 'hepttri', 'heptsquare', and 'nonahex' operators.
''',
'''
The 250th Fibonacci number:

c:\>rpn -c -a55 [ 1 1 ] [ 1 1 ] 250 linearrecur
7,896,325,826,131,730,509,282,738,943,634,332,893,686,268,675,876,375

The Fibonacci sequence:

c:\>rpn [ 1 1 ] [ 0 1 ] 1 18 range linearrecur
[ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597 ]

The Tribonacci sequence:

c:\>rpn [ 1 1 1 ] [ 0 0 1 ] 1 18 range linearrecur
[ 0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768 ]

The Octanacci sequence:

c:\>rpn [ 1 8 dup ] [ 0 7 dup 1 ] 1 20 range linear
[ 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 4, 8, 16, 32, 64, 128, 255, 509, 1016, 2028 ]

The Pell numbers:

c:\>rpn [ 1 2 ] [ 0 1 ] 1 15 range linearrecur
[ 0, 1, 2, 5, 12, 29, 70, 169, 408, 985, 2378, 5741, 13860, 33461, 80782 ]

The Perrin sequence:

c:\>rpn [ 1 1 0 ] [ 3 0 2 ] 1 20 range linearrecur
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
    'magnetic_constant' : [
'constants', 'returns the magnetic constant',
'''
TODO:  explain all the other names this has
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
    'makepyth3' : [
'conversion', 'makes a pythagorean triple given two integers, n and k, as seeds',
'''
''',
'''
''' ],
    'makepyth4' : [
'conversion', 'makes a pythagorean quadruple given two integers, n and k, as seeds',
'''
n and k cannot both be odd.
''',
'''
''' ],
    'maketime' : [
'conversion', 'interpret argument as absolute time',
'''
''',
'''
''' ],
    'march' : [
'constants', 'returns 3, which is the code for March',
'''
This is defined for convenience for use with date operators.
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
    'maxdouble' : [
'conversion', 'returns the largest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn maxdouble
1.79769313486e308

c:\>rpn maxdouble double -x
7fef ffff ffff ffff
''' ],
    'maxfloat' : [
'conversion', 'returns the largest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn maxfloat
3.40282346639e38

c:\>rpn maxfloat float -x
7f7f ffff
''' ],
    'maxindex' : [
'list_operators', 'returns the index of largest value in list n',
'''
''',
'''
''' ],
    'maxlong' : [
'conversion', 'returns the maximum 32-bit signed integer',
'''
This is the largest number that can be represented by a 32-bit signed
integer assuming two's complement representation.

''',
'''
c:\>rpn maxlong
2147483647

When does a 32-bit time_t wrap?

c:\>rpn 1970-01-01 maxlong seconds +
2038-01-19 03:14:07
''' ],
    'maxlonglong' : [
'conversion', 'returns the maximum 64-bit signed integer',
'''
This is the largest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn maxlonglong
9223372036854775807

When does a 64-bit time_t wrap?

c:\>rpn 1970-01-01 maxlonglong seconds +
rpn:  value is out of range to be converted into a time
0

c:\>rpn -c maxlonglong seconds years convert
292,271,023,045 years

Not for a long while...
''' ],
    'maxquadlong' : [
'conversion', 'returns the maximum 128-bit signed integer',
'''
This is the largest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
''' ],
    'maxshort' : [
'conversion', 'returns the maximum 16-bit signed integer',
'''
This is the largest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
''' ],
    'maxuchar' : [
'conversion', 'returns the maximum 8-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
''' ],
    'maxulong' : [
'conversion', 'returns the maximum 32-bit unsigned integer',
'''
This is the largest number that can be represented by a 32-bit unsigned
integer.
''',
'''
''' ],
    'maxulonglong' : [
'conversion', 'returns the maximum 64-bit unsigned integer',
'''
This is the largest number that can be represented by a 64-bit unsigned
integer.
''',
'''
''' ],
    'maxuquadlong' : [
'conversion', 'returns the maximum 128-bit unsigned integer',
'''
This is the largest number that can be represented by a 128-bit unsigned
integer.
''',
'''
''' ],
    'maxushort' : [
'conversion', 'returns the maximum 16-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
''' ],
    'may' : [
'constants', 'returns 5, which is the code for May',
'''
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'mean' : [
'arithmetic', 'calculates the mean of values in list n',
'''
''',
'''
''' ],
    'memorial_day' : [
'date', 'calculates the date of Memorial Day (US) for the year specified',
'''
''',
'''
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
    'minchar' : [
'conversion', 'returns the minimum 8-bit signed integer',
'''
This is the smallest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn minchar
-128

c:\>rpn minchar -x
-0080

c:\>rpn maxchar minchar -
255
''' ],
    'mindouble' : [
'conversion', 'returns the smallest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn mindouble
2.22507385851e-308

c:\>rpn mindouble double -x
0010 0000 0000 0000
''' ],
    'minfloat' : [
'conversion', 'returns the smallest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
c:\>rpn minfloat
1.17549435082e-38

c:\>rpn minfloat float -x
0080 0000
''' ],
    'minindex' : [
'list_operators', 'returns the index of smallest value in list n',
'''
''',
'''
''' ],
    'minlong' : [
'conversion', 'returns the minimum 32-bit signed integer',
'''
This is the smallest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn minlong
-2147483648

c:\>rpn maxlong minlong -
4294967295
''' ],
    'minlonglong' : [
'conversion', 'returns the minimum 64-bit signed integer',
'''
This is the smallest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn minlonglong
-9223372036854775808

c:\>rpn maxlonglong minlonglong - 1 + log2
64
''' ],
    'minquadlong' : [
'conversion', 'returns the minimum 128-bit signed integer',
'''
This is the smallest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn minquadlong
-170141183460469231731687303715884105728

c:\>rpn maxquadlong minquadlong - 1 + log2
128
''' ],
    'minshort' : [
'conversion', 'returns the minimum 16-bit signed integer',
'''
This is the smallest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
c:\>rpn minshort
-32768

c:\>rpn maxshort minshort -
65535
''' ],
    'minuchar' : [
'conversion', 'returns the minimum 8-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn minuchar
0

c:\>rpn maxuchar minuchar -
255
''' ],
    'minulong' : [
'conversion', 'returns the minimum 32-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn minulong
0

c:\>rpn maxulong minulong - 1 + log2
32
''' ],
    'minulonglong' : [
'conversion', 'returns the minimum 64-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn minulonglong
0

c:\>rpn maxulonglong minulonglong - 1 + log2
64
''' ],
    'minuquadlong' : [
'conversion', 'returns the minimum 128-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn minuquadlong
0

c:\>rpn maxuquadlong minuquadlong - 1 + log2
128
''' ],
    'minushort' : [
'conversion', 'returns the minimum 16-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
c:\>rpn minushort
0

c:\>rpn maxushort minushort -
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
This is defined for convenience for use with date operators.
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
    'newtons_constant' : [
'constants', 'returns Newton\'s gravitational constant',
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
    'not_equal' : [
'arithmetic', 'returns 1 if n does not equal k, otherwise returns 0',
'''
''',
'''
''' ],
    'not_greater' : [
'arithmetic', 'returns 1 if n is not greater than k, otherwise returns 0',
'''
''',
'''
''' ],
    'not_less' : [
'arithmetic', 'returns 1 if n is not less than k, otherwise returns 0',
'''
''',
'''
''' ],
    'november' : [
'constants', 'returns 11, which is the code for November',
'''
This is defined for convenience for use with date operators.
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
'date', 'finds the nth day (1 = Monday, etc.) of the month',
'''
a = four-digit year, b = month (1-12), c = week (1-5 for first through 5th),
d = day (1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''' ],
    'nthweekdayofyear' : [
'date', 'finds the nth day (1 = Monday) of the year',
'''
a = four-digit year, b = week (negative values count from the end), c = day
(1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''' ],
    'nthprime?' : [
'prime_numbers', 'finds the index of the closest prime over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'nthquad?' : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
    'octal_mode' : [
'settings', 'set temporary octal mode in interactive mode',
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
    'october' : [
'constants', 'returns 10, which is the code for October',
'''
This is defined for convenience for use with date operators.
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
    'oeiscomment' : [
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
    'oeisex' : [
'special', 'downloads the comment field for the OEIS integer series n',
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
    'oeisname' : [
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
'logical', 'calculates the bitwise \'or\' of n and k',
'''
''',
'''
''' ],
    'output_radix' : [
'settings', 'TODO: describe me',
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
'logical', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
''',
'''
''' ],
    'pascaltri' : [
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
    'pentsquare' : [
'polygonal_numbers', 'calculates the nth pentagonal square number',
'''
''',
'''
''' ],
    'penttri' : [
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
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
    'polyval' : [
'algebra', 'interprets the list as a polynomial and evaluates it for value k',
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
'settings', 'TODO: describe me',
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
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primepi' : [
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primes' : [
'prime_numbers', 'generates a range of k primes starting from index n',
'''
This operator is much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'primorial' : [
'prime_numbers', 'calculates the nth primorial',
'''
This function calculates the product of the first n prime numbers.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
    'quadprime?' : [
'prime_numbers', 'finds the closest set of quadruplet primes above n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quadprime' : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quadprime_' : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
    'quintprime' : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'quintprime_' : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'radians' : [
'trigonometry', 'interprets n as radians and converts to degrees',
'''
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
    'randint' : [
'special', 'returns a random integer from 0 to n - 1',
'''
''',
'''
''' ],
    'randint_' : [
'special', 'returns a list of k random integers from 0 to n - 1',
'''

''',
'''
Test the birthday paradox:

rpn -D 365 23 randint_ sort

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
    'safeprime' : [
'prime_numbers', 'returns the nth safe prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'saturday' : [
'constants', 'returns 6, which is the code for Saturday',
'''
This is defined for convenience for use with date operators.
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
    'september' : [
'constants', 'returns 9, which is the code for September',
'''
This is defined for convenience for use with date operators.
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
    'sextprime' : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sextprime_' : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexyprime' : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns the smaller of
nth set of sexy primes, so the value of the result + 6 will also be prime.
''',
'''
c:\>rpn 16387 sexyprime
1000033

c:\>rpn 1 10 range sexyprime
[ 5, 7, 11, 13, 17, 23, 31, 37, 41, 47 ]
''' ],
    'sexyprime_' : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns both members
of the nth set of sexy primes, which will differ by 6.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 213819 sexyprime_
[ 20000063, 20000069 ]

c:\>rpn 1001 1010 range sexyprime_
[ [ 31957, 31963 ], [ 32003, 32009 ], [ 32051, 32057 ], [ 32057, 32063 ],
[ 32063, 32069 ], [ 32077, 32083 ], [ 32083, 32089 ], [ 32183, 32189 ],
[ 32251, 32257 ], [ 32297, 32303 ] ]
''' ],
    'sexytriplet' : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexytriplet_' : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexyquad' : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'sexyquad_' : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'short' : [
'conversion', 'converts the value to a signed 16-bit integer',
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
    'sophieprime' : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
    'stefan_boltzmann' : [
'constants', 'returns the Stefan-Boltzmann constant',
'''
''',
'''
c:\>rpn stefan_boltzmann
5.670373e-8 watts per meter^2 kelvin^4
''' ],
    'steloct' : [
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
    'subfac' : [
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
    'sunday' : [
'constants', 'returns 7, which is the code for Sunday',
'''
This is defined for convenience for use with date operators.
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

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
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
'date', 'calculates the date of Thanksgiving (US) for the year specified',
'''
''',
'''
''' ],
    'thursday' : [
'constants', 'returns 4, which is the code for Thursday',
'''
This is defined for convenience for use with date operators.
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
    'tounixtime' : [
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
    'trianglearea' : [
'trigonometry', 'calculates the area of a triangle with sides of length a, b, and c',
'''
This operator uses Heron's formula, which takes the square root of the product
of the semiperimeter and the respective differences of the semiperimeter and
the lengths of each side.

area = sqrt( s( s - a )( s - b )( s - c ) )
''',
'''
c:\>rpn 3 4 5 trianglearea
6

c:\>rpn 2 3 makepyth3 unlist trianglearea
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
    'triplebal' : [
'prime_numbers', 'returns the nth triple balanced prime',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
only the first prime of the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 tripletprime
101

c:\>rpn 1 10 range tripletprime
[ 5, 7, 11, 13, 17, 37, 41, 67, 97, 101 ]
''' ],
    'tripletprime_' : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
a list of the three primes in the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
c:\>rpn 10 tripletprime_
[ 101, 103, 107 ]

c:\>rpn 1 10 range tripletprime_
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
This is defined for convenience for use with date operators.
''',
'''
''' ],
    'twinprime' : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
''',
'''
''' ],
    'twinprime_' : [
'prime_numbers', 'returns the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in rpndata/ and is
distributed with data files calculated through the first billion primes.
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
    'unlist' : [
'list_operators', 'expands a list into separate arguments',
'''
''',
'''
''' ],
    'union' : [
'list_operators', 'returns the union of two lists',
'''
''',
'''
c:\>rpn 2 3 makepyth3 unlist trianglearea
30
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
If a value as the result of evaluation is a measurement, i.e., contains a unit
of measurement, then this operator will evaluate that value as a number, the
numerical part of the measurement value.
''',
'''
c:\>rpn 1000 light-years value
1000
''' ],
    'wednesday' : [
'constants', 'returns 3, which is the code for Wednesday',
'''
This is defined for convenience for use with date operators.
''',
'''
c:\>rpn 2015 august 4 wednesday nthweekday
2015-08-26 00:00:00
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

}


# //******************************************************************************
# //
# //  makeHelp
# //
# //******************************************************************************

def makeHelp( helpTopics ):
    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
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

