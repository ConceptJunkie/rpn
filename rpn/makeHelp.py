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
import pickle
import os
import sys
import time

from pathlib import Path

from rpn.rpn import rpn, handleOutput
from rpn.rpnNumberTheory import mersennePrimeExponents
from rpn.rpnOutput import printParagraph
from rpn.rpnPrimeUtils import checkForPrimeData
from rpn.rpnUtils import getUserDataPath
from rpn.rpnVersion import PROGRAM_VERSION, PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE, RPN_PROGRAM_NAME

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

MAX_EXAMPLE_COUNT = 2426

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
parser.add_argument( '-q', '--quiet', action = 'store_true' )

args = parser.parse_args( sys.argv[ 1 : ] )

HELP_DEBUG_MODE = args.debug
QUIET_MODE = args.quiet

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
    # print( command )
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
        print( '\r', ' ' * 60, end='' )

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
#    -o, --refresh_oeis_cache
#        redownload content from the OEIS, since existing sequences are very occasionally updated
#


helpTopics = {
    # pylint: disable=bad-continuation
    'options' :
    'rpn' + PROGRAM_VERSION_STRING + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE + '\n\n' + '''
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
        octal mode: equivalent to \'-r8 -w9 -g3 -z\'

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
        hex mode: equivalent to '-r16 -w16 -g4 -z'

    -y, --identify
        identify the result (may just repeat input)

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
''' + makeCommandExample( '[ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *', indent=4 ) + '''
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
This feature allows the user to define a function for use with the 'eval',
'ranged_sum', 'ranged_product', 'limit' and 'decreasing_limit' operators, etc.
'lambda' starts an expression that becomes a function.

rpn user fuctions can use up to 3 variables, x, y, and z.  rpn provides a
number of operators that can be used with user functions.  See, 'rpn help
functions' for information about these operators.

User functions cannot currently contain list literals or measurements.

Some examples:
''' + makeCommandExample( '3 lambda x 2 * eval', indent=4 ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval', indent=4 ) + '''
''' + makeCommandExample( 'inf lambda x 1 + fib x fib / limit', indent=4 ) + '''
''' + makeCommandExample( '1 inf lambda 2 x ** 1/x ranged_sum', indent=4 ) + '''
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
equivalent to the '-y" command-line option.

identify_mode:  Aliased to '-y'.

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

"rpn 1 200 range fib lambda x factor 100 filter_min 999 filter_max eval -a50"
crashes!  The same operation without the lambda works fine.  It has something to
do with nested generators inside lambdas.

'$varname' syntax doesn't work in interactive mode!

"rpn 4 lambda 1 x range powerset geometric_mean eval" loses the first item in
the powerset.  Trying it without 'geometric_mean' shows the powerset correctly.
But adding the 'geometric_mean' operator gives results that clearly don'tlambert
include the first result of the powerset '[ 1 ]'.  This might be related to the
'filter_min'/'filter_max' problem above.  I bet it has something to do with
generators.

-i doesn't work for lists.

'(' and ')' (multiple operators) don't work with generators because the
generator only works once.   The structure of the evaluator won't allow me to
fix this, I think.  It may have to wait until I convert all rpn expressions to
Python before this can be fixed.

'collate' does not work with generators.

-d needs to parse out the scientific notation part of the value

Converting negative numbers to different bases gives weird answers.

-u doesn't work with complex numbers

'result' doesn't work with measurements.

User-defined functions can't include measurements.

"rpn 1 1 4 range range 10 15 range 1 3 range range2" crashes because
operators that take more than 2 arguments don't handle recursive list
arguments.  I need a @threeArgFunctionEvaluator, except that would be insane to
write, so I really need a generic function evaluator, and I think I might know
how I can do that.

'reversal_addition' doesn't work with generators.  I see a theme here.

See 'rpn help TODO'.
    ''',
    'TODO' :
    '''
This is my informal, short-term todo list for rpn.  It often grows and seldom
gets smaller.

*  'humanize' - like 'name' but only 2 significant digits when > 1000

*  'name' should handle fractions smaller than 1 gracefully (right now it
   prints nothing)

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

A few more bug fixes, plus new calendar-related operators:  'easter'.
'election_day', 'labor_day', 'memorial_day', 'nthday', 'presidents_day',
'thanksgiving'.

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
"99.99999j", or "99.9999i" i.e., any regular number appended with an 'i' or 'j'.
The 'i' operator remains, but can be considered deprecated, as it is no longer
needed.

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

8.5.0

Big Clean-Up and Documentation Release!

Much more thorough argument validation has been implemented on all operators.
In addition, all non-constant operator function names now end with 'Operator',
which means I can be sure they are not being called recursively, or being called
by other operator functions, so that the argument expansion and validation isn't
being done more than once.

I have continued my focus on completing the online help, which is now more than
95% complete.  This also resulted in a number of operators being eliminated (see
below), and a bevy of bug fixes.

The help for units is now complete.  Every unit has help text.

The 'number_from_file' and 'get_decimal_digits' operators have been added.

Time zone handling has been improved.  'to_time_zone', 'set_time_zone' and
'to_local_time' have been added.

'lat_long_to_nac' was removed (after I fixed it), since the developers of the
Natural Area Code claim a copyright on the system itself, and do not allow
outside implementations.  I guess they don't want people adopting their system.
<shrug>

I removed the 'cyclotomic' operator, since I don't understand it enough to
explain what it does or why it's useful.  I'm just exposing an mpmath function.
Some day I'll probably go through an expose all those mpmath functions that I
haven't already.

I removed 'planck_angular_frequency' since there is some confusion as to how it
should be defined.   Plus, it isn't very interesting.
(see https://chemphys.ca/pbunker/PlanckWiki.pdf)

I removed the 'planck_pressure' operator since it was identical to the
'planck_energy_density' operator.

I removed 'iso_date' and 'iso_day' which _both_ duplicated 'to_iso'.  Also,
'make_iso_time' was essentially a duplicate function as well, so it's been
removed.

I renamed the following operators to be more consistent:
'get_utc' --> 'to_utc'
'get_local_time' --> 'to_local_time'
'num' --> 'ranged_sum'
'nprod' --> 'ranged_product'
'power_tower2' --> 'power_tower_right'
'is_friendly' --> 'is_sociable_list'
'limitn' --> 'decreasing_limit'

Removed a couple of unit types for which I could not find sufficient
documentation.  In particular the Talk page on Wikipedia claims that a couple of
the wine bottle sizes they had previously reported could not be verified.

Removed the 'filter_lists' operator because it isn't needed.  'filter' works
fine on a list of lists.

I got rid of the 'repeat' operator because I literally couldn't think of a use
for i

I eliminated 'eval_list2' and 'eval_list3' because I couldn't figure out how to
contrive a meaningful example, and therefore don't think they would be useful.

The 'recurrence' operator was removed, because it was a duplicate of the
'sequence' operator.
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
''' + makeCommandExample( '2 sqrt 20 make_continued_fraction', indent=8 ) + '''
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
''' + makeCommandExample( '1 1 5 nth_prime lambda 1 x prime 1/x - ranged_product - 100 *', indent=8 ) + '''
    What percentage of numbers have a factor less than 100?
''' + makeCommandExample( '1 1 100 nth_prime lambda 1 x prime 1/x - ranged_product - 100 *', indent=8 ) + '''
    What percentage of numbers have a factor less than 1000?
''' + makeCommandExample( '1 1 1000 nth_prime lambda 1 x prime 1/x - ranged_product - 100 *', indent=8 ) + '''

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
                          'gamma 11 24 / gamma ] prod 1/x * -', indent=8 ) + '''
    Schwartzchild Constant (Conic Constant)
''' + makeCommandExample( '0 inf lambda 2 x ** x ! / ranged_sum', indent=8 ) + '''
''' + makeCommandExample( 'e 2 **', indent=8 ) + '''
    Somos\' Quadratic Recurrence Constant
''' + makeCommandExample( '-a20 1 inf lambda x 1 2 x ** / power ranged_product', indent=8 ) + '''
    Prevost Constant
''' + makeCommandExample( '-a20 1 inf lambda x fib 1/x ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 prevost_constant', indent=8 ) + '''
    Euler's number
''' + makeCommandExample( '-a20 0 inf lambda x ! 1/x ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e', indent=8 ) + '''
    Gelfond Constant
''' + makeCommandExample( '-a20 0 inf lambda pi x power x ! / ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e pi power', indent=8 ) + '''
    Bloch-Landau Constant
''' + makeCommandExample( '-a20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /', indent=8 ) + '''
    Hausdorff Dimension
''' + makeCommandExample( '-a20 0 inf lambda 2 x 2 * 1 + power x 2 * 1 + * 1/x ranged_sum 0 inf '
                          'lambda 3 x 2 * 1 + power x 2 * 1 + * 1/x ranged_sum /', indent=8 ) + '''
''' + makeCommandExample( '-a20 3 log 2 log /', indent=8 ) + '''
    Beta( 3 )
''' + makeCommandExample( '-a20 0 inf lambda x 2 * 1 + 3 power 1/x -1 x ** * ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 pi 3 power 32 /', indent=8 ) + '''
    Lemniscate Constant
''' + makeCommandExample( '-a20 4 2 pi / sqrt * 0.25 ! sqr *', indent=8 ) + '''
    sqrt( e )
''' + makeCommandExample( '-a20 0 inf lambda 2 x power x ! * 1/x ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 0 inf lambda x 2 * !! 1/x ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e sqrt', indent=8 ) + '''
    1/e
''' + makeCommandExample( '-a20 0 inf lambda x ! 1/x -1 x ** * ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 e 1/x', indent=8 ) + '''
    An approximation of Zeta( 6 )
''' + makeCommandExample( '-a20 -p30 1 1 1000 primes -6 power - 1/x prod', indent=8 ) + '''
''' + makeCommandExample( '-a20 pi 6 power 945 /', indent=8 ) + '''
''' + makeCommandExample( '-a20 6 zeta', indent=8 ) + '''
    Ramanujan-Forsythe Constant
''' + makeCommandExample( '0 inf lambda x 2 * 3 - !! x 2 * !! / sqr ranged_sum', indent=8 ) + '''
    Apery's Constant
''' + makeCommandExample( '-a20 1 inf lambda x 3 power 1/x ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '-a20 3 zeta', indent=8 ) + '''
''' + makeCommandExample( '-a20 apery', indent=8 ) + '''
    An approximation of the Omega Constant
''' + makeCommandExample( '-a20 [ e 1/x 100 dup ] power_tower_right', indent=8 ) + '''
''' + makeCommandExample( '-a20 omega', indent=8 ) + '''
    Liouville Number
''' + makeCommandExample( '-a120 1 inf lambda 10 x ! power 1/x ranged_sum', indent=8 ) + '''
    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                0 100000 range 3 * 2 + sqr 1/x sum -
                1 100000 range 3 * 1 + sqr 1/x sum + *

    An approximation of the Hafner-Sarnak-McCurley Constant (2)
''' + makeCommandExample( '-a7 1 1 100000 primes sqr 1/x - prod', indent=8, slow=True ) + '''
''' + makeCommandExample( '2 zeta 1/x', indent=8 ) + '''
    An approximation of the infinite tetration of i
''' + makeCommandExample( '-a20 [ 1j 1000 dup ] power_tower_right', indent=8 ) + '''
    Cahen's Constant
''' + makeCommandExample( '1 inf lambda x nth_sylvester 1 - 1/x -1 x 1 + ** * ranged_sum', indent=8 ) + '''
    Erdos-Borwein Constant
''' + makeCommandExample( '1 inf lambda 2 x ** 1 - 1/x ranged_sum', indent=8 ) + '''
    An approximation of the Heath-Brown-Moroz constant
''' + makeCommandExample( '-a6 1 60000 primes lambda 1 x 1/x - 7 ** 1 7 x * 1 + x sqr / + * eval prod',
                          indent=8, slow=True ) + '''
    Kepler-Bouwkamp constant
''' + makeCommandExample( '3 inf lambda pi x / cos ranged_product', indent=8 ) + '''
    Ramanujan-Forsyth series
''' + makeCommandExample( '0 inf lambda x 2 * 3 - !! x 2 * !! / sqr ranged_sum', indent=8 ) + '''
    Machin-Gregory series
''' + makeCommandExample( '0 inf lambda -1 x ** 1 2 / 2 x * 1 + ** * 2 x * 1 + / ranged_sum', indent=8 ) + '''
''' + makeCommandExample( '1 2 / arctan', indent=8 ) + '''
    Somos quadratic recurrence constant
''' + makeCommandExample( '1 inf lambda x 1 + x / 2 x ** root ranged_product', indent=8 ) + '''
    Niven's constant
''' + makeCommandExample( '1 2 inf lambda 1 x zeta 1/x - ranged_sum +', indent=8 ) + '''
    Kepler-Bouwkamp constant
''' + makeCommandExample( '3 inf lambda pi x / cos ranged_product', indent=8 ) + '''
    Exponential Factorial Constant
''' + makeCommandExample( '-p80 -a20 1 inf lambda 1 x 1 range power_tower / ranged_sum', indent=8 ) + '''
    Conway's Constant
''' + makeCommandExample( '-p80 -a20 [ 1, 0, -1, -2, -1, 2, 2, 1, -1, -1, -1, -1, -1, 2, 5, 3, -2, -10, -3, -2, 6, 6, '
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
'algebra', 'adds two polynomials',
'''
This operator interprets two lists as polynomials and adds them.

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
This operator calculates the discriminant of polynomial n (n is a list of
coefficients of the powers of x in decreasing order).

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
This operator solves for the roots of a polynomial, using mpmath's numerical
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
This operator solves a cubic equation described by the 4 arguments.  It returns
the two roots of the equation.

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
This operator solves a quadratic equation described by the 3 arguments.  It
returns the two roots of the equation.

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
This operator solves a quartic equation described by the 5 arguments.  It
returns the four roots of the equation.

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
This operator calculates the absolute value of n.

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
This operator calculates the antiharmonic mean of a a list of numbers n.

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
This operator is the equivalent of 'n 1 subtract' and is provided as a
convenience.
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
This operator calculates the greatest common denominator of elements in list n.

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
This operator calculates the greatest common denominator of n and k.

'n k gcd2' is equivalent to '[ n k ] gcd'
''',
'''
''' + makeCommandExample( '5 20 gcd2' ) + '''
''' + makeCommandExample( '3150 8820 gcd2' ),
[ 'reduce', 'lcm', 'gcd', 'relatively_prime' ] ],

    'geometric_mean' : [
'arithmetic', 'calculates the geometric mean of a a list of numbers n',
'''
This operator calculates the geometric mean of a a list of numbers n.

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
This operator calculates the harmonic mean of a a list of numbers n.

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
This operator is the equivalent of 'n 1 add', and is provided as a convenience.
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
This operator returns true (1) is n is an integer, and false (0) if it is not.
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
This operator returns true (1) if n is a perfect kth power, otherwise it returns
false (0).

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
This operator returns true (1) is n is less than k, otherwise it returns false
(0).

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
This operator returns true (1) is n does not equal k, otherwise it returns false
(0).
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
This operator returns true (1) if n is not greater than k, otherwise it returns
false (0).  'is_not_greater' is the equivalent of less than or equal.

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
This operator returns true (1) if n is not less than k, otherwise it returns
false (0).  'is_not_less' is the equivalent of greater than or equal.

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
This operator returns true (1) if n is not zero, otherwise it returns false (0).
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
This operator returns 1 if the argument is an odd integer (i.e., an integer n
such that n % 2 == 1), otherwise it returns 0.

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
This operator returns true (1) if n is an integral power of k, otherwise it
returns false (0).  It accepts complex arguments.
''',
'''
''' + makeCommandExample( '16 4 is_power_of_k' ) + '''
''' + makeCommandExample( '32 2 is_power_of_k' ),
[ 'is_square', 'is_kth_power' ] ],

    'is_square' : [
'arithmetic', 'returns whether n is a perfect square',
'''
This operator returns true (1) if n is a perfect square, otherwise it returns
false (0).

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
This operator returns true (1) if n is zero, otherwise it returns false (0).
This is simply a check for a zero value.

The operator is primarily useful in lambdas.  It is actually identical to the
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
This operator calculates the least common multiple (LCM) of n and k.

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
This operator returns the decimal part of n.  It is the equivalent of
'n n floor -'.

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
This operator calculates the mean of values in list n.

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
This operator calculates n modulo k.

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
This operator calculates the negative of n.

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
This operator returns the nearest integer to n.

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
This operator calculates the product of the values in list n.

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
This operator returns the reciprocal of n.

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
This operator calculates the root mean square of the values in list n.

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
The operator rounds n to the nearest integer.

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
This operator rounds n to the nearest kth power of 10.

Note that 'n round' is the equivalent of 'n 0 round_by_digits'.

'round_by_digits' requires a real argument.  If the value is exactly halfway
between the least significant digit, 'round_by_digits' will round up.
''',
'''
''' + makeCommandExample( '12 1 round_by_digits' ) + '''
''' + makeCommandExample( '12 0 round_by_digits' ) + '''
''' + makeCommandExample( '567 3 round_by_digits' ) + '''
''' + makeCommandExample( 'pi -3 round_by_digits' ) + '''
''' + makeCommandExample( '-a15 pi -13 round_by_digits -d' ),
[ 'round', 'round_by_value', 'nearest_int' ] ],

    'round_by_value' : [
'arithmetic', 'rounds n to the nearest multiple of k',
'''
This operator rounds n to the nearest multiple of k.

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
'arithmetic', 'returns the sign of n',
'''
This operator retuens the sign of n.

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
This operator calculates the standard deviation of the values in list n.

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
''' + makeCommandExample( '10 10000 random_integers stddev' ) + '''
''' + makeCommandExample( '1 100 range count_divisors stddev' ),
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
This operator calculates the sum of the values in list n.

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


    'earth2' : [
'astronomical_objects', 'the Earth',
'''
This operator represents the planet Earth for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''',
[ 'venus2', 'mars2' ] ],

    'jupiter2' : [
'astronomical_objects', 'the planet Jupiter',
'''
This operator represents the planet Jupiter for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'jupiter2 "Stuttgart, Germany" 2020-01-01 next_rising' ),
[ 'mars2', 'saturn2' ] ],

    'mars2' : [
'astronomical_objects', 'the plenet Mars',
'''
This operator represents the planet Mars for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'mars2 "San Francisco, California" 2019-05-23 next_setting' ),
[ 'earth2', 'jupiter2' ] ],

    'mercury2' : [
'astronomical_objects', 'the planet Mercury',
'''
This operator represents the planet Mercury for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'mercury "Helsinki, Finland" 2019-04-28 transit_time' ),
[ 'venus2', 'mars2' ] ],

    'moon2' : [
'astronomical_objects', 'the Moon',
'''
This operator represents the Moon for the new versions of the astronomical
operators based on the SkyField library, rather the pyephem library.
''',
'''
''' + makeCommandExample( 'moon2 "Leesburg, VA" "2019-05-10 11:00:00" sky_location' ),
[ 'earth2', 'mars2' ] ],

    'neptune2' : [
'astronomical_objects', 'the plent Neptune',
'''
This operator represents the planet Neptune for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'neptune2 "Sao Paulo, Brazil" 2019-05-23 previous_rising' ),
[ 'uranus2', 'pluto2'  ] ],

    'pluto2' : [
'astronomical_objects', 'the planet Pluto',
'''
This operator represents the planet Pluto for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.

Yes, I still consider Pluto a planet.  Talk to the hand.
''',
'''
''' + makeCommandExample( 'pluto2 "2019-05-09 09:23:00" distance_from_earth miles convert -c' ),
[ 'uranus2', 'neptune2' ] ],

    'saturn2' : [
'astronomical_objects', 'the planet Saturn',
'''
This operator represents the planet Saturn for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'saturn2 now distance_from_earth c / hms' ),
[ 'jupiter2', 'uranus2' ] ],

    'sun2' : [
'astronomical_objects', 'the Sun',
'''
This operator represents the Sun for the new versions of the astronomical
operators based on the SkyField library, rather the pyephem library.
''',
'''
''' + makeCommandExample( 'sun2 "Richmond, VA" "2019-05-10 13:45:00" sky_location' ),
[ 'moon2', 'venus2' ] ],

    'uranus2' : [
'astronomical_objects', 'the planet Uranus',
'''
This operator represents the planet Uranus for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'uranus "Harrisburg, PA" "2019-04-29" antitransit_time hms' ),
[ 'saturn2', 'neptune2' ] ],

    'venus2' : [
'astronomical_objects', 'the planet Venus',
'''
This operator represents the planet Venus for the new versions of the
astronomical operators based on the SkyField library, rather the pyephem
library.
''',
'''
''' + makeCommandExample( 'venus2 "Boulder, Colorado" "2019-04-15 06:00:00" next_rising' ),
[ 'mercury2', 'earth2' ] ],


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
[ 'sky_location', 'angular_size', 'distance_from_sun' ] ],

    'distance_from_sun' : [
'astronomy', 'returns the distance from the Sun of astronomical object n for date-time k',
'''
This operator returns the distance of the astronomical body n from the Sun at
date-time k.
''',
'''
''' + makeCommandExample( '-c mars2 "2018-07-10 16:00" distance_from_sun miles convert' ) + '''
''' + makeCommandExample( '-c jupiter2 "2018-07-10 16:00" distance_from_sun miles convert' ),
[ 'sky_location', 'angular_size', 'distance_from_earth' ] ],

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
What was the phase of the moon the day I got married:
''' + makeCommandExample( '"1993-04-17 10:30:00" moon_phase', indent=4 ) + '''
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
This operator returns the date of the next antitransit of body a, when viewed
from location b, at date c.  The antitransit is defined as the point where the
body crosses the anti-meridian.

The meridian is defined as the line running overhead from the celestial North
pole to the South pole, and the anti-meridian as the other half of the same
great circle; so the transit and anti-transit operators always succeed, whether
the body crosses the horizon or not.
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
''' + makeCommandExample( '2030-01-01 next_last_quarter_moon' ),
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
This operator returns the next rising of astronomical body a, when viewed from
location b, starting at date-time c.
''',
'''
''' + makeCommandExample( 'jupiter "London, UK" now next_rising' ) + '''
''' + makeCommandExample( 'saturn "Beijing, China" 2019-05-31 next_rising' ),
[ 'previous_rising', 'next_setting', 'next_transit', 'next_antitransit' ] ],

    'next_setting' : [
'astronomy', 'returns the date of the next setting of body a, when viewed from location b, at date c',
'''
This operator returns the next setting of astronomical body a, when viewed from
location b, starting at date-time c.
''',
'''
''' + makeCommandExample( 'neptune "Paris, France" now next_setting' ) + '''
''' + makeCommandExample( 'mercury "Gary, Indiana" 2019-06-30 next_setting' ),
[ 'previous_setting', 'next_rising', 'next_transit', 'next_antitransit' ] ],

    'next_transit' : [
'astronomy', 'returns the date of the next transit of body a, when viewed from location b, at date c',
'''
This operator returns the date of the next transit of body a, when viewed from
location b, at date c.  The transit is defined as the point where the body
crosses the meridian.  In the case of the Sun, this is considered "solar noon".

The meridian is defined as the line running overhead from the celestial North
pole to the South pole, and the anti-meridian as the other half of the same
great circle; so the transit and anti-transit operators always succeed, whether
the body crosses the horizon or not.
''',
'''
''' + makeCommandExample( 'moon "Albuquerque, NM" 2019-05-03 next_transit' ) + '''
''' + makeCommandExample( 'uranus "Lexington, KY" 2016-03-30 next_transit' ),
[ 'previous_transit', 'next_rising', 'next_setting', 'next_antitransit' ] ],

    'night_time' : [
'astronomy', 'calculates the duration of the next night (i.e., antitransit_time for the sun)',
'''
Thie operator calculates the calculates the duration of the next night (i.e.,
'antitransit_time' for the sun).

This is also the amount of time between sunset and sunrise.
''',
'''
''' + makeCommandExample( '"Washington, DC" 2017-04-08 night_time' ) + '''
''' + makeCommandExample( '"Washington, DC" 2017-04-09 sunrise "Washington, DC" 2017-04-08 sunset -' ),
[ 'day_time', 'dawn', 'dusk', 'transit_time', 'antitransit_time', 'night_time' ] ],

    'previous_antitransit' : [
'astronomy', 'returns the date of the previous antitransit of body a, when viewed from location b, at date c',
'''
This operator returns the date of the previous antitransit of body a, when
viewed from location b, at date c.  The antitransit is defined as the point
where the body crosses the anti-meridian.

The meridian is defined as the line running overhead from the celestial North
pole to the South pole, and the anti-meridian as the other half of the same
great circle; so the transit and anti-transit operators always succeed, whether
the body crosses the horizon or not.
''',
'''
''' + makeCommandExample( 'mercury "Tulsa, OK" 2019-06-03 previous_antitransit' ) + '''
''' + makeCommandExample( 'pluto "Lincoln, NE" 2018-01-12 previous_antitransit' ),
[ 'next_antitransit', 'previous_rising', 'previous_setting', 'previous_transit' ] ],

    'previous_first_quarter_moon' : [
'astronomy', 'returns the date of the previous first quarter moon before date-time n',
'''
This operator returns the time of the most recent previous first quarter moon
before date-time n.
''',
'''
''' + makeCommandExample( 'today previous_first_quarter_moon' ) + '''
''' + makeCommandExample( '1988-05-03 previous_first_quarter_moon' ),
[ 'next_first_quarter_moon', 'previous_last_quarter_moon', 'previous_full_moon', 'previous_new_moon' ] ],

    'previous_full_moon' : [
'astronomy', 'returns the date of the previous full moon before date-time n',
'''
This operator returns the time of the most recent previous full moon before
date-time n.
''',
'''
''' + makeCommandExample( 'today previous_full_moon' ) + '''
''' + makeCommandExample( '2016-10-31 previous_full_moon' ) + '''
''' + makeCommandExample( '2005-06-23 previous_full_moon' ),
[ 'next_full_moon', 'previous_last_quarter_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_last_quarter_moon' : [
'astronomy', 'returns the date of the previous last quarter moon before date-time n',
'''
This operator returns the time of the most recent previous last quarter moon
before date-time n.
''',
'''
''' + makeCommandExample( 'today previous_last_quarter_moon' ) + '''
''' + makeCommandExample( '1971-01-01 previous_last_quarter_moon' ),
[ 'next_last_quarter_moon', 'previous_full_moon', 'previous_first_quarter_moon', 'previous_new_moon' ] ],

    'previous_new_moon' : [
'astronomy', 'returns the date of the previous new moon before date-time n',
'''
This operator returns the time of the most recent previous new moon before
date-time n.
''',
'''
''' + makeCommandExample( 'today previous_new_moon' ) + '''
''' + makeCommandExample( '2020-03-19 previous_new_moon' ),
[ 'next_new_moon', 'previous_full_moon', 'previous_first_quarter_moon', 'previous_last_quarter_moon' ] ],

    'previous_rising' : [
'astronomy', 'returns the date of the previous rising of body a, when viewed from location b, at date c',
'''
This operator returns the most recent previous rising of astronomical body a,
when viewed from location b, starting at date-time c.
''',
'''
''' + makeCommandExample( 'saturn "New York City, NY" 2012-12-11 previous_rising' ) + '''
''' + makeCommandExample( 'mars "San Diego, CA" 2019-06-30 previous_rising' ),
[ 'next_rising', 'previous_setting', 'previous_transit', 'previous_antitransit' ] ],

    'previous_setting' : [
'astronomy', 'returns the date of the previous setting of body a, when viewed from location b, at date c',
'''
This operator returns the most recent previous setting of astronomical body a,
when viewed from location b, starting at date-time c.
''',
'''
''' + makeCommandExample( 'neptune "Paris, France" now previous_setting' ) + '''
''' + makeCommandExample( 'mercury "Gary, Indiana" 2019-06-30 previous_setting' ),
[ 'next_setting', 'previous_rising', 'previous_transit', 'previous_antitransit' ] ],

    'previous_transit' : [
'astronomy', 'returns the date of the previous transit of body a, when viewed from location b, at date c',
'''
This operator returns the date of the previous transit of body a, when viewed
from location b, at date c.  The transit is defined as the point where the body
crosses the meridian.  In the case of the Sun, this is considered "solar noon".

The meridian is defined as the line running overhead from the celestial North
pole to the South pole, and the anti-meridian as the other half of the same
great circle; so the transit and anti-transit operators always succeed, whether
the body crosses the horizon or not.
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
''' + makeCommandExample( 'sun "Indianapolis, IN" "2020-09-10 09:14:00" sky_location' ) + '''
''' + makeCommandExample( 'moon "Indianapolis, IN" "2020-09-10 09:14:00" sky_location' ),
[ 'distance_from_earth', 'angular_size', 'distance_from_sun' ] ],

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
This operator calculates the next sun antitransit time at location n for
date-time k.

Think of it sort of like "anti-solar-noon".
''',
'''
''' + makeCommandExample( '"Bridgeford, CT" today sun_antitransit' ),
[ 'solar_noon', 'sunrise', 'sunset' ] ],

    'transit_time' : [
'astronomy', 'calculates the duration of time from the next rising until the subseqent setting of a body',
'''
This operator calculates the duration of time from the next rising until the
subseqent setting of astronomical body a, when viewed from location b, starting
at date-time c.
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
'bitwise_and' is the logical operation which returns true if and only if the two
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
'bitwise_nand' is the logical operation, 'not and' which returns true if zero or
one of the operands is true.

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
'bitwise_nor' is the logical operation 'not or', which returns true if and only
if neither of the two operands is true.

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
'bitwise_not' is the logical operation, which returns the opposite of the
operand.

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
'bitwise_or' is the logical operation which returns true if at least one of the
two operands is true.

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
'bitwise_xnor' is the 'exclusive nor' logical operation, which returns true if
and only if the two operands are the same.

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
'bitwise_xor' is the 'exclusive or' logical operation, which returns true if and
only if the two operands are different.

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
'calendars', 'returns the date of the first Sunday of Advent for the year n',
'''
This operator eturns the date of the first Sunday of Advent for the year
specified.

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
'calendars', 'returns the date of Ascension Thursday for the year n',
'''
This operator returns the date of Ascension Thursday for the year specified.

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
'calendars', 'calculates the date of Ash Wednesday for the year n',
'''
This operator calculates the date of Ash Wednesday for the year specified.

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
This operator prints a month calendar for date-time n.

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
[ 'year_calendar', 'weekday', 'weekday_name' ] ],

    'christmas' : [
'calendars', 'returns the date of Christmas for the year n',
'''
This operator returns the date of Christmas for the year specified.

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
This operator returns the date of Columbus Day (US) for the year specified.

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
This operator calculates the ending date for Daylight Saving Time (US) for the
year specified.

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
This operator calculates the starting date for Daylight Saving Time (US) for the
year specified.

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
This operator calculates the date of Easter for the year specified.

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
This operator calculates the date of Election Day (US) for the year specified.

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
This operator eturns the date of Epiphany for the year n.

From https://en.wikipedia.org/wiki/Epiphany_(holiday):

Epiphany is a Christian feast day that celebrates the revelation (theophany) of
God incarnate as Jesus Christ.

In Western Christianity, the feast commemorates principally (but not solely) the
visit of the Magi to the Christ Child, and thus Jesus' physical manifestation to
the Gentiles.  It is sometimes called Three Kings' Day, and in some traditions
celebrated as Little Christmas.  Moreover, the feast of the Epiphany, in some
denominations, also initiates the liturgical season of Epiphanytide.

The traditional date for the feast is January 6.
''',
'''
''' + makeCommandExample( '2011 epiphany' ) + '''
''' + makeCommandExample( '2019 2022 range epiphany' ),
[ 'christmas', 'easter' ] ],

    'fathers_day' : [
'calendars', 'calculates the date of Father\'s Day (US) for the year n',
'''
This operator calculates the date of Father\'s Day (US) for the year specified.

From https://en.wikipedia.org/wiki/Father%27s_Day:

Father's Day is a day of honoring fatherhood and paternal bonds, as well as the
influence of fathers in society.  In Catholic countries of Europe, it has been
celebrated on March 19 as Saint Joseph's Day since the Middle Ages.  In America,
Father's Day was founded by Sonora Smart Dodd, and celebrated on the third
Sunday of June for the first time in 1910.  It is held on various days in many
parts of the world all throughout the year, often in the months of March, May
and June.

In the U.S., and most other countries, Father's Day occurs on the third Sunday
in June.  This is the definition that rpn uses.
''',
'''
''' + makeCommandExample( 'today fathers_day' ) + '''
''' + makeCommandExample( '1994 fathers_day' ),
[ 'mothers_day', 'thanksgiving' ] ],

    'from_bahai' : [
'calendars', 'converts a date in the Baha\'i calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Baha'i calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '177 7 10 from_bahai' ) + '''
''' + makeCommandExample( '1 1 1 from_bahai' ),
[ 'to_bahai', 'to_bahai_name' ] ],

    'from_ethiopian' : [
'calendars', 'converts a date in the Ethiopian calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Ethiopiam calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '2012 3 9 from_ethiopian' ) + '''
''' + makeCommandExample( '2011 1 18 from_ethiopian' ),
[ 'to_ethiopian', 'to_ethiopian_name' ] ],

    'from_french_republican' : [
'calendars', 'converts a date in the French Republican calendar to the equivalent Gregorian date',
'''
This operator converts a date in the French Republican calendar to the
equivalent Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '228 04 15 from_french_republican' ) + '''
''' + makeCommandExample( '8 8 14 from_french_republican' ),
[ 'to_french_republican', 'to_french_republican_name' ] ],

    'from_hebrew' : [
'calendars', 'converts a date in the Hebrew calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Hebrew calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '5780 7 15 from_hebrew' ) + '''
''' + makeCommandExample( '5000 1 1 from_hebrew' ),
[ 'to_hebrew', 'to_hebrew_name' ] ],

    'from_indian_civil' : [
'calendars', 'converts a date in the Indian civil calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Indian Civil calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '1942 4 30 from_indian_civil' ) + '''
''' + makeCommandExample( '1912 7 2 from_indian_civil' ),
[ 'to_indian_civil', 'to_indian_civil_name' ] ],

    'from_islamic' : [
'calendars', 'converts a date in the Islamic calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Islamic calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '1439 2 7 from_islamic' ) + '''
''' + makeCommandExample( '1 1 1 from_islamic' ),
[ 'to_islamic', 'to_islamic_name' ] ],

    'from_julian' : [
'calendars', 'converts a date to the equivalent date in the Julian calendar',
'''
This operator converts a date in the Julian calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '2020 1 1 from_julian' ) + '''
''' + makeCommandExample( '1912 12 30 from_julian' ),
[ 'to_julian', 'to_julian_day' ] ],

    'from_mayan' : [
'calendars', 'converts a date in the Mayan long count calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Mayan long count calendar to the equivalent
Gregorian date.

From https://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar:

The Mesoamerican Long Count calendar is a non-repeating, vigesimal (base 20) and
octodecimal (base 18) calendar used by several pre-Columbian Mesoamerican
cultures, most notably the Maya.  For this reason, it is often known as the Maya
(or Mayan) Long Count calendar.  Using a modified vigesimal tally, the Long
Count calendar identifies a day by counting the number of days passed since a
mythical creation date that corresponds to August 11, 3114 BCE in the Proleptic
Gregorian calendar.  The Long Count calendar was widely used on monuments.

Rather than using a base 10 scheme, the Long Count days were tallied in a
modified base-20 scheme.  In a pure base 20 scheme, 0.0.0.1.5 is equal to 25 and
0.0.0.2.0 is equal to 40.  The Long Count is not pure base-20, however, since
the second digit from the right (and only that digit) rolls over to zero when it
reaches 18.  Thus 0.0.1.0.0 does not represent 400 days, but rather only 360
days and 0.0.0.17.19 represents 359 days.
''',
'''
''' + makeCommandExample( '12 19 17 19 19 from_mayan' ) + '''
''' + makeCommandExample( '13 1 1 1 1 from_mayan' ) + '''
''' + makeCommandExample( '12 1 1 1 1 from_mayan' ),
[ 'to_mayan' ] ],

    'from_persian' : [
'calendars', 'converts a date in the Persian calendar to the equivalent Gregorian date',
'''
This operator converts a date in the Persian calendar to the equivalent
Gregorian date.  The 3 arguments required are year, month, and day.
''',
'''
''' + makeCommandExample( '1399 4 31 from_persian' ) + '''
''' + makeCommandExample( '1399 1 1 from_persian' ),
[ 'to_persian', 'to_persian_name' ] ],

    'good_friday' : [
'calendars', 'calculates the date of Good Friday for the year n',
'''
This operator calculates the date of Good Friday for the year specified.

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
This operator returns the date of Independence Day (US) for the year specified.

Independence Day celebrates the signing of the Declaration of Independence on
July 4, 1776, which signified the intention of the British colonies to separate
from England and become their own country.
''',
'''
''' + makeCommandExample( '2017 independence_day' ),
[ 'veterans_day', 'memorial_day', 'columbus_day' ] ],

    'labor_day' : [
'calendars', 'calculates the date of Labor Day (US) for the year n',
'''
This operator calculates the date of Labor Day (US) for the year specified.

In the U.S., Labor Day falls on the first Monday of September.
''',
'''
''' + makeCommandExample( '2016 labor_day' ) + '''
''' + makeCommandExample( '2016 labor_day 2015 memorial_day -' ),
[ 'memorial_day', 'election_day', 'presidents_day' ] ],

    'martin_luther_king_day' : [
'calendars', 'returns the date of Martin Luther King Day (US) for the year n',
'''
This operator returns the date of Martin Luther King Day (US) for the year
specified.

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
This operator calculates the date of Memorial Day (US) for the year specified.

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
This operator calculates the date of Mother\'s Day (US) for the year specified.

From https://en.wikipedia.org/wiki/Mother%27s_Day:

Mother's Day is a celebration honoring the mother of the family, as well as
motherhood, maternal bonds, and the influence of mothers in society.  It is
celebrated on various days in many parts of the world, most commonly in the
months of March or May.  It complements similar celebrations honoring family
members, such as Father's Day, Siblings Day, and Grandparents Day.

The modern Mother's Day began in the United States, at the initiative of Anna
Jarvis in the early 20th century.  It is not directly related to the many
traditional celebrations of mothers and motherhood that have existed throughout
the world over thousands of years, such as the Greek cult to Cybele, the mother
god Rhea, the Roman festival of Hilaria, or the Christian Laetare Sunday
celebration (associated with the image of Mother Church).  However, in some
countries, Mother's Day is still synonymous with these older traditions.

In the U.S., which is the definition rpn uses, Mother's Day is celebrated on the
second Sunday in May.
''',
'''
''' + makeCommandExample( 'today mothers_day' ) + '''
''' + makeCommandExample( '1993 mothers_day' ),
[ 'fathers_day', 'thanksgiving' ] ],

    'new_years_day' : [
'calendars', 'returns the date of New Year\'s Day (US) for the year specified',
'''
This operator returns the date of New Year\'s Day (US) for the year specified.

From https://en.wikipedia.org/wiki/New_Year%27s_Day:

New Year's Day, also simply called New Year, is observed on 1 January, the first
day of the year on the modern Gregorian calendar as well as the Julian calendar.

In pre-Christian Rome under the Julian calendar, the day was dedicated to Janus,
god of gateways and beginnings, for whom January is also named.  As a date in
the Gregorian calendar of Christendom, New Year's Day liturgically marked the
Feast of the Naming and Circumcision of Jesus, which is still observed as such
in the Anglican Church and Lutheran Church.  The Roman Catholic Church
celebrates on this day the Solemnity of Mary, Mother of God.

In present day, with most countries now using the Gregorian calendar as their de
facto calendar, New Year's Day is among the most celebrated public holidays in
the world, often observed with fireworks at the stroke of midnight as the new
year starts in each time zone.  Other global New Year's Day traditions include
making New Year's resolutions and calling one's friends and family.
''',
'''
''' + makeCommandExample( '2020 new_years_day' ) + '''
''' + makeCommandExample( '2021 new_years_day' ),
[ 'labor_day', 'election_day', 'presidents_day' ] ],

    'nth_weekday' : [
'calendars', 'finds the nth day (1 = Monday, etc.) of the month',
'''
This operator returns the date of the c-th weekday (d) of month b in year a, as
follows:

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
This operator returns the date of the b-th weekday (c) in year a, as follows:

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
This operator returns the date of Pentecost Sunday for the year specified.

From https://en.wikipedia.org/wiki/Pentecost:

The Christian holiday of Pentecost, which is celebrated the 50th day (the
seventh Sunday) after Easter Sunday, commemorates the descent of the Holy Spirit
upon the Apostles and other followers of Jesus Christ while they were in
Jerusalem celebrating the Feast of Weeks, as described in the Acts of the
Apostles (Acts 2:1–31).
''',
'''
''' + makeCommandExample( '2019 pentecost' ) + '''
''' + makeCommandExample( '2020 pentecost' ),
[ 'easter', 'ascension' ] ],

    'presidents_day' : [
'calendars', 'calculates the date of Presidents Day (US) for the year specified',
'''
This operator calculates the date of Presidents Day (US) for the year specified.

From https://en.wikipedia.org/wiki/Washington%27s_Birthday:

Washington's Birthday is a federal holiday in the United States celebrated on
the third Monday of February in honor of George Washington, the first President
of the United States, who was born on February 22, 1732.  The Uniform Monday
Holiday Act of 1971 moved this holiday to the third Monday, which can fall from
February 15 to 21, inclusive.

Colloquially, the day is also now widely known as Presidents' Day (though the
placement of the apostrophe, if any, varies) and is often an occasion to
remember all the presidents.

