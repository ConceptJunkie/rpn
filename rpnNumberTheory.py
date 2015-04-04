#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnNumberTheory.py
# //
# //  RPN command-line calculator number theory operators
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools
import random

from fractions import Fraction
from functools import reduce
from mpmath import *

from rpnDeclarations import *


# //******************************************************************************
# //
# //  getNthAlternatingFactorial
# //
# //******************************************************************************

def getNthAlternatingFactorial( n ):
    result = 0

    negative = False

    for i in arange( n, 0, -1 ):
        if negative:
            result = fadd( result, fneg( fac( i ) ) )
            negative = False
        else:
            result = fadd( result, fac( i ) )
            negative = True

    return result


# //******************************************************************************
# //
# //  getNthPascalLine
# //
# //******************************************************************************

def getNthPascalLine( n ):
    result = [ ]

    for i in arange( 0, n ):
        result.append( binomial( n - 1, i ) )

    return result


# //******************************************************************************
# //
# //  getDivisorCount
# //
# //******************************************************************************

def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in factor( n ) ] )


# //******************************************************************************
# //
# //  getDivisors
# //
# //******************************************************************************

def getDivisors( n ):
    result = getExpandedFactorList( factor( n ) )

    result = [ list( i ) for i in
               itertools.chain.from_iterable( itertools.combinations( result, r )
               for r in range( 0, len( result ) + 1 ) ) ]

    from operator import mul
    result = set( [ reduce( mul, i, 1 ) for i in result[ 1 : ] ] )
    result.add( 1 )

    result = sorted( list( result ) )

    return result


# //******************************************************************************
# //
# //  factor
# //
# //  This is not my code, and I need to find the source so I can attribute it.
# //  I think I got it from stackoverflow.com.
# //
# //******************************************************************************

def factor( n ):
    if n < -1:
        return [ ( -1, 1 ) ] + factor( fneg( n ) )
    elif n == -1:
        return [ ( -1, 1 ) ]
    elif n == 0:
        return [ ( 0, 1 ) ]
    elif n == 1:
        return [ ( 1, 1 ) ]
    else:
        def getPotentialPrimes( ):
            basePrimes = ( 2, 3, 5 )

            for basePrime in basePrimes:
                yield basePrime

            basePrimes = ( 7, 11, 13, 17, 19, 23, 29, 31 )

            primeGroup = 0

            while True:
                for basePrime in basePrimes:
                    yield primeGroup + basePrime

                primeGroup += 30

        factors = [ ]
        sqrtn = sqrt( n )

        for divisor in getPotentialPrimes( ):
            if divisor > sqrtn:
                break

            power = 0

            while ( fmod( n, divisor ) ) == 0:
                n = floor( fdiv( n, divisor ) )
                power += 1

            if power > 0:
                factors.append( ( divisor, power ) )
                sqrtn = sqrt( n )

        if n > 1:
            factors.append( ( int( n ), 1 ) )

        return factors


# //******************************************************************************
# //
# //  getExpandedFactorList
# //
# //******************************************************************************

def getExpandedFactorList( factors ):
    factors = map( lambda x: [ x[ 0 ] ] * x[ 1 ], factors )
    return reduce( lambda x, y: x + y, factors, [ ] )


# //******************************************************************************
# //
# //  getNthLucasNumber
# //
# //******************************************************************************

def getNthLucasNumber( n ):
    if n == 1:
        return 1
    else:
        return floor( fadd( power( phi, n ), 0.5 ) )


# //******************************************************************************
# //
# //  getNthJacobsthalNumber
# //
# //  From: http://oeis.org/A001045
# //
# //  a( n ) = ceiling( 2 ^ ( n + 1 ) / 3 ) - ceiling( 2 ^ n / 3 )
# //
# //******************************************************************************

def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], n )


# //******************************************************************************
# //
# //  getNthBaseKRepunit
# //
# //******************************************************************************

