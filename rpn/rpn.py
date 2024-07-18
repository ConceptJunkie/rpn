#!/usr/bin/env python

#******************************************************************************
#
#  rpn.py
#
#  rpnChilada - RPN command-line calculator
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  *** NOTE:  Don't run this file directly.  Use ../rpn.py.
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

#  https://en.wikipedia.org/wiki/Medieval_weights_and_measures

#  http://mathworld.wolfram.com/FavardConstants.html
#  How can we create a lambda to produce multiple Favard constants with a single expression?

#  rpn 4 meters meters * is_square

import argparse
import os
import sys
import time
import types

from pathlib import Path
import readline

from mpmath import fneg, im, mp, mpc, mpmathify, nan, nstr, re

from rpn.rpnOperator import checkForVariable

from rpn.time.rpnDateTime import RPNDateTime

from rpn.units.rpnConstantUtils import loadGlobalConstants
from rpn.units.rpnMeasurementClass import RPNMeasurement

from rpn.util.rpnAliases import OPERATOR_ALIASES
from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnUtils import getDataPath

from rpn.time.rpnDateTime import formatDateTime

from rpn.rpnOperators import \
    evaluateTerm, functionOperators, loadUserFunctionsFile, RPNFunction, saveUserFunctionsFile

from rpn.util.rpnOutput import \
    formatListOutput, formatOutput, formatUnits, printHelp, printHelpModeHelp, \
    printInteractiveHelp, printTitleScreen

from rpn.util.rpnPersistence import \
    loadUnitData, loadUnitNameData, loadUserVariablesFile, saveUserVariablesFile, loadUserConfigurationFile, \
    saveResult, saveUserConfigurationFile

from rpn.math.rpnPrimeUtils import checkForPrimeData
from rpn.util.rpnSettings import setAccuracy, setPrecision
from rpn.special.rpnSpecial import handleIdentify
from rpn.math.rpnSpecialBase import specialBaseNames

from rpn.util.rpnUtils import \
    getCurrentArgList, getUserDataPath, parseNumerals, validateArguments, validateOptions

from rpn.rpnVersion import \
    RPN_PROGRAM_NAME, PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_DESCRIPTION, COPYRIGHT_MESSAGE

import rpn.util.rpnGlobals as g

if not hasattr( time, 'time_ns' ):
    from rpn.util.rpnNanoseconds import time_ns
else:
    from time import time_ns


#******************************************************************************
#
#  lookAhead
#
#******************************************************************************

def lookAhead( iterable ):
    '''
    Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    '''
    # Get an iterator and pull the first value.
    i = iter( iterable )
    try:
        last = next( i )
    except StopIteration:
        return

    # Run the iterator to exhaustion (starting from the second value).
    for value in i:
        # Report the *previous* value (more to come).
        yield last, True
        last = value

    # Report the last value.
    yield last, False


#******************************************************************************
#
#  evaluate
#
#******************************************************************************

def evaluate( terms ):
    '''
    This is the core function in rpn that evaluates the terms to be
    calculated.  terms are put into a stack, and popped off one at a time
    when evaluated.  When an operator is popped off and evaluated, the results
    get pushed back on to the stack for further processing, or ultimately,
    output.
    '''
    valueList = [ ]
    index = 1                 # only used for error messages

    # handle a unit operator
    if not g.unitOperators:
        loadUnitData( )
        loadGlobalConstants( )

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term, hasMore in lookAhead( terms ):
        if term in g.aliases:
            term = g.aliases[ term ]

        if term in functionOperators:
            if g.creatingFunction:
                g.creatingFunction = False
            else:
                raise ValueError( 'function operators require a function definition' )

        currentValueList = getCurrentArgList( valueList )

        if g.creatingFunction:
            currentValueList[ -1 ].add( term )
            continue

        try:
            if not evaluateTerm( term, index, currentValueList, not hasMore ):
                valueList = [ nan ]
                break
        except ValueError as error:
            print( f'rpn:  error:  { error }' )
            valueList = [ nan ]
            break

        index = index + 1

    if len( g.echoArguments ) > 0:
        returnValue = list( g.echoArguments )

        if isinstance( valueList, list ) and len( valueList ) == 1:
            returnValue.append( valueList[ 0 ] )
        else:
            returnValue.append( valueList )

        g.echoArguments = [ ]
        return [ returnValue ]

    return valueList


