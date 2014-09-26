#!/usr/bin/env python

# http://en.wikipedia.org/wiki/Physical_constant

# Things that don't work, but should:
#
#   This requires implicit conversion between unit types
#   rpn -D 16800 mA hours * 5 volts * joule convert
#

# http://pythonhosted.org//astral/#
# http://stackoverflow.com/questions/14698104/how-to-predict-tides-using-harmonic-constants
# http://rhodesmill.org/pyephem/quick.html
# https://github.com/geopy/geopy

# Here's another idea... when listing units, include the aliases

# https://en.wikipedia.org/wiki/Gas_constant
# https://en.wikipedia.org/wiki/Coulomb_constant

# Schwarzschild Radius - Hmmm... operators that turn one kind of unit into another (e.g., mass -> length)

# The Hubble Constant

# Time dilation
# c:\>rpn 1 0.9999 sqr - sqrt 1/x
# 70.7124459519


#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import arrow
import argparse
import calendar
import datetime
import struct
import sys
import time

from mpmath import *
from random import randrange

from rpnCombinatorics import *
from rpnComputer import *
from rpnConstants import *
from rpnDeclarations import *
from rpnList import *
from rpnMeasurement import *
from rpnModifiers import *
from rpnNumberTheory import *
from rpnOutput import *
from rpnPolynomials import *
from rpnPolytope import *
from rpnPrimeUtils import *
from rpnTime import *
from rpnUtils import *
from rpnVersion import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


#//******************************************************************************
#//
#//  add
#//
#//  We used to be able to call fadd directly, but now we want to be able to add
#//  units.  Adding units includes an implicit conversion if the units are not
#//  the same.
#//
#//******************************************************************************

def add( n, k ):
    if isinstance( n, arrow.Arrow ) and isinstance( k, Measurement ):
        return addTimes( n, k )
    elif isinstance( n, Measurement ) and isinstance( k, arrow.Arrow ):
        return addTimes( k, n )
    elif isinstance( n, Measurement ):
        return n.add( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).add( k )
    else:
        return fadd( n, k )


#//******************************************************************************
#//
#//  subtract
#//
#//  We used to be able to call fsub directly, but now we want to be able to
#//  subtract units and do the appropriate conversions.
#//
#//******************************************************************************

def subtract( n, k ):
    if isinstance( n, arrow.Arrow ):
        if isinstance( k, Measurement ):
            return subtractTimes( n, k )
        elif isinstance( k, arrow.Arrow ):
            if n > k:
                delta = n - k
                factor = 1
            else:
                delta = k - n
                factor = -1

            if delta.days != 0:
                result = Measurement( delta.days * factor, 'day' )
                result = result.add( Measurement( delta.seconds * factor, 'second' ) )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            elif delta.seconds != 0:
                result = Measurement( delta.seconds * factor, 'second' )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            else:
                result = Measurement( delta.microseconds * factor, 'microsecond' )

            return result
        else:
            raise ValueError( 'cannot subtract incompatible types' )
    elif isinstance( n, Measurement ):
        if isinstance( k, arrow.Arrow ):
            return subtractTimes( k, n )
        elif isinstance( k, Measurement ):
            return Measurement( n ).subtract( k )
        else:
            return n.subtract( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).subtract( k )
    else:
        return fsub( n, k )


#//******************************************************************************
#//
#//  getNegative
#//
#//******************************************************************************

def getNegative( n ):
    if isinstance( n, Measurement ):
        return Measurement( fneg( n.getValue( ) ), n.getUnits( ) )
    else:
        return fneg( n )


#//******************************************************************************
#//
#//  divide
#//
#//  We used to be able to call fdiv directly, but now we want to also divide
#//  the units.  Doing so lets us do all kinds of great stuff because now we
#//  can support compound units without having to explicitly declare them in
#//  makeUnits.py.
#//
#//******************************************************************************

def divide( n, k ):
    if isinstance( n, Measurement ):
        return n.divide( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).divide( k )
    else:
        return fdiv( n, k )


#//******************************************************************************
#//
#//  multiply
#//
#//  We used to be able to call fmul directly, but now we want to also multiply
#//  the units.  This allows compound units and the conversion routines try to
#//  be smart enough to deal with this.  There are scenarios in which it doesn't
#//  work, like converting parsec*barn to cubic_inch.  However, that can be done
#//  by converting parsec to inches and barn to square_inch separately and
#//  multiplying the result.
#//
#//******************************************************************************

def multiply( n, k ):
    if isinstance( n, Measurement ):
        return n.multiply( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).multiply( k )
    else:
        return fmul( n, k )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( n, k ):
    if isinstance( n, Measurement ):
        return n.exponentiate( k )
    elif isinstance( k, Measurement ):
        raise ValueError( 'a measurement cannot be exponentiated (yet)' )
    else:
        return power( n, k )


#//******************************************************************************
#//
#//  takeReciprocal
#//
#//  We used to be able to call fdiv directly, but now we want to handle
#//  Measurements.
#//
#//******************************************************************************

def takeReciprocal( n ):
    if isinstance( n, Measurement ):
        return n.invert( )
    else:
        return fdiv( 1, n )


#//******************************************************************************
#//
#//  performTrigOperation
#//
#//******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, Measurement ):
        value = mpf( i.convertValue( Measurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )


#//******************************************************************************
#//
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  getRegularPolygonArea
#//
#//  based on having sides of unit length
#//
#//  http://www.mathopenref.com/polygonregulararea.html
#//
#//******************************************************************************

def getRegularPolygonArea( n ):
    if n < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( n, fmul( 4, tan( fdiv( pi, n ) ) ) )


#//******************************************************************************
#//
#//  getNSphereRadius
#//
#//  k needs to be a Measurement so getNSphereRadius can tell if it's an area
#//  or a volume and use the correct formula.
#//
#//******************************************************************************

def getNSphereRadius( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return Measurement( k, 'inch' )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return k
    elif measurementType == { 'area' : 1 }:
        return fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                           fmul( n, power( pi, fdiv( n, 2 ) ) ) ),
                     root( k, fsub( n, 1 ) ) )
    elif measurementType == { 'volume' : 1 }:
        return root( fmul( fdiv( gamma( fadd( fdiv( n, 2 ), 1 ) ),
                                 power( pi, fdiv( n, 2 ) ) ), k ), 3 )
    else:
        raise ValueError( 'incompatible measurement type for computing the radius: ' + measurementType )


