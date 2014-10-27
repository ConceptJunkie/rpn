#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnEstimates.py
#//
#//  RPN command-line calculator estimate table declarations
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

from mpmath import *


#//******************************************************************************
#//
#//  accelerationTable
#//
#//  meters/second^2 : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28acceleration%29
#//
#//******************************************************************************

accelerationTable = {
    mpf( '0.0058' )     : 'the acceleration of the Earth due to the Sun\'s gravity',
    mpf( '1.62' )       : 'the Moon\'s gravity at its equator',
    mpf( '4.3' )        : 'the acceleration going from 0-60 mph in 6.4 seconds (Saab 9-5 Hirsch)',
    mpf( '9.80665' )    : 'the Earth\'s gravity',
    mpf( '15.2' )       : 'the acceleration going from 0-100 kph in 2.4 seconds (Bugatti Veyron)',
    mpf( '29' )         : 'the maximum acceleration during launch and re-entry of the Space Shuttle',
    mpf( '70.6' )       : 'the maximum acceleration of Apollo 6 during re-entry',
    mpf( '79' )         : 'the acceleration of an F-16 aircraft pulling out of a dive',
    mpf( '147' )        : 'the acceleration of an explosive seat ejection from an aircraft',
    mpf( '2946' )       : 'the acceleration of a soccer ball being kicked',
    mpf( '29460' )      : 'the acceleration of a baseball struck by a bat',
    mpf( '3.8e6' )      : 'the surface gravity of white dwarf Sirius B',
    mpf( '1.9e9' )      : 'the mean acceleration of a proton in the Large Hadron Collider',
    mpf( '7.0e12' )     : 'the maximum surface gravity of a neutron star',
}


#//******************************************************************************
#//
#//  angleTable
#//
#//  radians : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28angular_velocity%29
#//
#//******************************************************************************

angleTable = {
    mpf( '8.405e-16' )  : 'the angle the Sun revolves around the galactic core in a second',
    mpf( '8.03e-10' )   : 'the angle Pluto revolves around the Sun in a second',
    mpf( '1.68e-8' )    : 'the angle Jupiter revolves around the Sun in a second',
    mpf( '1.99e-7' )    : 'the angle the Earth revolves around the Sun in a second',
    mpf( '7.27e-5' )    : 'the angle the Earth rotates in a second',
    mpf( '1.454e-4' )  : 'the angle a clock hour hand moves in a second',
    mpf( '1.7453e-3' )  : 'the angle a clock minute hand moves in a second',
    mpf( '0.10471976' ) : 'the angle a clock second hand moves in a second',
    mpf( '3.4906585' )  : 'the angle a long-playing record rotates in one second',
    mpf( '94' )         : 'the angle the spin cycle of washing machine rotates in one second',
    mpf( '753.982237' ) : 'the angle a 7200-rpm harddrive rotates in a second',
}


#//******************************************************************************
#//
#//  areaTable
#//
#//  meters^2 : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28area%29
#//
#//******************************************************************************

areaTable = {
    mpf( '2.6121e-70' ) : 'the Planck area',
    mpf( '1.0e-52' )    : 'one shed',
    mpf( '1.0e-48' )    : 'one square yoctometer',
    mpf( '1.0e-42' )    : 'one square zeptometer',
    mpf( '1.0e-36' )    : 'one square attometer',
    mpf( '1.0e-28' )    : 'one barn, roughly the cross-sectional area of a uranium nucleus',
    mpf( '1.0e-24' )    : 'one square picometer',
    mpf( '1.0e-18' )    : 'one square nanometer',
    mpf( '1.0e-12' )    : 'one square micron, the surface area of an E. coli bacterium',
    mpf( '1.0e-10' )    : 'the surface area of a human red blood cell',
    mpf( '7.1684e-9' )  : 'the area of a single pixel at 300 dpi resolution',
    mpf( '6.4516e-8' )  : 'the area of a single pixel at 100 dpi resolution',
    mpf( '1.9635e-7' )  : 'the cross-sectional area of a 0.5mm pencil lead',
    mpf( '2.9e-4' )     : 'the area of one side of a U.S. penny',
    mpf( '4.6e-3' )     : 'the area of the face of a credit card',
    mpf( '0.009677' )   : 'the area of a 3x5 inch index card',
    mpf( '0.06032246' ) : 'the area of American Letter size paper (8.5x11")',
    mpf( '0.181' )      : 'the surface area of a basketball (diameter 24 cm)',
    mpf( '1.73' )       : 'the average body surface area of a human',
    mpf( '261' )        : 'the area of a standard tennis court',
    mpf( '1250' )       : 'the area of an Olympic-size swimming pool',
    mpf( '4046.856' )   : 'one acre',
    mpf( '5400' )       : 'the size of an American football field',
    mpf( '22074' )      : 'the area of a Manhattan city block',
    mpf( '5.3e4' )      : 'the area of the base of the Great Pyramid of Giza',
    mpf( '4.4e5' )      : 'the area of Vatican City',
    mpf( '6.0e5' )      : 'the total floor area of the Pentagon',
    mpf( '2.0e6' )      : 'the area of Monaco (country ranked 192nd by area)',
    mpf( '2589988.11' ) : 'one square mile',
    mpf( '5.95e7' )     : 'the area of Manhattan Island',
    mpf( '1.29e9' )     : 'the area of Los Angeles, California, USA',
    mpf( '1.8e9' )      : 'the surface area of a typical neutron star',
    mpf( '2.188e9' )    : 'the area of Tokyo',
    mpf( '1.1e10' )     : 'the area of Jamaica',
    mpf( '6.887e10' )   : 'the area of Lake Victoria',
    mpf( '8.4e10' )     : 'the area of Austria',
    mpf( '1.0e11' )     : 'the area of South Korea',
    mpf( '3.0e11' )     : 'the area of Italy',
    mpf( '3.57e11' )    : 'the area of Germany',
    mpf( '3.779e11' )   : 'the area of Japan',
    mpf( '5.1e11' )     : 'the area of Spain',
    mpf( '7.8e11' )     : 'the area of Turkey',
    mpf( '1.0e12' )     : 'the area of Egypt (country ranked 29th by area)',
    mpf( '7.74e12' )    : 'the area of Australia (country ranked 6th by area)',
    mpf( '9.0e12' )     : 'the area of the largest extent of the Roman Empire',
    mpf( '1.0e13' )     : 'the area of Canada (including water)',
    mpf( '1.4e13' )     : 'the area of Antarctica',
    mpf( '1.7e13' )     : 'the area of Russia (country ranked 1st by area)',
    mpf( '3.0e13' )     : 'the area of Africa',
    mpf( '3.6e13' )     : 'the area of largest extent of the British Empire[citation needed]',
    mpf( '3.8e13' )     : 'the surface area of the Moon',
    mpf( '7.7e13' )     : 'the area of the Atlantic Ocean',
    mpf( '1.44e14' )    : 'the surface area of Mars',
    mpf( '1.5e14' )     : 'the land area of Earth',
    mpf( '1.56e14' )    : 'the area of the Pacific Ocean',
    mpf( '3.6e14' )     : 'the water area of Earth',
    mpf( '5.1e14' )     : 'the total surface area of Earth',
    mpf( '7.6e15' )     : 'the surface area of Neptune',
    mpf( '4.3e16' )     : 'the surface area of Saturn',
    mpf( '6.1e16' )     : 'the surface area of Jupiter',
    mpf( '4.6e17' )     : 'the area swept by the Moon\'s orbit of Earth',
    mpf( '6.1e18' )     : 'the surface area of the Sun',
    mpf( '1.1e22' )     : 'the area swept by Mercury\'s orbit around the Sun',
    mpf( '3.7e22' )     : 'the area swept by Venus\' orbit around the Sun',
    mpf( '7.1e22' )     : 'the area swept by Earth\'s orbit around the Sun',
    mpf( '1.6e23' )     : 'the area swept by Mars\' orbit around the Sun',
    mpf( '2.81e23' )    : 'the surface area of a Dyson sphere with a radius of 1 AU',
    mpf( '1.9e24' )     : 'the area swept by Jupiter\'s orbit around the Sun',
    mpf( '6.4e24' )     : 'the area swept by Saturn\'s orbit around the Sun',
    mpf( '8.5e24' )     : 'the surface area of the red supergiant star Betelgeuse',
    mpf( '2.4e25' )     : 'the surface area of the largest known star, the Hypergiant VY Canis Majoris',
    mpf( '2.6e25' )     : 'the area swept by Uranus\' orbit around the Sun',
    mpf( '6.4e25' )     : 'the area swept by Neptune\'s orbit around the Sun',
    mpf( '1.1e26' )     : 'the area swept by Pluto\'s orbit around the Sun',
    mpf( '2.0e32' )     : 'the approximate surface area of an Oort Cloud',
    mpf( '3.0e32' )     : 'the approximate surface area of a Bok globule',
    mpf( '7.0e41' )     : 'the approximate area of Milky Way\'s galactic disk',
}


#//******************************************************************************
#//
#//  capacitanceTable
#//
#//  farads : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28capacitance%29
#//
#//******************************************************************************

capacitanceTable = {
    mpf( '2.0e-15' )    : 'the gate capacitance of a MOS transistor, per micron of gate width',
    mpf( '3.0e-14' )    : 'the capacitance of a DRAM cell',
    mpf( '1.0e-13' )    : 'the capacitance of a small ceramic capacitor (100 fF)',
    mpf( '1.0e-12' )    : 'the capacitance of a small mica or PTFE capacitor (1 pF)',
    mpf( '4.0e-12' )    : 'the capacitive sensing of air-water-snow-ice (4 pF)',
    mpf( '5.0e-12' )    : 'the capacitance of a low condenser microphone (5 pF)',
    mpf( '4.5e-11' )    : 'a variable capacitor (45 pF)',
    mpf( '4.9e-11' )    : 'the capacitance of a yoga mat of TPE with relative permittivity of 4.5 and 8 mm thick sandwiched between two 1 dm^2 electrodes (49 pF)',
    mpf( '5.0e-11' )    : 'the capacitance of 1 m of Cat 5 network cable (between the two conductors of a twisted pair) (50 pF)',
    mpf( '1.0e-10' )    : 'the capacitance of the standard human body model (100 pF)',
    mpf( '1.0e-10' )    : 'the capacitance of 1 m of 50 ohm coaxial cable (between the inner and outer conductors) (100 pF)',
    mpf( '1.0e-10' )    : 'the capacitance of a high condenser microphone (100 pF)',
    mpf( '3.3e-10' )    : 'the capacitance of a variable capacitor (330 pF)',
    mpf( '1.0e-9' )     : 'the capacitance of a typical leyden jar (1 nF)',
    mpf( '1.0e-7' )     : 'the capacitance of a small aluminum electrolytic capacitor (100 nF)',
    mpf( '8.2e-7' )     : 'the capacitance of a large mica and PTFE capacitor (820 nF)',
    mpf( '1.0e-4' )     : 'the capacitance of a large ceramic capacitor (100 uF)',
    mpf( '6.8e-3' )     : 'the capacitance of a small electric double layer supercapacitor (6.8 mF)',
    mpf( '1.0' )        : 'the Earth-ionosphere capacitance (1 F)',
    mpf( '1.5' )        : 'the capacitance of a large aluminum electrolytic capacitor (1.5 F)',
    mpf( '5.0e3' )      : 'the capacitance of a large electric double-layer supercapacitor (5000 F)',
}


#//******************************************************************************
#//
#//  chargeTable
#//
#//  coulombs : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28charge%29
#//
#//******************************************************************************

chargeTable = {
    mpf( '-5.34e-20' )  : 'the charge of down, strange and bottom quarks (-1/3 e)',
    mpf( '1.068e-19' )  : 'the charge of up, charm and top quarks (2/3 e)',
    mpf( '1.602e-19' )  : 'the elementary charge e, i.e. the negative charge on a single electron or the positive charge on a single proton',
    mpf( '1.9e-18' )    : 'the Planck charge',
    mpf( '1.473e-17' )  : 'the positive charge on a uranium nucleus (92 e)',
    mpf( '1.0e-15' )    : 'the charge on a typical dust particle',
    mpf( '1.0e-12' )    : 'the charge in typical microwave frequency capacitors',
    mpf( '1.0e-9' )     : 'the charge in typical radio frequency capacitors',
    mpf( '1.0e-6' )     : 'the charge in typical audio frequency capacitors, and the static electricity from rubbing materials together',
    mpf( '1.0e-3' )     : 'the charge in typical power supply capacitors',
    mpf( '1.0' )        : 'a 1 coulomb charge: two negative point charges of 1 C, placed one meter apart, would experience a repulsive force of 9 GN',
    mpf( '26' )         : 'the charge in a typical thundercloud (15 - 350 C)',
    mpf( '5.0e3' )      : 'the typical alkaline AA battery is about 5000 C, or ~ 1.4 Ah',
    mpf( '9.64e4' )     : 'the charge on one mole of electrons (Faraday constant)',
    mpf( '2.16e5' )     : 'a car battery charge',
    mpf( '1.07e7' )     : 'the charge needed to produce 1 kg of aluminum from bauxite in an electrolytic cell',
    mpf( '5.9e8' )      : 'the charge in the worl\'s largest battery bank (36 MWh), assuming 220VAC output',
}


#//******************************************************************************
#//
#//  constantTable
#//
#//  unities : description
#//
#//******************************************************************************

constantTable = {
}


#//******************************************************************************
#//
#//  currentTable
#//
#//  amperes : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28current%29
#//
#//******************************************************************************

currentTable = {
    mpf( '1.0e-5' )     : 'the minimum current necessary to cause death (by ventricular fibrillation when applied directly across the human heart)',
    mpf( '7.0e-3' )     : 'the current draw of a portable hearing aid (typically 1 mW at 1.4 V)',
    mpf( '3.0e-3' )     : 'the current draw of a cathode ray tube electron gun beam (1-5 mA)',
    mpf( '1.0e-2' )     : 'the current which through the hand to foot may cause a person to freeze and be unable to let go (10 mA)',
    mpf( '2.0e-2' )     : 'the deadly limit of current for skin contact (at 120-230 V)',
    mpf( '1.5e-1' )     : 'the current draw of a 230 V AC, 22-inch/56-centimeter portable television (35 W)',
    mpf( '1.66e-1' )    : 'the current draw of a typical 12 V motor vehicle instrument panel light',
    mpf( '2.9e-1' )     : 'the current draw of a 120 V AC, 22-inch/56-centimeter portable television (35 W)',
    mpf( '1.35' )       : 'the current draw of a Tesla coil, 0.76 meters (2 ft 6 in) high, at 200 kV and 270 kV peak',
    mpf( '2.1' )        : 'the current draw of a high power LED current (peak 2.7 A)',
    mpf( '5.0' )        : 'the current draw of a typical 12 V motor vehicle headlight (typically 60 W)',
    mpf( '16.67' )      : 'the current draw of a 120 V AC, Toaster, kettle (2 kW)',
    mpf( '38.33' )      : 'the current draw of a 120 V AC, Immersion heater (4.6 kW)',
    mpf( '120' )        : 'the current draw of a typical 12 V motor vehicle starter motor (typically 1-2 kW)',
    mpf( '166' )        : 'the current draw of a 400 V low voltage secondary side distribution transformer with primary 12 kV ; 200 kVA (up to 1000 kVA also common)',
    mpf( '2.0e3' )      : 'the current draw of a 10.5 kV secondary side from an electrical substation with primary 115 kV ; 63 MVA',
    mpf( '2.5e4' )      : 'the current draw of a Lorentz force can crusher',
    mpf( '1.00e5' )     : 'the low range of Birkeland current which creates the Earth\'s aurorae',
    mpf( '1.40e5' )     : 'the "Sq" current of one daytime vortex within the ionospheric dynamo region',
    mpf( '1.0e6' )      : 'the high range of Birkeland current which creates Earth\'s aurorae',
    mpf( '5.0e6' )      : 'the current of the flux tube between Jupiter and Io',
    mpf( '2.7e7' )      : 'the firing current of the Z machine at the Sandia National Laboratories',
    mpf( '2.56e8' )     : 'the current produced in explosive flux compression generator (VNIIEF laboratories, Russia)',
    mpf( '3.0e9' )      : 'the total current in the Sun\'s heliospheric current sheet',
    mpf( '3.0e18' )     : 'the current of a 2 kpc segment of the 50 kpc-long radio jet of the Seyfert galaxy 3C 303',
    mpf( '3.479e25' )   : 'the Planck current',
}


#//******************************************************************************
#//
#//  dataRateTable
#//
#//  bits/second : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28bit_rate%29
#//
#//******************************************************************************

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
    mpf( '5.0e-2' )     : 'the bit rate for Project ELF which transmits 3-letter codes to U.S. nuclear submarines',
    mpf( '5.0e1' )      : 'the data rate for transmissions from GPS satellites',
    mpf( '5.6e1' )      : 'the data rate for a skilled operator in Morse code',
    mpf( '4.0e3' )      : 'the minimum data rate achieved for encoding recognizable speech (using special-purpose speech codecs)',
    mpf( '8.0e3' )      : 'the data rate of low-bitrate telephone quality',
    mpf( '3.2e4' )      : 'the data rate of MW quality and ADPCM voice in telephony',
    mpf( '5.6e4' )      : 'the data rate of 56kbit modem',
    mpf( '6.4e4' )      : 'the data rate of an ISDN B channel or best quality, uncompressed telephone line',
    mpf( '1.92e5' )     : 'the data rate for "nearly CD quality" for a file compressed in the MP3 format',
    mpf( '1.4112e6' )   : 'the data rate of CD audio (uncompressed, 16-bit samples x 44.1 kHz x 2 channels)',
    mpf( '1.536e6' )    : 'the data rate of 24 channels of telephone in the US, or a good VTC T1',
    mpf( '2.0e6' )      : 'the data rate of 30 channels of telephone audio or a Video Tele-Conference at VHS quality',
    mpf( '8.0e6' )      : 'the data rate of DVD quality video',
    mpf( '1.0e7' )      : 'the data rate of classic Ethernet: 10BASE2, 10BASE5, 10BASE-T',
    mpf( '1.0e7' )      : 'the data rate that the human retina transmits data to the brain, according to research',
    mpf( '2.7e7' )      : 'the data rate of HDTV quality video',
    mpf( '4.8e8' )      : 'the data rate of USB 2.0 High-Speed (interface signalling rate)',
    mpf( '7.86e8' )     : 'the data rate of FireWire IEEE 1394b-2002 S800',
    mpf( '9.5e8' )      : 'the data rate of a harddrive read, Samsung SpinPoint F1 HD103Uj',
    mpf( '1.0e9' )      : 'the data rate of Gigabit Ethernet',
    mpf( '1.067e9' )    : 'the data rate of Parallel ATA UDMA 6; conventional PCI 32 bit 33 MHz - 133 MB/s',
    mpf( '1.244e9' )    : 'the data rate of OC-24, a 1.244 Gbit/s SONET data channel',
    mpf( '1.5e9' )      : 'the data rate of SATA 1.5Gbit/s - First generation (interface signaling rate)',
    mpf( '3.0e9' )      : 'the data rate of SATA 3Gbit/s - Second generation (interface signaling rate)',
    mpf( '5.0e9' )      : 'the data rate of USB 3.0 SuperSpeed',
    mpf( '6.0e9' )      : 'the data rate of SATA 6Gbit/s - Third generation (interface signaling rate)',
    mpf( '8.533e9' )    : 'the data rate of PCI-X 64 bit 133 MHz - 1,067 MB/s',
    mpf( '9.953e9' )    : 'the data rate of OC-192, a 9.953 Gbit/s SONET data channel',
    mpf( '1.0e10' )     : 'the data rate of the Thunderbolt interface standard',
    mpf( '1.0e10' )     : 'the data rate of 10 Gigabit Ethernet',
    mpf( '1.0e10' )     : 'the data rate of USB 3.1 SuperSpeed 10 Gbit/s',
    mpf( '3.9813e10' )  : 'the data rate of OC-768, a 39.813 Gbit/s SONET data channel, the fastest in current use',
    mpf( '4.0e10' )     : 'the data rate of 40 Gigabit Ethernet',
    mpf( '8.0e10' )     : 'the data rate of PCI Express x16 v2.0',
    mpf( '9.6e10' )     : 'the data rate of InfiniBand 12X QDR',
    mpf( '1.0e11' )     : 'the data rate of 100 Gigabit Ethernet',
    mpf( '1.28e11' )    : 'the data rate for PCI Express x16 v3.0',
    mpf( '1.28e12' )    : 'the data rate of a SEA-ME-WE 4 submarine communications cable - 1.28 terabits per second',
    mpf( '3.84e12' )    : 'the data rate of a I-ME-WE submarine communications cable - design capacity of 3.84 terabits per second',
    mpf( '2.45e14' )    : 'the projected average global internet traffic in 2015 according to Cisco\'s 2011 VNI IP traffic forecast',
    mpf( '1.050e15' )   : 'the data rate over a 14-transmission-core optical fiber developed by NEC and Corning researchers',
}


