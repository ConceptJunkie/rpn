#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnUtils.py
# //
# //  RPN command-line calculator utility functions
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from __future__ import print_function

import six

if six.PY3:
    import builtins

import arrow
import bz2
import contextlib
import math
import os
import pickle
import signal

from mpmath import *
from random import randrange

from rpnDeclarations import *
from rpnUnitClasses import UnitTypeInfo
from rpnVersion import *

from functools import reduce

import rpnGlobals as g


# //******************************************************************************
# //
# //  class DelayedKeyboardInterrupt
# //
# //  http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-being-interrupted-by-keyboardinterrupt-in-py
# //
# //******************************************************************************

class DelayedKeyboardInterrupt( object ):
    def __enter__( self ):
        self.signal_received = False
        self.old_handler = signal.getsignal( signal.SIGINT )
        signal.signal( signal.SIGINT, self.handler )

    def handler( self, signal, frame ):
        self.signal_received = ( signal, frame )

    def __exit__(self, type, value, traceback):
        signal.signal( signal.SIGINT, self.old_handler )

        if self.signal_received:
            self.old_handler( *self.signal_received )


# //******************************************************************************
# //
# //  setAccuracy
# //
# //******************************************************************************

def setAccuracy( n ):
    if n == -1:
        g.outputAccuracy = g.defaultOutputAccuracy
    else:
        g.outputAccuracy = int( n )

    if mp.dps < g.outputAccuracy:
        mp.dps = g.outputAccuracy

    return g.outputAccuracy


# //******************************************************************************
# //
# //  rand_
# //
# //******************************************************************************

def rand_( n ):
    result = [ ]

    for i in arange( 0, n ):
        result.append( rand( ) )

    return result


# //******************************************************************************
# //
# //  randrange_
# //
# //******************************************************************************

def randrange_( n, k ):
    result = [ ]

    for i in arange( 0, k ):
        result.append( randrange( n ) )

    return result


# //******************************************************************************
# //
# //  round
# //
# //******************************************************************************

def round( n, decimals ):
    factor = power( 10, decimals )
    return fdiv( nint( fmul( n, factor ) ), factor )


# //******************************************************************************
# //
# //  loadUnitData
# //
# //******************************************************************************

def loadUnitData( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'units.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitsVersion = pickle.load( pickleFile )
            g.basicUnitTypes.update( pickle.load( pickleFile ) )
            g.unitOperators.update( pickle.load( pickleFile ) )
            g.operatorAliases.update( pickle.load( pickleFile ) )
    except IOError:
        print( 'rpn:  Unable to load unit info data.  Unit conversion will be unavailable.  Run makeUnits.py to make the unit data files.' )
        return False

    return True


# //******************************************************************************
# //
# //  loadHelpData
# //
# //******************************************************************************

def loadHelpData( ):
    if g.helpLoaded:
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.helpVersion = pickle.load( pickleFile )
            g.helpTopics = pickle.load( pickleFile )
            g.operatorHelp = pickle.load( pickleFile )
    except FileNotFoundError:
        print( 'rpn:  Unable to load help file.  Help will be unavailable.  Run makeHelp.py to create the help files.' )
        return

    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_help.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitTypeDict = pickle.load( pickleFile )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit help data.  Run makeUnits.py to make the unit data files.' )
        return False

    g.operatorCategories = set( g.operatorHelp[ key ][ 0 ] for key in g.operatorHelp )

    g.helpLoaded = True

    return True


# //******************************************************************************
# //
# //  loadUnitConversionMatrix
# //
# //******************************************************************************

def loadUnitConversionMatrix( ):
    try:
        with contextlib.closing( bz2.BZ2File( g.dataPath + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) as pickleFile:
            g.unitConversionMatrix.update( pickle.load( pickleFile ) )
    except FileNotFoundError:
        print( 'rpn:  Unable to load unit conversion data.  Unit conversion will be unavailable.  Run makeUnits.py to make the unit data files.' )


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
# //  debugPrint
# //
# //******************************************************************************

def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return


# //******************************************************************************
# //
# //  downloadOEISSequence
# //
# //******************************************************************************

def downloadOEISSequence( id ):
    keywords = downloadOEISText( id, 'K' ).split( ',' )

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
    import urllib.request
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

    data = urllib.request.urlopen( 'http://oeis.org/search?q=id%3AA{:06}'.format( id ) + '&fmt=text' ).read( )

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
# //  convertToBase10
# //
# //******************************************************************************

def convertToBase10( integer, mantissa, inputRadix ):
    result = mpmathify( 0 )
    base = mpmathify( 1 )

    validNumerals = g.numerals[ : inputRadix ]

    for i in range( len( integer ) - 1, -1, -1 ):
        digit = validNumerals.find( integer[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( integer[ i ], inputRadix ) )

        result += digit * base
        base *= inputRadix

    base = fdiv( 1, inputRadix )

    for i in range( 0, len( mantissa ) ):
        digit = validNumerals.find( mantissa[ i ] )

        if digit == -1:
            raise ValueError( 'invalid numeral \'%c\' for base %d' % ( mantissa[ i ], inputRadix ) )

        result += digit * base
        base /= inputRadix

    return result


# //******************************************************************************
# //
# //  parseInputValue
# //
# //  Parse out a time value or a numerical expression and attempt to set the
# //  precision to an appropriate value based on the expression.
# //
# //******************************************************************************

def parseInputValue( term, inputRadix ):
    if isinstance( term, mpf ):
        return term

    innerChars = term[ 1 : -1 ]

    if '/' in innerChars:
        term = term.replace( '/', '-' )
        innerChars = term[ 1 : -1 ]

    if ( '-' in innerChars ) or ( ':' in innerChars ):
        try:
            datetime = arrow.get( term )
            datetime = RPNDateTime( datetime.year, datetime.month, datetime.day, datetime.hour,
                                    datetime.minute, datetime.second, datetime.microsecond,
                                    datetime.tzinfo )
        except:
            raise ValueError( 'error parsing datetime' )

        return datetime

    if term == '0':
        return mpmathify( 0 )

    # ignore commas
    term = ''.join( [ i for i in term if i not in ',' ] )

    if term[ 0 ] == '\\':
        term = term[ 1 : ]
        ignoreSpecial = True
    else:
        ignoreSpecial = False

    if '.' in term:
        if inputRadix == 10:
            newPrecision = len( term ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

            return mpmathify( term )

        decimal = term.find( '.' )
    else:
        decimal = len( term )

    negative = term[ 0 ] == '-'

    if negative:
        start = 1
    else:
        if term[ 0 ] == '+':
            start = 1
        else:
            start = 0

    integer = term[ start : decimal ]
    mantissa = term[ decimal + 1 : ]

    # check for hex, then binary, then octal, otherwise a plain old decimal integer
    if not ignoreSpecial and mantissa == '':
        if integer[ 0 ] == '0':
            if len( integer ) == 1:
                return mpmathify( 0 )

            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                if mp.dps < newPrecision:
                    setAccuracy( newPrecision )

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    setAccuracy( newPrecision )

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        if integer[ 0 ] == '1' and integer[ -1 ] in 'bB':
            # set the precision big enough to handle this value
            newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

            integer = integer[ : -1 ]
            return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                setAccuracy( newPrecision )

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


# //******************************************************************************
# //
# //  convertToBaseN
# //
# //  This handles any integer base as long as there is a big-enough list of
# //  numerals to use.  In practice this ends up being 0-9, a-z, and A-Z, which
# //  allows us to support up to base 62.
# //
# //******************************************************************************

def convertToBaseN( value, base, outputBaseDigits, numerals ):
    if outputBaseDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( numerals ) )

    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( fneg( value ), base, outputBaseDigits, numerals )

    if base == 10:
        return str( value )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    leftDigits = mpmathify( value )

    while leftDigits > 0:
        modulo = fmod( leftDigits, base )

        if outputBaseDigits:
            result.insert( 0, int( modulo ) )
        else:
            result = numerals[ int( modulo ) ] + result

        leftDigits = floor( fdiv( leftDigits, base ) )

    return result


# //******************************************************************************
# //
# //  convertToSpecialBase
# //
# //  This version supports arbitrary bases.  The place value is determined
# //  with the function passed in.
# //
# //******************************************************************************

def convertToSpecialBase( value, baseFunction, outputBaseDigits = False, numerals = g.defaultNumerals ):
    if value == 0:
        return 0

    if value < 0:
        return '-' + convertToBaseN( fneg( value ), base, outputBaseDigits, numerals )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    positionValues = [ ]

    position = 1
    positionValue = baseFunction( position )

    while positionValue <= value:
        positionValues.append( positionValue )

        position += 1
        positionValue = baseFunction( position )

    if outputBaseDigits:
        result = [ ]
    else:
        result = ''

    remaining = value

    while len( positionValues ):
        base = positionValues.pop( )

        digit = floor( fdiv( remaining, base ) )

        if outputBaseDigits:
            result.append( digit )
        else:
            result += numerals[ int( digit ) ]

        remaining = fsub( remaining, fmul( digit, base ) )

    return result


# //******************************************************************************
# //
# //  convertToIterativeBase
# //
# //******************************************************************************

def convertToIterativeBase( value, baseFunction, outputBaseDigits, numerals ):
    return 'fred'


# //******************************************************************************
# //
# //  convertToNonintegerBase
# //
# //******************************************************************************

def convertToNonintegerBase( num, base ):
    epsilon = power( 10, -( mp.dps - 3 ) )
    minPlace = -( floor( mp.dps / log( base ) ) )

    output = ''
    integer = ''

    start = True
    previousPlace = 0
    remaining = num

    originalPlace = 0

    # find starting place
    place = int( floor( log( remaining, base ) ) )

    while remaining > epsilon:
        if place < minPlace:
            break

        if place == -1:
            integer = output
            output = ''

        placeValue = power( base, place )
        value = fdiv( remaining, placeValue )

        value = fmul( value, power( 10, mp.dps - 3 ) )
        value = nint( value )
        value = fdiv( value, power( 10, mp.dps - 3 ) )

        value = floor( value )
        remaining = chop( fsub( remaining, fmul( placeValue, value ) ) )

        output += str( value )[ : -2 ]

        place -= 1

    if place >= 0:
        integer = output + '0' * place
        output = ''

    if integer == '':
        return output, ''
    else:
        return integer, output


# //******************************************************************************
# //
# //  convertToPhiBase
# //
# //******************************************************************************

def convertToPhiBase( num ):
    epsilon = power( 10, -( mp.dps - 3 ) )

    output = ''
    integer = ''

    start = True
    previousPlace = 0
    remaining = num

    originalPlace = 0

    while remaining > epsilon:
        place = int( floor( log( remaining, phi ) ) )

        if start:
            output = '1'
            start = False
            originalPlace = place
        else:
            if place < -( originalPlace + 1 ):
                break

            for i in range( previousPlace, place + 1, -1 ):
                output += '0'

                if ( i == 1 ):
                    integer = output
                    output = ''

            output += '1'

            if place == 0:
                integer = output
                output = ''

        previousPlace = place
        remaining -= power( phi, place )

    if integer == '':
        return output, ''
    else:
        return integer, output


# //******************************************************************************
# //
# //  convertToFibBase
# //
# //  Returns a string with Fibonacci encoding for n (n >= 1).
# //
# //  adapted from https://en.wikipedia.org/wiki/Fibonacci_coding
# //
# //******************************************************************************

def convertToFibBase( value ):
    result = ''

    n = value

    if n >= 1:
        a = 1
        b = 1

        c = fadd( a, b )    # next Fibonacci number
        fibs = [ b ]        # list of Fibonacci numbers, starting with F(2), each <= n

        while n >= c:
            fibs.append( c )  # add next Fibonacci number to end of list
            a = b
            b = c
            c = fadd( a, b )

        for fibnum in reversed( fibs ):
            if n >= fibnum:
                n = fsub( n, fibnum )
                result = result + '1'
            else:
                result = result + '0'

    return result


# //******************************************************************************
# //
# //  convertFractionToBaseN
# //
# //******************************************************************************

def convertFractionToBaseN( value, base, precision, outputBaseDigits ):
    if outputBaseDigits:
        if ( base < 2 ):
            raise ValueError( 'base must be greater than 1' )
    else:
        if not ( 2 <= base <= len( g.numerals ) ):
            raise ValueError( 'base must be from 2 to %d' % len( g.numerals ) )

    if value < 0 or value >= 1.0:
        raise ValueError( 'value (%s) must be >= 0 and < 1.0' % value )

    if base == 10:
        return str( value )

    result = ''

    while value > 0 and precision > 0:
        value = fmul( value, base )

        digit = int( value )

        if len( result ) == g.outputAccuracy:
            if digit >= base // 2:
                digit += 1

            break

        if outputBaseDigits:
            if result != '':
                result += ' '

            result += str( digit )
        else:
            result += g.numerals[ digit ]

        value = fsub( value, digit )
        precision -= 1

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

        if len( aliasList ) > 0:
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

    return True


# //******************************************************************************
# //
# //  evaluateOneListFunction
# //
# //******************************************************************************

def evaluateOneListFunction( func, args ):
    if isinstance( args, list ):
        for arg in args:
            if isinstance( arg, list ) and isinstance( arg[ 0 ], list ):
                return [ evaluateOneListFunction( func, arg ) for arg in args ]

        return func( args )
    else:
        return func( [ args ] )


# //******************************************************************************
# //
# //  evaluateOneArgFunction
# //
# //******************************************************************************

def evaluateOneArgFunction( func, args ):
    if isinstance( args, list ):
        return [ evaluateOneArgFunction( func, i ) for i in args ]
    else:
        return func( args )


# //******************************************************************************
# //
# //  evaluateTwoArgFunction
# //
# //  This seems somewhat non-pythonic...
# //
# //******************************************************************************

def evaluateTwoArgFunction( func, _arg1, _arg2 ):
    if isinstance( _arg1, list ):
        len1 = len( _arg1 )
        if len1 == 1:
            arg1 = _arg1[ 0 ]
            list1 = False
        else:
            arg1 = _arg1
            list1 = True
    else:
        arg1 = _arg1
        list1 = False

    if isinstance( _arg2, list ):
        len2 = len( _arg2 )
        if len2 == 1:
            arg2 = _arg2[ 0 ]
            list2 = False
        else:
            arg2 = _arg2
            list2 = True
    else:
        arg2 = _arg2
        list2 = False

    if list1:
        if list2:
            return [ evaluateTwoArgFunction( func, arg1[ index ], arg2[ index ] ) for index in range( 0, min( len1, len2 ) ) ]
        else:
            return [ evaluateTwoArgFunction( func, i, arg2 ) for i in arg1 ]

    else:
        if list2:
            return [ evaluateTwoArgFunction( func, arg1, j ) for j in arg2 ]
        else:
            return func( arg2, arg1 )


# //******************************************************************************
# //
# //  callers
# //
# //******************************************************************************

callers = [
    lambda func, args: [ func( ) ],
    evaluateOneArgFunction,
    evaluateTwoArgFunction,

    # 3, 4, and 5 argument functions don't recurse with lists more than one level

    lambda func, arg1, arg2, arg3:
        [ func( a, b, c ) for c in arg1 for b in arg2 for a in arg3 ],
    lambda func, arg1, arg2, arg3, arg4:
        [ func( a, b, c, d ) for d in arg1 for c in arg2 for b in arg3 for a in arg4 ],
    lambda func, arg1, arg2, arg3, arg4, arg5:
        [ func( a, b, c, d, e ) for e in arg1 for d in arg2 for c in arg3 for b in arg4 for a in arg5 ],
]


# //******************************************************************************
# //
# //  getExpandedFactorList
# //
# //  Takes a list of tuples where each tuple is a prime factor and an exponent
# //  and returns a simple list of prime factors.
# //
# //******************************************************************************

def getExpandedFactorList( factors ):
    factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return sorted( reduce( lambda x, y: x + y, factors, [ ] ) )


# //******************************************************************************
# //
# //  convertLatLongToNAC
# //
# //  https://en.wikipedia.org/wiki/Natural_Area_Code
# //
# //******************************************************************************

def convertLatLongToNAC( args ):
    if not isinstance( args, list ):
        args = [ args, 0 ]
    elif len( args ) > 0 and isinstance( args[ 0 ], list ):
        return [ convertLatLongToNAC( i ) for i in args ]
    elif len( args ) == 1:
        args.append( 0 )

    numerals = '0123456789BCDFGHJKLMNPQRSTVWXZ'

    if args[ 0 ] > 90.0 or args[ 0 ] < -90.0:
        raise ValueError( '\'natural_area_code\' requires a latitude parameter of -90 to 90' )

    if args[ 1 ] > 180.0 or args[ 1 ] < -180.0:
        raise ValueError( '\'natural_area_code\' requires a longitutde parameter of -180 to 180' )

    lat = fdiv( fadd( args[ 0 ], 90 ), 180 ) * 729000000
    long = fdiv( fadd( args[ 1 ], 180 ), 360 ) * 729000000   # 30 ** 6

    return convertToBaseN( long, 30, False, numerals ) + ' ' + convertToBaseN( lat, 30, False, numerals )

