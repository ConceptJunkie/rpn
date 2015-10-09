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
from mpmath import ceil

from rpnDateTime import RPNDateTime
from rpnName import getOrdinalName


# //******************************************************************************
# //
# //  calendar names
# //
# //******************************************************************************

bahaiYears = [
    'Alif',
    'Ba\'',
    'Ab',
    'Dal',
    'Bab',
    'Vav',
    'Abad',
    'Jad',
    'Baha\'',
    'Hubb',
    'Bahhaj',
    'Javab',
    'Ahad',
    'Vahhab',
    'Vidad',
    'Badi`',
    'Bahi',
    'Abha',
    'Vahid',
]

bahaiMonths = [
    'Baha',
    'Jalal',
    'Jamal',
    '`Azamat',
    'Nur',
    'Rahmat',
    'Kalimat',
    'Kamal',
    'Asma\'',
    '`Izzat',
    'Mashiyyat',
    '`Ilm',
    'Qudrat',
    'Qawl',
    'Masa\'il',
    'Sharaf',
    'Sultan',
    'Mulk',
    'Ayyam-i-Ha',
    '`Ala\''
]

bahaiDays = [
    'Kamal',     # Monday
    'Fidal',
    '`Idal',
    'Istijlal',
    'Istiqlal',
    'Jalal',
    'Jamal'
]

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
    'Yom Shabbat',
    'Yom Rishon'
]

indianCivilDays = (
    "Somavara",     # Monday
    "Mangalavara",
    "Budhavara",
    "Guruvara",
    "Sukravara",
    "Sanivara",
    "Ravivara",
)

indianCivilMonths = (
    "Chaitra",
    "Vaishakha",
    "Jyeshtha",
    "Ashadha",
    "Shravana",
    "Bhaadra",
    "Ashwin",
    "Kartika",
    "Agrahayana",
    "Pausha",
    "Magha",
    "Phalguna",
)

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
# //  getJulianDay
# //
# //******************************************************************************

def getJulianDay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    return gregorian.to_jd( n.year, n.month, n.day )


# //******************************************************************************
# //
# //  getLilianDay
# //
# //******************************************************************************

def getLilianDay( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    return ceil( n.subtract( RPNDateTime( 1582, 10, 15 ) ) )


# //******************************************************************************
# //
# //  getISODate
# //
# //******************************************************************************

def getISODate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'a date-time type required for this operator' )

    result = n.isocalendar( )

    return list( result )


# //******************************************************************************
# //
# //  getISODateName
# //
# //******************************************************************************

def getISODateName( n ):
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
# //  convertHebrewDate
# //
# //******************************************************************************

def convertHebrewDate( year, month, day ):
    return RPNDateTime( *hebrew.to_gregorian( int( year ), int( month ), int( day ) ) )


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
# //  getIndianCivilCalendarDate
# //
# //******************************************************************************

def getIndianCivilCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( indian_civil.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  convertIndianCivilDate
# //
# //******************************************************************************

def convertIndianCivilDate( year, month, day ):
    return RPNDateTime( *indian_civil.to_gregorian( int( year ), int( month ), int( day ) ) )


# //******************************************************************************
# //
# //  getIndianCivilCalendarDateName
# //
# //******************************************************************************

def getIndianCivilCalendarDateName( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    date = indian_civil.from_gregorian( n.year, n.month, n.day )

    return indianCivilDays[ n.weekday( ) ] + ', ' + indianCivilMonths[ date[ 1 ] - 1 ] + \
           ' ' + str( date[ 2 ] ) + ', ' + str( date[ 0 ] )


# //******************************************************************************
# //
# //  getMayanCalendarDate
# //
# //******************************************************************************

def getMayanCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( mayan.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  convertMayanDate
# //
# //******************************************************************************

def convertMayanDate( baktun, katun, tun, uinal, kin ):
    return RPNDateTime( *mayan.to_gregorian( int( baktun ), int( katun ), int( tun ), \
                        int( uinal ), int( kin ) ) )


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
# //  convertIslamicDate
# //
# //******************************************************************************

def convertIslamicDate( year, month, day ):
    return RPNDateTime( *islamic.to_gregorian( int( year ), int( month ), int( day ) ) )


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
# //  convertJulianDate
# //
# //******************************************************************************

def convertJulianDate( year, month, day ):
    return RPNDateTime( *julian.to_gregorian( int( year ), int( month ), int( day ) ) )


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
# //  convertPersianDate
# //
# //******************************************************************************

def convertPersianDate( year, month, day ):
    return RPNDateTime( *persian.to_gregorian( int( year ), int( month ), int( day ) ) )


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


# //******************************************************************************
# //
# //  getBahaiCalendarDate
# //
# //******************************************************************************

def getBahaiCalendarDate( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    return list( bahai.from_gregorian( n.year, n.month, n.day ) )


# //******************************************************************************
# //
# //  convertBahaiDate
# //
# //******************************************************************************

def convertBahaiDate( year, month, day ):
    return RPNDateTime( *bahai.to_gregorian( int( year ), int( month ), int( day ) ) )


# //******************************************************************************
# //
# //  getBahaiCalendarDateName
# //
# //******************************************************************************

def getBahaiCalendarDateName( n ):
    if not isinstance( n, RPNDateTime ):
        raise ValueError( 'time type required for this operator' )

    date = bahai.from_gregorian( n.year, n.month, n.day )

    result = bahaiDays[ n.weekday( ) ] + ', ' + bahaiMonths[ date[ 1 ] - 1 ] + \
           ' ' + str( date[ 2 ] ) + ', '

    print( date )

    if date[ 0 ] >= 1:
        result += 'Year ' + bahaiYears[ date[ 0 ] % 19 - 1 ] + ' of the ' + \
                  getOrdinalName( ( date[ 0 ] / 19 ) + 1 ) + ' Vahid of the ' + \
                  getOrdinalName( ( date[ 0 ] / 361 ) + 1 ) + ' Kull-i-Shay\'' + \
                  ' (Year ' + str( date[ 0 ] ) + ')'
    else:
        result += str( date[ 0 ] )

    return result