#//******************************************************************************
#//
#//  densityTable
#//
#//  gram/liter : description
#//
#//  http://en.wikipedia.org/wiki/Density
#//  http://en.wikipedia.org/wiki/Orders_of_magnitude_%28density%29
#//
#//******************************************************************************

densityTable = {
    mpf( '1.0e-27' )    : 'the density (very approximate) of the universe',
    mpf( '1.0e-22' )    : 'the probable lowest observed density of space in galactic spiral arm (1 hydrogen atom every 16 cubic centimeters)',
    mpf( '1.0e-18' )    : 'the observed density of space in core of galaxy (600 hydrogen atoms in every cubic centimetre); best vacuum from a laboratory (1 pPa)',
    mpf( '2.0e-14' )    : 'the density of the Sun\'s corona',
    mpf( '1.0e-13' )    : 'the density at top of the Solar transition region',
    mpf( '1.0e-11' )    : 'the density at the bottom of the Solar transition region',
    mpf( '1.34e-5' )    : 'the density of Earth\'s atmosphere at 82 km altitude; star Mu Cephei\'s approximate mean density',
    mpf( '1.0e-4' )     : 'the density of Earth\'s atmosphere at 68 km altitude',
    mpf( '2.0e-4' )     : 'the density of the Solar photosphere-chromosphere boundary',
    mpf( '4.0e-4' )     : 'the density of the Solar photosphere\'s lower boundary',
    mpf( '1.0e-3' )     : 'the density achieved in a mechanical vacuum pump; the density of the Sun just below its photosphere',
    mpf( '1.8e-2' )     : 'the density of Earth\'s atmosphere at 30 km altitude',
    mpf( '9.0e-2' )     : 'the density of Hydrogen gas, the least dense substance at STP',
    mpf( '1.6e-1' )     : 'the density of Earth\'s atmosphere at 16 km altitude',
    mpf( '1.8e-1' )     : 'the density of aerographite',
    mpf( '9.0e-1' )     : 'the density of an ultralight metallic microlattice',
    mpf( '1.10e0' )     : 'the lowest density achieved for an aerogel',
    mpf( '1.48e0' )     : 'the density of Earth\'s atmosphere at sea level',
    mpf( '1.0e1' )      : 'the lowest density of a typical aerogel',
    mpf( '1.24e1' )     : 'the density of tungsten hexafluoride, one of the heaviest known gases at standard conditions',
    mpf( '6.5e1' )      : 'the surface density of Venus\' atmosphere',
    mpf( '7.0e1' )      : 'the density of liquid hydrogen at approximately -255 degrees C',
    mpf( '7.5e1' )      : 'the approximate density of styrofoam',
    mpf( '2.40e2' )     : 'the approximate density of cork',
    mpf( '5.0e2' )      : 'the highest density of a typical aerogel',
    mpf( '5.35e2' )     : 'the density of lithium (Li)',
    mpf( '7.00e2' )     : 'the typical density of wood',
    mpf( '8.60e2' )     : 'the density of potassium (K)',
    mpf( '9.167e2' )    : 'the density of water ice at temperatures < 0 degrees C',
    mpf( '9.70e2' )     : 'the density of sodium (Na)',
    mpf( '1.000e3' )    : 'the density of liquid water at 4 degrees C',
    mpf( '1.030e3' )    : 'the density of salt water',
    mpf( '1.062e3' )    : 'the average density of the human body',
    mpf( '1.261e3' )    : 'the density of glycerol',
    mpf( '1.408e3' )    : 'the average density of the Sun',
    mpf( '1.622e3' )    : 'the density of tetrachloroethene',
    mpf( '1.740e3' )    : 'the density of magnesium (Mg)',
    mpf( '1.850e3' )    : 'the density of beryllium (Be)',
    mpf( '2.000e3' )    : 'the density of concrete',
    mpf( '2.330e3' )    : 'the density of silicon',
    mpf( '2.700e3' )    : 'the density of aluminium',
    mpf( '3.325e3' )    : 'the density of diiodomethane (liquid at room temperature)',
    mpf( '3.500e3' )    : 'the density of diamond',
    mpf( '4.540e3' )    : 'the density of titanium',
    mpf( '4.800e3' )    : 'the density of selenium',
    mpf( '5.515e3' )    : 'the average density of the Earth',
    mpf( '6.100e3' )    : 'the density of vanadium',
    mpf( '6.690e3' )    : 'the density of antimony',
    mpf( '7.000e3' )    : 'the density of zinc',
    mpf( '7.200e3' )    : 'the density of chromium',
    mpf( '7.310e3' )    : 'the density of tin',
    mpf( '7.325e3' )    : 'the density of manganese',
    mpf( '7.870e3' )    : 'the density of iron',
    mpf( '8.570e3' )    : 'the density of niobium',
    mpf( '8.600e3' )    : 'the density of brass',
    mpf( '8.650e3' )    : 'the density of cadmium',
    mpf( '8.900e3' )    : 'the density of cobalt',
    mpf( '8.900e3' )    : 'the density of nickel',
    mpf( '8.940e3' )    : 'the density of copper (Cu)',
    mpf( '9.750e3' )    : 'the density of bismuth (Bi)',
    mpf( '1.0220e4' )   : 'the density of molybdenum (Mo)',
    mpf( '1.0500e4' )   : 'the density of silver (Ag)',
    mpf( '1.1340e4' )   : 'the density of lead (Pb)',
    mpf( '1.1700e4' )   : 'the density of thorium (Th)',
    mpf( '1.2410e4' )   : 'the density of rhodium (Rh)',
    mpf( '1.3546e4' )   : 'the density of mercury (Hg)',
    mpf( '1.6600e4' )   : 'the density of tantalum (Ta)',
    mpf( '1.8800e4' )   : 'the density of uranium (U)',
    mpf( '1.9300e4' )   : 'the density of tungsten (W)',
    mpf( '1.9320e4' )   : 'the density of gold (Au)',
    mpf( '1.9840e4' )   : 'the density of plutonium (Pu)',
    mpf( '2.1450e4' )   : 'the density of platinum (Pt)',
    mpf( '2.2420e4' )   : 'the density of iridium (Ir)',
    mpf( '2.2590e4' )   : 'the density of osmium (Os), the densest known substance at STP',
    mpf( '4.1000e4' )   : 'the estimated density of Hassium (Hs), assuming that an isotope featuring a long half-life exists',
    mpf( '1.5e5' )      : 'the density of the core of the Sun',
    mpf( '1.0e9' )      : 'the density of a white dwarf',
    mpf( '2.0e13' )     : 'the approximate density of the universe at end of the electroweak epoch',
    mpf( '2.0e17' )     : 'the density of atomic nuclei and neutron stars',
    mpf( '1.0e23' )     : 'the density of a hypothetical preon star',
    mpf( '5.1e96' )     : 'the Planck density',
}


#//******************************************************************************
#//
#//  dynamicViscosityTable
#//
#//  pascal-second : description
#//
#//  http://en.wikipedia.org/wiki/Viscosity
#//
#//******************************************************************************

dynamicViscosityTable = {
    mpf( '8.8e-6' )     : 'the dynamic viscosity of hydrogen',
    mpf( '1.3e-5' )     : 'the dynamic viscosity of steam (at 100 degrees C)',
    mpf( '1.827e-5' )   : 'the dynamic viscosity of air at 18 degrees C',
    mpf( '2.822e-4' )   : 'the dynamic viscosity of water at 100 degrees C',
    mpf( '3.2e-4' )     : 'the dynamic viscosity of acetone',
    mpf( '6.0e-4' )     : 'the dynamic viscosity of gasoline',
    mpf( '1.002e-3' )   : 'the dynamic viscosity of water at 20 degrees C',
    mpf( '1.6e-3' )     : 'the dynamic viscosity of mercury',
    mpf( '3.0e-3' )     : 'the dynamic viscosity of milk',
    mpf( '4.0e-3' )     : 'the dynamic viscosity of human blood',
    mpf( '8.1e-3' )     : 'the dynamic viscosity of olive oil',
    mpf( '1.0e-1' )     : 'the dynamic viscosity of castor oil',
    mpf( '1.5' )        : 'the dynamic viscosity of glycerine',
    mpf( '5.0' )        : 'the dynamic viscosity of Karo syrup',
    mpf( '10' )         : 'the dynamic viscosity of honey',
    mpf( '50' )         : 'the dynamic viscosity of ketchup',
    mpf( '70' )         : 'the dynamic viscosity of mustard',
    mpf( '100' )        : 'the dynamic viscosity of sour Cream',
    mpf( '250' )        : 'the dynamic viscosity of peanut butter',
    mpf( '1.0e3' )      : 'the dynamic viscosity of lard',
    mpf( '1.0e4' )      : 'the dynamic viscosity of plate glass (at 900 degrees C)',
    mpf( '2.3e8' )      : 'the approximate viscosity of pitch',
}


#//******************************************************************************
#//
#//  electricalConductanceTable
#//
#//  mhos : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28resistance%29
#//
#//******************************************************************************

electricalConductanceTable = {
    mpf( '5.0e-20' )        : 'the resistance of a 1 meter path though sulphur at standard temperature and pressure',
    mpf( '5.0e-15' )        : 'the resistenace of a 1 meter path through quartz, upper limit',
    mpf( '1.01010101e-11' ) : 'the highest resistor code on common circuits (white white white)',
    mpf( '1.0e-5' )         : 'the approximate resistance of the human body with dry skin',
    mpf( '1.0e-3' )         : 'the approximate resistance of the human body through wet or broken skin',
    mpf( '1.515e-3' )       : 'the resistance of a circular mil-foot of Nichrome',
    mpf( '3.33564095e-2' )  : 'the Planck impedance',
    mpf( '0.10204')         : 'the resistance of a circular mil-foot of silver',
    mpf( '5.0' )            : 'the resistance of a 1 meter path in 35g/kg salinity seawater at 20 degrees C',
    mpf( '6.139e6' )        : 'the resistance of a one cubic centimeter block of silver',
}


#//******************************************************************************
#//
#//  electricalPotentialTable
#//
#//  volts : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28voltage%29
#//
#//******************************************************************************

electricPotentialTable = {
    mpf( '5.0e-7' )     : 'the change in nerve cell potential caused by opening a single acetylcholine receptor channel (500 nV)',
    mpf( '2.0e-6' )     : 'the voltage of noise in an EEG taken at the scalp (2 uV)',
    mpf( '1.0e-5' )     : 'the minimum peak-to-peak amplitude of an average EEG taken at the scalp (10 uV)',
    mpf( '1.5e-5' )     : 'the minimum terrestrial digital-TV RF antenna signal (-85 dBm over 75 ohms)',
    mpf( '5.6e-5' )     : 'the minimum terrestrial analog-TV RF antenna signal (35 dB[uV])',
    mpf( '1.0e-4' )     : 'the maximum peak-to-peak amplitude of an average EEG taken at the scalp (100 uV)',
    mpf( '7.5e-2' )     : 'the nerve cell resting potential (75 mV)',
    mpf( '0.316' )      : 'the typical voltage reference level in consumer audio electronics (0.316 V rms)',
    mpf( '0.9' )        : 'the voltage of a lemon battery cell (made with copper and zinc electrodes)',
    mpf( '1.5' )        : 'the voltage of an alkaline AA, AAA, C or D battery',
    mpf( '5.0' )        : 'the voltage of USB power, used for example to charge a cell phone or a digital camera',
    mpf( '6.0' )        : 'the common voltage for medium-size electric lanterns (6 V)',
    mpf( '12' )         : 'the typical car battery (12 V)',
    mpf( '110' )        : 'the typical domestic wall socket voltage (110 V)',
    mpf( '600' )        : 'the voltage an electric eel sends in an average attack',
    mpf( '630' )        : 'the voltage in London Underground railway tracks',
    mpf( '2450' )       : 'the voltage used for electric chair execution in Nebraska',
    mpf( '1.0e4' )      : 'an electric fence (10kV)',
    mpf( '1.5e4' )      : 'the voltage of overhead railway AC electrification lines, 162/3 Hz (15 kV)',
    mpf( '2.5e4' )      : 'the voltage of European high-speed train overhead power lines (25 kV)',
    mpf( '3.45e4' )     : 'the voltage in North America for power distribution to end users (34.5 kV)',
    mpf( '2.3e5' )      : 'the highest voltage used in North American power high-voltage transmission substations (230 kV)',
    mpf( '3.45e5' )     : 'the lowest voltage used in EHV power transmission systems (345 kV)',
    mpf( '8.0e5' )      : 'the lowest voltage used by ultra-high voltage (UHV) power transmission systems (800 kV)',
    mpf( '3.0e6' )      : 'the voltage used by the ultra-high voltage electron microscope at Osaka University',
    mpf( '2.55e7' )     : 'the largest man-made voltage - produced in a Van de Graaff generator at Oak Ridge National Laboratory',
    mpf( '1.0e8' )      : 'the potential difference between the ends of a typical lightning bolt',
    mpf( '7.0e15' )     : 'the voltage around a particular energetic highly magnetized rotating neutron star',
    mpf( '1.04e27' )    : 'the Planck voltage',
}


#//******************************************************************************
#//
#//  electricalResistanceTable
#//
#//  ohms : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28resistance%29
#//
#//******************************************************************************

electricalResistanceTable = {
    mpf( '1.629e-7' )   : 'the resistance of a one cubic centimeter block of silver',
    mpf( '0.2' )        : 'the resistance of a 1 meter path in 35g/kg salinity seawater at 20 degrees C',
    mpf( '9.8')         : 'the resistance of a circular mil-foot of silver',
    mpf( '29.9792458' ) : 'the Planck impedance',
    mpf( '6.60e2' )     : 'the resistance of a circular mil-foot of Nichrome',
    mpf( '1.0e3' )      : 'the approximate resistance of the human body through wet or broken skin',
    mpf( '1.0e5' )      : 'the approximate resistance of the human body with dry skin',
    mpf( '9.9e10' )     : 'the highest resistor code on common circuits (white white white)',
    mpf( '2.0e14' )     : 'the resistenace of a 1 meter path through quartz, upper limit',
    mpf( '2.0e19' )     : 'the resistance of a 1 meter path though sulphur at standard temperature and pressure',
}


#//******************************************************************************
#//
#//  energyTable
#//
#//  joules : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28energy%29
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28specific_energy%29
#//  https://en.wikipedia.org/wiki/Energy_density
#//
#//******************************************************************************

