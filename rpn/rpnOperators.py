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

from mpmath import apery, arange, catalan, cplot, e, euler, exp, fadd, fdiv, fib, fmul, glaisher, inf, khinchin, \
                   lambertw, limit, mertens, mpf, mpmathify, nprod, nsum, phi, pi, plot, power, splot, sqrt

from rpn.rpnAliases import dumpAliasesOperator
from rpn.rpnOperator import callers, RPNOperator
from rpn.rpnOutput import printTitleScreen
from rpn.rpnVersion import PROGRAM_DESCRIPTION, PROGRAM_NAME, PROGRAM_VERSION

from rpn.rpnAstronomy import getAngularSeparationOperator, getAngularSizeOperator, getAntitransitTimeOperator, \
                             getAutumnalEquinoxOperator, getNextAstronomicalDawnOperator, getDayTimeOperator, \
                             getDistanceFromEarthOperator, getEclipseTotalityOperator, getMoonPhaseOperator, \
                             getNextAntitransitOperator, getNextAstronomicalDuskOperator, getNextCivilDawnOperator, \
                             getNextCivilDuskOperator, getNextFirstQuarterMoonOperator, getNextFullMoonOperator, \
                             getNextLastQuarterMoonOperator, getNextMoonAntitransitOperator, getNextMoonRiseOperator, \
                             getNextMoonSetOperator, getNextMoonTransitOperator, getNextNauticalDawnOperator, \
                             getNextNauticalDuskOperator, getNextNewMoonOperator, getNextRisingOperator, \
                             getNextSettingOperator, getNextSunAntitransitOperator, getNextSunriseOperator, \
                             getNextSunsetOperator, getNextTransitOperator, getNightTimeOperator, \
                             getPreviousAntitransitOperator, getPreviousFirstQuarterMoonOperator, \
                             getPreviousFullMoonOperator, getPreviousLastQuarterMoonOperator, \
                             getPreviousNewMoonOperator, getPreviousRisingOperator, getPreviousSettingOperator, \
                             getPreviousTransitOperator, getSkyLocationOperator, getSolarNoonOperator, \
                             getSummerSolsticeOperator, getTransitTimeOperator, getVernalEquinoxOperator, \
                             getWinterSolsticeOperator, RPNAstronomicalObject

from rpn.rpnCalendar import convertBahaiDateOperator, convertEthiopianDateOperator, \
                            convertFrenchRepublicanDateOperator, convertHebrewDateOperator, \
                            convertIndianCivilDateOperator, convertIslamicDateOperator, convertJulianDateOperator, \
                            convertMayanDateOperator, convertPersianDateOperator, generateMonthCalendarOperator, \
                            generateYearCalendarOperator, getBahaiCalendarDateOperator, \
                            getBahaiCalendarDateNameOperator, getEthiopianCalendarDateOperator, \
                            getEthiopianCalendarDateNameOperator, getFrenchRepublicanCalendarDateOperator, \
                            getFrenchRepublicanCalendarDateNameOperator, getHebrewCalendarDateOperator, \
                            getHebrewCalendarDateNameOperator, getIndianCivilCalendarDateOperator, \
                            getIndianCivilCalendarDateNameOperator, getIslamicCalendarDateOperator, \
                            getIslamicCalendarDateNameOperator, getISODateOperator, getISODateNameOperator, \
                            getJulianCalendarDateOperator, getJulianDayOperator, getLilianDayOperator, \
                            getMayanCalendarDateOperator, getOrdinalDateOperator, getPersianCalendarDateOperator, \
                            getPersianCalendarDateNameOperator

from rpn.rpnChemistry import getAtomicNumberOperator, getAtomicSymbolOperator, getAtomicWeightOperator, \
                             getElementBlockOperator, getElementBoilingPointOperator, getElementDensityOperator, \
                             getElementDescriptionOperator, getElementGroupOperator, getElementMeltingPointOperator, \
                             getElementNameOperator, getElementOccurrenceOperator, getElementPeriodOperator, \
                             getElementStateOperator, getMolarMassOperator

from rpn.rpnCombinatorics import countFrobenius, getArrangements, getBellPolynomial, getBinomial, \
                                 getCombinations, getCompositions, getDeBruijnSequence, getIntegerPartitions, \
                                 getLahNumber, getMultinomial, getNarayanaNumberOperator, getNthAperyNumber, \
                                 getNthBell, \
                                 getNthBernoulli, getNthCatalanNumber, getNthDelannoyNumber,getNthMenageNumber, \
                                 getNthMotzkinNumber, getNthMultifactorial, getNthPellNumber, getNthSchroederNumber, \
                                 getNthSchroederHipparchusNumber, getNthSylvesterNumber, getPartitionNumber, \
                                 getPartitionsWithLimit, getPermutations, getStirling1Number, getStirling2Number

from rpn.rpnComputer import andOperator, convertToCharOperator, convertToDoubleOperator, convertToFloatOperator, \
                            convertToLongOperator, convertToLongLongOperator, convertToQuadLongOperator, \
                            convertToShortOperator, convertToSignedIntOperator, convertToUnsignedCharOperator, \
                            convertToUnsignedIntOperator, convertToUnsignedLongOperator, \
                            convertToUnsignedLongLongOperator, convertToUnsignedQuadLongOperator, \
                            convertToUnsignedShortOperator, getBitCountOperator, getBitwiseAnd, getBitwiseNand, \
                            getBitwiseNor, getBitwiseOr, getBitwiseXnor, getBitwiseXor, getInvertedBits, getParity, \
                            interpretAsDoubleOperator, interpretAsFloatOperator, nandOperator, orOperator, \
                            norOperator, notOperator, packIntegerOperator, shiftLeft, shiftRight, \
                            unpackIntegerOperator, xnorOperator, xorOperator

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
                                 getvonKlitzingConstant

from rpn.rpnDateTime import calculateAdventOperator, calculateAscensionThursdayOperator, \
                            calculateAshWednesdayOperator, calculateColumbusDayOperator, \
                            calculateDSTEndOperator, calculateDSTStartOperator, calculateEasterOperator, \
                            calculateElectionDayOperator, calculateFathersDayOperator, calculateGoodFridayOperator, \
                            calculateLaborDayOperator, calculateMartinLutherKingDayOperator, \
                            calculateMemorialDayOperator, calculateMothersDayOperator, \
                            calculateNthWeekdayOfMonthOperator, calculateNthWeekdayOfYearOperator, \
                            calculatePentecostSundayOperator, calculatePresidentsDayOperator, \
                            calculateThanksgivingOperator, convertFromUnixTimeOperator, \
                            convertToDHMSOperator, convertToHMSOperator, convertToYDHMSOperator, \
                            convertToUnixTimeOperator, getChristmasDayOperator, getDayOperator, \
                            getEpiphanyDayOperator, getHourOperator, getIndependenceDayOperator, getISODayOperator, \
                            getMinuteOperator, getMonthOperator, getNewYearsDayOperator, getNowOperator, \
                            getSecondOperator, getTodayOperator, getTomorrowOperator, getVeteransDayOperator, \
                            getWeekdayOperator, getWeekdayNameOperator, getYearOperator, getYesterdayOperator, \
                            makeDateTimeOperator, makeISOTimeOperator, makeJulianTimeOperator, RPNDateTime

from rpn.rpnDice import enumerateDiceGenerator, enumerateMultipleDiceGenerator, permuteDiceGenerator, rollDice, \
                        rollMultipleDiceGenerator, rollSimpleDice

from rpn.rpnDebug import debugPrint

from rpn.rpnFactor import getFactorsOperator

from rpn.rpnGenerator import RPNGenerator

from rpn.rpnGeometry import getAntiprismSurfaceAreaOperator, getAntiprismVolumeOperator, getConeSurfaceAreaOperator, \
                            getConeVolumeOperator, getDodecahedronSurfaceAreaOperator, getDodecahedronVolumeOperator, \
                            getIcosahedronSurfaceAreaOperator, getIcosahedronVolumeOperator, \
                            getKSphereSurfaceAreaOperator, getKSphereRadiusOperator, getKSphereVolumeOperator, \
                            getOctahedronSurfaceAreaOperator, getOctahedronVolumeOperator, \
                            getRegularPolygonAreaOperator, getPrismSurfaceAreaOperator, getPrismVolumeOperator, \
                            getSphereAreaOperator, getSphereRadiusOperator, getSphereVolumeOperator, \
                            getTetrahedronSurfaceAreaOperator, getTetrahedronVolumeOperator, \
                            getTorusSurfaceAreaOperator, getTorusVolumeOperator, getTriangleAreaOperator

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

from rpn.rpnList import alternateSignsOperator, alternateSigns2Operator, appendListsOperator, \
                        calculateAntiharmonicMeanOperator, calculateArithmeticMeanOperator, \
                        calculateGeometricMeanOperator, calculateHarmonicMeanOperator, calculatePowerTowerOperator, \
                        calculatePowerTower2Operator, calculateRootMeanSquare, collate, compareLists, countElements, \
                        doesListRepeat, enumerateList, equalsOneOf, filterMax, filterMin, filterOnFlags, findInList, \
                        flattenOperator, getAlternatingSumOperator, getAlternatingSum2Operator, getAndAll, \
                        getCumulativeListDiffs, getCumulativeListProducts, getCumulativeListSums, \
                        getCumulativeListRatios, getCumulativeOccurrenceRatios, getDifference, getGCDOperator, \
                        getGCDOfList, getListCombinations, getListCombinationsWithRepeats, getLeft, getListDiffs, \
                        getListPowerSet, getListRatios, getRight, getIndexOfMax, getIndexOfMin, getListElement, \
                        getListPermutations, getListPermutationsWithRepeats, getNandAll, getNonzeroes, getNorAll, \
                        getProductOperator, getOccurrences, getOccurrenceRatios, getOrAll, getRandomElement, \
                        getReverse, getSlice, getStandardDeviation, getSublist, getSumOperator, getUniqueElements, \
                        getZeroes, groupElements, interleave, isPalindromeList, listAndOneArgFunctionEvaluator, \
                        makeIntersection, makeUnion, permuteLists, reduceListOperator, shuffleList, sortAscending, \
                        sortDescending

from rpn.rpnLocation import convertLatLongToNACOperator, getGeographicDistanceOperator, getLocationInfoOperator, \
                            getTimeZoneOperator, makeLocationOperator

from rpn.rpnMath import acosOperator, acoshOperator, acotOperator, acothOperator, acscOperator, acschOperator, \
                        addOperator, asecOperator, asechOperator, asinOperator, asinhOperator, atanOperator, \
                        atanhOperator, calculateHypotenuseOperator, calculateNthHyperoperatorOperator, \
                        calculateNthRightHyperoperatorOperator, cosOperator, coshOperator, cotOperator, cothOperator, \
                        cscOperator, cschOperator, cubeOperator, decrementOperator, divideOperator, getAGMOperator, \
                        getAbsoluteValueOperator, getArgumentOperator, getCeilingOperator, getConjugateOperator, \
                        getCubeRootOperator, getCubeSuperRootOperator, getExpOperator, getExp10Operator, \
                        getExpOperator, getExpPhiOperator, getFloorOperator, getImaginaryOperator, getLIOperator, \
                        getLambertWOperator, getLargerOperator, getLog10Operator, getLog2Operator, getLogOperator, \
                        getLogXYOperator, getMantissaOperator, getMaximumOperator, getMinimumOperator, \
                        getModuloOperator, getNearestIntOperator, getNegativeOperator, getPolyexpOperator, \
                        getPolylogOperator, getPowerOperator, getRealOperator, getReciprocalOperator, \
                        getRootOperator, getSignOperator, getSmallerOperator, getSquareRootOperator, \
                        getSquareSuperRootOperator, getSuperRootOperator, getSuperRootsOperator, getValueOperator, \
                        incrementOperator, isDivisibleOperator, isEqualOperator, isEvenOperator, isGreaterOperator, \
                        isIntegerOperator, isKthPowerOperator, isLessOperator, isNotEqualOperator, \
                        isNotGreaterOperator, isNotLessOperator, isNotZeroOperator, isOddOperator, isPowerOperator, \
                        isSquareOperator, isZeroOperator, multiplyOperator, roundByDigitsOperator, \
                        roundByValueOperator, roundOffOperator, secOperator, sechOperator, sinOperator, sinhOperator, \
                        squareOperator, subtractOperator, tanOperator, tanhOperator, tetrateOperator, \
                        tetrateRightOperator

from rpn.rpnMeasurement import applyNumberValueToUnit, convertToBaseUnitsOperator, convertToDMSOperator, \
                               convertToPrimitiveUnitsOperator, convertUnits, estimateOperator, getDimensions, \
                               invertUnitsOperator

from rpn.rpnMeasurementClass import RPNMeasurement

from rpn.rpnModifiers import decrementNestedListLevelOperator, duplicateOperationOperator, duplicateTermOperator, \
                             endOperatorListOperator, getPreviousOperator, incrementNestedListLevelOperator, \
                             startOperatorListOperator, unlistOperator

from rpn.rpnName import getNameOperator, getOrdinalNameOperator

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
                                isDeficient, isFriendly, isHarmonicDivisorNumber, isKHyperperfect, \
                                isKPerfect, isKSemiprimeOperator, isKSphenicOperator, isPerfect, isPernicious, \
                                isPolydivisible, isPowerful, isPronic, isRoughOperator, isRuthAaronNumber, \
                                isSemiprime, isSmoothOperator, isSphenic, isSquareFree, isUnusual, \
                                makeContinuedFraction, makeEulerBrick, makePythagoreanQuadruple, \
                                makePythagoreanTriple, makePythagoreanTriples, solveFrobeniusOperator

