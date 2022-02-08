#!/usr/bin/env python

#*******************************************************************************
#
#  rpnPolynomials.py
#
#  rpnChilada polynomial operators
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#*******************************************************************************

import collections

from itertools import zip_longest
from mpmath import acos, arange, chop, cos, fadd, fdiv, fmul, fneg, fprod, fsub, \
                   fsum, im, libmp, mp, mpc, polyroots, polyval, power, root, sin, sqrt

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnUtils import listAndOneArgFunctionEvaluator, listArgFunctionEvaluator
from rpn.rpnValidator import argValidator, ComplexValidator, IntValidator, ListValidator


def determinant( M ):
    # pylint: disable=invalid-name
    """
    Computes the determinant of a matrix via the Schur determinant identity.
    Input: M -- square matrix; i.e., a list of lists.
    Output: A number.  If all input elements are integers, then this will also
            be an integer.

    Examples:
    > determinant([[1,2,3,4],[1,2,3,5],[1,2,4,4],[4,3,2,1]])
    5

    Adapted from https://pypi.python.org/pypi/labmath, which carries the MIT license
    but has no copyright notice.
    """
    # What is the algorithm's complexity?
    k = len( M )
    assert all( len( r ) == k for r in M )

    if k == 1:
        return M[ 0 ][ 0 ]

    if k == 2:
        return M[ 0 ][ 0 ] * M[ 1 ][ 1 ] - M[ 0 ][ 1 ] * M[ 1 ][ 0 ]

    if k == 3:
        a, b, c = M[ 0 ][ 0 ], M[ 0 ][ 1 ], M[ 0 ][ 2 ]
        d, e, f = M[ 1 ][ 0 ], M[ 1 ][ 1 ], M[ 1 ][ 2 ]
        g, h, i = M[ 2 ][ 0 ], M[ 2 ][ 1 ], M[ 2 ][ 2 ]
        return a * e * i + b * f * g + c * d * h - a * f * h - b * d * i - c * e * g

    sign = 1

    for r in range( k ):
        if M[ r ][ 0 ] != 0:
            break
    else:
        return 0

    if r != 0:
        M[ 0 ], M[ r ], sign = M[ r ], M[ 0 ], -1

    a = M[ 0 ][ 0 ]

    aD_CB = [ [ a * M[ r ][ s ] - M[ r ][ 0 ] * M[ 0 ][ s ] for s in range( 1, k ) ] for r in range( 1, k ) ]
    d = determinant( aD_CB )
    ints = isinstance( d, int ) and isinstance( a, int )
    return sign * d // a ** ( k - 2 ) if ints else sign * d / a ** ( k - 2 )


#*******************************************************************************
#
#  class Polynomial
#
#  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
#
#*******************************************************************************

