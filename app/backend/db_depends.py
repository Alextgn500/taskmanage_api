from app.backend.db import AsyncSessionLocal

async def get_async_db():
    """
    Зависимость для получения асинхронной сессии БД в FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
