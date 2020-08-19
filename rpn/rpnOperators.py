#!/usr/bin/env python

#******************************************************************************
#
#  rpnOperators.py
#
#  rpnChilada operator definitions
#  copyright (c) 2020, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

import configparser
import difflib
import inspect
import os
import string

from shutil import copyfile

import ephem

from mpmath import apery, arange, catalan, cplot, e, euler, fadd, fdiv, fib, fmul, glaisher, inf, khinchin, \
                   lambertw, limit, mertens, mpf, mpmathify, nprod, nsum, phi, pi, plot, power, splot, sqrt

from rpn.rpnAliases import dumpAliases
from rpn.rpnOperator import callers, RPNValidator, RPNOperator
from rpn.rpnOutput import printTitleScreen
from rpn.rpnVersion import PROGRAM_DESCRIPTION, PROGRAM_NAME, PROGRAM_VERSION

from rpn.rpnAstronomy import getAngularSeparation, getAngularSize, getAntitransitTime, getAutumnalEquinox, \
                             getNextAstronomicalDawn, getDayTime, getDistanceFromEarth, getEclipseTotality, \
                             getMoonPhase, getNextAntitransit, getNextAstronomicalDusk, getNextCivilDawn, \
                             getNextCivilDusk, getNextFirstQuarterMoon, getNextFullMoon, getNextLastQuarterMoon, \
                             getNextMoonAntitransit, getNextMoonRise, getNextMoonSet, getNextMoonTransit, \
                             getNextNauticalDawn, getNextNauticalDusk, getNextNewMoon, getNextRising, \
                             getNextSetting, getNextSunAntitransit, getNextSunrise, getNextSunset, getNextTransit, \
                             getNightTime, getPreviousAntitransit, getPreviousFirstQuarterMoon, \
                             getPreviousFullMoon, getPreviousLastQuarterMoon, getPreviousNewMoon, \
                             getPreviousRising, getPreviousSetting, getPreviousTransit, getSkyLocation, \
                             getSolarNoon, getSummerSolstice, getTransitTime, getVernalEquinox, getWinterSolstice, \
                             RPNAstronomicalObject

from rpn.rpnCalendar import convertBahaiDate, convertEthiopianDate, convertFrenchRepublicanDate, convertHebrewDate, \
                            convertIndianCivilDate, convertIslamicDate, convertJulianDate, convertMayanDate, \
                            convertPersianDate, generateMonthCalendar, generateYearCalendar, getBahaiCalendarDate, \
                            getBahaiCalendarDateName, getEthiopianCalendarDate, getEthiopianCalendarDateName, \
                            getFrenchRepublicanCalendarDate, getFrenchRepublicanCalendarDateName, \
                            getHebrewCalendarDate, getHebrewCalendarDateName, getIndianCivilCalendarDate, \
                            getIndianCivilCalendarDateName, getIslamicCalendarDate, getIslamicCalendarDateName, \
                            getISODate, getISODateName, getJulianCalendarDate, getJulianDay, getLilianDay, \
                            getMayanCalendarDate, getOrdinalDate, getPersianCalendarDate, \
                            getPersianCalendarDateName

from rpn.rpnChemistry import getAtomicNumber, getAtomicSymbol, getAtomicWeight, getElementBlock, \
                             getElementBoilingPoint, getElementDensity, getElementDescription, \
                             getElementGroup, getElementMeltingPoint, getElementName, getElementOccurrence, \
                             getElementPeriod, getElementState, getMolarMass

from rpn.rpnCombinatorics import countFrobenius, getArrangements, getBellPolynomial, getBinomial, \
                                 getCombinations, getCompositions, getDeBruijnSequence, getIntegerPartitions, \
                                 getLahNumber, getMultinomial, getNarayanaNumberOperator, getNthAperyNumber, \
                                 getNthBell, \
                                 getNthBernoulli, getNthCatalanNumber, getNthDelannoyNumber,getNthMenageNumber, \
                                 getNthMotzkinNumber, getNthMultifactorial, getNthPellNumber, getNthSchroederNumber, \
                                 getNthSchroederHipparchusNumber, getNthSylvesterNumber, getPartitionNumber, \
                                 getPartitionsWithLimit, getPermutations, getStirling1Number, getStirling2Number

from rpn.rpnComputer import andOperands, convertToChar, convertToDouble, convertToFloat, convertToLong, \
                            convertToLongLong, convertToQuadLong, convertToShort, convertToSignedIntOperator, \
                            convertToUnsignedChar, convertToUnsignedInt, convertToUnsignedLong, \
                            convertToUnsignedLongLong, convertToUnsignedQuadLong, convertToUnsignedShort, \
                            getBitCountOperator, getBitwiseAnd, getBitwiseNand, getBitwiseNor, getBitwiseOr, \
                            getBitwiseXnor, getBitwiseXor, getInvertedBits, getParity, nandOperands, orOperands, \
                            norOperands, notOperand, packInteger, shiftLeft, shiftRight, unpackInteger, xnorOperands, \
                            xorOperands

from rpn.rpnConstantUtils import getChampernowneConstant, getCopelandErdosConstant, getFaradayConstant, \
                                 getFineStructureConstant, getMillsConstant, getPlanckAcceleration, \
                                 getPlanckAngularFrequency, getPlanckArea, getPlanckCharge, getPlanckCurrent, \
                                 getPlanckDensity, getPlanckEnergy, getPlanckElectricalInductance, \
                                 getPlanckEnergyDensity, getPlanckForce, getPlanckImpedance, getPlanckIntensity, \
                                 getPlanckLength, getPlanckMagneticInductance, getPlanckMass, getPlanckMomentum, \
                                 getPlanckPower, getPlanckPressure, getPlanckTemperature, getPlanckTime, \
                                 getPlanckViscosity, getPlanckVoltage, getPlanckVolume, getPlanckVolumetricFlowRate, \
                                 getPlasticConstant, getRadiationConstant, getRobbinsConstant, \
                                 getStefanBoltzmannConstant, getThueMorseConstant, getVacuumImpedance, \
                                 getvonKlitzingConstant, interpretAsDouble, interpretAsFloat

from rpn.rpnDateTime import calculateAdvent, calculateAscensionThursday, calculateAshWednesday, calculateColumbusDay, \
                            calculateDSTEnd, calculateDSTStart, calculateEaster, calculateElectionDay, \
                            calculateFathersDay, calculateGoodFriday, calculateLaborDay, calculateMartinLutherKingDay, \
                            calculateMemorialDay, calculateMothersDay, calculateNthWeekdayOfMonthOperator, \
                            calculateNthWeekdayOfYear, calculatePentecostSunday, calculatePresidentsDay, \
                            calculateThanksgiving, convertFromUnixTime, convertToDHMS, convertToHMS, convertToYDHMS, \
                            convertToUnixTime, getChristmasDay, getDay, getEpiphanyDay, getHour, getIndependenceDay, \
                            getISODay, getMinute, getMonth, getNewYearsDay, getSecond, getToday, getTomorrow, \
                            getVeteransDay, getWeekday, getWeekdayName, getYear, getYesterday, makeDateTime, \
                            makeISOTime, makeJulianTime, RPNDateTime

from rpn.rpnDice import enumerateDiceGenerator, enumerateMultipleDiceGenerator, permuteDiceGenerator, rollDice, \
                        rollMultipleDiceGenerator, rollSimpleDice

from rpn.rpnDebug import debugPrint

from rpn.rpnFactor import getFactorsOperator

from rpn.rpnGenerator import RPNGenerator

from rpn.rpnGeometry import getAntiprismSurfaceArea, getAntiprismVolume, getConeSurfaceArea, getConeVolume, \
                            getDodecahedronSurfaceArea, getDodecahedronVolume, getIcosahedronSurfaceArea, \
                            getIcosahedronVolume, getKSphereSurfaceAreaOperator, getKSphereRadiusOperator, \
                            getKSphereVolumeOperator, getOctahedronSurfaceArea, getOctahedronVolume, \
                            getRegularPolygonAreaOperator, getPrismSurfaceArea, getPrismVolume, getSphereArea, \
                            getSphereRadius, getSphereVolume, getTetrahedronSurfaceArea, getTetrahedronVolume, \
                            getTorusSurfaceArea, getTorusVolume, getTriangleArea

from rpn.rpnInput import parseInputValue, readListFromFile

from rpn.rpnLexicographic import addDigits, buildNumbers, buildStepNumbers, combineDigits, containsAnyDigits, \
                                 containsDigits, containsOnlyDigits, countDifferentDigits, countDigits, \
                                 duplicateDigits, duplicateNumber, findPalindrome, generateSquareDigitChain, \
                                 getBaseKDigits, getCyclicPermutations, getDigitCount, getDigits, getErdosPersistence, \
                                 getPersistence, getKPersistence, getLeftDigits, getLeftTruncationsGenerator, \
                                 getNonzeroBaseKDigits, getNonzeroDigits, getNthReversalAddition, getRightDigits, \
                                 getRightTruncationsGenerator, isAutomorphic, isBaseKNarcissistic, isBaseKPandigital, \
                                 isBaseKSmithNumber, isBouncy, isDecreasing, isDigitalPermutation, \
                                 isGeneralizedDudeneyNumber, isHarshadNumber, isIncreasing, isKaprekarNumber, \
                                 isKMorphicOperator, isNarcissistic, isOrderKSmithNumber, isPalindromeOperator, \
                                 isPandigital, isPerfectDigitalInvariant, isPerfectDigitToDigitInvariant, \
                                 isSmithNumber, isStepNumber, isSumProductNumber, isTrimorphic, multiplyDigits, \
                                 multiplyDigitPowers, multiplyNonzeroDigitPowers, multiplyNonzeroDigits, \
                                 permuteDigits, replaceDigits, reverseDigitsOperator, rotateDigitsLeft, \
                                 rotateDigitsRight, showErdosPersistence, showKPersistence, showPersistence, sumDigits

from rpn.rpnList import alternateSigns, appendLists, calculateAntiharmonicMeanOperator, \
                        calculateArithmeticMeanOperator, calculateGeometricMeanOperator, \
                        calculateHarmonicMeanOperator, calculatePowerTower, calculatePowerTower2, \
                        calculateRootMeanSquare, collate, compareLists, countElements, doesListRepeat, \
                        enumerateList, equalsOneOf, filterMax, filterMin, filterOnFlags, findInList, flatten, \
                        getAlternatingSum, getAndAll, getCumulativeListDiffs, getCumulativeListProducts, \
                        getCumulativeListSums, getCumulativeListRatios, getCumulativeOccurrenceRatios, getDifference, \
                        getGCDOperator, getGCDOfList, getListCombinations, getListCombinationsWithRepeats, getLeft, \
                        getListDiffs, getListPowerset, getListRatios, getRight, getIndexOfMax, getIndexOfMin, \
                        getListElement, getListPermutations, getListPermutationsWithRepeats, getNandAll, \
                        getNonzeroes, getNorAll, getProduct, getOccurrences, getOccurrenceRatios, getOrAll, \
                        getRandomElement, getReverse, getSlice, getStandardDeviation, getSublist, getSum, \
                        getUniqueElements, getZeroes, groupElements, interleave, isPalindromeList, \
                        listAndOneArgFunctionEvaluator, makeIntersection, makeUnion, permuteLists, \
                        reduceListOperator, shuffleList, sortAscending, sortDescending

from rpn.rpnLocation import convertLatLongToNAC, getGeographicDistance, getLocation, getLocationInfo, \
                            getTimeZone, makeLocation

from rpn.rpnMath import addOperator, calculateHypotenuse, calculateNthHyperoperator, calculateNthRightHyperoperator, \
                        cube, decrement, exp, divideOperator, getAbsoluteValue, getAGM, getArgument, getCeiling, \
                        getConjugate, getCubeRoot, getCubeSuperRoot, getExp, getExp10, getExpPhi, getFloor, \
                        getImaginary, getLambertW, getLarger, getLI, getLog, getLog10, getLog2, getLogXY, \
                        getMantissa, getMaximum, getMinimum, getModulo, getNearestInt, getNegative, getPolyexp, \
                        getPolylog, getPowerOperator, getReal, getReciprocal, getRootOperator, getSign, getSmaller, \
                        getSquareRoot, getSquareSuperRoot, getSuperRoot, getSuperRoots, getValue, acosOperator, \
                        acotOperator, acothOperator, acoshOperator, acscOperator, acschOperator, asecOperator, \
                        asechOperator, asinOperator, asinhOperator, atanOperator, atanhOperator, cotOperator, \
                        cothOperator, cscOperator, cschOperator, cosOperator, coshOperator, secOperator, \
                        sechOperator, sinOperator, sinhOperator, tanOperator, tanhOperator, increment, \
                        isDivisibleOperator, isEqual, isEven, isGreater, isKthPower, isLess, isNotEqual, \
                        isNotGreater, isNotLess, isNotZero, isOdd, isPower, isSquare, isZero, multiplyOperator, \
                        roundByDigits, roundByValueOperator, roundOff, square, subtractOperator, tetrate, tetrateRight

from rpn.rpnMeasurement import applyNumberValueToUnit, convertToBaseUnits, convertToDMS, convertToPrimitiveUnits, \
                               convertUnits, estimate, getDimensions, invertUnits, RPNMeasurement, RPNUnits

from rpn.rpnModifiers import decrementNestedListLevel, duplicateOperation, duplicateTerm, endOperatorList, \
                             getPrevious, incrementNestedListLevel, startOperatorList, unlist

from rpn.rpnName import getName, getOrdinalName

from rpn.rpnNumberTheory import areRelativelyPrimeOperator, calculateAckermannFunctionOperator, \
                                calculateChineseRemainderTheorem, convertFromContinuedFraction, findNthSumOfCubes, \
                                findNthSumOfSquares, findSumsOfKNonzeroPowers, findSumsOfKPowers, \
                                generatePolydivisibles, getAbundanceOperator, getAbundanceRatio, getAliquotSequence, \
                                getAlternatingHarmonicFraction, getAltZeta, getBarnesG, getBeta, getCollatzSequence, \
                                getCyclotomic, getDigamma, getDigitalRoot, getDivisorCountOperator, \
                                getDivisorsOperator, getEulerPhi, getFrobeniusNumber, getGamma, \
                                getGeometricRecurrence, getHarmonicFraction, getHarmonicResidueOperator, \
                                getHurwitzZeta, getLCM, getLCMOfList, getLeylandNumber, getLimitedAliquotSequence, \
                                getLinearRecurrence, getLinearRecurrenceWithModulo, getLogGamma, \
                                getNthAlternatingFactorial, getGreedyEgyptianFraction, getNthBaseKRepunit, \
                                getNthCarolNumber, getNthDoubleFactorial, getNthCalkinWilf, getNthFactorial, \
                                getNthFibonacci, getNthFibonorial, getNthHarmonicNumber, getNthHeptanacci, \
                                getNthHexanacci, getNthHyperfactorial, getNthJacobsthalNumber, \
                                getNthKFibonacciNumber, getNthKThabitNumber, getNthKThabit2Number, getNthKyneaNumber, \
                                getNthLeonardoNumber, getNthLinearRecurrence, getNthLinearRecurrenceWithModulo, \
                                getNthLucasNumber, getNthMersenneExponent, getNthMersennePrime, getNthMerten, \
                                getNthMobiusNumberOperator, getNthPadovanNumber, getNthPhitorial, getNthOctanacci, \
                                getNthPascalLine, getNthPentanacci, getNthPerfectNumber, getNthKPolygorial, \
                                getNthSternNumberOperator, getNthSubfactorial, getNthSuperfactorial, \
                                getNthTetranacci, getNthThabitNumber, getNthThabit2Number, \
                                getNthThueMorseNumberOperator, getNthTribonacci, getNthZetaZero, getPolygamma, \
                                getPowModOperator, getPrimePi, getRadical, getSigmaKOperator, getSigmaOperator, \
                                getTrigamma, getUnitRoots, getZeta, interpretAsBaseOperator, interpretAsFraction, \
                                isAbundant, isAchillesNumber, isAntiharmonic, isCarmichaelNumberOperator, \
                                isDeficient, isFriendly, isHarmonicDivisorNumber, isInteger, isKHyperperfect, \
                                isKPerfect, isKSemiprimeOperator, isKSphenicOperator, isPerfect, isPernicious, \
                                isPolydivisible, isPowerful, isPronic, isRoughOperator, isRuthAaronNumber, \
                                isSemiprime, isSmoothOperator, isSphenic, isSquareFree, isUnusual, \
                                makeContinuedFraction, makeEulerBrick, makePythagoreanQuadruple, \
                                makePythagoreanTriple, makePythagoreanTriples, solveFrobeniusOperator

from rpn.rpnPersistence import dumpFunctionCache, dumpPrimeCache, getUserFunctionsFileName, loadConstants, \
                               loadResult, loadUnitConversionMatrix, loadUnitData

