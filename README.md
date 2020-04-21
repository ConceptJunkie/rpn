# rpn

rpnChilada is a command-line Reverse-Polish Notation calculator.

rpnChilada supports arithmetic with arbitrary precision, powers and roots, logarithms, algebraic functions (including polynomials arithmetic and solving), trigonometric functions, complex numbers, computer science related functions (bitwise math, base conversion), number theory functions, astronomical functions, prime number calculations and lookup, can operate with single operands or lists of operands and supports a wide variety of flexible unit conversions comparable to the GNU units program.

## Updates

### Update - July 11, 2019

Version 8.2.0 is released.   This version has a few new operators and streamlined unit tests, as well as the usual bug fixes.

---

The current release is 8.2.0.

See "rpn help settings" for more information.

## Installing RPN on Debian-based Linux:

I don't think this is correct yet.

#sudo apt install python3-dev python3-pip libgmp-dev libmpfr-dev libmpc-dev python3-setuptools python3-gmpy2

#pip3 install rpnChilada

## Running RPN using the source:

rpn is written in Python 3, and requires several libraries for the hard math stuff (gmpy2 is optional, but recommended for improved performance).

Please see requirements.txt for a list of required Python packages.

Windows users will want to use Christophe Gohlke's Windows installers for gmpy2 and pyephem at https://www.lfd.uci.edu/~gohlke/pythonlibs/.

Using rpnChilada:

rpnChilada is very easy to use.  It's just like any RPN calculator: Operands go first, then the operators. All examples assume `rpn` is an alias for `python /<path-to-rpn>/rpn.py`.  In interactive mode, you leave off the `rpn`.
I always create an alias for "python rpn.py" called "rpn".  If you are using the package installed with pip, there are commands in the scripts directories called "rpn" and "rpnChilada" to launch rpnChilada.

Unit tests can be run with the testRPN command (when installed from the wheel) or by running testRPN.py from the rpn/ directory.

For instance:

	rpn 2 2 +

will calculate 2 + 2.

rpn supports more than 900 operators. (`rpn _dump_operators` will list them all.)

The entire operator list is also included at the bottom of this document.

rpn has pretty extensive built-in help, although the help files are not complete. However, all operators have at least a brief description, and most are obvious enough to use easily.

Start with `rpn help` for an overview. To dive right in, see `rpn help examples`. In interactive mode, typing `help` will launch help mode. Then, `topics` will print out a list of help topics and `exit` will return to rpn.

The data files are stored in the same location as `rpn.py` in a subdirectory called `rpndata/`.

If you really want to generate prime numbers, see my "primes" project: https://github.com/ConceptJunkie/primes I've calculated the first 15 billion prime numbers and will someday update the rpn lookup tables.

The project https://github.com/ConceptJunkie/rpnChiladaData provides the compiled prime number data files.  If you installed rpnChilada with pip, then this data will be automatically installed.

