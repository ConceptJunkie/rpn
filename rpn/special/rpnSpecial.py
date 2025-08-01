#!/usr/bin/env python

#*******************************************************************************
#
#  rpnSpecial.py
#
#  rpnChilada special operators
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#*******************************************************************************

import functools
import re as regex
import sys
import urllib.request as urllib2
import uuid

from urllib.error import URLError

from random import randrange

from mpmath import arange, cbrt, ceil, fabs, fadd, fdiv, fib, findpoly, \
                   floor, fmul, fsub, identify, inf, log, log10, mpmathify, \
                   phi, power, rand, root, sqrt

from rpn.math.rpnCombinatorics import \
    getNthAperyNumber, getNthDelannoyNumber, getNthMenageNumber, getNthMotzkinNumber, getNthPellNumber, \
    getNthSchroederNumber, getNthSchroederHipparchusNumber, getNthSylvesterNumber, getPartitionNumber

from rpn.math.rpnFactor import getFactors

from rpn.math.rpnLexicographic import getErdosPersistence, getPersistence, \
    hasUniqueDigits, isAutomorphic, isBaseKSmithNumber, \
    isDecreasing, isBouncy, isIncreasing, isKaprekarNumber, isKMorphic, \
    isNarcissistic, isOrderKSmithNumber, isPandigital, isPerfectDigitalInvariant, \
    isPerfectDigitToDigitInvariant, isSmithNumber, isStepNumber, isTrimorphic, \
    multiplyDigits, multiplyNonzeroDigits, sumDigits

from rpn.math.rpnMath import isInteger

from rpn.math.rpnNumberTheory import \
    getDigitalRoot, getDivisorCount, getNthDoubleFactorial, getEulerPhi, \
    getNthMobiusNumber, getNthAlternatingFactorial, getNthBaseKRepunit, \
    getNthCalkinWilf, getNthCarolNumber, getNthFactorial, getNthFibonorial, \
    getNthHyperfactorial, getNthJacobsthalNumber, getNthKFibonacciNumber, \
    getNthKyneaNumber, getNthLeonardoNumber, getNthLucasNumber, \
    getNthMersenneExponent, getNthMersennePrime, getNthPadovanNumber, \
    getNthPerfectNumber, getNthSubfactorial, getNthSternNumber, \
    getNthSuperfactorial, getNthThabitNumber, getRadical, getSigma, \
    isAbundant, isAchillesNumber, isAntiharmonic, isCarmichaelNumber, \
    isDeficient, isKHyperperfect, isPernicious, isPolydivisible, isPowerful, \
    isPronic, isRough, isRuthAaronNumber, isSemiprime, isSmooth, isSphenic, \
    isSquareFree, isUnusual

from rpn.math.rpnPolytope import findCenteredPolygonalNumber, findPolygonalNumber, \
                            getNthCenteredPolygonalNumber, getNthPolygonalNumber

from rpn.math.rpnPrimeUtils import getPrimes, isPrime

from rpn.math.rpnSimpleMath import isEven, isKthPower, isOdd

from rpn.special.rpnName import getNumberName, getShortOrdinalName

from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnPersistence import cachedOEISFunction
from rpn.util.rpnSettings import setAccuracy
from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, ComplexValidator, DefaultValidator, IntValidator

LARGEST_NUMBER_TO_FACTOR = power( 10, 40 )


#*******************************************************************************
#
#  getRandomNumber
#
#*******************************************************************************

def getRandomNumber( ):
    return rand( )


def getRandomNumberOperator( ):
    return getRandomNumber( )


#*******************************************************************************
#
#  getRandomInteger
#
#*******************************************************************************

def getRandomInteger( n ):
    return randrange( int( n ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getRandomIntegerOperator( n ):
    return getRandomInteger( n )


#*******************************************************************************
#
#  getMultipleRandoms
#
#*******************************************************************************

def getMultipleRandoms( n ):
    '''
    Returns n random numbers.
    '''
    for _ in arange( 0, n ):
        yield rand( )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getMultipleRandomsOperator( n ):
    return RPNGenerator.createGenerator( getMultipleRandoms, n )


#*******************************************************************************
#
#  getRandomIntegers
#
#*******************************************************************************

def getRandomIntegers( n, k ):
    '''
    Returns k random integers between 0 and n-1.
    '''
    for _ in arange( 0, k ):
        yield randrange( int( n ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 0 ) ] )
def getRandomIntegersOperator( n, k ):
    return RPNGenerator.createGenerator( getRandomIntegers, [ n, k ] )


#*******************************************************************************
#
#  removeUnderscores
#
#*******************************************************************************

def removeUnderscores( source ):
    '''
    This function replaces the underscores in a string with spaces, and is
    used for formatting unit output.
    '''
    result = ''

    for c in source:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


#*******************************************************************************
#
#  downloadOEISSequenceOperator
#
#*******************************************************************************

@cachedOEISFunction( 'oeis' )
def downloadOEISSequence( aNumber ):
    '''Downloads and formats data from oeis.org.'''
    keywords = downloadOEISText( aNumber, 'K' ).split( ',' )

    # If oeis.org isn't available, just punt everything
    if keywords == [ '' ]:
        return 0

    result, success = downloadOEISTable( aNumber )

    if success:
        return result

    if 'nonn' in keywords:
        result = downloadOEISText( aNumber, 'S' )
        result += downloadOEISText( aNumber, 'T' )
        result += downloadOEISText( aNumber, 'U' )
    else:
        result = downloadOEISText( aNumber, 'V' )
        result += downloadOEISText( aNumber, 'W' )
        result += downloadOEISText( aNumber, 'X' )

    if 'cons' in keywords:
        offset = int( downloadOEISText( aNumber, 'O' ).split( ',' )[ 0 ] )
        result = ''.join( result.split( ',' ) )
        return mpmathify( result[ : offset ] + '.' + result[ offset : ] )

    value_list = [ int( i ) for i in result.split( ',' ) ]

    setAccuracy( max( len( i ) for i in value_list ) + 1 )

    return [ int( i ) for i in result.split( ',' ) ]


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISSequenceOperator( aNumber ):
    return downloadOEISSequence( aNumber )


#*******************************************************************************
#
#  downloadOEISText
#
#*******************************************************************************

def downloadOEISText( aNumber, char, addCR = False ):
    '''
    Downloads, formats and caches text data from oeis.org.
    '''
    try:
        with urllib2.urlopen( f'http://oeis.org/search?q=id%3AA{int( aNumber ):06}' + '&fmt=text' ) as url:
            data = url.read( )
    except URLError:
        print( 'rpn:  HTTP access to oeis.org failed' )
        return ''

    pattern = regex.compile( b'%' + bytes( char, 'ascii' ) + b' A[0-9][0-9][0-9][0-9][0-9][0-9] (.*?)\n', regex.DOTALL )

    lines = pattern.findall( data )

    result = ''

    for line in lines:
        if result != '' and addCR:
            result += '\n'

        result += line.decode( 'ascii' )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISCommentOperator( n ):
    return downloadOEISText( n, 'C', True )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISExtraOperator( n ):
    return downloadOEISText( n, 'E', True )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISNameOperator( n ):
    return downloadOEISText( n, 'N', True )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISOffsetOperator( n ):
    return int( downloadOEISText( n, 'O' ).split( ',' )[ 0 ] )


#*******************************************************************************
#
#  downloadOEISTable
#
#*******************************************************************************

def downloadOEISTable( aNumber ):
    try:
        with urllib2.urlopen( f'http://oeis.org/A{int( aNumber ):06}/b{int( aNumber ):06}.txt' ) as url:
            data = url.read( )
    except URLError:
        print( 'HTTP access to oeis.org failed', file=sys.stderr )
        return [ ], False

    pattern = regex.compile( b'(.*?)[\n]', regex.DOTALL )
    lines = pattern.findall( data )

    # check if the last line doesn't end with a linefeed
    if data[ -1 ] != b'\n':
        lines.append( data[ data.rfind( b'\n' ) + 1 : ] )

    result = [ ]

    for line in lines:
        line = line.decode( 'ascii' ).strip( )

        if line == '':
            continue

        if line[ 0 ] == '#' or len( line ) == 0:
            continue

        result.append( int( line.split( )[ 1 ] ) )

    return result, True


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def downloadOEISTableOperator( aNumber ):
    downloadOEISTable( aNumber )


#*******************************************************************************
#
#  handleIdentify
#
#*******************************************************************************

def handleIdentify( result, file=sys.stdout ):
    '''Calls the mpmath identify function to try to identify a constant.'''
    if isinstance( result, ( list, RPNGenerator ) ):
        for i in list( result ):
            handleIdentify( i )

        return

    formula = identify( result )

    if formula is None:
        base = [ 'pi', 'e', 'euler', 'sqrt(pi)', 'phi' ]
        formula = identify( result, base )

    if formula is None:
        print( '    = [formula cannot be found]', file=file )
    else:
        print( '    = ' + formula, file=file )


#*******************************************************************************
#
#  findPolynomial
#
#*******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 1 ) ] )
def findPolynomialOperator( n, k ):
    '''
    Calls the mpmath findpoly function to try to identify a polynomial of
    degree <= k for which n is a zero.
    '''
    setAccuracy( 53 )

    poly = findpoly( n, int( k ) )

    if poly is None:
        poly = findpoly( n, int( k ), tol = 1e-10 )

    if poly is None:
        poly = findpoly( n, int( k ), tol = 1e-7 )

    if poly is None:
        return [ 0 ]
    else:
        return poly


#*******************************************************************************
#
#  generateUUIDOperator
#
#*******************************************************************************

def generateUUIDOperator( ):
    '''
    Generates a UUID that uses the current machine's MAC address and the
    current time as seeds.
    '''
    return str( uuid.uuid1( ) )


#*******************************************************************************
#
#  generateRandomUUIDOperator
#
#*******************************************************************************

def generateRandomUUIDOperator( ):
    '''Generates a completely random UUID.'''
    return str( uuid.uuid4( ) )


#*******************************************************************************
#
#  findInput
#
#*******************************************************************************

def findInput( value, func, estimator, minimum=0, maximum=inf ):
    guess1 = floor( estimator( value ) )

    guess1 = min( guess1, maximum )
    guess1 = max( guess1, minimum )

    # closing in
    result = func( guess1 )
    debugPrint( 'findInput func call', guess1 )

    if result == value:
        return True, guess1
    elif result > value:
        over = True
        delta = -1
    else:
        over = False
        delta = 1

    guess2 = guess1 + delta

    guess2 = min( guess2, maximum )
    guess2 = max( guess2, minimum )

    result = func( guess2 )
    debugPrint( 'findInput func call', guess2 )

    if result == value:
        return True, guess2

    if over:
        def comparator( a, b ):
            return a > b
    else:
        def comparator( a, b ):
            return a < b

    while comparator( result, value ):
        delta *= 2
        guess1 = guess2
        guess2 += delta

        if guess2 > maximum:
            return False, 0

        if guess2 < minimum:
            break

        result = func( guess2 )
        debugPrint( 'findInput func call', guess2 )

        if result == value:
            return True, guess2

    guess1 = max( minimum, guess1 )
    guess2 = max( minimum, guess2 )

    if guess1 == guess2:
        return False, 0
    elif guess1 > guess2:
        guess1, guess2 = int( guess2 ), int( guess1 )
    else:
        guess1, guess2 = int( guess1 ), int( guess2 )

    debugPrint( '->guesses:', guess1, guess2 )

    while guess1 + 1 != guess2:
        newGuess = guess1 + ( guess2 - guess1 ) // 2

        result = func( newGuess )
        debugPrint( 'findInput func call', newGuess )

        if result == value:
            return True, newGuess
        elif result > value:
            guess2 = newGuess
        else:
            guess1 = newGuess

    debugPrint( 'didn\'t find anything' )

    return False, 0


#*******************************************************************************
#
#  describeInteger
#
#*******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def describeIntegerOperator( n ):
    indent = ' ' * 4

    print( )
    print( int( n ), 'is:' )

    if isOdd( n ):
        print( indent + 'odd' )
    elif isEven( n ):
        print( indent + 'even' )

    if isPrime( n ):
        isPrimeFlag = True
        print( indent + 'prime' )
    elif n > 3:
        isPrimeFlag = False
        print( indent + 'composite' )
    else:
        isPrimeFlag = False

    if isKthPower( n, 2 ):
        print( indent + 'the ' + getShortOrdinalName( sqrt( n ) ) + ' square number' )

    if isKthPower( n, 3 ):
        print( indent + 'the ' + getShortOrdinalName( cbrt( n ) ) + ' cube number' )

    for i in arange( 4, fadd( ceil( log( fabs( n ), 2 ) ), 1 ) ):
        if isKthPower( n, i ):
            print( indent + 'the ' + getShortOrdinalName( root( n, i ) ) + ' ' +
                   getNumberName( i, True ) + ' power'  )

    # triangular
    guess = findPolygonalNumber( n, 3 )

    if getNthPolygonalNumber( guess, 3 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' triangular number' )

    # pentagonal
    guess = findPolygonalNumber( n, 5 )

    if getNthPolygonalNumber( guess, 5 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' pentagonal number' )

    # hexagonal
    guess = findPolygonalNumber( n, 6 )

    if getNthPolygonalNumber( guess, 6 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' hexagonal number' )

    # heptagonal
    guess = findPolygonalNumber( n, 7 )

    if getNthPolygonalNumber( guess, 7 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' heptagonal number' )

    # octagonal
    guess = findPolygonalNumber( n, 8 )

    if getNthPolygonalNumber( guess, 8 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' octagonal number' )

    # nonagonal
    guess = findPolygonalNumber( n, 9 )

    if getNthPolygonalNumber( guess, 9 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' nonagonal number' )

    # decagonal
    guess = findPolygonalNumber( n, 10 )

    if getNthPolygonalNumber( guess, 10 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' decagonal number' )

    # if n > 1:
    #    for i in range( 11, 101 ):
    #        if getNthPolygonalNumber( findPolygonalNumber( n, i ), i ) == n:
    #            print( indent + str( i ) + '-gonal' )

    # centered triangular
    guess = findCenteredPolygonalNumber( n, 3 )

    if getNthCenteredPolygonalNumber( guess, 3 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered triangular' )

    # centered square
    guess = findCenteredPolygonalNumber( n, 4 )

    if getNthCenteredPolygonalNumber( guess, 4 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered square number' )

    # centered pentagonal
    guess = findCenteredPolygonalNumber( n, 5 )

    if getNthCenteredPolygonalNumber( guess, 5 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered pentagonal number' )

    # centered hexagonal
    guess = findCenteredPolygonalNumber( n, 6 )

    if getNthCenteredPolygonalNumber( guess, 6 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered hexagonal number' )

    # centered heptagonal
    guess = findCenteredPolygonalNumber( n, 7 )

    if getNthCenteredPolygonalNumber( guess, 7 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered heptagonal number' )

    # centered octagonal
    guess = findCenteredPolygonalNumber( n, 8 )

    if getNthCenteredPolygonalNumber( guess, 8 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered octagonal number' )

    # centered nonagonal
    guess = findCenteredPolygonalNumber( n, 9 )

    if getNthCenteredPolygonalNumber( guess, 9 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered nonagonal number' )

    # centered decagonal
    guess = findCenteredPolygonalNumber( n, 10 )

    if getNthCenteredPolygonalNumber( guess, 10 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered decagonal number' )

    # pandigital
    if isPandigital( n ):
        print( indent + 'pandigital' )

    # for i in range( 4, 21 ):
    #    if isBaseKPandigital( n, i ):
    #        print( indent + 'base ' + str( i ) + ' pandigital' )

    # Fibonacci
    result = findInput( n, fib, lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Fibonacci number' )

    # Tribonacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 3 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Tribonacci number' )

    # Tetranacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 4 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Tetranacci number' )

    # Pentanacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 5 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Pentanacci number' )

    # Hexanacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 6 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Hexanacci number' )

    # Heptanacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 7 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Heptanacci number' )

    # Octanacci
    result = findInput( n, lambda n : getNthKFibonacciNumber( n, 8 ), lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Octanacci number' )

    # Lucas numbers
    result = findInput( n, getNthLucasNumber, lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Lucas number' )

    # base-k repunits
    if n > 1:
        for i in range( 2, 21 ):
            result = findInput( n, functools.partial( getNthBaseKRepunit, k=i ),
                                functools.partial( log, b=i ), minimum=1 )

            if result[ 0 ]:
                print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' base-' + str( i ) + ' repunit' )

    # Jacobsthal numbers
    result = findInput( n, getNthJacobsthalNumber, lambda n: fmul( log( n ), 1.6 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Jacobsthal number' )

    # Padovan numbers
    result = findInput( n, getNthPadovanNumber, lambda n: fmul( log10( n ), 9 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Padovan number' )

    # Fibonorial numbers
    result = findInput( n, getNthFibonorial, lambda n: sqrt( fmul( log( n ), 10 ) ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Fibonorial number' )

    # Mersenne primes
    result = findInput( n, getNthMersennePrime, lambda n: fadd( fmul( log( log( sqrt( n ) ) ), 2.7 ), 3 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Mersenne prime' )

    # perfect number
    result = findInput( n, getNthPerfectNumber, lambda n: fmul( log( log( n ) ), 2.6 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' perfect number' )

    # Mersenne exponent
    result = findInput( n, getNthMersenneExponent, lambda n: fmul( log( n ), 2.7 ), maximum=50 )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Mersenne exponent' )

    if not isPrimeFlag and n != 1 and n <= LARGEST_NUMBER_TO_FACTOR:
        # deficient
        if isDeficient( n ):
            print( indent + 'deficient' )

        # abundant
        if isAbundant( n ):
            print( indent + 'abundant' )

        # k_hyperperfect
        for i in sorted( list( set( sorted( downloadOEISSequence( 34898 )[ : 500 ] ) ) ) )[ 1 : ]:
            if i > n:
                break

            if isKHyperperfect( n, i ):
                print( indent + str( i ) + '-hyperperfect' )
                break

        # smooth
        for i in getPrimes( 2, 50 ):
            if isSmooth( n, i ):
                print( indent + str( i ) + '-smooth' )
                break

        # rough
        previousPrime = 2

        for i in getPrimes( 2, 50 ):
            if not isRough( n, i ):
                print( indent + str( previousPrime ) + '-rough' )
                break

            previousPrime = i

        # is_semiprime
        if isSemiprime( n ):
            print( indent + 'semiprime' )

        # is_sphenic
        elif isSphenic( n ):
            print( indent + 'sphenic' )
        elif isSquareFree( n ):
            print( indent + 'square-free' )

        # powerful
        if isPowerful( n ):
            print( indent + 'powerful' )

    # factorial
    result = findInput( n, getNthFactorial, lambda n: power( log10( n ), 0.92 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' factorial number' )

    # alternating factorial
    result = findInput( n, getNthAlternatingFactorial, lambda n: fmul( sqrt( log( n ) ), 0.72 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' alternating factorial number' )

    # double factorial
    if n == 1:
        result = ( True, 1 )
    else:
        result = findInput( n, getNthDoubleFactorial, lambda n: fdiv( power( log( log( n ) ), 4 ), 7 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' double factorial number' )

    # hyperfactorial
    result = findInput( n, getNthHyperfactorial, lambda n: fmul( sqrt( log( n ) ), 0.8 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' hyperfactorial number' )

    # subfactorial
    result = findInput( n, getNthSubfactorial, lambda n: fmul( log10( n ), 1.1 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' subfactorial number' )

    # superfactorial
    if n == 1:
        result = ( True, 1 )
    else:
        result = findInput( n, getNthSuperfactorial, lambda n: fadd( sqrt( log( n ) ), 1 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' superfactorial number' )

    # pernicious
    if isPernicious( n ):
        print( indent + 'pernicious' )

    # pronic
    if isPronic( n ):
        print( indent + 'pronic' )

    # Achilles
    if isAchillesNumber( n ):
        print( indent + 'an Achilles number' )

    # antiharmonic
    if isAntiharmonic( n ):
        print( indent + 'antiharmonic' )

    # unusual
    if isUnusual( n ):
        print( indent + 'unusual' )

    # hyperperfect
    for i in range( 2, 21 ):
        if isKHyperperfect( n, i ):
            print( indent + str( i ) + '-hyperperfect' )

    # Ruth-Aaron
    if isRuthAaronNumber( n ):
        print( indent + 'a Ruth-Aaron number' )

    # Smith numbers
    if isSmithNumber( n ):
        print( indent + 'a Smith number' )

    # base-k Smith numbers
    for i in range( 2, 10 ):
        if isBaseKSmithNumber( n, i ):
            print( indent + 'a base-' + str( i ) + ' Smith number' )

    # order-k Smith numbers
    for i in range( 2, 11 ):
        if isOrderKSmithNumber( n, i ):
            print( indent + 'an order-' + str( i ) + ' Smith number' )

    # polydivisible
    if isPolydivisible( n ):
        print( indent + 'polydivisible' )

    # Carol numbers
    result = findInput( n, getNthCarolNumber, lambda n: fmul( log10( n ), fdiv( 5, 3 ) ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Carol number' )

    # Kynea numbers
    result = findInput( n, getNthKyneaNumber, lambda n: fmul( log10( n ), fdiv( 5, 3 ) ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Kynea number' )

    # Leonardo numbers
    result = findInput( n, getNthLeonardoNumber, lambda n: fsub( log( n, phi ), fdiv( 1, phi ) ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Leonardo number' )

    # Thabit numbers
    result = findInput( n, getNthThabitNumber, lambda n: fmul( log10( n ), 3.25 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Thabit number' )

    # Carmmichael
    if isCarmichaelNumber( n ):
        print( indent + 'a Carmichael number' )

    # narcissistic
    if isNarcissistic( n ):
        print( indent + 'narcissistic' )

    # PDI
    if isPerfectDigitalInvariant( n ):
        print( indent + 'a perfect digital invariant' )

    # PDDI
    if isPerfectDigitToDigitInvariant( n, 10 ):
        print( indent + 'a perfect digit-to-digit invariant in base 10' )

    # Kaprekar
    if isKaprekarNumber( n ):
        print( indent + 'a Kaprekar number' )

    # automorphic
    if isAutomorphic( n ):
        print( indent + 'automorphic' )

    # trimorphic
    if isTrimorphic( n ):
        print( indent + 'trimorphic' )

    # k-morphic
    for i in range( 4, 11 ):
        if isKMorphic( n, i ):
            print( indent + str( i ) + '-morphic' )

    # bouncy
    if isBouncy( n ):
        print( indent + 'bouncy' )

    # step number
    if isStepNumber( n ):
        print( indent + 'a step number' )

    # Apery numbers
    result = findInput( n, getNthAperyNumber, lambda n: fadd( fdiv( log( n ), 1.5 ), 1 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Apery number' )

    # Delannoy numbers
    result = findInput( n, getNthDelannoyNumber, lambda n: fmul( log10( n ), 1.35 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Delannoy number' )

    # Schroeder numbers
    result = findInput( n, getNthSchroederNumber, lambda n: fmul( log10( n ), 1.6 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Schroeder number' )

    # Schroeder-Hipparchus numbers
    result = findInput( n, getNthSchroederHipparchusNumber, lambda n: fdiv( log10( n ), 1.5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Schroeder-Hipparchus number' )

    # Motzkin numbers
    result = findInput( n, getNthMotzkinNumber, log )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Motzkin number' )

    # Pell numbers
    result = findInput( n, getNthPellNumber, lambda n: fmul( log( n ), 1.2 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Pell number' )

    # Sylvester numbers
    if n > 1:
        result = findInput( n, getNthSylvesterNumber, lambda n: sqrt( sqrt( log( n ) ) ) )

        if result[ 0 ]:
            print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Sylvester number' )

    # partition numbers
    result = findInput( n, getPartitionNumber, lambda n: power( log( n ), 1.56 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' partition number' )

    # menage numbers
    result = findInput( n, getNthMenageNumber, lambda n: fdiv( log10( n ), 1.2 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' menage number' )

    print( )
    print( int( n ), 'has:' )

    # number of digits
    digits = log10( n )

    if isInteger( digits ):
        digits += 1
    else:
        digits = ceil( digits )

    print( indent + str( int( digits ) ) + ' digit' + ( 's' if digits > 1 else '' ) )

    # digit sum
    print( indent + 'a digit sum of ' + str( int( sumDigits( n ) ) ) )

    # digit product
    digitProduct = multiplyDigits( n )

    print( indent + 'a digit product of ' + str( int( digitProduct ) ) )

    # non-zero digit product
    if digitProduct == 0:
        print( indent + 'a non-zero digit product of ' + str( int( multiplyNonzeroDigits( n ) ) ) )

    if not isPrimeFlag and n != 1 and n <= LARGEST_NUMBER_TO_FACTOR:
        # factors
        factors = getFactors( n )
        factorCount = len( factors )
        print( indent + str( factorCount ) + ' prime factor' + ( 's' if factorCount > 1 else '' ) +
               ': ' + ', '.join( [ str( int( i ) ) for i in factors ] ) )

        # number of divisors
        divisorCount = int( getDivisorCount( n ) )
        print( indent + str( divisorCount ) + ' divisor' + ( 's' if divisorCount > 1 else '' ) )

    if n <= LARGEST_NUMBER_TO_FACTOR:
        print( indent + 'a divisor sum of ' + str( int( getSigma( n ) ) ) )
        print( indent + 'a Stern value of ' + str( int( getNthSternNumber( n ) ) ) )
        calkinWilf = getNthCalkinWilf( n )
        print( indent + 'a Calkin-Wilf value of ' + str( int( calkinWilf[ 0 ] ) ) + '/' +
               str( int( calkinWilf[ 1 ] ) ) )
        print( indent + 'a Mobius value of ' + str( int( getNthMobiusNumber( n ) ) ) )
        print( indent + 'a radical of ' + str( int( getRadical( n ) ) ) )
        print( indent + 'a Euler phi value of ' + str( int( getEulerPhi( n ) ) ) )

    print( indent + 'a digital root of ' + str( int( getDigitalRoot( n ) ) ) )

    if hasUniqueDigits( n ):
        print( indent + 'unique digits' )

    print( indent + 'a multiplicative persistence of ' + str( int( getPersistence( n ) ) ) )
    print( indent + 'an Erdos persistence of ' + str( int( getErdosPersistence( n ) ) ) )

    if n > 9 and isIncreasing( n ):
        if not isDecreasing( n ):
            print( indent + 'increasing digits' )
    elif n > 9 and isDecreasing( n ):
        print( indent + 'decreasing digits' )

    print( )

    return n


#*******************************************************************************
#
#  ifOperator
#
#*******************************************************************************

@argValidator( [ DefaultValidator( ), DefaultValidator( ), ComplexValidator( ) ] )
def ifOperator( a, b, c ):
    return a if c else b
