setlocal
pushd
call d r

echos VERSION= > version.txt
type rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

python setup_rpn.py build_exe
"C:\Program Files\Inno Setup 5\ISCC.exe" rpn.iss

move Output\setup_rpn.exe "e:\download\setup_rpn-%VERSION%-win32.exe"

del /sxyz /nt build
del /sxyz /nt Output

del version.txt

popd
endlocal

