#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeRPNPrimes.py
#//
#//  RPN command-line calculator prime data generator
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import argparse
import bz2
import contextlib
import pickle
import os
#import pyprimes
import sys
import time

from mpmath import *

from rpnDeclarations import *
from rpnPrimeUtils import *
from rpnUtils import *


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeRPNPrimes'
PROGRAM_DESCRIPTION = 'RPN command-line calculator prime data generator'


#//******************************************************************************
#//
#//  loadTable
#//
#//******************************************************************************

def loadTable( fileName, default ):
    global dataPath

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'rb' ) ) as pickleFile:
            primes = pickle.load( pickleFile )
    except FileNotFoundError:
        primes = default

    return primes


def loadSmallPrimes( ):
    return loadTable( 'small_primes', { 4 : 7 } )


def loadLargePrimes( ):
    return loadTable( 'large_primes', { 1000000 : 15485863 } )


def loadIsolatedPrimes( ):
    return loadTable( 'isolated_primes', { 2 : 23 } )


def loadTwinPrimes( ):
    return loadTable( 'twin_primes', { 3 : 11 } )


def loadBalancedPrimes( ):
    return loadTable( 'balanced_primes', { 2 : 5 } )


def loadDoubleBalancedPrimes( ):
    return loadTable( 'double_balanced_primes', { 1 : getNthDoubleBalancedPrime( 1 ) } )


def loadTripleBalancedPrimes( ):
    return loadTable( 'triple_balanced_primes', { 1 : getNthTripleBalancedPrime( 1 ) } )


def loadSophiePrimes( ):
    return loadTable( 'sophie_primes', { 4 : 11 } )


def loadCousinPrimes( ):
    return loadTable( 'cousin_primes', { 2 : 7 } )


def loadSexyPrimes( ):
    return loadTable( 'sexy_primes', { 2 : 7 } )


def loadSexyTripletPrimes( ):
    return loadTable( 'sexy_triplets', { 2 : 7 } )


def loadSexyQuadrupletPrimes( ):
    return loadTable( 'sexy_quadruplets', { 2 : 11 } )


def loadTripletPrimes( ):
    return loadTable( 'triplet_primes', { 2 : 7 } )


def loadQuadrupletPrimes( ):
    return loadTable( 'quad_primes', { 2 : 11 } )


def loadQuintupletPrimes( ):
    return loadTable( 'quint_primes', { 3 : 11 } )


def loadSextupletPrimes( ):
    return loadTable( 'sext_primes', { 1 : 7 } )


#//******************************************************************************
#//
#//  saveTable
#//
#//******************************************************************************

def saveTable( fileName, var ):
    global dataPath

    with contextlib.closing( bz2.BZ2File( dataPath + os.sep + fileName + '.pckl.bz2', 'wb' ) ) as pickleFile:
        pickle.dump( var, pickleFile )


def saveSmallPrimes( smallPrimes ):
    saveTable( 'small_primes', smallPrimes )


def saveLargePrimes( largePrimes ):
    saveTable( 'large_primes', largePrimes )


def saveIsolatedPrimes( isolatedPrimes ):
    saveTable( 'isolated_primes', isolatedPrimes )


def saveTwinPrimes( twinPrimes ):
    saveTable( 'twin_primes', twinPrimes )


def saveBalancedPrimes( balancedPrimes ):
    saveTable( 'balanced_primes', balancedPrimes )


def saveDoubleBalancedPrimes( doubleBalancedPrimes ):
    saveTable( 'double_balanced_primes', doubleBalancedPrimes )


def saveTripleBalancedPrimes( tripleBalancedPrimes ):
    saveTable( 'triple_balanced_primes', tripleBalancedPrimes )


def saveSophiePrimes( sophiePrimes ):
    saveTable( 'sophie_primes', sophiePrimes )


def saveCousinPrimes( cousinPrimes ):
    saveTable( 'cousin_primes', cousinPrimes )


def saveSexyPrimes( sexyPrimes ):
    saveTable( 'sexy_primes', sexyPrimes )


def saveSexyTriplets( sexyTriplets ):
    saveTable( 'sexy_triplets', sexyTriplets )


def saveSexyQuadruplets( sexyQuadruplets ):
    saveTable( 'sexy_quadruplets', sexyQuadruplets )


def saveTripletPrimes( tripletPrimes ):
    saveTable( 'triplet_primes', tripletPrimes )