energyTable = {
    mpf( '2.0e-33' )    : 'the average kinetic energy of translational motion of a molecule at the lowest temperature reached, 100 picokelvins, as of 2003',
    mpf( '6.6e-28' )    : 'the eergy of a typical AM radio photon (1 MHz) (4e-9 eV)',
    mpf( '1.6e-24' )    : 'the energy of a typical microwave oven photon (2.45 GHz) (1e-5 eV)',
    mpf( '2.0e-23' )    : 'the average kinetic energy of translational motion of a molecule in the Boomerang Nebula, the coldest place known outside of a laboratory, (1 K)',
    mpf( '2.0e-22' )    : 'the minumum energy of infrared light photons',
    mpf( '1.7e-21' )    : '1 kJ/mol, converted to energy per molecule',
    mpf( '2.1e-21' )    : 'the thermal energy in each degree of freedom of a molecule at 25 degrees C (kT/2) (0.01 eV)',
    mpf( '2.856e-21' )  : 'the minimum amount of energy required at 25 degrees C to change one bit of information, according to Landauer\'s principle',
    mpf( '3.0e-21' )    : 'the minimum energy of a van der Waals interaction between atoms (0.02 eV)',
    mpf( '4.1e-21' )    : '"kT" at 25 degrees C, a common rough approximation for the total thermal energy of each molecule in a system (0.03 eV)',
    mpf( '4.5e-20' )    : 'the upper bound of the mass-energy of a neutrino in particle physics (0.28 eV)',
    mpf( '6.0e-21' )    : 'the maximum energy of a van der Waals interaction between atoms (0.04 eV)',
    mpf( '1.6e-19' )    : '1 electronvolt (eV)',
    mpf( '3.0e-19' )    : 'the minimum energy of photons in visible light',
    mpf( '5.0e-19' )    : 'the minimum energy of ultraviolet light photons',
    mpf( '2.0e-17' )    : 'the minimum energy of X-ray photons',
    mpf( '2.0e-14' )    : 'the minimum energy of gamma ray photons',
    mpf( '2.7e-14' )    : 'the upper bound of the mass-energy of a muon neutrino',
    mpf( '8.2e-14' )    : 'the rest mass-energy of an electron',
    mpf( '1.6e-13' )    : '1 megaelectronvolt (MeV)',
    mpf( '2.3e-12' )    : 'the kinetic energy of neutrons produced by D-T fusion, used to trigger fission (14.1 MeV)',
    mpf( '3.4e-11' )    : 'the average total energy released in the nuclear fission of one uranium-235 atom (215 MeV)',
    mpf( '1.503e-10' )  : 'rest mass-energy of a proton',
    mpf( '1.505e-10' )  : 'the rest mass-energy of a neutron',
    mpf( '1.6e-10' )    : '1 gigaelectronvolt (GeV)',
    mpf( '3.0e-10' )    : 'the rest mass-energy of a deuteron',
    mpf( '6.0e-10' )    : 'the rest mass-energy of an alpha particle',
    mpf( '1.6e-9' )     : '10 GeV',
    mpf( '8.0e-9' )     : 'the initial operating energy per beam of the CERN Large Electron Positron Collider in 1989 (50 GeV)',
    mpf( '1.3e-8' )     : 'the mass-energy of a W boson (80.4 GeV)',
    mpf( '1.5e-8' )     : 'the mass-energy of a Z boson (91.2 GeV)',
    mpf( '1.6e-8' )     : '100 GeV',
    mpf( '2.0e-8' )     : 'the mass-energy of the particle believed to be the Higgs Boson (125.3 GeV)',
    mpf( '6.4e-8' )     : 'the operating energy per proton of the CERN Super Proton Synchrotron accelerator in 1976',
    mpf( '1.6e-7' )     : '1 TeV (teraelectronvolt), about the same kinetic energy as flying mosquito',
    mpf( '5.6e-7' )     : 'the energy per proton in the CERN Large Hadron Collider in 2011 (3.5 TeV)',
    mpf( '0.11' )       : 'the energy of an American half-dollar falling 1-meter',
    mpf( '1.0' )        : '1 newton-meter, 1 Watt-second, the kinetic energy produced by ~100 grams falling 1 meter, or required to heat 1 gm of cool air by 1 degree C',
    mpf( '1.4' )        : '1 ft-lbf (foot-pound force)',
    mpf( '4.184' )      : '~1 thermochemical calorie (small calorie)',
    mpf( '4.1868' )     : '~1 International (Steam) Table calorie',
    mpf( '8.0' )        : 'the Greisen-Zatsepin-Kuzmin theoretical upper limit for the energy of a cosmic ray coming from a distant source',
    mpf( '50' )         : 'the most energetic cosmic ray ever detected, in 1991',
    mpf( '100' )        : 'the flash energy of a typical pocket camera electronic flash capacitor (100-400 uF @ 330 V)',
    mpf( '300' )        : 'the energy of a lethal dose of X-rays',
    mpf( '300' )        : 'the kinetic energy of an average person jumping as high as he can',
    mpf( '330' )        : 'the energy required to melt 1 g of ice',
    mpf( '360' )        : 'the kinetic energy of 800 g standard men\'s javelin thrown at > 30 m/s by elite javelin throwers',
    mpf( '600' )        : 'the kinetic energy of 2 kg standard men\'s discus thrown at 24.4 m/s by the world record holder Juergen Schult',
    mpf( '600' )        : 'the energy use of a 10-watt flashlight for 1-minute',
    mpf( '750' )        : '1 horsepower applied for 1 second',
    mpf( '780' )        : 'the kinetic energy of 7.26 kg standard men\'s shot thrown at 14.7 m/s by the world record holder Randy Barnes',
    mpf( '1.1e3' )      : '1 British thermal unit (BTU), depending on the temperature',
    mpf( '1.4e3' )      : 'the total solar radiation received from the Sun by 1 square meter at the altitude of Earth\'s orbit per second (solar constant)',
    mpf( '1.8e3' )      : 'the kinetic energy of M16 rifle bullet (5.56x45mm NATO M855, 4.1 g fired at 930 m/s)',
    mpf( '2.3e3' )      : 'the energy needed to vaporize 1 g of water into steam',
    mpf( '3.0e3' )      : 'the energy of a Lorentz force can crusher pinch',
    mpf( '3.4e3' )      : 'the kinetic energy of world-record men\'s hammer throw (7.26 kg thrown at 30.7 m/s in 1986)',
    mpf( '3.6e3' )      : '1 Wh (watt-hour)',
    mpf( '4.2e3' )      : 'the energy released by explosion of 1 gram of TNT',
    mpf( '4.2e3' )      : '~1 food Calorie (large calorie)',
    mpf( '7.0e3' )      : 'the approxmate muzzle energy of an elephant gun, firing a .458 Winchester Magnum',
    mpf( '9.0e3' )      : 'the energy in an alkaline AA battery',
    mpf( '1.7e4' )      : 'the energy released by the metabolism of 1 gram of carbohydrates or protein',
    mpf( '3.8e4' )      : 'the energy released by the metabolism of 1 gram of fat',
    mpf( '4.5e4' )      : 'the approximate energy released by the combustion of 1 gram of gasoline',
    mpf( '5.0e4' )      : 'the kinetic energy of 1 gram of matter moving at 10 km/s',
    mpf( '3.0e5' )      : 'the kinetic energy of a one ton automobile at highway speeds (89 km/h or 55 mph)',
    mpf( '5.0e5' )      : 'the kinetic energy of a 1 gram meteor hitting Earth',
    mpf( '1.0e6' )      : 'the kinetic energy of a 2 tonne vehicle at 32 metres per second (72 miles per hour)',
    mpf( '1.2e6' )      : 'the approximate food energy of a snack such as a Snickers bar (280 food calories)',
    mpf( '3.6e6' )      : '1 kWh (kilowatt-hour)',
    mpf( '8.4e6' )      : 'the recommended food energy intake per day for a moderately active woman (2000 food calories)',
    mpf( '1.0e7' )      : 'the kinetic energy of the armor-piercing round fired by the assault guns of the ISU-152 tank',
    mpf( '1.1e7' )      : 'the recommended food energy intake per day for a moderately active man (2600 food calories)',
    mpf( '3.7e7' )      : '$1 of electricity at a cost of $0.10/kWh (the US average retail cost in 2009)',
    mpf( '4.0e7' )      : 'the energy from the combustion of 1 cubic meter of natural gas',
    mpf( '4.2e7' )      : 'the caloric energy consumed by Olympian Michael Phelps on a daily basis during Olympic training',
    mpf( '6.3e7' )      : 'the theoretical minimum energy required to accelerate 1 kg of matter to escape velocity from Earth\'s surface (ignoring atmosphere)',
    mpf( '1.0e8' )      : 'the kinetic energy of a 55 tonne aircraft at typical landing speed (59 m/s or 115 knots)',
    mpf( '1.1e8' )      : 'the energy in 1 therm, depending on the temperature',
    mpf( '1.1e8' )      : 'the energy of 1 Tour de France, or ~90 hours ridden at 5 W/kg by a 65 kg rider',
    mpf( '1.3e8' )      : 'the energy used by the fictional DeLorean in the "Back to the Future", traveling at 88 mph expending 1.21 GW of power as it passes a through planar singularity',
    mpf( '7.3e8' )      : 'the energy from burning 16 kilograms of oil (using 135 kg per barrel of light crude)',
    mpf( '5.0e9' )      : 'the energy in an average lightning bolt',
    mpf( '1.1e9' )      : 'the magnetic stored energy in the world\'s largest toroidal superconducting magnet for the ATLAS experiment at CERN, Geneva',
    mpf( '1.4e9' )      : 'the theoretical minimum amount of energy required to melt a tonne of steel (380 kWh)',
    mpf( '2.0e9' )      : 'the Planck energy',
    mpf( '3.3e9' )      : 'the approximate average amount of energy expended by a human heart muscle over an 80-year lifetime',
    mpf( '4.5e9' )      : 'average annual energy usage of a standard refrigerator',
    mpf( '6.1e9' )      : 'approximately 1 bboe (barrel of oil equivalent)',
    mpf( '2.3e10' )     : 'the kinetic energy of an Airbus A380 at cruising speed (560 tonnes at 562 knots or 289 m/s)',
    mpf( '4.2e10' )     : 'approximately 1 toe (ton of oil equivalent)',
    mpf( '5.0e10' )     : 'the yield energy of a Massive Ordnance Air Blast bomb, the second most powerful non-nuclear weapon ever designed',
    mpf( '7.3e10' )     : 'the energy consumed by the average U.S. automobile in the year 2000',
    mpf( '8.64e10' )    : '1 megawatt-day (MWd), a measurement used in the context of power plants',
    mpf( '8.8e10' )     : 'the total energy released in the nuclear fission of one gram of uranium-235',
    mpf( '3.4e12' )     : 'the maximum fuel energy of an Airbus A330-300 (97,530 liters of Jet A-1)',
    mpf( '3.6e12' )     : '1 gigawatt-hour (GWh)',
    mpf( '4.0e12' )     : 'the electricity generated by one 20-kg CANDU fuel bundle assuming ~29% thermal efficiency of reactor',
    mpf( '6.4e12' )     : 'the energy contained in jet fuel in a Boeing 747-100B aircraft at max fuel capacity (183,380 liters of Jet A-1)',
    mpf( '1.1e13' )     : 'the energy of the maximum fuel an Airbus A380 can carry (320,000 liters of Jet A-1)',
    mpf( '1.2e13' )     : 'the orbital kinetic energy of the International Space Station (417 tonnes at 7.7 km/s)',
    mpf( '8.8e13' )     : 'the energy yield of the Fat Man atomic bomb used in World War II (21 kilotons)',
    mpf( '9.0e13' )     : 'the theoretical total mass-energy of 1 gram of matter',
    mpf( '6.0e14' )     : 'the energy released by an average hurricane in 1 second',
    mpf( '1.0e15' )     : 'the approximate energy released by a severe thunderstorm',
    mpf( '1.0e15' )     : 'the yearly electricity consumption in Greenland as of 2008',
    mpf( '4.2e15' )     : 'the energy released by explosion of 1 megaton of TNT',
    mpf( '1.0e16' )     : 'the estimated impact energy released in forming Meteor Crater in Arizona',
    mpf( '1.1e16' )     : 'the yearly electricity consumption in Mongolia as of 2010',
    mpf( '9.0e16' )     : 'the mass-energy in 1 kilogram of antimatter (or matter)',
    mpf( '1.0e17' )     : 'the energy released on the Earth\'s surface by the magnitude 9.1-9.3 2004 Indian Ocean earthquake',
    mpf( '1.7e17' )     : 'the total energy from the Sun that strikes the face of the Earth each second',
    mpf( '2.1e17' )     : 'the yield of the Tsar Bomba, the largest nuclear weapon ever tested (50 megatons)',
    mpf( '4.2e17' )     : 'the yearly electricity consumption of Norway as of 2008',
    mpf( '8.0e17' )     : 'the estimated energy released by the eruption of the Indonesian volcano, Krakatoa, in 1883',
    mpf( '1.4e18' )     : 'the yearly electricity consumption of South Korea as of 2009',
    mpf( '1.4e19' )     : 'the yearly electricity production and consumption in the U.S. as of 2009',
    mpf( '5.0e19' )     : 'the energy released in 1-day by an average hurricane in producing rain (400 times greater than the wind energy)',
    mpf( '6.4e19' )     : 'the yearly electricity consumption of the world as of 2008',
    mpf( '6.8e19' )     : 'the yearly electricity generation of the world as of 2008',
    mpf( '5.0e20' )     : 'the total world annual energy consumption in 2010',
    mpf( '8.0e20' )     : 'the estimated global uranium resources for generating electricity 2005',
    mpf( '6.9e21' )     : 'the estimated energy contained in the world\'s natural gas reserves as of 2010',
    mpf( '7.9e21' )     : 'the estimated energy contained in the world\'s petroleum reserves as of 2010',
    mpf( '1.5e22' )     : 'the total energy from the Sun that strikes the face of the Earth each day',
    mpf( '2.4e22' )     : 'the estimated energy contained in the world\'s coal reserves as of 2010',
    mpf( '2.9e22' )     : 'the total identified global uranium-238 resources using fast reactor technology',
    mpf( '3.9e22' )     : 'the estimated energy contained in the world\'s fossil fuel reserves as of 2010',
    mpf( '4.0e22' )     : 'the estimated total energy released by the magnitude 9.1-9.3 2004 Indian Ocean Earthquake',
    mpf( '2.2e23' )     : 'the total global uranium-238 resources using fast reactor technology',
    mpf( '5.0e23' )     : 'the approximate energy released in the formation of the Chicxulub Crater in the Yucatan Peninsula',
    mpf( '5.5e24' )     : 'the total energy from the Sun that strikes the face of the Earth each year',
    mpf( '1.3e26' )     : 'a conservative estimate of the energy released by the impact that created the Caloris basin on Mercury',
    mpf( '3.8e26' )     : 'the total energy output of the Sun each second',
    mpf( '3.8e28' )     : 'the kinetic energy of the Moon in its orbit around the Earth (counting only its velocity relative to the Earth)',
    mpf( '2.1e29' )     : 'the rotational energy of the Earth',
    mpf( '1.8e30' )     : 'the gravitational binding energy of Mercury',
    mpf( '3.3e31' )     : 'the total energy output of the Sun each day',
    mpf( '2.0e32' )     : 'the gravitational binding energy of the Earth',
    mpf( '2.7e33' )     : 'the Earth\'s kinetic energy in its orbit',
    mpf( '1.2e34' )     : 'the total energy output of the Sun each year',
    mpf( '6.6e39' )     : 'the theoretical total mass-energy of the Moon',
    mpf( '5.4e41' )     : 'the theoretical total mass-energy of the Earth',
    mpf( '6.9e41' )     : 'the gravitational binding energy of the Sun',
    mpf( '5.0e43' )     : 'the total energy of all gamma rays in a typical gamma-ray burst',
    mpf( '1.5e44' )     : 'the estimated energy released in a supernova, sometimes referred to as a "foe"',
    mpf( '1.0e46' )     : 'the estimated energy released in a hypernova',
    mpf( '1.8e47' )     : 'the theoretical total mass-energy of the Sun',
    mpf( '8.8e47' )     : 'GRB 080916C - the most powerful Gamma-Ray Burst (GRB) ever recorded - total isotropic energy output estimated at 8.8 x 10^47 joules',
    mpf( '4.0e58' )     : 'the visible mass-energy in our galaxy, the Milky Way',
    mpf( '1.0e59' )     : 'the total mass-energy of our galaxy, the Milky Way, including dark matter and dark energy',
    mpf( '1.5e62' )     : 'the approximate total mass-energy of the Virgo Supercluster including dark matter, the Supercluster which contains the Milky Way',
    mpf( '4.0e69' )     : 'the estimated total mass-energy of the observable universe',
}


#//******************************************************************************
#//
#//  forceTable
#//
#//  newtons : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28force%29
#//
#//******************************************************************************

forceTable = {
    mpf( '3.6e-47' )    : 'the gravitational attraction of the proton and the electron in hydrogen atom',
    mpf( '8.9e-30' )    : 'the weight of an electron',
    mpf( '1.6e-26' )    : 'the weight of a hydrogen atom',
    mpf( '5.0e-24' )    : 'the force necessary to synchronize the motion of a single trapped ion with an external signal measured in a 2010 experiment',
    mpf( '1.7e-22' )    : 'the force measured in a 2010 experiment by perturbing 60 beryllium-9 ions',
    mpf( '1.0e-14' )    : 'the appoximate Brownian motion force on an E. coli bacterium averaged over 1 second',
    mpf( '1.0e-13' )    : 'the force needed to stretch double-stranded DNA to 50% relative extension',
    mpf( '4.0e-12' )    : 'the force needed to break a hydrogen bond',
    mpf( '5.0e-12' )    : 'the maximum force of a molecular motor',
    mpf( '1.6e-10' )    : 'the force needed to break a typical noncovalent bond',
    mpf( '1.6e-9' )     : 'the force needed to break a typical covalent bond',
    mpf( '8.2e-8' )     : 'the force on an electron in a hydrogen atom',
    mpf( '2.0e-7' )     : 'the force between two 1 meter long conductors, 1 meter apart by the definition of one ampere',
    mpf( '1.5e-4' )     : 'the maximum output of FEEP ion thrusters used in NASA\'s Laser Interferometer Space Antenna (150 uN)',
    mpf( '9.2e-2' )     : 'the maximum thrust of the NSTAR ion engine tested on NASA\'s space probe Deep Space 1 (92 mN)',
    mpf( '1.0' )        : 'the weight of an average apple',
    mpf( '9.8' )        : 'a one kilogram-force, nominal weight of a 1 kg object at sea level on Earth',
    mpf( '720' )        : 'the average force of human bite, measured at molars',
    mpf( '8.0e3' )      : 'the maximum force achieved by weight lifters during a "clean and jerk" lift',
    mpf( '9.0e3' )      : 'the bite force of one adult American alligator',
    mpf( '1.8e5' )      : 'the bite force of an adult great white shark',
    mpf( '4.5e5' )      : 'the force applied by the engine of a small car during peak acceleration[citation needed]',
    mpf( '1.0e5' )      : 'the average force applied by seatbelt and airbag to a restrained passenger in a car which hits a stationary barrier at 100 km/h',
    mpf( '8.9e5' )      : 'the maximum pulling force (tractive effort) of a single large diesel-electric locomotive',
    mpf( '1.8e6' )      : 'the thrust of Space Shuttle Main Engine at lift-off',
    mpf( '1.9e6' )      : 'the weight of the largest Blue Whale',
    mpf( '3.5e7' )      : 'the thrust of Saturn V rocket at lift-off',
    mpf( '5.7e8' )      : 'a simplistic estimate of force of sunlight on Earth',
    mpf( '2.0e20' )     : 'the gravitational attraction between Earth and Moon',
    mpf( '3.5e22' )     : 'the gravitational attraction between Earth and Sun',
    mpf( '1.2e44' )     : 'the Planck force',
}


#//******************************************************************************
#//
#//  frequencyTable
#//
#//  hertz : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28force%29
#//
#//******************************************************************************

# The second is the duration of 9 192 631 770 periods of the radiation corresponding to the transition between the
# two hyperfine levels of the ground state of the caesium 133 atom.

frequencyTable = {
    mpf( '2.296e-18' )          : 'the frequency of the Hubble Constant (once in 13.8 billion years)',
    mpf( '1.0e-15' )            : '1 femtohertz (fHz)',
    mpf( '1.0e-12' )            : '1 picohertz (pHz)',
    mpf( '3.1687535787e-11' )   : 'the frequency of once a millennium',
    mpf( '3.1687535787e-10' )   : 'the frequency of once a century',
    mpf( '3.1687535787e-9' )    : 'the frequency of once a decade',
    mpf( '3.1687535787e-8' )    : 'the Earth\'s orbital frequency (once a year)',
    mpf( '3.6603221e-5' )       : 'the Moon\'s orbital frequency (once a siderial month)',
    mpf( '1.653e-6' )           : 'the frequency of once a week',
    mpf( '1.15741e-5' )         : 'the Earth\'s rotation frequency (once a day)',
    mpf( '2.777778e-4' )        : 'the frequency of once an hour',
    mpf( '1.0e-3' )             : '1 millihertz (mHz)',
    mpf( '1.66666667e-2' )      : 'the frequency of one RPM',
    mpf( '1.4285714e-2' )       : 'the average frequency of an adult human\'s resting heart beat',
    mpf( '10' )                 : 'the cyclic rate of a typical automobile engine at idle (equivalent to 600 rpm)',
    mpf( '12' )                 : 'the frequency of lowest possible frequency that a human can hear',
    mpf( '27.5' )               : 'the frequency of the lowest musical note (A) playable on a normally-tuned standard piano',
    mpf( '50' )                 : 'the frequency of standard AC mains power (European AC, Tokyo AC)',
    mpf( '60' )                 : 'the frequency of standard AC mains power (American AC, Osaka AC)',
    mpf( '100' )                : 'the cyclic rate of a typical automobile engine at redline (equivalent to 6000 rpm)',
    mpf( '261.626' )            : 'the frequency of the musical note middle C',
    mpf( '440' )                : 'the frequency of the concert pitch (A above middle C), used for tuning musical instruments',
    mpf( '4.186e3' )            : 'the frequency of the highest musical note (C8) playable on a normally-tuned standard piano',
    mpf( '8.0e3' )              : 'the frequency of the ISDN sampling rate',
    mpf( '1.4e4' )              : 'the frequency of the typical upper limit of adult human hearing',
    mpf( '1.74e4' )             : 'a frequency known as \'The Mosquito\', which is generally only audible to those under the age of 24',
    mpf( '5.30e5' )             : 'the lower end of the AM radio broadcast spectrum',
    mpf( '7.40e5' )             : 'the clock speed of the world\'s first commercial microprocessor, the Intel 4004 (1971)',
    mpf( '1.710e6' )            : 'the higher end of the AM radio broadcast spectrum',
    mpf( '4.77e6' )             : 'the clock frequency of the 8086 processor in the IBM PC',
    mpf( '1.356e7' )            : 'the frequency of Near Field Communication',
    mpf( '8.8e7' )              : 'the lower end of the FM radio broadcast spectrum',
    mpf( '1.08e8' )             : 'the upper end of the FM radio broadcast spectrum',
    mpf( '1.42e9' )             : 'the frequency of the hyperfine transition of hydrogen, also known as the hydrogen line or 21 cm line',
    mpf( '2.4e9' )              : 'the frequency of microwave ovens, Wireless LANs and cordless phones (starting in 1998)',
    mpf( '3.8e9' )              : 'the fastest common desktop processor speed as of 2014',
    mpf( '4.7e9' )              : 'the AMD FX-9790 clock speed, fastest commercial processor in 2014',
    mpf( '5.8e9' )              : 'the cordless phone frequency introduced in 2003',
    mpf( '1.602e11' )           : 'the peak of cosmic microwave background radiation',
    mpf( '8.45e11' )            : 'the frequency of the fastest transistor (Dec. 2006)',
    mpf( '2.1e13' )             : 'the lower end of the frequency of infrared light used in thermal imaging',
    mpf( '3.3e13' )             : 'the upper end of the frequency of infrared light used in thermal imaging',
    mpf( '4.28e14' )            : 'the lower end of the visible light spectrum (red)',
    mpf( '7.50e14' )            : 'the upper end of the visible light spectrum (violet)',
    mpf( '2.47e15' )            : 'the frequency of the Lyman-alpha line',
    mpf( '3.0e16' )             : 'the frequency of X-Rays',
    mpf( '3.00e17' )            : 'the frequency of gamma rays',
    mpf( '1.0e18' )             : '1 exahertz (EHz)',
    mpf( '1.0e21' )             : '1 zettahertz (ZHz)',
    mpf( '1.0e21' )             : '1 yottahertz (YHz)',
    mpf( '3.9e27' )             : 'the frequency of the highest energy (16 TeV) gamma ray detected, from Markarian 501',
    mpf( '1.85e43' )            : 'the Planck frequency, the inverse of the Planck time',
}


