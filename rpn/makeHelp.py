#!/usr/bin/env python

#******************************************************************************
#
#  makeHelp
#
#  rpnChilada help file generator
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  *** NOTE:  Don't run this file directly.  Use ../makeHelp.py.
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import shlex

import argparse
import bz2
import contextlib
import io
from pathlib import Path
import pickle
import os
import sys
import time

from rpn.rpn import rpn, handleOutput
from rpn.rpnOutput import printParagraph
from rpn.rpnPrimeUtils import checkForPrimeData
from rpn.rpnUtils import getUserDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE, \
                           PROGRAM_NAME, RPN_PROGRAM_NAME

import rpn.rpnGlobals as g

if not hasattr( time, 'time_ns' ):
    from rpn.rpnNanoseconds import time_ns
else:
    from time import time_ns

g.checkForSingleResults = True
g.lineLength = 80


#******************************************************************************
#
#  constants and start-up code
#
#******************************************************************************

PROGRAM_NAME = 'makeHelp'
PROGRAM_DESCRIPTION = 'rpnChilada help generator'

MAX_EXAMPLE_COUNT = 2007

os.chdir( getUserDataPath( ) )    # SkyField doesn't like running in the root directory

startTime = time_ns( )

print( 'makeHelp' + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION )
print( COPYRIGHT_MESSAGE )
print( )

checkForPrimeData( )

if not g.primeDataAvailable:
    sys.stderr.write( 'The prime number data cache is not available.\n' )
    sys.stderr.write( 'Please see https://github.com/ConceptJunkie/rpndata/ for more details.\n\n' )

parser = argparse.ArgumentParser( prog = PROGRAM_NAME, description = RPN_PROGRAM_NAME + ' - ' +
                                  PROGRAM_DESCRIPTION + COPYRIGHT_MESSAGE, add_help = False,
                                  formatter_class = argparse.RawTextHelpFormatter,
                                  prefix_chars = '-' )

parser.add_argument( '-d', '--debug', action = 'store_true' )

args = parser.parse_args( sys.argv[ 1 : ] )

HELP_DEBUG_MODE = args.debug

EXAMPLE_COUNT = 0


#******************************************************************************
#
#  makeCommandExample
#
#******************************************************************************

def makeCommandExample( command, indent=0, slow=False ):
    '''
    You know, it didn't occur to me for years that I should make the help
    actually use rpn to run the examples.  This way, when things change,
    the output is always accurate.
    '''
    global EXAMPLE_COUNT
    EXAMPLE_COUNT += 1

    if not command:
        return ''

    # This total count needs to be manually updated when the help examples are modified.
    global MAX_EXAMPLE_COUNT
    #print( command )
    print( '\rGenerating example: ', EXAMPLE_COUNT, 'of', MAX_EXAMPLE_COUNT, end='' )
    #print( )

    if slow:
        print( '  (please be patient...)', end='', flush=True )

    output = io.StringIO( )

    global HELP_DEBUG_MODE
    if HELP_DEBUG_MODE:
        print( )
        print( command )

    print( ' ' * indent + 'c:\\>rpn ' + command, file=output )

    handleOutput( rpn( shlex.split( command.replace( '\\', '\\\\' ) ) ), indent=indent, file=output )

    if slow:
        print( '\r', ' ' * 55, end='' )

    result = output.getvalue( )
    output.close( )

    return result


#******************************************************************************
#
#  basic help categories
#
#******************************************************************************

#    -e, --profile
#        gather performance statistics
#


helpTopics = {
    # pylint: disable=bad-continuation
    'options' :
    'rpn' + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION + '\n' +
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
         ignore cached results, recalculates values, then updates cache

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
''' + makeCommandExample( '0x10', indent=4 ) + '''
A number consisting solely of 0s and 1s with a trailing 'b' or 'B' is
interpreted as binary.
''' + makeCommandExample( '101b', indent=4 ) + '''
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
''' + makeCommandExample( '-t [d:5] build_numbers lambda 1 x add_digits x 1 add_digits / 1 3 / is_equal filter',
                          indent=4, slow=True ) + '''
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
''' + makeCommandExample( 'usb1 kilobit/second convert', indent=4 ) + '''
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
''' + makeCommandExample( '[ 24 hours sqr G earth_mass ] prod 4 pi sqr * / cube_root miles convert earth_radius -',
                          indent=4 ) + '''
Or better yet, there's now an operator for that:
''' + makeCommandExample( '24 hours earth_mass orbital_radius earth_radius - miles convert', 4 ) + '''
I've tried to make the unit conversion flexible and smart.
''' + makeCommandExample( '16800 mA hours * 5 volts * joule convert', indent=4 ) + '''
''' + makeCommandExample( 'gigaparsec barn * cubic_inches convert', indent=4 ) + '''
''' + makeCommandExample( 'cubic_inch gigaparsec barn * convert', indent=4 ) + '''
''' + makeCommandExample( 'watt ohm / sqrt', indent=4 ) + '''
    ''',
    'interactive_mode' :
    '''
Interactive mode is a new feature introduced with version 6.  If rpn is
launched with no expressions, then it will start an interactive prompt that
allows the user to enter successive expressions for evaluation.

Interactive mode also introduces some new operators.  Each expression that is
evaluated is given a successive number:

c:\\>rpn
rpnChilada 8.4.0 - RPN command-line calculator
copyright (c) 2020 (1988), Rick Gutleber (rickg@his.com)

Type "help" for more information, and "exit" to exit.
rpn (1)> 2 3 +
5
rpn (2)> 10 sqrt
3.162277660168

These numbers can be used to refer to previous results by prepending the
result number with '$':

rpn (3)> $1 5 +
10
rpn (4)> $2 sqr
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

input_radix:  This sets the radix that rpn will use to interpret input values.

integer_grouping:  This specifies the number of digits in a group when printing
an integer

leading_zero:

leading_zero_mode:  Aliased to '-z'.

octal_mode:  Aliased to '-o'.

output_radix:

precision:

The precision will not be set lower than the accuracy + 2.

timer:  The timer function prints out the time taken for each operation.

timer_mode:  Turns on the timer for the next operation.  Aliased to '-t'.
    ''',
    'about' :
    PROGRAM_NAME + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION + '\n' +
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

'$varname' syntax doesn't work in interactive mode!

Using 'for_each' on a nested list should give a nice error message.

'rpn [ 1 2 3 ] lambda x 2 + for_each' crashes.  I'm not sure why it crashes,
and I'm not even sure what it should do.

-i doesn't work for lists.

'(' and ')' (multiple operators) don't work with generators because the
generator only works once.   The structure of the evaluator won't allow me to
fix this, I think..  It may have to wait until I convert all rpn expressions to
Python before this can be fixed.

'collate' does not work with generators.

Chained calls to 'next_new_moon' give the same answer over and over.  Other
related operators probably do the same thing.

-d needs to parse out the scientific notation part of the value

Converting negative numbers to different bases gives weird answers.

-u doesn't work with complex numbers

'result' doesn't work with measurements.

Date comparisons before the epoch (1970-01-01) don't work.  It seems to be a
limitation of the Arrow class.

User-defined functions can't include measurements.

"rpn 1 1 4 range range 10 15 range 1 3 range range2" crashes because
operators that take more than 2 arguments don't handle recursive list
arguments.

'reversal_addition' doesn't work with generators.

See 'rpn help TODO'.
    ''',
    'TODO' :
    '''
This is my informal, short-term todo list for rpn.  It often grows and seldom
gets smaller.

*  'humanize' - like 'name' but only 2 significant digits when > 1000

*  'name' should handle fractions smaller than 1 gracefully (right now it
   prints nothing)

*  support date comparisons, etc. before the epoch (Arrow doesn't work before
   the epoch apparently!)

*  create an output handler for RPNLocation

*  'result' doesn't work with measurements

*  https://en.wikipedia.org/wiki/American_wire_gauge

*  'mean' should work with measurements

*  units aren't supported in user-defined functions

*  http://stackoverflow.com/questions/14698104/how-to-predict-tides-using-harmonic-constants

*  OEIS comment text occasionally contains non-ASCII characters, and rpn chokes
   on that

*  'fraction' needs to figure out what precision is needed and set it itself

Long-term goals

*  The biggest change I want to do is completely rewrite parsing and evaluating.
   I want the parser to generate Python code, then the evaluator can simply go
   away, because Python will do it for us!   The current parsing logic has been
   extended beyond all reasonableness.  It's excessively complex has lots of
   edge cases where it breaks down.

*  Performance, performance, performance.  There's a lot of functionality in
   rpn which is way too slow.

*  Converting to using numpy arrays instead of lists should improve performance.

*  I would love to support nested lambdas, but this won't happen until the
   parser is redesigned.

*  Turn rpn into a full-blown scripting language.  It's 2/3 of the way there.
   Why not go all the way?  Once the parser generates Python, I think I'll be
   90% of the way there.

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

The operators 'double_balanced_prime', double_balanced_prime_',
'triple_balanced_prime', and 'triple_balanced_prime' now work correctly.  The
data files have been significantly expanded as well.

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

Added the 'lat_long_to_nac' operator.

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

7.2.1

Unit conversion is now a lot smarter because the automatically-generated area
and volume units are generated more intelligently.  This means expressions
using the "square" and "cubic" units will convert automatically and you won't
end up with something like "foot^2/square_mile".

...and yes, a few bug fixes.

7.2.2

A big change that doesn't affect functionality is that the prime number data
now resides in a separate package called rpnChiladaData.  This data rarely
changes so there's no reason to download it.

A major bug was uncovered after almost a year.  rpnChilada thought there were
51920.97 seconds in a day because of a typo.  This has been fixed, and I
figured out how to detect other similar problems if they exist.  This change
will be implemented in the next few days.

7.2.3

I messed up the upload for 7.2.2.  No code changes, just fixed packaging.

7.2.4

Just a bunch of fixes.  makeUnits has been improved a bit, and I've validated
that all conversions exist, and are consistent.

7.2.5

I fat-fingered an addition to the requirements.txt file.  :-/

8.0.0

The unit conversion code has been heavily refactored and works much better now.

Added the 'base_units' and 'dimensions' operators, mostly for testing purposes.

Added '_dump_conversions' and '_dump_cache', also for testing purposes.

rpnChilada is now smart enough to recognize when an OEIS request has failed,
and to ignore the cached result stored as a result.  If it detects that the
cached value is empty, it will perform the request again and recache the
result.

Help now supports units and constant operators after way too long.  Filling in
the help info for the units and constant operators, along with all the existing
help info that's missing, will take a while, and is continuing.

rpnChilada has officially dropped Python 2 support.  I rarely tested it anyway.

Added 'wind_chill' and 'heat_index' operators.

The unit tests now confirm that aliases do not collide with other reserved
words.  The alias creation for generated types has also been cleaned up.

The astronomy functionality has been refactored to support migrating to the
skyfield library from pyephem.

Removed the 'break_on' operator because it no longer works.  It will be
re-implemented in the future.

Added 'to_ethiopian', 'to_ethiopian_name' and 'from_ethiopian' operators for
converting to and from the Ethiopian calendar.

Added more unit tests and the usual bug fixes.

8.1.0

Added the 'get_partitions', 'nth_linear_recurrence' and
'nth_linear_recurrence_with_modulo' operators.

Added 'black_hole_surface_tides' now that I understand it.  I also added a more
general 'tidal_force' operator.

Added 'is_harmonic_divisor_number', 'is_antiharmonic', 'harmonic_fraction',
'alternating_harmonic_fraction', 'harmonic_residue', 'harmonic_mean',
and 'antiharmonic_mean' operators.

Added 'hyperoperator' and 'hyperoperator_right' operators.

Added 'root_mean_square', 'stirling1', 'stirling2', 'ackermann',
'square_super_root', 'cube_super_root' and 'super_root' operators.

Added 'filter_integers', 'filter_on_flags', 'is_k_perfect', 'phitorial', and
'relatively_prime' operators.

If the OEIS text file for a particular sequence has a last line that doesn't
end with a linefeed, rpn now parses out the last value correctly, instead of
missing it completely.

Finally, after many years complex numbers are also formatted according to the
same rules for formatting regular real numbers.

rpnChilada also finally recognizes the Python syntax for imaginary numbers of
"99.99999j", i.e., any regular number appended with a 'j'.   The 'i' operator
remains, but can be considered deprecated, as it is no longer needed.

Added more unit tests and the usual bug fixes.

More help text has been filled in.

8.1.1

As usual, I messed up something with the release and have to fix it.

8.2.0

Added the 'is_pernicious' operator.

Added the 'pythagorean_triples' and 'get_partitions_with_limit' operators.

Added the '_dump_prime_cache' operator.

Added 'filter_max' and 'filter_min' which are shortcuts for much wordier lambda
constructions.

Added 'polygonal_pyramidal' and 'polygorial' operators.

The unit test suite has been streamlined so that it runs faster, since it's
used so much.  Added the -t argument to time individual tests.  Added the -f
argument to allow filtering which tests will be run (based on a text filter).

A number of bug fixes and improvements have been made to the prime number
functions and data.

And the usual bug fixes.

8.3.0

The astronomy operators now don't care which order the arguments are in, except
for 'angular_separation', which expects the first two arguments to be
astronomical bodies.

8.4.0

Revamped the prime number operators, and filled in a couple of missing ones.

A number of operator names have changed for more consistency.  The old names
have been added as aliases.

Added the 'bitwise_xnor', 'from_french_republican', 'to_french_republican',
'to_french_republcan_name' operators.

A fix was made to support using rpn on OS X.

A number of bugs were fixed, and I did extensive touch-ups based on pylint.
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
    center of the Milky Way, to the density of gold:
''' + makeCommandExample( '4.3 million solar_mass 4.3 million solar_mass black_hole_radius sphere_volume / '
                          'Gold element_density /', indent=8 ) + '''

Advanced examples:

Calculation (or approximation) of various mathematical constants:

    Polya Random Walk Constant
''' + makeCommandExample( '-p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 / gamma 7 24 / '
                          'gamma 11 24 / gamma ] prod 1/x * -', indent=8, slow=True ) + '''
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
''' + makeCommandExample( '-a20 0 inf lambda 2 x 2 * 1 + power x 2 * 1 + * 1/x nsum 0 inf '
                          'lambda 3 x 2 * 1 + power x 2 * 1 + * 1/x nsum /', indent=8 ) + '''
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
''' + makeCommandExample( '-a20 [ 1j 1000 dup ] power_tower2', indent=8 ) + '''
    Cahen's Constant
''' + makeCommandExample( '1 inf lambda x nth_sylvester 1 - 1/x -1 x 1 + ** * nsum', indent=8 ) + '''
    Erdos-Borwein Constant
''' + makeCommandExample( '1 inf lambda 2 x ** 1 - 1/x nsum', indent=8 ) + '''
    An approximation of the Heath-Brown-Moroz constant
''' + makeCommandExample( '-a6 1 60000 primes lambda 1 x 1/x - 7 ** 1 7 x * 1 + x sqr / + * eval prod',
                          indent=8, slow=True ) + '''
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
''' + makeCommandExample( '-a80 [ 1, 0, -1, -2, -1, 2, 2, 1, -1, -1, -1, -1, -1, 2, 5, 3, -2, -10, -3, -2, 6, 6, '
                          '1, 9, -3, -7, -8, -8, 10, 6, 8, -5, -12, 7, -7, 7, 1, -3, 10, 1, -6, -2, -10, -3, 2, 9, '
                          '-3, 14, -8, 0, -7, 9, 3, -4, -10, -7, 12, 7, 2, -12, -4, -2, 5, 0, 1, -7, 7, -4, 12, -6, '
                          '3, -6 ] solve real max', indent=8, slow=True ) + '''
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


#******************************************************************************
#
#  operator help
#
#******************************************************************************

operatorHelp = {
    # pylint: disable=bad-continuation line-too-long
    #******************************************************************************
    #
    #  algebra operators
    #
    #******************************************************************************

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

Ref:  https://en.wikipedia.org/wiki/Discriminant
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
[ 'add_polynomials', 'find_polynomial', 'multiply_polynomials', 'polynomial_power' ] ],

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
[ 'add_polynomials', 'eval_polynomial', 'multiply_polynomials', 'polynomial_product' ] ],

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
[ 'add_polynomials', 'eval_polynomial', 'multiply_polynomials', 'polynomial_power' ] ],

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
[ 'add_polynomials', 'multiply_polynomials', 'polynomial_power' ] ],

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


    #******************************************************************************
    #
    #  arithmetic operators
    #
    #******************************************************************************

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

    'antiharmonic_mean' : [
'arithmetic', 'calculates the antiharmonic mean of a a list of numbers n',
'''
The antiharmonic mean of a set of positive numbers is defined as the arithmetic
mean of the squares of the numbers divided by the arithmetic mean of the
numbers.

Ref:  https://en.wikipedia.org/wiki/Contraharmonic_mean
''',
'''
''' + makeCommandExample( '[ 1 2 3 4 6 8 ] antiharmonic_mean' ) + '''
''' + makeCommandExample( '[ 1 15 range ] antiharmonic_mean' ) + '''
Calculate the antiharmonic mean of the first n numbers from 1 to 7:
''' + makeCommandExample( '[ 1 1 7 range range ] antiharmonic_mean' ),
[ 'mean', 'agm', 'geometric_mean', 'root_mean_square', 'harmonic_mean' ] ],

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
''' + makeCommandExample( '5.1 3.4j +' ),
[ 'floor', 'nearest_int', 'mantissa', 'round' ] ],

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

Division is supported for measurements.  If two measurements with the same
units are divided, the result will be a number, since the units cancel.
''',
'''
''' + makeCommandExample( '1440 24 /' ) + '''
''' + makeCommandExample( '2520 1 10 range /' ) + '''
''' + makeCommandExample( 'miles hour / furlongs fortnight / convert' ) + '''
How long would 4 AA batteries power a Raspberry Pi 4, which draws 7 watts?
''' + makeCommandExample( '4 aa_battery 7 watts / hms', indent=4 ),
[ 'multiply', 'add', 'subtract', 'reciprocal' ] ],

    'equals_one_of' : [
'arithmetic', 'returns 1 if n equals any value in the list k, otherwise returns 0',
'''
This operator returns 1 if n equals any element in the list k, otherwise it
returns 0.

This operator is a shortcut which is equivalent to 'n k equals or_all'
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
''' + makeCommandExample( '-2.5 5.7j + floor' ),
[ 'ceiling', 'round', 'nearest_int', 'mantissa' ] ],

    'gcd' : [
'arithmetic', 'calculates the greatest common denominator of elements in list n',
'''
The greatest common denominator is the largest number which is a common divisor
of every element in list n.  If numbers are relatively prime, then their
greatest common divisor is 1.
''',
'''
''' + makeCommandExample( '[ 5 10 20 ] gcd' ) + '''
''' + makeCommandExample( '[ 27 64 ] gcd' ) + '''
''' + makeCommandExample( '[ 3150 8820 ] gcd' ),
[ 'reduce', 'lcm', 'gcd2', 'relatively_prime' ] ],

    'gcd2' : [
'arithmetic', 'calculates the greatest common denominator of n and k',
'''
'n k gcd2' is equivalent to '[ n k ] gcd'
''',
'''
''' + makeCommandExample( '5 20 gcd2' ) + '''
''' + makeCommandExample( '3150 8820 gcd2' ),
[ 'reduce', 'lcm', 'gcd', 'relatively_prime' ] ],

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
[ 'mean', 'agm', 'harmonic_mean', 'root_mean_square' ] ],

    'harmonic_mean' : [
'arithmetic', 'calculates the harmonic mean of a a list of numbers n',
'''
The harmonic mean (sometimes called the subcontrary mean) is one of
several kinds of average, and in particular one of the Pythagorean
means.  Typically, it is appropriate for situations when the average of
rates is desired.

The harmonic mean can be expressed as the reciprocal of the arithmetic mean
of the reciprocals of the given set of observations.