def saveQuadrupletPrimes( quadPrimes ):
    saveTable( 'quad_primes', quadPrimes )


def saveQuintupletPrimes( quintPrimes ):
    saveTable( 'quint_primes', quintPrimes )


def saveSextupletPrimes( sextPrimes ):
    saveTable( 'sext_primes', sextPrimes )


#//******************************************************************************
#//
#//  importTable
#//
#//******************************************************************************

def importTable( fileName, loadTableFunc, saveTableFunc  ):
    print( fileName )
    var = loadTableFunc( )

    with contextlib.closing( bz2.BZ2File( fileName, 'rb' ) ) as pickleFile:
        imported = pickle.load( pickleFile )

    var.update( imported )

    saveTableFunc( var )

    return len( var )


def importSmallPrimes( fileName ):
    return importTable( fileName, loadSmallPrimes, saveSmallPrimes )


def importLargePrimes( fileName ):
    return importTable( fileName, loadLargePrimes, saveLargePrimes )


def importIsolatedPrimes( fileName ):
    return importTable( fileName, loadIsolatedPrimes, saveIsolatedPrimes )


def importTwinPrimes( fileName ):
    return importTable( fileName, loadTwinPrimes, saveTwinPrimes )


def importBalancedPrimes( fileName ):
    return importTable( fileName, loadBalancedPrimes, saveBalancedPrimes )


def importDoubleBalancedPrimes( fileName ):
    return importTable( fileName, loadDoubleBalancedPrimes, saveDoubleBalancedPrimes )


def importTripleBalancedPrimes( fileName ):
    return importTable( fileName, loadTripleBalancedPrimes, saveTripleBalancedPrimes )


def importSophiePrimes( fileName ):
    return importTable( fileName, loadSophiePrimes, saveSophiePrimes )


def importCousinPrimes( fileName ):
    return importTable( fileName, loadCousinPrimes, saveCousinPrimes )


def importSexyPrimes( fileName ):
    return importTable( fileName, loadSexyPrimes, saveSexyPrimes )


def importSexyTriplets( fileName ):
    return importTable( fileName, loadSexyTripletPrimes, saveSexyTriplets )


def importSexyQuadruplets( fileName ):
    return importTable( fileName, loadSexyQuadrupletPrimes, saveSexyQuadruplets )


def importTripletPrimes( fileName ):
    return importTable( fileName, loadTripletPrimes, saveTripletPrimes )


def importQuadrupletPrimes( fileName ):
    return importTable( fileName, loadQuadrupletPrimes, saveQuadrupletPrimes )


def importQuintupletPrimes( fileName ):
    return importTable( fileName, loadQuintupletPrimes, saveQuintupletPrimes )


def importSextupletPrimes( fileName ):
    return importTable( fileName, loadSextupletPrimes, saveSextupletPrimes )


#//******************************************************************************
#//
#//  makeTable
#//
#//******************************************************************************

def makeTable( start, end, step, func, name ):
    global updateDicts

    updateDicts = True

    try:
        for i in range( int( start ), int( end ) + 1, int( step ) ):
            p = func( i )

            if isinstance( p, list ):
                p = p[ 0 ]

            print( name + ':  {:,} : {:,}'.format( i, p ) )
            sys.stdout.flush( )
    except KeyboardInterrupt:
        pass

    return end


def makeSmallPrimes( start, end, step ):
    global smallPrimes
    getNthPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthPrime, 'small' )
    saveSmallPrimes( smallPrimes )
    return end


def makeLargePrimes( start, end, step ):
    global largePrimes
    getNthPrime( 1000000 )  # force the cache to load
    end = makeTable( start, end, step, getNthPrime, 'prime' )
    saveLargePrimes( largePrimes )
    return end


def makeIsolatedPrimes( start, end, step ):
    global isolatedPrimes
    getNthIsolatedPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthIsolatedPrime, 'isolated' )
    saveIsolatedPrimes( isolatedPrimes )
    return end


def makeSuperPrimes( start, end ):
    global smallPrimes
    global largePrimes
    global updateDicts

    getNthPrime( 100 )      # force small primes cache to load
    getNthPrime( 1000000 )  # force large primes cache to load

    try:
        for i in range( int( start ), int( end ) + 1, 1 ):
            updateDicts = False
            nth = getNthPrime( i )

            updateDicts = True
            p = getNthPrime( nth )

            print( 'super:  {:,} : {:,} : {:,}'.format( i, nth, p ) )
            sys.stdout.flush( )
    except KeyboardInterrupt:
        pass

    saveSmallPrimes( smallPrimes )
    saveLargePrimes( largePrimes )

    return end


