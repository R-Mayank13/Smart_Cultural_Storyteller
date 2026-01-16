@echo off
title Smart Cultural Storyteller
color 0A
cls

echo.
echo ========================================
echo    Smart Cultural Storyteller
echo    One-Click Launcher
echo ========================================
echo.

REM Go to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ Python not found! Please install Python from python.org
    echo Press any key to open Python download page...
    pause >nul
    start https://python.org/downloads/
    exit /b 1
)

REM Silent install everything
color 0B
echo 📦 Setting up application...
echo.

REM Install Python packages silently
echo [INFO] Installing dependencies...
python -m pip install --upgrade pip --quiet --disable-pip-version-check
python -m pip install gradio openai requests pillow gtts pygame python-dotenv transformers torch diffusers accelerate --quiet --disable-pip-version-check

REM Create .env file
if not exist ".env" (
    echo [INFO] Creating environment file...
    echo OPENAI_API_KEY=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 > ".env"
)

REM Kill any existing processes on port 7860
echo [INFO] Stopping any existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :7860') do (
    taskkill /f /pid %%a >nul 2>&1
)

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start app in background and wait for it to be ready
color 0A
echo.
echo ========================================
echo ✅ Starting Smart Cultural Storyteller...
echo 🌐 Will open http://localhost:7860 when ready...
echo ========================================
echo.

REM Start Python app
start "" python app.py

REM Wait for server to start (check if port is listening)
echo [WAIT] Waiting for server to start...
:wait_loop
timeout /t 1 /nobreak >nul
netstat -an | findstr :7860 | findstr LISTENING >nul
if errorlevel 1 goto wait_loop

REM Server is ready, open browser
color 0E
echo.
echo ========================================
echo 🚀 Server is ready! Opening browser...
echo ========================================
start http://localhost:7860

color 0A
echo.
echo ========================================
echo ✅ APPLICATION IS RUNNING SUCCESSFULLY!
echo 🌐 URL: http://localhost:7860
echo 🎭 Smart Cultural Storyteller is ready!
echo 🛑 Close this window to stop the application
echo ========================================
echo.
pause