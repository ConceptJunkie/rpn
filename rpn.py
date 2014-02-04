#!/usr/bin/env python

import argparse
from decimal import *

RPN_VERSION = "2.0.0"
COPYRIGHT_MESSAGE = "copyright 2012 (1988), Rick Gutleber (rickg@his.com)"

defaultPrecision = 8

def main( ):
    parser = argparse.ArgumentParser( prog='rpn', description='whereis - ' + RPN_VERSION +
                                      ' - ' + COPYRIGHT_MESSAGE,
                                       epilog="Arguments are interpreted as Reverse Polish Notation.\n" +
                                       "Supported operators include +, -, *, /, ** (power), // (root)\n" )

    parser.add_argument( 'terms', nargs='+', metavar='term' )
    parser.add_argument( '-p', '--precision', type=int, action='store', default=8 )

    args = parser.parse_args( )

    precision = args.precision

    operators = { '+', '-', '*', '/', '**', '//' }

    value = 0.0

    getcontext( ).prec = precision

    index = 1
    valueList = list( )

    for term in args.terms:
        if term in operators:
            isOperator = True
        else:
            isOperator = False

            try:
                value = Decimal( term )
            except:
                print( "rpn: error parsing term " + format( index ) + " ('" + term + "')" )
                break

        if isOperator:
            if len( valueList ) < 2:
                print( "rpn: operand expected for term " + format( index ) + " ('" + term + "')" )
                break

            value = valueList.pop( )

            if term == '+':
                valueList.append( valueList.pop( ) + value )
            elif term == '-':
                valueList.append( valueList.pop( ) - value )
            elif term == '*':
                valueList.append( valueList.pop( ) * value )
            elif term == '/':
                valueList.append( valueList.pop( ) / value )
            elif term == '**':
                valueList.append( valueList.pop( ) ** value )
            elif term == '//':
                valueList.append( valueList.pop( ) ** ( Decimal( '1.0' ) / value ) )
        else:
            valueList.append( value )

        index = index + 1
    else:
        if len( valueList ) > 1:
            print( "rpn: unexpected end of input at term " + format( index ) + " ('" + term + "')" )
            print( valueList )
        else:
            print( valueList.pop( ) )


if __name__ == '__main__':
    main( )

