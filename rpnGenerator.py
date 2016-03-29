#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnList.py
# //
# //  RPN command-line calculator list operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import itertools

from rpnUtils import getMPFIntegerAsString

from mpmath import arange, ceil, fadd, fdiv, fmul, fsub, mpmathify, power


# //******************************************************************************
# //
# //  class RPNGenerator
# //
# //******************************************************************************

class RPNGenerator( object ):
    """This class implements generators for rpn values, which allows rpn to
       avoid having to expand ranges to complete lists when evaluating them."""
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

    def __getitem__( self, index ):
        return next( itertools.islice( self.generator, index, index + 1 ) )

    @staticmethod
    def create( value ):
        if isinstance( value, RPNGenerator ):
            return value
        else:
            if isinstance( value, list ):
                count = len( value )
            else:
                count = 1

            return RPNGenerator( itemGenerator( value ), count )

    @staticmethod
    def createRange( start, end, step = 1 ):
        try:
            result = RPNGenerator( rangeGenerator( start, end, step ),
                                   ceil( fdiv( fadd( fsub( end, start ), 1 ), step ) ) )
        except TypeError:
            result = RPNGenerator( rangeGenerator( start, end, step ) )

        return result

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
    def createFilter( generator, func ):
        return RPNGenerator( filterGenerator( generator, func ) )

    @staticmethod
    def createPermutations( value ):
        return RPNGenerator( permutationGenerator( value ) )

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
        for item in value:
            yield item
    else:
        for item in [ value ]:
            yield item


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
# //  chainedGenerator
# //
# //******************************************************************************

def chainedGenerator( generator, func ):
    for i in generator:
        yield( func( i ) )


# //******************************************************************************
# //
# //  filterGenerator
# //
# //******************************************************************************

def filterGenerator( generator, func ):
    for i in generator:
        if func( i ):
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
# //  productGenerator
# //
# //******************************************************************************

def productGenerator( value ):
    for product in itertools.product( *value ):
        yield mpmathify( ''.join( product ) )


