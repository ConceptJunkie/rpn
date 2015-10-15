rpn is a command-line Reverse-Polish Notation calculator.

rpn supports arithmetic with arbitrary precision, powers and roots, logarithms,
algebraic functions (including polynomials arithmetic and solving),
trigonometric functions, complex numbers, computer science related functions
(bitwise math, base conversion), number theory functions, astronomical
functions, prime number calculations and lookup, can operate with single
operands or lists of operands and supports a wide variety of flexible unit
conversions comparable to the GNU units program.

****

UPDATE - October 15, 2015

I've decided the upcoming release will be version 7 since so much has been
added, a lot has been reorganized and I've gotten serious about unit tests.

An official release of version 7 probably won't be for a while, because I
really want to be able to release it on PyPI.  There's a lot of work I want to
do before cutting another release, and it's going to take some time, but the
current git master contains all the latest features and is working fine.

rpn should still work on Android, but there are problems with the ephem
library.  I think it has to do with building the AstroLib code, and haven't had
a chance to try to diagnose the problem.

UPDATE - August 5, 2015

I am working on creating a wheel for rpn, and I'm hoping I can also make it
Python 2 compatible before cutting another release.  The biggest roadblock is
just getting some round tuits instead of adding in new operators, which is much
more fun.

Another cool update:  rpn can now be run on Android with the Termux app
(http://termux.com/)!  Right now, it fails a unit test having to do with date
formatting, which I haven't gotten around to investigating, but otherwise it
works great.  Where else can you factor a 50-digit number on your Android
device?

The current release is 6.4.0.

rpn is a console app and can be launched from the command-line.  However,
there is now an "interactive mode" and an icon to launch rpn for Windows users.

Running RPN using the Windows installer:

The installer includes the compiled help file, unit conversion tables and
prime number lookup tables.  Clicking on the icon will launch an rpn "shell",
which works just like running rpn from the command-line, except you don't need
to say "python rpn.py".

There are operators to perform the same thing normally done with command-line
switches.

See "rpn help settings" for more information.

Running RPN using the source:

rpn is written in Python 3, and requires several libraries for the hard math
stuff (gmpy2 is optional, but recommended for improved performance).

If you have pip installed, you can install the prerequisites with the
following:

    pip install pyprimes
    pip install mpmath
    pip install gmpy2
    pip install arrow
    pip install pyreadline
    pip install ephem
    pip install convertdate
    pip install geopy

Before running rpn, you should run the scripts to generate the data files that
rpn uses for displaying help, doing unit conversions, and looking up various
prime numbers.

    python makeUnits.py
    python makeHelp.py
    python preparePrimeData.py

Using rpn:

rpn is very easy to use.  It's just like any RPN calculator:  Operands go first,
then the operators.  All examples assume "rpn" is an alias for "python
/<path-to-rpn>/rpn.py".  In interactive mode, you leave off the "rpn".

For instance:

    rpn 2 2 +

will calculate 2 + 2.

rpn supports more than 600 operators.  ('rpn _dumpops' will list them all.)

The entire operator list is also included at the bottom of this document.

rpn has pretty extensive built-in help, although the help files are not
complete.  However, all operators have at least a brief description, and most
are obvious enough to use easily.

Start with "rpn help" for an overview.  To dive right in, see "rpn help
examples".  In interactive mode, typing "help" will launch help mode.   Then,
"topics" will print out a list of help topics and "exit" will return to rpn.

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 6.4.0 isn't finished as a standalone program).

The data files are stored in the same location as rpn.py in a subdirectory
called rpndata/.  In the Windows installer version, they are stored in the same
directory as the EXE.

If you really want to generate prime numbers, see my "primes" project:
https://github.com/ConceptJunkie/primes   I've calculated the first 10 billion
prime numbers and will someday update the rpn lookup tables.

rpn also provides a simple interface for accessing The On-Line Encyclopedia of
Integer Sequences (http://oeis.org), see "rpn help special" and "rpn help
oeis".

Feedback, Comments, Bug Reports:

Any feedback is welcome at rickg@his.com.  This was originally an exercise to
learn Python, but slowly blossomed into something really useful and fun, so I
wanted to share it.  rpn also exposes just a few of the features of the amazing
mpmath library (by Fredrik Johansson, http://mpmath.org/) which is where
almost all the hard math stuff is actually done.

Rick Gutleber
rickg@his.com

p.s. rpn is licensed under the GNU GPL version 3.0.  See (see
<http://www.gnu.org/licenses/gpl.html> for more information).

Release Notes:

6.4.0 - "Factoring Fun"

Revamped factorization to be much, much faster, using the Brent-Pollard
algorithm instead of just brute-force dividing.   More to come...

Added the 'magnetic_constant', 'electric_constant', 'rydberg_constant',
'newtons_constant' and 'fine_structure' operators.

Added 'eulerphi' operator.

Added caching for factorizations.  I often factor the same numbers over and
over (like when I'm playing with the Fibonaccis) so it made sense to cache the
results for non-trivial factoring.

Added the 'sigma, 'aliquot', 'polypower', 'mobius' and 'mertens' operators.
The old 'mertens' operator was renamed to 'mertens_constant'.  The 'aliquot'
operator is another use-case for caching factorizations... try it with 276.
rpn can can now factor the first 450 or so in a reasonably short time.

Added the 'frobenius', 'slice', 'sublist', 'left' and 'right' operators.

Added 'crt' operator.

...and the usual slew of bug fixes.

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

Added the 'lcm' operator.

The 'pascal' operator was renamed to 'pascaltri' to avoid a collision with
the 'pascal' unit.

Fixed several minor bugs.

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

abs accuracy acos acosh acot acoth acsc acsch add add_digits aliquot
alternate_signs alternate_signs_2 alternating_factorial alternating_sum
alternating_sum_2 and apery append april argument asec asech ash_wednesday asin
asinh astronomical_dawn astronomical_dusk atan atanh august autumnal_equinox
avogadro balanced_prime balanced_prime_ base bell bell_polynomial bernoulli
binomial calendar carol catalan ceiling centered_cube centered_decagonal
centered_heptagonal centered_hexagonal centered_nonagonal centered_octagonal
centered_pentagonal centered_polygonal centered_square centered_triangular cf
champernowne char combine_digits comma comma_mode compositions conjugate
convert copeland cos cosh cot coth count count_bits count_divisors cousin_prime
cousin_prime_ crt csc csch cube cube_root dawn debruijn decagonal
decagonal_centered_square decagonal_heptagonal decagonal_hexagonal
decagonal_nonagonal decagonal_octagonal decagonal_pentagonal
decagonal_triangular december decimal_grouping default delannoy dhms diffs
diffs2 distance divide divisors dms dodecahedral double double_balanced
double_balanced_ double_factorial dst_end dst_start dup_digits dup_operator
dup_term dusk e easter ecm eddington_number egypt election_day
electric_constant element estimate euler euler_brick euler_phi eval eval2 eval3
eval_poly exp exp10 exponential_range expphi factor factorial false
faradays_constant february fibonacci fibonorial filter filter_by_index
find_palindrome find_poly fine_structure flatten float floor fraction friday
frobenius from_bahai from_hebrew from_indian_civil from_islamic from_julian
from_mayan from_persian from_unix_time gamma gcd geometric_mean geometric_range
get_digits glaisher group_elements harmonic help heptagonal
heptagonal_hexagonal heptagonal_pentagonal heptagonal_square
heptagonal_triangular heptanacci hexagonal hexagonal_pentagonal
hexagonal_square hexanacci hex_mode hms hyper4_2 hyperfactorial hypotenuse i
icosahedral identify identify_mode imaginary infinity input_radix integer
integer_grouping interleave intersection invert_units isolated_prime iso_day
is_abundant is_achilles is_deficient is_divisible is_equal is_even is_greater
is_k_semiprime is_less is_not_equal is_not_greater is_not_less is_not_zero
is_odd is_palindrome is_pandigital is_perfect is_powerful is_prime is_pronic
is_rough is_semiprime is_smooth is_sphenic is_square is_squarefree is_unusual
is_zero itoi jacobsthal january july june jupiter khinchin kynea labor_day lah
lambertw latlong latlong_to_nac lcm leading_zero leading_zero_mode left
leonardo leyland lgamma li limit limitn linear_recurrence ln location
location_info log10 log2 logxy long longlong lucas magnetic_constant make_cf
make_iso_time make_julian_time make_pyth_3 make_pyth_4 make_time march mars max
max_char max_double max_float max_index max_long max_longlong max_quadlong
max_short max_uchar max_ulong max_ulonglong max_uquadlong max_ushort may mean
memorial_day mercury mertens mertens_constant mills min min_char min_double
min_float min_index min_long min_longlong min_quadlong min_short min_uchar
min_ulong min_ulonglong min_uquadlong min_ushort mobius modulo monday moon
moonrise moonset moon_antitransit moon_phase moon_transit motzkin
multifactorial multiply multiply_digits name nand narayana nautical_dawn
nautical_dusk nearest_int negate negative negative_infinity neptune
newtons_constant next_antitransit next_first_quarter_moon next_full_moon
next_last_quarter_moon next_new_moon next_prime next_prime_index
next_quadruplet_prime next_quadruplet_prime_index next_quintuplet_prime
next_rising next_setting next_transit nonagonal nonagonal_heptagonal
nonagonal_hexagonal nonagonal_octagonal nonagonal_pentagonal nonagonal_square
nonagonal_triangular nonzero nor not november now nprod nsum nth_apery
nth_catalan nth_centered_decagonal nth_centered_heptagonal
nth_centered_hexagonal nth_centered_nonagonal nth_centered_octagonal
nth_centered_pentagonal nth_centered_polygonal nth_centered_square
nth_centered_triangular nth_decagonal nth_heptagonal nth_hexagonal
nth_nonagonal nth_octagonal nth_pentagonal nth_polygonal nth_square
nth_triangular nth_weekday nth_weekday_of_year n_sphere_area n_sphere_radius
n_sphere_volume occurrences octagonal octagonal_heptagonal octagonal_hexagonal
octagonal_pentagonal octagonal_square octagonal_triangular octahedral
octal_mode october oeis oeis_comment oeis_ex oeis_name omega or ordinal_name
output_radix pack padovan parity partitions pascal_triangle pell pentagonal
pentagonal_square pentagonal_triangular pentanacci pentatope permutations phi
pi plastic plot plot2 plotc pluto polyadd polygamma polygonal polygon_area
polylog polymul polypower polyprime polyprod polysum polytope power powmod
precision presidents_day previous previous_antitransit
previous_first_quarter_moon previous_full_moon previous_last_quarter_moon
previous_new_moon previous_rising previous_setting previous_transit prevost
prime primepi primes primorial product pyramid quadruplet_prime
quadruplet_prime_ quintuplet_prime quintuplet_prime_ radiation_constant random
random_ random_integer random_integer_ range range2 ratios real reciprocal
reduce repunit result reversal_addition reverse reverse_digits rhombdodec
riesel right robbins root round rydberg_constant safe_prime saturday saturn
schroeder sec sech september set sextuplet_prime sextuplet_prime_ sexy_prime
sexy_prime_ sexy_quadruplet sexy_quadruplet_ sexy_triplet sexy_triplet_
shift_left shift_right short shuffle sigma sign silver_ratio sin sinh
sky_location slice solar_noon solve solve2 solve3 solve4 sophie_prime sort
sort_descending sphere_area sphere_radius sphere_volume square square_root
square_triangular stddev stefan_boltzmann stella_octangula subfactorial sublist
subtract sum summer_solstice sum_digits sun sunday sunrise sunset
sun_antitransit superfactorial superprime sylvester tan tanh tetrahedral
tetranacci tetrate thabit thanksgiving thursday timer timer_mode today tomorrow
topic tower tower2 to_bahai to_bahai_name to_hebrew to_hebrew_name
to_indian_civil to_indian_civil_name to_islamic to_islamic_name to_iso
to_iso_name to_julian to_julian_day to_lilian_day to_mayan to_ordinal_date
to_persian to_persian_name to_unix_time triangle_area triangular tribonacci
triplet_prime triplet_prime_ triple_balanced triple_balanced_ true
truncated_octahedral truncated_tetrahedral tuesday twin_prime twin_prime_ uchar
uinteger ulong ulonglong undouble unfilter unfilter_by_index unfloat union
unique unit_roots unlist unpack uranus use_members ushort value venus
vernal_equinox wednesday weekday winter_solstice x xor y ydhms year_calendar
yesterday z zero zeta [ ] _dump_aliases _dump_operators _stats { }
