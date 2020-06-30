#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnMath.py
# //
# //  rpnChilada mathematical operators
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from functools import reduce

from hyperop import hyperop
from mpmath import acos, acosh, acot, acoth, acsc, acsch, agm, arange, arg, \
                   asec, asech, asin, asinh, atan, atanh, autoprec, ceil, \
                   conj, cos, cosh, cot, coth, csc, csch, e, exp, fabs, fadd, \
                   fdiv, floor, fmod, fmul, fneg, fsub, hypot, im, isint, \
                   lambertw, li, ln, log, log10, mpc, mpf, nint, phi, polyexp, \
                   polylog, power, re, root, sec, sech, sign, sin, sinh, sqrt, \
                   tan, tanh, unitroots

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, real, real_int


# //******************************************************************************
# //
# //  add
# //
# //  We used to be able to call fadd directly, but now we want to be able to add
# //  units.  Adding units includes an implicit conversion if the units are not
# //  the same, assuming they are compatible.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def add( n, k ):
    if isinstance( n, RPNDateTime ) and isinstance( k, RPNMeasurement ):
        return n.add( k )
    elif isinstance( n, RPNMeasurement ) and isinstance( k, RPNDateTime ):
        return k.add( n )
    elif isinstance( n, RPNMeasurement ):
        return n.add( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).add( k )
    else:
        return fadd( n, k )

@oneArgFunctionEvaluator( )
def increment( n ):
    return add( n, 1 )


# //******************************************************************************
# //
# //  subtract
# //
# //  We used to be able to call fsub directly, but now we want to be able to
# //  subtract units and do the appropriate conversions.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def subtract( n, k ):
    if isinstance( n, RPNDateTime ):
        return n.subtract( k )
    elif isinstance( n, RPNMeasurement ):
        if isinstance( k, RPNDateTime ):
            return k.subtract( n )
        else:
            return n.subtract( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).subtract( k )
    else:
        return fsub( n, k )

@oneArgFunctionEvaluator( )
def decrement( n ):
    return subtract( n, 1 )


# //******************************************************************************
# //
# //  getNegative
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNegative( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fneg( n.value ), n.units )
    else:
        return fneg( n )


# //******************************************************************************
# //
# //  getSign
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getSign( n ):
    if isinstance( n, RPNMeasurement ):
        return sign( n.value )
    else:
        return sign( n )


# //******************************************************************************
# //
# //  getValue
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getValue( n ):
    if isinstance( n, RPNMeasurement ):
        return n.value
    else:
        return n


# //******************************************************************************
# //
# //  divide
# //
# //  We used to be able to call fdiv directly, but now we want to also divide
# //  the units.  Doing so lets us do all kinds of great stuff because now we
# //  can support compound units without having to explicitly declare them in
# //  makeUnits.py.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def divide( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.divide( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).divide( k )
    else:
        return fdiv( n, k )


# //******************************************************************************
# //
# //  multiply
# //
# //  We used to be able to call fmul directly, but now we want to also multiply
# //  the units.  This allows compound units and the conversion routines try to
# //  be smart enough to deal with this.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def multiply( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.multiply( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).multiply( k )
    else:
        return fmul( n, k )


# //******************************************************************************
# //
# //  getPower
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getPower( n, k ):
    if isinstance( n, RPNMeasurement ):
        result = RPNMeasurement( n )
        return result.exponentiate( k )
    else:
        return power( n, k )

@oneArgFunctionEvaluator( )
def square( n ):
    return getPower( n, 2 )

@oneArgFunctionEvaluator( )
def cube( n ):
    return getPower( n, 3 )


