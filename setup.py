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

setup (
    name = 'rpn',
    version = PROGRAM_VERSION_NAME,
    #description = 'command-line RPN calculator with arbitrary precision',
    description = 'command-line RPN calculator',
#    long_description =
#'''
#rpn is a command-line Reverse-Polish Notation calculator that was first
#written in C in 1988 as a four-function calculator.  It was rewritten in
#Python 3 in 2012 and now uses the mpmath library.  It was a Python learning
#exercise for me, and a fun little toy, but when I found mpmath, it became
#really cool and powerful, so props to Fredrik Johansson, who did all the
#heavy lifting (http://mpmath.org).
#''',

    long_description =
'''
rpn is a command-line Reverse-Polish Notation
calculator with over 700 operators, based
on mpmath (props to Fredrik Johansson,
http://mpmath.org).
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

    data_files = [ ( 'Lib/site-packages/rpn/' + rpndata,
                              [ 'rpn' + os.sep + g.dataDir + os.sep + 'balanced_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'cousin_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'double_balanced_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'huge_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'isolated_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'large_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'quad_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'quint_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'sext_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'sexy_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'sexy_quadruplets.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'sexy_triplets.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'small_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'sophie_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'super_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'triple_balanced_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'triplet_primes.txt',
                                'rpn' + os.sep + g.dataDir + os.sep + 'twin_primes.txt' ] ) ],

    entry_points = {
        'console_scripts': [
            'rpn = rpn:__main__',
            'makeHelp = makeHelp:__main__',
            'makeUnits = makeUnits:__main__',
            'preparePrimeData = preparePrimeData:__main__',
            'testRPN = rpn.testRPN:__main__',
        ],
    }
)

