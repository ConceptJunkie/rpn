#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpn.py
# //
# //  RPN command-line calculator, setup script
# //  copyright (c) 2015 (1988), Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //******************************************************************************

import os

from setuptools import setup, find_packages

import rpnGlobals as g

def read( *paths ):
    """Build a file path from *paths* and return the contents."""
    with open( os.path.join( *paths ), 'r') as f:
        return f.read( )

setup(
    name = 'rpn',
    version = '6.5.0',
    description = 'command-line RPN calculator with arbitrary precision',
    long_description = 'TODO: write long description!',
    #long_description = ( read( 'README.rst' ) + '\n\n' +
    #                     read( 'HISTORY.rst' ) + '\n\n' +
    #                     read( 'AUTHORS.rst' ) ),
    url = 'http://github.com/ConceptJunkie/rpn/',
    license = 'GPL3',
    author = 'Rick Gutleber',
    author_email = 'rickg@his.com',
    py_modules = [ 'rpn',
                   'rpnCombinatorics',
                   'rpnComputer',
                   'rpnConstants',
                   'rpnDate',
                   'rpnDeclarations',
                   'rpnEstimates',
                   'rpnFactor',
                   'rpnGeometry',
                   'rpnGlobals',
                   'rpnList',
                   'rpnMath',
                   'rpnMeasurement',
                   'rpnModifiers',
                   'rpnName',
                   'rpnNumberTheory',
                   'rpnOperators',
                   'rpnOutput',
                   'rpnPolynomials',
                   'rpnPolytope',
                   'rpnPrimeUtils',
                   'rpnPrimes',
                   'rpnTime',
                   'rpnUnits',
                   'rpnUtils',
                   'rpnVersion' ],
    install_requires = open( 'requirements.txt' ).read( ).splitlines( ),
    include_package_data = True,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Environment :: Console',
    ],
    data_files = [ ( 'data_files', [ g.DataDir + os.sep + 'balanced_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'cousin_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'double_balanced_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'help.pckl.bz2',
                                     g.DataDir + os.sep + 'isolated_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'large_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'quad_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'quint_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'sext_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'sexy_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'sexy_quadruplets.pckl.bz2',
                                     g.DataDir + os.sep + 'sexy_triplets.pckl.bz2',
                                     g.DataDir + os.sep + 'small_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'sophie_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'super_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'triple_balanced_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'triplet_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'twin_primes.pckl.bz2',
                                     g.DataDir + os.sep + 'unit_conversions.pckl.bz2',
                                     g.DataDir + os.sep + 'unit_help.pckl.bz2',
                                     g.DataDir + os.sep + 'units.pckl.bz2' ] ) ],
    packages = find_packages( exclude = [ 'test*', 'setup_*', 'makeRPNPrimes*' ] ),
)

