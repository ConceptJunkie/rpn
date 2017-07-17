#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnNumberTheory.py
# //
# //  RPN command-line calculator number theory operators
# //  copyright (c) 2017, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools
import random

from fractions import Fraction
from functools import reduce

from mpmath import altzeta, arange, barnesg, beta, binomial, e, fabs, fac, \
                   fac2, fadd, fdiv, fib, floor, fmod, fmul, fneg, fprod, \
                   fsub, fsum, gamma, harmonic, hyperfac, loggamma, mp, mpc, \
                   mpf, mpmathify, nint, phi, polyroots, polyval, power, \
                   primepi, psi, re, root, superfac, sqrt, unitroots, \
                   zeta, zetazero

from rpnFactor import getFactors, getFactorList
from rpnGenerator import RPNGenerator
from rpnMath import isDivisible, isEven
from rpnPersistence import cachedFunction
from rpnUtils import getMPFIntegerAsString, oneArgFunctionEvaluator, \
                     twoArgFunctionEvaluator, real, real_int

import rpnGlobals as g


# //******************************************************************************
# //
# //  getNthAlternatingFactorial
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthAlternatingFactorial( n ):
    result = 0

    negative = False

    for i in arange( real( n ), 0, -1 ):
        if negative:
            result = fadd( result, fneg( fac( i ) ) )
            negative = False
        else:
            result = fadd( result, fac( i ) )
            negative = True

    return result


# //******************************************************************************
# //
# //  getNthPascalLineGenerator
# //
# //******************************************************************************

def getNthPascalLineGenerator( n ):
    for i in arange( 0, real( n ) ):
        yield binomial( n - 1, i )

@oneArgFunctionEvaluator( )
def getNthPascalLine( n ):
    return RPNGenerator.createGenerator( getNthPascalLineGenerator, n )


# //******************************************************************************
# //
# //  getDivisorCount
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'divisor_count' )
def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in getFactorList( n ) ] )


# //******************************************************************************
# //
# //  createDivisorList
# //
# //******************************************************************************

def createDivisorList( seed, factorList ):
    result = [ ]

    factor, count = factorList[ 0 ]

    for i in range( count + 1 ):
        divisors = [ ]
        divisors.extend( seed )
        divisors.extend( [ factor ] * i )

        if len( factorList ) > 1:
            result.extend( createDivisorList( divisors, factorList[ 1 : ] ) )
        else:
            result.extend( [ fprod( divisors ) ] )

    return result


# //******************************************************************************
# //
# //  getDivisors
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getDivisors( n ):
    if n == 0:
        return [ 0 ]
    elif n == 1:
        return [ 1 ]

    return sorted( createDivisorList( [ ], getFactorList( n ) ) )


# //******************************************************************************
# //
# //  getNthLucasNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthLucasNumber( n ):
    if real( n ) == 0:
        return 2
    elif n == 1:
        return 1
    else:
        precision = int( fdiv( fmul( n, 2 ), 8 ) )

        if ( mp.dps < precision ):
            mp.dps = precision

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

@oneArgFunctionEvaluator( )
def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], fadd( real( n ), 1 ) )


# //******************************************************************************
# //
# //  getNthBaseKRepunit
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( real( k ) ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


# //******************************************************************************
# //
# //  getPrimePi
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getPrimePi( n ):
    return primepi( real( n ) )


# //******************************************************************************
# //
# //  getNthFibonacci
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthFibonacci( n ):
    return fib( real_int( n ) )


# //******************************************************************************
# //
# //  getNthFibonacciPolynomial
# //
# //  http://mathworld.wolfram.com/Fibonaccin-StepNumber.html
# //  http://oeis.org/A118745
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthFibonacciPolynomial( n ):
    if real( n ) < 2:
        raise ValueError( 'argument >= 2 expected' )
    elif n == 2:
        return [ 2, -1 ]
    else:
        result = [ ]

        i = int( n )

        for j in range( -1, i - 3 ):
            result.append( j )

        result.append( ( i - 1 ) * 2 )
        result.append( -1 )

        return result


# //******************************************************************************
# //
# //  getNthKFibonacciNumber
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthKFibonacciNumber( n, k ):
    if real( n ) < 0:
        raise ValueError( 'non-negative argument expected' )

    if real( k ) < 2:
        raise ValueError( 'argument <= 2 expected' )

    if n < k - 1:
        return 0

    nth = int( n ) + 4

    precision = int( fdiv( fmul( n, k ), 8 ) )

    if ( mp.dps < precision ):
        mp.dps = precision

    poly = [ 1 ]
    poly.extend( [ -1 ] * int( k ) )

    roots = polyroots( poly )
    nthPoly = getNthFibonacciPolynomial( k )

    result = 0
    exponent = fsum( [ nth, fneg( k ), -2 ] )

    for i in range( 0, int( k ) ):
        result += fdiv( power( roots[ i ], exponent ), polyval( nthPoly, roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )

@oneArgFunctionEvaluator( )
def getNthTribonacci( n ):
    return getNthKFibonacciNumber( n, 3 )

@oneArgFunctionEvaluator( )
def getNthTetranacci( n ):
    return getNthKFibonacciNumber( n, 4 )

@oneArgFunctionEvaluator( )
def getNthPentanacci( n ):
    return getNthKFibonacciNumber( n, 5 )

@oneArgFunctionEvaluator( )
def getNthHexanacci( n ):
    return getNthKFibonacciNumber( n, 6 )

@oneArgFunctionEvaluator( )
def getNthHeptanacci( n ):
    return getNthKFibonacciNumber( n, 7 )

@oneArgFunctionEvaluator( )
def getNthOctanacci( n ):
    return getNthKFibonacciNumber( n, 8 )


# //******************************************************************************
# //
# //  getNthKFibonacciNumberTheSlowWay
# //
# //******************************************************************************

def getNthKFibonacciNumberTheSlowWay( n, k ):
    '''
    This is used for testing getNthKFibonacciNumber( ).
    '''
    precision = int( fdiv( fmul( real( n ), real( k ) ), 8 ) )

    if ( mp.dps < precision ):
        mp.dps = precision

    return getNthLinearRecurrence( [ 1 ] * int( k ), [ 0 ] * ( int( k ) - 1 ) + [ 1 ], fadd( n, 1 ) )


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

@oneArgFunctionEvaluator( )
def getNthPadovanNumber( arg ):
    n = fadd( real( arg ), 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    e = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, e ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, e ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, e ) ) )

    return nint( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                             fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                             fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )


# //******************************************************************************
# //
# //  RPNContinuedFraction
# //
# //  adapted from ActiveState Python, recipe 578647
# //
# //******************************************************************************

class RPNContinuedFraction( list ):
    '''This class represents a continued fraction as a list of integer terms.'''
    def __init__( self, value, maxterms = 15, cutoff = 1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            if mp.dps < maxterms:
                mp.dps = maxterms

            self.extend( value )
        else:
            raise ValueError( 'RPNContinuedFraction requires a number or a list' )

    def getFraction( self, terms = None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


# //******************************************************************************
# //
# //  convertFromContinuedFraction
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertFromContinuedFraction( n ):
    if not isinstance( n, list ):
        n = [ n ]

    if ( len( n ) == 1 ) and ( n[ 0 ] <= 0 ):
        raise ValueError( "invalid input for evaluating a continued fraction" )

    fraction = RPNContinuedFraction( n ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


# //******************************************************************************
# //
# //  makeContinuedFraction
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def makeContinuedFraction( n, k ):
    return RPNContinuedFraction( real( n ), maxterms = real_int( k ), cutoff = power( 10, -( mp.dps - 2 ) ) )


# //******************************************************************************
# //
# //  interpretAsFraction
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def interpretAsFraction( n, k ):
    if ( mp.dps < real_int( k ) ):
        mp.dps = k

    fraction = RPNContinuedFraction( real( n ), maxterms = k ).getFraction( )
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
        args.reverse( )
    else:
        args = [ args ]

    if isinstance( base, list ):
        return [ interpretAsBase( args, i ) for i in base ]

    value = mpmathify( 0 )
    multiplier = mpmathify( 1 )

    for i in args:
        if i >= real_int( base ):
            raise ValueError( 'invalid value for base', int( base ) )

        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


@twoArgFunctionEvaluator( )
def interpretAsBaseOperator( args, base ):
    return interpretAsBase( args, base )


# //******************************************************************************
# //
# //  getGreedyEgyptianFraction
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getGreedyEgyptianFraction( n, d ):
    if real( n ) > real( d ):
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
# //  getLinearRecurrence
# //
# //  Fibonacci sequence = rpn [ 1 1 ] 1 n linear
# //  Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n linear
# //
# //******************************************************************************

def getLinearRecurrence( recurrence, seeds, count ):
    if not isinstance( recurrence, ( list, RPNGenerator ) ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, ( list, RPNGenerator ) ):
        seeds = [ seeds ]

    if not seeds:
        raise ValueError( 'for operator \'linear_recurrence\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( list( getLinearRecurrence( recurrence[ : i ], seeds, 1 ) ) )

    if real_int( count ) < len( seeds ):
        for i in range( int( count ) ):
            yield seeds[ i ]
    else:
        if not recurrence:
            raise ValueError( 'internal error:  for operator \'linear_recurrence\', '
                              'recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in seeds:
            yield i

        for i in arange( len( seeds ), count ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

            result.append( newValue )
            yield newValue

            del result[ 0 ]


# //******************************************************************************
# //
# //  getNthLinearRecurrence
# //
# //******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    return list( getLinearRecurrence( recurrence, seeds, n ) )[ -1 ]


# //******************************************************************************
# //
# //  getLinearRecurrenceWithModulo
# //
# //******************************************************************************

def getLinearRecurrenceWithModulo( recurrence, seeds, count, modulo ):
    if not isinstance( recurrence, ( list, RPNGenerator ) ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, ( list, RPNGenerator ) ):
        seeds = [ seeds ]

    if not seeds:
        raise ValueError( 'for operator \'linear_recurrence_with_modulo\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getLinearRecurrenceWithModulo( recurrence[ : i ], seeds, i, modulo ) )

    if real_int( count ) < len( seeds ):
        for i in range( int( count ) ):
            yield seeds[ i ]
    else:
        if not recurrence:
            raise ValueError( 'internal error:  for operator \'linear_recurrence_with_modulo\', '
                              'recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in seeds:
            yield i

        for i in arange( len( seeds ), count ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fmod( fadd( newValue, fmul( result[ j ], recurrence[ j ] ) ), modulo )

            result.append( newValue )
            yield newValue

            del result[ 0 ]


# //******************************************************************************
# //
# //  getGeometricRecurrence
# //
# //******************************************************************************

def getGeometricRecurrence( recurrence, powers, seeds, count ):
    if not isinstance( recurrence, ( list, RPNGenerator ) ):
        recurrence = [ recurrence ]

    if not isinstance( powers, ( list, RPNGenerator ) ):
        powers = [ powers ]

    if not isinstance( seeds, ( list, RPNGenerator ) ):
        seeds = [ seeds ]

    if not seeds:
        raise ValueError( 'for operator \'linear_recurrence\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( list( getLinearRecurrence( recurrence[ : i ], seeds, 1 ) ) )

    if real_int( count ) < len( seeds ):
        for i in range( int( count ) ):
            yield seeds[ i ]
    else:
        if not recurrence:
            raise ValueError( 'internal error:  for operator \'linear_recurrence\', '
                              'recurrence list cannot be empty ' )

        if not powers:
            raise ValueError( 'internal error:  for operator \'geometric_recur\', '
                              'powers list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in seeds:
            yield i

        for i in arange( len( seeds ), count ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fadd( newValue, fmul( power( result[ j ], powers[ j ] ), recurrence[ j ] ) )

            result.append( newValue )
            yield newValue

            del result[ 0 ]


# //******************************************************************************
# //
# //  makePythagoreanTriple
# //
# //  Euclid's formula
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Pythag/pythag.html#mnformula
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def makePythagoreanTriple( n, k ):
    if real( n ) < 0 or real( k ) < 0:
        raise ValueError( "'make_pyth_3' requires positive arguments" )

    if n == k:
        raise ValueError( "'make_pyth_3' requires unequal arguments" )

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

@twoArgFunctionEvaluator( )
def makePythagoreanQuadruple( a, b ):
    if a < 0 or b < 0:
        raise ValueError( "'make_pyth_4' requires positive arguments" )

    # if a == b:
    #     raise ValueError( "'make_pyth_4' requires unequal arguments" )

    odd1 = ( fmod( a, 2 ) == 1 )
    odd2 = ( fmod( b, 2 ) == 1 )

    if odd1 and odd2:
        raise ValueError( "'make_pyth_4' arguments cannot both be odd" )

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
            raise ValueError( "'make_pyth_4' oops, can't make one!" )
        else:
            div = [ i for i in div[ : ( len( div ) - 1 ) // 2 ] if fmod( sumsqr, fmul( i, 2 ) ) == 0 and fmod( i, 2 ) == 0 ]
            p = random.choice( div )

    psqr = fmul( p, p )
    result.append( fdiv( fsub( sumsqr, psqr ), fmul( p, 2 ) ) )
    result.append( fdiv( fadd( sumsqr, psqr ), fmul( p, 2 ) ) )

    return sorted( result )


# //******************************************************************************
# //
# //  makeEulerBrick
# //
# //  http://mathworld.wolfram.com/EulerBrick.html
# //
# //  Saunderson's solution lets (a',b',c') be a Pythagorean triple, then
# //  ( a, b, c ) = ( a'( 4b'^2 - c'^2 ), ( b'( 4a'^2 ) - c'^2 ), 4a'b'c' )
# //
# //******************************************************************************

def makeEulerBrick( _a, _b, _c ):
    a, b, c = sorted( [ real( _a ), real( _b ), real( _c ) ] )

    if fadd( power( a, 2 ), power( b, 2 ) ) != power( c, 2 ):
        raise ValueError( "'euler_brick' requires a pythogorean triple" )

    result = [ ]

    a2 = fmul( a, a )
    b2 = fmul( b, b )
    c2 = fmul( c, c )

    result.append( fabs( fmul( a, fsub( fmul( 4, b2 ), c2 ) ) ) )
    result.append( fabs( fmul( b, fsub( fmul( 4, a2 ), c2 ) ) ) )
    result.append( fprod( [ 4, a, b, c ] ) )

    return sorted( result )


# //******************************************************************************
# //
# //  getNthFibonorial
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthFibonorial( n ):
    result = 1

    for i in arange( 2, real( n ) ):
        result = fmul( result, fib( i ) )

    return result


# //******************************************************************************
# //
# //  getGCDOfList
# //
# //******************************************************************************

def getGCDOfList( args ):
    if ( isinstance( args, RPNGenerator ) ):
        args = list( args )

    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getGCDOfList( real( arg ) ) for arg in args ]
    else:
        result = max( args )

        for pair in itertools.combinations( args, 2 ):
            gcd = getGCD( *pair )

            if gcd < result:
                result = gcd

        return result

@twoArgFunctionEvaluator( )
def getGCD( n, k ):
    while k:
        n, k = k, fmod( n, k )

    return n


# //******************************************************************************
# //
# //  getExtendedGCD
# //
# //  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getExtendedGCD( a, b ):
    '''
    Euclid's Extended GCD Algorithm

    >>> xgcd(314159265, 271828186)
    (-18013273, 20818432, 7)
    '''
    u, u1 = 1, 0
    v, v1 = 0, 1

    while b != 0:
        q = floor( fdiv( a, b ) )
        r = fmod( a, b )
        a, b = b, r
        u, u1 = u1, fsub( u, fmul( q, u1 ) )
        v, v1 = v1, fsub( v, fmul( q, v1 ) )

    return ( u, v, a ) if a > 0 else ( -u, -v, -a )


# //******************************************************************************
# //
# //  getLCM
# //
# //******************************************************************************

def getLCMOfList( args ):
    if isinstance( args, RPNGenerator ):
        return getLCMOfList( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getLCMOfList( arg ) for arg in args ]
        else:
            result = 1

            for arg in args:
                result = result * arg / getGCD( result, arg )

            return result
    else:
        return args

@twoArgFunctionEvaluator( )
def getLCM( n, k ):
    return getLCMOfList( [ n, k ] )


# //******************************************************************************
# //
# //  getFrobeniusNumber
# //
# //  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
# //
# //  Since this is classified as a list operator, it has to behave like the
# //  other operators in rpnList.py.
# //
# //******************************************************************************

def getFrobeniusNumber( args ):
    '''
    http://ccgi.gladman.plus.com/wp/?page_id=1500

    For the integer sequence (a[0], a[1], ...) with a[0] < a[1] < ... < a[n],
    return the largest number, N, that cannot be expressed in the form:
    N = sum(m[i] * x[i]) where all m[i] are non-negative integers.

    >>> frobenius_number( [ 9949, 9967, 9973 ] )
    24812836

    >>> frobenius_number( [ 6, 9, 20 ] )
    43

    >>> frobenius_number( [ 5, 8, 15 ] )
    27

    frobenius_number( [ 5, 8, 9, 12 ] )
    11
    '''

    if isinstance( args, RPNGenerator ):
        args = list( args )

    if isinstance( args, list ):
        if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
            return [ getFrobeniusNumber( arg ) for arg in args ]
        else:
            a = [ ]

            if getGCDOfList( args ) > 1:
                raise ValueError( "the 'frobenius' operator is only valid for lists of values that contain at least one pair of coprime values" )

            for i in sorted( args ):
                a.append( int( i ) )

            def __residue_table( a ):
                n = [ 0 ] + [ None ] * ( a[ 0 ] - 1 )

                for i in range( 1, len( a ) ):
                    d = int( getGCD( a[ 0 ], a[ i ] ) )
                    for r in range( d ):
                        try:
                            nn = min( n[ q ] for q in range( r, a[ 0 ], d ) if n[ q ] is not None )
                        except ValueError:
                            continue

                        if nn is not None:
                            for c in range( a[ 0 ] // d ):
                                nn += a[ i ]
                                p = nn % a[ 0 ]
                                nn = min( nn, n[ p ] ) if n[ p ] is not None else nn
                                n[ p ] = nn
                return [ i for i in n if i is not None ]

            return max( __residue_table( sorted( a ) ) ) - min( a )
    else:
        return 1 if args > 1 else -1


# //******************************************************************************
# //
# //  _crt
# //
# //  Helper function for calculateChineseRemainderTheorem
# //
# //******************************************************************************

def _crt( a, b, m, n ):
    d = getGCD( m, n )

    if fmod( fsub( a, b ), d ) != 0:
        return None

    x = floor( fdiv( m, d ) )
    y = floor( fdiv( n, d ) )
    z = floor( fdiv( fmul( m, n ), d ) )
    p, q, r = getExtendedGCD( x, y )

    return fmod( fadd( fprod( [ b, p, x ] ), fprod( [ a, q, y ] ) ), z )


# //******************************************************************************
# //
# //  calculateChineseRemainderTheorem
# //
# //  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
# //
# //  Since this is classified as a list operator, it has to behave like the
# //  other operators in rpnList.py.
# //
# //******************************************************************************

def calculateChineseRemainderTheorem( values, mods ):
    '''
    The Chinese Remainder Theorem (CRT)

    Solve the equations x = a[i] mod m[i] for x

    >>> crt((2, 3, 5, 7), (97, 101, 103, 107))
    96747802
    '''

    if isinstance( values, list ) != isinstance( mods, list ):
        raise ValueError( "the 'crt' operator requires arguments that are both lists" )

    if not isinstance( values, list ):
        return calculateChineseRemainderTheorem( [ values ], [ mods ] )

    if isinstance( values[ 0 ], list ):
        if isinstance( mods[ 0 ], list ):
            return [ calculateChineseRemainderTheorem( i, j ) for i in values for j in mods ]
        else:
            return [ calculateChineseRemainderTheorem( i, mods ) for i in values ]
    else:
        if isinstance( mods[ 0 ], list ):
            return [ calculateChineseRemainderTheorem( values, j ) for j in mods ]

    if len( values ) != len( mods ):
        raise ValueError( "the 'crt' operator requires arguments that are both lists of the same length" )

    x = values[ 0 ]
    mm = mods[ 0 ]

    for i in range( 1, len( values ) ):
        x = _crt( values[ i ], x, mods[ i ], mm )

        if not x:
            break

        mm = getLCM( [ mods[ i ], mm ] )

    return x

@twoArgFunctionEvaluator( )
def calculateChineseRemainderTheoremOperator( values, mods ):
    return calculateChineseRemainderTheorem( values, mods )


# //******************************************************************************
# //
# //  getRadical
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getRadical( target ):
    '''
    Returns the value of the radical function for n, which is the largest
    squarefree divisor.
    '''

    n = floor( target )

    if real( n ) == 0:
        return 0
    elif n == 1:
        return 1

    factors = set( getFactors( n ) )

    result = 1

    for i in factors:
        result = fmul( result, i )

    return result


# //******************************************************************************
# //
# //  getSigma
# //
# //******************************************************************************

@cachedFunction( 'sigma' )
def getSigma( target ):
    '''
    Returns the sum of the divisors of n, including 1 and n.

    http://math.stackexchange.com/questions/22721/is-there-a-formula-to-calculate-the-sum-of-all-proper-divisors-of-a-number
    '''
    n = floor( target )

    if real( n ) == 0:
        return 0
    elif n == 1:
        return 1

    factorList = getFactorList( n )

    result = 1

    for factor in factorList:
        numerator = fsub( power( factor[ 0 ], fadd( factor[ 1 ], 1 ) ), 1 )
        denominator = fsub( factor[ 0 ], 1 )
        #debugPrint( 'sigma', numerator, denominator )
        result = fmul( result, fdiv( numerator, denominator ) )

        if result != floor( result ):
            raise ValueError( 'insufficient precision for \'sigma\', increase precision using -p or -a)' )

    return result

@oneArgFunctionEvaluator( )
def getSigmaOperator( n ):
    return getSigma( n )

@oneArgFunctionEvaluator( )
def getAbundanceRatio( n ):
    return fdiv( getSigma( n ), n )


# //******************************************************************************
# //
# //  getSigmaN
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getSigmaN( n, k ):
    '''
    Returns the sum of the divisors of n, including 1 and n, to the k power.

    https://oeis.org/A001157
    '''
    if real( n ) == 0:
        return 0
    elif n == 1:
        return 1

    factorList = getFactorList( n )

    result = 1

    for factor in factorList:
        numerator = fsub( power( factor[ 0 ], fmul( fadd( factor[ 1 ], 1 ), k ) ), 1 )
        denominator = fsub( power( factor[ 0 ], k ), 1 )
        result = fmul( result, fdiv( numerator, denominator ) )

        if result != floor( result ):
            raise ValueError( 'insufficient precision for \'sigma_n\', increase precision using -p or -a)' )

    return result


# //******************************************************************************
# //
# //  getAliquotSequenceGenerator
# //
# //******************************************************************************

def getAliquotSequenceGenerator( n, k ):
    '''
    The aliquot sum of n is the sum of the divisors of n, not counting n itself
    as a divisor.  Subsequent aliquot sums can then be computed.  These sequences
    usually terminate, but some, like 276, get so large it has not been determined
    if they ever terminate.
    '''
    yield real( floor( n ) )

    a = n

    for i in arange( 0, real( k ) - 1 ):
        b = fsub( getSigma( a ), a )
        yield b
        a = b

@twoArgFunctionEvaluator( )
def getAliquotSequence( n, k ):
    return RPNGenerator.createGenerator( getAliquotSequenceGenerator, [ n, k ] )


# //******************************************************************************
# //
# //  getMobius
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'mobius' )
def getMobius( n ):
    if real( n ) == 1:
        return 1

    factorList = getFactorList( n )

    for i in factorList:
        if i[ 1 ] > 1:
            return 0

    if len( factorList ) % 2:
        return -1
    else:
        return 1


# //******************************************************************************
# //
# //  getNthMerten
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'merten' )
def getNthMerten( n ):
    if real( n ) == 1:
        return 1

    result = 0

    for i in arange( 1, n + 1 ):
        result = fadd( result, getMobius( i ) )

    return result


# //******************************************************************************
# //
# //  getEulerPhi
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'euler_phi' )
def getEulerPhi( n ):
    if real( n ) < 2:
        return n

    return reduce( fmul, ( fmul( fsub( i[ 0 ], 1 ), power( i[ 0 ], fsub( i[ 1 ], 1 ) ) ) for i in getFactorList( n ) ) )


# //******************************************************************************
# //
# //  getPowMod
# //
# //******************************************************************************

def getPowMod( a, b, c ):
    return pow( real_int( a ), real_int( b ), real_int( c ) )


# //******************************************************************************
# //
# //  getAbundance
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'abundance' )
def getAbundance( n ):
    if real_int( n ) < 2:
        return 0

    return fsub( getSigma( n ), fmul( n, 2 ) )


# //******************************************************************************
# //
# //  isDeficient
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isDeficient( n ):
    if real_int( n ) < 1:
        return 0
    elif n == 1:
        return 1

    return 1 if getAbundance( n ) < 0 else 0


# //******************************************************************************
# //
# //  isAbundant
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isAbundant( n ):
    if real_int( n ) < 2:
        return 0

    return 1 if getAbundance( n ) > 0 else 0


# //******************************************************************************
# //
# //  isPerfect
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isPerfect( n ):
    if real_int( n ) < 2:
        return 0

    return 1 if getAbundance( n ) == 0 else 0


# //******************************************************************************
# //
# //  isSmooth
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
@cachedFunction( 'smooth' )
def isSmooth( n, k ):
    if real_int( n ) <= real_int( k ):
        return 1

    return 1 if max( [ i[ 0 ] for i in getFactorList( n ) ] ) <= k else 0


# //******************************************************************************
# //
# //  isRough
# //
# //  https://en.wikipedia.org/wiki/Rough_number
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
@cachedFunction( 'rough' )
def isRough( n, k ):
    if real_int( n ) == 1:
        return 1
    elif n < real_int( k ):
        return 0

    return 1 if min( [ i[ 0 ] for i in getFactorList( n ) ] ) >= k else 0


# //******************************************************************************
# //
# //  isKSemiPrime
# //
# //******************************************************************************

@cachedFunction( 'k_semiprime' )
def isKSemiPrime( n, k ):
    return 1 if sum( [ i[ 1 ] for i in getFactorList( n ) ] ) == k else 0

@twoArgFunctionEvaluator( )
def isKSemiPrimeOperator( n, k ):
    return isKSemiPrime( n, k )

@oneArgFunctionEvaluator( )
def isSemiPrime( n ):
    return isKSemiPrime( n, 2 )


# //******************************************************************************
# //
# //  isKSphenic
# //
# //******************************************************************************

@cachedFunction( 'k_sphenic' )
def isKSphenic( n, k ):
    factorList = getFactorList( n )

    if len( factorList ) != k:
        return 0

    return 1 if max( [ i[ 1 ] for i in factorList ] ) == 1 else 0

@oneArgFunctionEvaluator( )
def isSphenic( n ):
    return isKSphenic( n, 3 )

@twoArgFunctionEvaluator( )
def isKSphenicOperator( n, k ):
    return isKSphenic( n, k )


# //******************************************************************************
# //
# //  isSquareFree
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'squarefree' )
def isSquareFree( n ):
    if real_int( n ) == 0:
        return 0

    return 1 if max( [ i[ 1 ] for i in getFactorList( n ) ] ) == 1 else 0


# //******************************************************************************
# //
# //  isPowerful
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'powerful' )
def isPowerful( n ):
    return 1 if min( [ i[ 1 ] for i in getFactorList( n ) ] ) >= 2 else 0


# //******************************************************************************
# //
# //  isAchillesNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'achilles' )
def isAchillesNumber( n ):
    factorList = getFactorList( n )

    if min( [ i[ 1 ] for i in factorList ] ) < 2:
        return 0

    return 1 if getGCDOfList( [ i[ 1 ] for i in factorList ] ) == 1 else 0


# //******************************************************************************
# //
# //  isUnusual
# //
# //  https://en.wikipedia.org/wiki/Unusual_number
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'unusual' )
def isUnusual( n ):
    if real_int( n ) < 2:
        return 0

    return 1 if max( [ i[ 0 ] for i in getFactorList( n ) ] ) > sqrt( n ) else 0


# //******************************************************************************
# //
# //  isPronic
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isPronic( n ):
    a = floor( sqrt( real_int( n ) ) )
    return 1 if n == fmul( a, fadd( a, 1 ) ) else 0


# //******************************************************************************
# //
# //  isPolydivisible
# //
# //  It seems to be about 10% faster on average to do the division tests in
# //  reverse order.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'polydivisible' )
def isPolydivisible( n ):
    if real_int( n ) < 0:
        raise ValueError( 'non-negative, real integer expected' )

    strValue = getMPFIntegerAsString( n )

    # a couple of cheats
    if ( len( strValue ) > 4 ) and ( strValue[ 4 ] not in [ '5', '0' ] ):
        return 0

    if ( len( strValue ) > 9 ) and ( strValue[ 9 ] != '0' ):
        return 0

    for i in range( len( strValue ), 1, -1 ):
        current = mpmathify( strValue[ : i ] )

        if not isDivisible( current, i ):
            return 0

    return 1


# //******************************************************************************
# //
# //  splitNumber
# //
# //******************************************************************************

def splitNumber( value, base ):
    result = [ ]

    while value:
        digit = fmod( value, base )
        result.append( digit )
        value = fdiv( fsub( value, digit ), base )

    return result


# //******************************************************************************
# //
# //  joinNumber
# //
# //******************************************************************************

def joinNumber( digits, base ):
    place = 1
    result = 0

    for digit in digits:
        result = fadd( result, fmul( digit, place ) )
        place = fmul( place, base )

    return result


# //******************************************************************************
# //
# //  generatePolydivisiblesGenerator
# //
# //******************************************************************************

def generatePolydivisiblesGenerator( _base ):
    base = int( _base )
    result = list( range( 1, base ) )
    newItems = list( range( 1, base ) )

    for i in newItems:
        yield i

    while newItems:
        newCandidates = [ ]

        while newItems:
            item = newItems.pop( 0 )
            digits = splitNumber( item, base )

            place = len( digits ) + 1

            if place % base == 0:
                newDigits = [ 0 ]
            elif base > 2 and isDivisible( base, 2 ):
                if place % ( base / 2 ) == 0:
                    newDigits = [ 0, base / 2 ]
                elif place % 2 == 0:
                    newDigits = list( range( 0, base, 2 ) )
                else:
                    newDigits = list( range( 0, base ) )
            else:
                newDigits = list( range( 0, base ) )

            newCandidateBase = fmul( item, base )

            for digit in newDigits:
                testMe = fadd( newCandidateBase, digit )

                if isDivisible( testMe, place ):
                    newCandidates.append( testMe )
                    yield testMe

        newItems = newCandidates

        newCandidates = [ ]

@oneArgFunctionEvaluator( )
def generatePolydivisibles( n ):
    return RPNGenerator.createGenerator( generatePolydivisiblesGenerator, n )


# //******************************************************************************
# //
# //  getNthStern
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'stern' )
def getNthStern( n ):
    '''Returns the nth number of Stern's diatomic series recursively.'''
    if real_int( n ) < 0:
        raise ValueError( 'non-negative, real integer expected' )

    if n in [ 0, 1 ]:
        return n
    elif n % 2 == 0: # even
        return getNthStern( floor( fdiv( n, 2 ) ) )
    else:
        return fadd( getNthStern( floor( fdiv( fsub( n, 1 ), 2 ) ) ),
                     getNthStern( floor( fdiv( fadd( n, 1 ), 2 ) ) ) )


# //******************************************************************************
# //
# //  getNthCalkinWilf
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCalkinWilf( n ):
    if real_int( n ) < 0:
        raise ValueError( 'non-negative, real integer expected' )

    if n == 0:
        return [ 0, 1 ]

    return [ getNthStern( n ), getNthStern( fadd( n, 1 ) ) ]


# //******************************************************************************
# //
# //  isFriendly
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'friendly' )
def isFriendly( n ):
    first = True

    abundance = 0

    for i in n:
        if first:
            abundance = fdiv( getSigma( i ), i )
            first = False
        elif fdiv( getSigma( i ), i ) != abundance:
            return 0

    return 1


# //******************************************************************************
# //
# //  isKHyperperfect
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
@cachedFunction( 'k_hyperperfect' )
def isKHyperperfect( n, k ):
    return 1 if fadd( fmul( k, fsub( getSigma( n ), fadd( n, 1 ) ) ), 1 ) == n else 0


# //******************************************************************************
# //
# //  getNthZetaZero
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthZetaZero( n ):
    return zetazero( int( n ) )


# //******************************************************************************
# //
# //  getNthMersennePrime
# //
# //******************************************************************************

mersennePrimeExponents = {
    1:   2,
    2:   3,
    3:   5,
    4:   7,
    5:   13,
    6:   17,
    7:   19,
    8:   31,
    9:   61,
    10:  89,
    11:  107,
    12:  127,
    13:  521,
    14:  607,
    15:  1279,
    16:  2203,
    17:  2281,
    18:  3217,
    19:  4253,
    20:  4423,
    21:  9689,
    22:  9941,
    23:  11213,
    24:  19937,
    25:  21701,
    26:  23209,
    27:  44497,
    28:  86243,
    29:  110503,
    30:  132049,
    31:  216091,
    32:  756839,
    33:  859433,
    34:  1257787,
    35:  1398269,
    36:  2976221,
    37:  3021377,
    38:  6972593,
    39:  13466917,
    40:  20996011,
    41:  24036583,
    42:  25964951,
    43:  30402457,
    44:  32582657,
    45:  37156667,
    46:  42643801,
    47:  43112609,
    48:  57885161,
    49:  74207281,
}

@oneArgFunctionEvaluator( )
def getNthMersenneExponent( n ):
    if 1 > real_int( n ) > 49:
        raise ValueError( 'invalid index for known Mersenne primes (1 to 49)' )

    return mersennePrimeExponents[ n ]


@oneArgFunctionEvaluator( )
def getNthMersennePrime( n ):
    return fsub( power( 2, getNthMersenneExponent( n ) ), 1 )


@oneArgFunctionEvaluator( )
def getNthPerfectNumber( n ):
    exponent = getNthMersenneExponent( n )
    return fmul( fsub( power( 2, exponent ), 1 ), power( 2, fsub( exponent, 1 ) ) )


# //******************************************************************************
# //
# //  getNthThueMorse
# //
# //  https://en.wikipedia.org/wiki/Thue%E2%80%93Morse_sequence
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
@cachedFunction( 'thue_morse' )
def getNthThueMorse( n ):
    if n == 0:
        return 0
    else:
        return fmod( fadd( n, getNthThueMorse( floor( fdiv( n, 2 ) ) ) ), 2 )


# //******************************************************************************
# //
# //  findSumsOfKPowersGenerator
# //
# //******************************************************************************

def findSumsOfKPowersGenerator( n, k, p, bNonZero=False ):
    limit = fadd( floor( root( n, p ) ), 1 )

    lower = fsub( limit, 1 )
    upper = fmul( limit, 2 )

    candidates = arange( 1 if bNonZero else 0, limit )

    l = itertools.combinations_with_replacement( candidates, int( k ) )

    for a in l:
        #sum = fsum( a )
        #
        #if lower > sum > upper:
        #    continue

        if fsum( [ power( i, p ) for i in a ] ) == n:
            yield list( a )

def findSumsOfKPowers( n, k, p ):
    return RPNGenerator( findSumsOfKPowersGenerator( n, k, p ) )

def findSumsOfKNonzeroPowers( n, k, p ):
    return RPNGenerator( findSumsOfKPowersGenerator( n, k, p, bNonZero = True ) )


@oneArgFunctionEvaluator( )
def getBarnesG( n ):
    return barnesg( n )

@twoArgFunctionEvaluator( )
def getBeta( n, k ):
    return beta( n, k )

@twoArgFunctionEvaluator( )
def getCyclotomic( n, k ):
    return cyclotomic( n, k )

@oneArgFunctionEvaluator( )
def getDigamma( n ):
    return psi( 0, n )

@oneArgFunctionEvaluator( )
def getDoubleFactorial( n ):
    return fac2( n )

@oneArgFunctionEvaluator( )
def getAltZeta( n ):
    return altzeta( n )

@oneArgFunctionEvaluator( )
def getFactorial( n ):
    return fac( n )

@oneArgFunctionEvaluator( )
def getGamma( n ):
    return gamma( n )

@oneArgFunctionEvaluator( )
def getHarmonic( n ):
    return harmonic( n )

@oneArgFunctionEvaluator( )
def getHyperfactorial( n ):
    return hyperfac( n )

@twoArgFunctionEvaluator( )
def getLeyland( n, k ):
    return fadd( power( n, k ), power( k, n ) )

@oneArgFunctionEvaluator( )
def getLogGamma( n ):
    return loggamma( n )

@oneArgFunctionEvaluator( )
def getNthCarol( n ):
    return fsub( power( fsub( power( 2, real( n ) ), 1 ), 2 ), 2 )

@oneArgFunctionEvaluator( )
def getNthKynea( n ):
    return fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 )

@oneArgFunctionEvaluator( )
def getNthLeonardo( n ):
    return fsub( fmul( 2, fib( fadd( n, 1 ) ) ), 1 )

@twoArgFunctionEvaluator( )
def getPolygamma( n, k ):
    return psi( n, k )

@oneArgFunctionEvaluator( )
def getNthRiesel( n ):
    return fsub( fmul( real( n ), power( 2, n ) ), 1 )

@oneArgFunctionEvaluator( )
def getSubfactorial( n ):
    return floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) )

@oneArgFunctionEvaluator( )
def getSuperfactorial( n ):
    return superfac( n )

@oneArgFunctionEvaluator( )
def getNthThabit( n ):
    return fsub( fmul( 3, power( 2, n ) ), 1 )

@oneArgFunctionEvaluator( )
def getTrigamma( n ):
    return psi( 1, n )

@oneArgFunctionEvaluator( )
def getUnitRoots( n ):
    return unitroots( real_int( n ) )

@oneArgFunctionEvaluator( )
def getZeta( n ):
    return zeta( n )

@twoArgFunctionEvaluator( )
def getHurwitzZeta( n, k ):
    return zeta( n, k )


# //******************************************************************************
# //
# //  getCollatzSequenceGenerator
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getCollatzSequenceGenerator( n, k ):

    if n == 0:
        return

    a = n

    for i in arange( 0, real( k ) - 1 ):
        if isEven( a ):
            b = fdiv( a, 2 )
        else:
            b = fadd( fmul( 3, a ), 1 )

        yield b

        if b == 1:
            return

        a = b

@twoArgFunctionEvaluator( )
def getCollatzSequence( n, k ):
    return RPNGenerator.createGenerator( getCollatzSequenceGenerator, [ n, k ] )