from rpn.rpnPersistence import dumpFunctionCacheOperator, dumpPrimeCacheOperator, getUserFunctionsFileName, \
                               loadConstants, loadResult, loadUnitConversionMatrix, loadUnitData

from rpn.rpnPhysics import calculateAcceleration, calculateBlackHoleEntropy, calculateBlackHoleLifetime, \
                           calculateBlackHoleLuminosity, calculateBlackHoleMass, calculateBlackHoleRadius, \
                           calculateBlackHoleSurfaceArea, calculateBlackHoleSurfaceGravity, \
                           calculateBlackHoleSurfaceTides, calculateBlackHoleTemperature, calculateDistance, \
                           calculateEnergyEquivalence, calculateEscapeVelocity, calculateHeatIndex, \
                           calculateHorizonDistance, calculateKineticEnergy, calculateMassEquivalence, \
                           calculateOrbitalMass, calculateOrbitalPeriod, calculateOrbitalRadius, \
                           calculateOrbitalVelocity, calculateSurfaceGravity, calculateTidalForce, \
                           calculateTimeDilation, calculateVelocity, calculateWindChill

from rpn.rpnPolynomials import addPolynomialsOperator, evaluatePolynomialOperator, exponentiatePolynomialOperator, \
                               getPolynomialDiscriminantOperator, multiplyPolynomialsOperator, \
                               multiplyPolynomialListOperator, solveCubicPolynomialOperator, \
                               solveQuadraticPolynomialOperator, solveQuarticPolynomialOperator, \
                               solvePolynomialOperator, sumPolynomialListOperator

from rpn.rpnPolytope import findCenteredDecagonalNumberOperator, findCenteredHeptagonalNumberOperator, \
                            findCenteredHexagonalNumberOperator, findCenteredNonagonalNumberOperator, \
                            findCenteredOctagonalNumberOperator, findCenteredPentagonalNumberOperator, \
                            findCenteredPolygonalNumberOperator, findCenteredSquareNumberOperator, \
                            findCenteredTriangularNumberOperator, findDecagonalNumberOperator, \
                            findHeptagonalNumberOperator, findHexagonalNumberOperator, findNonagonalNumberOperator, \
                            findOctagonalNumberOperator, findPentagonalNumberOperator, \
                            findPolygonalNumberOperator, findSquareNumberOperator, findTriangularNumberOperator, \
                            getNthCenteredCubeNumberOperator, getNthCenteredDecagonalNumberOperator, \
                            getNthCenteredDodecahedralNumberOperator, getNthCenteredHeptagonalNumberOperator, \
                            getNthCenteredHexagonalNumberOperator, getNthCenteredIcosahedralNumberOperator, \
                            getNthCenteredNonagonalNumberOperator, getNthCenteredOctagonalNumberOperator, \
                            getNthCenteredOctahedralNumberOperator, getNthCenteredPentagonalNumberOperator, \
                            getNthCenteredPolygonalNumberOperator, getNthCenteredSquareNumberOperator, \
                            getNthCenteredTetrahedralNumberOperator, getNthCenteredTriangularNumberOperator, \
                            getNthDecagonalCenteredSquareNumberOperator, getNthDecagonalHeptagonalNumberOperator, \
                            getNthDecagonalHexagonalNumberOperator, getNthDecagonalNonagonalNumberOperator, \
                            getNthDecagonalNumberOperator, getNthDecagonalOctagonalNumberOperator, \
                            getNthDecagonalPentagonalNumberOperator, getNthDecagonalTriangularNumberOperator, \
                            getNthDodecahedralNumberOperator, getNthGeneralizedDecagonalNumberOperator, \
                            getNthGeneralizedHeptagonalNumberOperator, getNthGeneralizedHexagonalNumberOperator, \
                            getNthGeneralizedNonagonalNumberOperator, getNthGeneralizedOctagonalNumberOperator, \
                            getNthGeneralizedPentagonalNumberOperator, getNthGeneralizedSquareNumberOperator, \
                            getNthGeneralizedTriangularNumberOperator, getNthHeptagonalHexagonalNumberOperator, \
                            getNthHeptagonalNumberOperator, getNthHeptagonalPentagonalNumberOperator, \
                            getNthHeptagonalSquareNumberOperator, getNthHeptagonalTriangularNumberOperator, \
                            getNthHexagonalNumberOperator, getNthHexagonalPentagonalNumberOperator, \
                            getNthHexagonalSquareNumberOperator, getNthIcosahedralNumberOperator, \
                            getNthNonagonalHeptagonalNumberOperator, getNthNonagonalHexagonalNumberOperator, \
                            getNthNonagonalNumberOperator, getNthNonagonalOctagonalNumberOperator, \
                            getNthNonagonalPentagonalNumberOperator, getNthNonagonalSquareNumberOperator, \
                            getNthNonagonalTriangularNumberOperator, getNthOctagonalHeptagonalNumberOperator, \
                            getNthOctagonalHexagonalNumberOperator, getNthOctagonalNumberOperator, \
                            getNthOctagonalPentagonalNumberOperator, getNthOctagonalSquareNumberOperator, \
                            getNthOctagonalTriangularNumberOperator, getNthTruncatedOctahedralNumberOperator, \
                            getNthOctahedralNumberOperator, getNthPentagonalNumberOperator, \
                            getNthPentagonalSquareNumberOperator, getNthPentagonalTriangularNumberOperator, \
                            getNthPentatopeNumberOperator, getNthPolygonalNumberOperator, \
                            getNthPolygonalPyramidalNumberOperator, getNthPolytopeNumberOperator, \
                            getNthPyramidalNumberOperator, getNthRhombicDodecahedralNumberOperator, \
                            getNthSquareTriangularNumberOperator, getNthStarNumberOperator, \
                            getNthStellaOctangulaNumberOperator, getNthTetrahedralNumberOperator, \
                            getNthTruncatedTetrahedralNumberOperator, getNthTriangularNumberOperator

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
                              getPreviousPrimesOperator, getPrimeRange, getPrimesGenerator, isCompositeOperator, \
                              isPrimeOperator, isStrongPseudoprime

from rpn.rpnSettings import setComma, setCommaMode, setDecimalGrouping, setHexMode, setIdentify, \
                            setIdentifyMode, setInputRadix, setIntegerGrouping, setLeadingZero, \
                            setLeadingZeroMode, setAccuracy, setPrecision, setOctalMode, setOutputRadix, \
                            setTimer, setTimerMode

from rpn.rpnSpecial import describeInteger, downloadOEISComment, downloadOEISExtra, downloadOEISName, \
                           downloadOEISOffset, downloadOEISSequence, findPolynomial, generateRandomUUIDOperator, \
                           generateUUIDOperator, getMultipleRandomsGenerator, getRandomInteger, \
                           getRandomIntegersGenerator, getRandomNumber

from rpn.rpnUnitClasses import RPNUnits

from rpn.rpnUtils import addEchoArgument, abortArgsNeeded, oneArgFunctionEvaluator, \
                         twoArgFunctionEvaluator, validateArguments