Ref:  https://en.wikipedia.org/wiki/Harmonic_mean
''',
'''
''' + makeCommandExample( '[ 1 2 4 ] harmonic_mean' ) + '''
''' + makeCommandExample( '[ 1 10 range ] harmonic_mean' ) + '''
Calculate the harmonic mean of the first n numbers from 1 to 7:
''' + makeCommandExample( '[ 1 1 7 range range ] harmonic_mean' ),
[ 'mean', 'agm', 'geometric_mean', 'root_mean_square', 'antiharmonic_mean', 'is_harmonic_divisor_number' ] ],

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
[ 'is_equal', 'is_even', 'is_odd' ] ],

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
'is_integer' requires a real argument.
''',
'''
''' + makeCommandExample( 'pi is_integer' ) + '''
''' + makeCommandExample( '1 is_integer' ) + '''
''' + makeCommandExample( '3.1 is_integer' ),
[ 'is_even', 'is_odd', 'nearest_int' ] ],

    'is_kth_power' : [
'arithmetic', 'returns 1 if n is a perfect kth power, otherwise returns 0',
'''
'is_kth_power' also works with complex numbers.
''',
'''
''' + makeCommandExample( '16 4 is_kth_power' ) + '''
''' + makeCommandExample( '32 5 is_kth_power' ) + '''
''' + makeCommandExample( '2j 3 + 5 ** 5 is_kth_power' ),
[ 'is_square', 'is_power_of_k' ] ],

    'is_less' : [
'arithmetic', 'returns 1 if n is less than k, otherwise returns 0',
'''
'is_less' requires a real argument.
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
This is the equivalent of 'is_equal not'.
''',
'''
''' + makeCommandExample( '0 1 is_not_equal' ) + '''
''' + makeCommandExample( '1 0 is_not_equal' ) + '''
''' + makeCommandExample( '1 1 is_not_equal' ),
[ 'is_equal', 'is_less', 'is_greater' ] ],

    'is_not_greater' : [
'arithmetic', 'returns 1 if n is not greater than k, otherwise returns 0',
'''
'is_not_greater' is the equivalent of less than or equal.

'is_not_greater' requires a real argument.
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
'is_not_less' is the equivalent of greater than or equal.

'is_not_less' requires a real argument.
''',
'''
''' + makeCommandExample( '0 1 is_not_less' ) + '''
''' + makeCommandExample( '1 0 is_not_less' ) + '''
''' + makeCommandExample( '1 1 is_not_less' ) + '''
''' + makeCommandExample( '3 5 ** 5 3 ** is_not_less' ),
[ 'is_less', 'is_not_greater' ] ],

    'is_not_zero' : [
'arithmetic', 'returns 1 if n is not zero, otherwise returns 0',
'''
This is simply a check for a non-zero value.

The operator is primarily useful in lambdas.  It is actually identical to
'not not'.
''',
'''
''' + makeCommandExample( '1 is_not_zero' ) + '''
''' + makeCommandExample( '0 is_not_zero' ),
[ 'is_zero', 'is_odd', 'is_even', 'is_not_equal' ] ],

    'is_odd' : [
'arithmetic', 'returns whether n is an odd number',
'''
This operator returns 1 if the argument is an odd integer (i.e., an
integer n such that n % 2 == 1), otherwise it returns 0.

'is_odd' expects a real argument.
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

''' + makeCommandExample( '2j 1 + sqr' ) + '''
''' + makeCommandExample( '-3 4j + is_square' ),
[ 'is_power_of_k', 'is_kth_power' ] ],

    'is_zero' : [
'arithmetic', 'returns 1 if n is zero else 0',
'''
The operator is primarily useful in lambdas.  It is actually idential to the
'not' operator.
''',
'''
''' + makeCommandExample( '0 is_zero' ) + '''
''' + makeCommandExample( '1 is_zero' ) + '''
''' + makeCommandExample( '2j is_zero' ) + '''
''' + makeCommandExample( '0j is_zero' ),
[ 'is_not_zero', 'is_odd', 'is_even', 'is_equal' ] ],

    'larger' : [
'arithmetic', 'returns the larger of n and k',
'''
This operator returns either n or k, according to which has a larger value.
'larger' requires real arguments.
''',
'''
''' + makeCommandExample( '7 8 larger' ) + '''
''' + makeCommandExample( 'pi 3 larger' ) + '''
''' + makeCommandExample( '1 -1 larger' ),
[ 'smaller' ] ],

    'lcm' : [
'arithmetic', 'calculates the least common multiple of elements in list n',
'''
The least common multiple is the smallest number that is an integral multiple
of every element in the list n.
''',
'''
''' + makeCommandExample( '[ 3 6 12 ] lcm' ) + '''
''' + makeCommandExample( '1 20 range lcm' ) + '''
''' + makeCommandExample( '1 5 primes lcm 5 primorial is_equal' ),
[ 'gcd', 'agm', 'lcm2' ] ],

    'lcm2' : [
'arithmetic', 'calculates the least common multiple of n and k',
'''
The least common multiple is the smallest number that is an integral multiple
of n and k.

'n k lcm2' is equivalent to '[ n k ] lcm'.
''',
'''
''' + makeCommandExample( '3 12 lcm2' ) + '''
''' + makeCommandExample( '24 36 lcm2' ),
[ 'gcd', 'agm', 'lcm' ] ],

    'mantissa' : [
'arithmetic', 'returns the decimal part of n',
'''
'mantissa' expects a real argument.
''',
'''
''' + makeCommandExample( 'pi mantissa' ) + '''
''' + makeCommandExample( '-p50 652 sqrt pi * exp mantissa' ),
[ 'floor', 'ceiling', 'nearest_int' ] ],

    'maximum' : [
'arithmetic', 'returns the largest value in list n',
'''
This operator returns the largest value in the input list of values n.

'maximum' requires a list of real arguments.
''',
'''
''' + makeCommandExample( '[ 5 8 2 23 9 ] max' ) + '''
''' + makeCommandExample( '10 1000 random_integers max' ),
[ 'minimum', 'larger', 'is_greater' ] ],

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
[ 'stddev', 'agm', 'geometric_mean', 'harmonic_mean', 'root_mean_square' ] ],

    'minimum' : [
'arithmetic', 'returns the smallest value in list n',
'''
This operator returns the smallest value in the input list of values n.

'minimum' requires a list of real arguments.
''',
'''
''' + makeCommandExample( '[ 5 8 2 23 9 ] min' ) + '''
''' + makeCommandExample( '10 1000 random_integers min' ),
[ 'maximum', 'smaller', 'is_less' ] ],

    'modulo' : [
'arithmetic', 'calculates n modulo k',
'''
'modulo' expects real arguments, but it doesn't require integer arguments.
''',
'''
''' + makeCommandExample( '7 4 modulo' ) + '''
''' + makeCommandExample( '2.6 0.5 modulo' ) + '''
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
This is the equalivent of 'n -1 *'.
''',
'''
''' + makeCommandExample( '1 negative' ) + '''
''' + makeCommandExample( '-1 negative' ) + '''
''' + makeCommandExample( '0 negative' ) + '''
''' + makeCommandExample( '3j negative' ) + '''
''' + makeCommandExample( '-4 5j + negative' ),
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
''' + makeCommandExample( '1.5 nearest_int' ) + '''
''' + makeCommandExample( '3.4j nearest_int' ) + '''
''' + makeCommandExample( '3.4j 5.6 + nearest_int' ),
[ 'round', 'floor', 'ceiling', 'mantissa' ] ],

    'product' : [
'arithmetic', 'calculates the product of values in list n',
'''
When multiplying more than two values, 'product' can be little more accurate
than successive uses of 'multiply'.
''',
'''
''' + makeCommandExample( '[ 2 3 7 12 ] product' ) + '''
How much energy does an average person expend climbing a flight of stairs?
''' + makeCommandExample( '[ 180 pounds 10 feet gee ] product kilocalories convert', indent=4 ) + '''
Calculating a facotrial the hard way:
''' + makeCommandExample( '1 10 range product', indent=4 ) + '''
''' + makeCommandExample( '10 !', indent=4 ) + '''
Calculating the magnetic constant:
''' + makeCommandExample( '[ 4 pi 10 -7 ** joule/ampere^2*meter ] product', indent=4 ),
[ 'multiply', 'sum' ] ],

    'reciprocal' : [
'arithmetic', 'returns the reciprocal of n',
'''
This is the equivalent of '1 n /', which is valid for any real or complex
number, except 0.
''',
'''
''' + makeCommandExample( '2 reciprocal' ) + '''
''' + makeCommandExample( '17 reciprocal' ) + '''
''' + makeCommandExample( '2j reciprocal' ) + '''
''' + makeCommandExample( '12j 13 + reciprocal' ),
[ 'divide' ] ],

    'root_mean_square' : [
'arithmetic', 'calculates the root mean square of values in list n',
'''
The root mean square is defined as the square root of the mean square (the
arithmetic mean of the squares of a set of numbers).  The root mean square is
also known as the quadratic mean and is a particular case of the generalized
mean with exponent.  Root mean square can also be defined for a continuously
varying function in terms of an integral of the squares of the instantaneous
values during a cycle.

For alternating electric current, root mean square is equal to the value of the
direct current that would produce the same average power dissipation in a
resistive load.

In estimation theory, the root mean square error of an estimator is a measure
of the imperfection of the fit of the estimator to the data.

Ref:  https://en.wikipedia.org/wiki/Root_mean_square
''',
'''
''' + makeCommandExample( '10 50 random_integers root_mean_square' ) + '''
''' + makeCommandExample( '1 50 range root_mean_square' ),
[ 'mean', 'agm', 'geometric_mean', 'stddev' ] ],

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
''' + makeCommandExample( '3 4j + sign' ),
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
The standard deviation is a measure that is used to quantify the amount of
variation or dispersion of a set of data values.  A low standard deviation
indicates that the data points tend to be close to the mean (also called the
expected value) of the set, while a high standard deviation indicates that the
data points are spread out over a wider range of values.

The standard deviation of a random variable, statistical population, data set,
or probability distribution is the square root of its variance.  It is
algebraically simpler, though in practice less robust, than the average
absolute deviation.  A useful property of the standard deviation is that,
unlike the variance, it is expressed in the same units as the data.

Ref:  https://en.wikipedia.org/wiki/Standard_deviation
''',
'''
''' + makeCommandExample( '10 50 random_integers stddev' ) + '''
''' + makeCommandExample( '1 50 range count_div stddev' ),
[ 'mean', 'agm', 'geometric_mean', 'root_mean_square' ] ],

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

When adding more than two values, 'sum' can be a little more accurate
than successive uses of 'add'.
''',
'''
''' + makeCommandExample( '[ 5 8 3 ] sum' ) + '''
''' + makeCommandExample( '1 100 range sum' ) + '''
''' + makeCommandExample( '[ 3 cups 21 teaspoons 7 tablespoons 1.5 deciliters ] sum' ),
[ 'add', 'product' ] ],


    #******************************************************************************
    #
    #  astronomical_object operators
    #
    #******************************************************************************

    'jupiter' : [
'astronomical_objects', 'the planet Jupiter',
'''
This operator represents the planet Jupiter for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'jupiter "Stuttgart, Germany" 2020-01-01 next_rising' ),
[ 'mars', 'saturn' ] ],

    'mars' : [
'astronomical_objects', 'the plenet Mars',
'''
This operator represents the planet Mars for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'mars "San Francisco, California" 2019-05-23 next_setting' ),
[ 'venus', 'jupiter' ] ],

    'mercury' : [
'astronomical_objects', 'the planet Mercury',
'''
This operator represents the planet Mercury for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'mercury "Helsinki, Finland" 2019-04-28 transit_time' ),
[ 'venus', 'mars' ] ],

    'moon' : [
'astronomical_objects', 'the Moon',
'''
This operator represents the Moon for astronomical operators that require an
astronomical object.
''',
'''
''' + makeCommandExample( 'moon "Leesburg, VA" "2019-05-10 11:00:00" sky_location' ),
[ 'venus', 'mars' ] ],

    'neptune' : [
'astronomical_objects', 'the plent Neptune',
'''
This operator represents the planet Neptune for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'neptune "Sao Paulo, Brazil" 2019-05-23 previous_rising' ),
[ 'uranus', 'pluto'  ] ],

    'pluto' : [
'astronomical_objects', 'the planet Pluto',
'''
This operator represents the planet Pluto for astronomical operators that
require an astronomical object.
Yes, I still consider Pluto a planet.  Talk to the hand.
''',
'''
''' + makeCommandExample( 'pluto "2019-05-09 09:23:00" distance_from_earth miles convert -c' ),
[ 'uranus', 'neptune' ] ],

    'saturn' : [
'astronomical_objects', 'the planet Saturn',
'''
This operator represents the planet Saturn for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'saturn now distance_from_earth c / hms' ),
[ 'jupiter', 'uranus' ] ],

    'sun' : [
'astronomical_objects', 'the Sun',
'''
This operator represents the Sun for astronomical operators that require an
astronomical object.
''',
'''
''' + makeCommandExample( 'sun "Richmond, VA" "2019-05-10 13:45:00" sky_location' ),
[ 'moon', 'venus' ] ],

    'uranus' : [
'astronomical_objects', 'the planet Uranus',
'''
This operator represents the planet Uranus for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'uranus "Harrisburg, PA" "2019-04-29" antitransit_time hms' ),
[ 'saturn', 'neptune' ] ],

    'venus' : [
'astronomical_objects', 'the planet Venus',
'''
This operator represents the planet Venus for astronomical operators that
require an astronomical object.
''',
'''
''' + makeCommandExample( 'venus "Boulder, Colorado" "2019-04-15 06:00:00" next_rising' ),
[ 'mercury', 'moon' ] ],


    #******************************************************************************
    #
    #  astronomy operators
    #
    #******************************************************************************

    'angular_separation' : [
'astronomy', 'returns the angular separation of astronomical objects a and b in radians, at location c, for date-time d',
'''
The angular separation describes the angle between where the two objects
appear in the sky.
''',
'''
''' + makeCommandExample( 'sun moon "Kitty Hawk, NC" "2017-08-21 14:50" angular_separation dms' ),
[ 'sky_location' ] ],

    'angular_size' : [
'astronomy', 'returns the angular size of astronomical object a in radians, at location b, for date-time c',
'''
The angular size describes the width in the sky of the astronomical body as an
angle.
''',
'''
''' + makeCommandExample( 'sun "Paris, France" now angular_size dms' ),
[ 'sky_location' ] ],

    'antitransit_time' : [
'astronomy', 'calculates the antitransit_time of a body a, at location b, starting with date-time c',
'''
The antitransit time is the duration of time from the next setting until the
subseqent rising of a body.
''',
'''
''' + makeCommandExample( 'venus "Ypsilanti, Michigan" "2019-04-15 06:00:00" antitransit_time' ),
[ 'day_time', 'dawn', 'dusk', 'transit_time', 'night_time' ] ],

    'astronomical_dawn' : [
'astronomy', 'calculates the time of the astronomical dawn for location n and date k',
'''
Astronomical dawn is defined as when the center of the sun is 18 degrees below
the horizon before the sun rises.
''',
'''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 astronomical_dawn' ) + '''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 nautical_dawn' ) + '''
''' + makeCommandExample( '"San Francisco, CA" 2016-11-02 dawn' ),
[ 'astronomical_dusk', 'nautical_dawn', 'dawn', 'dusk' ] ],

    'astronomical_dusk' : [
'astronomy', 'calculates the time of the astronomical dusk for location n and date k',
'''
Astronomical dusk is defined as when the center of the sun is 18 degrees below
the horizon after the sun sets.
''',
'''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 nautical_dusk' ) + '''
''' + makeCommandExample( '"Bogota, Bolivia" 2016-09-24 dusk' ),
[ 'astronomical_dawn', 'nautical_dusk', 'dawn', 'dusk' ] ],

    'autumnal_equinox' : [
'astronomy', 'calculates the time of the autumnal equinox for year n',
'''
https://en.wikipedia.org/wiki/September_equinox:

The September (or autumnal) equinox (or Southward equinox) is the moment when
the Sun appears to cross the celestial equator, heading southward.  Due to
differences between the calendar year and the tropical year, the September
equinox can occur at any time between September 21 and 24.

At the equinox, the Sun as viewed from the equator rises due east and sets due
west. Before the Southward equinox, the Sun rises and sets more northerly, and
afterwards, it rises and sets more southerly.

The equinox may be taken to mark the end of summer and the beginning of autumn
(autumnal equinox) in the Northern Hemisphere, while marking the end of winter
and the start of spring (vernal equinox) in the Southern Hemisphere.

rpn uses the Northern hemisphere-centric definition of the term.
''',
'''
''' + makeCommandExample( '2019 autumnal_equinox' ) + '''
''' + makeCommandExample( '2020 autumnal_equinox' ),
[ 'vernal_equinox', 'summer_solstice', 'winter_solstice' ] ],

    'dawn' : [
'astronomy', 'calculates the next dawn time at location n for date-time k',
'''
The definition of dawn being used the is "civil" definition of dawn, i.e., the
center of the sun is 6 degrees below the horizon.
''',
'''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 nautical_dusk' ) + '''
''' + makeCommandExample( '"Santiago, Chile" 2016-09-24 dusk' ),
[ 'day_time', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'day_time' : [
'astronomy', 'calculates the duration of the next day at location n, starting at time k',
'''
This is the transit time for the sun, which is also the amount of time between
sunrise and sunset.
''',
'''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 day_time' ) + '''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 ( sunset sunrise ) unlist -' ),
[ 'dawn', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'distance_from_earth' : [
'astronomy', 'returns the distance from Earth of astronomical object n for date-time k',
'''
This operator returns the distance of the astronomical body n from Earth at
date-time k.
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
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 11:00:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 12:00:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 13:00:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 13:30:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 13:50:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 14:10:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 14:30:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Richmond, Virginia" "2017-08-21 14:50:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Raleigh, NC" "2017-08-21 14:50:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Charleston, SC" "2017-08-21 14:50:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Atlanta, GA" "2017-08-21 14:50:00" eclipse_totality' ) + '''
''' + makeCommandExample( 'sun moon "Tallahassee, FL" "2017-08-21 14:50:00" eclipse_totality' ),
[ 'sky_location', 'angular_size', 'angular_separation' ] ],

    'moonrise' : [
'astronomy', 'calculates the next moonrise time at location n for date-time k',
'''
I suppose some discussion of how timezones come into play would be appropriate
here.  If I knew, I'd explain it.
''',
'''
''' + makeCommandExample( '"Leesburg, Virginia" "2019-05-14 13:00:00" moonrise' ) + '''
''' + makeCommandExample( '"Leesburg, Virginia" "2019-05-14 15:00:00" moonrise' ) + '''
''' + makeCommandExample( '"Johannesburg, South Africa" 2020-01-01 moonrise' ),
[ 'moonset', 'moon_phase' ] ],

    'moonset' : [
'astronomy', 'calculates the nenxt moonset time at location n for date-time k',
'''
I suppose some discussion of how timezones come into play would be appropriate
here.  If I knew, I'd explain it.
''',
'''
''' + makeCommandExample( '"Sheboygan, Michigan" 2019-06-12 moonrise' ) + '''
''' + makeCommandExample( '"Tokyo, Japan" "2019-07-23 04:00:00" moonrise' ) + '''
''' + makeCommandExample( '"Bucharest, Romania" 2019-01-25 moonrise' ),
[ 'moonrise', 'moon_phase' ] ],

    'moon_antitransit' : [
'astronomy', 'calculates the next moon antitransit time at location n for date-time k',
'''
The antitransit time of the moon is the duration between the setting and rising
of the moon.
''',
'''
''' + makeCommandExample( '"Beijing, China" 2019-04-15 moon_antitransit' ),
[ 'moon_transit' ] ],

    'moon_phase' : [
'astronomy', 'determines the phase of the moon as a percentage for date-time n',
'''
The moon phase cycle starts at the new moon and completes with the next new
moon.  Therefore, 0% is the new moon, 25% is the first quarter, 50% is a full
moon, 75% is the last quarter and 100% is the new moon again.
''',
'''
What was the phase of the moon when I was born:
''' + makeCommandExample( '"1965-03-31 05:00:00" moon_phase', indent=4 ) + '''
... a waning crescent.
''',
[ 'moonrise', 'moonset' ] ],

    'moon_transit' : [
'astronomy', 'calculates the next moon transit time at location n for date k',
'''
The transit time of the moon is the duration between the rising and setting of
the moon.
''',
'''
''' + makeCommandExample( '"Tokyo, Japan" 2017-12-12 moon_transit' ) + '''
''' + makeCommandExample( '"Washington, DC" 2017-03-08 moon_transit' ),
[ 'moon_antitransit', 'moonrise', 'moonset' ] ],

    'nautical_dawn' : [
'astronomy', 'calculates the time of the nautical dawn for location n and date k',
'''
Nautical dawn is defined as when the center of the sun is 18 degrees below
the horizon before the sun rises.
''',
'''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 astronomical_dawn' ) + '''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 nautical_dawn' ) + '''
''' + makeCommandExample( '"Pittsburgh, PA" 2017-06-22 dawn' ),
[ 'nautical_dusk', 'dawn', 'astronomical_dawn' ] ],

    'nautical_dusk' : [
'astronomy', 'calculates the time of the nautical dusk for location n and date k',
'''
Nautical dusk is defined as when the center of the sun is 18 degrees below
the horizon after the sun sets.
''',
'''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 astronomical_dusk' ) + '''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 nautical_dusk' ) + '''
''' + makeCommandExample( '"Eugene, OR" 2017-01-07 dusk' ),
[ 'nautical_dawn', 'dusk', 'astronomical_dusk' ] ],

    'next_antitransit' : [
'astronomy', 'returns the time of the next antitransit of body a, when viewed from location b, at date-time c',
'''
''',
'''
''' + makeCommandExample( 'mars "Yakima, Washington" 2019-04-07 next_antitransit' ) + '''
''' + makeCommandExample( 'venus "Roanoke Rapids, NC" 2019-05-12 next_antitransit' ),
[ 'previous_antitransit', 'next_transit', 'next_rising', 'next_setting' ] ],

    'next_first_quarter_moon' : [
'astronomy', 'returns the date of the next first quarter moon after date-time n',
'''
This operator returns the time of the next first quarter moon after date-time
n.
''',
'''
''' + makeCommandExample( 'today next_first_quarter_moon' ) + '''
''' + makeCommandExample( '2008 easter next_first_quarter_moon' ),
[ 'next_full_moon', 'next_last_quarter_moon', 'next_new_moon', 'previous_first_quarter_moon' ] ],

    'next_full_moon' : [
'astronomy', 'returns the date of the next full moon after date-time n',
'''
This operator returns the time of the next full moon after date-time n.
''',
'''
''' + makeCommandExample( 'today next_full_moon' ) + '''
''' + makeCommandExample( '2011-02-02 next_full_moon' ),
[ 'previous_full_moon', 'next_first_quarter_moon', 'next_last_quarter_moon', 'next_new_moon' ] ],

    'next_last_quarter_moon' : [
'astronomy', 'returns the date of the next last quarter moon after date-time n',
'''
This operator returns the time of the next last quarter moon after date-time n.
''',
'''
''' + makeCommandExample( 'today next_last_quarter_moon' ) + '''
''' + makeCommandExample( '2050-01-01 next_last_quarter_moon' ),
[ 'previous_last_quarter_moon', 'next_new_moon', 'next_first_quarter_moon', 'next_new_moon' ] ],

    'next_new_moon' : [
'astronomy', 'returns the date of the next new moon after date-time n',
'''
This operator returns the time of the next new moon after date-time n.
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
''' + makeCommandExample( 'jupiter "London, UK" now next_rising' ) + '''
''' + makeCommandExample( 'saturn "Beijing, China" 2019-05-31 next_rising' ),
[ 'previous_rising', 'next_setting', 'next_transit', 'next_antitransit' ] ],

    'next_setting' : [
'astronomy', 'returns the date of the next setting of body a, when viewed from location b, at date c',
'''
''',
'''
''' + makeCommandExample( 'neptune "Paris, France" now next_setting' ) + '''
''' + makeCommandExample( 'mercury "Gary, Indiana" 2019-06-30 next_setting' ),
[ 'previous_setting', 'next_rising', 'next_transit', 'next_antitransit' ] ],

    'next_transit' : [
'astronomy', 'returns the date of the next transit of body a, when viewed from location b, at date c',
'''
''',
'''
''' + makeCommandExample( 'moon "Albuquerque, NM" 2019-05-03 next_transit' ) + '''
''' + makeCommandExample( 'uranus "Lexington, KY" 2016-03-30 next_transit' ),
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
''' + makeCommandExample( 'mercury "Tulsa, OK" 2019-06-03 previous_antitransit' ) + '''
''' + makeCommandExample( 'pluto "Lincoln, NE" 2018-01-12 previous_antitransit' ),
[ 'next_antitransit', 'previous_rising', 'previous_setting', 'previous_transit' ] ],

    'previous_first_quarter_moon' : [
'astronomy', 'returns the date of the previous first quarter moon before date-time n',
'''
This operator returns the time of the previous first quarter moon before
date-time n.
''',
'''
''' + makeCommandExample( 'today previous_first_quarter_moon' ) + '''
''' + makeCommandExample( '1988-05-03 previous_first_quarter_moon' ),
[ 'next_first_quarter_moon', 'previous_last_quarter_moon', 'previous_full_moon', 'previous_new_moon' ] ],

    'previous_full_moon' : [
'astronomy', 'returns the date of the previous full moon before date-time n',
'''
This operator returns the time of the previous full
moon before date-time n.
''',
'''
''' + makeCommandExample( 'today previous_full_moon' ) + '''
''' + makeCommandExample( '2016-10-31 previous_full_moon' ) + '''
''' + makeCommandExample( '2005-06-23 previous_full_moon' ),
[ 'next_full_moon', 'previous_last_quarter_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_last_quarter_moon' : [
'astronomy', 'returns the date of the previous last quarter moon before date-time n',
'''
This operator returns the time of the previous last quarter
moon before
 date-time n.
''',
'''
''' + makeCommandExample( 'today previous_last_quarter_moon' ) + '''
''' + makeCommandExample( '1971-01-01 previous_last_quarter_moon' ),
[ 'next_last_quarter_moon', 'previous_full_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_new_moon' : [
'astronomy', 'returns the date of the previous new moon before date-time n',
'''
This operator returns the time of the previous new
moon before date-time n.
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
''' + makeCommandExample( 'saturn "New York City, NY" 2012-12-11 previous_rising' ) + '''
''' + makeCommandExample( 'mars "San Diego, CA" 2019-06-30 previous_rising' ),
[ 'next_rising', 'previous_setting', 'previous_transit', 'previous_antitransit' ] ],

    'previous_setting' : [
'astronomy', 'returns the date of the previous setting of body a, when viewed from location b, at date c',
'''
''',
'''
''' + makeCommandExample( 'neptune "Paris, France" now previous_setting' ) + '''
''' + makeCommandExample( 'mercury "Gary, Indiana" 2019-06-30 previous_setting' ),
[ 'next_setting', 'previous_rising', 'previous_transit', 'previous_antitransit' ] ],

    'previous_transit' : [
'astronomy', 'returns the date of the previous transit of body a, when viewed from location b, at date c',
'''
''',
'''
''' + makeCommandExample( 'neptune "Paris, France" now previous_transit' ) + '''
''' + makeCommandExample( 'mercury "Gary, Indiana" 2019-06-30 previous_transit' ),
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
From https://en.wikipedia.org/wiki/Noon#Solar_noon:

Solar noon is the time when the Sun appears to contact the local celestial
meridian.  This is when the Sun apparently reaches its highest point in the
sky, at 12 noon apparent solar time and can be observed using a sundial.  The
local or clock time of solar noon depends on the longitude and date.
''',
'''
''' + makeCommandExample( '"Santiago, Chile" 2019-12-11 solar_noon' ) + '''
''' + makeCommandExample( '"Leesburg, VA" 2019-05-30 solar_noon' ),
[ 'dawn', 'dusk' ] ],

    'summer_solstice' : [
'astronomy', 'calculates the time of the summer solstice for year n',
'''
The summer solstice, also known as estival solstice or midsummer, occurs when
one of the Earth's poles has its maximum tilt toward the Sun.  It happens twice
yearly, once in each hemisphere (Northern and Southern).  For that hemisphere,
the summer solstice is when the Sun reaches its highest position in the sky and
is the day with the longest period of daylight.  Within the Arctic circle (for
the northern hemisphere) or Antarctic circle (for the southern hemisphere),
there is continuous daylight around the summer solstice.

rpn uses the Northern hemisphere-centric definition of the term.
''',
'''
''' + makeCommandExample( '2010 summer_solstice' ) + '''
''' + makeCommandExample( '2019 2022 range summer_solstice' ),
[ 'winter_solstice', 'autumnal_equinox', 'vernal_equinox' ] ],

    'sunrise' : [
'astronomy', 'calculates the next sunrise time at location n for date-time k',
'''
Sunrise (or sunup) is the moment when the upper limb of the Sun appears on the
horizon in the morning.  The term can also refer to the entire process of the
solar disk crossing the horizon and its accompanying atmospheric effects.

Astronomically, sunrise occurs for only an instant: the moment at which the
upper limb of the Sun appears tangent to the horizon.
''',
'''
''' + makeCommandExample( '"Santiago, Chile" 2019-12-11 sunrise' ) + '''
''' + makeCommandExample( '"Leesburg, VA" 2019-05-30 sunrise' ),
[ 'sunset', 'solar_noon' ] ],

    'sunset' : [
'astronomy', 'calculates the next sunset time at location n for date-time k',
'''
From https://en.wikipedia.org/wiki/Sunset:

Sunset, also known as sundown, is the daily disappearance of the Sun below the
horizon due to Earth's rotation.  As viewed from the Equator, the equinox Sun
sets exactly due west in both Spring and Autumn.  As viewed from the middle
latitudes, the local summer Sun sets to the northwest for the Northern
Hemisphere, but to the southwest for the Southern Hemisphere.

The time of sunset is defined in astronomy as the moment when the upper
limb of the Sun disappears below the horizon.  Near the horizon, atmospheric
refraction causes sunlight rays to be distorted to such an extent that
geometrically the solar disk is already about one diameter below the horizon
when a sunset is observed.

Sunset is distinct from twilight, which is divided into three stages, the
first being civil twilight, which begins once the Sun has disappeared below the
horizon, and continues until it descends to 6 degrees below the horizon; the
second phase is nautical twilight, between 6 and 12 degrees below the horizon;
and the third is astronomical twilight, which is the period when the Sun is
between 12 and 18 degrees below the horizon.  Dusk is at the very end of
astronomical twilight, and is the darkest moment of twilight just before night.
Night occurs when the Sun reaches 18 degrees below the horizon and no longer
illuminates the sky.
''',
'''
''' + makeCommandExample( '"Santiago, Chile" 2019-12-11 sunset' ) + '''
''' + makeCommandExample( '"Leesburg, VA" 2019-05-30 sunset' ),
[ 'sunrise', 'solar_noon' ] ],

    'sun_antitransit' : [
'astronomy', 'calculates the next sun antitransit time at location n for date-time k',
'''
Think of it sort of like "anti-noon".
''',
'''
''' + makeCommandExample( '"Bridgeford, CT" today sun_antitransit' ),
[ 'solar_noon', 'sunrise', 'sunset' ] ],

    'transit_time' : [
'astronomy', 'calculates the duration of time from the next rising until the subseqent setting of a body',
'''
a is an astronomical object, b is a location and c is a date-time value
''',
'''
''' + makeCommandExample( 'moon "Washington, DC" today transit_time hms' ),
[ 'day_time', 'dawn', 'dusk', 'antitransit_time', 'night_time' ] ],

    'vernal_equinox' : [
'astronomy', 'calculates the time of the vernal equinox for year n',
'''
The March (or vernal) equinox or Northward equinox is the equinox on the Earth
when the subsolar point appears to leave the Southern Hemisphere and cross the
celestial equator, heading northward as seen from Earth.  The March equinox is
known as the vernal equinox (spring equinox) in the Northern Hemisphere and as
the autumnal equinox in the Southern.

On the Gregorian calendar, the Northward equinox can occur as early as 19 March
or as late as 21 March at Greenwich.  For a common year the computed time
slippage is about 5 hours 49 minutes later than the previous year, and for a
leap year about 18 hours 11 minutes earlier than the previous year.  Balancing
the increases of the common years against the losses of the leap years keeps
the calendar date of the March equinox from drifting more than one day from 20
March each year.

The March equinox may be taken to mark the beginning of spring and the end of
winter in the Northern Hemisphere but marks the beginning of autumn and the end
of summer in the Southern Hemisphere.[8]

In astronomy, the March equinox is the zero point of sidereal time and,
consequently, right ascension.  It also serves as a reference for calendars
and celebrations in many human cultures and religions.

rpn uses the Northern hemisphere-centric definition of the term.
''',
'''
''' + makeCommandExample( '2014 vernal_equinox' ) + '''
''' + makeCommandExample( '2019 2022 range vernal_equinox' ),
[ 'summer_solstice', 'autumnal_equinox', 'winter_solstice' ] ],

    'winter_solstice' : [
'astronomy', 'calculates the time of the winter solstice for year n',
'''
From https://en.wikipedia.org/wiki/Winter_solstice:

The winter solstice, hiemal solstice or hibernal solstice, also known as
midwinter, occurs when one of the Earth's poles has its maximum tilt away from
the Sun.  It happens twice yearly, once in each hemisphere (Northern and
Southern).  For that hemisphere, the winter solstice is the day with the
shortest period of daylight and longest night of the year, when the Sun is at
its lowest daily maximum elevation in the sky.  At the pole, there is
continuous darkness or twilight around the winter solstice.  Its opposite is
the summer solstice.

rpn uses the Northern hemisphere-centric definition of the term.
''',
'''
''' + makeCommandExample( '1987 winter_solstice' ) + '''
''' + makeCommandExample( '2019 2022 range winter_solstice' ),
[ 'autumnal_equinox', 'summer_solstice', 'vernal_equinox' ] ],


    #******************************************************************************
    #
    #  bitwise operators
    #
    #******************************************************************************

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

    'bitwise_xnor' : [
'bitwise', 'calculates the bitwise \'xnor\' of n and k',
'''
'xnor' is the 'exclusive or' logical operation, which returns true if and only
if the two operands are the same.

The operands are converted to strings of bits large enough to represent the
larger of the values, rounded up to the next highest multiple of the bitwise
group size, which defaults to ''' + str( g.defaultBitwiseGroupSize ) + '.' + '''

As a bitwise operator, this operation is applied succesively to each
corresponding bit in the binary representation of both operands.  The result
is the numerical representation of the string of 'xnor'ed bits.
''',
'''
''' + makeCommandExample( '-x 0xffff0000 0x12345678 xnor' ) + '''
''' + makeCommandExample( '[ 0 0 1 1 ] [ 0 1 0 1 ] xnor' ),
[ 'bitwise_and', 'bitwise_or', 'bitwise_nand', 'bitwise_nor', 'bitwise_not', 'bitwise_xor' ] ],

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
[ 'bitwise_and', 'bitwise_or', 'bitwise_nand', 'bitwise_nor', 'bitwise_not', 'bitwise_xnor' ] ],

    'count_bits' : [
'bitwise', 'returns the number of set bits in the non-negative integer n',
'''
In order to count bits in a C integer or IEEE floating point representation,
use 'uint32', 'float', 'double', etc. and then use that result as an argument
for 'count_bits'.
''',
'''
''' + makeCommandExample( '1 20 range count_bits' ) + '''
''' + makeCommandExample( '4858773054 count_bits' ) + '''
Count the bits in an 32-bit C-style (two's complement) integer:
''' + makeCommandExample( '-372 uint32 count_bits', indent=4 ) + '''
Count the bits in an IEEE 32-bit float:
''' + makeCommandExample( '57.651 float count_bits', indent=4 ),
[ 'parity' ] ],

    'parity' : [
'bitwise', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
0 means there are an even number of ones in the binary representation of n.
1 means there are an odd number of ones in the binary representation of n.
''',
'''
''' + makeCommandExample( '1987 parity' ) + '''
''' + makeCommandExample( '1 20 range parity' ),
[ 'count_bits' ] ],

    'shift_left' : [
'bitwise', 'performs a bitwise left shift of value n by k bits',
'''
This is effectively the same as multiplying by 2 for each bit shifted.
''',
'''
''' + makeCommandExample( '1 3 shift_left' ) + '''
''' + makeCommandExample( '16 4 shift_left' ) + '''
''' + makeCommandExample( '1 20 range 1 shift_left' ),
[ 'shift_right' ] ],

    'shift_right' : [
'bitwise', 'performs a bitwise right shift of value n by k bits',
'''
This is effectively the same as dividing by 2 for each bit shifted and
dropping the remainder.
''',
'''
''' + makeCommandExample( '1 1 shift_right' ) + '''
''' + makeCommandExample( '31 3 shift_right' ) + '''
''' + makeCommandExample( '1 20 range 1 shift_right' ),
[ 'shift_left' ] ],


    #******************************************************************************
    #
    #  calendar operators
    #
    #******************************************************************************

    'advent' : [
'calendars', 'returns the date of the first Sunday of Advent for the year specified',
'''
Advent is a season observed in many Christian churches as a time of expectant
waiting and preparation for both the celebration of the Nativity of Jesus at
Christmas and the return of Jesus at the Second Coming.

Advent is celebrated by the Western Christianty starting with the fourth Sunday
preceding Christmas, and ending on Christmas Eve.

Ref:  https://en.wikipedia.org/wiki/Advent
''',
'''
''' + makeCommandExample( '2018 advent' ) + '''
''' + makeCommandExample( '1943 advent' ),
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
c:\\> rpn 2016-09-01 cal

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

Note:  I originally didn't intend to make this operator, since Christmas
is always on the same date, but one day, I was checking the number of
days until Christmas and used the 'christmas' operator instinctively.
''',
'''
''' + makeCommandExample( '2017 christmas' ) + '''
''' + makeCommandExample( '1942 christmas' ),
[ 'thanksgiving', 'easter', 'epiphany', 'advent' ] ],

    'columbus_day' : [
'calendars', 'returns the date of Columbus Day (US) for the year n',
'''
Columbus Day is a national holiday in many countries of the Americas and
elsewhere which officially celebrates the anniversary of Christopher Columbus'
arrival in the Americas on October 12, 1492 (Julian Calendar).

Christopher Columbus was an Italian explorer who set sail across the Atlantic
Ocean in search of a faster route to the the Far East only to land at the New
World.

Ref:  https://en.wikipedia.org/wiki/Columbus_Day
''',
'''
''' + makeCommandExample( '2017 columbus_day' ) + '''
''' + makeCommandExample( '2020 columbus_day' ),
[ 'independence_day', 'veterans_day', 'memorial_day', 'martin_luther_king_day' ] ],

    'dst_end' : [
'calendars', 'calculates the ending date for Daylight Saving Time (US) for the year n',
'''
This function is specific to the United States.  The history of Daylight Saving
Time is rather complicated, and this function attempts to return correct
historical values for every year since DST was adopted.
''',
'''
''' + makeCommandExample( '1972 1976 range dst_start -s1' ) + '''
''' + makeCommandExample( '2004 2009 range dst_start -s1' ),
[ 'dst_start' ] ],

    'dst_start' : [
'calendars', 'calculates the starting date for Daylight Saving Time (US) for the year n',
'''
This function is specific to the United States.  The history of Daylight Saving
Time is rather complicated, and this function attempts to return correct
historical values for every year since DST was adopted.
''',
'''
''' + makeCommandExample( '1972 1976 range dst_end -s1' ) + '''
''' + makeCommandExample( '2004 2009 range dst_end -s1' ),
[ 'dst_end' ] ],

    'easter' : [
'calendars', 'calculates the date of Easter for the year n',
'''
In the Christian calendar, Easter commemorates the Resurrection of Christ.  The
'easter' operator calculates Easter based on the Roman Catholic calendar, which
is the traditional date through most of Western Christendom.
''',
'''
''' + makeCommandExample( '2016 easter' ) + '''
''' + makeCommandExample( '1973 easter' ),
[ 'ash_wednesday', 'good_friday', 'christmas', 'pentecost' ] ],

    'election_day' : [
'calendars', 'calculates the date of Election Day (US) for the year n',
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
'calendars', 'returns the date of Epiphany for the year n',
'''
''',
'''
''' + makeCommandExample( '2011 epiphany' ) + '''
''' + makeCommandExample( '2019 2022 range epiphany' ),
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
''' + makeCommandExample( '177 7 10 from_bahai' ) + '''
''' + makeCommandExample( '1 1 1 from_bahai' ),
[ 'to_bahai', 'to_bahai_name' ] ],

    'from_ethiopian' : [
'calendars', 'converts a date in the Ethiopian calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '2012 3 9 from_ethiopian' ) + '''
''' + makeCommandExample( '2011 1 18 from_ethiopian' ),
[ 'to_ethiopian', 'to_ethiopian_name' ] ],

    'from_french_republican' : [
'calendars', 'converts a date in the French Republican calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '228 04 15 from_french_republican' ) + '''
''' + makeCommandExample( '8 8 14 from_french_republican' ),
[ 'to_french_republican', 'to_french_republican_name' ] ],

    'from_hebrew' : [
'calendars', 'converts a date in the Hebrew calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '5780 7 15 from_hebrew' ) + '''
''' + makeCommandExample( '5000 1 1 from_hebrew' ),
[ 'to_hebrew', 'to_hebrew_name' ] ],

    'from_indian_civil' : [
'calendars', 'converts a date in the Indian civil calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '1942 4 30 from_indian_civil' ) + '''
''' + makeCommandExample( '1912 7 2 from_indian_civil' ),
[ 'to_indian_civil', 'to_indian_civil_name' ] ],

    'from_islamic' : [
'calendars', 'converts a date in the Islamic calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '1439 2 7 from_islamic' ) + '''
''' + makeCommandExample( '1 1 1 from_islamic' ),
[ 'to_islamic', 'to_islamic_name' ] ],

    'from_julian' : [
'calendars', 'converts a date to the equivalent date in the Julian calendar',
'''
''',
'''
''' + makeCommandExample( '2020 1 1 from_julian' ) + '''
''' + makeCommandExample( '1912 12 30 from_julian' ),
[ 'to_julian', 'to_julian_day' ] ],

    'from_mayan' : [
'calendars', 'converts a date in the Mayan long count calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '12 19 17 19 19 from_mayan' ) + '''
''' + makeCommandExample( '13 1 1 1 1 from_mayan' ) + '''
''' + makeCommandExample( '12 1 1 1 1 from_mayan' ),
[ 'to_mayan' ] ],

    'from_persian' : [
'calendars', 'converts a date in the Persian calendar to the equivalent Gregorian date',
'''
''',
'''
''' + makeCommandExample( '1399 4 31 from_persian' ) + '''
''' + makeCommandExample( '1399 1 1 from_persian' ),
[ 'to_persian','to_persian_name' ] ],

    'good_friday' : [
'calendars', 'calculates the date of Good Friday for the year specified',
'''
Good Friday is celebrated by Christians as the day which Jesus was crucified
and died.  This day is two days before the celebration of Jesus' Resurrection
on Easter Sunday, as determined by the Roman Catholic calendar and celebrated
by msot of Western Christendom.
''',
'''
''' + makeCommandExample( '2017 good_friday' ) + '''
''' + makeCommandExample( '2017 easter 2017 good_friday -' ),
[ 'easter', 'ash_wednesday' ] ],

    'independence_day' : [
'calendars', 'returns the date of Independence Day (US) for the year n',
'''
Independence Day celebrates the signing of the Declaration of Independence on
July 4, 1776, which signified the intention of the British colonies to separate
from England and become their own country.
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
[ 'to_iso', 'make_iso_time', 'iso_day', 'to_iso_name' ] ],

    'labor_day' : [
'calendars', 'calculates the date of Labor Day (US) for the year n',
'''
In the U.S., Labor Day falls on the first Monday of September.
''',
'''
''' + makeCommandExample( '2016 labor_day' ) + '''
''' + makeCommandExample( '2016 labor_day 2015 memorial_day -' ),
[ 'memorial_day', 'election_day', 'presidents_day' ] ],

    'martin_luther_king_day' : [
'calendars', 'returns the date of Martin Luther King Day (US) for the year n',
'''
Martin Luther King Day is a Federal holiday in the United States, celebrating
the accomplishments of Dr. Martin Luther King, Jr. who was an American Baptist
minister and influential civil rights spokesperson and activist.

The holiday is celebrated on the third Monday in January, commemorating Dr.
King's birthday on January 15, 1929.
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
''' + makeCommandExample( '2020 2025 range memorial_day -s1' ),
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
''' + makeCommandExample( '2019 8 2 1 nth_weekday' ) + '''
''' + makeCommandExample( '2019 11 4 3 nth_weekday' ) + '''
''' + makeCommandExample( '2020 3 1 1 nth_weekday', indent=4 ),
[ 'nth_weekday_of_year' ] ],

    'nth_weekday_of_year' : [
'calendars', 'finds the nth day (1 = Monday) of the year',
'''
a = four-digit year, b = week (negative values count from the end), c = day
(1 = Monday, 2 = Tuesday, etc. through 7 = Sunday)
''',
'''
''' + makeCommandExample( '2019 8 1 nth_weekday_of_year' ) + '''
''' + makeCommandExample( '2019 43 3 nth_weekday_of_year' ) + '''
Find the last Friday of 2020:
''' + makeCommandExample( '2020 -1 5 nth_weekday_of_year', indent=4 ),
[ 'nth_weekday' ] ],

    'pentecost' : [
'calendars', 'returns the date of Pentecost Sunday for the year specified',
'''
''',
'''
''' + makeCommandExample( '2019 pentecost' ) + '''
''' + makeCommandExample( '2020 pentecost' ),
[ 'easter', 'ascension' ] ],

    'presidents_day' : [
'calendars', 'calculates the date of Presidents Day (US) for the year specified',
'''
''',
'''
''' + makeCommandExample( '2018 presidents_day' ) + '''
''' + makeCommandExample( '2019 presidents_day' ),
[ 'labor_day', 'memorial_day', 'election_day' ] ],

    'thanksgiving' : [
'calendars', 'calculates the date of Thanksgiving (US) for the year specified',
'''
''',
'''
''' + makeCommandExample( '2017 thanksgiving' ) + '''
''' + makeCommandExample( '2019 thanksgiving' ),
[ 'christmas', 'easter', 'mothers_day', 'fathers_day' ] ],

    'to_bahai' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i',
'''
''',
'''
''' + makeCommandExample( '2017-01-11 to_bahai' ) + '''
''' + makeCommandExample( '2018-03-21 to_bahai' ),
[ 'from_bahai', 'to_bahai_name' ] ],

    'to_bahai_name' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i calendar with the weekday and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the Baha'i
names are used.
''',
'''
''' + makeCommandExample( '2017-01-11 to_bahai_name' ) + '''
''' + makeCommandExample( '2018-03-21 to_bahai_name' ),
[ 'from_bahai', 'to_bahai' ] ],

    'to_ethiopian' : [
'calendars', 'converts a date to the equivalent date in the Ethiopian calendar',
'''
''',
'''
''' + makeCommandExample( '2018-12-21 to_ethiopian' ) + '''
''' + makeCommandExample( '2019-04-19 to_ethiopian' ),
[ 'from_ethiopian', 'to_ethiopian_name' ] ],

    'to_ethiopian_name' : [
'calendars', 'converts a date to the equivalent date in the Ethiopian calendar with the day and month names',
'''
The Ethiopian calendar names every day in the month after a saint.  This
function returns the month and date names for the current date in the
Ethiopian calendar.

Since rpnChilada is limited to ASCII text, ASCII versions of the Ethiopian
names are used.
''',
'''
''' + makeCommandExample( '2018-09-15 to_ethiopian_name' ) + '''
''' + makeCommandExample( '2019-05-07 to_ethiopian_name' ),
[ 'from_ethiopian', 'to_ethiopian' ] ],

    'to_french_republican' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i',
'''
''',
'''
''' + makeCommandExample( '1799-07-14 to_french_republican' ) + '''
''' + makeCommandExample( '2020-07-20 to_french_republican' ),
[ 'from_french_republican', 'to_french_republican_name' ] ],

    'to_french_republican_name' : [
'calendars', 'converts a date to the equivalent date in the French Republican calendar with the weekday and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the French
Republican names are used.
''',
'''
''' + makeCommandExample( '1793-04-17 to_french_republican_name' ) + '''
''' + makeCommandExample( '2020-08-21 to_french_republican_name' ),
[ 'from_french_republican', 'to_french_republican' ] ],

    'to_hebrew' : [
'calendars', 'converts a date to the equivalent date in the Hebrew calendar',
'''
''',
'''
''' + makeCommandExample( '2018-04-30 to_hebrew' ) + '''
''' + makeCommandExample( '2019-06-09 to_hebrew' ),
[ 'from_hebrew', 'to_hebrew_name' ] ],

    'to_hebrew_name' : [
'calendars', 'converts a date to the equivalent date in the Hebrew calendar with the weekday and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the Hebrew
names are used.
''',
'''
''' + makeCommandExample( '2018-04-30 to_hebrew_name' ) + '''
''' + makeCommandExample( '2019-06-09 to_hebrew_name' ),
[ 'from_hebrew', 'to_hebrew' ] ],

    'to_indian_civil' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar',
'''
''',
'''
''' + makeCommandExample( '2019-02-28 to_indian_civil' ) + '''
''' + makeCommandExample( '2019-09-01 to_indian_civil' ),
[ 'from_indian_civil', 'to_indian_civil_name' ] ],

    'to_indian_civil_name' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar with the weekday and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the Indian
names are used.
''',
'''
''' + makeCommandExample( '2019-02-28 to_indian_civil_name' ) + '''
''' + makeCommandExample( '2019-09-01 to_indian_civil_name' ),
[ 'from_indian_civil', 'to_indian_civil' ] ],

    'to_islamic' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar',
'''
''',
'''
''' + makeCommandExample( '2019-01-11 to_islamic' ) + '''
''' + makeCommandExample( '2019-12-01 to_islamic' ),
[ 'from_islamic', 'to_islamic_name' ] ],

    'to_islamic_name' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar with day and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the Islamic
names are used.
''',
'''
''' + makeCommandExample( '2019-01-11 to_islamic_name' ) + '''
''' + makeCommandExample( '2019-12-01 to_islamic_name' ),
[ 'from_islamic', 'to_islamic' ] ],

    'to_iso' : [
'calendars', 'converts a date to the equivalent ISO date',
'''
''',
'''
''' + makeCommandExample( '2020-01-11 to_iso' ) + '''
''' + makeCommandExample( '2020-07-21 to_iso' ),
[ 'iso_date', 'to_iso_name', 'iso_day', 'make_iso_time' ] ],

    'to_iso_name' : [
'calendars', 'converts a date to the formatted version of the equivalent ISO date',
'''
''',
'''
''' + makeCommandExample( '2020-01-11 to_iso_name' ) + '''
''' + makeCommandExample( '2020-07-21 to_iso_name' ),
[ 'iso_date', 'to_iso', 'iso_day', 'make_iso_time' ] ],

    'to_julian' : [
'calendars', 'converts a date to the equivalent date in the Julian calendar',
'''
''',
'''
''' + makeCommandExample( '1987-06-13 to_julian' ) + '''
''' + makeCommandExample( '1991-10-30 to_julian' ),
[ 'from_julian', 'to_julian_day' ] ],

    'to_julian_day' : [
'calendars', 'returns the Julian day for a time value',
'''
''',
'''
''' + makeCommandExample( '1987-06-13 to_julian_day' ) + '''
''' + makeCommandExample( '1991-10-30 to_julian_day' ),
[ 'from_julian', 'to_julian' ] ],

    'to_lilian_day' : [
'calendars', 'returns the Lilian day for a time value',
'''
''',
'''
''' + makeCommandExample( '1978-08-23 to_lilian_day' ) + '''
''' + makeCommandExample( '1968-05-03 to_lilian_day' ),
[ 'to_julian_day' ] ],

    'to_mayan' : [
'calendars', 'converts a date to the equivalent date in the Mayan long count calendar',
'''
''',
'''
''' + makeCommandExample( '2012-12-20 to_mayan' ) + '''
''' + makeCommandExample( '2012-12-21 to_mayan' ),
[ 'from_mayan' ] ],

    'to_ordinal_date' : [
'calendars', 'returns the date in the Ordinal Date format',
'''
''',
'''
''' + makeCommandExample( '2018-12-13 to_ordinal_date' ) + '''
''' + makeCommandExample( '2019-01-04 to_ordinal_date' ),
[ 'to_iso', 'to_julian_day', 'to_lilian_day' ] ],

    'to_persian' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar',
'''
''',
'''
''' + makeCommandExample( '2019-03-15 to_persian' ) + '''
''' + makeCommandExample( '2019-08-17 to_persian' ),
[ 'from_persian', 'to_persian_name' ] ],

    'to_persian_name' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar with the weekday and month names',
'''
Since rpnChilada is limited to ASCII text, ASCII versions of the Persian
names are used.
''',
'''
''' + makeCommandExample( '2019-03-15 to_persian_name' ) + '''
''' + makeCommandExample( '2019-08-17 to_persian_name' ),
[ 'from_persian', 'to_persian' ] ],

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
side-effect.  It actually returns an empty string.
''',
'''
c:\\>rpn 2019 year_calendar
                                  2019

      January                   February                   March
Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
       1  2  3  4  5                      1  2                      1  2
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       3  4  5  6  7  8  9
13 14 15 16 17 18 19      10 11 12 13 14 15 16      10 11 12 13 14 15 16
20 21 22 23 24 25 26      17 18 19 20 21 22 23      17 18 19 20 21 22 23
27 28 29 30 31            24 25 26 27 28            24 25 26 27 28 29 30
                                                    31

       April                      May                       June
Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6                1  2  3  4                         1
 7  8  9 10 11 12 13       5  6  7  8  9 10 11       2  3  4  5  6  7  8
14 15 16 17 18 19 20      12 13 14 15 16 17 18       9 10 11 12 13 14 15
21 22 23 24 25 26 27      19 20 21 22 23 24 25      16 17 18 19 20 21 22
28 29 30                  26 27 28 29 30 31         23 24 25 26 27 28 29
                                                    30

        July                     August                  September
Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6                   1  2  3       1  2  3  4  5  6  7
 7  8  9 10 11 12 13       4  5  6  7  8  9 10       8  9 10 11 12 13 14
14 15 16 17 18 19 20      11 12 13 14 15 16 17      15 16 17 18 19 20 21
21 22 23 24 25 26 27      18 19 20 21 22 23 24      22 23 24 25 26 27 28
28 29 30 31               25 26 27 28 29 30 31      29 30

      October                   November                  December
Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa      Su Mo Tu We Th Fr Sa
       1  2  3  4  5                      1  2       1  2  3  4  5  6  7
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       8  9 10 11 12 13 14
13 14 15 16 17 18 19      10 11 12 13 14 15 16      15 16 17 18 19 20 21
20 21 22 23 24 25 26      17 18 19 20 21 22 23      22 23 24 25 26 27 28
27 28 29 30 31            24 25 26 27 28 29 30      29 30 31

''',
[ 'calendar', 'weekday' ] ],


    #******************************************************************************
    #
    #  chemistry operators
    #
    #******************************************************************************

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
[ 'element_description', 'atomic_symbol' ] ],

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


    #******************************************************************************
    #
    #  combinatoric operators
    #
    #******************************************************************************

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
[ 'nth_bell' ] ],

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

    'debruijn_sequence' : [
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
''' + makeCommandExample( '3 3 debruijn_sequence' ),
[ 'permutations' ] ],

    'count_frobenius' : [
'combinatorics', 'calculates the number of combinations of items on n that add up to k',
'''
While 'frobenius' returns the lowest number that is not a linear combination of
the values in n, the 'count_frobenius' operators returns the number of
different ways that linear combinations of the values in n add up to k.
''',
'''
''' + makeCommandExample( '[ 6 9 20 ] 42 count_frobenius' ) + '''
''' + makeCommandExample( '[ 1 5 10 25 50 100 ] 100 count_frobenius' ),
[ 'frobenius', 'solve_frobenius' ] ],

    'lah_number' : [
'combinatorics', 'calculate the Lah number for n and k',
'''
from https://en.wikipedia.org/wiki/Lah_number:

In mathematics, the Lah numbers, discovered by Ivo Lah in 1955, are
coefficients expressing rising factorials in terms of falling factorials.

Unsigned Lah numbers have an interesting meaning in combinatorics:  they count
the number of ways a set of n elements can be partitioned into k nonempty
linearly ordered subsets. Lah numbers are related to Stirling numbers.

The Lah numbers are only defined for n >= k.
''',
'''
''' + makeCommandExample( '3 2 lah_number' ) + '''
''' + makeCommandExample( '12 1 lah_number' ) + '''
''' + makeCommandExample( '12 1 lah_number 12 ! -' ) + '''
''' + makeCommandExample( '7 2 lah_number' ) + '''
''' + makeCommandExample( '7 2 lah_number 6 7 ! *  2 / -' ) + '''
''' + makeCommandExample( '-a20 15 3 lah_number' ) + '''
''' + makeCommandExample( '-a20 15 3 lah_number [ 13 14 15 ! ] prod 12 / -' ) + '''
''' + makeCommandExample( '17 16 lah_number' ) + '''
''' + makeCommandExample( '17 16 lah_number 17 16 * -' ),
[ 'stirling1_number', 'stirling2_number', 'narayana_number' ] ],

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

    'narayana_number' : [
'combinatorics', 'calculates the Narayana number for n and k',
'''
From https://en.wikipedia.org/wiki/Narayana_number:

In combinatorics, the Narayana numbers N(n, k), n = 1, 2, 3 ..., 1 <= k <= n,
form a triangular array of natural numbers, called Narayana triangle, that
occur in various counting problems.  They are named after Indian mathematician
T. V. Narayana (1930-1987).   The sum of the nth row of the Narayana triangle
is the nth Catalan number.

An example of a counting problem whose solution can be given in terms of the
Narayana numbers N(n,k), is the number of words containing n pairs of
parentheses, which are correctly matched (known as Dyck words) and which
contain k distinct nestings. For instance, N(4,2) = 6, since with four pairs
of parentheses, six sequences can be created which each contain two occurrences
the sub-pattern ():

(()(()))  ((()()))  ((())())
()((()))  (())(())  ((()))()
''',
'''
''' + makeCommandExample( '10 5 narayana_number' ) + '''
''' + makeCommandExample( '8 4 narayana_number' ) + '''
The 10th row of the 'Narayana triangle':
''' + makeCommandExample( '10 1 10 range narayana_number', indent=4 ),
[ 'nth_catalan', 'lah_number', 'stirling1_number', 'stirling2_number' ] ],

    'nth_apery' : [
'combinatorics', 'calculates the nth Apery number',
'''
From https://mathworld.wolfram.com/AperyNumber.html:

Apery's numbers are defined by
        n
       ---     2        2
A_n =  \    |n|  |n + k|
       /    |k|  |  k  |
       ---
       k=0

where |n| is a binomial coefficient.
      |k|

https://oeis.org/A005259
''',
'''
''' + makeCommandExample( '-a20 1 10 range nth_apery' ) + '''
''' + makeCommandExample( '-a50 30 nth_apery' ),
[ 'nth_sylvester', 'nth_bell', 'nth_motzkin' ] ],

    'nth_bell' : [
'combinatorics', 'calculates the nth Bell number',
'''
From https://en.wikipedia.org/wiki/Bell_number:

In combinatorial mathematics, the Bell numbers count the possible partitions
of a set. These numbers have been studied by mathematicians since the 19th
century, and their roots go back to medieval Japan.  In an example of Stigler's
law of eponymy, they are named after Eric Temple Bell, who wrote about them in
the 1930s.

The Bell numbers are denoted Bn, where n is an integer greater than or equal to
zero.  Starting with B0 = B1 = 1, the first few Bell numbers are

1, 1, 2, 5, 15, 52, 203, 877, 4140, ... (sequence A000110 in the OEIS).

The Bell number Bn counts the number of different ways to partition a set that
has exactly n elements, or equivalently, the number of equivalence relations on
it. Bn also counts the number of different rhyme schemes for n-line poems.

As well as appearing in counting problems, these numbers have a different
interpretation, as moments of probability distributions.  In particular, Bn is
the nth moment of a Poisson distribution with mean 1.

https://oeis.org/A000110
''',
'''
''' + makeCommandExample( '-a20 1 12 range nth_bell' ) + '''
''' + makeCommandExample( '-a40 40 nth_bell' ),
[ 'bell_polynomial', 'partitions' ] ],

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
''' + makeCommandExample( '1 20 range nth_bernoulli' ) + '''
''' + makeCommandExample( '50 nth_bernoulli' ),
[ 'zeta', 'tan', 'tanh' ] ],

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
''' + makeCommandExample( '1 20 range nth_catalan' ) + '''
''' + makeCommandExample( '-a30 50 nth_catalan' ),
[ 'pascal_triangle', 'nth_schroeder_hipparchus' ] ],

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
[ 'nth_schroeder', 'nth_motzkin' ] ],

    'nth_menage' : [
'combinatorics', 'calculate the nth Menage number for n and k',
'''
https://en.wikipedia.org/wiki/M%C3%A9nage_problem
''',
'''
''' + makeCommandExample( '1 10 range nth_menage' ),
[ 'combinations', 'permutations' ] ],

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
[ 'nth_schroeder', 'nth_delannoy' ] ],

    'nth_pell' : [
'combinatorics', 'calculates the nth Pell number',
'''
In mathematics, the Pell numbers are an infinite sequence of integers, known
since ancient times, that comprise the denominators of the closest rational
approximations to the square root of 2. This sequence of approximations begins
1/1, 3/2, 7/5, 17/12, and 41/29, so the sequence of Pell numbers begins with
1, 2, 5, 12, and 29.

Ref:  https://en.wikipedia.org/wiki/Pell_number:
''',
'''
''' + makeCommandExample( '1 20 range nth_pell' ),
[ 'continued_fraction', 'fraction' ] ],

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
[ 'nth_delannoy', 'nth_motzkin' ] ],

    'nth_schroeder_hipparchus' : [
'combinatorics', 'calculates the nth Schroeder-Hipparchus number',
'''
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

Ref:  https://en.wikipedia.org/wiki/Schr%C3%B6der%E2%80%93Hipparchus_number:
''',
'''
''' + makeCommandExample( '1 12 range nth_schroeder_hipparchus' ),
[ 'nth_catalan', 'nth_schroeder' ] ],

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
[ 'egyptian_fractions' ] ],

    'partitions' : [
'combinatorics', 'returns the partition number for n',
'''
A partition of a positive integer n, also called an integer partition, is a way
of writing n as a sum of positive integers.  Two sums that differ only in the
order of their summands are considered the same partition.

For example, 4 can be partitioned in five distinct ways:
    4
    3 + 1
    2 + 2
    2 + 1 + 1
    1 + 1 + 1 + 1

Ref:  https://en.wikipedia.org/wiki/Partition_%28number_theory%29:
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

    'stirling1_number' : [
'combinatorics', 'calculates the Stirling number of the first kind for n and k',
'''
Stirling numbers of the first kind arise in the study of permutations.  In
particular, the Stirling numbers of the first kind count permutations according
to their number of cycles (counting fixed points as cycles of length one).

The Stirling numbers of the first and second kind can be understood as inverses
of one another when viewed as triangular matrices.

Ref:  https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
''',
'''
''' + makeCommandExample( '3 2 stirling1_number' ) + '''
''' + makeCommandExample( '10 7 stirling1_number' ) + '''
''' + makeCommandExample( '5 1 5 range stirling1_number' ),
[ 'stirling2_number', 'permutations', 'lah_number' ] ],

    'stirling2_number' : [
'combinatorics', 'calculates the Sitrling number of the second kind for n and k',
'''
A Stirling number of the second kind (or Stirling partition number) is the
number of ways to partition a set of n objects into k non-empty subsets.
Stirling numbers of the second kind occur in the field of mathematics called
combinatorics and the study of partitions.

Stirling numbers of the second kind are one of two kinds of Stirling numbers,
the other kind being called Stirling numbers of the first kind (or Stirling
cycle numbers).

Ref:  https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind
''',
'''
''' + makeCommandExample( '3 2 stirling2_number' ) + '''
''' + makeCommandExample( '10 7 stirling2_number' ) + '''
''' + makeCommandExample( '5 1 5 range stirling2_number' ),
[ 'stirling1_number', 'permutations', 'lah_number' ] ],


    #******************************************************************************
    #
    #  complex math operators
    #
    #******************************************************************************

    'argument' : [
'complex_math', 'calculates complex argument (phase) of n',
'''
The complex argument, or phase, of a complex number is defined as the
signed angle between the positive real axis and n in the complex plane.
''',
'''
''' + makeCommandExample( '3 3j + arg' ) + '''
''' + makeCommandExample( '3 3j + arg radians degrees convert' ),
[ 'conjugate', 'real', 'imaginary', 'i' ] ],

    'conjugate' : [
'complex_math', 'calculates complex conjugate of n',
'''
The complex conjugate is simply the nunmber with the same real part and an
imaginary part with the same magnitude but opposite sign.
''',
'''
''' + makeCommandExample( '3 3j + conj' ),
[ 'argument', 'real', 'imaginary', 'i' ] ],

#    'i' : [
#'complex_math', 'the constant i, the square root of -1',
#'''
#This operator is a constant that represents i, the square root of -1, which is
#classified as an imaginary number.
#
#rpn now recognizes the Python syntax of using 'j' to represent i.  The 'i'
#operator remains, but is no longer needed.
#''',
#'''
#''' + makeCommandExample( '2 i *' ) + '''
#''' + makeCommandExample( '2j' ) + '''
#''' + makeCommandExample( 'e pi i * **' ) + '''
#
#There's a rounding error here, but this demonstrates Euler's famous equation:
#
#e ^ ( pi * i ) = -1
#''',
#[ 'argument', 'conjugate', 'real', 'imaginary' ] ],

    'imaginary' : [
'complex_math', 'returns the imaginary part of n',
'''
''',
'''
''' + makeCommandExample( '7 imaginary' ) + '''
''' + makeCommandExample( '7j imaginary' ) + '''
''' + makeCommandExample( '3 4j + imaginary' ),
[ 'argument', 'conjugate', 'real', 'i' ] ],

    'real' : [
'complex_math', 'returns the real part of n',
'''
''',
'''
''' + makeCommandExample( '7 real' ) + '''
''' + makeCommandExample( '7j real' ) + '''
''' + makeCommandExample( '3 4j + real' ),
[ 'imaginary', 'i', 'argument', 'conjugate' ] ],


    #******************************************************************************
    #
    #  constants operators
    #
    #******************************************************************************

    'apery_constant' : [
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
''' + makeCommandExample( '-a50 -d5 apery' ) + '''
''' + makeCommandExample( '-a50 -d5 3 zeta' ),
[ 'zeta' ] ],

    'catalan_constant' : [
'constants', 'returns Catalan\'s constant',
'''
From https://en.wikipedia.org/wiki/Catalan%27s_constant:

In mathematics, Catalan's constant G, which appears in combinatorics, is
defined by the alternating sum of the reciprocals of the square of the odd
numbers:

       1    1    1    1    1
b(2) = _  - _  + _  - _  + _  -  ...
        2    2    2    2    2
       1    3    5    7    9

where b is the Direchlet beta function.

Its numerical value is approximately

G = 0.915965594177219015054603514932384110774...
''',
'''
''' + makeCommandExample( 'catalan_constant' ),
[ 'beta', 'zeta' ] ],

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
[ 'copeland_erdos_constant' ] ],

    'copeland_erdos_constant' : [
'constants', 'returns the Copeland-Erdos constant',
'''
From https://en.wikipedia.org/wiki/Copeland%E2%80%93Erd%C5%91s_constant:

The Copeland-Erdos constant is the concatenation of "0." with the base 10
representations of the prime numbers in order.  Its value, using the modern
definition of prime, is approximately 0.235711131719232931374143...

In base 10, the constant is a normal number, a fact proven by Arthur Herbert
Copeland and Paul Erdos in 1946 (hence the name of the constant).
''',
'''
''' + makeCommandExample( '-a60 copeland' ),
[ 'champernowne_constant' ] ],

    'e' : [
'constants', 'returns e (Euler\'s number)',
'''
From https://en.wikipedia.org/wiki/E_(mathematical_constant):

The number e, known as Euler's number, is a mathematical constant
approximately equal to 2.71828 which can be characterized in many ways.  It is
the base of the natural logarithm.  It is the limit of (1 + 1/n)^n as n
approaches infinity, an expression that arises in the study of compound
interest.  It can also be calculated as the sum of the infinite series:
     oo
    ---   1
    \     --
    /     n!
    ---
    n=0

The number e has eminent importance in mathematics, alongside 0, 1, p, and i.
All five of these numbers play important and recurring roles across
mathematics, and these five constants appear in one formulation of Euler's
identity. Like the constant p, e is also irrational (i.e. it cannot be
represented as ratio of integers) and transcendental (i.e. it is not a root of
any non-zero polynomial with rational coefficients).
''',
'''
''' + makeCommandExample( 'e' ),
[ 'pi', 'i' ] ],

    'eddington_number' : [
'constants', 'returns Arthur Eddington\'s famous estimate of the number of subatomic particles in the Universe',
'''
Eddington argued that the value of the fine-structure constant, a, could be
obtained by pure deduction.  He related a to the Eddington number, which was
his estimate of the number of protons in the universe.  This led him in 1929 to
conjecture that a was exactly 1/137.  Other physicists did not adopt this
conjecture and did not accept his argument.

In the late 1930s, the best experimental value of the fine-structure constant,
a, was approximately 1/136.  Eddington then argued, from aesthetic and
numerological considerations, that a should be exactly 1/136.  He devised a
"proof" that NEdd = 136 x 2^256, or about 1.57 x 10e79.  Some estimates of NEdd
point to a value of about 10e80.  These estimates assume that all matter can be
taken to be hydrogen and require assumed values for the number and size of
galaxies and stars in the universe.

Attempts to find a mathematical basis for this dimensionless constant have
continued up to the present time.

In 1938, Arthur Eddington famously claimed that, "I believe there are
15,747,724,136,275,002,577,605,653,961,181,555,468,044,717,914,527,116,709,366,231,425,076,185,631,031,296
protons in the universe and the same number of electrons."  This number is equal to 136 * 2^256.''',
'''
''' + makeCommandExample( '-c -a100 eddington_number' ),
[ 'fine_structure_constant' ] ],

    'euler_mascheroni_constant' : [
'constants', 'returns the Euler-Mascheroni constant',
'''
From https://en.wikipedia.org/wiki/Euler%E2%80%93Mascheroni_constant:

The Euler-Mascheroni constant (also called Euler's constant) is a mathematical
constant recurring in analysis and number theory, usually denoted by the
lowercase Greek letter gamma.

It is defined as the limiting difference between the harmonic series and the
natural logarithm.
''',
'''
''' + makeCommandExample( 'euler_mascheroni_constant' ),
[ 'gamma', 'zeta', 'nth_harmonic_number', 'log' ] ],

    'faraday_constant' : [
'constants', 'returns the Faraday Constant',
'''
The Faraday constant is named after Michael Faraday.  In physics and
chemistry, this constant represents the magnitude of electric charge per mole
of electrons.

Ref:  https://en.wikipedia.org/wiki/Faraday_constant
''',
'''
''' + makeCommandExample( 'faraday_constant' ),
[ 'avogadro_number', 'electron_charge' ] ],

    'fine_structure_constant' : [
'constants', 'returns the fine-structure constant',
'''
From https://en.wikipedia.org/wiki/Fine-structure_constant:

In physics, the fine-structure constant, also known as Sommerfeld's constant,
commonly denoted by a (the Greek letter alpha), is a fundamental physical
constant characterizing the strength of the electromagnetic interaction
between elementary charged particles.  It is a dimensionless quantity related
to the elementary charge e, which characterizes the strength of the coupling
of an elementary charged particle with the electromagnetic field, by the formula

4 pi epsilon_sub_0 h_bar c alpha = e^2.

epsilon_sub_0 is the electric constant, h_bar is the reduced Planck constant,
c is the speed of light and e is the elemtary_charge.

As a dimensionless quantity, its numerical value, approximately 1/137, is
independent of the system of units used.

While there are multiple physical interpretations for a, it received its name
from Arnold Sommerfeld introducing it (1916) in extending the Bohr model of
the atom:  a quantifies the gap in the fine structure of the spectral lines of
the hydrogen atom, which had been precisely measured by Michelson and Morley.
''',
'''
''' + makeCommandExample( 'fine_structure_constant' ),
[ 'electric_constant', 'electron_charge', 'speed_of_light', 'reduced_planck_constant' ] ],

    'glaisher_constant' : [
'constants', 'returns Glaisher\'s constant',
'''
From https://en.wikipedia.org/wiki/Glaisher%E2%80%93Kinkelin_constant:

In mathematics, the Glaisher-Kinkelin constant or Glaisher's constant,
typically denoted A, is a mathematical constant, related to the K-function
and the Barnes G-function.  The constant appears in a number of sums and
integrals, especially those involving gamma functions and zeta functions.
It is named after mathematicians James Whitbread Lee Glaisher and Hermann
Kinkelin.
''',
'''
''' + makeCommandExample( 'glaisher_constant' ),
[ 'zeta', 'gamma' ] ],

    'infinity' : [
'constants', 'evaluates to infinity, used to describe ranges for nsum, nprod, and limit',
'''
This operator represents infinity, and is meant to be used with 'nsum',
'nprod', and 'limit' when describing infinite ranges.
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
''' + makeCommandExample( 'i i **' ) + '''
''' + makeCommandExample( 'itoi' ),
[ 'i' ] ],

    'khinchin_constant' : [
'constants', 'returns Khinchin\'s constant',
'''
From https://en.wikipedia.org/wiki/Khinchin%27s_constant:

In number theory, Aleksandr Yakovlevich Khinchin proved that for almost all
real numbers x, coefficients a_sub_i of the continued fraction expansion of x
have a finite geometric mean that is independent of the value of x and is known
as Khinchin's constant.
''',
'''
''' + makeCommandExample( 'khinchin_constant' ),
[ 'continued_fraction' ] ],

    'merten_constant' : [
'constants', 'returns Merten\'s constant',
'''
From https://en.wikipedia.org/wiki/Meissel%E2%80%93Mertens_constant:

The Meissel-Mertens constant (named after Ernst Meissel and Franz Mertens),
also referred to as Mertens constant, Kronecker's constant, Hadamard-de la
Vallee-Poussin constant or the prime reciprocal constant, is a mathematical
constant in number theory, defined as the limiting difference between the
harmonic series summed only over the primes and the natural logarithm of the
natural logarithm.
''',
'''
''' + makeCommandExample( '-a50 merten_constant' ),
[ 'euler_mascheroni_constant' ] ],

    'mills_constant' : [
'constants', 'returns the Mills constant',
'''
from http://primes.utm.edu/glossary/page.php?sort=MillsConstant:

In the late forties Mills proved that there was a real number A > 1 for which
A ^ 3 ^ n is always a prime (n = 1,2,3,...).  He proved existence only, and did
not attempt to find such an A.  Later others proved that there are uncountably
many choices for A, but again gave no value for A.  It is still not yet possible
to calculate a proven value for A, but if you are willing to accept the Riemann
Hypothesis, then the least possible value for Mills' constant (usually called
"the Mills Constant") [is this].

rpn does not calculate Mills' constant.  The value is hard-coded to 3500
decimal places.
''',
'''
''' + makeCommandExample( '-a50 mills_constant' ),
[ 'prime' ] ],

    'negative_infinity' : [
'constants', 'evaluates to negative infinity, used to describe ranges for nsum, nprod, and limit',
'''
This operator represents negative infinity, and is meant to be used with
'nsum', 'nprod', and 'limit' when describing infinite ranges.
''',
'''
''',
[ 'infinity' ] ],

    'omega_constant' : [
'constants', 'returns the Omega constant',
'''
From https://en.wikipedia.org/wiki/Omega_constant:

The omega constant is a mathematical constant defined as the unique real number
that satisfies the equation

    Omega e^Omega = 1

It is the value of W(1), where W is Lambert's W function.  The name is derived
from the alternate name for Lambert's W function, the omega function.
''',
'''
''' + makeCommandExample( 'omega_constant' ),
[ 'lambertw' ] ],

    'phi' : [
'constants', 'returns phi (the Golden Ratio)',
'''
From https://en.wikipedia.org/wiki/Golden_ratio:

In mathematics, two quantities are in the golden ratio if their ratio is the
same as the ratio of their sum to the larger of the two quantities.

a + b   a
----- = - = phi
  a     b

where the Greek letter phi represents the golden ratio.  It is an irrational
number that is a solution to the quadratic equation x^2 - x - 1 = 0 with a
value of:

phi = 1 + sqrt( 5 )
      -------------
            2

The golden ratio is also called the golden mean or golden section.  Other
names include extreme and mean ratio, medial section, divine proportion,
divine section, golden proportion, golden cut, and golden number.

Mathematicians since Euclid have studied the properties of the golden ratio,
including its appearance in the dimensions of a regular pentagon and in a
golden rectangle, which may be cut into a square and a smaller rectangle with
the same aspect ratio.  The golden ratio has also been used to analyze the
proportions of natural objects as well as man-made systems such as financial
markets, in some cases based on dubious fits to data.  The golden ratio
appears in some patterns in nature, including the spiral arrangement of leaves
and other plant parts.
''',
'''
''' + makeCommandExample( 'phi' ),
[ 'e', 'pi' ] ],

    'pi' : [
'constants', 'returns pi (Archimedes\' constant)',
'''
Frpm https://en.wikipedia.org/wiki/Pi:

The number pi is a mathematical constant.  It is defined as the ratio of a
circle's circumference to its diameter, and it also has various equivalent
definitions.  It appears in many formulas in all areas of mathematics and
physics.  It is approximately equal to 3.14159.  It has been represented by
the Greek letter "pi" since the mid-18th century, and is spelled out as "pi".
It is also referred to as Archimedes' constant.

Being an irrational number, pi cannot be expressed as a common fraction,
although fractions such as 22/7 are commonly used to approximate it.
Equivalently its decimal representation never ends and never settles into a
permanently repeating pattern.  Its decimal (or other base) digits appear to
be randomly distributed, and are conjectured to satisfy a specific kind of
statistical randomness.  It is known that pi is a transcendental number:  it
is not the root of any polynomial with rational coefficients.  The
transcendence of pi implies that it is impossible to solve the ancient
challenge of squaring the circle with a compass and straightedge.
''',
'''
''' + makeCommandExample( 'pi' ),
[ 'e', 'phi', 'tau' ] ],

    'planck_acceleration' : [
'constants', 'returns the Planck acceleration',
'''
This is a derived constant calculated from the CODATA values for the Planck
force and Planck mass.

Ref:  https://www.physics.nist.gov/cgi-bin/cuu/Value?plkm
''',
'''
''' + makeCommandExample( 'planck_acceleration' ),
[ 'planck_force', 'planck_mass' ] ],

    'planck_area' : [
'constants', 'returns the Planck area',
'''
This is a derived constant calculated from the CODATA value for the Planck
length.
''',
'''
''' + makeCommandExample( 'planck_area' ),
[ 'planck_length', 'planck_volume' ] ],

    'planck_angular_frequency' : [
'constants', 'returns the Planck angular frequency',
'''
''',
'''
''' + makeCommandExample( 'planck_angular_frequency' ),
[ 'planck_time', 'planck_length' ] ],

    'planck_charge' : [
'constants', 'returns the Planck charge',
'''
''',
'''
''' + makeCommandExample( 'planck_charge' ),
[ 'planck_current', 'planck_voltage' ] ],

    'planck_current' : [
'constants', 'returns the Planck current',
'''
''',
'''
''' + makeCommandExample( 'planck_current' ),
[ 'planck_voltage', 'planck_charge' ] ],

    'planck_density' : [
'constants', 'returns the Planck density',
'''
This is a derived constant calculated from the CODATA values for the Planck
mass and Planck length.

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_density' ),
[ 'planck_mass', 'planck_volume' ] ],

    'planck_energy' : [
'constants', 'returns the Planck energy',
'''

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_energy' ),
[ 'planck_charge', 'planck_power' ] ],

    'planck_energy_density' : [
'constants', 'returns the Planck energy density',
'''
''',
'''
''' + makeCommandExample( 'planck_energy_density' ),
[ 'planck_volume', 'planck_charge' ] ],

    'planck_force' : [
'constants', 'returns the Planck force',
'''
This is a derived constant calculated from the CODATA values for the Planck
mass, Planck length and Planck time.

Ref:  CODATA 2014
''',
'''
''' + makeCommandExample( 'planck_force' ),
[ 'planck_mass', 'planck_acceleration' ] ],

    'planck_impedance' : [
'constants', 'returns the Planck impedance',
'''
''',
'''
''' + makeCommandExample( 'planck_impedance' ),
[ 'planck_voltage', 'planck_charge' ] ],

    'planck_intensity' : [
'constants', 'returns the Planck intensity',
'''
''',
'''
''' + makeCommandExample( 'planck_intensity' ),
[ 'planck_power', 'planck_area' ] ],

    'planck_length' : [
'constants', 'returns the Planck length',
'''
''',
'''
''' + makeCommandExample( 'planck_length' ),
[ 'planck_area', 'planck_volume' ] ],

    'planck_mass' : [
'constants', 'returns the Planck mass',
'''
''',
'''
''' + makeCommandExample( 'planck_mass' ),
[ 'planck_force', 'planck_acceleration' ] ],

    'planck_momentum' : [
'constants', 'returns the Planck momentum',
'''
''',
'''
''' + makeCommandExample( 'planck_momentum' ),
[ 'planck_mass' ] ],

    'planck_power' : [
'constants', 'returns the Planck power',
'''
''',
'''
''' + makeCommandExample( 'planck_power' ),
[ 'planck_force', 'planck_energy' ] ],

    'planck_pressure' : [
'constants', 'returns the Planck pressure',
'''
''',
'''
''' + makeCommandExample( 'planck_pressure' ),
[ 'planck_force', 'planck_volume' ] ],

    'planck_temperature' : [
'constants', 'returns the Planck temperature',
'''
''',
'''
''' + makeCommandExample( 'planck_temperature' ),
[ 'planck_energy', 'planck_intensity' ] ],

    'planck_time' : [
'constants', 'returns Planck time',
'''
''',
'''
''' + makeCommandExample( 'planck_time' ),
[ 'planck_length', 'planck_acceleration' ] ],

    'planck_voltage' : [
'constants', 'returns the Planck voltage',
'''
''',
'''
''' + makeCommandExample( 'planck_voltage' ),
[ 'planck_charge', 'planck_impedance' ] ],

    'planck_volume' : [
'constants', 'returns the Planck volume',
'''
This is a derived constant calculated from the CODATA value for the Planck
length.

Ref:  http://physics.nist.gov/cuu/Constants/index.html
''',
'''
''' + makeCommandExample( 'planck_volume' ),
[ 'planck_length', 'planck_area' ] ],

    'plastic_constant' : [
'constants', 'returns the Plastic constant',
'''
From https://en.wikipedia.org/wiki/Plastic_number:

In mathematics, the plastic number (also known as the plastic constant, the
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
[ 'fibonacci', 'nsum' ] ],

    'radiation_constant' : [
'constants', 'returns the Radiation Constant',
'''
''',
'''
''' + makeCommandExample( 'radiation_constant' ),
[ 'electric_constant', 'magnetic_constant', 'faraday_constant' ] ],

    'robbins_constant' : [
'constants', 'returns Robbins\' constant',
'''
Robbins' constant represents the average distance between two points selected
at random within a unit cube.
''',
'''
''' + makeCommandExample( 'robbins_constant' ),
[ 'prevost_constant','plastic_constant', 'mills_constant' ] ],

    'silver_ratio' : [
'constants', 'returns the "silver ratio", defined to be 1 + sqrt( 2 )',
'''
''',
'''
''' + makeCommandExample( 'silver_ratio' ),
[ 'phi', 'plastic_constant' ] ],

    'stefan_boltzmann_constant' : [
'constants', 'returns the Stefan Boltzmann Constant',
'''
The Stefan-Boltzmann constant (also Stefan's constant), a physical constant
denoted by the Greek letter sigma, is the constant of proportionality in the
Stefan-Boltzmann law: "the total intensity radiated over all wavelengths
increases as the temperature increases", of a black body which is proportional
to the fourth power of the thermodynamic temperature.

Ref:  https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant
''',
'''
''' + makeCommandExample( 'stefan_boltzmann_constant' ),
[ 'boltzmann_constant', 'electric_constant', 'magnetic_constant' ] ],

    'tau' : [
'constants', 'returns tau (twice Archimedes\' constant, or 2 pi)',
'''
In 2001, Robert Palais proposed using the number of radians in a turn as the
fundamental circle constant instead of pi, which amounts to the number of
radians in half a turn, in order to make mathematics simpler and more
intuitive.

In 2010, Michael Hartl proposed to use tau to represent Palais' circle
constant: tau = 2 pi.  He offered two reasons.  First, tau is the number of
radians in one turn, which allows fractions of a turn to be expressed more
directly: for instance, a 3/4 turn would be represented as 3/4 tau rad instead
of 3/2 pi rad.

Ref:  https://en.wikipedia.org/wiki/Turn_(angle)#Tau_proposals
''',
'''
''' + makeCommandExample( 'tau' ),
[ 'e', 'phi', 'pi' ] ],

    'thue_morse_constant' : [
'constants', 'calculates the Thue-Morse constant',
'''
In mathematics, the Prouhet-Thue-Morse constant, named for Eugene Prouhet,
Axel Thue, and Marston Morse, is the number whose binary expansion
.01101001100101101001011001101001... is given by the Thue-Morse sequence.

Ref:  https://en.wikipedia.org/wiki/Prouhet%E2%80%93Thue%E2%80%93Morse_constant
''',
'''
''' + makeCommandExample( 'thue_morse_constant' ),
[ 'nth_thue_morse' ] ],

    'vacuum_impedance' : [
'constants', 'returns the Vacuum Impedance constant',
'''
Ref:  https://en.wikipedia.org/wiki/Impedance_of_free_space
''',
'''
''' + makeCommandExample( 'vacuum_impedance' ),
[ 'magnetic_constant', 'electric_constant' ] ],

    'von_klitzing_constant' : [
'constants', 'returns the von Klitzing constant',
'''
The value is derived from h/e^2, where h is Planck's constant and e is the
charge of the electron.

Ref:  CODATA 2014
Ref:  https://www.easycalculation.com/constant/von-klitzing-constant.html
Ref:  https://en.wikipedia.org/wiki/Quantum_Hall_effect#The_Bohr_atom_interpretation_of_the_von_Klitzing_constant
''',
'''
''' + makeCommandExample( 'von_klitzing_constant' ),
[ 'planck_constant', 'electron_charge' ] ],


    #******************************************************************************
    #
    #  conversion operators
    #
    #******************************************************************************

    'char' : [
'conversion', 'converts the value to a signed 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '-1 char' ) + '''
''' + makeCommandExample( '1 char' ) + '''
''' + makeCommandExample( '128 char' ) + '''
''' + makeCommandExample( '200 char' ) + '''
''' + makeCommandExample( '2000 char' ),
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
''' + makeCommandExample( '150,000 seconds [ day hour minute second ] convert', indent=4 ),
[ 'invert_units', 'value' ] ],

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
[ 'hms' ] ],

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
'conversion', 'converts Unix time (seconds since epoch) to a date-time format',
'''
This operator converts a Unix time, which is defined to be the number of
seconds since the epoch, January 1, 1970 00:00:00, to a date-time.
''',
'''
''' + makeCommandExample( '1 from_unix_time' ) + '''
''' + makeCommandExample( '1596647399 from_unix_time' ) + '''
''' + makeCommandExample( '2147483647 from_unix_time' ),
[ 'to_unix_time' ] ],

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
This is the generalized version of the 'char', 'short', 'long', etc.,
operators, that allows any arbitrary size of bits, including sizes that are not
multiples of 8.
''',
'''
''' + makeCommandExample( '128 8 integer' ) + '''
''' + makeCommandExample( '4 billion 32 integer' ) + '''
''' + makeCommandExample( '4 billion 33 integer' ),
[ 'uinteger', 'char', 'short', 'long' ] ],

    'invert_units' : [
'conversion', 'inverts the units and takes the reciprocal of the value',
'''
This operation returns an equivalent measurement with the units inverted from
the original operand.

