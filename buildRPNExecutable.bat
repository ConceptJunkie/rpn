rem TCC script for building the RPN installer

setlocal

echos VERSION= > version.txt
type rpn\rpnVersion.py | grep PROGRAM_VERSION | cut -d"'" -f2 >> version.txt

set /r version.txt
set TCL_LIBRARY=C:\app\python38\tcl\tcl8.6
set TK_LIBRARY=C:\app\python38\tcl\tk8.6

python setup_rpn.py build_exe

copy rpn\rpndata\finals2000A.all build\exe.win-amd64-3.9\
copy rpn\rpndata\de421.bsp build\exe.win-amd64-3.9\

del version.txt

endlocal

