#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnKeyboard.py
# //
# //  RPN command-line calculator utility functions
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import signal
import sys


# //******************************************************************************
# //
# //  class DelayedKeyboardInterrupt
# //
# //  http://stackoverflow.com/questions/842557/how-to-prevent-a-block-of-code-from-being-interrupted-by-keyboardinterrupt-in-py
# //
# //******************************************************************************

class DelayedKeyboardInterrupt( object ):
    '''This class is used to mask keyboard interrupts.'''
    def __enter__( self ):
        self.signal_received = False
        self.old_handler = signal.getsignal( signal.SIGINT )
        signal.signal( signal.SIGINT, self.handler )

    def handler( self, signal, frame ):
        self.signal_received = ( signal, frame )

    def __exit__( self, type, value, traceback ):
        signal.signal( signal.SIGINT, self.old_handler )

        if self.signal_received:
            self.old_handler( *self.signal_received )