#//******************************************************************************
#//
#//  illuminanceTable
#//
#//  lux : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28illuminance%29
#//
#//******************************************************************************

illuminanceTable = {
    mpf( '1.0e-4' )     : 'the illuminance of starlight on an overcast, moonless night sky',
    mpf( '1.4e-4' )     : 'the illuminance of Venus at its brightest',
    mpf( '2.0e-4' )     : 'the illuminance of starlight on a clear, moonless night sky, excluding airglow',
    mpf( '2.0e-3' )     : 'the illuminance of starlight on a clear, moonless night sky, including airglow',
    mpf( '1.0e-2' )     : 'the illuminance of the quarter Moon',
    mpf( '2.5e-2' )     : 'the illuminance of the full Moon on a clear night',
    mpf( '1.0' )        : 'the illuminance of the extreme of darkest storm clouds at sunset/sunrise',
    mpf( '40' )         : 'the illuminance of a fully overcast sky at sunset/sunrise',
    mpf( '200' )        : 'the illuminance of the extreme of darkest storm clouds at midday',
    mpf( '400' )        : 'the illuminance of sunrise or sunset on a clear day',
    mpf( '25000' )      : 'the illuminance of typical overcast day at midday',
    mpf( '120000' )     : 'the illuminance of the brightest sunlight',
}


#//******************************************************************************
#//
#//  inductanceTable
#//
#//  henries : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28inductance%29
#//
#//******************************************************************************

inductanceTable = {
    mpf( '1.0e-9' )     : 'the inductance of a thin film chip inductor, 1.6x0.8 mm with a typical power rating of 0.1 W (range: 1-100 nH)',
    mpf( '5.25e-7' )    : 'the inductance of one meter of Cat-5 cable pair',
    mpf( '5.0e-5' )     : 'the inductance of a coil with 99 turns, 0.635 cm long with a diameter of 0.635 cm',
    mpf( '1.0e-3' )     : 'the inductance of a coil 2.2 cm long with a diameter of 1.6 cm with 800 mA capability, used in kW amplifiers',
    mpf( '1.0' )        : 'the inductance of an inductor a few cm long and a few cm in diameter with many turns of wire on a ferrite core',
    mpf( '11' )         : 'the inductance of a mains electricity transformer primary at 120 V (range: 8-11 H)',
    mpf( '1.326e3' )    : 'the inductance of 500 kV, 3000 MW power line transformer primary winding',
}


#//******************************************************************************
#//
#//  informationEntropyTable
#//
#//  bits : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28data%29
#//
#//******************************************************************************

informationEntropyTable = {
    mpf( '1' )              : '1 bit - 0 or 1, false or true',
    mpf( '1.58496' )        : 'the approximate size of a trit (a base-3 digit, log2( 3 )',
    mpf( '2' )              : 'a crumb (rarely used term), enough to uniquely identify one base pair of DNA',
    mpf( '3' )              : 'the size of an octal digit',
    mpf( '4' )              : 'the size of a hexadecimal digit; decimal digits in binary-coded decimal form',
    mpf( '5' )              : 'the size of code points in the Baudot code, used in telex communication',
    mpf( '6' )              : 'the size of code points in Univac Fieldata, in IBM "BCD" format, and in Braille; enough to uniquely identify one codon of genetic code',
    mpf( '7' )              : 'the size of code points in the ASCII character set, minimum length to store 2 decimal digits',
    mpf( '8' )              : '1 byte (a.k.a. "octet") on many computer architectures, Equivalent to 1 "word" on 8-bit computers (Apple II, Atari 800, Commodore 64, et al.)',
    mpf( '10' )             : 'the minimum bit length to store a single byte with error-correcting memory, minimum frame length to transmit a single byte with asynchronous serial protocols',
    mpf( '12' )             : 'the word length of the PDP-8 of Digital Equipment Corporation (built from 1965-1990)',
    mpf( '16' )             : 'a commonly used in many programming languages, the size of an integer capable of holding 65,536 different values',
    mpf( '32' )             : 'size of addresses in IPv4, the current Internet protocol',
    mpf( '36' )             : 'the size of word on Univac 1100-series computers and Digital Equipment Corporation\'s PDP-10',
    mpf( '128' )            : 'size of addresses in IPv6, the successor protocol of IPv4',
    mpf( '256' )            : 'the minimum key length for the recommended strong cryptographic message digests as of 2004',
    mpf( '640' )            : 'the capacity of a punched card',
    mpf( '1288' )           : 'the approximate maximum capacity of a standard magnetic stripe card',
    mpf( '2048' )           : 'the RAM capacity of the stock Altair 8800',
    mpf( '4096' )           : 'the approximate amount of information on a sheet of single-spaced typewritten paper (without formatting)',
    mpf( '4704' )           : 'the uncompressed single-channel frame length in standard MPEG audio (75 frames per second and per channel), with medium quality 8-bit sampling at 44,100 Hz (or 16-bit sampling at 22,050 Hz)',
    mpf( '8192' )           : 'the RAM capacity of a Sinclair ZX81',
    mpf( '9408' )           : 'the uncompressed single-channel frame length in standard MPEG audio (75 frames per second and per channel), with standard 16-bit sampling at 44,100 Hz',
    mpf( '15360' )          : 'one screen of data displayed on an 8-bit monochrome text console (80x24)',
    mpf( '16384' )          : 'one page of typed text, the RAM capacity of Nintendo Entertainment System',
    mpf( '131072' )         : 'the RAM capacity of the smallest Sinclair ZX Spectrum.',
    mpf( '524288' )         : 'the RAM capacity of a lot of popular 8-bit Computers like the C-64, Amstrad CPC, etc.',
    mpf( '1048576' )        : 'the RAM capacity of popular 8-bit Computers like the C-128, Amstrad CPC etc. Or a 1024 x 768 pixel jpeg image',
    mpf( '1978560' )        : 'a one-page, standard-resolution black-and-white fax (1728 x 1145 pixels)',
    mpf( '4147200' )        : 'one frame of uncompressed NTSC DVD video (720 x 480 x 12 bpp Y\'CbCr)',
    mpf( '4976640' )        : 'one frame of uncompressed PAL DVD video (720 x 576 x 12 bpp Y\'CbCr)',
    mpf( '5.0e6' )          : 'a typical English book volume in plain text format of 500 pages x 2000 characters per page and 5-bits per character',
    mpf( '5242880' )        : 'the maximum addressable memory of the original IBM PC architecture',
    mpf( '8343400' )        : 'one "typical" sized photograph with reasonably good quality (1024 x 768 pixels)',
    mpf( '1.152e7' )        : 'the capacity of a lower-resolution computer monitor (as of 2006), 800 x 600 pixels, 24 bpp',
    mpf( '11796480' )       : 'the capacity of a 3.5 in floppy disk, colloquially known as 1.44 megabyte but actually 1.44 x 1000 x 1024 bytes',
    mpf( '2.5e7' )          : 'the amount of data in a typical color slide',
    mpf( '3.0e7' )          : 'the storage capacity of the first commercial harddisk IBM 350 in 1956',
    mpf( '33554432' )       : 'the RAM capacity of stock Nintendo 64 and average size of a music track in MP3 format',
    mpf( '4.194304e7' )     : 'the approximate size of the Complete Works of Shakespeare',
    mpf( '7.5e7' )          : 'the amount of information in a typical phone book',
    mpf( '9.8304e7' )       : 'capacity of a high-resolution computer monitor as of 2011, 2560 x 1600 pixels, 24 bpp',
    mpf( '1.50e7' )         : 'the amount of data in a large foldout map',
    mpf( '4.2336e8356' )    : 'a five-minute audio recording, in CDDA quality',
    mpf( '5.4525952e9' )    : 'the storage capacity of a regular compact disc (CD)',
    mpf( '5.888802816e9' )  : 'the capacity of a large regular compact disc',
    mpf( '6.4e9' )          : 'the capacity of the human genome (assuming 2 bits for each base pair)',
    mpf( '6710886400' )     : 'the average size of a movie in Divx format in 2002',
    mpf( '8589934592' )     : 'the maximum disk capacity using the 21-bit LBA SCSI standard introduced in 1979',
    mpf( '17179869184' )    : 'the storage limit of IDE standard for harddisks in 1986 and the volume limit for FAT16 released in 1984',
    mpf( '34359738368' )    : 'the maximum addressable memory for the Motorola 68020 (1984) and Intel 80386 (1985)',
    mpf( '3.76e10' )        : 'the capacity of a single-layer, single-sided DVD',
    mpf( '79215880888' )    : 'the size of Wikipedia article text compressed with bzip2 on 2013-06-05',
    mpf( '1.46e11' )        : 'the capacity of a double-sided, dual-layered DVD',
    mpf( '2.15e11' )        : 'the capacity of a single-sided, single-layered 12-cm Blu-ray disc',
    mpf( '1.34e12' )        : 'the estimated capacity of the Polychaos dubium genome, the largest known genome',
    mpf( '8.97e12' )        : 'the data of pi to the largest number of decimal digits ever calculated as of 2010',
    mpf( '1.0e13' )         : 'the capacity of a human being\'s functional memory, according to Raymond Kurzweil',
    mpf( '16435678019584' ) : 'the size of all multimedia files used in English wikipedia on May 2012',
    mpf( '17592186044416' ) : 'the capacity of a hard disk that would be considered average as of 2012 and the maximum disk capacity using the 32-bit LBA SCSI introduced in 1987',
    mpf( '1.40737e14' )     : 'the NTFS volume capacity in Windows 7, Windows Server 2008 R2 or earlier implementation',
    mpf( '3.6028e16' )      : 'the theoretical maximum of addressable physical memory in the AMD64 architecture',
    mpf( '4.5e16' )         : 'the estimated hard drive space in Google\'s server farm as of 2004',
    mpf( '1.0e16' )         : 'the estimated approximate size of the Library of Congress\'s collection, including non-book materials, as of 2005',
    mpf( '2.0e17' )         : 'the storage space of Megaupload file-hosting service at the time it was shut down in 2012',
    mpf( '8.0e17' )         : 'the storage capacity of the fictional Star Trek character Data',
    mpf( '1.15292e18' )     : 'the storage limit using the ATA-6 standard introduced in 2002',
    mpf( '1.6e18' )         : 'the total amount of printed material in the world',
    mpf( '1.47573e20' )     : 'the maximum addressable memory using 64-bit addresses',
    mpf( '3.5e20' )         : 'the increase in information capacity when 1 Joule of energy is added to a heat-bath at 300 K (27 degrees C)',
    mpf( '3.4e21' )         : 'the amount of information that can be stored in 1 gram of DNA',
    mpf( '4.7e21' )         : 'the amount of digitally stored information in the world as of May 2009',
    mpf( '7.55579e22' )     : 'the Maximum volume and file size in the Unix File System (UFS) and maximum disk capacity using the 64-bit LBA SCSI standard introduced in 2000 using 512-byte blocks',
    mpf( '1.0e23' )         : 'the increase in information capacity when 1 Joule of energy is added to a heat-bath at 1 K (-272.15 degrees C)',
    mpf( '6.0e23' )         : 'the information content of 1 mole (12.01 g) of graphite at 25 degrees C; equivalent to an average of 0.996 bits per atom',
    mpf( '7.3e24' )         : 'the information content of 1 mole (18.02 g) of liquid water at 25 degrees C; equivalent to an average of 12.14 bits per molecule',
    mpf( '1.1e25' )         : 'entropy increase of 1 mole (18.02 g) of water, on vaporizing at 100 degrees C at standard pressure; equivalent to an average of 18.90 bits per molecule',
    mpf( '1.5e25' )         : 'the information content of 1 mole (20.18 g) of neon gas at 25 degrees C and 1 atm; equivalent to an average of 25.39 bits per atom',
    mpf( '2.0e45' )         : 'the number of bits required to perfectly recreate the natural matter of the average-sized U.S. adult male human being to the quantum level (Bekenstein bound)',
    mpf( '1.0e58' )         : 'the approximate thermodynamic entropy of the sun (about 30 bits per proton, plus 10 bits per electron)',
    mpf( '1.0e69' )         : 'the approximate thermodynamic entropy of the Milky Way Galaxy (counting only the stars, not the black holes within the galaxy)',
    mpf( '1.5e77' )         : 'the approximate information content of a one-solar-mass black hole',
    mpf( '1.0e92' )         : 'the information capacity of the observable universe, according to Seth Lloyd',
    mpf( '1.0e105' )        : 'the estimated theoretical maximum entropy of the universe',
}


#//******************************************************************************
#//
#//  lengthTable
#//
#//  meters : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28length%29
#//  https://en.wikipedia.org/wiki/List_of_examples_of_lengths
#//
#//******************************************************************************

