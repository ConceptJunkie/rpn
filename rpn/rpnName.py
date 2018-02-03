#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnName.py
# //
# //  RPN command-line calculator functions for converting integers to English names
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import fabs, fdiv, floor, fmod, mpf, power

from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnUtils import oneArgFunctionEvaluator, real_int


# //******************************************************************************
# //
# //  getModifiedOnesName
# //
# //******************************************************************************

def getModifiedOnesName( name, code ):
    if ( 'n' in code ) and ( name in [ 'septe', 'nove' ] ):
        return name + 'n'
    elif ( 'm' in code ) and ( name in [ 'septe', 'nove' ] ):
        return name + 'm'
    elif ( 's' in code ) and ( name in [ 'tre', 'se' ] ):
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

def getSmallNumberName( n, ordinal = False ):
    unitNumberNames = \
        [ '', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
          'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
          'sixteen', 'seventeen', 'eighteen', 'nineteen' ]

    unitOrdinalNumberNames = \
        [ '', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh',
          'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth',
          'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth',
          'nineteenth' ]

    tensNumberNames = \
        [ '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
          'eighty', 'ninety' ]

    tensOrdinalNumberNames = \
        [ '', '', 'twentieth', 'thirtieth', 'fortieth',
          'fiftieth', 'sixtieth', 'seventieth', 'eightieth', 'ninetieth' ]

    hundreds = n // 100
    tens = ( n // 10 ) % 10
    ones = n % 10

    name = ''

    if hundreds > 0:
        name = unitNumberNames[ hundreds ] + ' hundred'

        if ordinal and tens == 0 and ones == 0:
            name += 'th'

    if tens > 1:
        if name != '':
            name += ' '

        if ordinal and ones == 0:
            name += tensOrdinalNumberNames[ tens ]
        else:
            name += tensNumberNames[ tens ]

    if ones > 0:
        if tens > 1:
            name += '-'

            if ordinal:
                name += unitOrdinalNumberNames[ ones ]
            else:
                name += unitNumberNames[ ones ]
        elif tens == 1:
            if name != '':
                name += ' '

            if ordinal:
                name += unitOrdinalNumberNames[ ones + 10 ]
            else:
                name += unitNumberNames[ ones + 10 ]
        else:
            if name != '':
                name += ' '

            if ordinal:
                name += unitOrdinalNumberNames[ ones ]
            else:
                name += unitNumberNames[ ones ]
    elif tens == 1:
        if name != '':
            name += ' '

        if ordinal:
            name += unitOrdinalNumberNames[ 10 ]
        else:
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
# //  getOrdinalName
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getOrdinalName( n ):
    return getNumberName( real_int( n ), ordinal = True )


# //******************************************************************************
# //
# //  getNumberName
# //
# //******************************************************************************

def getNumberName( n, ordinal = False ):
    units = ''

    if isinstance( n, RPNMeasurement ):
        value = n.getValue( )

        if value == 1 or value == -1:
            units = n.getUnitName( )
        else:
            units = n.getPluralUnitName( )

        n = real_int( value )

    if n == 0:
        if ordinal:
            name = 'zeroth'
        else:
            name = 'zero'

        if units:
            name += ' '
            name += units

        return name

    current = fabs( n )

    if current >= power( 10, 3003 ):
        raise ValueError( 'value out of range for converting to an English name' )

    group = 0
    name = ''

    firstTime = True

    while current > 0:
        section = getSmallNumberName( int( fmod( current, 1000 ) ), ordinal if firstTime else False )

        firstTime = False

        if section != '':
            groupName = getNumberGroupName( group )

            if groupName != '':
                section += ' ' + groupName

                if ordinal and name == '':
                    section += 'th'

            if name == '':
                name = section
            else:
                name = section + ' ' + name

        current = floor( fdiv( current, 1000 ) )
        group += 1

    if n < 0:
        name = 'negative ' + name

    if units:
        name += ' '
        name += units

    return name


@oneArgFunctionEvaluator( )
def getName( n ):
    return getNumberName( n )

