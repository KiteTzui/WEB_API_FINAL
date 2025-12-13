from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from pydantic import BaseModel

import database

router = APIRouter(prefix="/rooms", tags=["rooms"])


class RoomSchema(BaseModel):
    id: int | None = None
    title: str
    price: float
    type: str | None = None
    capacity: int | None = None
    image_url: str | None = None
    status: str | None = None
    description: str | None = None


@router.get("/", response_model=List[RoomSchema])
async def list_rooms(session=Depends(database.get_session)):
    res = await session.execute(select(database.RoomModel))
    rows = res.scalars().all()
    return [RoomSchema(id=r.id, title=r.title, price=r.price, type=r.type, capacity=r.capacity, image_url=r.image_url, status=r.status, description=r.description) for r in rows]


@router.get("/{room_id}", response_model=RoomSchema)
async def get_room(room_id: int, session=Depends(database.get_session)):
    r = await session.get(database.RoomModel, room_id)
    if not r:
        raise HTTPException(status_code=404, detail="Room not found")
    return RoomSchema(id=r.id, title=r.title, price=r.price, type=r.type, capacity=r.capacity, image_url=r.image_url, status=r.status, description=r.description)


@router.post("/", response_model=RoomSchema)
async def create_room(room: RoomSchema, session=Depends(database.get_session)):
    obj = database.RoomModel(title=room.title, price=room.price, type=room.type, capacity=room.capacity, image_url=room.image_url, status=room.status, description=room.description)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return RoomSchema(id=obj.id, title=obj.title, price=obj.price, type=obj.type, capacity=obj.capacity, image_url=obj.image_url, status=obj.status, description=obj.description)


@router.put("/{room_id}", response_model=RoomSchema)
async def update_room(room_id: int, room: RoomSchema, session=Depends(database.get_session)):
    obj = await session.get(database.RoomModel, room_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Room not found")
    obj.title = room.title
    obj.price = room.price
    obj.type = room.type
    obj.capacity = room.capacity
    obj.image_url = room.image_url
    obj.status = room.status
    obj.description = room.description
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return RoomSchema(id=obj.id, title=obj.title, price=obj.price, type=obj.type, capacity=obj.capacity, image_url=obj.image_url, status=obj.status, description=obj.description)


@router.delete("/{room_id}")
async def delete_room(room_id: int, session=Depends(database.get_session)):
    obj = await session.get(database.RoomModel, room_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Room not found")
    await session.delete(obj)
    await session.commit()
    return {"detail": "deleted"}
