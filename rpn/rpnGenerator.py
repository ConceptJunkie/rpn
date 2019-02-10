#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnList.py
# //
# //  RPN command-line calculator list operators
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools

from mpmath import arange, ceil, fadd, fdiv, fmul, fsub, mpmathify, power


# //******************************************************************************
# //
# //  class RPNGenerator
# //
# //******************************************************************************

class RPNGenerator( object ):
    '''This class implements generators for rpn values, which allows rpn to
    avoid having to expand ranges to complete lists when evaluating them.'''
    def __init__( self, generator = None, count = -1 ):
        self.generator = generator
        self.count = count

    def getGenerator( self ):
        return self.generator

    def getCount( self ):
        return self.count

    def __iter__( self ):
        return self.generator

    def __next__( self ):
        return self.generator.__next__( )

    # I have to admit, I have no idea how I came up with this or why it's necessary.
    def __getitem__( self, index ):
        if isinstance( index, slice ):
            return next( itertools.islice( self.generator, index.start, index.end, 1 ) )
        else:
            return next( itertools.islice( self.generator, index, index + 1 ) )

    def clone( self ):
        self.generator, newGenerator = itertools.tee( self.generator )
        return RPNGenerator( newGenerator, self.count )

    @staticmethod
    def create( value ):
        if isinstance( value, RPNGenerator ):
            return value
        elif isinstance( value, list ):
            count = len( value )
        else:
            count = 1

        return RPNGenerator( itemGenerator( value ), count )

    @staticmethod
    def createRange( start, end, step = 1 ):
        try:
            # attempt to calculate the number of items to be generated
            result = RPNGenerator( rangeGenerator( start, end, step ),
                                   ceil( fdiv( fadd( fsub( end, start ), 1 ), step ) ) )
        except TypeError:
            # if that fails, then just do without the count
            result = RPNGenerator( rangeGenerator( start, end, step ) )

        return result

    @staticmethod
    def createSizedRange( start, step = 1, count = 1 ):
        end = fadd( start, fmul( fsub( count, 1 ), step ) )
        return RPNGenerator( rangeGenerator( start, end, step ), count )

    @staticmethod
    def createGeometric( value, step, count ):
        return RPNGenerator( geometricRangeGenerator( value, step, count ), count )

    @staticmethod
    def createExponential( value, step, count ):
        return RPNGenerator( exponentialRangeGenerator( value, step, count ), count )

    @staticmethod
    def createChained( generator, func ):
        return RPNGenerator( chainedGenerator( generator, func ) )

    @staticmethod
    def createFilter( generator, func, invert=False ):
        return RPNGenerator( filterGenerator( generator, func, invert ) )

    @staticmethod
    def createPermutations( value ):
        return RPNGenerator( permutationGenerator( value ) )

    @staticmethod
    def createStringProduct( value ):
        return RPNGenerator( stringProductGenerator( value ) )

    @staticmethod
    def createProduct( value ):
        return RPNGenerator( productGenerator( value ) )

    @staticmethod
    def createGenerator( func, value ):
        if isinstance( value, list ):
            return RPNGenerator( func( *value ) )
        else:
            return RPNGenerator( func( value ) )


# //******************************************************************************
# //
# //  itemGenerator
# //
# //  A generator for a single item or list, used in list operators
# //
# //******************************************************************************

def itemGenerator( value ):
    if isinstance( value, list ):
        yield from value
    else:
        yield from [ value ]


# //******************************************************************************
# //
# //  rangeGenerator
# //
# //******************************************************************************

def rangeGenerator( start, end, step ):
    if start > end and step > 0:
        step = -step

    current = start

    if ( step > 0 ):
        while ( current <= end ):
            yield current
            current = fadd( current, step )
    else:
        while ( current >= end ):
            yield current
            current = fadd( current, step )


# //******************************************************************************
# //
# //  geometricRangeGenerator
# //
# //******************************************************************************

def geometricRangeGenerator( value, step, count ):
    current = value

    for i in arange( 0, count ):
        yield current
        current = fmul( current, step )


# //******************************************************************************
# //
# //  exponentialRangeGenerator
# //
# //******************************************************************************

def exponentialRangeGenerator( value, step, count ):
    current = value

    for i in arange( 0, count ):
        yield current
        current = power( current, step )


# //******************************************************************************
# //
# //  evaluateNestedArgs
# //
# //******************************************************************************

def evaluateNestedArgs( func, i ):
    if isinstance( i, ( list, RPNGenerator ) ):
        return [ evaluateNestedArgs( func, j ) for j in i ]
    else:
        return func( i )


# //******************************************************************************
# //
# //  chainedGenerator
# //
# //******************************************************************************

def chainedGenerator( generator, func ):
    for i in generator:
        yield( evaluateNestedArgs( func, i ) )


# //******************************************************************************
# //
# //  filterGenerator
# //
# //******************************************************************************

def filterGenerator( generator, func, invert=False ):
    for i in generator:
        if func( i ) != invert:
            yield( i )


# //******************************************************************************
# //
# //  permutationGenerator
# //
# //******************************************************************************

def permutationGenerator( value ):
    for permutation in itertools.permutations( value ):
        yield mpmathify( ''.join( permutation ) )


# //******************************************************************************
# //
# //  stringProductGenerator
# //
# //******************************************************************************

def stringProductGenerator( value ):
    for product in itertools.product( *value ):
        yield mpmathify( ''.join( product ) )


# //******************************************************************************
# //
# //  productGenerator
# //
# //******************************************************************************

def productGenerator( value ):
    for item in itertools.product( *value ):
        yield [ mpmathify( i ) for i in item ]

