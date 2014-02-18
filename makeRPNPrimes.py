#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeRPNPrimes.py
#//
#//  RPN command-line calculator prime data generator
#//  copyright (c) 2013 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import argparse
import bz2
import collections
import contextlib
import datetime
import pickle
import itertools
import math
import os
import pyprimes
import random
import string
import struct
import sys
import textwrap
import time

from fractions import Fraction
from functools import reduce
from mpmath import *

from rpnDeclarations import *


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
    except FileNotFoundError as error:
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
    except KeyboardInterrupt as error:
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
    except KeyboardInterrupt as error:
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
#//  parseInputValue
#//
#//  Parse out a numerical expression and attempt to set the precision to an
#//  appropriate value based on the expression.
#//
#//******************************************************************************

def parseInputValue( term, inputRadix ):
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
                mp.dps = newPrecision

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
            if integer[ 1 ] in 'Xx':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( ( math.log10( 16 ) * ( len( integer ) - 2 ) ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                return mpmathify( int( integer[ 2 : ], 16 ) )
            elif integer[ -1 ] in 'bB':
                # set the precision big enough to handle this value
                newPrecision = math.ceil( math.log10( 2 ) * ( len( integer ) - 1 ) ) + 1

                if mp.dps < newPrecision:
                    mp.dps = newPrecision

                integer = integer[ : -1 ]
                return mpmathify( int( integer, 2 ) * ( -1 if negative else 1 ) )
            else:
                integer = integer[ 1 : ]

                return mpmathify( int( integer, 8 ) )
        elif inputRadix == 10:
            newPrecision = len( integer ) + 1

            if mp.dps < newPrecision:
                mp.dps = newPrecision

            return fneg( integer ) if negative else mpmathify( integer )

    # finally, we have a non-radix 10 number to parse
    result = convertToBase10( integer, mantissa, inputRadix )
    return fneg( result ) if negative else mpmathify( result )


#//******************************************************************************
#//
#//  roundMantissa
#//
#//******************************************************************************

def roundMantissa( mantissa, accuracy ):
    if len( mantissa ) <= accuracy:
        return mantissa

    lastDigit = int( mantissa[ accuracy - 1 ] )
    extraDigit = int( mantissa[ accuracy ] )

    result = mantissa[ : accuracy - 1 ]

    if extraDigit >= 5:
        result += str( lastDigit + 1 )
    else:
        result += str( lastDigit )

    return result


#//******************************************************************************
#//
#//  formatOutput
#//
#//  This takes a string representation of the result and formats it according
#//  to a whole bunch of options.
#//
#//******************************************************************************

def formatOutput( output, radix, numerals, integerGrouping, integerDelimiter, leadingZero,
                  decimalGrouping, decimalDelimiter, baseAsDigits, outputAccuracy ):
    # filter out text strings
    for c in output:
        if c in '+-.':
            continue

        if c in string.whitespace or c in string.punctuation:
            return output

    exponentIndex = output.find( 'e' )

    if exponentIndex > 0:
        exponent = int( output[ exponentIndex + 1 : ] )
        output = output[ : exponentIndex ]
    else:
        exponent = 0

    #print( strOutput )

    if '.' in strOutput:
        decimal = strOutput.find( '.' )
    else:
        decimal = len( strOutput )

    negative = strOutput[ 0 ] == '-'

    strResult = '';

    integer = strOutput[ 1 if negative else 0 : decimal ]
    integerLength = len( integer )

    return result


#//******************************************************************************
#//
#//  printParagraph
#//
#//******************************************************************************

def printParagraph( text, length = 79, indent = 0 ):
    lines = textwrap.wrap( text, length )

    for line in lines:
        print( ' ' * indent + line )


#//******************************************************************************
#//
#//  printGeneralHelp
#//
#//******************************************************************************

def printGeneralHelp( basicCategories, operatorCategories ):
    print( PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )


#//******************************************************************************
#//
#//  printTitleScreen
#//
#//******************************************************************************

def printTitleScreen( ):
    print( PROGRAM_NAME, PROGRAM_VERSION, '-', PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )
    print( 'For more information use, \'makeRPNprimes help\'.' )


#//******************************************************************************
#//
#//  printOperatorHelp
#//
#//******************************************************************************

def printOperatorHelp( helpArgs, term, operatorInfo, operatorHelp ):
    if operatorInfo[ 1 ] == 1:
        print( 'n ', end='' )
    elif operatorInfo[ 1 ] == 2:
        print( 'n k ', end='' )
    elif operatorInfo[ 1 ] == 3:
        print( 'a b c ', end='' )
    elif operatorInfo[ 1 ] == 4:
        print( 'a b c d ', end='' )
    elif operatorInfo[ 1 ] == 5:
        print( 'a b c d e ', end='' )

    print( term + ' - ' + operatorHelp[ 1 ] )

    print( )

    print( 'category: ' + operatorHelp[ 0 ] )

    if operatorHelp[ 2 ] == '\n':
        print( )
        print( 'No further help is available.' )
    else:
        print( operatorHelp[ 2 ] )

    if len( helpArgs ) > 1 and helpArgs[ 1 ] in ( 'ex', 'example' ):
        print( )

        if operatorHelp[ 3 ] == '\n':
            print( 'No examples are available.' )
        else:
            print( term + ' examples:' )
            print( operatorHelp[ 3 ] )


#//******************************************************************************
#//
#//  printHelp
#//
#//******************************************************************************

def printHelp( helpArgs ):
    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'help.pckl.bz2', 'rb' ) ) as pickleFile:
            helpVersion = pickle.load( pickleFile )
            basicCategories = pickle.load( pickleFile )
            operatorHelp = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to help file.  Help will be unavailable.' )
        return

    if helpVersion != PROGRAM_VERSION:
        print( 'rpn:  help file version mismatch' )

    operatorCategories = set( operatorHelp[ key ][ 0 ] for key in operatorHelp )

    if len( helpArgs ) == 0:
        printGeneralHelp( basicCategories, operatorCategories )
        return

    term = helpArgs[ 0 ]

    if term in operators:
        printOperatorHelp( helpArgs, term, operators[ term ], operatorHelp[ term ] )