#//******************************************************************************
#//
#//  getNSphereSurfaceArea
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is a volume
#//  then it is taken to be the volume.  If it is an area, then it is returned
#//  unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereSurfaceArea( n, k ):
    if not isinstance( k, Measurement ):
        return getNSphereSurfaceArea( n, Measurement( k, 'inch' ) )

    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( fmul( n, power( pi, fdiv( n, 2 ) ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, fsub( n, 1 ) ) )
    elif measurementType == { 'area' : 1 }:
        return k
    elif measurementType == { 'volume' : 1 }:
        return 3    # TODO: formula for converting volume to surface area
    else:
        raise ValueError( 'incompatible measurement type for computing the surface area' )


#//******************************************************************************
#//
#//  getNSphereVolume
#//
#//  https://en.wikipedia.org/wiki/N-sphere#Volume_and_surface_area
#//
#//  n dimensions, k measurement
#//
#//  If k is a length, then it is taken to be the radius.  If it is an area
#//  then it is taken to be the surface area.  If it is a volume, then it is
#//  returned unchanged.  Other measurement types cause an exception.
#//
#//******************************************************************************

def getNSphereVolume( n, k ):
    if n < 3:
        raise ValueError( 'the number of dimensions must be at least 3' )

    if not isinstance( k, Measurement ):
        return getNSphereVolume( n, Measurement( k, 'inch' ) )

    measurementType = k.getTypes( )

    if measurementType == { 'length' : 1 }:
        return fmul( fdiv( power( pi, fdiv( n, 2 ) ),
                           gamma( fadd( fdiv( n, 2 ), 1 ) ) ), power( k, n ) )
    elif measurementType == { 'area' : 1 }:
        return 2   # TODO: formula for converting surface area to volume
    elif measurementType == { 'volume' : 1 }:
        return k
    else:
        raise ValueError( 'incompatible measurement type for computing the volume' )


#//******************************************************************************
#//
#//  getTriangleArea
#//
#//  https://en.wikipedia.org/wiki/Equilateral_triangle#Area
#//
#//******************************************************************************

def getTriangleArea( a, b, c ):
    return fdiv( fsum( [ power( a, 2 ), power( b, 2 ), power( c, 2 ) ] ), fmul( 4, sqrt( 3 ) ) )


#//******************************************************************************
#//
#//  getPrimorial
#//
#//******************************************************************************

def getPrimorial( n ):
    result = 2

    for i in arange( 1, n ):
        result = fmul( result, getNthPrime( i + 1 ) )

    return result


#//******************************************************************************
#//
#//  makeImaginary
#//
#//******************************************************************************

def makeImaginary( n ):
    return mpc( real='0.0', imag=n )


#//******************************************************************************
#//
#//  isSquare
#//
#//******************************************************************************

def isSquare( n ):
    sqrtN = sqrt( n )

    return 1 if sqrtN == floor( sqrtN ) else 0


#//******************************************************************************
#//
#//  getModifiedOnesName
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getSmallNumberName
#//
#//  Returns an english number name for anything from 0 to 999.
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  getNumberGroupName
#//
#//  returns the name of the "group", i.e., the three-digit group of an integer
#//  separated by commas in the usual notation.  Group 0 has no name because it
#//  represents the "ones".  Group 1 is "thousand", group 2 is "million", etc.
#//
#//******************************************************************************

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
        special = False

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


#//******************************************************************************
#//
#//  getNumberName
#//
#//******************************************************************************

def getNumberName( n ):
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


#//******************************************************************************
#//
#//  dumpOperators
#//
#//******************************************************************************

def dumpOperators( ):
    print( 'operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )

    print( )

    print( 'list operators:' )

    for i in sorted( [ key for key in listOperators ] ):
        print( '   ' + i )

    print( )

    print( 'modifer operators:' )

    for i in sorted( [ key for key in modifiers ] ):
        print( '   ' + i )

    print( )
    print( 'internal operators:' )

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )

    print( )


    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  dumpAliases
#//
#//******************************************************************************

def dumpAliases( ):
    for alias in sorted( [ key for key in operatorAliases ] ):
        print( alias, operatorAliases[ alias ] )

    return len( operatorAliases )


#//******************************************************************************
#//
#//  printStats
#//
#//******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:13,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


#//******************************************************************************
#//
#//  dumpStats
#//
#//******************************************************************************

def dumpStats( ):
    if g.unitConversionMatrix is None:
        loadUnitConversionMatrix( )

    print( '{:10,} unique operators'.format( len( listOperators ) + len( operators ) + len( modifiers ) ) )
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    printStats( loadSmallPrimes( g.dataPath ), 'small primes' )
    printStats( loadLargePrimes( g.dataPath ), 'large primes' )
    printStats( loadIsolatedPrimes( g.dataPath ), 'isolated primes' )
    printStats( loadTwinPrimes( g.dataPath ), 'twin primes' )
    printStats( loadBalancedPrimes( g.dataPath ), 'balanced primes' )
    printStats( loadDoubleBalancedPrimes( g.dataPath ), 'double balanced primes' )
    printStats( loadTripleBalancedPrimes( g.dataPath ), 'triple balanced primes' )
    printStats( loadSophiePrimes( g.dataPath ), 'Sophie Germain primes' )
    printStats( loadCousinPrimes( g.dataPath ), 'cousin primes' )
    printStats( loadSexyPrimes( g.dataPath ), 'sexy primes' )
    printStats( loadTripletPrimes( g.dataPath ), 'triplet primes' )
    printStats( loadSexyTripletPrimes( g.dataPath ), 'sexy triplet primes' )
    printStats( loadQuadrupletPrimes( g.dataPath ), 'quadruplet primes' )
    printStats( loadSexyQuadrupletPrimes( g.dataPath ), 'sexy quadruplet primes' )
    printStats( loadQuintupletPrimes( g.dataPath ), 'quintuplet primes' )
    printStats( loadSextupletPrimes( g.dataPath ), 'sextuplet primes' )

    print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#//******************************************************************************
#//
#//  loadResult
#//
#//******************************************************************************

def loadResult( valueList ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'result.pckl.bz2', 'rb' ) ) as pickleFile:
            result = pickle.load( pickleFile )
    except FileNotFoundError:
        result = mapmathify( 0 )

    return result


#//******************************************************************************
#//
#//  saveResult
#//
#//******************************************************************************

def saveResult( result ):
    with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'result.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( result, pickleFile )


#//******************************************************************************
#//
#//  getPrimes
#//
#//******************************************************************************

def getPrimes( value, count ):
    result = list( )

    for i in getNthPrimeRange( value, count ):
        result.append( i )

    return result


#//******************************************************************************
#//
#//  getCurrentArgList
#//
#//******************************************************************************

def getCurrentArgList( valueList ):
    argList = valueList

    for i in range( 0, g.nestedListLevel ):
        argList = argList[ -1 ]

    return argList


#//******************************************************************************
#//
#//  estimate
#//
#//******************************************************************************

def estimate( measurement ):
    if isinstance( measurement, Measurement ):
        unitType = getUnitType( measurement.getUnitName( ) )
        unitTypeOutput = removeUnderscores( unitType )

        unitTypeInfo = g.basicUnitTypes[ unitType ]

        unit = Measurement( 1, { unitTypeInfo.baseUnit : 1 } )
        value = mpf( Measurement( measurement.convertValue( unit ), unit.getUnits( ) ) )

        if len( unitTypeInfo.estimateTable ) == 0:
            return 'No estimates are available for this unit type (' + unitTypeOutput + ').'

        matchingKeys = [ key for key in unitTypeInfo.estimateTable if key <= mpf( value ) ]

        if len( matchingKeys ) == 0:
            estimateKey = min( key for key in unitTypeInfo.estimateTable )

            multiple = fdiv( estimateKey, value )

            return 'approximately ' + nstr( multiple, 3 ) + ' times smaller than ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
        else:
            estimateKey = max( matchingKeys )

            multiple = fdiv( value, estimateKey )

            return 'approximately ' + nstr( multiple, 3 ) + ' times ' + \
                   unitTypeInfo.estimateTable[ estimateKey ]
    elif isinstance( measurement, arrow.Arrow ):
        return measurement.humanize( )
    else:
        raise TypeError( 'incompatible type for estimating' )


#//******************************************************************************
#//
#//  convertToDMS
#//
#//******************************************************************************

def convertToDMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'degree' : 1 } ), Measurement( 1, { 'arcminute' : 1 } ),
                              Measurement( 1, { 'arcsecond' : 1 } ) ] )


#//******************************************************************************
#//
#//  evaluateFunction
#//
#//  Evaluate a user-defined function.  This is the simplest operator to use
#//  user-defined functions.   Eventually I want to compile the user-defined
#//  function into Python code, so when I start passing them to mpmath they'll
#//  run faster.
#//
#//******************************************************************************

def evaluateFunction( n, k ):
    if not isinstance( k, FunctionInfo ):
        raise ValueError( '\'eval\' expects a function argument' )

    if isinstance( n, list ):
        result = [ ]

        for item in n:
            result.append( k.evaluate( item ) )

        return result
    else:
        valueList = [ ]

        for item in k.valueList:
            if item == 'x':
                valueList.append( n )
            else:
                valueList.append( item )

        index = 1

        while len( valueList ) > 1:
            term = valueList.pop( 0 )

            if term in operatorAliases:
                term = operatorAliases[ term ]

            if not evaluateTerm( term, index, valueList ):
                break

            index = index + 1

        return valueList[ 0 ]


