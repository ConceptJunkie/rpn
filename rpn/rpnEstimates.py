#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnEstimates.py
# //
# //  RPN command-line calculator estimate table declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import mpmathify


# //******************************************************************************
# //
# //  accelerationTable
# //
# //  meters/second^2 : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28acceleration%29
# //
# //******************************************************************************

accelerationTable = {
    mpmathify( '0.0058' )     : 'the acceleration of the Earth due to the Sun\'s gravity',
    mpmathify( '1.62' )       : 'the Moon\'s gravity at its equator',
    mpmathify( '4.3' )        : 'the acceleration going from 0-60 mph in 6.4 seconds (Saab 9-5 Hirsch)',
    mpmathify( '9.80665' )    : 'the Earth\'s gravity',
    mpmathify( '15.2' )       : 'the acceleration going from 0-100 kph in 2.4 seconds (Bugatti Veyron)',
    mpmathify( '29' )         : 'the maximum acceleration during launch and re-entry of the Space Shuttle',
    mpmathify( '70.6' )       : 'the maximum acceleration of Apollo 6 during re-entry',
    mpmathify( '79' )         : 'the acceleration of an F-16 aircraft pulling out of a dive',
    mpmathify( '147' )        : 'the acceleration of an explosive seat ejection from an aircraft',
    mpmathify( '2946' )       : 'the acceleration of a soccer ball being kicked',
    mpmathify( '29460' )      : 'the acceleration of a baseball struck by a bat',
    mpmathify( '3.8e6' )      : 'the surface gravity of white dwarf Sirius B',
    mpmathify( '1.9e9' )      : 'the mean acceleration of a proton in the Large Hadron Collider',
    mpmathify( '7.0e12' )     : 'the maximum surface gravity of a neutron star',
    mpmathify( '9.149e21' )   : 'classical (Bohr model) acceleration of an electron around a H nucleus',
    mpmathify( '5.561e51' )   : 'Planck acceleration',
}


# //******************************************************************************
# //
# //  amountOfSubstanceTable
# //
# //  radians : description
# //
# //
# //
# //******************************************************************************

amountOfSubstanceTable = {
    mpmathify( '1' )  : 'a mole... that\'s all we got',
}


# //******************************************************************************
# //
# //  angleTable
# //
# //  radians : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28angular_velocity%29
# //
# //******************************************************************************

angleTable = {
    mpmathify( '8.405e-16' )  : 'the angle the Sun revolves around the galactic core in a second',
    mpmathify( '8.03e-10' )   : 'the angle Pluto revolves around the Sun in a second',
    mpmathify( '1.68e-8' )    : 'the angle Jupiter revolves around the Sun in a second',
    mpmathify( '1.99e-7' )    : 'the angle the Earth revolves around the Sun in a second',
    mpmathify( '7.27e-5' )    : 'the angle the Earth rotates in a second',
    mpmathify( '1.454e-4' )  : 'the angle a clock hour hand moves in a second',
    mpmathify( '1.7453e-3' )  : 'the angle a clock minute hand moves in a second',
    mpmathify( '0.10471976' ) : 'the angle a clock second hand moves in a second',
    mpmathify( '3.4906585' )  : 'the angle a long-playing record rotates in one second',
    mpmathify( '94' )         : 'the angle the spin cycle of washing machine rotates in one second',
    mpmathify( '753.982237' ) : 'the angle a 7200-rpm harddrive rotates in a second',
}


# //******************************************************************************
# //
# //  areaTable
# //
# //  meters^2 : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28area%29
# //
# //******************************************************************************

areaTable = {
    mpmathify( '2.6121e-70' ) : 'the Planck area',
    mpmathify( '1.0e-52' )    : 'one shed',
    mpmathify( '1.0e-48' )    : 'one square yoctometer',
    mpmathify( '1.0e-42' )    : 'one square zeptometer',
    mpmathify( '1.0e-36' )    : 'one square attometer',
    mpmathify( '1.0e-28' )    : 'one barn, roughly the cross-sectional area of a uranium nucleus',
    mpmathify( '1.0e-24' )    : 'one square picometer',
    mpmathify( '1.0e-18' )    : 'one square nanometer',
    mpmathify( '1.0e-12' )    : 'one square micron, the surface area of an E. coli bacterium',
    mpmathify( '1.0e-10' )    : 'the surface area of a human red blood cell',
    mpmathify( '7.1684e-9' )  : 'the area of a single pixel at 300 dpi resolution',
    mpmathify( '6.4516e-8' )  : 'the area of a single pixel at 100 dpi resolution',
    mpmathify( '1.9635e-7' )  : 'the cross-sectional area of a 0.5mm pencil lead',
    mpmathify( '2.9e-4' )     : 'the area of one side of a U.S. penny',
    mpmathify( '4.6e-3' )     : 'the area of the face of a credit card',
    mpmathify( '0.009677' )   : 'the area of a 3x5 inch index card',
    mpmathify( '0.06032246' ) : 'the area of American Letter size paper (8.5x11")',
    mpmathify( '0.181' )      : 'the surface area of a basketball (diameter 24 cm)',
    mpmathify( '1.73' )       : 'the average body surface area of a human',
    mpmathify( '261' )        : 'the area of a standard tennis court',
    mpmathify( '1250' )       : 'the area of an Olympic-size swimming pool',
    mpmathify( '4046.856' )   : 'one acre',
    mpmathify( '5400' )       : 'the size of an American football field',
    mpmathify( '22074' )      : 'the area of a Manhattan city block',
    mpmathify( '5.3e4' )      : 'the area of the base of the Great Pyramid of Giza',
    mpmathify( '4.4e5' )      : 'the area of Vatican City',
    mpmathify( '6.0e5' )      : 'the total floor area of the Pentagon',
    mpmathify( '2.0e6' )      : 'the area of Monaco (country ranked 192nd by area)',
    mpmathify( '2589988.11' ) : 'one square mile',
    mpmathify( '5.95e7' )     : 'the area of Manhattan Island',
    mpmathify( '1.29e9' )     : 'the area of Los Angeles, California, USA',
    mpmathify( '1.8e9' )      : 'the surface area of a typical neutron star',
    mpmathify( '2.188e9' )    : 'the area of Tokyo',
    mpmathify( '1.1e10' )     : 'the area of Jamaica',
    mpmathify( '6.887e10' )   : 'the area of Lake Victoria',
    mpmathify( '8.4e10' )     : 'the area of Austria',
    mpmathify( '1.0e11' )     : 'the area of South Korea',
    mpmathify( '3.0e11' )     : 'the area of Italy',
    mpmathify( '3.57e11' )    : 'the area of Germany',
    mpmathify( '3.779e11' )   : 'the area of Japan',
    mpmathify( '5.1e11' )     : 'the area of Spain',
    mpmathify( '7.8e11' )     : 'the area of Turkey',
    mpmathify( '1.0e12' )     : 'the area of Egypt (country ranked 29th by area)',
    mpmathify( '7.74e12' )    : 'the area of Australia (country ranked 6th by area)',
    mpmathify( '9.0e12' )     : 'the area of the largest extent of the Roman Empire',
    mpmathify( '1.0e13' )     : 'the area of Canada (including water)',
    mpmathify( '1.4e13' )     : 'the area of Antarctica',
    mpmathify( '1.7e13' )     : 'the area of Russia (country ranked 1st by area)',
    mpmathify( '3.0e13' )     : 'the area of Africa',
    mpmathify( '3.6e13' )     : 'the area of largest extent of the British Empire[citation needed]',
    mpmathify( '3.8e13' )     : 'the surface area of the Moon',
    mpmathify( '7.7e13' )     : 'the area of the Atlantic Ocean',
    mpmathify( '1.44e14' )    : 'the surface area of Mars',
    mpmathify( '1.5e14' )     : 'the land area of Earth',
    mpmathify( '1.56e14' )    : 'the area of the Pacific Ocean',
    mpmathify( '3.6e14' )     : 'the water area of Earth',
    mpmathify( '5.1e14' )     : 'the total surface area of Earth',
    mpmathify( '7.6e15' )     : 'the surface area of Neptune',
    mpmathify( '4.3e16' )     : 'the surface area of Saturn',
    mpmathify( '6.1e16' )     : 'the surface area of Jupiter',
    mpmathify( '4.6e17' )     : 'the area swept by the Moon\'s orbit of Earth',
    mpmathify( '6.1e18' )     : 'the surface area of the Sun',
    mpmathify( '1.1e22' )     : 'the area swept by Mercury\'s orbit around the Sun',
    mpmathify( '3.7e22' )     : 'the area swept by Venus\' orbit around the Sun',
    mpmathify( '7.1e22' )     : 'the area swept by Earth\'s orbit around the Sun',
    mpmathify( '1.6e23' )     : 'the area swept by Mars\' orbit around the Sun',
    mpmathify( '2.81e23' )    : 'the surface area of a Dyson sphere with a radius of 1 AU',
    mpmathify( '1.9e24' )     : 'the area swept by Jupiter\'s orbit around the Sun',
    mpmathify( '6.4e24' )     : 'the area swept by Saturn\'s orbit around the Sun',
    mpmathify( '8.5e24' )     : 'the surface area of the red supergiant star Betelgeuse',
    mpmathify( '2.4e25' )     : 'the surface area of the largest known star, the Hypergiant VY Canis Majoris',
    mpmathify( '2.6e25' )     : 'the area swept by Uranus\' orbit around the Sun',
    mpmathify( '6.4e25' )     : 'the area swept by Neptune\'s orbit around the Sun',
    mpmathify( '1.1e26' )     : 'the area swept by Pluto\'s orbit around the Sun',
    mpmathify( '2.0e32' )     : 'the approximate surface area of an Oort Cloud',
    mpmathify( '3.0e32' )     : 'the approximate surface area of a Bok globule',
    mpmathify( '7.0e41' )     : 'the approximate area of Milky Way\'s galactic disk',
}


# //******************************************************************************
# //
# //  capacitanceTable
# //
# //  farads : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28capacitance%29
# //
# //******************************************************************************

capacitanceTable = {
    mpmathify( '2.0e-15' )    : 'the gate capacitance of a MOS transistor, per micron of gate width',
    mpmathify( '3.0e-14' )    : 'the capacitance of a DRAM cell',
    mpmathify( '1.0e-13' )    : 'the capacitance of a small ceramic capacitor (100 fF)',
    mpmathify( '1.0e-12' )    : 'the capacitance of a small mica or PTFE capacitor (1 pF)',
    mpmathify( '4.0e-12' )    : 'the capacitive sensing of air-water-snow-ice (4 pF)',
    mpmathify( '5.0e-12' )    : 'the capacitance of a low condenser microphone (5 pF)',
    mpmathify( '4.5e-11' )    : 'a variable capacitor (45 pF)',
    mpmathify( '4.9e-11' )    : 'the capacitance of a yoga mat of TPE with relative permittivity of 4.5 and 8 mm thick sandwiched between two 1 dm^2 electrodes (49 pF)',
    mpmathify( '5.0e-11' )    : 'the capacitance of 1 m of Cat 5 network cable (between the two conductors of a twisted pair) (50 pF)',
    mpmathify( '1.0e-10' )    : 'the capacitance of the standard human body model (100 pF)',
    mpmathify( '1.0e-10' )    : 'the capacitance of 1 m of 50 ohm coaxial cable (between the inner and outer conductors) (100 pF)',
    mpmathify( '1.0e-10' )    : 'the capacitance of a high condenser microphone (100 pF)',
    mpmathify( '3.3e-10' )    : 'the capacitance of a variable capacitor (330 pF)',
    mpmathify( '1.0e-9' )     : 'the capacitance of a typical leyden jar (1 nF)',
    mpmathify( '1.0e-7' )     : 'the capacitance of a small aluminum electrolytic capacitor (100 nF)',
    mpmathify( '8.2e-7' )     : 'the capacitance of a large mica and PTFE capacitor (820 nF)',
    mpmathify( '1.0e-4' )     : 'the capacitance of a large ceramic capacitor (100 uF)',
    mpmathify( '6.8e-3' )     : 'the capacitance of a small electric double layer supercapacitor (6.8 mF)',
    mpmathify( '1.0' )        : 'the Earth-ionosphere capacitance (1 F)',
    mpmathify( '1.5' )        : 'the capacitance of a large aluminum electrolytic capacitor (1.5 F)',
    mpmathify( '5.0e3' )      : 'the capacitance of a large electric double-layer supercapacitor (5000 F)',
}


# //******************************************************************************
# //
# //  catalysisTable
# //
# //  katals : description
# //
# //******************************************************************************

catalysisTable = {
    mpmathify( '1.66667e-8' ) : 'the enzyme_unit, the former standard unit of catalytic activity',
    mpmathify( '1.0' )        : 'the katal, the standard SI derived unit of catalytic activity (= 1 mole/second)',
}


# //******************************************************************************
# //
# //  chargeTable
# //
# //  coulombs : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28charge%29
# //
# //******************************************************************************

chargeTable = {
    mpmathify( '-5.34e-20' )  : 'the charge of down, strange and bottom quarks (-1/3 e)',
    mpmathify( '1.068e-19' )  : 'the charge of up, charm and top quarks (2/3 e)',
    mpmathify( '1.602e-19' )  : 'the elementary charge e, i.e. the negative charge on a single electron or the positive charge on a single proton',
    mpmathify( '1.9e-18' )    : 'the Planck charge',
    mpmathify( '1.473e-17' )  : 'the positive charge on a uranium nucleus (92 e)',
    mpmathify( '1.0e-15' )    : 'the charge on a typical dust particle',
    mpmathify( '1.0e-12' )    : 'the charge in typical microwave frequency capacitors',
    mpmathify( '1.0e-9' )     : 'the charge in typical radio frequency capacitors',
    mpmathify( '1.0e-6' )     : 'the charge in typical audio frequency capacitors, and the static electricity from rubbing materials together',
    mpmathify( '1.0e-3' )     : 'the charge in typical power supply capacitors',
    mpmathify( '1.0' )        : 'a 1 coulomb charge: two negative point charges of 1 C, placed one meter apart, would experience a repulsive force of 9 GN',
    mpmathify( '26' )         : 'the charge in a typical thundercloud (15 - 350 C)',
    mpmathify( '5.0e3' )      : 'the typical alkaline AA battery is about 5000 C, or ~ 1.4 Ah',
    mpmathify( '9.64e4' )     : 'the charge on one mole of electrons (Faraday constant)',
    mpmathify( '2.16e5' )     : 'a car battery charge',
    mpmathify( '1.07e7' )     : 'the charge needed to produce 1 kg of aluminum from bauxite in an electrolytic cell',
    mpmathify( '5.9e8' )      : 'the charge in the worl\'s largest battery bank (36 MWh), assuming 220VAC output',
}


# //******************************************************************************
# //
# //  constantTable
# //
# //  unities : description
# //
# //******************************************************************************

constantTable = {
}


# //******************************************************************************
# //
# //  currentTable
# //
# //  amperes : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28current%29
# //
# //******************************************************************************

currentTable = {
    mpmathify( '1.0e-5' )     : 'the minimum current necessary to cause death (by ventricular fibrillation when applied directly across the human heart)',
    mpmathify( '7.0e-3' )     : 'the current draw of a portable hearing aid (typically 1 mW at 1.4 V)',
    mpmathify( '3.0e-3' )     : 'the current draw of a cathode ray tube electron gun beam (1-5 mA)',
    mpmathify( '1.0e-2' )     : 'the current which through the hand to foot may cause a person to freeze and be unable to let go (10 mA)',
    mpmathify( '2.0e-2' )     : 'the deadly limit of current for skin contact (at 120-230 V)',
    mpmathify( '1.5e-1' )     : 'the current draw of a 230 V AC, 22-inch/56-centimeter portable television (35 W)',
    mpmathify( '1.66e-1' )    : 'the current draw of a typical 12 V motor vehicle instrument panel light',
    mpmathify( '2.9e-1' )     : 'the current draw of a 120 V AC, 22-inch/56-centimeter portable television (35 W)',
    mpmathify( '1.35' )       : 'the current draw of a Tesla coil, 0.76 meters (2 ft 6 in) high, at 200 kV and 270 kV peak',
    mpmathify( '2.1' )        : 'the current draw of a high power LED current (peak 2.7 A)',
    mpmathify( '5.0' )        : 'the current draw of a typical 12 V motor vehicle headlight (typically 60 W)',
    mpmathify( '16.67' )      : 'the current draw of a 120 V AC, Toaster, kettle (2 kW)',
    mpmathify( '38.33' )      : 'the current draw of a 120 V AC, Immersion heater (4.6 kW)',
    mpmathify( '120' )        : 'the current draw of a typical 12 V motor vehicle starter motor (typically 1-2 kW)',
    mpmathify( '166' )        : 'the current draw of a 400 V low voltage secondary side distribution transformer with primary 12 kV ; 200 kVA (up to 1000 kVA also common)',
    mpmathify( '2.0e3' )      : 'the current draw of a 10.5 kV secondary side from an electrical substation with primary 115 kV ; 63 MVA',
    mpmathify( '2.5e4' )      : 'the current draw of a Lorentz force can crusher',
    mpmathify( '1.00e5' )     : 'the low range of Birkeland current which creates the Earth\'s aurorae',
    mpmathify( '1.40e5' )     : 'the "Sq" current of one daytime vortex within the ionospheric dynamo region',
    mpmathify( '1.0e6' )      : 'the high range of Birkeland current which creates Earth\'s aurorae',
    mpmathify( '5.0e6' )      : 'the current of the flux tube between Jupiter and Io',
    mpmathify( '2.7e7' )      : 'the firing current of the Z machine at the Sandia National Laboratories',
    mpmathify( '2.56e8' )     : 'the current produced in explosive flux compression generator (VNIIEF laboratories, Russia)',
    mpmathify( '3.0e9' )      : 'the total current in the Sun\'s heliospheric current sheet',
    mpmathify( '3.0e18' )     : 'the current of a 2 kpc segment of the 50 kpc-long radio jet of the Seyfert galaxy 3C 303',
    mpmathify( '3.479e25' )   : 'the Planck current',
}


# //******************************************************************************
# //
# //  dataRateTable
# //
# //  bits/second : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28bit_rate%29
# //
# //******************************************************************************

# cdromspeed       75 2048 bytes / sec # For data CDs (mode1) 75 sectors are read
#                                      # each second with 2048 bytes per sector.
#                                      # Audio CDs do not have sectors, but
#                                      # people sometimes divide the bit rate by
#                                      # 75 and claim a sector length of 2352.
#                                      # Data CDs have a lower rate due to
#                                      # increased error correction overhead.
#                                      # There is a rarely used mode (mode2) with
#                                      # 2336 bytes per sector that has fewer
#                                      # error correction bits than mode1.
# cdaudiospeed      44.1 kHz 2*16 bits # CD audio data rate at 44.1 kHz with 2
#                                      # samples of sixteen bits each.
# dvdspeed                 1385 kB/s   # This is the "1x" speed of a DVD using
#                                      # constant linear velocity (CLV) mode.
#                                      # Modern DVDs may vary the linear velocity
#                                      # as they go from the inside to the
#                                      # outside of the disc.
#


