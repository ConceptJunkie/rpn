#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnTestUtils.py
# //
# //  rpnChilada test utility functions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import shlex
import time

from rpn.rpn import rpn, handleOutput
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement

from mpmath import almosteq, fsub, isinf, mpf, mpmathify, log10, mp, nan, workdps

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  compareResults
# //
# //******************************************************************************

#import pysnooper
#@pysnooper.snoop( )
def compareResults( result1, result2 ):
    '''Compares two RPN expressions to make sure they produce the same result.
    Does nothing if the results compare successfully, otherwise raises an
    exception.'''

    if isinstance( result1, RPNGenerator ):
        return compareResults( list( result1.getGenerator( ) ), result2 )

    if isinstance( result2, RPNGenerator ):
        return compareResults( result1, list( result2.getGenerator( ) ) )

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
            print( '**** error in results comparison' )
            print( type( result1 ), type( result2 ) )
            print( result1, result2, 'are not equal' )
            raise ValueError( 'unit test failed' )
        else:
            return

    if isinstance( result1, RPNMeasurement ) and isinstance( result2, RPNMeasurement ):
        if result1 != result2:
            print( '**** error in results comparison' )
            print( type( result1 ), type( result2 ) )

            with workdps( 50 ):
                print( result1.value, result1.units, result2.value, result2.units, 'are not equal' )

            raise ValueError( 'unit test failed' )
        else:
            return True

    if isinstance( result1, list ) and isinstance( result2, list ):
        if len( result1 ) != len( result2 ):
            raise ValueError( 'lists are not of equal length:', len( result1 ), len( result2 ) )

        for i in range( 0, len( result1 ) ):
            if isinf( result1[ i ] ):
                if isinf( result2[ i ] ):
                    return True
                else:
                    print( '**** error in results comparison' )
                    print( type( result1[ i ] ), type( result2[ i ] ) )
                    print( result1[ i ], result2[ i ], 'are not equal' )

                    raise ValueError( 'unit test failed' )

            if not compareValues( result1[ i ], result2[ i ] ):
                digits = max( log10( result1[ i ] ), log10( result2[ i ] ) ) + 5

                mp.dps = digits

                print( '**** error in results comparison' )
                print( type( result1[ i ] ), type( result2[ i ] ) )
                print( result1[ i ], result2[ i ], 'are not equal' )
                print( 'difference', fsub( result1[ i ], result2[ i ] ) )
                print( 'difference found at index', i )

                raise ValueError( 'unit test failed' )
    else:
        if not compareValues( result1, result2 ):
            print( '**** error in results comparison' )
            print( '    result 1: ', result1 )
            print( '    result 2: ', result2 )

            raise ValueError( 'unit test failed' )


# //******************************************************************************
# //
# //  compareValues
# //
# //******************************************************************************

def compareValues( result1, result2 ):
    if isinstance( result1, RPNMeasurement ) != isinstance( result2, RPNMeasurement ):
        return False

    if isinstance( result1, RPNMeasurement ):
        return result1.__eq__( result2 )
    else:
        if isinf( result1 ):
            if isinf( result2 ):
                return True
            else:
                raise ValueError( 'unit test failed' )
                print( '**** error in results comparison' )
                print( type( result1 ), type( result2 ) )
                print( result1, result2, 'are not equal' )

        return almosteq( result1, result2 )


# //******************************************************************************
# //
# //  expectException
# //
# //******************************************************************************

def expectException( command ):
    if g.testFilter:
        if g.testFilter not in command:
            return

    print( 'rpn', command )

    result = rpn( shlex.split( command + ' -I' ) )

    if result == [ nan ]:
        print( 'exception test passed!' )
        print( '' )
        return True

    raise ValueError( 'exception was expected but didn\'t happen' )
    return False


# //******************************************************************************
# //
# //  expectEqual
# //
# //******************************************************************************

#@pysnooper.snoop( )
def expectEqual( command1, command2 ):
    if g.testFilter:
        if g.testFilter not in command1 and g.testFilter not in command2:
            return

    if g.timeIndividualTests:
        startTime = time.process_time( )

    print( 'rpn', command1 )
    print( 'rpn', command2 )

    # Converting to a list makes sure generators get evaluated before the
    # precision gets reset.
    result1 = rpn( shlex.split( command1 + ' -I' ) )[ 0 ]

    if isinstance( result1, RPNGenerator ):
        result1 = list( result1.getGenerator( ) )

    result2 = rpn( shlex.split( command2 + ' -I' ) )[ 0 ]

    if isinstance( result2, RPNGenerator ):
        result2 = list( result2.getGenerator( ) )

    compareResults( result1, result2 )

    print( '    both are equal!' )

    if g.timeIndividualTests:
        print( 'Test complete.  Time elapsed:  {:.3f} seconds'.format( time.process_time( ) - startTime ) )

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
                if compareValues( elem, elem2 ):
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
# //  This is the same as expectEqual, but the results don't need to be in the
# //  same order.
# //
# //******************************************************************************

def expectEquivalent( command1, command2 ):
    if g.testFilter:
        if g.testFilter not in command1 and g.testFilter not in command2:
            return

    if g.timeIndividualTests:
        startTime = time.process_time( )

    print( 'rpn', command1 )
    print( 'rpn', command2 )

    result1 = rpn( shlex.split( command1 + ' -I' ) )[ 0 ]
    result2 = rpn( shlex.split( command2 + ' -I' ) )[ 0 ]

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

    print( '    both are equal!' )

    if g.timeIndividualTests:
        print( 'Test complete.  Time elapsed:  {:.3f} seconds'.format( time.process_time( ) - startTime ) )

    print( '' )


# //******************************************************************************
# //
# //  testOperator
# //
# //******************************************************************************

def testOperator( command, ignoreCache = True ):
    if g.testFilter:
        if g.testFilter not in command:
            return

    if g.timeIndividualTests:
        startTime = time.process_time( )

    print( 'rpn', command )

    if ignoreCache:
        result = rpn( shlex.split( command + ' -I' ) )
    else:
        result = rpn( shlex.split( command ) )

    if result is not None and isinstance( result[ 0 ], mpf ) and result == [ nan ]:
        raise ValueError( 'unit test failed' )

    if result is not None:
        handleOutput( result )

    print( '    operator works!' )

    if g.timeIndividualTests:
        print( 'Test complete.  Time elapsed:  {:.3f} seconds'.format( time.process_time( ) - startTime ) )

    print( '' )


# //******************************************************************************
# //
# //  expectResult
# //
# //******************************************************************************

def expectResult( command, expected ):
    if g.testFilter:
        if g.testFilter not in command:
            return

    if g.timeIndividualTests:
        startTime = time.process_time( )

    print( 'rpn', command )
    result = rpn( shlex.split( command + ' -I' ) )[ 0 ]

    compare = None

    if isinstance( expected, list ):
        compare = [ ]

        for i in expected:
            if isinstance( i, ( int, float, complex ) ):
                compare.append( mpmathify( i ) )
            else:
                compare.append( i )
    else:
        if isinstance( expected, ( int, float, complex ) ):
            compare = mpmathify( expected )
        else:
            compare = expected

    compareResults( result, compare )

    print( '    test passed!' )

    if g.timeIndividualTests:
        print( 'Test complete.  Time elapsed:  {:.3f} seconds'.format( time.process_time( ) - startTime ) )

    print( '' )

