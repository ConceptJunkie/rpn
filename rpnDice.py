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
else:
    FileNotFoundError = IOError


def debugPrint( *args, **kwargs ):
    if g.debugMode:
        builtins.print( *args, **kwargs )
    else:
        return

import itertools

from random import randrange

import rpnGlobals as g


# //******************************************************************************
# //
# //  rollDice
# //
# //******************************************************************************

def rollDice( expression ):
    return evaluateDiceExpression( parseDiceExpression( expression ) )


# //******************************************************************************
# //
# //  rollMultipleDice
# //
# //******************************************************************************

def rollMultipleDice( expression, times ):
    result = [ ]

    dice = parseDiceExpression( expression )

    for i in arange( 0, times ):
        result.append( evaluateDiceExpression( dice ) )

    return result


# //******************************************************************************
# //
# //  permuteDice
# //
# //  format: [c]dv[x[p]][h[q]]
# //
# //  c - dice count, defaults to 1
# //  v - dice value, i.e., number of sides, minumum 2, no maximum
# //  p - drop lowest die value(s), defaults to 1
# //  q - drop highest value(s), defaults to 1
# //
# //******************************************************************************

def permuteDice( expression ):
    dice = parseDiceExpression( expression )

    result = [ ]

    diceList = [ ]

    for diceCount, diceValue, dropLowest, dropHighestCount, modifier in dice:
        for i in range( diceCount ):
            diceList.append( range( 1, diceValue + 1 ) )

    permutations = itertools.product( *diceList )

    for values in permutations:
        result.append( sum( values ) )

    return result


# //******************************************************************************
# //
# //  getDicePermutations
# //
# //******************************************************************************

#def getDicePermutations( diceCount, diceValue, dropLowestCount, dropHighestCount, modifier ):
#    if dropLowestCount == 0 and dropHighestCount == 0:
#        return itertools.product( range( 1, diceValue + 1 ), repeat=diceCount )
#    else:
#        for values in itertools.product( range( 1, diceValue + 1 ), repeat=diceCount ):



# //******************************************************************************
# //
# //  parseDiceExpression
# //
# //  expr[,expr]
# //
# //
# //  format: [c]dv[x[p]][h[q]][-+]y
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

                if ( dropLowestCount < 0 ):
                    raise ValueError( 'drop lowest count must be non-negative' )

                state = defaultState
            elif state == dropHighestCountState:
                if piece == '':
                    dropHighestCount = 1
                else:
                    dropHighestCount = int( piece )
            elif state == plusModifierState:
                print( 'plus', piece )
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

        # trailing x means drop count is 1
        if state == dropLowestCountState:
            dropLowestCount = 1
        elif state == dropHighestCountState:
            dropHighestCount = 1

        if diceCount == 0:
            diceCount = 1

        if dropLowestCount != 0 and diceValue == 0:
            raise ValueError( 'dice expression requires \'d\' if \'x\' is used' )

        if dropHighestCount != 0 and diceValue == 0:
            raise ValueError( 'dice expression requires \'d\' if \'h\' is used' )

        if dropLowestCount >= diceCount:
            raise ValueError( 'drop lowest count \'x\' cannot be greater than or equal to dice count \'d\'' )

        if dropHighestCount >= diceCount:
            raise ValueError( 'drop highest count \'h\' cannot be greater than or equal to dice count \'d\'' )

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

def evaluateDiceExpression( args ):
    result = 0

    for diceCount, diceValue, dropLowestCount, dropHighestCount, modifier in args:
        if dropLowestCount == 0 and dropHighestCount == 0:
            for i in range( 0, diceCount ):
                result += randrange( diceValue ) + 1
        else:
            dice = [ ]

            for i in range( 0, diceCount ):
                dice.append( randrange( diceValue ) + 1 )

            dice.sort( )
            debugPrint( 'dice', dice )

            if dropHighestCount > 0:
                debugPrint( 'drop', dice[ dropLowestCount : -dropHighestCount ] )
                result += sum( dice[ dropLowestCount : -dropHighestCount ] )
            else:
                debugPrint( 'drop', dice[ dropLowestCount : ] )
                result += sum( dice[ dropLowestCount : ] )

        result += modifier

    return result

