#!/usr/bin/env python

#******************************************************************************
#
#  rpnGlobals.py
#
#  rpnChilada global declarations
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import sqlite3

from collections import MutableMapping
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
defaultPrecision = 20

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# state variables
astroDataLoaded = False         # Whether or not we've tried to load the astronomy data
astroDataAvailable = False      # If the astronomy data is available (i.e., It's there, _and_ we loaded it.)
checkForSingleResults = False   # This is set true for making help and unit tests, because those should always eturn single results
creatingFunction = False        # Whether we're in the process of creating a user-defined function
cwd = None
duplicateOperations = 0
echoArguments: List[ str ] = [ ]
helpLoaded = False
interactive = False
lastOperand = 0
nestedListLevel = 0
operandsToRemove = 0
operatorList = False            # whether we are in the process of creating an operator list (between '(' and ')' operators)
operatorsInList = 0
startTime = 0
testFilter = ''
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
maxToFactorByTrialDivision = 100000000  # 10,000 squared because we check all primes below 10,000
minValueForYAFU = defaultMinValueForYAFU
numerals = ''
outputAccuracy = -1
outputRadix = defaultOutputRadix
refreshOEISCache = False
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
helpTopics: Dict[ str, list ] = { }
helpVersion = '0.0.0'
operatorCategories: List[ str ] = [ ]
operatorHelp: Dict[ str, list ] = { }
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
planets = None
ephemeris = None
timescale = None

# constants
c = None
e = None
e0 = None
G = None
h = None
h_bar = None
k = None

