#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnUnits
#//
#//  RPN command-line calculator unit conversion declarations
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

from mpmath import *

from rpnDeclarations import *
from rpnEstimates import *


# The candela is the luminous intensity, in a given direction, of a source
# that emits monochromatic radiation of frequency 540 × 1012 hertz and that
# has a radiant intensity in that direction of 1/683 watt per steradian.

# It follows that the spectral luminous efficacy for monochromatic radiation of
# frequency of 5.40e14 hertz is exactly 683 lumens per watt, K = 683 lm/W
# = 683 cd sr/W.

# Derived quantity                                            SI coherent derived unit
#
# area                          A                             square metre                    m^2
# volume                        V                             cubic metre                     m^3
# speed, velocity               v                             metre per second                m/s
# acceleration                  a                             metre per second squared        m/s^2
# wavenumber                    small sigma, nu tilde         reciprocal metre                m^-1
# density, mass density         small rho                     kilogram per cubic metre        kg/m3
# surface density               small rho sub A               kilogram per square metre       kg/m2
# specific volume               v                             cubic metre per kilogram        m3/kg
# current density               j                             ampere per square metre         A/m2
# magnetic field strength       H                             ampere per metre                A/m
# amount concentration,         c                             mole per cubic metre            mol/m3
# mass concentration            small rho, small gamma        kilogram per cubic metre        kg/m3
# luminance                     L sub v                       candela per square metre        cd/m2
# refractive index              n                             one                             1
# relative permeability         mu sub r                      one                             1
#
#
# SI coherent derived unit
#
# Derived Quantity              Name            Symbol              other SI units     SI Base Units
#
# plane angle                   radian          rad                 1                  m/m
# solid angle                   steradian       sr                  1                  m2/m2
# frequency                     hertz           Hz                                     s^-1
# force                         newton          N                                      m kg s^-2
# pressure, stress              pascal          Pa                  N/m2               m^-1 kg s^-2
# energy, work, amount of heat  joule           J                   N m                m2 kg s^-2
#
# power, radiant flux           watt            W J/s m2 kg s^-3
#
# electric charge,              coulomb         C                                      s A
# amount of electricity
#
# electric potential difference, volt           V                   W/A                m2 kg s^-3 A^-1
# electromotive force
#
# capacitance                   farad           F                   C/V                m^-2 kg^-1 s4 A2
# electric resistance           ohm             omega               V/A                m2 kg s^-3 A^-2
# electric conductance          siemens         S                   A/V                m^-2 kg^-1 s3 A2
# magnetic flux                 weber           Wb                  V s                m2 kg s^-2 A^-1
# magnetic flux density         tesla           T                   Wb/m2              kg s^-2 A^-1
# inductance                    henry           H                   Wb/A               m2 kg s^-2 A^-2
# Celsius temperature           degree Celsius  degree C                               K
# luminous flux                 lumen           lm                  cd sr              cd
# illuminance                   lux             lx                  lm/m2              m^-2 cd
#
# activity referred to          becquerel       Bq                                     s^-1
# a radionuclide
#
# absorbed dose,                gray            Gy                  J/kg               m2 s^-2
# specific energy (imparted),
# kerma
#
# dose equivalent,              sievert         Sv                  J/kg               m2 s^-2
# ambient dose equivalent,
# directional dose equivalent,
# personal dose equivalent
#
# catalytic activity            katal           kat                                    s^-1 mol
#
#
# dynamic viscosity             pascal second                       Pa s               m^-1 kg s^-1
# moment of force               newton metre                        N m                m2 kg s^-2
# surface tension               newton per metre                    N/m                kg s^-2
# angular velocity              radian per second                   rad/s              m m^-1 s^-1 = s^-1
# angular acceleration          radian per second squared           rad/s2             m m^-1 s^-2 = s^-2
#
# heat flux density,            watt per square metre               W/m2               kg s^-3
# irradiance
#
# heat capacity, entropy        joule per kelvin                    J/K                m2 kg s^-2 K^-1
#
# specific heat capacity,       joule per kilogram kelvin           J/(kg K)           m2 s^-2 K^-1
# specific entropy
#
# specific energy               joule per kilogram                  J/kg               m2 s^-2
# thermal conductivity          watt per metre kelvin               W/(m K)            m kg s^-3 K^-1
# energy density                joule per cubic metre               J/m3               m^-1 kg s^-2
# electric field strength       volt per metre                      V/m                m kg s^-3 A^-1
# electric charge density       coulomb per cubic metre             C/m3               m^-3 s A
# surface charge density        coulomb per square metre            C/m2               m^-2 s A
#
# electric flux density,        coulomb per square metre            C/m2               m^2 s A
# electric displacement
#
# permittivity                  farad per metre                     F/m                m^3 kg^1 s4 A2
# permeability                  henry per metre                     H/m                m kg s^-2 A^-2
# molar energy                  joule per mole                      J/mol              m2 kg s^-2 mol^-1
#
# molar entropy,                joule per mole kelvin               J/(mol K)          m2 kg s^-2 K^-1 mol^-1
# molar heat capacity
#
# exposure (x- and gamma-rays)  coulomb per kilogram                C/kg               kg^-1 s A
# absorbed dose rate            gray per second                     Gy/s               m2 s^3
# radiant intensity             watt per steradian                  W/sr               m4 m^-2 kg s^-3 = m2 kg s^-3
# radiance                      watt per square metre steradian     W/(m2 sr)          m2 m^-2 kg s^-3 = kg s^-3
#
# catalytic activity            katal per cubic metre               kat/m3             m^-3 s^-1 mol
# concentration
#
# Quantity              Name of unit                Symbol                  Value in SI units (a)
#
# Units accepted for use with the SI
#
# energy                electronvolt                eV                      1 eV = 1.602 176 53 (14) * 10e-19 J
#
# mass                  dalton,                     Da                      1 Da = 1.660 538 86 (28) * 10e-27 kg
#                       unified atomic mass unit    u                       1 u = 1 Da
#
# length                astronomical unit           ua                      1 ua = 1.495 978 706 91 (6) * 10e11 m
#
#
# Natural units (n.u.)
#
# speed                 n.u. of speed               c sub 0                 299 792 458 m/s (exact)
#                       (speed of light in vacuum)
#
# action                n.u. of action              h                       1.054 571 68 (18) * 10e-34 J s
#                       (reduced Planck constant)
#
# mass                  n.u. of mass                m sub e                 9.109 3826 (16) * 10e-31 kg
#                       (electron mass)
#
# time                  n.u. of time                h/(m sub e c sub 0^2)   1.288 088 6677 (86) * 10e-21 s
#
# Atomic units (a.u.)
#
# charge                a.u. of charge,             e                       1.602 176 53 (14) * 10e-19 C
#                       (elementary charge)
#
# mass                  a.u. of mass,               m sub e                 9.109 3826 (16) * 10e-31 kg
#                       (electron mass)
#
# action                a.u. of action,             h                       1.054 571 68 (18) * 10e-34 J s
#                       (reduced Planck constant)
#
# length                a.u. of length, bohr        a sub 0                 0.529 177 2108 (18) * 10e-10 m
#                       (Bohr radius)
#
# energy                a.u. of energy, hartree     Eh                      4.359 744 17 (75) * 10e-18 J
#                       (Hartree energy)
#
# time                  a.u. of time                h/Eh                    # 2.418 884 326 505 (16) * 10e-17 s
#
#
# Other non-SI units
#
# Quantity              Name of unit                Symbol                  Value in SI units
#
# pressure              bar                         bar                     1 bar = 0.1 MPa = 100 kPa = 105 Pa
#                       millimetre of mercury       mmHg                    1 mmHg ~= 133.322 Pa
# length                angstrom                    A                       1 A = 0.1 nm = 100 pm = 10-10 m
# distance              nautical mile               M                       1 M = 1852 m
# area                  barn                        b                       1 b = 100 fm^2 = (10^-12 cm)^2 = 10^-28 m^2
# speed                 knot                        kn                      1 kn = (1852/3600) m/s
# logarithmic           neper                       Np
# ratio quantities      bel                         B                       numerical value of the neper, the
#                       decibel (h, i)              dB                      bel and the decibel]
#
#
# Quantity              Name of unit                Symbol                  Value in SI units
#
# energy                erg                         erg                     1 erg = 10-7 J
# force                 dyne                        dyn                     1 dyn = 10-5 N
# dynamic viscosity     poise                       P                       1 P = 1 dyn s cm-2 = 0.1 Pa s
# kinematic viscosity   stokes                      St                      1 St = 1 cm2 s^-1 = 10^-4 m2 s^-1
# luminance             stilb                       sb                      1 sb = 1 cd cm-2 = 10^4 cd m-2
# illuminance           phot                        ph                      1 ph = 1 cd sr cm-2 = 104 lx
# acceleration          gal                         Gal                     1 Gal = 1 cm s-2 = 10-2 m s-2
# magnetic flux         maxwell                     Mx                      1 Mx = 1 G cm2 = 10-8 Wb
# magnetic flux density gauss                       G                       1 G = 1 Mx cm-2 = 10-4 T
# magnetic field        oersted                     Oe                      1 Oe ^= (1000/4 pi ) A m^-1
#


#
# # particle wavelengths: the compton wavelength of a particle is
# # defined as h / m c where m is the mass of the particle.
#
# electronwavelength      h / m_e c
# lambda_C                electronwavelength
# protonwavelength        h / m_p c
# lambda_C,p              protonwavelength
# neutronwavelength       h / m_n c
# lambda_C,n              neutronwavelength
#
# # Magnetic moments
#
# bohrmagneton            e hbar / 2 electronmass
# mu_B                    bohrmagneton
# nuclearmagneton         e hbar /  2 protonmass
# mu_N                    nuclearmagneton
# mu_mu                  -4.49044807e-26 J/T  # Muon magnetic moment
# mu_p                    1.410606743e-26 J/T # Proton magnetic moment
# mu_e                   -928.476430e-26 J/T  # Electron magnetic moment
# mu_n                   -0.96623647e-26      # Neutron magnetic moment
# mu_d                    0.433073489e-26 J/T # Deuteron magnetic moment
# mu_t                    1.504609447e-26 J/T # Triton magnetic moment
# mu_h                   -1.074617486e-26 J/T # Helion magnetic moment
#
# crith                   0.089885 gram       # The crith is the mass of one
#                                             #   liter of hydrogen at standard
#                                             #   temperature and pressure.
#
# kayser                  1/cm            # Proposed as a unit for wavenumber
# balmer                  kayser          # Even less common name than "kayser"
#
# darcy           centipoise cm^2 / s atm # Measures permeability to fluid flow.
#
#                                         #   One darcy is the permeability of a
#                                         #   medium that allows a flow of cc/s
#                                         #   of a liquid of centipoise viscosity
#                                         #   under a pressure gradient of
#                                         #   atm/cm.  Named for H. Darcy.
#
# mobileohm               cm / dyn s      # mobile ohm, measure of mechanical
#                                         #   mobility
# mechanicalohm           dyn s / cm      # mechanical resistance
# acousticalohm           dyn s / cm^5    # ratio of the sound pressure of
#                                         #   1 dyn/cm^2 to a source of strength
#                                         #   1 cm^3/s
# ray                     acousticalohm
# rayl                    dyn s / cm^3    # Specific acoustical resistance
# eotvos                  1e-9 Gal/cm     # Change in gravitational acceleration
#                                         #   over horizontal distance
#
#
# intampere               0.999835 A    # Defined as the current which in one
# intamp                  intampere     #   second deposits .001118 gram of
#                                       #   silver from an aqueous solution of
#                                       #   silver nitrate.
# intfarad                0.999505 F
# intvolt                 1.00033 V
# intohm                  1.000495 ohm  # Defined as the resistance of a
#                                       #   uniform column of mercury containing
#                                       #   14.4521 gram in a column 1.063 m
#                                       #   long and maintained at 0 degC.
# daniell                 1.042 V       # Meant to be electromotive force of a
#                                       #   Daniell cell, but in error by .04 V
# faraday                 N_A e mol     # Charge that must flow to deposit or
# faraday_phys            96521.9 C     #   liberate one gram equivalent of any
# faraday_chem            96495.7 C     #   element.  (The chemical and physical
#                                       #   values are off slightly from what is
#                                       #   obtained by multiplying by amu_chem
#                                       #   or amu_phys.  These values are from
#                                       #   a 1991 NIST publication.)  Note that
#                                       #   there is a Faraday constant which is
#                                       #   equal to N_A e and hence has units of
#                                       #   C/mol.
# kappline                6000 maxwell  # Named by and for Gisbert Kapp
# siemensunit             0.9534 ohm    # Resistance of a meter long column of
#                                       #   mercury with a 1 mm cross section.
#
# blondel                 apostilb      # Named after a French scientist.
#
# # Some luminance data from the IES Lighting Handbook, 8th ed, 1993
#
# sunlum                  1.6e9 cd/m^2  # at zenith
# sunillum                100e3 lux     # clear sky
# sunillum_o              10e3 lux      # overcast sky
# sunlum_h                6e6 cd/m^2    # value at horizon
# skylum                  8000 cd/m^2   # average, clear sky
# skylum_o                2000 cd/m^2   # average, overcast sky
# moonlum                 2500 cd/m^2
#
#
# anomalisticyear         365.2596 days       # The time between successive
#                                             #   perihelion passages of the
#                                             #   earth.
# siderealyear            365.256360417 day   # The time for the earth to make
#                                             #   one revolution around the sun
#                                             #   relative to the stars.
# tropicalyear            365.242198781 day   # The time needed for the mean sun
#                                             #   as defined above to increase
#                                             #   its longitude by 360 degrees.
#                                             #   Most references defined the
#                                             #   tropical year as the interval
#                                             #   between vernal equinoxes, but
#                                             #   this is misleading.  The length
#                                             #   of the season changes over time
#                                             #   because of the eccentricity of
#                                             #   the earth's orbit.  The time
#                                             #   between vernal equinoxes is
#                                             #   approximately 365.24237 days
#                                             #   around the year 2000.  See
#                                             #   "Mathematical Astronomy
#                                             #   Morsels" for more details.
# eclipseyear             346.62 days         # The line of nodes is the
#                                             #   intersection of the plane of
#                                             #   Earth's orbit around the sun
#                                             #   with the plane of the moon's
#                                             #   orbit around earth.  Eclipses
#                                             #   can only occur when the moon
#                                             #   and sun are close to this
#                                             #   line.  The line rotates and
#                                             #   appearances of the sun on the
#                                             #   line of nodes occur every
#                                             #   eclipse year.
# saros                   223 synodicmonth    # The earth, moon and sun appear in
#                                             #   the same arrangement every
#                                             #   saros, so if an eclipse occurs,
#                                             #   then one saros later, a similar
#                                             #   eclipse will occur.  (The saros
#                                             #   is close to 19 eclipse years.)
#                                             #   The eclipse will occur about
#                                             #   120 degrees west of the
#                                             #   preceeding one because the
#                                             #   saros is not an even number of
#                                             #   days.  After 3 saros, an
#                                             #   eclipse will occur at
#                                             #   approximately the same place.

# anomalisticmonth        27.55454977 day     # Time for the moon to travel from
#                                             #   perigee to perigee
# nodicalmonth            27.2122199 day      # The nodes are the points where
# draconicmonth           nodicalmonth        #   an orbit crosses the ecliptic.
# draconiticmonth         nodicalmonth        #   This is the time required to
#                                             #   travel from the ascending node
#                                             #   to the next ascending node.
# lunarmonth              29 days + 12 hours + 44 minutes + 2.8 seconds
#                                             # Mean time between full moons.
# synodicmonth            lunarmonth          #   Full moons occur when the sun
# lunation                synodicmonth        #   and moon are on opposite sides
# lune                    1|30 lunation       #   of the earth.  Since the earth
# lunour                  1|24 lune           #   moves around the sun, the moon
#                                             #   has to revolve a bit extra to
#                                             #   get into the full moon
#                                             #   configuration.

