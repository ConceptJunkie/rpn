#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnDeclarations.py
# //
# //  RPN command-line calculator constant and class declarations
# //  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import collections
import itertools

from mpmath import *

from fractions import Fraction

from rpnUtils import loadUnitConversionMatrix
from rpnEstimates import *

import rpnGlobals as g


# //******************************************************************************
# //
# //  constants
# //
# //******************************************************************************

PROGRAM_NAME = 'rpn'
PROGRAM_DESCRIPTION = 'RPN command-line calculator'


# //******************************************************************************
# //
# //  specialUnitConversionMatrix
# //
# //  This is for units that can't be converted with a simple multiplication
# //  factor.
# //
# //  Plus, I'm not going to do the transitive thing here, so it's necessary
# //  to explicitly state the conversions for all permutations.  That bugs me.
# //
# //  I would have included this table in makeUnits.py, but pickle doesn't
# //  work on lambdas, which is, to me, very non-Pythonic.   I could also
# //  save the expressions as strings and use eval, but that seems very
# //  non-Pythonic, too.
# //
# //  ( first unit, second unit, conversion function )
# //
# //******************************************************************************

specialUnitConversionMatrix = {
    ( 'celsius',               'delisle' )                         : lambda c: fmul( fsub( 100, c ), fdiv( 3, 2 ) ),
    ( 'celsius',               'degrees_newton' )                  : lambda c: fmul( c, fdiv( 33, 100 ) ),
    ( 'celsius',               'fahrenheit' )                      : lambda c: fadd( fmul( c, fdiv( 9, 5 ) ), 32 ),
    ( 'celsius',               'kelvin' )                          : lambda c: fadd( c, mpf( '273.15' ) ),
    ( 'celsius',               'rankine' )                         : lambda c: fmul( fadd( c, mpf( '273.15' ) ), fdiv( 9, 5 ) ),
    ( 'celsius',               'reaumur' )                         : lambda c: fmul( c, fdiv( 4, 5 ) ),
    ( 'celsius',               'romer' )                           : lambda c: fadd( fmul( c, fdiv( 21, 40 ) ), mpf( '7.5' ) ),

    ( 'delisle',               'celsius' )                         : lambda d: fsub( 100, fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle',               'degrees_newton' )                  : lambda d: fsub( 33, fmul( d, fdiv( 11, 50 ) ) ),
    ( 'delisle',               'fahrenheit' )                      : lambda d: fsub( 212, fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle',               'kelvin' )                          : lambda d: fsub( mpf( '373.15' ), fmul( fdiv( 2, 3 ), d ) ),
    ( 'delisle',               'rankine' )                         : lambda d: fsub( mpf( '671.67' ), fmul( fdiv( 6, 5 ), d ) ),
    ( 'delisle',               'reaumur' )                         : lambda d: fsub( 80, fmul( d, fdiv( 8, 15 ) ) ),
    ( 'delisle',               'romer' )                           : lambda d: fsub( 60, fmul( d, fdiv( 7, 20 ) ) ),

    ( 'degrees_newton',        'celsius' )                         : lambda n: fmul( n, fdiv( 100, 33 ) ),
    ( 'degrees_newton',        'delisle' )                         : lambda n: fmul( fsub( 33, n ), fdiv( 50, 11 ) ),
    ( 'degrees_newton',        'fahrenheit' )                      : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), 32 ),
    ( 'degrees_newton',        'kelvin' )                          : lambda n: fadd( fmul( n, fdiv( 100, 33 ) ), mpf( '273.15' ) ),
    ( 'degrees_newton',        'rankine' )                         : lambda n: fadd( fmul( n, fdiv( 60, 11 ) ), mpf( '491.67' ) ),
    ( 'degrees_newton',        'reaumur' )                         : lambda n: fmul( n, fdiv( 80, 33 ) ),
    ( 'degrees_newton',        'romer' )                           : lambda n: fadd( fmul( n, fdiv( 35, 22 ) ), mpf( 7.5 ) ),

    ( 'fahrenheit',            'celsius' )                         : lambda f: fmul( fsub( f, 32 ), fdiv( 5, 9 ) ),
    ( 'fahrenheit',            'degrees_newton' )                  : lambda f: fmul( fsub( f, 32 ), fdiv( 11, 60 ) ),
    ( 'fahrenheit',            'delisle' )                         : lambda f: fmul( fsub( 212, f ), fdiv( 5, 6 ) ),
    ( 'fahrenheit',            'kelvin' )                          : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 5, 9 ) ), mpf( '273.15' ) ),
    ( 'fahrenheit',            'rankine' )                         : lambda f: fadd( f, mpf( '459.67' ) ),
    ( 'fahrenheit',            'reaumur' )                         : lambda f: fmul( fsub( f, 32 ), fdiv( 4, 9 ) ),
    ( 'fahrenheit',            'romer' )                           : lambda f: fadd( fmul( fsub( f, 32 ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'kelvin',                'celsius' )                         : lambda k: fsub( k, mpf( '273.15' ) ),
    ( 'kelvin',                'degrees_newton' )                  : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 33, 100 ) ),
    ( 'kelvin',                'delisle' )                         : lambda k: fmul( fsub( mpf( '373.15' ), k ), fdiv( 3, 2 ) ),
    ( 'kelvin',                'fahrenheit' )                      : lambda k: fsub( fmul( k, fdiv( 9, 5 ) ), mpf( '459.67' ) ),
    ( 'kelvin',                'rankine' )                         : lambda k: fmul( k, fdiv( 9, 5 ) ),
    ( 'kelvin',                'reaumur' )                         : lambda k: fmul( fsub( k, mpf( '273.15' ) ), fdiv( 4, 5 ) ),
    ( 'kelvin',                'romer' )                           : lambda k: fadd( fmul( fsub( k, mpf( '273.15' ) ), fdiv( 21, 40 ) ), mpf( 7.5 ) ),

    ( 'rankine',               'celsius' )                         : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 5, 9 ) ),
    ( 'rankine',               'degrees_newton' )                  : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 11, 60 ) ),
    ( 'rankine',               'delisle' )                         : lambda r: fmul( fsub( mpf( '671.67' ), r ), fdiv( 5, 6 ) ),
    ( 'rankine',               'fahrenheit' )                      : lambda r: fsub( r, mpf( '459.67' ) ),
    ( 'rankine',               'kelvin' )                          : lambda r: fmul( r, fdiv( 5, 9 ) ),
    ( 'rankine',               'reaumur' )                         : lambda r: fmul( fsub( r, mpf( '491.67' ) ), fdiv( 4, 9 ) ),
    ( 'rankine',               'romer' )                           : lambda r: fadd( fmul( fsub( r, mpf( '491.67' ) ), fdiv( 7, 24 ) ), mpf( '7.5' ) ),

    ( 'reaumur',               'celsius' )                         : lambda re: fmul( re, fdiv( 5, 4 ) ),
    ( 'reaumur',               'degrees_newton' )                  : lambda re: fmul( re, fdiv( 33, 80 ) ),
    ( 'reaumur',               'delisle' )                         : lambda re: fmul( fsub( 80, re ), fdiv( 15, 8 ) ),
    ( 'reaumur',               'fahrenheit' )                      : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), 32 ),
    ( 'reaumur',               'kelvin' )                          : lambda re: fadd( fmul( re, fdiv( 5, 4 ) ), mpf( '273.15' ) ),
    ( 'reaumur',               'rankine' )                         : lambda re: fadd( fmul( re, fdiv( 9, 4 ) ), mpf( '491.67' ) ),
    ( 'reaumur',               'romer' )                           : lambda re: fadd( fmul( re, fdiv( 21, 32 ) ), mpf( 7.5 ) ),

    ( 'romer',                 'celsius' )                         : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ),
    ( 'romer',                 'degrees_newton' )                  : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 22, 35 ) ),
    ( 'romer',                 'delisle' )                         : lambda ro: fmul( fsub( 60, ro ), fdiv( 20, 7 ) ),
    ( 'romer',                 'fahrenheit' )                      : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), 32 ),
    ( 'romer',                 'kelvin' )                          : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 40, 21 ) ), mpf( '273.15' ) ),
    ( 'romer',                 'rankine' )                         : lambda ro: fadd( fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 24, 7 ) ), mpf( '491.67' ) ),
    ( 'romer',                 'reaumur' )                         : lambda ro: fmul( fsub( ro, mpf( '7.5' ) ), fdiv( 32, 21 ) ),

    ( 'dBm',                   'watt' )                            : lambda dBm: power( 10, fdiv( fsub( dBm, 30 ), 10 ) ),
    ( 'watt',                  'dBm' )                             : lambda W: fmul( log10( fmul( W, 1000 ) ), 10 ),
}


