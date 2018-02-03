#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPolynomials.py
# //
# //  RPN command-line calculator polynomial operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

import collections

if six.PY3:
    from itertools import zip_longest
else:
    from itertools import izip_longest as zip_longest

from mpmath import acos, arange, chop, cos, fadd, fdiv, fmul, fneg, fprod, fsub, \
                   fsum, im, libmp, mp, mpc, polyroots, polyval, power, root, sin, sqrt

from rpn.rpnGenerator import RPNGenerator


# //******************************************************************************
# //
# //  class Polynomial
# //
# //  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
# //
# //******************************************************************************

class Polynomial( object ):
    '''This class represents a polynomial as a list of coefficients.'''
    def __init__( self, *args ):
        '''
        Create a polynomial in one of three ways:

        p = Polynomial( poly )              # copy constructor
        p = Polynomial( [ 1, 2, 3 ... ] )   # from sequence
        p = Polynomial( 1, 2, 3 ... )       # from scalars
        '''
        super( Polynomial, self ).__init__( )

        if len( args ) == 1:
            val = args[ 0 ]

            if isinstance( val, Polynomial ):                # copy constructor
                self.coeffs = val.coeffs[ : ]
            elif isinstance( val, collections.Iterable ):    # from sequence
                self.coeffs = list( val )
            else:                                            # from single scalar
                self.coeffs = [ val + 0 ]
        else:                                                # multiple scalars
            self.coeffs = [ i + 0 for i in args ]

        self.trim( )

    def __add__( self, val ):
        "Return self+val"
        if isinstance( val, Polynomial ):                    # add Polynomial
            res = reversed( [ a + b for a, b in zip_longest( reversed( self.coeffs ), reversed( val.coeffs ), fillvalue = 0 ) ] )
        else:                                                # add scalar
            if self.coeffs:
                res = self.coeffs[ : ]
                res[ 0 ] += val
            else:
                res = val

        return self.__class__( res )

    def __call__( self, val ):
        "Evaluate at X==val"
        res = 0
        pwr = 1

        for co in self.coeffs:
            res += co * pwr
            pwr *= val

        return res

    def __eq__( self, val ):
        "Test self==val"
        if isinstance( val, Polynomial ):
            return self.coeffs == val.coeffs
        else:
            return len( self.coeffs ) == 1 and self.coeffs[ 0 ] == val

    def __mul__( self, val ):
        "Return self*val"
        if isinstance( val, Polynomial ):
            _s = self.coeffs
            _v = val.coeffs
            res = [ 0 ] * ( len( _s ) + len( _v ) - 1 )

            for selfpow, selfco in enumerate( _s ):
                for valpow, valco in enumerate( _v ):
                    res[ selfpow + valpow ] += fmul( selfco, valco )
        else:
            res = [ co * val for co in self.coeffs ]

        return self.__class__( res )

    def __neg__( self ):
        "Return -self"
        return self.__class__( [ -co for co in self.coeffs ] )

    def __pow__( self, y, z = None ):
        raise NotImplemented( )

    def _radd__( self, val ):
        "Return val+self"
        return self + val

    def __repr__( self ):
        return "{0}({1})".format( self.__class__.__name__, self.coeffs )

    def __rmul__( self, val ):
        "Return val*self"
        return self * val

    def __rsub__( self, val ):
        "Return val-self"
        return -self + val

    def __str__( self ):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = [ ]

        for po, co in enumerate( self.coeffs ):
            if co:
                if po == 0:
                    po = ''
                elif po == 1:
                    po = 'x'
                else:
                    po = 'x^' + str( po )

                res.append( str( co ) + po )

        if res:
            res.reverse( )
            return ' + '.join( res )
        else:
            return "0"

    def __sub__( self, val ):
        "Return self-val"
        return self.__add__( -val )

    def trim( self ):
        "Remove leading 0-coefficients"
        while self.coeffs[ 0 ] == 0:
            del self.coeffs[ 0 ]

    def getCoefficients( self ):
        return self.coeffs


# //******************************************************************************
# //
# //  solveQuadraticPolynomial
# //
# //******************************************************************************

def solveQuadraticPolynomial( a, b, c ):
    '''This function applies the quadratic formula to solve a polynomial
    with coefficients of a, b, and c.'''
    if a == 0:
        if b == 0:
            raise ValueError( 'invalid expression, no variable coefficients' )
        else:
            # linear equation, one root
            return [ fdiv( fneg( c ), b ) ]
    else:
        d = sqrt( fsub( power( b, 2 ), fmul( 4, fmul( a, c ) ) ) )

        x1 = fdiv( fadd( fneg( b ), d ), fmul( 2, a ) )
        x2 = fdiv( fsub( fneg( b ), d ), fmul( 2, a ) )

        return [ x1, x2 ]


# //******************************************************************************
# //
# //  solveCubicPolynomial
# //
# //  Adapted from http://www.1728.org/cubic2.htm
# //
# //******************************************************************************

