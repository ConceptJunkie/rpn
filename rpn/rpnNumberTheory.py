#!/usr/bin/env python

#******************************************************************************
#
#  rpnNumberTheory.py
#
#  rpnChilada number theory operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import random

from fractions import Fraction
from functools import reduce

import numpy as np

from mpmath import altzeta, arange, barnesg, beta, binomial, ceil, e, fabs, fac, fac2, fadd, fdiv, fib, \
                   floor, fmod, fmul, fneg, fprod, fsub, fsum, gamma, harmonic, hyperfac, libmp, log, log10, \
                   loggamma, mp, mpc, mpf, mpmathify, nint, phi, polyroots, polyval, power, primepi2, psi, re, root, \
                   superfac, sqrt, unitroots, zeta, zetazero

from rpn.rpnComputer import getBitCount
from rpn.rpnFactor import getFactors, getFactorList
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnList import getGCD, getGCDOfList, calculatePowerTowerRight, reduceList
from rpn.rpnMath import isDivisible, isEven, isInteger, isOdd
from rpn.rpnPersistence import cachedFunction
from rpn.rpnPrimeUtils import findPrime, getNthPrime, isPrime
from rpn.rpnUtils import getMPFIntegerAsString, listArgFunctionEvaluator, \
                         listAndOneArgFunctionEvaluator, oneArgFunctionEvaluator, setAccuracyForN, \
                         twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, ComplexValidator, IntValidator, ListValidator, RealValidator


#******************************************************************************
#
#  getNthAlternatingFactorial
#
#******************************************************************************

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


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthAlternatingFactorialOperator( n ):
    return getNthAlternatingFactorial( n )


#******************************************************************************
#
#  getNthPascalLineGenerator
#
#******************************************************************************

def getNthPascalLineGenerator( n ):
    for i in arange( 0, n ):
        yield binomial( n - 1, i )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getNthPascalLineOperator( n ):
    return RPNGenerator.createGenerator( getNthPascalLineGenerator, n )


#******************************************************************************
#
#  getVanEckGenerator
#
#******************************************************************************

def getVanEckGenerator( n ):
    count = 0
    seen = [ 0 ]
    val = 0

    while count < n:
        yield val

        if val in seen[ 1 : ]:
            val = seen.index( val, 1 )
        else:
            val = 0

        seen.insert( 0, val )
        count += 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getVanEckOperator( n ):
    return RPNGenerator.createGenerator( getVanEckGenerator, n )


#******************************************************************************
#
#  getDivisorCount
#
#******************************************************************************

@cachedFunction( 'divisor_count' )
def getDivisorCount( n ):
    if n == 1:
        return 1

    return fprod( [ i[ 1 ] + 1 for i in getFactorList( n ) ] )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getDivisorCountOperator( n ):
    return getDivisorCount( n )


#******************************************************************************
#
#  createDivisorList
#
#******************************************************************************

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


#******************************************************************************
#
#  getDivisors
#
#******************************************************************************

