::ELEVATE THE SCRIPT

@echo off
setlocal enabledelayedexpansion

:: If the script was run with a directory argument, change to that directory
if not "%~1"=="" (
    cd /d %~1
)

:: Check for admin rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If not admin
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %CD%", "", "runas", 1 >> "%temp%\getadmin.vbs"
    
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

::ACTUAL SCRIPT 

@echo off

REM Check if the virtual environment already exists
if not exist "venv\" (
    echo Preparing a virtual environment...

:: Unzip python-3.8.0-embed-win32_modified.zip to python-3.8.0-embed-win32_modified directory
    tar -xf python-3.8.0-embed-win32_modified.zip 

:: Install pip
    python-3.8.0-embed-win32_modified\python.exe get-pip.py 
:: Upgrade pip
    python-3.8.0-embed-win32_modified\Scripts\pip.exe install --upgrade pip

:: Install Pillow using only binaries
    python-3.8.0-embed-win32_modified\Scripts\pip.exe install Pillow --only-binary=:all:

:: Install wheel
    python-3.8.0-embed-win32_modified\Scripts\pip.exe install wheel

:: Install virtualenv
    python-3.8.0-embed-win32_modified\Scripts\pip.exe install virtualenv

:: Create a virtual environment
    python-3.8.0-embed-win32_modified\Scripts\virtualenv.exe venv

    echo Activating virtual environment...
    call venv\Scripts\activate
    echo Installing requirements...
    python-3.8.0-embed-win32_modified\Scripts\pip.exe install -r requirements.txt --only-binary=:all:
) else (
    echo Virtual environment already exists.
    echo Activating existing virtual environment...
    call venv\Scripts\activate
)


REM Ask for the directory
set /P directory="Please enter the destination directory: "
if "%directory%"=="" (
    echo You must enter a directory to continue.
    goto :eof
)

REM Ask for the threshold
set threshold=0.6
set /P userThreshold="Would you like to change the threshold? Default is 0.6 (Leave empty for default): "
if not "%userThreshold%"=="" (
    set threshold=%userThreshold%
)
cls
python-3.8.0-embed-win32_modified\python.exe script.py "%directory%" --minscore %threshold%

echo Done!
PAUSE
