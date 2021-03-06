#!/usr/bin/env python

#******************************************************************************
#
#  rpnDateTimeClass.py
#
#  rpnChilada date and time class
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import calendar
import datetime

from dateutil import tz
from functools import lru_cache

import arrow

from mpmath import floor, fmod, fmul, fneg, fsub, nan

from rpn.rpnMeasurementClass import RPNMeasurement

import rpn.rpnGlobals as g

arrowVersion = [ int( i ) for i in arrow.__version__.split( '.' ) ]

if arrowVersion[ 0 ] == 0 and arrowVersion[ 1 ] < 16:
    raise ValueError( 'Please upgrade the arrow package to version 0.16.0 or later.' )


#******************************************************************************
#
#  getUTCOffset
#
#******************************************************************************

def getUTCOffset( timeZone ):
    dateTime = datetime.datetime.now( timeZone )
    return RPNMeasurement( dateTime.utcoffset( ).total_seconds( ), 'seconds' )


#******************************************************************************
#
#  getLocalTimeZone
#
#******************************************************************************

@lru_cache( 1 )
def getLocalTimeZone( ):
    if 'time_zone' in g.userVariables:
        #print( 'tz from g.userVariables' )
        return tz.gettz( g.userVariables[ 'time_zone' ] )

    #print( 'tz from tz.gettz( )', tz.gettz( ), getUTCOffset( tz.gettz( ) ).value )
    return tz.gettz( )


#******************************************************************************
#
#  class RPNDateTime
#
#******************************************************************************