#******************************************************************************
#
#  handleOutput
#
#******************************************************************************

def handleOutput( valueList, indent=0, file=sys.stdout ):
    '''
    Once the evaluation of terms is complete, the results need to be
    translated into output.

    If the result is a list or a generator, special formatting turns those
    into text output.  Date-time values and measurements also require special
    formatting.

    Setting file to an io.StringIO objects allows for 'printing' to a string,
    which is used by makeHelp.py to generate actual rpn output for the examples.
    '''
    if valueList is None:
        return file

    indentString = ' ' * indent

    if len( valueList ) != 1:
        if g.checkForSingleResults:
            print( 'valueList', valueList )
            formatListOutput( valueList )
            raise ValueError( 'unexpected multiple results!' )

        valueList = [ valueList ]

    if isinstance( valueList[ 0 ], RPNFunction ):
        print( indentString + 'rpn:  unexpected end of input in function definition', file=file )
    else:
        mp.pretty = True
        result = valueList.pop( )

        if result is nan:
            return file

        if g.comma:
            g.integerGrouping = 3     # override whatever was set on the command-line
            g.leadingZero = False     # this one, too
            g.integerDelimiter = ','
        else:
            g.integerDelimiter = ' '

        if isinstance( result, types.GeneratorType):
            formatListOutput( result, indent=indent, file=file)
        elif isinstance( result, RPNGenerator ):
            formatListOutput( result.getGenerator( ), indent=indent, file=file )
        elif isinstance( result, list ):
            formatListOutput( result, indent=indent, file=file )
        else:
            # single result
            if isinstance( result, RPNDateTime ):
                outputString = formatDateTime( result )
            elif isinstance( result, str ):
                result = checkForVariable( result )
                outputString = result
            else:
                # output the answer with all the extras according to command-line arguments
                # handle the units if we are displaying a measurement
                if isinstance( result, RPNMeasurement ):
                    outputString = formatOutput( nstr( result.value, g.outputAccuracy, min_fixed=-g.maximumFixed - 1 ) )
                    outputString += ' ' + formatUnits( result )
                # handle a complex output (mpmath type: mpc)
                elif isinstance( result, mpc ):
                    #print( 'result', result, type( result ) )
                    #print( 'im', im( result ), type( im( result ) ) )
                    #print( 're', re( result ), type( re( result ) ) )

                    if im( result ) > 0:
                        outputString = '(' + formatOutput( nstr( mpmathify( re( result ) ),
                                                                 g.outputAccuracy, min_fixed=-g.maximumFixed - 1 ) ) + \
                                       ' + ' + formatOutput( nstr( mpmathify( im( result ) ),
                                                                   g.outputAccuracy,
                                                                   min_fixed=-g.maximumFixed - 1 ) ) + 'j)'
                    elif im( result ) < 0:
                        outputString = '(' + formatOutput( nstr( mpmathify( re( result ) ),
                                                                 g.outputAccuracy, min_fixed=-g.maximumFixed - 1 ) ) + \
                                       ' - ' + formatOutput( nstr( fneg( mpmathify( im( result ) ) ),
                                                                   g.outputAccuracy,
                                                                   min_fixed=-g.maximumFixed - 1 ) ) + 'i)'
                    else:
                        outputString = formatOutput( nstr( re( result ), g.outputAccuracy,
                                                           min_fixed=-g.maximumFixed - 1 ) )
                # otherwise, it's a plain old mpf
                else:
                    outputString = formatOutput( nstr( result, g.outputAccuracy, min_fixed=-g.maximumFixed - 1 ) )

            print( indentString + outputString, file=file )

        # handle --identify
        if g.identify:
            handleIdentify( result, file )

        saveResult( result )

    if g.timer or g.tempTimerMode:
        print( f'\n { indentString }{ ( time_ns( ) - g.startTime ) / 1_000_000_000:.3f} seconds', file=file )

    return file


#******************************************************************************
#
#  enterInteractiveMode
#
#******************************************************************************

