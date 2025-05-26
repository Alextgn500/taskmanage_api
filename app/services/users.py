from sqlalchemy.orm import Session
from sqlalchemy import and_
from slugify import slugify

from app.models.userm import Users
from app.schemas.users import CreateUser, UpdateUser, UserResponse
from fastapi import HTTPException


def getusers(skip: int, limit: int, db: Session):
    return db.query(Users).offset(skip).limit(limit).all()


def getuser(userid: int, db: Session):
    user = db.query(Users).filter(Users.id == userid).first()
    if user is None:
        raise HTTPException(statuscode=404, detail="User not found")
    return user


def createuser(user: CreateUser, db: Session):
    existinguser = db.query(Users).filter(
        and_(Users.username == user.username, Users.firstname == user.firstname)
    ).first()

    if existinguser:
        raise HTTPException(statuscode=400, detail="Пользователь с таким username и firstname уже существует")

    userslug = slugify(user.username)
    newuser = Users(user.dict(), slug=userslug)
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


def updateuser(userid: int, user: UpdateUser, db: Session):
    existinguser = db.get(Users, userid)
    if existinguser is None:
        raise HTTPException(statuscode=404, detail="User not found")

    for key, value in user.dict(excludeunset=True).items():
        setattr(existinguser, key, value)

    existinguser.slug = slugify(existinguser.username)
    db.commit()
    db.refresh(existinguser)
    return existinguser


def deleteuser(userid: int, db: Session, deletetasksfunc):
    existinguser = db.get(Users, userid)
    if existinguser is None:
        raise HTTPException(statuscode=404, detail="User not found")

    deletetasksfunc(userid, db)

    db.delete(existinguser)
    db.commit()
    return {"detail": "User and associated tasks deleted successfully"}
