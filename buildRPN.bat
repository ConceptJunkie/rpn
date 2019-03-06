rem TCC script for building the RPN wheel

del dist\*.whl
del dist\*.gz
rem del rpn\rpndata\oeis.cache
rem del rpn\rpndata\locations.pckl.bz2

rem python makeUnits.py
rem python makeHelp.py

python setup.py sdist bdist_wheel

del /sxyz /nt rpnChilada.egg-info