def enterInteractiveMode( ):
    '''
    If rpn is launched with no expression, then it goes into interactive
    mode, where it will continue to evaluate new expressions input until
    the 'exit' command.
    '''
    readline.parse_and_bind( 'tab: complete' )
    readline.parse_and_bind( 'set editing-mode vi' )

    printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )

    g.results.append( None )   # g.results[ 0 ]
    g.interactive = True

    while True:
        g.promptCount += 1

        # clear single operation flags
        g.tempCommaMode = False
        g.tempHexMode = False
        g.tempIdentifyMode = False
        g.tempLeadingZeroMode = False
        g.tempOctalMode = False
        g.tempTimerMode = False

        try:
            line = input( 'rpn (' + str( g.promptCount ) + ')> ' )
        except EOFError:
            break

        line = line.strip( )

        if line in [ 'exit', 'quit' ]:
            break

        terms = line.split( ' ' )

        if terms[ 0 ] == 'help':
            enterHelpMode( terms[ 1 : ] )
        else:
            if g.timer or g.tempTimerMode:
                g.startTime = time_ns( )

            #newTerms = preprocessTerms( terms )
            #print( 'newTerms', newTerms )

            if validateArguments( terms ):
                valueList = evaluate( terms )

                g.results.append( valueList[ -1 ] )

                handleOutput( valueList )
            else:
                g.results.append( 0 )


#******************************************************************************
#
#  enterHelpMode
#
#******************************************************************************

def enterHelpMode( terms ):
    '''
    When using rpn interactively, help is a special mode, which allows the user
    to navigate the help contents with much fewer keystrokes than having to
    invoke help over and over.
    '''
    printHelpModeHelp( )

    while True:
        try:
            line = input( 'rpn help>' )
        except EOFError:
            break

        line = line.strip( )

        if line in [ 'exit', 'quit' ]:
            break

        terms = line.split( ' ' )

        if terms[ 0 ] == 'help':
            printHelpModeHelp( )
        elif terms[ 0 ] == 'topics':
            printInteractiveHelp( )
        else:
            for term in terms:
                printHelp( [ term ], interactive=True )


#******************************************************************************
#
#  rpn
#
#******************************************************************************