# lunaryear               12 lunarmonth
#
# # The Hewbrew year is also based on lunar months, but synchronized to the solar
# # calendar.  The months vary irregularly between 29 and 30 days in length, and
# # the years likewise vary.  The regular year is 353, 354, or 355 days long.  To
# # keep up with the solar calendar, a leap month of 30 days is inserted every
# # 3rd, 6th, 8th, 11th, 14th, 17th, and 19th years of a 19 year cycle.  This
# # gives leap years that last 383, 384, or 385 days.
#
#
# # Objects on the earth are charted relative to a perfect ellipsoid whose
# # dimensions are specified by different organizations.  The ellipsoid is
# # specified by an equatorial radius and a flattening value which defines the
# # polar radius.  These values are the 1996 values given by the International
# # Earth Rotation Service (IERS) whose reference documents can be found at
# # http://maia.usno.navy.mil/
#
# earthflattening         1|298.25642
# earthradius_equatorial  6378136.49 m
# earthradius_polar       (-earthflattening+1) earthradius_equatorial
#
# landarea                148.847e6 km^2
# oceanarea               361.254e6 km^2
#
# moonradius              1738 km         # mean value
# sunradius               6.96e8 m
#
#
# # Many astronomical values can be measured most accurately in a system of units
# # using the astronomical unit and the mass of the sun as base units.  The
# # uncertainty in the gravitational constant makes conversion to SI units
# # significantly less accurate.
#
# # The astronomical unit was defined to be the length of the of the semimajor
# # axis of a massless object with the same year as the earth.  With such a
# # definition in force, and with the mass of the sun set equal to one, Kepler's
# # third law can be used to solve for the value of the gravitational constant.
#
# # Kepler's third law says that (2 pi / T)^2 a^3 = G M where T is the orbital
# # period, a is the size of the semimajor axis, G is the gravitational constant
# # and M is the mass.  With M = 1 and T and a chosen for the earth's orbit, we
# # find sqrt(G) = (2 pi / T) sqrt(AU^3).  This constant is called the Gaussian
# # gravitational constant, apparently because Gauss originally did the
# # calculations.  However, when the original calculation was done, the value
# # for the length of the earth's year was inaccurate.  The value used is called
# # the Gaussian year.  Changing the astronomical unit to bring it into
# # agreement with more accurate values for the year would have invalidated a
# # lot of previous work, so instead the astronomical unit has been kept equal
# # to this original value.  This is accomplished by using a standard value for
# # the Gaussian gravitational constant.  This constant is called k.
# # Many values below are from http://ssd.jpl.nasa.gov/?constants
#
# gauss_k                 0.01720209895   # This beast has dimensions of
#                                         # au^(3|2) / day and is exact.
# gaussianyear      (2 pi / gauss_k) days # Year that corresponds to the Gaussian
#                                         # gravitational constant. This is a
#                                         # fictional year, and doesn't
#                                         # correspond to any celestial event.
# astronomicalunit         149597870700 m # IAU definition from 2012, exact
# au                     astronomicalunit # ephemeris for the above described
#                                         # astronomical unit.  (See the NASA
#                                         # site listed above.)
# solarmass                  1.9891e30 kg
# sunmass                       solarmass
#
#
# sundist                 1.0000010178 au # mean earth-sun distance
# moondist                3.844e8 m       # mean earth-moon distance
# sundist_near            1.471e11 m      # earth-sun distance at perihelion
# sundist_far             1.521e11 m      # earth-sun distance at aphelion
#
# # The following are masses for planetary systems, not just the planet itself.
# # The comments give the uncertainty in the denominators.  As noted above,
# # masses are given relative to the solarmass because this is more accurate.
# # The conversion to SI is uncertain because of uncertainty in G, the
# # gravitational constant.
# #
# # Values are from http://ssd.jpl.nasa.gov/astro_constants.html
#
# mercurymass             solarmass / 6023600   # 250
# venusmass               solarmass / 408523.71 # 0.06
# earthmoonmass           solarmass / 328900.56 # 0.02
# marsmass                solarmass / 3098708   # 9
# jupitermass             solarmass / 1047.3486 # 0.0008
# saturnmass              solarmass / 3497.898  # 0.018
# uranusmass              solarmass / 22902.98  # 0.03
# neptunemass             solarmass / 19412.24  # 0.04
# plutomass               solarmass / 1.35e8    # 0.07e8
#
# moonearthmassratio      0.012300034 # uncertainty 3 x 10-9
# earthmass               earthmoonmass / ( 1 + moonearthmassratio)
# moonmass                moonearthmassratio earthmass
#
#
# # These are the old values for the planetary masses.  They may give
# # the masses of the planets alone.
#
# oldmercurymass             0.33022e24 kg
# oldvenusmass               4.8690e24 kg
# oldmarsmass                0.64191e24 kg
# oldjupitermass             1898.8e24 kg
# oldsaturnmass              568.5e24 kg
# olduranusmass              86.625e24 kg
# oldneptunemass             102.78e24 kg
# oldplutomass               0.015e24 kg
#
# # Mean radius from http://ssd.jpl.nsaa.gov/phys_props_planets.html which in
# # turn cites Global Earth Physics by CF Yoder, 1995.
#
# mercuryradius           2440 km
# venusradius             6051.84 km
# earthradius             6371.01 km
# marsradius              3389.92 km
# jupiterradius           69911 km
# saturnradius            58232 km
# uranusradius            25362 km
# neptuneradius           24624 km
# plutoradius             1151 km
#
# moongravity             1.62 m/s^2
#
#
# surveyorschain          66 surveyft
# surveychain             surveyorschain
# surveyorspole           1|4 surveyorschain
# surveyorslink           1|100 surveyorschain
# chain                   66 ft
# link                    1|100 chain
# ch                      chain
# USacre                  10 surveychain^2
# intacre                 10 chain^2       # Acre based on international ft
# intacrefoot             acre foot
# USacrefoot              USacre surveyfoot
# acrefoot                intacrefoot
# acre                    intacre
# section                 mile^2
# township                36 section
# homestead               160 acre # Area of land granted by the 1862 Homestead
#                                  # Act of the United States Congress
# gunterschain            surveyorschain
#
# engineerschain          100 ft
# engineerslink           1|100 engineerschain
# ramsdenschain           engineerschain
# ramsdenslink            engineerslink
#
# gurleychain             33 feet           # Andrew Ellicott chain is the
# gurleylink              1|50 gurleychain  # same length
#
# wingchain               66 feet           # Chain from 1664, introduced by
# winglink                1|80 wingchain    # Vincent Wing, also found in a
#                                           # 33 foot length with 40 links.
#
# # History.
#
# troughtonyard           914.42190 mm
# bronzeyard11            914.39980 mm
# mendenhallyard          surveyyard
# internationalyard       yard
#
#
# cable                   1|10 nauticalmile
# intcable                cable              # international cable
# cablelength             cable
# UScable                 100 USfathom
# navycablelength         720 USft           # used for depth in water
# marineleague            3 nauticalmile
# geographicalmile        brnauticalmile
# knot                    nauticalmile / hr
#
#
#
# # USA shoe sizes.  These express the length of the shoe or the length
# # of the "last", the form that the shoe is made on.  But note that
# # this only captures the length.  It appears that widths change 1/4
# # inch for each letter within the same size, and if you change the
# # length by half a size then the width changes between 1/8 inch and
# # 1/4 inch.  But this may not be standard.  If you know better, please
# # contact me.
#
# shoesize_delta          1|3 inch     # USA shoe sizes differ by this amount
# shoe_men0               8.25 inch
# shoe_women0             (7+11|12) inch
# shoe_boys0              (3+11|12) inch
# shoe_girls0             (3+7|12) inch
#
# shoesize_men(n) units=[1;inch]   shoe_men0 + n shoesize_delta ; \
#                                 (shoesize_men+(-shoe_men0))/shoesize_delta
# shoesize_women(n) units=[1;inch] shoe_women0 + n shoesize_delta ; \
#                                 (shoesize_women+(-shoe_women0))/shoesize_delta
# shoesize_boys(n) units=[1;inch]  shoe_boys0 + n shoesize_delta ; \
#                                 (shoesize_boys+(-shoe_boys0))/shoesize_delta
# shoesize_girls(n) units=[1;inch] shoe_girls0 + n shoesize_delta ; \
#                                 (shoesize_girls+(-shoe_girls0))/shoesize_delta
#
#
# buck                    US$
# fin                     5 US$
# sawbuck                 10 US$
# usgrand                 1000 US$
# greenback               US$
# key                     kg           # usually of marijuana, 60's
# lid                     1 oz         # Another 60's weed unit
# footballfield           usfootballfield
# usfootballfield         100 yards
# canadafootballfield     110 yards    # And 65 yards wide
# marathon                26 miles + 385 yards
#
# British
#
# goad                    4.5 UKft     # used for cloth, possibly named after the
#                                      #   stick used for prodding animals.
#
# virgate                 1|4 hide
# nook                    1|2 virgate
# rood                    furlong rod  # Area of a strip a rod by a furlong
# englishcarat            troyounce/151.5 # Originally intended to be 4 grain
#                                         #   but this value ended up being
#                                         #   used in the London diamond market
# mancus                  2 oz
# mast                    2.5 lb
# nailkeg                 100 lbs
# basebox                 31360 in^2      # Used in metal plating
#
#
# #
# # Counting measures
# #
#
#
# rep                     8.38 mGy     # Roentgen Equivalent Physical, the amount
#                                      #   of radiation which , absorbed in the
#                                      #   body, would liberate the same amount
#                                      #   of energy as 1 roentgen of X rays
#                                      #   would, or 97 ergs.
#


#//******************************************************************************
#//
#//  basicUnitTypes
#//
#//  0:  conversion from the basic unit types:
#//          length, mass, time, angle, energy, current, electric_potential,
#//          temperature, luminous_intensity, informantion_entropy,
#//          constant (not a real unit)
#//
#//  1:  'standard' unit of measurement
#//
#//  Note:  I chose not to incorporate mass-energy equivalence here.  I don't
#//         think it helps.  I just created the 'gram-equivalent' unit instead.
#//
#//         I probably want to make a special case for converting mass to
#//         energy so it will work with all mass units.
#//
#//******************************************************************************

basicUnitTypes = {
    'acceleration' : UnitTypeInfo(
        [ 'length/time^2' ],
        'meter/second^2',
        accelerationTable
    ),

    'angle' : UnitTypeInfo(
        [ 'angle' ],
        'radian',
        angleTable
    ),

    'area' : UnitTypeInfo(
        [ 'length^2' ],
        'square_meter',
        areaTable,
    ),

    'capacitance' : UnitTypeInfo(
        [ 'current^2*time^2/energy' ],
        'farad',
        capacitanceTable,
    ),

    'charge' : UnitTypeInfo(
        [ 'current*time' ],
        'coulomb',
        chargeTable,
    ),

    'constant' : UnitTypeInfo(
        [ 'constant' ],
        'unity',
        constantTable,
    ),

    'current' : UnitTypeInfo(
        [ 'current', 'electric_potential/electrical_resistance' ],
        'ampere',
        currentTable,
    ),

    'data_rate' : UnitTypeInfo(
        [ 'information_entropy/time' ],
        'bit/second',
        dataRateTable,
    ),

    'density' : UnitTypeInfo(
        [ 'mass/length^3' ],
        'gram/cubic_meter',
        densityTable,
    ),

    'dynamic_viscosity' : UnitTypeInfo(
        [ 'pressure*time' ],
        'pascal*second',
        dynamicViscosityTable,
    ),

    'electrical_conductance' : UnitTypeInfo(
        [ 'current^2/energy*time', 'current/electric_potential' ],
        'mho',
        electricalConductanceTable,
    ),

    'electrical_resistance' : UnitTypeInfo(
        [ 'energy*time/current^2', 'electric_potential/current' ],
        'ohm',
        electricalResistanceTable,
    ),

    'electric_potential' : UnitTypeInfo(
        [ 'energy/current*time', 'current*electrical_resistance' ],
        'volt',
        electricPotentialTable,
    ),

    'energy' : UnitTypeInfo(
        [ 'electric_potential*current*time', 'electric_potential*charge' ],
        'joule',
        energyTable,
    ),

    'force' : UnitTypeInfo(
        [ 'mass*length/time' ],
        'newton',
        forceTable,
    ),

    'frequency' : UnitTypeInfo(
        [ '1/time' ],
        'hertz',
        frequencyTable,
    ),

    'illuminance' : UnitTypeInfo(
        [ 'luminous_intensity*angle^2/length^2' ],
        'lux',
        illuminanceTable,
    ),

    'inductance' : UnitTypeInfo(
        [ 'electric_potential*time/current' ],
        'henry',
        inductanceTable,
    ),

    'information_entropy' : UnitTypeInfo(
        [ 'information_entropy' ],
        'bit',
        informationEntropyTable,
    ),

    'length' : UnitTypeInfo(
        [ 'length' ],
        'meter',
        lengthTable,
    ),

    'luminance' : UnitTypeInfo(
        [ 'luminous_intensity/length^2' ],
        'candela/meter^2',
        luminanceTable,
    ),

    'luminous_flux' : UnitTypeInfo(
        [ 'luminous_intensity*angle^2' ],
        'lumen',
        luminousFluxTable,
    ),

    'luminous_intensity' : UnitTypeInfo(
        [ 'luminous_intensity' ],
        'candela',
        luminousIntensityTable,
    ),

    'magnetic_field_strength' : UnitTypeInfo(
        [ 'charge/length' ],
        'ampere/meter',
        magneticFieldStrengthTable,
    ),

    'magnetic_flux' : UnitTypeInfo(
        [ 'electric_potential*time' ],
        'weber',
        magneticFluxTable,
    ),

    'magnetic_flux_density' : UnitTypeInfo(
        [ 'electric_potential*time/length^2' ],
        'tesla',
        magneticFluxDensityTable,
    ),

    'mass' : UnitTypeInfo(
        [ 'mass' ],
        'gram',
        massTable,
    ),

    'power' : UnitTypeInfo(
        [ 'energy/time' ],
        'watt',
        powerTable,
    ),

    'pressure' : UnitTypeInfo(
        [ 'mass/length^2' ],
        'pascal',
        pressureTable,
    ),

    'radiation_absorbed_dose' : UnitTypeInfo(
        [ 'energy/mass' ],
        'gray',
        radiationAbsorbedDoseTable,
    ),

    'radiation_equivalent_dose' : UnitTypeInfo(
        [ 'energy/mass' ],
        'sievert',
        radiationEquivalentDoseTable,
    ),

    'radiation_exposure' : UnitTypeInfo(
        [ 'current*time/mass' ],
        'coulomb/gram',
        radiationExposureTable,
    ),

    'radioactivity' : UnitTypeInfo(
        [ '1/time' ],
        'becquerel',
        radioactivityTable,
    ),

    'solid_angle' : UnitTypeInfo(
        [ 'angle^2' ],
        'steradian',
        solidAngleTable,
    ),

    'temperature' : UnitTypeInfo(
        [ 'temperature' ],
        'kelvin',
        temperatureTable,
    ),

    'time' : UnitTypeInfo(
        [ 'time' ],
        'second',
        timeTable,
    ),

    'velocity' : UnitTypeInfo(
        [ 'length/time' ],
        'meter/second',
        velocityTable,
    ),

    'volume' : UnitTypeInfo(
        [ 'length^3' ],
        'liter',
        volumeTable,
    ),
}


#//******************************************************************************
#//
#//  unitOperators
#//
#//  unit name : unitType, representation, plural, abbrev, aliases, categories
#//
#//******************************************************************************

