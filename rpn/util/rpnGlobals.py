#!/usr/bin/env python

#******************************************************************************
#
#  rpnGlobals.py
#
#  rpnChilada global declarations
#  copyright (c) 2025, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import sqlite3

from collections.abc import MutableMapping
from typing import Dict, List
# pylint: disable=invalid-name

from mpmath import mpf

# general globals
dataDir = 'rpndata'

# base identifiers
phiBase = -1
fibBase = -2
facBase = -3
doublefacBase = -4
squareBase = -5
lucasBase = -6
triangularBase = -7
primorialBase = -8
eBase = -9
piBase = -10
sqrt2Base = -11

maxSpecialBase = -11

# default options
defaultBitwiseGroupSize = 16
defaultCFTerms = 10
defaultDecimalDelimiter = ' '
defaultDecimalGrouping = 5
defaultInputRadix = 10
defaultIntegerDelimiter = ','
defaultIntegerGrouping = 3
defaultLineLength = 80
defaultListFormatLevel = 1
defaultMinValueForYAFU = 1_000_000_000_000_000_000
defaultMaximumFixed = 5
defaultOutputAccuracy = 12
defaultOutputRadix = 10
defaultPrecision = -1

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# state variables
astroDataLoaded = False         # Whether or not we've tried to load the astronomy data
astroDataAvailable = False      # If the astronomy data is available (i.e., It's there, _and_ we loaded it.)
checkForSingleResults = False   # This is for making help and unit tests, because those always return single results
creatingFunction = False        # Whether we're in the process of creating a user-defined function
cwd = None
duplicateOperations = 0
echoArguments: List[ str ] = [ ]
helpLoaded = False
interactive = False
lastOperand = 0
nestedListLevel = 0
operandsToRemove = 0
operatorList = False            # whether we are in the process of creating an operator list
operatorsInList = 0
slowTests = False
startTime = 0
testFilter = ''
testWithYafu = False
useMembers = 0

# options
bitwiseGroupSize = 0
comma = False
debugMode = False
decimalDelimiter = defaultDecimalDelimiter
decimalGrouping = 0
echo_command = False
identify = False
ignoreCache = False
inputRadix = defaultInputRadix
integerDelimiter = defaultIntegerDelimiter
integerGrouping = defaultIntegerGrouping
leadingZero = False
lineLength = defaultLineLength
listFormatLevel = 0
maximumFixed = defaultMaximumFixed
maxToFactorByTrialDivision = 100_000_000  # 10,000 squared because we check all primes below 10,000
minValueForYAFU = defaultMinValueForYAFU
numerals = ''
outputPrecision = -1
outputRadix = defaultOutputRadix
refreshOEISCache = False
showTimeZones = False
tempCommaMode = False
tempHexMode = False
tempIdentifyMode = False
tempLeadingZeroMode = False
tempOctalMode = False
tempTimerMode = False
timeIndividualTests = False
timeLimit = 0
timer = False
useYAFU = True
verbose = False
zhangConjecturesAllowed = False

# internal constants
unitConversionPrecision = 50

# unit data
basicUnitTypes: Dict[ str, list ] = { }
constantOperators: Dict[ str, list ] = { }
constantOperatorNames: List[ str ] = [ ]
aliases: Dict[ str, str ] = { }
unitConversionMatrix: Dict[ tuple, mpf ] = { }
unitOperators: Dict[ str, list ] = { }
unitOperatorNames: List[ str ] = [ ]

# help data
EXAMPLE_COUNT = 0
HELP_TOPICS: Dict[ str, list ] = { }
helpVersion = '0.0.0'
operatorCategories: List[ str ] = [ ]
OPERATOR_HELP: Dict[ str, list ] = { }
unitTypeDict: Dict[ str, list ] = { }

# interactive mode
results: List[ mpf ] = [ ]
variables: Dict[ str, str ] = { }
promptCount = 0

# factor cache
minValueToCache = 100000
factorCache = None

# location cache
locationCache = None

# user-defined constants
constants: Dict[ str, list ] = { }

# all keywords
keywords: List[ str ] = [ ]

# operator caches
functionCaches: Dict[ str, MutableMapping ] = { }

# prime number data
databases: Dict[ str, sqlite3.Connection ] = { }
cursors: Dict[ str, sqlite3.Cursor ] = { }
primeDataAvailable = False

# chemistry tables
elements = None
atomic_numbers = None

# config
userVariables: Dict[ str, str ] = { }
userVariablesAreDirty = False
userFunctions: Dict[ str, str ] = { }
userFunctionsAreDirty = False
userConfiguration: Dict[ str, str ] = { }
userConfigurationIsDirty = False

# astronomy data
ephemeris = None
timescale = None

# timezonefinder
timeZoneFinder = None

# constants
c = None
e = None
e0 = None
G = None
h = None
h_bar = None
k = None

