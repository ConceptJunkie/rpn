#!/usr/bin/env python

#******************************************************************************
#
#  rpnMath.py
#
#  rpnChilada mathematical operators
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from functools import reduce

from hyperop import hyperop

from mpmath import acos, acosh, acot, acoth, acsc, acsch, agm, arange, arg,  asec, asech, asin, \
                   asinh, atan, atanh, autoprec, ceil, conj, cos, cosh, cot, coth, csc, csch, e, \
                   exp, fabs, fadd, fdiv, floor, fmod, fmul, fneg, fsub, hypot, im, isint, \
                   lambertw, li, ln, log, log10, mpf, nint, phi, polyexp, polylog, power, re, \
                   root, sec, sech, sign, sin, sinh, sqrt, tan, tanh, unitroots

from rpn.math.rpnSimpleMath import isDivisible, isEven, isKthPower, isOdd, isSquare, roundNumberByValue

from rpn.time.rpnDateTime import RPNDateTime

from rpn.units.rpnMeasurementClass import RPNMeasurement

from rpn.util.rpnGenerator import RPNGenerator
from rpn.util.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator, listArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, AdditiveValidator, ComparableValidator, IntValidator, \
                             ListValidator, MultiplicativeValidator, RealValidator, RealOrMeasurementValidator


#******************************************************************************
#
#  add
#
#  We used to be able to call fadd directly, but now we want to be able to add
#  units.  Adding units includes an implicit conversion if the units are not
#  the same, assuming they are compatible.
#
#******************************************************************************

def add( n, k ):
    if isinstance( n, RPNDateTime ) and isinstance( k, RPNMeasurement ):
        return n.add( k )

    if isinstance( n, RPNMeasurement ) and isinstance( k, RPNDateTime ):
        return k.add( n )

    if isinstance( n, RPNMeasurement ):
        return n.add( k )

    if isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).add( k )

    return fadd( n, k )


@twoArgFunctionEvaluator( )
# note, a date-time can be added to, but it cannot itself be added
@argValidator( [ AdditiveValidator( ), MultiplicativeValidator( ) ] )
def addOperator( n, k ):
    return add( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ AdditiveValidator( ) ] )
def incrementOperator( n ):
    return add( n, 1 )


#******************************************************************************
#
#  subtract
#
#  We used to be able to call fsub directly, but now we want to be able to
#  subtract units and do the appropriate conversions.
#
#******************************************************************************

def subtract( n, k ):
    if isinstance( n, RPNDateTime ):
        return n.subtract( k )

    if isinstance( n, RPNMeasurement ):
        if isinstance( k, RPNDateTime ):
            return k.subtract( n )

        return n.subtract( k )

    if isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).subtract( k )

    return fsub( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ AdditiveValidator( ), AdditiveValidator( ) ] )
def subtractOperator( n, k ):
    return subtract( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ AdditiveValidator( ) ] )
def decrementOperator( n ):
    return subtract( n, 1 )


#******************************************************************************
#
#  getNegativeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getNegativeOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fneg( n.value ), n.units )

    return fneg( n )


#******************************************************************************
#
#  getSignOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getSignOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return sign( n.value )

    return sign( n )


#******************************************************************************
#
#  getValueOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getValueOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.value

    return n


