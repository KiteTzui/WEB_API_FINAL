@echo off
REM Cleanup Verification Script (Windows)
REM This script verifies that all cleanup tasks were completed successfully

echo.
echo ==========================================
echo Staycation Project Cleanup Verification
echo ==========================================
echo.

setlocal enabledelayedexpansion
set PASS=0
set FAIL=0

echo Checking for required files...
echo ==================================

for %%F in (
    "requirements.txt"
    "fastapi_api\database.py"
    "fastapi_api\main.py"
    "fastapi_api\routers\rooms.py"
    "fastapi_api\routers\bookings.py"
    "fastapi_api\routers\users.py"
    ".gitignore"
    "CLEANUP_COMPLETED.md"
    "QUICK_REFERENCE.md"
    "PROJECT_STATUS.md"
    "setup.bat"
    "setup.sh"
) do (
    if exist "%%F" (
        echo [OK] %%F exists
        set /a PASS=!PASS!+1
    ) else (
        echo [FAIL] %%F missing
        set /a FAIL=!FAIL!+1
    )
)
echo.

echo Checking for removed files...
echo ==================================

for %%F in (
    "fastapi_api\routers\bookins.py"
    "django_frontend\templates\admin_base.html.bak_20251210164737"
    "django_frontend\templates\admin_base.html.bak_20251210164937"
    "django_frontend\templates\admin_base.html.bak_20251210165231"
    "django_frontend\templates\admin_booking.html.bak_20251210164331"
    "django_frontend\templates\admin_dashboard.html.bak_20251210163703"
    "django_frontend\templates\admin_dashboard.html.bak_20251210164331"
    "django_frontend\templates\admin_rooms.html.bak_20251210164331"
    "django_frontend\templates\base.html.bak_20251210164331"
    "django_frontend\static\css\admin.css.bak_20251210163441"
    "django_frontend\static\css\admin.css.bak_20251210163853"
    "django_frontend\static\css\admin.css.bak_20251210164331"
) do (
    if not exist "%%F" (
        echo [OK] %%F removed
        set /a PASS=!PASS!+1
    ) else (
        echo [FAIL] %%F still exists
        set /a FAIL=!FAIL!+1
    )
)
echo.

echo Checking code quality...
echo ==================================

REM Check requirements.txt for version pins
findstr /M "==" requirements.txt >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] requirements.txt has pinned versions
    set /a PASS=!PASS!+1
) else (
    echo [FAIL] requirements.txt missing version pins
    set /a FAIL=!FAIL!+1
)

REM Check main.py for ProductModel removal
findstr /M "ProductModel" fastapi_api\main.py >nul 2>&1
if %ERRORLEVEL% == 1 (
    echo [OK] ProductModel removed from main.py
    set /a PASS=!PASS!+1
) else (
    echo [FAIL] ProductModel still in main.py
    set /a FAIL=!FAIL!+1
)

REM Check database.py for SQLite3
findstr /M "sqlite" fastapi_api\database.py >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] SQLite3 configured in database.py
    set /a PASS=!PASS!+1
) else (
    echo [FAIL] SQLite3 not found in database.py
    set /a FAIL=!FAIL!+1
)

REM Check requirements for aiosqlite
findstr /M "aiosqlite" requirements.txt >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo [OK] aiosqlite added to requirements.txt
    set /a PASS=!PASS!+1
) else (
    echo [FAIL] aiosqlite not in requirements.txt
    set /a FAIL=!FAIL!+1
)

echo.
echo ==========================================
echo Verification Summary
echo ==========================================
echo Passed: %PASS%
echo Failed: %FAIL%
echo.

if %FAIL% == 0 (
    echo [OK] ALL CHECKS PASSED!
    echo Your project is clean and ready to use.
    echo.
    echo Next steps:
    echo 1. Run: setup.bat
    echo 2. Start FastAPI: cd fastapi_api ^&^& uvicorn main:app --reload
    echo 3. Visit: http://localhost:8000/docs
    echo.
) else (
    echo [FAIL] SOME CHECKS FAILED
    echo Please review the failures above.
    echo.
)

pause