def solveCubicPolynomial( a, b, c, d ):
    '''This function applies the cubic formula to solve a polynomial
    with coefficients of a, b, c and d.'''
    if mp.dps < 50:
        mp.dps = 50

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


# //******************************************************************************
# //
# //  solveQuarticPolynomial
# //
# //  Adapted from http://www.1728.org/quartic2.htm
# //
# //******************************************************************************

def solveQuarticPolynomial( _a, _b, _c, _d, _e ):
    '''This function applies the quartic formula to solve a polynomial
    with coefficients of a, b, c, d, and e.'''
    if mp.dps < 50:
        mp.dps = 50

    # maybe it's really an order-3 polynomial
    if _a == 0:
        return solveCubicPolynomial( _b, _c, _d, _e )

    # degenerate case, just return the two real and two imaginary 4th roots of the
    # constant term divided by the 4th root of a
    elif _b == 0 and _c == 0 and _d == 0:
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

    y1, y2, y3 = solveCubicPolynomial( 1, fdiv( f, 2 ), fdiv( fsub( power( f, 2 ), fmul( 4, h ) ), 16 ),
                                       fneg( fdiv( power( g, 2 ), 64 ) ) )

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


# //******************************************************************************
# //
# //  addPolynomials
# //
# //******************************************************************************

def addPolynomials( a, b ):
    '''Adds two polynomials.'''
    len_diff = len( a ) - len( b )

    if len_diff > 0:
        for i in range( 0, len_diff ):
            b.insert( 0, 0 )
    else:
        for i in range( 0, -len_diff ):
            a.insert( 0, 0 )

    result = Polynomial( a )
    result += Polynomial( b )

    return result.getCoefficients( )


# //******************************************************************************
# //
# //  multiplyPolynomials
# //
# //******************************************************************************

def multiplyPolynomials( a, b ):
    '''Multiplies two polynomials together.'''
    result = Polynomial( a )
    result *= Polynomial( b )

    return result.getCoefficients( )


# //******************************************************************************
# //
# //  evaluatePolynomial
# //
# //******************************************************************************

def evaluatePolynomial( a, b ):
    '''Evaluates an arbitrary polynomial a for value b.'''
    if not isinstance( a, list ):
        a = [ a ]

    if isinstance( b, list ):
        return [ evaluatePolynomial( a, i ) for i in b ]
    else:
        return polyval( a, b )


# //******************************************************************************
# //
# //  exponentiatePolynomial
# //
# //******************************************************************************

def exponentiatePolynomial( n, k ):
    '''Exponentiates an arbitrary polynomial by an integral power k.'''
    if not isinstance( n, list ):
        n = [ n ]

    if isinstance( k, list ):
        return [ exponentiatePolynomial( n, i ) for i in k ]
    else:
        result = n

        for i in arange( 0, k - 1 ):
            result = multiplyPolynomials( result, n )

        return result


# //******************************************************************************
# //
# //  solvePolynomial
# //
# //******************************************************************************

def solvePolynomial( args ):
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
        result = polyroots( args, maxsteps = 100, extraprec = 20 )

    return result


# //******************************************************************************
# //
# //  multiplyListOfPolynomials
# //
# //******************************************************************************

def multiplyListOfPolynomials( args ):
    '''Interprets args as a list of polynomials and returns the polynomial
    product.'''
    if isinstance( args, RPNGenerator ):
        args = list( args )
    elif isinstance( args[ 0 ][ 0 ], ( list, RPNGenerator ) ):
        return [ multiplyListOfPolynomials( arg ) for arg in args ]
    elif not isinstance( args, list ):
        args = [ args ]

    result = None

    for arg in args:
        if isinstance( arg, RPNGenerator ):
            arg = list( arg )
        elif not isinstance( arg, list ):
            arg = [ arg ]

        if result is None:
            result = Polynomial( [ i for i in arg ] )
        else:
            result *= Polynomial( [ i for i in arg ] )

    return result.getCoefficients( )


# //******************************************************************************
# //
# //  sumListOfPolynomials
# //
# //******************************************************************************

def sumListOfPolynomials( args ):
    '''Interprets args as a list of polynomials and returns the polynomial sum.'''
    if isinstance( args, RPNGenerator ):
        args = list( args )
    elif isinstance( args[ 0 ][ 0 ], ( list, RPNGenerator ) ):
        return [ sumListOfPolynomials( arg ) for arg in args ]
    elif not isinstance( args, list ):
        args = [ args ]

    result = None

    for arg in args:
        if isinstance( arg, RPNGenerator ):
            arg = list( arg )
        elif not isinstance( arg, list ):
            arg = [ arg ]

        if result is None:
            result = Polynomial( [ i for i in arg ] )
        else:
            result += Polynomial( [ i for i in arg ] )

    return result.getCoefficients( )