dataRateTable = {
    mpmathify( '5.0e-2' )     : 'the bit rate for Project ELF which transmits 3-letter codes to U.S. nuclear submarines',
    mpmathify( '5.0e1' )      : 'the data rate for transmissions from GPS satellites',
    mpmathify( '5.6e1' )      : 'the data rate for a skilled operator in Morse code',
    mpmathify( '4.0e3' )      : 'the minimum data rate achieved for encoding recognizable speech (using special-purpose speech codecs)',
    mpmathify( '8.0e3' )      : 'the data rate of low-bitrate telephone quality',
    mpmathify( '3.2e4' )      : 'the data rate of MW quality and ADPCM voice in telephony',
    mpmathify( '5.6e4' )      : 'the data rate of 56kbit modem',
    mpmathify( '6.4e4' )      : 'the data rate of an ISDN B channel or best quality, uncompressed telephone line',
    mpmathify( '1.92e5' )     : 'the data rate for "nearly CD quality" for a file compressed in the MP3 format',
    mpmathify( '1.4112e6' )   : 'the data rate of CD audio (uncompressed, 16-bit samples x 44.1 kHz x 2 channels)',
    mpmathify( '1.536e6' )    : 'the data rate of 24 channels of telephone in the US, or a good VTC T1',
    mpmathify( '2.0e6' )      : 'the data rate of 30 channels of telephone audio or a Video Tele-Conference at VHS quality',
    mpmathify( '8.0e6' )      : 'the data rate of DVD quality video',
    mpmathify( '1.0e7' )      : 'the data rate of classic Ethernet: 10BASE2, 10BASE5, 10BASE-T',
    mpmathify( '1.0e7' )      : 'the data rate that the human retina transmits data to the brain, according to research',
    mpmathify( '2.7e7' )      : 'the data rate of HDTV quality video',
    mpmathify( '4.8e8' )      : 'the data rate of USB 2.0 High-Speed (interface signalling rate)',
    mpmathify( '7.86e8' )     : 'the data rate of FireWire IEEE 1394b-2002 S800',
    mpmathify( '9.5e8' )      : 'the data rate of a harddrive read, Samsung SpinPoint F1 HD103Uj',
    mpmathify( '1.0e9' )      : 'the data rate of Gigabit Ethernet',
    mpmathify( '1.067e9' )    : 'the data rate of Parallel ATA UDMA 6; conventional PCI 32 bit 33 MHz - 133 MB/s',
    mpmathify( '1.244e9' )    : 'the data rate of OC-24, a 1.244 Gbit/s SONET data channel',
    mpmathify( '1.5e9' )      : 'the data rate of SATA 1.5Gbit/s - First generation (interface signaling rate)',
    mpmathify( '3.0e9' )      : 'the data rate of SATA 3Gbit/s - Second generation (interface signaling rate)',
    mpmathify( '5.0e9' )      : 'the data rate of USB 3.0 SuperSpeed',
    mpmathify( '6.0e9' )      : 'the data rate of SATA 6Gbit/s - Third generation (interface signaling rate)',
    mpmathify( '8.533e9' )    : 'the data rate of PCI-X 64 bit 133 MHz - 1,067 MB/s',
    mpmathify( '9.953e9' )    : 'the data rate of OC-192, a 9.953 Gbit/s SONET data channel',
    mpmathify( '1.0e10' )     : 'the data rate of the Thunderbolt interface standard',
    mpmathify( '1.0e10' )     : 'the data rate of 10 Gigabit Ethernet',
    mpmathify( '1.0e10' )     : 'the data rate of USB 3.1 SuperSpeed 10 Gbit/s',
    mpmathify( '3.9813e10' )  : 'the data rate of OC-768, a 39.813 Gbit/s SONET data channel, the fastest in current use',
    mpmathify( '4.0e10' )     : 'the data rate of 40 Gigabit Ethernet',
    mpmathify( '8.0e10' )     : 'the data rate of PCI Express x16 v2.0',
    mpmathify( '9.6e10' )     : 'the data rate of InfiniBand 12X QDR',
    mpmathify( '1.0e11' )     : 'the data rate of 100 Gigabit Ethernet',
    mpmathify( '1.28e11' )    : 'the data rate for PCI Express x16 v3.0',
    mpmathify( '1.28e12' )    : 'the data rate of a SEA-ME-WE 4 submarine communications cable - 1.28 terabits per second',
    mpmathify( '3.84e12' )    : 'the data rate of a I-ME-WE submarine communications cable - design capacity of 3.84 terabits per second',
    mpmathify( '2.45e14' )    : 'the projected average global internet traffic in 2015 according to Cisco\'s 2011 VNI IP traffic forecast',
    mpmathify( '1.050e15' )   : 'the data rate over a 14-transmission-core optical fiber developed by NEC and Corning researchers',
}


# //******************************************************************************
# //
# //  densityTable
# //
# //  gram/liter : description
# //
# //  http://en.wikipedia.org/wiki/Density
# //  http://en.wikipedia.org/wiki/Orders_of_magnitude_%28density%29
# //
# //******************************************************************************

densityTable = {
    mpmathify( '1.0e-27' )    : 'the density (very approximate) of the universe',
    mpmathify( '1.0e-22' )    : 'the probable lowest observed density of space in galactic spiral arm (1 hydrogen atom every 16 cubic centimeters)',
    mpmathify( '1.0e-18' )    : 'the observed density of space in core of galaxy (600 hydrogen atoms in every cubic centimetre); best vacuum from a laboratory (1 pPa)',
    mpmathify( '2.0e-14' )    : 'the density of the Sun\'s corona',
    mpmathify( '1.0e-13' )    : 'the density at top of the Solar transition region',
    mpmathify( '1.0e-11' )    : 'the density at the bottom of the Solar transition region',
    mpmathify( '1.34e-5' )    : 'the density of Earth\'s atmosphere at 82 km altitude; star Mu Cephei\'s approximate mean density',
    mpmathify( '1.0e-4' )     : 'the density of Earth\'s atmosphere at 68 km altitude',
    mpmathify( '2.0e-4' )     : 'the density of the Solar photosphere-chromosphere boundary',
    mpmathify( '4.0e-4' )     : 'the density of the Solar photosphere\'s lower boundary',
    mpmathify( '1.0e-3' )     : 'the density achieved in a mechanical vacuum pump; the density of the Sun just below its photosphere',
    mpmathify( '1.8e-2' )     : 'the density of Earth\'s atmosphere at 30 km altitude',
    mpmathify( '9.0e-2' )     : 'the density of Hydrogen gas, the least dense substance at STP',
    mpmathify( '1.6e-1' )     : 'the density of Earth\'s atmosphere at 16 km altitude',
    mpmathify( '1.8e-1' )     : 'the density of aerographite',
    mpmathify( '9.0e-1' )     : 'the density of an ultralight metallic microlattice',
    mpmathify( '1.10e0' )     : 'the lowest density achieved for an aerogel',
    mpmathify( '1.48e0' )     : 'the density of Earth\'s atmosphere at sea level',
    mpmathify( '1.0e1' )      : 'the lowest density of a typical aerogel',
    mpmathify( '1.24e1' )     : 'the density of tungsten hexafluoride, one of the heaviest known gases at standard conditions',
    mpmathify( '6.5e1' )      : 'the surface density of Venus\' atmosphere',
    mpmathify( '7.0e1' )      : 'the density of liquid hydrogen at approximately -255 degrees C',
    mpmathify( '7.5e1' )      : 'the approximate density of styrofoam',
    mpmathify( '2.40e2' )     : 'the approximate density of cork',
    mpmathify( '5.0e2' )      : 'the highest density of a typical aerogel',
    mpmathify( '5.35e2' )     : 'the density of lithium (Li)',
    mpmathify( '7.00e2' )     : 'the typical density of wood',
    mpmathify( '8.60e2' )     : 'the density of potassium (K)',
    mpmathify( '9.167e2' )    : 'the density of water ice at temperatures < 0 degrees C',
    mpmathify( '9.70e2' )     : 'the density of sodium (Na)',
    mpmathify( '1.000e3' )    : 'the density of liquid water at 4 degrees C',
    mpmathify( '1.030e3' )    : 'the density of salt water',
    mpmathify( '1.062e3' )    : 'the average density of the human body',
    mpmathify( '1.261e3' )    : 'the density of glycerol',
    mpmathify( '1.408e3' )    : 'the average density of the Sun',
    mpmathify( '1.622e3' )    : 'the density of tetrachloroethene',
    mpmathify( '1.740e3' )    : 'the density of magnesium (Mg)',
    mpmathify( '1.850e3' )    : 'the density of beryllium (Be)',
    mpmathify( '2.000e3' )    : 'the density of concrete',
    mpmathify( '2.330e3' )    : 'the density of silicon',
    mpmathify( '2.700e3' )    : 'the density of aluminium',
    mpmathify( '3.325e3' )    : 'the density of diiodomethane (liquid at room temperature)',
    mpmathify( '3.500e3' )    : 'the density of diamond',
    mpmathify( '4.540e3' )    : 'the density of titanium',
    mpmathify( '4.800e3' )    : 'the density of selenium',
    mpmathify( '5.515e3' )    : 'the average density of the Earth',
    mpmathify( '6.100e3' )    : 'the density of vanadium',
    mpmathify( '6.690e3' )    : 'the density of antimony',
    mpmathify( '7.000e3' )    : 'the density of zinc',
    mpmathify( '7.200e3' )    : 'the density of chromium',
    mpmathify( '7.310e3' )    : 'the density of tin',
    mpmathify( '7.325e3' )    : 'the density of manganese',
    mpmathify( '7.870e3' )    : 'the density of iron',
    mpmathify( '8.570e3' )    : 'the density of niobium',
    mpmathify( '8.600e3' )    : 'the density of brass',
    mpmathify( '8.650e3' )    : 'the density of cadmium',
    mpmathify( '8.900e3' )    : 'the density of cobalt',
    mpmathify( '8.900e3' )    : 'the density of nickel',
    mpmathify( '8.940e3' )    : 'the density of copper (Cu)',
    mpmathify( '9.750e3' )    : 'the density of bismuth (Bi)',
    mpmathify( '1.0220e4' )   : 'the density of molybdenum (Mo)',
    mpmathify( '1.0500e4' )   : 'the density of silver (Ag)',
    mpmathify( '1.1340e4' )   : 'the density of lead (Pb)',
    mpmathify( '1.1700e4' )   : 'the density of thorium (Th)',
    mpmathify( '1.2410e4' )   : 'the density of rhodium (Rh)',
    mpmathify( '1.3546e4' )   : 'the density of mercury (Hg)',
    mpmathify( '1.6600e4' )   : 'the density of tantalum (Ta)',
    mpmathify( '1.8800e4' )   : 'the density of uranium (U)',
    mpmathify( '1.9300e4' )   : 'the density of tungsten (W)',
    mpmathify( '1.9320e4' )   : 'the density of gold (Au)',
    mpmathify( '1.9840e4' )   : 'the density of plutonium (Pu)',
    mpmathify( '2.1450e4' )   : 'the density of platinum (Pt)',
    mpmathify( '2.2420e4' )   : 'the density of iridium (Ir)',
    mpmathify( '2.2590e4' )   : 'the density of osmium (Os), the densest known substance at STP',
    mpmathify( '4.1000e4' )   : 'the estimated density of Hassium (Hs), assuming that an isotope featuring a long half-life exists',
    mpmathify( '1.5e5' )      : 'the density of the core of the Sun',
    mpmathify( '1.0e9' )      : 'the density of a white dwarf',
    mpmathify( '2.0e13' )     : 'the approximate density of the universe at end of the electroweak epoch',
    mpmathify( '2.3e17' )     : 'the density of an atomic nucleus',
    mpmathify( '1.0e18' )     : 'the density of a neutron star',
    mpmathify( '1.0e23' )     : 'the density of a hypothetical preon star',
    mpmathify( '5.1e96' )     : 'the Planck density',
}


# //******************************************************************************
# //
# //  dynamicViscosityTable
# //
# //  pascal-second : description
# //
# //  http://en.wikipedia.org/wiki/Viscosity
# //
# //******************************************************************************

dynamicViscosityTable = {
    mpmathify( '8.8e-6' )     : 'the dynamic viscosity of hydrogen',
    mpmathify( '1.3e-5' )     : 'the dynamic viscosity of steam (at 100 degrees C)',
    mpmathify( '1.827e-5' )   : 'the dynamic viscosity of air at 18 degrees C',
    mpmathify( '2.822e-4' )   : 'the dynamic viscosity of water at 100 degrees C',
    mpmathify( '3.2e-4' )     : 'the dynamic viscosity of acetone',
    mpmathify( '6.0e-4' )     : 'the dynamic viscosity of gasoline',
    mpmathify( '1.002e-3' )   : 'the dynamic viscosity of water at 20 degrees C',
    mpmathify( '1.6e-3' )     : 'the dynamic viscosity of mercury',
    mpmathify( '3.0e-3' )     : 'the dynamic viscosity of milk',
    mpmathify( '4.0e-3' )     : 'the dynamic viscosity of human blood',
    mpmathify( '8.1e-3' )     : 'the dynamic viscosity of olive oil',
    mpmathify( '1.0e-1' )     : 'the dynamic viscosity of castor oil',
    mpmathify( '1.5' )        : 'the dynamic viscosity of glycerine',
    mpmathify( '5.0' )        : 'the dynamic viscosity of Karo syrup',
    mpmathify( '10' )         : 'the dynamic viscosity of honey',
    mpmathify( '50' )         : 'the dynamic viscosity of ketchup',
    mpmathify( '70' )         : 'the dynamic viscosity of mustard',
    mpmathify( '100' )        : 'the dynamic viscosity of sour Cream',
    mpmathify( '250' )        : 'the dynamic viscosity of peanut butter',
    mpmathify( '1.0e3' )      : 'the dynamic viscosity of lard',
    mpmathify( '1.0e4' )      : 'the dynamic viscosity of plate glass (at 900 degrees C)',
    mpmathify( '2.3e8' )      : 'the approximate viscosity of pitch',
}


# //******************************************************************************
# //
# //  electricalConductanceTable
# //
# //  mhos : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28resistance%29
# //
# //******************************************************************************

electricalConductanceTable = {
    mpmathify( '5.0e-20' )        : 'the resistance of a 1 meter path though sulphur at standard temperature and pressure',
    mpmathify( '5.0e-15' )        : 'the resistenace of a 1 meter path through quartz, upper limit',
    mpmathify( '1.01010101e-11' ) : 'the highest resistor code on common circuits (white white white)',
    mpmathify( '1.0e-5' )         : 'the approximate resistance of the human body with dry skin',
    mpmathify( '1.0e-3' )         : 'the approximate resistance of the human body through wet or broken skin',
    mpmathify( '1.515e-3' )       : 'the resistance of a circular mil-foot of Nichrome',
    mpmathify( '3.33564095e-2' )  : 'the Planck impedance',
    mpmathify( '0.10204')         : 'the resistance of a circular mil-foot of silver',
    mpmathify( '5.0' )            : 'the resistance of a 1 meter path in 35g/kg salinity seawater at 20 degrees C',
    mpmathify( '6.139e6' )        : 'the resistance of a one cubic centimeter block of silver',
}


# //******************************************************************************
# //
# //  electricalPotentialTable
# //
# //  volts : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28voltage%29
# //
# //******************************************************************************

electricPotentialTable = {
    mpmathify( '5.0e-7' )     : 'the change in nerve cell potential caused by opening a single acetylcholine receptor channel (500 nV)',
    mpmathify( '2.0e-6' )     : 'the voltage of noise in an EEG taken at the scalp (2 uV)',
    mpmathify( '1.0e-5' )     : 'the minimum peak-to-peak amplitude of an average EEG taken at the scalp (10 uV)',
    mpmathify( '1.5e-5' )     : 'the minimum terrestrial digital-TV RF antenna signal (-85 dBm over 75 ohms)',
    mpmathify( '5.6e-5' )     : 'the minimum terrestrial analog-TV RF antenna signal (35 dB[uV])',
    mpmathify( '1.0e-4' )     : 'the maximum peak-to-peak amplitude of an average EEG taken at the scalp (100 uV)',
    mpmathify( '7.5e-2' )     : 'the nerve cell resting potential (75 mV)',
    mpmathify( '0.316' )      : 'the typical voltage reference level in consumer audio electronics (0.316 V rms)',
    mpmathify( '0.9' )        : 'the voltage of a lemon battery cell (made with copper and zinc electrodes)',
    mpmathify( '1.5' )        : 'the voltage of an alkaline AA, AAA, C or D battery',
    mpmathify( '5.0' )        : 'the voltage of USB power, used for example to charge a cell phone or a digital camera',
    mpmathify( '6.0' )        : 'the common voltage for medium-size electric lanterns (6 V)',
    mpmathify( '12' )         : 'the typical car battery (12 V)',
    mpmathify( '110' )        : 'the typical domestic wall socket voltage (110 V)',
    mpmathify( '600' )        : 'the voltage an electric eel sends in an average attack',
    mpmathify( '630' )        : 'the voltage in London Underground railway tracks',
    mpmathify( '2450' )       : 'the voltage used for electric chair execution in Nebraska',
    mpmathify( '1.0e4' )      : 'an electric fence (10kV)',
    mpmathify( '1.5e4' )      : 'the voltage of overhead railway AC electrification lines, 162/3 Hz (15 kV)',
    mpmathify( '2.5e4' )      : 'the voltage of European high-speed train overhead power lines (25 kV)',
    mpmathify( '3.45e4' )     : 'the voltage in North America for power distribution to end users (34.5 kV)',
    mpmathify( '2.3e5' )      : 'the highest voltage used in North American power high-voltage transmission substations (230 kV)',
    mpmathify( '3.45e5' )     : 'the lowest voltage used in EHV power transmission systems (345 kV)',
    mpmathify( '8.0e5' )      : 'the lowest voltage used by ultra-high voltage (UHV) power transmission systems (800 kV)',
    mpmathify( '3.0e6' )      : 'the voltage used by the ultra-high voltage electron microscope at Osaka University',
    mpmathify( '2.55e7' )     : 'the largest man-made voltage - produced in a Van de Graaff generator at Oak Ridge National Laboratory',
    mpmathify( '1.0e8' )      : 'the potential difference between the ends of a typical lightning bolt',
    mpmathify( '7.0e15' )     : 'the voltage around a particular energetic highly magnetized rotating neutron star',
    mpmathify( '1.04e27' )    : 'the Planck voltage',
}


# //******************************************************************************
# //
# //  electricalResistanceTable
# //
# //  ohms : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28resistance%29
# //
# //******************************************************************************

electricalResistanceTable = {
    mpmathify( '1.629e-7' )   : 'the resistance of a one cubic centimeter block of silver',
    mpmathify( '0.2' )        : 'the resistance of a 1 meter path in 35g/kg salinity seawater at 20 degrees C',
    mpmathify( '9.8')         : 'the resistance of a circular mil-foot of silver',
    mpmathify( '29.9792458' ) : 'the Planck impedance',
    mpmathify( '6.60e2' )     : 'the resistance of a circular mil-foot of Nichrome',
    mpmathify( '1.0e3' )      : 'the approximate resistance of the human body through wet or broken skin',
    mpmathify( '1.0e5' )      : 'the approximate resistance of the human body with dry skin',
    mpmathify( '9.9e10' )     : 'the highest resistor code on common circuits (white white white)',
    mpmathify( '2.0e14' )     : 'the resistenace of a 1 meter path through quartz, upper limit',
    mpmathify( '2.0e19' )     : 'the resistance of a 1 meter path though sulphur at standard temperature and pressure',
}


# //******************************************************************************
# //
# //  energyTable
# //
# //  joules : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28energy%29
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28specific_energy%29
# //  https://en.wikipedia.org/wiki/Energy_density
# //
# //******************************************************************************