#//******************************************************************************
#//
#//  evaluateSum
#//
#//  Calculate the sum of a user-defined function across a range.
#//
#//******************************************************************************

def evaluateSum( start, end, func ):
    return nsum( lambda n: evaluateFunction( n, func ), [ start, end ] )


#//******************************************************************************
#//
#//  evaluateProduct
#//
#//  Calculate the product of a user-defined function across a range.
#//
#//******************************************************************************

def evaluateProduct( start, end, func ):
    return nprod( lambda n: evaluateFunction( n, func ), [ start, end ] )


#//******************************************************************************
#//
#//  evaluateLimit
#//
#//  Calculate the limit of a user-defined function as the argument approaches
#//  x.
#//
#//******************************************************************************

def evaluateLimit( x, func ):
    return limit( lambda n: evaluateFunction( n, func ), x )


#//******************************************************************************
#//
#//  evaluateLimitNegative
#//
#//  Calculate the limit of a user-defined function as the argument approaches
#//  x.  This differs from evaluateLimit by approaching the limit from above.
#//
#//******************************************************************************

def evaluateLimitNegative( x, func ):
    return limit( lambda n: evaluateFunction( n, func ), x, direction=-1 )


#//******************************************************************************
#//
#//  functionOperators
#//
#//  This is just a list of operators that terminate the function creation
#//  state.
#//
#//******************************************************************************

functionOperators = [ 'eval', 'nsum', 'nprod', 'limit', 'limitn' ]


#//******************************************************************************
#//
#//  getValue
#//
#//  This function is used to turn a measurement into a regular number because
#//  most functions don't work on measurements.
#//
#//******************************************************************************

def getValue( n ):
    return mpf( n )


#//******************************************************************************
#//
#//  modifiers are operators that directly modify the argument stack instead of
#//  just returning a value.
#//
#//  '[' and ']' are special arguments that change global state in order to
#//  create list operands.
#//
#//******************************************************************************

modifiers = {
    'dup'               : OperatorInfo( duplicateTerm, 2 ),
    'flatten'           : OperatorInfo( flatten, 1 ),
    'previous'          : OperatorInfo( getPrevious, 1 ),
    'unlist'            : OperatorInfo( unlist, 1 ),
    'x'                 : OperatorInfo( createFunction, 0 ),
    '['                 : OperatorInfo( incrementNestedListLevel, 0 ),
    ']'                 : OperatorInfo( decrementNestedListLevel, 0 ),
}


#//******************************************************************************
#//
#//  listOperators are operators that handle whether or not an argument is a
#//  list themselves (because they require a list argument).  Unlike regular
#//  operators, we don't want listOperators permutated over each list element,
#//  and if we do for auxillary arguments, these operator handlers will do that
#//  themselves.
#//
#//******************************************************************************

listOperators = {
    'altsign'           : OperatorInfo( alternateSigns, 1 ),
    'altsign2'          : OperatorInfo( alternateSigns2, 1 ),
    'altsum'            : OperatorInfo( getAlternatingSum, 1 ),
    'altsum2'           : OperatorInfo( getAlternatingSum2, 1 ),
    'append'            : OperatorInfo( appendLists, 2 ),
    'base'              : OperatorInfo( interpretAsBase, 2 ),
    'calendar'          : OperatorInfo( generateMonthCalendar, 1 ),
    'cf'                : OperatorInfo( convertFromContinuedFraction, 1 ),
    'convert'           : OperatorInfo( convertUnits, 2 ),
    'count'             : OperatorInfo( countElements, 1 ),
    'diffs'             : OperatorInfo( getListDiffs, 1 ),
    'gcd'               : OperatorInfo( getGCD, 1 ),
    'interleave'        : OperatorInfo( interleave, 2 ),
    'intersection'      : OperatorInfo( makeIntersection, 2 ),
    'linearrecur'       : OperatorInfo( getNthLinearRecurrence, 3 ),
    'makeisotime'       : OperatorInfo( makeISOTime, 1 ),
    'makejuliantime'    : OperatorInfo( makeJulianTime, 1 ),
    'maketime'          : OperatorInfo( makeTime, 1 ),
    'max'               : OperatorInfo( max, 1 ),
    'maxindex'          : OperatorInfo( getIndexOfMax, 1 ),
    'mean'              : OperatorInfo( lambda n: fdiv( fsum( n ), len( n ) ), 1 ),
    'min'               : OperatorInfo( min, 1 ),
    'minindex'          : OperatorInfo( getIndexOfMin, 1 ),
    'nonzero'           : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e != 0 ], 1 ),
    'polyadd'           : OperatorInfo( addPolynomials, 2 ),
    'polymul'           : OperatorInfo( multiplyPolynomials, 2 ),
    'polyprod'          : OperatorInfo( multiplyListOfPolynomials, 1 ),
    'polysum'           : OperatorInfo( addListOfPolynomials, 1 ),
    'polyval'           : OperatorInfo( evaluatePolynomial, 2 ),
    'product'           : OperatorInfo( fprod, 1 ),
    'ratios'            : OperatorInfo( getListRatios, 1 ),
    'result'            : OperatorInfo( loadResult, 0 ),
    'reverse'           : OperatorInfo( getReverse, 1 ),
    'solve'             : OperatorInfo( solvePolynomial, 1 ),
    'sort'              : OperatorInfo( sortAscending, 1 ),
    'sortdesc'          : OperatorInfo( sortDescending, 1 ),
    'stddev'            : OperatorInfo( getStandardDeviation, 1 ),
    'sum'               : OperatorInfo( sum, 1 ),
    'tower'             : OperatorInfo( calculatePowerTower, 1 ),
    'tower2'            : OperatorInfo( calculatePowerTower2, 1 ),
    'union'             : OperatorInfo( makeUnion, 2 ),
    'unique'            : OperatorInfo( getUniqueElements, 1 ),
    'unpack'            : OperatorInfo( unpackInteger, 2 ),
    'zero'              : OperatorInfo( lambda n: [ index for index, e in enumerate( n ) if e == 0 ], 1 ),
}


#//******************************************************************************
#//
#//  operators
#//
#//  Regular operators expect zero or more single values and if those arguments
#//  are lists, rpn will iterate calls to the operator handler for each element
#//  in the list.   Multiple lists for arguments are not permutated.  Instead,
#//  the operator handler is called for each element in the first list, along
#//  with the nth element of each other argument that is also a list.
#//
#//******************************************************************************

