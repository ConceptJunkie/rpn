#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDateTime.py
# //
# //  rpnChilada date and time operations
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import calendar
import datetime
import pytz

import arrow

from dateutil import tz

from mpmath import floor, fmod, fmul, fneg, fsub, nan

from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement, convertUnits
from rpn.rpnUtils import oneArgFunctionEvaluator, validateReal, validateRealInt

import rpn.rpnGlobals as g


# //******************************************************************************
# //
# //  month and day constants
# //
# //******************************************************************************

MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7

JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12


# //******************************************************************************
# //
# //  getLocalTimeZone
# //
# //******************************************************************************

def getLocalTimeZone( ):
    if 'time_zone' in g.userVariables:
        return pytz.timezone( g.userVariables[ 'time_zone' ] )
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
                                             int( microsecond ), tzinfo )

    def setDateOnly( self, dateOnly = True ):
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

    @staticmethod
    def getUTCOffset( timeZone = getLocalTimeZone( ) ):
        dateTime = datetime.datetime.now( timeZone )
        return RPNMeasurement( dateTime.utcoffset( ).total_seconds( ), 'seconds' )

    def getLocalTime( self, timeZone = getLocalTimeZone( ) ):
        result = self
        result = result.add( self.getUTCOffset( timeZone ) )
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
        elif self.year < value.year:
            return -1
        elif self.month > value.month:
            return 1
        elif self.month > value.month:
            return -1
        elif self.day > value.day:
            return 1
        elif self.day > value.day:
            return -1
        elif self.hour > value.hour:
            return 1
        elif self.hour > value.hour:
            return -1
        elif self.minute > value.minute:
            return 1
        elif self.minute > value.minute:
            return -1
        elif self.second > value.second:
            return 1
        elif self.second > value.second:
            return -1
        elif self.microsecond > value.microsecond:
            return 1
        elif self.microsecond > value.microsecond:
            return -1
        else:
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
        result = RPNDateTime.parseDateTime( validateRealInt( n ) )
    except OverflowError:
        print( 'rpn:  out of range error for \'from_unix_time\'' )
        return nan
    except TypeError:
        print( 'rpn:  expected integer for \'from_unix_time\'' )
        return nan

    return result


# //******************************************************************************
# //
# //  convertToHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToHMS( n ):
    return convertUnits( n, [ 'hour', 'minute', 'second' ] )


# //******************************************************************************
# //
# //  convertToDHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToDHMS( n ):
    return convertUnits( n, [ 'day', 'hour', 'minute', 'second' ] )


# //******************************************************************************
# //
# //  convertToYDHMS
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def convertToYDHMS( n ):
    return convertUnits( n, [ 'year', 'day', 'hour', 'minute', 'second' ] )


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
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


# //******************************************************************************
# //
# //  getTomorrow
# //
# //******************************************************************************

def getTomorrow( ):
    now = getNow( )
    now = now + datetime.timedelta( days = 1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


# //******************************************************************************
# //
# //  getYesterday
# //
# //******************************************************************************

def getYesterday( ):
    now = getNow( )
    now = now + datetime.timedelta( days = -1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


# //******************************************************************************
# //
# //  calculateEaster
# //
# //  This algorithm comes from Gauss.
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateEaster( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = validateRealInt( year )

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
    ashWednesday = calculateEaster( validateRealInt( year ) ).add( RPNMeasurement( -46, 'day' ) )
    return RPNDateTime( *ashWednesday.getYMD( ), dateOnly = True )


# //******************************************************************************
# //
# //  calculateGoodFriday
# //
# //  2 days before Easter
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateGoodFriday( year ):
    goodFriday = calculateEaster( validateRealInt( year ) ).add( RPNMeasurement( -2, 'day' ) )
    return RPNDateTime( *goodFriday.getYMD( ), dateOnly = True )


# //******************************************************************************
# //
# //  getLastDayOfMonth
# //
# //******************************************************************************

def getLastDayOfMonth( year, month ):
    return calendar.monthrange( validateRealInt( year ), validateRealInt( month ) )[ 1 ]


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
        year = validateRealInt( year )

    if validateRealInt( nth ) > 0:
        firstDay = RPNDateTime( year, 1, 1 )

        firstWeekDay = validateRealInt( weekday ) - firstDay.isoweekday( ) + 1

        if firstWeekDay < 1:
            firstWeekDay += 7

        result = RPNDateTime( year, 1, firstWeekDay ).add( RPNMeasurement( nth - 1, 'week' ) )
        result.setDateOnly( )

        return result
    elif nth < 0:
        lastDay = RPNDateTime( year, 12, 31 )

        lastWeekDay = validateRealInt( weekday ) - lastDay.isoweekday( )

        if lastWeekDay > 0:
            lastWeekDay -= 7

        lastWeekDay += 31

        result = RPNDateTime( year, 12, lastWeekDay, dateOnly = True ).add( RPNMeasurement( ( nth + 1 ), 'week' ) )
        result.setDateOnly( )

        return result

    raise ValueError( '0th weekday makes no sense in this context' )


# //******************************************************************************
# //
# //  calculateNthWeekdayOfMonth
# //
# //  Monday = 1, etc.
# // ( -1 == last. -2 == next to last, etc.)
# //
# //******************************************************************************

def calculateNthWeekdayOfMonth( year, month, nth, weekday ):
    if validateRealInt( weekday ) > SUNDAY or weekday < MONDAY:
        raise ValueError( 'day of week must be 1 - 7 (Monday to Sunday)' )

    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = validateRealInt( year )

    firstDayOfWeek = arrow.Arrow( validateRealInt( year ), validateRealInt( month ), 1 ).isoweekday( )

    if nth < 0:
        day = ( ( weekday + 1 ) - firstDayOfWeek ) % 7

        while day <= getLastDayOfMonth( year, month ):
            day += 7

        day += nth * 7
    else:
        day = ( weekday - firstDayOfWeek + 1 ) + nth * 7

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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, NOVEMBER, 4, THURSDAY )


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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, SEPTEMBER, 1, MONDAY )


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
        year = validateRealInt( year )

    result = calculateNthWeekdayOfMonth( year, NOVEMBER, 1, MONDAY )
    result.replace( day = result.day + 1 )

    return RPNDateTime( *result.getYMD( ), dateOnly = True )


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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, MAY, -1, MONDAY )


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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, FEBRUARY, 3, MONDAY )


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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, JANUARY, 3, MONDAY )


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
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, OCTOBER, 2, MONDAY )


