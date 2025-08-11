from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.auth.auth_user import auth_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.task_r import router_task
from app.routers.user_r import router_user
from app.backend.db_depends import get_async_db
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - здесь размещаем все действия при запуске
    print("🚀 Запуск приложения...")
    print("📊 Создание таблиц в базе данных...")
    await create_tables()
    print("✅ Таблицы созданы успешно!")
    print("🎯 Task Manager API готов к работе!")
    print("Приложение запущено")
    print("API доступно:")
    print("  - С префиксом /api: http://localhost:8000/api/")
    print("  - Без префикса (для прокси): http://localhost:8000/")
    print("  - Swagger UI: http://localhost:8000/docs")

    yield  # ← Приложение работает

    # Shutdown - здесь можно добавить действия при остановке
    print("👋 Остановка приложения...")

app = FastAPI(
    title="TaskManager API",
    description="API для управления задачами и пользователями",
    version="1.0.0"
)
origins = [
    "http://localhost:3000"
]

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Подключаем роутеры с префиксом /api (для Swagger и прямых запросов)
app.include_router(router_user, prefix="/api")
app.include_router(router_task, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Дублирующие роутеры БЕЗ префикса (для React прокси)
app.include_router(router_user, prefix="", tags=["users-proxy"])
app.include_router(router_task, prefix="", tags=["tasks-proxy"])
app.include_router(auth_router, prefix="", tags=["auth-proxy"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Добро пожаловать в TaskManager API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": "1.0.0"
    }

@app.get("/api/", tags=["root"])
async def api_root():
    return {
        "message": "TaskManager API работает!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": "1.0.0"
    }

# Раздача статических файлов React из папки build
app.mount("/static", StaticFiles(directory="build/static"), name="static")

from fastapi import HTTPException

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api") or full_path.startswith("static"):
        raise HTTPException(status_code=404)
    index_path = os.path.join("build", "index.html")
    return FileResponse(index_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
