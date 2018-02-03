#!/usr/bin/env python

# //******************************************************************************
# //
# //  ballie_psw.py
# //
# //  Adapted from https://github.com/smllmn/baillie-psw and converted to use
# //  mpmath.
# //
# //******************************************************************************

from math import sqrt
from mpmath import fdiv, fmod, fsub, power

from rpn.rpnPrimes import primes
from rpn.rpnMath import isInteger, isSquare

from rpn.miller_rabin import miller_rabin_base_2
from rpn.jacobi_symbol import jacobi_symbol
from rpn.lucas_pp import lucas_pp


def D_chooser( candidate ):
    """Choose a D value suitable for the Baillie-PSW test"""
    D = 5

    while jacobi_symbol( D, candidate ) != -1:
        D += 2 if D > 0 else -2
        D *= -1

    return D


def baillie_psw( candidate ):
    """Perform the Baillie-PSW probabilistic primality test on candidate"""
    if candidate < 0:
        raise ValueError( "'is_prime' is not defined for negative numbers" )
    elif candidate == 1:
        return False
    elif not isInteger( candidate ):
        return False
    elif candidate in primes:
        return True

    # Check divisibility by a short list of primes less than 50
    for known_prime in [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 ]:
        if fmod( candidate, known_prime ) == 0:
            return False

    # Now perform the Miller-Rabin primality test base 2
    if not miller_rabin_base_2( candidate ):
        return False

    # Check that the number isn't a square number, as this will throw out
    # calculating the correct value of D later on (and means we have a
    # composite number)
    if isSquare( candidate ):
        return False

    # Finally perform the Lucas primality test
    D = D_chooser( int( candidate ) )

    if not lucas_pp( candidate, D, 1, fdiv( fsub( 1, D ), 4 ) ):
        return False

    # You've probably got a prime!
    return True

