#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUnitTypes.py
# //
# //  RPN command-line calculator unit type declarations
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from rpn.rpnEstimates import *
from rpn.rpnUnitClasses import RPNUnitTypeInfo


# https://en.wikipedia.org/wiki/Radiant_exposure#SI_radiometry_units

# https://en.wikipedia.org/wiki/List_of_physical_quantities

expandedUnitTypes = {
    'abseleration'          : ( 'length*time^3',        'meter*second^3' ),
    'absement'              : ( 'length*time',          'meter*second' ),
    'abserk'                : ( 'length*time^4',        'meter*second^4' ),
    'absity'                : ( 'length*time^2',        'meter*second^2' ),
    'absock'                : ( 'length*time^8',        'meter*second^8' ),
    'absorbed_dose_rate'    : ( 'length^2/time^3',      'meter^2*second^3' ),
    'absop'                 : ( 'length*time^7',        'meter*second^7' ),
    'absounce'              : ( 'length*time^5',        'meter*second^5' ),
    'absrackle'             : ( 'length*time^6',        'meter*second^6' ),
    'absrop'                : ( 'length*time^9',        'meter*second^9' ),
    'acceleration'          : ( 'length/time^2',        'meter*second^2' ),
    'angular_acceleration'  : ( '1/time^2'              'radian/second^2' ),
}


# //******************************************************************************
# //
# //  basicUnitTypes
# //
# //  dimension:
# //      length, mass, time, charge, temperature, angle, electric_potential
# //      information_entropy, luminous_intensity
# //
# //  baseUnit:  The standard or customary unit of measurement for this unit
# //      type
# //
# //  estimateTable : The table of estimates, expressed in terms of the base
# //      unit, used for the 'estimate' operator.
# //
# //  Constant is not a 'real' unit type, but it is useful for it to act like
# //  one because it makes for useful operators, e.g. "20 M" for "20,000,000'.
# //
# //  https://en.wikipedia.org/wiki/SI_electromagnetism_units
# //
# //
# //******************************************************************************