class Polynomial( ):
    '''This class represents a polynomial as a list of coefficients.'''
    def __init__( self, *args ):
        '''
        Create a polynomial in one of three ways:

        p = Polynomial( poly )              # copy constructor
        p = Polynomial( [ 1, 2, 3 ... ] )   # from sequence
        p = Polynomial( 1, 2, 3 ... )       # from scalars
        '''
        super( ).__init__( )

        if len( args ) == 1:
            val = args[ 0 ]

            if isinstance( val, Polynomial ):                  # copy constructor
                self.coeffs = val.coeffs[ : ]
            elif isinstance( val, collections.abc.Iterable ):  # from sequence
                self.coeffs = list( val )
            else:                                              # from single scalar
                self.coeffs = [ val + 0 ]
        else:                                                   # multiple scalars
            self.coeffs = [ i + 0 for i in args ]

        self.trim( )

    def __add__( self, val ):
        'Return self + val'
        if isinstance( val, Polynomial ):                    # add Polynomial
            res = reversed( [ a + b for a, b in zip_longest( reversed( self.coeffs ),
                                                             reversed( val.coeffs ), fillvalue = 0 ) ] )
        else:                                                # add scalar
            if self.coeffs:
                res = self.coeffs[ : ]
                res[ 0 ] += val
            else:
                res = val

        return self.__class__( res )

    def __call__( self, val ):
        'Evaluate at X == val'
        res = 0
        pwr = 1

        for coeff in self.coeffs:
            res += coeff * pwr
            pwr *= val

        return res

    def __eq__( self, val ):
        'Test self == val'
        if isinstance( val, Polynomial ):
            return self.coeffs == val.coeffs

        return len( self.coeffs ) == 1 and self.coeffs[ 0 ] == val

    def __mul__( self, val ):
        'Return self * val'
        if isinstance( val, Polynomial ):
            ours = self.coeffs
            theirs = val.coeffs
            res = [ 0 ] * ( len( ours ) + len( theirs ) - 1 )

            for selfpow, selfco in enumerate( ours ):
                for valpow, valco in enumerate( theirs ):
                    res[ selfpow + valpow ] += fmul( selfco, valco )
        else:
            res = [ coeff * val for coeff in self.coeffs ]

        return self.__class__( res )

    def __neg__( self ):
        'Return -self'
        return self.__class__( [ -coeff for coeff in self.coeffs ] )

    def __pow__( self, y, z = None ):
        raise NotImplementedError( )

    def __radd__( self, val ):
        'Return val + self'
        return self + val

    def __repr__( self ):
        return f'{ self.__class__.__name__ }({ self.coeffs })'

    def __rmul__( self, val ):
        'Return val * self'
        return self * val

    def __rsub__( self, val ):
        'Return val - self'
        return -self + val

    def __str__( self ):
        'Return string formatted as aX^3 + bX^2 + c^X + d'
        res = [ ]

        for exponent, coeff in enumerate( self.coeffs ):
            if coeff:
                if exponent == 0:
                    exponent = ''
                elif exponent == 1:
                    exponent = 'x'
                else:
                    exponent = 'x^' + str( exponent )

                res.append( str( coeff ) + exponent )

        if res:
            res.reverse( )
            return ' + '.join( res )

        return '0'

    def __sub__( self, val ):
        'Return self-val'
        return self.__add__( -val )

    def trim( self ):
        'Remove leading 0-coefficients'
        while self.coeffs[ 0 ] == 0:
            del self.coeffs[ 0 ]

    def getCoefficients( self ):
        return self.coeffs

    def getDiscriminant( self ):
        '''
        Computes the discriminant of a polynomial.  The input is ordered from lowest
        degree to highest so that coeffs[k] is the coefficient of the x**k term.
        Input: coeffs -- list of numbers
        Output: A number

        Examples:
        > discriminant([1,2,3,4,5])
        10800

        Adapted from https://pypi.python.org/pypi/labmath, which carries the MIT license
        but has no copyright notice.
        '''
        result = [ ]
        a = self.coeffs[ ::-1 ]
        n = len( a ) - 1

        for x in range( n - 1 ):
            result.append( [ 0 ] * x + a + [ 0 ] * ( n - 2 - x ) )

        del a[ -1 ]

        for x in range( n ):
            a[ x ] *= n - x

        for x in range( n ):
            result.append( [ 0 ] * x + a + [ 0 ] * ( n - 1 - x ) )

        return ( -1 ) ** ( n * ( n - 1 ) // 2 ) * determinant( result ) / self.coeffs[ -1 ]


#*******************************************************************************
#
#  solveQuadraticPolynomialOperator
#
#*******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    # pylint: disable=invalid-name
    '''
    This function applies the quadratic formula to solve a polynomial
    with coefficients of a, b, and c.
    '''
    if a == 0:
        if b == 0:
            raise ValueError( 'invalid expression, no variable coefficients' )

        # linear equation, one root
        return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


@argValidator( [ ComplexValidator( ), ComplexValidator( ), ComplexValidator( ) ] )
def solveQuadraticPolynomialOperator( a, b, c ):
    return solveQuadraticPolynomial( a, b, c )


#*******************************************************************************
#
#  solveCubicPolynomialOperator
#
#  Adapted from http://www.1728.org/cubic2.htm
#
#*******************************************************************************

@argValidator( [ ComplexValidator( ), ComplexValidator( ), ComplexValidator( ), ComplexValidator( ) ] )
def solveCubicPolynomial( a, b, c, d ):
    # pylint: disable=invalid-name
    '''
    This function applies the cubic formula to solve a polynomial
    with coefficients of a, b, c and d.
    '''
    mp.dps = max( 50, mp.dps )

    if a == 0:
        return solveQuadraticPolynomial( b, c, d )

    f = fdiv( fsub( fdiv( fmul( 3, c ), a ), fdiv( power( b, 2 ), power( a, 2 ) ) ), 3 )

    g = fdiv( fadd( fsub( fdiv( fmul( 2, power( b, 3 ) ), power( a, 3 ) ),
                          fdiv( fprod( [ 9, b, c ] ), power( a, 2 ) ) ),
                    fdiv( fmul( 27, d ), a ) ), 27 )
    h = fadd( fdiv( power( g, 2 ), 4 ), fdiv( power( f, 3 ), 27 ) )

    # all three roots are the same
    if h == 0:
        x1 = fneg( root( fdiv( d, a ), 3 ) )
        x2 = x1
        x3 = x2
    # two imaginary and one real root
    elif h > 0:
        r = fadd( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if r < 0:
            s = fneg( root( fneg( r ), 3 ) )
        else:
            s = root( r, 3 )

        t = fsub( fneg( fdiv( g, 2 ) ), sqrt( h ) )

        if t < 0:
            u = fneg( root( fneg( t ), 3 ) )
        else:
            u = root( t, 3 )

        x1 = fsub( fadd( s, u ), fdiv( b, fmul( 3, a ) ) )

        real = fsub( fdiv( fneg( fadd( s, u ) ), 2 ), fdiv( b, fmul( 3, a ) ) )
        imaginary = fdiv( fmul( fsub( s, u ), sqrt( 3 ) ), 2 )

        x2 = mpc( real, imaginary )
        x3 = mpc( real, fneg( imaginary ) )
    # all real roots
    else:
        j = sqrt( fsub( fdiv( power( g, 2 ), 4 ), h ) )
        k = acos( fneg( fdiv( g, fmul( 2, j ) ) ) )

        if j < 0:
            l = fneg( root( fneg( j ), 3 ) )
        else:
            l = root( j, 3 )

        m = cos( fdiv( k, 3 ) )
        n = fmul( sqrt( 3 ), sin( fdiv( k, 3 ) ) )
        p = fneg( fdiv( b, fmul( 3, a ) ) )

        x1 = fsub( fmul( fmul( 2, l ), cos( fdiv( k, 3 ) ) ), fdiv( b, fmul( 3, a ) ) )
        x2 = fadd( fmul( fneg( l ), fadd( m, n ) ), p )
        x3 = fadd( fmul( fneg( l ), fsub( m, n ) ), p )

    return [ chop( x1 ), chop( x2 ), chop( x3 ) ]


@argValidator( [ ComplexValidator( ), ComplexValidator( ), ComplexValidator( ), ComplexValidator( ) ] )
def solveCubicPolynomialOperator( a, b, c, d ):
    return solveCubicPolynomial( a, b, c, d )


#*******************************************************************************
#
#  solveQuarticPolynomialOperator
#
#  Adapted from http://www.1728.org/quartic2.htm
#
#*******************************************************************************

@argValidator( [ ComplexValidator( ), ComplexValidator( ), ComplexValidator( ), ComplexValidator( ),
                 ComplexValidator( ) ] )
def solveQuarticPolynomialOperator( _a, _b, _c, _d, _e ):
    # pylint: disable=invalid-name
    '''
    This function applies the quartic formula to solve a polynomial
    with coefficients of a, b, c, d, and e.
    '''
    mp.dps = max( 50, mp.dps )

    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )

    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    if _b == 0 and _c == 0 and _d == 0:
        e = fdiv( _e, _a )

        f = root( _a, 4 )

        x1 = fdiv( root( fneg( e ), 4 ), f )
        x2 = fdiv( fneg( root( fneg( e ), 4 ) ), f )
        x3 = fdiv( mpc( 0, root( fneg( e ), 4 ) ), f )
        x4 = fdiv( mpc( 0, fneg( root( fneg( e ), 4 ) ) ), f )

        return [ x1, x2, x3, x4 ]

    # otherwise we have a regular quartic to solve
    b = fdiv( _b, _a )
    c = fdiv( _c, _a )
    d = fdiv( _d, _a )
    e = fdiv( _e, _a )

    # we turn the equation into a cubic that we can solve
    f = fsub( c, fdiv( fmul( 3, power( b, 2 ) ), 8 ) )
    g = fsum( [ d, fdiv( power( b, 3 ), 8 ), fneg( fdiv( fmul( b, c ), 2 ) ) ] )
    h = fsum( [ e, fneg( fdiv( fmul( 3, power( b, 4 ) ), 256 ) ),
                fmul( power( b, 2 ), fdiv( c, 16 ) ), fneg( fdiv( fmul( b, d ), 4 ) ) ] )

    roots = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                  fneg( fdiv( power( g, 2 ), 64 ) ) )
    y1 = roots[ 0 ]
    y2 = roots[ 1 ]
    y3 = roots[ 2 ]

    # pick two non-zero roots, if there are two imaginary roots, use them
    if y1 == 0:
        root1 = y2
        root2 = y3
    elif y2 == 0:
        root1 = y1
        root2 = y3
    elif y3 == 0:
        root1 = y1
        root2 = y2
    elif im( y1 ) != 0:
        root1 = y1

        if im( y2 ) != 0:
            root2 = y2
        else:
            root2 = y3
    else:
        root1 = y2
        root2 = y3

    # more variables...
    p = sqrt( root1 )
    q = sqrt( root2 )
    r = fdiv( fneg( g ), fprod( [ 8, p, q ] ) )
    s = fneg( fdiv( b, 4 ) )

    # put together the 4 roots
    x1 = fsum( [ p, q, r, s ] )
    x2 = fsum( [ p, fneg( q ), fneg( r ), s ] )
    x3 = fsum( [ fneg( p ), q, fneg( r ), s ] )
    x4 = fsum( [ fneg( p ), fneg( q ), r, s ] )

    return [ chop( x1 ), chop( x2 ), chop( x3 ), chop( x4 ) ]


