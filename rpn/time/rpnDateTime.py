#!/usr/bin/env python

#******************************************************************************
#
#  rpnDateTime.py
#
#  rpnChilada date and time operations
#  copyright (c) 2024, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import calendar
import datetime
import pendulum

from mpmath import mpf

from rpn.time.rpnDateTimeClass import RPNDateTime
from rpn.util.rpnGenerator import RPNGenerator
from rpn.units.rpnMeasurement import convertUnits
from rpn.util.rpnUtils import oneArgFunctionEvaluator, listArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.util.rpnValidator import argValidator, DateTimeValidator, IntValidator, ListValidator, YearValidator
from rpn.units.rpnMeasurementClass import RPNMeasurement

import rpn.util.rpnGlobals as g


#******************************************************************************
#
#  month and day constants
#
#******************************************************************************

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


#******************************************************************************
#
#  formatDateTime
#
#******************************************************************************

def formatDateTime( datetime ):
    if not isinstance( datetime, RPNDateTime ):
        raise ValueError( 'expected RPNDateTime' )

    if datetime.getDateOnly( ):
        return datetime.formatDate( )

    # if datetime.microsecond:
    #     return datetime.format( 'YYYY-MM-DD HH:mm:ss.SSSSSS' )
    # else:
    return datetime.format( includeTZ=g.showTimeZones )


#******************************************************************************
#
#  convertToUnixTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def convertToUnixTimeOperator( n ):
    return n.getTimestamp( )


#******************************************************************************
#
#  convertFromUnixTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertFromUnixTimeOperator( n ):
    try:
        result = RPNDateTime.parseDateTime( n ).getLocalTime( )
    except OverflowError as overflow_error:
        raise ValueError( 'out of range error' ) from overflow_error
    except TypeError as type_error:
        raise ValueError( 'expected time value' ) from type_error
    except OSError as os_error:
        raise ValueError( 'out of range error' ) from os_error

    return result