lengthTable = {
    mpf( '1.616199e-35' )   : 'the Planck length; typical scale of hypothetical loop quantum gravity or size of a hypothetical string and of branes; according to string theory lengths smaller than this do not make any physical sense',
    mpf( '2.0e-23' )        : 'the effective cross section radius of 1 MeV neutrinos[3]',
    mpf( '1.0e-21' )        : 'the upper bound for the width of a cosmic string in string theory',
    mpf( '7.0e-21' )        : 'the effective cross section radius of high energy neutrinos',
    mpf( '3.1e-19' )        : 'the de Broglie wavelength of protons at the Large Hadron Collider (4 TeV as of 2012)',
    mpf( '1.0e-18' )        : 'the upper limit for the size of quarks and electrons, upper bound of the typical size range for "fundamental strings"',
    mpf( '1.0e-17' )        : 'the range of the weak force',
    mpf( '8.5e-16' )        : 'the approximate radius of a proton',
    mpf( '1.5e-15' )        : 'the size of an 11 MeV proton',
    mpf( '2.81794e-15' )    : 'the classical electron radius',
    mpf( '1.0e-12' )        : 'the longest wavelength of gamma rays',
    mpf( '2.4e-12' )        : 'the Compton wavelength of electron',
    mpf( '5.0e-12' )        : 'the wavelength of shortest X-rays',
    mpf( '2.5e-11' )        : 'the radius of a hydrogen atom',
    mpf( '3.1e-11' )        : 'the radius of a helium atom',
    mpf( '5.3e-11' )        : 'the Bohr radius',
    mpf( '1.0e-10' )        : 'an Angstrom (also the covalent radius of a sulfur atom)',
    mpf( '1.54e-10' )       : 'the length of a typical covalent bond (C-C)',
    mpf( '3.4e-10' )        : 'the thickness of single layer graphene',
    mpf( '7.0e-10' )        : 'the width of glucose molecule',
    mpf( '9.0e-10' )        : 'the width of sucrose molecule',
    mpf( '1.0e-9' )         : 'the diameter of a carbon nanotube',
    mpf( '2.5e-9' )         : 'the smallest microprocessor transistor gate oxide thickness (as of Jan 2007)',
    mpf( '8.0e-9' )         : 'the average thickness of a cell membrane',
    mpf( '1.0e-8' )         : 'the thickness of cell wall in gram-negative bacteria',
    mpf( '4.0e-8' )         : 'the wavelength of extreme ultraviolet',
    mpf( '9.0e-8' )         : 'the size of the Human immunodeficiency virus (HIV) (generally, viruses range in size from 20 nm to 450 nm)',
    mpf( '1.25e-7' )        : 'the standard depth of pits on compact discs (width: 500 nm, length: 850 nm to 3.5 um)',
    mpf( '4.075e-7' )       : 'the center wavelength of violet light',
    mpf( '6.825e-5' )       : 'the center wavelength of red light',
    mpf( '2.0e-6' )         : 'the particle size that a surgical mask removes at 80-95% efficiency',
    mpf( '3.5e-6' )         : 'the size of a typical yeast cell',
    mpf( '7.0e-6' )         : 'the average diameter of a red blood cell',
    mpf( '1.0e-5' )         : 'the typical size of a fog, mist or cloud water droplet',
    mpf( '1.2e-5' )         : 'the width of acrylic fiber',
    mpf( '2.54e-5' )        : '1/1000 inch, commonly referred to as one thou or one mil',
    mpf( '5.0e-5' )         : 'the length of a typical Euglena gracilis, a flagellate protist',
    mpf( '9.0e-5' )         : 'the average thickness of paper',
    mpf( '1.0e-4' )         : 'the average width of a strand of human hair',
    mpf( '2.0e-4' )         : 'the typical length of Paramecium caudatum, a ciliate protist',
    mpf( '5.0e-4' )         : 'the length of a typical Amoeba proteus',
    mpf( '7.60e-4' )        : 'the thickness of a typical credit card',
    mpf( '0.00254' )        : 'the distance between pins in DIP (dual-inline-package) electronic components',
    mpf( '0.005' )          : 'the length of average red ant',
    mpf( '0.00762' )        : '7.62 mm, a common military ammunition size',
    mpf( '0.0254' )         : 'an inch',
    mpf( '0.04267' )        : 'the diameter of a golf ball',
    mpf( '0.054' )          : 'the width of a typical credit card',
    mpf( '0.086' )          : 'the length of a typical credit card',
    mpf( '0.12' )           : 'the diameter of a Compact Disc (120 mm)',
    mpf( '0.22' )           : 'the diameter of a typical soccer ball',
    mpf( '0.3048' )         : 'a foot',
    mpf( '0.9144' )         : 'a yard',
    mpf( '1.7' )            : 'the average height of a human',
    mpf( '8.38' )           : 'the length of a London Bus (Routemaster)',
    mpf( '33' )             : 'the length of longest blue whale measured, the largest animal',
    mpf( '91.44' )          : 'the length of a football field',
    mpf( '93.47' )          : 'the height of the Statue of Liberty (foundation of pedestal to torch)',
    mpf( '137' )            : 'the height of the Great Pyramid of Giza',
    mpf( '979' )            : 'the height of the Salto Angel, the world\'s highest free-falling waterfall (Venezuela)',
    mpf( '1.609e3' )        : 'an international mile',
    mpf( '1.852e3' )        : 'a nautical mile',
    mpf( '8.848e3' )        : 'the height of the highest mountain on earth, Mount Everest',
    mpf( '1.0911e4' )       : 'the depth of deepest part of the ocean, Mariana Trench',
    mpf( '1.3e4' )          : 'the narrowest width of the Strait of Gibraltar, separating Europe and Africa',
    mpf( '42194.988' )      : 'the length of a marathon',
    mpf( '9.0e4' )          : 'the width of the Bering Strait',
    mpf( '1.11e5' )         : 'the distance covered by one degree of latitude on Earth\'s surface',
    mpf( '1.63e5' )         : 'the length of the Suez Canal',
    mpf( '9.746e5' )        : 'the greatest diameter of the dwarf planet Ceres',
    mpf( '2.390e6' )        : 'the diameter of dwarf planet Pluto',
    mpf( '3.480e6' )        : 'the diameter of the Moon',
    mpf( '5.200e6' )        : 'the typical distance covered by the winner of the 24 Hours of Le Mans automobile endurance race',
    mpf( '6.400e6' )        : 'the length of the Great Wall of China',
    mpf( '6.600e6' )        : 'the approximate length of the two longest rivers, the Nile and the Amazon',
    mpf( '7.821e6' )        : 'the length of the Trans-Canada Highway',
    mpf( '9.288e6' )        : 'the length of the Trans-Siberian Railway, longest in the world',
    mpf( '1.2756e7' )       : 'the equatorial diameter of the Earth',
    mpf( '4.0075e7' )       : 'the length of the Earth\'s equator',
    mpf( '1.42984e8' )      : 'the diameter of Jupiter',
    mpf( '299792458' )      : 'a light-second, the distance travelled by light in one second',
    mpf( '3.84e8' )         : 'the Moon\'s orbital distance from Earth',
    mpf( '1.39e9' )         : 'the diameter of the Sun',
    mpf( '1.79875e10' )     : 'the approximately one light-minute',
    mpf( '1.4959787e11' )   : 'an astronomical unit (AU), the mean distance between Earth and Sun',
    mpf( '9.0e11' )         : 'the optical diameter of Betelgeuse (~600x Sun)',
    mpf( '1.4e12' )         : 'the orbital distance of Saturn from Sun',
    mpf( '1.96e12' )        : 'the estimated optical diameter of VY Canis Majoris (1420x Sun)',
    mpf( '2.3e12' )         : 'the estimated optical diameter of NML Cygni (1650x Sun)',
    mpf( '2.37e12' )        : 'the median point of the optical diameter of UY Scuti, as of 2014 the largest known star',
    mpf( '5.9e12' )         : 'the orbital distance of Pluto from Sun',
    mpf( '7.5e12' )         : 'the estimated outer boundary of the Kuiper belt, inner boundary of the Oort cloud (~50 AU)',
    mpf( '1.0e13' )         : 'the diameter of our Solar System as a whole',
    mpf( '1.625e13' )       : 'the distance of the Voyager 1 spacecraft from Sun (as of Feb 2009), the farthest man-made object so far',
    mpf( '6.203e13' )       : 'the estimated radius of the event horizon of the supermassive black hole in NGC 4889, the largest known black hole to date',
    mpf( '1.8e14' )         : 'the size of the debris disk around the star 51 Pegasi',
    mpf( '7.5e15' )         : 'the supposed outer boundary of the Oort cloud (~50,000 AU)',
    mpf( '9.46e15' )        : 'a light year, the distance travelled by light in one year; at its current speed, Voyager 1 would need 17,500 years to travel this distance',
    mpf( '3.0857e16' )      : 'a parsec',
    mpf( '3.99e16' )        : 'the distance to nearest star (Proxima Centauri)',
    mpf( '4.13e16' )        : 'the distance to nearest discovered extrasolar planet (Alpha Centauri Bb) as of March 2013',
    mpf( '1.93e17' )        : 'the distance to nearest discovered extrasolar planet with potential to support life as we know it (Gliese 581 d) as of October 2010',
    mpf( '6.15e17' )        : 'the approximate radius of humanity\'s radio bubble, caused by high-power TV broadcasts leaking through the atmosphere into outer space',
    mpf( '1.9e18' )         : 'the distance to nearby solar twin (HIP 56948), a star with properties virtually identical to our Sun',
    mpf( '9.46e18' )        : 'the average thickness of Milky Way Galaxy',
    mpf( '3.086e22' )       : 'a kiloparsec',
    mpf( '1.135e20' )       : 'the thickness of Milky Way Galaxy\'s gaseous disk',
    mpf( '9.5e20' )         : 'the diameter of galactic disk of Milky Way Galaxy',
    mpf( '1.54e21' )        : 'the distance to SN 1987A, the most recent naked eye supernova',
    mpf( '1.62e21' )        : 'the distance to the Large Magellanic Cloud (a dwarf galaxy orbiting the Milky Way)',
    mpf( '1.66e21' )        : 'the distance to the Small Magellanic Cloud (another dwarf galaxy orbiting the Milky Way)',
    mpf( '6.15e21' )        : 'the diameter of the low surface brightness disc halo of the giant spiral galaxy Malin 1',
    mpf( '1.324e22' )       : 'the radius of the diffuse stellar halo of IC 1101, one of the largest known galaxies',
    mpf( '2.376e22' )       : 'the distance to the Andromeda Galaxy',
    mpf( '3.086e22' )       : 'a megaparsec',
    mpf( '5.0e22' )         : 'the diameter of Local Group of galaxies',
    mpf( '4.50e23' )        : 'the approximate distance to Virgo cluster of galaxies',
    mpf( '1.9e24' )         : 'the diameter of the Local Supercluster and the largest voids and filaments',
    mpf( '5.0e24' )         : 'the diameter of the enormous Horologium Supercluster',
    mpf( '9.46e24' )        : 'the diameter of the Pisces-Cetus Supercluster Complex, the supercluster complex where we live',
    mpf( '1.3e25' )         : 'the length of the Sloan Great Wall, a giant wall of galaxies (galactic filament)',
    mpf( '3.086e25' )       : 'a gigaparsec',
    mpf( '3.784e25' )       : 'the length of the Huge-LQG, a group of 73 quasars',
    mpf( '9.5e25' )         : 'the estimated light travel distance to certain quasars, length of the Hercules-Corona Borealis Great Wall, a colossal wall of galaxies, the largest and the most massive structure in the observable universe as of 2014',
    mpf( '1.27e26' )        : 'the estimated light travel distance to UDFj-39546284, the most distant object ever observed',
    mpf( '8.7e26' )         : 'the approximate diameter (comoving distance) of the visible universe',
    mpf( '2.4e27' )         : 'the lower bound of the (possibly infinite) radius of the universe, if it is a 3-sphere, according to one estimate using the WMAP data at 95% confidence',
    mpf( '3.086e28' )       : 'a teraparsec',
    mpf( '7.4e28' )         : 'the lower bound of the homogeneous universe derived from the Planck spacecraft',
}


#//******************************************************************************
#//
#//  luminanceTable
#//
#//  candelas/meter^2 : description
#//
#//  https://en.wikipedia.org/wiki/Luminance
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28luminance%29
#//
#//******************************************************************************

luminanceTable = {
    mpf( '1.0e-6' ) : 'the luminance of the absolute threshold of human vision',
    mpf( '4.0e-4' ) : 'the luminance of the darkest sky',
    mpf( '1.0e-3' ) : 'the luminance of a typical night sky',
    mpf( '1.4e-3' ) : 'the luminance of a typical photographic scene lit by full moon',
    mpf( '5.0e-3' ) : 'the approximate luminance of the scotopic/mesopic threshold',
    mpf( '4.0e-2' ) : 'the luminance of the phosphorescent markings on a watch dial after 1 h in the dark',
    mpf( '2.0' )    : 'the luminance of floodlit buildings, monuments, and fountains',
    mpf( '5.0' )    : 'the approximate luminance of the mesopic/photopic threshold',
    mpf( '25' )     : 'the luminance of a typical photographic scene at sunrise or sunset',
    mpf( '30' )     : 'the luminance of a green electroluminescent source',
    mpf( '55' )     : 'the standard SMPTE cinema screen luminance',
    mpf( '80' )     : 'the luminance of monitor white in the sRGB reference viewing environment',
    mpf( '250' )    : 'the peak luminance of a typical LCD monitor',
    mpf( '700' )    : 'the luminance of a typical photographic scene on overcast day',
    mpf( '2000' )   : 'the luminance of an average cloudy sky',
    mpf( '2500' )   : 'the luminance of the Moon\'s surface',
    mpf( '5000' )   : 'the luminance of a typical photographic scene in full sunlight',
    mpf( '7000' )   : 'the luminance of an average clear sky',
    mpf( '1.0e4' )  : 'the luminance of a white illuminated cloud',
    mpf( '1.2e4' )  : 'the luminance of a fluorescent lamp',
    mpf( '7.5e4' )  : 'the luminance of a low pressure sodium-vapor lamp',
    mpf( '1.3e5' )  : 'the luminance of a frosted incandescent light bulb',
    mpf( '6.0e5' )  : 'the luminance of the solar disk at the horizon',
    mpf( '7.0e6' )  : 'the luminance of the filament of a clear incandescent lamp',
    mpf( '1.0e8' )  : 'the luminance of brightness which can cause retinal damage',
    mpf( '1.6e9' )  : 'the luminance of the solar disk at noon',
}


#//******************************************************************************
#//
#//  luminousFluxTable
#//
#//  lumens : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28luminous_flux%29
#//
#//******************************************************************************

luminousFluxTable = {
    mpf( '0.025' )      : 'the luminous flux of the light of a firefly',
    mpf( '12.57' )      : 'the luminous flux of the light of a candle',
    mpf( '780' )        : 'the luminous flux of a 60 W incandescent light bulb',
    mpf( '930' )        : 'the luminous flux of a 75 W incandescent light bulb',
    mpf( '2990' )       : 'the luminous flux of a 200 W incandescent light bulb',
    mpf( '6.0e5' )      : 'the luminous flux of an IMAX projector bulb',
    mpf( '4.23e10' )    : 'the luminous flux of the Luxor Sky Beam spotlight array in Las Vegas',
    mpf( '4.6e24' )     : 'the luminous flux of the dimmest class of red dwarf star',
    mpf( '3.0768e28' )  : 'the luminous flux of the Sun',
    mpf( '1.382e38' )   : 'the luminous flux of a Type 1a supernova',
    mpf( '1.26e41' )    : 'the luminous flux of Quasar 3C 273',
}


#//******************************************************************************
#//
#//  luminousIntensityTable
#//
#//  candelas : description
#//
#//  https://en.wikipedia.org/wiki/Candela#Examples
#//
#//******************************************************************************

luminousIntensityTable = {
    mpf( '5.0e-2' ) : 'the luminous intensity of a typical indicator LED',
    mpf( '1.0' )    : 'the approximate luminous intensity of a candle',
    mpf( '15' )     : 'the intensity of an "ultra-bright" LED',
    mpf( '75' )     : 'the luminous intensity of a typical fire alarm strobe',
}


#//******************************************************************************
#//
#//  magneticFieldStrengthTable
#//
#//  amperes/meter : description
#//
#//******************************************************************************

magneticFieldStrengthTable = {
}


#//******************************************************************************
#//
#//  magneticFluxTable
#//
#//  webers : description
#//
#//******************************************************************************

magneticFluxTable = {
}


#//******************************************************************************
#//
#//  magneticFluxDensityTable
#//
#//  teslas : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28magnetic_field%29
#//
#//******************************************************************************

magneticFluxDensityTable = {
    mpf( '5e-18' )      : 'the magnetic flux density precision attained for Gravity Probe B',
    mpf( '3.1869e-5' )  : 'the magnetic flux density of the Earth\'s magnetic field at 0 degrees long., 0 degrees lat.',
    mpf( '5.0e-3' )     : 'the magnetic flux density of a typical refrigerator magnet',
    mpf( '0.3' )        : 'the magnetic flux density of solar sunspots',
    mpf( '3.0' )        : 'the magnetic flux density of a common magnetic resonance imaging system',
    mpf( '8.0' )        : 'the magnetic flux density of the Large Hadron Collider magnets',
    mpf( '16' )         : 'the magnetic flux density strong enough to levitate a frog',
    mpf( '2800' )       : 'the magnetic flux density of the largest magnetic field produced in a laboratory',
    mpf( '1.0e8' )      : 'the lower range of magnetic flux density in a magnetar',
    mpf( '1.0e11' )     : 'the upper range of magnetic flux density in a magnetar',
}


#//******************************************************************************
#//
#//  massTable
#//
#//  grams : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28mass%29
#//
#//******************************************************************************

massTable = {
    mpf( '4.2e-37' )    : 'the mass equivalent of the energy of a photon at the peak of the spectrum of the cosmic microwave background radiation (0.235 meV/c2)',
    mpf( '1.8e-33' )    : 'the mass equivalent of one electronvolt (1 eV/c^2)',
    mpf( '3.6e-33' )    : 'the mass of an electron neutrino, (upper limit, 2 eV/c2)',
    mpf( '9.11e-28' )   : 'the mass of an electron (511 keV/c2), the lightest elementary particle with a measured nonzero rest mass',
    mpf( '5.5e-27' )    : 'the mass of an up quark (as a current quark, upper limit of 1.7-3.1 MeV/c2)',
    mpf( '1.9e-25' )    : 'the mass of a muon (106 MeV/c2)',
    mpf( '1.661e-24' )  : 'the atomic mass unit (u) or dalton (Da)',
    mpf( '1.673e-24' )  : 'the mass of proton (938.3 MeV/c2)',
    mpf( '1.674e-24' )  : 'the mass of a hydrogen atom, the lightest atom',
    mpf( '1.675e-24' )  : 'the mass of a neutron (939.6 MeV/c2)',
    mpf( '1.2e-23' )    : 'the mass of a lithium atom (6.941 u)',
    mpf( '3.0e-23' )    : 'the mass of a water molecule (18.015 u)',
    mpf( '8.0e-23' )    : 'the mass of a titanium atom (47.867 u)',
    mpf( '1.1e-22' )    : 'the mass of a copper atom (63.546 u)',
    mpf( '1.6e-22' )    : 'the mass of a Z boson (91.2 GeV/c2)',
    mpf( '3.1e-22' )    : 'the mass of a top quark (173 GeV/c2), the heaviest known elementary particle',
    mpf( '3.2e-22' )    : 'the mass of a caffeine molecule (194 u)',
    mpf( '3.5e-22' )    : 'the mass of a lead-208 atom, the heaviest stable isotope known',
    mpf( '1.2e-21' )    : 'the mass of a buckyball molecule (720 u)',
    mpf( '1.4e-20' )    : 'the mass of ubiquitin, a small protein (8.6 kDa)[13]',
    mpf( '5.5e-20' )    : 'the mass of a typical protein (median size of roughly 300 amino acids ~= 33 kDa)',
    mpf( '1.1e-19' )    : 'the mass of a hemoglobin A molecule in blood (64.5 kDa)',
    mpf( '1.65e-18' )   : 'the mass of a double-stranded DNA molecule consisting of 1,578 base pairs (995,000 daltons)',
    mpf( '4.3e-18' )    : 'the mass of a prokaryotic ribosome (2.6 MDa)',
    mpf( '7.1e-18' )    : 'the mass of a eukaryotic ribosome (4.3 MDa)',
    mpf( '7.6e-18' )    : 'the mass of a Brome mosaic virus, a small virus (4.6 MDa)',
    mpf( '3.0e-17' )    : 'the mass of the Synaptic vesicle in rats (16.1 +/- 3.8 MDa)',
    mpf( '6.8e-17' )    : 'the mass of the Tobacco mosaic virus (41 MDa)',
    mpf( '1.1e-16' )    : 'the mass of the nuclear pore complex in yeast (66 MDa)',
    mpf( '2.5e-16' )    : 'the mass of a Human adenovirus (150 MDa)',
    mpf( '1.0e-15' )    : 'the mass of an HIV-1 virus',
    mpf( '4.7e-15' )    : 'the mass of a DNA sequence of length 4.6 Mbp, the length of the E. coli genome',
    mpf( '1.0e-14' )    : 'the mass of a Vaccinia virus, a large virus',
    mpf( '1.1e-14' )    : 'the mass equivalent of 1 joule',
    mpf( '3.0e-13' )    : 'the mass of a Prochlorococcus cyanobacteria, the smallest photosynthetic organism on Earth',
    mpf( '1.0e-12' )    : 'the mass of an E. coli bacterium (wet weight)',
    mpf( '6.0e-12' )    : 'the mass of DNA in a typical diploid human cell (approximate)',
    mpf( '2.2e-11' )    : 'the mass of a human sperm cell',
    mpf( '6.0e-11' )    : 'the mass of a yeast cell (quite variable)',
    mpf( '1.5e-10' )    : 'the mass of a Dunaliella salina, a green algae (dry weight)',
    mpf( '1.0e-9' )     : 'the mass of an average human cell (1 nanogram)',
    mpf( '8.0e-9' )     : 'the mass of a grain of birch pollen',
    mpf( '2.5e-7' )     : 'the mass of a grain of maize pollen',
    mpf( '3.5e-7' )     : 'the mass of a very fine grain of sand (0.063 mm diameter, 350 nanograms)',
    mpf( '3.6e-6' )     : 'the mass of a human ovum',
    mpf( '2.0e-5' )     : 'the uncertainty in the mass of the International Prototype Kilogram (IPK) (+/-20 ug)',
    mpf( '2.2e-5' )     : 'the Planck mass',
    mpf( '7.0e-5' )     : 'the mass of one eyebrow hair (approximate)',
    mpf( '2.5e-4' )     : 'the mass of a fruit fly (dry weight)',
    mpf( '2.5e-3' )     : 'the mass of a mosquito, common smaller species (about 2.5 milligrams)',
    mpf( '2.0e-2' )     : 'the mass of an adult housefly (Musca domestica, 21.4 milligrams)',
    mpf( '2.0e-1' )     : 'one metric carat (200 milligrams)',
    mpf( '0.5' )        : 'the mass of a raisin (approximately 0.5 gram)',
    mpf( '1.0' )        : 'the mass of one cubic centimeter of water (1 gram)',
    mpf( '1.0' )        : 'the mass of a U.S. dollar bill (1 gram)',
    mpf( '7.5' )        : 'the mass of a Euro coin (7.5 grams)',
    mpf( '8.1' )        : 'the mass of a U.S. dollar coin (8.1 grams)',
    mpf( '28.35' )      : 'one ounce (avoirdupois) (28.35 grams)',
    mpf( '4.7e1' )      : 'the mass equivalent of one megaton of TNT equivalent',
    mpf( '1.5e2' )      : 'the mass of a typical orange (100-200 grams)',
    mpf( '4.54e2' )     : 'one pound (avoirdupois) (454 grams)',
    mpf( '1.0e3' )      : 'the mass of one litre of water',
    mpf( '2.0e3' )      : 'the mass of a Chihuahua, the smallest breed of dog (Chihuahua)',
    mpf( '3.25e3' )     : 'the mass of a newborn human baby',
    mpf( '4.0e3' )      : 'the mass of a women\'s shot',
    mpf( '4.5e3' )      : 'the mass of a typical housecat',
    mpf( '7.26e3' )     : 'the mass of a men\'s shot',
    mpf( '1.8e4' )      : 'the mass of a medium-sized dog',
    mpf( '2.0e4' )      : 'the mass of a typical CRT computer monitor',
    mpf( '1.8e5' )      : 'the mass of a typical mature male lion, female (130 kg) and male (180 kg)',
    mpf( '3.5e5' )      : 'the mass of a typical grand piano',
    mpf( '6.5e5' )      : 'the mass of a typical dairy cow',
    mpf( '9.072e5' )    : 'one short ton (2000 pounds - U.S.)',
    mpf( '1.0e6' )      : 'one metric ton/tonne, 1 cubic metre of water',
    mpf( '1.2e6' )      : 'the mass of a typical passenger cars',
    mpf( '5.5e6' )      : 'the mass of an average male African bush elephant',
    mpf( '1.1e7' )      : 'the mass of the Hubble Space Telescope (11 tonnes)',
    mpf( '1.2e7' )      : 'the mass of the largest elephant on record (12 tonnes)',
    mpf( '1.4e7' )      : 'the mass of Big Ben\'s bell (14 tonnes)',
    mpf( '4.4e7' )      : 'the maximum gross mass (truck + load combined) of a semi-trailer truck in the EU (40-44 tonnes)',
    mpf( '7.3e7' )      : 'the mass of the largest dinosaur, Argentinosaurus (73 tonnes)',
    mpf( '1.8e8' )      : 'the mass of the blue whale, the largest animal ever (180 tonnes)',
    mpf( '4.2e8' )      : 'the mass of the International Space Station (417 tonnes)',
    mpf( '4.39985e8' )  : 'the mass of the takeoff weight of a Boeing 747-8',
    mpf( '6.0e8' )      : 'the mass of the world\'s heaviest aircraft: Antonov An-225 (maximum take-off mass: 600 tonnes, payload: 250 tonnes)',
    mpf( '1.0e9' )      : 'the mass of the trunk of the giant sequoia tree, "General Sherman", largest living tree by trunk volume (1121 tonnes)',
    mpf( '2.041e9' )    : 'the launch mass of the Space Shuttle (2041 tonnes)',
    mpf( '6.0e9' )      : 'the mass of the largest clonal colony, the quaking aspen named Pando (largest living organism, 6000 tonnes)',
    mpf( '7.8e9' )      : 'the mass of a Virginia-class nuclear submarine (submerged weight)',
    mpf( '1.0e10' )     : 'the mass of the annual production of Darjeeling tea',
    mpf( '5.2e10' )     : 'the mass of the RMS Titanic when fully loaded (52,000 tonnes)',
    mpf( '9.97e10' )    : 'the mass of the heaviest train ever, Australia\'s BHP Iron Ore, 2001 record (99,700 tonnes)',
    mpf( '6.6e11' )     : 'the mass of the largest ship and largest mobile man-made object, Seawise Giant, when fully loaded (660,000 tonnes)',
    mpf( '4.3e12' )     : 'the mass of matter converted into energy by the Sun each second',
    mpf( '6.0e12' )     : 'the mass of the Great Pyramid of Giza',
    mpf( '6.0e13' )     : 'the mass of the concrete in the Three Gorges Dam, the world\'s largest concrete structure',
    mpf( '1.0e14' )     : 'the mass of a primordial black hole with an evaporation time equal to the age of the universe',
    mpf( '2.0e14' )     : 'the mass of the amount of water stored in London storage reservoirs (0.2 km3)',
    mpf( '4.0e14' )     : 'the total mass of the human world population',
    mpf( '5.0e14' )     : 'the total biomass of Antarctic krill',
    mpf( '1.55e15' )    : 'the global biomass of fish (estaimted)',
    mpf( '4.0e15' )     : 'the mass of the world crude oil production in 2009 (3,843 Mt)',
    mpf( '5.5e15' )     : 'the mass of a teaspoon (5 ml) of neutron star material (5.5 billion tonnes)',
    mpf( '1.0e16' )     : 'the mass of a 1km tall mountain (very approximate)',
    mpf( '1.05e17' )    : 'the total mass of carbon fixed in organic compounds by photosynthesis each year on Earth',
    mpf( '7.2e17' )     : 'the mass of the total carbon stored in Earth\'s atmosphere',
    mpf( '2.0e18' )     : 'the mass of the total carbon stored in the terrestrial biosphere',
    mpf( '3.5e18' )     : 'the mass of the total carbon stored in coal deposits worldwide',
    mpf( '1.0e19' )     : 'the mass of the total carbon content of all organisms on Earth (rough estimate)',
    mpf( '3.8e19' )     : 'the mass of the total carbon stored in the oceans',
    mpf( '1.6e20' )     : 'the mass of Prometheus, a shepherd satellite for the inner edge of Saturn\'s F Ring',
    mpf( '5.1e21' )     : 'the mass of the Earth\'s atmosphere',
    mpf( '5.6e21' )     : 'the mass of Hyperion, a moon of Saturn',
    mpf( '3.0e22' )     : 'the mass of Juno, the third largest asteroid in the asteroid belt',
    mpf( '3.0e22' )     : 'the mass of the rings of Saturn',
    mpf( '9.4e23' )     : 'the mass of Ceres, the largest asteroid in the asteroid belt',
    mpf( '1.4e24' )     : 'the mass of the Earth\'s oceans',
    mpf( '1.5e24' )     : 'the mass of Charon, the largest moon of Pluto',
    mpf( '3.3e24' )     : 'the mass of the Asteroid Belt',
    mpf( '1.3e25' )     : 'the mass of Pluto',
    mpf( '2.1e25' )     : 'the mass of Triton, largest moon of Neptune',
    mpf( '7.3e25' )     : 'the mass of Earth\'s Moon',
    mpf( '1.3e26' )     : 'the mass of Titan, largest moon of Saturn',
    mpf( '1.5e26' )     : 'the mass of Ganymede, largest moon of Jupiter',
    mpf( '3.3e26' )     : 'the mass of Mercury',
    mpf( '6.4e26' )     : 'the mass of Mars',
    mpf( '4.9e27' )     : 'the mass of Venus',
    mpf( '6.0e27' )     : 'the mass of Earth',
    mpf( '3.0e28' )     : 'the mass of Oort cloud',
    mpf( '8.7e28' )     : 'the mass of Uranus',
    mpf( '1.0e29' )     : 'the mass of Neptune',
    mpf( '5.7e29' )     : 'the mass of Saturn',
    mpf( '1.9e30' )     : 'the mass of Jupiter',
    mpf( '8.0e31' )     : 'the mass of a typical brown dwarf',
    mpf( '3.0e32' )     : 'the mass of Barnard\'s Star, a nearby red dwarf',
    mpf( '2.0e33' )     : 'the mass of the Sun',
    mpf( '2.8e33' )     : 'the mass of Chandrasekhar limit (1.4 solar masses)',
    mpf( '4.0e34' )     : 'the mass of Betelgeuse, a red supergiant star (20 solar masses)',
    mpf( '2.5e35' )     : 'the mass of Pistol Star, one of the most massive known stars',
    mpf( '1.6e36' )     : 'the Pleiades star cluster (800 solar masses)',
    mpf( '1.0e38' )     : 'the mass of a typical globular cluster in the Milky Way',
    mpf( '2.4e39' )     : 'the mass of the Gould Belt of stars, including the Sun (1.2e6 solar masses)',
    mpf( '7.5e39' )     : 'the mass of the black hole at the center of the Milky Way, associated with the radio source Sagittarius A* (3.7 +/- 0.2e6 solar masses)',
    mpf( '4.17e43' )    : 'the mass of NGC 4889, the largest measured supermassive black hole (2.1e10 solar masses)',
    mpf( '4.0e44' )     : 'the visible mass of the Milky Way galaxy',
    mpf( '1.2e45' )     : 'the mass of Milky Way galaxy (5.8e11 solar masses)',
    mpf( '2.5e45' )     : 'the mass of the Local Group of galaxies, including the Milky Way',
    mpf( '1.5e48' )     : 'the mass of the Local or Virgo Supercluster of galaxies, including the Local Group',
    mpf( '6.0e55' )     : 'the mass of the observable universe',
}