def makeTwinPrimes( start, end, step ):
    global twinPrimes
    getNthTwinPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTwinPrime, 'twin' )
    saveTwinPrimes( twinPrimes )
    return end


def makeBalancedPrimes( start, end, step ):
    global balancedPrimes
    getNthBalancedPrimes( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthBalancedPrime, 'balanced' )
    saveBalancedPrimes( balancedPrimes )
    return end


def makeDoubleBalancedPrimes( start, end, step ):
    global doubleBalancedPrimes
    end = makeTable( start, end, step, getNthDoubleBalancedPrime, 'double_balanced' )
    saveDoubleBalancedPrimes( doubleBalancedPrimes )
    return end


def makeTripleBalancedPrimes( start, end, step ):
    global tripleBalancedPrimes
    end = makeTable( start, end, step, getNthTripleBalancedPrime, 'triple_balanced' )
    saveTripleBalancedPrimes( tripleBalancedPrimes )
    return end


def makeSophiePrimes( start, end, step ):
    global sophiePrimes
    getNthSophiePrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSophiePrime, 'sophie' )
    saveSophiePrimes( sophiePrimes )
    return end


def makeCousinPrimes( start, end, step ):
    global cousinPrimes
    getNthCousinPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthCousinPrime, 'cousin' )
    saveCousinPrimes( cousinPrimes )
    return end


def makeSexyPrimes( start, end, step ):
    global sexyPrimes
    getNthSexyPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyPrime, 'sexy' )
    saveSexyPrimes( sexyPrimes )
    return end


def makeSexyTriplets( start, end, step ):
    global sexyTriplets
    getNthSexyTriplet( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyTriplet, 'sexytrip' )
    saveSexyTriplets( sexyTriplets )
    return end


def makeSexyQuadruplets( start, end, step ):
    global sexyQUadruplets
    getNthSexyQuadruplet( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthSexyQuadruplet, 'sexyquad' )
    saveSexyQuadruplets( sexyQuadruplets )
    return end


def makeTripletPrimes( start, end, step ):
    global tripletPrimes
    getNthTripletPrime( 100 )  # force the cache to load
    end = makeTable( start, end, step, getNthTripletPrime, 'triplet' )
    saveTripletPrimes( tripletPrimes )
    return end


def makeQuadrupletPrimes( start, end, step ):
    global quadPrimes
    getNthQuadrupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuadrupletPrime, 'quad' )
    saveQuadrupletPrimes( quadPrimes )
    return end


def makeQuintupletPrimes( start, end, step ):
    global quintPrimes
    getNthQuintupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthQuintupletPrime, 'quint' )
    saveQuintupletPrimes( quintPrimes )
    return end


def makeSextupletPrimes( start, end, step ):
    global sextPrimes
    getNthSextupletPrime( 10 )  # force the cache to load
    end = makeTable( start, end, step, getNthSextupletPrime, 'sext' )
    saveSextupletPrimes( sextPrimes )
    return end


#//******************************************************************************
#//
#//  dumpTable
#//
#//******************************************************************************

def dumpTable( loadFunc, name ):
    var = loadFunc( )

    for i in sorted( [ key for key in var ] ):
        print( name + ':  ' + str( i ) + ' : ' + str( var[ i ] ) )

    return max( [ key for key in var ] )


def dumpSmallPrimes( ):
    return dumpTable( loadSmallPrimes, 'small' )


def dumpLargePrimes( ):
    return dumpTable( loadLargePrimes, 'prime' )


def dumpIsolatedPrimes( ):
    return dumpTable( loadIsolatedPrimes, 'isolated' )


def dumpTwinPrimes( ):
    return dumpTable( loadTwinPrimes, 'twin' )


def dumpBalancedPrimes( ):
    return dumpTable( loadBalancedPrimes, 'balanced' )


def dumpDoubleBalancedPrimes( ):
    return dumpTable( loadDoubleBalancedPrimes, 'double_balanced' )


def dumpTripleBalancedPrimes( ):
    return dumpTable( loadTripleBalancedPrimes, 'triple_balanced' )


