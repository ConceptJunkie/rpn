#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnPolytope.py
# //
# //  RPN command-line calculator polytope operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************


from mpmath import *

from rpnNumberTheory import *


# //******************************************************************************
# //
# //  getNthPolygonalNumber
# //
# //******************************************************************************

def getNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coeff = fdiv( fsub( k, 2 ), 2 )
    return polyval( [ coeff, fneg( fsub( coeff, 1 ) ), 0 ], n )


# //******************************************************************************
# //
# //  findNthPolygonalNumber
# //
# //  http://www.wolframalpha.com/input/?i=solve+%28+%28+k+%2F+2+%29+-+1+%29+x^2+-+%28+%28+k+%2F+2+%29+-+2+%29+x+%2B+0+%3D+n+for+x
# //
# //******************************************************************************

def findNthPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    return fdiv( fsum( [ sqrt( fsum( [ power( k, 2 ), fprod( [ 8, k, n ] ),
                                       fneg( fmul( 8, k ) ), fneg( fmul( 16, n ) ), 16 ] ) ),
                         k, -4 ] ), fmul( 2, fsub( k, 2 ) ) )


# //******************************************************************************
# //
# //  getCenteredPolygonalNumber
# //
# //******************************************************************************

def getCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    coefficient = fdiv( k, 2 )
    return polyval( [ coefficient, fneg( coefficient ), 1 ], n )


# //******************************************************************************
# //
# //  findCenteredPolygonalNumber
# //
# //  wolframalpha.com solved this for me.
# //
# //******************************************************************************

def findCenteredPolygonalNumber( n, k ):
    if k < 3:
        raise ValueError( 'the number of sides of the polygon cannot be less than 3,' )

    s = fdiv( k, 2 )

    return fdiv( fadd( sqrt( s ), sqrt( fsum( [ fmul( 4, n ), s, -4 ] ) ) ), fmul( 2, sqrt( s ) ) )


# //******************************************************************************
# //
# //  getNthPentagonalTriangularNumber
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/LRGF.html
# //
# //******************************************************************************

def getNthPentagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -195, 195 ], [ 1, 210, 40755 ], n )


# //******************************************************************************
# //
# //  getNthPentagonalSquareNumber
# //
# //  http://www.maths.surrey.ac.uk/hosted-sites/R.Knott/Fibonacci/LRGF.html
# //
# //******************************************************************************

def getNthPentagonalSquareNumber( n ):
    return getNthLinearRecurrence( [ 1, -9603, 9603 ], [ 1, 9801, 94109401 ], n )


# //******************************************************************************
# //
# //  getNthHexagonalSquareNumber
# //
# //  http://oeis.org/A046177
# //
# //  a( n ) = floor( 1 / 32 * ( tan( 3 * pi / 8 ) ) ^ ( 8 * n - 4 ) )
# //
# //******************************************************************************

# //******************************************************************************
# //
# //  getNthHexagonalPentagonalNumber
# //
# //  http://oeis.org/A046178
# //
# //  a( n ) = ceiling( 1 / 12 * ( sqrt( 3 ) - 1 ) * ( 2 + sqrt( 3 ) ) ^ ( 4n - 2 ) )
# //
# //******************************************************************************

def getNthHexagonalPentagonalNumber( n ):
    return ceil( fdiv( fmul( fsub( sqrt( 3 ), 1 ),
                             power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                       12 ) )


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

def getNthHeptagonalTriangularNumber( n ):
    return getNthLinearRecurrence( [ 1, -1, -103682, 103682, 1 ],
                                   [ 1, 55, 121771, 5720653, 12625478965 ], n )


# //******************************************************************************
# //
# //  getNthHeptagonalSquareNumber
# //
# //  http://oeis.org/A046195
# //
# //  LinearRecurrence[ { 1 , 0, 1442, -1442, 0, -1, 1 },
# //                    { 1, 6, 49, 961, 8214, 70225, 1385329 }, n ]
# //
# //******************************************************************************

def getNthHeptagonalSquareNumber( n ):
    index = getNthLinearRecurrence( [ 1, -1, 0, -1442, 1442, 0, 1 ],
                                    [ 1, 6, 49, 961, 8214, 70225, 1385329 ], n )

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

def getNthHeptagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( power( fadd( 2, sqrt( 15 ) ), 2 ),
                              power( fadd( 4, sqrt( 15 ) ), fsub( fmul( 4, n ), 3 ) ) ), 240 ) )


