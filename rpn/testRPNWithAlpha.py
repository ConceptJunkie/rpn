#!/usr/bin/env python

# //******************************************************************************
# //
# //  testRPNWithAlpha
# //
# //  test script for RPN
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import os
import sys
import time
import wolframalpha

from collections import OrderedDict

from rpn.rpnOperators import *

from rpn.rpnAliases import operatorAliases
from rpn.rpnOperators import constants
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnPersistence import cachedFunction, loadUnitNameData
from rpn.rpnPrimeUtils import checkForPrimeData
from rpn.rpnTestUtils import *
from rpn.rpnUtils import getUserDataPath

from mpmath import *

client = None


# //******************************************************************************
# //
# //  initializeAlpha
# //
# //******************************************************************************

def initializeAlpha( ):
    with open( getUserDataPath( ) + os.sep + 'wolframalpha.key', "r" ) as input:
        key = input.read( ).replace( '\n', '' )

    return wolframalpha.Client( key )


# //******************************************************************************
# //
# //  queryAlpha
# //
# //******************************************************************************

@cachedFunction( 'wolfram', overrideIgnore=True )
def queryAlpha( query ):
    client = initializeAlpha( )
    res = client.query( query )
    return next( res.results ).text


# //******************************************************************************
# //
# //  testOperator just evaluates an RPN expression to make sure nothing throws
# //  an exception.
# //
# //  expectEqual actually tests that the result from RPN matches the value
# //  given.
# //
# //  expectEqual evaluates two RPN expressions and verifies that the results
# //  are the same.
# //
# //  expectEquivalent evaluates two RPN expressions and verifies that the
# //  results are equivalent.  This means that if the results are lists, they
# //  need to have the same elements, but not necessarily be in the same order.
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  runAlgebraOperatorTests
# //
# //******************************************************************************

def runAlgebraOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runArithmeticOperatorTests
# //
# //******************************************************************************

def runArithmeticOperatorTests( ):
    # gcd
    #expectEqual( '[ 124 324 ] gcd', queryAlpha( 'gcd of 324 and 124' ) )
    #expectEqual( '[ 1296 1440 ] gcd', queryAlpha( 'gcd of 1296 and 1440' ) )

    # lcm
    #expectEqual( '[ 3 12 36 65 10 ] lcm', queryAlpha( 'least common multiple of 3 12 36 65 10' ) )
    #expectEqual( '[ 1296 728 3600 460 732 ] lcm', queryAlpha( 'least common multiple of 1296 728 3600 460 732' ) )
    pass


# //******************************************************************************
# //
# //  runAstronomyOperatorTests
# //
# //******************************************************************************

def runAstronomyOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runBitwiseOperatorTests
# //
# //******************************************************************************

def runBitwiseOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runCalendarOperatorTests
# //
# //******************************************************************************

def runCalendarOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runCombinatoricsOperatorTests
# //
# //******************************************************************************

def runCombinatoricsOperatorTests( ):
    # binomial
    #expectEqual( '12 9 binomial', queryAlpha( '12 choose 9' ) )
    #expectEqual( '-a20 120 108 binomial', queryAlpha( '120 choose 108' ) )
    pass


# //******************************************************************************
# //
# //  runComplexMathOperatorTests
# //
# //******************************************************************************

def runComplexMathOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runConstantOperatorTests
# //
# //******************************************************************************

def runConstantOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runConversionOperatorTests
# //
# //******************************************************************************

def runConversionOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runDateTimeOperatorTests
# //
# //******************************************************************************

def runDateTimeOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runFunctionOperatorTests
# //
# //******************************************************************************

def runFunctionOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runGeographyOperatorTests
# //
# //******************************************************************************

def runGeographyOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runGeometryOperatorTests
# //
# //******************************************************************************

def runGeometryOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runInternalOperatorTests
# //
# //******************************************************************************

def runInternalOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runLexicographyOperatorTests
# //
# //******************************************************************************

def runLexicographyOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runListOperatorTests
# //
# //******************************************************************************

def runListOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runLogarithmsOperatorTests
# //
# //******************************************************************************

def runLogarithmsOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runModifierOperatorTests
# //
# //******************************************************************************

def runModifierOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runNumberTheoryOperatorTests
# //
# //******************************************************************************