# //******************************************************************************
# //
# //  operatorAliases
# //
# //******************************************************************************

operatorAliases = {
    'divides'       : 'isdivisible',
    '|'             : 'isdivisible',
    '!!'            : 'doublefac',
    '!'             : 'factorial',
    '!='            : 'not_equal',
    '%'             : 'modulo',
    '*'             : 'multiply',
    '<'             : 'less',
    '<='            : 'not_greater',
    '=='            : 'equal',
    '>'             : 'greater',
    '>='            : 'not_less',
    '**'            : 'power',
    '***'           : 'tetrate',
    '+'             : 'add',
    '-'             : 'subtract',
    '-c'            : 'comma_mode',
    '-i'            : 'identify_mode',
    '-o'            : 'octal_mode',
    '-t'            : 'timer_mode',
    '-x'            : 'hex_mode',
    '-z'            : 'leading_zero_mode',
    '/'             : 'divide',
    '//'            : 'root',
    '1/x'           : 'reciprocal',
    '?'             : 'help',
    'apr'           : 'april',
    'arcosine'      : 'acos',
    'arcsine'       : 'asin',
    'arctangent'    : 'atan',
    'arg'           : 'argument',
    'args'          : 'arguments',
    'arithmean'     : 'mean',
    'ashwed'        : 'ash_wednesday',
    'ashwednesday'  : 'ash_wednesday',
    'ash_wed'       : 'ash_wednesday',
    'aug'           : 'august',
    'average'       : 'mean',
    'avg'           : 'mean',
    'bal'           : 'balanced',
    'bal?'          : 'balanced?',
    'bal_'          : 'balanced_',
    'bits'          : 'countbits',
    'cal'           : 'calendar',
    'cbrt'          : 'root3',
    'cc'            : 'cubic_centimeter',
    'ccube'         : 'centeredcube',
    'cdec'          : 'cdecagonal',
    'cdec?'         : 'cdecagonal?',
    'ceil'          : 'ceiling',
    'champ'         : 'champernowne',
    'chept'         : 'cheptagonal',
    'chept?'        : 'cheptagonal?',
    'chex'          : 'chexagonal',
    'chex?'         : 'chexagonal?',
    'click'         : 'kilometer',
    'cnon'          : 'cnonagonal',
    'cnon?'         : 'cnonagonal?',
    'coct'          : 'coctagonal',
    'coct?'         : 'coctagonal?',
    'conj'          : 'conjugate',
    'cosine'        : 'cos',
    'cousin'        : 'cousinprime',
    'cousin?'       : 'cousinprime?',
    'cousin_'       : 'cousinprime_',
    'cpent'         : 'cpentagonal',
    'cpent?'        : 'cpentagonal?',
    'cpoly'         : 'cpolygonal',
    'cpoly?'        : 'cpolygonal?',
    'ctri'          : 'ctriangular',
    'ctri?'         : 'ctriangular?',
    'cuberoot'      : 'root3',
    'cube_root'     : 'root3',
    'dec'           : 'december',
    'deca'          : 'decagonal',
    'deca?'         : 'decagonal?',
    'divcount'      : 'countdiv',
    'f!'            : 'fibonorial',
    'fac'           : 'factorial',
    'fac2'          : 'doublefac',
    'feb'           : 'february',
    'fermi'         : 'femtometer',
    'fib'           : 'fibonacci',
    'frac'          : 'fraction',
    'fri'           : 'friday',
    'fromunix'      : 'fromunixtime',
    'gammaflux'     : 'nanotesla',
    'gamma_flux'    : 'nanotesla',
    'gemmho'        : 'micromho',
    'geomrange'     : 'georange',
    'gigohm'        : 'gigaohm',
    'harm'          : 'harmonic',
    'hept'          : 'heptagonal',
    'hept?'         : 'heptagonal?',
    'hex'           : 'hexagonal',
    'hex?'          : 'hexagonal?',
    'hyper4'        : 'tetrate',
    'inf'           : 'infinity',
    'im'            : 'imaginary',
    'int'           : 'long',
    'int16'         : 'short',
    'int32'         : 'long',
    'int64'         : 'longlong',
    'int8'          : 'char',
    'intersect'     : 'intersection',
    'inv'           : 'reciprocal',
    'isdiv'         : 'isdivisible',
    'isoday'        : 'iso_day',
    'issqr'         : 'issquare',
    'jan'           : 'january',
    'jul'           : 'july',
    'julianday'     : 'julian_day',
    'jun'           : 'june',
    'klick'         : 'kilometer',
    'left'          : 'shiftleft',
    'len'           : 'count',
    'length'        : 'count',
    'linear'        : 'linearrecur',
    'log'           : 'ln',
    'makeiso'       : 'makeisotime',
    'makejulian'    : 'makejuliantime',
    'makepyth'      : 'makepyth3',
    'mar'           : 'march',
    'math'          : 'arithmetic',
    'maxint'        : 'maxlong',
    'maxint128'     : 'maxquadlong',
    'maxint16'      : 'maxshort',
    'maxint32'      : 'maxlong',
    'maxint64'      : 'maxlonglong',
    'maxint8'       : 'maxchar',
    'maxuint'       : 'maxulong',
    'maxuint128'    : 'maxuquadlong',
    'maxuint16'     : 'maxushort',
    'maxuint32'     : 'maxulong',
    'maxuint64'     : 'maxulonglong',
    'maxuint8'      : 'maxuchar',
    'mcg'           : 'microgram',
    'megalerg'      : 'megaerg',
    'megaohm'       : 'megohm',
    'metre'         : 'meter',
    'metres'        : 'meter',
    'minint'        : 'minlong',
    'minint128'     : 'minquadlong',
    'minint16'      : 'minshort',
    'minint32'      : 'minlong',
    'minint64'      : 'minlonglong',
    'minint8'       : 'minchar',
    'minuint'       : 'minulong',
    'minuint128'    : 'minuquadlong',
    'minuint16'     : 'minushort',
    'minuint32'     : 'minulong',
    'minuint64'     : 'minulonglong',
    'minuint8'      : 'minuchar',
    'mod'           : 'modulo',
    'mon'           : 'monday',
    'mult'          : 'multiply',
    'neg'           : 'negative',
    'ninf'          : 'negative_infinity',
    'non'           : 'nonagonal',
    'non?'          : 'nonagonal?',
    'nonasq'        : 'nonasquare',
    'nonzeroes'     : 'nonzero',
    'nov'           : 'november',
    'nthday'        : 'nthweekday',
    'nthdayofyear'  : 'nthweekdayofyear',
    'oct'           : 'october',
    'octa'          : 'octagonal',
    'octa?'         : 'octagonal?',
    'p!'            : 'primorial',
    'pent'          : 'pentagonal',
    'pent?'         : 'pentagonal?',
    'poly'          : 'polygonal',
    'poly?'         : 'polygonal?',
    'polyeval'      : 'polyval',
    'prev'          : 'previous',
    'prod'          : 'product',
    'puff'          : 'picofarad',
    'pyr'           : 'pyramid',
    'quad'          : 'quadprime',
    'quad?'         : 'quadprime?',
    'quad_'         : 'quadprime_',
    'quint'         : 'quintprime',
    'quint?'        : 'quintprime?',
    'quint_'        : 'quintprime_',
    'rand'          : 'random',
    're'            : 'real',
    'right'         : 'shiftright',
    'safe'          : 'safeprime',
    'safe?'         : 'safeprime?',
    'sat'           : 'saturday',
    'sep'           : 'september',
    'sext'          : 'sextprime',
    'sext?'         : 'sextprime?',
    'sext_'         : 'sextprime_',
    'sexy'          : 'sexyprime',
    'sexy3'         : 'sexytriplet',
    'sexy3?'        : 'sexytriplet?',
    'sexy3_'        : 'sexytriplet_',
    'sexy4'         : 'sexyquad',
    'sexy4?'        : 'sexyquad?',
    'sexy4_'        : 'sexyquad_',
    'sexy?'         : 'sexyprime?',
    'sexy_'         : 'sexyprime',
    'sigma'         : 'microsecond',
    'sigmas'        : 'microsecond',
    'sine'          : 'sin',
    'sophie'        : 'sophieprime',
    'sophie?'       : 'sophieprime?',
    'split'         : 'unpack',
    'sqr'           : 'square',
    'sqrt'          : 'root2',
    'sqrtri'        : 'squaretri',
    'squareroot'    : 'root2',
    'square_root'   : 'root2',
    'sun'           : 'sunday',
    'syl'           : 'sylvester',
    'tangent'       : 'tan',
    'thur'          : 'thursday',
    'thurs'         : 'thursday',
    'tounix'        : 'tounixtime',
    'tri'           : 'triangular',
    'tri?'          : 'triangular?',
    'triarea'       : 'trianglearea',
    'trib'          : 'tribonacci',
    'triplet'       : 'tripletprime',
    'triplet?'      : 'tripletprime?',
    'triplet_'      : 'tripletprime_',
    'trisqr'        : 'squaretri',
    'tue'           : 'tuesday',
    'tues'          : 'tuesday',
    'twin'          : 'twinprime',
    'twin?'         : 'twinprime?',
    'twin_'         : 'twinprime_',
    'uint'          : 'ulong',
    'uint16'        : 'ushort',
    'uint32'        : 'ulong',
    'uint64'        : 'ulonglong',
    'uint8'         : 'uchar',
    'units'         : 'unit_types',
    'unsigned'      : 'uinteger',
    'wed'           : 'wednesday',
    'woodall'       : 'riesel',
    'yearcal'       : 'year_calendar',
    'yearcalendar'  : 'year_calendar',
    'zeroes'        : 'zero',
    'zero_mode'     : 'leading_zero_mode',
    '^'             : 'power',
    '~'             : 'not',
}


