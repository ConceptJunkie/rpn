rem //******************************************************************************
rem //
rem //  BackupRPN
rem //
rem //  This TCC script is used to backup RPN.   It assumes Cygwin is installed.
rem //
rem //******************************************************************************

setlocal

iff "%1" == "" then
    echo usage:  BackupRPN target_dir_list [versioned_target_dir_list]
	quit
endiff

rem set VERSION=%@execstr[grep "PROGRAM_VERSION " rpn\rpnVersion.py | cut -d' ' -f3  | tr -d -c 01234567890.]
set RPN_FILES=__init__.py;rpn*.py;makeHelp.py;makeRPNPrimes.py;makeUnits.py;setup_rpn.py;test*.py;profile*.py;rpn.ico;rpn32.iss;rpn64.iss;BuildRPN.bat;BuildRPNInstaller.bat;requirements.txt;setup.cfg;MANIFEST.in;setup.py;unpickle.py;preparePrimeData.py;BackupRPN.bat;rpn.py;makeHelp.py;makeUnits.py;preparePrimes.py;testRPN.py;README.md;pylintrc

echo %VERSION

for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR for %FILE in (%RPN_FILES) copy %FILE %TARGET_DIR

cd rpn
echo on
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR for %FILE in (%RPN_FILES) copy %FILE %TARGET_DIR%\rpn

cd math
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py factorise.py %TARGET_DIR%\rpn\math
cd ..

cd science
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py %TARGET_DIR%\rpn\science
cd ..

cd special
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py %TARGET_DIR%\rpn\special
cd ..

cd test
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py test*.py %TARGET_DIR%\rpn\test
cd ..

cd time
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py %TARGET_DIR%\rpn\time
cd ..

cd units
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py %TARGET_DIR%\rpn\units
cd ..


cd util
for /t; %TARGET_DIR in (%1) if exist %TARGET_DIR .and. isdir %TARGET_DIR copy rpn*.py %TARGET_DIR%\rpn\util
cd ..

cd ..

endlocal

