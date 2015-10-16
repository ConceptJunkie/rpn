# //******************************************************************************
# //
# //  testRPN
# //
# //  main test script for RPN
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import shlex

from rpn import rpn, handleOutput

from mpmath import *


# //******************************************************************************
# //
# //  expectEqual
# //
# //******************************************************************************

def expectEqual( command1, command2 ):
    print( 'rpn', command1 )
    print( 'rpn', command2 )

    result1 = rpn( shlex.split( command1 ) )[ 0 ]
    result2 = rpn( shlex.split( command2 ) )[ 0 ]

    if isinstance( result1, list ) and isinstance( result2, list ):
        for i in range( 0, min( len( result1 ), len( result2 ) ) ):
            if not almosteq( result1[ i ], result2[ i ] ):
                print( type( result1[ i ] ), type( result2[ i ] ) )
                print( result1[ i ], result2[ i ], 'are not equal' )
                raise ValueError( 'unit test failed' )
    elif not almosteq( result1, result2 ):
        print( '**** error in equivalence test \'' + command1 + '\' and \'' + command2 + '\'' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
        raise ValueError( 'unit test failed' )

    print( 'both are equal!' )
    print( )


# //******************************************************************************
# //
# //  testOperator
# //
# //******************************************************************************

def testOperator( command ):
    print( 'rpn', command )
    result = rpn( shlex.split( command ) )

    if not result is None:
        handleOutput( result )

    print( )


# //******************************************************************************
# //
# //  expectRPN
# //
# //******************************************************************************

def expectRPN( command, expected ):
    print( 'rpn', command )
    result = rpn( shlex.split( command ) )[ 0 ]

    compare = None

    if isinstance( expected, list ):
        compare = [ ]

        for i in expected:
            if isinstance( i, int ) or isinstance( i, float ) or isinstance( i, complex ):
                compare.append( mpmathify( i ) )
            else:
                compare.append( i )
    else:
        if isinstance( expected, int ) or isinstance( expected, float ) or isinstance( expected, complex ):
            compare = mpmathify( expected )
        else:
            compare = expected

    if not result is None:
        if result == compare:
            print( result )
            print( 'passed!' )
        else:
            print( '**** error in test \'' + command + '\'' )
            print( '    expected: ', expected )
            print( '    but got: ', result )

            raise ValueError( 'unit test failed' )

    print( )


