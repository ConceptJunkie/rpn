#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnMath.py
#//
#//  RPN command-line calculator, mathematical operators
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

from mpmath import *

from rpnMeasurement import *


#//******************************************************************************
#//
#//  add
#//
#//  We used to be able to call fadd directly, but now we want to be able to add
#//  units.  Adding units includes an implicit conversion if the units are not
#//  the same.
#//
#//******************************************************************************

def add( n, k ):
    if isinstance( n, arrow.Arrow ) and isinstance( k, Measurement ):
        return addTimes( n, k )
    elif isinstance( n, Measurement ) and isinstance( k, arrow.Arrow ):
        return addTimes( k, n )
    elif isinstance( n, Measurement ):
        return n.add( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).add( k )
    else:
        return fadd( n, k )


#//******************************************************************************
#//
#//  subtract
#//
#//  We used to be able to call fsub directly, but now we want to be able to
#//  subtract units and do the appropriate conversions.
#//
#//******************************************************************************

def subtract( n, k ):
    if isinstance( n, arrow.Arrow ):
        if isinstance( k, Measurement ):
            return subtractTimes( n, k )
        elif isinstance( k, arrow.Arrow ):
            if n > k:
                delta = n - k
                factor = 1
            else:
                delta = k - n
                factor = -1

            if delta.days != 0:
                result = Measurement( delta.days * factor, 'day' )
                result = result.add( Measurement( delta.seconds * factor, 'second' ) )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            elif delta.seconds != 0:
                result = Measurement( delta.seconds * factor, 'second' )
                result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
            else:
                result = Measurement( delta.microseconds * factor, 'microsecond' )

            return result
        else:
            raise ValueError( 'cannot subtract incompatible types' )
    elif isinstance( n, Measurement ):
        if isinstance( k, arrow.Arrow ):
            return subtractTimes( k, n )
        elif isinstance( k, Measurement ):
            return Measurement( n ).subtract( k )
        else:
            return n.subtract( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).subtract( k )
    else:
        return fsub( n, k )


#//******************************************************************************
#//
#//  getNegative
#//
#//******************************************************************************

def getNegative( n ):
    if isinstance( n, Measurement ):
        return Measurement( fneg( n.getValue( ) ), n.getUnits( ) )
    else:
        return fneg( n )


#//******************************************************************************
#//
#//  divide
#//
#//  We used to be able to call fdiv directly, but now we want to also divide
#//  the units.  Doing so lets us do all kinds of great stuff because now we
#//  can support compound units without having to explicitly declare them in
#//  makeUnits.py.
#//
#//******************************************************************************

def divide( n, k ):
    if isinstance( n, Measurement ):
        return n.divide( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).divide( k )
    else:
        return fdiv( n, k )


#//******************************************************************************
#//
#//  multiply
#//
#//  We used to be able to call fmul directly, but now we want to also multiply
#//  the units.  This allows compound units and the conversion routines try to
#//  be smart enough to deal with this.
#//
#//******************************************************************************

def multiply( n, k ):
    if isinstance( n, Measurement ):
        return n.multiply( k )
    elif isinstance( k, Measurement ):
        return Measurement( n ).multiply( k )
    else:
        return fmul( n, k )


#//******************************************************************************
#//
#//  exponentiate
#//
#//******************************************************************************

def exponentiate( n, k ):
    if isinstance( n, Measurement ):
        return n.exponentiate( k )
    elif isinstance( k, Measurement ):
        raise ValueError( 'a measurement cannot be exponentiated (yet)' )
    else:
        return power( n, k )


#//******************************************************************************
#//
#//  takeReciprocal
#//
#//  We used to be able to call fdiv directly, but now we want to handle
#//  Measurements.
#//
#//******************************************************************************

def takeReciprocal( n ):
    if isinstance( n, Measurement ):
        return n.invert( )
    else:
        return fdiv( 1, n )


#//******************************************************************************
#//
#//  tetrate
#//
#//  This is the smaller (left-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrate( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( result, i )

    return result


#//******************************************************************************
#//
#//  tetrateLarge
#//
#//  This is the larger (right-associative) version of the hyper4 operator.
#//
#//  This function forces the second argument to an integer and runs at O( n )
#//  based on the second argument.
#//
#//******************************************************************************

def tetrateLarge( i, j ):
    result = i

    for x in arange( 1, j ):
        result = power( i, result )

    return result


#//******************************************************************************
#//
#//  isSquare
#//
#//******************************************************************************

def isSquare( n ):
    sqrtN = sqrt( n )

    return 1 if sqrtN == floor( sqrtN ) else 0


#//******************************************************************************
#//
#//  performTrigOperation
#//
#//******************************************************************************

def performTrigOperation( i, operation ):
    if isinstance( i, Measurement ):
        value = mpf( i.convertValue( Measurement( 1, { 'radian' : 1 } ) ) )
    else:
        value = i

    return operation( value )



