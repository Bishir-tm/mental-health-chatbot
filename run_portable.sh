#!/bin/bash
echo "AI Mental Health Chatbot - Portable Version"
echo "==============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run portable_setup.py first"
    exit 1
fi

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "Models directory not found!"
    echo "Please run portable_setup.py first to download the model"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting portable chatbot server..."
echo ""
echo "The chatbot will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app_portable.py