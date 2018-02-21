#!/usr/bin/env python

# //******************************************************************************
# //
# //  setup.py
# //
# //  RPN command-line calculator, setup script
# //  copyright (c) 2018, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

requirements = 'requirements.txt'
rpndata = 'rpndata'

import os
import glob

from setuptools import setup, find_packages
from rpn.rpnVersion import PROGRAM_VERSION_NAME

import rpn.rpnGlobals as g

def read( *paths ):
    '''Build a file path from *paths* and return the contents.'''
    with open( os.path.join( *paths ), 'r') as f:
        return f.read( )

setup(
    name = 'rpnChilada',
    version = PROGRAM_VERSION_NAME,
    #description = 'command-line RPN calculator with arbitrary precision',
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
number theory functions, astronomy functions, extensive unit conversions
and much, much more.   rpnChilada supports lists, but not matrices.

rpnChilada comes with integrated help, which isn't complete, but has at
least a basic description of every function, and over 1200 built-in
examples.

rpnChilada also comes with a fairly extensive test suite, which is being
constantly improved.

There are still bugs, and since it's a one-person side-project, progress
is slow, but bug reports and feature requests are welcome at rickg@his.com.

Version 7 has been in the works for more than two and a half years, and the
number of operators since version 6.4 has increased by at least 200.  It also
supports user-defined variables and functions.
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
            #'makeRPNHelp = rpn.makeHelp:main',
            #'makeRPNUnits = rpn.makeUnits:main',
            #'prepareRPNPrimeData = rpn.preparePrimeData:main',
            'testRPN = rpn.testRPN:main',
        ],
    }
)