# //******************************************************************************
# //
# //  combineUnits
# //
# //  Combine units2 into units1
# //
# //******************************************************************************

def combineUnits( units1, units2 ):
    if not g.unitConversionMatrix:
        loadUnitConversionMatrix( )

    newUnits = Units( units1 )

    factor = mpmathify( 1 )

    for unit2 in units2:
        if unit2 in newUnits:
            newUnits[ unit2 ] += units2[ unit2 ]
        else:
            for unit1 in units1:
                if unit1 == unit2:
                    newUnits[ unit2 ] += units2[ unit2 ]
                    break
                elif getUnitType( unit1 ) == getUnitType( unit2 ):
                    factor = fdiv( factor, pow( mpmathify( g.unitConversionMatrix[ ( unit1, unit2 ) ] ), units2[ unit2 ] ) )
                    newUnits[ unit1 ] += units2[ unit2 ]
                    break
            else:
                newUnits[ unit2 ] = units2[ unit2 ]

    return factor, newUnits


# //******************************************************************************
# //
# //  class Units
# //
# //******************************************************************************

class Units( collections.Counter ):
    def __init__( self, *arg, **kw ):
        if ( len( arg ) == 1 ):
            if isinstance( arg[ 0 ], str ):
                self.update( self.parseUnitString( arg[ 0 ] ) )
            elif isinstance( arg[ 0 ], ( list, tuple ) ):
                for item in arg[ 0 ]:
                    self.update( item )  # for Counter, update( ) adds, not replaces
            elif isinstance( arg[ 0 ], ( Units, dict ) ):
                self.update( arg[ 0 ] )
        else:
            super( Units, self ).__init__( *arg, **kw )

    def invert( self ):
        for unit in self:
            self[ unit ] = -( self[ unit ] )

        return self

    def getUnitTypes( self ):
        types = Units( )

        for unit in self:
            if unit in g.basicUnitTypes:
                unitType = unit
            else:
                if unit not in g.unitOperators:
                    raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

                unitType = g.unitOperators[ unit ].unitType

            types[ unitType ] += self[ unit ]

        return types

    def simplify( self ):
        result = Units( )

        for unit in self:
            if unit not in g.unitOperators:
                raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

            simpleUnits = Units( g.unitOperators[ unit ].representation )

            exponent = self.get( unit )

            if exponent != 1:   # handle exponent
                for unit2 in simpleUnits:
                    simpleUnits[ unit2 ] *= exponent

            result.update( simpleUnits )

        return result

    def getPrimitiveTypes( self ):
        return self.getBasicTypes( True )

    def getBasicTypes( self, primitive=False ):
        result = Units( )

        for unit in self:
            if unit in g.basicUnitTypes:
                unitType = unit
            else:
                if unit not in g.unitOperators:
                    raise ValueError( 'undefined unit type \'{}\''.format( unit ) )

                unitType = g.unitOperators[ unit ].unitType

            if primitive:
                basicUnits = Units( g.basicUnitTypes[ unitType ].primitiveUnit )
            else:
                basicUnits = Units( g.basicUnitTypes[ unitType ].simpleTypes )

            exponent = self[ unit ]

            if exponent != 1:   # handle exponent
                for unitType2 in basicUnits:
                    basicUnits[ unitType2 ] *= exponent

            result.update( basicUnits )

        zeroKeys = [ ]

        for unitType in result:
            if result[ unitType ] == 0:
                zeroKeys.append( unitType )

        for zeroKey in zeroKeys:
            del result[ zeroKey ]

        return result

    def getUnitString( self ):
        resultString = ''

        for unit in sorted( self ):
            exponent = self.get( unit )

            if exponent > 0:
                if resultString != '':
                    resultString += '*'

                resultString += unit

                if exponent > 1:
                    resultString += '^' + str( int( exponent ) )

        denominator = ''

        for unit in sorted( self ):
            exponent = self.get( unit )

            if exponent < 0:
                if denominator != '':
                    denominator += '*'

                denominator += unit

                if exponent < -1:
                    denominator += '^' + str( int( -exponent ) )

        if denominator != '':
            resultString += '/' + denominator

        return resultString

    def parseUnitString( self, expression ):
        pieces = expression.split( '/' )

        if len( pieces ) > 2:
            raise ValueError( 'only one \'/\' is permitted' )
        elif len( pieces ) == 2:
            result = self.parseUnitString( pieces[ 0 ] )
            result.subtract( self.parseUnitString( pieces[ 1 ] ) )

            return result
        else:
            result = Units( )

            units = expression.split( '*' )

            for unit in units:
                if unit == '':
                    raise ValueError( 'wasn\'t expecting another \'*\'' )

                operands = unit.split( '^' )

                operandCount = len( operands )

                exponent = 1

                if operandCount > 1:
                    for i in range( 1, operandCount ):
                        exponent *= int( floor( operands[ i ] ) )

                result[ operands[ 0 ] ] += exponent

            return result


