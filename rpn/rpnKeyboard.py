#!/usr/bin/env python

#******************************************************************************
#
#  rpnKeyboard.py
#
#  rpnChilada keyboard utility functions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import signal


#******************************************************************************
#
#  class DelayedKeyboardInterrupt
#
#  http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-\
#      being-interrupted-by-keyboardinterrupt-in-py
#
#******************************************************************************

class DelayedKeyboardInterrupt( ):
    '''This class is used to mask keyboard interrupts.'''
    def __init__( self ):
        self.signalReceived = False
        self.oldHandler = None

    def __enter__( self ):
        self.signalReceived = False
        self.oldHandler = signal.getsignal( signal.SIGINT )
        signal.signal( signal.SIGINT, self.handler )

    def handler( self, signalType, frame ):
        self.signalReceived = ( signalType, frame )

    def __exit__( self, signalType, value, traceback ):
        signal.signal( signal.SIGINT, self.oldHandler )

        if self.signalReceived:
            self.oldHandler( *self.signalReceived )
