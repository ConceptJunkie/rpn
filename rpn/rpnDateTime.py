#!/usr/bin/env python

#******************************************************************************
#
#  rpnDateTime.py
#
#  rpnChilada date and time operations
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import calendar
import datetime
import pytz

import arrow

from dateutil import tz

from mpmath import floor, fmod, fmul, fneg, fsub, nan

from rpn.rpnDateTimeClass import RPNDateTime
from rpn.rpnGenerator import RPNGenerator
from rpn.rpnMeasurement import RPNMeasurement, convertUnits
from rpn.rpnUtils import oneArgFunctionEvaluator
from rpn.rpnValidator import argValidator, IntValidator

import rpn.rpnGlobals as g


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
#  getLocalTimeZone
#
#******************************************************************************

def getLocalTimeZone( ):
    if 'time_zone' in g.userVariables:
        return pytz.timezone( g.userVariables[ 'time_zone' ] )
    elif tz.tzlocal( ) is None:
        return pytz.timezone( 'US/Eastern' )
    else:
        return tz.tzlocal( )


#******************************************************************************
#
#  convertToUnixTime
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def convertToUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( n ).timestamp
    except OverflowError:
        raise ValueError( 'out of range error' )
    except TypeError:
        raise ValueError( 'expected time value' )
    except OSError:
        raise ValueError( 'out of range error' )

    return result


#******************************************************************************
#
#  convertFromUnixTime
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def convertFromUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( int( n ) )
    except OverflowError:
        raise ValueError( 'out of range error' )
    except TypeError:
        raise ValueError( 'expected time value' )
    except OSError:
        raise ValueError( 'out of range error' )

    return result