def rpn( cmdArgs ):
    '''
    This is the main function which processes the command-line arguments,
    handling both options and the expression to evaluate.   This function is
    mainly concerned with parsing and handling the command-line options.

    It finally calls evaluate( ) with the expression to be calculated, and
    returns the results, which can be formatted for output or used in another
    way (such as the unit test functionality).
    '''
    # initialize globals
    g.outputRadix = 10

    # allow unlimited conversion lengths for integers
    sys.set_int_max_str_digits(0)

    # look for help argument before we start setting everything up (because it's faster this way)
    showHelp = False
    helpArgs = [ ]

    for arg in cmdArgs:
        if arg == 'help':
            showHelp = True
        else:
            if showHelp:
                helpArgs.append( arg )

    if showHelp:
        parser = argparse.ArgumentParser( prog = PROGRAM_NAME, description = RPN_PROGRAM_NAME +
                                          ' - ' + PROGRAM_DESCRIPTION + '\n    ' +
                                          COPYRIGHT_MESSAGE, add_help = False,
                                          formatter_class = argparse.RawTextHelpFormatter,
                                          prefix_chars = '-' )

        parser.add_argument( 'terms', nargs = '*', metavar = 'term' )
        parser.add_argument( '-l', '--line_length', type = int, action = 'store',
                             default = g.defaultLineLength )

        args = parser.parse_args( cmdArgs )

        loadUnitNameData( )

        g.aliases.update( OPERATOR_ALIASES )

        printHelp( helpArgs )
        return None

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog = PROGRAM_NAME, description = RPN_PROGRAM_NAME +
                                      ' - ' + PROGRAM_DESCRIPTION + '\n    ' +
                                      COPYRIGHT_MESSAGE, add_help = False,
                                      formatter_class = argparse.RawTextHelpFormatter,
                                      prefix_chars = '-' )

    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, default=g.defaultOutputAccuracy,
                         const=g.defaultOutputAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, default=g.defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, default=0,
                         const=g.defaultDecimalGrouping )
    parser.add_argument( '-D', '--DEBUG', action='store_true' )
    parser.add_argument( '-e', '--profile', action='store_true' )
    parser.add_argument( '-E', '--echo_command', action='store_true' )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, default=0,
                         const=g.defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-I', '--ignore_cache', action='store_true' )
    parser.add_argument( '-k', '--show_timezones', action='store_true' )
    parser.add_argument( '-l', '--line_length', type=int, default=g.defaultLineLength )
    parser.add_argument( '-m', '--maximum_fixed', type=int, default=g.defaultMaximumFixed )
    parser.add_argument( '-n', '--numerals', type=str, default=g.defaultNumerals )
    parser.add_argument( '-o', '--octal', action='store_true' )
    parser.add_argument( '-p', '--precision', type=int, default=g.defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type=str, default=g.defaultOutputRadix )
    parser.add_argument( '-s', '--list_format_level', nargs='?', type=int, default=0,
                         const=g.defaultListFormatLevel )
    parser.add_argument( '-t', '--timer', action='store_true' )
    parser.add_argument( '-T', '--time_limit', nargs='?', type=int, default=0, const=g.timeLimit )
    parser.add_argument( '-V', '--version', action='store_true' )
    parser.add_argument( '-v', '--verbose', action='store_true' )
    parser.add_argument( '-w', '--bitwise_group_size', type = int, default = g.defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action='store_true' )
    parser.add_argument( '-y', '--identify', action='store_true' )
    parser.add_argument( '-z', '--leading_zero', action='store_true' )
    parser.add_argument( '-!', '--print_options', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # pull out the options and the terms
    options = [ ]
    terms = [ ]

    loadUserVariablesFile( )
    loadUserFunctionsFile( )
    loadUserConfigurationFile( )

    if 'yafu_path' in g.userConfiguration and 'yafu_binary' in g.userConfiguration:
        g.useYAFU = True
    else:
        g.useYAFU = False

    for arg in cmdArgs:
        if len( arg ) > 1 :
            if arg[ 0 ] == '$' and arg[ 1 : ] not in g.userVariables:
                raise ValueError( 'undefined user variable referenced: ' + arg )

            if arg[ 0 ] == '@' and arg[ 1 : ] not in g.userFunctions:
                raise ValueError( 'undefined user function referenced: ' + arg )

            if arg[ 0 ] == '-' :
                if arg[ 1 ].isdigit( ):     # a negative number, not an option
                    terms.append( arg )
                elif arg[ 1 ] in ( 'i', 'j' ):  # -i and -j are also numbers
                    terms.append( '-1j' )
                else:
                    options.append( arg )
            else:
                terms.append( arg )
        else:
            terms.append( arg )

    debugPrint( 'terms', terms )
    debugPrint( 'options', options )

    # OK, let's parse and validate the options
    args = parser.parse_args( options )

    g.aliases.update( OPERATOR_ALIASES )

    if args.help or args.other_help:
        loadUnitNameData( )

        printHelp( )
        return None

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return None

    # these are either globals or can be modified by other options (like -x)
    g.bitwiseGroupSize = args.bitwise_group_size
    g.integerGrouping = args.integer_grouping
    g.leadingZero = args.leading_zero

    # handle -a
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

    # handle -e
    g.echo_command = args.echo_command

    # handle -g
    g.integerGrouping = args.integer_grouping

    # handle -i
    g.identify = args.identify

    # handle -I
    g.ignoreCache = args.ignore_cache
    g.refreshOEISCache = args.ignore_cache

    if args.show_timezones:
        g.showTimeZones = True

    # handle -l
    g.lineLength = args.line_length

    # handle -m
    g.maximumFixed = args.maximum_fixed

    # handle -n
    g.numerals = parseNumerals( args.numerals )

    # handle -o
    if args.octal:
        g.outputRadix = 8
        g.leadingZero = True
        g.integerGrouping = 3
        g.bitwiseGroupSize = 9

    # handle -p
    setPrecision( args.precision )

    # handle -r
    if args.output_radix in specialBaseNames:
        g.outputRadix = specialBaseNames[ args.output_radix ]
    else:
        try:
            # if g.outputRadix was already set (e.g., by -o) then we don't want to override it
            if g.outputRadix == 10:
                g.outputRadix = int( args.output_radix )
        except ValueError:
            print( f'rpn:  cannot interpret output radix \'{ args.output_radix }\' as a number' )
            return [ nan ]

    # -r validation
    if ( ( g.outputRadix < g.maxSpecialBase ) or ( g.outputRadix == 0 ) or
         ( g.outputRadix == 1 ) or ( g.outputRadix > 62 ) ):
        print( 'rpn:  output radix must be from 2 to 62, fib, phi, fac, doublefac, square, lucas' )
        return [ nan ]

    # handle -s
    g.listFormatLevel = args.list_format_level

    # handle -t
    g.timer = args.timer

    # handle -T
    g.timeLimit = args.time_limit

    # handle -v
    g.verbose = args.verbose

    # handle -V
    if args.version:
        return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]

    # handle -x
    if args.hex:
        g.outputRadix = 16
        g.leadingZero = True
        g.integerGrouping = 4
        g.bitwiseGroupSize = 16

    # handle -u and -y:  mpmath wants precision of at least 53 for these functions
    if args.identify and mp.dps < 53:
        setAccuracy( 53 )

    if args.print_options:
        print( f'--output_accuracy:   { g.outputAccuracy }' )
        print( f'--input_radix:  { g.inputRadix }' )
        print( f'--comma:  { "true" if g.comma else "false" }' )
        print( f'--decimal_grouping:  { g.decimalGrouping }' )
        print( f'--integer_grouping:  { g.integerGrouping }' )
        print( f'--line_length:  { g.lineLength }' )
        print( f'--numerals:  { g.numerals }' )
        print( f'--octal:  { "true" if args.octal else "false" }' )
        print( f'--precision:  { args.precision }' )
        print( f'--output_radix:  { g.outputRadix }' )
        print( f'--list_format_level:  { g.listFormatLevel }' )
        print( f'--timer:  { "true" if args.timer else "false" }' )
        print( f'--verbose:  { "true" if g.verbose else "false" }' )
        print( f'--bitwise_group_size:  { g.bitwiseGroupSize }' )
        print( f'--hex:  { "true" if args.hex else "false" }' )
        print( f'--identify:  { "true" if args.identify else "false" }' )
        print( f'--leading_zero:  { "true" if g.leadingZero else "false" }' )
        print( f'--ignore_cache:  { "true" if g.ignoreCache else "false" }' )
        print( )

    g.creatingFunction = False

    # enter interactive mode if there are no arguments
    if not terms:
        if not loadUnitNameData( ):
            return None

        enterInteractiveMode( )
        return None

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( terms ):
        return None

    #newTerms = preprocessTerms( terms )
    #print( 'newTerms', newTerms )

    # waiting until we've validated the arguments to do this because it's slow
    if not loadUnitNameData( ):
        return None

    if g.echo_command:
        print( *sys.argv )

    if g.timer:
        g.startTime = time_ns( )

    return evaluate( terms )


