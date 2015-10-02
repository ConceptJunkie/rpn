#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDate.py
# //
# //  RPN command-line calculator date operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import arrow
import calendar
import datetime

from rpnMeasurement import *
from rpnTime import *


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
# //  getNow
# //
# //******************************************************************************

def getNow( ):
    return RPNDateTime.now( tzinfo = tz.tzlocal( ) )


# //******************************************************************************
# //
# //  getToday
# //
# //******************************************************************************

def getToday( ):
    now = datetime.datetime.now( )
    return RPNDateTime( now.year, now.month, now.day, dateOnly = True, tzinfo = tz.tzlocal( ) )


# //******************************************************************************
# //
# //  calculateEaster
# //
# //  This algorithm comes from Gauss.
# //
# //******************************************************************************

def calculateEaster( year ):
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


# //******************************************************************************
# //
# //  calculateAshWednesday
# //
# //  46 days before Easter (40 days, not counting Sundays)
# //
# //******************************************************************************

def calculateAshWednesday( year ):
    return addTimes( calculateEaster( year ), Measurement( -46, 'day' ) )


# //******************************************************************************
# //
# //  getLastDayOfMonth
# //
# //******************************************************************************

def getLastDayOfMonth( year, month ):
    return calendar.monthrange( int( year ), int( month ) )[ 1 ]


# //******************************************************************************
# //
# //  getJulianDay
# //
# //******************************************************************************

def getJulianDay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    return n.timetuple( ).tm_yday


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
        year = int( year )

    if nth > 0:
        firstDay = RPNDateTime( year, 1, 1 )

        firstWeekDay = weekday - firstDay.isoweekday( ) + 1

        if firstWeekDay < 1:
            firstWeekDay += 7

        result = addTimes( RPNDateTime( year, 1, firstWeekDay ), Measurement( nth - 1, 'week' ) )
        result.setDateOnly( )

        return result
    elif nth < 0:
        lastDay = RPNDateTime( year, 12, 31 )

        lastWeekDay = weekday - lastDay.isoweekday( )

        if lastWeekDay > 0:
            lastWeekDay -= 7

        lastWeekDay += 31

        result = addTimes( RPNDateTime( year, 12, lastWeekDay, dateOnly = True ),
                           Measurement( ( nth + 1 ), 'week' ) )
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
    if weekday > Sunday or weekday < Monday:
        raise ValueError( 'day of week must be 1 - 7 (Monday to Sunday)' )

    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    firstDayOfWeek = arrow.Arrow( year, month, 1 ).isoweekday( )

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

def calculateThanksgiving( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    return calculateNthWeekdayOfMonth( year, November, 4, Thursday )


# //******************************************************************************
# //
# //  calculateLaborDay
# //
# //  the first Monday in September
# //
# //******************************************************************************

def calculateLaborDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    return calculateNthWeekdayOfMonth( year, 9, 1, 1 )


# //******************************************************************************
# //
# //  calculateElectionDay
# //
# //  the first Tuesday after the first Monday (so it's never on the 1st day)
# //
# //******************************************************************************

def calculateElectionDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    result = calculateNthWeekdayOfMonth( year, November, 1, Monday)
    return result.replace( day = result.day + 1 )


# //******************************************************************************
# //
# //  calculateMemorialDay
# //
# //  the last Monday in May (4th or 5th Monday)
# //
# //******************************************************************************

def calculateMemorialDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    return calculateNthWeekdayOfMonth( year, May, -1, Monday )


# //******************************************************************************
# //
# //  calculatePresidentsDay
# //
# //  the third Monday in February
# //
# //******************************************************************************

def calculatePresidentsDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

    return calculateNthWeekdayOfMonth( year, February, 3, Monday )


# //******************************************************************************
# //
# //  calculateDSTStart
# //
# //  the second Sunday in March
# //
# //******************************************************************************

def calculateDSTStart( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

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

def calculateDSTEnd( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year
    else:
        year = int( year )

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

def getISODay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a time type required for this operator' )

    return list( n.isocalendar( ) )


# //******************************************************************************
# //
# //  getWeekday
# //
# //******************************************************************************

def getWeekday( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return calendar.day_name[ n.weekday( ) ]