# //******************************************************************************
# //
# //  class UnitTypeInfo
# //
# //******************************************************************************

class UnitTypeInfo( ):
    def __init__( self, simpleTypes, baseUnit, primitiveUnit, estimateTable ):
        self.simpleTypes = Units( simpleTypes )
        self.baseUnitType = Units( baseUnit )
        self.baseUnit = baseUnit
        self.primitiveUnit = primitiveUnit
        self.estimateTable = estimateTable


# //******************************************************************************
# //
# //  getUnitType
# //
# //******************************************************************************

def getUnitType( unit ):
    if unit in g.basicUnitTypes:
        return unit

    if unit in g.operatorAliases:
        unit = g.operatorAliases[ unit ]

    if unit in g.unitOperators:
        return g.unitOperators[ unit ].unitType
    else:
        raise ValueError( 'undefined unit type \'{}\''.format( unit ) )


# //******************************************************************************
# //
# //  class UnitInfo
# //
# //******************************************************************************

class UnitInfo( ):
    def __init__( self, unitType, representation, plural, abbrev, aliases, categories, description='',
                  autoGenerated=False ):
        self.unitType = unitType
        self.representation = representation
        self.plural = plural
        self.abbrev = abbrev
        self.aliases = aliases
        self.categories = categories
        self.description = description
        self.autoGenerated = autoGenerated


