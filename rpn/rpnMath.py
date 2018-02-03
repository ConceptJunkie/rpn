#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnMath.py
# //
# //  RPN command-line calculator, mathematical operators
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import acos, acosh, acot, acoth, acsc, acsch, agm, arange, arg, \
                   asec, asech, asin, asinh, atan, atanh, ceil, conj, cos, \
                   cosh, cot, coth, csc, csch, exp, fabs, fadd, fdiv, floor, \
                   fmod, fmul, fneg, fsub, hypot, im, lambertw, li, ln, log, \
                   log10, mpc, mpf, nint, phi, polyexp, polylog, power, re, \
                   root, sec, sech, sign, sin, sinh, sqrt, tan, tanh

from rpn.rpnDateTime import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement, RPNUnits
from rpn.rpnName import getOrdinalName
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
        return RPNMeasurement( fneg( n.getValue( ) ), n.getUnits( ) )
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
        return sign( n.getValue( ) )
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
        return n.getValue( )
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
        n = n.normalizeUnits( )

        if not isInteger( k ):
            raise ValueError( 'cannot take a fractional root of a measurement' )

        newUnits = RPNUnits( n.getUnits( ) )

        for unit, exponent in newUnits.items( ):
            if fmod( exponent, k ) != 0:
                if k == 2:
                    name = 'square'
                elif k == 3:
                    name = 'cube'
                else:
                    name = getOrdinalName( k )

                raise ValueError( 'cannot take the ' + name + ' root of this measurement: ', n.getUnits( ) )

            newUnits[ unit ] /= k

        value = root( n.getValue( ), k )

        return RPNMeasurement( value, newUnits )

    return root( n, real( k ) )

@oneArgFunctionEvaluator( )
def getSquareRoot( n ):
    return getRoot( n, 2 )

@oneArgFunctionEvaluator( )
def getCubeRoot( n ):
    return getRoot( n, 3 )


# //******************************************************************************
# //
# //  takeReciprocal
# //
# //  We used to be able to call fdiv directly, but now we want to handle
# //  RPNMeasurements.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def takeReciprocal( n ):
    if isinstance( n, RPNMeasurement ):
        return n.invert( )
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
        return RPNMeasurement( fabs( n.getValue( ) ), n.getUnits( ) )
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
        return RPNMeasurement( nint( n.getValue( ) ), n.getUnits( ) )
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

    for x in arange( 1, j ):
        result = power( result, i )

    return result


# //******************************************************************************
# //
# //  tetrateLarge
# //
# //  This is the larger (right-associative) version of the hyper4 operator.
# //
# //  This function forces the second argument to an integer and runs in O( n )
# //  time based on the second argument.
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


# //******************************************************************************
# //
# //  isDivisible
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isDivisible( n, k ):
    return 1 if fmod( real( n ), real( k ) ) == 0 else 0


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
    logN = log( n, k )

    return 1 if logN == floor( logN ) else 0


# //******************************************************************************
# //
# //  isKthPower
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def isKthPower( n, k ):
    rootN = root( n, real_int( k ) )

    return 1 if rootN == floor( rootN ) else 0


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
    return 1 if n == floor( n ) else 0


# //******************************************************************************
# //
# //  roundOff
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def roundOff( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundOff( n.getValue( ) ), n.getUnits( ) )
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
        return RPNMeasurement( roundByValue( n.getValue( ), value ), n.getUnits( ) )
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
        return RPNMeasurement( roundByDigits( n.getValue( ), digits ), n.getUnits( ) )
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
        return RPNMeasurement( getFloor( n.getValue( ) ), n.getUnits( ) )
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
        return RPNMeasurement( getCeiling( n.getValue( ) ), n.getUnits( ) )
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
    return 1 if fmod( real( n ), 2 ) == 0 else 0


# //******************************************************************************
# //
# //  isOdd
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def isOdd( n ):
    return 1 if fmod( real( n ), 2 ) == 1 else 0


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
    return fsub( n, floor( n ) )


# //******************************************************************************
# //
# //  getModulo
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getModulo( n, k ):
    return fmod( real( n ), real( k ) )


# //******************************************************************************
# //
# //  getAGM
# //
# //******************************************************************************

@twoArgFunctionEvaluator( )
def getAGM( n, k ):
    return agm( n, k ),


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

