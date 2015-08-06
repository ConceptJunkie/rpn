from cx_Freeze import setup, Executable
from rpnVersion import PROGRAM_VERSION

import rpnGlobals as g

import os

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = \
    dict(
        packages = [ 'gmpy2', 'matplotlib', 'numpy', 'pylab' ],

        include_files = [
            g.DataDir + os.sep + 'balanced_primes.pckl.bz2',
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
            g.DataDir + os.sep + 'triplet_primes.pckl.bz2',
            g.DataDir + os.sep + 'triple_balanced_primes.pckl.bz2',
            g.DataDir + os.sep + 'twin_primes.pckl.bz2'
            g.DataDir + os.sep + 'units.pckl.bz2',
            g.DataDir + os.sep + 'unit_conversions.pckl.bz2',
            g.DataDir + os.sep + 'unit_help.pckl.bz2',
        ],

        include_msvcr = 1,
        optimize = 2,
    )

executables = [
    Executable( script = 'rpn.py',
                base = None,
                icon = 'rpn.ico',
                initScript = None,
                shortcutName = 'rpn ' + PROGRAM_VERSION,
                targetName = 'rpn.exe'
    )
]

setup( name = 'rpn',
       version = PROGRAM_VERSION,
       author = 'Rick Gutleber',
       author_email = 'rickg@his.com',
       description = 'command-line RPN calculator',
       options = dict( build_exe = buildOptions ),
       executables = executables
)

