#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnSpecial.py
# //
# //  RPN command-line calculator special operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

import functools
import os
import signal
import sys

from mpmath import arange, cbrt, ceil, e, euler, fabs, fadd, fib, findpoly, floor, \
                   fmul, identify, im, log, log10, mpf, mpmathify, nint, nstr, \
                   pi, rand, root, sqrt

from random import randrange
from functools import reduce

from rpn.rpnFactor import getFactors
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnLexicographic import sumDigits, multiplyDigits, multiplyNonzeroDigits, \
                                 isBaseKPandigital, isPandigital
from rpn.rpnMath import isEven, isInteger, isKthPower, isOdd
from rpn.rpnName import getNumberName, getShortOrdinalName
from rpn.rpnNumberTheory import getDivisorCount, getNthBaseKRepunit, \
                                getNthJacobsthalNumber, getNthLucasNumber
from rpn.rpnPersistence import cachedFunction
from rpn.rpnPolytope import findCenteredPolygonalNumber, findPolygonalNumber, \
                            getNthCenteredPolygonalNumber, getNthPolygonalNumber
from rpn.rpnPrimeUtils import isPrimeNumber
from rpn.rpnUtils import debugPrint, oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         real_int

import rpn.rpnGlobals as g


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
@cachedFunction( 'oeis', True )
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
        return [ int( i ) for i in result.split( ',' ) ]


# //******************************************************************************
# //
# //  downloadOEISText
# //
# //******************************************************************************

def downloadOEISText( id, char, addCR = False ):
    '''Downloads, formats and caches text data from oeis.org.'''
    if six.PY3:
        import urllib.request as urllib2
    else:
        import urllib2

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
@cachedFunction( 'oeis_table', True )
def downloadOEISTable( id ):
    if six.PY3:
        import urllib.request as urllib2
    else:
        import urllib2

    try:
        data = urllib2.urlopen( 'http://oeis.org/A{:06}/b{:06}.txt'.format( int( id ), int( id ) ) ).read( )
    except:
        return [ ], False

    import re as regex
    pattern = regex.compile( b'(.*?)[\n]', regex.DOTALL )
    lines = pattern.findall( data )

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


def getRandomNumber( ):
    return rand( )

@oneArgFunctionEvaluator( )
def getRandomInteger( n ):
    return randrange( n )


# //******************************************************************************
# //
# //  findInput
# //
# //******************************************************************************

def findInput( value, func, estimator ):
    guess1 = floor( estimator( value ) )

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
        guess2 += delta

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

    if n > 0:
        print( indent + 'positive' )
    elif n < 0:
        print( indent + 'negative' )

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

    guess = findPolygonalNumber( n, 3 )

    if getNthPolygonalNumber( guess, 3 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' triangular number' )

    guess = findPolygonalNumber( n, 5 )

    if getNthPolygonalNumber( guess, 5 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' pentagonal number' )

    guess = findPolygonalNumber( n, 6 )

    if getNthPolygonalNumber( guess, 6 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' hexagonal number' )

    guess = findPolygonalNumber( n, 7 )

    if getNthPolygonalNumber( guess, 7 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' heptagonal number' )

    guess = findPolygonalNumber( n, 8 )

    if getNthPolygonalNumber( guess, 8 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' octagonal number' )

    guess = findPolygonalNumber( n, 9 )

    if getNthPolygonalNumber( guess, 9 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' nonagonal number' )

    guess = findPolygonalNumber( n, 10 )

    if getNthPolygonalNumber( guess, 10 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' decagonal number' )

    #for i in range( 11, 101 ):
    #    if getNthPolygonalNumber( findPolygonalNumber( n, i ), i ) == n:
    #        print( indent + str( i ) + '-gonal' )

    guess = findCenteredPolygonalNumber( n, 3 )

    if getNthCenteredPolygonalNumber( guess, 3 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered triangular' )

    guess = findCenteredPolygonalNumber( n, 4 )

    if getNthCenteredPolygonalNumber( guess, 4 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered square number' )

    guess = findCenteredPolygonalNumber( n, 5 )

    if getNthCenteredPolygonalNumber( guess, 5 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered pentagonal number' )

    guess = findCenteredPolygonalNumber( n, 6 )

    if getNthCenteredPolygonalNumber( guess, 6 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered hexagonal number' )

    guess = findCenteredPolygonalNumber( n, 7 )

    if getNthCenteredPolygonalNumber( guess, 7 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered heptagonal number' )

    guess = findCenteredPolygonalNumber( n, 8 )

    if getNthCenteredPolygonalNumber( guess, 8 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered octagonal number' )

    guess = findCenteredPolygonalNumber( n, 9 )

    if getNthCenteredPolygonalNumber( guess, 9 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered nonagonal number' )

    guess - findCenteredPolygonalNumber( n, 10 )

    if getNthCenteredPolygonalNumber( guess, 10 ) == n:
        print( indent + 'the ' + getShortOrdinalName( guess ) + ' centered decagonal number' )

    if isPandigital( n ):
        print( indent + 'pandigital' )

    #for i in range( 4, 21 ):
    #    if isBaseKPandigital( n, i ):
    #        print( indent + 'base ' + str( i ) + ' pandigital' )

    # Fibonacci numbers
    result = findInput( n, fib, lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Fibonacci number' )

    # Lucas numbers
    result = findInput( n, getNthLucasNumber, lambda n: fmul( log10( n ), 5 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Lucas number' )

    # Jacobsthal numbers
    result = findInput( n, getNthJacobsthalNumber, lambda n: fmul( log( n ), 1.6 ) )

    if result[ 0 ]:
        print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' Jacobsthal number' )

    if n > 1:
        for i in range( 2, 21 ):
            result = findInput( n, lambda x: getNthBaseKRepunit( x, i ), lambda n: log( n, i ) )

            if result[ 0 ]:
                print( indent + 'the ' + getShortOrdinalName( result[ 1 ] ) + ' base ' + str( i ) + ' repunit' )

    print( )
    print( int( n ), 'has:' )

    digits = log10( n )

    if isInteger( digits ):
        digits += 1
    else:
        digits = ceil( digits )

    print( indent + str( int( digits ) ) + ' digit' + ( 's' if digits > 1 else '' ) )
    print( indent + 'a digit sum of ' + str( int( sumDigits( n ) ) ) )

    digitProduct = multiplyDigits( n )

    print( indent + 'a digit product of ' + str( int( digitProduct ) ) )

    if digitProduct == 0:
        print( indent + 'a non-zero digit product of ' + str( int( multiplyNonzeroDigits( n ) ) ) )

    if not isPrime and n != 1:
        factors = getFactors( n )
        factorCount = len( factors )
        print( indent + str( factorCount ) + ' prime factor' + ( 's' if factorCount > 1 else '' ) + \
               ': ' + ', '.join( [ str( int( i ) ) for i in factors ] ) )

        divisorCount = int( getDivisorCount( n ) )
        print( indent + str( divisorCount ) + ' divisor' + ( 's' if divisorCount > 1 else '' ) )

    print( )

    return n




