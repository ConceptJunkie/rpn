#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDateTime.py
# //
# //  RPN command-line calculator date and time operations
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import arrow
import calendar
import datetime
import pytz
import tzlocal

from dateutil import tz

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement, convertUnits
from rpn.rpnUtils import oneArgFunctionEvaluator, real, real_int

import rpn.rpnGlobals as g

from mpmath import floor, fmod, fmul, fneg, fsub, nan


# //******************************************************************************
# //
# //  month and day constants
# //
# //******************************************************************************

Monday = 1
Tuesday = 2
Wednesday = 3
Thursday = 4
Friday = 5
Saturday = 6
Sunday = 7

January = 1
February = 2
March = 3
April = 4
May = 5
June = 6
July = 7
August = 8
September = 9
October = 10
November = 11
December = 12


# //******************************************************************************
# //
# //  getLocalTimeZone
# //
# //******************************************************************************

def getLocalTimeZone( ):
    if 'time_zone' in g.userVariables:
        return pytz( g.userVariables[ 'time_zone' ] )
    elif tz.tzlocal( ) is None:
        return pytz.timezone( 'US/Eastern' )
    else:
        return tz.tzlocal( )


# //******************************************************************************
# //
# //  class RPNDateTime
# //
# //******************************************************************************

class RPNDateTime( arrow.Arrow ):
    '''This class wraps the Arrow class, with lots of convenience functions and
    implements support for date math.'''
    def __init__( self, year, month, day, hour = 0, minute = 0, second = 0,
                  microsecond = 0, tzinfo = getLocalTimeZone( ), dateOnly = False ):
        self.dateOnly = dateOnly
        super( RPNDateTime, self ).__init__( int( year ), int( month ), int( day ),
                                             int( hour ), int( minute ), int( second ),
                                             microsecond, tzinfo )

    def setDateOnly( self, dateOnly = True ):
        self.dateOnly = dateOnly

    def getDateOnly( self ):
        return self.dateOnly

    @staticmethod
    def get( *args, **kwargs ):
        result = arrow.api.get( *args, **kwargs )

        return RPNDateTime( result.year, result.month, result.day, result.hour,
                            result.minute, result.second, result.microsecond, result.tzinfo )

    @staticmethod
    def getUTCOffset( tz = getLocalTimeZone( ) ):
        d = datetime.datetime.now( tz )
        return RPNMeasurement( d.utcoffset( ).total_seconds( ), 'seconds' )

    def getLocalTime( self, tz = getLocalTimeZone( ) ):
        result = self
        result = result.add( self.getUTCOffset( tz ) )
        #return result.subtract( RPNMeasurement( result.astimezone( tz ).dst( ).seconds, 'seconds' ) )
        return result

    @staticmethod
    def parseDateTime( n ):
        result = arrow.api.get( n )

        return RPNDateTime( result.year, result.month, result.day, result.hour,
                            result.minute, result.second, result.microsecond, result.tzinfo )

    @staticmethod
    def convertFromArrow( arrow ):
        return RPNDateTime( arrow.year, arrow.month, arrow.day, arrow.hour,
                            arrow.minute, arrow.second, arrow.microsecond, arrow.tzinfo )

    @staticmethod
    def convertFromEphemDate( ephem_date ):
        dateValues = list( ephem_date.tuple( ) )

        dateValues.append( int( fmul( fsub( dateValues[ 5 ], floor( dateValues[ 5 ] ) ), 1000000 ) ) )
        dateValues[ 5 ] = int( floor( dateValues[ 5 ] ) )

        return RPNDateTime( *dateValues )

    @staticmethod
    def getNow( ):
        return RPNDateTime.convertFromArrow( arrow.now( ) )

    def incrementMonths( self, months ):
        newDay = self.day
        newMonth = self.month + int( months )
        newYear = self.year

        if not ( 1 < newMonth < 12 ):
            newYear += ( newMonth - 1 ) // 12
            newMonth = ( ( newMonth - 1 ) % 12 ) + 1

        maxDay = calendar.monthrange( newYear, newMonth )[ 1 ]

        if newDay > maxDay:
            newDay = maxDay

        return RPNDateTime( newYear, newMonth, newDay, self.hour, self.minute, self.second )

    def add( self, time ):
        if not isinstance( time, RPNMeasurement ):
            ValueError( 'RPNMeasurement expected' )

        if 'years' in g.unitOperators[ time.getUnitString( ) ].categories:
            years = convertUnits( time, 'year' ).getValue( )
            return self.replace( year = self.year + years )
        elif 'months' in g.unitOperators[ time.getUnitString( ) ].categories:
            months = convertUnits( time, 'month' ).getValue( )
            return self.incrementMonths( months )
        else:
            days = int( floor( convertUnits( time, 'day' ).getValue( ) ) )
            seconds = int( fmod( floor( convertUnits( time, 'second' ).getValue( ) ), 86400 ) )
            microseconds = int( fmod( floor( convertUnits( time, 'microsecond' ).getValue( ) ), 1000000 ) )

            try:
                return self + datetime.timedelta( days = days, seconds = seconds, microseconds = microseconds )
            except OverflowError:
                print( 'rpn:  value is out of range to be converted into a time' )
                return nan

    def format( self ):
        return "{0:4d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}".format( self.year, self.month, self.day,
                                                                        self.hour, self.minute, self.second )

    def formatDate( self ):
        return "{0:4d}-{1:02d}-{2:02d}".format( self.year, self.month, self.day )

    def formatTime( self ):
        return "{0:02d}:{1:02d}:{2:02d}".format( self.hour, self.minute, self.second )

    def subtract( self, time ):
        if isinstance( time, RPNMeasurement ):
            kneg = RPNMeasurement( fneg( time.getValue( ) ), time.getUnits( ) )
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


