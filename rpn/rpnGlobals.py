#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnGlobals.py
# //
# //  RPN command-line calculator global declarations
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

# general globals
dataDir = 'rpndata'
ecm = True

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
defaultIntegerGrouping = 3
defaultLineLength = 80
defaultListFormatLevel = 1
defaultMinValueForYAFU = 1000000000000000000
defaultMaximumFixed = 5
defaultOutputAccuracy = 12
defaultOutputRadix = 10
defaultPrecision = 20

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# state variables
astroDataLoaded = False
creatingFunction = False
duplicateOperations = 0
echoArguments = [ ]
helpLoaded = False
interactive = False
lastOperand = 0
nestedListLevel = 0
operandsToRemove = 0
operatorList = False
operatorsInList = 0
startTime = 0
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
leadingZero = False
lineLength = defaultLineLength
listFormatLevel = 0
maximumFixed = defaultMaximumFixed
maxToFactorByTrialDivision = 100000000  # 10,000 squared because we check all primes below 10,000
minValueForYAFU = defaultMinValueForYAFU
numerals = ''
outputAccuracy = -1
outputRadix = defaultOutputRadix
tempCommaMode = False
tempHexMode = False
tempIdentifyMode = False
tempLeadingZeroMode = False
tempOctalMode = False
tempTimerMode = False
timeLimit = 0
timer = False
useYAFU = True
verbose = False
zhangConjecturesAllowed = False

# unit data
basicUnitTypes = { }
operatorAliases = { }
unitConversionMatrix = { }
unitOperators = { }
unitOperatorNames = [ ]
unitsVersion = "0.0.0"

# help data
helpTopics = { }
helpVersion = "0.0.0"
operatorCategories = [ ]
operatorHelp = { }
unitTypeDict = { }

# interactive mode
results = [ ]
variables = { }
promptCount = 0

# factor cache
minValueToCache = 100000
factorCache = None

# location cache
locationCache = None

# user-defined constants
constants = { }

# all keywords
keywords = [ ]

# operator caches
functionCaches = { }

# prime number data
databases = { }
cursors = { }

# chemistry tables
elements = None
atomic_numbers = None

# config
userVariables = { }
userVariablesAreDirty = False
userFunctions = { }
userFunctionsAreDirty = False
userConfiguration = { }
userConfigurationIsDirty = False

# astronomy data
planets = None
ephemeris = None
timescale = None

