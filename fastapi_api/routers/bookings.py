from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from pydantic import BaseModel

import database

router = APIRouter(prefix="/bookings", tags=["bookings"])


class BookingSchema(BaseModel):
    id: int | None = None
    guest_name: str
    room: str
    checkin: str | None = None
    checkout: str | None = None
    status: str | None = None
    nights: int | None = None
    total: float | None = None


@router.get("/", response_model=List[BookingSchema])
async def list_bookings(session=Depends(database.get_session)):
    res = await session.execute(select(database.BookingModel))
    rows = res.scalars().all()
    return [BookingSchema(**{k: getattr(r, k) for k in ['id','guest_name','room','checkin','checkout','status','nights','total']}) for r in rows]


@router.post("/", response_model=BookingSchema)
async def create_booking(b: BookingSchema, session=Depends(database.get_session)):
    obj = database.BookingModel(guest_name=b.guest_name, room=b.room, checkin=b.checkin, checkout=b.checkout, status=b.status, nights=b.nights, total=b.total)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return BookingSchema(id=obj.id, guest_name=obj.guest_name, room=obj.room, checkin=obj.checkin, checkout=obj.checkout, status=obj.status, nights=obj.nights, total=obj.total)


@router.get("/{booking_id}", response_model=BookingSchema)
async def get_booking(booking_id: int, session=Depends(database.get_session)):
    obj = await session.get(database.BookingModel, booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingSchema(id=obj.id, guest_name=obj.guest_name, room=obj.room, checkin=obj.checkin, checkout=obj.checkout, status=obj.status, nights=obj.nights, total=obj.total)


@router.put("/{booking_id}", response_model=BookingSchema)
async def update_booking(booking_id: int, b: BookingSchema, session=Depends(database.get_session)):
    obj = await session.get(database.BookingModel, booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Booking not found")
    obj.guest_name = b.guest_name
    obj.room = b.room
    obj.checkin = b.checkin
    obj.checkout = b.checkout
    obj.status = b.status
    obj.nights = b.nights
    obj.total = b.total
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return BookingSchema(id=obj.id, guest_name=obj.guest_name, room=obj.room, checkin=obj.checkin, checkout=obj.checkout, status=obj.status, nights=obj.nights, total=obj.total)


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, session=Depends(database.get_session)):
    obj = await session.get(database.BookingModel, booking_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Booking not found")
    await session.delete(obj)
    await session.commit()
    return {"detail": "deleted"}
