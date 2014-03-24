#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnEstimates.py
#//
#//  RPN command-line calculator, estimate table declarations
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

from mpmath import *

#// Can we stick this in somewhere?
#//
#// https://en.wikipedia.org/wiki/Orders_of_magnitude_%28density%29

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
    mpf( '0.0001454' )  : 'the angle a clock hour hand moves in a second',
    mpf( '0.0017453' )  : 'the angle a clock minute hand moves in a second',
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
    mpf( '7.0e-9' )     : 'the surface area of a human red blood cell',
    mpf( '7.1684e-9' )  : 'the area of a single pixel at 300 dpi resolution',
    mpf( '6.4516e-8' )  : 'the area of a single pixel at 100 dpi resolution',
    mpf( '1.9635e-7' )  : 'the cross-sectional area of a 0.5mm pencil lead',
    mpf( '2.9e-4' )     : 'the area of one side of a U.S. penny',
    mpf( '4.6e-3' )     : 'the area of the face of a credit card',
    mpf( '0.009677' )   : 'the area of a 3x5 inch index card',
    mpf( '0.06032246' ) : 'American letter size paper (8.5x11")',
    mpf( '1.73' )       : 'the average body surface area of a human',
    mpf( '261' )        : 'the size of a standard tennis court',
    mpf( '1250' )       : 'the surface area of an Olympic-size swimming pool',
    mpf( '4046.856' )   : 'one acre',
    mpf( '22074' )      : 'area of a Manhattan city block',
    mpf( '440000' )     : 'Vatican City',
    mpf( '2589988.11' ) : 'one square mile',
    mpf( '5.95e7' )     : 'the surface area of Manhattan Island',
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
    mpf( '2.0e-15' )    : 'gate capacitance of a MOS transistor, per micron of gate width',
    mpf( '3.0e-14' )    : 'DRAM cell',
    mpf( '1.0e-13' )    : 'small ceramic capacitor (100 fF)',
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

dataRateTable = {
}


#//******************************************************************************
#//
#//  electricalConductanceTable
#//
#//  mhos : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28resistance%29
#//******************************************************************************


electricalConductanceTable = {
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
}


#//******************************************************************************
#//
#//  electricalPotentialTable
#//
#//  volts : description
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28voltage%29
#//
#//******************************************************************************

electricPotentialTable = {
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
    mpf( '1.0e-4' )     : 'starlight on an overcast, moonless night sky',
    mpf( '1.4e-4' )     : 'Venus at its brightest',
    mpf( '2.0e-4' )     : 'starlight on a clear, moonless night sky, excluding airglow',
    mpf( '2.0e-3' )     : 'starlight on a clear, moonless night sky, including airglow',
    mpf( '1.0e-2' )     : 'the quarter Moon',
    mpf( '2.5e-2' )     : 'the full Moon on a clear night',
    mpf( '1' )          : 'the extreme of darkest storm clouds at sunset/sunrise',
    mpf( '40' )         : 'a fully overcast sky at sunset/sunrise',
    mpf( '200' )        : 'the extreme of darkest storm clouds at midday',
    mpf( '400' )        : 'sunrise or sunset on a clear day',
    mpf( '25000' )      : 'typical overcast day at midday',
    mpf( '120000' )     : 'the brightest sunlight',
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
    mpf( '1.0e-9' )     : 'a thin film chip inductor, 1.6x0.8 mm with a typical power rating of 0.1 W (range: 1-100 nH)',
    mpf( '5.25e-7' )    : 'the inductance of one meter of Cat-5 cable pair',
    mpf( '5.0e-5' )     : 'a coil with 99 turns, 0.635 cm long with a diameter of 0.635 cm',
    mpf( '1.0e-3' )     : 'a coil 2.2 cm long with a diameter of 1.6 cm with 800 mA capability, used in kW amplifiers',
    mpf( '1.0' )        : 'an inductor a few cm long and a few cm in diameter with many turns of wire on a ferrite core',
    mpf( '11' )         : 'a mains electricity transformer primary at 120 V (range: 8-11 H)',
    mpf( '1.326e3' )    : '500 kV, 3000 MW power line transformer primary winding',
}


#//******************************************************************************
#//
#//  informationEntropyTable
#//
#//  bits : description
#//
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28data%29
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28entropy%29
#//
#//******************************************************************************

