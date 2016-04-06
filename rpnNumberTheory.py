#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnNumberTheory.py
# //
# //  RPN command-line calculator number theory operators
# //  copyright (c) 2016, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools
import random

from fractions import Fraction
from functools import reduce

from mpmath import arange, binomial, fabs, fac, fadd, fdiv, fib, floor, fmod, \
                   fmul, fneg, fprod, fsub, fsum, mp, mpc, mpf, mpmathify, nint, \
                   phi, polyroots, polyval, power, primepi2, re, root, sqrt

from rpnFactor import getECMFactors
from rpnGenerator import RPNGenerator
from rpnMath import isDivisible
from rpnPersistence import cachedFunction
from rpnUtils import real, real_int, getMPFIntegerAsString

import rpnGlobals as g


# //******************************************************************************
# //
# //  getNthAlternatingFactorial
# //
# //******************************************************************************

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
# //  getNthPascalLine
# //
# //******************************************************************************

def getNthPascalLine( n ):
    for i in arange( 0, real( n ) ):
        yield binomial( n - 1, i )


# //******************************************************************************
# //
# //  getDivisorCount
# //
# //******************************************************************************

def getDivisorCount( n ):
    if n == 1:
        return 1

    factors = getECMFactors( n ) if g.ecm else getFactors( n )
    return fprod( [ i[ 1 ] + 1 for i in factors ] )


# //******************************************************************************
# //
# //  createDivisorList
# //
# //******************************************************************************

def createDivisorList( seed, factors ):
    result = [ ]

    factor, count = factors[ 0 ]

    for i in range( count + 1 ):
        divisors = [ ]
        divisors.extend( seed )
        divisors.extend( [ factor ] * i )

        if len( factors ) > 1:
            result.extend( createDivisorList( divisors, factors[ 1 : ] ) )
        else:
            result.extend( [ fprod( divisors ) ] )

    return result


# //******************************************************************************
# //
# //  getDivisors
# //
# //******************************************************************************

def getDivisors( n ):
    if n == 0:
        return [ 0 ]
    elif n == 1:
        return [ 1 ]

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return sorted( createDivisorList( [ ], factors ) )


# //******************************************************************************
# //
# //  getNthLucasNumber
# //
# //******************************************************************************

def getNthLucasNumber( n ):
    if real( n ) == 0:
        return 2
    elif n == 1:
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
    return getNthLinearRecurrence( [ 2, 1 ], [ 0, 1 ], fadd( real( n ), 1 ) )


# //******************************************************************************
# //
# //  getNthBaseKRepunit
# //
# //******************************************************************************

def getNthBaseKRepunit( n, k ):
    return getNthLinearRecurrence( [ fneg( real( k ) ), fadd( k, 1 ) ], [ 1, fadd( k, 1 ) ], n )


# //******************************************************************************
# //
# //  getPrimePi
# //
# //******************************************************************************

def getPrimePi( n ):
    result = primepi2( real( n ) )

    return [ mpf( result.a ), mpf( result.b ) ]


# //******************************************************************************
# //
# //  getNthFibonacci
# //
# //******************************************************************************

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


# //******************************************************************************
# //
# //  getNthKFibonacciNumberTheSlowWay
# //
# //******************************************************************************

def getNthKFibonacciNumberTheSlowWay( n, k ):
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
    """This class represents a continued fraction as a list of integer terms."""
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

def convertFromContinuedFraction( n ):
    if not isinstance( n, list ):
        n = [ n ]

    if ( len( n ) == 1 ) and ( n[ 0 ] <= 0 ):
        raise ValueError( "invalid input for evaluating a continued fraction" )

    fraction = RPNContinuedFraction( n ).getFraction( )
    return fdiv( fraction.numerator, fraction.denominator )


# //******************************************************************************
# //
# //  interpretAsFraction
# //
# //******************************************************************************

def interpretAsFraction( i, j ):
    fraction = RPNContinuedFraction( i, maxterms = j ).getFraction( )
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


# //******************************************************************************
# //
# //  getGreedyEgyptianFraction
# //
# //******************************************************************************

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
# //  getNthLinearRecurrence
# //
# //  nth element of Fibonacci sequence = rpn [ 1 1 ] 1 n linear
# //  nth element of Lucas sequence = rpn [ 1 1 ] [ 1 3 ] n linear
# //
# //******************************************************************************

