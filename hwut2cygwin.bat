@ECHO OFF
REM PURPOSE:
REM
REM Calling HWUT from DOS/Windows on test files which have been developed in a
REM Unix environment.
REM
REM This script calls HWUT through a cygwin environment. All arguments normally
REM passed to HWUT can be passed to this script. Then, the control is passed to  
REM a cygwin shell. From there the script
REM
REM                          HWUT_PATH/hwut2cygwin.sh
REM
REM is executed. It receives the path of the current working directory and the 
REM arguments which have been passed to this script. Inside, HWUT is setup 
REM and then the application is run.
REM
REM REQUIRES:
REM
REM * HWUT_CYGWIN_DIR: the directory of the desired cygwin installation.
REM
REM * PATH: better contains the directory of this file. This way, the script 
REM         can easily be called from the command line.
REM
REM Author: Frank-Rene Schaefer, 2014.
REM ____________________________________________________________________________
IF "%HWUT_CYGWIN_PATH%"=="" goto NO_WE_CANT

REM (*) Current working directory
set work_path=%CD:\=\\%

REM (*) HWUT_PATH 
REM     (Find the path name of the directory of THIS batch file).
for %%F in (%~pd0) do set hwut_path=%%~dpF
set hwut_path=%hwut_path:\=\\%

REM Location of the 'cygpath' utility. That is the utility which we need to 
REM reformat DOS file names into CygWin file names.
set cygpath_util="/usr/bin/cygpath"

REM (*) CYGWIN!
%HWUT_CYGWIN_PATH%\bin\bash.exe --login -i -c "$(%cygpath_util% %hwut_path:\=\\%)\hwut2cygwin.sh $(%cygpath_util% %work_path:\=\\%) %*"
goto YES_WE_COULD

REM ___________________________________________________________________________
REM
:NO_WE_CANT
   ECHO ----------------------------------------------------------------------
   ECHO 'HWUT_CYGWIN_PATH' environment variable must be defined!
   ECHO It must point to the directory of the cygwin installation to be used.
   ECHO ----------------------------------------------------------------------
:YES_WE_COULD
pause