# //******************************************************************************
# //
# //  getNthHeptagonalHexagonalNumber
# //
# //  http://oeis.org/A048903
# //
# //  a(n) = floor( 1 / 80 * ( sqrt( 5 ) - 1 ) * ( 2 + sqrt( 5 ) ) ^ ( 8n - 5 ) )
# //
# //******************************************************************************

def getNthHeptagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( sqrt( 5 ), 1 ),
                              power( fadd( 2, sqrt( 5 ) ), fsub( fmul( 8, n ), 5 ) ) ), 80 ) )


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

def getNthOctagonalTriangularNumber( n ):
    sign = power( -1, n )

    return floor( fdiv( fmul( fsub( 7, fprod( [ 2, sqrt( 6 ), sign ] ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 4, n ), 2 ) ) ),
                        96 ) )


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

def getNthOctagonalSquareNumber( n ):
    return floor( fdiv( power( fadd( 2, sqrt( 3 ) ), fsub( fmul( 4, n ), 2 ) ), 12 ) )


# //******************************************************************************
# //
# //  getNthOctagonalPentagonalNumber
# //
# //  http://oeis.org/A046189
# //
# //  a(n) = floor( 1 / 96 * ( 11 - 6 * sqrt( 2 ) *( -1 ) ^ n ) * ( 1 + sqrt( 2 ) ) ^ ( 8 * n - 6 ) )
# //
# //******************************************************************************

def getNthOctagonalPentagonalNumber( n ):
    return floor( fdiv( fmul( fsub( 11, fprod( [ 6, sqrt( 2 ), power( -1, n ) ] ) ),
                              power( fadd( 1, sqrt( 2 ) ), fsub( fmul( 8, n ), 6 ) ) ), 96 ) )


# //******************************************************************************
# //
# //  getNthOctagonalHexagonalNumber
# //
# //  http://oeis.org/A046192
# //
# //  a(n) = floor( 1 / 96 * ( 3 * sqrt( 3 ) - sqrt( 2 ) ) * ( sqrt( 3 ) + sqrt( 2 ) ) ^ ( 8n - 5 ) )
# //
# //******************************************************************************

def getNthOctagonalHexagonalNumber( n ):
    return floor( fdiv( fmul( fsub( fmul( 3, sqrt( 3 ) ), sqrt( 2 ) ),
                              power( fadd( sqrt( 3 ), sqrt( 2 ) ), fsub( fmul( 8, n ), 5 ) ) ), 96 ) )


# //******************************************************************************
# //
# //  getNthOctagonalHeptagonalNumber
# //
# //  http://oeis.org/A048906
# //
# //  a(n) = floor( 1 / 480 * ( 17 + 2 * sqrt( 3 0 ) ) * ( sqrt( 5 ) + sqrt( 6 ) ) ^ ( 8n - 6 ) )
# //
# //******************************************************************************

def getNthOctagonalHeptagonalNumber( n ):
    return floor( fdiv( fmul( fadd( 17, fmul( sqrt( 30 ), 2 ) ),
                              power( fadd( sqrt( 5 ), sqrt( 6 ) ), fsub( fmul( 8, n ), 6 ) ) ), 480 ) )


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

def getNthNonagonalTriangularNumber( n ):
    a = fmul( 3, sqrt( 7 ) )
    b = fadd( 8, a )
    c = fsub( 8, a )

    return fsum( [ fdiv( 5, 14 ),
                   fmul( fdiv( 9, 28 ), fadd( power( b, n ), power( c, n ) ) ),
                   fprod( [ fdiv( 3, 28 ),
                            sqrt( 7 ),
                            fsub( power( b, n ), power( c, n ) ) ] ) ] )


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

def getNthNonagonalSquareNumber( n ):
    p = fsum( [ fmul( 8, sqrt( 7 ) ), fmul( 9, sqrt( 14 ) ), fmul( -7, sqrt( 2 ) ), -28 ] )
    q = fsum( [ fmul( 7, sqrt( 2 ) ), fmul( 9, sqrt( 14 ) ), fmul( -8, sqrt( 7 ) ), -28 ] )
    sign = power( -1, n )

    index = fdiv( fsub( fmul( fadd( p, fmul( q, sign ) ),
                              power( fadd( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), n ) ),
                        fmul( fsub( p, fmul( q, sign ) ),
                              power( fsub( fmul( 2, sqrt( 2 ) ), sqrt( 7 ) ), fsub( n, 1 ) ) ) ), 112 )

    return power( round( index ), 2 )


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