energyTable = {
    mpmathify( '2.0e-33' )    : 'the average kinetic energy of translational motion of a molecule at the lowest temperature reached, 100 picokelvins, as of 2003',
    mpmathify( '6.6e-28' )    : 'the eergy of a typical AM radio photon (1 MHz) (4e-9 eV)',
    mpmathify( '1.6e-24' )    : 'the energy of a typical microwave oven photon (2.45 GHz) (1e-5 eV)',
    mpmathify( '2.0e-23' )    : 'the average kinetic energy of translational motion of a molecule in the Boomerang Nebula, the coldest place known outside of a laboratory, (1 K)',
    mpmathify( '2.0e-22' )    : 'the minumum energy of infrared light photons',
    mpmathify( '1.7e-21' )    : '1 kJ/mol, converted to energy per molecule',
    mpmathify( '2.1e-21' )    : 'the thermal energy in each degree of freedom of a molecule at 25 degrees C (kT/2) (0.01 eV)',
    mpmathify( '2.856e-21' )  : 'the minimum amount of energy required at 25 degrees C to change one bit of information, according to Landauer\'s principle',
    mpmathify( '3.0e-21' )    : 'the minimum energy of a van der Waals interaction between atoms (0.02 eV)',
    mpmathify( '4.1e-21' )    : '"kT" at 25 degrees C, a common rough approximation for the total thermal energy of each molecule in a system (0.03 eV)',
    mpmathify( '4.5e-20' )    : 'the upper bound of the mass-energy of a neutrino in particle physics (0.28 eV)',
    mpmathify( '6.0e-21' )    : 'the maximum energy of a van der Waals interaction between atoms (0.04 eV)',
    mpmathify( '1.6e-19' )    : '1 electronvolt (eV)',
    mpmathify( '3.0e-19' )    : 'the minimum energy of photons in visible light',
    mpmathify( '5.0e-19' )    : 'the minimum energy of ultraviolet light photons',
    mpmathify( '2.0e-17' )    : 'the minimum energy of X-ray photons',
    mpmathify( '2.0e-14' )    : 'the minimum energy of gamma ray photons',
    mpmathify( '2.7e-14' )    : 'the upper bound of the mass-energy of a muon neutrino',
    mpmathify( '8.2e-14' )    : 'the rest mass-energy of an electron',
    mpmathify( '1.6e-13' )    : '1 megaelectronvolt (MeV)',
    mpmathify( '2.3e-12' )    : 'the kinetic energy of neutrons produced by D-T fusion, used to trigger fission (14.1 MeV)',
    mpmathify( '3.4e-11' )    : 'the average total energy released in the nuclear fission of one uranium-235 atom (215 MeV)',
    mpmathify( '1.503e-10' )  : 'rest mass-energy of a proton',
    mpmathify( '1.505e-10' )  : 'the rest mass-energy of a neutron',
    mpmathify( '1.6e-10' )    : '1 gigaelectronvolt (GeV)',
    mpmathify( '3.0e-10' )    : 'the rest mass-energy of a deuteron',
    mpmathify( '6.0e-10' )    : 'the rest mass-energy of an alpha particle',
    mpmathify( '1.6e-9' )     : '10 GeV',
    mpmathify( '8.0e-9' )     : 'the initial operating energy per beam of the CERN Large Electron Positron Collider in 1989 (50 GeV)',
    mpmathify( '1.3e-8' )     : 'the mass-energy of a W boson (80.4 GeV)',
    mpmathify( '1.5e-8' )     : 'the mass-energy of a Z boson (91.2 GeV)',
    mpmathify( '1.6e-8' )     : '100 GeV',
    mpmathify( '2.0e-8' )     : 'the mass-energy of the particle believed to be the Higgs Boson (125.3 GeV)',
    mpmathify( '6.4e-8' )     : 'the operating energy per proton of the CERN Super Proton Synchrotron accelerator in 1976',
    mpmathify( '1.6e-7' )     : '1 TeV (teraelectronvolt), about the same kinetic energy as flying mosquito',
    mpmathify( '5.6e-7' )     : 'the energy per proton in the CERN Large Hadron Collider in 2011 (3.5 TeV)',
    mpmathify( '0.11' )       : 'the energy of an American half-dollar falling 1-meter',
    mpmathify( '1.0' )        : '1 newton-meter, 1 Watt-second, the kinetic energy produced by ~100 grams falling 1 meter, or required to heat 1 gm of cool air by 1 degree C',
    mpmathify( '1.4' )        : '1 ft-lbf (foot-pound force)',
    mpmathify( '4.184' )      : '~1 thermochemical calorie (small calorie)',
    mpmathify( '4.1868' )     : '~1 International (Steam) Table calorie',
    mpmathify( '8.0' )        : 'the Greisen-Zatsepin-Kuzmin theoretical upper limit for the energy of a cosmic ray coming from a distant source',
    mpmathify( '50' )         : 'the most energetic cosmic ray ever detected, in 1991',
    mpmathify( '100' )        : 'the flash energy of a typical pocket camera electronic flash capacitor (100-400 uF @ 330 V)',
    mpmathify( '300' )        : 'the energy of a lethal dose of X-rays',
    mpmathify( '300' )        : 'the kinetic energy of an average person jumping as high as he can',
    mpmathify( '330' )        : 'the energy required to melt 1 g of ice',
    mpmathify( '360' )        : 'the kinetic energy of 800 g standard men\'s javelin thrown at > 30 m/s by elite javelin throwers',
    mpmathify( '600' )        : 'the kinetic energy of 2 kg standard men\'s discus thrown at 24.4 m/s by the world record holder Juergen Schult',
    mpmathify( '600' )        : 'the energy use of a 10-watt flashlight for 1-minute',
    mpmathify( '750' )        : '1 horsepower applied for 1 second',
    mpmathify( '780' )        : 'the kinetic energy of 7.26 kg standard men\'s shot thrown at 14.7 m/s by the world record holder Randy Barnes',
    mpmathify( '1.1e3' )      : '1 British thermal unit (BTU), depending on the temperature',
    mpmathify( '1.4e3' )      : 'the total solar radiation received from the Sun by 1 square meter at the altitude of Earth\'s orbit per second (solar constant)',
    mpmathify( '1.8e3' )      : 'the kinetic energy of M16 rifle bullet (5.56x45mm NATO M855, 4.1 g fired at 930 m/s)',
    mpmathify( '2.3e3' )      : 'the energy needed to vaporize 1 g of water into steam',
    mpmathify( '3.0e3' )      : 'the energy of a Lorentz force can crusher pinch',
    mpmathify( '3.4e3' )      : 'the kinetic energy of world-record men\'s hammer throw (7.26 kg thrown at 30.7 m/s in 1986)',
    mpmathify( '3.6e3' )      : '1 Wh (watt-hour)',
    mpmathify( '4.2e3' )      : 'the energy released by explosion of 1 gram of TNT',
    mpmathify( '4.2e3' )      : '~1 food Calorie (large calorie)',
    mpmathify( '7.0e3' )      : 'the approxmate muzzle energy of an elephant gun, firing a .458 Winchester Magnum',
    mpmathify( '9.0e3' )      : 'the energy in an alkaline AA battery',
    mpmathify( '1.7e4' )      : 'the energy released by the metabolism of 1 gram of carbohydrates or protein',
    mpmathify( '3.8e4' )      : 'the energy released by the metabolism of 1 gram of fat',
    mpmathify( '4.5e4' )      : 'the approximate energy released by the combustion of 1 gram of gasoline',
    mpmathify( '5.0e4' )      : 'the kinetic energy of 1 gram of matter moving at 10 km/s',
    mpmathify( '3.0e5' )      : 'the kinetic energy of a one ton automobile at highway speeds (89 km/h or 55 mph)',
    mpmathify( '5.0e5' )      : 'the kinetic energy of a 1 gram meteor hitting Earth',
    mpmathify( '1.0e6' )      : 'the kinetic energy of a 2 tonne vehicle at 32 metres per second (72 miles per hour)',
    mpmathify( '1.2e6' )      : 'the approximate food energy of a snack such as a Snickers bar (280 food calories)',
    mpmathify( '3.6e6' )      : '1 kWh (kilowatt-hour)',
    mpmathify( '8.4e6' )      : 'the recommended food energy intake per day for a moderately active woman (2000 food calories)',
    mpmathify( '1.0e7' )      : 'the kinetic energy of the armor-piercing round fired by the assault guns of the ISU-152 tank',
    mpmathify( '1.1e7' )      : 'the recommended food energy intake per day for a moderately active man (2600 food calories)',
    mpmathify( '3.7e7' )      : '$1 of electricity at a cost of $0.10/kWh (the US average retail cost in 2009)',
    mpmathify( '4.0e7' )      : 'the energy from the combustion of 1 cubic meter of natural gas',
    mpmathify( '4.2e7' )      : 'the caloric energy consumed by Olympian Michael Phelps on a daily basis during Olympic training',
    mpmathify( '6.3e7' )      : 'the theoretical minimum energy required to accelerate 1 kg of matter to escape velocity from Earth\'s surface (ignoring atmosphere)',
    mpmathify( '1.0e8' )      : 'the kinetic energy of a 55 tonne aircraft at typical landing speed (59 m/s or 115 knots)',
    mpmathify( '1.1e8' )      : 'the energy in 1 therm, depending on the temperature',
    mpmathify( '1.1e8' )      : 'the energy of 1 Tour de France, or ~90 hours ridden at 5 W/kg by a 65 kg rider',
    mpmathify( '1.3e8' )      : 'the energy used by the fictional DeLorean in the "Back to the Future", traveling at 88 mph expending 1.21 GW of power as it passes a through planar singularity',
    mpmathify( '7.3e8' )      : 'the energy from burning 16 kilograms of oil (using 135 kg per barrel of light crude)',
    mpmathify( '5.0e9' )      : 'the energy in an average lightning bolt',
    mpmathify( '1.1e9' )      : 'the magnetic stored energy in the world\'s largest toroidal superconducting magnet for the ATLAS experiment at CERN, Geneva',
    mpmathify( '1.4e9' )      : 'the theoretical minimum amount of energy required to melt a tonne of steel (380 kWh)',
    mpmathify( '2.0e9' )      : 'the Planck energy',
    mpmathify( '3.3e9' )      : 'the approximate average amount of energy expended by a human heart muscle over an 80-year lifetime',
    mpmathify( '4.5e9' )      : 'average annual energy usage of a standard refrigerator',
    mpmathify( '6.1e9' )      : 'approximately 1 bboe (barrel of oil equivalent)',
    mpmathify( '2.3e10' )     : 'the kinetic energy of an Airbus A380 at cruising speed (560 tonnes at 562 knots or 289 m/s)',
    mpmathify( '4.2e10' )     : 'approximately 1 toe (ton of oil equivalent)',
    mpmathify( '5.0e10' )     : 'the yield energy of a Massive Ordnance Air Blast bomb, the second most powerful non-nuclear weapon ever designed',
    mpmathify( '7.3e10' )     : 'the energy consumed by the average U.S. automobile in the year 2000',
    mpmathify( '8.64e10' )    : '1 megawatt-day (MWd), a measurement used in the context of power plants',
    mpmathify( '8.8e10' )     : 'the total energy released in the nuclear fission of one gram of uranium-235',
    mpmathify( '3.4e12' )     : 'the maximum fuel energy of an Airbus A330-300 (97,530 liters of Jet A-1)',
    mpmathify( '3.6e12' )     : '1 gigawatt-hour (GWh)',
    mpmathify( '4.0e12' )     : 'the electricity generated by one 20-kg CANDU fuel bundle assuming ~29% thermal efficiency of reactor',
    mpmathify( '6.4e12' )     : 'the energy contained in jet fuel in a Boeing 747-100B aircraft at max fuel capacity (183,380 liters of Jet A-1)',
    mpmathify( '1.1e13' )     : 'the energy of the maximum fuel an Airbus A380 can carry (320,000 liters of Jet A-1)',
    mpmathify( '1.2e13' )     : 'the orbital kinetic energy of the International Space Station (417 tonnes at 7.7 km/s)',
    mpmathify( '8.8e13' )     : 'the energy yield of the Fat Man atomic bomb used in World War II (21 kilotons)',
    mpmathify( '9.0e13' )     : 'the theoretical total mass-energy of 1 gram of matter',
    mpmathify( '6.0e14' )     : 'the energy released by an average hurricane in 1 second',
    mpmathify( '1.0e15' )     : 'the approximate energy released by a severe thunderstorm',
    mpmathify( '1.0e15' )     : 'the yearly electricity consumption in Greenland as of 2008',
    mpmathify( '4.2e15' )     : 'the energy released by explosion of 1 megaton of TNT',
    mpmathify( '1.0e16' )     : 'the estimated impact energy released in forming Meteor Crater in Arizona',
    mpmathify( '1.1e16' )     : 'the yearly electricity consumption in Mongolia as of 2010',
    mpmathify( '9.0e16' )     : 'the mass-energy in 1 kilogram of antimatter (or matter)',
    mpmathify( '1.0e17' )     : 'the energy released on the Earth\'s surface by the magnitude 9.1-9.3 2004 Indian Ocean earthquake',
    mpmathify( '1.7e17' )     : 'the total energy from the Sun that strikes the face of the Earth each second',
    mpmathify( '2.1e17' )     : 'the yield of the Tsar Bomba, the largest nuclear weapon ever tested (50 megatons)',
    mpmathify( '4.2e17' )     : 'the yearly electricity consumption of Norway as of 2008',
    mpmathify( '8.0e17' )     : 'the estimated energy released by the eruption of the Indonesian volcano, Krakatoa, in 1883',
    mpmathify( '1.4e18' )     : 'the yearly electricity consumption of South Korea as of 2009',
    mpmathify( '1.4e19' )     : 'the yearly electricity production and consumption in the U.S. as of 2009',
    mpmathify( '5.0e19' )     : 'the energy released in 1-day by an average hurricane in producing rain (400 times greater than the wind energy)',
    mpmathify( '6.4e19' )     : 'the yearly electricity consumption of the world as of 2008',
    mpmathify( '6.8e19' )     : 'the yearly electricity generation of the world as of 2008',
    mpmathify( '5.0e20' )     : 'the total world annual energy consumption in 2010',
    mpmathify( '8.0e20' )     : 'the estimated global uranium resources for generating electricity 2005',
    mpmathify( '6.9e21' )     : 'the estimated energy contained in the world\'s natural gas reserves as of 2010',
    mpmathify( '7.9e21' )     : 'the estimated energy contained in the world\'s petroleum reserves as of 2010',
    mpmathify( '1.5e22' )     : 'the total energy from the Sun that strikes the face of the Earth each day',
    mpmathify( '2.4e22' )     : 'the estimated energy contained in the world\'s coal reserves as of 2010',
    mpmathify( '2.9e22' )     : 'the total identified global uranium-238 resources using fast reactor technology',
    mpmathify( '3.9e22' )     : 'the estimated energy contained in the world\'s fossil fuel reserves as of 2010',
    mpmathify( '4.0e22' )     : 'the estimated total energy released by the magnitude 9.1-9.3 2004 Indian Ocean Earthquake',
    mpmathify( '2.2e23' )     : 'the total global uranium-238 resources using fast reactor technology',
    mpmathify( '5.0e23' )     : 'the approximate energy released in the formation of the Chicxulub Crater in the Yucatan Peninsula',
    mpmathify( '5.5e24' )     : 'the total energy from the Sun that strikes the face of the Earth each year',
    mpmathify( '1.3e26' )     : 'a conservative estimate of the energy released by the impact that created the Caloris basin on Mercury',
    mpmathify( '3.8e26' )     : 'the total energy output of the Sun each second',
    mpmathify( '3.8e28' )     : 'the kinetic energy of the Moon in its orbit around the Earth (counting only its velocity relative to the Earth)',
    mpmathify( '2.1e29' )     : 'the rotational energy of the Earth',
    mpmathify( '1.8e30' )     : 'the gravitational binding energy of Mercury',
    mpmathify( '3.3e31' )     : 'the total energy output of the Sun each day',
    mpmathify( '2.0e32' )     : 'the gravitational binding energy of the Earth',
    mpmathify( '2.7e33' )     : 'the Earth\'s kinetic energy in its orbit',
    mpmathify( '1.2e34' )     : 'the total energy output of the Sun each year',
    mpmathify( '6.6e39' )     : 'the theoretical total mass-energy of the Moon',
    mpmathify( '5.4e41' )     : 'the theoretical total mass-energy of the Earth',
    mpmathify( '6.9e41' )     : 'the gravitational binding energy of the Sun',
    mpmathify( '5.0e43' )     : 'the total energy of all gamma rays in a typical gamma-ray burst',
    mpmathify( '1.5e44' )     : 'the estimated energy released in a supernova, sometimes referred to as a "foe"',
    mpmathify( '1.0e46' )     : 'the estimated energy released in a hypernova',
    mpmathify( '1.8e47' )     : 'the theoretical total mass-energy of the Sun',
    mpmathify( '8.8e47' )     : 'GRB 080916C - the most powerful Gamma-Ray Burst (GRB) ever recorded - total isotropic energy output estimated at 8.8 x 10^47 joules',
    mpmathify( '4.0e58' )     : 'the visible mass-energy in our galaxy, the Milky Way',
    mpmathify( '1.0e59' )     : 'the total mass-energy of our galaxy, the Milky Way, including dark matter and dark energy',
    mpmathify( '1.5e62' )     : 'the approximate total mass-energy of the Virgo Supercluster including dark matter, the Supercluster which contains the Milky Way',
    mpmathify( '4.0e69' )     : 'the estimated total mass-energy of the observable universe',
}


# //******************************************************************************
# //
# //  forceTable
# //
# //  newtons : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28force%29
# //
# //******************************************************************************

forceTable = {
    mpmathify( '3.6e-47' )    : 'the gravitational attraction of the proton and the electron in hydrogen atom',
    mpmathify( '8.9e-30' )    : 'the weight of an electron',
    mpmathify( '1.6e-26' )    : 'the weight of a hydrogen atom',
    mpmathify( '5.0e-24' )    : 'the force necessary to synchronize the motion of a single trapped ion with an external signal measured in a 2010 experiment',
    mpmathify( '1.7e-22' )    : 'the force measured in a 2010 experiment by perturbing 60 beryllium-9 ions',
    mpmathify( '1.0e-14' )    : 'the appoximate Brownian motion force on an E. coli bacterium averaged over 1 second',
    mpmathify( '1.0e-13' )    : 'the force needed to stretch double-stranded DNA to 50% relative extension',
    mpmathify( '4.0e-12' )    : 'the force needed to break a hydrogen bond',
    mpmathify( '5.0e-12' )    : 'the maximum force of a molecular motor',
    mpmathify( '1.6e-10' )    : 'the force needed to break a typical noncovalent bond',
    mpmathify( '1.6e-9' )     : 'the force needed to break a typical covalent bond',
    mpmathify( '8.2e-8' )     : 'the force on an electron in a hydrogen atom',
    mpmathify( '2.0e-7' )     : 'the force between two 1 meter long conductors, 1 meter apart by the definition of one ampere',
    mpmathify( '1.5e-4' )     : 'the maximum output of FEEP ion thrusters used in NASA\'s Laser Interferometer Space Antenna (150 uN)',
    mpmathify( '9.2e-2' )     : 'the maximum thrust of the NSTAR ion engine tested on NASA\'s space probe Deep Space 1 (92 mN)',
    mpmathify( '1.0' )        : 'the weight of an average apple',
    mpmathify( '9.8' )        : 'a one kilogram-force, nominal weight of a 1 kg object at sea level on Earth',
    mpmathify( '720' )        : 'the average force of human bite, measured at molars',
    mpmathify( '8.0e3' )      : 'the maximum force achieved by weight lifters during a "clean and jerk" lift',
    mpmathify( '9.0e3' )      : 'the bite force of one adult American alligator',
    mpmathify( '1.8e5' )      : 'the bite force of an adult great white shark',
    mpmathify( '4.5e5' )      : 'the force applied by the engine of a small car during peak acceleration[citation needed]',
    mpmathify( '1.0e5' )      : 'the average force applied by seatbelt and airbag to a restrained passenger in a car which hits a stationary barrier at 100 km/h',
    mpmathify( '8.9e5' )      : 'the maximum pulling force (tractive effort) of a single large diesel-electric locomotive',
    mpmathify( '1.8e6' )      : 'the thrust of Space Shuttle Main Engine at lift-off',
    mpmathify( '1.9e6' )      : 'the weight of the largest Blue Whale',
    mpmathify( '3.5e7' )      : 'the thrust of Saturn V rocket at lift-off',
    mpmathify( '5.7e8' )      : 'a simplistic estimate of force of sunlight on Earth',
    mpmathify( '2.0e20' )     : 'the gravitational attraction between Earth and Moon',
    mpmathify( '3.5e22' )     : 'the gravitational attraction between Earth and Sun',
    mpmathify( '1.2e44' )     : 'the Planck force',
}


# //******************************************************************************
# //
# //  frequencyTable
# //
# //  hertz : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28force%29
# //
# //******************************************************************************

# The second is the duration of 9 192 631 770 periods of the radiation corresponding to the transition between the
# two hyperfine levels of the ground state of the caesium 133 atom.

frequencyTable = {
    mpmathify( '2.296e-18' )          : 'the frequency of the Hubble Constant (once in 13.8 billion years)',
    mpmathify( '1.0e-15' )            : '1 femtohertz (fHz)',
    mpmathify( '1.0e-12' )            : '1 picohertz (pHz)',
    mpmathify( '3.1687535787e-11' )   : 'the frequency of once a millennium',
    mpmathify( '3.1687535787e-10' )   : 'the frequency of once a century',
    mpmathify( '3.1687535787e-9' )    : 'the frequency of once a decade',
    mpmathify( '3.1687535787e-8' )    : 'the Earth\'s orbital frequency (once a year)',
    mpmathify( '3.6603221e-5' )       : 'the Moon\'s orbital frequency (once a siderial month)',
    mpmathify( '1.653e-6' )           : 'the frequency of once a week',
    mpmathify( '1.15741e-5' )         : 'the Earth\'s rotation frequency (once a day)',
    mpmathify( '2.777778e-4' )        : 'the frequency of once an hour',
    mpmathify( '1.0e-3' )             : '1 millihertz (mHz)',
    mpmathify( '1.66666667e-2' )      : 'the frequency of one RPM',
    mpmathify( '1.4285714e-2' )       : 'the average frequency of an adult human\'s resting heart beat',
    mpmathify( '10' )                 : 'the cyclic rate of a typical automobile engine at idle (equivalent to 600 rpm)',
    mpmathify( '12' )                 : 'the frequency of lowest possible frequency that a human can hear',
    mpmathify( '27.5' )               : 'the frequency of the lowest musical note (A) playable on a normally-tuned standard piano',
    mpmathify( '50' )                 : 'the frequency of standard AC mains power (European AC, Tokyo AC)',
    mpmathify( '60' )                 : 'the frequency of standard AC mains power (American AC, Osaka AC)',
    mpmathify( '100' )                : 'the cyclic rate of a typical automobile engine at redline (equivalent to 6000 rpm)',
    mpmathify( '261.626' )            : 'the frequency of the musical note middle C',
    mpmathify( '440' )                : 'the frequency of the concert pitch (A above middle C), used for tuning musical instruments',
    mpmathify( '4.186e3' )            : 'the frequency of the highest musical note (C8) playable on a normally-tuned standard piano',
    mpmathify( '8.0e3' )              : 'the frequency of the ISDN sampling rate',
    mpmathify( '1.4e4' )              : 'the frequency of the typical upper limit of adult human hearing',
    mpmathify( '1.74e4' )             : 'a frequency known as \'The Mosquito\', which is generally only audible to those under the age of 24',
    mpmathify( '5.30e5' )             : 'the lower end of the AM radio broadcast spectrum',
    mpmathify( '7.40e5' )             : 'the clock speed of the world\'s first commercial microprocessor, the Intel 4004 (1971)',
    mpmathify( '1.710e6' )            : 'the higher end of the AM radio broadcast spectrum',
    mpmathify( '4.77e6' )             : 'the clock frequency of the 8086 processor in the IBM PC',
    mpmathify( '1.356e7' )            : 'the frequency of Near Field Communication',
    mpmathify( '8.8e7' )              : 'the lower end of the FM radio broadcast spectrum',
    mpmathify( '1.08e8' )             : 'the upper end of the FM radio broadcast spectrum',
    mpmathify( '1.42e9' )             : 'the frequency of the hyperfine transition of hydrogen, also known as the hydrogen line or 21 cm line',
    mpmathify( '2.4e9' )              : 'the frequency of microwave ovens, Wireless LANs and cordless phones (starting in 1998)',
    mpmathify( '3.8e9' )              : 'the fastest common desktop processor speed as of 2014',
    mpmathify( '4.7e9' )              : 'the AMD FX-9790 clock speed, fastest commercial processor in 2014',
    mpmathify( '5.8e9' )              : 'the cordless phone frequency introduced in 2003',
    mpmathify( '1.602e11' )           : 'the peak of cosmic microwave background radiation',
    mpmathify( '8.45e11' )            : 'the frequency of the fastest transistor (Dec. 2006)',
    mpmathify( '2.1e13' )             : 'the lower end of the frequency of infrared light used in thermal imaging',
    mpmathify( '3.3e13' )             : 'the upper end of the frequency of infrared light used in thermal imaging',
    mpmathify( '4.28e14' )            : 'the lower end of the visible light spectrum (red)',
    mpmathify( '7.50e14' )            : 'the upper end of the visible light spectrum (violet)',
    mpmathify( '2.47e15' )            : 'the frequency of the Lyman-alpha line',
    mpmathify( '3.0e16' )             : 'the frequency of X-Rays',
    mpmathify( '3.00e17' )            : 'the frequency of gamma rays',
    mpmathify( '1.0e18' )             : '1 exahertz (EHz)',
    mpmathify( '1.0e21' )             : '1 zettahertz (ZHz)',
    mpmathify( '1.0e21' )             : '1 yottahertz (YHz)',
    mpmathify( '3.9e27' )             : 'the frequency of the highest energy (16 TeV) gamma ray detected, from Markarian 501',
    mpmathify( '1.85e43' )            : 'the Planck frequency, the inverse of the Planck time',
}


