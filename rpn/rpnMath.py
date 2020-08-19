#!/usr/bin/env python

#******************************************************************************
#
#  rpnMath.py
#
#  rpnChilada mathematical operators
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

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
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, listArgFunctionEvaluator
from rpn.rpnValidator import argValidator, ComplexOrMeasurementValidator, ComplexOrMeasurementValidator, \
                             ComplexOrMeasurementOrDateTimeValidator, DefaultValidator, \
                             IntValidator, ListValidator, RealValidator, RealOrMeasurementValidator, \
                             RealOrMeasurementOrDateTimeValidator


#******************************************************************************
#
#  addOperator
#
#  We used to be able to call fadd directly, but now we want to be able to add
#  units.  Adding units includes an implicit conversion if the units are not
#  the same, assuming they are compatible.
#
#******************************************************************************

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

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementOrDateTimeValidator( ), ComplexOrMeasurementValidator( ) ] )
def addOperator( n, k ):
    return add( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementOrDateTimeValidator( ) ] )
def incrementOperator( n ):
    return add( n, 1 )


#******************************************************************************
#
#  subtractOperator
#
#  We used to be able to call fsub directly, but now we want to be able to
#  subtract units and do the appropriate conversions.
#
#******************************************************************************

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

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementOrDateTimeValidator( ), ComplexOrMeasurementOrDateTimeValidator( ) ] )
def subtractOperator( n, k ):
    return subtract( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementOrDateTimeValidator( ) ] )
def decrementOperator( n ):
    return subtract( n, 1 )


#******************************************************************************
#
#  getNegativeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getNegativeOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fneg( n.value ), n.units )
    else:
        return fneg( n )


#******************************************************************************
#
#  getSignOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getSignOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return sign( n.value )
    else:
        return sign( n )


#******************************************************************************
#
#  getValueOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getValueOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.value
    else:
        return n


#******************************************************************************
#
#  divideOperator
#
#  We used to be able to call fdiv directly, but now we want to also divide
#  the units.  Doing so lets us do all kinds of great stuff because now we
#  can support compound units without having to explicitly declare them in
#  makeUnits.py.
#
#******************************************************************************

