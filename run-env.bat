@echo off

REM Check if the virtual environment already exists
if not exist "venv\" (
    echo Creating a virtual environment...

:: Install pip
    python-3.8.0-embed-win32\python.exe get-pip.py --no-cache-dir

:: Upgrade pip
    python-3.8.0-embed-win32\Scripts\pip.exe install --upgrade pip --no-cache-dir --force-reinstall

:: Install Pillow using only binaries
    python-3.8.0-embed-win32\Scripts\pip.exe install Pillow --only-binary=:all: --no-cache-dir --force-reinstall

:: Install wheel
    python-3.8.0-embed-win32\Scripts\pip.exe install wheel --no-cache-dir --force-reinstall

:: Install virtualenv
    python-3.8.0-embed-win32\Scripts\pip.exe install virtualenv --no-cache-dir --force-reinstall

:: Create a virtual environment
    python-3.8.0-embed-win32\Scripts\virtualenv.exe venv

    echo Activating virtual environment...
    call venv\Scripts\activate
    echo Installing requirements...
    python-3.8.0-embed-win32\Scripts\pip.exe install --no-cache-dir --force-reinstall -r requirements.txt --only-binary=:all:
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

python-3.8.0-embed-win32\python.exe script.py "%directory%" --minscore %threshold%

echo Done!
PAUSE
