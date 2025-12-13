#!/bin/bash
# Setup script for Staycation Hotel Booking System

echo "=========================================="
echo "Staycation Hotel Booking System Setup"
echo "=========================================="
echo ""

# Check Python installation
echo "Checking Python installation..."
python --version || { echo "Python is not installed!"; exit 1; }
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# FastAPI Backend Setup
echo "=========================================="
echo "FastAPI Backend Setup"
echo "=========================================="
echo ""
cd fastapi_api
echo "Installing aiosqlite for async SQLite support..."
pip install aiosqlite
echo "✓ aiosqlite installed"
echo ""
cd ..

# Django Frontend Setup
echo "=========================================="
echo "Django Frontend Setup"
echo "=========================================="
echo ""
cd django_frontend
echo "Running Django migrations..."
python manage.py migrate
echo "✓ Django migrations completed"
echo ""
echo "Creating Django superuser..."
python manage.py createsuperuser
echo "✓ Django superuser created"
echo ""
cd ..

echo "=========================================="
echo "Setup Complete! ✓"
echo "=========================================="
echo ""
echo "To start the FastAPI server:"
echo "  cd fastapi_api"
echo "  uvicorn main:app --reload"
echo ""
echo "To start the Django development server:"
echo "  cd django_frontend"
echo "  python manage.py runserver"
echo ""
echo "Database: SQLite3 (./staycation.db)"
echo "Documentation: See CLEANUP_COMPLETED.md"
echo ""
