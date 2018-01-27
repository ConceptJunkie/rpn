rem TCC script for building the RPN wheel and Windows installer

python setup.py bdist_wheel
python setup.py bdist_wininst

del /sxyz /nt build

