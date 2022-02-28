#!/usr/bin/env python

#******************************************************************************
#
#  rpnVersion.py
#
#  rpnChilada version identification
#  copyright (c) 2022, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

#******************************************************************************
#
#  version variable initialization
#
#******************************************************************************

PROGRAM_NAME = 'rpnChilada'
PROGRAM_VERSION = '8.5.991'
PROGRAM_VERSION_NAME = '8.6.beta1'
COPYRIGHT_MESSAGE = 'copyright (c) 2021 (1988), Rick Gutleber (rickg@his.com)'

if PROGRAM_VERSION != PROGRAM_VERSION_NAME:
    PROGRAM_VERSION_STRING = ' ' + PROGRAM_VERSION + ' (' + PROGRAM_VERSION_NAME + ')'
else:
    PROGRAM_VERSION_STRING = ' ' + PROGRAM_VERSION

RPN_PROGRAM_NAME = PROGRAM_NAME + PROGRAM_VERSION_STRING

PROGRAM_DESCRIPTION = 'RPN command-line calculator'
