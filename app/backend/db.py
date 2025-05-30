from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.backend.base import Base
from app.models.user_m import Users
from app.models.task_m import Tasks

# Асинхронное подключение к базе данных
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:000@localhost:5432/my_db"
async_engine = create_async_engine(ASYNC_DATABASE_URL)

# Создаем фабрику асинхронных сессий с использованием async_sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Функция для проверки регистрации моделей
def check_registered_models():
    """
    Проверяет, что все модели правильно зарегистрированы в Base.metadata
    """
    tables = Base.metadata.tables
    print(f"Зарегистрированные таблицы: {', '.join(tables.keys())}")
    return len(tables) > 0


async def async_create_tables():
    """
    Асинхронно создает все таблицы в базе данных
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Асинхронно созданы таблицы в базе данных")


if __name__ == "__main__":
    # Проверяем модели перед созданием таблиц
    check_registered_models()

    # Асинхронное создание таблиц
    import asyncio

    asyncio.run(async_create_tables())