def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( k ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


# //******************************************************************************
# //
# //  getPrimePi
# //
# //******************************************************************************

def getPrimePi( n ):
    result = primepi2( n )

    return [ mpf( result.a ), mpf( result.b ) ]


# //******************************************************************************
# //
# //  getNthTribonacci
# //
# //******************************************************************************

def getNthTribonacci( n ):
    roots = polyroots( [ 1, -1, -1, -1  ] )
    roots2 = polyroots( [ 44, 0, -2, -1 ] )

    result = 0

    for i in range( 0, 3 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


# //******************************************************************************
# //
# //  getNthTetranacci
# //
# //  http://mathworld.wolfram.com/TetranacciNumber.html
# //
# //******************************************************************************

def getNthTetranacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1 ] )
    roots2 = polyroots( [ 563, 0, -20, -5, -1 ] )

    result = 0

    for i in range( 0, 4 ):
        result += fmul( roots2[ i ], power( roots[ i ], n ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


# //******************************************************************************
# //
# //  getNthPentanacci
# //
# //******************************************************************************

def getNthPentanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 5 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 8, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


# //******************************************************************************
# //
# //  getNthHexanacci
# //
# //******************************************************************************

def getNthHexanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 6 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 10, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


# //******************************************************************************
# //
# //  getNthHeptanacci
# //
# //******************************************************************************

def getNthHeptanacci( n ):
    roots = polyroots( [ 1, -1, -1, -1, -1, -1, -1, -1 ] )

    result = 0

    for i in range( 0, 7 ):
        result += fdiv( power( roots[ i ], n ), polyval( [ -1, 0, 1, 2, 3, 12, -1 ], roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


# //******************************************************************************
# //
# //  getNthPadovanNumber
# //
# //  Padovan sequence: a(n) = a(n-2) + a(n-3) with a(0)=1, a(1)=a(2)=0.
# //
# //  http://oeis.org/A000931
# //
# //  a(n) = (r^n)/(2r+3) + (s^n)/(2s+3) + (t^n)/(2t+3) where r, s, t are the
# //  three roots of x^3-x-1
# //
# //  http://www.wolframalpha.com/input/?i=solve+x^3-x-1
# //
# //  Unfortunately, the roots are scary-complicated, but it's a non-iterative
# //  formula, so I'll use it.
# //
# //  Wikipedia leaves off the first 4 terms, but Sloane's includes them.
# //  Wikipedia cites Ian Stewart and Mathworld, and I'll use their definition.
# //
# //******************************************************************************

def getNthPadovanNumber( arg ):
    n = fadd( arg, 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    e = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, e ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, e ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, e ) ) )

    return round( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                              fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                              fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )


# //******************************************************************************
# //
# //  convertFromContinuedFraction
# //
# //******************************************************************************

def convertFromContinuedFraction( n ):
    if not isinstance( n, list ):
        n = [ n ]

    if ( len( n ) == 1 ) and ( n[ 0 ] == 0 ):
        raise ValueError( "invalid input for evaluating a continued fraction" )

    fraction = ContinuedFraction( n ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


# //******************************************************************************
# //
# //  interpretAsFraction
# //
# //******************************************************************************

def interpretAsFraction( i, j ):
    fraction = ContinuedFraction( i, maxterms=j ).getFraction( )
    return [ fraction.numerator, fraction.denominator ]


# //******************************************************************************
# //
# //  interpretAsBase
# //
# //  This is a list operator so if the integer argument (base) is also a list,
# //  we need to handle that explicitly here.
# //
# //******************************************************************************

def interpretAsBase( args, base ):
    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ interpretAsBase( i, base ) for i in args ]
        else:
            args.reverse( )
    else:
        args = [ args ]

    if isinstance( base, list ):
        return [ interpretAsBase( args, i ) for i in base ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


# //******************************************************************************
# //
# //  getGreedyEgyptianFraction
# //
# //******************************************************************************

def getGreedyEgyptianFraction( n, d ):
    if n > d:
        raise ValueError( "'egypt' requires the numerator to be smaller than the denominator" )

    # Create a list to store the Egyptian fraction representation.
    result = [ ]

    rational = Fraction( int( n ), int( d ) )

    # Now, iteratively subtract out the largest unit fraction that may be
    # subtracted out until we arrive at a unit fraction.
    while True:
        # If the rational number has numerator 1, we're done.
        if rational.numerator == 1:
            result.append( rational )
            return result

        # Otherwise, find the largest unit fraction less than the current rational number.
        # This is given by the ceiling of the denominator divided by the numerator.
        unitFraction = Fraction( 1, rational.denominator // rational.numerator + 1 )

        result.append( unitFraction )

        # Subtract out this unit fraction.
        rational = rational - unitFraction

    return result


# //******************************************************************************
# //
# //  getNthLinearRecurrence
# //
# //  nth element of Fibonacci sequence = rpn [ 1 1 ] 1 n linear
# //  nth element of Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n linear
# //
# //******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    if not isinstance( recurrence, list ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, list ):
        seeds = [ seeds ]

    if len( seeds ) == 0:
        raise ValueError( 'internal error:  for operator \'linearrecur\', '
                          'seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getNthLinearRecurrence( recurrence[ : i ], seeds, i ) )

    if isinstance( n, list ):
        return [ getNthLinearRecurrence( recurrence, seeds, i ) for i in n ]

    if n < len( seeds ):
        return seeds[ int( n ) - 1 ]
    else:
        if len( recurrence ) == 0:
            raise ValueError( 'internal error:  for operator \'linearrecur\', '
                              'recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in arange( len( seeds ), n ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

            result.append( newValue )
            del result[ 0 ]

        return result[ -1 ]


# //******************************************************************************
# //
# //  makePythagoreanTriple
# //
# //  Euclid's formula
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Pythag/pythag.html#mnformula
# //
# //******************************************************************************

def makePythagoreanTriple( n, k ):
    if n < 0 or k < 0:
        raise ValueError( "'makepyth3' requires positive arguments" )

    if n == k:
        raise ValueError( "'makepyth3' requires unequal arguments" )

    result = [ ]

    result.append( fprod( [ 2, n, k ] ) )
    result.append( fabs( fsub( fmul( n, n ), fmul( k, k ) ) ) )
    result.append( fadd( fmul( n, n ), fmul( k, k ) ) )

    return sorted( result )


# //******************************************************************************
# //
# //  makePythagoreanQuadruple
# //
# //  From https://en.wikipedia.org/wiki/Pythagorean_quadruple:
# //
# //  All Pythagorean quadruples (including non-primitives, and with repetition,
# //  though a, b and c do not appear in all possible orders) can be generated
# //  from two positive integers a and b as follows:
# //
# //  If a and b have different parity, let p be any factor of a^2 + b^2 such that
# //  p^2 < a^2 + b^2.  Then c = (a^2 + b^2 - p^2)/(2p) and d =
# //  (a^2 + b^2 + p^2)/(2p).  Note that p = {d - c}.
# //
# //  A similar method exists for a, b both even, with the further restriction
# //  that 2p must be an even factor of a^2 + b^2. No such method exists if both
# //  a and b are odd.
# //
# //******************************************************************************

def makePythagoreanQuadruple( a, b ):
    if a < 0 or b < 0:
        raise ValueError( "'makepyth4' requires positive arguments" )

    #if a == b:
    #    raise ValueError( "'makepyth4' requires unequal arguments" )

    odd1 = ( fmod( a, 2 ) == 1 )
    odd2 = ( fmod( b, 2 ) == 1 )

    if odd1 and odd2:
        raise ValueError( "'makepyth4' arguments cannot both be odd" )

    result = [ a, b ]

    sumsqr = fadd( fmul( a, a ), fmul( b, b ) )


    div = getDivisors( sumsqr )

    if odd1 != odd2:
        if len( div ) <= 3:
            p = 1
        else:
            p = random.choice( div[ : ( len( div ) - 1 ) // 2 ] )
    else:
        if ( fmod( sumsqr, 2 ) == 1 ):
            raise ValueError( "'makepyth4' oops, can't make one!" )
        else:
            div = [ i for i in div[ : ( len( div ) - 1 ) // 2 ] if fmod( i, 2 ) == 0 ]
            p = random.choice( div )

    psqr = fmul( p, p )
    result.append( fdiv( fsub( sumsqr, psqr ), fmul( p, 2 ) ) )
    result.append( fdiv( fadd( sumsqr, psqr ), fmul( p, 2 ) ) )

    return sorted( result )

