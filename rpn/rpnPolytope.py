#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPolytope.py
# //
# //  RPN command-line calculator polytope operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import arange, ceil, fadd, fac, fdiv, floor, fmod, fmul, fneg, fprod, \
                   fsub, fsum, mp, nint, pi, polyval, power, sqrt, tan

from rpn.rpnNumberTheory import getNthLinearRecurrence
from rpn.rpnSettings import setAccuracy
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, \
                         real, real_int


# //******************************************************************************
# //
# //  getNthGeneralizedPolygonalNumber
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthGeneralizedPolygonalNumber( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    negative = ( fmod( n, 2 ) == 0 )

    n = floor( fdiv( fadd( n, 1 ), 2 ) )

    if negative:
        n = fneg( n )

    return getNthPolygonalNumber( n, k )

@oneArgFunctionEvaluator( )
def getNthGeneralizedPentagonalNumber( n ):
    return getNthGeneralizedPolygonalNumber( n, 5 )


# //******************************************************************************
# //
# //  getNthPolygonalNumber
# //
# //******************************************************************************

def getNthPolygonalNumber( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coeff = fdiv( fsub( k, 2 ), 2 )
    return polyval( [ coeff, fneg( fsub( coeff, 1 ) ), 0 ], real( n ) )

@twoArgFunctionEvaluator( )
def getNthPolygonalNumberOperator( n, k ):
    return getNthPolygonalNumber( n, k )

@oneArgFunctionEvaluator( )
def getNthTriangularNumber( n ):
    return getNthPolygonalNumber( n, 3 )

@oneArgFunctionEvaluator( )
def getNthPentagonalNumber( n ):
    return getNthPolygonalNumber( n, 5 )

@oneArgFunctionEvaluator( )
def getNthHexagonalNumber( n ):
    return getNthPolygonalNumber( n, 6 )

@oneArgFunctionEvaluator( )
def getNthHeptagonalNumber( n ):
    return getNthPolygonalNumber( n, 7 )

@oneArgFunctionEvaluator( )
def getNthOctagonalNumber( n ):
    return getNthPolygonalNumber( n, 8 )

@oneArgFunctionEvaluator( )
def getNthNonagonalNumber( n ):
    return getNthPolygonalNumber( n, 9 )

@oneArgFunctionEvaluator( )
def getNthDecagonalNumber( n ):
    return getNthPolygonalNumber( n, 10 )


# //******************************************************************************
# //
# //  findPolygonalNumber
# //
# //  http://www.wolframalpha.com/input/?i=solve+%28+%28+k+%2F+2+%29+-+1+%29+x^2+-+%28+%28+k+%2F+2+%29+-+2+%29+x+%2B+0+%3D+n+for+x
# //
# //******************************************************************************

def findPolygonalNumber( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return floor( fdiv( fsum( [ sqrt( fsum( [ power( k, 2 ), fprod( [ 8, k, real( n ) ] ),
                                             fneg( fmul( 8, k ) ), fneg( fmul( 16, n ) ), 16 ] ) ),
                               k, -4 ] ), fmul( 2, fsub( k, 2 ) ) ) )

@twoArgFunctionEvaluator( )
def findPolygonalNumberOperator( n, k ):
    return findPolygonalNumber( n, k )

@oneArgFunctionEvaluator( )
def findTriangularNumber( n ):
    return findPolygonalNumber( n, 3 )

@oneArgFunctionEvaluator( )
def findSquareNumber( n ):
    return findPolygonalNumber( n, 4 )

@oneArgFunctionEvaluator( )
def findPentagonalNumber( n ):
    return findPolygonalNumber( n, 5 )

@oneArgFunctionEvaluator( )
def findHexagonalNumber( n ):
    return findPolygonalNumber( n, 6 )

@oneArgFunctionEvaluator( )
def findHeptagonalNumber( n ):
    return findPolygonalNumber( n, 7 )

@oneArgFunctionEvaluator( )
def findOctagonalNumber( n ):
    return findPolygonalNumber( n, 8 )

@oneArgFunctionEvaluator( )
def findNonagonalNumber( n ):
    return findPolygonalNumber( n, 9 )

@oneArgFunctionEvaluator( )
def findDecagonalNumber( n ):
    return findPolygonalNumber( n, 10 )


# //******************************************************************************
# //
# //  getNthCenteredPolygonalNumber
# //
# //******************************************************************************

def getNthCenteredPolygonalNumber( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coefficient = fdiv( k, 2 )
    return polyval( [ coefficient, fneg( coefficient ), 1 ], real( n ) )

@twoArgFunctionEvaluator( )
def getNthCenteredPolygonalNumberOperator( n, k ):
    return getNthCenteredPolygonalNumber( n, k )

@oneArgFunctionEvaluator( )
def getNthCenteredTriangularNumber( n ):
    return getNthCenteredPolygonalNumber( n, 3 )

@oneArgFunctionEvaluator( )
def getNthCenteredSquareNumber( n ):
    return getNthCenteredPolygonalNumber( n, 4 )

@oneArgFunctionEvaluator( )
def getNthCenteredPentagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 5 )

@oneArgFunctionEvaluator( )
def getNthCenteredHexagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 6 )

@oneArgFunctionEvaluator( )
def getNthCenteredHeptagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 7 )

@oneArgFunctionEvaluator( )
def getNthCenteredOctagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 8 )

