import logging
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import and_
from slugify import slugify
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.models.task_m import Tasks
from app.schemas.task_s import TaskResponse, CreateTask, UpdateTask


async def get_all_tasks(skip: int, limit: int, db: Session):
    result = await db.execute(select(Tasks).offset(skip).limit(limit))
    tasks = result.scalars().all()
    return tasks


async def get_task_by_id(task_id: int, db: Session):
    result = await db.execute(select(Tasks).where(Tasks.id == task_id))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


logger = logging.getLogger(__name__)


async def create_task(task: CreateTask, db: Session):
    print(f"🚀 create_task вызвана для задачи: {task.title}")

    # Генерируем базовый slug
    base_slug = slugify(task.title)
    print(f"🔧 Базовый slug: {base_slug}")

    # Проверяем уникальность slug
    slug_result = await db.execute(select(Tasks).where(Tasks.slug == base_slug))
    existing_slug = slug_result.scalars().first()

    if existing_slug:
        timestamp = int(datetime.now().timestamp())
        unique_slug = f"{base_slug}-{timestamp}"
        print(f"🔧 Slug занят, создаю уникальный: {unique_slug}")
    else:
        unique_slug = base_slug
        print(f"🔧 Slug свободен: {unique_slug}")

    db_task = Tasks(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed,
        user_id=task.user_id,
        slug=unique_slug
    )

    print(f"🎯 Создаю задачу со slug: {unique_slug}")

    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    print(f"✅ Задача создана с ID: {db_task.id}, slug: {db_task.slug}")
    return db_task


async def update_task(task_id: int, task: UpdateTask, db: Session):
    result = await db.execute(select(Tasks).where(Tasks.id == task_id))
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(task_id: int, db: Session):
    """
    Удаляет задачу по указанному ID.

    Args:
        task_id: ID задачи для удаления
        db: Сессия базы данных

    Returns:
        dict: Сообщение об успешном удалении

    Raises:
        HTTPException: Если задача не найдена или произошла ошибка
    """
    try:
        # Поиск задачи по ID
        result = await db.execute(select(Tasks).where(Tasks.id == task_id))
        db_task = result.scalar_one_or_none()

        # Проверка существования задачи
        if db_task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        # Удаление задачи
        await db.delete(db_task)  # Добавлен await
        await db.commit()

        return {"detail": "Task deleted successfully"}

    except HTTPException:
        # Пробрасываем HTTPException дальше
        raise

    except Exception as e:
        # Обработка непредвиденных ошибок
        await db.rollback()  # Откат транзакции при ошибке
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting task: {str(e)}"
        )


async def delete_tasks_by_user(user_id: int, db: Session):
    """Удаляет все задачи, связанные с указанным пользователем"""
    try:
        result = await db.execute(select(Tasks).where(Tasks.user_id == user_id))
        tasks = result.scalars().all()

        for task in tasks:
            await db.delete(task)  # Удаляем каждую задачу

        return len(tasks)  # Возвращаем количество удаленных задач

    except Exception as e:
        # Логируем ошибку
        print(f"Error in delete_tasks_by_user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting tasks: {str(e)}"
        )
