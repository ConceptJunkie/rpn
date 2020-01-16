#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnSpecial.py
# //
# //  rpnChilada special operators
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import functools
import os
import signal
import sys

from mpmath import arange, cbrt, ceil, e, euler, fabs, fadd, fdiv, fib, findpoly, \
                   floor, fmul, fsub, identify, im, inf, log, log10, mpf, mpmathify, \
                   nint, nstr, phi, pi, power, rand, root, sqrt

from random import randrange
from functools import reduce

from rpn.rpnCombinatorics import getNthAperyNumber, getNthDelannoyNumber, getNthMenageNumber, \
                                 getNthMotzkinNumber, getNthPellNumber, getNthSchroederNumber, \
                                 getNthSchroederHipparchusNumber, getNthSylvesterNumber, getPartitionNumber
from rpn.rpnFactor import getFactors
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnLexicographic import getErdosPersistence, getPersistence, \
                                 hasUniqueDigits, isAutomorphic, isBaseKPandigital, isBaseKSmithNumber, \
                                 isDecreasing, isBouncy, isIncreasing, isKaprekar, \
                                 isKMorphic, isNarcissistic, isOrderKSmithNumber, isPandigital, \
                                 isPerfectDigitalInvariant, isPerfectDigitToDigitInvariant, isSmithNumber, \
                                 isStepNumber, isTrimorphic, multiplyDigits, multiplyNonzeroDigits, \
                                 sumDigits
from rpn.rpnMath import isEven, isInteger, isKthPower, isOdd
from rpn.rpnName import getNumberName, getShortOrdinalName
from rpn.rpnNumberTheory import getDigitalRoot, getDivisorCount, getNthDoubleFactorial, getEulerPhi, \
                                getMobius, getNthAlternatingFactorial, getNthBaseKRepunit, getNthCalkinWilf, \
                                getNthCarolNumber, getNthFactorial, getNthFibonorial, getNthHyperfactorial, \
                                getNthJacobsthalNumber, getNthKFibonacciNumber, getNthKyneaNumber, \
                                getNthLeonardoNumber, getNthLucasNumber, getNthMersenneExponent, \
                                getNthMersennePrime, getNthPadovanNumber, getNthPerfectNumber, \
                                getNthRieselNumber, getNthSubfactorial, getNthStern, getNthSuperfactorial, \
                                getNthThabitNumber, getRadical, getSigma, isAbundant, isAchillesNumber, \
                                isAntiharmonic, isCarmichaelNumber, isDeficient, isFriendly, \
                                isKHyperperfect, isKPerfect, isPernicious, isPolydivisible, isPowerful, \
                                isPronic, isRough, isRuthAaronNumber, isSemiprime, isSmooth, isSphenic, \
                                isSquareFree, isUnusual
from rpn.rpnPersistence import cachedFunction, cachedOEISFunction
from rpn.rpnPolytope import findCenteredPolygonalNumber, findPolygonalNumber, \
                            getNthCenteredPolygonalNumber, getNthPolygonalNumber
from rpn.rpnPrimeUtils import getPrimes, isPrimeNumber
from rpn.rpnUtils import debugPrint, oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         real_int

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  getRandomNumber
# //
# //******************************************************************************

def getRandomNumber( ):
    return rand( )


# //******************************************************************************
# //
# //  getRandomInteger
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getRandomInteger( n ):
    return randrange( n )


# //******************************************************************************
# //
# //  getMultipleRandoms
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getMultipleRandoms( n ):
    '''Returns n random numbers.'''
    for i in arange( 0, real_int( n ) ):
        yield rand( )

@oneArgFunctionEvaluator( )
def getMultipleRandomsGenerator( n ):
        return RPNGenerator.createGenerator( getMultipleRandoms, n )


# //******************************************************************************
# //
# //  getRandomIntegers
# //
# //******************************************************************************

def getRandomIntegers( n, k ):
    '''Returns k random integers between 0 and n-1.'''
    for i in arange( 0, real_int( k ) ):
        yield randrange( n )

@twoArgFunctionEvaluator( )
def getRandomIntegersGenerator( n, k ):
    return RPNGenerator.createGenerator( getRandomIntegers, [ n, k ] )


# //******************************************************************************
# //
# //  removeUnderscores
# //
# //******************************************************************************

