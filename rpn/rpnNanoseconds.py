#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnNanoseconds
# //
# //  nanosecond-resolution timer for Python <= 3.6
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import ctypes


# //******************************************************************************
# //
# //  time_ns
# //
# //  https://stackoverflow.com/questions/55774054/precise-time-in-nano-seconds-for-python-3-6-and-earlier
# //
# //******************************************************************************

CLOCK_REALTIME = 0

class timespec( ctypes.Structure ):
    _fields_ = [
        ( 'tv_sec', ctypes.c_int64 ), # seconds, https://stackoverflow.com/q/471248/1672565
        ( 'tv_nsec', ctypes.c_int64 ), # nanoseconds
        ]

clock_gettime = ctypes.cdll.LoadLibrary( 'libc.so.6' ).clock_gettime
clock_gettime.argtypes = [ ctypes.c_int64, ctypes.POINTER( timespec ) ]
clock_gettime.restype = ctypes.c_int64

def time_ns( ):
    tmp = timespec( )
    ret = clock_gettime( CLOCK_REALTIME, ctypes.pointer( tmp ) )

    if bool( ret ):
        raise OSError( )

    return tmp.tv_sec * 10 ** 9 + tmp.tv_nsec