def divide( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.divide( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).divide( k )
    else:
        return fdiv( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def divideOperator( n, k ):
    return divide( n, k )


#******************************************************************************
#
#  multiplyOperator
#
#  We used to be able to call fmul directly, but now we want to also multiply
#  the units.  This allows compound units and the conversion routines try to
#  be smart enough to deal with this.
#
#******************************************************************************

def multiply( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.multiply( k )
    elif isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).multiply( k )
    else:
        return fmul( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def multiplyOperator( n, k ):
    return multiply( n, k )


#******************************************************************************
#
#  getPowerOperator
#
#******************************************************************************

def getPower( n, k ):
    if isinstance( n, RPNMeasurement ):
        result = RPNMeasurement( n )
        return result.exponentiate( k )
    else:
        return power( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getPowerOperator( n, k ):
    return getPower( n, k )

def square( n ):
    return getPower( n, 2 )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def squareOperator( n ):
    return getPower( n, 2 )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cubeOperator( n ):
    return getPower( n, 3 )


#******************************************************************************
#
#  getRootOperator
#
#******************************************************************************

def getRoot( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getRoot( k )

    if not isint( k ):
        return power( n, fdiv( 1, k ) )
    else:
        return root( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getRootOperator( n, k ):
    return getRoot( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getSquareRootOperator( n ):
    return getRoot( n, 2 )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getCubeRootOperator( n ):
    return getRoot( n, 3 )


#******************************************************************************
#
#  getSquareSuperRootOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getSquareSuperRootOperator( n ):
    '''Returns the positive, real square super root of n.'''
    return power( e, lambertw( log( n ) ) )


#******************************************************************************
#
#  getCubeSuperRootOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getCubeSuperRootOperator( n ):
    '''Returns the positive, real cube super root of n.'''
    value = fmul( 2, log( n ) )
    return sqrt( fdiv( value, lambertw( value ) ) )


#******************************************************************************
#
#  getSuperRootOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), IntValidator( 1 ) ] )
def getSuperRootOperator( n, k ):
    '''Returns the positive, real kth super root of n.'''
    k = fsub( k, 1 )
    value = fmul( k, log( n ) )
    return root( fdiv( value, lambertw( value ) ), k )


#******************************************************************************
#
#  getSuperRootsOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), IntValidator( 1 ) ] )
def getSuperRootsOperator( n, k ):
    '''Returns all the super-roots of n, not just the nice, positive, real one.'''
    k = fsub( k, 1 )
    factors = [ fmul( i, root( k, k ) ) for i in unitroots( int( k ) ) ]
    base = root( fdiv( log( n ), lambertw( fmul( k, log( n ) ) ) ), k )

    return [ fmul( i, base ) for i in factors ]


#******************************************************************************
#
#  getReciprocalOperator
#
#  We used to be able to call fdiv directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getReciprocalOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.invert( invertValue=False )
    else:
        return fdiv( 1, n )


#******************************************************************************
#
#  getAbsoluteValueOperator
#
#  We used to be able to call fabs directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getAbsoluteValueOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fabs( n.value ), n.units )
    else:
        return fabs( n )


#******************************************************************************
#
#  getNearestIntOperator
#
#  We used to be able to call fdiv directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getNearestIntOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( nint( n.value ), n.units )
    else:
        return nint( n )


#******************************************************************************
#
#  tetrateOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), IntValidator( 0 ) ] )
def tetrateOperator( i, j ):
    '''
    This is the smaller (left-associative) version of the hyper4 operator.

    This function forces the second argument to an integer and runs in O( n )
    time based on the second argument.
    '''
    result = i

    for _ in arange( 1, j ):
        result = power( result, i )

    return result


#******************************************************************************
#
#  tetrateRightOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), IntValidator( 0 ) ] )
def tetrateRightOperator( i, j ):
    '''
    This is the larger, right-associative version of the hyper4 operator.

    This function forces the second argument to an integer and runs in O( n )
    time based on the second argument.
    '''
    result = i

    for _ in arange( 1, j ):
        result = power( i, result )

    return result


#******************************************************************************
#
#  isDivisibleOperator
#
#  Is n divisible by k?
#
#******************************************************************************

def isDivisible( n, k ):
    if n == 0:
        return 1

    return 1 if ( n >= k ) and ( fmod( n, k ) == 0 ) else 0

@twoArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ ComplexOrMeasurementValidator( ),  ComplexOrMeasurementValidator( ) ] )
def isDivisibleOperator( n, k ):
    return isDivisible( n, k )


#******************************************************************************
#
#  isSquareOperator
#
#  The "smarter" algorithm is slower... WHY?!
#
#******************************************************************************

#TODO: handle measurements
def isSquare( n ):
    #mod = fmod( n, 16 )

    #if mod in [ 0, 1, 4, 9 ]:
    sqrtN = sqrt( n )
    return 1 if sqrtN == floor( sqrtN ) else 0
    #else:
    #    return 0


@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def isSquareOperator( n ):
    return isSquare( n )


#******************************************************************************
#
#  isPowerOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def isPowerOperator( n, k ):
    #print( 'log( n )', log( n ) )
    #print( 'log( k )', log( k ) )
    #print( 'divide', autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )
    return isInteger( autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )


#******************************************************************************
#
#  isKthPowerOperator
#
#******************************************************************************

def isKthPower( n, k ):
    if not isint( k, gaussian=True ):
        raise ValueError( 'integer argument expected' )

    if k == 1:
        return 1

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

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), IntValidator( 1 ) ] )
def isKthPowerOperator( n, k ):
    return isKthPower( n, k )


#******************************************************************************
#
#  performTrigOperation
#
#******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, RPNMeasurement ):
        value = mpf( i.convertValue( RPNMeasurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acosOperator( n ):
    return performTrigOperation( n, acos )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acoshOperator( n ):
    return performTrigOperation( n, acosh )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acotOperator( n ):
    return performTrigOperation( n, acot )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acothOperator( n ):
    return performTrigOperation( n, acoth )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acscOperator( n ):
    return performTrigOperation( n, acsc )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def acschOperator( n ):
    return performTrigOperation( n, acsch )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def asecOperator( n ):
    return performTrigOperation( n, asec )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def asechOperator( n ):
    return performTrigOperation( n, asech )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def asinOperator( n ):
    return performTrigOperation( n, asin )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def asinhOperator( n ):
    return performTrigOperation( n, asinh )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def atanOperator( n ):
    return performTrigOperation( n, atan )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def atanhOperator( n ):
    return performTrigOperation( n, atanh )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cosOperator( n ):
    return performTrigOperation( n, cos )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def coshOperator( n ):
    return performTrigOperation( n, cosh )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cotOperator( n ):
    return performTrigOperation( n, cot )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cothOperator( n ):
    return performTrigOperation( n, coth )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cscOperator( n ):
    return performTrigOperation( n, csc )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cschOperator( n ):
    return performTrigOperation( n, csch )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def secOperator( n ):
    return performTrigOperation( n, sec )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def sechOperator( n ):
    return performTrigOperation( n, sech )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def sinOperator( n ):
    return performTrigOperation( n, sin )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def sinhOperator( n ):
    return performTrigOperation( n, sinh )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def tanOperator( n ):
    return performTrigOperation( n, tan )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def tanhOperator( n ):
    return performTrigOperation( n, tanh )


#******************************************************************************
#
#  isEqualOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isEqual( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isEqual( k ) else 0
    else:
        if isinstance( n, RPNMeasurement ):
            return 1 if k.isEqual( n ) else 0
        else:
            return 1 if n == k else 0

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isEqualOperator( n, k ):
    return isEqual( n, k )


#******************************************************************************
#
#  isNotEqualOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotEqualOperator( n, k ):
    return 0 if isEqual( n, k ) else 1


#******************************************************************************
#
#  isGreaterOperator
#
#******************************************************************************

def isGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isLarger( k ) else 0
    else:
        return 1 if n > k else 0

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isGreaterOperator( n, k ):
    return isGreater( n, k )


#******************************************************************************
#
#  isLessOperator
#
#******************************************************************************

def isLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isSmaller( k ) else 0
    else:
        return 1 if n < k else 0

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isLessOperator( n, k ):
    return isLess( n, k )


#******************************************************************************
#
#  isNotGreaterOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotGreaterOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotLarger( k ) else 0
    else:
        return 1 if n <= k else 0


#******************************************************************************
#
#  isNotLessOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotLessOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotSmaller( k ) else 0
    else:
        return 1 if n >= k else 0


#******************************************************************************
#
#  isIntegerOperator
#
#******************************************************************************

def isInteger( n ):
    return 1 if fmod( n, 1 ) == 0 else 0

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ) ] )
def isIntegerOperator( n ):
    return isInteger( n )


#******************************************************************************
#
#  roundOffOperator
#
#******************************************************************************

def roundOff( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundOff( n.value ), n.units )
    else:
        return floor( fadd( n, 0.5 ) )

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ) ] )
def roundOffOperator( n ):
    return roundOff( n )


