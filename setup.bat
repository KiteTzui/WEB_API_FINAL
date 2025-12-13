@echo off
REM Setup script for Staycation Hotel Booking System (Windows)

echo.
echo ==========================================
echo Staycation Hotel Booking System Setup
echo ==========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed!
    exit /b 1
)
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM FastAPI Backend Setup
echo ==========================================
echo FastAPI Backend Setup
echo ==========================================
echo.
cd fastapi_api
echo Installing aiosqlite for async SQLite support...
pip install aiosqlite
echo [OK] aiosqlite installed
echo.
cd ..

REM Django Frontend Setup
echo ==========================================
echo Django Frontend Setup
echo ==========================================
echo.
cd django_frontend
echo Running Django migrations...
python manage.py migrate
echo [OK] Django migrations completed
echo.
echo Creating Django superuser...
python manage.py createsuperuser
echo [OK] Django superuser created
echo.
cd ..

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the FastAPI server:
echo   cd fastapi_api
echo   uvicorn main:app --reload
echo.
echo To start the Django development server:
echo   cd django_frontend
echo   python manage.py runserver
echo.
echo Database: SQLite3 (./staycation.db)
echo Documentation: See CLEANUP_COMPLETED.md
echo.
pause
