#!/usr/bin/env python

# //******************************************************************************
# //
# //  lucas_pp.py
# //
# //  Adapted from https://github.com/smllmn/baillie-psw and converted to use
# //  mpmath.
# //
# //******************************************************************************

def U_V_subscript( k, n, U, V, P, Q, D ):
    k, n, U, V, P, Q, D = map( int, ( k, n, U, V, P, Q, D ) )
    digits = list( map( int, str( bin( k ) )[ 2: ] ) )
    subscript = 1

    for digit in digits[ 1: ]:
        U, V = U * V % n, ( pow( V, 2, n ) - 2 * pow( Q, subscript, n ) ) % n
        subscript *= 2

        if digit == 1:
            if not ( P * U + V ) & 1:
                if not ( D * U + P *V ) & 1:
                    U, V = ( P * U + V ) >> 1, ( D * U + P * V ) >> 1
                else:
                    U, V = ( P * U + V ) >> 1, ( D * U + P * V + n ) >> 1
            elif not ( D * U + P * V ) & 1:
                U, V = ( P * U + V + n ) >> 1, ( D * U +  P * V ) >> 1
            else:
                U, V = ( P * U + V + n ) >> 1, ( D * U + P * V + n ) >> 1

            subscript += 1
            U, V = U % n, V % n

    return U, V


def lucas_pp( n, D, P, Q ):
    n, D, P, Q = map( int, ( n, D, P, Q ) )

    """Perform the Lucas probable prime test"""
    U, V = U_V_subscript( n + 1, n, 1, P, P, Q, D )

    if U != 0:
        return False

    d = n + 1
    s = 0

    while not d & 1:
        d = d >> 1
        s += 1

    U, V = U_V_subscript( n + 1, n, 1, P, P, Q, D )

    if U == 0:
        return True

    for r in xrange(s):
        U, V = ( U * V ) % n, ( pow( V, 2, n ) - 2 * pow( Q, d * ( 2 ** r ), n ) ) % n

        if V == 0:
            return True

    return False


