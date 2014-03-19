#!/usr/bin/env python

#//******************************************************************************
#//
#//  rpn
#//
#//  RPN command-line calculator, global declarations
#//  copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

from mpmath import *


#//******************************************************************************
#//
#//  variable initialization
#//
#//******************************************************************************

PROGRAM_VERSION = '5.17.4'
COPYRIGHT_MESSAGE = 'copyright (c) 2014 (1988), Rick Gutleber (rickg@his.com)'

defaultPrecision = 20
defaultAccuracy = 10
defaultCFTerms = 10
defaultBitwiseGroupSize = 16
defaultInputRadix = 10
defaultOutputRadix = 10
defaultDecimalGrouping = 5
defaultIntegerGrouping = 3

defaultNumerals = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

numerals = ''

phiBase = -1
fibBase = -2

inputRadix = 10

unitStack = [ ]

unitConversionMatrix = None


#//******************************************************************************
#//
#//  specialUnitConversionMatrix
#//
#//  This is for units that can't be converted with a simple multiplication
#//  factor.
#//
#//  Plus, I'm not going to do the transitive thing here, so it's necessary
#//  to explicitly state the conversions for all permutations.  That bugs me.
#//
#//  I would have included this table in makeUnits.py, but pickle doesn't
#//  work on lambdas, which is, to me, very non-Pythonic.   I could also
#//  save the expressions as strings and use eval, but that seems very
#//  non-Pythonic, too.
#//
#//  ( first unit, second unit, conversion function )
#//
#//******************************************************************************

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


#//******************************************************************************
#//
#//  class UnitTypeInfo
#//
#//******************************************************************************

class UnitTypeInfo( ):
    def __init__( self, simpleTypes, baseUnit, estimateTable ):
        self.simpleTypes = simpleTypes
        self.baseUnit = baseUnit
        self.estimateTable = estimateTable


#//******************************************************************************
#//
#//  class UnitInfo
#//
#//******************************************************************************

class UnitInfo( ):
    def __init__( self, unitType, representation, plural, abbrev, aliases, categories ):
        self.unitType = unitType
        self.representation = representation
        self.plural = plural
        self.abbrev = abbrev
        self.aliases = aliases
        self.categories = categories


#//******************************************************************************
#//
#//  class Polynomial
#//
#//  http://stackoverflow.com/questions/5413158/multiplying-polynomials-in-python
#//
#//******************************************************************************

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
            res = [ a + b for a, b in itertools.zip_longest( self.coeffs, val.coeffs, fillvalue=0 ) ]
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
                for valpow,valco in enumerate( _v ):
                    res[ selfpow + valpow ] += selfco * valco
        else:
            res = [ co * val for co in self.coeffs ]
        return self.__class__( res )


    def __neg__( self ):
        "Return -self"
        return self.__class__( [ -co for co in self.coeffs ] )


    def __pow__( self, y, z = None ):
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


#//******************************************************************************
#//
#//  accelerationTable
#//
#//  meters/second^2 : description
#//
#//******************************************************************************

accelerationTable = {
}


#//******************************************************************************
#//
#//  angleTable
#//
#//  radians : description
#//
#//******************************************************************************

angleTable = {
}


#//******************************************************************************
#//
#//  angleTable
#//
#//  meters^2 : description
#//
#//******************************************************************************

areaTable = {
}


#//******************************************************************************
#//
#//  capacitanceTable
#//
#//  farads : description
#//
#//******************************************************************************

capacitanceTable = {
}


#//******************************************************************************
#//
#//  chargeTable
#//
#//  coulombs : description
#//
#//******************************************************************************

chargeTable = {
}


#//******************************************************************************
#//
#//  constantTable
#//
#//  unities : description
#//
#//******************************************************************************

constantTable = {
}


#//******************************************************************************
#//
#//  currentTable
#//
#//  amperes : description
#//
#//******************************************************************************

currentTable = {
}


#//******************************************************************************
#//
#//  dataRateTable
#//
#//  bits/second : description
#//
#//******************************************************************************

dataRateTable = {
}


#//******************************************************************************
#//
#//  electricalConductanceTable
#//
#//  mhos : description
#//
#//******************************************************************************

electricalConductanceTable = {
}


#//******************************************************************************
#//
#//  electricalResistanceTable
#//
#//  ohms : description
#//
#//******************************************************************************

electricalResistanceTable = {
}


#//******************************************************************************
#//
#//  electricalPotentialTable
#//
#//  volts : description
#//
#//******************************************************************************

electricPotentialTable = {
}


#//******************************************************************************
#//
#//  energyTable
#//
#//  joules : description
#//
#//******************************************************************************

energyTable = {
}


#//******************************************************************************
#//
#//  forceTable
#//
#//  newtons : description
#//
#//******************************************************************************

forceTable = {
}


#//******************************************************************************
#//
#//  illuminanceTable
#//
#//  lux : description
#//
#//******************************************************************************

illuminanceTable = {
}


#//******************************************************************************
#//
#//  inductanceTable
#//
#//  henries : description
#//
#//******************************************************************************

inductanceTable = {
}


