rpn is a command-line Reverse-Polish Notation calculator.

rpn supports arithmetic with arbitrary precision, powers and roots, logarithms,
algebraic functions (including polynomials arithmetic and solving),
trigonometric functions, complex numbers, computer science related functions
(bitwise math, base conversion), number theory functions, prime number
calculations and lookup, can operate with single operands or lists of operands
and supports a wide variety of flexible unit conversions comparable to the GNU
units program.

****

The current version is 6.2.0.

Installers for Windows can be found here:

https://www.strongspace.com/conceptjunkie/public/setup_rpn-6.2.0-win32.exe
https://www.strongspace.com/conceptjunkie/public/setup-rpn-6.2.0-win64.exe

rpn is a console app and can be launched from the command-line.  However,
there is now an "interactive mode" and an icon to launch rpn for Windows users.

The installer includes the compiled help file, unit conversion tables and
prime number lookup tables.

Running RPN using the source:

rpn is written in Python 3, and requires the mpmath, pyprimes, readline and
arrow libraries for most of the hard math stuff (gmpy2 is optional, but
recommended).

If you have pip installed, you can install the prerequisites with the
following:

    pip install pyprimes
    pip install mpmath
    pip install gmpy2
    pip install arrow
    pip install readline  (or download an installer from here:
            http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyreadline)

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

rpn supports more than 400 operators.  The entire list is included at the
bottom of this document.

rpn has pretty extensive built-in help, although the help files are not
complete yet.

Start with "rpn help" for an overview.  To dive right in, see "rpn help
examples".  In interactive mode, typing "help" will launch help mode.   Then,
"topics" will print out a list of help topics and "exit" will return to rpn.

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 6.0.0 isn't finished as a standalone program).

The data files are stored in the same location as rpn.py in a subdirectory
called rpndata/.  In the Windows installer version, they are stored in the same
directory as the EXE.

If you really want to generate prime numbers, see my "primes" project:
https://github.com/ConceptJunkie/primes

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

6.1.0

New operators:  'maxdouble', 'maxfloat', 'mindouble', 'minfloat'

Base conversion for output is no longer limited to 1000 digits.  There's no
reason to do that.

'rpn 0 cf' now throws an error rather than dividing by 0.

6.0.1

Added code to prevent scientific notation from messing up base conversions for
the integral part of the number (up to 1000 digits).

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

5.28.5

More bug fixes and code cleanup.  Added the 'unfloat' and 'undouble' operators.

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

Operators supported by rpn:

[ ] abs accuracy acos acosh acot acoth acsc acsch add altfac altsign altsign2
altsum altsum2 and apery aperynum append april asec asech ash_wednesday asin
asinh atan atanh august avogadro balanced balanced_ base bell bellpoly
bernoulli binomial calendar carol catalan catalans cdecagonal cdecagonal?
ceiling centeredcube cf champernowne char cheptagonal cheptagonal? chexagonal
cnonagonal cnonagonal? coctagonal coctagonal? comma comma_mode convert copeland
cos cosh cot coth count countbits countdiv cousinprime cpentagonal cpentagonal?
cpolygonal cpolygonal? csc csch csquare csquare? ctriangular ctriangular? cube
debruijn decagonal decagonal? december decimal_grouping default delannoy dhms
diffs diffs2 divide divisors dms dodecahedral double doublebal doublebal_
doublefac dst_end dst_start dup e easter egypt election_day element equal
estimate euler eulerbrick eval eval2 eval3 exp exp10 expphi exprange factor
factorial false february fibonacci fibonorial filter find_poly flatten float
floor fraction friday fromunixtime gamma gcd georange glaisher greater harmonic
help heptagonal heptagonal? heptanacci hepthex heptpent heptsquare hepttri
hex_mode hexagonal hexagonal? hexanacci hexpent hms hyper4_2 hyperfac hypot i
icosahedral identify identify_mode infinity input_radix integer
integer_grouping interleave intersection isdivisible iso_day isolated isprime
issquare itoi jacobsthal january julian_day july june khinchin kynea labor_day
lah lambertw leading_zero leading_zero_mode less leyland lgamma li limit limitn
linearrecur ln log10 log2 logxy long longlong lucas makecf makeisotime
makejuliantime makepyth3 makepyth4 maketime march max maxchar maxdouble
maxfloat maxindex maxlong maxlonglong maxquadlong maxshort maxuchar maxulong
maxulonglong maxuquadlong maxushort may mean memorial_day mertens mills min
minchar mindouble minfloat minindex minlong minlonglong minquadlong minshort
minuchar minulong minulonglong minuquadlong minushort modulo monday motzkin
multiply name narayana negative negative_infinity nonagonal nonagonal? nonahept
nonahex nonaoct nonapent nonasquare nonatri nonzero not not_equal not_greater
not_less november now nprod nspherearea nsphereradius nspherevolume nsum
nthprime? nthquad? nthweekday nthweekdayofyear octagonal octagonal? octahedral
octal_mode octhept octhex october octpent octsquare octtri oeis oeiscomment
oeisex oeisname omega or output_radix pack padovan parity pascal pell
pentagonal pentagonal? pentanacci pentatope perm phi pi plastic plot plot2
plotc polyadd polyarea polygamma polygonal polygonal? polylog polymul polyprime
polyprod polysum polytope polyval power precision presidents_day previous
prevost prime prime? primepi primes primorial product pyramid quadprime
quadprime? quadprime_ quintprime quintprime_ randint randint_ random random_
range range2 ratios reciprocal reduce repunit result reverse rhombdodec riesel
robbins root root2 root3 round safeprime saturday schroeder sec sech september
set sextprime sextprime_ sexyprime sexyprime_ sexyquad sexyquad_ sexytriplet
sexytriplet_ shiftleft shiftright short sin sinh solve solve2 solve3 solve4
sophieprime sort sortdesc spherearea sphereradius spherevolume square squaretri
stddev steloct subfac subtract sum sunday superfac superprime sylvester tan
tanh tetrahedral tetranacci tetrate thabit thanksgiving thursday timer
timer_mode today topic tounixtime tower tower2 trianglearea triangular
triangular? tribonacci triplebal triplebal_ tripletprime true truncoct trunctet
tuesday twinprime twinprime_ uchar uinteger ulong ulonglong undouble unfloat
union unique unitroots unlist unlist unpack ushort value wednesday weekday x
xor y ydhms year_calendar z zero zeta ~

