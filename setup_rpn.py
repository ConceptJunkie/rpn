from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = \
    dict(
        packages = [ ],
        excludes = [ ],
        include_files = [
            'rpndata/help.pckl.bz2',
            'rpndata/unit_conversions.pckl.bz2',
            'rpndata/units.pckl.bz2'
        ] )

base = 'Console'

executables = [
    Executable( 'rpn.py', base = base )
]

setup( name='rpn', version = '5.20.2', description = 'command-line RPN calculator',
       options = dict( build_exe = buildOptions ), executables = executables )

