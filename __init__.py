#!/usr/bin/env python

# //******************************************************************************
# //
# //  __init__.py
# //
# //  RPN command-line calculator
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

__all__ = [ "rpn" ]

from rpn import makeHelp
from rpn import makeUnits
from rpn import preparePrimeData
from rpn import pyecm
from rpn import rpn
from rpn import rpnAliases
from rpn import rpnAstronomy
from rpn import rpnBase
from rpn import rpnCalendar
from rpn import rpnChemistry
from rpn import rpnCombinatorics
from rpn import rpnComputer
from rpn import rpnConstants
from rpn import rpnConstantUtils
from rpn import rpnDateTime
from rpn import rpnDeclarations
from rpn import rpnDice
from rpn import rpnEstimates
from rpn import rpnFactor
from rpn import rpnGenerator
from rpn import rpnGeometry
from rpn import rpnGlobals
from rpn import rpnInput
from rpn import rpnLexicographic
from rpn import rpnList
from rpn import rpnLocation
from rpn import rpnMath
from rpn import rpnMeasurement
from rpn import rpnModifiers
from rpn import rpnName
from rpn import rpnNumberTheory
from rpn import rpnOperators
from rpn import rpnOutput
from rpn import rpnPersistence
from rpn import rpnPhysics
from rpn import rpnPolynomials
from rpn import rpnPolytope
from rpn import rpnPrimes
from rpn import rpnPrimeUtils
from rpn import rpnSettings
from rpn import rpnTestUtils
from rpn import rpnUnitClasses
from rpn import rpnUnits
from rpn import rpnUtils
from rpn import rpnVersion
from rpn import testConvert
from rpn import testHelp
from rpn import testRPN

__version__ = PROGRAM_VERSION

__all__ = [
    'makeHelp', 'makeUnits', 'preparePrimeData', 'rpn', 'testRPN',
]