operators = {
    'abs'               : OperatorInfo( fabs, 1 ),
    'acos'              : OperatorInfo( lambda n: performTrigOperation( n, acos ), 1 ),
    'acosh'             : OperatorInfo( lambda n: performTrigOperation( n, acosh ), 1 ),
    'acot'              : OperatorInfo( lambda n: performTrigOperation( n, acot ), 1 ),
    'acoth'             : OperatorInfo( lambda n: performTrigOperation( n, acoth ), 1 ),
    'acsc'              : OperatorInfo( lambda n: performTrigOperation( n, acsc ), 1 ),
    'acsch'             : OperatorInfo( lambda n: performTrigOperation( n, acsch ), 1 ),
    'add'               : OperatorInfo( add, 2, ),
    'altfac'            : OperatorInfo( getNthAlternatingFactorial, 1 ),
    'and'               : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x & y ), 2 ),
    'apery'             : OperatorInfo( apery, 0 ),
    'aperynum'          : OperatorInfo( getNthAperyNumber, 1 ),
    'april'             : OperatorInfo( lambda: 4, 0 ),
    'asec'              : OperatorInfo( lambda n: performTrigOperation( n, asec ), 1 ),
    'asech'             : OperatorInfo( lambda n: performTrigOperation( n, asech ), 1 ),
    'ash_wednesday'     : OperatorInfo( calculateAshWednesday, 1 ),
    'asin'              : OperatorInfo( lambda n: performTrigOperation( n, asin ), 1 ),
    'asinh'             : OperatorInfo( lambda n: performTrigOperation( n, asinh ), 1 ),
    'atan'              : OperatorInfo( lambda n: performTrigOperation( n, atan ), 1 ),
    'atanh'             : OperatorInfo( lambda n: performTrigOperation( n, atanh ), 1 ),
    'august'            : OperatorInfo( lambda: 8, 0 ),
    'avogadro'          : OperatorInfo( getAvogadrosNumber, 0 ),
    'balanced'          : OperatorInfo( getNthBalancedPrime, 1 ),
    'balanced_'         : OperatorInfo( getNthBalancedPrimeList, 1 ),
    'bell'              : OperatorInfo( bell, 1 ),
    'bellpoly'          : OperatorInfo( bell, 2 ),
    'bernoulli'         : OperatorInfo( bernoulli, 1 ),
    'binomial'          : OperatorInfo( binomial, 2 ),
    'carol'             : OperatorInfo( lambda n : fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 ), 1 ),
    'catalan'           : OperatorInfo( lambda n: fdiv( binomial( fmul( 2, n ), n ), fadd( n, 1 ) ), 1 ),
    'catalans'          : OperatorInfo( catalan, 0 ),
    'cdecagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 10 ), 1 ),
    'cdecagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 10 ), 1 ),
    'ceiling'           : OperatorInfo( ceil, 1 ),
    'centeredcube'      : OperatorInfo( getNthCenteredCubeNumber, 1 ),
    'champernowne'      : OperatorInfo( getChampernowneConstant, 0 ),
    'char'              : OperatorInfo( lambda n: convertToSignedInt( n , 8 ), 1 ),
    'cheptagonal'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 7 ), 1 ),
    'cheptagonal?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 7 ), 1 ),
    'chexagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 6 ), 1 ),
    'cnonagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 9 ), 1 ),
    'cnonagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 9 ), 1 ),
    'coctagonal'        : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 8 ), 1 ),
    'coctagonal?'       : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 8 ), 1 ),
    'copeland'          : OperatorInfo( getCopelandErdosConstant, 0 ),
    'cos'               : OperatorInfo( lambda n: performTrigOperation( n, cos ), 1 ),
    'cosh'              : OperatorInfo( lambda n: performTrigOperation( n, cosh ), 1 ),
    'cot'               : OperatorInfo( lambda n: performTrigOperation( n, cot ), 1 ),
    'coth'              : OperatorInfo( lambda n: performTrigOperation( n, coth ), 1 ),
    'countbits'         : OperatorInfo( getBitCount, 1 ),
    'countdiv'          : OperatorInfo( getDivisorCount, 1 ),
    'cousinprime'       : OperatorInfo( getNthCousinPrime, 1 ),
    'cpentagonal'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 5 ), 1 ),
    'cpentagonal?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 5 ), 1 ),
    'cpolygonal'        : OperatorInfo( lambda n, k: getCenteredPolygonalNumber( n, k ), 2 ),
    'cpolygonal?'       : OperatorInfo( lambda n, k: findCenteredPolygonalNumber( n, k ), 2 ),
    'csc'               : OperatorInfo( lambda n: performTrigOperation( n, csc ), 1 ),
    'csch'              : OperatorInfo( lambda n: performTrigOperation( n, csch ), 1 ),
    'csquare'           : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 4 ), 1 ),
    'csquare?'          : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 4 ), 1 ),
    'ctriangular'       : OperatorInfo( lambda n: getCenteredPolygonalNumber( n, 3 ), 1 ),
    'ctriangular?'      : OperatorInfo( lambda n: findCenteredPolygonalNumber( n, 3 ), 1 ),
    'cube'              : OperatorInfo( lambda n: exponentiate( n, 3 ), 1 ),
    'decagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 10 ), 1 ),
    'decagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 10 ), 1 ),
    'december'          : OperatorInfo( lambda: 12, 0 ),
    'delannoy'          : OperatorInfo( getNthDelannoyNumber, 1 ),
    'dhms'              : OperatorInfo( convertToDHMS, 1 ),
    'divide'            : OperatorInfo( divide, 2 ),
    'divisors'          : OperatorInfo( getDivisors, 1 ),
    'dms'               : OperatorInfo( convertToDMS, 1 ),
    'dodecahedral'      : OperatorInfo( lambda n : polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], n ), 1 ),
    'double'            : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'd', float( n ) ) ) ), 1 ),
    'doublebal'         : OperatorInfo( getNthDoubleBalancedPrime, 1 ),
    'doublebal_'        : OperatorInfo( getNthDoubleBalancedPrimeList, 1 ),
    'doublefac'         : OperatorInfo( fac2, 1 ),
    'dst_end'           : OperatorInfo( calculateDSTEnd, 1 ),
    'dst_start'         : OperatorInfo( calculateDSTStart, 1 ),
    'e'                 : OperatorInfo( e, 0 ),
    'easter'            : OperatorInfo( calculateEaster, 1 ),
    'egypt'             : OperatorInfo( getGreedyEgyptianFraction, 2 ),
    'election_day'      : OperatorInfo( calculateElectionDay, 1 ),
    'element'           : OperatorInfo( getListElement, 2 ),
    'estimate'          : OperatorInfo( estimate, 1 ),
    'euler'             : OperatorInfo( euler, 0 ),
    'eval'              : OperatorInfo( evaluateFunction, 2 ),
    'exp'               : OperatorInfo( exp, 1 ),
    'exp10'             : OperatorInfo( lambda n: power( 10, n ), 1 ),
    'expphi'            : OperatorInfo( lambda n: power( phi, n ), 1 ),
    'exprange'          : OperatorInfo( expandExponentialRange, 3 ),
    'factor'            : OperatorInfo( lambda i: getExpandedFactorList( factor( i ) ), 1 ),
    'factorial'         : OperatorInfo( fac, 1 ),
    'february'          : OperatorInfo( lambda: 2, 0 ),
    'fibonacci'         : OperatorInfo( fib, 1 ),
    'float'             : OperatorInfo( lambda n : fsum( b << 8 * i for i, b in enumerate( struct.pack( 'f', float( n ) ) ) ), 1 ),
    'floor'             : OperatorInfo( floor, 1 ),
    'fraction'          : OperatorInfo( interpretAsFraction, 2 ),
    'friday'            : OperatorInfo( lambda: 5, 0 ),
    'fromunixtime'      : OperatorInfo( lambda n: arrow.get( n ), 1 ),
    'gamma'             : OperatorInfo( gamma, 1 ),
    'georange'          : OperatorInfo( expandGeometricRange, 3 ),
    'glaisher'          : OperatorInfo( glaisher, 0 ),
    'harmonic'          : OperatorInfo( harmonic, 1 ),
    'heptagonal'        : OperatorInfo( lambda n: getNthPolygonalNumber( n, 7 ), 1 ),
    'heptagonal?'       : OperatorInfo( lambda n: findNthPolygonalNumber( n, 7 ), 1 ),
    'heptanacci'        : OperatorInfo( getNthHeptanacci, 1 ),
    'hepthex'           : OperatorInfo( getNthHeptagonalHexagonalNumber, 1 ),
    'heptpent'          : OperatorInfo( getNthHeptagonalPentagonalNumber, 1 ),
    'heptsquare'        : OperatorInfo( getNthHeptagonalSquareNumber, 1 ),
    'hepttri'           : OperatorInfo( getNthHeptagonalTriangularNumber, 1 ),
    'hexagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 6 ), 1 ),
    'hexagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 6 ), 1 ),
    'hexanacci'         : OperatorInfo( getNthHexanacci, 1 ),
    'hexpent'           : OperatorInfo( getNthHexagonalPentagonalNumber, 1 ),
    'hms'               : OperatorInfo( convertToHMS, 1 ),
    'hyper4_2'          : OperatorInfo( tetrateLarge, 2 ),
    'hyperfac'          : OperatorInfo( hyperfac, 1 ),
    'hypot'             : OperatorInfo( hypot, 2 ),
    'i'                 : OperatorInfo( makeImaginary, 1 ),
    'icosahedral'       : OperatorInfo( lambda n: polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], n ), 1 ),
    'infinity'          : OperatorInfo( lambda: inf, 0 ),
    'integer'           : OperatorInfo( convertToSignedInt, 2 ),
    'isdivisible'       : OperatorInfo( lambda i, n: 1 if fmod( i, n ) == 0 else 0, 2 ),
    'isolated'          : OperatorInfo( getNthIsolatedPrime, 1 ),
    'iso_day'           : OperatorInfo( getISODay, 1 ),
    'isprime'           : OperatorInfo( lambda n: 1 if isPrime( n ) else 0, 1 ),
    'issquare'          : OperatorInfo( isSquare, 1 ),
    'itoi'              : OperatorInfo( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'jacobsthal'        : OperatorInfo( getNthJacobsthalNumber, 1 ),
    'january'           : OperatorInfo( lambda: 1, 0 ),
    'julian_day'        : OperatorInfo( getJulianDay, 1 ),
    'july'              : OperatorInfo( lambda: 7, 0 ),
    'june'              : OperatorInfo( lambda: 6, 0 ),
    'khinchin'          : OperatorInfo( khinchin, 0 ),
    'kynea'             : OperatorInfo( lambda n : fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 ), 1 ),
    'labor_day'         : OperatorInfo( calculateLaborDay, 1 ),
    'lah'               : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), fac( fsub( n, 1 ) ) ), fac( fsub( k, 1 ) ) ), 2 ),
    'lambertw'          : OperatorInfo( lambertw, 1 ),
    'leyland'           : OperatorInfo( lambda x, y : fadd( power( x, y ), power( y, x ) ), 2 ),
    'lgamma'            : OperatorInfo( loggamma, 1 ),
    'li'                : OperatorInfo( li, 1 ),
    'limit'             : OperatorInfo( evaluateLimit, 2 ),
    'limitn'            : OperatorInfo( evaluateLimitNegative, 2 ),
    'ln'                : OperatorInfo( ln, 1 ),
    'log10'             : OperatorInfo( log10, 1 ),
    'log2'              : OperatorInfo( lambda n: log( n, 2 ), 1 ),
    'logxy'             : OperatorInfo( log, 2 ),
    'long'              : OperatorInfo( lambda n: convertToSignedInt( n , 32 ), 1 ),
    'longlong'          : OperatorInfo( lambda n: convertToSignedInt( n , 64 ), 1 ),
    'lucas'             : OperatorInfo( getNthLucasNumber, 1 ),
    'makecf'            : OperatorInfo( lambda n, k: ContinuedFraction( n, maxterms=k, cutoff=power( 10, -( mp.dps - 2 ) ) ), 2 ),
    'march'             : OperatorInfo( lambda: 3, 0 ),
    'maxchar'           : OperatorInfo( lambda: ( 1 << 7 ) - 1, 0 ),
    'maxlong'           : OperatorInfo( lambda: ( 1 << 31 ) - 1, 0 ),
    'maxlonglong'       : OperatorInfo( lambda: ( 1 << 63 ) - 1, 0 ),
    'maxquadlong'       : OperatorInfo( lambda: ( 1 << 127 ) - 1, 0 ),
    'maxshort'          : OperatorInfo( lambda: ( 1 << 15 ) - 1, 0 ),
    'maxuchar'          : OperatorInfo( lambda: ( 1 << 8 ) - 1, 0 ),
    'maxulong'          : OperatorInfo( lambda: ( 1 << 32 ) - 1, 0 ),
    'maxulonglong'      : OperatorInfo( lambda: ( 1 << 64 ) - 1, 0 ),
    'maxuquadlong'      : OperatorInfo( lambda: ( 1 << 128 ) - 1, 0 ),
    'maxushort'         : OperatorInfo( lambda: ( 1 << 16 ) - 1, 0 ),
    'may'               : OperatorInfo( lambda: 5, 0 ),
    'memorial_day'      : OperatorInfo( calculateMemorialDay, 1 ),
    'mertens'           : OperatorInfo( mertens, 0 ),
    'mills'             : OperatorInfo( getMillsConstant, 0 ),
    'minchar'           : OperatorInfo( lambda: -( 1 << 7 ), 0 ),
    'minlong'           : OperatorInfo( lambda: -( 1 << 31 ), 0 ),
    'minlonglong'       : OperatorInfo( lambda: -( 1 << 63 ), 0 ),
    'minquadlong'       : OperatorInfo( lambda: -( 1 << 127 ), 0 ),
    'minshort'          : OperatorInfo( lambda: -( 1 << 15 ), 0 ),
    'minuchar'          : OperatorInfo( lambda: 0, 0 ),
    'minulong'          : OperatorInfo( lambda: 0, 0 ),
    'minulonglong'      : OperatorInfo( lambda: 0, 0 ),
    'minuquadlong'      : OperatorInfo( lambda: 0, 0 ),
    'minushort'         : OperatorInfo( lambda: 0, 0 ),
    'modulo'            : OperatorInfo( fmod, 2 ),
    'monday'            : OperatorInfo( lambda: 1, 0 ),
    'motzkin'           : OperatorInfo( getNthMotzkinNumber, 1 ),
    'multiply'          : OperatorInfo( multiply, 2 ),
    'name'              : OperatorInfo( getNumberName, 1 ),
    'narayana'          : OperatorInfo( lambda n, k: fdiv( fmul( binomial( n, k ), binomial( n, fsub( k, 1 ) ) ), n ), 2 ),
    'negative'          : OperatorInfo( getNegative, 1 ),
    'negative_infinity' : OperatorInfo( lambda: -inf, 0 ),
    'nonagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 9 ), 1 ),
    'nonagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 9 ), 1 ),
    'nonahept'          : OperatorInfo( getNthNonagonalHeptagonalNumber, 1 ),
    'nonahex'           : OperatorInfo( getNthNonagonalHexagonalNumber, 1 ),
    'nonaoct'           : OperatorInfo( getNthNonagonalOctagonalNumber, 1 ),
    'nonapent'          : OperatorInfo( getNthNonagonalPentagonalNumber, 1 ),
    'nonasquare'        : OperatorInfo( getNthNonagonalSquareNumber, 1 ),
    'nonatri'           : OperatorInfo( getNthNonagonalTriangularNumber, 1 ),
    'not'               : OperatorInfo( getInvertedBits, 1 ),
    'november'          : OperatorInfo( lambda: 11, 0 ),
    'now'               : OperatorInfo( getNow, 0 ),
    'nprod'             : OperatorInfo( evaluateProduct, 3 ),
    'nspherearea'       : OperatorInfo( getNSphereSurfaceArea, 2 ),
    'nsphereradius'     : OperatorInfo( getNSphereRadius, 2 ),
    'nspherevolume'     : OperatorInfo( getNSphereVolume, 2 ),
    'nsum'              : OperatorInfo( evaluateSum, 3 ),
    'nthprime?'         : OperatorInfo( lambda i: findPrime( i )[ 0 ], 1 ),
    'nthquad?'          : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 0 ], 1 ),
    'nthweekday'        : OperatorInfo( calculateNthWeekdayOfMonth , 4 ),
    'nthweekdayofyear'  : OperatorInfo( calculateNthWeekdayOfYear, 3 ),
    'octagonal'         : OperatorInfo( lambda n: getNthPolygonalNumber( n, 8 ), 1 ),
    'octagonal?'        : OperatorInfo( lambda n: findNthPolygonalNumber( n, 8 ), 1 ),
    'octahedral'        : OperatorInfo( lambda n: polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], n ), 1 ),
    'octhept'           : OperatorInfo( getNthOctagonalHeptagonalNumber, 1 ),
    'octhex'            : OperatorInfo( getNthOctagonalHexagonalNumber, 1 ),
    'october'           : OperatorInfo( lambda: 10, 0 ),
    'octpent'           : OperatorInfo( getNthOctagonalPentagonalNumber, 1 ),
    'octsquare'         : OperatorInfo( getNthOctagonalSquareNumber, 1 ),
    'octtri'            : OperatorInfo( getNthOctagonalTriangularNumber, 1 ),
    'oeis'              : OperatorInfo( lambda n: downloadOEISSequence( int( n ) ), 1 ),
    'oeiscomment'       : OperatorInfo( lambda n: downloadOEISText( int( n ), 'C', True ), 1 ),
    'oeisex'            : OperatorInfo( lambda n: downloadOEISText( int( n ), 'E', True ), 1 ),
    'oeisname'          : OperatorInfo( lambda n: downloadOEISText( int( n ), 'N', True ), 1 ),
    'omega'             : OperatorInfo( lambda: lambertw( 1 ), 0 ),
    'or'                : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x | y ), 2 ),
    'padovan'           : OperatorInfo( getNthPadovanNumber, 1 ),
    'parity'            : OperatorInfo( lambda n : getBitCount( n ) & 1, 1 ),
    'pascal'            : OperatorInfo( getNthPascalLine, 1 ),
    'pell'              : OperatorInfo( getNthPellNumber, 1 ),
    'pentagonal'        : OperatorInfo( lambda n: getNthPolygonalNumber( n, 5 ), 1 ),
    'pentagonal?'       : OperatorInfo( lambda n: findNthPolygonalNumber( n, 5 ), 1 ),
    'pentanacci'        : OperatorInfo( getNthPentanacci, 1 ),
    'pentatope'         : OperatorInfo( getNthPentatopeNumber, 1 ),
    'perm'              : OperatorInfo( getPermutations, 2 ),
    'phi'               : OperatorInfo( phi, 0 ),
    'pi'                : OperatorInfo( pi, 0 ),
    'plastic'           : OperatorInfo( getPlasticConstant, 0 ),
    'polyarea'          : OperatorInfo( getRegularPolygonArea, 1 ),
    'polygamma'         : OperatorInfo( psi, 2 ),
    'polygonal'         : OperatorInfo( getNthPolygonalNumber, 2 ),
    'polygonal?'        : OperatorInfo( findNthPolygonalNumber, 2 ),
    'polylog'           : OperatorInfo( polylog, 2 ),
    'polyprime'         : OperatorInfo( getNthPolyPrime, 2 ),
    'polytope'          : OperatorInfo( getNthPolytopeNumber, 2 ),
    'power'             : OperatorInfo( exponentiate, 2 ),
    'presidents_day'    : OperatorInfo( calculatePresidentsDay, 1 ),
    'prevost'           : OperatorInfo( getPrevostConstant, 0 ),
    'prime'             : OperatorInfo( getNthPrime, 1 ),
    'prime?'            : OperatorInfo( lambda n: findPrime( n )[ 1 ], 1 ),
    'primepi'           : OperatorInfo( getPrimePi, 1 ),
    'primes'            : OperatorInfo( getPrimes, 2 ),
    'primorial'         : OperatorInfo( getPrimorial, 1 ),
    'pyramid'           : OperatorInfo( lambda n: getNthPolygonalPyramidalNumber( n, 4 ), 1 ),
    'quadprime'         : OperatorInfo( getNthQuadrupletPrime, 1 ),
    'quadprime?'        : OperatorInfo( lambda i: findQuadrupletPrimes( i )[ 1 ], 1 ),
    'quadprime_'        : OperatorInfo( getNthQuadrupletPrimeList, 1 ),
    'quintprime'        : OperatorInfo( getNthQuintupletPrime, 1 ),
    'quintprime_'       : OperatorInfo( getNthQuintupletPrimeList, 1 ),
    'randint'           : OperatorInfo( randrange, 1 ),
    'random'            : OperatorInfo( rand, 0 ),
    'range'             : OperatorInfo( expandRange, 2 ),
    'range2'            : OperatorInfo( expandSteppedRange, 3 ),
    'reciprocal'        : OperatorInfo( takeReciprocal, 1 ),
    'repunit'           : OperatorInfo( getNthBaseKRepunit, 2 ),
    'rhombdodec'        : OperatorInfo( getNthRhombicDodecahedralNumber, 1 ),
    'riesel'            : OperatorInfo( lambda n: fsub( fmul( n, power( 2, n ) ), 1 ), 1 ),
    'robbins'           : OperatorInfo( getRobbinsConstant, 0 ),
    'root'              : OperatorInfo( root, 2 ),
    'root2'             : OperatorInfo( sqrt, 1 ),
    'root3'             : OperatorInfo( cbrt, 1 ),
    'round'             : OperatorInfo( lambda n: floor( fadd( n, 0.5 ) ), 1 ),
    'safeprime'         : OperatorInfo( lambda n: fadd( fmul( getNthSophiePrime( n ), 2 ), 1 ), 1 ),
    'saturday'          : OperatorInfo( lambda: 6, 0 ),
    'schroeder'         : OperatorInfo( getNthSchroederNumber, 1 ),
    'sec'               : OperatorInfo( lambda n: performTrigOperation( n, sec ), 1 ),
    'sech'              : OperatorInfo( lambda n: performTrigOperation( n, sech ), 1 ),
    'september'         : OperatorInfo( lambda: 9, 0 ),
    'sextprime'         : OperatorInfo( getNthSextupletPrime, 1 ),
    'sextprime_'        : OperatorInfo( getNthSextupletPrimeList, 1 ),
    'sexyprime'         : OperatorInfo( getNthSexyPrime, 1 ),
    'sexyprime_'        : OperatorInfo( getNthSexyPrimeList, 1 ),
    'sexyquad'          : OperatorInfo( getNthSexyQuadruplet, 1 ),
    'sexyquad_'         : OperatorInfo( getNthSexyQuadrupletList, 1 ),
    'sexytriplet'       : OperatorInfo( getNthSexyTriplet, 1 ),
    'sexytriplet_'      : OperatorInfo( getNthSexyTripletList, 1 ),
    'shiftleft'         : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x << y ), 2 ),
    'shiftright'        : OperatorInfo( lambda n, k: performBitwiseOperation( n, k, lambda x, y:  x >> y ), 2 ),
    'short'             : OperatorInfo( lambda n: convertToSignedInt( n , 16 ), 1 ),
    'sin'               : OperatorInfo( lambda n: performTrigOperation( n, sin ), 1 ),
    'sinh'              : OperatorInfo( lambda n: performTrigOperation( n, sinh ), 1 ),
    'solve2'            : OperatorInfo( solveQuadraticPolynomial, 3 ),
    'solve3'            : OperatorInfo( solveCubicPolynomial, 4 ),
    'solve4'            : OperatorInfo( solveQuarticPolynomial, 5 ),
    'sophieprime'       : OperatorInfo( getNthSophiePrime, 1 ),
    'spherearea'        : OperatorInfo( lambda n: getNSphereSurfaceArea( 3, n ), 1 ),
    'sphereradius'      : OperatorInfo( lambda n: getNSphereRadius( 3, n ), 1 ),
    'spherevolume'      : OperatorInfo( lambda n: getNSphereVolume( 3, n ), 1 ),
    'square'            : OperatorInfo( lambda i: exponentiate( i, 2 ), 1 ),
    'squaretri'         : OperatorInfo( getNthSquareTriangularNumber, 1 ),
    'steloct'           : OperatorInfo( getNthStellaOctangulaNumber, 1 ),
    'subfac'            : OperatorInfo( lambda n: floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) ), 1 ),
    'subtract'          : OperatorInfo( subtract, 2, ),
    'sunday'            : OperatorInfo( lambda: 7, 0 ),
    'superfac'          : OperatorInfo( superfac, 1 ),
    'superprime'        : OperatorInfo( getNthSuperPrime, 1 ),
    'sylvester'         : OperatorInfo( getNthSylvester, 1 ),
    'tan'               : OperatorInfo( lambda n: performTrigOperation( n, tan ), 1 ),
    'tanh'              : OperatorInfo( lambda n: performTrigOperation( n, tanh ), 1 ),
    'tetrahedral'       : OperatorInfo( lambda n: polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n ), 1 ),
    'tetranacci'        : OperatorInfo( getNthTetranacci, 1 ),
    'tetrate'           : OperatorInfo( tetrate, 2 ),
    'thabit'            : OperatorInfo( lambda n : fsub( fmul( 3, power( 2, n ) ), 1 ), 1 ),
    'thanksgiving'      : OperatorInfo( calculateThanksgiving, 1 ),
    'thursday'          : OperatorInfo( lambda: 4, 0 ),
    'today'             : OperatorInfo( getToday, 0 ),
    'tounixtime'        : OperatorInfo( convertToUnixTime, 1 ),
    'trianglearea'      : OperatorInfo( getTriangleArea, 3 ),
    'triangular'        : OperatorInfo( lambda n : getNthPolygonalNumber( n, 3 ), 1 ),
    'triangular?'       : OperatorInfo( lambda n : findNthPolygonalNumber( n, 3 ), 1 ),
    'tribonacci'        : OperatorInfo( getNthTribonacci, 1 ),
    'triplebal'         : OperatorInfo( getNthTripleBalancedPrime, 1 ),
    'triplebal_'        : OperatorInfo( getNthTripleBalancedPrimeList, 1 ),
    'tripletprime'      : OperatorInfo( getNthTripletPrime, 1 ),
    'tripletprime'      : OperatorInfo( getNthTripletPrimeList, 1 ),
    'truncoct'          : OperatorInfo( getNthTruncatedOctahedralNumber, 1 ),
    'trunctet'          : OperatorInfo( getNthTruncatedTetrahedralNumber, 1 ),
    'tuesday'           : OperatorInfo( lambda: 2, 0 ),
    'twinprime'         : OperatorInfo( getNthTwinPrime, 1 ),
    'twinprime_'        : OperatorInfo( getNthTwinPrimeList, 1 ),
    'uchar'             : OperatorInfo( lambda n: int( fmod( n, power( 2, 8 ) ) ), 1 ),
    'uinteger'          : OperatorInfo( lambda n, k: int( fmod( n, power( 2, k ) ) ), 2 ),
    'ulong'             : OperatorInfo( lambda n: int( fmod( n, power( 2, 32 ) ) ), 1 ),
    'ulonglong'         : OperatorInfo( lambda n: int( fmod( n, power( 2, 64 ) ) ), 1 ),
    'unitroots'         : OperatorInfo( lambda i: unitroots( int( i ) ), 1 ),
    'ushort'            : OperatorInfo( lambda n: int( fmod( n, power( 2, 16 ) ) ), 1 ),
    'value'             : OperatorInfo( getValue, 1 ),
    'wednesday'         : OperatorInfo( lambda: 3, 0 ),
    'weekday'           : OperatorInfo( getWeekday, 1, ),
    'xor'               : OperatorInfo( lambda i, j: performBitwiseOperation( i, j, lambda x, y:  x ^ y ), 2 ),
    'ydhms'             : OperatorInfo( convertToYDHMS, 1 ),
    'year_calendar'     : OperatorInfo( generateYearCalendar, 1 ),
    'zeta'              : OperatorInfo( zeta, 1 ),
    '_dumpalias'        : OperatorInfo( dumpAliases, 0 ),
    '_dumpops'          : OperatorInfo( dumpOperators, 0 ),
    '_stats'            : OperatorInfo( dumpStats, 0 ),
    '~'                 : OperatorInfo( getInvertedBits, 1 ),