#*******************************************************************************
#
#  addPolynomialsOperator
#
#*******************************************************************************

@argValidator( [ ListValidator( ), ListValidator( ) ] )
def addPolynomialsOperator( a, b ):
    '''Adds two polynomials.'''
    lengthDiff = len( a ) - len( b )

    if lengthDiff > 0:
        for _ in range( 0, lengthDiff ):
            b.insert( 0, 0 )
    else:
        for _ in range( 0, -lengthDiff ):
            a.insert( 0, 0 )

    result = Polynomial( a )
    result += Polynomial( b )

    return result.getCoefficients( )


#*******************************************************************************
#
#  multiplyPolynomialsOperator
#
#*******************************************************************************

def multiplyPolynomials( a, b ):
    '''Multiplies two polynomials together.'''
    result = Polynomial( a )
    result *= Polynomial( b )

    return result.getCoefficients( )


@argValidator( [ ListValidator( ), ListValidator( ) ] )
def multiplyPolynomialsOperator( a, b ):
    return multiplyPolynomials( a, b )


#*******************************************************************************
#
#  evaluatePolynomialOperator
#
#*******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), ComplexValidator( ) ] )
def evaluatePolynomialOperator( a, b ):
    return polyval( a, b )


#*******************************************************************************
#
#  exponentiatePolynomialOperator
#
#*******************************************************************************

