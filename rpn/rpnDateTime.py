#!/usr/bin/env python

#******************************************************************************
#
#  rpnDateTime.py
#
#  rpnChilada date and time operations
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import calendar
import datetime

import arrow

from mpmath import mpf

from rpn.rpnDateTimeClass import RPNDateTime, getLocalTimeZone
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnLocation import getTimeZoneName
from rpn.rpnMeasurementClass import RPNMeasurement
from rpn.rpnMeasurement import convertUnits
from rpn.rpnUtils import oneArgFunctionEvaluator, listArgFunctionEvaluator, twoArgFunctionEvaluator
from rpn.rpnValidator import argValidator, DateTimeValidator, IntValidator, ListValidator, YearValidator


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
#  convertToUnixTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def convertToUnixTimeOperator( n ):
    try:
        result = RPNDateTime.parseDateTime( n.to( 'utc' ) ).int_timestamp
    except OverflowError as overflow_error:
        raise ValueError( 'out of range error' ) from overflow_error
    except TypeError as type_error:
        raise ValueError( 'expected time value' ) from type_error
    except OSError as os_error:
        raise ValueError( 'out of range error' ) from os_error

    return result


#******************************************************************************
#
#  convertFromUnixTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertFromUnixTimeOperator( n ):
    try:
        result = RPNDateTime.parseDateTime( int( n ) ).getLocalTime( )
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

    if len( n ) == 1:
        return RPNDateTime( n[ 0 ], 1, 1 )

    result = RPNDateTime( n[ 0 ], 1, 1 ).add( RPNMeasurement( n[ 1 ] - 1, 'day' ) )

    if len( n ) >= 3:
        result = result.replace( hour = int( n[ 2 ] ) )

    if len( n ) >= 4:
        result = result.replace( minute = int( n[ 3 ] ) )

    if len( n ) >= 5:
        result = result.replace( second = int( n[ 4 ] ) )

    if len( n ) >= 6:
        result = result.replace( microsecond = int( n[ 5 ] ) )

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
    return RPNDateTime.now( tzinfo=getLocalTimeZone( ) )


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
    now = getNow( )
    now = now + datetime.timedelta( days = 1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getYesterdayOperator
#
#******************************************************************************

def getYesterdayOperator( ):
    now = getNow( )
    now = now + datetime.timedelta( days = -1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateEasterOperator
#
#******************************************************************************

def calculateEaster( year ):
    '''This algorithm comes from Gauss.'''
    if isinstance( year, RPNDateTime ):
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
    ''' Monday = 1, etc., as per arrow, nth == -1 for last, etc.'''
    if isinstance( year, RPNDateTime ):
        year = year.year

    if nth > 0:
        firstDay = RPNDateTime( year, 1, 1 )

        firstWeekDay = weekday - firstDay.isoweekday( ) + 1

        if firstWeekDay < 1:
            firstWeekDay += 7

        result = RPNDateTime( year, 1, firstWeekDay ).add( RPNMeasurement( nth - 1, 'week' ) )
        result.setDateOnly( )

        return result

    if nth < 0:
        lastDay = RPNDateTime( year, 12, 31 )

        lastWeekDay = weekday - lastDay.isoweekday( )

        if lastWeekDay > 0:
            lastWeekDay -= 7

        lastWeekDay += 31

        result = RPNDateTime( year, 12, lastWeekDay, dateOnly = True ).add( RPNMeasurement( ( nth + 1 ), 'week' ) )
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
        year = year.year

    firstDayOfWeek = arrow.Arrow( int( year ), int( month ), 1 ).isoweekday( )

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
        year = year.year

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
        year = year.year

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
        year = year.year

    result = calculateNthWeekdayOfMonth( year, NOVEMBER, 1, MONDAY )
    result.replace( day = result.day + 1 )

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
        year = year.year

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
        year = year.year

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
        year = year.year

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
        year = year.year

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
        year = year.year

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
        year = year.year

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
    firstAdvent = firstAdvent.subtract( RPNMeasurement( getWeekday( firstAdvent ), 'day'  ) )

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
        year = year.year

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
        year = year.year

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, NOVEMBER, 1, SUNDAY )

    if year == 1974:
        return RPNDateTime( 1974, DECEMBER, 31, dateOnly = True )  # technically DST never ended in 1974

    if year >= 1967:
        return calculateNthWeekdayOfMonth( year, OCTOBER, -1, SUNDAY )

    raise ValueError( 'DST was not standardized before 1967' )


#******************************************************************************
#
#  getWeekdayOperator
#
#******************************************************************************

def getWeekday( n ):
    return n.weekday( ) + 1


@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getWeekdayOperator( n ):
    return getWeekday( n )


#******************************************************************************
#
#  getWeekdayNameOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getWeekdayNameOperator( n ):
    return calendar.day_name[ getWeekday( n ) - 1 ]


#******************************************************************************
#
#  getYearOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getYearOperator( n ):
    return n.year


#******************************************************************************
#
#  getMonthOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getMonthOperator( n ):
    return n.month


#******************************************************************************
#
#  getDayOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getDayOperator( n ):
    return n.day


#******************************************************************************
#
#  getHourOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getHourOperator( n ):
    return n.hour


#******************************************************************************
#
#  getMinuteOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getMinuteOperator( n ):
    return n.minute


#******************************************************************************
#
#  getSecondOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getSecondOperator( n ):
    return n.second


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
    return dt.to( 'utc' )


#******************************************************************************
#
#  setLocalTimeOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ DateTimeValidator( ) ] )
def getLocalTimeOperator( dt ):
    return dt.getLocalTime( )


#******************************************************************************
#
#  setTimeZoneOperator
#
#******************************************************************************

def setTimeZone( dt, timezone ):
    try:
        tz = arrow.now( timezone ).tzinfo
    except TypeError:
        tz = arrow.now( getTimeZoneName( timezone ) ).tzinfo
    except arrow.parser.ParserError:
        tz = arrow.now( getTimeZoneName( timezone ) ).tzinfo
    #except Exception as e:
    #    import sys
    #    print('Whew!', sys.exc_info()[0], 'occurred.')

    dt = RPNDateTime.parseDateTime( dt )
    dt = dt.replace( tzinfo=tz )
    return dt


@twoArgFunctionEvaluator( )
#@argValidator( [ DateTimeValidator( ) ] )
def setTimeZoneOperator( dt, timezone ):
    return setTimeZone( dt, timezone )


#******************************************************************************
#
#  convertTimeZoneOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
#@argValidator( [ DateTimeValidator( ) ] )
def convertTimeZoneOperator( dt, timezone ):
    try:
        tz = arrow.now( timezone ).tzinfo
    except arrow.parser.ParserError:
        tz = arrow.now( getTimeZoneName( timezone ) ).tzinfo

    return dt.to( tz )
