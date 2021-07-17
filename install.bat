@echo off

REM This script will attempt to automatically install all the required dependencies found in requiments.txt using python
REM Please note that this script is not guaranteed to work on all systems and is provided as-is.
REM If you find any issues, please report them to the author.

REM Attenpt to start py launcher without relying on PATH
%SYSTEMROOT%\py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO attempt
%SYSTEMROOT%\py.exe -m pip install -r requirements.txt
GOTO end

REM Attempts to run pythong relying on PATH
:attempt
py.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO lastattempt
py.exe -m pip install -r requirements.txt
PAUSE
GOTO end

REM As a last resortm attempt to run whatever python there is
:lastattempt
python.exe --version > NUL 2>&1
IF %ERRORLEVEL% NEQ 0 GOTO message
python.exe pip install -r requirements.txt
PAUSE
GOTO end

:message
echo "Python was not found on your system. Please install python and try again."
PAUSE

:end
