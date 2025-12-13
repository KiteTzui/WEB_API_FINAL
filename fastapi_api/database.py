import os
from sqlalchemy import Column, Integer, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

# SQLite3 configuration for async operations
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./staycation.db"
)

# Create async engine with SQLite
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False  # Set to True for SQL query logging
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()



# Room Model - Staycation rooms
class RoomModel(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    type = Column(String(100), nullable=True)
    capacity = Column(Integer, nullable=True)
    image_url = Column(String(1024), nullable=True)
    status = Column(String(50), nullable=True)
    description = Column(String(1024), nullable=True)


# Booking Model - Guest bookings
class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    guest_name = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False)
    checkin = Column(String(100), nullable=True)
    checkout = Column(String(100), nullable=True)
    status = Column(String(50), nullable=True)
    nights = Column(Integer, nullable=True)
    total = Column(Float, nullable=True)


# User Model - System users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)



async def init_db():
    """Initialize database - create all tables and seed initial data."""
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed sample data if tables are empty
    async with AsyncSessionLocal() as session:
        # Check and seed rooms
        res = await session.execute(select(RoomModel))
        rooms = res.scalars().all()
        if not rooms:
            sample_rooms = [
                RoomModel(
                    title="Deluxe Suite",
                    price=199.0,
                    type="Suite",
                    capacity=2,
                    image_url="/static/images/room1.jpg",
                    status="available",
                    description="Luxurious suite with premium amenities"
                ),
                RoomModel(
                    title="Standard Room",
                    price=99.0,
                    type="Standard",
                    capacity=2,
                    image_url="/static/images/room2.jpg",
                    status="available",
                    description="Comfortable standard room for your stay"
                ),
            ]
            session.add_all(sample_rooms)
        
        # Check and seed bookings
        resb = await session.execute(select(BookingModel))
        bookings = resb.scalars().all()
        if not bookings:
            sample_bookings = [
                BookingModel(
                    guest_name="John Smith",
                    room="Deluxe Suite",
                    checkin="Dec 10, 2024",
                    checkout="Dec 15, 2024",
                    status="Confirmed",
                    nights=5,
                    total=995.0
                ),
                BookingModel(
                    guest_name="Emily Johnson",
                    room="Standard Room",
                    checkin="Dec 8, 2024",
                    checkout="Dec 10, 2024",
                    status="Pending",
                    nights=2,
                    total=198.0
                ),
                BookingModel(
                    guest_name="Michael Brown",
                    room="Deluxe Suite",
                    checkin="Dec 12, 2024",
                    checkout="Dec 18, 2024",
                    status="Confirmed",
                    nights=6,
                    total=1194.0
                ),
            ]
            session.add_all(sample_bookings)
        
        # Check and seed users
        resu = await session.execute(select(UserModel))
        users = resu.scalars().all()
        if not users:
            sample_users = [
                UserModel(
                    username="admin",
                    email="admin@staycation.com",
                    full_name="Administrator"
                ),
                UserModel(
                    username="guest",
                    email="guest@staycation.com",
                    full_name="Guest User"
                ),
            ]
            session.add_all(sample_users)
        
        await session.commit()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session for FastAPI endpoints."""
    async with AsyncSessionLocal() as session:
        yield session
