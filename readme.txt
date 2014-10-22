rpn is a command-line Reverse-Polish Notation calculator.

rpn supports arithmetic with arbitrary precision, powers and roots, logarithms,
algebraic functions (including polynomials arithmetic and solving),
trigonometric functions, complex numbers, computer science related functions
(bitwise math, base conversion), number theory functions, prime number
calculations and lookup, can operate with single operands or lists of operands
and supports a wide variety of flexible unit conversions comparable to the GNU
units program.

The current version is 5.28.5.

Version 5.28 has been dedicated primarily to bug-fixes, because there are lots
of dumb little bugs.  I particularly need to clean up the unit conversion
stuff.  It's a work in progress.

Installers for Windows can be found here:

https://www.strongspace.com/conceptjunkie/public/rpn-5.28.5-win32.msi
https://www.strongspace.com/conceptjunkie/public/rpn-5.28.5-amd64.msi

The additional prime number data adds approximately 50MB to the installer size.

https://www.strongspace.com/conceptjunkie/public/rpn_with_prime_data-5.28.5-win32.msi
https://www.strongspace.com/conceptjunkie/public/rpn_with_prime_data-5.28.5-amd64.msi

rpn is a console app and must be launched from the command-line.  The installer
includes the compiled help file, unit conversion tables and prime number lookup
tables.  The installer does not add rpn.exe to the Windows path, so a batch
file or alias will be useful for launching it.

Running RPN using the source:

rpn is written in Python 3, and requires the mpmath, pyprimes and arrow
libraries for most of the hard math stuff (gmpy2 is optional, but recommended).

If you have pip installed, you can install the prerequisites with the
following:

    pip install pyprimes
    pip install mpmath
    pip install gmpy2
    pip install arrow

Before running rpn, you should run makeHelp.py and makeUnits.py to generate
the data files that rpn uses for displaying help and doing unit conversions
respectively.

Using rpn:

rpn is very easy to use.  It's just like any RPN calculator:  Operands go first,
then the operators.

For instance:

    rpn 2 2 +

will calculate 2 + 2.  "rpn _dumpops" is an internal command that will list
all the implemented operators for the curious.  They are also listed in the
help text.

rpn has pretty extensive built-in help, although not all the help files are
complete yet.

Start with "rpn help" for an overview.  To dive right in, see "rpn help
examples".

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 5.20.0 isn't finished as a standalone program).

The data files are stored in the same location as rpn.py in a subdirectory
called rpndata/.  In the Windows installer version, they are stored in the same
directory as the EXE.

Until I fix makeRPNPrimes.py, if you really want to generate prime numbers, go
back to version 4 and check out the '_make*' commands.

