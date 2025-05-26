from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_
from slugify import slugify
from fastapi import HTTPException

from app.models.task_m import Tasks
from app.schemas.task_s import TaskResponse, CreateTask


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


def create_task(task: CreateTask, db: Session):
    existing_task = db.query(Tasks).filter(Tasks.title == task.title).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Задача с таким заголовком уже существует")

    task_slug = slugify(task.title)

    db_task = Tasks(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed,
        user_id=task.user_id,
        slug=task_slug
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(task_id: int, task: CreateTask, db: Session):
    result = db.execute(select(Tasks).where(Tasks.id == task_id))
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(task_id: int, db: Session):
    result = db.execute(select(Tasks).where(Tasks.id == task_id))
    db_task = result.scalar_one_or_none()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}