#   'antitet'           : OperatorInfo( findTetrahedralNumber, 1 ),
#   'bernfrac'          : OperatorInfo( bernfrac, 1 ),
#   'powmod'            : OperatorInfo( getPowMod, 3 ),
}


#//******************************************************************************
#//
#//  applyNumberValueToUnit
#//
#//  We have to treat constant units differently because they become plain
#//  numbers.
#//
#//******************************************************************************

def applyNumberValueToUnit( number, term ):
    if g.unitOperators[ term ].unitType == 'constant':
        value = mpf( Measurement( number, term ).convertValue( Measurement( 1, { 'unity' : 1 } ) ) )
    else:
        value = Measurement( number, term, g.unitOperators[ term ].representation, g.unitOperators[ term ].plural )

    return value


#//******************************************************************************
#//
#//  abortArgsNeeded
#//
#//******************************************************************************

def abortArgsNeeded( term, index, argsNeeded ):
    print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
           format( argsNeeded ) + ' argument', end='' )

    print( 's' if argsNeeded > 1 else '' )
    sys.exit( 0 )


#//******************************************************************************
#//
#//  evaluateTerm
#//
#//  This looks worse than it is.  It just has to do slightly different things
#//  depending on what kind of term or operator is involved.  Plus, there's a
#//  lot of exception handling.
#//
#//******************************************************************************

