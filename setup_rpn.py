from cx_Freeze import setup, Executable
from rpnVersion import PROGRAM_VERSION

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = \
    dict(
        packages = [ ],
        excludes = [ ],
        include_files = [
            'rpndata/help.pckl.bz2',
            'rpndata/units.pckl.bz2',
            'rpndata/unit_conversions.pckl.bz2'
        ]
    )

base = 'Console'

executables = [
    Executable( 'rpn.py', base = base )
]

setup( name='rpn', version = PROGRAM_VERSION, description = 'command-line RPN calculator',
       options = dict( build_exe = buildOptions ), executables = executables )

