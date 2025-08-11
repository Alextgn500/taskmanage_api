from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_async_db
from app.models.user_m import Users
from sqlalchemy import select

# Создание роутера
auth_router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    user_id: int
    username: str
    firstname: str
    lastname: str


# ✅ Добавьте эту схему для регистрации
class RegisterRequest(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int
    password: str


class RegisterResponse(BaseModel):
    message: str
    user_id: int
    firstname: str
    lastname: str
    username: str
    age: int
    slug: str


# ✅ Роут для входа
@auth_router.post("/login", response_model=LoginResponse, tags=["auth"])
async def login(user_data: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    # Поиск пользователя
    result = await db.execute(select(Users).where(Users.username == user_data.username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    # Проверка пароля (без хеширования пока)
    if user.password != user_data.password:
        raise HTTPException(status_code=401, detail="Неверный пароль")

    return LoginResponse(
        message="Успешный вход в систему",
        user_id=user.id,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname
    )


# ✅ Новый роут для регистрации
@auth_router.post("/register", response_model=RegisterResponse, tags=["auth"])
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_async_db)):
    # Проверяем, существует ли пользователь
    result = await db.execute(select(Users).where(Users.username == user_data.username))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    # Создаем нового пользователя БЕЗ slug (пароль НЕ хешируем пока)
    new_user = Users(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        age=user_data.age,
        password=user_data.password  # Сохраняем как есть, без хеширования
    )

    # Сохраняем в БД для получения ID
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Создаем уникальный slug ПОСЛЕ получения ID
    user_slug = f"{slugify(user_data.username)}-{new_user.id}"
    new_user.slug = user_slug

    # Обновляем пользователя с slug
    await db.commit()
    await db.refresh(new_user)

    return RegisterResponse(
        message="Пользователь успешно зарегистрирован",
        user_id=new_user.id,
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        age=new_user.age,
        slug=new_user.slug
    )