@oneArgFunctionEvaluator( )
def getNthCenteredNonagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 9 )

@oneArgFunctionEvaluator( )
def getNthCenteredDecagonalNumber( n ):
    return getNthCenteredPolygonalNumber( n, 10 )


# //******************************************************************************
# //
# //  findCenteredPolygonalNumber
# //
# //  wolframalpha.com solved this for me.
# //
# //******************************************************************************

def findCenteredPolygonalNumber( n, k ):
    if real_int( k ) < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    s = fdiv( k, 2 )

    return nint( fdiv( fadd( sqrt( s ),
                       sqrt( fsum( [ fmul( 4, real( n ) ), s, -4 ] ) ) ), fmul( 2, sqrt( s ) ) ) )

@twoArgFunctionEvaluator( )
def findCenteredPolygonalNumberOperator( n, k ):
    return findCenteredPolygonalNumber( n, k )

@oneArgFunctionEvaluator( )
def findCenteredTriangularNumber( n ):
    return findCenteredPolygonalNumber( n, 3 )

@oneArgFunctionEvaluator( )
def findCenteredSquareNumber( n ):
    return findCenteredPolygonalNumber( n, 4 )

@oneArgFunctionEvaluator( )
def findCenteredPentagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 5 )

@oneArgFunctionEvaluator( )
def findCenteredHexagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 6 )

@oneArgFunctionEvaluator( )
def findCenteredHeptagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 7 )

@oneArgFunctionEvaluator( )
def findCenteredOctagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 8 )

@oneArgFunctionEvaluator( )
def findCenteredNonagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 9 )

@oneArgFunctionEvaluator( )
def findCenteredDecagonalNumber( n ):
    return findCenteredPolygonalNumber( n, 10 )



# //******************************************************************************
# //
# //  getNthPentagonalTriangularNumber
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/LRGF.html
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPentagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -195, 195 ], [ 1, 210, 40755 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthPentagonalSquareNumber
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/LRGF.html
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPentagonalSquareNumber( n ):
    return getNthLinearRecurrence( [ 1, -9603, 9603 ], [ 1, 9801, 94109401 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthHexagonalSquareNumber
# //
# //  http://oeis.org/A046177
# //
# //  a( n ) = floor( 1 / 32 * ( tan( 3 * pi / 8 ) ) ^ ( 8 * n - 4 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHexagonalSquareNumber( n ):
    return nint( floor( fdiv( power( tan( fdiv( fmul( 3, pi ), 8 ) ),
                                     fsub( fmul( 8, real_int( n ) ), 4 ) ), 32 ) ) )


# //******************************************************************************
# //
# //  getNthHexagonalPentagonalNumber
# //
# //  http://oeis.org/A046178
# //
# //  a( n ) = ceiling( 1 / 12 * ( sqrt( 3 ) - 1 ) * ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHexagonalPentagonalNumber( n ):
    return nint( ceil( fdiv( fmul( fsub( sqrt( 3 ), 1 ),
                                   power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, real_int( n ) ), 2 ) ) ),
                             12 ) ) )


# //******************************************************************************
# //
# //  getNthHeptagonalTriangularNumber
# //
# //  http://oeis.org/A046194
# //
# //  a(n) = 1 / 80 * ( ( 3 - sqrt( 5 ) * ( -1 ) ^ n ) * ( 2 + sqrt( 5 ) ) ^ ( 4n - 2 ) +
# //                    ( 3 + sqrt( 5 ) * ( -1 ) ^ n ) * ( 2 - sqrt( 5 ) ) ^ ( 4n - 2 ) - 14 )
# //
# //  LinearRecurrence[ { 1, 103682, -103682, -1, 1 },
# //                    { 1, 55, 121771, 5720653, 12625478965 }, n ]
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHeptagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -1, -103682, 103682, 1 ],
                                   [ 1, 55, 121771, 5720653, 12625478965 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthHeptagonalSquareNumber
# //
# //  http://oeis.org/A046195
# //
# //  LinearRecurrence[ { 1, 0, 1442, -1442, 0, -1, 1 },
# //                    { 1, 6, 49, 961, 8214, 70225, 1385329 }, n ]
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHeptagonalSquareNumber( n ):
    index = getNthLinearRecurrence( [ 1, -1, 0, -1442, 1442, 0, 1 ],
                                    [ 1, 6, 49, 961, 8214, 70225, 1385329 ], real_int( n ) )

    return getNthPolygonalNumber( index, 7 )


# //******************************************************************************
# //
# //  getNthHeptagonalPentagonalNumber
# //
# //  http://oeis.org/A048900
# //
# //  a(n) = floor( 1 / 240 * ( ( 2 + sqrt( 15 ) ) ^ 2 * ( 4 + sqrt( 15 ) ) ^ ( 4n - 3 ) ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHeptagonalPentagonalNumber( n ):
    return nint( floor( fdiv( fmul( power( fadd( 2, sqrt( 15 ) ), 2 ),
                                    power( fadd( 4, sqrt( 15 ) ),
                                           fsub( fmul( 4, real_int( n ) ), 3 ) ) ), 240 ) ) )


# //******************************************************************************
# //
# //  getNthHeptagonalHexagonalNumber
# //
# //  http://oeis.org/A048903
# //
# //  a(n) = floor( 1 / 80 * ( sqrt( 5 ) - 1 ) * ( 2 + sqrt( 5 ) ) ^ ( 8n - 5 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthHeptagonalHexagonalNumber( n ):
    return nint( floor( fdiv( fmul( fsub( sqrt( 5 ), 1 ),
                                    power( fadd( 2, sqrt( 5 ) ),
                                           fsub( fmul( 8, real_int( n ) ), 5 ) ) ), 80 ) ) )


# //******************************************************************************
# //
# //  getNthOctagonalTriangularNumber
# //
# //  From http://oeis.org/A046183
# //
# //  a(n) = floor( 1 / 96 * ( 7 - 2 * sqrt( 6 ) * ( -1 ) ^ n ) * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 4n - 2 ) )
# //
# //  LinearRecurrence[{1, 9602, -9602, -1, 1}, {1, 21, 11781, 203841, 113123361}, 13]
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthOctagonalTriangularNumber( n ):
    sign = power( -1, real( n ) )

    return nint( floor( fdiv( fmul( fsub( 7, fprod( [ 2, sqrt( 6 ), sign ] ) ),
                                    power( fadd( sqrt( 3 ), sqrt( 2 ) ),
                                           fsub( fmul( 4, real_int( n ) ), 2 ) ) ),
                              96 ) ) )


# //******************************************************************************
# //
# //  getNthOctagonalSquareNumber
# //
# //  From http://oeis.org/A036428:
# //
# //  a(n) = 1 / 12 * ( ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) + ( 2 - sqrt( 3 ) ) ^ ( 4n -2 ) - 2 )
# //  a(n) = floor ( 1 / 12 * ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthOctagonalSquareNumber( n ):
    return nint( floor( fdiv( power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, real( n ) ), 2 ) ), 12 ) ) )


# //******************************************************************************
# //
# //  getNthOctagonalPentagonalNumber
# //
# //  http://oeis.org/A046189
# //
# //  a(n) = floor( 1 / 96 * ( 11 - 6 * sqrt( 2 ) *( -1 ) ^ n ) * ( 1 + sqrt( 2 ) ) ^ ( 8 * n - 6 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthOctagonalPentagonalNumber( n ):
    return nint( floor( fdiv( fmul( fsub( 11, fprod( [ 6, sqrt( 2 ), power( -1, real_int( n ) ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 8, n ), 6 ) ) ), 96 ) ) )


# //******************************************************************************
# //
# //  getNthOctagonalHexagonalNumber
# //
# //  http://oeis.org/A046192
# //
# //  a(n) = floor( 1 / 96 * ( 3 * sqrt( 3 ) - sqrt( 2 ) ) * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 8n - 5 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthOctagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( fmul( 3, sqrt( 3 ) ), sqrt( 2 ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ),
                                     fsub( fmul( 8, real_int( n ) ), 5 ) ) ), 96 ) )


