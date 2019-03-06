#!/usr/bin/env python

# //******************************************************************************
# //
# //  makeHelp
# //
# //  RPN command-line calculator help file generator
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import shlex
import six

import argparse
import bz2
import contextlib
import io
import pickle
import os
import sys

from pathlib import Path

from rpn.rpn import rpn, handleOutput
from rpn.rpnUtils import getDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE, \
                           PROGRAM_NAME, RPN_PROGRAM_NAME

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'makeHelp'
PROGRAM_DESCRIPTION = 'RPN command-line calculator help generator'

maxExampleCount = 1278


print( 'makeHelp' + PROGRAM_VERSION_STRING + 'RPN command-line calculator help file generator' )
print( COPYRIGHT_MESSAGE )
print( )

parser = argparse.ArgumentParser( prog = PROGRAM_NAME, description = RPN_PROGRAM_NAME + ' - ' +
                                  PROGRAM_DESCRIPTION + COPYRIGHT_MESSAGE,
                                  add_help = False,
                                  formatter_class = argparse.RawTextHelpFormatter,
                                  prefix_chars = '-' )

parser.add_argument( '-d', '--debug', action = 'store_true' )

args = parser.parse_args( sys.argv[ 1 : ] )

helpDebugMode = args.debug

exampleCount = 0


# //******************************************************************************
# //
# //  makeCommandExample
# //
# //******************************************************************************

def makeCommandExample( command, indent=0, slow=False ):
    '''
    You know, it didn't occur to me for years that I should make the help
    actually use rpn to run the examples.  This way, when things change,
    the output is always accurate.
    '''
    global exampleCount
    exampleCount += 1

    if not command:
        return ''

    # This total count needs to be manually updated when the help examples are modified.
    global maxExampleCount
    #print( command )
    print( '\rGenerating example: ', exampleCount, 'of', maxExampleCount, end='' )
    #print( )

    if slow:
        print( '  (please be patient...)', end='', flush=True )

    output = io.StringIO( )

    global helpDebugMode
    if helpDebugMode:
        print( )
        print( command )

    print( ' ' * indent + 'c:\\>rpn ' + command, file=output )

    handleOutput( rpn( shlex.split( command.replace( '\\', '\\\\' ) ) ), indent=indent, file=output )

    if slow:
        print( '\r', ' ' * 55, end='' )

    result = output.getvalue( )
    output.close( )

    return result


# //******************************************************************************
# //
# //  basic help categories
# //
# //******************************************************************************

#    -e, --profile
#        gather performance statistics
#


helpTopics = {
    'options' :
    'rpn' + PROGRAM_VERSION_STRING + PROGRAM_DESCRIPTION + '\n' +
    COPYRIGHT_MESSAGE + '\n\n' +
    '''
command-line options:

    -a[n], --output_accuracy [n]
        maximum number of decimal places to display, irrespective of internal
        precision (default: ''' + str( g.defaultOutputAccuracy ) + ')' + '''

    -bn : --input_radix n
        specify the radix for input (default: ''' + str( g.defaultInputRadix ) + ')' + '''

    -c, --comma
        add commas to result, e.g., 1,234,567.0

    -d[n], --decimal_grouping [n]
        display decimal places separated into groups (default: ''' + str( g.defaultDecimalGrouping ) + ')' + '''

    -D, --DEBUG
        output debugging information

    -E, --echo_command
        echoes the command line options (so can they can be included in redirected output)

    -g[n], --integer_grouping [n]
        display integer separated into groups (default: ''' + str( g.defaultIntegerGrouping ) + ')' + '''

    -h, --help
        displays basic help information

    -i, --identify
        identify the result (may just repeat input)

    -I, --ignore_cache
         ignore cached results, and recalculates values, then updates cache

    -ln, --line_length
        line length to use for formatting help (default: ''' + str( g.defaultLineLength ) + ')' + '''

    -mn, --maximum_fixed (default: ''' + str( g.defaultMaximumFixed ) + ')' + '''
        the maximum number of decimal places to show fixed notation (e.g., if
        -m8 is set, then any value smaller 1.0e-8 will be displayed with
        scientific notation),

    -nstr, --numerals str
        characters set to use as numerals for output, '-' can be used for range (e.g., -na-z)

    -o, --octal
        octal mode: equivalent to \'-r8 -w9 -i3 -z\'

    -pn, --precision n
        precision, i.e., number of significant digits to use

    -rn, --output_radix n
        output in a different base (2 to 62, fib, fac, fac2, tri, sqr, lucas, primorial,
        e, pi, phi, sqrt2 )

        Please note that rpn doesn't use scientific notation with -r, so if the
        number being converted exceeds the accuracy setting, it will appear to
        be converted accurately.

    -sn, --list_format_level n
        output lists with one item per line, up to n levels deep of nested lists

    -t, --timer
        display calculation time

    -v, --verbose
        output status messages when factoring

    -w[n], --bitwise_group_size [n]
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
''' + makeCommandExample( '2 2 + ', indent=4 ) + '''
( 5 + 6 ) * ( 7 + 8 )
''' + makeCommandExample( '5 6 + 7 8 + *', indent=4 ) + '''
3 sqrt( 2 ) / 4:
''' + makeCommandExample( '3 2 sqrt * 4 /', indent=4 ) + '''
Lists are specified using the bracket operators.  Most operators can take
lists as operands, which results in the operation being performed on each
item in the list.  If the operator takes two or more operands, then any
operand can be a list.  If one operand is a list and the other is a single
value, then each value in the list will have the single operand applied to
it with the operator, and the result will be displayed as a list.
''' + makeCommandExample( '[ 2 3 4 5 6 ] 10 +', indent=4 ) + '''
''' + makeCommandExample( '7 [ 1 2 3 4 5 6 7 ] *', indent=4 ) + '''
If both operands are lists, then each element from the first list is applied
to the corresponding element in the second list.  If one list is shorter than
the other, then only that many elements will have the operator applied and the
resulting list will only be as long as the shorter list.  The rest of the
items in the longer list are ignored.
''' + makeCommandExample( '[ 1 2 3 4 5 6 7 ] [ 1 2 3 4 5 6 7 ] **', indent=4 ) + '''
''' + makeCommandExample( '[ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *', indent=4 ) +   '''
Some operators take lists as operands 'natively'.  This means the operator
requires a list, because the operation does not make sense for a single
value.  For example, 'mean' averages the values of a list.  If the
required list argument is a single value, rpn will promote it to a list.
''' + makeCommandExample( '1 mean', indent=4 ) + '''
If the list operator takes a list and a non-list argument, then the non-list
argument can be a list, and rpn will evaluate the operator for all values in
the list.
''' + makeCommandExample( '[ 1 2 3 ] [ 4 5 6 ] eval_poly', indent=4 ) + '''
List operands can also themselves be composed of lists and rpn will recurse.
''' + makeCommandExample( '[ [ 1 2 3 ] [ 4 5 6 ] [ 2 3 5 ] ] mean', indent=4 ) + '''
This becomes more powerful when used with operators that return lists, such as
the 'range' operator.  Here is an rpn expression that calculates the first 10
harmonic numbers:
''' + makeCommandExample( '1 1 10 range range 1/x sum', indent=4 ),
    'input' :
    '''
For integers, rpn understands hexidecimal input of the form '0x...'.
''' + makeCommandExample( 'rpn 0x10', indent=4 ) + '''
A number consisting solely of 0s and 1s with a trailing 'b' or 'B' is
interpreted as binary.
''' + makeCommandExample( 'rpn 101b', indent=4 ) + '''
''' + makeCommandExample( '011b', indent=4 ) + '''
Otherwise, a leading '0' is interpreted as octal.
''' + makeCommandExample( '030', indent=4 ) + '''
''' + makeCommandExample( '0101', indent=4 ) + '''
Decimal points are not allowed for binary, octal or hexadecimal modes,
but fractional numbers in bases other than 10 can be input using -b.
''' + makeCommandExample( '14.5 -b6', indent=4 ) + '''
''' + makeCommandExample( 'hello.hi -b36', indent=4 ) + '''
A leading '\\' forces the term to be interpreted as a number rather than an
operator (for use with higher bases with -b).
''' + makeCommandExample( '\\add -b20', indent=4 ) + '''
    ''',
    'settings' :
    '''
Configuration Settings:
    ''',
    'output' :
    '''
[ TODO: describe output formats supported by rpn ]

For now, go to 'rpn help options' and see -a, -c, -d, -g, -l, -m, -o, -r,
-s, -t, -v, -w, -x, and -z,
    ''',
    'time_features' :
    '''
[ TODO: describe time features supported by rpn ]

For now, here are some examples:

operators:
''' + makeCommandExample( 'now', indent=4 ) + '''
''' + makeCommandExample( 'today', indent=4 ) + '''
ISO-8601 format ("YYYY-MM-DD[T| ][HH:mm:SS]", no timezones):
''' + makeCommandExample( '2014-09-02T13:36:28', indent=4 ) + '''
''' + makeCommandExample( '"2014-09-02 13:36:28"', indent=4 ) + '''
''' + makeCommandExample( '2014-09-02', indent=4 ) + '''
'make_datetime' operator:
''' + makeCommandExample( '[ 2014 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 28 ] make_datetime', indent=4 ) + '''
How many days old am I?
''' + makeCommandExample( 'today 1965-03-31 -', indent=4 ) + '''
When will I be 20,000 days old?
''' + makeCommandExample( '1965-03-31 20000 days +', indent=4 ) + '''
How many seconds old is my oldest son (to within a few minutes)?
''' + makeCommandExample( '-c now "1994-03-06 06:20:00" - seconds convert', indent=4 ) + '''
What day of the week was I born on?
''' + makeCommandExample( '1965-03-31 weekday', indent=4 ) + '''
How many days until Christmas?
''' + makeCommandExample( '2016-12-25 today -', indent=4 ) + '''
How many days older am I than my first child?
''' + makeCommandExample( '1994-03-06 1965-03-31 -', indent=4 ) + '''
What date is 4 weeks from now?
''' + makeCommandExample( 'today 4 weeks +', indent=4 ) + '''
What date is 4 months from now?
''' + makeCommandExample( 'today 4 months +', indent=4 ) + '''
What about 6 months from 2 days ago?
''' + makeCommandExample( 'today 2 days - 6 months +', indent=4 ) + '''
There is no February 30, so we use the real last day of the month.  Months
are handled differently from the other time units with respect to time math
because they can differ in length.

However, the month as an absolute unit of time is simply equated to 30
days:
''' + makeCommandExample( 'month days convert', indent=4 ) + '''
How long was the summer in 2015?
''' + makeCommandExample( '2015 autumnal_equinox 2015 summer_solstice - dhms', indent=4 ),
    'user_functions' :
    '''
This feature allows the user to define a function for use with the eval, nsum,
nprod, limit and limitn operators, etc.  'lambda' starts an expression that
becomes a function.

rpn user fuctions can use up to 3 variables, x, y, and z.  rpn provides a
number of operators that can be used with user functions.  See, 'rpn help
functions' for information about these operators.

User functions cannot currently contain lists or measurements.

Some examples:
''' + makeCommandExample( '3 lambda x 2 * eval', indent=4 ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval', indent=4 ) + '''
''' + makeCommandExample( 'inf lambda x 1 + fib x fib / limit', indent=4 ) + '''
''' + makeCommandExample( '1 inf lambda 2 x ** 1/x nsum', indent=4 ) + '''
What 5-digit number when preceded by a 1 is 1/3 the value of the same 5-digit
number with a 1 added on the end?
''' + makeCommandExample( '-t [d:5] build_numbers lambda 1 x add_digits x 1 add_digits / 1 3 / is_equal filter', indent=4, slow=True ) + '''
And we can check that our result works:
''' + makeCommandExample( '428571 142857 /', indent=4 ) + '''
Here's a list of the first 10 perfect numbers:
''' + makeCommandExample( '-a60 1 10 range lambda x mersenne 2 x mersenne 1 + log2 1 - ** * eval' ) + '''
Here's proof they are perfect (i.e., the results are identical):
''' + makeCommandExample( '-a60 1 10 range lambda x mersenne 2 x mersenne 1 + log2 1 - ** * eval sigma 2 /' ),

    'unit_conversion' :
    '''
[ TODO: describe unit conversions in rpn ]

For now, here are some examples:
''' + makeCommandExample( '10 miles km convert', indent=4 ) + '''
''' + makeCommandExample( '2 gallons cups convert', indent=4 ) + '''
''' + makeCommandExample( '153 pounds stone convert', indent=4 ) + '''
''' + makeCommandExample( 'usb1 kilobit/second', indent=4 ) + '''
''' + makeCommandExample( '60 miles hour / furlongs fortnight / convert', indent=4 ) + '''
''' + makeCommandExample( '10 tons estimate', indent=4 ) + '''
''' + makeCommandExample( '78 kg [ pound ounce ] convert', indent=4 ) + '''
''' + makeCommandExample( '150,000 seconds [ day hour minute second ] convert', indent=4 ) + '''
There's a slight rounding error that I'd really like to fix.

What is the radius of a sphere needed to hold 8 fluid ounces?
''' + makeCommandExample( '8 floz sphere_radius inch convert', indent=4 ) + '''
What is the volume of a sphere with a surface area of 100 square inches?
''' + makeCommandExample( '100 square_inches sphere_volume cubic_inches convert', indent=4 ) + '''
What is the temperature of a black hole with the same mass as the sun?
''' + makeCommandExample( 'h_bar c 3 ** * [ 8 pi G boltzmann sun_mass ] prod /', indent=4 ) + '''
And what is the radius of the black hole (i.e., the Schwartzchild radius)?
''' + makeCommandExample( '[ 2 G sun_mass ] prod c sqr /', indent=4 ) + '''
What is the Planck length?
''' + makeCommandExample( 'h_bar G * c 3 ** / sqrt', indent=4 ) + '''
What is the Planck temperature?
''' + makeCommandExample( 'h_bar c 5 ** * G boltzmann sqr * / sqrt', indent=4 ) + '''
What is the Planck energy?
''' + makeCommandExample( 'h_bar c 5 ** * G / sqrt joule convert', indent=4 ) + '''
What is the Planck mass?
''' + makeCommandExample( 'h_bar c * G / sqrt', indent=4 ) + '''
What is the Planck time?
''' + makeCommandExample( 'h_bar G * c 5 ** / sqrt', indent=4 ) + '''
And how does the surface gravity of that black hole compare to Earth's?
''' + makeCommandExample( '-c -a20 G sun_mass * 2954.17769868 meters sqr / gee /', indent=4 ) + '''
What is the age of the universe based on a Hubble constant of 67.8
km/second*Mpc?
''' + makeCommandExample( '-c 67.8 km second Mpc * / invert years convert', indent=4 ) + '''
What is the acceleration due to gravity at the Earth's surface?
''' + makeCommandExample( 'G earth_mass * earth_radius 2 ** /', indent=4 ) + '''
What is the escape velocity from the Earth's surface?
''' + makeCommandExample( '2 G * earth_mass * earth_radius / sqrt', indent=4 ) + '''
Obviously, this doesn't take air resistance into account.

What is the orbital velocity of a satellite orbiting the Earth at an altitude
of 640 kilometers?
''' + makeCommandExample( 'G earth_mass * earth_radius 640 km + / sqrt mph convert', indent=4 ) + '''
What is the altitude from the Earth's surface of an object in geosynchronous
orbit?
''' + makeCommandExample( '[ 24 hours sqr G earth_mass ] prod 4 pi sqr * / cube_root miles convert earth_radius -', indent=4 ) + '''
Or better yet, there's now an operator for that:
''' + makeCommandExample( '24 hours earth_mass orbital_radius earth_radius - miles convert', 4 ) + '''
I tried to make the unit conversion flexible and smart.  It is... sometimes.
''' + makeCommandExample( '16800 mA hours * 5 volts * joule convert', indent=4 ) + '''
''' + makeCommandExample( 'gigaparsec barn * cubic_inches convert', indent=4 ) + '''
''' + makeCommandExample( 'cubic_inches gigaparsec barn * convert', indent=4 ) + '''
And sometimes it isn't.

This is a long-standing deficiency in the design.  I've struggled to figure
out to support more compound unit conversions through dimensional analysis.

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
rpn 7.0.0 - RPN command-line calculator
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

decimal_grouping:  Sets the decimal grouping number.  This is equivalent to the
'-d' command-line option.

hex_mode:  Aliased to '-x'.

identify:  Attempts to find an algebraic representation of the result.  This is
equivalent to the '-i" command-line option.

identify_mode:  Aliased to '-i'.

input_radix:

integer_grouping:

leading_zero:

leading_zero_mode:  Aliased to '-z'.

octal_mode:  Aliased to '-o'.

output_radix:  s

precision:

The precision will not be set lower than the accuracy + 2.

timer:  The timer function prints out the time taken for each operation.

timer_mode:  Turns on the timer for the next operation.  Aliased to '-t'.
    ''',
    'about' :
    PROGRAM_NAME + PROGRAM_VERSION_STRING + PROGRAM_DESCRIPTION + '\n' +
    COPYRIGHT_MESSAGE +
    '''

rpn is a command-line Reverse-Polish Notation calculator that was first
written in C in 1988.  It was rewritten in Python 3 in 2012 and now uses the
mpmath library.  It was a Python-learning exercise for me, and a fun little
toy, but when I found mpmath, it became really cool and powerful, so props
to Fredrik Johansson, who did all the heavy lifting (http://mpmath.org).  I
subsequently added support for unit conversions that rivals the GNU units app
and lots of other cool features thanks to the wealth of Python libraries.
    ''',
    'bugs' :
    '''
Perhaps the worst bug is the some operations that use generators still manage
to rack up astronomical memory usage.  I haven't been able to figure out how
this happens, but it's probably something stupid on my part.

Using 'for_each' on a nested list should give a nice error message.

Using 'for_each_list' on a non-nested list crashes.

-i doesn't work for lists.

It is not currently possible to convert between hertz and 1/second.  The
dimensional analysis fails.  This is one of only 2 instances where two
different types are so related (i.e., one is the reciprocal of the other).
The other instance is 'ohm' and 'mho'.

'(' and ')' (multiple operators) don't work with generators because the
generator only works once.

'collate' does not work with generators.

'unlist' doesn't seem to do anything any more.

Chained calls to 'next_new_moon' give the same answer over and over.  Other
related operators probably do the same thing.

-d needs to parse out the scientific notation part of the value

Converting negative numbers to different bases gives weird answers.

-u doesn't work with complex numbers

'result' doesn't work with measurements.

Date comparisons before the epoch (1970-01-01) don't work.  It seems to be a
limitation of the Arrow class.

User-defined functions can't include units.

Transitive conversions with units that require special functions don't work.

"rpn 1 1 4 range range 10 15 range 1 3 range range2" crashes because
operators that take more than 2 arguments don't handle recursive list
arguments.

Complex numbers don't obey the accuracy level on output (-a).

Cousin primes seem to be broken starting with index 99, according to OEIS.

'duplicate_ops' flat out doesn't work any more.

'reversal_addition' doesn't work with generators.

See 'rpn help TODO'.
    ''',
    'TODO' :
    '''
This is my informal, short-term todo list for rpn.  It often grows and seldom
gets smaller.

*  'humanize' - like 'name' but only 2 significant digits when > 1000
*  'name' should handle fractions smaller than 1 gracefully (right now it prints nothing)
*  support date comparisons, etc. before the epoch
*  create an output handler for RPNLocation
*  'result' doesn't work with measurements
*  https://en.wikipedia.org/wiki/American_wire_gauge
*  'rpn 1 20 range dBm kilowatt convert' fails.  This conversion doesn't work because dBm to watt uses a special function.
*  'mean' should work with measurements
*  units aren't supported in user-defined functions
*  http://en.wikipedia.org/wiki/Physical_constant
*  http://stackoverflow.com/questions/14698104/how-to-predict-tides-using-harmonic-constants
*  OEIS comment text occasionally contains non-ASCII characters, and rpn chokes on that
*  *_primes_ operators seem to be unreasonably slow
*  'fraction' needs to figure out what precision is needed and set it itself

Long-term goals

*  Performance, performance, performance.  There's a lot of functionality in rpn which is way too slow.
*  This is a big one, and may not be possible with the current syntax, but I would love to support nested lambdas.
*  Turn rpn into a full-blown scripting language.  It's 2/3 of the way there.  Why not go all the way?
*  Redesign the parsing logic.  It's excessively complex has lots of edge cases where it breaks down.
*  Lambdas are converted into Python code, compiled and run.  Perhaps all expressions should work this way.

See 'rpn help bugs'.
    ''',
    'old_release_notes' :
    '''
See git for changes prior to 5.18.1.

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

Fixed the list operator parsing so 'polynomial_product' and 'polynomial_sum'
work correctly.

5.20.3

Made a fix to improve rpn's reporting of the argument in question when there
is an error.  It's probably not 100% correct yet.

5.20.4

rpn now correctly reports the argument in question on any error.

5.20.5

rpn now throws an error when attempting to get the 0th or less prime number.

5.20.6

The 'next_prime' operator wasn't working correctly for small values.

5.20.7

Added help for unit types.   Help for individual units will come eventually,
but they are pretty self-explanatory.

5.21.0

The long-awaited absolute time feature:  rpn can now handle absolute time
values.  For input, just use ISO 8601 format, or a reasonable subset thereof.
There is also the 'make_datetime' operator, which takes a list similar to the
old 'tounixtime' operator.

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

Experimental support for mpmath plotting functionality using the new
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

Added the 'faraday_constant', 'radiation_constant' and
'stefan_boltzmann_constant' operators.

Added the 'magnetic_constant', 'electric_constant', 'rydberg_constant',
'newton_constant' and 'fine_structure_constant' operators.

Revamped factorization to be much, much faster.

Added 'euler_phi' operator.

Added caching for factorizations.

Added the 'sigma, 'aliquot', 'polynomial_power', 'mobius' and 'merten'
operators.  The old 'merten' operator was renamed to 'merten_constant'.

Added the 'frobenius', 'slice', 'sublist', 'left' and 'right' operators.

Added 'crt' operator.

...and the usual bug fixes.

7.0.0

Added the 'hexagonal_square' operator.

Added the 'duplicate_operator', 'add_digits', and 'duplicate_digits' operators.

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

Added the 'eddington_number' operator... just a fun historical oddity.

Added a new operator category:  Astronomy (thanks to pyephem).  Added the
'vernal_equinox', 'summer_solstice', 'autumnal_equinox', and 'winter_solstice'
operators.

Added 'next_new_moon', 'next_first_quarter_moon', 'next_full_moon',
'next_last_quarter_moon', 'previous_new_moon', 'previous_first_quarter_moon',
'previous_full_moon', 'previous_last_quarter_moon' and 'moon_phase' operators.

Added 'sunrise', 'sunset', 'moonrise', 'moonset', 'sun_transit',
'sun_antitransit', 'moon_transit', 'moon_antitransit', 'dawn', 'dusk',
'nautical_dawn', 'nautical_dusk', 'astronomical_dawn', 'astronomical_dusk',
'next_rising', 'next_setting', 'next_transit', 'next_antitransit',
'previous_rising', 'previous_setting', 'previous_transit',
'previous_antitransit', operators.

Added support for calendar conversions (and the Calendar operator type) with
the following operators: 'to_hebrew', 'to_hebrew_name', 'to_julian_date',
'to_islamic', 'to_islamic_name', 'to_ordinal_date', 'to_persian',
'to_persian_name', 'to_bahai', 'to_bahai_name'.

Added the 'ordinal_name' operator.

Added the 'from_hebrew', 'from_islamic', 'from_julian', 'from_bahai',
'from_persian' operators.

Added the 'decagonal_triangular', 'decagonal_centered_square',
'decagonal_pentagonal', 'decagonal_hexagonal', 'decagonal_heptagonal',
'decagonal_octagonal', 'decagonal_nonagonal' operators.

Added the 'distance' operator and changed geocoding lookup to use Nominatim
instead of Google, because the Google lookup (provided by ephem) suddenly
stopped working.

Added the 'cone_volume', 'cone_area', 'torus_volume' and 'torus_area',
'tetrahedron_area', 'tetrahedron_volume', 'octahedron_area',
'octahedron_volume', 'dodecahedron_area', 'dodecahedron_volume',
'icosahedron_area', 'icosahedron_volume', 'prism_area', 'prism_volume',
'antiprism_area', 'antiprism_volume' operators.

Added the 'planck_constant' and 'reduced_planck_constant' operators... finally.

Added support for expressions that are generators instead of lists.  This
allows for lazy evaluation of large lists and avoids creating them entirely in
memory unnecessarily.

The following command:

    rpn -t 1 10000 2 range2 2 10000 2 range2 union

now runs about 60 times faster.

Added the 'centered_tetrahedral', 'centered_octahedral',
'centered_dodecahedral', and 'centered_icosahedral' operators.

Added the 'stern', 'calkin_wilf', and 'generalized_pentagonal' operators.

Added the 'nth_mersenne', 'mass_equivalence', and 'energy_equivalence'
operators.

Added support for automatically caching the results of any function, so
expensive calculations can be persisted for future reuse.

Filled in a bunch of help text.  There's still a long way to go, but I'm making
progress.

Added a number of unit tests and argument validation for most of the operators.

Implemented lots of unit tests.

...and the usual bug fixes.

Please note that through the alpha and beta releases I neglected to make
release notes, so there are a ton of new features not mentioned here.
    ''',
    'release_notes' :
    '''
For notes about earlier versions, use 'help old_release_notes'.

7.2.1

Unit conversion is now a lot smarter because the automatically-generated area
and volume units are generated more intelligently.  This means expressions
using the "square" and "cubic" units will convert automatically and you won't
end up with something like "foot^2/square_mile".

...and yes, a few bug fixes.

7.2.0

Added 'random_element' operator.

The gmpy2 digits( ) function is a much faster way to convert numbers to bases
2 through 62.

Added support for using yafu for factoring.

Added 'aliquot_limit' operator.

Added support for user configuration:  'set_config', 'get_config',
'delete_config' and 'dump_config'.

Added the 'mothers_day', 'fathers_day' and 'advent' operators.

Added the 'molar_gas_constant', 'aliquot_limit' and 'distance' operators
(the old 'distance' operator is now called 'geo_distance').

Added unit tests for converting units, and made a few fixes accordingly.

Verbose mode for factoring gets turned on with -D.

Oops, there were two operators named 'distance'.  'distance' now refers to the
physics operator and the geography operator is now named 'geo_distance'.

The 'acceleration' operator has been implemented.

The derived Planck units are now calculated, instead of hard-coded.

Block Hole operators:  'black_hole_entropy', 'black_hole_lifetime',
'black_hole_luminosity', 'black_hole_mass', 'black_hole_radius' (was
'schwarzchild_radius'), 'black_hole_surface_area',
'black_hole_surface_gravity', 'black_hole_temperature'

...and the usual bug fixes.

7.1.0

Added 'discriminant', 'is_strong_pseudoprime' and 'compare_lists' operators.

Fixed a few mistakes in the help examples.

The unit tests no longer use cached values for functions (but it still uses
the cache for functions that access the Internet:  the OEIS functions and the
location functions).

Added 'describe', 'is_smith_number', 'is_base_k_smith_number',
'is_order_k_smith_number' operators.

Replaced the -R option with 'get_base_k_digits'.   It should have been an
operator all along.

The rpnChilada wheel works on Linux now.
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
''' + makeCommandExample( '2 3 +', indent=4 ) + '''
''' + makeCommandExample( '12 9 -', indent=4 ) + '''
''' + makeCommandExample( '23 47 *', indent=4 ) + '''
''' + makeCommandExample( '10 7 /', indent=4 ) + '''
Basic trigonometry usage:

    Sine of 60 degrees:
''' + makeCommandExample( '60 degrees sin', indent=8 ) + '''
    Tangent of 45 degrees ('deg' is an alias for 'degrees'):
''' + makeCommandExample( '45 deg tan', indent=8 ) + '''
    Convert 2 pi radians to degrees:
''' + makeCommandExample( '2 pi * radians degrees convert', indent=8 ) + '''
    What angle has a slope of 2?
''' + makeCommandExample( '2 atan', indent=8 ) + '''
    Let's do that again and convert the answer to degrees:
''' + makeCommandExample( '2 atan radians degrees convert', indent=8 ) + '''
    Note:  'rad' is not an alias for 'radians' since it is a unit of radiation
           exposure.

Convert an IP address to a 32-bit value and back:
    We'll use '-x' to convert the result to hexadecimal:
''' + makeCommandExample( '-x [ 192 168 0 1 ] 256 base', indent=8 ) + '''
    We can convert it back by using base 256:
''' + makeCommandExample( '0xc0a80001 256 get_base_k_digits', indent=8 ) + '''
Construct the square root of two from a continued fraction:

    First, here's the square root of two to 20 places:
''' + makeCommandExample( '-a20 2 sqrt', indent=8 ) + '''
    Now let's make a continued fraction from that, calculated to 20 terms.
''' + makeCommandExample( '2 sqrt 20 make_cf', indent=8 ) + '''
    Here's the nearest fractional approximation of the square root of two,
    taken to 20 terms:
''' + makeCommandExample( '2 sqrt 20 frac', indent=8 ) + '''
    And we can calculate the square root of two from the continued fraction.

    In reality, the continued fraction representation of the square root of
    two is infinite, so this is only an approximation, based on the first 30
    terms of the continued fraction:
''' + makeCommandExample( '-a20 [ 1 2 30 dup ] cf', indent=8 ) + '''
Calculations with lists:
    List of primes in the first 50 fibonacci numbers:
''' + makeCommandExample( '1 50 range fib lambda x is_prime filter', indent=8 ) + '''
    List the indices of the primes in the first 50 fibonacci numbers:
''' + makeCommandExample( '3 50 range fib factor lambda x count for_each_list 1 - zeroes 3 +', indent=8 ) + '''
    This calculation works by listing the indices of fibonacci numbers with a
    single factor.  We are skipping fib( 1 ) and fib( 2 ) because they have a
    single factor (of 1), but of course, aren't prime.  Of course, we could
    just use 'is_prime' again, but I wanted to show solving the problem another
    way.

    Which of the first thousand pentagonal numbers are also triangular:
''' + makeCommandExample( '1000 pent nth_triangular', indent=8 ) + '''
    So the thousandth pentagonal number is a little bigger than the 1731st
    triangular number.  That tells us how many triangular numbers to look at.
''' + makeCommandExample( '1 1000 range pent 1 1731 range tri intersection', indent=8 ) + '''
    So, 1, 210, and 40755 are triangular and pentagonal.

    Which triangular numbers are those?
''' + makeCommandExample( '1 1000 range pent 1 1731 range tri intersection tri?', indent=8 ) + '''
    The first, 20th, and 285th.

    Which pentagonal numbers are those?
''' + makeCommandExample( '1 1000 range pent 1 1731 range tri intersection pent?', indent=8 ) + '''
    The first, 12th, and 165th pentagonal numbers are also triangular.

    Calculate the first 10 Fibonacci numbers without using the 'fib' operator:
''' + makeCommandExample( '[ 1 1 ] [ 0 1 ] 15 linear_recurrence', indent=8 ) + '''

    What percentage of numbers have a factor less than or equal to 5?
''' + makeCommandExample( '1 1 5 nth_prime lambda 1 x prime 1/x - nprod - 100 *', indent=8 ) + '''
    What percentage of numbers have a factor less than 100?
''' + makeCommandExample( '1 1 100 nth_prime lambda 1 x prime 1/x - nprod - 100 *', indent=8 ) + '''
    What percentage of numbers have a factor less than 100?
''' + makeCommandExample( '1 1 100 nth_prime lambda 1 x prime 1/x - nprod - 100 *', indent=8 ) + '''
    What percentage of numbers have a factor less than 1000?
''' + makeCommandExample( '1 1 1000 nth_prime lambda 1 x prime 1/x - nprod - 100 *', indent=8 ) + '''

Calculations with absolute time:
    operators:
''' + makeCommandExample( 'now', indent=8 ) + '''
''' + makeCommandExample( 'today', indent=8 ) + '''
    ISO-8601 format ("YYYY-MM-DD[T| ][HH:mm:SS]", no timezones):
''' + makeCommandExample( '2014-09-02T13:36:28', indent=8 ) + '''
''' + makeCommandExample( '"2014-09-02 13:36:28"', indent=8 ) + '''
''' + makeCommandExample( '2014-09-02', indent=8 ) + '''
    'make_datetime' operator:
''' + makeCommandExample( '[ 2014 ] make_datetime', indent=8 ) + '''
''' + makeCommandExample( '[ 2014 9 ] make_datetime', indent=8 ) + '''
''' + makeCommandExample( '[ 2014 9 2 ] make_datetime', indent=8 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 ] make_datetime', indent=8 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 ] make_datetime', indent=8 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 28 ] make_datetime', indent=8 ) + '''
    How many days old am I?
''' + makeCommandExample( 'today 1965-03-31 -', indent=8 ) + '''
    When will I be 20,000 days old?
''' + makeCommandExample( '1965-03-31 20000 days +', indent=8 ) + '''
    What day of the week was I born on?
''' + makeCommandExample( '1965-03-31 weekday', indent=8 ) + '''
    What is today (when the help file was generated)?
''' + makeCommandExample( 'today', indent=8 ) + '''
    How many days until Christmas?
''' + makeCommandExample( 'today get_year christmas today -', indent=8 ) + '''
    How many days older am I than my first child?
''' + makeCommandExample( '1994-03-06 1965-03-31 -', indent=8 ) + '''
    What date is 4 weeks from now?
''' + makeCommandExample( 'today 4 weeks +', indent=8 ) + '''
    What date is 4 months from now?
''' + makeCommandExample( 'today 4 months +', indent=8 ) + '''
    On September 1, 2014, what would have 6 months from 2 days ago?
''' + makeCommandExample( '2014-09-01 2 days - 6 months +', indent=8 ) + '''
    There is no February 30, so we use the real last day of the month.  Months
    are handled differently from the other time units with respect to time math
    because they can differ in length.

    However, the month as an absolute unit of time is simply equated to 30
    days:
''' + makeCommandExample( 'month days convert', indent=8 ) + '''
Unit conversions:
    Unit conversions should be very intuitive.
''' + makeCommandExample( '10 miles km convert', indent=8 ) + '''
''' + makeCommandExample( '2 gallons cups convert', indent=8 ) + '''
''' + makeCommandExample( '153 pounds stone convert', indent=8 ) + '''
    rpn supports compound units:
''' + makeCommandExample( '65 miles hour / meters second / convert', indent=8 ) + '''
''' + makeCommandExample( '65 miles hour / furlongs fortnight / convert', indent=8 ) + '''
    rpn has unit definitions, as well as physical constants defined:
''' + makeCommandExample( 'gee', indent=8 ) + '''
''' + makeCommandExample( 'gee 10 seconds *', indent=8 ) + '''
''' + makeCommandExample( 'gee 10 seconds * ft s / convert', indent=8 ) + '''
    So a falling object will be travelling at 321.7 ft/sec after 10 seconds.

    Here's a little more advanced version of the problem.  Let's say we have
    launched a rocket that is accelerated at 5 Gs for 5 minutes.  How long
    would it take for it to reach Jupiter?
''' + makeCommandExample( 'jupiter now distance_from_earth 5 gee 5 minutes * / dhms', indent=8 ) + '''

    Now, let's compare the density of Sagittarius A, the black hole at the
    center of the Milky Way, to the density of gold...
''' + makeCommandExample( '4.3 million solar_mass 4.3 million solar_mass black_hole_radius sphere_volume / Gold element_density /', indent=8 ) + '''

Advanced examples:

Calculation (or approximation) of various mathematical constants:

    Polya Random Walk Constant
''' + makeCommandExample( '-p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 / gamma 7 24 / gamma 11 24 / gamma ] prod 1/x * -', indent=8, slow=True ) + '''
    Schwartzchild Constant (Conic Constant)
''' + makeCommandExample( '0 inf lambda 2 x ** x ! / nsum', indent=8 ) + '''
''' + makeCommandExample( 'e 2 **', indent=8 ) + '''
    Somos\' Quadratic Recurrence Constant
''' + makeCommandExample( '-a20 1 inf lambda x 1 2 x ** / power nprod', indent=8 ) + '''
    Prevost Constant
''' + makeCommandExample( '-a20 1 inf lambda x fib 1/x nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 prevost_constant', indent=8 ) + '''
    Euler's number
''' + makeCommandExample( '-a20 0 inf lambda x ! 1/x nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e', indent=8 ) + '''
    Gelfond Constant
''' + makeCommandExample( '-a20 0 inf lambda pi x power x ! / nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e pi power', indent=8 ) + '''
    Bloch-Landau Constant
''' + makeCommandExample( '-a20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /', indent=8 ) + '''
    Hausdorff Dimension
''' + makeCommandExample( '-a20 0 inf lambda 2 x 2 * 1 + power x 2 * 1 + * 1/x nsum 0 inf lambda 3 x 2 * 1 + power x 2 * 1 + * 1/x nsum /', indent=8 ) + '''
''' + makeCommandExample( '-a20 3 log 2 log /', indent=8 ) + '''
    Beta( 3 )
''' + makeCommandExample( '-a20 0 inf lambda x 2 * 1 + 3 power 1/x -1 x ** * nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 pi 3 power 32 /', indent=8 ) + '''
    Lemniscate Constant
''' + makeCommandExample( '-a20 4 2 pi / sqrt * 0.25 ! sqr *', indent=8 ) + '''
    sqrt( e )
''' + makeCommandExample( '-a20 0 inf lambda 2 x power x ! * 1/x nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 0 inf lambda x 2 * !! 1/x nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e sqrt', indent=8 ) + '''
    1/e
''' + makeCommandExample( '-a20 0 inf lambda x ! 1/x -1 x ** * nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e 1/x', indent=8 ) + '''
    An approximation of Zeta( 6 )
''' + makeCommandExample( '-a20 -p30 1 1 1000 primes -6 power - 1/x prod', indent=8 ) + '''
''' + makeCommandExample( '-a20 pi 6 power 945 /', indent=8 ) + '''
''' + makeCommandExample( '-a20 6 zeta', indent=8 ) + '''
    Ramanujan-Forsythe Constant
''' + makeCommandExample( '0 inf lambda x 2 * 3 - !! x 2 * !! / sqr nsum', indent=8 ) + '''
    Apery's Constant
''' + makeCommandExample( '-a20 1 inf lambda x 3 power 1/x nsum', indent=8 ) + '''
''' + makeCommandExample( '-a20 3 zeta', indent=8 ) + '''
''' + makeCommandExample( '-a20 apery', indent=8 ) + '''
    An approximation of the Omega Constant
''' + makeCommandExample( '-a20 [ e 1/x 100 dup ] power_tower2', indent=8 ) + '''
''' + makeCommandExample( '-a20 omega', indent=8 ) + '''
    Liouville Number
''' + makeCommandExample( '-a120 1 inf lambda 10 x ! power 1/x nsum', indent=8 ) + '''
    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                0 100000 range 3 * 2 + sqr 1/x sum -
                1 100000 range 3 * 1 + sqr 1/x sum + *

    An approximation of the Hafner-Sarnak-McCurley Constant (2)
''' + makeCommandExample( '-a7 1 1 100000 primes sqr 1/x - prod', indent=8, slow=True ) + '''
''' + makeCommandExample( '2 zeta 1/x', indent=8 ) + '''
    An approximation of the infinite tetration of i
''' + makeCommandExample( '-a20 [ 1 i 1000 dup ] power_tower2', indent=8 ) + '''
    Cahen's Constant
''' + makeCommandExample( '1 inf lambda x nth_sylvester 1 - 1/x -1 x 1 + ** * nsum', indent=8 ) + '''
    Erdos-Borwein Constant
''' + makeCommandExample( '1 inf lambda 2 x ** 1 - 1/x nsum', indent=8 ) + '''
    An approximation of the Heath-Brown-Moroz constant
''' + makeCommandExample( '-a6 1 60000 primes lambda 1 x 1/x - 7 ** 1 7 x * 1 + x sqr / + * eval prod', indent=8, slow=True ) + '''
    Kepler-Bouwkamp constant
''' + makeCommandExample( '3 inf lambda pi x / cos nprod', indent=8 ) + '''
    Ramanujan-Forsyth series
''' + makeCommandExample( '0 inf lambda x 2 * 3 - !! x 2 * !! / sqr nsum', indent=8 ) + '''
    Machin-Gregory series
''' + makeCommandExample( '0 inf lambda -1 x ** 1 2 / 2 x * 1 + ** * 2 x * 1 + / nsum', indent=8 ) + '''
''' + makeCommandExample( '1 2 / arctan', indent=8 ) + '''
    Somos quadratic recurrence constant
''' + makeCommandExample( '1 inf lambda x 1 + x / 2 x ** root nprod', indent=8 ) + '''
    Niven's constant
''' + makeCommandExample( '1 2 inf lambda 1 x zeta 1/x - nsum +', indent=8 ) + '''
    Kepler-Bouwkamp constant
''' + makeCommandExample( '3 inf lambda pi x / cos nprod', indent=8 ) + '''
    Exponential Factorial Constant
''' + makeCommandExample( '-a80 1 inf lambda 1 x 1 range power_tower / nsum', indent=8 ) + '''
    Conway's Constant
''' + makeCommandExample( '-a80 [ 1, 0, -1, -2, -1, 2, 2, 1, -1, -1, -1, -1, -1, 2, 5, 3, -2, -10, -3, -2, 6, 6, 1, 9, -3, -7, -8, -8, 10, 6, 8, -5, -12, 7, -7, 7, 1, -3, 10, 1, -6, -2, -10, -3, 2, 9, -3, 14, -8, 0, -7, 9, 3, -4, -10, -7, 12, 7, 2, -12, -4, -2, 5, 0, 1, -7, 7, -4, 12, -6, 3, -6 ] solve real max', indent=8, slow=True ) + '''
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

# //******************************************************************************
# //
# //  algebra operators
# //
# //******************************************************************************

    'add_polynomials' : [
'algebra', 'interprets two lists as polynomials and adds them',
'''
For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).

For 'add_polynomials', the result is simply the sum of each respective
coefficient.
''',
'''
''' + makeCommandExample( '[ 1 3 5 ] [ 2 4 6 ] add_polynomials' ) + '''
''' + makeCommandExample( '[ 1 1 ] [ 2 2 2 ] add_polynomials' ) + '''
''' + makeCommandExample( '[ 1 ] [ 4 5 dup ] add_polynomials' ),
[ 'multiply_polynomials', 'polynomial_power', 'polynomial_sum' ] ],

    'discriminant' : [
'algebra', 'calculates the discriminant of polynomial n',
'''
from https://en.wikipedia.org/wiki/Discriminant:

In algebra, the discriminant of a polynomial is a polynomial function of its
coefficients, which allows deducing some properties of the roots without
computing them. For example, the discriminant of the quadratic polynomial is
zero if and only if the polynomial has a double root, and (in the case of
real coefficients) is positive if and only if the polynomial has two real
roots.

More generally, for a polynomial of an arbitrary degree, the discriminant is
zero if and only if it has a multiple root, and, in the case of real
coefficients, it is positive if and only if the number of non-real roots is a
multiple of 4 when the degree is 4 or higher.

The discriminant is widely used in number theory, either directly or through
its generalization as the discriminant of a number field. For factoring a
polynomial with integer coefficients, the standard method consists in
factoring first its reduction modulo a prime number not dividing the
discriminant (and not dividing the leading coefficient).
''',
'''
''' + makeCommandExample( '[ 5 4 3 2 1 ] discriminant' ) + '''
''' + makeCommandExample( '[ 4 -20 25 ] discriminant' ),
[ 'add_polynomials', 'eval_polynomial', 'multiply_polynomials', 'polynomial_power' ] ],

    'eval_polynomial' : [
'algebra', 'interprets the list as a polynomial and evaluates it for value k',
'''
This operator interprets n as a polynomial and evaluates it for value k.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 1 2 ] 3 eval_polynomial' ) + '''
''' + makeCommandExample( '[ 10 -20 30 -40 50 -60 ] 154 eval_polynomial' ) + '''
''' + makeCommandExample( '[ 8 5 3 -4 ] 1 10 range eval_polynomial' ),
[ 'add_polynomials', 'find_polynomials', 'multiply_polynomials', 'polynomial_power' ] ],

    'find_polynomial' : [
'algebra', 'finds a polynomial, of order less than or equal to k, for which n is a zero',
'''
This operator uses mpmath's algebraic identification functionality to attempt
to find a polynomial for which n is a zero.  The matching polynomial, if found,
will be limited to an order of no higher than k.
''',
'''
''' + makeCommandExample( '2 sqrt 10 find_polynomial' ) + '''
''' + makeCommandExample( 'phi 3 ** 10 find_polynomial' ) + '''
''' + makeCommandExample( 'silver 10 find_polynomial' ) + '''
''' + makeCommandExample( 'plastic 10 find_polynomial' ) + '''
''' + makeCommandExample( 'mertens_constant 100 find_polynomial' ),
[ 'eval_polynomial', 'solve' ] ],

    'multiply_polynomials' : [
'algebra', 'interprets two lists as polynomials and multiplies them',
'''
This operator multiplies two polynomials.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 1 0 ] [ 1 0 ] multiply_polynomials' ) + '''
''' + makeCommandExample( '[ 1 1 ] [ 1 1 1 ] multiply_polynomials' ) + '''
''' + makeCommandExample( '[ 6 6 8 8 ] [ 10 12 24 36 ] multiply_polynomials' ),
[ 'add_polynomials', 'eval_polynomial', 'polynomial_power', 'polynomial_product' ] ],

    'polynomial_power' : [
'algebra', 'exponentiates polynomial n by the integer power k',
'''
This operator raises a polynomial to an integral power.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 1 1 ] 2 polynomial_power' ) + '''
''' + makeCommandExample( '[ 1 2 1 ] 4 polynomial_power' ) + '''
''' + makeCommandExample( '[ 1 1 ] 8 polynomial_power' ),
[ 'add_polynomials', 'eval_polynomial', 'multiply_polynomial', 'polynomial_product' ] ],

    'polynomial_product' : [
'algebra', 'interprets elements of list n as polynomials and calculates their product',
'''
This operator calculates the product of a list of polynomials.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 3 4 ] [ 2 3 ] multiply_polynomials' ) + '''
''' + makeCommandExample( '[ [ 3 4 ] [ 2 3 ] ] polynomial_product' ) + '''
''' + makeCommandExample( '[ [ 1 2 3 ] [ 4 5 6 ] [ 7 8 9 10 ] ] polynomial_product' ),
[ 'add_polynomials', 'eval_polynomial', 'multiply_polynomial', 'polynomial_power' ] ],

    'polynomial_sum' : [
'algebra', 'interprets elements of list n as polynomials and calculates their sum',
'''
This operator calculates the sum of a list of polynomials.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 3 4 ] [ 2 3 ] add_polynomials' ) + '''
''' + makeCommandExample( '[ [ 3 4 ] [ 2 3 ] ] polynomial_sum' ) + '''
''' + makeCommandExample( '[ [ 1 2 3 ] [ 4 5 6 ] [ 7 8 9 10 ] ] polynomial_sum' ),
[ 'add_polynomials', 'multiply_polynomial', 'polynomial_power' ] ],

    'solve' : [
'algebra', 'interprets list n as a polynomial and solves for its roots',
'''
This function solves for the roots of a polynomial, using mpmath's numerical
solver.

