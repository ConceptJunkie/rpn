#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUtils.py
# //
# //  RPN command-line calculator utility functions
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

if six.PY3:
    import builtins
else:
    FileNotFoundError = IOError


def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


import bz2
import contextlib
import os
import pickle
import signal
import sys

from mpmath import arange, fadd, findpoly, floor, identify, im, log10, \
                   mpmathify, nint, nstr, rand

from random import randrange
from functools import reduce

import rpnGlobals as g

from rpnGenerator import RPNGenerator


# //******************************************************************************
# //
# //  getDataPath
# //
# //******************************************************************************

def getDataPath( ):
    if getattr( sys, 'frozen', False ):
        g.dataPath = os.path.dirname( sys.executable )
    else:
        g.dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + g.dataDir


# //******************************************************************************
# //
# //  class DelayedKeyboardInterrupt
# //
# //  http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-being-interrupted-by-keyboardinterrupt-in-py
# //
# //******************************************************************************

class DelayedKeyboardInterrupt( object ):
    """This class is used to mask keyboard interrupts."""
    def __enter__( self ):
        self.signal_received = False
        self.old_handler = signal.getsignal( signal.SIGINT )
        signal.signal( signal.SIGINT, self.handler )

    def handler( self, signal, frame ):
        self.signal_received = ( signal, frame )

    def __exit__( self, type, value, traceback ):
        signal.signal( signal.SIGINT, self.old_handler )

        if self.signal_received:
            self.old_handler( *self.signal_received )


# //******************************************************************************
# //
# //  getMultipleRandoms
# //
# //******************************************************************************

def getMultipleRandoms( n ):
    for i in arange( 0, real( n ) ):
        yield rand( )


# //******************************************************************************
# //
# //  getRandomIntegers
# //
# //******************************************************************************

def getRandomIntegers( n, k ):
    for i in arange( 0, real( k ) ):
        yield randrange( n )


# //******************************************************************************
# //
# //  removeUnderscores
# //
# //******************************************************************************

def removeUnderscores( source ):
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

def downloadOEISSequence( id ):
    keywords = downloadOEISText( id, 'K' ).split( ',' )

    # If oeis.org isn't available, just punt everything
    if keywords == [ '' ]:
        return 0

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
    if six.PY3:
        import urllib.request as urllib2
    else:
        import urllib2

    import re as regex

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'oeis.pckl.bz2', 'rb' ) ) as pickleFile:
            oeisCache = pickle.load( pickleFile )
    except FileNotFoundError:
        oeisCache = { }

    if id in oeisCache:
        oeisItem = oeisCache[ id ]
    else:
        oeisItem = { }

    if char in oeisItem:
        return oeisItem[ char ]

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

    oeisItem[ char ] = result

    oeisCache[ id ] = oeisItem

    if not os.path.isdir( g.dataPath ):
        os.makedirs( g.dataPath )

    with DelayedKeyboardInterrupt( ):
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'oeis.pckl.bz2', 'wb' ) ) as pickleFile:
            pickle.dump( oeisCache, pickleFile )

    return result


# //******************************************************************************
# //
# //  addAliases
# //
# //******************************************************************************

def addAliases( operatorList, operatorAliases ):
    for index, operator in enumerate( operatorList ):
        aliasList = [ key for key in operatorAliases if operator == operatorAliases[ key ] ]

        if operator in g.unitOperators:
            unitInfo = g.unitOperators[ operator ]

            if unitInfo.abbrev != '':
                aliasList.append( unitInfo.abbrev )

            aliasList.extend( unitInfo.aliases )

            aliasList = list( set( aliasList ) )

        if aliasList:
            operatorList[ index ] += ' (' + ', '.join( sorted( aliasList ) ) + ')'


# //******************************************************************************
# //
# //  validateOptions
# //
# //******************************************************************************

def validateOptions( args ):
    if args.hex:
        if args.output_radix != 10 and args.output_radix != 16:
            return False, '-r and -x can\'t be used together'

        if args.octal:
            return False, '-x and -o can\'t be used together'

    if args.octal:
        if args.output_radix != 10 and args.output_radix != 8:
            return False, '-r and -o can\'t be used together'

    if args.output_radix_numerals > 0:
        if args.hex:
            return False, '-R and -x can\'t be used together'

        if args.octal:
            return False, '-R and -o can\'t be used together'

        if args.output_radix != 10:
            return False, '-R and -r can\'t be used together'

        if args.output_radix_numerals < 2:
            return False, 'output radix must be greater than 1'

    if args.comma and args.integer_grouping > 0 :
        return False, 'rpn:  -c can\'t be used with -i'

    if args.output_radix_numerals > 0 and \
       ( args.comma or args.decimal_grouping > 0 or args.integer_grouping > 0 ):
        return False, '-c, -d and -i can\'t be used with -R'

    return True, ''


# //******************************************************************************
# //
# //  validateArguments
# //
# //******************************************************************************

def validateArguments( terms ):
    bracketCount = 0

    for term in terms:
        if term == '[':
            bracketCount += 1
        elif term == ']':
            bracketCount -= 1

    if bracketCount:
        print( 'rpn:  mismatched brackets (count: {})'.format( bracketCount ) )
        return False

    braceCount = 0

    for term in terms:
        if term == '{':
            braceCount += 1
        elif term == '}':
            braceCount -= 1

    if braceCount:
        print( 'rpn:  mismatched brace (count: {})'.format( braceCount ) )
        return False

    return True


# //******************************************************************************
# //
# //  getCurrentArgList
# //
# //******************************************************************************

def getCurrentArgList( valueList ):
    argList = valueList

    for i in range( 0, g.nestedListLevel ):
        argList = argList[ -1 ]

    return argList


# //******************************************************************************
# //
# //  abortArgsNeeded
# //
# //******************************************************************************

def abortArgsNeeded( term, index, argsNeeded ):
    print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
           format( argsNeeded ) + ' argument', end = '' )

    print( 's' if argsNeeded > 1 else '' )


# //******************************************************************************
# //
# //  handleIdentify
# //
# //******************************************************************************

def handleIdentify( result, file=sys.stdout ):
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
# //  printStats
# //
# //******************************************************************************

def printStats( dict, name ):
    index = max( [ key for key in dict ] )

    print( '{:10,} {:23} max: {:14,} ({:,})'.format( len( dict ), name, index, dict[ index ] ) )


# //******************************************************************************
# //
# //  getExpandedFactorList
# //
# //  Takes a list of tuples where each tuple is a prime factor and an exponent
# //  and returns a simple list of prime factors.
# //
# //******************************************************************************

def getExpandedFactorList( factors ):
    factorMap = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return sorted( reduce( lambda x, y: x + y, factorMap, [ ] ) )


# //******************************************************************************
# //
# //  real
# //
# //  Skipping the standard naming convention to keep this name really short.
# //
# //******************************************************************************

def real( n ):
    if isinstance( n, ( list, RPNGenerator ) ):
        return n

    if im( n ) != 0:
        raise ValueError( 'real argument expected ({})'.format( n ) )

    return n


# //******************************************************************************
# //
# //  real_int
# //
# //  Skipping the standard naming convention to keep this name really short.
# //
# //******************************************************************************

def real_int( n ):
    if im( n ) != 0:
        raise ValueError( 'real argument expected ({})'.format( n ) )

    if n != floor( n ):
        raise ValueError( 'integer argument expected ({})'.format( n ) )

    return int( n )


# //******************************************************************************
# //
# //  getMPFIntegerAsString
# //
# //******************************************************************************

def getMPFIntegerAsString( n ):
    if n == 0:
        return '0'
    else:
        return nstr( nint( n ), int( floor( log10( n ) + 10  ) ) )[ : -2 ]


# //******************************************************************************
# //
# //  addEchoArgument
# //
# //******************************************************************************

def addEchoArgument( argument ):
    if isinstance( argument, list ) and len( argument ) == 1:
        g.echoArguments.append( argument[ 0 ] )
    else:
        g.echoArguments.append( argument )

    return argument


# //******************************************************************************
# //
# //  parseNumerals
# //
# //******************************************************************************

def parseNumerals( argument ):
    '''
    '-' is a special character that defines a range from the preceding character
    to the succeeding character.

    Therefore, '-' is not a valid numeral, but really, who would want to do that?
    '''
    result = ''

    previous = ''
    makeRange = False

    for c in argument:
        if c == '-':
            makeRange = True

            if previous == '':
                raise ValueError( 'invalid numeral expression' )
        else:
            if makeRange:

                for c2 in range( ord( previous ) + 1, ord( c ) + 1 ):
                    result += chr( c2 )

                makeRange = False
            else:
                result += c

            previous = c

    if makeRange:
        raise ValueError( 'invalid numeral expression' )

    return result