#******************************************************************************
#
#  divide
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

    if isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).divide( k )

    return fdiv( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def divideOperator( n, k ):
    return divide( n, k )


#******************************************************************************
#
#  multiply
#
#  We used to be able to call fmul directly, but now we want to also multiply
#  the units.  This allows compound units and the conversion routines try to
#  be smart enough to deal with this.
#
#******************************************************************************

def multiply( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.multiply( k )

    if isinstance( k, RPNMeasurement ):
        return RPNMeasurement( n ).multiply( k )

    return fmul( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def multiplyOperator( n, k ):
    return multiply( n, k )


#******************************************************************************
#
#  getPower
#
#******************************************************************************

def getPower( n, k ):
    if isinstance( n, RPNMeasurement ):
        result = RPNMeasurement( n )
        return result.exponentiate( k )

    return power( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def getPowerOperator( n, k ):
    return getPower( n, k )


def square( n ):
    return getPower( n, 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def squareOperator( n ):
    return getPower( n, 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cubeOperator( n ):
    return getPower( n, 3 )


#******************************************************************************
#
#  getRoot
#
#******************************************************************************

def getRoot( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getRoot( k )

    if not isint( k ):
        return power( n, fdiv( 1, k ) )

    return root( n, k )


@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def getRootOperator( n, k ):
    return getRoot( n, k )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getSquareRootOperator( n ):
    return getRoot( n, 2 )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getCubeRootOperator( n ):
    return getRoot( n, 3 )


#******************************************************************************
#
#  getReciprocalOperator
#
#  We used to be able to call fdiv directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getReciprocalOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return n.invert( invertValue=False )

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
@argValidator( [ MultiplicativeValidator( ) ] )
def getAbsoluteValueOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fabs( n.value ), n.units )

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
@argValidator( [ MultiplicativeValidator( ) ] )
def getNearestIntOperator( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( nint( n.value ), n.units )

    return nint( n )


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
@argValidator( [ MultiplicativeValidator( ) ] )
def acosOperator( n ):
    return performTrigOperation( n, acos )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def acoshOperator( n ):
    return performTrigOperation( n, acosh )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def acotOperator( n ):
    return performTrigOperation( n, acot )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def acothOperator( n ):
    return performTrigOperation( n, acoth )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def acscOperator( n ):
    return performTrigOperation( n, acsc )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def acschOperator( n ):
    return performTrigOperation( n, acsch )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def asecOperator( n ):
    return performTrigOperation( n, asec )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def asechOperator( n ):
    return performTrigOperation( n, asech )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def asinOperator( n ):
    return performTrigOperation( n, asin )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def asinhOperator( n ):
    return performTrigOperation( n, asinh )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def atanOperator( n ):
    return performTrigOperation( n, atan )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def atanhOperator( n ):
    return performTrigOperation( n, atanh )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cosOperator( n ):
    return performTrigOperation( n, cos )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def coshOperator( n ):
    return performTrigOperation( n, cosh )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cotOperator( n ):
    return performTrigOperation( n, cot )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cothOperator( n ):
    return performTrigOperation( n, coth )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cscOperator( n ):
    return performTrigOperation( n, csc )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def cschOperator( n ):
    return performTrigOperation( n, csch )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def secOperator( n ):
    return performTrigOperation( n, sec )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def sechOperator( n ):
    return performTrigOperation( n, sech )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def sinOperator( n ):
    return performTrigOperation( n, sin )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def sinhOperator( n ):
    return performTrigOperation( n, sinh )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def tanOperator( n ):
    return performTrigOperation( n, tan )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def tanhOperator( n ):
    return performTrigOperation( n, tanh )


#******************************************************************************
#
#  isEqual
#
#******************************************************************************

def isEqual( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isEqual( k ) else 0

    if isinstance( n, RPNMeasurement ):
        return 1 if k.isEqual( n ) else 0

    return 1 if n == k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isEqualOperator( n, k ):
    return isEqual( n, k )


#******************************************************************************
#
#  isNotEqualOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isNotEqualOperator( n, k ):
    return 0 if isEqual( n, k ) else 1


#******************************************************************************
#
#  isGreater
#
#******************************************************************************

def isGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isLarger( k ) else 0

    return 1 if n > k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isGreaterOperator( n, k ):
    return isGreater( n, k )


#******************************************************************************
#
#  isLess
#
#******************************************************************************

def isLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isSmaller( k ) else 0

    return 1 if n < k else 0


@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isLessOperator( n, k ):
    return isLess( n, k )


#******************************************************************************
#
#  isNotGreaterOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isNotGreaterOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotLarger( k ) else 0

    return 1 if n <= k else 0


#******************************************************************************
#
#  isNotLessOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def isNotLessOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotSmaller( k ) else 0

    return 1 if n >= k else 0


#******************************************************************************
#
#  isInteger
#
#******************************************************************************

def isInteger( n ):
    if isinstance( n, RPNMeasurement ):
        return isInteger( n.value )

    return 1 if fmod( n, 1 ) == 0 else 0


@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ) ] )
def isIntegerOperator( n ):
    return isInteger( n )


#******************************************************************************
#
#  roundOff
#
#******************************************************************************

def roundOff( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundOff( n.value ), n.units )

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
        return RPNMeasurement( roundNumberByValue( n.value, value ), n.units )

    return roundNumberByValue( n, value )


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

    return roundNumberByValue( n, power( 10, digits ) )


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
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
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
@argValidator( [ ComparableValidator( ), ComparableValidator( ) ] )
def getSmallerOperator( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isLess( n, k ) else k

    return n if n < k else k


#******************************************************************************
#
#  getFloor
#
#******************************************************************************

def getFloor( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getFloor( n.value ), n.units )

    return floor( n )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getFloorOperator( n ):
    return getFloor( n )


#******************************************************************************
#
#  getCeiling
#
#******************************************************************************

def getCeiling( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getCeiling( n.value ), n.units )

    return ceil( n )


@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
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

    return min( n )


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

    if isinstance( k, RPNMeasurement ):
        raise ValueError( 'cannot take a non-measurement modulo a measurement' )

    return fmod( n, k )

#******************************************************************************
#
#  getSquareSuperRootOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getSquareSuperRootOperator( n ):
    '''Returns the positive, real square super root of n.'''
    return power( e, lambertw( log( n ) ) )


#******************************************************************************
#
#  getCubeSuperRootOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
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
@argValidator( [ MultiplicativeValidator( ), IntValidator( 1 ) ] )
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
@argValidator( [ MultiplicativeValidator( ), IntValidator( 1 ) ] )
def getSuperRootsOperator( n, k ):
    '''Returns all the super-roots of n, not just the nice, positive, real one.'''
    k = fsub( k, 1 )
    factors = [ fmul( i, root( k, k ) ) for i in unitroots( int( k ) ) ]
    base = root( fdiv( log( n ), lambertw( fmul( k, log( n ) ) ) ), k )

    return [ fmul( i, base ) for i in factors ]


#******************************************************************************
#
#  tetrateOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), IntValidator( 0 ) ] )
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
@argValidator( [ MultiplicativeValidator( ), IntValidator( 0 ) ] )
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

@twoArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
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

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def isSquareOperator( n ):
    return isSquare( n )


#******************************************************************************
#
#  isPowerOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
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

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), IntValidator( 1 ) ] )
def isKthPowerOperator( n, k ):
    return isKthPower( n, k )


#******************************************************************************
#
#  isEvenOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def isEvenOperator( n ):
    return isEven( n )


#******************************************************************************
#
#  isOddOperator
#
#******************************************************************************

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
@argValidator( [ MultiplicativeValidator( ) ] )
def isNotZeroOperator( n ):
    return 0 if n == 0 else 1


#******************************************************************************
#
#  isZeroOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
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
#  getAGMOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def getAGMOperator( n, k ):
    return agm( n, k )


#******************************************************************************
#
#  getExpOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getExpOperator( n ):
    return exp( n )


#******************************************************************************
#
#  getExp10Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getExp10Operator( n ):
    return power( 10, n )


#******************************************************************************
#
#  getExpPhiOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getExpPhiOperator( n ):
    return power( phi, n )


#******************************************************************************
#
#  getArgumentOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getArgumentOperator( n ):
    return arg( n )


#******************************************************************************
#
#  getConjugateOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getConjugateOperator( n ):
    return conj( n )


#******************************************************************************
#
#  getImaginaryOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getImaginaryOperator( n ):
    return im( n )


#******************************************************************************
#
#  getRealOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getRealOperator( n ):
    return re( n )


#******************************************************************************
#
#  getLambertWOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getLambertWOperator( n ):
    return lambertw( n )


#******************************************************************************
#
#  getLIOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getLIOperator( n ):
    return li( n )


#******************************************************************************
#
#  getLogOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getLogOperator( n ):
    return ln( n )


#******************************************************************************
#
#  getLog10Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getLog10Operator( n ):
    return log10( n )


#******************************************************************************
#
#  getLog2Operator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ) ] )
def getLog2Operator( n ):
    return log( n, 2 )


#******************************************************************************
#
#  getLogXYOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def getLogXYOperator( n, k ):
    return log( n, k )


#******************************************************************************
#
#  getPolyexpOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
def getPolyexpOperator( n, k ):
    return polyexp( n, k )


#******************************************************************************
#
#  getPolylogOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ MultiplicativeValidator( ), MultiplicativeValidator( ) ] )
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


@argValidator( [ IntValidator( 0 ), RealValidator( 0 ), IntValidator( 0 ) ] )
def calculateNthHyperoperatorOperator( a, b, c ):
    if a == 0:
        return c + 1

    if b == 0:
        if c == 1:
            return 0

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

        return 4

    if a > 4 and c > 2:
        raise ValueError( 'overflow' )

    if a > 4 and b > 4:
        raise ValueError( 'overflow' )

    return HyperopLeft( a )( b, c )


#******************************************************************************
#
#  calculateNthRightHyperoperatorOperator
#
#******************************************************************************

@argValidator( [ IntValidator( 0 ), RealValidator( 0 ), IntValidator( 0 ) ] )
def calculateNthRightHyperoperatorOperator( a, b, c ):
    if a == 0:
        return c + 1

    if b == 0:
        if c == 1:
            return 0

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

        return 4

    if a > 4 and c > 2:
        raise ValueError( 'overflow' )

    if a > 4 and b > 5:
        raise ValueError( 'overflow' )

    return hyperop( a )( b, c )


@argValidator( [ IntValidator( ), IntValidator( ), IntValidator( 1 ) ] )
def getPowModOperator( a, b, c ):
    return pow( int( a ), int( b ), int( c ) )


#******************************************************************************
#
#  getPowModOperatorNew
#
#******************************************************************************

@argValidator( [ IntValidator( ), IntValidator( ), IntValidator( 1 ) ] )
def getPowModOperatorNew( a, b, c ):
    return getPowMod( a, b, c )