The result is the same value, but in inverted units.  This is useful for turning
a result into something more intuitive and readable.
''',
'''
''' + makeCommandExample( '10 1/inch invert_units' ) + '''
''' + makeCommandExample( '3 cups invert_units' ) + '''
''' + makeCommandExample( '0.025 hours mile / invert_units' ),
[ 'reciprocal' ] ],

    'lat_long_to_nac' : [
'conversion', 'converts a latitude-longitude pair to the NAC format',
'''
''',
'''
''' + makeCommandExample( '"Leesburg, VA" location_info lat_long_to_nac' ) + '''
''' + makeCommandExample( '"Moscow, Russia" location_info lat_long_to_nac' ),
[ 'lat_long', 'location_info' ] ],

    'long' : [
'conversion', 'converts the value to a signed 32-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '1 long' ) + '''
''' + makeCommandExample( '4 billion long' ) + '''
''' + makeCommandExample( '-2 billion long' ),
[ 'char', 'longlong', 'quadlong', 'ulong' ] ],

    'longlong' : [
'conversion', 'converts the value to a signed 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '100 longlong' ) + '''
''' + makeCommandExample( '-100 longlong' ) + '''
''' + makeCommandExample( '-a20 -c 9,000,000,000,000,000,000 longlong' ) + '''
''' + makeCommandExample( '-a20 -c 9,500,000,000,000,000,000 longlong' ),
[ 'char', 'long', 'ulonglong', 'quadlong', 'integer' ] ],

    'pack' : [
'conversion', 'packs an integer using a values list n and a list of bit fields k',
'''
This operator packs unsigned integers (n) into a larger integer, using k as the
list of field sizes in bits.  The 'unpack' operator will return the original
list when given the same field specification.

Here's an example with the different fields separated from each other:

c:\> rpn [ 2 9 4 ] [ 3 4 5 ] pack -r2
10 1001 00100