# //******************************************************************************
# //
# //  illuminanceTable
# //
# //  lux : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28illuminance%29
# //
# //******************************************************************************

illuminanceTable = {
    mpmathify( '1.0e-4' )     : 'the illuminance of starlight on an overcast, moonless night sky',
    mpmathify( '1.4e-4' )     : 'the illuminance of Venus at its brightest',
    mpmathify( '2.0e-4' )     : 'the illuminance of starlight on a clear, moonless night sky, excluding airglow',
    mpmathify( '2.0e-3' )     : 'the illuminance of starlight on a clear, moonless night sky, including airglow',
    mpmathify( '1.0e-2' )     : 'the illuminance of the quarter Moon',
    mpmathify( '2.5e-2' )     : 'the illuminance of the full Moon on a clear night',
    mpmathify( '1.0' )        : 'the illuminance of the extreme of darkest storm clouds at sunset/sunrise',
    mpmathify( '40' )         : 'the illuminance of a fully overcast sky at sunset/sunrise',
    mpmathify( '200' )        : 'the illuminance of the extreme of darkest storm clouds at midday',
    mpmathify( '400' )        : 'the illuminance of sunrise or sunset on a clear day',
    mpmathify( '25000' )      : 'the illuminance of typical overcast day at midday',
    mpmathify( '120000' )     : 'the illuminance of the brightest sunlight',
}


# //******************************************************************************
# //
# //  inductanceTable
# //
# //  henries : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28inductance%29
# //
# //******************************************************************************

inductanceTable = {
    mpmathify( '1.0e-9' )     : 'the inductance of a thin film chip inductor, 1.6x0.8 mm with a typical power rating of 0.1 W (range: 1-100 nH)',
    mpmathify( '5.25e-7' )    : 'the inductance of one meter of Cat-5 cable pair',
    mpmathify( '5.0e-5' )     : 'the inductance of a coil with 99 turns, 0.635 cm long with a diameter of 0.635 cm',
    mpmathify( '1.0e-3' )     : 'the inductance of a coil 2.2 cm long with a diameter of 1.6 cm with 800 mA capability, used in kW amplifiers',
    mpmathify( '1.0' )        : 'the inductance of an inductor a few cm long and a few cm in diameter with many turns of wire on a ferrite core',
    mpmathify( '11' )         : 'the inductance of a mains electricity transformer primary at 120 V (range: 8-11 H)',
    mpmathify( '1.326e3' )    : 'the inductance of 500 kV, 3000 MW power line transformer primary winding',
}


# //******************************************************************************
# //
# //  informationEntropyTable
# //
# //  bits : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28data%29
# //
# //******************************************************************************

informationEntropyTable = {
    mpmathify( '1' )              : '1 bit - 0 or 1, false or true',
    mpmathify( '1.58496' )        : 'the approximate size of a trit (a base-3 digit, log2( 3 )',
    mpmathify( '2' )              : 'a crumb (rarely used term), enough to uniquely identify one base pair of DNA',
    mpmathify( '3' )              : 'the size of an octal digit',
    mpmathify( '4' )              : 'the size of a hexadecimal digit; decimal digits in binary-coded decimal form',
    mpmathify( '5' )              : 'the size of code points in the Baudot code, used in telex communication',
    mpmathify( '6' )              : 'the size of code points in Univac Fieldata, in IBM "BCD" format, and in Braille; enough to uniquely identify one codon of genetic code',
    mpmathify( '7' )              : 'the size of code points in the ASCII character set, minimum length to store 2 decimal digits',
    mpmathify( '8' )              : '1 byte (a.k.a. "octet") on many computer architectures, Equivalent to 1 "word" on 8-bit computers (Apple II, Atari 800, Commodore 64, et al.)',
    mpmathify( '10' )             : 'the minimum bit length to store a single byte with error-correcting memory, minimum frame length to transmit a single byte with asynchronous serial protocols',
    mpmathify( '12' )             : 'the word length of the PDP-8 of Digital Equipment Corporation (built from 1965-1990)',
    mpmathify( '16' )             : 'a commonly used in many programming languages, the size of an integer capable of holding 65,536 different values',
    mpmathify( '32' )             : 'size of addresses in IPv4, the current Internet protocol',
    mpmathify( '36' )             : 'the size of word on Univac 1100-series computers and Digital Equipment Corporation\'s PDP-10',
    mpmathify( '128' )            : 'size of addresses in IPv6, the successor protocol of IPv4',
    mpmathify( '256' )            : 'the minimum key length for the recommended strong cryptographic message digests as of 2004',
    mpmathify( '640' )            : 'the capacity of a punched card',
    mpmathify( '1288' )           : 'the approximate maximum capacity of a standard magnetic stripe card',
    mpmathify( '2048' )           : 'the RAM capacity of the stock Altair 8800',
    mpmathify( '4096' )           : 'the approximate amount of information on a sheet of single-spaced typewritten paper (without formatting)',
    mpmathify( '4704' )           : 'the uncompressed single-channel frame length in standard MPEG audio (75 frames per second and per channel), with medium quality 8-bit sampling at 44,100 Hz (or 16-bit sampling at 22,050 Hz)',
    mpmathify( '8192' )           : 'the RAM capacity of a Sinclair ZX81',
    mpmathify( '9408' )           : 'the uncompressed single-channel frame length in standard MPEG audio (75 frames per second and per channel), with standard 16-bit sampling at 44,100 Hz',
    mpmathify( '15360' )          : 'one screen of data displayed on an 8-bit monochrome text console (80x24)',
    mpmathify( '16384' )          : 'one page of typed text, the RAM capacity of Nintendo Entertainment System',
    mpmathify( '131072' )         : 'the RAM capacity of the smallest Sinclair ZX Spectrum.',
    mpmathify( '524288' )         : 'the RAM capacity of a lot of popular 8-bit Computers like the C-64, Amstrad CPC, etc.',
    mpmathify( '1048576' )        : 'the RAM capacity of popular 8-bit Computers like the C-128, Amstrad CPC etc. Or a 1024 x 768 pixel jpeg image',
    mpmathify( '1978560' )        : 'a one-page, standard-resolution black-and-white fax (1728 x 1145 pixels)',
    mpmathify( '4147200' )        : 'one frame of uncompressed NTSC DVD video (720 x 480 x 12 bpp Y\'CbCr)',
    mpmathify( '4976640' )        : 'one frame of uncompressed PAL DVD video (720 x 576 x 12 bpp Y\'CbCr)',
    mpmathify( '5.0e6' )          : 'a typical English book volume in plain text format of 500 pages x 2000 characters per page and 5-bits per character',
    mpmathify( '5242880' )        : 'the maximum addressable memory of the original IBM PC architecture',
    mpmathify( '8343400' )        : 'one "typical" sized photograph with reasonably good quality (1024 x 768 pixels)',
    mpmathify( '1.152e7' )        : 'the capacity of a lower-resolution computer monitor (as of 2006), 800 x 600 pixels, 24 bpp',
    mpmathify( '11796480' )       : 'the capacity of a 3.5 in floppy disk, colloquially known as 1.44 megabyte but actually 1.44 x 1000 x 1024 bytes',
    mpmathify( '2.5e7' )          : 'the amount of data in a typical color slide',
    mpmathify( '3.0e7' )          : 'the storage capacity of the first commercial harddisk IBM 350 in 1956',
    mpmathify( '33554432' )       : 'the RAM capacity of stock Nintendo 64 and average size of a music track in MP3 format',
    mpmathify( '4.194304e7' )     : 'the approximate size of the Complete Works of Shakespeare',
    mpmathify( '7.5e7' )          : 'the amount of information in a typical phone book',
    mpmathify( '9.8304e7' )       : 'capacity of a high-resolution computer monitor as of 2011, 2560 x 1600 pixels, 24 bpp',
    mpmathify( '1.50e7' )         : 'the amount of data in a large foldout map',
    mpmathify( '4.2336e8356' )    : 'a five-minute audio recording, in CDDA quality',
    mpmathify( '5.4525952e9' )    : 'the storage capacity of a regular compact disc (CD)',
    mpmathify( '5.888802816e9' )  : 'the capacity of a large regular compact disc',
    mpmathify( '6.4e9' )          : 'the capacity of the human genome (assuming 2 bits for each base pair)',
    mpmathify( '6710886400' )     : 'the average size of a movie in Divx format in 2002',
    mpmathify( '8589934592' )     : 'the maximum disk capacity using the 21-bit LBA SCSI standard introduced in 1979',
    mpmathify( '17179869184' )    : 'the storage limit of IDE standard for harddisks in 1986 and the volume limit for FAT16 released in 1984',
    mpmathify( '34359738368' )    : 'the maximum addressable memory for the Motorola 68020 (1984) and Intel 80386 (1985)',
    mpmathify( '3.76e10' )        : 'the capacity of a single-layer, single-sided DVD',
    mpmathify( '79215880888' )    : 'the size of Wikipedia article text compressed with bzip2 on 2013-06-05',
    mpmathify( '1.46e11' )        : 'the capacity of a double-sided, dual-layered DVD',
    mpmathify( '2.15e11' )        : 'the capacity of a single-sided, single-layered 12-cm Blu-ray disc',
    mpmathify( '1.34e12' )        : 'the estimated capacity of the Polychaos dubium genome, the largest known genome',
    mpmathify( '8.97e12' )        : 'the data of pi to the largest number of decimal digits ever calculated as of 2010',
    mpmathify( '1.0e13' )         : 'the capacity of a human being\'s functional memory, according to Raymond Kurzweil',
    mpmathify( '16435678019584' ) : 'the size of all multimedia files used in English wikipedia on May 2012',
    mpmathify( '17592186044416' ) : 'the capacity of a hard disk that would be considered average as of 2012 and the maximum disk capacity using the 32-bit LBA SCSI introduced in 1987',
    mpmathify( '1.40737e14' )     : 'the NTFS volume capacity in Windows 7, Windows Server 2008 R2 or earlier implementation',
    mpmathify( '3.6028e16' )      : 'the theoretical maximum of addressable physical memory in the AMD64 architecture',
    mpmathify( '4.5e16' )         : 'the estimated hard drive space in Google\'s server farm as of 2004',
    mpmathify( '2.4e16' )         : 'the estimated approximate size of the Library of Congress\'s collection, including non-book materials',
    mpmathify( '2.0e17' )         : 'the storage space of Megaupload file-hosting service at the time it was shut down in 2012',
    mpmathify( '8.0e17' )         : 'the storage capacity of the fictional Star Trek character Data',
    mpmathify( '1.15292e18' )     : 'the storage limit using the ATA-6 standard introduced in 2002',
    mpmathify( '1.6e18' )         : 'the total amount of printed material in the world',
    mpmathify( '1.47573e20' )     : 'the maximum addressable memory using 64-bit addresses',
    mpmathify( '3.5e20' )         : 'the increase in information capacity when 1 Joule of energy is added to a heat-bath at 300 K (27 degrees C)',
    mpmathify( '3.4e21' )         : 'the amount of information that can be stored in 1 gram of DNA',
    mpmathify( '4.7e21' )         : 'the amount of digitally stored information in the world as of May 2009',
    mpmathify( '7.55579e22' )     : 'the Maximum volume and file size in the Unix File System (UFS) and maximum disk capacity using the 64-bit LBA SCSI standard introduced in 2000 using 512-byte blocks',
    mpmathify( '1.0e23' )         : 'the increase in information capacity when 1 Joule of energy is added to a heat-bath at 1 K (-272.15 degrees C)',
    mpmathify( '6.0e23' )         : 'the information content of 1 mole (12.01 g) of graphite at 25 degrees C; equivalent to an average of 0.996 bits per atom',
    mpmathify( '7.3e24' )         : 'the information content of 1 mole (18.02 g) of liquid water at 25 degrees C; equivalent to an average of 12.14 bits per molecule',
    mpmathify( '1.1e25' )         : 'entropy increase of 1 mole (18.02 g) of water, on vaporizing at 100 degrees C at standard pressure; equivalent to an average of 18.90 bits per molecule',
    mpmathify( '1.5e25' )         : 'the information content of 1 mole (20.18 g) of neon gas at 25 degrees C and 1 atm; equivalent to an average of 25.39 bits per atom',
    mpmathify( '2.0e45' )         : 'the number of bits required to perfectly recreate the natural matter of the average-sized U.S. adult male human being to the quantum level (Bekenstein bound)',
    mpmathify( '1.0e58' )         : 'the approximate thermodynamic entropy of the sun (about 30 bits per proton, plus 10 bits per electron)',
    mpmathify( '1.0e69' )         : 'the approximate thermodynamic entropy of the Milky Way Galaxy (counting only the stars, not the black holes within the galaxy)',
    mpmathify( '1.5e77' )         : 'the approximate information content of a one-solar-mass black hole',
    mpmathify( '1.0e92' )         : 'the information capacity of the observable universe, according to Seth Lloyd',
    mpmathify( '1.0e105' )        : 'the estimated theoretical maximum entropy of the universe',
}


# //******************************************************************************
# //
# //  jerkTable
# //
# //  meters/second^3 : description
# //
# //******************************************************************************

jerkTable = {
}


# //******************************************************************************
# //
# //  jounceTable
# //
# //  meters/second^4 : description
# //
# //******************************************************************************

jounceTable = {
}


# //******************************************************************************
# //
# //  lengthTable
# //
# //  meters : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28length%29
# //  https://en.wikipedia.org/wiki/List_of_examples_of_lengths
# //
# //******************************************************************************

lengthTable = {
    mpmathify( '1.616199e-35' )   : 'the Planck length; typical scale of hypothetical loop quantum gravity or size of a hypothetical string and of branes; according to string theory lengths smaller than this do not make any physical sense',
    mpmathify( '2.0e-23' )        : 'the effective cross section radius of 1 MeV neutrinos[3]',
    mpmathify( '1.0e-21' )        : 'the upper bound for the width of a cosmic string in string theory',
    mpmathify( '7.0e-21' )        : 'the effective cross section radius of high energy neutrinos',
    mpmathify( '3.1e-19' )        : 'the de Broglie wavelength of protons at the Large Hadron Collider (4 TeV as of 2012)',
    mpmathify( '1.0e-18' )        : 'the upper limit for the size of quarks and electrons, upper bound of the typical size range for "fundamental strings"',
    mpmathify( '1.0e-17' )        : 'the range of the weak force',
    mpmathify( '8.5e-16' )        : 'the approximate radius of a proton',
    mpmathify( '1.5e-15' )        : 'the size of an 11 MeV proton',
    mpmathify( '2.81794e-15' )    : 'the classical electron radius',
    mpmathify( '1.0e-12' )        : 'the longest wavelength of gamma rays',
    mpmathify( '2.4e-12' )        : 'the Compton wavelength of electron',
    mpmathify( '5.0e-12' )        : 'the wavelength of shortest X-rays',
    mpmathify( '2.5e-11' )        : 'the radius of a hydrogen atom',
    mpmathify( '3.1e-11' )        : 'the radius of a helium atom',
    mpmathify( '5.3e-11' )        : 'the Bohr radius',
    mpmathify( '1.0e-10' )        : 'an Angstrom (also the covalent radius of a sulfur atom)',
    mpmathify( '1.54e-10' )       : 'the length of a typical covalent bond (C-C)',
    mpmathify( '3.4e-10' )        : 'the thickness of single layer graphene',
    mpmathify( '7.0e-10' )        : 'the width of glucose molecule',
    mpmathify( '9.0e-10' )        : 'the width of sucrose molecule',
    mpmathify( '1.0e-9' )         : 'the diameter of a carbon nanotube',
    mpmathify( '2.5e-9' )         : 'the smallest microprocessor transistor gate oxide thickness (as of Jan 2007)',
    mpmathify( '8.0e-9' )         : 'the average thickness of a cell membrane',
    mpmathify( '1.0e-8' )         : 'the thickness of cell wall in gram-negative bacteria',
    mpmathify( '4.0e-8' )         : 'the wavelength of extreme ultraviolet',
    mpmathify( '9.0e-8' )         : 'the size of the Human immunodeficiency virus (HIV) (generally, viruses range in size from 20 nm to 450 nm)',
    mpmathify( '1.25e-7' )        : 'the standard depth of pits on compact discs (width: 500 nm, length: 850 nm to 3.5 um)',
    mpmathify( '4.075e-7' )       : 'the center wavelength of violet light',
    mpmathify( '6.825e-5' )       : 'the center wavelength of red light',
    mpmathify( '2.0e-6' )         : 'the particle size that a surgical mask removes at 80-95% efficiency',
    mpmathify( '3.5e-6' )         : 'the size of a typical yeast cell',
    mpmathify( '7.0e-6' )         : 'the average diameter of a red blood cell',
    mpmathify( '1.0e-5' )         : 'the typical size of a fog, mist or cloud water droplet',
    mpmathify( '1.2e-5' )         : 'the width of acrylic fiber',
    mpmathify( '2.54e-5' )        : '1/1000 inch, commonly referred to as one thou or one mil',
    mpmathify( '5.0e-5' )         : 'the length of a typical Euglena gracilis, a flagellate protist',
    mpmathify( '9.0e-5' )         : 'the average thickness of paper',
    mpmathify( '1.0e-4' )         : 'the average width of a strand of human hair',
    mpmathify( '2.0e-4' )         : 'the typical length of Paramecium caudatum, a ciliate protist',
    mpmathify( '5.0e-4' )         : 'the length of a typical Amoeba proteus',
    mpmathify( '7.60e-4' )        : 'the thickness of a typical credit card',
    mpmathify( '0.00254' )        : 'the distance between pins in DIP (dual-inline-package) electronic components',
    mpmathify( '0.005' )          : 'the length of average red ant',
    mpmathify( '0.00762' )        : '7.62 mm, a common military ammunition size',
    mpmathify( '0.0254' )         : 'an inch',
    mpmathify( '0.04267' )        : 'the diameter of a golf ball',
    mpmathify( '0.054' )          : 'the width of a typical credit card',
    mpmathify( '0.086' )          : 'the length of a typical credit card',
    mpmathify( '0.12' )           : 'the diameter of a Compact Disc (120 mm)',
    mpmathify( '0.22' )           : 'the diameter of a typical soccer ball',
    mpmathify( '0.3048' )         : 'a foot',
    mpmathify( '0.9144' )         : 'a yard',
    mpmathify( '1.7' )            : 'the average height of a human',
    mpmathify( '8.38' )           : 'the length of a London Bus (Routemaster)',
    mpmathify( '33' )             : 'the length of longest blue whale measured, the largest animal',
    mpmathify( '91.44' )          : 'the length of a football field',
    mpmathify( '93.47' )          : 'the height of the Statue of Liberty (foundation of pedestal to torch)',
    mpmathify( '137' )            : 'the height of the Great Pyramid of Giza',
    mpmathify( '979' )            : 'the height of the Salto Angel, the world\'s highest free-falling waterfall (Venezuela)',
    mpmathify( '1.609e3' )        : 'an international mile',
    mpmathify( '1.852e3' )        : 'a nautical mile',
    mpmathify( '8.848e3' )        : 'the height of the highest mountain on earth, Mount Everest',
    mpmathify( '1.0911e4' )       : 'the depth of deepest part of the ocean, Mariana Trench',
    mpmathify( '1.3e4' )          : 'the narrowest width of the Strait of Gibraltar, separating Europe and Africa',
    mpmathify( '42194.988' )      : 'the length of a marathon',
    mpmathify( '9.0e4' )          : 'the width of the Bering Strait',
    mpmathify( '1.11e5' )         : 'the distance covered by one degree of latitude on Earth\'s surface',
    mpmathify( '1.63e5' )         : 'the length of the Suez Canal',
    mpmathify( '9.746e5' )        : 'the greatest diameter of the dwarf planet Ceres',
    mpmathify( '2.390e6' )        : 'the diameter of dwarf planet Pluto',
    mpmathify( '3.480e6' )        : 'the diameter of the Moon',
    mpmathify( '5.200e6' )        : 'the typical distance covered by the winner of the 24 Hours of Le Mans automobile endurance race',
    mpmathify( '6.400e6' )        : 'the length of the Great Wall of China',
    mpmathify( '6.600e6' )        : 'the approximate length of the two longest rivers, the Nile and the Amazon',
    mpmathify( '7.821e6' )        : 'the length of the Trans-Canada Highway',
    mpmathify( '9.288e6' )        : 'the length of the Trans-Siberian Railway, longest in the world',
    mpmathify( '1.2756e7' )       : 'the equatorial diameter of the Earth',
    mpmathify( '4.0075e7' )       : 'the length of the Earth\'s equator',
    mpmathify( '1.42984e8' )      : 'the diameter of Jupiter',
    mpmathify( '299792458' )      : 'a light-second, the distance travelled by light in one second',
    mpmathify( '3.84e8' )         : 'the Moon\'s orbital distance from Earth',
    mpmathify( '1.39e9' )         : 'the diameter of the Sun',
    mpmathify( '1.79875e10' )     : 'the approximately one light-minute',
    mpmathify( '1.4959787e11' )   : 'an astronomical unit (AU), the mean distance between Earth and Sun',
    mpmathify( '9.0e11' )         : 'the optical diameter of Betelgeuse (~600x Sun)',
    mpmathify( '1.4e12' )         : 'the orbital distance of Saturn from Sun',
    mpmathify( '1.96e12' )        : 'the estimated optical diameter of VY Canis Majoris (1420x Sun)',
    mpmathify( '2.3e12' )         : 'the estimated optical diameter of NML Cygni (1650x Sun)',
    mpmathify( '2.37e12' )        : 'the median point of the optical diameter of UY Scuti, as of 2014 the largest known star',
    mpmathify( '5.9e12' )         : 'the orbital distance of Pluto from Sun',
    mpmathify( '7.5e12' )         : 'the estimated outer boundary of the Kuiper belt, inner boundary of the Oort cloud (~50 AU)',
    mpmathify( '1.0e13' )         : 'the diameter of our Solar System as a whole',
    mpmathify( '1.625e13' )       : 'the distance of the Voyager 1 spacecraft from Sun (as of Feb 2009), the farthest man-made object so far',
    mpmathify( '6.203e13' )       : 'the estimated radius of the event horizon of the supermassive black hole in NGC 4889, the largest known black hole to date',
    mpmathify( '1.8e14' )         : 'the size of the debris disk around the star 51 Pegasi',
    mpmathify( '7.5e15' )         : 'the supposed outer boundary of the Oort cloud (~50,000 AU)',
    mpmathify( '9.46e15' )        : 'a light year, the distance travelled by light in one year; at its current speed, Voyager 1 would need 17,500 years to travel this distance',
    mpmathify( '3.0857e16' )      : 'a parsec',
    mpmathify( '3.99e16' )        : 'the distance to nearest star (Proxima Centauri)',
    mpmathify( '4.13e16' )        : 'the distance to nearest discovered extrasolar planet (Alpha Centauri Bb) as of March 2013',
    mpmathify( '1.93e17' )        : 'the distance to nearest discovered extrasolar planet with potential to support life as we know it (Gliese 581 d) as of October 2010',
    mpmathify( '6.15e17' )        : 'the approximate radius of humanity\'s radio bubble, caused by high-power TV broadcasts leaking through the atmosphere into outer space',
    mpmathify( '1.9e18' )         : 'the distance to nearby solar twin (HIP 56948), a star with properties virtually identical to our Sun',
    mpmathify( '9.46e18' )        : 'the average thickness of Milky Way Galaxy',
    mpmathify( '3.086e22' )       : 'a kiloparsec',
    mpmathify( '1.135e20' )       : 'the thickness of Milky Way Galaxy\'s gaseous disk',
    mpmathify( '9.5e20' )         : 'the diameter of galactic disk of Milky Way Galaxy',
    mpmathify( '1.54e21' )        : 'the distance to SN 1987A, the most recent naked eye supernova',
    mpmathify( '1.62e21' )        : 'the distance to the Large Magellanic Cloud (a dwarf galaxy orbiting the Milky Way)',
    mpmathify( '1.66e21' )        : 'the distance to the Small Magellanic Cloud (another dwarf galaxy orbiting the Milky Way)',
    mpmathify( '6.15e21' )        : 'the diameter of the low surface brightness disc halo of the giant spiral galaxy Malin 1',
    mpmathify( '1.324e22' )       : 'the radius of the diffuse stellar halo of IC 1101, one of the largest known galaxies',
    mpmathify( '2.376e22' )       : 'the distance to the Andromeda Galaxy',
    mpmathify( '3.086e22' )       : 'a megaparsec',
    mpmathify( '5.0e22' )         : 'the diameter of Local Group of galaxies',
    mpmathify( '4.50e23' )        : 'the approximate distance to Virgo cluster of galaxies',
    mpmathify( '1.9e24' )         : 'the diameter of the Local Supercluster and the largest voids and filaments',
    mpmathify( '5.0e24' )         : 'the diameter of the enormous Horologium Supercluster',
    mpmathify( '9.46e24' )        : 'the diameter of the Pisces-Cetus Supercluster Complex, the supercluster complex where we live',
    mpmathify( '1.3e25' )         : 'the length of the Sloan Great Wall, a giant wall of galaxies (galactic filament)',
    mpmathify( '3.086e25' )       : 'a gigaparsec',
    mpmathify( '3.784e25' )       : 'the length of the Huge-LQG, a group of 73 quasars',
    mpmathify( '9.5e25' )         : 'the estimated light travel distance to certain quasars, length of the Hercules-Corona Borealis Great Wall, a colossal wall of galaxies, the largest and the most massive structure in the observable universe as of 2014',
    mpmathify( '1.27e26' )        : 'the estimated light travel distance to UDFj-39546284, the most distant object ever observed',
    mpmathify( '8.7e26' )         : 'the approximate diameter (comoving distance) of the visible universe',
    mpmathify( '2.4e27' )         : 'the lower bound of the (possibly infinite) radius of the universe, if it is a 3-sphere, according to one estimate using the WMAP data at 95% confidence',
    mpmathify( '3.086e28' )       : 'a teraparsec',
    mpmathify( '7.4e28' )         : 'the lower bound of the homogeneous universe derived from the Planck spacecraft',
}


