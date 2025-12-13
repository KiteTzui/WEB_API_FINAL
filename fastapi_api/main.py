from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import database
import routers.rooms as rooms_router
import routers.bookings as bookings_router
import routers.users as users_router

# Initialize FastAPI app
app = FastAPI(
    title="Staycation API",
    description="API for Staycation Hotel Booking System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Initialize database on startup."""
    await database.init_db()


@app.get("/")
async def home():
    """Home endpoint."""
    return {
        "message": "Staycation API is running 🏨",
        "project": "Staycation Hotel Booking System",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Include routers
app.include_router(rooms_router.router, prefix="/api", tags=["Rooms"])
app.include_router(bookings_router.router, prefix="/api", tags=["Bookings"])
app.include_router(users_router.router, prefix="/api", tags=["Users"])