@listAndOneArgFunctionEvaluator( )
@argValidator( [ ListValidator( ), IntValidator( 1 ) ] )
def exponentiatePolynomialOperator( n, k ):
    '''Exponentiates an arbitrary polynomial by an integral power k.'''
    result = n

    for _ in arange( 0, k - 1 ):
        result = multiplyPolynomials( result, n )

    return result


#*******************************************************************************
#
#  solvePolynomialOperator
#
#*******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def solvePolynomialOperator( args ):
    '''Uses the mpmath solve function to numerically solve an arbitrary polynomial.'''
    if isinstance( args, RPNGenerator ):
        args = list( args )
    elif not isinstance( args, list ):
        args = [ args ]

    while args[ 0 ] == 0:
        args = args[ 1 : ]

    length = len( args )

    if length == 0:
        raise ValueError( 'invalid expression, no variable coefficients' )

    if length < 2:
        raise ValueError( "'solve' requires at least an order-1 polynomial (i.e., 2 terms)" )

    nonZeroes = 0
    nonZeroIndex = 0

    for i in range( 0, length ):
        if args[ i ] != 0:
            nonZeroes += 1
            nonZeroIndex = i

    if nonZeroes == 1 and nonZeroIndex == length - 1:
        raise ValueError( 'invalid expression, no variable coefficients' )

    if nonZeroes == 1:
        return [ 0 ] * ( length - nonZeroIndex - 1 )

    try:
        result = polyroots( args )
    except libmp.libhyper.NoConvergence:
        try:
            #  Let's try again, really hard!
            result = polyroots( args, maxsteps = 2000, extraprec = 5000 )
        except libmp.libhyper.NoConvergence as e:
            raise ValueError( 'polynomial failed to converge' ) from e

    return result