informationEntropyTable = {
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
    mpf( '1.78' )       : 'the height of a typical adult male human',
    mpf( '91.44' )      : 'the length of a football field',
    mpf( '42194.988' )  : 'a marathon',
    mpf( '3983126.34' ) : 'the distance from New York to Los Angeles',
    mpf( '12756272' )   : 'the diameter of the Earth',
    mpf( '142984000' )  : 'the diameter of Jupiter',
    mpf( '1391980000' ) : 'the diameter of the Sun',
    mpf( '1.49598e11' ) : 'the distance from the Earth to the Sun',
    mpf( '4.01135e16' ) : 'the distance to the closest star, Proxima Centauri',
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
    mpf( '0.025' )      : 'the light of a firefly',
    mpf( '12.57' )      : 'the light of a candle',
    mpf( '780' )        : 'a 60 W incandescent light bulb',
    mpf( '930' )        : 'a 75 W incandescent light bulb',
    mpf( '2990' )       : 'a 200 W incandescent light bulb',
    mpf( '6.0e5' )      : 'an IMAX projector bulb',
    mpf( '4.23e10' )    : 'the Luxor Sky Beam spotlight array in Las Vegas',
    mpf( '4.6e24' )     : 'the dimmest class of red dwarf star',
    mpf( '3.0768e28' )  : 'the Sun',
    mpf( '1.382e38' )   : 'a Type 1a supernova',
    mpf( '1.26e41' )    : 'Quasar 3C 273',
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
    mpf( '5e-18' )      : 'the precision attained for Gravity Probe B',
    mpf( '3.1869e-5' )  : 'the Earth\'s magnetic field at 0 degrees long., 0 degrees lat.',
    mpf( '5.0e-3' )     : 'a typical refrigerator magnet',
    mpf( '0.3' )        : 'the strength of solar sunspots',
    mpf( '3' )          : 'the maximum strength of a common magnetic resonance imaging system',
    mpf( '16' )         : 'a magnetic field strong enough to levitate a frog',
    mpf( '2800' )       : 'the largest magnetic field produced in a laboratory',
    mpf( '1.0e8' )      : 'the lower range for the magnetic field strength in a magnetar',
    mpf( '1.0e11' )     : 'the upper range for the magnetic field strength in a magnetar',
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
    mpf( '0.003' )      : 'an average ant',
    mpf( '17.5' )       : 'a typical mouse',
    mpf( '7.0e4' )      : 'an average human',
    mpf( '5.5e6' )      : 'an average male African bush elephant',
    mpf( '4.39985e8' )  : 'the takeoff weight of a Boeing 747-8',
    mpf( '5.9742e27' )  : 'the Earth',
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
}


#//******************************************************************************
#//
#//  radiationAbsorbedDoseTable
#//
#//  grays : description
#//
#//******************************************************************************

radiationAbsorbedDoseTable = {
}


#//******************************************************************************
#//
#//  radiationEquivalentDoseTable
#//
#//  sieverts : description
#//
#//  https://en.wikipedia.org/wiki/Sievert
#//  https://en.wikipedia.org/wiki/Orders_of_magnitude_%28radiation%29
#//
#//******************************************************************************

radiationEquivalentDoseTable = {
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

radioactivityTable = {
}


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
    mpf( '1e-10' )          : 'the lowest temperature ever produced in a laboratory',
    mpf( '5e-8' )           : 'the Fermi temperature of potassium-40',
    mpf( '1e-6' )           : 'the temperature produced by nuclear demagnetrization refrigeration',
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
    mpf( '1.416785e32' )    : 'the Planck temperature, at which the wavelength of black body radiation' + \
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
    mpf( '9e-14' )          : 'the volume of a human red blood cell',
    mpf( '1.3e-10' )        : 'the volume of a very fine grain of sand',
    mpf( '6.2e-8' )         : 'the volume of a medium grain of sand',
    mpf( '4.0e-6' )         : 'the volume of a large grain of sand',
    mpf( '0.0049' )         : 'a teaspoon',
    mpf( '3.785' )          : 'a gallon',
    mpf( '1000' )           : 'a cubic meter',
    mpf( '11000' )          : 'the approximate volume of an elephant',
    mpf( '38500' )          : 'a 20-foot shipping container',
    mpf( '2.5e6' )          : 'an Olympic-sized swimming pool',
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

