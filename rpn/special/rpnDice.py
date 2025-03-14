#!/usr/bin/env python

#******************************************************************************
#
#  rpnDice.py
#
#  rpnChilada dice simulation operators
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import collections
import functools
import itertools
import re

from collections import Counter
from random import randrange

from mpmath import arange

from rpn.util.rpnDebug import debugPrint
from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, IntValidator, StringValidator


# write a function to enumerate the number of outcomes for a dice expression
# without actually permuting them.  i.e., rpn <dice_expr> permute_dice occurrences
#
# Is that possible?  It's definitely possible without including x and h.  With them
# it becomes a problem that's harder than I can solve, probably.
#
# c:\>rpn [ 1 6 dup ] 3 poly_power 3 enumerate -s1
# [
#     [ 3, 1 ],
#     [ 4, 3 ],
#     [ 5, 6 ],
#     [ 6, 10 ],
#     [ 7, 15 ],
#     [ 8, 21 ],
#     [ 9, 25 ],
#     [ 10, 27 ],
#     [ 11, 27 ],
#     [ 12, 25 ],
#     [ 13, 21 ],
#     [ 14, 15 ],
#     [ 15, 10 ],
#     [ 16, 6 ],
#     [ 17, 3 ],
#     [ 18, 1 ]
# ]
#
# c:\>rpn 3d6 permute_dice occurrences -s1
# [
#     [ 3, 1 ],
#     [ 4, 3 ],
#     [ 5, 6 ],
#     [ 6, 10 ],
#     [ 7, 15 ],
#     [ 8, 21 ],
#     [ 9, 25 ],
#     [ 10, 27 ],
#     [ 11, 27 ],
#     [ 12, 25 ],
#     [ 13, 21 ],
#     [ 14, 15 ],
#     [ 15, 10 ],
#     [ 16, 6 ],
#     [ 17, 3 ],
#     [ 18, 1 ]
# ]
#
# Make a new data type (dict) and then write an operator for summing multiple dicts.  Piece o' cake.
# Or use Counter...
#


#******************************************************************************
#
#  rollDice
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def rollDiceOperator( expression ):
    values, modifier = evaluateDiceExpression( parseDiceExpression( expression ) )
    return sum( values ) + modifier


#******************************************************************************
#
#  rollMultipleDice
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ StringValidator( ), IntValidator( 0 ) ] )
def rollMultipleDice( expression, times ):
    dice = parseDiceExpression( expression )

    for _ in arange( 0, times ):
        values, modifier = evaluateDiceExpression( dice )
        yield sum( values ) + modifier


def rollMultipleDiceOperator( n, k ):
    return RPNGenerator( rollMultipleDice( n, k ) )


#******************************************************************************
#
#  enumerateDice
#
#******************************************************************************

def enumerateDice( expression ):
    return evaluateDiceExpression( parseDiceExpression( expression ), False )[ 0 ]


@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def enumerateDiceOperator( n ):
    return RPNGenerator( enumerateDice( n ) )


#******************************************************************************
#
#  enumerateMultipleDice
#
#******************************************************************************

def enumerateMultipleDice( expression, count ):
    dice = parseDiceExpression( expression )

    for _ in arange( 0, count ):
        yield evaluateDiceExpression( dice )[ 0 ]


@twoArgFunctionEvaluator( )
@argValidator( [ StringValidator( ), IntValidator( 0 ) ] )
def enumerateMultipleDiceOperator( n, k ):
    return RPNGenerator( enumerateMultipleDice( n, k ) )


#******************************************************************************
#
#  permuteDice
#
#  format: [c]dv[x[p]][h[q]][-+]y
#
#  c - dice count, defaults to 1
#  v - dice value, i.e., number of sides, minumum 2
#  p - drop lowest die value(s), defaults to 1
#  q - drop highest value(s), defaults to 1
#  y - add or subtract y from the total (modifier)
#
#******************************************************************************

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
def permuteDiceOperator( n ):
    return RPNGenerator( permuteDice( n ) )


#******************************************************************************
#
#  parseDiceExpression
#
#  format: [c]dv[,[c]dv...][x[p]][h[q]][-+]y
#
#  c - dice count, defaults to 1
#  v - dice value, i.e., number of sides, minumum 2
#  p - drop lowest die value(s), defaults to 1
#  q - drop highest value(s), defaults to 1
#  y - add or subtract y from the total (modifier)
#
#  return values:
#
#  a list of 5-tuples:  dice count, dice value, drop lowest count,
#                       drop highest count, modifier
#
#******************************************************************************

