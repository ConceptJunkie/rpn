import os

from setuptools import setup, find_packages

setup(
    data_files = [ ( 'data_files', [ 'rpndata/balanced_primes.pckl.bz2',
                                     'rpndata/cousin_primes.pckl.bz2',
                                     'rpndata/double_balanced_primes.pckl.bz2',
                                     'rpndata/help.pckl.bz2',
                                     'rpndata/isolated_primes.pckl.bz2',
                                     'rpndata/large_primes.pckl.bz2',
                                     'rpndata/quad_primes.pckl.bz2',
                                     'rpndata/quint_primes.pckl.bz2',
                                     'rpndata/sext_primes.pckl.bz2',
                                     'rpndata/sexy_primes.pckl.bz2',
                                     'rpndata/sexy_quadruplets.pckl.bz2',
                                     'rpndata/sexy_triplets.pckl.bz2',
                                     'rpndata/small_primes.pckl.bz2',
                                     'rpndata/sophie_primes.pckl.bz2',
                                     'rpndata/super_primes.pckl.bz2',
                                     'rpndata/triple_balanced_primes.pckl.bz2',
                                     'rpndata/triplet_primes.pckl.bz2',
                                     'rpndata/twin_primes.pckl.bz2',
                                     'rpndata/unit_conversions.pckl.bz2',
                                     'rpndata/unit_help.pckl.bz2',
                                     'rpndata/units.pckl.bz2' ] ) ],
    packages = find_packages( exclude = [ 'test*', 'setup_*', 'makeRPNPrimes*' ] ),
)

def read( *paths ):
    """Build a file path from *paths* and return the contents."""
    with open( os.path.join( *paths ), 'r') as f:
        return f.read( )

setup(
    name = 'rpn',
    version = '6.5.0',
    description = 'command-line RPN calculator with arbitrary precision',
    long_description = 'TODO: write long description!',
    #long_description=( read( 'README.rst' ) + '\n\n' +
    #                   read( 'HISTORY.rst' ) + '\n\n' +
    #                   read( 'AUTHORS.rst' ) ),
    url = 'http://github.com/ConceptJunkie/rpn/',
    license = 'GPL3',
    author = 'Rick Gutleber',
    author_email = 'rickg@his.com',
    py_modules = [ 'rpn' ],
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
)

