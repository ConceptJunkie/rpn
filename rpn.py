#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpn.py
#//
#//  RPN command-line calculator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

# http://en.wikipedia.org/wiki/Physical_constant

# http://pythonhosted.org//astral/#
# http://stackoverflow.com/questions/14698104/how-to-predict-tides-using-harmonic-constants
# http://rhodesmill.org/pyephem/quick.html
# https://github.com/geopy/geopy

# Schwarzschild Radius - Hmmm... operators that turn one kind of unit into another (e.g., mass -> length)

# The Hubble Constant

# Time dilation
# c:\>rpn 1 0.9999 sqr - sqrt 1/x
# 70.7124459519


import argparse
import sys
import time

from mpmath import *

from rpnDeclarations import *
from rpnOperators import *
from rpnOutput import *
from rpnUtils import *
from rpnVersion import *

import rpnGlobals as g


#//******************************************************************************
#//
#//  evaluate
#//
#//******************************************************************************

def evaluate( terms ):
    valueList = list( )
    index = 1                 # only used for error messages

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in terms:
        if term in g.operatorAliases:
            term = g.operatorAliases[ term ]

        if term in functionOperators:
            if g.creatingFunction:
                g.creatingFunction = False
            else:
                raise ValueError( 'function operators require a function definition' )
        elif g.creatingFunction:
            currentValueList[ -1 ].add( term )
            continue

        currentValueList = getCurrentArgList( valueList )

        try:
            if not evaluateTerm( term, index, currentValueList ):
                valueList = [ 0 ]
                break
        except ValueError as error:
            print( 'rpn:  error:  {0}'.format( error ) )
            valueList = [ 0 ]
            break

        index = index + 1

    return valueList


#//******************************************************************************
#//
#//  handleOutput
#//
#//******************************************************************************

