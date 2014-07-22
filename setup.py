from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = \
    dict( packages = [ ],
          excludes = [ ],
          include_files = [ 'rpndata/balanced_primes.pckl.bz2',
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
                            'rpndata/units.pckl.bz2' ]
           )

base = 'Console'

executables = [
    Executable( 'rpn.py', base = base )
]

setup( name='rpn', version = '5.20.1', description = 'command-line RPN calculator',
       options = dict( build_exe = buildOptions ), executables = executables )

