@echo off
echo 🤖 AI Mental Health Chatbot - TinyLLaMA
echo ======================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.py first:
    echo python setup.py
    pause
    exit /b 1
)

echo ✅ Activating virtual environment...
call venv\Scripts\activate

echo 🚀 Starting chatbot server...
echo.
echo The chatbot will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo 👋 Chatbot stopped. Press any key to exit.
pause