#******************************************************************************
#
#  roundByValueOperator
#
#******************************************************************************

def roundByValue( n, value ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundByValue( n.value, value ), n.units )
    else:
        return fmul( floor( fdiv( fadd( n, fdiv( value, 2 ) ), value ) ), value )

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealValidator( ) ] )
def roundByValueOperator( n, value ):
    return roundByValue( n, value )


#******************************************************************************
#
#  roundByDigitsOperator
#
#******************************************************************************

def roundByDigits( n, digits ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundByDigits( n.value, digits ), n.units )
    else:
        return roundByValue( n, power( 10, digits ) )

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), IntValidator( ) ] )
def roundByDigitsOperator( n, digits ):
    return roundByDigits( n, digits )


#******************************************************************************
#
#  getLargerOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getLargerOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isGreater( n, k ) else k

    return n if n > k else k


#******************************************************************************
#
#  getSmallerOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getSmallerOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isLess( n, k ) else k

    return n if n < k else k


#******************************************************************************
#
#  getFloorOperator
#
#******************************************************************************

def getFloor( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getFloor( n.value ), n.units )
    else:
        return floor( n )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getFloorOperator( n ):
    return getFloor( n )


#******************************************************************************
#
#  getCeilingOperator
#
#******************************************************************************

def getCeiling( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getCeiling( n.value ), n.units )
    else:
        return ceil( n )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getCeilingOperator( n ):
    return getCeiling( n )


#******************************************************************************
#
#  getMaximumOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getMaximumOperator( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ max( arg ) for arg in n ]
    else:
        return max( n )


