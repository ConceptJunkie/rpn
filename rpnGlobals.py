#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpnGlobals.py
#//
#//  RPN command-line calculator global declarations
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

# general globals

dataPath = ''

# constants

phiBase = -1
fibBase = -2

# default options

defaultAccuracy = 12
defaultBitwiseGroupSize = 16
defaultCFTerms = 10
defaultDecimalDelimiter = ' '
defaultDecimalGrouping = 5
defaultInputRadix = 10
defaultIntegerGrouping = 3
defaultLineLength = 80
defaultOutputRadix = 10
defaultPrecision = 20

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# state variables

creatingFunction = False
nestedListLevel = 0

# options

accuracy = -1
comma = False
outputBaseDigits = False
bitwiseGroupSize = 0
debugMode = False
decimalDelimiter = defaultDecimalDelimiter
decimalGrouping = 0
inputRadix = defaultInputRadix
leadingZero = False
lineLength = defaultLineLength
numerals = ''
outputRadix = defaultOutputRadix

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