#//******************************************************************************
#//
#//  powerTable
#//
#//  watts : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28power%29
#//
#//******************************************************************************

powerTable = {

    mpf( '1.0e-20' )    : 'the approximate power of Galileo space probe\'s radio signal (when at Jupiter) as received on earth by a 70-meter DSN antenna',
    mpf( '1.0e-18' )    : 'the approximate power scale at which operation of nanoelectromechanical systems are overwhelmed by thermal fluctuations',
    mpf( '1.0e-16' )    : 'the GPS signal strength measured at the surface of the Earth,[clarification needed] roughly equivalent to viewing a 25-watt light bulb from a distance of 10,000 miles',
    mpf( '2.5e-15' )    : 'the minimum discernible signal at the antenna terminal of a good FM radio receiver',
    mpf( '1.0e-14' )    : 'the approximate lower limit of power reception on digital spread-spectrum cell phones (-110 dBm)',
    mpf( '1.0e-12' )    : 'the average power consumption of a human cell (-90 dBm)',
    mpf( '1.84e-11' )   : 'the power lost in the form of synchrotron radiation by a proton revolving in the Large Hadron Collider at 7000 GeV',
    mpf( '1.50e-10' )   : 'the power entering a human eye from a 100-watt lamp 1 km away',
    mpf( '1.5e-8' )     : 'the upper range of power consumption of 8-bit PIC microcontroller chips when in "sleep" mode',
    mpf( '1.0e-6' )     : 'the approximate consumption of a quartz or mechanical wristwatch (-30 dBm)',
    mpf( '3.0e-6' )     : 'the power of the cosmic microwave background radiation per square meter',
    mpf( '5.0e-3' )     : 'the power of the laser in a CD-ROM drive',
    mpf( '1.0e-2' )     : 'the power of the laser in a DVD player',
    mpf( '7.0e-2' )     : 'the antenna power in a typical consumer wireless router',
    mpf( '5.0e-2' )     : 'the maximum allowed carrier output power of an FRS radio',
    mpf( '2.0' )        : 'the maximum allowed carrier power output of a MURS radio (2 W)',
    mpf( '4.0' )        : 'the power consumption of an incandescent night light (4 W)',
    mpf( '4.0' )        : 'the maximum allowed carrier power output of a 10-meter CB radio (4 W)',
    mpf( '8.0' )        : 'the power output of human-powered equipment using a hand crank (8 W)',
    mpf( '14' )         : 'the power consumption of a typical household compact fluorescent light bulb (14 W)',
    mpf( '30' )         : 'the approximate power consumption of the human brain',
    mpf( '60' )         : 'the power consumption of a 60W incandescent light bulb',
    mpf( '100' )        : 'the approximate basal metabolic rate of an adult human body',
    mpf( '120' )        : 'the electric power output of 1 square meter solar panel in full sunlight (approx. 12% efficiency), at sea level',
    mpf( '130' )        : 'the peak power consumption of a Pentium 4 CPU',
    mpf( '200' )        : 'the average power output of a stationary bicycle average power output',
    mpf( '290' )        : 'one thousand BTU/hour',
    mpf( '400' )        : 'the legal limit of power output of an amateur radio station in the United Kingdom',
    mpf( '500' )        : 'the power output (useful work plus heat) of a person working hard physically',
    mpf( '745.7' )      : 'one horsepower',
    mpf( '750' )        : 'the approximate amount of sunshine falling on a square metre of the Earth\'s surface at noon on a clear day in March for northern temperate latitudes',
    mpf( '909' )        : 'the peak output power of a healthy human (nonathlete) during a 30-second cycle sprint at 30.1 degree Celsius',
    mpf( '1.1e3' )      : 'the power of a typical microwave oven',
    mpf( '1.366e3' )    : 'the power per square metre received from the Sun at the Earth\'s orbit',
    mpf( '1.5e3' )      : 'the legal limit of power output of an amateur radio station in the United States (1.5 kW)',
    mpf( '2.0e3' )      : 'the approximate short-time power output of sprinting professional cyclists and weightlifters doing snatch',
    mpf( '2.4e3' )      : 'the average power consumption per person worldwide in 2008',
    mpf( '4.95e3' )     : 'the average photosynthetic power output per square kilometer of ocean',
    mpf( '3.6e3' )      : 'the synchrotron radiation power lost per ring in the Large Hadron Collider at 7000 GeV',
    mpf( '1.0e4' )      : 'the average power consumption per person in the United States in 2008',
    mpf( '2.4e4' )      : 'the average photosynthetic power output per square kilometer of land',
    mpf( '3.0e4' )      : 'the power generated by the four motors of GEN H-4 one-man helicopter',
    mpf( '1.0e5' )      : 'the highest allowed ERP for an FM band radio station in the United States',
    mpf( '1.67e5' )     : 'the power consumption of UNIVAC 1 computer',
    mpf( '2.0e5' )      : 'the upper limit of power output for typical automobiles',
    mpf( '4.5e5' )      : 'the approximate maximum power output of a large 18-wheeler truck engine',
    mpf( '1.3e6' )      : 'the power output of P-51 Mustang fighter aircraft',
    mpf( '1.5e6' )      : 'the peak power output of GE\'s standard wind turbine',
    mpf( '2.4e6' )      : 'the peak power output of a Princess Coronation class steam locomotive (approx 3.3K EDHP on test) (1937)',
    mpf( '2.5e6' )      : 'the peak power output of a blue whale',
    mpf( '3.0e6' )      : 'the mechanical power output of a diesel locomotive',
    mpf( '1.0e7' )      : 'the highest ERP allowed for an UHF television station',
    mpf( '1.03e7' )     : 'the electrical power output of Togo',
    mpf( '1.22e7' )     : 'the approximate power available to a Eurostar 20-carriage train',
    mpf( '1.6e7' )      : 'the rate at which a typical gasoline pump transfers chemical energy to a vehicle',
    mpf( '2.6e7' )      : 'the peak power output of the reactor of a Los Angeles-class nuclear submarine',
    mpf( '7.5e7' )      : 'the maximum power output of one GE90 jet engine as installed on the Boeing 777',
    mpf( '1.4e8' )      : 'the average power consumption of a Boeing 747 passenger aircraft',
    mpf( '1.9e8' )      : 'the peak power output of a Nimitz-class aircraft carrier',
    mpf( '9.0e8' )      : 'the electric power output of a CANDU nuclear reactor',
    mpf( '9.59e8' )     : 'the average electrical power consumption of Zimbabwe in 1998',
    mpf( '1.3e9' )      : 'the electric power output of Manitoba Hydro Limestone hydroelectric generating station',
    mpf( '2.074e9' )    : 'the peak power generation of Hoover Dam',
    mpf( '2.1e9' )      : 'the peak power generation of Aswan Dam',
    mpf( '4.116e9' )    : 'the installed capacity of Kendal Power Station, the world\'s largest coal-fired power plant',
    mpf( '8.21e9' )     : 'the capacity of the Kashiwazaki-Kariwa Nuclear Power Plant, the world\'s largest nuclear power plant',
    mpf( '1.17e10' )    : 'the power produced by the Space Shuttle in liftoff configuration (9.875 GW from the SRBs; 1.9875 GW from the SSMEs)',
    mpf( '1.26e10' )    : 'the electrical power generation of the Itaipu Dam',
    mpf( '1.27e10' )    : 'the average electrical power consumption of Norway in 1998',
    mpf( '1.83e10' )    : 'the peak electrical power generation of the Three Gorges Dam, the world\'s largest hydroelectric power plant of any type',
    mpf( '5.5e10' )     : 'the peak daily electrical power consumption of Great Britain in November 2008',
    mpf( '7.4e10' )     : 'the total installed wind turbine capacity at end of 2006',
    mpf( '1.016e11' )   : 'the peak electrical power consumption of France (February 8, 2012 at 7:00 pm)',
    mpf( '1.90e11' )    : 'the average power consumption of the first stage of the Saturn V rocket',
    mpf( '7.00e11' )    : 'the cumulative basal metabolic rate of all humans as of 2013 (7 billion people)',
    mpf( '2.0e12' )     : 'the approximate power generated between the surfaces of Jupiter and its moon Io due to Jupiter\'s magnetic field',
    mpf( '3.34e12' )    : 'the average total (gas, electricity, etc.) power consumption of the US in 2005',
    mpf( '1.6e13' )     : 'the average total power consumption of the human world in 2010',
    mpf( '4.4e13' )     : 'the average total heat flux from Earth\'s interior',
    mpf( '7.5e13' )     : 'the global net primary production (= biomass production) via photosynthesis',
    mpf( '1.25e14' )    : 'the typical rate of heat energy release by a hurricane',
    mpf( '2.90e14' )    : 'the power the Z machine reaches in 1 billionth of a second when it is fired',
    mpf( '3.0e14' )     : 'the power reached by the extremely high-power Hercules laser from the University of Michigan.',
    mpf( '1.1e15' )     : 'the world\'s most powerful laser pulses by laser still in operation (claimed on March 31, 2008 by Texas Center for High Intensity Laser Science at The University of Texas at Austin)',
    mpf( '1.25e15' )    : 'the world\'s most powerful laser pulses (claimed on May 23, 1996 by Lawrence Livermore Laboratory)',
    mpf( '1.4e15' )     : 'the estimated heat flux transported by the Gulf Stream.',
    mpf( '4.0e15' )     : 'the estimated total heat flux transported by Earth\'s atmosphere and oceans away from the equator towards the poles',
    mpf( '5.0e15' )     : 'the estimated total power output of a Type-I civilization on the Kardashev scale',
    mpf( '1.74e17' )    : 'the total power received by Earth from the Sun',
    mpf( '2.0e17' )     : 'the power of the Extreme Light Infrastructure laser',
    mpf( '1.35e23' )    : 'the approximate luminosity of Wolf 359',
    mpf( '3.38e25' )    : 'the peak power output of the Tsar Bomba, the largest nuclear weapon ever built',
    mpf( '5.0e25' )     : 'the estimated total power output of a Type-II civilization on the Kardashev scale',
    mpf( '3.846e26' )   : 'the luminosity of the Sun',
    mpf( '3.31e31' )    : 'the approximate luminosity of Beta Centauri',
    mpf( '1.23e32' )    : 'the approximate luminosity of Deneb',
    mpf( '5.0e36' )     : 'the approximate luminosity of the Milky Way galaxy',
    mpf( '1.0e40' )     : 'the approximate luminosity of a quasar',
    mpf( '1.0e42' )     : 'the approximate luminosity of the Local Supercluster',
    mpf( '1.0e45' )     : 'the approximate luminosity of a gamma-ray burst',
    mpf( '2.0e49' )     : 'the approximate total luminosity of all the stars in the observable universe',
    mpf( '3.63e52' )    : 'the Planck power',
}


#//******************************************************************************
#//
#//  pressureTable
#//
#//  pascals : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28pressure%29
#//  https://en.wikipedia.org/wiki/Sound_pressure
#//
#//******************************************************************************

