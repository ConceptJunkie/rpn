#!/usr/bin/env python

# New idea:  cache OEIS results!

# unfloat, undouble

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

import argparse
import sys

from mpmath import *

from rpnDeclarations import *
from rpnOperators import *
from rpnOutput import *
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