# //******************************************************************************
# //
# //  getNthOctagonalHeptagonalNumber
# //
# //  http://oeis.org/A048906
# //
# //  a(n) = floor( 1 / 480 * ( 17 + 2 * sqrt( 3 0 ) ) * ( sqrt( 5 ) + sqrt( 6 ) ) ^ ( 8n - 6 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthOctagonalHeptagonalNumber( n ):
    return nint( floor( fdiv( fmul( fadd( 17, fmul( sqrt( 30 ), 2 ) ),
                                    power( fadd( sqrt( 5 ), sqrt( 6 ) ),
                                           fsub( fmul( 8, real_int( n ) ), 6 ) ) ), 480 ) ) )


# //******************************************************************************
# //
# //  getNthNonagonalTriangularNumber
# //
# //  From http://oeis.org/A048907:
# //
# //  a( n ) = ( 5 / 14 ) +
# //           ( 9 / 28 ) * { [ 8 - 3 * sqrt( 7 ) ] ^ n + [ 8 + 3 * sqrt( 7 ) ] ^ n } +
# //           ( 3 / 28 ) * sqrt( 7 ) * { [ 8 + 3 * sqrt( 7 ) ] ^ n - [ 8 - 3 * sqrt( 7 ) ] ^ n }
# //
# //******************************************************************************

# TODO:  fix me

@oneArgFunctionEvaluator( )
def getNthNonagonalTriangularNumber( n ):
    a = fmul( 3, sqrt( 7 ) )
    b = fadd( 8, a )
    c = fsub( 8, a )

    return nint( fsum( [ fdiv( 5, 14 ),
                         fmul( fdiv( 9, 28 ), fadd( power( b, real_int( n ) ), power( c, n ) ) ),
                         fprod( [ fdiv( 3, 28 ),
                                  sqrt( 7 ),
                                  fsub( power( b, n ), power( c, n ) ) ] ) ] ) )


# //******************************************************************************
# //
# //  getNthNonagonalSquareNumber
# //
# //  From http://oeis.org/A048911:
# //
# //  Indices of square numbers which are also 9-gonal.
# //
# //  Let p = 8 * sqrt( 7 ) + 9 * sqrt( 14 ) - 7 * sqrt( 2 ) - 28 and
# //      q = 7 * sqrt( 2 ) + 9 * sqrt( 14 ) - 8 * sqrt( 7 ) - 28.
# //
# //  Then a( n ) = 1 / 112 *
# //                 ( ( p + q * (-1) ^ n ) * ( 2 * sqrt( 2 ) + sqrt( 7 ) ) ^ n -
# //                  ( p - q * (-1) ^ n ) * ( 2 * sqrt( 2 ) - sqrt( 7 ) ) ^ ( n - 1 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthNonagonalSquareNumber( n ):
    if real( n ) < 0:
        ValueError( '' )

    p = fsum( [ fmul( 8, sqrt( 7 ) ), fmul( 9, sqrt( 14 ) ), fmul( -7, sqrt( 2 ) ), -28 ] )
    q = fsum( [ fmul( 7, sqrt( 2 ) ), fmul( 9, sqrt( 14 ) ), fmul( -8, sqrt( 7 ) ), -28 ] )
    sign = power( -1, real_int( n ) )

    index = fdiv( fsub( fmul( fadd( p, fmul( q, sign ) ),
                              power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), n ) ),
                        fmul( fsub( p, fmul( q, sign ) ),
                              power( fsub( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), fsub( n, 1 ) ) ) ), 112 )

    return nint( power( nint( index ), 2 ) )


