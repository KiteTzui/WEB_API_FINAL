#!/bin/bash
# Cleanup Verification Script
# This script verifies that all cleanup tasks were completed successfully

echo ""
echo "=========================================="
echo "Staycation Project Cleanup Verification"
echo "=========================================="
echo ""

PASS=0
FAIL=0

# Function to check if file exists
check_file_exists() {
    if [ -f "$1" ]; then
        echo "✅ PASS: $1 exists"
        ((PASS++))
    else
        echo "❌ FAIL: $1 missing"
        ((FAIL++))
    fi
}

# Function to check if file doesn't exist
check_file_missing() {
    if [ ! -f "$1" ]; then
        echo "✅ PASS: $1 correctly removed"
        ((PASS++))
    else
        echo "❌ FAIL: $1 still exists (should be removed)"
        ((FAIL++))
    fi
}

echo "Checking for required files..."
echo "================================"
check_file_exists "requirements.txt"
check_file_exists "fastapi_api/database.py"
check_file_exists "fastapi_api/main.py"
check_file_exists "fastapi_api/routers/rooms.py"
check_file_exists "fastapi_api/routers/bookings.py"
check_file_exists "fastapi_api/routers/users.py"
check_file_exists ".gitignore"
check_file_exists "CLEANUP_COMPLETED.md"
check_file_exists "QUICK_REFERENCE.md"
check_file_exists "PROJECT_STATUS.md"
check_file_exists "setup.sh"
check_file_exists "setup.bat"
echo ""

echo "Checking for removed files..."
echo "================================"
check_file_missing "fastapi_api/routers/bookins.py"
check_file_missing "django_frontend/templates/admin_base.html.bak_20251210164737"
check_file_missing "django_frontend/templates/admin_base.html.bak_20251210164937"
check_file_missing "django_frontend/templates/admin_base.html.bak_20251210165231"
check_file_missing "django_frontend/templates/admin_booking.html.bak_20251210164331"
check_file_missing "django_frontend/templates/admin_dashboard.html.bak_20251210163703"
check_file_missing "django_frontend/templates/admin_dashboard.html.bak_20251210164331"
check_file_missing "django_frontend/templates/admin_rooms.html.bak_20251210164331"
check_file_missing "django_frontend/templates/base.html.bak_20251210164331"
check_file_missing "django_frontend/static/css/admin.css.bak_20251210163441"
check_file_missing "django_frontend/static/css/admin.css.bak_20251210163853"
check_file_missing "django_frontend/static/css/admin.css.bak_20251210164331"
echo ""

echo "Checking code quality..."
echo "================================"

# Check if requirements.txt has pinned versions
if grep -q "==" requirements.txt; then
    echo "✅ PASS: requirements.txt has pinned versions"
    ((PASS++))
else
    echo "❌ FAIL: requirements.txt missing version pins"
    ((FAIL++))
fi

# Check if main.py is cleaned (no ProductModel)
if ! grep -q "ProductModel" fastapi_api/main.py; then
    echo "✅ PASS: ProductModel removed from main.py"
    ((PASS++))
else
    echo "❌ FAIL: ProductModel still in main.py"
    ((FAIL++))
fi

# Check if database.py has SQLite3 config
if grep -q "sqlite" fastapi_api/database.py; then
    echo "✅ PASS: SQLite3 configured in database.py"
    ((PASS++))
else
    echo "❌ FAIL: SQLite3 not found in database.py"
    ((FAIL++))
fi

# Check if aiosqlite is in requirements
if grep -q "aiosqlite" requirements.txt; then
    echo "✅ PASS: aiosqlite added to requirements.txt"
    ((PASS++))
else
    echo "❌ FAIL: aiosqlite not in requirements.txt"
    ((FAIL++))
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo "Your project is clean and ready to use."
    echo ""
    echo "Next steps:"
    echo "1. Run: bash setup.sh (or setup.bat on Windows)"
    echo "2. Start FastAPI: cd fastapi_api && uvicorn main:app --reload"
    echo "3. Visit: http://localhost:8000/docs"
    exit 0
else
    echo "❌ SOME CHECKS FAILED"
    echo "Please review the failures above."
    exit 1
fi