from rpn.rpnPhysics import calculateAcceleration, calculateBlackHoleEntropy, calculateBlackHoleLifetime, \
                           calculateBlackHoleLuminosity, calculateBlackHoleMass, calculateBlackHoleRadius, \
                           calculateBlackHoleSurfaceArea, calculateBlackHoleSurfaceGravity, \
                           calculateBlackHoleSurfaceTides, calculateBlackHoleTemperature, calculateDistance, \
                           calculateEnergyEquivalence, calculateEscapeVelocity, calculateHeatIndex, \
                           calculateHorizonDistance, calculateKineticEnergy, calculateMassEquivalence, \
                           calculateOrbitalMass, calculateOrbitalPeriod, calculateOrbitalRadius, \
                           calculateOrbitalVelocity, calculateSurfaceGravity, calculateTidalForce, \
                           calculateTimeDilation, calculateVelocity, calculateWindChill

from rpn.rpnPolynomials import addPolynomials, evaluatePolynomial, exponentiatePolynomial, getPolynomialDiscriminant, \
                               multiplyPolynomials, multiplyPolynomialList, solveCubicPolynomial, \
                               solveQuadraticPolynomial, solveQuarticPolynomial, solvePolynomial, sumPolynomialList

from rpn.rpnPolytope import findCenteredDecagonalNumber, findCenteredHeptagonalNumber, findCenteredHexagonalNumber, \
                            findCenteredNonagonalNumber, findCenteredOctagonalNumber, findCenteredPentagonalNumber, \
                            findCenteredPolygonalNumberOperator, findCenteredSquareNumber, \
                            findCenteredTriangularNumber, findDecagonalNumber, findHeptagonalNumber, \
                            findHexagonalNumber, findNonagonalNumber, findOctagonalNumber, findPentagonalNumber, \
                            findPolygonalNumberOperator, findSquareNumber, findTriangularNumber, \
                            getNthCenteredCubeNumber, getNthCenteredDecagonalNumber, \
                            getNthCenteredDodecahedralNumber, getNthCenteredHeptagonalNumber, \
                            getNthCenteredHexagonalNumber, getNthCenteredIcosahedralNumber, \
                            getNthCenteredNonagonalNumber, getNthCenteredOctagonalNumber, \
                            getNthCenteredOctahedralNumber, getNthCenteredPentagonalNumber, \
                            getNthCenteredPolygonalNumberOperator, getNthCenteredSquareNumber, \
                            getNthCenteredTetrahedralNumber, getNthCenteredTriangularNumber, \
                            getNthDecagonalCenteredSquareNumber, getNthDecagonalHeptagonalNumber, \
                            getNthDecagonalHexagonalNumber, getNthDecagonalNonagonalNumber, \
                            getNthDecagonalNumber, getNthDecagonalOctagonalNumber, \
                            getNthDecagonalPentagonalNumber, getNthDecagonalTriangularNumber, \
                            getNthDodecahedralNumber, getNthGeneralizedPentagonalNumber, \
                            getNthHeptagonalHexagonalNumber, getNthHeptagonalNumber, getNthHeptagonalPentagonalNumber, \
                            getNthHeptagonalSquareNumber, getNthHeptagonalTriangularNumber, getNthHexagonalNumber, \
                            getNthHexagonalPentagonalNumber, getNthHexagonalSquareNumber, getNthIcosahedralNumber, \
                            getNthNonagonalHeptagonalNumber, getNthNonagonalHexagonalNumber, getNthNonagonalNumber, \
                            getNthNonagonalOctagonalNumber, getNthNonagonalPentagonalNumber, \
                            getNthNonagonalSquareNumber, getNthNonagonalTriangularNumber, \
                            getNthOctagonalHeptagonalNumber, getNthOctagonalHexagonalNumber, getNthOctagonalNumber, \
                            getNthOctagonalPentagonalNumber, getNthOctagonalSquareNumber, \
                            getNthOctagonalTriangularNumber, getNthTruncatedOctahedralNumber, getNthOctahedralNumber, \
                            getNthPentagonalNumber, getNthPentagonalSquareNumber, getNthPentagonalTriangularNumber, \
                            getNthPentatopeNumber, getNthPolygonalNumberOperator, getNthPolygonalPyramidalNumber, \
                            getNthPolytopeNumber, getNthPyramidalNumber, getNthRhombicDodecahedralNumber, \
                            getNthSquareTriangularNumber, getNthStarNumber, getNthStellaOctangulaNumber, \
                            getNthTetrahedralNumber, getNthTruncatedTetrahedralNumber, getNthTriangularNumber

from rpn.rpnPrimeUtils import countCache, findPrimeOperator, findQuadrupletPrimeOperator, \
                              findQuintupletPrimeOperator, findSextupletPrimeOperator, findTripletPrimeOperator, \
                              findTwinPrimeOperator, getMaxPrime, getNextPrimeOperator, getNextPrimesOperator, \
                              getNextQuadrupletPrime, getNextQuadrupletPrimes, getNextQuintupletPrime, \
                              getNextQuintupletPrimes, getNextSextupletPrime, getNextSextupletPrimes, \
                              getNextTripletPrime, getNextTripletPrimes, getNextTwinPrime, getNextTwinPrimes, \
                              getNthBalancedPrime, getNthBalancedPrimeList,getNthCousinPrime, getNthCousinPrimeList, \
                              getNthDoubleBalancedPrime, getNthDoubleBalancedPrimeList, getNthIsolatedPrime, \
                              getNthOctyPrime, getNthOctyPrimeList, getNthPolyPrime, getNthPrime, getNthPrimorial, \
                              getNthQuadrupleBalancedPrime, getNthQuadrupleBalancedPrimeList, getNthQuadrupletPrime, \
                              getNthQuadrupletPrimeList, getNthQuintupletPrime, getNthQuintupletPrimeList, \
                              getNthSextupletPrime, getNthSextupletPrimeList, getNthSexyPrime, getNthSexyPrimeList, \
                              getNthSexyQuadruplet, getNthSexyQuadrupletList, getNthSexyTriplet, \
                              getNthSexyTripletList, getNthSophiePrime, getNthSuperPrime, getNthTripleBalancedPrime, \
                              getNthTripleBalancedPrimeList, getNthTripletPrime, getNthTripletPrimeList, \
                              getNthTwinPrime, getNthTwinPrimeList, getSafePrime, getPreviousPrimeOperator, \
                              getPreviousPrimesOperator, getPrimeRange, getPrimesGenerator, isComposite, \
                              isPrimeOperator, isStrongPseudoprime

from rpn.rpnSettings import setComma, setCommaMode, setDecimalGrouping, setHexMode, setIdentify, \
                            setIdentifyMode, setInputRadix, setIntegerGrouping, setLeadingZero, \
                            setLeadingZeroMode, setAccuracy, setPrecision, setOctalMode, setOutputRadix, \
                            setTimer, setTimerMode

from rpn.rpnSpecial import describeInteger, downloadOEISComment, downloadOEISExtra, downloadOEISName, \
                           downloadOEISOffset, downloadOEISSequence, findPolynomial, generateRandomUUID, \
                           generateUUID, getMultipleRandomsGenerator, getRandomInteger, \
                           getRandomIntegersGenerator, getRandomNumber

from rpn.rpnUtils import addEchoArgument, abortArgsNeeded, oneArgFunctionEvaluator, \
                         twoArgFunctionEvaluator, validateArguments

from rpn.rpnValidator import argValidator

import rpn.rpnGlobals as g


#******************************************************************************
#
#  constants
#
#  Constants are always operators that take no arguments.
#
#  Please note that the last two RPNOperator arguments must go on a new line
#  because the 'lambda' functionality parses the lambdas in RPNOperator objects
#  to build Python code out of them.
#
#******************************************************************************

constants = {
    # mathematical constants
    # we use mpf( ) so the type returned is mpf rather than the mpmath constant type
    'apery_constant'                : RPNOperator( lambda: mpf( apery ),
                                                   0, [ ] ),
    'catalan_constant'              : RPNOperator( lambda: mpf( catalan ),
                                                   0, [ ] ),
    'champernowne_constant'         : RPNOperator( getChampernowneConstant,
                                                   0, [ ] ),
    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant,
                                                   0, [ ] ),
    'e'                             : RPNOperator( lambda: mpf( e ),
                                                   0, [ ] ),
    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ),
                                                   0, [ ] ),
    'euler_mascheroni_constant'     : RPNOperator( lambda: mpf( euler ),
                                                   0, [ ] ),
    'glaisher_constant'             : RPNOperator( lambda: mpf( glaisher ),
                                                   0, [ ] ),
    'infinity'                      : RPNOperator( lambda: inf,
                                                   0, [ ] ),
    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ),
                                                   0, [ ] ),
    'khinchin_constant'             : RPNOperator( lambda: mpf( khinchin ),
                                                   0, [ ] ),
    'merten_constant'               : RPNOperator( lambda: mpf( mertens ),
                                                   0, [ ] ),
    'mills_constant'                : RPNOperator( getMillsConstant,
                                                   0, [ ] ),
    'negative_infinity'             : RPNOperator( lambda: -inf,
                                                   0, [ ] ),
    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ),
                                                   0, [ ] ),
    'phi'                           : RPNOperator( lambda: mpf( phi ),
                                                   0, [ ] ),
    'pi'                            : RPNOperator( lambda: mpf( pi ),
                                                   0, [ ] ),
    'plastic_constant'              : RPNOperator( getPlasticConstant,
                                                   0, [ ] ),
    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ),
                                                   0, [ ] ),
    'robbins_constant'              : RPNOperator( getRobbinsConstant,
                                                   0, [ ] ),
    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ),
                                                   0, [ ] ),
    'tau'                           : RPNOperator( lambda: fmul( mpf( pi ), 2 ),
                                                   0, [ ] ),
    'thue_morse_constant'           : RPNOperator( getThueMorseConstant,
                                                   0, [ ] ),

    # derived physical constants
    'faraday_constant'              : RPNOperator( getFaradayConstant,
                                                   0, [ ] ),
    'fine_structure_constant'       : RPNOperator( getFineStructureConstant,
                                                   0, [ ] ),
    'radiation_constant'            : RPNOperator( getRadiationConstant,
                                                   0, [ ] ),
    'stefan_boltzmann_constant'     : RPNOperator( getStefanBoltzmannConstant,
                                                   0, [ ] ),
    'vacuum_impedance'              : RPNOperator( getVacuumImpedance,
                                                   0, [ ] ),
    'von_klitzing_constant'         : RPNOperator( getvonKlitzingConstant,
                                                   0, [ ] ),

    # Planck constants
    'planck_length'                 : RPNOperator( getPlanckLength,
                                                   0, [ ] ),
    'planck_mass'                   : RPNOperator( getPlanckMass,
                                                   0, [ ] ),
    'planck_time'                   : RPNOperator( getPlanckTime,
                                                   0, [ ] ),
    'planck_charge'                 : RPNOperator( getPlanckCharge,
                                                   0, [ ] ),
    'planck_temperature'            : RPNOperator( getPlanckTemperature,
                                                   0, [ ] ),

    'planck_acceleration'           : RPNOperator( getPlanckAcceleration,
                                                   0, [ ] ),
    'planck_angular_frequency'      : RPNOperator( getPlanckAngularFrequency,
                                                   0, [ ] ),
    'planck_area'                   : RPNOperator( getPlanckArea,
                                                   0, [ ] ),
    'planck_current'                : RPNOperator( getPlanckCurrent,
                                                   0, [ ] ),
    'planck_density'                : RPNOperator( getPlanckDensity,
                                                   0, [ ] ),
    'planck_energy'                 : RPNOperator( getPlanckEnergy,
                                                   0, [ ] ),
    'planck_electrical_inductance'  : RPNOperator( getPlanckElectricalInductance,
                                                   0, [ ] ),
    'planck_energy_density'         : RPNOperator( getPlanckEnergyDensity,
                                                   0, [ ] ),
    'planck_force'                  : RPNOperator( getPlanckForce,
                                                   0, [ ] ),
    'planck_impedance'              : RPNOperator( getPlanckImpedance,
                                                   0, [ ] ),
    'planck_intensity'              : RPNOperator( getPlanckIntensity,
                                                   0, [ ] ),
    'planck_magnetic_inductance'    : RPNOperator( getPlanckMagneticInductance,
                                                   0, [ ] ),
    'planck_momentum'               : RPNOperator( getPlanckMomentum,
                                                   0, [ ] ),
    'planck_power'                  : RPNOperator( getPlanckPower,
                                                   0, [ ] ),
    'planck_pressure'               : RPNOperator( getPlanckPressure,
                                                   0, [ ] ),
    'planck_viscosity'              : RPNOperator( getPlanckViscosity,
                                                   0, [ ] ),
    'planck_voltage'                : RPNOperator( getPlanckVoltage,
                                                   0, [ ] ),
    'planck_volumetric_flow_rate'   : RPNOperator( getPlanckVolumetricFlowRate,
                                                   0, [ ] ),
    'planck_volume'                 : RPNOperator( getPlanckVolume,
                                                   0, [ ] ),
}


#******************************************************************************
#
#  class RPNFunction
#
#  Starting index is a little confusing.  When rpn knows it is parsing a
#  function declaration, it will put all the arguments so far into the
#  RPNFunction object.  However, it can't know how many of them it
#  actually needs until it's time to evaluate the function, so we need to
#  save all the terms we have so far, since we can't know until later how
#  many of them we will need.
#
#  Once we are able to parse out how many arguments belong to the function
#  declaration, then we can determine what arguments are left over to be used
#  with the function operation.   All function operations take at least one
#  argument before the function declaration.
#
#******************************************************************************

