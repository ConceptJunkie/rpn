#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDice.py
# //
# //  RPN command-line calculator dice rolling functions
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools

from collections import Counter
from mpmath import arange
from random import randrange

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnUtils import debugPrint, oneArgFunctionEvaluator, twoArgFunctionEvaluator

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  rollDice
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def rollDice( expression ):
    values, modifier = evaluateDiceExpression( parseDiceExpression( expression ) )
    return sum( values ) + modifier


# //******************************************************************************
# //
# //  rollMultipleDice
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def rollMultipleDice( expression, times ):
    dice = parseDiceExpression( expression )

    for i in arange( 0, times ):
        values, modifier = evaluateDiceExpression( dice )
        yield sum( values ) + modifier

def rollMultipleDiceGenerator( n, k ):
    return RPNGenerator( rollMultipleDice( n, k ) )


# //******************************************************************************
# //
# //  enumerateDice
# //
# //******************************************************************************

def enumerateDice( expression ):
    return evaluateDiceExpression( parseDiceExpression( expression ), False )[ 0 ]

@oneArgFunctionEvaluator( )
def enumerateDiceGenerator( n ):
    return RPNGenerator( enumerateDice( n ) )


# //******************************************************************************
# //
# //  enumerateMultipleDice
# //
# //******************************************************************************

def enumerateMultipleDice( expression, count ):
    dice = parseDiceExpression( expression )

    for i in arange( 0, count ):
        yield evaluateDiceExpression( dice )[ 0 ]

@twoArgFunctionEvaluator( )
def enumerateMultipleDiceGenerator( n, k ):
    return RPNGenerator( enumerateMultipleDice( n, k ) )


# //******************************************************************************
# //
# //  permuteDice
# //
# //  format: [c]dv[x[p]][h[q]][-+]y
# //
# //  c - dice count, defaults to 1
# //  v - dice value, i.e., number of sides, minumum 2
# //  p - drop lowest die value(s), defaults to 1
# //  q - drop highest value(s), defaults to 1
# //  y - add or subtract y from the total (modifier)
# //
# //******************************************************************************

def permuteDice( expression ):
    dice = parseDiceExpression( expression )

    diceList = [ ]

    dropAny = False
    ranges = [ ]
    dropRanges = [ ]
    drops = [ ]
    start = 0
    modifierTotal = 0
    groupCount = len( dice )

    for diceCount, diceValue, dropLowest, dropHighest, modifier in dice:
        ranges.append( ( start, start + diceCount ) )
        start += diceCount

        if dropLowest > 0 or dropHighest > 0:
            drops.append( True )
            dropRanges.append( ( dropLowest, diceCount - dropHighest ) )
            dropAny = True
        else:
            drops.append( False )
            dropRanges.append( ( 0, 0 ) )

        modifierTotal += modifier

        for i in range( diceCount ):
            diceList.append( range( 1, diceValue + 1 ) )

    permutations = itertools.product( *diceList )

    for values in permutations:
        if dropAny:
            total = 0

            for i in range( 0, groupCount ):
                group = values[ ranges[ i ][ 0 ] : ranges[ i ][ 1 ] ]

                if drops[ i ]:
                    group = list( group )
                    group.sort( )
                    total += sum( group[ dropRanges[ i ][ 0 ] : dropRanges[ i ][ 1 ] ] )
                else:
                    total += sum( group )

                total += modifierTotal
                yield total
        else:
            yield sum( values ) + modifierTotal

@oneArgFunctionEvaluator( )
def permuteDiceGenerator( n ):
    return RPNGenerator( permuteDice( n ) )


# //******************************************************************************
# //
# //  parseDiceExpression
# //
# //  format: [c]dv[,[c]dv...][x[p]][h[q]][-+]y
# //
# //  c - dice count, defaults to 1
# //  v - dice value, i.e., number of sides, minumum 2
# //  p - drop lowest die value(s), defaults to 1
# //  q - drop highest value(s), defaults to 1
# //  y - add or subtract y from the total (modifier)
# //
# //  return values:
# //
# //  a list of 5-tuples:  dice count, dice value, drop lowest count,
# //                       drop highest count, modifier
# //
# //******************************************************************************