def removeUnderscores( source ):
    '''This function replaces the underscores in a string with spaces, and is
    used for formatting unit output.'''
    result = ''

    for c in source:
        if c == '_':
            result += ' '
        else:
            result += c

    return result


# //******************************************************************************
# //
# //  downloadOEISSequence
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedOEISFunction( 'oeis', overrideIgnore=True )
def downloadOEISSequence( id ):
    '''Downloads and formats data from oeis.org.'''
    keywords = downloadOEISText( id, 'K' ).split( ',' )

    # If oeis.org isn't available, just punt everything
    if keywords == [ '' ]:
        return 0

    result, success = downloadOEISTable( id )

    if success:
        return result

    if 'nonn' in keywords:
        result = downloadOEISText( id, 'S' )
        result += downloadOEISText( id, 'T' )
        result += downloadOEISText( id, 'U' )
    else:
        result = downloadOEISText( id, 'V' )
        result += downloadOEISText( id, 'W' )
        result += downloadOEISText( id, 'X' )

    if 'cons' in keywords:
        offset = int( downloadOEISText( id, 'O' ).split( ',' )[ 0 ] )
        result = ''.join( result.split( ',' ) )
        return mpmathify( result[ : offset ] + '.' + result[ offset : ] )
    else:
        #return [ mpmathify( i ) for i in result.split( ',' ) ]
        return [ int( i ) for i in result.split( ',' ) ]


# //******************************************************************************
# //
# //  downloadOEISText
# //
# //******************************************************************************

def downloadOEISText( id, char, addCR = False ):
    '''Downloads, formats and caches text data from oeis.org.'''
    import urllib.request as urllib2
    import re as regex

    try:
        data = urllib2.urlopen( 'http://oeis.org/search?q=id%3AA{:06}'.format( int( id ) ) + '&fmt=text' ).read( )
    except:
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
def downloadOEISComment( n ):
    return downloadOEISText( real_int( n ), 'C', True )

@oneArgFunctionEvaluator( )
def downloadOEISExtra( n ):
    return downloadOEISText( real_int( n ), 'E', True )

@oneArgFunctionEvaluator( )
def downloadOEISName( n ):
    return downloadOEISText( real_int( n ), 'N', True )

@oneArgFunctionEvaluator( )
def downloadOEISOffset( n ):
    return int( downloadOEISText( real_int( n ), 'O' ).split( ',' )[ 0 ] )


# //******************************************************************************
# //
# //  downloadOEISTable
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def downloadOEISTable( id ):
    import urllib.request as urllib2

    try:
        data = urllib2.urlopen( 'http://oeis.org/A{:06}/b{:06}.txt'.format( int( id ), int( id ) ) ).read( )
    except:
        print( 'HTTP access to oeis.org failed', file=sys.stderr )
        return [ ], False

    import re as regex
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


# //******************************************************************************
# //
# //  handleIdentify
# //
# //******************************************************************************

def handleIdentify( result, file=sys.stdout ):
    '''Calls the mpmath identify function to try to identify a constant.'''
    formula = identify( result )

    if formula is None:
        base = [ 'pi', 'e', 'euler', 'sqrt(pi)', 'phi' ]
        formula = identify( result, base )

    if formula is None:
        print( '    = [formula cannot be found]', file=file )
    else:
        print( '    = ' + formula, file=file )


# //******************************************************************************
# //
# //  findPolynomial
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def findPolynomial( n, k ):
    '''Calls the mpmath findpoly function to try to identify a polynomial of
    degree <= k for which n is a zero.'''
    poly = findpoly( n, int( k ) )

    if poly is None:
        poly = findpoly( n, int( k ), tol = 1e-10 )

    if poly is None:
        poly = findpoly( n, int( k ), tol = 1e-7 )

    if poly is None:
        return [ 0 ]
    else:
        return poly


# //******************************************************************************
# //
# //  generateUUID
# //
# //******************************************************************************

def generateUUID( ):
    '''Generates a UUID that uses the current machine's MAC address and the
    current time as seeds.'''
    import uuid

    return str( uuid.uuid1( ) )


# //******************************************************************************
# //
# //  generateRandomUUID
# //
# //******************************************************************************

def generateRandomUUID( ):
    '''Generates a completely random UUID.'''
    import uuid

    return str( uuid.uuid4( ) )


# //******************************************************************************
# //
# //  findInput
# //
# //******************************************************************************