pressureTable = {

    mpf( '1.0e-17' )    : 'the estimated pressure in outer space in intergalactic voids',
    mpf( '5.0e-15' )    : 'the typical pressure in outer space between stars in the Milky Way',
    mpf( '1.0e-12' )    : 'the lowest pressure obtained in laboratory conditions (1 picopascal)',
    mpf( '4.0e-11' )    : 'the atmosphere pressure of the Moon at lunar day, very approximately (40 picopascals)',
    mpf( '1.0e-10' )    : 'the atmospheric pressure of Mercury, very approximately (100 pPa)',
    mpf( '8.0e-10' )    : 'the atmospheric pressure of the Moon at lunar night, very approximately (800 pPa)',
    mpf( '1.0e-9' )     : 'the vacuum expected in the beam pipe of the Large Hadron Collider\'s Atlas experiment (< 1 nPa)',
    mpf( '1.0e-9' )     : 'the approximate solar wind pressure at Earth\'s distance from the Sun',
    mpf( '1.0e-8' )     : 'the pressure inside a vacuum chamber for laser cooling of atoms (magneto-optical trap, 10 nPa)',
    mpf( '1.0e-7' )     : 'the highest pressure still considered ultra high vacuum (100 nPa)',
    mpf( '1.0e-6' )     : 'the pressure inside a vacuum tube, very approximate, (1 uPa)',
    mpf( '1.0e-6' )     : 'the radiation pressure of sunlight on a perfectly reflecting surface at the distance of the Earth',
    mpf( '2.0e-5' )     : 'the reference pressure for sound in air, and the threshold of human hearing (0 dB)',
    mpf( '1.0e-1' )     : 'the upper limit of high vacuum (100 mPa)',
    mpf( '2.0e-1' )     : 'the atmospheric pressure on Pluto (1988 figure; very roughly, 200 mPa)',
    mpf( '1.0' )        : 'the pressure exerted by a US dollar bill resting flat on a surface',
    mpf( '10' )         : 'the pressure increase per millimeter of a water column at Earth mean sea level',
    mpf( '10' )         : 'the pressure due to direct impact of a gentle breeze (~9 mph or 14 km/h)',
    mpf( '86' )         : 'the pressure from the weight of a U.S. penny lying flat',
    mpf( '100' )        : 'the pressure due to direct impact of a strong breeze (~28 mph or 45 km/h)',
    mpf( '120' )        : 'the pressure from the weight of a U.S. quarter lying flat',
    mpf( '133.3224' )   : 'one torr ~= 1 mmHg (133.3224 pascals)',
    mpf( '300' )        : 'the lung air pressure difference moving the normal breaths of a person (only 0.3% of standard atmospheric pressure)',
    mpf( '610' )        : 'the partial vapour pressure at the triple point of water (611.73 Pa)',
    mpf( '650' )        : 'a typical atmospheric pressure on Mars, < 1% of atmospheric sea-level pressure on Earth',
    mpf( '2.0e3' )      : 'the pressure of popping popcorn (very approximate)',
    mpf( '2.6e3' )      : 'the pressure to make water boil at room temperature (22 degrees C) (0.38 psi, 20 mmHg)',
    mpf( '5.0e3' )      : 'the blood pressure fluctuation (40 mmHg) between heartbeats for a typical healthy adult (0.8 psi)',
    mpf( '6.3e3' )      : 'the pressure where water boils at normal human body temperature (37 degrees C), the pressure below which humans absolutely cannot survive (Armstrong Limit), 0.9 psi',
    mpf( '9.8e3' )      : 'the lung pressure that a typical person can exert (74 mmHg, 1.4 psi)',
    mpf( '1.0e4' )      : 'the pressure increase per meter of a water column',
    mpf( '1.0e4' )      : 'the decrease in air pressure when going from Earth sea level to 1000 m elevation',
    mpf( '1.3e4' )      : 'the pressure for human lung, measured for trumpet player making staccato high notes (1.9 psi)',
    mpf( '1.6e4' )      : 'the systolic blood pressure in a healthy adult while at rest (< 120 mmHg gauge pressure)',
    mpf( '1.93e4' )     : 'the high end of lung pressure, exertable without injury by a healthy person for brief times (2.8 psi)',
    mpf( '3.4e4' )      : 'the level of long-duration blast overpressure (from a large-scale explosion) that would cause most buildings to collapse (5 psi)',
    mpf( '7.0e4' )      : 'the pressure inside an incandescent light bulb',
    mpf( '8.0e4' )      : 'the pressure inside vacuum cleaner at sea level on Earth (80% of standard atmospheric pressure, 11.6 psi)',
    mpf( '8.7e4' )      : 'the record low atmospheric pressure for typhoon/hurricane (Typhoon Tip in 1979) (only 86% of standard atmospheric pressure, 12.6 psi)',
    mpf( '1.0e5' )      : 'one bar (14.5 psi), approximately equal to the weight of one kilogram (1 kilopond) acting on one square centimeter',
    mpf( '3.5e5 ' )     : 'the typical impact pressure of a fist punch (approximate)',
    mpf( '2.0e5' )      : 'the typical air pressure in an automobile tire relative to atmosphere (30 psi gauge pressure)',
    mpf( '3.0e5' )      : 'the water pressure of a garden hose (50 psi)',
    mpf( '5.17e5' )     : 'the carbon dioxide pressure in a champagne bottle',
    mpf( '5.2e5' )      : 'the partial vapour pressure at the triple point of carbon dioxide (75 psi)',
    mpf( '7.6e5' )      : 'the air pressure in a heavy truck/bus tire relative to atmosphere (110 psi gauge pressure)',
    mpf( '8.0e5' )      : 'the vapor pressure of water in a kernel of popcorn when the kernel ruptures',
    mpf( '1.1e6' )      : 'the pressure of an average human bite (162 psi)',
    mpf( '2.0e6' )      : 'the maximum typical pressure used in boilers of steam locomotives (290 psi)',
    mpf( '5.0e6' )      : 'the maximum rated pressure for the Seawold class military nuclear submarine (estimated), at a depth of 500 m (700 psi)',
    mpf( '9.2e6' )      : 'the atmospheric pressure of Venus (92 bar, 1,300 psi)',
    mpf( '1.0e7' )      : 'the pressure exerted by a 45 kg woman wearing stiletto heels when a heel hits the floor (1,450 psi)',
    mpf( '1.5e7' )      : 'the power stroke maximum pressure in diesel truck engine when burning fuel (2,200 psi)',
    mpf( '2.0e7' )      : 'the typical pressure used for hydrogenolysis reactions (2,900 psi)',
    mpf( '2.1e7' )      : 'the pressure of a typical aluminium scuba tank of pressurized air (210 bar, 3,000 psi)',
    mpf( '2.8e7' )      : 'the overpressure caused by the bomb explosion during the Oklahoma City bombing',
    mpf( '6.9e7' )      : 'the water pressure withstood by the DSV Shinkai 6500 in visiting ocean depths of > 6500 meters (10,000 psi)',
    mpf( '1.1e8' )      : 'the pressure at bottom of Mariana Trench, about 11 km below ocean surface (1,100 bar, 16,000 psi)',
    mpf( '2.0e8' )      : 'the approximate pressure inside a reactor for the synthesis of high-pressure polyethylene (HPPE)',
    mpf( '2.8e8' )      : 'the maximum chamber pressure during a pistol firing (40,000 psi)',
    mpf( '4.0e8' )      : 'the chamber pressure of a late 1910s .50 Browning Machine Gun discharge (58,000 psi)',
    mpf( '6.2e8' )      : 'the water pressure used in a water jet cutter (90,000 psi)',
    mpf( '1.0e9' )      : 'the pressure of extremely high-pressure chemical reactors (10 kbar)',
    mpf( '1.5e9' )      : 'the pressure at which diamond melts using a 3 kJ laser without turning into graphite first',
    mpf( '1.5e9' )      : 'the tensile strength of Inconel 625 according to Aircraft metal strength tables and the Mil-Hdbk-5 (220,000 psi)',
    mpf( '5.8e9' )      : 'the ultimate tensile strength of the polymer Zylon (840,000 psi)',
    mpf( '1.0e10' )     : 'the pressure at which octaoxygen forms at room temperature (100,000 bar)',
    mpf( '1.8e10' )     : 'the pressure needed for the first commercially successful synthesis of diamond',
    mpf( '2.4e10' )     : 'the lower range of stability for enstatite in its perovskite-structured polymorph, possibly the most common mineral inside the Earth',
    mpf( '1.1e11' )     : 'the upper range of stability for enstatite in its perovskite-structured polymorph, possibly the most common mineral inside the Earth',
    mpf( '4.0e10' )     : 'the quantum mechanical electron degeneracy pressure in a block of copper',
    mpf( '4.8e10' )     : 'the detonation pressure of pure CL-20, the most powerful high explosive in mass production',
    mpf( '6.9e10' )     : 'the highest water jet pressure made in research lab (approx. 1 million psi)',
    mpf( '9.6e10' )     : 'the pressure at which metallic oxygen forms (960,000 bar)',
    mpf( '1.0e11' )     : 'the theoretical tensile strength of a carbon nanotube (CNT)',
    mpf( '1.3e11' )     : 'the intrinsic strength of monolayer graphene',
    mpf( '3.0e11' )     : 'the pressure attainable with a diamond anvil cell',
    mpf( '3.6e11' )     : 'the pressure inside the core of the Earth (3.64 million bar)',
    mpf( '5.4e14' )     : 'the pressure inside an Ivy Mike-like nuclear bomb detonation (5.3 billion bar)',
    mpf( '6.5e15' )     : 'the pressure inside a W80 nuclear warhead detonation (64 billion bar)',
    mpf( '2.5e16' )     : 'the pressure inside the core of the Sun (250 billion bar)',
    mpf( '5.7e16' )     : 'the pressure inside a uranium nucleus (8 MeV in a sphere of radius 175 pm)',
    mpf( '1.0e34' )     : 'the Pressure range inside a neutron star (0.3 to 1.6 x 10^34)',
    mpf( '4.6e113' )    : 'the Planck pressure',
}


#//******************************************************************************
#//
#//  radiationDoseTable
#//
#//  sieverts : description
#//
#//  https://en.wikipedia.org/wiki/Sievert
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28radiation%29
#//
#//******************************************************************************

radiationDoseTable = {
    mpf( '1.0e-6' )     : 'the cosmic ray dose rate on commercial flights, which varies from 1 to 10 uSv/hour, depending on altitude, position and solar sunspot phase',
    mpf( '1.0e-5' )     : 'the daily exposure due to natural background radiation, including radon',
    mpf( '6.0e-5' )     : 'the radiation dose from a chest X-ray (AP+Lat)',
    mpf( '7.0e-5' )     : 'the radiation dose from a transatlantic airplane flight',
    mpf( '9.0e-5' )     : 'the radiation dose from a dental X-ray (panoramic)',
    mpf( '1.0e-4' )     : 'the average USA dose from consumer products in a year',
    mpf( '1.5e-4' )     : 'the USA EPA cleanup annual dose standard',
    mpf( '2.5e-4' )     : 'the USA NRC cleanup annual dose standard for individual sites/sources',
    mpf( '2.7e-4' )     : 'the yearly dose from natural cosmic radiation at sea level (0.5 in Denver due to altitude)',
    mpf( '2.8e-4' )     : 'the yearly dose from natural terrestrial radiation in the USA (0.16-0.63 mSv depending on soil composition)',
    mpf( '4.6e-4' )     : 'the estimated largest off-site dose possible from March 28, 1979 Three Mile Island accident',
    mpf( '4.8e-4' )     : 'the USA NRC public area daily exposure limit',
    mpf( '6.6e-4' )     : 'the average annual dose from human-made sources in the USA',
    mpf( '7.0e-4' )     : 'the radiation dose from a mammogram',
    mpf( '1.0e-3' )     : 'the limit of annual dose from man-made sources to someone who is not a radiation worker in the USA and Canada',
    mpf( '1.1e-3' )     : 'the average USA radiation worker annual occupational dose in 1980',
    mpf( '1.2e-3' )     : 'the radiation dose from an abdominal X-ray',
    mpf( '2.0e-3' )     : 'the USA average annual dose from medical and natural background radiation',
    mpf( '2.0e-3' )     : 'the human internal annual radiation dose due to radon, varies with radon levels',
    mpf( '2.0e-3' )     : 'the radiation dose from a head CT',
    mpf( '3.0e-3' )     : 'the USA average annual dose from all natural sources',
    mpf( '3.66e-3' )    : 'the USA average annual dose from all sources, including medical diagnostic radiation doses',
    mpf( '4.0e-3' )     : 'the Canada CNSC maximum occupational dose to a pregnant woman who is a designated Nuclear Energy Worker',
    mpf( '5.0e-3' )     : 'the USA NRC occupational annual dose limit for minors (10% of adult limit)',
    mpf( '5.0e-3' )     : 'the USA NRC occupational limit for pregnant women',
    mpf( '6.4e-3' )     : 'the annual dose received at the High Background Radiation Area (HBRA) of Yangjiang, China',
    mpf( '7.6e-3' )     : 'the annual dose received at Fountainhead Rock Place, Santa Fe, NM from natural sources',
    mpf( '8.0e-3' )     : 'the radiation dose from a chest CT',
    mpf( '1.0e-2' )     : 'the lower dose level for public calculated from the 1 to 5 rem range for which USA EPA guidelines mandate emergency action when resulting from a nuclear accident',
    mpf( '1.0e-2' )     : 'the radiation dose from an Abdominal CT',
    mpf( '5.0e-2' )     : 'the USA NRC/ Canada CNSC occupational annual dose limit for designated Nuclear Energy Workers',
    mpf( '1.0e-1' )     : 'the Canada CNSC occupational limit over a 5-year dosimetry period for designated Nuclear Energy Workers',
    mpf( '1.0e-1' )     : 'the USA EPA acute dose level estimated to increase cancer risk 0.8%',
    mpf( '1.75e-1' )    : 'the annual exposure from natural radiation in Guarapari, Brazil',
    mpf( '2.5e-1' )     : 'the whole body dose exclusion zone criteria for US nuclear reactor siting (2 hours)',
    mpf( '2.5e-1' )     : 'the USA EPA voluntary maximum dose for emergency non-life-saving work',
    mpf( '2.60e-1' )    : 'the annual exposure calculated from 260 mGy per year peak natural background dose in Ramsar',
    mpf( '5.0e-1' )     : 'the USA NRC occupational whole skin, limb skin, or single organ annual exposure limit',
    mpf( '5.0e-1' )     : 'the Canada CNSC occupational limit for designated Nuclear Energy Workers carrying out urgent and necessary work during an emergency',
    mpf( '7.5e-1' )     : 'the USA EPA voluntary maximum dose for emergency life-saving work',
    mpf( '1.0' )        : 'the hourly exposure level reported during Fukushima I nuclear accidents, in immediate vicinity of reactor',
    mpf( '3.0' )        : 'the thyroid dose (due to iodine absorption) exclusion zone criteria for US nuclear reactor siting (converted from 300 rem)',
    mpf( '4.8' )        : 'the LD50 exposure level (actually LD50/60) in humans from radiation poisoning with medical treatment, estimated from 480 to 540 rem',
    mpf( '5.0' )        : 'the exposure from the estimated 510 rem dose fatally received by Harry Daghlian on 1945 August 21 at Los Alamos and the lower estimate for fatality of Russian specialist on 1968 April 5 at Chelyabinsk-70',
    mpf( '5.0' )        : 'the level of exposure most commercial electronics can survive (5 - 10 Sv)',
    mpf( '21' )         : 'the exposure from the estimated 2100 rem dose fatally received by Louis Slotin on 1946 May 21 at Los Alamos and the lower estimate for fatality of Russian specialist on 1968 April 5 Chelyabinsk-70',
    mpf( '48.5' )       : 'the exposure from the estimated 4500 + 350 rad dose for fatality of Russian experimenter on 1997 June 17 at Sarov',
    mpf( '60.0' )       : 'the exposure from the estimated 6000 rem doses for several Russian fatalities from 1958 onwards, such as on 1971 May 26 at the Kurchatov Institute. The lower estimate for a Los Alamos fatality in 1958 December 30.',
    mpf( '100' )        : 'the exposure from the estimated 10000 rad dose for fatality at the United Nuclear Fuels Recovery Plant on 1964 July 24',
    mpf( '200' )        : 'the exposure of some Chernobyl emergency workers over 1100 hours (170 mSv)',
    mpf( '1000000' )    : 'the radiation level most radiation-hardened electronics can survive',
}


#//******************************************************************************
#//
#//  radiationExposureTable
#//
#//  coulombs/gram : description
#//
#//******************************************************************************

radiationExposureTable = {
}


#//******************************************************************************
#//
#//  radioactivityTable
#//
#//  becquerels : description
#//
#//  https://en.wikipedia.org/wiki/List_of_radioactive_isotopes_by_half-life
#//
#//******************************************************************************

