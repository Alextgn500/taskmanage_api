from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user_s import UserResponse, CreateUser, UpdateUser
from app.backend.db_depends import get_db
from app.services import users  # импорт бизнес-логики из services/users.py
from app.services import tasks

router_user = APIRouter(prefix='/users', tags='users')


@router_user.get("/", responsemodel=List[UserResponse])
def readusers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return users.getusers(skip, limit, db)


@router_user.get("/{userid}", responsemodel=UserResponse)
def readuser(userid: int, db: Session = Depends(get_db)):
    return users.getuser(userid, db)


@router_user.post("/", responsemodel=UserResponse)
def createuser(user: CreateUser, db: Session = Depends(get_db)):
    return users.createuser(user, db)


@router_user.put("/{userid}", responsemodel=UserResponse)
def updateuser(userid: int, user: UpdateUser, db: Session = Depends(get_db)):
    return users.updateuser(userid, user, db)


@router_user.delete("/{userid}/tasks", responsemodel=dict)
def deleteuser(userid: int, db: Session = Depends(get_db)):
    # передаём функцию для удаления задач пользователя в сервисы
    return users.deleteuser(userid, db, tasks.deletetasks)