#//******************************************************************************
#//
#//  validateOptions
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  validateArguments
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  loadUnitConversionMatrix
#//
#//******************************************************************************

def loadUnitConversionMatrix( ):
    global unitConversionMatrix

    try:
        with contextlib.closing( bz2.BZ2File( dataPath + os.sep + 'unit_conversions.pckl.bz2', 'rb' ) ) as pickleFile:
            unitConversionMatrix = pickle.load( pickleFile )
    except FileNotFoundError as error:
        print( 'rpn:  Unable to load unit conversion matrix data.  Unit conversion will be unavailable.' )


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
    nestedListLevel = 0

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
        printHelp( helpArgs )
        return

    # set up the command-line options parser
    parser = argparse.ArgumentParser( prog=PROGRAM_NAME, description=PROGRAM_NAME + ' ' + PROGRAM_VERSION + ': ' +
                                      PROGRAM_DESCRIPTION + '\n    ' + COPYRIGHT_MESSAGE, add_help=False,
                                      formatter_class=argparse.RawTextHelpFormatter, prefix_chars='-' )

    parser.add_argument( 'terms', nargs='*', metavar='term' )
    parser.add_argument( '-a', '--output_accuracy', nargs='?', type=int, action='store', default=defaultAccuracy, # -1
                         const=defaultAccuracy )
    parser.add_argument( '-b', '--input_radix', type=str, action='store', default=defaultInputRadix )
    parser.add_argument( '-c', '--comma', action='store_true' )
    parser.add_argument( '-d', '--decimal_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultDecimalGrouping )
    parser.add_argument( '-g', '--integer_grouping', nargs='?', type=int, action='store', default=0,
                         const=defaultIntegerGrouping )
    parser.add_argument( '-h', '--help', action='store_true' )
    parser.add_argument( '-i', '--identify', action='store_true' )
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
    if len( sys.argv ) == 1:
        printTitleScreen( )
        return

    args = parser.parse_args( )

    if args.help or args.other_help:
        printHelp( [ ] )
        return

    valid, errorString = validateOptions( args )

    if not valid:
        print( 'rpn:  ' + errorString )
        return

    mp.dps = args.precision

    if args.time:
        time.clock( )

    # these are either globals or can be modified by other options (like -x)
    bitwiseGroupSize = args.bitwise_group_size
    integerGrouping = args.integer_grouping
    leadingZero = args.leading_zero

    # handle -a - set precision to be at least 2 greater than output accuracy
    if mp.dps < args.output_accuracy + 2:
        mp.dps = args.output_accuracy + 2

    # handle -n
    numerals = args.numerals

    # handle -b
    inputRadix = int( args.input_radix )

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
        bitwiseGroupSize = 16

    # handle -o
    if args.octal:
        outputRadix = 8
        leadingZero = True
        integerGrouping = 3
        bitwiseGroupSize = 9

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
        print( '--input_radix:  %d'% inputRadix )
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
        print( '--bitwise_group_size:  %d' % bitwiseGroupSize )
        print( '--hex:  ' + ( 'true' if args.hex else 'false' ) )
        print( '--identify:  ' + ( 'true' if args.identify else 'false' ) )
        print( '--leading_zero:  ' + ( 'true' if leadingZero else 'false' ) )
        print( )

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
            except ValueError as error:
                print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except TypeError as error:
                print( 'rpn:  type error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )
                break
            except ZeroDivisionError as error:
                print( 'rpn:  division by zero' )
                break
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
        if len( valueList ) > 1 or len( valueList ) == 0:
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
                print( formatListOutput( result, outputRadix, numerals, integerGrouping, integerDelimiter,
                                         leadingZero, args.decimal_grouping, ' ', baseAsDigits,
                                         args.output_accuracy ) )
            else:
                # output the answer with all the extras according to command-line arguments
                resultString = nstr( result, mp.dps )

                outputString = formatOutput( resultString, outputRadix, numerals, integerGrouping,
                                             integerDelimiter, leadingZero, args.decimal_grouping,
                                             ' ', baseAsDigits, args.output_accuracy )

                # handle the units if we are display a measurement
                if isinstance( result, Measurement ):
                    outputString += ' ' + formatUnits( result )

                print( outputString )

                # handle --identify
                if args.identify:
                    formula = identify( result )

                    if formula is None:
                        base = [ 'pi', 'e' ]
                        formula = identify( result, base )

                    # I don't know if this would ever be useful to try.
                    #if formula is None:
                    #    base.extend( [ 'log(2)', 'log(3)', 'log(4)', 'log(5)', 'log(6)', 'log(7)', 'log(8)', 'log(9)' ] )
                    #    formula = identify( result, base )
                    #
                    # Nor this.
                    #if formula is None:
                    #    base.extend( [ 'phi', 'euler', 'catalan', 'apery', 'khinchin', 'glaisher', 'mertens', 'twinprime' ] )
                    #    formula = identify( result, base )

                    if formula is None:
                        print( '    = [formula cannot be found]' )
                    else:
                        print( '    = ' + formula )

                # handle --find_poly
                if args.find_poly > 0:
                    poly = str( findpoly( result, args.find_poly ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000 ) )

                    if poly == 'None':
                        poly = str( findpoly( result, args.find_poly, maxcoeff=1000000, tol=1e-10 ) )

                    if poly == 'None':
                        print( '    = polynomial of degree <= %d not found' % args.find_poly )
                    else:
                        print( '    = polynomial ' + poly )

            saveResult( result )

        if args.time:
            print( '\n%.3f seconds' % time.clock( ) )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )
