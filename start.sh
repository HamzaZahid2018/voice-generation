#!/bin/bash

echo "========================================"
echo "  Deepgram TTS - Quick Start"
echo "========================================"
echo

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found!"
    echo "Please install Python 3"
    exit 1
fi

echo
echo "Installing requirements..."
pip3 install -r requirements.txt

echo
echo "========================================"
echo "Choose an option:"
echo "========================================"
echo "1. Run Web App (Basic)"
echo "2. Run Web App (Advanced)"
echo "3. Run CLI Script"
echo "========================================"
echo

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo
        echo "Starting basic web app..."
        echo "Open your browser to: http://localhost:8501"
        echo
        streamlit run app.py
        ;;
    2)
        echo
        echo "Starting advanced web app..."
        echo "Open your browser to: http://localhost:8501"
        echo
        streamlit run app_advanced.py
        ;;
    3)
        echo
        echo "Running CLI script..."
        echo
        python3 deepgram_improved.py
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