# //******************************************************************************
# //
# //  calculateMothersDay
# //
# //  the second Sunday in May (in the U.S. and most other countries)
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateMothersDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, MAY, 2, SUNDAY )


# //******************************************************************************
# //
# //  calculateFathersDay
# //
# //  the third Sunday in June (in the U.S. and most other countries)
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateFathersDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = validateRealInt( year )

    return calculateNthWeekdayOfMonth( year, JUNE, 3, SUNDAY )


# //******************************************************************************
# //
# //  getNewYearsDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getNewYearsDay( year ):
    return RPNDateTime( year, JANUARY, 1, dateOnly = True )


# //******************************************************************************
# //
# //  getVeteransDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getVeteransDay( year ):
    return RPNDateTime( year, NOVEMBER, 11, dateOnly = True )


# //******************************************************************************
# //
# //  getIndependenceDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getIndependenceDay( year ):
    return RPNDateTime( year, JULY, 4, dateOnly = True )


# //******************************************************************************
# //
# //  getChristmasDay
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def getChristmasDay( year ):
    return RPNDateTime( year, DECEMBER, 25, dateOnly = True )


# //******************************************************************************
# //
# //  calculateAdvent
# //
# //  4 Sundays before Christmas
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateAdvent( year ):
    firstAdvent = getChristmasDay( validateRealInt( year ) ).add( RPNMeasurement( -3, 'week' ) )
    firstAdvent = firstAdvent.subtract( RPNMeasurement( getWeekday( firstAdvent ), 'day'  ) )

    return RPNDateTime( *firstAdvent.getYMD( ), dateOnly = True )


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
    return RPNDateTime( *( calculateEaster( year ).add( RPNMeasurement( 7, 'weeks' ) ).getYMD( ) ),
                        dateOnly = True )


# //******************************************************************************
# //
# //  calculateAscensionThursday
# //
# //******************************************************************************

@oneArgFunctionEvaluator( )
def calculateAscensionThursday( year ):
    '''
I don't know why it's 39 days after Easter instead of 40, but that's how
the math works out.  It's the 40th day of the Easter season.

Or as John Wright says, "Catholics can't count."
    '''
    return RPNDateTime( *calculateEaster( year ).add( RPNMeasurement( 39, 'days' ) ).getYMD( ),
                        dateOnly = True )


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
        year = validateRealInt( year )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, MARCH, 2, SUNDAY )
    elif year == 1974:
        return RPNDateTime( 1974, JANUARY, 7, dateOnly = True )
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, APRIL, 1, SUNDAY )
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
        year = validateRealInt( year )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, NOVEMBER, 1, SUNDAY )
    elif year == 1974:
        return RPNDateTime( 1974, DECEMBER, 31, dateOnly = True )  # technically DST never ended in 1974
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, OCTOBER, -1, SUNDAY )
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

def isDST( dateTime, timeZone ):
    return dateTime.astimezone( timeZone ).dst( ) != datetime.timedelta( 0 )

