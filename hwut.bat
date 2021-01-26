REM  SPDX license identifier: LGPL-2.1
REM 
REM  Copyright (C) Frank-Rene Schaefer, private.
REM  Copyright (C) Frank-Rene Schaefer, 
REM                Visteon Innovation&Technology GmbH, 
REM                Kerpen, Germany.
REM 
REM  This file is part of "HWUT -- The hello worldler's unit test".
REM 
REM                   http://hwut.sourceforge.net
REM 
REM  This file is free software; you can redistribute it and/or
REM  modify it under the terms of the GNU Lesser General Public
REM  License as published by the Free Software Foundation; either
REM  version 2.1 of the License, or (at your option) any later version.
REM 
REM  This file is distributed in the hope that it will be useful,
REM  but WITHOUT ANY WARRANTY; without even the implied warranty of
REM  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
REM  Lesser General Public License for more details.
REM 
REM  You should have received a copy of the GNU Lesser General Public
REM  License along with this file; if not, write to the Free Software
REM  Foundation, Inc., 51 Franklin Street, Fifth Floor,
REM  Boston, MA 02110-1301 USA
REM 
REM ------------------------------------------------------------------------------

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