# //******************************************************************************
# //
# //  class OperatorInfo
# //
# //******************************************************************************

class OperatorInfo( ):
    def __init__( self, function, argCount ):
        self.function = function
        self.argCount = argCount


# //******************************************************************************
# //
# //  class FunctionInfo
# //
# //  Starting index is a little confusing.  When rpn knows it is parsing a
# //  function declaration, it will put all the arguments so far into the
# //  FunctionInfo object.  However, it can't know how many of them it actually
# //  needs until it's time to evaluate the function, so we need to save all the
# //  terms we have so far, since we can't know until later how many of them we
# //  will need.
# //
# //  Once we are able to parse out how many arguments belong to the function
# //  declaration, then we can determine what arguments are left over to be used
# //  with the function operation.   All function operations take at least one
# //  argument before the function declaration.
# //
# //******************************************************************************

class FunctionInfo( ):
    def __init__( self, valueList=[ ], startingIndex=0 ):
        self.valueList = [ ]

        if isinstance( valueList, list ):
            for value in valueList:
                self.valueList.append( value )
        else:
            self.valueList.append( valueList )

        self.startingIndex = startingIndex

    def evaluate( self, arg ):
        return arg

    def add( self, arg ):
        self.valueList.append( arg )


# //******************************************************************************
# //
# //  class Polynomial
# //
# //  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
# //
# //******************************************************************************

