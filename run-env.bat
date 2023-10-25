@echo off

REM Check if the virtual environment already exists
if not exist "venv\" (
    echo Creating a virtual environment...
    python-3.8.0-embed-win32\python.exe get-pip.py
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\pip.exe install --upgrade pip
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\pip.exe install Pillow --only-binary=:all:
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\pip.exe install wheel
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\pip.exe install virtualenv
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\virtualenv.exe venv
    echo Activating virtual environment...
    call venv\Scripts\activate
    echo Installing requirements...
    C:\Sources\offline-nsfw-scanner\python-3.8.0-embed-win32\Scripts\pip.exe install --no-cache-dir --force-reinstall -r requirements.txt --only-binary=:all:
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