# //******************************************************************************
# //
# //  luminanceTable
# //
# //  candelas/meter^2 : description
# //
# //  https://en.wikipedia.org/wiki/Luminance
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28luminance%29
# //
# //******************************************************************************

luminanceTable = {
    mpmathify( '1.0e-6' ) : 'the luminance of the absolute threshold of human vision',
    mpmathify( '4.0e-4' ) : 'the luminance of the darkest sky',
    mpmathify( '1.0e-3' ) : 'the luminance of a typical night sky',
    mpmathify( '1.4e-3' ) : 'the luminance of a typical photographic scene lit by full moon',
    mpmathify( '5.0e-3' ) : 'the approximate luminance of the scotopic/mesopic threshold',
    mpmathify( '4.0e-2' ) : 'the luminance of the phosphorescent markings on a watch dial after 1 h in the dark',
    mpmathify( '2.0' )    : 'the luminance of floodlit buildings, monuments, and fountains',
    mpmathify( '5.0' )    : 'the approximate luminance of the mesopic/photopic threshold',
    mpmathify( '25' )     : 'the luminance of a typical photographic scene at sunrise or sunset',
    mpmathify( '30' )     : 'the luminance of a green electroluminescent source',
    mpmathify( '55' )     : 'the standard SMPTE cinema screen luminance',
    mpmathify( '80' )     : 'the luminance of monitor white in the sRGB reference viewing environment',
    mpmathify( '250' )    : 'the peak luminance of a typical LCD monitor',
    mpmathify( '700' )    : 'the luminance of a typical photographic scene on overcast day',
    mpmathify( '2000' )   : 'the luminance of an average cloudy sky',
    mpmathify( '2500' )   : 'the luminance of the Moon\'s surface',
    mpmathify( '5000' )   : 'the luminance of a typical photographic scene in full sunlight',
    mpmathify( '7000' )   : 'the luminance of an average clear sky',
    mpmathify( '1.0e4' )  : 'the luminance of a white illuminated cloud',
    mpmathify( '1.2e4' )  : 'the luminance of a fluorescent lamp',
    mpmathify( '7.5e4' )  : 'the luminance of a low pressure sodium-vapor lamp',
    mpmathify( '1.3e5' )  : 'the luminance of a frosted incandescent light bulb',
    mpmathify( '6.0e5' )  : 'the luminance of the solar disk at the horizon',
    mpmathify( '7.0e6' )  : 'the luminance of the filament of a clear incandescent lamp',
    mpmathify( '1.0e8' )  : 'the luminance of brightness which can cause retinal damage',
    mpmathify( '1.6e9' )  : 'the luminance of the solar disk at noon',
}


# //******************************************************************************
# //
# //  luminousFluxTable
# //
# //  lumens : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28luminous_flux%29
# //  https://en.wikipedia.org/wiki/Lumen_(unit)
# //
# //******************************************************************************

luminousFluxTable = {
    mpmathify( '0.025' )      : 'the luminous flux of the light of a firefly',
    mpmathify( '12.57' )      : 'the luminous flux of the light of a candle',
    mpmathify( '200' )        : 'the luminous flux of a 25 W incandescent light bulb',
    mpmathify( '450' )        : 'the luminous flux of a 40 W incandescent light bulb',
    mpmathify( '800' )        : 'the luminous flux of a 60 W incandescent light bulb',
    mpmathify( '1100' )       : 'the luminous flux of a 75 W incandescent light bulb',
    mpmathify( '1600' )       : 'the luminous flux of a 100 W incandescent light bulb',
    mpmathify( '2400' )       : 'the luminous flux of a 150 W incandescent light bulb',
    mpmathify( '3100' )       : 'the luminous flux of a 200 W incandescent light bulb',
    mpmathify( '4000' )       : 'the luminous flux of a 300 W incandescent light bulb',
    mpmathify( '6.0e5' )      : 'the luminous flux of an IMAX projector bulb',
    mpmathify( '4.23e10' )    : 'the luminous flux of the Luxor Sky Beam spotlight array in Las Vegas',
    mpmathify( '4.6e24' )     : 'the luminous flux of the dimmest class of red dwarf star',
    mpmathify( '3.0768e28' )  : 'the luminous flux of the Sun',
    mpmathify( '1.382e38' )   : 'the luminous flux of a Type 1a supernova',
    mpmathify( '1.26e41' )    : 'the luminous flux of Quasar 3C 273',
}


# //******************************************************************************
# //
# //  luminousIntensityTable
# //
# //  candelas : description
# //
# //  https://en.wikipedia.org/wiki/Candela#Examples
# //
# //******************************************************************************

luminousIntensityTable = {
    mpmathify( '5.0e-2' ) : 'the luminous intensity of a typical indicator LED',
    mpmathify( '1.0' )    : 'the approximate luminous intensity of a candle',
    mpmathify( '15' )     : 'the intensity of an "ultra-bright" LED',
    mpmathify( '75' )     : 'the luminous intensity of a typical fire alarm strobe',
}


# //******************************************************************************
# //
# //  magneticFieldStrengthTable
# //
# //  amperes/meter : description
# //
# //******************************************************************************

magneticFieldStrengthTable = {
}


# //******************************************************************************
# //
# //  magneticFluxTable
# //
# //  webers : description
# //
# //******************************************************************************

magneticFluxTable = {
}


# //******************************************************************************
# //
# //  magneticFluxDensityTable
# //
# //  teslas : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28magnetic_field%29
# //
# //******************************************************************************

magneticFluxDensityTable = {
    mpmathify( '5e-18' )        : 'the magnetic flux density measurement precision attained for NASA\'s Gravity Probe B',
    mpmathify( '3.1869e-5' )    : 'the magnetic flux density of the Earth\'s magnetic field at 0 degrees long., 0 degrees lat.',
    mpmathify( '5.0e-3' )       : 'the magnetic flux density of a typical refrigerator magnet',
    mpmathify( '0.3' )          : 'the magnetic flux density of solar sunspots',
    mpmathify( '3.0' )          : 'the magnetic flux density of a common magnetic resonance imaging system',
    mpmathify( '8.0' )          : 'the magnetic flux density of the Large Hadron Collider magnets',
    mpmathify( '16' )           : 'the magnetic flux density strong enough to levitate a frog',
    mpmathify( '2800' )         : 'the magnetic flux density of the largest magnetic field produced in a laboratory',
    mpmathify( '1.0e8' )        : 'the lower range of magnetic flux density in a magnetar',
    mpmathify( '1.0e11' )       : 'the upper range of magnetic flux density in a magnetar',
}


# //******************************************************************************
# //
# //  massTable
# //
# //  kilograms : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28mass%29
# //
# //******************************************************************************

massTable = {
    mpmathify( '4.2e-40' )      : 'the mass equivalent of the energy of a photon at the peak of the spectrum of the cosmic microwave background radiation (0.235 meV/c2)',
    mpmathify( '1.8e-36' )      : 'the mass equivalent of one electronvolt (1 eV/c^2)',
    mpmathify( '3.6e-36' )      : 'the mass of an electron neutrino, (upper limit, 2 eV/c2)',
    mpmathify( '9.11e-31' )     : 'the mass of an electron (511 keV/c2), the lightest elementary particle with a measured nonzero rest mass',
    mpmathify( '5.5e-30' )      : 'the mass of an up quark (as a current quark, upper limit of 1.7-3.1 MeV/c2)',
    mpmathify( '1.9e-28' )      : 'the mass of a muon (106 MeV/c2)',
    mpmathify( '1.661e-27' )    : 'the atomic mass unit (u) or dalton (Da)',
    mpmathify( '1.673e-27' )    : 'the mass of proton (938.3 MeV/c2)',
    mpmathify( '1.674e-27' )    : 'the mass of a hydrogen atom, the lightest atom',
    mpmathify( '1.675e-27' )    : 'the mass of a neutron (939.6 MeV/c2)',
    mpmathify( '1.2e-26' )      : 'the mass of a lithium atom (6.941 u)',
    mpmathify( '3.0e-26' )      : 'the mass of a water molecule (18.015 u)',
    mpmathify( '8.0e-26' )      : 'the mass of a titanium atom (47.867 u)',
    mpmathify( '1.1e-25' )      : 'the mass of a copper atom (63.546 u)',
    mpmathify( '1.6e-25' )      : 'the mass of a Z boson (91.2 GeV/c2)',
    mpmathify( '3.1e-25' )      : 'the mass of a top quark (173 GeV/c2), the heaviest known elementary particle',
    mpmathify( '3.2e-25' )      : 'the mass of a caffeine molecule (194 u)',
    mpmathify( '3.5e-25' )      : 'the mass of a lead-208 atom, the heaviest stable isotope known',
    mpmathify( '1.2e-24' )      : 'the mass of a buckyball molecule (720 u)',
    mpmathify( '1.4e-23' )      : 'the mass of ubiquitin, a small protein (8.6 kDa)[13]',
    mpmathify( '5.5e-23' )      : 'the mass of a typical protein (median size of roughly 300 amino acids ~= 33 kDa)',
    mpmathify( '1.1e-22' )      : 'the mass of a hemoglobin A molecule in blood (64.5 kDa)',
    mpmathify( '1.65e-21' )     : 'the mass of a double-stranded DNA molecule consisting of 1,578 base pairs (995,000 daltons)',
    mpmathify( '4.3e-21' )      : 'the mass of a prokaryotic ribosome (2.6 MDa)',
    mpmathify( '7.1e-21' )      : 'the mass of a eukaryotic ribosome (4.3 MDa)',
    mpmathify( '7.6e-21' )      : 'the mass of a Brome mosaic virus, a small virus (4.6 MDa)',
    mpmathify( '3.0e-20' )      : 'the mass of the Synaptic vesicle in rats (16.1 +/- 3.8 MDa)',
    mpmathify( '6.8e-20' )      : 'the mass of the Tobacco mosaic virus (41 MDa)',
    mpmathify( '1.1e-19' )      : 'the mass of the nuclear pore complex in yeast (66 MDa)',
    mpmathify( '2.5e-19' )      : 'the mass of a Human adenovirus (150 MDa)',
    mpmathify( '1.0e-18' )      : 'the mass of an HIV-1 virus',
    mpmathify( '4.7e-18' )      : 'the mass of a DNA sequence of length 4.6 Mbp, the length of the E. coli genome',
    mpmathify( '1.0e-17' )      : 'the mass of a Vaccinia virus, a large virus',
    mpmathify( '1.1e-17' )      : 'the mass equivalent of 1 joule',
    mpmathify( '3.0e-16' )      : 'the mass of a Prochlorococcus cyanobacteria, the smallest photosynthetic organism on Earth',
    mpmathify( '1.0e-15' )      : 'the mass of an E. coli bacterium (wet weight)',
    mpmathify( '6.0e-15' )      : 'the mass of DNA in a typical diploid human cell (approximate)',
    mpmathify( '2.2e-14' )      : 'the mass of a human sperm cell',
    mpmathify( '6.0e-14' )      : 'the mass of a yeast cell (quite variable)',
    mpmathify( '1.5e-13' )      : 'the mass of a Dunaliella salina, a green algae (dry weight)',
    mpmathify( '1.0e-12' )      : 'the mass of an average human cell (1 nanogram)',
    mpmathify( '8.0e-12' )      : 'the mass of a grain of birch pollen',
    mpmathify( '2.5e-10' )      : 'the mass of a grain of maize pollen',
    mpmathify( '3.5e-10' )      : 'the mass of a very fine grain of sand (0.063 mm diameter, 350 nanograms)',
    mpmathify( '3.6e-9' )       : 'the mass of a human ovum',
    mpmathify( '2.0e-8' )       : 'the uncertainty in the mass of the International Prototype Kilogram (IPK) (+/-20 ug)',
    mpmathify( '2.2e-8' )       : 'the Planck mass',
    mpmathify( '7.0e-8' )       : 'the mass of one eyebrow hair (approximate)',
    mpmathify( '2.5e-7' )       : 'the mass of a fruit fly (dry weight)',
    mpmathify( '2.5e-6' )       : 'the mass of a mosquito, common smaller species (about 2.5 milligrams)',
    mpmathify( '2.0e-5' )       : 'the mass of an adult housefly (Musca domestica, 21.4 milligrams)',
    mpmathify( '2.0e-4' )       : 'one metric carat (200 milligrams)',
    mpmathify( '5.0e-4' )       : 'the mass of a raisin (approximately 0.5 gram)',
    mpmathify( '1.0e-3' )       : 'the mass of one cubic centimeter of water (1 gram)',
    mpmathify( '1.0e-3' )       : 'the mass of a U.S. dollar bill (1 gram)',
    mpmathify( '7.5e-3' )       : 'the mass of a Euro coin (7.5 grams)',
    mpmathify( '8.1e-3' )       : 'the mass of a U.S. dollar coin (8.1 grams)',
    mpmathify( '2.835e-2' )     : 'one ounce (avoirdupois) (28.35 grams)',
    mpmathify( '4.7e-2' )       : 'the mass equivalent of one megaton of TNT equivalent',
    mpmathify( '1.5e-1' )       : 'the mass of a typical orange (100-200 grams)',
    mpmathify( '4.54e-1' )      : 'one pound (avoirdupois) (454 grams)',
    mpmathify( '1.0' )          : 'the mass of one litre of water',
    mpmathify( '2.0' )          : 'the mass of a Chihuahua, the smallest breed of dog (Chihuahua)',
    mpmathify( '3.25' )         : 'the mass of a newborn human baby',
    mpmathify( '4.0' )          : 'the mass of a women\'s shot',
    mpmathify( '4.5' )          : 'the mass of a typical housecat',
    mpmathify( '7.26' )         : 'the mass of a men\'s shot',
    mpmathify( '1.8e1' )        : 'the mass of a medium-sized dog',
    mpmathify( '2.0e1' )        : 'the mass of a typical CRT computer monitor',
    mpmathify( '1.8e2' )        : 'the mass of a typical mature male lion, female (130 kg) and male (180 kg)',
    mpmathify( '3.5e2' )        : 'the mass of a typical grand piano',
    mpmathify( '6.5e2' )        : 'the mass of a typical dairy cow',
    mpmathify( '9.072e2' )      : 'one short ton (2000 pounds - U.S.)',
    mpmathify( '1.0e3' )        : 'one metric ton/tonne, 1 cubic metre of water',
    mpmathify( '1.2e3' )        : 'the mass of a typical passenger cars',
    mpmathify( '5.5e3' )        : 'the mass of an average male African bush elephant',
    mpmathify( '1.1e4' )        : 'the mass of the Hubble Space Telescope (11 tonnes)',
    mpmathify( '1.2e4' )        : 'the mass of the largest elephant on record (12 tonnes)',
    mpmathify( '1.4e4' )        : 'the mass of Big Ben\'s bell (14 tonnes)',
    mpmathify( '4.4e4' )        : 'the maximum gross mass (truck + load combined) of a semi-trailer truck in the EU (40-44 tonnes)',
    mpmathify( '7.3e4' )        : 'the mass of the largest dinosaur, Argentinosaurus (73 tonnes)',
    mpmathify( '1.8e5' )        : 'the mass of the blue whale, the largest animal ever (180 tonnes)',
    mpmathify( '4.2e5' )        : 'the mass of the International Space Station (417 tonnes)',
    mpmathify( '4.39985e5' )    : 'the mass of the takeoff weight of a Boeing 747-8',
    mpmathify( '6.0e5' )        : 'the mass of the world\'s heaviest aircraft: Antonov An-225 (maximum take-off mass: 600 tonnes, payload: 250 tonnes)',
    mpmathify( '1.0e6' )        : 'the mass of the trunk of the giant sequoia tree, "General Sherman", largest living tree by trunk volume (1121 tonnes)',
    mpmathify( '2.041e6' )      : 'the launch mass of the Space Shuttle (2041 tonnes)',
    mpmathify( '6.0e6' )        : 'the mass of the largest clonal colony, the quaking aspen named Pando (largest living organism, 6000 tonnes)',
    mpmathify( '7.8e6' )        : 'the mass of a Virginia-class nuclear submarine (submerged weight)',
    mpmathify( '1.0e7' )        : 'the mass of the annual production of Darjeeling tea',
    mpmathify( '5.2e7' )        : 'the mass of the RMS Titanic when fully loaded (52,000 tonnes)',
    mpmathify( '9.97e7' )       : 'the mass of the heaviest train ever, Australia\'s BHP Iron Ore, 2001 record (99,700 tonnes)',
    mpmathify( '6.6e8' )        : 'the mass of the largest ship and largest mobile man-made object, Seawise Giant, when fully loaded (660,000 tonnes)',
    mpmathify( '4.3e9' )        : 'the mass of matter converted into energy by the Sun each second',
    mpmathify( '6.0e9' )        : 'the mass of the Great Pyramid of Giza',
    mpmathify( '6.0e10' )       : 'the mass of the concrete in the Three Gorges Dam, the world\'s largest concrete structure',
    mpmathify( '1.0e11' )       : 'the mass of a primordial black hole with an evaporation time equal to the age of the universe',
    mpmathify( '2.0e11' )       : 'the mass of the amount of water stored in London storage reservoirs (0.2 km3)',
    mpmathify( '4.0e11' )       : 'the total mass of the human world population',
    mpmathify( '5.0e11' )       : 'the total biomass of Antarctic krill',
    mpmathify( '1.55e12' )      : 'the global biomass of fish (estaimted)',
    mpmathify( '4.0e12' )       : 'the mass of the world crude oil production in 2009 (3,843 Mt)',
    mpmathify( '5.5e12' )       : 'the mass of a teaspoon (5 ml) of neutron star material (5.5 billion tonnes)',
    mpmathify( '1.0e13' )       : 'the mass of a 1km tall mountain (very approximate)',
    mpmathify( '1.05e14' )      : 'the total mass of carbon fixed in organic compounds by photosynthesis each year on Earth',
    mpmathify( '7.2e14' )       : 'the mass of the total carbon stored in Earth\'s atmosphere',
    mpmathify( '2.0e15' )       : 'the mass of the total carbon stored in the terrestrial biosphere',
    mpmathify( '3.5e15' )       : 'the mass of the total carbon stored in coal deposits worldwide',
    mpmathify( '1.0e16' )       : 'the mass of the total carbon content of all organisms on Earth (rough estimate)',
    mpmathify( '3.8e16' )       : 'the mass of the total carbon stored in the oceans',
    mpmathify( '1.6e17' )       : 'the mass of Prometheus, a shepherd satellite for the inner edge of Saturn\'s F Ring',
    mpmathify( '5.1e18' )       : 'the mass of the Earth\'s atmosphere',
    mpmathify( '5.6e18' )       : 'the mass of Hyperion, a moon of Saturn',
    mpmathify( '3.0e19' )       : 'the mass of Juno, the third largest asteroid in the asteroid belt',
    mpmathify( '3.0e19' )       : 'the mass of the rings of Saturn',
    mpmathify( '9.4e20' )       : 'the mass of Ceres, the largest asteroid in the asteroid belt',
    mpmathify( '1.4e21' )       : 'the mass of the Earth\'s oceans',
    mpmathify( '1.5e21' )       : 'the mass of Charon, the largest moon of Pluto',
    mpmathify( '3.3e21' )       : 'the mass of the Asteroid Belt',
    mpmathify( '1.3e22' )       : 'the mass of Pluto',
    mpmathify( '2.1e22' )       : 'the mass of Triton, largest moon of Neptune',
    mpmathify( '7.3e22' )       : 'the mass of Earth\'s Moon',
    mpmathify( '1.3e23' )       : 'the mass of Titan, largest moon of Saturn',
    mpmathify( '1.5e23' )       : 'the mass of Ganymede, largest moon of Jupiter',
    mpmathify( '3.3e23' )       : 'the mass of Mercury',
    mpmathify( '6.4e23' )       : 'the mass of Mars',
    mpmathify( '4.9e24' )       : 'the mass of Venus',
    mpmathify( '6.0e24' )       : 'the mass of Earth',
    mpmathify( '3.0e25' )       : 'the mass of Oort cloud',
    mpmathify( '8.7e25' )       : 'the mass of Uranus',
    mpmathify( '1.0e26' )       : 'the mass of Neptune',
    mpmathify( '5.7e26' )       : 'the mass of Saturn',
    mpmathify( '1.9e27' )       : 'the mass of Jupiter',
    mpmathify( '8.0e28' )       : 'the mass of a typical brown dwarf',
    mpmathify( '3.0e29' )       : 'the mass of Barnard\'s Star, a nearby red dwarf',
    mpmathify( '2.0e30' )       : 'the mass of the Sun',
    mpmathify( '2.8e30' )       : 'the mass of Chandrasekhar limit (1.4 solar masses)',
    mpmathify( '4.0e31' )       : 'the mass of Betelgeuse, a red supergiant star (20 solar masses)',
    mpmathify( '2.5e32' )       : 'the mass of Pistol Star, one of the most massive known stars',
    mpmathify( '1.6e33' )       : 'the Pleiades star cluster (800 solar masses)',
    mpmathify( '1.0e35' )       : 'the mass of a typical globular cluster in the Milky Way',
    mpmathify( '2.4e36' )       : 'the mass of the Gould Belt of stars, including the Sun (1.2e6 solar masses)',
    mpmathify( '7.5e36' )       : 'the mass of the black hole at the center of the Milky Way, associated with the radio source Sagittarius A* (3.7 +/- 0.2e6 solar masses)',
    mpmathify( '4.17e40' )      : 'the mass of NGC 4889, the largest measured supermassive black hole (2.1e10 solar masses)',
    mpmathify( '4.0e41' )       : 'the visible mass of the Milky Way galaxy',
    mpmathify( '1.2e42' )       : 'the mass of Milky Way galaxy (5.8e11 solar masses)',
    mpmathify( '2.5e42' )       : 'the mass of the Local Group of galaxies, including the Milky Way',
    mpmathify( '1.5e45' )       : 'the mass of the Local or Virgo Supercluster of galaxies, including the Local Group',
    mpmathify( '6.0e52' )       : 'the mass of the observable universe',
}