Please note that if there were leading zeroes in the result, they would not be
shown by rpn.
''',
'''
''' + makeCommandExample( '[ 2 9 4 ] [ 3 4 5 ] pack -r2' ) + '''
''' + makeCommandExample( '[ 1 1 1 1 ] [ 1 3 4 5 ] pack -r2' ) + '''
''' + makeCommandExample( '[ 1 1 1 ] [ 3 4 5 ] pack [ 3 4 5 ] unpack' ) + '''
If a value is too big, it gets truncated to the field size:
''' + makeCommandExample( '[ 1 223 1 ] [ 3 4 5 ] pack [ 3 4 5 ] unpack' ),
[ 'unpack' ] ],

    'quadlong' : [
'conversion', 'converts the value to a signed 128-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '100 quadlong' ) + '''
''' + makeCommandExample( '-100 quadlong' ) + '''
''' + makeCommandExample( '-a40 -c 170,000,000,000,000,000,000,000,000,000,000,000,000 quadlong' ) + '''
''' + makeCommandExample( '-a40 -c 170,500,000,000,000,000,000,000,000,000,000,000,000 quadlong' ),
[ 'char', 'long', 'ulonglong', 'integer' ] ],

    'short' : [
'conversion', 'converts the value to a signed 16-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '100 short' ) + '''
''' + makeCommandExample( '-100 short' ) + '''
''' + makeCommandExample( '32767 short' ) + '''
''' + makeCommandExample( '32768 short' ),
[ 'ushort', 'char', 'long', 'integer' ] ],

    'to_unix_time' : [
'conversion', 'converts from date-time list to Unix time (seconds since epoch)',
'''
This operator converts a date-time to Unix time, which is defined to be the
number of seconds since the epoch, January 1, 1970 00:00:00.  Times from before
the epoch are undefined for this operator.
''',
'''
''' + makeCommandExample( '"1970-01-01 00:01:00" to_unix_time' ) + '''
''' + makeCommandExample( '2001-01-01 to_unix_time' ) + '''
''' + makeCommandExample( '2020-08-05 to_unix_time' ) + '''
''' + makeCommandExample( '"2038-01-19 03:14:07" to_unix_time' ),
[ 'from_unix_time' ] ],

    'uchar' : [
'conversion', 'converts the value to an unsigned 8-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '-1 uchar' ) + '''
''' + makeCommandExample( '1 uchar' ) + '''
''' + makeCommandExample( '128 uchar' ) + '''
''' + makeCommandExample( '256 uchar' ) + '''
''' + makeCommandExample( '2000 uchar' ),
[ 'char', 'ushort', 'ulong', 'uinteger' ] ],

    'uinteger' : [
'conversion', 'converts the value to an unsigned k-bit integer',
'''
This is the generalized version of the 'uchar', 'ushort', 'ulong', etc.,
operators, that allows any arbitrary size of bits, including sizes that are not
multiples of 8.
''',
'''
''' + makeCommandExample( '32 5 uinteger' ) + '''
''' + makeCommandExample( '32 6 uinteger' ) + '''
''' + makeCommandExample( '256 9 uinteger -r2' ) + '''
''' + makeCommandExample( '-9 3 uinteger' ) + '''
''' + makeCommandExample( '2000 12 uinteger' ),
[ 'integer', 'uchar', 'ushort', 'ulong', 'ulonglong', 'uquadlong' ] ],

    'ulong' : [
'conversion', 'converts the value to an unsigned 32-bit integer',
'''
This operator is useful for determining the behavior for C and C++ which use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '32 ulong' ) + '''
''' + makeCommandExample( '-32 ulong' ) + '''
''' + makeCommandExample( '-c 3,000,000,000 ulong' ) + '''
''' + makeCommandExample( '-c 5,000,000,000 ulong' ),
[ 'long', 'ulonglong', 'uquadlong', 'uinteger', 'uchar' ] ],

    'ulonglong' : [
'conversion', 'converts the value to an unsigned 64-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '100 ulonglong' ) + '''
''' + makeCommandExample( '-a20 -c -100 ulonglong' ) + '''
''' + makeCommandExample( '-a20 -c 18,000,000,000,000,000,000 ulonglong' ) + '''
''' + makeCommandExample( '-a20 -c 19,000,000,000,000,000,000 ulonglong' ),
[ 'ulong', 'longlong', 'uquadlong', 'uinteger', 'uchar' ] ],

    'uquadlong' : [
'conversion', 'converts the value to an unsigned 128-bit integer',
'''
This operator is useful for determining the behavior for C and C++ that use
fixed-size integer types.
''',
'''
''' + makeCommandExample( '100 uquadlong' ) + '''
''' + makeCommandExample( '-a40 -c -100 uquadlong' ) + '''
''' + makeCommandExample( '-a40 -c 340,000,000,000,000,000,000,000,000,000,000,000,000 uquadlong' ) + '''
''' + makeCommandExample( '-a40 -c 341,000,000,000,000,000,000,000,000,000,000,000,000 uquadlong' ),
[ 'ulong', 'quadlong', 'uinteger', 'uchar', 'ulonglong' ] ],

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
This operator unpacks unsigned integers from a larger integer (n), using k as
the list of field sizes in bits.
''',
'''
''' + makeCommandExample( '0xffff [ 4 5 7 ] unpack -r2' ) + '''
''' + makeCommandExample( '[ 1 1 1 ] [ 4 9 2 ] pack [ 4 9 2 ] unpack' ) + '''
If a value is too big, it gets truncated to the field size:
''' + makeCommandExample( '[ 1 223 1 ] [ 4 9 2 ] pack [ 4 9 2 ] unpack' ),
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


    #******************************************************************************
    #
    #  date_time operators
    #
    #******************************************************************************

    'iso_day' : [
'date_time', 'returns the ISO day and week for a date-time value',
'''
''',
'''
''',
[ 'iso_date', 'to_iso', 'iso_day', 'to_iso_name' ] ],


    'get_day' : [
'date_time', 'returns the day value of a date-time',
'''
''',
'''
''',
[ 'get_year', 'get_month' ] ],

    'get_hour' : [
'date_time', 'returns the hour value of a date-time',
'''
''',
'''
''',
[ 'get_minute', 'get_second' ] ],

    'get_minute' : [
'date_time', 'returns the minute value of a date-time',
'''
''',
'''
''',
[ 'get_hour', 'get_second' ] ],

    'get_month' : [
'date_time', 'returns the month value of a date-time',
'''
''',
'''
''',
[ 'get_year', 'get_day' ] ],

    'get_second' : [
'date_time', 'returns the second value of a date-time',
'''
''',
'''
''',
[ 'get_minute', 'get_second' ] ],

    'get_year' : [
'date_time', 'returns the year value of a date-time',
'''
''',
'''
''',
[ 'get_month', 'get_day' ] ],

    'make_datetime' : [
'date_time', 'interpret argument as absolute date-time',
'''
''',
'''
''',
[ 'make_iso_time', 'make_julian_time' ] ],

    'make_iso_time' : [
'date_time', 'interpret argument as absolute date-time specified in the ISO format',
'''
''',
'''
''',
[ 'make_datetime', 'make_julian_time' ] ],

    'make_julian_time' : [
'date_time', 'interpret argument as absolute date-time specified by year, Julian day and optional time of day',
'''
''',
'''
''',
[ 'make_datetime', 'make_iso_time' ] ],

    'now' : [
'date_time', 'returns the current date-time',
'''
''',
'''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'now' ),
[ 'today' ] ],

    'today' : [
'date_time', 'returns the current date',
'''
''',
'''
''' + makeCommandExample( 'yesterday' ) + '''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'tomorrow' ),
[ 'yesterday', 'tomorrow' ] ],

    'tomorrow' : [
'date_time', 'returns the next date',
'''
''',
'''
''' + makeCommandExample( 'yesterday' ) + '''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'tomorrow' ),
[ 'yesterday', 'today' ] ],

    'yesterday' : [
'date_time', 'returns the previous date',
'''
''',
'''
''' + makeCommandExample( 'yesterday' ) + '''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'tomorrow' ),
[ 'today', 'tomorrow' ] ],


    #******************************************************************************
    #
    #  function operators
    #
    #******************************************************************************

    #    'break_on' : [
    #'functions', '',
    #'''
    #''',
    #'''
    #''',
    #[ 'filter', 'filter_by_index', 'lambda', 'unfilter' ] ],

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

''' + makeCommandExample( '-a20 1 100 range lambda x is_square filter' ) + '''
''' + makeCommandExample( '-a20 1 80 range fib lambda x is_prime filter' ),
[ 'filter_by_index', 'lambda', 'unfilter', 'filter_integers' ] ],

    'filter_by_index' : [
'functions', 'filters a list n using function k applied to the list indexes',
'''
''',
'''
''',
[ 'filter', 'lambda', 'unfilter_by_index' ] ],

    'filter_integers' : [
'functions', 'filters a list of integers, 1 through n inclusive',
'''
The function is a special case of 'filter', and is implemented as shortcut
since it is a common scenario.

The user-created function can accept two variables:  x, which is the value
being iterated from one to n, and y, which is the value n itself
''',
'''
Which of the first 80 fibonacci numbers is prime?

''' + makeCommandExample( '-a20 80 lambda x fib is_prime filter_integers' ),
[ 'filter_by_index', 'lambda', 'unfilter', 'filter_integers' ] ],

    'filter_lists' : [
'functions', '',
'''
''',
'''
''',
[ 'filter' ] ],

    'for_each' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list of arguments',
'''
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 7 9 ] [ 4 3 ] ] lambda x y power for_each' ),
[ 'for_each_list', 'repeat', 'sequence' ] ],

    'for_each_list' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list argument',
'''
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 6 7 ] [ 8 9 ] ] lambda x -1 element for_each_list' ) + '''
''' + makeCommandExample( '[ [ 1 2 ] [ 3 4 ] [ 5 6 ] [ 7 8 ] ] lambda x sum for_each_list' ),
[ 'for_each', 'repeat', 'sequence' ] ],

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
[ 'eval', 'function', 'limit', 'nsum', 'nprod' ] ],

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
[ 'limit', 'lambda' ] ],

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
rpn 0 pi lambda x sin plot

rpn -5 5 lambda x 4 ** 3 x 3 ** * + 25 x * - plot

rpn 1 50 lambda x fib plot

rpn 1 10 lambda x 1 + fib x fib / plot

''',
[ 'plot2', 'lambda', 'plot_complex' ] ],

    'plot2' : [
'functions', 'plot a 3D function with 2 variables',
'''
'plot2' is very much considered experimental.

'plot2' is not currently supported by the Windows installer since it requires
a number of extra libraries.
''',
'''
rpn -2 2 -2 2 lambda x 2 ** y 2 ** - plot2

''',
[ 'plot', 'lambda', 'plot_complex' ] ],

    'plot_complex' : [
'functions', 'plot a complex function e for values of x between a and b real, c and d imaginary',
'''
'plot_complex' is very much considered experimental.

'plot_complex' is not currently supported by the Windows installer since it
requires a number of extra libraries.
''',
'''
rpn -10 10 -10 10 zeta plot_complex

rpn-10 10 -10 10 zeta plot_complex

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
[ 'eval0', 'eval', 'filter', 'lambda', 'sequence' ] ],

    'sequence' : [
'functions', 'evaluates a 1-arg function c with initial argument a, b times',
'''
''',
'''
''' + makeCommandExample( '1 10 lambda x 2 * 3 + sequence' ) + '''
The Collatz sequence for 19:
''' + makeCommandExample( '19 21 lambda 3 x * 1 + x 2 / x is_odd if sequence' ),
[ 'eval', 'filter', 'lambda', 'repeat' ] ],

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
[ 'filter', 'unfilter_by_index', 'lambda' ] ],

    'unfilter_by_index' : [
'functions', 'filters a list n using the inverse of function k applied to the list indexes',
'''
''',
'''
''',
[ 'filter_by_index', 'unfilter', 'lambda' ] ],

    'x' : [
'functions', 'used as a variable in user-defined functions',
'''
See the 'user_functions' help topic for more details.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( '1 inf lambda 1 2 x ** / nsum' ),
[ 'lambda', 'y', 'z' ] ],

    'y' : [
'functions', 'used as a variable in user-defined functions',
'''
''',
'''
''' + makeCommandExample( '3 4 lambda x 2 ** y 2 ** + sqrt eval2' ) + '''
''' + makeCommandExample( '[ 1 5 range 1 5 range ] permute_lists lambda x y ** for_each' ),
[ 'lambda', 'x', 'z' ] ],

    'z' : [
'functions', 'used as a variable in user-defined functions',
'''
''',
'''
''',
[ 'lambda', 'x', 'y' ] ],


    #******************************************************************************
    #
    #  geometry operators
    #
    #******************************************************************************

    'antiprism_area' : [
'geometry', 'calculates the surface area of an n-sided antiprism of edge length k',
'''
If no unit is specified for the edge length, rpn interprets it as a length in
meters.
''',
'''
''' + makeCommandExample( '3 1 antiprism_area' ) + '''
''' + makeCommandExample( '7 1 meter antiprism_area' ),
[ 'antiprism_volume', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'antiprism_volume' : [
'geometry', 'calculates the volume of an n-sided antiprism of edge length k',
'''
If no unit is specified for the edge length, rpn interprets it as a length in
meters.
''',
'''
''' + makeCommandExample( '3 1 antiprism_volume' ) + '''
''' + makeCommandExample( '7 1 meter antiprism_volume' ),
[ 'antiprism_area', 'prism_volume', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'cone_area' : [
'geometry', 'calculates the surface area of a cone of radius n and height k',
'''
If no unit is specified for either or both of the lengths, rpn interprets them
as a length in meters.
''',
'''
''' + makeCommandExample( '4 5 cone_area' ) + '''
''' + makeCommandExample( '7 inches 3 inches cone_area' ),
[ 'torus_area', 'sphere_area', 'prism_area', 'k_sphere_area', 'cone_volume' ] ],

    'cone_volume' : [
'geometry', 'calculates the volume of a cone of radius n and height k',
'''
If no unit is specified for either or both of the lengths, rpn interprets them
as a length in meters.
''',
'''
''' + makeCommandExample( '4 5 cone_volume' ) + '''
''' + makeCommandExample( '7 inches 3 inches cone_volume' ),
[ 'torus_volume', 'sphere_volume', 'prism_volume', 'k_sphere_volume', 'cone_area' ] ],

    'dodecahedron_area' : [
'geometry', 'calculates the surface area of a regular dodecahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_volume', 'icosahedron_area', 'sphere_area' ] ],

    'dodecahedron_volume' : [
'geometry', 'calculates the volume of a regular dodecahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

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
[ 'square_root', 'distance' ] ],

    'icosahedron_area' : [
'geometry', 'calculates the surface area of a regular icosahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_area', 'icosahedron_volume', 'sphere_area' ] ],

    'icosahedron_volume' : [
'geometry', 'calculates the volume of a regular icosahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_area', 'sphere_volume' ] ],

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
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_volume', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'octahedron_volume' : [
'geometry', 'calculates the volume of a regular octahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octahedron_area', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

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
[ 'antiprism_volume', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'prism_volume' : [
'geometry', 'calculates the volume of an a-sided prism of edge length b, and height c',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_area', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

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
[ 'antiprism_area', 'prism_area', 'tetrahedron_volume', 'octahedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'tetrahedron_volume' : [
'geometry', 'calculates the volume of a regular tetrahedron of edge length n',
'''
''',
'''
''',
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_area', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

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


    #******************************************************************************
    #
    #  geography operators
    #
    #******************************************************************************

    'geographic_distance' : [
'geography', 'calculates the distance, along the Earth\'s surface, of two locations',
'''
''',
'''
''',
[ 'lat_long' ] ],

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
[ 'location_info', 'geographic_distance' ] ],

    'location_info' : [
'geography', 'returns the lat-long for location n',
'''
Location n is a string containing a geographic location.  The operator returns
a two item list containing the values of latitude and longitude in degrees.
''',
'''
''' + makeCommandExample( '"Dakar, Senegal" location_info' ) + '''
''' + makeCommandExample( '"Philadelphia, PA" location_info' ) + '''
''' + makeCommandExample( '"Nome, AL" location_info' ),
[ 'lat_long', 'geographic_distance', 'get_timezone' ] ],


    #******************************************************************************
    #
    #  internal operators
    #
    #******************************************************************************

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
c:\\>rpn _dump_aliases
! factorial
!! double_factorial
!= is_not_equal
% percent
* multiply
** power
*** tetrate
+ add

...

zolotniks zolotnik
zpc zeptoparsec
zpz zeptopotrzebie
zs zeptosecond
zsr zeptosteradian
zst zeptostere
{ (
| is_divisible
} )
~ bitwise_not

8726
''',
[ '_dump_cache', '_dump_conversions', '_dump_operators', '_dump_stats', '_dump_units', '_dump_constants', '_dump_prime_cache' ] ],

    '_dump_cache' : [
'internal', 'dumps the contents of cache n',
'''
The operator returns number of items in the cache.

Since most of the cache names are also operator names, be sure to use the
string literal delimiter (') for the cache name.

e.g.,  "rpn 'next_prime _dump_cache"
''',
'''
c:\\>rpn 'thue_morse _dump_cache
((mpf('0.0'),), {}) 0
((mpf('1.0'),), {}) 1.0
((mpf('2.0'),), {}) 1.0
((mpf('3.0'),), {}) 0.0
((mpf('4.0'),), {}) 1.0
((mpf('5.0'),), {}) 0.0
((mpf('6.0'),), {}) 0.0
((mpf('7.0'),), {}) 1.0
((mpf('8.0'),), {}) 1.0
...
''',
[ '_dump_conversions', '_dump_operators', '_dump_stats', '_dump_units', '_dump_aliases', '_dump_prime_cache' ] ],

    '_dump_constants' : [
'internal', 'dumps the list of constants',
'''
The operator returns number of constants.
''',
'''
''',
[ '_dump_cache', '_dump_conversions', '_dump_operators', '_dump_stats', '_dump_units', '_dump_aliases', '_dump_prime_cache' ] ],

    '_dump_conversions' : [
'internal', 'dumps the list of unit conversions',
'''
The operator returns number of unit conversions.
''',
'''
''',
[ '_dump_cache', '_dump_constants', '_dump_operators', '_dump_stats', '_dump_units', '_dump_aliases', '_dump_prime_cache' ] ],

    '_dump_operators' : [
'internal', 'lists all rpn operators',
'''
The list of operators is divided into normal operators, list operators (which
require at least one list argument), modifier operators (which work outside of
the RPN syntax), and internal operators, which describe rpnChilada itself.

The operator returns number of operators.
''',
'''
c:\\>rpn _dump_operators
regular operators:
   abs
   abundance
   abundance_ratio
   acceleration
   accuracy
   ackermann_number
   ...
''',
[ '_dump_cache', '_dump_conversions', '_dump_aliases', '_dump_stats', '_dump_units', '_dump_constants', '_dump_prime_cache' ] ],

    '_dump_prime_cache' : [
'internal', 'dumps the contents of a prime number cache file',
'''
The operator returns the number of key-value pairs stored in the cache.
''',
'''
''',
[ '_dump_cache', '_dump_conversions', '_dump_aliases', '_dump_stats', '_dump_units', '_dump_constants' ] ],

    '_dump_stats' : [
'internal', 'dumps rpn statistics',
'''
This operator returns the count of unique operators, the count of unit
convesions, the count of indexed prime numbers of each type, the index of the
highest prime number and the value of the highest prime number.

The operator returns the rpnChilada version number in list format.
''',
'''
''',
[ '_dump_cache', '_dump_conversions', '_dump_aliases', '_dump_operators', '_dump_units', '_dump_constants', '_dump_prime_cache' ] ],

    '_dump_units' : [
'internal', 'lists all rpn units',
'''
The operator returns number of units.
''',
'''
''',
[ '_dump_cache', '_dump_conversions', '_dump_aliases', '_dump_operators', '_dump_stats', '_dump_constants', '_dump_prime_cache' ] ],


    #******************************************************************************
    #
    #  lexicographic operators
    #
    #******************************************************************************

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
[ 'combine_digits', 'duplicate_digits', 'duplicate_number', 'get_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

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
''' + makeCommandExample( '1 7 primes combine_digits' ),
[ 'build_numbers', 'duplicate_digits', 'duplicate_number', 'get_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

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
[ 'rotate_digits_left', 'rotate_digits_right' ] ],

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
[ 'add_digits', 'combine_digits', 'duplicate_digits' ] ],

    'erdos_persistence' : [
'lexicography', 'counts the Erdos version of multiplicative persistence for n',
'''
This operator implements a variation of 'multiplicative persistence' as
described by Martin Gardner.

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

Erdos' variation works the same except that zeroes are ignored.
''',
'''
''',
[ 'persistence', 'show_erdos_persistence', 'k_persistence' ] ],

    'filter_max' : [
'functions', 'filters all values greater than k from list n',
'''
This operator is a shortcut for 'n lambda x k is_not_greater filter'.
''',
'''
''' + makeCommandExample( '1 30 range 10 filter_max' ),
[ 'filter_min', 'filter', 'filter_integers', 'filter_on_flags' ] ],

    'filter_min' : [
'functions', 'filters all values less than k from list n',
'''
This operator is a shortcut for 'n lambda x k is_not_less filter'.
''',
'''
''' + makeCommandExample( '1 30 range 20 filter_min' ),
[ 'filter_max', 'filter', 'filter_integers', 'filter_on_flags' ] ],

    'filter_on_flags' : [
'functions', 'filters the list n based on the nonzero values of the list k',
'''
The function is a kludge to work around the lack of nested lambdas in
rpnChilada 8.x.  This work around covers a lot of situations where nested
lambdas would otherwise be used.
''',
'''
''' + makeCommandExample( '1 6 range [ 0 1 0 1 0 1 ] filter_on_flags' ),
[ 'filter_lists', 'filter', 'filter_integers' ] ],

    'find_palindrome' : [
'lexicography', 'adds the reverse of n to itself up to k successive times to find a palindrome',
'''
''',
'''
''' + makeCommandExample( '-a30 10911 55 find_palindrome' ),
[  ] ],

    'get_base_k_digits' : [
'number_theory', 'interprets n as a list of digits in base k',
'''
This operator is the equivalent of converting a number to base k, representing
each digit by its base-10 equivalent.
''',
'''
''' + makeCommandExample( '1 million 2 10 range get_base_k_digits -s1' ) + '''
''' + makeCommandExample( '1042 10 get_base_k_digits' ) + '''
''' + makeCommandExample( '1042 8 get_base_k_digits' ) + '''
''' + makeCommandExample( '3232235521 256 get_base_k_digits' ),
[ 'base' ] ],

    'get_digits' : [
'lexicography', 'returns the list of digits comprising integer n',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''' + makeCommandExample( '1234567890 get_digits' ),
[ 'digits', 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_left_digits', 'get_right_digits', 'rotate_digits_left', 'rotate_digits_right' ] ],

    'get_left_digits' : [
'lexicography', 'returns a number composed of the left k digits of n',
'''
This operator simply extracts the left k digits of n and returns them as a
number.
''',
'''
''' + makeCommandExample( '1234567890 5 get_left_digits' ) + '''
''' + makeCommandExample( '1000001 4 get_left_digits' ),
[ 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_digits', 'get_right_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

    'get_left_truncations' : [
'lexicography', 'returns a list of numbers, successively truncated a digit from the left',
'''
This operator returns a list of numbers where each one has the leftmost digit
truncated from the one previous, until there are none left.
''',
'''
''' + makeCommandExample( '1234567890 get_left_truncations' ) + '''
''' + makeCommandExample( '10101010 get_left_truncations' ),
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
This operator simply takes the right k digits of n and returns them as a number.
''',
'''
''' + makeCommandExample( '1234567890 5 get_right_digits' ) + '''
''' + makeCommandExample( '1000001 4 get_right_digits' ),
[ 'has_digits', 'get_nonzero_digits', 'get_base_k_digits', 'get_left_digits', 'get_digits', 'rotate_digits_left', 'rotate_digits_right'  ] ],

    'get_right_truncations' : [
'lexicography', 'returns a list of numbers, successively truncated a digit from the right',
'''
This operator returns a list of numbers where each one has the rightmost digit
truncated from the one previous, until there are none left.
''',
'''
''' + makeCommandExample( '1234567890 get_right_truncations' ) + '''
''' + makeCommandExample( '10101010 get_right_truncations' ),
[ 'digits', 'get_left_truncations' ] ],

    'has_digits' : [
'lexicography', 'returns whether n contains all of the digits in k',
'''
This boolean operator returns true if the set of unique digits in n is the
same as the set of unique digits in k.
''',
'''
''' + makeCommandExample( '1234 4321 has_digits' ) + '''
''' + makeCommandExample( '12345 5421 has_digits' ) + '''
''' + makeCommandExample( '12333455 5534112 has_digits' ) + '''
''' + makeCommandExample( '12345 54216 has_digits' ) + '''
''' + makeCommandExample( '55555 5 has_digits' ),
[ 'get_digits', 'has_only_digits', 'is_digital_permutation', 'has_any_digits' ] ],

    'has_any_digits' : [
'lexicography', 'returns whether n contains any of the digits in k',
'''
This boolean operator returns true if the set of unique digits in n is a
superset of the set of unique digits in k.
''',
'''
''' + makeCommandExample( '1234 4321 has_any_digits' ) + '''
''' + makeCommandExample( '12345 5421 has_any_digits' ) + '''
''' + makeCommandExample( '12333455 5534112 has_any_digits' ) + '''
''' + makeCommandExample( '12345 54216 has_any_digits' ) + '''
''' + makeCommandExample( '55555 5 has_any_digits' ),
[ 'count_different_digits', 'has_digits', 'get_digits', 'has_only_digits', 'is_digital_permutation' ] ],

    'has_only_digits' : [
'lexicography', 'returns whether n contains only the digits in k and no others',
'''
This boolean operator returns true if the set of unique digits in n is a
subset of the set of unique digits in k.
''',
'''
''' + makeCommandExample( '1234 4321 has_only_digits' ) + '''
''' + makeCommandExample( '12345 5421 has_only_digits' ) + '''
''' + makeCommandExample( '12333455 5534112 has_only_digits' ) + '''
''' + makeCommandExample( '12345 54216 has_only_digits' ) + '''
''' + makeCommandExample( '55555 5 has_only_digits' ),
[ 'get_digits', 'has_digits', 'has_any_digits', 'is_digital_permutation' ] ],

    'is_automorphic' : [
'lexicography', 'returns whether the digits of n squared end with n',
'''
This operator looks at the number lexicographically by determining if the
number squared ends with the digits of the original number.

6 squared is 36, which ends with the digit 6, so 6 is automorphic.
''',
'''
''' + makeCommandExample( '6 is_automorphic' ) + '''
''' + makeCommandExample( '90625 is_automorphic' ),
[ 'is_k_morphic', 'is_trimorphic', 'is_kaprekar' ] ],

    'is_base_k_pandigital' : [
'lexicography', 'returns whether n a pandigital number in base k',
'''
This boolean operator returns whether n is a pandigital number in base k.
''',
'''
''' + makeCommandExample( '123456780 -b9' ) + '''
''' + makeCommandExample( '54480996 9 is_base_k_pandigital' ),
[ 'is_pandigital' ] ],

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
A bouncy number is a number that is alternatingly increasing and decreasing,
or decreasing and increasing.   In other words, at least one successive digit
is greater than the previous one, and at least one successive digit is smaller
than the previous one.

Please note that while number consisting of a single digit, like '222222' is
considered both increasing and decreasing, it is not considered bouncy.  I need
to look up the definitions and see if that's cool.
''',
'''
''' + makeCommandExample( '12321 is_bouncy' ) + '''
''' + makeCommandExample( '54321 is_bouncy' ) + '''
''' + makeCommandExample( '74258 is_bouncy' ) + '''
Most numbers are bouncy:
''' + makeCommandExample( '10000 20000 range lambda x is_bouncy filter count', indent=4 ),
[ 'is_increasing', 'is_decreasing' ] ],

    'is_decreasing' : [
'lexicography', 'returns whether an integer n is decreasing',
'''
A decreasing number is one where each successive digit is equal to or smaller
than the previous digit.
''',
'''
''' + makeCommandExample( '443211 is_decreasing' ) + '''
''' + makeCommandExample( '1234 is_decreasing' ) + '''
''' + makeCommandExample( '11111111111 is_decreasing' ),
[ 'is_increasing', 'is_bouncy' ] ],

    'is_digital_permutation' : [
'lexicography', 'returns whether k is a digital permutation of n',
'''
If the digits of k are the same as the digits of n, except for their order,
then k is a digital permutation of n.
''',
'''
''' + makeCommandExample( '101 110 is_digital_permutation' ) + '''
''' + makeCommandExample( '1234 4321 is_digital_permutation' ) + '''
''' + makeCommandExample( '1201 1201 is_digital_permutation' ),
[ 'is_pandigital', 'permute_digits' ] ],

    'is_generalized_dudeney' : [
'lexicography', 'returns whether an integer n is a generalized Dudeney number of power k',
'''
From https://en.wikipedia.org/wiki/Dudeney_number:

In number theory, a Dudeney number in a given number base b is a natural
number equal to the perfect cube of another natural number such that the digit
sum of the first natural number is equal to the second.  The name derives from
Henry Dudeney, who noted the existence of these numbers in one of his puzzles,
Root Extraction, where a professor in retirement at Colney Hatch postulates
this as a general method for root extraction.

There are exactly six Dudeney Numbers: 1, 512, 4913, 5832, 17576, and 19683.

This concept can be generalized to other powers, which is what this operator
determines:  whether or not n is a Dudeney number of power k.
''',
'''
''' + makeCommandExample( '90 20 is_generalized_dudeney' ) + '''
''' + makeCommandExample( '91 20 is_generalized_dudeney' ) + '''
''' + makeCommandExample( '180 20 is_generalized_dudeney' ) + '''
''' + makeCommandExample( '181 20 is_generalized_dudeney' ) + '''
''' + makeCommandExample( '209 20 is_generalized_dudeney' ),
[ 'is_pdi', 'is_pddi', 'is_narcissistic' ] ],

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
An increasing number is one where each successive digit is equal to or larger
than the previous digit.
''',
'''
''' + makeCommandExample( '4456788 is_increasing' ) + '''
''' + makeCommandExample( '7784 is_increasing' ) + '''
''' + makeCommandExample( '6666666666666666 is_decreasing' ),
[ 'is_decreasing', 'is_bouncy' ] ],

    'is_kaprekar' : [
'lexicography', 'returns whether an integer n is a Kaprekar number',
'''
From https://en.wikipedia.org/wiki/Kaprekar_number:

In mathematics, a natural number in a given number base is a p-Kaprekar number
if the representation of its square in that base can be split into two parts,
where the second part has p digits, that add up to the original number.  The
numbers are named after D. R. Kaprekar.
''',
'''
''' + makeCommandExample( '1 10000 range lambda x is_kaprekar filter' ),
[ 'is_narcissistic', 'is_automorphic', 'is_kaprekar' ] ],

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
From https://en.wikipedia.org/wiki/Narcissistic_number:

In number theory, a narcissistic number (also known as a pluperfect digital
invariant, an Armstrong number (after Michael F. Armstrong) or a plus perfect
number) in a given number base b is a number that is the sum of its own digits
each raised to the power of the number of digits.
''',
'''
''' + makeCommandExample( '1 250 range lambda x 4 is_k_narcissistic filter -r4' ) + '''
''' + makeCommandExample( '1 5000 range lambda x 5 is_k_narcissistic filter -r5' ) + '''
''' + makeCommandExample( '1 5000 range lambda x 6 is_k_narcissistic filter -r6' ) + '''
''' + makeCommandExample( '1 5000 range lambda x 7 is_k_narcissistic filter -r7' ),
[ 'is_narcissistic' ] ],

    'is_narcissistic' : [
'lexicography', 'returns whether an integer n is narcissistic',
'''
From https://en.wikipedia.org/wiki/Narcissistic_number:

In number theory, a narcissistic number (also known as a pluperfect digital
invariant, an Armstrong number (after Michael F. Armstrong) or a plus perfect
number) in a given number base b is a number that is the sum of its own digits
each raised to the power of the number of digits.

This operator operates only on base 10, and 'n is_narcissistic' the equivalent
of 'n 10 is_k_narcissistic'.
''',
'''
''' + makeCommandExample( '1 5000 range lambda x is_narcissistic filter' ),
[ 'is_k_narcissistic', 'is_generalized_dudeney', 'is_pdi', 'is_pddi' ] ],

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

    'is_digital_palindrome' : [
'lexicography', 'returns whether the digtis of n form a palindrome',
'''
n is treated as an integer.  If its digits are palindromic, i.e., they
read the same forwards as backwards, then the operator returns 1.
''',
'''
''' + makeCommandExample( '101 is_digital_palindrome' ) + '''
''' + makeCommandExample( '1201 is_digital_palindrome' ),
[ 'find_palindrome', 'is_pandigital', 'is_increasing', 'is_decreasing' ] ],

    'is_pandigital' : [
'lexicography', 'returns whether an integer n is pandigital',
'''
A pandigital number contains at least one of all the of the digits 0 through
9.
''',
'''
''' + makeCommandExample( '123456789 is_pandigital' ) + '''
''' + makeCommandExample( '1234567890 is_pandigital' ) + '''
''' + makeCommandExample( '-a30 [ 3 3 7 19 928163 1111211111 ] prod is_pandigital' ),
[ 'is_base_k_pandigital', 'is_digital_palindrome', 'is_increasing', 'is_decreasing' ] ],

    'is_pdi' : [
'lexicography', 'returns whether an integer n is a perfect digital invariant',
'''
From https://en.wikipedia.org/wiki/Perfect_digital_invariant:

In number theory, a perfect digital invariant (PDI) is a number in a given
number base b that is the sum of its own digits each raised to a given power p.
''',
'''
''' + makeCommandExample( '370 is_pdi' ) + '''
''' + makeCommandExample( '371 is_pdi' ) + '''
''' + makeCommandExample( '1 1000 range lambda x is_pdi filter' ),
[ 'is_narcissistic', 'is_generalized_dudeney', 'is_pddi' ] ],

    'is_pddi' : [
'lexicography', 'returns whether an integer n is a perfect digit-to-digit invariant for base k',
'''
From https://en.wikipedia.org/wiki/Perfect_digit-to-digit_invariant:

In number theory, a perfect digit-to-digit invariant (PDDI; also known as a
Munchausen number) is a natural number in a given number base b that is equal
to the sum of its digits each raised to the power of itself.  For example, in
base 3 (ternary) there are three:  1, 12, and 22.  The term "Munchausen number"
was coined by Dutch mathematician and software engineer Daan van Berkel in
2009, as this evokes the story of Baron Munchausen raising himself up by his
own ponytail because each digit is raised to the power of itself.
''',
'''
''' + makeCommandExample( '1 100 range lambda x 2 is_pddi filter' ) + '''
''' + makeCommandExample( '1 100 range lambda x 3 is_pddi filter' ) + '''
''' + makeCommandExample( '1 100 range lambda x 4 is_pddi filter' ) + '''
''' + makeCommandExample( '1 1000 range lambda x 5 is_pddi filter' ) + '''
''' + makeCommandExample( '1 1000 range lambda x 6 is_pddi filter' ),
[ 'is_narcissistic', 'is_generalized_dudeney', 'is_pdi' ] ],

    'is_step_number' : [
'list_operators', 'returns whether n is a step number',
'''
A step number is one where each successive digit is one greater or one lesser
than the previous digit.  '0' is considered adjacent to '1', but not not
adjacent to '9'.  The definition used for "step" doesn't wrap around.
''',
'''
''' + makeCommandExample( '1000 10000 range lambda x is_step_number filter' ),
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
''' + makeCommandExample( '1 400 range lambda x is_smith_number filter' ),
[ 'is_base_k_smith_number', 'is_order_k_smith_number' ] ],

    'is_trimorphic' : [
'lexicography', 'returns whether the digits of n cubed end with n',
'''
''',
'''
''' + makeCommandExample( '9999 is_trimorphic' ) + '''
''' + makeCommandExample( '1 500 range lambda x is_trimorphic filter' ),
[ 'is_automorphic', 'is_trimorphic' ] ],

    'k_persistence' : [
'lexicography', 'counts the number of times it takes to successively multiply the digits of n to the kth power to get a one-digit number',
'''
This operator implements 'multiplicative persistence' as described by Martin
Gardner, with the addition that every digit is first taken to the kth power.

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

This version works the same with the addition that every digit is first taken
to the kth power.
''',
'''
''' + makeCommandExample( '80 100 range 2 k_persistence' ) + '''
''' + makeCommandExample( '80 100 range 3 k_persistence' ) + '''
''' + makeCommandExample( '80 100 range 4 k_persistence' ) + '''
''' + makeCommandExample( '280 300 range 4 k_persistence' ) + '''
''' + makeCommandExample( '280 300 range 5 k_persistence' ),
[ 'persistence', 'show_k_persistence', 'show_erdos_persistence' ] ],

    'multiply_digits' : [
'lexicography', 'calculates the product of the digits of integer n',
'''
This operator splits n into individual digits and multiplies them all
together.  If any of the digits is 0, then the result will be 0, so there is
also a version that ignores 0, 'multiply_nonzero_digits'.
''',
'''
''' + makeCommandExample( '123456789 multiply_digits' ) + '''
''' + makeCommandExample( '1234567 multiply_digits' ) + '''
''' + makeCommandExample( '12345670 multiply_digits' ),
[ 'multiply_digit_powers', 'multiply_nonzero_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_digit_powers' : [
'lexicography', 'calculates the product of the kth power of each digit of integer n',
'''
This is a version of "multiply_digits' that takes each digit to the power k
before doing the multiplication.  If k is 1 then it's the same as
'multiply_digits'.
''',
'''
''' + makeCommandExample( '123456789 2 multiply_digit_powers' ) + '''
''' + makeCommandExample( '-a15 1234567 4 multiply_digit_powers' ) + '''
''' + makeCommandExample( '-a15 12345670 4 multiply_digit_powers' ),
[ 'multiply_digits', 'multiply_nonzero_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_nonzero_digits' : [
'lexicography', 'calculates the product of the non-zero digits of integer n',
'''
This is a version of "multiply_nonzero_digits' that takes each digit to the
power k before doing the multiplication.  If k is 1 then it's the same as
'multiply_nonzero_digits'.
''',
'''
''' + makeCommandExample( '123456789 multiply_nonzero_digits' ) + '''
''' + makeCommandExample( '1234567 multiply_nonzero_digits' ) + '''
''' + makeCommandExample( '12345670 multiply_nonzero_digits' ),
[ 'multiply_digit_powers', 'multiply_digits', 'multiply_nonzero_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'multiply_nonzero_digit_powers' : [
'lexicography', 'calculates the product of the kth power of each non-zero digit of integer n',
'''
This is a version of "multiply_nonzero_digits' that takes each digit to the
power k before doing the multiplication.  If k is 1 then it's the same as
'multiply_nonzero_digits'.
''',
'''
''' + makeCommandExample( '123456789 2 multiply_nonzero_digit_powers' ) + '''
''' + makeCommandExample( '-a15 1234567 4 multiply_nonzero_digit_powers' ) + '''
''' + makeCommandExample( '-a15 12345670 4 multiply_nonzero_digit_powers' ),
[ 'multiply_digits', 'multiply_nonzero_digits', 'multiply_digit_powers', 'sum_digits', 'get_digits', 'persistence' ] ],

    'permute_digits' : [
'lexicography', 'generates all values with lexicographic permutations of the digits of n',
'''
This operator takes the individual digits of n and returns a list of all
lexicographic permutations of the digits.
''',
'''
''' + makeCommandExample( '1234 permute_digits' ),
[ 'combine_digits', 'is_digital_permutation' ] ],

    'persistence' : [
'lexicography', 'counts the number of times it takes to successively multiply the digits of n to get a one-digit number',
'''
This operator implements 'multiplicative persistence' as described by Martin
Gardner:

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

This operator returns the count of the resulting chain of numbers.
''',
'''
''' + makeCommandExample( '80 100 range persistence' ) + '''
''' + makeCommandExample( '280 300 range persistence' ),
[ 'show_persistence', 'k_persistence', 'show_erdos_persistence' ] ],

    'replace_digits' : [
'lexicography', 'return value a with every instance of digit b replaced with digit c',
'''
''',
'''
''' + makeCommandExample( '123 1 4 replace_digits' ) + '''
''' + makeCommandExample( '1997 9 8 replace_digits' ) + '''
''' + makeCommandExample( '5000 5 0 replace_digits' ),
[ 'combine_digits', 'permute_digits' ] ],

    'reversal_addition' : [
'lexicography', 'TODO: describe me',
'''
''',
'''
''' + makeCommandExample( '-a20 89 24 reversal_addition' ),
[ ] ],

    'reverse_digits' : [
'lexicography', 'returns n with its digits reversed',
'''
The digits of the number are reversed and the results are combined to form a
new number.
''',
'''
''' + makeCommandExample( '123456789 reverse_digits' ) + '''
''' + makeCommandExample( '1010 reverse_digits' ),
[ 'permute_digits', 'replace_digits' ] ],

    'rotate_digits_left' : [
'lexicography', 'rotates the digits of n to the left by k digits',
'''
''',
'''
''',
[ 'rotate_digits_right' ] ],

    'rotate_digits_right' : [
'lexicography', 'rotates the digits of n to the right by k digits',
'''
''',
'''
''',
[ 'rotate_digits_left' ] ],

    'show_erdos_persistence' : [
'lexicography', 'shows the Erdos multiplicative persistence chain of n',
'''
This operator implements a variation of 'multiplicative persistence' as
described by Martin Gardner.

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

Erdos' variation works the same except that zeroes are ignored.

This operator outputs the list of numbers produced.
''',
'''
''',
[ 'persistence', 'show_persistence', 'show_k_persistence' ] ],

    'show_k_persistence' : [
'lexicography', 'shows the multiplicative persistence chain of n using kth powers',
'''
This operator implements 'multiplicative persistence' as described by Martin
Gardner, with the addition that every digit is first taken to the kth power.

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

This version works the same with the addition that every digit is first taken
to the kth power, and outputs the list of numbers produced.
''',
'''
''',
[ 'k_persistence', 'show_persistence', 'show_erdos_persistence' ] ],

    'show_persistence' : [
'lexicography', 'shows the multiplicative persistence chain of n',
'''
This operator implements 'multiplicative persistence' as described by Martin
Gardner:

"A number's persistence is the number of steps required to reduce it to a
single digit by multiplying all its digits to obtain a second number, then
multiplying all the digits of that number to obtain a third number, and so
on until a one-digit number is obtained.

This operator outputs the list of numbers produced.
''',
'''
''',
[ 'persistence', 'show_k_persistence', 'show_erdos_persistence' ] ],

    'square_digit_chain' : [
'lexicography', 'generates a chain of sums of squared digits',
'''
Summing the squares of each digit of a number will produce another number.
This chain terminates when the next result is one that has already appeared.
''',
'''
''' + makeCommandExample( '123 square_digit_chain' ) + '''
''' + makeCommandExample( '1997 square_digit_chain' ) + '''
''' + makeCommandExample( '943875938475938475 square_digit_chain' ),
[ 'sum_digits', 'show_persistence', 'show_erdos_persistence' ] ],

    'sum_digits' : [
'lexicography', 'calculates the sum of the digits of integer n',
'''
''',
'''
''',
[ 'multiply_digits', 'get_digits' ] ],


    #******************************************************************************
    #
    #  logical operators
    #
    #******************************************************************************

    'and' : [
'logical', 'returns 1 if n and k are both nonzero',
'''
''',
'''
''' + makeCommandExample( '0 0 and' ) + '''
''' + makeCommandExample( '0 1 and' ) + '''
''' + makeCommandExample( '1 0 and' ) + '''
''' + makeCommandExample( '1 1 and' ),
[ 'or', 'nand', 'bitwise_and' ] ],

    'nand' : [
'logical', 'returns 1 if n and k are both zero',
'''
''',
'''
''' + makeCommandExample( '0 0 nand' ) + '''
''' + makeCommandExample( '0 1 nand' ) + '''
''' + makeCommandExample( '1 0 nand' ) + '''
''' + makeCommandExample( '1 1 nand' ),
[ 'or', 'nand', 'bitwise_nand' ] ],

    'nor' : [
'logical', 'returns 1 if n and k are both 0',
'''
''',
'''
''' + makeCommandExample( '0 0 nor' ) + '''
''' + makeCommandExample( '0 1 nor' ) + '''
''' + makeCommandExample( '1 0 nor' ) + '''
''' + makeCommandExample( '1 1 nor' ),
[ 'or', 'nand', 'bitwise_nor' ] ],

    'not' : [
'logical', 'negates the operand',
'''
''',
'''
''' + makeCommandExample( '0 not' ) + '''
''' + makeCommandExample( '1 not' ),
[ 'or', 'nand', 'bitwise_not' ] ],

    'or' : [
'logical', 'return 1 if either n or k, or both, are zero',
'''
''',
'''
''' + makeCommandExample( '0 0 or' ) + '''
''' + makeCommandExample( '0 1 or' ) + '''
''' + makeCommandExample( '1 0 or' ) + '''
''' + makeCommandExample( '1 1 or' ),
[ 'nor', 'and', 'bitwise_or' ] ],

    'xnor' : [
'logical', 'returns 1 if n and k are both 0 or both 1',
'''
''',
'''
''' + makeCommandExample( '0 0 xnor' ) + '''
''' + makeCommandExample( '0 1 xnor' ) + '''
''' + makeCommandExample( '1 0 xnor' ) + '''
''' + makeCommandExample( '1 1 xnor' ),
[ 'xor', 'bitwise_xnor' ] ],

    'xor' : [
'logical', 'return 1 if n and k are not both 0 and not both 1',
'''
''',
'''
''' + makeCommandExample( '0 0 xor' ) + '''
''' + makeCommandExample( '0 1 xor' ) + '''
''' + makeCommandExample( '1 0 xor' ) + '''
''' + makeCommandExample( '1 1 xor' ),
[ 'xnor', 'bitwise_xor' ] ],


    #******************************************************************************
    #
    #  list operators
    #
    #******************************************************************************

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
[ 'element' ] ],

    'cumulative_diffs' : [
'list_operators', 'returns a list with the differences between each element of list n with the first element',
'''
The list returned will be one shorter than the length of the list n.
''',
'''
''' + makeCommandExample( '[ 0 1 2 3 4 5 ] cumulative_diffs' ) + '''
''' + makeCommandExample( '[ 1 3 6 10 15 21 28 36 45 55 ] cumulative_diffs' ) + '''
''' + makeCommandExample( '[ 100 200 300 400 500 ] cumulative_diffs' ),
[ 'diffs', 'ratios', 'cumulative_ratios', 'cumulative_sums' ] ],

    'cumulative_products' : [
'list_operators', 'returns a list of the cumulative products of element with the elements that precede it',
'''
This operator returns a list of the cumulative products of element with the
elements that precede it

The xth item of the resulting list is the product of the first x items in n.
''',
'''
''' + makeCommandExample( '1 10 range cumulative_products' ),
[ 'cumulative_sums', 'cumulative_ratios', 'cumulative_diffs' ] ],

    'cumulative_ratios' : [
'list_operators', 'returns a list with the ratios between each element of n and the first',
'''
This operator is analogous to the 'cumulative_diffs' operator.
''',
'''
''' + makeCommandExample( '1 10 range fibonacci cumulative_ratios' ),
[ 'ratios', 'diffs', 'cumulative_diffs', 'cumulative_products' ] ],

    'cumulative_sums' : [
'list_operators', 'return a list of the cumulative sums of n',
'''
The xth item of the resulting list is the sum of the first x items in n.
''',
'''
''' + makeCommandExample( '1 10 range cumulative_sums' ),
[ 'cumulative_products', 'cumulative_ratios', 'cumulative_diffs' ] ],

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
The list returned will be one shorter than the length of the list n.
''',
'''
''' + makeCommandExample( '[ 0 1 2 3 4 5 ] diffs' ) + '''
''' + makeCommandExample( '[ 0 1 3 6 10 15 21 28 36 45 55 ] diffs' ) + '''
''' + makeCommandExample( '[ 0 1 4 9 16 25 36 49 64 81 100 ] diffs' ),
[ 'cumulative_diffs', 'ratios', 'cumulative_ratios' ] ],

    'does_list_repeat' : [
'list_operators', 'returns the length of the repeated elements in the list',
'''
This operator returns true if one or more of the initial elements of the list
are repeated in their entirety at least once, and any partial remainders are
equal to the partial amount of the original sublist of repeated elements.
''',
'''
''' + makeCommandExample( '[ 1 ] does_list_repeat' ) + '''
''' + makeCommandExample( '[ 1 1 ] does_list_repeat' ) + '''
''' + makeCommandExample( '[ 1 1 1 ] does_list_repeat' ) + '''
''' + makeCommandExample( '[ 1 2 1 2 1 ] does_list_repeat' ) + '''
''' + makeCommandExample( '[ 1 2 1 2 1 2 ] does_list_repeat' ) + '''
''' + makeCommandExample( '[ 1 2 3 1 2 3 1 2 3 1 2 3 ] does_list_repeat' ),
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
[ 'count' ] ],

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
This used to have the arguments swapped, but that seemed wrong.
''',
'''
''' + makeCommandExample( '6 [ 1 4 5 6 9 ] find' ) + '''
And we can access the found item using the 'element' operator:
''' + makeCommandExample( '[ 1 4 5 6 9 ] 3 element', indent=4 ),
[ 'count', 'filter' ] ],

    'flatten' : [
'list_operators', 'flattens a nested lists in list n to a single level',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 [ 3 4 ] [ 5 [ 6 7 ] 8 [ 9 ] ] [ [ 10 ] ] ] flatten' ),
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
''' + makeCommandExample( '[ 1 2 3 4 ] 2 get_combinations -s1' ),
[ 'get_permutations', 'get_repeat_combinations', 'get_partitions' ] ],

    'get_partitions' : [
'list_operators', 'generates all integer partitions of n',
'''
A partition of a positive integer n, also called an integer partition, is a way
of writing n as a sum of positive integers.  Two sums that differ only in the
order of their summands are considered the same partition.

For example, 4 can be partitioned in five distinct ways:
    4
    3 + 1
    2 + 2
    2 + 1 + 1
    1 + 1 + 1 + 1

This operator generates the list of partitions as a list of lists of integers,
where each nested list is a different, unique partitioning of n into integers.

Ref:  https://en.wikipedia.org/wiki/Partition_%28number_theory%29:
''',
'''
''' + makeCommandExample( '2 get_partitions' ) + '''
''' + makeCommandExample( '3 get_partitions' ) + '''
''' + makeCommandExample( '4 get_partitions' ),
[ 'get_combinations', 'get_permutations', 'get_partitions' ] ],

    'get_partitions_with_limit' : [
'list_operators', 'generates all integer partitions of n that are no greater than k',
'''
This operator creates a list of integer partitions of n which is a subset of
what 'get_partitions' creates.  No individual partition can be larger than k.
If k is equal to n, then all integer partitions will be created.

For example, 4 can be partitioned in three distinct ways that no partition is
greater than 2:
    2 + 2
    2 + 1 + 1
    1 + 1 + 1 + 1

This operator generates the list of partitions as a list of lists of integers,
where each nested list is a different, unique partitioning of n into integers.

Ref:  https://en.wikipedia.org/wiki/Partition_%28number_theory%29:
''',
'''
''' + makeCommandExample( '4 2 get_partitions_with_limit -s1' ) + '''
''' + makeCommandExample( '5 3 get_partitions_with_limit -s1' ),
[ 'get_combinations', 'get_permutations', 'get_partitions' ] ],

    'get_permutations' : [
'list_operators', 'generates all permutations of k members of list n',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] 2 get_permutations -s1' ),
[ 'get_combinations', 'get_repeat_permutations', 'get_partitions' ] ],

    'get_repeat_combinations' : [
'list_operators', 'generates all combinations of k members of list n, with repeats allowed',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] 2 get_repeat_combinations -s1' ),
[ 'get_permutations', 'get_combinations' ] ],

    'get_repeat_permutations' : [
'list_operators', 'generates all permutations of k members of list n, with repeats allowed',
'''
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] 2 get_repeat_permutations -s1' ),
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
[ 'is_digital_palindrome' ] ],

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
''' + makeCommandExample( '10 100 random_integers occurrences' ) + '''
''' + makeCommandExample( '5 6 debruijn_sequence occurrences' ),
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
[ 'permute_lists', 'sublist' ] ],

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
[ 'gcd', 'gcd2' ] ],

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
''' + makeCommandExample( '[ 1 2 3 ] [ 4 5 6 ] union' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] [ 3 4 5 ] union' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] [ 3 3 3 ] union' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] [ 1 2 3 ] union' ),
[ 'intersection', 'append', 'permute_lists', 'interleave' ] ],

    'unique' : [
'list_operators', 'returns a list of its unique elements',
'''
''',
'''
''' + makeCommandExample( '1 8 range 2 9 range append 3 10 range append unique' ),
[ 'sort' ] ],

    'zero' : [
'list_operators', 'returns a list of the indices of elements in list n that are zero',
'''
This operator is useful for applying an operator that returns a binary value
on a list, and getting a summary of the results.

Indices are zero-based.
''',
'''
''' + makeCommandExample( '[ 1 0 2 0 3 0 4 ] zero' ) + '''
List the non-prime Fibonacci numbers:
''' + makeCommandExample( '0 20 range fib is_prime zero fib' ),
[ 'nonzero' ] ],


    #******************************************************************************
    #
    #  logarithm operators
    #
    #******************************************************************************

    'lambertw' : [
'logarithms', 'the Lambert W function',
'''
From https://en.wikipedia.org/wiki/Lambert_W_function:

In mathematics, the Lambert W function, also called the omega function or
product logarithm, is a multivalued function, namely the branches of the
inverse relation of the function f(w) = we^w, where w is any complex number
and e^w is the exponential function.

The Lambert W relation cannot be expressed in terms of elementary functions.
It is useful in combinatorics, for instance, in the enumeration of trees.  It
can be used to solve various equations involving exponentials (e.g. the maxima
of the Planck, Bose-Einstein, and Fermi-Dirac distributions) and also occurs in
the solution of delay differential equations, such as y'(t) = a y(t - 1).  In
biochemistry, and in particular enzyme kinetics, a closed-form solution for the
time-course kinetics analysis of Michaelis-Menten kinetics is described in
terms of the Lambert W function.
''',
'''
''' + makeCommandExample( '0 lambertw' ) + '''
''' + makeCommandExample( '10 lambertw' ) + '''
''' + makeCommandExample( '100 lambertw' ),
[ 'log', 'omega_constant' ] ],

    'li' : [
'logarithms', 'calculates the logarithmic integral of n',
'''
From https://en.wikipedia.org/wiki/Logarithmic_integral_function:

In mathematics, the logarithmic integral function or integral logarithm li(x)
is a special function.  It is relevant in problems of physics and has number
theoretic significance.  In particular, according to the Siegel-Walfisz theorem
it is a very good approximation to the prime-counting function, which is
defined as the number of prime numbers less than or equal to a given value x.
''',
'''
''' + makeCommandExample( '2 li' ) + '''
''' + makeCommandExample( '1000000 li' ) + '''
''' + makeCommandExample( '1000000 prime_pi' ) + '''
''' + makeCommandExample( '10000000000000 li' ) + '''
''' + makeCommandExample( '10000000000000 prime_pi' ),
[ 'log' ] ],

    'log' : [
'logarithms', 'calculates the natural logarithm of n',
'''
''',
'''
''' + makeCommandExample( '2 log' ) + '''
''' + makeCommandExample( 'e log' ) + '''
''' + makeCommandExample( 'e 2 ** log' ) + '''
''' + makeCommandExample( '10 log' ) + '''
''' + makeCommandExample( 'e e sqrt * log' ),
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
[ 'polylog', 'exp' ] ],


    'polylog' : [
'logarithms', 'calculates the polylogarithm of n, k',
'''
''',
'''
''',
[ 'log', 'polyexp' ] ],


    #******************************************************************************
    #
    #  modifier operators
    #
    #******************************************************************************

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
[ ']', '(', ')' ] ],

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
[ '[', '(', ')' ] ],

    '(' : [
'modifiers', 'starts an operator list',
'''
An operator list is used to perform multiple operations on a single set of
arguments.  The operators must all take the same number of arguments.

Operator lists can only be used with literal lists.  (Internally, the work as
long as the list isn't implemented as a generator, which means a literal list
would work fine, but a list generated by an operator, such as 'range' won't.
This is something I've wanted to fix for a long time.)
''',
'''
''' + makeCommandExample( 'today "Denver, Colorada" ( sunrise sunset )' ) + '''
''' + makeCommandExample( '10 ( triangular square pentagonal hexagonal heptagonal )' ),
[ ')', '[', ']' ] ],

    ')' : [
'modifiers', 'end an operator list',
'''
An operator list is used to perform multiple operations on a single set of
arguments.  The operators must all take the same number of arguments.

Operator lists can only be used with literal lists.  (Internally, the work as
long as the list isn't implemented as a generator, which means a literal list
would work fine, but a list generated by an operator, such as 'range' won't.
This is something I've wanted to fix for a long time.)
''',
'''
''' + makeCommandExample( 'today "Leesburg, VA" [ venus mars jupiter saturn ] ( next_rising next_setting ) -s1' ),
[ '(', '[', ']' ] ],

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
[ 'previous', 'echo', 'duplicate_operator' ] ],

    'duplicate_operator' : [
'modifiers', 'duplicates an operation n times',
'''
The argument n, which is a count of the number of times to duplicate the
operation, and the 'duplicate_operator' operator must precede another
operator, which will then be performed n times.

If n is 1, then the 'duplicate_operator' operator has no effect, since
operators are evaluated once by default.

'duplicate_operator' is not allowed inside a lambda.  If 'duplicate_operator'
is not followed by another operator, then it has no effect.
''',
'''
''' + makeCommandExample( '10 1 duplicate_operator sqr' ) + '''
''' + makeCommandExample( '10 2 duplicate_operator sqr' ) + '''
''' + makeCommandExample( '10 3 duplicate_operator sqr' ) + '''
''' + makeCommandExample( '8 3 2 duplicate_operator **' ) + '''
''' + makeCommandExample( '8 3 3 duplicate_operator **' ),
[ 'previous', 'echo', 'duplicate_term' ] ],

    'previous' : [
'modifiers', 'duplicates the previous argument (identical to \'n 2 duplicate_term\')',
'''
This is a shortcut that can prevent having to duplicate a long expression.
''',
'''
''' + makeCommandExample( '[ 3 previous ]' ) + '''
''' + makeCommandExample( '[ 3 sqr previous ]' ),
[ 'echo', 'duplicate_term' ] ],

    'unlist' : [
'modifiers', 'expands a list into separate arguments',
'''
This operator turns a list into separate arguments so they can be passed to an
operator that works with separate arguments.
''',
'''
Here, we use 'unlist' to make arguments for 'euler_brick':

''' + makeCommandExample( '4 5 make_pyth_3' ) + '''
''' + makeCommandExample( '4 5 make_pyth_3 unlist euler_brick' ),
[ 'flatten' ] ],


    #******************************************************************************
    #
    #  number theory operators
    #
    #******************************************************************************

    'abundance' : [
'number_theory', 'returns the abundance of n',
'''
''',
'''
''',
[ 'abundance_ratio' ] ],

    'abundance_ratio' : [
'number_theory', 'returns the abundance ratio of n',
'''
''',
'''
''',
[ 'abundance' ] ],

    'ackermann_number' : [
'number_theory', 'calculates the value of the Ackermann function for n and k',
'''
''',
'''
''' + makeCommandExample( '1 3 range 4 ackermann_number' ) + '''
''' + makeCommandExample( '3 1 10 range ackermann_number' ),
[ 'hyperoperator' ] ],

    'aliquot' : [
'number_theory', 'returns the first k members of the aliquot sequence of n',
'''
''',
'''
''' + makeCommandExample( '276 10 aliquot' ) + '''
''' + makeCommandExample( '320 25 aliquot' ),
[ 'aliquot_limit', 'collatz' ] ],

    'aliquot_limit' : [
'number_theory', 'returns the members of the aliquot sequence of n until a value in the sequence exceeds 10^k',
'''
''',
'''
''' + makeCommandExample( '276 4 aliquot_limit' ) + '''
''' + makeCommandExample( '320 4 aliquot_limit' ),
[ 'aliquot', 'collatz' ] ],

    'alternating_factorial' : [
'number_theory', 'calculates the alternating factorial of n',
'''
An alternating factorial is the absolute value of the alternating sum of the
first n factorials of positive integers, having the recurrence relation:

af( n ) = n! - af( n - 1 )

Ref:  https://en.wikipedia.org/wiki/Alternating_factorial
''',
'''
''' + makeCommandExample( '1 10 range alternating_factorial' ),
[ 'factorial' ] ],

    'alternating_harmonic_fraction' : [
'number_theory', 'returns the rational version of the nth alternating harmonic number',
'''
The alternating harmonic series consists of the sums of the reciprocals of
the natural numbers, where every second one is negative.  They are all
rational numbers, so it's possible to represent them as fractions.
''',
'''
''' + makeCommandExample( '2 alternating_harmonic_fraction' ) + '''
''' + makeCommandExample( '7 alternating_harmonic_fraction' ) + '''
''' + makeCommandExample( '-a20 60 alternating_harmonic_fraction' ) + '''
''' + makeCommandExample( '-a50 110 alternating_harmonic_fraction' ),
[ 'harmonic_fraction' ] ],

    'barnesg' : [
'number_theory', 'evaluates the Barnes G-function for n',
'''
The Barnes G-function is the generalization of the superfactorial to real and
complex numbers.
''',
'''
''',
[ 'superfactorial', 'gamma' ] ],

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
[ 'zeta', 'gamma' ] ],

    'calkin_wilf' : [
'number_theory', 'calculates the nth member of the Calkin-Wilf sequence',
'''
The Calkin-Wilf tree is a tree in which the vertices correspond one-to-one to
the positive rational numbers.  The tree is rooted at the number 1, and any
rational number expressed in simplest terms as the fraction a/b has as its two
children the numbers a/a+b and a+b/b.  Every positive rational number appears
exactly once in the tree.

The sequence of rational numbers in a breadth-first traversal of the
Calkin-Wilf tree is known as the Calkin-Wilf sequence.

This operator returns a list of two numbers, the numerator and the denominator
of the nth number in the Calkin-Wilf sequence.

Ref:  https://en.wikipedia.org/wiki/Calkin%E2%80%93Wilf_tree
''',
'''
''' + makeCommandExample( '0 10 range calkin_wilf' ) + '''
''' + makeCommandExample( '1000000 calkin_wilf' ) + '''
''' + makeCommandExample( '1000000000000000000000000000000000 calkin_wilf' ),
[ ] ],

    'continued_fraction' : [
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''',
[ 'make_continued_fraction', 'fraction' ] ],

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
divisors from the list of prime factors.

'rpn divisors count' calculates the same result, but the 'divisors' operator
can generate prohibitively large lists for numbers with a lot of factors.
''',
'''
''' + makeCommandExample( '98280 count_divisors' ) + '''
''' + makeCommandExample( '1 20 range count_divisors' ),
[ 'divisors', 'factor' ] ],

    'crt' : [
'number_theory', 'calculates Chinese Remainder Theorem result of a list n of values and a list k of modulos',
'''
So using the Chinese Remainder Theorem, this function calculates a number that
is equal to n[ x ] modulo k[ x ], with x iterating through the indices of each
list (which must be the same size).
''',
'''
''',
[ 'digital_root', 'harmonic_residue' ] ],

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
[ 'polygamma' ] ],

    'digital_root' : [
'number_theory', 'returns the digital root of N',
'''
https://en.wikipedia.org/wiki/Digital_root
''',
'''
''',
[ 'harmonic_residue', 'crt' ] ],

    'divisors' : [
'number_theory', 'returns a list of divisors of n',
'''
This operator lists all proper divisors of an integer including 1 and the
integer itself, sorted in order of increasing size.
''',
'''
''' + makeCommandExample( '3600 divisors' ) + '''
''' + makeCommandExample( '[ 2 3 5 ] prod divisors' ),
[ 'count_divisors', 'factor' ] ],

    'double_factorial' : [
'number_theory', 'calculates the double factorial of n',
'''
The name 'double factorial' is a little misleading as the definition of this
function is that n is multiplied by every second number between it and 1.

So it could sort of be thought of as a "half factorial".
''',
'''
''' + makeCommandExample( '1 10 range double_factorial' ),
[ 'factorial', 'superfactorial', 'subfactorial', 'multifactorial' ] ],

    'egyptian_fractions' : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' + makeCommandExample( '45 67 egyptian_fractions' ) + '''