# //******************************************************************************
# //
# //  convertToUnixTime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( n ).timestamp
    except OverflowError:
        print( 'rpn:  out of range error for \'to_unix_time\'' )
        return nan
    except TypeError:
        print( 'rpn:  expected time value for \'to_unix_time\'' )
        return nan

    return result


# //******************************************************************************
# //
# //  convertFromUnixTime
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertFromUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( real( n ) )
    except OverflowError:
        print( 'rpn:  out of range error for \'from_unix_time\'' )
        return nan
    except TypeErrorme:
        print( 'rpn:  expected time value for \'from_unix_time\'' )
        return nan

    return result


# //******************************************************************************
# //
# //  convertToHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToHMS( n ):
    return convertUnits( n, [ RPNMeasurement( 1, { 'hour' : 1 } ),
                              RPNMeasurement( 1, { 'minute' : 1 } ),
                              RPNMeasurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  convertToDHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToDHMS( n ):
    return convertUnits( n, [ RPNMeasurement( 1, { 'day' : 1 } ),
                              RPNMeasurement( 1, { 'hour' : 1 } ),
                              RPNMeasurement( 1, { 'minute' : 1 } ),
                              RPNMeasurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  convertToYDHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToYDHMS( n ):
    return convertUnits( n, [ RPNMeasurement( 1, { 'year' : 1 } ),
                              RPNMeasurement( 1, { 'day' : 1 } ),
                              RPNMeasurement( 1, { 'hour' : 1 } ),
                              RPNMeasurement( 1, { 'minute' : 1 } ),
                              RPNMeasurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  makeJulianTime
# //
# //******************************************************************************

def makeJulianTime( n ):
    if isinstance( n, RPNGenerator ):
        return makeJulianTime( list( n ) )
    elif len( n ) == 1:
        return RPNDateTime( n[ 0 ], 1, 1 )

    result = RPNDateTime( n[ 0 ], 1, 1 ).add( RPNMeasurement( n[ 1 ] - 1, 'day' ) )

    if len( n ) >= 3:
        result = result.replace( hour = n[ 2 ] )

    if len( n ) >= 4:
        result = result.replace( minute = n[ 3 ] )

    if len( n ) >= 5:
        result = result.replace( second = n[ 4 ] )

    if len( n ) >= 6:
        result = result.replace( microsecond = n[ 5 ] )

    return result


# //******************************************************************************
# //
# //  makeISOTime
# //
# //******************************************************************************

def makeISOTime( n ):
    if isinstance( n, RPNGenerator ):
        return makeISOTime( list( n ) )
    elif len( n ) == 1:
        year = n[ 0 ]
        week = 1
        day = 1
    elif len( n ) == 2:
        year = n[ 0 ]
        week = n[ 1 ]
        day = 1
    else:
        year = n[ 0 ]
        week = n[ 1 ]
        day = n[ 2 ]

    result = datetime.datetime.strptime( '%04d-%02d-%1d' % ( int( year ), int( week ), int( day ) ), '%Y-%W-%w' )

    if RPNDateTime( year, 1, 4 ).isoweekday( ) > 4:
        result -= datetime.timedelta( days = 7 )

    return result


# //******************************************************************************
# //
# //  makeDateTime
# //
# //******************************************************************************

def makeDateTime( n ):
    if isinstance( n, ( RPNGenerator, int ) ):
        return makeDateTime( list( n ) )
    elif isinstance( n, str ):
        return RPNDateTime.get( n )
    elif isinstance( n[ 0 ], list ):
        return [ makeDateTime( i ) for i in n ]

    if len( n ) == 1:
        n.append( 1 )

    if len( n ) == 2:
        n.append( 1 )
    elif len( n ) > 7:
        n = n[ : 7 ]

    return RPNDateTime( *n )


# //******************************************************************************
# //
# //  getNow
# //
# //******************************************************************************

def getNow( ):
    return RPNDateTime.now( tzinfo = getLocalTimeZone( ) )


# //******************************************************************************
# //
# //  getToday
# //
# //******************************************************************************

def getToday( ):
    now = getNow( )
    return RPNDateTime( now.year, now.month, now.day, dateOnly = True )


# //******************************************************************************
# //
# //  getTomorrow
# //
# //******************************************************************************

def getTomorrow( ):
    now = getNow( )
    now = now + datetime.timedelta( days = 1 )
    return RPNDateTime( now.year, now.month, now.day, dateOnly = True )


# //******************************************************************************
# //
# //  getYesterday
# //
# //******************************************************************************

def getYesterday( ):
    now = getNow( )
    now = now + datetime.timedelta( days = -1 )
    return RPNDateTime( now.year, now.month, now.day, dateOnly = True )


# //******************************************************************************
# //
# //  calculateEaster
# //
# //  This algorithm comes from Gauss.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateEaster( year ):
    if isinstance( real( year ), RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    a = year % 19
    b = year // 100
    c = year % 100
    d = ( 19 * a + b - b // 4 - ( ( b - ( b + 8 ) // 25 + 1 ) // 3 ) + 15 ) % 30
    e = ( 32 + 2 * ( b % 4 ) + 2 * ( c // 4 ) - d - ( c % 4 ) ) % 7
    f = d + e - 7 * ( ( a + 11 * d + 22 * e ) // 451 ) + 114
    month = f // 31
    day = f % 31 + 1

    return RPNDateTime( year, month, day, dateOnly = True )


# //******************************************************************************
# //
# //  calculateAshWednesday
# //
# //  46 days before Easter (40 days, not counting Sundays)
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateAshWednesday( year ):
    return calculateEaster( real( year ) ).add( RPNMeasurement( -46, 'day' ) )


# //******************************************************************************
# //
# //  calculateGoodFriday
# //
# //  2 days before Easter
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateGoodFriday( year ):
    return calculateEaster( real( year ) ).add( RPNMeasurement( -2, 'day' ) )


# //******************************************************************************
# //
# //  getLastDayOfMonth
# //
# //******************************************************************************

def getLastDayOfMonth( year, month ):
    return calendar.monthrange( real_int( year ), real_int( month ) )[ 1 ]


# //******************************************************************************
# //
# //  calculateNthWeekdayOfYear
# //
# //  Monday = 1, etc., as per arrow, nth == -1 for last
# //
# //******************************************************************************

def calculateNthWeekdayOfYear( year, nth, weekday ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    if real( nth ) > 0:
        firstDay = RPNDateTime( year, 1, 1 )

        firstWeekDay = real( weekday ) - firstDay.isoweekday( ) + 1

        if firstWeekDay < 1:
            firstWeekDay += 7

        result = RPNDateTime( year, 1, firstWeekDay ).add( RPNMeasurement( nth - 1, 'week' ) )
        result.setDateOnly( )

        return result
    elif nth < 0:
        lastDay = RPNDateTime( year, 12, 31 )

        lastWeekDay = real( weekday ) - lastDay.isoweekday( )

        if lastWeekDay > 0:
            lastWeekDay -= 7

        lastWeekDay += 31

        result = RPNDateTime( year, 12, lastWeekDay, dateOnly = True ).add( RPNMeasurement( ( nth + 1 ), 'week' ) )
        result.setDateOnly( )

        return result


# //******************************************************************************
# //
# //  calculateNthWeekdayOfMonth
# //
# //  Monday = 1, etc.
# // ( -1 == last. -2 == next to last, etc.)
# //
# //******************************************************************************

def calculateNthWeekdayOfMonth( year, month, nth, weekday ):
    if real( weekday ) > Sunday or weekday < Monday:
        raise ValueError( 'day of week must be 1 - 7 (Monday to Sunday)' )

    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    firstDayOfWeek = arrow.Arrow( real( year ), real( month ), 1 ).isoweekday( )

    if nth < 0:
        day = ( ( real( weekday ) + 1 ) - firstDayOfWeek ) % 7

        while day <= getLastDayOfMonth( year, month ):
            day += 7

        day += nth * 7
    else:
        day = ( real( weekday ) - firstDayOfWeek + 1 ) + nth * 7

        if weekday >= firstDayOfWeek:
            day -= 7

    return RPNDateTime( year, month, day, dateOnly = True )


# //******************************************************************************
# //
# //  calculateThanksgiving
# //
# //  the fourth Thursday in November
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateThanksgiving( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, November, 4, Thursday )


# //******************************************************************************
# //
# //  calculateLaborDay
# //
# //  the first Monday in September
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateLaborDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, 9, 1, 1 )


# //******************************************************************************
# //
# //  calculateElectionDay
# //
# //  the first Tuesday after the first Monday (so it's never on the 1st day)
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateElectionDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    result = calculateNthWeekdayOfMonth( year, November, 1, Monday)
    return result.replace( day = result.day + 1 )


# //******************************************************************************
# //
# //  calculateMemorialDay
# //
# //  the last Monday in May (4th or 5th Monday)
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateMemorialDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, May, -1, Monday )


# //******************************************************************************
# //
# //  calculatePresidentsDay
# //
# //  the third Monday in February
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculatePresidentsDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, February, 3, Monday )


# //******************************************************************************
# //
# //  calculateMartinLutherKingDay
# //
# //  the third Monday in January
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateMartinLutherKingDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, January, 3, Monday )


# //******************************************************************************
# //
# //  calculateColumbusDay
# //
# //  the second Monday in October
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateColumbusDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    return calculateNthWeekdayOfMonth( year, October, 2, Monday )


# //******************************************************************************
# //
# //  getNewYearsDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNewYearsDay( year ):
    return RPNDateTime( year, 1, 1, dateOnly = True )


# //******************************************************************************
# //
# //  getVeteransDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getVeteransDay( year ):
    return RPNDateTime( year, 11, 11, dateOnly = True )


# //******************************************************************************
# //
# //  getIndependenceDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getIndependenceDay( year ):
    return RPNDateTime( year, 7, 4, dateOnly = True )


# //******************************************************************************
# //
# //  getChristmasDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getChristmasDay( year ):
    return RPNDateTime( year, 12, 25, dateOnly = True )


# //******************************************************************************
# //
# //  getEpiphanyDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getEpiphanyDay( year ):
    return RPNDateTime( year, 1, 6, dateOnly = True )


# //******************************************************************************
# //
# //  calculatePentecostSunday
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculatePentecostSunday( year ):
    return calculateEaster( year ).add( RPNMeasurement( 7, 'weeks' ) )


# //******************************************************************************
# //
# //  calculateAscensionThursday
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateAscensionThursday( year ):
    '''
    I don't know why it's 39 days after Easter instead of 40, but that's how
    the math works out.  As John Wright says, "Catholics can't count."
    '''
    return calculateEaster( year ).add( RPNMeasurement( 39, 'days' ) )


# //******************************************************************************
# //
# //  calculateDSTStart
# //
# //  the second Sunday in March
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateDSTStart( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, March, 2, Sunday )
    elif year == 1974:
        return RPNDateTime( 1974, January, 7, dateOnly = True )
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, April, 1, Sunday )
    else:
        raise ValueError( 'DST was not standardized before 1967' )


# //******************************************************************************
# //
# //  calculateDSTEnd
# //
# //  the first Sunday in November
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateDSTEnd( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = real_int( year )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, November, 1, Sunday )
    elif year == 1974:
        return RPNDateTime( 1974, December, 31, dateOnly = True )  # technically DST never ended in 1974
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, October, -1, Sunday )
    else:
        raise ValueError( 'DST was not standardized before 1967' )


# //******************************************************************************
# //
# //  getISODay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getISODay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return list( n.isocalendar( ) )


# //******************************************************************************
# //
# //  getWeekday
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getWeekday( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.weekday( ) + 1


# //******************************************************************************
# //
# //  getWeekdayName
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getWeekdayName( n ):
    return calendar.day_name[ getWeekday( n ) - 1 ]


# //******************************************************************************
# //
# //  getYear
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getYear( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.year


# //******************************************************************************
# //
# //  getMonth
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getMonth( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.month


# //******************************************************************************
# //
# //  getDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getDay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.day


# //******************************************************************************
# //
# //  getHour
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getHour( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.hour


# //******************************************************************************
# //
# //  getMinute
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getMinute( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.minute


# //******************************************************************************
# //
# //  getSecond
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getSecond( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.second + n.microsecond / 1000000


# //******************************************************************************
# //
# //  isDST
# //
# //******************************************************************************

def isDST( t, tz ):
    return t.astimezone( tz ).dst( ) != datetime.timedelta( 0 )

