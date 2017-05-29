#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnSpecial.py
# //
# //  RPN command-line calculator special operators
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
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

from mpmath import arange, fadd, findpoly, floor, identify, im, log10, \
                   mpmathify, nint, nstr, rand

from random import randrange
from functools import reduce

import rpnGlobals as g

from rpnGenerator import RPNGenerator
from rpnPersistence import cachedFunction
from rpnUtils import real_int


# //******************************************************************************
# //
# //  getMultipleRandoms
# //
# //******************************************************************************

def getMultipleRandoms( n ):
    '''Returns n random numbers.'''
    for i in arange( 0, real_int( n ) ):
        yield rand( )


# //******************************************************************************
# //
# //  getRandomIntegers
# //
# //******************************************************************************

def getRandomIntegers( n, k ):
    '''Returns k random integers between 0 and n-1.'''
    for i in arange( 0, real_int( k ) ):
        yield randrange( n )


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

@cachedFunction( 'oeis' )
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
        data = urllib2.urlopen( 'http://oeis.org/search?q=id%3AA{:06}'.format( id ) + '&fmt=text' ).read( )
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


# //******************************************************************************
# //
# //  downloadOEISTable
# //
# //******************************************************************************

@cachedFunction( 'oeis_table' )
def downloadOEISTable( id ):
    if six.PY3:
        import urllib.request as urllib2
    else:
        import urllib2

    try:
        data = urllib2.urlopen( 'http://oeis.org/A{:06}/b{:06}.txt'.format( id, id ) ).read( )
    except:
        return [ ], False

    import re as regex
    pattern = regex.compile( b'(.*?)\n', regex.DOTALL )
    lines = pattern.findall( data )

    result = [ ]

    for line in lines:
        line = line.decode( 'ascii' )

        if line == '':
            continue

        if line[ 0 ] == '#':
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
        base = [ 'pi', 'e', 'euler' ]
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