unitOperators = {
    # acceleration

    'galileo' :
        UnitInfo( 'acceleration', 'galileo', 'galileos', '', [ ], [ 'CGS' ] ),

    'meter/second^2' :
        UnitInfo( 'acceleration', 'meter/second^2', 'meters/second^2', 'm/s^2', [ ], [ 'SI' ] ),

    'standard_gravity' :
        UnitInfo( 'acceleration', 'standard_gravity', 'standard_gravities', 'G', [ ], [ 'natural' ] ),

    # angle

    'arcminute' :
        UnitInfo( 'angle', 'arcminute', 'arcminutes', 'arcmin', [ 'arcmins' ], [ 'mathematics' ] ),

    'arcsecond' :
        UnitInfo( 'angle', 'arcsecond', 'arcseconds', 'arcsec', [ 'arcsecs' ], [ 'mathematics' ] ),

    'centrad' :
        UnitInfo( 'angle', 'centrad', 'centrads', '', [ ], [ 'mathematics', 'science' ] ),

    'degree' :
        UnitInfo( 'angle', 'degree', 'degrees', 'deg', [ ], [ 'mathematics' ] ),

    'grad' :
        UnitInfo( 'angle', 'grad', 'grads', '', [ 'gon', 'gons' ], [ 'mathematics' ] ),

    'milliarcsecond' :
        UnitInfo( 'angle', 'milliarcsecond', 'milliarcseconds', 'mas', [ 'milliarcsecs' ], [ 'astronomy' ] ),

    'octant' :
        UnitInfo( 'angle', 'octant', 'octants', '', [ ], [ 'mathematics' ] ),

    'pointangle' :
        UnitInfo( 'angle', 'pointangle', 'pointangles', '', [ ], [ 'navigation' ] ),

    'quadrant' :
        UnitInfo( 'angle', 'quadrant', 'quadrants', '', [ ], [ 'mathematics' ] ),

    'quintant' :
        UnitInfo( 'angle', 'quintant', 'quintants', '', [ ], [ 'mathematics' ] ),

    'radian' :
        UnitInfo( 'angle', 'radian', 'radians', 'rad', [ ], [ 'mathematics', 'SI' ] ),

    'sextant' :
        UnitInfo( 'angle', 'sextant', 'sextants', '', [ 'flat', 'flats' ], [ 'mathematics' ] ),

    # area

    'acre' :
        UnitInfo( 'area', 'acre', 'acres', 'ac', [ ], [ 'imperial' ] ),

    'are' :
        UnitInfo( 'area', 'are', 'ares', 'a', [ ], [ 'SI' ] ),

    'barn' :
        UnitInfo( 'area', 'barn', 'barns', '', [ ], [ 'science' ] ),

    'bovate' :
        UnitInfo( 'area', 'bovate', 'bovates', '', [ ], [ 'imperial' ] ),

    'carucate' :
        UnitInfo( 'area', 'carucate', 'carucates', '', [ ], [ 'imperial' ] ),

    'homestead':
        UnitInfo( 'area', 'homestead', 'homesteads', '', [ ], [ 'US' ] ),

    'imperial_square' :
        UnitInfo( 'area', 'imperial_sqaure', 'imperial_squares', '', [ ], [ 'imperial' ] ),

    'morgen' :
        UnitInfo( 'area', 'morgen', 'morgens', '', [ ], [ 'obsolete' ] ),

    'nanoacre' :
        UnitInfo( 'area', 'nanoacre', 'nanoacres', 'nac', [ ], [ 'computing' ] ),

    'outhouse' :
        UnitInfo( 'area', 'outhouse', 'outhouse', '', [ ], [ 'science', 'humorous' ] ),

    'planck_area' :
        UnitInfo( 'area', 'planck_area', 'planck_areas', '', [ ], [ 'natural', 'science' ] ),

    'rood' :
        UnitInfo( 'area', 'rood', 'roods', '', [ 'farthingdale' ], [ 'imperial' ] ),

    'section':
        UnitInfo( 'area', 'section', 'sections', '', [ ], [ 'US' ] ),

    'shed' :
        UnitInfo( 'area', 'shed', 'sheds', '', [ ], [ 'science' ] ),

    'square_foot' :
        UnitInfo( 'area', 'foot^2', 'square_feet', 'sqft', [ 'ft^2', 'feet^2' ], [ 'imperial' ] ),

    'square_meter' :
        UnitInfo( 'area', 'meter^2', 'square_meters', 'm^2', [ 'meters^2' ], [ 'SI' ] ),

    'square_yard' :
        UnitInfo( 'area', 'yard^2', 'square_yards', 'sqyd', [ 'yd^2', 'yards^2' ], [ 'imperial' ] ),

    'township':
        UnitInfo( 'area', 'township', 'townships', '', [ ], [ 'US' ] ),

    'virgate':
        UnitInfo( 'area', 'virgate', 'virgates', '', [ ], [ 'imperial' ] ),

    # capacitance

    'abfarad' :
        UnitInfo( 'capacitance', 'abfarad', 'abfarads', 'abF', [ ], [ 'CGS' ] ),

    'coulomb/volt' :
        UnitInfo( 'capacitance', 'coulomb/volt', 'coulombs/volt', 'C/V', [ 'coulomb/volts', 'coulombs/volts', 'C/volts', 'C/volt', 'coulomb/V', 'coulombs/V' ], [ 'SI' ] ),

    'farad' :
        UnitInfo( 'capacitance', 'farad', 'farads', 'F', [ ], [ 'SI' ] ),

    'jar' :
        UnitInfo( 'capacitance', 'jar', 'jars', '', [ ], [ 'obsolete' ] ),

    'statfarad' :
        UnitInfo( 'capacitance', 'statfarad', 'statfarads', 'statF', [ ], [ 'CGS' ] ),

    # charge

    'abcoulomb' :
        UnitInfo( 'charge', 'abcoulomb', 'abcoulombs', 'abC', [ ], [ 'CGS' ] ),

    'ampere-second' :
        UnitInfo( 'charge', 'ampere*second', 'ampere*second', 'A/s', [ 'ampere/sec', 'ampere/s', 'amp/sec', 'amp/s', 'amps/sec', 'amps/s' ], [ 'SI' ] ),

    'coulomb' :
        UnitInfo( 'charge', 'coulomb', 'coulombs', 'C', [ ], [ 'SI' ] ),

    'farad-volt' :
        UnitInfo( 'charge', 'farad*volt', 'farad-volts', 'F*V', [ 'F/volt', 'F/volts', 'farad/volts', 'farads/volts', 'farad/V', 'farads/V' ], [ 'SI' ] ),

    'franklin' :
        UnitInfo( 'charge', 'franklin', 'franklins', 'Fr', [ ], [ 'CGS' ] ),

    'electron_charge' :
        UnitInfo( 'charge', 'electron_charge', 'electron_charges', '', [ 'elementary_charge', 'proton_charge' ], [ 'natural' ] ),

    'faraday' :
        UnitInfo( 'charge', 'faraday', 'faradays', 'Fd', [ ], [ 'natural' ] ),   # electron_charge * Avogradro's number!

    'planck_charge' :
        UnitInfo( 'charge', 'planck_charge', 'planck_charges', '', [ ], [ 'natural', 'science' ] ),

    'statcoulomb' :
        UnitInfo( 'charge', 'statcoulomb', 'statcoulombs', 'statC', [ 'esu_charge' ], [ 'CGS' ] ),

    # constant - Constant is a special type that is immediately converted to a numerical value when used.
    #            It's not intended to be used as a unit, per se.  Also, these units are in order of their
    #            value instead of alphabetical order like all the others

    'alpha' :
        UnitInfo( 'constant', 'alpha', 'alpha', '', [ 'fine_structure_constant' ], [ 'constant' ] ),

    'decillionth' :
        UnitInfo( 'constant', 'decillionth', 'decillionths', '', [ ], [ 'constant' ] ),

    'nonillionth' :
        UnitInfo( 'constant', 'nonillionth', 'nonillionths', '', [ ], [ 'constant' ] ),

    'octillionth' :
        UnitInfo( 'constant', 'octillionth', 'octillionths', '', [ ], [ 'constant' ] ),

    # 'y' can't be used here since it's used for 'year'
    'septillionth' :
        UnitInfo( 'constant', 'septillionth', 'septillionths', '', [ 'yocto' ], [ 'constant' ] ),

    'sextillionth' :
        UnitInfo( 'constant', 'sextillionth', 'sextillionths', 'z', [ 'zepto' ], [ 'constant' ] ),

    # 'a' can't be used here since it's used for 'are'
    'quintillionth' :
        UnitInfo( 'constant', 'quintillionth', 'quintillionths', '', [ 'atto' ], [ 'constant' ] ),

    'quadrillionth' :
        UnitInfo( 'constant', 'quadrillionth', 'quadrillionths', 'f', [ 'femto' ], [ 'constant' ] ),

    'trillionth' :
        UnitInfo( 'constant', 'trillionth', 'trillionths', 'p', [ 'pico' ], [ 'constant' ] ),

    'billionth' :
        UnitInfo( 'constant', 'billionth', 'billionths', 'n', [ 'nano' ], [ 'constant' ] ),

    'millionth' :
        UnitInfo( 'constant', 'millionth', 'millionths', 'u', [ 'micro' ], [ 'constant' ] ),

    # 'm' can't be used here since it's used for 'meter'
    'thousandth' :
        UnitInfo( 'constant', 'thousandth', 'thousandths', '', [ 'milli' ], [ 'constant' ] ),

    'alpha' :
        UnitInfo( 'constant', 'alpha', 'alpha', '', [ 'fine_structure_constant' ], [ 'constant' ] ),

    'percent' :
        UnitInfo( 'constant', 'percent', 'percent', '%', [ 'hundredth', 'centi' ], [ 'constant' ] ),

    'tenth' :
        UnitInfo( 'constant', 'tenth', 'tenths', '', [ 'deci', 'tithe' ], [ 'constant' ] ),

    'quarter' :
        UnitInfo( 'constant', 'quarter', 'quarters', '', [ 'fourth' ], [ 'constant' ] ),

    'third' :
        UnitInfo( 'constant', 'third', 'thirds', '', [ ], [ 'constant' ] ),

    'half' :
        UnitInfo( 'constant', 'half', 'halves', '', [ ], [ 'constant' ] ),

    'unity' :
        UnitInfo( 'constant', 'x unity', 'x unity', '', [ ], [ 'constant' ] ),

    'ten' :
        UnitInfo( 'constant', 'ten', 'tens', '', [ 'deca', 'deka', 'dicker' ], [ 'constant' ] ),

    'dozen' :
        UnitInfo( 'constant', 'dozen', 'dozen', '', [ ], [ 'constant' ] ),

    'score' :
        UnitInfo( 'constant', 'score', 'score', '', [ ], [ 'constant' ] ),

    'flock' :
        UnitInfo( 'constant', 'flock', 'flocks', '', [ 'timer' ], [ 'constant' ] ),

    'shock' :
        UnitInfo( 'constant', 'shock', 'shocks', '', [ ], [ 'constant' ] ),

    'hundred' :
        UnitInfo( 'constant', 'hundred', 'hundred', '', [ 'hecto', 'toncount' ], [ 'constant' ] ),

    'long_hundred' :
        UnitInfo( 'constant', 'long_hundred', 'long_hundreds', '', [ ], [ 'constant' ] ),

    'gross' :
        UnitInfo( 'constant', 'gross', 'gross', '', [ ], [ 'constant' ] ),

    'thousand' :
        UnitInfo( 'constant', 'thousand', 'thousand', 'k', [ 'kilo' ], [ 'constant' ] ),

    'great_gross' :
        UnitInfo( 'constant', 'great_gross', 'great_gross', '', [ ], [ 'constant' ] ),

    'million' :
        UnitInfo( 'constant', 'million', 'million', 'M', [ 'mega' ], [ 'constant' ] ),

    # 'G' can't be used here since it's used for 'standard gravity'
    'billion' :
        UnitInfo( 'constant', 'billion', 'billion', '', [ 'giga' ], [ 'constant' ] ),

    # 'T' can't be used here since it's used for 'tesla'
    'trillion' :
        UnitInfo( 'constant', 'trillion', 'trillion', '', [ 'tera' ], [ 'constant' ] ),

    'quadrillion' :
        UnitInfo( 'constant', 'quadrillion', 'quadrillion', 'P', [ 'peta' ], [ 'constant' ] ),

    'quintillion' :
        UnitInfo( 'constant', 'quintillion', 'quintillion', 'E', [ 'exa' ], [ 'constant' ] ),

    'sextillion' :
        UnitInfo( 'constant', 'sextillion', 'sextillion', 'Z', [ 'zetta' ], [ 'constant' ] ),

    'septillion' :
        UnitInfo( 'constant', 'septillion', 'septillion', 'Y', [ 'yotta' ], [ 'constant' ] ),

    'octillion' :
        UnitInfo( 'constant', 'octillion', 'octillion', '', [ ], [ 'constant' ] ),

    'nonillion' :
        UnitInfo( 'constant', 'nonillion', 'nonillion', '', [ ], [ 'constant' ] ),

    'decillion' :
        UnitInfo( 'constant', 'decillion', 'decillion', '', [ ], [ 'constant' ] ),

    'undecillion' :
        UnitInfo( 'constant', 'undecillion', 'undecillion', '', [ ], [ 'constant' ] ),

    'duodecillion' :
        UnitInfo( 'constant', 'duodecillion', 'duodecillion', '', [ ], [ 'constant' ] ),

    'tredecillion' :
        UnitInfo( 'constant', 'tredecillion', 'tredecillion', '', [ ], [ 'constant' ] ),

    'quattuordecillion' :
        UnitInfo( 'constant', 'quattuordecillion', 'quattuordecillion', '', [ ], [ 'constant' ] ),

    'quindecillion' :
        UnitInfo( 'constant', 'quindecillion', 'quindecillion', '', [ 'quinquadecillion' ], [ 'constant' ] ),

    'sexdecillion' :
        UnitInfo( 'constant', 'sexdecillion', 'sexdecillion', '', [ ], [ 'constant' ] ),

    'septendecillion' :
        UnitInfo( 'constant', 'septemdecillion', 'septemdecillion', '', [ ], [ 'constant' ] ),

    'octodecillion' :
        UnitInfo( 'constant', 'octodecillion', 'octodecillion', '', [ ], [ 'constant' ] ),

    'novemdecillion' :
        UnitInfo( 'constant', 'novemdecillion', 'novemdecillion', '', [ 'novendecillion' ], [ 'constant' ] ),

    'vigintillion' :
        UnitInfo( 'constant', 'vigintillion', 'vigintillion', '', [ ], [ 'constant' ] ),

    'googol' :
        UnitInfo( 'constant', 'googol', 'googols', '', [ ], [ 'constant' ] ),

    'centillion' :
        UnitInfo( 'constant', 'centillion', 'centillion', '', [ ], [ 'constant' ] ),

    # current

    'abampere' :
        UnitInfo( 'current', 'abampere', 'abamperes', 'abA', [ 'abamp', 'abamps', 'biot', 'biots' ], [ 'CGS' ] ),

    'ampere' :
        UnitInfo( 'current', 'ampere', 'amperes', 'A', [ 'amp', 'amps', 'galvat', 'galvats' ], [ 'SI' ] ),

    'coulomb/second' :
        UnitInfo( 'current', 'coulomb/second', 'coulombs/second', 'C/s', [ 'C/sec', 'coulomb/sec', 'coulombs/sec', 'coulomb/s', 'coulombs/s' ], [ 'SI' ] ),

    'statampere' :
        UnitInfo( 'current', 'statampere', 'statamperes', 'statA', [ 'statamp', 'statamps', 'esu_current' ], [ 'CGS' ] ),

    # data_rate

    'bit/second' :
        UnitInfo( 'data_rate', 'bit/second', 'bits/second', 'b/s', [ 'bit/s', 'bits/s', 'bit/sec', 'bits/sec' ], [ 'computing' ] ),

    'byte/second' :
        UnitInfo( 'data_rate', 'byte/second', 'bytes/second', 'B/s', [ 'byte/s', 'bytes/s' 'byte/sec', 'bytes/sec' ], [ 'computing' ] ),

    # density

    'gram/meter^3' :
        UnitInfo( 'density', 'gram/meter^3', 'grams/meter^3', 'g/m^3', [ '' ], [ 'SI' ] ),

    'density_of_water' :
        UnitInfo( 'density', 'x density_of_water', 'x density_of_water', '', [ 'water' ], [ 'natural' ] ),

    # dynamic_viscosity

    'newton-second/meter^2' :
        UnitInfo( 'dynamic_viscosity', 'newton*second/meter^2', 'newton*second/meter^2', 'Ns/m^2', [ ], [ 'CGS' ] ),

    'pascal-second' :
        UnitInfo( 'dynamic_viscosity', 'pascal*second', 'pascal*second', 'Pas', [ ], [ 'SI' ] ),

    'poise' :
        UnitInfo( 'dynamic_viscosity', 'pascal*second', 'pascal*second', '', [ ], [ 'CGS' ] ),

    # electric_potential

    'abvolt' :
        UnitInfo( 'electric_potential', 'abvolt', 'abvolts', 'abV', [ ], [ 'CGS' ] ),

    'coulomb/farad' :
        UnitInfo( 'electric_potential', 'coulomb/farad', 'coulombs/farad', 'C/F', [ 'coulomb/F', 'coulombs/F', 'C/farad', 'C/farads', 'coulombs/farads' ], [ 'SI' ] ),

    'volt' :
        UnitInfo( 'electric_potential', 'volt', 'volts', 'V', [ ], [ 'SI' ] ),

    'watt/ampere' :
        UnitInfo( 'electric_potential', 'watt/ampere', 'watts/ampere', 'W/A', [ 'watt/amp', 'watt/amps', 'watt/A', 'watts/amp', 'watts/amps', 'watts/A', 'W/amp', 'W/amps', 'W/ampere', 'W/amperes' ], [ 'SI' ] ),

    'statvolt' :
        UnitInfo( 'electric_potential', 'statvolt', 'statvolts', 'statV', [ 'esu_potential' ], [ 'CGS' ] ),

    # electrical_conductance

    'abmho' :
        UnitInfo( 'electrical_conductance', 'abmho', 'abmhos', '', [ 'absiemens' ], [ 'CGS' ] ),

    'ampere/volt' :
        UnitInfo( 'electrical_conductance', 'ampere/volt', 'amperes/volt', 'A/V', [ 'amp/V', 'amps/V', 'ampere/V', 'amperes/V', 'A/volt', 'amp/volt', 'amps/volt', 'A/volts', 'amp/volts', 'amps/volts', 'amperes/volts', ], [ 'SI' ] ),

    'second^3-ampere^2/kilogram-meter^2':
        UnitInfo( 'electrical_conductance', 'kilogram*meter^2/second^3*ampere^2', 'kilogram*meter^2/second^3*ampere^2', 'kg*m^2/s^3*A^2', [ ], [ 'SI' ] ),

    'siemens' :
        UnitInfo( 'electrical_conductance', 'siemens', 'siemens', 'S', [ 'mho' ], [ 'SI' ] ),

    'statmho' :
        UnitInfo( 'electrical_conductance', 'statmho', 'statmhos', '', [ ], [ 'CGS' ] ),

    'statsiemens' :
        UnitInfo( 'electrical_conductance', 'statsiemens', 'statsiemens', 'statS', [ '' ], [ 'SI' ] ),

    # electrical_resistance

    '1/siemens' :
        UnitInfo( 'electrical_resistance', '1/siemens', '1/siemens', '1/S', [ '1/mho' ], [ 'SI' ] ),

    'abohm' :
        UnitInfo( 'electrical_resistance', 'abohm', 'abohms', 'o', [ ], [ 'CGS' ] ),

    'german_mile' :
        UnitInfo( 'electrical_resistance', 'german_mile', 'german_mile', '', [ ], [ 'obsolete' ] ),

    'impedance_of_free_space' :
        UnitInfo( 'electrical_resistance', 'impedance_of_free_space', 'x impedance_of_free_space', 'Z0', [ ], [ 'natural' ] ),

    'jacobi' :
        UnitInfo( 'electrical_resistance', 'jacobi', 'jacobis', '', [ ], [ 'obsolete' ] ),

    'joule-second/coulomb^2' :
        UnitInfo( 'electrical_resistance', 'joule*second/coulomb^2', 'joule*second/coulomb^2', 'J*s/C^2', [ ], [ 'SI' ] ),

    'joule/second-ampere^2' :
        UnitInfo( 'electrical_resistance', 'joule/second*ampere^2', 'joule/second*ampere^2', 'J/s*A^2', [ ], [ 'SI' ] ),

    'kilogram-meter^2/second^3-ampere^2' :
        UnitInfo( 'electrical_resistance', 'kilogram*meter^2/second^3*ampere^2', 'kilogram*meter^2/second^3*ampere^2', 'kg*m^2/s^3*A^2', [ ], [ 'SI' ] ),

    'matthiessen' :
        UnitInfo( 'electrical_resistance', 'matthiessen', 'matthiessens', '', [ ], [ 'obsolete' ] ),   # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C

    'meter^2-kilogram/second-coulomb^2' :
        UnitInfo( 'electrical_resistance', 'meter^2*kilogram/second*coulomb^2', 'meter^2*kilogram/second*coulomb^2', 'm^2*kg/s*C^2', [ ], [ 'SI' ] ),

    'ohm' :
        UnitInfo( 'electrical_resistance', 'ohm', 'ohms', 'O', [ ], [ 'SI' ] ),

    'second/farad' :
        UnitInfo( 'electrical_resistance', 'second/farad', 'second/farad', 's/F', [ 's/farad', 's/farads', 'sec/farad', 'sec/farads', 'sec/F', 'second/F', 'seconds/F' ], [ 'SI' ] ),

    'statohm' :
        UnitInfo( 'electrical_resistance', 'statohm', 'statohms', 'statO', [ ], [ 'SI' ] ),

    'varley' :
        UnitInfo( 'electrical_resistance', 'varley', 'varleys', '', [ ], [ 'obsolete' ] ),  # based on one mile of 1/16 inch diameter pure annealed copper wire at 15.5 degrees C

    'von_klitzing_constant' :
        UnitInfo( 'electrical_resistance', 'von_klitzing_constant', 'x_von_klitzing_constant', '', [ 'von_klitzing' ], [ 'natural' ] ),

    'volt/ampere' :
        UnitInfo( 'electrical_resistance', 'volt/ampere', 'volts/ampere', 'V/A', [ 'volt/amp', 'volt/amps', 'volt/A', 'volts/amp', 'volts/amps', 'volts/A', 'V/amp', 'V/amps', 'V/ampere', 'V/amperes' ], [ 'SI' ] ),

    'watt/ampere^2' :
        UnitInfo( 'electrical_resistance', 'watt/ampere^2', 'watts/ampere^2', 'W/A^2', [ 'watt/amperes^2', 'watts/amperes^2', 'W/ampere^2', 'W/amperes^2' ], [ 'SI' ] ),

    # energy

    'aa_battery' :
        UnitInfo( 'energy', 'AA_battery', 'AA_batteries', '', [ 'aa-battery', 'aa-batteries', 'AA-battery', 'AA-batteries' ], [ 'informal' ] ),

    'btu' :
        UnitInfo( 'energy', 'BTU', 'BTUs', '', [ 'btu', 'btus' ], [ 'England', 'US' ] ),

    'calorie' :
        UnitInfo( 'energy', 'calorie', 'calories', 'cal', [ ], [ 'CGS' ] ),

    'electronvolt' :
        UnitInfo( 'energy', 'electronvolt', 'electronvolts', 'eV', [ 'electron-volt', 'electron-volts' ], [ 'science' ] ),

    'erg' :
        UnitInfo( 'energy', 'erg', 'ergs', '', [ ], [ 'CGS' ] ),

    'gallon_of_ethanol' :
        UnitInfo( 'energy', 'gallon_of_ethanol', 'gallons_of_ethanol', '', [ ], [ 'informal' ] ),

    'gallon_of_gasoline' :
        UnitInfo( 'energy', 'gallon_of_gasoline', 'gallons_of_gasoline', '', [ 'gallon_of_gas', 'gallons_of_gas' ], [ 'informal' ] ),

    'gram-equivalent' :
        UnitInfo( 'energy', 'gram-equivalent', 'grams-equivalent', 'gE', [ 'gram-energy', 'grams-energy', 'gramme-equivalent', 'grammes-equivalent',  'gramme-energy', 'grammes-energy' ], [ 'natural' ] ),

    'hartree' :
        UnitInfo( 'energy', 'hartree', 'hartrees', 'Eh', [ ], [ 'science' ] ),

    'horsepower-second' :
        UnitInfo( 'energy', 'horsepower*second', 'horsepower-seconds', 'hps', [ ], [ 'US' ] ),

    'joule' :
        UnitInfo( 'energy', 'joule', 'joules', 'J', [ ], [ 'SI' ] ),

    'kilogram-meter^2/second^2' :
        UnitInfo( 'energy', 'kilogram*meter^2/second^2', 'kilogram*meter^2/second^2', 'kg*m^2/s^2', [ ], [ 'SI' ] ),

    'newton-meter' :
        UnitInfo( 'energy', 'newton*meter', 'newton-meters', 'N*m', [ ], [ 'SI' ] ),

    'planck_energy' :
        UnitInfo( 'energy', 'planck_energy', 'planck_energy', 'EP', [ ], [ 'natural', 'science' ] ),

    'rydberg' :
        UnitInfo( 'energy', 'rydberg', 'rydbergs', 'Ry', [ ], [ 'science' ] ),

    'ton_of_TNT' :
        UnitInfo( 'energy', 'ton_of_TNT', 'tons_of_TNT', 'tTNT', [ ], [ 'informal' ] ),

    #'volt-ampere-second' :
    #    UnitInfo( 'energy', 'ampere*second*volt', 'ampere*second*volt', 'VAs', [ ], [ 'SI' ] ),

    'watt-second' :
        UnitInfo( 'energy', 'watt*second', 'watt-seconds', 'Ws', [ ], [ 'SI' ] ),

    # force

    'dyne' :
        UnitInfo( 'force', 'dyne', 'dynes', 'dyn', [ ], [ 'CGS' ] ),

    'gram-force' :
        UnitInfo( 'force', 'gram-force', 'grams-force', 'g-m', [ ], [ 'CGS' ] ),

    'joule/meter' :
        UnitInfo( 'force', 'joule/meter', 'joule/meter', 'J/m', [ ], [ 'SI' ] ),

    'newton' :
        UnitInfo( 'force', 'newton', 'newtons', 'N', [ ], [ 'SI' ] ),

    'planck_force' :
        UnitInfo( 'force', 'planck_force', 'planck_force', '', [ ], [ 'natural', 'science' ] ),

    'pond' :
        UnitInfo( 'force', 'pond', 'ponds', '', [ ], [ 'metric' ] ),

    'pound-foot/second^2' :
        UnitInfo( 'force', 'pound*foot/second^2', 'pound*foot/second^2', 'lb*ft/sec^2', [ ], [ 'FPS' ] ),

    'poundal' :
        UnitInfo( 'force', 'poundal', 'poundals', 'pdl', [ ], [ 'England' ] ),

    'sthene' :
        UnitInfo( 'force', 'sthene', 'sthenes', 'sn', [ 'funal' ], [ 'MTS' ] ),

    # frequency

    'hertz' :
        UnitInfo( 'frequency', 'hertz', 'hertz', 'Hz', [ ], [ 'SI' ] ),

    'every_minute' :
        UnitInfo( 'frequency', 'x every_minute', 'x every minute', '', [ ], [ ] ),

    'hourly' :
        UnitInfo( 'frequency', 'x hourly', 'x hourly', '', [ ], [ ] ),

    'daily' :
        UnitInfo( 'frequency', 'x daily', 'x daily', '', [ ], [ ] ),

    'weekly' :
        UnitInfo( 'frequency', 'x weekly', 'x weekly', '', [ ], [ ] ),

    'monthly' :
        UnitInfo( 'frequency', 'x monthly', 'x monthly', '', [ ], [ ] ),

    'yearly' :
        UnitInfo( 'frequency', 'x yearly', 'x yearly', '', [ ], [ ] ),

    # illuminance

    'footcandle' :
        UnitInfo( 'illuminance', 'footcandle', 'footcandles', 'fc', [ ], [ 'FPS' ] ),

    'lux' :
        UnitInfo( 'illuminance', 'lux', 'lux', 'lx', [ ], [ 'SI' ] ),

    'lumen/meter^2' :
        UnitInfo( 'illuminance', 'lumen/meter^2', 'lumens/meter^2', 'lm/m^2', [ 'lm/square_meter', 'lumen/square_meter', 'lumens/square_meter', 'lumen/m^2', 'lumens/m^2' ], [ 'SI' ] ),

    'lumen/foot^2' :
        UnitInfo( 'illuminance', 'lumen/foot^2', 'lumens/foot^2', 'lm/ft^2', [ 'lm/square_foot', 'lumen/square_foot', 'lumens/square_foot', 'lumen/ft^2', 'lumens/ft^2' ], [ 'FPS' ] ),

    'nox' :
        UnitInfo( 'illuminance', 'nox', 'nox', 'nx', [ ], [ 'obsolete' ] ),

    'phot' :
        UnitInfo( 'illuminance', 'phot', 'phots', 'ph', [ ], [ 'CGS' ] ),

    # inductance

    'abhenry' :
        UnitInfo( 'inductance', 'abhenry', 'abhenries', 'abH', [ ], [ 'CGS' ] ),

    'henry' :
        UnitInfo( 'inductance', 'henry', 'henries', 'H', [ ], [ 'SI' ] ),

    'weber/ampere' :
        UnitInfo( 'inductance', 'weber/ampere', 'webers/ampere', 'Wb/A', [ 'Wb/ampere', 'Wb/ampere', 'weber/A', 'webers/A', 'Wb/amp', 'weber/amp', 'webers/amp' ], [ 'SI' ] ),

    'stathenry' :
        UnitInfo( 'inductance', 'stathenry', 'stathenries', 'statH', [ ], [ 'CGS' ] ),

    # information_entropy

    'ban' :
        UnitInfo( 'information_entropy', 'ban', 'bans', '', [ 'hartley', 'hartleys', 'dit', 'dits' ], [ 'IEC' ] ),

    'bit' :
        UnitInfo( 'information_entropy', 'bit', 'bits', 'b', [ 'shannon', 'shannons' ], [ 'computing' ] ),

    'boltzmann_constant' :
        UnitInfo( 'information_entropy', 'boltzmann_constant', 'x boltzmann_constant', '', [ 'boltzmann' ], [ 'natural' ] ),

    'byte' :
        UnitInfo( 'information_entropy', 'byte', 'bytes', 'B', [ 'octet', 'octets' ], [ 'computing' ] ),

    'btupf' :
        UnitInfo( 'information_entropy', 'btupf', 'btupf', '', [ ], [ 'England' ] ),

    'clausius' :
        UnitInfo( 'information_entropy', 'clausius', 'clausius', '', [ ], [ 'CGS' ] ),

    'dword' :
        UnitInfo( 'information_entropy', 'dword', 'dwords', '', [ 'double_word', 'double_words', 'long_integer', 'long_integers' ], [ 'computing' ] ),

    'joule/kelvin' :
        UnitInfo( 'information_entropy', 'joule/kelvin', 'joules/kelvin', 'J/K', [ 'joule/K', 'joules/K' ], [ 'SI' ] ),

    'library_of_congress' :
        UnitInfo( 'information_entropy', 'library_of_congress', 'libraries_of_congress', 'LoC', [ 'congress', 'congresses' ], [ 'computing' ] ),

    'nibble' :
        UnitInfo( 'information_entropy', 'nibble', 'nibbles', '', [ 'nybble', 'nybbles' ], [ 'computing' ] ),

    'nat' :
        UnitInfo( 'information_entropy', 'nat', 'nats', '', [ 'nip', 'nips', 'nepit', 'nepits' ], [ 'IEC' ] ),

    'nyp' :
        UnitInfo( 'information_entropy', 'nyp', 'nyps', '', [ ], [ 'computing' ] ),   # suggested by Donald Knuth

    'oword' :
        UnitInfo( 'information_entropy', 'oword', 'owords', '', [ 'octaword', 'octawords' ], [ 'computing' ] ),

    'qword' :
        UnitInfo( 'information_entropy', 'qword', 'qwords', '', [ 'quad_word', 'quad_words', 'longlong_integer', 'longlong_integers' ], [ 'computing' ] ),

    'trit' :
        UnitInfo( 'information_entropy', 'trit', 'trits', '', [ ], [ 'computing' ] ),

    'tryte' :
        UnitInfo( 'information_entropy', 'tryte', 'trytes', '', [ ], [ 'computing' ] ),

    'word' :
        UnitInfo( 'information_entropy', 'word', 'words', '', [ 'short_integer', 'short_integers', 'wyde' ], [ 'computing' ] ),  # 'wyde' suggested by Knuth

    # length

    'aln' :
        UnitInfo( 'length', 'aln', 'alns', '', [ ], [ 'obsolete' ] ),

    'arpent' :
        UnitInfo( 'length', 'arpent', 'arpents', '', [ ], [ 'obsolete', 'France' ] ),

    'angstrom' :
        UnitInfo( 'length', 'angstrom', 'angstroms', 'A', [ 'angstroem' ], [ 'science' ] ),

    'astronomical_unit' :
        UnitInfo( 'length', 'astronomical_unit', 'astronomical_units', 'au', [ ], [ 'science' ] ),

    'barleycorn' :
        UnitInfo( 'length', 'barleycorn', 'barleycorns', '', [ ], [ 'imperial' ] ),

    'bohr_radius' :
        UnitInfo( 'length', 'bohr_radius', 'bohr_radii', 'a0', [ 'bohr' ], [ 'science' ] ),

    'bolt' :
        UnitInfo( 'length', 'bolt', 'bolts', '', [ ], [ 'obsolete' ] ),

    'caliber' :
        UnitInfo( 'length', 'caliber', 'caliber', '', [ 'calibre' ], [ 'US' ] ),

    'chain' :
        UnitInfo( 'length', 'chain', 'chains', '', [ ], [ 'imperial' ] ),

    'cubit' :
        UnitInfo( 'length', 'cubit', 'cubits', '', [ ], [ 'imperial' ] ),

    'earth_radius' :
        UnitInfo( 'length', 'earth_radius', 'earth_radii', 'Rgeo', [ ], [ 'natural' ] ),

    'ell' :
        UnitInfo( 'length', 'ell', 'ells', '', [ ], [ 'imperial' ] ),

    'famn' :
        UnitInfo( 'length', 'famn', 'famns', '', [ ], [ 'obsolete' ] ),

    'farshimmelt_potrzebie' :
        UnitInfo( 'length', 'farshimmelt_potrzebie', 'farshimmelt potrzebies', 'fpz', [ 'far-potrzebie' ], [ 'Potrzebie', 'humorous' ] ),

    'fathom' :
        UnitInfo( 'length', 'fathom', 'fathoms', 'fath', [ ], [ 'imperial' ] ),

    'finger' :
        UnitInfo( 'length', 'finger', 'fingers', '', [ ], [ 'imperial' ] ),

    'fingerbreadth' :
        UnitInfo( 'length', 'fingerbreadth', 'fingerbreadths', '', [ 'fingersbreadth' ], [ 'obsolete' ] ),

    'foot' :
        UnitInfo( 'length', 'foot', 'feet', 'ft', [ ], [ 'traditional', 'FPS' ] ),

    'furlong' :
        UnitInfo( 'length', 'furlong', 'furlongs', '', [ ], [ 'imperial' ] ),

    'furshlugginer_potrzebie' :
        UnitInfo( 'length', 'furshlugginer_potrzebie', 'furshlugginer potrzebies', 'Fpz', [ 'Fur-potrzebie' ], [ 'Potrzebie', 'humorous' ] ),

    'greek_cubit' :
        UnitInfo( 'length', 'greek_cubit', 'greek_cubits', '', [ ], [ 'obsolete', 'Greece' ] ),

    'gutenberg' :
        UnitInfo( 'length', 'gutenberg', 'gutenbergs', '', [ ], [ 'typography' ] ),

    'hand' :
        UnitInfo( 'length', 'hand', 'hands', '', [ ], [ 'imperial' ] ),

    'handbreadth' :
        UnitInfo( 'length', 'handbreadth', 'handbreadths', '', [ 'handsbreadth' ], [ 'obsolete' ] ),

    'inch' :
        UnitInfo( 'length', 'inch', 'inches', 'in', [ ], [ 'imperial' ] ),

    'jupiter_radius' :
        UnitInfo( 'length', 'jupiter_radius', 'jupiter_radii', 'Rjov', [ ], [ 'natural' ] ),

    'ken' :
        UnitInfo( 'length', 'ken', 'kens', '', [ ], [ 'obsolete' ] ),

    'kyu' :
        UnitInfo( 'length', 'kyu', 'kyus', '', [ 'Q' ], [ 'typography', 'computing' ] ),

    'league' :
        UnitInfo( 'length', 'league', 'leagues', '', [ ], [ 'imperial' ] ),

    'light-second' :
        UnitInfo( 'length', 'light*second', 'light-seconds', '', [ 'light-second' ], [ 'science' ] ),

    'light-year' :
        UnitInfo( 'length', 'light-year', 'light-years', 'ly', [ 'a1' ], [ 'science' ] ),

    'link' :
        UnitInfo( 'length', 'link', 'links', '', [ ], [ 'informal' ] ),

    'long_cubit' :
        UnitInfo( 'length', 'long_cubit', 'long_cubits', '', [ ], [ 'obsolete' ] ),

    'long_reed' :
        UnitInfo( 'length', 'long_reed', 'long_reeds', '', [ ], [ 'obsolete' ] ),

    'marathon' :
        UnitInfo( 'length', 'marathon', 'marathons', '', [ ], [ 'informal' ] ),

    'meter' :
        UnitInfo( 'length', 'meter', 'meters', 'm', [ ], [ 'SI' ] ),

    'micron' :
        UnitInfo( 'length', 'micron', 'microns', '', [ ], [ 'science' ] ),

    'mil' :
        UnitInfo( 'length', 'mil', 'mils', '', [ 'thou' ], [ 'US' ] ),

    'mile' :
        UnitInfo( 'length', 'mile', 'miles', 'mi', [ ], [ 'imperial' ] ),

    'nail' :
        UnitInfo( 'length', 'nail', 'nails', '', [ ], [ 'imperial' ] ),

    'nautical_mile' :
        UnitInfo( 'length', 'nautical_mile', 'nautical_miles', '', [ ], [ 'nautical' ] ),

    'parsec' :
        UnitInfo( 'length', 'parsec', 'parsecs', 'pc', [ ], [ 'science' ] ),

    'perch' :
        UnitInfo( 'length', 'perch', 'perches', '', [ 'pole', 'poles' ], [ 'imperial' ] ),

    'pica' :
        UnitInfo( 'length', 'pica', 'picas', '', [ 'cicero' ], [ 'typography' ] ),

    'planck_length' :
        UnitInfo( 'length', 'planck_length', 'planck_lengths', 'lP', [ ], [ 'natural', 'science' ] ),

    'point' :
        UnitInfo( 'length', 'point', 'points', '', [ ], [ 'typography' ] ),

    'poppyseed' :
        UnitInfo( 'length', 'poppyseed', 'poppyseeds', '', [ ], [ 'imperial' ] ),

    'reed' :
        UnitInfo( 'length', 'reed', 'reeds', '', [ ], [ 'obsolete' ] ),

    'rod' :
        UnitInfo( 'length', 'rod', 'rods', 'rd', [ ], [ 'imperial' ] ),

    'rope' :
        UnitInfo( 'length', 'rope', 'ropes', '', [ ], [ 'obsolete' ] ),

    'potrzebie' :
        UnitInfo( 'length', 'potrzebie', 'potrzebies', 'pz', [ ], [ 'Potrzebie', 'humorous' ] ),

    'siriometer' :
        UnitInfo( 'length', 'siriometer', 'siriometers', '', [ ], [ 'science' ] ),  # proposed in 1911 by Cark V. L. Charlier

    'skein' :
        UnitInfo( 'length', 'skein', 'skeins', '', [ ], [ 'obsolete' ] ),

    'smoot' :
        UnitInfo( 'length', 'smoot', 'smoots', '', [ ], [ 'humorous' ] ),

    'solar_radius' :
        UnitInfo( 'length', 'solar_radius', 'solar_radii', 'Rsol', [ 'sun_radius', 'sun_radii' ], [ 'natural' ] ),

    'span' :
        UnitInfo( 'length', 'span', 'spans', '', [ 'breadth' ], [ 'imperial' ] ),

    'twip' :
        UnitInfo( 'length', 'twip', 'twips', '', [ ], [ 'computing' ] ),

    'yard' :
        UnitInfo( 'length', 'yard', 'yards', 'yd', [ ], [ 'imperial' ] ),

    # luminance

    'apostilb' :
        UnitInfo( 'luminance', 'apostilb', 'apostilbs', 'asb', [ 'blondel' ], [ 'CGS' ] ),

    'bril' :
        UnitInfo( 'luminance', 'bril', 'brils', '', [ ], [ 'obsolete' ] ),

    'candela/meter^2' :
        UnitInfo( 'luminance', 'candela/meter^2', 'candelas/meter^2', 'cd/m^2', [ 'candela/m^2', 'candelas/m^2', 'candela/square_meter', 'candelas/square_meter', 'cd/square_meter' ], [ 'SI' ] ),

    'footlambert' :
        UnitInfo( 'luminance', 'footlambert', 'footlamberts', 'fL', [ 'foot-lambert' ], [ 'US', 'obsolete' ] ),

    'lambert' :
        UnitInfo( 'luminance', 'lambert', 'lamberts', 'L', [ ], [ 'CGS' ] ),

    'nit' :
        UnitInfo( 'luminance', 'nit', 'nits', 'nt', [ 'meterlambert', 'meter-lambert', 'meterlamberts', 'meter-lamberts' ], [ 'obsolete' ] ),

    'skot' :
        UnitInfo( 'luminance', 'skot', 'skots', '', [ ], [ 'obsolete' ] ),

    'stilb' :
        UnitInfo( 'luminance', 'stilb', 'stilbs', 'sb', [ ], [ 'CGS' ] ),

    # luminous_flux

    'lumen' :
        UnitInfo( 'luminous_flux', 'lumen', 'lumens', 'lm', [ ], [ 'SI' ] ),

    'candela-steradian' :
        UnitInfo( 'luminous_flux', 'candela-steradian', 'candela-steradians', 'cd*sr', [ 'cd-sr' ], [ 'SI' ] ),

    # luminous_intensity

    'candela' :
        UnitInfo( 'luminous_intensity', 'candela', 'candelas', 'cd', [ ], [ 'SI' ] ),

    'hefnerkerze' :
        UnitInfo( 'luminous_intensity', 'hefnerkerze', 'hefnerkerze', 'HK', [ ], [ 'obsolete' ] ),

    # magnetic_field_strength

    'ampere/meter' :
        UnitInfo( 'magnetic_field_strength', 'ampere/meter', 'amperes/meter', 'A/m', [ 'amp/m', 'amps/m', 'ampere/m', 'amperes/m', 'A/meter', 'amp/meter', 'amps/meter', 'A/meters', 'amp/meters', 'amps/meters', 'ampere/meters', 'amperes/meters' ], [ 'SI' ] ),

    'oersted' :
        UnitInfo( 'magnetic_field_strength', 'oersted', 'oersted', 'Oe', [ ], [ 'CGS' ] ),

    # magnetic_flux

    'gauss*centimeter^2' :
        UnitInfo( 'magnetic_flux', 'gauss*centimeter^2', 'gauss*centimeter^2', 'gauss*cm^2', [ 'gauss*square_cm' ], [ 'CGS' ] ),

    'maxwell' :
        UnitInfo( 'magnetic_flux', 'maxwell', 'maxwells', 'Mx', [ 'line' ], [ 'CGS' ] ),

    'volt-second' :
        UnitInfo( 'magnetic_flux', 'volt*second', 'volts*seconds', 'V*s', [ ], [ 'SI' ] ),

    'unit_pole' :
        UnitInfo( 'magnetic_flux', 'unit_pole', 'unit_poles', '', [ 'unitpole', 'unitpoles' ], [ 'CGS' ] ),

    'tesla*meter^2' :
        UnitInfo( 'magnetic_flux', 'tesla*meter^2', 'tesla*meter^2', 'T/m^2', [ 'tesla*square_meter', 'teslas*square_meter', 'T*square_meter', 'tesla*m^2', 'teslas*m^2', 'teslas*meter^2' ], [ 'SI' ] ),

    'weber' :
        UnitInfo( 'magnetic_flux', 'weber', 'webers', 'Wb', [ ], [ 'SI' ] ),

    # magnetic_flux_density

    'gauss' :
        UnitInfo( 'magnetic_flux_density', 'gauss', 'gauss', '', [ ], [ 'CGS' ] ),

    'kilogram/ampere-second^2' :
        UnitInfo( 'magnetic_flux_density', 'kilogram/ampere*second^2', 'kilogram/ampere*second^2', 'kg/A*s^2', [ ], [ 'SI' ] ),

    'maxwell/centimeter^2' :
        UnitInfo( 'magnetic_flux_density', 'maxwell/centimeter^2', 'maxwells/centimeter^2', 'Mx/cm^2', [ 'maxwell/cm^2', 'maxwells/cm^2', 'Mx/centimeter^2', 'Mx/square_centimeter', 'Mx/square_cm', 'maxwell/square_centimeter', 'maxwells/square_centimeter', 'maxwell/square_cm', 'maxwells/square_cm' ], [ 'CGS' ] ),

    'tesla' :
        UnitInfo( 'magnetic_flux_density', 'tesla', 'teslas', 'T', [ ], [ 'SI' ] ),

    'weber/meter^2' :
        UnitInfo( 'magnetic_flux_density', 'weber/meter^2', 'webers/meter^2', 'Wb/m^2', [ ], [ 'SI' ] ),

    # mass

    'blintz' :
        UnitInfo( 'mass', 'blintz', 'blintzes', 'b', [ ], [ 'Potrzebie', 'humorous' ] ),

    'carat' :
        UnitInfo( 'mass', 'carat', 'carats', 'kt', [ 'karat', 'karats' ], [ 'US' ] ),

    'dalton' :
        UnitInfo( 'mass', 'dalton', 'daltons', '', [ 'amu', 'atomic_mass_unit' ], [ 'science' ] ),

    'doppelzentner' :
        UnitInfo( 'mass', 'doppelzentner', 'doppelzentners', '', [ ], [ 'Germany' ] ),

    'earth_mass' :
        UnitInfo( 'mass', 'earth_mass', 'earth_masses', 'Mgeo', [ ], [ 'natural' ] ),

    'farshimmelt_blintz' :
        UnitInfo( 'mass', 'farshimmelt_blintz', 'farshimmelt_blintzes', 'fb', [ 'far-blintz' ], [ 'Potrzebie', 'humorous' ] ),

    'furshlugginer_blintz' :
        UnitInfo( 'mass', 'furshlugginer_blintz', 'furshlugginer_blintzes', 'Fb', [ 'Fur-blintz' ], [ 'Potrzebie', 'humorous' ] ),

    'grain' :
        UnitInfo( 'mass', 'grain', 'grains', 'gr', [ ], [ 'traditional' ] ),

    'gram' :
        UnitInfo( 'mass', 'gram', 'grams', 'g', [ 'gramme', 'grammes' ], [ 'SI' ] ),

    'jupiter_mass' :
        UnitInfo( 'mass', 'jupiter_mass', 'jupiter_masses', 'Mjov', [ ], [ 'natural' ] ),

    'kip' :
        UnitInfo( 'mass', 'kip', 'kips', '', [ 'kilopound', 'kilopounds' ], [ 'US' ] ),

    'ounce' :
        UnitInfo( 'mass', 'ounce', 'ounces', 'oz', [ ], [ 'traditional' ] ),

    'pennyweight' :
        UnitInfo( 'mass', 'pennyweight', 'pennyweights', 'dwt', [ 'pwt' ], [ 'traditional', 'England' ] ),

    'pfund' :
        UnitInfo( 'mass', 'pfund', 'pfunds', '', [ ], [ 'Germany' ] ),

    'planck_mass' :
        UnitInfo( 'mass', 'planck_mass', 'planck_masses', 'mP', [ ], [ 'natural', 'science' ] ),

    'pound' :
        UnitInfo( 'mass', 'pound', 'pounds', 'lb', [ ], [ 'US', 'traditional', 'FPS' ] ),

    'proton_mass' :
        UnitInfo( 'mass', 'proton_mass', 'proton_masses', '', [ ], [ 'natural' ] ),

    'quintal' :
        UnitInfo( 'mass', 'quintal', 'quintals', 'q', [ ], [ ] ),

    'sheet' :
        UnitInfo( 'mass', 'sheet', 'sheets', '', [ ], [ ] ),

    'slug' :
        UnitInfo( 'mass', 'slug', 'slugs', '', [ 'gee_pound', 'geepound', 'gee-pound', 'gee_pounds', 'geepounds', 'gee-pounds' ], [ 'FPS' ] ),

    'solar_mass' :
        UnitInfo( 'mass', 'solar_mass', 'solar_masses', 'Msol', [ 'sun_mass', 'sun_masses' ], [ 'natural' ] ),

    'stone' :
        UnitInfo( 'mass', 'stone', 'stone', '', [ ], [ 'traditional', 'England' ] ),

    'stone_us' :
        UnitInfo( 'mass', 'stone_us', 'stones_us', '', [ 'us_stone', 'us_stones' ], [ 'US' ] ),

    'ton' :
        UnitInfo( 'mass', 'ton', 'tons', '', [ ], [ 'traditional', 'US' ] ),

    'tonne' :
        UnitInfo( 'mass', 'tonne', 'tonnes', '', [ ], [ 'MTS' ] ),

    'troy_ounce' :
        UnitInfo( 'mass', 'troy_ounce', 'troy_ounces', '', [ ], [ 'traditional' ] ),

    'troy_pound' :
        UnitInfo( 'mass', 'troy_pound', 'troy_pounds', '', [ ], [ 'traditional'  ] ),

    'wey' :
        UnitInfo( 'mass', 'wey', 'weys', '', [ ], [ 'obsolete', 'England' ] ),

    'zentner' :
        UnitInfo( 'mass', 'zentner', 'zentners', '', [ ], [ 'Germany' ] ),

    # particle masses

    'electron_mass' :
        UnitInfo( 'mass', 'electron_mass', 'electron_masses', '', [ 'electron_rest_mass', 'electron_rest_masses' ], [ 'natural', 'science' ] ),

    'proton_mass' :
        UnitInfo( 'mass', 'proton_mass', 'proton_masses', '', [ ], [ 'natural', 'science' ] ),

    'neutron_mass' :
        UnitInfo( 'mass', 'neutron_mass', 'neutron_masses', '', [ ], [ 'natural', 'science' ] ),

    'muon_mass' :
        UnitInfo( 'mass', 'muon_mass', 'muon_masses', '', [ ], [ 'natural', 'science' ] ),

    'deuteron_mass' :
        UnitInfo( 'mass', 'deuteron_mass', 'deuteron_masses', '', [ ], [ 'natural', 'science' ] ),

    'alpha_particle_mass' :
        UnitInfo( 'mass', 'alpha_particle_mass', 'alpha_particle_masses', '', [ 'alpha_mass', 'alpha_masses' ], [ 'natural', 'science' ] ),

    'tau_mass' :
        UnitInfo( 'mass', 'tau_mass', 'tau_masses', '', [ ], [ 'natural', 'science' ] ),

    'triton_mass' :
        UnitInfo( 'mass', 'triton_mass', 'triton_masses', '', [ ], [ 'natural', 'science' ] ),

    'helion_mass' :
        UnitInfo( 'mass', 'helion_mass', 'helion_masses', '', [ ], [ 'natural', 'science' ] ),

    # power

    'dBm' :
        UnitInfo( 'power', 'dBm', 'dBm', 'dBm', [ 'dBmW', 'decibel-milliwatt' ], [ 'engineering' ] ),

    'erg/second' :
        UnitInfo( 'power', 'erg/second', 'ergs/second', 'erg/s', [ 'ergs/s' ], [ 'CGS' ] ),

    'horsepower' :
        UnitInfo( 'power', 'horsepower', 'horsepower', 'hp', [ ], [ 'US' ] ),

    'joule/second' :
        UnitInfo( 'power', 'joule/second', 'joules/second', 'J/s', [ 'joule/s', 'joules/s', 'J/sec', 'joule/sec', 'joules/sec', 'J/seconds', 'joule/seconds', 'joules/seconds' ], [ 'SI' ] ),

    'lusec' :
        UnitInfo( 'power', 'lusec', 'lusecs', '', [ ], [ 'obsolete' ] ),

    'kilogram-meter^2/second^3' :
        UnitInfo( 'power', 'kilogram*meter^2/second^3', 'kilogram*meter^2/second^3', 'kg*m^2/s^3', [ ], [ 'SI' ] ),

    'newton-meter/second' :
        UnitInfo( 'power', 'newton*meter/second', 'newton*meter/second', 'N*m/s', [ ], [ 'SI' ] ),

    'pferdestarke' :
        UnitInfo( 'power', 'pferdestarke', 'pferdestarke', '', [ ], [ 'obsolete', 'Germany' ] ),

    'planck_power' :
        UnitInfo( 'power', 'planck_power', 'planck_power', '', [ ], [ 'natural', 'science' ] ),

    'poncelet' :
        UnitInfo( 'power', 'poncelet', 'poncelets', '', [ ], [ 'obsolete' ] ),

    'solar_luminosity' :
        UnitInfo( 'power', 'solar_luminosity', 'solar_luminosities', '', [ 'solar_output' ], [ 'natural' ] ),

    'volt-ampere' :
        UnitInfo( 'power', 'volt*ampere', 'volt*ampere', 'VA', [ ], [ 'SI' ] ),

    'watt' :
        UnitInfo( 'power', 'watt', 'watts', 'W', [ ], [ 'SI' ] ),

    # pressure

    'atmosphere' :
        UnitInfo( 'pressure', 'atmosphere', 'atmospheres', 'atm', [ ], [ 'natural' ] ),

    'bar' :
        UnitInfo( 'pressure', 'bar', 'bars', '', [ ], [ ] ),

    'barye' :
        UnitInfo( 'pressure', 'barye', 'baryes', 'Ba', [ 'barad' ], [ 'CGS' ] ),

    'mmHg' :
        UnitInfo( 'pressure', 'mmHg', 'mmHg', '', [ ], [ 'metric' ] ),

    'newton/meter^2' :
        UnitInfo( 'pressure', 'newton/meter^2', 'newtons/meter^2', 'N/m^2', [ ], [ 'SI' ] ),

    'pascal' :
        UnitInfo( 'pressure', 'pascal', 'pascals', 'Pa', [ ], [ 'SI' ] ),

    'pieze' :
        UnitInfo( 'pressure', 'pieze', 'piezes', '', [ ], [ 'MTS' ] ),

    'psi' :
        UnitInfo( 'pressure', 'pound/inch^2', 'pounds/inch^2', 'psi', [ 'lb/in^2' ], [ 'FPS' ] ),

    'torr' :
        UnitInfo( 'pressure', 'torr', 'torr', '', [ ], [ ] ),

    # radioactivity

    'becquerel' :
        UnitInfo( 'radioactivity', 'becquerel', 'becquerels', 'Bq', [ ], [ 'SI' ] ),

    'curie' :
        UnitInfo( 'radioactivity', 'curie', 'curies', 'Ci', [ ], [ 'obsolete' ] ),

    'rutherford' :
        UnitInfo( 'radioactivity', 'rutherford', 'rutherfords', 'rd', [ ], [ 'obsolete' ] ),

    # radiation_absorbed_dose

    'gray' :
        UnitInfo( 'radiation_absorbed_dose', 'gray', 'grays', 'Gy', [ ], [ 'SI' ] ),

    'joule/kilogram' :
        UnitInfo( 'radiation_absorbed_dose', 'joule/kilogram', 'joules/kilogram', 'J/kg', [ 'joule/kg', 'joules/kg', 'J/kilogram', 'J/kilograms', 'joule/kilograms', 'joules/kilograms' ], [ 'SI' ] ),

    'rad' :
        UnitInfo( 'radiation_absorbed_dose', 'rad', 'rads', '', [ ], [ 'CGS' ] ),

    # radiation_equivalent_dose

    'banana_equivalent_dose' :
        UnitInfo( 'radiation_equivalent_dose', 'banana_equivalent_dose', 'banana_equivalent_doses', '', [ 'banana' ], [ 'natural' ] ),

    'rem' :
        UnitInfo( 'radiation_equivalent_dose', 'rem', 'rems', '', [ 'roentgen_equivalent_man' ], [ 'CGS' ] ),

    'sievert' :
        UnitInfo( 'radiation_equivalent_dose', 'sievert', 'sieverts', 'Sv', [ ], [ 'SI' ] ),

    # radiation_exposure

    'coulomb/kilogram' :
        UnitInfo( 'radiation_exposure', 'coulomb/kilogram', 'coulombs/kilogram', 'C/kg', [ ], [ 'SI' ] ),

    'roentgen' :
        UnitInfo( 'radiation_exposure', 'roentgen', 'roentgens', 'R', [ 'parker' ], [ 'NIST' ] ),

    # solid_angle

    'sphere' :
        UnitInfo( 'solid_angle', 'sphere', 'spheres', '', [ ], [ 'mathematics' ] ),

    'square_arcminute' :
        UnitInfo( 'solid_angle', 'arcminute^2', 'arcminutes^2', 'arcmin^2', [ 'square_arcminutes', 'sq_arcminute', 'sq_arcminutes', 'sqarcmin', 'sqarcmins', 'arcmins^2' ], [ 'mathematics' ] ),

    'square_arcsecond' :
        UnitInfo( 'solid_angle', 'arcsecond^2', 'arcseconds^2', 'arcsec^2', [ 'square_arcseconds', 'sq_arcsecond', 'sq_arcseconds', 'sqarcsec', 'sqarcsecs', 'arcsecs^2' ], [ 'mathematics' ] ),

    'square_degree' :
        UnitInfo( 'solid_angle', 'degree^2', 'degrees^2', 'deg^2', [ 'square_degrees', 'sqdeg' ], [ 'mathematics' ] ),

    'square_octant' :
        UnitInfo( 'solid_angle', 'octant^2', 'octants^2', '', [ 'square_octants', 'sqoctant', 'sqoctants' ], [ 'mathematics' ] ),

    'square_quadrant' :
        UnitInfo( 'solid_angle', 'quadrant^2', 'quadrants^2', '', [ 'square_quadrants', 'sqquadrant', 'sqquadrants' ], [ 'mathematics' ] ),

    'square_quintant' :
        UnitInfo( 'solid_angle', 'quintant^2', 'quintants^2', '', [ 'square_quintants', 'sqquintant', 'sqquintants' ], [ 'mathematics' ] ),

    'square_sextant' :
        UnitInfo( 'solid_angle', 'sextant^2', 'sextants^2', '', [ 'square_sextants', 'sqsextant', 'sqsextants' ], [ 'mathematics' ] ),

    'square_grad' :
        UnitInfo( 'solid_angle', 'grad^2', 'grads^2', '', [ 'square_grads', 'sqgrad', 'square_gon', 'square_gons', 'sq_gon', 'sq_gons','sqgon', 'sqgons', 'grad^2', 'grads^2', 'gon^2', 'gons^2' ], [ 'mathematics' ] ),

    'steradian' :
        UnitInfo( 'solid_angle', 'steradian', 'steradians', 'sr', [ 'square_radian', 'square_radians', 'sq_radian', 'sq_radians', 'sq_rad', 'sqrad', 'radian^2', 'radians^2', 'rad^2' ], [ 'SI', 'mathematics' ] ),

    # temperature

    'celsius' :
        UnitInfo( 'temperature', 'celsius', 'degrees_celsius', '', [ 'centigrade', 'degC' ], [ 'SI' ] ),

    'degree_newton' :
        UnitInfo( 'temperature', 'degree_newton', 'degrees_newton', '', [ 'newton_degree', 'newton_degrees', 'degN' ], [ 'obsolete' ] ),

    'delisle' :
        UnitInfo( 'temperature', 'delisle', 'degrees_delisle', 'De', [ 'degDe' ], [ 'obsolete' ] ),

    'fahrenheit' :
        UnitInfo( 'temperature', 'fahrenheit', 'degrees_fahrenheit', '', [ 'fahr', 'degF' ], [ 'US', 'traditional' ] ),

    'kelvin' :
        UnitInfo( 'temperature', 'kelvin', 'degrees_kelvin', 'K', [ 'degK' ], [ 'SI' ] ),

    'rankine' :
        UnitInfo( 'temperature', 'rankine', 'degrees_rankine', 'R', [ 'degR' ], [ 'obsolete' ] ),

    'reaumur' :
        UnitInfo( 'temperature', 'reaumur', 'degrees_reaumur', 'Re', [ 'degRe' ], [ 'obsolete' ] ),

    'romer' :
        UnitInfo( 'temperature', 'romer', 'degrees_romer', 'Ro', [ 'defRo' ], [ 'obsolete' ] ),

    # time

    'beat' :
        UnitInfo( 'time', 'beat', 'beat', '', [ ], [ ] ),

    'blink' :
        UnitInfo( 'time', 'blink', 'blink', '', [ ], [ ] ),

    'century' :
        UnitInfo( 'time', 'century', 'centuries', 'y', [ ], [ 'traditional', 'US', 'years' ] ),

    'clarke' :
        UnitInfo( 'time', 'clarke', 'clarkes', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'cowznofski' :
        UnitInfo( 'time', 'cowznofski', 'cowznofskis', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'day' :
        UnitInfo( 'time', 'day', 'days', 'd', [ ], [ 'traditional', 'US' ] ),

    'decade' :
        UnitInfo( 'time', 'decade', 'decades', '', [ ], [ 'traditional', 'years' ] ),

    'fortnight' :
        UnitInfo( 'time', 'fortnight', 'fortnights', '', [ ], [ 'traditional' ] ),

    'gregorian_year' :
        UnitInfo( 'time', 'gregorian_year', 'gregorian_years', '', [ '' ], [ 'traditional' ] ),

    'hour' :
        UnitInfo( 'time', 'hour', 'hours', 'hr', [ ], [ 'traditional' ] ),

    'kovac' :
        UnitInfo( 'time', 'kovac', 'kovacs', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'jiffy' :
        UnitInfo( 'time', 'jiffy', 'jiffies', '', [ ], [ 'computing' ] ),

    'lunar_day' :
        UnitInfo( 'time', 'lunar_day', 'lunar_days', '', [ 'tidal_day', 'tidal_days' ], [ 'science' ] ),

    'lustrum' :
        UnitInfo( 'time', 'lustrum', 'lustra', '', [ ], [ 'obsolete', 'years' ] ),

    'martin' :
        UnitInfo( 'time', 'martin', 'martins', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'microcentury' :
        UnitInfo( 'time', 'microcentury', 'microcenturies', '', [ ], [ 'humorous', 'computing' ] ),

    'microfortnight' :
        UnitInfo( 'time', 'microfortnight', 'microfortnights', '', [ ], [ 'humorous', 'computing' ] ),

    'mingo' :
        UnitInfo( 'time', 'mingo', 'mingoes', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'minute' :
        UnitInfo( 'time', 'minute', 'minutes', '', [ ], [ 'traditional' ] ),  # 'min' is already an operator

    'month' :
        UnitInfo( 'time', 'month', 'months', 'mo', [ ], [ 'traditional', 'months' ] ),

    'nanocentury' :
        UnitInfo( 'time', 'nanocentury', 'nanocenturies', '', [ ], [ 'humorous', 'computing' ] ),

    'planck_time' :
        UnitInfo( 'time', 'x planck_time', 'x planck_time', 'tP', [ ], [ 'natural', 'science' ] ),

    'second' :
        UnitInfo( 'time', 'second', 'seconds', '', [ ], [ 'SI', 'traditional', 'FPS' ] ),   # 'sec' is already an operator

    'shake' :
        UnitInfo( 'time', 'shake', 'shakes', '', [ ], [ 'science' ] ),

    'sidereal_day' :
        UnitInfo( 'time', 'sidereal_day', 'sidereal_days', '', [ 'earth_day' ], [ 'science' ] ),

    'sidereal_hour' :
        UnitInfo( 'time', 'sidereal_hour', 'sidereal_hours', '', [ ], [ 'science' ] ),

    'sidereal_minute' :
        UnitInfo( 'time', 'sidereal_minute', 'sidereal_minutes', '', [ ], [ 'science' ] ),

    'sidereal_month' :
        UnitInfo( 'time', 'sidereal_month', 'sidereal_months', '', [ ], [ 'science' ] ),

    'sidereal_second' :
        UnitInfo( 'time', 'sidereal_second', 'sidereal_seconds', '', [ ], [ 'science' ] ),

    'sidereal_year' :
        UnitInfo( 'time', 'sidereal_year', 'sidereal_years', '', [ 'earth_year' ], [ 'science' ] ),

    'svedberg' :
        UnitInfo( 'time', 'svedberg', 'svedbergs', '', [ ], [ ] ),

    'tropical_year' :
        UnitInfo( 'time', 'tropical_year', 'tropical_years', '', [ 'solar_year', 'solar_years' ], [ 'science' ] ),

    'week' :
        UnitInfo( 'time', 'week', 'weeks', 'wk', [ 'sennight' ], [ 'traditional', 'obsolete' ] ),

    'wolverton' :
        UnitInfo( 'time', 'wolverton', 'wolvertons', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'wood' :
        UnitInfo( 'time', 'wood', 'woods', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'year' :
        UnitInfo( 'time', 'year', 'years', '', [ 'annum', 'julian_year', 'julian_years' ], [ 'traditional', 'years' ] ),

    # planet days

    'mercury_day' :
        UnitInfo( 'time', 'mercury_day', 'mercury_days', '', [ ], [ 'science' ] ),

    'venus_day' :
        UnitInfo( 'time', 'venus_day', 'venus_days', '', [ ], [ 'science' ] ),

    'mars_day' :
        UnitInfo( 'time', 'mars_day', 'mars_days', '', [ ], [ 'science' ] ),

    'jupiter_day' :
        UnitInfo( 'time', 'jupiter_day', 'jupiter_days', '', [ ], [ 'science' ] ),

    'saturn_day' :
        UnitInfo( 'time', 'saturn_day', 'saturn_days', '', [ ], [ 'science' ] ),

    'uranus_day' :
        UnitInfo( 'time', 'uranus_day', 'uranus_days', '', [ ], [ 'science' ] ),

    'neptune_day' :
        UnitInfo( 'time', 'neptune_day', 'neptune_days', '', [ ], [ 'science' ] ),

    'pluto_day' :
        UnitInfo( 'time', 'pluto_day', 'pluto_days', '', [ ], [ 'science' ] ),

    # planet years

    'mercury_year' :
        UnitInfo( 'time', 'mercury_year', 'mercury_years', '', [ ], [ 'science' ] ),

    'venus_year' :
        UnitInfo( 'time', 'venus_year', 'venus_years', '', [ ], [ 'science' ] ),

    'mars_year' :
        UnitInfo( 'time', 'mars_year', 'mars_years', '', [ ], [ 'science' ] ),

    'jupiter_year' :
        UnitInfo( 'time', 'jupiter_year', 'jupiter_years', '', [ ], [ 'science' ] ),

    'saturn_year' :
        UnitInfo( 'time', 'saturn_year', 'saturn_years', '', [ ], [ 'science' ] ),

    'uranus_year' :
        UnitInfo( 'time', 'uranus_year', 'uranus_years', '', [ ], [ 'science' ] ),

    'neptune_year' :
        UnitInfo( 'time', 'neptune_year', 'neptune_years', '', [ ], [ 'science' ] ),

    'pluto_year' :
        UnitInfo( 'time', 'pluto_year', 'pluto_years', '', [ ], [ 'science' ] ),

    # velocity

    'kine' :
        UnitInfo( 'velocity', 'kine', 'kine', '', [ '' ], [ 'CGS' ] ),

    'meter/second' :
        UnitInfo( 'velocity', 'meter/second', 'meters/second', 'm/s', [ 'mps' ], [ 'SI' ] ),

    'knot' :
        UnitInfo( 'velocity', 'knot', 'knots', '', [ ], [ 'nautical' ] ),

    'speed_of_light' :
        UnitInfo( 'velocity', 'speed_of_light', 'x_speed_of_light', 'c', [ 'light' ], [ 'natural' ] ),

    'mach' :
        UnitInfo( 'velocity', 'mach', 'mach', '', [ ], [ 'US' ] ),

    'mile/hour' :
        UnitInfo( 'velocity', 'mile/hour', 'miles/hour', 'mi/h', [ 'mph' ], [ 'FPS', 'imperial' ] ),

    'kilometer/hour' :
        UnitInfo( 'velocity', 'kilometer/hour', 'kilometers/hour', 'km/h', [ 'kph' ], [ 'FPS', 'imperial' ] ),

    # volume

    'acre-foot' :
        UnitInfo( 'volume', 'acre*foot', 'acre-feet', 'ac*ft', [ ], [ 'FPS', 'imperial' ] ),

    'balthazar' :
        UnitInfo( 'volume', 'balthazar', 'balthazars', '', [ ], [ 'wine' ] ),

    'bucket' :
        UnitInfo( 'volume', 'bucket', 'buckets', '', [ ], [ 'imperial' ] ),

    'bushel' :
        UnitInfo( 'volume', 'bushel', 'bushels', 'bu', [ ], [ 'imperial' ] ),

    'chopine' :
        UnitInfo( 'volume', 'chopine', 'chopines', '', [ ], [ 'wine' ] ),

    'clavelin' :
        UnitInfo( 'volume', 'clavelin', 'clavelins', '', [ ], [ 'wine' ] ),

    'cord' :
        UnitInfo( 'volume', 'cord', 'cords', '', [ ], [ 'traditional' ] ),

    'cubic_inch' :
        UnitInfo( 'volume', 'inch^3', 'cubic_inches', 'cuin', [ 'in^3', 'inch^3', 'inches^3' ], [ 'traditional' ] ),

    'cubic_foot' :
        UnitInfo( 'volume', 'foot^3', 'cubic_feet', 'cuft', [ 'ft^3', 'foot^3', 'feet^3' ], [ 'traditional', 'FPS' ] ),

    'cubic_meter' :
        UnitInfo( 'volume', 'meter^3', 'cubic_meters', 'm^3', [ 'meter^3', 'meters^3' ], [ 'SI' ] ),

    'coomb' :
        UnitInfo( 'volume', 'coomb', 'coombs', '', [ ], [ 'imperial' ] ),

    'cup' :
        UnitInfo( 'volume', 'cup', 'cups', '', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'dash' :
        UnitInfo( 'volume', 'dash', 'dashes', '', [ ], [ 'cooking' ] ),

    'demi' :
        UnitInfo( 'volume', 'demi', 'demis', '', [ ], [ 'wine' ] ),

    'dessertspoon' :
        UnitInfo( 'volume', 'dessertspoon', 'dessertspoons', '', [ ], [ 'traditional', 'cooking' ] ),

    'dram' :
        UnitInfo( 'volume', 'dram', 'drams', '', [ 'fluid_dram', 'fluid_drams', 'fluidram', 'fluidrams', 'fluid_drachm', 'fluid_drachms', 'fldr' ], [ 'traditional' ] ),

    'dry_barrel' :
        UnitInfo( 'volume', 'dry_barrel', 'dry_barrels', '', [ ], [ 'imperial' ] ),

    'dry_hogshead' :
        UnitInfo( 'volume', 'dry_hogshead', 'dry_hogsheads', '', [ ], [ 'imperial' ] ),

    'dry_gallon' :
        UnitInfo( 'volume', 'dry_gallon', 'dry_gallons', '', [ ], [ 'traditional', 'US' ] ),

    'dry_pint' :
        UnitInfo( 'volume', 'dry_pint', 'dry_pints', '', [ ], [ 'traditional', 'US' ] ),

    'dry_quart' :
        UnitInfo( 'volume', 'dry_quart', 'dry_quarts', '', [ ], [ 'traditional', 'US' ] ),

    'dry_tun' :
        UnitInfo( 'volume', 'dry_tun', 'dry_tuns', '', [ ], [ 'imperial' ] ),

    'farshimmelt_ngogn' :
        UnitInfo( 'volume', 'farshimmelt_ngogn', 'farshimmelt_ngogns', 'fn', [ 'far-ngogn' ], [ 'Potrzebie', 'humorous' ] ),

    'fifth' :
        UnitInfo( 'volume', 'fifth', 'fifths', '', [ ], [ 'wine' ] ),

    'firkin' :
        UnitInfo( 'volume', 'firkin', 'firkins', '', [ ], [ 'imperial' ] ),

    'fluid_ounce' :
        UnitInfo( 'volume', 'fluid_ounce', 'fluid_ounces', '', [ 'floz' ], [ 'traditional' ] ),

    'furshlugginer_ngogn' :
        UnitInfo( 'volume', 'furshlugginer_ngogn', 'furshlugginer_ngogns', 'Fn', [ 'Fur-ngogn' ], [ 'Potrzebie', 'humorous' ] ),

    'gallon' :
        UnitInfo( 'volume', 'gallon', 'gallons', 'gal', [ ], [ 'imperial' ] ),

    'gill' :
        UnitInfo( 'volume', 'gill', 'gills', '', [ ], [ 'imperial' ] ),

    'goliath' :
        UnitInfo( 'volume', 'goliath', 'goliaths', '', [ 'primat' ], [ 'wine' ] ),

    'hogshead' :
        UnitInfo( 'volume', 'hogshead', 'hogsheads', '', [ ], [ 'traditional', 'wine' ] ),

    'imperial' :
        UnitInfo( 'volume', 'imperial', 'imperials', '', [ ], [ 'wine' ] ),

    'imperial_bushel' :
        UnitInfo( 'volume', 'imperial_bushel', 'imperial_bushels', '', [ ], [ 'imperial' ] ),

    'imperial_butt' :
        UnitInfo( 'volume', 'imperial_butt', 'imperial_butts', '', [ 'imperial_pipe', 'imperial_pipes' ], [ 'imperial' ] ),

    'imperial_cup' :
        UnitInfo( 'volume', 'imperial_cup', 'imperial_cups', '', [ ], [ 'imperial' ] ),

    'imperial_gallon' :
        UnitInfo( 'volume', 'imperial_gallon', 'imperial_gallons', '', [ ], [ 'imperial' ] ),

    'imperial_gill' :
        UnitInfo( 'volume', 'imperial_gill', 'imperial_gills', '', [ ], [ 'imperial' ] ),

    'imperial_hogshead' :
        UnitInfo( 'volume', 'imperial_hogshead', 'imperial_hogsheads', '', [ ], [ 'imperial' ] ),

    'imperial_peck' :
        UnitInfo( 'volume', 'imperial_peck', 'imperial_pecks', '', [ ], [ 'imperial' ] ),

    'imperial_pint' :
        UnitInfo( 'volume', 'imperial_pint', 'imperial_pints', '', [ ], [ 'imperial' ] ),

    'imperial_quart' :
        UnitInfo( 'volume', 'imperial_quart', 'imperial_quarts', '', [ ], [ 'imperial' ] ),

    'jack' :
        UnitInfo( 'volume', 'jack', 'jacks', '', [ 'jackpot' ], [ 'imperial' ] ),

    'jennie' :
        UnitInfo( 'volume', 'jennie', 'jennies', '', [ ], [ 'wine' ] ),

    'jeroboam' :
        UnitInfo( 'volume', 'jeroboam', 'jeroboams', '', [ 'double_magnum' ], [ 'wine' ] ),

    'jigger' :
        UnitInfo( 'volume', 'jigger', 'jiggers', '', [ ], [ 'imperial' ] ),

    'kenning' :
        UnitInfo( 'volume', 'kenning', 'kennings', '', [ ], [ 'imperial' ] ),

    'kilderkin' :
        UnitInfo( 'volume', 'kilderkin', 'kilderkins', '', [ ], [ 'imperial' ] ),

    'liter' :
        UnitInfo( 'volume', 'liter', 'liters', 'l', [ ], [ 'SI' ] ),

    'magnum' :
        UnitInfo( 'volume', 'magnum', 'magnums', '', [ ], [ 'wine' ] ),

    'marie_jeanne' :
        UnitInfo( 'volume', 'marie_jeanne', 'marie_jeannes', '', [ ], [ 'wine' ] ),

    'melchior' :
        UnitInfo( 'volume', 'melchior', 'melchiors', '', [ ], [ 'wine' ] ),

    'melchizedek' :
        UnitInfo( 'volume', 'melchizedek', 'melchizedeks', '', [ ], [ 'wine' ] ),

    'methuselah' :
        UnitInfo( 'volume', 'methuselah', 'methuselahs', '', [ ], [ 'wine' ] ),

    'minim':
        UnitInfo( 'volume', 'minim', 'minims', 'gtt', [ 'drop' ], [ 'traditional' ] ),

    'mordechai' :
        UnitInfo( 'volume', 'mordechai', 'mordechais', '', [ ], [ 'wine' ] ),

    'nebuchadnezzar' :
        UnitInfo( 'volume', 'nebuchadnezzar', 'nebuchadnezzars', '', [ ], [ 'wine' ] ),

    'ngogn' :
        UnitInfo( 'volume', 'ngogn', 'ngogns', '', [ ], [ 'Potrzebie', 'humorous' ] ),

    'oil_barrel' :
        UnitInfo( 'volume', 'oil_barrel', 'oil_barrels', 'bbl', [ ], [ 'US' ] ),

    'peck' :
        UnitInfo( 'volume', 'peck', 'pecks', 'pk', [ ], [ 'imperial' ] ),

    'piccolo' :
        UnitInfo( 'volume', 'piccolo', 'piccolos', '', [ ], [ 'wine' ] ),

    'pinch' :
        UnitInfo( 'volume', 'pinch', 'pinches', '', [ ], [ 'traditional', 'cooking' ] ),

    'pin' :
        UnitInfo( 'volume', 'pin', 'pins', '', [ ], [ 'imperial' ] ),

    'pint' :
        UnitInfo( 'volume', 'pint', 'pints', 'pt', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'pipe' :
        UnitInfo( 'volume', 'pipe', 'pipes', '', [ 'butt', 'butts' ], [ 'imperial' ] ),

    'planck_volume' :
        UnitInfo( 'volume', 'planck_volume', 'planck_volumes', '', [ ], [ 'natural', 'science' ] ),

    'pony' :
        UnitInfo( 'volume', 'pony', 'ponies', '', [ ], [ 'imperial' ] ),

    'pottle' :
        UnitInfo( 'volume', 'pottle', 'pottles', '', [ ], [ 'imperial' ] ),

    'puncheon' :
        UnitInfo( 'volume', 'puncheon', 'puncheons', '', [ 'tertian', 'tertians' ], [ 'wine' ] ),

    'quart' :
        UnitInfo( 'volume', 'quart', 'quarts', '', [ ], [ 'US' ] ),

    'rehoboam' :
        UnitInfo( 'volume', 'rehoboam', 'rehoboams', '', [ ], [ 'wine' ] ),

    'rundlet' :
        UnitInfo( 'volume', 'rundlet', 'rundlets', '', [ ], [ 'imperial', 'wine' ] ),

    'salmanazar' :
        UnitInfo( 'volume', 'salmanazar', 'salmanazars', '', [ ], [ 'wine' ] ),

    'scruple' :
        UnitInfo( 'volume', 'scruple', 'scruples', '', [ 'fluid_scruple', 'fluid_scruples' ], [ 'traditional' ] ),

    'smidgen' :
        UnitInfo( 'volume', 'smidgen', 'smidgens', '', [ 'smidgeon', 'smidgeons' ], [ 'traditional', 'cooking' ] ),

    'solomon' :
        UnitInfo( 'volume', 'solomon', 'solomons', '', [ ], [ 'wine' ] ),

    'sovereign' :
        UnitInfo( 'volume', 'sovereign', 'sovereigns', '', [ ], [ 'wine' ] ),

    'standard' :
        UnitInfo( 'volume', 'standard', 'standards', '', [ ], [ 'wine' ] ),

    'stere' :
        UnitInfo( 'volume', 'stere', 'steres', 'st', [ ], [ 'metric', 'obsolete' ] ),  # ... but not SI

    'strike' :
        UnitInfo( 'volume', 'strike', 'strikes', '', [ ], [ 'imperial' ] ),

    'tablespoon' :
        UnitInfo( 'volume', 'tablespoon', 'tablespoons', 'tbsp', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'teaspoon' :
        UnitInfo( 'volume', 'teaspoon', 'teaspoons', 'tsp', [ ], [ 'traditional', 'cooking', 'US' ] ),

    'tenth' :
        UnitInfo( 'volume', 'tenth', 'tenths', '', [ ], [ 'wine' ] ),

    'tierce' :
        UnitInfo( 'volume', 'tierce', 'tierces', '', [ ], [ 'wine', 'imperial' ] ),

    'tun' :
        UnitInfo( 'volume', 'tun', 'tuns', '', [ ], [ 'imperial' ] ),

    'wine_barrel' :
        UnitInfo( 'volume', 'wine_barrel', 'wine_barrels', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_butt' :
        UnitInfo( 'volume', 'wine_butt', 'wine_butts', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_gallon' :
        UnitInfo( 'volume', 'wine_gallon', 'wine_gallons', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_hogshead' :
        UnitInfo( 'volume', 'wine_hogshead', 'wine_hogsheads', '', [ ], [ 'imperial', 'wine' ] ),

    'wine_pipe' :
        UnitInfo( 'volume', 'wine_pipe', 'wine_pipes', '', [ 'wine_butt', 'wine_butts' ], [ 'imperial' ] ),

    'wine_tun' :
        UnitInfo( 'volume', 'wine_tun', 'wine_tuns', '', [ ], [ 'imperial', 'wine' ] ),
}


#//******************************************************************************
#//
#//  metricUnits
#//
#//  ... or any units that should get the SI prefixes
#//
#//  ( name, plural name, abbreviation, aliases, plural aliases )
#//
#//******************************************************************************

metricUnits = [
    ( 'ampere',             'amperes',          'A',    [ 'amp' ], [ 'amps' ] ),
    ( 'ampere-second',      'ampere-seconds',   'As',   [ 'amp-second' ], [ 'amp-seconds' ] ),
    ( 'are',                'ares',             'a',    [ ], [ ] ),
    ( 'bar',                'bars',             'bar',  [ ], [ ] ),
    ( 'barn',               'barns',            'bn',   [ ], [ ] ),     # 'bn' is not standard
    ( 'becquerel',          'becquerels',       'Bq',   [ ], [ ] ),
    ( 'blintz',             'blintzes',         'bl',   [ ], [ ] ),
    ( 'coulomb',            'coulombs',         'C',    [ ], [ ] ),
    ( 'calorie',            'calories',         'cal',  [ 'cal' ], [ 'cals' ] ),
    ( 'electronvolt',       'electronvolts',    'eV',   [ ], [ ] ),
    ( 'farad',              'farad',            'F',    [ ], [ ] ),
    ( 'gram-equivalent',    'grams-equivalent', 'gE',   [ 'gram-energy', 'gramme-energy' ], [ 'grams-energy', 'grammes-energy' ] ),
    ( 'gram',               'grams',            'g',    [ 'gramme' ], [ 'grammes' ] ),
    ( 'gram-force',         'grams-force',      'gf',   [ 'gramme-force' ], [ 'grammes-force' ] ),
    ( 'henry',              'henries',          'H',    [ ], [ ] ),
    ( 'joule',              'joules',           'J',    [ ], [ ] ),
    ( 'kelvin',             'kelvins',          'K',    [ ], [ ] ),
    ( 'liter',              'liters',           'l',    [ 'litre' ], [ 'litres' ] ),
    ( 'light-year',         'light-years',      'ly',   [ ], [ ] ),
    ( 'lux',                'lux',              'lx',   [ ], [ ] ),
    ( 'meter',              'meters',           'm',    [ 'metre' ], [ 'metres' ] ),
    ( 'newton',             'newtons',          'N',    [ ], [ ] ),
    ( 'ngogn',              'ngogns',           'ng',   [ ], [ ] ),
    ( 'ohm',                'ohms',             'O',    [ ], [ ] ),
    ( 'parsec',             'parsecs',          'pc',   [ ], [ ] ),
    ( 'pascal',             'pascals',          'Pa',   [ ], [ ] ),
    ( 'pascal-second',      'pascal-seconds',   'Pas',  [ ], [ ] ),
    ( 'pond',               'ponds',            'pond', [ ], [ ] ),     # 'p' is used for 'pico'
    ( 'potrzebie',          'potrzebies',       'pz',   [ ], [ ] ),
    ( 'rem',                'rems',             'rem',  [ ], [ ] ),
    ( 'second',             'seconds',          's',    [ ], [ ] ),
    ( 'siemens',            'siemens',          'S',    [ 'mho' ], [ 'mhos' ] ),
    ( 'sievert',            'sieverts',         'Sv',   [ ], [ ] ),
    ( 'stere',              'steres',           'st',   [ ], [ ] ),
    ( 'tesla',              'teslas',           'T',    [ ], [ ] ),
    ( 'ton_of_TNT',         'tons_of_TNT',      'tTNT', [ ], [ ] ),
    ( 'volt',               'volts',            'V',    [ ], [ ] ),
    ( 'watt',               'watts',            'W',    [ ], [ ] ),
    ( 'watt-second',        'watt-seconds',     'Ws',   [ ], [ ] ),
]


#//******************************************************************************
#//
#//  dataUnits
#//
#//  ... or any units that should get the SI prefixes (positive powers of 10)
#//  and the binary prefixes
#//
#//  ( name, plural name, abbreviation, aliases, plural aliases )
#//
#//******************************************************************************

dataUnits = [
    ( 'bit',            'bits',             'b',    [ ], [ ] ),
    ( 'bit/second',     'bits/second',      'bps',  [ ], [ ] ),
    ( 'byte',           'bytes',            'B',    [ ], [ ] ),
    ( 'byte/second',    'bytes/second',     'Bps',  [ ], [ ] ),
]


#//******************************************************************************
#//
#//  timeUnits
#//
#//******************************************************************************

timeUnits = [
    ( 'minute',     'minutes',      'm',        '60' ),
    ( 'hour',       'hours',        'h',        '3600' ),
    ( 'day',        'days',         'd',        '86400' ),
    ( 'year',       'years',        'y',        '31557600' ),   # Julian year == 365.25 days
]


#//******************************************************************************
#//
#//  metricPrefixes
#//
#//  ( name, abbreviation, power of 10 )
#//
#//******************************************************************************

metricPrefixes = [
    ( 'yotta',      'Y',      '24' ),
    ( 'zetta',      'Z',      '21' ),
    ( 'exa',        'E',      '18' ),
    ( 'peta',       'P',      '15' ),
    ( 'tera',       'T',      '12' ),
    ( 'giga',       'G',      '9' ),
    ( 'mega',       'M',      '6' ),
    ( 'kilo',       'k',      '3' ),
    ( 'hecto',      'h',      '2' ),
    ( 'deca',       'da',     '1' ),
    ( 'deci',       'd',      '-1' ),
    ( 'centi',      'c',      '-2' ),
    ( 'milli',      'm',      '-3' ),
    ( 'micro',      'u',      '-6' ),  # it's really a mu
    ( 'nano',       'n',      '-9' ),
    ( 'pico',       'p',      '-12' ),
    ( 'femto',      'f',      '-15' ),
    ( 'atto',       'a',      '-18' ),
    ( 'zepto',      'z',      '-21' ),
    ( 'yocto',      'y',      '-24' ),
]


#//******************************************************************************
#//
#//  dataPrefixes
#//
#//  ( name, abbreviation, power of 10 )
#//
#//******************************************************************************

dataPrefixes = [
    ( 'yotta',      'Y',      '24' ),
    ( 'zetta',      'Z',      '21' ),
    ( 'exa',        'E',      '18' ),
    ( 'peta',       'P',      '15' ),
    ( 'tera',       'T',      '12' ),
    ( 'giga',       'G',      '9' ),
    ( 'mega',       'M',      '6' ),
    ( 'kilo',       'k',      '3' ),
]


#//******************************************************************************
#//
#//  binaryPrefixes
#//
#//  ( name, abbreviation, power of 2 )
#//
#//******************************************************************************

binaryPrefixes = [
    ( 'yobi',       'Yi',     '80' ),
    ( 'zebi',       'Zi',     '70' ),
    ( 'exi',        'Ei',     '60' ),
    ( 'pebi',       'Pi',     '50' ),
    ( 'tebi',       'Ti',     '40' ),
    ( 'gibi',       'Gi',     '30' ),
    ( 'mebi',       'Mi',     '20' ),
    ( 'kibi',       'ki',     '10' ),
]


#//******************************************************************************
#//
#//  conversion constants
#//
#//******************************************************************************

speedOfLight = '299792458'   # in m/s by definition


#//******************************************************************************
#//
#//  unitConversionMatrix
#//
#//  ( first unit, second unit, conversion factor )
#//
#//******************************************************************************

unitConversionMatrix = {
    ( 'aa_battery',                 'joule' )                               : mpmathify( '15400' ),
    ( 'abampere',                   'ampere' )                              : mpmathify( '10' ),
    ( 'abcoulomb',                  'coulomb' )                             : mpmathify( '10' ),
    ( 'abfarad',                    'farad' )                               : mpmathify( '1.0e9' ),
    ( 'abmho',                      'siemens' )                             : mpmathify( '1.0e9' ),
    ( 'acre',                       'nanoacre' )                            : mpmathify( '1.0e9' ),
    ( 'acre',                       'square_yard' )                         : mpmathify( '4840' ),
    ( 'acre-foot',                  'cubic_foot' )                          : mpmathify( '43560' ),
    ( 'aln',                        'inch' )                                : mpmathify( '23.377077865' ),
    ( 'alpha',                      'unity' )                               : mpmathify( '0.0072973526' ),
    ( 'alpha_particle_mass',        'dalton' )                              : mpmathify( '4.001506179125' ),
    ( 'ampere',                     'coulomb/second' )                      : mpmathify( '1' ),
    ( 'ampere',                     'statampere' )                          : mpmathify( speedOfLight ),
    ( 'arcminute',                  'arcsecond' )                           : mpmathify( '60' ),
    ( 'arcsecond',                  'milliarcsecond' )                      : mpmathify( '1000' ),
    ( 'are',                        'square_meter' )                        : mpmathify( '100' ),
    ( 'arpent',                     'foot' )                                : mpmathify( '192' ),
    ( 'astronomical_unit',          'meter' )                               : mpmathify( '149597870691' ),
    ( 'atmosphere',                 'pascal' )                              : mpmathify( '101325' ),
    ( 'balthazar',                  'liter' )                               : mpmathify( '12.0' ),
    ( 'ban',                        'nat' )                                 : log( 10 ),
    ( 'banana_equivalent_dose',     'sievert' )                             : mpmathify( '9.8e-8' ),
    ( 'bar',                        'pascal' )                              : mpmathify( '1.0e5' ),
    ( 'barleycorn',                 'poppyseed' )                           : mpmathify( '4' ),
    ( 'beat',                       'blink' )                               : mpmathify( '100' ),
    ( 'becquerel',                  'curie' )                               : mpmathify( '3.7e10' ),
    ( 'billion',                    'unity' )                               : mpmathify( '1.0e9' ),
    ( 'bit',                        'nat' )                                 : log( 2 ),
    ( 'blintz',                     'farshimmelt_blintz' )                  : mpmathify( '1.0e5' ),
    ( 'blintz',                     'furshlugginer_blintz' )                : mpmathify( '1.0e-6' ),
    ( 'blintz',                     'gram' )                                : mpmathify( '36.42538631' ),
    ( 'bohr_radius',                'meter' )                               : mpmathify( '5.2917721e-11' ),
    ( 'bolt',                       'foot' )                                : mpmathify( '120' ),
    ( 'boltzmann_constant',         'joule/kelvin' )                        : mpmathify( '1.3806488e-23' ),
    ( 'btu',                        'joule' )                               : mpmathify( '1054.5' ),
    ( 'btupf',                      'joule/kelvin' )                        : mpmathify( '1899.100534716' ),
    ( 'bucket',                     'gallon' )                              : mpmathify( '4' ),
    ( 'bushel',                     'peck' )                                : mpmathify( '4' ),
    ( 'byte',                       'bit' )                                 : mpmathify( '8' ),
    ( 'calorie',                    'joule' )                               : mpmathify( '4.184' ),
    ( 'carat',                      'grain' )                               : fadd( 3, fdiv( 1, 6 ) ),
    ( 'carucate',                   'acre' )                                : mpmathify( '120' ),
    ( 'carucate',                   'bovate' )                              : mpmathify( '8' ),
    ( 'centillion',                 'unity' )                               : mpmathify( '1.0e303' ),
    ( 'century',                    'microcentury' )                        : mpmathify( '1.0e6' ),
    ( 'century',                    'nanocentury' )                         : mpmathify( '1.0e9' ),
    ( 'century',                    'year' )                                : mpmathify( '100' ),
    ( 'chain',                      'yard' )                                : mpmathify( '22' ),
    ( 'chopine',                    'liter' )                               : mpmathify( '0.25' ),
    ( 'clarke',                     'day' )                                 : mpmathify( '1' ),
    ( 'clarke',                     'wolverton' )                           : mpmathify( '1.0e6' ),
    ( 'clausius',                   'joule/kelvin' )                        : mpmathify( '4186.8' ),
    ( 'clavelin',                   'liter' )                               : mpmathify( '0.62' ),
    ( 'coomb',                      'strike' )                              : mpmathify( '2' ),
    ( 'cord',                       'cubic_foot' )                          : mpmathify( '128' ),
    ( 'coulomb',                    'ampere-second' )                       : mpmathify( '1' ),
    ( 'coulomb',                    'farad-volt' )                          : mpmathify( '1' ),
    ( 'coulomb/farad',              'volt' )                                : mpmathify( '1' ),
    ( 'coulomb/kilogram',           'roentgen' )                            : mpmathify( '3876' ),
    ( 'coulomb/volt',               'farad' )                               : mpmathify( '1' ),
    ( 'cowznofski',                 'mingo' )                               : mpmathify( '10' ),
    ( 'cubic_meter',                'liter' )                               : mpmathify( '1000' ),
    ( 'cubit',                      'inch' )                                : mpmathify( '18' ),
    ( 'cup',                        'dram' )                                : mpmathify( '64' ),
    ( 'cup',                        'fluid_ounce' )                         : mpmathify( '8' ),
    ( 'cup',                        'gill' )                                : mpmathify( '2' ),
    ( 'daily',                      'monthly' )                             : mpmathify( '30' ),
    ( 'daily',                      'weekly' )                              : mpmathify( '7' ),
    ( 'daily',                      'yearly' )                              : mpmathify( '365.25' ),
    ( 'day',                        'beat' )                                : mpmathify( '1000' ),
    ( 'day',                        'hour' )                                : mpmathify( '24' ),
    ( 'decade',                     'year' )                                : mpmathify( '10' ),
    ( 'decillion',                  'unity' )                               : mpmathify( '1.0e33' ),
    ( 'degree',                     'arcminute' )                           : mpmathify( '60' ),
    ( 'demi',                       'liter' )                               : mpmathify( '0.375' ),
    ( 'density_of_water',           'gram/meter^3' )                        : mpmathify( '1.0e6' ),
    ( 'dessertspoon',               'teaspoon' )                            : mpmathify( '2' ),
    ( 'deuteron_mass',              'dalton' )                              : mpmathify( '2.013553212712' ),
    ( 'doppelzentner',              'zentner' )                             : mpmathify( '2' ),
    ( 'dozen',                      'unity' )                               : mpmathify( '12' ),
    ( 'dram',                       'scruple' )                             : mpmathify( '3' ),
    ( 'dry_barrel',                 'bushel' )                              : mpmathify( '4' ),
    ( 'dry_barrel',                 'cubic_inch' )                          : mpmathify( '7056' ),
    ( 'dry_gallon',                 'dry_quart' )                           : mpmathify( '4' ),
    ( 'dry_hogshead',               'dry_barrel' )                          : mpmathify( '2' ),
    ( 'dry_pint',                   'cubic_inch' )                          : mpmathify( '33.6003125' ),
    ( 'dry_quart',                  'dry_pint' )                            : mpmathify( '2' ),
    ( 'dry_tun',                    'dry_hogshead' )                        : mpmathify( '4' ),
    ( 'duodecillion',               'unity' )                               : mpmathify( '1.0e39' ),
    ( 'dword',                      'bit' )                                 : mpmathify( '32' ),
    ( 'earth_mass',                 'gram' )                                : mpmathify( '5.9742e27' ),
    ( 'earth_radius',               'meter' )                               : mpmathify( '6378136' ),
    ( 'electron_charge',            'coulomb' )                             : mpmathify( '1.602176565e-19' ),
    ( 'electron_mass',              'gram' )                                : mpmathify( '9.10938291e-28' ),
    ( 'ell',                        'inch' )                                : mpmathify( '45' ),
    ( 'every_minute',               'hourly' )                              : mpmathify( '60' ),
    ( 'famn',                       'aln' )                                 : mpmathify( '3' ),
    ( 'farad',                      'jar' )                                 : mpmathify( '9.0e8' ),
    ( 'farad',                      'statfarad' )                           : mpmathify( '898755178736.5' ),
    ( 'faraday',                    'coulomb' )                             : mpmathify( '96485.3383' ),
    ( 'fathom',                     'foot' )                                : mpmathify( '6' ),
    ( 'finger',                     'inch' )                                : mpmathify( '4.5' ),
    ( 'fingerbreadth',              'inch' )                                : mpmathify( '0.75' ),
    ( 'firkin',                     'gallon' )                              : mpmathify( '9' ),
    ( 'firkin',                     'pin' )                                 : mpmathify( '2' ),
    ( 'flock',                      'unity' )                               : mpmathify( '40' ),
    ( 'fluid_ounce',                'dram' )                                : mpmathify( '8' ),
    ( 'fluid_ounce',                'tablespoon' )                          : mpmathify( '2' ),
    ( 'foot',                       'inch' )                                : mpmathify( '12' ),
    ( 'footcandle',                 'lumen/foot^2' )                        : mpmathify( '1' ),
    ( 'footcandle',                 'lux' )                                 : mpmathify( '10.763910417' ),            # (m/ft)^2
    ( 'footlambert',                'candela/meter^2' )                     : mpmathify( '3.42625909963539052691' ),  # 1/pi cd/ft^2
    ( 'fortnight',                  'day' )                                 : mpmathify( '14' ),
    ( 'fortnight',                  'microfortnight' )                      : mpmathify( '1.0e6' ),
    ( 'furlong',                    'yard' )                                : mpmathify( '220' ),
    ( 'gallon',                     'fifth' )                               : mpmathify( '5' ),
    ( 'gallon',                     'quart' )                               : mpmathify( '4' ),
    ( 'gallon_of_gasoline',         'gallon_of_ethanol' )                   : mpmathify( '1.425' ),  # approx.
    ( 'gallon_of_gasoline',         'joule' )                               : mpmathify( '1.2e8' ),  # approx. obviously
    ( 'gauss',                      'maxwell/centimeter^2' )                : mpmathify( '1' ),
    ( 'goliath',                    'liter' )                               : mpmathify( '27.0' ),
    ( 'googol',                     'unity' )                               : mpmathify( '1.0e100' ),
    ( 'grad',                       'degree' )                              : mpmathify( '0.9' ),
    ( 'gram',                       'dalton' )                              : mpmathify( '1.66053886e-24' ),
    ( 'gram',                       'planck_mass' )                         : mpmathify( '45945.113967' ),
    ( 'gram-equivalent',            'joule' )                               : fdiv( power( mpf( speedOfLight ), 2 ), 1000 ),
    ( 'gray',                       'joule/kilogram' )                      : mpmathify( '1' ),
    ( 'gray',                       'rad' )                                 : mpmathify( '100' ),
    ( 'great_gross',                'gross' )                               : mpmathify( '12' ),
    ( 'greek_cubit',                'inch' )                                : mpmathify( '18.22' ),
    ( 'gregorian_year',             'day' )                                 : mpmathify( '365.2425' ),
    ( 'gross',                      'unity' )                               : mpmathify( '144' ),
    ( 'handbreadth',                'inch' )                                : mpmathify( '3' ),
    ( 'hartree',                    'rydberg' )                             : mpmathify( '2' ),
    ( 'hefnerkerze',                'candela' )                             : mpmathify( '0.920' ),  # approx.
    ( 'helion_mass',                'dalton' )                              : mpmathify( '3.0149322468' ),
    ( 'henry',                      'abhenry' )                             : mpmathify( '1.0e9' ),
    ( 'henry',                      'weber/ampere' )                        : mpmathify( '1' ),
    ( 'hertz',                      'every_minute' )                        : mpmathify( '60' ),
    ( 'homestead',                  'acre' )                                : mpmathify( '160' ),
    ( 'horsepower',                 'watt' )                                : mpmathify( '745.69987158227022' ),
    ( 'horsepower-second',          'joule' )                               : mpmathify( '745.69987158227022' ),
    ( 'hour',                       'minute' )                              : mpmathify( '60' ),
    ( 'hourly',                     'daily' )                               : mpmathify( '24' ),
    ( 'hundred',                    'unity' )                               : mpmathify( '100' ),
    ( 'impedance_of_free_space',    'ohm' )                                 : fmul( pi, mpmathify( '119.9169832' ) ),
    ( 'imperial_bushel',            'kenning' )                             : mpmathify( '2' ),
    ( 'imperial_butt',              'imperial_hogshead' )                   : mpmathify( '2' ),
    ( 'imperial_cup',               'imperial_gill' )                       : mpmathify( '2' ),
    ( 'imperial_gallon',            'pottle' )                              : mpmathify( '2' ),
    ( 'imperial_gill',              'jack' )                                : mpmathify( '2' ),
    ( 'imperial_hogshead',          'coomb' )                               : mpmathify( '2' ),
    ( 'imperial_peck',              'imperial_quart' )                      : mpmathify( '2' ),
    ( 'imperial_pint',              'imperial_cup' )                        : mpmathify( '2' ),
    ( 'imperial_quart',             'imperial_pint' )                       : mpmathify( '2' ),
    ( 'imperial_square',            'square_foot' )                         : mpmathify( '100' ),
    ( 'inch',                       'barleycorn' )                          : mpmathify( '3' ),
    ( 'inch',                       'caliber' )                             : mpmathify( '100' ),
    ( 'inch',                       'gutenberg' )                           : mpmathify( '7200' ),
    ( 'inch',                       'meter' )                               : mpmathify( '0.0254' ),
    ( 'inch',                       'mil' )                                 : mpmathify( '1000' ),
    ( 'inch',                       'pica' )                                : mpmathify( '6' ),
    ( 'inch',                       'point' )                               : mpmathify( '72' ),
    ( 'inch',                       'twip' )                                : mpmathify( '1440' ),
    ( 'jack',                       'tablespoon' )                          : mpmathify( '5' ),
    ( 'jennie',                     'liter' )                               : mpmathify( '0.5' ),
    ( 'jeroboam',                   'liter' )                               : mpmathify( '3.0' ),  # some French regions use 4.5
    ( 'jigger',                     'pony' )                                : mpmathify( '2' ),
    ( 'joule',                      'electronvolt' )                        : mpmathify( '6.24150974e18' ),
    ( 'joule',                      'erg' )                                 : mpmathify( '1.0e7' ),
    ( 'joule',                      'kilogram-meter^2/second^2' )           : mpmathify( '1' ),
    ( 'joule/second',               'watt' )                                : mpmathify( '1' ),
    ( 'jupiter_day',                'day' )                                 : mpmathify( '0.41354' ),
    ( 'jupiter_mass',               'gram' )                                : mpmathify( '1.8987e30' ),
    ( 'jupiter_radius',             'meter' )                               : mpmathify( '7.1492e7' ),
    ( 'jupiter_year',               'year' )                                : mpmathify( '11.862615' ),
    ( 'ken',                        'inch' )                                : mpmathify( '83.4' ),
    ( 'kenning',                    'imperial_peck' )                       : mpmathify( '2' ),
    ( 'kilderkin',                  'firkin' )                              : mpmathify( '2' ),
    ( 'kip',                        'pound' )                               : mpmathify( '1000' ),
    ( 'kovac',                      'wolverton' )                           : mpmathify( '10' ),
    ( 'lambert',                    'candela/meter^2' )                     : fdiv( 10000, pi ),
    ( 'league',                     'mile' )                                : mpmathify( '3' ),
    ( 'library_of_congress',        'byte' )                                : mpmathify( '1.0e13' ),
    ( 'light-second',               'meter' )                               : mpmathify( speedOfLight ),
    ( 'light-year',                 'light-second' )                        : mpmathify( '31557600' ),
    ( 'link',                       'inch' )                                : mpmathify( '7.92' ),
    ( 'liter',                      'ngogn' )                               : mpmathify( '86.2477899004' ),
    ( 'long_cubit',                 'inch' )                                : mpmathify( '21' ),
    ( 'long_hundred',               'unity' )                               : mpmathify( '120' ),
    ( 'long_reed',                  'foot' )                                : mpmathify( '10.5' ),
    ( 'lunar_day',                  'minute' )                              : mpmathify( '1490' ),
    ( 'lustrum',                    'year' )                                : mpmathify( '5' ),
    ( 'lux',                        'lumen/meter^2' )                       : mpmathify( '1' ),
    ( 'lux',                        'nox' )                                 : mpmathify( '1000' ),
    ( 'mach',                       'meter/second' )                        : mpmathify( '295.0464' ),
    ( 'magnum',                     'liter' )                               : mpmathify( '1.5' ),
    ( 'marathon',                   'yard' )                                : mpmathify( '46145' ),
    ( 'marie_jeanne',               'liter' )                               : mpmathify( '2.25' ),
    ( 'mars_day',                   'day' )                                 : mpmathify( '1.02595675' ),
    ( 'mars_year',                  'year' )                                : mpmathify( '1.8808476' ),
    ( 'martin',                     'kovac' )                               : mpmathify( '100' ),
    ( 'maxwell',                    'gauss*centimeter^2' )                  : mpmathify( '1' ),
    ( 'melchior',                   'liter' )                               : mpmathify( '18.0' ),
    ( 'melchizedek',                'liter' )                               : mpmathify( '30.0' ),
    ( 'mercury_day',                'day' )                                 : mpmathify( '58.6462' ),
    ( 'mercury_year',               'year' )                                : mpmathify( '0.2408467' ),
    ( 'meter',                      'angstrom' )                            : mpmathify( '1.0e10' ),
    ( 'meter',                      'kyu' )                                 : mpmathify( '4000' ),
    ( 'meter',                      'micron' )                              : mpmathify( '1.0e6' ),
    ( 'meter/second',               'kine' )                                : mpmathify( '100' ),
    ( 'meter/second',               'knot' )                                : mpmathify( '1.943844492' ),
    ( 'methuselah',                 'liter' )                               : mpmathify( '6.0' ),
    ( 'mile',                       'foot' )                                : mpmathify( '5280' ),
    ( 'mile/hour',                  'kilometer/hour' )                      : mpmathify( '1.609344' ),
    ( 'mile/hour',                  'meter/second' )                        : mpmathify( '0.44704' ),
    ( 'million',                    'unity' )                               : mpmathify( '1.0e6' ),
    ( 'mingo',                      'clarke' )                              : mpmathify( '10' ),
    ( 'minute',                     'second' )                              : mpmathify( '60' ),
    ( 'mmHg',                       'pascal' )                              : mpmathify( '133.3224' ),        # approx.
    ( 'month',                      'day' )                                 : mpmathify( '30' ),
    ( 'mordechai',                  'liter' )                               : mpmathify( '9.0' ),
    ( 'morgen',                     'are' )                                 : mpmathify( '85.6532' ),
    ( 'muon_mass',                  'dalton' )                              : mpmathify( '0.1134289267' ),
    ( 'nail',                       'inch' )                                : mpmathify( '2.25' ),
    ( 'nat',                        'joule/kelvin' )                        : mpmathify( '1.380650e-23' ),
    ( 'nautical_mile',              'meter' )                               : mpmathify( '1852' ),
    ( 'nebuchadnezzar',             'liter' )                               : mpmathify( '15.0' ),
    ( 'neptune_day',                'day' )                                 : mpmathify( '0.768' ),
    ( 'neptune_year',               'year' )                                : mpmathify( '164.79132' ),
    ( 'neutron_mass',               'dalton' )                              : mpmathify( '1.00866491600' ),
    ( 'newton',                     'dyne' )                                : mpmathify( '1.0e5' ),
    ( 'newton',                     'joule/meter' )                         : mpmathify( '1' ),
    ( 'newton',                     'pond' )                                : mpmathify( '101.97161298' ),
    ( 'newton',                     'poundal' )                             : mpmathify( '7.233013851' ),
    ( 'newton-second/meter^2',      'pascal' )                              : mpmathify( '1' ),
    ( 'newton/meter^2',             'pascal' )                              : mpmathify( '1' ),
    ( 'ngogn',                      'farshimmelt_ngogn' )                   : mpmathify( '1.0e5' ),
    ( 'ngogn',                      'furshlugginer_ngogn' )                 : mpmathify( '1.0e-6' ),
    ( 'nibble',                     'bit' )                                 : mpmathify( '4' ),
    ( 'nit',                        'apostilb' )                            : pi,
    ( 'nit',                        'candela/meter^2' )                     : mpmathify( '1' ),
    ( 'nit',                        'lambert' )                             : fdiv( pi, 10000 ),
    ( 'nonillion',                  'unity' )                               : mpmathify( '1.0e30' ),
    ( 'novemdecillion',             'unity' )                               : mpmathify( '1.0e60' ),
    ( 'nyp',                        'bit' )                                 : mpmathify( '2' ),
    ( 'octant',                     'degree' )                              : mpmathify( '45' ),
    ( 'octillion',                  'unity' )                               : mpmathify( '1.0e27' ),
    ( 'octodecillion',              'unity' )                               : mpmathify( '1.0e57' ),
    ( 'oersted',                    'ampere/meter' )                        : mpmathify( '79.5774715' ),
    ( 'ohm',                        '1/siemens' )                           : mpmathify( '1' ),
    ( 'ohm',                        'abohm' )                               : mpmathify( '1e9' ),
    ( 'ohm',                        'german_mile' )                         : mpmathify( '57.44' ),
    ( 'ohm',                        'jacobi' )                              : mpmathify( '0.6367' ),
    ( 'ohm',                        'joule-second/coulomb^2' )              : mpmathify( '1' ),
    ( 'ohm',                        'joule/second-ampere^2' )               : mpmathify( '1' ),
    ( 'ohm',                        'kilogram-meter^2/second^3-ampere^2' )  : mpmathify( '1' ),
    ( 'ohm',                        'matthiessen' )                         : mpmathify( '13.59' ),
    ( 'ohm',                        'meter^2-kilogram/second-coulomb^2' )   : mpmathify( '1' ),
    ( 'ohm',                        'second/farad' )                        : mpmathify( '1' ),
    ( 'ohm',                        'varley' )                              : mpmathify( '25.61' ),
    ( 'ohm',                        'volt/ampere' )                         : mpmathify( '1' ),
    ( 'ohm',                        'watt/ampere^2' )                       : mpmathify( '1' ),
    ( 'oil_barrel',                 'gallon' )                              : mpmathify( '42' ),
    ( 'ounce',                      'gram' )                                : mpmathify( '28.349523125' ),
    ( 'oword',                      'bit' )                                 : mpmathify( '128' ),
    ( 'parsec',                     'light-year' )                          : mpmathify( '3.261563776971' ),
    ( 'pascal',                     'barye' )                               : mpmathify( '10' ),
    ( 'pascal-second',              'poise' )                               : mpmathify( '10' ),
    ( 'peck',                       'dry_gallon' )                          : mpmathify( '2' ),
    ( 'perch',                      'foot' )                                : mpmathify( '16.5' ),
    ( 'pferdestarke',               'watt' )                                : mpmathify( '735.49875' ),
    ( 'pfund',                      'gram' )                                : mpmathify( '500' ),
    ( 'phot',                       'lux' )                                 : mpmathify( '10000' ),
    ( 'piccolo',                    'liter' )                               : mpmathify( '0.1875' ),
    ( 'pieze',                      'pascal' )                              : mpmathify( '1000' ),
    ( 'planck_area',                'square_meter' )                        : mpmathify( '2.6121003e-70' ),
    ( 'planck_charge',              'coulomb' )                             : mpmathify( '1.875545956e-18' ),
    ( 'planck_energy',              'joule' )                               : mpmathify( '1.956e9' ),
    ( 'planck_length',              'meter' )                               : mpmathify( '1.616199e-35' ),
    ( 'planck_time',                'second' )                              : mpmathify( '5.39106e-44' ),
    ( 'planck_volume',              'cubic_meter' )                         : mpmathify( '4.22419e-105' ),
    ( 'pluto_day',                  'day' )                                 : mpmathify( '6.3867' ),
    ( 'pluto_year',                 'year' )                                : mpmathify( '247.92065' ),
    ( 'pointangle',                 'degree' )                              : fdiv( 360, 32 ),
    ( 'poncelet',                   'watt' )                                : mpmathify( '980.665' ),
    ( 'pony',                       'dram' )                                : mpmathify( '6' ),
    ( 'potrzebie',                  'farshimmelt_potrzebie' )               : mpmathify( '1.0e5' ),
    ( 'potrzebie',                  'furshlugginer_potrzebie' )             : mpmathify( '1.0e-6' ),
    ( 'potrzebie',                  'meter' )                               : mpmathify( '0.002263348517438173216473' ),  # see Mad #33
    ( 'pottle',                     'imperial_quart' )                      : mpmathify( '2' ),
    ( 'pound',                      'grain' )                               : mpmathify( '7000' ),
    ( 'pound',                      'ounce' )                               : mpmathify( '16' ),
    ( 'pound',                      'sheet' )                               : mpmathify( '700' ),
    ( 'proton_mass',                'dalton' )                              : mpmathify( '1.007276466812' ),
    ( 'proton_mass',                'gram' )                                : mpmathify( '1.6726218e-24' ),
    ( 'psi',                        'pascal' )                              : mpmathify( '6894.757' ),        # approx.
    ( 'quadrant',                   'degree' )                              : mpmathify( '90' ),
    ( 'quadrillion',                'unity' )                               : mpmathify( '1.0e15' ),
    ( 'quart',                      'cup' )                                 : mpmathify( '4' ),
    ( 'quart',                      'liter' )                               : mpmathify( '0.946352946' ),
    ( 'quart',                      'pint' )                                : mpmathify( '2' ),
    ( 'quattuordecillion',          'unity' )                               : mpmathify( '1.0e45' ),
    ( 'quindecillion',              'unity' )                               : mpmathify( '1.0e48' ),
    ( 'quintant',                   'degree' )                              : mpmathify( '72' ),
    ( 'quintillion',                'unity' )                               : mpmathify( '1.0e18' ),
    ( 'qword',                      'bit' )                                 : mpmathify( '64' ),
    ( 'radian',                     'centrad' )                             : mpmathify( '100' ),
    ( 'radian',                     'degree' )                              : fdiv( 180, pi ),
    ( 'reed',                       'foot' )                                : mpmathify( '9' ),
    ( 'rehoboam',                   'liter' )                               : mpmathify( '4.5' ),
    ( 'rod',                        'foot' )                                : mpmathify( '16.5' ),
    ( 'rood',                       'square_yard' )                         : mpmathify( '1210' ),
    ( 'rope',                       'foot' )                                : mpmathify( '20' ),
    ( 'rutherford',                 'becquerel' )                           : mpmathify( '1.0e6' ),
    ( 'rydberg',                    'joule' )                               : mpmathify( '2.179872e-18' ),
    ( 'salmanazar',                 'liter' )                               : mpmathify( '9.0' ),
    ( 'saturn_day',                 'day' )                                 : mpmathify( '0.4375' ),
    ( 'saturn_year',                'year' )                                : mpmathify( '29.447498' ),
    ( 'score',                      'unity' )                               : mpmathify( '20' ),
    ( 'scruple',                    'minim' )                               : mpmathify( '20' ),
    ( 'second',                     'jiffy' )                               : mpmathify( '100' ),
    ( 'second',                     'shake' )                               : mpmathify( '1.0e8' ),
    ( 'second',                     'svedberg' )                            : mpmathify( '1.0e13' ),
    ( 'section',                    'acre' )                                : mpmathify( '640' ),
    ( 'septendecillion',            'unity' )                               : mpmathify( '1.0e54' ),
    ( 'septillion',                 'unity' )                               : mpmathify( '1.0e24' ),
    ( 'sexdecillion',               'unity' )                               : mpmathify( '1.0e51' ),
    ( 'sextant',                    'degree' )                              : mpmathify( '60' ),
    ( 'sextillion',                 'unity' )                               : mpmathify( '1.0e21' ),
    ( 'shock',                      'unity' )                               : mpmathify( '60' ),
    ( 'sidereal_day',               'second' )                              : mpmathify( '86164.09054' ),
    ( 'sidereal_day',               'sidereal_hour' )                       : mpmathify( '24' ),
    ( 'sidereal_hour',              'sidereal_minute' )                     : mpmathify( '60' ),
    ( 'sidereal_minute',            'sidereal_second' )                     : mpmathify( '60' ),
    ( 'sidereal_month',             'day' )                                 : mpmathify( '27.321661' ),
    ( 'sidereal_year',              'day' )                                 : mpmathify( '365.256360417' ),
    ( 'siemens',                    'ampere/volt' )                         : mpmathify( '1' ),
    ( 'siemens',                    'kilogram-meter^2/second^3-ampere^2' )  : mpmathify( '1' ),
    ( 'siemens',                    'statsiemens' )                         : mpmathify( '898755178736.5' ),
    ( 'sievert',                    'rem' )                                 : mpmathify( '100' ),
    ( 'siriometer',                 'astronomical_unit' )                   : mpmathify( '1.0e6' ),
    ( 'skein',                      'foot' )                                : mpmathify( '360' ),
    ( 'skot',                       'bril' )                                : mpmathify( '1.0e4' ),
    ( 'skot',                       'lambert' )                             : mpmathify( '1.0e7' ),
    ( 'slug',                       'pound' )                               : mpmathify( '32.174048556' ),
    ( 'smoot',                      'inch' )                                : mpmathify( '67' ),
    ( 'solar_luminosity',           'watt' )                                : mpmathify( '3.826e26' ),
    ( 'solar_mass',                 'gram' )                                : mpmathify( '1.989e33' ),
    ( 'solar_radius',               'meter' )                               : mpmathify( '6.9599e8' ),
    ( 'solomon',                    'liter' )                               : mpmathify( '20.0' ),
    ( 'sovereign',                  'liter' )                               : mpmathify( '25.0' ),
    ( 'span',                       'inch' )                                : mpmathify( '9' ),
    ( 'speed_of_light',             'meter/second' )                        : mpmathify( speedOfLight ),
    ( 'sphere',                     'steradian' )                           : fmul( 4, pi ),
    ( 'square_arcminute',           'square_arcsecond' )                    : mpmathify( '3600' ),
    ( 'square_degree',              'square_arcminute' )                    : mpmathify( '3600' ),
    ( 'square_meter',               'barn' )                                : mpmathify( '1.0e28' ),
    ( 'square_meter',               'outhouse' )                            : mpmathify( '1.0e34' ),
    ( 'square_meter',               'shed' )                                : mpmathify( '1.0e52' ),
    ( 'square_octant',              'square_degree' )                       : mpmathify( '2025' ),
    ( 'square_quadrant',            'square_degree' )                       : mpmathify( '8100' ),
    ( 'square_sextant',             'square_degree' )                       : mpmathify( '3600' ),
    ( 'square_yard',                'square_foot' )                         : mpmathify( '9' ),
    ( 'standard',                   'liter' )                               : mpmathify( '0.75' ),
    ( 'standard_gravity',           'galileo' )                             : mpmathify( '980.6650' ),
    ( 'standard_gravity',           'meter/second^2' )                      : mpmathify( '9.80665' ),
    ( 'statcoulomb',                'coulomb' )                             : mpmathify( '3.335641e-10' ),  # 0.1A*m/c ), approx.
    ( 'statcoulomb',                'franklin' )                            : mpmathify( '1' ),
    ( 'stathenry',                  'henry' )                               : mpmathify( '898755178740' ),
    ( 'statmho',                    'siemens' )                             : mpmathify( '8.99e11' ),
    ( 'statohm',                    'ohm' )                                 : mpmathify( '898755178740' ),
    ( 'statvolt',                   'volt' )                                : fdiv( mpf( speedOfLight ), mpf( '1.0e6' ) ),
    ( 'steradian',                  'square_degree' )                       : power( fdiv( 180, pi ), 2 ),
    ( 'steradian',                  'square_grad' )                         : power( fdiv( 200, pi ), 2 ),
    ( 'sthene',                     'newton' )                              : mpmathify( '1000' ),
    ( 'stilb',                      'candela/meter^2' )                     : mpmathify( '10000' ),
    ( 'stone',                      'pound' )                               : mpmathify( '14' ),
    ( 'stone_us',                   'pound' )                               : mpmathify( '12.5' ),
    ( 'strike',                     'imperial_bushel' )                     : mpmathify( '2' ),
    ( 'tablespoon',                 'teaspoon' )                            : mpmathify( '3' ),
    ( 'tau_mass',                   'dalton' )                              : mpmathify( '1.90749' ),
    ( 'teaspoon',                   'dash' )                                : mpmathify( '8' ),
    ( 'teaspoon',                   'pinch' )                               : mpmathify( '16' ),
    ( 'teaspoon',                   'smidgen' )                             : mpmathify( '32' ),
    ( 'ten',                        'unity' )                               : mpmathify( '10' ),
    ( 'tenth',                      'liter' )                               : mpmathify( '0.378' ),
    ( 'tesla',                      'gauss' )                               : mpmathify( '10000' ),
    ( 'tesla',                      'kilogram/ampere-second^2' )            : mpmathify( '1' ),
    ( 'tesla',                      'weber/meter^2' )                       : mpmathify( '1' ),
    ( 'thousand',                   'unity' )                               : mpmathify( '100' ),
    ( 'ton',                        'pound' )                               : mpmathify( '2000' ),
    ( 'tonne',                      'gram' )                                : mpmathify( '1.0e6' ),
    ( 'ton_of_TNT',                 'joule' )                               : mpmathify( '4.184e9' ),
    ( 'torr',                       'mmHg' )                                : mpmathify( '1' ),
    ( 'township',                   'acre' )                                : mpmathify( '23040' ),
    ( 'tredecillion',               'unity' )                               : mpmathify( '1.0e42' ),
    ( 'trillion',                   'unity' )                               : mpmathify( '1.0e12' ),
    ( 'trit',                       'nat' )                                 : log( 3 ),
    ( 'triton_mass',                'dalton' )                              : mpmathify( '3.0155007134' ),
    ( 'tropical_year',              'day' )                                 : mpmathify( '365.24219' ),
    ( 'troy_ounce',                 'gram' )                                : mpmathify( '31.1034768' ),
    ( 'troy_pound',                 'pound' )                               : mpmathify( '12' ),
    ( 'tryte',                      'trit' )                                : mpmathify( '6' ),   # as defined by the Setun computer
    ( 'undecillion',                'unity' )                               : mpmathify( '1.0e36' ),
    ( 'unity',                      'billionth' )                           : mpmathify( '1.0e9' ),
    ( 'unity',                      'decillionth' )                         : mpmathify( '1.0e33' ),
    ( 'unity',                      'half' )                                : mpmathify( '2' ),
    ( 'unity',                      'millionth' )                           : mpmathify( '1.0e6' ),
    ( 'unity',                      'nonillionth' )                         : mpmathify( '1.0e30' ),
    ( 'unity',                      'octillionth' )                         : mpmathify( '1.0e27' ),
    ( 'unity',                      'percent' )                             : mpmathify( '100' ),
    ( 'unity',                      'quadrillionth' )                       : mpmathify( '1.0e15' ),
    ( 'unity',                      'quarter' )                             : mpmathify( '4' ),
    ( 'unity',                      'quintillionth' )                       : mpmathify( '1.0e18' ),
    ( 'unity',                      'septillionth' )                        : mpmathify( '1.0e24' ),
    ( 'unity',                      'sextillionth' )                        : mpmathify( '1.0e21' ),
    ( 'unity',                      'tenth' )                               : mpmathify( '10' ),
    ( 'unity',                      'third' )                               : mpmathify( '3' ),
    ( 'unity',                      'trillionth' )                          : mpmathify( '1.0e12' ),
    ( 'uranus_day',                 'day' )                                 : mpmathify( '0.65' ),
    ( 'uranus_year',                'year' )                                : mpmathify( '84.016846' ),
    ( 'venus_day',                  'day' )                                 : mpmathify( '243.01' ),
    ( 'venus_year',                 'year' )                                : mpmathify( '0.61519726' ),
    ( 'vigintillion',               'unity' )                               : mpmathify( '1.0e63' ),
    ( 'virgate',                    'bovate' )                              : mpmathify( '30' ),
    ( 'volt',                       'abvolt' )                              : mpmathify( '1.0e8' ),
    ( 'volt-ampere',                'watt' )                                : mpmathify( '1' ),
    ( 'von_klitzing_constant',      'ohm' )                                 : mpmathify( '25812.807557' ),
    ( 'watt',                       'erg/second' )                          : mpmathify( '1.0e7' ),
    ( 'watt',                       'kilogram-meter^2/second^3' )           : mpmathify( '1' ),
    ( 'watt',                       'lusec' )                               : mpmathify( '7500' ),
    ( 'watt',                       'newton-meter/second' )                 : mpmathify( '1' ),
    ( 'watt-second',                'joule' )                               : mpmathify( '1' ),
    ( 'weber',                      'maxwell' )                             : mpmathify( '1.0e8' ),
    ( 'weber',                      'tesla*meter^2' )                       : mpmathify( '1' ),
    ( 'weber',                      'unit_pole' )                           : mpmathify( '7957747.154594' ),
    ( 'weber',                      'volt-second' )                         : mpmathify( '1' ),
    ( 'week',                       'day' )                                 : mpmathify( '7' ),
    ( 'wey',                        'pound' )                               : mpmathify( '252' ),
    ( 'wine_barrel',                'wine_gallon' )                         : mpmathify( '31.5' ),
    ( 'wine_butt',                  'wine_gallon' )                         : mpmathify( '126' ),
    ( 'wine_gallon',                'gallon' )                              : mpmathify( '1' ),
    ( 'wine_hogshead',              'gallon' )                              : mpmathify( '63' ),
    ( 'wine_tun',                   'gallon' )                              : mpmathify( '252' ),
    ( 'wine_tun',                   'puncheon' )                            : mpmathify( '3' ),
    ( 'wine_tun',                   'rundlet' )                             : mpmathify( '14' ),
    ( 'wine_tun',                   'tierce' )                              : mpmathify( '6' ),
    ( 'wine_tun',                   'wine_pipe' )                           : mpmathify( '2' ),
    ( 'wood',                       'martin' )                              : mpmathify( '100' ),
    ( 'word',                       'bit' )                                 : mpmathify( '16' ),
    ( 'yard',                       'foot' )                                : mpmathify( '3' ),
    ( 'year',                       'day' )                                 : mpmathify( '365.25' ),   # Julian year = 365 and 1/4 days
    ( 'zentner',                    'gram' )                                : mpmathify( '50000' ),

    #( 'volt-ampere-second',        'joule' )                                : mpmathify( '1' ),

}

