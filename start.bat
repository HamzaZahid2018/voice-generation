@echo off
echo ========================================
echo   Deepgram TTS - Quick Start
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    pause
    exit
)

echo.
echo Installing requirements...
pip install -r requirements.txt

echo.
echo ========================================
echo Choose an option:
echo ========================================
echo 1. Run Web App (Basic)
echo 2. Run Web App (Advanced)
echo 3. Run CLI Script
echo ========================================
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting basic web app...
    echo Open your browser to: http://localhost:8501
    echo.
    streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo Starting advanced web app...
    echo Open your browser to: http://localhost:8501
    echo.
    streamlit run app_advanced.py
) else if "%choice%"=="3" (
    echo.
    echo Running CLI script...
    echo.
    python deepgram_improved.py
) else (
    echo Invalid choice!
    pause
)