For functions that take polynomial arguments, rpn interprets the list as
coefficients of powers of x in decreasing order with the rightmost element
representing the coefficient of x^0 (i.e., the constant).
''',
'''
''' + makeCommandExample( '[ 1 3 -28 ] solve' ) + '''
''' + makeCommandExample( '[ 1 4 -20 -48 ] solve' ) + '''
''' + makeCommandExample( '[ 1 2 -107 -648 -1008 ] solve' ),
[ 'find_polynomial', 'solve_quartic', 'solve_quadratic', 'solve_cubic' ] ],

    'solve_cubic' : [
'algebra', 'solves a cubic equation',
'''
a is the cubic coefficient (x^3), b is the quadratic coefficient (x^2), c is
the linear coefficient (x), and d is the constant coefficient.

This operator uses the cubic formula to solve cubic equations.  The 'solve'
operator uses mpmath's numerical solver to do the same thing.
''',
'''
''' + makeCommandExample( '1 4 -20 -48 solve_cubic' ),
[ 'solve_quartic', 'solve_quadratic', 'solve' ] ],

    'solve_quadratic' : [
'algebra', 'solves a quadratic equation',
'''
a is the quadratic coefficient (x^2), b is the linear coefficient (x), and c
is the constant coefficient.

This operator uses the quadratic formula to solve quadratic equations.  The
'solve' operator uses mpmath's numerical solver to do the same thing.
''',
'''
''' + makeCommandExample( '1 3 -28 solve_quadratic' ),
[ 'solve_quartic', 'solve_cubic', 'solve' ] ],

    'solve_quartic' : [
'algebra', 'solves a quartic equation',
'''
a is the quartic coefficient (x^4), b is the cubic coefficient (x^3), c is the
quadratic coefficient (x^2), d is the linear coefficient (x), and e is the
constant coefficient.

This operator uses the cubic formula to solve cubic equations.  The 'solve'
operator uses mpmath's numerical solver to do the same thing.
''',
'''
''' + makeCommandExample( '1 2 -107 -648 -1008 solve_quartic' ),
[ 'solve_quadratic', 'solve_cubic', 'solve' ] ],


# //******************************************************************************
# //
# //  arithmetic operators
# //
# //******************************************************************************

    'abs' : [
'arithmetic', 'calculates the absolute value of n',
'''
The absolute value of a number represents its magnitude, regardless of sign.

The absolute value of 0 or a postive number is the number itself.  The
absolute value of a negative number is the number without the negative sign.

The absolute value of a complex number is the modulus of that number, i.e.,
it's distance from the origin of the complex plane, which is calculated by
finding the length of the hypotenuse of right triangle formed by the X-axis,
the Y-axis and the line segment betweent the origin and the complex number
itself.
''',
'''
''' + makeCommandExample( '1 abs' ) + '''
''' + makeCommandExample( '-1 abs' ) + '''
''' + makeCommandExample( '[ -10 20 -30 40 -50 ] abs' ),
[ 'negative', 'sign' ] ],

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

Addition is supported for measurements.
''',
'''
''' + makeCommandExample( '2 2 +' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 5 6 ] 5 add' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 5 6 ] [ 10 10 10 10 10 10 ] +' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 5 6 ] [ 10 10 10 ] add' ) + '''
''' + makeCommandExample( '1 mile 1 km +' ),
[ 'subtract', 'sum', 'multiply', 'divide' ] ],

    'ceiling' : [
'arithmetic', 'returns the next higher integer for n',
'''
This operator returns the next higher integer for n.

n can be any real number.  If n is complex, the imaginary component is also
increased to the next integral multiple of i.
''',
'''
''' + makeCommandExample( '3.4 ceil' ) + '''
''' + makeCommandExample( '-5.8 ceil' ) + '''
''' + makeCommandExample( '5.1 3.4 i +' ),
[ 'floor', 'nint', 'mantissa', 'round' ] ],

    'decrement' : [
'arithmetic', 'returns n - 1',
'''
This operator is the equivalent of 'n 1 subtract'.
''',
'''
''' + makeCommandExample( '1 decrement', indent=4 ) + '''
''' + makeCommandExample( '1 10 range decrement', indent=4 ) + '''
List the first 10 pronic numbers:
''' + makeCommandExample( '1 10 range lambda x x decrement * eval', indent=4 ),
[ 'increment', 'subtract' ] ],

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
''' + makeCommandExample( '1440 24 /' ) + '''
''' + makeCommandExample( '2520 1 10 range /' ) + '''
''' + makeCommandExample( 'miles hour / furlongs fortnight / convert' ),
[ 'multiply', 'add', 'subtract', 'reciprocal' ] ],

    'equals_one_of' : [
'arithmetic', 'returns 1 if n equals any value in the list k, otherwise returns 0',
'''
''',
'''
''' + makeCommandExample( '0 [ 0 1 2 ] equals_one_of' ) + '''
''' + makeCommandExample( '49 1 10 range sqr equals_one_of' ),
[ 'is_equal' ] ],

    'floor' : [
'arithmetic', 'calculates the next lower integer for n',
'''
This operator returns the next lower integer for n.

n can be any real number.  If n is complex, the imaginary component is also
decreased to the next lower integral multiple of i.
''',
'''
''' + makeCommandExample( '0.1 floor' ) + '''
''' + makeCommandExample( '-6.9 floor' ) + '''
''' + makeCommandExample( '-2.5 5.7 i + floor' ),
[ 'ceiling', 'round', 'nearest_int', 'mantissa' ] ],

    'gcd' : [
'arithmetic', 'calculates the greatest common denominator of elements in list n',
'''
''',
'''
''' + makeCommandExample( '[ 5 10 20 ] gcd' ) + '''
''' + makeCommandExample( '[ 3150 8820 ] gcd' ),
[ 'reduce', 'lcm', 'gcd2' ] ],

    'gcd2' : [
'arithmetic', 'calculates the greatest common denominator of n and k',
'''
'n k gcd2' is equivalent to '[ n k ] gcd'
''',
'''
''' + makeCommandExample( '5 20 gcd2' ) + '''
''' + makeCommandExample( '3150 8820 gcd2' ),
[ 'reduce', 'lcm', 'gcd' ] ],

    'geometric_mean' : [
'arithmetic', 'calculates the geometric mean of a a list of numbers n',
'''
The geometric mean is calculated by taking the kth root of the product of k
values.
''',
'''
''' + makeCommandExample( '[ 1 2 ] geometric_mean' ) + '''
''' + makeCommandExample( '[ 1 10 range ] geometric_mean' ) + '''
Calculate the geometric mean of the first n numbers from 1 to 5:
''' + makeCommandExample( '[ 1 1 5 range range ] geometric_mean' ),
[ 'mean', 'agm', 'harmonic_mean' ] ],

    'harmonic_mean' : [
'arithmetic', 'calculates the geometric mean of a a list of numbers n',
'''
The harmonic mean is calculated by taking ...
''',
'''
''' + makeCommandExample( '[ 1 2 4 ] harmonic_mean' ) + '''
''' + makeCommandExample( '[ 1 10 range ] harmonic_mean' ) + '''
Calculate the harmonic mean of the first n numbers from 1 to 5:
''' + makeCommandExample( '[ 1 1 5 range range ] harmonic_mean' ),
[ 'mean', 'agm', 'geometric_mean' ] ],

    'increment' : [
'arithmetic', 'returns n + 1',
'''
This operator is the equivalent of 'n 1 add'.
''',
'''
''' + makeCommandExample( '1 increment' ) + '''
''' + makeCommandExample( '1 10 range increment' ) + '''
''' + makeCommandExample( '1 10 range lambda x increment fib x fib / eval' ),
[ 'decrement', 'add' ] ],

    'is_divisible' : [
'arithmetic', 'returns whether n is n divisible by k',
'''
'is_divisible' returns 1 if n is divisible by k, and 0 if not.  This operator
expects real, integral arguments.
''',
'''
''' + makeCommandExample( '6 2 is_divisible' ) + '''
''' + makeCommandExample( '1 10 range 2 is_divisible' ) + '''
''' + makeCommandExample( '12 1 10 range is_divisible' ),
[ ] ],

    'is_equal' : [
'arithmetic', 'returns 1 if n equals k, otherwise returns 0',
'''
This operator returns 1 if the two arguments are equal, otherwise it returns 0.
It is most useful in lambdas.
''',
'''
''' + makeCommandExample( '0 1 is_equal' ) + '''
''' + makeCommandExample( '1 0 is_equal' ) + '''
''' + makeCommandExample( '1 1 is_equal' ) + '''
''' + makeCommandExample( 'pi 2 / 1 asin is_equal' ),
[ 'is_not_equal', 'is_less', 'is_greater', 'equals_one_of' ] ],

    'is_even' : [
'arithmetic', 'returns whether n is an even number',
'''
This operator returns 1 if the argument is an even integer (i.e., an
integer n such that n % 2 == 0), otherwise it returns 0.  It expects a real
argument.
''',
'''
''' + makeCommandExample( '2 is_even' ) + '''
''' + makeCommandExample( '3 is_even' ) + '''
''' + makeCommandExample( '1 100 primes lambda x is_even filter' ),
[ 'is_odd', 'is_zero' ] ],

    'is_greater' : [
'arithmetic', 'returns 1 if n is greater than k, otherwise returns 0',
'''
This operator returns 1 if the second argument is greater than the first,
otherwise it returns 0.  It is most useful in lambdas.
''',
'''
''' + makeCommandExample( '0 1 is_greater' ) + '''
''' + makeCommandExample( '1 0 is_greater' ) + '''
''' + makeCommandExample( '1 1 is_greater' ) + '''
''' + makeCommandExample( '3 5 ** 5 3 ** is_greater' ),
[ 'is_less', 'is_equal' ] ],

    'is_integer' : [
'arithmetic', 'returns 1 if n is an integer, otherwise returns 0',
'''
For complex numbers, is integer considers the real part and the complex part
seperately.  I don't know if that's appropriate, but that's how it works for
now.
''',
'''
''' + makeCommandExample( 'pi is_integer' ) + '''
''' + makeCommandExample( '1 is_integer' ) + '''
''' + makeCommandExample( '3 i 7 + is_integer' ) + '''
''' + makeCommandExample( '3.1 i 4 + is_integer' ),
[ 'is_even', 'is_odd', 'nearest_int' ] ],

    'is_kth_power' : [
'arithmetic', 'returns whether n is a perfect kth power',
'''
''',
'''
''' + makeCommandExample( '16 4 is_kth_power' ) + '''
''' + makeCommandExample( '32 5 is_kth_power' ),
[ 'is_square', 'is_power_of_k' ] ],

    'is_less' : [
'arithmetic', 'returns 1 if n is less than k, otherwise returns 0',
'''
''',
'''
''' + makeCommandExample( '0 1 is_less' ) + '''
''' + makeCommandExample( '1 0 is_less' ) + '''
''' + makeCommandExample( '1 1 is_less' ) + '''
''' + makeCommandExample( '3 5 ** 5 3 ** is_less' ),
[ 'is_greater', 'is_equal' ] ],

    'is_not_equal' : [
'arithmetic', 'returns 1 if n does not equal k, otherwise returns 0',
'''
''',
'''
''' + makeCommandExample( '0 1 is_not_equal' ) + '''
''' + makeCommandExample( '1 0 is_not_equal' ) + '''
''' + makeCommandExample( '1 1 is_not_equal' ),
[ 'is_equal', 'is_less', 'is_greater' ] ],

    'is_not_greater' : [
'arithmetic', 'returns 1 if n is not greater than k, otherwise returns 0',
'''
'is_not_greater' is the equivalent of "less than or equal".
''',
'''
''' + makeCommandExample( '0 1 is_not_greater' ) + '''
''' + makeCommandExample( '1 0 is_not_greater' ) + '''
''' + makeCommandExample( '1 1 is_not_greater' ) + '''
''' + makeCommandExample( '3 5 ** 5 3 ** is_not_greater' ),
[ 'is_greater', 'is_not_less' ] ],

    'is_not_less' : [
'arithmetic', 'returns 1 if n is not less than k, otherwise returns 0',
'''
'is_not_less' is the equivalent of "greater than or equal".
''',
'''
''' + makeCommandExample( '0 1 is_not_less' ) + '''
''' + makeCommandExample( '1 0 is_not_less' ) + '''
''' + makeCommandExample( '1 1 is_not_less' ) + '''
''' + makeCommandExample( '3 5 ** 5 3 ** is_not_less' ),
[ 'is_less', 'is_not_greater' ] ],

    'is_not_zero' : [
'arithmetic', 'returns whether n is not zero',
'''
This is simply a check for a non-zero value.
''',
'''
''' + makeCommandExample( '1 is_not_zero' ) + '''
''' + makeCommandExample( '0 is_not_zero' ),
[ 'is_zero', 'is_odd', 'is_even', 'is_not_equal' ] ],

    'is_odd' : [
'arithmetic', 'returns whether n is an odd number',
'''
This operator returns 1 if the argument is an odd integer (i.e., an
integer n such that n % 2 == 1), otherwise it returns 0.  It expects a real
argument.
n % 2 == 1).
''',
'''
''' + makeCommandExample( '2 is_odd' ) + '''
''' + makeCommandExample( '3 is_odd' ) + '''
''' + makeCommandExample( '1 10 range is_odd' ),
[ 'is_even', 'is_zero' ] ],

    'is_power_of_k' : [
'arithmetic', 'returns whether n is a perfect power of k',
'''
Returns 1 if n is an integral power of k, otherwise it returns 0.  It accepts
complex arguments.
''',
'''
''' + makeCommandExample( '16 4 is_power_of_k' ) + '''
''' + makeCommandExample( '32 2 is_power_of_k' ),
[ 'is_square', 'is_kth_power' ] ],

    'is_square' : [
'arithmetic', 'returns whether n is a perfect square',
'''
This operator is also the equivalent of 'n 2 is_kth_power'.  It accepts complex
arguments.
''',
'''
''' + makeCommandExample( '16 is_square' ) + '''
''' + makeCommandExample( '32 is_square' ) + '''
This works with complex numbers:

''' + makeCommandExample( '2 i 1 + sqr' ) + '''
''' + makeCommandExample( '-3 4 i + is_square' ),
[ 'is_power_of_k', 'is_kth_power' ] ],

    'is_zero' : [
'arithmetic', 'returns whether n is zero',
'''
The operator is primarily useful in lambdas.
''',
'''
''' + makeCommandExample( '0 is_zero' ) + '''
''' + makeCommandExample( '1 is_zero' ) + '''
''' + makeCommandExample( '2 i is_zero' ) + '''
''' + makeCommandExample( '0 i is_zero' ),
[ 'is_not_zero', 'is_odd', 'is_even', 'is_equal' ] ],

    'larger' : [
'arithmetic', 'returns the larger of n and k',
'''
'larger' requires real arguments.
''',
'''
''' + makeCommandExample( '7 8 larger' ) + '''
''' + makeCommandExample( 'pi 3' ) + '''
''' + makeCommandExample( '1 -1 larger' ),
[ 'smaller', 'is_larger' ] ],

    'lcm' : [
'arithmetic', 'calculates the least common multiple of elements in list n',
'''
''',
'''
''' + makeCommandExample( '[ 3 6 12 ] lcm' ) + '''
''' + makeCommandExample( '1 20 range lcm' ) + '''
''' + makeCommandExample( '1 5 primes lcm 5 primorial is_equal' ),
[ 'gcd', 'agm', 'lcm2' ] ],

    'lcm2' : [
'arithmetic', 'calculates the least common multiple of n and k',
'''
'n k lcm2' is equivalent to '[ n k ] lcm'.
''',
'''
''' + makeCommandExample( '3 12 lcm2' ) + '''
''' + makeCommandExample( '24 36 lcm2' ),
[ 'gcd', 'agm', 'lcm' ] ],

    'mantissa' : [
'arithmetic', 'returns the decimal part of n',
'''
''',
'''
''' + makeCommandExample( 'pi mantissa' ) + '''
''' + makeCommandExample( '-p50 652 sqrt pi * exp mantissa' ),
[ 'floor', 'ceiling', 'nint' ] ],

    'max' : [
'arithmetic', 'returns the largest value in list n',
'''
This operator returns the largest value in the input list of values n.

'max' requires a list of real arguments.
''',
'''
''' + makeCommandExample( '[ 5 8 2 23 9 ] max' ) + '''
''' + makeCommandExample( '10 1000 random_integer_ max' ),
[ 'min', 'larger', 'is_greater' ] ],

    'mean' : [
'arithmetic', 'calculates the mean of values in list n',
'''
This is the classic definition of 'mean', often called 'average':  the sum of
all items divided by the number of items.

'mean' requires a list of real arguments.
''',
'''
''' + makeCommandExample( '1 10 range mean' ) + '''
''' + makeCommandExample( '1 1000 range sum_digits mean' ),
[ 'stddev', 'agm', 'geometric_mean', 'harmonic_mean' ] ],

    'min' : [
'arithmetic', 'returns the smallest value in list n',
'''
This operator returns the smallest value in the input list of values n.

'min' requires a list of real arguments.
''',
'''
''' + makeCommandExample( '[ 5 8 2 23 9 ] min' ) + '''
''' + makeCommandExample( '10 1000 random_integer_ min' ),
[ 'max', 'smaller', 'is_less' ] ],

    'modulo' : [
'arithmetic', 'calculates n modulo k',
'''
''',
'''
''' + makeCommandExample( '7 4 modulo' ) + '''
''' + makeCommandExample( '143 12 modulo' ),
[ 'powmod', 'divide' ] ],

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
''' + makeCommandExample( '32 56 *' ) + '''
''' + makeCommandExample( '7 1 10 range *' ) + '''
''' + makeCommandExample( '16800 mA hours * 5 volts * joule convert' ),
[ 'add', 'subtract', 'divide', 'power' ] ],

    'negative' : [
'arithmetic', 'calculates the negative of n',
'''
''',
'''
''' + makeCommandExample( '1 negative' ) + '''
''' + makeCommandExample( '-1 negative' ) + '''
''' + makeCommandExample( '0 negative' ),
[ 'sign', 'abs' ] ],

    'nearest_int' : [
'arithmetic', 'returns the nearest integer to n',
'''
On a tie, 'nearest_int' returns the nearest even number.  This makes it slightly
different than 'round'.
''',
'''
''' + makeCommandExample( '2 sqrt nearest_int' ) + '''
''' + makeCommandExample( '3 sqrt neg nearest_int' ) + '''
''' + makeCommandExample( '0.5 nearest_int' ) + '''
''' + makeCommandExample( '1.5 nearest_int' ),
[ 'round', 'floor', 'ceiling', 'mantissa' ] ],

    'product' : [
'arithmetic', 'calculates the product of values in list n',
'''
''',
'''
''' + makeCommandExample( '[ 2 3 7 12 ] product' ) + '''
''' + makeCommandExample( '1 10 range product' ) + '''
''' + makeCommandExample( '10 !' ) + '''
Calculating the magnetic constant:
''' + makeCommandExample( '[ 4 pi 10 -7 ** joule/ampere^2*meter ] product', indent=4 ),
[ 'multiply', 'sum' ] ],

    'reciprocal' : [
'arithmetic', 'returns the reciprocal of n',
'''
''',
'''
''',
[ 'divide' ] ],

    'round' : [
'arithmetic', 'rounds n to the nearest integer',
'''
'round' requires a real argument.   If the value is exactly halfway between
integers, 'round' will round up to the next highest integer.
''',
'''
''' + makeCommandExample( '1.2 round' ) + '''
''' + makeCommandExample( '-7.8 round' ) + '''
''' + makeCommandExample( '4.5 round' ) + '''
''' + makeCommandExample( '-13.5 round' ),
[ 'round_by_digits', 'round_by_value', 'nearest_int' ] ],

    'round_by_digits' : [
'arithmetic', 'rounds n to the nearest kth power of 10',
'''
Note that 'n round' is the equivalent of 'n 0 round_by_digits'.

'round_by_digits' requires a real argument.  If the value is exactly halfway
between the least significant digit, 'round_by_digits' will round up.
''',
'''
''' + makeCommandExample( '12 1 round_by_digits' ) + '''
''' + makeCommandExample( '12 0 round_by_digits' ) + '''
''' + makeCommandExample( '567 3 round_by_digits' ) + '''
''' + makeCommandExample( 'pi -3 round_by_digits' ) + '''
''' + makeCommandExample( '-a15 -13 pi round_by_digits -d' ),
[ 'round', 'round_by_value', 'nearest_int' ] ],

    'round_by_value' : [
'arithmetic', 'rounds n to the nearest multiple of k',
'''
Note that 'n round' is the equivalent of 'n 1 round_by_value'.  If the value
is exactly halfway between multiples of k, 'round_by_value' will round up.
''',
'''
''' + makeCommandExample( '11 3 round_by_value' ) + '''
''' + makeCommandExample( '23 5 round_by_value' ) + '''
''' + makeCommandExample( 'pi 2 round_by_value' ) + '''
''' + makeCommandExample( 'pi 0.2 round_by_value' ) + '''
''' + makeCommandExample( 'pi 0.03 round_by_value' ) + '''
''' + makeCommandExample( 'pi 0.004 round_by_value' ),
[ 'round_by_digits', 'round', 'nearest_int' ] ],

    'sign' : [
'arithmetic', 'returns the sign of a value',
'''
For real numbers, 'sign' returns 1 for positive, -1 for negative and 0 for
zero.

For complex numbers, it gives the projection of the value n onto the complex
unit circle.
''',
'''
''' + makeCommandExample( '37 sign' ) + '''
''' + makeCommandExample( '-8 sign' ) + '''
''' + makeCommandExample( '0 sign' ) + '''
''' + makeCommandExample( '3 4 i + sign' ),
[ 'negative', 'abs' ] ],

    'smaller' : [
'arithmetic', 'returns the smaller of n and k',
'''
'smaller' requires real arguments.
''',
'''
''' + makeCommandExample( '1 2 smaller' ) + '''
''' + makeCommandExample( '4 3 smaller' ) + '''
''' + makeCommandExample( '8 9 ** 9 8 ** smaller' ),
[ 'larger', 'is_less' ] ],

    'stddev' : [
'arithmetic', 'calculates the standard deviation of values in list n',
'''
''',
'''
''' + makeCommandExample( '10 50 random_integer_ stddev' ) + '''
''' + makeCommandExample( '1 50 range count_div stddev' ),
[ 'mean', 'agm', 'geometric_mean' ] ],

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
''' + makeCommandExample( '17 8 -' ) + '''
''' + makeCommandExample( '10 [ 1 2 3 4 ] -' ) + '''
''' + makeCommandExample( '[ 10 9 8 7 ] [ 6 5 4 3 ] -' ) + '''
''' + makeCommandExample( '1 gallon 4 cups -' ) + '''
''' + makeCommandExample( '1776-06-24 10 days -' ),
[ 'add', 'multiply', 'divide' ] ],

    'sum' : [
'arithmetic', 'calculates the sum of values in list n',
'''
In addition to numbers, 'sum' can also add up a list of measurements.
''',
'''
''' + makeCommandExample( '[ 5 8 3 ] sum' ) + '''
''' + makeCommandExample( '1 100 range sum' ) + '''
''' + makeCommandExample( '[ 3 cups 21 teaspoons 7 tablespoons 1.5 deciliters ] sum' ),
[ 'add', 'prod' ] ],


# //******************************************************************************
# //
# //  astronomical_object operators
# //
# //******************************************************************************

    'jupiter' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'mars' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'mercury' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'moon' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'neptune' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'pluto' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'saturn' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'sun' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'uranus' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],

    'venus' : [
'astronomical_objects', '',
'''
''',
'''
''',
[ ] ],


