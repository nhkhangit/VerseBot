@echo off
echo Starting Todo List API...

:: Set UTF-8 encoding
chcp 65001

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    echo Please install Python and add it to PATH
    pause
    exit /b 1
)

:: Check if virtual environment exists
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
) ELSE (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

:: Check if .env exists
IF NOT EXIST ".env" (
    echo Creating .env file...
    (
        echo POSTGRES_USER=postgres
        echo POSTGRES_PASSWORD=Abc123password
        echo POSTGRES_HOST=localhost
        echo POSTGRES_PORT=5432
        echo POSTGRES_DB=todolist_db
    ) > .env
)

:: Check PostgreSQL
@REM pg_isready -h localhost -p 5432 >nul 2>&1
@REM if %ERRORLEVEL% NEQ 0 (
@REM     echo WARNING: PostgreSQL is not running or not accessible
@REM     echo Please make sure PostgreSQL is running on port 5432
@REM     choice /C YN /M "Do you want to continue anyway"
@REM     if errorlevel 2 exit /b 1
@REM )

:: Check if database exists
@REM psql -U postgres -lqt | find "postgres" >nul
@REM if %ERRORLEVEL% NEQ 0 (
@REM     echo Creating database...
@REM     psql -U postgres -c "CREATE DATABASE postgres;"
@REM     if %ERRORLEVEL% NEQ 0 (
@REM         echo Failed to create database
@REM         pause
@REM         exit /b 1
@REM     )
@REM )

:: Clear screen
cls

echo.
echo =================================
echo     Todo List API is starting
echo =================================
echo.
echo Available at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

:: If the application stops, deactivate the virtual environment
deactivate