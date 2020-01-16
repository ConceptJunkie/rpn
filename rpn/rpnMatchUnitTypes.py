#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnMatchUnitTypes.py
# //
# //  rpnChilada measurements class and unit conversion
# //  copyright (c) 2020, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

from mpmath import mpf


# //******************************************************************************
# //
# //  getWhichUnitType
# //
# //******************************************************************************

def getWhichUnitType( measurement, unitTypes ):
    for unitType in unitTypes:
        if measurement.isOfUnitType( unitType ):
            return unitType

    return None


# //******************************************************************************
# //
# //  matchUnitTypes
# //
# //  In addition to measurements, this method also handles RPNDateTime ('datetime')
# //  RPNLocation ('location'), and strings (assumed to be locations, and converted
# //  to RPNLocation)
# //
# //******************************************************************************

def matchUnitTypes( args, validUnitTypes ):
    from rpn.rpnAstronomy import RPNAstronomicalObject
    from rpn.rpnDateTime import RPNDateTime
    from rpn.rpnLocation import getLocation, RPNLocation
    from rpn.rpnMeasurement import RPNMeasurement

    result = { }

    for unitTypeList in validUnitTypes:
        unitTypes = list( unitTypeList )

        #print( 'unitTypes', unitTypes )

        if len( args ) != len( unitTypes ):
            raise ValueError( 'argument count mismatch in matchUnitTypes( )' )

        for arg in args:
            if isinstance( arg, mpf ):
                if 'constant' in unitTypes:
                    result[ 'constant' ] = arg
                    continue
                else:
                    result = { }
                    break

            if isinstance( arg, RPNDateTime ):
                if 'datetime' in unitTypes:
                    result[ 'datetime' ] = arg
                    continue
                else:
                    result = { }
                    break

            if isinstance( arg, str ):
                if 'location' in unitTypes:
                    result[ 'location' ] = getLocation( arg )
                    continue
                else:
                    result = { }
                    break

            if isinstance( arg, RPNLocation ):
                if 'location' in unitTypes:
                    result[ 'location' ] = arg
                    continue
                else:
                    result = { }
                    break

            if isinstance( arg, RPNAstronomicalObject ):
                if 'body' in unitTypes:
                    result[ 'body' ] = arg
                    continue
                else:
                    result = { }
                    break

            unitType = getWhichUnitType( arg, unitTypes )
            #print( 'found unit type', unitType )

            if unitType:
                #print( 'setting unitType', unitType )
                result[ unitType ] = arg
            else:
                result = { }
                #print( 'breaking...' )
                #print( )
                break

            unitTypes.remove( unitType )
        else:
            return result

    return None