# //******************************************************************************
# //
# //  astronomy operators
# //
# //******************************************************************************

    'angular_separation' : [
'astronomy', 'returns the angular separation of astronomical objects a and b in radians, at location c, for date-time d',
'''
''',
'''
''' + makeCommandExample( 'sun moon "Kitty Hawk, NC" "2017-08-21 14:50" angular_separation dms' ),
[ 'sky_location' ] ],

    'angular_size' : [
'astronomy', 'returns the angular size of astronomical object a in radians, at location b, for date-time c',
'''
''',
'''
''' + makeCommandExample( 'sun "Paris, France" now angular_size dms' ),
[ 'sky_location' ] ],

    'antitransit_time' : [
'astronomy', 'calculates the duration of time from the next setting until the subseqent rising of a body'
'''
''',
'''
''',
[ 'day_time', 'dawn', 'dusk', 'transit_time', 'night_time' ] ],

    'astronomical_dawn' : [
'astronomy', 'calculates the time of the astronomical dawn for location n and date k',
'''
''',
'''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 astronomical_dawn' ) + '''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 nautical_dawn' ) + '''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 dawn' ),
[ 'astronomical_dusk', 'nautical_dawn', 'dawn', 'dusk' ] ],

    'astronomical_dusk' : [
'astronomy', 'calculates the time of the astronomical dusk for location n and date k',
'''
''',
'''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 nautical_dusk' ) + '''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 dusk' ),
[ 'astronomical_dawn', 'nautical_dusk', 'dawn', 'dusk' ] ],

    'autumnal_equinox' : [
'astronomy', 'calculates the time of the autumnal equinox for year n',
'''
''',
'''
''',
[ 'vernal_equinox', 'summer_solstice', 'winter_solstice' ] ],

    'dawn' : [
'astronomy', 'calculates the next dawn time at location n for date-time k',
'''
The definition of dusk being used the is "civil" definition of dawn, i.e., the
center of the sun is 6 degrees below the horizon.
''',
'''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 nautical_dusk' ) + '''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 dusk' ),
[ 'day_time', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'day_time' : [
'astronomy', 'calculates the duration of the next day (i.e., transit_time for the sun)',
'''
This is also the amount of time between sunrise and sunset.
''',
'''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 day_time' ) + '''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 ( sunset sunrise ) unlist -' ),
[ 'dawn', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'distance_from_earth' : [
'astronomy', 'returns the distance from Earth of astronomical object n for date-time k',
'''
''',
'''
''' + makeCommandExample( '-c mars "2018-07-10 16:00" distance_from_earth miles convert' ) + '''
''' + makeCommandExample( '-c jupiter "2018-07-10 16:00" distance_from_earth miles convert' ),
[ 'sky_location', 'angular_size' ] ],

    'dusk' : [
'astronomy', 'calculates the next dusk time at location n for date-time k',
'''
The definition of dusk being used the is "civil" definition of dusk, i.e., the
center of the sun is 6 degrees below the horizon.
''',
'''
''' + makeCommandExample( '"Napoli, Italy" 2017-05-14 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Napoli, Italy" 2017-05-14 nautical_dusk' ) + '''
''' + makeCommandExample( '"Napoli, Italy" 2017-05-14 dusk' ),
[ 'day_time', 'dawn', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'eclipse_totality' : [
'astronomy', 'returns the percentage of the eclipsed body that is covered by the eclipsing body',
'''
a and b are the two bodies in question (in any order), c is the location and d
is the time.
''',
'''
''',
[ 'sky_location', 'angular_size', 'angular_separation' ] ],

    'moonrise' : [
'astronomy', 'calculates the next moonrise time at location n for date-time k',
'''
''',
'''
''',
[ 'moonset', 'moon_phase' ] ],

    'moonset' : [
'astronomy', 'calculates the nenxt moonset time at location n for date-time k',
'''
''',
'''
''',
[ 'moonrise', 'moon_phase' ] ],

    'moon_antitransit' : [
'astronomy', 'calculates the next moon antitransit time at location n for date-time k',
'''
''',
'''
''',
[ 'moon_transit' ] ],

    'moon_phase' : [
'astronomy', 'determines the phase of the moon as a percentage for date-time n',
'''
The moon phase cycle starts at the new moon and completes with the next new
moon.  Therefore, 0% is the new moon, 25% is the first quarter, 50% is a full
moon, 75% is the last quarter and 100% is the new moon again.
''',
'''
What was the phase of the moon the day I was born:

''' + makeCommandExample( '1965-03-31 moon_phase' ) + '''
... a waning crescent.
''',
[ 'moonrise', 'moonset' ] ],

    'moon_transit' : [
'astronomy', 'calculates the next moon transit time at location n for date k',
'''
''',
'''
''' + makeCommandExample( '"Washington, DC" 2017-03-08 moon_transit' ),
[ 'moon_antitransit', 'moonrise', 'moonset' ] ],

    'nautical_dawn' : [
'astronomy', 'calculates the time of the nautical dawn for location n and date k',
'''
''',
'''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 astronomical_dawn' ) + '''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 nautical_dawn' ) + '''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 dawn' ),
[ 'nautical_dusk', 'dawn', 'astronomical_dawn' ] ],

    'nautical_dusk' : [
'astronomy', 'calculates the time of the nautical dusk for location n and date k',
'''
''',
'''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 nautical_dusk' ) + '''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 dusk' ),
[ 'nautical_dawn', 'dusk', 'astronomical_dusk' ] ],

    'next_antitransit' : [
'astronomy', 'returns the date of the next antitransit of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'previous_antitransit', 'next_transit', 'next_rising', 'next_setting' ] ],

    'next_first_quarter_moon' : [
'astronomy', 'returns the date of the next First Quarter Moon after n',
'''
''',
'''
''' + makeCommandExample( 'today next_first_quarter_moon' ) + '''
''' + makeCommandExample( '2008 easter next_first_quarter_moon' ),
[ 'next_full_moon', 'next_last_quarter_moon', 'next_new_moon', 'previous_first_quarter_moon' ] ],

    'next_full_moon' : [
'astronomy', 'returns the date of the next Full Moon after n',
'''
''',
'''
''' + makeCommandExample( 'today next_full_moon' ) + '''
''' + makeCommandExample( '2011-02-02 next_full_moon' ),
[ 'previous_full_moon', 'next_first_quarter_moon', 'next_last_quarter_moon', 'next_new_moon' ] ],

    'next_last_quarter_moon' : [
'astronomy', 'returns the date of the next Last Quarter Moon after n',
'''
''',
'''
''' + makeCommandExample( 'today next_last_quarter_moon' ) + '''
''' + makeCommandExample( '2050-01-01 next_last_quarter_moon' ),
[ 'previous_last_quarter_moon', 'next_new_moon', 'next_first_quarter_moon', 'next_new_moon' ] ],

    'next_new_moon' : [
'astronomy', 'returns the date of the next New Moon after n',
'''
''',
'''
''' + makeCommandExample( 'today next_new_moon' ) + '''
''' + makeCommandExample( '5776 05 15 from_hebrew next_new_moon to_hebrew_name' ),
[ 'previous_new_moon', 'next_first_quarter_moon', 'next_last_quarter_moon', 'next_full_moon' ] ],

    'next_rising' : [
'astronomy', 'returns the date of the next rising of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'previous_rising', 'next_setting', 'next_transit', 'next_antitransit' ] ],

    'next_setting' : [
'astronomy', 'returns the date of the next setting of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'previous_setting', 'next_rising', 'next_transit', 'next_antitransit' ] ],

    'next_transit' : [
'astronomy', 'returns the date of the next transit of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'previous_transit', 'next_rising', 'next_setting', 'next_antitransit' ] ],

    'night_time' : [
'astronomy', 'calculates the duration of the next night (i.e., antitransit_time for the sun)',
'''
This is also the amount of time between sunset and sunrise.
''',
'''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 night_time' ) + '''
''' + makeCommandExample( '"Washington, DC" 2017-04-09 sunrise "Washington, DC" 2017-04-08 sunset -' ),
[ 'day_time', 'dawn', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'previous_antitransit' : [
'astronomy', 'returns the date of the previous antitransit of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'next_antitransit', 'previous_rising', 'previous_setting', 'previous_transit' ] ],

    'previous_first_quarter_moon' : [
'astronomy', 'returns the date of the previous First Quarter Moon before n',
'''
''',
'''
''' + makeCommandExample( 'today previous_first_quarter_moon' ) + '''
''' + makeCommandExample( '1988-05-03 previous_first_quarter_moon' ),
[ 'next_first_quarter_moon', 'previous_last_quarter_moon', 'previous_full_moon', 'previous_new_moon' ] ],

    'previous_full_moon' : [
'astronomy', 'returns the date of the previous Full Moon before n',
'''
''',
'''
''' + makeCommandExample( 'today previous_full_moon' ) + '''
''' + makeCommandExample( '2016-10-31 previous_full_moon' ) + '''
''' + makeCommandExample( '2005-06-23 previous_full_moon' ),
[ 'next_full_moon', 'previous_last_quarter_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_last_quarter_moon' : [
'astronomy', 'returns the date of the previous Last Quarter Moon before n',
'''
''',
'''
''' + makeCommandExample( 'today previous_last_quarter_moon' ) + '''
''' + makeCommandExample( '1971-01-01 previous_last_quarter_moon' ),
[ 'next_last_quarter_moon', 'previous_full_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_new_moon' : [
'astronomy', 'returns the date of the previous New Moon before n',
'''
''',
'''
''' + makeCommandExample( 'today previous_new_moon' ) + '''
''' + makeCommandExample( '2020-03-19 previous_new_moon' ),
[ 'next_new_moon', 'previous_full_moon', 'previous_first_quarter_moon', 'previous_last_quarter_moon' ] ],

    'previous_rising' : [
'astronomy', 'returns the date of the previous rising of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'next_rising', 'previous_setting', 'previous_transit', 'previous_antitransit' ] ],

    'previous_setting' : [
'astronomy', 'returns the date of the previous setting of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'next_setting', 'previous_rising', 'previous_transit', 'previous_antitransit' ] ],

    'previous_transit' : [
'astronomy', 'returns the date of the previous transit of body a, when viewed from location b, at date c',
'''
''',
'''
''',
[ 'next_transit', 'previous_rising', 'previous_setting', 'previous_antitransit' ] ],

    'sky_location' : [
'astronomy', 'returns the sky location of astronomical object a, at location b, for date-time c',
'''
The location is returned as a list where the elements represent the azimuth and
altitude in degrees.  Azimuth corresponds to compass direction, and altitude ranges
from 0 degrees at the horizon to 90 degrees at zenith and -90 degrees at nadir.
''',
'''
''',
[ 'distance_from_earth', 'angular_size' ] ],

    'solar_noon' : [
'astronomy', 'calculates the next solar noon time at location n for date-time k',
'''
''',
'''
''',
[ 'dawn', 'dusk' ] ],

    'summer_solstice' : [
'astronomy', 'calculates the time of the summer solstice for year n',
'''
''',
'''
''',
[ 'winter_solstice', 'autumnal_equinox', 'vernal_equinox' ] ],

    'sunrise' : [
'astronomy', 'calculates the next sunrise time at location n for date-time k',
'''
''',
'''
''',
[ 'sunset', 'solar_noon' ] ],

    'sunset' : [
'astronomy', 'calculates the next sunset time at location n for date-time k',
'''
''',
'''
''',
[ 'sunrise', 'solar_noon' ] ],

    'sun_antitransit' : [
'astronomy', 'calculates the next sun antitransit time at location n for date-time k',
'''
Think of it sort of like "anti-noon".
''',
'''
''' + makeCommandExample( '"Bridgeford, CT" today sun_antitransit' ),
[ 'sun_transit', 'sunrise', 'sunset' ] ],

    'transit_time' : [
'astronomy', 'calculates the duration of time from the next rising until the subseqent setting of a body'
'''
a is an astronomical object, b is a location and c is a date-time value
''',
'''
''' + makeCommandExample( 'moon "Washington, DC" today transit_time hms' ),
[ 'day_time', 'dawn', 'dusk', 'antitransit_time', 'night_time' ] ],

    'vernal_equinox' : [
'astronomy', 'calculates the time of the vernal equinox for year n',
'''
''',
'''
''',
[ 'summer_solstice', 'autumnal_equinox', 'winter_solstice' ] ],

    'winter_solstice' : [
'astronomy', 'calculates the time of the winter solstice for year n',
'''
''',
'''
''',
[ 'autumnal_equinox', 'summer_solstice', 'vernal_equinox' ] ],


# //******************************************************************************
# //
# //  bitwise operators
# //
# //******************************************************************************

    'bitwise_and' : [
'bitwise', 'calculates the bitwise \'and\' of n and k',
'''
'and' is the logical operation which returns true if and only if the two
operands are true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'and'ed bits.
''',
'''
''' + makeCommandExample( '-x 0xF0F0F0F0 0x12345678 and' ) + '''
''' + makeCommandExample( '[ 0 0 1 1 ] [ 0 1 0 1 ] and' ),
[ 'bitwise_or', 'bitwise_not', 'bitwise_nor', 'bitwise_nand', 'bitwise_xor' ] ],

    'bitwise_nand' : [
'bitwise', 'calculates the bitwise \'nand\' of n and k',
'''
'nand' is the logical operation, 'not and' which returns true if zero or one
of the operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'and'ed bits.
''',
'''
''' + makeCommandExample( '-x 0x01234567 0xffff0000 nand' ) + '''
''' + makeCommandExample( '-x [ 0x0000 0x0000 0xffff 0xffff ] [ 0x0000 0xffff 0x0000 0xffff ] nand' ),
[ 'bitwise_and', 'bitwise_or', 'bitwise_not', 'bitwise_nor', 'bitwise_xor' ] ],

    'bitwise_nor' : [
'bitwise', 'calculates the bitwise \'nor\' of n and k',
'''
'nor' is the logical operation 'not or', which returns true if and only if
neither of the two operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'nor'ed bits.
''',
'''
''' + makeCommandExample( '-x 0x01234567 0x0000ffff nor' ) + '''
''' + makeCommandExample( '-x [ 0x0000 0x0000 0xffff 0xffff ] [ 0x0000 0xffff 0x0000 0xffff ] nor' ),
[ 'bitwise_or', 'bitwise_and', 'bitwise_not', 'bitwise_nand', 'bitwise_xor' ] ],

    'bitwise_not' : [
'bitwise', 'calculates the bitwise negation of n',
'''
'not' is the logical operation, which returns the opposite of the operand.

The operand is converted to a string of bits large enough to represent the
value, rounded up to the next highest multiple of the bitwise group size,
which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each bit in
the binary representation of the operand.  The result is the numerical
representation of the string of 'not'ed bits.
''',
'''
''' + makeCommandExample( '-x 0xF0F0F0F0 not' ) + '''
''' + makeCommandExample( '-x [ 0 1 ] not' ),
[ 'bitwise_and', 'bitwise_or', 'bitwise_nor', 'bitwise_nand', 'bitwise_xor' ] ],

    'bitwise_or' : [
'bitwise', 'calculates the bitwise \'or\' of n and k',
'''
'or' is the logical operation which returns true if at least one of the two
operands is true.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'or'ed bits.
''',
'''
''' + makeCommandExample( '-x 0xf0f0f0f0 0x0f0f0f0f or' ) + '''
''' + makeCommandExample( '[ 0 0 1 1 ] [ 0 1 0 1 ] or' ),
[ 'bitwise_and', 'bitwise_not', 'bitwise_nand', 'bitwise_nor', 'bitwise_xor' ] ],

    'bitwise_xor' : [
'bitwise', 'calculates the bitwise \'xor\' of n and k',
'''
'xor' is the 'exclusive or' logical operation, which returns true if and only
if the two operands are different.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'xor'ed bits.
''',
'''
''' + makeCommandExample( '-x 0xffff0000 0x12345678 xor' ) + '''
''' + makeCommandExample( '[ 0 0 1 1 ] [ 0 1 0 1 ] xor' ),
[ 'bitwise_and', 'bitwise_or', 'bitwise_nand', 'bitwise_nor', 'bitwise_not' ] ],

    'count_bits' : [
'bitwise', 'returns the number of set bits in the value of n',
'''
''',
'''
''',
[ 'parity' ] ],

    'parity' : [
'bitwise', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
''',
'''
''',
[ 'count_bits' ] ],

    'shift_left' : [
'bitwise', 'performs a bitwise left shift of value n by k bits',
'''
''',
'''
''',
[ 'shift_right' ] ],

    'shift_right' : [
'bitwise', 'performs a bitwise right shift of value n by k bits',
'''
''',
'''
''',
[ 'shift_left' ] ],


# //******************************************************************************
# //
# //  calendar operators
# //
# //******************************************************************************

    'advent' : [
'calendars', 'returns the date of the first Sunday of Advent for the year specified',
'''
''',
'''
''' + makeCommandExample( '2018 advent' ),
[ 'thanksgiving', 'easter', 'epiphany', 'christmas' ] ],
    'ascension' : [
'calendars', 'returns the date of Ascension Thursday for the year specified',
'''
Ascension Thursday is the 40th day of the Easter season in the Christian
calendar, which starts with Easter.  It commemorates the day Christ ascended
into Heaven, on the 40th day after His Resurrection, and marks the end of the
Easter season.
''',
'''
''' + makeCommandExample( '2017 ascension' ) + '''
''' + makeCommandExample( '2017 ascension 2017 easter -' ),
[ 'easter', 'christmas' ] ],

    'ash_wednesday' : [
'calendars', 'calculates the date of Ash Wednesday for the year specified',
'''
Ash Wednesday marks the beginning of Lent, the 40-day penitential season
leading up to Easter in the Christian calendar.  Note that the season of Lent
does not technically include Sundays, so the difference between Easter and Ash
Wednesday is actually 46 days.
''',
'''
''' + makeCommandExample( '2017 ash_wednesday' ) + '''
''' + makeCommandExample( '2017 easter 2017 ash_wednesday -' ),
[ 'easter', 'good_friday' ] ],

    'calendar' : [
'calendars', 'prints a month calendar for date-time n',
'''
The 'calendar' operator is special in that what it prints out is a side-effect.
The operator itself doesn't actually do anything.
''',
'''
c:\>rpn 2016-09-01 cal

   September 2016
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30
''',
[ 'year_calendar', 'weekday','weekday_name' ] ],

    'christmas' : [
'calendars', 'returns the date of Christmas for the year specified',
'''
Christmas commemorates the birth of Christ in the Christian calendar, although
it does not reflect the actual birth day of Jesus, which is unrecorded, and
is considered likely to have happened in the springtime, some time between
6 B.C. and 4 A.D.

I originally didn't intend to make this operator, since Christmas is always
on the same date, but one day, I was checking the number of days until
Christmas and used the 'christmas' operator instinctively.
''',
'''
''' + makeCommandExample( '2017 christmas' ),
[ 'thanksgiving', 'easter', 'epiphany', 'advent' ] ],

    'columbus_day' : [
'calendars', 'returns the date of Columbus Day as celebrated in the U.S. for the year specified',
'''
''',
'''
''' + makeCommandExample( '2017 columbus_day' ),
[ 'independence_day', 'veterans_day', 'memorial_day', 'martin_luther_king_day' ] ],

    'dst_end' : [
'calendars', 'calculates the ending date for Daylight Saving Time for the year specified',
'''
''',
'''
''',
[ 'dst_start' ] ],

    'dst_start' : [
'calendars', 'calculates the starting date for Daylight Saving Time for the year specified',
'''
The history of Daylight Saving Time is rather complicated, and this function
attempts to return correct historical values for every year since DST was
adopted in the United States.
''',
'''
''',
[ 'dst_end' ] ],

    'easter' : [
'calendars', 'calculates the date of Easter for the year specified',
'''
In the Christian calendar, Easter commemorates the Resurrection of Christ.
''',
'''
''' + makeCommandExample( '2016 easter' ) + '''
''' + makeCommandExample( '1973 easter' ),
[ 'ash_wednesday', 'good_friday', 'christmas', 'pentecost' ] ],

    'election_day' : [
'calendars', 'calculates the date of Election Day (US) for the year specified',
'''
In the U.S., Election Day is defined to be the first Tuesday after the first
Monday in November.  This definition was established by the U.S. Congress in
1845.
''',
'''
''' + makeCommandExample( '2016 election_day' ) + '''
''' + makeCommandExample( '1964 election_day' ),
[ 'labor_day', 'memorial_day', 'presidents_day' ] ],

    'epiphany' : [
'calendars', 'returns the date of Epiphany for the year specified',
'''
''',
'''
''',
[ 'christmas', 'easter' ] ],

    'fathers_day' : [
'calendars', 'calculates the date of Father\'s Day (US) for the year specified',
'''
In the U.S., and most other countries, Father's Day occurs on the third Sunday
in June.
''',
'''
''' + makeCommandExample( 'today fathers_day' ) + '''
''' + makeCommandExample( '1993 fathers_day' ),
[ 'mothers_day', 'thanksgiving' ] ],

    'from_bahai' : [
'calendars', 'converts a date in the Baha\'i calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'from_hebrew' : [
'calendars', 'converts a date in the Hebrew calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'from_indian_civil' : [
'calendars', 'converts a date in the Indian civil calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'from_islamic' : [
'calendars', 'converts a date in the Islamic calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'from_julian' : [
'calendars', 'converts a date to the equivalent date in the Julian calendar',
'''
''',
'''
''',
[ ] ],

    'from_mayan' : [
'calendars', 'converts a date in the Mayan long count calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'from_persian' : [
'calendars', 'converts a date in the Persian calendar to the equivalent Gregorian date',
'''
''',
'''
''',
[ ] ],

    'good_friday' : [
'calendars', 'calculates the date of Good Friday for the year specified',
'''
Good Friday is celebrated by Christians as the day which Jesus was crucified
and died.  This day is two days before the celebration of Jesus' Resurrection
on Easter Sunday.
''',
'''
''' + makeCommandExample( '2017 good_friday' ) + '''
''' + makeCommandExample( '2017 easter 2017 good_friday -' ),
[ 'easter', 'ash_wednesday' ] ],

    'independence_day' : [
'calendars', 'returns the date of Independence Day as celebrated in the U.S. for the year specified',
'''
''',
'''
''' + makeCommandExample( '2017 independence_day' ),
[ 'veterans_day', 'memorial_day', 'columbus_day' ] ],

    'iso_date' : [
'calendars', 'returns the date in the ISO format',
'''
''',
'''
''',
[ ] ],

    'labor_day' : [
'calendars', 'calculates the date of Labor Day (US) for the year specified',
'''
In the U.S., Labor Day falls on the first Monday of September.
''',
'''
''' + makeCommandExample( '2016 labor_day' ) + '''
''' + makeCommandExample( '2016 labor_day 2015 memorial_day -' ),
[ 'memorial_day', 'election_day', 'presidents_day' ] ],

    'martin_luther_king_day' : [
'calendars', 'returns the date of Martin Luther King Day as celebrated in the U.S. for the year specified',
'''
''',
'''
''' + makeCommandExample( '2017 martin_luther_king_day' ),
[ 'independence_day', 'veterans_day', 'memorial_day', 'columbus_day' ] ],

    'memorial_day' : [
'calendars', 'calculates the date of Memorial Day (US) for the year specified',
'''
In the U.S., Memorial Day occurs on the last Monday in May.  This holiday
is dedicated to the memorial of the men and women who gave their lives in the
armed services.
''',
'''
''' + makeCommandExample( '2016 memorial_day' ) + '''
''' + makeCommandExample( '2020 2025 memorial_day -s1' ),
[ 'labor_day', 'election_day', 'presidents_day' ] ],

    'mothers_day' : [
'calendars', 'calculates the date of Mother\'s Day (US) for the year specified',
'''
In the U.S., and most other countries, Mother's Day occurs on the second Sunday
in May.
''',
'''
''' + makeCommandExample( 'today mothers_day' ) + '''
''' + makeCommandExample( '1993 mothers_day' ),
[ 'fathers_day', 'thanksgiving' ] ],

    'new_years_day' : [
'calendars', 'returns the date of New Year\'s Day (US) for the year specified',
'''
''',
'''
''' + makeCommandExample( '2020 new_years_day' ),
[ 'labor_day', 'election_day', 'presidents_day' ] ],

    'nth_weekday' : [
'calendars', 'finds the nth day (1 = Monday, etc.) of the month',
'''
a = four-digit year, b = month (1-12), c = week (1-5 for first through 5th),
d = day (1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''',
[ ] ],

    'nth_weekday_of_year' : [
'calendars', 'finds the nth day (1 = Monday) of the year',
'''
a = four-digit year, b = week (negative values count from the end), c = day
(1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''',
[ ] ],

    'pentecost' : [
'calendars', 'returns the date of Pentecost Sunday for the year specified',
'''
''',
'''
''',
[ 'easter' ] ],

    'presidents_day' : [
'calendars', 'calculates the date of Presidents Day (US) for the year specified',
'''
''',
'''
''',
[ 'labor_day', 'memorial_day', 'election_day' ] ],

    'thanksgiving' : [
'calendars', 'calculates the date of Thanksgiving (US) for the year specified',
'''
''',
'''
''',
[ 'christmas', 'easter', 'mothers_day', 'fathers_day' ] ],

    'to_bahai' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i',
'''
''',
'''
''',
[ 'from_bahai' ] ],

    'to_bahai_name' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i calendar with the weekday and month names',
'''
''',
'''
''',
[ 'from_bahai' ] ],

    'to_hebrew' : [
'calendars', 'converts a date to the equivalent date in the Hebrew calendar',
'''
''',
'''
''',
[ 'from_hebrew' ] ],

    'to_hebrew_name' : [
'calendars', 'converts a date to the equivalent date in the Hebrew calendar with the weekday and month names',
'''
''',
'''
''',
[ 'from_hebrew' ] ],

    'to_indian_civil' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar',
'''
''',
'''
''',
[ 'from_indian_civil' ] ],

    'to_indian_civil_name' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar with the weekday and month names',
'''
''',
'''
''',
[ 'from_indian_civil' ] ],

    'to_islamic' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar',
'''
''',
'''
''',
[ 'from_islamic' ] ],

    'to_islamic_name' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar with day and month names',
'''
''',
'''
''',
[ 'from_islamic' ] ],

    'to_iso' : [
'calendars', 'converts a date to the equivalent ISO date',
'''
''',
'''
''',
[ ] ],

    'to_iso_name' : [
'calendars', 'converts a date to the formatted version of the equivalent ISO date',
'''
''',
'''
''',
[ ] ],

    'to_julian' : [
'calendars', 'converts a date to the equivalent date in the Julian calendar',
'''
''',
'''
''',
[ ] ],

    'to_julian_day' : [
'calendars', 'returns the Julian day for a time value',
'''
''',
'''
''',
[ ] ],

    'to_lilian_day' : [
'calendars', 'returns the Lilian day for a time value',
'''
''',
'''
''',
[ ] ],

    'to_mayan' : [
'calendars', 'converts a date to the equivalent date in the Mayan long count calendar',
'''
''',
'''
''',
[ 'from_mayan' ] ],

    'to_ordinal_date' : [
'calendars', 'returns the date in the Ordinal Date format',
'''
''',
'''
''',
[ ] ],

    'to_persian' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar',
'''
''',
'''
''',
[ 'from_persian' ] ],

    'to_persian_name' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar with the weekday and month names',
'''
''',
'''
''',
[ 'from_persian' ] ],

    'veterans_day' : [
'calendars', 'returns the date of Veterans Day as celebrated in the U.S. for the year specified',
'''
''',
'''
''' + makeCommandExample( '2017 veterans_day' ),
[ 'independence_day', 'memorial_day', 'columbus_day' ] ],

    'weekday' : [
'calendars', 'calculates the day of the week of an absolute time',
'''
Given any date, the 'weekday' operator will determine what day of the week
that date occurred on.  It returns a number representing the weekday,
where 0 == Monday, 1 == Tuesday, 2 == Wednesday, 3 == Thursday,
4 == Friday, 5 == Saturday and 6 == Sunday.
''',
'''
''' + makeCommandExample( 'today weekday' ) + '''
''' + makeCommandExample( '1776-07-04 weekday' ) + '''
''' + makeCommandExample( '1965-03-31 weekday' ) + '''
''' + makeCommandExample( '1993-04-17 weekday' ),
[ 'calendar', 'nth_weekday', 'nth_weekday_of_year', 'weekday_name' ] ],

    'weekday_name' : [
'calendars', 'calculates the day of the week of an absolute time',
'''
Given any date, the 'weekday' operator will determine what day of the week
that date occurred on.  Unlike the 'weekday' operator, 'weekday_name' will
print out the actual name of the weekday.
''',
'''
''' + makeCommandExample( 'today weekday_name' ) + '''
''' + makeCommandExample( '1901-01-01 weekday_name' ) + '''
''' + makeCommandExample( '1852-02-29 weekday_name' ) + '''
''' + makeCommandExample( '1929-10-29 weekday_name' ) + '''
''' + makeCommandExample( '2043-04-17 weekday_name' ),
[ 'calendar', 'nth_weekday', 'nth_weekday_of_year' ] ],

    'year_calendar' : [
'calendars', 'prints a month calendar for the date value',
'''
The 'year_calendar' operator is special in that what it prints out is a
side-effect.  It actually returns the date value passed in as a result, so as
far as rpn is concerned, it's an operator that does nothing.
''',
'''
''',
[ 'calendar', 'weekday' ] ],


# //******************************************************************************
# //
# //  chemistry operators
# //
# //******************************************************************************

    'atomic_number' : [
'chemistry', 'returns the atomic number of element n',
'''
Elements can be referred to by atomic symbol or name.
''',
'''
''' + makeCommandExample( 'He atomic_number -s1' ) + '''
''' + makeCommandExample( 'Beryllium atomic_number -s1' ),
[ 'atomic_symbol', 'atomic_weight', 'element_name' ] ],

    'atomic_symbol' : [
'chemistry', 'returns the atomic symbol of element n',
'''
Elements can be referred to by atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range atomic_symbol -s1' ),
[ 'atomic_number', 'element_name', 'atomic_weight' ] ],

    'atomic_weight' : [
'chemistry', 'returns the atomic weight of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range atomic_weight -s1' ),
[ 'atomic_number', 'element_name', 'atomic_symbol', 'molar_mass' ] ],

    'element_block' : [
'chemistry', 'returns the block of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_block -s1' ),
[ 'element_group', 'element_description', 'element_period' ] ],

    'element_boiling_point' : [
'chemistry', 'returns the boiling point of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_boiling_point -s1' ),
[ 'element_melting_point', 'element_density' ] ],

    'element_density' : [
'chemistry', 'returns the density of element n for STP',
'''
Elements can be referred to by atomic symbol, atomic number or name.

Density is reported in grams per cubic centimeter under standard temperature
and pressure conditions.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_density -s1' ),
[ 'atomic_weight' ] ],

    'element_description' : [
'chemistry', 'returns the description of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_description -s1' ),
[ 'element_block', 'element_group', 'element_period', 'element_occurrence' ] ],

    'element_group' : [
'chemistry', 'returns the group of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_group -s1' ),
[ 'element_block', 'element_description', 'element_period' ] ],

    'element_melting_point' : [
'chemistry', 'returns the melting point of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_melting_point -s1' ),
[ 'element_boiling_point', 'element_density' ] ],

    'element_name' : [
'chemistry', 'returns the name of element n',
'''
Elements can be referred to by atomic symbol or atomic number.
''',
'''
''' + makeCommandExample( '1 10 range atomic_symbol element_name -s1' ),
[ ] ],

    'element_occurrence' : [
'chemistry', 'returns the occurrence of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_occurrence -s1' ),
[ 'element_description', 'element_state' ] ],

    'element_period' : [
'chemistry', 'returns the period of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_period -s1' ),
[ 'element_block', 'element_group' ] ],

    'element_state' : [
'chemistry', 'returns the state (at STP) of element n',
'''
Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_state -s1' ),
[ 'element_description', 'element_occurrence' ] ],

    'molar_mass' : [
'chemistry', 'returns the molar mass of molecule n',
'''
Currently, the parser for molecules is very simple.  Molecule expressions
consist solely of:

EN[EN...]

Where E is the atomic symbol of an element, and N is the count of atoms.
''',
'''
''' + makeCommandExample( 'H2O molar_mass' ) + '''
''' + makeCommandExample( 'C12H22O11 molar_mass' ),
[ 'atomic_weight' ] ],



# //******************************************************************************
# //
# //  combinatoric operators
# //
# //******************************************************************************

    'arrangements' : [
'combinatorics', 'calculates the number of arrangements of n or fewer objects out of n objects',
'''
''',
'''
''' + makeCommandExample( '1 10 range arrangements' ) + '''
''' + makeCommandExample( '5 arrangements' ) + '''
''' + makeCommandExample( '5 0 5 range permutations sum' ),
[ 'compositions', 'partitions' ] ],

    'bell_polynomial' : [
'combinatorics', 'evaluates the nth Bell polynomial with k',
'''
''',
'''
''',
[ ] ],

    'binomial' : [
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
''',
'''
''',
[ 'multinomial' ] ],

    'combinations' : [
'combinatorics', 'calculates the number of combinations of k out of n objects',
'''
''',
'''
''' + makeCommandExample( '6 3 combinations' ) + '''
''' + makeCommandExample( '10 8 combinations' ) + '''
''' + makeCommandExample( '21 15 combinations' ),
[ 'permutations' ] ],

    'compositions' : [
'combinatorics', 'returns a list containing all distinct ordered k-tuples of positive integers whose elements sum to n',
'''
This is referred to as the compositions of n.  Non-integer arguments are
truncated to integers.
''',
'''
''' + makeCommandExample( '5 2 compositions' ) + '''
''' + makeCommandExample( '5 3 compositions' ) + '''
''' + makeCommandExample( '5 4 compositions' ),
[ 'partitions', 'arrangements' ] ],

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
''' + makeCommandExample( '3 3 debruijn' ),
[ ] ],

    'denomination_combinations' : [
'combinatorics', 'calculates the number of combinations of items on n that add up to k',
'''
''',
'''
''' + makeCommandExample( '[ 1 5 10 25 50 100 ] 100 denomination_combinations' ),
[ ] ],

    'lah' : [
'combinatorics', 'calculate the Lah number for n and k',
'''
from https://en.wikipedia.org/wiki/Lah_number:

In mathematics, the Lah numbers, discovered by Ivo Lah in 1955, are
coefficients expressing rising factorials in terms of falling factorials.

Unsigned Lah numbers have an interesting meaning in combinatorics: they count
the number of ways a set of n elements can be partitioned into k nonempty
linearly ordered subsets. Lah numbers are related to Stirling numbers.

The Lah numbers are only defined for n >= k.
''',
'''
''' + makeCommandExample( '3 2 lah' ) + '''
''' + makeCommandExample( '12 1 lah' ) + '''
''' + makeCommandExample( '12 1 lah 12 ! -' ) + '''
''' + makeCommandExample( '7 2 lah' ) + '''
''' + makeCommandExample( '7 2 lah 6 7 ! *  2 / -' ) + '''
''' + makeCommandExample( '15 3 lah' ) + '''
''' + makeCommandExample( '15 3 lah [ 13 14 15 ! ] prod 12 / -' ) + '''
''' + makeCommandExample( '17 16 lah' ) + '''
''' + makeCommandExample( '17 16 lah 17 16 * -' ),
[ ] ],

    'multifactorial' : [
'combinatorics', 'calculates the nth k-factorial',
'''
The multifactorial operation is defined to be the product of every k-th
integer from n down to 1.  Therefore, the 1-multifactorial function is the
same as the 'factorial' operator and the 2-multifactorial function is the
same as the 'doublefac' operator.
''',
'''
''' + makeCommandExample( '1 20 range 3 multifactorial' ) + '''
''' + makeCommandExample( '1 20 range 4 multifactorial' ) + '''
''' + makeCommandExample( '1 20 range 5 multifactorial' ),
[ 'factorial', 'subfactorial' ] ],

    'multinomial' : [
'combinatorics', 'calculates the multinomial coefficient of list n',
'''
''',
'''
''',
[ 'binomial' ] ],

    'narayana' : [
'combinatorics', 'calculates the Nayayana number for n and k',
'''
From https://en.wikipedia.org/wiki/Narayana_number:

In combinatorics, the Narayana numbers N(n, k), n = 1, 2, 3 ..., 1 <= k <= n,
form a triangular array of natural numbers, called Narayana triangle, that
occur in various counting problems.  They are named after Indian mathematician
T. V. Narayana (1930-1987).
''',
'''
''' + makeCommandExample( '10 5 narayana' ) + '''
''' + makeCommandExample( '8 4 narayana' ) + '''
The 10th row of the 'Narayana triangle':
''' + makeCommandExample( '10 1 10 range narayana', indent=4 ),
[ ] ],

    'nth_apery' : [
'combinatorics', 'calculates the nth Apery number',
'''
''',
'''
''',
[ ] ],

    'nth_bell' : [
'combinatorics', 'calculates the nth Bell number',
'''
''',
'''
''',
[ ] ],

    'nth_bernoulli' : [
'combinatorics', 'calculates the nth Bernoulli number',
'''
From https://en.wikipedia.org/wiki/Bernoulli_number:

In mathematics, the Bernoulli numbers Bn are a sequence of rational numbers
with deep connections to number theory.

The Bernoulli numbers appear in the Taylor series expansions of the tangent
and hyperbolic tangent functions, in formulas for the sum of powers of the
first positive integers, in the Euler-Maclaurin formula, and in expressions
for certain values of the Riemann zeta function.

The Bernoulli numbers were discovered around the same time by the Swiss
mathematician Jakob Bernoulli, after whom they are named, and independently by
Japanese mathematician Seki Ko-wa.

Ada Lovelace's note G on the analytical engine from 1842 describes an algorithm
for generating Bernoulli numbers with Babbage's machine.  As a result, the
Bernoulli numbers have the distinction of being the subject of the first
published complex computer program.
''',
'''
''' + makeCommandExample( '1 20 range nth_bernoulli' ),
[ ] ],

    'nth_catalan' : [
'combinatorics', 'calculates nth Catalan number',
'''
From https://en.wikipedia.org/wiki/Catalan_number:

In combinatorial mathematics, the Catalan numbers form a sequence of natural
numbers that occur in various counting problems, often involving
recursively-defined objects. They are named after the Belgian mathematician
Eugene Charles Catalan (1814-1894).
''',
'''
''' + makeCommandExample( '1 20 range nth_catalan' ),
[ ] ],

    'nth_delannoy' : [
'combinatorics', 'calculates the nth Central Delannoy number',
'''
From https://en.wikipedia.org/wiki/Delannoy_number:

In mathematics, a central Delannoy number D describes the number of paths from
the southwest corner (0, 0) of a rectangular grid to the northeast corner
(n, n), using only single steps north, northeast, or east.  The Delannoy
numbers are named after French army officer and amateur mathematician Henri
Delannoy.
''',
'''
''' + makeCommandExample( '1 10 range nth_delannoy' ),
[ 'nth_schroeder' ] ],

    'nth_menage' : [
'combinatorics', 'calculate the nth Menage number for n and k',
'''
https://en.wikipedia.org/wiki/M%C3%A9nage_problem
''',
'''
''' + makeCommandExample( '1 10 range nth_menage' ),
[ ] ],

    'nth_motzkin' : [
'combinatorics', 'calculates the nth Motzkin number',
'''
From https://en.wikipedia.org/wiki/Motzkin_number:

In mathematics, a Motzkin number for a given number n is the number of
different ways of drawing non-intersecting chords between n points on a circle
(not necessarily touching every point by a chord).  The Motzkin numbers are
named after Theodore Motzkin, and have very diverse applications in geometry,
combinatorics and number theory.
''',
'''
''' + makeCommandExample( '1 10 range nth_motzkin' ),
[ ] ],

    'nth_pell' : [
'combinatorics', 'calculates the nth Pell number',
'''
From https://en.wikipedia.org/wiki/Pell_number:

In mathematics, the Pell numbers are an infinite sequence of integers, known
since ancient times, that comprise the denominators of the closest rational
approximations to the square root of 2. This sequence of approximations begins
1/1, 3/2, 7/5, 17/12, and 41/29, so the sequence of Pell numbers begins with
1, 2, 5, 12, and 29.
''',
'''
''' + makeCommandExample( '1 20 range nth_pell' ),
[ ] ],

    'nth_schroeder' : [
'combinatorics', 'calculates the nth Schroeder number',
'''
In mathematics, a Schroeder number describes the number of paths from the
southwest corner (0, 0) of an n x n grid to the northeast corner (n, n), using
only single steps north, northeast, or east, that do not rise above the SW-NE
diagonal.

They were named after the German mathematician Ernst Schroeder.
''',
'''
''' + makeCommandExample( '1 10 range nth_schroeder' ),
[ 'nth_delannoy' ] ],

    'nth_schroeder_hipparchus' : [
'combinatorics', 'calculates the nth Schroeder-Hipparchus number',
'''
From https://en.wikipedia.org/wiki/Schr%C3%B6der%E2%80%93Hipparchus_number:

In number theory, the Schroeder-Hipparchus numbers form an integer sequence
that can be used to count the number of plane trees with a given set of leaves,
the number of ways of inserting parentheses into a sequence, and the number of
ways of dissecting a convex polygon into smaller polygons by inserting
diagonals.

They are also called the super-Catalan numbers, the little Schroeder numbers,
or the Hipparchus numbers, after Eugene Charles Catalan and his Catalan numbers,
Ernst Schroeder and the closely related Schroeder numbers, and the ancient Greek
mathematician Hipparchus who appears from evidence in Plutarch to have known of
these numbers.
''',
'''
''' + makeCommandExample( '1 12 range nth_schroeder_hipparchus' ),
[ ] ],

    'nth_sylvester' : [
'combinatorics', 'calculates the nth Sylvester number',
'''
In number theory, Sylvester's sequence is an integer sequence in which each member
of the sequence is the product of the previous members, plus one.