#//******************************************************************************
#//
#//  informationEntropyTable
#//
#//  bits : description
#//
#//******************************************************************************

informationEntropyTable = {
}


#//******************************************************************************
#//
#//  lengthTable
#//
#//  meters : description
#//
#//******************************************************************************

lengthTable = {
    mpf( '1.78' )       : 'the height of a typical adult male human',
    mpf( '91.44' )      : 'the length of a football field',
    mpf( '42194.988' )  : 'a marathon',
    mpf( '3983126.34' ) : 'the distance from New York to Los Angeles',
    mpf( '12756272' )   : 'the diameter of the Earth',
    mpf( '142984000' )  : 'the diameter of Jupiter',
    mpf( '1391980000' ) : 'the diameter of the Sun',
    mpf( '1.49598e11' ) : 'the distance from the Earth to the Sun',
    mpf( '4.01135e16' ) : 'the distance to the closest star, Proxima Centauri',
}


#//******************************************************************************
#//
#//  luminanceTable
#//
#//  candelas/meter^2 : description
#//
#//******************************************************************************

luminanceTable = {
}


#//******************************************************************************
#//
#//  luminousFluxTable
#//
#//  lumens : description
#//
#//******************************************************************************

luminousFluxTable = {
}


#//******************************************************************************
#//
#//  luminousIntensityTable
#//
#//  candelas : description
#//
#//******************************************************************************

luminousIntensityTable = {
}


#//******************************************************************************
#//
#//  magneticFieldStrengthTable
#//
#//  amperes/meter : description
#//
#//******************************************************************************

magneticFieldStrengthTable = {
}


#//******************************************************************************
#//
#//  magneticFluxTable
#//
#//  webers : description
#//
#//******************************************************************************

magneticFluxTable = {
}


#//******************************************************************************
#//
#//  magneticFluxDensityTable
#//
#//  teslas : description
#//
#//******************************************************************************

magneticFluxDensityTable = {
    mpf( '5e-18' )      : 'the precision attained for Gravity Probe B',
    mpf( '3.1869e-5' )  : 'the Earth\'s magnetic field at 0 degrees long., 0 degrees lat.',
    mpf( '5.0e-3' )     : 'a typical refrigerator magnet',
    mpf( '0.3' )        : 'the strength of solar sunspots',
    mpf( '3' )          : 'the maximum strength of a common magnetic resonance imaging system',
    mpf( '16' )         : 'a magnetic field strong enough to levitate a frog',
    mpf( '2800' )       : 'the largest magnetic field produced in a laboratory',
    mpf( '1.0e8' )      : 'the lower range for the magnetic field strength in a magnetar',
    mpf( '1.0e11' )     : 'the upper range for the magnetic field strength in a magnetar',
}


#//******************************************************************************
#//
#//  massTable
#//
#//  grams : description
#//
#//******************************************************************************

massTable = {
    mpf( '0.003' )      : 'an average ant',
    mpf( '17.5' )       : 'a typical mouse',
    mpf( '7.0e4' )      : 'an average human',
    mpf( '5.5e6' )      : 'an average male African bush elephant',
    mpf( '4.39985e8' )  : 'the takeoff weight of a Boeing 747-8',
    mpf( '5.9742e27' )  : 'the Earth',
}


#//******************************************************************************
#//
#//  powerTable
#//
#//  watts : description
#//
#//******************************************************************************

powerTable = {
}


#//******************************************************************************
#//
#//  pressureTable
#//
#//  pascals : description
#//
#//******************************************************************************

pressureTable = {
}


#//******************************************************************************
#//
#//  radiationAbsorbedDoseTable
#//
#//  grays : description
#//
#//******************************************************************************

radiationAbsorbedDoseTable = {
}


#//******************************************************************************
#//
#//  radiationEquivalentDoseTable
#//
#//  sieverts : description
#//
#//******************************************************************************

radiationEquivalentDoseTable = {
}


#//******************************************************************************
#//
#//  radiationExposureTable
#//
#//  coulombs/gram : description
#//
#//******************************************************************************

radiationExposureTable = {
}


#//******************************************************************************
#//
#//  radioactivityTable
#//
#//  becquerels : description
#//
#//******************************************************************************

radioactivityTable = {
}


#//******************************************************************************
#//
#//  solidAngleTable
#//
#//  steradians : description
#//
#//******************************************************************************

solidAngleTable = {
}


#//******************************************************************************
#//
#//  temperatureTable
#//
#//  kelvins : description
#//
#//******************************************************************************

temperatureTable = {
}


#//******************************************************************************
#//
#//  timeTable
#//
#//  seconds : description
#//
#//******************************************************************************

timeTable = {
}


#//******************************************************************************
#//
#//  velocityTable
#//
#//  meters/second : description
#//
#//******************************************************************************

velocityTable = {
}


#//******************************************************************************
#//
#//  volumeTable
#//
#//  liters : description
#//
#//******************************************************************************

volumeTable = {
    mpf( '0.0049' ) : 'a teaspoon',
    mpf( '3.785' )  : 'a gallon',
    mpf( '2.5e6' )  : 'an Olympic-sized swimming pool',
}


