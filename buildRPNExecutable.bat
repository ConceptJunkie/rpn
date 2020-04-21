rem TCC script for building the RPN installer

setlocal

echos VERSION= > version.txt
type rpn\rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

set /r version.txt
set TCL_LIBRARY=C:\app\python38\tcl\tcl8.6
set TK_LIBRARY=C:\app\python38\tcl\tk8.6

python setup_rpn.py build_exe

copy rpn\rpndata\de405.bsp build\exe.win-amd64-3.8\
copy rpn\rpndata\de421.bsp build\exe.win-amd64-3.8\

del version.txt

endlocal