Sylvester's sequence is named after James Joseph Sylvester, who first
investigated it in 1880. Its values grow doubly exponentially, and the sum of
its reciprocals forms a series of unit fractions that converges to 1 more
rapidly than any other series of unit fractions with the same number of terms.
''',
'''
''' + makeCommandExample( '1 10 range nth_sylvester' ),
[ ] ],

    'partitions' : [
'combinatorics', 'returns the partition number for n',
'''
From https://en.wikipedia.org/wiki/Partition_%28number_theory%29:

In number theory and combinatorics, a partition of a positive integer n, also
called an integer partition, is a way of writing n as a sum of positive
integers.  Two sums that differ only in the order of their summands are
considered the same partition.

For example, 4 can be partitioned in five distinct ways:
    4
    3 + 1
    2 + 2
    2 + 1 + 1
    1 + 1 + 1 + 1
''',
'''
''' + makeCommandExample( '4 partitions' ),
[ 'compositions', 'arrangements' ] ],

    'permutations' : [
'combinatorics', 'calculates the number of permutations of k out of n objects',
'''
When calculating the number of permutations of k objects, order matters.
''',
'''
''' + makeCommandExample( '5 2 permutations' ) + '''
''' + makeCommandExample( '10 7 permutations' ) + '''
''' + makeCommandExample( '20 10 permutations' ),
[ 'combinations' ] ],


# //******************************************************************************
# //
# //  complex math operators
# //
# //******************************************************************************

    'argument' : [
'complex_math', 'calculates complex argument (phase) of n',
'''
The complex argument, or phase, of a complex number is defined as the
signed angle between the positive real axis and n in the complex plane.
''',
'''
''' + makeCommandExample( '3 3 i + arg' ) + '''
''' + makeCommandExample( '3 3 i + arg radians degrees convert' ),
[ 'conjugate', 'real', 'imaginary', 'i' ] ],

    'conjugate' : [
'complex_math', 'calculates complex conjugate of n',
'''
The complex conjugate is simply the nunmber with the same real part and an
imaginary part with the same magnitude but opposite sign.
''',
'''
''' + makeCommandExample( '3 3 i + conj' ),
[ 'argument', 'real', 'imaginary', 'i' ] ],

    'i' : [
'complex_math', 'multiplies n by i',
'''
''',
'''
''' + makeCommandExample( 'e pi i **' ) + '''

There's a rounding error here, but this demonstrates Euler's famous equation:

e ^ ( pi * i ) = -1
''',
[ 'argument', 'conjugate', 'real', 'imaginary' ] ],

    'imaginary' : [
'complex_math', 'returns the imaginary part of n',
'''
''',
'''
''' + makeCommandExample( '7 imaginary' ) + '''
''' + makeCommandExample( '7 i imaginary' ) + '''
''' + makeCommandExample( '3 4 i + imaginary' ),
[ 'real', 'i' ] ],

    'real' : [
'complex_math', 'returns the real part of n',
'''
''',
'''
''' + makeCommandExample( '7 real' ) + '''
''' + makeCommandExample( '7 i real' ) + '''
''' + makeCommandExample( '3 4 i + real' ),
[ 'imaginary', 'i', 'argument', 'conjugate' ] ],


# //******************************************************************************
# //
# //  constants operators
# //
# //******************************************************************************

    'aa_battery' : [
'constants', 'returns the approximate energy content of a fully-charged AA alkaline battery',
'''
''',
'''
''' + makeCommandExample( 'aa_battery' ) + '''
''' + makeCommandExample( 'gallon_of_gasoline aa_battery /' ),
[ 'gallon_of_gasoline' ] ],

    'alpha_particle_mass' : [
'constants', 'returns the mass of an alpha particle',
'''
The alpha particle is the equivalent of a helium nucleus, and consists of two
protons and two neutrons.

Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'alpha_particle_mass' ) + '''
''' + makeCommandExample( 'alpha_particle_mass proton_mass /' ),
[ 'proton_mass', 'electron_mass', 'helion_mass', 'neutron_mass', 'deuteron_mass' ] ],

    'apery_constant' : [
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
''' + makeCommandExample( '-a50 -d5 apery' ) + '''
''' + makeCommandExample( '-a50 -d5 3 zeta' ),
[ ] ],

    'avogadro_number' : [
'constants', 'returns Avogadro\'s number, the number of atoms in a mole',
'''
Ref: CODATA 2014
''',
'''
''' + makeCommandExample( 'avogadro' ) + '''
''' + makeCommandExample( '-a24 avogadro' ),
[ ] ],

    'bohr_radius' : [
'constants', 'returns the Bohr radius',
'''
''',
'''
''' + makeCommandExample( 'bohr_radius' ),
[ ] ],

    'boltzmann_constant' : [
'constants', 'returns the Boltzmann constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'boltzmann_constant' ),
[ ] ],

    'catalan_constant' : [
'constants', 'returns Catalan\'s constant',
'''
''',
'''
''' + makeCommandExample( 'catalan_constant' ),
[ ] ],

    'champernowne_constant' : [
'constants', 'returns the Champernowne constant for the input base',
'''
The Champernowne constant is a transcendental number created by successive
appending every natural number as a decimal value.

The Champernowne constant is normally defined for base 10, but this operator
can also apply the same concept for any input base.
''',
'''
''' + makeCommandExample( '-a60 champernowne_constant' ) + '''
The base 7 Champernowne constant in base 7:
''' + makeCommandExample( '-a60 -b7 champernowne_constant -r7' ) + '''
The base 7 Champernowne constant converted to base 10:
''' + makeCommandExample( '-a60 -b7 champernowne_constant' ),
[ ] ],

    'copeland_erdos_constant' : [
'constants', 'returns the Copeland-Erdos constant',
'''
''',
'''
''' + makeCommandExample( '-a60 copeland' ),
[ ] ],

    'default' : [
'constants', 'used with settings operators',
'''
''',
'''
''',
[ ] ],

    'density_of_hg' : [
'constants', 'returns the density of mercury in kg/m^3',
'''
''',
'''
''' + makeCommandExample( 'density_of_hg' ) + '''
''' + makeCommandExample( '80 element_density kilogram meter 3 ** / convert' ),
[ ] ],

    'deuteron_mass' : [
'constants', 'returns the mass of a deuterium nucleus',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'deuteron_mass' ),
[ 'triton_mass', 'proton_mass', 'electron_mass', 'alpha_particle_mass', 'neutron_mass', 'helion_mass' ] ],

    'e' : [
'constants', 'returns e (Euler\'s number)',
'''
''',
'''
''' + makeCommandExample( 'e' ),
[ 'pi', 'phi' ] ],

    'eddington_number' : [
'constants', 'returns Arthur Eddington\'s famous estimate of the number of subatomic particles in the Universe',
'''In 1938, Arthur Eddington famously claimed that, "I believe there are
15,747,724,136,275,002,577,605,653,961,181,555,468,044,717,914,527,116,709,366,231,425,076,185,631,031,296
protons in the universe and the same number of electrons."  This number is equal to 136 * 2^256.''',
'''
''' + makeCommandExample( '-c -a100 eddington_number' ),
[ ] ],

    'electric_constant' : [
'constants', 'returns the electric constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'electric_constant' ),
[ ] ],

    'electron_charge' : [
'constants', 'returns the charge of an electron',
'''
''',
'''
''' + makeCommandExample( 'electron_charge' ),
[ ] ],

    'electron_mass' : [
'constants', 'returns the mass of an electron',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'electron_mass' ) + '''
''' + makeCommandExample( 'proton_mass electron_mass /' ),
[ 'proton_mass', 'muon_mass', 'tau_mass', 'neutron_mass' ] ],

    'euler_mascheroni_constant' : [
'constants', 'returns the Euler-Mascheroni constant',
'''
''',
'''
''' + makeCommandExample( 'euler_mascheroni_constant' ),
[ ] ],

    'false' : [
'constants', 'used with boolean settings operators',
'''
'false' simply evaluates to 0
''',
'''
''',
[ 'true' ] ],

    'faraday_constant' : [
'constants', 'returns Faraday\'s Constant',
'''
''',
'''
''' + makeCommandExample( 'faraday_constant' ),
[ ] ],

    'fine_structure_constant' : [
'constants', 'returns the fine-structure constant',
'''
''',
'''
''' + makeCommandExample( 'fine_structure_constant' ),
[ ] ],

    'gallon_of_ethanol' : [
'constants', 'returns the energy content of a gallon of ethanol',
'''
''',
'''
''' + makeCommandExample( 'gallon_of_ethanol' ) + '''
''' + makeCommandExample( 'gallon_of_gasoline gallon_of_ethanol /' ),
[ 'gallon_of_gasoline', 'aa_battery' ] ],

    'gallon_of_gasoline' : [
'constants', 'returns the energy content of a gallon of gasoline',
'''
''',
'''
''' + makeCommandExample( 'gallon_of_gasoline' ) + '''
''' + makeCommandExample( 'gallon_of_gasoline gallon_of_ethanol /' ),
[ 'gallon_of_ethanol', 'aa_battery' ] ],

    'glaisher_constant' : [
'constants', 'returns Glaisher\'s constant',
'''
''',
'''
''' + makeCommandExample( 'glaisher_constant' ),
[ ] ],

    'helion_mass' : [
'constants', 'returns the mass of a helion',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'helion_mass' ),
[ 'proton_mass', 'alpha_particle_mass', 'neutron_mass', 'deuteron_mass', 'triton_mass' ] ],

    'infinity' : [
'constants', 'evaluates to infinity, used to describe ranges for nsum, nprod, and limit',
'''
''',
'''
''' + makeCommandExample( '1 inf lambda x fib 1/x nsum' ) + '''
''' + makeCommandExample( '1 inf lambda x lucas 1/x nsum' ) + '''
''' + makeCommandExample( 'phi' ) + '''
''' + makeCommandExample( 'infinity lambda x 1 + fib x fib / limit' ),
[ 'negative_infinity' ] ],

    'itoi' : [
'constants', 'returns i to the i power',
'''
''',
'''
''' + makeCommandExample( '1 i 1 i **' ) + '''
''' + makeCommandExample( 'itoi' ),
[ 'i' ] ],

    'khinchin_constant' : [
'constants', 'returns Khinchin\'s constant',
'''
''',
'''
''' + makeCommandExample( 'khinchin_constant' ),
[ ] ],

    'magnetic_constant' : [
'constants', 'returns the magnetic constant',
'''
This constant is exact by definition.

Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'magnetic_constant' ),
[ ] ],

    'max_char' : [
'constants', 'returns the maximum 8-bit signed integer',
'''
''',
'''
''' + makeCommandExample( 'max_char' ) + '''
''' + makeCommandExample( 'max_char -x' ),
[ 'min_char', 'max_uchar', 'max_short', 'max_long' ] ],

    'max_double' : [
'constants', 'returns the largest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'max_double' ) + '''
''' + makeCommandExample( 'max_double double -x' ),
[ 'max_float', 'min_double' ] ],

    'max_float' : [
'constants', 'returns the largest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'max_float' ) + '''
''' + makeCommandExample( 'max_float float -x' ),
[ 'max_double', 'min_float' ] ],

    'max_long' : [
'constants', 'returns the maximum 32-bit signed integer',
'''
This is the largest number that can be represented by a 32-bit signed
integer assuming two's complement representation.

''',
'''
''' + makeCommandExample( 'max_long' ) + '''
When does a 32-bit time_t wrap?
''' + makeCommandExample( '1970-01-01 max_long seconds +' ),
[ 'min_long', 'max_longlong', 'max_char', 'max_ulong', 'max_short' ] ],

    'max_longlong' : [
'constants', 'returns the maximum 64-bit signed integer',
'''
This is the largest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'max_longlong' ) + '''
How long until a 64-bit time_t would wrap?
''' + makeCommandExample( '-c max_longlong seconds years convert' ),
[ 'min_longlong', 'max_quadlong', 'max_long', 'max_ulonglong' ] ],

    'max_quadlong' : [
'constants', 'returns the maximum 128-bit signed integer',
'''
This is the largest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( '-a40 max_quadlong' ),
[ 'min_quadlong', 'min_uquadlong', 'max_longlong', 'max_long' ] ],

    'max_short' : [
'constants', 'returns the maximum 16-bit signed integer',
'''
This is the largest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'max_short' ),
[ 'min_short', 'max_ushort', 'max_char', 'max_long' ] ],

    'max_uchar' : [
'constants', 'returns the maximum 8-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
''' + makeCommandExample( 'max_uchar' ),
[ 'min_uchar', 'max_char', 'max_ushort', 'max_ulong' ] ],

    'max_ulong' : [
'constants', 'returns the maximum 32-bit unsigned integer',
'''
This is the largest number that can be represented by a 32-bit unsigned
integer.
''',
'''
''' + makeCommandExample( 'max_ulong' ),
[ 'min_ulong', 'max_long', 'max_uchar', 'max_ushort' ] ],

    'max_ulonglong' : [
'constants', 'returns the maximum 64-bit unsigned integer',
'''
This is the largest number that can be represented by a 64-bit unsigned
integer.
''',
'''
''' + makeCommandExample( '-a20 max_ulonglong' ),
[ 'min_ulonglong', 'max_longlong', 'max_uquadlong', 'max_ulong' ] ],

    'max_uquadlong' : [
'constants', 'returns the maximum 128-bit unsigned integer',
'''
This is the largest number that can be represented by a 128-bit unsigned
integer.
''',
'''
''' + makeCommandExample( '-a40 max_uquadlong' ),
[ 'min_uquadlong', 'max_quadlong', 'max_ulonglong', 'max_ulong' ] ],

    'max_ushort' : [
'constants', 'returns the maximum 16-bit unsigned integer',
'''
This is the largest number that can be represented by a 16-bit unsigned
integer.
''',
'''
''' + makeCommandExample( 'max_ushort' ),
[ 'min_ushort', 'max_short', 'max_uchar', 'max_ulong' ] ],

    'merten_constant' : [
'constants', 'returns Merten\'s constant',
'''
''',
'''
''' + makeCommandExample( '-a50 merten_constant' ),
[ ] ],

    'mills_constant' : [
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

rpn does not calculate Mills' constant.  The value is hard-coded to 3500
decimal places.
''',
'''
''' + makeCommandExample( '-a50 mills_constant' ),
[ ] ],

    'min_char' : [
'constants', 'returns the minimum 8-bit signed integer',
'''
This is the smallest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'min_char' ) + '''
''' + makeCommandExample( 'min_char -x' ) + '''
''' + makeCommandExample( 'max_char min_char -' ),
[ 'max_char', 'min_uchar', 'min_short', 'min_long' ] ],

    'min_double' : [
'constants', 'returns the smallest value that can be represented by a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'min_double' ) + '''
''' + makeCommandExample( 'min_double double -x' ),
[ 'max_double', 'min_float' ] ],

    'min_float' : [
'constants', 'returns the smallest value that can be represented by a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'min_float' ) + '''
''' + makeCommandExample( 'min_float float -x' ),
[ 'max_float', 'min_double' ] ],

    'min_long' : [
'constants', 'returns the minimum 32-bit signed integer',
'''
This is the smallest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'min_long' ) + '''
''' + makeCommandExample( 'max_long min_long -' ),
[ 'max_long', 'min_ulong', 'min_short', 'min_char' ] ],

    'min_longlong' : [
'constants', 'returns the minimum 64-bit signed integer',
'''
This is the smallest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'min_longlong' ) + '''
''' + makeCommandExample( 'max_longlong min_longlong - 1 + log2' ),
[ 'max_longlong', 'min_ulonglong', 'min_long', 'min_quadlong' ] ],

    'min_quadlong' : [
'constants', 'returns the minimum 128-bit signed integer',
'''
This is the smallest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'min_quadlong' ) + '''
''' + makeCommandExample( 'max_quadlong min_quadlong - 1 + log2' ),
[ 'max_quadlong', 'min_uquadlong', 'min_long', 'min_quadlong' ] ],

    'min_short' : [
'constants', 'returns the minimum 16-bit signed integer',
'''
This is the smallest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''',
'''
''' + makeCommandExample( 'min_short' ) + '''
''' + makeCommandExample( 'max_short min_short -' ),
[ 'max_short', 'min_ushort', 'min_char', 'min_long' ] ],

    'min_uchar' : [
'constants', 'returns the minimum 8-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
''' + makeCommandExample( 'min_uchar' ) + '''
''' + makeCommandExample( 'max_uchar min_uchar -' ),
[ 'min_char', 'max_uchar', 'min_ushort', 'min_ulong' ] ],

    'min_ulong' : [
'constants', 'returns the minimum 32-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
''' + makeCommandExample( 'min_ulong' ) + '''
''' + makeCommandExample( 'max_ulong min_ulong - 1 + log2' ),
[ 'max_ulong', 'min_long', 'min_uchar', 'min_ushort' ] ],

    'min_ulonglong' : [
'constants', 'returns the minimum 64-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
''' + makeCommandExample( 'min_ulonglong' ) + '''
''' + makeCommandExample( 'max_ulonglong min_ulonglong - 1 + log2' ),
[ 'min_longlong', 'max_ulonglong', 'min_ulong', 'min_uquadlong' ] ],

    'min_uquadlong' : [
'constants', 'returns the minimum 128-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
''' + makeCommandExample( 'min_uquadlong' ) + '''
''' + makeCommandExample( 'max_uquadlong min_uquadlong - 1 + log2' ),
[ 'min_quadlong', 'max_uquadlong', 'min_ulong', 'min_ulonglong' ] ],

    'min_ushort' : [
'constants', 'returns the minimum 16-bit unsigned integer',
'''
By definition, the smallest unsigned integer of any size is 0.
''',
'''
''' + makeCommandExample( 'min_ushort' ) + '''
''' + makeCommandExample( 'max_ushort min_ushort -' ),
[ 'max_ushort', 'min_short', 'min_uchar', 'min_ulong' ] ],

    'molar_gas_constant' : [
'constants', 'returns the molar gas constant',
'''
Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'molar_gas_constant' ),
[ ] ],

    'muon_mass' : [
'constants', 'returns the mass of a muon',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''',
[ 'proton_mass', 'electron_mass', 'tau_mass', 'neutron_mass' ] ],

    'negative_infinity' : [
'constants', 'evaluates to negative infinity, used to describe ranges for nsum, nprod, and limit',
'''
''',
'''
''',
[ 'infinity' ] ],

    'neutron_mass' : [
'constants', 'returns the mass of a neutron',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'neutron_mass' ) + '''
''' + makeCommandExample( 'proton_mass neutron_mass /' ),
[ 'proton_mass', 'electron_mass', 'alpha_particle_mass', 'helion_mass', 'deuteron_mass', 'triton_mass' ] ],

    'newton_constant' : [
'constants', 'returns Newton\'s gravitational constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'newton_constant' ),
[ ] ],

    'omega_constant' : [
'constants', 'returns the Omega constant',
'''
''',
'''
''' + makeCommandExample( 'omega_constant' ),
[ ] ],

    'phi' : [
'constants', 'returns phi (the Golden Ratio)',
'''
''',
'''
''' + makeCommandExample( 'phi' ),
[ 'e', 'pi' ] ],

    'pi' : [
'constants', 'returns pi (Archimedes\' constant)',
'''
''',
'''
''' + makeCommandExample( 'pi' ),
[ 'e', 'phi' ] ],

    'planck_area' : [
'constants', 'returns the Planck area',
'''
This is a derived constant calculated from the CODATA value for the Planck
length.

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_area' ),
[ ] ],

    'planck_angular_frequency' : [
'constants', 'returns the ',
'''
''',
'''
''' + makeCommandExample( 'planck_angular_frequency' ),
[ ] ],

    'planck_charge' : [
'constants', 'returns the Planck charge',
'''
''',
'''
''' + makeCommandExample( 'planck_charge' ),
[ ] ],

    'planck_constant' : [
'constants', 'returns the Planck constant',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_constant' ),
[ ] ],

    'planck_current' : [
'constants', 'returns the Planck current',
'''
''',
'''
''' + makeCommandExample( 'planck_current' ),
[ ] ],

    'planck_density' : [
'constants', 'returns the Planck density',
'''
This is a derived constant calculated from the CODATA values for the Planck
mass and Planck length.

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_density' ),
[ ] ],

    'planck_energy' : [
'constants', 'returns the Planck energy',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_energy' ),
[ ] ],

    'planck_energy_density' : [
'constants', 'returns the Planck energy density',
'''
''',
'''
''' + makeCommandExample( 'planck_energy_density' ),
[ ] ],

    'planck_force' : [
'constants', 'returns the Planck force',
'''
This is a derived constant calculated from the CODATA values for the Planck
mass, Planck length and Planck time.

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_force' ),
[ ] ],

    'planck_impedance' : [
'constants', 'returns the Planck impedance',
'''
''',
'''
''' + makeCommandExample( 'planck_impedance' ),
[ ] ],

    'planck_intensity' : [
'constants', 'returns the Planck intensity',
'''
''',
'''
''' + makeCommandExample( 'planck_intensity' ),
[ ] ],

    'planck_length' : [
'constants', 'returns the Planck length',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_length' ),
[ ] ],

    'planck_mass' : [
'constants', 'returns the Planck mass',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_mass' ),
[ ] ],

    'planck_momentum' : [
'constants', 'returns the Planck momentum',
'''
''',
'''
''' + makeCommandExample( 'planck_momentum' ),
[ ] ],

    'planck_power' : [
'constants', 'returns the Planck power',
'''
''',
'''
''' + makeCommandExample( 'planck_power' ),
[ ] ],

    'planck_pressure' : [
'constants', 'returns the Planck pressure',
'''
''',
'''
''' + makeCommandExample( 'planck_pressure' ),
[ ] ],

    'planck_temperature' : [
'constants', 'returns the Planck temperature',
'''
Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_temperature' ),
[ ] ],

    'planck_time' : [
'constants', 'returns Planck time',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_time' ),
[ ] ],

    'planck_voltage' : [
'constants', 'returns the Planck voltage',
'''
''',
'''
''' + makeCommandExample( 'planck_voltage' ),
[ ] ],

    'planck_volume' : [
'constants', 'returns the Planck volume',
'''
This is a derived constant calculated from the CODATA value for the Planck
length.

Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'planck_volume' ),
[ ] ],

    'plastic_constant' : [
'constants', 'returns the Plastic constant',
'''
From https://en.wikipedia.org/wiki/Plastic_number:

In mathematics, the plastic number ? (also known as the plastic constant, the
minimal Pisot number, the platin number, Siegel's number or, in French, le
nombre radiant) is a mathematical constant which is the unique real solution
of the cubic equation x^3 = x + 1.

Dutch architect and Benedictine monk Dom Hans van der Laan gave the name
plastic number ('het plastische getal' in Dutch) to this number in 1928.  In
1924, 4 years prior to von der Laan's christening of the number's name, French
engineer Gerard Cordonnier had already discovered the number and referred to it
as the radiant number ('le nombre radiant' in French).  Unlike the names of the
golden ratio and silver ratio, the word plastic was not intended by van der
Laan to refer to a specific substance, but rather in its adjectival sense,
meaning something that can be given a three-dimensional shape.  This, according
to Padovan, is because the characteristic ratios of the number,
3/4 and 1/7, relate to the limits of human perception in relating one physical
size to another.  Van der Laan designed the 1967 St. Benedictusberg Abbey church
to these plastic number proportions.
''',
'''
''' + makeCommandExample( 'plastic_constant' ),
[ 'silver_ratio', 'phi' ] ],

    'prevost_constant' : [
'constants', 'calculates Prevost\'s constant',
'''
Prevost's constant is the sum of the reciprocals of the Fibonacci numbers.
''',
'''
''' + makeCommandExample( 'prevost_constant' ),
[ ] ],

    'proton_mass' : [
'constants', 'returns the mass of a proton',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'proton_mass' ),
[ 'neutron_mass', 'electron_mass', 'alpha_particle_mass', 'helion_mass', 'deuteron_mass', 'triton_mass' ] ],

    'radiation_constant' : [
'constants', 'returns the Radiation Constant',
'''
''',
'''
''' + makeCommandExample( 'radiation_constant' ),
[ ] ],

    'reduced_planck_constant' : [
'constants', 'returns the reduced Planck constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'reduced_planck_constant' ) + '''
''' + makeCommandExample( 'planck_constant reduced_planck_constant /' ),
[ ] ],

    'robbins_constant' : [
'constants', 'returns Robbins\' constant',
'''
Robbins' constant represents the average distance between two points selected
at random within a unit cube.
''',
'''
''' + makeCommandExample( 'robbins_constant' ),
[ ] ],

    'rydberg_constant' : [
'constants', 'returns the Rydberg constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'rydberg_constant' ),
[ ] ],

    'sidereal_year' : [
'constants', 'returns the length of a sideral year for the Earth',
'''
''',
'''
''' + makeCommandExample( 'sidereal_year' ),
[ ] ],

    'silver_ratio' : [
'constants', 'returns the "silver ratio", defined to be 1 + sqrt( 2 )',
'''
''',
'''
''' + makeCommandExample( 'silver_ratio' ),
[ ] ],

    'solar_constant' : [
'constants', 'returns the solar constant',
'''
This operator returns the average amount of luminous energy the Earth receives
from the Sun.  The solar constant does vary slightly over time due to
fluctuations in solar energy output.
''',
'''
''' + makeCommandExample( 'solar_constant' ),
[ ] ],

    'speed_of_light' : [
'constants', 'returns the speed of light in a vacuum in meters per second',
'''
''',
'''
''' + makeCommandExample( 'speed_of_light' ),
[ ] ],

    'stefan_boltzmann_constant' : [
'constants', 'returns the Stefan-Boltzmann constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'stefan_boltzmann_constant' ),
[ ] ],

    'tau_mass' : [
'constants', 'returns the mass of a tau particle',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'tau_mass' ),
[ 'proton_mass', 'neutron_mass', 'electron_mass', 'muon_mass' ] ],

    'thue_morse_constant' : [
'constants', 'calculates the Thue-Morse constant',
'''
''',
'''
''' + makeCommandExample( 'thue_morse_constant' ),
[ ] ],

    'triton_mass' : [
'constants', 'returns the mass of a tritium nucleus',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'triton_mass' ) + '''
''' + makeCommandExample( 'triton_mass avogadros_number * grams convert' ),
[ 'proton_mass', 'neutron_mass', 'electron_mass', 'alpha_particle_mass', 'helion_mass', 'deuteron_mass', 'helion_mass' ] ],

    'tropical_year' : [
'constants', 'returns the length of a tropical year for the Earth',
'''
''',
'''
''' + makeCommandExample( 'tropical_year' ),
[ ] ],

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
''',
[ 'false' ] ],

    'vacuum_impedance' : [
'constants', 'returns the vacuum impedence constant',
'''
Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'vacuum_impedance' ),
[ ] ],

    'von_klitzing_constant' : [
'constants', 'returns the von Klitzing constant',
'''
Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'von_klitzing_constant' ),
[ ] ],


# //******************************************************************************
# //
# //  planet, sun and moon constants
# //
# //******************************************************************************

    'sun_luminosity' : [
'constants', 'returns the luminosity of the Sun',
'''
''',
'''
''' + makeCommandExample( 'sun_luminosity' ),
[ ] ],

    'sun_mass' : [
'constants', 'returns the mass of the Sun',
'''
Ref:  http://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
''',
'''
''' + makeCommandExample( 'sun_mass' ),
[ ] ],

    'sun_radius' : [
'constants', 'returns the radius of the Sun',
'''
''',
'''
''' + makeCommandExample( 'sun_radius' ),
[ ] ],

    'sun_volume' : [
'constants', 'returns the volume of the Sun',
'''
''',
'''
''' + makeCommandExample( 'sun_volume' ),
[ ] ],

    'mercury_mass' : [
'constants', 'returns the mass of the planet Mercury',
'''
''',
'''
''' + makeCommandExample( 'mercury_mass' ),
[ ] ],

    'mercury_radius' : [
'constants', 'returns the radius of the planet Mercury',
'''
''',
'''
''' + makeCommandExample( 'mercury_radius' ),
[ ] ],

    'mercury_revolution' : [
'constants', 'returns the revolution time of the planet Mercury around the Sun',
'''
''',
'''
''' + makeCommandExample( 'mercury_revolution' ),
[ ] ],

    'mercury_volume' : [
'constants', 'returns the volume of the planet Mercury',
'''
''',
'''
''' + makeCommandExample( 'mercury_volume' ),
[ ] ],

    'venus_mass' : [
'constants', 'returns the mass of the planet Venus',
'''
''',
'''
''' + makeCommandExample( 'venus_mass' ),
[ ] ],

    'venus_radius' : [
'constants', 'returns the radius of the planet Venus',
'''
''',
'''
''' + makeCommandExample( 'venus_radius' ),
[ ] ],

    'venus_revolution' : [
'constants', 'returns the revolution time of the planet Venus around the Sun',
'''
''',
'''
''' + makeCommandExample( 'venus_revolution' ),
[ ] ],

    'venus_volume' : [
'constants', 'returns the volume of the planet Venus',
'''
''',
'''
''' + makeCommandExample( 'venus_volume' ),
[ ] ],

    'earth_mass' : [
'constants', 'returns the mass of the Earth',
'''
''',
'''
''' + makeCommandExample( 'earth_mass' ),
[ ] ],

    'earth_radius' : [
'constants', 'returns the radius of the planet Earth',
'''
''',
'''
''' + makeCommandExample( 'earth_radius' ),
[ ] ],

    'earth_volume' : [
'constants', 'returns the volume of the planet Earth',
'''
''',
'''
''' + makeCommandExample( 'earth_volume' ),
[ ] ],

    'moon_radius' : [
'constants', 'returns the radius of the Moon',
'''
''',
'''
''' + makeCommandExample( 'moon_radius' ),
[ ] ],

    'moon_revolution' : [
'constants', 'returns teh revolution time for the Moon around the Earth',
'''
''',
'''
''' + makeCommandExample( 'moon_revolution' ),
[ ] ],

    'moon_volume' : [
'constants', 'returns the volume of the Moon',
'''
''',
'''
''' + makeCommandExample( 'moon_volume' ),
[ ] ],

    'mars_mass' : [
'constants', 'returns the mass of the planet Mars',
'''
''',
'''
''' + makeCommandExample( 'mars_mass' ),
[ ] ],

    'mars_radius' : [
'constants', 'returns the radius ofthe planet Mars',
'''
''',
'''
''' + makeCommandExample( 'mars_radius' ),
[ ] ],

    'mars_revolution' : [
'constants', 'returns revolution time of the planet Mars around the Sun',
'''
''',
'''
''' + makeCommandExample( 'mars_revolution' ),
[ ] ],

    'mars_volume' : [
'constants', 'returns the volume of the planet Mars',
'''
''',
'''
''' + makeCommandExample( 'mars_volume' ),
[ ] ],

    'jupiter_mass' : [
'constants', 'returns the mass of the planet Jupiter',
'''
''',
'''
''' + makeCommandExample( 'jupiter_mass' ),
[ ] ],

    'jupiter_radius' : [
'constants', 'returns the radius of the planet Jupiter',
'''
''',
'''
''' + makeCommandExample( 'jupiter_radius' ),
[ ] ],

    'jupiter_revolution' : [
'constants', 'returns the revolution time of the planet Jupiter around the Sun',
'''
''',
'''
''' + makeCommandExample( 'jupiter_revolution' ),
[ ] ],

    'jupiter_volume' : [
'constants', 'returns the volume of the planet Jupiter',
'''
''',
'''
''' + makeCommandExample( 'jupiter_volume' ),
[ ] ],

    'saturn_mass' : [
'constants', 'returns the mass of the planet Saturn',
'''
''',
'''
''' + makeCommandExample( 'saturn_mass' ),
[ ] ],

    'saturn_radius' : [
'constants', 'returns the radius of the planet Saturn',
'''
''',
'''
''' + makeCommandExample( 'saturn_radius' ),
[ ] ],

    'saturn_revolution' : [
'constants', 'returns the revolution time of the planet Saturn around the Sun',
'''
''',
'''
''' + makeCommandExample( 'saturn_revolution' ),
[ ] ],

    'saturn_volume' : [
'constants', 'returns the volume of the planet Saturn',
'''
''',
'''
''' + makeCommandExample( 'saturn_volume' ),
[ ] ],

    'uranus_mass' : [
'constants', 'returns the mass of the planet Uranus',
'''
''',
'''
''' + makeCommandExample( 'uranus_mass' ),
[ ] ],

    'uranus_radius' : [
'constants', 'returns the radius of the planet Uranus',
'''
''',
'''
''' + makeCommandExample( 'uranus_radius' ),
[ ] ],

    'uranus_revolution' : [
'constants', 'returns the revolution time of the planet Uranus around the Sun',
'''
''',
'''
''' + makeCommandExample( 'uranus_revolution' ),
[ ] ],

    'uranus_volume' : [
'constants', 'returns the volume of the planet Uranus',
'''
''',
'''
''' + makeCommandExample( 'uranus_volume' ),
[ ] ],

    'neptune_mass' : [
'constants', 'returns the mass of the planet Neptune',
'''
''',
'''
''' + makeCommandExample( 'neptune_mass' ),
[ ] ],

    'neptune_radius' : [
'constants', 'returns the radius ofthe planet Neptune',
'''
''',
'''
''' + makeCommandExample( 'neptune_radius' ),
[ ] ],

    'neptune_revolution' : [
'constants', 'returns the revolution time of the planet Neptune around the Sun',
'''
''',
'''
''' + makeCommandExample( 'neptune_revolution' ),
[ ] ],

    'neptune_volume' : [
'constants', 'returns the volume of the planet Neptune',
'''
''',
'''
''' + makeCommandExample( 'neptune_volume' ),
[ ] ],

    'pluto_mass' : [
'constants', 'returns the mass of the planet Pluto',
'''
Yes, I still count Pluto as a planet.
''',
'''
''' + makeCommandExample( 'pluto_mass' ),
[ ] ],

    'pluto_radius' : [
'constants', 'returns the radius of the planet Pluto',
'''
Yes, I still count Pluto as a planet.
''',
'''
''' + makeCommandExample( 'pluto_radius' ),
[ ] ],

    'pluto_revolution' : [
'constants', 'returns the revolution time of the planet Pluto around the Sun',
'''
Yes, I still count Pluto as a planet.
''',
'''
''' + makeCommandExample( 'pluto_revolution' ),
[ ] ],

    'pluto_volume' : [
'constants', 'returns the volume of the planet Pluto',
'''
Yes, I still count Pluto as a planet.
''',
'''
''' + makeCommandExample( 'pluto_volume' ),
[ ] ],


