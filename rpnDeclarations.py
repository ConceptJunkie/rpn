#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDeclarations.py
# //
# //  RPN command-line calculator constant and class declarations
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import calendar
import collections
import datetime
import ephem
import itertools

from dateutil import tz
from fractions import Fraction
from mpmath import *

from rpnEstimates import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


# //******************************************************************************
# //
# //  class RPNLocation
# //
# //  This class represents a location on the surface of the Earth.
# //
# //  The observer class measures lat/long in radians, but no one else does,
# //  so the methods assume degrees.
# //
# //******************************************************************************

class RPNLocation( object ):
    def __init__( self, name, observer ):
        self.name = name
        self.observer = observer

    def getLat( self ):
        return fdiv( fmul( mpmathify( float( self.observer.lat ) ), 180 ), pi )

    def getLong( self ):
        return fdiv( fmul( mpmathify( float( self.observer.long ) ), 180 ), pi )

    def setLat( self, value ):
        self.observer.lat = fmul( fdiv( value, 180 ), pi )

    def setLong( self, value ):
        self.observer.long = fmul( fdiv( value, 180 ), pi )


# //******************************************************************************
# //
# //  class OperatorInfo
# //
# //******************************************************************************

class OperatorInfo( ):
    def __init__( self, function, argCount = 0 ):
        self.function = function
        self.argCount = argCount


# //******************************************************************************
# //
# //  class FunctionInfo
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  FunctionInfo object.  However, it can't know how many of them it actually
# //  needs until it's time to evaluate the function, so we need to save all the
# //  terms we have so far, since we can't know until later how many of them we
# //  will need.
# //
# //  Once we are able to parse out how many arguments belong to the function
# //  declaration, then we can determine what arguments are left over to be used
# //  with the function operation.   All function operations take at least one
# //  argument before the function declaration.
# //
# //******************************************************************************

class FunctionInfo( ):
    def __init__( self, valueList = [ ], startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        else:
            self.valueList.append( valueList )

        self.startingIndex = startingIndex

    def evaluate( self, arg ):
        return arg

    def add( self, arg ):
        self.valueList.append( arg )


# //******************************************************************************
# //
# //  class Polynomial
# //
# //  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
# //
# //******************************************************************************

class Polynomial( object ):
    def __init__( self, *args ):
        """
        Create a polynomial in one of three ways:

        p = Polynomial( poly )              # copy constructor
        p = Polynomial( [ 1, 2, 3 ... ] )   # from sequence
        p = Polynomial( 1, 2, 3 ... )       # from scalars
        """
        super( Polynomial, self ).__init__( )

        if len( args ) == 1:
            val = args[ 0 ]

            if isinstance( val, Polynomial ):                # copy constructor
                self.coeffs = val.coeffs[ : ]
            elif isinstance( val, collections.Iterable ):    # from sequence
                self.coeffs = list( val )
            else:                                            # from single scalar
                self.coeffs = [ val + 0 ]
        else:                                                # multiple scalars
            self.coeffs = [ i + 0 for i in args ]
        self.trim( )

    def __add__( self, val ):
        "Return self+val"
        if isinstance( val, Polynomial ):                    # add Polynomial
            res = [ a + b for a, b in itertools.zip_longest( self.coeffs,
                                                             val.coeffs, fillvalue = 0 ) ]
        else:                                                # add scalar
            if self.coeffs:
                res = self.coeffs[ : ]
                res[ 0 ] += val
            else:
                res = val

        return self.__class__( res )

    def __call__( self, val ):
        "Evaluate at X==val"
        res = 0
        pwr = 1

        for co in self.coeffs:
            res += co * pwr
            pwr *= val

        return res

    def __eq__( self, val ):
        "Test self==val"
        if isinstance( val, Polynomial ):
            return self.coeffs == val.coeffs
        else:
            return len( self.coeffs ) == 1 and self.coeffs[ 0 ] == val

    def __mul__( self, val ):
        "Return self*val"
        if isinstance( val, Polynomial ):
            _s = self.coeffs
            _v = val.coeffs
            res = [ 0 ] * ( len( _s ) + len( _v ) - 1 )

            for selfpow, selfco in enumerate( _s ):
                for valpow, valco in enumerate( _v ):
                    res[ selfpow + valpow ] += selfco * valco
        else:
            res = [ co * val for co in self.coeffs ]
        return self.__class__( res )

    def __neg__( self ):
        "Return -self"
        return self.__class__( [ -co for co in self.coeffs ] )

    def __pow__( self, y, z = None ):
        raise NotImplemented( )

    def _radd__( self, val ):
        "Return val+self"
        return self + val

    def __repr__( self ):
        return "{0}({1})".format( self.__class__.__name__, self.coeffs )

    def __rmul__( self, val ):
        "Return val*self"
        return self * val

    def __rsub__( self, val ):
        "Return val-self"
        return -self + val

    def __str__( self ):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = [ ]

        for po, co in enumerate( self.coeffs ):
            if co:
                if po == 0:
                    po = ''
                elif po == 1:
                    po = 'X'
                else:
                    po = 'X^' + str( po )

                res.append( str( co ) + po )

        if res:
            res.reverse( )
            return ' + '.join( res )
        else:
            return "0"

    def __sub__( self, val ):
        "Return self-val"
        return self.__add__( -val )

    def trim( self ):
        "Remove trailing 0-coefficients"
        _co = self.coeffs

        if _co:
            offs = len( _co ) - 1

            if _co[ offs ] == 0:
                offs -= 1

                while offs >= 0 and _co[ offs ] == 0:
                    offs -= 1

                del _co[ offs + 1 : ]

    def getCoefficients( self ):
        return self.coeffs


# //******************************************************************************
# //
# //  ContinuedFraction
# //
# //  A continued fraction, represented as a list of integer terms.
# //
# //  adapted from ActiveState Python, recipe 578647
# //
# //******************************************************************************

class ContinuedFraction( list ):
    def __init__( self, value, maxterms = 15, cutoff = 1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            self.extend( value )
        else:
            raise ValueError( 'ContinuedFraction requires a number or a list' )

    def getFraction( self, terms = None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