''' + makeCommandExample( '45 67 egyptian_fractions sum 67 *' ),
[ 'nth_sylvester', 'fraction' ] ],

    'eta' : [
'number_theory', 'calculates the Dirichlet eta function for n',
'''
The eta function is also known as the "alternating zeta function".
''',
'''
''',
[ 'zeta' ] ],

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
[ 'make_pyth_3', 'make_pyth_4' ] ],

    'euler_phi' : [
'number_theory', 'calculates Euler\'s totient function for n',
'''
''',
'''
''',
[ 'sigma' ] ],

    'factor' : [
'number_theory', 'calculates the prime factorization of n',
'''
rpnChilada's native prime factoring capability is fairly strong.  I've
incorporated code that utilizes Brent's Pollard Rho algorithm and
SIQS (the Self-Initializing Quadratic Sieve).

For better results, rpnChilada supports calling YAFU, which is probably
the most powerful piece of open-source factoring software available, and
is supported on most platforms.

https://sourceforge.net/projects/yafu/

Setting up YAFU is outside of the scope of this documentation.  In order to
take advantage of YAFU, please set the following configuration values:

'yafu_binary' needs to be set to the YAFU executable name.
'yafu_path' needs to be set to the location of the YAFU executable.

e.g.:

rpn yafu_binary 'yafu-x64.core2.exe set_config
rpn yafu_path 'c:\\app\\yafu set_config
''',
'''
''' + makeCommandExample( '8675309 factor' ) + '''
''' + makeCommandExample( '10000000000000000000001 factor' ) + '''
''' + makeCommandExample( '-a20 2 43 ** 1 - factor' ),
[ 'reduce', 'divisors' ] ],

    'factorial' : [
'number_theory', 'calculates the prime factorization of n',
'''
'factorial' calculates the product of all whole numbers from 1 to n.
''',
'''
''' + makeCommandExample( '1 10 range factorial' ),
[ 'superfactorial', 'hyperfactorial', 'barnesg', 'gamma', 'double_factorial', 'subfactorial' ] ],

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
This shows the relationship between the Fibonacci numbers and the Lucas numbers:

''' + makeCommandExample( '1 30 2 range2 fib lambda x sqr 5 * 4 - eval sqrt 2 30 2 range2 fib lambda x sqr 5 * 4 + eval sqrt interleave' ) + '''
''' + makeCommandExample( '1 30 range lucas' ),
[ 'tribonacci', 'fibonorial', 'tetranacci', 'pentanacci', 'hexanacci', 'heptanacci', 'octanacci' ] ],

    'fibonorial' : [
'number_theory', 'calculates the product of the first n Fibonacci numbers',
'''
The name is a portmanteau of 'fibonacci' and 'factorial'.
''',
'''
''' + makeCommandExample( '1 10 range fibonorial' ),
[ 'fibonacci', 'factorial' ] ],

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
[ 'make_continued_fraction', 'continued_fraction' ] ],

    'frobenius' : [
'number_theory', 'calculates the frobenius number of a list of values with gcd > 1',
'''
The Frobenius number is the smallest number that is not a linear combination of
a list of operands.  The list of operands must have a greatest common
denominator of 1.

It is commonly associated with Chicken McNuggets from McDonalds, which are
sold in packages of 6, 9 and 20.   The Frobenius number for Chicken McNuggets
is 43, meaning that 43 is the smallest number of McNuggets

 also called the Chicken McNuggets number, as the
problem it relates
''',
'''
''',
[ 'solve_frobenius', 'count_frobenius' ] ],

    'gamma' : [
'number_theory', 'calculates the gamma function for n',
'''
From https://en.wikipedia.org/wiki/Gamma_function:

In mathematics, the gamma function (represented by Gamma) is one commonly used
extension of the factorial function to complex numbers. The gamma function is
defined for all complex numbers except the non-positive integers.  For any
positive integer n:

Gamma( n ) = ( n - 1 )!
''',
'''
''' + makeCommandExample( '1 10 range gamma' ) + '''
''' + makeCommandExample( 'i gamma' ) + '''
''' + makeCommandExample( '-1j gamma' ),
[ 'factorial', 'log_gamma' ] ],

    'generate_polydivisibles' : [
'number_theory', 'generates all the polydivisible numbers for base n',
'''
''',
'''
''' + makeCommandExample( '2 generate_polydivisibles' ) + '''
''' + makeCommandExample( '3 generate_polydivisibles' ),
[ 'is_polydivisible' ] ],

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
[ 'linear_recurrence', 'nth_linear_recurrence' ] ],

    'harmonic_fraction' : [
'number_theory', 'returns the rational version of the nth harmonic number',
'''
The harmonic series consists of the sums of the reciprocals of the natural
numbers.  They are all rational numbers, so it's possible to represent
them as fractions.

This is an exact calculation, so while it's possible to get the value of the
googolth harmonic number (to a limited precision), calculating a large harmonic
fraction is far more limited.
''',
'''
''' + makeCommandExample( '1 harmonic_fraction' ) + '''
''' + makeCommandExample( '5 harmonic_fraction' ) + '''
''' + makeCommandExample( '-a20 50 harmonic_fraction' ) + '''
''' + makeCommandExample( '-a50 100 harmonic_fraction' ),
[ 'alternating_harmonic_fraction' ] ],

    'harmonic_residue' : [
'number_theory', 'returns the harmonic residue of n',
'''
The harmonic residue is the remainder of the product of n and the divisor
count of n, divided by the sum of the divisors of n.
''',
'''
''' + makeCommandExample( '1 10 range harmonic_residue' ) + '''
''' + makeCommandExample( '1 10 range nth_perfect_number harmonic_residue' ),
[ 'digital_root', 'crt' ] ],

    'heptanacci' : [
'number_theory', 'calculates the nth Heptanacci number',
'''
''',
'''
The first several heptanacci numbers:
''' + makeCommandExample( '1 20 range heptanacci', indent=4 ) + '''
The Heptanacci constant:
''' + makeCommandExample( 'infinity lambda x 6 + heptanacci x 5 + heptanacci / limit', indent=4 ),
[ 'fibonacci' ] ],

    'hexanacci' : [
'number_theory', 'calculates the nth Hexanacci number',
'''
''',
'''
The first several hexanacci numbers:
''' + makeCommandExample( '1 20 range hexanacci', indent=4 ) + '''
The Hexanacci constant:
''' + makeCommandExample( 'infinity lambda x 5 + hexanacci x 4 + hexanacci / limit', indent=4 ),
[ 'fibonacci' ] ],

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
[ 'factorial', 'superfactorial' ] ],

    'is_abundant' : [
'number_theory', 'returns whether or not n is an abundant number',
'''
An abundant number or excessive number is a number for which the sum of its
proper divisors is greater than the number itself.  The integer 12 is the
first abundant number.  Its proper divisors are 1, 2, 3, 4 and 6 for a total
of 16.  The amount by which the sum exceeds the number is the abundance.  The
number 12 has an abundance of 4, for example.

Ref:  https://en.wikipedia.org/wiki/Abundant_number
''',
'''
The first several abundant numbers:
''' + makeCommandExample( '1 80 range lambda x is_abundant filter' ),
[ 'abundance', 'abundance_ratio' ] ],

    'is_achilles' : [
'number_theory', 'returns whether or not n is an Achilles number',
'''
From: https://en.wikipedia.org/wiki/Achilles_number:

An Achilles number is a number that is powerful but not a perfect power.  A
positive integer n is a powerful number if, for every prime factor p of n,
p^2 is also a divisor.  In other words, every prime factor appears at least
squared in the factorization.  All Achilles numbers are powerful.  However,
not all powerful numbers are Achilles numbers:  only those that cannot be
represented as mk, where m and k are positive integers greater than 1.

Achilles numbers were named by Henry Bottomley after Achilles, a hero of the
Trojan war, who was also powerful but imperfect.  Strong Achilles numbers are
Achilles numbers whose Euler totients are also Achilles numbers.
''',
'''
''' + makeCommandExample( '1 1000 range lambda x is_achilles filter' ),
[ ] ],

    'is_antiharmonic' : [
'number_theory', 'returns whether or not n is an antiharmonic number',
'''
A number is antiharmonic if the sum of the squares of its divisors divides the
sum of its divisors.
''',
'''
The first several antiharmonic numbers:
''' + makeCommandExample( '1 150 range lambda x is_antiharmonic filter' ),
[ ] ],

    'is_carmichael' : [
'number_theory', 'returns whether n is a Carmichael number',
'''
''',
'''
''' + makeCommandExample( '1 10000 range lambda x is_carmichael filter' ),
[ ] ],

    'is_composite' : [
'number_theory', 'returns whether n is composite',
'''
A composite number is one that has more than one prime factor.
''',
'''
''' + makeCommandExample( '1 20 range lambda x is_composite filter' ),
[ 'is_prime' ] ],

    'is_deficient' : [
'number_theory', 'returns whether or not n is a deficient number',
'''
A deficient number is a number n for which the sum of divisors is less than
twice n.

Ref:  https://en.wikipedia.org/wiki/Deficient_number
''',
'''
The first several deficient numbers:
''' + makeCommandExample( '1 25 range lambda x is_deficient filter' ),
[ 'is_abundant', 'is_perfect' ] ],

    'is_friendly' : [
'number_theory', 'returns whether list n is a list of mutually friendly numbers',
'''
''',
'''
''',
[ ] ],

    'is_harmonic_divisor_number' : [
'number_theory', 'returns whether or not n is a harmonic divisor number',
'''
A harmonic divisor number, or Ore number (named after Oystein Ore who defined
it in 1948), is a positive integer whose divisors have a harmonic mean that is
an integer.

Ref:  https://en.wikipedia.org/wiki/Harmonic_divisor_number
''',
'''
The first few harmonic divisor numbers:
''' + makeCommandExample( '-a45 1 500 range lambda x is_harmonic_divisor_number filter' ),
[ 'harmonic_mean' ] ],

    'is_k_hyperperfect' : [
'number_theory', 'returns whether an integer n is k hyperperfect',
'''
''',
'''
''',
[ 'is_k_perfect', 'is_perfect' ] ],

    'is_k_perfect' : [
'number_theory', 'returns whether an integer n is k perfect',
'''
''',
'''
''',
[ 'is_k_hyperperfect', 'is_perfect' ] ],

    'is_k_semiprime' : [
'number_theory', 'returns whether n is a k-factor square-free number',
'''
A number is k-semiprime if is the product of k prime factors, and those factors
do not need to be unique.  To determine if a number has k unique prime factors,
use 'is_k_sphenic'.
''',
'''
''' + makeCommandExample( '20 29 range lambda x 2 is_k_semiprime filter' ) + '''
''' + makeCommandExample( '101 120 range lambda x 3 is_k_semiprime filter' ) + '''
''' + makeCommandExample( '101 120 range lambda x 3 is_k_semiprime filter factor -s1' ) + '''
''' + makeCommandExample( '1000 1300 range lambda x 7 is_k_semiprime filter' ),
[ 'is_prime', 'is_semiprime', 'is_k_sphenic' ] ],

    'is_k_sphenic' : [
'number_theory', 'returns whether n is a product of k distinct primes',
'''
This is my terminology, generalizing the idea of 'sphenic' to having an
arbitrary number of squarefree factors.

This terminology is not used, as far as I can tell, but there does not seem to
be an appropriate term to describe having a squarefree number of other than 1
(prime) or 3 (sphenic) factors.
''',
'''
''' + makeCommandExample( '1 100 range lambda x 3 is_k_sphenic filter' ) + '''
Fewer numbers are k_sphenic than k_semiprime because sphenic numbers must have
unique factors:

''' + makeCommandExample( '70 100 range lambda x 3 is_k_sphenic filter' ) + '''
''' + makeCommandExample( '70 100 range lambda x 3 is_k_semiprime filter' ) + '''
''' + makeCommandExample( '10 primorial 10 is_k_sphenic' ),
[ 'is_prime', 'is_k_semiprime', 'is_semiprime', 'is_sphenic' ] ],

    'is_perfect' : [
'number_theory', 'returns whether or not n is a perfect number',
'''
A perfect number is a positive integer that is equal to the sum of its proper
positive divisors, that is, the sum of its positive divisors excluding the
number itself (also known as its aliquot sum).  Equivalently, a perfect number
is a number that is half the sum of all of its positive divisors (including
itself) i.e. s1(n) = 2n.

Ref:  https://en.wikipedia.org/wiki/Perfect_number
''',
'''
The first few perfect numbers:
''' + makeCommandExample( '1 500 range lambda x is_perfect filter' ),
[ 'nth_perfect_number', 'is_abundant', 'is_deficient', 'is_k_perfect', 'is_k_hyperperfect' ] ],

    'is_pernicious' : [
'number_theory', 'returns whether n is pernicious',
'''
A pernicious number has a prime number of ones in its binary representation.
''',
'''
''' + makeCommandExample( '1 30 range is_pernicious' ),
[ ] ],

    'is_polydivisible' : [
'number_theory', 'returns whether or not n is polydivisible',
'''
''',
'''
''' + makeCommandExample( '100 200 range lambda x is_polydivisible filter' ) + '''
''' + makeCommandExample( '102000 103000 range lambda x is_polydivisible filter' ),
[ 'is_divisible', 'generate_polydivisibles' ] ],

    'is_powerful' : [
'number_theory', 'returns whether n is a powerful number',
'''
From https://en.wikipedia.org/wiki/Powerful_number:

A powerful number is a positive integer m such that for every prime number p
dividing m, p^2 also divides m.  Equivalently, a powerful number is the product
of a square and a cube, that is, a number m of the form m = a^2b^3, where a and
b are positive integers.  Powerful numbers are also known as squareful,
square-full, or 2-full.  Paul Erdos and George Szekeres studied such numbers
and Solomon W. Golomb named such numbers powerful.
''',
'''
''' + makeCommandExample( '1 100 range lambda x is_powerful filter' ),
[ 'is_achilles', 'is_squarefree' ] ],

    'is_prime' : [
'number_theory', 'returns whether n is prime',
'''
My goal is optimize primality testing automatically so it can use the much
faster Miller-Rabin test without being unsure of the result.

Right now it's kind of dumb.  It just calls the old algorithm
for numbers smaller than a trillion.
''',
'''
''' + makeCommandExample( '1 50 range lambda x is_prime filter' ) + '''
''' + makeCommandExample( '1 100 range fibonacci lambda x is_prime filter' ) + '''
''' + makeCommandExample( '1 100 range triangular lambda x is_prime filter' ),
[ 'is_sphenic', 'is_semiprime', 'is_k_sphenic', 'is_strong_pseudoprime', 'is_composite' ] ],

    'is_pronic' : [
'number_theory', 'returns whether n is pronic',
'''
A pronic number is a number which is the product of two consecutive integers,
that is, a number of the form n(n + 1).  The study of these numbers dates back
to Aristotle.  They are also called oblong numbers, heteromecic numbers, or
rectangular numbers; however, the term "rectangular number" has also been
applied to the composite numbers.

All pronic numbers are even, and 2 is the only prime pronic number.  It is also
the only pronic number in the Fibonacci sequence and the only pronic Lucas
number.
''',
'''
''' + makeCommandExample( '1 200 range lambda x is_pronic filter' ) + '''
''' + makeCommandExample( '71 97 * is_pronic' ) + '''
''' + makeCommandExample( '[ 71 97 107 ] is_pronic' ),
[ 'is_sphenic', 'is_semiprime', 'is_prime' ] ],

    'is_rough' : [
'number_theory', 'returns whether n is a k-rough number',
'''
From https://en.wikipedia.org/wiki/Rough_number:

A k-rough number, as defined by Finch in 2001 and 2003, is a positive integer
whose prime factors are all greater than or equal to k.

1 is always considered k-rough for any k.

Therefore, by this definition, all numbers are 2-rough.
''',
'''
''' + makeCommandExample( '1 25 range lambda x 2 is_rough filter' ) + '''
''' + makeCommandExample( '1 25 range lambda x 3 is_rough filter' ) + '''
''' + makeCommandExample( '1 50 range lambda x 5 is_rough filter' ) + '''
''' + makeCommandExample( '1 50 range lambda x 7 is_rough filter' ),
[ 'is_smooth', 'is_unusual' ] ],

    'is_ruth_aaron' : [
'number_theory', 'returns whether n is a Ruth-Aaron number',
'''
    #  http://mathworld.wolfram.com/Ruth-AaronPair.html
''',
'''
''',
[ ] ],

    'is_semiprime' : [
'number_theory', 'returns whether n is a semiprime number',
'''
''',
'''
''' + makeCommandExample( '1 10 range is_semiprime' ),
[ 'is_prime', 'is_sphenic', 'is_k_sphenic' ] ],

    'is_smooth' : [
'number_theory', 'returns whether n is a k-smooth number',
'''
From https://en.wikipedia.org/wiki/Smooth_number:

In number theory, a n-smooth (or n-friable) number is an integer whose prime
factors are all less or equal to n.  For example, a 7-smooth number is a
number whose prime factors are all at most 7, so 49 = 7^2 and 15750 = 2 *
3^2 * 5^3 * 7 are both 7-smooth, while 11 and 702 = 2 * 3^3 * 13 are not
7-smooth.  The term seems to have been coined by Leonard Adleman.  Smooth
numbers are especially important in cryptography, which relies on factorization
of integers.  The 2-smooth numbers are just the powers of 2, while 5-smooth
numbers are known as regular numbers.
''',
'''
''' + makeCommandExample( '1 100 range lambda x 2 is_smooth filter' ) + '''
''' + makeCommandExample( '1 100 range lambda x 3 is_smooth filter' ) + '''
''' + makeCommandExample( '1 100 range lambda x 5 is_smooth filter' ),
[ 'is_rough', 'is_unusual' ] ],

    'is_sphenic' : [
'number_theory', 'returns whether n is a sphenic number',
'''
''',
'''
''' + makeCommandExample( '1 20 range lambda x is_sphenic filter' ) + '''
''' + makeCommandExample( '71 97 * is_sphenic' ) + '''
''' + makeCommandExample( '[ 71 97 107 ] is_pronic' ),
[ 'is_k_sphenic', 'is_semiprime', 'is_prime' ] ],

    'is_squarefree' : [
'number_theory', 'returns whether n is a square-free number',
'''
A square-free number is a number that only has unique prime factors.
''',
'''
''' + makeCommandExample( '1 25 range lambda x is_squarefree filter' ),
[ 'is_semiprime', 'is_pronic' ] ],

    'is_strong_pseudoprime' : [
'number_theory', 'returns whether n is a strong pseudoprime to base k',
'''
''',
'''
''',
[ 'is_prime', 'is_k_sphenic', 'is_semiprime' ] ],

    'is_unusual' : [
'number_theory', 'returns whether n is an unusual number',
'''
From https://en.wikipedia.org/wiki/Unusual_number:

In number theory, an unusual number is a natural number n whose largest prime
factor is strictly greater than sqrt( n ).

A k-smooth number has all its prime factors less than or equal to k, therefore,
an unusual number is non-sqrt( n )-smooth.
''',
'''
''' + makeCommandExample( '1 25 range lambda x is_unusual filter' ),
[ 'is_prime', 'is_smooth', 'is_rough' ] ],

    'k_fibonacci' : [
'number_theory', 'calculates the nth K-Fibonacci number',
'''
''',
'''
''' + makeCommandExample( '1 10 range 2 k_fibonacci' ) + '''
''' + makeCommandExample( '1 10 range 3 k_fibonacci' ) + '''
''' + makeCommandExample( '10 2 10 range k_fibonacci' ),
[ 'fibonacci' ] ],

    'leyland_number' : [
'number_theory', 'returns the Leyland number for n and k',
'''
''',
'''
''',
[ ] ],

    'log_gamma' : [
'number_theory', 'calculates the loggamma function for n',
'''
The logarithm of the gamma function is treated as a special function.
''',
'''
''' + makeCommandExample( '0.1 loggamma' ) + '''
''' + makeCommandExample( '1 loggamma' ) + '''
''' + makeCommandExample( '2 loggamma' ) + '''
''' + makeCommandExample( '10 loggamma' ),
[ 'log', 'gamma' ] ],

    'linear_recurrence' : [
'number_theory', 'calculates the first c values of a linear recurrence specified by a list of factors (a) and of seeds (b)',
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
[ 'linear_recurrence_with_modulo', 'nth_linear_recurrence', 'nth_linear_recurrence_with_modulo' ] ],

    'linear_recurrence_with_modulo' : [
'number_theory', 'calculates the first c values of a linear recurrence specified by a list of factors (a) and of seeds (b), where each successive result is taken modulo d',
'''
''',
'''
''',
[ 'linear_recurrence', 'nth_linear_recurrence', 'nth_linear_recurrence_with_modulo' ] ],

    'lucas' : [
'number_theory', 'calculates the nth Lucas number',
'''
The Lucas sequence works just like the Fibonacci sequence, but starts with
1 and 3, instead of 0 and 1.  It shares many properties with the Fibonacci
sequence.
''',
'''
''' + makeCommandExample( '1 17 range lucas' ),
[ 'fibonacci' ] ],

    'make_continued_fraction' : [
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''',
[ 'continued_fraction' ] ],

    'make_pyth_3' : [
'number_theory', 'makes a pythagorean triple given two integers, n and k, as seeds',
'''
''',
'''
''',
[ 'make_pyth_4', 'hypotenuse', 'pythagorean_triples' ] ],

    'make_pyth_4' : [
'number_theory', 'makes a pythagorean quadruple given two integers, n and k, as seeds',
'''
n and k cannot both be odd.
''',
'''
''',
[ 'make_pyth_3', 'hypotenuse' ] ],

    'nth_carol' : [
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''' + makeCommandExample( '1 20 range nth_carol' ) + '''
''' + makeCommandExample( '25337 nth_carol' ),
[ ] ],

    'nth_harmonic_number' : [
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
The harmonic series consists of the reciprocals of the natural numbers.
''',
'''
''' + makeCommandExample( '1 nth_harmonic_number' ) + '''
''' + makeCommandExample( '2 nth_harmonic_number' ) + '''
''' + makeCommandExample( '10000 nth_harmonic_number' ) + '''
''' + makeCommandExample( '1e100 nth_harmonic' ),
[ 'harmonic_fraction' ] ],

    'nth_kynea' : [
'number_theory', 'gets the nth Kynea number',
'''
A Kynea number is an integer of the form 4 ^ n + 2 ^ ( n + 1 ) - 1, studied by
Cletus Emmanuel.  The nth Kynea number is also equal to the nth power of 4
added to the (n + 1)th Mersenne number.
''',
'''
''' + makeCommandExample( '1 20 range nth_kynea' ) + '''
''' + makeCommandExample( '63598 nth_kynea' ),
[ 'nth_mersenne_prime', 'nth_carol', 'nth_jacobsthal' ] ],

    'nth_jacobsthal' : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
''',
'''
''' + makeCommandExample( '1 20 range nth_jacobsthal' ) + '''
''' + makeCommandExample( '4783 nth_jacobsthal' ),
[ ] ],

    'nth_linear_recurrence' : [
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
''',
'''
The 20th Fibonacci number:
''' + makeCommandExample( '[ 1 1 ] [ 0 1 ] 20 nth_linear_recurrence', indent=4 ) + '''
The 17th Lucas number:
''' + makeCommandExample( '[ 1 1 ] [ 1 3 ] 17 nth_linear_recurrence', indent=4 ) + '''
The 43rd Tribonacci sequence:
''' + makeCommandExample( '[ 1 1 1 ] [ 0 0 1 ] 43 nth_linear_recurrence', indent=4 ) + '''
The 12th Octanacci sequence:
''' + makeCommandExample( '[ 1 8 dup ] [ 0 7 dup 1 ] 12 nth_linear_recurrence', indent=4 ) + '''
The 15th Pell number:
''' + makeCommandExample( '[ 1 2 ] [ 0 1 ] 15 nth_linear_recurrence', indent=4 ) + '''
The 21st Perrin number:
''' + makeCommandExample( '[ 1 1 0 ] [ 3 0 2 ] 21 nth_linear_recurrence', indent=4 ),
[ 'linear_recurrence_with_modulo', 'nth_linear_recurrence', 'nth_linear_recurrence_with_modulo' ] ],

    'nth_linear_recurrence_with_modulo' : [
'number_theory', 'calculates the cth value of a linear recurrence specified by a list of factors (a) and of seeds (b), where each successive result is taken modulo d',
'''
THis allows for the calculation of linear recurrences when only a modular
answer is required.  This means that it is far faster to calculate than working
out the full value of the linear recurrence.
''',
'''
The last 6 digits of the 20000th Fibonacci number:
''' + makeCommandExample( '[ 1 1 ] [ 0 1 ] 20000 100000 nth_linear_recurrence_with_modulo', indent=4 ),
[ 'linear_recurrence', 'nth_linear_recurrence', 'linear_recurrence_with_modulo' ] ],

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
'number_theory', 'returns the exponent in the nth Mersenne prime',
'''
These values are stored in a look-up table.  They are not calculated. ;-)

