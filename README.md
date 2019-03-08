# rpn

rpn is a command-line Reverse-Polish Notation calculator.

rpn supports arithmetic with arbitrary precision, powers and roots, logarithms, algebraic functions (including polynomials arithmetic and solving), trigonometric functions, complex numbers, computer science related functions (bitwise math, base conversion), number theory functions, astronomical functions, prime number calculations and lookup, can operate with single operands or lists of operands and supports a wide variety of flexible unit conversions comparable to the GNU units program.

## Updates

### Update - March 7, 2019

This is embarrassing.  I just discovered a long-standing bug with the unit conversion code where for some reason it thinks there are 59021.97 seconds in a day.  I've narrowed the bug down to between the 7.0.0 and 7.1.0 releases.  This is weird because
every other unit conversion I checked, including other conversions with days and seconds work correctly.  The makeUnits code has been in place for about 3 or 4 years and always seemed to be rock-solid.  I'll try to push a 7.2.2 in the next few days, or
possibly even 7.3.0 depending on what else gets included.

### Update - February 26, 2019

OK, stick a fork in 7.2.0.  It's done.  I'd intended to get back to releasing often, but 10 months is not "often".

Aside from the usual ton of bug fixes and minor improvements, this version offers several operators having to do with the physics of black holes.  See "rpn help physics" for details.

The 7.2.0 release will show up on PyPI in the next day or two as soon as I have some time to test the wheel.

### Update - February 22, 2019

Not much has happened with rpn lately, but I do have some good plans.  I haven't released 7.2 mostly due to laziness, but I've also got some solid ideas for improvements with the unit conversion functionality.  For one thing, I want to fold the constants into the units database, and I have an idea for adding some implicit unit conversion.

I've also wanted to migrate from pyephem, which is no longer being developed, to Skyfield, which is recommended by the people who used to make pyephem.  Skyfield is also a pure Python library, which makes my life easier.  However, Skyfield is a more low-level library, so there's not a one-to-one correspondence for most of the pyephem functionality I've been using.

### Update - February 21, 2018

rpn is available on pypi.org.  Since there always was a project called "rpn", I had to come up with a new name, so I'm happy to introduce "rpnChilada".

Windows users will want to use Christophe Gohlke's Windows installers for gmpy2 and pyephem at https://www.lfd.uci.edu/~gohlke/pythonlibs/.

### Update - August 15, 2016

I am very excited that people have started noticing rpn!

Please continue with comments, suggestions and bug reports. rpn has lots of little bugs and possibly some big ones, too, and although I have unit tests, most of the time, I find bugs from using it.

I especially want to thank the folks at The Nineteenth Byte on Stack Exchange for their nice comments. I also love solving puzzles with rpn, so if there's something you'd like to see it be able to do, drop me a line at rickg@his.com.

I'll try to focus on improving the help in the near future.

### Update - July 19, 2016

I don't know if anyone has ever looked at this project... not even my Mom. But anyhow, I wanted to leave an update anyway. The "imminent" release of version 7 is anything but. I have been too lazy to tackle trying to make the wheel work correctly. I've been making small additions here and there, including bug fixes whenever I find problems.

Currently, my short list is topped with switching to SQLite for caching function results to disk. I was experimenting with the sigma function and found that once the cache of values got past a million, loading it had become unreasonably slow. I think it would also be a very good idea to convert the prime number data files to SQLite tables as well.

There are a few Python 2 compatibility problems that remain, and those should be easy to fix, but I've been too busy with a combiniation of real life and general laziness. The conversion to using generators mentioned in the last update is complete and has greatly improved performance for a lot of operators.

RPN continues to proceed slowly and it works just fine right now, so it can be used just fine despite being a "pre-release".

### Update - November 16, 2015

The scope of changes for version 7 keeps growing. The transition to lazy list evaluation (using generators) is going to be a very big change and currently a lot of operators are broken.

It is recommended that anyone using RPN from Git stick with the 7.0.alpha1 tag for the time being.

### Update - October 15, 2015

I've decided the upcoming release will be version 7 since so much has been added, a lot has been reorganized and I've gotten serious about unit tests.

An official release of version 7 probably won't be for a while, because I really want to be able to release it on PyPI. There's a lot of work I want to do before cutting another release, and it's going to take some time, but the current git master contains all the latest features and is working fine.

