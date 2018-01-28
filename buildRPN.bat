rem TCC script for building the RPN wheel and Windows installer

python setup.py bdist_wheel

del /sxyz /nt build
del /sxyz /nt rpn.egg-info

