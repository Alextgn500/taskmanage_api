# Task Manager API

RESTful API для управления задачами, разработанное с использованием FastAPI и SQLAlchemy.

## Функциональность

- Создание, чтение, обновление и удаление задач
- Управление пользователями
- Асинхронная работа с базой данных
- Документация API через Swagger UI

## Технологии

- FastAPI
- SQLAlchemy (асинхронный режим)
- PostgreSQL
- Pydantic для валидации данных
- Alembic для миграций базы данных

## Установка и запуск

1. Клонировать репозиторий:
   
git clone https://github.com/Alextgn500/taskmanage_api.git
cd taskmanager_api


2. Создать виртуальное окружение:
   
python -m venv newvenv
newvenv\Scripts\activate


3. Установить зависимости:
   
   pip install -r requirements.txt


4. Настроить переменные окружения (создать файл .env)

5. Запустить миграции:
   
   alembic upgrade head


6. Запустить сервер:
   
 uvicorn app.main:app --reload


7. Открыть документацию API:
   
 http://localhost:8000/docs