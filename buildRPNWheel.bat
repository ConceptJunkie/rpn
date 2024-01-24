rem TCC script for building the RPN wheel

del dist\*.whl
del dist\*.gz

python makeUnits.py
python makeHelp.py

python setup.py sdist bdist_wheel

del /sxyz /nt rpnChilada.egg-info
del /sxyz /nt build

