#!/usr/bin/env python

#******************************************************************************
#
#  rpnNanoseconds
#
#  nanosecond-resolution timer for Python <= 3.6 on Linux
#  copyright (c) 2021, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import ctypes


#******************************************************************************
#
#  time_ns
#
#  https://stackoverflow.com/questions/55774054/precise-time-in-nano-seconds-for-python-3-6-and-earlier
#
#  This is a Linux-specific implementation, but I've never needed this for
#  Windows since I can always control what version of Python I am running.
#
#******************************************************************************

CLOCK_REALTIME = 0


class TimeSpec( ctypes.Structure ):
    _fields_ = [
        ( 'tv_sec', ctypes.c_int64 ),   # seconds, https://stackoverflow.com/q/471248/1672565
        ( 'tv_nsec', ctypes.c_int64 ),   # nanoseconds
    ]


clock_gettime = ctypes.cdll.LoadLibrary( 'libc.so.6' ).clock_gettime
clock_gettime.argtypes = [ ctypes.c_int64, ctypes.POINTER( TimeSpec ) ]
clock_gettime.restype = ctypes.c_int64


def time_ns( ):
    timespec = TimeSpec( )
    ret = clock_gettime( CLOCK_REALTIME, ctypes.pointer( timespec ) )

    if bool( ret ):
        raise OSError( )

    return timespec.tv_sec * 1_000_000_000 + timespec.tv_nsec
