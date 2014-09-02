rpn is a command-line Reverse-Polish Notation calculator.

It supports arithmetic with arbitrary precision, powers and roots, logarithms,
alegbraic functions (including polynomials arithmetic and solving),
trigonometric functions, complex nunmbers, computer science related functions
(bitwise math, base conversion), number theory functions, prime number
calculations and lookup, and can operate with single operands or lists of
operands and supports a wide variety of flexible unit conversions comparable to
the GNU units program.

Installers for Windows can be found here:

https://www.strongspace.com/conceptjunkie/public/rpn-5.23.1-win32.msi
https://www.strongspace.com/conceptjunkie/public/rpn-5.23.1-amd64.msi

rpn is a console app and must be launched from the command-line.  The installer
includes the compiled help file, unit conversion tables and prime number lookup
tables.  The installer does not add rpn.exe to the Windows path, so a batch
file or alias will be useful for launching it.

Running RPN using the source:

rpn is written in Python 3, and requires the mpmath, pyprimes and arrow
libraries for most of the hard math stuff (gmpy2 is optional).

If you have pip installed, you can install the prerequisites with the
following:

    pip install pyprimes
    pip install mpmath
    pip install gmpy2
    pip install arrow

Before running rpn, you should run makeHelp.py and makeUnits.py to generate
the data files that rpn uses for displaying help and doing unit conversions
respectively.

Using rpn:

rpn is very easy to use.  It's just like any RPN calculator:  Operands go first,
then the operators.

For instance:

    rpn 2 2 +

will calculate 2 + 2.  "rpn _dumpops" is an internal command that will list
all the implemented operators for the curious.  They are also listed in the
help text.

rpn has pretty extensive built-in help, although not all the help files are
complete yet.

Start with "rpn help" for an overview.  To dive right in, see "rpn help
examples".

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 5.20.0 isn't finished as a standalone program).

The data files are stored in the same location as rpn.py in a subdirectory
called rpndata/.  In the Windows installer version, they are stored in the same
directory as the EXE.

Until I fix makeRPNPrimes.py, if you really want to generate prime numbers, go
back to version 4 and check out the '_make*' commands.

rpn also provides a simple interface for querying The On-Line Encyclopedia of
Integer Sequences (http://oeis.org).

Feedback, Comments, Bug Reports:

Any feedback is welcome at rickg@his.com.  This was originally an exercise to
learn Python, but slowly blossomed into something really useful and fun, so I
wanted to share it.  rpn also exposes just a few of the features of the amazing
mpmath library (by Fredrik Johansson, http://mpmath.org/) which is where all
the hard stuff is actually done.

Rick Gutleber
rickg@his.com

p.s. rpn is licensed under the GNU GPL verison 3.0.  See (see
<http://www.gnu.org/licenses/gpl.html> for more information).