class Polynomial( object ):
    def __init__( self, *args ):
        """
        Create a polynomial in one of three ways:

        p = Polynomial( poly )              # copy constructor
        p = Polynomial( [ 1, 2, 3 ... ] )   # from sequence
        p = Polynomial( 1, 2, 3 ... )       # from scalars
        """
        super( Polynomial, self ).__init__( )

        if len( args ) == 1:
            val = args[ 0 ]

            if isinstance( val, Polynomial ):                # copy constructor
                self.coeffs = val.coeffs[ : ]
            elif isinstance( val, collections.Iterable ):    # from sequence
                self.coeffs = list( val )
            else:                                            # from single scalar
                self.coeffs = [ val + 0 ]
        else:                                                # multiple scalars
            self.coeffs = [ i + 0 for i in args ]
        self.trim( )

    def __add__( self, val ):
        "Return self+val"
        if isinstance( val, Polynomial ):                    # add Polynomial
            res = [ a + b for a, b in itertools.zip_longest( self.coeffs,
                                                             val.coeffs, fillvalue=0 ) ]
        else:                                                # add scalar
            if self.coeffs:
                res = self.coeffs[ : ]
                res[ 0 ] += val
            else:
                res = val

        return self.__class__( res )

    def __call__( self, val ):
        "Evaluate at X==val"
        res = 0
        pwr = 1

        for co in self.coeffs:
            res += co * pwr
            pwr *= val

        return res

    def __eq__( self, val ):
        "Test self==val"
        if isinstance( val, Polynomial ):
            return self.coeffs == val.coeffs
        else:
            return len( self.coeffs ) == 1 and self.coeffs[ 0 ] == val

    def __mul__( self, val ):
        "Return self*val"
        if isinstance( val, Polynomial ):
            _s = self.coeffs
            _v = val.coeffs
            res = [ 0 ] * ( len( _s ) + len( _v ) - 1 )

            for selfpow, selfco in enumerate( _s ):
                for valpow, valco in enumerate( _v ):
                    res[ selfpow + valpow ] += selfco * valco
        else:
            res = [ co * val for co in self.coeffs ]
        return self.__class__( res )

    def __neg__( self ):
        "Return -self"
        return self.__class__( [ -co for co in self.coeffs ] )

    def __pow__( self, y, z=None ):
        raise NotImplemented( )

    def _radd__( self, val ):
        "Return val+self"
        return self + val

    def __repr__( self ):
        return "{0}({1})".format( self.__class__.__name__, self.coeffs )

    def __rmul__( self, val ):
        "Return val*self"
        return self * val

    def __rsub__( self, val ):
        "Return val-self"
        return -self + val

    def __str__( self ):
        "Return string formatted as aX^3 + bX^2 + c^X + d"
        res = [ ]

        for po, co in enumerate( self.coeffs ):
            if co:
                if po == 0:
                    po = ''
                elif po == 1:
                    po = 'X'
                else:
                    po = 'X^' + str( po )

                res.append( str( co ) + po )

        if res:
            res.reverse( )
            return ' + '.join( res )
        else:
            return "0"

    def __sub__( self, val ):
        "Return self-val"
        return self.__add__( -val )

    def trim( self ):
        "Remove trailing 0-coefficients"
        _co = self.coeffs

        if _co:
            offs = len( _co ) - 1

            if _co[ offs ] == 0:
                offs -= 1

                while offs >= 0 and _co[ offs ] == 0:
                    offs -= 1

                del _co[ offs + 1 : ]

    def getCoefficients( self ):
        return self.coeffs


