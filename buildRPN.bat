rem TCC script for building the RPN installer

setlocal
pushd
call d r

echos VERSION= > version.txt
type rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

set /r version.txt

python setup_rpn.py build_exe
"C:\Program Files\Inno Setup 5\ISCC.exe" rpn.iss

iff %_X64 eq 1 then
    move Output\setup_rpn.exe "%RPN_TARGET%\setup_rpn-%VERSION%-win64.exe"
else
    move Output\setup_rpn.exe "%RPN_TARGET%\setup_rpn-%VERSION%-win32.exe"
endiff

del /sxyz /nt build
del /sxyz /nt Output

del version.txt

popd
endlocal