#*******************************************************************************
#
#  multiplyPolynomialListOperator
#
#*******************************************************************************

def multiplyPolynomialList( args ):
    '''Interprets args as a list of polynomials and returns the polynomial
    product.'''
    if isinstance( args, RPNGenerator ):
        args = list( args )
    elif isinstance( args[ 0 ][ 0 ], ( list, RPNGenerator ) ):
        return [ multiplyPolynomialList( arg ) for arg in args ]
    elif not isinstance( args, list ):
        args = [ args ]

    result = None

    for arg in args:
        if isinstance( arg, RPNGenerator ):
            arg = list( arg )
        elif not isinstance( arg, list ):
            arg = [ arg ]

        if result is None:
            # arg might be a generator pylint: disable=unnecessary-comprehension
            result = Polynomial( [ i for i in arg ] )
        else:
            # arg might be a generator
            result *= Polynomial( [ i for i in arg ] )

    return result.getCoefficients( )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def multiplyPolynomialListOperator( n ):
    return multiplyPolynomialList( n )


#*******************************************************************************
#
#  sumPolynomialListOperator
#
#*******************************************************************************

def sumPolynomialList( args ):
    '''Interprets args as a list of polynomials and returns the polynomial sum.'''
    if isinstance( args, RPNGenerator ):
        args = list( args )
    elif isinstance( args[ 0 ][ 0 ], ( list, RPNGenerator ) ):
        return [ sumPolynomialList( arg ) for arg in args ]
    elif not isinstance( args, list ):
        args = [ args ]

    result = None

    for arg in args:
        if isinstance( arg, RPNGenerator ):
            arg = list( arg )
        elif not isinstance( arg, list ):
            arg = [ arg ]

        if result is None:
            # arg might be a generator
            # pylint: disable=unnecessary-comprehension
            result = Polynomial( [ i for i in arg ] )
        else:
            # arg might be a generator
            result += Polynomial( [ i for i in arg ] )

    return result.getCoefficients( )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def sumPolynomialListOperator( n ):
    return sumPolynomialList( n )


#*******************************************************************************
#
#  getPolynomialDiscriminantOperator
#
#*******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( )] )
def getPolynomialDiscriminantOperator( n ):
    return Polynomial( n ).getDiscriminant( )
