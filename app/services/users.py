from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_
from slugify import slugify
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.user_m import Users
from app.schemas.user_s import CreateUser, UpdateUser, UserResponse
from app.services.tasks import delete_tasks_by_user


async def get_users(skip: int, limit: int, db: Session):
    result = await db.execute(select(Users).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


async def get_user(user_id: int, db: Session):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_user(user: CreateUser, db: Session):
    # Проверяем существование пользователя с таким же username и firstname
    result = await db.execute(
        select(Users).where(
            and_(Users.username == user.username, Users.firstname == user.firstname)
        )
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким username и firstname уже существует")

    user_slug = slugify(user.username)

    # Создаем словарь с данными пользователя
    user_data = user.dict() if hasattr(user, 'dict') else user.model_dump()

    # Создаем нового пользователя
    new_user = Users(**user_data, slug=user_slug)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(user_id: int, user: UpdateUser, db: Session):
    # Получаем существующего пользователя
    result = await db.execute(select(Users).where(Users.id == user_id))
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем атрибуты пользователя
    user_data = user.dict(exclude_unset=True) if hasattr(user, 'dict') else user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(existing_user, key, value)

    # Обновляем slug
    existing_user.slug = slugify(existing_user.username)

    await db.commit()
    await db.refresh(existing_user)
    return existing_user


async def delete_user(user_id: int, db: Session, delete_tasks_func):
    """
    Удаляет пользователя и все связанные с ним задачи.

    Args:
        user_id: ID пользователя для удаления
        db: Сессия базы данных
        delete_tasks_func: Функция для удаления связанных задач
    """
    try:
        # Получаем существующего пользователя
        result = await db.execute(select(Users).where(Users.id == user_id))
        existing_user = result.scalar_one_or_none()

        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Удаляем задачи пользователя
        deleted_tasks_count = await delete_tasks_func(user_id, db)

        # Удаляем пользователя
        await db.delete(existing_user)
        await db.commit()

        return {
            "detail": f"User and {deleted_tasks_count} associated tasks deleted successfully",
            "user_id": user_id,
            "deleted_tasks_count": deleted_tasks_count
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting user: {str(e)}"
        )