#radioactivityTable = {
#    mpf( '1' )  : 'hydrogen-7 (half-life: 23e-24 s)',
#    mpf( '1' )  : 'hydrogen-5 (half-life: 80e-24 s)',
#    mpf( '1' )  : 'hydrogen-4 (half-life: 100e-24 s)',
#    mpf( '1' )  : 'nitrogen-10 (half-life: 200e-24 s)',
#    mpf( '1' )  : 'hydrogen-6 (half-life: 290e-24 s)',
#    mpf( '1' )  : 'lithium-5 (half-life: 324e-24 s)',
#    mpf( '1' )  : 'lithium-4 (half-life: 325e-24 s)',
#    mpf( '1' )  : 'boron-7 (half-life: 350e-24 s)',
#    mpf( '1' )  : 'helium-5 (half-life: 760e-24 s)',
#    mpf( '1' )  : 'helium-10 (half-life: 1.52e-21 s)',
#    mpf( '1' )  : 'lithium-10 (half-life: 2.0e-21 s)',
#    mpf( '1' )  : 'carbon-8 (half-life: 2.0e-21 s)',
#    mpf( '1' )  : 'helium-7 (half-life: 3.040e-21 s)',
#    mpf( '1' )  : 'beryllium-6 (half-life: 5.0e-21 s)',
#    mpf( '1' )  : 'helium-9 (half-life: 7.0e-21 s)',
#    mpf( '1' )  : 'boron-9 (half-life: 800e-21 s)',
#    mpf( '1' )  : 'beryllium-8 (half-life: 81.9e-18 s)',
#    mpf( '1' )  : 'boron-16 (half-life: 190e-12 s)',
#    mpf( '1' )  : 'beryllium-13 (half-life: 500e-12 s)',
#    mpf( '1' )  : 'lithium-12 (half-life: 10e-9 s)',
#    mpf( '1' )  : 'boron-18 (half-life: 26e-9 s)',
#    mpf( '1' )  : 'carbon-21 (half-life: 30e-9 s)',
#    mpf( '1' )  : 'beryllium-15 (half-life: 200e-9 s)',
#    mpf( '1' )  : 'beryllium-16 (half-life: 200e-9 s)',
#    mpf( '1' )  : 'Copernicium-277 (half-life: 240e-6 s)',
#    mpf( '1' )  : 'hassium-265 (half-life: 2.0e-3 s)',
#    mpf( '1' )  : 'boron-19 (half-life: 2.92e-3 s)',
#    mpf( '1' )  : 'meitnerium-266 (half-life: 3.4e-3 s)',
#    mpf( '1' )  : 'boron-17 (half-life: 5.08e-3 s)',
#    mpf( '1' )  : 'carbon-22 (half-life: 6.2e-3 s)',
#    mpf( '1' )  : 'lithium-11 (half-life: 8.59e-3 s)',
#    mpf( '1' )  : 'boron-15 (half-life: 9.87e-3 s)',
#    mpf( '1' )  : 'boron-14 (half-life: 12.5e-3 s)',
#    mpf( '1' )  : 'carbon-20 (half-life: 16e-3 s)',
#    mpf( '1' )  : 'boron-13 (half-life: 17.33e-3 s)',
#    mpf( '1' )  : 'boron-12 (half-life: 20.2e-3 s)',
#    mpf( '1' )  : 'beryllium-12 (half-life: 21.49e-3 s)',
#    mpf( '1' )  : 'carbon-19 (half-life: 46.2e-3 s)',
#    mpf( '1' )  : 'carbon-18 (half-life: 92e-3 s)',
#    mpf( '1' )  : 'bohrium-262 (half-life: 102e-3 s)',
#    mpf( '1' )  : 'helium-8 (half-life: 119e-3 s)',
#    mpf( '1' )  : 'carbon-9 (half-life: 126.5e-3 s)',
#    mpf( '1' )  : 'lithium-9 (half-life: 178.3e-3 s)',
#    mpf( '1' )  : 'carbon-17 (half-life: 193e-3 s)',
#    mpf( '1' )  : 'carbon-16 (half-life: 747e-3 s)',
#    mpf( '1' )  : 'boron-8 (half-life: 770e-3 s)',
#    mpf( '1' )  : 'helium-6 (half-life: 806.7 s)',
#    mpf( '1' )  : 'lithium-8 (half-life: 839.9e-3 s)',
#    mpf( '1' )  : 'carbon-15 (half-life: 2.449 s)',
#    mpf( '1' )  : 'flerovium-289 (half-life: 2.6 s)',
#    mpf( '1' )  : 'beryllium-14 (half-life: 4.84 s)',
#    mpf( '1' )  : 'beryllium-11 (half-life: 13.81 s)',
#    mpf( '1' )  : 'carbon-10 (half-life: 19.29 s)',
#    mpf( '1' )  : 'dubnium-261 (half-life: 27 s)',
#    mpf( '1' )  : 'seaborgium-266 (half-life: 30 s)',
#    mpf( '1' )  : 'dubnium-262 (half-life: 34 s)',
#    mpf( '1' )  : 'rutherfordium-261 (half-life: 81 s)',
#    mpf( '1' )  : 'nobelium-253 (half-life: 97 s)',
#    mpf( '1' )  : 'carbon-11 (half-life: 1.22e3 s)',
#    mpf( '1' )  : 'nobelium-259 (half-life: 3.5e3 s)',
#    mpf( '1' )  : 'fluorine-18 (half-life: 6.586e3 s)',
#    mpf( '1' )  : 'mendelevium-257 (half-life: 19.9e3 s)',
#    mpf( '1' )  : 'erbium-165 (half-life: 37.3e3 s)',
#    mpf( '1' )  : 'sodium-24 (half-life: 53.9e3 s)',
#    mpf( '1' )  : 'fermium-252 (half-life: 91.4e3 s)',
#    mpf( '1' )  : 'erbium-160 (half-life: 102.9e3 s)',
#    mpf( '1' )  : 'fermium-253 (half-life: 260e3 s)',
#    mpf( '1' )  : 'manganese-52 (half-life: 483.1e3 s)',
#    mpf( '1' )  : 'thulium-167 (half-life: 799e3 s)',
#    mpf( '1' )  : 'vanadium-48 (half-life: 1.38011e6 s)',
#    mpf( '1' )  : 'californium-253 (half-life: 1.539e6 s)',
#    mpf( '1' )  : 'chromium-51 (half-life: 2.39350e6 s)',
#    mpf( '1' )  : 'mendelevium-258 (half-life: 4.45e6 s)',
#    mpf( '1' )  : 'beryllium-7 (half-life: 4.590e6 s)',
#    mpf( '1' )  : 'californium-254 (half-life: 5.23e6 s)',
#    mpf( '1' )  : 'cobalt-56 (half-life: 6.676e6 s)',
#    mpf( '1' )  : 'scandium-46 (half-life: 7.239e6 s)',
#    mpf( '1' )  : 'sulfur-35 (half-life: 7.544e6 s)',
#    mpf( '1' )  : 'thulium-168 (half-life: 8.04e6 s)',
#    mpf( '1' )  : 'fermium-257 (half-life: 8.68e6 s)',
#    mpf( '1' )  : 'thulium-170 (half-life: 11.11e6 s)',
#    mpf( '1' )  : 'polonium-210 (half-life: 11.9e6 s)',
#    mpf( '1' )  : 'cobalt-57 (half-life: 23.483e6 s)',
#    mpf( '1' )  : 'vanadium-49 (half-life: 29e6 s)',
#    mpf( '1' )  : 'californium-248 (half-life: 28.81e6 s)',
#    mpf( '1' )  : 'ruthenium-106 (half-life: 32.3e6 s)',
#    mpf( '1' )  : 'neptunium-235 (half-life: 34.2e6 s)',
#    mpf( '1' )  : 'cadmium-109 (half-life: 40.0e6 s)',
#    mpf( '1' )  : 'thulium-171 (half-life: 61e6 s)',
#    mpf( '1' )  : 'caesium-134 (half-life: 65.17e6 s)',
#    mpf( '1' )  : 'sodium-22 (half-life: 82.1e6 s)',
#    mpf( '1' )  : 'rhodium-101 (half-life: 100e6 s)',
#    mpf( '1' )  : 'cobalt-60 (half-life: 166.35e6 s)',
#    mpf( '1' )  : 'hydrogen-3 (half-life: 389e6 s)',
#    mpf( '1' )  : 'californium-250 (half-life: 413e6 s)',
#    mpf( '1' )  : 'niobium meta state Nb-93m (half-life: 509e6 s)',
#    mpf( '1' )  : 'strontium-90 (half-life: 909e6 s)',
#    mpf( '1' )  : 'curium-243 (half-life: 920e6 s)',
#    mpf( '1' )  : 'caesium-137 (half-life: 952e6 s)',
#    mpf( '1' )  : 'titanium-44 (half-life: 2.0e9 s)',
#    mpf( '1' )  : 'uranium-232 (half-life: 2.17e9 s)',
#    mpf( '1' )  : 'plutonium-238 (half-life: 2.77e9 s)',
#    mpf( '1' )  : 'nickel-63 (half-life: 3.16e9 s)',
#    mpf( '1' )  : 'silicon-32 (half-life: 5.4e9 s)',
#    mpf( '1' )  : 'argon-39 (half-life: 8.5e9 s)',
#    mpf( '1' )  : 'californium-249 (half-life: 11.1e9 s)',
#    mpf( '1' )  : 'silver-108 (half-life: 13.2e9 s)',
#    mpf( '1' )  : 'americium-241 (half-life: 13.64e9 s)',
#    mpf( '1' )  : 'niobium-91 (half-life: 21e9 s)',
#    mpf( '1' )  : 'californium-251 (half-life: 28.3e9 s)',
#    mpf( '1' )  : 'holmium-166(m1) (half-life: 38e9 s)',
#    mpf( '1' )  : 'berkelium-247 (half-life: 44e9 s)',
#    mpf( '1' )  : 'radium-226 (half-life: 50e9 s)',
#    mpf( '1' )  : 'molybdenum-93 (half-life: 130e9 s)',
#    mpf( '1' )  : 'holmium-153 (half-life: 144e9 s)',
#    mpf( '1' )  : 'curium-246 (half-life: 149e9 s)',
#    mpf( '1' )  : 'carbon-14 (half-life: 181e9 s)',
#    mpf( '1' )  : 'plutonium-240 (half-life: 207.1e9 s)',
#    mpf( '1' )  : 'thorium-229 (half-life: 232e9 s)',
#    mpf( '1' )  : 'americium-243 (half-life: 233e9 s)',
#    mpf( '1' )  : 'curium-245 (half-life: 270e9 s)',
#    mpf( '1' )  : 'curium-250 (half-life: 280e9 s)',
#    mpf( '1' )  : 'tin-126 (half-life: 320e9 s)',
#    mpf( '1' )  : 'niobium-94 (half-life: 640e9 s)',
#    mpf( '1' )  : 'plutonium-239 (half-life: 761e9 s)',
#    mpf( '1' )  : 'protactinium-231 (half-life: 1.034e12 s)',
#    mpf( '1' )  : 'lead-202 (half-life: 1.66e12 s)',
#    mpf( '1' )  : 'lanthanum-137 (half-life: 1.9e12 s)',
#    mpf( '1' )  : 'thorium-230 (half-life: 2.379e12 s)',
#    mpf( '1' )  : 'nickel-59 (half-life: 2.4e12 s)',
#    mpf( '1' )  : 'calcium-41 (half-life: 3.3e12 s)',
#    mpf( '1' )  : 'neptunium-236 (half-life: 4.9e12 s)',
#    mpf( '1' )  : 'uranium-233 (half-life: 5.02e12 s)',
#    mpf( '1' )  : 'rhenium-186 (half-life: 6.3e12 s)',
#    mpf( '1' )  : 'technetium-99 (half-life: 6.66e12 s)',
#    mpf( '1' )  : 'krypton-81 (half-life: 7.2e12 s)',
#    mpf( '1' )  : 'uranium-234 (half-life: 7.75e12 s)',
#    mpf( '1' )  : 'chlorine-36 (half-life: 9.5e12 s)',
#    mpf( '1' )  : 'curium-248 (half-life: 11e12 s)',
#    mpf( '1' )  : 'bismuth-208 (half-life: 11.6e12 s)',
#    mpf( '1' )  : 'plutonium-242 (half-life: 11.77e12 s)',
#    mpf( '1' )  : 'aluminium-26 (half-life: 22.6e12 s)',
#    mpf( '1' )  : 'selenium-79 (half-life: 36e12 s)',
#    mpf( '1' )  : 'iron-60 (half-life: 47e12 s)',
#    mpf( '1' )  : 'beryllium-10 (half-life: 43e12 s)',
#    mpf( '1' )  : 'zirconium-93 (half-life:  s)',
#    mpf( '1' )  : 'gadolinium-150 (half-life:  s)',
#    mpf( '1' )  : 'neptunium-237 (half-life:  s)',
#    mpf( '1' )  : 'caesium-135 (half-life:  s)',
#    mpf( '1' )  : 'technetium-97 (half-life:  s)',
#    mpf( '1' )  : 'dysprosium-154 (half-life:  s)',
#    mpf( '1' )  : 'bismuth-210 (half-life:  s)',
#    mpf( '1' )  : 'manganese-53 (half-life:  s)',
#    mpf( '1' )  : 'technetium-98 (half-life:  s)',
#    mpf( '1' )  : 'palladium-107 (half-life:  s)',
#    mpf( '1' )  : 'hafnium-182 (half-life:  s)',
#    mpf( '1' )  : 'lead-205 (half-life:  s)',
#    mpf( '1' )  : 'curium-247 (half-life:  s)',
#    mpf( '1' )  : 'iodine-129 (half-life:  s)',
#    mpf( '1' )  : 'uranium-236 (half-life:  s)',
#    mpf( '1' )  : 'niobium-92 (half-life:  s)',
#    mpf( '1' )  : 'plutonium-244 (half-life:  s)',
#    mpf( '1' )  : 'samarium-146 (half-life:  s)',
#    mpf( '1' )  : 'uranium-235 (half-life:  s)',
#    mpf( '1' )  : 'potassium-40 (half-life:  s)',
#    mpf( '1' )  : 'uranium-238 (half-life:  s)',
#    mpf( '1' )  : 'thorium-232 (half-life:  s)',
#    mpf( '1' )  : 'lutetium-176 (half-life:  s)',
#    mpf( '1' )  : 'rhenium-187 (half-life:  s)',
#    mpf( '1' )  : 'rubidium-87 (half-life:  s)',
#    mpf( '1' )  : 'lanthanum-138 (half-life:  s)',
#    mpf( '1' )  : 'samarium-147 (half-life:  s)',
#    mpf( '1' )  : 'platinum-190 (half-life:  s)',
#    mpf( '1' )  : 'gadolinium-152 (half-life:  s)',
#    mpf( '1' )  : 'indium-115 (half-life:  s)',
#    mpf( '1' )  : 'tantalum-180 (half-life:  s)',
#    mpf( '1' )  : 'hafnium-174 (half-life:  s)',
#    mpf( '1' )  : 'osmium-186 (half-life:  s)',
#    mpf( '1' )  : 'neodymium-144 (half-life:  s)',
#    mpf( '1' )  : 'samarium-148 (half-life:  s)',
#    mpf( '1' )  : 'cadmium-113 (half-life:  s)',
#    mpf( '1' )  : 'vanadium-50 (half-life:  s)',
#    mpf( '1' )  : 'tungsten-180 (half-life:  s)',
#    mpf( '1' )  : 'europium-151 (half-life:  s)',
#    mpf( '1' )  : 'neodymium-150 (half-life:  s)',
#    mpf( '1' )  : 'molybdenum-100 (half-life:  s)',
#    mpf( '1' )  : 'bismuth-209 (half-life:  s)',
#    mpf( '1' )  : 'zirconium-96 (half-life:  s)',
#    mpf( '1' )  : 'cadmium-116 (half-life:  s)',
#    mpf( '1' )  : 'calcium-48  43 (half-life:  s)',
#    mpf( '1' )  : 'selenium-82 (half-life:  s)',
#    mpf( '1' )  : 'tellurium-130 (half-life:  s)',
#    mpf( '1' )  : 'barium-130 (half-life:  s)',
#    mpf( '1' )  : 'germanium-76 (half-life:  s)',
#    mpf( '1' )  : 'xenon-136 (half-life:  s)',
#    mpf( '1' )  : 'tellurium-128 (half-life:  s)',
#}


#//******************************************************************************
#//
#//  solidAngleTable
#//
#//  steradians : description
#//
#//  https://en.wikipedia.org/wiki/Solid_angle
#//
#//******************************************************************************

solidAngleTable = {
    mpf( '6.67e-5' )    : 'the solid angle of the Moon as seen from Earth',
    mpf( '6.87e-5' )    : 'the solid angle of the Sun as seen from Earth',
}


#//******************************************************************************
#//
#//  temperatureTable
#//
#//  kelvins : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28temperature%29
#//
#//******************************************************************************

temperatureTable = {
    mpf( '1.0e-10' )        : 'the lowest temperature ever produced in a laboratory',
    mpf( '5.0e-8' )         : 'the Fermi temperature of potassium-40',
    mpf( '1.0e-6' )         : 'the temperature produced by nuclear demagnetrization refrigeration',
    mpf( '1.7e-3' )         : 'the temperature record for helium-3/helium-4 dliution refrigeration',
    mpf( '9.5e-1' )         : 'the melting point of helium',
    mpf( '2.725' )          : 'the temperature of the cosmic microwave background',
    mpf( '14.01' )          : 'the melting point of hydrogen',
    mpf( '44' )             : 'the mean temperature on Pluto',
    mpf( '183.9' )          : 'the coldest air recorded on Earth (Vostok Station, Antarctica)',
    mpf( '210' )            : 'the mean temperature on Mars',
    mpf( '234.3' )          : 'the melting point of mercury',
    mpf( '273.15' )         : 'the melting point of water',
    mpf( '287' )            : 'the mean temperature of Earth',
    mpf( '330' )            : 'the average body temperature for a human',
    mpf( '319.3' )          : 'the hottest temperature recorded on Earth (Death Valley)',
    mpf( '373.15' )         : 'the boiling point of water',
    mpf( '450' )            : 'the mean temperature on Mercury',
    mpf( '600.65' )         : 'the melting point of lead',
    mpf( '740' )            : 'the mean temperature on Venus',
    mpf( '933.47' )         : 'the melting point of aluminum',
    mpf( '1170' )           : 'the temperature of a wood fire',
    mpf( '1811' )           : 'the melting point of iron',
    mpf( '2022' )           : 'the boiling point of lead',
    mpf( '3683' )           : 'the melting point of tungsten',
    mpf( '5780' )           : 'the surface temperature of the Sun',
    mpf( '1.6e5' )          : 'the surface temperature of the hottest white dwarfs',
    mpf( '1.56e7' )         : 'the core temperature of the Sun',
    mpf( '2.3e7' )          : 'the temperature at which beryllium-7 can fuse',
    mpf( '2.3e8' )          : 'the temperature at which carbon-12 can fuse',
    mpf( '7.5e8' )          : 'the temperature at which oxygen can fuse',
    mpf( '1.0e10' )         : 'the temperature of a supernova',
    mpf( '7.0e11' )         : 'the temperature of a quasar\'s accretion disk',
    mpf( '6.7e13' )         : 'the temperature of gamma-ray burst from a collapsar',
    mpf( '2.8e15' )         : 'the temperature of an electroweak star',
    mpf( '1.0e21' )         : 'the temperature of dark matter in active galactic nuclei',
    mpf( '1.0e30' )         : 'the Hagedorn temperature, the highest possible temperature according to string theory',
    mpf( '1.416785e32' )    : 'the Planck temperature, at which the wavelength of black body radiation' +
                              'reaches the Planck length',
    mpf( '1.0e33' )         : 'the Landau pole, the maximum theoretical temperature according to QED',
}


#//******************************************************************************
#//
#//  timeTable
#//
#//  seconds : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28frequency%29
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28time%29
#//
#//******************************************************************************

timeTable = {
    mpf( '5.39106e-44' )    : 'the Planck time',
    mpf( '1.35135e-6' )     : 'the clock cycle of the Intel 4004 microprocessor (1971)',
    mpf( '60' )             : 'one minute (60 seconds)',
    mpf( '3600' )           : 'one hour (60 minutes)',
    mpf( '86400' )          : 'one day (24 hours)',
    mpf( '604800' )         : 'one week (7 days)',
    mpf( '2551442.8016' )   : 'the synodic lunar month',
    mpf( '3.15576e7' )      : 'one Julian year (365.25 days)',
    mpf( '3.15576e8' )      : 'one decade (10 years)',
    mpf( '3.15576e9' )      : 'one century (100 years)',
    mpf( '3.15576e10' )     : 'one millennium (1000 years)',
}


#//******************************************************************************
#//
#//  velocityTable
#//
#//  meters/second : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28speed%29
#//
#//******************************************************************************

velocityTable = {
    mpf( '2.2e-18' )    : 'the expansion rate between 2 points in free space 1 meter apart under Hubble\'s law',
    mpf( '3.0e-9' )     : 'the upper range of the typical relative speed of continental drift',
    mpf( '1.4e-5' )     : 'the growth rate of bamboo, the fastest-growing woody plant, over 24 hours',
    mpf( '0.00275' )    : 'the world record speed of the fastest snail',
    mpf( '0.080' )      : 'the top speed of a sloth',
    mpf( '30' )         : 'the typical speed of a car on the freeway',
    mpf( '130' )        : 'the wind speed of a powerful tornado',
    mpf( '250' )        : 'the typical cruising speed of a modern jet airliner',
    mpf( '343' )        : 'the speed of sound (in dry air at sea level at 20 degrees C)',
    mpf( '981' )        : 'the top speed of the SR-71 Blackbird',
    mpf( '3373' )       : 'the speed of the X-43 rocket/scramjet plane',
    mpf( '11107' )      : 'the speed of Apollo 10, the high speed record for a manned vehicle',
    mpf( '11200' )      : 'the escape velocity from Earth',
    mpf( '29800' )      : 'the speed of the Earth in orbit around the Sun',
    mpf( '2.0e5' )      : 'the orbital speed of the Solar System in the Milky Way galaxy',
    mpf( '5.52e5' )     : 'the speed of the Milky Way, relative to the cosmic microwave background',
    mpf( '1.4e7' )      : 'the typical speed of a fast neutron',
    mpf( '3.0e7' )      : 'the typical speed of an electron in a cathode ray tube',
}


#//******************************************************************************
#//
#//  volumeTable
#//
#//  liters : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28volume%29
#//
#//******************************************************************************

volumeTable = {
    mpf( '4.22419e-102' )   : 'the Planck volume',
    mpf( '9.4e-41' )        : 'the classical volume of an electron',
    mpf( '1.5e-38' )        : 'the volume of a proton',
    mpf( '6.54e-29' )       : 'the volume of a hydrogen atom',
    mpf( '9.0e-14' )        : 'the volume of a human red blood cell',
    mpf( '1.3e-10' )        : 'the volume of a very fine grain of sand',
    mpf( '6.2e-8' )         : 'the volume of a medium grain of sand',
    mpf( '4.0e-6' )         : 'the volume of a large grain of sand',
    mpf( '0.0049' )         : 'a teaspoon',
    mpf( '3.785' )          : 'a gallon',
    mpf( '1000' )           : 'the volume of a cubic meter',
    mpf( '11000' )          : 'the approximate volume of an elephant',
    mpf( '38500' )          : 'the volume of a 20-foot shipping container',
    mpf( '2.5e6' )          : 'the volume of an Olympic-sized swimming pool',
    mpf( '3.0e14' )         : 'the estimated volume of crude oil on Earth',
    mpf( '1.2232e16' )      : 'the volume of Lake Superior',
    mpf( '2.6e18' )         : 'the volume of Greenland ice cap',
    mpf( '1.4e21' )         : 'the volume of water in all of Earth\'s oceans',
    mpf( '1.08e24' )        : 'the volume of the Earth',
    mpf( '1.e27' )          : 'the volume of Jupiter',
    mpf( '1.e30' )          : 'the volume of the Sun',
    mpf( '2.75e38' )        : 'the volume of the star Betelgeuse',
    mpf( '3.3e64' )         : 'the volume of the Milky Way',
    mpf( '3.4e83' )         : 'the approxmimate volume of the observable universe',
}