# //******************************************************************************
# //
# //  powerTable
# //
# //  watts : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28power%29
# //
# //******************************************************************************

powerTable = {
    mpmathify( '1.0e-20' )  : 'the approximate power of Galileo space probe\'s radio signal (when at Jupiter) as received on earth by a 70-meter DSN antenna',
    mpmathify( '1.0e-18' )  : 'the approximate power scale at which operation of nanoelectromechanical systems are overwhelmed by thermal fluctuations',
    mpmathify( '1.0e-16' )  : 'the GPS signal strength measured at the surface of the Earth,[clarification needed] roughly equivalent to viewing a 25-watt light bulb from a distance of 10,000 miles',
    mpmathify( '2.5e-15' )  : 'the minimum discernible signal at the antenna terminal of a good FM radio receiver',
    mpmathify( '1.0e-14' )  : 'the approximate lower limit of power reception on digital spread-spectrum cell phones (-110 dBm)',
    mpmathify( '1.0e-12' )  : 'the average power consumption of a human cell (-90 dBm)',
    mpmathify( '1.84e-11' ) : 'the power lost in the form of synchrotron radiation by a proton revolving in the Large Hadron Collider at 7000 GeV',
    mpmathify( '1.50e-10' ) : 'the power entering a human eye from a 100-watt lamp 1 km away',
    mpmathify( '1.5e-8' )   : 'the upper range of power consumption of 8-bit PIC microcontroller chips when in "sleep" mode',
    mpmathify( '1.0e-6' )   : 'the approximate consumption of a quartz or mechanical wristwatch (-30 dBm)',
    mpmathify( '3.0e-6' )   : 'the power of the cosmic microwave background radiation per square meter',
    mpmathify( '5.0e-3' )   : 'the power of the laser in a CD-ROM drive',
    mpmathify( '1.0e-2' )   : 'the power of the laser in a DVD player',
    mpmathify( '7.0e-2' )   : 'the antenna power in a typical consumer wireless router',
    mpmathify( '5.0e-2' )   : 'the maximum allowed carrier output power of an FRS radio',
    mpmathify( '2.0' )      : 'the maximum allowed carrier power output of a MURS radio (2 W)',
    mpmathify( '4.0' )      : 'the power consumption of an incandescent night light (4 W)',
    mpmathify( '4.0' )      : 'the maximum allowed carrier power output of a 10-meter CB radio (4 W)',
    mpmathify( '8.0' )      : 'the power output of human-powered equipment using a hand crank (8 W)',
    mpmathify( '14' )       : 'the power consumption of a typical household compact fluorescent light bulb (14 W)',
    mpmathify( '30' )       : 'the approximate power consumption of the human brain',
    mpmathify( '60' )       : 'the power consumption of a 60W incandescent light bulb',
    mpmathify( '100' )      : 'the approximate basal metabolic rate of an adult human body',
    mpmathify( '120' )      : 'the electric power output of 1 square meter solar panel in full sunlight (approx. 12% efficiency), at sea level',
    mpmathify( '130' )      : 'the peak power consumption of a Pentium 4 CPU',
    mpmathify( '200' )      : 'the average power output of a stationary bicycle average power output',
    mpmathify( '290' )      : 'one thousand BTU/hour',
    mpmathify( '400' )      : 'the legal limit of power output of an amateur radio station in the United Kingdom',
    mpmathify( '500' )      : 'the power output (useful work plus heat) of a person working hard physically',
    mpmathify( '745.7' )    : 'one horsepower',
    mpmathify( '750' )      : 'the approximate amount of sunshine falling on a square metre of the Earth\'s surface at noon on a clear day in March for northern temperate latitudes',
    mpmathify( '909' )      : 'the peak output power of a healthy human (nonathlete) during a 30-second cycle sprint at 30.1 degree Celsius',
    mpmathify( '1.1e3' )    : 'the power of a typical microwave oven',
    mpmathify( '1.366e3' )  : 'the power per square metre received from the Sun at the Earth\'s orbit',
    mpmathify( '1.5e3' )    : 'the legal limit of power output of an amateur radio station in the United States (1.5 kW)',
    mpmathify( '2.0e3' )    : 'the approximate short-time power output of sprinting professional cyclists and weightlifters doing snatch',
    mpmathify( '2.4e3' )    : 'the average power consumption per person worldwide in 2008',
    mpmathify( '4.95e3' )   : 'the average photosynthetic power output per square kilometer of ocean',
    mpmathify( '3.6e3' )    : 'the synchrotron radiation power lost per ring in the Large Hadron Collider at 7000 GeV',
    mpmathify( '1.0e4' )    : 'the average power consumption per person in the United States in 2008',
    mpmathify( '2.4e4' )    : 'the average photosynthetic power output per square kilometer of land',
    mpmathify( '3.0e4' )    : 'the power generated by the four motors of GEN H-4 one-man helicopter',
    mpmathify( '1.0e5' )    : 'the highest allowed ERP for an FM band radio station in the United States',
    mpmathify( '1.67e5' )   : 'the power consumption of UNIVAC 1 computer',
    mpmathify( '2.0e5' )    : 'the upper limit of power output for typical automobiles',
    mpmathify( '4.5e5' )    : 'the approximate maximum power output of a large 18-wheeler truck engine',
    mpmathify( '1.3e6' )    : 'the power output of P-51 Mustang fighter aircraft',
    mpmathify( '1.5e6' )    : 'the peak power output of GE\'s standard wind turbine',
    mpmathify( '2.4e6' )    : 'the peak power output of a Princess Coronation class steam locomotive (approx 3.3K EDHP on test) (1937)',
    mpmathify( '2.5e6' )    : 'the peak power output of a blue whale',
    mpmathify( '3.0e6' )    : 'the mechanical power output of a diesel locomotive',
    mpmathify( '1.0e7' )    : 'the highest ERP allowed for an UHF television station',
    mpmathify( '1.03e7' )   : 'the electrical power output of Togo',
    mpmathify( '1.22e7' )   : 'the approximate power available to a Eurostar 20-carriage train',
    mpmathify( '1.6e7' )    : 'the rate at which a typical gasoline pump transfers chemical energy to a vehicle',
    mpmathify( '2.6e7' )    : 'the peak power output of the reactor of a Los Angeles-class nuclear submarine',
    mpmathify( '7.5e7' )    : 'the maximum power output of one GE90 jet engine as installed on the Boeing 777',
    mpmathify( '1.4e8' )    : 'the average power consumption of a Boeing 747 passenger aircraft',
    mpmathify( '1.9e8' )    : 'the peak power output of a Nimitz-class aircraft carrier',
    mpmathify( '9.0e8' )    : 'the electric power output of a CANDU nuclear reactor',
    mpmathify( '9.59e8' )   : 'the average electrical power consumption of Zimbabwe in 1998',
    mpmathify( '1.3e9' )    : 'the electric power output of Manitoba Hydro Limestone hydroelectric generating station',
    mpmathify( '2.074e9' )  : 'the peak power generation of Hoover Dam',
    mpmathify( '2.1e9' )    : 'the peak power generation of Aswan Dam',
    mpmathify( '4.116e9' )  : 'the installed capacity of Kendal Power Station, the world\'s largest coal-fired power plant',
    mpmathify( '8.21e9' )   : 'the capacity of the Kashiwazaki-Kariwa Nuclear Power Plant, the world\'s largest nuclear power plant',
    mpmathify( '1.17e10' )  : 'the power produced by the Space Shuttle in liftoff configuration (9.875 GW from the SRBs; 1.9875 GW from the SSMEs)',
    mpmathify( '1.26e10' )  : 'the electrical power generation of the Itaipu Dam',
    mpmathify( '1.27e10' )  : 'the average electrical power consumption of Norway in 1998',
    mpmathify( '1.83e10' )  : 'the peak electrical power generation of the Three Gorges Dam, the world\'s largest hydroelectric power plant of any type',
    mpmathify( '5.5e10' )   : 'the peak daily electrical power consumption of Great Britain in November 2008',
    mpmathify( '7.4e10' )   : 'the total installed wind turbine capacity at end of 2006',
    mpmathify( '1.016e11' ) : 'the peak electrical power consumption of France (February 8, 2012 at 7:00 pm)',
    mpmathify( '1.90e11' )  : 'the average power consumption of the first stage of the Saturn V rocket',
    mpmathify( '7.00e11' )  : 'the cumulative basal metabolic rate of all humans as of 2013 (7 billion people)',
    mpmathify( '2.0e12' )   : 'the approximate power generated between the surfaces of Jupiter and its moon Io due to Jupiter\'s magnetic field',
    mpmathify( '3.34e12' )  : 'the average total (gas, electricity, etc.) power consumption of the US in 2005',
    mpmathify( '1.6e13' )   : 'the average total power consumption of the human world in 2010',
    mpmathify( '4.4e13' )   : 'the average total heat flux from Earth\'s interior',
    mpmathify( '7.5e13' )   : 'the global net primary production (= biomass production) via photosynthesis',
    mpmathify( '1.25e14' )  : 'the typical rate of heat energy release by a hurricane',
    mpmathify( '2.90e14' )  : 'the power the Z machine reaches in 1 billionth of a second when it is fired',
    mpmathify( '3.0e14' )   : 'the power reached by the extremely high-power Hercules laser from the University of Michigan.',
    mpmathify( '1.1e15' )   : 'the world\'s most powerful laser pulses by laser still in operation (claimed on March 31, 2008 by Texas Center for High Intensity Laser Science at The University of Texas at Austin)',
    mpmathify( '1.25e15' )  : 'the world\'s most powerful laser pulses (claimed on May 23, 1996 by Lawrence Livermore Laboratory)',
    mpmathify( '1.4e15' )   : 'the estimated heat flux transported by the Gulf Stream.',
    mpmathify( '4.0e15' )   : 'the estimated total heat flux transported by Earth\'s atmosphere and oceans away from the equator towards the poles',
    mpmathify( '5.0e15' )   : 'the estimated total power output of a Type-I civilization on the Kardashev scale',
    mpmathify( '1.74e17' )  : 'the total power received by Earth from the Sun',
    mpmathify( '2.0e17' )   : 'the power of the Extreme Light Infrastructure laser',
    mpmathify( '1.35e23' )  : 'the approximate luminosity of Wolf 359',
    mpmathify( '3.38e25' )  : 'the peak power output of the Tsar Bomba, the largest nuclear weapon ever built',
    mpmathify( '5.0e25' )   : 'the estimated total power output of a Type-II civilization on the Kardashev scale',
    mpmathify( '3.846e26' ) : 'the luminosity of the Sun',
    mpmathify( '3.31e31' )  : 'the approximate luminosity of Beta Centauri',
    mpmathify( '1.23e32' )  : 'the approximate luminosity of Deneb',
    mpmathify( '5.0e36' )   : 'the approximate luminosity of the Milky Way galaxy',
    mpmathify( '1.0e40' )   : 'the approximate luminosity of a quasar',
    mpmathify( '1.0e42' )   : 'the approximate luminosity of the Local Supercluster',
    mpmathify( '1.0e45' )   : 'the approximate luminosity of a gamma-ray burst',
    mpmathify( '2.0e49' )   : 'the approximate total luminosity of all the stars in the observable universe',
    mpmathify( '3.63e52' )  : 'the Planck power',
}


# //******************************************************************************
# //
# //  pressureTable
# //
# //  pascals : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28pressure%29
# //  https://en.wikipedia.org/wiki/Sound_pressure
# //
# //******************************************************************************

