import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.task_r import router_task
from app.routers.user_r import router_user
from app.backend.db_depends import get_async_db

# Создаем экземпляр FastAPI
app = FastAPI(
    title="TaskManager API",
    description="API для управления задачами и пользователями",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(router_user, prefix="/api/users", tags=["users"])
app.include_router(router_task, prefix="/api/tasks", tags=["tasks"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Добро пожаловать в TaskManager API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Обработчик запуска без создания таблиц
@app.on_event("startup")
async def startup_event():
    print("Приложение запущено")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