#******************************************************************************
#
#  convertToHMSOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def convertToHMSOperator( n ):
    return convertUnits( n, [ 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  convertToDHMSOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def convertToDHMSOperator( n ):
    return convertUnits( n, [ 'day', 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  convertToYDHMSOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def convertToYDHMSOperator( n ):
    return convertUnits( n, [ 'year', 'day', 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  makeJulianTimeOperator
#
#******************************************************************************

def makeJulianTime( n ):
    if isinstance( n, RPNGenerator ):
        return makeJulianTime( list( n ) )

    result = RPNDateTime( n[ 0 ], 1, 1 )

    if len( n ) >= 2:
        result = result.add( RPNMeasurement( n[ 1 ] - 1, 'day' ) )

    if len( n ) >= 3:
        result = result.add( RPNMeasurement( n[ 2 ], 'hour' ) )

    if len( n ) >= 4:
        result = result.add( RPNMeasurement( n[ 3 ], 'minute' ) )

    if len( n ) >= 5:
        result = result.add( RPNMeasurement( n[ 4 ], 'second' ) )

    if len( n ) >= 6:
        result = result.add( RPNMeasurement( n[ 5 ], 'microsecond' ) )

    return result


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def makeJulianTimeOperator( n ):
    return makeJulianTime( n )


#******************************************************************************
#
#  makeDateTimeOperator
#
#******************************************************************************

def makeDateTime( n ):
    if isinstance( n, ( RPNGenerator, int, mpf ) ):
        return makeDateTime( list( n ) )

    if isinstance( n[ 0 ], list ):
        return [ makeDateTime( i ) for i in n ]

    if len( n ) == 1:
        n.append( 1 )

    if len( n ) == 2:
        n.append( 1 )
    elif len( n ) > 7:
        n = n[ : 7 ]

    return RPNDateTime( *n )


@listArgFunctionEvaluator( )
@argValidator( [ ListValidator( ) ] )
def makeDateTimeOperator( n ):
    return makeDateTime( n )


#******************************************************************************
#
#  getNowOperator
#
#******************************************************************************

def getNow( ):
    return RPNDateTime.getNow( )

def getNowOperator( ):
    return getNow( )


#******************************************************************************
#
#  getTodayOperator
#
#******************************************************************************

def getTodayOperator( ):
    now = getNow( )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getTomorrowOperator
#
#******************************************************************************

def getTomorrowOperator( ):
    tomorrow = getNow( ).add( RPNMeasurement( 1, 'day' ) )
    return RPNDateTime( *tomorrow.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getYesterdayOperator
#
#******************************************************************************

def getYesterdayOperator( ):
    yesterday = getNow( ).subtract( RPNMeasurement( 1, 'day' ) )
    return RPNDateTime( *yesterday.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateEasterOperator
#
#******************************************************************************

def calculateEaster( year ):
    '''This algorithm comes from Gauss.'''
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )
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


@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateEasterOperator( year ):
    return calculateEaster( year )


#******************************************************************************
#
#  calculateAshWednesdayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateAshWednesdayOperator( year ):
    '''46 days before Easter (40 days, not counting Sundays)'''
    ashWednesday = calculateEaster( year ).add( RPNMeasurement( -46, 'day' ) )
    return RPNDateTime( *ashWednesday.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateGoodFridayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateGoodFridayOperator( year ):
    '''2 days before Easter'''
    goodFriday = calculateEaster( year ).add( RPNMeasurement( -2, 'day' ) )
    return RPNDateTime( *goodFriday.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getLastDayOfMonth
#
#******************************************************************************

def getLastDayOfMonth( year, month ):
    return calendar.monthrange( int( year ), int( month ) )[ 1 ]


#******************************************************************************
#
#  calculateNthWeekdayOfYear
#
#******************************************************************************

@argValidator( [ IntValidator( ), IntValidator( -53, 53 ), IntValidator( MONDAY, SUNDAY ) ] )
def calculateNthWeekdayOfYearOperator( year, nth, weekday ):
    ''' Monday = 1, etc., nth == -1 for last, etc.'''
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    if nth > 0:
        firstDay = RPNDateTime( year, 1, 1 )

        firstWeekday = weekday - firstDay.getDayOfWeek( ) + 1

        if firstWeekday < 1:
            firstWeekday += 7

        result = RPNDateTime( year, 1, firstWeekday ).add( RPNMeasurement( nth - 1, 'week' ) )
        result.setDateOnly( )

        return result

    if nth < 0:
        lastDay = RPNDateTime( year, 12, 31 )

        lastWeekday = weekday - ( lastDay.getDayOfWeek( ) )

        if lastWeekday > 0:
            lastWeekday -= 7

        lastWeekday += 31

        result = RPNDateTime( year, 12, lastWeekday, dateOnly = True ).add( RPNMeasurement( ( nth + 1 ), 'week' ) )
        result.setDateOnly( )

        return result

    raise ValueError( '0th weekday makes no sense in this context' )


#******************************************************************************
#
#  calculateNthWeekdayOfMonth
#
#******************************************************************************

def calculateNthWeekdayOfMonth( year, month, nth, weekday ):
    if weekday > SUNDAY or weekday < MONDAY:
        raise ValueError( 'day of week must be 1 - 7 (Monday to Sunday)' )

    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    firstDayOfWeek = pendulum.datetime( int( year ), int( month ), 1 ).day_of_week

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


@argValidator( [ IntValidator( ), IntValidator( 1, 12 ), IntValidator( -5, 5 ), IntValidator( MONDAY, SUNDAY ) ] )
def calculateNthWeekdayOfMonthOperator( year, month, nth, weekday ):
    return calculateNthWeekdayOfMonth( year, month, nth, weekday )


#******************************************************************************
#
#  calculateThanksgivingOperator
#
#  the fourth Thursday in November
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateThanksgivingOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, NOVEMBER, 4, THURSDAY )


#******************************************************************************
#
#  calculateLaborDayOperator
#
#  the first Monday in September
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateLaborDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, SEPTEMBER, 1, MONDAY )


#******************************************************************************
#
#  calculateElectionDayOperator
#
#  the first Tuesday after the first Monday (so it's never on the 1st day)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateElectionDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    result = calculateNthWeekdayOfMonth( year, NOVEMBER, 1, MONDAY )
    result.add( RPNMeasurement( 1, 'day' ) )

    return RPNDateTime( *result.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateMemorialDayOperator
#
#  the last Monday in May (4th or 5th Monday)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateMemorialDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, MAY, -1, MONDAY )


#******************************************************************************
#
#  calculatePresidentsDayOperator
#
#  the third Monday in February
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculatePresidentsDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, FEBRUARY, 3, MONDAY )


#******************************************************************************
#
#  calculateMartinLutherKingDayOperator
#
#  the third Monday in January
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateMartinLutherKingDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, JANUARY, 3, MONDAY )


#******************************************************************************
#
#  calculateColumbusDayOperator
#
#  the second Monday in October
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateColumbusDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, OCTOBER, 2, MONDAY )


#******************************************************************************
#
#  calculateMothersDayOperator
#
#  the second Sunday in May (in the U.S. and most other countries)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateMothersDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, MAY, 2, SUNDAY )


#******************************************************************************
#
#  calculateFathersDayOperator
#
#  the third Sunday in June (in the U.S. and most other countries)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateFathersDayOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    return calculateNthWeekdayOfMonth( year, JUNE, 3, SUNDAY )


#******************************************************************************
#
#  getNewYearsDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def getNewYearsDayOperator( year ):
    return RPNDateTime( year, JANUARY, 1, dateOnly = True )


#******************************************************************************
#
#  getVeteransDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def getVeteransDayOperator( year ):
    return RPNDateTime( year, NOVEMBER, 11, dateOnly = True )


#******************************************************************************
#
#  getIndependenceDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def getIndependenceDayOperator( year ):
    return RPNDateTime( year, JULY, 4, dateOnly = True )


#******************************************************************************
#
#  getChristmasDayOperator
#
#******************************************************************************

def getChristmasDay( year ):
    return RPNDateTime( year, DECEMBER, 25, dateOnly = True )


@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def getChristmasDayOperator( year ):
    return getChristmasDay( year )


#******************************************************************************
#
#  calculateAdventOperator
#
#  4 Sundays before Christmas
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateAdventOperator( year ):
    firstAdvent = getChristmasDay( year ).add( RPNMeasurement( -3, 'week' ) )
    firstAdvent = firstAdvent.subtract( RPNMeasurement( getDayOfWeek( firstAdvent ), 'day'  ) )

    return RPNDateTime( *firstAdvent.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getEpiphanyDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def getEpiphanyDayOperator( year ):
    return RPNDateTime( year, 1, 6, dateOnly = True )


#******************************************************************************
#
#  calculatePentecostSundayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculatePentecostSundayOperator( year ):
    return RPNDateTime( *( calculateEaster( year ).add( RPNMeasurement( 7, 'weeks' ) ).getYMD( ) ),
                        dateOnly = True )


#******************************************************************************
#
#  calculateAscensionThursdayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateAscensionThursdayOperator( year ):
    '''
I don't know why Ascension is 39 days after Easter instead of 40, but that's
how the math works out.  It's the 40th day of the Easter season.

Or as John Wright says, "Catholics can't count."  I think it stems from the
Church being created before the number 0.
    '''
    return RPNDateTime( *calculateEaster( year ).add( RPNMeasurement( 39, 'days' ) ).getYMD( ),
                        dateOnly = True )


#******************************************************************************
#
#  calculateDSTStartOperator
#
#  the second Sunday in March
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateDSTStartOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, MARCH, 2, SUNDAY )

    if year == 1974:
        return RPNDateTime( 1974, JANUARY, 7, dateOnly = True )

    if year >= 1967:
        return calculateNthWeekdayOfMonth( year, APRIL, 1, SUNDAY )

    raise ValueError( 'DST was not standardized before 1967' )


#******************************************************************************
#
#  calculateDSTEndOperator
#
#  the first Sunday in November
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ YearValidator( ) ] )
def calculateDSTEndOperator( year ):
    if isinstance( year, RPNDateTime ):
        year = year.getYear( )

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, NOVEMBER, 1, SUNDAY )

    if year == 1974:
        return RPNDateTime( 1974, DECEMBER, 31, dateOnly = True )  # technically DST never ended in 1974

    if year >= 1967:
        return calculateNthWeekdayOfMonth( year, OCTOBER, -1, SUNDAY )

    raise ValueError( 'DST was not standardized before 1967' )


#******************************************************************************
#
#  getDayOfWeekOperator
#
#******************************************************************************

def getDayOfWeek( n ):
    return n.getDayOfWeek( )


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getDayOfWeekOperator( n ):
    return getDayOfWeek( n )


#******************************************************************************
#
#  getDayOfWeekNameOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getDayOfWeekNameOperator( n ):
    return calendar.day_name[ getDayOfWeek( n ) - 1 ]


#******************************************************************************
#
#  getYearOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getYearOperator( n ):
    return n.getYear( )


#******************************************************************************
#
#  getMonthOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getMonthOperator( n ):
    return n.getMonth( )


#******************************************************************************
#
#  getDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getDayOperator( n ):
    return n.getDay( )


#******************************************************************************
#
#  getHourOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getHourOperator( n ):
    return n.getHour( )


#******************************************************************************
#
#  getMinuteOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getMinuteOperator( n ):
    return n.getMinute( )


#******************************************************************************
#
#  getSecondOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getSecondOperator( n ):
    return n.getSecond( )


#******************************************************************************
#
#  isDST
#
#******************************************************************************

def isDST( dateTime, timeZone ):
    return dateTime.astimezone( timeZone ).dst( ) != datetime.timedelta( 0 )


#******************************************************************************
#
#  setUTCOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getUTCOperator( dt ):
    return dt.convertTimeZone( 'utc' )


#******************************************************************************
#
#  getLocalTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getLocalTimeOperator( dt ):
    return dt.getLocalTime( )


#******************************************************************************
#
#  modifyTimeZoneOperator
#
#******************************************************************************

def modifyTimeZone( dt, timeZone ):
    return dt.modifyTimeZone( timeZone )


@twoArgFunctionEvaluator( )
#@argValidator( [ DateTimeValidator( ) ] )
def modifyTimeZoneOperator( dt, timeZone ):
    return modifyTimeZone( dt, timeZone )


#******************************************************************************
#
#  convertTimeZoneOperator
#
#******************************************************************************

def convertTimeZone( dt, timeZone ):
    return dt.convertTimeZone( timeZone )

@twoArgFunctionEvaluator( )
#@argValidator( [ DateTimeValidator( ) ] )
def convertTimeZoneOperator( dt, timezone ):
    return dt.convertTimeZone( timezone )