def dumpSophiePrimes( ):
    return dumpTable( loadSophiePrimes, 'sophie' )


def dumpCousinPrimes( ):
    return dumpTable( loadCousinPrimes, 'cousin' )


def dumpSexyPrimes( ):
    return dumpTable( loadSexyPrimes, 'sexy' )


def dumpSexyTriplets( ):
    return dumpTable( loadSexyTripletPrimes, 'sexytrip' )


def dumpSexyQuadruplets( ):
    return dumpTable( loadSexyQuadrupletPrimes, 'sexyquad' )


def dumpTripletPrimes( ):
    return dumpTable( loadTripletPrimes, 'triplet' )


def dumpQuadrupletPrimes( ):
    return dumpTable( loadQuadrupletPrimes, 'quad' )


def dumpQuintupletPrimes( ):
    return dumpTable( loadQuintupletPrimes, 'quint' )


def dumpSextupletPrimes( ):
    return dumpTable( loadQSextupletPrimes, 'sext' )


#//******************************************************************************
#//
#//  operators
#//
#//  Regular operators expect zero or more single values and if those arguments
#//  are lists, rpn will iterate calls to the operator handler for each element
#//  in the list.   Multiple lists for arguments are not permutated.  Instead,
#//  the operator handler is called for each element in the first list, along
#//  with the nth element of each other argument that is also a list.
#//
#//******************************************************************************

