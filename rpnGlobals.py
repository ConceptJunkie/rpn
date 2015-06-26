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

# general globals

dataPath = ''

# constants

phiBase = -1
fibBase = -2

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

# unit data

basicUnitTypes = { }
operatorAliases = { }
unitConversionMatrix = { }
unitOperators = { }
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
factorCache = None