# //******************************************************************************
# //
# //  getNthNonagonalPentagonalNumber
# //
# //  http://oeis.org/A048915
# //
# //  a(n) = floor(1/336*(25+4*sqrt(21))*(5-sqrt(21)*(-1)^n)*(2*sqrt(7)+3*sqrt(3))^(4n-4)).
# //
# //  LinearRecurrence[{1, 146361602, -146361602, -1, 1}, {1, 651, 180868051, 95317119801, 26472137730696901}, 9]
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthNonagonalPentagonalNumber( n ):
    sqrt21 = sqrt( 21 )
    sign = power( -1, real_int( n ) )

    return nint( floor( fdiv( fprod( [ fadd( 25, fmul( 4, sqrt21 ) ),
                                       fsub( 5, fmul( sqrt21, sign ) ),
                                       power( fadd( fmul( 2, sqrt( 7 ) ), fmul( 3, sqrt( 3 ) ) ),
                                              fsub( fmul( 4, n ), 4 ) ) ] ),
                              336 ) ) )


# //******************************************************************************
# //
# //  getNthNonagonalHexagonalNumber
# //
# //  From http://oeis.org/A048907:
# //
# //  a( n ) = floor( 9 / 112 * ( 8 - 3 * sqrt( 7 ) * (-1) ^ n ) *
# //                            ( 8 + 3 * sqrt( 7 ) ) ^ ( 4 * n - 4 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthNonagonalHexagonalNumber( n ):
    # a = fmul( 3, sqrt( 7 ) )
    # b = fadd( 8, a )
    # c = fsub( 8, a )

    # sign = 1 #power( -1, n )
    # exponent = fsub( fmul( 4, n ), 4 )

    # print( str( fmul( c, sign ) ) + '  ' + str( power( b, exponent ) ) )

    # return floor( fprod( [ fdiv( 9, 112 ), fmul( c, sign ), power( b, exponent ) ] ) )

    return getNthLinearRecurrence( [ 1, -1, -4162056194, 4162056194, 1 ],
                                   [ 1, 325, 5330229625, 1353857339341, 22184715227362706161 ],
                                   real_int( n ) )


# //******************************************************************************
# //
# //  getNthNonagonalHeptagonalNumber
# //
# //  From http://oeis.org/A048921
# //
# //  a(n) = floor(1/560*(39+4*sqrt(35))*(6+sqrt(35))^(4*n-3)).
# //
# //  LinearRecurrence[{20163, -20163, 1}, {1, 26884, 542041975}, 9];
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthNonagonalHeptagonalNumber( n ):
    sqrt35 = sqrt( 35 )

    return nint( floor( fdiv( fmul( fadd( 39, fmul( 4, sqrt35 ) ),
                              power( fadd( 6, sqrt35 ), fsub( fmul( 4, real_int( n ) ), 3 ) ) ),
                              560 ) ) )