def parseDiceExpression( arg ):
    counter = Counter( arg )

    if counter[ 'a' ] > 1:
        raise ValueError( 'dice expressions can only contain a single \'x\'' )

    if counter[ 'h' ] > 1:
        raise ValueError( 'dice expressions can only contain a single \'h\'' )

    if counter[ '+' ] > 1:
        raise ValueError( 'dice expressions can only contain a single \'+\'' )

    if counter[ '-' ] > 1:
        raise ValueError( 'dice expressions can only contain a single \'-\'' )

    if counter[ '+' ] + counter[ '-' ] > 1:
        raise ValueError( 'dice expressions can only have a single modifier (\'+\' or \'-\')' )

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

                if diceValue < 2:
                    raise ValueError( 'dice value must be greater than 1' )

                state = defaultState
            elif state == dropLowestCountState:
                if piece == '':
                    dropLowestCount = 1
                else:
                    dropLowestCount = int( piece )

                if dropLowestCount < 1:
                    raise ValueError( 'drop lowest count must be positive' )

                state = defaultState
            elif state == dropHighestCountState:
                if piece == '':
                    dropHighestCount = 1
                else:
                    dropHighestCount = int( piece )

                if dropHighestCount < 1:
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


#******************************************************************************
#
#  evaluateDiceExpression
#
#  a list of 5-tuples:  dice count, dice value, drop lowest count,
#                       drop highest count, modifier
#
#******************************************************************************

def evaluateDiceExpression( args, sumIfPossible=True ):
    result = [ ]
    modifierSum = 0    # currently only a single modifier is allowed

    if sumIfPossible:
        result = [ 0 ]

    for diceCount, diceValue, dropLowestCount, dropHighestCount, modifier in args:
        modifierSum += modifier

        if dropLowestCount == 0 and dropHighestCount == 0:
            if sumIfPossible:
                for _ in range( 0, diceCount ):
                    result[ 0 ] += ( randrange( diceValue ) + 1 )
            else:
                for _ in range( 0, diceCount ):
                    result.append( randrange( diceValue ) + 1 )
        else:
            dice = [ ]

            for _ in range( 0, diceCount ):
                dice.append( randrange( diceValue ) + 1 )

            dice.sort( )
            debugPrint( 'dice', dice )

            if dropHighestCount > 0:
                debugPrint( 'drop', dice[ dropLowestCount : -dropHighestCount ] )
                result.extend( dice[ dropLowestCount : -dropHighestCount ] )
            else:
                debugPrint( 'drop', dice[ dropLowestCount : ] )
                result.extend( dice[ dropLowestCount : ] )

    return result, modifierSum


#******************************************************************************
#
#  rollSimpleDice
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def rollSimpleDiceOperator( n, k ):
    values, modifier = evaluateDiceExpression( [ ( int( n ), int( k ), 0, 0, 0 ) ] )
    return sum( values ) + modifier

def dice_roll_distribution(num_dice, num_sides, drop_lowest=0, drop_highest=0):
    # Generate all possible rolls of the dice
    all_rolls = itertools.product(range(1, num_sides+1), repeat=num_dice)

    # Determine the lowest and highest dice to drop
    dice_to_drop = drop_lowest + drop_highest
    if dice_to_drop >= num_dice:
        return None # Can't drop all dice

    # Create a dictionary to store the counts for each total value
    totals = {i:0 for i in range(num_dice, num_dice*num_sides+1)}

    # Count the occurrences of each total value, taking into account dropped dice
    for roll in all_rolls:
        sorted_roll = sorted(roll)
        total = sum(sorted_roll[dice_to_drop:-drop_highest])
        totals[total] += 1

    return totals


@functools.lru_cache(maxsize=None)
def getDiceRollDistribution(dice_count, sides, drop_highest=0, drop_lowest=0):
    dice_results = collections.Counter()

    if dice_count == 0:
        dice_results[0] = 1
    elif sides == 0:
        raise ValueError( 'dice must have more than 0 sides' )
    else:
        for count_showing_max in range(dice_count + 1):  # 0..count

            d1 = getDiceRollDistribution(dice_count - count_showing_max, sides - 1, max(drop_highest - count_showing_max, 0), drop_lowest)

            count_showing_max_not_dropped = \
                            max( min(count_showing_max - drop_highest, dice_count - drop_highest - drop_lowest), 0)

            sum_showing_max = count_showing_max_not_dropped * sides

            multiplier = binomial(dice_count, count_showing_max)

            for k, v in d1.items():
                dice_results[sum_showing_max + k] += multiplier * v

    return dice_results

