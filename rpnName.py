#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnName.py
# //
# //  RPN command-line calculator functions for converting integers to English names
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import *

from rpnMeasurement import Measurement


# //******************************************************************************
# //
# //  getModifiedOnesName
# //
# //******************************************************************************

def getModifiedOnesName( name, code ):
    if ( 'n' in code ) and ( ( name == 'septe' ) or ( name == 'nove' ) ):
        return name + 'n'
    elif ( 'm' in code ) and ( ( name == 'septe' ) or ( name == 'nove' ) ):
        return name + 'm'
    elif ( 's' in code ) and ( ( name == 'tre' ) or ( name == 'se' ) ):
        return name + 's'
    elif ( 'x' in code ):
        if ( name == 'tre' ):
            return name + 's'
        elif ( name == 'se' ):
            return name + 'x'
        else:
            return name
    else:
        return name


# //******************************************************************************
# //
# //  getSmallNumberName
# //
# //  Returns an english number name for anything from 0 to 999.
# //
# //******************************************************************************

def getSmallNumberName( n ):
    unitNumberNames = [ '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                        'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
                        'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
                        'nineteen' ]

    tensNumberNames = [ '', '', 'twenty', 'thirty', 'forty',
                        'fifty', 'sixty', 'seventy', 'eighty', 'ninety' ]

    hundreds = n // 100
    tens = ( n // 10 ) % 10
    ones = n % 10

    name = ''

    if hundreds > 0:
        name = unitNumberNames[ hundreds ] + ' hundred'

    if tens > 1:
        if name != '':
            name += ' '

        name += tensNumberNames[ tens ]

    if ones > 0:
        if tens > 1:
            name += '-'
            name += unitNumberNames[ ones ]
        elif tens == 1:
            if name != '':
                name += ' '

            name += unitNumberNames[ ones + 10 ]
        else:
            if name != '':
                name += ' '

            name += unitNumberNames[ ones ]
    elif tens == 1:
        if name != '':
            name += ' '

        name += unitNumberNames[ 10 ]

    return name


# //******************************************************************************
# //
# //  getNumberGroupName
# //
# //  returns the name of the "group", i.e., the three-digit group of an integer
# //  separated by commas in the usual notation.  Group 0 has no name because it
# //  represents the "ones".  Group 1 is "thousand", group 2 is "million", etc.
# //
# //******************************************************************************

def getNumberGroupName( n ):
    groupNames = [ '', 'thousand', 'million', 'billion', 'trillion',
                   'quadrillion', 'quintillion', 'sextillion', 'septillion',
                   'octillion', 'nonillion', 'decillion' ]

    onesNames = [ '', 'un', 'duo', 'tre', 'quattuor', 'quinqua', 'se', 'septe', 'octo', 'nove' ]

    tensNames = [ ( '', '' ), ( 'deci', 'n' ), ( 'viginti', 'ms' ), ( 'triginta', 'ns' ),
                  ( 'quadraginta', 'ns' ), ( 'quinquaginta', 'ns' ), ( 'sexaginta', 'n' ),
                  ( 'septuaginta', 'n' ), ( 'octoginta', 'mx' ), ( 'nonaginta', '' ) ]

    hundredsNames = [ ( '', '' ), ( 'centi', 'nx' ), ( 'ducenti', 'n' ), ( 'trecenti', 'ns' ),
                      ( 'quadringenti', 'ns' ), ( 'quingenti', 'ns' ), ( 'sescenti', 'n' ),
                      ( 'septingenti', 'n' ), ( 'octingenti', 'mx' ), ( 'nongenti', '' ) ]

    if n < len( groupNames ):
        return groupNames[ n ]
    else:
        n -= 1

        hundreds = n // 100
        tens = ( n // 10 ) % 10
        ones = n % 10

        name = ''
        hasTens = False

        if ones > 0:
            name += onesNames[ ones ]

        if tens > 0:
            hasTens = True

            if name != '':
                name = getModifiedOnesName( name, tensNames[ tens ][ 1 ] )

            name += tensNames[ tens ][ 0 ]

        if hundreds > 0:
            if not hasTens:
                name = getModifiedOnesName( name, hundredsNames[ hundreds ][ 1 ] )

            name += hundredsNames[ hundreds ][ 0 ]

        if name[ -1 ] in 'ai':
            name = name[ : -1 ]

        name += 'illion'

        return name


# //******************************************************************************
# //
# //  getNumberName
# //
# //******************************************************************************

def getNumberName( n ):
    if isinstance( n, Measurement ):
        n = mpf( n )

    if n == 0:
        return 'zero'

    current = fabs( n )

    if current >= power( 10, 3003 ):
        raise ValueError( 'value out of range for converting to an English name' )

    group = 0
    name = ''

    while current > 0:
        section = getSmallNumberName( int( fmod( current, 1000 ) ) )

        if section != '':
            groupName = getNumberGroupName( group )

            if groupName != '':
                section += ' ' + groupName

            if name == '':
                name = section
            else:
                name = section + ' ' + name

        current = floor( fdiv( current, 1000 ) )
        group += 1

    if n < 0:
        name = 'negative ' + name

    return name