rpn should still work on Android, but there are problems with the ephem library. I think it has to do with building the AstroLib code, and haven't had a chance to try to diagnose the problem.

### Update - August 5, 2015

I am working on creating a wheel for rpn, and I'm hoping I can also make it Python 2 compatible before cutting another release. The biggest roadblock is just getting some round tuits instead of adding in new operators, which is much more fun.

Another cool update: rpn can now be run on Android with the Termux app
(http://termux.com/)! Right now, it fails a unit test having to do with date formatting, which I haven't gotten around to investigating, but otherwise it works great. Where else can you factor a 50-digit number on your Android device?

---

The current release is 7.2.2.

See "rpn help settings" for more information.

## Running RPN using the source:

rpn is written in Python 3, and requires several libraries for the hard math stuff (gmpy2 is optional, but recommended for improved performance).

You will need to install the following prerequisites:

```
arrow>=0.12.1
convertdate>=2.1.2
enum34>=1.1.6
ephem>=3.7.6.0
geopy>=1.11.0
gmpy2>=2.0.8
mpmath>=1.1.0
numpy>=1.14.0
pylru>=1.0.9
pyreadline>=2.1
pytz>=2017.3
six>=1.11.0
skyfield>=1.10
timezonefinder>=2.1.2
tzlocal>=1.5.1
```

Windows users will want to use Christophe Gohlke's Windows installers for gmpy2 and pyephem at https://www.lfd.uci.edu/~gohlke/pythonlibs/.

Using rpnChilada:

rpnChilada is very easy to use.  It's just like any RPN calculator: Operands go first, then the operators. All examples assume `rpn` is an alias for `python /<path-to-rpn>/rpn.py`.  In interactive mode, you leave off the `rpn`.
I always create an alias for "python rpn.py" called "rpn".  If you are using the package installed with pip, there are commands in the scripts directories called "rpn" and "rpnChilada" to launch rpnChilada.

For instance:

	rpn 2 2 +

will calculate 2 + 2.

rpn supports more than 700 operators. (`rpn _dumpops` will list them all.)

The entire operator list is also included at the bottom of this document.

rpn has pretty extensive built-in help, although the help files are not complete. However, all operators have at least a brief description, and most are obvious enough to use easily.

Start with `rpn help` for an overview. To dive right in, see `rpn help examples`. In interactive mode, typing `help` will launch help mode. Then, `topics` will print out a list of help topics and `exit` will return to rpn.

`makeRPNPrimes.py` consists of a bunch of functions for pre-calculating and caching different kinds of prime numbers that was recently pulled out of `rpn.py` (and as of version 6.4.0 isn't finished as a standalone program).

The data files are stored in the same location as `rpn.py` in a subdirectory called `rpndata/`. In the Windows installer version, they are stored in the same directory as the `EXE`.

If you really want to generate prime numbers, see my "primes" project: https://github.com/ConceptJunkie/primes I've calculated the first 10 billion prime numbers and will someday update the rpn lookup tables.

rpn also provides a simple interface for accessing The On-Line Encyclopedia of Integer Sequences (http://oeis.org), see `rpn help special` and `rpn help oeis`.

## Feedback, Comments, Bug Reports:

Any feedback is welcome at [rickg@his.com](mailto:rickg@his.com). This was originally an exercise to learn Python, but slowly blossomed into something really useful and fun, so I wanted to share it. rpn also exposes just a few of the features of the amazing mpmath library (by Fredrik Johansson, http://mpmath.org/) which is where almost all the hard math stuff is actually done.

**Rick Gutleber**
[rickg@his.com](mailto:rickg@his.com)

p.s. rpn is licensed under the GNU GPL version 3.0. See (see
(http://www.gnu.org/licenses/gpl.html) for more information).

## Release Notes

7.2.2

A big change that doesn't affect functionality is that the prime number data
now resides in a separate package called rpnChiladaData.  This data rarely
changes so there's no reason to download it.

A major bug was uncovered after almost a year.  rpnChilada thought there were
51920.97 seconds in a day because of a typo.  This has been fixed, and I
figured out how to detect other similar problems if they exist.  This change
will be implemented in the next few days.

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

7.0.0

Version 7 represents over 2-1/2 years of work and I neglected to keep track of the changes.

There are probably around 200 more operators since 6.4 was released, and I replaced the factoring code with a much faster verison.

rpn now supports user-defined variables and functions, including persistent variables and functions.

6.4.0 - "Factoring Fun"

Revamped factorization to be much, much faster, using the Brent-Pollard
algorithm instead of just brute-force dividing.   More to come...

Added the 'magnetic_constant', 'electric_constant', 'rydberg_constant',
'newtons_constant' and 'fine_structure' operators.

Added 'eulerphi' operator.

Added caching for factorizations.  I often factor the same numbers over and over (like when I'm playing with the Fibonaccis) so it made sense to cache the results for non-trivial factoring.

Added the 'sigma, 'aliquot', 'polypower', 'mobius' and 'mertens' operators.  The old 'mertens' operator was renamed to 'mertens_constant'.  The 'aliquot' operator is another use-case for caching factorizations... try it with 276.
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

The 'pascal' operator was renamed to 'pascaltri' to avoid a collision with the 'pascal' unit.

Fixed several minor bugs.

6.2.0

Experimental support for mpath plotting functionality using the new
operators, 'plot', 'plot2', 'plotc'.  These operators are not supported
in the Windows installer.

'quit' is now an alias for 'exit' in interactive mode and help mode.

Improvements in function definition.  'y' and 'z' are now operators, allowing for defining functions on 2 or 3 variables.

Operators 'eval2' and 'eval3' allow for evaluation of 2 and 3 variable
operators.

rpn now throws an error if a user-defined function is invalidly specified, instead of going into an infinite loop.

'filter' allows filtering a list based on a user-defined function.

If the units in a measurement cancel out, then the measurement is converted back to a numerical value.

Added 'rand_' and 'randint_' operators.

Added the 'debruijn' operator.

Fixed several minor bugs.

6.1.0

New operators:  'maxdouble', 'maxfloat', 'mindouble', 'minfloat'

Base conversion for output is no longer limited to 1000 digits.  There's no reason to do that.

'rpn 0 cf' now throws an error rather than dividing by 0.

6.0.1

Added code to prevent scientific notation from messing up base conversions for the integral part of the number (up to 1000 digits).

6.0.0

Introduced interactive mode, including variable declaration and referencing previous results by number.  (see 'rpn help interactive_mode')

Added caching for OEIS operators.  However, it turns out some OEIS text is non-ASCII, so I'll have to deal with that.

Operator help now includes examples by default.

The 'time' operator type conflicted with the 'time' unit type, so I changed the operator type to 'date'... because they were all about dates!

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

abs abundance abundance_ratio acceleration accuracy acos acosh acot acoth acsc
acsch add add_digits advent agm aliquot aliquot_limit alternating_factorial
and angular_separation angular_size antiprism_area antiprism_volume
antitransit_time argument arrangements ascension asec asech ash_wednesday
asin asinh astronomical_dawn astronomical_dusk atan atanh atomic_number
atomic_symbol atomic_weight autumnal_equinox balanced_prime balanced_prime_
barnesg bell_polynomial beta binomial bitwise_and bitwise_nand bitwise_nor
bitwise_not bitwise_or bitwise_xor black_hole_entropy black_hole_lifetime
black_hole_luminosity black_hole_mass black_hole_radius
black_hole_surface_area black_hole_surface_gravity black_hole_temperature
build_numbers build_step_numbers calendar calkin_wilf ceiling centered_cube
centered_decagonal centered_dodecahedral centered_heptagonal centered_hexagonal
centered_icosahedral centered_nonagonal centered_octagonal centered_octahedral
centered_pentagonal centered_polygonal centered_square centered_tetrahedral
centered_triangular char christmas collatz columbus_day combinations comma
comma_mode compositions cone_area cone_volume conjugate constant cos cosh cot
coth count_bits count_different_digits count_digits count_divisors
cousin_prime cousin_prime_ csc csch cube cube_root cyclic_permutations
cyclotomic dawn day_time debruijn decagonal decagonal_centered_square
decagonal_heptagonal decagonal_hexagonal decagonal_nonagonal
decagonal_octagonal decagonal_pentagonal decagonal_triangular decimal_grouping
decrement delete_config describe dhms digamma digital_root digits distance
distance_from_earth divide divisors dms dodecahedral dodecahedron_area
dodecahedron_volume double double_balanced double_balanced_ double_factorial
dst_end dst_start dump_config duplicate_digits duplicate_number dusk easter
eclipse_totality egypt election_day element_block element_boiling_point
element_density element_description element_group element_melting_point
element_name element_occurrence element_period element_state energy_equivalence
enumerate_dice enumerate_dice_ epiphany erdos_persistence escape_velocity
estimate eta euler_brick euler_phi eval eval0 eval2 eval3 eval_list eval_list2
eval_list3 exp exp10 exponential_range expphi factor factorial fathers_day
fibonacci fibonorial find_palindrome find_polynomial find_sum_of_cubes
find_sum_of_squares float floor fraction from_bahai from_hebrew
from_indian_civil from_islamic from_julian from_mayan from_persian
from_unix_time function gamma gcd2 generalized_pentagonal
generate_polydivisibles geo_distance geometric_range get_base_k_digits
get_config get_day get_digits get_hour get_left_digits get_left_truncations
get_minute get_month get_nonzero_base_k_digits get_nonzero_digits
get_right_digits get_right_truncations get_second get_timezone get_variable
get_year good_friday harmonic has_any_digits has_digits has_only_digits help
heptagonal heptagonal_hexagonal heptagonal_pentagonal heptagonal_square
heptagonal_triangular heptanacci hex_mode hexagonal hexagonal_pentagonal
hexagonal_square hexanacci hms horizon_distance hurwitz_zeta hyper4_2
hyperfactorial hypotenuse i icosahedral icosahedron_area icosahedron_volume
identify identify_mode if imaginary increment independence_day input_radix
integer integer_grouping interval_range invert_units is_abundant is_achilles
is_automorphic is_base_k_pandigital is_base_k_smith_number is_bouncy
is_carmichael is_composite is_decreasing is_deficient is_digital_permutation
is_divisible is_equal is_even is_generalized_dudeney is_greater is_harshad
is_increasing is_integer is_k_hyperperfect is_k_morphic is_k_narcissistic
is_k_semiprime is_k_sphenic is_kaprekar is_kth_power is_less is_narcissistic
is_not_equal is_not_greater is_not_less is_not_zero is_odd
is_order_k_smith_number is_palindrome is_pandigital is_pddi is_pdi is_perfect
is_polydivisible is_power_of_k is_powerful is_prime is_pronic is_rough
is_ruth_aaron is_semiprime is_smith_number is_smooth is_sphenic is_square
is_squarefree is_step_number is_strong_pseudoprime is_sum_product is_trimorphic
is_unusual is_zero iso_date iso_day isolated_prime jupiter k_fibonacci
k_persistence k_sphere_area k_sphere_radius k_sphere_volume kinetic_energy
labor_day lah lambertw larger lat_long lcm2 leading_zero leading_zero_mode
leyland li limit limitn list_from_file location location_info log log10 log2
log_gamma logxy long longlong lucas make_cf make_pyth_3 make_pyth_4 mantissa
mars martin_luther_king_day mass_equivalence memorial_day mercury merten mobius
modulo molar_mass moon moon_antitransit moon_phase moon_transit moonrise
moonset mothers_day multifactorial multiply multiply_digit_powers
multiply_digits multiply_nonzero_digit_powers multiply_nonzero_digits name nand
narayana nautical_dawn nautical_dusk nearest_int negative neptune new_years_day
next_antitransit next_first_quarter_moon next_full_moon next_last_quarter_moon
next_new_moon next_prime next_primes next_quadruplet_prime
next_quintuplet_prime next_rising next_setting next_transit night_time
nonagonal nonagonal_heptagonal nonagonal_hexagonal nonagonal_octagonal
nonagonal_pentagonal nonagonal_square nonagonal_triangular nor not now nprod
nsum nth_apery nth_bell nth_bernoulli nth_carol nth_catalan
nth_centered_decagonal nth_centered_heptagonal nth_centered_hexagonal
nth_centered_nonagonal nth_centered_octagonal nth_centered_pentagonal
nth_centered_polygonal nth_centered_square nth_centered_triangular
nth_decagonal nth_delannoy nth_heptagonal nth_hexagonal nth_jacobsthal
nth_kynea nth_leonardo nth_menage nth_mersenne_exponent nth_mersenne_prime
nth_motzkin nth_nonagonal nth_octagonal nth_padovan nth_pell nth_pentagonal
nth_perfect_number nth_polygonal nth_prime nth_quadruplet_prime
nth_quintuplet_prime nth_schroeder nth_schroeder_hipparchus nth_square
nth_stern nth_sylvester nth_thue_morse nth_triangular nth_weekday
nth_weekday_of_year octagonal octagonal_heptagonal octagonal_hexagonal
octagonal_pentagonal octagonal_square octagonal_triangular octahedral
octahedron_area octahedron_volume octal_mode octanacci oeis oeis_comment
oeis_ex oeis_name oeis_offset or orbital_mass orbital_period orbital_radius
orbital_velocity ordinal_name output_radix parity partitions pascal_triangle
pentagonal pentagonal_square pentagonal_triangular pentanacci pentatope
pentecost permutations permute_dice permute_digits persistence plot plot2 plotc
pluto polyexp polygamma polygon_area polygonal polylog polyprime polytope power
powmod precision presidents_day previous_antitransit
previous_first_quarter_moon previous_full_moon previous_last_quarter_moon
previous_new_moon previous_prime previous_primes previous_rising
previous_setting previous_transit prime prime_pi prime_range primes primorial
prism_area prism_volume pyramid quadruplet_prime quadruplet_prime_
quintuplet_prime quintuplet_prime_ radical random random_ random_integer
random_integer_ range real reciprocal recurrence repeat replace_digits repunit
result reversal_addition reverse_digits rhombic_dodecahedral riesel roll_dice
roll_dice_ roll_simple_dice root rotate_digits_left rotate_digits_right round
round_by_digits round_by_value safe_prime saturn sec sech set_config
set_variable sextuplet_prime sextuplet_prime_ sexy_prime sexy_prime_
sexy_quadruplet sexy_quadruplet_ sexy_triplet sexy_triplet_ shift_left
shift_right short show_erdos_persistence show_k_persistence show_persistence
sigma sigma_k sign sin sinh sized_range sky_location smaller solar_noon
solve_cubic solve_quadratic solve_quartic sophie_prime sphere_area
sphere_radius sphere_volume square square_digit_chain square_root
square_triangular star stella_octangula subfactorial subtract sum_digits
summer_solstice sums_of_k_nonzero_powers sums_of_k_powers sun sun_antitransit
sunrise sunset superfactorial superprime surface_gravity tan tanh tetrahedral
tetrahedron_area tetrahedron_volume tetranacci tetrate thabit thanksgiving
time_dilation timer timer_mode to_bahai to_bahai_name to_hebrew to_hebrew_name
to_indian_civil to_indian_civil_name to_islamic to_islamic_name to_iso
to_iso_name to_julian to_julian_day to_lilian_day to_mayan to_ordinal_date
to_persian to_persian_name to_unix_time today tomorrow topic torus_area
torus_volume transit_time triangle_area triangular tribonacci trigamma
triple_balanced triple_balanced_ triplet_prime triplet_prime_
truncated_octahedral truncated_tetrahedral twin_prime twin_prime_ uchar
uinteger ulong ulonglong undouble unfloat unit_roots uranus ushort uuid
uuid_random value velocity venus vernal_equinox veterans_day weekday
weekday_name winter_solstice xnor xor ydhms year_calendar yesterday zeta
zeta_zero add_polynomials alternate_signs alternate_signs_2 alternating_sum
alternating_sum_2 and_all append base break_on cf collate combine_digits
compare_lists convert count crt cumulative_diffs cumulative_ratios
denomination_combinations difference diffs discriminant echo element enumerate
equals_one_of eval_polynomial filter filter_by_index filter_list find flatten
for_each for_each_list frobenius gcd geometric_mean geometric_recurrence
get_combinations get_permutations get_repeat_combinations
get_repeat_permutations group_elements harmonic_mean interleave intersection
is_friendly is_palindrome_list latlong_to_nac lcm left linear_recurrence
linear_recurrence_with_modulo make_datetime make_iso_time make_julian_time max
max_index mean min min_index multinomial multiply_polynomials nand_all nonzero
nor_all occurrence_cumulative occurrence_ratios occurrences or_all pack
permute_lists polynomial_power polynomial_product polynomial_sum power_tower
power_tower2 powerset product random_element ratios reduce reverse right
shuffle slice solve sort sort_descending stddev sublist sum unfilter
unfilter_by_index union unique unpack zero ( ) [ ] duplicate_operator
duplicate_term lambda previous unlist x y z _dump_aliases _dump_constants
_dump_operators _dump_units _stats