def handleOutput( valueList, identify, findPoly, showTime ):
    if len( valueList ) == 0:
        return

    if isinstance( valueList[ 0 ], FunctionInfo ):
        print( 'rpn:  unexpected end of input in function definition' )
    elif len( valueList ) > 1 or len( valueList ) == 0:
        print( 'rpn:  unexpected end of input' )
    else:
        mp.pretty = True
        result = valueList.pop( )

        if g.comma:
            g.integerGrouping = 3     # override whatever was set on the command-line
            g.leadingZero = False     # this one, too
            g.integerDelimiter = ','
        else:
            g.integerDelimiter = ' '

        if isinstance( result, list ):
            print( formatListOutput( result ) )
        else:
            if isinstance( result, arrow.Arrow ):
                outputString = formatDateTime( result )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                outputString = formatOutput( resultString )

                # handle the units if we are displaying a measurement
                if isinstance( result, Measurement ):
                    outputString += ' ' + formatUnits( result )

            printParagraph( outputString )

            # handle --identify
            if identify:
                handleIdentify( result )

            # handle --find_poly
            if findPoly > 0:
                findPolynomial( result, findPoly )

        saveResult( result )

    if showTime:
        print( '\n%.3f seconds' % time.clock( ) )


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

    # look for help argument before we start setting everything up (because it's faster this way)
    help = False

    for i in range( 0, len( cmd_args ) ):
        if cmd_args[ i ] == 'help':
            help = True
        else:
            if help:
                helpArg = cmd_args[ i ]

    # this hack keeps argparse from interpreting negative numbers with scientific notation as flags
    for i, arg in enumerate( cmd_args ):
        if ( len( arg ) > 1 ) and ( arg[ 0 ]  == '-' ) and arg[ 1 ].isdigit( ):
            cmd_args[ i ] = ' ' + arg


    if help:
        parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' +
                                          PROGRAM_VERSION + ': ' + PROGRAM_DESCRIPTION + '\n    ' +
                                          COPYRIGHT_MESSAGE, add_help=False,
                                          formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

        parser.add_argument( 'terms', nargs='*', metavar='term' )
        parser.add_argument( '-l', '--line_length', type=int, action='store', default=g.defaultLineLength )

        args = parser.parse_args( cmd_args )

        loadUnitData( )

        g.operatorAliases.update( operatorAliases )

        printHelp( operators, listOperators, modifiers, helpArg )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=g.defaultAccuracy,  # -1
                         const=g.defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=g.defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=g.defaultDecimalGrouping )
    parser.add_argument( '-D', '--DEBUG', action='store_true' )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=g.defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--identify', action='store_true' )
    parser.add_argument( '-l', '--line_length', type=int, action='store', default=g.defaultLineLength )
    parser.add_argument( '-n', '--numerals', type=str, action='store', default=g.defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=g.defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, action='store', default=g.defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type=int, action='store', default=0 )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-u', '--find_poly', nargs='?', type=int, action='store', default=0, const=1000 )
    parser.add_argument( '-w', '--bitwise_group_size', type=int, action='store', default=g.defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    args = parser.parse_args( cmd_args )

    # now that argparse is done, let's get rid of the spaces we added above
    for i, arg in enumerate( args.terms ):
        if arg[ 0 ]  == ' ':
            args.terms[ i ] = arg[ 1 : ]

    g.operatorAliases.update( operatorAliases )

    if args.help or args.other_help:
        loadUnitData( )

        printHelp( operators, listOperators, modifiers, '' )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    g.bitwiseGroupSize = args.bitwise_group_size
    g.integerGrouping = args.integer_grouping
    g.leadingZero = args.leading_zero

    # handle -a - set precision to be at least 2 greater than output accuracy
    setAccuracy( args.output_accuracy )

    # handle -b
    g.inputRadix = int( args.input_radix )

    # handle -c
    g.comma = args.comma

    # handle -d
    g.decimalGrouping = args.decimal_grouping

    # handle -D
    if args.DEBUG:
        g.debugMode = True

    # handle -l
    g.lineLength = args.line_length

    # handle -n
    g.numerals = args.numerals

    # handle -o
    if args.octal:
        g.outputRadix = 8
        g.leadingZero = True
        g.integerGrouping = 3
        g.bitwiseGroupSize = 9

    # handle -p
    setPrecision( args.precision )

    # handle -r
    if args.output_radix == 'phi':
        g.outputRadix = g.phiBase
    elif args.output_radix == 'fib':
        g.outputRadix = g.fibBase
    else:
        try:
            g.outputRadix = int( args.output_radix )
        except ValueError as error:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return

    # handle -R
    if args.output_radix_numerals > 0:
        g.outputBaseDigits = True
        g.outputRadix = args.output_radix_numerals

    # -r/-R validation
    if g.outputBaseDigits:
        if ( g.outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return
    elif ( ( g.outputRadix != g.phiBase ) and ( g.outputRadix != g.fibBase ) and \
           ( g.outputRadix < 2 or g.outputRadix > 62 ) ):
        print( 'rpn:  output radix must be from 2 to 62, or phi' )
        return

    # handle -x
    if args.hex:
        g.outputRadix = 16
        g.leadingZero = True
        g.integerGrouping = 4
        g.bitwiseGroupSize = 16

    # handle -u and -y:  mpmath wants precision of at least 53 for these functions
    if ( args.identify or args.find_poly > 0 ) and mp.dps < 53:
        mp.dps = 53

    if args.print_options:
        print( '--output_accuracy:  %d' % g.accuracy )
        print( '--input_radix:  %d' % g.inputRadix )
        print( '--comma:  ' + ( 'true' if g.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % g.decimalGrouping )
        print( '--integer_grouping:  %d' % g.integerGrouping )
        print( '--numerals:  ' + g.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision .dps )
        print( '--output_radix:  %d' % g.outputRadix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--time:  ' + ( 'true' if args.time else 'false' ) )
        print( '--find_poly:  %d' % args.find_poly )
        print( '--bitwise_group_size:  %d' % g.bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if g.leadingZero else 'false' ) )
        print( )

    # enter interactive mode if there are no arguments
    if len( args.terms ) == 0:
        if not loadUnitData( ):
            return

        import readline

        readline.parse_and_bind( 'tab: complete' )
        readline.parse_and_bind( 'set editing-mode vi' )

        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )

        g.results.append( None )   # g.results[ 0 ]

        while True:
            g.promptCount += 1

            try:
                line = input( 'rpn (' + str( g.promptCount ) + ')>' )
            except EOFError:
                break

            if line == 'exit':
                break

            terms = line.split( ' ' )

            if validateArguments( terms ):
                valueList = evaluate( terms )

                g.results.append( valueList[ -1 ] )

                handleOutput( valueList, args.identify, args.find_poly, args.time, )
            else:
                g.results.append( 0 )

        return

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    # waiting until we've validated the arguments to do this because it's slow
    if not loadUnitData( ):
        return

    if g.unitsVersion != PROGRAM_VERSION:
        print( 'rpn  units data file version mismatch' )

    valueList = evaluate( args.terms )

    handleOutput( valueList, args.identify, args.find_poly, args.time )

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

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )


