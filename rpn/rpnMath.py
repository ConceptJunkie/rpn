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
from rpn.rpnUtils import oneArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, ComplexValidator, ComplexOrMeasurementValidator, \
                             ComplexOrMeasurementOrDateTimeValidator, DefaultValidator, \
                             IntValidator, RealValidator, RealOrMeasurementValidator, \
                             RealOrMeasurementOrDateTimeValidator


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
def increment( n ):
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
def decrement( n ):
    return subtract( n, 1 )


#******************************************************************************
#
#  getNegative
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getNegative( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fneg( n.value ), n.units )
    else:
        return fneg( n )


#******************************************************************************
#
#  getSign
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getSign( n ):
    if isinstance( n, RPNMeasurement ):
        return sign( n.value )
    else:
        return sign( n )


#******************************************************************************
#
#  getValue
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getValue( n ):
    if isinstance( n, RPNMeasurement ):
        return n.value
    else:
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
#  getPower
#
#******************************************************************************

def getPower( n, k ):
    if isinstance( n, RPNMeasurement ):
        result = RPNMeasurement( n )
        return result.exponentiate( k )
    else:
        return power( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexValidator( ) ] )
def getPowerOperator( n, k ):
    return getPower( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def square( n ):
    return getPower( n, 2 )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def cube( n ):
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
    else:
        return root( n, k )

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ), ComplexValidator( ) ] )
def getRootOperator( n, k ):
    return getRoot( n, k )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getSquareRoot( n ):
    return getRoot( n, 2 )

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getCubeRoot( n ):
    return getRoot( n, 3 )


#******************************************************************************
#
#  getSquareSuperRoot
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getSquareSuperRoot( n ):
    '''Returns the positive, real square super root of n.'''
    return power( e, lambertw( log( n ) ) )


#******************************************************************************
#
#  getCubeSuperRoot
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ) ] )
def getCubeSuperRoot( n ):
    '''Returns the positive, real cube super root of n.'''
    value = fmul( 2, log( n ) )
    return sqrt( fdiv( value, lambertw( value ) ) )


#******************************************************************************
#
#  getSuperRoot
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 1 ) ] )
def getSuperRoot( n, k ):
    '''Returns the positive, real kth super root of n.'''
    k = fsub( k, 1 )
    value = fmul( k, log( n ) )
    return root( fdiv( value, lambertw( value ) ), k )


#******************************************************************************
#
#  getSuperRoots
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 1 ) ] )
def getSuperRoots( n, k ):
    '''Returns all the super-roots of n, not just the nice, positive, real one.'''
    k = fsub( k, 1 )
    factors = [ fmul( i, root( k, k ) ) for i in unitroots( int( k ) ) ]
    base = root( fdiv( log( n ), lambertw( fmul( k, log( n ) ) ) ), k )

    return [ fmul( i, base ) for i in factors ]


#******************************************************************************
#
#  getReciprocal
#
#  We used to be able to call fdiv directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getReciprocal( n ):
    if isinstance( n, RPNMeasurement ):
        return n.invert( invertValue=False )
    else:
        return fdiv( 1, n )


#******************************************************************************
#
#  getAbsoluteValue
#
#  We used to be able to call fabs directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getAbsoluteValue( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( fabs( n.value ), n.units )
    else:
        return fabs( n )


#******************************************************************************
#
#  getNearestInt
#
#  We used to be able to call fdiv directly, but now we want to handle
#  RPNMeasurements.
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getNearestInt( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( nint( n.value ), n.units )
    else:
        return nint( n )


#******************************************************************************
#
#  tetrate
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 0 ) ] )
def tetrate( i, j ):
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
#  tetrateRight
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 0 ) ] )
def tetrateRight( i, j ):
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
#  isDivisible
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
#  isSquare
#
#  The "smarter" algorithm is slower... WHY?!
#
#******************************************************************************

@oneArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def isSquare( n ):
    #mod = fmod( n, 16 )

    #if mod in [ 0, 1, 4, 9 ]:
    sqrtN = sqrt( n )
    return 1 if sqrtN == floor( sqrtN ) else 0
    #else:
    #    return 0


#******************************************************************************
#
#  isPower
#
#******************************************************************************

@twoArgFunctionEvaluator( )
#TODO: handle measurements
@argValidator( [ ComplexValidator( ), ComplexValidator( ) ] )
def isPower( n, k ):
    #print( 'log( n )', log( n ) )
    #print( 'log( k )', log( k ) )
    #print( 'divide', autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )
    return isInteger( autoprec( lambda n, k: fdiv( re( log( n ) ), re( log( k ) ) ) )( n, k ) )


#******************************************************************************
#
#  isKthPower
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ ComplexValidator( ), IntValidator( 1 ) ] )
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
def acosOperator( n ):
    return performTrigOperation( n, acos )

@oneArgFunctionEvaluator( )
def acoshOperator( n ):
    return performTrigOperation( n, acosh )

@oneArgFunctionEvaluator( )
def acotOperator( n ):
    return performTrigOperation( n, acot )

@oneArgFunctionEvaluator( )
def acothOperator( n ):
    return performTrigOperation( n, acoth )

@oneArgFunctionEvaluator( )
def acscOperator( n ):
    return performTrigOperation( n, acsc )

@oneArgFunctionEvaluator( )
def acschOperator( n ):
    return performTrigOperation( n, acsch )

@oneArgFunctionEvaluator( )
def asecOperator( n ):
    return performTrigOperation( n, asec )

@oneArgFunctionEvaluator( )
def asechOperator( n ):
    return performTrigOperation( n, asech )

@oneArgFunctionEvaluator( )
def asinOperator( n ):
    return performTrigOperation( n, asin )

@oneArgFunctionEvaluator( )
def asinhOperator( n ):
    return performTrigOperation( n, asinh )

@oneArgFunctionEvaluator( )
def atanOperator( n ):
    return performTrigOperation( n, atan )

@oneArgFunctionEvaluator( )
def atanhOperator( n ):
    return performTrigOperation( n, atanh )

@oneArgFunctionEvaluator( )
def cosOperator( n ):
    return performTrigOperation( n, cos )

@oneArgFunctionEvaluator( )
def coshOperator( n ):
    return performTrigOperation( n, cosh )

@oneArgFunctionEvaluator( )
def cotOperator( n ):
    return performTrigOperation( n, cot )

@oneArgFunctionEvaluator( )
def cothOperator( n ):
    return performTrigOperation( n, coth )

@oneArgFunctionEvaluator( )
def cscOperator( n ):
    return performTrigOperation( n, csc )

@oneArgFunctionEvaluator( )
def cschOperator( n ):
    return performTrigOperation( n, csch )

@oneArgFunctionEvaluator( )
def secOperator( n ):
    return performTrigOperation( n, sec )

@oneArgFunctionEvaluator( )
def sechOperator( n ):
    return performTrigOperation( n, sech )

@oneArgFunctionEvaluator( )
def sinOperator( n ):
    return performTrigOperation( n, sin )

@oneArgFunctionEvaluator( )
def sinhOperator( n ):
    return performTrigOperation( n, sinh )

@oneArgFunctionEvaluator( )
def tanOperator( n ):
    return performTrigOperation( n, tan )

@oneArgFunctionEvaluator( )
def tanhOperator( n ):
    return performTrigOperation( n, tanh )


#******************************************************************************
#
#  isEqual
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


#******************************************************************************
#
#  isNotEqual
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotEqual( n, k ):
    return 0 if isEqual( n, k ) else 1


#******************************************************************************
#
#  isGreater
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isLarger( k ) else 0
    else:
        return 1 if n > k else 0


#******************************************************************************
#
#  isLess
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isSmaller( k ) else 0
    else:
        return 1 if n < k else 0


#******************************************************************************
#
#  isNotGreater
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotGreater( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotLarger( k ) else 0
    else:
        return 1 if n <= k else 0


#******************************************************************************
#
#  isNotLess
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def isNotLess( n, k ):
    if isinstance( n, RPNMeasurement ):
        return 1 if n.isNotSmaller( k ) else 0
    else:
        return 1 if n >= k else 0


#******************************************************************************
#
#  isInteger
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ) ] )
def isInteger( n ):
    return 1 if fmod( n, 1 ) == 0 else 0


#******************************************************************************
#
#  roundOff
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ) ] )
def roundOff( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundOff( n.value ), n.units )
    else:
        return floor( fadd( n, 0.5 ) )


