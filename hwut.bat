@ECHO OFF

REM ___________________________________________________________________________
REM START: The following has been copied and modified from the QUEX
REM        OpenSource Project.
where /q python.exe 
IF %ERRORLEVEL% NEQ 0 (
   echo NOTE: 'python.exe' not found in system's PATH!
   echo NOTE: Please, set the environment variable.
   if EXIST "C:\Python27\python.exe" (
      echo NOTE: Found it in "C:\Python27".
      echo NOTE: Assume "C:\Python27\" to be correct.
      set PATH=C:\Python27;"%PATH%"
      echo PATH
      echo "%PATH%"
   ) else (
      echo ERROR:
      echo ERROR: Cannot execute hwut.
      echo ERROR:
      exit /B   
   )
)
REM END 
REM ___________________________________________________________________________

REM (*) HWUT_PATH 
REM     (Find the path name of the directory of THIS batch file).
for %%F in ("%~pd0") do set x_path=%%~dpF

REM Delete trailing backslash
if %x_path:~-1%==\ SET x_path=%x_path:~0,-1%

setlocal enabledelayedexpansion
set HWUT_PATH=%x_path%

python "%HWUT_PATH%\hwut-exe.py" %*