pressureTable = {
    mpmathify( '1.0e-17' )  : 'the estimated pressure in outer space in intergalactic voids',
    mpmathify( '5.0e-15' )  : 'the typical pressure in outer space between stars in the Milky Way',
    mpmathify( '1.0e-12' )  : 'the lowest pressure obtained in laboratory conditions (1 picopascal)',
    mpmathify( '4.0e-11' )  : 'the atmosphere pressure of the Moon at lunar day, very approximately (40 picopascals)',
    mpmathify( '1.0e-10' )  : 'the atmospheric pressure of Mercury, very approximately (100 pPa)',
    mpmathify( '8.0e-10' )  : 'the atmospheric pressure of the Moon at lunar night, very approximately (800 pPa)',
    mpmathify( '1.0e-9' )   : 'the vacuum expected in the beam pipe of the Large Hadron Collider\'s Atlas experiment (< 1 nPa)',
    mpmathify( '1.0e-9' )   : 'the approximate solar wind pressure at Earth\'s distance from the Sun',
    mpmathify( '1.0e-8' )   : 'the pressure inside a vacuum chamber for laser cooling of atoms (magneto-optical trap, 10 nPa)',
    mpmathify( '1.0e-7' )   : 'the highest pressure still considered ultra high vacuum (100 nPa)',
    mpmathify( '1.0e-6' )   : 'the pressure inside a vacuum tube, very approximate, (1 uPa)',
    mpmathify( '1.0e-6' )   : 'the radiation pressure of sunlight on a perfectly reflecting surface at the distance of the Earth',
    mpmathify( '2.0e-5' )   : 'the reference pressure for sound in air, and the threshold of human hearing (0 dB)',
    mpmathify( '1.0e-1' )   : 'the upper limit of high vacuum (100 mPa)',
    mpmathify( '2.0e-1' )   : 'the atmospheric pressure on Pluto (1988 figure; very roughly, 200 mPa)',
    mpmathify( '1.0' )      : 'the pressure exerted by a US dollar bill resting flat on a surface',
    mpmathify( '10' )       : 'the pressure increase per millimeter of a water column at Earth mean sea level',
    mpmathify( '10' )       : 'the pressure due to direct impact of a gentle breeze (~9 mph or 14 km/h)',
    mpmathify( '86' )       : 'the pressure from the weight of a U.S. penny lying flat',
    mpmathify( '100' )      : 'the pressure due to direct impact of a strong breeze (~28 mph or 45 km/h)',
    mpmathify( '120' )      : 'the pressure from the weight of a U.S. quarter lying flat',
    mpmathify( '133.3224' ) : 'one torr ~= 1 mmHg (133.3224 pascals)',
    mpmathify( '300' )      : 'the lung air pressure difference moving the normal breaths of a person (only 0.3% of standard atmospheric pressure)',
    mpmathify( '610' )      : 'the partial vapour pressure at the triple point of water (611.73 Pa)',
    mpmathify( '650' )      : 'a typical atmospheric pressure on Mars, < 1% of atmospheric sea-level pressure on Earth',
    mpmathify( '2.0e3' )    : 'the pressure of popping popcorn (very approximate)',
    mpmathify( '2.6e3' )    : 'the pressure to make water boil at room temperature (22 degrees C) (0.38 psi, 20 mmHg)',
    mpmathify( '5.0e3' )    : 'the blood pressure fluctuation (40 mmHg) between heartbeats for a typical healthy adult (0.8 psi)',
    mpmathify( '6.3e3' )    : 'the pressure where water boils at normal human body temperature (37 degrees C), the pressure below which humans absolutely cannot survive (Armstrong Limit), 0.9 psi',
    mpmathify( '9.8e3' )    : 'the lung pressure that a typical person can exert (74 mmHg, 1.4 psi)',
    mpmathify( '1.0e4' )    : 'the pressure increase per meter of a water column',
    mpmathify( '1.0e4' )    : 'the decrease in air pressure when going from Earth sea level to 1000 m elevation',
    mpmathify( '1.3e4' )    : 'the pressure for human lung, measured for trumpet player making staccato high notes (1.9 psi)',
    mpmathify( '1.6e4' )    : 'the systolic blood pressure in a healthy adult while at rest (< 120 mmHg gauge pressure)',
    mpmathify( '1.93e4' )   : 'the high end of lung pressure, exertable without injury by a healthy person for brief times (2.8 psi)',
    mpmathify( '3.4e4' )    : 'the level of long-duration blast overpressure (from a large-scale explosion) that would cause most buildings to collapse (5 psi)',
    mpmathify( '7.0e4' )    : 'the pressure inside an incandescent light bulb',
    mpmathify( '8.0e4' )    : 'the pressure inside vacuum cleaner at sea level on Earth (80% of standard atmospheric pressure, 11.6 psi)',
    mpmathify( '8.7e4' )    : 'the record low atmospheric pressure for typhoon/hurricane (Typhoon Tip in 1979) (only 86% of standard atmospheric pressure, 12.6 psi)',
    mpmathify( '1.0e5' )    : 'one bar (14.5 psi), approximately equal to the weight of one kilogram (1 kilopond) acting on one square centimeter',
    mpmathify( '3.5e5 ' )   : 'the typical impact pressure of a fist punch (approximate)',
    mpmathify( '2.0e5' )    : 'the typical air pressure in an automobile tire relative to atmosphere (30 psi gauge pressure)',
    mpmathify( '3.0e5' )    : 'the water pressure of a garden hose (50 psi)',
    mpmathify( '5.17e5' )   : 'the carbon dioxide pressure in a champagne bottle',
    mpmathify( '5.2e5' )    : 'the partial vapour pressure at the triple point of carbon dioxide (75 psi)',
    mpmathify( '7.6e5' )    : 'the air pressure in a heavy truck/bus tire relative to atmosphere (110 psi gauge pressure)',
    mpmathify( '8.0e5' )    : 'the vapor pressure of water in a kernel of popcorn when the kernel ruptures',
    mpmathify( '1.1e6' )    : 'the pressure of an average human bite (162 psi)',
    mpmathify( '2.0e6' )    : 'the maximum typical pressure used in boilers of steam locomotives (290 psi)',
    mpmathify( '5.0e6' )    : 'the maximum rated pressure for the Seawold class military nuclear submarine (estimated), at a depth of 500 m (700 psi)',
    mpmathify( '9.2e6' )    : 'the atmospheric pressure of Venus (92 bar, 1,300 psi)',
    mpmathify( '1.0e7' )    : 'the pressure exerted by a 45 kg woman wearing stiletto heels when a heel hits the floor (1,450 psi)',
    mpmathify( '1.5e7' )    : 'the power stroke maximum pressure in diesel truck engine when burning fuel (2,200 psi)',
    mpmathify( '2.0e7' )    : 'the typical pressure used for hydrogenolysis reactions (2,900 psi)',
    mpmathify( '2.1e7' )    : 'the pressure of a typical aluminium scuba tank of pressurized air (210 bar, 3,000 psi)',
    mpmathify( '2.8e7' )    : 'the overpressure caused by the bomb explosion during the Oklahoma City bombing',
    mpmathify( '6.9e7' )    : 'the water pressure withstood by the DSV Shinkai 6500 in visiting ocean depths of > 6500 meters (10,000 psi)',
    mpmathify( '1.1e8' )    : 'the pressure at bottom of Mariana Trench, about 11 km below ocean surface (1,100 bar, 16,000 psi)',
    mpmathify( '2.0e8' )    : 'the approximate pressure inside a reactor for the synthesis of high-pressure polyethylene (HPPE)',
    mpmathify( '2.8e8' )    : 'the maximum chamber pressure during a pistol firing (40,000 psi)',
    mpmathify( '4.0e8' )    : 'the chamber pressure of a late 1910s .50 Browning Machine Gun discharge (58,000 psi)',
    mpmathify( '6.2e8' )    : 'the water pressure used in a water jet cutter (90,000 psi)',
    mpmathify( '1.0e9' )    : 'the pressure of extremely high-pressure chemical reactors (10 kbar)',
    mpmathify( '1.5e9' )    : 'the pressure at which diamond melts using a 3 kJ laser without turning into graphite first',
    mpmathify( '1.5e9' )    : 'the tensile strength of Inconel 625 according to Aircraft metal strength tables and the Mil-Hdbk-5 (220,000 psi)',
    mpmathify( '5.8e9' )    : 'the ultimate tensile strength of the polymer Zylon (840,000 psi)',
    mpmathify( '1.0e10' )   : 'the pressure at which octaoxygen forms at room temperature (100,000 bar)',
    mpmathify( '1.8e10' )   : 'the pressure needed for the first commercially successful synthesis of diamond',
    mpmathify( '2.4e10' )   : 'the lower range of stability for enstatite in its perovskite-structured polymorph, possibly the most common mineral inside the Earth',
    mpmathify( '1.1e11' )   : 'the upper range of stability for enstatite in its perovskite-structured polymorph, possibly the most common mineral inside the Earth',
    mpmathify( '4.0e10' )   : 'the quantum mechanical electron degeneracy pressure in a block of copper',
    mpmathify( '4.8e10' )   : 'the detonation pressure of pure CL-20, the most powerful high explosive in mass production',
    mpmathify( '6.9e10' )   : 'the highest water jet pressure made in research lab (approx. 1 million psi)',
    mpmathify( '9.6e10' )   : 'the pressure at which metallic oxygen forms (960,000 bar)',
    mpmathify( '1.0e11' )   : 'the theoretical tensile strength of a carbon nanotube (CNT)',
    mpmathify( '1.3e11' )   : 'the intrinsic strength of monolayer graphene',
    mpmathify( '3.0e11' )   : 'the pressure attainable with a diamond anvil cell',
    mpmathify( '3.6e11' )   : 'the pressure inside the core of the Earth (3.64 million bar)',
    mpmathify( '5.4e14' )   : 'the pressure inside an Ivy Mike-like nuclear bomb detonation (5.3 billion bar)',
    mpmathify( '6.5e15' )   : 'the pressure inside a W80 nuclear warhead detonation (64 billion bar)',
    mpmathify( '2.5e16' )   : 'the pressure inside the core of the Sun (250 billion bar)',
    mpmathify( '5.7e16' )   : 'the pressure inside a uranium nucleus (8 MeV in a sphere of radius 175 pm)',
    mpmathify( '1.0e34' )   : 'the Pressure range inside a neutron star (0.3 to 1.6 x 10^34)',
    mpmathify( '4.6e113' )  : 'the Planck pressure',
}


# //******************************************************************************
# //
# //  radiationDoseTable
# //
# //  sieverts : description
# //
# //  https://en.wikipedia.org/wiki/Sievert
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28radiation%29
# //
# //******************************************************************************

radiationDoseTable = {
    mpmathify( '1.0e-6' )   : 'the cosmic ray dose rate on commercial flights, which varies from 1 to 10 uSv/hour, depending on altitude, position and solar sunspot phase',
    mpmathify( '1.0e-5' )   : 'the daily exposure due to natural background radiation, including radon',
    mpmathify( '6.0e-5' )   : 'the radiation dose from a chest X-ray (AP+Lat)',
    mpmathify( '7.0e-5' )   : 'the radiation dose from a transatlantic airplane flight',
    mpmathify( '9.0e-5' )   : 'the radiation dose from a dental X-ray (panoramic)',
    mpmathify( '1.0e-4' )   : 'the average USA dose from consumer products in a year',
    mpmathify( '1.5e-4' )   : 'the USA EPA cleanup annual dose standard',
    mpmathify( '2.5e-4' )   : 'the USA NRC cleanup annual dose standard for individual sites/sources',
    mpmathify( '2.7e-4' )   : 'the yearly dose from natural cosmic radiation at sea level (0.5 in Denver due to altitude)',
    mpmathify( '2.8e-4' )   : 'the yearly dose from natural terrestrial radiation in the USA (0.16-0.63 mSv depending on soil composition)',
    mpmathify( '4.6e-4' )   : 'the estimated largest off-site dose possible from March 28, 1979 Three Mile Island accident',
    mpmathify( '4.8e-4' )   : 'the USA NRC public area daily exposure limit',
    mpmathify( '6.6e-4' )   : 'the average annual dose from human-made sources in the USA',
    mpmathify( '7.0e-4' )   : 'the radiation dose from a mammogram',
    mpmathify( '1.0e-3' )   : 'the limit of annual dose from man-made sources to someone who is not a radiation worker in the USA and Canada',
    mpmathify( '1.1e-3' )   : 'the average USA radiation worker annual occupational dose in 1980',
    mpmathify( '1.2e-3' )   : 'the radiation dose from an abdominal X-ray',
    mpmathify( '2.0e-3' )   : 'the USA average annual dose from medical and natural background radiation',
    mpmathify( '2.0e-3' )   : 'the human internal annual radiation dose due to radon, varies with radon levels',
    mpmathify( '2.0e-3' )   : 'the radiation dose from a head CT',
    mpmathify( '3.0e-3' )   : 'the USA average annual dose from all natural sources',
    mpmathify( '3.66e-3' )  : 'the USA average annual dose from all sources, including medical diagnostic radiation doses',
    mpmathify( '4.0e-3' )   : 'the Canada CNSC maximum occupational dose to a pregnant woman who is a designated Nuclear Energy Worker',
    mpmathify( '5.0e-3' )   : 'the USA NRC occupational annual dose limit for minors (10% of adult limit)',
    mpmathify( '5.0e-3' )   : 'the USA NRC occupational limit for pregnant women',
    mpmathify( '6.4e-3' )   : 'the annual dose received at the High Background Radiation Area (HBRA) of Yangjiang, China',
    mpmathify( '7.6e-3' )   : 'the annual dose received at Fountainhead Rock Place, Santa Fe, NM from natural sources',
    mpmathify( '8.0e-3' )   : 'the radiation dose from a chest CT',
    mpmathify( '1.0e-2' )   : 'the lower dose level for public calculated from the 1 to 5 rem range for which USA EPA guidelines mandate emergency action when resulting from a nuclear accident',
    mpmathify( '1.0e-2' )   : 'the radiation dose from an Abdominal CT',
    mpmathify( '5.0e-2' )   : 'the USA NRC/ Canada CNSC occupational annual dose limit for designated Nuclear Energy Workers',
    mpmathify( '1.0e-1' )   : 'the Canada CNSC occupational limit over a 5-year dosimetry period for designated Nuclear Energy Workers',
    mpmathify( '1.0e-1' )   : 'the USA EPA acute dose level estimated to increase cancer risk 0.8%',
    mpmathify( '1.75e-1' )  : 'the annual exposure from natural radiation in Guarapari, Brazil',
    mpmathify( '2.5e-1' )   : 'the whole body dose exclusion zone criteria for US nuclear reactor siting (2 hours)',
    mpmathify( '2.5e-1' )   : 'the USA EPA voluntary maximum dose for emergency non-life-saving work',
    mpmathify( '2.60e-1' )  : 'the annual exposure calculated from 260 mGy per year peak natural background dose in Ramsar',
    mpmathify( '5.0e-1' )   : 'the USA NRC occupational whole skin, limb skin, or single organ annual exposure limit',
    mpmathify( '5.0e-1' )   : 'the Canada CNSC occupational limit for designated Nuclear Energy Workers carrying out urgent and necessary work during an emergency',
    mpmathify( '7.5e-1' )   : 'the USA EPA voluntary maximum dose for emergency life-saving work',
    mpmathify( '1.0' )      : 'the hourly exposure level reported during Fukushima I nuclear accidents, in immediate vicinity of reactor',
    mpmathify( '3.0' )      : 'the thyroid dose (due to iodine absorption) exclusion zone criteria for US nuclear reactor siting (converted from 300 rem)',
    mpmathify( '4.8' )      : 'the LD50 exposure level (actually LD50/60) in humans from radiation poisoning with medical treatment, estimated from 480 to 540 rem',
    mpmathify( '5.0' )      : 'the exposure from the estimated 510 rem dose fatally received by Harry Daghlian on 1945 August 21 at Los Alamos and the lower estimate for fatality of Russian specialist on 1968 April 5 at Chelyabinsk-70',
    mpmathify( '5.0' )      : 'the level of exposure most commercial electronics can survive (5 - 10 Sv)',
    mpmathify( '21' )       : 'the exposure from the estimated 2100 rem dose fatally received by Louis Slotin on 1946 May 21 at Los Alamos and the lower estimate for fatality of Russian specialist on 1968 April 5 Chelyabinsk-70',
    mpmathify( '48.5' )     : 'the exposure from the estimated 4500 + 350 rad dose for fatality of Russian experimenter on 1997 June 17 at Sarov',
    mpmathify( '60.0' )     : 'the exposure from the estimated 6000 rem doses for several Russian fatalities from 1958 onwards, such as on 1971 May 26 at the Kurchatov Institute. The lower estimate for a Los Alamos fatality in 1958 December 30.',
    mpmathify( '100' )      : 'the exposure from the estimated 10000 rad dose for fatality at the United Nuclear Fuels Recovery Plant on 1964 July 24',
    mpmathify( '200' )      : 'the exposure of some Chernobyl emergency workers over 1100 hours (170 mSv)',
    mpmathify( '1000000' )  : 'the radiation level most radiation-hardened electronics can survive',
}


# //******************************************************************************
# //
# //  radiationExposureTable
# //
# //  coulombs/kilogram : description
# //
# //******************************************************************************

radiationExposureTable = {
    mpmathify( '6.8e-9' )   : 'the average hourly background radiation exposure on Earth',
    mpmathify( '1.47e-7' )  : 'the average radiation exposure from a dental X-ray',
    mpmathify( '4.12e-9' )  : 'the average radiation exposure from a gantrointestinal X-ray investigation',
    mpmathify( '0.03' )     : 'the radiation exposure sufficient to cause nausea, vomiting and weakness in humans',
    mpmathify( '0.06' )     : 'the radiation exposure sufficient to cause headache, fever, puroura, hemorrhage or infections in humans',
    mpmathify( '0.18' )     : 'the radiation exposure sufficient to cause diarrhea and leukopenia in humans',
    mpmathify( '0.235' )    : 'the radiation exposure sufficient to cause death in humans',
}


# //******************************************************************************
# //
# //  radioactivityTable
# //
# //  becquerels : description
# //
# //  https://en.wikipedia.org/wiki/List_of_radioactive_isotopes_by_half-life
# //
# //******************************************************************************

