@echo off
echo Virtual Keyboard Launcher
echo ========================

REM Try to find Python
set PYTHON_CMD=

REM Check if python is in PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :found_python
)

REM Check if python3 is in PATH
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

REM Check Microsoft Store Python
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
    goto :found_python
)

REM Check common Python installation paths
for %%i in (39 310 311 312 313) do (
    if exist "C:\Python%%i\python.exe" (
        set PYTHON_CMD="C:\Python%%i\python.exe"
        goto :found_python
    )
)

echo Python not found!
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_CMD%

REM Check if requirements are installed
echo Checking dependencies...
%PYTHON_CMD% -c "import cv2, mediapipe, pyautogui, keyboard, numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo Starting Virtual Keyboard...
echo.
echo Controls:
echo - ESC: Exit
echo - Space: Toggle keyboard visibility
echo - Index finger: Point to keys
echo - Bring finger close to palm to press
echo.

%PYTHON_CMD% virtual_keyboard.py

echo.
echo Virtual Keyboard closed.
pause 