The day is a state holiday in most states, with official names including
Washington's Birthday, Presidents' Day, President's Day, and Washington's and
Lincoln's Birthday.  The various states use 14 different names.  Depending upon
the specific law, the state holiday may officially celebrate Washington alone,
Washington and Lincoln, or some other combination of U.S. presidents (such as
Washington and Thomas Jefferson, who was born in April).
''',
'''
''' + makeCommandExample( '2022 presidents_day' ) + '''
''' + makeCommandExample( '2023 presidents_day' ),
[ 'labor_day', 'memorial_day', 'election_day' ] ],

    'thanksgiving' : [
'calendars', 'calculates the date of Thanksgiving (US) for the year specified',
'''
This operator calculates the date of Thanksgiving (US) for the year specified.

From https://en.wikipedia.org/wiki/Thanksgiving:

Thanksgiving Day is a national holiday celebrated on various dates in the United
States, Canada, some of the Caribbean islands, and Liberia.  It began as a day
of giving thanks and sacrifice for the blessing of the harvest and of the
preceding year.  Similarly named festival holidays occur in Germany and Japan.
Thanksgiving is celebrated on the second Monday of October in Canada and on the
fourth Thursday of November in the United States and Brazil, and around the
same part of the year in other places.  Although Thanksgiving has historical
roots in religious and cultural traditions, it has long been celebrated as a
secular holiday as well.
''',
'''
''' + makeCommandExample( '2017 thanksgiving' ) + '''
''' + makeCommandExample( '2019 thanksgiving' ),
[ 'christmas', 'easter', 'mothers_day', 'fathers_day' ] ],

    'to_bahai' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i calendar',
'''
This operator converts a date to the equivalent date in the Baha\'i calendar.
''',
'''
''' + makeCommandExample( '2017-01-11 to_bahai' ) + '''
''' + makeCommandExample( '2018-03-21 to_bahai' ),
[ 'from_bahai', 'to_bahai_name' ] ],

    'to_bahai_name' : [
'calendars', 'converts a date to the equivalent date in the Baha\'i calendar with the weekday and month names',
'''
This operator converts a date to the equivalent date in the Baha\'i calendar
with the weekday and month names.

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
This operator converts a date to the equivalent date in the Ethiopian calendar.
''',
'''
''' + makeCommandExample( '2018-12-21 to_ethiopian' ) + '''
''' + makeCommandExample( '2019-04-19 to_ethiopian' ),
[ 'from_ethiopian', 'to_ethiopian_name' ] ],

    'to_ethiopian_name' : [
'calendars', 'converts a date to the equivalent date in the Ethiopian calendar with the day and month names',
'''
This operator converts a date to the equivalent date in the Ethiopian calendar
with the day and month names.  The Ethiopian calendar names every day of the
month after a saint.

Since rpnChilada is limited to ASCII text, ASCII versions of the Ethiopian
names are used.
''',
'''
''' + makeCommandExample( '2018-09-15 to_ethiopian_name' ) + '''
''' + makeCommandExample( '2019-05-07 to_ethiopian_name' ),
[ 'from_ethiopian', 'to_ethiopian' ] ],

    'to_french_republican' : [
'calendars', 'converts a date to the equivalent date in the French Republican calendar',
'''
This operator converts a date to the equivalent date in the French Republican
calendar.
''',
'''
''' + makeCommandExample( '1799-07-14 to_french_republican' ) + '''
''' + makeCommandExample( '2020-07-20 to_french_republican' ),
[ 'from_french_republican', 'to_french_republican_name' ] ],

    'to_french_republican_name' : [
'calendars', 'converts a date to the equivalent date in the French Republican calendar with the weekday and month names',
'''
This operator converts a date to the equivalent date in the French Republican
calendar with day and month names.

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
This operator converts a date to the equivalent date in the Hebrew calendar.

Since rpnChilada is limited to ASCII text, ASCII versions of the Hebrew
names are used.

Technically, days in the Hebrew calendar start at sundown, not midnight.
rpnChilada does not that into consideration, because it would require a
geographic location as input.
''',
'''
''' + makeCommandExample( '2018-04-30 to_hebrew' ) + '''
''' + makeCommandExample( '2019-06-09 to_hebrew' ),
[ 'from_hebrew', 'to_hebrew_name' ] ],

    'to_hebrew_name' : [
'calendars', 'converts a date to the equivalent date in the Hebrew calendar with the weekday and month names',
'''
This operator converts a date to the equivalent date in the Hebrew calendar with
day and month names.

Since rpnChilada is limited to ASCII text, ASCII versions of the Hebrew
names are used.

Technically, days in the Hebrew calendar start at sundown, not midnight.
rpnChilada does not that into consideration, because it would require a
geographic location as input.
''',
'''
''' + makeCommandExample( '2018-04-30 to_hebrew_name' ) + '''
''' + makeCommandExample( '2019-06-09 to_hebrew_name' ),
[ 'from_hebrew', 'to_hebrew' ] ],

    'to_indian_civil' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar',
'''
This operator converts a date to the equivalent date in the Indian Civil
calendar.
''',
'''
''' + makeCommandExample( '2019-02-28 to_indian_civil' ) + '''
''' + makeCommandExample( '2019-09-01 to_indian_civil' ),
[ 'from_indian_civil', 'to_indian_civil_name' ] ],

    'to_indian_civil_name' : [
'calendars', 'converts a date to the equivalent date in the Indian Civil calendar with the weekday and month names',
'''
This operator converts a date to the equivalent date in the Indian Civil
calendar with day and month names.

Since rpnChilada is limited to ASCII text, ASCII versions of the Islamic
names are used.
''',
'''
''' + makeCommandExample( '2019-02-28 to_indian_civil_name' ) + '''
''' + makeCommandExample( '2019-09-01 to_indian_civil_name' ),
[ 'from_indian_civil', 'to_indian_civil' ] ],

    'to_islamic' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar',
'''
This operator converts a date to the equivalent date in the Islamic calendar.
''',
'''
''' + makeCommandExample( '2019-01-11 to_islamic' ) + '''
''' + makeCommandExample( '2019-12-01 to_islamic' ),
[ 'from_islamic', 'to_islamic_name' ] ],

    'to_islamic_name' : [
'calendars', 'converts a date to the equivalent date in the Islamic calendar with day and month names',
'''
This operator converts a date to the equivalent date in the Islamic calendar
with day and month names.

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
The ISO day format is represented here by a three-valued list which contains the
year, the number of the week, and the weekday (from 1-7, 1 = Monday).
''',
'''
''' + makeCommandExample( '2020-01-11 to_iso' ) + '''
''' + makeCommandExample( '2020-07-21 to_iso' ),
[ 'to_iso', 'to_iso_name' ] ],

    'to_iso_name' : [
'calendars', 'converts a date to the formatted version of the equivalent ISO date',
'''
THis operator converts a date to the formatted version of the equivalent ISO
date.  The format consists of a "yyyy-Www-d", where "yyyy" is the year, "ww" is
the one- or two-digit date number, and d is the weekday. (from 1-7, 1 = Monday).

TODO:  This operator returns a string value that rpnChilada cannot currently
parse.
''',
'''
''' + makeCommandExample( '2020-01-11 to_iso_name' ) + '''
''' + makeCommandExample( '2020-07-21 to_iso_name' ),
[ 'to_iso' ] ],

    'to_julian' : [
'calendars', 'converts a date to the equivalent Julian date',
'''

''',
'''
''' + makeCommandExample( '1987-06-13 to_julian' ) + '''
''' + makeCommandExample( '1991-10-30 to_julian' ),
[ 'from_julian', 'to_julian_day' ] ],

    'to_julian_day' : [
'calendars', 'returns the Julian Day Number for a time value',
'''
This operator converts a date to the equivalent Julian Day Number.

From https://en.wikipedia.org/wiki/Julian_day:

Julian day is the continuous count of days since the beginning of the Julian
Period and is used primarily by astronomers, and in software for easily
calculating elapsed days between two events (e.g. food production date and sell
by date).

The Julian Day Number (JDN) is the integer assigned to a whole solar day in the
Julian day count starting from noon Universal time, with Julian day number 0
assigned to the day starting at noon on Monday, January 1, 4713 BC, proleptic
Julian calendar (November 24, 4714 BC, in the proleptic Gregorian calendar).
For example, the Julian day number for the day starting at 12:00 UT (noon) on
January 1, 2000, was 2451545.

The Julian date (JD) of any instant is the Julian day number plus the fraction
of a day since the preceding noon in Universal Time.  Julian dates are expressed
as a Julian day number with a decimal fraction added.  For example, the Julian
Date for 00:30:00.0 UT January 1, 2013, is 2456293.520833.
''',
'''
''' + makeCommandExample( '"1987-06-13 11:13:00" to_julian_day' ) + '''
''' + makeCommandExample( '"1991-10-30 19:30:00" to_julian_day' ),
[ 'from_julian', 'to_julian' ] ],

    'to_lilian_day' : [
'calendars', 'calculates the Lilian date for a date-time value',
'''
The operator calculates the Lilian date for date-time value n.

From https://en.wikipedia.org/wiki/Lilian_date:

A Lilian date is the number of days since the beginning of the Gregorian
Calendar on October 15, 1582, regarded as Lilian date 1.  It was invented by
Bruce G. Ohms of IBM in 1986 and is named for Aloysius Lilius, who devised the
Gregorian Calendar.  Lilian dates can be used to calculate the number of days
between any two dates occurring since the beginning of the Gregorian calendar.
It is currently used by date conversion routines that are part of IBM Language
Environment (LE) software.

The Lilian date is only a date format:  it is not tied to any particular time
standard.  Another, better known, date notation that is used for similar
purposes is the Julian date, which is tied to Universal time (or some other
closely related time scale, such as International Atomic Time).  The Julian date
always begins at noon, Universal time, and a decimal fraction may be used to
represent the time of day.  In contrast, Ohms did not make any mention of time
zones or time of day in his paper.
''',
'''
''' + makeCommandExample( '1978-08-23 to_lilian_day' ) + '''
''' + makeCommandExample( '1968-05-03 to_lilian_day' ),
[ 'to_julian_day' ] ],

    'to_mayan' : [
'calendars', 'converts a date to the equivalent date in the Mayan long count calendar',
'''
This operator converts a date to the equivalent date in the Mayan long count
calendar.
''',
'''
''' + makeCommandExample( '2012-12-20 to_mayan' ) + '''
''' + makeCommandExample( '2012-12-21 to_mayan' ),
[ 'from_mayan' ] ],

    'to_ordinal_date' : [
'calendars', 'calculates date-time n in the Ordinal Date format',
'''
This operator calculates date-time n in the Ordinal Date format.  The Ordinal
Date format is simply the year and a dash followed by the ordinal date, i.e.,
the number of days since January 1st inclusive.

This output is not a format that rpnChilada can parse.
''',
'''
''' + makeCommandExample( '2018-12-13 to_ordinal_date' ) + '''
''' + makeCommandExample( '2019-01-04 to_ordinal_date' ),
[ 'to_iso', 'to_julian_day', 'to_lilian_day' ] ],

    'to_persian' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar',
'''
This operator converts a date to the equivalent date in the Persian calendar.
''',
'''
''' + makeCommandExample( '2019-03-15 to_persian' ) + '''
''' + makeCommandExample( '2019-08-17 to_persian' ),
[ 'from_persian', 'to_persian_name' ] ],

    'to_persian_name' : [
'calendars', 'converts a date to the equivalent date in the Persian calendar with the weekday and month names',
'''
This operator converts a date to the equivalent date in the Persian calendar
with the weekday and month names.

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
This operator returns the date of Veterans Day as celebrated in the U.S. for the
year specified.

From https://en.wikipedia.org/wiki/Veterans_Day:

Veterans Day (originally known as Armistice Day) is a federal holiday in the
United States observed annually on November 11, for honoring military veterans,
that is, persons who have served in the United States Armed Forces (and were
discharged under conditions other than dishonorable).
''',
'''
''' + makeCommandExample( '2017 veterans_day' ),
[ 'independence_day', 'memorial_day', 'columbus_day' ] ],

    'weekday' : [
'calendars', 'calculates the day of the week of date-time n',
'''
This operator calculates the day of the week of a specified date-time.

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
'calendars', 'calculates the name of the day of the week of date-time n',
'''
This operator calculates the name of the day of the week of a specified
date-time.

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
'calendars', 'prints a month calendar for date n',
'''
This operator prints a month calendar for the date value.

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
This operator returns the atomic number of element n.

Elements can be referred to by atomic symbol or name.
''',
'''
''' + makeCommandExample( 'He atomic_number -s1' ) + '''
''' + makeCommandExample( 'Beryllium atomic_number -s1' ),
[ 'atomic_symbol', 'atomic_weight', 'element_name' ] ],

    'atomic_symbol' : [
'chemistry', 'returns the atomic symbol of element n',
'''
This operator returns the atomic symbol of element n.