class RPNDateTime( arrow.Arrow ):
    '''
    This class wraps the Arrow class, with lots of convenience functions and
    implements support for date math.

    There was a temptation here to try to normalize timezones in this class, but
    I decided it's best left to the operator functions.
    '''
    def __init__( self, year, month, day, hour=0, minute=0, second=0,
                  microsecond=0, tzinfo=getLocalTimeZone( ), fold=0, dateOnly=False ):
        self.dateOnly = dateOnly
        super( RPNDateTime, self ).__init__( year=int( year ), month=int( month ), day=int( day ),
                                             hour=int( hour ), minute=int( minute ), second=int( second ),
                                             microsecond=int( microsecond ), tzinfo=tzinfo, fold=fold )

    def setDateOnly( self, dateOnly=True ):
        self.dateOnly = dateOnly

    def getDateOnly( self ):
        return self.dateOnly

    @staticmethod
    def get( *args, **kwargs ):
        result = arrow.api.get( *args, **kwargs )

        return RPNDateTime( result.year, result.month, result.day, result.hour,
                            result.minute, result.second, result.microsecond, result.tzinfo )

    def getYMD( self ):
        return ( self.year, self.month, self.day )

    def getLocalTime( self, timeZone=getLocalTimeZone( ) ):
        result = self
        result = result.subtract( getUTCOffset( self.tzinfo ) )
        result = result.add( getUTCOffset( timeZone ) )
        result.tzinfo = timeZone
        #return result.subtract( RPNMeasurement( result.astimezone( tz ).dst( ).seconds, 'seconds' ) )
        return result

    @staticmethod
    def parseDateTime( n ):
        result = arrow.api.get( n )

        return RPNDateTime( result.year, result.month, result.day, result.hour,
                            result.minute, result.second, result.microsecond, result.tzinfo )

    @staticmethod
    def convertFromArrow( arrowDT ):
        return RPNDateTime( arrowDT.year, arrowDT.month, arrowDT.day, arrowDT.hour,
                            arrowDT.minute, arrowDT.second, arrowDT.microsecond, arrowDT.tzinfo )

    @staticmethod
    def convertFromEphemDate( ephemDate ):
        dateValues = list( ephemDate.tuple( ) )

        dateValues.append( int( fmul( fsub( dateValues[ 5 ], floor( dateValues[ 5 ] ) ), 1000000 ) ) )
        dateValues[ 5 ] = int( floor( dateValues[ 5 ] ) )

        return RPNDateTime( *dateValues )

    @staticmethod
    def getNow( ):
        return RPNDateTime.convertFromArrow( arrow.now( ) )

    def compare( self, value ):
        if self.year > value.year:
            return 1
        if self.year < value.year:
            return -1

        if self.month > value.month:
            return 1

        if self.month < value.month:
            return -1

        if self.day > value.day:
            return 1

        if self.day < value.day:
            return -1

        if self.hour > value.hour:
            return 1

        if self.hour < value.hour:
            return -1

        if self.minute > value.minute:
            return 1

        if self.minute < value.minute:
            return -1

        if self.second > value.second:
            return 1

        if self.second < value.second:
            return -1

        if self.microsecond > value.microsecond:
            return 1

        if self.microsecond < value.microsecond:
            return -1

        return 0

    def incrementMonths( self, months ):
        newDay = self.day
        newMonth = self.month + int( months )
        newYear = self.year

        if not 1 < newMonth < 12:
            newYear += ( newMonth - 1 ) // 12
            newMonth = ( ( newMonth - 1 ) % 12 ) + 1

        maxDay = calendar.monthrange( newYear, newMonth )[ 1 ]

        if newDay > maxDay:
            newDay = maxDay

        return RPNDateTime( newYear, newMonth, newDay, self.hour, self.minute, self.second )

    def add( self, time ):
        if not isinstance( time, RPNMeasurement ):
            ValueError( 'RPNMeasurement expected' )

        #print( 'time.getUnitName( )', time.getUnitName( ) )
        #print( 'g.unitOperators[ time.getUnitName( ) ].categories', g.unitOperators[ time.getUnitName( ) ].categories )

        if 'years' in g.unitOperators[ time.getUnitName( ) ].categories:
            years = time.convertValue( 'year' )
            return self.replace( year = self.year + years )
        elif 'months' in g.unitOperators[ time.getUnitName( ) ].categories:
            months = time.convertValue( 'month' )
            return self.incrementMonths( months )
        else:
            days = int( floor( time.convertValue( 'day' ) ) )
            seconds = int( fmod( floor( time.convertValue( 'second' ) ), 86400 ) )
            microseconds = int( fmod( floor( time.convertValue( 'microsecond' ) ), 1000000 ) )

            try:
                return self + datetime.timedelta( days = days, seconds = seconds, microseconds = microseconds )
            except OverflowError:
                print( 'rpn:  value is out of range to be converted into a time' )
                return nan

    def format( self ):
        return '{0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format( self.year, self.month, self.day,
                                                                        self.hour, self.minute, self.second )

    def formatDate( self ):
        return '{0:4d}-{1:02d}-{2:02d}'.format( self.year, self.month, self.day )

    def formatTime( self ):
        return '{0:02d}:{1:02d}:{2:02d}'.format( self.hour, self.minute, self.second )

    def subtract( self, time ):
        if isinstance( time, RPNMeasurement ):
            kneg = RPNMeasurement( fneg( time.value ), time.units )
            return self.add( kneg )
        elif isinstance( time, RPNDateTime ):
            if self > time:
                delta = self - time
                factor = 1
            else:
                delta = time - self
                factor = -1

            if delta.days != 0:
                result = RPNMeasurement( delta.days * factor, 'day' )
                result = result.add( RPNMeasurement( delta.seconds * factor, 'second' ) )
                result = result.add( RPNMeasurement( delta.microseconds * factor, 'microsecond' ) )
            elif delta.seconds != 0:
                result = RPNMeasurement( delta.seconds * factor, 'second' )
                result = result.add( RPNMeasurement( delta.microseconds * factor, 'microsecond' ) )
            else:
                result = RPNMeasurement( delta.microseconds * factor, 'microsecond' )

            return result
        else:
            raise ValueError( 'incompatible type for subtracting from an absolute time' )

    def __gt__( self, value ):
        return self.compare( value ) > 0

    def __lt__( self, value ):
        return self.compare( value ) < 0

    def __eq__( self, value ):
        return self.compare( value ) == 0

    def __ge__( self, value ):
        return self.compare( value ) >= 0

    def __le__( self, value ):
        return self.compare( value ) <= 0