basicUnitTypes = {
    '_null_type' : RPNUnitTypeInfo(
        'constant',
        '_null_unit',
        '_null_unit',
        None
    ),

    'acceleration' : RPNUnitTypeInfo(
        'length/time^2',
        'meter/second^2',
        'meter/second^2',
        accelerationTable
    ),

    'amount_of_substance' : RPNUnitTypeInfo(
        'amount_of_substance',
        'mole',
        'mole',
        amountOfSubstanceTable
    ),

    'angle' : RPNUnitTypeInfo(
        'angle',
        'radian',
        'radian',
        angleTable
    ),

    'area' : RPNUnitTypeInfo(
        'length^2',
        'meter^2',
        'meter^2',
        areaTable,
    ),

    'capacitance' : RPNUnitTypeInfo(
        'current^2*time^4/mass*length^2',
        'farad',
        'ampere^2*second^4*/kilogram*meter^2',
        capacitanceTable,
    ),

    'catalysis' : RPNUnitTypeInfo(
        'amount_of_substance/time',
        'katal',
        'mole/second',
        catalysisTable,
    ),

    'charge' : RPNUnitTypeInfo(
        'current*time',
        'coulomb',
        'ampere*second',
        chargeTable,
    ),

    'constant' : RPNUnitTypeInfo(
        'constant',
        'unity',
        'unity',
        constantTable,
    ),

    'current' : RPNUnitTypeInfo(
        'current',
        'ampere',
        'ampere',
        currentTable,
    ),

    'data_rate' : RPNUnitTypeInfo(
        'mass*length^2/time^3*temperature',
        'bit/second',
        'bit/second',
        dataRateTable,
    ),

    'density' : RPNUnitTypeInfo(
        'mass/length^3',
        'kilogram/liter',
        'kilogram/liter',
        densityTable,
    ),

    'dynamic_viscosity' : RPNUnitTypeInfo(
        'mass/length*time',
        'pascal*second',
        'kilogram/meter*second',
        dynamicViscosityTable,
    ),

    'electrical_conductance' : RPNUnitTypeInfo(
        'current^2*time^3/length^2*mass',
        'siemens',
        'ampere^2*second^3/kilogram*meter^2',
        electricalConductanceTable,
    ),

    'electrical_resistance' : RPNUnitTypeInfo(
        'length^2*mass/current^2*time^3',
        'ohm',
        'kilogram*meter^2/ampere^2*second^3',
        electricalResistanceTable,
    ),

    'electric_potential' : RPNUnitTypeInfo(
        'mass*length^2/current*time^3',
        'volt',
        'kilogram*meter^2/ampere*second^3',
        electricPotentialTable,
    ),

    'energy' : RPNUnitTypeInfo(
        'mass*length^2/time^2',
        'joule',
        'kilogram*meter^2/second^2',
        energyTable,
    ),

    'force' : RPNUnitTypeInfo(
        'mass*length/time^2',
        'newton',
        'kilogram*meter/second^2',
        forceTable,
    ),

    'frequency' : RPNUnitTypeInfo(
        '1/time',
        'hertz',
        '1/second',
        frequencyTable,
    ),

    'illuminance' : RPNUnitTypeInfo(
        'luminous_intensity*angle^2/length^2',
        'lux',
        'candela*radian^2/meter^2',
        illuminanceTable,
    ),

    'inductance' : RPNUnitTypeInfo(
        'mass*length^2/time^2*current^2',
        'henry',
        'kilogram*meter^2/ampere^2*second^2',
        inductanceTable,
    ),

    'information_entropy' : RPNUnitTypeInfo(
        'mass*length^2/time^2*temperature',
        'bit',
        'kilogram*meter^2/second^2*kelvin',
        informationEntropyTable,
    ),

    'jerk' : RPNUnitTypeInfo(
        'length/time^3',
        'meter/second^3',
        'meter/second^3',
        jerkTable
    ),

    'jounce' : RPNUnitTypeInfo(
        'length/time^4',
        'meter/second^4',
        'meter/second^4',
        jounceTable
    ),

    'length' : RPNUnitTypeInfo(
        'length',
        'meter',
        'meter',
        lengthTable,
    ),

    'luminance' : RPNUnitTypeInfo(
        'luminous_intensity/length^2',
        'candela/meter^2',
        'candela/meter^2',
        luminanceTable,
    ),

    'luminous_flux' : RPNUnitTypeInfo(
        'luminous_intensity*angle^2',
        'lumen',
        'candela*radian^2',
        luminousFluxTable,
    ),

    'luminous_intensity' : RPNUnitTypeInfo(
        'luminous_intensity',
        'candela',
        'candela',
        luminousIntensityTable,
    ),

    'magnetic_field_strength' : RPNUnitTypeInfo(
        'current/length',
        'ampere/meter',
        'ampere/meter',
        magneticFieldStrengthTable,
    ),

    'magnetic_flux' : RPNUnitTypeInfo(
        'mass*length^2/time^2*current',
        'weber',
        'kilogram*meter^2/ampere*second^2',
        magneticFluxTable,
    ),

    'magnetic_flux_density' : RPNUnitTypeInfo(
        'mass/time^2*current',
        'tesla',
        'kilogram/ampere*second^2',
        magneticFluxDensityTable,
    ),

    'mass' : RPNUnitTypeInfo(
        'mass',
        'kilogram',
        'kilogram',
        massTable,
    ),

    'power' : RPNUnitTypeInfo(
        'mass*length^2/time^3',
        'watt',
        'kilogram*meter^2/second^3',
        powerTable,
    ),

    'pressure' : RPNUnitTypeInfo(
        'mass/length*time^2',
        'pascal',
        'kilogram/meter*second^2',
        pressureTable,
    ),

    'radiation_dose' : RPNUnitTypeInfo(
        'length^2/time^2',
        'sievert',
        'meter^2/second^2',
        radiationDoseTable,
    ),

    'radiation_exposure' : RPNUnitTypeInfo(
        'current*time/mass',
        'coulomb/kilogram',
        'ampere*second/kilogram',
        radiationExposureTable,
    ),

    'radiosity' : RPNUnitTypeInfo(
        'mass/time^3',
        'watt/meter^2',
        'kilograms/second^3',
        radiosityTable,
    ),

    'solid_angle' : RPNUnitTypeInfo(
        'angle^2',
        'steradian',
        'radian^2',
        solidAngleTable,
    ),

    'temperature' : RPNUnitTypeInfo(
        'temperature',
        'kelvin',
        'kelvin',
        temperatureTable,
    ),

    'time' : RPNUnitTypeInfo(
        'time',
        'second',
        'second',
        timeTable,
    ),

    'velocity' : RPNUnitTypeInfo(
        'length/time',
        'meter/second',
        'meter/second',
        velocityTable,
    ),

    'volume' : RPNUnitTypeInfo(
        'length^3',
        'liter',
        'meter^3',
        volumeTable,
    ),
}