#******************************************************************************
#
#  __main__
#
#******************************************************************************

def main( ):
    checkForPrimeData( )

    unitsFile = Path( getUserDataPath( ) + os.sep + 'units.pckl.bz2' )

    g.cwd = os.getcwd( )

    os.chdir( getUserDataPath( ) )     # SkyField doesn't like running in the root directory

    if not unitsFile.is_file( ):
        print( f'unit conversion data files not found in {getDataPath()}' )
        print( 'Please run makeUnits.py to initialize the unit conversion data files.' )
        sys.exit( 0 )

    helpFile = Path( getUserDataPath( ) + os.sep + 'help.pckl.bz2' )

    if not helpFile.is_file( ):
        print( f'help files not found in {getDataPath()}' )
        print( 'Please run makeHelp.py to initialize the help files.' )
        sys.exit( 0 )

    try:
        #for arg in sys.argv:
        #    if arg == '-e':
        #        import profile
        #        profile.run( 'handleOutput( rpn( sys.argv[ 1 : ] ) )' )

        handleOutput( rpn( sys.argv[ 1 : ] ) )

        if g.userVariablesAreDirty:
            saveUserVariablesFile( )

        if g.userFunctionsAreDirty:
            saveUserFunctionsFile( )

        if g.userConfigurationIsDirty:
            saveUserConfigurationFile( )
    except ValueError as error:
        print( f'\nrpn:  value error:  { error }' )

        if g.debugMode:
            raise

        sys.exit( 0 )
    except KeyboardInterrupt:
        print( )
        print( 'handling ctrl-c keyboard interrupt...' )
        sys.exit( 0 )


#******************************************************************************
#
#  __main__
#
#******************************************************************************

if __name__ == '__main__':
    main( )

