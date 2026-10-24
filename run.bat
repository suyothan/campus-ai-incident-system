@echo off
title CampusAI - Multimodal Facility & Hazard Diagnostic Platform
color 0b

echo ===================================================================
echo     CAMPUS AI: MULTIMODAL FACILITY & HAZARD DIAGNOSTICS
echo     Google Cloud Platform Stack:
echo     Cloud Run + GCS + Vertex AI + Firestore + BigQuery + Looker Studio
echo ===================================================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit /b
)

echo.
echo Starting FastAPI web server on port 8080...
echo Open your browser at: http://localhost:8080
echo.

REM Automatically open browser
start http://localhost:8080

REM Run FastAPI application
python app.py
pause
