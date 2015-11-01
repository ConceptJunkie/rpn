#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnGlobals.py
# //
# //  RPN command-line calculator global declarations
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import six

# general globals

dataPath = ''
dataDir = 'rpndata'
ecm = True

# constants

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'

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

defaultOutputAccuracy = 12
defaultBitwiseGroupSize = 16
defaultCFTerms = 10
defaultDecimalDelimiter = ' '
defaultDecimalGrouping = 5
defaultInputRadix = 10
defaultIntegerGrouping = 3
defaultLineLength = 80
defaultListFormatLevel = 1
defaultOutputRadix = 10
defaultPrecision = 20

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# state variables

creatingFunction = False
helpLoaded = False
nestedListLevel = 0
duplicateOperations = 0
startTime = 0
useMembers = 0
operatorList = False
lastOperand = 0
operandsToRemove = 0
operatorsInList = 0

# options

bitwiseGroupSize = 0
comma = False
debugMode = False
decimalDelimiter = defaultDecimalDelimiter
decimalGrouping = 0
identify = False
inputRadix = defaultInputRadix
leadingZero = False
lineLength = defaultLineLength
listFormatLevel = 0
numerals = ''
outputAccuracy = -1
outputBaseDigits = False
outputRadix = defaultOutputRadix
tempCommaMode = False
tempHexMode = False
tempIdentifyMode = False
tempLeadingZeroMode = False
tempOctalMode = False
tempTimerMode = False
timer = False
verbose = False

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
minValueToCache = 1000000
factorCache = None

# location cache
locationCache = None

