import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = \
    dict(
        packages = [ ],
        excludes = [ ],
        include_files = [
            'rpndata/balanced_primes.pckl.bz2',
            'rpndata/cousin_primes.pckl.bz2',
            'rpndata/double_balanced_primes.pckl.bz2',
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
            'rpndata/twin_primes.pckl.bz2' ] )

base = 'Console'

executables = [
    Executable( 'makeRPNPrimes.py', base = base )
]

if 'bdist_msi' in sys.argv:
    sys.argv += [ '--initial-target-dir', 'c:\\Program Files\\rpn' ]

setup( name='rpnprimes', version = '5.20.2', description = 'command-line RPN calculator prime number data files',
       options = dict( build_exe = buildOptions ), executables = executables )

