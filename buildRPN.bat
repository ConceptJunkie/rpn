rem TCC script for building the RPN wheel

mkdir rpn
copy *.py rpn

mkdir rpn\rpndata
copy rpndata\*.txt rpn\rpndata

python setup.py bdist_wininst

del /sxyz /nt build
del /sxyz /nt rpn

