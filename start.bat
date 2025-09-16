@echo off
echo Easy AI Speaker Avatar System
echo =============================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask, pyttsx3, cv2, PIL" >nul 2>&1
if errorlevel 1 (
    echo Dependencies not found. Installing...
    echo.
    python download.py
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Start the system
echo Starting Easy AI Speaker Avatar System...
echo.
python run.py

pause
