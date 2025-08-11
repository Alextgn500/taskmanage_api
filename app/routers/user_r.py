from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_s import UserResponse, CreateUser, UpdateUser
from app.backend.db_depends import get_async_db
from app.services import users  # импорт бизнес-логики из services/users.py

router_user = APIRouter(prefix='/users', tags=['users'])  # исправлено: tags должен быть списком


@router_user.get("/", response_model=List[UserResponse])  # исправлено: responsemodel -> response_model
async def read_users(skip: int = 0, limit: int = None, db: Session = Depends(get_async_db)):
    return await users.get_users(skip, limit, db)


@router_user.get("/{user_id}", response_model=UserResponse)  # исправлено: userid -> user_id, responsemodel -> response_model
async def read_user(user_id: int, db: Session = Depends(get_async_db)):
    return await users.get_user(user_id, db)


@router_user.post("/", response_model=UserResponse, status_code=201)  # исправлено: responsemodel -> response_model
async def create_user(user: CreateUser, db: Session = Depends(get_async_db)):
    return await users.create_user(user, db)


@router_user.put("/{user_id}", response_model=UserResponse)  # исправлено: userid -> user_id, responsemodel -> response_model
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_async_db)):
    return await users.update_user(user_id, user, db)


@router_user.delete("/{user_id}", response_model=dict)  # исправлено: userid -> user_id, responsemodel -> response_model, удалил /tasks из пути
async def delete_user(user_id: int, db: Session = Depends(get_async_db)):
    # передаём функцию для удаления задач пользователя в сервисы
    from app.services.tasks import delete_tasks_by_user
    return await users.delete_user(user_id, db, delete_tasks_by_user)