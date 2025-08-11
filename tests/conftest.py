import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from main import app
from app.backend.db_depends import get_async_db
from app.backend.base import Base

# Синхронная база для создания таблиц и очистки
SYNC_DATABASE_URL = "sqlite:///./test.db"
sync_engine = create_engine(SYNC_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Асинхронная база для работы приложения
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
async_engine = create_async_engine(ASYNC_DATABASE_URL, connect_args={"check_same_thread": False})

# Асинхронная сессия
TestingAsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def override_get_async_db():
    """Переопределение асинхронной зависимости для тестов"""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создание тестовой базы данных"""
    Base.metadata.create_all(bind=sync_engine)
    yield
    Base.metadata.drop_all(bind=sync_engine)


@pytest.fixture(autouse=True)
def clean_db():
    """Синхронная очистка базы данных перед каждым тестом"""
    with TestingSyncSessionLocal() as session:
        try:
            # Удаляем все данные из таблиц
            session.execute(text("DELETE FROM tasks"))
            session.execute(text("DELETE FROM users"))
            session.commit()
        except Exception as e:
            print(f"Ошибка очистки БД: {e}")
            session.rollback()


@pytest.fixture
def test_client():
    """Фикстура для тестового клиента"""
    app.dependency_overrides[get_async_db] = override_get_async_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session():
    """Асинхронная фикстура для сессии базы данных"""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "age": 25,
        "password": "password123"
    }


@pytest.fixture
def test_task_data():
    return {
        "title": "Test Task",
        "content": "This is a test task",
        "priority": 1,
        "completed": False,
        "user_id": 1
    }