# //******************************************************************************
# //
# //  ContinuedFraction
# //
# //  A continued fraction, represented as a list of integer terms.
# //
# //  adapted from ActiveState Python, recipe 578647
# //
# //******************************************************************************

class ContinuedFraction( list ):
    def __init__( self, value, maxterms=15, cutoff=1e-10 ):
        if isinstance( value, ( int, float, mpf ) ):
            value = mpmathify( value )
            remainder = floor( value )
            self.append( remainder )

            while len( self ) < maxterms:
                value -= remainder

                if value > cutoff:
                    value = fdiv( 1, value )
                    remainder = floor( value )
                    self.append( remainder )
                else:
                    break

        elif isinstance( value, ( list, tuple ) ):
            self.extend( value )
        else:
            raise ValueError( 'ContinuedFraction requires a number or a list' )

    def getFraction( self, terms=None ):
        if terms is None or terms >= len( self ):
            terms = len( self ) - 1

        frac = Fraction( 1, int( self[ terms ] ) )

        for t in reversed( self[ 1 : terms ] ):
            frac = 1 / ( frac + int( t ) )

        frac += int( self[ 0 ] )

        return frac

    def __float__( self ):
        return float( self.getFraction( ) )

    def __str__( self ):
        return '[%s]' % ', '.join( [ str( int( x ) ) for x in self ] )


