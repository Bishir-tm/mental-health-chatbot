@echo off
echo AI Mental Health Chatbot - Portable Version
echo ===============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found!
    echo Please run portable_setup.py first
    pause
    exit /b 1
)

REM Check if models directory exists
if not exist "models" (
    echo Models directory not found!
    echo Please run portable_setup.py first to download the model
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting portable chatbot server...
echo.
echo The chatbot will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app_portable.py

echo.
echo Chatbot stopped. Press any key to exit.
pause