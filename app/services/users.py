from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_
from slugify import slugify
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.user_m import Users
from app.schemas.user_s import CreateUser, UpdateUser, UserResponse
from app.services.tasks import delete_tasks_by_user


async def authenticate_user(username: str, password: str, db: Session):
    """Проверка пользователя для входа"""
    try:
        # Найти пользователя по username
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user:
            return None
        if user.password == password:  # ⚠️ В продакшене хешируйте пароли!
            return user

        return None
    except Exception as e:
        print(f"Ошибка аутентификации: {e}")
    return None


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
    print(f"Начало создания пользователя: {user.username}")

    # Проверяем существование пользователя с таким же username и firstname
    result = await db.execute(
        select(Users).where(
            and_(Users.username == user.username, Users.firstname == user.firstname)
        )
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким username и firstname уже существует")

    # Создаем словарь с данными пользователя
    user_data = user.model_dump() if hasattr(user, 'dict') else user.model_dump()
    print(f"Данные пользователя: {user_data}")

    # Создаем нового пользователя БЕЗ slug
    new_user = Users(**user_data)
    print(f"Пользователь создан, ID до commit: {new_user.id}")

    # Добавляем в БД и коммитим для получения ID
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    print(f"ID после commit: {new_user.id}")

    # Проверяем функцию slugify
    base_slug = slugify(user.username)
    print(f"Base slug: {base_slug}")

    # Создаем уникальный slug с ID
    user_slug = f"{base_slug}-{new_user.id}"
    print(f"Финальный slug: {user_slug}")

    # Обновляем пользователя с новым slug
    new_user.slug = user_slug
    print(f"Slug установлен в объект: {new_user.slug}")

    await db.commit()
    await db.refresh(new_user)

    print(f"Slug после финального commit: {new_user.slug}")

    return new_user

async def update_user(user_id: int, user: UpdateUser, db: Session):
    # Получаем существующего пользователя
    result = await db.execute(select(Users).where(Users.id == user_id))
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем атрибуты пользователя
    user_data = user.model_dump(exclude_unset=True)
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