#******************************************************************************
#
#  getMinimumOperator
#
#******************************************************************************

@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def getMinimumOperator( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ min( arg ) for arg in n ]
    else:
        return min( n )


#******************************************************************************
#
#  isEvenOperator
#
#******************************************************************************

def isEven( n ):
    return 1 if fmod( n, 2 ) == 0 else 0

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def isEvenOperator( n ):
    return isEven( n )


#******************************************************************************
#
#  isOddOperator
#
#******************************************************************************

def isOdd( n ):
    return 1 if fmod( n, 2 ) == 1 else 0

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def isOddOperator( n ):
    return isOdd( n )


#******************************************************************************
#
#  isNotZeroOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def isNotZeroOperator( n ):
    return 0 if n == 0 else 1


#******************************************************************************
#
#  isZeroOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def isZeroOperator( n ):
    return 1 if n == 0 else 0


#******************************************************************************
#
#  getMantissaOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ RealValidator( ) ] )
def getMantissaOperator( n ):
    return fmod( fabs( n ), 1 )


#******************************************************************************
#
#  getModuloOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getModuloOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getModulo( k )
    elif isinstance( k, RPNMeasurement ):
        raise ValueError( 'cannot take a non-measurement modulo a measurement' )
    else:
        return fmod( n, k )


#******************************************************************************
#
#  getAGMOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getAGMOperator( n, k ):
    return agm( n, k )


#******************************************************************************
#
#  getExpOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getExpOperator( n ):
    return exp( n )


#******************************************************************************
#
#  getExp10Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getExp10Operator( n ):
    return power( 10, n )


#******************************************************************************
#
#  getExpPhiOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getExpPhiOperator( n ):
    return power( phi, n )


#******************************************************************************
#
#  getArgumentOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getArgumentOperator( n ):
    return arg( n )


#******************************************************************************
#
#  getConjugateOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getConjugateOperator( n ):
    return conj( n )


#******************************************************************************
#
#  getImaginaryOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getImaginaryOperator( n ):
    return im( n )


#******************************************************************************
#
#  getRealOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getRealOperator( n ):
    return re( n )


#******************************************************************************
#
#  getLambertWOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getLambertWOperator( n ):
    return lambertw( n )


#******************************************************************************
#
#  getLIOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getLIOperator( n ):
    return li( n )


#******************************************************************************
#
#  getLogOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getLogOperator( n ):
    return ln( n )


#******************************************************************************
#
#  getLog10Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getLog10Operator( n ):
    return log10( n )


#******************************************************************************
#
#  getLog2Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getLog2Operator( n ):
    return log( n, 2 )


#******************************************************************************
#
#  getLogXYOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getLogXYOperator( n, k ):
    return log( n, k )


#******************************************************************************
#
#  getPolyexpOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getPolyexpOperator( n, k ):
    return polyexp( n, k )


#******************************************************************************
#
#  getPolylogOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexOrMeasurementValidator( ) ] )
def getPolylogOperator( n, k ):
    return polylog( n, k )


#******************************************************************************
#
#  calculateHypotenuseOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( 0 ), RealValidator( 0 ) ] )
def calculateHypotenuseOperator( n, k ):
    return hypot( n, k )


#******************************************************************************
#
#  calculateNthHyperoperatorOperator
#
#******************************************************************************

class HyperopLeft( hyperop ):
    def __call__( self, a, b ):
        '''
        Evaluate and return expression H[n](a,b).
        (a,b) must be non-negative for n>4.
        '''
        check = self._check_value( a, b )

        if check is not None:
            return check

        # Apply fold
        #return reduce( lambda x, y: self.lower( x, y ), self._repeat( a, b ) )
        return reduce( self.lower, self._repeat( a, b ) )

@argValidator( [ IntValidator( 0 ), IntValidator( 0 ), IntValidator( 0 ) ] )
def calculateNthHyperoperatorOperator( a, b, c ):
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

    return HyperopLeft( a )( b, c )


#******************************************************************************
#
#  calculateNthRightHyperoperatorOperator
#
#******************************************************************************

@argValidator( [ IntValidator( 0 ), IntValidator( 0 ), IntValidator( 0 ) ] )
def calculateNthRightHyperoperatorOperator( a, b, c ):
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