radioactivityTable = {
    mpmathify( '0.016' )        : 'average radioactivity of radium-226 in 1 gram of limestone',
    mpmathify( '0.048' )        : 'average radioactivity of radium-226 in 1 gram of igneous rock',
    mpmathify( '12437' )        : 'radioactivity of 1 gram of uranium-238',
    mpmathify( '8.0e5' )        : 'average natural radioactivity of 1 cubic meter of soil on the surface of Earth',
    mpmathify( '3.64981e10' )   : 'radioactivity of 1 gram of radium-226',
    mpmathify( '5.2e18' )       : 'estimated total radioactivity released by the Chernobyl accident',
    mpmathify( '3.65282e21' )   : 'radioactivity of 1 gram of nitrogen-16',
#     mpmathify( '1' )  : 'hydrogen-7 (half-life: 23e-24 s)',
#     mpmathify( '1' )  : 'hydrogen-5 (half-life: 80e-24 s)',
#     mpmathify( '1' )  : 'hydrogen-4 (half-life: 100e-24 s)',
#     mpmathify( '1' )  : 'nitrogen-10 (half-life: 200e-24 s)',
#     mpmathify( '1' )  : 'hydrogen-6 (half-life: 290e-24 s)',
#     mpmathify( '1' )  : 'lithium-5 (half-life: 324e-24 s)',
#     mpmathify( '1' )  : 'lithium-4 (half-life: 325e-24 s)',
#     mpmathify( '1' )  : 'boron-7 (half-life: 350e-24 s)',
#     mpmathify( '1' )  : 'helium-5 (half-life: 760e-24 s)',
#     mpmathify( '1' )  : 'helium-10 (half-life: 1.52e-21 s)',
#     mpmathify( '1' )  : 'lithium-10 (half-life: 2.0e-21 s)',
#     mpmathify( '1' )  : 'carbon-8 (half-life: 2.0e-21 s)',
#     mpmathify( '1' )  : 'helium-7 (half-life: 3.040e-21 s)',
#     mpmathify( '1' )  : 'beryllium-6 (half-life: 5.0e-21 s)',
#     mpmathify( '1' )  : 'helium-9 (half-life: 7.0e-21 s)',
#     mpmathify( '1' )  : 'boron-9 (half-life: 800e-21 s)',
#     mpmathify( '1' )  : 'beryllium-8 (half-life: 81.9e-18 s)',
#     mpmathify( '1' )  : 'boron-16 (half-life: 190e-12 s)',
#     mpmathify( '1' )  : 'beryllium-13 (half-life: 500e-12 s)',
#     mpmathify( '1' )  : 'lithium-12 (half-life: 10e-9 s)',
#     mpmathify( '1' )  : 'boron-18 (half-life: 26e-9 s)',
#     mpmathify( '1' )  : 'carbon-21 (half-life: 30e-9 s)',
#     mpmathify( '1' )  : 'beryllium-15 (half-life: 200e-9 s)',
#     mpmathify( '1' )  : 'beryllium-16 (half-life: 200e-9 s)',
#     mpmathify( '1' )  : 'Copernicium-277 (half-life: 240e-6 s)',
#     mpmathify( '1' )  : 'hassium-265 (half-life: 2.0e-3 s)',
#     mpmathify( '1' )  : 'boron-19 (half-life: 2.92e-3 s)',
#     mpmathify( '1' )  : 'meitnerium-266 (half-life: 3.4e-3 s)',
#     mpmathify( '1' )  : 'boron-17 (half-life: 5.08e-3 s)',
#     mpmathify( '1' )  : 'carbon-22 (half-life: 6.2e-3 s)',
#     mpmathify( '1' )  : 'lithium-11 (half-life: 8.59e-3 s)',
#     mpmathify( '1' )  : 'boron-15 (half-life: 9.87e-3 s)',
#     mpmathify( '1' )  : 'boron-14 (half-life: 12.5e-3 s)',
#     mpmathify( '1' )  : 'carbon-20 (half-life: 16e-3 s)',
#     mpmathify( '1' )  : 'boron-13 (half-life: 17.33e-3 s)',
#     mpmathify( '1' )  : 'boron-12 (half-life: 20.2e-3 s)',
#     mpmathify( '1' )  : 'beryllium-12 (half-life: 21.49e-3 s)',
#     mpmathify( '1' )  : 'carbon-19 (half-life: 46.2e-3 s)',
#     mpmathify( '1' )  : 'carbon-18 (half-life: 92e-3 s)',
#     mpmathify( '1' )  : 'bohrium-262 (half-life: 102e-3 s)',
#     mpmathify( '1' )  : 'helium-8 (half-life: 119e-3 s)',
#     mpmathify( '1' )  : 'carbon-9 (half-life: 126.5e-3 s)',
#     mpmathify( '1' )  : 'lithium-9 (half-life: 178.3e-3 s)',
#     mpmathify( '1' )  : 'carbon-17 (half-life: 193e-3 s)',
#     mpmathify( '1' )  : 'carbon-16 (half-life: 747e-3 s)',
#     mpmathify( '1' )  : 'boron-8 (half-life: 770e-3 s)',
#     mpmathify( '1' )  : 'helium-6 (half-life: 806.7 s)',
#     mpmathify( '1' )  : 'lithium-8 (half-life: 839.9e-3 s)',
#     mpmathify( '1' )  : 'carbon-15 (half-life: 2.449 s)',
#     mpmathify( '1' )  : 'flerovium-289 (half-life: 2.6 s)',
#     mpmathify( '1' )  : 'beryllium-14 (half-life: 4.84 s)',
#     mpmathify( '1' )  : 'beryllium-11 (half-life: 13.81 s)',
#     mpmathify( '1' )  : 'carbon-10 (half-life: 19.29 s)',
#     mpmathify( '1' )  : 'dubnium-261 (half-life: 27 s)',
#     mpmathify( '1' )  : 'seaborgium-266 (half-life: 30 s)',
#     mpmathify( '1' )  : 'dubnium-262 (half-life: 34 s)',
#     mpmathify( '1' )  : 'rutherfordium-261 (half-life: 81 s)',
#     mpmathify( '1' )  : 'nobelium-253 (half-life: 97 s)',
#     mpmathify( '1' )  : 'carbon-11 (half-life: 1.22e3 s)',
#     mpmathify( '1' )  : 'nobelium-259 (half-life: 3.5e3 s)',
#     mpmathify( '1' )  : 'fluorine-18 (half-life: 6.586e3 s)',
#     mpmathify( '1' )  : 'mendelevium-257 (half-life: 19.9e3 s)',
#     mpmathify( '1' )  : 'erbium-165 (half-life: 37.3e3 s)',
#     mpmathify( '1' )  : 'sodium-24 (half-life: 53.9e3 s)',
#     mpmathify( '1' )  : 'fermium-252 (half-life: 91.4e3 s)',
#     mpmathify( '1' )  : 'erbium-160 (half-life: 102.9e3 s)',
#     mpmathify( '1' )  : 'fermium-253 (half-life: 260e3 s)',
#     mpmathify( '1' )  : 'manganese-52 (half-life: 483.1e3 s)',
#     mpmathify( '1' )  : 'thulium-167 (half-life: 799e3 s)',
#     mpmathify( '1' )  : 'vanadium-48 (half-life: 1.38011e6 s)',
#     mpmathify( '1' )  : 'californium-253 (half-life: 1.539e6 s)',
#     mpmathify( '1' )  : 'chromium-51 (half-life: 2.39350e6 s)',
#     mpmathify( '1' )  : 'mendelevium-258 (half-life: 4.45e6 s)',
#     mpmathify( '1' )  : 'beryllium-7 (half-life: 4.590e6 s)',
#     mpmathify( '1' )  : 'californium-254 (half-life: 5.23e6 s)',
#     mpmathify( '1' )  : 'cobalt-56 (half-life: 6.676e6 s)',
#     mpmathify( '1' )  : 'scandium-46 (half-life: 7.239e6 s)',
#     mpmathify( '1' )  : 'sulfur-35 (half-life: 7.544e6 s)',
#     mpmathify( '1' )  : 'thulium-168 (half-life: 8.04e6 s)',
#     mpmathify( '1' )  : 'fermium-257 (half-life: 8.68e6 s)',
#     mpmathify( '1' )  : 'thulium-170 (half-life: 11.11e6 s)',
#     mpmathify( '1' )  : 'polonium-210 (half-life: 11.9e6 s)',
#     mpmathify( '1' )  : 'cobalt-57 (half-life: 23.483e6 s)',
#     mpmathify( '1' )  : 'vanadium-49 (half-life: 29e6 s)',
#     mpmathify( '1' )  : 'californium-248 (half-life: 28.81e6 s)',
#     mpmathify( '1' )  : 'ruthenium-106 (half-life: 32.3e6 s)',
#     mpmathify( '1' )  : 'neptunium-235 (half-life: 34.2e6 s)',
#     mpmathify( '1' )  : 'cadmium-109 (half-life: 40.0e6 s)',
#     mpmathify( '1' )  : 'thulium-171 (half-life: 61e6 s)',
#     mpmathify( '1' )  : 'caesium-134 (half-life: 65.17e6 s)',
#     mpmathify( '1' )  : 'sodium-22 (half-life: 82.1e6 s)',
#     mpmathify( '1' )  : 'rhodium-101 (half-life: 100e6 s)',
#     mpmathify( '1' )  : 'cobalt-60 (half-life: 166.35e6 s)',
#     mpmathify( '1' )  : 'hydrogen-3 (half-life: 389e6 s)',
#     mpmathify( '1' )  : 'californium-250 (half-life: 413e6 s)',
#     mpmathify( '1' )  : 'niobium meta state Nb-93m (half-life: 509e6 s)',
#     mpmathify( '1' )  : 'strontium-90 (half-life: 909e6 s)',
#     mpmathify( '1' )  : 'curium-243 (half-life: 920e6 s)',
#     mpmathify( '1' )  : 'caesium-137 (half-life: 952e6 s)',
#     mpmathify( '1' )  : 'titanium-44 (half-life: 2.0e9 s)',
#     mpmathify( '1' )  : 'uranium-232 (half-life: 2.17e9 s)',
#     mpmathify( '1' )  : 'plutonium-238 (half-life: 2.77e9 s)',
#     mpmathify( '1' )  : 'nickel-63 (half-life: 3.16e9 s)',
#     mpmathify( '1' )  : 'silicon-32 (half-life: 5.4e9 s)',
#     mpmathify( '1' )  : 'argon-39 (half-life: 8.5e9 s)',
#     mpmathify( '1' )  : 'californium-249 (half-life: 11.1e9 s)',
#     mpmathify( '1' )  : 'silver-108 (half-life: 13.2e9 s)',
#     mpmathify( '1' )  : 'americium-241 (half-life: 13.64e9 s)',
#     mpmathify( '1' )  : 'niobium-91 (half-life: 21e9 s)',
#     mpmathify( '1' )  : 'californium-251 (half-life: 28.3e9 s)',
#     mpmathify( '1' )  : 'holmium-166(m1) (half-life: 38e9 s)',
#     mpmathify( '1' )  : 'berkelium-247 (half-life: 44e9 s)',
#     mpmathify( '1' )  : 'radium-226 (half-life: 50e9 s)',
#     mpmathify( '1' )  : 'molybdenum-93 (half-life: 130e9 s)',
#     mpmathify( '1' )  : 'holmium-153 (half-life: 144e9 s)',
#     mpmathify( '1' )  : 'curium-246 (half-life: 149e9 s)',
#     mpmathify( '1' )  : 'carbon-14 (half-life: 181e9 s)',
#     mpmathify( '1' )  : 'plutonium-240 (half-life: 207.1e9 s)',
#     mpmathify( '1' )  : 'thorium-229 (half-life: 232e9 s)',
#     mpmathify( '1' )  : 'americium-243 (half-life: 233e9 s)',
#     mpmathify( '1' )  : 'curium-245 (half-life: 270e9 s)',
#     mpmathify( '1' )  : 'curium-250 (half-life: 280e9 s)',
#     mpmathify( '1' )  : 'tin-126 (half-life: 320e9 s)',
#     mpmathify( '1' )  : 'niobium-94 (half-life: 640e9 s)',
#     mpmathify( '1' )  : 'plutonium-239 (half-life: 761e9 s)',
#     mpmathify( '1' )  : 'protactinium-231 (half-life: 1.034e12 s)',
#     mpmathify( '1' )  : 'lead-202 (half-life: 1.66e12 s)',
#     mpmathify( '1' )  : 'lanthanum-137 (half-life: 1.9e12 s)',
#     mpmathify( '1' )  : 'thorium-230 (half-life: 2.379e12 s)',
#     mpmathify( '1' )  : 'nickel-59 (half-life: 2.4e12 s)',
#     mpmathify( '1' )  : 'calcium-41 (half-life: 3.3e12 s)',
#     mpmathify( '1' )  : 'neptunium-236 (half-life: 4.9e12 s)',
#     mpmathify( '1' )  : 'uranium-233 (half-life: 5.02e12 s)',
#     mpmathify( '1' )  : 'rhenium-186 (half-life: 6.3e12 s)',
#     mpmathify( '1' )  : 'technetium-99 (half-life: 6.66e12 s)',
#     mpmathify( '1' )  : 'krypton-81 (half-life: 7.2e12 s)',
#     mpmathify( '1' )  : 'uranium-234 (half-life: 7.75e12 s)',
#     mpmathify( '1' )  : 'chlorine-36 (half-life: 9.5e12 s)',
#     mpmathify( '1' )  : 'curium-248 (half-life: 11e12 s)',
#     mpmathify( '1' )  : 'bismuth-208 (half-life: 11.6e12 s)',
#     mpmathify( '1' )  : 'plutonium-242 (half-life: 11.77e12 s)',
#     mpmathify( '1' )  : 'aluminium-26 (half-life: 22.6e12 s)',
#     mpmathify( '1' )  : 'selenium-79 (half-life: 36e12 s)',
#     mpmathify( '1' )  : 'iron-60 (half-life: 47e12 s)',
#     mpmathify( '1' )  : 'beryllium-10 (half-life: 43e12 s)',
#     mpmathify( '1' )  : 'zirconium-93 (half-life:  s)',
#     mpmathify( '1' )  : 'gadolinium-150 (half-life:  s)',
#     mpmathify( '1' )  : 'neptunium-237 (half-life:  s)',
#     mpmathify( '1' )  : 'caesium-135 (half-life:  s)',
#     mpmathify( '1' )  : 'technetium-97 (half-life:  s)',
#     mpmathify( '1' )  : 'dysprosium-154 (half-life:  s)',
#     mpmathify( '1' )  : 'bismuth-210 (half-life:  s)',
#     mpmathify( '1' )  : 'manganese-53 (half-life:  s)',
#     mpmathify( '1' )  : 'technetium-98 (half-life:  s)',
#     mpmathify( '1' )  : 'palladium-107 (half-life:  s)',
#     mpmathify( '1' )  : 'hafnium-182 (half-life:  s)',
#     mpmathify( '1' )  : 'lead-205 (half-life:  s)',
#     mpmathify( '1' )  : 'curium-247 (half-life:  s)',
#     mpmathify( '1' )  : 'iodine-129 (half-life:  s)',
#     mpmathify( '1' )  : 'uranium-236 (half-life:  s)',
#     mpmathify( '1' )  : 'niobium-92 (half-life:  s)',
#     mpmathify( '1' )  : 'plutonium-244 (half-life:  s)',
#     mpmathify( '1' )  : 'samarium-146 (half-life:  s)',
#     mpmathify( '1' )  : 'uranium-235 (half-life:  s)',
#     mpmathify( '1' )  : 'potassium-40 (half-life:  s)',
#     mpmathify( '1' )  : 'uranium-238 (half-life:  s)',
#     mpmathify( '1' )  : 'thorium-232 (half-life:  s)',
#     mpmathify( '1' )  : 'lutetium-176 (half-life:  s)',
#     mpmathify( '1' )  : 'rhenium-187 (half-life:  s)',
#     mpmathify( '1' )  : 'rubidium-87 (half-life:  s)',
#     mpmathify( '1' )  : 'lanthanum-138 (half-life:  s)',
#     mpmathify( '1' )  : 'samarium-147 (half-life:  s)',
#     mpmathify( '1' )  : 'platinum-190 (half-life:  s)',
#     mpmathify( '1' )  : 'gadolinium-152 (half-life:  s)',
#     mpmathify( '1' )  : 'indium-115 (half-life:  s)',
#     mpmathify( '1' )  : 'tantalum-180 (half-life:  s)',
#     mpmathify( '1' )  : 'hafnium-174 (half-life:  s)',
#     mpmathify( '1' )  : 'osmium-186 (half-life:  s)',
#     mpmathify( '1' )  : 'neodymium-144 (half-life:  s)',
#     mpmathify( '1' )  : 'samarium-148 (half-life:  s)',
#     mpmathify( '1' )  : 'cadmium-113 (half-life:  s)',
#     mpmathify( '1' )  : 'vanadium-50 (half-life:  s)',
#     mpmathify( '1' )  : 'tungsten-180 (half-life:  s)',
#     mpmathify( '1' )  : 'europium-151 (half-life:  s)',
#     mpmathify( '1' )  : 'neodymium-150 (half-life:  s)',
#     mpmathify( '1' )  : 'molybdenum-100 (half-life:  s)',
#     mpmathify( '1' )  : 'bismuth-209 (half-life:  s)',
#     mpmathify( '1' )  : 'zirconium-96 (half-life:  s)',
#     mpmathify( '1' )  : 'cadmium-116 (half-life:  s)',
#     mpmathify( '1' )  : 'calcium-48  43 (half-life:  s)',
#     mpmathify( '1' )  : 'selenium-82 (half-life:  s)',
#     mpmathify( '1' )  : 'tellurium-130 (half-life:  s)',
#     mpmathify( '1' )  : 'barium-130 (half-life:  s)',
#     mpmathify( '1' )  : 'germanium-76 (half-life:  s)',
#     mpmathify( '1' )  : 'xenon-136 (half-life:  s)',
#     mpmathify( '1' )  : 'tellurium-128 (half-life:  s)',
}


# //******************************************************************************
# //
# //  radiosityTable
# //
# //  watts/meter^2 : description
# //
# //******************************************************************************

radiosityTable = {
    mpmathify( '1.0' )      : 'one watt per square meter',   # goobles... fill me in
}


# //******************************************************************************
# //
# //  solidAngleTable
# //
# //  steradians : description
# //
# //  https://en.wikipedia.org/wiki/Solid_angle
# //
# //******************************************************************************

solidAngleTable = {
    mpmathify( '6.67e-5' )  : 'the solid angle of the Moon as seen from Earth',
    mpmathify( '6.87e-5' )  : 'the solid angle of the Sun as seen from Earth',
    mpmathify( '0.62' )     : 'the solid angle of a spherical octant',
    mpmathify( '2.47' )     : 'the solid angle of a spherical quadrant',
    mpmathify( '6.28' )     : 'the solid angle of a hemisphere',
    mpmathify( '12.57' )     : 'the solid angle of a sphere, the largest possible solid angle by definition',
}


# //******************************************************************************
# //
# //  temperatureTable
# //
# //  kelvins : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28temperature%29
# //
# //******************************************************************************

temperatureTable = {
    mpmathify( '1.0e-10' )      : 'the lowest temperature ever produced in a laboratory',
    mpmathify( '5.0e-8' )       : 'the Fermi temperature of potassium-40',
    mpmathify( '1.0e-6' )       : 'the temperature produced by nuclear demagnetrization refrigeration',
    mpmathify( '1.7e-3' )       : 'the temperature record for helium-3/helium-4 dliution refrigeration',
    mpmathify( '9.5e-1' )       : 'the melting point of helium',
    mpmathify( '2.725' )        : 'the temperature of the cosmic microwave background',
    mpmathify( '14.01' )        : 'the melting point of hydrogen',
    mpmathify( '44' )           : 'the mean temperature on Pluto',
    mpmathify( '183.9' )        : 'the coldest air recorded on Earth (Vostok Station, Antarctica)',
    mpmathify( '210' )          : 'the mean temperature on Mars',
    mpmathify( '234.3' )        : 'the melting point of mercury',
    mpmathify( '273.15' )       : 'the melting point of water',
    mpmathify( '287' )          : 'the mean temperature of Earth',
    mpmathify( '330' )          : 'the average body temperature for a human',
    mpmathify( '319.3' )        : 'the hottest temperature recorded on Earth (Death Valley)',
    mpmathify( '373.15' )       : 'the boiling point of water',
    mpmathify( '450' )          : 'the mean temperature on Mercury',
    mpmathify( '600.65' )       : 'the melting point of lead',
    mpmathify( '740' )          : 'the mean temperature on Venus',
    mpmathify( '933.47' )       : 'the melting point of aluminum',
    mpmathify( '1170' )         : 'the temperature of a wood fire',
    mpmathify( '1811' )         : 'the melting point of iron',
    mpmathify( '2022' )         : 'the boiling point of lead',
    mpmathify( '3683' )         : 'the melting point of tungsten',
    mpmathify( '5780' )         : 'the surface temperature of the Sun',
    mpmathify( '1.6e5' )        : 'the surface temperature of the hottest white dwarfs',
    mpmathify( '1.56e7' )       : 'the core temperature of the Sun',
    mpmathify( '2.3e7' )        : 'the temperature at which beryllium-7 can fuse',
    mpmathify( '2.3e8' )        : 'the temperature at which carbon-12 can fuse',
    mpmathify( '7.5e8' )        : 'the temperature at which oxygen can fuse',
    mpmathify( '1.0e10' )       : 'the temperature of a supernova',
    mpmathify( '7.0e11' )       : 'the temperature of a quasar\'s accretion disk',
    mpmathify( '6.7e13' )       : 'the temperature of gamma-ray burst from a collapsar',
    mpmathify( '2.8e15' )       : 'the temperature of an electroweak star',
    mpmathify( '1.0e21' )       : 'the temperature of dark matter in active galactic nuclei',
    mpmathify( '1.0e30' )       : 'the Hagedorn temperature, the highest possible temperature according to string theory',
    mpmathify( '1.416785e32' )  : 'the Planck temperature, at which the wavelength of black body radiation' +
                                  'reaches the Planck length',
    mpmathify( '1.0e33' )       : 'the Landau pole, the maximum theoretical temperature according to QED',
}


# //******************************************************************************
# //
# //  tidalForceTable
# //
# //  1/second^2 : description
# //
# //******************************************************************************

tidalForceTable = {
}


# //******************************************************************************
# //
# //  timeTable
# //
# //  seconds : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28frequency%29
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28time%29
# //
# //******************************************************************************

timeTable = {
    mpmathify( '5.39106e-44' )  : 'the Planck time',
    mpmathify( '1.35135e-6' )   : 'the clock cycle of the Intel 4004 microprocessor (1971)',
    mpmathify( '60' )           : 'one minute (60 seconds)',
    mpmathify( '3600' )         : 'one hour (60 minutes)',
    mpmathify( '86400' )        : 'one day (24 hours)',
    mpmathify( '604800' )       : 'one week (7 days)',
    mpmathify( '2551442.8016' ) : 'the synodic lunar month',
    mpmathify( '3.15576e7' )    : 'one Julian year (365.25 days)',
    mpmathify( '3.15576e8' )    : 'one decade (10 years)',
    mpmathify( '3.15576e9' )    : 'one century (100 years)',
    mpmathify( '3.15576e10' )   : 'one millennium (1000 years)',
}


# //******************************************************************************
# //
# //  velocityTable
# //
# //  meters/second : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28speed%29
# //
# //******************************************************************************

velocityTable = {
    mpmathify( '2.2e-18' )  : 'the expansion rate between 2 points in free space 1 meter apart under Hubble\'s law',
    mpmathify( '3.0e-9' )   : 'the upper range of the typical relative speed of continental drift',
    mpmathify( '1.4e-5' )   : 'the growth rate of bamboo, the fastest-growing woody plant, over 24 hours',
    mpmathify( '0.00275' )  : 'the world record speed of the fastest snail',
    mpmathify( '0.080' )    : 'the top speed of a sloth',
    mpmathify( '30' )       : 'the typical speed of a car on the freeway',
    mpmathify( '130' )      : 'the wind speed of a powerful tornado',
    mpmathify( '250' )      : 'the typical cruising speed of a modern jet airliner',
    mpmathify( '343' )      : 'the speed of sound (in dry air at sea level at 20 degrees C)',
    mpmathify( '981' )      : 'the top speed of the SR-71 Blackbird',
    mpmathify( '3373' )     : 'the speed of the X-43 rocket/scramjet plane',
    mpmathify( '11107' )    : 'the speed of Apollo 10, the high speed record for a manned vehicle',
    mpmathify( '11200' )    : 'the escape velocity from Earth',
    mpmathify( '29800' )    : 'the speed of the Earth in orbit around the Sun',
    mpmathify( '2.0e5' )    : 'the orbital speed of the Solar System in the Milky Way galaxy',
    mpmathify( '5.52e5' )   : 'the speed of the Milky Way, relative to the cosmic microwave background',
    mpmathify( '1.4e7' )    : 'the typical speed of a fast neutron',
    mpmathify( '3.0e7' )    : 'the typical speed of an electron in a cathode ray tube',
}


# //******************************************************************************
# //
# //  volumeTable
# //
# //  liters : description
# //
# //  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28volume%29
# //
# //******************************************************************************

volumeTable = {
    mpmathify( '4.22419e-102' ) : 'the Planck volume',
    mpmathify( '9.4e-41' )      : 'the classical volume of an electron',
    mpmathify( '1.5e-38' )      : 'the volume of a proton',
    mpmathify( '6.54e-29' )     : 'the volume of a hydrogen atom',
    mpmathify( '9.0e-14' )      : 'the volume of a human red blood cell',
    mpmathify( '1.3e-10' )      : 'the volume of a very fine grain of sand',
    mpmathify( '6.2e-8' )       : 'the volume of a medium grain of sand',
    mpmathify( '4.0e-6' )       : 'the volume of a large grain of sand',
    mpmathify( '0.0049' )       : 'a teaspoon',
    mpmathify( '0.219' )        : 'the volume of a standard Major League baseball',
    mpmathify( '0.94625' )      : 'a U.S. quart',
    mpmathify( '3.785' )        : 'a U.S. gallon',
    mpmathify( '1000' )         : 'the volume of a cubic meter',
    mpmathify( '11000' )        : 'the approximate volume of an elephant',
    mpmathify( '38500' )        : 'the volume of a 20-foot shipping container',
    mpmathify( '2.5e6' )        : 'the volume of an Olympic-sized swimming pool',
    mpmathify( '3.0e14' )       : 'the estimated volume of crude oil on Earth',
    mpmathify( '4.17e15' )      : 'the volume of the Grand Canyon',
    mpmathify( '1.2232e16' )    : 'the volume of Lake Superior',
    mpmathify( '2.6e18' )       : 'the volume of Greenland ice cap',
    mpmathify( '1.4e21' )       : 'the volume of water in all of Earth\'s oceans',
    mpmathify( '1.08e24' )      : 'the volume of the Earth',
    mpmathify( '1.e27' )        : 'the volume of Jupiter',
    mpmathify( '1.e30' )        : 'the volume of the Sun',
    mpmathify( '2.75e38' )      : 'the volume of the star Betelgeuse',
    mpmathify( '3.3e64' )       : 'the volume of the Milky Way',
    mpmathify( '3.4e83' )       : 'the approxmimate volume of the observable universe',
}

