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

from rpn.rpnBase import getBaseKDigitsOperator, getNonzeroBaseKDigitsOperator

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

from rpn.rpnCombinatorics import countFrobeniusOperator, getArrangementsOperator, getNthBellPolynomialOperator, \
                                 getBinomialOperator, getCombinationsOperator, getCompositionsOperator, \
                                 getDeBruijnSequenceOperator, getIntegerPartitionsOperator, getLahNumberOperator, \
                                 getMultinomialOperator, getNarayanaNumberOperator, getNthAperyNumberOperator, \
                                 getNthBellNumberOperator, getNthBernoulliNumberOperator, \
                                 getNthCatalanNumberOperator, getNthDelannoyNumberOperator, \
                                 getNthMenageNumberOperator, getNthMotzkinNumberOperator, \
                                 getNthMultifactorialOperator, getNthPellNumberOperator, \
                                 getNthSchroederNumberOperator, getNthSchroederHipparchusNumberOperator, \
                                 getNthSylvesterNumberOperator, getPartitionNumberOperator, \
                                 getPartitionsWithLimitOperator, getPermutationsOperator, getStirling1NumberOperator, \
                                 getStirling2NumberOperator

from rpn.rpnComputer import andOperator, convertToCharOperator, convertToDoubleOperator, convertToFloatOperator, \
                            convertToLongOperator, convertToLongLongOperator, convertToQuadLongOperator, \
                            convertToShortOperator, convertToSignedIntOperator, convertToUnsignedCharOperator, \
                            convertToUnsignedIntOperator, convertToUnsignedLongOperator, \
                            convertToUnsignedLongLongOperator, convertToUnsignedQuadLongOperator, \
                            convertToUnsignedShortOperator, getBitCountOperator, getBitwiseAndOperator, \
                            getBitwiseNandOperator, getBitwiseNorOperator, getBitwiseOrOperator, \
                            getBitwiseXnorOperator, getBitwiseXorOperator, getInvertedBitsOperator, \
                            getParityOperator, interpretAsDoubleOperator, interpretAsFloatOperator, \
                            nandOperator, orOperator, norOperator, notOperator, packIntegerOperator, \
                            shiftLeftOperator, shiftRightOperator, unpackIntegerOperator, xnorOperator, \
                            xorOperator

from rpn.rpnConstantUtils import getChampernowneConstant, getCopelandErdosConstant, getFaradayConstant, \
                                 getFineStructureConstant, getMillsConstant, getPlanckAcceleration, \
                                 getPlanckArea, getPlanckCharge, getPlanckCurrent, getPlanckDensity, \
                                 getPlanckEnergy, getPlanckElectricalInductance, getPlanckEnergyDensity, \
                                 getPlanckForce, getPlanckImpedance, getPlanckIntensity, getPlanckLength, \
                                 getPlanckMagneticInductance, getPlanckMass, getPlanckMomentum, getPlanckPower, \
                                 getPlanckTemperature, getPlanckTime, getPlanckViscosity, getPlanckVoltage, \
                                 getPlanckVolume, getPlanckVolumetricFlowRate, getPlasticConstant, \
                                 getRadiationConstant, getRobbinsConstant, getStefanBoltzmannConstant, \
                                 getThueMorseConstant, getVacuumImpedance, getvonKlitzingConstant

from rpn.rpnDateTime import calculateAdventOperator, calculateAscensionThursdayOperator, \
                            calculateAshWednesdayOperator, calculateColumbusDayOperator, \
                            calculateDSTEndOperator, calculateDSTStartOperator, calculateEasterOperator, \
                            calculateElectionDayOperator, calculateFathersDayOperator, calculateGoodFridayOperator, \
                            calculateLaborDayOperator, calculateMartinLutherKingDayOperator, \
                            calculateMemorialDayOperator, calculateMothersDayOperator, \
                            calculateNthWeekdayOfMonthOperator, calculateNthWeekdayOfYearOperator, \
                            calculatePentecostSundayOperator, calculatePresidentsDayOperator, \
                            calculateThanksgivingOperator, convertFromUnixTimeOperator, \
                            convertTimeZoneOperator, convertToDHMSOperator, convertToHMSOperator, \
                            convertToYDHMSOperator, convertToUnixTimeOperator, getChristmasDayOperator, \
                            getDayOperator, getEpiphanyDayOperator, getHourOperator, getIndependenceDayOperator, \
                            getLocalTimeOperator, getMinuteOperator, getMonthOperator, getNewYearsDayOperator, \
                            getNowOperator, getSecondOperator, getTodayOperator, getTomorrowOperator, getUTCOperator, \
                            getVeteransDayOperator, getWeekdayOperator, getWeekdayNameOperator, getYearOperator, \
                            getYesterdayOperator, makeDateTimeOperator, makeJulianTimeOperator, RPNDateTime, \
                            setTimeZoneOperator

from rpn.rpnDice import enumerateDiceOperator, enumerateMultipleDiceOperator, permuteDiceOperator, rollDiceOperator, \
                        rollMultipleDiceOperator, rollSimpleDiceOperator

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

from rpn.rpnInput import parseInputValue, readListFromFileOperator, readNumberFromFileOperator

from rpn.rpnLexicographic import addDigitsOperator, buildNumbersOperator, buildStepNumbersOperator, \
                                 combineDigitsOperator, containsAnyDigitsOperator, containsDigitsOperator, \
                                 containsOnlyDigitsOperator, countDifferentDigitsOperator, countDigitsOperator, \
                                 duplicateDigitsOperator, duplicateNumberOperator, findPalindromeOperator, \
                                 generateSquareDigitChainOperator, getCyclicPermutationsOperator, \
                                 getDigitCountOperator, getDecimalDigitsOperator, getDigitsOperator, \
                                 getErdosPersistenceOperator, getPersistenceOperator, getKPersistenceOperator, \
                                 getLeftDigitsOperator, getLeftTruncationsOperator, getNonzeroDigitsOperator, \
                                 getNthReversalAdditionOperator, getRightDigitsOperator, \
                                 getRightTruncationsOperator, isAutomorphicOperator, isBaseKNarcissisticOperator, \
                                 isBaseKPandigitalOperator, isBaseKSmithNumberOperator, isBouncyOperator, \
                                 isDecreasingOperator, isDigitalPermutationOperator, \
                                 isGeneralizedDudeneyNumberOperator, isHarshadNumberOperator, isIncreasingOperator, \
                                 isKaprekarNumberOperator, isKMorphicOperator, isNarcissisticOperator, \
                                 isOrderKSmithNumberOperator, isPalindromeOperator, isPandigitalOperator, \
                                 isPerfectDigitalInvariantOperator, isPerfectDigitToDigitInvariantOperator, \
                                 isSmithNumberOperator, isStepNumberOperator, isSumProductNumberOperator, \
                                 isTrimorphicOperator, multiplyDigitsOperator, multiplyDigitPowersOperator, \
                                 multiplyNonzeroDigitPowersOperator, multiplyNonzeroDigitsOperator, \
                                 permuteDigitsOperator, replaceDigitsOperator, reverseDigitsOperator, \
                                 rotateDigitsLeftOperator, rotateDigitsRightOperator, showErdosPersistenceOperator, \
                                 showKPersistenceOperator, showPersistenceOperator, sumDigitsOperator

from rpn.rpnList import alternateSignsOperator, alternateSigns2Operator, appendListsOperator, \
                        calculateAntiharmonicMeanOperator, calculateArithmeticMeanOperator, \
                        calculateGeometricMeanOperator, calculateHarmonicMeanOperator, calculatePowerTowerOperator, \
                        calculatePowerTowerRightOperator, calculateRootMeanSquareOperator, collateOperator, \
                        compareListsOperator, countElementsOperator, doesListRepeatOperator, enumerateListOperator, \
                        equalsOneOfOperator, filterMaxOperator, filterMinOperator, filterOnFlagsOperator, \
                        findInListOperator, flattenOperator, getAlternatingSumOperator, getAlternatingSum2Operator, \
                        getAndAllOperator, getCumulativeListDiffsOperator, getCumulativeListMeansOperator, \
                        getCumulativeListProductsOperator, getCumulativeListRatiosOperator, \
                        getCumulativeListSumsOperator, getCumulativeOccurrenceRatiosOperator, getDifferenceOperator, \
                        getGCDOperator, getGCDOfListOperator, getListCombinationsOperator, \
                        getListCombinationsWithRepeatsOperator, getLeftOperator, getListDiffsOperator, \
                        getListPowerSetOperator, getListRatiosOperator, getRightOperator, getIndexOfMaxOperator, \
                        getIndexOfMinOperator, getListElementOperator, getListPermutationsOperator, \
                        getListPermutationsWithRepeatsOperator, getNandAllOperator, getNonzeroesOperator, \
                        getNorAllOperator, getProductOperator, getOccurrencesOperator, getOccurrenceRatiosOperator, \
                        getOrAllOperator, getRandomElementOperator, getReverseOperator, getSliceOperator, \
                        getStandardDeviationOperator, getSublistOperator, getSumOperator, getUniqueElementsOperator, \
                        getZeroesOperator, groupElementsOperator, interleaveOperator, isPalindromeListOperator, \
                        makeIntersectionOperator, makeUnionOperator, permuteListsOperator, reduceListOperator, \
                        shuffleListOperator, sortAscendingOperator, sortDescendingOperator

from rpn.rpnLocation import getGeographicDistanceOperator, getLocationInfoOperator, getTimeZoneOperator, \
                            getTimeZoneOffsetOperator, makeLocationOperator

from rpn.rpnMath import acosOperator, acoshOperator, acotOperator, acothOperator, acscOperator, acschOperator, \
                        addOperator, asecOperator, asechOperator, asinOperator, asinhOperator, atanOperator, \
                        atanhOperator, calculateHypotenuseOperator, calculateNthHyperoperatorOperator, \
                        calculateNthRightHyperoperatorOperator, cosOperator, coshOperator, cotOperator, cothOperator, \
                        cscOperator, cschOperator, cubeOperator, decrementOperator, divideOperator, getAGMOperator, \
                        getAbsoluteValueOperator, getArgumentOperator, getCeilingOperator, getConjugateOperator, \
                        getCubeRootOperator, getCubeSuperRootOperator, getExp10Operator, getExpOperator, \
                        getExpPhiOperator, getFloorOperator, getImaginaryOperator, getLIOperator, \
                        getLambertWOperator, getLargerOperator, getLog10Operator, getLog2Operator, getLogOperator, \
                        getLogXYOperator, getMantissaOperator, getMaximumOperator, getMinimumOperator, \
                        getModuloOperator, getNearestIntOperator, getNegativeOperator, getPolyexpOperator, \
                        getPolylogOperator, getPowerOperator, getPowModOperator, getRealOperator, \
                        getReciprocalOperator, getRootOperator, getSignOperator, getSmallerOperator, \
                        getSquareRootOperator, getSquareSuperRootOperator, getSuperRootOperator, \
                        getSuperRootsOperator, getValueOperator, incrementOperator, isDivisibleOperator, \
                        isEqualOperator, isEvenOperator, isGreaterOperator, isIntegerOperator, isKthPowerOperator, \
                        isLessOperator, isNotEqualOperator, isNotGreaterOperator, isNotLessOperator, \
                        isNotZeroOperator, isOddOperator, isPowerOperator, isSquareOperator, isZeroOperator, \
                        multiplyOperator, roundByDigitsOperator, roundByValueOperator, roundOffOperator, secOperator, \
                        sechOperator, sinOperator, sinhOperator, squareOperator, subtractOperator, tanOperator, \
                        tanhOperator, tetrateOperator, tetrateRightOperator

from rpn.rpnMeasurement import applyNumberValueToUnit, convertToBaseUnitsOperator, convertToDMSOperator, \
                               convertToPrimitiveUnitsOperator, convertUnitsOperator, estimateOperator, \
                               getDimensionsOperator, invertUnitsOperator

from rpn.rpnMeasurementClass import RPNMeasurement

from rpn.rpnModifiers import decrementNestedListLevelOperator, duplicateOperationOperator, duplicateTermOperator, \
                             endOperatorListOperator, getPreviousOperator, incrementNestedListLevelOperator, \
                             startOperatorListOperator, unlistOperator

from rpn.rpnName import getNameOperator, getOrdinalNameOperator

