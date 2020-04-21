rem TCC script for building the RPN installer

setlocal

if not exist mkdir dist

if exist version.txt rm version.txt

echos VERSION= > version.txt
type rpn\rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

set /r version.txt

iff %_X64 eq 1 then
    "%PROG32_DIR%\Inno Setup 5\ISCC.exe" rpn64.iss
    move Output\setup_rpnChilada.exe "dist\setup_rpnChilada-%VERSION%-win64.exe"
else
    copy msvcp100-win32.dll build\exe.win32-3.6\msvcp100.dll
    "%PROG32_DIR%\Inno Setup 5\ISCC.exe" rpn32.iss
    move Output\setup_rpnChilada.exe "dist\setup_rpnChilada-%VERSION%-win32.exe"
endiff

rem del /sxyz /nt build
rem del /sxyz /nt Output

del version.txt

endlocal

