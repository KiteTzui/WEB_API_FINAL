from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from pydantic import BaseModel

import database

router = APIRouter(prefix="/users", tags=["users"])


class UserSchema(BaseModel):
    id: int | None = None
    username: str
    email: str | None = None
    full_name: str | None = None


@router.get("/", response_model=List[UserSchema])
async def list_users(session=Depends(database.get_session)):
    res = await session.execute(select(database.UserModel))
    rows = res.scalars().all()
    return [UserSchema(id=r.id, username=r.username, email=r.email, full_name=r.full_name) for r in rows]


@router.post("/", response_model=UserSchema)
async def create_user(u: UserSchema, session=Depends(database.get_session)):
    obj = database.UserModel(username=u.username, email=u.email, full_name=u.full_name)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return UserSchema(id=obj.id, username=obj.username, email=obj.email, full_name=obj.full_name)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, session=Depends(database.get_session)):
    obj = await session.get(database.UserModel, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema(id=obj.id, username=obj.username, email=obj.email, full_name=obj.full_name)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, u: UserSchema, session=Depends(database.get_session)):
    obj = await session.get(database.UserModel, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    obj.username = u.username
    obj.email = u.email
    obj.full_name = u.full_name
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return UserSchema(id=obj.id, username=obj.username, email=obj.email, full_name=obj.full_name)


@router.delete("/{user_id}")
async def delete_user(user_id: int, session=Depends(database.get_session)):
    obj = await session.get(database.UserModel, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(obj)
    await session.commit()
    return {"detail": "deleted"}