Elements can be referred to by atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range atomic_symbol -s1' ),
[ 'atomic_number', 'element_name', 'atomic_weight' ] ],

    'atomic_weight' : [
'chemistry', 'returns the atomic weight of element n',
'''
This operator returns the atomic weight of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range atomic_weight -s1' ),
[ 'atomic_number', 'element_name', 'atomic_symbol', 'molar_mass' ] ],

    'element_block' : [
'chemistry', 'returns the block of element n',
'''
This operator returns the block designation of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_block -s1' ),
[ 'element_group', 'element_description', 'element_period' ] ],

    'element_boiling_point' : [
'chemistry', 'returns the boiling point of element n',
'''
This operator returns the boiling point of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_boiling_point -s1' ),
[ 'element_melting_point', 'element_density' ] ],

    'element_density' : [
'chemistry', 'returns the density of element n for STP',
'''
This operator returns the density of element n.

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
This operator returns the description of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_description -s1' ),
[ 'element_block', 'element_group', 'element_period', 'element_occurrence' ] ],

    'element_group' : [
'chemistry', 'returns the group of element n',
'''
This operator returns the group designation of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_group -s1' ),
[ 'element_block', 'element_description', 'element_period' ] ],

    'element_melting_point' : [
'chemistry', 'returns the melting point of element n',
'''
This operator returns the melting point of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_melting_point -s1' ),
[ 'element_boiling_point', 'element_density' ] ],

    'element_name' : [
'chemistry', 'returns the name of element n',
'''
This operator returns the full name of element n.

Elements can be referred to by atomic symbol or atomic number.
''',
'''
''' + makeCommandExample( '1 10 range atomic_symbol element_name -s1' ),
[ 'element_description', 'atomic_symbol' ] ],

    'element_occurrence' : [
'chemistry', 'returns the occurrence of element n',
'''
This operator returns the occurrence of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_occurrence -s1' ),
[ 'element_description', 'element_state' ] ],

    'element_period' : [
'chemistry', 'returns the period of element n',
'''
This operator returns the period designation of element n.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_period -s1' ),
[ 'element_block', 'element_group' ] ],

    'element_state' : [
'chemistry', 'returns the state (at STP) of element n',
'''
This element returns the state of matter of element n.  This state of matter
reported for under standard temperature and pressure conditions.

Elements can be referred to by atomic symbol, atomic number or name.
''',
'''
''' + makeCommandExample( '1 10 range element_name element_state -s1' ),
[ 'element_description', 'element_occurrence' ] ],

    'molar_mass' : [
'chemistry', 'returns the molar mass of molecule n',
'''
This operator computes the molar mass of molecule n.

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
This operator calculates the number of arrangements of n or fewer objects out of
n objects.
''',
'''
''' + makeCommandExample( '1 10 range arrangements' ) + '''
''' + makeCommandExample( '5 arrangements' ) + '''
''' + makeCommandExample( '5 0 5 range permutations sum' ),
[ 'compositions', 'partitions' ] ],

    'binomial' : [
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
The operator computers the binomial coefficient for n and k, which is:

         n!
    ------------
    k!( n - k )!

The binomial coefficient gives the number of ways that k items can be chosen
from a set of n items.  More generally, the binomial coefficient is a
well-defined function of arbitrary real or complex n and k, via the gamma
function.
''',
'''
''' + makeCommandExample( '5 6 binomial' ) + '''
Generating Pascal's triangle:
''' + makeCommandExample( '0 5 range lambda x 0 x range binomial eval -s1' ) + '''
''' + makeCommandExample( '10 20 ** 10 10 ** binomial' ),
[ 'multinomial' ] ],

    'combinations' : [
'combinatorics', 'calculates the number of combinations of k out of n objects',
'''
This operator calculates the number of combinations of k out of n objects.
''',
'''
''' + makeCommandExample( '6 3 combinations' ) + '''
''' + makeCommandExample( '10 8 combinations' ) + '''
''' + makeCommandExample( '21 15 combinations' ),
[ 'permutations' ] ],

    'compositions' : [
'combinatorics', 'returns a list containing all distinct ordered k-tuples of positive integers whose elements sum to n',
'''
This operator returns a list containing all distinct ordered k-tuples of
positive integers whose elements sum to n.

This is referred to as the compositions of n.
''',
'''
''' + makeCommandExample( '5 2 compositions' ) + '''
''' + makeCommandExample( '5 3 compositions' ) + '''
''' + makeCommandExample( '5 4 compositions' ),
[ 'partitions', 'arrangements' ] ],

    'debruijn_sequence' : [
'combinatorics', 'generates a deBruijn sequence of n symbols and word-size k',
'''
This operator generates a deBruijn sequence of n symbols and word-size k.

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
[ 'permutations', 'nth_thue_morse' ] ],

    'count_frobenius' : [
'combinatorics', 'calculates the number of combinations of items on n that add up to k',
'''
This operator calculates the number of combinations of items on n that add up to
.

While 'frobenius' returns the lowest number that is not a linear combination of
the values in n, the 'count_frobenius' operators returns the number of
different ways that linear combinations of the values in n add up to k.
''',
'''
''' + makeCommandExample( '[ 6 9 20 ] 42 count_frobenius' ) + '''
''' + makeCommandExample( '[ 1 5 10 25 50 100 ] 100 count_frobenius' ),
[ 'frobenius', 'solve_frobenius' ] ],

    'lah_number' : [
'combinatorics', 'calculates the Lah number for n and k',
'''
This operator calculates the Lah number for n and k.

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
This operator calculates the nth k-factorial.

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
This operator calculates the multinomial coefficient of list n.

From https://en.wikipedia.org/wiki/Multinomial_theorem:

For any positive integer m and any nonnegative integer n, the multinomial
formula tells us how a sum with m terms expands when raised to an arbitrary
power n:

        n!
-------------------
k1! k2! k3! ... km!

is a multinomial coefficient.  The sum is taken over all combinations of
nonnegative integer indices k1 through km such that the sum of all ki is n.
That is, for each term in the expansion, the exponents of the xi must add up to
n.  Also, as with the binomial theorem, quantities of the form x^0 that appear
are taken to equal 1 (even when x equals zero).

In the case m = 2, this statement reduces to that of the binomial theorem.

The multinomial coefficients have a direct combinatorial interpretation, as the
number of ways of depositing n distinct objects into m distinct bins, with k1
objects in the first bin, k2 objects in the second bin, and so on.
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] multinomial' ) + '''
''' + makeCommandExample( '[ 6 8 11 ] multinomial' ),
[ 'binomial' ] ],

    'narayana_number' : [
'combinatorics', 'calculates the Narayana number for n and k',
'''
This operator calculates the Narayana number for n and k.

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
This operator calculates the nth Apery number.

From https://mathworld.wolfram.com/AperyNumber.html:

Apery's numbers are defined by
        n
       ---
A_n =  \\
       /     bin( n, k ) ^ 2 * bin( n + k, k ) ^ 2
       ---
       k=0

where bin( n, k ) is the binomial coefficient.

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
[ 'nth_bell_polynomial', 'partitions' ] ],


    'nth_bell_polynomial' : [
'combinatorics', 'evaluates the nth Bell polynomial with k',
'''
This operator evaluates the nth Bell polynomial for k.

From https://en.wikipedia.org/wiki/Bell_polynomials:

In combinatorial mathematics, the Bell polynomials, named in honor of Eric
Temple Bell, are used in the study of set partitions.  They are related to
Stirling and Bell numbers.  They also occur in many applications, such as in the
Faa di Bruno's formula.

From mpmath's documentation:

For n, a nonnegative integer, bell(n,x) evaluates the Bell polynomial Bn( x ),
the first few of which are:

B0( x ) = 1
B1( x ) = x
B2( x ) = x^2 + x
B3( x ) = x^3 + 3x^2 + x

or bell() is called with only one argument, it gives the n-th Bell number Bn,
which is the number of partitions of a set with n  elements.  [ Note:
rpnChilada exposes this functionality with the 'nth_bell' operator. ]

By setting the precision to at least log10( Bn ) digits, bell( ) provides fast
calculation of exact Bell numbers.
''',
'''
''' + makeCommandExample( '0 2.5 nth_bell_polynomial' ) + '''
''' + makeCommandExample( '1 2.5 nth_bell_polynomial' ) + '''
''' + makeCommandExample( '2 2.5 nth_bell_polynomial' ),
[ 'nth_bell' ] ],

    'nth_bernoulli' : [
'combinatorics', 'calculates the nth Bernoulli number',
'''
This operator calculates the nth Bernoulli number.

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
'combinatorics', 'calculates the nth Catalan number',
'''
This operator calculates the nth Catalan number.

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
This operator calculates the nth Central Delannoy number.

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
This operator calculates the nth Menage number for n and k.

From https://en.wikipedia.org/wiki/M%C3%A9nage_problem:

''',
'''
''' + makeCommandExample( '1 10 range nth_menage' ),
[ 'combinations', 'permutations' ] ],

    'nth_motzkin' : [
'combinatorics', 'calculates the nth Motzkin number',
'''
This operator calculates the nth Motzkin number.

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
This operator calculates the nth Pell number.

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
This operator calculates the nth Schroeder number.

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
This operator calculates the nth Schroeder-Hipparchus number.

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
This operator calculates the nth Sylvester number.

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
This operator returns the partition number for n.

A partition of a positive integer n, also called an integer partition, is a way
of writing n as a sum of positive integers.  Two sums that differ only in the
order of their summands are considered the same partition.

For example, 4 can be partitioned in five distinct ways:
    4
    3 + 1
    2 + 2
    2 + 1 + 1
    1 + 1 + 1 + 1

Ref:  https://en.wikipedia.org/wiki/Partition_%28number_theory%29
''',
'''
''' + makeCommandExample( '4 partitions' ),
[ 'compositions', 'arrangements' ] ],

    'permutations' : [
'combinatorics', 'calculates the number of permutations of k out of n objects',
'''
This operator calculates the number of permutations of k out of n objects.

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
This operator calculates the Stirling number of the first kind for n and k.

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
'combinatorics', 'calculates the Stirling number of the second kind for n and k',
'''
This operator calculates the Stirling number of the second kind for n and k.

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
This operator calculates complex argument (phase) of n.

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
This operator calculates complex conjugate of n.

The complex conjugate is simply the nunmber with the same real part and an
imaginary part with the same magnitude but opposite sign.
''',
'''
''' + makeCommandExample( '3 3j + conj' ),
[ 'argument', 'real', 'imaginary', 'i' ] ],

    'imaginary' : [
'complex_math', 'returns the imaginary part of n',
'''
This operator returns the imaginary part of complex number n.

Complex numbers have a real component and an imaginary component.  Of course,
either one of these components might be zero.
''',
'''
''' + makeCommandExample( '7 imaginary' ) + '''
''' + makeCommandExample( '7j imaginary' ) + '''
''' + makeCommandExample( '3 4j + imaginary' ),
[ 'argument', 'conjugate', 'real', 'i' ] ],

    'real' : [
'complex_math', 'returns the real part of n',
'''
This operator returns the real component of a complex number n.

Complex numbers have a real component and an imaginary component.  Of course,
either one of these components might be zero.
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

        1     1     1     1     1
b(2) = --- - --- + --- - --- + --- -  ...
       1^2   3^2   5^2   7^2   9^2

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
    \\     --
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
"proof" that NEdd = 136 x 2^256, or about 1.57 x 1.0e79.  Some estimates of NEdd
point to a value of about 1.0e80.  These estimates assume that all matter can be
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
'constants', 'evaluates to infinity, used to describe ranges for ranged_sum, etc.',
'''
This operator represents infinity, and is meant to be used with 'ranged_sum',
'ranged_product', and 'limit' when describing infinite ranges.
''',
'''
''' + makeCommandExample( '1 inf lambda x fib 1/x ranged_sum' ) + '''
''' + makeCommandExample( '1 inf lambda x lucas 1/x ranged_sum' ) + '''
''' + makeCommandExample( 'phi' ) + '''
''' + makeCommandExample( 'infinity lambda x 1 + fib x fib / limit' ),
[ 'negative_infinity' ] ],

    'itoi' : [
'constants', 'returns i to the i power',
'''
This is a constant that returns i to the i power, which is equivalent to e to
the pi/2 * i power.

Thanks to the funkiness of complex math, this value ends up being equal to
approximately 0.2079.
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
'constants', 'evaluates to negative infinity, used to describe ranges for ranged_sum, etc.',
'''
This operator represents negative infinity, and is meant to be used with
'ranged_sum', 'ranged_product', and 'limit' when describing infinite ranges.
''',
'''
''' + makeCommandExample( 'negative_infinity lambda e x ** decreasing_limit' ),
[ 'infinity' ] ],

    'omega_constant' : [
'constants', 'returns the Omega constant',
'''
From https://en.wikipedia.org/wiki/Omega_constant:

The omega constant is a mathematical constant defined as the unique real number
that satisfies the equation

    Omega e^Omega = 1

It is the value of W( 1 ), where W is Lambert's W function.  The name is derived
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
This is a derived constant calculated by dividing the speed of light by the
Planck length.
''',
'''
''' + makeCommandExample( 'planck_acceleration' ),
[ 'planck_force', 'planck_mass' ] ],

    'planck_area' : [
'constants', 'returns the Planck area',
'''
This is a derived constant calculated from squaring the Planck length to get an
area.
''',
'''
''' + makeCommandExample( 'planck_area' ),
[ 'planck_length', 'planck_volume' ] ],

    'planck_charge' : [
'constants', 'returns the Planck charge',
'''
From https://en.wikipedia.org/wiki/Planck_charge:

In physics, the Planck charge, denoted by qP, is one of the base units in the
system of natural units called Planck units.  It is a quantity of electric
charge defined in terms of fundamental physical constants.

The Planck charge is the only base Planck unit that does not depend on the
gravitational constant and is defined as:

          ___________________________
         /
qP =    /  4 * pi * e_0 * h_bar * c
      \\/

where c is the speed of light in a vacuum, ħ_bar is the reduced Planck constant,
and e_0 is the permittivity of free space.
''',
'''
''' + makeCommandExample( 'planck_charge' ),
[ 'planck_current', 'planck_voltage' ] ],

    'planck_current' : [
'constants', 'returns the Planck current',
'''
This is a derived constant calculated by dividing the Planck charge by the
Planck time.
''',
'''
''' + makeCommandExample( 'planck_current' ),
[ 'planck_voltage', 'planck_charge' ] ],

    'planck_density' : [
'constants', 'returns the Planck density',
'''
This is a derived constant calculated from the dividing the Planck mass by the
Planck volume.
''',
'''
''' + makeCommandExample( 'planck_density' ),
[ 'planck_mass', 'planck_volume' ] ],

    'planck_energy' : [
'constants', 'returns the Planck energy',
'''
This is a derived constant calculated from the multiplying the Planck mass by
the speed of light squared.
''',
'''
''' + makeCommandExample( 'planck_energy' ),
[ 'planck_charge', 'planck_power' ] ],

    'planck_energy_density' : [
'constants', 'returns the Planck energy density',
'''
This is a derived constant calculated from the dividing the Planck energy by
the Planck volume.
''',
'''
''' + makeCommandExample( 'planck_energy_density' ),
[ 'planck_volume', 'planck_charge' ] ],

    'planck_force' : [
'constants', 'returns the Planck force',
'''
This is a derived constant calculated from the dividing the Planck energy by
the Planck length.
''',
'''
''' + makeCommandExample( 'planck_force' ),
[ 'planck_mass', 'planck_acceleration' ] ],

    'planck_impedance' : [
'constants', 'returns the Planck impedance',
'''
From http://dictionary.sensagent.com/Planck%20impedance/en-en/:

The Planck impedance is the unit of electrical resistance, denoted by ZP, in the
system of natural units known as Planck units.  The Planck impedance is directly
coupled to the impedance of free space, Z0, and differs in value from Z0 only by
a factor of 4 pi.
''',
'''
''' + makeCommandExample( 'planck_impedance' ),
[ 'planck_voltage', 'planck_charge' ] ],

    'planck_intensity' : [
'constants', 'returns the Planck intensity',
'''
This constant is calculated by dividing the Planck power by the Planck area, to
get a radiosity result.
''',
'''
''' + makeCommandExample( 'planck_intensity' ),
[ 'planck_power', 'planck_area' ] ],

    'planck_length' : [
'constants', 'returns the Planck length',
'''
From https://en.wikipedia.org/wiki/Planck_length:

In physics, the Planck length, denoted lP, is a unit of length that is the
distance light in a perfect vacuum travels in one unit of Planck time.  It is
also the reduced Compton wavelength of a particle with Planck mass.  It is a
base unit in the system of Planck units, developed by physicist Max Planck.  The
Planck length can be defined from three fundamental physical constants:  the
speed of light in a vacuum, the Planck constant, and the gravitational constant.
It is the smallest distance about which current experimentally corroborated
models of physics can make meaningful statements.  At such small distances, the
conventional laws of macro-physics no longer apply, and even relativistic
physics requires special treatment.

It is defined as:
          _______________
         /   h_bar * G
mP =    /    ---------
      \\/        c^3

where c is the speed of light in a vacuum, G is the gravitational constant, and
ħ_bar is the reduced Planck constant.
''',
'''
''' + makeCommandExample( 'planck_length' ),
[ 'planck_area', 'planck_volume' ] ],

    'planck_mass' : [
'constants', 'returns the Planck mass',
'''
From https://en.wikipedia.org/wiki/Planck_mass:

In physics, the Planck mass, denoted by mP, is the unit of mass in the system of
natural units known as Planck units.  It is approximately 21 micrograms, or
roughly the mass of a flea egg.

Unlike some other Planck units, such as Planck length, Planck mass is not a
fundamental lower or upper bound; instead, Planck mass is a unit of mass defined
using only what Max Planck considered fundamental and universal units.  For
comparison, this value is of the order of 10^15 (a quadrillion) times larger
than the highest energy available to particle accelerators as of 2015.

It is defined as:
          _______________
         /   h_bar * c
mP =    /    ---------
      \\/         G

where c is the speed of light in a vacuum, G is the gravitational constant, and
ħ_bar is the reduced Planck constant.
''',
'''
''' + makeCommandExample( 'planck_mass' ) + '''
''' + makeCommandExample( 'planck_mass energy_equivalence GeV convert' ) + '''
''' + makeCommandExample( 'planck_mass daltons convert' ),
[ 'planck_force', 'planck_acceleration' ] ],

    'planck_momentum' : [
'constants', 'returns the Planck momentum',
'''
This is a derived constant calculated from the multiplying the Planck mass by
the speed of light.
''',
'''
''' + makeCommandExample( 'planck_momentum' ),
[ 'planck_mass' ] ],

    'planck_power' : [
'constants', 'returns the Planck power',
'''
This is a derived constant calculated from the dividing the Planck energy by
the Planck time.
''',
'''
''' + makeCommandExample( 'planck_power' ),
[ 'planck_force', 'planck_energy' ] ],

    'planck_temperature' : [
'constants', 'returns the Planck temperature',
'''
From https://en.wikipedia.org/wiki/Planck_units#Planck_temperature:

The Planck temperature of 1 (unity), equal to 1.416785(16) * 1.0e32 K, is
considered a fundamental limit of temperature.  An object with the temperature
of 1.42 * 1.0e32 kelvin (TP) would emit a black body radiation with a peak
wavelength of 1.616 * 1.0e−35 m (Planck length), where each photon and each
individual collision would have the energy to create a Planck particle.  There
are no known physical models able to describe temperatures greater than or equal
to TP.

It is defined as:
          _______________
         /  h_bar * c^5
mP =    /   -----------
      \\/   G * k_sub_b^2

where c is the speed of light in a vacuum, G is the gravitational constant, and
ħ_bar is the reduced Planck constant, and k_sub_b is Boltzmann's constant.
''',
'''
''' + makeCommandExample( 'planck_temperature' ),
[ 'planck_energy', 'planck_intensity' ] ],

    'planck_time' : [
'constants', 'returns Planck time',
'''
From https://en.wikipedia.org/wiki/Planck_units#Planck_time:

A Planck time unit is the time required for light to travel a distance of 1
Planck length in a vacuum, which is a time interval of approximately 5.39 *
1.0e−44 s.  All scientific experiments and human experiences occur over time
scales that are many orders of magnitude longer than the Planck time, making any
events happening at the Planck scale undetectable with current scientific
technology.  As of November 2016, the smallest time interval uncertainty in
direct measurements was on the order of 850 zeptoseconds (8.50 × 1.0e−19
seconds).

It is defined as:
          _______________
         /   h_bar * G
tP =    /    ---------
      \\/        c^5

where c is the speed of light in a vacuum, G is the gravitational constant, and
ħ_bar is the reduced Planck constant.
''',
'''
''' + makeCommandExample( 'planck_time' ),
[ 'planck_length', 'planck_acceleration' ] ],

    'planck_voltage' : [
'constants', 'returns the Planck voltage',
'''
This is a derived constant calculated from the dividing the Planck mass by
the Planck charge.
''',
'''
''' + makeCommandExample( 'planck_voltage' ),
[ 'planck_charge', 'planck_impedance' ] ],

    'planck_volume' : [
'constants', 'returns the Planck volume',
'''
This is a derived constant calculated from cubing the Planck length to get a
volume.
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
[ 'fibonacci', 'ranged_sum' ] ],

    'radiation_constant' : [
'constants', 'returns the Radiation Constant',
'''
The radiation constant, or radiation density constant is by:

4 sigma
-------
   c

where sigma is the Stefan-Boltzmann constant and c is the speed of light.

Ref:  https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant
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
[ 'prevost_constant', 'plastic_constant', 'mills_constant' ] ],

    'silver_ratio' : [
'constants', 'returns the silver ratio, defined to be 1 + sqrt( 2 )',
'''
This operator returns the silver ratio, which is defined to be 1 + sqrt( 2 ).

From https://en.wikipedia.org/wiki/Silver_ratio:

In mathematics, two quantities are in the silver ratio (or silver mean) if the
ratio of the smaller of those two quantities to the larger quantity is the same
as the ratio of the larger quantity to the sum of the smaller quantity and twice
the larger quantity.  This defines the silver ratio as an irrational
mathematical constant, whose value of one plus the square root of 2 is
approximately 2.4142135623.  Its name is an allusion to the golden ratio;
analogously to the way the golden ratio is the limiting ratio of consecutive
Fibonacci numbers, the silver ratio is the limiting ratio of consecutive Pell
numbers.
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
From https://en.wikipedia.org/wiki/Impedance_of_free_space:

The impedance of free space, z_0, is a physical constant relating the magnitudes
of the electric and magnetic fields of electromagnetic radiation travelling
through free  space. That is, z_0 = |E|/|H|, where |E| is the electric field
strength and |H| is the magnetic field strength.  Its presently accepted value
is z_0 = 376.730313668(57) ohms.
''',
'''
''' + makeCommandExample( 'vacuum_impedance' ),
[ 'magnetic_constant', 'electric_constant' ] ],

    'von_klitzing_constant' : [
'constants', 'returns the von Klitzing constant',
'''
The value is derived from h/e^2, where h is Planck's constant and e is the
charge of the electron.

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

c:\\> rpn [ 2 9 4 ] [ 3 4 5 ] pack -r2
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
''' + makeCommandExample( '"1970-01-01 00:00:00" utc set_time_zone to_unix_time' ) + '''
''' + makeCommandExample( '2001-01-01 to_unix_time' ) + '''
''' + makeCommandExample( '2020-08-05 to_unix_time' ) + '''
''' + makeCommandExample( '"2038-01-18 22:14:07" utc set_time_zone to_unix_time' ),
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

    'get_day' : [
'date_time', 'returns the day value of a date-time',
'''
This operator returns the value of the day of the month from date-time n.
''',
'''
''' + makeCommandExample( 'today get_day' ) + '''
''' + makeCommandExample( '1965-03-31 get_day' ),
[ 'get_year', 'get_month' ] ],

    'get_hour' : [
'date_time', 'returns the hour value of a date-time',
'''
This operator returns the value of the hour from date-time n.
''',
'''
''' + makeCommandExample( 'now get_hour' ) + '''
''' + makeCommandExample( '"2020-08-29 13:15:36" get_hour' ),
[ 'get_minute', 'get_second' ] ],

    'to_local_time' : [
'date_time', 'converts a datetime to the local timezone',
'''
This operator converts a datetime to the local timezone.
''',
'''
''' + makeCommandExample( 'now' ) + '''
''' + makeCommandExample( 'now to_utc' ) + '''
''' + makeCommandExample( 'now to_utc to_local_time' ),
[ 'set_time_zone', 'to_utc' ] ],

    'get_minute' : [
'date_time', 'returns the minute value of a date-time',
'''
This operator returns the value of the minute from date-time n.
''',
'''
''' + makeCommandExample( 'now get_minute' ) + '''
''' + makeCommandExample( '"2020-08-29 13:14:53" get_minute' ),
[ 'get_hour', 'get_second' ] ],

    'get_month' : [
'date_time', 'returns the month value of a date-time',
'''
This operator returns the value of the month from date-time n.
''',
'''
''' + makeCommandExample( 'today get_month' ) + '''
''' + makeCommandExample( '1965-03-31 get_month' ),
[ 'get_year', 'get_day' ] ],

    'get_second' : [
'date_time', 'returns the second value of a date-time',
'''
This operator returns the value of the second from date-time n.
''',
'''
''' + makeCommandExample( 'now get_second' ) + '''
''' + makeCommandExample( '"2020-08-29 13:13:18" get_second' ),
[ 'get_minute', 'get_second' ] ],

    'get_year' : [
'date_time', 'returns the year value of a date-time',
'''
This operator returns the value of the year from date-time n.
''',
'''
''' + makeCommandExample( 'today get_year' ) + '''
''' + makeCommandExample( '1965-03-31 get_year' ),
[ 'get_month', 'get_day' ] ],

    'make_datetime' : [
'date_time', 'interprets list argument as a date-time',
'''
This operator interprets list argument n as a date-time.  The list can have 1 to
6 elements that are interpreted as year, month, day, hour, minute, second.
''',
'''
''' + makeCommandExample( '[ 2014 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 ] make_datetime', indent=4 ) + '''
''' + makeCommandExample( '[ 2014 9 2 13 36 28 ] make_datetime', indent=4 ),
[ 'make_julian_time' ] ],

    'make_julian_time' : [
'date_time', 'interprets list n as absolute date-time specified by year, Julian day and optional time of day',
'''
There elements of the list are interpreted as year, day, hour, minute, second.

The day element can include a fraction, which will be converted, but if the
hour, minute and second elements exist, they will override this.
''',
'''
''' + makeCommandExample( '[ 2020 ] make_julian_time', indent=4 ) + '''
''' + makeCommandExample( '[ 2020 235 ] make_julian_time', indent=4 ) + '''
''' + makeCommandExample( '[ 2020 235.37 ] make_julian_time', indent=4 ) + '''
''' + makeCommandExample( '[ 2020 235 8 10 12 ] make_julian_time', indent=4 ),
[ 'make_datetime' ] ],

    'now' : [
'date_time', 'returns the current date-time',
'''
This operator simply returns the current time value for the current timezone.
''',
'''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'now' ),
[ 'today' ] ],

    'set_time_zone' : [
'date_time', 'sets the date-time n to the timezone k',
'''
This operator sets the timezone value of n to timezone k.  k can be the name of
a timezone or a geographic location.  It does not convert the date-time value to
a different time zone, it actually changes the time value.  It is used to
specify a time in a different timezone.

To convert a date-time value to a different time zone, use 'to_time_zone'.
''',
'''
''' + makeCommandExample( 'now' ) + '''
Here, we're taking a time and setting the time zone, meaning the actual time is
changed:

''' + makeCommandExample( 'now "Moscow, Russia" set_time_zone' ) + '''
''' + makeCommandExample( 'now "Moscow, Russia" set_time_zone to_local_time' ) + '''
Here, we're converting to a different time zone, so the time remains the same:

''' + makeCommandExample( 'now "Moscow, Russia" to_time_zone' ) + '''
''' + makeCommandExample( 'now "Moscow, Russia" to_time_zone to_local_time' ),
[ 'to_time_zone', 'to_local_time' ] ],

    'today' : [
'date_time', 'returns the current date',
'''
This operator is a short-cut that returns the current date, with a time value of
00:00:00 (midnight).
''',
'''
''' + makeCommandExample( 'yesterday' ) + '''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'tomorrow' ),
[ 'yesterday', 'tomorrow' ] ],

    'tomorrow' : [
'date_time', 'returns the next date',
'''
This operator is a short-cut that returns the current date plus one day, with a
time value of 00:00:00 (midnight).
''',
'''
''' + makeCommandExample( 'yesterday' ) + '''
''' + makeCommandExample( 'today' ) + '''
''' + makeCommandExample( 'tomorrow' ),
[ 'yesterday', 'today' ] ],

    'to_time_zone' : [
'date_time', 'converts the date-time n to the timezone k',
'''
This operator converts the date-time value of n to the timezone of k.  k can be
the name of a timezone or the name of a geographic location.

To set the timezone for a particular date-time value without converting, use
'set_time_zone'.
''',
'''
''' + makeCommandExample( 'now' ) + '''
Here, we're converting to a different time zone, so the time remains the same:

''' + makeCommandExample( 'now "Johannesburg, South Africa" to_time_zone' ) + '''
''' + makeCommandExample( 'now "Johannesburg, South Africa" to_time_zone to_local_time' ) + '''
Here, we're taking a time and setting the time zone, meaning the actual time is
changed:

''' + makeCommandExample( 'now "Johannesburg, South Africa" set_time_zone' ) + '''
''' + makeCommandExample( 'now "Johannesburg, South Africa" set_time_zone to_local_time' ),
[ 'set_time_zone', 'to_local_time' ] ],

    'to_utc' : [
'date_time', 'returns the datetime converted to UTC time',
'''
This operator returns date-time n converted to the UTC timezone.
''',
'''
''' + makeCommandExample( '"2020-08-29 13:13:18" to_utc' ),
[ 'to_local_time', 'set_time_zone' ] ],

    'yesterday' : [
'date_time', 'returns the previous date',
'''
This operator is a short-cut that returns the current date minus one day, with
a time value of 00:00:00 (midnight).
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

    'decreasing_limit' : [
'functions', 'calculates the limit of function k( x ) as x approaches n from above',
'''
This operator calculates the limit of function k( x ) as x approaches n from
above.

Underneath this operator uses the mpmath limit( ) function, which has all kinds
of smarts to estimate the limits accurately, even for infinite ranges.  However,
rpnChilada does not do a great job of exposing the full functionality of
limit( ).  If the result of a limit is infinite, it returns some weird answers.

'decreasing_limit' is useful when the function is discontinuous.
''',
'''
''' + makeCommandExample( '1 lambda x floor limit' ) + '''
''' + makeCommandExample( '1 lambda x floor decreasing_limit' ),
[ 'limit', 'lambda' ] ],

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
[ 'eval0', 'eval2', 'eval3', 'eval_list', 'filter', 'lambda', 'sequence', 'function' ] ],

    'eval0' : [
'functions', 'evaluates the zero-argument function n',
'''
Although a user-defined function with no arguments is not likely to have many
uses, rpn does support it.
''',
'''
The Silver ratio:

''' + makeCommandExample( 'lambda 1 2 sqrt + eval0' ) + '''
''' + makeCommandExample( 'lambda 10 random_int 1 + eval0' ),
[ 'eval', 'eval2', 'eval3', 'filter', 'lambda', 'sequence', 'function' ] ],

    'eval2' : [
'functions', 'evaluates the function c for the given arguments a and b',
'''
'eval2' is the simplest operator for user-defined functions with 2 variables.
It just plugs in the values a and b into the function c and returns the
result.
''',
'''
''' + makeCommandExample( 'lambda 1 2 sqrt + eval0' ) + '''
''' + makeCommandExample( 'lambda 10 random_int 1 + eval0' ),
[ 'eval', 'eval3', 'filter', 'lambda', 'sequence', 'function' ] ],

    'eval3' : [
'functions', 'evaluates the function d for the given arguments a, b, and c',
'''
'eval3' is the simplest operator for user-defined functions with 3 variables.
It just plugs in the values a, b, and c into the function d and returns the
result.
''',
'''
Solving a quadratic equation the hard way, using the quadratic formula:

''' + makeCommandExample( '1 -4 -21 lambda y neg y sqr 4 x * z * - sqrt - 2 x * / eval3' ) + '''

Of course, rpn has better ways to do this:

''' + makeCommandExample( '1 -4 -21 solve2' ) + '''
''' + makeCommandExample( '[ 1 -4 -21 ] solve' ),
[ 'eval', 'eval3', 'filter', 'lambda', 'sequence', 'function' ] ],

    'eval_list' : [
'functions', 'evaluates the function n for the given list arguments in k',
'''
This operator evaluates the function n for the given list arguments in k.

This means that k should be a list of lists, where each sublist is passed to n.
This is useful for lambda functions that expect a list argument rather than a
single value.
''',
'''
Show the averages of the factors of each of the first 20 numbers:
''' + makeCommandExample( '1 20 range factor lambda x mean eval_list' ),
[ 'eval', 'lambda' ] ],

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
The 'filter' operator uses a one-argument user-defined function to filter out
elements based on whether or not the function returns 0 for each element.

'filter_by_index' works the same way, except the index of the element is passed
to the user-defined function to determine if the element is to be filtered.
''',
'''
''' + makeCommandExample( '1 50 range fib lambda x is_prime filter_by_index' ),
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

    'filter_ratio' : [
'functions', 'returns the ratio of items in list n not filtered out by function k',
'''
The function is applied to each element of the list just like the 'filter'
operator and the ratio of items which remain after filtering is returned.
''',
'''
What is the ratio of 4-digit numbers that have exactly two number 2s?

''' + makeCommandExample( '1000 9999 range lambda x 2 count_digits 2 equals filter_ratio' ),
[ 'filter_by_index', 'lambda', 'unfilter', 'filter_integers', 'unfilter_ratio' ] ],

    'for_each' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list of arguments',
'''
This operator evaluates function n on elements of list n, each of which are
lists themselves, treating each element as a list of arguments passed to
function n.   Therefore, the sublists themselves should each have the same
number of elements as the number of arguments expected by function n.
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 7 9 ] [ 4 3 ] ] lambda x y power for_each' ),
[ 'for_each_list', 'sequence' ] ],

    'for_each_list' : [
'functions', 'evaluates function k on elements of list n, treating each element as a list argument',
'''
This operator evaluates function k on elements of list n, treating each element
as a list argument.  This is necessary when using lambdas that contain an
operator that expects a list argument.
''',
'''
''' + makeCommandExample( '[ [ 2 3 ] [ 4 5 ] [ 6 7 ] [ 8 9 ] ] lambda x -1 element for_each_list' ) + '''
''' + makeCommandExample( '[ [ 1 2 ] [ 3 4 ] [ 5 6 ] [ 7 8 ] ] lambda x sum for_each_list' ),
[ 'for_each', 'sequence' ] ],

    'function': [
'functions', 'creates a user-defined function k named n',
'''
This operator creates a user-defined function k named n.  User functions can be
invoked just like any other operator.  Functions are invoked by name, prefixed
with '@'.
''',
'''
''' + makeCommandExample( 'test_function lambda x 4 ** function' ) + '''
''' + makeCommandExample( '1 10 range @test_function' ) + '''
A two-argument function is created and invoked the same way:
''' + makeCommandExample( 'test_function_2 lambda x 2 ** y 2 ** + function' ) + '''
''' + makeCommandExample( '3 4 @test_function_2' ),
[ 'eval', 'eval2', 'eval3', 'filter', 'lambda', 'sequence' ] ],

    'lambda' : [
'functions', 'begins a function definition',
'''
Allows the user to define a function for use with the 'eval', 'ranged_sum',
'ranged_product', and 'limit' operators, etc.  Basically 'lambda' starts an
expression that becomes a function.

See the 'user_functions' help topic for more details.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( 'inf lambda x 1 + fib x fib / limit' ),
[ 'eval', 'function', 'limit', 'ranged_sum', 'ranged_product' ] ],

    'limit' : [
'functions', 'calculates the limit of function k( x ) as x approaches n',
'''
This operator calculates the limit of function k( x ) as x approaches n.

Underneath this operator uses the mpmath limit( ) function, which has all kinds
of smarts to estimate the limits accurately, even for infinite ranges.
However, rpnChilada does not do a great job of exposing the full functionality
of limit( ).  If the result of a limit is infinite, it returns some weird
answers.
''',
'''
''' + makeCommandExample( 'infinity lambda x 1 + fib x fib / limit' ) + '''
''' + makeCommandExample( 'infinity lambda 2 x 4 * 1 + ** x ! 4 ** * 2 x 1 + * / 2 x * ! 2 ** / limit' ),
[ 'decreasing_limit', 'lambda' ] ],

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

    'ranged_product' : [
'functions', 'calculates the product of function c over the range of a through b',
'''
This operator calculates the product of function c over the range of integers a
through b.

This operator allows for infinite arguments, using 'infinity' and
'negative_infinity'.
''',
'''
Somos\' Quadratic Recurrence Constant
''' + makeCommandExample( '-a20 1 inf lambda x 1 2 x ** / power ranged_product' ) + '''
What percentage of numbers have a factor less than 1000?
''' + makeCommandExample( '1 1 1000 nth_prime lambda 1 x prime 1/x - ranged_product - 100 *' ),
[ 'ranged_sum', 'lambda' ] ],

    'ranged_sum' : [
'functions', 'calculates the sum of function c over the range of integers a through b',
'''
This operator calculates the sum of function c over the range of integers a
through b.

This operator allows for infinite arguments, using 'infinity' and
'negative_infinity'.
''',
'''
Prevost Constant
''' + makeCommandExample( '-a20 1 inf lambda x fib 1/x ranged_sum' ) + '''
1/e
''' + makeCommandExample( '-a20 0 inf lambda x ! 1/x -1 x ** * ranged_sum' ),
[ 'ranged_product', 'lambda' ] ],

    'sequence' : [
'functions', 'evaluates a 1-arg function c with initial argument a, b times',
'''
This operator evaluates a 1-arg function c with initial argument a, b times.

This is similar to 'eval' when passed a list, except each subsequent call to the
function c is given the results of the previous call of function c.
''',
'''
''' + makeCommandExample( '1 10 lambda x 2 * 3 + sequence' ) + '''
The Collatz sequence for 19:
''' + makeCommandExample( '19 21 lambda 3 x * 1 + x 2 / x is_odd if sequence' ),
[ 'eval', 'filter', 'lambda' ] ],

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
[ 'filter', 'unfilter_by_index', 'lambda', 'filter_ratio' ] ],

    'unfilter_by_index' : [
'functions', 'filters a list n using the inverse of function k applied to the list indexes',
'''
The 'unfilter' operator uses a one-argument user-defined function to filter out
elements based on whether or not the function returns 1 for each element.

'unfilter_by_index' works the same way, except the index of the element is passed
to the user-defined function to determine if the element is to be filtered.
''',
'''
''' + makeCommandExample( '1 40 range fib lambda x is_composite unfilter_by_index' ),
[ 'filter_by_index', 'unfilter', 'lambda' ] ],

    'unfilter_ratio' : [
'functions', 'returns the ratio of items in list n filtered out by function k',
'''
The function is applied to each element of the list just like the 'filter'
operator and the ratio of items which are filtered out is returned.
''',
'''
What is the ratio of the first 100,000 numbers that aren't prime?

''' + makeCommandExample( '1 100000 range lambda x is_prime unfilter_ratio' ),
[ 'filter_by_index', 'lambda', 'unfilter', 'filter_integers', 'filter_ratio' ] ],

    'x' : [
'functions', 'used as a variable in user-defined functions',
'''
This operator is used for the definition of user-defined functions with 1,2  or
3 arguments.  The 'x' operator represents the first argument of the function.

See the 'user_functions' help topic for more details.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( '1 inf lambda 1 2 x ** / ranged_sum' ),
[ 'lambda', 'y', 'z' ] ],

    'y' : [
'functions', 'used as a variable in user-defined functions',
'''
This operator is used for the definition of user-defined functions with 2 or 3
arguments.  The 'y' operator represents the second argument of the function.
''',
'''
''' + makeCommandExample( '3 4 lambda x 2 ** y 2 ** + sqrt eval2' ) + '''
''' + makeCommandExample( '[ 1 5 range 1 5 range ] permute_lists lambda x y ** for_each' ),
[ 'lambda', 'x', 'z' ] ],

    'z' : [
'functions', 'used as a variable in user-defined functions',
'''
This operator is used for the definition of user-defined functions with 3
arguments.  The 'z' operator represents the third argument of the function.
''',
'''
''' + makeCommandExample( '3 lambda x 2 * eval' ) + '''
''' + makeCommandExample( '5 lambda x 2 ** 1 - eval' ) + '''
''' + makeCommandExample( '1 inf lambda 1 2 x ** / ranged_sum' ),
[ 'lambda', 'x', 'y' ] ],


    #******************************************************************************
    #
    #  geometry operators
    #
    #******************************************************************************

    'antiprism_area' : [
'geometry', 'calculates the surface area of an n-sided antiprism of edge length k',
'''
This operator calculates the surface area of an n-sided antiprism of edge length
k.

The antiprism is defined to be a regular n-gon on each end with edge length k,
and rotated with respect to each other at an angle of 360/2n degrees.  Both
sides are connected on their vertices by a series of equilateral triangles to
form a solid shape.

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
This operator calculates the volume of an n-sided antiprism of edge length k.

The antiprism is defined to be a regular n-gon on each end with edge length k,
and rotated with respect to each other at an angle of 360/2n degrees.  Both
sides are connected on their vertices by a series of equilateral triangles to
form a solid shape.

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
The operator calculates the surface area of a cone of radius n and height k.

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
The operator calculates the volume of a cone of radius n and height k.

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
This operator returns the surface area of a regular dodecahedron of edge length
n.

The surface area of a dodecahedron is 12 times the area of a regular pentagon
with edge length n.
''',
'''
''' + makeCommandExample( '1 inch dodecahedron_area' ),
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_volume', 'icosahedron_area', 'sphere_area' ] ],

    'dodecahedron_volume' : [
'geometry', 'calculates the volume of a regular dodecahedron of edge length n',
'''
This operator returns the volume of a regular dodecahedron of edge length n.
''',
'''
''' + makeCommandExample( '1 inch dodecahedron_volume' ),
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
This operator returns the surface area of a regular icosahedron of edge length
n.

The surface area of an icosahedron is 20 times the area of an equilateral
triangle with edge length n.
''',
'''
''' + makeCommandExample( '1 inch icosahedron_area' ),
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_area', 'icosahedron_volume', 'sphere_area' ] ],

    'icosahedron_volume' : [
'geometry', 'calculates the volume of a regular icosahedron of edge length n',
'''
This operator returns the volume of a regular icosahedron of edge length n.
''',
'''
''' + makeCommandExample( '1 inch icosahedron_volume' ),
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_area', 'sphere_volume' ] ],

    'k_sphere_area' : [
'geometry', 'calculates the surface area of a k-sphere of size n (radius or volume)',
'''
This operator calculates the surface area of an k-dimensional sphere of size n
(radius or volume).

The surface area of a k-dimensional sphere will be a (k - 1)-dimensional result.

Furthermore, volume is taken to mean k-dimensional volume.
''',
'''
''' + makeCommandExample( '3 feet^5 5 k_sphere_area' ) + '''
''' + makeCommandExample( '19 inches 7 k_sphere_area' ),
[ 'torus_area', 'sphere_volume', 'prism_area', 'k_sphere_area', 'cone_area', 'k_sphere_radius' ] ],

    'k_sphere_radius' : [
'geometry', 'calculates the radius of an n-sphere of size k (surface area or volume)',
'''
This operator calculates the radius of an k-dimensional sphere of size n
(surface area or volume).

The surface area of a k-dimensional sphere is a (k - 1)-dimensional value.

Furthermore, volume is taken to mean k-dimensional volume.
''',
'''
''' + makeCommandExample( '3 feet^5 5 k_sphere_radius' ) + '''
''' + makeCommandExample( '3 feet 5 k_sphere_radius' ) + '''
''' + makeCommandExample( '4 3 / pi * meters^3 3 k_sphere_radius' ),
[ 'k_sphere_volume', 'sphere_radius', 'k_sphere_area' ] ],

    'k_sphere_volume' : [
'geometry', 'calculates the volume of an n-sphere of size k (radius or surface area)',
'''
This operator calculates the radius of an k-dimensional sphere of size n
(radius or surface area).

The surface area of a k-dimensional sphere is a (k - 1)-dimensional value.

Furthermore, volume is taken to mean k-dimensional volume.
''',
'''
''' + makeCommandExample( '3 feet^4 5 k_sphere_volume' ) + '''
''' + makeCommandExample( '6 meters 5 k_sphere_volume' ) + '''
''' + makeCommandExample( '3 4 / meter 3 k_sphere_volume' ),
[ 'torus_volume', 'sphere_volume', 'prism_volume', 'k_sphere_area', 'cone_volume', 'k_sphere_radius' ] ],

    'octahedron_area' : [
'geometry', 'calculates the surface area of a regular octahedron of edge length n',
'''
This operator returns the surface area of a regular octahedron of edge length n.

The surface area of an octahedron is 8 times the area of an equilateral
triangle with edge length n.
''',
'''
''' + makeCommandExample( '1 inch octahedron_area' ),
[ 'antiprism_area', 'prism_area', 'tetrahedron_area', 'octahedron_volume', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'octahedron_volume' : [
'geometry', 'calculates the volume of a regular octahedron of edge length n',
'''
This operator returns the volume of a regular octahedron of edge length n.
''',
'''
''' + makeCommandExample( '1 inch octahedron_volume' ),
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_volume', 'octahedron_area', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'polygon_area' : [
'geometry', 'calculates the area of an regular n-sided polygon with sides of length k',
'''
This operator calculates the area of an regular n-sided polygon with sides of
length k
''',
'''
''' + makeCommandExample( '5 3 feet polygon_area' ) + '''
''' + makeCommandExample( '16 1 inch polygon_area' ) + '''
''' + makeCommandExample( '7 1 mile polygon_area' ),
[ 'triangle_area' ] ],

    'prism_area' : [
'geometry', 'calculates the surface area of an a-sided prism of edge length b, and height c',
'''
This operator calculates the surface area of an a-sided prism of edge length b
and height c.

The prism is defined to be a regular n-gon (a sides) on each end with side
length b, with the two ends set apart at a distance of c.  Both end are
connected on their vertices by a series of rectangles to form a solid shape.

If no unit is specified for the edge length or height, rpn interprets it as a
length in meters.
''',
'''
''' + makeCommandExample( '3 4 inches 1 inch prism_area' ) + '''
''' + makeCommandExample( '7 3 meters 1 meter prism_area' ),
[ 'antiprism_volume', 'prism_area', 'tetrahedron_area', 'octahedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'prism_volume' : [
'geometry', 'calculates the volume of an a-sided prism of edge length b, and height c',
'''
This operator calculates the volume of an a-sided prism of edge length b and
height c.

The prism is defined to be a regular n-gon (a sides) on each end with side
length b, with the two ends set apart at a distance of c.  Both end are
connected on their vertices by a series of rectangles to form a solid shape.

If no unit is specified for the edge length or height, rpn interprets it as a
length in meters.
''',
'''
''' + makeCommandExample( '3 4 inches 1 inch prism_volume' ) + '''
''' + makeCommandExample( '7 3 meters 1 meter prism_volume' ),
[ 'antiprism_volume', 'prism_area', 'tetrahedron_volume', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'sphere_area' : [
'geometry', 'calculates the surface area of a sphere of size n (radius or volume)',
'''
This operator returns the surface area of a sphere given either a radius or a
volume.  If the argument is a length, it will be interpreted as the radius of
the sphere, and if the argument is a volume, it will be interpreted as the
volume of the sphere.
''',
'''
''' + makeCommandExample( '10 inches sphere_area' ) + '''
''' + makeCommandExample( '1 liter sphere_area' ),
[ 'torus_area', 'sphere_volume', 'prism_area', 'k_sphere_area', 'cone_area', 'sphere_radius' ] ],

    'sphere_radius' : [
'geometry', 'calculates the radius of a sphere of size n (surface area or volume)',
'''
This operator returns the radius of a sphere given either a volume or a surface
area.  If the argument is an area, it will be interpreted as the surface area of
the sphere, and if the argument is a volume, it will be interpreted as the
volume of the sphere.
''',
'''
''' + makeCommandExample( '10 square_inches sphere_radius' ) + '''
''' + makeCommandExample( '1 liter sphere_radius' ),
[ 'sphere_volume', 'sphere_radius', 'k_sphere_radius' ] ],

    'sphere_volume' : [
'geometry', 'calculates the volume of a sphere of size n (radius or surface area)',
'''
This operator returns the volume of a sphere given either a radius or a surface
area.  If the argument is a length, it will be interpreted as the radius of the
sphere, and if the argument is an area, it will be interpreted as the surface
area of the sphere.
''',
'''
''' + makeCommandExample( '1 inch sphere_volume' ) + '''
''' + makeCommandExample( '10 square_inches sphere_volume' ),
[ 'torus_volume', 'sphere_area', 'prism_volume', 'k_sphere_volume', 'cone_volume', 'sphere_radius' ] ],

    'tetrahedron_area' : [
'geometry', 'calculates the surface area of a regular tetrahedron of edge length n',
'''
This operator returns the surface area of a regular tetrahedron of edge length
n.

The surface area of an tetrahedron is 4 times the area of an equilateral
triangle with edge length n.
''',
'''
''' + makeCommandExample( '1 inch octahedron_area' ),
[ 'antiprism_area', 'prism_area', 'tetrahedron_volume', 'octahedron_area', 'dodecahedron_area', 'icosahedron_area', 'sphere_area' ] ],

    'tetrahedron_volume' : [
'geometry', 'calculates the volume of a regular tetrahedron of edge length n',
'''
This operator returns the volume of a regular tetrahedron of edge length n.
''',
'''
''' + makeCommandExample( '1 inch tetrahedron_volume' ),
[ 'antiprism_volume', 'prism_volume', 'tetrahedron_area', 'octahedron_volume', 'dodecahedron_volume', 'icosahedron_volume', 'sphere_volume' ] ],

    'torus_area' : [
'geometry', 'calculates the surface area of a torus of major radius n and minor radius k',
'''
This operator returns the surface area of a torus with major radius n and minor
radius k.
''',
'''
''' + makeCommandExample( '6 inches 1 inch torus_area' ),
[ 'torus_volume', 'sphere_area', 'prism_area', 'k_sphere_area', 'cone_area' ] ],

    'torus_volume' : [
'geometry', 'calculates the volume of a torus of major radius n and minor radius k',
'''
This operator returns the volume of a torus with major radius n and minor radius k.
''',
'''
''' + makeCommandExample( '6 inches 1 inch torus_volume' ),
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
'geography', 'calculates the distance, along the Earth\'s surface, between two locations',
'''
This operator calculates the distance, along the Earth\'s surface, between two
locations.

The two locations are specified using either a string that represents a
geographic location to look up, or a lat-long specification using the 'lat_long'
operator.
''',
'''
''' + makeCommandExample( '"New York City, NY" "Los Angeles, CA" geographic_distance' ) + '''
''' + makeCommandExample( '"Nome, Alaska" "Johannesburg, South Africa" geographic_distance' ),
[ 'lat_long' ] ],

    'get_time_zone' : [
'date_time', 'returns the timezone name for location or date-time n',
'''
This operator returns the name of the timezone of date-time n or that contains
location n.
''',
'''
''' + makeCommandExample( 'now get_time_zone' ) + '''
''' + makeCommandExample( '"New York City, NY" get_time_zone' ) + '''
''' + makeCommandExample( '"Nome, Alaska" get_time_zone' ) + '''
''' + makeCommandExample( '"Johannesburg, South Africa" get_time_zone' ),
[ 'location_info', 'get_time_zone_offset' ] ],

    'get_time_zone_offset' : [
'date_time', 'returns the timezone offset in seconds for location or date-time n',
'''
This operator returns the offset in seconds from UTC for the timezone that 
contains location n.
''',
'''
''' + makeCommandExample( '"New York City, NY" get_time_zone_offset' ) + '''
''' + makeCommandExample( '"Nome, Alaska" get_time_zone_offset' ) + '''
''' + makeCommandExample( '"Johannesburg, South Africa" get_time_zone_offset' ),
[ 'location_info', 'get_time_zone' ] ],

    'lat_long' : [
'geography', 'creates a location object given the lat/long for use with other operators',
'''
This operator returns an RPNLocation object, which can be passed to any operator
that requires a location argument.  The argument to this operator is the
latitude and longitude.  It is used to specify a location by latitude and
longitude.
''',
'''
''' + makeCommandExample( '45.63 125.54 lat_long get_time_zone' ) + '''
''' + makeCommandExample( '45.63 125.54 lat_long 45.67 125.43 lat_long geographic_distance' ),
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
[ 'lat_long', 'geographic_distance', 'get_time_zone', 'get_time_zone_offset' ] ],


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
c:\\>rpn _dump_constants
aa_battery:  15400 joule
alpha_particle_mass:  6.644657230e-27 kilogram
april:  4
august:  8
avogadro_number:  6.022140756e23
bohr_radius:  5.29177210903e-11 meter
...
''',
[ '_dump_cache', '_dump_conversions', '_dump_operators', '_dump_stats', '_dump_units', '_dump_aliases', '_dump_prime_cache' ] ],

    '_dump_conversions' : [
'internal', 'dumps the list of unit conversions',
'''
The operator returns number of unit conversions.
''',
'''
c:\\>rpn _dump_conversions
('1/second', 'attobecquerel') 1000000000000000000.0
('1/second', 'attocurie') 27027027.02702702702702702702702702702702702702702703
('1/second', 'attohertz') 1000000000000000000.0
('1/second', 'becquerel') 1.0
('1/second', 'centibecquerel') 100.0
('1/second', 'centicurie') 0.000000002702702702702702702702702702702702702702702702702703
('1/second', 'centihertz') 100.0
...
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
c:\\>rpn 'twin_primes _dump_prime_cache
            1 3
            2 5
            3 11
            4 17
            5 29
            6 41
            7 59
            8 71
            ...
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
c:\\>rpn _dump_stats
rpnChilada 8.5.0 - RPN command-line calculator
copyright (c) 2020 (1988), Rick Gutleber (rickg@his.com)

rpnChilada Statistics:

       742 regular operators
       109 list operators
        12 modifier operators
        ...
''',
[ '_dump_cache', '_dump_conversions', '_dump_aliases', '_dump_operators', '_dump_units', '_dump_constants', '_dump_prime_cache' ] ],

    '_dump_units' : [
'internal', 'lists all rpn units',
'''
The operator returns number of units.
''',
'''
c:\\>rpn _dump_units
1/second
1/siemens
_null_unit
abampere
abcoulomb
abfarad
abhenry
abmho
...
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

    's':              step digits:  This will replaced with a step digit, based
                      on the previous digit, i.e., one greater than or one less
                      than.  Step digits cannot wrap, so for 0, the only step
                      digit is 1, and for 9, the only step digit is 8.

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
''' + makeCommandExample( '2 build_step_numbers' ) + '''
''' + makeCommandExample( '3 build_step_numbers' ),
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
This operator counts the number of occurrences in the digits of n of all the
unique digits in k.
''',
'''
''' + makeCommandExample( '1222333456 1 count_digits' ) + '''
''' + makeCommandExample( '1222333456 23 count_digits' ),
[ 'count_different_digits', 'digits', 'has_digits', 'has_any_digits', 'has_only_digits' ] ],

    'count_different_digits' : [
'lexicography', 'counts the number of different digits in n',
'''
This operator simply counts the number of different digits in integer n.  The
result can be anything from 1 to 10 (for a pandigital number).
''',
'''
''' + makeCommandExample( '1222333456 count_different_digits' ) + '''
''' + makeCommandExample( '7575577755 count_different_digits' ),
[ 'count_digits', 'has_digits', 'has_only_digits' ] ],

    'cyclic_permutations' : [
'lexicography', 'returns a list of all cyclic permutations of integer n',
'''
This operator returns a list containing all the cyclic permutations of integer
n.
''',
'''
''' + makeCommandExample( '12345 cyclic_permutations' ) + '''
All of the circular primes up to a million:
''' + makeCommandExample( '[1379:1:6] build_numbers lambda x cyclic_permutations is_prime and_all filter [ 2 5 ] append sort' ),
[ 'rotate_digits_left', 'rotate_digits_right' ] ],

    'digits' : [
'lexicography', 'counts the number of digits in an integer',
'''
This operator counts the number of digits in an integer.  The functionality is
very similar log10( n ) + 1, except for 0.
''',
'''
''' + makeCommandExample( '1222333456 digits' ) + '''
''' + makeCommandExample( '10 digits' ),
[ 'count_digits', 'has_digits', 'has_any_digits', 'has_only_digits' ] ],

    'duplicate_digits' : [
'lexicography', 'append n with a copy of its last k digits',
'''
This operator returns a new number consisting of the digits of n, followed by
the last k digits of n.

This is a weird operator that I probably made to solve a Project Euler problem.
<shrug>
''',
'''
''' + makeCommandExample( '2345 3 duplicate_digits' ) + '''
''' + makeCommandExample( '12345 5 duplicate_digits' ),
[ 'add_digits', 'combine_digits', 'duplicate_number' ] ],

    'duplicate_number' : [
'lexicography', 'return a number with the digits of n duplicated k times',
'''
This operator takes the digits of n and appends them k times to create a larger
number.
''',
'''
''' + makeCommandExample( '2345 3 duplicate_number' ) + '''
''' + makeCommandExample( '12345 5 duplicate_number' ),
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
''' + makeCommandExample( '6788 erdos_persistence' ) + '''
''' + makeCommandExample( '68889 erdos_persistence' ) + '''
''' + makeCommandExample( '55555555555555557777777777777 erdos_persistence' ),
[ 'persistence', 'show_erdos_persistence', 'k_persistence' ] ],

    'filter_max' : [
'functions', 'filters all values greater than k from list n',
'''
This operator is a shortcut for 'n lambda x k is_not_greater filter'.
''',
'''
''' + makeCommandExample( '1 30 range 10 filter_max' ),
[ 'filter_min', 'filter', 'filter_integers', 'filter_on_flags', 'filter_ratio' ] ],

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
[ 'filter', 'filter_integers' ] ],

    'find_palindrome' : [
'lexicography', 'adds the reverse of n to itself up to k successive times to find a palindrome',
'''
This operator adds the reversed-digits version of n to itself, and repeating the
process with the subsequent results up to k successive times to find a
palindrome (i.e., a number whose digits are the same forwards and backwards).

If a palindrome number is found, the operator returns two values, the number of
steps it took to get to the palindrome, and the palindrome itself.   If no
palindrome is found, the operator returns k and 0.

The numbers can get quite large, so it's best to set a high accuracy when using
this operator.
''',
'''
Find the longest palindrome chain in the numbers between 10000 and 11000.  Of
course, it necessary by trial-and-error to discover how long the chains can
become and how big the numbers get.
''' + makeCommandExample( '-a30 10000 11000 range 100 find_palindrome lambda 0 x 0 element x 1 element 0 equal if for_each_list max_index 10000 +' ) + '''
''' + makeCommandExample( '-a30 10911 55 find_palindrome' ) + '''
''' + makeCommandExample( '-a20 89 25 find_palindrome' ),
[ 'reversal_addition', 'is_kaprekar', 'reverse_digits' ] ],

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

    'get_decimal_digits' : [
'lexicography', 'returns a list of k digits comprising the number n',
'''
This operator returns a list of k digits comprising the number n.  This includes
the integral value of n (if any) followed by enough decimal digits to make k
digits.

The last digit is not rounded up.

It is necessary to set the accuracy to k using -a if k is greater than the
default accuracy.
''',
'''
''' + makeCommandExample( '-a20 pi 20 get_decimal_digits' ) + '''
''' + makeCommandExample( '-a20 2 sqrt 20 get_decimal_digits' ) + '''
''' + makeCommandExample( '19457 3 get_decimal_digits' ) + '''
''' + makeCommandExample( '34.678 4 get_decimal_digits' ) + '''
''' + makeCommandExample( '0.00078 5 get_decimal_digits' ),
[ 'get_digits', 'get_base_k_digits' ] ],


    'get_digits' : [
'lexicography', 'returns the list of digits comprising integer n',
'''
This operation is useful for working with any lexicographic feature based
on the digits that comprise an integer.
''',
'''
''' + makeCommandExample( '1234567890 get_digits' ),
[ 'get_decimal_digits', 'digits', 'has_digits', 'get_nonzero_digits', 'get_base_k_digits' ] ],

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
''' + makeCommandExample( '90625 is_automorphic' ) + '''
''' + makeCommandExample( '90625 squared' ),
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
'lexicography', 'returns whether n is a Smith number in base k',
'''
Returns true (1) if n is a Smith number in base k.

From https://en.wikipedia.org/wiki/Smith_number:

In number theory, a Smith number is a composite number for which, in a given
number base, the sum of its digits is equal to the sum of the digits in its
prime factorization in the given number base.  In the case of numbers that are
not square-free, the factorization is written without exponents, writing the
repeated factor as many times as needed.
''',
'''
''' + makeCommandExample( '164736913905 10 is_base_k_smith_number' ) + '''
''' + makeCommandExample( '1 400 range lambda x 10 is_base_k_smith_number filter' ),
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
From https://en.wikipedia.org/wiki/Harshad_number:

In mathematics, a harshad number (or Niven number) in a given number base is an
integer that is divisible by the sum of its digits when written in that base.
Harshad numbers in base n are also known as n-harshad (or n-Niven) numbers.
Harshad numbers were defined by D. R. Kaprekar, a mathematician from India.  The
word "harshad" comes from the Sanskrit harsa (joy) + da (give), meaning
joy-giver.  The term "Niven number" arose from a paper delivered by Ivan M.
Niven at a conference on number theory in 1977.  All integers between zero and
n are n-harshad numbers.

The number 18 is a harshad number in base 10, because the sum of the digits 1
and 8 is 9 (1 + 8 = 9), and 18 is divisible by 9.

Given the divisibility test for 9, one might be tempted to generalize that all
numbers divisible by 9 are also harshad numbers.  But for the purpose of
determining the harshadness of n, the digits of n can only be added up once and
n must be divisible by that sum; otherwise, it is not a harshad number.  For
example, 99 is not a harshad number, since 9 + 9 = 18, and 99 is not divisible
by 18.

The base number (and furthermore, its powers) will always be a harshad number in
its own base, since it will be represented as "10" and 1 + 0 = 1.
''',
'''
''' + makeCommandExample( '1 40 range lambda x 10 is_harshad filter' ) + '''
''' + makeCommandExample( '100 150 range lambda x 9 is_harshad filter' ) + '''
''' + makeCommandExample( '1000 1100 range lambda x 27 is_harshad filter' ),
[ 'sum_digits', 'get_base_k_digits' ] ],

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
The operator returns 1 if the digits of the kth power of n end with the digits
of n, otherwise it returns 0.
''',
'''
''' + makeCommandExample( '9376 4 is_k_morphic' ) + '''
''' + makeCommandExample( '-a20 9376 4 **' ) + '''
''' + makeCommandExample( '749 5 is_k_morphic' ) + '''
''' + makeCommandExample( '-a20 749 5 **' ) + '''
''' + makeCommandExample( '5001 7 is_k_morphic' ) + '''
''' + makeCommandExample( '-a30 5001 7 **' ) + '''
''' + makeCommandExample( '7943 13 is_k_morphic' ) + '''
''' + makeCommandExample( '-a60 7943 13 **' ),
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
From https://en.wikipedia.org/wiki/Sum-product_number:

A sum-product number in a given number base b is a natural number that is equal
to the product of the sum of its digits and the product of its digits.
''',
'''
''' + makeCommandExample( '1 1000 range lambda x 7 is_sum_product filter -r7' ) + '''
''' + makeCommandExample( '1 1000 range lambda x 10 is_sum_product filter' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 11 is_sum_product filter -r11' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 14 is_sum_product filter -r14' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 19 is_sum_product filter -r19' ),
[ 'sum_digits', 'multiply_digits' ] ],

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
This operator returns 1 if the digits of n cubed end with the digits of n,
otherwise it returns 0.
''',
'''
''' + makeCommandExample( '9999 is_trimorphic' ) + '''
''' + makeCommandExample( '9999 cubed' ) + '''
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
This operator returns a value based on argument a with every instance of digit b
replaced with digit c.
''',
'''
''' + makeCommandExample( '123 1 4 replace_digits' ) + '''
''' + makeCommandExample( '1997 9 8 replace_digits' ) + '''
''' + makeCommandExample( '5000 5 0 replace_digits' ),
[ 'combine_digits', 'permute_digits' ] ],

    'reversal_addition' : [
'lexicography', 'returns a list by successively reversing the digits and adding that value to the previous element',
'''
This operator returns a list based on n, where each successive element of the
list is produced by reversing the digits of the last element and adding that new
value to the last element.

This process is continued for k steps, unless a number with palindrome digits
(i.e., the number reads the same forwards and backwards ) occurs, in which case
the resulting list is terminated at that point.
''',
'''
''' + makeCommandExample( '-a20 89 24 reversal_addition' ),
[ 'find_palindrome', 'is_kaprekar' ] ],

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
This operator takes the input value n, and shifts its digits left by k places.
This means that the leftmost k digits are rotated around to the end of the
number, as if the digits were on a ring.
''',
'''
''' + makeCommandExample( '123456 1 rotate_digits_left' ) + '''
''' + makeCommandExample( '123456 4 rotate_digits_left' ) + '''
''' + makeCommandExample( '123456 6 rotate_digits_left' ) + '''
''' + makeCommandExample( '123456 7 rotate_digits_left' ),
[ 'rotate_digits_right' ] ],

    'rotate_digits_right' : [
'lexicography', 'rotates the digits of n to the right by k digits',
'''
This operator takes the input value n, and shifts its digits right by k places.
This means that the rightmost k digits are rotated around to the start of the
number, as if the digits were on a ring
''',
'''
''' + makeCommandExample( '123456 1 rotate_digits_right' ) + '''
''' + makeCommandExample( '123456 4 rotate_digits_right' ) + '''
''' + makeCommandExample( '123456 6 rotate_digits_right' ) + '''
''' + makeCommandExample( '123456 7 rotate_digits_right' ),
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
''' + makeCommandExample( '6788 show_erdos_persistence' ) + '''
''' + makeCommandExample( '68889 show_erdos_persistence' ),
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
''' + makeCommandExample( '3 3 show_k_persistence' ) + '''
''' + makeCommandExample( '2 4 show_k_persistence' ),
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
''' + makeCommandExample( '6788 show_persistence' ) + '''
''' + makeCommandExample( '68889 show_persistence' ),
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
This operator calculates the sum of the digits of integer n.
''',
'''
''' + makeCommandExample( '1234 sum_digits' ) + '''
''' + makeCommandExample( '6788 sum_digits' ) + '''
''' + makeCommandExample( '-a40 3 50 ** sum_digits' ),
[ 'multiply_digits', 'get_digits' ] ],


    #******************************************************************************
    #
    #  logical operators
    #
    #******************************************************************************

    'and' : [
'logical', 'returns 1 if n and k are both nonzero',
'''
'and' is the logical operation which returns true if and only if the two
operands are true.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
'nand' is the logical operation which returns true if at least one of the two
operands is false.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
'nor' is the logical operation which returns true if and only if the two
operands are false.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
'not' is the logical operation which negates its single operand.  If the operand
is true, then it returns false (0).  If the operand is false, then it returns
true (1).

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
''',
'''
''' + makeCommandExample( '0 not' ) + '''
''' + makeCommandExample( '1 not' ),
[ 'or', 'nand', 'bitwise_not' ] ],

    'or' : [
'logical', 'return 1 if either n or k, or both, are zero',
'''
'or' is the logical operation which returns true if one or both of the operands
is true.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
'xnor' is the logical operation which returns true if both of the operands
are true, or both of the operands are false.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
'xor' is the logical operation which returns true if one operand is true, and
the other operand is false.

True and false in this context are defined to be non-zero and zero for operands
and 1 and 0 for return values.
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
''' + makeCommandExample( '1 1000 range lambda [ x is_antiharmonic x is_pernicious x is_semiprime ] and_all filter' ),
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
This operator returns a list of n-element lists of corresponding elements from
each sublist of n.
''',
'''
''' + makeCommandExample( '6 10 range 1 enumerate' ) + '''
''' + makeCommandExample( '6 10 range 1 enumerate collate' ),
[ 'flatten', 'group_elements', 'interleave' ] ],

    'compare_lists' : [
'list_operators', 'compares lists n and k',
'''
This operator compares lists n and k, and returns 1 if they are the same, and 0
if they are not.

'is_equal' is not a list operator, so it will only compare elements of two
lists up to the length of the shorter of the two lists.  'compare_lists' will
compare them fully.
''',
'''
''' + makeCommandExample( '[ 1 2 3 4 ] 1 4 range compare_lists' ) + '''
''' + makeCommandExample( '1 3 range 1 4 range is_equal' ) + '''
''' + makeCommandExample( '1 3 range 1 4 range compare_lists' ),
[ 'append' ] ],

    'count' : [
'list_operators', 'counts the elements of list n',
'''
This operator simply counts the number of elements in the list.
''',
'''
''' + makeCommandExample( '1 100 range count' ),
[ 'element' ] ],

    'cumulative_diffs' : [
'list_operators', 'returns a list with the differences between each element of list n with the first element',
'''
This operator returns a list with the differences between each element of list
n with the first element.

The list returned will be one shorter than the length of the list n.
''',
'''
''' + makeCommandExample( '[ 0 1 2 3 4 5 ] cumulative_diffs' ) + '''
''' + makeCommandExample( '[ 1 3 6 10 15 21 28 36 45 55 ] cumulative_diffs' ) + '''
''' + makeCommandExample( '[ 100 200 300 400 500 ] cumulative_diffs' ),
[ 'diffs', 'ratios', 'cumulative_ratios', 'cumulative_sums', 'cumulative_means' ] ],

    'cumulative_means' : [
'list_operators', 'returns a list of the cumulative means of each element and the elements that precede it',
'''
This operator returns a list of the cumulative means of each element in list n
and all the elements that precede it.

The xth item of the resulting list is the mean of the first x items in n.
''',
'''
''' + makeCommandExample( '1 10 range cumulative_means' ),
[ 'cumulative_sums', 'cumulative_ratios', 'cumulative_products', 'cumulative_diffs' ] ],

    'cumulative_products' : [
'list_operators', 'returns a list of the cumulative products of element with the elements that precede it',
'''
This operator returns a list of the cumulative products of each element with the
elements that precede it

The xth item of the resulting list is the product of the first x items in n.
''',
'''
''' + makeCommandExample( '1 10 range cumulative_products' ),
[ 'cumulative_sums', 'cumulative_ratios', 'cumulative_diffs', 'cumulative_means' ] ],

    'cumulative_ratios' : [
'list_operators', 'returns a list with the ratios between each element of n and the first',
'''
This operator is analogous to the 'cumulative_diffs' operator.
''',
'''
''' + makeCommandExample( '1 10 range fibonacci cumulative_ratios' ),
[ 'ratios', 'diffs', 'cumulative_diffs', 'cumulative_products', 'cumulative_means' ] ],

    'cumulative_sums' : [
'list_operators', 'return a list of the cumulative sums of n',
'''
The xth item of the resulting list is the sum of the first x items in n.
''',
'''
''' + makeCommandExample( '1 10 range cumulative_sums' ),
[ 'cumulative_products', 'cumulative_ratios', 'cumulative_diffs', 'cumulative_means' ] ],

    'difference' : [
'list_operators', 'returns a list of unique elements in list k that are not found in list n',
'''
This operator eturns a list of unique elements in list k that are not found in
list n.
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
This operator returns the kth item from list n.  The index is zero-based.
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
This operator returns the first index of list k that equals n.  If the value n
is not found in the list, the operator returns -1.
''',
'''
''' + makeCommandExample( '[ 1 4 5 6 9 ] 6 find' ) + '''
And we can access the found item using the 'element' operator:
''' + makeCommandExample( '[ 1 4 5 6 9 ] 3 element', indent=4 ),
[ 'count', 'filter' ] ],

    'flatten' : [
'list_operators', 'flattens a nested lists in list n to a single level',
'''
This operator takes an arbitrarily nested list and flattens it to a simple list
of items, which each element of each sublist arranged in order, depth-first.
''',
'''
''' + makeCommandExample( '[ 1 2 [ 3 4 ] [ 5 [ 6 7 ] 8 [ 9 ] ] [ [ 10 ] ] ] flatten' ),
[ 'collate', 'interleave', 'group_elements' ] ],

    'geometric_range' : [
'list_operators', 'generates a list of geometric progression of numbers',
'''
This operator generates a list of geometric progressions of numbers.

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
This operator returns a list of lists, where each list has k members.  Every
combination of k elements from list n are generated.
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
This operator returns a list of lists, where each list has k members.  Every
permutation of k elements from list n are generated.

This is different from 'get_combinations' in that order matters, so [ 1, 2 ] and
[ 2, 1 ] are considered distinct.
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] 2 get_permutations -s1' ),
[ 'get_combinations', 'get_repeat_permutations', 'get_partitions' ] ],

    'get_repeat_combinations' : [
'list_operators', 'generates all combinations of k members of list n, with repeats allowed',
'''
This operator returns a list of lists, where each list has k members.  Every
combination of k elements from list n are generated, including repeats of each
element.
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] 2 get_repeat_combinations -s1' ),
[ 'get_permutations', 'get_combinations' ] ],

    'get_repeat_permutations' : [
'list_operators', 'generates all permutations of k members of list n, with repeats allowed',
'''
This operator returns a list of lists, where each list has k members.  Every
permutations of k elements from list n are generated, including repeats of each
element.
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
This operator returns a list of unique elements that exist in both lists.
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
This operator returns true (1) if the list n is a palindrome, meaning that the
values of the elements are the same in both directions.
''',
'''
''' + makeCommandExample( '[ 1 2 3 ] is_palindrome_list' ) + '''
''' + makeCommandExample( '[ 1 2 3 2 1 ] is_palindrome_list' ) + '''
''' + makeCommandExample( '[ 1 2 3 ] is_palindrome_list' ),
[ 'is_digital_palindrome' ] ],

    'left' : [
'list_operators', 'returns the left k items from list n',
'''
This operator returns a list consisting of the leftmost k items of list n.
''',
'''
''' + makeCommandExample( '1 10 range 6 left' ) + '''
''' + makeCommandExample( '1 10 range 4 left' ) + '''
''' + makeCommandExample( '1 10 range 1 4 range left' ),
[ 'right', 'slice', 'sublist', 'random_element' ] ],

    'max_index' : [
'list_operators', 'returns the index of largest value in list n',
'''
This operator returns the index of the item in the list with the largest value.
If there are more than one item in the list with this largest value, then the
operator returns the index of the first occurrence of that value.
''',
'''
''' + makeCommandExample( '[ 8 10 9 3 4 2 5 1 7 6 ] max_index' ) + '''
''' + makeCommandExample( '[ 1 2 3 3 2 3 1 ] max_index' ) + '''
''' + makeCommandExample( '[ 1 ] max_index' ),
[ 'min_index', 'element' ] ],

    'min_index' : [
'list_operators', 'returns the index of smallest value in list n',
'''
This operator returns the index of the item in the list with the smallest value.
If there are more than one item in the list with this smallest value, then the
operator returns the index of the first occurrence of that value.
''',
'''
''' + makeCommandExample( '[ 8 10 9 3 4 2 5 1 7 6 ] min_index' ) + '''
''' + makeCommandExample( '[ 1 2 3 1 2 3 1 ] min_index' ) + '''
''' + makeCommandExample( '[ 1 ] min_index' ),
[ 'max_index', 'element' ] ],

    'nand_all' : [
'list_operators', 'returns true if every member of the list is zero',
'''
This operator returns true (1) if every member of the list is zero, otherwise it
returns false (0).
''',
'''
''' + makeCommandExample( '[ 1 0 1 0 ] nand_all' ) + '''
''' + makeCommandExample( '[ 1 1 1 1 ] nand_all' ) + '''
''' + makeCommandExample( '[ 0 0 0 0 ] nand_all' ),
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
This operator returns true (1) if any member of the list is zero, otherwise it
returns false (0).
''',
'''
''' + makeCommandExample( '[ 1 0 1 0 ] nor_all' ) + '''
''' + makeCommandExample( '[ 1 1 1 1 ] nor_all' ) + '''
''' + makeCommandExample( '[ 0 0 0 0 ] nor_all' ),
[ 'and_all', 'or_all', 'nand_all' ] ],

    'occurrence_cumulative' : [
'list_operators', 'returns the cumulative ratio of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
ratio (out of 1.0), where each value is the cumulative ratio of that item and the
ones preceding it.  The result will be sorted by values.
''',
'''
''' + makeCommandExample( '2d4 permute_dice occurrence_cumulative -s1' ),
[ 'occurrence_ratios', 'occurrences' ] ],

    'occurrence_ratios' : [
'list_operators', 'returns the ratio of occurrences of each value in a list',
'''
The result is a list of lists, where each sublist contains a value and a
ratio (out of 1.0).  The result will be sorted by values.
''',
'''
''' + makeCommandExample( '2d4 permute_dice occurrence_ratios -s1' ),
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
''' + makeCommandExample( '[ 1 0 1 0 ] or_all' ) + '''
''' + makeCommandExample( '[ 1 1 1 1 ] or_all' ) + '''
''' + makeCommandExample( '[ 0 0 0 0 ] or_all' ),
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
This operator returns the powerset of list n.  The powerset of a list includes
every subset of that list, including the empty set, but 'powerset' leaves out
the empty set.

I don't think including an empty list in the output would ever be useful.
''',
'''
''' + makeCommandExample( '1 3 range powerset' ),
[ 'permute_lists', 'sublist' ] ],

    'random_element' : [
'list_operators', 'returns a random element from list n',
'''
This operator returns a single, randomly-chosen element from list n.
''',
'''
''' + makeCommandExample( '1 10 range random_element' ) + '''
''' + makeCommandExample( '[ 1 5 10 12 15 19 ] random_element' ) + '''
''' + makeCommandExample( '[ 1 4 range 5 8 range 9 12 range ] random_element' ),
[ 'shuffle', 'sublist', 'reverse', 'powerset' ] ],

    'range' : [
'list_operators', 'generates a list of successive integers from n to k',
'''
This operator generates a list of successive integers starting from n and
continuing to k.  If k is greater than n, then the list consists of successive
numbers in numerical reverse order.
''',
'''
''' + makeCommandExample( '1 10 range' ) + '''
''' + makeCommandExample( '10 1 range' ),
[ 'exponential_range', 'geometric_range', 'interval_range', 'sized_range' ] ],

    'ratios' : [
'list_operators', 'returns a list with the ratios between successive elements of list n',
'''
This operator returns a list of the ratios between successive elements of list
n.  If the list has length x, then the result will be of length x - 1.

This operator is analogous to the 'diffs' operator.
''',
'''
''' + makeCommandExample( '1 10 range ratios' ) + '''
''' + makeCommandExample( '-p4 1 10 range fib ratios' ),
[ 'cumulative_ratios', 'diffs', 'cumulative_diffs' ] ],

    'reduce' : [
'list_operators', 'reduces out the common factors from each element of a list',
'''
In other words, each element of the list is divided by the greatest common
denominator of the whole list.
''',
'''
''' + makeCommandExample( '[ 3 12 27 15 ] reduce' ) + '''
''' + makeCommandExample( '[ 1 2 3 4 ] reduce' ) + '''
''' + makeCommandExample( '[ 10 20 40 50 30 ] reduce' ),
[ 'gcd', 'gcd2' ] ],

    'reverse' : [
'list_operators', 'returns list n with its elements reversed',
'''
This operator returns a list with all of the elements in list n, but reversed in
order.
''',
'''
''' + makeCommandExample( '1 10 range reverse' ),
[ 'shuffle', 'random_element' ] ],

    'right' : [
'list_operators', 'returns the right k items from list n',
'''
This operator returns a list consisting of the leftmost k items of list n.
''',
'''
''' + makeCommandExample( '1 10 range 6 right' ) + '''
''' + makeCommandExample( '1 10 range 4 right' ) + '''
''' + makeCommandExample( '1 10 range 1 4 range right' ),
[ 'left', 'slice', 'sublist', 'random_element' ] ],

    'shuffle' : [
'list_operators', 'randomly shuffles the elements in a list',
'''
This operator returns a list of all the elements of n reordered randomly.
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
This operator returns a list of unique items that occur in either list.
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
This operator returns a list of the unique elements in list n.
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
This operator calculates the natural logarithm of n.

From https://en.wikipedia.org/wiki/Natural_logarithm:
''',
'''
''' + makeCommandExample( '2 log' ) + '''
''' + makeCommandExample( 'e log' ) + '''
''' + makeCommandExample( 'e 2 ** log' ) + '''
''' + makeCommandExample( '10 log' ) + '''
''' + makeCommandExample( 'e -1 * log' ) + '''
''' + makeCommandExample( '3 5j + log' ),
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
Evaluates the polyexponential function, defined for arbitrary complex n, k by
the series:
                      inf
                    ------
                     \\      x^n
    E_sub_n( k ) =    \\     --- k^x
                     /       x!
                    ------
                     x = 1

E_sub_n( k ) is constructed from the exponential function analogously to how the
polylogarithm is constructed from the ordinary logarithm; as a function of n
(with k fixed), E_sub_n is an L-series.  It is an entire function of both n and
k.
''',
'''
''' + makeCommandExample( '0.5 1 polyexp' ) + '''
''' + makeCommandExample( '1 inf lambda x 0.5 ** x ! / ranged_sum' ) + '''
''' + makeCommandExample( '-3 4j - 2.5 2j + polyexp' ) + '''
''' + makeCommandExample( '4 -100 polyexp' ),
[ 'polylog', 'exp' ] ],

    'polylog' : [
'logarithms', 'calculates the polylogarithm of n, k',
'''
Computes the polylogarithm, defined by the sum

                       inf
                     ------
                      \\       k^x
    Li_sub_n( k ) =    \\      ---
                      /       x^n
                     ------
                      x = 1

This series is convergent only for |k| < 1, so elsewhere the analytic
continuation is implied.

The polylogarithm should not be confused with the logarithmic integral (also
denoted by Li or li), which is implemented as 'li'.
''',
'''
''' + makeCommandExample( '1 0.5 polylog' ) + '''
''' + makeCommandExample( '2 log' ) + '''
''' + makeCommandExample( '2 0.5 polylog' ) + '''
''' + makeCommandExample( 'pi sqr 6 2 log sqr * - 12 /' ) + '''
''' + makeCommandExample( '2 10 polylog' ),
[ 'log', 'polyexp', 'li' ] ],


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
From https://en.wikipedia.org/wiki/Abundant_number:

In number theory, an abundant number or excessive number is a number for which
the sum of its proper divisors is greater than the number itself.  The integer
12 is the first abundant number.  Its proper divisors are 1, 2, 3, 4 and 6 for a
total of 16.  The amount by which the sum exceeds the number is the abundance.
The number 12 has an abundance of 4, for example.

The sum of the proper divisors is also called the aliquot sum.

An abundant number has a positive abundance.  A deficient number has a negative
abundance.  A perfect number (or 1) has a zero abundance.
''',
'''
''' + makeCommandExample( '1 20 range abundance' ) + '''
''' + makeCommandExample( '672 abundance' ),
[ 'abundance_ratio', 'aliquot', 'is_abundant', 'is_deficient', 'is_perfect' ] ],

    'abundance_ratio' : [
'number_theory', 'returns the abundance ratio of n',
'''
The abundance ratio of n is the ratio of the sum of the proper divisors of n
(i.e., the aliquot sum) to n itself.

An abundant number has an abundance ratio greater than 2.  A deficient number
has an abundance ratio less than 2.  A perfect number has an abundance ratio of
2, exactly.
''',
'''
''' + makeCommandExample( '1 10 range abundance_ratio' ) + '''
''' + makeCommandExample( '672 abundance_ratio' ) + '''
''' + makeCommandExample( '1680 abundance_ratio' ) + '''
''' + makeCommandExample( '32760 abundance_ratio' ),
[ 'abundance', 'aliquot', 'is_abundant', 'is_deficient', 'is_perfect' ] ],

    'ackermann_number' : [
'number_theory', 'calculates the value of the Ackermann function for n and k',
'''
From https://en.wikipedia.org/wiki/Ackermann_function:

In computability theory, the Ackermann function, named after Wilhelm Ackermann,
is one of the simplest and earliest-discovered examples of a total computable
function that is not primitive recursive.  All primitive recursive functions are
total and computable, but the Ackermann function illustrates that not all total
computable functions are primitive recursive.

After Ackermann's publication of his function (which had three nonnegative
integer arguments), many authors modified it to suit various purposes, so that
today "the Ackermann function" may refer to any of numerous variants of the
original function.  One common version, the two-argument Ackermann–Peter
function, is defined as follows for nonnegative integers m and n:

A⁡(0,n)	= n+1
A⁡(m+1,0) = A⁡(m,1)
A⁡(m+1,n+1) = A⁡(m,A(m+1,n))

This is the version of the function implemented by the 'ackermann_number'
operator.
''',
'''
''' + makeCommandExample( '1 3 range 4 ackermann_number' ) + '''
''' + makeCommandExample( '3 1 10 range ackermann_number' ),
[ 'hyperoperator' ] ],

    'aliquot' : [
'number_theory', 'returns the first k members of the aliquot sequence of n',
'''
The sum of the proper divisors of an integer is called the aliquot sum.  An
aliquot sequence is created by taking successive aliquot sums, starting from
a particular integer.

An aliquot sequence can result in an infinite loop of amicable numbers, a set of
numbers for which the aliquot sums loop.  For instance, 220 has an aliquot sum
of 284, which in turn has an aliquot sum of 220.

Otherwise, an aliquot sequence can terminate by going to 0, since the aliquot
sum of 1 is defined to be 0.

It is conjectured that all aliquot sequences that do not end up in a loop of
amicable numbers eventually go to 0.

This operator will generating the aliquot sequence, starting with n and
continuing until k numbers are generated, or a repeat occurs.
''',
'''
''' + makeCommandExample( '276 10 aliquot' ) + '''
''' + makeCommandExample( '614 20 aliquot' ) + '''
''' + makeCommandExample( '320 25 aliquot' ),
[ 'aliquot_limit', 'collatz' ] ],

    'aliquot_limit' : [
'number_theory', 'returns the members of the aliquot sequence of n until 10^k is exceeded',
'''
The sum of the proper divisors of an integer is called the aliquot sum.  An
aliquot sequence is created by taking successive aliquot sums, starting from
a particular integer.

An aliquot sequence can result in an infinite loop of amicable numbers, a set of
numbers for which the aliquot sums loop.  For instance, 220 has an aliquot sum
of 284, which in turn has an aliquot sum of 220.

Otherwise, an aliquot sequence can terminate by going to 0, since the aliquot
sum of 1 is defined to be 0.

It is conjectured that all aliquot sequences that do not end up in a loop of
amicable numbers eventually go to 0.

This operator will generating the aliquot sequence, starting with n and
continuing until k numbers are generated, or a repeat occurs, or the sequence
produces a number exceeding 10^k (i.e., has more than k digits).
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
''' + makeCommandExample( '7 barnesg' ) + '''
''' + makeCommandExample( '15.6 barnesg' ) + '''
''' + makeCommandExample( '4 3j + barnesg' ),
[ 'superfactorial', 'gamma' ] ],

    'base' : [
'number_theory', 'interprets list elements from n as base k digits',
'''
This operator is used to convert numbers from an arbitrary base to base 10.
Instead of having to come up with additional digits to represent every base-k,
the list n is interpreted as a list of base-k digits, which are themselves
repesented in base 10.
''',
'''
''' + makeCommandExample( '-x [ 76 81 43 17 ] 97 base' ) + '''
Convert an IP address to a 32-bit value and back (by pretending it's a base-256
number):
    We'll use '-x' to convert the result to hexadecimal:
''' + makeCommandExample( '-x [ 192 168 0 1 ] 256 base' ) + '''
    We can convert it back by using base 256:
''' + makeCommandExample( '0xc0a80001 256 get_base_k_digits' ) + '''
''',
[ 'get_base_k_digits' ] ],

    'beta' : [
'number_theory', 'evaluates the Beta function for n and k',
'''
The operator computer the Beta function, which is equal to:

    gamma( x ) gamma( y )
    ---------------------
       gamma( x + y )

The 'beta' operator is the equivalent to 'n gamma k gamma * n k + gamma /'.

For integer and half-integer arguments where all three gamma functions are
finite, the Beta function becomes either rational number or a rational multiple
of pi.
''',
'''
''' + makeCommandExample( '5 2 beta' ) + '''
''' + makeCommandExample( '-1.5 2 beta' ) + '''
''' + makeCommandExample( '2.5 1.5 beta 16 *' ),
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
[ 'nth_stern', 'fraction', 'continued_fraction' ] ],

    'continued_fraction' : [
'number_theory', 'interprets list n as a continued fraction',
'''
This operator interprets list n as terms in a continued fraction.  Note that
setting a sufficient level of accuracy (using -a) is very important to getting
a correct result with longer lists.

From https://en.wikipedia.org/wiki/Continued_fraction:

In mathematics, a continued fraction is an expression obtained through an
iterative process of representing a number as the sum of its integer part and
the reciprocal of another number, then writing this other number as the sum of
its integer part and another reciprocal, and so on.  In a finite continued
fraction (or terminated continued fraction), the iteration/recursion is
terminated after finitely many steps by using an integer in lieu of another
continued fraction. In  contrast, an infinite continued fraction is an infinite
expression.  In either case, all integers in the sequence, other than the first,
must be positive.  The integers are called the coefficients or terms of the
continued fraction.
''',
'''
''' + makeCommandExample( '[ 3 7 15 1 292 1 1 1 2 1 ] continued_fraction' ) + '''
''' + makeCommandExample( '[ 1 2 2 2 2 2 2 2 2 2 2 2 ] continued_fraction' ),
[ 'make_continued_fraction', 'fraction' ] ],

    'collatz' : [
'number_theory', 'returns the first k members of the Collatz sequence of n',
'''
From https://en.wikipedia.org/wiki/Collatz_conjecture:

The Collatz conjecture is a conjecture in mathematics that concerns a sequence
defined as follows:  start with any positive integer n.  Then each term is
obtained from the previous term as follows:  if the previous term is even, the
next term is one half of the previous term.  If the previous term is odd, the
next term is 3 times the previous term plus 1.  The conjecture is that no matter
what value of n, the sequence will always reach 1.

This operator will generate the first k elements of the Collatz sequence for n,
or until 1 is reached.
''',
'''
''' + makeCommandExample( '3 10 collatz' ) + '''
''' + makeCommandExample( '74 25 collatz' ),
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
Using the Chinese Remainder Theorem, this function calculates a number that is
equal to n[ x ] modulo k[ x ], with x iterating through the indices of each
list (which must be the same size).
''',
'''
''' + makeCommandExample( '[ 2 3 5 7 ] [ 1 2 3 4 ] crt' ) + '''
''' + makeCommandExample( '[ 101 103 107 109 ] [ 21 22 23 25 ] crt' ),
[ 'digital_root', 'harmonic_residue' ] ],

    'digamma' : [
'number_theory', 'calculates the digamma function for n',
'''
The digamma function is defined as the logarithmic derivative of the gamma
function.

This is the equivalent of '0 n polygamma'.
''',
'''
''' + makeCommandExample( '1 10 10 geometric_range digamma' ),
[ 'polygamma', 'trigamma' ] ],

    'digital_root' : [
'number_theory', 'returns the digital root of n',
'''
From https://en.wikipedia.org/wiki/Digital_root:

The digital root (also repeated digital sum) of a natural number in a given
number base is the (single digit) value obtained by an iterative process of
summing digits, on each iteration using the result from the previous iteration
to compute a digit sum.  The process continues until a single-digit number is
reached.
''',
'''
''' + makeCommandExample( '1 20 range digital_root' ),
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
This operator calculates the Egyption fractions for n/k using the greedy
algorithm.

From https://en.wikipedia.org/wiki/Egyptian_fraction:

An Egyptian fraction is a finite sum of distinct unit fractions, such as:

1   1    1
- + - + --
2   3   16

That is, each fraction in the expression has a numerator equal to 1 and a
denominator that is a positive integer, and all the denominators differ from
each other.  The value of an expression of this type is a positive rational
number a/b; for instance the Egyptian fraction above sums to 43/48.  Every
positive rational number can be represented by an Egyptian fraction.  Sums of
this type, and similar sums also including 2/3 and 3/4 as summands, were used as
a serious notation for rational numbers by the ancient Egyptians, and continued
to be used by other civilizations into medieval times.  In modern mathematical
notation, Egyptian fractions have been superseded by vulgar fractions and
decimal notation.  However, Egyptian fractions continue to be an object of study
in modern number theory and recreational mathematics, as well as in modern
historical studies of ancient mathematics.

From https://en.wikipedia.org/wiki/Greedy_algorithm_for_Egyptian_fractions:

In mathematics, the greedy algorithm for Egyptian fractions is a greedy
algorithm, first described by Fibonacci, for transforming rational numbers into
 Egyptian fractions.  An Egyptian fraction is a representation of an irreducible
 fraction as a sum of distinct unit fractions, as e.g. 5/6 = 1/2 + 1/3.  As the
 name indicates, these representations have been used as long ago as ancient
 Egypt, but the first published systematic method for constructing such
 expansions is described in the Liber Abaci (1202) of Leonardo of Pisa
 (Fibonacci).  It is called a greedy algorithm because at each step the
 algorithm chooses greedily the largest possible unit fraction that can be used
 in any representation of the remaining fraction.
''',
'''
''' + makeCommandExample( '45 67 egyptian_fractions' ) + '''
''' + makeCommandExample( '45 67 egyptian_fractions sum 67 *' ),
[ 'nth_sylvester', 'fraction' ] ],

    'eta' : [
'number_theory', 'calculates the Dirichlet eta function for n',
'''
This operator calculates the Dirichlet eta function for n.

From https://en.wikipedia.org/wiki/Dirichlet_eta_function:

n mathematics, in the area of analytic number theory, the Dirichlet eta function
is defined by the following Dirichlet series, which converges for any complex
number having real part > 0:

                          1     1     1     1
         eta( n ) =  1 + --- - --- + --- - --- ...
                         2^n   3^n   4^n   5^n

This Dirichlet series is the alternating sum corresponding to the Dirichlet
series expansion of the Riemann zeta function, zeta( s ) — and for this reason
the Dirichlet eta function is also known as the alternating zeta function, also
denoted zeta*( s ).
''',
'''
''' + makeCommandExample( '3 eta' ) + '''
''' + makeCommandExample( '2 6i + eta' ),
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
From https://en.wikipedia.org/wiki/Euler%27s_totient_function:

In number theory, Euler's totient function counts the positive integers up to a
given integer n that are relatively prime to n.  It is written using the Greek
letter phi as phi( n ), and may also be called Euler's phi function.  In other
words, it is the number of integers k in the range 1 <= k <= n for which the
greatest common divisor gcd( n, k ) is equal to 1.  The integers k of this form
are sometimes referred to as totatives of n.

For example, the totatives of n = 9 are the six numbers 1, 2, 4, 5, 7 and 8.
They are all relatively prime to 9, but the other three numbers in this range,
3, 6, and 9 are not, since gcd( 9, 3 ) = gcd( 9, 6 ) = 3 and gcd( 9, 9 ) = 9.
Therefore, phi( 9 ) = 6.  As another example, phi( 1 ) = 1 since for n = 1 the
only integer in the range from 1 to n is 1 itself, and gcd( 1, 1 ) = 1.

Euler's totient function is a multiplicative function, meaning that if two
numbers m and n are relatively prime, then phi( mn ) = phi( m ) phi( n ).  This
function gives the order of the multiplicative group of integers modulo n (the
group of units of the ring ℤ/nℤ).  It is also used for defining the RSA
encryption system.
''',
'''
''' + makeCommandExample( '17 euler_phi' ) + '''
''' + makeCommandExample( '48 euler_phi' ) + '''
''' + makeCommandExample( '17 48 * euler_phi' ) + '''
''' + makeCommandExample( '1 20 range euler_phi' ),
[ 'sigma', 'factor' ] ],

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
This operator calculates the product of all whole numbers from 1 to n.  It is
also capable of calculating the analytical generalization of the factorial
function to non-integer and complex numbers.
''',
'''
''' + makeCommandExample( '1 10 range factorial' ) + '''
''' + makeCommandExample( '4.5 factorial' ) + '''
''' + makeCommandExample( '3 2j - factorial' ),
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
'number_theory', 'calculates the largest x for which the sum of the first x cubes is less than or equal to n',
'''
This operator calculates the largest value x, for which the sum of the first x
cubes is less than or equal to n.
''',
'''
''' + makeCommandExample( '3025 find_sum_of_cubes' ) + '''
''' + makeCommandExample( '11025 find_sum_of_cubes' ),
[ 'find_sum_of_squares' ] ],

    'find_sum_of_squares' : [
'number_theory', 'calculates the largest x for which the sum of the first x squares is less than n',
'''
This operator calculates the largest value x, for which the sum of the first x
squares is less than or equal to n.
''',
'''
''' + makeCommandExample( '55 find_sum_of_squares' ) + '''
''' + makeCommandExample( '506 find_sum_of_squares' ),
[ 'find_sum_of_cubes' ] ],

    'fraction' : [
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
This operator calculates a rational approximation of n using k terms of the
continued fraction representation of n.   It returns a list of two values,
signifying the numerator and denominator of the approximation.

It is necessary to make sure the accuracy (-a) is set high enough for a correct
result.

TODO: auto-precision?
''',
'''
''' + makeCommandExample( '2 sqrt 10 fraction' ) + '''
''' + makeCommandExample( '-a20 2 sqrt 20 fraction' ) + '''
''' + makeCommandExample( 'pi 4 fraction' ) + '''
''' + makeCommandExample( '-a30 pi 20 fraction' ),
[ 'make_continued_fraction', 'continued_fraction' ] ],

    'frobenius' : [
'number_theory', 'calculates the frobenius number of a list of values with gcd > 1',
'''
The Frobenius number is the largest number that is not a linear combination of
a list of operands.  The list of operands must have a greatest common
denominator of 1.

It is commonly associated with Chicken McNuggets from McDonalds, which are
sold in packages of 6, 9 and 20.   The Frobenius number for Chicken McNuggets
is 43, meaning that 43 is the largest number of McNuggets that cannot be
ordered with combinations of 6, 9 or 20 pieces.
''',
'''
''' + makeCommandExample( '[ 6 9 20 ] frobenius' ) + '''
''' + makeCommandExample( '[ 9 20 ] frobenius' ) + '''
''' + makeCommandExample( '[ 5 12 ] frobenius' ),
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
This operator generates all the polydivisible numbers for base n.

From https://en.wikipedia.org/wiki/Polydivisible_number:

In mathematics a polydivisible number (or magic number) is a number in a given
number base with digits abcde... that has the following properties:

Its first digit a is not 0.
The number formed by its first two digits ab is a multiple of 2.
The number formed by its first three digits abc is a multiple of 3.
The number formed by its first four digits abcd is a multiple of 4.
etc.
''',
'''
''' + makeCommandExample( '2 generate_polydivisibles' ) + '''
''' + makeCommandExample( '3 generate_polydivisibles' ),
[ 'is_polydivisible' ] ],

    'geometric_recurrence' : [
'number_theory', 'calculates the dth value of a geometric recurrence specified by a list of factors (a), powers (b) and of seeds (c)',
'''
This operator calculates the dth value of a geometric recurrence specified by a
list of factors (a), powers (b) and of seeds (c).

The factors (a) indicate the multiple of each preceding value to add to create
the next value in the recurrence list, listed from right to left (meaning the
last factor corresponds to the (n - 1)th value in the sequence.

The seeds (c), simply specify a list of initial values.  The number of seeds
cannot exceed the number of factors, but there may be fewer seeds.
''',
'''
''' + makeCommandExample( '2 generate_polydivisibles' ) + '''
''' + makeCommandExample( '3 generate_polydivisibles' ),
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
The Heptanacci sequence is a generalization of the Fibonacci sequence, starting
with: 0, 0, 0, 0, 0, 0, 1, and where each successive value is the sum of the
previous seven terms.
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
The Hexanacci sequence is a generalization of the Fibonacci sequence, starting
with: 0, 0, 0, 0, 0, 1, and where each successive value is the sum of the
previous six terms.
''',
'''
The first several hexanacci numbers:
''' + makeCommandExample( '1 20 range hexanacci', indent=4 ) + '''
The Hexanacci constant:
''' + makeCommandExample( 'infinity lambda x 5 + hexanacci x 4 + hexanacci / limit', indent=4 ),
[ 'fibonacci' ] ],

    'hurwitz_zeta' : [
'number_theory', 'calculates the Hurwitz zeta function for n and k',
'''
This operator calculates the Hurwitz zeta function for n and k.

From https://en.wikipedia.org/wiki/Hurwitz_zeta_function:

In mathematics, the Hurwitz zeta function, named after Adolf Hurwitz, is one of
the many zeta functions.  It is formally defined for complex arguments s with
Re(s) > 1 and q with Re(q) > 0 by

                inf
                ---         1
zeta( n, k ) =  \\      -----------
                /      ( x + k )^n
                ---
               x = 0

This series is absolutely convergent for the given values of n and k and can be
extended to a meromorphic function defined for all s != 1.  The Riemann zeta
function is zeta( n, 1 ).=
''',
'''
''' + makeCommandExample( '2 3 hurwitz_zeta' ) + '''
''' + makeCommandExample( '3 3 hurwitz_zeta' ) + '''
''' + makeCommandExample( '3 3 4j - hurwitz_zeta' ),
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
[ 'is_powerful', 'is_perfect' ] ],

    'is_antiharmonic' : [
'number_theory', 'returns whether or not n is an antiharmonic number',
'''
A number is antiharmonic if the sum of the squares of its divisors divides the
sum of its divisors.
''',
'''
The first several antiharmonic numbers:
''' + makeCommandExample( '1 150 range lambda x is_antiharmonic filter' ),
[ 'divisors' ] ],

    'is_carmichael' : [
'number_theory', 'returns whether n is a Carmichael number',
'''
From https://en.wikipedia.org/wiki/Carmichael_number:

In number theory, a Carmichael number is a composite number n which satisfies
the modular arithmetic congruence relation:  b^(n-1) equiv 1 (mod n)

for all integers b which are relatively prime to n.  They are named for Robert
Carmichael.

Equivalently, a Carmichael number is a composite number n for which

b^n equiv b (mod n).
''',
'''
''' + makeCommandExample( '1 10000 range lambda x is_carmichael filter' ),
[ 'gcd', 'modulo' ] ],

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

    'is_sociable_list' : [
'number_theory', 'returns whether list n is a list of sociable numbers',
''';
This operator returns true (1) if the list n is a list of sociable numbers.
Sociable numbers form a looped aliquot chain:  The sum of divisors of each
numbers is the next number in the list, with the last number having a divisor
sum that equals the first number.

Therefore, if any of these numbers are used with the 'aliquot' operator, they
will result in early termination because of a loop.
''',
'''
''',
[ 'sigma', 'aliquot' ] ],

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
This operator returns true (1) whether an integer n is k hyperperfect, otherwise
false (0).

From https://en.wikipedia.org/wiki/Hyperperfect_number:

In mathematics, a k-hyperperfect number is a natural number n for which the
equality n = 1 + k( sigma( n ) − n − 1 ) holds, where sigma( n ) is the divisor
function (i.e., the sum of all positive divisors of n).  A hyperperfect number
is a k-hyperperfect number for some integer k.  Hyperperfect numbers generalize
perfect numbers, which are 1-hyperperfect.
''',
'''
''' + makeCommandExample( '7056410014866537089009269921 12 is_k_hyperperfect' ) + '''
''' + makeCommandExample( '42052982615431201 18 is_k_hyperperfect' ) + '''
''' + makeCommandExample( '47268697363953913 2772 is_k_hyperperfect' ),
[ 'is_k_perfect', 'is_perfect' ] ],

    'is_k_perfect' : [
'number_theory', 'returns whether an integer n is k-perfect',
'''
This operator returns whether an integer n is k-perfect.

From https://en.wikipedia.org/wiki/Multiply_perfect_number:

In mathematics, a multiply perfect number (also called multiperfect number or
pluperfect number) is a generalization of a perfect number.

For a given natural number k, a number n is called k-perfect (or k-fold perfect)
if and only if the sum of all positive divisors of n (the divisor function,
sigma( n ) is equal to kn; a number is thus perfect if and only if it is
2-perfect.  A number that is k-perfect for a certain k is called a multiply
perfect number.  As of 2014, k-perfect numbers are known for each value of k up to 11.[1]
''',
'''
''' + makeCommandExample( '6 2 is_k_perfect' ) + '''
''' + makeCommandExample( '8128 2 is_k_perfect' ) + '''
''' + makeCommandExample( '672 3 is_k_perfect' ) + '''
''' + makeCommandExample( '14182439040 5 is_k_perfect' ) + '''
''' + makeCommandExample( '154345556085770649600 6 is_k_perfect' ) + '''
''' + makeCommandExample( '141310897947438348259849402738485523264343544818565120000 7 is_k_perfect' ),
[ 'is_k_hyperperfect', 'is_perfect' ] ],

    'is_k_polydivisible' : [
'number_theory', 'returns whether or not n is base-k polydivisible',
'''
This operator returns whether or not n is a base-k polydivisible number.

From https://en.wikipedia.org/wiki/Polydivisible_number:

In mathematics a polydivisible number (or magic number) is a number in a given
number base with digits abcde... that has the following properties:

Its first digit a is not 0.
The number formed by its first two digits ab is a multiple of 2.
The number formed by its first three digits abc is a multiple of 3.
The number formed by its first four digits abcd is a multiple of 4.
...
''',
'''
''' + makeCommandExample( '1 1000 range lambda x 3 is_k_polydivisible filter' ) + '''
''' + makeCommandExample( '1 200 range lambda x 4 is_k_polydivisible filter' ) + '''
''' + makeCommandExample( '100 150 range lambda x 10 is_k_polydivisible filter' ),
[ 'is_divisible', 'generate_polydivisibles' ] ],

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

''' + makeCommandExample( '1 100 range lambda x 3 is_k_sphenic filter' ) + '''
Let's contrast that with the 3-semiprime numbers:
''' + makeCommandExample( '1 100 range lambda x 3 is_k_semiprime filter' ) + '''
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
[ 'parity', 'count_bits' ] ],

    'is_polydivisible' : [
'number_theory', 'returns whether or not n is polydivisible',
'''
From https://en.wikipedia.org/wiki/Polydivisible_number:

In mathematics a polydivisible number (or magic number) is a number in a given
number base with digits abcde... that has the following properties:

Its first digit a is not 0.
The number formed by its first two digits ab is a multiple of 2.
The number formed by its first three digits abc is a multiple of 3.
The number formed by its first four digits abcd is a multiple of 4.
...

This operator works only with base 10.  For other bases, use
'is_k_polydivisible'.
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
From https://en.wikipedia.org/wiki/Ruth–Aaron_pair:

In mathematics, a Ruth–Aaron pair consists of two consecutive integers (e.g.,
714 and 715) for which the sums of the prime factors of each integer are equal:

714 = 2 × 3 × 7 × 17,
715 = 5 × 11 × 13,

and

2 + 3 + 7 + 17 = 5 + 11 + 13 = 29.

This operator returns 1 if n is the smaller number of a Ruth-Aaron pair, along
with n + 1.

The name was given by Carl Pomerance for Babe Ruth and Hank Aaron, as Ruth's
career regular-season home run total was 714, a record which Aaron eclipsed on
April 8, 1974, when he hit his 715th career home run.  Pomerance was a
mathematician at the University of Georgia at the time Aaron (a member of the
nearby Atlanta Braves) broke Ruth's record, and the student of one of
Pomerance's colleagues noticed that the sums of the prime factors of 714 and 715
were equal.
''',
'''
''' + makeCommandExample( '1 1000 range lambda x is_ruth_aaron filter' ),
[ 'sigma', 'aliquot' ] ],

    'is_semiprime' : [
'number_theory', 'returns whether n is a semiprime number',
'''
A semiprime number is a number that has two unique prime factors.

This concept can be generalized to any number, and that is implemented in the
'is_k_sphenic' operator.
''',
'''
''' + makeCommandExample( '1 20 range lambda x is_semiprime filter' ) + '''
''' + makeCommandExample( '1 20 range lambda x is_semiprime filter factor -s1' ) + '''
''' + makeCommandExample( '71 97 * is_semiprime' ) + '''
''' + makeCommandExample( '[ 71 97 107 ] product is_semiprime' ),
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
A sphenic number is a number that has three unique prime factors.

This concept can be generalized to any number, and that is implemented in the
'is_k_sphenic' operator.
''',
'''
''' + makeCommandExample( '1 100 range lambda x is_sphenic filter' ) + '''
''' + makeCommandExample( '1 100 range lambda x is_sphenic filter factor -s1' ) + '''
''' + makeCommandExample( '71 97 * is_sphenic' ) + '''
''' + makeCommandExample( '[ 71 97 107 ] product is_sphenic' ),
[ 'is_k_sphenic', 'is_semiprime', 'is_prime' ] ],

    'is_squarefree' : [
'number_theory', 'returns whether n is a square-free number',
'''
A square-free number is a number that only has unique prime factors.
''',
'''
''' + makeCommandExample( '1 25 range lambda x is_squarefree filter' ),
[ 'is_semiprime', 'is_pronic', 'nth_mobius' ] ],

    'is_strong_pseudoprime' : [
'number_theory', 'returns whether n is a strong pseudoprime to base k',
'''
From https://en.wikipedia.org/wiki/Strong_pseudoprime:

A strong pseudoprime is a composite number that passes the Miller–Rabin
primality test.  All prime numbers pass this test, but a small fraction of
composites also pass.

Unlike the Fermat pseudoprimes, for which there exist numbers that are
pseudoprimes to all coprime bases (the Carmichael numbers), there are no
composites that are strong pseudoprimes to all bases.
''',
'''
''' + makeCommandExample( '74593 3 is_strong_pseudoprime' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 4 is_strong_pseudoprime filter' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 5 is_strong_pseudoprime filter' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 15 is_strong_pseudoprime filter' ) + '''
''' + makeCommandExample( '1 10000 range lambda x 347 is_strong_pseudoprime filter' ),
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
This operator allows for an arbitrary generalization of the Fibonacci sequence.
The sequence of numbers generated starts with k - 1 zeroes, and a 1 with each
successive value being the sum of the previous k terms.

The nth Fibonacci number can be obtained with "n 2 k_fibonacci".  The nth
Tribonacci number can be obtained with "n 3 k_fibonacci", etc.
''',
'''
''' + makeCommandExample( '1 10 range 2 k_fibonacci' ) + '''
''' + makeCommandExample( '1 10 range 3 k_fibonacci' ) + '''
''' + makeCommandExample( '10 2 10 range k_fibonacci' ),
[ 'fibonacci' ] ],

    'leyland_number' : [
'number_theory', 'returns the Leyland number for n and k',
'''
From https://en.wikipedia.org/wiki/Leyland_number:

In number theory, a Leyland number is a number of the form x^y + y^x where x and
y are integers greater than 1.  They are named after the mathematician Paul
Leyland.  The first few Leyland numbers are

8, 17, 32, 54, 57, 100, 145, 177, 320, 368, 512, 593, 945, 1124...

The requirement that x and y both be greater than 1 is important, since without
it every positive integer would be a Leyland number of the form x1 + 1x.  Also,
because of the commutative property of addition, the condition x >= y is usually
added to avoid double-covering the set of Leyland numbers (so we have 1 < y <=
x).
''',
'''
''' + makeCommandExample( '2 3 leyland_number' ) + '''
''' + makeCommandExample( '4 5 leyland_number' ) + '''
''' + makeCommandExample( '14 27 leyland_number' ) + '''
The first 15 Leyland numbers in order:
''' + makeCommandExample( '2 10 range lambda 2 x range x leyland_number eval flatten sort 15 left' ),
[ 'nth_carol', 'nth_kynea' ] ],

    'log_gamma' : [
'number_theory', 'calculates the loggamma function for n',
'''
The logarithm of the gamma function is treated as a special function.

This operator computes the principal branch of the log-gamma function, which has
infinitely many complex branch cuts, the principal log-gamma function only has a
single branch cut along the negative half-axis.
''',
'''
''' + makeCommandExample( '0.1 loggamma' ) + '''
''' + makeCommandExample( '1 loggamma' ) + '''
''' + makeCommandExample( '3 loggamma' ) + '''
''' + makeCommandExample( '-1.5 loggamma' ) + '''
''' + makeCommandExample( '3 4j +' ) + '''
''' + makeCommandExample( '1e3000j loggamma' ),
[ 'log', 'gamma' ] ],

    'linear_recurrence' : [
'number_theory', 'calculates the first c values of a linear recurrence specified by factors (a) and seeds (b)',
'''
This operator calculates the first c values of a linear recurrence specified by
a list of factors (a) and a list of seeds (b).

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
'number_theory', 'calculates the first c values of a linear recurrence specified by factors (a) and seeds (b), modulo d',
'''
This operator calculates the first c values of a linear recurrence specified by
a list of factors (a) and a list of seeds (b),  where each successive result is
taken modulo d.

The factors (a) indicate the multiple of each preceding value to add to create
the next value in the recurrence list, listed from right to left (meaning the
last factor corresponds to the n - 1'th value in the sequence.  For the
Fibonacci or Lucas lists, this would be [ 1 1 ], meaning the previous value,
plus the one before that.  The tribonacci sequence would have a factor list of
[ 1 1 1 ].

The seeds (b), simply specify a list of initial values.  The number of seeds
cannot exceed the number of factors, but there may be fewer seeds.
''',
'''
The Fibonacci sequence modulo 100:
''' + makeCommandExample( '[ 1 1 ] [ 0 1 ] 18 100 linear_recurrence_with_modulo' ) + '''
The Lucas Sequence modulo 100:
''' + makeCommandExample( '[ 1 1 ] [ 1 3 ] 17 100 linear_recurrence_with_modulo' ),
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
This operator calculates k terms of the continued fraction representation of n.

It is necessary to make sure the accuracy (-a) is set high enough for a correct
answer.   TODO:  Do this automatically?

From https://en.wikipedia.org/wiki/Continued_fraction:

In mathematics, a continued fraction is an expression obtained through an
iterative process of representing a number as the sum of its integer part and
the reciprocal of another number, then writing this other number as the sum of
its integer part and another reciprocal, and so on.  In a finite continued
fraction (or terminated continued fraction), the iteration/recursion is
terminated after finitely many steps by using an integer in lieu of another
continued fraction.  In contrast, an infinite continued fraction is an infinite
expression.  In either case, all integers in the sequence, other than the first,
must be positive.  The integers are called the coefficients or terms of the
continued fraction.
''',
'''
''' + makeCommandExample( '-a20 2 sqrt 10 make_continued_fraction' ) + '''
''' + makeCommandExample( '-a20 pi 10 make_continued_fraction' ),
[ 'continued_fraction' ] ],

    'make_pyth_3' : [
'number_theory', 'makes a pythagorean triple given two integers, n and k, as seeds',
'''
This operator makes a pythagorean triple given two integers, n and k, as seeds.

From https://en.wikipedia.org/wiki/Pythagorean_triple:

A Pythagorean triple consists of three positive integers a, b, and c, such that
a^2 + b^2 = c^2.  Such a triple is commonly written (a, b, c), and a well-known
example is (3, 4, 5).  If (a, b, c) is a Pythagorean triple, then so is
(ka, kb, kc) for any positive integer k.  A primitive Pythagorean triple is one
in which a, b and c are coprime (that is, they have no common divisor larger
than 1).  A triangle whose sides form a Pythagorean triple is called a
Pythagorean triangle, and is necessarily a right triangle.
''',
'''
''' + makeCommandExample( '1 2 make_pyth_3' ) + '''
''' + makeCommandExample( '1 4 make_pyth_3' ) + '''
''' + makeCommandExample( '25 67 make_pyth_3' ),
[ 'make_pyth_4', 'hypotenuse', 'pythagorean_triples' ] ],

    'make_pyth_4' : [
'number_theory', 'makes a pythagorean quadruple given two integers, n and k, as seeds',
'''
This makes a pythagorean quadruple given two integers, n and k, as seeds.  n and
k cannot both be odd.

https://en.wikipedia.org/wiki/Pythagorean_quadruple:

A Pythagorean quadruple is a tuple of integers a, b, c and d, such that a^2 +
b^2 + c^2 = d^2.  They are solutions of a Diophantine equation and often only
positive integer values are considered.  However, to provide a more complete
geometric interpretation, the integer values can be allowed to be negative and
zero (thus allowing Pythagorean triples to be included) with the only condition
being that d > 0.  In this setting, a Pythagorean quadruple (a, b, c, d) defines
a cuboid with integer side lengths |a|, |b|, and |c|, whose space diagonal has
integer length d; with this interpretation, Pythagorean quadruples are thus also
called Pythagorean boxes.

rpnChilada will only generate Pythagorean quadruple with all positive integers.
''',
'''
''' + makeCommandExample( '1 2 make_pyth_4' ) + '''
''' + makeCommandExample( '1 4 make_pyth_4' ) + '''
''' + makeCommandExample( '24 67 make_pyth_4' ),
[ 'make_pyth_3', 'hypotenuse' ] ],

    'nth_carol' : [
'number_theory', 'gets the nth Carol number',
'''
From https://en.wikipedia.org/wiki/Carol_number:

A Carol number is an integer of the form 4^n - 2^n+1 - 1, or equivalently
(2^n - 1)^2.   The first few Carol numbers are: −1, 7, 47, 223, 959, 3967,
16127, 65023, 261119, 1046527, ...

The numbers were first studied by Cletus Emmanuel, who named them after a
friend, Carol G. Kirnon.

For n > 2, the binary representation of the n-th Carol number is n − 2
consecutive ones, a single zero in the middle, and n + 1 more consecutive ones.

''',
'''
''' + makeCommandExample( '1 20 range nth_carol' ) + '''
''' + makeCommandExample( '25337 nth_carol' ),
[ 'nth_thabit', 'nth_kynea' ] ],

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

    'nth_jacobsthal' : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
From https://en.wikipedia.org/wiki/Jacobsthal_number:

In mathematics, the Jacobsthal numbers are an integer sequence named after the
German mathematician Ernst Jacobsthal.  Like the related Fibonacci numbers, they
are a specific type of Lucas sequence U sub n(P,Q) for which P = 1, and Q = −2 -
and are defined by a similar recurrence relation:  in simple terms, the sequence
starts with 0 and 1, then each following number is found by adding the number
before it to twice the number before that.  The first Jacobsthal numbers are:

0, 1, 1, 3, 5, 11, 21, 43, 85, 171, 341, 683, 1365, 2731, 5461, 10923, 21845,
43691, 87381, 174763, 349525, ...
''',
'''
''' + makeCommandExample( '1 20 range nth_jacobsthal' ) + '''
''' + makeCommandExample( '4783 nth_jacobsthal' ),
[ 'fibonacci', 'lucas' ] ],

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
[ 'nth_mersenne_prime', 'nth_carol', 'nth_jacobsthal', 'leyland_number' ] ],

    'nth_k_thabit' : [
'number_theory', 'gets the nth base k Thabit number',
'''
From https://en.wikipedia.org/wiki/Thabit_number:

In number theory, a Thabit number, Thâbit ibn Kurrah number, or 321 number is
an integer of the form 3 * 2^n - 1 for a non-negative integer n.

The 9th Century mathematician, physician, astronomer and translator Thābit ibn
Qurra is credited as the first to study these numbers and their relation to
amicable numbers.

For integer b >= 2, a Thabit number base b is a number of the form
( b + 1 ) * b^n − 1 for a non-negative integer n.  Also, for integer b >= 2, a
Thabit number of the second kind base b is a number of the form
( b + 1 ) * b^n + 1 for a non-negative integer n.
''',
'''
''' + makeCommandExample( '1 20 range 2 nth_k_thabit' ) + '''
''' + makeCommandExample( '1 15 range 3 nth_k_thabit' ) + '''
''' + makeCommandExample( '1 10 range 4 nth_k_thabit' ) + '''
''' + makeCommandExample( '23 6 nth_k_thabit' ),
[ 'nth_thabit', 'nth_thabit_2', 'nth_k_thabit_2' ] ],

    'nth_k_thabit_2' : [
'number_theory', 'gets the nth base k Thabit number of the second kind',
'''
From https://en.wikipedia.org/wiki/Thabit_number:

In number theory, a Thabit number, Thâbit ibn Kurrah number, or 321 number is
an integer of the form 3 * 2^n - 1 for a non-negative integer n.

The 9th Century mathematician, physician, astronomer and translator Thābit ibn
Qurra is credited as the first to study these numbers and their relation to
amicable numbers.

For integer b >= 2, a Thabit number base b is a number of the form
( b + 1 ) * b^n − 1 for a non-negative integer n.  Also, for integer b >= 2, a
Thabit number of the second kind base b is a number of the form
( b + 1 ) * b^n + 1 for a non-negative integer n.
''',
'''
''' + makeCommandExample( '1 20 range 2 nth_k_thabit_2' ) + '''
''' + makeCommandExample( '1 15 range 3 nth_k_thabit_2' ) + '''
''' + makeCommandExample( '1 10 range 4 nth_k_thabit_2' ) + '''
''' + makeCommandExample( '15 7 nth_k_thabit_2' ),
[ 'nth_thabit', 'nth_thabit_2', 'nth_k_thabit' ] ],

    'nth_linear_recurrence' : [
'number_theory', 'calculates the cth value of a linear recurrence for factors a and seeds b',
'''
This operator calculates the cth value of a linear recurrence specified by a
list of factors (a) and of seeds (b).

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
'number_theory', 'calculates the cth value of a linear recurrence for factors a, seeds b, modulo d',
'''
This operator calculates the cth value of a linear recurrence specified by a
list of factors (a) and of seeds (b), where each successive result is taken
modulo d.

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

This allows for the calculation of linear recurrences when only a modular
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
are 0 and 1, and each subsequent value is calculated by:

L( n ) = L( n - 1 ) + L( n - 2 ) + 1

rpn calculates the nth Leonardo number using the following formula, where
F( n ) is the nth Fibonacci number:

L( n ) = 2F( n + 1 ) - 1
''',
'''
''' + makeCommandExample( '1 20 range nth_leonardo' ),
[ 'fibonacci', 'lucas', 'nth_jacobsthal' ] ],

    'nth_mersenne_exponent' : [
'number_theory', 'returns the exponent in the nth Mersenne prime',
'''
These values are stored in a look-up table.  They are not calculated.  :-)

There are currently ''' + str( len( mersennePrimeExponents ) ) + ''' known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.

https://primes.utm.edu/mersenne/index.html
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_mersenne_exponent' ) + '''
''' + makeCommandExample( str( len( mersennePrimeExponents ) ) + ' nth_mersenne_exponent' ),
[ 'nth_mersenne_prime', 'nth_perfect_number' ] ],

    'nth_mersenne_prime' : [
'number_theory', 'returns the nth known Mersenne prime',
'''
These values are stored in a look-up table.  They are not calculated.  :-)

There are currently ''' + str( len( mersennePrimeExponents ) ) + ''' known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.

https://primes.utm.edu/mersenne/index.html
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_mersenne_prime' ) + '''
''' + makeCommandExample( str( len( mersennePrimeExponents ) ) + ' nth_mersenne_prime' ),
[ 'nth_mersenne_exponent', 'nth_perfect_number' ] ],

    'nth_merten' : [
'number_theory', 'returns Merten\'s function for n',
'''
From https://en.wikipedia.org/wiki/Mertens_function:

In number theory, the Mertens function is defined for all positive integers n as

           n
         ------
          \\
M( n ) =   \\     mu( k )
          /
         ------
         k = 1

where mu( k ) is the Moebius function.  The function is named in honour of Franz
Mertens.

Less formally, M( x ) is the count of square-free integers up to x that have an
even number of prime factors, minus the count of those that have an odd number.
''',
'''
''' + makeCommandExample( '1 20 range nth_merten' ) + '''
''' + makeCommandExample( '3563 nth_merten' ),
[ 'nth_mobius' ] ],

    'nth_mobius' : [
'number_theory', 'calculates the Mobius function for n',
'''
https://en.wikipedia.org/wiki/M%C3%B6bius_function

The classical Moebius function mu(n) is an important multiplicative function in
number theory and combinatorics.  The German mathematician August Ferdinand
Moebius introduced it in 1832.  It is a special case of a more general object in
combinatorics.

For any positive integer n, define mu(n) as the sum of the primitive nth roots
of unity.  It has values in {−1, 0, 1} depending on the factorization of n into
prime factors:

mu(n) = 1 if n is a square-free positive integer with an even number of prime
factors.

mu(n) = −1 if n is a square-free positive integer with an odd number of prime
factors.

mu(n) = 0 if n has a squared prime factor.
''',
'''
''' + makeCommandExample( '1 20 range nth_mobius' ) + '''
''' + makeCommandExample( '4398 nth_mobius' ),
[ 'factor', 'is_squarefree', 'nth_merten' ] ],

    'nth_padovan' : [
'number_theory', 'calculates the nth Padovan number',
'''
The Padovan sequence is the sequence of integers P(n) defined by the initial
values:

    P( 0 ) = P( 1 ) = P( 2 ) = 1

and the recurrence relation

    P( n ) = P( n - 2 ) + P( n - 3 ).

The Padovan numbers can be computed by rpn using the 'linear_recurrence'
functionality, but OEIS (http://oeis.org/A000931) provides a non-iterative
formula.
''',
'''
''' + makeCommandExample( '1 20 range nth_padovan' ) + '''
''' + makeCommandExample( '1 100 range nth_padovan lambda x is_prime filter' ),
[ 'fibonacci', 'lucas' ] ],

    'nth_perfect_number' : [
'number_theory', 'returns the nth known perfect number',
'''
These values are stored in a look-up table.  They are not calculated.  :-)

The nth known perfect number is computed from the nth known Mersenne prime.
There are currently ''' + str( len( mersennePrimeExponents ) ) + ''' known Mersenne primes.  This list is subject to change
as new Mersenne Primes are being actively searched for.
''',
'''
''' + makeCommandExample( '-a30 1 10 range nth_perfect_number' ) + '''
''' + makeCommandExample( str( len( mersennePrimeExponents ) ) + ' nth_perfect_number' ),
[ 'is_perfect', 'nth_mersenne_exponent' ] ],

    'nth_stern' : [
'number_theory', 'calculates the nth value of the Stern diatomic series',
'''
Stern's diatomic sequence is the integer sequence

0, 1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5, 2, 5, 3, 4, ...

Using zero-based numbering, the nth value in the sequence is the value fusc(n)
of the fusc function, named according to the obfuscating appearance of the
 sequence of values and defined by the recurrence relations

fusc⁡( 2n ) = fusc⁡( n )
fusc⁡( 2n + 1 ) = fusc⁡( n ) + fusc⁡( n + 1 ),

with the base cases fusc( 0 ) = 0 and fusc( 1 ) = 1.

The nth rational number in a breadth-first traversal of the Calkin–Wilf tree is
the number:

 fusc( n )
 ----------
fusc( n + 1 )

Thus, the diatomic sequence forms both the sequence of numerators and the
sequence of denominators of the numbers in the Calkin–Wilf sequence.
''',
'''
''' + makeCommandExample( '1 20 range nth_stern' ) + '''
''' + makeCommandExample( '223800 223810 range nth_stern' ),
[ 'calkin_wilf' ] ],

    'nth_thabit' : [
'number_theory', 'gets the nth Thabit number',
'''
From https://en.wikipedia.org/wiki/Thabit_number:

In number theory, a Thabit number, Thâbit ibn Kurrah number, or 321 number is
an integer of the form 3 * 2^n - 1 for a non-negative integer n.

The 9th Century mathematician, physician, astronomer and translator Thābit ibn
Qurra is credited as the first to study these numbers and their relation to
amicable numbers.

The binary representation of the Thabit number 3 * 2^n − 1 is n + 2 digits
long, consisting of "10" followed by n 1s.
''',
'''
''' + makeCommandExample( '1 20 range nth_thabit' ) + '''
''' + makeCommandExample( '2375 nth_thabit' ),
[ 'nth_thabit', 'nth_thabit_2', 'nth_k_thabit_2', 'nth_carol' ] ],

    'nth_thabit_2' : [
'number_theory', 'gets the nth Thabit number of the second kind',
'''
From https://en.wikipedia.org/wiki/Thabit_number:

In number theory, a Thabit number, Thâbit ibn Kurrah number, or 321 number is
an integer of the form 3 * 2^n - 1 for a non-negative integer n.  The nth Thabit
number of the second kind is of the form 3 * 2^n + 1.

The 9th Century mathematician, physician, astronomer and translator Thābit ibn
Qurra is credited as the first to study these numbers and their relation to
amicable numbers.
''',
'''
''' + makeCommandExample( '1 20 range nth_thabit_2' ) + '''
''' + makeCommandExample( '168 nth_thabit_2' ),
[ 'nth_thabit', 'nth_thabit_2', 'nth_k_thabit' ] ],

    'nth_thue_morse' : [
'number_theory', 'calculates the nth value of the Thue-Morse sequence',
'''
From https://en.wikipedia.org/wiki/Thue–Morse_sequence:

In mathematics, the Thue–Morse sequence, or Prouhet–Thue–Morse sequence, is the
binary sequence (an infinite sequence of 0s and 1s) obtained by starting with 0
and successively appending the Boolean complement of the sequence obtained thus
far.  The first few steps of this procedure yield the strings 0 then 01, 0110,
01101001, 0110100110010110, and so on, which are prefixes of the Thue–Morse
sequence.  The full sequence begins:

01101001100101101001011001101001...

The sequence is named after Axel Thue and Marston Morse.

In their book on the problem of fair division, Steven Brams and Alan Taylor
invoked the Thue–Morse sequence but did not identify it as such.  When
allocating a contested pile of items between two parties who agree on the items'
relative values, Brams and Taylor suggested a method they called balanced
alternation, or taking turns taking turns taking turns... , as a way to
circumvent the favoritism inherent when one party chooses before the other.  An
example showed how a divorcing couple might reach a fair settlement in the
distribution of jointly-owned items.  The parties would take turns to be the
first chooser at different points in the selection process:  Ann chooses one
item, then Ben does, then Ben chooses one item, then Ann does.
''',
'''
The first 20 members of the Thue Morse sequence:
''' + makeCommandExample( '1 20 range nth_thue_morse', indent=4 ),
[ 'debruijn_sequence' ] ],

    'octanacci' : [
'number_theory', 'calculates the nth Octanacci number',
'''
The Fibonacci sequence can be generalized by adding more than two terms to
create the next successive term.  Under this generalization, the starting values
of a k-fibonacci sequence are made up of k-1 zeroes and a one, and each
successive value is calculated by summing the k previous values.

The octanacci sequence is the name given to the 8-fibonacci sequence.
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
The operator calculates the nth line of Pascal\'s triangle and returns a list of
the values.

From https://en.wikipedia.org/wiki/Pascal%27s_triangle:

In mathematics, Pascal's triangle is a triangular array of the binomial
coefficients.  In much of the Western world, it is named after the French
mathematician Blaise Pascal, although other mathematicians studied it centuries
before him in India, Persia (Iran), China, Germany, and Italy.

The rows of Pascal's triangle are conventionally enumerated starting with row
n = 0 at the top (the 0th row).  The entries in each row are numbered from the
left beginning with k = 0 and are usually staggered relative to the numbers in
the adjacent rows.  The triangle may be constructed in the following manner:
In row 0 (the topmost row), there is a unique nonzero entry 1.  Each entry of
each subsequent row is constructed by adding the number above and to the left
with the number above and to the right, treating blank entries as 0.  For
example, the initial number in the first (or any other) row is 1 (the sum of 0
and 1), whereas the numbers 1 and 3 in the third row are added to produce the
number 4 in the fourth row.
''',
'''
The first 10 lines of Pascal's triangle:
''' + makeCommandExample( '1 10 range pascal_triangle -s1' ),
[ 'nth_catalan' ] ],

    'pentanacci' : [
'number_theory', 'calculates the nth Pentanacci number',
'''
The Pentanacci sequence is a generalization of the Fibonacci sequence, starting
with: 0, 0, 0, 0, 1, and where each successive value is the sum of the previous
five terms.
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
From https://en.wikipedia.org/wiki/Polygamma_function:

In mathematics, the polygamma function of order m is a meromorphic function on
the complex numbers C defined as the (m + 1)th derivative of the logarithm of
the gamma function.

The operator returns the polygamma function of order n for the value k.
''',
'''
''' + makeCommandExample( '5 6 polygamma' ) + '''
''' + makeCommandExample( '0 5 range 10 polygamma' ),
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
THis operator calculates whether or not n and k are relatively prime, returning
1 if they are, and 0 if they are not.

Numbers are relatively prime if their greatest common denominator is 1.
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
THis operator returns the sum of the proper divisors of n.   The proper divisors
include 1 and n, as well as all other divisors of n.
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
This operator is a generalization of the 'sigma' operator where the divisors are
raised to the power of k before being summed.
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
This operator is explicit version of 'count_frobenius' in that it actually
enumerates the different ways items described by the coefficients of n can be
combined to create a total of k.

'count_frobenius' returns how many different ways the items can be combined.
'solve_frobenius' actually shows all the solutions.
''',
'''
The Chicken McNugget problem appears again.  List the ways to make an order of 42 McNuggets:
''' + makeCommandExample( '[ 6 9 20 ] 42 solve_frobenius -s1' ) + '''
List the ways to make 17 cents with pennies, nickels and dimes:
''' + makeCommandExample( '[ 1 5 10 ] 17 solve_frobenius' ),
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
'number_theory', 'calculates every combination of b cth powers that sum to a',
'''
This operator calculates every combination of b cth powers that sum to a.

This version of the operator allows the results to be zero, so that if there are
fewer than b cth powers can add up to a, they will be included as well.
''',
'''
''' + makeCommandExample( '5104 3 3 sums_of_k_powers' ),
[ 'sums_of_k_nonzero_powers' ] ],

    'sums_of_k_nonzero_powers' : [
'number_theory', 'calculates every combination of b nonzero cth powers that sum to a',
'''
THis operator calculates every combination of b nonzero cth powers of positive
integers that sum to a.

The name of the operator adheres to the rpnChilada standard that two-argument
operators have arguments named n and k.
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
From https://en.wikipedia.org/wiki/Generalizations_of_Fibonacci_numbers:

The tetranacci numbers start with four predetermined terms, each term afterwards
being the sum of the preceding four terms.

The tetranacci constant is the ratio toward which adjacent tetranacci numbers
tend.  It is a root of the polynomial x^4 - x^3 - x^2 - x - 1 = 0.
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
From https://en.wikipedia.org/wiki/Generalizations_of_Fibonacci_numbers:

The tribonacci numbers are like the Fibonacci numbers, but instead of starting
with two predetermined terms, the sequence starts with three predetermined terms
and each term afterwards is the sum of the preceding three terms.  The first few
tribonacci numbers are:

The series was first described formally by Agronomof in 1914, but its first
unintentional use is in the Origin of species by Charles R. Darwin.  In the
example of illustrating the growth of elephant population, he relied on the
calculations made by his son, George H. Darwin.  The term tribonacci was
suggested by Feinberg in 1963.
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
The trigamma function is defined as the logarithmic second derivative of the
gamma function.

This is the equivalent of '1 n polygamma'.
''',
'''
''' + makeCommandExample( '1 10 10 geometric_range trigamma' ),
[ 'polygamma' ] ],

    'unit_roots' : [
'number_theory', 'calculates the nth roots of unity',
'''
From https://en.wikipedia.org/wiki/Root_of_unity:

In mathematics, a root of unity, occasionally called a de Moivre number, is any
complex number that yields 1 when raised to some positive integer power n.
Roots of unity are used in many branches of mathematics, and are especially
important in number theory, the theory of group characters, and the discrete
Fourier transform.
''',
'''
''' + makeCommandExample( '2 unit_roots' ) + '''
''' + makeCommandExample( '3 unit_roots' ) + '''
''' + makeCommandExample( '4 unit_roots' ),
[ 'root' ] ],

    'van_eck' : [
'number_theory', 'calculates the first n members of the van Eck sequence',
'''
''',
'''
''',
[ 'root' ] ],


    'zeta' : [
'number_theory', 'calculates Riemann\'s zeta function for n',
'''
This operator computes the Riemann zeta function:

                          1     1     1     1
        zeta( n ) =  1 + --- + --- + --- + --- ...
                         2^n   3^n   4^n   5^n

Although these series only converge for re( s ) > 1, the Riemann and Hurwitz
zeta functions are defined through analytic continuation for arbitrary complex
n != 1.  n = 1 is a pole.
''',
'''
''' + makeCommandExample( '2 zeta' ) + '''
''' + makeCommandExample( 'pi sqr 6 /' ) + '''
''' + makeCommandExample( '0 zeta' ) + '''
''' + makeCommandExample( '-1 zeta' ) + '''
''' + makeCommandExample( '20 zeta' ) + '''
''' + makeCommandExample( '-3 4j + zeta' ),
[ 'hurwitz_zeta', 'eta' ] ],

    'zeta_zero' : [
'number_theory', 'calculates the nth non-trivial zero of Riemann\'s zeta function',
'''
This operator omputes the n-th nontrivial zero of zeta( s ) on the critical
line, i.e. returns an approximation of the n-th largest complex number s = 1/2 +
ti for which zeta( s ) = 0.

The Riemann Hypothesis in short claims that all non-trivial zeroes of the zeta
function have a real part equal to 1/2.
''',
'''
''' + makeCommandExample( '1 5 range zeta_zero' ) + '''
''' + makeCommandExample( '183456 zeta_zero' ),
[ 'zeta' ] ],


    #******************************************************************************
    #
    #  physics operators
    #
    #******************************************************************************

    'acceleration' : [
'physics', 'calculates acceleration given different measurement types',
'''
This operator calculates constant acceleration from a stationary start, given
measurements in two different units (in either order), from one of the following
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
This operator calculates the entropy of a black hole given one of several
different measurements.

The measurements supported include the following measurements of the black hole:

Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the lifetime of a black hole given one of several
different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the luminosity of a black hole given one of several
different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the mass of a black hole given one of several different
measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Tidal force (at the event horizon)
Temperature
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
This operator calculates the Schwarzchild radius of a black hole of mass n given
one of several different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the surface area of a black hole given one of several
different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the surface gravity of a black hole given one of
several different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
Temperature
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
This operator calculates the tidal force at the event horizon of a black hole
given one of several different measurements.

Tidal force is meters/second^2/meter, which means the meters cancel out and
it ends up being 1/second^2, which I found confusing, but it makes sense if you
think about it.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Temperature
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
This operator calculates the temperature of a black hole given one of several
different measurements.

The measurements supported include the following measurements of the black hole:

Entropy
Surface area
Lifetime (until evaporation via Hawking Radiation)
Luminosity
Surface gravity (at the event horizon)
Schwarzchild radius (i.e., radius of the event horizon)
Mass
Tidal force (at the event horizon)
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
This operator calculates distance given measurements in two different units (in
either order), from one of the following combinations of units:

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
Thjis operator calculates the energy equivalence of mass n.  It uses Einstein's
energy-matter equivalence equation, E = mc^2, to calculate the energy
equivalence of mass n.
''',
'''
''' + makeCommandExample( '1 gram energy_equivalence' ) + '''
''' + makeCommandExample( '1 pound energy_equivalence' ),
[ 'mass_equivalence' ] ],

    'escape_velocity' : [
'physics', 'calculates the escape velocity of an object of mass n and radius k',
'''
This operator calculates the escape velocity of an object of mass n and radius
k.

From https://en.wikipedia.org/wiki/Escape_velocity:

In physics (specifically, celestial mechanics), escape velocity is the minimum
speed needed for a free, non-propelled object to escape from the gravitational
influence of a massive body, that is, to achieve an infinite distance from it.
Escape velocity is a function of the mass of the body and distance to the center
of mass of the body.

A rocket, continuously accelerated by its exhaust, need not reach ballistic
escape velocity at any distance since it is supplied with additional kinetic
energy by the expulsion of its reaction mass.  It can achieve escape at any
speed, given a suitable mode of propulsion and sufficient propellant to provide
the accelerating force on the object to escape.
''',
'''
''' + makeCommandExample( 'earth_mass earth_radius escape_velocity' ) + '''
''' + makeCommandExample( 'moon_mass moon_radius escape_velocity' ),
[ 'velocity', 'acceleration', 'orbital_velocity' ] ],

    'heat_index' : [
'physics', 'calculates the heat index given the temperature and the relative humidity',
'''
This operator calculates the heat index given the temperature and the relative
humidity.

From https://en.wikipedia.org/wiki/Heat_index:

The heat index (HI) is an index that combines air temperature and relative
humidity, in shaded areas, to posit a human-perceived equivalent temperature, as
how hot it would feel if the humidity were some other value in the shade.  The
result is also known as the "felt air temperature", "apparent temperature",
"real feel" or "feels like".  For example, when the temperature is 32 degrees C
(90 degrees F) with 70% relative humidity, the heat index is 41 degrees C (106
degrees F).

The heat index was developed in 1979 by Robert G. Steadman.  Like the wind chill
index, the heat index contains assumptions about the human body mass and height,
clothing, amount of physical activity, individual heat tolerance, sunlight and
ultraviolet radiation exposure, and the wind speed.  Significant deviations from
these will result in heat index values which do not accurately reflect the
perceived temperature
''',
'''
''' + makeCommandExample( '90 degrees_F 50 percent heat_index' ) + '''
''' + makeCommandExample( '90 degrees_F 70 percent heat_index' ) + '''
''' + makeCommandExample( '30 degrees_C 80 percent heat_index' ),
[ 'wind_chill' ] ],

    'horizon_distance' : [
'physics', 'calculates the distance to the horizon for altitude n on a body of radius k',
'''
This operator calculates the distance to the horizon for altitude n on a body of
radius k, assuming the body is a perfect sphere.
''',
'''
''' + makeCommandExample( '6 feet earth_radius horizon_distance' ) + '''
''' + makeCommandExample( '6 feet moon_radius horizon_distance' ) + '''
''' + makeCommandExample( '30 feet earth_radius horizon_distance' ),
[ 'orbital_radius', 'distance' ] ],

    'kinetic_energy' : [
'physics', 'calculates kinetic energy from velocity and mass',
'''
This operatro calculates kinetic energy from velocity and mass.

The kinetic energy is equal to 1/2 mass times velocity squared.  This is a
non-relativistic calculation.
''',
'''
''' + makeCommandExample( '60 mph 2000 pounds kinetic_energy' ) + '''
''' + makeCommandExample( '120 mph 2000 pounds kinetic_energy' ) + '''
''' + makeCommandExample( '66 miles second / earth_mass kinetic_energy' ),
[ 'velocity', 'acceleration', 'escape_velocity' ] ],

    'mass_equivalence' : [
'physics', 'calculates the mass equivalence of energy n',
'''
The operator calculates the mass equivalence of energy n.

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
This operator calculates the mass of the object being orbited, assuming the
object it's orbiting is spherical and the orbit is perfectly round.

Any two of the following three measurements can be used (in any order) as
arguments:

    orbital period,
    orbital velocity,
    orbit radius (the distance between the centers of mass)

Mass returned is really the combined mass of the object orbiting and the
object being orbited.
''',
'''
''' + makeCommandExample( '90.9 minutes earth_radius 200 miles + orbital_mass' ) + '''
''' + makeCommandExample( '66 miles second / 1 au orbital_mass' ) + '''
''' + makeCommandExample( 'earth_mass' ) + '''
''' + makeCommandExample( '20000 mph 24 hours orbital_mass' ),
[ 'orbital_period', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_period' : [
'physics', 'calculates the orbital period of an object',
'''
This operator calculates the orbital period of an object, assuming the objects
are spherical and the orbit is perfectly round.

Any two of the following three measurements can be used (in any order) as
arguments:

    mass (the combined mass of the two objects)
    orbit radius (the distance between the centers of mass)
    orbital velocity
''',
'''
''' + makeCommandExample( '66 miles second / 1 au orbital_period' ) + '''
''' + makeCommandExample( '20000 mph earth_mass orbital_period' ),
[ 'orbital_mass', 'orbital_radius', 'orbital_velocity' ] ],

    'orbital_radius' : [
'physics', 'calculates the radius of an orbit',
'''
The operator calculates the radius of an orbit, assuming the bodies in question
are spherical and the orbit is perfectly round.

Any two of the following three measurements can be used (in any order) as
arguments:

    mass (the combined mass of the two objects)
    orbital period
    orbital velocity
''',
'''
The orbital radius of a geosynchronous satellite:
''' + makeCommandExample( '24 hours earth_mass orbital_radius' ) + '''
''' + makeCommandExample( '66 miles second / 1 au orbital_mass' ) + '''
''' + makeCommandExample( 'earth_mass' ) + '''
''' + makeCommandExample( '20000 mph 24 hours orbital_mass' ),
[ 'orbital_mass', 'orbital_period', 'orbital_velocity' ] ],

    'orbital_velocity' : [
'physics', 'calculates the circular orbital velocity of an object',
'''
The operator calculates the orbital velocity for an object orbiting a spherical
body and the orbit is perfectly round.

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
This operator calculates the surface gravity of a spherical object.

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
Let's say we have a 500-meter long spaceship pointing at a black hole of 500,000
solar masses at the event horizon.  How much tidal force is the ship
experiencing between the bow and the stern:
''' + makeCommandExample( '500000 solar_mass previous black_hole_radius 500 meters tidal_force' ) + '''
Calculate the lunar tidal force on Earth for a delta of one meter (i.e., how
much tidal force affects an object one meter in size (assuming it's pointing
at the Moon).
''' + makeCommandExample( 'earth_mass 238900 miles 1 meter tidal_force' ),
[ 'black_hole_surface_tides' ] ],

    'time_dilation' : [
'physics', 'calculates the relativistic time-dilation effect of a velocity difference of n',
'''
This operator calculates the relativistic time-dilation effect of a velocity
difference of n.

If a velocity greater than the speed of light is used for n, the answer will be
imaginary.  You can decide what that means.
''',
'''
''' + makeCommandExample( '1 million mph time_dilation' ) + '''
''' + makeCommandExample( '0.99 c * time_dilation' ),
[ 'velocity' ] ],

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
'physics', 'calculates the wind chill given the temperature and the wind speed',
'''
This operator calculates the wind chill given the temperature and the wind
speed.

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
This operator calculates the nth centered cube number.

From https://en.wikipedia.org/wiki/Centered_cube_number:

A centered cube number is a centered figurate number that counts the number of
points in a three-dimensional pattern formed by a point surrounded by concentric
cubical layers of points, with i^2 points on the square faces of the ith layer.
Equivalently, it is the number of points in a body-centered cubic pattern within
a cube that has n + 1 points along each of its edges.

The centered cube number for a pattern with n concentric layers around the
central point is given by the formula:

n^3 + ( n + 1 )^3 = ( 2n + 1 )( n^2 + n + 1 ).

Because of the factorization ( 2n + 1 )( n^2 + n + 1 ), it is impossible for a
centered cube number to be a prime number.  The only centered cube number that
is also a square number is 9, which can be shown by solving 2n + 1 = n^2 + n +
1.
''',
'''
''' + makeCommandExample( '1 10 range centered_cube' ) + '''
''' + makeCommandExample( '1000 centered_cube' ),
[ 'cube', 'centered_polygonal' ] ],

    'centered_decagonal' : [
'figurate_numbers', 'calculates the nth centered decagonal number',
'''
This operator calculates the nth centered decagonal number.

From https://en.wikipedia.org/wiki/Centered_decagonal_number:

A centered decagonal number is a centered figurate number that represents a
decagon with a dot in the center and all other dots surrounding the center dot
in successive decagonal layers.  The centered decagonal number for n is given by
the formula:  5n^2 + 5n + 1.

Like any other centered k-gonal number, the nth centered decagonal number can be
reckoned by multiplying the (n − 1)th triangular number by k, 10 in this case,
then adding 1.  As a consequence of performing the calculation in base 10, the
centered decagonal numbers can be obtained by simply adding a 1 to the right of
each triangular number.  Therefore, all centered decagonal numbers are odd and
in base 10 always end in 1.
''',
'''
''' + makeCommandExample( '1 10 range centered_decagonal' ) + '''
''' + makeCommandExample( '5413 centered_decagonal' ),
[ 'decagonal', 'centered_polygonal', 'nth_centered_decagonal' ] ],

    'centered_dodecahedral' : [
'figurate_numbers', 'calculates the nth centered dodecahedral number',
'''
This operator calculates the nth centered dodecahedral number.

https://en.wikipedia.org/wiki/Centered_dodecahedral_number

A centered dodecahedral number is a centered figurate number that represents a
dodecahedron.  The centered dodecahedral number for a specific n is given by
( 2n + 1 )( 5n^2 + 5n + 1 ).
''',
'''
''' + makeCommandExample( '1 10 range centered_dodecahedral' ) + '''
''' + makeCommandExample( '4890 centered_dodecahedral' ),
[ 'dodecahedral', 'centered_tetrahedral', 'centered_octahedral', 'centered_icosahedral' ] ],

    'centered_heptagonal' : [
'figurate_numbers', 'calculates the nth centered heptagonal number',
'''
This operator calculates the nth centered heptagonal number.

From https://en.wikipedia.org/wiki/Centered_heptagonal_number:

A centered heptagonal number is a centered figurate number that represents a
heptagon with a dot in the center and all other dots surrounding the center dot
in successive heptagonal layers.  The centered heptagonal number for n is given
by the formula:

7n^2 - 7n + 2
-------------
      2

This can also be calculated by multiplying the triangular number for (n – 1) by
7, then adding 1.

Centered heptagonal numbers alternate parity in the pattern odd-even-even-odd.
''',
'''
''' + makeCommandExample( '1 10 range centered_heptagonal' ) + '''
''' + makeCommandExample( '13112 centered_heptagonal' ),
[ 'heptagonal', 'centered_polygonal', 'nth_centered_heptagonal' ] ],

    'centered_hexagonal' : [
'figurate_numbers', 'calculates the nth centered hexagonal number',
'''
This operator calculates the nth centered hexagonal number.

From https://en.wikipedia.org/wiki/Centered_hexagonal_number:

A centered hexagonal number, or hex number,[1] is a centered figurate number
that represents a hexagon with a dot in the center and all other dots
surrounding the center dot in a hexagonal lattice.  Centered hexagonal numbers
have practical applications in materials logistics management.

A centered hexagonal number is a centered figurate number that represents a
hexagon with a dot in the center and all other dots surrounding the center dot
in a hexagonal lattice.

The nth centered hexagonal number is given by the formula:

        n( n - 1 )
1 + 6 ( ---------- )
            2

This shows that the centered hexagonal number for n is 1 more than 6 times the
(n − 1)th triangular number.
''',
'''
''' + makeCommandExample( '1 10 range centered_hexagonal' ) + '''
''' + makeCommandExample( '73817 centered_hexagonal' ),
[ 'hexagonal', 'centered_polygonal', 'nth_centered_hexagonal' ] ],

    'centered_icosahedral' : [
'figurate_numbers', 'calculates the nth centered icosahedral number',
'''
From https://en.wikipedia.org/wiki/Centered_icosahedral_number:

A centered icosahedral number is a centered figurate number that represents an
icosahedron.  The centered icosahedral number for a specific n is given by:

( 2n + 1 )( 5n^2 + 5n + 3 )
---------------------------
             3
''',
'''
''' + makeCommandExample( '1 10 range centered_icosahedral' ) + '''
''' + makeCommandExample( '1243 centered_icosahedral' ),
[ 'icosahedral', 'centered_tetrahedral', 'centered_octahedral', 'centered_dodecahedral' ] ],

    'centered_nonagonal' : [
'figurate_numbers', 'calculates the nth centered nonagonal number',
'''
This operator calculates the nth centered nonagonal number.

From https://en.wikipedia.org/wiki/Centered_nonagonal_number:

A centered nonagonal number (or centered enneagonal number) is a centered
figurate number that represents a nonagon with a dot in the center and all other
dots surrounding the center dot in successive nonagonal layers.  The centered
nonagonal number for n is given by the formula:

( 3n - 2 )( 3n - 1 )
--------------------
          2

Multiplying the (n - 1)th triangular number by 9 and then adding 1 yields the
nth centered nonagonal number, but centered nonagonal numbers have an even
simpler relation to triangular numbers:  every third triangular number (the 1st,
4th, 7th, etc.) is also a centered nonagonal number.

The list of centered nonagonal numbers includes the perfect numbers 28 and 496.
All even perfect numbers are triangular numbers whose index is an odd Mersenne
prime.  Since every Mersenne prime greater than 3 is congruent to 1 modulo 3, it
follows that every even perfect number greater than 6 is a centered nonagonal
number.

In 1850, Sir Frederick Pollock conjectured that every natural number is the sum
of at most eleven centered nonagonal numbers, which has been neither proven nor
disproven.
''',
'''
''' + makeCommandExample( '1 10 range centered_nonagonal' ) + '''
''' + makeCommandExample( '8933 centered_nonagonal' ),
[ 'nonagonal', 'centered_polygonal', 'nth_centered_nonagonal' ] ],

    'centered_octagonal' : [
'figurate_numbers', 'calculates the nth centered octagonal number',
'''
This operator calculates the nth centered octagonal number.

From https://en.wikipedia.org/wiki/Centered_octagonal_number:

A centered octagonal number is a centered figurate number that represents an
octagon with a dot in the center and all other dots surrounding the center dot
in successive octagonal layers.  The centered octagonal numbers are the same as
the odd square numbers.  Thus, the nth centered octagonal number is given by the
formula:  ( 2n - 1 )^2 = 4n^2 - 4n + 1.

Calculating Ramanujan's tau function on a centered octagonal number yields an
odd number, whereas for any other number the function yields an even number.
''',
'''
''' + makeCommandExample( '1 10 range centered_octagonal' ) + '''
''' + makeCommandExample( '5012 centered_octagonal' ),
[ 'octagonal', 'centered_polygonal', 'nth_centered_octagonal' ] ],

    'centered_octahedral' : [
'figurate_numbers', 'calculates the nth centered octahedral number',
'''
This operator calculates the nth centered octahedral number.

From https://en.wikipedia.org/wiki/Centered_octahedral_number:

A centered octahedral number or Haüy octahedral number is a figurate number that
counts the number of points of a three-dimensional integer lattice that lie
inside an octahedron centered at the origin.  The same numbers are special cases
of the Delannoy numbers, which count certain two-dimensional lattice paths.  The
Hauey octahedral numbers are named after Rene Just Hauey.

The name "Hauey octahedral number" comes from the work of Rene Just Hauey, a
French mineralogist active in the late 18th and early 19th centuries.  His "
Hauey construction" approximates an octahedron as a polycube, formed by
accreting concentric layers of cubes onto a central cube.  The centered
octahedral numbers count the number of cubes used by this construction.  Hauey
proposed this construction, and several related constructions of other
polyhedra, as a model for the structure of crystalline minerals.

The number of three-dimensional lattice points within n steps of the origin is
given by the formula:

( 2n + 1 )( 2n^2 + 2n + 3 )
---------------------------
            3
''',
'''
''' + makeCommandExample( '1 10 range centered_octahedral' ) + '''
''' + makeCommandExample( '7476 centered_octahedral' ),
[ 'octahedral', 'centered_tetrahedral', 'centered_icosahedral', 'centered_dodecahedral' ] ],

    'centered_pentagonal' : [
'figurate_numbers', 'calculates the nth centered pentagonal number',
'''
This operator calculates the nth centered pentagonal number.

From https://en.wikipedia.org/wiki/Centered_pentagonal_number:

A centered pentagonal number is a centered figurate number that represents a
pentagon with a dot in the center and all other dots surrounding the center in
successive pentagonal layers.  The centered pentagonal number for n is given by
the formula:

5n^2 - 5n + 2
-------------
      2

The parity of centered pentagonal numbers follows the pattern even-even-odd, and
in base 10 the units follow the pattern 1-6-6-1.
''',
'''
''' + makeCommandExample( '1 10 range centered_pentagonal' ) + '''
''' + makeCommandExample( '9654 centered_pentagonal' ),
[ 'pentagonal', 'centered_polygonal', 'nth_centered_pentagonal' ] ],

    'centered_polygonal' : [
'figurate_numbers', 'calculates the nth centered k-gonal number',
'''
This operator is the generalized function that calculate the nth centered
k-gonal number for all k greater than 2.
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
From https://en.wikipedia.org/wiki/Centered_square_number:

In elementary number theory, a centered square number is a centered figurate
number that gives the number of dots in a square with a dot in the center and
all other dots surrounding the center dot in successive square layers.  That is,
each centered square number equals the number of dots within a given city block
distance of the center dot on a regular square lattice.  While centered square
numbers, like figurate numbers in general, have few if any direct practical
applications, they are sometimes studied in recreational mathematics for their
elegant geometric and arithmetic properties.

The formula for the nth centered square is n^2 + (n - 1)^2.

Every centered square number except 1 is the hypotenuse of a Pythagorean triple
(for example, 3-4-5, 5-12-13, 7-24-25).  This is exactly the sequence of
Pythagorean triples where the two longest sides differ by 1.
''',
'''
''' + makeCommandExample( '1 10 range centered_square' ) + '''
''' + makeCommandExample( '11452 centered_square' ),
[ 'square', 'centered_polygonal', 'nth_centered_square' ] ],

    'centered_tetrahedral' : [
'figurate_numbers', 'calculates the nth centered tetrahedral number',
'''
This operator calculates the nth centered tetrahedral number.

From https://en.wikipedia.org/wiki/Centered_tetrahedral_number:

A centered tetrahedral number is a centered figurate number that represents a
tetrahedron.  The centered tetrahedral number for a specific n is given by:

( 2n + 1 )( n^2 + n + 3 )
-------------------------
            3
''',
'''
''' + makeCommandExample( '1 10 range centered_tetrahedral' ) + '''
''' + makeCommandExample( '10000 centered_tetrahedral' ),
[ 'tetrahedral', 'centered_octahedral', 'centered_icosahedral', 'centered_dodecahedral' ] ],

    'centered_triangular' : [
'figurate_numbers', 'calculates the nth centered triangular number',
'''
This operator calculates the nth centered triangular number.

From https://en.wikipedia.org/wiki/Centered_triangular_number:

A centered (or centred) triangular number is a centered figurate number that
represents a triangle with a dot in the center and all other dots surrounding
the center in successive triangular layers.  The centered triangular number for
n is given by the formula:

3n^2 + 3n + 2
-------------
      2
''',
'''
''' + makeCommandExample( '1 10 range centered_triangular' ) + '''
''' + makeCommandExample( '1000 centered_triangular' ),
[ 'triangular', 'centered_polygonal', 'nth_centered_triangular' ] ],

    'decagonal' : [
'figurate_numbers', 'calculates the nth decagonal number',
'''
This operator calculates the nth decagonal number.

From https://en.wikipedia.org/wiki/Decagonal_number:

A decagonal number is a figurate number that extends the concept of triangular
and square numbers to the decagon (a ten-sided polygon).  However, unlike the
triangular and square numbers, the patterns involved in the construction of
decagonal numbers are not rotationally symmetrical.  Specifically, the nth
decagonal numbers counts the number of dots in a pattern of n nested decagons,
all sharing a common corner, where the ith decagon in the pattern has sides made
of i dots spaced one unit apart from each other.  The nth decagonal number is
given by the formula:  4n^2 - 3n.

Decagonal numbers consistently alternate parity.
''',
'''
''' + makeCommandExample( '1 10 range decagonal' ) + '''
''' + makeCommandExample( '5000 decagonal' ),
[ 'centered_decagonal', 'polygonal', 'nth_decagonal' ] ],

    'decagonal_centered_square' : [
'figurate_numbers', 'calculates the nth decagonal centered square number',
'''
This operator calculates the nth number that is both decagonal and centered
square.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_centered_square' ) + '''
''' + makeCommandExample( '59 decagonal_centered_square' ),
[ 'decagonal', 'centered_square', 'polygonal', 'centered_polygonal' ] ],

    'decagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
This operator calculates the nth number that is both decagonal and heptagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_heptagonal' ) + '''
''' + makeCommandExample( '127 decagonal_heptagonal' ),
[ 'decagonal', 'heptagonal', 'polygonal' ] ],

    'decagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth decagonal hexagonal number',
'''
This operator calculates the nth number that is both decagonal and hexagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_hexagonal' ) + '''
''' + makeCommandExample( '5741 decagonal_hexagonal' ),
[ 'decagonal', 'hexagonal', 'polygonal' ] ],

    'decagonal_nonagonal' : [
'figurate_numbers', 'calculates the nth decagonal heptagonal number',
'''
This operator calculates the nth number that is both decagonal and heptagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_nonagonal' ) + '''
''' + makeCommandExample( '5762 decagonal_nonagonal' ),
[ 'decagonal', 'nonagonal', 'polygonal' ] ],

    'decagonal_octagonal' : [
'figurate_numbers', 'calculates the nth decagonal octagonal number',
'''
This operator calculates the nth number that is both decagonal and octagonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_octagonal' ) + '''
''' + makeCommandExample( '2111 decagonal_octagonal' ),
[ 'decagonal', 'octagonal', 'polygonal' ] ],

    'decagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth decagonal pentagonal number',
'''
This operator calculates the nth number that is both decagonal and pentgonal.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_pentagonal' ) + '''
''' + makeCommandExample( '12000 decagonal_pentagonal' ),
[ 'decagonal', 'pentagonal', 'polygonal' ] ],

    'decagonal_triangular' : [
'figurate_numbers', 'calculates the nth decagonal triangular number',
'''
This operator calculates the nth number that is both decagonal and triangular.
''',
'''
''' + makeCommandExample( '1 10 range decagonal_triangular' ) + '''
''' + makeCommandExample( '351 decagonal_triangular' ),
[ 'decagonal', 'triangular', 'polygonal' ] ],

    'dodecahedral' : [
'figurate_numbers', 'returns the nth dodecahedral number',
'''
From https://en.wikipedia.org/wiki/Dodecahedral_number:

A dodecahedral number is a figurate number that represents a dodecahedron.  The
nth dodecahedral number is given by the formula:

n ( 3n - 1 )( 3n - 2 )
----------------------
          2
''',
'''
''' + makeCommandExample( '1 10 range dodecahedral' ) + '''
''' + makeCommandExample( '507 dodecahedral' ),
[ 'centered_dodecahedral', 'rhombic_dodecahedral' ] ],

    'generalized_decagonal' : [
'figurate_numbers', 'calculates the nth generalized decagonal number',
'''
This operator calculates the nth generalized decagonal number.

Generalized decagonal numbers are obtained from the formula for decaagonal
numbers (4n^2 - 3n), but with n taking values in the sequence 0, 1, −1, 2,
−2, 3, −3, 4...
''',
'''
''' + makeCommandExample( '1 10 range generalized_decagonal' ) + '''
''' + makeCommandExample( '986 generalized_decagonal' ),
[ 'decagonal', 'polygonal' ] ],

    'generalized_heptagonal' : [
'figurate_numbers', 'calculates the nth generalized heptagonal number',
'''
This operator calculates the nth generalized heptagonal number.

Generalized heptagonal numbers are obtained from the formula for heptagonal
numbers ( ( 5n^2 - 3n ) / 2 ), but with n taking values in the sequence 0, 1, −1, 2,
−2, 3, −3, 4...
''',
'''
''' + makeCommandExample( '1 10 range generalized_heptagonal' ) + '''
''' + makeCommandExample( '1437 generalized_heptagonal' ),
[ 'heptagonal', 'polygonal' ] ],

    'generalized_nonagonal' : [
'figurate_numbers', 'calculates the nth generalized nonagonal number',
'''
This operator calculates the nth generalized nonagonal number.

Generalized nonagonal numbers are obtained from the formula for nonagonal
numbers ( ( 7n^2 - 5n ) / 2 ), but with n taking values in the sequence 0, 1, −1, 2,
−2, 3, −3, 4...
''',
'''
''' + makeCommandExample( '1 10 range generalized_nonagonal' ) + '''
''' + makeCommandExample( '692 generalized_nonagonal' ),
[ 'nonagonal', 'polygonal' ] ],

    'generalized_octagonal' : [
'figurate_numbers', 'calculates the nth generalized octagonal number',
'''
Thhis operator calculates the nth generalized octagonal number.

Generalized octagonal numbers are obtained from the formula for octagonal
numbers ( 3n^2 - 2n ), but with n taking values in the sequence 0, 1, −1, 2, −2,
3, −3, 4...
''',
'''
''' + makeCommandExample( '1 10 range generalized_octagonal' ) + '''
''' + makeCommandExample( '436 generalized_octagonal' ),
[ 'octagonal', 'polygonal' ] ],

    'generalized_pentagonal' : [
'figurate_numbers', 'calculates the nth generalized pentagonal number',
'''
This operator calculates the nth generalized pentagonal number.

From https://en.wikipedia.org/wiki/Pentagonal_number:

Generalized pentagonal numbers are obtained from the formula for pentagonal
numbers ( ( 3n^2 - n ) / 2 ), but with n taking values in the sequence 0, 1,
−1, 2, −2, 3, −3, 4...

Generalized pentagonal numbers are closely related to centered hexagonal
numbers.  When the array corresponding to a centered hexagonal number is divided
between its middle row and an adjacent row, it appears as the sum of two
generalized pentagonal numbers, with the larger piece being a pentagonal number
proper.
''',
'''
''' + makeCommandExample( '1 10 range generalized_pentagonal' ) + '''
''' + makeCommandExample( '542 generalized_pentagonal' ),
[ 'pentagonal', 'polygonal' ] ],

    'heptagonal' : [
'figurate_numbers', 'calculates the nth heptagonal number',
'''
This operator calculates the nth heptagonal number.

A heptagonal number is a figurate number that is constructed by combining
heptagons with ascending size.  The n-th heptagonal number is given by the
formula:

5n^2 - 3n
---------
    2

The parity of heptagonal numbers follows the pattern odd-odd-even-even.  Like
square numbers, the digital root in base 10 of a heptagonal number can only be
1, 4, 7 or 9.  Five times a heptagonal number, plus 1 equals a triangular
number.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal' ) + '''
''' + makeCommandExample( '27870 heptagonal' ),
[ 'hexagonal', 'octagonal', 'polygonal' ] ],

    'heptagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth heptagonal hexagonal number',
'''
This operator calculates the nth number that is both heptagonal and hexagonal.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_hexagonal' ) + '''
''' + makeCommandExample( '911 heptagonal_hexagonal' ),
[ 'heptagonal', 'hexagonal', 'polygonal' ] ],

    'heptagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth heptagonal pentagonal number',
'''
This operator calculates the nth number that is both heptagonal and pentgonal.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_pentagonal' ) + '''
''' + makeCommandExample( '7027 heptagonal_pentagonal' ),
[ 'heptagonal', 'pentagonal', 'polygonal' ] ],

    'heptagonal_square' : [
'figurate_numbers', 'calculates the nth heptagonal square number',
'''
This operator alculates the nth number that is both heptagonal and square.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_square' ) + '''
''' + makeCommandExample( '1813 heptagonal_square' ),
[ 'heptagonal', 'square', 'polygonal' ] ],

    'heptagonal_triangular' : [
'figurate_numbers', 'calculates the nth heptagonal triangular number',
'''
This operator calculates the nth number that is both heptagonal and triangular.
''',
'''
''' + makeCommandExample( '1 10 range heptagonal_triangular' ) + '''
''' + makeCommandExample( '216 heptagonal_triangular' ),
[ 'heptagonal', 'triangular', 'polygonal' ] ],

    'hexagonal' : [
'figurate_numbers', 'calculates the nth hexagonal number',
'''
This operator calculates the nth hexagonal number.

From https://en.wikipedia.org/wiki/Hexagonal_number:

A hexagonal number is a figurate number.  The nth hexagonal number h(n) is the
number of distinct dots in a pattern of dots consisting of the outlines of
regular hexagons with sides up to n dots, when the hexagons are overlaid so that
they share one vertex.

The formula for the nth hexagonal number is:  2n^2 - n.

Every hexagonal number is a triangular number, but only every other triangular
number (the 1st, 3rd, 5th, 7th, etc.) is a hexagonal number.  Like a triangular
number, the digital root in base 10 of a hexagonal number can only be 1, 3, 6,
or 9.  The digital root pattern, repeating every nine terms, is "1 6 6 1 9 3 1
3 9".
''',
'''
''' + makeCommandExample( '1 10 range hexagonal' ) + '''
''' + makeCommandExample( '7776 hexagonal' ),
[ 'pentagonal', 'heptagonal', 'polygonal' ] ],

    'hexagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth hexagonal pentagonal number',
'''
This operator calculates the nth number that is both hexagonal and pentagonal.
''',
'''
''' + makeCommandExample( '1 10 range hexagonal_pentagonal' ) + '''
''' + makeCommandExample( '3125 hexagonal_pentagonal' ),
[ 'hexagonal', 'pentagonal', 'polygonal' ] ],

    'hexagonal_square' : [
'figurate_numbers', 'calculates the nth hexagonal square number',
'''
This operator calculates the nth number that is both hexagonal and square.
''',
'''
''' + makeCommandExample( '1 10 range hexagonal_square' ) + '''
''' + makeCommandExample( '443 hexagonal_square' ),
[ 'hexagonal', 'square', 'polygonal' ] ],

    'icosahedral' : [
'figurate_numbers', 'calculates the nth icosahedral number',
'''
This operator calculates the nth icosahedral number.

From https://en.wikipedia.org/wiki/Icosahedral_number:

An icosahedral number is a figurate number that represents an icosahedron.  The
nth icosahedral number is given by the formula:

    n ( 5n^2 - 5n + 2 )
    -------------------
             2

The first study of icosahedral numbers appears to have been by Rene Descartes,
around 1630, in his "De solidorum elementis".  Prior to Descartes, figurate
numbers had been studied by the ancient Greeks and by Johann Faulhaber, but only
for polygonal numbers, pyramidal numbers, and cubes.  Descartes introduced the
study of figurate numbers based on the Platonic solids and some semiregular
polyhedra; his work included the icosahedral numbers.  However, "De solidorum
elementis" was lost, and not rediscovered until 1860.  In the meantime,
icosahedral numbers had been studied again by other mathematicians, including
Friedrich Wilhelm Marpurg in 1774, Georg Simon Kluegel in 1808, and Sir
Frederick Pollock in 1850.
''',
'''
''' + makeCommandExample( '1 10 range icosahedral' ) + '''
''' + makeCommandExample( '400 icosahedral' ),
[ 'tetrahedral', 'octahedral', 'dodecahedral' ] ],

    'nonagonal' : [
'figurate_numbers', 'calculates the nth nonagonal number',
'''
This operator calculates the nth nonagonal number.

From https://en.wikipedia.org/wiki/Nonagonal_number:

A nonagonal number (or an enneagonal number) is a figurate number that extends
the concept of triangular and square numbers to the nonagon (a nine-sided
polygon).  However, unlike the triangular and square numbers, the patterns
involved in the construction of nonagonal numbers are not rotationally
symmetrical.  Specifically, the nth nonagonal number counts the number of dots
in a pattern of n nested nonagons, all sharing a common corner, where the ith
nonagon in the pattern has sides made of i dots spaced one unit apart from each
other.  The nonagonal number for n is given by the formula:

    n ( 7n - 5 )
    ------------
         2

The parity of nonagonal numbers follows the pattern odd-odd-even-even.
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
''',
'''
''' + makeCommandExample( '1 10 range nonagonal_triangular' ) + '''
''' + makeCommandExample( '454 nonagonal_triangular' ),
[ 'nonagonal', 'triangular', 'polygonal' ] ],

    'nth_centered_decagonal' : [
'figurate_numbers', 'finds the index of the centered decagonal number of value n',
'''
This operator solves for the index of the equation used by 'centered_decagonal'
to get the index i of the ith centered decagonal number that corresponds to the
value n.

If n is not a centered decagonal number, the result will be the index of the
highest centered decagonal number less than n.
''',
'''
''' + makeCommandExample( '10000000 nth_centered_decagonal' ) + '''
''' + makeCommandExample( 'result centered_decagonal' ),
[ 'centered_decagonal', 'nth_centered_polygonal' ] ],

    'nth_centered_heptagonal' : [
'figurate_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'nth_centered_heptagonal' solves for the index of the equation used by
'centered_heptagonal' to get the index i of the ith centered heptagonal number
that corresponds to the value n.

If n is not a centered heptagonal number, the result will be the index of the
highest centered heptagonal number less than n.
''',
'''
''' + makeCommandExample( '1000000 nth_centered_heptagonal' ) + '''
''' + makeCommandExample( 'result centered_heptagonal' ),
[ 'centered_heptagonal', 'nth_centered_polygonal' ] ],

    'nth_centered_hexagonal' : [
'figurate_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'nth_centered_hexagonal' solves for the index of the equation used by
'centered_hexagonal' to get the index i of the ith centered hexagonal number
that corresponds to the value n.

If n is not a centered hexagonal number, the result will be the index of the
highest centered hexagonal number less than n.
''',
'''
''' + makeCommandExample( '1000000 nth_centered_hexagonal' ) + '''
''' + makeCommandExample( 'result centered_hexagonal' ),
[ 'centered_hexagonal', 'nth_centered_polygonal' ] ],

    'nth_centered_nonagonal' : [
'figurate_numbers', 'finds the index of the centered nonagonal number of value n',
'''
'nth_centered_nonagonal' solves for the index of the equation used by
'centered_nonagonal' to get the index i of the ith centered nonagonal number
that corresponds to the value n.

If n is not a centered nonagonal number, the result will be the index of the
highest centered nonagonal number less than n.
''',
'''
''' + makeCommandExample( '1000000 nth_centered_nonagonal' ) + '''
''' + makeCommandExample( 'result centered_nonagonal' ),
[ 'centered_nonagonal', 'nth_centered_polygonal' ] ],

    'nth_centered_octagonal' : [
'figurate_numbers', 'finds the index of the centered octgonal number of value n',
'''
'nth_centered_octagonal' solves for the index of the equation used by
'centered_octagonal' to get the index i of the ith centered octagonal number
that corresponds to the value n.

If n is not a centered octagonal number, the result will be the index of the
highest centered octagonal number less than n.
''',
'''
''' + makeCommandExample( '1000 nth_centered_octagonal' ) + '''
''' + makeCommandExample( 'result centered_octagonal' ),
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
''' + makeCommandExample( '10000000 nth_centered_pentagonal' ) + '''
''' + makeCommandExample( '2000 centered_pentagonal' ),
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
''' + makeCommandExample( '1000 nth_centered_pentagonal' ) + '''
''' + makeCommandExample( '1000 5 nth_centered_polygonal' ) + '''
''' + makeCommandExample( '25456 16 nth_centered_polygonal' ) + '''
''' + makeCommandExample( 'result 16 centered_polygonal' ),
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
''' + makeCommandExample( '10000000 nth_centered_square' ) + '''
''' + makeCommandExample( 'result centered_square' ),
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
''' + makeCommandExample( '100000000 nth_centered_triangular' ) + '''
''' + makeCommandExample( 'result centered_triangular' ),
[ 'centered_triangular', 'nth_centered_polygonal' ] ],

    'nth_decagonal' : [
'figurate_numbers', 'finds the index of the decagonal number of value n',
'''
This operator solves for the index of the equation used by 'decagonal' to get
the index i of the ith decagonal number that corresponds to the value n.

If n is not a decagonal number, the result will be the index of the highest
decagonal number less than n.
''',
'''
''' + makeCommandExample( '100000000 nth_decagonal' ) + '''
''' + makeCommandExample( 'result decagonal' ),
[ 'decagonal', 'nth_polygonal', 'nth_centered_decagonal' ] ],

    'nth_hexagonal' : [
'figurate_numbers', 'finds the index of the hexagonal number of value n',
'''
This operator solves for the index of the equation used by 'hexagonal' to get
the index i of the ith hexagonal number that corresponds to the value n.

If n is not a hexagonal number, the result will be the index of the highest
hexagonal number less than n.
''',
'''
''' + makeCommandExample( '100000000 nth_hexagonal' ) + '''
''' + makeCommandExample( 'result hexagonal' ),
[ 'hexagonal', 'nth_polygonal', 'nth_centered_hexagonal' ] ],

    'nth_heptagonal' : [
'figurate_numbers', 'finds the index of the heptagonal number of value n',
'''
This operator solves for the index of the equation used by 'heptagonal' to get
the index i of the ith heptagonal number that corresponds to the value n.

If n is not a heptagonal number, the result will be the index of the highest
heptagonal number less than n.
''',
'''
''' + makeCommandExample( '100000000 nth_heptagonal' ) + '''
''' + makeCommandExample( 'result heptagonal' ),
[ 'heptagonal', 'nth_polygonal', 'nth_centered_heptagonal' ] ],

    'nth_nonagonal' : [
'figurate_numbers', 'finds the index of the nonagonal number of value n',
'''
This operator solves for the index of the equation used by 'nonagonal' to get
the index i of the ith nonagonal number that corresponds to the value n.

If n is not a nonagonal number, the result will be the index of the highest
nonagonal number less than n.
''',
'''
''' + makeCommandExample( '100000000 nth_nonagonal' ) + '''
''' + makeCommandExample( 'result nonagonal' ),
[ 'nonagonal', 'nth_polygonal', 'nth_centered_nonagonal' ] ],

    'nth_octagonal' : [
'figurate_numbers', 'finds the index of the octagonal number of value n',
'''
This operator solves for the index of the equation used by 'octagonal' to get
the index i of the ith octagonal number that corresponds to the value n.

If n is not a octagonal number, the result will be the index of the highest
octagonal number less than n.
''',
'''
''' + makeCommandExample( '100000000 nth_octagonal' ) + '''
''' + makeCommandExample( 'result octagonal' ),
[ 'octagonal', 'nth_polygonal', 'nth_centered_octagonal' ] ],

    'nth_pentagonal' : [
'figurate_numbers', 'finds the index of the pentagonal number of value n',
'''
This operator solves for the index of the equation used by 'pentagonal' to get
the index i of the ith pentagonal number that corresponds to the value n.

If n is not a pentagonal number, the result will be the index of the highest
pentagonal number less than n.
''',
'''
''' + makeCommandExample( '1000000000 nth_pentagonal' ) + '''
''' + makeCommandExample( 'result pentagonal' ),
[ 'pentagonal', 'nth_polygonal', 'nth_centered_pentagonal' ] ],

    'nth_polygonal' : [
'figurate_numbers', 'finds the index of the polygonal number with k sides of value n',
'''
This operator solves for the index of the equation used by 'polygonal' to get
the index i of the ith k-polygonal number that corresponds to the value n.

If n is not a k-polygonal number, the result will be the index of the highest
k-polygonal number less than n.
''',
'''
''' + makeCommandExample( '10000 10 nth_polygonal' ) + '''
''' + makeCommandExample( 'result 10 polygonal' ),
[ 'polygonal', 'nth_centered_polygonal' ] ],

    'nth_square' : [
'figurate_numbers', 'finds the index of the square number of value n',
'''
This operator solves for the index of the equation used by 'square' to get
the index i of the ith square number that corresponds to the value n.

If n is not a square number, the result will be the index of the highest
square number less than n.
''',
'''
''' + makeCommandExample( '1000000000 nth_square' ) + '''
''' + makeCommandExample( 'result square' ),
[ 'square', 'nth_polygonal' ] ],

    'nth_triangular' : [
'figurate_numbers', 'finds the index of the triangular number of value n',
'''
This operator solves for the index of the equation used by 'triangular' to get
the index i of the ith triangular number that corresponds to the value n.

If n is not a triangular number, the result will be the index of the highest
triangular number less than n.
''',
'''
''' + makeCommandExample( '1000000000 nth_triangular' ) + '''
''' + makeCommandExample( 'result triangular' ),
[ 'triangular', 'nth_polygonal' ] ],

    'octagonal' : [
'figurate_numbers', 'calculates the nth octagonal number',
'''
This operator calculates the nth octagonal number.

From https://en.wikipedia.org/wiki/Octagonal_number:

An octagonal number is a figurate number that represents an octagon.  The
octagonal number for n is given by the formula 3n^2 - 2n, with n > 0.

Octagonal numbers can be formed by placing triangular numbers on the four sides
of a square.
''',
'''
''' + makeCommandExample( '1 16 range octagonal' ) + '''
''' + makeCommandExample( '2685 octagonal' ),
[ 'centered_octagonal', 'polygonal' ] ],

    'octagonal_heptagonal' : [
'figurate_numbers', 'calculates the nth octagonal heptagonal number',
'''
This operator calculates the nth number that is both octagonal and heptagonal.
''',
'''
''' + makeCommandExample( '-a22 1 5 range octagonal_heptagonal' ) + '''
''' + makeCommandExample( '-a40 13 octagonal_pentagonal' ),
[ 'octagonal', 'heptagonal' ] ],

    'octagonal_hexagonal' : [
'figurate_numbers', 'calculates the nth octagonal hexagonal number',
'''
This operator calculates the nth number that is both octagonal and hexagonal.
''',
'''
''' + makeCommandExample( '-a20 1 5 range octagonal_hexagonal' ) + '''
''' + makeCommandExample( '-a50 12 octagonal_hexagonal' ),
[ 'octagonal', 'hexagonal' ] ],

    'octagonal_pentagonal' : [
'figurate_numbers', 'calculates the nth octagonal pentagonal number',
'''
This operator calculates the nth number that is both octagonal and pentagonal.
''',
'''
''' + makeCommandExample( '-a20 1 6 range octagonal_pentagonal' ) + '''
''' + makeCommandExample( '-a50 17 octagonal_pentagonal' ),
[ 'octagonal', 'pentagonal' ] ],

    'octagonal_square' : [
'figurate_numbers', 'calculates the nth octagonal square number',
'''
This operator calculates the nth number that is both octagonal and square.
''',
'''
''' + makeCommandExample( '-a20 1 7 range octagonal_square' ) + '''
''' + makeCommandExample( '-a50 22 octagonal_square' ),
[ 'octagonal', 'square' ] ],

    'octagonal_triangular' : [
'figurate_numbers', 'calculates the nth octagonal triangular number',
'''
This operator calculates the nth number that is both octagonal and triangular.
''',
'''
''' + makeCommandExample( '-a20 1 8 range octagonal_triangular' ) + '''
''' + makeCommandExample( '-a22 12 octagonal_triangular' ),
[ 'octagonal', 'triangular' ] ],

    'octahedral' : [
'figurate_numbers', 'calculates the nth octahedral number',
'''
This operator calculates the nth octahedral number.

From "The Book of Numbers", by John Conway and Richard Guy:

The easiest way to view the octahedral numbers is as double square pyramids, the
sum of two consecutive square pyramids.
''',
'''
''' + makeCommandExample( '1 15 range octahedral' ) + '''
''' + makeCommandExample( '4881 octahedral' ),
[ 'tetrahedral', 'dodecahedral' ] ],

    'pentagonal' : [
'figurate_numbers', 'calculates the nth pentagonal number',
'''
This operator calculates the nth pentagonal number.

From https://en.wikipedia.org/wiki/Pentagonal_number:

A pentagonal number is a figurate number that extends the concept of triangular
and square numbers to the pentagon, but, unlike the first two, the patterns
involved in the construction of pentagonal numbers are not rotationally
symmetrical.  The nth pentagonal number p(n) is the number of distinct dots in a
pattern of dots consisting of the outlines of regular pentagons with sides up to
n dots, when the pentagons are overlaid so that they share one vertex.  For
instance, the third one is formed from outlines comprising 1, 5 and 10 dots, but
the 1, and 3 of the 5, coincide with 3 of the 10 - leaving 12 distinct dots, 10
in the form of a pentagon, and 2 inside.

p(n) is given by the formula:

3n^2 - n
--------
    2

The nth pentagonal number is one third of the (3n − 1)th triangular number.
''',
'''
''' + makeCommandExample( '1 16 range pentagonal' ) + '''
''' + makeCommandExample( '174985 pentagonal' ),
[ 'centered_pentagonal', 'polygonal' ] ],

    'pentagonal_square' : [
'figurate_numbers', 'calculates the nth pentagonal square number',
'''
This operator calculates the nth number that is both pentagonal and square.
''',
'''
''' + makeCommandExample( '-a20 1 5 range pentagonal_square' ) + '''
''' + makeCommandExample( '-a40 11 pentagonal_square' ),
[ 'pentagonal', 'square' ] ],

    'pentagonal_triangular' : [
'figurate_numbers', 'calculates the nth pentagonal triangular number',
'''
This operator calculates the nth number that is both pentagonal and triangular.
''',
'''
''' + makeCommandExample( '-a20 1 6 range pentagonal_triangular' ) + '''
''' + makeCommandExample( '-a25 11 pentagonal_triangular' ),
[ 'pentagonal', 'triangular' ] ],

    'pentatope' : [
'figurate_numbers', 'calculates the nth pentatope number',
'''
This operate calculates the nth pentatope number.

From https://en.wikipedia.org/wiki/Pentatope_number:

A pentatope number is a number in the fifth cell of any row of Pascal's triangle
starting with the 5-term row 1 4 6 4 1 either from left to right or from right
to left.

The formula for the nth pentatope number is represented by the 4th rising
factorial of n divided by the factorial of 4:

n ( n + 1 )( n + 2 )( n + 3 )
-----------------------------
             24
''',
'''
''' + makeCommandExample( '1 15 range pentatope' ) + '''
''' + makeCommandExample( '1238 pentatope' ),
[ 'polytope', 'polygonal' ] ],

    'polygonal' : [
'figurate_numbers', 'calculates the nth polygonal number with k sides',
'''
This operator calculates the nth polygonal number with k sides for k greater
than 2.
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
This operator calculates the nth pyramidal number with k sides.

From https://en.wikipedia.org/wiki/Pyramidal_number:

A pyramidal number is a figurate number that represents a pyramid with a
polygonal base and a given number of triangular sides.  A pyramidal number is
the number of points in a pyramid where each layer of the pyramid is a k-sided
polygon of points.  The term usually refers to square pyramidal numbers, which
have a square base with four sides, but it can also refer to pyramids with three
or more sides.  It is possible to extend the pyramidal numbers to higher
dimensions.
''',
'''
''' + makeCommandExample( '23 pyramidal' ) + '''
''' + makeCommandExample( '23 4 polygonal_pyramidal' ) + '''
''' + makeCommandExample( '-a25 387 129 polygonal_pyramidal' ),
[ 'polygonal', 'pyramidal' ] ],

    'polytope' : [
'figurate_numbers', 'calculates the nth polytope number of dimension k',
'''
This operator  the nth polytope number of dimension k.  The polytope number is
defined to be a generalization of figurate numbers in k dimensions, starting
with triangular, tetrahedral, pentatope, etc.

The formula for the nth k-dimensional polytope number is:

              n - 1
      1       -----
 ---------- * |   |  ( x + n )
 ( d - 1 )!   |   |
              x = 0

That's meant to he a big pi to represent the ranged product from 0 to n - 1.
ASCII art rules!

Ref:  "The Book of Numbers", John H. Conway and Richard K. Guy
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
From https://en.wikipedia.org/wiki/Square_pyramidal_number:

In mathematics, a pyramid number, or square pyramidal number, is a figurate
number that represents the number of stacked spheres in a pyramid with a square
base.  Square pyramidal numbers also solve the problem of counting the number of
squares in an n × n grid.

These numbers can be expressed in a formula as:

n ( n + 1 )( 2n + 1 )
---------------------
         6

This is the equivalent of 'n 4 polygonal_pyramidal'.
''',
'''
''' + makeCommandExample( '1 10 range pyramidal' ) + '''
''' + makeCommandExample( '-a15 56714 pyramidal' ),
[ 'polygonal_pyramidal', 'square' ] ],

    'rhombic_dodecahedral' : [
'figurate_numbers', 'calculates the nth rhombic dodecahedral number',
'''
This operator calculates the nth rhombic dodecahedral number.

From "The Book of Numbers", by John Conway and Richard Guy:

One way to visualize the rhombic dodecahedral number is by appending a square
pyramid to each of the six faces of a centered cube.
''',
'''
''' + makeCommandExample( '1 8 range rhombic_dodecahedral' ) + '''
''' + makeCommandExample( '715 rhombic_dodecahedral' ),
[ 'dodecahedral', 'centered_dodecahedral' ] ],

    'square_triangular' : [
'figurate_numbers', 'calculates the nth square triangular number',
'''
This operator calculates the nth number that is both square and triangular.
''',
'''
''' + makeCommandExample( '1 8 range square_triangular' ) + '''
''' + makeCommandExample( '-a25 16 square_triangular' ),
[ 'square', 'triangular' ] ],

    'star' : [
'figurate_numbers', 'calculates the nth star number',
'''
This operator calculates the nth star number.

From https://en.wikipedia.org/wiki/Star_number:

A star number is a centered figurate number a centered hexagram (six-pointed
star), such as the one that Chinese checkers is played on.

The nth star number is given by the formula S(n) = 6n (n − 1) + 1.

Geometrically, the nth star number is made up of a central point and 12 copies
of the ( n − 1 )th triangular number - making it numerically equal to the nth
centered dodecagonal number, but differently arranged.
''',
'''
''' + makeCommandExample( '1 15 range star' ) + '''
''' + makeCommandExample( '8542 star' ),
[ 'polygonal', 'pyramidal' ] ],

    'stella_octangula' : [
'figurate_numbers', 'calculates the nth stella octangula number',
'''
This operator calculates the nth stella octangula number.

From https://en.wikipedia.org/wiki/Stella_octangula_number:

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
This operator calculates the nth tetrahedral number.

From https://en.wikipedia.org/wiki/Tetrahedral_number:

A tetrahedral number, or triangular pyramidal number, is a figurate number that
represents a pyramid with a triangular base and three sides, called a
tetrahedron.  The nth tetrahedral number, Te(n), is the sum of the first n
triangular numbers.

The formula for the nth tetrahedral number is represented by the 3rd rising
factorial of n divided by the factorial of 3:

n ( n + 1 )( n + 2 )
--------------------
         6

Tetrahedral numbers can be modelled by stacking spheres.  For example, the fifth
tetrahedral number (Te(5) = 35) can be modelled with 35 billiard balls and the
standard triangular billiards ball frame that holds 15 balls in place.  Then 10
more balls are stacked on top of those, then another 6, then another three and
one ball at the top completes the tetrahedron.
''',
'''
''' + makeCommandExample( '1 8 range tetrahedral' ) + '''
''' + makeCommandExample( '413 tetrahedral' ),
[ 'octahedral', 'dodecahedral', 'icosahedral' ] ],

    'triangular' : [
'figurate_numbers', 'calculates the nth triangular number',
'''
This operator calculates the nth triangular number.

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
This operator calculates the nth truncated octahedral number.

From "The Book of Numbers", by John Conway and Richard Guy:

Start with the (3n - 2)th octahedral number, and cut off the (n - 1)th square
pyramid from each of its six vertices.
''',
'''
''' + makeCommandExample( '1 10 range truncated_octahedral' ),
[ 'octahedral', 'stella_octangula' ] ],

    'truncated_tetrahedral' : [
'figurate_numbers', 'calculates the nth truncated tetrahedral number',
'''
This operator calculates the nth truncated tetrahedral number.

From "The Book of Numbers", by John Conway and Richard Guy:

Start with the (3n - 2)th tetrahedral number, and cut off the (n - 1)th
tetrahedral pyramid from each corner, we are left with the nth truncated
tetrahedral number.
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
'powers_and_roots', 'calculates the arithmetic-geometric mean of n and k',
'''
This operator calculates the arithmetic-geometric mean of n and k.

From https://en.wikipedia.org/wiki/Arithmetic–geometric_mean:

In mathematics, the arithmetic–geometric mean (AGM) of two positive real numbers
x and y is defined as follows:

Call x and y a_0 and g_0:

a0 = x
g0 = y

Then define the two interdependent sequences (a_n) and (g_n) as:

         1
a_n+1 =  - ( a_n + g_n )
         2

             ____________
            /
g_n+1 =    /  a_n g_n
         \\/

These two sequences converge to the same number, the arithmetic–geometric mean
of x and y; it is denoted by M( x, y ), or sometimes by agm( x, y ).

The arithmetic-geometric mean is used in fast algorithms for exponential and
trigonometric functions, as well as some mathematical constants, in particular,
computing pi.
''',
'''
''' + makeCommandExample( '24 6 agm' ) + '''
''' + makeCommandExample( '3 2j - 4 agm' ),
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
THe operator calculates the cube super-root of n.  It returns x such that
( x ^ x ) ^ x = n.
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
This operator calculates e to the power of n.  it is the inverse of the 'log'
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
This operator calculates 10 to the power of n.  it is the inverse of the 'log10'
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
This operator simply takes phi (the Golden Ratio) to the power of the argument n.

It was originally added to make testing the base phi output easier.
''',
'''
''' + makeCommandExample( '2 expphi' ) + '''
''' + makeCommandExample( '3 expphi 2 expphi -' ),
[ 'phi', 'exp', 'exp10' ] ],

    'hyperoperator' : [
'powers_and_roots', 'calculates the ath hyperoperator with operands b and c',
'''
The operator calculates the ath hyperoperator with operands b and c.

from https://en.wikipedia.org/wiki/Hyperoperation:

In mathematics, the hyperoperation sequence is an infinite sequence of
arithmetic operations (called hyperoperations in this context) that starts with
a unary operation (the successor function with a = 0).  The sequence continues
with the binary operations of addition (a = 1), multiplication (a = 2), and
exponentiation (a = 3).

rpnChilada does support real operands for b, but c must be a non-negative
integer.

rpnChilada extrapolates operations beyond multiplication using
left-associativity.  It appears that right-associativity is the conventional
interpretation, and for that, rpnChilada provides 'hyperoperator_right'.  Even
with left associativity, hyperoperators beyond 3 quickly overflow.

rpnChilada does support real operands for b, but c must be a non-negative
integer.  For a > 4, only integer operands are allowed.
''',
'''
The succssor function:
''' + makeCommandExample( '0 1 1 hyperoperator' ) + '''
Addition:
''' + makeCommandExample( '1 3 3 hyperoperator' ) + '''
Multiplication:
''' + makeCommandExample( '2 36 45 hyperoperator' ) + '''
Exponentiation:
''' + makeCommandExample( '3 9 9 hyperoperator' ) + '''
''' + makeCommandExample( '3 pi 3 hyperoperator' ) + '''
Tetration:
''' + makeCommandExample( '-a20 4 2.8 10 hyperoperator' ) + '''
Pentation:
''' + makeCommandExample( '-a20 5 3 2 hyperoperator' ) + '''
2 and 2 always make 4:
''' + makeCommandExample( '1 10 range lambda x 2 2 hyperoperator eval' ),
[ 'tetrate_right', 'tetrate', 'power', 'hyperoperator_right' ] ],

    'hyperoperator_right' : [
'powers_and_roots', 'calculates the ath right-associative hyperoperator with operands b and c',
'''
The operator calculates the ath hyperoperator with operands b and c using
right-associativity.

from https://en.wikipedia.org/wiki/Hyperoperation:

In mathematics, the hyperoperation sequence is an infinite sequence of
arithmetic operations (called hyperoperations in this context) that starts with
a unary operation (the successor function with n = 0).  The sequence continues
with the binary operations of addition (n = 1), multiplication (n = 2), and
exponentiation (n = 3).

After that, the sequence proceeds with further binary operations extending
beyond exponentiation, using right-associativity.  For the operations beyond
exponentiation, the nth member of this sequence is named by Reuben Goodstein
after the Greek prefix of n suffixed with -ation (such as tetration (n = 4),
pentation (n = 5), hexation (n = 6), etc.) and can be written as using n − 2
arrows in Knuth's up-arrow notation.

rpnChilada does support real operands for b, but c must be a non-negative
integer.  For a > 4, only integer operands are allowed.

Since the zeroth operation is a unary operation, rpnChilada ignores the c
operand when a = 0.
''',
'''
The succssor function:
''' + makeCommandExample( '0 1 1 hyperoperator_right' ) + '''
Addition:
''' + makeCommandExample( '1 3 3 hyperoperator_right' ) + '''
Multiplication:
''' + makeCommandExample( '2 36 45 hyperoperator_right' ) + '''
Exponentiation:
''' + makeCommandExample( '3 9 9 hyperoperator_right' ) + '''
''' + makeCommandExample( '3 pi 3 hyperoperator' ) + '''
Tetration:
''' + makeCommandExample( '-a20 4 1.8 6 hyperoperator_right' ) + '''
Pentation:
''' + makeCommandExample( '-a20 5 4 2 hyperoperator_right' ) + '''
2 and 2 always make 4:
''' + makeCommandExample( '1 10 range lambda x 2 2 hyperoperator_right eval' ),
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
'powers_and_roots', 'calculates the result of list n as a power tower',
'''
This operator calculates the result of interpreting list n as a left-associative
"power tower", meaning a succession of exponentiations:

( ( ( n1 ^ n2  ) ^ n3 ) ^ n4 ) ...
''',
'''
''' + makeCommandExample( '-a20 [ 2 3 4 5 ] power_tower' ) + '''
''' + makeCommandExample( '[ 5 -6 7 -8 ] power_tower' ) + '''
''' + makeCommandExample( '[ i i i i i i i ] power_tower' ),
[ 'power_tower_right', 'power' ] ],

    'power_tower_right' : [
'powers_and_roots', 'calculates list n as a right-associative power tower',
'''
This operator calculates the result of interpreting list n as a
right-associative "power tower", meaning a succession of exponentiations:

( n1 ^ ( n2 ^ ( n3 ^ n4 ) ) ) ...
''',
'''
Right-associative exponentiation makes for huge results:
''' + makeCommandExample( '[ 2 3 4 5 ] power_tower_right' ) + '''
''' + makeCommandExample( '[ 4.1 7.6 2.5 3.8 ] power_tower_right' ) + '''
An approximation of the infinite tetration of i
''' + makeCommandExample( '-a20 [ 1j 1000 dup ] power_tower_right' ),
[ 'power_tower', 'power' ] ],

    'powmod' : [
'powers_and_roots', 'calculates a to the bth power modulo c',
'''
This operator calculates a to the bth power modulo c.

a, b and c must be integers.
''',
'''
''' + makeCommandExample( '2 100 1024 powmod' ) + '''
''' + makeCommandExample( '34765 894574 100000 powmod' ),
[ 'power', 'modulo' ] ],

    'root' : [
'powers_and_roots', 'calculates the kth root of n',
'''
This operator calculates the kth root of n.
''',
'''
''' + makeCommandExample( '2 12 root' ) + '''
''' + makeCommandExample( '1 10 range 2 //' ) + '''
''' + makeCommandExample( '4 foot^2 2 //' ) + '''
''' + makeCommandExample( 'e i //' ),
[ 'power', 'square_root', 'cube_root', 'square_super_root' ] ],

    'square' : [
'powers_and_roots', 'calculates the square of n',
'''
This operator calculates the square of n.  It is the equivalent of 'n 2 power'.
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
This operator calculates the square root of n.  It is the equivalent of
'n 2 root'.
''',
'''
''' + makeCommandExample( '2 square_root' ) + '''
''' + makeCommandExample( '64 feet^2 square_root' ) + '''
''' + makeCommandExample( '5 sqrt 1 + 2 /' ),
[ 'square', 'cube_root', 'root', 'square_super_root' ] ],

    'square_super_root' : [
'powers_and_roots', 'calculates the square super-root of n',
'''
The operator calculates the square super-root of n. It returns x such that
x^x = n.
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
This operator calculates the principal, real, kth super-root of n.

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
This operator calculates all of the kth super-roots of n.

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

rpnChilada does support real operands for n, but k must be a non-negative
integer.

This version of the tetration operator is left-associative, and the equivalent
operation using exponentiation is shown in the examples.
''',
'''
''' + makeCommandExample( '3 3 tetrate' ) + '''
''' + makeCommandExample( '3 3 ** 3 **' ) + '''
''' + makeCommandExample( '10 10 tetrate' ) + '''
''' + makeCommandExample( '2 1 6 range tetrate' ),
[ 'power', 'tetrate_right', 'hyperoperator' ] ],

    'tetrate_right' : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
Tetration is the process of repeated exponentiation.  n is exponentiated by
itself k times.

This version of the tetration operator is right-associative, and the equivalent
operation using exponentiation is shown in the examples.  This results in much
larger numbers, and it's easy to overflow rpn.
''',
'''
''' + makeCommandExample( '3 3 tetrate' ) + '''
''' + makeCommandExample( '3 3 3 ** **' ) + '''
''' + makeCommandExample( '5 3 tetrate_right' ) + '''
''' + makeCommandExample( '2 1 5 range tetrate_right' ),
[ 'tetrate', 'power', 'hyperoperator_right' ] ],


    #******************************************************************************
    #
    #  prime number operators
    #
    #******************************************************************************

    'balanced_prime' : [
'prime_numbers', 'calculates the first of the nth set of balanced primes',
'''
This operator calculates the nth balanced prime.

A balanced prime is a prime which is the average of its immediate pair
of prime neighbors.

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
This operator calculates the nth set of balanced primes.  It prints the 3 prime
numbers that make up the nth balanced prime and its pair of prime neighbors.

A balanced prime is a prime which is the average of its immediate pair of prime
neighbors.

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
'prime_numbers', 'calculates the nth cousin prime',
'''
This operator calculates the first member of the nth set of cousin primes.

Cousin primes are primes that are separated by 4.  The first of a pair of
cousin primes must end with the digit 3, 7, or 9, because if a prime ends with
a 1, then a number 4 great cannot be a prime, since it ends with 5.

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
'prime_numbers', 'calculates the nth set of cousin primes',
'''
This operator calculates the nth set of cousin primes.  It returns the both
members of the nth set of cousin primes.

Cousin primes are primes that are separated by 4.  The first of a pair of
cousin primes must end with the digit 3, 7, or 9, because if a prime ends with
a 1, then a number 4 great cannot be a prime, since it ends with 5.

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
'prime_numbers', 'calculates the nth double balanced prime',
'''
This operator calculates the nth double balanced prime.

A double balanced prime is a prime which is the average of its immediate pair
of prime neighbors, and its nextmost immediate pair of prime neighbors.

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
This operator prints the 5 prime numbers that make up the nth double balanced
prime and its two nested pairs of prime neighbors.

A double balanced prime is a prime which is the average of its immediate pair
of prime neighbors, and its second pair of prime neighbors.

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
'prime_numbers', 'calculates the nth isolated prime',
'''
This operator calculates the nth isolated prime.

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
'prime_numbers', 'calculates the next prime number greater than n',
'''
This operator calculates the next prime number greater than n.

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
'prime_numbers', 'calculates the next k smallest prime numbers greater than n',
'''
This operator calculates the next k prime numbers greater n.
''',
'''
''' + makeCommandExample( '100 10 next_primes' ) + '''
''' + makeCommandExample( '-a71 10 70 ** random_int 5 next_primes -s1' ),
[ 'prime', 'primes', 'next_prime', 'previous_primes' ] ],

    'next_quadruplet_prime' : [
'prime_numbers', 'calculates the first member of the smallest set of quadruplet primes above n',
'''
This operator calculates the first member of the smallest set of quadruplet
primes greater than n.

A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.
''',
'''
''' + makeCommandExample( '100 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '1,000 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_quadruplet_prime' ) + '''
''' + makeCommandExample( '100,000 next_quadruplet_prime' ),
[ 'quadruplet_prime', 'nth_quadruplet_prime', 'quadruplet_primes', 'next_quadruplet_primes' ] ],

    'next_quadruplet_primes' : [
'prime_numbers', 'calculates the smallest set of quadruplet primes above n',
'''
This operator calculates the smallest set of quadruplet primes greater than n.

A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.
''',
'''
''' + makeCommandExample( '100 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '1,000 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_quadruplet_primes' ) + '''
''' + makeCommandExample( '100,000 next_quadruplet_primes' ),
[ 'quadruplet_prime', 'nth_quadruplet_prime', 'quadruplet_primes', 'next_quadruplet_prime' ] ],

    'next_quintuplet_prime' : [
'prime_numbers', 'calculates the first member of the smallest set of quintuplet primes above n',
'''
This operator calculates the first member of the smallest set of quintuplet
primes greater than n.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equivalent.
''',
'''
''' + makeCommandExample( '100 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_quintuplet_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_quintuplet_prime' ),
[ 'quintuplet_primes', 'quintuplet_prime', 'nth_quintuplet_prime', 'next_quintuplet_primes' ] ],

    'next_quintuplet_primes' : [
'prime_numbers', 'calculates the the smallest set of quintuplet primes above n',
'''
This operator calculates the smallest set of quintuplet primes greater than n.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equivalent.
''',
'''
''' + makeCommandExample( '100 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_quintuplet_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_quintuplet_primes' ),
[ 'quintuplet_primes', 'quintuplet_prime', 'nth_quintuplet_prime', 'next_quintuplet_primes' ] ],

    'next_sextuplet_prime' : [
'prime_numbers', 'calculates the first member of the smallest set of sextuplet primes above n',
'''
This operator calculates the first member of the smallest set of sextuplet
primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_sextuplet_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_sextuplet_prime' ),
[ 'sextuplet_primes', 'sextuplet_prime', 'nth_sextuplet_prime', 'next_sextuplet_primes' ] ],

    'next_sextuplet_primes' : [
'prime_numbers', 'calculates the the smallest set of sextuplet primes above n',
'''
This operator calculates the smallest set of sextuplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_sextuplet_primes' ) + '''
''' + makeCommandExample( '100,000,000 next_sextuplet_primes' ),
[ 'sextuplet_primes', 'sextuplet_prime', 'nth_sextuplet_prime', 'next_sextuplet_primes' ] ],

    'next_triplet_prime' : [
'prime_numbers', 'calculates the next first member of the smallest set of triplet primes above n',
'''
This operator calculates the first member of the smallest set of triplet primes
greater than n.
''',
'''
''' + makeCommandExample( '100 next_triplet_prime' ) + '''
''' + makeCommandExample( '10,000 next_triplet_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_triplet_prime' ) + '''
''' + makeCommandExample( '1,000,000,000 next_triplet_prime' ),
[ 'triplet_prime', 'nth_triplet_prime', 'triplet_primes' ] ],

    'next_triplet_primes' : [
'prime_numbers', 'calculates the smallest set of triplet primes above n',
'''
This operator calculates smallest set of triplet primes greater than n.
''',
'''
''' + makeCommandExample( '100 next_triplet_primes' ) + '''
''' + makeCommandExample( '10,000 next_triplet_primes' ) + '''
''' + makeCommandExample( '1,000,000 next_triplet_primes' ),
[ 'triplet_prime', 'nth_triplet_prime', 'triplet_primes' ] ],

    'next_twin_prime' : [
'prime_numbers', 'calculates the first member of the smallest set of twin primes above n',
'''
This operator calculates the first member of the smallest set of twin primes
greater than n.
''',
'''
''' + makeCommandExample( '100 next_twin_prime' ) + '''
''' + makeCommandExample( '10,000 next_twin_prime' ) + '''
''' + makeCommandExample( '1,000,000 next_twin_prime' ) + '''
''' + makeCommandExample( '100,000,000 next_twin_prime' ),
[ 'twin_prime', 'nth_twin_prime', 'twin_primes' ] ],

    'next_twin_primes' : [
'prime_numbers', 'calculates the smallest set of twin primes above n',
'''
This operator calculates the smallest set of twin primes greater than n.

Twin primes are prime numbers that have a difference of 2.
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
This operator finds the index of the prime number that is closest to, but not
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
This operator finds the index of the first of the closest quadruplet prime set
greater than n.

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
''' + makeCommandExample( '3 quadruplet_prime' ) + '''
''' + makeCommandExample( '10000 nth_quadruplet_prime' ) + '''
''' + makeCommandExample( '13 quadruplet_primes' ),
[ 'quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'nth_quintuplet_prime' : [
'prime_numbers', 'finds the index of the first of the closest quintuplet prime set greater than n',
'''
This operator finds the index of the prime quintuplet whose first member is
closest to, but not larger than n.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equvalent.

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
''' + makeCommandExample( '100,000 nth_sextuplet_prime' ) + '''
''' + makeCommandExample( '7 sextuplet_primes' ) + '''
''' + makeCommandExample( '100,000,000,000 nth_sextuplet_prime' ) + '''
''' + makeCommandExample( '8627 sextuplet_primes' ),
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
''' + makeCommandExample( '4 11 polyprime -c' ),
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
'prime_numbers', 'calculates the nth set of quadruplet primes',
'''
This operator calculates a list containing the four members of the nth prime
quadruplet.

A prime quadruplet is a set of four primes of the form p, p+2, p+6, p+8.  This
is the closest possible grouping of four primes larger than 3, and is the only
prime constellation of length 4.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range quadruplet_primes -s1' ),
[ 'nth_quadruplet_prime', 'next_quadruplet_prime', 'quadruplet_primes' ] ],

    'quintuplet_prime' : [
'prime_numbers', 'finds the first of the nth set of quintruplet primes',
'''
This operator returns the a first of the 5 primes that make up the nth prime
quintuplet.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 or p+12 is also prime, then
the five primes form a prime quintuplet which is the closest admissible
constellation of five primes.   rpn considers the two kinds of quintuplets
(ones with p-4 and ones with p+12) as equivalent.

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
This operator returns the nth safe prime.

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
'prime_numbers', 'calculates the first of the nth set of sextuplet primes',
'''
This operator calculates the first of the six primes that make up the nth prime
sextuplet.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 and p+12 are both also prime,
then the six primes are a prime sextuplet.

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
'prime_numbers', 'calculates the nth set of sextuplet primes',
'''
This operator calculates the nth set of sextuplet primes.  It returns the a list
of the six primes that make up the nth prime sextuplet.

If p, p+2, p+6, p+8 is a prime quadruplet and p-4 and p+12 are both also prime,
then the six primes are a prime sextuplet.

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
'prime_numbers', 'calculates the first of the nth set of sexy primes',
'''
This operator calculates the first of the nth set of sexy primes.

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
'prime_numbers', 'calculates the nth set of sexy primes',
'''
This operator calculates the nth set of sexy primes.

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
'prime_numbers', 'calculates the first of the nth set of sexy triplet primes',
'''
This operator calculates the first of the nth set of sexy triplet primes.

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
'prime_numbers', 'calculates the nth set of sexy triplet primes',
'''
This operator calculates a list of the three primes that form the nth sexy
triplet.

Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 is also prime, then this
forms a "sexy triplet".

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
'prime_numbers', 'calculates the first of the nth set of sexy quadruplet primes',
'''
This operator calculates the first of the four primes that form the nth sexy
quadruplet.

Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 and n + 18 are also both
prime, then this forms a "sexy quadruplet".

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
'prime_numbers', 'calculates the nth set of sexy quadruplet primes',
'''
This operator calculates a list of the four primes that form the nth sexy
quadruplet.

Sexy primes are defined to be a pair of numbers, n and n + 6, which are both
prime.  n + 2 or n + 4 may also be prime.  If n + 12 and n + 18 are also both
prime, then this forms a "sexy quadruplet".

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
'prime_numbers', 'calculates the nth Sophie Germain prime',
'''
This operator calculates the nth Sophie Germain prime.

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
'prime_numbers', 'calculates the nth super prime (the nth primeth prime)',
'''
This operator calculates the mth prime where m is the nth prime.

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
'prime_numbers', 'calculates the nth triple balanced prime',
'''
This operator calculates the nth triple balanced prime.

A triple balanced prime is a prime which is the average of its immediate pair
of prime neighbors, its second pair of prime neighbors and its third pair of
prime neighbors.

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
'prime_numbers', 'calculates the nth triple balanced prime and its neighbors',
'''
This operator calculates the 7 prime numbers that make up the nth triple
balanced prime and its three nested pairs of prime neighbors.

A triple balanced prime is a prime which is the average of its immediate pair
of prime neighbors, its second pair of prime neighbors and its third pair of
prime neighbors.

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
'prime_numbers', 'calculates the first of the nth set of triplet primes',
'''
This operator calculates the first of the three primes in the nth prime triplet.

A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.

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
'prime_numbers', 'calculates the nth set of triplet primes',
'''
This operator calculates a list of the three primes in the nth prime triplet.

A set of triplet primes are three prime numbers that are as close as they
can be, either n, n + 2, n + 6, or n, n + 4, n + 6.

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
'prime_numbers', 'calculates the first of the nth set of twin primes',
'''
This operator calculates the first of the two primes that make up the nth twin
prime pair.

Twin primes are prime numbers separated by 2.  The first twin prime pair
consists of 3 and 5.  It is conjectured that there infinitely many twin primes.

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
'prime_numbers', 'calculates the nth set of twin primes',
'''
This operator calculates a list of the two priems that make up the nth twin
prime pair.

Twin primes are prime numbers separated by 2.  The first twin prime pair
consists of 3 and 5.  It is conjectured that there infinitely many twin primes.

Prime numbers can be calculated from scratch, but this would be excessively
slow.  rpnChilada supports caching prime values to data files in ''' +
g.dataDir + '''/ and is distributed with data files calculated
through several billion primes.
''',
'''
''' + makeCommandExample( '1 10 range twin_primes' ) + '''
''' + makeCommandExample( '157 twin_primes' ) + '''
An _extremely_ crude estimation of Brun's twin prime constant:
''' + makeCommandExample( '1 1000 range twin_primes 1/x sum sum', indent=4, slow=True ),
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
''',
[ 'precision' ] ],

    'comma' : [
'settings', 'allows changing the comma option in interactive mode',
'''
This operator allows changing the comma option in interactive mode.
''',
'''
rpn (1)>5 12 **
244140625
rpn (2)>true comma
1
rpn (3)>5 12 **
244,140,625
rpn (4)>false comma
0
rpn (5)>5 12 **
244140625
''',
[ 'comma_mode' ] ],

    'comma_mode' : [
'settings', 'sets temporary comma mode in interactive mode',
'''
This operator sets comma mode to true for a single expression, the one one
'comma_mode' appears in.

Other than modifying the flag that turns on comma mode, this operator is
ignored by rpnChilada.
''',
'''
rpn (1)> 2 23 **
8388608
rpn (2)> comma_mode 2 23 **
8,388,608
rpn (3)> 2 23 **
8388608
''',
[ 'comma' ] ],

    'decimal_grouping' : [
'settings', 'used in interactive mode to set the decimal grouping level',
'''
This operator is used in interactive mode to set the decimal grouping level.
''',
'''
rpn (1)> pi
3.14159265359
rpn (2)> 3 decimal_grouping
3
rpn (3)> pi
3.141 592 653 59
''',
[ 'integer_grouping' ] ],

    'hex_mode' : [
'settings', 'set temporary hex mode in interactive mode',
'''
This operator is used in interactive mode to temporarily set hexadecimal mode to
true, just for that expression.  Then it returns to the default behavior.

Hexadecimal mode consists of base 16 output, an integer grouping of 4, and
leading zero mode set to true.

Other than modifying the flag that turns on hexadecimal mode, this operator is
ignored by rpnChilada.
''',
'''
rpn (1)> 45 47 *
2115
rpn (2)> hex_mode 47 47 *
08a1
rpn (3)> 45 47 *
2115
''',
[ 'octal_mode', 'output_radix' ] ],

    'identify' : [
'settings', 'set identify mode in interactive mode',
'''
This operator sets identify mode in interactive mode.
''',
'''
''',
[ 'identify_mode' ] ],

    'identify_mode' : [
'settings', 'set temporary identify mode in interactive mode',
'''
This operator is used in interactive mode to temporarily turn on identify mode,
just for the current expression.  Then it returns to the default behavior.

Other than modifying the flag that turns on identify mode, this operator is
ignored by rpnChilada.
''',
'''
''',
[ 'identify' ] ],

    'input_radix' : [
'settings', 'used in interactive mode to set the input radix',
'''
This operator is used to set the input radix in interactive mode.  When the
input radix is set to something other than 10, all input will be interpreted as
being in that base.
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
This operator is used in interactive mode to set the integer grouping size.
''',
'''
rpn (2)> 13 8 **
815730721
rpn (3)> 3 integer_grouping
3
rpn (4)> 13 8 **
815 730 721
rpn (5)> 4 integer_grouping
4
rpn (6)> 13 8 **
8 1573 0721
rpn (7)> default integer_grouping
3
''',
[ 'integer_grouping' ] ],

    'leading_zero' : [
'settings', 'when set to true and integer grouping is being used, output will include leading zeroes',
'''
This operator is used to set the leading zero mode, which will cause the most
significant integer grouping (if it's set to a non-zero value) to be back-filled
with zeroes.
''',
'''
rpn (3)> 432935874
4 3293 5874
rpn (4)> 1 leading_zero
0000
rpn (5)> 432935874
0004 3293 5874
''',
[ 'leading_zero_mode' ] ],

    'leading_zero_mode' : [
'settings', 'sets temporary leading zero mode in interactive mode',
'''
This operator is used in interactive mode to temporarily set the leading zero
mode to true, just for that expression.  Then it returns to the default
behavior.

Other than modifying the flag that turns on leading zero mode, this operator is
ignored by rpnChilada.
''',
'''
rpn (13)> 2439085424
24 3908 5424
rpn (14)> leading_zero_mode 2439085424
0024 3908 5424
rpn (15)> 2439085424
24 3908 5424
''',
[ 'leading_zero' ] ],

    'octal_mode' : [
'settings', 'sets temporary octal mode in interactive mode',
'''
This operator is used in interactive mode to temporarily set octal mode to true,
just for that expression.  Then it returns to the default behavior.

Octal mode consists of base 8 output, an integer grouping of 3, and leading zero
mode set to true.

Other than modifying the flag that turns on octal mode, this operator is
ignored by rpnChilada.
''',
'''
rpn (1)> 693
693
rpn (2)> octal_mode 693
001 265
rpn (3)> 693
693
''',
[ 'hex_mode', 'output_radix' ] ],

    'output_radix' : [
'settings', 'used in the interactive mode to set the output radix',
'''
This operator is used to set the output radix in interactive mode.  When the
output radix is set to n, all numerical output will be in base n.
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
This operator used in interactive mode to set the output precision.  When the
precision is set, if the accuracy is lower than that value, it will also be
increased to the same level.
''',
'''
''',
[ 'accuracy' ] ],

    'timer' : [
'settings', 'set timer mode in interactive mode',
'''
This operator is used in interactive mode to turn timer mode on and off.  If
it's turned on ('true timer'), then every operator will be followed with a
print-out of the time it took.
''',
'''
''',
[ 'timer_mode' ] ],

    'timer_mode' : [
'settings', 'set temporary timer mode in interactive mode',
'''
This operator is used in interactive mode to temporarily set the timer mode to
true, just for that expression.  Then it returns to the default behavior.

When the timer mode is true, rpnChilada will output the time it takes to
evaluate each expression.

Other than modifying the flag that turns on timer mode, this operator is
ignored by rpnChilada.
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

#    'constant' : [
#'special', 'creates a user-defined constant',
#'''
#This operator is not implemented yet!
#''',
#'''
#''',
#[ 'set_variable' ] ],

    'delete_config' : [
'special', 'delete configuration setting n',
'''
This operator deletes the entry for n in the configuration file.
''',
'''
c:\\> rpn test1 fred set_config
fred

c:\\> rpn dump_config
test1: "fred"

1

c:\\> rpn test1 delete_config
test1

c:\\> rpn dump_config

0
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

    'dump_variables' : [
'special', 'dumps all user-defined variables',
'''
Tis operator dumps the user-defined variables.
''',
'''
c:\\>rpn dump_variables
fred: "3.1415926535897932385"
barney: "31.0"
foo: "2020-09-07T11:52:37.008158-04:00"

3
''',
[ 'set_variable', 'get_variable', 'dump_variables' ] ],

    'describe' : [
'special', 'outputs a list of properties of integer n',
'''
This is a special operator whose output is simply printed to the console.  The
actual return value of the operator is the integer argument, so from RPN's
point of view, it doesn't actually do anything interesting.
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
'special', 'reads a list of values from a text file',
'''
The text file should have one number per line, and the values are subject to the
same processing as numerical values on the rpn command line.
''',
'''
c:\\>cat test.txt
1
9
11
13
16

c:\\>rpn test.txt list_from_file
[ 1, 9, 11, 13, 16 ]
''',
[ 'number_from_file', 'set_variable', 'get_variable' ] ],

    'name' : [
'special', 'returns the English name for the integer value or measurement n',
'''
This operator returns the English name for any integer n.

The upper limit of integers rpn can name is 10^3003 - 1.

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

    'number_from_file' : [
'special', 'reads a number from a text file',
'''
This operator reads a number from an ASCII text file.  The contents of the text
file are interpreted as a single number composed of all characters '0' - '9'
contained in the text file, without regarding any other characters, including
whitespace.
''',
'''
c:\\>cat test.txt
365093519915713555773254766
479531418686699271736651614
c:\\>rpn test.txt number_from_file
365093519915713555773254766479531418686699271736651614
''',
[ 'list_from_file', 'set_variable', 'get_variable' ] ],

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

The upper limit of integers rpn can name is 10^3003 - 1.

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

The second option is:

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
''' + makeCommandExample( '4 random_int 1 + 4 roll_simple_dice' ),
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
The operator prints a list of help topics, but only in interactive help mode.
The equivalent information can be printed out from the command-line simply with
"rpn help".

TODO:  Just made the stupid thing do the same in non-interactive mode.
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
''' + makeCommandExample( '60 degrees tanh' ) + '''
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

        operatorHelp[ constant ] = [
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

    if not QUIET_MODE:
        for topic, helpInfo in operatorHelp.items( ):
            if len( helpInfo ) != 5:
                print( 'error: malformed help data for topic \'' + topic + '\'' )
                continue

            if not helpInfo[ 0 ]:
                noCategory.append( topic )

            if not helpInfo[ 1 ]:
                noDescription.append( topic )

            if ( not helpInfo[ 2 ] or helpInfo[ 2 ] == '\n' ) and \
               topic not in g.unitOperators:
                noHelpText.append( topic )

            if ( not helpInfo[ 3 ] or helpInfo[ 3 ] == '\n' ) and \
               ( topic not in g.unitOperators and topic not in constantOperators ):
                noExamples.append( topic )

            if len( helpInfo[ 4 ] ) == 0:
                noCrossReferences.append( topic )
            else:
                for crossReference in helpInfo[ 4 ]:
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