def getDivisors( n ):
    if n == 0:
        return [ 0 ]
    elif n == 1:
        return [ 1 ]

    return sorted( createDivisorList( [ ], getFactorList( n ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getDivisorsOperator( n ):
    return getDivisors( n )


#******************************************************************************
#
#  getNthLucasNumber
#
#******************************************************************************

def getNthLucasNumber( n ):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        precision = int( fdiv( fmul( n, 2 ), 8 ) )

        if mp.dps < precision:
            mp.dps = precision

        return floor( fadd( power( phi, n ), 0.5 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthLucasNumberOperator( n ):
    return getNthLucasNumber( n )


#******************************************************************************
#
#  getNthJacobsthalNumber
#
#  From: http://oeis.org/A001045
#
#  a( n ) = ceiling( 2 ^ ( n + 1 ) / 3 ) - ceiling( 2 ^ n / 3 )
#
#******************************************************************************

def getNthJacobsthalNumber( n ):
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthJacobsthalNumberOperator( n ):
    return getNthJacobsthalNumber( n )


#******************************************************************************
#
#  getNthBaseKRepunitOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 2 ) ] )
def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( k ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], fsub( n, 1 ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 2 ) ] )
def getNthBaseKRepunitOperator( n, k ):
    return getNthBaseKRepunit( n, k )


#******************************************************************************
#
#  getPrimePi
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getPrimePiOperator( n ):
    # we can look it up and give an exact answer
    if n <= 60_000_000_000:  # max huge prime...
        result = findPrime( n )[ 0 ]

        if getNthPrime( result ) > n:
            result -= 1

        return result

    result = primepi2( n )

    if result.a == result.b:
        return mpf( result.a )
    else:
        return [ mpf( result.a ), mpf( result.b ) ]


#******************************************************************************
#
#  getNthFibonacci
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthFibonacciOperator( n ):
    return fib( n )


#******************************************************************************
#
#  getNthFibonacciPolynomial
#
#  http://mathworld.wolfram.com/Fibonaccin-StepNumber.html
#  http://oeis.org/A118745
#
#******************************************************************************

def getNthFibonacciPolynomial( n ):
    if n == 2:
        return [ 2, -1 ]

    result = [ ]

    i = int( n )

    for j in range( -1, i - 3 ):
        result.append( j )

    result.append( ( i - 1 ) * 2 )
    result.append( -1 )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )  # might need to be 2
def getNthFibonacciPolynomialOperator( n ):
    return getNthFibonacciPolynomial( n )


#******************************************************************************
#
#  getNthKFibonacciNumber
#
#******************************************************************************

def getNthKFibonacciNumber( n, k ):
    if n < k - 1:
        return 0

    nth = int( n ) + 4

    precision = int( fdiv( fmul( n, k ), 8 ) )

    if mp.dps < precision:
        mp.dps = precision

    poly = [ 1 ]
    poly.extend( [ -1 ] * int( k ) )

    try:
        roots = polyroots( poly )
    except libmp.libhyper.NoConvergence:
        try:
            #  Let's try again, really hard!
            roots = polyroots( poly, maxsteps = 2000, extraprec = 5000 )
        except libmp.libhyper.NoConvergence:
            raise ValueError( 'polynomial failed to converge' )

    nthPoly = getNthFibonacciPolynomial( k )

    result = 0
    exponent = fsum( [ nth, fneg( k ), -2 ] )

    for i in range( 0, int( k ) ):
        result += fdiv( power( roots[ i ], exponent ), polyval( nthPoly, roots[ i ] ) )

    return floor( fadd( re( result ), fdiv( 1, 2 ) ) )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def getNthKFibonacciNumberOperator( n, k ):
    return getNthKFibonacciNumber( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthTribonacciOperator( n ):
    return getNthKFibonacciNumber( n, 3 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthTetranacciOperator( n ):
    return getNthKFibonacciNumber( n, 4 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthPentanacciOperator( n ):
    return getNthKFibonacciNumber( n, 5 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthHexanacciOperator( n ):
    return getNthKFibonacciNumber( n, 6 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthHeptanacciOperator( n ):
    return getNthKFibonacciNumber( n, 7 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthOctanacciOperator( n ):
    return getNthKFibonacciNumber( n, 8 )


#******************************************************************************
#
#  getNthKFibonacciNumberTheSlowWay
#
#******************************************************************************

def getNthKFibonacciNumberTheSlowWay( n, k ):
    '''
    This is used for testing getNthKFibonacciNumber( ).
    '''
    precision = int( fdiv( fmul( int( n ), k ), 8 ) )

    if mp.dps < precision:
        mp.dps = precision

    return getNthLinearRecurrence( [ 1 ] * int( k ), [ 0 ] * ( int( k ) - 1 ) + [ 1 ], n )


#******************************************************************************
#
#  getNthPadovanNumber
#
#  Padovan sequence: a(n) = a(n-2) + a(n-3) with a(0)=1, a(1)=a(2)=0.
#
#  http://oeis.org/A000931
#
#  a(n) = (r^n)/(2r+3) + (s^n)/(2s+3) + (t^n)/(2t+3) where r, s, t are the
#  three roots of x^3-x-1
#
#  http://www.wolframalpha.com/input/?i=solve+x^3-x-1
#
#  Unfortunately, the roots are scary-complicated, but it's a non-iterative
#  formula, so I'll use it.
#
#  Wikipedia leaves off the first 4 terms, but Sloane's includes them.
#  Wikipedia cites Ian Stewart and Mathworld, and I'll use their definition.
#
#******************************************************************************

def getNthPadovanNumber( arg ):
    n = fadd( arg, 4 )

    a = root( fsub( fdiv( 27, 2 ), fdiv( fmul( 3, sqrt( 69 ) ), 2 ) ), 3 )
    b = root( fdiv( fadd( 9, sqrt( 69 ) ), 2 ), 3 )
    c = fadd( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    d = fsub( 1, fmul( mpc( 0, 1 ), sqrt( 3 ) ) )
    f = power( 3, fdiv( 2, 3 ) )

    r = fadd( fdiv( a, 3 ), fdiv( b, f ) )
    s = fsub( fmul( fdiv( d, -6 ), a ), fdiv( fmul( c, b ), fmul( 2, f ) ) )
    t = fsub( fmul( fdiv( c, -6 ), a ), fdiv( fmul( d, b ), fmul( 2, f ) ) )

    return nint( re( fsum( [ fdiv( power( r, n ), fadd( fmul( 2, r ), 3 ) ),
                             fdiv( power( s, n ), fadd( fmul( 2, s ), 3 ) ),
                             fdiv( power( t, n ), fadd( fmul( 2, t ), 3 ) ) ] ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthPadovanNumberOperator( n ):
    return getNthPadovanNumber( n )


#******************************************************************************
#
#  RPNContinuedFraction
#
#  adapted from ActiveState Python, recipe 578647
#
#******************************************************************************

class RPNContinuedFraction( list ):
    '''This class represents a continued fraction as a list of integer terms.'''
    def __init__( self, value, maxterms=15, cutoff=1e-10 ):
        if mp.dps < maxterms:
            mp.dps = maxterms

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
            self.extend( value )
        else:
            raise ValueError( 'RPNContinuedFraction requires a number or a list' )

    def getFraction( self, terms = None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for term in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( term ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


#******************************************************************************
#
#  convertFromContinuedFractionOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def convertFromContinuedFractionOperator( n ):
    if ( len( n ) == 1 ) and ( n[ 0 ] <= 0 ):
        raise ValueError( 'invalid input for evaluating a continued fraction' )

    fraction = RPNContinuedFraction( n ).getFraction( )

    return fdiv( fraction.numerator, fraction.denominator )


#******************************************************************************
#
#  makeContinuedFractionOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( ), IntValidator( 1 ) ] )
def makeContinuedFractionOperator( n, k ):
    return RPNContinuedFraction( n, maxterms = k, cutoff = power( 10, -( mp.dps / 2 ) ) )


#******************************************************************************
#
#  interpretAsFraction
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( ), IntValidator( 1 ) ] )
def interpretAsFractionOperator( n, k ):
    k = int( k )

    if mp.dps < k:
        mp.dps = k

    cutoff = fmul( n, power( 10, -( mp.dps / 2 ) ) )
    fraction = RPNContinuedFraction( value=n, maxterms=k, cutoff=cutoff ).getFraction( )

    return [ fraction.numerator, fraction.denominator ]


#******************************************************************************
#
#  interpretAsBase
#
#  This is a list operator so if the integer argument (base) is also a list,
#  we need to handle that explicitly here.
#
#******************************************************************************

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
        if i >= base:
            raise ValueError( 'invalid value for base', int( base ) )

        value = fadd( value, fmul( i, multiplier ) )
        multiplier = fmul( multiplier, base )

    return value


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 2 ) ] )
def interpretAsBaseOperator( args, base ):
    return interpretAsBase( args, base )


#******************************************************************************
#
#  getGreedyEgyptianFractionOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def getGreedyEgyptianFractionOperator( nominator, denominator ):
    if nominator > denominator:
        raise ValueError( "'egyptian_fractions' requires the numerator to be smaller than the denominator" )

    # Create a list to store the Egyptian fraction representation.
    result = [ ]

    rational = Fraction( int( nominator ), int( denominator ) )

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


#******************************************************************************
#
#  getLinearRecurrence
#
#  Fibonacci sequence = rpn [ 1 1 ] 1 n linear
#  Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n linear
#
#******************************************************************************

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

    if count < len( seeds ):
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


@argValidator( [ ListValidator( ), ListValidator( ), IntValidator( 1 ) ] )
def getLinearRecurrenceOperator( recurrence, seeds, count ):
    return RPNGenerator( getLinearRecurrence( recurrence, seeds, count ) )


#******************************************************************************
#
#  getNthLinearRecurrence
#
#******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    #return list( getLinearRecurrence( recurrence, seeds, n ) )[ -1 ]
    n = int( n )

    if not isinstance( recurrence, ( list, RPNGenerator ) ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, ( list, RPNGenerator ) ):
        seeds = [ seeds ]

    if not seeds:
        raise ValueError( 'for operator \'linear_recurrence\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( list( getLinearRecurrence( recurrence[ : i ], seeds, 1 ) ) )

    if n < len( seeds ):
        return seeds[ n ]

    if not recurrence:
        raise ValueError( 'internal error:  for operator \'nth_linear_recurrence\', '
                          'recurrence list cannot be empty ' )

    result = [ ]
    result.extend( seeds )

    for i in arange( len( seeds ), n + 1 ):
        newValue = 0

        for j in range( -1, -( len( seeds ) + 1 ), -1 ):
            newValue = fadd( newValue, fmul( result[ j ], recurrence[ j ] ) )

        result.append( newValue )

        del result[ 0 ]

    return result[ -1 ]


@argValidator( [ ListValidator( ), ListValidator( ), IntValidator( 1 ) ] )
def getNthLinearRecurrenceOperator( recurrence, seeds, n ):
    return getNthLinearRecurrence( recurrence, seeds, n )


#******************************************************************************
#
#  getLinearRecurrenceWithModulo
#
#******************************************************************************

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

    if count < len( seeds ):
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


@argValidator( [ ListValidator( ), ListValidator( ), IntValidator( 1 ), IntValidator( 2 ) ] )
def getLinearRecurrenceWithModuloOperator( recurrence, seeds, count, modulo ):
    return RPNGenerator( getLinearRecurrenceWithModulo( recurrence, seeds, count, modulo ) )


#******************************************************************************
#
#  getNthLinearRecurrenceWithModulo
#
#******************************************************************************

def getNthLinearRecurrenceWithModulo( recurrence, seeds, n, modulo ):
    if not isinstance( recurrence, ( list, RPNGenerator ) ):
        recurrence = [ recurrence ]

    if not isinstance( seeds, ( list, RPNGenerator ) ):
        seeds = [ seeds ]

    if not seeds:
        raise ValueError( 'for operator \'linear_recurrence_with_modulo\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getLinearRecurrenceWithModulo( recurrence[ : i ], seeds, i, modulo ) )

    if n < len( seeds ):
        return seeds[ int( n ) ]
    else:
        if not recurrence:
            raise ValueError( 'internal error:  for operator \'nth_linear_recurrence_with_modulo\', '
                              'recurrence list cannot be empty ' )

        result = [ ]
        result.extend( seeds )

        for i in arange( len( seeds ), n + 1 ):
            newValue = 0

            for j in range( -1, -( len( seeds ) + 1 ), -1 ):
                newValue = fmod( fadd( newValue, fmul( result[ j ], recurrence[ j ] ) ), modulo )

            result.append( newValue )

            del result[ 0 ]

    return result[ -1 ]


@argValidator( [ ListValidator( ), ListValidator( ), IntValidator( 1 ), IntValidator( 2 ) ] )
def getNthLinearRecurrenceWithModuloOperator( recurrence, seeds, n, modulo ):
    return getNthLinearRecurrenceWithModulo( recurrence, seeds, n, modulo )


#******************************************************************************
#
#  getGeometricRecurrence
#
#******************************************************************************

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

    if count < len( seeds ):
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


@argValidator( [ ListValidator( ), ListValidator( ), ListValidator( ), IntValidator( 2 ) ] )
def getGeometricRecurrenceOperator( recurrence, powers, seeds, count ):
    return RPNGenerator( getGeometricRecurrence( recurrence, powers, seeds, count ) )


#******************************************************************************
#
#  makePythagoreanTriple
#
#  Euclid's formula
#
#  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Pythag/pythag.html#mnformula
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def makePythagoreanTripleOperator( n, k ):
    if n == k:
        raise ValueError( "'make_pyth_3' requires unequal arguments" )

    result = [ ]

    result.append( fprod( [ 2, n, k ] ) )
    result.append( fabs( fsub( fmul( n, n ), fmul( k, k ) ) ) )
    result.append( fadd( fmul( n, n ), fmul( k, k ) ) )

    return sorted( result )


#******************************************************************************
#
#  generatePythagoreanTriples
#
#  https://stackoverflow.com/questions/575117/generating-unique-ordered-pythagorean-triplets
#
#******************************************************************************

def generatePythagoreanTriplesOld( n ):
    # pylint: disable=invalid-name
    for x in arange( 1, n + 1 ):
        y = x + 1
        z = y + 1

        while z <= n:
            while z * z < x * x + y * y:
                z += 1

            if z * z == x * x + y * y and z <= n:
                yield [ x, y, z ]

            y += 1


def generatePythagoreanTriples( limit ):
    # pylint: disable=invalid-name
    u = np.mat( ' 1  2  2; -2 -1 -2; 2 2 3' )
    a = np.mat( ' 1  2  2;  2  1  2; 2 2 3' )
    d = np.mat( '-1 -2 -2;  2  1  2; 2 2 3' )

    uad = np.array( [ u, a, d ] )

    m = np.array( [ 3, 4, 5 ] )

    while m.size:
        m = m.reshape( -1, 3 )

        if limit:
            m = m[ m[ :, 2 ] <= limit ]

        for i in range( m.size // 3 ):
            if m[ i ][ 1 ] > m[ i ][ 0 ]:
                yield [ m[ i ][ 0 ], m[ i ][ 1 ], m[ i ][ 2 ] ]
            else:
                yield [ m[ i ][ 1 ], m[ i ][ 0 ], m[ i ][ 2 ] ]

        m = np.dot( m, uad )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def makePythagoreanTriplesOperator( n ):
    return RPNGenerator.createGenerator( generatePythagoreanTriples, n )


#******************************************************************************
#
#  makePythagoreanQuadruple
#
#  From https://en.wikipedia.org/wiki/Pythagorean_quadruple:
#
#  All Pythagorean quadruples (including non-primitives, and with repetition,
#  though a, b and c do not appear in all possible orders) can be generated
#  from two positive integers a and b as follows:
#
#  If a and b have different parity, let p be any factor of a^2 + b^2 such that
#  p^2 < a^2 + b^2.  Then c = (a^2 + b^2 - p^2)/(2p) and d =
#  (a^2 + b^2 + p^2)/(2p).  Note that p = {d - c}.
#
#  A similar method exists for a, b both even, with the further restriction
#  that 2p must be an even factor of a^2 + b^2. No such method exists if both
#  a and b are odd.
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def makePythagoreanQuadrupleOperator( a, b ):
    # pylint: disable=invalid-name
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
        if fmod( sumsqr, 2 ) == 1:
            raise ValueError( "'make_pyth_4' oops, can't make one!" )

        div = [ i for i in div[ : ( len( div ) - 1 ) // 2 ]
                if fmod( sumsqr, fmul( i, 2 ) ) == 0 and fmod( i, 2 ) == 0 ]
        p = random.choice( div )

    psqr = fmul( p, p )
    result.append( fdiv( fsub( sumsqr, psqr ), fmul( p, 2 ) ) )
    result.append( fdiv( fadd( sumsqr, psqr ), fmul( p, 2 ) ) )

    return sorted( result )


#******************************************************************************
#
#  makeEulerBrick
#
#  http://mathworld.wolfram.com/EulerBrick.html
#
#  Saunderson's solution lets (a',b',c') be a Pythagorean triple, then
#  ( a, b, c ) = ( a'( 4b'^2 - c'^2 ), ( b'( 4a'^2 ) - c'^2 ), 4a'b'c' )
#
#******************************************************************************

@argValidator( [ IntValidator( 1 ), IntValidator( 1 ), IntValidator( 1 ) ] )
def makeEulerBrickOperator( _a, _b, _c ):
    # pylint: disable=invalid-name
    a, b, c = sorted( [ _a, _b, _c ] )

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


#******************************************************************************
#
#  getNthFibonorial
#
#******************************************************************************

def getNthFibonorial( n ):
    result = 1

    for i in arange( 2, n ):
        result = fmul( result, fib( i ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthFibonorialOperator( n ):
    return getNthFibonorial( n )


#******************************************************************************
#
#  getExtendedGCD
#
#  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( ), IntValidator( ) ] )
def getExtendedGCD( a, b ):
    # pylint: disable=invalid-name
    '''
    Euclid's Extended GCD Algorithm

    > xgcd(314159265, 271828186)
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


#******************************************************************************
#
#  getLCMOperator
#
#******************************************************************************

def getLCMOfList( args ):
    if isinstance( args[ 0 ], ( list, RPNGenerator ) ):
        return [ getLCMOfList( arg ) for arg in args ]

    result = 1

    for arg in args:
        result = fdiv( fmul( result, arg ), getGCD( result, arg ) )

    return result


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getLCMOperator( n, k ):
    return getLCMOfList( [ n, k ] )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def getLCMOfListOperator( n ):
    return getLCMOfList( n )


#******************************************************************************
#
#  getFrobeniusNumber
#
#  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500,
#  (c) copyright 2010-2016, Brian Gladman
#
#  That address is dead, but I found the same page in another location:
#
#  http://brg.a2hosted.com/?page_id=1500
#
#  Since this is classified as a list operator, it has to behave like the
#  other operators in rpnList.py.
#
#******************************************************************************

def getFrobeniusNumber( args ):
    # pylint: disable=invalid-name
    '''
    http://ccgi.gladman.plus.com/wp/?page_id=1500

    For the integer sequence (a[0], a[1], ...) with a[0] < a[1] < ... < a[n],
    return the largest number, N, that cannot be expressed in the form:
    N = sum(m[i] * x[i]) where all m[i] are non-negative integers.

    > frobenius_number( [ 9949, 9967, 9973 ] )
    24812836

    > frobenius_number( [ 6, 9, 20 ] )
    43

    > frobenius_number( [ 5, 8, 15 ] )
    27

    > frobenius_number( [ 5, 8, 9, 12 ] )
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
                raise ValueError( 'the \'frobenius\' operator is only valid for lists '
                                  'of values that have a greatest common denominator of 1' )

            for i in sorted( args ):
                a.append( int( i ) )

            def getResidueTable( a ):
                n = [ 0 ] + [ None ] * ( a[ 0 ] - 1 )

                for i in range( 1, len( a ) ):
                    d = int( getGCD( a[ 0 ], a[ i ] ) )
                    for r in range( d ):
                        try:
                            nn = min( n[ q ] for q in range( r, a[ 0 ], d ) if n[ q ] is not None )
                        except ValueError:
                            continue

                        if nn is not None:
                            for _ in range( a[ 0 ] // d ):
                                nn += a[ i ]
                                p = nn % a[ 0 ]
                                nn = min( nn, n[ p ] ) if n[ p ] is not None else nn
                                n[ p ] = nn
                return [ i for i in n if i is not None ]

            return max( getResidueTable( sorted( a ) ) ) - min( a )
    else:
        return 1 if args > 1 else -1


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def getFrobeniusNumberOperator( n ):
    return getFrobeniusNumber( n )


#******************************************************************************
#
#  solveFrobenius
#
#******************************************************************************

def solveFrobenius( n, k, translate, prefix=None ):
    #print( )
    #print( 'n', n )
    #print( 'k', k )
    #print( 'prefix', prefix )

    if prefix is None:
        prefix = [ ]

    size = len( n ) + len( prefix )

    if len( n ) == 1:
        if isDivisible( k, n[ 0 ] ):
            result = prefix + [ fdiv( k, n[ 0 ] ) ]
            yield [ result[ int( translate[ i ] ) ] for i in range( len( result ) ) ]

        return

    count = ceil( fdiv( k, n[ 0 ] ) ) + 1
    #print( 'count', count )

    result = [ ]

    for i in arange( count ):
        remainder = fsub( k, fmul( n[ 0 ], i ) )

        if remainder == 0:
            result = prefix + [ i ]
            result.extend( [ 0 ] * ( size - len( result ) ) )
            yield [ result[ int( translate[ i ] ) ] for i in range( len( result ) ) ]
            return

        yield from solveFrobenius( n[ 1 : ], remainder, translate, prefix + [ i ] )


@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 0 ) ] )
def solveFrobeniusOperator( n, k ):
    if len( n ) > 1 and getGCDOfList( n ) > 1:
        raise ValueError( 'the \'solve_frobenius\' operator is only valid for lists '
                          'of values that have a greatest common denominator of 1' )

    sortedArgs = sorted( n, reverse=True )

    old = 0

    indices = { }

    for i, item in enumerate( n ):
        indices[ item ] = i

    translate = [ ]

    for arg in sortedArgs:
        if arg == old:
            raise ValueError( "'solve_frobenius' requires a list of unique values for operand n" )

        old = arg

        translate.append( indices[ arg ] )

    return RPNGenerator.createGenerator( solveFrobenius, [ sortedArgs, k, translate ] )


#******************************************************************************
#
#  _crt
#
#  Helper function for calculateChineseRemainderTheorem
#
#******************************************************************************

def _crt( a, b, m, n ):
    # pylint: disable=invalid-name
    d = getGCD( m, n )

    if fmod( fsub( a, b ), d ) != 0:
        return None

    x = floor( fdiv( m, d ) )
    y = floor( fdiv( n, d ) )
    z = floor( fdiv( fmul( m, n ), d ) )
    p, q, _ = getExtendedGCD( x, y )

    return fmod( fadd( fprod( [ b, p, x ] ), fprod( [ a, q, y ] ) ), z )


#******************************************************************************
#
#  calculateChineseRemainderTheorem
#
#  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
#
#  Since this is classified as a list operator, it has to behave like the
#  other operators in rpnList.py.
#
#******************************************************************************

def calculateChineseRemainderTheorem( values, mods ):
    # pylint: disable=invalid-name
    '''
    The Chinese Remainder Theorem (CRT)

    Solve the equations x = a[i] mod m[i] for x

    > crt((2, 3, 5, 7), (97, 101, 103, 107))
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
            return 0

        mm = getLCMOfList( [ mods[ i ], mm ] )

    return x


@argValidator( [ ListValidator( ), ListValidator( ) ] )
def calculateChineseRemainderTheoremOperator( values, mods ):
    return calculateChineseRemainderTheorem( values, mods )


#******************************************************************************
#
#  getRadicalOperator
#
#******************************************************************************

def getRadical( target ):
    '''
    Returns the value of the radical function for n, which is the largest
    squarefree divisor.
    '''
    n = floor( target )

    if n == 0:
        return 0
    elif n == 1:
        return 1

    factors = set( getFactors( n ) )

    result = 1

    for i in factors:
        result = fmul( result, i )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getRadicalOperator( n ):
    return getRadical( n )


#******************************************************************************
#
#  getSigma
#
#******************************************************************************

#@cachedFunction( 'sigma' )     # This resulted in some really weird bugs in the 'aliquot' operator, and having the
#                               # factors already cached means it really isn't necessary.
def getSigma( target ):
    '''
    Returns the sum of the divisors of n, including 1 and n.

    http://math.stackexchange.com/questions/22721/is-there-a-formula-to-calculate-the-sum-of-all-proper-divisors-of-a-number
    '''
    n = floor( target )

    if n == 0:
        return 0
    elif n == 1:
        return 1

    factorList = getFactorList( n )

    setAccuracyForN( n )

    result = 1

    for factor in factorList:
        numerator = fsub( power( factor[ 0 ], fadd( factor[ 1 ], 1 ) ), 1 )
        denominator = fsub( factor[ 0 ], 1 )
        #debugPrint( 'sigma', numerator, denominator )
        result = fmul( result, fdiv( numerator, denominator ) )

        if result != floor( result ):
            raise ValueError( 'insufficient precision for \'sigma\', increase precision using -p or -a' )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getSigmaOperator( n ):
    return getSigma( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getAbundanceRatioOperator( n ):
    return fdiv( getSigma( n ), n )


#******************************************************************************
#
#  getSigmaK
#
#******************************************************************************

def getSigmaK( n, k ):
    '''
    Returns the sum of the divisors of n, including 1 and n, to the k power.

    https://oeis.org/A001157
    '''
    if n == 0:
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
            raise ValueError( 'insufficient precision for \'sigma_k\', increase precision using -p or -a' )

    return result


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def getSigmaKOperator( n, k ):
    return getSigmaK( n, k )


#******************************************************************************
#
#  getAliquotSequenceGenerator
#
#******************************************************************************

def getAliquotSequenceGenerator( n, k ):
    '''
    The aliquot sum of n is the sum of the divisors of n, not counting n itself
    as a divisor.  Subsequent aliquot sums can then be computed.  These sequences
    usually terminate, but some, like 276, get so large it has not been determined
    if they ever terminate.
    '''
    yield n

    a = n

    results = [ a ]

    for _ in arange( 0, k - 1 ):
        b = fsub( getSigma( a ), a )
        yield b

        if b in results:
            break

        a = b

        results.append( a )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def getAliquotSequenceOperator( n, k ):
    return RPNGenerator.createGenerator( getAliquotSequenceGenerator, [ n, k ] )


#******************************************************************************
#
#  getLimitedAliquotSequenceGenerator
#
#******************************************************************************

def getLimitedAliquotSequenceGenerator( n, k ):
    '''
    This generates aliquots until the usual termination conditions of
    getAliquotSequence, or the number exceeds k decimal digits in size.
    '''
    yield n

    a = n

    results = [ a ]

    while log10( a ) <= k and a != 0:
        b = fsub( getSigma( a ), a )
        yield b

        if b in results:
            break

        a = b

        results.append( a )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def getLimitedAliquotSequenceOperator( n, k ):
    return RPNGenerator.createGenerator( getLimitedAliquotSequenceGenerator, [ n, k ] )


#******************************************************************************
#
#  getNthMobiusNumber
#
#******************************************************************************

@cachedFunction( 'mobius' )
def getNthMobiusNumber( n ):
    if n == 1:
        return 1

    factorList = getFactorList( n )

    for i in factorList:
        if i[ 1 ] > 1:
            return 0

    if len( factorList ) % 2:
        return -1
    else:
        return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getNthMobiusNumberOperator( n ):
    return getNthMobiusNumber( n )


#******************************************************************************
#
#  getNthMertenOperator
#
#  This recursive version is much, much faster when the cache is being used.
#
#******************************************************************************

@cachedFunction( 'merten' )
def getNthMerten( n ):
    if n == 1:
        return 1

    result = 0

    for i in arange( 1, n + 1 ):
        result = fadd( result, getNthMobiusNumber( i ) )

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getNthMertenOperator( n ):
    return getNthMerten( n )


#******************************************************************************
#
#  getEulerPhiOperator
#
#******************************************************************************

@cachedFunction( 'euler_phi' )
def getEulerPhi( n ):
    if n < 2:
        return n

    return reduce( fmul, ( fmul( fsub( i[ 0 ], 1 ),
                                 power( i[ 0 ], fsub( i[ 1 ], 1 ) ) ) for i in getFactorList( n ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getEulerPhiOperator( n ):
    return getEulerPhi( n )


#******************************************************************************
#
#  getAbundanceOperator
#
#******************************************************************************

@cachedFunction( 'abundance' )
def getAbundance( n ):
    if n < 2:
        return 0

    return fsub( getSigma( n ), fmul( n, 2 ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getAbundanceOperator( n ):
    return getAbundance( n )


#******************************************************************************
#
#  isAbundantOperator
#
#******************************************************************************

def isAbundant( n ):
    if n < 2:
        return 0

    return 1 if getAbundance( n ) > 0 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isAbundantOperator( n ):
    return isAbundant( n )


#******************************************************************************
#
#  isAchillesNumber
#
#******************************************************************************

@cachedFunction( 'achilles' )
def isAchillesNumber( n ):
    factorList = getFactorList( n )

    if min( [ i[ 1 ] for i in factorList ] ) < 2:
        return 0

    return 1 if getGCDOfList( [ i[ 1 ] for i in factorList ] ) == 1 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def isAchillesNumberOperator( n ):
    return isAchillesNumber( n )


#******************************************************************************
#
#  isDeficientOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isDeficient( n ):
    if n < 1:
        return 0
    elif n == 1:
        return 1

    return 1 if getAbundance( n ) < 0 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isDeficientOperator( n ):
    return isDeficient( n )


#******************************************************************************
#
#  isKPolydivisible
#
#******************************************************************************

@cachedFunction( 'k_polydivisible' )
def isKPolydivisible( n, k ):
    testMe = n

    digits = fadd( floor( fdiv( log( n ), log( k ) ) ), 1 )

    while testMe > 0:
        if not isDivisible( testMe, digits ):
            return 0

        testMe = floor( fdiv( testMe, k ) )
        digits -= 1

    return 1


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 2 ) ] )
def isKPolydivisibleOperator( n, k ):
    return isKPolydivisible( n, k )


#******************************************************************************
#
#  isKSemiprime
#
#******************************************************************************

@cachedFunction( 'k_semiprime' )
def isKSemiprime( n, k ):
    return 1 if sum( [ i[ 1 ] for i in getFactorList( n ) ] ) == k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def isKSemiprimeOperator( n, k ):
    return isKSemiprime( n, k )


def isSemiprime( n ):
    return isKSemiprime( n, 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isSemiprimeOperator( n ):
    return isSemiprime( n )


#******************************************************************************
#
#  isKSphenic
#
#******************************************************************************

@cachedFunction( 'k_sphenic' )
def isKSphenic( n, k ):
    factorList = getFactorList( n )

    if len( factorList ) != k:
        return 0

    for i in getFactorList( n ):
        if i[ 1 ] > 1:
            return 0

    return 1


def isSphenic( n ):
    return isKSphenic( n, 3 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isSphenicOperator( n ):
    return isSphenic( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def isKSphenicOperator( n, k ):
    return isKSphenic( n, k )


#******************************************************************************
#
#  isPerfect
#
#******************************************************************************

def isPerfect( n ):
    if n < 2:
        return 0

    return 1 if getAbundance( n ) == 0 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPerfectOperator( n ):
    return isPerfect( n )


#******************************************************************************
#
#  isPerniciousOperator
#
#******************************************************************************

def isPernicious( n ):
    if n < 1:
        return 0

    return 1 if isPrime( getBitCount( n ) ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPerniciousOperator( n ):
    return isPernicious( n )


#******************************************************************************
#
#  isPoliteOperator
#
#******************************************************************************

def isPolite( n ):
    if n < 1:
        return 0

    divisors = getDivisors( n )

    for divisor in divisors:
        if isOdd( divisor ):
            return 1

    return 0


#******************************************************************************
#
#  getPolitenessOperator
#
#******************************************************************************

def getPoliteness( n ):
    if n < 1:
        return 0

    divisors = getDivisors( n )

    result = 0

    for divisor in divisors:
        if isOdd( divisor ):
            result += 1

    return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getPolitenessOperator( n ):
    return getPoliteness( n )


#******************************************************************************
#
#  isPolydivisible
#
#  It seems to be about 10% faster on average to do the division tests in
#  reverse order.
#
#******************************************************************************

@cachedFunction( 'polydivisible' )
def isPolydivisible( n ):
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


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPolydivisibleOperator( n ):
    return isPolydivisible( n )


#******************************************************************************
#
#  isRough
#
#  https://en.wikipedia.org/wiki/Rough_number
#
#  Please note that rough is not the opposite of smooth.
#
#******************************************************************************

@cachedFunction( 'rough' )
def isRough( n, k ):
    return 1 if min( [ i[ 0 ] for i in getFactorList( n ) ] ) >= k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ),
                 IntValidator( 2, None, specials=[ ( isPrime, 'argument must be a prime number' ) ] ) ] )
def isRoughOperator( n, k ):
    if k < 2:
        return 1

    if n < 1:
        return 0

    if n == 1:
        return 1

    if n < k:
        return 0

    if n == k:
        return 1

    return isRough( n, k )


#******************************************************************************
#
#  isSmooth
#
#******************************************************************************

@cachedFunction( 'smooth' )
def isSmooth( n, k ):
    return 1 if sorted( getFactorList( n ) )[ -1 ][ 0 ] <= k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ),
                 IntValidator( 2, None, specials=[ ( isPrime, 'argument must be a prime number' ) ] ) ] )
def isSmoothOperator( n, k ):
    if n <= k:
        return 1

    return isSmooth( n, k )


#******************************************************************************
#
#  isSquareFree
#
#******************************************************************************

@cachedFunction( 'squarefree' )
def isSquareFree( n ):
    if n == 0:
        return 0

    for i in getFactorList( n ):
        if i[ 1 ] > 1:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isSquareFreeOperator( n ):
    return isSquareFree( n )


#******************************************************************************
#
#  isPowerful
#
#******************************************************************************

@cachedFunction( 'powerful' )
def isPowerful( n ):
    if n == 1:
        return 1

    for i in getFactorList( n ):
        if i[ 1 ] == 1:
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def isPowerfulOperator( n ):
    return isPowerful( n )


#******************************************************************************
#
#  isPronic
#
#******************************************************************************

def isPronic( n ):
    a = floor( sqrt( n ) )
    return 1 if n == fmul( a, fadd( a, 1 ) ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isPronicOperator( n ):
    return isPronic( n )


#******************************************************************************
#
#  isUnusual
#
#  https://en.wikipedia.org/wiki/Unusual_number
#
#******************************************************************************

@cachedFunction( 'unusual' )
def isUnusual( n ):
    if n < 2:
        return 0

    return 1 if max( [ i[ 0 ] for i in getFactorList( n ) ] ) > sqrt( n ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isUnusualOperator( n ):
    return isUnusual( n )


#******************************************************************************
#
#  splitNumber
#
#******************************************************************************

def splitNumber( value, base ):
    result = [ ]

    while value:
        digit = fmod( value, base )
        result.append( digit )
        value = fdiv( fsub( value, digit ), base )

    return result


#******************************************************************************
#
#  joinNumber
#
#******************************************************************************

def joinNumber( digits, base ):
    place = 1
    result = 0

    for digit in digits:
        result = fadd( result, fmul( digit, place ) )
        place = fmul( place, base )

    return result


#******************************************************************************
#
#  generatePolydivisiblesGenerator
#
#******************************************************************************

def generatePolydivisiblesGenerator( _base ):
    base = int( _base )
    newItems = list( range( 1, base ) )

    yield 0

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
@argValidator( [ IntValidator( 2 ) ] )
def generatePolydivisiblesOperator( n ):
    return RPNGenerator.createGenerator( generatePolydivisiblesGenerator, n )


#******************************************************************************
#
#  getNthSternNumber
#
#******************************************************************************

@cachedFunction( 'stern' )
def getNthSternNumber( n ):
    '''Returns the nth number of Stern's diatomic series recursively.'''
    if n in [ 0, 1 ]:
        return n
    elif n % 2 == 0:  # even
        return getNthSternNumber( floor( fdiv( n, 2 ) ) )
    else:
        return fadd( getNthSternNumber( floor( fdiv( fsub( n, 1 ), 2 ) ) ),
                     getNthSternNumber( floor( fdiv( fadd( n, 1 ), 2 ) ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthSternNumberOperator( n ):
    return getNthSternNumber( n )


#******************************************************************************
#
#  getNthCalkinWilf
#
#******************************************************************************

def getNthCalkinWilf( n ):
    if n == 0:
        return [ 0, 1 ]

    return [ getNthSternNumber( n ), getNthSternNumber( fadd( n, 1 ) ) ]


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthCalkinWilfOperator( n ):
    return getNthCalkinWilf( n )


#******************************************************************************
#
#  isSociableListOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def isSociableListOperator( n ):
    if len( n ) < 2:
        raise ValueError( '\'is_sociable_list\' requires a list with more than one element' )

    first = True

    abundance = 0

    for i in n:
        if first:
            abundance = fdiv( getSigma( i ), i )
            first = False
        elif fdiv( getSigma( i ), i ) != abundance:
            return 0

    return 1


#******************************************************************************
#
#  isKHyperperfect
#
#******************************************************************************

@cachedFunction( 'k_hyperperfect' )
def isKHyperperfect( n, k ):
    setAccuracyForN( n )
    return 1 if fadd( fmul( k, fsub( getSigma( n ), fadd( n, 1 ) ) ), 1 ) == n else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def isKHyperperfectOperator( n, k ):
    return isKHyperperfect( n, k )


#******************************************************************************
#
#  isKPerfect
#
#******************************************************************************

@cachedFunction( 'k_perfect' )
def isKPerfect( n, k ):
    setAccuracyForN( n )
    return 1 if fdiv( getSigma( n ), n ) == k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def isKPerfectOperator( n, k ):
    return isKPerfect( n, k )


#******************************************************************************
#
#  getNthZetaZero
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getNthZetaZeroOperator( n ):
    return zetazero( int( n ) )


#******************************************************************************
#
#  getNthMersennePrime
#
#******************************************************************************

MERSENNE_PRIME_EXPONENTS = {
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
    50:  77232917,
    51:  82589933
}


def getNthMersenneExponent( n ):
    if n == 0:
        return 1

    return MERSENNE_PRIME_EXPONENTS[ n ]


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0, len( MERSENNE_PRIME_EXPONENTS ) ) ] )
def getNthMersenneExponentOperator( n ):
    return getNthMersenneExponent( n )


def getNthMersennePrime( n ):
    if n == 0:
        return 1

    return fsub( power( 2, getNthMersenneExponent( n ) ), 1 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0, len( MERSENNE_PRIME_EXPONENTS ) ) ] )
def getNthMersennePrimeOperator( n ):
    return getNthMersennePrime( n )


def getNthPerfectNumber( n ):
    exponent = getNthMersenneExponent( n )
    return fmul( fsub( power( 2, exponent ), 1 ), power( 2, fsub( exponent, 1 ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0, len( MERSENNE_PRIME_EXPONENTS ) ) ] )
def getNthPerfectNumberOperator( n ):
    return getNthPerfectNumber( n )


#******************************************************************************
#
#  getNthThueMorseNumber
#
#  https://en.wikipedia.org/wiki/Thue%E2%80%93Morse_sequence
#
#******************************************************************************

@cachedFunction( 'thue_morse' )
def getNthThueMorseNumber( n ):
    if n == 0:
        return 0
    else:
        return fmod( fadd( n, getNthThueMorseNumber( floor( fdiv( n, 2 ) ) ) ), 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthThueMorseNumberOperator( n ):
    return getNthThueMorseNumber( n )


#******************************************************************************
#
#  findSumsOfKPowersGenerator
#
#******************************************************************************

def findSumsOfKPowersGenerator( n, k, p, bNonZero=False, prefix=None ):
    if prefix is None:
        prefix = [ ]

    # If we are looking for only one power, then we only have one choice
    if k == 1:
        if n == 0:
            if not bNonZero and not prefix:
                yield [ 0 ]
        else:
            value = root( n, p )

            if isInteger( value ):
                yield prefix + [ value ]

        return

    if n == 0:
        yield prefix + [ 0 ] * int( k )

    start = prefix[ -1 ] if prefix else 1 if bNonZero else 0
    limit = ceil( root( n, p ) )

    for i in arange( start, limit ):
        remainder = fsub( n, power( i, p ) )

        if remainder >= fdiv( n, 2 ):
            yield from findSumsOfKPowersGenerator( fsub( n, power( i, p ) ),
                                                   fsub( k, 1 ), p, bNonZero, prefix + [ i ] )


@cachedFunction( 'sums_of_k_powers' )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ), IntValidator( 1 ) ] )
def findSumsOfKPowersOperator( n, k, p ):
    return RPNGenerator( findSumsOfKPowersGenerator( n, k, p ) )


@cachedFunction( 'sums_of_k_nonzero_powers' )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ), IntValidator( 1 ) ] )
def findSumsOfKNonzeroPowersOperator( n, k, p ):
    return RPNGenerator( findSumsOfKPowersGenerator( n, k, p, bNonZero = True ) )


#******************************************************************************
#
#  some one-line operators
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getBarnesGOperator( n ):
    return barnesg( n )


@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), ComplexValidator( ) ] )
def getBetaOperator( n, k ):
    return beta( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getDigammaOperator( n ):
    return psi( 0, n )


def getNthDoubleFactorial( n ):
    return fac2( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getNthDoubleFactorialOperator( n ):
    return fac2( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getAltZetaOperator( n ):
    return altzeta( n )


def getNthFactorial( n ):
    return fac( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getNthFactorialOperator( n ):
    return fac( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getGammaOperator( n ):
    return gamma( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthHarmonicNumberOperator( n ):
    return harmonic( n )


def getNthHyperfactorial( n ):
    return hyperfac( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getNthHyperfactorialOperator( n ):
    return hyperfac( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getLeylandNumberOperator( n, k ):
    return fadd( power( n, k ), power( k, n ) )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getLogGammaOperator( n ):
    return loggamma( n )


def getNthCarolNumber( n ):
    return fsub( power( fsub( power( 2, n ), 1 ), 2 ), 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthCarolNumberOperator( n ):
    return getNthCarolNumber( n )


def getNthKyneaNumber( n ):
    return fsub( power( fadd( power( 2, n ), 1 ), 2 ), 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthKyneaNumberOperator( n ):
    return getNthKyneaNumber( n )


def getNthLeonardoNumber( n ):
    return fsub( fmul( 2, fib( fadd( n, 1 ) ) ), 1 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthLeonardoNumberOperator( n ):
    return getNthLeonardoNumber( n )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), ComplexValidator( ) ] )
def getPolygammaOperator( n, k ):
    return psi( n, k )


def getNthSubfactorial( n ):
    return floor( fadd( fdiv( fac( n ), e ), fdiv( 1, 2 ) ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthSubfactorialOperator( n ):
    return getNthSubfactorial( n )


def getNthSuperfactorial( n ):
    return superfac( n )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getNthSuperfactorialOperator( n ):
    return getNthSuperfactorial( n )


def getNthThabitNumber( n ):
    return fsub( fmul( 3, power( 2, n ) ), 1 )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthThabitNumberOperator( n ):
    return getNthThabitNumber( n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthThabit2NumberOperator( n ):
    return fadd( fmul( 3, power( 2, n ) ), 1 )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getNthKThabitNumberOperator( n, k ):
    return fsub( fmul( fadd( k, 1 ), power( k, n ) ), 1 )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def getNthKThabit2NumberOperator( n, k ):
    return fadd( fmul( fadd( k, 1 ), power( k, n ) ), 1 )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getTrigammaOperator( n ):
    return psi( 1, n )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getUnitRootsOperator( n ):
    return unitroots( int( n ) )


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getZetaOperator( n ):
    return zeta( n )


@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), ComplexValidator( ) ] )
def getHurwitzZetaOperator( n, k ):
    return zeta( n, k )


#******************************************************************************
#
#  getCollatzSequenceGenerator
#
#******************************************************************************

def getCollatzSequenceGenerator( n, k ):
    if n == 0:
        yield 0
        return

    a = n

    for _ in arange( 0, k - 1 ):
        if isEven( a ):
            b = fdiv( a, 2 )
        else:
            b = fadd( fmul( 3, a ), 1 )

        yield b

        if b == 1:
            return

        a = b


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 1 ) ] )
def getCollatzSequenceOperator( n, k ):
    return RPNGenerator.createGenerator( getCollatzSequenceGenerator, [ n, fadd( k, 1 ) ] )


#******************************************************************************
#
#  findNthSumOfSquaresOperator
#
#  http://www.wolframalpha.com/input/?i=(+n+(+n+%2B+1+)+(+2n+%2B+1+)+)+%2F+6+%3D+x,+solve+for+n
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def findNthSumOfSquaresOperator( n ):
    sqrt3 = sqrt( 3 )

    bigTerm = root( fadd( fmul( sqrt3, sqrt( fsub( fmul( 3888, power( n, 2 ) ), 1 ) ) ), fmul( 108, n ) ), 3 )

    return fdiv( fsub( fadd( fdiv( bigTerm, power( 3, fdiv( 2, 3 ) ) ),
                             fdiv( 1, fmul( root( 3, 3 ), bigTerm ) ) ), 1 ), 2 )


#******************************************************************************
#
#  findNthSumOfCubesOperator
#
#  http://www.wolframalpha.com/input/?i=x+%3D+1%2F4+n%5E2+(+n+%2B+1+)%5E2+for+n
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def findNthSumOfCubesOperator( n ):
    return fdiv( fsub( sqrt( fadd( fmul( 8, sqrt( n ) ), 1 ) ), 1 ), 2 )


#******************************************************************************
#
#  getDigitalRootOperator
#
#  https://en.wikipedia.org/wiki/Digital_root
#
#******************************************************************************

def getDigitalRoot( n ):
    if n == 0:
        return 0

    result = fmod( n, 9 )

    if result == 0:
        return 9
    else:
        return result


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getDigitalRootOperator( n ):
    return getDigitalRoot( n )


#******************************************************************************
#
#  isCarmichaelNumber
#
#  https://en.wikipedia.org/wiki/Carmichael_number
#
#******************************************************************************

#import pysnooper

#@cachedFunction( 'carmichael' )
#@pysnooper.snoop( )
def isCarmichaelNumber( n ):
    factorList = getFactorList( n )

    for i in factorList:
        # check to see that the number is squarefree
        if i[ 1 ] > 1:
            return 0

        if not isDivisible( n - 1, i[ 0 ] - 1 ):
            return 0

    return 1


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isCarmichaelNumberOperator( n ):
    if n < 2 or isDivisible( n, 2 ) or isPrime( n ):
        return 0

    return isCarmichaelNumber( n )


#******************************************************************************
#
#  isRuthAaronNumber
#
#  http://mathworld.wolfram.com/Ruth-AaronPair.html
#
#******************************************************************************

@cachedFunction( 'ruth_aaron' )
def isRuthAaronNumber( n ):
    return 1 if fsum( getFactors( n ) ) == fsum( getFactors( fadd( n, 1 ) ) ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isRuthAaronNumberOperator( n ):
    return isRuthAaronNumber( n )


#******************************************************************************
#
#  calculateAckermannFunctionOperator
#
#******************************************************************************

def calculateAckermannFunction( n, k ):
    '''
    https://stackoverflow.com/questions/12678099/ackermann-function-understanding

    Computes the value of the Ackermann function for the input integers m and n.
    the Ackermann function being:
    A( n, k ) = k + 1                        if n = 0
              = A ( n - 1 , 1 )              if n > 0 and k == 1
              = A ( n - 1 , A ( n , k - 1 )  if n > 0 and k > 0
    '''

    # shortcuts to help with excessive recursion
    if n == 1:
        return fadd( k, 2 )

    if n == 2:
        return fadd( fmul( 2, k ), 3 )

    if n == 3:
        return fsub( power( 2, fadd( k, 3 ) ), 3 )

    if n == 4:
        return fsub( calculatePowerTowerRight( [ 2 ] * ( int( k ) + 3 ) ), 3 )

    # Here's the real algorithm...
    if n == 0:
        #print( k + 1 )
        return fadd( k, 1 )

    if n > 0 and k == 0:
        #print( "ackermann( ", n - 1, ",", 1, " ) " )
        return calculateAckermannFunction( fsub( n, 1 ), 1 )

    if n > 0 and k > 0:
        #print( "Ackermann( ", n - 1, ",", "Ackermann( ", n, ",", k- 1, " )", " )" )
        return calculateAckermannFunction( fsub( n, 1 ), calculateAckermannFunction( n, fsub( k, 1 ) ) )

    raise ValueError( 'invalid arguments' )


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 0 ) ] )
def calculateAckermannFunctionOperator( n, k ):
    return calculateAckermannFunction( n, k )


#******************************************************************************
#
#  getHarmonicResidueOperator
#
#******************************************************************************

def getHarmonicResidue( n ):
    if n < 2:
        return 0

    return fmod( fmul( n, getDivisorCount( n ) ), getSigma( n ) )


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getHarmonicResidueOperator( n ):
    return getHarmonicResidue( n )


#******************************************************************************
#
#  isHarmonicDivisorNumberOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isHarmonicDivisorNumberOperator( n ):
    if n < 1:
        return 0

    return 1 if getHarmonicResidue( n ) == 0 else 0


#******************************************************************************
#
#  isAntiharmonicOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isAntiharmonic( n ):
    if n < 1:
        return 0

    return 1 if isDivisible( getSigmaK( n, 2 ), getSigmaK( n, 1 ) ) else 0


@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def isAntiharmonicOperator( n ):
    return isAntiharmonic( n )


#******************************************************************************
#
#  getHarmonicFractionOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getHarmonicFractionOperator( n ):
    n = int( n )

    if n == 1:
        return [ 1, 1 ]

    denominator = getLCMOfList( range( 2, n + 1 ) )

    numerator = 0

    for i in range( 1, n + 1 ):
        numerator = fadd( numerator, fdiv( denominator, i ) )

    return reduceList( [ numerator, denominator ] )


#******************************************************************************
#
#  getAlternatingHarmonicFractionOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ) ] )
def getAlternatingHarmonicFractionOperator( n ):
    n = int( n )

    if n == 1:
        return [ 1, 1 ]

    denominator = getLCMOfList( range( 2, n + 1 ) )

    numerator = 0

    for i in range( 1, n + 1 ):
        if fmod( i, 2 ):
            numerator = fadd( numerator, fdiv( denominator, i ) )
        else:
            numerator = fsub( numerator, fdiv( denominator, i ) )

    return reduceList( [ numerator, denominator ] )


#******************************************************************************
#
#  areRelativelyPrimeOperator
#
#******************************************************************************

def areRelativelyPrime( n, k ):
    return 1 if getGCD( n, k ) == 1 else 0


@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 1 ), IntValidator( 1 ) ] )
def areRelativelyPrimeOperator( n, k ):
    return areRelativelyPrime( n, k )


#******************************************************************************
#
#  getNthPhitorialOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ) ] )
def getNthPhitorialOperator( n ):
    if n < 2:
        return 1

    result = 1

    for i in arange( 1, n + 1 ):
        if areRelativelyPrime( i, n ):
            result = fmul( result, i )

    return result


#******************************************************************************
#
#  getNthKPolygorialOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ IntValidator( 0 ), IntValidator( 3 ) ] )
def getNthKPolygorialOperator( n, k ):
    return fmul( fdiv( fac( n ), power( 2, n ) ),
                 fdiv( fmul( power( fsub( k, 2 ), n ),
                             gamma( fdiv( fadd( fsub( fmul( n, k ), fmul( 2, n ) ), 2 ), fsub( k, 2 ) ) ) ),
                       gamma( fdiv( 2, fsub( k, 2 ) ) ) ) )


#******************************************************************************
#
#  getIntegerSquareRoot
#
#  https://code.activestate.com/recipes/577821-integer-square-root-function/
#
#******************************************************************************

#def getIntegerSquareRoot( x ):
#    if x < 0:
#        raise ValueError('square root not defined for negative numbers')
#
#    n = int(x)
#
#    if n == 0:
#        return 0
#
#    a, b = divmod(n.bit_length(), 2)
#    x = 2**(a+b)
#
#    while True:
#        y = (x + n//x)//2
#
#        if y >= x:
#            return x
#
#        x = y
#
#    # Frederik Johansson
#    x = 2^ceil(numbits(N)/2)
#    loop:
#        y = floor((x + floor(N/x))/2)
#        if y >= x
#            return x
#        x = y


############################################################################
# License: Freely available for use, abuse and modification
# (this is the Simplified BSD License, aka FreeBSD license)
# Copyright 2001-2012 Robert Campbell. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
############################################################################
#def carmichaellambda(n):
#        """carmichaellambda(n) - Compute Carmichael's Lambda function
#        of n - the smallest exponent e such that b**e = 1 for all b coprime to n.
#        Otherwise defined as the exponent of the group of integers mod n."""
#        thefactors = factors(n)
#        thefactors.sort()
#        thefactors += [0]  # Mark the end of the list of factors
#        carlambda = 1 # The Carmichael Lambda function of n
#        carlambda_comp = 1 # The Carmichael Lambda function of the component p**e
#        oldfact = 1
#        for fact in thefactors:
#                if fact==oldfact:
#                        carlambda_comp = (carlambda_comp*fact)
#                else:
#                        if ((oldfact == 2) and (carlambda_comp >= 4)):
#                           carlambda_comp /= 2 # Z_(2**e) is not cyclic for e>=3
#
#                        if carlambda == 1:
#                                carlambda = carlambda_comp
#                        else:
#                                carlambda = (carlambda * carlambda_comp)/gcd(carlambda,carlambda_comp)
#
#                        carlambda_comp = fact-1
#                        oldfact = fact
#        return carlambda

