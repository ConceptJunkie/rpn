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


# //******************************************************************************
# //
# //  incrementMonths
# //
# //******************************************************************************

def incrementMonths( n, months ):
    newDay = n.day
    newMonth = n.month + int( months )
    newYear = n.year

    if newMonth < 1 or newMonth > 12:
        newYear += ( newMonth - 1 ) // 12
        newMonth = ( ( newMonth - 1 ) % 12 ) + 1

    maxDay = calendar.monthrange( newYear, newMonth )[ 1 ]

    if newDay > maxDay:
        newDay = maxDay

    return RPNDateTime( newYear, newMonth, newDay, n.hour, n.minute, n.second )


# //******************************************************************************
# //
# //  addTimes
# //
# //  arrow + measurement
# //
# //******************************************************************************

def addTimes( n, k ):
    if 'years' in g.unitOperators[ k.getUnitString( ) ].categories:
        years = convertUnits( k, 'year' ).getValue( )
        return n.replace( year = n.year + years )
    elif 'months' in g.unitOperators[ k.getUnitString( ) ].categories:
        months = convertUnits( k, 'month' ).getValue( )
        result = incrementMonths( n, months )
        return result
    else:
        days = int( floor( convertUnits( k, 'day' ).getValue( ) ) )
        seconds = int( fmod( floor( convertUnits( k, 'second' ).getValue( ) ), 86400 ) )
        microseconds = int( fmod( floor( convertUnits( k, 'microsecond' ).getValue( ) ), 1000000 ) )

        try:
            return n + datetime.timedelta( days = days, seconds = seconds, microseconds = microseconds )
        except OverflowError:
            print( 'rpn:  value is out of range to be converted into a time' )
            return 0


# //******************************************************************************
# //
# //  subtractTimes
# //
# //  arrow - measurement
# //
# //******************************************************************************

def subtractTimes( n, k ):
    if isinstance( k, Measurement ):
        kneg = Measurement( fneg( k.getValue( ) ), k.getUnits( ) )
        return addTimes( n, kneg )
    elif isinstance( k, RPNDateTime ):
        if n > k:
            delta = n - k
            factor = 1
        else:
            delta = k - n
            factor = -1

        if delta.days != 0:
            result = Measurement( delta.days * factor, 'day' )
            result = result.add( Measurement( delta.seconds * factor, 'second' ) )
            result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
        elif delta.seconds != 0:
            result = Measurement( delta.seconds * factor, 'second' )
            result = result.add( Measurement( delta.microseconds * factor, 'microsecond' ) )
        else:
            result = Measurement( delta.microseconds * factor, 'microsecond' )

        return result
    else:
        raise ValueError( 'incompatible type for subtracting from an absolute time' )


# //******************************************************************************
# //
# //  getNow
# //
# //******************************************************************************

def getNow( ):
    return RPNDateTime.now( )


# //******************************************************************************
# //
# //  getToday
# //
# //******************************************************************************

def getToday( ):
    now = datetime.datetime.now( )
    return RPNDateTime( now.year, now.month, now.day, dateOnly = True )


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
        raise ValueError( 'a time type required for this operator' )

    return n.timetuple( ).tm_yday


# //******************************************************************************
# //
# //  getJulianWeekFromDate
# //
# //******************************************************************************

def getJulianWeekFromDate( date ):
    pass


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
    if weekday > 7 or weekday < 1:
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

    return calculateNthWeekdayOfMonth( year, 11, 4, 4 )


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

    result = calculateNthWeekdayOfMonth( year, 11, 1, 1 )
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

    return calculateNthWeekdayOfMonth( year, 5, -1, 1 )


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

    return calculateNthWeekdayOfMonth( year, 2, 3, 1 )


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
        return calculateNthWeekdayOfMonth( year, 3, 2, 7 )
    elif year == 1974:
        return RPNDateTime( 1974, 1, 7, dateOnly = True )
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, 4, 1, 7 )
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
        return calculateNthWeekdayOfMonth( year, 11, 1, 7 )
    elif year == 1974:
        return RPNDateTime( 1974, 12, 31, dateOnly = True )  # technically DST never ended in 1974
    elif year >= 1967:
        return calculateNthWeekdayOfMonth( year, 10, -1, 7 )
    else:
        raise ValueError( 'DST was not standardized before 1967' )


# //******************************************************************************
# //
# //  generateMonthCalendar
# //
# //******************************************************************************

def generateMonthCalendar( n ):
    cal = calendar.TextCalendar( firstweekday = 6 )

    if isinstance( n[ 0 ], RPNDateTime ):
        cal.prmonth( n[ 0 ].year, n[ 0 ].month )
    elif len( n ) >= 2:
        cal.prmonth( int( n[ 0 ] ), int( n[ 1 ] ) )
    else:
        raise ValueError( 'this operator requires at least 2 items in the list' )

    print( )

    return n


# //******************************************************************************
# //
# //  generateYearCalendar
# //
# //******************************************************************************

def generateYearCalendar( n ):
    cal = calendar.TextCalendar( firstweekday = 6 )

    if isinstance( n, RPNDateTime ):
        cal.pryear( n.year )
    else:
        cal.pryear( n )

    print( )

    return n


# //******************************************************************************
# //
# //  convertToUnixTime
# //
# //******************************************************************************

def convertToUnixTime( n ):
    try:
        result = n.timestamp
    except OverflowError:
        print( 'rpn:  out of range error for \'to_unix_time\'' )
        return 0
    except TypeError:
        print( 'rpn:  expected time value for \'to_unix_time\'' )
        return 0

    return result


# //******************************************************************************
# //
# //  convertToHMS
# //
# //******************************************************************************

def convertToHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  convertToDHMS
# //
# //******************************************************************************

def convertToDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'day' : 1 } ), Measurement( 1, { 'hour' : 1 } ),
                              Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  convertToYDHMS
# //
# //******************************************************************************

def convertToYDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'year' : 1 } ), Measurement( 1, { 'day' : 1 } ),
                              Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


# //******************************************************************************
# //
# //  makeJulianTime
# //
# //******************************************************************************

def makeJulianTime( n ):
    if len( n ) == 1:
        return RPNDateTime( n[ 0 ], 1, 1, dateOnly = True  )

    result = addTimes( RPNDateTime( n[ 0 ], 1, 1 ), Measurement( n[ 1 ] - 1, 'day' ) )

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
    if len( n ) == 1:
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

    result = datetime.datetime.strptime( '%04d-%02d-%1d' % ( year, week, day ), '%Y-%W-%w' )

    if RPNDateTime( year, 1, 4 ).isoweekday( ) > 4:
        result -= datetime.timedelta( days = 7 )

    return result


# //******************************************************************************
# //
# //  makeTime
# //
# //******************************************************************************

def makeTime( n ):
    if isinstance( n, str ):
        return RPNDateTime.get( n )

    if len( n ) == 1:
        n.append( 1 )

    if len( n ) == 2:
        n.append( 1 )
    elif len( n ) > 7:
        n = n[ : 7 ]

    return RPNDateTime( *n )


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
# //  getWeekDay
# //
# //******************************************************************************

def getWeekday( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return calendar.day_name[ n.weekday( ) ]


