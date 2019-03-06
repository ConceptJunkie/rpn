rem TCC script for building the RPN wheel

del dist\*.whl
del dist\*.gz
del rpn\rpndata\oeis.cache
del rpn\rpndata\locations.pckl.bz2

python makeUnits.py
python makeHelp.py

python setup.py sdist bdist_wheel

del /sxyz /nt rpnChilada.egg-info

