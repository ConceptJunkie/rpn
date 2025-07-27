#!/usr/bin/env python

#******************************************************************************
#
#  rpnSimpleMath.py
#
#  rpnChilada mathematical functions that don't require dates or measurements.
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

from mpmath import arange, autoprec, fadd, fdiv, floor, fmod, fmul, im, isint, \
                   mpc, mpmathify, power, re, root, sqrt


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


#******************************************************************************
#
#  isSquare
#
#  The "smarter" algorithm is slower... WHY?!
#
#******************************************************************************

def isSquare( n ):
    #mod = fmod( n, 16 )

    #if mod in [ 0, 1, 4, 9 ]:
    sqrtN = sqrt( n )
    return 1 if sqrtN == floor( sqrtN ) else 0
    #else:
    #    return 0


#******************************************************************************
#
#  isKthPower
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

    rootN = autoprec( root )( n, k )
    return 1 if isint( rootN, gaussian=True ) else 0


#******************************************************************************
#
#  roundNumberByValue
#
#******************************************************************************

def roundNumberByValue( n, value ):
    return fmul( floor( fdiv( fadd( n, fdiv( value, 2 ) ), value ) ), value )


#******************************************************************************
#
#  roundNumberByDigits
#
#******************************************************************************

def roundNumberByDigits( n, digits ):
    return roundNumberByValue( n, power( 10, digits ) )


#******************************************************************************
#
#  roundImaginaryByDigits
#
#  The real and imaginary parts are rounded separately.
#
#******************************************************************************

def roundImaginaryByDigits( value, precision ):
    if fmod( re( value ), 1 ) == 0:
        value_re = re( value )
    else:
        value_re = roundNumberByDigits( re( value ), precision )

    if fmod( im( value ), 1 ) == 0:
        value_im = im( value )
    else:
        value_im = roundNumberByDigits( im( value ), precision )

    return mpmathify( mpc( real=value_re, imag=value_im ) )


#******************************************************************************
#
#  isEven
#
#******************************************************************************

def isEven( n ):
    return 1 if fmod( n, 2 ) == 0 else 0


#******************************************************************************
#
#  isOdd
#
#******************************************************************************

def isOdd( n ):
    return 1 if fmod( n, 2 ) == 1 else 0


#******************************************************************************
#
#  getPowMod
#
#******************************************************************************

def getPowMod( a, b, c ):
    '''
    Calculate (a ** y) % z efficiently.
    '''
    result = 1

    while b:
        if fmod( b, 2 ) == 1:
            result = fmod( fmul( result, a ), c )

        b = floor( fdiv( b, 2 ) )
        a = fmod( fmul( a, a ), c )

    return result