def parseDiceExpression( arg ):
    counter = Counter( arg )

    if ( counter[ 'a' ] > 1 ):
        raise ValueError( 'dice expressions can only contain a single \'x\'' )

    if ( counter[ 'h' ] > 1 ):
        raise ValueError( 'dice expressions can only contain a single \'h\'' )

    if ( counter[ '+' ] > 1 ):
        raise ValueError( 'dice expressions can only contain a single \'+\'' )

    if ( counter[ '-' ] > 1 ):
        raise ValueError( 'dice expressions can only contain a single \'-\'' )

    if ( counter[ '+' ] + counter[ '-' ] > 1 ):
        raise ValueError( 'dice expressions can only have a single modifier (\'+\' or \'-\')' )

    import re
    expressions = re.split( ',', arg )

    result = [ ]

    for expr in expressions:
        pieces = re.split( '([dhx+-])', expr )

        debugPrint( 'pieces', pieces )

        diceValue = 0
        diceCount = 0
        dropLowestCount = 0
        dropHighestCount = 0
        modifier = 0

        defaultState = 0
        diceValueState = 1
        dropLowestCountState = 2
        dropHighestCountState = 3
        plusModifierState = 4
        minusModifierState = 5

        state = defaultState

        for piece in pieces:
            if state == defaultState:
                if piece == 'd':
                    state = diceValueState
                elif piece == 'x':
                    state = dropLowestCountState
                elif piece == 'h':
                    state = dropHighestCountState
                elif piece == '-':
                    state = minusModifierState
                elif piece == '+':
                    state = plusModifierState
                else:
                    if piece == '':
                        diceCount = 1
                    else:
                        diceCount = int( piece )
            elif state == diceValueState:
                diceValue = int( piece )

                if ( diceValue < 2 ):
                    raise ValueError( 'dice value must be greater than 1' )

                state = defaultState
            elif state == dropLowestCountState:
                if piece == '':
                    dropLowestCount = 1
                else:
                    dropLowestCount = int( piece )

                if ( dropLowestCount < 1 ):
                    raise ValueError( 'drop lowest count must be positive' )

                state = defaultState
            elif state == dropHighestCountState:
                if piece == '':
                    dropHighestCount = 1
                else:
                    dropHighestCount = int( piece )

                if ( dropHighestCount < 1 ):
                    raise ValueError( 'drop highest count must be positive' )

            elif state == plusModifierState:
                if piece == '':
                    modifier = 1
                else:
                    modifier = int( piece )

                state = defaultState
            elif state == minusModifierState:
                if piece == '':
                    modifier = -1
                else:
                    modifier = -int( piece )

                state = defaultState

        if diceCount == 0:
            diceCount = 1

        if dropLowestCount != 0 and diceValue == 0:
            raise ValueError( 'dice expression requires \'d\' if \'x\' is used' )

        if dropHighestCount != 0 and diceValue == 0:
            raise ValueError( 'dice expression requires \'d\' if \'h\' is used' )

        if ( dropLowestCount + dropHighestCount ) >= diceCount:
            raise ValueError( 'this dice expression is dropping as many or more dice than are being rolled' )

        debugPrint( 'expression', expr )
        debugPrint( 'diceCount', diceCount )
        debugPrint( 'diceValue', diceValue )
        debugPrint( 'dropLowestCount', dropLowestCount )
        debugPrint( 'dropHighestCount', dropHighestCount )
        debugPrint( 'modifier', modifier )

        result.append( ( diceCount, diceValue, dropLowestCount, dropHighestCount, modifier ) )

    return result


# //******************************************************************************
# //
# //  evaluateDiceExpression
# //
# //  a list of 5-tuples:  dice count, dice value, drop lowest count,
# //                       drop highest count, modifier
# //
# //******************************************************************************

def evaluateDiceExpression( args, sumIfPossible=True ):
    result = [ ]

    if sumIfPossible:
        result = [ 0 ]

    for diceCount, diceValue, dropLowestCount, dropHighestCount, modifier in args:
        if dropLowestCount == 0 and dropHighestCount == 0:
            if sumIfPossible:
                for i in range( 0, diceCount ):
                    result[ 0 ] += ( randrange( diceValue ) + 1 )
            else:
                for i in range( 0, diceCount ):
                    result.append( randrange( diceValue ) + 1 )
        else:
            dice = [ ]

            for i in range( 0, diceCount ):
                dice.append( randrange( diceValue ) + 1 )

            dice.sort( )
            debugPrint( 'dice', dice )

            if dropHighestCount > 0:
                debugPrint( 'drop', dice[ dropLowestCount : -dropHighestCount ] )
                result.extend( dice[ dropLowestCount : -dropHighestCount ] )
            else:
                debugPrint( 'drop', dice[ dropLowestCount : ] )
                result.extend( dice[ dropLowestCount : ] )

    return result, modifier


# //******************************************************************************
# //
# //  rollSimpleDice
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def rollSimpleDice( n, k ):
    values, modifier = evaluateDiceExpression( [ ( int( n ), int( k ), 0, 0, 0 ) ] )
    return sum( values ) + modifier

