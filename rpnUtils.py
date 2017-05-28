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


import functools
import os
import sys

from mpmath import arange, fadd, floor, im, log10, mpmathify, nint, nstr

from random import randrange
from functools import reduce

import rpnGlobals as g

from rpnPersistence import cachedFunction
from rpnGenerator import RPNGenerator


# //******************************************************************************
# //
# //  getDataPath
# //
# //******************************************************************************

def getDataPath( ):
    '''Returns the path for the data files.'''
    if getattr( sys, 'frozen', False ):
        g.dataPath = os.path.dirname( sys.executable )
    else:
        g.dataPath = os.path.dirname( os.path.realpath( __file__ ) ) + os.sep + g.dataDir


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
# //  addAliases
# //
# //******************************************************************************

def addAliases( operatorList, operatorAliases ):
    '''Adds the predefined aliases from the operator table into the global alias list.'''
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
    '''Validates arguments for options that take arguments, and also checks for
    options that are mutually exclusive.'''
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
    '''Does some preliminary argument validatation, such as checking fo matching
    braces and braces.'''
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
    '''Issues the error message when an operator is provided with an insufficient
    number of arguments.'''
    print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
           format( argsNeeded ) + ' argument', end = '' )

    print( 's' if argsNeeded > 1 else '' )


# //******************************************************************************
# //
# //  getExpandedFactorList
# //
# //******************************************************************************

def getExpandedFactorList( factors ):
    '''Takes a list of tuples where each tuple is a prime factor and an exponent
    and returns a simple list of prime factors.'''
    factorMap = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return sorted( reduce( lambda x, y: x + y, factorMap, [ ] ) )


# //******************************************************************************
# //
# //  getExpandedFactorListSympy
# //
# //******************************************************************************

def getExpandedFactorListSympy( factors ):
    '''Takes a list of tuples where each tuple is a prime factor and an exponent
    and returns a simple list of prime factors.'''
    result = [ ]

    for key in factors:
        for i in arange( 0, factors[ key ] ):
            result.append( key )

    return sorted( result )


# //******************************************************************************
# //
# //  real
# //
# //  Skipping the standard naming convention to keep this name really short.
# //
# //******************************************************************************

def real( n ):
    '''Validates that a value is real and throws an error if it isn't.'''
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
    '''Validates that a value is a real integer and throws an error if it
    isn't.'''
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
    '''Turns an mpmath mpf integer value into a string for use by lexicographic
    operators.'''
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
    '''Echos the argument in the rpn output while continuing to use it for
    evaluation.'''
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


# //******************************************************************************
# //
# //  oneArgFunctionEvaluator
# //
# //******************************************************************************

#def oneArgFunctionEvaluator( ):
#    def oneArgFunction( func )
#        @functools.wraps( func )
#
#        def
#
#    if isinstance( args, list ):
#        result = [ evaluateOneArgFunction( func, i, level + 1 ) for i in args ]
#    elif isinstance( args, RPNGenerator ):
#        result = RPNGenerator.createChained( args.getGenerator( ), func )
#    else:
#        result = func( args )
#
#    # if this is the 'echo' operator, just return the result
#    if func.__name__ == 'addEchoArgument':
#        return result
#
#    # otherwise, check for arguments to be echoed, and echo them before the result
#    if level == 0 and not g.operatorList and len( g.echoArguments ) > 0:
#        returnValue = list( g.echoArguments )
#        returnValue.append( result )
#        g.echoArguments = [ ]
#        return returnValue
#    else:
#        return result


import signal
import functools

class TimeoutError(Exception): pass

def timeout(seconds, error_message = 'Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return functools.wraps(func)(wrapper)

    return decorated

