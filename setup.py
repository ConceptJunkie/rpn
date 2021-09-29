#!/usr/bin/env python

#******************************************************************************
#
#  setup.py
#
#  rpnChilada setup script for the rpnChilada wheel
#  copyright (c) 2018, Rick Gutleber (rickg@his.com)
#
#  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
#  information).
#
#******************************************************************************

requirements = 'requirements.txt'
rpndata = 'rpndata'

import os
import glob

from setuptools import setup, find_packages
from rpn.rpnVersion import PROGRAM_VERSION_NAME


def read( *paths ):
    '''Build a file path from *paths* and return the contents.'''
    with open( os.path.join( *paths ), 'r' ) as f:
        return f.read( )


setup(
    name = 'rpnChilada',
    version = PROGRAM_VERSION_NAME,
    description = 'command-line RPN calculator',
    long_description =
'''
rpnChilada is a command-line Reverse-Polish Notation calculator that was
first written in C in 1988 as a four-function calculator.

It was rewritten in Python 3 in 2012 and now uses the mpmath library.  It
was a Python learning exercise for me, and a fun little toy, but when I
found mpmath, it became really cool and powerful, so props to Fredrik
Johansson, who did most of the heavy lifting (http://mpmath.org).

rpnChilada gives you the whole enchilada when it comes to playing with
numbers.  You get math functions, algebra functions, combinatoric functions,
number theory functions, astronomy functions, physics functions, unit
conversions (comparable to GNU Units) and much, much more.   There are over
1000 unique operators.  rpnChilada supports lists, but not matrices.

rpnChilada comes with integrated help, which isn't complete, but has at
least a basic description of every operator, and over 2400 built-in
examples.  Help now includes descriptions for constants and units as well,
although a lot of these still need to be filled in.

rpnChilada also comes with an extensive test suite, which is being constantly
improved.  Many of the functions are validated against the OEIS.

Version 8 represents a major overhaul of the unit conversion code.  Unit
conversion is now significantly smarter than it used to be, and intermediate
conversions are no longer necessary.

There are still bugs, and since it's a one-person side project, progress
is slow, but bug reports and feature requests are welcome at rickg@his.com.

Note, Windows users will want the Windows-specific wheels for pyephem and
gmpy2:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyephem

https://www.lfd.uci.edu/~gohlke/pythonlibs/#gmpy

Linux users will need the development versions of the GMP, MPC and MFPR
libraries.

rpnChilada can be launched with 'rpnChilada' or 'rpn' in the Python Scripts/
directory.

For a quick primer on rpnChilada's use, try "rpn help examples".  Please note
that the OEIS integration and geographic location functions require Internet
access.
''',

    url = 'http://github.com/ConceptJunkie/rpn/',
    license = 'GPL3',
    author = 'Rick Gutleber',
    author_email = 'rickg@his.com',

    install_requires = open( requirements ).read( ).splitlines( ),

    include_package_data = True,

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',        
        'Topic :: Scientific/Engineering :: Mathematics',
        'Environment :: Console',
    ],

    packages = find_packages( ),
    py_modules = [ os.path.splitext( os.path.basename( i ) )[ 0 ] for i in glob.glob( "*.py" ) ],

    # This maps the directories to the installed location under site-packages/
    package_dir = { '.' : 'rpn' },

    entry_points = {
        'console_scripts': [
            'rpn = rpn.rpn:main',
            'rpnChilada = rpn.rpn:main',
            'rpnMakeHelp = rpn.makeHelp:main',
            'rpnMakeUnits = rpn.makeUnits:main',
            #'rpnPreparePrimeData = rpn.preparePrimeData:main',
            'testRPN = rpn.testRPN:main',
        ],
    }
)