operators = {
    '_dumpbal'      : [ dumpBalancedPrimes, 0 ],
    '_dumpcousin'   : [ dumpCousinPrimes, 0 ],
    '_dumpdouble'   : [ dumpDoubleBalancedPrimes, 0 ],
    '_dumpiso'      : [ dumpIsolatedPrimes, 0 ],
    '_dumpprimes'   : [ dumpLargePrimes, 0 ],
    '_dumpquad'     : [ dumpQuadrupletPrimes, 0 ],
    '_dumpquint'    : [ dumpQuintupletPrimes, 0 ],
    '_dumpsext'     : [ dumpSextupletPrimes, 0 ],
    '_dumpsexy'     : [ dumpSexyPrimes, 0 ],
    '_dumpsmall'    : [ dumpSmallPrimes, 0 ],
    '_dumpsophie'   : [ dumpSophiePrimes, 0 ],
    '_dumptriple'   : [ dumpTripleBalancedPrimes, 0 ],
    '_dumptriplet'  : [ dumpTripletPrimes, 0 ],
    '_dumptwin'     : [ dumpTwinPrimes, 0 ],
    '_importbal'    : [ importBalancedPrimes, 1 ],
    '_importcousin' : [ importCousinPrimes, 1 ],
    '_importdouble' : [ importDoubleBalancedPrimes, 1 ],
    '_importiso'    : [ importIsolatedPrimes, 1 ],
    '_importprimes' : [ importLargePrimes, 1 ],
    '_importquad'   : [ importQuadrupletPrimes, 1 ],
    '_importquint'  : [ importQuintupletPrimes, 1 ],
    '_importsext'   : [ importSextupletPrimes, 1 ],
    '_importsexy'   : [ importSexyPrimes, 1 ],
    '_importsexy3'  : [ importSexyTriplets, 1 ],
    '_importsexy4'  : [ importSexyQuadruplets, 1 ],
    '_importsmall'  : [ importSmallPrimes, 1 ],
    '_importsophie' : [ importSophiePrimes, 1 ],
    '_importtriple' : [ importTripleBalancedPrimes, 1 ],
    '_importtriplet': [ importTripletPrimes, 1 ],
    '_importtwin'   : [ importTwinPrimes, 1 ],
    '_makebal'      : [ makeBalancedPrimes, 3 ],
    '_makecousin'   : [ makeCousinPrimes, 3 ],
    '_makedouble'   : [ makeDoubleBalancedPrimes, 3 ],
    '_makeiso'      : [ makeIsolatedPrimes, 3 ],
    '_makeprimes'   : [ makeLargePrimes, 3 ],
    '_makequad'     : [ makeQuadrupletPrimes, 3 ],
    '_makequint'    : [ makeQuintupletPrimes, 3 ],
    '_makesext'     : [ makeSextupletPrimes, 3 ],
    '_makesexy'     : [ makeSexyPrimes, 3 ],
    '_makesexy3'    : [ makeSexyTriplets, 3 ],
    '_makesexy4'    : [ makeSexyQuadruplets, 3 ],
    '_makesmall'    : [ makeSmallPrimes, 3 ],
    '_makesophie'   : [ makeSophiePrimes, 3 ],
    '_makesuper'    : [ makeSuperPrimes, 2 ],
    '_maketriple'   : [ makeTripleBalancedPrimes, 3 ],
    '_maketriplet'  : [ makeTripletPrimes, 3 ],
    '_maketwin'     : [ makeTwinPrimes, 3 ],
}


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    global addToListArgument
    global dataPath
    global numerals
    global updateDicts

    global balancedPrimes
    global cousinPrimes
    global doubleBalancedPrimes
    global isolatedPrimes
    global largePrimes
    global quadPrimes
    global quintPrimes
    global sextPrimes
    global sexyPrimes
    global sexyQuadruplets
    global sexyTriplets
    global smallPrimes
    global sophiePrimes
    global superPrimes
    global tripleBalancedPrimes
    global tripletPrimes
    global twinPrimes

    # initialize globals
    balancedPrimes = { }
    cousinPrimes = { }
    doubleBalancedPrimes = { }
    isolatedPrimes = { }
    largePrimes = { }
    quadPrimes = { }
    quintPrimes = { }
    sextPrimes = { }
    sexyPrimes = { }
    sexyQuadruplets = { }
    sexyTriplets = { }
    smallPrimes = { }
    sophiePrimes = { }
    superPrimes = { }
    tripleBalancedPrimes = { }
    tripletPrimes = { }
    twinPrimes = { }

    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )

    help = False
    helpArgs = [ ]

    for i in range( 0, len( sys.argv ) ):
        if sys.argv[ i ] == 'help':
            help = True
        else:
            if help:
                helpArgs.append( sys.argv[ i ] )

    if help:
        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, { }, { }, { }, helpArgs )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION +
                                      ': ' + PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE,
                                      add_help=False, formatter_class=argparse.RawTextHelpFormatter,
                                      prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-t', '--time', action='store_true' )
    parser.add_argument( '-?', '--other_help', action='store_true' )

    # OK, let's parse and validate the arguments
    if len( sys.argv ) == 1:
        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION )
        return

    args = parser.parse_args( )

    if args.help or args.other_help:
        printHelp( PROGRAM_NAME, PROGRAM_DESCRIPTION, operators, { }, { }, { }, [ ] )
        return

    if args.time:
        time.clock( )

    index = 1                 # only used for error messages
    valueList = list( )

    if len( args.terms ) == 0:
        print( 'rpn:  no terms found' )
        return

    # let's check out the arguments before we start to do any calculations
    if not validateArguments( args.terms ):
        return

    # start parsing terms and populating the evaluation stack... this is the heart of rpn
    for term in args.terms:
        if term in operators:
            argsNeeded = operators[ term ][ 1 ]

            # first we validate, and make sure the operator has enough arguments
            if len( valueList ) < argsNeeded:
                print( 'rpn:  error in arg ' + format( index ) + ':  operator \'' + term + '\' requires ' +
                       format( argsNeeded ) + ' argument', end='' )

                print( 's' if argsNeeded > 1 else '' )
                break

            try:
                if argsNeeded == 0:
                    result = callers[ 0 ]( operators[ term ][ 0 ], None )
                else:
                    argList = list( )

                    for i in range( 0, argsNeeded ):
                        arg = valueList.pop( )
                        argList.append( arg if isinstance( arg, list ) else [ arg ] )

                    result = callers[ argsNeeded ]( operators[ term ][ 0 ], *argList )

                if len( result ) == 1:
                    result = result[ 0 ]

                valueList.append( result )
            except KeyboardInterrupt as error:
                print( 'rpn:  keyboard interrupt' )
                break
            #except ValueError as error:
            #    print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
            #except TypeError as error:
            #    print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
            #    break
            #except ZeroDivisionError as error:
            #    print( 'rpn:  division by zero' )
            #    break
        else:
            try:
                valueList.append( parseInputValue( term, inputRadix ) )
            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                valueList.append( term )
                print( 'rpn:  error in arg ' + format( index ) +
                       ':  unrecognized argument: \'%s\'' % sys.argv[ index ] )
                break

        index = index + 1
    else:    # i.e., if the for loop completes
        if args.time:
            print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

