# Quick Reference Guide

## Project Structure (Clean)

```
WEB_API_FINAL/
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Main container config
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies (pinned versions)
├── .gitignore                  # Git ignore rules (updated)
├── CLEANUP_COMPLETED.md        # Detailed cleanup log
├── setup.sh                    # Linux/Mac setup script
├── setup.bat                   # Windows setup script
│
├── .github/
│   └── workflows/
│       └── docker-ci-cd.yml    # CI/CD pipeline
│
├── docker/                     # Environment files
│   ├── db.env
│   ├── django.env
│   └── fastapi.env
│
├── fastapi_api/                # FastAPI Backend (SQLite3)
│   ├── main.py                 # ✓ Cleaned - removed unused endpoints
│   ├── database.py             # ✓ SQLite3 setup (aiosqlite)
│   ├── Dockerfile
│   ├── wait_for_db.py
│   ├── models/                 # Data models
│   │   ├── booking_model.py
│   │   ├── room_model.py
│   │   └── user_model.py
│   └── routers/                # API endpoints
│       ├── rooms.py            # Room CRUD
│       ├── bookings.py         # Booking CRUD
│       └── users.py            # User CRUD
│       └── [removed] bookins.py (was empty/duplicate)
│
├── django_frontend/            # Django Admin Dashboard
│   ├── manage.py
│   ├── Dockerfile
│   ├── frontend/               # Django project settings
│   │   ├── settings.py         # ✓ SQLite3 configured
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── views/
│   │   ├── views.py
│   │   └── urls.py
│   ├── templates/              # ✓ Cleaned - 11 .bak files removed
│   │   ├── admin_base.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_rooms.html
│   │   ├── admin_booking.html
│   │   ├── base.html
│   │   ├── booking.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── room_details.html
│   │   ├── rooms.html
│   │   └── staycation_nav.html
│   └── static/                 # ✓ Cleaned - 3 .bak files removed
│       ├── css/
│       │   ├── admin.css
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
│
└── web_frontend/               # Alternative Django app
    ├── manage.py
    ├── shop/
    │   └── migrations/
    │       └── __init__.py
    └── web_frontend/
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

## Database Configuration

### FastAPI (Main API)
- **Type**: SQLite3 with async support
- **Driver**: aiosqlite
- **Location**: `./staycation.db`
- **Auto-Init**: Yes (on app startup)
- **Configuration**: `fastapi_api/database.py`

### Django (Admin Interface)
- **Type**: SQLite3
- **Location**: `django_frontend/db.sqlite3`
- **Configuration**: `django_frontend/frontend/settings.py`

## What Was Cleaned

### Deleted Files (16 total)
- **Templates**: 11 backup files (.bak_20251210*)
  - admin_base.html (3 backups)
  - admin_booking.html (1 backup)
  - admin_dashboard.html (2 backups)
  - admin_rooms.html (1 backup)
  - base.html (1 backup)
  
- **CSS**: 3 backup files (.bak_20251210*)
  - admin.css (3 backups)
  
- **Code**: 1 redundant file
  - `fastapi_api/routers/bookins.py` (empty, was typo duplicate)

### Removed Code
- **ProductModel** class (not used in staycation app)
- Product CRUD endpoints (GET /products, POST /products, etc.)
- Unused imports from FastAPI main.py

### Updated Files
- ✅ `fastapi_api/main.py` - Cleaned, added health check
- ✅ `fastapi_api/database.py` - Optimized, improved docs
- ✅ `requirements.txt` - Pinned versions
- ✅ `.gitignore` - Added .db, .bak_* exclusions

## Quick Start

### 1. Setup Environment
```bash
# Windows
setup.bat

# Linux/Mac
bash setup.sh
```

### 2. Start FastAPI Server
```bash
cd fastapi_api
uvicorn main:app --reload
# API will be at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Start Django Admin
```bash
cd django_frontend
python manage.py runserver
# Admin will be at http://localhost:8000/admin
```

## Available Endpoints

### API Endpoints (FastAPI)
```
GET    /health              - Health check
GET    /api/rooms/          - List rooms
POST   /api/rooms/          - Create room
GET    /api/rooms/{id}      - Get room details
PUT    /api/rooms/{id}      - Update room
DELETE /api/rooms/{id}      - Delete room

GET    /api/bookings/       - List bookings
POST   /api/bookings/       - Create booking
GET    /api/bookings/{id}   - Get booking
PUT    /api/bookings/{id}   - Update booking
DELETE /api/bookings/{id}   - Delete booking

GET    /api/users/          - List users
POST   /api/users/          - Create user
GET    /api/users/{id}      - Get user
PUT    /api/users/{id}      - Update user
DELETE /api/users/{id}      - Delete user
```

### Admin Panel (Django)
```
/admin                      - Django admin interface
/                           - Home page
/rooms                      - View rooms
/bookings                   - View bookings
/login                      - Login page
```

## Database Tables

### SQLite3 Database (staycation.db)
1. **rooms** - Hotel room inventory
   - id, title, price, type, capacity, image_url, status, description

2. **bookings** - Guest reservations
   - id, guest_name, room, checkin, checkout, status, nights, total

3. **users** - System users
   - id, username, email, full_name

### Default Sample Data
- 2 rooms (Deluxe Suite, Standard Room)
- 3 bookings with realistic guest data
- 2 users (admin, guest)

## Environment Variables

### FastAPI (.env)
```
DATABASE_URL=sqlite+aiosqlite:///./staycation.db
```

### Django (.env)
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Important Notes

✅ All backup files removed
✅ Unused code removed
✅ SQLite3 properly configured
✅ Async database support enabled
✅ Dependencies pinned to versions
✅ Code properly documented
✅ .gitignore updated

## Troubleshooting

**Database not created?**
- FastAPI automatically creates `./staycation.db` on first run
- Django uses `django_frontend/db.sqlite3`

**Import errors?**
- Run `pip install -r requirements.txt`
- Activate virtual environment: `.venv\Scripts\activate` (Windows)

**Port already in use?**
- Change FastAPI port: `uvicorn main:app --port 8001`
- Change Django port: `python manage.py runserver 8001`

For detailed cleanup information, see **CLEANUP_COMPLETED.md**
