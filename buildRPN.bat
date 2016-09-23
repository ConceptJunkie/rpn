rem TCC script for building the RPN wheel

mkdir src\rpn
copy *.py src\rpn

mkdir src\rpn\data
copy rpndata\*.txt src\rpn\data

python setup.py bdist_wheel

del /sxyz /nt build
del /sxyz /nt src

