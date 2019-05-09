#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnConstantOperators.py
# //
# //  RPN command-line calculator constant operator declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import exp, fadd, fdiv, fmul, fprod, log, mpf, mpmathify, power

from rpn.rpnConstantUtils import *
from rpn.rpnOperator import RPNOperator
from rpn.rpnUnitClasses import RPNConstantInfo


# //******************************************************************************
# //
# //  constantOperators
# //
# //  unit name : value, unit, aliases, multipliable, description
# //
# //  When unit types are multiplied in compound units, they need to be
# //  specified in alphabetical order in the name, but not the representations.
# //
# //******************************************************************************

constantOperators = {
    # physical constants
    'avogadro_number' :
        RPNConstantInfo( '6.022140756e23', '', [ 'avogadro', 'avogadros_number', 'N_sub_A' ], False,
                         'Avogadro\'s number, the number of atoms in a mole',
                         '''
Ref:  https://www.bipm.org/utils/en/pdf/si-revised-brochure/Draft-SI-Brochure-2018.pdf
''' ),

    'boltzmann_constant' :
        RPNConstantInfo( '1.380649e-23', 'kilogram*meter^2/second^2*kelvin',
                         [ 'boltzmann', 'boltzmanns_const', 'k_sub_b', 'k_b' ], False,
                         'The Boltzmann constant relates the average kinetic energy of particles in a gas to the temperature of the gas',
                         '''
Ref:  https://en.wikipedia.org/wiki/Boltzmann_constant
      https://www.bipm.org/utils/en/pdf/si-revised-brochure/Draft-SI-Brochure-2018.pdf

This value is now exact, by definition.
''' ),

    'bohr_radius' :
        RPNConstantInfo( '5.2917721067e-11', 'meter', [ ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0
''' ),

    'classical_electron_radius' :
        RPNConstantInfo( '2.8179403227e-15', 'meter', [ 'electron_radius' ], False,
                         '',
                         '''
Ref:  https://en.wikipedia.org/wiki/Classical_electron_radius
''' ),

    'coulomb_constant' :
        RPNConstantInfo( '8.9875517873681764e9', 'kilogram*meter^3/ampere^2*second^4', [ ], False,
                         '',
                         '''
Ref:  https://en.wikipedia.org/wiki/Coulomb%27s_constant
''' ),

    'electric_constant' :
        RPNConstantInfo( '8.854187817e-12', 'ampere^2*second^4/kilogram*meter^3',
                         [ 'e0', 'e_0', 'e_nought', 'e_sub_0', 'free_space_permittivity', 'vacuum_permittivity' ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?ep0
''' ),

    'electron_charge' :
        RPNConstantInfo( '1.602176634e-19', 'coulomb', [ 'elementary_charge', 'electron' ], False,
                         '',
                         '''
Ref:  https://en.wikipedia.org/wiki/2019_redefinition_of_SI_base_units#Ampere

This new value is exact, by definition.
''' ),

    'hyperfine_transition_frequency_of_cesium' :
        RPNConstantInfo( '9192631770', 'Hz', [ 'delta_nu_sub_cs' ], False,
                         '',
                         '''
Since 1967, the second has been defined as exactly "the duration of
9,192,631,770 periods of the radiation corresponding to the transition between
the two hyperfine levels of the ground state of the caesium-133 atom" (at a
temperature of 0 K).  This length of a second was selected to correspond
exactly to the length of the ephemeris second previously defined.  Atomic
clocks use such a frequency to measure seconds by counting cycles per second
at that frequency.  Radiation of this kind is one of the most stable and
reproducible phenomena of nature. The current generation of atomic clocks are
accurate to within one second in a few hundred million years.

Ref:  https://en.wikipedia.org/wiki/Second#%22Atomic%22_second
Ref:  https://www.bipm.org/utils/en/pdf/si-revised-brochure/Draft-SI-Brochure-2018.pdf
''' ),


# TODO
# https://en.wikipedia.org/wiki/2019_redefinition_of_SI_base_units
# The luminous efficacy Kcd of monochromatic radiation of frequency 540×1012 Hz is exactly 683 lumens per watt (lm·W-1).
# Kcd = 683 cd·sr·s3·kg-1·m-2

    'magnetic_constant' :
        RPNConstantInfo( fprod( [ 4, pi, mpmathify( '1.00000000082e-7' ) ] ), 'newton/ampere^2',
                         [ 'free_space_permeability', 'mu0', 'mu_0', 'mu_sub_0', 'mu_nought' ], False,
                         '',
                         '''
The physical constant, ('mu_0'), commonly called the vacuum permeability,
permeability of free space, permeability of vacuum, or magnetic constant, is
the magnetic permeability in a classical vacuum.  Vacuum permeability is
derived from production of a magnetic field by an electric current or by a
moving electric charge and in all other formulas for magnetic-field production
in a vacuum.

As of May 20, 2019, the vacuum permeability mu_0 is no longer a defined
constant (per the former definition of the SI ampere), but rather needs to be
determined experimentally; 4pi x 1.000 000 000 82 (20) 10e-7 H/m (or N/A^2) is a
recently measured value in the revised SI.  It is proportional to the
dimensionless fine-structure constant with no other dependencies.

Ref:  https://en.wikipedia.org/wiki/Vacuum_permeability
''' ),

    'magnetic_flux_quantum' :
        RPNConstantInfo( '2.067833831e-15', 'weber',
                          [ 'magnetic_flux_quanta', 'josephson_constant', 'K_sub_j' ], False,
                         '',
                         '''
The (superconducting) magnetic flux quantum F0 = h/2e =~
2.067833831(13)x10e-15 Wb is a combination of fundamental physical constants:
the Planck constant h and the electron charge e.  Its value is, therefore, the
same for any superconductor.

Ref:  https://en.wikipedia.org/wiki/Magnetic_flux_quantum
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?flxquhs2e
''' ),

    'molar_gas_constant' :
        RPNConstantInfo( '8.3144598', 'joule/mole*kelvin',
                          [ 'gas_constant', 'ideal_gas_constant', 'universal_gas_constant' ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?r
''' ),

    'newton_constant' :
        RPNConstantInfo( '6.67408e-11', 'meter^3/kilogram*second^2', [ 'G', 'newtons_constant' ], False,
                         'Newton\'s constant of gravitation',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?bg
''' ),

    'nuclear_magneton' :
        RPNConstantInfo( '5.050783699e-27', 'joule/tesla', [ ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?mun

''' ),

    'planck_constant' :
        RPNConstantInfo( '6.62607015e-34', 'kilogram*meter^2/second', [ 'h', 'planck' ], False,
                         '',
                         '''
Ref:  https://en.wikipedia.org/wiki/Planck_constant
The Planck constant (denoted h, also called Planck's constant) is a physical
constant that is the quantum of electromagnetic action, which relates the
energy carried by a photon to its frequency.  A photon's energy is equal to
its frequency multiplied by the Planck constant.  The Planck constant is of
fundamental importance in quantum mechanics, and in metrology it is the basis
for the definition of the kilogram.

This is the exact value, set on 20 Nov 2018 by the General Conference on
Weights and Measures.
''' ),

    'reduced_planck_constant' :
        RPNConstantInfo( fdiv( mpmathify( '6.626070040e-34' ), fmul( 2, pi ) ), 'kilogram*meter^2/second',
                         [ 'h_bar', 'reduced_planck', 'dirac', 'dirac_constant' ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?h
''' ),

    'rydberg_constant' :
        RPNConstantInfo( '10973731.568508', 'meter^-1', [ ], False,
                         '',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?ryd
''' ),

    'speed_of_light' :
        RPNConstantInfo( '299792458', 'meter/second',
                         [ 'c', 'lightspeed', 'light_speed', 'planck_speed', 'planck_velocity', 'light' ], False,
                         'the speed of light in a vacuum',
                         '''
Ref:  CODATA 2014 value - https://physics.nist.gov/cgi-bin/cuu/Value?c
''' ),

    # physical quantities
    'aa_battery' :
        RPNConstantInfo( '15400', 'joule', [ ], True,
                         'Typical energy charge of a fully-charged alkaline AA battery',
                         '''
''' ),

    'gallon_of_ethanol' :
        RPNConstantInfo( '8.4e7', 'joule', [ ], True,
                         'Energy content of a U.S. gallon of ethanol',
                         '''
''' ),

    'gallon_of_gasoline' :
        RPNConstantInfo( '1.2e8', 'joule', [ ], True,
                         'Typical energy content of a U.S. gallon of gasoline',
                         '''
''' ),

    'density_of_water' :
        RPNConstantInfo( '997.0474', 'kilogram/meter^3', [ 'water' ], True,
                         'Density of pure water at 25 degress Celsius',
                         '''
''' ),

    'solar_constant' :
        RPNConstantInfo( '1360.8', 'watt/meter^2', [ ], True,
                         'Average maximum energy received from the Sun on the Earth\'s surface',
                         '''
This constant represents the average maximum amount of luminous energy the
Earth receives from the Sun.  The solar constant does vary slightly over
time due to fluctuations in solar energy output.
''' ),

    # subatomic particle constants
    'alpha_particle_mass' :
        RPNConstantInfo( '6.644657230e-27', 'kilogram', [ ], True,
                         'Alpha particle (helium nucleus) mass',
                         '''
The alpha particle is the equivalent of a helium nucleus, and consists of two
protons and two neutrons.
''' ),

    'deuteron_mass' :
        RPNConstantInfo( '3.34358550157e-27', 'kilogram', [ ], True,
                         'Deuterium nucleus mass',
                         '''
The nucleus of deuterium is called a deuteron.  It has a mass of
2.013553212745(40) u (equal to 1875.612928(12) MeV).

The charge radius of the deuteron is 2.1413(25) fm.[21] Like the proton radius,
measurements using muonic deuterium produce a significantly smaller result:
2.12562(78) fm.[22] This is 6s less than the accepted CODATA 2014 value,
measured using electrons, and confirms the unresolved proton charge radius anomaly.

Ref:  https://en.wikipedia.org/wiki/Deuterium#Deuteron_mass_and_radius
''' ),

    'electron_mass' :
        RPNConstantInfo( '9.10938356e-31', 'kilogram', [ 'electron_rest_mass' ], True,
                         '',
                         '''
The electron rest mass is the mass of a stationary electron, also known as the
invariant mass of the electron.  It is one of the fundamental constants of
physics.  It has a value of about 9.109x10^-31 kilograms or about 5.486x10^-4
atomic mass units, equivalent to an energy of about 8.187xe10^-14 joules or about
0.5110 MeV.

https://en.wikipedia.org/wiki/Electron_rest_mass
''' ),

    'helion_mass' :
        RPNConstantInfo( '5.006412700e-27', 'kilogram', [ ], True,
                         'Helium-3 nucleus mass',
                         '''
A helion is a short name for the naked nucleus of helium, a doubly positively
charged helium ion. In practice, helion refers specifically to the nucleus of
the helium-3 isotope, consisting of two protons and one neutron.  The nucleus
of the other stable isotope of helium, helium-4 isotope, which consists of two
protons and two neutrons, is specifically called an alpha particle.

This particle is emitted in the decay of tritium, an isotope of hydrogen.

https://en.wikipedia.org/wiki/Helion_(chemistry)
https://physics.nist.gov/cgi-bin/cuu/Value?mh
''' ),

    'muon_mass' :
        RPNConstantInfo( '1.883531594e-28', 'kilogram', [ ], True,
                         '',
                         '''
The muon, (from the Greek letter mu, used to represent it) is an elementary
particle similar to the electron, with an electric charge of -1 e and a spin of
1/2, but with a much greater mass.  It is classified as a lepton.  As is the
case with other leptons, the muon is not believed to have any sub-structure -
that is, it is not thought to be composed of any simpler particles.

Ref:  https://en.wikipedia.org/wiki/Muon
''' ),

    'neutron_mass' :
        RPNConstantInfo( '1.674927471e-27', 'kilogram', [ ], True,
                         '',
                         '''
The neutron is a subatomic particle, with no net electric charge and a mass
slightly larger than that of a proton.  Protons and neutrons constitute the
nuclei of atoms.  Since protons and neutrons behave similarly within the
nucleus, and each has a mass of approximately one atomic mass unit, they are
both referred to as nucleons.  Their properties and interactions are described
by nuclear physics.

Ref:  https://en.wikipedia.org/wiki/Neutron
''' ),

    'proton_mass' :
        RPNConstantInfo( '1.672621898e-27', 'kilogram', [ ], True,
                         '',
                         '''
A proton is a subatomic particle with a positive electric charge of +1
elementary charge and a mass slightly less than that of a neutron.  Protons
and neutrons, each with masses of approximately one atomic mass unit, are
collectively referred to as "nucleons".

One or more protons are present in the nucleus of every atom; they are a
necessary part of the nucleus.  The number of protons in the nucleus is the
defining property of an element, and is referred to as the atomic number
(represented by the symbol Z). Since each element has a unique number of
protons, each element has its own unique atomic number.

https://en.wikipedia.org/wiki/Proton
''' ),

    'tau_mass' :
        RPNConstantInfo( '3.16747e-27', 'kilogram', [ ], True,
                         '',
                         '''
The tau, also called the tau lepton, tau particle, or tauon, is an elementary
particle similar to the electron, with negative electric charge and a spin of
1/2. Together with the electron, the muon, and the three neutrinos, it is a
lepton.

https://en.wikipedia.org/wiki/Tau_(particle)
''' ),

    'triton_mass' :
        RPNConstantInfo( '5.007356665e-27', 'kilogram', [ ], True,
                         '',
                         '''
Tritium, also known as hydrogen-3, is a radioactive isotope of hydrogen.  The
nucleus of tritium (sometimes called a triton) contains one proton and two
neutrons, whereas the nucleus of protium (by far the most abundant hydrogen
isotope) contains one proton and no neutrons.  Naturally occurring tritium is
extremely rare on Earth, where trace amounts are formed by the interaction of
the atmosphere with cosmic rays.  It can be produced by irradiating lithium
metal or lithium-bearing ceramic pebbles in a nuclear reactor.

Ref:  https://en.wikipedia.org/wiki/Tritium
''' ),

    'triple_point_of_water' :
        RPNConstantInfo( '273.16', 'kelvin', [ ], True,
                         '',
                         '''
In thermodynamics, the triple point of a substance is the temperature and
pressure at which the three phases (gas, liquid, and solid) of that substance
coexist in thermodynamic equilibrium.

The triple point of water was used to define the kelvin, the base unit of
thermodynamic temperature in the International System of Units (SI).  The value
of the triple point of water was fixed by definition, rather than measured, but
that changed with the 2019 redefinition of SI base units.

Ref:  https://en.wikipedia.org/wiki/Triple_point
''' ),

    # heavenly body constants
    'sun_luminosity' :
        RPNConstantInfo( '3.826e26', 'watt', [ 'solar_luminosity' ], True,
                         '',
                         '''
The watt (symbol: W) is a unit of power.  In the International System of Units
(SI) it is defined as a derived unit of 1 joule per second, and is used to
quantify the rate of energy transfer.

Ref:  https://en.wikipedia.org/wiki/Watt
''' ),

    'sun_mass' :
        RPNConstantInfo( '1.988500e30', 'kilogram', [ 'solar_mass' ], True,
                         '',
                         '''
Ref:  http://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
''' ),

    'sun_radius' :
        RPNConstantInfo( '6.9599e8', 'meter', [ 'solar_radius' ], True,
                         '',
                         '''
''' ),

    'sun_volume' :
        RPNConstantInfo( '1.412e27', 'meter^3', [ 'solar_volume' ], True,
                         '',
                         '''
''' ),


    'mercury_mass' :
        RPNConstantInfo( '3.301e26', 'kilogram', [ ], True,
                         'the mass of the planet Mercury',
                         '''
''' ),

    # equitorial radius
    'mercury_radius' :
        RPNConstantInfo( '2.4397e6', 'meter', [ ], True,
                         'the radius of the planet Mercury',
                         '''
''' ),

    # sidereal orbit period
    'mercury_revolution' :
        RPNConstantInfo( '87.969', 'day', [ 'mercury_year' ], True,
                         'the revolution time of the planet Mercury around the Sun',
                         '''
''' ),

    'mercury_volume' :
        RPNConstantInfo( '6.083e19', 'meter^3', [ ], True,
                         'the volume of the planet Mercury',
                         '''
''' ),

    'venus_mass' :
        RPNConstantInfo( '4.8689952e24', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'venus_radius' :
        RPNConstantInfo( '6.0518e6', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'venus_revolution' :
        RPNConstantInfo( '224.701', 'day', [ 'venus_year' ], True,
                         '',
                         '''
''' ),

    'venus_volume' :
        RPNConstantInfo( '9.2843e20', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'earth_density' :
        RPNConstantInfo( '5.514', 'gram/centimeter^3', [ ], True,   # https://en.wikipedia.org/wiki/Earth#Composition_and_structure
                         '',
                         '''
''' ),

    'earth_gravity' :
        RPNConstantInfo( '9.80665', 'meter/second^2',               # based on earth_radius
                         [ 'earth_gravities', 'gee', 'gees', 'standard_gravity', 'standard_gravities' ], True,
                         '',
                         '''
''' ),

    'earth_mass' :
        RPNConstantInfo( '5.9640955e24', 'kilogram', [ ], True,     # based on earth_radius and earth_gravity
                         '',
                         '''
''' ),

    'earth_radius' :
        RPNConstantInfo( '6371800', 'meter', [ ], True,             # https://en.wikipedia.org/wiki/Earth_radius#Global_average_radii - volumetric radius
                         '',
                         '''
''' ),

    'earth_volume' :
        RPNConstantInfo( '1.083207324897e21', 'meter^3', [ ], True, # based on earth_radius
                         '',
                         '''
''' ),

    'sidereal_year' :
        RPNConstantInfo( '365.256360417', 'day', [ ], True,
                         '',
                         '''
''' ),

    'tropical_year' :
        RPNConstantInfo( '365.24219', 'day', [ 'solar_year' ], True,
                         '',
                         '''
The definition used is the calculation of the mean tropical year on
1 January 2000.
''' ),

    'moon_gravity' :
        RPNConstantInfo( '1.62', 'meter/second^2',                  # based on moon_radius
                         [ 'moon_gravities', 'lunar_gravity', 'lunar_gravities' ], True,
                         '',
                         '''
''' ),

    'moon_mass' :
        RPNConstantInfo( '7.342e22', 'kilogram', [ 'lunar_mass' ], True,
                         '',
                         '''
''' ),


    'moon_radius' :
        RPNConstantInfo( '1.7381e6', 'meter', [ 'lunar_radius' ], True,
                         '',
                         '''
''' ),

    'moon_revolution' :
        RPNConstantInfo( '27.321662', 'day', [ 'sidereal_month', 'lunar_revolution' ], True,
                         '',
                         '''
''' ),

    'moon_volume' :
        RPNConstantInfo( '2.1958e19', 'meter^3', [ 'lunar_volume' ], True,
                         '',
                         '''
''' ),

    'mars_mass' :
        RPNConstantInfo( '6.4191269e23', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'mars_radius' :
        RPNConstantInfo( '3.3962e6', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'mars_revolution' :
        RPNConstantInfo( '686.980', 'day', [  'mars_year' ], True,
                         '',
                         '''
''' ),

    'mars_volume' :
        RPNConstantInfo( '1.6318e20', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_mass' :
        RPNConstantInfo( '1.8983e27', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_radius' :
        RPNConstantInfo( '7.1492e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'jupiter_revolution' :
        RPNConstantInfo( '11.862', 'year', [ 'jupiter_year' ], True,
                         '',
                         '''
''' ),

    'jupiter_volume' :
        RPNConstantInfo( '1.43128e24', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'saturn_mass' :
        RPNConstantInfo( '5.6836e26', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'saturn_radius' :
        RPNConstantInfo( '6.0268e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'saturn_revolution' :
        RPNConstantInfo( '29.457', 'year', [ 'saturn_year' ], True,
                         '',
                         '''
''' ),

    'saturn_volume' :
        RPNConstantInfo( '8.2713e23', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'uranus_mass' :
        RPNConstantInfo( '8.6816e25', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'uranus_radius' :
        RPNConstantInfo( '2.5559e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'uranus_revolution' :
        RPNConstantInfo( '84.011', 'year', [ 'uranus_year' ], True,
                         '',
                         '''
''' ),

    'uranus_volume' :
        RPNConstantInfo( '6.833e22', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'neptune_mass' :
        RPNConstantInfo( '1.0242e26', 'kilogram', [ ], True,
                         '',
                         '''
''' ),

    'neptune_radius' :
        RPNConstantInfo( '2.4764e7', 'meter', [ ], True,
                         '',
                         '''
''' ),

    'neptune_revolution' :
        RPNConstantInfo( '164.79', 'year', [ 'neptune_year' ], True,
                         '',
                         '''
''' ),

    'neptune_volume' :
        RPNConstantInfo( '6.254e22', 'meter^3', [ ], True,
                         '',
                         '''
''' ),

    'pluto_mass' :
        RPNConstantInfo( '1.0303e22', 'kilogram', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_radius' :
        RPNConstantInfo( '1.185e6', 'meter', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_revolution' :
        RPNConstantInfo( '247.94', 'year', [ 'pluto_year' ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    'pluto_volume' :
        RPNConstantInfo( '6.97e18', 'meter^3', [ ], True,
                         '',
                         '''
Yes, I still count Pluto as a planet.
''' ),

    # settings constants
    'default' :
        RPNConstantInfo( '-1', '', [ ], False,
                         '\'default\' simply evaluates to -1',
                         '''
used with settings operators

''' ),

    'false' :
        RPNConstantInfo( 0, '', [ ], False,
                         '\'false\' simply evaluates to 0',
                         '''
used with boolean settings operators

''' ),

    'true' :
        RPNConstantInfo( 1, '', [ ], False,
                         '\'true\' simply evaluates to 1',
                         '''
used with boolean settings operators

rpn (1)>5 12 **
244140625
rpn (2)>true comma
1
rpn (3)>5 12 **
244,140,625
''' ),

    # day of week constants
    'monday' :
        RPNConstantInfo( 1, '', [ 'mon' ], False,
                         '',
                         '''
This is defined for convenience for use with date operators.
''' ),

    'tuesday' :
        RPNConstantInfo( 2, '', [ 'tue', 'tues' ], False,
                         '',
                         '''
''' ),

    'wednesday' :
        RPNConstantInfo( 3, '', [ 'wed' ], False,
                         '',
                         '''
''' ),

    'thursday' :
        RPNConstantInfo( 4, '', [ 'thu', 'thur','thurs' ], False,
                         '',
                         '''
''' ),

    'friday' :
        RPNConstantInfo( 5, '', [ 'fri' ], False,
                         '',
                         '''
''' ),

    'saturday' :
        RPNConstantInfo( 6, '', [ 'sat' ], False,
                         '',
                         '''
''' ),

    'sunday' :
        RPNConstantInfo( 7, '', [ ], False,
                         '',
                         '''
''' ),

    # month constants
    'january' :
        RPNConstantInfo( 1, '', [ 'jan' ], False,
                         '',
                         '''
''' ),

    'february' :
        RPNConstantInfo( 2, '', [ 'feb' ],  False,
                         '',
                         '''
''' ),

    'march' :
        RPNConstantInfo( 3, '', [ 'mar' ], False,
                         '',
                         '''
''' ),

    'april' :
        RPNConstantInfo( 4, '', [ 'apr' ], False,
                         '',
                         '''
''' ),

    'may' :
        RPNConstantInfo( 5, '', [ ], False,
                         '',
                         '''
''' ),

    'june' :
        RPNConstantInfo( 6, '', [ 'jun' ], False,
                         '',
                         '''
''' ),

    'july' :
        RPNConstantInfo( 7, '', [ 'jul' ], False,
                         '',
                         '''
''' ),

    'august' :
        RPNConstantInfo( 8, '', [ 'aug' ], False,
                         '',
                         '''
''' ),

    'september' :
        RPNConstantInfo( 9, '', [ 'sep' ], False,
                         '',
                         '''
''' ),

    'october' :
        RPNConstantInfo( 10, '', [ 'oct' ], False,
                         '',
                         '''
''' ),

    'november' :
        RPNConstantInfo( 11, '', [ 'nov' ], False,
                         '',
                         '''
''' ),

    'december' :
        RPNConstantInfo( 12, '', [ 'dec' ], False,
                         '',
                         '''
''' ),

    # programming integer constants
    'max_char' :
        RPNConstantInfo( ( 1 << 7 ) - 1, '', [ 'maxchar', 'max_int8', 'maxint8' ], False,
                         'the maximum 8-bit signed integer',
                         '''
This is the largest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''' ),

    'max_double' :
        RPNConstantInfo( getMaxDouble( ), '', [ 'maxdouble' ], False,
                         'the largest value that can be represented by a 64-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'max_float' :
        RPNConstantInfo( getMaxFloat( ), '', [ 'maxfloat' ], False,
                         'the largest value that can be represented by a 32-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'max_long' :
        RPNConstantInfo( ( 1 << 31 ) - 1, '',
                         [ 'max_int', 'maxint', 'max_int32', 'maxint32', 'maxlong' ], False,
                         'the maximum 32-bit signed integer',
                         '''
This is the largest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''' ),

    'max_longlong' :
        RPNConstantInfo( ( 1 << 63 ) - 1, '', [ 'max_int64', 'maxint64', 'maxlonglong' ], False,
                         'the maximum 64-bit signed integer',
                         '''
This is the largest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''' ),

    'max_quadlong' :
        RPNConstantInfo( ( 1 << 127 ) - 1, '',
                         [ 'max_int128', 'maxint128', 'max_quad', 'maxquad', 'maxquadlong' ], False,
                         'the maximum 128-bit signed integer',
                         '''
This is the largest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''' ),

    'max_short' :
        RPNConstantInfo( ( 1 << 15 ) - 1, '', [ 'max_int16', 'maxint16', 'maxshort' ], False,
                         'the maximum 16-bit signed integer',
                         '''
This is the largest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''' ),

    'max_uchar' :
        RPNConstantInfo( ( 1 << 8 ) - 1, '', [ 'max_uint8', 'maxuint8', 'maxuchar' ], False,
                         'the maximum 8-bit unsigned integer',
                         '''
This is the largest number that can be represented by an 8-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ulong' :
        RPNConstantInfo( ( 1 << 32 ) - 1, '',
                         [ 'max_uint32', 'maxuint32', 'max_uint', 'maxuint', 'maxulong' ], False,
                         'the maximum 32-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 32-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ulonglong' :
        RPNConstantInfo( ( 1 << 64 ) - 1, '', [ 'max_uint64', 'maxuint64', 'maxulonglong' ], False,
                         'the maximum 64-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 64-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_uquadlong' :
        RPNConstantInfo( ( 1 << 128 ) - 1, '', [ 'max_uint128', 'maxuint128', 'maxuquadlong' ], False,
                         'the maximum 128-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 128-bit unsigned
integer assuming two's complement representation.
''' ),

    'max_ushort' :
        RPNConstantInfo( ( 1 << 16 ) - 1, '', [ 'max_uint16', 'maxuint16', 'maxushort' ], False,
                         'the maximum 16-bit unsigned integer',
                         '''
This is the largest number that can be represented by a 16-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_char' :
        RPNConstantInfo( -( 1 << 7 ), '', [ 'min_int8', 'minint8', 'minchar' ], False,
                         'the minimum 8-bit signed integer',
                         '''
This is the smallest number that can be represented by an 8-bit signed
integer assuming two's complement representation.
''' ),

    'min_double' :
        RPNConstantInfo( getMinDouble( ), '', [ 'mindouble' ], False,
                         'the smallest value that can be represented by a 64-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'min_float' :
        RPNConstantInfo( getMinFloat( ), '', [ 'minfloat' ], False,
                         'the smallest value that can be represented by a 32-bit IEEE 754 float',
                         '''
For all IEEE 754 floating point numbers, rpn assumes big-endian byte ordering.
''' ),

    'min_long' :
        RPNConstantInfo( -( 1 << 31 ), '', [ 'min_int32', 'minint32', 'minlong' ], False,
                         'the minimum 32-bit signed integer',
                         '''
This is the smallest number that can be represented by a 32-bit signed
integer assuming two's complement representation.
''' ),

    'min_longlong' :
        RPNConstantInfo( -( 1 << 63 ), '', [ 'min_int64', 'minint64', 'minlonglong' ], False,
                         'the minimum 64-bit signed integer',
                         '''
This is the smallest number that can be represented by a 64-bit signed
integer assuming two's complement representation.
''' ),

    'min_quadlong' :
        RPNConstantInfo( -( 1 << 127 ), '',
                         [ 'min_int128', 'minint128', 'min_quad', 'minquad', 'minquadlong' ], False,
                         'the minimum 128-bit signed integer',
                         '''
This is the smallest number that can be represented by a 128-bit signed
integer assuming two's complement representation.
''' ),

    'min_short' :
        RPNConstantInfo( -( 1 << 15 ), '', [ 'min_int16', 'minint16', 'minshort' ], False,
                         'the minimum 16-bit signed integer',
                         '''
This is the smallest number that can be represented by a 16-bit signed
integer assuming two's complement representation.
''' ),

    'min_uchar' :
        RPNConstantInfo( 0, '', [ 'min_uint8', 'minuint8', 'minuchar' ], False,
                         'the minimum 8-bit unsigned integer',
                         '''
This is the smallest number that can be represented by an 8-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ulong' :
        RPNConstantInfo( 0, '', [ 'min_uint32', 'minuint32', 'minulong' ], False,
                         'the minimum 32-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 32-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ulonglong' :
        RPNConstantInfo( 0, '', [ 'min_uint64', 'minuint64', 'minulonglong' ], False,
                         'the minimum 64-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 64-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_uquadlong' :
        RPNConstantInfo( 0, '', [ 'min_uint128', 'minuint128', 'min_quad', 'minquad', 'minquadlong' ], False,
                         'the minimum 128-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 128-bit unsigned
integer assuming two's complement representation.
''' ),

    'min_ushort' :
        RPNConstantInfo( 0, '', [ 'min_uint16', 'minuint16', 'minushort' ], False,
                         'the minimum 16-bit unsigned integer',
                         '''
This is the smallest number that can be represented by a 16-bit unsigned
integer assuming two's complement representation.
''' ),

    # mathematical constants
    'i' :
        RPNConstantInfo( 1j, '', [ 'min_uint16', 'minuint16', 'minushort' ], False,
                         'i, the square root of -1, which is the same as \'1j\'',
                         '''
The imaginary number i is the square root of -1.  Python's normal syntax for
imaginary numbers uses the 'j' suffix with a number, but for just the value of i
itself, '1j' seems clumsy, so there's the 'i' constant.

'-i' however cannot be used since that is the command-line switch for
interactive mode.
''' ),

}