largestNumberToFactor = power( 10, 50 )

def findInput( value, func, estimator, max=inf ):
    guess1 = floor( estimator( value ) )

    if guess1 > max:
        guess1 = max

    if guess1 < 1:
        guess1 = 1

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

    if guess2 > max:
        guess2 = max

    result = func( guess2 )
    debugPrint( 'findInput func call', guess2 )

    if result == value:
        return True, guess2

    if over:
        comparator = lambda a, b: a > b
    else:
        comparator = lambda a, b: a < b

    while comparator( result, value ):
        delta *= 2
        guess1 = guess2
        guess2 += delta

        if guess2 > max:
            return False, 0

        result = func( guess2 )
        debugPrint( 'findInput func call', guess2 )

        if result == value:
            return True, guess2

    if guess1 > guess2:
        guess1, guess2 = int( guess2 ), int( guess1 )
    else:
        guess1, guess2 = int( guess1 ), int( guess2 )

    debugPrint( 'guesses:', guess1, guess2 )

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


# //******************************************************************************
# //
# //  describeInteger
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def describeInteger( n ):
    if n < 1:
        raise ValueError( "'describe' requires a positive integer argument" )

    indent = ' ' * 4

    print( )
    print( real_int( n ), 'is:' )

    if isOdd( n ):
        print( indent + 'odd' )
    elif isEven( n ):
        print( indent + 'even' )

    if isPrimeNumber( n ):
        isPrime = True
        print( indent + 'prime' )
    elif n > 3:
        isPrime = False
        print( indent + 'composite' )
    else:
        isPrime = False

    if isKthPower( n, 2 ):
        print( indent + 'the ' + getShortOrdinalName( sqrt( n ) ) + ' square number' )

    if isKthPower( n, 3 ):
        print( indent + 'the ' + getShortOrdinalName( cbrt( n ) ) + ' cube number' )

    for i in arange( 4, fadd( ceil( log( fabs( n ), 2 ) ), 1 ) ):
        if isKthPower( n, i ):
            print( indent + 'the ' + getShortOrdinalName( root( n, i ) ) + ' ' + \
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

    #if n > 1:
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
    guess - findCenteredPolygonalNumber( n, 10 )

    if getNthCenteredPolygonalNumber( guess, 10 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered decagonal number' )

    # pandigital
    if isPandigital( n ):
        print( indent + 'pandigital' )

    #for i in range( 4, 21 ):
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
            result = findInput( n, lambda x: getNthBaseKRepunit( x, i ), lambda n: log( n, i ) )

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

    ## perfect number
    result = findInput( n, getNthPerfectNumber, lambda n: fmul( log( log( n ) ), 2.6 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' perfect number' )

    # Mersenne exponent
    result = findInput( n, getNthMersenneExponent, lambda n: fmul( log( n ), 2.7 ), max=50 )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Mersenne exponent' )

    if not isPrime and n != 1 and n <= largestNumberToFactor:
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

    # Riesel numbers
    result = findInput( n, getNthRieselNumber, lambda n: fmul( log( n ), 1.25 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Riesel number' )

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
    if isKaprekar( n ):
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
    result = findInput( n, getNthMotzkinNumber, lambda n: log( n ) )

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

    if not isPrime and n != 1 and n <= largestNumberToFactor:
        # factors
        factors = getFactors( n )
        factorCount = len( factors )
        print( indent + str( factorCount ) + ' prime factor' + ( 's' if factorCount > 1 else '' ) + \
               ': ' + ', '.join( [ str( int( i ) ) for i in factors ] ) )

        # number of divisors
        divisorCount = int( getDivisorCount( n ) )
        print( indent + str( divisorCount ) + ' divisor' + ( 's' if divisorCount > 1 else '' ) )

    if n <= largestNumberToFactor:
        print( indent + 'a sum of divisors of ' + str( int( getSigma( n ) ) ) )
        print( indent + 'a Stern value of ' + str( int( getNthStern( n ) ) ) )
        calkin_wilf = getNthCalkinWilf( n )
        print( indent + 'a Calkin-Wilf value of ' + str( int( calkin_wilf[ 0 ] ) ) + '/' + str( int( calkin_wilf[ 1 ] ) ) )
        print( indent + 'a Mobius value of ' + str( int( getMobius( n ) ) ) )
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