def getNthLinearRecurrence( recurrence, seeds, n ):
    if not isinstance( recurrence, list ):
        return getNthLinearRecurrence( [ recurrence ], seeds, real( n ) )

    if not isinstance( seeds, list ):
        return getNthLinearRecurrence( recurrence, [ seeds ], real( n ) )

    if not seeds:
        raise ValueError( 'for operator \'linear_recur\', seeds list cannot be empty ' )

    # calculate missing seeds
    for i in range( len( seeds ), len( recurrence ) ):
        seeds.append( getNthLinearRecurrence( recurrence[ : i ], seeds, i ) )

    if isinstance( n, list ):
        return [ getNthLinearRecurrence( recurrence, seeds, real( i ) ) for i in n ]

    if real( n ) < len( seeds ):
        return seeds[ int( n ) - 1 ]
    else:
        if not recurrence:
            raise ValueError( 'internal error:  for operator \'linear_recur\', '
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

def getNthFibonorial( n ):
    result = 1

    for i in arange( 2, real( n ) ):
        result = fmul( result, fib( i ) )

    return result


# //******************************************************************************
# //
# //  getGCD
# //
# //  This function is intended to be used with two numerical values or a
# //  single list of values.   The list can be recursive (to support the
# //  'gcd' list operator), but if b is non-zero, then a and b must be single
# //  values.
# //
# //******************************************************************************

def getGCD( a, b = 0 ):
    if real( b ) == 0:
        a = list( a )
    else:
        a, b = fabs( a ), fabs( b )

        while a:
            b, a = a, fmod( b, a )

        return b

    if isinstance( a[ 0 ], list ):
        return [ getGCD( real( arg ) ) for arg in a ]
    else:
        result = max( a )

        for pair in itertools.combinations( a, 2 ):
            gcd = getGCD( *pair )

            if gcd < result:
                result = gcd

        return result


# //******************************************************************************
# //
# //  getExtendedGCD
# //
# //  adapted from http://ccgi.gladman.plus.com/wp/?page_id=1500
# //
# //******************************************************************************

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

def getLCM( args ):
    if isinstance( args, RPNGenerator ):
        return getLCM( list( args ) )
    elif isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getLCM( arg ) for arg in args ]
        else:
            result = 1

            for arg in args:
                result = result * arg / getGCD( result, arg )

            return result
    else:
        return args


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

    >>> frobenius_number((9949, 9967, 9973))
    24812836

    >>> frobenius_number((6, 9, 20))
    43

    >>> frobenius_number((5, 8, 15))
    27

    frobenius_number((5, 8, 9, 12))
    11
    '''

    if isinstance( args, list ):
        if isinstance( args[ 0 ], list ):
            return [ getFrobeniusNumber( arg ) for arg in args ]
        else:
            a = [ ]

            if getGCD( args ) > 1:
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


# //******************************************************************************
# //
# //  getSigma
# //
# //******************************************************************************

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

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    result = 1

    for factor in factors:
        numerator = fsub( power( factor[ 0 ], fadd( factor[ 1 ], 1 ) ), 1 )
        denominator = fsub( factor[ 0 ], 1 )
        #debugPrint( 'sigma', numerator, denominator )
        result = fmul( result, fdiv( numerator, denominator ) )

        if result != floor( result ):
            raise ValueError( 'insufficient precision for \'sigma\', increase precision (-p))' )

    return result


# //******************************************************************************
# //
# //  getSigmaN
# //
# //******************************************************************************

def getSigmaN( n, k ):
    '''
    Returns the sum of the divisors of n, including 1 and n, to the k power.

    https://oeis.org/A001157
    '''
    if real( n ) == 0:
        return 0
    elif n == 1:
        return 1

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    result = 1

    for factor in factors:
        numerator = fsub( power( factor[ 0 ], fmul( fadd( factor[ 1 ], 1 ), k ) ), 1 )
        denominator = fsub( power( factor[ 0 ], k ), 1 )
        result = fmul( result, fdiv( numerator, denominator ) )

        if result != floor( result ):
            raise ValueError( 'insufficient precision for \'sigma_n\', increase precision (-p))' )

    return result


# //******************************************************************************
# //
# //  getAliquotSequence
# //
# //******************************************************************************

def getAliquotSequence( n, k ):
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


# //******************************************************************************
# //
# //  getMobius
# //
# //******************************************************************************

@cachedFunction( 'mobius' )
def getMobius( n ):
    if real( n ) == 1:
        return 1

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    for i in factors:
        if i[ 1 ] > 1:
            return 0

    if len( factors ) % 2:
        return -1
    else:
        return 1


# //******************************************************************************
# //
# //  getNthMerten
# //
# //******************************************************************************

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

@cachedFunction( 'euler_phi' )
def getEulerPhi( n ):
    if real( n ) < 2:
        return n

    if g.ecm:
        return reduce( fmul, ( fmul( fsub( i[ 0 ], 1 ), power( i[ 0 ], fsub( i[ 1 ], 1 ) ) ) for i in getECMFactors( n ) ) )
    else:
        return reduce( fmul, ( fmul( fsub( i[ 0 ], 1 ), power( i[ 0 ], fsub( i[ 1 ], 1 ) ) ) for i in getFactors( n ) ) )


# //******************************************************************************
# //
# //  getPowMod
# //
# //******************************************************************************

def getPowMod( a, b, c ):
    return pow( real_int( a ), real_int( b ), real_int( c ) )


# //******************************************************************************
# //
# //  isDeficient
# //
# //******************************************************************************

def isDeficient( n ):
    if real( n ) < 2:
        return 0

    return 1 if fsum( getDivisors( n )[ : -1 ] ) < n else 0


# //******************************************************************************
# //
# //  isAbundant
# //
# //******************************************************************************

def isAbundant( n ):
    if real( n ) < 2:
        return 0

    return 1 if fsum( getDivisors( n )[ : -1 ] ) > n else 0


# //******************************************************************************
# //
# //  isPerfect
# //
# //******************************************************************************

def isPerfect( n ):
    if n < 2:
        return 0

    return 1 if fsum( getDivisors( n )[ : -1 ] ) == n else 0


# //******************************************************************************
# //
# //  isSmooth
# //
# //******************************************************************************

def isSmooth( n, k ):
    if real( n ) < real( k ):
        return 0

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if max( [ i[ 0 ] for i in factors ] ) <= k else 0


# //******************************************************************************
# //
# //  isRough
# //
# //  https://en.wikipedia.org/wiki/Rough_number
# //
# //******************************************************************************

def isRough( n, k ):
    if real( n ) < real( k ):
        return 0

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if min( [ i[ 0 ] for i in factors ] ) >= k else 0


# //******************************************************************************
# //
# //  isKSemiPrime
# //
# //******************************************************************************

def isKSemiPrime( n, k ):
    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if sum( [ i[ 1 ] for i in factors ] ) == k else 0


# //******************************************************************************
# //
# //  isSphenic
# //
# //******************************************************************************

def isSphenic( n ):
    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    if len( factors ) != 3:
        return 0

    return 1 if max( [ i[ 1 ] for i in factors ] ) == 1 else 0


# //******************************************************************************
# //
# //  isSquareFree
# //
# //******************************************************************************

def isSquareFree( n ):
    if real_int( n ) == 0:
        return 0

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if max( [ i[ 1 ] for i in factors ] ) == 1 else 0


# //******************************************************************************
# //
# //  isPowerful
# //
# //******************************************************************************

def isPowerful( n ):
    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if min( [ i[ 1 ] for i in factors ] ) >= 2 else 0


# //******************************************************************************
# //
# //  isAchillesNumber
# //
# //******************************************************************************

def isAchillesNumber( n ):
    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    if min( [ i[ 1 ] for i in factors ] ) < 2:
        return 0

    return 1 if getGCD( [ i[ 1 ] for i in factors ] ) == 1 else 0


# //******************************************************************************
# //
# //  isUnusual
# //
# //  https://en.wikipedia.org/wiki/Unusual_number
# //
# //******************************************************************************

def isUnusual( n ):
    if real_int( n ) < 2:
        return 0

    factors = getECMFactors( n ) if g.ecm else getFactors( n )

    return 1 if max( [ i[ 0 ] for i in factors ] ) > sqrt( n ) else 0


# //******************************************************************************
# //
# //  isPronic
# //
# //******************************************************************************

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
# //  generatePolydivisibles
# //
# //******************************************************************************

def generatePolydivisibles( _base ):
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


# //******************************************************************************
# //
# //  getNthStern
# //
# //******************************************************************************

def getNthStern( n ):
    """Return the nth number of Stern's diatomic series recursively"""
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

def getNthCalkinWilf( n ):
    if real_int( n ) < 0:
        raise ValueError( 'non-negative, real integer expected' )

    if n == 0:
        return 0

    return fdiv( getNthStern( n ), getNthStern( fadd( n, 1 ) ) )

