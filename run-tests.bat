@echo off
echo ====================================================
echo Automation of saucedemo.com tests
echo ====================================================

REM Step 1: Stop old containers
echo [1/4] Stopping old containers...
docker-compose down --remove-orphans 2>nul

REM Step 2: Run tests
echo [2/4] Running tests in Docker...
docker-compose up tests --build

IF %ERRORLEVEL% NEQ 0 (
    echo Error running tests!
    pause
    exit /b 1
)

REM Step 3: Generate Allure report
echo [3/4] Generating Allure report...
docker run --rm -v "%cd%\allure-results:/allure-results" -v "%cd%\allure-report:/allure-report" frankescobar/allure-docker-service allure generate /allure-results -o /allure-report --clean

REM Step 4: Start web server with report
echo [4/4] Starting web server for report...
echo ====================================================
echo Allure report available at:
echo http://localhost:8000
echo ====================================================
echo Press Ctrl+C to stop server
echo ====================================================

cd allure-report
start python -m http.server 8000
timeout /t 2 /nobreak >nul
start http://localhost:8000

pause