# //******************************************************************************
# //
# //  day of week name constants
# //
# //******************************************************************************

    'monday' : [
'constants', 'returns 1, which is the code for Monday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2018 1 3 1 nth_weekday' ) + '''
''' + makeCommandExample( '2018 january 3 monday nth_weekday' ),
[ 'sunday', 'tuesday' ] ],

    'tuesday' : [
'constants', 'returns 2, which is the code for Tuesday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2018 24 2 nth_weekday_of_year' ) + '''
''' + makeCommandExample( '2018 24 tuesday nth_weekday_of_year' ),
[ 'monday', 'wednesday' ] ],

    'wednesday' : [
'constants', 'returns 3, which is the code for Wednesday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1967 3 4 3 nth_weekday' ) + '''
''' + makeCommandExample( '1967 march 4 wednesday nth_weekday' ),
[ 'tuesday', 'thursday' ] ],

    'thursday' : [
'constants', 'returns 4, which is the code for Thursday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1973 8 -1 4 nth_weekday' ) + '''
''' + makeCommandExample( '1973 august -1 thursday nth_weekday' ),
[ 'wednesday', 'friday' ] ],

    'friday' : [
'constants', 'returns 5, which is the code for Friday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2001 43 5 nth_weekday_of_year' ) + '''
''' + makeCommandExample( '2001 43 friday nth_weekday_of_year' ),
[ 'thursday', 'saturday' ] ],

    'saturday' : [
'constants', 'returns 6, which is the code for Saturday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1981 8 6 nth_weekday_of_year' ) + '''
''' + makeCommandExample( '1981 8 saturday nth_weekday_of_year' ),
[ 'friday', 'sunday' ] ],

    'sunday' : [
'constants', 'returns 7, which is the code for Sunday',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1998 4 -2 7 nth_weekday' ) + '''
''' + makeCommandExample( '1998 april -2 sunday nth_weekday' ),
[ 'saturday', 'monday' ] ],


# //******************************************************************************
# //
# //  month name constants
# //
# //******************************************************************************

    'january' : [
'constants', 'returns 1, which is the code for January',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2015 1 3 1 nth_weekday' ) + '''
''' + makeCommandExample( '2015 january 3 monday nth_weekday' ),
[ 'december', 'february' ] ],

    'february' : [
'constants', 'returns 1, which is the code for February',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1921 2 1 4 nth_weekday' ) + '''
''' + makeCommandExample( '1921 february 1 thursday nth_weekday' ),
[ 'january', 'march' ] ],

    'march' : [
'constants', 'returns 1, which is the code for March',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1945 3 1 3 nth_weekday' ) + '''
''' + makeCommandExample( '1945 march 1 wednesday nth_weekday' ),
[ 'february', 'april' ] ],

    'april' : [
'constants', 'returns 1, which is the code for April',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2050 4 1 5 nth_weekday' ) + '''
''' + makeCommandExample( '2050 april 1 friday nth_weekday' ),
[ 'march', 'may' ] ],

    'may' : [
'constants', 'returns 1, which is the code for May',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1899 5 -3 7 nth_weekday' ) + '''
''' + makeCommandExample( '1899 may -3 sunday nth_weekday' ),
[ 'april', 'june' ] ],

    'june' : [
'constants', 'returns 1, which is the code for June',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2017 6 3 6 nth_weekday' ) + '''
''' + makeCommandExample( '2017 june 3 saturday nth_weekday' ),
[ 'may', 'july' ] ],

    'july' : [
'constants', 'returns 1, which is the code for July',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2100 7 1 1 nth_weekday' ) + '''
''' + makeCommandExample( '2100 july 1 monday nth_weekday' ),
[ 'june', 'august' ] ],

    'august' : [
'constants', 'returns 1, which is the code for August',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2017 8 4 2 nth_weekday' ) + '''
''' + makeCommandExample( '2017 august 4 tuesday nth_weekday' ),
[ 'july', 'september' ] ],

    'september' : [
'constants', 'returns 9, which is the code for September',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1987 9 2 5 nth_weekday' ) + '''
''' + makeCommandExample( '1987 september 2 friday nth_weekday' ),
[ 'august', 'october' ] ],

    'october' : [
'constants', 'returns 10, which is the code for October',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '1961 10 4 3 nth_weekday' ) + '''
''' + makeCommandExample( '1961 october 4 wednesday nth_weekday' ),
[ 'september', 'november' ] ],

    'november' : [
'constants', 'returns 11, which is the code for November',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2007 11 1 1 nth_weekday' ) + '''
''' + makeCommandExample( '2007 november 1 monday nth_weekday' ),
[ 'october', 'december' ] ],

    'december' : [
'constants', 'returns 12, which is the code for December',
'''
This is defined for convenience for use with date operators.
''',
'''
''' + makeCommandExample( '2000 12 5 7 nth_weekday' ) + '''
''' + makeCommandExample( '2000 december 5 sunday nth_weekday' ),
[ 'november', 'january' ] ],


# //******************************************************************************
# //
# //  conversion operators
# //
# //******************************************************************************

    'char' : [
'conversion', 'converts the value to a signed 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'uchar', 'short', 'long', 'integer' ] ],

    'convert' : [
'conversion', 'performs unit conversion',
'''
Unit conversion is a pretty extensive feature and needs some serious help
text.  Some day, I'll write it.  In the meantime, see 'help unit_conversion'.
''',
'''
''' + makeCommandExample( '10 miles km convert' ) + '''
''' + makeCommandExample( '2 gallons cups convert' ) + '''
''' + makeCommandExample( '3 cups 4 tablespoons + fluid_ounce convert' ) + '''
''' + makeCommandExample( '153 pounds grams convert' ) + '''
''' + makeCommandExample( '65 mph kph convert' ) + '''
''' + makeCommandExample( '60 miles hour / furlongs fortnight / convert' ) + '''
''' + makeCommandExample( '78 kg [ pound ounce ] convert' ) + '''
This conversions suffers from a minor rounding error I haven't been able to
fix yet:
''' + makeCommandExample( '150,000 seconds [ day hour minute second ] convert' ),
[ ] ],

    'dhms' : [
'conversion', 'shortcut for \'[ day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ day hour minute second ]
convert' in order to convert a time interval to days, hours, minutes and
seconds.
''',
'''
''' + makeCommandExample( 'sidereal_year dhms' ),
[ 'hms', 'ydhms' ] ],

    'dms' : [
'conversion', 'shortcut for \'[ degree arcminute arcsecond ] convert\'',
'''
This shortcut operator replaces having to type '[ degree arcminute arcsecond ]
convert' in order to convert an angle to degrees, arcminutes and arcseconds.
''',
'''
''' + makeCommandExample( 'pi 7 / radians dms' ),
[ ] ],

    'double' : [
'conversion', 'converts n to the representation of a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'pi double -x' ) + '''
''' + makeCommandExample( '-a20 0x400921fb54442d18 undouble' ),
[ 'undouble', 'float' ] ],

    'float' : [
'conversion', 'converts n to the representation of a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'pi float -x' ) + '''
''' + makeCommandExample( '0x40490fdb unfloat' ),
[ 'unfloat', 'double' ] ],

    'from_unix_time' : [
'conversion', 'converts Unix time (seconds since epoch) to a date-time format'
'''
''',
'''
''' + makeCommandExample( '1471461891 from_unix_time' ),
[ ] ],

    'hms' : [
'conversion', 'shortcut for \'[ hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ hour minute second ] convert'
in order to convert a time interval to hours, minutes and seconds.
''',
'''
''' + makeCommandExample( '8 microcenturies hms' ) + '''
''' + makeCommandExample( '15,625 seconds hms' ),
[ 'ydhms', 'dhms' ] ],

    'integer' : [
'conversion', 'converts the value to an signed k-bit integer',
'''
''',
'''
''',
[ 'uinteger', 'char', 'short', 'long' ] ],

    'invert_units' : [
'conversion', 'inverts the units and takes the reciprocal of the value'
'''
This operation returns an equivalent measurement with the units inverted from
the original operand.

The result is the same value, but in inverted units.  This is useful for turning
a result into something more intuitive and readable.
''',
'''
''' + makeCommandExample( '3 cups invert_units' ) + '''
''' + makeCommandExample( '40 mph invert_units' ),
[ ] ],

    'latlong_to_nac' : [
'conversion', '',
'''
''',
'''
''',
[ ] ],

    'long' : [
'conversion', 'converts the value to a signed 32-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'longlong', 'quadlong', 'ulong' ] ],

    'longlong' : [
'conversion', 'converts the value to a signed 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'long', 'ulonglong', 'quadlong', 'integer' ] ],

    'pack' : [
'conversion', 'packs an integer using a values list n and a list of bit fields k',
'''
''',
'''
''',
[ 'unpack' ] ],

    'short' : [
'conversion', 'converts the value to a signed 16-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'ushort', 'char', 'long', 'integer' ] ],

    'to_unix_time' : [
'conversion', 'converts from date-time list to Unix time (seconds since epoch)',
'''
''',
'''
''',
[ 'from_unix_time' ] ],

    'uchar' : [
'conversion', 'converts the value to an unsigned 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'char', 'ushort', 'ulong', 'uinteger' ] ],

    'uinteger' : [
'conversion', 'converts the value to an unsigned k-bit integer',
'''
''',
'''
''',
[ 'integer', 'uchar', 'ushort', 'ulong' ] ],

    'ulong' : [
'conversion', 'converts the value to an unsigned 32-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'long', 'ulonglong', 'uquadlong', 'uinteger' ] ],

    'ulonglong' : [
'conversion', 'converts the value to an unsigned 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''',
[ 'ulong', 'longlong', 'uquadlong', 'uinteger' ] ],

    'undouble' : [
'conversion', 'interprets a 64-bit integer as a 64-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'pi double -x' ) + '''
''' + makeCommandExample( '-a20 0x400921fb54442d18 undouble' ),
[ 'double', 'unfloat' ] ],

    'unfloat' : [
'conversion', 'interprets a 32-bit integer as a 32-bit IEEE 754 float',
'''
For all IEEE 754 floating point numbers, rpn assumed big-endian byte ordering.
''',
'''
''' + makeCommandExample( 'pi float -x' ) + '''
''' + makeCommandExample( '0x40490fdb unfloat' ),
[ 'float', 'undouble' ] ],

    'unpack' : [
'conversion', 'unpacks an integer value n into bit fields k',
'''
''',
'''
''',
[ 'pack' ] ],

    'ushort' : [
'conversion', 'converts the value to an unsigned 16-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '10 ushort' ) + '''
''' + makeCommandExample( '100000 ushort' ) + '''
''' + makeCommandExample( '-2000 ushort' ),
[ 'short', 'uchar', 'ulong', 'uinteger' ] ],

    'ydhms' : [
'conversion', 'shortcut for \'[ year day hour minute second ] convert\'',
'''
This shortcut operator replaces having to type '[ year day hour minute
second ] convert' in order to convert a time interval to days, hours, minutes
and seconds.
''',
'''
''' + makeCommandExample( '1 billion seconds ydhms' ),
[ 'hms', 'dhms' ] ],


# //******************************************************************************
# //
# //  date_time operators
# //
# //******************************************************************************

    'iso_day' : [
'date_time', 'returns the ISO day and week for a date-time value',
'''
''',
'''
''',
[ ] ],


    'get_day' : [
'date_time', 'returns the day value of a date-time',
'''
''',
'''
''',
[ ] ],

    'get_hour' : [
'date_time', 'returns the hour value of a date-time',
'''
''',
'''
''',
[ ] ],

    'get_minute' : [
'date_time', 'returns the minute value of a date-time',
'''
''',
'''
''',
[ ] ],

    'get_month' : [
'date_time', 'returns the month value of a date-time',
'''
''',
'''
''',
[ ] ],

    'get_second' : [
'date_time', 'returns the second value of a date-time',
'''
''',
'''
''',
[ ] ],

    'get_year' : [
'date_time', 'returns the year value of a date-time',
'''
''',
'''
''',
[ ] ],

    'make_datetime' : [
'date_time', 'interpret argument as absolute date-time',
'''
''',
'''
''',
[ ] ],

    'make_iso_time' : [
'date_time', 'interpret argument as absolute date-time specified in the ISO format',
'''
''',
'''
''',
[ ] ],

    'make_julian_time' : [
'date_time', 'interpret argument as absolute date-time specified by year, Julian day and optional time of day',
'''
''',
'''
''',
[ ] ],

    'now' : [
'date_time', 'returns the current date-time',
'''
''',
'''
''',
[ ] ],

    'today' : [
'date_time', 'returns the current date',
'''
''',
'''
''',
[ ] ],

    'tomorrow' : [
'date_time', 'returns the next date',
'''
''',
'''
''',
[ ] ],

    'yesterday' : [
'date_time', 'returns the previous date',
'''
''',
'''
''',
[ ] ],


# //******************************************************************************
# //
# //  function operators
# //
# //******************************************************************************

    'break_on' : [
'functions', '',
'''
''',
'''
''',
[ 'filter', 'filter_by_index', 'lambda', 'unfilter' ] ],


    'eval' : [
'functions', 'evaluates the function n for the given argument k',
'''
'eval' is the simplest operator for user-defined functions.  It just plugs
in the value n into the one-argument function k and returns the result.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( '1 10 range lambda x 2 ** 1 - eval' ),
[ 'eval0', 'eval2', 'eval3', 'filter', 'lambda', 'recurrence', 'function' ] ],

    'eval0' : [
'functions', 'evaluates the zero-argument function n',
'''
''',
'''
''',
[ 'eval', 'eval2', 'eval3', 'filter', 'lambda', 'recurrence', 'function' ] ],

    'eval2' : [
'functions', 'evaluates the function c for the given arguments a and b',
'''
'eval2' is the simplest operator for user-defined functions with 2 variables.
It just plugs in the values a and b into the function c and returns the
result.
''',
'''
''',
[ 'eval', 'eval3', 'filter', 'lambda', 'recurrence', 'function' ] ],

    'eval3' : [
'functions', 'evaluates the function d for the given arguments a, b, and c',
'''
'eval3' is the simplest operator for user-defined functions with 3 variables.
It just plugs in the values a, b, and c into the function d and returns the
result.
''',
'''
Solving a quadratic equation the hard way, using the quadratic formula:

''' + makeCommandExample( '1 -4 -21 lambda y neg y sqr 4 x * z * - sqrt + 2 x * / eval3' ) + '''
''' + makeCommandExample( '1 -4 -21 lambda y neg y sqr 4 x * z * - sqrt - 2 x * / eval3' ) + '''
Of course, rpn has better ways to do this:
''' + makeCommandExample( '1 -4 -21 solve2' ) + '''
''' + makeCommandExample( '[ 1 -4 -21 ] solve' ),
[ 'eval', 'eval3', 'filter', 'lambda', 'recurrence', 'function' ] ],

    'eval_list' : [
'functions', 'evaluates the function n for the given list argument[s] k',
'''
''',
'''
''',
[ 'eval', 'eval_list2', 'eval_list3', 'lambda' ] ],

    'eval_list2' : [
'functions', 'evaluates the function n for the given list argument[s] k',
'''
''',
'''
''',
[ 'eval', 'eval_list', 'eval_list3', 'lambda' ] ],

    'eval_list3' : [
'functions', 'evaluates the function n for the given list argument[s] k',
'''
''',
'''
''',
[ 'eval', 'eval_list', 'eval_list2', 'lambda' ] ],

    'filter' : [
'functions', 'filters a list n using function k',
'''
The function is applied to each element of the list and a new list is returned
which consists only of those elements for which the function returned a
non-zero value.
''',
'''
Which of the first 80 fibonacci numbers is prime?

''' + makeCommandExample( '-a20 1 80 range fib lambda x is_prime filter' ),
[ 'break_on', 'filter_by_index', 'lambda', 'unfilter' ] ],

    'filter_by_index' : [
'functions', 'filters a list n using function k applied to the list indexes',
'''
''',
'''
''',
[ 'filter', 'lambda', 'unfilter_by_index' ] ],

    'filter_list' : [
'functions', '',
'''
''',
'''
''',
[ 'filter' ] ],

    'for_each' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list of arguments'
'''
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 7 9 ] [ 4 3 ] ] lambda x y power for_each' ),
[ 'for_each_list', 'repeat' ] ],

    'for_each_list' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list argument',
'''
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 6 7 ] [ 8 9 ] ] lambda x -1 element for_each_list' ) + '''
''' + makeCommandExample( '[ [ 1 2 ] [ 3 4 ] [ 5 6 ] [ 7 8 ] ] lambda x sum for_each_list' ),
[ 'for_each', 'repeat' ] ],

    'function': [
'functions', 'creates a user-defined function k named n',
'''
Functions are invoked by name, prefixed with '@'.
''',
'''
''' + makeCommandExample( 'test_function lambda x 4 ** function' ) + '''
''' + makeCommandExample( '1 10 range @test_function' ),
[ 'eval', 'eval2', 'eval3', 'filter', 'lambda', 'recurrence' ] ],

    'lambda' : [
'functions', 'begins a function definition',
'''
Allows the user to define a function for use with the eval, nsum, nprod,
and limit operators, etc.  Basically 'lambda' starts an expression that
becomes a function.

See the 'user_functions' help topic for more details.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( 'inf lambda x 1 + fib x fib / limit' ),
[ 'eval', 'functions', 'limit', 'nsum', 'nprod' ] ],

    'limit' : [
'functions', 'calculates the limit of function k( x ) as x approaches n',
'''
''',
'''
''' + makeCommandExample( 'inf lambda x 1 + fib x fib / limit' ),
[ 'limitn', 'lambda' ] ],

    'limitn' : [
'functions', 'calculates the limit of function k( x ) as x approaches n from above',
'''
''',
'''
''',
[ 'limit', 'lamdba' ] ],

    'nprod' : [
'functions', 'calculates the product of function c over the range of a through b',
'''
''',
'''
''',
[ 'nsum', 'lambda' ] ],

    'nsum' : [
'functions', 'calculates the sum of function c over the range of a through b',
'''
''',
'''
''',
[ 'nprod', 'lambda' ] ],

    'plot' : [
'functions', 'plot function c for values of x between a and b',
'''
'plot' is very much considered experimental.  It's easy to construct an
incompletely-defined function and cause mpmath to go into an infinite loop.

I suppose I need to make my function evaluation logic smarter.   That would
also allow me to plot more than one function at a time.

'plot' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
c:\>rpn 0 pi lambda x sin plot

c:\>rpn -5 5 lambda x 4 ** 3 x 3 ** * + 25 x * - plot

c:\>rpn 1 50 lambda x fib plot

c:\>rpn 1 10 lambda x 1 + fib x fib / plot

''',
[ 'plot2', 'lambda', 'plotc' ] ],

    'plot2' : [
'functions', 'plot a 3D function '
'''
'plot2' is very much considered experimental.

Here's an example to try:

c:\>rpn -2 2 -2 2 lambda x 2 ** y 2 ** - plot2

'plot2' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
''',
[ 'plot', 'lamdba', 'plotc' ] ],

    'plotc' : [
'functions', 'plot a complex function e for values of x between a and b real, c and d imaginary',
'''
'plotc' is very much considered experimental.

'plotc' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
''',
[ 'plot', 'plot2', 'lambda' ] ],

    'recurrence' : [
'functions', 'evaluates the function c, b times, starting with a and using the result of each previous function call as an argument for the next',
'''
This feature only works with one-argument functions."
''',
'''
''',
[ 'eval', 'filter', 'lambda' ] ],

    'repeat' : [
'functions', 'evaluates a 0-arg function n, k times',
'''
''',
'''
''',
[ 'eval0', 'eval', 'filter', 'lambda' ] ],

    'unfilter' : [
'functions', 'filters a list n using the inverse of function k',
'''
The function is applied to each element of the list and a new list is returned
which consists only of those elements for which the function returns a zero
value.
''',
'''
'unfilter' is the same as adding 'not' to 'filter':

''' + makeCommandExample( '1 20 range lambda x is_prime unfilter' ) + '''
''' + makeCommandExample( '1 20 range lambda x is_prime not filter' ),
[ 'filter', 'unfilter_by_index', 'lamdba' ] ],

    'unfilter_by_index' : [
'functions', 'filters a list n using the inverse of function k applied to the list indexes',
'''
''',
'''
''',
[ 'filter_by_index', 'unfilter', 'lamdba' ] ],

    'x' : [
'functions', 'used as a variable in user-defined functions',
'''
See the 'user_functions' help topic for more details.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( '1 inf lambda 1 2 x ** / nsum' ),
[ 'lamdba', 'y', 'z' ] ],

    'y' : [
'functions', 'used as a variable in user-defined functions',
'''
''',
'''
''',
[ 'lamdba', 'x', 'z' ] ],

    'z' : [
'functions', 'used as a variable in user-defined functions',
'''
''',
'''
''',
[ 'lamdba', 'x', 'y' ] ],


# //******************************************************************************
# //
# //  geometry operators
# //
# //******************************************************************************

    'antiprism_area' : [
'geometry', 'calculates the surface area of an n-sided antiprism of edge length k',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_area', 'tetrahedron_area', 'octohedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'antiprism_volume' : [
'geometry', 'calculates the volume of an n-sided antiprism of edge length k',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_volume', 'tetrahedron_volume', 'octohedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'cone_area' : [
'geometry', 'calculates the surface area of a cone of radius n and height k',
'''
''',
'''
''',
[ 'torus_area', 'sphere_area', 'prism_area', 'k_sphere_area', 'cone_volume' ] ],

    'cone_volume' : [
'geometry', 'calculates the volume of a cone of radius n and height k',
'''
''',
'''
''',
[ 'torus_volume', 'sphere_volume', 'prism_volume', 'k_sphere_volume', 'cone_area' ] ],

    'dodecahedron_area' : [
'geometry', 'calculates the surface area of a regular dodecahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octohedron_area', 'dodecahedron_volume', 'icosahedron_area', 'sphere_area' ] ],

    'dodecahedron_volume' : [
'geometry', 'calculates the volume of a regular dodecahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octohedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'hypotenuse' : [
'geometry', 'calculates the hypotenuse of n and k',
'''
Given a right triangle with sides of n and k, the 'hypotenuse' operator
calculates what the length of the hypotenuse would be.
''',
'''
''' + makeCommandExample( '3 4 hypotenuse' ) + '''
''' + makeCommandExample( '7 24 hypotenuse' ) + '''
''' + makeCommandExample( '1 1 hypotenuse' ),
[ ] ],

    'icosahedron_area' : [
'geometry', 'calculates the surface area of a regular icosahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octohedron_area', 'dodecahedron_area', 'icosahedron_volume', 'sphere_area' ] ],

    'icosahedron_volume' : [
'geometry', 'calculates the volume of a regular icosahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octohedron_volume', 'dodecahedron_volume', 'icosahedron_area', 'sphere_volume' ] ],

    'k_sphere_area' : [
'geometry', 'calculates the surface area of an n-sphere of size k (radius or volume)',
'''
''',
'''
''',
[ 'torus_area', 'sphere_volume', 'prism_area', 'k_sphere_area', 'cone_area', 'k_sphere_radius' ] ],

    'k_sphere_radius' : [
'geometry', 'calculates the radius of an n-sphere of size k (surface area or volume)',
'''
''',
'''
''',
[ 'k_sphere_volume', 'sphere_radius', 'k_sphere_area' ] ],

    'k_sphere_volume' : [
'geometry', 'calculates the volume of an n-sphere of size k (radius or surface area)',
'''
''',
'''
''',
[ 'torus_volume', 'sphere_volume', 'prism_volume', 'k_sphere_area', 'cone_volume', 'k_sphere_radius' ] ],

    'octahedron_area' : [
'geometry', 'calculates the surface area of a regular octahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octohedron_volume', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'octahedron_volume' : [
'geometry', 'calculates the volume of a regular octahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octohedron_area', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'polygon_area' : [
'geometry', 'calculates the area of an regular n-sided polygon with sides of length k',
'''
''',
'''
''',
[ 'triangle_area' ] ],

    'prism_area' : [
'geometry', 'calculates the surface area of an a-sided prism of edge length b, and height c',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_area', 'tetrahedron_area', 'octohedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'prism_volume' : [
'geometry', 'calculates the volume of an a-sided prism of edge length b, and height c',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_area', 'tetrahedron_volume', 'octohedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'sphere_area' : [
'geometry', 'calculates the surface area of a sphere of size n (radius or volume)',
'''
''',
'''
''',
[ 'torus_area', 'sphere_volume', 'prism_area', 'k_sphere_area', 'cone_area', 'sphere_radius' ] ],

    'sphere_radius' : [
'geometry', 'calculates the radius of a sphere of size n (surface area or volume)',
'''
''',
'''
''',
[ 'sphere_volume', 'sphere_radius', 'k_sphere_radius' ] ],

    'sphere_volume' : [
'geometry', 'calculates the volume of a sphere of size n (radius or surface area)',
'''
''',
'''
''',
[ 'torus_volume', 'sphere_area', 'prism_volume', 'k_sphere_volume', 'cone_volume', 'sphere_radius' ] ],

    'tetrahedron_area' : [
'geometry', 'calculates the surface area of a regular tetrahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_volume', 'octohedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'tetrahedron_volume' : [
'geometry', 'calculates the volume of a regular tetrahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_area', 'octohedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'torus_area' : [
'geometry', 'calculates the surface area of a torus of major radius n and minor radius k',
'''
''',
'''
''',
[ 'torus_volume', 'sphere_area', 'prism_area', 'k_sphere_area', 'cone_area' ] ],

    'torus_volume' : [
'geometry', 'calculates the volume of a torus of major radius n and minor radius k',
'''
''',
'''
''',
[ 'torus_area', 'sphere_volume', 'prism_volume', 'k_sphere_volume', 'cone_volume' ] ],

    'triangle_area' : [
'geometry', 'calculates the area of a triangle with sides of length a, b, and c',
'''
This operator uses Heron's formula, which takes the square root of the product
of the semiperimeter and the respective differences of the semiperimeter and
the lengths of each side.

area = sqrt( s( s - a )( s - b )( s - c ) )

This operator can also handle length measurements.
''',
'''
''' + makeCommandExample( '3 4 5 triangle_area' ) + '''
''' + makeCommandExample( '3 inches 4 inches 5 inches triangle_area' ) + '''
''' + makeCommandExample( '2 3 make_pyth_3 unlist triangle_area' ),
[ 'polygon_area', 'prism_area' ] ],


# //******************************************************************************
# //
# //  geography operators
# //
# //******************************************************************************

    'geo_distance' : [
'geography', 'calculates the distance, along the Earth\'s surface, of two locations',
'''
''',
'''
''',
[ 'location', 'lat_long' ] ],

    'get_timezone' : [
'geography', 'returns the timezone for location n',
'''
''',
'''
''',
[ 'location_info' ] ],

    'lat_long' : [
'geography', 'creates a location object given the lat/long for use with other operators',
'''
''',
'''
''',
[ 'location_info', 'location', 'geo_distance' ] ],

    'location' : [
'geography', 'returns the lat-long for a location string',
'''
''',
'''
''',
[ 'location_info', 'lat_long', 'geo_distance' ] ],

    'location_info' : [
'geography', 'returns the lat-long for a location',
'''
''',
'''
''',
[ 'location', 'lat_long', 'geo_distance', 'get_timezone' ] ],


# //******************************************************************************
# //
# //  internal operators
# //
# //******************************************************************************

    '_dump_aliases' : [
'internal', 'dumps the list of aliases for operators',
'''
rpn maintains a list of aliases for operators and units.  As of 7.0.0, there
are over 7000 aliases.  A lot of these are automatically generated for
metric unit types and certain compound units.  The rest are manually defined
aliases for units and operator names.

The operator returns number of aliases.
''',
'''
''',
[ '_dump_operators', '_stats', '_dump_units', '_dump_constants' ] ],

    '_dump_constants' : [
'internal', 'dumps the list of constants',
'''
The operator returns number of constants.
''',
'''
''',
[ '_dump_operators', '_stats', '_dump_units', '_dump_aliases' ] ],

    '_dump_operators' : [
'internal', 'lists all rpn operators',
'''
The list of operators is divided into normal operators, list operators (which
require at least one list argument), modifier operators (which work outside of
the RPN syntax), and internal operators, which describe RPN itself.

The operator returns number of operators.
''',
'''
''',
[ '_dump_aliases', '_stats', '_dump_units', '_dump_constants' ] ],

    '_dump_units' : [
'internal', 'lists all rpn units',
'''
The operator returns number of units.
''',
'''
''',
[ '_dump_aliases', '_dump_operators', '_stats', '_dump_constants' ] ],

    '_stats' : [
'internal', 'dumps rpn statistics',
'''
This operator returns the count of unique operators, the count of unit
convesions, the count of indexed prime numbers of each type, the index of the
highest prime number and the value of the highest prime number.

The operator returns the RPN version number in list format.
''',
'''
''',
[ '_dump_aliases', '_dump_operators', '_dump_units', '_dump_constants' ] ],


# //******************************************************************************
# //
# //  lexicographic operators
# //
# //******************************************************************************

    'add_digits' : [
'lexicography', 'adds the digits of k to n',
'''
The individual digits are combined lexicographically to produce a number that
is the equivalent of the concatenation of digits from each argument.
''',
'''
''' + makeCommandExample( '34 45 add_digits' ) + '''
''' + makeCommandExample( '12345 67890 add_digits' ) + '''
''',
[ 'build_numbers', 'combine_digits', 'duplicate_digits', 'duplicate_number', 'get_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

    'build_numbers' : [
'lexicography', 'constructs numbers lexicographically using a simple language',
'''
The simple language used to build numbers is similar to regular expressions
where the result is any permutation of digits that matches the pattern.

The expression consists of one or more digit expressions, each of which
describes the possible values for each digit in the resulting number.

The resulting numbers are presented in numeric order.

Digit expressions include:
    '0' through '9':  literal digits

    'd':              all digits, the equivalent of "[0-9]"

    'e':              even digits, the equivalent of "[24680]"

    'o':              odd digits, the equivalent of "[13579]"

    [I[I]...]:        a set of possible values for digits where I is a
                      literal digit or a range, which is specified by
                      two separate digits with a '-' in between

    [I[I]...:m]:      a set of possible values, as above, but for m digits,
                      not just one

    [I[I]...:n:m]:    all permutations of digits from a minimum of n digits
                      to a maximum of m digits

Please note that 'd', 'e', and 'o' can occur in a digit set (i.e., inside
brackets).  Also note that 'e' by itself is interpreted as the number e (i.e.,
Euler's number).  'o' by itself is interpreted as the symbol for 'abohm'.
''',
'''
''' + makeCommandExample( '[1248] build_numbers' ) + '''
''' + makeCommandExample( '[e] build_numbers' ) + '''
''' + makeCommandExample( '[e7] build_numbers' ) + '''
''' + makeCommandExample( '[o] build_numbers' ) + '''
''' + makeCommandExample( '[1-37-9] build_numbers' ) + '''
''' + makeCommandExample( '[1-367-9] build_numbers' ) + '''
''' + makeCommandExample( '2[1-4]5 build_numbers' ) + '''
''' + makeCommandExample( '[1-3][4-6] build_numbers' ) + '''
''' + makeCommandExample( '[1-5:2] build_numbers' ) + '''
''' + makeCommandExample( '[1-4:2:3] build_numbers' ) + '''
''' + makeCommandExample( '[1-4:1:2]e build_numbers' ) + '''
''',
[ ] ],

    'build_step_numbers' : [
'list_operators', 'builds all step numbers up to n digits in length',
'''
I have to admit, this operator was only created in a failed attempt to solve
the Euler Project Problem #178.
''',
'''
''',
[ 'is_step_number' ] ],

    'combine_digits' : [
'lexicography', 'combines the digits of all elements of list n into a single number',
'''
The individual digits are combined lexicographically to produce a number that
is the equivalent of the concatenation of digits from each item in the argument
list.

This function is the "list version" of 'add_digits'.  It does the same thing as
'add_digits', but with a list of arguments instead of two arguments.
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] combine_digits' ) + '''
''' + makeCommandExample( '9 0 range combine_digits' ) + '''
''' + makeCommandExample( '1 1 7 range primes combine_digits' ),
[ ] ],

    'count_digits' : [
'lexicography', 'counts the occurrences in n of all digits in k',
'''
''',
'''
''' + makeCommandExample( '1222333456 1 count_digits' ) + '''
''' + makeCommandExample( '1222333456 23 count_digits' ),
[ 'count_different_digits', 'digits', 'has_digits', 'has_any_digits', 'has_only_digits' ] ],

    'count_different_digits' : [
'lexicography', 'counts the number of different digits in n',
'''
''',
'''
''' + makeCommandExample( '1222333456 count_different_digits' ) + '''
''' + makeCommandExample( '7575577755 count_different_digits' ),
[ 'count_digits', 'has_digits', 'has_only_digits' ] ],

    'cyclic_permutations' : [
'lexicography', 'returns a list of all cyclic permutations of n',
'''
''',
'''
All of the circular primes up to a million:
''' + makeCommandExample( '[1379:1:6] build_numbers lambda x cyclic_permutations is_prime and_all filter [ 2 5 ] append sort' ),
[ 'rotate_left', 'rotate_right' ] ],

    'digits' : [
'lexicography', 'counts the number of digits in an integer',
'''
''',
'''
''' + makeCommandExample( '1222333456 digits' ) + '''
''' + makeCommandExample( '10 digits' ),
[ 'count_digits', 'has_digits', 'has_any_digits', 'has_only_digits' ] ],

    'duplicate_digits' : [
'lexicography', 'append n with a copy of its last k digits',
'''
''',
'''
''',
[ 'add_digits', 'combine_digits', 'duplicate_number' ] ],

    'duplicate_number' : [
'lexicography', 'return a number with the digits of n duplicated k times',
'''
''',
'''
''',
[ 'add_digits', 'combine_digits', 'duplicate_dugits' ] ],

    'erdos_persistence' : [
'lexicography', 'counts the Erdos version of multiplicative persistence for n',
'''
Erdos' version of multiplicative persistence is like Gardner's, but when
multiplying digits, zeroes are dropped, which makes it more interesting.
''',
'''
''',
[ ] ],

    'find_palindrome' : [
'lexicography', 'adds the reverse of n to itself up to k successive times to find a palindrome',
'''
''',
'''
''' + makeCommandExample( '-a30 10911 55 find_palindrome' ),
[ ] ],

    'get_base_k_digits' : [
'lexicography', 'returns the list of digits comprising integer n in base k',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''' + makeCommandExample( '1 million 2 10 range get_base_k_digits -s1' ),
[ 'get_nonzero_digits', 'get_nonzero_base_k_digits' ] ],

    'get_digits' : [
'lexicography', 'returns the list of digits comprising integer n',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''',
[ 'digits', 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_left_digits', 'get_right_digits', 'rotate_digits_left', 'rotate_digits_right' ] ],

    'get_left_digits' : [
'lexicography', 'returns a number composed of the left k digits of n',
'''
''',
'''
''' + makeCommandExample( '1234567890 5 get_left_digits' ) + '''
''' + makeCommandExample( '1000001 4 get_left_digits' ),
[ 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_digits', 'get_right_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

    'get_left_truncations' : [
'lexicography', 'returns the blah blah blah',
'''
''',
'''
''',
[ 'count_digits', 'digits', 'get_right_truncations', 'has_only_digits' ] ],

    'get_nonzero_base_k_digits' : [
'lexicography', 'returns the list of non-zero digits comprising integer n in base k',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''' + makeCommandExample( '1 million 2 10 range get_nonzero_base_k_digits -s1' ),
[ 'get_nonzero_digits', 'get_base_k_digits' ] ],

    'get_nonzero_digits' : [
'lexicography', 'returns the list of non-zero digits comprising integer n',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''' + makeCommandExample( '1 10 range get_nonzero_digits -s1' ),
[ 'get_digits', 'get_nonzero_base_k_digits' ] ],

    'get_right_digits' : [
'lexicography', 'returns a number composed of the right k digits of n',
'''
''',
'''
''' + makeCommandExample( '1234567890 5 get_right_digits' ) + '''
''' + makeCommandExample( '1000001 4 get_right_digits' ),
[ 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_left_digits', 'get_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

    'get_right_truncations' : [
'lexicography', 'returns the blah blah blah',
'''
''',
'''
''',
[ 'digits', 'get_left_truncations' ] ],

    'has_digits' : [
'lexicography', 'returns whether n contains all of the digits in k',
'''
''',
'''
''',
[ 'get_digits', 'has_only_digits' ] ],

    'has_any_digits' : [
'lexicography', 'returns whether n contains any of the digits in k',
'''
''',
'''
''',
[ 'count_different_digits', 'has_digits', 'get_digits', 'has_only_digits' ] ],

    'has_only_digits' : [
'lexicography', 'returns whether n contains all of the digits in k and no others',
'''
''',
'''
''',
[ 'get_digits', 'has_digits' ] ],

    'is_automorphic' : [
'lexicography', 'returns whether the digits of n squared end with n',
'''
''',
'''
''',
[ 'is_k_morphic', 'is_trimorphic' ] ],

    'is_base_k_pandigital' : [
'lexicography', '',
'''
''',
'''
''',
[ ] ],

    'is_base_k_smith_number' : [
'lexicography', 'returns whether n is a Smith Number in base k',
'''
A Smith number is a composite number for which the sum of its digits is equal
to the sum of the digits in its prime factorization.

https://en.wikipedia.org/wiki/Smith_number
''',
'''
''',
[ 'is_smith_number', 'is_order_k_smith_number' ] ],

    'is_bouncy' : [
'lexicography', 'returns whether an integer n is bouncy',
'''
''',
'''
''',
[ ] ],

    'is_decreasing' : [
'lexicography', 'returns whether an integer n is decreasing',
'''
''',
'''
''',
[ ] ],

    'is_digital_permutation' : [
'lexicography', 'returns whether k is a digital permutation of n',
'''
''',
'''
''',
[ ] ],

    'is_generalized_dudeney' : [
'lexicography', 'returns whether an integer n is a generalized Dudeney number',
'''
''',
'''
''',
[ ] ],

    'is_harshad' : [
'lexicography', 'returns whether an integer n is a Harshad number',
'''
''',
'''
''',
[ ] ],

    'is_increasing' : [
'lexicography', 'returns whether an integer n is increasing',
'''
''',
'''
''',
[ ] ],

    'is_kaprekar' : [
'lexicography', 'returns whether an integer n is a Kaprekar number in base k',
'''
''',
'''
''',
[ ] ],

    'is_k_morphic' : [
'lexicography', 'returns whether the digits of n to the k power end with n',
'''
''',
'''
''',
[ 'is_automorphic', 'is_trimorphic' ] ],

    'is_k_narcissistic' : [
'lexicography', 'returns whether an integer n is base-k narcissistic',
'''
''',
'''
''',
[ ] ],

    'is_narcissistic' : [
'lexicography', 'returns whether an integer n is narcissistic',
'''
''',
'''
''',
[ ] ],

    'is_order_k_smith_number' : [
'lexicography', 'returns whether n is am order-k Smith Number',
'''
An order-k Smith number is a composite number for which the sum of the kth
power of its digits is equal to the sum of the kth power of the digits of its
prime factorization.
''',
'''
''' + makeCommandExample( '1 1000 range lambda x 2 is_order_k_smith_number filter' ),
[ 'is_smith_number', 'is_base_k_smith_number' ] ],

    'is_palindrome' : [
'lexicography', 'returns whether an integer n is palindromic',
'''
n is treated as an integer.  If its digits are palindromic, i.e., they
read the same forwards as backwards, then the operator returns 1.
''',
'''
''' + makeCommandExample( '101 is_palindrome' ) + '''
''' + makeCommandExample( '1201 is_palindrome' ),
[ ] ],

    'is_pandigital' : [
'lexicography', 'returns whether an integer n is pandigital',
'''
A pandigital number contains at least one of all the of the digits 0 through
9.   If the number is smaller than 10 digits, then it is considered pandigital
if it contains all the digits from 1 to n, where n is the length of the string
in digits.
''',
'''
''' + makeCommandExample( '1234 is_pandigital' ) + '''
''' + makeCommandExample( '1274 is_pandigital' ) + '''
''' + makeCommandExample( '123456789 is_pandigital' ) + '''
''' + makeCommandExample( '1234567890 is_pandigital' ) + '''
''' + makeCommandExample( '-a30 [ 3 3 7 19 928163 1111211111 ] prod is_pandigital' ),
[ ] ],

    'is_pdi' : [
'lexicography', 'returns whether an integer n is a perfect digital invariant',
'''
''',
'''
''' + makeCommandExample( '370 is_pdi' ) + '''
''' + makeCommandExample( '371 is_pdi' ) + '''
''' + makeCommandExample( '1 1000 range lambda x is_pdi filter' ),
[ 'is_pdi' ] ],

    'is_pddi' : [
'lexicography', 'returns whether an integer n is a perfect digit-to-digti invariant for base k',
'''
''',
'''
''',
[ 'is_pdi' ] ],

    'is_step_number' : [
'list_operators', 'returns 1 if n is a step number else 0',
'''
''',
'''
''',
[ 'build_step_numbers' ] ],

    'is_sum_product' : [
'lexicography', 'returns whether an integer n is a sum-product number',
'''
''',
'''
''',
[ ] ],

    'is_smith_number' : [
'lexicography', 'returns whether n is a Smith Number',
'''
A Smith number is a composite number for which the sum of its digits is equal
to the sum of the digits in its prime factorization.
''',
'''
''',
[ 'is_base_k_smith_number', 'is_order_k_smith_number' ] ],

    'is_trimorphic' : [
'lexicography', 'returns whether the digits of n cubed end with n',
'''
''',
'''
''' + makeCommandExample( '9999 is_trimorphic' ) + '''
''' + makeCommandExample( '1 50 range is_trimorphic' ),
[ 'is_automorphic', 'is_trimorphic' ] ],

    'k_persistence' : [
'lexicography', 'counts the number of times it takes to successively multiply the digits of n to the kth power to get a one-digit number',
'''
''',
'''
''',
[ 'persistence', 'show_k_persistence', 'show_erdos_persistence' ] ],

    'multiply_digits' : [
'lexicography', 'calculates the product of the digits of integer n',
'''
''',
'''
''',
[ 'multiply_digit_powers', 'multiply_nonzero_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_digit_powers' : [
'lexicography', 'calculates the product of the kth power of each digit of integer n',
'''
''',
'''
''',
[ 'multiply_digits', 'multiply_nonzero_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_nonzero_digits' : [
'lexicography', 'calculates the product of the non-zero digits of integer n',
'''
''',
'''
''',
[ 'multiply_digit_powers', 'multiply_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_nonzero_digit_powers' : [
'lexicography', 'calculates the product of the kth power of each non-zero digit of integer n',
'''
''',
'''
''',
[ 'multiply_digits', 'multiply_nonzero_digits', 'multiply_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'permute_digits' : [
'lexicography', 'generates all values with lexicographic permutations of the digits of n',
'''
This operator takes the individual digits of n and returns a list of all
lexicographic permutations of the digits.
''',
'''
''' + makeCommandExample( '123 permute_digits' ) + '''
''' + makeCommandExample( '5567 permute_digits' ),
[ ] ],

    'persistence' : [
'lexicography', 'counts the number of times it takes to successively multiply the digits of n to get a one-digit number',
'''
This operator implements 'multiplicative persistence' as described by Martin
Gardner:

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.
''',
'''
''',
[ 'show_persistence', 'k_persistence', 'show_erdos_persistence' ] ],

    'replace_digits' : [
'lexicography', 'returns the blah blah blah',
'''
''',
'''
''',
[ ] ],

    'reversal_addition' : [
'lexicography', 'TODO: describe me',
'''
''',
'''
''' + makeCommandExample( '-a20 89 24 rev_add' ),
[ ] ],

    'reverse_digits' : [
'lexicography', 'returns n with its digits reversed',
'''
'reverse_digits' converts the argument to an integer.
''',
'''
''' + makeCommandExample( '123456789 reverse_digits' ),
[ ] ],

    'rotate_digits_left' : [
'lexicography', 'rotates the digits of n to the left by k digits',
'''
''',
'''
''',
[ ] ],

    'rotate_digits_right' : [
'lexicography', 'rotates the digits of n to the right by k digits',
'''
''',
'''
''',
[ ] ],

    'show_erdos_persistence' : [
'lexicography', 'shows the Erdos multiplicative persistence chain of n (see \'persistence\')'
'''
''',
'''
''',
[ 'persistence', 'show_persistence', 'show_k_persistence' ] ],

    'show_k_persistence' : [
'lexicography', 'shows the multiplicative persistence chain of n for k'
'''
''',
'''
''',
[ 'k_persistence', 'show_persistence', 'show_erdos_persistence' ] ],

    'show_persistence' : [
'lexicography', 'shows the multiplicative persistence chain of n'
'''
''',
'''
''',
[ 'persistence', 'show_k_persistence', 'show_erdos_persistence' ] ],

    'square_digit_chain' : [
'lexicography', '',
'''
''',
'''
''',
[ ] ],

    'sum_digits' : [
'lexicography', 'calculates the sum of the digits of integer n',
'''
''',
'''
''',
[ 'multiply_digits', 'get_digits' ] ],


# //******************************************************************************
# //
# //  logical operators
# //
# //******************************************************************************

    'and' : [
'logical', 'returns 1 if n and k are both nonzero',
'''
''',
'''
''' + makeCommandExample( '0 0 and' ) + '''
''' + makeCommandExample( '0 1 and' ) + '''
''' + makeCommandExample( '1 0 and' ) + '''
''' + makeCommandExample( '1 1 and' ) + '''
''',
[ 'or', 'nand' ] ],

    'nand' : [
'logical', 'returns 1 if n and k are both zero',
'''
''',
'''
''' + makeCommandExample( '0 0 nand' ) + '''
''' + makeCommandExample( '0 1 nand' ) + '''
''' + makeCommandExample( '1 0 nand' ) + '''
''' + makeCommandExample( '1 1 nand' ) + '''
''',
[ 'or', 'nand' ] ],

    'nor' : [
'logical', '',
'''
''',
'''
''' + makeCommandExample( '0 0 nor' ) + '''
''' + makeCommandExample( '0 1 nor' ) + '''
''' + makeCommandExample( '1 0 nor' ) + '''
''' + makeCommandExample( '1 1 nor' ) + '''
''',
[ 'or', 'nand' ] ],

    'not' : [
'logical', '',
'''
''',
'''
''' + makeCommandExample( '0 not' ) + '''
''' + makeCommandExample( '1 not' ) + '''
''',
[ 'or', 'nand' ] ],

    'or' : [
'logical', '',
'''
''',
'''
''' + makeCommandExample( '0 0 or' ) + '''
''' + makeCommandExample( '0 1 or' ) + '''
''' + makeCommandExample( '1 0 or' ) + '''
''' + makeCommandExample( '1 1 or' ) + '''
''',
[ 'nor', 'and' ] ],

    'xnor' : [
'logical', '',
'''
''',
'''
''' + makeCommandExample( '0 0 xnor' ) + '''
''' + makeCommandExample( '0 1 xnor' ) + '''
''' + makeCommandExample( '1 0 xnor' ) + '''
''' + makeCommandExample( '1 1 xnor' ) + '''
''',
[ 'xor' ] ],

    'xor' : [
'logical', '',
'''
''',
'''
''' + makeCommandExample( '0 0 xor' ) + '''
''' + makeCommandExample( '0 1 xor' ) + '''
''' + makeCommandExample( '1 0 xor' ) + '''
''' + makeCommandExample( '1 1 xor' ) + '''
''',
[ 'xnor' ] ],


# //******************************************************************************
# //
# //  list operators
# //
# //******************************************************************************

    'alternate_signs' : [
'list_operators', 'alternates signs in the list by making every even element negative',
'''
The return value is a list of the same size as the original with the sign of
every second element reversed, starting with the second.
''',
'''
''' + makeCommandExample( '1 10 range alternate_signs' ),
[ 'alternate_signs_2' ] ],

    'alternate_signs_2' : [
'list_operators', 'alternates signs in the list by making every odd element negative',
'''
The return value is a list of the same size as the original with the sign of
every other element reversed, starting with the first element.
''',
'''
''' + makeCommandExample( '1 10 range alternate_signs_2' ),
[ 'alternate_signs' ] ],

    'alternating_sum' : [
'list_operators', 'calculates the alternating sum of list n (addition first)',
'''
This operator calculates the sum of the list, alternating the signs of every
second element starting with the second.

This operator is the same as using 'alternate_signs sum'.
''',
'''
''' + makeCommandExample( '1 10 range alternate_signs sum' ) + '''
''' + makeCommandExample( '1 10 range alternating_sum' ) + '''
Calculating e:
''' + makeCommandExample( '-a20 0 25 range factorial 1/x alternating_sum 1/x' ),
[ 'alternating_sum_2' ] ],

    'alternating_sum_2' : [
'list_operators', 'calaculates the alternating sum of list n (subtraction first)',
'''
This operator calculates the sum of the list, alternating the signs of every
other element starting with the first.

This operator is the same as using 'alternate_signs_2 sum'.
''',
'''
''' + makeCommandExample( '1 10 range alternate_signs_2 sum' ) + '''
''' + makeCommandExample( '1 10 range alternating_sum_2 sum' ),
[ 'alternating_sum' ] ],

    'and_all' : [
'list_operators', 'returns true if every member of the list is non-zero',
'''
The operator performs a logical and on every member of the list.  The result is
a return value of 1 if the list elements are all non-zero, otherwise it returns
0.
''',
'''
''',
[ 'or_all', 'nand_all', 'nor_all' ] ],

    'append' : [
'list_operators', 'appends the second list on to the first list',
'''
This operator appends the second list of items to the first list resulting
in a single list containing all items in order from the first operand list and
then the second operand list.
''',
'''
''' + makeCommandExample( '1 5 range 6 10 range append' ),
[ 'union', 'intersection', 'permute_lists', 'interleave' ] ],

    'collate' : [
'list_operators', 'returns a list of n-element lists of corresponding elements from each sublist of n',
'''
''',
'''
''',
[ 'flatten', 'group_elements', 'interleave' ] ],

    'compare_lists' : [
'list_operators', 'compares lists n and k',
'''
'is_equal' is not a list operator, so it will only compare elements of two
lists up to the length of the shorter of the two lists.
''',
'''
''' + makeCommandExample( '[ 1 2 3 4 ] 1 4 range compare_lists' ) + '''
''' + makeCommandExample( '1 3 range 1 4 range compare_lists' ),
[ 'append' ] ],

    'count' : [
'list_operators', 'counts the elements of list n',
'''
This simply counts the number of elements in the list.
''',
'''
''' + makeCommandExample( '1 100 range count' ),
[ ] ],

    'cumulative_diffs' : [
'list_operators', 'returns a list with the differences between each element of list n with the first element',
'''
''',
'''
''',
[ 'diffs', 'ratios', 'cumulative_ratios' ] ],

    'cumulative_ratios' : [
'list_operators', 'returns a list with the ratios between each element of n and the first',
'''
This operator is analogous to the 'cumulative_diffs' operator.
''',
'''
''',
[ 'ratios', 'diffs', 'cumulative_diffs' ] ],

    'difference' : [
'list_operators', 'returns a list of unique elements in list k that are not found in list n',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 4 ] [ 3 4 5 ] difference' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] [ 4 5 6 ] difference' ) + '''
''' + makeCommandExample( '[ 1 1 2 3 3 3 ] [ 1 2 3 4 5 5 ] difference' ),
[ 'union', 'append', 'permute_lists', 'interleave' ] ],

    'diffs' : [
'list_operators', 'returns a list with the differences between successive elements of list n',
'''
''',
'''
''',
[ 'cumulative_diffs', 'ratios', 'cumulative_ratios' ] ],

    'element' : [
'list_operators', 'returns a single element from a list',
'''
The index is zero-based.
''',
'''
''' + makeCommandExample( '1 10 range 5 element' ) + '''
''' + makeCommandExample( '0 1000 range 34 element' ),
[ 'max_index', 'min_index' ] ],

    'enumerate' : [
'list_operators', 'numbers the items in list n starting with k',
'''
This operator returns a list of lists, where each sublist contains a
consecutive number, starting with k, and the original nth element of the list.
''',
'''
''' + makeCommandExample( '1 10 range 1 enumerate' ) + '''
''' + makeCommandExample( '20 30 range boiling_point 20 enumerate -s1' ),
[ ] ],

    'exponential_range' : [
'list_operators', 'generates a list of exponential progression of numbers',
'''
a = starting value, b = step exponent, c = size of list to generate

Each successive item in the list is calculated by raising the previous item to
the bth power.  The list is expanded to contain c items.
''',
'''
''' + makeCommandExample( '2 2 10 exponential_range' ),
[ 'range', 'geometric_range', 'interval_range', 'sized_range' ] ],

    'find' : [
'list_operators', 'returns the first index of k that equals n',
'''
''',
'''
This used to have the arguments swapped, but that seemed wrong.
''',
[ ] ],

    'flatten' : [
'list_operators', 'flattens a nested lists in list n to a single level',
'''
''',
'''
''',
[ 'collate', 'interleave', 'group_elements' ] ],

    'geometric_range' : [
'list_operators', 'generates a list of geometric progression of numbers',
'''
The list starts at a, and each successive value is multiplied by b, until the
list contains c items.
''',
'''
''' + makeCommandExample( '1 2 10 geometric_range' ) + '''
The intervals of the chromatic scale:
''' + makeCommandExample( '1 2 12 // 13 geometric_range' ),
[ 'exponential_range', 'range', 'interval_range', 'sized_range' ] ],

    'get_combinations' : [
'list_operators', 'generates all combinations of k members of list n',
'''
''',
'''
''',
[ 'get_permutations', 'get_repeat_combinations' ] ],

    'get_permutations' : [
'list_operators', 'generates all permutations of k members of list n',
'''
''',
'''
''',
[ 'get_combinations', 'get_repeat_permutations' ] ],

    'get_repeat_combinations' : [
'list_operators', 'generates all combinations of k members of list n, with repeats allowed',
'''
''',
'''
''',
[ 'get_permutations', 'get_combinations' ] ],

    'get_repeat_permutations' : [
'list_operators', 'generates all permutations of k members of list n, with repeats allowed',
'''
''',
'''
''',
[ 'get_permutations', 'get_repeat_combinations' ] ],

    'group_elements' : [
'list_operators', 'groups the elements of list n into sublsts of k elements',
'''
If there are elements left over (i.e., not enough to create the final group
of k elements, then the remaining list elements are included in the final
group.
''',
'''
''' + makeCommandExample( '1 10 range 5 group_elements' ) + '''
''' + makeCommandExample( '1 11 range 5 group_elements' ),
[ 'collate', 'flatten', 'interleave' ] ],

    'interleave' : [
'list_operators', 'interleaves lists n and k into a single list',
'''
Given an input of two lists, n and k 'interleave' returns a single list in which the
members of n and k are interleaved alternately.  If one list is longer than the other
then the extra list elements from the longer list are ignored.
''',
'''
''' + makeCommandExample( '[ 1 3 5 ] [ 2 4 6 ] interleave' ) + '''
''' + makeCommandExample( '[ 1 3 5 ] [ 2 4 6 8 10 ] interleave' ) + '''
''' + makeCommandExample( '1 20 2 range2 2 20 2 range2 interleave' ),
[ 'group_elements', 'collate', 'flatten' ] ],

    'intersection' : [
'list_operators', 'returns a list of unique elements that exist in both lists',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 4 ] [ 3 4 5 ] intersection' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] [ 4 5 6 ] intersection' ) + '''
''' + makeCommandExample( '[ 1 1 2 3 3 3 ] [ 1 2 3 4 5 5 ] intersection' ) + '''
''' + makeCommandExample( '1 10 range 1 10 range prime intersection' ) + '''
Find numbers that are triangular and square at the same time:
''' + makeCommandExample( '1 100 range tri 1 100 range sqr intersect' ),
[ 'union', 'append', 'permute_lists', 'interleave' ] ],

    'interval_range' : [
'list_operators', 'generates a list of arithmetic progression of numbers',
'''
a is the starting value, b is the ending value, c is the increment.

The generated list will contain every value up to, but not exceeding b.  If b
is not equal to a plus a multiple of c, then it will not appear in the list.
''',
'''
''' + makeCommandExample( '1 10 2 interval_range' ) + '''
''' + makeCommandExample( '100 90 -2 interval_range' ) + '''
''' + makeCommandExample( '1 10 1 10 range interval_range' ),
[ 'exponential_range', 'geometric_range', 'range', 'sized_range' ] ],

    'is_palindrome_list' : [
'list_operators', 'returns 1 if list n is a palindrome',
'''
''',
'''
''',
[ ] ],

    'left' : [
'list_operators', 'returns the left k items from list n',
'''
''',
'''
''' + makeCommandExample( '1 10 range 6 left' ) + '''
''' + makeCommandExample( '1 10 range 4 left' ) + '''
''' + makeCommandExample( '1 10 range 1 4 range left' ),
[ 'right', 'slice', 'sublist', 'random_element' ] ],

    'max_index' : [
'list_operators', 'returns the index of largest value in list n',
'''
''',
'''
''',
[ 'min_index', 'element' ] ],

    'min_index' : [
'list_operators', 'returns the index of smallest value in list n',
'''
''',
'''
''',
[ 'max_index', 'element' ] ],

    'nand_all' : [
'list_operators', 'returns true if every member of the list is zero',
'''
''',
'''
''',
[ 'nor_all', 'and_all', 'or_all' ] ],

    'nonzero' : [
'list_operators', 'returns the indices of elements of list n that are not zero',
'''
This operator is useful for applying an operator that returns a binary value
on a list, and getting a summary of the results.

Indices are zero-based.
''',
'''
''' + makeCommandExample( '[ 1 0 2 0 3 0 4 ] nonzero' ) + '''
List the prime Fibonacci numbers:
''' + makeCommandExample( '0 20 range fib is_prime nonzero fib' ),
[ 'zero' ] ],

    'nor_all' : [
'list_operators', 'returns true if any member of the list is zero',
'''
''',
'''
''',
[ 'and_all', 'or_all', 'nand_all' ] ],

    'occurrence_cumulative' : [
'list_operators', 'returns the cumulative ratio of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
ratio (out of 1.0), where each value is the cumulative ratio of that item and the
ones preceding it.  The result will be sorted by values.
''',
'''
''',
[ 'occurrence_ratios', 'occurrences' ] ],

    'occurrence_ratios' : [
'list_operators', 'returns the ratio of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
ratio (out of 1.0).  The result will be sorted by values.
''',
'''
''',
[ 'occurrence_cumulative', 'occurrences' ] ],

    'occurrences' : [
'list_operators', 'returns the number of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
count.  The result will be sorted by values.
''',
'''
''' + makeCommandExample( '1 10 range occurrences' ) + '''
''' + makeCommandExample( '10 100 random_integer_ occurrences' ) + '''
''' + makeCommandExample( '5 6 debruijn occurrences' ),
[ 'occurrence_cumulative', 'occurrence_ratios' ] ],

    'or_all' : [
'list_operators', 'returns true if any member of the list is non-zero',
'''
The operator performs a logical or on every member of the list.  The result is
a return value of 1 if any of the list elements is non-zero, otherwise it
returns 0.
''',
'''
''',
[ 'and_all', 'nor_all', 'nand_all' ] ],

    'permute_lists' : [
'list_operators', 'generates all permutations of the members of each list',
'''
This operator generates a list of permutations of the members of each sublist.

The operand must consist of a list of lists.  The output results will be a
sequence of lists where each list contains one element from each sublist of
the operand.  Every permutation of lists containing one item from each sublist
will be output.
''',
'''
''' + makeCommandExample( '[ 1 4 range 5 8 range ] permute_lists combine_digits' ) + '''
''' + makeCommandExample( '[ 1 4 range 5 8 range [ 1 3 5 ] ] permute_lists combine_digits' ) + '''
''' + makeCommandExample( '[ 1 5 primes 1 5 primes 1 5 primes ] permute_lists product sort' ),
[ 'append', 'interleave', 'intersection', 'union' ] ],

    'powerset' : [
'list_operators', 'generates the powerset of list n',
'''
I'm going to be honest.  I don't think including an empty list in the output
would ever be useful, so the operator leaves it out.
''',
'''
''',
[ ] ],

    'random_element' : [
'list_operators', 'returns a random element from list n',
'''
''',
'''
''' + makeCommandExample( '1 10 range random_element' ) + '''
''' + makeCommandExample( '[ 1 5 10 12 15 19 ] random_element' ) + '''
''' + makeCommandExample( '[ 1 4 range 5 8 range 9 12 range ] random_element' ),
[ 'shuffle', 'sublist', 'reverse', 'powerset' ] ],

    'range' : [
'list_operators', 'generates a list of successive integers from n to k',
'''
''',
'''
''',
[ 'exponential_range', 'geometric_range', 'interval_range', 'sized_range' ] ],

    'ratios' : [
'list_operators', 'returns a list with the ratios between successive elements of list n',
'''
This operator is analogous to the 'diffs' operator.
''',
'''
''',
[ 'cumulative_ratios', 'diffs', 'cumulative_diffs' ] ],

    'reduce' : [
'list_operators', 'reduces out the common factors from each element of a list',
'''
In other words, each element of the list is divided by the greatest common
denominator of the whole list.
''',
'''
''',
[ 'gcd' ] ],

    'reverse' : [
'list_operators', 'returns list n with its elements reversed',
'''
''',
'''
''',
[ 'shuffle', 'random_element' ] ],

    'right' : [
'list_operators', 'returns the right k items from list n',
'''
''',
'''
''' + makeCommandExample( '1 10 range 6 right' ) + '''
''' + makeCommandExample( '1 10 range 4 right' ) + '''
''' + makeCommandExample( '1 10 range 1 4 range right' ),
[ 'left', 'slice', 'sublist', 'random_element' ] ],

    'shuffle' : [
'list_operators', 'randomly shuffles the elements in a list',
'''
''',
'''
''' + makeCommandExample( '1 10 range shuffle' ),
[ 'reverse', 'random_element' ] ],

    'sized_range' : [
'list_operators', 'generates a list of arithmetic progression of numbers',
'''
The list starts at a, and each successive value is increased by b, until the
list contains c items.
''',
'''
''' + makeCommandExample( '1 2 10 sized_range' ) + '''
''' + makeCommandExample( '10 10 10 sized_range' ) + '''
''' + makeCommandExample( '1 1 5 range 5 sized_range' ),
[ 'exponential_range', 'geometric_range', 'interval_range', 'range' ] ],

    'slice' : [
'list_operators', 'returns a slice of list a from starting index b to ending index c',
'''
Indices are zero-based, and the ending index is not included in the slice.
This functionality echoes the Python slicing semantics.  As in Python, a
negative ending index represents counting backwards from the end of the list.

An ending index of 0 represents the end of the list.
''',
'''
''' + makeCommandExample( '1 10 range 0 5 slice' ) + '''
''' + makeCommandExample( '1 10 range 5 9 slice' ) + '''
''' + makeCommandExample( '1 10 range 2 0 slice' ) + '''
''' + makeCommandExample( '1 10 range 2 -1 slice' ) + '''
''' + makeCommandExample( '1 10 range 2 -2 slice' ),
[ 'right', 'left', 'sublist' ] ],

    'sort' : [
'list_operators', 'sorts the elements of list n numerically in ascending order',
'''
The 'sort' operator gets applied recursively, so all sublists will be sorted as
well.  I might have to reconsider that.
''',
'''
''' + makeCommandExample( '[ rand rand rand ] sort' ) + '''
''' + makeCommandExample( '[ [ 3 2 1 ] [ 7 3 4 ] [ 10 5 9 ] ]' ),
[ 'sort_descending' ] ],

    'sort_descending' : [
'list_operators', 'sorts the elements of list n numerically in descending order',
'''
The 'sort_descending' operator works exactly like the sort operator, sorting
the list (and all sublists), except in descending order.
''',
'''
''' + makeCommandExample( '1 70 6 range2 sort_descending' ) + '''
''' + makeCommandExample( '1 20 range count_divisors sort_descending' ),
[ 'sort' ] ],

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
''' + makeCommandExample( '1 10 range 0 5 sublist' ) + '''
''' + makeCommandExample( '1 10 range 1 5 sublist' ) + '''
''' + makeCommandExample( '1 10 range 1 3 sublist' ),
[ 'right', 'left', 'slice' ] ],

    'union' : [
'list_operators', 'returns the union of unique elements from two lists',
'''
''',
'''
''',
[ 'intersection', 'append', 'permute_lists', 'interleave' ] ],

    'unique' : [
'list_operators', 'returns a list of its unique elements',
'''
''',
'''
''' + makeCommandExample( '1 8 range 2 9 range append 3 10 range append unique' ),
[ ] ],

    'zero' : [
'list_operators', 'returns a list of the indices of elements in list n that are zero',
'''
This operator is useful for applying an operator that returns a binary value
on a list, and getting a summary of the results.

Indices are zero-based.

(see 'nonzero')
''',
'''
''' + makeCommandExample( '[ 1 0 2 0 3 0 4 ] zero' ) + '''
List the non-prime Fibonacci numbers:
''' + makeCommandExample( '0 20 range fib is_prime zero fib' ),
[ ] ],


# //******************************************************************************
# //
# //  logarithm operators
# //
# //******************************************************************************

    'lambertw' : [
'logarithms', '',
'''
''',
'''
''',
[ ] ],

    'li' : [
'logarithms', 'calculates the logarithmic interval of n',
'''
''',
'''
''',
[ ] ],

    'log' : [
'logarithms', 'calculates the natural logarithm of n',
'''
''',
'''
''',
[ 'log10', 'exp', 'polylog', 'log2', 'exp10', 'logxy' ] ],

    'log10' : [
'logarithms', 'calculates the base-10 logarithm of n',
'''
The base-10 logarithm of n is the power to which 10 is raised to get the number
n.
''',
'''
''' + makeCommandExample( '10 log10' ) + '''
''' + makeCommandExample( '3221 log10' ) + '''
''' + makeCommandExample( '10 3221 log10 1481 log10 + power' ),
[ 'log', 'logxy', 'log2', 'exp', 'exp10' ] ],

    'log2' : [
'logarithms', 'calculates the base-2 logarithm of n',
'''
The base-2 logarithm of n is the power to which 2 is raised to get the number
n.

The base-2 logarithm also calculates the number of bits necessary to store n
different values.
''',
'''
''' + makeCommandExample( '8 log2' ) + '''
''' + makeCommandExample( '65536 log2' ),
[ 'log', 'log10', 'logxy', 'exp', 'exp10' ] ],

    'logxy' : [
'logarithms', 'calculates the base-k logarithm of n',
'''
The base-k logarithm of n is the power to which k is raised to get the number
n.
''',
'''
''' + makeCommandExample( '1000 10 logxy' ) + '''
''' + makeCommandExample( '78125 5 logxy' ) + '''
''' + makeCommandExample( 'e sqr e logxy' ),
[ 'log', 'log10', 'log2', 'exp', 'exp10' ] ],

    'polyexp' : [
'logarithms', 'calculates the polyexponential of n, k',
'''
''',
'''
''',
[ ] ],


    'polylog' : [
'logarithms', 'calculates the polylogarithm of n, k',
'''
''',
'''
''',
[ ] ],


# //******************************************************************************
# //
# //  modifier operators
# //
# //******************************************************************************

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

*** Note:  As of 7.0.0, there are a few operators that don't correctly support
replacing single operands with lists.  I'm working through these to make
sure they all work.

*** Specifically, operators that are not of the type 'list_operators' that
take three or more operands do not work with lists.
''',
'''
''' + makeCommandExample( '[ 10 20 30 40 ] prime' ) + '''
''' + makeCommandExample( '[ 2 3 4 6 7 ] 3 +' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 ] [ 4 3 2 1 ] +' ) + '''
''' + makeCommandExample( '[ [ 1 2 3 4 ] [ 2 3 4 5 ] [ 3 4 5 6 ] ] [ 8 9 10 11 ] +' ),
[ ']' ] ],

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

*** Note:  As of 7.0.0, there are a few operators that don't correctly support
replacing single operands with lists.  I'm working through these to make
sure they all work.

*** Specifically, operators that are not of the type 'list_operators' that
take three or more operands do not work with lists.
''',
'''
''' + makeCommandExample( '[ 10 20 30 40 ] prime' ) + '''
''' + makeCommandExample( '[ 2 3 4 6 7 ] 3 +' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 ] [ 4 3 2 1 ] +' ) + '''
''' + makeCommandExample( '[ [ 1 2 3 4 ] [ 2 3 4 5 ] [ 3 4 5 6 ] ] [ 8 9 10 11 ] +' ),
[ '[' ] ],

    '(' : [
'modifiers', 'starts an operator list',
'''
''',
'''
''',
[ ')' ] ],

    ')' : [
'modifiers', 'end an operator list',
'''
''',
'''
''',
[ '(' ] ],

    'duplicate_term' : [
'modifiers', 'duplicates an argument n k times',
'''
This function duplicates terms, but requires the bracket operators to make the
resulting expression a list, rather than a set of k expressions.
''',
'''
''' + makeCommandExample( '10 2 duplicate_term +' ) + '''
''' + makeCommandExample( '[ 10 10 duplicate_term ]' ) + '''
''' + makeCommandExample( '[ 1 10 range 10 duplicate_term ]' ) + '''
''' + makeCommandExample( '[ 1 10 range 10 duplicate_term ] unique' ),
[ ] ],

    'duplicate_operator' : [
'modifiers', 'duplicates an operation n times',
'''
''',
'''
''',
[ ] ],

    'previous' : [
'modifiers', 'duplicates the previous argument (identical to \'n 2 dup\')',
'''
''',
'''
''',
[ ] ],

    'unlist' : [
'modifiers', 'expands a list into separate arguments',
'''
''',
'''
Here, we use 'unlist' to make arguments for 'euler_brick':

''' + makeCommandExample( '4 5 make_pyth_3' ) + '''
''' + makeCommandExample( '4 5 make_pyth_3 unlist euler_brick' ),
[ ] ],


# //******************************************************************************
# //
# //  number theory operators
# //
# //******************************************************************************

    'abundance' : [
'number_theory', 'returns the abundance of n',
'''
''',
'''
''',
[ ] ],

    'abundance_ratio' : [
'number_theory', 'returns the abundance ratio of n',
'''
''',
'''
''',
[ ] ],

    'aliquot' : [
'number_theory', 'returns the first k members of the aliquot sequence of n',
'''
''',
'''
''',
[ 'aliquot_limit', 'collatz' ] ],

    'aliquot_limit' : [
'number_theory', 'returns the members of the aliquot sequence of n until a value in the sequence exceeds 10^k',
'''
''',
'''
''',
[ 'aliquot', 'collatz' ] ],

    'alternating_factorial' : [
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''',
[ ] ],

    'barnesg' : [
'number_theory', 'evaluates the Barnes G-function for n',
'''
The Barnes G-function is the generalization of the superfactorial.
''',
'''
''',
[ ] ],

    'base' : [
'number_theory', 'interprets list elements as base k digits',
'''
''',
'''
''',
[ 'get_base_k_digits' ] ],

    'beta' : [
'number_theory', 'evaluates the Beta function for n and k',
'''
The Beta function is the equivalent to 'n gamma k gamma * n k + gamma /'.
''',
'''
''',
[ ] ],

    'calkin_wilf' : [
'number_theory', 'calculates the nth member of the Calkin-Wilf sequence',
'''
The operator returns a list of two numbers, the numerator and the denominator
of the nth Calkin-Wilf number.
''',
'''
''' + makeCommandExample( '0 10 range calkin_wilf' ) + '''
''' + makeCommandExample( '1000000 calkin_wilf' ),
[ ] ],

    'cf' : [
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''',
[ ] ],

    'collatz' : [
'number_theory', 'returns the first k members of the Collatz sequence of n',
'''
''',
'''
''',
[ 'aliquot' ] ],

    'count_divisors' : [
'number_theory', 'returns a count of the divisors of n',
'''
The count_divisors operator factors the argument and then calculates number of
divisors from the list of prime factors.  'divisors count' calculates the same
result, but the 'divisors' operator can generate prohibitively large lists for
numbers with a lot of factors.
''',
'''
''' + makeCommandExample( '98280 count_divisors' ) + '''
''' + makeCommandExample( '1 20 range count_divisors' ),
[ ] ],

    'crt' : [
'number_theory', 'calculates Chinese Remainder Theorem result of a list n of values and a list k of modulos',
'''
So using the Chinese Remainder Theorem, this function calculates a number that
is equal to n[ x ] modulo k[ x ], with x iterating through the indices of each
list (which must be the same size).
''',
'''
''',
[ ] ],

    'cyclotomic' : [
'number_theory', 'evaluates the the nth cyclotomic polynomial for k',
'''
''',
'''
''',
[ ] ],

    'digamma' : [
'number_theory', 'calculates the digamma function for n',
'''
This is the equivalent of '0 n polygamma'.
''',
'''
''',
[ ] ],

    'digital_root' : [
'number_theory', 'returns the digital root of N',
'''
https://en.wikipedia.org/wiki/Digital_root
''',
'''
''',
[ ] ],

    'divisors' : [
'number_theory', 'returns a list of divisors of n',
'''
This operator lists all proper divisors of an integer including 1 and the
integer itself, sorted in order of increasing size.
''',
'''
''' + makeCommandExample( '3600 divisors' ) + '''
''' + makeCommandExample( '[ 2 3 5 ] prod divisors' ),
[ ] ],

    'double_factorial' : [
'number_theory', 'calculates the double factorial of n',
'''
The name 'double factorial' is a little misleading as the definition of this
function is that n is multiplied by every second number between it and 1.

So it could sort of be thought of as a "half factorial".
''',
'''
''' + makeCommandExample( '1 10 range double_factorial' ),
[ ] ],

    'egypt' : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''',
[ ] ],

    'eta' : [
'number_theory', 'calculates the Dirichlet eta function for n',
'''
The eta function is also known as the "alternating zeta function".
''',
'''
''',
[ ] ],

    'euler_brick' : [
'number_theory', 'creates the dimensions of an Euler brick, given a Pythagorean triple',
'''
An Euler brick is a brick with three dimensions such that any two pairs form
a Pythogorean triples, therefore the face diagonals are also integers.
''',
'''
''' + makeCommandExample( '2 3 make_pyth_3 unlist euler_brick' ) + '''
''' + makeCommandExample( '828 2035 hypotenuse' ) + '''
''' + makeCommandExample( '828 3120 hypotenuse' ) + '''
''' + makeCommandExample( '2035 3120 hypotenuse' ),
[ ] ],

    'euler_phi' : [
'number_theory', 'calculates Euler\'s totient function for n',
'''
''',
'''
''',
[ ] ],

    'factor' : [
'number_theory', 'calculates the prime factorization of n',
'''
In order to take advantage of YAFU, please set the following configuration
values:

'yafu_binary' needs to be set to the YAFU executable name.
'yafu_path' needs to be set to the location of the YAFU executable.

e.g.:

rpn yafu_binary 'yafu-x64.core2.exe
rpn yafu_path 'c:\app\yafu
''',
'''
''',
[ ] ],

    'factorial' : [
'number_theory', 'calculates the prime factorization of n',
'''
'factorial' calculates the product of all whole numbers from 1 to n.
''',
'''
''' + makeCommandExample( '1 10 range factorial' ),
[ ] ],

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
''' + makeCommandExample( '1 20 range fibonacci' ) + '''
This shows the relationship between the Fibonacci numbers and the Lucas numbers
''' + makeCommandExample( '1 30 2 range2 fib lambda x sqr 5 * 4 - eval sqrt 2 30 2 range2 fib lambda x sqr 5 * 4 + eval sqrt interleave' ) + '''
''' + makeCommandExample( '1 30 range lucas' ),
[ ] ],

    'fibonorial' : [
'number_theory', 'calculates the product of the first n Fibonacci numbers',
'''
The name is a portmanteau of 'fibonacci' and 'factorial'.
''',
'''
''' + makeCommandExample( '1 10 range fibonorial' ),
[ ] ],

    'find_sum_of_cubes' : [
'number_theory', 'calculates the largest x for which the sum of the first xth squares is less than n',
'''
''',
'''
''' + makeCommandExample( '3025 find_sum_of_cubes' ) + '''
''' + makeCommandExample( '11025 find_sum_of_cubes' ),
[ 'find_sum_of_squares' ] ],

    'find_sum_of_squares' : [
'number_theory', 'calculates the largest x for which the sum of the first xth squares is less than n',
'''
''',
'''
''' + makeCommandExample( '55 find_sum_of_squares' ) + '''
''' + makeCommandExample( '506 find_sum_of_squares' ),
[ 'find_sum_of_cubes' ] ],

    'fraction' : [
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''',
[ ] ],

    'frobenius' : [
'number_theory', 'calculates the frobenius number of a list of values with gcd > 1'
'''
''',
'''
''',
[ ] ],

    'gamma' : [
'number_theory', 'calculates the gamma function for n',
'''
''',
'''
''',
[ ] ],

    'generate_polydivisibles' : [
'number_theory', 'generates all the polydivisible numbers for base n',
'''
''',
'''
''',
[ ] ],

    'get_base_k_digits' : [
'number_theory', 'interprets n as a list digits in base k',
'''
''',
'''
''',
[ 'base' ] ],

    'harmonic' : [
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
The harmonic series consists of the reciprocals of the natural numbers.
''',
'''
''' + makeCommandExample( '1 harmonic' ) + '''
''' + makeCommandExample( '2 harmonic' ) + '''
''' + makeCommandExample( '100 harmonic' ) + '''
''' + makeCommandExample( '1e100 harmonic' ),
[ ] ],

    'heptanacci' : [
'number_theory', 'calculates the nth Heptanacci number',
'''
''',
'''
''',
[ ] ],

    'hexanacci' : [
'number_theory', 'calculates the nth Hexanacci number',
'''
''',
'''
''',
[ ] ],

    'hurwitz_zeta' : [
'number_theory', 'calculates Hurwitz\'s zeta function for n and k',
'''
''',
'''
''',
[ 'zeta' ] ],

    'hyperfactorial' : [
'number_theory', 'calculates the hyperfactorial of n',
'''
Sloane and Plouffe define the hyperfactorial function as the product of the
first n numbers each taken to the power of itself.
''',
'''
''' + makeCommandExample( '-a45 1 10 range hyperfactorial' ),
[ ] ],

    'is_abundant' : [
'number_theory', 'returns whether or not n is an abundant number',
'''
''',
'''
''',
[ ] ],

    'is_achilles' : [
'number_theory', 'returns whether or not n is an Achilles number',
'''
''',
'''
''',
[ ] ],

    'is_carmichael' : [
'number_theory', 'returns whether n is a Carmichael number',
'''
''',
'''
''',
[ ] ],

    'is_composite' : [
'number_theory', 'returns whether n is composite',
'''
''',
'''
''',
[ ] ],

    'is_deficient' : [
'number_theory', 'returns whether or not n is a deficient number',
'''
''',
'''
''',
[ ] ],

    'is_friendly' : [
'number_theory', 'returns whether list n is a list of mutually friendly numbers',
'''
''',
'''
''',
[ ] ],

    'is_k_hyperperfect' : [
'number_theory', 'returns whether an integer n is k hyperperfect',
'''
''',
'''
''',
[ ] ],

    'is_k_semiprime' : [
'number_theory', 'returns whether n is a k-factor square-free number',
'''
''',
'''
''',
[ ] ],

    'is_k_sphenic' : [
'number_theory', 'returns whether n is a product of k distinct primes',
'''
This is my terminology, generalizing the idea of 'sphenic' to having an
arbitrary number of squarefree factors.

This terminology is not used, as far as I can tell, but there does not seem to
be an appropriate term to describe having a number of squarefree other than 1
(prime), 2 (semiprime), or 3 (sphenic).
''',
'''
''',
[ ] ],

    'is_perfect' : [
'number_theory', 'returns whether or not n is a perfect number',
'''
''',
'''
''',
[ ] ],

    'is_polydivisible' : [
'number_theory', 'returns whether or not n is polydivisible',
'''
''',
'''
''',
[ ] ],

    'is_powerful' : [
'number_theory', 'returns whether n is a powerful number',
'''
''',
'''
''',
[ ] ],

    'is_prime' : [
'number_theory', 'returns whether n is prime',
'''
My goal is optimize primality testing automatically so it can use the much
faster Miller-Rabin test without being unsure of the result.

Right now it's kind of dumb.  It just calls the old algorithm
for numbers smaller than a trillion.
''',
'''
''',
[ ] ],

    'is_prime_old' : [
'number_theory', 'returns whether n is prime',
'''
This uses the much, much faster Miller-Rabin code, but it can't be 100% sure
beyond a certain size.
''',
'''
''',
[ ] ],

    'is_pronic' : [
'number_theory', 'returns whether n is pronic',
'''
''',
'''
''',
[ ] ],

    'is_rough' : [
'number_theory', 'returns whether n is a k-rough number',
'''
''',
'''
''',
[ ] ],

    'is_ruth_aaron' : [
'number_theory', 'returns whether n is a Ruth-Aaron number',
'''
# //  http://mathworld.wolfram.com/Ruth-AaronPair.html
''',
'''
''',
[ ] ],

    'is_semiprime' : [
'number_theory', 'returns whether n is a semiprime number',
'''
''',
'''
''',
[ ] ],

    'is_smooth' : [
'number_theory', 'returns whether n is a k-smooth number',
'''
''',
'''
''',
[ ] ],

    'is_sphenic' : [
'number_theory', 'returns whether n is a sphenic number',
'''
''',
'''
''',
[ ] ],

    'is_squarefree' : [
'number_theory', 'returns whether n is a square-free number',
'''
''',
'''
''',
[ ] ],

    'is_strong_pseudoprime' : [
'number_theory', 'returns whether n is a strong pseudoprime to base k',
'''
''',
'''
''',
[ ] ],

    'is_unusual' : [
'number_theory', 'returns whether n is an unusual number',
'''
''',
'''
''',
[ ] ],

    'k_fibonacci' : [
'number_theory', 'calculates the nth K-Fibonacci number',
'''
''',
'''
''',
[ ] ],

    'leyland' : [
'number_theory', 'returns the Leyland number for n and k',
'''
''',
'''
''',
[ ] ],

    'log_gamma' : [
'number_theory', 'calculates the loggamma function for n',
'''
''',
'''
''',
[ ] ],

    'geometric_recurrence' : [
'number_theory', 'calculates the dth value of a linear recurrence specified by a list of factors (a), powers (b) and of seeds (c)',
'''
The factors (a) indicate the multiple of each preceding value to add to create
the next value in the recurrence list, listed from right to left (meaning the
last factor corresponds to the n - 1'th value in the sequence.  For the
Fibonacci or Lucas lists, this would be [ 1 1 ], meaning the previous value,
plus the one before that.  The tribonacci sequence would have a factor list of
[ 1 1 1 ].

The seeds (c), simply specify a list of initial values.  The number of seeds
cannot exceed the number of factors, but there may be fewer seeds.

The is some disagreement about whether the zeroes count as part of these linear
recurrence sequences.  In rpn, for the 'fib' and 'lucas', 'tribonacci' operators,
etc., in accordance with mpmath, they do not.  However, Sloane (oeis.org) does
count the zeroes.
''',
'''
''',
[ 'linear_recurrence' ] ],

    'linear_recurrence' : [
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
The Fibonacci sequence:
''' + makeCommandExample( '[ 1 1 ] [ 0 1 ] 18 linear_recurrence' ) + '''
The Lucas Sequence:
''' + makeCommandExample( '[ 1 1 ] [ 1 3 ] 17 linear_recurrence' ) + '''
The Tribonacci sequence:
''' + makeCommandExample( '[ 1 1 1 ] [ 0 0 1 ] 18 linear_recurrence' ) + '''
The Octanacci sequence:
''' + makeCommandExample( '[ 1 8 dup ] [ 0 7 dup 1 ] 20 linear_recurrence' ) + '''
The Pell numbers:
''' + makeCommandExample( '[ 1 2 ] [ 0 1 ] 15 linear_recurrence' ) + '''
The Perrin sequence:
''' + makeCommandExample( '[ 1 1 0 ] [ 3 0 2 ] 20 linear_recurrence' ),
[ 'linear_recurrence_with_modulo' ] ],

    'linear_recurrence_with_modulo' : [
'number_theory', 'calculates the cth value of a linear recurrence specified by a list of factors (a) and of seeds (b), where each successive result is taken modulo d',
'''
''',
'''
''',
[ ] ],

    'lucas' : [
'number_theory', 'calculates the nth Lucas number',
'''
The Lucas sequence works just like the Fibonacci sequence, but starts with
1 and 3, instead of 0 and 1.  It shares many properties with the Fibonacci
sequence.
''',
'''
''' + makeCommandExample( '1 17 range lucas' ),
[ ] ],

    'make_cf' : [
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''',
[ ] ],

    'make_pyth_3' : [
'number_theory', 'makes a pythagorean triple given two integers, n and k, as seeds',
'''
''',
'''
''',
[ 'make_pyth_4', 'hypotenuse' ] ],

    'make_pyth_4' : [
'number_theory', 'makes a pythagorean quadruple given two integers, n and k, as seeds',
'''
n and k cannot both be odd.
''',
'''
''',
[ 'make_pyth_3', 'hypotenuse' ] ],

    'merten' : [
'number_theory', 'returns Merten\'s function for n',
'''
''',
'''
''',
[ ] ],

    'mobius' : [
'number_theory', 'calculates the Mobius function for n',
'''
''',
'''
''',
[ ] ],

    'nth_carol' : [
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''',
[ ] ],

    'nth_kynea' : [
'number_theory', 'gets the nth Kynea number',
'''
A Kynea number is an integer of the form 4 ^ n + 2 ^ ( n + 1 ) - 1, studied by
Cletus Emmanuel.  The nth Kynea number is also equal to the nth power of 4
added to the (n + 1)th Mersenne number.
''',
'''
''',
[ ] ],

    'nth_jacobsthal' : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
''',
'''
''',
[ ] ],

    'nth_leonardo' : [
'number_theory', 'returns the nth Leonardo number',
'''
The Leonardo numbers form a recurrence relation where zeroth and first values
are 1 and 1, and each subsequent value is calculated by:

L( n ) = L( n - 1 ) + L( n - 2 ) + 1

rpn calculates the nth Leonardo number using the following formula, where
F( n ) is the nth Fibonacci number:

L( n ) = 2F( n + 1 ) - 1
''',
'''
''' + makeCommandExample( '1 20 range nth_leonardo' ),
[ ] ],

    'nth_mersenne_exponent' : [
'number_theory', '',
'''
These values are stored in a look-up table.  They are not calculated. ;-)