from rpn.rpnNumberTheory import areRelativelyPrimeOperator, calculateAckermannFunctionOperator, \
                                calculateChineseRemainderTheoremOperator, convertFromContinuedFractionOperator, \
                                findNthSumOfCubesOperator, findNthSumOfSquaresOperator, \
                                findSumsOfKNonzeroPowersOperator, findSumsOfKPowersOperator, \
                                generatePolydivisiblesOperator, getAbundanceOperator, getAbundanceRatioOperator, \
                                getAliquotSequenceOperator, getAlternatingHarmonicFractionOperator, \
                                getAltZetaOperator, getBarnesGOperator, getBetaOperator, getCollatzSequenceOperator, \
                                getDigammaOperator, getDigitalRootOperator, \
                                getDivisorCountOperator, getDivisorsOperator, getEulerPhiOperator, \
                                getFrobeniusNumberOperator, getGammaOperator, getGeometricRecurrenceOperator, \
                                getHarmonicFractionOperator, getHarmonicResidueOperator, getHurwitzZetaOperator, \
                                getLCMOperator, getLCMOfListOperator, getLeylandNumberOperator, \
                                getLimitedAliquotSequenceOperator, getLinearRecurrenceOperator, \
                                getLinearRecurrenceWithModuloOperator, getLogGammaOperator, \
                                getNthAlternatingFactorialOperator, getGreedyEgyptianFractionOperator, \
                                getNthBaseKRepunitOperator, getNthCarolNumberOperator, getNthDoubleFactorialOperator, \
                                getNthCalkinWilfOperator, getNthFactorialOperator, getNthFibonacciOperator, \
                                getNthFibonorialOperator, getNthHarmonicNumberOperator, getNthHeptanacciOperator, \
                                getNthHexanacciOperator, getNthHyperfactorialOperator, \
                                getNthJacobsthalNumberOperator, getNthKFibonacciNumberOperator, \
                                getNthKThabitNumberOperator, getNthKThabit2NumberOperator, getNthKyneaNumberOperator, \
                                getNthLeonardoNumberOperator, getNthLinearRecurrenceOperator, \
                                getNthLinearRecurrenceWithModuloOperator, getNthLucasNumberOperator, \
                                getNthMersenneExponentOperator, getNthMersennePrimeOperator, getNthMertenOperator, \
                                getNthMobiusNumberOperator, getNthPadovanNumberOperator, getNthPhitorialOperator, \
                                getNthOctanacciOperator, getNthPascalLineOperator, getNthPentanacciOperator, \
                                getNthPerfectNumberOperator, getNthKPolygorialOperator, getNthSternNumberOperator, \
                                getNthSubfactorialOperator, getNthSuperfactorialOperator, getNthTetranacciOperator, \
                                getNthThabitNumberOperator, getNthThabit2NumberOperator, \
                                getNthThueMorseNumberOperator, getNthTribonacciOperator, getNthZetaZeroOperator, \
                                getPolygammaOperator, getPrimePiOperator, getRadicalOperator, \
                                getSigmaKOperator, getSigmaOperator, getTrigammaOperator, getUnitRootsOperator, \
                                getZetaOperator, interpretAsBaseOperator, interpretAsFractionOperator, \
                                isAbundantOperator, isAchillesNumberOperator, isAntiharmonicOperator, \
                                isCarmichaelNumberOperator, isDeficientOperator, isHarmonicDivisorNumberOperator, \
                                isKHyperperfectOperator, isKPerfectOperator, isKPolydivisibleOperator, \
                                isKSemiprimeOperator, isKSphenicOperator, isPerfectOperator, isPerniciousOperator, \
                                isPolydivisibleOperator, isPowerfulOperator, isPronicOperator, isRoughOperator, \
                                isRuthAaronNumberOperator, isSemiprimeOperator, isSmoothOperator, \
                                isSociableListOperator, isSphenicOperator, isSquareFreeOperator, isUnusualOperator, \
                                makeContinuedFractionOperator, makeEulerBrickOperator, \
                                makePythagoreanQuadrupleOperator, makePythagoreanTripleOperator, \
                                makePythagoreanTriplesOperator, solveFrobeniusOperator

from rpn.rpnPersistence import doesCacheExist, getUserFunctionsFileName, loadConstants, loadResultOperator, \
                               loadUnitConversionMatrix, loadUnitData, openFunctionCache, openPrimeCache

from rpn.rpnPhysics import calculateAccelerationOperator, calculateBlackHoleEntropyOperator, \
                           calculateBlackHoleLifetimeOperator, calculateBlackHoleLuminosityOperator, \
                           calculateBlackHoleMassOperator, calculateBlackHoleRadiusOperator, \
                           calculateBlackHoleSurfaceAreaOperator, calculateBlackHoleSurfaceGravityOperator, \
                           calculateBlackHoleSurfaceTidesOperator, calculateBlackHoleTemperatureOperator, \
                           calculateDistanceOperator, calculateEnergyEquivalenceOperator, \
                           calculateEscapeVelocityOperator, calculateHeatIndexOperator, \
                           calculateHorizonDistanceOperator, calculateKineticEnergyOperator, \
                           calculateMassEquivalenceOperator, calculateOrbitalMassOperator, \
                           calculateOrbitalPeriodOperator, calculateOrbitalRadiusOperator, \
                           calculateOrbitalVelocityOperator, calculateSurfaceGravityOperator, \
                           calculateTidalForceOperator, calculateTimeDilationOperator, \
                           calculateVelocityOperator, calculateWindChillOperator

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
                            getNthGeneralizedHeptagonalNumberOperator, getNthGeneralizedNonagonalNumberOperator, \
                            getNthGeneralizedOctagonalNumberOperator, getNthGeneralizedPentagonalNumberOperator, \
                            getNthHeptagonalHexagonalNumberOperator, getNthHeptagonalNumberOperator, \
                            getNthHeptagonalPentagonalNumberOperator, getNthHeptagonalSquareNumberOperator, \
                            getNthHeptagonalTriangularNumberOperator, getNthHexagonalNumberOperator, \
                            getNthHexagonalPentagonalNumberOperator, getNthHexagonalSquareNumberOperator, \
                            getNthIcosahedralNumberOperator, getNthNonagonalHeptagonalNumberOperator, \
                            getNthNonagonalHexagonalNumberOperator, getNthNonagonalNumberOperator, \
                            getNthNonagonalOctagonalNumberOperator, getNthNonagonalPentagonalNumberOperator, \
                            getNthNonagonalSquareNumberOperator, getNthNonagonalTriangularNumberOperator, \
                            getNthOctagonalHeptagonalNumberOperator, getNthOctagonalHexagonalNumberOperator, \
                            getNthOctagonalNumberOperator, getNthOctagonalPentagonalNumberOperator, \
                            getNthOctagonalSquareNumberOperator, getNthOctagonalTriangularNumberOperator, \
                            getNthTruncatedOctahedralNumberOperator, getNthOctahedralNumberOperator, \
                            getNthPentagonalNumberOperator, getNthPentagonalSquareNumberOperator, \
                            getNthPentagonalTriangularNumberOperator, getNthPentatopeNumberOperator, \
                            getNthPolygonalNumberOperator, getNthPolygonalPyramidalNumberOperator, \
                            getNthPolytopeNumberOperator, getNthPyramidalNumberOperator, \
                            getNthRhombicDodecahedralNumberOperator, getNthSquareTriangularNumberOperator, \
                            getNthStarNumberOperator, getNthStellaOctangulaNumberOperator, \
                            getNthTetrahedralNumberOperator, getNthTruncatedTetrahedralNumberOperator, \
                            getNthTriangularNumberOperator

from rpn.rpnPrimeUtils import countCache, findPrimeOperator, findQuadrupletPrimeOperator, \
                              findQuintupletPrimeOperator, findSextupletPrimeOperator, findTripletPrimeOperator, \
                              findTwinPrimeOperator, getMaxPrime, getNextPrimeOperator, \
                              getNextPrimesOperator, getNextQuadrupletPrimeOperator, getNextQuadrupletPrimesOperator, \
                              getNextQuintupletPrimeOperator, getNextQuintupletPrimesOperator, \
                              getNextSextupletPrimeOperator, getNextSextupletPrimesOperator, \
                              getNextTripletPrimeOperator, getNextTripletPrimesOperator, getNextTwinPrimeOperator, \
                              getNextTwinPrimesOperator, getNthBalancedPrimeOperator, \
                              getNthBalancedPrimeListOperator, getNthCousinPrimeOperator, \
                              getNthCousinPrimeListOperator, getNthDoubleBalancedPrimeOperator, \
                              getNthDoubleBalancedPrimeListOperator, getNthIsolatedPrimeOperator, \
                              getNthOctyPrimeOperator, getNthOctyPrimeListOperator, getNthPolyPrimeOperator, \
                              getNthPrimeOperator, getNthPrimorialOperator, getNthQuadrupleBalancedPrimeOperator, \
                              getNthQuadrupleBalancedPrimeListOperator, getNthQuadrupletPrimeOperator, \
                              getNthQuadrupletPrimeListOperator, getNthQuintupletPrimeOperator, \
                              getNthQuintupletPrimeListOperator, getNthSextupletPrimeOperator, \
                              getNthSextupletPrimeListOperator, getNthSexyPrimeOperator, \
                              getNthSexyPrimeListOperator, getNthSexyQuadrupletOperator, \
                              getNthSexyQuadrupletListOperator, getNthSexyTripletOperator, \
                              getNthSexyTripletListOperator, getNthSophiePrimeOperator, getNthSuperPrimeOperator, \
                              getNthTripleBalancedPrimeOperator, getNthTripleBalancedPrimeListOperator, \
                              getNthTripletPrimeOperator, getNthTripletPrimeListOperator, getNthTwinPrimeOperator, \
                              getNthTwinPrimeListOperator, getSafePrimeOperator, getPreviousPrimeOperator, \
                              getPreviousPrimesOperator, getPrimeRangeOperator, getPrimesOperator, \
                              isCompositeOperator, isPrimeOperator, isStrongPseudoprimeOperator

from rpn.rpnSettings import setCommaOperator, setCommaModeOperator, setDecimalGroupingOperator, setHexModeOperator, \
                            setIdentifyOperator, setIdentifyModeOperator, setInputRadixOperator, \
                            setIntegerGroupingOperator, setLeadingZeroOperator, setLeadingZeroModeOperator, \
                            setAccuracyOperator, setPrecisionOperator, setOctalModeOperator, setOutputRadixOperator, \
                            setTimerOperator, setTimerModeOperator

from rpn.rpnSpecial import describeIntegerOperator, downloadOEISCommentOperator, downloadOEISExtraOperator, \
                           downloadOEISNameOperator, downloadOEISOffsetOperator, downloadOEISSequenceOperator, \
                           findPolynomialOperator, generateRandomUUIDOperator, generateUUIDOperator, \
                           getMultipleRandomsOperator, getRandomIntegerOperator, getRandomIntegersOperator, \
                           getRandomNumberOperator, ifOperator

from rpn.rpnUnitClasses import RPNUnits

from rpn.rpnUtils import addEchoArgumentOperator, abortArgsNeeded, listAndOneArgFunctionEvaluator, \
                         oneArgFunctionEvaluator, twoArgFunctionEvaluator, validateArguments

from rpn.rpnValidator import argValidator, StringValidator

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
                                         function.find( '\n' ) - 1 ] + ' )'

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
    except configparser.NoSectionError:
        return
    except configparser.KeyError:
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

    for item in n:
        value = k.evaluate( item )

        if invert and value == 0:
            yield item
        elif not invert and value != 0:
            yield item


def filterListOperator( n, k ):
    return RPNGenerator( filterList( n, k ) )


def unfilterListOperator( n, k ):
    return RPNGenerator( filterList( n, k, invert=True ) )


#******************************************************************************
#
#  filterRatio
#
#******************************************************************************

def filterRatio( n, k, invert=False ):
    if isinstance( n, mpf ):
        n = [ n ]

    if not isinstance( k, RPNFunction ):
        if invert:
            raise ValueError( '\'unfilter\' expects a function argument' )

        raise ValueError( '\'filter\' expects a function argument' )

    total = len( n )
    filter = 0

    for item in n:
        value = k.evaluate( item )

        if invert and value == 0:
            filter += 1
        elif not invert and value != 0:
            filter += 1

    return fdiv( filter, total )


def filterRatioOperator( n, k ):
    return filterRatio( n, k ) 


def unfilterRatioOperator( n, k ):
    return filterRatio( n, k, invert=True ) 


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

        if invert and value == 0:
            yield item
        elif not invert and value != 0:
            yield item


def filterListByIndexOperator( n, k ):
    return RPNGenerator( filterListByIndex( n, k ) )


def unfilterListByIndexOperator( n, k ):
    return RPNGenerator( filterListByIndex( n, k, invert=True ) )


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
        if isinstance( i, RPNGenerator ):
            yield func.evaluate( *list( i ) )
        elif isinstance( i, list ):
            yield func.evaluate( *i )
        else:
            yield func.evaluate( i )


def forEachOperator( listArg, func ):
    return RPNGenerator( forEach( listArg, func ) )


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


def forEachListOperator( listArg, func ):
    return RPNGenerator( forEachList( listArg, func ) )


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


