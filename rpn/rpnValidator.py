#!/usr/bin/env python

#******************************************************************************
#
#  rpnValidator.py
#
#  rpnChilada argument validation classes
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import functools

from mpmath import floor, im, mpf
from mpmath.ctx_mp_python import mpc

from rpn.rpnDateTimeClass import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnLocationClass import RPNLocation
from rpn.rpnMeasurementClass import RPNMeasurement


#******************************************************************************
#
#  argValidator
#
#******************************************************************************

def argValidator( validators ):
    def argValidatorFunction( func ):
        @functools.wraps( func )
        def validateArgs( *args ):
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
    '''
    This is a class used to validate arguments for operators.
    '''
    Default =               0           # any argument is valid
    Real =                  1
    Integer =               1 << 1
    Complex =               1 << 2
    ComplexInteger =        1 << 3
    String =                1 << 4
    DateTime =              1 << 5
    Location =              1 << 6      # location object (operators will automatically convert a string)
    Boolean =               1 << 7      # 0 or 1
    Measurement =           1 << 8
    Length =                1 << 9
    AstronomicalObject =    1 << 10
    List =                  1 << 11     # the argument must be a list
    Generator =             1 << 12     # Generator is a separate type, but eventually it should be equivalent to List
    Function =              1 << 13
    TimeZone =              1 << 14
    Year =                  1 << 15
    Comparable =            1 << 16     # real, or measurement, or date-time
    Additive =              1 << 17     # a value that can have something added to or subtracted from
    Multiplicative =        1 << 18     # a value that can be multiplied (complex, measurement)

    def __init__( self, valueType=Default, minValue=None, maxValue=None, specials=None ):
        self.valueType = valueType
        self.minValue = minValue
        self.maxValue = maxValue
        self.specials = specials

    def validate( self, argument ):
        if self.valueType == self.Default:
            pass
        elif self.valueType == self.Integer:
            argument = self.validateInt( argument )
        elif self.valueType == self.Real:
            argument = self.validateReal( argument )
        elif self.valueType == self.Complex:
            argument = self.validateComplex( argument )
        elif self.valueType == self.Integer + self.Measurement:
            argument = self.validateIntOrMeasurement( argument )
        elif self.valueType == self.Real + self.Measurement:
            argument = self.validateRealOrMeasurement( argument )
        elif self.valueType == self.Complex + self.Measurement:
            argument = self.validateComplexOrMeasurement( argument )
        elif self.valueType == self.Real + self.Measurement + self.DateTime:
            argument = self.validateComparable( argument )
        elif self.valueType == self.Comparable:
            argument = self.validateAdditive( argument )
        elif self.valueType == self.Length:
            argument = self.validateLength( argument )
        elif self.valueType == self.List:
            argument = self.validateList( argument )
        elif self.valueType == self.Integer + self.String + self.Measurement:
            argument = self.validateElement( argument )
        elif self.valueType == self.Location:
            argument = self.validateLocation( argument )
        elif self.valueType == self.Location + self.DateTime:
            argument = self.validateLocationOrDateTime( argument )
        elif self.valueType == self.Year:
            argument = self.validateYear( argument )

        if self.specials:
            for special in self.specials:
                if not special[ 0 ]( argument ):
                    raise ValueError( special[ 1 ] )

        return argument

    def addSpecial( self, func, formatString ):
        if self.specials:
            self.specials.append( ( func, formatString ) )
        else:
            self.specials = [ ( func, formatString ) ]

    def validateInt( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'type { type( argument ) } found, integer value expected' )

        if im( argument ) != 0:
            raise ValueError( f'real argument expected ( { argument } )' )

        if argument != floor( argument ):
            raise ValueError( f'integer argument expected ({ argument })' )

        if self.minValue is not None and argument < self.minValue:
            raise ValueError( f'argument value is { int( argument ) }, '
                              f'but the minimum valid value is { int( self.minValue ) }.' )

        if self.maxValue is not None and argument > self.maxValue:
            raise ValueError( f'argument value is { int( argument ) }, '
                              f'but the maximum valid value is { int( self.maxValue ) }.' )

        return argument

    def validateReal( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'type { type( argument ) } found, numeric value expected' )

        if im( argument ) != 0:
            raise ValueError( f'real argument expected ({ argument })' )

        if self.minValue is not None and argument < self.minValue:
            raise ValueError( f'argument value is { argument }, minimum valid value is { self.minValue }.' )

        if self.maxValue is not None and argument > self.maxValue:
            raise ValueError( f'argument value is { argument }, maximum valid value is { self.maxValue }.' )

        return argument

    def validateComplex( self, argument ):
        if not isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            raise ValueError( f'type { type( argument ) } found, numeric value expected' )

        if self.minValue is not None :
            raise ValueError( 'The min constraint is invalid for validating complex arguments.' )

        if self.maxValue is not None :
            raise ValueError( 'The max constraint is invalid for validating complex arguments.' )

        return argument

    @staticmethod
    def validateDateTime( argument ):
        if not isinstance( argument, RPNDateTime ):
            raise ValueError( f'argument is type { type( argument ) }, but date-time value expected' )

        return argument

    @staticmethod
    def validateString( argument ):
        if not isinstance( argument, str ):
            raise ValueError( f'argument is type { type( argument ) }, but string value expected' )

        return argument

    @staticmethod
    def validateMeasurement( argument ):
        if not isinstance( argument, RPNMeasurement ):
            raise ValueError( f'argument is type { type( argument ) }, but measurement value expected' )

        return argument

    def validateIntOrMeasurement( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateInt( argument )
        elif isinstance( argument, RPNMeasurement ):
            self.validateMeasurement( argument )
        else:
            raise ValueError( f'type { type( argument ) } found, integer or measurement value expected' )

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
            raise ValueError( f'type { type( argument ) } found, numeric or measurement value expected' )

        return argument

    def validateComparable( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateReal( argument )
        elif isinstance( argument, ( RPNMeasurement, RPNDateTime ) ):
            pass
        else:
            raise ValueError( f'type { type( argument ) } found, numeric, measurement, date-time value expected' )

        return argument

    def validateAdditive( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateComplex( argument )
        elif isinstance( argument, ( RPNMeasurement, RPNDateTime ) ):
            pass
        else:
            raise ValueError( f'type { type( argument ) } found, numeric, measurement, date-time value expected' )

        return argument

    def validateLength( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            self.validateReal( argument )
            argument = RPNMeasurement( argument, 'meter' )
        elif isinstance( argument, RPNMeasurement ):
            if argument.getDimensions( ) != { 'length' : 1 }:
                raise ValueError( 'measurement argument must be a length' )
        else:
            raise ValueError( f'type { type( argument ) } found, measurement (length) expected' )

        return argument

    @staticmethod
    def validateList( argument ):
        if not isinstance( argument, ( list, RPNGenerator ) ):
            raise ValueError( f'type { type( argument ) } found, list expected' )

        return argument

    def validateElement( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            self.validateInt( argument )
        elif isinstance( argument, RPNMeasurement ):
            self.validateMeasurement( argument )
        elif not isinstance( argument, str ):
            raise ValueError( f'type { type( argument ) } found, string or integer expected' )

        return argument

    @staticmethod
    def validateLocation( argument ):
        if not isinstance( argument, ( str, RPNLocation ) ):
            raise ValueError( f'type { type( argument ) } found, string or location object expected' )

        return argument

    @staticmethod
    def validateLocationOrDateTime( argument ):
        if not isinstance( argument, ( str, RPNLocation, RPNDateTime ) ):
            raise ValueError( f'type { type( argument ) } found, string, date-time or location object expected' )

        return argument

    def validateYear( self, argument ):
        if isinstance( argument, ( complex, mpc, mpf, int, float ) ):
            argument = self.validateInt( argument )
        elif isinstance( argument, RPNDateTime ):
            self.validateDateTime( argument )
            argument = argument.year
        else:
            raise ValueError( f'type { type( argument ) } found, integer or date-time value expected' )

        return argument


class DefaultValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Default, specials=specials )


class IntValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.Integer, minValue, maxValue, specials )


class RealValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.Real, minValue, maxValue, specials )


class ComplexValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.Complex, minValue, maxValue, specials )


class MeasurementValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.Measurement, minValue, maxValue, specials=specials )


class StringValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.String, specials )


class LengthValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.Length, minValue, maxValue, specials=specials )


class DateTimeValidator( RPNValidator ):
    def __init__( self, minValue=None, maxValue=None, specials=None ):
        super( ).__init__( RPNValidator.DateTime, minValue, maxValue, specials=specials )


class ListValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.List, specials=specials )


class YearValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Year, specials=specials )


class LocationValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Location, specials=specials )


class ComparableValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Comparable, specials=specials )


class AdditiveValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Additive, specials=specials )


class MultiplicativeValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Multiplicative, specials=specials )


class ElementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Integer + RPNValidator.String, specials=specials )


# compound validators

class IntOrMeasurementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Integer + RPNValidator.Measurement, specials=specials )


class RealOrMeasurementValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Real + RPNValidator.Measurement, specials=specials )


class LocationOrDateTimeValidator( RPNValidator ):
    def __init__( self, specials=None ):
        super( ).__init__( RPNValidator.Location + RPNValidator.DateTime, specials=specials )