There are currently 51 known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.

https://primes.utm.edu/mersenne/index.html
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_mersenne_exponent' ) + '''
''' + makeCommandExample( '51 nth_mersenne_exponent' ),
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

    'nth_merten' : [
'number_theory', 'returns Merten\'s function for n',
'''
''',
'''
''' + makeCommandExample( '1 20 range nth_merten' ) + '''
''' + makeCommandExample( '3563 nth_merten' ),
[ ] ],

    'nth_mobius' : [
'number_theory', 'calculates the Mobius function for n',
'''
''',
'''
''' + makeCommandExample( '1 20 range nth_mobius' ) + '''
''' + makeCommandExample( '4398 nth_mobius' ),
[ ] ],

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
There are currently 51 known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_perfect_number' ) + '''
''' + makeCommandExample( '49 nth_perfect_number' ),
[ 'is_perfect', 'nth_mersenne_exponent' ] ],

    'nth_stern' : [
'number_theory', 'calculates the nth value of the Stern diatomic series',
'''
''',
'''
The first 20 members of the Stern sequence:
''' + makeCommandExample( '1 20 range nth_stern', indent=4 ),
[ ] ],

    'nth_thabit' : [
'number_theory', 'gets the nth Thabit number',
'''
''',
'''
''' + makeCommandExample( '1 20 range nth_thabit' ) + '''
''' + makeCommandExample( '2375 nth_thabit' ),
[ ] ],

    'nth_thue_morse' : [
'number_theory', 'calculates the nth value of the Thue-Morse sequence',
'''
''',
'''
The first 20 members of the Thue Morse sequence:
''' + makeCommandExample( '1 20 range nth_thue_morse', indent=4 ),
[ ] ],

    'octanacci' : [
'number_theory', 'calculates the nth Octanacci number',
'''
''',
'''
The first several octanacci numbers:
''' + makeCommandExample( '1 20 range octanacci', indent=4 ) + '''
The Octanacci constant:
''' + makeCommandExample( 'infinity lambda x 7 + octanacci x 6 + octanacci / limit', indent=4 ),
[ 'fibonacci' ] ],

    'pascal_triangle' : [
'number_theory', 'calculates the nth line of Pascal\'s triangle',
'''
''',
'''
The first 10 lines of Pascal's triangle:
''' + makeCommandExample( '1 10 range pascal_triangle -s1' ),
[ 'nth_catalan' ] ],

    'pentanacci' : [
'number_theory', 'calculates the nth Pentanacci number',
'''
''',
'''
The first several pentanacci numbers:
''' + makeCommandExample( '1 20 range pentanacci', indent=4 ) + '''
The Pentanacci constant:
''' + makeCommandExample( 'infinity lambda x 4 + pentanacci x 3 + pentanacci / limit', indent=4 ),
[  'fibonacci' ] ],

    'polygamma' : [
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''' + makeCommandExample( '5 6 polygamma' ),
[ 'gamma', 'trigamma' ] ],

    'polygorial' : [
'number_theory', 'calculates the polygamma function for n',
'''
http://danieldockery.com/res/math/polygorials.pdf
''',
'''
''' + makeCommandExample( '1 10 range 3 polygorial' ) + '''
''' + makeCommandExample( '1 10 range 4 polygorial' ) + '''
''' + makeCommandExample( '5 6 polygorial' ),
[ 'factorial', 'phitorial', 'primorial' ] ],

    'phitorial' : [
'number_theory', 'calculates the nth photorial',
'''
This function calculates the product of all numbers between 1 and n, which are
relatively prime to n.
''',
'''
The first several phitorial numbers:
''' + makeCommandExample( '1 10 range phitorial', indent=4 ),
[ 'factorial', 'primorial' ] ],

    'primorial' : [
'number_theory', 'calculates the nth primorial',
'''
This function calculates the product of the first n prime numbers.
''',
'''
''' + makeCommandExample( '1 10 range primorial' ),
[ 'factorial', 'phitorial', 'prime' ] ],

    'pythagorean_triples' : [
'number_theory', 'calculates all primitive pythagorean triples with a hypotenuse length up to n',
'''
Primitive pythagorean triples are triples where the individual numbers do not
a common factor.
''',
'''
''' + makeCommandExample( '50 pythagorean_triples -s1' ),
[ 'make_pyth_3', 'make_pyth_4' ] ],

    'relatively_prime' : [
'number_theory', 'calculates whether n and k are relatively prime',
'''
Numbers are relatively prime if their great common denominator is 1.
''',
'''
''' + makeCommandExample( '5 8 relatively_prime' ) + '''
All the numbers from 1-20 that are relatively prime with 20:
''' + makeCommandExample( '1 20 range lambda y x relatively_prime filter_integers', indent=4 ),
[ 'reduce', 'lcm', 'gcd', 'gcd2' ] ],

    'repunit' : [
'number_theory', 'returns the nth repunit in base k',
'''
A repunit for base-k is a number consisting of entirely of the digit 1 in that
base.
''',
'''
''' + makeCommandExample( '11 10 repunit' ) + '''
''' + makeCommandExample( '11 4 repunit -r4' ) + '''
''' + makeCommandExample( '11 4 repunit' ),
[ 'has_digits', 'is_digital_palindrome', 'duplicate_digits' ] ],

    'radical' : [
'number_theory', 'returns the value of the radical function for n',
'''
The radical function is defined as the largest squarefree factor.
''',
'''
''' + makeCommandExample( '1 100 range radical' ),
[ 'harmonic_residue', 'digital_root' ] ],

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

    'solve_frobenius' : [
'number_theory', 'produces a list of coefficients of solutions to Frobenius equation n equal to k',
'''
''',
'''
''',
[ 'frobenius', 'count_frobenius' ] ],

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
[ 'factorial', 'double_factorial', 'superfactorial' ] ],

    'sums_of_k_powers' : [
'number_theory', 'calculates every combination of b cth powers that sum to n',
'''
''',
'''
''' + makeCommandExample( '5104 3 3 sums_of_k_powers' ),
[ 'sums_of_k_nonzero_powers' ] ],

    'sums_of_k_nonzero_powers' : [
'number_theory', 'calculates every combination of b nonzero cth powers that sum to n',
'''
''',
'''
''' + makeCommandExample( '1072 3 3 sums_of_k_nonzero_powers' ),
[ 'sums_of_k_powers' ] ],

    'superfactorial' : [
'number_theory', 'calculates the superfactorial of n',
'''
The superfactorial function is defined by Sloane and Plouffe to be the product
of the first n factorials, which is the equivalent of the integral values of
the Barnes G-function.
''',
'''
''' + makeCommandExample( '-a30 1 10 range superfactorial' ),
[ 'barnesg', 'factorial' ] ],

    'tetranacci' : [
'number_theory', 'calculates the nth Tetranacci number',
'''
''',
'''
The first several tetranacci numbers:
''' + makeCommandExample( '1 20 range tetranacci', indent=4 ) + '''
The Tetranacci constant:
''' + makeCommandExample( 'infinity lambda x 3 + tetranacci x 2 + tetranacci / limit', indent=4 ),
[ 'fibonacci' ] ],

    'tribonacci' : [
'number_theory', 'calculates the nth Tribonacci number',
'''
''',
'''
The first several tribonacci numbers:
''' + makeCommandExample( '1 20 range tribonacci', indent=4 ) + '''
The Tribonacci constant:
''' + makeCommandExample( 'infinity lambda x 2 + tribonacci x 1 + tribonacci / limit', indent=4 ),
[ 'fibonacci' ] ],

    'trigamma' : [
'number_theory', 'calculates the trigamma function for n',
'''
This is the equivalent of '1 n polygamma'.
''',
'''
''' + makeCommandExample( '23 trigamma' ),
[ 'polygamma' ] ],

    'unit_roots' : [
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
''' + makeCommandExample( '2 unit_roots' ) + '''
''' + makeCommandExample( '3 unit_roots' ) + '''
''' + makeCommandExample( '4 unit_roots' ),
[ 'root' ] ],

    'zeta' : [
'number_theory', 'calculates Riemann\'s zeta function for n',
'''
''',
'''
''' + makeCommandExample( '2 zeta' ),
[ 'hurwitz_zeta', 'eta' ] ],

    'zeta_zero' : [
'number_theory', 'calculates the nth non-trivial zero of Riemann\'s zeta function',
'''
''',
'''
''' + makeCommandExample( '1 5 range zeta_zero' ),
[ 'zeta' ] ],


    #******************************************************************************
    #
    #  physics operators
    #
    #******************************************************************************

    'acceleration' : [
'physics', 'calculates acceleration given different measurement types',
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
'physics', 'calculates the entropy of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_entropy' ) + '''
''' + makeCommandExample( '1 year black_hole_entropy' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_entropy' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_entropy' ) + '''
''' + makeCommandExample( 'gee black_hole_entropy' ) + '''
''' + makeCommandExample( '100 tons black_hole_entropy' ),
[ 'black_hole_mass', 'black_hole_surface_gravity', 'black_hole_surface_area', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'black_hole_surface_tides' ] ],

    'black_hole_lifetime' : [
'physics', 'calculates the lifetime of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_lifetime' ) + '''
''' + makeCommandExample( '1 year black_hole_lifetime' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_lifetime' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_lifetime' ) + '''
''' + makeCommandExample( '1.0e12 kg black_hole_lifetime' ) + '''
''' + makeCommandExample( 'gee black_hole_lifetime' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_area', 'black_hole_temperature', 'black_hole_surface_gravity', 'black_hole_luminosity', 'black_hole_surface_tides' ] ],

    'black_hole_luminosity' : [
'physics', 'calculates the luminosity of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_luminosity' ) + '''
''' + makeCommandExample( '1 year black_hole_luminosity' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_luminosity' ) + '''
''' + makeCommandExample( '1.0e16 kg black_hole_luminosity' ) + '''
''' + makeCommandExample( 'gee black_hole_luminosity' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_area', 'black_hole_temperature', 'black_hole_surface_gravity', 'black_hole_lifetime', 'black_hole_surface_tides' ] ],

    'black_hole_mass' : [
'physics', 'calculates the mass of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_mass' ) + '''
''' + makeCommandExample( '1 year black_hole_mass' ) + '''
''' + makeCommandExample( '373 kelvin black_hole_mass' ) + '''
''' + makeCommandExample( '1 billion watts black_hole_mass' ) + '''
''' + makeCommandExample( '10 gee black_hole_mass' ),
[ 'black_hole_surface_area', 'black_hole_surface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'black_hole_surface_tides' ] ],

    'black_hole_radius' : [
'physics', 'calculates the Schwarzchild radius of a black hole of mass n',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( 'earth_mass black_hole_radius' ) + '''
''' + makeCommandExample( '10 solar_mass black_hole_radius' ) + '''
''' + makeCommandExample( '100 miles^2 black_hole_radius' ) + '''
''' + makeCommandExample( '10000 years black_hole_radius' ) + '''
''' + makeCommandExample( '3 kelvin black_hole_radius' ) + '''
''' + makeCommandExample( '1 trillion watts black_hole_radius' ) + '''
''' + makeCommandExample( '100 gee black_hole_radius' ),
[ 'black_hole_surface_area', 'black_hole_surface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'black_hole_surface_tides' ] ],

    'black_hole_surface_area' : [
'physics', 'calculates the surface area of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1000 miles^2 black_hole_surface_area' ) + '''
''' + makeCommandExample( '15 minutes black_hole_surface_area' ) + '''
''' + makeCommandExample( '1.0e12 kelvin black_hole_surface_area' ) + '''
''' + makeCommandExample( '1 sextillion watts black_hole_surface_area' ) + '''
''' + makeCommandExample( '1.0e25 gee black_hole_surface_area' ),
[ 'black_hole_mass', 'black_hole_surface_gravity', 'black_hole_entropy', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'black_hole_surface_tides' ] ],

    'black_hole_surface_gravity' : [
'physics', 'calculates the surface gravity of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1 acre black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '1 million years black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '1.0e15 kelvin black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '60 watts black_hole_surface_gravity' ) + '''
''' + makeCommandExample( '2000 gee black_hole_surface_gravity' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_area', 'black_hole_temperature', 'black_hole_luminosity', 'black_hole_lifetime', 'surface_gravity', 'black_hole_surface_tides' ] ],

    'black_hole_surface_tides' : [
'physics', 'calculates the tidal force at the event horizon of a black hole given one of several different measurements',
'''
Tidal force is meters/second^2/meter, which means the meters cancel out and
it ends up being 1/second^2, which I found confusing, but it makes sense if you
think about it.

https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '100 square_inch black_hole_surface_tides' ) + '''
''' + makeCommandExample( '1 quadrillion years black_hole_surface_tides' ) + '''
''' + makeCommandExample( '273 kelvin black_hole_surface_tides' ) + '''
''' + makeCommandExample( '1 thousand watts black_hole_surface_tides' ) + '''
''' + makeCommandExample( '100 gee black_hole_surface_tides' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_area', 'black_hole_lifetime', 'black_hole_surface_gravity', 'black_hole_luminosity', 'black_hole_temperature' ] ],

    'black_hole_temperature' : [
'physics', 'calculates the temperature of a black hole given one of several different measurements',
'''
https://www.vttoth.com/CMS/physics-notes/311-hawking-radiation-calculator
''',
'''
''' + makeCommandExample( '1 square_inch black_hole_temperature' ) + '''
''' + makeCommandExample( '14 billion years black_hole_temperature' ) + '''
''' + makeCommandExample( '273 kelvin black_hole_temperature' ) + '''
''' + makeCommandExample( '1 million watts black_hole_temperature' ) + '''
''' + makeCommandExample( '0.01 gee black_hole_temperature' ),
[ 'black_hole_mass', 'black_hole_entropy', 'black_hole_surface_area', 'black_hole_lifetime', 'black_hole_surface_gravity', 'black_hole_luminosity', 'black_hole_surface_tides' ] ],

    'distance' : [
'physics', 'calculates distance given different measurement types',
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
[ 'mass_equivalence' ] ],

    'escape_velocity' : [
'physics', 'calculates the escape velocity of an object of mass n and radius k',
'''
''',
'''
''',
[ 'velocity', 'acceleration', 'orbital_velocity' ] ],

    'heat_index' : [
'physics', 'calculates the heat index given the temperature and the relative humidity',
'''
Ref:  https://en.wikipedia.org/wiki/Heat_index
''',
'''
''' + makeCommandExample( '90 degrees_F 50 percent heat_index' ) + '''
''' + makeCommandExample( '30 degrees_C 80 percent heat_index' ),
[ 'wind_chill' ] ],

    'horizon_distance' : [
'physics', 'calculates the distance to the horizon for altitude n on a body of radius k (assuming the body is a perfect sphere)',
'''
''',
'''
''',
[ ] ],

    'kinetic_energy' : [
'physics', 'calculates kinetic energy from velocity and mass',
'''
The kinetic energy is equal to 1/2 mass times velocity squared.
''',
'''
''',
[ 'velocity', 'acceleration', 'escape_velocity' ] ],

    'mass_equivalence' : [
'physics', 'calculates the mass equivalence of energy n',
'''
This is calculated simply using Einstein's energy/mass equivalence formula
E = mc^2, which solved for m gives, m = E/c^2
''',
'''
''' + makeCommandExample( '1 gallon_of_gasoline mass_equivalence' ) + '''
''' + makeCommandExample( '1 ton_of_tnt mass_equivalence' ),
[ 'energy_equivalence' ] ],

    'orbital_mass' : [
'physics', 'calculates the mass of the object being orbited',
'''
Any two of the following three measurements can be used (in any order) as
arguments:

    orbital period,
    orbital velocity,
    orbit radius (the distance between the centers of mass)

Mass returned is really the combined mass of the object orbiting and the
object being orbited.

''',
'''
''',
[ 'orbital_period', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_period' : [
'physics', 'calculates the orbital period of an object',
'''
Any two of the following three measurements can be used (in any order) as
arguments:

    mass (the combined mass of the two objects)
    orbit radius (the distance between the centers of mass)
    orbital velocity
''',
'''
''',
[ 'orbital_mass', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_radius' : [
'physics', 'calculates the radius of an orbit',
'''
Any two of the following three measurements can be used (in any order) as
arguments:

    mass (the combined mass of the two objects)
    orbital period
    orbital velocity
''',
'''
''',
[ 'orbital_mass', 'orbital_period', 'orbital_velocity' ] ],

    'orbital_velocity' : [
'physics', 'calculates the circular orbital velocity of an object for values n and k',
'''
Any two of the following three measurements can be used (in any order) as
arguments:

    mass (the combined mass of the two objects)
    orbit radius (the distance between the centers of mass)
    orbital period
''',
'''
''' + makeCommandExample( '24 hours earth_mass orbital_velocity' ) + '''
''' + makeCommandExample( 'earth_mass 100 miles orbital_velocity' ) + '''
''' + makeCommandExample( 'sun_mass solar_year orbital_velocity mph convert' ),
[ 'orbital_mass', 'orbital_period', 'orbital_radius' ] ],

    'surface_gravity' : [
'physics', 'calculates the surface gravity of a spherical object',
'''
Any two of the following three measurements can be used (in any order) as
arguments, except the two arguments cannot be radius and volume, because
the mass and density cnanot be calculated from only the radius and volume:

    density
    mass
    radius
    volume
''',
'''
''' + makeCommandExample( 'earth_mass earth_radius surface_gravity' ) + '''
''' + makeCommandExample( '5.51 g/cm^3 earth_volume surface_gravity' ) + '''
Calculate the surface gravity of a 10-solar-mass black hole:
''' + makeCommandExample( '10 solar_mass 10 solar_mass black_hole_radius surface_gravity', indent=4 ) + '''
''' + makeCommandExample( '10 solar_mass black_hole_surface_gravity', indent=4 ),
[ 'black_hole_surface_gravity' ] ],

    'tidal_force' : [
'physics', 'calculates the tidal_force due to gravity, given the mass (a), distance from the mass (b), and the distance difference (c)',
'''
https://en.wikipedia.org/wiki/Tidal_force#Formulation
''',
'''
''' + makeCommandExample( '500000 solar_mass previous black_hole_radius 500 meters tidal_force' ) + '''
Calculate the lunar tidal force on Earth for a delta of one meter (i.e., how
much tidal force affects an object one meter in size (assuming it's pointing
at the Moon).
''' + makeCommandExample( 'earth_mass 238900 miles 1 meter tidal_force' ),
[ ] ],

    'time_dilation' : [
'physics', 'calculates the relativistic time-dilation effect of a velocity difference of n',
'''
''',
'''
''' + makeCommandExample( '1 million mph time_dilation' ) + '''
''' + makeCommandExample( '0.99 c * time_dilation' ),
[ ] ],

    'velocity' : [
'physics', 'calculates velocity given different measurement types',
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

    'wind_chill' : [
'physics', 'calculates the wind chill given the temperature and the wind',
'''
Ref:  https://en.wikipedia.org/wiki/Wind_chill
''',
'''
''' + makeCommandExample( '32 degrees_F 10 mph wind_chill' ) + '''
''' + makeCommandExample( '0 degrees_C 20 m/s wind_chill' ),
[ 'heat_index' ] ],


    #******************************************************************************
    #
    #  figurate number operators
    #
    #******************************************************************************

    'centered_cube' : [
'figurate_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_cube' ) + '''
''' + makeCommandExample( '1000 centered_cube' ),
[ 'cube', 'centered_polygonal' ] ],

    'centered_decagonal' : [
'figurate_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_decagonal' ) + '''
''' + makeCommandExample( '5413 centered_decagonal' ),
[ 'decagonal', 'centered_polygonal', 'nth_centered_decagonal' ] ],

    'centered_dodecahedral' : [
'figurate_numbers', 'calculates the nth centered dodecahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_dodecahedral' ) + '''
''' + makeCommandExample( '4890 centered_dodecahedral' ),
[ 'dodecahedral', 'centered_tetrahedral', 'centered_octahedral', 'centered_icosahedral' ] ],

    'centered_heptagonal' : [
'figurate_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_heptagonal' ) + '''
''' + makeCommandExample( '13112 centered_heptagonal' ),
[ 'heptagonal', 'centered_polygonal', 'nth_centered_heptagonal' ] ],

    'centered_hexagonal' : [
'figurate_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_hexagonal' ) + '''
''' + makeCommandExample( '73817 centered_hexagonal' ),
[ 'hexagonal', 'centered_polygonal', 'nth_centered_hexagonal' ] ],

    'centered_icosahedral' : [
'figurate_numbers', 'calculates the nth centered icosahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_icosahedral' ) + '''
''' + makeCommandExample( '1243 centered_icosahedral' ),
[ 'icosahedral', 'centered_tetrahedral', 'centered_octahedral', 'centered_dodecahedral' ] ],

    'centered_nonagonal' : [
'figurate_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_nonagonal' ) + '''
''' + makeCommandExample( '8933 centered_nonagonal' ),
[ 'nonagonal', 'centered_polygonal', 'nth_centered_nonagonal' ] ],

    'centered_octagonal' : [
'figurate_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_octagonal' ) + '''
''' + makeCommandExample( '5012 centered_octagonal' ),
[ 'octagonal', 'centered_polygonal', 'nth_centered_octagonal' ] ],

    'centered_octahedral' : [
'figurate_numbers', 'calculates the nth centered octahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_octahedral' ) + '''
''' + makeCommandExample( '7476 centered_octahedral' ),
[ 'octahedral', 'centered_tetrahedral', 'centered_icosahedral', 'centered_dodecahedral' ] ],

    'centered_pentagonal' : [
'figurate_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_pentagonal' ) + '''
''' + makeCommandExample( '9654 centered_pentagonal' ),
[ 'pentagonal', 'centered_polygonal', 'nth_centered_pentagonal' ] ],

    'centered_polygonal' : [
'figurate_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range 3 centered_polygonal' ) + '''
''' + makeCommandExample( '2 3 10 range centered_polygonal' ) + '''
''' + makeCommandExample( '5 3 10 range centered_polygonal' ) + '''
''' + makeCommandExample( '96 43 centered_polygonal' ),
[ 'nth_centered_polygonal', 'polygonal' ] ],

    'centered_square' : [
'figurate_numbers', 'calculates the nth centered square number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_square' ) + '''
''' + makeCommandExample( '11452 centered_square' ),
[ 'square', 'centered_polygonal', 'nth_centered_square' ] ],

    'centered_tetrahedral' : [
'figurate_numbers', 'calculates the nth centered tetrahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_tetrahedral' ) + '''
''' + makeCommandExample( '10000 centered_tetrahedral' ),
[ 'tetrahedral', 'centered_octahedral', 'centered_icosahedral', 'centered_dodecahedral' ] ],

    'centered_triangular' : [
'figurate_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''' + makeCommandExample( '1 10 range centered_triangular' ) + '''
''' + makeCommandExample( '1000 centered_triangular' ),
[ 'triangular', 'centered_polygonal', 'nth_centered_triangular' ] ],

    'decagonal' : [
'figurate_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range decagonal' ) + '''
''' + makeCommandExample( '5000 decagonal' ),
[ 'centered_decagonal', 'polygonal', 'nth_decagonal' ] ],

    'decagonal_centered_square' : [
'figurate_numbers', 'calculates the nth decagonal centered square number',
'''
'decagonal_centered_square' calculates the nth number that is both decagonal and
centered square.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_centered_square' ) + '''
''' + makeCommandExample( '59 decagonal_centered_square' ),
[ 'decagonal', 'centered_square', 'polygonal', 'centered_polygonal' ] ],

    'decagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
'decagonal_heptagonal' calculates the nth number that is both decagonal and
heptagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_heptagonal' ) + '''
''' + makeCommandExample( '127 decagonal_heptagonal' ),
[ 'decagonal', 'heptagonal', 'polygonal' ] ],

    'decagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth decagonal hexagonal number',
'''
'decagonal_hexagonal' calculates the nth number that is both decagonal and
hexagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_hexagonal' ) + '''
''' + makeCommandExample( '5741 decagonal_hexagonal' ),
[ 'decagonal', 'hexagonal', 'polygonal' ] ],

    'decagonal_nonagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
'decagonal_heptagonal' calculates the nth number that is both decagonal and
heptagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_nonagonal' ) + '''
''' + makeCommandExample( '5762 decagonal_nonagonal' ),
[ 'decagonal', 'nonagonal', 'polygonal' ] ],

    'decagonal_octagonal' : [
'figurate_numbers', 'calculates the nth decagonal octagonal number',
'''
'decagonal_octagonal' calculates the nth number that is both decagonal and
octagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_octagonal' ) + '''
''' + makeCommandExample( '2111 decagonal_octagonal' ),
[ 'decagonal', 'octagonal', 'polygonal' ] ],

    'decagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth decagonal pentagonal number',
'''
'decagonal_pentagonal' calculates the nth number that is both decagonal and
pentgonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_pentagonal' ) + '''
''' + makeCommandExample( '12000 decagonal_pentagonal' ),
[ 'decagonal', 'pentagonal', 'polygonal' ] ],

    'decagonal_triangular' : [
'figurate_numbers', 'calculates the nth decagonal triangular number',
'''
'decagonal_triangular' calculates the nth number that is both decagonal and
triangular.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_triangular' ) + '''
''' + makeCommandExample( '351 decagonal_triangular' ),
[ 'decagonal', 'triangular', 'polygonal' ] ],

    'dodecahedral' : [
'figurate_numbers', 'returns the nth dodecahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range dodecahedral' ) + '''
''' + makeCommandExample( '507 dodecahedral' ),
[ 'centered_dodecahedral', 'rhombic_dodecahedral' ] ],

    'generalized_pentagonal' : [
'figurate_numbers', 'calculates the nth generalized pentagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range generalized_pentagonal' ) + '''
''' + makeCommandExample( '542 generalized_pentagonal' ),
[ 'pentagonal', 'polygonal' ] ],

    'heptagonal' : [
'figurate_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range heptagonal' ) + '''
''' + makeCommandExample( '27870 heptagonal' ),
[ 'hexagonal', 'octagonal', 'polygonal' ] ],

    'heptagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth heptagonal hexagonal number',
'''
'heptagonal_hexagonal' calculates the nth number that is both heptagonal and
hexagonal.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_hexagonal' ) + '''
''' + makeCommandExample( '911 heptagonal_hexagonal' ),
[ 'heptagonal', 'hexagonal', 'polygonal' ] ],

    'heptagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth heptagonal pentagonal number',
'''
'heptagonal_pentagonal' calculates the nth number that is both heptagonal and
pentgonal.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_pentagonal' ) + '''
''' + makeCommandExample( '7027 heptagonal_pentagonal' ),
[ 'heptagonal', 'pentagonal', 'polygonal' ] ],

    'heptagonal_square' : [
'figurate_numbers', 'calculates the nth heptagonal square number',
'''
'heptagonal_square' calculates the nth number that is both heptagonal and
square.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_square' ) + '''
''' + makeCommandExample( '1813 heptagonal_square' ),
[ 'heptagonal', 'square', 'polygonal' ] ],

    'heptagonal_triangular' : [
'figurate_numbers', 'calculates the nth heptagonal triangular number',
'''
'heptagonal_triangular' calculates the nth number that is both heptagonal and
triangular.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_triangular' ) + '''
''' + makeCommandExample( '216 heptagonal_triangular' ),
[ 'heptagonal', 'triangular', 'polygonal' ] ],

    'hexagonal' : [
'figurate_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range hexagonal' ) + '''
''' + makeCommandExample( '7776 hexagonal' ),
[ 'pentagonal', 'heptagonal', 'polygonal' ] ],

    'hexagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth hexagonal pentagonal number',
'''
'hexagonal_pentagonal' calculates the nth number that is both hexagonal and
pentagonal.
''',
'''
''' + makeCommandExample( '1 10 range hexagonal_pentagonal' ) + '''
''' + makeCommandExample( '3125 hexagonal_pentagonal' ),
[ 'hexagonal', 'pentagonal', 'polygonal' ] ],

    'hexagonal_square' : [
'figurate_numbers', 'calculates the nth hexagonal square number',
'''
'hexagonal_square' calculates the nth number that is both hexagonal and
square.
''',
'''
''' + makeCommandExample( '1 10 range hexagonal_square' ) + '''
''' + makeCommandExample( '443 hexagonal_square' ),
[ 'hexagonal', 'square', 'polygonal' ] ],

    'icosahedral' : [
'figurate_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''' + makeCommandExample( '1 10 range icosahedral' ) + '''
''' + makeCommandExample( '400 icosahedral' ),
[ 'tetrahedral', 'octahedral', 'dodecahedral' ] ],

    'nonagonal' : [
'figurate_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''' + makeCommandExample( '1 10 range nonagonal' ) + '''
''' + makeCommandExample( '6561 nonagonal' ),
[ 'octagonal', 'decagonal', 'polygonal' ] ],

    'nonagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonagonal_heptagonal' calculates the nth number that is both nonagonal and