def dumpOperatorsOperator( ):
    return dumpOperators( )


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
        print( constant + ':  ' + str( g.constantOperators[ constant ].value ) + ' ' +
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
#  dumpFunctionCacheOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def dumpFunctionCacheOperator( name ):
    if not doesCacheExist( name ):
        raise ValueError( 'cache \'' + name + '\' does not exist.' )

    cache = openFunctionCache( name )

    keys = sorted( cache.keys( ) )

    for key in keys:
        print( key, cache[ key ] )

    return len( cache )


#******************************************************************************
#
#  dumpPrimeCacheOperator
#
#******************************************************************************

@oneArgFunctionEvaluator( )
@argValidator( [ StringValidator( ) ] )
def dumpPrimeCacheOperator( name ):
    if name not in g.cursors:
        if not doesCacheExist( name ):
            raise ValueError( 'cache \'' + name + '\' does not exist.' )

        openPrimeCache( name )

    rows = g.cursors[ name ].execute( 'SELECT id, value FROM cache ORDER BY id' ).fetchall( )

    rows.sort( key=lambda x: x[ 0 ] )

    for row in rows:
        print( '{:13} {}'.format( row[ 0 ], row[ 1 ] ) )

    return len( rows )


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
            except ValueError:
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
                    ( isinstance( currentValueList[ -1 ], list ) and
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

    except ZeroDivisionError:
        print( 'rpn:  division by zero' )

        if g.debugMode:
            raise

        return False

    except IndexError:
        print( 'rpn:  index error for list operator at arg ' + format( index ) +
               '.  Are your arguments in the right order?' )

        if g.debugMode:
            raise

        return False

    return True


#******************************************************************************
#
#  printHelpMessageOperator
#
#******************************************************************************

def printHelpMessageOperator( ):
    from rpn.rpnOutput import printHelp
    printHelp( interactive=True )
    return 0


#******************************************************************************
#
#  printHelpTopic
#
#******************************************************************************

def printHelpTopic( n ):
    from rpn.rpnOutput import printHelp

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
def getUserVariableOperator( key ):
    if not isinstance( key, str ):
        raise ValueError( 'variable names must be strings' )

    if key in g.userVariables:
        return parseInputValue( g.userVariables[ key ] )
    else:
        return ''


#******************************************************************************
#
#  setUserVariable
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def setUserVariableOperator( key, value ):
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
def getUserConfigurationOperator( key ):
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
def setUserConfigurationOperator( key, value ):
    g.userConfiguration[ key ] = value
    g.userConfigurationIsDirty = True

    return value


#******************************************************************************
#
#  deleteUserConfiguration
#
#******************************************************************************

@oneArgFunctionEvaluator( )
def deleteUserConfigurationOperator( key ):
    if key not in g.userConfiguration:
        raise ValueError( 'key \'' + key + '\' not found' )

    del g.userConfiguration[ key ]
    g.userConfigurationIsDirty = True

    return key


#******************************************************************************
#
#  dumpUserConfigurationOperator
#
#******************************************************************************

def dumpUserConfigurationOperator( ):
    for i in g.userConfiguration:
        print( i + ':', '"' + g.userConfiguration[ i ] + '"' )

    print( )

    return len( g.userConfiguration )


#******************************************************************************
#
#  dumpUserConfigurationOperator
#
#******************************************************************************

def dumpVariablesOperator( ):
    for i in g.userVariables:
        print( i + ':', '"' + g.userVariables[ i ] + '"' )

    print( )

    return len( g.userVariables )


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

#def filterListOfLists( n, func, invert=False ):
#    if not isinstance( func, RPNFunction ):
#        if invert:
#            raise ValueError( '\'unfilter_lists\' expects a function argument' )
#
#        raise ValueError( '\'filter_lists\' expects a function argument' )
#
#    for i in n:
#        value = func.evaluate( i )
#
#        if ( value != 0 ) != invert:
#            yield i
#
#
#def filterListOfListsOperator( n, func ):
#    return RPNGenerator( filterListOfLists( n, func ) )
#
#
#def unfilterListOfListsOperator( n, func ):
#    return RPNGenerator( filterListOfLists( n, func, invert=True ) )


#******************************************************************************
#
#  evaluateLimitOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateLimitOperator( n, func ):
    return limit( func.evaluate, n, direction=-1, exp=True )


#******************************************************************************
#
#  evaluateDecreasingLimitOperator
#
#******************************************************************************

@twoArgFunctionEvaluator( )
def evaluateDecreasingLimitOperator( n, func ):
    return limit( func.evaluate, n, exp=True )


#******************************************************************************
#
#  evaluateRangedProductOperator
#
#******************************************************************************

def evaluateRangedProductOperator( start, end, func ):
    return nprod( func.evaluate, [ start, end ] )


#******************************************************************************
#
#  evaluateRangedSumOperator
#
#******************************************************************************

def evaluateRangedSumOperator( start, end, func ):
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
    'decreasing_limit',
    'eval0',
    'eval',
    'eval2',
    'eval3',
    'eval_list',
    'filter',
    'filter_by_index',
    'filter_integers',
    'filter_ratio',
    'for_each',
    'for_each_list',
    'function',
    'limit',
    'plot',
    'plot2',
    'plot_complex',
    'ranged_product',
    'ranged_sum',
    'sequence',
    'unfilter',
    'unfilter_by_index',
    'unfilter_ratio',
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
    'add_polynomials'                   : RPNOperator( addPolynomialsOperator, 2 ),
    'discriminant'                      : RPNOperator( getPolynomialDiscriminantOperator, 1 ),
    'eval_polynomial'                   : RPNOperator( evaluatePolynomialOperator, 2 ),
    'multiply_polynomials'              : RPNOperator( multiplyPolynomialsOperator, 2 ),
    'polynomial_power'                  : RPNOperator( exponentiatePolynomialOperator, 2 ),
    'polynomial_product'                : RPNOperator( multiplyPolynomialListOperator, 1 ),
    'polynomial_sum'                    : RPNOperator( sumPolynomialListOperator, 1 ),
    'solve'                             : RPNOperator( solvePolynomialOperator, 1 ),

    # arithmetic
    'antiharmonic_mean'                 : RPNOperator( calculateAntiharmonicMeanOperator, 1 ),
    'equals_one_of'                     : RPNOperator( equalsOneOfOperator, 2 ),
    'gcd'                               : RPNOperator( getGCDOfListOperator, 1 ),
    'geometric_mean'                    : RPNOperator( calculateGeometricMeanOperator, 1 ),
    'harmonic_mean'                     : RPNOperator( calculateHarmonicMeanOperator, 1 ),
    'lcm'                               : RPNOperator( getLCMOfListOperator, 1 ),
    'maximum'                           : RPNOperator( getMaximumOperator, 1 ),
    'mean'                              : RPNOperator( calculateArithmeticMeanOperator, 1 ),
    'minimum'                           : RPNOperator( getMinimumOperator, 1 ),
    'product'                           : RPNOperator( getProductOperator, 1 ),
    'root_mean_square'                  : RPNOperator( calculateRootMeanSquareOperator, 1 ),
    'stddev'                            : RPNOperator( getStandardDeviationOperator, 1 ),
    'sum'                               : RPNOperator( getSumOperator, 1 ),

    # combinatoric
    'count_frobenius'                   : RPNOperator( countFrobeniusOperator, 2 ),
    'multinomial'                       : RPNOperator( getMultinomialOperator, 1 ),

    # conversion
    'convert'                           : RPNOperator( convertUnitsOperator, 2 ),
    'pack'                              : RPNOperator( packIntegerOperator, 2 ),
    'unpack'                            : RPNOperator( unpackIntegerOperator, 2 ),

    # date_time
    'make_datetime'                     : RPNOperator( makeDateTimeOperator, 1 ),
    'make_julian_time'                  : RPNOperator( makeJulianTimeOperator, 1 ),

    # function
    'filter'                            : RPNOperator( filterListOperator, 2 ),
    'filter_by_index'                   : RPNOperator( filterListByIndexOperator, 2 ),
    'filter_ratio'                      : RPNOperator( filterRatioOperator, 2 ),
    'for_each'                          : RPNOperator( forEachOperator, 2 ),
    'for_each_list'                     : RPNOperator( forEachListOperator, 2 ),
    'unfilter'                          : RPNOperator( unfilterListOperator, 2 ),
    'unfilter_by_index'                 : RPNOperator( unfilterListByIndexOperator, 2 ),
    'unfilter_ratio'                    : RPNOperator( unfilterRatioOperator, 2 ),

    # lexicographic
    'combine_digits'                    : RPNOperator( combineDigitsOperator, 1 ),

    # list
    'alternate_signs'                   : RPNOperator( alternateSignsOperator, 1 ),
    'alternate_signs_2'                 : RPNOperator( alternateSigns2Operator, 1 ),
    'alternating_sum'                   : RPNOperator( getAlternatingSumOperator, 1 ),
    'alternating_sum_2'                 : RPNOperator( getAlternatingSum2Operator, 1 ),
    'and_all'                           : RPNOperator( getAndAllOperator, 1 ),
    'append'                            : RPNOperator( appendListsOperator, 2 ),
    'collate'                           : RPNOperator( collateOperator, 1 ),
    'compare_lists'                     : RPNOperator( compareListsOperator, 2 ),
    'count'                             : RPNOperator( countElementsOperator, 1 ),
    'cumulative_diffs'                  : RPNOperator( getCumulativeListDiffsOperator, 1 ),
    'cumulative_means'                  : RPNOperator( getCumulativeListMeansOperator, 1 ),
    'cumulative_products'               : RPNOperator( getCumulativeListProductsOperator, 1 ),
    'cumulative_ratios'                 : RPNOperator( getCumulativeListRatiosOperator, 1 ),
    'cumulative_sums'                   : RPNOperator( getCumulativeListSumsOperator, 1 ),
    'difference'                        : RPNOperator( getDifferenceOperator, 2 ),
    'diffs'                             : RPNOperator( getListDiffsOperator, 1 ),
    'does_list_repeat'                  : RPNOperator( doesListRepeatOperator, 1 ),
    'element'                           : RPNOperator( getListElementOperator, 2 ),
    'enumerate'                         : RPNOperator( enumerateListOperator, 2 ),
    'filter_max'                        : RPNOperator( filterMaxOperator, 2 ),
    'filter_min'                        : RPNOperator( filterMinOperator, 2 ),
    'filter_on_flags'                   : RPNOperator( filterOnFlagsOperator, 2 ),
    'find'                              : RPNOperator( findInListOperator, 2 ),
    'flatten'                           : RPNOperator( flattenOperator, 1 ),
    'get_combinations'                  : RPNOperator( getListCombinationsOperator, 2 ),
    'get_repeat_combinations'           : RPNOperator( getListCombinationsWithRepeatsOperator, 2 ),
    'get_permutations'                  : RPNOperator( getListPermutationsOperator, 2 ),
    'get_repeat_permutations'           : RPNOperator( getListPermutationsWithRepeatsOperator, 2 ),
    'group_elements'                    : RPNOperator( groupElementsOperator, 2 ),
    'interleave'                        : RPNOperator( interleaveOperator, 2 ),
    'intersection'                      : RPNOperator( makeIntersectionOperator, 2 ),
    'is_palindrome_list'                : RPNOperator( isPalindromeListOperator, 1 ),
    'left'                              : RPNOperator( getLeftOperator, 2 ),
    'max_index'                         : RPNOperator( getIndexOfMaxOperator, 1 ),
    'min_index'                         : RPNOperator( getIndexOfMinOperator, 1 ),
    'nand_all'                          : RPNOperator( getNandAllOperator, 1 ),
    'nonzero'                           : RPNOperator( getNonzeroesOperator, 1 ),
    'nor_all'                           : RPNOperator( getNorAllOperator, 1 ),
    'occurrences'                       : RPNOperator( getOccurrencesOperator, 1 ),
    'occurrence_cumulative'             : RPNOperator( getCumulativeOccurrenceRatiosOperator, 1 ),
    'occurrence_ratios'                 : RPNOperator( getOccurrenceRatiosOperator, 1 ),
    'or_all'                            : RPNOperator( getOrAllOperator, 1 ),
    'permute_lists'                     : RPNOperator( permuteListsOperator, 1 ),
    'powerset'                          : RPNOperator( getListPowerSetOperator, 1 ),
    'random_element'                    : RPNOperator( getRandomElementOperator, 1 ),
    'ratios'                            : RPNOperator( getListRatiosOperator, 1 ),
    'reduce'                            : RPNOperator( reduceListOperator, 1 ),
    'reverse'                           : RPNOperator( getReverseOperator, 1 ),
    'right'                             : RPNOperator( getRightOperator, 2 ),
    'shuffle'                           : RPNOperator( shuffleListOperator, 1 ),
    'slice'                             : RPNOperator( getSliceOperator, 3 ),
    'sort'                              : RPNOperator( sortAscendingOperator, 1 ),
    'sort_descending'                   : RPNOperator( sortDescendingOperator, 1 ),
    'sublist'                           : RPNOperator( getSublistOperator, 3 ),
    'union'                             : RPNOperator( makeUnionOperator, 2 ),
    'unique'                            : RPNOperator( getUniqueElementsOperator, 1 ),
    'zero'                              : RPNOperator( getZeroesOperator, 1 ),

    # number_theory
    'base'                              : RPNOperator( interpretAsBaseOperator, 2 ),
    'continued_fraction'                : RPNOperator( convertFromContinuedFractionOperator, 1 ),
    'crt'                               : RPNOperator( calculateChineseRemainderTheoremOperator, 2 ),
    'frobenius'                         : RPNOperator( getFrobeniusNumberOperator, 1 ),
    'geometric_recurrence'              : RPNOperator( getGeometricRecurrenceOperator, 4 ),
    'is_sociable_list'                  : RPNOperator( isSociableListOperator, 1 ),
    'linear_recurrence'                 : RPNOperator( getLinearRecurrenceOperator, 3 ),
    'linear_recurrence_with_modulo'     : RPNOperator( getLinearRecurrenceWithModuloOperator, 4 ),
    'nth_linear_recurrence'             : RPNOperator( getNthLinearRecurrenceOperator, 3 ),
    'nth_linear_recurrence_with_modulo' : RPNOperator( getNthLinearRecurrenceWithModuloOperator, 4 ),
    'solve_frobenius'                   : RPNOperator( solveFrobeniusOperator, 2 ),

    # powers_and_roots
    'power_tower'                       : RPNOperator( calculatePowerTowerOperator, 1 ),
    'power_tower_right'                 : RPNOperator( calculatePowerTowerRightOperator, 1 ),

    # special
    'echo'                              : RPNOperator( addEchoArgumentOperator, 1 ),
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
    'find_polynomial'                   : RPNOperator( findPolynomialOperator, 2 ),
    'solve_cubic'                       : RPNOperator( solveCubicPolynomialOperator, 4 ),
    'solve_quadratic'                   : RPNOperator( solveQuadraticPolynomialOperator, 3 ),
    'solve_quartic'                     : RPNOperator( solveQuarticPolynomialOperator, 5 ),

    # arithmetic
    'abs'                               : RPNOperator( getAbsoluteValueOperator, 1 ),
    'add'                               : RPNOperator( addOperator, 2 ),
    'ceiling'                           : RPNOperator( getCeilingOperator, 1 ),
    'decrement'                         : RPNOperator( decrementOperator, 1 ),
    'divide'                            : RPNOperator( divideOperator, 2 ),
    'floor'                             : RPNOperator( getFloorOperator, 1 ),
    'gcd2'                              : RPNOperator( getGCDOperator, 2 ),
    'increment'                         : RPNOperator( incrementOperator, 1 ),
    'is_divisible'                      : RPNOperator( isDivisibleOperator, 2 ),
    'is_equal'                          : RPNOperator( isEqualOperator, 2 ),
    'is_even'                           : RPNOperator( isEvenOperator, 1 ),
    'is_greater'                        : RPNOperator( isGreaterOperator, 2 ),
    'is_integer'                        : RPNOperator( isIntegerOperator, 1 ),
    'is_kth_power'                      : RPNOperator( isKthPowerOperator, 2 ),
    'is_less'                           : RPNOperator( isLessOperator, 2 ),
    'is_not_equal'                      : RPNOperator( isNotEqualOperator, 2 ),
    'is_not_greater'                    : RPNOperator( isNotGreaterOperator, 2 ),
    'is_not_less'                       : RPNOperator( isNotLessOperator, 2 ),
    'is_not_zero'                       : RPNOperator( isNotZeroOperator, 1 ),
    'is_odd'                            : RPNOperator( isOddOperator, 1 ),
    'is_power_of_k'                     : RPNOperator( isPowerOperator, 2 ),
    'is_square'                         : RPNOperator( isSquareOperator, 1 ),
    'is_zero'                           : RPNOperator( isZeroOperator, 1 ),
    'larger'                            : RPNOperator( getLargerOperator, 2 ),
    'lcm2'                              : RPNOperator( getLCMOperator, 2 ),
    'mantissa'                          : RPNOperator( getMantissaOperator, 1 ),
    'modulo'                            : RPNOperator( getModuloOperator, 2 ),
    'multiply'                          : RPNOperator( multiplyOperator, 2 ),
    'nearest_int'                       : RPNOperator( getNearestIntOperator, 1 ),
    'negative'                          : RPNOperator( getNegativeOperator, 1 ),
    'reciprocal'                        : RPNOperator( getReciprocalOperator, 1 ),
    'round'                             : RPNOperator( roundOffOperator, 1 ),
    'round_by_digits'                   : RPNOperator( roundByDigitsOperator, 2 ),
    'round_by_value'                    : RPNOperator( roundByValueOperator, 2 ),
    'sign'                              : RPNOperator( getSignOperator, 1 ),
    'smaller'                           : RPNOperator( getSmallerOperator, 2 ),
    'subtract'                          : RPNOperator( subtractOperator, 2 ),

    # astronom
    'angular_separation'                : RPNOperator( getAngularSeparationOperator, 4 ),
    'angular_size'                      : RPNOperator( getAngularSizeOperator, 3 ),
    'antitransit_time'                  : RPNOperator( getAntitransitTimeOperator, 3 ),
    'astronomical_dawn'                 : RPNOperator( getNextAstronomicalDawnOperator, 2 ),
    'astronomical_dusk'                 : RPNOperator( getNextAstronomicalDuskOperator, 2 ),
    'autumnal_equinox'                  : RPNOperator( getAutumnalEquinoxOperator, 1 ),
    'dawn'                              : RPNOperator( getNextCivilDawnOperator, 2 ),
    'day_time'                          : RPNOperator( getDayTimeOperator, 2 ),
    'distance_from_earth'               : RPNOperator( getDistanceFromEarthOperator, 2 ),
    'dusk'                              : RPNOperator( getNextCivilDuskOperator, 2 ),
    'eclipse_totality'                  : RPNOperator( getEclipseTotalityOperator, 4 ),
    'moonrise'                          : RPNOperator( getNextMoonRiseOperator, 2 ),
    'moonset'                           : RPNOperator( getNextMoonSetOperator, 2 ),
    'moon_antitransit'                  : RPNOperator( getNextMoonAntitransitOperator, 2 ),
    'moon_phase'                        : RPNOperator( getMoonPhaseOperator, 1 ),
    'moon_transit'                      : RPNOperator( getNextMoonTransitOperator, 2 ),
    'nautical_dawn'                     : RPNOperator( getNextNauticalDawnOperator, 2 ),
    'nautical_dusk'                     : RPNOperator( getNextNauticalDuskOperator, 2 ),
    'next_antitransit'                  : RPNOperator( getNextAntitransitOperator, 3 ),
    'next_first_quarter_moon'           : RPNOperator( getNextFirstQuarterMoonOperator, 1 ),
    'next_full_moon'                    : RPNOperator( getNextFullMoonOperator, 1 ),
    'next_last_quarter_moon'            : RPNOperator( getNextLastQuarterMoonOperator, 1 ),
    'next_new_moon'                     : RPNOperator( getNextNewMoonOperator, 1 ),
    'next_rising'                       : RPNOperator( getNextRisingOperator, 3 ),
    'next_setting'                      : RPNOperator( getNextSettingOperator, 3 ),
    'next_transit'                      : RPNOperator( getNextTransitOperator, 3 ),
    'night_time'                        : RPNOperator( getNightTimeOperator, 2 ),
    'previous_antitransit'              : RPNOperator( getPreviousAntitransitOperator, 3 ),
    'previous_first_quarter_moon'       : RPNOperator( getPreviousFirstQuarterMoonOperator, 1 ),
    'previous_full_moon'                : RPNOperator( getPreviousFullMoonOperator, 1 ),
    'previous_last_quarter_moon'        : RPNOperator( getPreviousLastQuarterMoonOperator, 1 ),
    'previous_new_moon'                 : RPNOperator( getPreviousNewMoonOperator, 1 ),
    'previous_rising'                   : RPNOperator( getPreviousRisingOperator, 3 ),
    'previous_setting'                  : RPNOperator( getPreviousSettingOperator, 3 ),
    'previous_transit'                  : RPNOperator( getPreviousTransitOperator, 3 ),
    'sky_location'                      : RPNOperator( getSkyLocationOperator, 3 ),
    'solar_noon'                        : RPNOperator( getSolarNoonOperator, 2 ),
    'summer_solstice'                   : RPNOperator( getSummerSolsticeOperator, 1 ),
    'sunrise'                           : RPNOperator( getNextSunriseOperator, 2 ),
    'sunset'                            : RPNOperator( getNextSunsetOperator, 2 ),
    'sun_antitransit'                   : RPNOperator( getNextSunAntitransitOperator, 2 ),
    'transit_time'                      : RPNOperator( getTransitTimeOperator, 3 ),
    'vernal_equinox'                    : RPNOperator( getVernalEquinoxOperator, 1 ),
    'winter_solstice'                   : RPNOperator( getWinterSolsticeOperator, 1 ),

    # astronomy - heavenly body operators
    'sun'                               : RPNOperator( lambda: RPNAstronomicalObject( ephem.Sun( ) ), 0 ),
    'mercury'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mercury( ) ), 0 ),
    'venus'                             : RPNOperator( lambda: RPNAstronomicalObject( ephem.Venus( ) ), 0 ),
    'moon'                              : RPNOperator( lambda: RPNAstronomicalObject( ephem.Moon( ) ), 0 ),
    'mars'                              : RPNOperator( lambda: RPNAstronomicalObject( ephem.Mars( ) ), 0 ),
    'jupiter'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Jupiter( ) ), 0 ),
    'saturn'                            : RPNOperator( lambda: RPNAstronomicalObject( ephem.Saturn( ) ), 0 ),
    'uranus'                            : RPNOperator( lambda: RPNAstronomicalObject( ephem.Uranus( ) ), 0 ),
    'neptune'                           : RPNOperator( lambda: RPNAstronomicalObject( ephem.Neptune( ) ), 0 ),
    'pluto'                             : RPNOperator( lambda: RPNAstronomicalObject( ephem.Pluto( ) ), 0 ),

    # bitwise
    'bitwise_and'                       : RPNOperator( getBitwiseAndOperator, 2 ),
    'bitwise_nand'                      : RPNOperator( getBitwiseNandOperator, 2 ),
    'bitwise_nor'                       : RPNOperator( getBitwiseNorOperator, 2 ),
    'bitwise_not'                       : RPNOperator( getInvertedBitsOperator, 1 ),
    'bitwise_or'                        : RPNOperator( getBitwiseOrOperator, 2 ),
    'bitwise_xnor'                      : RPNOperator( getBitwiseXnorOperator, 2 ),
    'bitwise_xor'                       : RPNOperator( getBitwiseXorOperator, 2 ),
    'count_bits'                        : RPNOperator( getBitCountOperator, 1 ),
    'parity'                            : RPNOperator( getParityOperator, 1 ),
    'shift_left'                        : RPNOperator( shiftLeftOperator, 2 ),
    'shift_right'                       : RPNOperator( shiftRightOperator, 2 ),

    # calendar
    'advent'                            : RPNOperator( calculateAdventOperator, 1 ),
    'ascension'                         : RPNOperator( calculateAscensionThursdayOperator, 1 ),
    'ash_wednesday'                     : RPNOperator( calculateAshWednesdayOperator, 1 ),
    'calendar'                          : RPNOperator( generateMonthCalendarOperator, 1 ),
    'christmas'                         : RPNOperator( getChristmasDayOperator, 1 ),
    'columbus_day'                      : RPNOperator( calculateColumbusDayOperator, 1 ),
    'dst_end'                           : RPNOperator( calculateDSTEndOperator, 1 ),
    'dst_start'                         : RPNOperator( calculateDSTStartOperator, 1 ),
    'easter'                            : RPNOperator( calculateEasterOperator, 1 ),
    'election_day'                      : RPNOperator( calculateElectionDayOperator, 1 ),
    'epiphany'                          : RPNOperator( getEpiphanyDayOperator, 1 ),
    'fathers_day'                       : RPNOperator( calculateFathersDayOperator, 1 ),
    'from_bahai'                        : RPNOperator( convertBahaiDateOperator, 3 ),
    'from_ethiopian'                    : RPNOperator( convertEthiopianDateOperator, 3 ),
    'from_french_republican'            : RPNOperator( convertFrenchRepublicanDateOperator, 3 ),
    'from_hebrew'                       : RPNOperator( convertHebrewDateOperator, 3 ),
    'from_indian_civil'                 : RPNOperator( convertIndianCivilDateOperator, 3 ),
    'from_islamic'                      : RPNOperator( convertIslamicDateOperator, 3 ),
    'from_julian'                       : RPNOperator( convertJulianDateOperator, 3 ),
    'from_mayan'                        : RPNOperator( convertMayanDateOperator, 5 ),
    'from_persian'                      : RPNOperator( convertPersianDateOperator, 3 ),
    'good_friday'                       : RPNOperator( calculateGoodFridayOperator, 1 ),
    'independence_day'                  : RPNOperator( getIndependenceDayOperator, 1 ),
    'labor_day'                         : RPNOperator( calculateLaborDayOperator, 1 ),
    'martin_luther_king_day'            : RPNOperator( calculateMartinLutherKingDayOperator, 1 ),
    'memorial_day'                      : RPNOperator( calculateMemorialDayOperator, 1 ),
    'mothers_day'                       : RPNOperator( calculateMothersDayOperator, 1 ),
    'new_years_day'                     : RPNOperator( getNewYearsDayOperator, 1 ),
    'nth_weekday'                       : RPNOperator( calculateNthWeekdayOfMonthOperator, 4 ),
    'nth_weekday_of_year'               : RPNOperator( calculateNthWeekdayOfYearOperator, 3 ),
    'pentecost'                         : RPNOperator( calculatePentecostSundayOperator, 1 ),
    'presidents_day'                    : RPNOperator( calculatePresidentsDayOperator, 1 ),
    'thanksgiving'                      : RPNOperator( calculateThanksgivingOperator, 1 ),
    'to_bahai'                          : RPNOperator( getBahaiCalendarDateOperator, 1 ),
    'to_bahai_name'                     : RPNOperator( getBahaiCalendarDateNameOperator, 1 ),
    'to_ethiopian'                      : RPNOperator( getEthiopianCalendarDateOperator, 1 ),
    'to_ethiopian_name'                 : RPNOperator( getEthiopianCalendarDateNameOperator, 1 ),
    'to_french_republican'              : RPNOperator( getFrenchRepublicanCalendarDateOperator, 1 ),
    'to_french_republican_name'         : RPNOperator( getFrenchRepublicanCalendarDateNameOperator, 1 ),
    'to_hebrew'                         : RPNOperator( getHebrewCalendarDateOperator, 1 ),
    'to_hebrew_name'                    : RPNOperator( getHebrewCalendarDateNameOperator, 1 ),
    'to_indian_civil'                   : RPNOperator( getIndianCivilCalendarDateOperator, 1 ),
    'to_indian_civil_name'              : RPNOperator( getIndianCivilCalendarDateNameOperator, 1 ),
    'to_islamic'                        : RPNOperator( getIslamicCalendarDateOperator, 1 ),
    'to_islamic_name'                   : RPNOperator( getIslamicCalendarDateNameOperator, 1 ),
    'to_iso'                            : RPNOperator( getISODateOperator, 1 ),
    'to_iso_name'                       : RPNOperator( getISODateNameOperator, 1 ),
    'to_julian'                         : RPNOperator( getJulianCalendarDateOperator, 1 ),
    'to_julian_day'                     : RPNOperator( getJulianDayOperator, 1 ),
    'to_lilian_day'                     : RPNOperator( getLilianDayOperator, 1 ),
    'to_mayan'                          : RPNOperator( getMayanCalendarDateOperator, 1 ),
    'to_ordinal_date'                   : RPNOperator( getOrdinalDateOperator, 1 ),
    'to_persian'                        : RPNOperator( getPersianCalendarDateOperator, 1 ),
    'to_persian_name'                   : RPNOperator( getPersianCalendarDateNameOperator, 1 ),
    'veterans_day'                      : RPNOperator( getVeteransDayOperator, 1 ),
    'weekday'                           : RPNOperator( getWeekdayOperator, 1 ),
    'weekday_name'                      : RPNOperator( getWeekdayNameOperator, 1 ),
    'year_calendar'                     : RPNOperator( generateYearCalendarOperator, 1 ),

    # chemistry
    'atomic_number'                     : RPNOperator( getAtomicNumberOperator, 1 ),
    'atomic_symbol'                     : RPNOperator( getAtomicSymbolOperator, 1 ),
    'atomic_weight'                     : RPNOperator( getAtomicWeightOperator, 1 ),
    'element_block'                     : RPNOperator( getElementBlockOperator, 1 ),
    'element_boiling_point'             : RPNOperator( getElementBoilingPointOperator, 1 ),
    'element_density'                   : RPNOperator( getElementDensityOperator, 1 ),
    'element_description'               : RPNOperator( getElementDescriptionOperator, 1 ),
    'element_group'                     : RPNOperator( getElementGroupOperator, 1 ),
    'element_melting_point'             : RPNOperator( getElementMeltingPointOperator, 1 ),
    'element_name'                      : RPNOperator( getElementNameOperator, 1 ),
    'element_occurrence'                : RPNOperator( getElementOccurrenceOperator, 1 ),
    'element_period'                    : RPNOperator( getElementPeriodOperator, 1 ),
    'element_state'                     : RPNOperator( getElementStateOperator, 1 ),
    'molar_mass'                        : RPNOperator( getMolarMassOperator, 1 ),

    # combinatoric
    'arrangements'                      : RPNOperator( getArrangementsOperator, 1 ),
    'binomial'                          : RPNOperator( getBinomialOperator, 2 ),
    'combinations'                      : RPNOperator( getCombinationsOperator, 2 ),
    'compositions'                      : RPNOperator( getCompositionsOperator, 2 ),
    'debruijn_sequence'                 : RPNOperator( getDeBruijnSequenceOperator, 2 ),
    'get_partitions'                    : RPNOperator( getIntegerPartitionsOperator, 1 ),
    'get_partitions_with_limit'         : RPNOperator( getPartitionsWithLimitOperator, 2 ),
    'lah_number'                        : RPNOperator( getLahNumberOperator, 2 ),
    'nth_menage'                        : RPNOperator( getNthMenageNumberOperator, 1 ),
    'multifactorial'                    : RPNOperator( getNthMultifactorialOperator, 2 ),
    'narayana_number'                   : RPNOperator( getNarayanaNumberOperator, 2 ),
    'nth_apery'                         : RPNOperator( getNthAperyNumberOperator, 1 ),
    'nth_bell'                          : RPNOperator( getNthBellNumberOperator, 1 ),
    'nth_bell_polynomial'               : RPNOperator( getNthBellPolynomialOperator, 2 ),
    'nth_bernoulli'                     : RPNOperator( getNthBernoulliNumberOperator, 1 ),
    'nth_catalan'                       : RPNOperator( getNthCatalanNumberOperator, 1 ),
    'nth_delannoy'                      : RPNOperator( getNthDelannoyNumberOperator, 1 ),
    'nth_motzkin'                       : RPNOperator( getNthMotzkinNumberOperator, 1 ),
    'nth_pell'                          : RPNOperator( getNthPellNumberOperator, 1 ),
    'nth_schroeder'                     : RPNOperator( getNthSchroederNumberOperator, 1 ),
    'nth_schroeder_hipparchus'          : RPNOperator( getNthSchroederHipparchusNumberOperator, 1 ),
    'nth_sylvester'                     : RPNOperator( getNthSylvesterNumberOperator, 1 ),
    'partitions'                        : RPNOperator( getPartitionNumberOperator, 1 ),
    'permutations'                      : RPNOperator( getPermutationsOperator, 2 ),
    'stirling1_number'                  : RPNOperator( getStirling1NumberOperator, 2 ),
    'stirling2_number'                  : RPNOperator( getStirling2NumberOperator, 2 ),

    # complex
    'argument'                          : RPNOperator( getArgumentOperator, 1 ),
    'conjugate'                         : RPNOperator( getConjugateOperator, 1 ),
    'imaginary'                         : RPNOperator( getImaginaryOperator, 1 ),
    'real'                              : RPNOperator( getRealOperator, 1 ),

    # conversion
    'char'                              : RPNOperator( convertToCharOperator, 1 ),
    'dhms'                              : RPNOperator( convertToDHMSOperator, 1 ),
    'dms'                               : RPNOperator( convertToDMSOperator, 1 ),
    'double'                            : RPNOperator( convertToDoubleOperator, 1 ),
    'float'                             : RPNOperator( convertToFloatOperator, 1 ),
    'from_unix_time'                    : RPNOperator( convertFromUnixTimeOperator, 1 ),
    'hms'                               : RPNOperator( convertToHMSOperator, 1 ),
    'integer'                           : RPNOperator( convertToSignedIntOperator, 2 ),
    'invert_units'                      : RPNOperator( invertUnitsOperator, 1 ),
    'long'                              : RPNOperator( convertToLongOperator, 1 ),
    'longlong'                          : RPNOperator( convertToLongLongOperator, 1 ),
    'quadlong'                          : RPNOperator( convertToQuadLongOperator, 1 ),
    'short'                             : RPNOperator( convertToShortOperator, 1 ),
    'to_unix_time'                      : RPNOperator( convertToUnixTimeOperator, 1 ),
    'uchar'                             : RPNOperator( convertToUnsignedCharOperator, 1 ),
    'uinteger'                          : RPNOperator( convertToUnsignedIntOperator, 2 ),
    'ulong'                             : RPNOperator( convertToUnsignedLongOperator, 1 ),
    'ulonglong'                         : RPNOperator( convertToUnsignedLongLongOperator, 1 ),
    'undouble'                          : RPNOperator( interpretAsDoubleOperator, 1 ),
    'unfloat'                           : RPNOperator( interpretAsFloatOperator, 1 ),
    'uquadlong'                         : RPNOperator( convertToUnsignedQuadLongOperator, 1 ),
    'ushort'                            : RPNOperator( convertToUnsignedShortOperator, 1 ),
    'ydhms'                             : RPNOperator( convertToYDHMSOperator, 1 ),

    # date_time
    'get_year'                          : RPNOperator( getYearOperator, 1 ),
    'get_month'                         : RPNOperator( getMonthOperator, 1 ),
    'get_day'                           : RPNOperator( getDayOperator, 1 ),
    'get_hour'                          : RPNOperator( getHourOperator, 1 ),
    'get_minute'                        : RPNOperator( getMinuteOperator, 1 ),
    'get_second'                        : RPNOperator( getSecondOperator, 1 ),
    'now'                               : RPNOperator( getNowOperator, 0 ),
    'set_time_zone'                     : RPNOperator( setTimeZoneOperator, 2 ),
    'today'                             : RPNOperator( getTodayOperator, 0 ),
    'tomorrow'                          : RPNOperator( getTomorrowOperator, 0 ),
    'to_local_time'                     : RPNOperator( getLocalTimeOperator, 1 ),
    'to_time_zone'                      : RPNOperator( convertTimeZoneOperator, 2 ),
    'to_utc'                            : RPNOperator( getUTCOperator, 1 ),
    'yesterday'                         : RPNOperator( getYesterdayOperator, 0 ),

    # figurate
    'centered_cube'                     : RPNOperator( getNthCenteredCubeNumberOperator, 1 ),
    'centered_decagonal'                : RPNOperator( getNthCenteredDecagonalNumberOperator, 1 ),
    'centered_dodecahedral'             : RPNOperator( getNthCenteredDodecahedralNumberOperator, 1 ),
    'centered_heptagonal'               : RPNOperator( getNthCenteredHeptagonalNumberOperator, 1 ),
    'centered_hexagonal'                : RPNOperator( getNthCenteredHexagonalNumberOperator, 1 ),
    'centered_icosahedral'              : RPNOperator( getNthCenteredIcosahedralNumberOperator, 1 ),
    'centered_nonagonal'                : RPNOperator( getNthCenteredNonagonalNumberOperator, 1 ),
    'centered_octagonal'                : RPNOperator( getNthCenteredOctagonalNumberOperator, 1 ),
    'centered_octahedral'               : RPNOperator( getNthCenteredOctahedralNumberOperator, 1 ),
    'centered_pentagonal'               : RPNOperator( getNthCenteredPentagonalNumberOperator, 1 ),
    'centered_polygonal'                : RPNOperator( getNthCenteredPolygonalNumberOperator, 2 ),
    'centered_square'                   : RPNOperator( getNthCenteredSquareNumberOperator, 1 ),
    'centered_tetrahedral'              : RPNOperator( getNthCenteredTetrahedralNumberOperator, 1 ),
    'centered_triangular'               : RPNOperator( getNthCenteredTriangularNumberOperator, 1 ),
    'decagonal'                         : RPNOperator( getNthDecagonalNumberOperator, 1 ),
    'decagonal_centered_square'         : RPNOperator( getNthDecagonalCenteredSquareNumberOperator, 1 ),
    'decagonal_heptagonal'              : RPNOperator( getNthDecagonalHeptagonalNumberOperator, 1 ),
    'decagonal_hexagonal'               : RPNOperator( getNthDecagonalHexagonalNumberOperator, 1 ),
    'decagonal_nonagonal'               : RPNOperator( getNthDecagonalNonagonalNumberOperator, 1 ),
    'decagonal_octagonal'               : RPNOperator( getNthDecagonalOctagonalNumberOperator, 1 ),
    'decagonal_pentagonal'              : RPNOperator( getNthDecagonalPentagonalNumberOperator, 1 ),
    'decagonal_triangular'              : RPNOperator( getNthDecagonalTriangularNumberOperator, 1 ),
    'dodecahedral'                      : RPNOperator( getNthDodecahedralNumberOperator, 1 ),
    'generalized_decagonal'             : RPNOperator( getNthGeneralizedDecagonalNumberOperator, 1 ),
    'generalized_heptagonal'            : RPNOperator( getNthGeneralizedHeptagonalNumberOperator, 1 ),
    'generalized_nonagonal'             : RPNOperator( getNthGeneralizedNonagonalNumberOperator, 1 ),
    'generalized_octagonal'             : RPNOperator( getNthGeneralizedOctagonalNumberOperator, 1 ),
    'generalized_pentagonal'            : RPNOperator( getNthGeneralizedPentagonalNumberOperator, 1 ),
    'heptagonal'                        : RPNOperator( getNthHeptagonalNumberOperator, 1 ),
    'heptagonal_hexagonal'              : RPNOperator( getNthHeptagonalHexagonalNumberOperator, 1 ),
    'heptagonal_pentagonal'             : RPNOperator( getNthHeptagonalPentagonalNumberOperator, 1 ),
    'heptagonal_square'                 : RPNOperator( getNthHeptagonalSquareNumberOperator, 1 ),
    'heptagonal_triangular'             : RPNOperator( getNthHeptagonalTriangularNumberOperator, 1 ),
    'hexagonal'                         : RPNOperator( getNthHexagonalNumberOperator, 1 ),
    'hexagonal_pentagonal'              : RPNOperator( getNthHexagonalPentagonalNumberOperator, 1 ),
    'hexagonal_square'                  : RPNOperator( getNthHexagonalSquareNumberOperator, 1 ),
    'icosahedral'                       : RPNOperator( getNthIcosahedralNumberOperator, 1 ),
    'nonagonal'                         : RPNOperator( getNthNonagonalNumberOperator, 1 ),
    'nonagonal_heptagonal'              : RPNOperator( getNthNonagonalHeptagonalNumberOperator, 1 ),
    'nonagonal_hexagonal'               : RPNOperator( getNthNonagonalHexagonalNumberOperator, 1 ),
    'nonagonal_octagonal'               : RPNOperator( getNthNonagonalOctagonalNumberOperator, 1 ),
    'nonagonal_pentagonal'              : RPNOperator( getNthNonagonalPentagonalNumberOperator, 1 ),
    'nonagonal_square'                  : RPNOperator( getNthNonagonalSquareNumberOperator, 1 ),
    'nonagonal_triangular'              : RPNOperator( getNthNonagonalTriangularNumberOperator, 1 ),
    'nth_centered_decagonal'            : RPNOperator( findCenteredDecagonalNumberOperator, 1 ),
    'nth_centered_heptagonal'           : RPNOperator( findCenteredHeptagonalNumberOperator, 1 ),
    'nth_centered_hexagonal'            : RPNOperator( findCenteredHexagonalNumberOperator, 1 ),
    'nth_centered_nonagonal'            : RPNOperator( findCenteredNonagonalNumberOperator, 1 ),
    'nth_centered_octagonal'            : RPNOperator( findCenteredOctagonalNumberOperator, 1 ),
    'nth_centered_pentagonal'           : RPNOperator( findCenteredPentagonalNumberOperator, 1 ),
    'nth_centered_polygonal'            : RPNOperator( findCenteredPolygonalNumberOperator, 2 ),
    'nth_centered_square'               : RPNOperator( findCenteredSquareNumberOperator, 1 ),
    'nth_centered_triangular'           : RPNOperator( findCenteredTriangularNumberOperator, 1 ),
    'nth_decagonal'                     : RPNOperator( findDecagonalNumberOperator, 1 ),
    'nth_heptagonal'                    : RPNOperator( findHeptagonalNumberOperator, 1 ),
    'nth_hexagonal'                     : RPNOperator( findHexagonalNumberOperator, 1 ),
    'nth_nonagonal'                     : RPNOperator( findNonagonalNumberOperator, 1 ),
    'nth_octagonal'                     : RPNOperator( findOctagonalNumberOperator, 1 ),
    'nth_pentagonal'                    : RPNOperator( findPentagonalNumberOperator, 1 ),
    'nth_polygonal'                     : RPNOperator( findPolygonalNumberOperator, 2 ),
    'nth_square'                        : RPNOperator( findSquareNumberOperator, 1 ),
    'nth_triangular'                    : RPNOperator( findTriangularNumberOperator, 1 ),
    'octagonal'                         : RPNOperator( getNthOctagonalNumberOperator, 1 ),
    'octagonal_heptagonal'              : RPNOperator( getNthOctagonalHeptagonalNumberOperator, 1 ),
    'octagonal_hexagonal'               : RPNOperator( getNthOctagonalHexagonalNumberOperator, 1 ),
    'octagonal_pentagonal'              : RPNOperator( getNthOctagonalPentagonalNumberOperator, 1 ),
    'octagonal_square'                  : RPNOperator( getNthOctagonalSquareNumberOperator, 1 ),
    'octagonal_triangular'              : RPNOperator( getNthOctagonalTriangularNumberOperator, 1 ),
    'octahedral'                        : RPNOperator( getNthOctahedralNumberOperator, 1 ),
    'pentagonal'                        : RPNOperator( getNthPentagonalNumberOperator, 1 ),
    'pentagonal_square'                 : RPNOperator( getNthPentagonalSquareNumberOperator, 1 ),
    'pentagonal_triangular'             : RPNOperator( getNthPentagonalTriangularNumberOperator, 1 ),
    'pentatope'                         : RPNOperator( getNthPentatopeNumberOperator, 1 ),
    'polygonal'                         : RPNOperator( getNthPolygonalNumberOperator, 2 ),
    'polygonal_pyramidal'               : RPNOperator( getNthPolygonalPyramidalNumberOperator, 2 ),
    'polytope'                          : RPNOperator( getNthPolytopeNumberOperator, 2 ),
    'pyramidal'                         : RPNOperator( getNthPyramidalNumberOperator, 1 ),
    'rhombic_dodecahedral'              : RPNOperator( getNthRhombicDodecahedralNumberOperator, 1 ),
    'square_triangular'                 : RPNOperator( getNthSquareTriangularNumberOperator, 1 ),
    'star'                              : RPNOperator( getNthStarNumberOperator, 1 ),
    'stella_octangula'                  : RPNOperator( getNthStellaOctangulaNumberOperator, 1 ),
    'tetrahedral'                       : RPNOperator( getNthTetrahedralNumberOperator, 1 ),
    'triangular'                        : RPNOperator( getNthTriangularNumberOperator, 1 ),
    'truncated_octahedral'              : RPNOperator( getNthTruncatedOctahedralNumberOperator, 1 ),
    'truncated_tetrahedral'             : RPNOperator( getNthTruncatedTetrahedralNumberOperator, 1 ),

    # function
    #'break_on'                         : RPNOperator( breakOnCondition, 3 ),
    'decreasing_limit'                  : RPNOperator( evaluateDecreasingLimitOperator, 2 ),
    'eval0'                             : RPNOperator( evaluateFunction0Operator, 1 ),
    'eval'                              : RPNOperator( evaluateFunctionOperator, 2 ),
    'eval2'                             : RPNOperator( evaluateFunction2Operator, 3 ),
    'eval3'                             : RPNOperator( evaluateFunction3Operator, 4 ),
    'eval_list'                         : RPNOperator( evaluateListFunctionOperator, 2 ),
    'filter_integers'                   : RPNOperator( filterIntegersOperator, 2 ),
    'function'                          : RPNOperator( createUserFunctionOperator, 2 ),
    'limit'                             : RPNOperator( evaluateLimitOperator, 2 ),
    'plot'                              : RPNOperator( plotFunctionOperator, 3 ),
    'plot2'                             : RPNOperator( plot2DFunctionOperator, 5 ),
    'plot_complex'                      : RPNOperator( plotComplexFunctionOperator, 5 ),
    'ranged_product'                    : RPNOperator( evaluateRangedProductOperator, 3 ),
    'ranged_sum'                        : RPNOperator( evaluateRangedSumOperator, 3 ),
    'sequence'                          : RPNOperator( getSequenceOperator, 3 ),

    # geography
    'geographic_distance'               : RPNOperator( getGeographicDistanceOperator, 2 ),
    'get_timezone'                      : RPNOperator( getTimeZoneOperator, 1 ),
    'get_timezone_offset'               : RPNOperator( getTimeZoneOffsetOperator, 1 ),
    'lat_long'                          : RPNOperator( makeLocationOperator, 2 ),
    'location_info'                     : RPNOperator( getLocationInfoOperator, 1 ),

    # geometry
    'antiprism_area'                    : RPNOperator( getAntiprismSurfaceAreaOperator, 2 ),
    'antiprism_volume'                  : RPNOperator( getAntiprismVolumeOperator, 2 ),
    'cone_area'                         : RPNOperator( getConeSurfaceAreaOperator, 2 ),
    'cone_volume'                       : RPNOperator( getConeVolumeOperator, 2 ),
    'dodecahedron_area'                 : RPNOperator( getDodecahedronSurfaceAreaOperator, 1 ),
    'dodecahedron_volume'               : RPNOperator( getDodecahedronVolumeOperator, 1 ),
    'hypotenuse'                        : RPNOperator( calculateHypotenuseOperator, 2 ),
    'icosahedron_area'                  : RPNOperator( getIcosahedronSurfaceAreaOperator, 1 ),
    'icosahedron_volume'                : RPNOperator( getIcosahedronVolumeOperator, 1 ),
    'k_sphere_area'                     : RPNOperator( getKSphereSurfaceAreaOperator, 2 ),
    'k_sphere_radius'                   : RPNOperator( getKSphereRadiusOperator, 2 ),
    'k_sphere_volume'                   : RPNOperator( getKSphereVolumeOperator, 2 ),
    'octahedron_area'                   : RPNOperator( getOctahedronSurfaceAreaOperator, 1 ),
    'octahedron_volume'                 : RPNOperator( getOctahedronVolumeOperator, 1 ),
    'polygon_area'                      : RPNOperator( getRegularPolygonAreaOperator, 2 ),
    'prism_area'                        : RPNOperator( getPrismSurfaceAreaOperator, 3 ),
    'prism_volume'                      : RPNOperator( getPrismVolumeOperator, 3 ),
    'sphere_area'                       : RPNOperator( getSphereAreaOperator, 1 ),
    'sphere_radius'                     : RPNOperator( getSphereRadiusOperator, 1 ),
    'sphere_volume'                     : RPNOperator( getSphereVolumeOperator, 1 ),
    'tetrahedron_area'                  : RPNOperator( getTetrahedronSurfaceAreaOperator, 1 ),
    'tetrahedron_volume'                : RPNOperator( getTetrahedronVolumeOperator, 1 ),
    'torus_area'                        : RPNOperator( getTorusSurfaceAreaOperator, 2 ),
    'torus_volume'                      : RPNOperator( getTorusVolumeOperator, 2 ),
    'triangle_area'                     : RPNOperator( getTriangleAreaOperator, 3 ),

    # lexicographic
    'add_digits'                        : RPNOperator( addDigitsOperator, 2 ),
    'build_numbers'                     : RPNOperator( buildNumbersOperator, 1 ),
    'build_step_numbers'                : RPNOperator( buildStepNumbersOperator, 1 ),
    'count_different_digits'            : RPNOperator( countDifferentDigitsOperator, 1 ),
    'count_digits'                      : RPNOperator( countDigitsOperator, 2 ),
    'cyclic_permutations'               : RPNOperator( getCyclicPermutationsOperator, 1 ),
    'digits'                            : RPNOperator( getDigitCountOperator, 1 ),
    'duplicate_digits'                  : RPNOperator( duplicateDigitsOperator, 2 ),
    'duplicate_number'                  : RPNOperator( duplicateNumberOperator, 2 ),
    'erdos_persistence'                 : RPNOperator( getErdosPersistenceOperator, 1 ),
    'find_palindrome'                   : RPNOperator( findPalindromeOperator, 2 ),
    'get_base_k_digits'                 : RPNOperator( getBaseKDigitsOperator, 2 ),
    'get_digits'                        : RPNOperator( getDigitsOperator, 1 ),
    'get_decimal_digits'                : RPNOperator( getDecimalDigitsOperator, 2 ),
    'get_left_digits'                   : RPNOperator( getLeftDigitsOperator, 2 ),
    'get_left_truncations'              : RPNOperator( getLeftTruncationsOperator, 1 ),
    'get_nonzero_base_k_digits'         : RPNOperator( getNonzeroBaseKDigitsOperator, 2 ),
    'get_nonzero_digits'                : RPNOperator( getNonzeroDigitsOperator, 1 ),
    'get_right_digits'                  : RPNOperator( getRightDigitsOperator, 2 ),
    'get_right_truncations'             : RPNOperator( getRightTruncationsOperator, 1 ),
    'has_any_digits'                    : RPNOperator( containsAnyDigitsOperator, 2 ),
    'has_digits'                        : RPNOperator( containsDigitsOperator, 2 ),
    'has_only_digits'                   : RPNOperator( containsOnlyDigitsOperator, 2 ),
    'is_automorphic'                    : RPNOperator( isAutomorphicOperator, 1 ),
    'is_base_k_pandigital'              : RPNOperator( isBaseKPandigitalOperator, 2 ),
    'is_base_k_smith_number'            : RPNOperator( isBaseKSmithNumberOperator, 2 ),
    'is_bouncy'                         : RPNOperator( isBouncyOperator, 1 ),
    'is_decreasing'                     : RPNOperator( isDecreasingOperator, 1 ),
    'is_digital_palindrome'             : RPNOperator( isPalindromeOperator, 1 ),
    'is_digital_permutation'            : RPNOperator( isDigitalPermutationOperator, 2 ),
    'is_generalized_dudeney'            : RPNOperator( isGeneralizedDudeneyNumberOperator, 2 ),
    'is_harshad'                        : RPNOperator( isHarshadNumberOperator, 2 ),
    'is_increasing'                     : RPNOperator( isIncreasingOperator, 1 ),
    'is_kaprekar'                       : RPNOperator( isKaprekarNumberOperator, 1 ),
    'is_k_morphic'                      : RPNOperator( isKMorphicOperator, 2 ),
    'is_k_narcissistic'                 : RPNOperator( isBaseKNarcissisticOperator, 2 ),
    'is_narcissistic'                   : RPNOperator( isNarcissisticOperator, 1 ),
    'is_order_k_smith_number'           : RPNOperator( isOrderKSmithNumberOperator, 2 ),
    'is_pandigital'                     : RPNOperator( isPandigitalOperator, 1 ),
    'is_pddi'                           : RPNOperator( isPerfectDigitToDigitInvariantOperator, 2 ),
    'is_pdi'                            : RPNOperator( isPerfectDigitalInvariantOperator, 1 ),
    'is_smith_number'                   : RPNOperator( isSmithNumberOperator, 1 ),
    'is_step_number'                    : RPNOperator( isStepNumberOperator, 1 ),
    'is_sum_product'                    : RPNOperator( isSumProductNumberOperator, 2 ),
    'is_trimorphic'                     : RPNOperator( isTrimorphicOperator, 1 ),
    'k_persistence'                     : RPNOperator( getKPersistenceOperator, 2 ),
    'multiply_digits'                   : RPNOperator( multiplyDigitsOperator, 1 ),
    'multiply_digit_powers'             : RPNOperator( multiplyDigitPowersOperator, 2 ),
    'multiply_nonzero_digits'           : RPNOperator( multiplyNonzeroDigitsOperator, 1 ),
    'multiply_nonzero_digit_powers'     : RPNOperator( multiplyNonzeroDigitPowersOperator, 2 ),
    'permute_digits'                    : RPNOperator( permuteDigitsOperator, 1 ),
    'persistence'                       : RPNOperator( getPersistenceOperator, 1 ),
    'replace_digits'                    : RPNOperator( replaceDigitsOperator, 3 ),
    'reverse_digits'                    : RPNOperator( reverseDigitsOperator, 1 ),
    'rotate_digits_left'                : RPNOperator( rotateDigitsLeftOperator, 2 ),
    'rotate_digits_right'               : RPNOperator( rotateDigitsRightOperator, 2 ),
    'show_erdos_persistence'            : RPNOperator( showErdosPersistenceOperator, 1 ),
    'show_k_persistence'                : RPNOperator( showKPersistenceOperator, 2 ),
    'show_persistence'                  : RPNOperator( showPersistenceOperator, 1 ),
    'square_digit_chain'                : RPNOperator( generateSquareDigitChainOperator, 1 ),
    'sum_digits'                        : RPNOperator( sumDigitsOperator, 1 ),

    # list
    'exponential_range'                 : RPNOperator( createExponentialRangeOperator, 3 ),
    'geometric_range'                   : RPNOperator( createGeometricRangeOperator, 3 ),
    'interval_range'                    : RPNOperator( createIntervalRangeOperator, 3 ),
    'range'                             : RPNOperator( createRangeOperator, 2 ),
    'sized_range'                       : RPNOperator( createSizedRangeOperator, 3 ),

    # logarithms
    'lambertw'                          : RPNOperator( getLambertWOperator, 1 ),
    'li'                                : RPNOperator( getLIOperator, 1 ),
    'log'                               : RPNOperator( getLogOperator, 1 ),
    'log10'                             : RPNOperator( getLog10Operator, 1 ),
    'log2'                              : RPNOperator( getLog2Operator, 1 ),
    'logxy'                             : RPNOperator( getLogXYOperator, 2 ),
    'polyexp'                           : RPNOperator( getPolyexpOperator, 2 ),
    'polylog'                           : RPNOperator( getPolylogOperator, 2 ),

    # logical
    'and'                               : RPNOperator( andOperator, 2 ),
    'nand'                              : RPNOperator( nandOperator, 2 ),
    'nor'                               : RPNOperator( norOperator, 2 ),
    'not'                               : RPNOperator( notOperator, 1 ),
    'or'                                : RPNOperator( orOperator, 2 ),
    'xnor'                              : RPNOperator( xnorOperator, 2 ),
    'xor'                               : RPNOperator( xorOperator, 2 ),

    # number_theory
    'abundance'                         : RPNOperator( getAbundanceOperator, 1 ),
    'abundance_ratio'                   : RPNOperator( getAbundanceRatioOperator, 1 ),
    'ackermann_number'                  : RPNOperator( calculateAckermannFunctionOperator, 2 ),
    'aliquot'                           : RPNOperator( getAliquotSequenceOperator, 2 ),
    'aliquot_limit'                     : RPNOperator( getLimitedAliquotSequenceOperator, 2 ),
    'alternating_factorial'             : RPNOperator( getNthAlternatingFactorialOperator, 1 ),
    'alternating_harmonic_fraction'     : RPNOperator( getAlternatingHarmonicFractionOperator, 1 ),
    'barnesg'                           : RPNOperator( getBarnesGOperator, 1 ),
    'beta'                              : RPNOperator( getBetaOperator, 2 ),
    'calkin_wilf'                       : RPNOperator( getNthCalkinWilfOperator, 1 ),
    'collatz'                           : RPNOperator( getCollatzSequenceOperator, 2 ),
    'count_divisors'                    : RPNOperator( getDivisorCountOperator, 1 ),
    'digamma'                           : RPNOperator( getDigammaOperator, 1 ),
    'digital_root'                      : RPNOperator( getDigitalRootOperator, 1 ),
    'divisors'                          : RPNOperator( getDivisorsOperator, 1 ),
    'double_factorial'                  : RPNOperator( getNthDoubleFactorialOperator, 1 ),
    'egyptian_fractions'                : RPNOperator( getGreedyEgyptianFractionOperator, 2 ),
    'eta'                               : RPNOperator( getAltZetaOperator, 1 ),
    'euler_brick'                       : RPNOperator( makeEulerBrickOperator, 3 ),
    'euler_phi'                         : RPNOperator( getEulerPhiOperator, 1 ),
    'factor'                            : RPNOperator( getFactorsOperator, 1 ),
    'factorial'                         : RPNOperator( getNthFactorialOperator, 1 ),
    'fibonacci'                         : RPNOperator( getNthFibonacciOperator, 1 ),
    'fibonorial'                        : RPNOperator( getNthFibonorialOperator, 1 ),
    'find_sum_of_cubes'                 : RPNOperator( findNthSumOfCubesOperator, 1 ),
    'find_sum_of_squares'               : RPNOperator( findNthSumOfSquaresOperator, 1 ),
    'fraction'                          : RPNOperator( interpretAsFractionOperator, 2 ),
    'gamma'                             : RPNOperator( getGammaOperator, 1 ),
    'generate_polydivisibles'           : RPNOperator( generatePolydivisiblesOperator, 1 ),
    'harmonic_fraction'                 : RPNOperator( getHarmonicFractionOperator, 1 ),
    'harmonic_residue'                  : RPNOperator( getHarmonicResidueOperator, 1 ),
    'heptanacci'                        : RPNOperator( getNthHeptanacciOperator, 1 ),
    'hexanacci'                         : RPNOperator( getNthHexanacciOperator, 1 ),
    'hurwitz_zeta'                      : RPNOperator( getHurwitzZetaOperator, 2 ),
    'hyperfactorial'                    : RPNOperator( getNthHyperfactorialOperator, 1 ),
    'is_abundant'                       : RPNOperator( isAbundantOperator, 1 ),
    'is_achilles'                       : RPNOperator( isAchillesNumberOperator, 1 ),
    'is_antiharmonic'                   : RPNOperator( isAntiharmonicOperator, 1 ),
    'is_carmichael'                     : RPNOperator( isCarmichaelNumberOperator, 1 ),
    'is_composite'                      : RPNOperator( isCompositeOperator, 1 ),
    'is_deficient'                      : RPNOperator( isDeficientOperator, 1 ),
    'is_harmonic_divisor_number'        : RPNOperator( isHarmonicDivisorNumberOperator, 1 ),
    'is_k_hyperperfect'                 : RPNOperator( isKHyperperfectOperator, 2 ),
    'is_k_perfect'                      : RPNOperator( isKPerfectOperator, 2 ),
    'is_k_polydivisible'                : RPNOperator( isKPolydivisibleOperator, 2 ),
    'is_k_semiprime'                    : RPNOperator( isKSemiprimeOperator, 2 ),
    'is_k_sphenic'                      : RPNOperator( isKSphenicOperator, 2 ),
    'is_perfect'                        : RPNOperator( isPerfectOperator, 1 ),
    'is_pernicious'                     : RPNOperator( isPerniciousOperator, 1 ),
    'is_polydivisible'                  : RPNOperator( isPolydivisibleOperator, 1 ),
    'is_powerful'                       : RPNOperator( isPowerfulOperator, 1 ),
    'is_prime'                          : RPNOperator( isPrimeOperator, 1 ),
    'is_pronic'                         : RPNOperator( isPronicOperator, 1 ),
    'is_rough'                          : RPNOperator( isRoughOperator, 2 ),
    'is_ruth_aaron'                     : RPNOperator( isRuthAaronNumberOperator, 1 ),
    'is_semiprime'                      : RPNOperator( isSemiprimeOperator, 1 ),
    'is_smooth'                         : RPNOperator( isSmoothOperator, 2 ),
    'is_sphenic'                        : RPNOperator( isSphenicOperator, 1 ),
    'is_squarefree'                     : RPNOperator( isSquareFreeOperator, 1 ),
    'is_strong_pseudoprime'             : RPNOperator( isStrongPseudoprimeOperator, 2 ),
    'is_unusual'                        : RPNOperator( isUnusualOperator, 1 ),
    'k_fibonacci'                       : RPNOperator( getNthKFibonacciNumberOperator, 2 ),
    'leyland_number'                    : RPNOperator( getLeylandNumberOperator, 2 ),
    'log_gamma'                         : RPNOperator( getLogGammaOperator, 1 ),
    'lucas'                             : RPNOperator( getNthLucasNumberOperator, 1 ),
    'make_continued_fraction'           : RPNOperator( makeContinuedFractionOperator, 2 ),
    'make_pyth_3'                       : RPNOperator( makePythagoreanTripleOperator, 2 ),
    'make_pyth_4'                       : RPNOperator( makePythagoreanQuadrupleOperator, 2 ),
    'nth_carol'                         : RPNOperator( getNthCarolNumberOperator, 1 ),
    'nth_harmonic_number'               : RPNOperator( getNthHarmonicNumberOperator, 1 ),
    'nth_jacobsthal'                    : RPNOperator( getNthJacobsthalNumberOperator, 1 ),
    'nth_k_thabit'                      : RPNOperator( getNthKThabitNumberOperator, 2 ),
    'nth_k_thabit_2'                    : RPNOperator( getNthKThabit2NumberOperator, 2 ),
    'nth_kynea'                         : RPNOperator( getNthKyneaNumberOperator, 1 ),
    'nth_leonardo'                      : RPNOperator( getNthLeonardoNumberOperator, 1 ),
    'nth_mersenne_exponent'             : RPNOperator( getNthMersenneExponentOperator, 1 ),
    'nth_mersenne_prime'                : RPNOperator( getNthMersennePrimeOperator, 1 ),
    'nth_merten'                        : RPNOperator( getNthMertenOperator, 1 ),
    'nth_mobius'                        : RPNOperator( getNthMobiusNumberOperator, 1 ),
    'nth_padovan'                       : RPNOperator( getNthPadovanNumberOperator, 1 ),
    'nth_perfect_number'                : RPNOperator( getNthPerfectNumberOperator, 1 ),
    'nth_stern'                         : RPNOperator( getNthSternNumberOperator, 1 ),
    'nth_thabit'                        : RPNOperator( getNthThabitNumberOperator, 1 ),
    'nth_thabit_2'                      : RPNOperator( getNthThabit2NumberOperator, 1 ),
    'nth_thue_morse'                    : RPNOperator( getNthThueMorseNumberOperator, 1 ),
    'octanacci'                         : RPNOperator( getNthOctanacciOperator, 1 ),
    'pascal_triangle'                   : RPNOperator( getNthPascalLineOperator, 1 ),
    'pentanacci'                        : RPNOperator( getNthPentanacciOperator, 1 ),
    'phitorial'                         : RPNOperator( getNthPhitorialOperator, 1 ),
    'polygamma'                         : RPNOperator( getPolygammaOperator, 2 ),
    'polygorial'                        : RPNOperator( getNthKPolygorialOperator, 2 ),
    'primorial'                         : RPNOperator( getNthPrimorialOperator, 1 ),
    'pythagorean_triples'               : RPNOperator( makePythagoreanTriplesOperator, 1 ),
    'radical'                           : RPNOperator( getRadicalOperator, 1 ),
    'relatively_prime'                  : RPNOperator( areRelativelyPrimeOperator, 2 ),
    'repunit'                           : RPNOperator( getNthBaseKRepunitOperator, 2 ),
    'reversal_addition'                 : RPNOperator( getNthReversalAdditionOperator, 2 ),
    'sigma'                             : RPNOperator( getSigmaOperator, 1 ),
    'sigma_k'                           : RPNOperator( getSigmaKOperator, 2 ),
    'subfactorial'                      : RPNOperator( getNthSubfactorialOperator, 1 ),
    'sums_of_k_powers'                  : RPNOperator( findSumsOfKPowersOperator, 3 ),
    'sums_of_k_nonzero_powers'          : RPNOperator( findSumsOfKNonzeroPowersOperator, 3 ),
    'superfactorial'                    : RPNOperator( getNthSuperfactorialOperator, 1 ),
    'tetranacci'                        : RPNOperator( getNthTetranacciOperator, 1 ),
    'tribonacci'                        : RPNOperator( getNthTribonacciOperator, 1 ),
    'trigamma'                          : RPNOperator( getTrigammaOperator, 1 ),
    'unit_roots'                        : RPNOperator( getUnitRootsOperator, 1 ),
    'zeta'                              : RPNOperator( getZetaOperator, 1 ),
    'zeta_zero'                         : RPNOperator( getNthZetaZeroOperator, 1 ),

    # physics
    'acceleration'                      : RPNOperator( calculateAccelerationOperator, 2 ),
    'black_hole_entropy'                : RPNOperator( calculateBlackHoleEntropyOperator, 1 ),
    'black_hole_lifetime'               : RPNOperator( calculateBlackHoleLifetimeOperator, 1 ),
    'black_hole_luminosity'             : RPNOperator( calculateBlackHoleLuminosityOperator, 1 ),
    'black_hole_mass'                   : RPNOperator( calculateBlackHoleMassOperator, 1 ),
    'black_hole_radius'                 : RPNOperator( calculateBlackHoleRadiusOperator, 1 ),
    'black_hole_surface_area'           : RPNOperator( calculateBlackHoleSurfaceAreaOperator, 1 ),
    'black_hole_surface_gravity'        : RPNOperator( calculateBlackHoleSurfaceGravityOperator, 1 ),
    'black_hole_surface_tides'          : RPNOperator( calculateBlackHoleSurfaceTidesOperator, 1 ),
    'black_hole_temperature'            : RPNOperator( calculateBlackHoleTemperatureOperator, 1 ),
    'distance'                          : RPNOperator( calculateDistanceOperator, 2 ),
    'energy_equivalence'                : RPNOperator( calculateEnergyEquivalenceOperator, 1 ),
    'escape_velocity'                   : RPNOperator( calculateEscapeVelocityOperator, 2 ),
    'heat_index'                        : RPNOperator( calculateHeatIndexOperator, 2 ),
    'horizon_distance'                  : RPNOperator( calculateHorizonDistanceOperator, 2 ),
    'kinetic_energy'                    : RPNOperator( calculateKineticEnergyOperator, 2 ),
    'mass_equivalence'                  : RPNOperator( calculateMassEquivalenceOperator, 1 ),
    'orbital_mass'                      : RPNOperator( calculateOrbitalMassOperator, 2 ),
    'orbital_period'                    : RPNOperator( calculateOrbitalPeriodOperator, 2 ),
    'orbital_radius'                    : RPNOperator( calculateOrbitalRadiusOperator, 2 ),
    'orbital_velocity'                  : RPNOperator( calculateOrbitalVelocityOperator, 2 ),
    'surface_gravity'                   : RPNOperator( calculateSurfaceGravityOperator, 2 ),
    'tidal_force'                       : RPNOperator( calculateTidalForceOperator, 3 ),
    'time_dilation'                     : RPNOperator( calculateTimeDilationOperator, 1 ),
    'velocity'                          : RPNOperator( calculateVelocityOperator, 2 ),
    'wind_chill'                        : RPNOperator( calculateWindChillOperator, 2 ),

    # powers_and_roots
    'agm'                               : RPNOperator( getAGMOperator, 2 ),
    'cube'                              : RPNOperator( cubeOperator, 1 ),
    'cube_root'                         : RPNOperator( getCubeRootOperator, 1 ),
    'cube_super_root'                   : RPNOperator( getCubeSuperRootOperator, 1 ),
    'exp'                               : RPNOperator( getExpOperator, 1 ),
    'exp10'                             : RPNOperator( getExp10Operator, 1 ),
    'expphi'                            : RPNOperator( getExpPhiOperator, 1 ),
    'hyperoperator'                     : RPNOperator( calculateNthHyperoperatorOperator, 3 ),
    'hyperoperator_right'               : RPNOperator( calculateNthRightHyperoperatorOperator, 3 ),
    'power'                             : RPNOperator( getPowerOperator, 2 ),
    'powmod'                            : RPNOperator( getPowModOperator, 3 ),
    'root'                              : RPNOperator( getRootOperator, 2 ),
    'square'                            : RPNOperator( squareOperator, 1 ),
    'square_root'                       : RPNOperator( getSquareRootOperator, 1 ),
    'square_super_root'                 : RPNOperator( getSquareSuperRootOperator, 1 ),
    'super_root'                        : RPNOperator( getSuperRootOperator, 2 ),
    'super_roots'                       : RPNOperator( getSuperRootsOperator, 2 ),
    'tetrate'                           : RPNOperator( tetrateOperator, 2 ),
    'tetrate_right'                     : RPNOperator( tetrateRightOperator, 2 ),

    # prime_number
    'balanced_prime'                    : RPNOperator( getNthBalancedPrimeOperator, 1 ),
    'balanced_primes'                   : RPNOperator( getNthBalancedPrimeListOperator, 1 ),
    'cousin_prime'                      : RPNOperator( getNthCousinPrimeOperator, 1 ),
    'cousin_primes'                     : RPNOperator( getNthCousinPrimeListOperator, 1 ),
    'double_balanced_prime'             : RPNOperator( getNthDoubleBalancedPrimeOperator, 1 ),
    'double_balanced_primes'            : RPNOperator( getNthDoubleBalancedPrimeListOperator, 1 ),
    'isolated_prime'                    : RPNOperator( getNthIsolatedPrimeOperator, 1 ),
    'next_prime'                        : RPNOperator( getNextPrimeOperator, 1 ),
    'next_primes'                       : RPNOperator( getNextPrimesOperator, 2 ),
    'next_quadruplet_prime'             : RPNOperator( getNextQuadrupletPrimeOperator, 1 ),
    'next_quadruplet_primes'            : RPNOperator( getNextQuadrupletPrimesOperator, 1 ),
    'next_quintuplet_prime'             : RPNOperator( getNextQuintupletPrimeOperator, 1 ),
    'next_quintuplet_primes'            : RPNOperator( getNextQuintupletPrimesOperator, 1 ),
    'next_sextuplet_prime'              : RPNOperator( getNextSextupletPrimeOperator, 1 ),
    'next_sextuplet_primes'             : RPNOperator( getNextSextupletPrimesOperator, 1 ),
    'next_triplet_prime'                : RPNOperator( getNextTripletPrimeOperator, 1 ),
    'next_triplet_primes'               : RPNOperator( getNextTripletPrimesOperator, 1 ),
    'next_twin_prime'                   : RPNOperator( getNextTwinPrimeOperator, 1 ),
    'next_twin_primes'                  : RPNOperator( getNextTwinPrimesOperator, 1 ),
    'nth_prime'                         : RPNOperator( findPrimeOperator, 1 ),
    'nth_quadruplet_prime'              : RPNOperator( findQuadrupletPrimeOperator, 1 ),
    'nth_quintuplet_prime'              : RPNOperator( findQuintupletPrimeOperator, 1 ),
    'nth_sextuplet_prime'               : RPNOperator( findSextupletPrimeOperator, 1 ),
    'nth_triplet_prime'                 : RPNOperator( findTripletPrimeOperator, 1 ),
    'nth_twin_prime'                    : RPNOperator( findTwinPrimeOperator, 1 ),
    'octy_prime'                        : RPNOperator( getNthOctyPrimeOperator, 1 ),
    'octy_primes'                       : RPNOperator( getNthOctyPrimeListOperator, 1 ),
    'polyprime'                         : RPNOperator( getNthPolyPrimeOperator, 2 ),
    'previous_prime'                    : RPNOperator( getPreviousPrimeOperator, 1 ),
    'previous_primes'                   : RPNOperator( getPreviousPrimesOperator, 2 ),
    'prime'                             : RPNOperator( getNthPrimeOperator, 1 ),
    'primes'                            : RPNOperator( getPrimesOperator, 2 ),
    'prime_pi'                          : RPNOperator( getPrimePiOperator, 1 ),
    'prime_range'                       : RPNOperator( getPrimeRangeOperator, 2 ),
    'quadruplet_prime'                  : RPNOperator( getNthQuadrupletPrimeOperator, 1 ),
    'quadruplet_primes'                 : RPNOperator( getNthQuadrupletPrimeListOperator, 1 ),
    'quadruple_balanced_prime'          : RPNOperator( getNthQuadrupleBalancedPrimeOperator, 1 ),
    'quadruple_balanced_primes'         : RPNOperator( getNthQuadrupleBalancedPrimeListOperator, 1 ),
    'quintuplet_prime'                  : RPNOperator( getNthQuintupletPrimeOperator, 1 ),
    'quintuplet_primes'                 : RPNOperator( getNthQuintupletPrimeListOperator, 1 ),
    'safe_prime'                        : RPNOperator( getSafePrimeOperator, 1 ),
    'sextuplet_prime'                   : RPNOperator( getNthSextupletPrimeOperator, 1 ),
    'sextuplet_primes'                  : RPNOperator( getNthSextupletPrimeListOperator, 1 ),
    'sexy_prime'                        : RPNOperator( getNthSexyPrimeOperator, 1 ),
    'sexy_primes'                       : RPNOperator( getNthSexyPrimeListOperator, 1 ),
    'sexy_quadruplet'                   : RPNOperator( getNthSexyQuadrupletOperator, 1 ),
    'sexy_quadruplets'                  : RPNOperator( getNthSexyQuadrupletListOperator, 1 ),
    'sexy_triplet'                      : RPNOperator( getNthSexyTripletOperator, 1 ),
    'sexy_triplets'                     : RPNOperator( getNthSexyTripletListOperator, 1 ),
    'sophie_prime'                      : RPNOperator( getNthSophiePrimeOperator, 1 ),
    'super_prime'                       : RPNOperator( getNthSuperPrimeOperator, 1 ),
    'triplet_prime'                     : RPNOperator( getNthTripletPrimeOperator, 1 ),
    'triplet_primes'                    : RPNOperator( getNthTripletPrimeListOperator, 1 ),
    'triple_balanced_prime'             : RPNOperator( getNthTripleBalancedPrimeOperator, 1 ),
    'triple_balanced_primes'            : RPNOperator( getNthTripleBalancedPrimeListOperator, 1 ),
    'twin_prime'                        : RPNOperator( getNthTwinPrimeOperator, 1 ),
    'twin_primes'                       : RPNOperator( getNthTwinPrimeListOperator, 1 ),

    # settings
    'accuracy'                          : RPNOperator( setAccuracyOperator, 1 ),
    'comma'                             : RPNOperator( setCommaOperator, 1 ),
    'comma_mode'                        : RPNOperator( setCommaModeOperator, 0 ),
    'decimal_grouping'                  : RPNOperator( setDecimalGroupingOperator, 1 ),
    'hex_mode'                          : RPNOperator( setHexModeOperator, 0 ),
    'identify'                          : RPNOperator( setIdentifyOperator, 1 ),
    'identify_mode'                     : RPNOperator( setIdentifyModeOperator, 0 ),
    'input_radix'                       : RPNOperator( setInputRadixOperator, 1 ),
    'integer_grouping'                  : RPNOperator( setIntegerGroupingOperator, 1 ),
    'leading_zero'                      : RPNOperator( setLeadingZeroOperator, 1 ),
    'leading_zero_mode'                 : RPNOperator( setLeadingZeroModeOperator, 0 ),
    'octal_mode'                        : RPNOperator( setOctalModeOperator, 0 ),
    'output_radix'                      : RPNOperator( setOutputRadixOperator, 1 ),
    'precision'                         : RPNOperator( setPrecisionOperator, 1 ),
    'timer'                             : RPNOperator( setTimerOperator, 1 ),
    'timer_mode'                        : RPNOperator( setTimerModeOperator, 0 ),

    # special
    'base_units'                        : RPNOperator( convertToBaseUnitsOperator, 1 ),
    'delete_config'                     : RPNOperator( deleteUserConfigurationOperator, 1 ),
    'describe'                          : RPNOperator( describeIntegerOperator, 1 ),
    'dimensions'                        : RPNOperator( getDimensionsOperator, 1 ),
    'dump_config'                       : RPNOperator( dumpUserConfigurationOperator, 0 ),
    'dump_variables'                    : RPNOperator( dumpVariablesOperator, 0 ),
    'enumerate_dice'                    : RPNOperator( enumerateDiceOperator, 1 ),
    'enumerate_dice_'                   : RPNOperator( enumerateMultipleDiceOperator, 2 ),
    'estimate'                          : RPNOperator( estimateOperator, 1 ),
    'help'                              : RPNOperator( printHelpMessageOperator, 0 ),
    'get_config'                        : RPNOperator( getUserConfigurationOperator, 1 ),
    'get_variable'                      : RPNOperator( getUserVariableOperator, 1 ),
    'if'                                : RPNOperator( ifOperator, 3 ),
    'list_from_file'                    : RPNOperator( readListFromFileOperator, 1 ),
    'name'                              : RPNOperator( getNameOperator, 1 ),
    'number_from_file'                  : RPNOperator( readNumberFromFileOperator, 1 ),
    'oeis'                              : RPNOperator( downloadOEISSequenceOperator, 1 ),
    'oeis_comment'                      : RPNOperator( downloadOEISCommentOperator, 1 ),
    'oeis_ex'                           : RPNOperator( downloadOEISExtraOperator, 1 ),
    'oeis_name'                         : RPNOperator( downloadOEISNameOperator, 1 ),
    'oeis_offset'                       : RPNOperator( downloadOEISOffsetOperator, 1 ),
    'ordinal_name'                      : RPNOperator( getOrdinalNameOperator, 1 ),
    'permute_dice'                      : RPNOperator( permuteDiceOperator, 1 ),
    'primitive_units'                   : RPNOperator( convertToPrimitiveUnitsOperator, 1 ),
    'random'                            : RPNOperator( getRandomNumberOperator, 0 ),
    'random_'                           : RPNOperator( getMultipleRandomsOperator, 1 ),
    'random_integer'                    : RPNOperator( getRandomIntegerOperator, 1 ),
    'random_integers'                   : RPNOperator( getRandomIntegersOperator, 2 ),
    'result'                            : RPNOperator( loadResultOperator, 0 ),
    'roll_dice'                         : RPNOperator( rollDiceOperator, 1 ),
    'roll_simple_dice'                  : RPNOperator( rollSimpleDiceOperator, 2 ),
    'roll_dice_'                        : RPNOperator( rollMultipleDiceOperator, 2 ),
    'set_config'                        : RPNOperator( setUserConfigurationOperator, 2 ),
    'set_variable'                      : RPNOperator( setUserVariableOperator, 2 ),

    #'topics' doesn't need to be handled here, see rpn.py, search for 'topics'

    'uuid'                              : RPNOperator( generateUUIDOperator, 0 ),
    'uuid_random'                       : RPNOperator( generateRandomUUIDOperator, 0 ),
    'value'                             : RPNOperator( getValueOperator, 1 ),

    # trigonometry
    'acos'                              : RPNOperator( acosOperator, 1 ),
    'acosh'                             : RPNOperator( acoshOperator, 1 ),
    'acot'                              : RPNOperator( acotOperator, 1 ),
    'acoth'                             : RPNOperator( acothOperator, 1 ),
    'acsc'                              : RPNOperator( acscOperator, 1 ),
    'acsch'                             : RPNOperator( acschOperator, 1 ),
    'asec'                              : RPNOperator( asecOperator, 1 ),
    'asech'                             : RPNOperator( asechOperator, 1 ),
    'asin'                              : RPNOperator( asinOperator, 1 ),
    'asinh'                             : RPNOperator( asinhOperator, 1 ),
    'atan'                              : RPNOperator( atanOperator, 1 ),
    'atanh'                             : RPNOperator( atanhOperator, 1 ),
    'cos'                               : RPNOperator( cosOperator, 1 ),
    'cosh'                              : RPNOperator( coshOperator, 1 ),
    'cot'                               : RPNOperator( cotOperator, 1 ),
    'coth'                              : RPNOperator( cothOperator, 1 ),
    'csc'                               : RPNOperator( cscOperator, 1 ),
    'csch'                              : RPNOperator( cschOperator, 1 ),
    'sec'                               : RPNOperator( secOperator, 1 ),
    'sech'                              : RPNOperator( sechOperator, 1 ),
    'sin'                               : RPNOperator( sinOperator, 1 ),
    'sinh'                              : RPNOperator( sinhOperator, 1 ),
    'tan'                               : RPNOperator( tanOperator, 1 ),
    'tanh'                              : RPNOperator( tanhOperator, 1 ),

    # internal
    '_dump_aliases'                     : RPNOperator( dumpAliasesOperator, 0 ),
    '_dump_cache'                       : RPNOperator( dumpFunctionCacheOperator, 1 ),
    '_dump_constants'                   : RPNOperator( dumpConstantsOperator, 0 ),
    '_dump_conversions'                 : RPNOperator( dumpUnitConversionsOperator, 0 ),
    '_dump_operators'                   : RPNOperator( dumpOperatorsOperator, 0 ),
    '_dump_prime_cache'                 : RPNOperator( dumpPrimeCacheOperator, 1 ),
    '_dump_stats'                       : RPNOperator( dumpStatsOperator, 0 ),
    '_dump_units'                       : RPNOperator( dumpUnitsOperator, 0 ),

    #'antitet'                          : RPNOperator( findTetrahedralNumber, 0 ),
    #'bernfrac'                         : RPNOperator( bernfrac, 1 ),
}