def evaluateTerm( term, index, currentValueList ):
    try:
        # handle a modifier operator
        if term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )

        # handle a unit operator
        elif term in g.unitOperators:
            # look for unit without a value (in which case we give it a value of 1)
            if len( currentValueList ) == 0 or isinstance( currentValueList[ -1 ], Measurement ) or \
               ( isinstance( currentValueList[ -1 ], list ) and isinstance( currentValueList[ -1 ][ 0 ], Measurement ) ):
                currentValueList.append( applyNumberValueToUnit( 1, term ) )
            # if the unit comes after a list, then apply it to every item in the list
            elif isinstance( currentValueList[ -1 ], list ):
                argList = currentValueList.pop( )

                newArg = [ ]

                for listItem in argList:
                    newArg.append( applyNumberValueToUnit( listItem, term ) )

                currentValueList.append( newArg )
            # and if it's a plain old number, then apply it to the unit
            elif isinstance( currentValueList[ -1 ], mpf ):
                currentValueList.append( applyNumberValueToUnit( currentValueList.pop( ), term ) )
            else:
                raise ValueError( 'unsupported type for a unit operator' )

        # handle a regular operator
        elif term in operators:
            operatorInfo = operators[ term ]

            argsNeeded = operatorInfo.argCount

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                abortArgsNeeded( term, index, argsNeeded )

            if argsNeeded == 0:
                result = callers[ 0 ]( operatorInfo.function, None )
            else:
                argList = list( )

                for i in range( 0, argsNeeded ):
                    arg = currentValueList.pop( )
                    argList.append( arg if isinstance( arg, list ) else [ arg ] )

                result = callers[ argsNeeded ]( operatorInfo.function, *argList )

            if len( result ) == 1:
                result = result[ 0 ]

            currentValueList.append( result )

        # handle a list operator
        elif term in listOperators:
            operatorInfo = listOperators[ term ]
            argsNeeded = operatorInfo.argCount

            # first we validate, and make sure the operator has enough arguments
            if len( currentValueList ) < argsNeeded:
                abortArgsNeeded( term, index, argsNeeded )

            # handle the call depending on the number of arguments needed
            if argsNeeded == 0:
                currentValueList.append( operatorInfo.function( currentValueList ) )
            elif argsNeeded == 1:
                currentValueList.append( evaluateOneListFunction( operatorInfo.function, currentValueList.pop( ) ) )
            else:
                listArgs = [ ]

                for i in range( 0, argsNeeded ):
                    listArgs.insert( 0, currentValueList.pop( ) )

                currentValueList.append( operatorInfo.function( *listArgs ) )
        # handle a plain old value (i.e., a number, not an operator)
        else:
            try:
                currentValueList.append( parseInputValue( term, g.inputRadix ) )

            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )
                if g.debugMode:
                    raise
                else:
                    sys.exit( 0 )

            except ( AttributeError, TypeError ):
                try:
                    print( 'rpn:  error in arg ' + format( index ) + ':  unrecognized argument: \'' +
                           term + '\'' )
                except:
                    print( 'rpn:  error in arg ' + format( index ) + ':  non-ASCII characters' )

                if g.debugMode:
                    raise
                else:
                    sys.exit( 0 )

    except KeyboardInterrupt as error:
        print( 'rpn:  keyboard interrupt' )

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )

    except ( ValueError, AttributeError, TypeError ) as error:
        print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )

    except ZeroDivisionError as error:
        print( 'rpn:  division by zero' )

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )

    except IndexError as error:
        print( 'rpn:  index error for list operator at arg ' + format( index ) +
               '.  Are your arguments in the right order?' )

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )

    return True