rpn also provides a simple interface for querying The On-Line Encyclopedia of
Integer Sequences (http://oeis.org).

Feedback, Comments, Bug Reports:

Any feedback is welcome at rickg@his.com.  This was originally an exercise to
learn Python, but slowly blossomed into something really useful and fun, so I
wanted to share it.  rpn also exposes just a few of the features of the amazing
mpmath library (by Fredrik Johansson, http://mpmath.org/) which is where all
the hard stuff is actually done.

Rick Gutleber
rickg@his.com

p.s. rpn is licensed under the GNU GPL version 3.0.  See (see
<http://www.gnu.org/licenses/gpl.html> for more information).

Release Notes:

5.28.4

Added the 'diffs2' operator.

More bug fixes thanks to the test script!

5.28.3

The operators 'doublebal', doublebal_', 'triplebal', and 'triplebal_' now work
correctly.  The data files have been significantly expanded as well.

More prime number updates will come in the next few weeks.  My target is to
expand every table up to the first 10 billion primes.

5.28.2

Several bug fixes relating to 'estimate' and unit conversion.   Some unit types
were folded together because they had the same basic units (e.g., frequency and
radioactivity were both time ^ -1, which confused the conversion logic).

5.28.1

Added separate installers for the plain-vanilla rpn (with only the "small
primes" data file, i.e., the first million primes), and the installer with all
of the prime data files.

The 'primes' operator has been fixed so it works correctly for small values.

I'm currently testing the prime functions, which I haven't touched in a long
time, so more fixes will definitely be coming.  The balanced prime functions
are currently broken and will be fixed shortly, including updated data files.

5.28.0

Added 'x', 'eval', 'nsum', 'nprod', 'limit', 'limitn', 'infinity', and
'negative_infinity', and 'value' operators.

5.27.2

Help for unit types now prints out all aliases for the unit operators.

5.27.1

Added an error message if the 'name' operand is out of range, and added support
for negative numbers.

5.27.0

Added the 'name' operator.

5.26.0

Added dynamic_visocity and frequency unit types and a few bug fixes.

Added units for the days and years of the other 8 planets in the Solar System.

Added several constant units for quaint or archaic number terms like 'score'
and 'gross'.

Added mass units for common particle masses.

Updated some natural values (electron mass, etc.).

Fixed some problems with generating and interpreting compound units.

Added the 'prevost' operator.

5.25.0

Added Julian date operators, ISO date operators, calendar operators and the
'ash_wednesday' operator.  Added support for the density unit type and several
small bug fixes.

5.24.0

A few more bug fixes, plus new calendar-related operators:  easter.
election_day, labor_day, memorial_day, nthday, presidents_day, thanksgiving

5.23.1

The help improvements actually work now.  So much for testing.

There are now some examples of absolute time handling.

5.23.0

Help will now search topics for partial matches if a complete match isn't found.

5.22.0

Added a bunch of new constants for powers of 10.

5.21.2

Added -l to format help output for different line lengths.  However, it still
doesn't format the blockquoted help text.

5.21.1

Added percent operator, weekday now throws a proper error is the operand isn't
a time value.

5.21.0

The long-awaited absolute time feature:  rpn can now handle absolute time
values.  For input, just use ISO 8601 format, or a reasonable subset thereof.
There is also the 'maketime' operator, which takes a list similar to the old
'tounixtime' operator.

5.20.7

Added help for unit types.   Help for individual units will come eventually,
but they are pretty self-explanatory.

5.20.6

The prime? operator wasn't working correctly for small values.

5.20.5

rpn now throws an error when attempting to get the 0th or less prime number.

5.20.4

rpn now correctly reports the argument in question on any error.

5.20.3

Made a fix to improve rpn's reporting of the argument in question when there is
an error.  It's probably not 100% correct yet.

5.20.2

Fixed the list operator parsing so polyprod and polysum work correctly.

5.20.1

Several calls to polyval( ) had hard-coded fractions in them instead of calls
to fdiv( ), resulting in rounding errors.

5.20.0

rpn finally comes with an installer for Windows, in 32-bit and 64-bit flavors.

5.19.3

The test script has been rewritten in Python.  It's still very basic and only
does a sanity test to show every operator works without crashing.  It doesn't
test for correct answers yet.

5.19.2

rpn now outputs an empty list correctly.  The 'append' operator (to append
lists) has been fixed.

5.19.1

Fixed several problems with 'tounixtime' and 'fromunixtime'.

The first version of a test script is available as a batch file.

5.19.0

Added 'randint' operator.

5.18.7

compoundUnits was still being referred to without the "g." global specifier.

5.18.6

rpn now prints out an error message if you try to get help for an unknown
topic.

5.18.5

Fixed a bug concerning adding dissimilar units.

5.18.4

rpn now correctly parses "-0" as a value again.

5.18.3

Added 'split' as an alias for 'unpack' because I couldn't remember what it was
called.

Made some minor fixes made based on running pyflakes, pylint pep8, and the
test script.

5.18.2

Made a bunch of bug fixes that showed up as a result of reorganizing the code.

5.18.1

It's clear I haven't done any unit conversions in a while because there were
still issues with declarations of variables.  Now, I've started eliminating the
use of "global" in favor of a global module.

