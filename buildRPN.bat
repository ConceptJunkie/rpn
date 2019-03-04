rem TCC script for building the RPN wheel

del dist\*.whl
del dist\*.gz

python setup.py sdist bdist_wheel

del /sxyz /nt build
del /sxyz /nt rpnChilada.egg-info

