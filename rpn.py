#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpn.py
# //
# //  RPN command-line calculator
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

from mpmath import mp

import argparse
import sys
import time

from mpmath import nan, nstr

from rpnAliases import operatorAliases
from rpnDateTime import RPNDateTime
from rpnGenerator import RPNGenerator
from rpnMeasurement import RPNMeasurement

from rpnOperators import checkForVariable, constants, evaluateTerm, functionOperators, \
                         listOperators, loadUnitNameData, modifiers, operators, \
                         RPNFunction, RPNVariable, saveResult, setAccuracy, \
                         setPrecision

from rpnOutput import formatDateTime, formatListOutput, formatOutput, formatUnits, \
                      printHelp, printHelpModeHelp, printTitleScreen

from rpnPersistence import flushDirtyCaches

from rpnUtils import getCurrentArgList, getDataPath, handleIdentify, \
                     validateArguments, validateOptions

from rpnVersion import PROGRAM_VERSION_STRING, COPYRIGHT_MESSAGE

import rpnGlobals as g

if not six.PY3:
    g.dataDir = "rpndata2"


# //******************************************************************************
# //
# //  lookAhead
# //
# //******************************************************************************

def lookAhead( iterable ):
    """
    Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter( iterable )
    last = next( it )

    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val

    # Report the last value.
    yield last, False


# //******************************************************************************
# //
# //  evaluate
# //
# //******************************************************************************

def evaluate( terms ):
    """
    This is the core function in rpn that evaluates the terms to be
    calculated.  terms are put into a stack, and popped off one at a time
    when evaluated.  When an operator is popped off and evaluated, the results
    get pushed back on to the stack for further processing, or ultimately,
    output.
    """
    valueList = list( )
    index = 1                 # only used for error messages

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term, hasMore in lookAhead( terms ):
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
            if not evaluateTerm( term, index, currentValueList, not hasMore ):
                valueList = [ nan ]
                break
        except ValueError as error:
            print( 'rpn:  error:  {0}'.format( error ) )
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


# //******************************************************************************
# //
# //  handleOutput
# //
# //******************************************************************************

def handleOutput( valueList ):
    """
    Once the evaluation of terms is complete, the results need to be
    translated into output.  It is expected there will be a single result,
    otherwise an error is thrown because the expression was incomplete.

    If the result is a list or a generator, special formatting turns those
    into text output.  Date-time values and measurements also require special
    formatting.
    """
    if valueList is None:
        return

    if isinstance( valueList[ 0 ], RPNFunction ):
        print( 'rpn:  unexpected end of input in function definition' )
    elif len( valueList ) != 1:
        print( 'rpn:  unexpected end of input' )
    else:
        mp.pretty = True
        result = valueList.pop( )

        if result is nan:
            return

        if g.comma:
            g.integerGrouping = 3     # override whatever was set on the command-line
            g.leadingZero = False     # this one, too
            g.integerDelimiter = ','
        else:
            g.integerDelimiter = ' '

        if isinstance( result, RPNGenerator ):
            formatListOutput( result.getGenerator( ) )
        elif isinstance( result, list ):
            formatListOutput( result )
        else:
            if isinstance( result, str ):
                result = checkForVariable( result )

            if isinstance( result, RPNVariable ):
                result = result.getValue( )

            if isinstance( result, RPNDateTime ):
                outputString = formatDateTime( result )
            elif isinstance( result, str ):
                outputString = result
            else:
                # output the answer with all the extras according to command-line arguments

                # handle the units if we are displaying a measurement
                if isinstance( result, RPNMeasurement ):
                    outputString = formatOutput( nstr( result.getValue( ), mp.dps ) )
                    outputString += ' ' + formatUnits( result )
                else:
                    outputString = formatOutput( nstr( result, mp.dps ) )

            print( outputString )

            # handle --identify
            if g.identify:
                handleIdentify( result )

        saveResult( result )

    if g.timer or g.tempTimerMode:
        print( '\n{:.3f} seconds'.format( time.process_time( ) - g.startTime ) )


# //******************************************************************************
# //
# //  enterInteractiveMode
# //
# //******************************************************************************

def enterInteractiveMode( ):
    """
    If rpn is launched with no expression, then it goes into interactive
    mode, where it will continue to evaluate new expressions input until
    the 'exit' command.
    """
    try:
        import readline
    except ImportError:
        import pyreadline as readline

    readline.parse_and_bind( 'tab: complete' )
    readline.parse_and_bind( 'set editing-mode vi' )

    printTitleScreen( g.PROGRAM_NAME, g.PROGRAM_DESCRIPTION )

    g.results.append( None )   # g.results[ 0 ]

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
            line = input( 'rpn (' + str( g.promptCount ) + ')>' )
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
                g.startTime = time.process_time( )

            if validateArguments( terms ):
                valueList = evaluate( terms )

                g.results.append( valueList[ -1 ] )

                handleOutput( valueList )
            else:
                g.results.append( 0 )


# //******************************************************************************
# //
# //  enterHelpMode
# //
# //******************************************************************************

def enterHelpMode( terms ):
    """
    When using rpn interactively, help is a special mode, which allows the user
    to navigate the help contents with much fewer keystrokes than having to
    invoke help over and over.
    """
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
                printHelp( operators, constants, listOperators, modifiers, term, True )


# //******************************************************************************
# //
# //  rpn
# //
# //******************************************************************************

def rpn( cmd_args ):
    """
    This is the main function which processes the command-line arguments,
    handling both options and the expression to evaluate.   This function is
    mainly concerned with parsing and handling the command-line options.

    It finally calls evaluate( ) with the expression to be calculated, and
    returns the results, which can be formatted for output or used in another
    way (such as the unit test functionality).
    """
    # initialize globals
    g.debugMode = False
    g.outputRadix = 10

    getDataPath( )

    # look for help argument before we start setting everything up (because it's faster this way)
    help = False
    helpArg = ''

    for i in range( 0, len( cmd_args ) ):
        if cmd_args[ i ] == 'help':
            help = True
        else:
            if help:
                helpArg = cmd_args[ i ]

    if help:
        parser = argparse.ArgumentParser( prog = g.PROGRAM_NAME, description = g.PROGRAM_NAME +
                                          PROGRAM_VERSION_STRING + g.PROGRAM_DESCRIPTION + '\n    ' +
                                          COPYRIGHT_MESSAGE, add_help = False,
                                          formatter_class = argparse.RawTextHelpFormatter,
                                          prefix_chars = '-' )

        parser.add_argument( 'terms', nargs = '*', metavar = 'term' )
        parser.add_argument( '-l', '--line_length', type = int, action = 'store',
                             default = g.defaultLineLength )

        args = parser.parse_args( cmd_args )

        loadUnitNameData( )

        g.operatorAliases.update( operatorAliases )

        printHelp( operators, constants, listOperators, modifiers, helpArg )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog = g.PROGRAM_NAME, description = g.PROGRAM_NAME +
                                      PROGRAM_VERSION_STRING + g.PROGRAM_DESCRIPTION + '\n    ' +
                                      COPYRIGHT_MESSAGE, add_help = False,
                                      formatter_class = argparse.RawTextHelpFormatter,
                                      prefix_chars = '-' )

    parser.add_argument( '-a', '--output_accuracy', nargs = '?', type = int, action = 'store',
                         default = g.defaultOutputAccuracy, const = g.defaultOutputAccuracy )
    parser.add_argument( '-b', '--input_radix', type = str, action = 'store',
                         default = g.defaultInputRadix )
    parser.add_argument( '-c', '--comma', action = 'store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs = '?', type = int, action = 'store',
                         default = 0, const = g.defaultDecimalGrouping )
    parser.add_argument( '-D', '--DEBUG', action = 'store_true' )
    parser.add_argument( '-e', '--profile', action = 'store_true' )
    parser.add_argument( '-g', '--integer_grouping', nargs = '?', type = int, action = 'store',
                         default = 0, const = g.defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action = 'store_true' )
    parser.add_argument( '-i', '--identify', action = 'store_true' )
    parser.add_argument( '-l', '--line_length', type = int, action = 'store',
                         default = g.defaultLineLength )
    parser.add_argument( '-n', '--numerals', type = str, action = 'store', default = g.defaultNumerals )
    parser.add_argument( '-o', '--octal', action = 'store_true' )
    parser.add_argument( '-p', '--precision', type = int, action = 'store', default = g.defaultPrecision )
    parser.add_argument( '-r', '--output_radix', type = str, action = 'store',
                         default = g.defaultOutputRadix )
    parser.add_argument( '-R', '--output_radix_numerals', type = int, action = 'store', default = 0 )
    parser.add_argument( '-s', '--list_format_level', nargs = '?', type = int, action = 'store', default = 0,
                         const = g.defaultListFormatLevel )
    parser.add_argument( '-t', '--timer', action = 'store_true' )
    parser.add_argument( '-v', '--verbose', action = 'store_true' )
    parser.add_argument( '-w', '--bitwise_group_size', type = int, action = 'store',
                         default = g.defaultBitwiseGroupSize )
    parser.add_argument( '-x', '--hex', action = 'store_true' )
    parser.add_argument( '-z', '--leading_zero', action = 'store_true' )
    parser.add_argument( '-!', '--print_options', action = 'store_true' )
    parser.add_argument( '-?', '--other_help', action = 'store_true' )

    # pull out the options and the terms
    options = [ ]
    terms = [ ]

    for i, arg in enumerate( cmd_args ):
        if ( len( arg ) > 1 ) and ( arg[ 0 ] == '-' ):
            if arg[ 1 ].isdigit( ):     # a negative number, not an option
                terms.append( arg )
            else:
                options.append( arg )
        else:
            terms.append( arg )

    # OK, let's parse and validate the options
    args = parser.parse_args( options )

    g.operatorAliases.update( operatorAliases )

    if args.help or args.other_help:
        loadUnitNameData( )

        printHelp( operators, constants, listOperators, modifiers, '' )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

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

    # handle -i
    g.identify = args.identify

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
    elif args.output_radix == 'fac' or args.output_radix == '!':
        g.outputRadix = g.facBase
    elif args.output_radix == 'fac2' or args.output_radix == 'double_fac' or args.output_radix == '!!':
        g.outputRadix = g.doublefacBase
    elif args.output_radix == 'square' or args.output_radix == 'sqr':
        g.outputRadix = g.squareBase
    elif args.output_radix == 'lucas':
        g.outputRadix = g.lucasBase
    elif args.output_radix == 'triangular' or args.output_radix == 'tri':
        g.outputRadix = g.triangularBase
    elif args.output_radix == 'primorial':
        g.outputRadix = g.primorialBase
    elif args.output_radix == 'e':
        g.outputRadix = g.eBase
    elif args.output_radix == 'pi':
        g.outputRadix = g.piBase
    elif args.output_radix == 'sqrt2':
        g.outputRadix = g.sqrt2Base
    else:
        try:
            # if g.outputRadix was already set (e.g., by -o) then we don't want to override it
            if g.outputRadix == 10:
                g.outputRadix = int( args.output_radix )
        except ValueError:
            print( 'rpn:  can\'t interpret output radix \'%s\' as a number' % args.output_radix )
            return [ nan ]

    # handle -R
    if args.output_radix_numerals > 0:
        g.outputBaseDigits = True
        g.outputRadix = args.output_radix_numerals

    # -r/-R validation
    if g.outputBaseDigits:
        if ( g.outputRadix < 2 ):
            print( 'rpn:  output radix must be greater than 1' )
            return [ nan ]
    elif ( ( g.outputRadix < g.maxSpecialBase ) or ( g.outputRadix == 0 ) or
           ( g.outputRadix == 1 ) or ( g.outputRadix > 62 ) ):
        print( 'rpn:  output radix must be from 2 to 62, fib, phi, fac, doublefac, square, lucas' )
        return [ nan ]

    # handle -s
    g.listFormatLevel = args.list_format_level

    # handle -t
    g.timer = args.timer

    # handle -v
    g.verbose = args.verbose

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
        print( '--output_accuracy:  %d' % g.outputAccuracy )
        print( '--input_radix:  %d' % g.inputRadix )
        print( '--comma:  ' + ( 'true' if g.comma else 'false' ) )
        print( '--decimal_grouping:  %d' % g.decimalGrouping )
        print( '--integer_grouping:  %d' % g.integerGrouping )
        print( '--line_length:  %d' % g.lineLength )
        print( '--numerals:  ' + g.numerals )
        print( '--octal:  ' + ( 'true' if args.octal else 'false' ) )
        print( '--precision:  %d' % args.precision )
        print( '--output_radix:  %d' % g.outputRadix )
        print( '--output_radix_numerals:  %d' % args.output_radix_numerals )
        print( '--list_format_level:  %d' % g.listFormatLevel )
        print( '--timer:  ' + ( 'true' if args.timer else 'false' ) )
        print( '--verbose:  ' + ( 'true' if g.verbose else 'false' ) )
        print( '--bitwise_group_size:  %d' % g.bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if g.leadingZero else 'false' ) )
        print( )

    # enter interactive mode if there are no arguments
    if not terms:
        if not loadUnitNameData( ):
            return

        enterInteractiveMode( )
        return

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( terms ):
        return

    # waiting until we've validated the arguments to do this because it's slow
    if not loadUnitNameData( ):
        return

    if g.timer:
        g.startTime = time.process_time( )

    return evaluate( terms )


# //******************************************************************************
# //
# //  __main__
# //
# //******************************************************************************

if __name__ == '__main__':
    try:
        for arg in sys.argv:
            if arg == '-e':
                import profile
                profile.run( 'handleOutput( rpn( sys.argv[ 1 : ] ) )' )

        handleOutput( rpn( sys.argv[ 1 : ] ) )
        flushDirtyCaches( )
    except ValueError as error:
        print( '\nrpn:  value error:  {0}'.format( error ) )

        if g.debugMode:
            raise
        else:
            sys.exit( 0 )
    except KeyboardInterrupt:
        print( )
        print( 'handling ctrl-c keyboard interrupt...' )
        flushDirtyCaches( )
        sys.exit( 0 )