# //******************************************************************************
# //
# //  getNthNonagonalOctagonalNumber
# //
# //  From http://oeis.org/A048924:
# //
# //  a(n) = floor(1/672*(11*sqrt(7)-9*sqrt(6))*(sqrt(6)+sqrt(7))^(8n-5)).
# //
# //  LinearRecurrence[{454275, -454275, 1}, {1, 631125, 286703855361}, 30]
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthNonagonalOctagonalNumber( n ):
    sqrt6 = sqrt( 6 )
    sqrt7 = sqrt( 7 )

    return nint( floor( fdiv( fmul( fsub( fmul( 11, sqrt7 ), fmul( 9, sqrt6 ) ),
                                    power( fadd( sqrt6, sqrt7 ), fsub( fmul( 8, real_int( n ) ), 5 ) ) ),
                              672 ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalTriangularNumber
# //
# //  from http://oeis.org/A133216
# //
# //  a(n) = floor ( 1/64 * (9 + 4*sqrt(2)*(-1)^n) * (1+sqrt(2))^(4*n-6) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalTriangularNumber( n ):
    return nint( floor( fdiv( fmul( fadd( 9, fprod( [ 4, sqrt( 2 ),
                                                      power( -1, fadd( real_int( n ), 1 ) ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 4, fadd( n, 1 ) ), 6 ) ) ), 64 ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalCenteredSquareNumber
# //
# //  from http://oeis.org/A133142
# //
# //  a( n ) = ( 1/8 ) +
# //           ( 7/16 ) * [ 721 - 228 * sqrt( 10 ) ] ^ n -
# //           ( 1/8 ) * [ 721 - 228 * sqrt( 10 ) ] ^ n * sqrt( 10 ) +
# //           ( 1/8 ) * [ 721 + 228 * sqrt( 10 ) ] ^ n * sqrt( 10 ) +
# //           ( 7/16 ) * [ 721 + 228 * sqrt( 10 ) ] ^ n
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalCenteredSquareNumber( n ):
    sqrt10 = sqrt( 10 )

    dps = 7 * int( real_int( n ) )

    if mp.dps < dps:
        mp.dps = dps

    return nint( floor( fsum( [ fdiv( 1, 8 ),
                              fmul( fdiv( 7, 16 ), power( fsub( 721, fmul( 228, sqrt10 ) ), fsub( n, 1 ) ) ),
                              fmul( fmul( fdiv( 1, 8 ), power( fsub( 721, fmul( 228, sqrt10 ) ), fsub( n, 1 ) ) ), sqrt10 ),
                              fmul( fmul( fdiv( 1, 8 ), power( fadd( 721, fmul( 228, sqrt10 ) ), fsub( n, 1 ) ) ), sqrt10 ),
                              fmul( fdiv( 7, 16 ), power( fadd( 721, fmul( 228, sqrt10 ) ), fsub( n, 1 ) ) ) ] ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalPentagonalNumber
# //
# //  from http://oeis.org/A202563
# //
# //  a( n ) = floor( 25 / 192 * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 8 * n - 6 ) )
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalPentagonalNumber( n ):
    return nint( floor( fmul( fdiv( 25, 192 ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ),
                                     fsub( fmul( 8, real_int( n ) ), 6 ) ) ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalHexagonalNumber
# //
# //  http://oeis.org/A203134
# //
# //  a(n) = floor(1/64 *(5*sqrt(2)-1)*(sqrt(2)+1)^(8*n-5)).
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalHexagonalNumber( n ):
    return nint( floor( fdiv( fmul( fsub( fmul( 5, sqrt( 2 ) ), 1 ),
                                    power( fadd( sqrt( 2 ), 1 ),
                                           fsub( fmul( 8, real_int( n ) ), 5 ) ) ), 64 ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalHeptagonalNumber
# //
# //  http://oeis.org/A203408
# //
# //  a(n) = floor(1/320*(11-2*sqrt(10)*(-1)^n)*(1+sqrt(10))* (3+sqrt(10))^(4*n-3)).
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalHeptagonalNumber( n ):
    sqrt10 = sqrt( 10 )

    return nint( floor( fdiv( fprod( [ fsub( 11,
                                             fmul( fmul( 2, sqrt10 ),
                                                   power( -1, real_int( n ) ) ) ),
                                       fadd( 1, sqrt10 ),
                                       power( fadd( 3, sqrt10 ),
                                              fsub( fmul( 4, n ), 3 ) ) ] ), 320 ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalOctagonalNumber
# //
# //  http://oeis.org/A203624
# //
# //  a(n) = floor(1/192*(13+4*sqrt(3))*(2+sqrt(3))^(8*n-6)).
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalOctagonalNumber( n ):
    return nint( floor( fdiv( fmul( fadd( 13, fmul( 4, sqrt( 3 ) ) ),
                                    power( fadd( 2, sqrt( 3 ) ),
                                           fsub( fmul( 8, real_int( n ) ), 6 ) ) ), 192 ) ) )


# //******************************************************************************
# //
# //  getNthDecagonalNonagonalNumber
# //
# //  http://oeis.org/A203627
# //
# //  a(n) = floor(1/448*(15+2*sqrt(14))*(2*sqrt(2)+sqrt(7))^(8*n-6)).
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthDecagonalNonagonalNumber( n ):
    dps = 8 * int( real_int( n ) )

    if mp.dps < dps:
        mp.dps = dps

    return nint( floor( fdiv( fmul( fadd( 15, fmul( 2, sqrt( 14 ) ) ),
                                    power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ),
                                           fsub( fmul( 8, n ), 6 ) ) ), 448 ) ) )


# //******************************************************************************
# //
# //  findTetrahedralNumber
# //
# //  Thanks for wolframalpha.com for solving the reverse of the above formula.
# //
# //******************************************************************************

def findTetrahedralNumber( n ):
    # sqrt3 = sqrt( 3 )
    # curt3 = cbrt( 3 )

    # TODO:  finish me
    return 0

# http://www.wolframalpha.com/input/?i=solve+p%3D%281%2F6%29*%28n^3%2B3*n^2%2B2*n%29+for+n


# //******************************************************************************
# //
# //  getNthTruncatedTetrahedralNumber
# //
# //  Take the (3n-2)th terahedral number and chop off the (n-1)th tetrahedral
# //  number from each corner.
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTruncatedTetrahedralNumber( n ):
    return fmul( fdiv( real_int( n ), 6 ), fsum( [ fprod( [ 23, n, n ] ), fmul( -27, n ), 10 ] ) )


# //******************************************************************************
# //
# //  getNthSquareTriangularNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthSquareTriangularNumber( n ):
    neededPrecision = int( real_int( n ) * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        setAccuracy( neededPrecision )

    sqrt2 = sqrt( 2 )

    return nint( power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                           power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                                    fmul( 4, sqrt2 ) ), 2 ) )


# //******************************************************************************
# //
# //  getNthPolygonalPyramidalNumber
# //
# //******************************************************************************

def getNthPolygonalPyramidalNumber( n, k ):
    return fprod( [ real_int( n ), fadd( n, 1 ),
                    fsub( fmul( fsub( k, 2 ), n ), fsub( k, 5 ) ),
                    fdiv( 1, 6 ) ] )

@oneArgFunctionEvaluator( )
def getNthPyramidalNumber( n ):
    return getNthPolygonalPyramidalNumber( n, 4 )



# // A002415         4-dimensional pyramidal numbers: n^2*(n^2-1)/12.
# //                                                  n^4 - n^2 / 12
# //
# // A005585         5-dimensional pyramidal numbers: n(n+1)(n+2)(n+3)(2n+3)/5!.
# //
# // A001608         Perrin sequence (or Ondrej Such sequence): a(n) = a(n-2) + a(n-3).
# //                 LinearRecurrence[{0, 1, 1}, {3, 0, 2}, n]
# //
# // A001845         Centered octahedral numbers (crystal ball sequence for cubic lattice).
# //                 LinearRecurrence[{4, -6, 4, -1}, {1, 7, 25, 63}, 40]
# //
# // A046090         Consider all Pythagorean triples (X,X+1,Z) ordered by increasing Z; sequence gives X+1 values.
# //                 a(n+1)=round((1+(7+5*sqrt(2))*(3+2*sqrt(2))^n)/2);
# //                 LinearRecurrence[{7, -7, 1}, {1, 4, 21}, 25]
# //
# // A050534         Tritriangular numbers: a(n)=binomial(binomial(n,2),2) = n(n + 1)(n - 1)(n - 2)/8.
# //
# // A002817         Doubly triangular numbers: n*(n+1)*(n^2+n+2)/8.
# //                 a(n) = 3*binomial(n+2, 4)+binomial(n+1, 2).
# //
# // A007588         Stella octangula numbers: n*(2*n^2 - 1).
# //
# // A005803         Second-order Eulerian numbers: 2^n - 2*n.
# //
# // A060888         n^6-n^5+n^4-n^3+n^2-n+1.      -- general form of this
# //
# // A048736         Dana Scott's sequence: a(n) = (a(n-2) + a(n-1) * a(n-3)) / a(n-4), a(0) = a(1) = a(2) = a(3) = 1.
# //
# // A005894         Centered tetrahedral numbers.
# //                 a(n)=(2*n+1)*(n^2+n+3)/3
# //
# // A046176         Indices of square numbers which are also hexagonal.
# //
# // A056105         First spoke of a hexagonal spiral.
# //
# // A006522         4-dimensional analogue of centered polygonal numbers. Also number of regions created by sides and diagonals of n-gon in general position.
# //                 a(n)=binomial(n, 4)+ binomial(n-1, 2)
# //
# // A022086         Fibonacci sequence beginning 0 3.
# //                 a(n) = round( (6phi-3)/5 phi^n ) (works for n>2)
# //
# // A069778         q-factorial numbers 3!_q.
# //
# // A005021         Random walks (binomial transform of A006054).
# //
# // A195142         Concentric 10-gonal numbers.
# //
# // A000453         Stirling numbers of the second kind, S(n,4).
# //
# // A005915         Hexagonal prism numbers: (n + 1)*(3*n^2 + 3*n + 1).
# //
# // A002418         4-dimensional figurate numbers: (5*n-1)*binomial(n+2,3)/4.
# //
# // A005165         Alternating factorials: n! - (n-1)! + (n-2)! - ... 1!.
# //
# // A006007         4-dimensional analogue of centered polygonal numbers: a(n) = n(n+1)*(n^2+n+4)/12.
# //
# // A104621         Heptanacci-Lucas numbers.
# //


# //******************************************************************************
# //
# //  getNthStellaOctangulaNumber
# //
# //  http://oeis.org/A007588
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthStellaOctangulaNumber( n ):
    return polyval( [ 2, 0, -1, 0 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthCenteredCubeNumber
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCenteredCubeNumber( n ):
    return fadd( power( real_int( n ), 3 ), power( fsub( n, 1 ), 3 ) )


# //******************************************************************************
# //
# //  getNthCenteredTetrahedralNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCenteredTetrahedralNumber( n ):
    arg = real_int( fsub( n, 1 ) )
    return fmul( fadd( fmul( arg, 2 ), 1 ), fdiv( polyval( [ 1, 1, 3 ], arg ), 3 ) )


# //******************************************************************************
# //
# //  getNthCenteredOctahedralNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCenteredOctahedralNumber( n ):
    arg = real_int( fsub( n, 1 ) )
    return fmul( fadd( fmul( arg, 2 ), 1 ), fdiv( polyval( [ 2, 2, 3 ], arg ), 3 ) )


# //******************************************************************************
# //
# //  getNthCenteredDodecahedralNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCenteredDodecahedralNumber( n ):
    arg = real_int( fsub( n, 1 ) )
    return fmul( fadd( fmul( arg, 2 ), 1 ), polyval( [ 5, 5, 1 ], arg ) )


# //******************************************************************************
# //
# //  getNthCenteredIcosahedralNumber
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthCenteredIcosahedralNumber( n ):
    arg = real_int( fsub( n, 1 ) )
    return fmul( fadd( fmul( arg, 2 ), 1 ), fdiv( polyval( [ 5, 5, 3 ], arg ), 3 ) )


# //******************************************************************************
# //
# //  getNthTruncatedOctahedralNumber
# //
# //  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
# //  number from each of the six vertices.
# //
# //  16n^3 - 33n^2 + 24n - 6
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthTruncatedOctahedralNumber( n ):
    return polyval( [ 16, -33, 24, 6 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthRhombicDodecahedralNumber
# //
# //  Take the (3n-2)th octahedral number and chop off the (n-1)th square pyramid
# //  number from each of the six vertices.
# //
# //  Rho(n) = CCub(n) + 6 Pyr(n-1)
# //
# //  4n^3 + 6n^2 + 4n + 1
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthRhombicDodecahedralNumber( n ):
    return polyval( [ 4, 6, 4, 1 ], real_int( n ) )


# //******************************************************************************
# //
# //  getNthPentatopeNumber
# //
# //  1/24n ( n + 1 )( n + 2 )( n + 3 )
# //
# //  1/24 n^4 + 1/4 n^3 + 11/24 n^2 + 1/4 n
# //
# //  1/24 ( n^4 + 6 n^3 + 11 n^2 + 6n )
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthPentatopeNumber( n ):
    return fdiv( polyval( [ 1, 6, 11, 6, 0 ], real_int( n ) ), 24 )


# //******************************************************************************
# //
# //  getNthPolytopeNumber
# //
# //  d = dimension
# //
# //  (1/(d-1)!) PI k=0 to n-1 (n+k)
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getNthPolytopeNumber( n, d ):
    result = real_int( n )
    m = n + 1

    for i in arange( 1, d - 1 ):
        result = fmul( result, m )
        m += 1

    return fdiv( result, fac( d - 1 ) )


# //******************************************************************************
# //
# //  getNthStarNumber
# //
# //  https://en.wikipedia.org/wiki/Star_number
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNthStarNumber( n ):
    arg = real_int( n )
    return fadd( fmul( fmul( 6, n ), fsub( n, 1 ) ), 1 )


@oneArgFunctionEvaluator( )
def getNthDodecahedralNumber( n ):
    return polyval( [ fdiv( 9, 2 ), fdiv( -9, 2 ), 1, 0 ], real( n ) )

@oneArgFunctionEvaluator( )
def getNthIcosahedralNumber( n ):
    return polyval( [ fdiv( 5, 2 ), fdiv( -5, 2 ), 1, 0 ], real( n ) )

@oneArgFunctionEvaluator( )
def getNthOctahedralNumber( n ):
    return polyval( [ fdiv( 2, 3 ), 0, fdiv( 1, 3 ), 0 ], real( n ) )

@oneArgFunctionEvaluator( )
def getNthTetrahedralNumber( n ):
    return polyval( [ fdiv( 1, 6 ), fdiv( 1, 2 ), fdiv( 1, 3 ), 0 ], n )