def getNthNonagonalPentagonalNumber( n ):
    sqrt21 = sqrt( 21 )
    sign = power( -1, n )

    return floor( fdiv( fprod( [ fadd( 25, fmul( 4, sqrt21 ) ),
                                 fsub( 5, fmul( sqrt21, sign ) ),
                                 power( fadd( fmul( 2, sqrt( 7 ) ), fmul( 3, sqrt( 3 ) ) ),
                                        fsub( fmul( 4, n ), 4 ) ) ] ),
                        336 ) )


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

def getNthNonagonalHexagonalNumber( n ):
    #a = fmul( 3, sqrt( 7 ) )
    #b = fadd( 8, a )
    #c = fsub( 8, a )

    #sign = 1 #power( -1, n )
    #exponent = fsub( fmul( 4, n ), 4 )

    #print( str( fmul( c, sign ) ) + '  ' + str( power( b, exponent ) ) )

    #return floor( fprod( [ fdiv( 9, 112 ), fmul( c, sign ), power( b, exponent ) ] ) )

    return getNthLinearRecurrence( [ 1, -1, -4162056194, 4162056194, 1 ],
                                   [ 1, 325, 5330229625, 1353857339341, 22184715227362706161 ], n )


# //******************************************************************************
# //
# //  getNthNonagonalHeptagonalNumber
# //
# //  From http://oeis.org/A048921
# //
# //  a(n) = floor(1/560*(39+4*sqrt(35))*(6+sqrt(35))^(4*n-3)).
# //
# //  LinearRecurrence[{20163, -20163, 1}, {1, 26884, 542041975}, 9]; (* Ant King, Dec 31 2011 *)
# //
# //******************************************************************************

def getNthNonagonalHeptagonalNumber( n ):
    sqrt35 = sqrt( 35 )

    return floor( fdiv( fmul( fadd( 39, fmul( 4, sqrt35 ) ),
                        power( fadd( 6, sqrt35 ), fsub( fmul( 4, n ), 3 ) ) ),
                        560 ) )


# //******************************************************************************
# //
# //  getNthNonagonalOctagonalNumber
# //
# //  From http://oeis.org/A048924:
# //
# //  a(n) = floor(1/672*(11*sqrt(7)-9*sqrt(6))*(sqrt(6)+sqrt(7))^(8n-5)).
# //
# //  LinearRecurrence[{454275, -454275, 1}, {1, 631125, 286703855361}, 30] (* Vincenzo Librandi, Dec 24 2011 *)
# //
# //******************************************************************************

def getNthNonagonalOctagonalNumber( n ):
    sqrt6 = sqrt( 6 )
    sqrt7 = sqrt( 7 )

    return floor( fdiv( fmul( fsub( fmul( 11, sqrt7 ), fmul( 9, sqrt6 ) ),
                              power( fadd( sqrt6, sqrt7 ), fsub( fmul( 8, n ), 5 ) ) ),
                        672 ) )

# Dec-tri
# http://oeis.org/A133216
# a(n) = floor ( 1/64 * (9 + 4*sqrt(2)*(-1)^n) * (1+sqrt(2))^(4*n-6) )

# Dec-square
# http://oeis.org/A133142
#  a(n)=(1/8)+(7/16)*[721-228*sqrt(10)]^n-(1/8)*[721-228*sqrt(10)]^n*sqrt(10)+(1/8)*[721+228 *sqrt(10)]^n*sqrt(10)+(7/16)*[721+228*sqrt(10)]^n

# Dec-pent
# http://oeis.org/A202563
# a(n) = floor(25/192*(sqrt(3)+sqrt(2))^(8*n-6))

# Dec-hex
# http://oeis.org/A203134
# a(n) = floor(1/64 *(5*sqrt(2)-1)*(sqrt(2)+1)^(8*n-5)).

# Dec-hept
# http://oeis.org/A203408
# a(n) = floor(1/320*(11-2*sqrt(10)*(-1)^n)*(1+sqrt(10))* (3+sqrt(10))^(4*n-3)).

# Dec-oct
# http://oeis.org/A203624
# a(n) = floor(1/192*(13+4*sqrt(3))*(2+sqrt(3))^(8*n-6)).

