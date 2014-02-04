#!/usr/bin/env python

#//******************************************************************************
#//
#//  makeHelp
#//
#//  RPN command-line calculator help file generator
#//  copyright (c) 2013, Rick Gutleber (rickg@his.com)
#//
#//  License: GNU GPL (see <http://www.gnu.org/licenses/gpl.html> for more
#//  information).
#//
#//******************************************************************************

import contextlib
import bz2
import pickle
import os


#//******************************************************************************
#//
#//  constants
#//
#//******************************************************************************

PROGRAM_NAME = 'makeHelp'
PROGRAM_VERSION = '5.7.8'
PROGRAM_DESCRIPTION = 'RPN command-line calculator help file generator'
COPYRIGHT_MESSAGE = 'copyright (c) 2014, Rick Gutleber (rickg@his.com)'

defaultPrecision = 20
defaultAccuracy = 10
defaultCFTerms = 10
defaultBitwiseGroupSize = 16
defaultInputRadix = 10
defaultOutputRadix = 10
defaultDecimalGrouping = 5
defaultIntegerGrouping = 3


#//******************************************************************************
#//
#//  basic help categories
#//
#//******************************************************************************

basicCategories = {
'options' :
'rpn ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE + '\n\n' +
'''
command-line options:

    -a [n], --output_accuracy [n]
        maximum number of decimal places to display, irrespective of internal
        precision (default: ''' + str( defaultAccuracy ) + ')' + '''

    -b n : --input_radix n
        specify the radix for input (default: ''' + str( defaultInputRadix ) + ')' + '''

    -c, --comma -
        add commas to result, e.g., 1,234,567.0

    -d [n], --decimal_grouping [n] -
        display decimal places separated into groups (default: ''' + str( defaultDecimalGrouping ) + ')' + '''

    -g [n], --integer_grouping [n]
        display integer separated into groups (default: ''' + str( defaultIntegerGrouping ) + ')' + '''

    -h, --help -
        displays basic help information

    -i, --identify
        identify the result (may repeat input)

    -n str, --numerals str
        characters set to use as numerals for output

    -o, --octal
        octal mode: equivalent to \'-r8 -w9 -i3 -z\'

    -p n, --precision n
        precision, i.e., number of significant digits to use

    -r n, --output_radix n
        output in a different base (2 to 62, or phi)

    -R n, --output_radix_numerals n
        output each digit is a space-delimited base-10 number

    -t, --time
        display calculation time

    -u, --find_poly
        find a polynomial such that P(x) ~= 0 of degree <= N (default: 1000)

    -w [n], --bitwise_group_size [n]
        bitwise operations group values by this size (default: ''' + str( defaultBitwiseGroupSize ) + ')' + '''

    -x, --hex
        hex mode: equivalent to '-r16 -w16 -i4 -z'

    -z, --leading_zero
        add leading zeros if needed with -i

    -!, --print_options
        print values for all options
''',
'arguments' :
'''
Arguments:

    As its name implies, rpn uses Reverse Polish Notation, otherwise referred
    to as postfix notation.  The operand(s) come first and then the operator.
    This notation works without the need for parentheses.  rpn supports
    brackets for creating lists of operands, but this serves a different
    purpose and is described later.

    Some simple examples:

    2 + 2:
        rpn 2 2 +

    3 sqrt(2) / 4:
        rpn 3 2 sqrt * 4 /

    Lists are specified using the bracket operators.
    Most operators can take lists as operands, which results in the operation
    being performed on each item in the list.  If the operator takes two
    operands, then either operand can be a list.  If one operand is a list
    and the other is a single value, then each value in the list will have
    the single operand applied to it with the operator, and the result will
    be displayed as a list.

    It is possible in certain cases to nest lists.  rpn tries to figure out
    a logical way (and unequivocal) to apply the operators to the operands.

    *** Special note:  I have not exhaustively tested every possible
    scenario with lists, but in general, if it makes sense, rpn will work
    correctly.

    For example:

    c:\>rpn [ 2 3 4 5 6 ] 10 +
    [ 12, 13, 14, 15, 16, 17 ]

    c:\>rpn 7 [ 1 2 3 4 5 6 7 ] *
    [ 7, 14, 21, 28, 35, 42, 49 ]

    If both operands are lists, then each element from the first list is
    applied to the corresponding element in the second list.  If one list
    is shorter than the other, then only that many elements will have the
    operator applied and the resulting list will only be as long as the
    shorter list.

    For example:

    rpn [ 1 2 3 4 5 6 7 ] [ 1 2 3 4 5 6 7 ] **
    [ 1, 4, 27, 256, 3125, 46656, 823543 ]

    rpn [ 10 20 30 40 50 60 ] [ 3 2 3 4 ] *
    [ 30, 40, 90, 160 ]

    Some operators take lists as operands 'natively'.  This means the
    operator requires a list, because the operation does not make sense for
    a single value.  For example, 'mean' averages the values of a list.  If
    the required list argument is a single value, rpn will promote it to a
    list.

    For example:

    c:\>rpn [ 1 2 3 ] [ 4 5 6 ] polyval
    [ 27, 38, 51 ]
''',
'input' :
'''
    For integers, rpn understands hexidecimal input of the form '0x....'.
    Otherwise, a leading '0' is interpreted as octal and a trailing 'b' or 'B'
    is interpreted as binary.  Decimal points are not allowed for binary,
    octal or hexadecimal modes, but fractional numbers in another base can be
    input using -b.

    A leading '\\' forces the term to be a number rather than an operator (for
    use with higher bases with -b).
''',
'output' :
'''
    [ description of output formats supported by rpn ]
''',
'conversion' :
'''
    [ describe unit conversions in rpn ]
''',
'about' :
PROGRAM_NAME + ' ' + PROGRAM_VERSION + ' - ' + PROGRAM_DESCRIPTION + '\n' + COPYRIGHT_MESSAGE +
'''

rpn is a command-line Reverse-Polish Notation calculator that was first written in C in 1988.
It was rewritten in Python 3 in 2012 and now uses the mpmath library.
''',
'bugs' :
'''
    rpn doesn't describe the correct argument in error messages if an option
    flag is used.

    -u doesn't work with complex numbers
''',
'license' :
'''
rpn is licensed under the GPL, version 3.0 and is ''' + '\n' + COPYRIGHT_MESSAGE + '''

    [ fill in extra boilerplate as needed ]
''',
'examples' :
'''
Here are some examples of using rpn:

Basic arithmetic operations:

    c:\>rpn 2 3 +
    5

    c:\>rpn 12 9 -
    3

    c:\>rpn 23 47 *
    1081

    c:\>rpn 10 7 /
    1.42857142857

Basic trigonometry usage:

    c:\>rpn 60 deg sin         # sine of 60 degrees
    0.866025403784

    c:\>rpn 45 deg tan         # tangent of 45 degrees
    1

    c:\>rpn 2 pi * rad         # 2 pi radians is how many degrees?
    360

    c:\>rpn 2 atan rad         # What angle (in degrees) has a slope of 2?
    63.4349488229

Convert an IP address to a 32-bit value and back:

    c:\>rpn [ 192 168 0 1 ] 256 base -x
    c0a8 0001

    c:\>rpn 0xc0a80001 -R 256
    192 168 0 1

Construct the square root of two from a continued fraction:

    c:\>rpn -p20 2 sqrt
    1.41421356237309504880

    c:\>rpn -p20 2 sqrt 20 cf2
    [ 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ]

    c:\>rpn -p20 2 sqrt 20 frac
    [ 22619537, 15994428 ]

    c:\>rpn -p20 [ 1 2 30 dup ] cf
    1.41421356237309504880

Calculations with lists:

    List of primes in the first 50 fibonacci numbers:
        rpn 1 50 range fib isprime nonzero 1 + fib

    Which of the first thousand pentagonal numbers are also triangular:
        c:\>rpn 1000 pent tri?
        1731.26218055

        c:\>rpn 1 1000 range pent 1 1732 range tri intersection

Please note that several of the following commands are broken up into multiple
lines for readability, but all of them are single commands to rpn.

In some commands, the precision is explicitly set such to limit the output to
what is accurately calculated.   If no precision options are used then the
calculation will be correct regardless of precision.

Calculation (or approximation) of various mathematical constants:

    Polya Random Walk Constant
        = rpn -p1000 -a30 1 16 2 3 / sqrt * pi 3 power * [ 1 24 / gamma 5 24 /
                    gamma 7 24 / gamma 11 24 / gamma ] prod 1/x * -

    Schwartzchild Constant (Conic Constant)
        = rpn -p20 2 0 30 range ** 0 30 range ! / sum
        = rpn e 2 **

    Somos\' Quadratic Recurrence Constant
        = rpn -p20 1 100 range 0.5 0.5 100 georange ** prod

    Prevost Constant
        = rpn -p20 1 100 range fib 1/x sum

    Euler's number = rpn -p20 0 100 range fac 1/x sum
                   = rpn e

    Gelfond Constant
        = rpn -p20 pi 0 100 range power 0 100 range ! / sum
        = rpn e pi power

    Bloch-Landau Constant
        = rpn -p20 1 3 / gamma 5 6 / gamma * 1 6 / gamma /

    Hausdorff Dimension
        = rpn -p20 2 0 100 range 2 * 1 + power 0 100 range 2 * 1 + *
            1/x sum 3 0 100 range 2 * 1 + power 0 100 range 2 * 1 +
            * 1/x sum /
        = rpn 3 log 2 log /

    Machin-Gregory Series
        = rpn -p20 1 1000 2 range2 2 1 1000 2 range2 power * 1/x altsum
        = rpn 1 2 / atan

    Beta(3)
        = rpn -p17 1 1000000 2 range2 3 power 1/x altsum
        = rpn pi 3 power 32 /

    Cahen's constant
        = rpn -p20 1 20 range sylvester 1 - 1/x altsum

    Lemniscate Constant
        = rpn 4 2 pi / sqrt * 0.25 ! sqr *

    sqrt( e )
        = rpn -p20 2 0 20 range power [ 0 20 range ] ! * 1/x sum
        = rpn -p20 0 20 range 2 * !! 1/x sum
        = rpn -p20 e sqrt

    1/e
        = rpn -p20 0 25 range fac 1/x altsum
        = rpn -p20 e 1/x

    Zeta( 6 )
        = rpn -p25 -a19 1 1 1000 primes -6 power - 1/x prod
        = rpn -p20 pi 6 power 945 /
        = rpn -p20 6 zeta

    Pythagoras' constant
        = rpn -p20 [ 1 2 25 dup ] cf
        = rpn -p20 2 sqrt

    Digamma
        = rpn -p25 -a20 1 1 1000 primes -6 power - 1/x prod
        = rpn -a5 [ 0 100000 range ] 1 + 1/x
                        [ 0 100000 range ] 1 4 / + 1/x - sum euler -

    Strongly Carefree Constant
        = rpn -a6 1 1 100000 primes 3 * 2 - 1 100000 primes 3 power / - prod
        = rpn -a7 6 pi sqr / 1 2
                1 100000 primes 1 100000 primes 1 + * 1/x * - prod *

    Ramanujan-Forsythe Constant
        = rpn 0 100000 range 2 * 3 - fac2 0 100000 range 2 * fac2 / sqr sum

    Apery's Constant
        = rpn -p20 1 5000 range 3 power 1/x sum
        = rpn -p20 3 zeta
        = rpn -p20 apery

    Omega Constant
        = rpn -p20 [ e 1/x 100 dup ] tower
        = rpn -p20 omega

    Liouville Number
        = rpn -p120 10 1 10 range ! power 1/x surpnm

    Gieseking Constant
        = rpn -a10 -p20 3 3 sqrt * 4 / 1
                0 100000 range 3 * 2 + sqr 1/x sum -
                1 100000 range 3 * 1 + sqr 1/x sum + *

    Hafner-Sarnak-McCurley Constant (2)
        = rpn -a7 1 1 100000 primes sqr 1/x - prod
        = rpn 2 zeta 1/x

    Infinite Tetration of i
        = rpn -p20 [ 1 i 1000 dup ] tower
''',
'notes' :
'''
When converting fractional output to other bases, rpn adjusts the precision
to the approximate equivalent for the new base since the precision is
applicable to base 10.

Tetration (hyperexponentiation) forces the second argument to an integer.

To compute the nth Fibonacci number accurately, rpn sets the precision to
a level sufficient to guarantee a correct answer.

Bitwise operators force all arguments to integers by truncation if necessary.
'''
}