There are currently 49 known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.

https://primes.utm.edu/mersenne/index.html
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_mersenne_exponent' ) + '''
''' + makeCommandExample( '49 nth_mersenne_exponent' ),
[ 'nth_mersenne_prime', 'nth_perfect_number' ] ],

    'nth_mersenne_prime' : [
'number_theory', 'returns the nth known Mersenne prime',
'''
These values are stored in a look-up table.  They are not calculated. ;-)

There are currently 49 known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.

https://primes.utm.edu/mersenne/index.html
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_mersenne_prime' ) + '''
''' + makeCommandExample( '49 nth_mersenne_prime' ),
[ 'nth_mersenne_exponent', 'nth_perfect_number' ] ],

    'nth_padovan' : [
'number_theory', 'calculates the nth Padovan number',
'''
The Padovan sequence is the sequence of integers P(n) defined by the initial values

    P( 0 ) = P( 1 ) = P( 2 ) = 1

and the recurrence relation

    P( n ) = P( n - 2 ) + P( n - 3 ).

The Padovan can be computed by rpn using the 'linear_recurrence' functionality,
but OEIS (http://oeis.org/A000931) provides a non-iterative formula.
''',
'''
''' + makeCommandExample( '1 20 range nth_padovan' ) + '''
''' + makeCommandExample( '1 100 range nth_padovan lambda x is_prime filter' ),
[ ] ],

    'nth_perfect_number' : [
'number_theory', 'returns the nth known perfect number',
'''
These values are stored in a look-up table.  They are not calculated. ;-)