from rpn.rpnValidator import argValidator, RPNValidator

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
    'apery_constant'                : RPNOperator( lambda: mpf( apery ), 0 ),
    'catalan_constant'              : RPNOperator( lambda: mpf( catalan ), 0 ),
    'champernowne_constant'         : RPNOperator( getChampernowneConstant, 0 ),
    'copeland_erdos_constant'       : RPNOperator( getCopelandErdosConstant, 0 ),
    'e'                             : RPNOperator( lambda: mpf( e ), 0 ),
    'eddington_number'              : RPNOperator( lambda: fmul( 136, power( 2, 256 ) ), 0 ),
    'euler_mascheroni_constant'     : RPNOperator( lambda: mpf( euler ), 0 ),
    'glaisher_constant'             : RPNOperator( lambda: mpf( glaisher ), 0 ),
    'infinity'                      : RPNOperator( lambda: inf, 0 ),
    'itoi'                          : RPNOperator( lambda: exp( fmul( -0.5, pi ) ), 0 ),
    'khinchin_constant'             : RPNOperator( lambda: mpf( khinchin ), 0 ),
    'merten_constant'               : RPNOperator( lambda: mpf( mertens ), 0 ),
    'mills_constant'                : RPNOperator( getMillsConstant, 0 ),
    'negative_infinity'             : RPNOperator( lambda: -inf, 0 ),
    'omega_constant'                : RPNOperator( lambda: lambertw( 1 ), 0 ),
    'phi'                           : RPNOperator( lambda: mpf( phi ), 0 ),
    'pi'                            : RPNOperator( lambda: mpf( pi ), 0 ),
    'plastic_constant'              : RPNOperator( getPlasticConstant, 0 ),
    'prevost_constant'              : RPNOperator( lambda: nsum( lambda n: fdiv( 1, fib( n ) ), [ 1, inf ] ), 0 ),
    'robbins_constant'              : RPNOperator( getRobbinsConstant, 0 ),
    'silver_ratio'                  : RPNOperator( lambda: fadd( 1, sqrt( 2 ) ), 0 ),
    'tau'                           : RPNOperator( lambda: fmul( mpf( pi ), 2 ), 0 ),
    'thue_morse_constant'           : RPNOperator( getThueMorseConstant, 0 ),

    # derived physical constants
    'faraday_constant'              : RPNOperator( getFaradayConstant, 0 ),
    'fine_structure_constant'       : RPNOperator( getFineStructureConstant, 0 ),
    'radiation_constant'            : RPNOperator( getRadiationConstant, 0 ),
    'stefan_boltzmann_constant'     : RPNOperator( getStefanBoltzmannConstant, 0 ),
    'vacuum_impedance'              : RPNOperator( getVacuumImpedance, 0 ),
    'von_klitzing_constant'         : RPNOperator( getvonKlitzingConstant, 0 ),

    # Planck constants
    'planck_length'                 : RPNOperator( getPlanckLength, 0 ),
    'planck_mass'                   : RPNOperator( getPlanckMass, 0 ),
    'planck_time'                   : RPNOperator( getPlanckTime, 0 ),
    'planck_charge'                 : RPNOperator( getPlanckCharge, 0 ),
    'planck_temperature'            : RPNOperator( getPlanckTemperature, 0 ),

    'planck_acceleration'           : RPNOperator( getPlanckAcceleration, 0 ),
    'planck_angular_frequency'      : RPNOperator( getPlanckAngularFrequency, 0 ),
    'planck_area'                   : RPNOperator( getPlanckArea, 0 ),
    'planck_current'                : RPNOperator( getPlanckCurrent, 0 ),
    'planck_density'                : RPNOperator( getPlanckDensity, 0 ),
    'planck_energy'                 : RPNOperator( getPlanckEnergy, 0 ),
    'planck_electrical_inductance'  : RPNOperator( getPlanckElectricalInductance, 0 ),
    'planck_energy_density'         : RPNOperator( getPlanckEnergyDensity, 0 ),
    'planck_force'                  : RPNOperator( getPlanckForce, 0 ),
    'planck_impedance'              : RPNOperator( getPlanckImpedance, 0 ),
    'planck_intensity'              : RPNOperator( getPlanckIntensity, 0 ),
    'planck_magnetic_inductance'    : RPNOperator( getPlanckMagneticInductance, 0 ),
    'planck_momentum'               : RPNOperator( getPlanckMomentum, 0 ),
    'planck_power'                  : RPNOperator( getPlanckPower, 0 ),
    'planck_pressure'               : RPNOperator( getPlanckPressure, 0 ),
    'planck_viscosity'              : RPNOperator( getPlanckViscosity, 0 ),
    'planck_voltage'                : RPNOperator( getPlanckVoltage, 0 ),
    'planck_volumetric_flow_rate'   : RPNOperator( getPlanckVolumetricFlowRate, 0 ),
    'planck_volume'                 : RPNOperator( getPlanckVolume, 0 ),
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
                debugPrint( 'term (constant):', term )
                debugPrint( 'function:', function )

                if function == '<lambda>':
                    function = inspect.getsource( constants[ term ].function )
                    debugPrint( 'lambda:', function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'

                    start = function.find( className ) + len( className )
                    end = len( function ) - 1

                    bracketLevel = 0
                    commaCount = 0

                    for index in range( end - 1, start, -1 ):
                        if function[ index ] == '[':
                            bracketLevel -= 1
                        elif function[ index ] == ']':
                            bracketLevel += 1
                        elif function[ index ] == ',' and bracketLevel == 0:
                            commaCount += 1

                            if commaCount == 2:
                                end = index
                                break

                    function = function[ start : end ] + ' )( )'
                else:
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
                debugPrint( 'term (operator):', term )
                debugPrint( 'function:', function )

                if function == '<lambda>':
                    function = inspect.getsource( operators[ term ].function )

                    # Inspect returns the actual source line, which is the definition in the
                    # operators dictionary, so we need to parse out the lambda definition.
                    className = 'RPNOperator'

                    start = function.find( className ) + len( className )
                    end = len( function ) - 1

                    bracketLevel = 0
                    commaCount = 0

                    for index in range( end - 1, start, -1 ):
                        if function[ index ] == '[':
                            bracketLevel -= 1
                        elif function[ index ] == ']':
                            bracketLevel += 1
                        elif function[ index ] == ',' and bracketLevel == 0:
                            commaCount += 1

                            if commaCount == 2:
                                end = index
                                break

                    function = function[ start : end ] + ' )'
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
#  createFunctionOperator
#
#  This only gets called if we are not already creating a function.
#
#******************************************************************************

def createFunctionOperator( valueList ):
    g.creatingFunction = True
    valueList.append( RPNFunction( valueList, len( valueList ) ) )


#******************************************************************************
#
#  addXOperator
#
#******************************************************************************

def addXOperator( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'x\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'x' )


#******************************************************************************
#
#  addYOperator
#
#******************************************************************************

def addYOperator( valueList ):
    if not g.creatingFunction:
        raise ValueError( '\'y\' requires \'lambda\' to start a function declaration' )

    valueList[ -1 ].add( 'y' )


#******************************************************************************
#
#  addZOperator
#
#******************************************************************************

def addZOperator( valueList ):
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
#  plotFunctionOperator
#
#******************************************************************************

def plotFunctionOperator( start, end, func ):
    plot( func.evaluate, [ start, end ] )
    return 0


#******************************************************************************
#
#  plot2DFunctionOperator
#
#******************************************************************************

def plot2DFunctionOperator( start1, end1, start2, end2, func ):
    splot( func.evaluate,
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ] )
    return 0


#******************************************************************************
#
#  plotComplexFunctionOperator
#
#******************************************************************************

def plotComplexFunctionOperator( start1, end1, start2, end2, func ):
    cplot( func.evaluate,
           [ float( start1 ), float( end1 ) ], [ float( start2 ), float( end2 ) ],
           points = 10000 )
    return 0


#******************************************************************************
#
#  evaluateRecurrenceOperator
#
#******************************************************************************

def evaluateRecurrenceOperator( start, count, func ):
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
#  repeatOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def repeatOperator( n, func ):
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
#  getSequenceOperator
#
#******************************************************************************

def getSequenceOperator( n, k, func ):
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
#  filterIntegersOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def filterIntegersOperator( n, func ):
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

#def handleMultiArgGeneratorOperator( func, args, currentValueList ):
#    newArgList = [ ]
#
#    for arg in args:
#        if isinstance( arg, list ):
#            newArgList.append( RPNGenerator.create( arg ) )
#        else:
#            newArgList.append( arg )
#
#    # check for arguments to be echoed, and echo them before the result
#    if len( g.echoArguments ) > 0:
#        for echoArg in g.echoArguments:
#            currentValueList.append( echoArg )
#
#    currentValueList.append( func( *newArgList ) )


#******************************************************************************
#
#  evaluateListOperator
#
#******************************************************************************

def evaluateListOperator( term, index, currentValueList ):
    # handle a list operator
    operatorInfo = listOperators[ term ]
    argsNeeded = operatorInfo.argCount

    # first we validate, and make sure the operator has enough arguments
    if len( currentValueList ) < argsNeeded:
        abortArgsNeeded( term, index, argsNeeded )
        return False

    # handle the call depending on the number of arguments needed
    if argsNeeded == 0:
        currentValueList.append( operatorInfo.function( currentValueList ) )
    elif argsNeeded == 1:
        args = currentValueList.pop( )
        handleOneArgListOperator( operatorInfo.function, args, currentValueList )
    else:
        argList = [ ]

        for _ in range( 0, argsNeeded ):
            argList.insert( 0, currentValueList.pop( ) )

        handleMultiArgListOperator( operatorInfo.function, argList, currentValueList )

    return True


#******************************************************************************
#
#  dumpOperatorsOperator
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

def dumpOperatorsOperator( totalsOnly=False ):
    return dumpOperators( totalsOnly )

#******************************************************************************
#
#  dumpConstantsOperator
#
#******************************************************************************

def dumpConstantsOperator( ):
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
#  dumpUnitsOperator
#
#******************************************************************************

def dumpUnitsOperator( ):
    if not g.unitOperators:
        loadUnitData( )
        loadConstants( )

    for i in sorted( g.unitOperators ):
        print( i )

    print( )

    return len( g.unitOperators )


#******************************************************************************
#
#  dumpUnitConversionsOperator
#
#******************************************************************************

def dumpUnitConversionsOperator( ):
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
#  dumpStatsOperator
#
#******************************************************************************

def dumpStatsOperator( printTitle=True ):
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
#  createUserFunctionOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def createUserFunctionOperator( key, func ):
    g.userFunctions[ key ] = func
    g.userFunctionsAreDirty = True

    return key


@oneArgFunctionEvaluator( )
def evaluateFunction0Operator( func ):
    return func.evaluate( )

@twoArgFunctionEvaluator( )
def evaluateFunctionOperator( n, func ):
    return func.evaluate( n )

def evaluateFunction2Operator( n, k, func ):
    return func.evaluate( n, k )

def evaluateFunction3Operator( a, b, c, func ):
    return func.evaluate( a, b, c )


#******************************************************************************
#
#  evaluateListFunction
#
#******************************************************************************

@listAndOneArgFunctionEvaluator( )
def evaluateListFunctionOperator( n, func ):
    return func.evaluate( n )

def evaluateListFunction2Operator( n, k, func ):
    return func.evaluate( n, k )

def evaluateListFunction3Operator( a, b, c, func ):
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
#  evaluateLimitOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateLimitOperator( n, func ):
    return limit( func.evaluate, n )


#******************************************************************************
#
#  evaluateReverseLimitOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateReverseLimitOperator( n, func ):
    return limit( func.evaluate, n, direction = -1 )


#******************************************************************************
#
#  evaluateProductOperator
#
#******************************************************************************

def evaluateProductOperator( start, end, func ):
    return nprod( func.evaluate, [ start, end ] )


#******************************************************************************
#
#  evaluateSumOperator
#
#******************************************************************************

def evaluateSumOperator( start, end, func ):
    return nsum( func.evaluate, [ start, end ] )


#******************************************************************************
#
#  createExponentialRangeOperator
#
#******************************************************************************

def createExponentialRangeOperator( a, b, c ):
    return RPNGenerator.createExponential( a, b, c )


#******************************************************************************
#
#  createGeometricRangeOperator
#
#******************************************************************************

def createGeometricRangeOperator( a, b, c ):
    return RPNGenerator.createGeometric( a, b, c )


#******************************************************************************
#
#  createRangeOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def createRangeOperator( start, end ):
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
    'duplicate_term'                : RPNOperator( duplicateTermOperator, 1 ),
    'duplicate_operator'            : RPNOperator( duplicateOperationOperator, 1 ),
    'previous'                      : RPNOperator( getPreviousOperator, 0 ),
    'unlist'                        : RPNOperator( unlistOperator, 0 ),
    'lambda'                        : RPNOperator( createFunctionOperator, 0 ),
    'x'                             : RPNOperator( addXOperator, 0 ),
    'y'                             : RPNOperator( addYOperator, 0 ),
    'z'                             : RPNOperator( addZOperator, 0 ),
    '['                             : RPNOperator( incrementNestedListLevelOperator, 0 ),
    ']'                             : RPNOperator( decrementNestedListLevelOperator, 0 ),
    '('                             : RPNOperator( startOperatorListOperator, 0 ),
    ')'                             : RPNOperator( endOperatorListOperator, 0 ),
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
    'add_polynomials'               : RPNOperator( addPolynomialsOperator, 2 ),
    'discriminant'                  : RPNOperator( getPolynomialDiscriminantOperator, 1 ),
    'eval_polynomial'               : RPNOperator( evaluatePolynomialOperator, 2 ),
    'multiply_polynomials'          : RPNOperator( multiplyPolynomialsOperator, 2 ),
    'polynomial_power'              : RPNOperator( exponentiatePolynomialOperator, 2 ),
    'polynomial_product'            : RPNOperator( multiplyPolynomialListOperator, 1 ),
    'polynomial_sum'                : RPNOperator( sumPolynomialListOperator, 1 ),
    'solve'                         : RPNOperator( solvePolynomialOperator, 1 ),

    # arithmetic
    'antiharmonic_mean'             : RPNOperator( calculateAntiharmonicMeanOperator, 1 ),
    'equals_one_of'                 : RPNOperator( equalsOneOf, 2 ),
    'gcd'                           : RPNOperator( getGCDOfList, 1 ),
    'geometric_mean'                : RPNOperator( calculateGeometricMeanOperator, 1 ),
    'harmonic_mean'                 : RPNOperator( calculateHarmonicMeanOperator, 1 ),
    'lcm'                           : RPNOperator( getLCMOfList, 1 ),
    'maximum'                       : RPNOperator( getMaximumOperator, 1 ),
    'mean'                          : RPNOperator( calculateArithmeticMeanOperator, 1 ),
    'minimum'                       : RPNOperator( getMinimumOperator, 1 ),
    'product'                       : RPNOperator( getProductOperator, 1 ),
    'root_mean_square'              : RPNOperator( calculateRootMeanSquare, 1 ),
    'stddev'                        : RPNOperator( getStandardDeviation, 1 ),
    'sum'                           : RPNOperator( getSumOperator, 1 ),

    # combinatoric
    'count_frobenius'               : RPNOperator( countFrobenius, 2 ),
    'multinomial'                   : RPNOperator( getMultinomial, 1 ),

    # conversion
    'convert'                       : RPNOperator( convertUnits, 2 ),   # list arguments are special
    'lat_long_to_nac'               : RPNOperator( convertLatLongToNACOperator, 1 ),
    'pack'                          : RPNOperator( packIntegerOperator, 2 ),
    'unpack'                        : RPNOperator( unpackIntegerOperator, 2 ),

    # date_time
    'make_datetime'                 : RPNOperator( makeDateTimeOperator, 1 ),
    'make_iso_time'                 : RPNOperator( makeISOTimeOperator, 1 ),
    'make_julian_time'              : RPNOperator( makeJulianTimeOperator, 1 ),

    # function
    'filter'                        : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k ) ), 2 ),
    'filter_lists'                  : RPNOperator( lambda n, k: RPNGenerator( filterListOfLists( n, k ) ), 2 ),
    'filter_by_index'               : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k ) ), 2 ),
    'for_each'                      : RPNOperator( lambda n, k: RPNGenerator( forEach( n, k ) ), 2 ),
    'for_each_list'                 : RPNOperator( lambda n, k: RPNGenerator( forEachList( n, k ) ), 2 ),
    'unfilter'                      : RPNOperator( lambda n, k: RPNGenerator( filterList( n, k, True ) ), 2 ),
    'unfilter_by_index'             : RPNOperator( lambda n, k: RPNGenerator( filterListByIndex( n, k, True ) ), 2 ),

    # lexicographic
    'combine_digits'                : RPNOperator( combineDigits, 1 ),

    # list
    'alternate_signs'               : RPNOperator( lambda n: RPNGenerator( alternateSignsOperator( n ) ), 1 ),
    'alternate_signs_2'             : RPNOperator( lambda n: RPNGenerator( alternateSigns2Operator( n ) ), 1 ),
    'alternating_sum'               : RPNOperator( lambda n: getAlternatingSumOperator( n ), 1 ),
    'alternating_sum_2'             : RPNOperator( lambda n: getAlternatingSum2Operator( n ), 1 ),
    'and_all'                       : RPNOperator( getAndAll, 1 ),
    'append'                        : RPNOperator( appendListsOperator, 2 ),
    'collate'                       : RPNOperator( lambda n: RPNGenerator( collate( n ) ), 1 ),
    'compare_lists'                 : RPNOperator( compareLists, 2 ),
    'count'                         : RPNOperator( countElements, 1 ),
    'cumulative_diffs'              : RPNOperator( lambda n: RPNGenerator( getCumulativeListDiffs( n ) ), 1 ),
    'cumulative_products'           : RPNOperator( lambda n: RPNGenerator( getCumulativeListProducts( n ) ), 1 ),
    'cumulative_ratios'             : RPNOperator( lambda n: RPNGenerator( getCumulativeListRatios( n ) ), 1 ),
    'cumulative_sums'               : RPNOperator( lambda n: RPNGenerator( getCumulativeListSums( n ) ),1 ),
    'difference'                    : RPNOperator( getDifference, 2 ),
    'diffs'                         : RPNOperator( lambda n: RPNGenerator( getListDiffs( n ) ), 1 ),
    'does_list_repeat'              : RPNOperator( doesListRepeat, 1 ),
    'element'                       : RPNOperator( getListElement, 2 ),
    'enumerate'                     : RPNOperator( lambda n, k: RPNGenerator( enumerateList( n, k ) ), 2 ),
    'filter_max'                    : RPNOperator( lambda n, k: RPNGenerator( filterMax( n, k ) ), 2 ),
    'filter_min'                    : RPNOperator( lambda n, k: RPNGenerator( filterMin( n, k ) ), 2 ),
    'filter_on_flags'               : RPNOperator( lambda n, k: RPNGenerator( filterOnFlags( n, k ) ), 2 ),
    'find'                          : RPNOperator( findInList, 2 ),
    'flatten'                       : RPNOperator( flattenOperator, 1 ),
    'get_combinations'              : RPNOperator( getListCombinations, 2 ),
    'get_repeat_combinations'       : RPNOperator( getListCombinationsWithRepeats, 2 ),
    'get_permutations'              : RPNOperator( getListPermutations, 2 ),
    'get_repeat_permutations'       : RPNOperator( getListPermutationsWithRepeats, 2 ),
    'group_elements'                : RPNOperator( groupElements, 2 ),
    'interleave'                    : RPNOperator( interleave, 2 ),
    'intersection'                  : RPNOperator( makeIntersection, 2 ),
    'is_palindrome_list'            : RPNOperator( isPalindromeList, 1 ),
    'left'                          : RPNOperator( getLeft, 2 ),
    'max_index'                     : RPNOperator( getIndexOfMax, 1 ),
    'min_index'                     : RPNOperator( getIndexOfMin, 1 ),
    'nand_all'                      : RPNOperator( getNandAll, 1 ),
    'nonzero'                       : RPNOperator( getNonzeroes, 1 ),
    'nor_all'                       : RPNOperator( getNorAll, 1 ),
    'occurrences'                   : RPNOperator( getOccurrences, 1 ),
    'occurrence_cumulative'         : RPNOperator( getCumulativeOccurrenceRatios, 1 ),
    'occurrence_ratios'             : RPNOperator( getOccurrenceRatios, 1 ),
    'or_all'                        : RPNOperator( getOrAll, 1 ),
    'permute_lists'                 : RPNOperator( permuteLists, 1 ),
    'powerset'                      : RPNOperator( lambda n: RPNGenerator( getListPowerSet( n ) ), 1 ),
    'random_element'                : RPNOperator( getRandomElement, 1 ),
    'ratios'                        : RPNOperator( lambda n: RPNGenerator( getListRatios( n ) ), 1 ),
    'reduce'                        : RPNOperator( reduceListOperator, 1 ),
    'reverse'                       : RPNOperator( getReverse, 1 ),
    'right'                         : RPNOperator( getRight, 2 ),
    'shuffle'                       : RPNOperator( shuffleList, 1 ),
    'slice'                         : RPNOperator( lambda a, b, c: RPNGenerator( getSlice( a, b, c ) ), 3 ),
    'sort'                          : RPNOperator( sortAscending, 1 ),
    'sort_descending'               : RPNOperator( sortDescending, 1 ),
    'sublist'                       : RPNOperator( lambda a, b, c: RPNGenerator( getSublist( a, b, c ) ), 3 ),
    'union'                         : RPNOperator( makeUnion, 2 ),
    'unique'                        : RPNOperator( getUniqueElements, 1 ),
    'zero'                          : RPNOperator( getZeroes, 1 ),

    # number_theory
    'base'                              : RPNOperator( interpretAsBaseOperator, 2 ),
    'continued_fraction'                : RPNOperator( convertFromContinuedFraction, 1 ),
    'crt'                               : RPNOperator( calculateChineseRemainderTheorem, 2 ),
    'frobenius'                         : RPNOperator( getFrobeniusNumber, 1 ),
    'geometric_recurrence'              : RPNOperator( lambda a, b, c, d: RPNGenerator( getGeometricRecurrence( a, b, c, d ) ), 4 ),
    'is_friendly'                       : RPNOperator( isFriendly, 1 ),
    'linear_recurrence'                 : RPNOperator( lambda a, b, c: RPNGenerator( getLinearRecurrence( a, b, c ) ), 3 ),
    'linear_recurrence_with_modulo'     : RPNOperator( lambda a, b, c, d: RPNGenerator( getLinearRecurrenceWithModulo( a, b, c, d ) ), 4 ),
    'nth_linear_recurrence'             : RPNOperator( getNthLinearRecurrence, 3 ),
    'nth_linear_recurrence_with_modulo' : RPNOperator( getNthLinearRecurrenceWithModulo, 4 ),
    'solve_frobenius'                   : RPNOperator( solveFrobeniusOperator, 2 ),

    # powers_and_roots
    'power_tower'                       : RPNOperator( calculatePowerTowerOperator, 1 ),
    'power_tower2'                      : RPNOperator( calculatePowerTower2Operator, 1 ),

    # special
    'echo'                              : RPNOperator( addEchoArgument, 1 ),
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
    'find_polynomial'               : RPNOperator( findPolynomial, 2 ),
    'solve_cubic'                   : RPNOperator( solveCubicPolynomialOperator, 4 ),
    'solve_quadratic'               : RPNOperator( solveQuadraticPolynomialOperator, 3 ),
    'solve_quartic'                 : RPNOperator( solveQuarticPolynomialOperator, 5 ),

    # arithmetic
    'abs'                           : RPNOperator( getAbsoluteValueOperator, 1 ),
    'add'                           : RPNOperator( addOperator, 2 ),
    'ceiling'                       : RPNOperator( getCeilingOperator, 1 ),
    'decrement'                     : RPNOperator( decrementOperator, 1 ),
    'divide'                        : RPNOperator( divideOperator, 2 ),
    'floor'                         : RPNOperator( getFloorOperator, 1 ),
    'gcd2'                          : RPNOperator( getGCDOperator, 2 ),
    'increment'                     : RPNOperator( incrementOperator, 1 ),
    'is_divisible'                  : RPNOperator( isDivisibleOperator, 2 ),
    'is_equal'                      : RPNOperator( isEqualOperator, 2 ),
    'is_even'                       : RPNOperator( isEvenOperator, 1 ),
    'is_greater'                    : RPNOperator( isGreaterOperator, 2 ),
    'is_integer'                    : RPNOperator( isIntegerOperator, 1 ),
    'is_kth_power'                  : RPNOperator( isKthPowerOperator, 2 ),
    'is_less'                       : RPNOperator( isLessOperator, 2 ),
    'is_not_equal'                  : RPNOperator( isNotEqualOperator, 2 ),
    'is_not_greater'                : RPNOperator( isNotGreaterOperator, 2 ),
    'is_not_less'                   : RPNOperator( isNotLessOperator, 2 ),
    'is_not_zero'                   : RPNOperator( isNotZeroOperator, 1 ),
    'is_odd'                        : RPNOperator( isOddOperator, 1 ),
    'is_power_of_k'                 : RPNOperator( isPowerOperator, 2 ),
    'is_square'                     : RPNOperator( isSquareOperator, 1 ),
    'is_zero'                       : RPNOperator( isZeroOperator, 1 ),
    'larger'                        : RPNOperator( getLargerOperator, 2 ),
    'lcm2'                          : RPNOperator( getLCM, 2 ),
    'mantissa'                      : RPNOperator( getMantissaOperator, 1 ),
    'modulo'                        : RPNOperator( getModuloOperator, 2 ),
    'multiply'                      : RPNOperator( multiplyOperator, 2 ),
    'nearest_int'                   : RPNOperator( getNearestIntOperator, 1 ),
    'negative'                      : RPNOperator( getNegativeOperator, 1 ),
    'reciprocal'                    : RPNOperator( getReciprocalOperator, 1 ),
    'round'                         : RPNOperator( roundOffOperator, 1 ),
    'round_by_digits'               : RPNOperator( roundByDigitsOperator, 2 ),
    'round_by_value'                : RPNOperator( roundByValueOperator, 2 ),
    'sign'                          : RPNOperator( getSignOperator, 1 ),
    'smaller'                       : RPNOperator( getSmallerOperator, 2 ),
    'subtract'                      : RPNOperator( subtractOperator, 2 ),

    # astronom
    'angular_separation'            : RPNOperator( getAngularSeparationOperator, 4 ),
    'angular_size'                  : RPNOperator( getAngularSizeOperator, 3 ),
    'antitransit_time'              : RPNOperator( getAntitransitTimeOperator, 3 ),
    'astronomical_dawn'             : RPNOperator( getNextAstronomicalDawnOperator, 2 ),
    'astronomical_dusk'             : RPNOperator( getNextAstronomicalDuskOperator, 2 ),
    'autumnal_equinox'              : RPNOperator( getAutumnalEquinoxOperator, 1 ),
    'dawn'                          : RPNOperator( getNextCivilDawnOperator, 2 ),
    'day_time'                      : RPNOperator( getDayTimeOperator, 2 ),
    'distance_from_earth'           : RPNOperator( getDistanceFromEarthOperator, 2 ),
    'dusk'                          : RPNOperator( getNextCivilDuskOperator, 2 ),
    'eclipse_totality'              : RPNOperator( getEclipseTotalityOperator, 4 ),
    'moonrise'                      : RPNOperator( getNextMoonRiseOperator, 2 ),
    'moonset'                       : RPNOperator( getNextMoonSetOperator, 2 ),
    'moon_antitransit'              : RPNOperator( getNextMoonAntitransitOperator, 2 ),
    'moon_phase'                    : RPNOperator( getMoonPhaseOperator, 1 ),
    'moon_transit'                  : RPNOperator( getNextMoonTransitOperator, 2 ),
    'nautical_dawn'                 : RPNOperator( getNextNauticalDawnOperator, 2 ),
    'nautical_dusk'                 : RPNOperator( getNextNauticalDuskOperator, 2 ),
    'next_antitransit'              : RPNOperator( getNextAntitransitOperator, 3 ),
    'next_first_quarter_moon'       : RPNOperator( getNextFirstQuarterMoonOperator, 1 ),
    'next_full_moon'                : RPNOperator( getNextFullMoonOperator, 1 ),
    'next_last_quarter_moon'        : RPNOperator( getNextLastQuarterMoonOperator, 1 ),
    'next_new_moon'                 : RPNOperator( getNextNewMoonOperator, 1 ),
    'next_rising'                   : RPNOperator( getNextRisingOperator, 3 ),
    'next_setting'                  : RPNOperator( getNextSettingOperator, 3 ),
    'next_transit'                  : RPNOperator( getNextTransitOperator, 3 ),
    'night_time'                    : RPNOperator( getNightTimeOperator, 2 ),
    'previous_antitransit'          : RPNOperator( getPreviousAntitransitOperator, 3 ),
    'previous_first_quarter_moon'   : RPNOperator( getPreviousFirstQuarterMoonOperator, 1 ),
    'previous_full_moon'            : RPNOperator( getPreviousFullMoonOperator, 1 ),
    'previous_last_quarter_moon'    : RPNOperator( getPreviousLastQuarterMoonOperator, 1 ),
    'previous_new_moon'             : RPNOperator( getPreviousNewMoonOperator, 1 ),
    'previous_rising'               : RPNOperator( getPreviousRisingOperator, 3 ),
    'previous_setting'              : RPNOperator( getPreviousSettingOperator, 3 ),
    'previous_transit'              : RPNOperator( getPreviousTransitOperator, 3 ),
    'sky_location'                  : RPNOperator( getSkyLocationOperator, 3 ),
    'solar_noon'                    : RPNOperator( getSolarNoonOperator, 2 ),
    'summer_solstice'               : RPNOperator( getSummerSolsticeOperator, 1 ),
    'sunrise'                       : RPNOperator( getNextSunriseOperator, 2 ),
    'sunset'                        : RPNOperator( getNextSunsetOperator, 2 ),
    'sun_antitransit'               : RPNOperator( getNextSunAntitransitOperator, 2 ),
    'transit_time'                  : RPNOperator( getTransitTimeOperator, 3 ),
    'vernal_equinox'                : RPNOperator( getVernalEquinoxOperator, 1 ),
    'winter_solstice'               : RPNOperator( getWinterSolsticeOperator, 1 ),

    # astronomy - heavenly body operators
    'sun'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Sun( ) ), 0 ),
    'mercury'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mercury( ) ), 0 ),
    'venus'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Venus( ) ), 0 ),
    'moon'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Moon( ) ), 0 ),
    'mars'                          : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mars( ) ), 0 ),
    'jupiter'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Jupiter( ) ), 0 ),
    'saturn'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Saturn( ) ), 0 ),
    'uranus'                        : RPNOperator( lambda: RPNAstronomicalObject( ephem.Uranus( ) ), 0 ),
    'neptune'                       : RPNOperator( lambda: RPNAstronomicalObject( ephem.Neptune( ) ), 0 ),
    'pluto'                         : RPNOperator( lambda: RPNAstronomicalObject( ephem.Pluto( ) ), 0 ),

    # bitwise
    'bitwise_and'                   : RPNOperator( getBitwiseAnd, 2 ),
    'bitwise_nand'                  : RPNOperator( getBitwiseNand, 2 ),
    'bitwise_nor'                   : RPNOperator( getBitwiseNor, 2 ),
    'bitwise_not'                   : RPNOperator( getInvertedBits, 1 ),
    'bitwise_or'                    : RPNOperator( getBitwiseOr, 2 ),
    'bitwise_xnor'                  : RPNOperator( getBitwiseXnor, 2 ),
    'bitwise_xor'                   : RPNOperator( getBitwiseXor, 2 ),
    'count_bits'                    : RPNOperator( getBitCountOperator, 1 ),
    'parity'                        : RPNOperator( getParity, 1 ),
    'shift_left'                    : RPNOperator( shiftLeft, 2 ),
    'shift_right'                   : RPNOperator( shiftRight, 2 ),

    # calendar
    'advent'                        : RPNOperator( calculateAdventOperator, 1 ),
    'ascension'                     : RPNOperator( calculateAscensionThursdayOperator, 1 ),
    'ash_wednesday'                 : RPNOperator( calculateAshWednesdayOperator, 1 ),
    'calendar'                      : RPNOperator( generateMonthCalendarOperator, 1 ),
    'christmas'                     : RPNOperator( getChristmasDayOperator, 1 ),
    'columbus_day'                  : RPNOperator( calculateColumbusDayOperator, 1 ),
    'dst_end'                       : RPNOperator( calculateDSTEndOperator, 1 ),
    'dst_start'                     : RPNOperator( calculateDSTStartOperator, 1 ),
    'easter'                        : RPNOperator( calculateEasterOperator, 1 ),
    'election_day'                  : RPNOperator( calculateElectionDayOperator, 1 ),
    'epiphany'                      : RPNOperator( getEpiphanyDayOperator, 1 ),
    'fathers_day'                   : RPNOperator( calculateFathersDayOperator, 1 ),
    'from_bahai'                    : RPNOperator( convertBahaiDateOperator, 3 ),
    'from_ethiopian'                : RPNOperator( convertEthiopianDateOperator, 3 ),
    'from_french_republican'        : RPNOperator( convertFrenchRepublicanDateOperator, 3 ),
    'from_hebrew'                   : RPNOperator( convertHebrewDateOperator, 3 ),
    'from_indian_civil'             : RPNOperator( convertIndianCivilDateOperator, 3 ),
    'from_islamic'                  : RPNOperator( convertIslamicDateOperator,3 ),
    'from_julian'                   : RPNOperator( convertJulianDateOperator, 3 ),
    'from_mayan'                    : RPNOperator( convertMayanDateOperator, 5 ),
    'from_persian'                  : RPNOperator( convertPersianDateOperator, 3 ),
    'good_friday'                   : RPNOperator( calculateGoodFridayOperator, 1 ),
    'independence_day'              : RPNOperator( getIndependenceDayOperator, 1 ),
    'iso_date'                      : RPNOperator( getISODateOperator, 1 ),
    'labor_day'                     : RPNOperator( calculateLaborDayOperator, 1 ),
    'martin_luther_king_day'        : RPNOperator( calculateMartinLutherKingDayOperator, 1 ),
    'memorial_day'                  : RPNOperator( calculateMemorialDayOperator, 1 ),
    'mothers_day'                   : RPNOperator( calculateMothersDayOperator, 1 ),
    'new_years_day'                 : RPNOperator( getNewYearsDayOperator, 1 ),
    'nth_weekday'                   : RPNOperator( calculateNthWeekdayOfMonthOperator, 4 ),
    'nth_weekday_of_year'           : RPNOperator( calculateNthWeekdayOfYearOperator, 3 ),
    'pentecost'                     : RPNOperator( calculatePentecostSundayOperator, 1 ),
    'presidents_day'                : RPNOperator( calculatePresidentsDayOperator, 1 ),
    'thanksgiving'                  : RPNOperator( calculateThanksgivingOperator, 1 ),
    'to_bahai'                      : RPNOperator( getBahaiCalendarDateOperator, 1 ),
    'to_bahai_name'                 : RPNOperator( getBahaiCalendarDateNameOperator, 1 ),
    'to_ethiopian'                  : RPNOperator( getEthiopianCalendarDateOperator, 1 ),
    'to_ethiopian_name'             : RPNOperator( getEthiopianCalendarDateNameOperator, 1 ),
    'to_french_republican'          : RPNOperator( getFrenchRepublicanCalendarDateOperator, 1 ),
    'to_french_republican_name'     : RPNOperator( getFrenchRepublicanCalendarDateNameOperator, 1 ),
    'to_hebrew'                     : RPNOperator( getHebrewCalendarDateOperator, 1 ),
    'to_hebrew_name'                : RPNOperator( getHebrewCalendarDateNameOperator, 1 ),
    'to_indian_civil'               : RPNOperator( getIndianCivilCalendarDateOperator, 1 ),
    'to_indian_civil_name'          : RPNOperator( getIndianCivilCalendarDateNameOperator, 1 ),
    'to_islamic'                    : RPNOperator( getIslamicCalendarDateOperator, 1 ),
    'to_islamic_name'               : RPNOperator( getIslamicCalendarDateNameOperator, 1 ),
    'to_iso'                        : RPNOperator( getISODateOperator, 1 ),
    'to_iso_name'                   : RPNOperator( getISODateNameOperator, 1 ),
    'to_julian'                     : RPNOperator( getJulianCalendarDateOperator, 1 ),
    'to_julian_day'                 : RPNOperator( getJulianDayOperator, 1 ),
    'to_lilian_day'                 : RPNOperator( getLilianDayOperator, 1 ),
    'to_mayan'                      : RPNOperator( getMayanCalendarDateOperator, 1 ),
    'to_ordinal_date'               : RPNOperator( getOrdinalDateOperator, 1 ),
    'to_persian'                    : RPNOperator( getPersianCalendarDateOperator, 1 ),
    'to_persian_name'               : RPNOperator( getPersianCalendarDateNameOperator, 1 ),
    'veterans_day'                  : RPNOperator( getVeteransDayOperator, 1 ),
    'weekday'                       : RPNOperator( getWeekdayOperator, 1 ),
    'weekday_name'                  : RPNOperator( getWeekdayNameOperator, 1 ),
    'year_calendar'                 : RPNOperator( generateYearCalendarOperator, 1 ),

    # chemistry
    'atomic_number'                 : RPNOperator( getAtomicNumberOperator, 1 ),
    'atomic_symbol'                 : RPNOperator( getAtomicSymbolOperator, 1 ),
    'atomic_weight'                 : RPNOperator( getAtomicWeightOperator, 1 ),
    'element_block'                 : RPNOperator( getElementBlockOperator, 1 ),
    'element_boiling_point'         : RPNOperator( getElementBoilingPointOperator, 1 ),
    'element_density'               : RPNOperator( getElementDensityOperator, 1 ),
    'element_description'           : RPNOperator( getElementDescriptionOperator, 1 ),
    'element_group'                 : RPNOperator( getElementGroupOperator, 1 ),
    'element_melting_point'         : RPNOperator( getElementMeltingPointOperator, 1 ),
    'element_name'                  : RPNOperator( getElementNameOperator, 1 ),
    'element_occurrence'            : RPNOperator( getElementOccurrenceOperator, 1 ),
    'element_period'                : RPNOperator( getElementPeriodOperator, 1 ),

    'element_state'                 : RPNOperator( getElementStateOperator, 1 ),
    'molar_mass'                    : RPNOperator( getMolarMassOperator, 1 ),

    # combinatoric
    'arrangements'                  : RPNOperator( getArrangements, 1 ),
    'bell_polynomial'               : RPNOperator( getBellPolynomial, 2 ),
    'binomial'                      : RPNOperator( getBinomial, 2 ),
    'combinations'                  : RPNOperator( getCombinations, 2 ),
    'compositions'                  : RPNOperator( getCompositions, 2 ),
    'debruijn_sequence'             : RPNOperator( getDeBruijnSequence, 2 ),
    'get_partitions'                : RPNOperator( getIntegerPartitions, 1 ),
    'get_partitions_with_limit'     : RPNOperator( getPartitionsWithLimit, 2 ),
    'lah_number'                    : RPNOperator( getLahNumber, 2 ),
    'nth_menage'                    : RPNOperator( getNthMenageNumber, 1 ),
    'multifactorial'                : RPNOperator( getNthMultifactorial, 2 ),
    'narayana_number'               : RPNOperator( getNarayanaNumberOperator, 2 ),
    'nth_apery'                     : RPNOperator( getNthAperyNumber, 1 ),
    'nth_bell'                      : RPNOperator( getNthBell, 1 ),
    'nth_bernoulli'                 : RPNOperator( getNthBernoulli, 1 ),
    'nth_catalan'                   : RPNOperator( getNthCatalanNumber, 1 ),
    'nth_delannoy'                  : RPNOperator( getNthDelannoyNumber, 1 ),
    'nth_motzkin'                   : RPNOperator( getNthMotzkinNumber, 1 ),
    'nth_pell'                      : RPNOperator( getNthPellNumber, 1 ),
    'nth_schroeder'                 : RPNOperator( getNthSchroederNumber, 1 ),
    'nth_schroeder_hipparchus'      : RPNOperator( getNthSchroederHipparchusNumber, 1 ),
    'nth_sylvester'                 : RPNOperator( getNthSylvesterNumber, 1 ),
    'partitions'                    : RPNOperator( getPartitionNumber, 1 ),
    'permutations'                  : RPNOperator( getPermutations, 2 ),
    'stirling1_number'              : RPNOperator( getStirling1Number, 2 ),
    'stirling2_number'              : RPNOperator( getStirling2Number, 2 ),

    # complex
    'argument'                      : RPNOperator( getArgumentOperator, 1 ),
    'conjugate'                     : RPNOperator( getConjugateOperator, 1 ),
    'imaginary'                     : RPNOperator( getImaginaryOperator, 1 ),
    'real'                          : RPNOperator( getRealOperator, 1 ),

    # conversion
    'char'                          : RPNOperator( convertToCharOperator, 1 ),
    'dhms'                          : RPNOperator( convertToDHMSOperator, 1 ),
    'dms'                           : RPNOperator( convertToDMSOperator, 1 ),
    'double'                        : RPNOperator( convertToDoubleOperator, 1 ),
    'float'                         : RPNOperator( convertToFloatOperator, 1 ),
    'from_unix_time'                : RPNOperator( convertFromUnixTimeOperator, 1 ),
    'hms'                           : RPNOperator( convertToHMSOperator, 1 ),
    'integer'                       : RPNOperator( convertToSignedIntOperator, 2 ),
    'invert_units'                  : RPNOperator( invertUnitsOperator, 1 ),
    'long'                          : RPNOperator( convertToLongOperator, 1 ),
    'longlong'                      : RPNOperator( convertToLongLongOperator, 1 ),
    'quadlong'                      : RPNOperator( convertToQuadLongOperator, 1 ),
    'short'                         : RPNOperator( convertToShortOperator, 1 ),
    'to_unix_time'                  : RPNOperator( convertToUnixTimeOperator, 1 ),
    'uchar'                         : RPNOperator( convertToUnsignedCharOperator, 1 ),
    'uinteger'                      : RPNOperator( convertToUnsignedIntOperator, 2 ),
    'ulong'                         : RPNOperator( convertToUnsignedLongOperator, 1 ),
    'ulonglong'                     : RPNOperator( convertToUnsignedLongLongOperator, 1 ),
    'undouble'                      : RPNOperator( interpretAsDoubleOperator, 1 ),
    'unfloat'                       : RPNOperator( interpretAsFloatOperator, 1 ),
    'uquadlong'                     : RPNOperator( convertToUnsignedQuadLongOperator, 1 ),
    'ushort'                        : RPNOperator( convertToUnsignedShortOperator, 1 ),
    'ydhms'                         : RPNOperator( convertToYDHMSOperator, 1 ),

    # date_time
    'get_year'                      : RPNOperator( getYearOperator, 1 ),
    'get_month'                     : RPNOperator( getMonthOperator, 1 ),
    'get_day'                       : RPNOperator( getDayOperator, 1 ),
    'get_hour'                      : RPNOperator( getHourOperator, 1 ),
    'get_minute'                    : RPNOperator( getMinuteOperator, 1 ),
    'get_second'                    : RPNOperator( getSecondOperator, 1 ),
    'iso_day'                       : RPNOperator( getISODayOperator, 1 ),
    'now'                           : RPNOperator( getNowOperator, 0 ),
    'today'                         : RPNOperator( getTodayOperator, 0 ),
    'tomorrow'                      : RPNOperator( getTomorrowOperator, 0 ),
    'yesterday'                     : RPNOperator( getYesterdayOperator, 0 ),

    # figurate
    'centered_cube'                 : RPNOperator( getNthCenteredCubeNumberOperator, 1 ),
    'centered_decagonal'            : RPNOperator( getNthCenteredDecagonalNumberOperator, 1 ),
    'centered_dodecahedral'         : RPNOperator( getNthCenteredDodecahedralNumberOperator, 1 ),
    'centered_heptagonal'           : RPNOperator( getNthCenteredHeptagonalNumberOperator, 1 ),
    'centered_hexagonal'            : RPNOperator( getNthCenteredHexagonalNumberOperator, 1 ),
    'centered_icosahedral'          : RPNOperator( getNthCenteredIcosahedralNumberOperator, 1 ),
    'centered_nonagonal'            : RPNOperator( getNthCenteredNonagonalNumberOperator, 1 ),
    'centered_octagonal'            : RPNOperator( getNthCenteredOctagonalNumberOperator, 1 ),
    'centered_octahedral'           : RPNOperator( getNthCenteredOctahedralNumberOperator, 1 ),
    'centered_pentagonal'           : RPNOperator( getNthCenteredPentagonalNumberOperator, 1 ),
    'centered_polygonal'            : RPNOperator( getNthCenteredPolygonalNumberOperator, 2 ),
    'centered_square'               : RPNOperator( getNthCenteredSquareNumberOperator, 1 ),
    'centered_tetrahedral'          : RPNOperator( getNthCenteredTetrahedralNumberOperator, 1 ),
    'centered_triangular'           : RPNOperator( getNthCenteredTriangularNumberOperator, 1 ),
    'decagonal'                     : RPNOperator( getNthDecagonalNumberOperator, 1 ),
    'decagonal_centered_square'     : RPNOperator( getNthDecagonalCenteredSquareNumberOperator, 1 ),
    'decagonal_heptagonal'          : RPNOperator( getNthDecagonalHeptagonalNumberOperator, 1 ),
    'decagonal_hexagonal'           : RPNOperator( getNthDecagonalHexagonalNumberOperator, 1 ),
    'decagonal_nonagonal'           : RPNOperator( getNthDecagonalNonagonalNumberOperator, 1 ),
    'decagonal_octagonal'           : RPNOperator( getNthDecagonalOctagonalNumberOperator, 1 ),
    'decagonal_pentagonal'          : RPNOperator( getNthDecagonalPentagonalNumberOperator, 1 ),
    'decagonal_triangular'          : RPNOperator( getNthDecagonalTriangularNumberOperator, 1 ),
    'dodecahedral'                  : RPNOperator( getNthDodecahedralNumberOperator, 1 ),
    'generalized_decagonal'         : RPNOperator( getNthGeneralizedDecagonalNumberOperator, 1 ),
    'generalized_heptagonal'        : RPNOperator( getNthGeneralizedHeptagonalNumberOperator, 1 ),
    'generalized_nonagonal'         : RPNOperator( getNthGeneralizedNonagonalNumberOperator, 1 ),
    'generalized_octagonal'         : RPNOperator( getNthGeneralizedOctagonalNumberOperator, 1 ),
    'generalized_pentagonal'        : RPNOperator( getNthGeneralizedPentagonalNumberOperator, 1 ),
    'heptagonal'                    : RPNOperator( getNthHeptagonalNumberOperator, 1 ),
    'heptagonal_hexagonal'          : RPNOperator( getNthHeptagonalHexagonalNumberOperator, 1 ),
    'heptagonal_pentagonal'         : RPNOperator( getNthHeptagonalPentagonalNumberOperator, 1 ),
    'heptagonal_square'             : RPNOperator( getNthHeptagonalSquareNumberOperator, 1 ),
    'heptagonal_triangular'         : RPNOperator( getNthHeptagonalTriangularNumberOperator, 1 ),
    'hexagonal'                     : RPNOperator( getNthHexagonalNumberOperator, 1 ),
    'hexagonal_pentagonal'          : RPNOperator( getNthHexagonalPentagonalNumberOperator, 1 ),
    'hexagonal_square'              : RPNOperator( getNthHexagonalSquareNumberOperator, 1 ),
    'icosahedral'                   : RPNOperator( getNthIcosahedralNumberOperator, 1 ),
    'nonagonal'                     : RPNOperator( getNthNonagonalNumberOperator, 1 ),
    'nonagonal_heptagonal'          : RPNOperator( getNthNonagonalHeptagonalNumberOperator, 1 ),
    'nonagonal_hexagonal'           : RPNOperator( getNthNonagonalHexagonalNumberOperator, 1 ),
    'nonagonal_octagonal'           : RPNOperator( getNthNonagonalOctagonalNumberOperator, 1 ),
    'nonagonal_pentagonal'          : RPNOperator( getNthNonagonalPentagonalNumberOperator, 1 ),
    'nonagonal_square'              : RPNOperator( getNthNonagonalSquareNumberOperator, 1 ),
    'nonagonal_triangular'          : RPNOperator( getNthNonagonalTriangularNumberOperator, 1 ),
    'nth_centered_decagonal'        : RPNOperator( findCenteredDecagonalNumberOperator, 1 ),
    'nth_centered_heptagonal'       : RPNOperator( findCenteredHeptagonalNumberOperator, 1 ),
    'nth_centered_hexagonal'        : RPNOperator( findCenteredHexagonalNumberOperator, 1 ),
    'nth_centered_nonagonal'        : RPNOperator( findCenteredNonagonalNumberOperator, 1 ),
    'nth_centered_octagonal'        : RPNOperator( findCenteredOctagonalNumberOperator, 1 ),
    'nth_centered_pentagonal'       : RPNOperator( findCenteredPentagonalNumberOperator, 1 ),
    'nth_centered_polygonal'        : RPNOperator( findCenteredPolygonalNumberOperator, 2 ),
    'nth_centered_square'           : RPNOperator( findCenteredSquareNumberOperator, 1 ),
    'nth_centered_triangular'       : RPNOperator( findCenteredTriangularNumberOperator, 1 ),
    'nth_decagonal'                 : RPNOperator( findDecagonalNumberOperator, 1 ),
    'nth_heptagonal'                : RPNOperator( findHeptagonalNumberOperator, 1 ),
    'nth_hexagonal'                 : RPNOperator( findHexagonalNumberOperator, 1 ),
    'nth_nonagonal'                 : RPNOperator( findNonagonalNumberOperator, 1 ),
    'nth_octagonal'                 : RPNOperator( findOctagonalNumberOperator, 1 ),
    'nth_pentagonal'                : RPNOperator( findPentagonalNumberOperator, 1 ),
    'nth_polygonal'                 : RPNOperator( findPolygonalNumberOperator, 2 ),
    'nth_square'                    : RPNOperator( findSquareNumberOperator, 1 ),
    'nth_triangular'                : RPNOperator( findTriangularNumberOperator, 1 ),
    'octagonal'                     : RPNOperator( getNthOctagonalNumberOperator, 1 ),
    'octagonal_heptagonal'          : RPNOperator( getNthOctagonalHeptagonalNumberOperator, 1 ),
    'octagonal_hexagonal'           : RPNOperator( getNthOctagonalHexagonalNumberOperator, 1 ),
    'octagonal_pentagonal'          : RPNOperator( getNthOctagonalPentagonalNumberOperator, 1 ),
    'octagonal_square'              : RPNOperator( getNthOctagonalSquareNumberOperator, 1 ),
    'octagonal_triangular'          : RPNOperator( getNthOctagonalTriangularNumberOperator, 1 ),
    'octahedral'                    : RPNOperator( getNthOctahedralNumberOperator, 1 ),
    'pentagonal'                    : RPNOperator( getNthPentagonalNumberOperator, 1 ),
    'pentagonal_square'             : RPNOperator( getNthPentagonalSquareNumberOperator, 1 ),
    'pentagonal_triangular'         : RPNOperator( getNthPentagonalTriangularNumberOperator, 1 ),
    'pentatope'                     : RPNOperator( getNthPentatopeNumberOperator, 1 ),
    'polygonal'                     : RPNOperator( getNthPolygonalNumberOperator, 2 ),
    'polygonal_pyramidal'           : RPNOperator( getNthPolygonalPyramidalNumberOperator, 2 ),
    'polytope'                      : RPNOperator( getNthPolytopeNumberOperator, 2 ),
    'pyramidal'                     : RPNOperator( getNthPyramidalNumberOperator, 1 ),
    'rhombic_dodecahedral'          : RPNOperator( getNthRhombicDodecahedralNumberOperator, 1 ),
    'square_triangular'             : RPNOperator( getNthSquareTriangularNumberOperator, 1 ),
    'star'                          : RPNOperator( getNthStarNumberOperator, 1 ),
    'stella_octangula'              : RPNOperator( getNthStellaOctangulaNumberOperator, 1 ),
    'tetrahedral'                   : RPNOperator( getNthTetrahedralNumberOperator, 1 ),
    'triangular'                    : RPNOperator( getNthTriangularNumberOperator, 1 ),
    'truncated_octahedral'          : RPNOperator( getNthTruncatedOctahedralNumberOperator, 1 ),
    'truncated_tetrahedral'         : RPNOperator( getNthTruncatedTetrahedralNumberOperator, 1 ),

    # function
    #'break_on'                      : RPNOperator( breakOnCondition, 3 ),
    'eval0'                         : RPNOperator( evaluateFunction0Operator, 1 ),
    'eval'                          : RPNOperator( evaluateFunctionOperator, 2 ),
    'eval2'                         : RPNOperator( evaluateFunction2Operator, 3 ),
    'eval3'                         : RPNOperator( evaluateFunction3Operator, 4 ),
    'eval_list'                     : RPNOperator( evaluateListFunctionOperator, 2 ),
    'eval_list2'                    : RPNOperator( evaluateListFunction2Operator, 3 ),
    'eval_list3'                    : RPNOperator( evaluateListFunction3Operator, 4 ),
    'filter_integers'               : RPNOperator( filterIntegersOperator, 2 ),
    'function'                      : RPNOperator( createUserFunctionOperator, 2 ),
    'limit'                         : RPNOperator( evaluateLimitOperator, 2 ),
    'limitn'                        : RPNOperator( evaluateReverseLimitOperator, 2 ),
    'nprod'                         : RPNOperator( evaluateProductOperator, 3 ),
    'nsum'                          : RPNOperator( evaluateSumOperator, 3 ),
    'plot'                          : RPNOperator( plotFunctionOperator, 3 ),
    'plot2'                         : RPNOperator( plot2DFunctionOperator, 5 ),
    'plot_complex'                  : RPNOperator( plotComplexFunctionOperator, 5 ),
    'recurrence'                    : RPNOperator( evaluateRecurrenceOperator, 3 ),
    'repeat'                        : RPNOperator( repeatOperator, 2 ),
    'sequence'                      : RPNOperator( getSequenceOperator, 3 ),

    # geography
    'geographic_distance'           : RPNOperator( getGeographicDistanceOperator, 2 ),
    'get_timezone'                  : RPNOperator( getTimeZoneOperator, 1 ),
    'lat_long'                      : RPNOperator( makeLocationOperator, 2 ),
    'location_info'                 : RPNOperator( getLocationInfoOperator, 1 ),

    # geometry
    'antiprism_area'                : RPNOperator( getAntiprismSurfaceAreaOperator, 2 ),
    'antiprism_volume'              : RPNOperator( getAntiprismVolumeOperator, 2 ),
    'cone_area'                     : RPNOperator( getConeSurfaceAreaOperator, 2 ),
    'cone_volume'                   : RPNOperator( getConeVolumeOperator, 2 ),
    'dodecahedron_area'             : RPNOperator( getDodecahedronSurfaceAreaOperator, 1 ),
    'dodecahedron_volume'           : RPNOperator( getDodecahedronVolumeOperator, 1 ),
    'hypotenuse'                    : RPNOperator( calculateHypotenuseOperator, 2 ),
    'icosahedron_area'              : RPNOperator( getIcosahedronSurfaceAreaOperator, 1 ),
    'icosahedron_volume'            : RPNOperator( getIcosahedronVolumeOperator, 1 ),
    'k_sphere_area'                 : RPNOperator( getKSphereSurfaceAreaOperator, 2 ),
    'k_sphere_radius'               : RPNOperator( getKSphereRadiusOperator, 2 ),
    'k_sphere_volume'               : RPNOperator( getKSphereVolumeOperator, 2 ),
    'octahedron_area'               : RPNOperator( getOctahedronSurfaceAreaOperator, 1 ),
    'octahedron_volume'             : RPNOperator( getOctahedronVolumeOperator, 1 ),
    'polygon_area'                  : RPNOperator( getRegularPolygonAreaOperator, 2 ),
    'prism_area'                    : RPNOperator( getPrismSurfaceAreaOperator, 3 ),
    'prism_volume'                  : RPNOperator( getPrismVolumeOperator, 3 ),
    'sphere_area'                   : RPNOperator( getSphereAreaOperator, 1 ),
    'sphere_radius'                 : RPNOperator( getSphereRadiusOperator, 1 ),
    'sphere_volume'                 : RPNOperator( getSphereVolumeOperator, 1 ),
    'tetrahedron_area'              : RPNOperator( getTetrahedronSurfaceAreaOperator, 1 ),
    'tetrahedron_volume'            : RPNOperator( getTetrahedronVolumeOperator, 1 ),
    'torus_area'                    : RPNOperator( getTorusSurfaceAreaOperator, 2 ),
    'torus_volume'                  : RPNOperator( getTorusVolumeOperator, 2 ),
    'triangle_area'                 : RPNOperator( getTriangleAreaOperator, 3 ),

    # lexicographic
    'add_digits'                    : RPNOperator( addDigits, 2 ),
    'build_numbers'                 : RPNOperator( buildNumbers, 1 ),
    'build_step_numbers'            : RPNOperator( buildStepNumbers, 1 ),
    'count_different_digits'        : RPNOperator( countDifferentDigits, 1 ),
    'count_digits'                  : RPNOperator( countDigits, 2 ),
    'cyclic_permutations'           : RPNOperator( getCyclicPermutations, 1 ),
    'digits'                        : RPNOperator( getDigitCount, 1 ),
    'duplicate_digits'              : RPNOperator( duplicateDigits, 2 ),
    'duplicate_number'              : RPNOperator( duplicateNumber, 2 ),
    'erdos_persistence'             : RPNOperator( getErdosPersistence, 1 ),
    'find_palindrome'               : RPNOperator( findPalindrome, 2 ),
    'get_base_k_digits'             : RPNOperator( getBaseKDigits, 2 ),
    'get_digits'                    : RPNOperator( getDigits, 1 ),
    'get_left_digits'               : RPNOperator( getLeftDigits, 2 ),
    'get_left_truncations'          : RPNOperator( getLeftTruncationsGenerator, 1 ),
    'get_nonzero_base_k_digits'     : RPNOperator( getNonzeroBaseKDigits, 2 ),
    'get_nonzero_digits'            : RPNOperator( getNonzeroDigits, 1 ),
    'get_right_digits'              : RPNOperator( getRightDigits, 2 ),
    'get_right_truncations'         : RPNOperator( getRightTruncationsGenerator, 1 ),
    'has_any_digits'                : RPNOperator( containsAnyDigits, 2 ),
    'has_digits'                    : RPNOperator( containsDigits, 2 ),
    'has_only_digits'               : RPNOperator( containsOnlyDigits, 2 ),
    'is_automorphic'                : RPNOperator( isAutomorphic, 1 ),
    'is_base_k_pandigital'          : RPNOperator( isBaseKPandigital, 2 ),
    'is_base_k_smith_number'        : RPNOperator( isBaseKSmithNumber, 2 ),
    'is_bouncy'                     : RPNOperator( isBouncy, 1 ),
    'is_decreasing'                 : RPNOperator( isDecreasing, 1 ),
    'is_digital_palindrome'         : RPNOperator( isPalindromeOperator, 1 ),
    'is_digital_permutation'        : RPNOperator( isDigitalPermutation, 2 ),
    'is_generalized_dudeney'        : RPNOperator( isGeneralizedDudeneyNumber, 2 ),
    'is_harshad'                    : RPNOperator( isHarshadNumber, 2 ),
    'is_increasing'                 : RPNOperator( isIncreasing, 1 ),
    'is_kaprekar'                   : RPNOperator( isKaprekarNumber, 1 ),
    'is_k_morphic'                  : RPNOperator( isKMorphicOperator, 2 ),
    'is_k_narcissistic'             : RPNOperator( isBaseKNarcissistic, 2 ),
    'is_narcissistic'               : RPNOperator( isNarcissistic, 1 ),
    'is_order_k_smith_number'       : RPNOperator( isOrderKSmithNumber, 2 ),
    'is_pandigital'                 : RPNOperator( isPandigital, 1 ),
    'is_pddi'                       : RPNOperator( isPerfectDigitToDigitInvariant, 2 ),
    'is_pdi'                        : RPNOperator( isPerfectDigitalInvariant, 1 ),
    'is_smith_number'               : RPNOperator( isSmithNumber, 1 ),
    'is_step_number'                : RPNOperator( isStepNumber, 1 ),
    'is_sum_product'                : RPNOperator( isSumProductNumber, 2 ),
    'is_trimorphic'                 : RPNOperator( isTrimorphic, 1 ),
    'k_persistence'                 : RPNOperator( getKPersistence, 2 ),
    'multiply_digits'               : RPNOperator( multiplyDigits, 1 ),
    'multiply_digit_powers'         : RPNOperator( multiplyDigitPowers, 2 ),
    'multiply_nonzero_digits'       : RPNOperator( multiplyNonzeroDigits, 1 ),
    'multiply_nonzero_digit_powers' : RPNOperator( multiplyNonzeroDigitPowers, 2 ),
    'permute_digits'                : RPNOperator( permuteDigits, 1 ),
    'persistence'                   : RPNOperator( getPersistence, 1 ),
    'replace_digits'                : RPNOperator( replaceDigits, 3 ),
    'reverse_digits'                : RPNOperator( reverseDigitsOperator, 1 ),
    'rotate_digits_left'            : RPNOperator( rotateDigitsLeft, 2 ),
    'rotate_digits_right'           : RPNOperator( rotateDigitsRight, 2 ),
    'show_erdos_persistence'        : RPNOperator( showErdosPersistence, 1 ),
    'show_k_persistence'            : RPNOperator( showKPersistence, 2 ),
    'show_persistence'              : RPNOperator( showPersistence, 1 ),
    'square_digit_chain'            : RPNOperator( generateSquareDigitChain, 1 ),
    'sum_digits'                    : RPNOperator( sumDigits, 1 ),

    # list
    'exponential_range'             : RPNOperator( createExponentialRangeOperator, 3 ),
    'geometric_range'               : RPNOperator( createGeometricRangeOperator, 3 ),
    'interval_range'                : RPNOperator( createIntervalRangeOperator, 3 ),
    'range'                         : RPNOperator( createRangeOperator, 2 ),
    'sized_range'                   : RPNOperator( createSizedRangeOperator, 3 ),

    # logarithms
    'lambertw'                      : RPNOperator( getLambertWOperator, 1 ),
    'li'                            : RPNOperator( getLIOperator, 1 ),
    'log'                           : RPNOperator( getLogOperator, 1 ),
    'log10'                         : RPNOperator( getLog10Operator, 1 ),
    'log2'                          : RPNOperator( getLog2Operator, 1 ),
    'logxy'                         : RPNOperator( getLogXYOperator, 2 ),
    'polyexp'                       : RPNOperator( getPolyexpOperator, 2 ),
    'polylog'                       : RPNOperator( getPolylogOperator, 2 ),

    # logical
    'and'                           : RPNOperator( andOperator, 2 ),
    'nand'                          : RPNOperator( nandOperator, 2 ),
    'nor'                           : RPNOperator( norOperator, 2 ),
    'not'                           : RPNOperator( notOperator, 1 ),
    'or'                            : RPNOperator( orOperator, 2 ),
    'xnor'                          : RPNOperator( xnorOperator, 2 ),
    'xor'                           : RPNOperator( xorOperator, 2 ),

    # number_theory
    'abundance'                     : RPNOperator( getAbundanceOperator, 1 ),
    'abundance_ratio'               : RPNOperator( getAbundanceRatio, 1 ),
    'ackermann_number'              : RPNOperator( calculateAckermannFunctionOperator, 2 ),
    'aliquot'                       : RPNOperator( getAliquotSequence, 2 ),
    'aliquot_limit'                 : RPNOperator( getLimitedAliquotSequence, 2 ),
    'alternating_factorial'         : RPNOperator( getNthAlternatingFactorial, 1 ),
    'alternating_harmonic_fraction' : RPNOperator( getAlternatingHarmonicFraction, 1 ),
    'barnesg'                       : RPNOperator( getBarnesG, 1 ),
    'beta'                          : RPNOperator( getBeta, 2 ),
    'calkin_wilf'                   : RPNOperator( getNthCalkinWilf, 1 ),
    'collatz'                       : RPNOperator( getCollatzSequence, 2 ),
    'count_divisors'                : RPNOperator( getDivisorCountOperator, 1 ),
    'cyclotomic'                    : RPNOperator( getCyclotomic, 2 ),
    'digamma'                       : RPNOperator( getDigamma, 1 ),
    'digital_root'                  : RPNOperator( getDigitalRoot, 1 ),
    'divisors'                      : RPNOperator( getDivisorsOperator, 1 ),
    'double_factorial'              : RPNOperator( getNthDoubleFactorial, 1 ),
    'egyptian_fractions'            : RPNOperator( getGreedyEgyptianFraction, 2 ),
    'eta'                           : RPNOperator( getAltZeta, 1 ),
    'euler_brick'                   : RPNOperator( makeEulerBrick, 3 ),
    'euler_phi'                     : RPNOperator( getEulerPhi, 1 ),
    'factor'                        : RPNOperator( getFactorsOperator, 1 ),
    'factorial'                     : RPNOperator( getNthFactorial, 1 ),
    'fibonacci'                     : RPNOperator( getNthFibonacci, 1 ),
    'fibonorial'                    : RPNOperator( getNthFibonorial, 1 ),
    'find_sum_of_cubes'             : RPNOperator( findNthSumOfCubes, 1 ),
    'find_sum_of_squares'           : RPNOperator( findNthSumOfSquares, 1 ),
    'fraction'                      : RPNOperator( interpretAsFraction, 2 ),
    'gamma'                         : RPNOperator( getGamma, 1 ),
    'generate_polydivisibles'       : RPNOperator( generatePolydivisibles, 1 ),
    'harmonic_fraction'             : RPNOperator( getHarmonicFraction, 1 ),
    'harmonic_residue'              : RPNOperator( getHarmonicResidueOperator, 1 ),
    'heptanacci'                    : RPNOperator( getNthHeptanacci, 1 ),
    'hexanacci'                     : RPNOperator( getNthHexanacci, 1 ),
    'hurwitz_zeta'                  : RPNOperator( getHurwitzZeta, 2 ),
    'hyperfactorial'                : RPNOperator( getNthHyperfactorial, 1 ),
    'is_abundant'                   : RPNOperator( isAbundant, 1 ),
    'is_achilles'                   : RPNOperator( isAchillesNumber, 1 ),
    'is_antiharmonic'               : RPNOperator( isAntiharmonic, 1 ),
    'is_carmichael'                 : RPNOperator( isCarmichaelNumberOperator, 1 ),
    'is_composite'                  : RPNOperator( isCompositeOperator, 1 ),
    'is_deficient'                  : RPNOperator( isDeficient, 1 ),
    'is_harmonic_divisor_number'    : RPNOperator( isHarmonicDivisorNumber, 1 ),
    'is_k_hyperperfect'             : RPNOperator( isKHyperperfect, 2 ),
    'is_k_perfect'                  : RPNOperator( isKPerfect, 2 ),
    'is_k_semiprime'                : RPNOperator( isKSemiprimeOperator, 2 ),
    'is_k_sphenic'                  : RPNOperator( isKSphenicOperator, 2 ),
    'is_perfect'                    : RPNOperator( isPerfect, 1 ),
    'is_pernicious'                 : RPNOperator( isPernicious, 1 ),
    'is_polydivisible'              : RPNOperator( isPolydivisible, 1 ),
    'is_powerful'                   : RPNOperator( isPowerful, 1 ),
    'is_prime'                      : RPNOperator( isPrimeOperator, 1 ),
    'is_pronic'                     : RPNOperator( isPronic, 1 ),
    'is_rough'                      : RPNOperator( isRoughOperator, 2 ),
    'is_ruth_aaron'                 : RPNOperator( isRuthAaronNumber, 1 ),
    'is_semiprime'                  : RPNOperator( isSemiprime, 1 ),
    'is_smooth'                     : RPNOperator( isSmoothOperator, 2 ),
    'is_sphenic'                    : RPNOperator( isSphenic, 1 ),
    'is_squarefree'                 : RPNOperator( isSquareFree, 1 ),
    'is_strong_pseudoprime'         : RPNOperator( isStrongPseudoprime, 2 ),
    'is_unusual'                    : RPNOperator( isUnusual, 1 ),
    'k_fibonacci'                   : RPNOperator( getNthKFibonacciNumber, 2 ),
    'leyland_number'                : RPNOperator( getLeylandNumber, 2 ),
    'log_gamma'                     : RPNOperator( getLogGamma, 1 ),
    'lucas'                         : RPNOperator( getNthLucasNumber, 1 ),
    'make_continued_fraction'       : RPNOperator( makeContinuedFraction, 2 ),
    'make_pyth_3'                   : RPNOperator( makePythagoreanTriple, 2 ),
    'make_pyth_4'                   : RPNOperator( makePythagoreanQuadruple, 2 ),
    'nth_carol'                     : RPNOperator( getNthCarolNumber, 1 ),
    'nth_harmonic_number'           : RPNOperator( getNthHarmonicNumber, 1 ),
    'nth_jacobsthal'                : RPNOperator( getNthJacobsthalNumber, 1 ),
    'nth_k_thabit'                  : RPNOperator( getNthKThabitNumber, 2 ),
    'nth_k_thabit_2'                : RPNOperator( getNthKThabit2Number, 2 ),
    'nth_kynea'                     : RPNOperator( getNthKyneaNumber, 1 ),
    'nth_leonardo'                  : RPNOperator( getNthLeonardoNumber, 1 ),
    'nth_mersenne_exponent'         : RPNOperator( getNthMersenneExponent, 1 ),
    'nth_mersenne_prime'            : RPNOperator( getNthMersennePrime, 1 ),
    'nth_merten'                    : RPNOperator( getNthMerten, 1 ),
    'nth_mobius'                    : RPNOperator( getNthMobiusNumberOperator, 1 ),
    'nth_padovan'                   : RPNOperator( getNthPadovanNumber, 1 ),
    'nth_perfect_number'            : RPNOperator( getNthPerfectNumber, 1 ),
    'nth_stern'                     : RPNOperator( getNthSternNumberOperator, 1 ),
    'nth_thabit'                    : RPNOperator( getNthThabitNumber, 1 ),
    'nth_thabit_2'                  : RPNOperator( getNthThabit2Number, 1 ),
    'nth_thue_morse'                : RPNOperator( getNthThueMorseNumberOperator, 1 ),
    'octanacci'                     : RPNOperator( getNthOctanacci, 1 ),
    'pascal_triangle'               : RPNOperator( getNthPascalLine, 1 ),
    'pentanacci'                    : RPNOperator( getNthPentanacci, 1 ),
    'phitorial'                     : RPNOperator( getNthPhitorial, 1 ),
    'polygamma'                     : RPNOperator( getPolygamma, 2 ),
    'polygorial'                    : RPNOperator( getNthKPolygorial, 2 ),
    'primorial'                     : RPNOperator( getNthPrimorial, 1 ),
    'pythagorean_triples'           : RPNOperator( makePythagoreanTriples, 1 ),
    'radical'                       : RPNOperator( getRadical, 1 ),
    'relatively_prime'              : RPNOperator( areRelativelyPrimeOperator, 2 ),
    'repunit'                       : RPNOperator( getNthBaseKRepunit, 2 ),
    'reversal_addition'             : RPNOperator( getNthReversalAddition, 2 ),
    'sigma'                         : RPNOperator( getSigmaOperator, 1 ),
    'sigma_k'                       : RPNOperator( getSigmaKOperator, 2 ),
    'subfactorial'                  : RPNOperator( getNthSubfactorial, 1 ),
    'sums_of_k_powers'              : RPNOperator( findSumsOfKPowers, 3 ),
    'sums_of_k_nonzero_powers'      : RPNOperator( findSumsOfKNonzeroPowers, 3 ),
    'superfactorial'                : RPNOperator( getNthSuperfactorial, 1 ),
    'tetranacci'                    : RPNOperator( getNthTetranacci, 1 ),
    'tribonacci'                    : RPNOperator( getNthTribonacci, 1 ),
    'trigamma'                      : RPNOperator( getTrigamma, 1 ),
    'unit_roots'                    : RPNOperator( getUnitRoots, 1 ),
    'zeta'                          : RPNOperator( getZeta, 1 ),
    'zeta_zero'                     : RPNOperator( getNthZetaZero, 1 ),

    # physics
    'acceleration'                  : RPNOperator( calculateAcceleration, 2 ),
    'black_hole_entropy'            : RPNOperator( calculateBlackHoleEntropy, 1 ),
    'black_hole_lifetime'           : RPNOperator( calculateBlackHoleLifetime, 1 ),
    'black_hole_luminosity'         : RPNOperator( calculateBlackHoleLuminosity, 1 ),
    'black_hole_mass'               : RPNOperator( calculateBlackHoleMass, 1 ),
    'black_hole_radius'             : RPNOperator( calculateBlackHoleRadius, 1 ),
    'black_hole_surface_area'       : RPNOperator( calculateBlackHoleSurfaceArea, 1 ),
    'black_hole_surface_gravity'    : RPNOperator( calculateBlackHoleSurfaceGravity, 1 ),
    'black_hole_surface_tides'      : RPNOperator( calculateBlackHoleSurfaceTides, 1 ),
    'black_hole_temperature'        : RPNOperator( calculateBlackHoleTemperature, 1 ),
    'distance'                      : RPNOperator( calculateDistance, 2 ),
    'energy_equivalence'            : RPNOperator( calculateEnergyEquivalence, 1 ),
    'escape_velocity'               : RPNOperator( calculateEscapeVelocity, 2 ),
    'heat_index'                    : RPNOperator( calculateHeatIndex, 2 ),
    'horizon_distance'              : RPNOperator( calculateHorizonDistance, 2 ),
    'kinetic_energy'                : RPNOperator( calculateKineticEnergy, 2 ),
    'mass_equivalence'              : RPNOperator( calculateMassEquivalence, 1 ),
    'orbital_mass'                  : RPNOperator( calculateOrbitalMass, 2 ),
    'orbital_period'                : RPNOperator( calculateOrbitalPeriod, 2 ),
    'orbital_radius'                : RPNOperator( calculateOrbitalRadius, 2 ),
    'orbital_velocity'              : RPNOperator( calculateOrbitalVelocity, 2 ),
    'surface_gravity'               : RPNOperator( calculateSurfaceGravity, 2 ),
    'tidal_force'                   : RPNOperator( calculateTidalForce, 3 ),
    'time_dilation'                 : RPNOperator( calculateTimeDilation, 1 ),
    'velocity'                      : RPNOperator( calculateVelocity, 2 ),
    'wind_chill'                    : RPNOperator( calculateWindChill, 2 ),

    # powers_and_roots
    'agm'                           : RPNOperator( getAGMOperator, 2 ),
    'cube'                          : RPNOperator( cubeOperator, 1 ),
    'cube_root'                     : RPNOperator( getCubeRootOperator, 1 ),
    'cube_super_root'               : RPNOperator( getCubeSuperRootOperator, 1 ),
    'exp'                           : RPNOperator( getExpOperator, 1 ),
    'exp10'                         : RPNOperator( getExp10Operator, 1 ),
    'expphi'                        : RPNOperator( getExpPhiOperator, 1 ),
    'hyperoperator'                 : RPNOperator( calculateNthHyperoperatorOperator, 3 ),
    'hyperoperator_right'           : RPNOperator( calculateNthRightHyperoperatorOperator, 3 ),
    'power'                         : RPNOperator( getPowerOperator, 2 ),
    'powmod'                        : RPNOperator( getPowModOperator, 3 ),
    'root'                          : RPNOperator( getRootOperator, 2 ),
    'square'                        : RPNOperator( squareOperator, 1 ),
    'square_root'                   : RPNOperator( getSquareRootOperator, 1 ),
    'square_super_root'             : RPNOperator( getSquareSuperRootOperator, 1 ),
    'super_root'                    : RPNOperator( getSuperRootOperator, 2 ),
    'super_roots'                   : RPNOperator( getSuperRootsOperator, 2 ),
    'tetrate'                       : RPNOperator( tetrateOperator, 2 ),
    'tetrate_right'                 : RPNOperator( tetrateRightOperator, 2 ),

    # prime_number
    'balanced_prime'                : RPNOperator( getNthBalancedPrime, 1 ),
    'balanced_primes'               : RPNOperator( getNthBalancedPrimeList, 1 ),
    'cousin_prime'                  : RPNOperator( getNthCousinPrime, 1 ),
    'cousin_primes'                 : RPNOperator( getNthCousinPrimeList, 1 ),
    'double_balanced_prime'         : RPNOperator( getNthDoubleBalancedPrime, 1 ),
    'double_balanced_primes'        : RPNOperator( getNthDoubleBalancedPrimeList, 1 ),
    'isolated_prime'                : RPNOperator( getNthIsolatedPrime, 1 ),
    'next_prime'                    : RPNOperator( getNextPrimeOperator, 1 ),
    'next_primes'                   : RPNOperator( getNextPrimesOperator, 2 ),
    'next_quadruplet_prime'         : RPNOperator( getNextQuadrupletPrime, 1 ),
    'next_quadruplet_primes'        : RPNOperator( getNextQuadrupletPrimes, 1 ),
    'next_quintuplet_prime'         : RPNOperator( getNextQuintupletPrime, 1 ),
    'next_quintuplet_primes'        : RPNOperator( getNextQuintupletPrimes, 1 ),
    'next_sextuplet_prime'          : RPNOperator( getNextSextupletPrime, 1 ),
    'next_sextuplet_primes'         : RPNOperator( getNextSextupletPrimes, 1 ),
    'next_triplet_prime'            : RPNOperator( getNextTripletPrime, 1 ),
    'next_triplet_primes'           : RPNOperator( getNextTripletPrimes, 1 ),
    'next_twin_prime'               : RPNOperator( getNextTwinPrime, 1 ),
    'next_twin_primes'              : RPNOperator( getNextTwinPrimes, 1 ),
    'nth_prime'                     : RPNOperator( findPrimeOperator, 1 ),
    'nth_quadruplet_prime'          : RPNOperator( findQuadrupletPrimeOperator, 1 ),
    'nth_quintuplet_prime'          : RPNOperator( findQuintupletPrimeOperator, 1 ),
    'nth_sextuplet_prime'           : RPNOperator( findSextupletPrimeOperator, 1 ),
    'nth_triplet_prime'             : RPNOperator( findTripletPrimeOperator, 1 ),
    'nth_twin_prime'                : RPNOperator( findTwinPrimeOperator, 1 ),
    'octy_prime'                    : RPNOperator( getNthOctyPrime, 1 ),
    'octy_primes'                   : RPNOperator( getNthOctyPrimeList, 1 ),
    'polyprime'                     : RPNOperator( getNthPolyPrime, 2 ),
    'previous_prime'                : RPNOperator( getPreviousPrimeOperator, 1 ),
    'previous_primes'               : RPNOperator( getPreviousPrimesOperator, 2 ),
    'prime'                         : RPNOperator( getNthPrime, 1 ),
    'primes'                        : RPNOperator( getPrimesGenerator, 2 ),
    'prime_pi'                      : RPNOperator( getPrimePi, 1 ),
    'prime_range'                   : RPNOperator( getPrimeRange, 2 ),
    'quadruplet_prime'              : RPNOperator( getNthQuadrupletPrime, 1 ),
    'quadruplet_primes'             : RPNOperator( getNthQuadrupletPrimeList, 1 ),
    'quadruple_balanced_prime'      : RPNOperator( getNthQuadrupleBalancedPrime, 1 ),
    'quadruple_balanced_primes'     : RPNOperator( getNthQuadrupleBalancedPrimeList, 1 ),
    'quintuplet_prime'              : RPNOperator( getNthQuintupletPrime, 1 ),
    'quintuplet_primes'             : RPNOperator( getNthQuintupletPrimeList, 1 ),
    'safe_prime'                    : RPNOperator( getSafePrime, 1 ),
    'sextuplet_prime'               : RPNOperator( getNthSextupletPrime, 1 ),
    'sextuplet_primes'              : RPNOperator( getNthSextupletPrimeList, 1 ),
    'sexy_prime'                    : RPNOperator( getNthSexyPrime, 1 ),
    'sexy_primes'                   : RPNOperator( getNthSexyPrimeList, 1 ),
    'sexy_quadruplet'               : RPNOperator( getNthSexyQuadruplet, 1 ),
    'sexy_quadruplets'              : RPNOperator( getNthSexyQuadrupletList, 1 ),
    'sexy_triplet'                  : RPNOperator( getNthSexyTriplet, 1 ),
    'sexy_triplets'                 : RPNOperator( getNthSexyTripletList, 1 ),
    'sophie_prime'                  : RPNOperator( getNthSophiePrime, 1 ),
    'super_prime'                   : RPNOperator( getNthSuperPrime, 1 ),
    'triplet_prime'                 : RPNOperator( getNthTripletPrime, 1 ),
    'triplet_primes'                : RPNOperator( getNthTripletPrimeList, 1 ),
    'triple_balanced_prime'         : RPNOperator( getNthTripleBalancedPrime, 1 ),
    'triple_balanced_primes'        : RPNOperator( getNthTripleBalancedPrimeList, 1 ),
    'twin_prime'                    : RPNOperator( getNthTwinPrime, 1 ),
    'twin_primes'                   : RPNOperator( getNthTwinPrimeList, 1 ),

    # settings
    'accuracy'                      : RPNOperator( lambda n: setAccuracy( fadd( n, 2 ) ), 1 ),
    'comma'                         : RPNOperator( setComma, 1 ),
    'comma_mode'                    : RPNOperator( setCommaMode, 0 ),
    'decimal_grouping'              : RPNOperator( setDecimalGrouping, 1 ),
    'hex_mode'                      : RPNOperator( setHexMode, 0 ),
    'identify'                      : RPNOperator( setIdentify, 1 ),
    'identify_mode'                 : RPNOperator( setIdentifyMode, 0 ),
    'input_radix'                   : RPNOperator( setInputRadix, 1 ),
    'integer_grouping'              : RPNOperator( setIntegerGrouping, 1 ),
    'leading_zero'                  : RPNOperator( setLeadingZero, 1 ),
    'leading_zero_mode'             : RPNOperator( setLeadingZeroMode, 0 ),
    'octal_mode'                    : RPNOperator( setOctalMode, 0 ),
    'output_radix'                  : RPNOperator( setOutputRadix, 1 ),
    'precision'                     : RPNOperator( setPrecision, 1 ),
    'timer'                         : RPNOperator( setTimer, 1 ),
    'timer_mode'                    : RPNOperator( setTimerMode, 0 ),

    # special
    'base_units'                    : RPNOperator( convertToBaseUnitsOperator, 1 ),
    'delete_config'                 : RPNOperator( deleteUserConfiguration, 1 ),
    'describe'                      : RPNOperator( describeInteger, 1 ),
    'dimensions'                    : RPNOperator( getDimensions, 1 ),
    'dump_config'                   : RPNOperator( dumpUserConfiguration, 0 ),
    'enumerate_dice'                : RPNOperator( enumerateDiceGenerator, 1 ),
    'enumerate_dice_'               : RPNOperator( enumerateMultipleDiceGenerator, 2 ),
    'estimate'                      : RPNOperator( estimateOperator, 1 ),
    'help'                          : RPNOperator( printHelpMessage, 0 ),
    'get_config'                    : RPNOperator( getUserConfiguration, 1 ),
    'get_variable'                  : RPNOperator( getUserVariable, 1 ),
    'if'                            : RPNOperator( lambda a, b, c: a if c else b, 3 ),
    'list_from_file'                : RPNOperator( readListFromFile, 1 ),
    'name'                          : RPNOperator( getNameOperator, 1 ),
    'oeis'                          : RPNOperator( downloadOEISSequence, 1 ),
    'oeis_comment'                  : RPNOperator( downloadOEISComment, 1 ),
    'oeis_ex'                       : RPNOperator( downloadOEISExtra, 1 ),
    'oeis_name'                     : RPNOperator( downloadOEISName, 1 ),
    'oeis_offset'                   : RPNOperator( downloadOEISOffset, 1 ),
    'ordinal_name'                  : RPNOperator( getOrdinalNameOperator, 1 ),
    'permute_dice'                  : RPNOperator( permuteDiceGenerator, 1 ),
    'primitive_units'               : RPNOperator( convertToPrimitiveUnitsOperator, 1 ),
    'random'                        : RPNOperator( getRandomNumber, 0 ),
    'random_'                       : RPNOperator( getMultipleRandomsGenerator, 1 ),
    'random_integer'                : RPNOperator( getRandomInteger, 1 ),
    'random_integers'               : RPNOperator( getRandomIntegersGenerator, 2 ),
    'result'                        : RPNOperator( loadResult, 0 ),
    'roll_dice'                     : RPNOperator( rollDice, 1 ),
    'roll_simple_dice'              : RPNOperator( rollSimpleDice, 2 ),
    'roll_dice_'                    : RPNOperator( rollMultipleDiceGenerator, 2 ),
    'set_config'                    : RPNOperator( setUserConfiguration, 2 ),
    'set_variable'                  : RPNOperator( setUserVariable, 2 ),

    #'topics' doesn't need to be handled here, see rpn.py, search for 'topics'

    'uuid'                          : RPNOperator( generateUUIDOperator, 0 ),
    'uuid_random'                   : RPNOperator( generateRandomUUIDOperator, 0 ),
    'value'                         : RPNOperator( getValueOperator, 1 ),

    # trigonometry
    'acos'                          : RPNOperator( acosOperator, 1 ),
    'acosh'                         : RPNOperator( acoshOperator, 1 ),
    'acot'                          : RPNOperator( acotOperator, 1 ),
    'acoth'                         : RPNOperator( acothOperator, 1 ),
    'acsc'                          : RPNOperator( acscOperator, 1 ),
    'acsch'                         : RPNOperator( acschOperator, 1 ),
    'asec'                          : RPNOperator( asecOperator, 1 ),
    'asech'                         : RPNOperator( asechOperator, 1 ),
    'asin'                          : RPNOperator( asinOperator, 1 ),
    'asinh'                         : RPNOperator( asinhOperator, 1 ),
    'atan'                          : RPNOperator( atanOperator, 1 ),
    'atanh'                         : RPNOperator( atanhOperator, 1 ),
    'cos'                           : RPNOperator( cosOperator, 1 ),
    'cosh'                          : RPNOperator( coshOperator, 1 ),
    'cot'                           : RPNOperator( cotOperator, 1 ),
    'coth'                          : RPNOperator( cothOperator, 1 ),
    'csc'                           : RPNOperator( cscOperator, 1 ),
    'csch'                          : RPNOperator( cschOperator, 1 ),
    'sec'                           : RPNOperator( secOperator, 1 ),
    'sech'                          : RPNOperator( sechOperator, 1 ),
    'sin'                           : RPNOperator( sinOperator, 1 ),
    'sinh'                          : RPNOperator( sinhOperator, 1 ),
    'tan'                           : RPNOperator( tanOperator, 1 ),
    'tanh'                          : RPNOperator( tanhOperator, 1 ),

    # internal
    '_dump_aliases'                 : RPNOperator( dumpAliasesOperator, 0 ),
    '_dump_cache'                   : RPNOperator( dumpFunctionCacheOperator, 1 ),
    '_dump_constants'               : RPNOperator( dumpConstantsOperator, 0 ),
    '_dump_conversions'             : RPNOperator( dumpUnitConversionsOperator, 0 ),
    '_dump_operators'               : RPNOperator( dumpOperatorsOperator, 0 ),
    '_dump_prime_cache'             : RPNOperator( dumpPrimeCacheOperator, 1 ),
    '_dump_stats'                   : RPNOperator( dumpStatsOperator, 0 ),
    '_dump_units'                   : RPNOperator( dumpUnitsOperator, 0 ),

    #'antitet'                       : RPNOperator( findTetrahedralNumber, 0 ),
    #'bernfrac'                      : RPNOperator( bernfrac, 1 ),
}