#//******************************************************************************
#//
#//  operator help
#//
#//******************************************************************************

operatorHelp = {
    '['         : [
'modifiers', 'begins a list',
'''
''',
'''
''' ],
    ']'         : [
'modifiers', 'ends a list',
'''
''',
'''
''' ],
    'abs'           : [
'arithmetic', 'calculates the absolute value of n',
'''
''',
'''
''' ],
    'acos'          : [
'trigonometry', 'calculates the arccosine of n',
'''
''',
'''
''' ],
    'acosh'         : [
'trigonometry', 'calculates the hyperbolic arccosine of n',
'''
''',
'''
''' ],
    'acot'          : [
'trigonometry', 'calcuates the arccotangent of n',
'''
''',
'''
''' ],
    'acoth'         : [
'trigonometry', 'calculates the hyperbolic arccotangent of n',
'''
''',
'''
''' ],
    'acsc'          : [
'trigonometry', 'calculates the arccosecant of n',
'''
''',
'''
''' ],
    'acsch'         : [
'trigonometry', 'calculates the hyperbolic arccosecant of n',
'''
''',
'''
''' ],
    'add'           : [
'arithmetic', 'adds n to k',
'''
This operator adds two terms together.
''',
'''
c:\>rpn 2 2 add
4

c:\>rpn [ 1 2 3 4 5 6 ] 5 add
[ 6, 7, 8, 9, 10, 11 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 10 10 10 ] add
[ 11, 12, 13, 14, 15, 16 ]

c:\>rpn [ 1 2 3 4 5 6 ] [ 10 10 10 ] add
[ 11, 12, 13 ]''' ],
    'altfac'        : [
'number_theory', 'calculates the alternating factorial of n',
'''
''',
'''
''' ],
    'altsign'       : [
'list_operators', 'alternates signs in the list by making every even element negative',
'''
''',
'''
''' ],
    'altsign2'      : [
'list_operators', 'alternates signs in the list by making every odd element negative',
'''
''',
'''
''' ],
    'altsum'        : [
'arithmetic', 'calculates the alternating sum of list n (addition first)',
'''
''',
'''
''' ],
    'altsum2'       : [
'arithmetic', 'calaculates the alternating sum of list n (subtraction first)',
'''
''',
'''
''' ],
    'and'           : [
'logical', 'calculates the bitwise \'and\' of n and k',
'''
''',
'''
''' ],
    'apery'         : [
'constants', 'returns Apery\'s constant',
'''
Apery's constant is the sum of the infinite series of the reciprocals of cubes
from 1 to infinity.  It is also, therefore, zeta( 3 ).
''',
'''
''' ],
    'aperynum'      : [
'combinatorics', 'calculates the nth Apery number',
'''
''',
'''
''' ],
    'append'        : [
'list_operators', 'appends the second list on to the first list',
'''
''',
'''
''' ],
    'asec'          : [
'trigonometry', 'calculates the arcsecant of n',
'''
''',
'''
''' ],
    'asech'         : [
'trigonometry', 'calculates the hyperbolic arcsecant of n',
'''
''',
'''
''' ],
    'asin'          : [
'trigonometry', 'calculates the arcsine of n',
'''
''',
'''
''' ],
    'asinh'         : [
'trigonometry', 'calculates the hyperbolic arcsine of n',
'''
''',
'''
''' ],
    'atan'          : [
'trigonometry', 'calculates the arctangent of n',
'''
''',
'''
''' ],
    'atanh'         : [
'trigonometry', 'calculates the hyperbolic arctangent of n',
'''
''',
'''
''' ],
    'balanced'      : [
'prime_numbers', 'calculate the first of the nth set of balanced primes',
'''
''',
'''
''' ],
    'balanced_'     : [
'prime_numbers', 'calculate the nth set of balanced primes',
'''
''',
'''
''' ],
    'base'          : [
'number_theory', 'interpret list elements as base k digits',
'''
''',
'''
''' ],
    'bell'          : [
'combinatorics', 'calculate the nth Bell number',
'''
''',
'''
''' ],
    'bellpoly'      : [
'algebra', 'evaluates the nth Bell polynomial with k',
'''
''',
'''
''' ],
    'bernoulli'     : [
'combinatorics', 'calculate the nth Bernoulli number',
'''
''',
'''
''' ],
    'binomial'      : [
'combinatorics', 'calculates the binomial coefficient of n and k',
'''
''',
'''
''' ],
    'catalan'       : [
'combinatorics', 'calculates nth Catalan number',
'''
''',
'''
''' ],
    'carol'         : [
'number_theory', 'gets the nth Carol number',
'''
''',
'''
''' ],
    'catalans'      : [
'constants', 'returns Catalan\'s constant',
'''
''',
'''
''' ],
    'centeredcube'  : [
'polyhedral_numbers', 'calculates the nth centered cube number',
'''
''',
'''
''' ],
    'cdecagonal'    : [
'polygonal_numbers', 'calculates the nth centered decagonal number',
'''
''',
'''
''' ],
    'cdecagonal?'   : [
'polygonal_numbers', 'finds the index of the centered decagonal number of value n',
'''
'cdecagonal?' solves for the index of the equation used by 'cdecagonal' to
get the index i of the ith centered decagonal number that corresponds to the
value n.

If n is not a centered decagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'ceiling'       : [
'arithmetic', 'returns the next highest integer for n',
'''
''',
'''
''' ],
    'cf'            : [
'number_theory', 'interprets list n as a continued fraction',
'''
''',
'''
''' ],
    'champernowne'  : [
'constants', 'returns the Champernowne constant',
'''
''',
'''
''' ],
    'char'          : [
'conversion', 'converts the value to a signed 8-bit integer',
'''
''',
'''
''' ],
    'cheptagonal'   : [
'polygonal_numbers', 'calculates the nth centered heptagonal number',
'''
''',
'''
''' ],
    'cheptagonal?'  : [
'polygonal_numbers', 'finds the index of the centered heptagonal number of value n',
'''
'cheptagonal?' solves for the index of the equation used by 'cheptagonal' to
get the index i of the ith centered heptagonal number that corresponds to the
value n.

If n is not a centered heptagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'chexagonal'    : [
'polygonal_numbers', 'calculates the nth centered hexagonal number',
'''
''',
'''
''' ],
    'chexagonal?'   : [
'polygonal_numbers', 'finds the index of the centered hexagonal number of value n',
'''
'chexagonal?' solves for the index of the equation used by 'chexagonal' to
get the index i of the ith centered hexagonal number that corresponds to the
value n.

If n is not a centered hexagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cnonagonal'    : [
'polygonal_numbers', 'calculates the nth centered nonagonal number',
'''
''',
'''
''' ],
    'cnonagonal?'   : [
'polygonal_numbers', 'finds the index of the centered nonagonal number of value n',
'''
'cnonagonal?' solves for the index of the equation used by 'cnonagonal' to
get the index i of the ith centered nonagonal number that corresponds to the
value n.

If n is not a centered nonagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'coctagonal'    : [
'polygonal_numbers', 'calculates the nth centered octagonal number',
'''
''',
'''
''' ],
    'coctagonal?'   : [
'polygonal_numbers', 'finds the index of the centered octgonal number of value n',
'''
'coctagonal?' solves for the index of the equation used by 'coctagonal' to
get the index i of the ith centered octagonal number that corresponds to the
value n.

If n is not a centered octagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'convert'       : [
'conversion', 'perform unit conversion',
'''
This is a special operator that doesn't require an operand.  If there is no
numerical value, then rpn will assume a value of 1.
''',
'''
''' ],
    'copeland'      : [
'constants', 'returns the Copeland Erdos constant',
'''
''',
'''
''' ],
    'cos'           : [
'trigonometry', 'calculates the cosine of n',
'''
''',
'''
''' ],
    'cosh'          : [
'trigonometry', 'calculates the hyperbolic cosine of n',
'''
''',
'''
''' ],
    'cot'           : [
'trigonometry', 'calculates the cotangent of n',
'''
''',
'''
''' ],
    'coth'          : [
'trigonometry', 'calculates the hyperbolic cotangent of n',
'''
''',
'''
''' ],
    'count'         : [
'list_operators', 'counts the elements of list n',
'''
''',
'''
''' ],
    'countbits'     : [
'logical', 'returns the number of set bits in the value of n',
'''
''',
'''
''' ],
    'countdiv'      : [
'number_theory', 'returns a count of the divisors of n',
'''
The divcount operator factors the argument and then calculates number of divisors
from the list of prime factors.  'divisors count' calculates the same result, but
the 'divisors' operator can generate prohibitively large lists for numbers with a
lot of factors.
''',
'''
c:\>rpn 98280 divcount
128

c:\>rpn 1 20 range divcount
[ 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6 ]
''' ],
    'cousinprime'   : [
'prime_numbers', 'returns the nth cousin prime',
'''
''',
'''
''' ],
    'cpentagonal'   : [
'polygonal_numbers', 'calculates the nth centered pentagonal number',
'''
''',
'''
''' ],
    'cpentagonal?'  : [
'polygonal_numbers', 'finds the index of the centered pentagonal number of value n',
'''
'cpentagonal?' solves for the index of the equation used by 'cpentagonal' to
get the index i of the ith centered pentagonal number that corresponds to the
value n.

If n is not a centered pentagonal number, the result will not be a whole
number.
''',
'''
''' ],
    'cpolygonal'    : [
'polygonal_numbers', 'calculates the nth centered k-gonal number',
'''
''',
'''
''' ],
    'cpolygonal?'   : [
'polygonal_numbers', 'finds the index of the centered polygonal number of value n',
'''
'cpolygonal?' solves for the index of the equation used by 'cpolygonal' to
get the index i of the ith centered k-sided polygonal number that corresponds
to the value n.

If n is not a centered k-sided polygonal number, the result will not be a whole
number.
''',
'''
''' ],
    'csc'           : [
'trigonometry', 'calculates the cosecant of n',
'''
''',
'''
''' ],
    'csch'          : [
'trigonometry', 'calculates hyperbolic cosecant of n',
'''
''',
'''
''' ],
    'csquare'       : [
'polygonal_numbers', 'calculates the nth centered square number',
'''
''',
'''
''' ],
    'csquare?'       : [
'polygonal_numbers', 'finds the index of the centered square number of value n',
'''
'csquare?' solves for the index of the equation used by 'csquare' to get the
index i of the ith centered square number that corresponds to the value n.

If n is not a centered square number, the result will not be a whole number.
''',
'''
''' ],
    'ctriangular'   : [
'polygonal_numbers', 'calculates the nth centered triangular number',
'''
''',
'''
''' ],
    'ctriangular?'   : [
'polygonal_numbers', 'finds the index of the centered triangular number of value n',
'''
'ctriangular?' solves for the index of the equation used by 'ctriangular' to
get the index i of the ith centered triangular number that corresponds to the
value n.

If n is not a centered triangular number, the result will not be a whole
number.
''',
'''
''' ],
    'cube'          : [
'powers_and_roots', 'calculates the cube of n',
'''
'cube' simply returns the value of n to the third power.
''',
'''
''' ],
    'decagonal'     : [
'polygonal_numbers', 'calculates the nth decagonal number',
'''
''',
'''
''' ],
    'decagonal?'    : [
'polygonal_numbers', 'finds the index of the decagonal number of value n',
'''
''',
'''
''' ],
    'degrees'       : [
'trigonometry', 'interprets n as degrees and converts to radians',
'''
''',
'''
''' ],
    'delannoy'      : [
'combinatorics', 'calculates the nth Delannoy number',
'''
''',
'''
''' ],
    'diffs'         : [
'list_operators', 'returns a list with the differences between successive elements of list n',
'''
''',
'''
''' ],
    'divide'        : [
'arithmetic', 'divides n by k',
'''
''',
'''
''' ],
    'divisors'      : [
'number_theory', 'returns a list of divisors of n',
'''
''',
'''
''' ],
    'dodecahedral'  : [
'polyhedral_numbers', 'returns the nth dodecahedral number',
'''
''',
'''
''' ],
    'double'        : [
'conversion', 'convert n to the representation of a 64-bit IEEE 754 float',
'''
''',
'''
''' ],
    'doublebal'     : [
'prime_numbers', 'returns the nth set of double balanced primes',
'''
''',
'''
''' ],
    'doublebal_'    : [
'prime_numbers', 'returns the nth set of double balanced primes',
'''
''',
'''
''' ],
    'doublefac'     : [
'number_theory', 'calculates the double factorial of n',
'''
''',
'''
''' ],
    'dup'       : [
'modifiers', 'duplicates a argument n k times',
'''
''',
'''
''' ],
    'e'             : [
'constants', 'returns e (Euler\'s number)',
'''
''',
'''
''' ],
    'egypt'         : [
'number_theory', 'calculates the greedy Egyption fractions for n/k',
'''
''',
'''
''' ],
    'element'       : [
'list_operators', 'return a single element from a list',
'''
''',
'''
''' ],
    'euler'         : [
'constants', 'returns the Euler-Mascheroni constant',
'''
''',
'''
''' ],
    'exp'           : [
'powers_and_roots', 'calculates the nth power of e',
'''
''',
'''
''' ],
    'exp10'         : [
'powers_and_roots', 'calculates nth power of 10',
'''
''',
'''
''' ],
    'expphi'        : [
'powers_and_roots', 'calculates the nth power of phi',
'''
expphi simply takes phi (the Golden Ratio) to the power of the argument n.

It was originally added to make testing the base phi output easier.
''',
'''
c:\>rpn 2 expphi
2.61803398875

c:\>rpn 3 expphi 2 expphi -
1.61803398875
''' ],
    'factor'        : [
'number_theory', 'calculates the prime factorization of n',
'''
''',
'''
''' ],
    'factorial'     : [
'number_theory', 'calculates the prime factorization of n',
'''
'factorial' calculates the product of all whole numbers from 1 to n.
''',
'''
''' ],
    'fibonacci'     : [
'number_theory', 'calculates the nth Fibonacci number',
'''
''',
'''
''' ],
    'flatten'   : [
'list_operators', 'flattens a nested lists in list n to a single level',
'''
''',
'''
''' ],
    'float'         : [
'conversion', 'convert n to the representation of a 32-bit IEEE 754 float',
'''
''',
'''
''' ],
    'floor'         : [
'arithmetic', 'calculates the next lowest integer for n',
'''
''',
'''
''' ],
    'fraction'      : [
'number_theory', 'calculates a rational approximation of n using k terms of the continued fraction',
'''
''',
'''
''' ],
    'fromunixtime'  : [
'conversion', 'converts Unix time (seconds since epoch) to a date-time format'
'''
''',
'''
''' ],
    'gamma'         : [
'number_theory', 'calculates the gamma function for n',
'''
''',
'''
''' ],
    'gcd'           : [
'arithmetic', 'calculates the greatest common denominator of elements in list n',
'''
''',
'''
''' ],
    'georange'      : [
'list_operators', 'generates a list of geometric progression of numbers',
'''
''',
'''
''' ],
    'glaisher'      : [
'constants', 'returns Glaisher\'s constant',
'''
''',
'''
''' ],
    'harmonic'      : [
'number_theory', 'returns the sum of the first n terms of the harmonic series',
'''
''',
'''
''' ],
    'heptagonal'    : [
'polygonal_numbers', 'calculates the nth heptagonal number',
'''
''',
'''
''' ],
    'heptagonal?'   : [
'polygonal_numbers', 'finds the index of the heptagonal number of value n',
'''
''',
'''
''' ],
    'heptanacci'    : [
'polygonal_numbers', 'calculates the nth Heptanacci number',
'''
''',
'''
''' ],
    'hepthex'       : [
'polygonal_numbers', 'calculates the nth heptagonal hexagonal number',
'''
''',
'''
''' ],
    'heptpent'      : [
'polygonal_numbers', 'calculates the nth heptagonal pentagonal number',
'''
''',
'''
''' ],
    'heptsquare'    : [
'polygonal_numbers', 'calculates the nth heptagonal square number',
'''
''',
'''
''' ],
    'hepttri'       : [
'polygonal_numbers', 'calculates the nth heptagonal triangular number',
'''
''',
'''
''' ],
    'hexagonal'     : [
'polygonal_numbers', 'calculates the nth hexagonal number',
'''
''',
'''
''' ],
    'hexagonal?'    : [
'polygonal_numbers', 'finds the index of the hexagonal number of value n',
'''
''',
'''
''' ],
    'hexanacci'     : [
'number_theory', 'calculates the nth Hexanacci number',
'''
''',
'''
''' ],
    'hexpent'       : [
'polygonal_numbers', 'calculates the nth hexagonal pentagonal number',
'''
''',
'''
''' ],
    'hyper4_2'      : [
'powers_and_roots', 'calculates the right-associative tetration of n by k',
'''
''',
'''
''' ],
    'hyperfac'      : [
'number_theory', 'calculates the hyperfactorial of n',
'''
''',
'''
''' ],
    'hypot'         : [
'trigonometry', 'calculates the hypotenuse of n and k',
'''
''',
'''
''' ],
    'i'             : [
'complex_math', 'multiplies n by i',
'''
''',
'''
''' ],
    'icosahedral'   : [
'polyhedral_numbers', 'returns the nth icosahedral number',
'''
''',
'''
''' ],
    'integer'       : [
'conversion', 'convert the value to an signed ik-bit nteger',
'''
''',
'''
''' ],
    'interleave'    : [
'list_operators', 'interleaves lists n and k into a single list',
'''
''',
'''
''' ],
    'intersection'  : [
'list_operators', 'returns the intersection of two lists',
'''
''',
'''
''' ],
    'isdivisible'   : [
'arithmetic', 'is n divisible by k?',
'''
''',
'''
''' ],
    'isolated'      : [
'prime_numbers', 'returns the nth isolated prime',
'''
''',
'''
''' ],
    'isprime'       : [
'number_theory', 'is prime?',
'''
''',
'''
''' ],
    'issquare'      : [
'arithmetic', 'is n a perfect square?',
'''
''',
'''
''' ],
    'itoi'          : [
'constants', 'returns i to the i power',
'''
''',
'''
''' ],
    'jacobsthal'      : [
'number_theory', 'returns nth number of the Jacobsthal sequence',
'''
''',
'''
''' ],
    'khinchin'      : [
'constants', 'returns Khinchin\'s constant',
'''
''',
'''
''' ],
    'lah'           : [
'combinatorics', '',
'''
''',
'''
''' ],
    'lambertw'      : [
'logarithms', '',
'''
''',
'''
''' ],
    'kynea'         : [
'number_theory', 'gets the nth Kynea number',
'''
''',
'''
''' ],
    'leyland'       : [
'number_theory', 'gets the Leyland number for n and k',
'''
''',
'''
''' ],
    'lgamma'        : [
'number_theory', 'calculates the loggamma function for n',
'''
''',
'''
''' ],
    'li'            : [
'logarithms', 'calculates the logarithmic interval of n',
'''
''',
'''
''' ],
    'linearrecur'   : [
'arithmetic', 'calculates the nth value of a linear recurrence specified by a list of seeds and of factors'
'''
''',
'''
''' ],
    'ln'            : [
'logarithms', 'calculates the natural logarithm of n',
'''
''',
'''
''' ],
    'log10'         : [
'logarithms', 'calculates the base-10 logarithm of n',
'''
''',
'''
''' ],
    'log2'          : [
'logarithms', 'calculates the base-2 logarithm of n',
'''
''',
'''
''' ],
    'logxy'         : [
'logarithms', 'calculates the base-k logarithm of n',
'''
''',
'''
''' ],
    'long'          : [
'conversion', 'converts the value to a signed 32-bit integer',
'''
''',
'''
''' ],
    'longlong'      : [
'conversion', 'converts the value to a signed 64-bit integer',
'''
''',
'''
''' ],
    'lucas'         : [
'number_theory', 'calculates the nth Lucas number',
'''
''',
'''
''' ],
    'makecf'        : [
'number_theory', 'calculates k terms of the continued fraction representation of n',
'''
''',
'''
''' ],
    'max'       : [
'arithmetic', 'returns the largest value in list n',
'''
''',
'''
''' ],
    'maxindex'  : [
'arithmetic', 'returns the index of largest value in list n',
'''
''',
'''
''' ],
    'mean'      : [
'arithmetic', 'calculates the mean of values in list n',
'''
''',
'''
''' ],
    'mertens'       : [
'constants', 'returns Merten\'s constant',
'''
''',
'''
''' ],
    'min'       : [
'arithmetic', 'returns the smallest value in list n',
'''
''',
'''
''' ],
    'minindex'  : [
'arithmetic', 'returns the index of smallest value in list n',
'''
''',
'''
''' ],
    'modulo'        : [
'arithmetic', 'calculates n modulo k',
'''
''',
'''
''' ],
    'motzkin'       : [
'combinatorics', 'calculates the nth Motzkin number',
'''
''',
'''
''' ],
    'multiply'      : [
'arithmetic', 'multiplies n by k',
'''
''',
'''
''' ],
    'narayana'      : [
'combinatorics', '',
'''
''',
'''
''' ],
    'negative'      : [
'arithmetic', 'calculates the negative of n',
'''
''',
'''
''' ],
    'nonagonal'     : [
'polygonal_numbers', 'calculates the nth nonagonal number',
'''
''',
'''
''' ],
    'nonagonal?'    : [
'polygonal_numbers', 'finds the index of the nonagonal number of value n',
'''
''',
'''
''' ],
    'nonahept'      : [
'polygonal_numbers', 'calculates the nth nonagonal heptagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and heptagonal.
''',
'''
''' ],
    'nonahex'       : [
'polygonal_numbers', 'calculates the nth nonagonal hexagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and hexagonal.
''',
'''
''' ],
    'nonaoct'       : [
'polygonal_numbers', 'calculates the nth nonagonal octagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and octagonal.
''',
'''
''' ],
    'nonapent'      : [
'polygonal_numbers', 'calculates the nth nonagonal pentagonal number',
'''
'nonahex' calculates the nth number that is both nonagonal and pentgonal.
''',
'''
''' ],
    'nonasquare'    : [
'polygonal_numbers', 'calculates the nth nonagonal square number',
'''
'nonasquare' calculates the nth number that is both nonagonal and square.
''',
'''
''' ],
    'nonatri'       : [
'polygonal_numbers', 'calculates the nth nonagonal triangular number',
'''
'nonatri' calculates the nth number that is both nonagonal and triangular.
''',
'''
''' ],
    'nonzero'   : [
'list_operators', 'returns the indices of elements of list n that are not zero',
'''
''',
'''
''' ],
    'not'           : [
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
    'nspherearea'   : [
'trigonometry', 'calculate the surface area of an n-sphere of size k (radius or volume)',
'''
''',
'''
''' ],
    'nsphereradius' : [
'trigonometry', 'calculate the radius of an n-sphere of size k (surface area or volume)',
'''
''',
'''
''' ],
    'nspherevolume' : [
'trigonometry', 'calculate the volume of an n-sphere of size k (radius or surface area)',
'''
''',
'''
''' ],
    'nthprime?'     : [
'prime_numbers', 'finds the index of the closest prime over n',
'''
''',
'''
''' ],
    'nthquad?'      : [
'prime_numbers', 'finds the index of the first of the closest quadruplet prime set over n',
'''
''',
'''
''' ],
    'octagonal'     : [
'polygonal_numbers', 'calculates the nth octagonal number',
'''
''',
'''
''' ],
    'octagonal?'    : [
'polygonal_numbers', 'finds the index of the octagonal number of value n',
'''
''',
'''
''' ],
    'octahedral'    : [
'polyhedral_numbers', 'calculates the nth octahedral number',
'''
''',
'''
''' ],
    'octhept'       : [
'polygonal_numbers', 'nth octagonal heptagonal number',
'''
''',
'''
''' ],
    'octhex'        : [
'polygonal_numbers', 'calculates the nth octagonal hexagonal number',
'''
''',
'''
''' ],
    'octpent'       : [
'polygonal_numbers', 'calculates the nth octagonal pentagonal number',
'''
''',
'''
''' ],
    'octsquare'     : [
'polygonal_numbers', 'calculates the nth octagonal square number',
'''
''',
'''
''' ],
    'octtri'        : [
'polygonal_numbers', 'calculates the nth octagonal triangular number',
'''
''',
'''
''' ],
    'oeis'          : [
'special', 'downloads the OEIS integer series n',
'''
''',
'''
''' ],
    'oeiscomment'   : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisex'        : [
'special', 'downloads the comment field for the OEIS integer series n',
'''
''',
'''
''' ],
    'oeisname'      : [
'special', 'downloads the name of the OEIS integer series n',
'''
''',
'''
''' ],
    'omega'         : [
'constants', 'return the Omega constant',
'''
''',
'''
''' ],
    'or'            : [
'logical', 'calculates the bitwise \'or\' of n and k',
'''
''',
'''
''' ],
    'padovan'       : [
'number_theory', 'calculates the the nth Padovan number',
'''
''',
'''
''' ],
    'parity'        : [
'logical', 'returns the bit parity of n (0 == even, 1 == odd)',
'''
''',
'''
''' ],
    'pascal'        : [
'number_theory', 'calculates the nth line of Pascal\'s triangle',
'''
''',
'''
''' ],
    'pell'          : [
'combinatorics', 'calculates the nth Pell number',
'''
''',
'''
''' ],
    'pentagonal'    : [
'polygonal_numbers', 'calculates the nth pentagonal number',
'''
''',
'''
''' ],
    'pentagonal?'   : [
'polygonal_numbers', 'finds the index of the pentagonal number of value n',
'''
''',
'''
''' ],
    'pentanacci'    : [
'number_theory', 'calculates the nth Pentanacci number',
'''
''',
'''
''' ],
    'pentatope'     : [
'polyhedral_numbers', 'calculates the nth pentatope number',
'''
''',
'''
''' ],
    'perm'          : [
'combinatorics', 'calculates the number of permutations of k out of n objects',
'''
''',
'''
''' ],
    'phi'           : [
'constants', 'returns phi (the Golden Ratio)',
'''
''',
'''
''' ],
    'pi'            : [
'constants', 'returns pi (Archimedes\' constant)',
'''
''',
'''
''' ],
    'plastic'       : [
'constants', 'returns the Plastic constant',
'''
''',
'''
''' ],
    'polyadd'   : [
'algebra', 'interpret two lists as polynomials and add them',
'''
''',
'''
''' ],
    'polyarea'   : [
'trigonometry', 'calculates the area of an regular n-sided polygon with sides of unit length',
'''
''',
'''
''' ],
    'polygamma'     : [
'number_theory', 'calculates the polygamma function for n',
'''
''',
'''
''' ],
    'polygonal'     : [
'number_theory', 'calculates the nth polygonal number with k sides',
'''
''',
'''
''' ],
    'polygonal?'     : [
'number_theory', 'finds the index of the polygonal number with k sides of value n',
'''
''',
'''
''' ],
    'polylog'       : [
'logarithms', 'calculates the polylogarithm of n, k',
'''
''',
'''
''' ],
    'polymul'   : [
'algebra', 'interpret two lists as polynomials and multiply them',
'''
''',
'''
''' ],
    'polyprime'     : [
'prime_numbers', 'returns the nth prime, recursively k times',
'''
''',
'''
''' ],
    'polyprod'  : [
'algebra', 'interprets elements of list n as polynomials and calculates their product',
'''
''',
'''
''' ],
    'polysum'   : [
'algebra', 'interprets elements of list n as polynomials and calculates their sum',
'''
''',
'''
''' ],
    'polytope'      : [
'polyhedral_numbers', 'calculates nth polytope number of dimension k',
'''
''',
'''
''' ],
    'polyval'   : [
'algebra', 'interpret the list as a polynomial and evaluate it for value k',
'''
''',
'''
''' ],
    'power'         : [
'powers_and_roots', 'calculates the kth power of n',
'''
''',
'''
''' ],
    'product'   : [
'arithmetic', 'calculates the product of values in list n',
'''
''',
'''
''' ],
    'prime'         : [
'prime_numbers', 'returns the nth prime',
'''
''',
'''
''' ],
    'primepi'       : [
'prime_numbers', 'estimates the count of prime numbers up to and including n',
'''
''',
'''
''' ],
    'primes'        : [
'prime_numbers', 'generates a range of primes from index n to index k',
'''
This function is identical to 'n k range prime', but is much more efficient
given the way calculating prime numbers is currently done.
''',
'''
''' ],
    'prime?'        : [
'prime_numbers', 'find the index of the closest prime at n or above',
'''
''',
'''
''' ],
    'primorial'     : [
'prime_numbers', 'calculates the nth primorial',
'''
''',
'''
''' ],
    'pyramid'       : [
'polyhedral_numbers', 'calculates the nth square pyramidal number',
'''
''',
'''
''' ],
    'quadprime?'    : [
'prime_numbers', 'find the closest set of quadruplet primes above n',
'''
''',
'''
''' ],
    'quadprime'     : [
'prime_numbers', 'returns the first of the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quadprime_'    : [
'prime_numbers', 'returns the nth set of quadruplet primes',
'''
''',
'''
''' ],
    'quintprime'    : [
'prime_numbers', 'returns the first of the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'quintprime_'   : [
'prime_numbers', 'returns the nth set of quintruplet primes',
'''
''',
'''
''' ],
    'radians'       : [
'trigonometry', 'interprets n as radians and converts to degrees',
'''
''',
'''
''' ],
    'random'        : [
'special', 'returns a random value from 0 to 1',
'''
''',
'''
''' ],
    'range'         : [
'list_operators', 'generates a list of successive integers from n to k',
'''
''',
'''
''' ],
    'range2'        : [
'list_operators', 'generates a list of arithmetic progression of numbers',
'''
''',
'''
''' ],
    'reciprocal'    : [
'arithmetic', 'returns the reciprocal of n',
'''
''',
'''
''' ],
    'repunit'       : [
'algebra', 'returns the nth repunit in base k',
'''
''',
'''
''' ],
    'result'        : [
'special', 'load previous result',
'''
''',
'''
''' ],
    'rhombdodec'    : [
'polyhedral_numbers', 'calculates the nth rhombic dodecahedral number',
'''
''',
'''
''' ],
    'riesel'        : [
'number_theory', 'calculates the nth Riesel (or Woodall) number',
'''
''',
'''
''' ],
    'root'          : [
'powers_and_roots', 'calculates the kth root of n',
'''
''',
'''
''' ],
    'root2'         : [
'powers_and_roots', 'calculates the square root of n',
'''
This operator is the equivalent of 'n 2 root'.
''',
'''
''' ],
    'root3'         : [
'powers_and_roots', 'calculates the cube root of n',
'''
This operator is the equivalent of 'n 3 root'.
''',
'''
''' ],
    'round'         : [
'arithmetic', 'rounds n to the nearest integer',
'''
''',
'''
''' ],
    'safeprime'     : [
'prime_numbers', 'returns the nth safe prime',
'''
''',
'''
''' ],
    'schroeder'     : [
'combinatorics', 'calculates the nth Schroeder number',
'''
''',
'''
''' ],
    'sec'           : [
'trigonometry', 'calculates the secant of n',
'''
''',
'''
''' ],
    'sech'          : [
'trigonometry', 'calculates the hyperbolic secant of n',
'''
''',
'''
''' ],
    'sextprime'     : [
'prime_numbers', 'returns the first of the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sextprime_'    : [
'prime_numbers', 'returns the nth set of sextuplet primes',
'''
''',
'''
''' ],
    'sexyprime'     : [
'prime_numbers', 'returns the first of the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexyprime_'    : [
'prime_numbers', 'returns the nth set of sexy primes',
'''
''',
'''
''' ],
    'sexytriplet'   : [
'prime_numbers', 'returns the first of the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexytriplet_'  : [
'prime_numbers', 'returns the nth set of sexy triplet primes',
'''
''',
'''
''' ],
    'sexyquad'     : [
'prime_numbers', 'returns the first of the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'sexyquad_'     : [
'prime_numbers', 'returns the nth set of sexy quadruplet primes',
'''
''',
'''
''' ],
    'short'         : [
'conversion', 'converts the value to a signed 16-bit integer',
'''
''',
'''
''' ],
    'sin'           : [
'trigonometry', 'calculates the sine of n',
'''
''',
'''
''' ],
    'sinh'          : [
'trigonometry', 'calculates the hyperbolic sine of n',
'''
''',
'''
''' ],
    'shiftleft'     : [
'logical', 'performs a bitwise left shift of value n by k bits',
'''
''',
'''
''' ],
    'shiftright'    : [
'logical', 'performs a bitwise right shift of value n by k bits',
'''
''',
'''
''' ],
    'solve'     : [
'algebra', 'interprets list n as a polynomial and solves for its roots',
'''
''',
'''
''' ],
    'solve2'        : [
'algebra', 'solves a quadratic equation',
'''
''',
'''
''' ],
    'solve3'        : [
'algebra', 'solves a cubic equation',
'''
''',
'''
''' ],
    'solve4'        : [
'algebra', 'solves a quartic equation',
'''
''',
'''
''' ],
    'sophieprime'   : [
'prime_numbers', 'returns the nth Sophie Germain prime',
'''
''',
'''
''' ],
    'sort'      : [
'list_operators', 'sort the elements of list n numerically in ascending order',
'''
The 'sort' operator gets applied recursively, so all sublists will be sorted as
well.  I might have to reconsider that.
''',
'''
c:\>rpn [ rand rand rand ] sort
[ 0.782934612763, 0.956555810967, 0.97728726503 ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] sort
[ [ 10 ], [ 9 ], [ 8 ], [ 5, 6, 7 ], [ 4 ], [ 3 ], [ 1, 2 ], [ 0 ], [ -1 ] ]

c:\>rpn [ 10 9 8 [ 7 6 5 ] 4 3 [ 2 1 ] 0 [ -1 ] ] flatten sort
[ -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
''' ],
    'sortdesc'  : [
'list_operators', 'sorts the elements of list n numerically in descending order',
'''
The 'sortdesc' operator works exactly like the sort operator, sorting the list
(and all sublists), except in descending order.
''',
'''
c:\>rpn 1 70 6 range2 sortdesc
[ 67, 61, 55, 49, 43, 37, 31, 25, 19, 13, 7, 1 ]

c:\>rpn 1 20 range countdiv sortdesc
[ 6, 6, 6, 5, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1 ]
''' ],
    'spherearea'   : [
'trigonometry', 'calculate the surface area of an sphere of size n (radius or volume)',
'''
''',
'''
''' ],
    'sphereradius' : [
'trigonometry', 'calculate the radius of an sphere of size n (surface area or volume)',
'''
''',
'''
''' ],
    'spherevolume' : [
'trigonometry', 'calculate the volume of an sphere of size n (radius or surface area)',
'''
''',
'''
''' ],
    'square'        : [
'powers_and_roots', 'calculates the square of n',
'''
''',
'''
''' ],
    'squaretri'     : [
'polygonal_numbers', 'calculates the nth square triangular number',
'''
''',
'''
''' ],
    'stddev'    : [
'arithmetic', 'calculates the standard deviation of values in list n',
'''
''',
'''
c:\>rpn 1 50 range countdiv stddev
2.14485430741
''' ],
    'steloct'       : [
'polyhedral_numbers', 'calculates the nth stella octangula number',
'''
''',
'''
''' ],
    'subfac'        : [
'number_theory', 'calculates the subfactorial of n',
'''
''',
'''
''' ],
    'subtract'      : [
'arithmetic', 'subtracts k from n',
'''
''',
'''
''' ],
    'sum'       : [
'arithmetic', 'calculates the sum of values in list n',
'''
''',
'''
''' ],
    'superfac'      : [
'number_theory', 'calculates the superfactorial of n',
'''
''',
'''
''' ],
    'superprime'    : [
'prime_numbers', 'returns the nth superprime (the nth primeth prime)',
'''
''',
'''
''' ],
    'sylvester'     : [
'combinatorics', 'calculates the nth Sylvester number',
'''
''',
'''
''' ],
    'tan'           : [
'trigonometry', 'calculates the tangent of n',
'''
''',
'''
''' ],
    'tanh'          : [
'trigonometry', 'calculates the hyperbolic tangent of n',
'''
''',
'''
''' ],
    'tetrate'       : [
'powers_and_roots', 'tetrates n by k',
'''
''',
'''
''' ],
    'tetrahedral'   : [
'polyhedral_numbers', 'calculates the nth tetrahedral number',
'''
''',
'''
''' ],
    'tetranacci'    : [
'number_theory', 'calculates the nth Tetranacci number',
'''
''',
'''
''' ],
    'thabit'        : [
'number_theory', 'gets the nth Thabit number',
'''
''',
'''
''' ],
    'tounixtime'    : [
'conversion', 'converts from date-time list to Unix time (seconds since epoch)'
'''
''',
'''
''' ],
    'tower'     : [
'powers_and_roots', 'calculates list n as a power tower',
'''
''',
'''
''' ],
    'tower2'    : [
'powers_and_roots', 'calculates list n as a right-associative power tower',
'''
''',
'''
''' ],
    'trianglearea'  : [
'trigonometry', 'calculates the area of a triangle with sides of length a, b, and c'
'''
''',
'''
''' ],
    'triangular'    : [
'polygonal_numbers', 'calcuates the nth triangular number',
'''
''',
'''
''' ],
    'triangular?'   : [
'polygonal_numbers', 'finds the index of the triangular number of value n',
'''
''',
'''
''' ],
    'tribonacci'    : [
'number_theory', 'calculates the nth Tribonacci number',
'''
''',
'''
''' ],
    'triplebal'     : [
'prime_numbers', 'returns the first of the nth set of triple balanced primes',
'''
''',
'''
''' ],
    'triplebal_'    : [
'prime_numbers', 'returns the nth set of triple balanced primes',
'''
''',
'''
''' ],
    'tripletprime'  : [
'prime_numbers', 'returns the first of the nth set of triplet primes',
'''
''',
'''
''' ],
    'tripletprime'  : [
'prime_numbers', 'returns the nth set of triplet primes',
'''
''',
'''
''' ],
    'truncoct'      : [
'polyhedral_numbers', 'calculates the nth truncated octahedral number',
'''
''',
'''
''' ],
    'trunctet'      : [
'polyhedral_numbers', 'calculates the nth truncated tetrahedral number',
'''
''',
'''
''' ],
    'twinprime'     : [
'prime_numbers', 'returns the first of the nth set of twin primes',
'''
''',
'''
''' ],
    'twinprime_'    : [
'prime_numbers', 'returns the nth set of twin primes',
'''
''',
'''
''' ],
    'uchar'         : [
'conversion', 'converts the value to an unsigned 8-bit integer',
'''
''',
'''
''' ],
    'uinteger'      : [
'conversion', 'convert the value to an unsigned k-bit integer',
'''
''',
'''
''' ],
    'ulong'         : [
'conversion', 'converts the value to an unsigned 32-bit integer',
'''
''',
'''
''' ],
    'ulonglong'         : [
'conversion', 'converts the value to an unsigned 64-bit integer',
'''
''',
'''
''' ],
    'union'     : [
'list_operators', 'returns the union of two lists',
'''
''',
'''
''' ],
    'unique'    : [
'list_operators', 'replaces list n with a list of its unique elements',
'''
''',
'''
''' ],
    'unitroots'     : [
'number_theory', 'calculates the nth roots of unity',
'''
''',
'''
''' ],
    'unlist'    : [
'modifiers', 'expands list n to individual arguments',
'''
''',
'''
''' ],
    'unpack'    : [
'number_theory', 'unpack an integer value into bit fields',
'''
''',
'''
''' ],
    'ushort'        : [
'conversion', 'converts the value to an unsigned 16-bit integer',
'''
''',
'''
''' ],
    'xor'           : [
'logical', 'calculates the bitwise \'xor\' of n and k',
'''
''',
'''
''' ],
    'zero'          : [
'list_operators', 'returns a list of the indices of elements in list n that are zero',
'''
''',
'''
''' ],
    'zeta'          : [
'number_theory', 'calculates the zeta function for n',
'''
''',
'''
''' ],
    '_dumpalias'    : [
'internal', 'dumps the list of aliases for operators',
'''
''',
'''
''' ],
    '_dumpbal'      : [
'internal', 'dumps the cached list of balanced primes',
'''
''',
'''
''' ],
    '_dumpcousin'   : [
'internal', 'dumps the cached list of cousin primes',
'''
''',
'''
''' ],
    '_dumpdouble'   : [
'internal', 'dumps the cached list of double balanced primes',
'''
''',
'''
''' ],
    '_dumpiso'      : [
'internal', 'dumps the cached list of isolated primes',
'''
''',
'''
''' ],
    '_dumpops'      : [
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_dumpprimes'   : [
'internal', 'dumps the cached list of large primes',
'''
''',
'''
''' ],
    '_dumpquad'     : [
'internal', 'dumps the cached list of quadruplet primes',
'''
''',
'''
''' ],
    '_dumpquint'    : [
'internal', 'dumps the cached list of quintuplet primes',
'''
''',
'''
''' ],
    '_dumpsext'     : [
'internal', 'dumps the cached list of sextuplet primes',
'''
''',
'''
''' ],
    '_dumpsexy'     : [
'internal', 'dumps the cached list of sexy primes',
'''
''',
'''
''' ],
    '_dumpsmall'    : [
'internal', 'dumps the cached list of small primes',
'''
''',
'''
''' ],
    '_dumpsophie'   : [
'internal', 'dumps the cached list of Sophie Germain primes',
'''
''',
'''
''' ],
    '_dumptriple'   : [
'internal', 'dumps the cached list of triple balanced primes',
'''
''',
'''
''' ],
    '_dumptriplet'  : [
'internal', 'dumps the cached list of triplet primes',
'''
''',
'''
''' ],
    '_dumptwin'     : [
'internal', 'dumps the cached list of twin primes',
'''
''',
'''
''' ],
    '_importbal'    : [
'internal', 'imports balanced primes from file n',
'''
''',
'''
''' ],
    '_importcousin' : [
'internal', 'imports cousin primes from file n',
'''
''',
'''
''' ],
    '_importdouble' : [
'internal', 'imports double balanced primes from file n',
'''
''',
'''
''' ],
    '_importiso'    : [
'internal', 'imports isolated primes from file n',
'''
''',
'''
''' ],
    '_importprimes' : [
'internal', 'imports large primes from file n',
'''
''',
'''
''' ],
    '_importquad'   : [
'internal', 'imports quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importquint'  : [
'internal', 'imports quintuplet primes from file n',
'''
''',
'''
''' ],
    '_importsext'   : [
'internal', 'imports sextuplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy'   : [
'internal', 'imports sexy primes from file n',
'''
''',
'''
''' ],
    '_importsexy3'  : [
'internal', 'imports sexy triplet primes from file n',
'''
''',
'''
''' ],
    '_importsexy4'  : [
'internal', 'imports sexy quadruplet primes from file n',
'''
''',
'''
''' ],
    '_importsmall'  : [
'internal', 'imports small primes from file n',
'''
''',
'''
''' ],
    '_importsophie' : [
'internal', 'imports Sophie Germain primes from file n',
'''
''',
'''
''' ],
    '_importtriple' : [
'internal', 'imports triple balanced primes from file n',
'''
''',
'''
''' ],
    '_importtriplet': [
'internal', 'imports triplet primes from file n',
'''
''',
'''
''' ],
    '_importtwin'   : [
'internal', 'imports twin primes from file n',
'''
''',
'''
''' ],
    '_dumpops'      : [
'internal', 'lists all rpn operators',
'''
''',
'''
''' ],
    '_makebal'      : [
'internal', 'calculates and caches balanced primes',
'''
''',
'''
''' ],
    '_makecousin'   : [
'internal', 'calculates and caches cousin primes',
'''
''',
'''
''' ],
    '_makedouble'   : [
'internal', 'calculates and caches double balanced primes',
'''
''',
'''
''' ],
    '_makeiso'      : [
'internal', 'calculates and caches isolated primes',
'''
''',
'''
''' ],
    '_makeprimes'   : [
'internal', 'calculates and caches large primes',
'''
''',
'''
''' ],
    '_makequad'     : [
'internal', 'calculates and caches quaduplet primes',
'''
''',
'''
''' ],
    '_makequint'    : [
'internal', 'calculates and caches quintuplet primes',
'''
''',
'''
''' ],
    '_makesext'     : [
'internal', 'calculates and caches sextuplet primes',
'''
''',
'''
''' ],
    '_makesexy'     : [
'internal', 'calculates and caches sexy primes',
'''
''',
'''
''' ],
    '_makesexy3'    : [
'internal', 'calculates and caches sexy triplet primes',
'''
''',
'''
''' ],
    '_makesexy4'    : [
'internal', 'calculates and caches sexy quadruplet primes',
'''
''',
'''
''' ],
    '_makesmall'    : [
'internal', 'calculates and caches small primes',
'''
''',
'''
''' ],
    '_makesophie'   : [
'internal', 'calculates and caches Sophie Germain primes',
'''
''',
'''
''' ],
    '_makesuper'    : [
'internal', 'calculates and caches super primes',
'''
''',
'''
''' ],
    '_maketriple'   : [
'internal', 'calculates and caches triple balanced primes',
'''
''',
'''
''' ],
    '_maketriplet'  : [
'internal', 'calculates and caches triplet primes',
'''
''',
'''
''' ],
    '_maketwin'     : [
'internal', 'calculates and caches twin primes',
'''
''',
'''
''' ],
    '_stats'        : [
'internal', 'dumps rpn statistics',
'''
''',
'''
''' ],
    '~'             : [
'logical', 'calculates the bitwise negation of n',
'''
''',
'''
''' ],
#   'antitet'       : [ findTetrahedralNumber, 1 ],
#   'bernfrac'      : [ bernfrac, 1 ],
#   'powmod'        : [ getPowMod, 3 ],
}


#//******************************************************************************
#//
#//  makeHelp
#//
#//******************************************************************************

def makeHelp( basicCategories ):
    dataPath = os.path.abspath( os.path.realpath( __file__ ) + os.sep + '..' + os.sep + 'rpndata' )
    fileName = dataPath + os.sep + 'help.pckl.bz2'

    with contextlib.closing( bz2.BZ2File( fileName, 'wb' ) ) as pickleFile:
        pickle.dump( PROGRAM_VERSION, pickleFile )
        pickle.dump( basicCategories, pickleFile )
        pickle.dump( operatorHelp, pickleFile )


#//******************************************************************************
#//
#//  main
#//
#//******************************************************************************

def main( ):
    print( PROGRAM_NAME, PROGRAM_VERSION, '-', PROGRAM_DESCRIPTION )
    print( COPYRIGHT_MESSAGE )
    print( )

    makeHelp( basicCategories )


#//******************************************************************************
#//
#//  __main__
#//
#//******************************************************************************

if __name__ == '__main__':
    main( )

