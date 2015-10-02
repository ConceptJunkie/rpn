#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnCalendar.py
# //
# //  RPN command-line calculator calendar operators
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import arrow
import calendar
import datetime

from convertdate import *
from dateutil import tz

from rpnMeasurement import *
from rpnTime import *


# //******************************************************************************
# //
# //  calendar names
# //
# //******************************************************************************

hebrewMonths = [
    'Nisan',
    'Iyar',
    'Sivan',
    'Tammuz',
    'Av',
    'Elul',
    'Tishrei',
    'Marcheshvan',
    'Kislev',
    'Tevet',
    'Shevat',
    'Adar I',
    'Adar II'
]

hebrewDays = [
    'Yom Sheni',     # Monday
    'Yom Shlishi',
    'Yom Revi\'i',
    'Yom Chamishi',
    'Yom Shishi',
    'Yom Shabbat'
    'Yom Rishon'
]

islamicMonths = [
    'Muharram',
    'Safar',
    'Rabi al-Awwal',
    'Rabi ath-Thani',
    'Jumada al-Ula',
    'Jumada ath-Thaniyah',
    'Rajab',
    'Sha`ban',
    'Ramadan',
    'Shawwal',
    'Dhu al-Qa`dah',
    'Dhu al-Hijjah'
]

islamicDays = [
    'al-Ithnayn',   # Monday
    'ath-Thulatha',
    'al-Arbi`a',
    'al-Khamis',
    'al-Jumu`ah',
    'as-Sabt',
    'al-Ahad'
]

persianMonths = [
    'Farvardin',
    'Ordibehesht',
    'Khordad',
    'Tir',
    'Mordad',
    'Shahrivar',
    'Mehr',
    'Aban',
    'Azar',
    'Dey',
    'Bahman',
    'Esfand'
]

persianDays = [
    'Yekshanbeh',   # Monday
    'Doshanbeh',
    'Seshhanbeh',
    'Chaharshanbeh',
    'Panjshanbeh',
    'Jomeh',
    'Shanbeh'
]


# //******************************************************************************
# //
# //  getOrdinalDate
# //
# //******************************************************************************

def getOrdinalDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    return str( n.year ) + '-' + str( n.timetuple( ).tm_yday )


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
# //  getISODate
# //
# //******************************************************************************

def getISODate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    result = n.isocalendar( )

    return str( result[ 0 ] ) + '-W' + str( result[ 1 ] ) + '-' + str( result[ 2 ] )


# //******************************************************************************
# //
# //  getHebrewCalendarDate
# //
# //******************************************************************************

def getHebrewCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( hebrew.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  getHebrewCalendarDateName
# //
# //******************************************************************************

def getHebrewCalendarDateName( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    date = hebrew.from_gregorian( n.year, n.month, n.day )

    return hebrewDays[ n.weekday( ) ] + ', ' + hebrewMonths[ date[ 1 ] - 1 ] + \
           ' ' + str( date[ 2 ] ) + ', ' + str( date[ 0 ] )


# //******************************************************************************
# //
# //  getIslamicCalendarDate
# //
# //******************************************************************************

def getIslamicCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( islamic.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  getIslamicCalendarDateName
# //
# //******************************************************************************

def getIslamicCalendarDateName( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    date = islamic.from_gregorian( n.year, n.month, n.day )

    return islamicDays[ n.weekday( ) ] + ', ' + islamicMonths[ date[ 1 ] - 1 ] + \
           ' ' + str( date[ 2 ] ) + ', ' + str( date[ 0 ] )


# //******************************************************************************
# //
# //  getJulianCalendarDate
# //
# //******************************************************************************

def getJulianCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( julian.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  getPersianCalendarDate
# //
# //******************************************************************************

def getPersianCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( persian.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  getPersianCalendarDateName
# //
# //******************************************************************************

def getPersianCalendarDateName( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    date = persian.from_gregorian( n.year, n.month, n.day )

    return persianDays[ n.weekday( ) ] + ', ' + persianMonths[ date[ 1 ] - 1 ] + \
           ' ' + str( date[ 2 ] ) + ', ' + str( date[ 0 ] )