# //******************************************************************************
# //
# //  getRoot
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getRoot( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getRoot( k )

    if not isint( k ):
        return power( n, fdiv( 1, k ) )
    else:
        return root( n, k )

@oneArgFunctionEvaluator( )
def getSquareRoot( n ):
    return getRoot( n, 2 )

@oneArgFunctionEvaluator( )
def getCubeRoot( n ):
    return getRoot( n, 3 )


# //******************************************************************************
# //
# //  getSquareSuperRoot
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getSquareSuperRoot( n ):
    return power( e, lambertw( log( n ) ) )


# //******************************************************************************
# //
# //  getCubeSuperRoot
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getCubeSuperRoot( n ):
    value = fmul( 2, log( n ) )
    return sqrt( fdiv( value, lambertw( value ) ) )


# //******************************************************************************
# //
# //  getSuperRoot
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getSuperRoot( n, k ):
    k = fsub( real_int( k ), 1 )
    value = fmul( k, log( n ) )
    return root( fdiv( value, lambertw( value ) ), k )


# //******************************************************************************
# //
# //  getSuperRoots
# //
# //  Returns all the super-roots of n, not just the nice, positive, real one.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getSuperRoots( n, k ):
    k = fsub( real_int( k ), 1 )
    factors = [ fmul( i, root( k, k ) ) for i in unitroots( int( k ) ) ]
    base = root( fdiv( log( n ), lambertw( fmul( k, log( n ) ) ) ), k )

    return [ fmul( i, base ) for i in factors ]


# //******************************************************************************
# //
# //  getReciprocal
# //
# //  We used to be able to call fdiv directly, but now we want to handle
# //  RPNMeasurements.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getReciprocal( n ):
    if isinstance( n, RPNMeasurement ):
        return n.invert( invertValue=False )
    else:
        return fdiv( 1, n )


# //******************************************************************************
# //
# //  getAbsoluteValue
# //
# //  We used to be able to call fabs directly, but now we want to handle
# //  RPNMeasurements.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getAbsoluteValue( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fabs( n.value ), n.units )
    else:
        return fabs( n )


# //******************************************************************************
# //
# //  getNearestInt
# //
# //  We used to be able to call fdiv directly, but now we want to handle
# //  RPNMeasurements.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNearestInt( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( nint( n.value ), n.units )
    else:
        return nint( n )


# //******************************************************************************
# //
# //  tetrate
# //
# //  This is the smaller (left-associative) version of the hyper4 operator.
# //
# //  This function forces the second argument to an integer and runs in O( n )
# //  time based on the second argument.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def tetrate( i, j ):
    result = i

    for _ in arange( 1, j ):
        result = power( result, i )

    return result


# //******************************************************************************
# //
# //  tetrateRight
# //
# //  This is the larger, right-associative version of the hyper4 operator.
# //
# //  This function forces the second argument to an integer and runs in O( n )
# //  time based on the second argument.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def tetrateRight( i, j ):
    result = i

    for _ in arange( 1, j ):
        result = power( i, result )

    return result


# //******************************************************************************
# //
# //  isDivisible
# //
# //  Is n divisible by k?
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isDivisible( n, k ):
    if n == 0:
        return 1

    return 1 if ( n >= k ) and ( fmod( real( n ), real( k ) ) == 0 ) else 0


# //******************************************************************************
# //
# //  isSquare
# //
# //  The "smarter" algorithm is slower... WHY?!
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isSquare( n ):
    #mod = fmod( n, 16 )

    #if mod in [ 0, 1, 4, 9 ]:
    sqrtN = sqrt( n )
    return 1 if sqrtN == floor( sqrtN ) else 0
    #else:
    #    return 0


# //******************************************************************************
# //
# //  isPower
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isPower( n, k ):
    #print( 'log( n )', log( n ) )
    #print( 'log( k )', log( k ) )
    #print( 'divide', autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )
    return isInteger( autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )


# //******************************************************************************
# //
# //  isKthPower
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isKthPower( n, k ):
    if not isint( k, gaussian=True ) and isint( k ):
        raise ValueError( 'integer arguments expected' )

    if k == 1:
        return 1
    elif k < 1:
        raise ValueError( 'a positive power k is expected' )

    if im( n ):
        # I'm not sure why this is necessary...
        if re( n ) == 0:
            return isKthPower( im( n ), k )

        # We're looking for a Gaussian integer among any of the roots.
        for i in [ autoprec( root )( n, k, i ) for i in arange( k ) ]:
            if isint( i, gaussian=True ):
                return 1

        return 0
    else:
        rootN = autoprec( root )( n, k )
        return 1 if isint( rootN, gaussian=True ) else 0


# //******************************************************************************
# //
# //  performTrigOperation
# //
# //******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, RPNMeasurement ):
        value = mpf( i.convertValue( RPNMeasurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )

@oneArgFunctionEvaluator( )
def get_acos( n ):
    return performTrigOperation( n, acos )

@oneArgFunctionEvaluator( )
def get_acosh( n ):
    return performTrigOperation( n, acosh )

@oneArgFunctionEvaluator( )
def get_acot( n ):
    return performTrigOperation( n, acot )

@oneArgFunctionEvaluator( )
def get_acoth( n ):
    return performTrigOperation( n, acoth )

@oneArgFunctionEvaluator( )
def get_acsc( n ):
    return performTrigOperation( n, acsc )

@oneArgFunctionEvaluator( )
def get_acsch( n ):
    return performTrigOperation( n, acsch )

@oneArgFunctionEvaluator( )
def get_asec( n ):
    return performTrigOperation( n, asec )

@oneArgFunctionEvaluator( )
def get_asech( n ):
    return performTrigOperation( n, asech )

@oneArgFunctionEvaluator( )
def get_asin( n ):
    return performTrigOperation( n, asin )

@oneArgFunctionEvaluator( )
def get_asinh( n ):
    return performTrigOperation( n, asinh )

@oneArgFunctionEvaluator( )
def get_atan( n ):
    return performTrigOperation( n, atan )

@oneArgFunctionEvaluator( )
def get_atanh( n ):
    return performTrigOperation( n, atanh )

@oneArgFunctionEvaluator( )
def get_cos( n ):
    return performTrigOperation( n, cos )

@oneArgFunctionEvaluator( )
def get_cosh( n ):
    return performTrigOperation( n, cosh )

@oneArgFunctionEvaluator( )
def get_cot( n ):
    return performTrigOperation( n, cot )

@oneArgFunctionEvaluator( )
def get_coth( n ):
    return performTrigOperation( n, coth )

@oneArgFunctionEvaluator( )
def get_csc( n ):
    return performTrigOperation( n, csc )

@oneArgFunctionEvaluator( )
def get_csch( n ):
    return performTrigOperation( n, csch )

@oneArgFunctionEvaluator( )
def get_sec( n ):
    return performTrigOperation( n, sec )

@oneArgFunctionEvaluator( )
def get_sech( n ):
    return performTrigOperation( n, sech )

@oneArgFunctionEvaluator( )
def get_sin( n ):
    return performTrigOperation( n, sin )

@oneArgFunctionEvaluator( )
def get_sinh( n ):
    return performTrigOperation( n, sinh )

@oneArgFunctionEvaluator( )
def get_tan( n ):
    return performTrigOperation( n, tan )

@oneArgFunctionEvaluator( )
def get_tanh( n ):
    return performTrigOperation( n, tanh )


# //******************************************************************************
# //
# //  isEqual
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isEqual( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isEqual( k ) else 0
    else:
        if isinstance( n, RPNMeasurement ):
            return 1 if k.isEqual( n ) else 0
        else:
            return 1 if n == k else 0


# //******************************************************************************
# //
# //  isNotEqual
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isNotEqual( n, k ):
    return 0 if isEqual( n, k ) else 1


# //******************************************************************************
# //
# //  isGreater
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isLarger( k ) else 0
    else:
        return 1 if real( n ) > real( k ) else 0


# //******************************************************************************
# //
# //  isLess
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isSmaller( k ) else 0
    else:
        return 1 if real( n ) < real( k ) else 0


# //******************************************************************************
# //
# //  isNotGreater
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isNotGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotLarger( k ) else 0
    else:
        return 1 if real( n ) <= real( k ) else 0


# //******************************************************************************
# //
# //  isNotLess
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isNotLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotSmaller( k ) else 0
    else:
        return 1 if real( n ) >= real( k ) else 0


# //******************************************************************************
# //
# //  isInteger
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isInteger( n ):
    return 1 if fmod( real( n ), 1 ) == 0 else 0


# //******************************************************************************
# //
# //  roundOff
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def roundOff( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundOff( n.value ), n.units )
    else:
        return floor( fadd( real( n ), 0.5 ) )


# //******************************************************************************
# //
# //  roundByValue
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def roundByValue( n, value ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundByValue( n.value, value ), n.units )
    else:
        return fmul( floor( fdiv( fadd( real( n ), fdiv( value, 2 ) ), value ) ), value )


# //******************************************************************************
# //
# //  roundByDigits
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def roundByDigits( n, digits ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundByDigits( n.value, digits ), n.units )
    else:
        return roundByValue( real( n ), power( 10, digits ) )


# //******************************************************************************
# //
# //  getLarger
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getLarger( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isGreater( n, k ) else k

    return n if real( n ) > real( k ) else k


# //******************************************************************************
# //
# //  getSmaller
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getSmaller( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isLess( n, k ) else k

    return n if real( n ) < real( k ) else k


# //******************************************************************************
# //
# //  getFloor
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getFloor( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getFloor( n.value ), n.units )
    else:
        return floor( n )


# //******************************************************************************
# //
# //  getCeiling
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getCeiling( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getCeiling( n.value ), n.units )
    else:
        return ceil( n )


# //******************************************************************************
# //
# //  getMaximum
# //
# //******************************************************************************

def getMaximum( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ max( arg ) for arg in n ]
    else:
        return max( n )


# //******************************************************************************
# //
# //  getMinimum
# //
# //******************************************************************************

def getMinimum( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ min( arg ) for arg in n ]
    else:
        return min( n )


# //******************************************************************************
# //
# //  isEven
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isEven( n ):
    return 1 if fmod( real_int( n ), 2 ) == 0 else 0


# //******************************************************************************
# //
# //  isOdd
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isOdd( n ):
    return 1 if fmod( real_int( n ), 2 ) == 1 else 0


# //******************************************************************************
# //
# //  isNotZero
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isNotZero( n ):
    return 0 if n == 0 else 1


# //******************************************************************************
# //
# //  isZero
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isZero( n ):
    return 1 if n == 0 else 0


# //******************************************************************************
# //
# //  getMantissa
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getMantissa( n ):
    return fmod( real( n ), 1 )


# //******************************************************************************
# //
# //  getModulo
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getModulo( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getModulo( k )
    elif isinstance( k, RPNMeasurement ):
        raise ValueError( 'cannot take a non-measurement modulo a measurement' )
    else:
        return fmod( real( n ), real( k ) )




# //******************************************************************************
# //
# //  getAGM
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getAGM( n, k ):
    return agm( n, k )


# //******************************************************************************
# //
# //  getExp
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getExp( n ):
    return exp( n )


# //******************************************************************************
# //
# //  getExp10
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getExp10( n ):
    return power( 10, n )


# //******************************************************************************
# //
# //  getExpPhi
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getExpPhi( n ):
    return power( phi, n )


# //******************************************************************************
# //
# //  getArgument
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getArgument( n ):
    return arg( n )


# //******************************************************************************
# //
# //  getConjugate
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getConjugate( n ):
    return conj( n )


# //******************************************************************************
# //
# //  getI
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getI( n ):
    return mpc( real = '0.0', imag = n )


# //******************************************************************************
# //
# //  getImaginary
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getImaginary( n ):
    return im( n )


# //******************************************************************************
# //
# //  getReal
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getReal( n ):
    return re( n )


# //******************************************************************************
# //
# //  getLambertW
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLambertW( n ):
    return lambertw( n )


# //******************************************************************************
# //
# //  getLI
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLI( n ):
    return li( n )


# //******************************************************************************
# //
# //  getLog
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLog( n ):
    return ln( n )


# //******************************************************************************
# //
# //  getLog10
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLog10( n ):
    return log10( n )


# //******************************************************************************
# //
# //  getLog2
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getLog2( n ):
    return log( n, 2 )


# //******************************************************************************
# //
# //  getLogXY
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getLogXY( n, k ):
    return log( n, k )


# //******************************************************************************
# //
# //  getPolyexp
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getPolyexp( n, k ):
    return polyexp( n, k )


# //******************************************************************************
# //
# //  getPolylog
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getPolylog( n, k ):
    return polylog( n, k )


# //******************************************************************************
# //
# //  calculateHypotenuse
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def calculateHypotenuse( n, k ):
    return hypot( n, k )


# //******************************************************************************
# //
# //  calculateNthHyperoperator
# //
# //******************************************************************************

class hyperopLeft( hyperop ):
    def __call__( self, a, b ):
        '''
        Evaluate and return expression H[n](a,b).
        (a,b) must be non-negative for n>4.
        '''
        check = self._check_value( a, b )

        if check is not None:
            return check

        # Apply fold
        return reduce( lambda x, y: self.lower( x, y ), self._repeat( a, b ) )

def calculateNthHyperoperator( a, b, c ):
    if a == 0:
        return c + 1

    if b == 0:
        if c == 1:
            return 0
        else:
            return 1

    if c == 0:
        return 1

    if a > 1 and b == 1:
        return 1

    if a > 1 and c == 1:
        return b

    if b == 2 and c == 2:
        if a == 0:
            return 3
        else:
            return 4

    return hyperopLeft( a )( b, c )


# //******************************************************************************
# //
# //  calculateNthRightHyperoperator
# //
# //******************************************************************************

def calculateNthRightHyperoperator( a, b, c ):
    if a == 0:
        return c + 1

    if b == 0:
        if c == 1:
            return 0
        else:
            return 1

    if c == 0:
        return 1

    if a > 1 and b == 1:
        return 1

    if a > 1 and c == 1:
        return b

    if b == 2 and c == 2:
        if a == 0:
            return 3
        else:
            return 4

    return hyperop( a )( b, c )

