#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnRational.py
# //
# //  RPN command-line calculator, rational value class
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from fractions import Fraction


# //******************************************************************************
# //
# //  class RPNRational
# //
# //  Maybe I'll get around to implementing this some day.
# //
# //******************************************************************************

class RPNRational( Fraction ):
    '''This class represents a rational value.  It is derived from
    fractions.Fraction, but has support for dealing with mpf, etc..'''

    def __init__( self, value ):
        self = value

    def __eq__( self, other ):
        return Fraction.__eq__( other )

    def __ne__( self, other ):
        return __ne__( self, other )