class RPNFunction( ):
    '''This class represents a user-defined function in rpn.'''
    def __init__( self, valueList = None, startingIndex = 0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        elif valueList:
            self.valueList.append( valueList )
        else:
            self.valueList = None

        self.startingIndex = startingIndex
        self.code = ''
        self.codeLocals = { }
        self.compiled = None
        self.function = None
        self.argCount = 0

    def add( self, arg ):
        self.valueList.append( arg )

    def evaluate( self, x = 0, y = 0, z = 0 ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        if self.argCount == 0:
            return self.function( )
        elif self.argCount == 1:
            return self.function( x )
        elif self.argCount == 2:
            return self.function( x, y )
        elif self.argCount == 3:
            return self.function( x, y, z )

        raise ValueError( 'too many arguments for a user-defined function' )

    def setCode( self, code ):
        if code.find( 'rpnInternalFunction( ):' ) != -1:
            self.argCount = 0
        elif code.find( 'rpnInternalFunction( x ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( z ):' ) != -1:
            self.argCount = 1
        elif code.find( 'rpnInternalFunction( x, y ):' ) != -1 or \
           code.find( 'rpnInternalFunction( x, z ):' ) != -1 or \
           code.find( 'rpnInternalFunction( y, z ):' ) != -1:
            self.argCount = 2
        else:
            self.argCount = 3

        self.code = code
        self.compile( )

    def getCode( self ):
        if not self.code:
            self.buildCode( )
            self.compile( )

        return self.code

    def getFunction( self ):
        if not self.function:
            self.buildCode( )
            self.compile( )

        return self.function

    def buildCode( self ):
        valueList = [ ]

        xArg = False
        yArg = False
        zArg = False

        for index, item in enumerate( self.valueList ):
            if index < self.startingIndex:
                continue

            if item == 'x':
                xArg = True
            elif item == 'y':
                yArg = True
            elif item == 'z':
                zArg = True

            valueList.append( item )

        self.code = 'def rpnInternalFunction('

        first = True

        self.argCount = 0

        if xArg:
            self.code += ' x'
            first = False
            self.argCount += 1

        if yArg:
            if first:
                first = False
            else:
                self.code += ','

            self.code += ' y'
            self.argCount += 1

        if zArg:
            if not first:
                self.code += ','

            self.code += ' z'
            self.argCount += 1

        self.code += ' ): return '

        emptyFunction = True

        args = [ ]
        listArgs = [ ]
        listDepth = 0

        debugPrint( 'terms', valueList )

        while valueList:
            term = valueList.pop( 0 )
            debugPrint( 'term:', term, 'args:', args )

            if not isinstance( term, list ) and term in g.aliases:
                term = g.aliases[ term ]

            if term in ( 'x', 'y', 'z' ) and not valueList:
                self.code += term
                emptyFunction = False
            elif term in constants:
                function = constants[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( constants[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) :
                                         function.find( '\n' ) - 1 ] + ' )'

                function += '( )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term == '[':
                listArgs.append( [ ] )
                listDepth += 1
            elif term == ']':
                arg = '[ '

                for listArg in listArgs[ listDepth - 1 ]:
                    if arg != '[ ':
                        arg += ', '

                    arg += listArg

                arg += ' ]'

                args.append( arg )

                del listArgs[ listDepth - 1 ]

                listDepth -= 1
            #elif term in specialFormatOperators:
            elif term in operators:
                function = operators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( operators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) :
                                         function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = operators[ term ].argCount

                if listDepth > 0:
                    if len( listArgs[ listDepth - 1 ] ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for _ in range( 0, operands ):
                        argList.insert( 0, listArgs[ listDepth - 1 ].pop( ) )
                else:
                    if len( args ) < operands:
                        raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                    for _ in range( 0, operands ):
                        argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term in listOperators:
                function = listOperators[ term ].function.__name__
                debugPrint( 'function', function )

                if function == '<lambda>':
                    function = inspect.getsource( listOperators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'
                    function = function[ function.find( className ) + len( className ) :
                                         function.find( '\n' ) -1 ] + ' )'

                function += '( '

                first = True

                argList = [ ]

                operands = listOperators[ term ].argCount

                if len( args ) < operands:
                    raise ValueError( '\'{0}\' expects {1} operands'.format( term, operands ) )

                for _ in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function += ', '

                    function += arg

                function += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function )
                else:
                    args.append( function )

                if not valueList:
                    self.code += function
                    emptyFunction = False
            elif term[ 0 ] == '@' and term[ 1 : ] in g.userFunctions:
                function2 = g.userFunctions[ term[ 1 : ] ].getCode( )
                debugPrint( 'function:', function2 )

                function2 = function2.replace( 'def rpnInternalFunction(', '( lambda' )
                function2 = function2.replace( ' ): return', ':' )

                function2 += ' )( '

                first = True

                argList = [ ]

                operands = g.userFunctions[ term[ 1 : ] ].argCount

                if len( args ) < operands:
                    raise ValueError( '{0} expects {1} operands'.format( term, operands ) )

                for _ in range( 0, operands ):
                    argList.insert( 0, args.pop( ) )

                for arg in argList:
                    if first:
                        first = False
                    else:
                        function2 += ', '

                    function2 += arg

                function2 += ' )'

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( function2 )
                else:
                    args.append( function2 )

                if not valueList:
                    self.code += function2
                    emptyFunction = False
            elif term[ 0 ] == '$' and term[ 1 : ] in g.userVariables:
                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( g.userVariables[ term[ 1 : ] ] )
                else:
                    args.append( g.userVariables[ term[ 1 : ] ] )
            else:
                if term not in ( 'x', 'y', 'z' ):
                    term = str( parseInputValue( term, g.inputRadix ) )

                if listDepth > 0:
                    listArgs[ listDepth - 1 ].append( term )
                else:
                    args.append( term )

        if emptyFunction:
            self.code += args[ 0 ]

        debugPrint( 'args:', args )
        debugPrint( 'valueList:', self.valueList[ self.startingIndex : ] )
        debugPrint( 'code:', self.code )

    def compile( self ):
        if not self.code:
            self.buildCode( )

        self.compiled = compile( self.code, '<string>', 'exec' )

        exec( self.compiled, globals( ), self.codeLocals )
        self.function = self.codeLocals[ 'rpnInternalFunction' ]


#******************************************************************************
#
#  createFunction
#
#  This only gets called if we are not already creating a function.
#
#******************************************************************************

def createFunction( valueList ):
    g.creatingFunction = True
    valueList.append( RPNFunction( valueList, len( valueList ) ) )


#******************************************************************************
#
#  addX
#
#******************************************************************************

def addX( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'x\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'x' )


#******************************************************************************
#
#  addY
#
#******************************************************************************

def addY( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'y\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'y' )


#******************************************************************************
#
#  addZ
#
#******************************************************************************

def addZ( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'z\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'z' )


#******************************************************************************
#
#  loadUserFunctionsFile
#
#******************************************************************************

def loadUserFunctionsFile( ):
    config = configparser.ConfigParser( )
    config.read( getUserFunctionsFileName( ) )

    try:
        items = config.items( 'User Functions' )
    except:
        return

    for item in items:
        func = RPNFunction( )
        func.setCode( item[ 1 ] )
        g.userFunctions[ item[ 0 ] ] = func


#******************************************************************************
#
#  saveUserFunctionsFile
#
#******************************************************************************

def saveUserFunctionsFile( ):
    config = configparser.ConfigParser( )

    config[ 'User Functions' ] = { }

    for key, value in g.userFunctions.items( ):
        config[ 'User Functions' ][ key ] = value.getCode( )

    if os.path.isfile( getUserFunctionsFileName( ) ):
        copyfile( getUserFunctionsFileName( ), getUserFunctionsFileName( ) + '.backup' )

    with open( getUserFunctionsFileName( ), 'w' ) as userFunctionsFile:
        config.write( userFunctionsFile )


#******************************************************************************
#
#  plotFunction
#
#******************************************************************************

def plotFunction( start, end, func ):
    plot( func.evaluate, [ start, end ] )
    return 0


#******************************************************************************
#
#  plot2DFunction
#
#******************************************************************************

def plot2DFunction( start1, end1, start2, end2, func ):
    splot( func.evaluate,
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


#******************************************************************************
#
#  plotComplexFunction
#
#******************************************************************************

def plotComplexFunction( start1, end1, start2, end2, func ):
    cplot( func.evaluate,
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ],
           points = 10000 )
    return 0


#******************************************************************************
#
#  evaluateRecurrence
#
#******************************************************************************

def evaluateRecurrence( start, count, func ):
    arg = start
    result = [ start ]

    for _ in arange( count ):
        arg = func.evaluate( arg )
        result.append( arg )

    return result


#******************************************************************************
#
#  repeatGenerator
#
#******************************************************************************

def repeatGenerator( n, func ):
    for _ in arange( 0, n ):
        yield func.evaluate( )


#******************************************************************************
#
#  repeat
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def repeat( n, func ):
    return RPNGenerator( repeatGenerator( n, func ) )


#******************************************************************************
#
#  sequenceGenerator
#
#******************************************************************************

def sequenceGenerator( n, k, func ):
    value = n

    if k > 0:
        yield value

    for _ in arange( 1, k ):
        value = func.evaluate( value )
        yield value


#******************************************************************************
#
#  getSequence
#
#******************************************************************************

def getSequence( n, k, func ):
    return RPNGenerator( sequenceGenerator( n, k, func ) )


#******************************************************************************
#
#  filterList
#
#******************************************************************************

def filterList( n, k, invert=False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )

        raise ValueError( '\'filter\' expects a function argument' )

    for i in n:
        value = k.evaluate( i )

        if ( value != 0 ) != invert:
            yield i


#******************************************************************************
#
#  filterListByIndex
#
#******************************************************************************

def filterListByIndex( n, k, invert=False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter_by_index\' expects a function argument' )

        raise ValueError( '\'filter_by_index\' expects a function argument' )

    for index, item in enumerate( n ):
        value = k.evaluate( index )

        if ( value != 0 ) != invert:
            yield item


#******************************************************************************
#
#  filterIntegersGenerator
#
#******************************************************************************

def filterIntegersGenerator( n, k ):
    if n < 1:
        raise ValueError( '\'filter_integers\' requires a positive integer argument' )

    if not isinstance( k, RPNFunction ):
        raise ValueError( '\'filter_integers\' expects a function argument' )

    for i in arange( 1, fadd( n, 1 ) ):
        value = k.evaluate( i, n )

        if value != 0:
            yield i


#******************************************************************************
#
#  filterIntegers
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def filterIntegers( n, func ):
    return RPNGenerator( filterIntegersGenerator( n, func ) )


#******************************************************************************
#
#  forEach
#
#******************************************************************************

def forEach( listArg, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each\' expects a function argument' )

    for i in listArg:
        yield func.evaluate( *i )


#******************************************************************************
#
#  forEachList
#
#******************************************************************************

def forEachList( listArg, func ):
    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'for_each_list\' expects a function argument' )

    for i in listArg:
        yield func.evaluate( i )


#******************************************************************************
#
#  breakOnCondition
#
#******************************************************************************

def breakOnCondition( arguments, condition, func ):
    if not isinstance( arguments, list ):
        arguments = [ arguments ]

    #print( 'arguments', arguments )

    if not isinstance( func, RPNFunction ):
        raise ValueError( '\'break_on\' expects a function argument' )

    for argument in arguments:
        value = func.evaluate( argument )

        if value == condition:
            return value

    return value


#******************************************************************************
#
#  preprocessTerms
#
#  *** Not used yet! ***
#
#******************************************************************************

def preprocessTerms( terms ):
    '''
    Given the initial list of arguments form the user, there are several
    things we want to do to the list before handing it off to the actual
    operator evaluator.  This logic used to be part of the evaluator, but
    that made the code a lot more complicated.  Hopefully, this will make
    the code simpler and easier to read.

    If this function returns an empty list, then rpn should abort.  This
    function should print out any error messages.
    '''
    result = [ ]

    # do some basic validation of the arguments we were given...
    if not validateArguments( terms ):
        return result

    print( 'operators', operators )

    for term in terms:
        # translate the aliases into their real names
        if term in g.aliases:
            result.append( g.aliases[ term ] )
        # operators and unit operator names can be stuck right back in the list
        elif term in g.unitOperatorNames or term in g.constantOperatorNames:
            result.append( term )
        # translate compound units in the equivalent operators
        elif ( '*' in term or '^' in term or '/' in term ) and \
            any( c in term for c in string.ascii_letters ):
            result.append( RPNUnits.parseUnitString( term ) )
        else:
            result.append( term )

    return result


#******************************************************************************
#
#  evaluateConstantOperator
#
#  We know there are no arguments.  Although none of the constants currently
#  return a list, maybe one will in the future, so I'll handle list results.
#
#******************************************************************************

def evaluateConstantOperator( term, currentValueList ):
    # handle a constant operator
    operatorInfo = constants[ term ]
    result = callers[ 0 ]( operatorInfo.function, None )

    newResult = list( )

    if not isinstance( result, list ):
        result = [ result ]

    for item in result:
        if isinstance( item, RPNMeasurement ) and item.units == { }:
            newResult.append( item.value )
        else:
            newResult.append( item )

    if len( newResult ) == 1:
        newResult = newResult[ 0 ]

    currentValueList.append( newResult )

    return True


#******************************************************************************
#
#  handleOneArgListOperator
#
#  Each operator is going to have to be responsible for how it handles
#  recursive lists.  In some cases, handling recursive lists makes sense.
#
#******************************************************************************

def handleOneArgListOperator( func, args, currentValueList ):
    if isinstance( args, RPNGenerator ):
        args = list( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if not isinstance( args, list ):
        currentValueList.append( func( [ args ] ) )
    else:
        currentValueList.append( func( args ) )


#******************************************************************************
#
#  handleOneArgGeneratorOperator
#
#******************************************************************************

def handleOneArgGeneratorOperator( func, args, currentValueList ):
    if isinstance( args, list ):
        args = RPNGenerator.create( args )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    if isinstance( args, RPNGenerator ):
        currentValueList.append( func( args ) )
    else:
        raise ValueError( 'then you shouldn\'t call handleOneArgGeneratorOperator, should you?' )


#******************************************************************************
#
#  handleMultiArgListOperator
#
#  Each operator is going to have to be responsible for how it handles
#  recursive lists.  In some cases, handling recursive lists makes sense.
#
#******************************************************************************

def handleMultiArgListOperator( func, argList, currentValueList ):
    newArgList = [ ]

    for arg in argList:
        if isinstance( arg, RPNGenerator ):
            newArgList.append( list( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


#******************************************************************************
#
#  handleMultiArgGeneratorOperator
#
#******************************************************************************

def handleMultiArgGeneratorOperator( func, args, currentValueList ):
    newArgList = [ ]

    for arg in args:
        if isinstance( arg, list ):
            newArgList.append( RPNGenerator.create( arg ) )
        else:
            newArgList.append( arg )

    # check for arguments to be echoed, and echo them before the result
    if len( g.echoArguments ) > 0:
        for echoArg in g.echoArguments:
            currentValueList.append( echoArg )

    currentValueList.append( func( *newArgList ) )


#******************************************************************************
#
#  evaluateListOperator
#
#******************************************************************************

def evaluateListOperator( term, index, currentValueList ):
    # handle a list operator
    operatorInfo = listOperators[ term ]
    argsNeeded = operatorInfo.argCount
    argTypes = operatorInfo.argTypes

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    # handle the call depending on the number of arguments needed
    if argsNeeded == 0:
        currentValueList.append( operatorInfo.function( currentValueList ) )
    elif argsNeeded == 1:
        args = currentValueList.pop( )

        if argTypes[ 0 ] == RPNValidator.Generator:
            handleOneArgGeneratorOperator( operatorInfo.function, args, currentValueList )
        else:
            handleOneArgListOperator( operatorInfo.function, args, currentValueList )
    else:
        argList = [ ]

        for _ in range( 0, argsNeeded ):
            argList.insert( 0, currentValueList.pop( ) )

        if argTypes[ 0 ] == RPNValidator.Generator:
            handleMultiArgGeneratorOperator( operatorInfo.function, argList, currentValueList )
        else:
            handleMultiArgListOperator( operatorInfo.function, argList, currentValueList )

    return True


#******************************************************************************
#
#  dumpOperators
#
#******************************************************************************

def dumpOperators( totalsOnly=False ):
    # TODO:  Use g.operatorNames, etc.
    if not totalsOnly:
        print( 'regular operators:' )

    regularOperators = 0

    for i in sorted( [ key for key in operators if key[ 0 ] != '_' ] ):
        # print( '   ' + i + ', args: ' + str( operators[ i ].argCount ) )
        regularOperators += 1

        if not totalsOnly:
            print( '   ' + i )

    if not totalsOnly:
        print( )
        print( 'list operators:' )

        for i in sorted( listOperators.keys( ) ):
            print( '   ' + i )

        print( )
        print( 'constant operators:' )

    constantNames = list( g.constantOperators.keys( ) )
    constantNames.extend( constants.keys( ) )

    if not totalsOnly:
        for i in sorted( constantNames ):
            print( '   ' + i )

        print( )
        print( 'modifier operators:' )

        for i in sorted( modifiers.keys( ) ):
            print( '   ' + i )

        print( )
        print( 'internal operators:' )

    internalOperators = 0

    for i in sorted( [ key for key in operators if key[ 0 ] == '_' ] ):
        internalOperators += 1

        if not totalsOnly:
            print( '   ' + i )

    if not totalsOnly:
        print( )

    print( '{:10,} regular operators'.format( regularOperators ) )
    print( '{:10,} list operators'.format( len( listOperators ) ) )
    print( '{:10,} modifier operators'.format( len( modifiers ) ) )
    print( '{:10,} constant operators'.format( len( constantNames ) ) )
    print( '{:10,} internal operators'.format( internalOperators ) )

    total = len( operators ) + len( listOperators ) + len( modifiers ) + len( constantNames )

    print( '     ----- ------------------' )
    print( '{:10,} unique operators'.format( total ) )
    print( )

    return total


#******************************************************************************
#
#  dumpConstants
#
#******************************************************************************

def dumpConstants( ):
    if not g.constantOperators:
        loadUnitData( )
        loadConstants( )

    for constant in sorted( g.constantOperators ):
        print( constant + ':  ' + str( g.constantOperators[ constant ].value ) + ' ' + \
               g.constantOperators[ constant ].unit )

    print( )

    return len( g.constantOperators )


#******************************************************************************
#
#  dumpUnits
#
#******************************************************************************

def dumpUnits( ):
    if not g.unitOperators:
        loadUnitData( )
        loadConstants( )

    for i in sorted( g.unitOperators ):
        print( i )

    print( )

    return len( g.unitOperators )


#******************************************************************************
#
#  dumpUnitConversions
#
#******************************************************************************

def dumpUnitConversions( ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    for i in sorted( g.unitConversionMatrix ):
        print( i, g.unitConversionMatrix[ i ] )

    print( )

    return len( g.unitConversionMatrix )


#******************************************************************************
#
#  printStats
#
#******************************************************************************

def printStats( cacheName, name ):
    count = countCache( cacheName )
    key, value = getMaxPrime( cacheName )

    print( '{:10,} {:27} max: {:14,} ({:,})'.format( count, name, key, value ) )


#******************************************************************************
#
#  dumpStats
#
#******************************************************************************

def dumpStats( printTitle=True ):
    if printTitle:
        printTitleScreen( PROGRAM_NAME, PROGRAM_DESCRIPTION, showHelp=False )
        print( )

    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    print( 'rpnChilada Statistics:' )
    print( )

    dumpOperators( totalsOnly=True )

    print( '{:10,} aliases'.format( len( g.aliases ) ) )
    print( )

    print( '{:10,} units'.format( len( g.unitOperators ) ) )
    print( '{:10,} unit conversions'.format( len( g.unitConversionMatrix ) ) )
    print( )

    if g.primeDataAvailable:
        printStats( 'small_primes', 'small primes' )
        printStats( 'large_primes', 'large primes' )
        printStats( 'huge_primes', 'huge primes' )
        print( )
        printStats( 'balanced_primes', 'balanced primes' )
        printStats( 'double_balanced_primes', 'double balanced primes' )
        printStats( 'triple_balanced_primes', 'triple balanced primes' )
        printStats( 'quadruple_balanced_primes', 'quadruple balanced primes' )
        print( )
        printStats( 'twin_primes', 'twin primes' )
        printStats( 'triplet_primes', 'triplet primes' )
        printStats( 'quad_primes', 'quadruplet primes' )
        printStats( 'quint_primes', 'quintuplet primes' )
        printStats( 'sext_primes', 'sextuplet primes' )
        print( )
        printStats( 'sexy_primes', 'sexy primes' )
        printStats( 'sexy_triplets', 'sexy triplet primes' )
        printStats( 'sexy_quadruplets', 'sexy quadruplet primes' )
        print( )
        printStats( 'cousin_primes', 'cousin primes' )
        printStats( 'octy_primes', 'octy primes' )
        printStats( 'isolated_primes', 'isolated primes' )
        printStats( 'sophie_primes', 'Sophie Germain primes' )

        print( )

    return [ int( i ) for i in PROGRAM_VERSION.split( '.' ) ]


#******************************************************************************
#
#  preparseForUnits
#
#  Break the string apart by '-', '/', '*', and '^' and if each element is a
#  unit, then convert '-' to '*'.   This way, we can still have '-' in
#  operator names (although I don't think there are currently any).
#
#******************************************************************************

def preparseForUnits( term ):
    if '-' in term:
        pieces = term.split( '-' )
    else:
        pieces = [ term ]

    newPieces = [ ]

    for piece in pieces:
        if '/' in piece:
            newPieces.extend( piece.split( '/' ) )
        else:
            newPieces.append( piece )

    pieces = newPieces

    newPieces = [ ]

    for piece in pieces:
        if '*' in piece:
            newPieces.extend( piece.split( '*' ) )
        else:
            newPieces.append( piece )

    pieces = newPieces

    for piece in pieces:
        if '^' in piece:
            splits = piece.split( '^' )

            unit = splits[ 0 ]

            if unit in g.aliases:
                unit = g.aliases[ unit ]

            if unit not in g.unitOperators:
                return term

            try:
                _ = int( splits[ 1 ] )
            except:
                return term
        else:
            if piece in g.aliases:
                piece = g.aliases[ piece ]

            if piece not in g.unitOperators:
                return term

    return term.replace( '-', '*' )


#******************************************************************************
#
#  evaluateTerm
#
#  This looks worse than it is.  It just has to do slightly different things
#  depending on what kind of term or operator is involved.  Plus, there's a
#  lot of exception handling.
#
#  This function assumes operator alias replacements have already occurred.
#
#******************************************************************************

def evaluateTerm( term, index, currentValueList, lastArg = True ):
    isList = isinstance( term, list )
    isGenerator = isinstance( term, RPNGenerator )

    try:
        term = preparseForUnits( term )

        # handle a modifier operator
        if not isList and not isGenerator and term in modifiers:
            operatorInfo = modifiers[ term ]
            operatorInfo.function( currentValueList )
        elif not isList and term in g.unitOperatorNames or term in g.constantOperatorNames or \
             ( '*' in term or '^' in term or '/' in term ) and \
             any( c in term for c in string.ascii_letters ):

            multipliable = True

            if term in g.unitOperatorNames:
                isConstant = False
            elif term in g.constantOperatorNames:
                isConstant = True
                multipliable = g.constantOperators[ term ].multipliable
            else:
                isConstant = False
                term = RPNUnits.parseUnitString( term )
                term = RPNMeasurement( 1, term ).simplifyUnits( ).units.normalizeUnits( )

                if term == RPNUnits( ):
                    term = RPNUnits( '_null_unit' )

            if multipliable:
                # look for unit without a value (in which case we give it a value of 1)
                if ( len( currentValueList ) == 0 ) or isinstance( currentValueList[ -1 ], RPNMeasurement ) or \
                    isinstance( currentValueList[ -1 ], RPNDateTime ) or \
                    ( isinstance( currentValueList[ -1 ], list ) and \
                      isinstance( currentValueList[ -1 ][ 0 ], RPNMeasurement ) ):
                    currentValueList.append( applyNumberValueToUnit( 1, term, isConstant ) )
                # if the unit comes after a generator, convert it to a list and apply the unit to each
                elif isinstance( currentValueList[ -1 ], RPNGenerator ):
                    newArg = [ ]

                    for value in list( currentValueList.pop( ) ):
                        newArg.append( applyNumberValueToUnit( value, term, isConstant ) )

                    currentValueList.append( newArg )
                # if the unit comes after a list, then apply it to every item in the list
                elif isinstance( currentValueList[ -1 ], list ):
                    argList = currentValueList.pop( )

                    newArg = [ ]

                    for listItem in argList:
                        newArg.append( applyNumberValueToUnit( listItem, term, isConstant ) )

                    currentValueList.append( newArg )
                # and if it's a plain old number, then apply it to the unit
                elif isinstance( currentValueList[ -1 ], ( mpf, int ) ):
                    currentValueList.append( applyNumberValueToUnit( currentValueList.pop( ), term, isConstant ) )
                else:
                    print( type( currentValueList[ -1 ] ) )
                    raise ValueError( 'unsupported type for a unit operator' )
            else:
                # only constant operators can be non-multipliable
                constantInfo = g.constantOperators[ term ]

                if constantInfo.unit == '':
                    currentValueList.append( mpmathify( constantInfo.value ) )
                else:
                    currentValueList.append( RPNMeasurement( constantInfo.value, constantInfo.unit ) )
        elif term in constants:
            if not evaluateConstantOperator( term, currentValueList ):
                return False
        elif term in operators:
            if g.duplicateOperations > 0:
                operatorInfo = operators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not operators[ term ].evaluate( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not operators[ term ].evaluate( term, index, currentValueList ):
                    return False
        elif term in listOperators:
            if g.duplicateOperations > 0:
                operatorInfo = listOperators[ term ]
                argsNeeded = operatorInfo.argCount

                if argsNeeded > 1:
                    savedArgs = currentValueList[ -argsNeeded + 1 : ]

                for i in range( 0, int( g.duplicateOperations ) ):
                    if argsNeeded > 1 and i > 0:
                        currentValueList.extend( savedArgs )

                    if not evaluateListOperator( term, index, currentValueList ):
                        return False

                g.duplicateOperations = 0
            else:
                if not evaluateListOperator( term, index, currentValueList ):
                    return False
        else:
            # handle a plain old value (i.e., a number or list, not an operator)... or
            # a reference to a user-defined function
            try:
                currentValueList.append( parseInputValue( term, g.inputRadix ) )

            except ValueError as error:
                print( 'rpn:  error in arg ' + format( index ) + ':  {0}'.format( error ) )

                if g.debugMode:
                    raise

                return False

            except ( AttributeError, TypeError ):
                if not lastArg:
                    currentValueList.append( term )
                    return True

                # build keyword list if needed
                if len( g.keywords ) == 0:
                    g.keywords = list( operators.keys( ) )
                    g.keywords.extend( list( listOperators.keys( ) ) )
                    g.keywords.extend( g.constantOperatorNames )
                    g.keywords.extend( constants )
                    g.keywords.extend( g.unitOperatorNames )
                    g.keywords.extend( g.aliases )

                guess = difflib.get_close_matches( term, g.keywords, 1 )

                if len( guess ) == 1:
                    guess = guess[ 0 ]

                    if guess in g.aliases:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  '
                               'Did you mean \'{1}\', i.e., an alias for \'{2}\'?'.
                               format( term, guess, g.aliases[ guess ] ) )
                    else:
                        print( 'rpn:  Unrecognized operator \'{0}\'.  Did you mean \'{1}\'?'.format( term, guess ) )
                else:
                    print( 'rpn:  Unrecognized operator \'{0}\'.'.format( term ) )

                return False

            # handle a user-defined function
            if isinstance( currentValueList[ -1 ], RPNFunction ):
                # make sure the code has been built so we can determine argCount correctly
                if not currentValueList[ -1 ].code:
                    currentValueList[ -1 ].buildCode( )

                if currentValueList[ -1 ].argCount == 0:
                    if not operators[ 'eval0' ].evaluate( 'eval0', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 1:
                    if not operators[ 'eval' ].evaluate( 'eval', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 2:
                    if not operators[ 'eval2' ].evaluate( 'eval2', index, currentValueList ):
                        return False
                elif currentValueList[ -1 ].argCount == 3:
                    if not operators[ 'eval3' ].evaluate( 'eval3', index, currentValueList ):
                        return False

                return True

    except ( ValueError, AttributeError, TypeError ) as error:
        print( 'rpn:  error for operator at arg ' + format( index ) + ':  {0}'.format( error ) )

        if g.debugMode:
            raise

        return False

    except ZeroDivisionError as error:
        print( 'rpn:  division by zero' )

        if g.debugMode:
            raise

        return False

    except IndexError as error:
        print( 'rpn:  index error for list operator at arg ' + format( index ) +
               '.  Are your arguments in the right order?' )

        if g.debugMode:
            raise

        return False

    return True


#******************************************************************************
#
#  printHelpMessage
#
#******************************************************************************

def printHelpMessage( ):
    from rpnOutput import printHelp
    printHelp( interactive=True )
    return 0


#******************************************************************************
#
#  printHelpTopic
#
#******************************************************************************

def printHelpTopic( n ):
    from rpnOutput import printHelp

    if isinstance( n, str ):
        printHelp( [ n ], interactive=True )
    elif isinstance( n, RPNMeasurement ):
        units = n.units
        # help for units isn't implemented yet, but now it will work
        printHelp( [ list( units.keys( ) )[ 0 ] ], interactive=True )
    else:
        print( 'The \'topic\' operator requires a string argument.' )

    return 0


#******************************************************************************
#
#  getUserVariable
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getUserVariable( key ):
    if not isinstance( key, str ):
        raise ValueError( 'variable names must be strings' )

    if key in g.userVariables:
        return g.userVariables[ key ]
    else:
        return ''


#******************************************************************************
#
#  setUserVariable
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def setUserVariable( key, value ):
    if not isinstance( key, str ):
        raise ValueError( 'variable names must be strings' )

    g.userVariables[ key ] = value
    g.userVariablesAreDirty = True

    return value


#******************************************************************************
#
#  getUserConfiguration
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def getUserConfiguration( key ):
    if key in g.userConfiguration:
        return g.userConfiguration[ key ]
    else:
        return ''


#******************************************************************************
#
#  setUserConfiguration
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def setUserConfiguration( key, value ):
    g.userConfiguration[ key ] = value
    g.userConfigurationIsDirty = True

    return value


#******************************************************************************
#
#  deleteUserConfiguration
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def deleteUserConfiguration( key ):
    if key not in g.userConfiguration:
        raise ValueError( 'key \'' + key + '\' not found' )

    del g.userConfiguration[ key ]
    g.userConfigurationIsDirty = True

    return key


#******************************************************************************
#
#  dumpUserConfiguration
#
#******************************************************************************

def dumpUserConfiguration( ):
    for i in g.userConfiguration:
        print( i + ':', '"' + g.userConfiguration[ i ] + '"' )

    print( )

    return len( g.userConfiguration )


#******************************************************************************
#
#  createUserFunction
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def createUserFunction( key, func ):
    g.userFunctions[ key ] = func
    g.userFunctionsAreDirty = True

    return key


@oneArgFunctionEvaluator( )
def evaluateFunction0( func ):
    return func.evaluate( )

@twoArgFunctionEvaluator( )
def evaluateFunction( n, func ):
    return func.evaluate( n )

def evaluateFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )


#******************************************************************************
#
#  evaluateListFunction
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
def evaluateListFunction( n, func ):
    return func.evaluate( n )

def evaluateListFunction2( n, k, func ):
    return func.evaluate( n, k )

def evaluateListFunction3( a, b, c, func ):
    return func.evaluate( a, b, c )


#******************************************************************************
#
#  filterListOfLists
#
#******************************************************************************

def filterListOfLists( n, func, invert=False ):
    if not isinstance( func, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter_lists\' expects a function argument' )

        raise ValueError( '\'filter_lists\' expects a function argument' )

    for i in n:
        value = func.evaluate( i )

        if ( value != 0 ) != invert:
            yield i


#******************************************************************************
#
#  evaluateLimit
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateLimit( n, func ):
    return limit( func.evaluate, n )


#******************************************************************************
#
#  evaluateReverseLimit
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateReverseLimit( n, func ):
    return limit( func.evaluate, n, direction = -1 )


#******************************************************************************
#
#  evaluateProduct
#
#******************************************************************************

def evaluateProduct( start, end, func ):
    return nprod( func.evaluate, [ start, end ] )


#******************************************************************************
#
#  evaluateSum
#
#******************************************************************************

def evaluateSum( start, end, func ):
    return nsum( func.evaluate, [ start, end ] )


#******************************************************************************
#
#  createExponentialRange
#
#******************************************************************************

def createExponentialRange( a, b, c ):
    return RPNGenerator.createExponential( a, b, c )


#******************************************************************************
#
#  createGeometricRange
#
#******************************************************************************

def createGeometricRange( a, b, c ):
    return RPNGenerator.createGeometric( a, b, c )


#******************************************************************************
#
#  createRange
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def createRange( start, end ):
    return RPNGenerator.createRange( start, end )


#******************************************************************************
#
#  createIntervalRangeOperator
#
#******************************************************************************

def createIntervalRangeOperator( a, b, c ):
    return RPNGenerator.createRange( a, b, c )


#******************************************************************************
#
#  createSizedRangeOperator
#
#******************************************************************************

def createSizedRangeOperator( a, b, c ):
    return RPNGenerator.createSizedRange( a, b, c )


#******************************************************************************
#
#  specialFormatOperators
#
#******************************************************************************

specialFormatOperators = {
    'and'       : '( {0} and {1} )',
    'nand'      : '( not ( {0} and {1} ) )',
    'or'        : '( {0} or {1} )',
    'nor'       : '( not ( {0} or {1} ) )',
}


#******************************************************************************
#
#  functionOperators
#
#  This is a list of operators that terminate the function creation state.
#
#******************************************************************************

functionOperators = [
    #'break_on',
    'eval0',
    'eval',
    'eval2',
    'eval3',
    'eval_list',
    'eval_list2',
    'eval_list3',
    'filter',
    'filter_by_index',
    'filter_integers',
    'for_each',
    'for_each_list',
    'function',
    'limit',
    'limitn',
    'nprod',
    'nsum',
    'plot',
    'plot2',
    'plot_complex',
    'recurrence',
    'repeat',
    'sequence',
    'unfilter',
    'unfilter_by_index',
]


#******************************************************************************
#
#  Modifiers are operators that directly modify the argument stack or global
#  state in addition to or instead of just returning a value.
#
#  Modifiers also don't adhere to the 'language' of rpn, which is strictly
#  postfix and context-free.  Unlike other operators consume one or more
#  values and return either a single list (possibly with sublists) or a single
#  value.  Also by changing global state, they can modify what comes _after_
#  them, which is not how the rpn language is defined.  However, this gives me
#  the flexibility to do some useful things that I am not otherwise able to
#  do.
#
#******************************************************************************

modifiers = {
    'duplicate_term'                : RPNOperator( duplicateTerm, 1 ),

    'duplicate_operator'            : RPNOperator( duplicateOperation, 1 ),

    'previous'                      : RPNOperator( getPrevious, 0 ),

    'unlist'                        : RPNOperator( unlist, 0 ),

    'lambda'                        : RPNOperator( createFunction, 0 ),

    'x'                             : RPNOperator( addX, 0 ),

    'y'                             : RPNOperator( addY, 0 ),

    'z'                             : RPNOperator( addZ, 0 ),

    '['                             : RPNOperator( incrementNestedListLevel, 0 ),

    ']'                             : RPNOperator( decrementNestedListLevel, 0 ),

    '('                             : RPNOperator( startOperatorList, 0 ),

    ')'                             : RPNOperator( endOperatorList, 0 ),
}


#******************************************************************************
#
#  listOperators are operators that handle whether or not an argument is a
#  list themselves (because they require a list argument).  Unlike regular
#  operators, we don't want listOperators permutated over each list element,
#  and if we do for auxillary arguments, these operator handlers will do that
#  themselves.
#
#******************************************************************************

listOperators = {
    # pylint: disable=line-too-long

    # algebra
    'add_polynomials'               : RPNOperator( addPolynomials,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'discriminant'                  : RPNOperator( getPolynomialDiscriminant,
                                                   1, [ RPNValidator.List ], [ ] ),

    'eval_polynomial'               : RPNOperator( evaluatePolynomial,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'multiply_polynomials'          : RPNOperator( multiplyPolynomials,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'polynomial_power'              : RPNOperator( exponentiatePolynomial,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'polynomial_product'            : RPNOperator( multiplyPolynomialList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'polynomial_sum'                : RPNOperator( sumPolynomialList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'solve'                         : RPNOperator( solvePolynomial,
                                                   1, [ RPNValidator.List ], [ ] ),

    # arithmetic
    'antiharmonic_mean'             : RPNOperator( calculateAntiharmonicMeanOperator,
                                                   1, [ RPNValidator.List ], [ ] ),

    'equals_one_of'                 : RPNOperator( equalsOneOf,
                                                   2, [ RPNValidator.Default, RPNValidator.List ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'gcd'                           : RPNOperator( getGCDOfList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'geometric_mean'                : RPNOperator( calculateGeometricMeanOperator,
                                                   1, [ RPNValidator.List ], [ ] ),

    'harmonic_mean'                 : RPNOperator( calculateHarmonicMeanOperator,
                                                   1, [ RPNValidator.List ], [ ] ),

    'lcm'                           : RPNOperator( getLCMOfList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'maximum'                       : RPNOperator( getMaximum,
                                                   1, [ RPNValidator.List ], [ ] ),

    'mean'                          : RPNOperator( calculateArithmeticMeanOperator,
                                                   1, [ RPNValidator.List ], [ ] ),

    'minimum'                       : RPNOperator( getMinimum,
                                                   1, [ RPNValidator.List ], [ ] ),

    'product'                       : RPNOperator( getProduct,
                                                   1, [ RPNValidator.List ], [ ] ),

    'root_mean_square'              : RPNOperator( calculateRootMeanSquare,
                                                   1, [ RPNValidator.List ], [ ] ),

    'stddev'                        : RPNOperator( getStandardDeviation,
                                                   1, [ RPNValidator.List ], [ ] ),

    'sum'                           : RPNOperator( getSum,
                                                   1, [ RPNValidator.List ], [ ] ),

    # combinatoric
    'count_frobenius'               : RPNOperator( countFrobenius,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'multinomial'                   : RPNOperator( getMultinomial,
                                                   1, [ RPNValidator.List ], [ ] ),

    # conversion
    'convert'                       : RPNOperator( convertUnits,
                                                   2, [ RPNValidator.List ], [ ] ),   # list arguments are special

    'lat_long_to_nac'               : RPNOperator( convertLatLongToNAC,
                                                   1, [ RPNValidator.List ], [ ] ),

    'pack'                          : RPNOperator( packInteger,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'unpack'                        : RPNOperator( unpackInteger,
                                                   2, [ RPNValidator.Integer, RPNValidator.List ], [ ] ),

    # date_time
    'make_datetime'                 : RPNOperator( makeDateTime,
                                                   1, [ RPNValidator.List ], [ ] ),

    'make_iso_time'                 : RPNOperator( makeISOTime,
                                                   1, [ RPNValidator.List ], [ ] ),

    'make_julian_time'              : RPNOperator( makeJulianTime,
                                                   1, [ RPNValidator.List ], [ ] ),

    # function
    'filter'                        : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'filter_lists'                  : RPNOperator( lambda n, k: RPNGenerator( filterListOfLists( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'filter_by_index'               : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'for_each'                      : RPNOperator( lambda n, k: RPNGenerator( forEach( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    #'for_each_list'                 : RPNOperator( lambda n, k: RPNGenerator( [ ( yield k.evaluate( i ) ) for i in n ] ),
    #                                               2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'for_each_list'                 : RPNOperator( lambda n, k: RPNGenerator( forEachList( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'unfilter'                      : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k, True ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    'unfilter_by_index'             : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k, True ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Function ], [ ] ),

    # lexicographic
    'combine_digits'                : RPNOperator( combineDigits,
                                                   1, [ RPNValidator.Generator ], [ ] ),

    # list
    'alternate_signs'               : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, False ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'alternate_signs_2'             : RPNOperator( lambda n: RPNGenerator( alternateSigns( n, True ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'alternating_sum'               : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'alternating_sum_2'             : RPNOperator( lambda n: getAlternatingSum( n, False ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'and_all'                       : RPNOperator( getAndAll,
                                                   1, [ RPNValidator.List ], [ ] ),

    'append'                        : RPNOperator( appendLists,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'collate'                       : RPNOperator( lambda n: RPNGenerator( collate( n ) ),
                                                   1, [ RPNValidator.List ], [ ] ),

    'compare_lists'                 : RPNOperator( compareLists,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'count'                         : RPNOperator( countElements,
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'cumulative_diffs'              : RPNOperator( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'cumulative_products'           : RPNOperator( lambda n: RPNGenerator( getCumulativeListProducts( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'cumulative_ratios'             : RPNOperator( lambda n: RPNGenerator( getCumulativeListRatios( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'cumulative_sums'               : RPNOperator( lambda n: RPNGenerator( getCumulativeListSums( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'difference'                    : RPNOperator( getDifference,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'diffs'                         : RPNOperator( lambda n: RPNGenerator( getListDiffs( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'does_list_repeat'              : RPNOperator( doesListRepeat,
                                                   1, [ RPNValidator.List ], [ ] ),

    'element'                       : RPNOperator( getListElement,
                                                   2, [ RPNValidator.List, RPNValidator.NonnegativeInteger ], [ ] ),

    'enumerate'                     : RPNOperator( lambda n, k: RPNGenerator( enumerateList( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Integer ], [ ] ),

    'filter_max'                    : RPNOperator( lambda n, k: RPNGenerator( filterMax( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Real ], [ ] ),

    'filter_min'                    : RPNOperator( lambda n, k: RPNGenerator( filterMin( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.Real ], [ ] ),

    'filter_on_flags'               : RPNOperator( lambda n, k: RPNGenerator( filterOnFlags( n, k ) ),
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'find'                          : RPNOperator( findInList,
                                                   2, [ RPNValidator.List, RPNValidator.Default ], [ ] ),

    'flatten'                       : RPNOperator( flatten,
                                                   1, [ RPNValidator.List ], [ ] ),

    'get_combinations'              : RPNOperator( getListCombinations,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'get_repeat_combinations'       : RPNOperator( getListCombinationsWithRepeats,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'get_permutations'              : RPNOperator( getListPermutations,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'get_repeat_permutations'       : RPNOperator( getListPermutationsWithRepeats,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'group_elements'                : RPNOperator( groupElements,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'interleave'                    : RPNOperator( interleave,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'intersection'                  : RPNOperator( makeIntersection,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'is_palindrome_list'            : RPNOperator( isPalindromeList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'left'                          : RPNOperator( getLeft,
                                                   2, [ RPNValidator.List, RPNValidator.NonnegativeInteger ], [ ] ),

    'max_index'                     : RPNOperator( getIndexOfMax,
                                                   1, [ RPNValidator.List ], [ ] ),

    'min_index'                     : RPNOperator( getIndexOfMin,
                                                   1, [ RPNValidator.List ], [ ] ),

    'nand_all'                      : RPNOperator( getNandAll,
                                                   1, [ RPNValidator.List ], [ ] ),

    'nonzero'                       : RPNOperator( getNonzeroes,
                                                   1, [ RPNValidator.List ], [ ] ),

    'nor_all'                       : RPNOperator( getNorAll,
                                                   1, [ RPNValidator.List ], [ ] ),

    'occurrences'                   : RPNOperator( getOccurrences,
                                                   1, [ RPNValidator.List ], [ ] ),

    'occurrence_cumulative'         : RPNOperator( getCumulativeOccurrenceRatios,
                                                   1, [ RPNValidator.List ], [ ] ),

    'occurrence_ratios'             : RPNOperator( getOccurrenceRatios,
                                                   1, [ RPNValidator.List ], [ ] ),

    'or_all'                        : RPNOperator( getOrAll,
                                                   1, [ RPNValidator.List ], [ ] ),

    'permute_lists'                 : RPNOperator( permuteLists,
                                                   1, [ RPNValidator.List ], [ ] ),

    'powerset'                      : RPNOperator( lambda n: RPNGenerator( getListPowerset( n ) ),
                                                   1, [ RPNValidator.List ], [ ] ),

    'random_element'                : RPNOperator( getRandomElement,
                                                   1, [ RPNValidator.List ], [ ] ),

    'ratios'                        : RPNOperator( lambda n: RPNGenerator( getListRatios( n ) ),
                                                   1, [ RPNValidator.Generator ], [ ] ),

    'reduce'                        : RPNOperator( reduceListOperator,
                                                   1, [ RPNValidator.List ], [ ] ),

    'reverse'                       : RPNOperator( getReverse,
                                                   1, [ RPNValidator.List ], [ ] ),

    'right'                         : RPNOperator( getRight,
                                                   2, [ RPNValidator.List, RPNValidator.NonnegativeInteger ], [ ] ),

    'shuffle'                       : RPNOperator( shuffleList,
                                                   1, [ RPNValidator.List ], [ ] ),

    'slice'                         : RPNOperator( lambda a, b, c: RPNGenerator( getSlice( a, b, c ) ),
                                                   3, [ RPNValidator.List, RPNValidator.Integer,
                                                        RPNValidator.Integer ], [ ] ),

    'sort'                          : RPNOperator( sortAscending,
                                                   1, [ RPNValidator.List ], [ ] ),

    'sort_descending'               : RPNOperator( sortDescending,
                                                   1, [ RPNValidator.List ], [ ] ),

    'sublist'                       : RPNOperator( lambda a, b, c: RPNGenerator( getSublist( a, b, c ) ),
                                                   3, [ RPNValidator.List, RPNValidator.Integer,
                                                        RPNValidator.Integer ], [ ] ),

    'union'                         : RPNOperator( makeUnion,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'unique'                        : RPNOperator( getUniqueElements,
                                                   1, [ RPNValidator.List ], [ ] ),

    'zero'                          : RPNOperator( getZeroes,
                                                   1, [ RPNValidator.List ], [ ] ),

    # number_theory
    'base'                          : RPNOperator( interpretAsBaseOperator,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    'continued_fraction'            : RPNOperator( convertFromContinuedFraction,
                                                   1, [ RPNValidator.List ], [ ] ),

    'crt'                           : RPNOperator( calculateChineseRemainderTheorem,
                                                   2, [ RPNValidator.List, RPNValidator.List ], [ ] ),

    'frobenius'                     : RPNOperator( getFrobeniusNumber,
                                                   1, [ RPNValidator.List ], [ ] ),

    'geometric_recurrence'          : RPNOperator( lambda a, b, c, d: RPNGenerator( getGeometricRecurrence( a, b, c, d ) ),
                                                   4, [ RPNValidator.List, RPNValidator.List, RPNValidator.List,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'is_friendly'                   : RPNOperator( isFriendly,
                                                   1, [ RPNValidator.List ], [ ] ),

    'linear_recurrence'             : RPNOperator( lambda a, b, c: RPNGenerator( getLinearRecurrence( a, b, c ) ),
                                                   3, [ RPNValidator.List, RPNValidator.List,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'linear_recurrence_with_modulo' : RPNOperator( lambda a, b, c, d: RPNGenerator( getLinearRecurrenceWithModulo( a, b, c, d ) ),
                                                   4, [ RPNValidator.List, RPNValidator.List,
                                                        RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'nth_linear_recurrence'         : RPNOperator( getNthLinearRecurrence,
                                                   3, [ RPNValidator.List, RPNValidator.List,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'nth_linear_recurrence_with_modulo' : RPNOperator( getNthLinearRecurrenceWithModulo,
                                                       4, [ RPNValidator.List, RPNValidator.List,
                                                            RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'solve_frobenius'               : RPNOperator( solveFrobeniusOperator,
                                                   2, [ RPNValidator.List, RPNValidator.PositiveInteger ], [ ] ),

    # powers_and_roots
    'power_tower'                   : RPNOperator( calculatePowerTower,
                                                   1, [ RPNValidator.List ], [ ] ),

    'power_tower2'                  : RPNOperator( calculatePowerTower2,
                                                   1, [ RPNValidator.List ], [ ] ),

    # special
    'echo'                          : RPNOperator( addEchoArgument,
                                                   1, [ RPNValidator.Default ], [ ] ),
}


#******************************************************************************
#
#  operators
#
#  Regular operators expect zero or more single values and if those arguments
#  are lists, rpn will iterate calls to the operator handler for each element
#  in the list.   Multiple lists for arguments are not permutated.  Instead,
#  the operator handler is called for each element in the first list, along
#  with the nth element of each other argument that is also a list.
#
#  Note:  There is something about the way some of the mpmath functions are
#  defined causes them not to work when used in a user-defined function.  So,
#  they are all wrapped in a lambda.
#
#******************************************************************************

operators = {
    # pylint: disable=line-too-long

    # algebra
    'find_polynomial'               : RPNOperator( findPolynomial,
                                                   2, [ RPNValidator.Default, RPNValidator.PositiveInteger ], [ ] ),

    'solve_cubic'                   : RPNOperator( solveCubicPolynomial,
                                                   4, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'solve_quadratic'               : RPNOperator( solveQuadraticPolynomial,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default ], [ ] ),

    'solve_quartic'                 : RPNOperator( solveQuarticPolynomial,
                                                   5, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default ], [ ] ),

    # arithmetic
    'abs'                           : RPNOperator( getAbsoluteValue,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'add'                           : RPNOperator( addOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'ceiling'                       : RPNOperator( getCeiling,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'decrement'                     : RPNOperator( decrement,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'divide'                        : RPNOperator( divideOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'floor'                         : RPNOperator( getFloor,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'gcd2'                          : RPNOperator( getGCDOperator,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'increment'                     : RPNOperator( increment,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'is_divisible'                  : RPNOperator( isDivisibleOperator,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'is_equal'                      : RPNOperator( isEqual,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'is_even'                       : RPNOperator( isEven,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'is_greater'                    : RPNOperator( isGreater,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'is_integer'                    : RPNOperator( isInteger,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'is_kth_power'                  : RPNOperator( isKthPower,
                                                   2, [ RPNValidator.Integer, RPNValidator.PositiveInteger ], [ ] ),

    'is_less'                       : RPNOperator( isLess,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'is_not_equal'                  : RPNOperator( isNotEqual,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'is_not_greater'                : RPNOperator( isNotGreater,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'is_not_less'                   : RPNOperator( isNotLess,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'is_not_zero'                   : RPNOperator( isNotZero,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'is_odd'                        : RPNOperator( isOdd,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'is_power_of_k'                 : RPNOperator( isPower,
                                                   2, [ RPNValidator.Integer, RPNValidator.PositiveInteger ], [ ] ),

    'is_square'                     : RPNOperator( isSquare,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'is_zero'                       : RPNOperator( isZero,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'larger'                        : RPNOperator( getLarger,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'lcm2'                          : RPNOperator( getLCM,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'mantissa'                      : RPNOperator( getMantissa,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'modulo'                        : RPNOperator( getModulo,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'multiply'                      : RPNOperator( multiplyOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'nearest_int'                   : RPNOperator( getNearestInt,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'negative'                      : RPNOperator( getNegative,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'reciprocal'                    : RPNOperator( getReciprocal,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'round'                         : RPNOperator( roundOff,
                                                   1, [ RPNValidator.Real ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'round_by_digits'               : RPNOperator( roundByDigits,
                                                   2, [ RPNValidator.Real, RPNValidator.Integer ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'round_by_value'                : RPNOperator( roundByValueOperator,
                                                   2, [ RPNValidator.Real, RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sign'                          : RPNOperator( getSign,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'smaller'                       : RPNOperator( getSmaller,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'subtract'                      : RPNOperator( subtractOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    # astronomy
    'angular_separation'            : RPNOperator( getAngularSeparation,
                                                   4, [ RPNValidator.AstronomicalObject, RPNValidator.AstronomicalObject,
                                                        RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'angular_size'                  : RPNOperator( getAngularSize,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'antitransit_time'              : RPNOperator( getAntitransitTime,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'astronomical_dawn'             : RPNOperator( getNextAstronomicalDawn,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'astronomical_dusk'             : RPNOperator( getNextAstronomicalDusk,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'autumnal_equinox'              : RPNOperator( getAutumnalEquinox,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'dawn'                          : RPNOperator( getNextCivilDawn,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'day_time'                      : RPNOperator( getDayTime,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'distance_from_earth'           : RPNOperator( getDistanceFromEarth,
                                                   2, [ RPNValidator.AstronomicalObject, RPNValidator.DateTime ], [ ] ),

    'dusk'                          : RPNOperator( getNextCivilDusk,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'eclipse_totality'              : RPNOperator( getEclipseTotality,
                                                   4, [ RPNValidator.AstronomicalObject, RPNValidator.AstronomicalObject,
                                                        RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'moonrise'                      : RPNOperator( getNextMoonRise,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'moonset'                       : RPNOperator( getNextMoonSet,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'moon_antitransit'              : RPNOperator( getNextMoonAntitransit,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'moon_phase'                    : RPNOperator( getMoonPhase,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'moon_transit'                  : RPNOperator( getNextMoonTransit,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'nautical_dawn'                 : RPNOperator( getNextNauticalDawn,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'nautical_dusk'                 : RPNOperator( getNextNauticalDusk,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'next_antitransit'              : RPNOperator( getNextAntitransit,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'next_first_quarter_moon'       : RPNOperator( getNextFirstQuarterMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'next_full_moon'                : RPNOperator( getNextFullMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'next_last_quarter_moon'        : RPNOperator( getNextLastQuarterMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'next_new_moon'                 : RPNOperator( getNextNewMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'next_rising'                   : RPNOperator( getNextRising,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'next_setting'                  : RPNOperator( getNextSetting,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'next_transit'                  : RPNOperator( getNextTransit,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'night_time'                    : RPNOperator( getNightTime,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'previous_antitransit'          : RPNOperator( getPreviousAntitransit,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'previous_first_quarter_moon'   : RPNOperator( getPreviousFirstQuarterMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'previous_full_moon'            : RPNOperator( getPreviousFullMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'previous_last_quarter_moon'    : RPNOperator( getPreviousLastQuarterMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'previous_new_moon'             : RPNOperator( getPreviousNewMoon,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'previous_rising'               : RPNOperator( getPreviousRising,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'previous_setting'              : RPNOperator( getPreviousSetting,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'previous_transit'              : RPNOperator( getPreviousTransit,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'sky_location'                  : RPNOperator( getSkyLocation,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'solar_noon'                    : RPNOperator( getSolarNoon,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'summer_solstice'               : RPNOperator( getSummerSolstice,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sunrise'                       : RPNOperator( getNextSunrise,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'sunset'                        : RPNOperator( getNextSunset,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'sun_antitransit'               : RPNOperator( getNextSunAntitransit,
                                                   2, [ RPNValidator.Location, RPNValidator.DateTime ], [ ] ),

    'transit_time'                  : RPNOperator( getTransitTime,
                                                   3, [ RPNValidator.AstronomicalObject, RPNValidator.Location,
                                                        RPNValidator.DateTime ], [ ] ),

    'vernal_equinox'                : RPNOperator( getVernalEquinox,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'winter_solstice'               : RPNOperator( getWinterSolstice,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    # astronomy - heavenly body operators
    'sun'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Sun( ) ),
                                                   0, [ ], [ ] ),

    'mercury'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mercury( ) ),
                                                   0, [ ], [ ] ),

    'venus'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Venus( ) ),
                                                   0, [ ], [ ] ),

    'moon'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Moon( ) ),
                                                   0, [ ], [ ] ),

    'mars'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mars( ) ),
                                                   0, [ ], [ ] ),

    'jupiter'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Jupiter( ) ),
                                                   0, [ ], [ ] ),

    'saturn'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Saturn( ) ),
                                                   0, [ ], [ ] ),

    'uranus'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Uranus( ) ),
                                                   0, [ ], [ ] ),

    'neptune'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Neptune( ) ),
                                                   0, [ ], [ ] ),

    'pluto'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Pluto( ) ),
                                                   0, [ ], [ ] ),

    # bitwise
    'bitwise_and'                   : RPNOperator( getBitwiseAnd,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_nand'                  : RPNOperator( getBitwiseNand,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_nor'                   : RPNOperator( getBitwiseNor,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_not'                   : RPNOperator( getInvertedBits,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_or'                    : RPNOperator( getBitwiseOr,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_xnor'                  : RPNOperator( getBitwiseXnor,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'bitwise_xor'                   : RPNOperator( getBitwiseXor,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'count_bits'                    : RPNOperator( getBitCountOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'parity'                        : RPNOperator( getParity,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'shift_left'                    : RPNOperator( shiftLeft,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'shift_right'                   : RPNOperator( shiftRight,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    # calendar
    'advent'                        : RPNOperator( calculateAdvent,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'ascension'                     : RPNOperator( calculateAscensionThursday,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'ash_wednesday'                 : RPNOperator( calculateAshWednesday,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'calendar'                      : RPNOperator( generateMonthCalendar,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'christmas'                     : RPNOperator( getChristmasDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'columbus_day'                  : RPNOperator( calculateColumbusDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'dst_end'                       : RPNOperator( calculateDSTEnd,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'dst_start'                     : RPNOperator( calculateDSTStart,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'easter'                        : RPNOperator( calculateEaster,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'election_day'                  : RPNOperator( calculateElectionDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'epiphany'                      : RPNOperator( getEpiphanyDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'fathers_day'                   : RPNOperator( calculateFathersDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'from_bahai'                    : RPNOperator( convertBahaiDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_ethiopian'                : RPNOperator( convertEthiopianDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_french_republican'        : RPNOperator( convertFrenchRepublicanDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_hebrew'                   : RPNOperator( convertHebrewDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_indian_civil'             : RPNOperator( convertIndianCivilDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_islamic'                  : RPNOperator( convertIslamicDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_julian'                   : RPNOperator( convertJulianDate,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_mayan'                    : RPNOperator( convertMayanDate,
                                                   5, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'from_persian'                  : RPNOperator( convertPersianDate,
                                                   3, [ RPNValidator.Integer, RPNValidator.Integer,
                                                        RPNValidator.Integer ], [ ] ),

    'good_friday'                   : RPNOperator( calculateGoodFriday,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'independence_day'              : RPNOperator( getIndependenceDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'iso_date'                      : RPNOperator( getISODate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'labor_day'                     : RPNOperator( calculateLaborDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'martin_luther_king_day'        : RPNOperator( calculateMartinLutherKingDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'memorial_day'                  : RPNOperator( calculateMemorialDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'mothers_day'                   : RPNOperator( calculateMothersDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'new_years_day'                 : RPNOperator( getNewYearsDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_weekday'                   : RPNOperator( calculateNthWeekdayOfMonthOperator,
                                                   4, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.Integer, RPNValidator.PositiveInteger ], [ ] ),

    'nth_weekday_of_year'           : RPNOperator( calculateNthWeekdayOfYear,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.Integer,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'pentecost'                     : RPNOperator( calculatePentecostSunday,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'presidents_day'                : RPNOperator( calculatePresidentsDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'thanksgiving'                  : RPNOperator( calculateThanksgiving,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'to_bahai'                      : RPNOperator( getBahaiCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_bahai_name'                 : RPNOperator( getBahaiCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_ethiopian'                  : RPNOperator( getEthiopianCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_ethiopian_name'             : RPNOperator( getEthiopianCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_french_republican'          : RPNOperator( getFrenchRepublicanCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_french_republican_name'     : RPNOperator( getFrenchRepublicanCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_hebrew'                     : RPNOperator( getHebrewCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_hebrew_name'                : RPNOperator( getHebrewCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_indian_civil'               : RPNOperator( getIndianCivilCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_indian_civil_name'          : RPNOperator( getIndianCivilCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_islamic'                    : RPNOperator( getIslamicCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_islamic_name'               : RPNOperator( getIslamicCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_iso'                        : RPNOperator( getISODate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_iso_name'                   : RPNOperator( getISODateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_julian'                     : RPNOperator( getJulianCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_julian_day'                 : RPNOperator( getJulianDay,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_lilian_day'                 : RPNOperator( getLilianDay,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_mayan'                      : RPNOperator( getMayanCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_ordinal_date'               : RPNOperator( getOrdinalDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_persian'                    : RPNOperator( getPersianCalendarDate,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'to_persian_name'               : RPNOperator( getPersianCalendarDateName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'veterans_day'                  : RPNOperator( getVeteransDay,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'weekday'                       : RPNOperator( getWeekday,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'weekday_name'                  : RPNOperator( getWeekdayName,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'year_calendar'                 : RPNOperator( generateYearCalendar,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    # chemistry
    'atomic_number'                 : RPNOperator( getAtomicNumber,
                                                   1, [ RPNValidator.String ], [ ] ),

    'atomic_symbol'                 : RPNOperator( getAtomicSymbol,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'atomic_weight'                 : RPNOperator( getAtomicWeight,
                                                   1, [ RPNValidator.String ], [ ] ),

    'element_block'                 : RPNOperator( getElementBlock,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_boiling_point'         : RPNOperator( getElementBoilingPoint,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_density'               : RPNOperator( getElementDensity,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_description'           : RPNOperator( getElementDescription,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_group'                 : RPNOperator( getElementGroup,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_melting_point'         : RPNOperator( getElementMeltingPoint,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_name'                  : RPNOperator( getElementName,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_occurrence'            : RPNOperator( getElementOccurrence,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_period'                : RPNOperator( getElementPeriod,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'element_state'                 : RPNOperator( getElementState,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'molar_mass'                    : RPNOperator( getMolarMass,
                                                   1, [ RPNValidator.String ], [ ] ),

    # combinatoric
    'arrangements'                  : RPNOperator( getArrangements,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'bell_polynomial'               : RPNOperator( getBellPolynomial,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'binomial'                      : RPNOperator( getBinomial,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'combinations'                  : RPNOperator( getCombinations,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'compositions'                  : RPNOperator( getCompositions,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'debruijn_sequence'             : RPNOperator( getDeBruijnSequence,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'get_partitions'                : RPNOperator( getIntegerPartitions,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'get_partitions_with_limit'     : RPNOperator( getPartitionsWithLimit,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'lah_number'                    : RPNOperator( getLahNumber,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'nth_menage'                    : RPNOperator( getNthMenageNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'multifactorial'                : RPNOperator( getNthMultifactorial,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'narayana_number'               : RPNOperator( getNarayanaNumberOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'nth_apery'                     : RPNOperator( getNthAperyNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_bell'                      : RPNOperator( getNthBell,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_bernoulli'                 : RPNOperator( getNthBernoulli,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_catalan'                   : RPNOperator( getNthCatalanNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_delannoy'                  : RPNOperator( getNthDelannoyNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_motzkin'                   : RPNOperator( getNthMotzkinNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_pell'                      : RPNOperator( getNthPellNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_schroeder'                 : RPNOperator( getNthSchroederNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_schroeder_hipparchus'      : RPNOperator( getNthSchroederHipparchusNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_sylvester'                 : RPNOperator( getNthSylvesterNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'partitions'                    : RPNOperator( getPartitionNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'permutations'                  : RPNOperator( getPermutations,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'stirling1_number'              : RPNOperator( getStirling1Number,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'stirling2_number'              : RPNOperator( getStirling2Number,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    # complex
    'argument'                      : RPNOperator( getArgument,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'conjugate'                     : RPNOperator( getConjugate,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'imaginary'                     : RPNOperator( getImaginary,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'real'                          : RPNOperator( getReal,
                                                   1, [ RPNValidator.Default ], [ ] ),

    # conversion
    'char'                          : RPNOperator( convertToChar,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'dhms'                          : RPNOperator( convertToDHMS,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'dms'                           : RPNOperator( convertToDMS,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'double'                        : RPNOperator( convertToDouble,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'float'                         : RPNOperator( convertToFloat,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'from_unix_time'                : RPNOperator( convertFromUnixTime,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'hms'                           : RPNOperator( convertToHMS,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'integer'                       : RPNOperator( convertToSignedIntOperator,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'invert_units'                  : RPNOperator( invertUnits,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'long'                          : RPNOperator( convertToLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'longlong'                      : RPNOperator( convertToLongLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'quadlong'                      : RPNOperator( convertToQuadLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'short'                         : RPNOperator( convertToShort,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'to_unix_time'                  : RPNOperator( convertToUnixTime,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'uchar'                         : RPNOperator( convertToUnsignedChar,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'uinteger'                      : RPNOperator( convertToUnsignedInt,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'ulong'                         : RPNOperator( convertToUnsignedLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'ulonglong'                     : RPNOperator( convertToUnsignedLongLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'undouble'                      : RPNOperator( interpretAsDouble,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'unfloat'                       : RPNOperator( interpretAsFloat,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'uquadlong'                     : RPNOperator( convertToUnsignedQuadLong,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'ushort'                        : RPNOperator( convertToUnsignedShort,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'ydhms'                         : RPNOperator( convertToYDHMS,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),
    # date_time
    'get_year'                      : RPNOperator( getYear,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'get_month'                     : RPNOperator( getMonth,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'get_day'                       : RPNOperator( getDay,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'get_hour'                      : RPNOperator( getHour,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'get_minute'                    : RPNOperator( getMinute,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'get_second'                    : RPNOperator( getSecond,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'iso_day'                       : RPNOperator( getISODay,
                                                   1, [ RPNValidator.DateTime ], [ ] ),

    'now'                           : RPNOperator( RPNDateTime.getNow,
                                                   0, [ ], [ ] ),

    'today'                         : RPNOperator( getToday,
                                                   0, [ ], [ ] ),

    'tomorrow'                      : RPNOperator( getTomorrow,
                                                   0, [ ], [ ] ),

    'yesterday'                     : RPNOperator( getYesterday,
                                                   0, [ ], [ ] ),

    # figurate
    'centered_cube'                 : RPNOperator( getNthCenteredCubeNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_decagonal'            : RPNOperator( getNthCenteredDecagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_dodecahedral'         : RPNOperator( getNthCenteredDodecahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_heptagonal'           : RPNOperator( getNthCenteredHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_hexagonal'            : RPNOperator( getNthCenteredHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_icosahedral'          : RPNOperator( getNthCenteredIcosahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_nonagonal'            : RPNOperator( getNthCenteredNonagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_octagonal'            : RPNOperator( getNthCenteredOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_octahedral'           : RPNOperator( getNthCenteredOctahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_pentagonal'           : RPNOperator( getNthCenteredPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_polygonal'            : RPNOperator( getNthCenteredPolygonalNumberOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'centered_square'               : RPNOperator( getNthCenteredSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_tetrahedral'          : RPNOperator( getNthCenteredTetrahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'centered_triangular'           : RPNOperator( getNthCenteredTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal'                     : RPNOperator( getNthDecagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_centered_square'     : RPNOperator( getNthDecagonalCenteredSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_heptagonal'          : RPNOperator( getNthDecagonalHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_hexagonal'           : RPNOperator( getNthDecagonalHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_nonagonal'           : RPNOperator( getNthDecagonalNonagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_octagonal'           : RPNOperator( getNthDecagonalOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_pentagonal'          : RPNOperator( getNthDecagonalPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'decagonal_triangular'          : RPNOperator( getNthDecagonalTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'dodecahedral'                  : RPNOperator( getNthDodecahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'generalized_pentagonal'        : RPNOperator( getNthGeneralizedPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptagonal'                    : RPNOperator( getNthHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptagonal_hexagonal'          : RPNOperator( getNthHeptagonalHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptagonal_pentagonal'         : RPNOperator( getNthHeptagonalPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptagonal_square'             : RPNOperator( getNthHeptagonalSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptagonal_triangular'         : RPNOperator( getNthHeptagonalTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hexagonal'                     : RPNOperator( getNthHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hexagonal_pentagonal'          : RPNOperator( getNthHexagonalPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hexagonal_square'              : RPNOperator( getNthHexagonalSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'icosahedral'                   : RPNOperator( getNthIcosahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal'                     : RPNOperator( getNthNonagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_heptagonal'          : RPNOperator( getNthNonagonalHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_hexagonal'           : RPNOperator( getNthNonagonalHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_octagonal'           : RPNOperator( getNthNonagonalOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_pentagonal'          : RPNOperator( getNthNonagonalPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_square'              : RPNOperator( getNthNonagonalSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nonagonal_triangular'          : RPNOperator( getNthNonagonalTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_decagonal'        : RPNOperator( findCenteredDecagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_heptagonal'       : RPNOperator( findCenteredHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_hexagonal'        : RPNOperator( findCenteredHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_nonagonal'        : RPNOperator( findCenteredNonagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_octagonal'        : RPNOperator( findCenteredOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_pentagonal'       : RPNOperator( findCenteredPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_polygonal'        : RPNOperator( findCenteredPolygonalNumberOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_square'           : RPNOperator( findCenteredSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_centered_triangular'       : RPNOperator( findCenteredTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_decagonal'                 : RPNOperator( findDecagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_heptagonal'                : RPNOperator( findHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_hexagonal'                 : RPNOperator( findHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_nonagonal'                 : RPNOperator( findNonagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_octagonal'                 : RPNOperator( findOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_pentagonal'                : RPNOperator( findPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_polygonal'                 : RPNOperator( findPolygonalNumberOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'nth_square'                    : RPNOperator( findSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_triangular'                : RPNOperator( findTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal'                     : RPNOperator( getNthOctagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal_heptagonal'          : RPNOperator( getNthOctagonalHeptagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal_hexagonal'           : RPNOperator( getNthOctagonalHexagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal_pentagonal'          : RPNOperator( getNthOctagonalPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal_square'              : RPNOperator( getNthOctagonalSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octagonal_triangular'          : RPNOperator( getNthOctagonalTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octahedral'                    : RPNOperator( getNthOctahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pentagonal'                    : RPNOperator( getNthPentagonalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pentagonal_square'             : RPNOperator( getNthPentagonalSquareNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pentagonal_triangular'         : RPNOperator( getNthPentagonalTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pentatope'                     : RPNOperator( getNthPentatopeNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'polygonal'                     : RPNOperator( getNthPolygonalNumberOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'polygonal_pyramidal'           : RPNOperator( getNthPolygonalPyramidalNumber,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'polytope'                      : RPNOperator( getNthPolytopeNumber,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'pyramidal'                     : RPNOperator( getNthPyramidalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'rhombic_dodecahedral'          : RPNOperator( getNthRhombicDodecahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'square_triangular'             : RPNOperator( getNthSquareTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'star'                          : RPNOperator( getNthStarNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'stella_octangula'              : RPNOperator( getNthStellaOctangulaNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'tetrahedral'                   : RPNOperator( getNthTetrahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'triangular'                    : RPNOperator( getNthTriangularNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'truncated_octahedral'          : RPNOperator( getNthTruncatedOctahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'truncated_tetrahedral'         : RPNOperator( getNthTruncatedTetrahedralNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    # function
    #'break_on'                      : RPNOperator( breakOnCondition,
    #                                               3, [ RPNValidator.Default, RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'eval0'                         : RPNOperator( evaluateFunction0,
                                                   1, [ RPNValidator.Function ], [ ] ),

    'eval'                          : RPNOperator( evaluateFunction,
                                                   2, [ RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'eval2'                         : RPNOperator( evaluateFunction2,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Function ], [ ] ),

    'eval3'                         : RPNOperator( evaluateFunction3,
                                                   4, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'eval_list'                     : RPNOperator( evaluateListFunction,
                                                   2, [ RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'eval_list2'                    : RPNOperator( evaluateListFunction2,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Function ], [ ] ),

    'eval_list3'                    : RPNOperator( evaluateListFunction3,
                                                   4, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'filter_integers'               : RPNOperator( filterIntegers,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.Function ], [ ] ),

    'function'                      : RPNOperator( createUserFunction,
                                                   2, [ RPNValidator.String, RPNValidator.Function ], [ ] ),

    'limit'                         : RPNOperator( evaluateLimit,
                                                   2, [ RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'limitn'                        : RPNOperator( evaluateReverseLimit,
                                                   2, [ RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'nprod'                         : RPNOperator( evaluateProduct,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Function ], [ ] ),

    'nsum'                          : RPNOperator( evaluateSum,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Function ], [ ] ),

    'plot'                          : RPNOperator( plotFunction,
                                                   3, [ RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Function ], [ ] ),

    'plot2'                         : RPNOperator( plot2DFunction,
                                                   5, [ RPNValidator.Default, RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'plot_complex'                  : RPNOperator( plotComplexFunction,
                                                   5, [ RPNValidator.Default, RPNValidator.Default, RPNValidator.Default,
                                                        RPNValidator.Default, RPNValidator.Function ], [ ] ),

    'recurrence'                    : RPNOperator( evaluateRecurrence,
                                                   3, [ RPNValidator.Default, RPNValidator.PositiveInteger, RPNValidator.Function ], [ ] ),

    'repeat'                        : RPNOperator( repeat,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.Function ], [ ] ),

    'sequence'                      : RPNOperator( getSequence,
                                                   3, [ RPNValidator.Default, RPNValidator.NonnegativeInteger, RPNValidator.Function ], [ ] ),

    # geography
    'geographic_distance'           : RPNOperator( getGeographicDistance,
                                                   2, [ RPNValidator.Location, RPNValidator.Location ], [ ] ),

    'get_timezone'                  : RPNOperator( getTimeZone,
                                                   1, [ RPNValidator.Location ], [ ] ),

    'lat_long'                      : RPNOperator( makeLocation,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'location_info'                 : RPNOperator( getLocationInfo,
                                                   1, [ RPNValidator.String ], [ ] ),

    # geometry
    'antiprism_area'                : RPNOperator( getAntiprismSurfaceArea,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal ], [ ] ),

    'antiprism_volume'              : RPNOperator( getAntiprismVolume,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal ], [ ] ),

    'cone_area'                     : RPNOperator( getConeSurfaceArea,
                                                   2, [ RPNValidator.NonnegativeReal, RPNValidator.NonnegativeReal ], [ ] ),

    'cone_volume'                   : RPNOperator( getConeVolume,
                                                   2, [ RPNValidator.NonnegativeReal, RPNValidator.NonnegativeReal ], [ ] ),

    'dodecahedron_area'             : RPNOperator( getDodecahedronSurfaceArea,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'dodecahedron_volume'           : RPNOperator( getDodecahedronVolume,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'hypotenuse'                    : RPNOperator( calculateHypotenuse,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'icosahedron_area'              : RPNOperator( getIcosahedronSurfaceArea,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'icosahedron_volume'            : RPNOperator( getIcosahedronVolume,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'k_sphere_area'                 : RPNOperator( getKSphereSurfaceAreaOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'k_sphere_radius'               : RPNOperator( getKSphereRadiusOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'k_sphere_volume'               : RPNOperator( getKSphereVolumeOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'octahedron_area'               : RPNOperator( getOctahedronSurfaceArea,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'octahedron_volume'             : RPNOperator( getOctahedronVolume,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'polygon_area'                  : RPNOperator( getRegularPolygonAreaOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.Measurement ], [ ] ),

    'prism_area'                    : RPNOperator( getPrismSurfaceArea,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal,
                                                        RPNValidator.NonnegativeReal ], [ ] ),

    'prism_volume'                  : RPNOperator( getPrismVolume,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.NonnegativeReal,
                                                        RPNValidator.NonnegativeReal ], [ ] ),

    'sphere_area'                   : RPNOperator( getSphereArea,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sphere_radius'                 : RPNOperator( getSphereRadius,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sphere_volume'                 : RPNOperator( getSphereVolume,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'tetrahedron_area'              : RPNOperator( getTetrahedronSurfaceArea,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'tetrahedron_volume'            : RPNOperator( getTetrahedronVolume,
                                                   1, [ RPNValidator.NonnegativeReal ], [ ] ),

    'torus_area'                    : RPNOperator( getTorusSurfaceArea,
                                                   2, [ RPNValidator.NonnegativeReal, RPNValidator.NonnegativeReal ], [ ] ),

    'torus_volume'                  : RPNOperator( getTorusVolume,
                                                   2, [ RPNValidator.NonnegativeReal, RPNValidator.NonnegativeReal ], [ ] ),

    'triangle_area'                 : RPNOperator( getTriangleArea,
                                                   3, [ RPNValidator.NonnegativeReal, RPNValidator.NonnegativeReal,
                                                        RPNValidator.NonnegativeReal ], [ ] ),

    # lexicographic
    'add_digits'                    : RPNOperator( addDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'build_numbers'                 : RPNOperator( buildNumbers,
                                                   1, [ RPNValidator.String ], [ ] ),

    'build_step_numbers'            : RPNOperator( buildStepNumbers,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'count_different_digits'        : RPNOperator( countDifferentDigits,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'count_digits'                  : RPNOperator( countDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'cyclic_permutations'           : RPNOperator( getCyclicPermutations,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'digits'                        : RPNOperator( getDigitCount,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'duplicate_digits'              : RPNOperator( duplicateDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'duplicate_number'              : RPNOperator( duplicateNumber,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'erdos_persistence'             : RPNOperator( getErdosPersistence,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'find_palindrome'               : RPNOperator( findPalindrome,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'get_base_k_digits'             : RPNOperator( getBaseKDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.PositiveInteger ], [ ] ),

    'get_digits'                    : RPNOperator( getDigits,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'get_left_digits'               : RPNOperator( getLeftDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'get_left_truncations'          : RPNOperator( getLeftTruncationsGenerator,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'get_nonzero_base_k_digits'     : RPNOperator( getNonzeroBaseKDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'get_nonzero_digits'            : RPNOperator( getNonzeroDigits,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'get_right_digits'              : RPNOperator( getRightDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger ], [ ] ),

    'get_right_truncations'         : RPNOperator( getRightTruncationsGenerator,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'has_any_digits'                : RPNOperator( containsAnyDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'has_digits'                    : RPNOperator( containsDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'has_only_digits'               : RPNOperator( containsOnlyDigits,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'is_automorphic'                : RPNOperator( isAutomorphic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_base_k_pandigital'          : RPNOperator( isBaseKPandigital,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_base_k_smith_number'        : RPNOperator( isBaseKSmithNumber,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_bouncy'                     : RPNOperator( isBouncy,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_decreasing'                 : RPNOperator( isDecreasing,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_digital_palindrome'         : RPNOperator( isPalindromeOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_digital_permutation'        : RPNOperator( isDigitalPermutation,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_generalized_dudeney'        : RPNOperator( isGeneralizedDudeneyNumber,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_harshad'                    : RPNOperator( isHarshadNumber,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_increasing'                 : RPNOperator( isIncreasing,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_kaprekar'                   : RPNOperator( isKaprekarNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_k_morphic'                  : RPNOperator( isKMorphicOperator,
                                                   2, [ RPNValidator.Integer, RPNValidator.PositiveInteger ], [ ] ),

    'is_k_narcissistic'             : RPNOperator( isBaseKNarcissistic,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_narcissistic'               : RPNOperator( isNarcissistic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_order_k_smith_number'       : RPNOperator( isOrderKSmithNumber,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_pandigital'                 : RPNOperator( isPandigital,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_pddi'                       : RPNOperator( isPerfectDigitToDigitInvariant,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_pdi'                        : RPNOperator( isPerfectDigitalInvariant,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_smith_number'               : RPNOperator( isSmithNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_step_number'                : RPNOperator( isStepNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_sum_product'                : RPNOperator( isSumProductNumber,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_trimorphic'                 : RPNOperator( isTrimorphic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'k_persistence'                 : RPNOperator( getKPersistence,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'multiply_digits'               : RPNOperator( multiplyDigits,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'multiply_digit_powers'         : RPNOperator( multiplyDigitPowers,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'multiply_nonzero_digits'       : RPNOperator( multiplyNonzeroDigits,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'multiply_nonzero_digit_powers' : RPNOperator( multiplyNonzeroDigitPowers,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'permute_digits'                : RPNOperator( permuteDigits,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'persistence'                   : RPNOperator( getPersistence,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'replace_digits'                : RPNOperator( replaceDigits,
                                                   3, [ RPNValidator.Integer, RPNValidator.NonnegativeInteger,
                                                        RPNValidator.NonnegativeInteger ], [ ] ),

    'reverse_digits'                : RPNOperator( reverseDigitsOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'rotate_digits_left'            : RPNOperator( rotateDigitsLeft,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.Integer ], [ ] ),

    'rotate_digits_right'           : RPNOperator( rotateDigitsRight,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.Integer ], [ ] ),

    'show_erdos_persistence'        : RPNOperator( showErdosPersistence,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'show_k_persistence'            : RPNOperator( showKPersistence,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'show_persistence'              : RPNOperator( showPersistence,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'square_digit_chain'            : RPNOperator( generateSquareDigitChain,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sum_digits'                    : RPNOperator( sumDigits,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    # list
    'exponential_range'             : RPNOperator( createExponentialRange,
                                                   3, [ RPNValidator.Real, RPNValidator.Real,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'geometric_range'               : RPNOperator( createGeometricRange,
                                                   3, [ RPNValidator.Real, RPNValidator.Real,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'interval_range'                : RPNOperator( createIntervalRangeOperator,
                                                   3, [ RPNValidator.Real, RPNValidator.Real,
                                                        RPNValidator.Real ], [ ] ),

    'range'                         : RPNOperator( createRange,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'sized_range'                   : RPNOperator( createSizedRangeOperator,
                                                   3, [ RPNValidator.Real, RPNValidator.Real,
                                                        RPNValidator.Real ], [ ] ),

    # logarithms
    'lambertw'                      : RPNOperator( getLambertW,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'li'                            : RPNOperator( getLI,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'log'                           : RPNOperator( getLog,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'log10'                         : RPNOperator( getLog10,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'log2'                          : RPNOperator( getLog2,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'logxy'                         : RPNOperator( getLogXY,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'polyexp'                       : RPNOperator( getPolyexp,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'polylog'                       : RPNOperator( getPolylog,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    # logical
    'and'                           : RPNOperator( andOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'nand'                          : RPNOperator( nandOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'nor'                           : RPNOperator( norOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'not'                           : RPNOperator( notOperand,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'or'                            : RPNOperator( orOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'xnor'                          : RPNOperator( xnorOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'xor'                           : RPNOperator( xorOperands,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    # number_theory
    'abundance'                     : RPNOperator( getAbundanceOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'abundance_ratio'               : RPNOperator( getAbundanceRatio,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'ackermann_number'              : RPNOperator( calculateAckermannFunctionOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'aliquot'                       : RPNOperator( getAliquotSequence,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'aliquot_limit'                 : RPNOperator( getLimitedAliquotSequence,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'alternating_factorial'         : RPNOperator( getNthAlternatingFactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'alternating_harmonic_fraction' : RPNOperator( getAlternatingHarmonicFraction,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'barnesg'                       : RPNOperator( getBarnesG,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'beta'                          : RPNOperator( getBeta,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'calkin_wilf'                   : RPNOperator( getNthCalkinWilf,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'collatz'                       : RPNOperator( getCollatzSequence,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'count_divisors'                : RPNOperator( getDivisorCountOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'cyclotomic'                    : RPNOperator( getCyclotomic,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.Default ], [ ] ),

    'digamma'                       : RPNOperator( getDigamma,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'digital_root'                  : RPNOperator( getDigitalRoot,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'divisors'                      : RPNOperator( getDivisorsOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'double_factorial'              : RPNOperator( getNthDoubleFactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'egyptian_fractions'            : RPNOperator( getGreedyEgyptianFraction,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'eta'                           : RPNOperator( getAltZeta,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'euler_brick'                   : RPNOperator( makeEulerBrick,
                                                   3, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger,
                                                        RPNValidator.PositiveInteger ], [ ] ),

    'euler_phi'                     : RPNOperator( getEulerPhi,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'factor'                        : RPNOperator( getFactorsOperator,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'factorial'                     : RPNOperator( getNthFactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'fibonacci'                     : RPNOperator( getNthFibonacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'fibonorial'                    : RPNOperator( getNthFibonorial,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'find_sum_of_cubes'             : RPNOperator( findNthSumOfCubes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'find_sum_of_squares'           : RPNOperator( findNthSumOfSquares,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'fraction'                      : RPNOperator( interpretAsFraction,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'gamma'                         : RPNOperator( getGamma,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'generate_polydivisibles'       : RPNOperator( generatePolydivisibles,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'harmonic_fraction'             : RPNOperator( getHarmonicFraction,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'harmonic_residue'              : RPNOperator( getHarmonicResidueOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'heptanacci'                    : RPNOperator( getNthHeptanacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hexanacci'                     : RPNOperator( getNthHexanacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hurwitz_zeta'                  : RPNOperator( getHurwitzZeta,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'hyperfactorial'                : RPNOperator( getNthHyperfactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_abundant'                   : RPNOperator( isAbundant,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_achilles'                   : RPNOperator( isAchillesNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_antiharmonic'               : RPNOperator( isAntiharmonic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_carmichael'                 : RPNOperator( isCarmichaelNumberOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_composite'                  : RPNOperator( isComposite,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_deficient'                  : RPNOperator( isDeficient,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_harmonic_divisor_number'    : RPNOperator( isHarmonicDivisorNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_k_hyperperfect'             : RPNOperator( isKHyperperfect,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_k_perfect'                  : RPNOperator( isKPerfect,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'is_k_semiprime'                : RPNOperator( isKSemiprimeOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_k_sphenic'                  : RPNOperator( isKSphenicOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_perfect'                    : RPNOperator( isPerfect,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_pernicious'                 : RPNOperator( isPernicious,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_polydivisible'              : RPNOperator( isPolydivisible,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_powerful'                   : RPNOperator( isPowerful,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_prime'                      : RPNOperator( isPrimeOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_pronic'                     : RPNOperator( isPronic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_rough'                      : RPNOperator( isRoughOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PrimeInteger ], [ ] ),

    'is_ruth_aaron'                 : RPNOperator( isRuthAaronNumber,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_semiprime'                  : RPNOperator( isSemiprime,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_smooth'                     : RPNOperator( isSmoothOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PrimeInteger ], [ ] ),

    'is_sphenic'                    : RPNOperator( isSphenic,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_squarefree'                 : RPNOperator( isSquareFree,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'is_strong_pseudoprime'         : RPNOperator( isStrongPseudoprime,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'is_unusual'                    : RPNOperator( isUnusual,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'k_fibonacci'                   : RPNOperator( getNthKFibonacciNumber,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'leyland_number'                : RPNOperator( getLeylandNumber,
                                                   2, [ RPNValidator.Real, RPNValidator.Real ], [ ] ),

    'log_gamma'                     : RPNOperator( getLogGamma,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'lucas'                         : RPNOperator( getNthLucasNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'make_continued_fraction'       : RPNOperator( makeContinuedFraction,
                                                   2, [ RPNValidator.Real, RPNValidator.PositiveInteger ], [ ] ),

    'make_pyth_3'                   : RPNOperator( makePythagoreanTriple,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger], [ ] ),

    'make_pyth_4'                   : RPNOperator( makePythagoreanQuadruple,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'nth_carol'                     : RPNOperator( getNthCarolNumber,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'nth_harmonic_number'           : RPNOperator( getNthHarmonicNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_jacobsthal'                : RPNOperator( getNthJacobsthalNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_k_thabit'                  : RPNOperator( getNthKThabitNumber,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'nth_k_thabit_2'                : RPNOperator( getNthKThabit2Number,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'nth_kynea'                     : RPNOperator( getNthKyneaNumber,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'nth_leonardo'                  : RPNOperator( getNthLeonardoNumber,
                                                   1, [ RPNValidator.Real ], [ ] ),

    'nth_mersenne_exponent'         : RPNOperator( getNthMersenneExponent,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_mersenne_prime'            : RPNOperator( getNthMersennePrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_merten'                    : RPNOperator( getNthMerten,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_mobius'                    : RPNOperator( getNthMobiusNumberOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_padovan'                   : RPNOperator( getNthPadovanNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_perfect_number'            : RPNOperator( getNthPerfectNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_stern'                     : RPNOperator( getNthSternNumberOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_thabit'                    : RPNOperator( getNthThabitNumber,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_thabit_2'                  : RPNOperator( getNthThabit2Number,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_thue_morse'                : RPNOperator( getNthThueMorseNumberOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octanacci'                     : RPNOperator( getNthOctanacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pascal_triangle'               : RPNOperator( getNthPascalLine,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pentanacci'                    : RPNOperator( getNthPentanacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'phitorial'                     : RPNOperator( getNthPhitorial,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'polygamma'                     : RPNOperator( getPolygamma,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.Default ], [ ] ),

    'polygorial'                    : RPNOperator( getNthKPolygorial,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.NonnegativeInteger ], [ ] ),

    'primorial'                     : RPNOperator( getNthPrimorial,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'pythagorean_triples'           : RPNOperator( makePythagoreanTriples,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'radical'                       : RPNOperator( getRadical,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'relatively_prime'              : RPNOperator( areRelativelyPrimeOperator,
                                                   2, [ RPNValidator.Integer, RPNValidator.Integer ], [ ] ),

    'repunit'                       : RPNOperator( getNthBaseKRepunit,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'reversal_addition'             : RPNOperator( getNthReversalAddition,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'sigma'                         : RPNOperator( getSigmaOperator,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'sigma_k'                       : RPNOperator( getSigmaKOperator,
                                                   2, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger ], [ ] ),

    'subfactorial'                  : RPNOperator( getNthSubfactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'sums_of_k_powers'              : RPNOperator( findSumsOfKPowers,
                                                   3, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'sums_of_k_nonzero_powers'      : RPNOperator( findSumsOfKNonzeroPowers,
                                                   3, [ RPNValidator.NonnegativeInteger, RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'superfactorial'                : RPNOperator( getNthSuperfactorial,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'tetranacci'                    : RPNOperator( getNthTetranacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'tribonacci'                    : RPNOperator( getNthTribonacci,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'trigamma'                      : RPNOperator( getTrigamma,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'unit_roots'                    : RPNOperator( getUnitRoots,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'zeta'                          : RPNOperator( getZeta,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'zeta_zero'                     : RPNOperator( getNthZetaZero,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    # physics
    'acceleration'                  : RPNOperator( calculateAcceleration,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'black_hole_entropy'            : RPNOperator( calculateBlackHoleEntropy,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_lifetime'           : RPNOperator( calculateBlackHoleLifetime,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_luminosity'         : RPNOperator( calculateBlackHoleLuminosity,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_mass'               : RPNOperator( calculateBlackHoleMass,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_radius'             : RPNOperator( calculateBlackHoleRadius,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_surface_area'       : RPNOperator( calculateBlackHoleSurfaceArea,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_surface_gravity'    : RPNOperator( calculateBlackHoleSurfaceGravity,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_surface_tides'      : RPNOperator( calculateBlackHoleSurfaceTides,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'black_hole_temperature'        : RPNOperator( calculateBlackHoleTemperature,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'distance'                      : RPNOperator( calculateDistance,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'energy_equivalence'            : RPNOperator( calculateEnergyEquivalence,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'escape_velocity'               : RPNOperator( calculateEscapeVelocity,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'heat_index'                    : RPNOperator( calculateHeatIndex,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'horizon_distance'              : RPNOperator( calculateHorizonDistance,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'kinetic_energy'                : RPNOperator( calculateKineticEnergy,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'mass_equivalence'              : RPNOperator( calculateMassEquivalence,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'orbital_mass'                  : RPNOperator( calculateOrbitalMass,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'orbital_period'                : RPNOperator( calculateOrbitalPeriod,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'orbital_radius'                : RPNOperator( calculateOrbitalRadius,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'orbital_velocity'              : RPNOperator( calculateOrbitalVelocity,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'surface_gravity'               : RPNOperator( calculateSurfaceGravity,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'tidal_force'                   : RPNOperator( calculateTidalForce,
                                                   3, [ RPNValidator.Measurement, RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'time_dilation'                 : RPNOperator( calculateTimeDilation,
                                                   1, [ RPNValidator.Measurement ], [ ] ),

    'velocity'                      : RPNOperator( calculateVelocity,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    'wind_chill'                    : RPNOperator( calculateWindChill,
                                                   2, [ RPNValidator.Measurement, RPNValidator.Measurement ], [ ] ),

    # powers_and_roots
    'agm'                           : RPNOperator( getAGM,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'cube'                          : RPNOperator( cube,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'cube_root'                     : RPNOperator( getCubeRoot,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'cube_super_root'               : RPNOperator( getCubeSuperRoot,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'exp'                           : RPNOperator( getExp,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'exp10'                         : RPNOperator( getExp10,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'expphi'                        : RPNOperator( getExpPhi,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'hyperoperator'                 : RPNOperator( calculateNthHyperoperator,
                                                   3, [ RPNValidator.NonnegativeInteger, RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'hyperoperator_right'           : RPNOperator( calculateNthRightHyperoperator,
                                                   3, [ RPNValidator.NonnegativeInteger, RPNValidator.Default, RPNValidator.Default ], [ ] ),

    'power'                         : RPNOperator( getPowerOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'powmod'                        : RPNOperator( getPowModOperator,
                                                   3, [ RPNValidator.Integer, RPNValidator.Integer,
                                                        RPNValidator.Integer ], [ ] ),

    'root'                          : RPNOperator( getRootOperator,
                                                   2, [ RPNValidator.Default, RPNValidator.Real ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'square'                        : RPNOperator( square,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'square_root'                   : RPNOperator( getSquareRoot,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'square_super_root'             : RPNOperator( getSquareSuperRoot,
                                                   1, [ RPNValidator.Default ], [ ] ),

    'super_root'                    : RPNOperator( getSuperRoot,
                                                   2, [ RPNValidator.Default, RPNValidator.NonnegativeInteger ], [ ] ),

    'super_roots'                   : RPNOperator( getSuperRoots,
                                                   2, [ RPNValidator.Default, RPNValidator.NonnegativeInteger ], [ ] ),

    'tetrate'                       : RPNOperator( tetrate,
                                                   2, [ RPNValidator.Default, RPNValidator.Real ], [ ] ),

    'tetrate_right'                 : RPNOperator( tetrateRight,
                                                   2, [ RPNValidator.Default, RPNValidator.Real ], [ ] ),

    # prime_number
    'balanced_prime'                : RPNOperator( getNthBalancedPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'balanced_primes'               : RPNOperator( getNthBalancedPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'cousin_prime'                  : RPNOperator( getNthCousinPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'cousin_primes'                 : RPNOperator( getNthCousinPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'double_balanced_prime'         : RPNOperator( getNthDoubleBalancedPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'double_balanced_primes'        : RPNOperator( getNthDoubleBalancedPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'isolated_prime'                : RPNOperator( getNthIsolatedPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_prime'                    : RPNOperator( getNextPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_primes'                   : RPNOperator( getNextPrimesOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'next_quadruplet_prime'         : RPNOperator( getNextQuadrupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_quadruplet_primes'        : RPNOperator( getNextQuadrupletPrimes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_quintuplet_prime'         : RPNOperator( getNextQuintupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_quintuplet_primes'        : RPNOperator( getNextQuintupletPrimes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_sextuplet_prime'          : RPNOperator( getNextSextupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_sextuplet_primes'         : RPNOperator( getNextSextupletPrimes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_triplet_prime'            : RPNOperator( getNextTripletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_triplet_primes'           : RPNOperator( getNextTripletPrimes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_twin_prime'               : RPNOperator( getNextTwinPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'next_twin_primes'              : RPNOperator( getNextTwinPrimes,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_prime'                     : RPNOperator( findPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_quadruplet_prime'          : RPNOperator( findQuadrupletPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_quintuplet_prime'          : RPNOperator( findQuintupletPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_sextuplet_prime'           : RPNOperator( findSextupletPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_triplet_prime'             : RPNOperator( findTripletPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'nth_twin_prime'                : RPNOperator( findTwinPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octy_prime'                    : RPNOperator( getNthOctyPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'octy_primes'                   : RPNOperator( getNthOctyPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'polyprime'                     : RPNOperator( getNthPolyPrime,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'previous_prime'                : RPNOperator( getPreviousPrimeOperator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'previous_primes'               : RPNOperator( getPreviousPrimesOperator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'prime'                         : RPNOperator( getNthPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'primes'                        : RPNOperator( getPrimesGenerator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'prime_pi'                      : RPNOperator( getPrimePi,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'prime_range'                   : RPNOperator( getPrimeRange,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'quadruplet_prime'              : RPNOperator( getNthQuadrupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'quadruplet_primes'             : RPNOperator( getNthQuadrupletPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'quadruple_balanced_prime'      : RPNOperator( getNthQuadrupleBalancedPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'quadruple_balanced_primes'     : RPNOperator( getNthQuadrupleBalancedPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'quintuplet_prime'              : RPNOperator( getNthQuintupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'quintuplet_primes'             : RPNOperator( getNthQuintupletPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'safe_prime'                    : RPNOperator( getSafePrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sextuplet_prime'               : RPNOperator( getNthSextupletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sextuplet_primes'              : RPNOperator( getNthSextupletPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_prime'                    : RPNOperator( getNthSexyPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_primes'                   : RPNOperator( getNthSexyPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_quadruplet'               : RPNOperator( getNthSexyQuadruplet,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_quadruplets'              : RPNOperator( getNthSexyQuadrupletList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_triplet'                  : RPNOperator( getNthSexyTriplet,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sexy_triplets'                 : RPNOperator( getNthSexyTripletList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'sophie_prime'                  : RPNOperator( getNthSophiePrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'super_prime'                   : RPNOperator( getNthSuperPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'triplet_prime'                 : RPNOperator( getNthTripletPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'triplet_primes'                : RPNOperator( getNthTripletPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'triple_balanced_prime'         : RPNOperator( getNthTripleBalancedPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'triple_balanced_primes'        : RPNOperator( getNthTripleBalancedPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'twin_prime'                    : RPNOperator( getNthTwinPrime,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'twin_primes'                   : RPNOperator( getNthTwinPrimeList,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    # settings
    'accuracy'                      : RPNOperator( lambda n: setAccuracy( fadd( n, 2 ) ),
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'comma'                         : RPNOperator( setComma,
                                                   1, [ RPNValidator.Boolean ], [ ] ),

    'comma_mode'                    : RPNOperator( setCommaMode,
                                                   0, [ ], [ ] ),

    'decimal_grouping'              : RPNOperator( setDecimalGrouping,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'hex_mode'                      : RPNOperator( setHexMode,
                                                   0, [ ], [ ] ),

    'identify'                      : RPNOperator( setIdentify,
                                                   1, [ RPNValidator.Boolean ], [ ] ),

    'identify_mode'                 : RPNOperator( setIdentifyMode,
                                                   0, [ ], [ ] ),

    'input_radix'                   : RPNOperator( setInputRadix,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'integer_grouping'              : RPNOperator( setIntegerGrouping,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'leading_zero'                  : RPNOperator( setLeadingZero,
                                                   1, [ RPNValidator.Boolean ], [ ] ),

    'leading_zero_mode'             : RPNOperator( setLeadingZeroMode,
                                                   0, [ ], [ ] ),

    'octal_mode'                    : RPNOperator( setOctalMode,
                                                   0, [ ], [ ] ),

    'output_radix'                  : RPNOperator( setOutputRadix,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'precision'                     : RPNOperator( setPrecision,
                                                   1, [ RPNValidator.NonnegativeInteger ], [ ] ),

    'timer'                         : RPNOperator( setTimer,
                                                   1, [ RPNValidator.Boolean ], [ ] ),

    'timer_mode'                    : RPNOperator( setTimerMode,
                                                   0, [ ], [ ] ),

    # special
    'base_units'                    : RPNOperator( convertToBaseUnits,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'delete_config'                 : RPNOperator( deleteUserConfiguration,
                                                   1, [ RPNValidator.String ], [ ] ),

    'describe'                      : RPNOperator( describeInteger,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'dimensions'                    : RPNOperator( getDimensions,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'dump_config'                   : RPNOperator( dumpUserConfiguration,
                                                   0, [ ], [ ] ),

    'enumerate_dice'                : RPNOperator( enumerateDiceGenerator,
                                                   1, [ RPNValidator.String ], [ ] ),

    'enumerate_dice_'               : RPNOperator( enumerateMultipleDiceGenerator,
                                                   2, [ RPNValidator.String, RPNValidator.PositiveInteger ], [ ] ),

    'estimate'                      : RPNOperator( estimate,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'help'                          : RPNOperator( printHelpMessage,
                                                   0, [ ], [ ] ),

    'get_config'                    : RPNOperator( getUserConfiguration,
                                                   1, [ RPNValidator.String ], [ ] ),

    'get_variable'                  : RPNOperator( getUserVariable,
                                                   1, [ RPNValidator.String ], [ ] ),

    'if'                            : RPNOperator( lambda a, b, c: a if c else b,
                                                   3, [ RPNValidator.Default, RPNValidator.Default, RPNValidator.Integer ], [ ] ),

    'list_from_file'                : RPNOperator( readListFromFile,
                                                   1, [ RPNValidator.String ], [ ] ),

    'name'                          : RPNOperator( getName,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'oeis'                          : RPNOperator( downloadOEISSequence,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'oeis_comment'                  : RPNOperator( downloadOEISComment,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'oeis_ex'                       : RPNOperator( downloadOEISExtra,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'oeis_name'                     : RPNOperator( downloadOEISName,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'oeis_offset'                   : RPNOperator( downloadOEISOffset,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'ordinal_name'                  : RPNOperator( getOrdinalName,
                                                   1, [ RPNValidator.Integer ], [ ] ),

    'permute_dice'                  : RPNOperator( permuteDiceGenerator,
                                                   1, [ RPNValidator.String ], [ ] ),

    'primitive_units'               : RPNOperator( convertToPrimitiveUnits,
                                                   1, [ RPNValidator.Measurement ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'random'                        : RPNOperator( getRandomNumber,
                                                   0, [ ], [ ] ),

    'random_'                       : RPNOperator( getMultipleRandomsGenerator,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'random_integer'                : RPNOperator( getRandomInteger,
                                                   1, [ RPNValidator.PositiveInteger ], [ ] ),

    'random_integers'               : RPNOperator( getRandomIntegersGenerator,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'result'                        : RPNOperator( loadResult,
                                                   0, [ ], [ ] ),

    'roll_dice'                     : RPNOperator( rollDice,
                                                   1, [ RPNValidator.String ], [ ] ),

    'roll_simple_dice'              : RPNOperator( rollSimpleDice,
                                                   2, [ RPNValidator.PositiveInteger, RPNValidator.PositiveInteger ], [ ] ),

    'roll_dice_'                    : RPNOperator( rollMultipleDiceGenerator,
                                                   2, [ RPNValidator.String, RPNValidator.PositiveInteger ], [ ] ),

    'set_config'                    : RPNOperator( setUserConfiguration,
                                                   2, [ RPNValidator.String, RPNValidator.String ], [ ] ),

    'set_variable'                  : RPNOperator( setUserVariable,
                                                   2, [ RPNValidator.String, RPNValidator.String ], [ ] ),

    #'topics' doesn't need to be handled here, see rpn.py, search for 'topics'

    'uuid'                          : RPNOperator( generateUUID,
                                                   0, [ ], [ ] ),

    'uuid_random'                   : RPNOperator( generateRandomUUID,
                                                   0, [ ], [ ] ),

    'value'                         : RPNOperator( getValue,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    # trigonometry
    'acos'                          : RPNOperator( acosOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'acosh'                         : RPNOperator( acoshOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'acot'                          : RPNOperator( acotOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'acoth'                         : RPNOperator( acothOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'acsc'                          : RPNOperator( acscOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'acsch'                         : RPNOperator( acschOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'asec'                          : RPNOperator( asecOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'asech'                         : RPNOperator( asechOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'asin'                          : RPNOperator( asinOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'asinh'                         : RPNOperator( asinhOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'atan'                          : RPNOperator( atanOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'atanh'                         : RPNOperator( atanhOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'cos'                           : RPNOperator( cosOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'cosh'                          : RPNOperator( coshOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'cot'                           : RPNOperator( cotOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'coth'                          : RPNOperator( cothOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'csc'                           : RPNOperator( cscOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'csch'                          : RPNOperator( cschOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sec'                           : RPNOperator( secOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sech'                          : RPNOperator( sechOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sin'                           : RPNOperator( sinOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'sinh'                          : RPNOperator( sinhOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'tan'                           : RPNOperator( tanOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    'tanh'                          : RPNOperator( tanhOperator,
                                                   1, [ RPNValidator.Default ], [ ],
                                                   RPNOperator.measurementsAllowed ),

    # internal
    '_dump_aliases'                 : RPNOperator( dumpAliases,
                                                   0, [ ], [ ] ),

    '_dump_cache'                   : RPNOperator( dumpFunctionCache,
                                                   1, [ RPNValidator.String ], [ ] ),

    '_dump_constants'               : RPNOperator( dumpConstants,
                                                   0, [ ], [ ] ),

    '_dump_conversions'             : RPNOperator( dumpUnitConversions,
                                                   0, [ ], [ ] ),

    '_dump_operators'               : RPNOperator( dumpOperators,
                                                   0, [ ], [ ] ),

    '_dump_prime_cache'             : RPNOperator( dumpPrimeCache,
                                                   1, [ RPNValidator.String ], [ ] ),

    '_dump_stats'                   : RPNOperator( dumpStats,
                                                   0, [ ], [ ] ),

    '_dump_units'                   : RPNOperator( dumpUnits,
                                                   0, [ ], [ ] ),

    #'antitet'                       : RPNOperator( findTetrahedralNumber, 0 ),
    #'bernfrac'                      : RPNOperator( bernfrac, 1 ),
}

