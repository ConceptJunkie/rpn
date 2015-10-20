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
# //  compareResults
# //
# //  Does nothing if the results compare successfully, otherwise raises an
# //  expection.
# //
# //******************************************************************************

def compareResults( result1, result2 ):
    if isinstance( result1, list ) != isinstance( result2, list ):
        print( '**** error in results comparison' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
        raise ValueError( 'one result is a list, the other isn\'t' )

    if isinstance( result1, str ) != isinstance( result2, str ):
        print( '**** error in results comparison' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
        raise ValueError( 'one result is a string, the other isn\'t' )

    if isinstance( result1, str ) and isinstance( result2, str ):
        if result1 != result2:
            print( type( result1[ i ] ), type( result2[ i ] ) )
            print( result1[ i ], result2[ i ], 'are not equal' )
            print( 'difference found at index', i )
            raise ValueError( 'unit test failed' )
        else:
            return

    if isinstance( result1, list ) and isinstance( result2, list ):
        if len( result1 ) != len( result2 ):
            raise ValueError( 'lists are not of equal length:', len( result1 ), len( result2 ) )

        for i in range( 0, len( result1 ) ):
            if not almosteq( result1[ i ], result2[ i ] ):
                print( type( result1[ i ] ), type( result2[ i ] ) )
                print( result1[ i ], result2[ i ], 'are not equal' )
                print( 'difference found at index', i )
                raise ValueError( 'unit test failed' )
    elif not almosteq( result1, result2 ):
        print( '**** error in results comparison' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
        raise ValueError( 'unit test failed' )


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

    compareResults( result1, result2 )

    print( 'both are equal!' )
    print( )


# //******************************************************************************
# //
# //  areListsEquivalent
# //
# //******************************************************************************

def areListsEquivalent( list1, list2 ):
    if len( list1 ) != len( list2 ):
        raise ValueError( 'lists are not of equal length:', len( list1 ), len( list2 ) )

    temp2 = list( list2 )   # make a mutable copy

    try:
        for elem in list1:
            for elem2 in temp2:
                if almosteq( elem, elem2 ):
                    temp2.remove( elem2 )
                    break
    except ValueError:
        print( 'catch', elem, temp2 )
        return False

    return not temp2


# //******************************************************************************
# //
# //  expectEquivalent
# //
# //******************************************************************************

def expectEquivalent( command1, command2 ):
    print( 'rpn', command1 )
    print( 'rpn', command2 )

    result1 = rpn( shlex.split( command1 ) )[ 0 ]
    result2 = rpn( shlex.split( command2 ) )[ 0 ]

    if isinstance( result1, list ) != isinstance( result2, list ):
        print( '**** error in results comparison' )
        print( '    result 1: ', result1 )
        print( '    result 2: ', result2 )
        raise ValueError( 'one result is a list, the other isn\'t' )

    if not areListsEquivalent( result1, result2 ):
        print( '**** error in results comparison' )
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

    print( 'operator works' )
    print( )


# //******************************************************************************
# //
# //  expectResult
# //
# //******************************************************************************

def expectResult( command, expected ):
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

    compareResults( result, compare )

    print( 'test passed!' )
    print( )