# Dec-non
# http://oeis.org/A203627
# a(n) = floor(1/448*(15+2*sqrt(14))*(2*sqrt(2)+sqrt(7))^(8*n-6)).


# //******************************************************************************
# //
# //  findTetrahedralNumber
# //
# //  Thanks for wolframalpha.com for solving the reverse of the above formula.
# //
# //******************************************************************************

def findTetrahedralNumber( n ):
    #sqrt3 = sqrt( 3 )
    #curt3 = cbrt( 3 )

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

def getNthTruncatedTetrahedralNumber( n ):
    return fmul( fdiv( n, 6 ), fsum( [ fprod( [ 23, n, n ] ), fmul( -27, n ), 10 ] ) )


# //******************************************************************************
# //
# //  getNthSquareTriangularNumber
# //
# //******************************************************************************

def getNthSquareTriangularNumber( n ):
    neededPrecision = int( n * 3.5 )  # determined by experimentation

    if mp.dps < neededPrecision:
        setAccuracy( neededPrecision )

    sqrt2 = sqrt( 2 )

    return power( fdiv( fsub( power( fadd( 1, sqrt2 ), fmul( 2, n ) ),
                                     power( fsub( 1, sqrt2 ), fmul( 2, n ) ) ),
                               fmul( 4, sqrt2 ) ), 2 )


# //******************************************************************************
# //
# //  getNthPolygonalPyramidalNumber
# //
# //******************************************************************************

def getNthPolygonalPyramidalNumber( n, k ):
    return fprod( [ n, fadd( n, 1 ),
                    fsub( fmul( fsub( k, 2 ), n ), fsub( k, 5 ) ),
                    fdiv( 1, 6 ) ] )


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
# // A022095         Fibonacci sequence beginning 1 5.
# //                 a(n) = ((2*sqrt(5)-1)*(((1+sqrt(5))/2)^(n+1)) + (2*sqrt(5)+1)*(((1-sqrt(5))/2)^(n+1)))/(sqrt(5)).
# //
# // A005894         Centered tetrahedral numbers.
# //                 a(n)=(2*n+1)*(n^2+n+3)/3
# //
# // A015447         Generalized Fibonacci numbers: a(n) = a(n-1) + 11*a(n-2).
# //                 a(n)={[ (1+3*sqrt(5))/2 ]^(n+1) - [ (1-3*sqrt(5))/2 ]^(n+1)}/3*sqrt(5).
# //                 LinearRecurrence[{1, 11}, {1, 1}, 30]
# //                 CoefficientList[Series[ 1/(1-x-11 x^2), {x, 0, 50}], x]
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
# // A074584         Esanacci ("6-anacci") numbers.
# //                 LinearRecurrence[{1, 1, 1, 1, 1, 1}, {6, 1, 3, 7, 15, 31}, 50]
# //
# // A195142         Concentric 10-gonal numbers.
# //
# // A000453         Stirling numbers of the second kind, S(n,4).
# //
# // A005915         Hexagonal prism numbers: (n + 1)*(3*n^2 + 3*n + 1).
# //
# // A015442         Generalized Fibonacci numbers: a(n) = a(n-1) + 7 a(n-2), a(0)=0, a(1)=1.
# //                 a(n) = ( ((1+sqrt(29))/2)^(n+1) - ((1-sqrt(29))/2)^(n+1) )/sqrt(29)
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

def getNthStellaOctangulaNumber( n ):
    return polyval( [ 2, 0, -1, 0 ], n )


# //******************************************************************************
# //
# //  getNthCenteredCube
# //
# //  from Conway and Guy's "The Book of Numbers"
# //
# //******************************************************************************

def getNthCenteredCubeNumber( n ):
    return fadd( power( n, 3 ), power( fsub( n, 1 ), 3 ) )


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

def getNthTruncatedOctahedralNumber( n ):
    return polyval( [ 16, -33, 24, 6 ], n )


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

def getNthRhombicDodecahedralNumber( n ):
    return polyval( [ 4, 6, 4, 1 ], n )


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

def getNthPentatopeNumber( n ):
    return fdiv( polyval( [ 1, 6, 11, 6, 0 ], n ), 24 )


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

def getNthPolytopeNumber( n, d ):
    result = n
    m = n + 1

    for i in arange( 1, d - 1 ):
        result = fmul( result, m )
        m += 1

    return fdiv( result, fac( d - 1 ) )


