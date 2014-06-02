rpn is a command-line Reverse-Polish Notation calculator.  It supports
arithmetic with arbitrary precision, powers and roots, logarithms, alegbraic
functions (including polynomials arithmetic and solving),  trigonometric
functions, complex nunmbers, computer science related functions (bitwise math,
base conversion), number theory functions, prime number calculations and lookup,
and can operate with single operands or lists of operands and supports a wide
variety of flexible unit conversions comparable to the GNU units program.

rpn is written for Python 3, and requires the mpmath and pyprimes libraries for
most of the really hard math stuff.  It's a work in progress, and at any
particular time, parts of it might be broken, although I try to not let this go
on for too long.

Getting Started:

If you have pip installed, you can install the prerequisites with the
following:

pip install pyprimes

pip install mpmath

pip install gmpy2

Before running rpn, you should run makeHelp.py and makeUnits.py to generate the
data files that rpn uses for displaying help and doing unit conversions
respectively.

rpn.py is the calculator itself.  It has pretty extensive built-in help (and
naturally for something written by its only user, a lot of it isn't filled in
yet).  Try 'rpn help' to start.

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 5.11.0 isn't finished as a standalone program). The data
files are stored in the same location as rpn.py in a subdirectory called
rpndata/.  Until I fix this, if you really want to generate prime numbers, go
back to version 4 and check out the '_make*' commands.

rpn doesn't try to replace any existing tools.  It's just something I wrote for
fun that ended up being a lot more useful and powerful than I originally
envisioned.

Rick Gutleber
rickg@his.com

p.s. rpn is licensed under the GNU GPL verison 3.0.  See (see
<http://www.gnu.org/licenses/gpl.html> for more information).