The nth known perfect number is computed from the nth known Mersenne prime.
There are currently 49 known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_perfect_number' ) + '''
''' + makeCommandExample( '49 nth_perfect_number' ),
[ ] ],

    'nth_stern' : [
'number_theory', 'calculates the nth value of the Stern diatomic series',
'''
''',
'''
''' + makeCommandExample( '1 100 range nth_stern' ),
[ ] ],

    'nth_thue_morse' : [
'number_theory', 'calculates the nth value of the Thue-Morse sequence',
'''
''',
'''
''' + makeCommandExample( '1 100 range nth_thue_morse' ),
[ ] ],

    'octanacci' : [
'number_theory', 'calculates the nth Octanacci number',
'''
''',
'''
''',
[ ] ],

    'pascal_triangle' : [
'number_theory', 'calculates the nth line of Pascal\'s triangle',
'''
''',
'''
''' + makeCommandExample( '1 10 range pascal_triangle -s1' ),
[ ] ],

    'pentanacci' : [
'number_theory', 'calculates the nth Pentanacci number',
'''
''',
'''
''' + makeCommandExample( '1 20 range pentanacci' ) + '''
''' + makeCommandExample( 'infinity lambda x 4 + pentanacci x 3 + pentanacci / limit' ),
[ ] ],

    'polygamma' : [
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''',
[ ] ],

    'primorial' : [
'number_theory', 'calculates the nth primorial',
'''
This function calculates the product of the first n prime numbers.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range primorial' ),
[ ] ],

    'repunit' : [
'number_theory', 'returns the nth repunit in base k',
'''
''',
'''
''' + makeCommandExample( '11 10 repunit' ) + '''
''' + makeCommandExample( '11 4 repunit -r4' ) + '''
''' + makeCommandExample( '11 4 repunit' ),
[ ] ],

    'riesel' : [
'number_theory', 'calculates the nth Riesel (or Woodall) number',
'''
''',
'''
''',
[ ] ],

    'radical' : [
'number_theory', 'returns the value of the radical function for n',
'''
The radical function is defined as the largest squarefree factor.
''',
'''
''' + makeCommandExample( '1 100 range radical' ),
[ ] ],

    'sigma' : [
'number_theory', 'returns the sum of the proper divisors of n',
'''
''',
'''
''' + makeCommandExample( '10 sigma' ) + '''
''' + makeCommandExample( '1 20 range sigma' ) + '''
Here's a list of deficient numbers from 1 to 100:
''' + makeCommandExample( '1 100 range lambda x sigma 2 / x is_less filter' ),
[ 'sigma_k', 'aliquot' ] ],

    'sigma_k' : [
'number_theory', 'returns the sum of the proper divisors of n each to the kth power',
'''
''',
'''
''' + makeCommandExample( '1 10 range sigma' ) + '''
''' + makeCommandExample( '1 10 range 1 sigma_k' ) + '''
''' + makeCommandExample( '1 10 range 2 sigma_k' ) + '''
''' + makeCommandExample( '1 10 range 3 sigma_k' ) + '''
''' + makeCommandExample( '1 10 range 4 sigma_k' ),
[ 'sigma' ] ],

    'subfactorial' : [
'number_theory', 'calculates the subfactorial of n',
'''
Also known as the 'derangement number', the subfactorial of integer n is the
number of permuations of n where no item appears in its natural place.

For instance, the derangements of [ 1, 2, 3 ] include [ 2, 3, 1 ] and
[ 3, 1, 2 ].

The subfactorial is calculated by the following formula:

floor( ( n!/e ) + 1/2 )
''',
'''
''' + makeCommandExample( '1 10 range subfactorial' ),
[ ] ],

    'sums_of_k_powers' : [
'number_theory', 'calculates every combination of b cth powers that sum to n',
'''
''',
'''
''' + makeCommandExample( '5104 3 3 sums_of_k_powers' ),
[ ] ],

    'sums_of_k_nonzero_powers' : [
'number_theory', 'calculates every combination of b nonzero cth powers that sum to n',
'''
''',
'''
''' + makeCommandExample( '1072 3 3 sums_of_k_nonzero_powers' ),
[ ] ],

    'superfactorial' : [
'number_theory', 'calculates the superfactorial of n',
'''
The superfactorial function is defined by Sloane and Plouffe to be the product
of the first n factorials, which is the equivalent of the integral values of
the Barnes G-function.
''',
'''
''' + makeCommandExample( '-a30 1 10 range superfactorial' ),
[ ] ],

    'tetranacci' : [
'number_theory', 'calculates the nth Tetranacci number',
'''
''',
'''
''',
[ ] ],

    'thabit' : [
'number_theory', 'gets the nth Thabit number',
'''
''',
'''
''',
[ ] ],

    'tribonacci' : [
'number_theory', 'calculates the nth Tribonacci number',
'''
''',
'''
''',
[ ] ],

    'trigamma' : [
'number_theory', 'calculates the trigamma function for n',
'''
This is the equivalent of '1 n polygamma'.
''',
'''
''',
[ ] ],

    'unit_roots' : [
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
''' + makeCommandExample( '2 unit_roots' ) + '''
''' + makeCommandExample( '3 unit_roots' ) + '''
''' + makeCommandExample( '4 unit_roots' ),
[ ] ],

    'zeta' : [
'number_theory', 'calculates Riemann\'s zeta function for n',
'''
''',
'''
''',
[ 'hurwitz_zeta' ] ],

    'zeta_zero' : [
'number_theory', 'calculates the nth non-trivial zero of Riemann\'s zeta function',
'''
''',
'''
''',
[ ] ],


# //******************************************************************************
# //
# //  physics operators
# //
# //******************************************************************************

    'acceleration' : [
'physics', 'calculates acceleration...',
'''
Calculates constant acceleration from a stationary start, given measurements
in two different units (in either order), from one of the following
combinations of units:
    velocity, length
    velocity, time
    distance, time
    acceleration, time      (trivial case)
    acceleration, length    (trivial case)
''',
'''
''' + makeCommandExample( '490.3325 meters 10 seconds acceleration' ),
[ 'velocity', 'distance' ] ],

    'black_hole_entropy' : [
'physics', 'calculates the entropy of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_mass' ) + '''
''' + makeCommandExample( '1 year black_hole_mass' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_mass' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_mass' ) + '''
''' + makeCommandExample( 'gee black_hole_mass' ) + '''
''' + makeCommandExample( '100 tons black_hole_mass' ),
[ 'black_hole_mass', 'black_hole_surface_gravity', 'black_hole_surface_area', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime' ] ],

    'black_hole_lifetime' : [
'physics', 'calculates the lifetime of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_lifetime' ) + '''
''' + makeCommandExample( '1 year black_hole_lifetime' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_lifetime' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_lifetime' ) + '''
''' + makeCommandExample( '1.0e12 kg black_hole_lifetime' ) + '''
''' + makeCommandExample( 'gee black_hole_lifetime' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_aarea', 'black_hole_temperature', 'black_hole_surface_gravity', 'black_hole_luminosity' ] ],

    'black_hole_luminosity' : [
'physics', 'calculates the luminosity of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_luminosity' ) + '''
''' + makeCommandExample( '1 year black_hole_luminosity' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_luminosity' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_luminosity' ) + '''
''' + makeCommandExample( 'gee black_hole_luminosity' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_aarea', 'black_hole_temperature', 'black_hole_surface_gravity', 'black_hole_lifetime' ] ],

    'black_hole_mass' : [
'physics', 'calculates the mass of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_mass' ) + '''
''' + makeCommandExample( '1 year black_hole_mass' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_mass' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_mass' ) + '''
''' + makeCommandExample( '10 gee black_hole_mass' ),
[ 'black_hole_surface_aarea', 'black_hole_surface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime' ] ],

    'black_hole_radius' : [
'physics', 'calculates the Schwarzchild radius of a black hole of mass n',
'''
''',
'''
''' + makeCommandExample( 'earth_mass black_hole_radius' ) + '''
''' + makeCommandExample( '10 solar_mass black_hole_radius' ),
[ 'black_hole_surface_aarea', 'black_hole_sureface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime' ] ],

    'black_hole_surface_area' : [
'physics', 'calculates the surface area of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_surface_area' ) + '''
''' + makeCommandExample( '1 year black_hole_surface_area' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_surface_area' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_surface_area' ) + '''
''' + makeCommandExample( '50 gee black_hole_surface_area' ),
[ 'black_hole_mass', 'black_hole_surface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime' ] ],

    'black_hole_surface_gravity' : [
'physics', 'calculates the surface gravity of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '1 year black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '2 gee black_hole_surface_gravity' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_aarea', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'surface_gravity' ] ],

    'black_hole_temperature' : [
'physics', 'calculates the temperature of a black hole given one of several different measurements'
'''
http://xaonon.dyndns.org/hawking/
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_temperature' ) + '''
''' + makeCommandExample( '1 year black_hole_temperature' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_temperature' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_temperature' ) + '''
''' + makeCommandExample( '0.01 gee black_hole_temperature' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_aarea', 'black_hole_lifetime', 'black_hole_sureface_gravity', 'black_hole_luminosity' ] ],

    'distance' : [
'physics', 'calculates distance...',
'''
Calculates distance given measurements in two different units (in either
order), from one of the following combinations of units:
    length, time          (trivial case)
    velocity, time
    acceleration, time
    jerk, time
    jounce, time
''',
'''
''' + makeCommandExample( '1 mile 5 seconds distance' ) + '''
''' + makeCommandExample( '100 mph 10 seconds distance' ) + '''
''' + makeCommandExample( 'gee 5 seconds distance' ),
[ 'velocity', 'acceleration' ] ],

    'energy_equivalence' : [
'physics', 'calculates the energy equivalence of mass n',
'''
''',
'''
''',
[ ] ],

    'escape_velocity' : [
'physics', 'calculates the escape velocity of an object of mass n and radius k',
'''
''',
'''
''',
[ ] ],

    'horizon_distance' : [
'physics', 'calculates the distance to the horizon for altitude n (assuming the Earth is a perfect sphere)'
'''
''',
'''
''',
[ ] ],

    'kinetic_energy' : [
'physics', '',
'''
''',
'''
''',
[ ] ],

    'mass_equivalence' : [
'physics', 'calculates the mass equivalence of energy n',
'''
''',
'''
''',
[ ] ],

    'orbital_mass' : [
'physics', '',
'''
''',
'''
''',
[ 'orbital_period', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_period' : [
'physics', 'calculates the orbital period of an object orbiting mass n at radius k',
'''
Mass n is really the combined mass of the object orbiting and the object being
orbited.
''',
'''
''',
[ 'orbital_mass', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_radius' : [
'physics', '',
'''
Mass n is really the combined mass of the object orbiting and the object being
orbited.
''',
'''
''',
[ 'orbital_mass', 'orbital_period', 'orbital_velocity' ] ],

    'orbital_velocity' : [
'physics', 'calculates the circular orbital velocity of an object for values n and k',
'''
The two arguments need to measurements of two of the following three types in
any order:

mass (the mass of the object being orbited)
length (the radius of the orbit)
time (the period of the orbit)

Mass n is really the combined mass of the object orbiting and the object being
orbited.
''',
'''
''' + makeCommandExample( '24 hours earth_mass orbital_velocity' ) + '''
''' + makeCommandExample( 'earth_mass 100 miles orbital_velocity' ) + '''
''' + makeCommandExample( 'sun_mass solar_year orbital_velocity mph convert' ),
[ 'orbital_mass', 'orbital_period', 'orbital_radius' ] ],

    'surface_gravity' : [
'physics', 'calculates the surface gravity of a spherical object',
'''
The two arguments need to be measurements of mass and radius, or measurements
of density and volume in either order.
''',
'''
''' + makeCommandExample( 'earth_mass earth_radius surface_gravity' ) + '''
''' + makeCommandExample( '5.51 g/cm^3 earth_volume surface_gravity' ) + '''
Calculate the surface gravity of a 10-solar-mass black hole:
''' + makeCommandExample( '10 solar_mass 10 solar_mass black_hole_radius surface_gravity', indent=4 ) + '''
''' + makeCommandExample( '10 solar_mass black_hole_surface_gravity', indent=4 ),
[ 'black_hole_gravity' ] ],

    'time_dilation' : [
'physics', 'calculates the relativistic time-dilation effect of a velocity difference of n',
'''
''',
'''
''' + makeCommandExample( '1 million mph time_dilation' ) + '''
''' + makeCommandExample( '0.99 c * time_dilation' ),
[ ] ],

    'velocity' : [
'physics', 'calculates velocity given...',
'''
Calculates velocity given measurements in two different units (in either
order), from one of the following combinations of units:
    acceleration, length
    acceleration, time
    jerk, length
    jerk, time
    jounce, length
    jounce, time
    length, time
    velocity, length        (trivial case)
    velocity, time          (trivial case)
''',
'''
''' + makeCommandExample( '9.80665 m/s^2 10 seconds velocity' ) + '''
''' + makeCommandExample( '9.80665 m/s^2 100 feet velocity' ) + '''
''' + makeCommandExample( '1 m/s^3 10 seconds velocity' ) + '''
''' + makeCommandExample( '1 m/s^3 100 feet velocity' ) + '''
''' + makeCommandExample( '1 m/s^4 10 seconds velocity' ) + '''
''' + makeCommandExample( '1 m/s^4 100 meters velocity' ) + '''
''' + makeCommandExample( '100 meters 10 seconds velocity' ) + '''
''',
[ 'acceleration', 'distance' ] ],


# //******************************************************************************
# //
# //  figurate number operators
# //
# //******************************************************************************

    'centered_cube' : [
'figurate_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''',
[ ] ],

    'centered_decagonal' : [
'figurate_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_dodecahedral' : [
'figurate_numbers', 'calculates the nth centered dodecahedral number',
'''
''',
'''
''',
[ ] ],

    'centered_heptagonal' : [
'figurate_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_hexagonal' : [
'figurate_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_icosahedral' : [
'figurate_numbers', 'calculates the nth centered icosahedral number',
'''
''',
'''
''',
[ ] ],

    'centered_nonagonal' : [
'figurate_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_octagonal' : [
'figurate_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_octahedral' : [
'figurate_numbers', 'calculates the nth centered octahedral number',
'''
''',
'''
''',
[ ] ],

    'centered_pentagonal' : [
'figurate_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''',
[ ] ],

    'centered_polygonal' : [
'figurate_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''',
[ ] ],

    'centered_square' : [
'figurate_numbers', 'calculates the nth centered square number',
'''
''',
'''
''',
[ ] ],

    'centered_tetrahedral' : [
'figurate_numbers', 'calculates the nth centered tetrahedral number',
'''
''',
'''
''',
[ ] ],

    'centered_triangular' : [
'figurate_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''',
[ ] ],

    'decagonal' : [
'figurate_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''',
[ ] ],

    'decagonal_centered_square' : [
'figurate_numbers', 'calculates the nth decagonal centered square number',
'''
'decagonal_centered_square' calculates the nth number that is both decagonal and
centered square.
''',
'''
''',
[ ] ],

    'decagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
'decagonal_heptagonal' calculates the nth number that is both decagonal and
heptagonal.
''',
'''
''',
[ ] ],

    'decagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth decagonal hexagonal number',
'''
'decagonal_hexagonal' calculates the nth number that is both decagonal and
hexagonal.
''',
'''
''',
[ ] ],

    'decagonal_nonagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
'decagonal_heptagonal' calculates the nth number that is both decagonal and
heptagonal.
''',
'''
''',
[ ] ],

    'decagonal_octagonal' : [
'figurate_numbers', 'calculates the nth decagonal octagonal number',
'''
'decagonal_octagonal' calculates the nth number that is both decagonal and
octagonal.
''',
'''
''',
[ ] ],

    'decagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth decagonal pentagonal number',
'''
'decagonal_pentagonal' calculates the nth number that is both decagonal and
pentgonal.
''',
'''
''',
[ ] ],

    'decagonal_triangular' : [
'figurate_numbers', 'calculates the nth decagonal triangular number',
'''
'decagonal_triangular' calculates the nth number that is both decagonal and
triangular.
''',
'''
''',
[ ] ],

    'dodecahedral' : [
'figurate_numbers', 'returns the nth dodecahedral number',
'''
''',
'''
''',
[ ] ],

    'generalized_pentagonal' : [
'figurate_numbers', 'calculates the nth generalized pentagonal number',
'''
''',
'''
''',
[ ] ],

    'heptagonal' : [
'figurate_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''',
[ ] ],

    'heptagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth heptagonal hexagonal number',
'''
'heptagonal_hexagonal' calculates the nth number that is both heptagonal and
hexagonal.
''',
'''
''',
[ ] ],

    'heptagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth heptagonal pentagonal number',
'''
'heptagonal_pentagonal' calculates the nth number that is both heptagonal and
pentgonal.
''',
'''
''',
[ ] ],

    'heptagonal_square' : [
'figurate_numbers', 'calculates the nth heptagonal square number',
'''
'heptagonal_square' calculates the nth number that is both heptagonal and
square.
''',
'''
''',
[ ] ],

    'heptagonal_triangular' : [
'figurate_numbers', 'calculates the nth heptagonal triangular number',
'''
'heptagonal_triangular' calculates the nth number that is both heptagonal and
triangular.
''',
'''
''',
[ ] ],

    'hexagonal' : [
'figurate_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''',
[ ] ],

    'hexagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth hexagonal pentagonal number',
'''
'hexagonal_pentagonal' calculates the nth number that is both hexagonal and
pentagonal.
''',
'''
''',
[ ] ],

    'hexagonal_square' : [
'figurate_numbers', 'calculates the nth hexagonal square number',
'''
'hexagonal_square' calculates the nth number that is both hexagonal and
square.
''',
'''
''',
[ ] ],

    'icosahedral' : [
'figurate_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''',
[ ] ],

    'nonagonal' : [
'figurate_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''',
[ ] ],

    'nonagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonagonal_heptagonal' calculates the nth number that is both nonagonal and
heptagonal.
''',
'''
''',
[ ] ],

    'nonagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonagonal_hexagonal' calculates the nth number that is both nonagonal and
hexagonal.
''',
'''
''',
[ ] ],

    'nonagonal_octagonal' : [
'figurate_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonagonal_octagonal' calculates the nth number that is both nonagonal and
octagonal.
''',
'''
''',
[ ] ],

    'nonagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonagonal_pentagonal' calculates the nth number that is both nonagonal and
pentgonal.
''',
'''
''',
[ ] ],

    'nonagonal_square' : [
'figurate_numbers', 'calculates the nth nonagonal square number',
'''
'nonagonal_square' calculates the nth number that is both nonagonal and square.
''',
'''
''',
[ ] ],

    'nonagonal_triangular' : [
'figurate_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonagonal_triangular' calculates the nth number that is both nonagonal and
triangular.

TODO: fix me
''',
'''
''',
[ ] ],

    'nth_centered_decagonal' : [
'figurate_numbers', 'finds the index of the centered decagonal number of value n',
'''
'nth_centered_decagonal' solves for the index of the equation used by
'centered_decagonal' to get the index i of the ith centered decagonal number
that corresponds to the value n.

If n is not a centered decagonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_heptagonal' : [
'figurate_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'nth_centered_heptagonal' solves for the index of the equation used by
'centered_heptagonal' to get the index i of the ith centered heptagonal number
that corresponds to the value n.

If n is not a centered heptagonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_hexagonal' : [
'figurate_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'nth_centered_hexagonal' solves for the index of the equation used by
'centered_hexagonal' to get the index i of the ith centered hexagonal number
that corresponds to the value n.

If n is not a centered hexagonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_nonagonal' : [
'figurate_numbers', 'finds the index of the centered nonagonal number of value n',
'''
'nth_centered_nonagonal' solves for the index of the equation used by
'centered_nonagonal' to get the index i of the ith centered nonagonal number
that corresponds to the value n.

If n is not a centered nonagonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_octagonal' : [
'figurate_numbers', 'finds the index of the centered octgonal number of value n',
'''
'nth_centered_octagonal' solves for the index of the equation used by
'centered_octagonal' to get the index i of the ith centered octagonal number
that corresponds to the value n.

If n is not a centered octagonal number, the result will not be a whole number.
''',
'''
''',
[ ] ],

    'nth_centered_pentagonal' : [
'figurate_numbers', 'finds the index of the centered pentagonal number of value n',
'''
'nth_centered_pentagonal? solves for the index of the equation used by
'centered_pentagonal' to get the index i of the ith centered pentagonal number
that corresponds to the value n.

If n is not a centered pentagonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_polygonal' : [
'figurate_numbers', 'finds the index of the centered polygonal number of value n',
'''
'nth_centered_polygonal' solves for the index of the equation used by
'centered_polygonal' to get the index i of the ith centered k-sided polygonal
number that corresponds to the value n.

If n is not a centered k-sided polygonal number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_centered_square' : [
'figurate_numbers', 'finds the index of the centered square number of value n',
'''
'nth_centered_square' solves for the index of the equation used by 'csquare'
to get the index i of the ith centered square number that corresponds to the
value n.

If n is not a centered square number, the result will not be a whole number.
''',
'''
''',
[ ] ],

    'nth_centered_triangular' : [
'figurate_numbers', 'finds the index of the centered triangular number of value n',
'''
'nth_centered_triangular' solves for the index of the equation used by
'centered_triangular' to get the index i of the ith centered triangular number
that corresponds to the value n.

If n is not a centered triangular number, the result will not be a whole
number.
''',
'''
''',
[ ] ],

    'nth_decagonal' : [
'figurate_numbers', 'finds the index of the decagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_hexagonal' : [
'figurate_numbers', 'finds the index of the hexagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_heptagonal' : [
'figurate_numbers', 'finds the index of the heptagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_nonagonal' : [
'figurate_numbers', 'finds the index of the nonagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_octagonal' : [
'figurate_numbers', 'finds the index of the octagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_pentagonal' : [
'figurate_numbers', 'finds the index of the pentagonal number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_polygonal' : [
'figurate_numbers', 'finds the index of the polygonal number with k sides of value n',
'''
''',
'''
''',
[ ] ],

    'nth_square' : [
'figurate_numbers', 'finds the index of the square number of value n',
'''
''',
'''
''',
[ ] ],

    'nth_triangular' : [
'figurate_numbers', 'finds the index of the triangular number of value n',
'''
''',
'''
''',
[ ] ],

    'octagonal' : [
'figurate_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''',
[ ] ],

    'octagonal_heptagonal' : [
'figurate_numbers', 'returns the nth octagonal heptagonal number',
'''
'octagonal_heptagonal' calculates the nth number that is both octagonal and
heptagonal.
''',
'''
''',
[ ] ],

    'octagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth octagonal hexagonal number',
'''
'octagonal_hexagonal' calculates the nth number that is both octagonal and
hexagonal.
''',
'''
''',
[ ] ],

    'octagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth octagonal pentagonal number',
'''
'octagonal_pentagonal' calculates the nth number that is both octagonal and
pentagonal.
''',
'''
''',
[ ] ],

    'octagonal_square' : [
'figurate_numbers', 'calculates the nth octagonal square number',
'''
'octagonal_square' calculates the nth number that is both octagonal and
square.
''',
'''
''',
[ ] ],

    'octagonal_triangular' : [
'figurate_numbers', 'calculates the nth octagonal triangular number',
'''
'octagonal_triangular' calculates the nth number that is both octagonal and
triangular.
''',
'''
''',
[ ] ],

    'octahedral' : [
'figurate_numbers', 'calculates the nth octahedral number',
'''
''',
'''
''',
[ ] ],

    'pentagonal' : [
'figurate_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''',
[ ] ],

    'pentagonal_square' : [
'figurate_numbers', 'calculates the nth pentagonal square number',
'''
''',
'''
''',
[ ] ],

    'pentagonal_triangular' : [
'figurate_numbers', 'calculates the nth pentagonal triangular number',
'''
''',
'''
''',
[ ] ],

    'pentatope' : [
'figurate_numbers', 'calculates the nth pentatope number',
'''
''',
'''
''',
[ ] ],

    'polygonal' : [
'figurate_numbers', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' + makeCommandExample( '13 triangular' ) + '''
''' + makeCommandExample( '13 3 polygonal' ) + '''
''' + makeCommandExample( '-a25 387 8925662618878671 polygonal' ),
[ ] ],

    'polytope' : [
'figurate_numbers', 'calculates nth polytope number of dimension k',
'''
''',
'''
''',
[ ] ],

    'pyramid' : [
'figurate_numbers', 'calculates the nth square pyramidal number',
'''
''',
'''
''',
[ ] ],

    'rhombic_dodecahedral' : [
'figurate_numbers', 'calculates the nth rhombic dodecahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range rhombic_dodecahedral' ),
[ ] ],

    'square_triangular' : [
'figurate_numbers', 'calculates the nth square triangular number',
'''
'square_triangular' calculates the nth number that is both square and
triangular.
''',
'''
''' + makeCommandExample( '1 8 range square_triangular' ),
[ ] ],

    'star' : [
'figurate_numbers', 'calculates the nth star number',
'''
''',
'''
''' + makeCommandExample( '1 8 range star' ),
[ ] ],

    'stella_octangula' : [
'figurate_numbers', 'calculates the nth stella octangula number',
'''
A stella octangula number is a figurate number based on the stella octangula,
of the form n(2n^2 - 1).

The "stella octangula" is otherwise known as a "stellated octahedron".

https://en.wikipedia.org/wiki/Stella_octangula_number
http://oeis.org/A007588
''',
'''
''' + makeCommandExample( '1 8 range stella_octangula' ),
[ ] ],

    'tetrahedral' : [
'figurate_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range tetrahedral' ),
[ ] ],

    'triangular' : [
'figurate_numbers', 'calcuates the nth triangular number',
'''
''',
'''
''' + makeCommandExample( '1 8 range triangular' ),
[ ] ],

    'truncated_octahedral' : [
'figurate_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range truncated_octahedral' ),
[ ] ],

    'truncated_tetrahedral' : [
'figurate_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range truncated_tetrahedral' ),
[ ] ],

#   'antitet' : [ findTetrahedralNumber, 1, [ ] ],


# //******************************************************************************
# //
# //  powers and roots operators
# //
# //******************************************************************************

    'agm' : [
'powers_and_roots', 'calculates the arithmetic-geometric mean of two numbers',
'''
''',
'''
''',
[ 'mean', 'geometric_mean', 'harmonic_mean' ] ],

    'cube' : [
'powers_and_roots', 'calculates the cube of n',
'''
'cube' simply returns the value of n to the third power.

It is the equivalent of 'n 3 power'.
''',
'''
''' + makeCommandExample( '4 cube' ) + '''
''' + makeCommandExample( '3 feet cube' ),
[ 'square', 'cube_root', 'power' ] ],

    'cube_root' : [
'powers_and_roots', 'calculates the cube root of n',
'''
This operator returns the cube root of n.

It is the equivalent of 'n 3 root'.
''',
'''
''' + makeCommandExample( '64 cube_root' ) + '''
''' + makeCommandExample( '27 feet^3 cube_root' ),
[ 'cube', 'square_root', 'root' ] ],

    'exp' : [
'powers_and_roots', 'calculates the nth power of e',
'''
This operator returns e to the power of n.  it is the inverse of the 'log'
operator and is the equivalent of the following:

'e n power'

n can be any real or complex value.
''',
'''
''' + makeCommandExample( '2 exp' ) + '''
''' + makeCommandExample( '1 10 range exp' ) + '''
''' + makeCommandExample( '1 i exp' ),
[ 'log', 'exp10', 'expphi', 'polyexp' ] ],

    'exp10' : [
'powers_and_roots', 'calculates nth power of 10',
'''
This operator returns 10 to the power of n.  it is the inverse of the 'log10'
operator and is the equivalent of the following:

'10 n power'

n can be any real or complex value.
''',
'''
''' + makeCommandExample( '2 exp10' ) + '''
''' + makeCommandExample( '1 10 range exp10' ) + '''
''' + makeCommandExample( '1 i exp10' ),
[ 'log10', 'exp', 'expphi' ] ],

    'expphi' : [
'powers_and_roots', 'calculates the nth power of phi',
'''
expphi simply takes phi (the Golden Ratio) to the power of the argument n.

It was originally added to make testing the base phi output easier.
''',
'''
''' + makeCommandExample( '2 expphi' ) + '''
''' + makeCommandExample( '3 expphi 2 expphi -' ),
[ 'phi', 'exp', 'exp10' ] ],

    'hyper4_2' : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''',
[ 'tetrate', 'power' ] ],

    'power' : [
'powers_and_roots', 'calculates the kth power of n',
'''
This operator raises the n to the power of k.
''',
'''
''' + makeCommandExample( '4 5 **' ) + '''
''' + makeCommandExample( '1 10 range 3 **' ) + '''
''' + makeCommandExample( '1 foot 3 ** gallon convert' ),
[ 'root', 'square', 'cube', 'tetrate' ] ],

    'power_tower' : [
'powers_and_roots', 'calculates list n as a power tower',
'''
''',
'''
''',
[ 'power_tower2', 'power' ] ],

    'power_tower2' : [
'powers_and_roots', 'calculates list n as a right-associative power tower',
'''
''',
'''
''',
[ 'power_tower', 'power' ] ],


    'powmod' : [
'powers_and_roots', 'calculates a to the bth power modulo c',
'''
a, b and c are assumed to be integers
''',
'''
''',
[ 'power', 'modulo' ] ],

    'root' : [
'powers_and_roots', 'calculates the kth root of n',
'''
This operator returns the kth root of n.
''',
'''
''' + makeCommandExample( '2 12 //' ) + '''
''' + makeCommandExample( '1 10 range 2 //' ) + '''
''' + makeCommandExample( '4 foot^2 2 //' ),
[ 'power', 'square_root', 'cube_root' ] ],

    'square' : [
'powers_and_roots', 'calculates the square of n',
'''
This operator is the equivalent of 'n 2 power'.

It returns the square of n.
''',
'''
''' + makeCommandExample( 'pi square' ) + '''
''' + makeCommandExample( '10 inches square foot^2 convert' ) + '''
''' + makeCommandExample( '[ 2 G sun_mass ] prod c square /' ) + '''
''' + makeCommandExample( '1 10 range square' ),
[ 'square_root', 'cube', 'power' ] ],

    'square_root' : [
'powers_and_roots', 'calculates the square root of n',
'''
This operator is the equivalent of 'n 2 root'.
''',
'''
''' + makeCommandExample( '2 square_root' ) + '''
''' + makeCommandExample( '64 feet^2 square_root' ) + '''
''' + makeCommandExample( '5 sqrt 1 + 2 /' ),
[ 'square', 'cube_root', 'root' ] ],

    'tetrate' : [
'powers_and_roots', 'tetrates n by k',
'''
Tetration is the process of repeated exponentiation.  n is exponentiated by
itself k times.
''',
'''
''' + makeCommandExample( '3 3 tetrate' ) + '''
''' + makeCommandExample( '10 10 tetrate' ) + '''
''' + makeCommandExample( '2 1 6 range tetrate' ),
[ 'power', 'hyper4_2' ] ],

