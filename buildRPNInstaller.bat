rem TCC script for building the RPN installer

setlocal

if not exist installer_dist mkdir installer_dist

if exist version.txt rm version.txt

echos VERSION= > version.txt
type rpn\rpnVersion.py | grep "PROGRAM_VERSION =" | cut -d"'" -f2 >> version.txt

set /r version.txt

"%PROG32_DIR%\Inno Setup 6\ISCC.exe" rpn64.iss
move Output\setup_rpnChilada.exe "dist\setup_rpnChilada-%VERSION%-win64.exe"

del /sxyz /nt build
del /sxyz /nt Output

del version.txt

endlocal