heptagonal.
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_heptagonal' ) + '''
''' + makeCommandExample( '273 nonagonal_heptagonal' ),
[ 'nonagonal', 'heptagonal', 'polygonal' ] ],

    'nonagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonagonal_hexagonal' calculates the nth number that is both nonagonal and
hexagonal.
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_hexagonal' ) + '''
''' + makeCommandExample( '256 nonagonal_hexagonal' ),
[ 'nonagonal', 'hexagonal', 'polygonal' ] ],

    'nonagonal_octagonal' : [
'figurate_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonagonal_octagonal' calculates the nth number that is both nonagonal and
octagonal.
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_octagonal' ) + '''
''' + makeCommandExample( '64 nonagonal_octagonal' ),
[ 'nonagonal', 'octagonal', 'polygonal' ] ],

    'nonagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonagonal_pentagonal' calculates the nth number that is both nonagonal and
pentgonal.
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_pentagonal' ) + '''
''' + makeCommandExample( '874 nonagonal_pentagonal' ),
[ 'nonagonal', 'pentagonal', 'polygonal' ] ],

    'nonagonal_square' : [
'figurate_numbers', 'calculates the nth nonagonal square number',
'''
'nonagonal_square' calculates the nth number that is both nonagonal and square.
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_square' ) + '''
''' + makeCommandExample( '656 nonagonal_square' ),
[ 'nonagonal', 'square', 'polygonal' ] ],

    'nonagonal_triangular' : [
'figurate_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonagonal_triangular' calculates the nth number that is both nonagonal and
triangular.

TODO: fix me
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_triangular' ) + '''
''' + makeCommandExample( '454 nonagonal_triangular' ),
[ 'nonagonal', 'triangular', 'polygonal' ] ],

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
[ 'centered_decagonal', 'nth_centered_polygonal' ] ],

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
[ 'centered_heptagonal', 'nth_centered_polygonal' ] ],

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
[ 'centered_hexagonal', 'nth_centered_polygonal' ] ],

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
[ 'centered_nonagonal', 'nth_centered_polygonal' ] ],

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
[ 'nth_centered_polygonal', 'centered_octagonal' ] ],

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
[ 'centered_pentagonal', 'nth_centered_polygonal' ] ],

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
[ 'centered_polygonal', 'polygonal' ] ],

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
[ 'centered_square', 'nth_centered_polygonal' ] ],

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
[ 'centered_triangular', 'nth_centered_polygonal' ] ],

    'nth_decagonal' : [
'figurate_numbers', 'finds the index of the decagonal number of value n',
'''
''',
'''
''',
[ 'decagonal', 'nth_polygonal', 'nth_centered_decagonal' ] ],

    'nth_hexagonal' : [
'figurate_numbers', 'finds the index of the hexagonal number of value n',
'''
''',
'''
''',
[ 'hexagonal', 'nth_polygonal', 'nth_centered_hexagonal' ] ],

    'nth_heptagonal' : [
'figurate_numbers', 'finds the index of the heptagonal number of value n',
'''
''',
'''
''',
[ 'heptagonal', 'nth_polygonal', 'nth_centered_heptagonal' ] ],

    'nth_nonagonal' : [
'figurate_numbers', 'finds the index of the nonagonal number of value n',
'''
''',
'''
''',
[ 'nonagonal', 'nth_polygonal', 'nth_centered_nonagonal' ] ],

    'nth_octagonal' : [
'figurate_numbers', 'finds the index of the octagonal number of value n',
'''
''',
'''
''',
[ 'octagonal', 'nth_polygonal', 'nth_centered_octagonal' ] ],

    'nth_pentagonal' : [
'figurate_numbers', 'finds the index of the pentagonal number of value n',
'''
''',
'''
''',
[ 'pentagonal', 'nth_polygonal', 'nth_centered_pentagonal' ] ],

    'nth_polygonal' : [
'figurate_numbers', 'finds the index of the polygonal number with k sides of value n',
'''
''',
'''
''',
[ 'polygonal', 'nth_centered_polygonal' ] ],

    'nth_square' : [
'figurate_numbers', 'finds the index of the square number of value n',
'''
''',
'''
''',
[ 'square', 'nth_polygonal' ] ],

    'nth_triangular' : [
'figurate_numbers', 'finds the index of the triangular number of value n',
'''
''',
'''
''',
[ 'triangular', 'nth_polygonal' ] ],

    'octagonal' : [
'figurate_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''' + makeCommandExample( '1 16 range octagonal' ) + '''
''' + makeCommandExample( '2685 octagonal' ),
[ 'centered_octagonal', 'polygonal' ] ],

    'octagonal_heptagonal' : [
'figurate_numbers', 'returns the nth octagonal heptagonal number',
'''
'octagonal_heptagonal' calculates the nth number that is both octagonal and
heptagonal.
''',
'''
''' + makeCommandExample( '-a22 1 5 range octagonal_heptagonal' ) + '''
''' + makeCommandExample( '-a40 13 octagonal_pentagonal' ),
[ 'octagonal', 'heptagonal' ] ],

    'octagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth octagonal hexagonal number',
'''
'octagonal_hexagonal' calculates the nth number that is both octagonal and
hexagonal.
''',
'''
''' + makeCommandExample( '-a20 1 5 range octagonal_hexagonal' ) + '''
''' + makeCommandExample( '-a50 12 octagonal_hexagonal' ),
[ 'octagonal', 'hexagonal' ] ],

    'octagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth octagonal pentagonal number',
'''
'octagonal_pentagonal' calculates the nth number that is both octagonal and
pentagonal.
''',
'''
''' + makeCommandExample( '-a20 1 6 range octagonal_pentagonal' ) + '''
''' + makeCommandExample( '-a50 17 octagonal_pentagonal' ),
[ 'octagonal', 'pentagonal' ] ],

    'octagonal_square' : [
'figurate_numbers', 'calculates the nth octagonal square number',
'''
'octagonal_square' calculates the nth number that is both octagonal and
square.
''',
'''
''' + makeCommandExample( '-a20 1 7 range octagonal_square' ) + '''
''' + makeCommandExample( '-a50 22 octagonal_square' ),
[ 'octagonal', 'square' ] ],

    'octagonal_triangular' : [
'figurate_numbers', 'calculates the nth octagonal triangular number',
'''
'octagonal_triangular' calculates the nth number that is both octagonal and
triangular.
''',
'''
''' + makeCommandExample( '-a20 1 8 range octagonal_triangular' ) + '''
''' + makeCommandExample( '-a22 12 octagonal_triangular' ),
[ 'octagonal', 'triangular' ] ],

    'octahedral' : [
'figurate_numbers', 'calculates the nth octahedral number',
'''
''',
'''
''' + makeCommandExample( '1 15 range octahedral' ) + '''
''' + makeCommandExample( '4881 octahedral' ),
[ 'tetrahedral', 'dodecahedral' ] ],

    'pentagonal' : [
'figurate_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''' + makeCommandExample( '1 16 range pentagonal' ) + '''
''' + makeCommandExample( '174985 pentagonal' ),
[ 'centered_pentagonal', 'polygonal' ] ],

    'pentagonal_square' : [
'figurate_numbers', 'calculates the nth pentagonal square number',
'''
''',
'''
''' + makeCommandExample( '-a20 1 5 range pentagonal_square' ) + '''
''' + makeCommandExample( '-a40 11 pentagonal_square' ),
[ 'pentagonal', 'square' ] ],

    'pentagonal_triangular' : [
'figurate_numbers', 'calculates the nth pentagonal triangular number',
'''
''',
'''
''' + makeCommandExample( '-a20 1 6 range pentagonal_triangular' ) + '''
''' + makeCommandExample( '-a25 11 pentagonal_triangular' ),
[ 'pentagonal', 'triangular' ] ],

    'pentatope' : [
'figurate_numbers', 'calculates the nth pentatope number',
'''
''',
'''
''' + makeCommandExample( '1 15 range pentatope' ) + '''
''' + makeCommandExample( '1238 pentatope' ),
[ 'polytope', 'polygonal' ] ],

    'polygonal' : [
'figurate_numbers', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' + makeCommandExample( '13 triangular' ) + '''
''' + makeCommandExample( '13 3 polygonal' ) + '''
''' + makeCommandExample( '1 10 range 5 polygonal' ) + '''
''' + makeCommandExample( '-a25 387 8925662618878671 polygonal' ),
[ 'polygonal_pyramidal', 'nth_polygonal' ] ],

    'polygonal_pyramidal' : [
'figurate_numbers', 'calculates the nth pyramidal number with k sides',
'''
''',
'''
''' + makeCommandExample( '23 pyramidal' ) + '''
''' + makeCommandExample( '23 4 polygonal_pyramidal' ) + '''
''' + makeCommandExample( '-a25 387 129 polygonal_pyramidal' ),
[ 'polygonal', 'pyramidal' ] ],

    'polytope' : [
'figurate_numbers', 'calculates nth polytope number of dimension k',
'''
''',
'''
''' + makeCommandExample( '1 10 range triangular' ) + '''
''' + makeCommandExample( '1 10 range 2 polytope' ) + '''
''' + makeCommandExample( '1 10 range tetrahedral' ) + '''
''' + makeCommandExample( '1 10 range 3 polytope' ) + '''
''' + makeCommandExample( '-a25 387 129 polytope' ),
[ 'polygonal', 'pentatope' ] ],

    'pyramidal' : [
'figurate_numbers', 'calculates the nth square pyramidal number',
'''
This is the equivalent of 'n 4 polygonal_pyramidal'.
''',
'''
''' + makeCommandExample( '1 10 range pyramidal' ) + '''
''' + makeCommandExample( '-a15 56714 pyramidal' ),
[ 'polygonal_pyramidal', 'square' ] ],

    'rhombic_dodecahedral' : [
'figurate_numbers', 'calculates the nth rhombic dodecahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range rhombic_dodecahedral' ) + '''
''' + makeCommandExample( '715 rhombic_dodecahedral' ),
[ 'dodecahedral', 'centered_dodecahedral' ] ],

    'square_triangular' : [
'figurate_numbers', 'calculates the nth square triangular number',
'''
'square_triangular' calculates the nth number that is both square and
triangular.
''',
'''
''' + makeCommandExample( '1 8 range square_triangular' ) + '''
''' + makeCommandExample( '-a25 16 square_triangular' ),
[ 'square', 'triangular' ] ],

    'star' : [
'figurate_numbers', 'calculates the nth star number',
'''
Star numbers are the same as centered dodecagonal numbers, so this is
equivalent to 'n 12 centered_polygonal'.
''',
'''
''' + makeCommandExample( '1 8 range star' ) + '''
''' + makeCommandExample( '8542 star' ),
[ 'polygonal', 'pyramidal' ] ],

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
''' + makeCommandExample( '1 8 range stella_octangula' ) + '''
''' + makeCommandExample( '6542 stella_octangula' ),
[ 'octahedral', 'truncated_octahedral' ] ],

    'tetrahedral' : [
'figurate_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range tetrahedral' ) + '''
''' + makeCommandExample( '413 tetrahedral' ),
[ 'octahedral', 'dodecahedral', 'icosahedral' ] ],

    'triangular' : [
'figurate_numbers', 'calculates the nth triangular number',
'''
Triangular numbers are the figurate numbers created by arranging items in the
shape of a triangle.   The first few triangular numbers can be easily
illustrated as such:

    *           *           *               *
              *   *       *   *           *   *
                        *   *   *       *   *   *
                                      *   *   *   *

The triangular numbers show up in many combinatorial problems, including
Pascal's triangle.
''',
'''
''' + makeCommandExample( '1 10 range triangular' ) + '''
''' + makeCommandExample( '3741 triangular' ),
[ 'nth_triangular', 'centered_triangular', 'polygonal' ] ],

    'truncated_octahedral' : [
'figurate_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range truncated_octahedral' ),
[ 'octahedral', 'stella_octangula' ] ],

    'truncated_tetrahedral' : [
'figurate_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' + makeCommandExample( '1 8 range truncated_tetrahedral' ) + '''
''' + makeCommandExample( '125 truncated_tetrahedral' ),
[  'tetrahedral', 'truncated_octahedral' ] ],

    #   'nth_tetrahedral' : [ findTetrahedralNumber, 1, [ ] ],


    #******************************************************************************
    #
    #  powers and roots operators
    #
    #******************************************************************************

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
[ 'cube', 'square_root', 'root', 'cube_super_root' ] ],

    'cube_super_root' : [
'powers_and_roots', 'calculates the cube super-root of n',
'''
The operator return x such that (x^x)^x = n.
''',
'''
''' + makeCommandExample( '8 cube_super_root' ) + '''
''' + makeCommandExample( '4294967296 cube_super_root' ) + '''
''' + makeCommandExample( '-73 cube_super_root' ) + '''
''' + makeCommandExample( '4 -2j + cube_super_root' ),
[ 'square', 'cube_root', 'root', 'square_root', 'square_super_root' ] ],

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
''' + makeCommandExample( 'i exp' ),
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
''' + makeCommandExample( 'i exp10' ),
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

    'hyperoperator' : [
'powers_and_roots', 'calculates the ath hyperoperator with operands b and c',
'''
''',
'''
''',
[ 'tetrate_right', 'tetrate', 'power', 'hyperoperator_right' ] ],

    'hyperoperator_right' : [
'powers_and_roots', 'calculates the ath right-associative hyperoperator with operands b and c',
'''
''',
'''
''',
[ 'tetrate_right', 'tetrate', 'power' ] ],

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
[ 'power', 'square_root', 'cube_root', 'square_super_root' ] ],

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
[ 'square', 'cube_root', 'root', 'square_super_root' ] ],

    'square_super_root' : [
'powers_and_roots', 'calculates the square super-root of n',
'''
The operator return x such that x^x = n.
''',
'''
''' + makeCommandExample( '4 square_super_root' ) + '''
''' + makeCommandExample( '16777216 square_super_root' ) + '''
''' + makeCommandExample( '-10 square_super_root' ) + '''
''' + makeCommandExample( 'i square_super_root' ),
[ 'square', 'cube_root', 'root', 'square_root', 'cube_super_root' ] ],

    'super_root' : [
'powers_and_roots', 'calculates the principal, real, kth super-root of n',
'''
The square super-root of n is x, where x^x = n.  The cube super-root of n is
x where x^x^x = n.  These correspond to 'n 2 super_root' and 'n 3 super_root'
respectively.  Higher numbers work similarly.

There are k - 1 super-roots of n, and this operator returns the real,
principle kth super-root of n.
''',
'''
''' + makeCommandExample( '256 2 super_root' ) + '''
''' + makeCommandExample( '8 3 super_root' ) + '''
''' + makeCommandExample( '340282366920938463463374607431768211456 4 super_root' ) + '''
''' + makeCommandExample( '-73 6 super_root' ) + '''
''' + makeCommandExample( '12 6j + 15 super_root' ),
[ 'root', 'square_root', 'square_super_root', 'super_roots' ] ],

    'super_roots' : [
'powers_and_roots', 'calculates all of the kth super-roots of n',
'''
The square super-root of n is x, where x^x = n.  The cube super-root of n is
x where x^x^x = n.  These correspond to 'n 2 super_root' and 'n 3 super_root'
respectively.  Higher numbers work similarly.

There are k - 1 super-roots of n, and this operator returns all of them.
''',
'''
''' + makeCommandExample( '256 2 super_roots' ) + '''
''' + makeCommandExample( '8 3 super_roots' ) + '''
''' + makeCommandExample( '340282366920938463463374607431768211456 4 super_roots' ) + '''
''' + makeCommandExample( '-128 5 super_roots' ) + '''
''' + makeCommandExample( '27 4j + 3 super_roots' ),
[ 'square', 'cube_root', 'root', 'square_root', 'super_root' ] ],

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
[ 'power', 'tetrate_right', 'hyperoperator' ] ],

    'tetrate_right' : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''',
[ 'tetrate', 'power', 'hyperoperator_right' ] ],


    #******************************************************************************
    #
    #  prime number operators
    #
    #******************************************************************************

    'balanced_prime' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''
A balanced prime is a prime which is the average of its immediate pair
of prime neighbors.

This operator returns the nth balanced prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range balanced_prime' ) + '''
''' + makeCommandExample( '100 balanced_prime' ),
[ 'balanced_primes', 'double_balanced_prime', 'triple_balanced_prime', 'quadruple_balanced_prime' ] ],

    'balanced_primes' : [
'prime_numbers', 'calculates the nth set of balanced primes',
'''
A balanced prime is a prime which is the average of its immediate pair of prime
neighbors.

This operator prints the 3 prime numbers that make up the nth balanced prime and
its pair of prime neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range balanced_primes -s1' ) + '''
''' + makeCommandExample( '10 balanced_primes diffs' ),
[ 'balanced_prime', 'double_balanced_primes', 'triple_balanced_primes', 'quadruple_balanced_primes' ] ],

    'cousin_prime' : [
'prime_numbers', 'returns the nth cousin prime',
'''
Cousin primes are primes that are separated by 4.  The first of a pair of
cousin primes must end with the digit 3, 7, or 9, because if a prime ends with
a 1, then a number 4 great cannot be a prime, since it ends with 5.

This operator returns the first member of the nth set of cousin primes.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 5 range cousin_prime' ) + '''
''' + makeCommandExample( '10000 cousin_prime' ),
[ 'cousin_primes', 'sexy_prime', 'octy_prime' ] ],

    'cousin_primes' : [
'prime_numbers', 'returns the nth set of cousin primes',
'''
Cousin primes are primes that are separated by 4.  The first of a pair of
cousin primes must end with the digit 3, 7, or 9, because if a prime ends with
a 1, then a number 4 great cannot be a prime, since it ends with 5.

This operator returns the boith members of the nth set of cousin primes.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 5 range cousin_primes -s1' ) + '''
''' + makeCommandExample( '1000 cousin_primes' ),
[ 'cousin_prime', 'sexy_primes', 'octy_primes' ] ],

    'double_balanced_prime' : [
'prime_numbers', 'returns the nth double balanced prime',
'''
A double balanced prime is a prime which is the average of its immediate pair
of prime neighbors, and its second pair of prime neighbors.

This operator returns the nth double balanced prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '5 double_balanced_prime' ) + '''
''' + makeCommandExample( '1 10 range double_balanced_prime' ),
[ 'balanced_prime', 'double_balanced_primes', 'triple_balanced_prime', 'quadruple_balanced_prime' ] ],

    'double_balanced_primes' : [
'prime_numbers', 'returns the nth double balanced prime and its neighbors',
'''
A double balanced prime is a prime which is the average of its immediate pair
of prime neighbors, and its second pair of prime neighbors.

This operator returns the nth double balanced prime.

This operator prints the 5 prime numbers that make up the nth double balanced
prime and its two nested pairs of prime neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '10 double_balanced_primes' ) + '''
''' + makeCommandExample( '10 double_balanced_primes diffs' ),
[ 'balanced_primes', 'double_balanced_prime', 'triple_balanced_primes', 'quadruple_balanced_primes' ] ],

    'isolated_prime' : [
'prime_numbers', 'returns the nth isolated prime',
'''
A prime is considered isolated if it is separated from its two prime neighbors
by more than 2.  An alternate definition is that an isolated prime is a prime
that is not part of a twin prime pair.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range isolated_prime' ) + '''
''' + makeCommandExample( '500 isolated_prime' ),
[ 'balanced_prime' ] ],

    'next_prime' : [
'prime_numbers', 'returns the smallest prime number greater than n',
'''
This operator returns the smallest prime number greater than n.

This function does not require the use of the prime data files, so arbitrarily
large values can be used.  Thanks to gmpy2, rpn can calculate the next prime
for numbers of a thousand digits or more in relatively quickly.
''',
'''
''' + makeCommandExample( '10 next_prime' ) + '''
Generate a random 200-digit prime:

''' + makeCommandExample( '-a201 10 200 ** random_int next_prime' ),
[ 'prime', 'primes', 'next_primes', 'previous_prime', 'previous_primes' ] ],

    'next_primes' : [
'prime_numbers', 'returns the next k smallest prime numbers greater than n',
'''
This operator returns the next k prime numbers greater n.
''',
'''
''' + makeCommandExample( '100 10 next_primes' ) + '''
''' + makeCommandExample( '-a71 10 70 ** random_int 5 next_primes -s1' ),
[ 'prime', 'primes', 'next_prime', 'previous_primes' ] ],

    'next_quadruplet_prime' : [
'prime_numbers', 'returns the first member of the smallest set of quadruplet primes above n',
'''
This operator returns the first member of the smallest set of quadruplet
primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '1,000 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '100,000 next_quadruplet_prime' ),
[ 'quadruplet_prime', 'nth_quadruplet_prime', 'quadruplet_primes', 'next_quadruplet_primes' ] ],

    'next_quadruplet_primes' : [
'prime_numbers', 'returns the smallest set of quadruplet primes above n',
'''
This operator returns the smallest set of quadruplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '1,000 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '100,000 next_quadruplet_primes' ),
[ 'quadruplet_prime', 'nth_quadruplet_prime', 'quadruplet_primes', 'next_quadruplet_prime' ] ],

    'next_quintuplet_prime' : [
'prime_numbers', 'returns the first member of the smallest set of quintuplet primes above n',
'''
This operator returns the first member of the smallest set of quintuplet
primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_quintuplet_prime' ),
[ 'quintuplet_primes', 'quintuplet_prime', 'nth_quintuplet_prime', 'next_quintuplet_primes' ] ],

    'next_quintuplet_primes' : [
'prime_numbers', 'returns the the smallest set of quintuplet primes above n',
'''
This operator returns the smallest set of quintuplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_quintuplet_primes' ),
[ 'quintuplet_primes', 'quintuplet_prime', 'nth_quintuplet_prime', 'next_quintuplet_primes' ] ],

    'next_sextuplet_prime' : [
'prime_numbers', 'returns the first member of the smallest set of sextuplet primes above n',
'''
This operator returns the first member of the smallest set of sextuplet
primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_sextuplet_prime' ),
[ 'sextuplet_primes', 'sextuplet_prime', 'nth_sextuplet_prime', 'next_sextuplet_primes' ] ],

    'next_sextuplet_primes' : [
'prime_numbers', 'returns the the smallest set of sextuplet primes above n',
'''
This operator returns the smallest set of sextuplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_sextuplet_primes' ),
[ 'sextuplet_primes', 'sextuplet_prime', 'nth_sextuplet_prime', 'next_sextuplet_primes' ] ],

    'next_triplet_prime' : [
'prime_numbers', 'returns the next first member of the smallest set of triplet primes above n',
'''
This operator returns the first member of the smallest set of triplet primes
greater than n.
''',
'''
''' + makeCommandExample( '100 next_triplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_triplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_triplet_prime' ) + '''
''' + makeCommandExample( '1,000,000,000 next_triplet_prime' ),
[ 'triplet_prime', 'nth_triplet_prime', 'triplet_primes' ] ],

    'next_triplet_primes' : [
'prime_numbers', 'returns the smallest set of triplet primes above n',
'''
This operator returns smallest set of triplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_triplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_triplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_triplet_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_triplet_primes' ),
[ 'triplet_prime', 'nth_triplet_prime', 'triplet_primes' ] ],

    'next_twin_prime' : [
'prime_numbers', 'returns the first member of the smallest set of twin primes above n',
'''
This operator returns the first member of the smallest set of twin primes
greater than n.
''',
'''
''' + makeCommandExample( '100 next_twin_prime' ) + '''
''' + makeCommandExample( '10,000 next_twin_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_twin_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_twin_prime' ),
[ 'twin_prime', 'nth_twin_prime', 'twin_primes' ] ],

    'next_twin_primes' : [
'prime_numbers', 'returns the smallest set of twin primes above n',
'''
This operator returns the smallest set of twin primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_twin_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_twin_primes' ) + '''
''' + makeCommandExample( '10,000,000 next_twin_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_twin_primes' ),
[ 'twin_prime', 'nth_twin_prime', 'twin_primes' ] ],

    'nth_prime' : [
'prime_numbers', 'finds the index of the closest prime less than or equal n',
'''
This operator returns the index of the prime number that is closest to, but not
larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100 nth_prime' ) + '''
''' + makeCommandExample( '25 prime' ) + '''
''' + makeCommandExample( '1000 nth_prime' ) + '''
''' + makeCommandExample( '168 prime' ),
[ 'prime', 'primes' ] ],

    'nth_quadruplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set greater than n',
'''
A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.

This operator returns the index of the prime quadruplet whose first member is
closest to, but not larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100 nth_quadruplet_prime' ) + '''
''' + makeCommandExample( '3 quadruplet_primes' ) + '''
''' + makeCommandExample( '10000 nth_quadruplet_prime' ) + '''
''' + makeCommandExample( '13 quadruplet_primes' ),
[ 'quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'nth_quintuplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest quintuplet prime set greater than n',
'''
If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equiivalent.

This operator returns the index of the prime quintuplet whose first member is
closest to, but not larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100 nth_quintuplet_prime' ) + '''
''' + makeCommandExample( '5 quintuplet_primes' ) + '''
''' + makeCommandExample( '10000 nth_quintuplet_prime' ) + '''
''' + makeCommandExample( '11 quintuplet_primes' ) + '''
''' + makeCommandExample( '85500 nth_quintuplet_prime' ) + '''
''' + makeCommandExample( '60 quintuplet_primes' ),
[ 'quintuplet_primes', 'quintuplet_prime', 'next_quintuplet_prime' ] ],

    'nth_sextuplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest sextuplet prime set greater than n',
'''
A prime sextuplet is a set of six primes of the form p, p+4, p+6, p+10, p+12
and p+14.  This is the closest possible grouping of six primes.

This operator returns the index of the prime sextuplet whose first member is
closest to, but not larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100,000 nth_quadruplet_prime' ) + '''
''' + makeCommandExample( '7 quadruplet_primes' ) + '''
''' + makeCommandExample( '100,000,000,000 nth_quadruplet_prime' ) + '''
''' + makeCommandExample( '8627 quadruplet_primes' ),
[ 'sextuplet_prime', 'next_sextuplet_prime', 'sextuplet_primes' ] ],

    'nth_triplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest triplet prime set greater than n',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.

This operator returns the index of the smallest triplet prime set whose first
member is larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100 nth_triplet_prime' ) + '''
''' + makeCommandExample( '10 triplet_primes' ) + '''
''' + makeCommandExample( '10000 nth_triplet_prime' ) + '''
''' + makeCommandExample( '113 triplet_primes' ),
[ 'quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'nth_twin_prime' : [
'prime_numbers', 'finds the index of the first of the closest twin prime pair greater than n',
'''
Twin primes are prime numbers separated by 2.  The first twin prime pair
consists of 3 and 5.  It is conjectured that there infinitely many twin primes.

This operator returns the index of the smallest twin prime pair whose first
member is larger than n.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '100 nth_twin_prime' ) + '''
''' + makeCommandExample( '9 twin_primes' ) + '''
''' + makeCommandExample( '10000 nth_twin_prime' ) + '''
''' + makeCommandExample( '206 twin_primes' ),
[ 'quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'octy_prime' : [
'prime_numbers', 'returns the first of the nth set of octy primes',
'''
Octy primes are defined to be a pair of numbers, n and n + 8, which are both
prime.  n + 2, n + 4 or n + 6 may also be prime.  This operator returns the
smaller of nth set of octy primes, so the value of the result + 8 will also be
prime.

Even though there are sexy triplets and sexy quadruplets, octy triplets and
octy quadruplets do not exist.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range octy_prime' ) + '''
''' + makeCommandExample( '5473 octy_prime' ) + '''
''' + makeCommandExample( '1000 1012 range octy_prime' ),
[ 'octy_primes', 'cousin_prime', 'sexy_prime' ] ],

    'octy_primes' : [
'prime_numbers', 'returns the nth set of octy primes',
'''
Octy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns both members
of the nth set of octy primes, which will differ by 6.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range octy_primes' ) + '''
''' + makeCommandExample( '2384 octy_primes' ) + '''
''' + makeCommandExample( '1001 1010 range octy_primes' ),
[ 'octy_prime', 'cousin_primes', 'sexy_primes' ] ],

    'polyprime' : [
'prime_numbers', 'returns the the kth superprime of the nth prime',
'''
This operator returns a prime number computed by taking the nth prime number
(and returning that if k is 1) and then using that as the new index for a prime
number, k - 1 more times.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 1 polyprime' ) + '''
''' + makeCommandExample( '1 2 polyprime' ) + '''
''' + makeCommandExample( '1 3 polyprime' ) + '''
''' + makeCommandExample( '1 1 10 range polyprime' ) + '''
''' + makeCommandExample( '3 6 polyprime' ) + '''
''' + makeCommandExample( '5 5 polyprime' ) + '''
''' + makeCommandExample( '4 12 polyprime -c' ),
[ 'super_prime', 'prime' ] ],

    'previous_prime' : [
'prime_numbers', 'returns the previous prime number less than n',
'''
This operator returns the largest prime less than n.

This function does not require the use of the prime data files, so arbitrarily
large values can be used.  Thanks to gmpy2, rpn can calculate the previous
prime for numbers of a thousand digits or more relatively quickly.
''',
'''
''' + makeCommandExample( '10 previous_prime' ) + '''
''' + makeCommandExample( '100 previous_prime' ),
[ 'prime', 'primes', 'next_primes', 'next_prime', 'previous_primes' ] ],

    'previous_primes' : [
'prime_numbers', 'returns the previous k prime numbers less than n',
'''
This operator returns the k largest primes less than n.

This function does not require the use of the prime data files, so arbitrarily
large values can be used.  Thanks to gmpy2, rpn can calculate the previous
prime for numbers of a thousand digits or more relatively quickly.
''',
'''
''' + makeCommandExample( '100 10 previous_primes' ) + '''
''' + makeCommandExample( '-a71 10 70 ** random_int 5 previous_primes -s1' ),
[ 'prime', 'primes', 'next_prime', 'next_primes', 'previous_prime' ] ],

    'prime' : [
'prime_numbers', 'returns the nth prime',
'''
Calculates the nth prime number.  For calculating ranges of primes, the
'primes' operator is much faster.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1,000,000 prime' ) + '''
''' + makeCommandExample( '1,000,000,000 prime' ),
[ 'primes', 'prime_range', 'next_prime', 'previous_prime' ] ],

    'primes' : [
'prime_numbers', 'generates a list of k primes starting from index n',
'''
This operator generates is list of k primes starting the nth prime.  This is
much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 20 primes' ) + '''
''' + makeCommandExample( '3206 10 primes' ) + '''
''' + makeCommandExample( '1,000,000 10 primes' ),
[ 'prime', 'prime_range' ] ],

    'prime_pi' : [
'prime_numbers', 'calculates the count of prime numbers up to and including n',
'''
This will return an exact answer for relatively small values (based on the
prime number data), and a range for larger values, which are estimated.
''',
'''
''' + makeCommandExample( '541 prime_pi' ) + '''
''' + makeCommandExample( '100 prime' ) + '''
''' + makeCommandExample( '10 10 ** prime_pi' ) + '''
''' + makeCommandExample( '10 100 ** prime_pi' ),
[ 'prime', 'primes', 'nth_prime' ] ],

    'prime_range' : [
'prime_numbers', 'generates a range of primes starting from index n to index k',
'''
This operator is much faster than using 'range' with 'prime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 21 prime_range' ) + '''
''' + makeCommandExample( '934 960 prime_range' ) + '''
''' + makeCommandExample( '999,990 1,000,000 prime_range' ),
[ 'prime', 'primes', 'next_prime', 'previous_prime' ] ],

    'quadruple_balanced_prime' : [
'prime_numbers', 'returns the nth quadruple balanced prime',
'''
A quadruple balanced prime is a prime which is the average of its immediate
pair of prime neighbors, and its second, third and fourth pairs of prime
neighbors.

This operator returns the nth quadruple balanced prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quadruple_balanced_prime' ) + '''
''' + makeCommandExample( '2 quadruple_balanced_prime' ),
[ 'balanced_prime', 'double_balanced_prime', 'triple_balanced_prime', 'quadruple_balanced_primes' ] ],

    'quadruple_balanced_primes' : [
'prime_numbers', 'returns the nth quadruple balanced prime and its neighbors',
'''
A quadruple balanced prime is a prime which is the average of its immediate
pair of prime neighbors, and its second, third and fourth pairs of prime
neighbors.

This operator prints the 9 prime numbers that make up the nth quadruple
balanced prime and its four nested pairs of prime neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '3 quadruple_balanced_primes' ) + '''
''' + makeCommandExample( '3 quadruple_balanced_primes diffs' ),
[ 'balanced_primes', 'double_balanced_primes', 'triple_balanced_primes', 'quadruple_balanced_prime' ] ],

    'quadruplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''