#******************************************************************************
#
#  convertToHMS
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def convertToHMS( n ):
    return convertUnits( n, [ 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  convertToDHMS
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def convertToDHMS( n ):
    return convertUnits( n, [ 'day', 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  convertToYDHMS
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def convertToYDHMS( n ):
    return convertUnits( n, [ 'year', 'day', 'hour', 'minute', 'second' ] )


#******************************************************************************
#
#  makeJulianTime
#
#******************************************************************************

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


#******************************************************************************
#
#  makeISOTime
#
#******************************************************************************

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


#******************************************************************************
#
#  makeDateTime
#
#******************************************************************************

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


#******************************************************************************
#
#  getNow
#
#******************************************************************************

def getNow( ):
    return RPNDateTime.now( tzinfo = getLocalTimeZone( ) )


#******************************************************************************
#
#  getToday
#
#******************************************************************************

def getToday( ):
    now = getNow( )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getTomorrow
#
#******************************************************************************

def getTomorrow( ):
    now = getNow( )
    now = now + datetime.timedelta( days = 1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getYesterday
#
#******************************************************************************

def getYesterday( ):
    now = getNow( )
    now = now + datetime.timedelta( days = -1 )
    return RPNDateTime( *now.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateEaster
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
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


#******************************************************************************
#
#  calculateAshWednesday
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateAshWednesday( year ):
    '''46 days before Easter (40 days, not counting Sundays)'''
    ashWednesday = calculateEaster( year ).add( RPNMeasurement( -46, 'day' ) )
    return RPNDateTime( *ashWednesday.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateGoodFriday
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateGoodFriday( year ):
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

@argValidator( [ IntValidator( ),
                 IntValidator( -53, 53 ),
                 IntValidator( MONDAY, SUNDAY ) ] )
def calculateNthWeekdayOfYear( year, nth, weekday ):
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
    elif nth < 0:
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

@argValidator( [ IntValidator( ),
                 IntValidator( 1, 12 ),
                 IntValidator( -5, 5 ),
                 IntValidator( MONDAY, SUNDAY ) ] )
def calculateNthWeekdayOfMonthOperator( year, month, nth, weekday ):
    return calculateNthWeekdayOfMonth( year, month, nth, weekday )


#******************************************************************************
#
#  calculateThanksgiving
#
#  the fourth Thursday in November
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateThanksgiving( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, NOVEMBER, 4, THURSDAY )


#******************************************************************************
#
#  calculateLaborDay
#
#  the first Monday in September
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateLaborDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, SEPTEMBER, 1, MONDAY )


#******************************************************************************
#
#  calculateElectionDay
#
#  the first Tuesday after the first Monday (so it's never on the 1st day)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateElectionDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    result = calculateNthWeekdayOfMonth( year, NOVEMBER, 1, MONDAY )
    result.replace( day = result.day + 1 )

    return RPNDateTime( *result.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  calculateMemorialDay
#
#  the last Monday in May (4th or 5th Monday)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateMemorialDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, MAY, -1, MONDAY )


#******************************************************************************
#
#  calculatePresidentsDay
#
#  the third Monday in February
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculatePresidentsDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, FEBRUARY, 3, MONDAY )


#******************************************************************************
#
#  calculateMartinLutherKingDay
#
#  the third Monday in January
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateMartinLutherKingDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, JANUARY, 3, MONDAY )


#******************************************************************************
#
#  calculateColumbusDay
#
#  the second Monday in October
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateColumbusDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, OCTOBER, 2, MONDAY )


#******************************************************************************
#
#  calculateMothersDay
#
#  the second Sunday in May (in the U.S. and most other countries)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateMothersDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, MAY, 2, SUNDAY )


#******************************************************************************
#
#  calculateFathersDay
#
#  the third Sunday in June (in the U.S. and most other countries)
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateFathersDay( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    return calculateNthWeekdayOfMonth( year, JUNE, 3, SUNDAY )


#******************************************************************************
#
#  getNewYearsDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getNewYearsDay( year ):
    return RPNDateTime( year, JANUARY, 1, dateOnly = True )


#******************************************************************************
#
#  getVeteransDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getVeteransDay( year ):
    return RPNDateTime( year, NOVEMBER, 11, dateOnly = True )


#******************************************************************************
#
#  getIndependenceDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getIndependenceDay( year ):
    return RPNDateTime( year, JULY, 4, dateOnly = True )


#******************************************************************************
#
#  getChristmasDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getChristmasDay( year ):
    return RPNDateTime( year, DECEMBER, 25, dateOnly = True )


#******************************************************************************
#
#  calculateAdvent
#
#  4 Sundays before Christmas
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateAdvent( year ):
    firstAdvent = getChristmasDay( year ).add( RPNMeasurement( -3, 'week' ) )
    firstAdvent = firstAdvent.subtract( RPNMeasurement( getWeekday( firstAdvent ), 'day'  ) )

    return RPNDateTime( *firstAdvent.getYMD( ), dateOnly = True )


#******************************************************************************
#
#  getEpiphanyDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def getEpiphanyDay( year ):
    return RPNDateTime( year, 1, 6, dateOnly = True )


#******************************************************************************
#
#  calculatePentecostSunday
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculatePentecostSunday( year ):
    return RPNDateTime( *( calculateEaster( year ).add( RPNMeasurement( 7, 'weeks' ) ).getYMD( ) ),
                        dateOnly = True )


#******************************************************************************
#
#  calculateAscensionThursday
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateAscensionThursday( year ):
    '''
I don't know why it's 39 days after Easter instead of 40, but that's how
the math works out.  It's the 40th day of the Easter season.

Or as John Wright says, "Catholics can't count.  I think it stems from the
Church being created before the number 0.
    '''
    return RPNDateTime( *calculateEaster( year ).add( RPNMeasurement( 39, 'days' ) ).getYMD( ),
                        dateOnly = True )


#******************************************************************************
#
#  calculateDSTStart
#
#  the second Sunday in March
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateDSTStart( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, MARCH, 2, SUNDAY )
    elif year == 1974:
        return RPNDateTime( 1974, JANUARY, 7, dateOnly = True )
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, APRIL, 1, SUNDAY )
    else:
        raise ValueError( 'DST was not standardized before 1967' )


#******************************************************************************
#
#  calculateDSTEnd
#
#  the first Sunday in November
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ IntValidator( ) ] )
def calculateDSTEnd( year ):
    if isinstance( year, RPNDateTime ):
        year = year.year

    if year >= 2007:
        return calculateNthWeekdayOfMonth( year, NOVEMBER, 1, SUNDAY )
    elif year == 1974:
        return RPNDateTime( 1974, DECEMBER, 31, dateOnly = True )  # technically DST never ended in 1974
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, OCTOBER, -1, SUNDAY )
    else:
        raise ValueError( 'DST was not standardized before 1967' )


#******************************************************************************
#
#  getISODay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getISODay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return list( n.isocalendar( ) )


#******************************************************************************
#
#  getWeekday
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getWeekday( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.weekday( ) + 1


#******************************************************************************
#
#  getWeekdayName
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getWeekdayName( n ):
    return calendar.day_name[ getWeekday( n ) - 1 ]


#******************************************************************************
#
#  getYear
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getYear( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.year


#******************************************************************************
#
#  getMonth
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getMonth( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.month


#******************************************************************************
#
#  getDay
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getDay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.day


#******************************************************************************
#
#  getHour
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getHour( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.hour


#******************************************************************************
#
#  getMinute
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getMinute( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.minute


#******************************************************************************
#
#  getSecond
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getSecond( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'date/time type required for this operator' )

    return n.second + n.microsecond / 1000000


#******************************************************************************
#
#  isDST
#
#******************************************************************************

def isDST( dateTime, timeZone ):
    return dateTime.astimezone( timeZone ).dst( ) != datetime.timedelta( 0 )
