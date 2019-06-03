from cx_Freeze import setup, Executable
from rpn.rpnVersion import PROGRAM_VERSION

import rpn.rpnGlobals as g

import os

# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = \
    dict(
        packages = [
            'pkg_resources._vendor',
        ],

        include_files = [
            "rpn" + os.sep + g.dataDir + os.sep + 'units.pckl.bz2',
            "rpn" + os.sep + g.dataDir + os.sep + 'unit_conversions.pckl.bz2',
            "rpn" + os.sep + g.dataDir + os.sep + 'unit_help.pckl.bz2',
            "rpn" + os.sep + g.dataDir + os.sep + 'unit_names.pckl.bz2',
            "rpn" + os.sep + g.dataDir + os.sep + 'deltat.data',
            "rpn" + os.sep + g.dataDir + os.sep + 'deltat.preds',
            "rpn" + os.sep + g.dataDir + os.sep + 'Leap_Second.dat',
        ],

        include_msvcr = 1,
        optimize = 2,
    )

executables = [
    Executable( script = 'rpn.py',
                base = None,
                icon = 'rpn.ico',
                initScript = None,
                shortcutName = 'rpnChilada ' + PROGRAM_VERSION,
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

