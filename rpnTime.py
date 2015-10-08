#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnTime.py
# //
# //  RPN command-line calculator time operations
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import arrow
import datetime

from rpnMeasurement import *
from rpnUtils import *

from rpnDeclarations import RPNDateTime


#//******************************************************************************
#//
#//  convertToUnixTime
#//
#//******************************************************************************

def convertToUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( n ).timestamp
    except OverflowError as error:
        print( 'rpn:  out of range error for \'to_unix_time\'' )
        return 0
    except TypeError as error:
        print( 'rpn:  expected time value for \'to_unix_time\'' )
        return 0

    return result


#//******************************************************************************
#//
#//  convertFromUnixTime
#//
#//******************************************************************************

def convertFromUnixTime( n ):
    try:
        result = RPNDateTime.parseDateTime( n )
    except OverflowError as error:
        print( 'rpn:  out of range error for \'from_unix_time\'' )
        return 0
    except TypeError as error:
        print( 'rpn:  expected time value for \'from_unix_time\'' )
        return 0

    return result


#//******************************************************************************
#//
#//  convertToHMS
#//
#//******************************************************************************

def convertToHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToDHMS
#//
#//******************************************************************************

def convertToDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'day' : 1 } ), Measurement( 1, { 'hour' : 1 } ),
                              Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  convertToYDHMS
#//
#//******************************************************************************

def convertToYDHMS( n ):
    return convertUnits( n, [ Measurement( 1, { 'year' : 1 } ), Measurement( 1, { 'day' : 1 } ),
                              Measurement( 1, { 'hour' : 1 } ), Measurement( 1, { 'minute' : 1 } ),
                              Measurement( 1, { 'second' : 1 } ) ] )


#//******************************************************************************
#//
#//  makeJulianTime
#//
#//******************************************************************************

def makeJulianTime( n ):
    if len( n ) == 1:
        return RPNDateTime( n[ 0 ], 1, 1 )

    result = RPNDateTime( n[ 0 ], 1, 1 ).add( Measurement( n[ 1 ] - 1, 'day' ) )

    if len( n ) >= 3:
        result = result.replace( hour = n[ 2 ] )

    if len( n ) >= 4:
        result = result.replace( minute = n[ 3 ] )

    if len( n ) >= 5:
        result = result.replace( second = n[ 4 ] )

    if len( n ) >= 6:
        result = result.replace( microsecond = n[ 5 ] )

    return result


#//******************************************************************************
#//
#//  makeISOTime
#//
#//******************************************************************************

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