rpn also provides a simple interface for accessing The On-Line Encyclopedia of Integer Sequences (http://oeis.org), see `rpn help special` and `rpn help oeis`.

rpnChilada used to provide a Windows installer, but I haven't been able to do that since version 6.4.0.  I hope to bring that back some day.

## Feedback, Comments, Bug Reports:

Any feedback is welcome at [rickg@his.com](mailto:rickg@his.com).  This was originally an exercise to learn Python, but slowly blossomed into something really useful and fun, so I wanted to share it. rpn also exposes just a few of the features of the amazing mpmath library (by Fredrik Johansson, http://mpmath.org/) which is where almost all the hard math stuff is actually done.

**Rick Gutleber**
[rickg@his.com](mailto:rickg@his.com)

p.s. rpn is licensed under the GNU GPL version 3.0. See (see (http://www.gnu.org/licenses/gpl.html) for more information).

## Release Notes

8.3.0 (beta)

The astronomy operators now don't care which order the arguments are in, except
for 'angular_separation', which expects the first two arguments to be
astronomical bodies.

The aliquot operators now detect if an amicable number chain has been found and
terminate.

Help has been filled in for all constants and most of the units.

Added 'does_list_repeat', 'sequence' and 'tau' operator.

Added the 'esterling' unit.

'hyperop' now has several hard-coded results for trivial cases.

Fixed bugs in 'triplet_prime' and 'horizon_distance'.

And the usual minor bug fixes.

8.2.0

Added the 'pythagorean_triples' and 'get_partitions_with_limit' operators.

Added the '_dump_prime_cache' operator.

Added 'filter_max' and 'filter_min' which are shortcuts for much wordier lambda
constructions.

Added 'polygonal_pyramidal' and 'polygorial' operators.

The unit test suite has been streamlined so that it runs faster, since it's
used so much.  Added the -t argument to time individual tests.  Added the -f
argument to allow filtering which tests will be run (based on a text filter).

And the usual bug fixes.

8.1.1

As usual, I messed up something with the release and have to fix it.

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

7.2.5

I fat-fingered an addition to the requirements.txt file.  :-/

7.2.4

Just a bunch of fixes.  makeUnits has been improved a bit, and I've validated that all conversions exist, and are consistent.

7.2.3

I messed up the upload for 7.2.2.  No code changes, just fixed packaging.

7.2.2

A big change that doesn't affect functionality is that the prime number data now resides in a separate package called rpnChiladaData.  This data rarely changes so there's no reason to download it.

A major bug was uncovered after almost a year.  rpnChilada thought there were 51920.97 seconds in a day because of a typo.  This has been fixed, and I figured out how to detect other similar problems if they exist.  This change will be implemented in the next few days.

7.2.1

Unit conversion is now a lot smarter because the automatically-generated area and volume units are generated more intelligently.  This means expressions using the "square" and "cubic" units will convert automatically and you won't end up with something like "foot^2/square_mile".

...and yes, a few bug fixes.

7.2.0

Added 'random_element' operator.

The gmpy2 digits( ) function is a much faster way to convert numbers to bases 2 through 62.

Added support for using yafu for factoring.

Added 'aliquot_limit' operator.

Added support for user configuration:  'set_config', 'get_config', 'delete_config' and 'dump_config'.

Added the 'mothers_day', 'fathers_day' and 'advent' operators.

Added the 'molar_gas_constant', 'aliquot_limit' and 'distance' operators (the old 'distance' operator is now called 'geo_distance').

Added unit tests for converting units, and made a few fixes accordingly.

Verbose mode for factoring gets turned on with -D.

Oops, there were two operators named 'distance'.  'distance' now refers to the physics operator and the geography operator is now named 'geo_distance'.

The 'acceleration' operator has been implemented.

The derived Planck units are now calculated, instead of hard-coded.

Block Hole operators:  'black_hole_entropy', 'black_hole_lifetime', 'black_hole_luminosity', 'black_hole_mass', 'black_hole_radius' (was 'schwarzchild_radius'), 'black_hole_surface_area', 'black_hole_surface_gravity', 'black_hole_temperature'

...and the usual bug fixes.

7.0.0

Version 7 represents over 2-1/2 years of work and I neglected to keep track of the changes.

There are probably around 200 more operators since 6.4 was released, and I replaced the factoring code with a much faster verison.

rpn now supports user-defined variables and functions, including persistent variables and functions.

Operators supported by rpn:

( ) aa_battery abs abundance abundance_ratio acceleration accuracy ackermann
acos acosh acot acoth acsc acsch add add_digits add_polynomials advent agm
aliquot aliquot_limit alpha_particle_mass alternate_signs alternate_signs_2
alternating_factorial alternating_harmonic_fraction alternating_sum
alternating_sum_2 and and_all angular_separation angular_size antiharmonic_mean
antiprism_area antiprism_volume antitransit_time apery_constant append april
argument arrangements ascension asec asech ash_wednesday asin asinh
astronomical_dawn astronomical_dusk atan atanh atomic_number atomic_symbol
atomic_weight august autumnal_equinox avogadro_number balanced_prime
balanced_prime_ barnesg base base_units bell_polynomial beta binomial
bitwise_and bitwise_nand bitwise_nor bitwise_not bitwise_or bitwise_xor
black_hole_entropy black_hole_lifetime black_hole_luminosity black_hole_mass
black_hole_radius black_hole_surface_area black_hole_surface_gravity
black_hole_surface_tides black_hole_temperature bohr_radius boltzmann_constant
build_numbers build_step_numbers calendar calkin_wilf catalan_constant ceiling
centered_cube centered_decagonal centered_dodecahedral centered_heptagonal
centered_hexagonal centered_icosahedral centered_nonagonal centered_octagonal
centered_octahedral centered_pentagonal centered_polygonal centered_square
centered_tetrahedral centered_triangular cf champernowne_constant char
christmas classical_electron_radius collate collatz columbus_day combinations
combine_digits comma comma_mode compare_lists compositions cone_area
cone_volume conjugate convert copeland_erdos_constant cos cosh cot coth
coulomb_constant count count_bits count_different_digits count_digits
count_divisors cousin_prime cousin_prime_ crt csc csch cube cube_root
cube_super_root cumulative_diffs cumulative_ratios cyclic_permutations
cyclotomic dawn day_time debruijn decagonal decagonal_centered_square
decagonal_heptagonal decagonal_hexagonal decagonal_nonagonal
decagonal_octagonal decagonal_pentagonal decagonal_triangular december
decimal_grouping decrement default delete_config denomination_combinations
density_of_water describe deuteron_mass dhms difference diffs digamma
digital_root digits dimensions discriminant distance distance_from_earth divide
divisors dms dodecahedral dodecahedron_area dodecahedron_volume double
double_balanced_prime double_balanced_prime_ double_factorial dst_end dst_start
dump_config duplicate_digits duplicate_number duplicate_operator duplicate_term
dusk e earth_density earth_gravity earth_mass earth_radius earth_volume easter
echo eclipse_totality eddington_number egypt election_day electric_constant
electron_charge electron_mass element element_block element_boiling_point
element_density element_description element_group element_melting_point
element_name element_occurrence element_period element_state energy_equivalence
enumerate enumerate_dice enumerate_dice_ epiphany equals_one_of
erdos_persistence escape_velocity estimate eta euler_brick
euler_mascheroni_constant euler_phi eval eval0 eval2 eval3 eval_list eval_list2
eval_list3 eval_polynomial exp exp10 exponential_range expphi factor factorial
false faraday_constant fathers_day february fibonacci fibonorial filter
filter_by_index filter_integers filter_lists filter_max filter_min
filter_on_flags find find_palindrome find_polynomial find_sum_of_cubes
find_sum_of_squares fine_structure_constant flatten float floor for_each
for_each_list fraction friday frobenius from_bahai from_ethiopian from_hebrew
from_indian_civil from_islamic from_julian from_mayan from_persian
from_unix_time function gallon_of_ethanol gallon_of_gasoline gamma gcd gcd2
generalized_pentagonal generate_polydivisibles geometric_mean geometric_range
geometric_recurrence geo_distance get_base_k_digits get_combinations get_config
get_day get_digits get_hour get_left_digits get_left_truncations get_minute
get_month get_nonzero_base_k_digits get_nonzero_digits get_partitions
get_partitions_with_limit get_permutations get_repeat_combinations
get_repeat_permutations get_right_digits get_right_truncations get_second
get_timezone get_variable get_year glaisher_constant good_friday group_elements
harmonic_fraction harmonic_mean harmonic_residue has_any_digits has_digits
has_only_digits heat_index helion_mass help heptagonal heptagonal_hexagonal
heptagonal_pentagonal heptagonal_square heptagonal_triangular heptanacci
hexagonal hexagonal_pentagonal hexagonal_square hexanacci hex_mode hms
horizon_distance hurwitz_zeta hyperfactorial
hyperfine_transition_frequency_of_cesium hyperoperator hyperoperator_right
hypotenuse i icosahedral icosahedron_area icosahedron_volume identify
identify_mode if imaginary increment independence_day infinity input_radix
integer integer_grouping interleave intersection interval_range invert_units
isolated_prime iso_date iso_day is_abundant is_achilles is_antiharmonic
is_automorphic is_base_k_pandigital is_base_k_smith_number is_bouncy
is_carmichael is_composite is_decreasing is_deficient is_digital_permutation
is_divisible is_equal is_even is_friendly is_generalized_dudeney is_greater
is_harmonic_divisor_number is_harshad is_increasing is_integer is_kaprekar
is_kth_power is_k_hyperperfect is_k_morphic is_k_narcissistic is_k_perfect
is_k_semiprime is_k_sphenic is_less is_narcissistic is_not_equal is_not_greater
is_not_less is_not_zero is_odd is_order_k_smith_number is_palindrome
is_palindrome_list is_pandigital is_pddi is_pdi is_perfect is_pernicious
is_polydivisible is_powerful is_power_of_k is_prime is_pronic is_rough
is_ruth_aaron is_semiprime is_smith_number is_smooth is_sphenic is_square
is_squarefree is_step_number is_strong_pseudoprime is_sum_product is_trimorphic
is_unusual is_zero itoi january july june jupiter jupiter_mass jupiter_radius
jupiter_revolution jupiter_volume khinchin_constant kinetic_energy k_fibonacci
k_persistence k_sphere_area k_sphere_radius k_sphere_volume labor_day lah
lambda lambertw larger latlong_to_nac lat_long lcm lcm2 leading_zero
leading_zero_mode left leyland li limit limitn linear_recurrence
linear_recurrence_with_modulo list_from_file location location_info log log10
log2 logxy log_gamma long longlong lucas magnetic_constant
magnetic_flux_quantum make_cf make_datetime make_iso_time make_julian_time
make_pyth_3 make_pyth_4 mantissa march mars mars_mass mars_radius
mars_revolution mars_volume martin_luther_king_day mass_equivalence maximum
max_char max_double max_float max_index max_long max_longlong max_quadlong
max_short max_uchar max_ulong max_ulonglong max_uquadlong max_ushort may mean
memorial_day mercury mercury_mass mercury_radius mercury_revolution
mercury_volume merten merten_constant mills_constant minimum min_char
min_double min_float min_index min_long min_longlong min_quadlong min_short
min_uchar min_ulong min_ulonglong min_uquadlong min_ushort mobius modulo
molar_gas_constant molar_mass monday moon moonrise moonset moon_antitransit
moon_gravity moon_mass moon_phase moon_radius moon_revolution moon_transit
moon_volume mothers_day multifactorial multinomial multiply multiply_digits
multiply_digit_powers multiply_nonzero_digits multiply_nonzero_digit_powers
multiply_polynomials muon_mass name nand nand_all narayana nautical_dawn
nautical_dusk nearest_int negative negative_infinity neptune neptune_mass
neptune_radius neptune_revolution neptune_volume neutron_mass newton_constant
new_years_day next_antitransit next_first_quarter_moon next_full_moon
next_last_quarter_moon next_new_moon next_prime next_primes
next_quadruplet_prime next_quintuplet_prime next_rising next_setting
next_transit night_time nonagonal nonagonal_heptagonal nonagonal_hexagonal
nonagonal_octagonal nonagonal_pentagonal nonagonal_square nonagonal_triangular
nonzero nor nor_all not november now nprod nsum nth_apery nth_bell
nth_bernoulli nth_carol nth_catalan nth_centered_decagonal
nth_centered_heptagonal nth_centered_hexagonal nth_centered_nonagonal
nth_centered_octagonal nth_centered_pentagonal nth_centered_polygonal
nth_centered_square nth_centered_triangular nth_decagonal nth_delannoy
nth_harmonic_number nth_heptagonal nth_hexagonal nth_jacobsthal nth_kynea
nth_leonardo nth_linear_recurrence nth_linear_recurrence_with_modulo nth_menage
nth_mersenne_exponent nth_mersenne_prime nth_motzkin nth_nonagonal
nth_octagonal nth_padovan nth_pell nth_pentagonal nth_perfect_number
nth_polygonal nth_prime nth_quadruplet_prime nth_quintuplet_prime nth_schroeder
nth_schroeder_hipparchus nth_square nth_stern nth_sylvester nth_thue_morse
nth_triangular nth_weekday nth_weekday_of_year nuclear_magneton occurrences
occurrence_cumulative occurrence_ratios octagonal octagonal_heptagonal
octagonal_hexagonal octagonal_pentagonal octagonal_square octagonal_triangular
octahedral octahedron_area octahedron_volume octal_mode octanacci october
octy_prime octy_prime_ oeis oeis_comment oeis_ex oeis_name oeis_offset
omega_constant or orbital_mass orbital_period orbital_radius orbital_velocity
ordinal_name or_all output_radix pack parity partitions pascal_triangle
pentagonal pentagonal_square pentagonal_triangular pentanacci pentatope
pentecost permutations permute_dice permute_digits permute_lists persistence
phi phitorial pi planck_acceleration planck_angular_frequency planck_area
planck_charge planck_constant planck_current planck_density
planck_electrical_inductance planck_energy planck_energy_density planck_force
planck_impedance planck_intensity planck_length planck_magnetic_inductance
planck_mass planck_momentum planck_power planck_pressure planck_temperature
planck_time planck_viscosity planck_voltage planck_volume
planck_volumetric_flow_rate plastic_constant plot plot2 plotc pluto pluto_mass
pluto_radius pluto_revolution pluto_volume polyexp polygamma polygonal
polygonal_pyramidal polygon_area polygorial polylog polynomial_power
polynomial_product polynomial_sum polyprime polytope power powerset power_tower
power_tower2 powmod precision presidents_day previous previous_antitransit
previous_first_quarter_moon previous_full_moon previous_last_quarter_moon
previous_new_moon previous_prime previous_primes previous_rising
previous_setting previous_transit prevost_constant prime primes prime_pi
prime_range primitive_units primorial prism_area prism_volume product
proton_mass pyramidal pythagorean_triples quadlong quadruplet_prime
quadruplet_prime_ quadruple_balanced_prime quadruple_balanced_prime_
quintuplet_prime quintuplet_prime_ radiation_constant radical random random_
random_element random_integer random_integer_ range ratios real reciprocal
recurrence reduce reduced_planck_constant relatively_prime repeat
replace_digits repunit result reversal_addition reverse reverse_digits
rhombic_dodecahedral riesel right robbins_constant roll_dice roll_dice_
roll_simple_dice root root_mean_square rotate_digits_left rotate_digits_right
round round_by_digits round_by_value rydberg_constant safe_prime saturday
saturn saturn_mass saturn_radius saturn_revolution saturn_volume sec sech
september set_config set_variable sextuplet_prime sextuplet_prime_ sexy_prime
sexy_prime_ sexy_quadruplet sexy_quadruplet_ sexy_triplet sexy_triplet_
shift_left shift_right short show_erdos_persistence show_k_persistence
show_persistence shuffle sidereal_year sigma sigma_k sign silver_ratio sin sinh
sized_range sky_location slice smaller solar_constant solar_noon solve
solve_cubic solve_quadratic solve_quartic sophie_prime sort sort_descending
speed_of_light sphere_area sphere_radius sphere_volume square
square_digit_chain square_root square_super_root square_triangular stant
operators: star stddev stefan_boltzmann_constant stella_octangula stirling1
stirling2 subfactorial sublist subtract sum summer_solstice
sums_of_k_nonzero_powers sums_of_k_powers sum_digits sun sunday sunrise sunset
sun_antitransit sun_luminosity sun_mass sun_radius sun_volume superfactorial
super_prime super_root surface_gravity tan tanh tau_mass tetrahedral
tetrahedron_area tetrahedron_volume tetranacci tetrate tetrate_right thabit
thanksgiving thue_morse_constant thursday tidal_force timer timer_mode
time_dilation today tomorrow topic torus_area torus_volume to_bahai
to_bahai_name to_ethiopian to_ethiopian_name to_hebrew to_hebrew_name
to_indian_civil to_indian_civil_name to_islamic to_islamic_name to_iso
to_iso_name to_julian to_julian_day to_lilian_day to_mayan to_ordinal_date
to_persian to_persian_name to_unix_time transit_time triangle_area triangular
tribonacci trigamma triplet_prime triplet_prime_ triple_balanced_prime
triple_balanced_prime_ triple_point_of_water triton_mass tropical_year true
truncated_octahedral truncated_tetrahedral tuesday twin_prime twin_prime_ uchar
uinteger ulong ulonglong undouble unfilter unfilter_by_index unfloat union
unique unit_roots unlist unpack uquadlong uranus uranus_mass uranus_radius
uranus_revolution uranus_volume ushort uuid uuid_random vacuum_impedance value
velocity venus venus_mass venus_radius venus_revolution venus_volume
vernal_equinox veterans_day von_klitzing_constant wednesday weekday
weekday_name wind_chill winter_solstice x xnor xor y ydhms year_calendar
yesterday z zero zeta zeta_zero [ ] _dump_aliases _dump_cache _dump_constants
_dump_conversions _dump_operators _dump_prime_cache _dump_stats _dump_units

