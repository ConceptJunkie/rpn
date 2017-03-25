rpn is a command-line Reverse-Polish Notation calculator.

rpn supports arithmetic with arbitrary precision, powers and roots, logarithms,
algebraic functions (including polynomials arithmetic and solving),
trigonometric functions, complex numbers, computer science related functions
(bitwise math, base conversion), number theory functions, astronomical
functions, prime number calculations and lookup, can operate with single
operands or lists of operands and supports a wide variety of flexible unit
conversions comparable to the GNU units program.

****

UPDATE - August 15, 2016

I am very excited that people have started noticing rpn!

Please continue with comments, suggestions and bug reports.  rpn has lots of
little bugs and possibly some big ones, too, and although I have unit tests,
most of the time, I find bugs from using it.

I especially want to thank the folks at The Nineteenth Byte on Stack Exchange
for their nice comments.  I also love solving puzzles with rpn, so if there's
something you'd like to see it be able to do, drop me a line at rickg@his.com.

I'll try to focus on improving the help in the near future.

UPDATE - July 19, 2016

I don't know if anyone has ever looked at this project... not even my Mom.  But
anyhow, I wanted to leave an update anyway.  The "imminent" release of version
7 is anything but.  I have been too lazy to tackle trying to make the wheel
work correctly.  I've been making small additions here and there, including bug
fixes whenever I find problems.

Currently, my short list is topped with switching to SQLite for caching
function results to disk.  I was experimenting with the sigma function and
found that once the cache of values got past a million, loading it had become
unreasonably slow.  I think it would also be a very good idea to convert the
prime number data files to SQLite tables as well.

There are a few Python 2 compatibility problems that remain, and those should
be easy to fix, but I've been too busy with a combiniation of real life and
general laziness.  The conversion to using generators mentioned in the last
update is complete and has greatly improved performance for a lot of operators.

RPN continues to proceed slowly and it works just fine right now, so it can be
used just fine despite being a "pre-release".

UPDATE - November 16, 2015

The scope of changes for version 7 keeps growing.  The transition to lazy list
evaluation (using generators) is going to be a very big change and currently a
lot of operators are broken.

It is recommended that anyone using RPN from Git stick with the 7.0.alpha1 tag
for the time being.

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

****

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
	pip install tzlocal
	pip install timezonefinder

If you are running Python 2, you will also need:

    pip install enum34
    pip install pylru

Note:  Windows users will want to install ephem using the wheels provided here:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyephem

Before running rpn, you need to run the scripts to generate the data files that
rpn uses for displaying help, doing unit conversions, and looking up various
prime numbers.   These only needs to be run again if they change.

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

Operators supported by rpn (as of 7.0.alpha36):