A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.

This operator returns the first member of the nth prime quadruplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quadruplet_prime' ),
[ 'nth_quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'quadruplet_primes' : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''
A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.

This operator returns a list containing the four members of the nth prime
quadruplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quadruplet_primes -s1' ),
[ 'nth_quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'quintuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''
If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equiivalent.  This operator returns the
a first of the 5 primes that make up the nth prime quintuplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quintuplet_prime' ),
[ 'quintuplet_primes', 'next_quintuplet_prime', 'nth_quintuplet_prime' ] ],

    'quintuplet_primes' : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''
If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet.  rpn considers the two kinds of
quintuplets (ones with p-4 and ones with p+12) as equivalent.

This operator returns the a list of the five primes that make up the nth prime
quintuplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quintuplet_primes -s1' ),
[ 'quintuplet_prime', 'nth_quintuplet_prime', 'next_quintuplet_prime' ] ],

    'safe_prime' : [
'prime_numbers', 'returns the nth safe prime',
'''
A safe prime is a prime number p such that ( p - 1 ) / 2 is also prime.  The
number ( p - 1 ) / 2 is a Sophie Germain prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range safe_prime' ) + '''
''' + makeCommandExample( '48365 safe_prime' ) + '''
''' + makeCommandExample( '1 10 range safe_prime 1 - 2 /' ) + '''
''' + makeCommandExample( '1 10 range sophie_prime' ),
[ 'sophie_prime' ] ],

    'sextuplet_prime' : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''
If p, p+2, p+6, p+8 is a prime quadruplet and p-4 and p+12 are both also prime,
then the six primes are a prime sextuplet.

This operator returns the first of the six primes that make up the nth prime
sextuplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sextuplet_prime' ) + '''
''' + makeCommandExample( '2939 sextuplet_prime' ),
[ 'sextuplet_primes' ] ],

    'sextuplet_primes' : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''
If p, p+2, p+6, p+8 is a prime quadruplet and p-4 and p+12 are both also prime,
then the six primes are a prime sextuplet.

This operator returns the a list of the six primes that make up the nth prime
sextuplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sextuplet_primes -s1' ) + '''
''' + makeCommandExample( '387 sextuplet_prime' ),
[ 'sextuplet_prime' ] ],

    'sexy_prime' : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns the smaller of
nth set of sexy primes, so the value of the result + 6 will also be prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_prime' ) + '''
''' + makeCommandExample( '16387 sexy_prime' ) + '''
''' + makeCommandExample( '10000 10010 range sexy_prime' ),
[ 'sexy_primes', 'sexy_triplet', 'sexy_quadruplet' ] ],

    'sexy_primes' : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  This operator returns both members
of the nth set of sexy primes, which will differ by 6.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_primes' ) + '''
''' + makeCommandExample( '819 sexy_primes' ) + '''
''' + makeCommandExample( '1001 1010 range sexy_primes' ),
[ 'sexy_prime', 'sexy_triplets', 'sexy_quadruplets' ] ],

    'sexy_triplet' : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 is also prime, then this
forms a "sexy triplet".

This operator returns the first of the three primes that form the nth sexy
triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_triplet' ) + '''
''' + makeCommandExample( '294785 sexy_triplet' ),
[ 'sexy_prime', 'sexy_triplets', 'sexy_quadruplet' ] ],

    'sexy_triplets' : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 is also prime, then this
forms a "sexy triplet".

This operator returns a list of the three primes that form the nth sexy
triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_triplets -s1' ) + '''
''' + makeCommandExample( '283751 sexy_triplets' ) + '''
''' + makeCommandExample( '8845 sexy_triplets is_prime and_all' ),
[ 'sexy_prime', 'sexy_triplet', 'sexy_quadruplets' ] ],

    'sexy_quadruplet' : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 and n + 18 are also both
prime, then this forms a "sexy quadruplet".

This operator returns the first of the four primes that form the nth sexy
quadruplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_quadruplet' ) + '''
''' + makeCommandExample( '751 sexy_quadruplet' ),
[ 'sexy_quadruplets', 'sexy_prime', 'sexy_triplet' ] ],

    'sexy_quadruplets' : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''
Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 and n + 18 are also both
prime, then this forms a "sexy quadruplet".

This operator returns a list of the four primes that form the nth sexy
quadruplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sexy_quadruplets -s1' ) + '''
''' + makeCommandExample( '2337 sexy_quadruplets' ) + '''
''' + makeCommandExample( '6465 sexy_quadruplets is_prime and_all' ),
[ 'sexy_quadruplet', 'sexy_primes', 'sexy_triplets' ] ],

    'sophie_prime' : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''
A Sophie Germain prime is a prime number p such that 2p + 1 is also prime.  The
number 2p + 1 is a safe prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range sophie_prime' ) + '''
''' + makeCommandExample( '34875 sophie_prime' ) + '''
''' + makeCommandExample( '1 10 range sophie_prime 2 * 1 +' ) + '''
''' + makeCommandExample( '1 10 range safe_prime' ),
[ 'safe_prime' ] ],

    'super_prime' : [
'prime_numbers', 'returns the nth super prime (the nth primeth prime)',
'''
This operator returns the mth prime where m is the nth prime.

This is equivalent to 'n 2 polyprime'.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range super_prime' ) + '''
''' + makeCommandExample( '34 super_prime' ) + '''
''' + makeCommandExample( '34 prime prime' ),
[ 'prime', 'polyprime' ] ],

    'triple_balanced_prime' : [
'prime_numbers', 'returns the nth triple balanced prime',
'''
A triple balanced prime is a prime which is the average of its immediate pair
of prime neighbors, its second pair of prime neighbors and its third pair of
prime neighbors.

This operator returns the nth triple balanced prime.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range triple_balanced_prime' ) + '''
''' + makeCommandExample( '2 triple_balanced_prime' ),
[ 'balanced_prime', 'double_balanced_prime', 'triple_balanced_primes', 'quadruple_balanced_prime' ] ],

    'triple_balanced_primes' : [
'prime_numbers', 'returns the nth triple balanced prime and its neighbors',
'''
A triple balanced prime is a prime which is the average of its immediate pair
of prime neighbors, its second pair of prime neighbors and its third pair of
prime neighbors.

This operator prints the 7 prime numbers that make up the nth triple balanced
prime and its three nested pairs of prime neighbors.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '3 triple_balanced_primes' ) + '''
''' + makeCommandExample( '3 triple_balanced_primes diffs' ),
[ 'balanced_primes', 'double_balanced_primes', 'triple_balanced_prime', 'quadruple_balanced_primes' ] ],

    'triplet_prime' : [
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.

This operator returns the first of the three primes in the nth prime triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1231 triplet_prime' ) + '''
''' + makeCommandExample( '1 10 range triplet_prime' ),
[ 'twin_prime', 'triplet_primes', 'quadruplet_prime', 'quintuplet_prime' ] ],

    'triplet_primes' : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.

This operator returns a list of the three primes in the nth prime triplet.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1231 triplet_primes' ) + '''
''' + makeCommandExample( '1 10 range triplet_primes -s1' ),
[ 'twin_primes', 'triplet_prime', 'quadruplet_primes', 'quintuplet_primes' ] ],

    'twin_prime' : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''
Twin primes are prime numbers separated by 2.  The first twin prime pair
consists of 3 and 5.  It is conjectured that there infinitely many twin primes.

This operator returns the first of the two primes that make up the nth twin
prime pair.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range twin_prime' ) + '''
''' + makeCommandExample( '85749 twin_prime' ),
[ 'twin_primes', 'triplet_prime', 'quadruplet_prime', 'quintuplet_prime' ] ],

    'twin_primes' : [
'prime_numbers', 'returns the nth set of twin primes',
'''
Twin primes are prime numbers separated by 2.  The first twin prime pair
consists of 3 and 5.  It is conjectured that there infinitely many twin primes.

This operator returns a list of the two priems that make up the nth twin
prime pair.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range twin_primes' ) + '''
''' + makeCommandExample( '157 twin_primes' ) + '''
An _extremely_ crude estimation of Brun's twin prime constant:
''' + makeCommandExample( '1 100 range twin_primes 1/x sum sum', indent=4 ),
[ 'twin_prime', 'triplet_primes', 'quadruplet_primes', 'quintuplet_primes' ] ],


    #******************************************************************************
    #
    #  settings operators (for use in interactive mode)
    #
    #******************************************************************************

    'accuracy' : [
'settings', 'sets output accuracy to n',
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
[ 'precision' ] ],

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
[ 'comma_mode' ] ],

    'comma_mode' : [
'settings', 'set temporary comma mode in interactive mode',
'''
''',
'''
''',
[ 'comma' ] ],

    'decimal_grouping' : [
'settings', 'used in interactive mode to set the decimal grouping level',
'''
''',
'''
''',
[ 'integer_grouping' ] ],

    'hex_mode' : [
'settings', 'set temporary hex mode in interactive mode',
'''
''',
'''
''',
[ 'octal_mode', 'output_radix' ] ],

    'identify' : [
'settings', 'set identify mode in interactive mode',
'''
''',
'''
''',
[ 'identify_mode' ] ],

    'identify_mode' : [
'settings', 'set temporary identify mode in interactive mode',
'''
''',
'''
''',
[ 'identify' ] ],

    'input_radix' : [
'settings', 'used in interactive mode to set the input radix',
'''
''',
'''
rpn (1)> 12 output_radix
10
rpn (2)> 1 15 range
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, 10, 11, 12, 13 ]
rpn (3)> 12 input_radix
10
rpn (4)> 1 15 range
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, 10, 11, 12, 13, 14, 15 ]
rpn (5)>
''',
[ 'output_radix' ] ],

    'integer_grouping' : [
'settings', 'used in interactive mode to set the integer grouping',
'''
''',
'''
''',
[ 'integer_grouping' ] ],

    'leading_zero' : [
'settings', 'when set to true and integer grouping is being used, output will include leading zeroes',
'''
''',
'''
''',
[ 'leading_zero_mode' ] ],

    'leading_zero_mode' : [
'settings', 'used in the interactive mode to set the leading zero mode for output',
'''
''',
'''
''',
[ 'leading_zero' ] ],

    'octal_mode' : [
'settings', 'set temporary octal mode in interactive mode',
'''
''',
'''
''',
[ 'hex_mode', 'output_radix' ] ],

    'output_radix' : [
'settings', 'used in the interactive mode to set the output radix',
'''
''',
'''
rpn (1)> 12 output_radix
10
rpn (2)> 1 15 range
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, 10, 11, 12, 13 ]
rpn (3)> 12 input_radix
10
rpn (4)> 1 15 range
[ 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, 10, 11, 12, 13, 14, 15 ]
rpn (5)>
''',
[ 'hex_mode', 'octal_mode', 'input_radix' ] ],

    'precision' : [
'settings', 'used in the interactive mode to set the output precision',
'''
''',
'''
''',
[ 'accuracy' ] ],

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


    #******************************************************************************
    #
    #  special operators
    #
    #******************************************************************************

    'base_units' : [
'special', 'returns a measurement converted to base units',
'''
Currently, this is only for informational purposes.  This operator also
currently does the same thing as 'primitive_units'.   I have plans for it,
though.
''',
'''
''' + makeCommandExample( '50 watts base_units' ) + '''
''' + makeCommandExample( '120 millivolts base_units' ) + '''
''' + makeCommandExample( '300 kilonewtons base_units' ),
[ 'dimensions', 'primitive_units' ] ],

    'constant' : [
'special', 'creates a user-defined constant',
'''
This operator is not implemented yet!
''',
'''
''',
[ 'set_variable' ] ],

    'delete_config' : [
'special', 'delete configuration setting n',
'''
This operator deletes the entry for n in the configuration file.
''',
'''
''',
[ 'dump_config', 'get_config', 'set_config' ] ],

    'dimensions' : [
'special', 'returns the unit dimensions for a measurement',
'''
This operator returns the unit dimensions for a measurement.

Currently, this is only for informational purposes.  There's nothing in
rpn that can use this output.
''',
'''
''' + makeCommandExample( '60 mph dimensions' ) + '''
''' + makeCommandExample( 'newton dimensions' ) + '''
''' + makeCommandExample( 'volt dimensions' ) + '''
''' + makeCommandExample( 'coulomb dimensions' ),
[ 'base_units', 'primitive_units' ] ],

    'dump_config' : [
'special', 'dumps all configuration settings',
'''
Tis operator dumps the user-defined configuration settings.
''',
'''
c:\\>rpn dump_config
yafu_binary: "yafu-x64-mingw-r388-sse41.exe"
yafu_path: "c:\\app\\yafu"

3
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
c:\\>rpn 55 describe

55 is:
    odd
    composite
    the 10th triangular number
    the 5th heptagonal number
    the 4th centered nonagonal number
    the 10th Fibonacci number
    deficient
    11-smooth
    5-rough
    semiprime
    pernicious
    unusual
    a base-2 Smith number
    a base-4 Smith number
    a Kaprekar number

55 has:
    2 digits
    a digit sum of 10
    a digit product of 25
    2 prime factors: 5, 11
    4 divisors
    a sum of divisors of 72
    a Stern value of 11
    a Calkin-Wilf value of 11/3
    a Mobius value of 1
    a radical of 55
    a Euler phi value of 40
    a digital root of 1
    a multiplicative persistence of 3
    an Erdos persistence of 3

55
''',
[ 'identify' ] ],

    'echo' : [
'special', 'when the next operator is evaluated, appends the result to n',
'''
The echo operator does not apply to operators in an operator list, but is
applied when the operator list is completed.
''',
'''
''' + makeCommandExample( '2 echo 2 +' ) + '''
''' + makeCommandExample( '2 echo 2 echo +' ),
[ 'previous' ] ],

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
''' + makeCommandExample( 'yafu_binary get_config' ),
[ 'delete_config', 'dump_config', 'set_config' ] ],

    'get_variable' : [
'special', 'retrieves the value for n in the user config data file',
'''
Preceding the variable name with '$' allows accessing the variable without
having to use the cumbersome 'get_variable' operator.
''',
'''
''' + makeCommandExample( 'magic_number 37 set_variable' ) + '''
''' + makeCommandExample( 'magic_number get_variable' ) + '''
''' + makeCommandExample( '$magic_number' ),
[ 'set_variable' ] ],

    'help' : [
'special', 'displays help text',
'''
By itself, help will print general help text.  If an argument is added _after_
'help' then help on that particular topic will be printed.
''',
'''
c:\\>rpn help add
n k add - adds n to k

alias:  +
category: arithmetic

This operator adds two terms together.  If one of the operands is a list, then
the other operand is added to each member of the list and the result is a
list.

...
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
[ 'not', 'is_equal' ] ],

    'list_from_file' : [
'special', 'reads a list of values from a file',
'''
The file should have one number per line, and the values are subject to the
same processing as numerical values on the rpn command line.
''',
'''
''',
[ 'set_config', 'get_config', 'set_variable', 'get_variable' ] ],

    'name' : [
'special', 'returns the English name for the integer value or measurement n',
'''
This operator returns the English name for any integer n.

The upper limit of integers rpn can name is 10^3004 - 1.

If the number has more digits than the current precision setting of rpn, the
result will be subject to rounding and will be incorrect.

''' + makeCommandExample( '157 name' ) + '''
c:\\>rpn 10 3000 ** name
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
All data downloaded from OEIS is cached.  Existing OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is to use
the -I option, when downloading an entry.
''',
'''
''' + makeCommandExample( '10349 oeis' ),
[ 'oeis_comment', 'oeis_ex', 'oeis_name', 'oeis_offset' ] ],

    'oeis_comment' : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  Existing OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is to use
the -I option, when downloading an entry.
''',
'''
''' + makeCommandExample( '98593 oeis_comment' ),
[ 'oeis_name', 'oeis_ex', 'oeis' ] ],

    'oeis_ex' : [
'special', 'downloads the extra information field for the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  Existing OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is to use
the -I option, when downloading an entry.
''',
'''
''' + makeCommandExample( '178 oeis_ex' ),
[ 'oeis_comment', 'oeis_name', 'oeis' ] ],

    'oeis_name' : [
'special', 'downloads the name of the OEIS integer series n',
'''
All data downloaded from OEIS is cached.  Existing OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is to use
the -I option, when downloading an entry.
''',
'''
''' + makeCommandExample( '10349 oeis_name' ),
[ 'oeis_ex', 'oeis', 'oeis_comment' ] ],

    'oeis_offset' : [
'special', 'downloads the offset for an OEIS sequence',
'''
The offset is used to denote the decimal offset of OEIS sequences that are
representations of decimal numbers.

All data downloaded from OEIS is cached.  Existing OEIS data is probably seldom
updated, but if it is, the only way to get rpn to download new data is to use
the -I option, when downloading an entry.
''',
'''
''' + makeCommandExample( '63 oeis_offset' ),
[ 'oeis_name', 'oeis_ex', 'oeis' ] ],

    'ordinal_name' : [
'special', 'returns the English ordinal name for the integer value n',
'''
The ordinal names for numbers start with 'first', 'second', etc.

The upper limit of integers rpn can name is 10^3004 - 1.

If the number has more digits than the current precision setting of rpn, the
result will be subject to rounding and will be incorrect.

c:\\>rpn 10 3000 ** ordinal_name
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

    'primitive_units' : [
'special', 'returns a measurement converted to primitive units',
'''
Currently, this is only for informational purposes.  This operator also
currently does the same thing as 'base_units'.   I have plans to change
'base_units'.
''',
'''
''' + makeCommandExample( '50 watts primitive_units' ) + '''
''' + makeCommandExample( '120 millivolts primitive_units' ) + '''
''' + makeCommandExample( '300 kilonewtons primitive_units' ),
[ 'dimensions', 'base_units' ] ],

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
[ 'random', 'random_', 'random_integers' ] ],

    'random_integers' : [
'special', 'returns a list of k random integers from 0 to n - 1',
'''
This operator returns a series of k random integers in the range of 0 to
n - 1, inclusive.

rpn is automatically seeded every time it runs, so random number streams are
not reproducible.
''',
'''
''' + makeCommandExample( '10 10 random_integers' ) + '''
''' + makeCommandExample( '1000 5 random_integers' ) + '''
''' + makeCommandExample( '1 billion 4 random_integers' ) + '''
Test the birthday paradox:
''' + makeCommandExample( '365 23 random_integers sort', indent=4 ) + '''
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
[ 'random_', 'random_integer', 'random_integers' ] ],

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
[ 'random', 'random_integer', 'random_integers' ] ],

    'result' : [
'special', 'loads the result from the previous invokation of rpn',
'''
'result' currently doesn't work with measurements.
''',
'''
''' + makeCommandExample( '2 sqrt' ) + '''
''' + makeCommandExample( 'result sqr' ),
[ 'echo', 'previous' ] ],

    'roll_dice' : [
'special', 'evaluates a dice expression n to simulate rolling dice',
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
'special', 'evaluates dice expression n to simulate rolling dice k times',
'''
Please see 'roll_dice' for an explanation of the dice expression language.

This operator will output k results of dice simulation based on the syntax
described for the 'roll_dice' operator.
''',
'''
''' + makeCommandExample( '2d6 10 roll_dice_' ) + '''
''' + makeCommandExample( '4d6x1 6 roll_dice_' ),
[ 'roll_dice', 'permute_dice', 'enumerate_dice', 'enumerate_dice_' ] ],

    'roll_simple_dice' : [
'special', 'rolls n dice with k sides each',
'''
This operator returns the sum of n randomly generated values from 1 to k.
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
''' + makeCommandExample( 'test_config_key test_config_value set_config' ) + '''
''' + makeCommandExample( 'test_config_key get_config' ),
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

    'topics' : [
'special', 'prints a list of help topics in help mode',
'''
''',
'''
rpn (1)> help
rpn help mode - 'topics' for a list of topics, 'exit' to return to rpn
rpn help>topics
For help on a specific topic, use the topic operator with a general topic, operator category or a specific operator
name.

The following is a list of general topics:

    TODO, about, arguments, bugs, examples, input, interactive_mode, license, metric, notes, old_release_notes,
    options, output, release_notes, settings, time_features, unit_conversion, unit_types, user_functions

    ...
''',
[ 'help' ] ],

    'uuid' : [
'special', 'generates a UUID',
'''
The UUID is generated using the host ID (MAC address if possible, otherwise
see RFC 4122) and the current time.
''',
'''
''' + makeCommandExample( 'uuid' ) + '''
''' + makeCommandExample( 'uuid' ),
[ 'uuid_random' ] ],

    'uuid_random' : [
'special', 'generates a random UUID',
'''
The UUID is generated completely randomly.
''',
'''
''' + makeCommandExample( 'uuid_random' ) + '''
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
[ 'invert_units' ] ],


    #******************************************************************************
    #
    #  trigonometry operators
    #
    #******************************************************************************

    'acos' : [
'trigonometry', 'calculates the arccosine of n',
'''
The arcosine is the inverse of cosine.  In other words, if cos( x ) = y, then
acos( y ) = x.
''',
'''
''' + makeCommandExample( '0 acos' ) + '''
''' + makeCommandExample( '0.5 acos radians degrees convert' ) + '''
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
''',
'''
''' + makeCommandExample( '0 acosh' ) + '''
''' + makeCommandExample( '0.234 acosh cosh' ) + '''
''' + makeCommandExample( '45 degrees cosh acosh radians degrees convert' ),
[ 'acos', 'atanh', 'asinh' ] ],

    'acot' : [
'trigonometry', 'calcuates the arccotangent of n',
'''
The arccotangent is the inverse of the cotangent.
''',
'''
''' + makeCommandExample( '2 sqrt acot cot' ) + '''
''' + makeCommandExample( '5 acoth' ) + '''
''' + makeCommandExample( '1 acot radians degrees convert' ),
[ 'cot', 'acoth', 'acsc', 'asec' ] ],

    'acoth' : [
'trigonometry', 'calculates the hyperbolic arccotangent of n',
'''
The hyperbolic arccotangent is the inverse of the hyperbolic cotangent.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' + makeCommandExample( '43 acoth coth' ) + '''
''' + makeCommandExample( '0.3 acoth' ) + '''
''' + makeCommandExample( '7 acoth radians degrees convert' ),
[ 'acot', 'coth', 'acsch', 'asech' ] ],

    'acsc' : [
'trigonometry', 'calculates the arccosecant of n',
'''
The arccosecant is the inverse of the cosecant.
''',
'''
''' + makeCommandExample( '0.1389 acsc csc' ) + '''
''' + makeCommandExample( '0.75 acsc' ) + '''
''' + makeCommandExample( '8.113 acsc radians degrees convert' ),
[ 'csc', 'asec', 'acsch', 'acot' ] ],

    'acsch' : [
'trigonometry', 'calculates the hyperbolic arccosecant of n',
'''
The hyperbolic arccosecant is the inverse of the hyperbolic cosecant.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' + makeCommandExample( '0.1237 acsch csch' ) + '''
''' + makeCommandExample( '0.25 acsch' ) + '''
''' + makeCommandExample( '0.75 acsch radians degrees convert' ),
[ 'csch', 'acsc', 'acoth', 'asech' ] ],

    'asec' : [
'trigonometry', 'calculates the arcsecant of n',
'''
The arcsecant is the inverse of the secant.
''',
'''
''' + makeCommandExample( '0.1237 sec asec' ) + '''
''' + makeCommandExample( '5 asec radians degrees convert' ) + '''
asec( x ) is the same as acos( 1/x ):
''' + makeCommandExample( '2 asec', indent=4 ) + '''
''' + makeCommandExample( '0.5 acos', indent=4 ),
[ 'sec', 'asech', 'acsc', 'acot' ] ],

    'asech' : [
'trigonometry', 'calculates the hyperbolic arcsecant of n',
'''
The hyperbolic arcsecant is the inverse of the hyperbolic secant.

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.
''',
'''
''' + makeCommandExample( '0.767 sech asech' ) + '''
''' + makeCommandExample( '1 asech' ) + '''
''' + makeCommandExample( '0.5 asech radians degrees convert' ),
[ 'sech', 'acsch', 'asec', 'acoth' ] ],

    'asin' : [
'trigonometry', 'calculates the arcsine of n',
'''
The arcsine is the inverse of sine.  In other words, if sin( x ) = y, then
asin( y ) = x.
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
''' + makeCommandExample( '60 degrees cos' ) + '''
''' + makeCommandExample( '-1 pi 2 / * cos' ),
[ 'sin', 'tan', 'acos', 'cosh' ] ],

    'cosh' : [
'trigonometry', 'calculates the hyperbolic cosine of n',
'''
The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

The hyperbolic cosine can be defined in terms of the exponential function:

         e^x + e^-x
cosh x = ----------
             2

The hyperbolic cosine can also be defined in terms of cosine:

cosh x = cos( ix )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( 'pi 4 / cosh' ) + '''
''' + makeCommandExample( '30 degrees cosh' ) + '''
Comparing hyperbolic cosine to cosine:
''' + makeCommandExample( '0.3 cosh', indent=4 ) + '''
''' + makeCommandExample( '0.3j cos', indent=4 ),
[ 'cos', 'acosh', 'sinh', 'tanh' ] ],

    'cot' : [
'trigonometry', 'calculates the cotangent of n',
'''
The cotangent cot( n ) is the reciprocal of tan( n ); i.e., the ratio of the
length of the adjacent side to the length of the opposite side.

cot( x ) = 1 / tan( x )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '30 degrees cot' ) + '''
Comparing cotangent to tangent:
''' + makeCommandExample( '0.2 cot' ) + '''
''' + makeCommandExample( '0.2 tan 1/x' ),
[ 'coth', 'acot', 'sec', 'csc' ] ],

    'coth' : [
'trigonometry', 'calculates the hyperbolic cotangent of n',
'''
The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

The hyperbolic cotangent can be defined in terms of sinh and cosh:

coth( x ) = cosh( x ) / sinh( x )

The hyperbolic cotangent can also be defined in terms of cotangent:

coth x = i cot( ix )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '67 degrees coth' ) + '''
Comparing hyperbolic cotangent to hyperbolic tangent:
''' + makeCommandExample( '2.3 coth', indent=4 ) + '''
''' + makeCommandExample( '2.3 tanh 1/x', indent=4 ),
[ 'cot', 'acoth', 'csch', 'sech' ] ],

    'csc' : [
'trigonometry', 'calculates the cosecant of n',
'''
The cosecant function is defined to be the reciprocal of the sine function.

csc( x ) = 1 / sin( x )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '45 degrees csc' ) + '''
Comparing cosecant to sine:
''' + makeCommandExample( '36 degrees csc 1/x', indent=4 ) + '''
''' + makeCommandExample( '36 degrees sin', indent=4 ),
[ 'csch', 'acsc', 'sec', 'cot' ] ],

    'csch' : [
'trigonometry', 'calculates hyperbolic cosecant of n',
'''
The hyperbolic cosecant is defined as the reciprocal of the hyperbolic sine
function.

csch( x ) = 1 / sinh( x )

The hyperbolic cosecant can also be defined in terms of the cosecant function:

csch( x ) = i csc( ix )

The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( 'pi 5 / radians csch' ) + '''
Comparing hyperbolic cosecant to hyperbolic sine:
''' + makeCommandExample( 'pi 6 / radians csch 1/x', indent=4 ) + '''
''' + makeCommandExample( 'pi 6 / radians sinh', indent=4 ),
[ 'csc', 'sech', 'acsch', 'coth' ] ],

    'sec' : [
'trigonometry', 'calculates the secant of n',
'''
The secant function is defined to be the reciprocal of the cosine function.

sec( x ) = 1 / cos( x )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '60 degrees sec' ) + '''
''' + makeCommandExample( 'pi 2 / sec' ) + '''
''' + makeCommandExample( '0 sec' ) + '''
Comparing secant to cosine
''' + makeCommandExample( 'pi 7 / sec', indent=4 ) + '''
''' + makeCommandExample( 'pi 7 / cos 1/x', indent=4 ),
[ 'csc', 'sech', 'asec', 'cot' ] ],

    'sech' : [
'trigonometry', 'calculates the hyperbolic secant of n',
'''
The hyperbolic trigonometric functions are analogous to the regular circular
trigonometric functions (sin, cos, etc.), except based on a unit hyperbola
instead of a unit circle.

The hyperbolic secant can be defined in terms of the hyperbolic cosine:

sech( x ) = 1 / cosh( x )

The hyperbolic secant can also be defined in terms of sec:

sech x = sec( ix )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '45 degrees sech' ) + '''
Comparing hyperbolic secant to hyperbolic cosine:
''' + makeCommandExample( '73.5 degrees sech 1/x', indent=4 ) + '''
''' + makeCommandExample( '73.5 degrees cosh', indent=4 ),
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

The hyperbolic sine can be defined in terms of the exponential function:

         e^x - e^-x
sinh x = ----------
             2

The hyperbolic sine can also be defined in terms of sine:

sinh x = -i sin( ix )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '3 degrees sinh' ) + '''
''' + makeCommandExample( 'pi 2 / sinh' ) + '''
Comparing hyperbolic sine to sine:
''' + makeCommandExample( '2 sinh', indent=4 ) + '''
''' + makeCommandExample( '-1j 2j sin *', indent=4 ),
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

The hyperbolic tangent can be defined in terms of sinh and cosh:

tanh x = sinh x / cosh x

The hyperbolic tangent can also be defined in terms of tangent:

tanh x = -i tan( ix )

All trigonometric operators that take angles assume the arguments are in
radians.  However, the operators also take measurements as arguments, so they
can handle a value in degrees without having to first convert.
''',
'''
''' + makeCommandExample( '3 pi * 4 / radians tanh' ) + '''
Comparing hyperbolic tangent to hyperbolic sine/hyperbolic cosine and tangent:
''' + makeCommandExample( '4 pi * 7 / tanh', indent=4 ) + '''
''' + makeCommandExample( '4 pi * 7 / ( sinh cosh ) unlist /', indent=4 ) + '''
''' + makeCommandExample( '-4j pi * 7 / i * tan', indent=4 ),
[ 'tan', 'atanh', 'cosh', 'sinh' ] ],

}


#******************************************************************************
#
#  makeHelp
#
#******************************************************************************

def makeHelp( helpTopics ):
    '''Builds the help data file.'''
    fileName = getUserDataPath( ) + os.sep + 'help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( helpTopics, pickleFile )
        pickle.dump( operatorHelp, pickleFile )

    print( )


#******************************************************************************
#
#  main
#
#******************************************************************************

def main( ):
    unitsFile = Path( getUserDataPath( ) + os.sep + 'units.pckl.bz2' )

    if not unitsFile.is_file( ):
        print( 'Please run "rpnMakeUnits" (or makeUnits.py) to initialize the unit conversion data files.' )
        sys.exit( 0 )

    from rpn.rpnConstantOperators import constantOperators

    for constant in constantOperators:
        helpText = '\n\'' + constant + '\' returns a value of ' + str( constantOperators[ constant ].value )

        if constantOperators[ constant ].unit:
            helpText += ' ' + constantOperators[ constant ].unit

        helpText += '\n'

        operatorHelp[ constant ] = [ \
            'constants', constantOperators[ constant ].description,
            helpText + constantOperators[ constant ].helpText, '', [ 'constants' ]
        ]

    for unit in g.unitOperators:
        unitInfo = g.unitOperators[ unit ]

        description = '\'' + unit + '\' is a unit of ' + unitInfo.unitType

        operatorHelp[ unit ] = [ unitInfo.unitType, description, unitInfo.helpText, '', [ 'unit_types' ] ]

    makeHelp( helpTopics )

    noCategory = [ ]
    noDescription = [ ]
    noHelpText = [ ]
    noExamples = [ ]
    noCrossReferences = [ ]
    badCrossReferences = set( )

    for topic, help in operatorHelp.items( ):
        if len( help ) != 5:
            print( 'error: malformed help data for topic \'' + topic + '\'' )
            continue

        if not help[ 0 ]:
            noCategory.append( topic )

        if not help[ 1 ]:
            noDescription.append( topic )

        if ( not help[ 2 ] or help[ 2 ] == '\n' ) and \
           topic not in g.unitOperators:
            noHelpText.append( topic )

        if ( not help[ 3 ] or help[ 3 ] == '\n' ) and \
           ( topic not in g.unitOperators and topic not in constantOperators ):
            noExamples.append( topic )

        if len( help[ 4 ] )== 0:
            noCrossReferences.append( topic )
        else:
            for crossReference in help[ 4 ]:
                if crossReference not in g.unitOperators and crossReference not in constantOperators and \
                   crossReference not in operatorHelp and crossReference not in ( 'constants', 'unit_types' ):
                    badCrossReferences.add( crossReference )

    if noCategory:
        print( )
        print( 'The following {} topics do not have a category defined:'.format( len( noCategory ) ) )
        print( )
        printParagraph( ', '.join( sorted( noCategory ) ) )

    if noDescription:
        print( )
        print( 'The following {} topics do not have any description:'.format( len( noDescription ) ) )
        print( )
        printParagraph( ', '.join( sorted( noDescription ) ) )

    if noHelpText:
        print( )
        print( 'The following {} topics do not have any help text:'.format( len( noHelpText ) ) )
        print( )
        printParagraph( ', '.join( sorted( noHelpText ) ) )

    if noExamples:
        print( )
        print( 'The following {} topics do not have any examples:'.format( len( noExamples ) ) )
        print( )
        printParagraph( ', '.join( sorted( noExamples ) ) )

    if noCrossReferences:
        print( )
        print( 'The following {} topics do not have any cross references:'.format( len( noCrossReferences ) ) )
        print( )
        printParagraph( ', '.join( sorted( noCrossReferences ) ) )

    if badCrossReferences:
        print( )
        print( 'The following {} cross references are invalid:'.format( len( badCrossReferences ) ) )
        print( )
        printParagraph( ', '.join( sorted( badCrossReferences ) ) )

    print( )
    print( 'Help data completed.  Time elapsed:  {:.3f} seconds'.format( ( time_ns( ) - startTime ) / 1_000_000_000 ) )


#******************************************************************************
#
#  __main__
#
#******************************************************************************

if __name__ == '__main__':
    main( )

