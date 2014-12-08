rem TCC script for building the RPN installer

setlocal
pushd
call d r

echos VERSION= > version.txt
type rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

set /r version.txt

python setup_rpn.py build_exe

iff %_X64 eq 1 then
    "%PROG32_DIR%\Inno Setup 5\ISCC.exe" rpn64.iss
    move Output\setup_rpn.exe "%RPN_TARGET%\setup_rpn-%VERSION%-win64.exe"
else
    "%PROG32_DIR%\Inno Setup 5\ISCC.exe" rpn32.iss
    move Output\setup_rpn.exe "%RPN_TARGET%\setup_rpn-%VERSION%-win32.exe"
endiff

del /sxyz /nt build
del /sxyz /nt Output

del version.txt

popd
endlocal

