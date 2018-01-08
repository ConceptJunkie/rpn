#!/usr/bin/env python

# //******************************************************************************
# //
# //  miller_rabin.py
# //
# //  Adapted from https://github.com/smllmn/baillie-psw and converted to use
# //  mpmath.
# //
# //******************************************************************************

from mpmath import fadd, fdiv, fmod, fsub

#def miller_rabin_base_2( n ):
#    """Perform the Miller Rabin primality test base 2"""
#    d = fsub( n, 1 )
#    s = 0
#
#    while fmod( d, 2 ) == 0:
#        d = fdiv( d, 2 )
#        s += 1
#
#    nInt = int( n )
#
#    x = pow( 2, int( d ), nInt )
#
#    nMinus1 = fsub( n, 1 )
#
#    if x == 1 or x == nMinus1:
#        return True
#
#    for i in range( s - 1 ):
#        x = pow( x, 2, nInt )
#
#        if x == 1:
#            return False
#        elif x == nMinus1:
#            return True
#
#    return False

def miller_rabin_base_2( n ):
    n = int( n )

    """Perform the Miller Rabin primality test base 2"""
    d = n - 1
    s = 0

    while not d & 1:    # Check for divisibility by 2
        d = d >> 1      # Divide by 2 using a binary right shift
        s += 1

    x = pow( 2, d, n )

    if x == 1 or x == n - 1:
        return True

    for i in range( s - 1 ):
        x = pow( x, 2, n )

        if x == 1:
            return False
        elif x == n - 1:
            return True

    return False