[ ] _dump_aliases _dump_operators _stats aa_battery abs abundance acceleration
accuracy acos acosh acot acoth acsc acsch add add_digits add_polynomials agm
aliquot alpha_particle_mass alternate_signs alternate_signs_2
alternating_factorial alternating_sum alternating_sum_2 and and_all
antiprism_area antiprism_volume antitransit_time apery_constant append april
argument arrangements ascension asec asech ash_wednesday asin asinh
astronomical_dawn astronomical_dusk atan atanh atomic_number atomic_symbol
atomic_weight august autumnal_equinox avogadro_number balanced_prime
balanced_prime_ barnesg base bell_polynomial beta binomial bohr_radius
boltzmann_constant build_numbers calendar calkin_wilf catalan_constant ceiling
centered_cube centered_decagonal centered_dodecahedral centered_heptagonal
centered_hexagonal centered_icosahedral centered_nonagonal centered_octagonal
centered_octahedral centered_pentagonal centered_polygonal centered_square
centered_tetrahedral centered_triangular cf champernowne_constant char
christmas collate combine_digits comma comma_mode compositions cone_area
cone_volume conjugate constant convert copeland_erdos_constant cos cosh cot
coth coulomb_constant count count_bits count_divisors cousin_prime
cousin_prime_ crt csc csch cube cube_root dawn day_time debruijn decagonal
decagonal_centered_square decagonal_heptagonal decagonal_hexagonal
decagonal_nonagonal decagonal_octagonal decagonal_pentagonal
decagonal_triangular december decimal_grouping decrement default density_of_hg
density_of_water deuteron_mass dhms diffs diffs2 digamma distance
distance_from_earth divide divisors dms dodecahedral dodecahedron_area
dodecahedron_volume double double_balanced double_balanced_ double_factorial
dst_end dst_start dup_digits dup_operator dup_term dusk e earth_density
earth_gravity earth_mass earth_radius earth_volume easter echo ecm
eddington_number egypt election_day electric_constant electron_charge
electron_mass element element_block element_boiling_point element_density
element_description element_group element_melting_point element_name
element_occurrence element_period element_state energy_equivalence enumerate
enumerate_dice enumerate_dice_ epiphany erdos_persistence escape_velocity
estimate eta euler_brick euler_mascheroni_constant euler_phi eval eval2 eval3
eval_polynomial exp exp10 exponential_range expphi factor factor_sympy
factorial false faraday_constant february fibonacci fibonorial filter
filter_by_index find_palindrome find_polynomial fine_structure_constant flatten
float floor fraction friday frobenius from_bahai from_hebrew from_indian_civil
from_islamic from_julian from_mayan from_persian from_unix_time
gallon_of_ethanol gallon_of_gasoline gamma gcd generalized_pentagonal
generate_polydivisibles geometric_mean geometric_range get_day get_digits
get_hour get_left_truncations get_minute get_month get_right_truncations
get_second get_timezone get_year glaisher_constant good_friday group_elements
harmonic helion_mass help heptagonal heptagonal_hexagonal heptagonal_pentagonal
heptagonal_square heptagonal_triangular heptanacci hex_mode hexagonal
hexagonal_pentagonal hexagonal_square hexanacci hms horizon_distance hyper4_2
hyperfactorial hypotenuse i icosahedral icosahedron_area icosahedron_volume
identify identify_mode imaginary increment infinity input_radix integer
integer_grouping interleave intersection interval_range invert_units
is_abundant is_achilles is_automorphic is_deficient is_divisible is_equal
is_even is_friendly is_generalized_dudeney is_greater is_harshad
is_k_hyperperfect is_k_narcissistic is_k_semiprime is_kaprekar is_less
is_morphic is_narcissistic is_not_equal is_not_greater is_not_less is_not_zero
is_odd is_palindrome is_pandigital is_pddi is_pdi is_perfect is_polydivisible
is_powerful is_prime is_pronic is_rough is_semiprime is_smooth is_sphenic
is_square is_squarefree is_sum_product is_trimorphic is_unusual is_zero
iso_date iso_day isolated_prime itoi january july june jupiter jupiter_mass
jupiter_radius jupiter_revolution jupiter_volume k_fibonacci khinchin_constant
kinetic_energy labor_day lah lambda lambertw larger latlong latlong_to_nac lcm
leading_zero leading_zero_mode left leyland li limit limitn linear_recurrence
location location_info log log10 log2 log_gamma logxy long longlong lucas
magnetic_constant make_cf make_datetime make_iso_time make_julian_time
make_pyth_3 make_pyth_4 march mars mars_mass mars_radius mars_revolution
mars_volume mass_equivalence max max_char max_double max_float max_index
max_long max_longlong max_quadlong max_short max_uchar max_ulong max_ulonglong
max_uquadlong max_ushort may mean memorial_day mercury mercury_mass
mercury_radius mercury_revolution mercury_volume merten merten_constant
mills_constant min min_char min_double min_float min_index min_long
min_longlong min_quadlong min_short min_uchar min_ulong min_ulonglong
min_uquadlong min_ushort mobius modulo molar_mass monday moon moon_antitransit
moon_gravity moon_mass moon_phase moon_radius moon_revolution moon_transit
moon_volume moonrise moonset multifactorial multinomial multiply
multiply_digits multiply_polynomials muon_mass n_persistence n_sphere_area
n_sphere_radius n_sphere_volume name nand nand_all narayana nautical_dawn
nautical_dusk nearest_int negate negative negative_infinity neptune
neptune_mass neptune_radius neptune_revolution neptune_volume neutron_mass
newton_constant next_antitransit next_first_quarter_moon next_full_moon
next_last_quarter_moon next_new_moon next_prime next_primes
next_quadruplet_prime next_quintuplet_prime next_rising next_setting
next_transit night_time nonagonal nonagonal_heptagonal nonagonal_hexagonal
nonagonal_octagonal nonagonal_pentagonal nonagonal_square nonagonal_triangular
nonzero nor nor_all not november now nprod nsum nth_apery nth_bell
nth_bernoulli nth_carol nth_catalan nth_centered_decagonal
nth_centered_heptagonal nth_centered_hexagonal nth_centered_nonagonal
nth_centered_octagonal nth_centered_pentagonal nth_centered_polygonal
nth_centered_square nth_centered_triangular nth_decagonal nth_delannoy
nth_heptagonal nth_hexagonal nth_jacobsthal nth_kynea nth_leonardo nth_menage
nth_mersenne_prime nth_motzkin nth_nonagonal nth_octagonal nth_padovan nth_pell
nth_pentagonal nth_polygonal nth_prime nth_quadruplet_prime
nth_quintuplet_prime nth_schroeder nth_schroeder_hipparchus nth_square
nth_stern nth_sylvester nth_thue_morse nth_triangular nth_weekday
nth_weekday_of_year occurrence_cumulative occurrence_ratios occurrences
octagonal octagonal_heptagonal octagonal_hexagonal octagonal_pentagonal
octagonal_square octagonal_triangular octahedral octahedron_area
octahedron_volume octal_mode octanacci october oeis oeis_comment oeis_ex
oeis_name omega_constant or or_all orbital_mass orbital_period orbital_radius
orbital_velocity ordinal_name output_radix pack parity partitions
pascal_triangle pentagonal pentagonal_square pentagonal_triangular pentanacci
pentatope pentecost permutations permute_dice permute_digits permute_lists
persistence phi pi planck_angular_frequency planck_area planck_charge
planck_constant planck_current planck_density planck_energy
planck_energy_density planck_force planck_impedance planck_intensity
planck_length planck_mass planck_momentum planck_power planck_pressure
planck_temperature planck_time planck_voltage planck_volume plastic_constant
plot plot2 plotc pluto pluto_mass pluto_radius pluto_revolution pluto_volume
polyexp polygamma polygon_area polygonal polylog polynomial_power
polynomial_product polynomial_sum polyprime polytope power powmod precision
presidents_day previous previous_antitransit previous_first_quarter_moon
previous_full_moon previous_last_quarter_moon previous_new_moon previous_rising
previous_setting previous_transit prevost_constant prime prime_pi prime_range
primes primorial prism_area prism_volume product proton_mass pyramid
quadruplet_prime quadruplet_prime_ quintuplet_prime quintuplet_prime_
radiation_constant random random_ random_integer random_integer_ range ratios
ratios2 real reciprocal reduce reduced_planck_constant repunit result
reversal_addition reverse reverse_digits rhombdodec riesel right
robbins_constant roll_dice roll_dice_ root round round_by_digits round_by_value
rydberg_constant safe_prime saturday saturn saturn_mass saturn_radius
saturn_revolution saturn_volume schwarzchild_radius sec sech september set
sextuplet_prime sextuplet_prime_ sexy_prime sexy_prime_ sexy_quadruplet
sexy_quadruplet_ sexy_triplet sexy_triplet_ shift_left shift_right short
show_erdos_persistence show_n_persistence show_persistence shuffle
sidereal_year sigma sigma_n sign silver_ratio sin sinh sized_range sky_location
slice smaller solar_constant solar_noon solve solve_cubic solve_quadratic
solve_quartic sophie_prime sort sort_descending speed_of_light sphere_area
sphere_radius sphere_volume square square_root square_triangular stants: star
stddev stefan_boltzmann_constant stella_octangula subfactorial sublist subtract
sum sum_digits summer_solstice sun sun_antitransit sun_luminosity sun_mass
sun_radius sun_volume sunday sunrise sunset superfactorial superprime
surface_gravity tan tanh tau_mass tetrahedral tetrahedron_area
tetrahedron_volume tetranacci tetrate thabit thanksgiving thue_morse_constant
thursday time_dilation timer timer_mode to_bahai to_bahai_name to_hebrew
to_hebrew_name to_indian_civil to_indian_civil_name to_islamic to_islamic_name
to_iso to_iso_name to_julian to_julian_day to_lilian_day to_mayan
to_ordinal_date to_persian to_persian_name to_unix_time today tomorrow topic
torus_area torus_volume tower tower2 transit_time triangle_area triangular
tribonacci trigamma triple_balanced triple_balanced_ triplet_prime
triplet_prime_ triton_mass tropical_year true truncated_octahedral
truncated_tetrahedral tuesday twin_prime twin_prime_ uchar uinteger ulong
ulonglong undouble unfilter unfilter_by_index unfloat union unique unit_roots
unlist unpack uranus uranus_mass uranus_radius uranus_revolution uranus_volume
ushort uuid uuid_random vacuum_impedance value velocity venus venus_mass
venus_radius venus_revolution venus_volume vernal_equinox von_klitzing_constant
wednesday weekday winter_solstice x xor y ydhms year_calendar yesterday z zero
zeta zeta_zero { }