#//******************************************************************************
#//
#//  handleIdentify
#//
#//******************************************************************************

def handleIdentify( result ):
    formula = identify( result )

    if formula is None:
        base = [ 'pi', 'e', 'euler' ]
        formula = identify( result, base )

    if formula is None:
        print( '    = [formula cannot be found]' )
    else:
        print( '    = ' + formula )



#//******************************************************************************
#//
#//  findPolynomial
#//
#//******************************************************************************

def findPolynomial( result, findPoly ):
    poly = str( findpoly( result, findPoly ) )

    if poly == 'None':
        poly = str( findpoly( result, findPoly, maxcoeff=1000 ) )

    if poly == 'None':
        poly = str( findpoly( result, findPoly, maxcoeff=100000 ) )

    if poly == 'None':
        poly = str( findpoly( result, findPoly, maxcoeff=1000000, tol=1e-10 ) )

    if poly == 'None':
        print( '    = polynomial of degree <= %d not found' % findPoly )
    else:
        print( '    = polynomial ' + poly )


#//******************************************************************************
#//
#//  rpn
#//
#//******************************************************************************

def rpn( cmd_args ):
    # initialize globals
    g.debugMode = False

    if getattr( sys, 'frozen', False ):
        g.dataPath = os.path.dirname( sys.executable )
    else:
        g.dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + 'rpndata'

    help = False
    helpArgs = [ ]

    if len( cmd_args ) == 0:
        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )
        return

    for i in range( 0, len( cmd_args ) ):
        if cmd_args[ i ] == 'help':
            help = True
        else:
            if help:
                helpArgs.append( cmd_args[ i ] )

    if help:
        parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' +
                                          PROGRAM_VERSION + ': ' + PROGRAM_DESCRIPTION + '\n    ' +
                                          COPYRIGHT_MESSAGE, add_help=False,
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          prefix_chars='-' )

        parser.add_argument( 'terms', nargs='*', metavar='term' )
        parser.add_argument( '-l', '--line_length', type=int, action='store', default=defaultLineLength )

        args = parser.parse_args( cmd_args )

        try:
            with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
                unitsVersion = pickle.load( pickleFile )
                g.basicUnitTypes = pickle.load( pickleFile )
                g.unitOperators = pickle.load( pickleFile )
                operatorAliases.update( pickle.load( pickleFile ) )
                g.compoundUnits = pickle.load( pickleFile )
        except FileNotFoundError as error:
            print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.' )

        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, listOperators, modifiers, operatorAliases,
                   g.dataPath, helpArgs, args.line_length )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=defaultAccuracy,  # -1
                         const=defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping )
    parser.add_argument( '-D', '--DEBUG', action='store_true' )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--identify', action='store_true' )
    parser.add_argument( '-l', '--line_length', type=int, action='store', default=defaultLineLength )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0 )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-u', '--find_poly', nargs='?', type=int, action='store', default=0, const=1000 )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store',
                         default=defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    args = parser.parse_args( cmd_args )

    if len( args.terms ) == 0:
        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )
        return

    if args.help or args.other_help:
        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, listOperators, modifiers,
                   operatorAliases, g.dataPath, [ ], args.line_length )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

    mp.dps = args.precision

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    g.bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -D
    if args.DEBUG:
        g.debugMode = True

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -n
    g.numerals = args.numerals

    # handle -b
    g.inputRadix = int( args.input_radix )

    # handle -r
    if args.output_radix == 'phi':
        outputRadix = phiBase
    elif args.output_radix == 'fib':
        outputRadix = fibBase
    else:
        try:
            outputRadix = int( args.output_radix )
        except ValueError as error:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return

    # handle -x
    if args.hex:
        outputRadix = 16
        leadingZero = True
        integerGrouping = 4
        g.bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        g.bitwiseGroupSize = 9

    # handle -R
    if args.output_radix_numerals > 0:
        baseAsDigits = True
        outputRadix = args.output_radix_numerals
    else:
        baseAsDigits = False

    # -r/-R validation
    if baseAsDigits:
        if ( outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return
    else:
        if ( outputRadix != phiBase and outputRadix != fibBase and
             ( outputRadix < 2 or outputRadix > 62 ) ):
            print( 'rpn:  output radix must be from 2 to 62, or phi' )
            return

    # handle -y and -u:  mpmath wants precision of at least 53 for these functions
    if args.identify or args.find_poly > 0:
        if mp.dps < 53:
            mp.dps = 53

    index = 1                 # only used for error messages
    valueList = list( )

    if args.print_options:
        print( '--output_accuracy:  %d' % args.output_accuracy )
        print( '--input_radix:  %d' % g.inputRadix )
        print( '--comma:  ' + ( 'true' if args.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % args.decimal_grouping )
        print( '--integer_grouping:  %d' % integerGrouping )
        print( '--numerals:  ' + args.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % args.output_radix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--time:  ' + ( 'true' if args.time else 'false' ) )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % g.bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            unitsVersion = pickle.load( pickleFile )
            g.basicUnitTypes = pickle.load( pickleFile )
            g.unitOperators = pickle.load( pickleFile )
            operatorAliases.update( pickle.load( pickleFile ) )
            g.compoundUnits = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.' )

    if unitsVersion != PROGRAM_VERSION:
        print( 'rpn  units data file version mismatch' )

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        if term in operatorAliases:
            term = operatorAliases[ term ]

        if term in functionOperators:
            if g.creatingFunction:
                g.creatingFunction = False
            else:
                raise ValueError( 'function operators require a function definition' )
        elif g.creatingFunction:
            currentValueList[ -1 ].add( term )
            continue

        currentValueList = getCurrentArgList( valueList )

        if not evaluateTerm( term, index, currentValueList ):
            break

        index = index + 1

    # handle output
    if isinstance( valueList[ 0 ], FunctionInfo ):
        print( 'rpn:  unexpected end of input in function definition' )
    elif len( valueList ) > 1 or len( valueList ) == 0:
        print( 'rpn:  unexpected end of input' )
    else:
        mp.pretty = True
        result = valueList.pop( )

        if args.comma:
            integerGrouping = 3     # override whatever was set on the command-line
            leadingZero = False     # this one, too
            integerDelimiter = ','
        else:
            integerDelimiter = ' '

        if isinstance( result, list ):
            print( formatListOutput( result, outputRadix, g.numerals, integerGrouping, integerDelimiter,
                                     leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                     args.output_accuracy ) )
        else:
            if isinstance( result, arrow.Arrow ):
                outputString = formatDateTime( result )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                outputString = formatOutput( resultString, outputRadix, g.numerals, integerGrouping,
                                             integerDelimiter, leadingZero, args.decimal_grouping,
                                             ' ', baseAsDigits, args.output_accuracy )

                # handle the units if we are displaying a measurement
                if isinstance( result, Measurement ):
                    outputString += ' ' + formatUnits( result )

            printParagraph( outputString, args.line_length )

            # handle --identify
            if args.identify:
                handleIdentify( result )

            # handle --find_poly
            if args.find_poly > 0:
                findPolynomial( result, args.find_poly )

        saveResult( result )

    if args.time:
        print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    try:
        rpn( sys.argv[ 1 : ] )
    except ValueError as error:
        print( 'rpn:  value error:  {0}'.format( error ) )