def runNumberTheoryOperatorTests( ):
    # frobenius
    #expectEqual( '[ 4, 7, 12 ] frobenius', queryAlpha( 'Frobenius number {4, 7, 12}' ) )
    #expectEqual( '[ 23, 29, 47 ] frobenius', queryAlpha( 'Frobenius number {23, 29, 47}' ) )
    pass


# //******************************************************************************
# //
# //  runPhysicsOperatorTests
# //
# //******************************************************************************

def runPhysicsOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runPolygonalOperatorTests
# //
# //******************************************************************************

def runPolygonalOperatorTests( ):
    # triangular
    #expectEqual( '203 triangular', queryAlpha( '203rd triangular number' ) )
    pass


# //******************************************************************************
# //
# //  runPolyhedralOperatorTests
# //
# //******************************************************************************

def runPolyhedralOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runPowersAndRootsOperatorTests
# //
# //******************************************************************************

def runPowersAndRootsOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runPrimeNumberOperatorTests
# //
# //******************************************************************************

def runPrimeNumberOperatorTests( ):
    for i in range( 150 ):
        print( 'ready!' )
        rpnSide = str( ( i + 1 ) * 100000000 ) + ' prime'
        alphaSide = str( ( i + 1 ) * 100000000 ) + 'th prime number'

        expectEqual( rpnSide, str( queryAlpha( alphaSide ) ) )
        time.sleep( 5 )


# //******************************************************************************
# //
# //  runSettingsOperatorTests
# //
# //  These operators need to be tested in interactive mode.
# //
# //******************************************************************************

def runSettingsOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runSpecialOperatorTests
# //
# //******************************************************************************

def runSpecialOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runTrigonometryOperatorTests
# //
# //******************************************************************************

def runTrigonometryOperatorTests( ):
    pass


# //******************************************************************************
# //
# //  runAdvancedTests
# //
# //  This is just for tests that are more complex than the single operator
# //  tests.
# //
# //******************************************************************************

def runAdvancedTests( ):
    pass


# //******************************************************************************
# //
# //  tests
# //
# //******************************************************************************

rpnTestList = [
    ( 'algebra',            runAlgebraOperatorTests ),
    ( 'arithmetic',         runArithmeticOperatorTests ),
    ( 'astronomy',          runAstronomyOperatorTests ),
    ( 'bitwise',            runBitwiseOperatorTests ),
    ( 'calendar',           runCalendarOperatorTests ),
    ( 'combinatorics',      runCombinatoricsOperatorTests ),
    ( 'complex',            runComplexMathOperatorTests ),
    ( 'constant',           runConstantOperatorTests ),
    ( 'conversion',         runConversionOperatorTests ),
    ( 'date_time',          runDateTimeOperatorTests ),
    ( 'function',           runFunctionOperatorTests ),
    ( 'geography',          runGeographyOperatorTests ),
    ( 'geometry',           runGeometryOperatorTests ),
    ( 'lexicography',       runLexicographyOperatorTests ),
    ( 'list',               runListOperatorTests ),
    ( 'logarithms',         runLogarithmsOperatorTests ),
    ( 'modifier',           runModifierOperatorTests ),
    ( 'number_theory',      runNumberTheoryOperatorTests ),
    ( 'physics',            runPhysicsOperatorTests ),
    ( 'polygonal',          runPolygonalOperatorTests ),
    ( 'polyhedral',         runPolyhedralOperatorTests ),
    ( 'powers_and_roots',   runPowersAndRootsOperatorTests ),
    ( 'prime_number',       runPrimeNumberOperatorTests ),
    ( 'settings',           runSettingsOperatorTests ),
    ( 'special',            runSpecialOperatorTests ),
    ( 'trigonometry',       runTrigonometryOperatorTests ),
    ( 'advanced',           runAdvancedTests ),

    ( 'internal',           runInternalOperatorTests )
]

rpnTests = OrderedDict( )

for test in rpnTestList:
    rpnTests[ test[ 0 ] ] = test[ 1 ]


# //******************************************************************************
# //
# //  runTests
# //
# //******************************************************************************

def runTests( tests ):
    if tests:
        for test in tests:
            if test in rpnTests:
                rpnTests[ test ]( )
    else:
        for test in rpnTests:
            rpnTests[ test ]( )


# //******************************************************************************
# //
# //  main
# //
# //******************************************************************************

def main( ):
    loadUnitNameData( )
    checkForPrimeData( )

    runTests( sys.argv[ 1 : ] )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    main( )

