rpn is a command-line Reverse-Polish Notation calculator.

I first wrote a very simple version of rpn way back in 1988 when I was first
learning C.  In the summer of 2012 when I was starting to explore Python, I
figured this was a great project for first Python program to write.  rpn was
something I still continued to use pretty regularly, and even though I'd
rewritten the original C rpn program in C++ a few years later, it was still a
very simple program that was essentially a 4-function command line calculator
and that's all.

However, starting with version 2, thanks to the embarrassment of riches to be
found among the libraries available for Python, and the language itself, rpn
ended up growing to become something really cool and a lot more useful and fun
than I would have guess when I started it just as an excuse to do something in
Python.

rpn is written for Python 3, and requires the mpmath and pyprimes libraries.
It's a work in progress, and at any particular time, parts of it might be
broken, although I try to not let this go on for too long.

Getting Started:

rpn.py is the calculator itself.  It has pretty extensive built-in help (and
naturally for something written by its only user, a lot of it isn't filled in
yet).

Before running rpn, you should run makeHelp.py and makeUnits.py to generate the
data files that rpn uses for displaying help and doing unit conversion
respectively.

makeRPNPrimes.py consists of a bunch of functions for pre-calculating and
caching different kinds of prime numbers that was recently pulled out of rpn.py
(and as of version 5.11.0 isn't finished as a standalone program). The data
files are stored in the same location as rpn.py in a subdirectory called
rpndata/.

There are plenty of tools out there that are as nice as this one, and
definitely plenty that are far more powerful and polished (and bug-free), but
if one person finds this code and has fun with it, then it's worth the trouble
of sharing it.

Rick Gutleber
rickg@his.com

p.s. rpn is licensed under the GNU GPL verison 3.0.  See (see
<http://www.gnu.org/licenses/gpl.html> for more information).