#******************************************************************************
#
#  roundByValue
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
#  roundByDigits
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), IntValidator( ) ] )
def roundByDigits( n, digits ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( roundByDigits( n.value, digits ), n.units )
    else:
        return roundByValue( n, power( 10, digits ) )


#******************************************************************************
#
#  getLarger
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getLarger( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isGreater( n, k ) else k

    return n if n > k else k


#******************************************************************************
#
#  getSmaller
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getSmaller( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n if isLess( n, k ) else k

    return n if n < k else k


#******************************************************************************
#
#  getFloor
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getFloor( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getFloor( n.value ), n.units )
    else:
        return floor( n )


#******************************************************************************
#
#  getCeiling
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ ComplexOrMeasurementValidator( ) ] )
def getCeiling( n ):
    if isinstance( n, RPNMeasurement ):
        return RPNMeasurement( getCeiling( n.value ), n.units )
    else:
        return ceil( n )


#******************************************************************************
#
#  getMaximum
#
#******************************************************************************

def getMaximum( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ max( arg ) for arg in n ]
    else:
        return max( n )


#******************************************************************************
#
#  getMinimum
#
#******************************************************************************

def getMinimum( n ):
    if isinstance( n[ 0 ], ( list, RPNGenerator ) ):
        return [ min( arg ) for arg in n ]
    else:
        return min( n )


#******************************************************************************
#
#  isEven
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def isEven( n ):
    return 1 if fmod( n, 2 ) == 0 else 0


#******************************************************************************
#
#  isOdd
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def isOdd( n ):
    return 1 if fmod( n, 2 ) == 1 else 0


#******************************************************************************
#
#  isNotZero
#
#******************************************************************************

@oneArgFunctionEvaluator( )
#@argValidator( [ RealValidator( ) ] )
def isNotZero( n ):
    return 0 if n == 0 else 1


#******************************************************************************
#
#  isZero
#
#******************************************************************************

@oneArgFunctionEvaluator( )
#@argValidator( [ RealValidator( ) ] )
def isZero( n ):
    return 1 if n == 0 else 0


#******************************************************************************
#
#  getMantissa
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ RealValidator( ) ] )
def getMantissa( n ):
    return fmod( fabs( n ), 1 )


#******************************************************************************
#
#  getModulo
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealOrMeasurementValidator( ), RealOrMeasurementValidator( ) ] )
def getModulo( n, k ):
    if isinstance( n, RPNMeasurement ):
        return n.getModulo( k )
    elif isinstance( k, RPNMeasurement ):
        raise ValueError( 'cannot take a non-measurement modulo a measurement' )
    else:
        return fmod( n, k )


#******************************************************************************
#
#  getAGM
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getAGM( n, k ):
    return agm( n, k )


#******************************************************************************
#
#  getExp
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getExp( n ):
    return exp( n )


#******************************************************************************
#
#  getExp10
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getExp10( n ):
    return power( 10, n )


#******************************************************************************
#
#  getExpPhi
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getExpPhi( n ):
    return power( phi, n )


#******************************************************************************
#
#  getArgument
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getArgument( n ):
    return arg( n )


#******************************************************************************
#
#  getConjugate
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getConjugate( n ):
    return conj( n )


#******************************************************************************
#
#  getImaginary
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getImaginary( n ):
    return im( n )


#******************************************************************************
#
#  getReal
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getReal( n ):
    return re( n )


#******************************************************************************
#
#  getLambertW
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLambertW( n ):
    return lambertw( n )


#******************************************************************************
#
#  getLI
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLI( n ):
    return li( n )


#******************************************************************************
#
#  getLog
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLog( n ):
    return ln( n )


#******************************************************************************
#
#  getLog10
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLog10( n ):
    return log10( n )


#******************************************************************************
#
#  getLog2
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getLog2( n ):
    return log( n, 2 )


#******************************************************************************
#
#  getLogXY
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getLogXY( n, k ):
    return log( n, k )


#******************************************************************************
#
#  getPolyexp
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getPolyexp( n, k ):
    return polyexp( n, k )


#******************************************************************************
#
#  getPolylog
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def getPolylog( n, k ):
    return polylog( n, k )


#******************************************************************************
#
#  calculateHypotenuse
#
#******************************************************************************

@twoArgFunctionEvaluator( )
@argValidator( [ RealValidator( 0 ), RealValidator( 0 ) ] )
def calculateHypotenuse( n, k ):
    return hypot( n, k )


#******************************************************************************
#
#  calculateNthHyperoperator
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

    return HyperopLeft( a )( b, c )


#******************************************************************************
#
#  calculateNthRightHyperoperator
#
#******************************************************************************

@argValidator( [ IntValidator( 0 ), IntValidator( 0 ), IntValidator( 0 ) ] )
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