# //******************************************************************************
# //
# //  prime number operators
# //
# //******************************************************************************

    'balanced_prime' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'balanced_prime_' : [
'prime_numbers', 'calculates the nth set of balanced primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'cousin_prime' : [
'prime_numbers', 'returns the nth cousin prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'cousin_prime_' : [
'prime_numbers', 'returns the nth set of cousin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'double_balanced' : [
'prime_numbers', 'returns the nth double balanced prime',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '50 double_balanced' ) + '''
''' + makeCommandExample( '1 10 range double_balanced' ),
[ ] ],

    'double_balanced_' : [
'prime_numbers', 'returns the nth double balanced prime and its neighbors',
'''
A double balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors.  This operator also returns the neighbors
and second neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '50 double_balanced_' ) + '''
''' + makeCommandExample( '50 double_balanced_ diffs' ),
[ ] ],

    'isolated_prime' : [
'prime_numbers', 'returns the nth isolated prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/
and is distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'next_prime' : [
'prime_numbers', 'returns the next prime number greater than or equal to n',
'''
''',
'''
''' + makeCommandExample( '10 next_prime' ) + '''
Generate a random 200-digit prime:

''' + makeCommandExample( '-a201 10 200 ** random_int next_prime' ),
[ 'prime', 'primes', 'next_primes', 'previous_prime', 'previous_primes' ] ],

    'next_primes' : [
'prime_numbers', 'returns the next k prime numbers greater than or equal to n',
'''
''',
'''
''' + makeCommandExample( '100 10 next_primes' ) + '''
''' + makeCommandExample( '-a71 10 70 ** random_int 5 next_primes -s1' ),
[ 'prime', 'primes', 'next_prime', 'previous_primes' ] ],

    'next_quadruplet_prime' : [
'prime_numbers', 'finds the closest set of quadruplet primes above n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'next_quintuplet_prime' : [
'prime_numbers', 'finds the closest set of quintuplet primes above n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'nth_prime' : [
'prime_numbers', 'finds the index of the closest prime less than or equal n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'nth_quadruplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'nth_quintuplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest quintuplet prime set over n',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'polyprime' : [
'prime_numbers', 'returns the nth prime, recursively k times',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'previous_prime' : [
'prime_numbers', 'returns the previous prime number less than n',
'''
''',
'''
''' + makeCommandExample( '10 previous_prime' ) + '''
''' + makeCommandExample( '100 previous_prime' ),
[ 'prime', 'primes', 'next_primes', 'next_prime', 'previous_primes' ] ],

    'previous_primes' : [
'prime_numbers', 'returns the previous k prime numbers less than n',
'''
''',
'''
''' + makeCommandExample( '100 10 previous_primes' ) + '''
''' + makeCommandExample( '-a71 10 70 ** random_int 5 previous_primes -s1' ),
[ 'prime', 'primes', 'next_prime', 'next_primes', 'previous_prime' ] ],

    'prime' : [
'prime_numbers', 'returns the nth prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ 'primes', 'prime_range' ] ],

    'primes' : [
'prime_numbers', 'generates a range of k primes starting from index n',
'''
This operator is much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion pribmes.
''',
'''
''' + makeCommandExample( '1 20 primes' ) + '''
''' + makeCommandExample( '320620307 10 primes' ),
[ 'prime', 'prime_range' ] ],

    'prime_pi' : [
'prime_numbers', 'calculates the count of prime numbers up to and including n',
'''
''',
'''
''',
[ ] ],

    'prime_range' : [
'prime_numbers', 'generates a range of primes starting from index n to index k',
'''
This operator is much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion pribmes.
''',
'''
''' + makeCommandExample( '1 21 prime_range' ) + '''
''' + makeCommandExample( '4458934 4458960 prime_range' ),
[ 'prime', 'primes' ] ],

    'quadruplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'quadruplet_prime_' : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'quintuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'quintuplet_prime_' : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'safe_prime' : [
'prime_numbers', 'returns the nth safe prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sextuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sextuplet_prime_' : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sexy_prime' : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns the smaller of
nth set of sexy primes, so the value of the result + 6 will also be prime.
''',
'''
''' + makeCommandExample( '16387 sexy_prime' ) + '''
''' + makeCommandExample( '1 10 range sexy_prime' ),
[ ] ],

    'sexy_prime_' : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns both members
of the nth set of sexy primes, which will differ by 6.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '213819 sexy_prime_' ) + '''
''' + makeCommandExample( '1001 1010 range sexy_prime_' ),
[ ] ],

    'sexy_triplet' : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sexy_triplet_' : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sexy_quadruplet' : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sexy_quadruplet_' : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'sophie_prime' : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'superprime' : [
'prime_numbers', 'returns the nth superprime (the nth primeth prime)',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'triple_balanced' : [
'prime_numbers', 'returns the nth triple balanced prime',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range triple_balanced' ),
[ ] ],

    'triple_balanced_' : [
'prime_numbers', 'returns the nth triple balanced prime and its neighbors',
'''
A triple balanced prime is a primes which is the average of its immediate
neighbors, its second neighbors and its third neighbors.  This operator also
returns the neighbors, second neighbors, and third neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '10 triple_balanced_' ) + '''
''' + makeCommandExample( '10 triple_balanced_ diffs' ),
[ ] ],

    'triplet_prime' : [
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
only the first prime of the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '1231 triplet_prime' ) + '''
''' + makeCommandExample( '1 10 range triplet_prime' ),
[ ] ],

    'triplet_prime_' : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.  This operator returns
a list of the three primes in the triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '1231 triplet_prime_' ) + '''
''' + makeCommandExample( '1 10 range triplet_prime_ -s1' ),
[ ] ],

    'twin_prime' : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''',
[ ] ],

    'twin_prime_' : [
'prime_numbers', 'returns the nth set of twin primes',
'''

Prime numbers can be calculated from scratch, but this would be excessively
slow.  RPN supports caching prime values to data files in ''' + g.dataDir + '''/ and is
distributed with data files calculated through several billion primes.
''',
'''
''' + makeCommandExample( '157 twin_prime_' ) + '''
''' + makeCommandExample( '1 20 twin_prime_' ) + '''
An extremely crude estimation of Brun's twin prime constant:

''' + makeCommandExample( 'rpn 1 50 range twin_primes_ 1/x sum sum' ),
[ ] ],


# //******************************************************************************
# //
# //  settings operators (for use in interactive mode)
# //
# //******************************************************************************

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
''',
[ ] ],

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
''',
[ ] ],

    'comma_mode' : [
'settings', 'set temporary comma mode in interactive mode',
'''
''',
'''
''',
[ ] ],

    'decimal_grouping' : [
'settings', 'used in interactive mode to set the decimal grouping level',
'''
''',
'''
''',
[ ] ],

    'hex_mode' : [
'settings', 'set temporary hex mode in interactive mode',
'''
''',
'''
''',
[ ] ],

    'identify' : [
'settings', 'set identify mode in interactive mode',
'''
''',
'''
''',
[ ] ],

    'identify_mode' : [
'settings', 'set temporary identify mode in interactive mode',
'''
''',
'''
''',
[ ] ],

    'input_radix' : [
'settings', 'used in interactive mode to set the input radix',
'''
''',
'''
''',
[ ] ],

    'integer_grouping' : [
'settings', 'used in interactive mode to set the integer grouping',
'''
''',
'''
''',
[ ] ],

    'leading_zero' : [
'settings', 'when set to true and integer grouping is being used, output will include leading zeroes',
'''
''',
'''
''',
[ ] ],

    'leading_zero_mode' : [
'settings', 'used in the interactive mode to set the leading zero mode for output',
'''
''',
'''
''',
[ ] ],

    'octal_mode' : [
'settings', 'set temporary octal mode in interactive mode',
'''
''',
'''
''',
[ ] ],

    'output_radix' : [
'settings', 'used in the interactive mode to set the output radix',
'''
''',
'''
''',
[ ] ],

    'precision' : [
'settings', 'used in the interactive mode to set the output precision',
'''
''',
'''
''',
[ ] ],

    'timer' : [
'settings', 'set timer mode in interactive mode',
'''
''',
'''
''',
[ 'timer_mode' ] ],

    'timer_mode' : [
'settings', 'set temporary timer mode in interactive mode',
'''
''',
'''
''',
[ 'timer' ] ],


# //******************************************************************************
# //
# //  special operators
# //
# //******************************************************************************

    'constant' : [
'special', 'creates a user-defined constant',
'''
This operator is not implemented yet!
''',
'''
''',
[ ] ],

    'delete_config' : [
'special', 'delete configuration setting n',
'''
''',
'''
''',
[ 'dump_config', 'get_config', 'set_config' ] ],

    'dump_config' : [
'special', 'dumps all configuration settings',
'''
''',
'''
''',
[ 'delete_config', 'get_config', 'set_config' ] ],

    'describe' : [
'special', 'outputs a list of properties of integer n',
'''
This is a special operator whose output is simply printed to the console.  The
actual return value of the operator is the integer argument, so from RPN's
point of view, it doesn't actually do anything.
''',
'''
''',
[ ] ],

    'echo' : [
'special', 'when the next operator is evaluated, appends the result to n',
'''
The echo operator does not apply to operators in an operator list, but is
applied when the operator list is completed.
''',
'''
''' + makeCommandExample( '2 echo 2 +' ) + '''
''' + makeCommandExample( '2 echo 2 echo +' ),
[ ] ],

    'enumerate_dice' : [
'special', 'evaluates a dice expression to simulate rolling dice, with dice values enumerated separately',
'''
This feature simulates dice rolling and can be used to do calculations and
simulations for role-playing games, war games or anything else that uses dice.

Please see 'roll_dice' for details of the dice expression mini-language.

Please note that 'enumerate_dice' ignores the modifiers applied to the dice
expressions.
''',
'''
''' + makeCommandExample( '3d6 enumerate_dice', indent=4 ) + '''
''' + makeCommandExample( '2d6,d8 enumerate_dice', indent=4 ) + '''
''' + makeCommandExample( 'd100 enumerate_dice', indent=4 ) + '''
''' + makeCommandExample( 'd2,d3,d4,d5,d6,d7,d8 enumerate_dice', indent=4 ),
[ 'roll_dice', 'enumerate_dice_', 'permute_dice', 'roll_dice_' ] ],

    'enumerate_dice_' : [
'special', 'evaluates a dice expression to simulate rolling dice k times, with dice values enumerated separately for each roll',
'''
Please see 'roll_dice' for an explanation of the dice expression language.

Please note that 'enumerate_dice' ignores the modifiers applied to the dice
expressions.
''',
'''
''' + makeCommandExample( '2d6 10 enumerate_dice_' ) + '''
''' + makeCommandExample( '4d6x1 6 enumerate_dice_' ),
[ 'roll_dice', 'enumerate_dice', 'permute_dice', 'roll_dice_' ] ],

    'estimate' : [
'special', 'estimates the value of a measurement in common terms',
'''
Often calculations result in units which are not intuitive, usually when they
are very small or very large.  The 'estimate' operator is an attempt to compare
a measurement to something familiar to give the user an idea of the rough
magnitude of the measurement.
''',
'''
''' + makeCommandExample( '1100 lumens estimate' ) + '''
''' + makeCommandExample( '400 acres estimate' ) + '''
''' + makeCommandExample( '1 square_mm estimate' ) + '''
''' + makeCommandExample( '8 gees estimate' ) + '''
''' + makeCommandExample( '1 arcsecond estimate' ) + '''
''' + makeCommandExample( '300 pounds estimate' ) + '''
''' + makeCommandExample( '1 farad estimate' ) + '''
''' + makeCommandExample( '1 franklin estimate' ) + '''
''' + makeCommandExample( '60 pascal-seconds estimate' ) + '''
''' + makeCommandExample( '1 gram energy_equivalence estimate' ) + '''
''' + makeCommandExample( '8 micrograms estimate' ) + '''
''' + makeCommandExample( '1 MHz estimate' ) + '''
''' + makeCommandExample( 'c 100 / estimate' ) + '''
''' + makeCommandExample( '10000 cubic_miles estimate' ) + '''
''' + makeCommandExample( '1 petabyte estimate' ) + '''
''' + makeCommandExample( '4 million gallons estimate' ),
[ 'convert' ] ],

    'get_config' : [
'special', 'get configuration setting n',
'''
There are currently only two configuration settings supported:

'yafu_binary' - the YAFU executable name.
'yafu_path' - the location of the YAFU executable.
''',
'''
''',
[ 'delete_config', 'dump_config', 'set_config' ] ],

    'get_variable' : [
'special', 'retrieves the value for n in the user config data file',
'''
''',
'''
''' + makeCommandExample( 'magic_number 37 set_variable' ) + '''
''' + makeCommandExample( 'magic_number get_variable' ) + '''
''' + makeCommandExample( '$magic_number' ),
[ 'set_variable' ] ],

    'help' : [
'special', 'displays help text',
'''
''',
'''
''',
[ 'topics' ] ],

    'if' : [
'special', 'returns a if condition c is true, otherwise returns b',
'''
'if' is useful in lambdas, which is why it was added.
''',
'''
''' + makeCommandExample( '1 2 true if' ) + '''
''' + makeCommandExample( '1 2 false if' ),
[ ] ],

    'list_from_file' : [
'special', 'reads a list of values from a file',
'''
The file should have one number per line, and the values are subject to the
same processing as numerical values on the rpn command line.
''',
'''
''',
[ ] ],

    'name' : [
'special', 'returns the English name for the integer value or measurement n',
'''
This operator returns the English name for any integer n.

The upper limit of integers rpn can name is 10^3004 - 1.

If the number has more digits than the current precision setting of rpn, the
result will be subject to rounding and will be incorrect.

''' + makeCommandExample( '157 name' ) + '''
c:\>rpn 10 3000 ** name
nine hundred ninety-nine octononagintanongentillion nine hundred ninety-nine
septenonagintanongentillion nine hundred ninety-nine senonagintanongentillion
nine hundred ninety-nine...
''' + makeCommandExample( '-a3000 10 3000 ** name' ),
'''
''' + makeCommandExample( '1 name' ) + '''
''' + makeCommandExample( '157 name' ) + '''
''' + makeCommandExample( '1,234,567,890 name' ) + '''
''' + makeCommandExample( '1 gallon name' ) + '''
''' + makeCommandExample( '114 feet name' ) + '''
''' + makeCommandExample( '2337 ounces [ pounds ounces ] convert name' ),
[ 'ordinal_name' ] ],

    'oeis' : [
'special', 'downloads the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
''' + makeCommandExample( 'rpn 10349 oeis' ),
[ 'oeis_comment', 'oeis_ex', 'oeis_name', 'oeis_offset' ] ],

    'oeis_comment' : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
''' + makeCommandExample( '98593 oeis_comment' ),
[ 'oeis_name', 'oeis_ex', 'oeis' ] ],

    'oeis_ex' : [
'special', 'downloads the extra information field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
''' + makeCommandExample( '178 oeis_ex' ),
[ 'oeis_comment', 'oeis_name', 'oeis' ] ],

    'oeis_name' : [
'special', 'downloads the name of the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.pckl.bz2.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
''' + makeCommandExample( '10349 oeis_name' ),
[ 'oeis_ex', 'oeis', 'oeis_comment' ] ],

    'oeis_offset' : [
'special', '',
'''
All data downloaded from OEIS is cached.  OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is
to delete rpnData/oeis.cache.  Eventually, I'll add a tool to allow
flushing the cache for a particular entry.
''',
'''
''',
[ 'oeis_name', 'oeis_ex', 'oeis' ] ],

    'ordinal_name' : [
'special', 'returns the English ordinal name for the integer value n',
'''
The ordinal names for numbers start with 'first', 'second', etc.

The upper limit of integers rpn can name is 10^3004 - 1.

If the number has more digits than the current precision setting of rpn, the
result will be subject to rounding and will be incorrect.

c:\>rpn 10 3000 ** ordinal_name
nine hundred ninety-nine octononagintanongentillion nine hundred ninety-nine
septenonagintanongentillion nine hundred ninety-nine senonagintanongentillion
nine hundred ninety-nine...
''' + makeCommandExample( '-a3000 10 3000 ** ordinal_name' ),
'''
''' + makeCommandExample( '0 ordinal_name' ) + '''
''' + makeCommandExample( '1 ordinal_name' ) + '''
''' + makeCommandExample( '2 ordinal_name' ) + '''
''' + makeCommandExample( '-1 ordinal_name' ) + '''
''' + makeCommandExample( '1999 ordinal_name' ) + '''
''' + makeCommandExample( '2001 ordinal_name' ),
[ 'name' ] ],

    'permute_dice' : [
'special', 'evaluates all permutations for a dice expression',
'''
This operator will iterate through all unique combinations of the dice
expression n (see 'roll_dice') and list all the results.
''',
'''
''' + makeCommandExample( '2d6 permute_dice' ) + '''
This expression compares the distribution of 4d6 drop the lowest and 5d6 drop
the two lowest for all outcomes.
''' + makeCommandExample( '4d6x1 permute_dice occurrence_ratios 5d6x2 permute_dice occurrence_ratios interleave -s1', indent=4 ) + '''
As can be seen the change for an 18 goes from 1.6% with '4d6x1' to 3.5% with
'5d6x2'.''',
[ 'roll_dice', 'roll_dice_', 'enumerate_dice', 'enumerate_dice_' ] ],

    'random_integer' : [
'special', 'returns a random integer from 0 to n - 1',
'''
This operator returns a random integer in the range of 0 to n - 1, inclusive.

rpn is automatically seeded every time it runs, so random number streams are
not reproducible.
''',
'''
''' + makeCommandExample( '10 random_integer' ) + '''
''' + makeCommandExample( '1000 random_integer' ) + '''
''' + makeCommandExample( '1000000 random_integer' ),
[ 'random', 'random_', 'random_integer_' ] ],

    'random_integer_' : [
'special', 'returns a list of k random integers from 0 to n - 1',
'''
This operator returns a series of k random integers in the range of 0 to
n - 1, inclusive.

rpn is automatically seeded every time it runs, so random number streams are
not reproducible.
''',
'''
''' + makeCommandExample( '10 10 random_integer_' ) + '''
''' + makeCommandExample( '1000 5 random_integer_' ) + '''
''' + makeCommandExample( '1 billion 4 random_integer_' ) + '''
Test the birthday paradox:
''' + makeCommandExample( '365 23 random_integer_ sort', indent=4 ) + '''
You will see a duplicate approximately 50% of the time.  Since this command
is run when the help file is generated, you may or may not see a duplicate
here, but the exact odds of seeing a duplicate can be computed:
''' + makeCommandExample( '1 364 364 21 - range 365 / prod -', indent=4 ),
[ 'random_integer', 'random', 'random_' ] ],

    'random' : [
'special', 'returns a random value from 0 to 1',
'''
This operator will return a random value greater than or equal to zero and less
than one.  The number of sigificant digits is controlled by the precision set
in rpn.
''',
'''
''' + makeCommandExample( 'random' ) + '''
''' + makeCommandExample( '-a20 random' ) + '''
''' + makeCommandExample( 'random 1000000 *' ),
[ ] ],

    'random_' : [
'special', 'returns a list of n random values from 0 to 1',
'''
This operator will return a list of n random values greater than or equal to
zero and less than one.  The number of sigificant digits is controlled by the
precision set in rpn.
''',
'''
''' + makeCommandExample( '5 random_' ) + '''
''' + makeCommandExample( '1000 random_ mean' ),
[ 'random', 'random_integer', 'random_integer_' ] ],

    'result' : [
'special', 'loads the result from the previous invokation of rpn',
'''
'result' currently doesn't work with measurements.
''',
'''
''' + makeCommandExample( '2 sqrt' ) + '''
''' + makeCommandExample( 'result sqr' ),
[ ] ],

    'roll_dice' : [
'special', 'evaluates a dice expression to simulate rolling dice',
'''
This feature simulates dice rolling and can be used to do calculations and
simulations for role-playing games, war games or anything else that uses dice.

The dice syntax is a mini-language whose expressions look like this:

format: [c]dv[,[c]dv]...][x[p]][h[q]][(-+)y]

c - dice count, defaults to 1
v - dice value, i.e., number of sides, minumum 2
p - drop lowest die value(s), defaults to 1
q - drop highest value(s), defaults to 1
y - add or subtract y from the total (modifier)

This is very terse and probably not valid BNF, so here's a breakdown.

First, there are one or more expressions of [c]dv separated by commas
(no spaces are allowed obviously).

c is the optional number of dice, and v describes the number of sides, so '3d6'
means 3 six-sided dice.  '2d6,d8' means 2 six-sided dice and 1 eight-sided die.

You can have as many of these expressions string together as you wish.
''' + makeCommandExample( '3d6 roll_dice', indent=4 ) + '''
''' + makeCommandExample( '2d6,d8 roll_dice', indent=4 ) + '''
''' + makeCommandExample( 'd100 roll_dice', indent=4 ) + '''
''' + makeCommandExample( 'd2,d3,d4,d5,d6,d7,d8 roll_dice', indent=4 ) + '''

Next, you can have two options to control the number of dice dropped by value:

x[p]

'x' means to drop the p lowest valued dice, where p defaults to 1 if it is left
out.

So, '4d6x' or '4d6x1' means: roll 4 six-sided dice and drop the lowest one.

For example, if rpn were to roll 2, 3, 3, and 6, the total would be 12 because
the 2 would be dropped.
''' + makeCommandExample( '4d6x1 roll_dice', indent=4 ) + '''
''' + makeCommandExample( '12d6x9 roll_dice', indent=4 ) + '''
h[q]

'h' means to drop the q highest valued dice, where q defaults to 1 if it is left
out.

So, '4d6h' or '4d6h1' means: roll 4 six-sided dice and drop the highest one.

For example, if rpn were to roll 1, 2, 4, and 5, the total would be 7 because
the 5 would be dropped.
''' + makeCommandExample( '4d6h1 roll_dice', indent=4 ) + '''
''' + makeCommandExample( '12d6h9 roll_dice', indent=4 ) + '''
Of course, you can combine 'x' and 'h':
''' + makeCommandExample( '10d8x3h3 roll_dice', indent=4 ) + '''
''' + makeCommandExample( '5d6xh roll_dice', indent=4 ) + '''
''' + makeCommandExample( '10d4x5h4 roll_dice', indent=4 ) + '''
Finally, you can optionally add or subtract a fixed amount to the result:
''' + makeCommandExample( '3d6+4 roll_dice', indent=4 ) + '''
''' + makeCommandExample( '2d4-2 roll_dice', indent=4 ) + '''
And obviously, this can result in a negative value.
''',
'''
''' + makeCommandExample( '3d6 roll_dice' ) + '''
''' + makeCommandExample( '4d8,3d10 roll_dice' ) + '''
''' + makeCommandExample( '2d4,2d6x1 roll_dice' ) + '''
''' + makeCommandExample( '2d4+2 roll_dice' ) + '''
''' + makeCommandExample( '4d6x1-3 roll_dice' ) + '''
''' + makeCommandExample( '2d4,4d6,8d10 roll_dice' ),
[ 'roll_dice', 'roll_simple_dice', 'permute_dice', 'enumerate_dice', 'enumerate_dice_' ] ],

    'roll_dice_' : [
'special', 'evaluates a dice expression to simulate rolling dice k times',
'''
Please see 'roll_dice' for an explanation of the dice expression language.
''',
'''
''' + makeCommandExample( '2d6 10 roll_dice_' ) + '''
''' + makeCommandExample( '4d6x1 6 roll_dice_' ),
[ 'roll_dice', 'permute_dice', 'enumerate_dice', 'enumerate_dice_' ] ],

    'roll_simple_dice' : [
'special', 'rolls n dice with k sides each',
'''
''',
'''
''' + makeCommandExample( '3 6 roll_simple_dice' ) + '''
''' + makeCommandExample( '4 random_int 4 roll_simple_dice' ),
[ 'roll_dice' ] ],

    'set_config' : [
'special', 'set configuration setting n with value k',
'''
Since rpn has lots of argument-parsing rules, prepending a single-quote (') to
the argument tells rpn to bypass all the parsing and just treat the argument as
a string.

There are currently only two configuration settings supported:

'yafu_binary' - the YAFU executable name.
'yafu_path' - the location of the YAFU executable.
''',
'''
''',
[ 'delete_config', 'dump_config', 'get_config' ] ],

    'set_variable' : [
'special', 'set the value k for key n in the user config file',
'''
These values can be accessed via the 'get_variable' operator, but they
can be more conveniently accessed with the '$' prefix.
''',
'''
''' + makeCommandExample( 'magic_number 37 set_variable' ) + '''
''' + makeCommandExample( 'magic_number get_variable' ) + '''
''' + makeCommandExample( '$magic_number' ) + '''
''' + makeCommandExample( 'my_location "Leesburg, VA" set_variable' ) + '''
''' + makeCommandExample( '$my_location today sunrise' ),
[ 'get_variable' ] ],

    'topic' : [
'special', 'prints a help topic in interactive mode',
'''
''',
'''
''',
[ 'help', 'topics' ] ],

    'topics' : [
'special', 'prints a list of help topics in help mode',
'''
''',
'''
''',
[ 'help', 'topic' ] ],

    'uuid' : [
'special', 'generates a UUID',
'''
The UUID is generated using the host ID (MAC address if possible, otherwise
see RFC 4122) and the current time.
''',
'''
''' + makeCommandExample( 'uuid' ),
[ 'uuid_random' ] ],

    'uuid_random' : [
'special', 'generates a random UUID',
'''
The UUID is generated completely randomly.
''',
'''
''' + makeCommandExample( 'uuid_random' ),
[ 'uuid' ] ],

    'value' : [
'special', 'converts a measurement to a numerical value',
'''
If a value as the result of evaluation is a measurement, i.e., contains a unit
of measurement, then this operator will evaluate that value as a number, the
numerical part of the measurement value.
''',
'''
''' + makeCommandExample( '1000 light-years value' ) + '''
''' + makeCommandExample( '100 years seconds convert value' ) + '''
''' + makeCommandExample( '2 pounds value 3 gallons value +' ) + '''
Koide's Constant... is it really 2/3?
(see https://www.johndcook.com/blog/2018/09/11/koide/)

''' + makeCommandExample( '[ electron_mass value muon_mass value tau_mass value ] sum [ electron_mass value sqrt muon_mass value sqrt tau_mass value sqrt ] sum sqr /' ),
[ ] ],


# //******************************************************************************
# //
# //  trigonometry operators
# //
# //******************************************************************************

    'acos' : [
'trigonometry', 'calculates the arccosine of n',
'''
The arcosine is the inverse of cosine.  In other words, if cos( x ) = y, then
acos( y ) = x.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '0 acos' ) + '''
''' + makeCommandExample( '0.5 acos radians deg convert' ) + '''
''' + makeCommandExample( '0.234 acos cos' ) + '''
''' + makeCommandExample( '45 degrees cos acos radians degrees convert' ),
[ 'cos', 'acosh', 'asin', 'atan' ] ],

    'acosh' : [
'trigonometry', 'calculates the hyperbolic arccosine of n',
'''
The hyperbolic arccosine is the inverse of the hyperbolic cosine.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '0 acosh' ) + '''
''' + makeCommandExample( '0.234 acosh cosh' ) + '''
''' + makeCommandExample( '45 degrees cosh acosh radians degrees convert' ),
[ ] ],

    'acot' : [
'trigonometry', 'calcuates the arccotangent of n',
'''
The arccotangent is the inverse of the cotangent.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'cot', 'acoth', 'acsc', 'asec' ] ],

    'acoth' : [
'trigonometry', 'calculates the hyperbolic arccotangent of n',
'''
The hyperbolic arccotangent is the inverse of the hyperbolic cotangent.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'acot', 'coth', 'acsch', 'asech' ] ],

    'acsc' : [
'trigonometry', 'calculates the arccosecant of n',
'''
The arccosecant is the inverse of the cosecant.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'csc', 'asec', 'acsch', 'acot' ] ],

    'acsch' : [
'trigonometry', 'calculates the hyperbolic arccosecant of n',
'''
The hyperbolic arccosecant is the inverse of the hyperbolic cosecant.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'csch', 'acsc', 'acoth', 'asech' ] ],

    'asec' : [
'trigonometry', 'calculates the arcsecant of n',
'''
The arcsecant is the inverse of the secant.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'sec', 'asech', 'acsc', 'acot' ] ],

    'asech' : [
'trigonometry', 'calculates the hyperbolic arcsecant of n',
'''
The hyperbolic arcsecant is the inverse of the hyperbolic secant.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'sech', 'acsch', 'asec', 'acoth' ] ],

    'asin' : [
'trigonometry', 'calculates the arcsine of n',
'''
The arcsine is the inverse of sine.  In other words, if sin( x ) = y, then
asin( y ) = x.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '0.5 asin' ) + '''
''' + makeCommandExample( '0.345 asin sin' ) + '''
''' + makeCommandExample( '0.75 sqrt asin radian deg convert' ) + '''
''' + makeCommandExample( '2 sqrt 1/x asin radian deg convert' ),
[ 'sin', 'acos', 'atan', 'asinh' ] ],

    'asinh' : [
'trigonometry', 'calculates the hyperbolic arcsine of n',
'''
The hyperbolic arcsine is the inverse of the hyperbolic sine.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '0.5 asinh' ) + '''
''' + makeCommandExample( '0.345 asinh sinh' ) + '''
''' + makeCommandExample( '0.75 sqrt asinh radian deg convert' ) + '''
''' + makeCommandExample( '2 sqrt 1/x asinh radian deg convert' ),
[ 'asin', 'sinh', 'acosh', 'atanh' ] ],

    'atan' : [
'trigonometry', 'calculates the arctangent of n',
'''
The arctangent is the inverse of tangent.  In other words, if tan( x ) = y, then
atan( y ) = x.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '3 atan' ) + '''
''' + makeCommandExample( '1 atan radians deg convert' ) + '''
''' + makeCommandExample( '5.612 atan tan' ) + '''
''' + makeCommandExample( '10 atan radians deg convert' ) + '''
''' + makeCommandExample( '89 degrees tan atan radians deg convert' ),
[ 'atanh', 'tan', 'acos', 'asin' ] ],

    'atanh' : [
'trigonometry', 'calculates the hyperbolic arctangent of n',
'''
The hyperbolic arctangent is the inverse of the hyperbolic tangent.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '3 atanh' ) + '''
''' + makeCommandExample( '0.5 atanh radians deg convert' ) + '''
''' + makeCommandExample( '5.612 atanh tan' ) + '''
''' + makeCommandExample( '89 degrees tanh atanh radians deg convert' ),
[ 'tanh', 'atan', 'acosh', 'asinh' ] ],

    'cos' : [
'trigonometry', 'calculates the cosine of n',
'''
The cosine of an angle is the ratio of the length of the adjacent side to the
length of the hypotenuse.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( 'pi 2 / cos' ) + '''
''' + makeCommandExample( '60 degrees cos' ),
[ 'sin', 'tan', 'acos', 'cosh' ] ],

    'cosh' : [
'trigonometry', 'calculates the hyperbolic cosine of n',
'''
The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'cos', 'acosh', 'sinh', 'tanh' ] ],

    'cot' : [
'trigonometry', 'calculates the cotangent of n',
'''
The cotangent cot( n ) is the reciprocal of tan( n ); i.e., the ratio of the
length of the adjacent side to the length of the opposite side.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'coth', 'acot', 'sec', 'csc' ] ],

    'coth' : [
'trigonometry', 'calculates the hyperbolic cotangent of n',
'''
The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'cot', 'acoth', 'csch', 'sech' ] ],

    'csc' : [
'trigonometry', 'calculates the cosecant of n',
'''
The cosecant function is defined to be the reciprocal of the sine function.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '36 degrees csc', indent=4 ) + '''
Comparing csc to sin:
''' + makeCommandExample( '36 degrees csc 1/x', indent=4 ) + '''
''' + makeCommandExample( '36 degrees sin', indent=4 ),
[ 'csch', 'acsc', 'sec', 'cot' ] ],

    'csch' : [
'trigonometry', 'calculates hyperbolic cosecant of n',
'''

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'csc', 'sech', 'acsch', 'coth' ] ],

    'sec' : [
'trigonometry', 'calculates the secant of n',
'''

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'csc', 'sech', 'asec', 'cot' ] ],

    'sech' : [
'trigonometry', 'calculates the hyperbolic secant of n',
'''

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'sec', 'asech', 'csch', 'coth' ] ],

    'sin' : [
'trigonometry', 'calculates the sine of n',
'''
The sine of an angle is the ratio of the length of the opposite side to the
length of the hypotenuse.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '60 degrees sin' ) + '''
''' + makeCommandExample( 'pi 2 / sin' ) + '''
''' + makeCommandExample( '0 sin' ),
[ 'asin', 'cos', 'tan', 'sinh' ] ],

    'sinh' : [
'trigonometry', 'calculates the hyperbolic sine of n',
'''

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'asinh', 'cosh', 'tanh', 'sin' ] ],

    'tan' : [
'trigonometry', 'calculates the tangent of n',
'''
The tangent of an angle is the ratio of the length of the opposite side to the
length of the adjacent side.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '30 degrees tan' ) + '''
''' + makeCommandExample( 'pi 4 / tan' ) + '''
''' + makeCommandExample( '127 degrees tan' ),
[ 'tanh', 'atan', 'sin', 'cos' ] ],

    'tanh' : [
'trigonometry', 'calculates the hyperbolic tangent of n',
'''

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''',
[ 'tan', 'atanh', 'cosh', 'sinh' ] ],

}


# //******************************************************************************
# //
# //  makeHelp
# //
# //******************************************************************************

def makeHelp( helpTopics ):
    '''Builds the help data file.'''
    fileName = getDataPath( ) + os.sep + 'help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( helpTopics, pickleFile )
        pickle.dump( operatorHelp, pickleFile )

    print( )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    primeFile = Path( getDataPath( ) + os.sep + 'small_primes.cache' )

    if not primeFile.is_file( ):
        print( 'Please run "prepareRPNPrimeData" to initialize the prime number data files.' )
        sys.exit( 0 )

    unitsFile = Path( getDataPath( ) + os.sep + 'units.pckl.bz2' )

    if not unitsFile.is_file( ):
        print( 'Please run "makeRPNUnits" to initialize the unit conversion data files.' )
        sys.exit( 0 )

    makeHelp( helpTopics )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

