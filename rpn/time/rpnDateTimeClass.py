#!/usr/bin/env python

#******************************************************************************
#
#  rpnDateTimeClass.py
#
#  rpnChilada date and time class
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import calendar
import datetime
from functools import lru_cache

from tzlocal import get_localzone

import rpn.util.rpnGlobals as g
from dateutil import tz

from mpmath import floor, fmod, fmul, fneg, fsub, mpf, nan

from rpn.units.rpnMeasurementClass import RPNMeasurement

import pendulum


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
    return get_localzone()


#******************************************************************************
#
#  class RPNDateTime
#
#******************************************************************************

class RPNDateTime( object ):
    '''
    This class wraps the Pendulum class, with lots of convenience functions and
    implements support for date math.

    There was a temptation here to try to normalize timezones in this class, but
    I decided it's best left to the operator functions.
    '''
    def __init__( self, year, month, day, hour=0, minute=0, second=0,
                  microsecond=0, tz=getLocalTimeZone( ), fold=0, dateOnly=False ):
        self.dateOnly = dateOnly
        self.dateTime = pendulum.datetime( int( year ), int( month ), int( day ), int( hour ),
                                          int( minute ), int( second ), int( microsecond ), tz=tz )

    def setDateOnly( self, dateOnly=True ):
        self.dateOnly = dateOnly

    def getDateOnly( self ):
        return self.dateOnly

    def getYMD( self ):
        return ( self.getYear( ), self.getMonth( ), self.getDay( ) )

    def getYMDHMS( self ):
        return ( self.getYear( ), self.getMonth( ), self.getDay( ), self.getHour( ), self.getMinute( ),
                 self.getSecond( ) )

    def getLocalTime( self, timeZone=getLocalTimeZone( ) ):
        result = self
        result.setTimeZone( timeZone )
        return result

    @staticmethod
    def parseDateTime( n ):
        if isinstance( n, str ):
            result = pendulum.parse( n )

            return RPNDateTime( result.year, result.month, result.day, result.hour,
                                result.minute, result.second, result.microsecond, result.tzinfo )
        elif isinstance( n, datetime.datetime ):
            return RPNDateTime( n.year, n.month, n.day, n.hour, n.minute, n.second, n.microsecond, n.tzinfo )
        elif isinstance( n, RPNDateTime ):
            return RPNDateTime( n.dateTime.year, n.dateTime.month, n.dateTime.day, n.dateTime.hour, n.dateTime.minute,
                                n.dateTime.second, n.dateTime.microsecond, n.dateTime.tzinfo )
        elif isinstance( n, mpf ):
            result = RPNDateTime( 1, 1, 1 )
            result.dateTime = pendulum.from_timestamp( int( n ) )
            return result
        else:
            raise ValueError( 'RPNDateTime parsing unsupported type' )

    @staticmethod
    def convertFromPendulum( pendulumDT ):
        return RPNDateTime( pendulumDT.year, pendulumDT.month, pendulumDT.day, pendulumDT.hour,
                            pendulumDT.minute, pendulumDT.second, pendulumDT.microsecond, pendulumDT.tzinfo )

    @staticmethod
    def convertFromEphemDate( ephemDate ):
        dateValues = list( ephemDate.tuple( ) )

        dateValues.append( int( fmul( fsub( dateValues[ 5 ], floor( dateValues[ 5 ] ) ), 1_000_000 ) ) )
        dateValues[ 5 ] = int( floor( dateValues[ 5 ] ) )

        # We always pass UTC time to ephem, so we'll expect UTC back
        dateValues.append( tz.gettz( 'UTC' ) )

        return RPNDateTime( *dateValues )

    @staticmethod
    def getNow( ):
        timeZone = pendulum.timezone( str( getLocalTimeZone( ) ).replace( ' ', '_' ) )
        dateTime = RPNDateTime.convertFromPendulum( pendulum.now( ) )
        dateTime = dateTime.setTimeZone( timeZone )
        return dateTime

    def compare( self, value ):
        if self.dateTime.year > value.dateTime.year:
            return 1

        if self.dateTime.year < value.dateTime.year:
            return -1

        if self.dateTime.month > value.dateTime.month:
            return 1

        if self.dateTime.month < value.dateTime.month:
            return -1

        if self.dateTime.day > value.dateTime.day:
            return 1

        if self.dateTime.day < value.dateTime.day:
            return -1

        if self.dateTime.hour > value.dateTime.hour:
            return 1

        if self.dateTime.hour < value.dateTime.hour:
            return -1

        if self.dateTime.minute > value.dateTime.minute:
            return 1

        if self.dateTime.minute < value.dateTime.minute:
            return -1

        if self.dateTime.second > value.dateTime.second:
            return 1

        if self.dateTime.second < value.dateTime.second:
            return -1

        if self.dateTime.microsecond > value.dateTime.microsecond:
            return 1

        if self.dateTime.microsecond < value.dateTime.microsecond:
            return -1

        return 0

    def incrementMonths( self, months ):
        newDay = self.dateTime.day
        newMonth = self.dateTime.month + int( months )
        newYear = self.dateTime.year

        if not 1 < newMonth < 12:
            newYear += ( newMonth - 1 ) // 12
            newMonth = ( ( newMonth - 1 ) % 12 ) + 1

        maxDay = calendar.monthrange( newYear, newMonth )[ 1 ]
        newDay = min( maxDay, newDay )

        self.dateTime = pendulum.datetime( newYear, newMonth, newDay, self.dateTime.hour, self.dateTime.minute,
                                           self.dateTime.second )

    def __add__( self, time ):
        return add( self, time )

    def __subtract__( self, time ):
        return subtract( self, time )

    def add( self, time ):
        if not isinstance( time, RPNMeasurement ):
            ValueError( 'RPNMeasurement expected' )

        #print( 'time.getUnitName( )', time.getUnitName( ) )
        #print( 'g.unitOperators[ time.getUnitName( ) ].categories', g.unitOperators[ time.getUnitName( ) ].categories )

        if 'years' in g.unitOperators[ time.getUnitName( ) ].categories:
            years = time.value
            self.dateTime = self.dateTime.add( years=int( years ) )
            return self
        elif 'months' in g.unitOperators[ time.getUnitName( ) ].categories:
            months = time.value
            self.dateTime = self.dateTime.add( months=int( months ) )
            return self
        else:
            days = int( floor( time.convertValue( 'day' ) ) )
            seconds = int( fmod( floor( time.convertValue( 'second' ) ), 86400 ) )
            microseconds = int( fmod( floor( time.convertValue( 'microsecond' ) ), 1_000_000 ) )

            try:
                self.dateTime = self.dateTime.add( days = days, seconds = seconds, microseconds = microseconds )
                return self
            except OverflowError:
                print( 'rpn:  value is out of range to be converted into a time' )
                return nan

    def format( self, includeTZ=True, locale='en-us' ):
        if includeTZ:
            return self.dateTime.format( 'YYYY-MM-DD HH:mm:ss ZZ' )
        else:
            return self.dateTime.format( 'YYYY-MM-DD HH:mm:ss' )

    def formatDate( self ):
        return self.dateTime.format( 'YYYY-MM-DD' )

    def formatTime( self ):
        return self.dateTime.format( 'HH:mm:ss' )

    def subtract( self, time ):
        if isinstance( time, RPNMeasurement ):
            kneg = RPNMeasurement( fneg( time.value ), time.units )
            return self.add( kneg )
        elif isinstance( time, RPNDateTime ):
            if self > time:
                delta = self.dateTime - time.dateTime
                factor = 1
            else:
                delta = time.dateTime - self.dateTime
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

    def modifyTimeZone( self, tz ):
        offset = self.dateTime.offset

        try:
            self.dateTime = self.dateTime.in_tz( tz )
        except pendulum.tz.exceptions.InvalidTimezone:
            self.dateTime = self.dateTime.in_tz( getLocation( tz ).getTimeZone( ) )

        newOffset = self.dateTime.offset

        self.dateTime = self.dateTime.add( seconds = ( newOffset - offset ) )

        return self

    def setTimeZone( self, tz ):
        try:
            self.dateTime = self.dateTime.set( tz=tz )
        except pendulum.tz.exceptions.InvalidTimezone:
            self.dateTime = self.dateTime.set( getLocation( tz ).getTimeZone( ) )

        return self

    def getYear( self ):
        return self.dateTime.year

    def getMonth( self ):
        return self.dateTime.month

    def getDay( self ):
        return self.dateTime.day

    def getHour( self ):
        return self.dateTime.hour

    def getMinute( self ):
        return self.dateTime.minute

    def getSecond( self ):
        return self.dateTime.second

    def getMicrosecond( self ):
        return self.dateTime.microsecond

    def getDayOfWeek( self ):
        return self.dateTime.weekday( ) + 1

    def getWeekOfYear( self ):
        return self.dateTime.week_of_year

    def getTimestamp( self ):
        return self.dateTime.int_timestamp
