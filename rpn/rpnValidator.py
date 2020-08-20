#!/usr/bin/env python

#******************************************************************************
#
#  rpnOperator.py
#
#  rpnChilada operator class definitions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import functools

from enum import Enum

from mpmath import floor, im, mpf

from mpmath.ctx_mp_python import mpc

from rpn.rpnDateTimeClass import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurementClass import RPNMeasurement

import rpn.rpnGlobals as g


#******************************************************************************
#
#  argValidator
#
#******************************************************************************

def argValidator( validators ):
    def argValidatorFunction( func ):
        @functools.wraps( func )

        def validateArgs( *args, **kwargs ):
            newArgs = [ ]
            for index, validator in enumerate( validators ):
                newArgs.append( validator.validate( args[ index ] ) )

            return func( *newArgs )

        return validateArgs

    return argValidatorFunction


#******************************************************************************
#
#  RPNValidator class
#
#******************************************************************************

class RPNValidator( ):
    Default =               0           # any argument is valid
    Real =                  1
    Integer =               2
    Complex =               4
    ComplexInteger =        8
    String =                16
    DateTime =              32
    Location =              64          # location object (operators will automatically convert a string)
    Boolean =               128         # 0 or 1
    Measurement =           256
    Length =                512
    AstronomicalObject =    1024
    List =                  2048        # the argument must be a list
    Generator =             4096        # Generator is a separate type now, but eventually it should be equivalent to List
    Function =              8192

    # These will be eliminated
    NonnegativeReal =       16384
    PositiveInteger =       32768
    NonnegativeInteger =    65536
    PrimeInteger =          131072

    type = Default
    min = None
    max = None
    specials = [ ]

    def __init__( self, type=Default, min=None, max=None, specials=None ):
        self.type = type
        self.min = min
        self.max = max

        if specials:
            self.specials = specials

    def validate( self, argument ):
        if self.type == self.Default:
            pass
        elif self.type == self.Integer:
            argument = self.validateInt( argument )
        elif self.type == self.Real:
            argument = self.validateReal( argument )
        elif self.type == self.Complex:
            argument = self.validateComplex( argument )
        elif self.type == self.Integer + self.Measurement:
            argument = self.validateIntOrMeasurement( argument )
        elif self.type == self.Real + self.Measurement:
            argument = self.validateRealOrMeasurement( argument )
        elif self.type == self.Complex + self.Measurement:
            argument = self.validateComplexOrMeasurement( argument )
        elif self.type == self.Real + self.Measurement + self.DateTime:
            argument = self.validateRealOrMeasurementOrDateTime( argument )
        elif self.type == self.Complex + self.Measurement + self.DateTime:
            argument = self.validateComplexOrMeasurementOrDateTime( argument )
        elif self.type == self.Length:
            argument = self.validateLength( argument )
        elif self.type == self.Integer + self.DateTime:
            argument = self.validateIntOrDateTime( argument )
        elif self.type == self.List:
            argument = self.validateList( argument )

        for special in self.specials:
            if not special[ 0 ]( argument ):
                raise ValueError( special[ 1 ] )

        return argument

    def addSpecial( self, func, formatString ):
        self.specials.append( ( func, formatString ) )

    def validateInt( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'\'type\' { type( argument ) } found, numeric value expected' )

        if im( argument ) != 0:
            raise ValueError( 'real argument expected ({})'.format( argument ) )

        if argument != floor( argument ):
            raise ValueError( 'integer argument expected ({})'.format( argument ) )

        if self.min is not None and argument < self.min:
            raise ValueError( f'argument value is { int( argument ) }, but the minimum valid value is { int( self.min ) }.' )

        if self.max is not None and argument > self.max:
            raise ValueError( f'argument value is { int( argument ) }, but the maximum valid value is { int( self.max ) }.' )

        return argument

    def validateReal( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'\'type\' { type( argument ) } found, numeric value expected' )

        if im( argument ) != 0:
            raise ValueError( 'real argument expected ({})'.format( argument ) )

        if self.min is not None and argument < self.min:
            raise ValueError( f'argument value is { argument }, minimum valid value is { self.min }.' )

        if self.max is not None and argument > self.max:
            raise ValueError( f'argument value is { argument }, maximum valid value is { self.max }.' )

        return argument

    def validateComplex( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'\'type\' { type( argument ) } found, numeric value expected' )

        if self.min is not None :
            raise ValueError( 'The min constraint is invalid for validating complex arguments.' )

        if self.max is not None :
            raise ValueError( 'The max constraint is invalid for validating complex arguments.' )

        return argument

    def validateDateTime( self, argument ):
        if isinstance( argument, RPNDateTime ):
            pass
        else:
            raise ValueError( f'argument is type { type( argument ) }, but date-time value expected' )

        return argument

    def validateMeasurement( self, argument ):
        if isinstance( argument, RPNMeasurement ):
            pass
        else:
            raise ValueError( f'argument is type { type( argument ) }, but measurement value expected' )

        return argument

    def validateIntOrMeasurement( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateInt( argument )
        elif isinstance( argument, RPNMeasurement ):
            self.validateMeasurement( argument )
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, numeric or measurement value expected' )

        return argument

    def validateIntOrDateTime( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateInt( argument )
        elif isinstance( argument, RPNDateTime ):
            self.validateDateTime( argument )
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, numeric or date-time value expected' )

        return argument

    def validateRealOrMeasurement( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateReal( argument )
        elif isinstance( argument, RPNMeasurement ):
            pass
        else:
            raise ValueError( f'argument is type { type( argument ) }, but numeric or measurement value expected' )

        return argument

    def validateComplexOrMeasurement( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateComplex( argument )
        elif isinstance( argument, RPNMeasurement ):
            pass
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, numeric or measurement value expected' )

        return argument

    def validateRealOrMeasurementOrDateTime( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateReal( argument )
        elif isinstance( argument, RPNMeasurement ):
            pass
        elif isinstance( argument, RPNDateTime ):
            pass
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, numeric, measurement, date-time value expected' )

        return argument

    def validateComplexOrMeasurementOrDateTime( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateComplex( argument )
        elif isinstance( argument, RPNMeasurement ):
            pass
        elif isinstance( argument, RPNDateTime ):
            pass
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, numeric, measurement, date-time value expected' )

        return argument

    def validateLength( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            self.validateReal( argument )
            argument = RPNMeasurement( argument, 'meter' )
        elif isinstance( argument, RPNMeasurement ):
            if argument.getDimensions( ) != { 'length' : 1 }:
                raise ValueError( 'measurement argument must be a length' )
        else:
            raise ValueError( f'\'type\' { type( argument ) } found, measurement (length) expected' )

        return argument

    def validateList( self, argument ):
        if not isinstance( argument, ( list, RPNGenerator ) ):
            raise ValueError( f'\'type\' { type( argument ) } found, list expected' )

        return argument



class DefaultValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Real, specials=specials )


class IntValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.Integer, min, max, specials )


class RealValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.Real, min, max, specials )


class ComplexValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.Complex, min, max, specials )


class MeasurementValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.Measurement, min, max, specials=specials )


class LengthValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.Length, min, max, specials=specials )


class DateTimeValidator( RPNValidator ):
    def __init__( self, min=None, max=None, specials=None ):
        super( ).__init__( RPNValidator.DateTime, min, max, specials=specials )


class IntOrDateTimeValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Integer + RPNValidator.DateTime, specials=specials )


class IntOrMeasurementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Integer + RPNValidator.Measurement, specials=specials )


class RealOrMeasurementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Real + RPNValidator.Measurement, specials=specials )


class ComplexOrMeasurementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Complex + RPNValidator.Measurement, specials=specials )


class RealOrMeasurementOrDateTimeValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Real + RPNValidator.Measurement + RPNValidator.DateTime, specials=specials )


class ComplexOrMeasurementOrDateTimeValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Complex + RPNValidator.Measurement + RPNValidator.DateTime, specials=specials )


class ListValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.List, specials=specials )

